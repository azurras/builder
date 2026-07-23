# ChristopherBell.dev Worker Service Directory Traversal Implementation Plan

## Document Status

ready-for-execution

## Objective

Grant the LocalService media worker non-inheriting traversal access to the protected production service directory, prove least privilege and effect ordering test-first, merge through all required gates, and complete rollback-ready production acceptance.

## Goals

- Reproduce the missing service-directory ACL request as behavioral RED evidence.
- Add one dedicated ACL constructor for directory-only LocalService traversal.
- Apply the ACL after any required worker stop and before worker file preparation or WinSW installation.
- Preserve protected website-control-file ACLs and existing worker-file ACLs.
- Pass focused/full production tests, the aggregate shared-folder gate, review, and GitHub CI.
- Deploy the exact merge with PowerShell 7 and complete authenticated shared-folder acceptance.

## Inputs

- Spec: `docs/specs/2026-07-23-christopherbell-dev-worker-service-directory-traversal.md`.
- Active work: `docs/work/2026-07-17-christopherbell-dev-shared-folder-portal.md`.
- Failed rollout result: `A:\Temp\cbdev-shared-folder-production-20260722-064200\result.json` at phase `worker startup`.
- Root-cause log: `A:\Shared-System\shared-folder-media-logs\ChristopherBellMediaWorker.wrapper.log` reports Win32 error 267 for working directory `C:\ProgramData\christopherbell.dev\service`.
- Verified rollback: merge `77ec3095e4f7f657209264d06d0f45bc8c8fed46`, website/MongoDB/cloudflared running, worker and feature flag absent, recovery normal, roots preserved, HTTP home 200.

## Branch

- Create `codex/worker-service-root-traversal` from exact `origin/main` at `77ec3095e4f7f657209264d06d0f45bc8c8fed46` in `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker`.
- Preserve the unrelated local `.superpowers/sdd/progress.md` modification; do not stage, overwrite, or clean it.

## Non-Goals

- No shared-folder API, permission, storage, media, UI, or account changes.
- No WinSW upgrade or service-identity change.
- No LocalService write/modify/delete/ownership/ACL-control rights on the service directory.
- No inheritable LocalService access on service-directory children.
- No direct production ACL mutation outside the reviewed installer.
- No shared-root or shared-data deletion.

## Assumptions

- `C:\ProgramData\christopherbell.dev\service` remains the WinSW working directory.
- WinSW, XML, launcher, and worker module retain explicit LocalService read-and-execute ACLs.
- `prod.cmd` and elevated acceptance use PowerShell 7; Windows PowerShell 5.1 is unsupported.
- The pinned rollback remains callable after each production mutation.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add the service-directory traversal contract test-first

Sequence / dependencies:

- Run after switching the isolated worktree to the exact branch/base above.
- Add Code Edit 1.1 only, run the focused test, and require the expected RED assertion before production code changes.
- Apply Code Edits 1.2 through 1.4 only after RED is recorded.

Implementation notes:

- Required skill: `write-jane-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: `Install-SharedFolderWorkerService` requests a protected service-root ACL that lets LocalService traverse the working directory before WinSW installation.
  - Invariants: LocalService receives read-and-execute only; the rule is non-inheriting; SYSTEM and Administrators retain full control; Administrators own the directory; initial service-stop failure still occurs before ACL/file effects.
  - Boundary/API: Keep ACL construction inside `Production.SharedFolder.psm1` and apply it through the existing `SetAclAction` effect seam; do not alter caller parameters.
  - Effects and failures: `Set-Acl` mutates a protected production directory. A failed ACL application must abort before file copy, uninstall/install, identity, or feature enablement.
  - Tests and evidence: A public install-boundary Pester test must fail because the service-root ACL request is absent, then pass while asserting rights, inheritance, owner, path, and ordering.

#### Code Edit 1.1

- File: `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`
- Lines: before 949
- Action: add

Proposed:

```powershell
    It 'grants LocalService non-inheriting service-directory traversal before WinSW install' {
        $productionRoot = Join-Path $TestDrive 'worker-service-traversal'
        $serviceRoot = Join-Path $productionRoot 'service'
        New-Item -ItemType Directory -Path $serviceRoot -Force | Out-Null
        'winsw' | Set-Content (Join-Path $serviceRoot 'ChristopherBellDev.exe')
        'website xml' | Set-Content (Join-Path $serviceRoot 'ChristopherBellDev.xml')
        'website script' | Set-Content (Join-Path $serviceRoot 'Start-ChristopherBellDev.ps1')
        $requests = [Collections.Generic.List[object]]::new()
        $events = [Collections.Generic.List[string]]::new()
        $state = @{ Existing = $false }

        Install-SharedFolderWorkerService -ProductionRoot $productionRoot `
            -GetServiceAction {
                param($name)
                if ($state.Existing) { [pscustomobject]@{ Name = $name; Status = 'Stopped' } }
            } `
            -InvokeWinSwAction {
                param($binary, $command)
                $events.Add($command)
                if ($command -eq 'install') { $state.Existing = $true }
                0
            } `
            -WaitForServicePresenceAction {
                param($name, $shouldExist, $timeoutSeconds)
                $state.Existing | Should -Be $shouldExist
            } `
            -StopServiceAction { param($name) } `
            -SetServiceIdentityAction { param($name, $identity) } `
            -GetServiceIdentityAction { param($name) 'NT AUTHORITY\LocalService' } `
            -ProtectPathAction { param($path) } `
            -SetAclAction {
                param($path, $acl)
                $requests.Add([pscustomobject]@{ Path = $path; Acl = $acl })
                $events.Add("acl:$([IO.Path]::GetFileName($path))")
            }

        $serviceRootRequests = @($requests | Where-Object Path -eq $serviceRoot)
        $serviceRootRequests.Count | Should -Be 1
        $acl = $serviceRootRequests[0].Acl
        $acl.AreAccessRulesProtected | Should -BeTrue
        $acl.GetOwner([Security.Principal.SecurityIdentifier]).Value |
            Should -Be 'S-1-5-32-544'
        $rules = @($acl.GetAccessRules(
            $true, $false, [Security.Principal.SecurityIdentifier]))
        $worker = $rules | Where-Object IdentityReference -eq 'S-1-5-19'
        ($worker.FileSystemRights -band [Security.AccessControl.FileSystemRights]::ReadAndExecute) |
            Should -Be ([Security.AccessControl.FileSystemRights]::ReadAndExecute)
        ($worker.FileSystemRights -band [Security.AccessControl.FileSystemRights]::Modify) |
            Should -Not -Be ([Security.AccessControl.FileSystemRights]::Modify)
        $worker.InheritanceFlags | Should -Be ([Security.AccessControl.InheritanceFlags]::None)
        $worker.PropagationFlags | Should -Be ([Security.AccessControl.PropagationFlags]::None)
        $events.IndexOf('acl:service') | Should -BeLessThan $events.IndexOf('install')
    }
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1" -FullNameFilter "*grants LocalService non-inheriting service-directory traversal before WinSW install*" -PassThru -Output Detailed; if ($r.FailedCount -ne 1) { exit 1 }'` before production edits.
- Require the failure at `serviceRootRequests.Count` with expected `1` and actual `0`.

#### Code Edit 1.2

- File: `ops/production/windows/modules/Production.SharedFolder.psm1`
- Lines: after 116
- Action: add

Proposed:

```powershell
function New-SharedFolderWorkerServiceDirectoryAcl {
    [CmdletBinding()]
    param()

    $acl = [Security.AccessControl.DirectorySecurity]::new()
    $acl.SetAccessRuleProtection($true, $false)
    $administrators = [Security.Principal.SecurityIdentifier]::new($script:AdministratorsSid)
    $system = [Security.Principal.SecurityIdentifier]::new($script:SystemSid)
    $worker = [Security.Principal.SecurityIdentifier]::new($script:LocalServiceSid)
    $acl.SetOwner($administrators)
    $inheritance = [Security.AccessControl.InheritanceFlags]::None
    $propagation = [Security.AccessControl.PropagationFlags]::None
    $allow = [Security.AccessControl.AccessControlType]::Allow
    foreach ($identity in @($system, $administrators)) {
        $rule = [Security.AccessControl.FileSystemAccessRule]::new(
            $identity,
            [Security.AccessControl.FileSystemRights]::FullControl,
            $inheritance,
            $propagation,
            $allow)
        [void]$acl.AddAccessRule($rule)
    }
    $workerRule = [Security.AccessControl.FileSystemAccessRule]::new(
        $worker,
        [Security.AccessControl.FileSystemRights]::ReadAndExecute,
        $inheritance,
        $propagation,
        $allow)
    [void]$acl.AddAccessRule($workerRule)
    return $acl
}
```

Verification:

- Parse `Production.SharedFolder.psm1` with `Management.Automation.Language.Parser` and require zero errors.
- Re-run the focused test from Code Edit 1.1 and require one pass.

#### Code Edit 1.3

- File: `ops/production/windows/modules/Production.SharedFolder.psm1`
- Lines: 378-381
- Action: replace

Current:

```powershell
    try {
        if ($serviceExists) { & $StopServiceAction $serviceName $GetServiceAction }

        if (-not (Test-Path -LiteralPath $websiteBinary -PathType Leaf)) {
```

Proposed:

```powershell
    try {
        if ($serviceExists) { & $StopServiceAction $serviceName $GetServiceAction }
        & $SetAclAction $serviceRoot (New-SharedFolderWorkerServiceDirectoryAcl)

        if (-not (Test-Path -LiteralPath $websiteBinary -PathType Leaf)) {
```

Verification:

- The focused test must prove the exact service-root request precedes `install`.
- Existing initial-query and initial-stop-query tests must still prove zero ACL/file/WinSW effects on those failures.

#### Code Edit 1.4

- File: `ops/production/windows/modules/Production.SharedFolder.psm1`
- Lines: 463
- Action: replace

Current:

```powershell
Export-ModuleMember -Function Get-SharedFolderRuntimePaths,New-SharedFolderRuntimeDirectories,New-SharedFolderAcl,New-SharedFolderWorkerFileAcl,Set-SharedFolderRuntimeAcls,Read-PinnedMediaToolManifest,Expand-ValidatedMediaArchive,Install-PinnedMediaTools,Install-SharedFolderWorkerService,Install-SharedFolderRuntime
```

Proposed:

```powershell
Export-ModuleMember -Function Get-SharedFolderRuntimePaths,New-SharedFolderRuntimeDirectories,New-SharedFolderAcl,New-SharedFolderWorkerFileAcl,New-SharedFolderWorkerServiceDirectoryAcl,Set-SharedFolderRuntimeAcls,Read-PinnedMediaToolManifest,Expand-ValidatedMediaArchive,Install-PinnedMediaTools,Install-SharedFolderWorkerService,Install-SharedFolderRuntime
```

Verification:

- Import the module under PowerShell 7 and require `Get-Command New-SharedFolderWorkerServiceDirectoryAcl` to resolve.

- [ ] Step 1: Switch to `codex/worker-service-root-traversal` from exact `origin/main`.
- [ ] Step 2: Apply Code Edit 1.1 only and record the expected RED failure.
- [ ] Step 3: Apply Code Edits 1.2-1.4 and require the focused test to pass.
- [ ] Step 4: Run the complete worker Pester file and full production Pester suite.
- [ ] Step 5: Run parser, diff, and aggregate shared-folder validation.

### Task 2 - Review, publish, and merge the correction

Sequence / dependencies:

- Run only after Task 1 tests and aggregate validation pass.

Implementation notes:

- Required skill: `write-jane-street-style-code` in Review Mode before merge; no code edits during review.
- Review ACL inheritance, owner, effective rights, failure ordering, service identity, and the complete branch diff.
- Stage only the module and test file; leave `.superpowers/sdd/progress.md` untouched.

- [ ] Step 1: Run whole-branch Review Mode and resolve every blocker test-first.
- [ ] Step 2: Commit and push `codex/worker-service-root-traversal`.
- [ ] Step 3: Open a ready PR with production error 267, root cause, RED/GREEN evidence, and rollback state.
- [ ] Step 4: Require all GitHub CI and CodeQL gates to pass.
- [ ] Step 5: Squash-merge and record the exact merge SHA/tree.

### Task 3 - Retry exact-release production acceptance

Sequence / dependencies:

- Run only after Task 2 merges.
- Re-prove the safe baseline before mutation.
- Refresh only the immutable identifiers in both prepared scripts.
- Launch both installer and rollback with PowerShell 7, never Windows PowerShell 5.1.

Implementation notes:

- Required skill: `write-jane-street-style-code` in Implementation Mode for identifier refresh and Review Mode for preflight.
- Before-Edit Brief:
  - Behavior: Install/reinstall and start the LocalService worker, deploy the pinned release, and complete infrastructure/browser acceptance.
  - Invariants: The feature flag follows both install passes; source SHA/tree cannot drift; rollback remains independently pinned; shared roots remain preserved.
  - Boundary/API: Modify only the identifier lines in the two reviewed temporary scripts.
  - Effects and failures: Elevated execution changes ACLs, worker registration, feature configuration, release/process state, and worker state. Any failure invokes rollback.
  - Tests and evidence: Parser/exact-tree preflight, two install passes, service/security/startup checks, HTTP authorization, authenticated listing/download/playback, and rollback evidence if needed.

#### Code Edit 3.1

- File: `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`
- Lines: 9-10
- Action: replace

Current:

```powershell
$expectedSha = '77ec3095e4f7f657209264d06d0f45bc8c8fed46'
$expectedTree = '8b7091eb65b9f8026c220f0c5c8212e0cc9a2fc3'
```

Proposed:

```powershell
$expectedSha = '<NEW_IMMUTABLE_SQUASH_MERGE_SHA>'
$expectedTree = '<NEW_IMMUTABLE_SQUASH_MERGE_TREE>'
```

Verification:

- Parse with zero errors and require source `HEAD^{tree}`, fetched `origin/main^{tree}`, and the expected tree to match.

#### Code Edit 3.2

- File: `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`
- Lines: 10-11
- Action: replace

Current:

```powershell
$expectedSha = '77ec3095e4f7f657209264d06d0f45bc8c8fed46'
$expectedTree = '8b7091eb65b9f8026c220f0c5c8212e0cc9a2fc3'
```

Proposed:

```powershell
$expectedSha = '<NEW_IMMUTABLE_SQUASH_MERGE_SHA>'
$expectedTree = '<NEW_IMMUTABLE_SQUASH_MERGE_TREE>'
```

Verification:

- Parse with zero errors and confirm the rollback contains no mutable `origin/main` dependency.

- [ ] Step 1: Re-prove website/dependency/recovery/listener/root health with worker and flag absent.
- [ ] Step 2: Refresh identifiers and complete read-only preflight.
- [ ] Step 3: Warn immediately before UAC and launch the guarded installer through PowerShell 7.
- [ ] Step 4: Require result status `infrastructure-passed-browser-pending`.
- [ ] Step 5: Verify authenticated `/shared`, permitted listing, exact download bytes, and applicable progressive playback in the logged-in browser.
- [ ] Step 6: Run the pinned PowerShell 7 rollback and prove the safe baseline after any failure.

### Task 4 - Close durable Builder work

Sequence / dependencies:

- Run only after successful production/browser acceptance or a verified rollback with an explicit blocker.

- [ ] Step 1: Save and validate a local app test report with exact requests, responses, service facts, ACL evidence, and production outcome.
- [ ] Step 2: Save spoke update and review artifacts.
- [ ] Step 3: Close the active shared-folder work only if the original feature is genuinely accepted live.
- [ ] Step 4: Save session memory, refresh indexes, validate hub state, and commit/push every Builder checkpoint.

## Code Changes

- `Production.SharedFolderWorker.Tests.ps1`: add the RED/GREEN public-boundary service-root ACL and ordering regression.
- `Production.SharedFolder.psm1`: add the non-inheriting directory ACL constructor, apply it before worker preparation/registration, and export it.
- Temporary production scripts: post-merge immutable SHA/tree refresh only.

## Files and Modules

- `ops/production/windows/modules/Production.SharedFolder.psm1`
- `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`

## Unit Testing

- RED: focused service-root ACL request count is 0 before production changes.
- GREEN: exact request count is 1; protected ACL, Administrators owner, LocalService read-and-execute, no modify, no inheritance, and pre-install ordering all pass.
- Existing initial service-query and stop-query failures still produce zero file/ACL/WinSW effects.
- Existing worker install/reinstall, identity, file ACL, cleanup, timeout, and aggregate-cause tests remain green.

## Local Testing

- `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`
- `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`
- PowerShell parser validation for the module, test, installer, and rollback scripts.
- `git diff --check` and exact two-file spoke diff before commit.
- `gradlew.bat sharedFolderCheck --no-daemon` with isolated `GRADLE_USER_HOME`; require `BUILD SUCCESSFUL`.
- Guarded production install through `C:\Program Files\PowerShell\7\pwsh.exe`, installed-worker security Pester, startup verification, HTTP checks, and authenticated browser acceptance.

## Validation

- Production error 267 is explained by the missing parent-directory traversal rule.
- RED/GREEN evidence proves the exact public install behavior.
- Local/full tests, aggregate build, review, and all required GitHub checks pass.
- Production worker starts as LocalService, exact merged release is active, recovery is normal, and site health remains good.
- Anonymous API remains denied; permitted authenticated listing/download and applicable playback pass.

## Rollback or Recovery

- Keep the current safe baseline until post-merge acceptance.
- Use the prepared rollback pinned to the same SHA/tree after any failed gate.
- Rollback removes the feature flag, reloads the website without it, removes or disables the worker, and proves website/dependency/recovery/listener/root health.
- Never delete shared contents, shared roots, production releases, MongoDB data, or cloudflared configuration.

## Risks

- An inheritable LocalService rule could expose website control files; explicit `None` inheritance/propagation assertions prevent it.
- Applying ACLs before an initial stop failure would violate no-effect semantics; existing failure-order tests and placement after stop prevent it.
- WinSW could reveal another startup-stage failure after traversal is fixed; preserved logs, guarded result phases, and rollback contain that risk.
- Production could drift between merge and UAC; exact SHA/tree checks before and inside the deployment lock prevent it.
- Authenticated playback depends on a suitable shared file; record honestly if only listing/download can be exercised.

## Completion Criteria

- The plan validator and execution-readiness review report no blockers.
- RED is observed before production code edits; focused/full/aggregate tests pass after.
- The two-file spoke change is committed, pushed, reviewed, CI-green, and squash-merged.
- Production result reaches `infrastructure-passed-browser-pending` without rollback.
- Authenticated shared-folder listing/download and applicable playback pass.
- Test report, spoke update/review, closure, session memory, indexes, and Builder state are committed and pushed.
