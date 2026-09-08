# 2026-07-22 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/specs/2026-07-22-christopherbell-dev-controlled-service-stop.md](#source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md)
- [docs/specs/2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output.md](#source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md)
- [docs/specs/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md](#source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md)
- [docs/specs/2026-07-22-christopherbell-dev-winsw2-worker-reinstall.md](#source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md)
- [docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-merge-review.md](#source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md)
- [docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review.md](#source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md)
- [docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-merge-update.md](#source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md)
- [docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update.md](#source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md)

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md"></a>
## 2026-07-22 | specs | christopherbell.dev Controlled Windows Service Stop Spec

Original source: `docs/specs/2026-07-22-christopherbell-dev-controlled-service-stop.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `dd0785d4ff1bab04bec97a40f7279200c37d07d05b5db6a873f88b166e66c060`.

<!-- migrated-source: docs/specs/2026-07-22-christopherbell-dev-controlled-service-stop.md -->
<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--christopherbelldev-controlled-windows-service-stop-spec"></a>
### christopherbell.dev Controlled Windows Service Stop Spec

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--document-status"></a>
#### Document Status

Ready for review.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--purpose"></a>
#### Purpose

Make planned production deployments and deployment rollbacks stop the native Windows website service safely even when WinSW 2.12.0 exits with its known invalid-handle failure after the child process has already stopped.

This work unblocks the shared-folder production rollout without changing shared-folder permissions, storage, previews, transcoding, or user-facing behavior.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--background"></a>
#### Background

The native Windows production site runs as the `ChristopherBellDev` service. The repository configures Service Control Manager recovery to restart the service after 10 seconds and then 30 seconds, with failures reset after one hour.

During the approved shared-folder production deployment, `Stop-Service ChristopherBellDev -ErrorAction Stop` failed. Windows application events showed WinSW 2.12.0 throwing `System.ComponentModel.Win32Exception (6): The handle is invalid` while enumerating the child process tree during `WrapperService.OnStop()`. The child PowerShell process had exited successfully, but the wrapper crash caused Service Control Manager recovery to restart the website while the deployment was attempting to switch releases.

The deployment was rolled back. The production website is online, the shared-folder worker is absent, the feature remains disabled, and `A:\Shared` plus `A:\Shared-System` remain intact.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--goals"></a>
#### Goals

- Give planned deployment and rollback stops one bounded, explicit service-stop boundary.
- Prevent Service Control Manager recovery from racing an intentional release switch.
- Accept a thrown stop command only when independent postconditions prove the service actually stopped.
- Restore the repository-owned recovery policy before any production restart.
- Preserve the original deployment or rollback failure when cleanup also fails, while reporting cleanup context.
- Keep normal automatic crash recovery enabled outside the short planned-stop window.
- Unblock a safe retry of the shared-folder production installation.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--non-goals"></a>
#### Non-Goals

- Upgrade WinSW to a 3.x prerelease.
- Replace WinSW or the native Windows service architecture.
- Add a public or remotely callable shutdown endpoint.
- Change the website application's shutdown behavior.
- Change shared-folder application code, permissions, files, or media behavior.
- Suppress arbitrary service-stop failures based only on exception text.
- Disable automatic recovery permanently.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--planned-stop-boundary"></a>
##### Planned Stop Boundary

1. A named production helper must own the complete intentional-stop transition for `ChristopherBellDev`.
2. The helper must first install a temporary no-restart recovery policy through the existing checked-process boundary.
3. The helper must request a normal service stop. It must not force-kill the website as the default path.
4. The helper must wait for a bounded stopped state using service state, not an arbitrary sleep.
5. The helper must also prove that the configured production port is no longer accepting connections before a release junction may change.
6. A `Stop-Service` exception may be accepted only when both stopped-state and closed-port postconditions pass within their bounds.
7. If either postcondition fails, the helper must fail closed and preserve the stop exception as causal context when one exists.
8. The helper must restore the repository-owned recovery policy in a `finally` path before returning or throwing.
9. Failure to restore the recovery policy is a deployment-blocking infrastructure failure. The service must not be restarted until recovery restoration succeeds.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--recovery-policy"></a>
##### Recovery Policy

The repository remains the source of truth for the website service recovery policy:

- first failure: restart after 10 seconds;
- second failure: restart after 30 seconds;
- reset failure count after one hour.

The temporary policy must contain no automatic restart actions. The normal policy must be reapplied and checked before `Start-Service ChristopherBellDev` is allowed.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--deployment-and-rollback-integration"></a>
##### Deployment and Rollback Integration

- `Switch-ProductionRelease` must use the controlled stop before changing the `current` junction.
- Its rollback path must use the same controlled stop before restoring the former junction.
- Any other production operation changed in this task must call the same boundary instead of duplicating recovery-policy sequencing.
- Existing deployment locking, candidate verification, atomic junction switching, endpoint verification, and former-release restoration behavior must remain intact.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--diagnostics-and-security"></a>
##### Diagnostics and Security

- Errors must identify the failed phase: suspend recovery, request stop, prove stopped state, prove closed port, restore recovery, start service, or verify endpoints.
- Diagnostic output must not include environment secrets, service credentials, or command lines containing secrets.
- Service name, port, timeouts, and recovery actions must be explicit at the boundary and validated before effects occur.
- Unexpected service states, command failures, and port-probe failures must remain fatal.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--proposed-approach"></a>
#### Proposed Approach

Add one focused helper to the existing Windows deployment module. It will perform this state transition:

1. Validate the service name, production port, and bounded timeouts.
2. Apply a temporary recovery policy with no restart actions.
3. Request a normal service stop and retain any thrown exception.
4. Wait until Service Control Manager reports `Stopped`.
5. Verify the production port is closed.
6. Restore and verify the normal recovery policy in `finally`.
7. Return only when every postcondition passes; otherwise throw a phase-specific failure with the original cause retained.

`Switch-ProductionRelease` will call this helper for both the forward switch and rollback. The release junction will never change until the stop boundary succeeds, and `Start-Service` will never run while recovery is still suspended.

The design deliberately contains the WinSW 2.12.0 failure at the deployment boundary. It does not identify success by matching WinSW's exception message. It identifies success from independently observable Windows service and network postconditions.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--files-and-modules-involved"></a>
#### Files and Modules Involved

- `ops/production/windows/modules/Production.Deploy.psm1`: controlled stop boundary and release-switch integration.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: focused behavioral regressions for the known wrapper failure and fail-closed paths.
- `ops/production/windows/modules/Production.Operations.psm1`: inspect for any restart path that must share the boundary; change only if required to prevent duplicated unsafe stop behavior.
- Existing aggregate Windows operations tests and production acceptance scripts: regression and live verification evidence.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--red-evidence"></a>
##### RED Evidence

Before production code changes, add a focused Pester regression in which `Stop-Service` throws after the service reaches `Stopped`. The existing implementation must fail the deployment instead of accepting the independently proven stop.

Add failure cases proving that the deployment remains blocked when:

- the service does not reach `Stopped`;
- the production port remains open;
- temporary recovery configuration fails;
- normal recovery restoration fails; or
- rollback encounters the same wrapper failure without satisfying postconditions.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--green-evidence"></a>
##### GREEN Evidence

- Run the focused `Production.Deploy.Tests.ps1` suite.
- Run the complete Windows production Pester suite.
- Run repository formatting, static checks, and the aggregate project verification required for production scripts.
- Review the final production and test diff against the Jane Street-style review rubric.
- Obtain an independent spoke review before merge.
- Require all GitHub pull-request checks to pass before merge.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--production-acceptance"></a>
##### Production Acceptance

After merge, retry the prepared shared-folder deployment with the exact merged commit and tree. Acceptance requires:

- the planned website stop completes without an automatic recovery race;
- the release switch and website restart succeed;
- the normal website recovery policy is installed after restart;
- `ChristopherBellDev` is running and the public home page returns HTTP 200;
- the shared-folder worker is installed under its intended least-privilege account and is running;
- `A:\Shared` and `A:\Shared-System` are preserved;
- the active release matches the merged commit and tree;
- `/shared` loads for an authorized session;
- the anonymous shared-folder API remains unauthorized;
- the installed-worker acceptance check passes; and
- startup verification passes.

If acceptance fails, run the prepared rollback, confirm the public site is healthy, confirm the worker and feature flag are absent, and confirm both shared-folder roots remain preserved.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- **Recovery remains suspended after an unexpected failure:** restoration runs in `finally`, blocks restart on failure, and is verified by tests plus live inspection.
- **A wrapper exception hides a real stop failure:** exception text is never sufficient; stopped-state and closed-port postconditions are mandatory.
- **A port closes before the service fully stops:** both service state and port state must pass.
- **A service reports stopped while a child still owns the port:** the closed-port postcondition catches the leaked process.
- **Rollback repeats the same race:** forward and rollback paths share one controlled boundary.
- **Operational code becomes broader than needed:** keep the change within the existing deployment modules and avoid wrapper upgrades or application shutdown APIs.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--completion-criteria"></a>
#### Completion Criteria

- The focused regression is witnessed failing before the production edit and passing afterward.
- All focused and aggregate Windows production tests pass.
- The implementation plan, code diff, and evidence pass Builder validation and independent review.
- The spoke change is committed, pushed, merged, and recorded in Builder.
- Production acceptance passes with normal recovery restored.
- The shared-folder production rollout is enabled without modifying or losing the existing shared folders.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-controlled-service-stop-md--open-questions"></a>
#### Open Questions

None. The user approved the controlled-stop approach on 2026-07-22.

<!-- /migrated-source: docs/specs/2026-07-22-christopherbell-dev-controlled-service-stop.md -->

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md"></a>
## 2026-07-22 | specs | ChristopherBell.dev Omitted Failure-Actions SCM Output

Original source: `docs/specs/2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `bf8e1f58d1c506fbff8c8387db0c2d54c6d955bf2a71bbacb2288cc47e062d45`.

<!-- migrated-source: docs/specs/2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output.md -->
<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--christopherbelldev-omitted-failure-actions-scm-output"></a>
### ChristopherBell.dev Omitted Failure-Actions SCM Output

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--document-status"></a>
#### Document Status

`ready-for-execution`

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--purpose"></a>
#### Purpose

Correct the Windows production recovery-policy verifier so it accepts the exact canonical `sc.exe qfailure` representation produced after recovery actions are disabled, without weakening the service-stop safety gate.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--background"></a>
#### Background

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

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--goals"></a>
#### Goals

- Accept the production-observed suspended representation: one reset field with value `0`, no `FAILURE_ACTIONS` label, no delay lines, and no parsed actions.
- Keep normal recovery verification exact: one reset field with value `3600`, one labeled first restart at 10 seconds, and one unlabeled continuation restart at 30 seconds.
- Reject any labeled failure-actions field in suspended output, including an empty field, an unknown action, duplicates, or delay lines.
- Preserve bounded SCM commands, stop gating, unconditional normal-policy restoration, stop postconditions, and causal error aggregation.
- Prove the correction with the captured live-output shape before another production retry.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--non-goals"></a>
#### Non-Goals

- Do not accept both omitted and empty `FAILURE_ACTIONS` fields for suspended policy.
- Do not infer suspended state solely from the absence of parsed restart actions.
- Do not change reset values, normal recovery actions, WinSW configuration, worker lifecycle, application code, permissions, storage, UI, or media behavior.
- Do not patch production files directly or deploy unmerged code.
- Do not delete or alter shared-folder contents.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--suspended-policy"></a>
##### Suspended policy

- `RESET_PERIOD (in seconds)` must appear exactly once and parse as `0`.
- `FAILURE_ACTIONS` must not appear.
- No `-- Delay =` fragment or recognized action line may appear.
- Missing reset, nonzero reset, duplicate reset, any action label, any recognized action, or any delay fragment must fail closed.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--normal-policy"></a>
##### Normal policy

- `RESET_PERIOD (in seconds)` must appear exactly once and parse as `3600`.
- `FAILURE_ACTIONS` must appear exactly once on the first restart line.
- The first action must be `RESTART` with delay `10000` milliseconds.
- The sole continuation action must be `RESTART` with delay `30000` milliseconds.
- Missing, duplicated, malformed, reordered, additional, or unrecognized fields must fail closed.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--operational-safety"></a>
##### Operational safety

- A suspended verification failure must prevent `Stop-Service`.
- Every suspension attempt must restore and verify normal recovery.
- Recovery commands must remain bounded.
- A restoration failure must retain both the primary and restoration causes.
- The guarded production retry must pin the merged commit and tree under the deployment lock.
- Any production failure must run the reviewed rollback and prove the disabled baseline.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--proposed-approach"></a>
#### Proposed Approach

Use the existing policy-specific parser boundary in `Assert-ProductionWebsiteRecoveryPolicy`.

- Continue counting labeled `FAILURE_ACTIONS` fields independently from recognized action lines.
- Change only the suspended branch from requiring exactly one empty labeled field to requiring zero labeled fields.
- Update the suspended fixture to omit the field, matching the captured Windows output.
- Add a regression proving the former empty-field fixture is rejected, so the accepted representation remains one strict canonical state rather than a widened compatibility set.
- Preserve the normal branch and every mutation, restoration, timeout, and service-stop path unchanged.

Alternatives rejected:

- Accept omitted or empty fields: broader than the production-observed contract and would create two trusted suspended representations.
- Ignore field cardinality and rely only on zero recognized actions: would permit malformed or unknown action fields to cross the validation boundary.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--files-and-modules"></a>
#### Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: suspended failure-action label cardinality.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: live-shaped suspended fixture and strict negative regression.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\suspended-qfailure-output.txt`: captured production evidence; temporary and not committed.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`: immutable identifier refresh after merge.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`: matching rollback identifier refresh after merge.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--validation-plan"></a>
#### Validation Plan

- RED: feed the captured live output shape to the current verifier and require the existing rejection.
- GREEN: require the same live-shaped fixture to pass after the one-branch parser correction.
- Require an empty labeled suspended `FAILURE_ACTIONS` field to fail.
- Preserve reset mismatch, duplicate reset, unknown/duplicate action, timeout, stop-gating, normal restoration, and causal-error tests.
- Run focused `Production.Deploy.Tests.ps1`, full Windows Pester, PowerShell parser checks, `git diff --check`, exact two-file scope, and an isolated clean Gradle build.
- Complete independent task and whole-branch reviews with no unresolved findings.
- Require all GitHub Actions and CodeQL checks before squash merge.
- Refresh immutable rollout identifiers, complete read-only preflight, and rerun guarded elevated deployment.
- Require infrastructure acceptance followed by authenticated `/shared` listing, download-byte, and applicable progressive-playback browser checks.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--rollback"></a>
#### Rollback

Use the existing reviewed rollback script pinned to the same merged tree. It removes the enable flag, proves or reloads a disabled runtime, removes or fail-safe disables the worker, and verifies website/dependency/listener/recovery/root health without deleting shared data.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output-md--open-questions"></a>
#### Open Questions

None.

<!-- /migrated-source: docs/specs/2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output.md -->

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md"></a>
## 2026-07-22 | specs | ChristopherBell.dev Suspended Recovery Reset Normalization Specification

Original source: `docs/specs/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4103d1d3721b99e4b8ace8d468853ebd90b0dafa0920669829e44c84008b6b1c`.

<!-- migrated-source: docs/specs/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md -->
<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--christopherbelldev-suspended-recovery-reset-normalization-specification"></a>
### ChristopherBell.dev Suspended Recovery Reset Normalization Specification

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--document-status"></a>
#### Document Status

Approved.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--purpose"></a>
#### Purpose

Make the controlled Windows website stop accept and deliberately request the Service Control Manager representation used when all recovery actions are suspended, without weakening restoration of the normal recovery policy.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--background"></a>
#### Background

The guarded shared-folder production deployment reached its pinned release switch and failed before stopping `ChristopherBellDev`. `Set-ProductionWebsiteRecoveryPolicy` requested an empty recovery action list with reset period `3600`. Windows accepted the mutation but `sc.exe qfailure ChristopherBellDev` reported reset period `0` and no actions. The verifier required reset period `3600` for both suspended and normal policies, so it rejected the valid suspended representation, restored the normal policy, and aborted before service stop.

The prepared rollback then restored the safe baseline and proved:

- `ChristopherBellDev`, MongoDB, and cloudflared are Running.
- The homepage returns HTTP 200.
- Website recovery is reset period 3600 with restart delays 10 and 30 seconds.
- `ChristopherBellMediaWorker` and `APP_SHARED_FOLDER_ENABLED` are absent.
- `A:\Shared` and `A:\Shared-System` are preserved.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--goals"></a>
#### Goals

- Model suspended recovery as reset period `0` with no recovery actions.
- Keep normal recovery exactly reset period `3600` with `RESTART:10000` and `RESTART:30000`.
- Send `reset= 0` when suspending so requested and observed SCM state are identical.
- Add behavioral regression coverage using the observed Windows `qfailure` representation.
- Preserve bounded recovery mutations and queries, stop gating, normal-policy restoration, and causal error handling.
- Complete TDD, independent review, PR, CI, merge, guarded production retry, browser acceptance, and Builder closeout.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--non-goals"></a>
#### Non-Goals

- No change to WinSW versions, worker reinstall behavior, website application code, shared-folder permissions, or media behavior.
- No relaxation of normal recovery verification.
- No direct production patch outside the merged exact-SHA deployment workflow.
- No worker or website mutation before the follow-up fix passes review and CI.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--suspended-policy"></a>
##### Suspended policy

- `Set-ProductionWebsiteRecoveryPolicy -Policy Suspended` invokes `sc.exe failure ChristopherBellDev reset= 0 actions= ''` through the existing bounded process boundary.
- Verification requires reset period exactly `0`.
- Verification requires an explicitly empty `FAILURE_ACTIONS` field, zero delay lines, and zero parsed actions.
- A missing reset period, any nonzero reset period, any action, or any delay line fails closed before `Stop-Service`.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--normal-policy"></a>
##### Normal policy

- Normal mutation remains `reset= 3600 actions= restart/10000/restart/30000`.
- Normal verification continues to require reset period exactly `3600` and the two ordered restart actions.
- Every suspended-policy attempt still reaches the normal-policy restoration path before return or throw.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--diagnostics"></a>
##### Diagnostics

- Verification errors state the policy-specific expected reset period.
- The production-discovered `reset period 0 and actions none` output is accepted only for `Suspended`, never for `Normal`.
- A suspended reset period such as `42` remains a mismatch and blocks service stop.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--proposed-approach"></a>
#### Proposed Approach

Keep the existing two-state `Suspended`/`Normal` boundary. Derive the requested and expected reset period from the policy: `0` for `Suspended`, `3600` for `Normal`. Update the recovery-query test fixture so its default output matches Windows: suspended queries report `0`, normal queries report `3600`. Add a focused RED assertion against the observed suspended output before changing the module, then update command-argument and diagnostic expectations.

Do not accept both `0` and `3600` for suspended state. A single canonical representation keeps mutation, observation, tests, and operator diagnostics aligned.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--files-and-modules"></a>
#### Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: derive policy-specific reset mutation, verification, and error text.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: model Windows normalization and prove suspended/normal separation plus controlled-stop ordering.
- Temporary guarded scripts under `A:\Temp\cbdev-shared-folder-production-20260722-064200`: update only after the fix is merged, using the new exact merge SHA/tree.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--validation-plan"></a>
#### Validation Plan

- Capture RED evidence showing observed suspended output with reset `0` is rejected before the module edit.
- Pass focused controlled-stop Pester tests with explicit failed-count handling.
- Pass the complete Windows production Pester suite.
- Pass PowerShell parser checks and `git diff --check`.
- Pass a clean isolated Gradle build.
- Complete independent task and whole-branch Review Mode passes with no Critical or Important findings.
- Pass GitHub Ubuntu, macOS, Windows, and CodeQL checks.
- Retry the exact-SHA/tree guarded production installer, including both worker install passes, pinned deployment, installed-worker acceptance, startup verification, and separate authenticated browser acceptance.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--rollback-and-recovery"></a>
#### Rollback and Recovery

- Production is already at the verified safe baseline before this change.
- Before merge, production remains unchanged.
- During the next rollout, any failed postcondition runs the reviewed rollback script and must re-prove the safe baseline.
- Never delete shared roots, shared data, prior releases, MongoDB data, or cloudflared configuration.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--risks"></a>
#### Risks

- Treating reset `0` as suspended must not leak into normal recovery; policy-specific tests enforce separation.
- Another Windows version could format `qfailure` differently; the parser remains label-based and still fails closed on missing or ambiguous fields.
- A future recovery-action design could give reset period meaning while suspended; that requires a new explicit policy rather than widening this verifier.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization-md--open-questions"></a>
#### Open Questions

None.

<!-- /migrated-source: docs/specs/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md -->

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md"></a>
## 2026-07-22 | specs | ChristopherBell.dev WinSW 2 Worker Reinstall Specification

Original source: `docs/specs/2026-07-22-christopherbell-dev-winsw2-worker-reinstall.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `fc869b244358364f9f4fc5f1c91acea12588b237bcbdccf57ebfa640194ce26c`.

<!-- migrated-source: docs/specs/2026-07-22-christopherbell-dev-winsw2-worker-reinstall.md -->
<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--christopherbelldev-winsw-2-worker-reinstall-specification"></a>
### ChristopherBell.dev WinSW 2 Worker Reinstall Specification

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--document-status"></a>
#### Document Status

Approved.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--purpose"></a>
#### Purpose

Make the shared-folder media worker installation idempotent with the pinned stable WinSW 2.12.0 runtime so the guarded production rollout can be retried safely.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--background"></a>
#### Background

The first elevated shared-folder runtime installation registered `ChristopherBellMediaWorker`, but the retry failed with `Media worker WinSW service refresh failed.` The worker was left stopped, the website remained healthy, and the prepared rollback removed the worker and feature flag while preserving `A:\Shared` and `A:\Shared-System`.

The repository calls `ChristopherBellMediaWorker.exe refresh` when the worker service already exists. WinSW's official v2 command list includes `install`, `uninstall`, `start`, `stop`, `stopwait`, `restart`, and `status`, but not `refresh`. `refresh` is a WinSW 3 feature. WinSW 3 remains a prerelease with documented breaking changes, so upgrading both production services is outside this recovery task.

Official references:

- WinSW 2 command contract: <https://github.com/winsw/winsw/blob/v2/README.md>
- WinSW project status and stable-versus-prerelease policy: <https://github.com/winsw/winsw>
- WinSW release history and WinSW 3 breaking changes: <https://github.com/winsw/winsw/releases>

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--goals"></a>
#### Goals

- Use only commands supported by WinSW 2.12.0.
- Keep first-time worker installation and repeated installation safe and deterministic.
- Refresh an existing worker registration by stopping, uninstalling, waiting for disappearance, reinstalling, and verifying reappearance.
- Preserve the `LocalService` identity and leave the worker stopped until explicit production acceptance starts it.
- Keep every service-state wait bounded and fail closed with actionable causal errors.
- Complete the full TDD, review, PR, CI, merge, rollback-ready production retry, and Builder closeout loop.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--non-goals"></a>
#### Non-Goals

- Upgrade the website or worker to WinSW 3.
- Change the website service stop/recovery boundary merged in PR 1221.
- Change Java, JavaScript, media processing, permissions, storage roots, or the shared-folder user experience.
- Delete or recreate `A:\Shared` or `A:\Shared-System`.
- Start the worker as part of installation; production acceptance owns the start transition.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--supported-winsw-2-lifecycle"></a>
##### Supported WinSW 2 lifecycle

- A missing worker service uses the supported `install` command.
- An existing worker is stopped before any worker control-file mutation.
- An existing worker uses the supported `uninstall` command, then waits no more than 30 seconds for SCM disappearance.
- Reinstallation begins only after disappearance is proven.
- After `install`, the installer waits no more than 30 seconds for SCM presence.
- Every WinSW nonzero exit, service query failure, or bounded wait timeout fails the operation.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--service-state-and-identity"></a>
##### Service state and identity

- File mutation remains behind the stopped-worker boundary.
- The reinstalled service is configured and verified as `NT AUTHORITY\LocalService`.
- Successful installation returns with the worker stopped.
- The website service is never stopped, restarted, reconfigured, or otherwise mutated by this worker-only lifecycle.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--failure-behavior"></a>
##### Failure behavior

- If stopping fails, no worker files or registration are changed.
- If worker file preparation or ACL application fails, the existing registration remains present and stopped; uninstall has not started.
- If uninstall fails, the installer attempts to leave the existing worker stopped and reports the uninstall cause.
- If uninstall succeeds but disappearance cannot be proven, installation does not continue.
- If reinstall or presence verification fails, the operation reports the original cause and attempts to leave any resulting worker registration stopped.
- The guarded production script sets `APP_SHARED_FOLDER_ENABLED=true` only after `prod install` succeeds, so a failed worker reinstall cannot enable the feature during the retry.
- The existing prepared rollback remains the production recovery path for any later acceptance failure.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--production-acceptance"></a>
##### Production acceptance

- Run the merged installer once with the worker absent and again with it present before enabling the feature; both runs must pass the worker-install phase.
- Require the worker to be present, stopped, Automatic delayed-start, configured with the expected recovery policy, and owned by `LocalService` after install.
- Continue the previously approved exact-SHA/tree deployment and acceptance sequence only after the idempotence proof passes.
- On any failure, run the prepared rollback and prove website HTTP 200, normal website recovery, absent worker and flag, and preserved shared roots.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--proposed-approach"></a>
#### Proposed Approach

Keep `Install-SharedFolderWorkerService` as the single lifecycle owner. Add an injected service-presence wait action so tests can prove exact ordering without touching SCM. For an existing service, the function stops it, prepares and protects all worker files while the stopped registration still exists, runs WinSW 2 `uninstall`, waits for absence, runs WinSW 2 `install`, and waits for presence. For a missing service, it prepares and protects files, installs, and verifies presence. Both paths then set and verify `LocalService`, stop defensively, and return without starting the worker.

The implementation must not parse WinSW error text. Exit codes, bounded SCM state, service identity, and final stopped state are authoritative.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--files-and-modules"></a>
#### Files and Modules

- `ops/production/windows/modules/Production.SharedFolder.psm1`: replace the unsupported refresh branch with the bounded WinSW 2 reinstall lifecycle.
- `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`: add RED/GREEN coverage for first install, existing-service reinstall, timeouts, command failures, exact ordering, identity, and final stopped state.
- Temporary guarded production scripts under `A:\Temp\cbdev-shared-folder-production-20260722-064200`: update only after the fix is merged, using the new exact merge SHA/tree.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--validation-plan"></a>
#### Validation Plan

- Capture a focused RED test showing the existing-service path requests unsupported `refresh` instead of `uninstall` and `install`.
- Pass the focused worker Pester suite with explicit failed-count handling.
- Pass the complete Windows production Pester suite.
- Pass PowerShell parser checks and `git diff --check`.
- Pass a clean isolated Gradle build.
- Complete independent Review Mode review with no Critical or Important findings.
- Pass GitHub Ubuntu, macOS, Windows, and CodeQL checks before merge.
- Perform the guarded elevated production acceptance and rollback on any failure.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--rollback-and-recovery"></a>
#### Rollback and Recovery

- Before merge, revert the task commit and rerun focused verification if the design proves unsound.
- During production, use `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1` after any failed postcondition.
- Never delete the shared roots, prior release, current healthy website release, or their contents.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--risks"></a>
#### Risks

- SCM can retain a deleted service temporarily; bounded absence verification prevents an immediate reinstall race.
- A reinstall failure can leave the worker absent; the operation fails closed before feature enablement, and rollback confirms the safe baseline.
- Reinstalling the wrong service would be destructive; the service name and worker binary remain fixed constants and tests assert exact arguments.
- A future WinSW 3 migration has a different risk profile and must receive its own spec, compatibility tests, and production rollout.

<a id="source-docs-specs-2026-07-22-christopherbell-dev-winsw2-worker-reinstall-md--open-questions"></a>
#### Open Questions

None.

<!-- /migrated-source: docs/specs/2026-07-22-christopherbell-dev-winsw2-worker-reinstall.md -->

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md"></a>
## 2026-07-22 | spoke-reviews | ChristopherBell.dev Shared Folder Merge Review

Original source: `docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-merge-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `c7e89b5a7e122db2e0fadc76048c0f83af4dc26085945e56f126a1171e730752`.

<!-- migrated-source: docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-merge-review.md -->
<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--christopherbelldev-shared-folder-merge-review"></a>
### ChristopherBell.dev Shared Folder Merge Review

- Related work: [Shared Folder Portal](2026-07-17-christopherbell-dev.md#source-docs-work-2026-07-17-christopherbell-dev-shared-folder-portal-md)
- Spoke update: [Shared Folder Merge Update](#source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md)
- Test report: [Alternate-Port Acceptance](../test-reports/2026-07-22-christopherbell-dev-shared-folder-alternate-port-acceptance.md)
- Repo: `azurras/christopherbell.dev`
- Branch: `codex/shared-folder-worker`
- Pull request: [#1219](https://github.com/azurras/christopherbell.dev/pull/1219)
- Reviewed merge: `6ad5a0a316d2674f96fca7b986a1d15d7abdc856`

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--findings"></a>
#### Findings

No Blockers. No Warnings.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--scope-reviewed"></a>
#### Scope Reviewed

Reviewed the Task 7-10 branch diff and the final runtime fixes, with special attention to restricted worker effects, native filesystem handles, upload state/version transitions, cache and maintenance bounds, HTTP range semantics, and production installation/test opt-ins.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--validation-checked"></a>
#### Validation Checked

Verified the 41-check isolated runtime result, 1,053-test Java result, 165-test JavaScript result, all three Pester lanes, final independent review, clean diff check, and successful Windows/macOS/Linux and CodeQL GitHub checks.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--house-style-compliance"></a>
#### House-Style Compliance

The implementation keeps trust and effect boundaries explicit, models upload and media transitions as bounded state changes, fails closed on stale identities and lease loss, avoids whole-file buffering, contains resource ownership, and provides focused regressions for each runtime failure found. Tests exercise contracts and failure paths rather than internal call choreography.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--residual-risks"></a>
#### Residual Risks

Production installation and the opt-in installed-worker security group remain operational proof, not a code-review gap. Host locking is intentionally scoped to the current single-Windows-host deployment.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-merge-review-md--merge-readiness"></a>
#### Merge Readiness

Approved and merged. Production rollout may proceed from the squash merge after the native Windows installer confirms the exact merged revision and elevated prerequisites.

<!-- /migrated-source: docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-merge-review.md -->

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md"></a>
## 2026-07-22 | spoke-reviews | ChristopherBell.dev Shared Folder Production Fix Merge Review

Original source: `docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `5170e269ec7b314639fa0754ae0c77efdbc44de3b8b915871f2827e31a11a4ca`.

<!-- migrated-source: docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review.md -->
<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--christopherbelldev-shared-folder-production-fix-merge-review"></a>
### ChristopherBell.dev Shared Folder Production Fix Merge Review

- Related work: [Shared Folder Portal](2026-07-17-christopherbell-dev.md#source-docs-work-2026-07-17-christopherbell-dev-shared-folder-portal-md)
- Spoke update: [Production Fix Merge Update](#source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md)
- Repo: `azurras/christopherbell.dev`
- Branch: `codex/shared-folder-production-fix`
- Pull request: [#1220](https://github.com/azurras/christopherbell.dev/pull/1220)
- Reviewed merge: `4429d11cb3d879315f8c5489909b28b8c70bc37c`

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--findings"></a>
#### Findings

No Blockers. No Warnings.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--scope-reviewed"></a>
#### Scope Reviewed

Reviewed the protected production flag path, website process default, worker installation and refresh sequence, service identity enforcement, early-stop boundary, file and ACL mutation boundary, and fail-closed behavior after setup errors.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--validation-checked"></a>
#### Validation Checked

Verified the focused 87-test production Pester result, aggregate shared-folder Gradle gate, exact stop-before-mutation regression, independent 0 Critical/0 Important/0 Minor review, and successful macOS, Ubuntu, Windows, and CodeQL checks.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--house-style-compliance"></a>
#### House-Style Compliance

The change keeps defaults explicit, separates required and optional configuration, validates the flag at both parsing and process-launch boundaries, contains service mutation behind an injected effect seam, and proves both operation order and failure state. It follows the updated Jane Street style guidance for explicit invariants and narrow effects.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--residual-risks"></a>
#### Residual Risks

Elevated production installation and installed-worker acceptance remain operational proof. The worker must not start until the merged installer confirms the LocalService identity and the live website must remain on the prior release if any guarded step fails.

<a id="source-docs-spoke-reviews-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review-md--merge-readiness"></a>
#### Merge Readiness

Approved and merged. Production rollout may proceed only from the exact squash merge with the guarded verification script.

<!-- /migrated-source: docs/spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-review.md -->

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md"></a>
## 2026-07-22 | spoke-updates | ChristopherBell.dev Shared Folder Merge Update

Original source: `docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-merge-update.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `a0ab84c92ed2575cc264558f717af555f8251ec3ccf74bb4fe6591aedc8aa523`.

<!-- migrated-source: docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-merge-update.md -->
<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--christopherbelldev-shared-folder-merge-update"></a>
### ChristopherBell.dev Shared Folder Merge Update

- Related work: [Shared Folder Portal](2026-07-17-christopherbell-dev.md#source-docs-work-2026-07-17-christopherbell-dev-shared-folder-portal-md)
- Test report: [Alternate-Port Acceptance](../test-reports/2026-07-22-christopherbell-dev-shared-folder-alternate-port-acceptance.md)
- Source repo: `azurras/christopherbell.dev`
- Reporting agent: Codex `/root`
- Status: merged

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--changes-made"></a>
#### Changes Made

Completed the post-portal Windows media worker, fixed-profile FFmpeg/ffprobe boundary, maintenance and capacity authority, pinned verification tooling, and opt-in installed-worker security acceptance. Alternate-port runtime testing exposed and resolved Spring constructor/proxy wiring, Mongo upload-lease version alignment, and full/partial download header and byte-boundary defects.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--files-touched"></a>
#### Files Touched

The spoke changes cover the shared-folder Java services/controllers/tests, browser portal and worker code, Windows production service/install/operations scripts, pinned media-tool manifest, Gradle verification tasks, and operator documentation.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--commits-and-pull-request"></a>
#### Commits and Pull Request

- Runtime commits: `fbe3769cfd894a75f45fed1b124ecbaf7450ccde`, `f91d404c8056bd6b8b316b41909ee0528964331a`
- Pull request: [azurras/christopherbell.dev#1219](https://github.com/azurras/christopherbell.dev/pull/1219)
- Squash merge: `6ad5a0a316d2674f96fca7b986a1d15d7abdc856`

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--validation"></a>
#### Validation

- Isolated port-8090 runtime acceptance: 41/41 passed.
- Java: 1,053 tests, 0 failures/errors, 3 expected platform skips.
- JavaScript: 165/165 passed.
- Worker Pester: 56/56; operations Pester: 28/28 under PowerShell 7 and Windows PowerShell 5.1.
- Independent final review: 0 Critical, 0 Important, 0 Minor.
- GitHub: Windows, macOS, Linux, all CodeQL language analyses, and aggregate CodeQL passed.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--blockers-and-risks"></a>
#### Blockers and Risks

No code or merge blocker remains. The installed worker, production roots, ACLs, and installed-worker security group require an elevated controlled production step. The strict maintenance authority is intentionally single-host.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-merge-update-md--next-actions"></a>
#### Next Actions

Install/deploy from the merged revision, run installed-worker acceptance and production smoke/portal checks, then close Builder work and save session memory.

<!-- /migrated-source: docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-merge-update.md -->

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md"></a>
## 2026-07-22 | spoke-updates | ChristopherBell.dev Shared Folder Production Fix Merge Update

Original source: `docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `5e299926fca714ab861c20a5e35cb1796f723456b72c858c368cfe1538bc79fa`.

<!-- migrated-source: docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update.md -->
<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md--christopherbelldev-shared-folder-production-fix-merge-update"></a>
### ChristopherBell.dev Shared Folder Production Fix Merge Update

- Related work: [Shared Folder Portal](2026-07-17-christopherbell-dev.md#source-docs-work-2026-07-17-christopherbell-dev-shared-folder-portal-md)
- Earlier test report: [Alternate-Port Acceptance](../test-reports/2026-07-22-christopherbell-dev-shared-folder-alternate-port-acceptance.md)
- Source repo: `azurras/christopherbell.dev`
- Reporting agent: Codex `/root`
- Status: merged

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md--changes-made"></a>
#### Changes Made

The first guarded production attempt rejected `APP_SHARED_FOLDER_ENABLED` before switching the live release. The rollback removed the incomplete worker service and feature flag, preserved `A:\Shared` and `A:\Shared-System`, and confirmed the website remained healthy. The follow-up change admits only an optional Boolean feature flag, explicitly defaults the website process to disabled, stops an existing worker before every file or service mutation, keeps it stopped through identity changes, and verifies `NT AUTHORITY\LocalService` before success.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md--commits-and-pull-request"></a>
#### Commits and Pull Request

- Fix commit: `051cdcb60652c748871d942392db9eebe15e2caf`
- Pull request: [azurras/christopherbell.dev#1220](https://github.com/azurras/christopherbell.dev/pull/1220)
- Squash merge: `4429d11cb3d879315f8c5489909b28b8c70bc37c`

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md--validation"></a>
#### Validation

- Focused production Pester: 87/87 passed.
- Aggregate `clean test :website:sharedFolderVerification`: passed.
- Independent final review: 0 Critical, 0 Important, 0 Minor.
- GitHub: macOS, Ubuntu, Windows, all CodeQL language analyses, and aggregate CodeQL passed. One unrelated timing-sensitive command-center test failed on the first Ubuntu attempt; the complete matrix passed on rerun without a patch change.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md--safe-rollback-evidence"></a>
#### Safe Rollback Evidence

- Live home page: HTTP 200 after rollback.
- Worker service present: false.
- Shared-folder feature flag present: false.
- Visible and private data roots: preserved.

<a id="source-docs-spoke-updates-2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update-md--next-actions"></a>
#### Next Actions

Deploy the exact merge revision, install and start the worker only after LocalService verification, run installed-worker and production HTTP acceptance, then close the Builder work and save session memory.

<!-- /migrated-source: docs/spoke-updates/2026-07-22-christopherbell-dev-shared-folder-production-fix-merge-update.md -->

