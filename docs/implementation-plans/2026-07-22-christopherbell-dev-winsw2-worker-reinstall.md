# ChristopherBell.dev WinSW 2 Worker Reinstall Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to execute this plan task by task. Every production-code edit and review must use `write-jane-street-style-code` in the appropriate mode.

**Goal:** Replace the unsupported WinSW 2 `refresh` command with a bounded stop, prepare, uninstall, wait, install, wait lifecycle and safely resume the shared-folder production rollout.

**Architecture:** Keep WinSW pinned at stable 2.12.0. `Install-SharedFolderWorkerService` remains the single lifecycle owner and receives an injectable bounded service-presence wait boundary. Existing registrations stay present and stopped while files and ACLs are prepared, then are uninstalled and reinstalled only through supported WinSW 2 commands. Tests drive exact ordering and fail-closed behavior without touching the real Service Control Manager.

**Tech Stack:** PowerShell 7, Pester 5, WinSW 2.12.0, Windows Service Control Manager, Java 25, Spring Boot, Gradle, GitHub Actions, CodeQL.

## Document Status

`ready-for-execution`

## Objective

Deliver the narrow worker-service lifecycle correction, prove both first installation and repeat installation, merge it through the normal CI gates, then retry the guarded production deployment with exact-release verification and the prepared rollback available throughout.

## Goals

- Remove the unsupported worker `refresh` command.
- Preserve the existing stopped registration until file copying and ACL protection have succeeded.
- Use only WinSW 2.12.0 `uninstall` and `install` for an existing registration.
- Bound disappearance and reappearance waits at 30 seconds by default.
- Preserve the primary setup failure if cleanup also fails.
- Set and verify `NT AUTHORITY\LocalService` and return with the worker stopped.
- Prove the missing-worker and existing-worker paths in production before enabling the shared-folder flag.
- Complete local verification, independent review, PR, CI, merge, production acceptance, rollback readiness, and Builder closeout.

## Inputs

- Approved spec: `docs/specs/2026-07-22-christopherbell-dev-winsw2-worker-reinstall.md`.
- Merged prerequisite: PR 1221 at `aba37983c158bddd0c9d9ae7d58bb2894a2537ec`, tree `4e45b2be6947de7c92c31f82bb7b3c808df5a72e`.
- Production diagnosis: the retry failed at `ChristopherBellMediaWorker.exe refresh`; rollback restored a healthy website, removed the worker registration and feature flag, and preserved both shared roots.
- Official WinSW v2 contract: `refresh` is absent; `install` and `uninstall` are supported.
- User decision: remain on stable WinSW 2 and use the bounded worker-only reinstall approach.

## Branch

- Base: exact `origin/main` commit `aba37983c158bddd0c9d9ae7d58bb2894a2537ec` before development begins.
- Branch: `codex/winsw2-worker-reinstall`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker`.
- Do not modify or clean the user's dirty primary checkout at `A:\Projects\christopherbell.dev`.

## Non-Goals

- No WinSW 3 upgrade or website-service binary change.
- No website service stop, restart, recovery-policy change, or configuration mutation in the worker lifecycle.
- No Java, JavaScript, media-processing, storage, permission-model, or shared-folder UI changes.
- No deletion or recreation of `A:\Shared` or `A:\Shared-System`.
- No worker start inside `Install-SharedFolderWorkerService`; production acceptance owns that transition.
- No broad production cleanup or unrelated service work.

## Assumptions

- The pinned website WinSW binary remains the verified source copied to the worker binary.
- WinSW returns zero only when its requested command succeeds.
- Service registration can remain transiently visible after `uninstall`, so an explicit bounded absence check is required.
- A newly installed worker is normally stopped, but the function will stop it defensively before identity configuration and return.
- The prepared production rollback scripts remain available under `A:\Temp\cbdev-shared-folder-production-20260722-064200`.
- Elevation will be available for production acceptance; inability to elevate stops the rollout without bypassing controls.

## Open Questions

None.

## Files and Modules

- `ops/production/windows/modules/Production.SharedFolder.psm1`: owns the worker lifecycle, bounded SCM wait, identity verification, and cleanup error preservation.
- `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`: owns injected-effect lifecycle, ordering, timeout, command-failure, identity, and cleanup regression tests.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`: guarded post-merge exact-release production installer; update only after merge.
- Builder artifacts under `docs/test-reports`, `docs/spoke-updates`, `docs/spoke-reviews`, `docs/work-closures`, and `docs/session-memory`: own durable verification and closure evidence.

## Task Breakdown

### Task 1 - Drive the supported worker lifecycle test-first

Required skill: `write-jane-street-style-code` in Implementation Mode.

Sequence and dependencies:

- Start from a clean branch created from the exact base commit.
- Add only the successful-lifecycle expectation first and capture the RED result showing `refresh` instead of `uninstall`, wait, and `install`.
- Implement the smallest lifecycle boundary needed to turn that test green.
- Add failure-path tests before each corresponding implementation refinement.
- Commit and push this task only after focused and full local verification pass.

Before-Edit Brief:

- **Behavior:** A missing worker prepares files, installs, waits for presence, stops, and verifies `LocalService`. An existing worker stops before file mutation, prepares files while still registered, uninstalls, waits for absence, installs, waits for presence, stops, and verifies `LocalService`.
- **Invariants:** The website service is untouched; file failure cannot remove an existing registration; no install follows an unproven disappearance; successful return means the worker is registered, stopped, and owned by `LocalService`; every wait is bounded.
- **Boundary/API:** Retain `Install-SharedFolderWorkerService`; add a validated wait timeout and injectable wait action for deterministic tests. Keep the fixed worker service name and binary path private to the function.
- **Effects and failures:** File and ACL mutations precede uninstall. Nonzero WinSW exits, wait errors/timeouts, identity mismatch, and stop errors propagate. Cleanup attempts to stop the worker without replacing the original failure; two failures are reported as an aggregate with the setup failure first.
- **Tests and evidence:** Pester mocks all SCM and WinSW effects. Capture one behavioral RED failure, then prove exact commands, event order, timeout arguments, fail-closed branch behavior, cleanup aggregation, identity, and final stopped state.

#### Code Edit 1.1

- File: `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`
- Lines: 949-1009
- Action: replace

Current:

```powershell
    It 'installs and refreshes the worker service idempotently through controlled service effects' {
        # ... injected service state and effects ...
        $commands | Should -Be @('install','refresh')
        $events | Should -Be @(
            'install','stop','set-identity','get-identity',
            'stop','refresh','stop','set-identity','get-identity')
    }
```

Proposed:

```powershell
    It 'installs and reinstalls the worker through supported WinSW 2 commands' {
        $productionRoot = Join-Path $TestDrive 'service-runtime'
        $serviceRoot = Join-Path $productionRoot 'service'
        New-Item -ItemType Directory -Path $serviceRoot -Force | Out-Null
        'winsw' | Set-Content (Join-Path $serviceRoot 'ChristopherBellDev.exe')
        'website xml' | Set-Content (Join-Path $serviceRoot 'ChristopherBellDev.xml')
        'website script' | Set-Content (Join-Path $serviceRoot 'Start-ChristopherBellDev.ps1')
        $commands = [Collections.Generic.List[string]]::new()
        $waits = [Collections.Generic.List[string]]::new()
        $events = [Collections.Generic.List[string]]::new()
        $identities = [Collections.Generic.List[string]]::new()
        $state = @{ Existing = $false; Status = 'Missing' }
        $getService = {
            param($name)
            if ($state.Existing) { [pscustomobject]@{ Name = $name } }
        }
        $invoke = {
            param($binary, $command)
            $commands.Add($command)
            $events.Add($command)
            if ($command -eq 'install') {
                $state.Existing = $true
                $state.Status = 'Stopped'
            } elseif ($command -eq 'uninstall') {
                $state.Existing = $false
                $state.Status = 'Missing'
            }
            0
        }
        $wait = {
            param($name, $shouldExist, $timeoutSeconds)
            $label = if ($shouldExist) { 'wait-present' } else { 'wait-absent' }
            $events.Add($label)
            $waits.Add("${name}=${shouldExist}:$timeoutSeconds")
            $state.Existing | Should -Be $shouldExist
        }
        $stopService = {
            param($name)
            $events.Add('stop')
            if ($state.Existing) { $state.Status = 'Stopped' }
        }
        $setIdentity = {
            param($name, $identity)
            $events.Add('set-identity')
            $identities.Add("$name=$identity")
        }
        $getIdentity = {
            param($name)
            $events.Add('get-identity')
            'NT AUTHORITY\LocalService'
        }

        $arguments = @{
            ProductionRoot = $productionRoot
            GetServiceAction = $getService
            InvokeWinSwAction = $invoke
            WaitForServicePresenceAction = $wait
            StopServiceAction = $stopService
            SetServiceIdentityAction = $setIdentity
            GetServiceIdentityAction = $getIdentity
            ProtectPathAction = { param($path) }
            SetAclAction = { param($path, $acl) }
        }
        Install-SharedFolderWorkerService @arguments
        $state.Status = 'Running'
        Install-SharedFolderWorkerService @arguments

        $commands | Should -Be @('install','uninstall','install')
        $waits | Should -Be @(
            'ChristopherBellMediaWorker=True:30',
            'ChristopherBellMediaWorker=False:30',
            'ChristopherBellMediaWorker=True:30')
        $events | Should -Be @(
            'install','wait-present','stop','set-identity','get-identity',
            'stop','uninstall','wait-absent','install','wait-present','stop',
            'set-identity','get-identity')
        $identities | Should -Be @(
            'ChristopherBellMediaWorker=NT AUTHORITY\LocalService',
            'ChristopherBellMediaWorker=NT AUTHORITY\LocalService')
        $state.Existing | Should -BeTrue
        $state.Status | Should -Be 'Stopped'
    }
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1" -PassThru -Output Detailed; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Before Code Edit 1.2, expect a behavioral RED failure because the existing implementation emits `refresh` and has no bounded waits.
- Record the exact failed assertion in the task evidence.

#### Code Edit 1.2

- File: `ops/production/windows/modules/Production.SharedFolder.psm1`
- Lines: 310-415
- Action: replace

Current:

```powershell
        if (-not $serviceExists) {
            $exitCode = & $InvokeWinSwAction $workerBinary 'install'
            if ($exitCode -ne 0) { throw 'Media worker WinSW service installation failed.' }
            & $StopServiceAction $serviceName
        } else {
            $exitCode = & $InvokeWinSwAction $workerBinary 'refresh'
            if ($exitCode -ne 0) { throw 'Media worker WinSW service refresh failed.' }
            & $StopServiceAction $serviceName
        }
```

Proposed:

```powershell
        if ($serviceExists) {
            $exitCode = & $InvokeWinSwAction $workerBinary 'uninstall'
            if ($exitCode -ne 0) {
                throw 'Media worker WinSW service uninstallation failed.'
            }
            & $WaitForServicePresenceAction `
                $serviceName $false $ServiceWaitTimeoutSeconds | Out-Null
        }

        $exitCode = & $InvokeWinSwAction $workerBinary 'install'
        if ($exitCode -ne 0) {
            throw 'Media worker WinSW service installation failed.'
        }
        & $WaitForServicePresenceAction `
            $serviceName $true $ServiceWaitTimeoutSeconds | Out-Null
        & $StopServiceAction $serviceName
```

Add to the parameter boundary:

```powershell
        [ValidateRange(1, 300)][int]$ServiceWaitTimeoutSeconds = 30,
        [scriptblock]$WaitForServicePresenceAction = {
            param($Name, $ShouldExist, $TimeoutSeconds)
            $timer = [Diagnostics.Stopwatch]::StartNew()
            do {
                $service = Get-Service $Name -ErrorAction SilentlyContinue
                if ([bool]$service -eq [bool]$ShouldExist) { return $service }
                Start-Sleep -Milliseconds 250
            } while ($timer.Elapsed -lt [TimeSpan]::FromSeconds($TimeoutSeconds))

            $expected = if ($ShouldExist) { 'appear' } else { 'disappear' }
            throw "Service did not $expected within $TimeoutSeconds seconds: $Name"
        },
```

Replace cleanup masking with ordered causal preservation:

```powershell
        $setupFailure = $_
        try {
            & $StopServiceAction $serviceName
        } catch {
            $failures = [Exception[]]@($setupFailure.Exception, $_.Exception)
            throw [AggregateException]::new(
                'Media worker setup and stopped-state cleanup both failed.', $failures)
        }
        throw $setupFailure
```

Verification:

- Re-run the focused successful-lifecycle test and expect it to pass.
- Confirm `rg -n "refresh" ops/production/windows/modules/Production.SharedFolder.psm1` returns no worker lifecycle command.
- Run `pwsh -NoLogo -NoProfile -Command '$e=$null; [Management.Automation.Language.Parser]::ParseFile((Resolve-Path "ops/production/windows/modules/Production.SharedFolder.psm1"),[ref]$null,[ref]$e) | Out-Null; if ($e.Count -ne 0) { $e; exit 1 }'`.

#### Code Edit 1.3

- File: `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`
- Lines: 1011-1065
- Action: replace

Current:

```powershell
    It 'fails closed when service control manager does not retain LocalService' { ... }

    It 'stops an existing worker before file mutations and leaves it stopped when they fail' {
        # Existing assertion proves stop precedes protection failure.
    }
```

Proposed:

```powershell
    It 'keeps an existing registration when worker file preparation fails' { ... }
    It 'does not install when WinSW uninstall fails' { ... }
    It 'does not install when service disappearance times out' { ... }
    It 'fails when WinSW install fails' { ... }
    It 'fails when service presence times out' { ... }
    It 'forwards the configured bounded timeout to every wait' { ... }
    It 'preserves setup and cleanup failures in causal order' { ... }
    It 'fails closed when service control manager does not retain LocalService' { ... }
```

Each test must assert the relevant command and event sequence, whether registration remains present, whether reinstall was skipped, the timeout value received by the injected wait action, and the final stopped-state cleanup attempt. The aggregate test must assert the original setup exception is `InnerExceptions[0]` and the cleanup exception is `InnerExceptions[1]`.

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1" -PassThru -Output Detailed; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`; administrator-only tests may remain explicitly skipped.
- Run `git diff --check` and inspect that only the module and worker test file changed.

- [ ] Step 1: Create `codex/winsw2-worker-reinstall` from the exact refreshed `origin/main` base in the existing isolated worktree.
- [ ] Step 2: Apply Code Edit 1.1 only and capture the expected RED evidence.
- [ ] Step 3: Apply Code Edit 1.2 and make the successful lifecycle test green.
- [ ] Step 4: Add Code Edit 1.3 tests before each failure-path refinement and make the focused suite green.
- [ ] Step 5: Run the full Windows Pester suite, parser validation, and `git diff --check`.
- [ ] Step 6: Perform task-spec review, resolve findings test-first, then commit and push with message `Use WinSW 2 worker reinstall lifecycle`.

### Task 2 - Validate, review, publish, and merge

Required skill: `write-jane-street-style-code` in Review Mode for every review pass.

Sequence and dependencies:

- Run only after Task 1 is committed and pushed with all focused tests green.
- Use fresh independent whole-branch review after the full local build.
- Merge only when every required GitHub check is successful.

Before-Edit Brief:

- **Behavior:** No new behavior is introduced in this task; it proves the branch implements the approved lifecycle and does not regress the application.
- **Invariants:** Review is read-only until a finding is accepted. Any repair returns to Implementation Mode and begins with a failing test or explicit static evidence.
- **Boundary/API:** Compare only `origin/main...HEAD`; preserve the dirty primary checkout and unrelated production state.
- **Effects and failures:** A local suite, build, review, or CI failure blocks merge. Do not weaken or skip a failing gate.
- **Tests and evidence:** Full Pester, clean isolated Gradle build, diff checks, independent review, and all GitHub Ubuntu/macOS/Windows plus CodeQL checks.

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Run `$env:GRADLE_USER_HOME = Join-Path $env:TEMP 'gradle-codex-winsw2-worker-reinstall'; .\gradlew.bat clean build --no-daemon` and require `BUILD SUCCESSFUL`.
- Run `git status --short --branch`, `git diff --check origin/main...HEAD`, and a whole-branch Review Mode pass.
- Open a ready PR with root cause, risk boundary, RED/GREEN evidence, and exact validation counts.
- Require Ubuntu, macOS, Windows, CodeQL actions, CodeQL Java/Kotlin, and CodeQL JavaScript checks to pass before squash merge.

- [ ] Step 1: Run the full local verification matrix.
- [ ] Step 2: Request independent whole-branch review and resolve all Critical and Important findings.
- [ ] Step 3: Push any review fixes as a separate completed-task commit.
- [ ] Step 4: Open the PR and wait for every required check.
- [ ] Step 5: Squash-merge and record the immutable merge SHA and tree.

### Task 3 - Retry the guarded production installation

Required skill: `write-jane-street-style-code` in Implementation Mode for the temporary guarded installer edit and Review Mode for its preflight inspection.

Sequence and dependencies:

- Run only after Task 2 is merged and the exact merge SHA/tree are known.
- Production must still match the safe rollback baseline before any mutation.
- Warn the user immediately before launching the elevated process so the UAC prompt is expected.
- Keep the prepared rollback callable after every mutation.

Before-Edit Brief:

- **Behavior:** Deploy the exact merged release, run `prod install` once with the worker absent and a second time with it present, and enable the feature only after both passes succeed. Then start and verify the worker and authenticated shared-folder portal.
- **Invariants:** The feature flag is absent until both idempotence passes succeed; the website remains healthy; exact SHA/tree verification is mandatory; shared roots and their contents are preserved; any failed gate triggers rollback.
- **Boundary/API:** Modify only the prepared temporary installer and its immutable release identifiers. Use the repository production commands for installation and verification rather than direct unbounded service mutation.
- **Effects and failures:** This task changes installed files, worker registration, environment configuration, and worker state under elevation. Failure runs the prepared rollback and proves the safe baseline.
- **Tests and evidence:** Preflight baseline, exact-release checks, two install passes, worker service contract, startup verification, local/public HTTP, authenticated portal/media checks, anonymous denial, and post-failure rollback evidence when applicable.

#### Code Edit 3.1

- File: `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`
- Lines: 9-10
- Action: replace

Current:

```powershell
$expectedSha = 'aba37983c158bddd0c9d9ae7d58bb2894a2537ec'
$expectedTree = '4e45b2be6947de7c92c31f82bb7b3c808df5a72e'
```

Proposed:

```powershell
$expectedSha = '<NEW_IMMUTABLE_SQUASH_MERGE_SHA>'
$expectedTree = '<NEW_IMMUTABLE_SQUASH_MERGE_TREE>'
```

Verification:

- Confirm the downloaded archive and extracted tree match the new exact merge SHA/tree.
- Confirm the rollback path remains unchanged and points to the known rollback script.

#### Code Edit 3.2

- File: `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`
- Lines: 77-78
- Action: replace

Current:

```powershell
    & $prodScript install
    Set-SharedFolderEnabled
```

Proposed:

```powershell
    & $prodScript install
    & $prodScript install
    Set-SharedFolderEnabled
```

Verification:

- Review the complete temporary script before elevation and confirm both install calls precede feature enablement.
- Confirm a first-pass failure prevents the second pass and feature enablement.
- Confirm a second-pass failure prevents feature enablement and reaches the guarded failure result.

Production acceptance:

- Before mutation, require `ChristopherBellDev` running, homepage HTTP 200 with expected body, normal recovery settings, no worker registration, no feature flag, and both shared roots present.
- After the first install pass, require the worker registration to be present, stopped, delayed automatic, and `LocalService`.
- After the second install pass, require the same postconditions, proving the existing-worker reinstall path.
- Only then enable `APP_SHARED_FOLDER_ENABLED=true`, start the worker through the approved command, and run `prod.cmd verify-startup`.
- Require `ChristopherBellDev`, `ChristopherBellMediaWorker`, MongoDB, and cloudflared to be healthy as applicable; require the website listener and local/public homepage to return 200.
- Require anonymous shared-folder API access to return 401/403 as designed, an authenticated permitted user to load `/shared`, downloads to return the expected bytes, and supported media to play progressively.
- Require the installed worker self-test to pass and require no unexpected service-recovery drift.
- On any failure, execute `rollback-failed-install.ps1` and prove website HTTP 200, normal website recovery, absent worker and flag, and preserved `A:\Shared` plus `A:\Shared-System`.

- [ ] Step 1: Re-audit the safe production baseline.
- [ ] Step 2: Update and review the temporary installer with the immutable merge identifiers and double-install gate.
- [ ] Step 3: Launch the guarded elevated installer and accept the expected UAC prompt.
- [ ] Step 4: Verify both absent-worker and existing-worker install passes before feature enablement.
- [ ] Step 5: Complete service, startup, HTTP, authorization, download, and progressive-media acceptance.
- [ ] Step 6: Run and verify rollback immediately if any postcondition fails.

### Task 4 - Save durable evidence and close the work

Sequence and dependencies:

- Run only after Task 3 reaches either successful acceptance or a fully verified rollback.
- Record actual results, not intended commands.
- Each Builder artifact is a commit-and-push checkpoint on Builder `main`.

Required artifacts and actions:

- Save a local app test report with exact commands, sent requests, received statuses/bodies, Pester/build counts, service facts, and production result.
- Ingest the spoke update with branch, commits, PR, merge SHA/tree, and production status.
- Save an independent spoke review record.
- Close the active shared-folder hub work only if the original accepted feature is genuinely complete; otherwise update it with the remaining concrete blocker.
- Save session memory covering the WinSW 2 decision, implemented lifecycle, production evidence, and recovery path.
- Refresh Builder indexes, validate hub state, then commit and push each required phase artifact.

- [ ] Step 1: Save and checkpoint the test report.
- [ ] Step 2: Save and checkpoint the spoke update and review.
- [ ] Step 3: Close or accurately update the source work record.
- [ ] Step 4: Save and checkpoint session memory.
- [ ] Step 5: Confirm both Builder and spoke repositories are in the expected final Git state.

## Code Changes

- Replace the worker's existing-service `refresh` branch with supported WinSW 2 `uninstall` and `install` commands separated by bounded SCM absence and presence checks.
- Add a validated timeout and injected wait boundary so unit tests remain deterministic and never touch the real Service Control Manager.
- Preserve setup and cleanup exceptions together when stopped-state cleanup also fails.
- Expand worker lifecycle tests to prove successful ordering, fail-closed branches, bounded waits, identity verification, and final stopped state.
- After merge, update the guarded temporary installer to the immutable merge SHA/tree and require two successful install passes before feature enablement.

## Unit Testing

- Successful first installation uses exactly one `install`, one presence wait, one defensive stop, and one identity set/read pair.
- Successful existing installation stops before file effects, uses exactly `uninstall` then `install`, waits for absence then presence, and returns stopped.
- The default wait timeout forwarded to every wait is exactly 30 seconds; a supplied in-range timeout is forwarded unchanged.
- Worker file preparation failure leaves an existing registration present and never calls `uninstall`.
- Nonzero uninstall exit prevents all subsequent waits and installs.
- Absence wait failure prevents reinstall.
- Nonzero install exit and presence wait failure both fail closed and attempt stopped-state cleanup.
- Identity mismatch fails and leaves the worker stopped.
- Simultaneous setup and cleanup failures preserve both exceptions in causal order.
- No test invokes real WinSW, SCM, ACL, or service-control effects.

## Local Testing

- Focused RED/GREEN Pester run for `Production.SharedFolderWorker.Tests.ps1`, with explicit `FailedCount` enforcement.
- Full `ops/production/windows/tests` Pester run, with explicit passed/failed/skipped counts.
- PowerShell parser validation of both edited files.
- `git diff --check` for whitespace and patch integrity.
- Clean Gradle build with a fresh task-specific `GRADLE_USER_HOME`.
- Independent task review and whole-branch Review Mode review.
- Production-safe non-8080 application verification if any application behavior unexpectedly changes; otherwise the PowerShell-only change is validated through its native suites and later guarded production acceptance.

## Validation

- Behavioral RED evidence demonstrates the pre-fix existing-service path calls unsupported `refresh`.
- All focused and full local suites pass with recorded counts.
- The exact branch diff contains only the intended module and worker tests.
- Independent review reports no unresolved Critical or Important findings.
- All required GitHub checks pass and the PR is squash-merged.
- Production proves both install paths before enabling the flag.
- Authenticated read/download/progressive playback succeeds for a permitted user; anonymous access remains denied.
- Final service, listener, release, recovery, roots, and startup checks pass, or rollback restores and proves the safe baseline.

## Rollback or Recovery

- Before merge, revert the task commit or fix forward test-first; do not alter production.
- If CI rejects the branch, keep production on the current merged release and resolve the gate before merge.
- During production, run `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1` after any failed postcondition.
- Never delete shared roots, current shared data, prior healthy releases, MongoDB data, or cloudflared configuration.
- After rollback, require the website service running, homepage HTTP 200, normal recovery actions, worker absent, feature flag absent, and both shared roots preserved.

## Risks

- SCM deletion can be asynchronous; the 30-second bounded absence gate prevents an immediate reinstall race.
- A successful uninstall followed by a failed install can leave the worker absent; the feature remains disabled and rollback confirms the safe website baseline.
- Cleanup can fail after the primary operation; ordered aggregation prevents loss of the actionable root cause.
- Reinstalling the wrong service would be destructive; the fixed worker name/path and exact injected-argument assertions constrain the target.
- A double production install adds a short worker-only registration cycle, but it is the direct acceptance proof for future idempotent deployments.
- Temporary installer drift could target the wrong release; immutable SHA/tree checks and read-only preflight review block that path.

## Completion Criteria

- The worker lifecycle contains no WinSW `refresh` command.
- Both missing and existing worker paths pass exact-order tests using only supported WinSW 2 commands.
- All failure-path, timeout, identity, and cleanup tests pass.
- Full local verification and independent review pass.
- The PR passes every required check and is squash-merged.
- Guarded production acceptance proves double install, correct worker identity/state, healthy website and dependencies, protected shared access, downloads, and progressive playback.
- Any failed rollout is fully rolled back and verified instead of being reported complete.
- Builder test, update, review, closure, indexes, validation, and session-memory artifacts are committed and pushed.
