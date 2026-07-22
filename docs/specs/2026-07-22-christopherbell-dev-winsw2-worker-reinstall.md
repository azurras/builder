# ChristopherBell.dev WinSW 2 Worker Reinstall Specification

## Document Status

Ready for review.

## Purpose

Make the shared-folder media worker installation idempotent with the pinned stable WinSW 2.12.0 runtime so the guarded production rollout can be retried safely.

## Background

The first elevated shared-folder runtime installation registered `ChristopherBellMediaWorker`, but the retry failed with `Media worker WinSW service refresh failed.` The worker was left stopped, the website remained healthy, and the prepared rollback removed the worker and feature flag while preserving `A:\Shared` and `A:\Shared-System`.

The repository calls `ChristopherBellMediaWorker.exe refresh` when the worker service already exists. WinSW's official v2 command list includes `install`, `uninstall`, `start`, `stop`, `stopwait`, `restart`, and `status`, but not `refresh`. `refresh` is a WinSW 3 feature. WinSW 3 remains a prerelease with documented breaking changes, so upgrading both production services is outside this recovery task.

Official references:

- WinSW 2 command contract: <https://github.com/winsw/winsw/blob/v2/README.md>
- WinSW project status and stable-versus-prerelease policy: <https://github.com/winsw/winsw>
- WinSW release history and WinSW 3 breaking changes: <https://github.com/winsw/winsw/releases>

## Goals

- Use only commands supported by WinSW 2.12.0.
- Keep first-time worker installation and repeated installation safe and deterministic.
- Refresh an existing worker registration by stopping, uninstalling, waiting for disappearance, reinstalling, and verifying reappearance.
- Preserve the `LocalService` identity and leave the worker stopped until explicit production acceptance starts it.
- Keep every service-state wait bounded and fail closed with actionable causal errors.
- Complete the full TDD, review, PR, CI, merge, rollback-ready production retry, and Builder closeout loop.

## Non-Goals

- Upgrade the website or worker to WinSW 3.
- Change the website service stop/recovery boundary merged in PR 1221.
- Change Java, JavaScript, media processing, permissions, storage roots, or the shared-folder user experience.
- Delete or recreate `A:\Shared` or `A:\Shared-System`.
- Start the worker as part of installation; production acceptance owns the start transition.

## Requirements

### Supported WinSW 2 lifecycle

- A missing worker service uses the supported `install` command.
- An existing worker is stopped before any worker control-file mutation.
- An existing worker uses the supported `uninstall` command, then waits no more than 30 seconds for SCM disappearance.
- Reinstallation begins only after disappearance is proven.
- After `install`, the installer waits no more than 30 seconds for SCM presence.
- Every WinSW nonzero exit, service query failure, or bounded wait timeout fails the operation.

### Service state and identity

- File mutation remains behind the stopped-worker boundary.
- The reinstalled service is configured and verified as `NT AUTHORITY\LocalService`.
- Successful installation returns with the worker stopped.
- The website service is never stopped, restarted, reconfigured, or otherwise mutated by this worker-only lifecycle.

### Failure behavior

- If stopping fails, no worker files or registration are changed.
- If worker file preparation or ACL application fails, the existing registration remains present and stopped; uninstall has not started.
- If uninstall fails, the installer attempts to leave the existing worker stopped and reports the uninstall cause.
- If uninstall succeeds but disappearance cannot be proven, installation does not continue.
- If reinstall or presence verification fails, the operation reports the original cause and attempts to leave any resulting worker registration stopped.
- The guarded production script sets `APP_SHARED_FOLDER_ENABLED=true` only after `prod install` succeeds, so a failed worker reinstall cannot enable the feature during the retry.
- The existing prepared rollback remains the production recovery path for any later acceptance failure.

### Production acceptance

- Run the merged installer once with the worker absent and again with it present before enabling the feature; both runs must pass the worker-install phase.
- Require the worker to be present, stopped, Automatic delayed-start, configured with the expected recovery policy, and owned by `LocalService` after install.
- Continue the previously approved exact-SHA/tree deployment and acceptance sequence only after the idempotence proof passes.
- On any failure, run the prepared rollback and prove website HTTP 200, normal website recovery, absent worker and flag, and preserved shared roots.

## Proposed Approach

Keep `Install-SharedFolderWorkerService` as the single lifecycle owner. Add an injected service-presence wait action so tests can prove exact ordering without touching SCM. For an existing service, the function stops it, prepares and protects all worker files while the stopped registration still exists, runs WinSW 2 `uninstall`, waits for absence, runs WinSW 2 `install`, and waits for presence. For a missing service, it prepares and protects files, installs, and verifies presence. Both paths then set and verify `LocalService`, stop defensively, and return without starting the worker.

The implementation must not parse WinSW error text. Exit codes, bounded SCM state, service identity, and final stopped state are authoritative.

## Files and Modules

- `ops/production/windows/modules/Production.SharedFolder.psm1`: replace the unsupported refresh branch with the bounded WinSW 2 reinstall lifecycle.
- `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`: add RED/GREEN coverage for first install, existing-service reinstall, timeouts, command failures, exact ordering, identity, and final stopped state.
- Temporary guarded production scripts under `A:\Temp\cbdev-shared-folder-production-20260722-064200`: update only after the fix is merged, using the new exact merge SHA/tree.

## Validation Plan

- Capture a focused RED test showing the existing-service path requests unsupported `refresh` instead of `uninstall` and `install`.
- Pass the focused worker Pester suite with explicit failed-count handling.
- Pass the complete Windows production Pester suite.
- Pass PowerShell parser checks and `git diff --check`.
- Pass a clean isolated Gradle build.
- Complete independent Review Mode review with no Critical or Important findings.
- Pass GitHub Ubuntu, macOS, Windows, and CodeQL checks before merge.
- Perform the guarded elevated production acceptance and rollback on any failure.

## Rollback and Recovery

- Before merge, revert the task commit and rerun focused verification if the design proves unsound.
- During production, use `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1` after any failed postcondition.
- Never delete the shared roots, prior release, current healthy website release, or their contents.

## Risks

- SCM can retain a deleted service temporarily; bounded absence verification prevents an immediate reinstall race.
- A reinstall failure can leave the worker absent; the operation fails closed before feature enablement, and rollback confirms the safe baseline.
- Reinstalling the wrong service would be destructive; the service name and worker binary remain fixed constants and tests assert exact arguments.
- A future WinSW 3 migration has a different risk profile and must receive its own spec, compatibility tests, and production rollout.

## Open Questions

None.
