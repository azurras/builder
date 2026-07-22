# ChristopherBell.dev Suspended Recovery Reset Normalization Specification

## Document Status

Approved.

## Purpose

Make the controlled Windows website stop accept and deliberately request the Service Control Manager representation used when all recovery actions are suspended, without weakening restoration of the normal recovery policy.

## Background

The guarded shared-folder production deployment reached its pinned release switch and failed before stopping `ChristopherBellDev`. `Set-ProductionWebsiteRecoveryPolicy` requested an empty recovery action list with reset period `3600`. Windows accepted the mutation but `sc.exe qfailure ChristopherBellDev` reported reset period `0` and no actions. The verifier required reset period `3600` for both suspended and normal policies, so it rejected the valid suspended representation, restored the normal policy, and aborted before service stop.

The prepared rollback then restored the safe baseline and proved:

- `ChristopherBellDev`, MongoDB, and cloudflared are Running.
- The homepage returns HTTP 200.
- Website recovery is reset period 3600 with restart delays 10 and 30 seconds.
- `ChristopherBellMediaWorker` and `APP_SHARED_FOLDER_ENABLED` are absent.
- `A:\Shared` and `A:\Shared-System` are preserved.

## Goals

- Model suspended recovery as reset period `0` with no recovery actions.
- Keep normal recovery exactly reset period `3600` with `RESTART:10000` and `RESTART:30000`.
- Send `reset= 0` when suspending so requested and observed SCM state are identical.
- Add behavioral regression coverage using the observed Windows `qfailure` representation.
- Preserve bounded recovery mutations and queries, stop gating, normal-policy restoration, and causal error handling.
- Complete TDD, independent review, PR, CI, merge, guarded production retry, browser acceptance, and Builder closeout.

## Non-Goals

- No change to WinSW versions, worker reinstall behavior, website application code, shared-folder permissions, or media behavior.
- No relaxation of normal recovery verification.
- No direct production patch outside the merged exact-SHA deployment workflow.
- No worker or website mutation before the follow-up fix passes review and CI.

## Requirements

### Suspended policy

- `Set-ProductionWebsiteRecoveryPolicy -Policy Suspended` invokes `sc.exe failure ChristopherBellDev reset= 0 actions= ''` through the existing bounded process boundary.
- Verification requires reset period exactly `0`.
- Verification requires an explicitly empty `FAILURE_ACTIONS` field, zero delay lines, and zero parsed actions.
- A missing reset period, any nonzero reset period, any action, or any delay line fails closed before `Stop-Service`.

### Normal policy

- Normal mutation remains `reset= 3600 actions= restart/10000/restart/30000`.
- Normal verification continues to require reset period exactly `3600` and the two ordered restart actions.
- Every suspended-policy attempt still reaches the normal-policy restoration path before return or throw.

### Diagnostics

- Verification errors state the policy-specific expected reset period.
- The production-discovered `reset period 0 and actions none` output is accepted only for `Suspended`, never for `Normal`.
- A suspended reset period such as `42` remains a mismatch and blocks service stop.

## Proposed Approach

Keep the existing two-state `Suspended`/`Normal` boundary. Derive the requested and expected reset period from the policy: `0` for `Suspended`, `3600` for `Normal`. Update the recovery-query test fixture so its default output matches Windows: suspended queries report `0`, normal queries report `3600`. Add a focused RED assertion against the observed suspended output before changing the module, then update command-argument and diagnostic expectations.

Do not accept both `0` and `3600` for suspended state. A single canonical representation keeps mutation, observation, tests, and operator diagnostics aligned.

## Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: derive policy-specific reset mutation, verification, and error text.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: model Windows normalization and prove suspended/normal separation plus controlled-stop ordering.
- Temporary guarded scripts under `A:\Temp\cbdev-shared-folder-production-20260722-064200`: update only after the fix is merged, using the new exact merge SHA/tree.

## Validation Plan

- Capture RED evidence showing observed suspended output with reset `0` is rejected before the module edit.
- Pass focused controlled-stop Pester tests with explicit failed-count handling.
- Pass the complete Windows production Pester suite.
- Pass PowerShell parser checks and `git diff --check`.
- Pass a clean isolated Gradle build.
- Complete independent task and whole-branch Review Mode passes with no Critical or Important findings.
- Pass GitHub Ubuntu, macOS, Windows, and CodeQL checks.
- Retry the exact-SHA/tree guarded production installer, including both worker install passes, pinned deployment, installed-worker acceptance, startup verification, and separate authenticated browser acceptance.

## Rollback and Recovery

- Production is already at the verified safe baseline before this change.
- Before merge, production remains unchanged.
- During the next rollout, any failed postcondition runs the reviewed rollback script and must re-prove the safe baseline.
- Never delete shared roots, shared data, prior releases, MongoDB data, or cloudflared configuration.

## Risks

- Treating reset `0` as suspended must not leak into normal recovery; policy-specific tests enforce separation.
- Another Windows version could format `qfailure` differently; the parser remains label-based and still fails closed on missing or ambiguous fields.
- A future recovery-action design could give reset period meaning while suspended; that requires a new explicit policy rather than widening this verifier.

## Open Questions

None.
