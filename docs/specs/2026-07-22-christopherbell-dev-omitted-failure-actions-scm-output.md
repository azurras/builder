# ChristopherBell.dev Omitted Failure-Actions SCM Output

## Document Status

`ready-for-execution`

## Purpose

Correct the Windows production recovery-policy verifier so it accepts the exact canonical `sc.exe qfailure` representation produced after recovery actions are disabled, without weakening the service-stop safety gate.

## Background

PR 1223, merged as `bebd4cd9c3f9c37eab8cb311484e018e35834d6d`, corrected the suspended recovery reset period from `3600` to `0` and hardened recovery-output parsing. A guarded exact-release production retry then failed before the website stop with:

```text
Suspended recovery policy verification failed. Expected reset period 0 seconds and actions none; received reset period 0 and actions none.
```

The reviewed rollback completed successfully. It removed the stopped media worker and enable flag, preserved both shared roots, restored normal recovery, and confirmed HTTP 200. The active production release is the merged PR 1223 commit.

An elevated evidence-only probe reproduced the failure without stopping or restarting the website. It captured the exact 196-byte suspended query output and restored normal recovery in `finally`. The live suspended output contains:

```text
[SC] QueryServiceConfig2 SUCCESS

SERVICE_NAME: ChristopherBellDev
        RESET_PERIOD (in seconds)    : 0
        REBOOT_MESSAGE               :
        COMMAND_LINE                 :
```

Windows omits the `FAILURE_ACTIONS` field entirely when the service has no configured recovery actions. The test fixture introduced by PR 1223 instead rendered an empty labeled field, so the parser's exact-one-field requirement rejected the real canonical state.

## Goals

- Accept the production-observed suspended representation: one reset field with value `0`, no `FAILURE_ACTIONS` label, no delay lines, and no parsed actions.
- Keep normal recovery verification exact: one reset field with value `3600`, one labeled first restart at 10 seconds, and one unlabeled continuation restart at 30 seconds.
- Reject any labeled failure-actions field in suspended output, including an empty field, an unknown action, duplicates, or delay lines.
- Preserve bounded SCM commands, stop gating, unconditional normal-policy restoration, stop postconditions, and causal error aggregation.
- Prove the correction with the captured live-output shape before another production retry.

## Non-Goals

- Do not accept both omitted and empty `FAILURE_ACTIONS` fields for suspended policy.
- Do not infer suspended state solely from the absence of parsed restart actions.
- Do not change reset values, normal recovery actions, WinSW configuration, worker lifecycle, application code, permissions, storage, UI, or media behavior.
- Do not patch production files directly or deploy unmerged code.
- Do not delete or alter shared-folder contents.

## Requirements

### Suspended policy

- `RESET_PERIOD (in seconds)` must appear exactly once and parse as `0`.
- `FAILURE_ACTIONS` must not appear.
- No `-- Delay =` fragment or recognized action line may appear.
- Missing reset, nonzero reset, duplicate reset, any action label, any recognized action, or any delay fragment must fail closed.

### Normal policy

- `RESET_PERIOD (in seconds)` must appear exactly once and parse as `3600`.
- `FAILURE_ACTIONS` must appear exactly once on the first restart line.
- The first action must be `RESTART` with delay `10000` milliseconds.
- The sole continuation action must be `RESTART` with delay `30000` milliseconds.
- Missing, duplicated, malformed, reordered, additional, or unrecognized fields must fail closed.

### Operational safety

- A suspended verification failure must prevent `Stop-Service`.
- Every suspension attempt must restore and verify normal recovery.
- Recovery commands must remain bounded.
- A restoration failure must retain both the primary and restoration causes.
- The guarded production retry must pin the merged commit and tree under the deployment lock.
- Any production failure must run the reviewed rollback and prove the disabled baseline.

## Proposed Approach

Use the existing policy-specific parser boundary in `Assert-ProductionWebsiteRecoveryPolicy`.

- Continue counting labeled `FAILURE_ACTIONS` fields independently from recognized action lines.
- Change only the suspended branch from requiring exactly one empty labeled field to requiring zero labeled fields.
- Update the suspended fixture to omit the field, matching the captured Windows output.
- Add a regression proving the former empty-field fixture is rejected, so the accepted representation remains one strict canonical state rather than a widened compatibility set.
- Preserve the normal branch and every mutation, restoration, timeout, and service-stop path unchanged.

Alternatives rejected:

- Accept omitted or empty fields: broader than the production-observed contract and would create two trusted suspended representations.
- Ignore field cardinality and rely only on zero recognized actions: would permit malformed or unknown action fields to cross the validation boundary.

## Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: suspended failure-action label cardinality.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: live-shaped suspended fixture and strict negative regression.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\suspended-qfailure-output.txt`: captured production evidence; temporary and not committed.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`: immutable identifier refresh after merge.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`: matching rollback identifier refresh after merge.

## Validation Plan

- RED: feed the captured live output shape to the current verifier and require the existing rejection.
- GREEN: require the same live-shaped fixture to pass after the one-branch parser correction.
- Require an empty labeled suspended `FAILURE_ACTIONS` field to fail.
- Preserve reset mismatch, duplicate reset, unknown/duplicate action, timeout, stop-gating, normal restoration, and causal-error tests.
- Run focused `Production.Deploy.Tests.ps1`, full Windows Pester, PowerShell parser checks, `git diff --check`, exact two-file scope, and an isolated clean Gradle build.
- Complete independent task and whole-branch reviews with no unresolved findings.
- Require all GitHub Actions and CodeQL checks before squash merge.
- Refresh immutable rollout identifiers, complete read-only preflight, and rerun guarded elevated deployment.
- Require infrastructure acceptance followed by authenticated `/shared` listing, download-byte, and applicable progressive-playback browser checks.

## Rollback

Use the existing reviewed rollback script pinned to the same merged tree. It removes the enable flag, proves or reloads a disabled runtime, removes or fail-safe disables the worker, and verifies website/dependency/listener/recovery/root health without deleting shared data.

## Open Questions

None.
