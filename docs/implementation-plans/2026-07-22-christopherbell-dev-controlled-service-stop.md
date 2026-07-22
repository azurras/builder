# christopherbell.dev Controlled Windows Service Stop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to execute this plan task by task with review checkpoints.

**Goal:** Make planned native Windows deployment and rollback stops tolerate the observed WinSW 2.12.0 wrapper failure only after independent stopped-service and closed-port postconditions pass, while restoring automatic recovery before any restart.

**Architecture:** `Production.Deploy.psm1` will own one exported controlled-stop boundary. It temporarily clears Service Control Manager recovery actions, requests a normal stop, proves the service and port are down, and restores the repository-owned recovery policy in `finally`; deployment and manual rollback both call this boundary. Pester tests exercise the observable function boundaries with deterministic service and port doubles before any live production retry.

**Tech Stack:** PowerShell 7, Pester 5, Windows Service Control Manager, `sc.exe`, WinSW 2.12.0, Gradle, GitHub Actions, and the existing native Windows production scripts.

## Document Status

`ready-for-execution`

## Objective

Unblock the shared-folder production rollout by containing the observed WinSW invalid-handle stop failure at the deployment boundary without upgrading the wrapper, adding a shutdown endpoint, permanently disabling recovery, or changing shared-folder application behavior.

## Goals

- Add one bounded controlled-stop function for `ChristopherBellDev`.
- Suspend automatic service recovery only during an intentional stop.
- Accept a thrown `Stop-Service` call only after the service reports `Stopped` and the production port is closed.
- Restore the normal 10-second/30-second recovery actions before any website restart.
- Fail closed if recovery configuration, service state, port state, release switching, restart, or endpoint verification is unsafe.
- Preserve both primary and recovery/rollback failures when more than one failure occurs.
- Reuse the same boundary from forward deployment and manual rollback.
- Commit and push each completed spoke task before proceeding.

## Inputs

- Approved spec: `docs/specs/2026-07-22-christopherbell-dev-controlled-service-stop.md`.
- Active work record: `docs/work/2026-07-17-christopherbell-dev-shared-folder-portal.md`.
- Spoke worktree: `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker`.
- Planning source commit: `4429d11cb3d879315f8c5489909b28b8c70bc37c`.
- Planning source tree: `262654c6c56b86c87628e2f16783017aaac018ce`.
- Observed Windows event: WinSW 2.12.0 threw `System.ComponentModel.Win32Exception (6)` from `Process.GetProcessTimes()` while stopping its child process tree; Service Control Manager then applied configured recovery.
- Microsoft `sc failure` contract: `actions= ""` configures no failure action, while `restart/10000/restart/30000` restores the repository-owned recovery sequence.
- Microsoft `sc qfailure` contract: the command reports reset period and configured failure actions for live acceptance inspection.

## Branch

- Base: exact merged commit `4429d11cb3d879315f8c5489909b28b8c70bc37c`.
- Branch: `codex/windows-service-stop-recovery`.
- Worktree: reuse the clean isolated worktree at `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker`; create the branch from the detached exact base without modifying or cleaning the primary checkout.
- Remote: push the branch to `origin` after each completed code task.

## Non-Goals

- No WinSW 3.x prerelease upgrade or service-wrapper replacement.
- No HTTP, JMX, actuator, or other remotely callable shutdown mechanism.
- No force-kill as the default stop path.
- No permanent change to the website service account, startup type, dependencies, or recovery policy.
- No changes to shared-folder roles, permissions, storage roots, uploads, previews, downloads, transcoding, or user interface.
- No suppression based on exception-message matching.
- No broad refactor of production modules or unrelated stop paths.
- No removal of `A:\Shared` or `A:\Shared-System` during deployment or rollback.

## Assumptions

- The production deployment and rollback commands run elevated and can configure service recovery actions.
- `Invoke-CheckedProcess` remains the repository-owned checked process boundary for `sc.exe`.
- `Get-Service`, `ServiceController.WaitForStatus`, and `Get-NetTCPConnection` are available on the Windows production host.
- The service name remains the fixed repository-owned `ChristopherBellDev` identity.
- The normal recovery policy remains reset after 3,600 seconds with restarts after 10,000 and 30,000 milliseconds.
- The production port comes from validated `deploy.json` and remains within 1-65535.
- The current safe production state remains website online, shared-folder feature disabled, worker absent, and both shared roots preserved until the final retry.

## Open Questions

None.

## Global Constraints

- Invoke `write-jane-street-style-code` before every code edit and follow `superpowers:test-driven-development` for each behavior change.
- Do not edit production code until the focused regression has been run and witnessed failing for the expected missing behavior.
- Treat service state, port state, recovery state, and release junctions as explicit operational invariants.
- Do not branch on WinSW exception text; only independent postconditions may convert a thrown stop request into success.
- Never start `ChristopherBellDev` until normal recovery restoration has succeeded.
- Preserve causal exceptions with `InnerException` or `AggregateException`; do not replace them with generic strings.
- Keep `sc.exe` arguments structured through `Invoke-CheckedProcess`; do not construct a shell command string.
- Keep every wait bounded and avoid arbitrary sleeps as the service-state synchronization mechanism.
- Preserve deployment locking, candidate verification, atomic junction switching, endpoint verification, and former-release restoration.
- Keep the live site on port 8080 untouched until focused and aggregate local verification pass.
- After each numbered code task: inspect the diff, run task verification, apply the Jane Street review rubric, commit, and push before starting the next task.

## Task Breakdown

### Task 1 - Add the controlled stop boundary and use it for deployment switching

Sequence / dependencies:

- Runs first because deployment and rollback both depend on the same stop invariant.
- Complete RED/GREEN locally, review, commit, and push before changing manual rollback.

Implementation notes:

- Required skill: invoke `write-jane-street-style-code` before any code edits.
- Required sub-skill: use `superpowers:test-driven-development` and witness the focused RED test before editing `Production.Deploy.psm1`.
- Before-Edit Brief:
  - Behavior: a planned stop may continue after `Stop-Service` throws only when `ChristopherBellDev` reaches `Stopped`, port 8080 has no listener, and normal recovery has been restored.
  - Invariants: the release junction never changes while the service or port is live; the service never restarts while recovery actions are suspended; invalid ports/timeouts and unexpected service states fail before trusted switching logic proceeds.
  - Boundary/API: export `Stop-ProductionWebsiteService` from `Production.Deploy.psm1` alongside the existing deployment functions; keep `Switch-ProductionRelease($Config, $Release)` compatible.
  - Effects and failures: `sc.exe`, Service Control Manager, service-state waits, TCP listener inspection, junction mutation, service start, and HTTP verification are explicit effects; multiple failures retain all causal exceptions.
  - Tests and evidence: a Pester regression first fails because `Stop-ProductionWebsiteService` does not exist, then covers wrapper-stop acceptance, service timeout, open port, recovery suspension failure, recovery restoration failure, deployment rollback, and combined failures.

#### Code Edit 1.1

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: after 5
- Action: add

Current:

```powershell
    InModuleScope Production.Deploy {
        It 'resolves fetched remote main instead of the checked out branch' {
```

Proposed:

```powershell
    InModuleScope Production.Deploy {
        BeforeAll {
            function New-ServiceStateStub {
                param(
                    [string]$Status = 'Stopped',
                    [switch]$WaitFails
                )
                $service = [pscustomobject]@{
                    Status = $Status
                    WaitFails = [bool]$WaitFails
                }
                $service | Add-Member -MemberType ScriptMethod -Name WaitForStatus -Value {
                    param($ExpectedStatus, $Timeout)
                    $null = $ExpectedStatus
                    $null = $Timeout
                    if ($this.WaitFails) {
                        throw [System.TimeoutException]::new('simulated service wait timeout')
                    }
                    $this.Status = 'Stopped'
                }
                $service | Add-Member -MemberType ScriptMethod -Name Refresh -Value { }
                return $service
            }
        }

        It 'accepts the WinSW stop exception only after stopped service and closed port postconditions pass' {
            Mock Invoke-CheckedProcess { '' }
            Mock Stop-Service { throw 'simulated WinSW invalid handle failure' }
            Mock Get-Service { New-ServiceStateStub }
            Mock Get-NetTCPConnection { $null }

            {
                Stop-ProductionWebsiteService -ProductionPort 8080 -PortTimeoutMilliseconds 1
            } | Should -Not -Throw

            Should -Invoke Invoke-CheckedProcess -Times 1 -Exactly -ParameterFilter {
                $FilePath -eq 'sc.exe' -and $ArgumentList[-1] -eq ''
            }
            Should -Invoke Invoke-CheckedProcess -Times 1 -Exactly -ParameterFilter {
                $FilePath -eq 'sc.exe' -and
                $ArgumentList[-1] -eq 'restart/10000/restart/30000'
            }
        }

        It 'fails closed when the website service does not reach Stopped' {
            Mock Invoke-CheckedProcess { '' }
            Mock Stop-Service { throw 'simulated WinSW invalid handle failure' }
            Mock Get-Service { New-ServiceStateStub -Status Running -WaitFails }

            {
                Stop-ProductionWebsiteService -ProductionPort 8080 -ServiceTimeoutSeconds 1
            } | Should -Throw '*did not reach Stopped*'

            Should -Invoke Invoke-CheckedProcess -Times 1 -Exactly -ParameterFilter {
                $ArgumentList[-1] -eq 'restart/10000/restart/30000'
            }
        }

        It 'fails closed when the production port remains open' {
            Mock Invoke-CheckedProcess { '' }
            Mock Stop-Service { }
            Mock Get-Service { New-ServiceStateStub }
            Mock Get-NetTCPConnection {
                [pscustomobject]@{ LocalPort = 8080; OwningProcess = 42 }
            }
            Mock Start-Sleep { }

            {
                Stop-ProductionWebsiteService -ProductionPort 8080 -PortTimeoutMilliseconds 1
            } | Should -Throw '*port 8080 remained open*'
        }

        It 'fails closed when the production port cannot be inspected' {
            Mock Invoke-CheckedProcess { '' }
            Mock Stop-Service { }
            Mock Get-Service { New-ServiceStateStub }
            Mock Get-NetTCPConnection { throw 'simulated TCP inspection failure' }

            {
                Stop-ProductionWebsiteService -ProductionPort 8080
            } | Should -Throw '*inspect production port 8080*'
        }

        It 'does not request a stop when recovery suspension fails' {
            Mock Invoke-CheckedProcess {
                if ($ArgumentList[-1] -eq '') { throw 'simulated recovery suspension failure' }
            }
            Mock Stop-Service { }

            {
                Stop-ProductionWebsiteService -ProductionPort 8080
            } | Should -Throw '*suspend website service recovery*'

            Should -Invoke Stop-Service -Times 0
        }

        It 'blocks restart when recovery restoration fails' {
            Mock Invoke-CheckedProcess {
                if ($ArgumentList[-1] -eq 'restart/10000/restart/30000') {
                    throw 'simulated recovery restoration failure'
                }
                return ''
            }
            Mock Stop-Service { }
            Mock Get-Service { New-ServiceStateStub }
            Mock Get-NetTCPConnection { $null }

            {
                Stop-ProductionWebsiteService -ProductionPort 8080
            } | Should -Throw '*restore website service recovery*'
        }

        It 'resolves fetched remote main instead of the checked out branch' {
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests\Production.Deploy.Tests.ps1' -Output Detailed"`.
- Expected RED: the first new test fails because `Stop-ProductionWebsiteService` is not recognized.
- Record the failing test name and missing-command error before production code changes.

#### Code Edit 1.2

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: before 98
- Action: add

Current:

```powershell
}

function Switch-ProductionRelease {
```

Proposed:

```powershell
}

function Set-ProductionWebsiteRecoveryPolicy {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet('Suspended','Normal')]
        [string]$Policy
    )

    $actions = if ($Policy -eq 'Normal') {
        'restart/10000/restart/30000'
    } else {
        ''
    }
    $phase = if ($Policy -eq 'Normal') { 'restore' } else { 'suspend' }
    try {
        Invoke-CheckedProcess -FilePath 'sc.exe' -ArgumentList @(
            'failure',
            'ChristopherBellDev',
            'reset=',
            '3600',
            'actions=',
            $actions
        ) | Out-Null
    } catch {
        throw [System.InvalidOperationException]::new(
            "Failed to $phase website service recovery.",
            $_.Exception)
    }
}

function Assert-ProductionWebsiteStopped {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateRange(1,65535)]
        [int]$ProductionPort,
        [ValidateRange(1,300)]
        [int]$ServiceTimeoutSeconds = 30,
        [ValidateRange(1,60000)]
        [int]$PortTimeoutMilliseconds = 10000
    )

    try {
        $service = Get-Service -Name 'ChristopherBellDev' -ErrorAction Stop
        $service.WaitForStatus(
            [System.ServiceProcess.ServiceControllerStatus]::Stopped,
            [timespan]::FromSeconds($ServiceTimeoutSeconds))
        $service.Refresh()
    } catch {
        throw [System.InvalidOperationException]::new(
            "ChristopherBellDev did not reach Stopped within $ServiceTimeoutSeconds seconds.",
            $_.Exception)
    }
    if ([string]$service.Status -ne 'Stopped') {
        throw "ChristopherBellDev did not reach Stopped within $ServiceTimeoutSeconds seconds."
    }

    $watch = [Diagnostics.Stopwatch]::StartNew()
    do {
        try {
            $listeners = @(
                Get-NetTCPConnection -State Listen -ErrorAction Stop |
                    Where-Object LocalPort -eq $ProductionPort
            )
        } catch {
            throw [System.InvalidOperationException]::new(
                "Failed to inspect production port $ProductionPort.",
                $_.Exception)
        }
        if ($listeners.Count -eq 0) { return }
        if ($watch.ElapsedMilliseconds -ge $PortTimeoutMilliseconds) { break }
        $remaining = $PortTimeoutMilliseconds - [int]$watch.ElapsedMilliseconds
        Start-Sleep -Milliseconds ([Math]::Max(1, [Math]::Min(250, $remaining)))
    } while ($true)

    throw "Production port $ProductionPort remained open after ChristopherBellDev stopped."
}

function Stop-ProductionWebsiteService {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateRange(1,65535)]
        [int]$ProductionPort,
        [ValidateRange(1,300)]
        [int]$ServiceTimeoutSeconds = 30,
        [ValidateRange(1,60000)]
        [int]$PortTimeoutMilliseconds = 10000
    )

    Set-ProductionWebsiteRecoveryPolicy -Policy Suspended
    $operationFailure = $null
    $restoreFailure = $null
    try {
        $stopFailure = $null
        try {
            Stop-Service -Name 'ChristopherBellDev' -ErrorAction Stop
        } catch {
            $stopFailure = $_.Exception
        }

        try {
            Assert-ProductionWebsiteStopped `
                -ProductionPort $ProductionPort `
                -ServiceTimeoutSeconds $ServiceTimeoutSeconds `
                -PortTimeoutMilliseconds $PortTimeoutMilliseconds
        } catch {
            $stateFailure = $_.Exception
            $operationFailure = if ($stopFailure) {
                [System.AggregateException]::new(
                    'Website service stop request and postcondition verification failed.',
                    [System.Exception[]]@($stopFailure, $stateFailure))
            } else {
                $stateFailure
            }
        }
    } finally {
        try {
            Set-ProductionWebsiteRecoveryPolicy -Policy Normal
        } catch {
            $restoreFailure = $_.Exception
        }
    }

    if ($restoreFailure) {
        if ($operationFailure) {
            throw [System.AggregateException]::new(
                'Website service stop and recovery restoration both failed.',
                [System.Exception[]]@($operationFailure, $restoreFailure))
        }
        throw [System.InvalidOperationException]::new(
            'Failed to restore website service recovery after the planned stop.',
            $restoreFailure)
    }
    if ($operationFailure) { throw $operationFailure }
}

function Switch-ProductionRelease {
```

Verification:

- `Policy` permits only the two valid recovery states.
- All `sc.exe` arguments remain structured and the checked process boundary preserves the cause.
- Service and port timeouts are bounded and validated before external effects.
- The stop exception is ignored only when both postconditions pass.
- Normal recovery restoration always runs after successful suspension and blocks return on failure.

#### Code Edit 1.3

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 98-119
- Action: replace

Current:

```powershell
function Switch-ProductionRelease {
    param($Config, [Parameter(Mandatory)][string]$Release)
    $release = Assert-ReleasePath $Config $Release
    $currentPath = Join-Path $Config.programDataRoot 'current'
    $previousPath = Join-Path $Config.programDataRoot 'previous'
    $old = Get-JunctionTarget $currentPath
    Stop-Service ChristopherBellDev -ErrorAction Stop
    try {
        if ($old) { Set-AtomicJunction $Config $previousPath $old }
        Set-AtomicJunction $Config $currentPath $release
        Start-Service ChristopherBellDev
        Test-ProductionEndpoints -Config $Config -Port $Config.productionPort
    } catch {
        if ($old) {
            Stop-Service ChristopherBellDev -ErrorAction SilentlyContinue
            Set-AtomicJunction $Config $currentPath $old
            Start-Service ChristopherBellDev
            Test-ProductionEndpoints -Config $Config -Port $Config.productionPort
        }
        throw
    }
}
```

Proposed:

```powershell
function Switch-ProductionRelease {
    param($Config, [Parameter(Mandatory)][string]$Release)
    $release = Assert-ReleasePath $Config $Release
    $currentPath = Join-Path $Config.programDataRoot 'current'
    $previousPath = Join-Path $Config.programDataRoot 'previous'
    $old = Get-JunctionTarget $currentPath
    Stop-ProductionWebsiteService -ProductionPort $Config.productionPort
    try {
        if ($old) { Set-AtomicJunction $Config $previousPath $old }
        Set-AtomicJunction $Config $currentPath $release
        Start-Service ChristopherBellDev
        Test-ProductionEndpoints -Config $Config -Port $Config.productionPort
    } catch {
        $deploymentFailure = $_.Exception
        if ($old) {
            try {
                Stop-ProductionWebsiteService -ProductionPort $Config.productionPort
                Set-AtomicJunction $Config $currentPath $old
                Start-Service ChristopherBellDev
                Test-ProductionEndpoints -Config $Config -Port $Config.productionPort
            } catch {
                throw [System.AggregateException]::new(
                    'Production deployment and automatic rollback both failed.',
                    [System.Exception[]]@($deploymentFailure, $_.Exception))
            }
        }
        throw $deploymentFailure
    }
}
```

Verification:

- The first junction mutation occurs only after the controlled stop returns.
- Forward restart occurs only after normal recovery restoration succeeds.
- Automatic rollback uses the same stop boundary.
- A failed rollback preserves both the deployment and rollback exceptions.

#### Code Edit 1.4

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 151
- Action: replace

Current:

```powershell
Export-ModuleMember -Function Invoke-ProductionDeploy,Resolve-OriginMainRelease,New-ReleaseFromOriginMain,Start-ProductionJar,Test-ProductionEndpoints,Test-CandidateRelease,Switch-ProductionRelease,Remove-ExpiredReleases
```

Proposed:

```powershell
Export-ModuleMember -Function Invoke-ProductionDeploy,Resolve-OriginMainRelease,New-ReleaseFromOriginMain,Start-ProductionJar,Test-ProductionEndpoints,Test-CandidateRelease,Stop-ProductionWebsiteService,Switch-ProductionRelease,Remove-ExpiredReleases
```

Verification:

- Import `Production.Deploy.psm1` and run `Get-Command Stop-ProductionWebsiteService`; expect one exported function from `Production.Deploy`.
- Private recovery and postcondition helpers remain unexported.

#### Code Edit 1.5

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: 16-27
- Action: replace

Current:

```powershell
        It 'restores the former release when production verification fails' {
            Mock Assert-ReleasePath { $Path }
            Mock Get-JunctionTarget { 'C:\data\releases\old' }
            Mock Stop-Service {}
            Mock Start-Service {}
            Mock Set-AtomicJunction {}
            $script:attempt = 0
            Mock Test-ProductionEndpoints { if ($script:attempt++ -eq 0) { throw 'failed verification' } }
            $config = [pscustomobject]@{ programDataRoot='C:\data'; productionPort=8080 }
            { Switch-ProductionRelease $config 'C:\data\releases\new' } | Should -Throw '*failed verification*'
            Should -Invoke Set-AtomicJunction -ParameterFilter { $Target -eq 'C:\data\releases\old' }
        }
```

Proposed:

```powershell
        It 'restores the former release through the controlled stop boundary when verification fails' {
            Mock Assert-ReleasePath { $Path }
            Mock Get-JunctionTarget { 'C:\data\releases\old' }
            Mock Stop-ProductionWebsiteService { }
            Mock Start-Service { }
            Mock Set-AtomicJunction { }
            $script:attempt = 0
            Mock Test-ProductionEndpoints {
                if ($script:attempt++ -eq 0) { throw 'failed verification' }
            }
            $config = [pscustomobject]@{
                programDataRoot = 'C:\data'
                productionPort = 8080
            }

            {
                Switch-ProductionRelease $config 'C:\data\releases\new'
            } | Should -Throw '*failed verification*'

            Should -Invoke Stop-ProductionWebsiteService -Times 2 -Exactly -ParameterFilter {
                $ProductionPort -eq 8080
            }
            Should -Invoke Set-AtomicJunction -ParameterFilter {
                $Target -eq 'C:\data\releases\old'
            }
        }

        It 'preserves deployment and rollback failures together' {
            Mock Assert-ReleasePath { $Path }
            Mock Get-JunctionTarget { 'C:\data\releases\old' }
            $script:stopAttempt = 0
            Mock Stop-ProductionWebsiteService {
                if ($script:stopAttempt++ -eq 1) { throw 'rollback stop failed' }
            }
            Mock Start-Service { }
            Mock Set-AtomicJunction { }
            Mock Test-ProductionEndpoints { throw 'deployment verification failed' }
            $config = [pscustomobject]@{
                programDataRoot = 'C:\data'
                productionPort = 8080
            }

            {
                Switch-ProductionRelease $config 'C:\data\releases\new'
            } | Should -Throw '*deployment and automatic rollback both failed*'
        }
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests\Production.Deploy.Tests.ps1' -Output Detailed"`.
- Expected GREEN: all deployment tests pass, including the exact RED regression.
- Run `git diff --check` and inspect production plus tests as one change.
- Commit with `fix: control Windows service stops during deploy` and push `codex/windows-service-stop-recovery`.

### Task 2 - Reuse the controlled stop boundary for manual rollback

Sequence / dependencies:

- Starts only after Task 1 is reviewed, committed, and pushed.
- Uses the exported function and combined-failure convention established by Task 1.

Implementation notes:

- Required skill: invoke `write-jane-street-style-code` before any code edits.
- Required sub-skill: use `superpowers:test-driven-development` and witness the rollback-specific RED test before editing `Production.Operations.psm1`.
- Before-Edit Brief:
  - Behavior: `prod.cmd rollback` uses the same controlled stop before both the requested junction swap and any restoration after failed verification.
  - Invariants: current/previous release paths remain validated; neither junction changes while the website or port is live; normal recovery is restored before every start.
  - Boundary/API: keep `Invoke-ProductionRollback([switch]$WhatIf)` and command routing compatible; consume exported `Stop-ProductionWebsiteService`.
  - Effects and failures: deployment lock, junction reads/writes, controlled service stop, restart, and HTTP verification remain explicit; requested rollback and restoration failures remain distinguishable.
  - Tests and evidence: a Pester test first fails because rollback still calls `Stop-Service`, then passes after both stop sites use the controlled boundary and combined failures are retained.

#### Code Edit 2.1

- File: `ops/production/windows/tests/Production.Operations.Tests.ps1`
- Lines: after 35
- Action: add

Current:

```powershell
        It 'refuses rollback unless both release junctions exist' {
            Mock Read-ProductionConfig { [pscustomobject]@{ programDataRoot='C:\data' } }
            Mock Enter-DeploymentLock { [IO.MemoryStream]::new() }
            Mock Get-JunctionTarget { $null }
            { Invoke-ProductionRollback -WhatIf } | Should -Throw '*Both current and previous*'
        }
```

Proposed:

```powershell
        It 'refuses rollback unless both release junctions exist' {
            Mock Read-ProductionConfig { [pscustomobject]@{ programDataRoot='C:\data' } }
            Mock Enter-DeploymentLock { [IO.MemoryStream]::new() }
            Mock Get-JunctionTarget { $null }
            { Invoke-ProductionRollback -WhatIf } | Should -Throw '*Both current and previous*'
        }

        It 'uses the controlled stop for rollback and restoration' {
            Mock Read-ProductionConfig {
                [pscustomobject]@{
                    programDataRoot = 'C:\data'
                    productionPort = 8080
                }
            }
            Mock Enter-DeploymentLock { [IO.MemoryStream]::new() }
            Mock Get-JunctionTarget {
                if ($Path -like '*\current') { return 'C:\data\releases\current' }
                return 'C:\data\releases\previous'
            }
            Mock Assert-ReleasePath { $Path }
            Mock Stop-Service { }
            Mock Stop-ProductionWebsiteService { }
            Mock Set-AtomicJunction { }
            Mock Start-Service { }
            $script:rollbackVerification = 0
            Mock Test-ProductionEndpoints {
                if ($script:rollbackVerification++ -eq 0) {
                    throw 'rollback verification failed'
                }
            }

            {
                Invoke-ProductionRollback
            } | Should -Throw '*rollback verification failed*'

            Should -Invoke Stop-ProductionWebsiteService -Times 2 -Exactly -ParameterFilter {
                $ProductionPort -eq 8080
            }
            Should -Invoke Set-AtomicJunction -ParameterFilter {
                $Target -eq 'C:\data\releases\current'
            }
            Should -Invoke Set-AtomicJunction -ParameterFilter {
                $Target -eq 'C:\data\releases\previous'
            }
        }
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests\Production.Operations.Tests.ps1' -Output Detailed"`.
- Expected RED: the new test reports zero calls to `Stop-ProductionWebsiteService` because production rollback still calls `Stop-Service` directly.
- Record the failing assertion before editing production code.

#### Code Edit 2.2

- File: `ops/production/windows/modules/Production.Operations.psm1`
- Lines: 18-45
- Action: replace

Current:

```powershell
function Invoke-ProductionRollback {
    [CmdletBinding()]
    param([switch]$WhatIf)
    $config = Read-ProductionConfig
    $lock = Enter-DeploymentLock (Join-Path $config.programDataRoot 'locks\deploy.lock')
    try {
        $current = Get-JunctionTarget (Join-Path $config.programDataRoot 'current')
        $previous = Get-JunctionTarget (Join-Path $config.programDataRoot 'previous')
        if (-not $current -or -not $previous) { throw 'Both current and previous releases are required.' }
        Assert-ReleasePath $config $current | Out-Null
        Assert-ReleasePath $config $previous | Out-Null
        if ($WhatIf) { Write-Output "Would roll back from $current to $previous"; return }
        Stop-Service ChristopherBellDev
        Set-AtomicJunction $config (Join-Path $config.programDataRoot 'current') $previous
        Set-AtomicJunction $config (Join-Path $config.programDataRoot 'previous') $current
        try {
            Start-Service ChristopherBellDev
            Test-ProductionEndpoints $config $config.productionPort
        } catch {
            Stop-Service ChristopherBellDev -ErrorAction SilentlyContinue
            Set-AtomicJunction $config (Join-Path $config.programDataRoot 'current') $current
            Set-AtomicJunction $config (Join-Path $config.programDataRoot 'previous') $previous
            Start-Service ChristopherBellDev
            Test-ProductionEndpoints $config $config.productionPort
            throw
        }
    } finally { $lock.Dispose() }
}
```

Proposed:

```powershell
function Invoke-ProductionRollback {
    [CmdletBinding()]
    param([switch]$WhatIf)
    $config = Read-ProductionConfig
    $lock = Enter-DeploymentLock (Join-Path $config.programDataRoot 'locks\deploy.lock')
    try {
        $currentPath = Join-Path $config.programDataRoot 'current'
        $previousPath = Join-Path $config.programDataRoot 'previous'
        $current = Get-JunctionTarget $currentPath
        $previous = Get-JunctionTarget $previousPath
        if (-not $current -or -not $previous) {
            throw 'Both current and previous releases are required.'
        }
        Assert-ReleasePath $config $current | Out-Null
        Assert-ReleasePath $config $previous | Out-Null
        if ($WhatIf) {
            Write-Output "Would roll back from $current to $previous"
            return
        }

        Stop-ProductionWebsiteService -ProductionPort $config.productionPort
        Set-AtomicJunction $config $currentPath $previous
        Set-AtomicJunction $config $previousPath $current
        try {
            Start-Service ChristopherBellDev
            Test-ProductionEndpoints $config $config.productionPort
        } catch {
            $rollbackFailure = $_.Exception
            try {
                Stop-ProductionWebsiteService -ProductionPort $config.productionPort
                Set-AtomicJunction $config $currentPath $current
                Set-AtomicJunction $config $previousPath $previous
                Start-Service ChristopherBellDev
                Test-ProductionEndpoints $config $config.productionPort
            } catch {
                throw [System.AggregateException]::new(
                    'Production rollback and release restoration both failed.',
                    [System.Exception[]]@($rollbackFailure, $_.Exception))
            }
            throw $rollbackFailure
        }
    } finally {
        $lock.Dispose()
    }
}
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests\Production.Operations.Tests.ps1' -Output Detailed"`.
- Expected GREEN: the exact RED test passes and existing rollback, startup, backup, and status tests remain green.
- Run both focused files together: `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests\Production.Deploy.Tests.ps1','.\ops\production\windows\tests\Production.Operations.Tests.ps1' -Output Detailed"`.
- Run `git diff --check` and apply the Jane Street review rubric to both modules and tests.
- Commit with `fix: reuse controlled stop for Windows rollback` and push the branch.

### Task 3 - Run complete verification, independent review, PR, CI, and merge

Sequence / dependencies:

- Starts only after Tasks 1 and 2 are independently green, reviewed locally, committed, and pushed.
- Contains no planned production code edits; any remediation re-enters the applicable task's RED/GREEN cycle.

Implementation notes:

- Required skill: invoke `write-jane-street-style-code` in Review Mode for the final production/test diff.
- Review boundary: compare `codex/windows-service-stop-recovery` with exact base `4429d11cb3d879315f8c5489909b28b8c70bc37c`.

Verification steps:

1. Run focused Pester:

   ```powershell
   pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests\Production.Deploy.Tests.ps1','.\ops\production\windows\tests\Production.Operations.Tests.ps1' -Output Detailed"
   ```

   Expected: all focused tests pass with zero failed containers or tests.

2. Run the full Windows production suite:

   ```powershell
   pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path '.\ops\production\windows\tests' -Output Detailed"
   ```

   Expected: all Windows production tests pass.

3. Run the repository build with an isolated Gradle home if the shared daemon registry is inaccessible:

   ```powershell
   $env:GRADLE_USER_HOME = Join-Path $env:TEMP 'cbdev-controlled-stop-gradle'
   .\gradlew.bat --no-daemon build
   ```

   Expected: `BUILD SUCCESSFUL`.

4. Run `git diff --check`, inspect `git status --short --branch`, and review every changed line against the Before-Edit Briefs and Jane Street blockers/warnings.
5. Obtain an independent spoke review that checks recovery restoration, failure aggregation, service/port postconditions, deployment ordering, rollback ordering, and test evidence.
6. Remediate every blocker with a new focused RED/GREEN cycle. Commit and push each completed remediation.
7. Open a pull request to `main` with the root-cause evidence, task commits, exact commands/results, rollback plan, and explicit note that shared-folder code is unchanged.
8. Wait for Windows, macOS, Ubuntu, and CodeQL checks. Diagnose any failure from its first actionable cause; do not merge around a failing gate.
9. Merge only after all required checks and independent review pass. Record the exact merge commit and tree.

## Task 4 - Retry production deployment and close the Builder work

Sequence / dependencies:

- Starts only after Task 3 is merged and the exact merged SHA/tree are known.
- Production remains feature-disabled until the elevated acceptance run succeeds.
- Contains no repository code edits unless production evidence exposes a new defect; any defect returns to design/TDD/review rather than being patched directly on the host.

Production steps:

1. Confirm the website is `Running`, `http://127.0.0.1:8080/` returns HTTP 200 with a non-empty body, the shared worker is absent, the feature flag is absent, and both shared roots exist.
2. Confirm the source worktree is clean and exactly matches the merged SHA/tree.
3. Update the prepared elevated installer and rollback scripts under `A:\Temp\cbdev-shared-folder-production-20260722-064200` to require the new exact merge SHA/tree. Do not print secrets or protected environment values.
4. Run the installer elevated after UAC approval.
5. Inspect `sc.exe qfailure ChristopherBellDev`; require reset period 3,600 seconds and restart actions after 10,000 and 30,000 milliseconds.
6. Require `ChristopherBellDev` to be `Running`, port 8080 to have exactly the intended listener, and `/` to return HTTP 200 with the expected non-empty website body.
7. Require the shared-folder worker to be installed under its intended least-privilege identity and `Running`.
8. Confirm `A:\Shared` and `A:\Shared-System` still exist and were not recreated over existing content.
9. Require the active release metadata to match the exact merged SHA/tree.
10. Verify `/shared` for an authorized logged-in account, verify anonymous shared API access returns 401, and run the installed-worker acceptance check.
11. Run `prod.cmd verify-startup` and record its complete result.
12. If any acceptance item fails, run the prepared rollback elevated, then prove HTTP 200, normal recovery restored, worker absent, feature flag absent, and both shared roots preserved.
13. Save a Builder test report with requests, responses, service/recovery evidence, exact SHA/tree, pass/fail results, and any gaps.
14. Ingest and review the spoke update, close the hub work, save session memory, refresh indexes, validate Builder, then commit and push each Builder checkpoint to `main`.

## Code Changes

- Add private recovery-policy and stop-postcondition helpers to `Production.Deploy.psm1`.
- Export `Stop-ProductionWebsiteService` as the one cross-module controlled-stop boundary.
- Replace direct deployment and automatic-rollback `Stop-Service` calls with the controlled boundary.
- Replace direct manual-rollback and restoration `Stop-Service` calls with the same boundary.
- Add focused Pester coverage for recovery suspension/restoration, thrown stop acceptance, service timeout, open port, deployment rollback, manual rollback, and combined failures.
- Do not change Java, JavaScript, shared-folder configuration, WinSW XML, storage roots, or media tooling.

## Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: owns recovery state, service/port postconditions, controlled stop, forward release switch, and automatic rollback.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: proves the controlled-stop contract and deployment sequencing.
- `ops/production/windows/modules/Production.Operations.psm1`: consumes the exported boundary for manual rollback and restoration.
- `ops/production/windows/tests/Production.Operations.Tests.ps1`: proves manual rollback integration without duplicating stop internals.
- `ops/production/windows/modules/Production.Install.psm1`: remains the source of truth for the same normal recovery values; no planned edit.
- `ops/production/windows/service/ChristopherBellDev.xml`: remains on stable WinSW 2.12.0; no planned edit.

## Unit Testing

- RED/GREEN: `Production.Deploy.Tests.ps1` for the controlled-stop boundary and deployment integration.
- RED/GREEN: `Production.Operations.Tests.ps1` for manual rollback integration.
- Focus assertions on observable outcomes and meaningful effect requests: accepted/rejected stop, recovery transitions, junction targets, start/verification ordering, and preserved failures.
- Avoid assertions on private helper implementation beyond the required structured `sc.exe` arguments.
- Run both focused files together after each task to catch module-export and cross-module regressions.

## Local Testing

- Run the full Windows production Pester directory from the isolated spoke worktree.
- Run `gradlew.bat --no-daemon build` with an isolated Gradle home and require `BUILD SUCCESSFUL`.
- Do not perform an unreviewed stop against the live `ChristopherBellDev` service during local development.
- The merged elevated deployment is the integration test for real Service Control Manager recovery mutation and the observed WinSW failure path.
- Record HTTP request `GET /`, expected status 200, and non-empty response-body evidence before and after the production switch.
- Record authenticated `GET /shared`, anonymous shared API 401, installed-worker acceptance, and startup verification in the Builder test report.

## Validation

- Builder plan validator returns no errors.
- Plan review reports no blockers and `ready` state before execution.
- Focused RED evidence is captured before each production edit.
- Focused and full Pester suites pass.
- Gradle build passes locally and GitHub Windows/macOS/Ubuntu plus CodeQL checks pass.
- Independent review reports no unresolved Critical or Important findings.
- Final diff contains only the four planned spoke files unless a separately reviewed remediation is required.
- Production recovery inspection, service status, TCP listener, HTTP evidence, worker identity/state, root preservation, active release, authorization, worker acceptance, and startup verification all pass.

## Rollback or Recovery

- Before merge, revert the task commit that introduced the failing behavior and rerun focused plus full verification.
- During production retry, use the prepared elevated rollback script if any postcondition fails.
- A failed recovery restoration blocks `Start-Service`; investigate and reapply `sc.exe failure ChristopherBellDev reset= 3600 actions= restart/10000/restart/30000` before allowing a restart.
- After rollback, require the website `Running`, HTTP 200 with non-empty body, normal recovery actions restored, worker absent, feature flag absent, and both shared roots preserved.
- Never delete `A:\Shared`, `A:\Shared-System`, the existing production release, or the prior release as part of rollback.

## Risks

- **No-action recovery syntax is passed incorrectly:** keep the empty value as a distinct `ProcessStartInfo.ArgumentList` item, assert it in Pester, and prove it with live `sc.exe qfailure` output.
- **A thrown stop hides a live service:** require both `Stopped` service state and a closed production port; exception text is irrelevant.
- **A stopped service leaves a child listener:** the port postcondition blocks junction mutation.
- **Recovery remains suspended:** restoration runs in `finally`; restoration failure blocks return and therefore blocks restart.
- **A primary failure is hidden by rollback/cleanup:** use `AggregateException` when both operations fail and assert combined diagnostics.
- **Polling hangs:** service and port waits have validated upper bounds.
- **Rollback duplicates unsafe logic:** both deployment and operations consume the same exported stop boundary.
- **Cross-platform CI cannot exercise Windows service APIs:** focused Pester runs on the Windows host; GitHub cross-platform builds protect the application regression surface; production acceptance proves the real SCM seam.
- **Production interruption:** preflight the safe state, preserve the prepared rollback, and keep the change limited to the intentional stop window.

## Completion Criteria

- The approved spec remains satisfied with no unresolved open question.
- Both task-specific RED failures were observed before their production edits.
- All focused and aggregate tests pass.
- Each code task was reviewed, committed, and pushed before the next task began.
- Independent review and all pull-request checks pass.
- The PR is merged and exact merge SHA/tree are recorded.
- Production deployment succeeds with normal recovery restored and the public site healthy.
- Shared-folder worker, roots, authorization, installed-worker acceptance, and startup verification pass.
- Builder test report, spoke update/review, closure, session memory, indexes, and validation are committed and pushed.
