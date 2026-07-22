# christopherbell.dev Controlled Windows Service Stop Spec

## Document Status

Ready for review.

## Purpose

Make planned production deployments and deployment rollbacks stop the native Windows website service safely even when WinSW 2.12.0 exits with its known invalid-handle failure after the child process has already stopped.

This work unblocks the shared-folder production rollout without changing shared-folder permissions, storage, previews, transcoding, or user-facing behavior.

## Background

The native Windows production site runs as the `ChristopherBellDev` service. The repository configures Service Control Manager recovery to restart the service after 10 seconds and then 30 seconds, with failures reset after one hour.

During the approved shared-folder production deployment, `Stop-Service ChristopherBellDev -ErrorAction Stop` failed. Windows application events showed WinSW 2.12.0 throwing `System.ComponentModel.Win32Exception (6): The handle is invalid` while enumerating the child process tree during `WrapperService.OnStop()`. The child PowerShell process had exited successfully, but the wrapper crash caused Service Control Manager recovery to restart the website while the deployment was attempting to switch releases.

The deployment was rolled back. The production website is online, the shared-folder worker is absent, the feature remains disabled, and `A:\Shared` plus `A:\Shared-System` remain intact.

## Goals

- Give planned deployment and rollback stops one bounded, explicit service-stop boundary.
- Prevent Service Control Manager recovery from racing an intentional release switch.
- Accept a thrown stop command only when independent postconditions prove the service actually stopped.
- Restore the repository-owned recovery policy before any production restart.
- Preserve the original deployment or rollback failure when cleanup also fails, while reporting cleanup context.
- Keep normal automatic crash recovery enabled outside the short planned-stop window.
- Unblock a safe retry of the shared-folder production installation.

## Non-Goals

- Upgrade WinSW to a 3.x prerelease.
- Replace WinSW or the native Windows service architecture.
- Add a public or remotely callable shutdown endpoint.
- Change the website application's shutdown behavior.
- Change shared-folder application code, permissions, files, or media behavior.
- Suppress arbitrary service-stop failures based only on exception text.
- Disable automatic recovery permanently.

## Requirements

### Planned Stop Boundary

1. A named production helper must own the complete intentional-stop transition for `ChristopherBellDev`.
2. The helper must first install a temporary no-restart recovery policy through the existing checked-process boundary.
3. The helper must request a normal service stop. It must not force-kill the website as the default path.
4. The helper must wait for a bounded stopped state using service state, not an arbitrary sleep.
5. The helper must also prove that the configured production port is no longer accepting connections before a release junction may change.
6. A `Stop-Service` exception may be accepted only when both stopped-state and closed-port postconditions pass within their bounds.
7. If either postcondition fails, the helper must fail closed and preserve the stop exception as causal context when one exists.
8. The helper must restore the repository-owned recovery policy in a `finally` path before returning or throwing.
9. Failure to restore the recovery policy is a deployment-blocking infrastructure failure. The service must not be restarted until recovery restoration succeeds.

### Recovery Policy

The repository remains the source of truth for the website service recovery policy:

- first failure: restart after 10 seconds;
- second failure: restart after 30 seconds;
- reset failure count after one hour.

The temporary policy must contain no automatic restart actions. The normal policy must be reapplied and checked before `Start-Service ChristopherBellDev` is allowed.

### Deployment and Rollback Integration

- `Switch-ProductionRelease` must use the controlled stop before changing the `current` junction.
- Its rollback path must use the same controlled stop before restoring the former junction.
- Any other production operation changed in this task must call the same boundary instead of duplicating recovery-policy sequencing.
- Existing deployment locking, candidate verification, atomic junction switching, endpoint verification, and former-release restoration behavior must remain intact.

### Diagnostics and Security

- Errors must identify the failed phase: suspend recovery, request stop, prove stopped state, prove closed port, restore recovery, start service, or verify endpoints.
- Diagnostic output must not include environment secrets, service credentials, or command lines containing secrets.
- Service name, port, timeouts, and recovery actions must be explicit at the boundary and validated before effects occur.
- Unexpected service states, command failures, and port-probe failures must remain fatal.

## Proposed Approach

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

## Files and Modules Involved

- `ops/production/windows/modules/Production.Deploy.psm1`: controlled stop boundary and release-switch integration.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: focused behavioral regressions for the known wrapper failure and fail-closed paths.
- `ops/production/windows/modules/Production.Operations.psm1`: inspect for any restart path that must share the boundary; change only if required to prevent duplicated unsafe stop behavior.
- Existing aggregate Windows operations tests and production acceptance scripts: regression and live verification evidence.

## Validation Plan

### RED Evidence

Before production code changes, add a focused Pester regression in which `Stop-Service` throws after the service reaches `Stopped`. The existing implementation must fail the deployment instead of accepting the independently proven stop.

Add failure cases proving that the deployment remains blocked when:

- the service does not reach `Stopped`;
- the production port remains open;
- temporary recovery configuration fails;
- normal recovery restoration fails; or
- rollback encounters the same wrapper failure without satisfying postconditions.

### GREEN Evidence

- Run the focused `Production.Deploy.Tests.ps1` suite.
- Run the complete Windows production Pester suite.
- Run repository formatting, static checks, and the aggregate project verification required for production scripts.
- Review the final production and test diff against the Jane Street-style review rubric.
- Obtain an independent spoke review before merge.
- Require all GitHub pull-request checks to pass before merge.

### Production Acceptance

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

## Risks and Mitigations

- **Recovery remains suspended after an unexpected failure:** restoration runs in `finally`, blocks restart on failure, and is verified by tests plus live inspection.
- **A wrapper exception hides a real stop failure:** exception text is never sufficient; stopped-state and closed-port postconditions are mandatory.
- **A port closes before the service fully stops:** both service state and port state must pass.
- **A service reports stopped while a child still owns the port:** the closed-port postcondition catches the leaked process.
- **Rollback repeats the same race:** forward and rollback paths share one controlled boundary.
- **Operational code becomes broader than needed:** keep the change within the existing deployment modules and avoid wrapper upgrades or application shutdown APIs.

## Completion Criteria

- The focused regression is witnessed failing before the production edit and passing afterward.
- All focused and aggregate Windows production tests pass.
- The implementation plan, code diff, and evidence pass Builder validation and independent review.
- The spoke change is committed, pushed, merged, and recorded in Builder.
- Production acceptance passes with normal recovery restored.
- The shared-folder production rollout is enabled without modifying or losing the existing shared folders.

## Open Questions

None. The user approved the controlled-stop approach on 2026-07-22.
