# ChristopherBell.dev Worker Service Directory Traversal

## Document Status

Ready for execution.

## Purpose

Allow the shared-folder media worker to start as `NT AUTHORITY\LocalService` without weakening the protected production service directory or granting the worker access to website control files.

## Background

The guarded production rollout of merge `77ec3095e4f7f657209264d06d0f45bc8c8fed46` completed both worker installation passes, enabled the feature, and deployed the pinned release. `Start-Service ChristopherBellMediaWorker` then failed. The pinned rollback passed and restored the safe baseline: the feature flag and worker are absent, the website, MongoDB, and cloudflared are running, normal website recovery is restored, HTTP `/` returns 200, and `A:\Shared` plus `A:\Shared-System` are preserved.

The retained WinSW wrapper log records the exact failure:

```text
An error occurred trying to start process 'C:\Program Files\PowerShell\7\pwsh.exe'
with working directory 'C:\ProgramData\christopherbell.dev\service'.
The directory name is invalid.
```

The directory exists. Its ACL permits only SYSTEM and Administrators. The worker executable, XML, launcher script, and worker module separately grant LocalService read-and-execute access, but LocalService cannot traverse the parent service directory to use it as WinSW's working directory.

## Goals

- Grant LocalService the minimum directory-only rights required to traverse and use the production service directory as the worker working directory.
- Preserve SYSTEM and Administrators full control and protected inheritance behavior.
- Keep LocalService out of website executable, XML, launcher, and other production control files.
- Apply the traversal ACL before worker registration and identity verification.
- Prove the exact ACL shape and effect ordering with RED/GREEN Pester coverage.
- Merge through required CI and rerun rollback-ready production acceptance.

## Non-Goals

- Do not grant LocalService modify, write, delete, ownership, or ACL-control rights on the service directory.
- Do not make the LocalService service-directory rule inheritable to children.
- Do not change shared-folder account permissions, storage roots, media behavior, website APIs, WinSW versions, or the worker service identity.
- Do not delete or alter files in `A:\Shared` or `A:\Shared-System`.
- Do not bypass the guarded installer, immutable release checks, or rollback.

## Requirements

1. A dedicated service-directory ACL constructor must protect inheritance, retain Administrators ownership, grant SYSTEM and Administrators full control, and grant LocalService `ReadAndExecute` on the directory itself only.
2. The LocalService rule must use no container/object inheritance flags so website control files do not inherit worker access.
3. `Install-SharedFolderWorkerService` must apply that ACL to `C:\ProgramData\christopherbell.dev\service` before invoking WinSW installation.
4. Existing per-file worker ACLs and protected website-control-file ACLs must remain unchanged.
5. A focused regression must fail before implementation because the install effect seam receives no service-directory ACL request.
6. Tests must assert the directory ACL rights, non-inheritance, owner, protected state, exact path, and ordering before WinSW installation.
7. The production retry must use PowerShell 7, the new immutable merge SHA/tree, two install passes, installed-worker security acceptance, startup verification, HTTP authorization checks, and authenticated browser acceptance.
8. Any failed production gate must run the pinned rollback and prove the safe baseline.

## Proposed Approach

Add `New-SharedFolderWorkerServiceDirectoryAcl` beside the existing shared-folder ACL constructors. Use a protected `DirectorySecurity` object with Administrators ownership; SYSTEM and Administrators receive full control, while LocalService receives non-inheriting `ReadAndExecute`. Apply it through the existing `SetAclAction` seam to the service root immediately before worker file preparation and WinSW registration.

This keeps traversal explicit at the directory boundary. It does not broaden the per-file access model and avoids changing the global protected-production ACL used by unrelated service files.

## Files and Modules

- `ops/production/windows/modules/Production.SharedFolder.psm1`: service-directory ACL constructor, install application, and export.
- `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`: ACL contract and install-order regression.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`: post-merge immutable identifier refresh only.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`: matching immutable rollback identifier refresh only.

## Validation Plan

- Capture RED Pester evidence proving no service-root traversal ACL is currently applied.
- Run focused worker tests after the change and require zero failures.
- Run all production Pester tests and the shared-folder aggregate Gradle gate.
- Validate PowerShell parsing and `git diff --check`.
- Review the whole branch for ACL inheritance, least privilege, effect ordering, and unrelated changes.
- Open a ready PR, require all GitHub checks, and squash-merge.
- Re-prove the safe production baseline, refresh both temporary scripts to the merge SHA/tree, and run the guarded installer with PowerShell 7.
- Require `infrastructure-passed-browser-pending`, then verify authenticated `/shared`, permitted listing, exact download bytes, and applicable progressive playback.
- Run and verify rollback immediately after any failed postcondition.

## Acceptance Criteria

- LocalService can traverse the service directory and WinSW starts the worker.
- The worker runs as `NT AUTHORITY\LocalService` with its existing runtime/file ACL contracts.
- Website control files do not inherit LocalService access.
- The feature is enabled only after both install passes succeed.
- Production uses the exact merged release, website recovery is normal, and public site health remains good.
- Authenticated shared-folder browsing/download and applicable playback pass.
- Builder test, review, closure, and session-memory artifacts are committed and pushed.

## Rollback

Use `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1` pinned to the same merge. Rollback removes the feature flag, reloads the website if needed, removes or disables the worker, restores normal recovery, and verifies website, dependency, listener, and root health. It must never delete shared data or production releases.

## Open Questions

None.
