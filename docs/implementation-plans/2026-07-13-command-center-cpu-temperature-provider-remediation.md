# christopherbell.dev Command Center CPU Temperature Provider Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task in the current session. Do not delegate unless Christopher explicitly requests subagents. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the Defender-flagged WinRing0 runtime, install and validate official PawnIO 2.2.0 without automatically enabling it, and restore CPU temperature through pinned LibreHardwareMonitor 0.9.6 resources only after every candidate and production safety gate passes.

**Architecture:** Production stores a protected `sensorLibrariesEnabled` boolean in `deploy.json`, defaults it to false, and maps it to the existing Spring environment switch at service startup. A local elevated `Production.Sensors` module owns fixed PawnIO download, hash/signature/Defender/install/status/enable/disable operations; the HTTP application cannot invoke it. Gradle downloads one pinned official LibreHardwareMonitor archive, extracts a fixed hash-pinned runtime set into generated resources, and the existing ACL-restricted provisioner plus bounded one-shot PowerShell probe consume those files.

**Tech Stack:** Java 25, Spring Boot, Gradle Kotlin DSL, Windows PowerShell 5.1 sensor process, PowerShell 7 production tooling, Pester 5, LibreHardwareMonitor 0.9.6, PawnIO 2.2.0, Microsoft Defender, WinSW, GitHub Actions, CodeQL.

## Global Constraints

- Keep `COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED=false` in production until every enablement gate passes.
- Never suppress, exclude, allow-list, or weaken Microsoft Defender.
- Never restore, rename, retain, or package WinRing0 or `jLibreHardwareMonitor` 1.0.6.
- Use only PawnIO 2.2.0 installer SHA-256 `1F519A22E47187F70A1379A48CA604981C4FCF694F4E65B734AAA74A9FBA3032`, Authenticode thumbprint `F380DCC9F706E2756A5047B832FFE719E1BC35F5`, and the official `namazso/PawnIO.Setup` release URL.
- Use only LibreHardwareMonitor 0.9.6 archive SHA-256 `086D9F1B5A99E643EDC2CFAAAC16051685B551E4C5AC0B32A57C58C0E529C001` from the official release URL.
- Keep PawnIO administrator-only and keep install/enable operations outside all HTTP request handling.
- Preserve fixed PowerShell arguments, bounded output, process-tree cleanup, cached refresh, sane Celsius parsing, and fail-closed unavailable behavior.
- Never reboot, shut down, or power-cycle automatically; installer exit 3010 stops execution and leaves sensors disabled.
- Verify on a non-8080 port before changing live production state.
- Preserve the divergent primary spoke checkout and unrelated dirty state.

---

## Document Status

ready-for-execution

## Objective

Deliver the approved remediation from test-first code changes through official-provider installation, alternate-port verification, PR/CI, merge, native Windows deployment, separately gated production enablement, live observation, and Builder closure.

## Goals

- Make sensor-disabled the durable production default and expose explicit local-only lifecycle commands.
- Reject any PawnIO artifact with the wrong URL, hash, signature, thumbprint, Defender result, version, or driver state.
- Remove the old Maven wrapper and its WinRing0-capable DLL from the dependency graph and built application.
- Package a fixed, checksum-pinned LibreHardwareMonitor 0.9.6 runtime from the official archive.
- Return an explicit unavailable CPU temperature when PawnIO is missing or unhealthy without repeatedly spawning failing probes.
- Prove plausible CPU temperature, service stability, process stability, and clean Defender state before and after production enablement.

## Inputs

- Approved spec: `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-13-command-center-cpu-temperature-provider-remediation.md`.
- Existing work record: `C:\Users\Christopher\Developer\builder\docs\work\2026-07-12-command-center-cpu-temperature-and-uptime.md`.
- Prior test report: `C:\Users\Christopher\Developer\builder\docs\test-reports\2026-07-12-command-center-cpu-temperature-and-uptime-test-report.md`.
- Spoke: `A:\Projects\christopherbell.dev`, remote `https://github.com/azurras/christopherbell.dev.git`.
- Current base: refreshed `origin/main` at `405bff22f008a6f6eec505c1949503949a717c31` or later.
- Production: native Windows services `MongoDB`, `ChristopherBellDev`, and `cloudflared`; website port 8080.
- Containment: installed startup script currently forces sensor libraries false and homepage returns HTTP 200 with `<title>CB | Home</title>`.
- Threat evidence: Defender `VulnerableDriver:WinNT/Winring0`, executed but contained/inactive before this plan.
- User decisions: direct PawnIO plus LibreHardwareMonitor design approved; stop before any reboot.

## Branch

- Refresh `origin/main`, then create or switch the clean isolated worktree `A:\Projects\christopherbell.dev-worktrees\command-center-cpu-temperature` to `codex/pawnio-cpu-temperature` from the refreshed remote base.
- Do not switch, reset, clean, or otherwise modify `A:\Projects\christopherbell.dev`.

## Non-Goals

- No LibreHardwareMonitor GUI, WMI service, remote driver-management endpoint, or monitoring agent.
- No automatic PawnIO uninstall; use the verified Windows uninstall entry under explicit operator control if rollback requires removal.
- No Defender exclusions or reduced Windows security settings.
- No new command-center browser controls for installing or enabling hardware providers.
- No changes to uptime formatting, power-action behavior, or unrelated telemetry providers.

## Assumptions

- PowerShell 7 and Pester 5 remain available for production operations tests.
- Windows PowerShell 5.1 remains the fixed bounded sensor host.
- PawnIO 2.2.0 silent mode accepts `/S` and returns DOS error 3010 when a reboot is required, as described by its official release notes; the first execution must confirm this contract while sensors remain disabled.
- The PawnIO driver and uninstall registration use the reviewed `PawnIO` identity; post-install status must prove the actual registered identity before enablement.
- The official .NET Framework LibreHardwareMonitor release contains the fixed runtime files and hashes listed in Task 3.
- Production continues running as SYSTEM, while the website remains healthy with sensors absent or disabled.

## Open Questions

None.

## Task Breakdown

### Task 1 - Make sensor disablement a protected durable production default

Sequence / dependencies:
- First code task; it ensures every later install, build, deploy, and rollback starts fail-closed.

Implementation notes:
- Store the state in protected `deploy.json`; do not add it to secret `app.env`.
- The startup script converts only the typed configuration boolean to lowercase `true` or `false`.
- Existing configuration merge behavior introduces the default without replacing any other operator value.

#### Code Edit 1.1
- File: `ops/production/windows/tests/Production.Install.Tests.ps1`
- Lines: after 47
- Action: add

Proposed:
```powershell
    It 'adds the sensor provider switch disabled without replacing existing values' {
        $root = Join-Path $TestDrive 'sensor-default'
        New-ProductionDirectories $root
        $deploy = Join-Path $root 'config\deploy.json'
        @{ repositoryPath='A:\custom-repository'; sensorLibrariesEnabled=$true } |
            ConvertTo-Json | Set-Content $deploy

        Install-ConfigurationExamples $root

        $updated = Get-Content $deploy -Raw | ConvertFrom-Json
        $updated.sensorLibrariesEnabled | Should -BeTrue
        $example = Get-Content (Join-Path $root 'config\deploy.example.json') -Raw | ConvertFrom-Json
        $example.sensorLibrariesEnabled | Should -BeFalse
    }

    It 'starts the website with the protected typed sensor switch' {
        $startup = Get-Content (Join-Path $PSScriptRoot '..\service\Start-ChristopherBellDev.ps1') -Raw
        $startup | Should -Match "sensorLibrariesEnabled"
        $startup | Should -Match "COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED"
        $startup | Should -Not -Match "SetEnvironmentVariable\('COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED',\s*'true'"
    }
```

Verification:
- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester ops/production/windows/tests/Production.Install.Tests.ps1 -Output Detailed"`.
- Expected RED: the example configuration has no `sensorLibrariesEnabled` property and the checked-in startup script does not map it.

#### Code Edit 1.2
- File: `ops/production/windows/config/deploy.example.json`
- Lines: 1-19
- Action: replace

Current:
```json
{
  "repositoryPath": "A:\\Projects\\christopherbell.dev",
  "remote": "origin",
  "branch": "main",
  "programDataRoot": "C:\\ProgramData\\christopherbell.dev",
  "javaExe": "C:\\Program Files\\Eclipse Adoptium\\jdk-25\\bin\\java.exe",
  "nodeExe": "C:\\Program Files\\nodejs\\node.exe",
  "mongoToolsPath": "C:\\Program Files\\MongoDB\\Tools\\100\\bin",
  "mongoShellExe": "C:\\Program Files\\MongoDB\\mongosh\\current\\bin\\mongosh.exe",
  "cloudflaredExe": "C:\\Program Files (x86)\\cloudflared\\cloudflared.exe",
  "backupRoot": "A:\\Projects\\christopherbell.dev-backups",
  "publicUrl": "https://www.christopherbell.dev/",
  "candidatePort": 8081,
  "productionPort": 8080,
  "smokeAccountEmail": "operator@example.com",
  "releaseRetention": 5,
  "autoDeployPollSeconds": 60,
  "autoDeployFailureBackoffSeconds": 900
}
```

Proposed:
```json
{
  "repositoryPath": "A:\\Projects\\christopherbell.dev",
  "remote": "origin",
  "branch": "main",
  "programDataRoot": "C:\\ProgramData\\christopherbell.dev",
  "javaExe": "C:\\Program Files\\Eclipse Adoptium\\jdk-25\\bin\\java.exe",
  "nodeExe": "C:\\Program Files\\nodejs\\node.exe",
  "mongoToolsPath": "C:\\Program Files\\MongoDB\\Tools\\100\\bin",
  "mongoShellExe": "C:\\Program Files\\MongoDB\\mongosh\\current\\bin\\mongosh.exe",
  "cloudflaredExe": "C:\\Program Files (x86)\\cloudflared\\cloudflared.exe",
  "backupRoot": "A:\\Projects\\christopherbell.dev-backups",
  "publicUrl": "https://www.christopherbell.dev/",
  "candidatePort": 8081,
  "productionPort": 8080,
  "smokeAccountEmail": "operator@example.com",
  "sensorLibrariesEnabled": false,
  "releaseRetention": 5,
  "autoDeployPollSeconds": 60,
  "autoDeployFailureBackoffSeconds": 900
}
```

Verification:
- Run the focused Pester file; the default/preservation test must pass.

#### Code Edit 1.3
- File: `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- Lines: 1-10
- Action: replace

Current:
```powershell
$ErrorActionPreference = 'Stop'
$root = 'C:\ProgramData\christopherbell.dev'
$config = Get-Content -LiteralPath (Join-Path $root 'config\deploy.json') -Raw | ConvertFrom-Json
$allowed = @('APP_JWT_SECRET','RESEND_API_KEY','APP_MAIL_FROM','SPRING_MONGODB_URI')
foreach ($line in Get-Content -LiteralPath (Join-Path $root 'config\app.env')) {
    if ($line -match '^([A-Z0-9_]+)=(.*)$' -and $allowed -contains $Matches[1]) {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
& $config.javaExe '-Xrs' '-jar' (Join-Path $root 'current\app.jar') '--spring.profiles.active=prod' "--server.port=$($config.productionPort)"
exit $LASTEXITCODE
```

Proposed:
```powershell
$ErrorActionPreference = 'Stop'
$root = 'C:\ProgramData\christopherbell.dev'
$config = Get-Content -LiteralPath (Join-Path $root 'config\deploy.json') -Raw | ConvertFrom-Json
$sensorProperty = $config.PSObject.Properties['sensorLibrariesEnabled']
if (-not $sensorProperty -or $sensorProperty.Value -isnot [bool]) {
    throw 'deploy.json sensorLibrariesEnabled must be a Boolean.'
}
$sensorLibrariesEnabled = if ($sensorProperty.Value) { 'true' } else { 'false' }
[Environment]::SetEnvironmentVariable(
    'COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED', $sensorLibrariesEnabled, 'Process')
$allowed = @('APP_JWT_SECRET','RESEND_API_KEY','APP_MAIL_FROM','SPRING_MONGODB_URI')
foreach ($line in Get-Content -LiteralPath (Join-Path $root 'config\app.env')) {
    if ($line -match '^([A-Z0-9_]+)=(.*)$' -and $allowed -contains $Matches[1]) {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
& $config.javaExe '-Xrs' '-jar' (Join-Path $root 'current\app.jar') '--spring.profiles.active=prod' "--server.port=$($config.productionPort)"
exit $LASTEXITCODE
```

Verification:
- Run the focused Pester file and parse the startup script with `[System.Management.Automation.Language.Parser]::ParseFile`; expect zero errors.

#### Code Edit 1.4
- File: `ops/production/windows/tests/Production.Common.Tests.ps1`
- Lines: 15-23
- Action: replace

Current:
```powershell
        $script:validConfig = @{
            repositoryPath=$repo; remote='origin'; branch='main'; programDataRoot=(Join-Path $TestDrive 'data')
            javaExe=$java.FullName; nodeExe=$node.FullName; mongoToolsPath=$tools; mongoShellExe=$mongosh.FullName
            backupRoot=$backup
            cloudflaredExe=(New-Item -ItemType File -Force (Join-Path $TestDrive 'cloudflared.exe')).FullName
            publicUrl='https://www.christopherbell.dev/'
            smokeAccountEmail='admin@christopherbell.dev'; candidatePort=8081; productionPort=8080
            releaseRetention=5; autoDeployPollSeconds=60; autoDeployFailureBackoffSeconds=900
        }
```

Proposed:
```powershell
        $script:validConfig = @{
            repositoryPath=$repo; remote='origin'; branch='main'; programDataRoot=(Join-Path $TestDrive 'data')
            javaExe=$java.FullName; nodeExe=$node.FullName; mongoToolsPath=$tools; mongoShellExe=$mongosh.FullName
            backupRoot=$backup
            cloudflaredExe=(New-Item -ItemType File -Force (Join-Path $TestDrive 'cloudflared.exe')).FullName
            publicUrl='https://www.christopherbell.dev/'
            smokeAccountEmail='admin@christopherbell.dev'; candidatePort=8081; productionPort=8080
            sensorLibrariesEnabled=$false
            releaseRetention=5; autoDeployPollSeconds=60; autoDeployFailureBackoffSeconds=900
        }
```

Verification:
- Run `Production.Common.Tests.ps1`; the complete valid configuration must still load.

#### Code Edit 1.5
- File: `ops/production/windows/tests/Production.Common.Tests.ps1`
- Lines: after 36
- Action: add

Proposed:
```powershell
    It 'rejects a missing or string sensor provider switch' {
        $validConfig.Remove('sensorLibrariesEnabled')
        $validConfig | ConvertTo-Json | Set-Content $configPath
        { Read-ProductionConfig -Path $configPath } | Should -Throw '*Boolean*'
        $validConfig.sensorLibrariesEnabled = 'false'
        $validConfig | ConvertTo-Json | Set-Content $configPath
        { Read-ProductionConfig -Path $configPath } | Should -Throw '*Boolean*'
    }
```

Verification:
- Expected RED: `Read-ProductionConfig` accepts the string and can cast it truthy.

#### Code Edit 1.6
- File: `ops/production/windows/modules/Production.Common.psm1`
- Lines: after 23
- Action: add

Proposed:
```powershell
    $sensorProperty = $config.PSObject.Properties['sensorLibrariesEnabled']
    if (-not $sensorProperty -or $sensorProperty.Value -isnot [bool]) {
        throw 'sensorLibrariesEnabled must be a Boolean.'
    }
```

Verification:
- Run `Production.Common.Tests.ps1`; missing/string states must fail and a JSON Boolean false must pass.
- Commit Task 1 with `git commit -m "Default production sensors to disabled"`.

### Task 2 - Add guarded local PawnIO lifecycle operations

Sequence / dependencies:
- Runs after Task 1 because install and enable operations rely on the protected false-by-default configuration state.

Implementation notes:
- The module owns only fixed constants and local elevated commands; no value comes from HTTP or browser input.
- Installation downloads into `C:\ProgramData\christopherbell.dev\sensors`, verifies before execution, scans before and after, and does not enable the feature.
- `sensor-enable` first proves PawnIO and Defender state, atomically updates the boolean, restarts only ChristopherBellDev, and restores false if endpoint verification fails.
- `sensor-disable` is idempotent and does not require PawnIO to be healthy.

#### Code Edit 2.1
- File: `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- Lines: 1-1
- Action: add

Proposed:
```powershell
Import-Module (Join-Path $PSScriptRoot '..\modules\Production.Common.psm1') -Global -Force
Import-Module (Join-Path $PSScriptRoot '..\modules\Production.Deploy.psm1') -Force
Import-Module (Join-Path $PSScriptRoot '..\modules\Production.Sensors.psm1') -Force

Describe 'PawnIO sensor provider operations' {
    InModuleScope Production.Sensors {
        BeforeEach {
            Mock Assert-SensorAdministrator {}
            Mock Assert-NoActiveSensorThreat {}
            Mock Start-MpScan {}
            Mock Restart-Service {}
            Mock Test-ProductionEndpoints {}
        }

        It 'rejects an installer whose hash or signer thumbprint differs' {
            Mock Test-Path { $true }
            Mock Get-FileHash { [pscustomobject]@{ Hash='BAD' } }
            Mock Get-AuthenticodeSignature {
                [pscustomobject]@{ Status='Valid'; SignerCertificate=[pscustomobject]@{ Thumbprint='BAD' } }
            }
            { Assert-PawnIoInstaller -Path 'C:\audit\PawnIO_setup.exe' } |
                Should -Throw '*SHA-256*'
        }

        It 'treats installer reboot-required as a stop with sensors still disabled' {
            Mock Invoke-WebRequest { 'installer' | Set-Content -LiteralPath $OutFile }
            Mock Assert-PawnIoInstaller {}
            Mock Start-Process { [pscustomobject]@{ ExitCode=3010 } }
            Mock Set-ProductionSensorState {}
            { Install-PawnIoProvider -Root $TestDrive } | Should -Throw '*reboot required*'
            Should -Invoke Set-ProductionSensorState -ParameterFilter { -not $Enabled }
        }

        It 'never enables sensors as part of a successful install' {
            Mock Invoke-WebRequest { 'installer' | Set-Content -LiteralPath $OutFile }
            Mock Assert-PawnIoInstaller {}
            Mock Start-Process { [pscustomobject]@{ ExitCode=0 } }
            Mock Set-ProductionSensorState {}
            Mock Assert-PawnIoInstallation { [pscustomobject]@{ Version='2.2.0'; Driver='Running' } }
            Install-PawnIoProvider -Root $TestDrive
            Should -Invoke Set-ProductionSensorState -Times 1 -ParameterFilter { -not $Enabled }
            Should -Invoke Start-MpScan -Times 2
        }

        It 'fails enablement closed and restores false when endpoint verification fails' {
            $configPath = Join-Path $TestDrive 'deploy.json'
            @{ productionPort=8080; sensorLibrariesEnabled=$false } | ConvertTo-Json | Set-Content $configPath
            Mock Assert-PawnIoInstallation { [pscustomobject]@{ Version='2.2.0'; Driver='Running' } }
            Mock Test-ProductionEndpoints { throw 'endpoint failed' }
            { Set-ProductionSensorState -Enabled $true -ConfigPath $configPath } | Should -Throw '*endpoint failed*'
            (Get-Content $configPath -Raw | ConvertFrom-Json).sensorLibrariesEnabled | Should -BeFalse
            Should -Invoke Restart-Service -Times 2 -ParameterFilter { $Name -eq 'ChristopherBellDev' }
        }

        It 'reports protected state installation and active threat state without mutation' {
            $configPath = Join-Path $TestDrive 'deploy.json'
            @{ sensorLibrariesEnabled=$false } | ConvertTo-Json | Set-Content $configPath
            Mock Get-PawnIoInstallation {
                [pscustomobject]@{
                    Version='2.2.0'; Driver='Running'; DriverPath='C:\Windows\System32\drivers\PawnIO.sys'
                    DriverSignature='Valid'; UninstallString='C:\Program Files\PawnIO\uninstall.exe'
                }
            }
            Mock Get-MpThreat { @() }
            $status = Get-ProductionSensorStatus -ConfigPath $configPath
            $status.Enabled | Should -BeFalse
            $status.PawnIoVersion | Should -Be '2.2.0'
            $status.Driver | Should -Be 'Running'
            $status.DriverSignature | Should -Be 'Valid'
            $status.UninstallRegistered | Should -BeTrue
            $status.ActiveThreats | Should -Be 0
        }

        It 'rejects an installed driver without a valid Windows signature' {
            Mock Get-PawnIoInstallation {
                [pscustomobject]@{ Version='2.2.0'; Driver='Running'; DriverSignature='NotSigned' }
            }
            { Assert-PawnIoInstallation } | Should -Throw '*signature*'
        }
    }
}
```

Verification:
- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester ops/production/windows/tests/Production.Sensors.Tests.ps1 -Output Detailed"`.
- Expected RED: `Production.Sensors.psm1` and every production function are missing.

#### Code Edit 2.2
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: 1-1
- Action: add

Proposed:
```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:PawnIoUri = 'https://github.com/namazso/PawnIO.Setup/releases/download/2.2.0/PawnIO_setup.exe'
$script:PawnIoSha256 = '1F519A22E47187F70A1379A48CA604981C4FCF694F4E65B734AAA74A9FBA3032'
$script:PawnIoSignerThumbprint = 'F380DCC9F706E2756A5047B832FFE719E1BC35F5'
$script:PawnIoVersion = '2.2.0'
$script:PawnIoRegistryPaths = @(
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO',
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO')

function Assert-SensorAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]$identity
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'Sensor provider operations require elevated PowerShell.'
    }
}

function Assert-NoActiveSensorThreat {
    $active = @(Get-MpThreat -ErrorAction Stop | Where-Object {
        $_.IsActive -and [string]$_.ThreatName -match '(?i)(Winring0|PawnIO)'
    })
    if ($active.Count -gt 0) { throw 'Microsoft Defender reports an active sensor-provider threat.' }
}

function Assert-PawnIoInstaller {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw 'PawnIO installer is missing.' }
    if ((Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash -ne $script:PawnIoSha256) {
        throw 'PawnIO installer SHA-256 verification failed.'
    }
    $signature = Get-AuthenticodeSignature -LiteralPath $Path
    $thumbprint = if ($signature.SignerCertificate) { [string]$signature.SignerCertificate.Thumbprint } else { '' }
    if ([string]$signature.Status -ne 'Valid' -or $thumbprint -ne $script:PawnIoSignerThumbprint) {
        throw 'PawnIO installer publisher verification failed.'
    }
}

function Get-PawnIoInstallation {
    foreach ($path in $script:PawnIoRegistryPaths) {
        if (Test-Path -LiteralPath $path) {
            $entry = Get-ItemProperty -LiteralPath $path
            $driver = Get-CimInstance Win32_SystemDriver -Filter "Name='PawnIO'" -ErrorAction SilentlyContinue
            $driverPath = if ($driver) {
                [Environment]::ExpandEnvironmentVariables([string]$driver.PathName).Trim('"')
            } else { $null }
            if ($driverPath -and $driverPath.StartsWith('\SystemRoot', [StringComparison]::OrdinalIgnoreCase)) {
                $driverPath = Join-Path $env:SystemRoot $driverPath.Substring(12)
            }
            if ($driverPath -and $driverPath.StartsWith('\??\')) { $driverPath = $driverPath.Substring(4) }
            $driverSignature = if ($driverPath -and (Test-Path -LiteralPath $driverPath -PathType Leaf)) {
                (Get-AuthenticodeSignature -LiteralPath $driverPath).Status.ToString()
            } else { 'Missing' }
            return [pscustomobject]@{
                Version = [string]$entry.DisplayVersion
                Driver = if ($driver) { [string]$driver.State } else { 'Missing' }
                DriverPath = $driverPath
                DriverSignature = $driverSignature
                UninstallString = [string]$entry.UninstallString
            }
        }
    }
    return $null
}

function Assert-PawnIoInstallation {
    $installation = Get-PawnIoInstallation
    if (-not $installation -or $installation.Version -ne $script:PawnIoVersion) {
        throw "PawnIO $($script:PawnIoVersion) is not installed."
    }
    if ($installation.Driver -ne 'Running') { throw 'PawnIO driver is not Running.' }
    if ($installation.DriverSignature -ne 'Valid') { throw 'PawnIO driver signature is not valid.' }
    if (-not $installation.UninstallString -or $installation.UninstallString.Trim().Length -eq 0) {
        throw 'PawnIO verified uninstall registration is missing.'
    }
    return $installation
}

function Write-ProductionSensorConfig {
    param([Parameter(Mandatory)][string]$Path, [Parameter(Mandatory)][bool]$Enabled)
    $config = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    if ($config.PSObject.Properties.Name -contains 'sensorLibrariesEnabled') {
        if ($config.PSObject.Properties['sensorLibrariesEnabled'].Value -isnot [bool]) {
            throw 'sensorLibrariesEnabled must be a Boolean.'
        }
        $config.sensorLibrariesEnabled = $Enabled
    } else {
        $config | Add-Member -NotePropertyName sensorLibrariesEnabled -NotePropertyValue $Enabled
    }
    $next = "$Path.next"
    try {
        $config | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $next -Encoding utf8
        Move-Item -LiteralPath $next -Destination $Path -Force
    } finally {
        if (Test-Path -LiteralPath $next) { Remove-Item -LiteralPath $next -Force }
    }
}

function Set-ProductionSensorState {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][bool]$Enabled,
        [string]$ConfigPath = 'C:\ProgramData\christopherbell.dev\config\deploy.json',
        [switch]$WhatIf
    )
    Assert-SensorAdministrator
    if ($Enabled) { Assert-NoActiveSensorThreat; Assert-PawnIoInstallation | Out-Null }
    if ($WhatIf) { Write-Output "Would set sensorLibrariesEnabled=$($Enabled.ToString().ToLowerInvariant()) and verify ChristopherBellDev."; return }
    $config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
    $sensorProperty = $config.PSObject.Properties['sensorLibrariesEnabled']
    if (-not $sensorProperty -or $sensorProperty.Value -isnot [bool]) {
        throw 'sensorLibrariesEnabled must be a Boolean.'
    }
    $previous = $sensorProperty.Value
    Write-ProductionSensorConfig -Path $ConfigPath -Enabled $Enabled
    try {
        Restart-Service -Name ChristopherBellDev
        $updated = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
        Test-ProductionEndpoints $updated ([int]$updated.productionPort)
    } catch {
        Write-ProductionSensorConfig -Path $ConfigPath -Enabled $previous
        Restart-Service -Name ChristopherBellDev
        throw
    }
}

function Install-PawnIoProvider {
    [CmdletBinding()]
    param([string]$Root = 'C:\ProgramData\christopherbell.dev', [switch]$WhatIf)
    Assert-SensorAdministrator
    $configPath = Join-Path $Root 'config\deploy.json'
    Set-ProductionSensorState -Enabled $false -ConfigPath $configPath -WhatIf:$WhatIf
    if ($WhatIf) { Write-Output 'Would download, verify, Defender-scan, and install PawnIO 2.2.0 without enabling sensors.'; return }
    $directory = Join-Path $Root 'sensors'
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
    $installer = Join-Path $directory 'PawnIO_setup-2.2.0.exe'
    Invoke-WebRequest -Uri $script:PawnIoUri -OutFile $installer
    Assert-PawnIoInstaller -Path $installer
    Start-MpScan -ScanType CustomScan -ScanPath $installer
    Assert-NoActiveSensorThreat
    $process = Start-Process -FilePath $installer -ArgumentList '/S' -Wait -PassThru
    if ($process.ExitCode -eq 3010) { throw 'PawnIO installation requires a reboot; sensors remain disabled.' }
    if ($process.ExitCode -ne 0) { throw "PawnIO installer exited with code $($process.ExitCode); sensors remain disabled." }
    $installation = Assert-PawnIoInstallation
    Start-MpScan -ScanType CustomScan -ScanPath $directory
    Assert-NoActiveSensorThreat
    return $installation
}

function Get-ProductionSensorStatus {
    [CmdletBinding()]
    param([string]$ConfigPath = 'C:\ProgramData\christopherbell.dev\config\deploy.json')
    $config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
    $sensorProperty = $config.PSObject.Properties['sensorLibrariesEnabled']
    if (-not $sensorProperty -or $sensorProperty.Value -isnot [bool]) {
        throw 'sensorLibrariesEnabled must be a Boolean.'
    }
    $installation = Get-PawnIoInstallation
    $activeThreats = @(Get-MpThreat -ErrorAction Stop | Where-Object {
        $_.IsActive -and [string]$_.ThreatName -match '(?i)(Winring0|PawnIO)'
    })
    [pscustomobject]@{
        Enabled = $sensorProperty.Value
        PawnIoVersion = if ($installation) { $installation.Version } else { 'NotInstalled' }
        Driver = if ($installation) { $installation.Driver } else { 'Missing' }
        DriverPath = if ($installation) { $installation.DriverPath } else { $null }
        DriverSignature = if ($installation) { $installation.DriverSignature } else { 'Missing' }
        UninstallRegistered = $null -ne $installation -and $installation.UninstallString -and $installation.UninstallString.Trim().Length -gt 0
        ActiveThreats = $activeThreats.Count
    }
}

Export-ModuleMember -Function Assert-PawnIoInstaller,Get-PawnIoInstallation,Assert-PawnIoInstallation,Install-PawnIoProvider,Set-ProductionSensorState,Get-ProductionSensorStatus
```

Verification:
- Run the new Pester file; all mocked mutation and failure-path tests must pass.
- Parse the new module with the PowerShell parser; expect zero errors.

#### Code Edit 2.3
- File: `ops/production/windows/prod.ps1`
- Lines: 1-35
- Action: replace

Current:
```powershell
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove')]
    [string]$Command = 'help',
    [switch]$WhatIf,
    [string]$CloudflareTokenPath
)

$ErrorActionPreference = 'Stop'
$moduleRoot = Join-Path $PSScriptRoot 'modules'
Import-Module (Join-Path $moduleRoot 'Production.Common.psm1') -Global -Force
foreach ($module in 'Production.Deploy','Production.Install','Production.Operations','Production.AutoDeploy') {
    Import-Module (Join-Path $moduleRoot "$module.psm1") -Force
}

$handlers = @{
    help = { Show-ProductionHelp }
    install = { Install-ProductionRuntime -WhatIf:$WhatIf -CloudflareTokenPath $CloudflareTokenPath }
    deploy = { Invoke-ProductionDeploy -WhatIf:$WhatIf }
    status = { Get-ProductionStatus }
    logs = { Watch-ProductionLogs }
    restart = { Restart-ProductionService -Verify }
    releases = { Get-ProductionReleases }
    rollback = { Invoke-ProductionRollback -WhatIf:$WhatIf }
    backup = { New-ProductionBackup }
    'verify-startup' = { Test-ProductionStartup }
    uninstall = { Uninstall-ProductionRuntime -WhatIf:$WhatIf }
    'auto-install' = { Install-AutoDeployTask -WhatIf:$WhatIf }
    'auto-deploy' = { Start-AutoDeployLoop }
    'auto-status' = { Get-AutoDeployStatus }
    'auto-remove' = { Remove-AutoDeployTask -WhatIf:$WhatIf }
}

& $handlers[$Command]
```

Proposed:
```powershell
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
    [string]$Command = 'help',
    [switch]$WhatIf,
    [string]$CloudflareTokenPath
)

$ErrorActionPreference = 'Stop'
$moduleRoot = Join-Path $PSScriptRoot 'modules'
Import-Module (Join-Path $moduleRoot 'Production.Common.psm1') -Global -Force
foreach ($module in 'Production.Deploy','Production.Install','Production.Operations','Production.AutoDeploy','Production.Sensors') {
    Import-Module (Join-Path $moduleRoot "$module.psm1") -Force
}

$handlers = @{
    help = { Show-ProductionHelp }
    install = { Install-ProductionRuntime -WhatIf:$WhatIf -CloudflareTokenPath $CloudflareTokenPath }
    deploy = { Invoke-ProductionDeploy -WhatIf:$WhatIf }
    status = { Get-ProductionStatus }
    logs = { Watch-ProductionLogs }
    restart = { Restart-ProductionService -Verify }
    releases = { Get-ProductionReleases }
    rollback = { Invoke-ProductionRollback -WhatIf:$WhatIf }
    backup = { New-ProductionBackup }
    'verify-startup' = { Test-ProductionStartup }
    uninstall = { Uninstall-ProductionRuntime -WhatIf:$WhatIf }
    'auto-install' = { Install-AutoDeployTask -WhatIf:$WhatIf }
    'auto-deploy' = { Start-AutoDeployLoop }
    'auto-status' = { Get-AutoDeployStatus }
    'auto-remove' = { Remove-AutoDeployTask -WhatIf:$WhatIf }
    'sensor-install' = { Install-PawnIoProvider -WhatIf:$WhatIf }
    'sensor-status' = { Get-ProductionSensorStatus }
    'sensor-enable' = { Set-ProductionSensorState -Enabled $true -WhatIf:$WhatIf }
    'sensor-disable' = { Set-ProductionSensorState -Enabled $false -WhatIf:$WhatIf }
}

& $handlers[$Command]
```

Verification:
- Extend `Production.Command.Tests.ps1` lines 29-38 so it imports `Production.Sensors` and expects the four exported sensor commands.
- Run all operations Pester tests; command help must list `sensor-install`, `sensor-status`, `sensor-enable`, and `sensor-disable`.
- Run `prod.cmd sensor-install -WhatIf` and `prod.cmd sensor-disable -WhatIf`; neither may download, restart, or mutate.
- Commit Task 2 with `git commit -m "Guard PawnIO sensor lifecycle operations"`.

### Task 3 - Replace the legacy dependency with pinned LibreHardwareMonitor 0.9.6 resources

Sequence / dependencies:
- Runs after Task 2; application packaging is changed while the production switch remains false.

Implementation notes:
- Remove both obsolete wrapper dependencies; command-center production code no longer calls either Java wrapper.
- Download only the official standard release archive, verify it before extraction, extract only the seven fixed runtime files below, and verify each extracted hash.
- Generated files belong under `website/build`; do not commit binary DLLs.
- `processResources` depends on preparation, and `check` verifies the boot JAR has the new resources and no legacy dependency or WinRing name.

#### Code Edit 3.1
- File: `website/build.gradle.kts`
- Lines: 1-3
- Action: replace

Current:
```kotlin
import org.gradle.api.GradleException
import org.gradle.language.base.plugins.LifecycleBasePlugin
```

Proposed:
```kotlin
import java.net.URI
import java.nio.file.Files
import java.nio.file.StandardCopyOption
import java.security.MessageDigest
import java.util.HexFormat
import java.util.zip.ZipFile
import org.gradle.api.GradleException
import org.gradle.language.base.plugins.LifecycleBasePlugin
import org.gradle.language.jvm.tasks.ProcessResources
```

Verification:
- Run `./gradlew :website:compileJava`; the Kotlin DSL must compile with the new standard-library imports.

#### Code Edit 3.2
- File: `website/build.gradle.kts`
- Lines: 31-35
- Action: replace

Current:
```kotlin
    // Host metrics and Windows hardware sensors
    implementation("com.github.oshi:oshi-core:7.4.0")
    implementation("io.github.pandalxb:jLibreHardwareMonitor:1.0.6")
    implementation("io.github.pandalxb:jPowerShell:1.0.1")
```

Proposed:
```kotlin

    // Host metrics; Windows sensor binaries are pinned generated resources below.
    implementation("com.github.oshi:oshi-core:7.4.0")
```

Verification:
- Run `./gradlew :website:dependencies --configuration runtimeClasspath` before the edit and record the old wrapper as RED evidence.
- After the edit, the dependency report must contain neither `jLibreHardwareMonitor` nor `jPowerShell`.

#### Code Edit 3.3
- File: `website/build.gradle.kts`
- Lines: after 67
- Action: add

Proposed:
```kotlin
val libreHardwareMonitorUri = URI(
    "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.6/LibreHardwareMonitor.zip")
val libreHardwareMonitorArchiveSha256 =
    "086d9f1b5a99e643edc2cfaaac16051685b551e4c5ac0b32a57c58c0e529c001"
val libreHardwareMonitorFiles = linkedMapOf(
    "LibreHardwareMonitorLib.dll" to "6ebc194316536ba61af5be24508ad9fcbb2ecc685e716c12e787c79530f66bf0",
    "HidSharp.dll" to "d86690efde30ea9179f669320f39148853793b743a98b531afeaf30598e22f54",
    "BlackSharp.Core.dll" to "cafb93afcc8d8a367e21f619673d05c06887d8964867fed1371f02ded1cd3e23",
    "DiskInfoToolkit.dll" to "1acbf51b3c10c51c986cf43021680d34a2e38d9a5ba652bcfa9a1b5f7fc09800",
    "RAMSPDToolkit-NDD.dll" to "b6882354c7c8ec186617e421507743dbfae09c5c1fc24cef76a1d0c0c26651de",
    "System.Memory.dll" to "d5e8e4866f9cfa66f7765660f84b210198893e55335487afe5ebda342c0e913d",
    "System.Runtime.CompilerServices.Unsafe.dll" to "08cbd7278b66f1e68425a82d4b97181a4130d93e3dd91831407aba7212ccdacf")

fun sha256(path: java.nio.file.Path): String = Files.newInputStream(path).use { input ->
    val digest = MessageDigest.getInstance("SHA-256")
    val buffer = ByteArray(8192)
    while (true) {
        val count = input.read(buffer)
        if (count < 0) break
        digest.update(buffer, 0, count)
    }
    HexFormat.of().formatHex(digest.digest())
}

val sensorResourceDirectory = layout.buildDirectory.dir("generated/sensor-resources")
val prepareSensorResources by tasks.registering {
    val archive = layout.buildDirectory.file("sensor-downloads/LibreHardwareMonitor-0.9.6.zip")
    outputs.dir(sensorResourceDirectory)
    doLast {
        val archivePath = archive.get().asFile.toPath()
        Files.createDirectories(archivePath.parent)
        libreHardwareMonitorUri.toURL().openStream().use { input ->
            Files.copy(input, archivePath, StandardCopyOption.REPLACE_EXISTING)
        }
        if (sha256(archivePath) != libreHardwareMonitorArchiveSha256) {
            Files.deleteIfExists(archivePath)
            throw GradleException("LibreHardwareMonitor archive SHA-256 verification failed.")
        }
        val output = sensorResourceDirectory.get().dir("lib").asFile.toPath()
        Files.createDirectories(output)
        ZipFile(archivePath.toFile()).use { zip ->
            libreHardwareMonitorFiles.forEach { (name, expected) ->
                val entry = zip.getEntry(name)
                    ?: throw GradleException("LibreHardwareMonitor release is missing $name.")
                val target = output.resolve(name)
                zip.getInputStream(entry).use { input ->
                    Files.copy(input, target, StandardCopyOption.REPLACE_EXISTING)
                }
                if (sha256(target) != expected) {
                    Files.deleteIfExists(target)
                    throw GradleException("LibreHardwareMonitor resource SHA-256 verification failed: $name")
                }
            }
        }
    }
}

sourceSets.named("main") { resources.srcDir(sensorResourceDirectory) }
tasks.named<ProcessResources>("processResources") { dependsOn(prepareSensorResources) }
```

Verification:
- Run `./gradlew :website:processResources --rerun-tasks`; expect one verified archive and exactly seven generated DLLs.
- Change a copied hash in the working tree, run the task, and record the expected checksum failure as RED security evidence; restore the correct hash immediately.

#### Code Edit 3.4
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: 22-79
- Action: replace

Current:
```java
  @Test
  void refusesPreexistingVersionDirectoryWithoutLoadingItsFiles() throws Exception {
    Path existing = Files.createDirectories(tempDir.resolve("jlibre-1.0.6-fixed"));
    Files.writeString(existing.resolve("LibreHardwareMonitorLib.dll"), "malicious", UTF_8);
    var provisioner = provisioner("trusted", hash("trusted"), path -> {}, "fixed");
    assertThatThrownBy(provisioner::provision).isInstanceOf(SecurityException.class);
  }

  private SecureNativeLibraryProvisioner provisionerWithLibraryAndScript(
      SecureNativeLibraryProvisioner.AclPolicy acl,
      String nonce) {
    return new SecureNativeLibraryProvisioner(
        tempDir,
        List.of(
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "LibreHardwareMonitorLib.dll", hash("trusted"),
                () -> new ByteArrayInputStream("trusted".getBytes(UTF_8))),
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "cpu-temperature.ps1", hash("trusted-script"),
                () -> new ByteArrayInputStream("trusted-script".getBytes(UTF_8)))),
        acl,
        () -> nonce);
  }
```

Proposed:
```java
  @Test
  void refusesPreexistingVersionDirectoryWithoutLoadingItsFiles() throws Exception {
    Path existing = Files.createDirectories(tempDir.resolve("librehardwaremonitor-0.9.6-fixed"));
    Files.writeString(existing.resolve("LibreHardwareMonitorLib.dll"), "malicious", UTF_8);
    var provisioner = provisioner("trusted", hash("trusted"), path -> {}, "fixed");
    assertThatThrownBy(provisioner::provision).isInstanceOf(SecurityException.class);
    assertThat(Files.readString(existing.resolve("LibreHardwareMonitorLib.dll"), UTF_8))
        .isEqualTo("malicious");
  }

  @Test
  void checksumMismatchFailsClosedAndRemovesCreatedVersionDirectory() {
    var provisioner = provisioner("tampered", hash("trusted"), path -> {}, "mismatch");
    assertThatThrownBy(provisioner::provision).isInstanceOf(SecurityException.class);
    assertThat(tempDir.resolve("librehardwaremonitor-0.9.6-mismatch")).doesNotExist();
  }

  @Test
  void verifiedExtractionReturnsPrimaryLibraryCompanionAndScriptThenCleansUp() throws Exception {
    var provisioner = provisionerWithLibraryCompanionAndScript(path -> {}, "verified");
    var libraries = provisioner.provision();
    assertThat(Files.readString(libraries.libreHardwareMonitor(), UTF_8)).isEqualTo("trusted");
    assertThat(Files.readString(libraries.directory().resolve("HidSharp.dll"), UTF_8))
        .isEqualTo("trusted-hid");
    assertThat(Files.readString(libraries.cpuTemperatureScript(), UTF_8))
        .isEqualTo("trusted-script");
    Path directory = libraries.directory();
    libraries.close();
    assertThat(directory).doesNotExist();
  }

  private SecureNativeLibraryProvisioner provisionerWithLibraryCompanionAndScript(
      SecureNativeLibraryProvisioner.AclPolicy acl, String nonce) {
    return new SecureNativeLibraryProvisioner(
        tempDir,
        List.of(
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "LibreHardwareMonitorLib.dll", hash("trusted"),
                () -> new ByteArrayInputStream("trusted".getBytes(UTF_8))),
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "HidSharp.dll", hash("trusted-hid"),
                () -> new ByteArrayInputStream("trusted-hid".getBytes(UTF_8))),
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "cpu-temperature.ps1", hash("trusted-script"),
                () -> new ByteArrayInputStream("trusted-script".getBytes(UTF_8)))),
        acl,
        () -> nonce);
  }
```

Verification:
- Run `./gradlew :website:test --tests '*SecureNativeLibraryProvisionerTest'`.
- Expected RED before production edits: old `jlibre-1.0.6-*` directory names and no companion assertion.

#### Code Edit 3.5
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 25-38
- Action: replace

Current:
```java
/** Extracts checksum-pinned native libraries only into an ACL-restricted fresh directory. */
final class SecureNativeLibraryProvisioner {
  static final String VERSION = "1.0.6";
  private final Path baseDirectory;
  private final List<ResourceSpec> resources;
  private final AclPolicy aclPolicy;
  private final Supplier<String> nonceSupplier;

  SecureNativeLibraryProvisioner(Path baseDirectory) {
    this(baseDirectory, List.of(
        resource("HidSharp.dll", "8c58e5fba22acc751032dfe97ce633e4f8a4c96089749bf316d55283b36649c2"),
        resource("LibreHardwareMonitorLib.dll", "a0f2728f1734c236a9d02d9e25a88bc4f8cb7bd1faff1770726beb7af06bf8dc"),
        resource("cpu-temperature.ps1", "4d47eccfc836fe4d4ea771bf36b1b4fa4a4b91490b3f2ed8ab5e9c475687b2f3")),
        new WindowsAclPolicy(), () -> UUID.randomUUID().toString());
  }
```

Proposed:
```java
/** Extracts checksum-pinned native libraries only into an ACL-restricted fresh directory. */
final class SecureNativeLibraryProvisioner {
  static final String VERSION = "0.9.6";
  private final Path baseDirectory;
  private final List<ResourceSpec> resources;
  private final AclPolicy aclPolicy;
  private final Supplier<String> nonceSupplier;

  SecureNativeLibraryProvisioner(Path baseDirectory) {
    this(baseDirectory, List.of(
        resource("LibreHardwareMonitorLib.dll", "6ebc194316536ba61af5be24508ad9fcbb2ecc685e716c12e787c79530f66bf0"),
        resource("HidSharp.dll", "d86690efde30ea9179f669320f39148853793b743a98b531afeaf30598e22f54"),
        resource("BlackSharp.Core.dll", "cafb93afcc8d8a367e21f619673d05c06887d8964867fed1371f02ded1cd3e23"),
        resource("DiskInfoToolkit.dll", "1acbf51b3c10c51c986cf43021680d34a2e38d9a5ba652bcfa9a1b5f7fc09800"),
        resource("RAMSPDToolkit-NDD.dll", "b6882354c7c8ec186617e421507743dbfae09c5c1fc24cef76a1d0c0c26651de"),
        resource("System.Memory.dll", "d5e8e4866f9cfa66f7765660f84b210198893e55335487afe5ebda342c0e913d"),
        resource("System.Runtime.CompilerServices.Unsafe.dll", "08cbd7278b66f1e68425a82d4b97181a4130d93e3dd91831407aba7212ccdacf"),
        resource("cpu-temperature.ps1", "34a0b773cf975a28039df2e265014ec024e103fe48d1b6ca54dd1eff96fa14fe")),
        new WindowsAclPolicy(), () -> UUID.randomUUID().toString());
  }
```

Verification:
- After Task 4 writes the exact LF UTF-8 script content, run `Get-FileHash` and require SHA-256 `34A0B773CF975A28039DF2E265014EC024E103FE48D1B6CA54DD1EFF96FA14FE`.

#### Code Edit 3.6
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 57-57
- Action: replace

Current:
```java
    Path versionDirectory = baseDirectory.resolve("jlibre-" + VERSION + "-" + nonce);
```

Proposed:
```java
    Path versionDirectory = baseDirectory.resolve(
        "librehardwaremonitor-" + VERSION + "-" + nonce);
```

Verification:
- Run the provisioner tests and build.
- Run `rg -n "jlibre|1\.0\.6|a0f2728f|WinRing" website/src website/build.gradle.kts`; expect no production match.

#### Code Edit 3.7
- File: `website/build.gradle.kts`
- Lines: after 96
- Action: add

Proposed:
```kotlin
val verifySensorRuntime by tasks.registering {
    dependsOn(tasks.named("bootJar"))
    doLast {
        val jar = tasks.named<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar")
            .get().archiveFile.get().asFile
        ZipFile(jar).use { zip ->
            val names = zip.entries().asSequence().map { it.name }.toList()
            if (names.any { it.contains("jLibreHardwareMonitor", ignoreCase = true) ||
                    it.contains("WinRing", ignoreCase = true) }) {
                throw GradleException("Legacy WinRing0 sensor runtime is present in the boot JAR.")
            }
            libreHardwareMonitorFiles.keys.forEach { name ->
                if ("BOOT-INF/classes/lib/$name" !in names) {
                    throw GradleException("Pinned sensor runtime is missing from the boot JAR: $name")
                }
            }
        }
    }
}
tasks.named("check") { dependsOn(verifySensorRuntime) }
```

Verification:
- Run `./gradlew :website:verifySensorRuntime`; expect PASS only with all pinned files and no legacy names.
- Inspect `jar tf website/build/libs/website.jar` and the runtime dependency report.
- Commit Task 3 with `git commit -m "Pin LibreHardwareMonitor PawnIO runtime"` after Task 4 replaces the script-hash marker.

### Task 4 - Fail the bounded probe closed when PawnIO is absent and validate the CPU-only path

Sequence / dependencies:
- Runs after Task 3 resource generation is present; completes the application-side provider replacement before the Task 3 commit.

Implementation notes:
- The script checks the exact uninstall registry version before loading any DLL.
- The assembly resolver searches only the ACL-restricted provisioned directory and only a simple assembly filename.
- CPU remains the only enabled hardware class.
- The Java probe contract and fixed arguments remain unchanged; exit code 3 is a concise unavailable result.

#### Code Edit 4.1
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbeTest.java`
- Lines: 38-45
- Action: replace

Current:
```java
  @Test
  void rejectsEmptyZeroMalformedOversizedAndNonZeroExitResults() {
    assertThat(read(FakeManagedProcess.completed("", "", 0))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("0", "", 0))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("NaN", "", 0))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("64", "failure", 1))).isEmpty();
    assertThat(read(FakeManagedProcess.truncated("64"))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("126", "", 0))).isEmpty();
  }
```

Proposed:
```java
  @Test
  void rejectsEmptyZeroMalformedOversizedProviderUnavailableAndNonZeroResults() {
    assertThat(read(FakeManagedProcess.completed("", "", 0))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("0", "", 0))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("NaN", "", 0))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("", "PawnIO 2.2.0 is unavailable.", 3))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("64", "failure", 1))).isEmpty();
    assertThat(read(FakeManagedProcess.truncated("64"))).isEmpty();
    assertThat(read(FakeManagedProcess.completed("126", "", 0))).isEmpty();
  }
```

Verification:
- Run the focused probe test; it must pass without changing the Java command surface.

#### Code Edit 4.2
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClientTest.java`
- Lines: after 94
- Action: add

Proposed:
```java
  @Test
  void providerUnavailableUsesFiveMinuteFailureBackoff() {
    var clock = new MutableClock();
    var executor = new ManualExecutorService();
    var probe = new FakeProbe(OptionalDouble.empty());
    var client = client(probe, executor, clock);

    client.readCelsius();
    executor.runNext();
    clock.advance(Duration.ofMinutes(4).plusSeconds(59));
    assertThat(client.readCelsius()).isEmpty();
    assertThat(executor.pending()).isZero();

    clock.advance(Duration.ofSeconds(1));
    assertThat(client.readCelsius()).isEmpty();
    assertThat(executor.pending()).isEqualTo(1);
    assertThat(probe.readCalls()).isEqualTo(1);
  }
```

Verification:
- Expected RED: the current client schedules the second probe after 30 seconds instead of five minutes.

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClient.java`
- Lines: before 21
- Action: add

Proposed:
```java
  private static final Duration FAILURE_RETRY_INTERVAL = Duration.ofMinutes(5);
```

Verification:
- Compile the focused client test; the constant supplies the fixed quiet-degradation interval.

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClient.java`
- Lines: 76-86
- Action: replace

Current:
```java
  private void refresh() {
    try {
      var value = probe.readCelsius();
      if (value.isPresent()) lastGood.set(new CachedTemperature(value, clock.instant()));
    } catch (RuntimeException ignored) {
      // The provider preserves the prior good value and explicit unavailable semantics.
    } finally {
      nextRefresh = clock.instant().plus(refreshInterval);
      refreshInFlight.set(false);
    }
  }
```

Proposed:
```java
  private void refresh() {
    Duration nextDelay = refreshInterval;
    try {
      var value = probe.readCelsius();
      if (value.isPresent()) {
        lastGood.set(new CachedTemperature(value, clock.instant()));
      } else {
        nextDelay = FAILURE_RETRY_INTERVAL;
      }
    } catch (RuntimeException ignored) {
      nextDelay = FAILURE_RETRY_INTERVAL;
      // The provider preserves the prior good value and explicit unavailable semantics.
    } finally {
      nextRefresh = clock.instant().plus(nextDelay);
      refreshInFlight.set(false);
    }
  }
```

Verification:
- Run `LibreHardwareCpuTemperatureClientTest`; success remains 30 seconds, failure retries after five minutes, and last-good expiry remains two refresh intervals.

#### Code Edit 4.5
- File: `website/src/main/resources/lib/cpu-temperature.ps1`
- Lines: 1-44
- Action: replace

Current:
```powershell
param(
  [Parameter(Mandatory = $true)]
  [string]$LibreHardwareMonitorPath
)

$computer = $null
try {
  Add-Type -Path $LibreHardwareMonitorPath
  $computer = [LibreHardwareMonitor.Hardware.Computer]::new()
  $computer.IsCpuEnabled = $true
  $computer.Open()
  $values = @()
  foreach ($hardware in $computer.Hardware) {
    if ($hardware.HardwareType -eq [LibreHardwareMonitor.Hardware.HardwareType]::Cpu) {
      $hardware.Update()
      $values += $hardware.Sensors |
          Where-Object {
            $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature -and
            $null -ne $_.Value -and
            [double]$_.Value -gt 0
          } |
          ForEach-Object { [double]$_.Value }
      foreach ($subHardware in $hardware.SubHardware) {
        $subHardware.Update()
        $values += $subHardware.Sensors |
            Where-Object {
              $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature -and
              $null -ne $_.Value -and
              [double]$_.Value -gt 0
            } |
            ForEach-Object { [double]$_.Value }
      }
    }
  }
  if ($values.Count -gt 0) {
    [Console]::Write(($values | Measure-Object -Maximum).Maximum.ToString(
        [Globalization.CultureInfo]::InvariantCulture))
  }
} finally {
  if ($null -ne $computer) { $computer.Close() }
}
```

Proposed:
```powershell
param(
  [Parameter(Mandatory = $true)]
  [string]$LibreHardwareMonitorPath
)

$pawnIo = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO' -ErrorAction SilentlyContinue
if (-not $pawnIo -or [string]$pawnIo.DisplayVersion -ne '2.2.0') {
  [Console]::Error.Write('PawnIO 2.2.0 is unavailable.')
  exit 3
}

$computer = $null
try {
  Add-Type -Path $LibreHardwareMonitorPath
  $computer = [LibreHardwareMonitor.Hardware.Computer]::new()
  $computer.IsCpuEnabled = $true
  $computer.Open()
  $values = @()
  foreach ($hardware in $computer.Hardware) {
    if ($hardware.HardwareType -eq [LibreHardwareMonitor.Hardware.HardwareType]::Cpu) {
      $hardware.Update()
      $values += $hardware.Sensors |
          Where-Object {
            $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature -and
            $null -ne $_.Value -and [double]$_.Value -gt 0
          } | ForEach-Object { [double]$_.Value }
      foreach ($subHardware in $hardware.SubHardware) {
        $subHardware.Update()
        $values += $subHardware.Sensors |
            Where-Object {
              $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature -and
              $null -ne $_.Value -and [double]$_.Value -gt 0
            } | ForEach-Object { [double]$_.Value }
      }
    }
  }
  if ($values.Count -gt 0) {
    [Console]::Write(($values | Measure-Object -Maximum).Maximum.ToString(
        [Globalization.CultureInfo]::InvariantCulture))
  }
} finally {
  if ($null -ne $computer) { $computer.Close() }
}
```

Verification:
- Parse the script; expect zero errors.
- Before PawnIO installation, invoke the provisioned fixed script from an elevated harness and expect exit 3, no stdout, bounded stderr, and no child process remaining.
- Calculate the LF UTF-8 SHA-256 with `Get-FileHash` and require `34A0B773CF975A28039DF2E265014EC024E103FE48D1B6CA54DD1EFF96FA14FE`.
- After installation, run the same fixed script and require one finite value `> 0` and `<= 125`.
- If Defender or AMSI blocks parsing or execution, record the detection, leave sensors disabled, and stop; do not bypass or exclude the script.

#### Code Edit 4.6
- File: `website/src/main/java/dev/christopherbell/admin/README.md`
- Lines: 30-36
- Action: replace

Current:
```markdown
- Host providers run concurrently behind independent timeouts on a private scheduler. CPU
  temperature returns a non-blocking cache and refreshes every 30 seconds through a bounded,
  one-shot Windows PowerShell process whose full process tree is terminated on timeout.
- The bundled sensor DLLs and CPU-temperature script are checksum-pinned and extracted with
  create-new semantics into a fresh, service-owned directory whose ACL permits only SYSTEM and
  Administrators.
  Sensor collection fails closed if extraction, checksum verification, or ACL hardening fails.
```

Proposed:
```markdown
- Host providers run concurrently behind independent timeouts on a private scheduler. CPU
  temperature returns a non-blocking cache and refreshes every 30 seconds through a bounded,
  one-shot Windows PowerShell process whose full process tree is terminated on timeout.
- CPU temperature requires locally installed PawnIO 2.2.0 and the pinned official
  LibreHardwareMonitor 0.9.6 runtime. The runtime DLLs and script are checksum-pinned and
  extracted with create-new semantics into a fresh, SYSTEM-owned directory whose ACL permits
  only SYSTEM and Administrators. Missing PawnIO, extraction, checksum, ACL, or probe failures
  fail closed to explicit unavailable state without blocking other telemetry.
```

Verification:
- Search command-center documentation for `jLibre`, `WinRing`, or claims that the old wrapper remains.
- Run all focused command-center tests and the complete build.
- Commit Tasks 3-4 together using `git commit -m "Replace WinRing0 sensor runtime"`.

### Task 5 - Complete staged installation, runtime proof, publication, deployment, and enablement

Sequence / dependencies:
- Runs only after Tasks 1-4 are committed and every automated check is green.

Implementation notes:
- This task deliberately separates install, candidate enablement, initial production deployment, and production enablement.
- A failure at any stage retains or restores false and stops before the next stage.
- Do not reboot on exit 3010; report the pending requirement and leave the website healthy.

#### Code Edit 5.1
- File: `docs/operations/windows-production.md`
- Lines: after 122
- Action: add

Proposed:
```markdown
CPU Temperature Provider
------------------------

CPU temperature is disabled by default in protected `deploy.json`. The website remains healthy
and reports the metric unavailable when PawnIO is absent or disabled. Provider lifecycle commands
are local elevated operations only:

    .\prod.cmd sensor-status
    .\prod.cmd sensor-install -WhatIf
    .\prod.cmd sensor-install
    .\prod.cmd sensor-enable -WhatIf
    .\prod.cmd sensor-enable
    .\prod.cmd sensor-disable

`sensor-install` downloads only the pinned official PawnIO 2.2.0 installer, verifies its SHA-256
and publisher thumbprint, scans it with Microsoft Defender, installs it silently, verifies the
registered version and running driver, scans again, and leaves sensors disabled. Exit code 3010
means a reboot is required; stop and obtain explicit reboot approval.

Never add a Defender exclusion. Enable only after the elevated direct probe and a non-production
port candidate return a plausible CPU Celsius value for three refresh windows with stable process
counts and no active Defender detection. On any problem, run `sensor-disable` first. If the driver
must be removed, use the verified PawnIO entry in Windows Installed Apps, then verify registry,
driver, Defender, and website state; never delete driver files manually.
```

Verification:
- Extend `Production.Command.Tests.ps1` to assert the runbook contains all four commands, exit 3010 behavior, Defender prohibition, and disable-first rollback.
- Run all Pester tests.

#### Code Edit 5.2
- File: `ops/production/windows/modules/Production.Common.psm1`
- Lines: 162-170
- Action: replace

Current:
```powershell
function Show-ProductionHelp {
    @'
Usage: prod.cmd <command> [-WhatIf]

Commands: install, deploy, status, logs, restart, releases, rollback, backup,
          verify-startup, uninstall, auto-install, auto-deploy, auto-status,
          auto-remove
'@ | Write-Output
}
```

Proposed:
```powershell
function Show-ProductionHelp {
    @'
Usage: prod.cmd <command> [-WhatIf]

Commands: install, deploy, status, logs, restart, releases, rollback, backup,
          verify-startup, uninstall, auto-install, auto-deploy, auto-status,
          auto-remove, sensor-install, sensor-status, sensor-enable,
          sensor-disable
'@ | Write-Output
}
```

Verification:
- Run `prod.cmd help`; expect all four sensor commands and exit 0.

#### Code Edit 5.3
- File: `ops/production/windows/modules/Production.Operations.psm1`
- Lines: 138-155
- Action: replace

Current:
```powershell
function Test-ProductionStartup {
    $config = Read-ProductionConfig
    foreach ($name in 'MongoDB','ChristopherBellDev','cloudflared') {
        $service = Get-Service $name -ErrorAction Stop
        if ([string]$service.Status -ne 'Running') { throw "$name must be Running." }
        if ([string]$service.StartType -ne 'Automatic') { throw "$name must use Automatic startup." }
    }
    $task = Get-ScheduledTask -TaskName 'ChristopherBellAutoDeploy' -ErrorAction Stop
    Assert-AutoDeployTaskContract -Task $task -Config $config
    Test-ProductionEndpoints $config $config.productionPort
    Wait-HttpStatus -Uri $config.publicUrl -ExpectedStatus 200 -Timeout ([timespan]::FromSeconds(30)) | Out-Null
    [pscustomobject]@{
        Services = 'RunningAutomatic'
        AutoDeployTask = $task.State
        NativeEndpoint = 200
        PublicEndpoint = 200
    }
}
```

Proposed:
```powershell
function Test-ProductionStartup {
    $config = Read-ProductionConfig
    foreach ($name in 'MongoDB','ChristopherBellDev','cloudflared') {
        $service = Get-Service $name -ErrorAction Stop
        if ([string]$service.Status -ne 'Running') { throw "$name must be Running." }
        if ([string]$service.StartType -ne 'Automatic') { throw "$name must use Automatic startup." }
    }
    if ($config.PSObject.Properties.Name -notcontains 'sensorLibrariesEnabled') {
        throw 'deploy.json must declare sensorLibrariesEnabled.'
    }
    $task = Get-ScheduledTask -TaskName 'ChristopherBellAutoDeploy' -ErrorAction Stop
    Assert-AutoDeployTaskContract -Task $task -Config $config
    Test-ProductionEndpoints $config $config.productionPort
    Wait-HttpStatus -Uri $config.publicUrl -ExpectedStatus 200 -Timeout ([timespan]::FromSeconds(30)) | Out-Null
    [pscustomobject]@{
        Services = 'RunningAutomatic'
        AutoDeployTask = $task.State
        NativeEndpoint = 200
        PublicEndpoint = 200
        SensorLibrariesEnabled = [bool]$config.sensorLibrariesEnabled
    }
}
```

Verification:
- Add a focused operations test that rejects missing state and returns false before enablement/true after enablement.
- Run all Pester tests and `prod.cmd verify-startup` after installed tooling is refreshed.

- [ ] **Step 1: Run complete automated verification**

Run:
```powershell
$env:GRADLE_USER_HOME = "$PWD\.gradle-user-home-pawnio"
.\gradlew.bat --no-daemon :website:test :website:jsTest :website:verifySensorRuntime :website:build --rerun-tasks
pwsh -NoLogo -NoProfile -Command "Invoke-Pester ops/production/windows/tests -Output Detailed"
git diff --check
```

Expected: all Java suites, all 116-or-more JavaScript tests, all Pester tests, sensor packaging verification, and the full build pass; no diff whitespace errors.

- [ ] **Step 2: Run a security-focused diff review**

Check fixed URLs/arguments, config mutation, signature/hash checks, Defender checks, process execution, ACL behavior, script assembly resolution, and rollback. Run:
```powershell
rg -n "jLibre|WinRing|Runtime\.exec|cmd\.exe|ProcessBuilder|Start-Process|Invoke-WebRequest|COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED" website ops
.\gradlew.bat :website:dependencies --configuration runtimeClasspath
jar tf website\build\libs\website.jar | rg -i "jlibre|winring|LibreHardwareMonitor|HidSharp|PawnIO"
```

Expected: no legacy dependency or WinRing artifact; only the reviewed fixed process/download paths.

- [ ] **Step 3: Install PawnIO without enabling sensors**

From refreshed protected tooling in elevated PowerShell:
```powershell
.\prod.cmd install
.\prod.cmd sensor-status
.\prod.cmd sensor-install -WhatIf
.\prod.cmd sensor-install
.\prod.cmd sensor-status
```

Expected: pre-status disabled/not installed/no active threat; install verifies fixed artifact, performs two Defender scans, returns exit 0, reports version 2.2.0 and Running driver, and post-status remains `Enabled=False`. Exit 3010 stops the plan before reboot.

- [ ] **Step 4: Prove the direct elevated probe and candidate app**

Record the installed driver path/signature and verified uninstall registration. Run the fixed provisioned script once from a non-elevated token and require that it cannot obtain a positive privileged CPU value, then run it under elevation and require one plausible value. Launch the candidate JAR on port 8090 with isolated MongoDB and `--command-center.sensor-libraries-enabled=true`. Observe at least 90 seconds. Record three or more positive Celsius samples, zero-growing Java-descendant PowerShell count, no port 8080 change, no active Defender threat, candidate HTTP 200/body marker, admin API 403 anonymously, and authenticated command-center CPU temperature in the browser.

- [ ] **Step 5: Commit, push, PR, and CI**

Commit documentation/verification changes with `git commit -m "Document PawnIO sensor recovery"`, push `codex/pawnio-cpu-temperature`, open a PR referencing the Defender incident and approved spec, wait for every Java 25 matrix and CodeQL gate, address only trusted `azurras` guidance, and merge by squash after green review.

- [ ] **Step 6: Deploy safely while still disabled**

Confirm the native auto-deployer selects the exact merge SHA. Refresh protected tooling with `prod.cmd install`, run `prod.cmd sensor-disable`, `prod.cmd verify-startup`, and `prod.cmd sensor-status`. Require Running/Automatic services, port 8080 ownership by the current Java process, HTTP 200 with 3912-or-current response bytes and `<title>CB | Home</title>`, no active threat, and `Enabled=False`.

- [ ] **Step 7: Enable production separately and observe**

Run `prod.cmd sensor-enable -WhatIf`, review the fixed action, then run `prod.cmd sensor-enable`. Observe at least 90 seconds and record three positive Celsius samples, stable process counts, one port-8080 owner, stable service PID unless intentionally restarted, no restart-loop events, no active Defender threat, authenticated browser CPU temperature, and human-readable uptime.

- [ ] **Step 8: Roll back immediately on any failed gate**

Run `prod.cmd sensor-disable`, verify HTTP 200/body marker, and keep PawnIO installed but unused while investigating. If the driver itself is implicated, use its verified Windows Installed Apps uninstall entry only after recording path/signature, stop before any requested reboot, and re-verify registry, driver, Defender, services, ports, processes, and endpoints.

Verification:
- All steps produce evidence for the Builder test report; no enablement may be inferred from install success alone.
- Commit Task 5 with `git commit -m "Document PawnIO sensor operations"` before publication if documentation was not included earlier.

## Code Changes

- `ops/production/windows/config/deploy.example.json`: add false-by-default protected sensor state.
- `ops/production/windows/service/Start-ChristopherBellDev.ps1`: map only the protected typed state to the Spring environment switch.
- `ops/production/windows/modules/Production.Sensors.psm1`: add fixed local elevated PawnIO verification/install/status/enable/disable operations.
- `ops/production/windows/prod.ps1` and `Production.Common.psm1`: expose and document four local commands.
- `Production.Operations.psm1`: include sensor state in startup verification.
- Pester tests: cover default preservation, signature/hash rejection, Defender gates, exit 3010, install-without-enable, rollback, status, command surface, and docs.
- `website/build.gradle.kts`: remove obsolete wrappers; download, verify, extract, package, and inspect official 0.9.6 resources.
- `SecureNativeLibraryProvisioner.java` and tests: pin 0.9.6 files and use a non-jLibre version directory.
- `cpu-temperature.ps1` and probe tests: require PawnIO 2.2.0, resolve only from the protected directory, and preserve CPU-only bounded sampling.
- Admin and production runbooks: document provider, failure, enablement, and rollback contracts.

## Files and Modules

- Production configuration/service: `ops/production/windows/config`, `service`, `modules`, `prod.ps1`.
- Operations tests: `ops/production/windows/tests`.
- Application packaging: `website/build.gradle.kts` and generated `website/build/generated/sensor-resources`.
- Sensor runtime: command-center metrics package and `website/src/main/resources/lib/cpu-temperature.ps1`.
- Documentation: admin README and native Windows operations runbook.
- Builder artifacts: updated work record, new test report, spoke update/review, closure, and session memory.

## Unit Testing

- Pester RED/GREEN for all local lifecycle state and failure paths.
- Java RED/GREEN for provisioner directory/resource behavior and provider-unavailable exit.
- Existing client cache, last-good expiration, timeout process-tree termination, output bounds, fixed arguments, ACL, and script-checksum tests remain green.
- Gradle verification rejects invalid archive/resource hashes, missing replacement resources, legacy dependencies, and legacy JAR entries.
- Full commands are specified in Task 5 Step 1.

## Local Testing

- Production remains on port 8080 with sensors disabled during all builds and candidate work.
- Direct elevated fixed-script test precedes candidate app enablement.
- A non-elevated fixed-script negative test proves PawnIO is not usable by an ordinary token before the elevated positive test.
- Candidate uses port 8090, isolated MongoDB, `SIMULATED` actions, controlled log, and sensors enabled.
- Browser verifies admin gating, actual CPU temperature, human uptime, and no layout regression.
- Candidate observation lasts at least three 30-second refresh windows.
- Candidate PID, process tree, port, database, and temporary files are cleaned after verification.

## Validation

- No active Defender finding and no WinRing0 artifact remain.
- PawnIO installer and installed identity match reviewed version/hash/signature/driver requirements.
- Installation never enables sensors; enablement is a separate guarded operation.
- CPU temperature is plausible and positive under SYSTEM or the feature remains explicitly unavailable/disabled.
- No PowerShell/Java process accumulation, port conflict, or service restart loop occurs.
- Production HTTP body evidence, authenticated browser evidence, process evidence, and Defender evidence are recorded.
- Full build, Pester, security review, PR CI/CodeQL, merge, deployment, and exact release verification pass.

## Rollback or Recovery

- First action is always `prod.cmd sensor-disable`; it must work without PawnIO health.
- The state mutation restores its previous boolean and restarts the website if endpoint verification fails.
- Application rollback uses the existing validated release-junction workflow only after disabling sensors.
- PawnIO removal uses its verified Windows uninstall entry; never delete driver files manually.
- Stop before any reboot-required result and request explicit approval.
- After rollback, verify false state, homepage 200/body marker, Running/Automatic services, one port owner, no orphan tree, and no active Defender threat.

## Risks

- PawnIO may require a reboot or may be incompatible with this Windows 11 build; mitigation is exit-3010 stop, separate approval, and disabled production.
- The actual installed driver identity may differ from assumed `PawnIO`; mitigation is to treat status failure as a blocker and update code/plan only from verified installed evidence before enablement.
- The seven-file runtime may expose a missing transitive assembly during the direct probe; mitigation is to keep sensors disabled and add only the exact missing file from the same pinned official archive with its recorded checksum and corresponding plan/spec amendment.
- Defender or another security product may reject PawnIO; mitigation is no exclusion and permanent unavailable fallback.
- Atomic configuration replacement may fail or endpoint restart may regress; mitigation is same-directory temp write, previous-value restoration, and endpoint re-verification.
- Driver-level faults can affect the host even with process isolation; mitigation is CPU-only enablement, short observation stages, immediate disable, verified uninstall, and no automatic reboot.
- Defender or AMSI may block the replacement script even when release hashes are correct; mitigation is to preserve the block, retain disabled state, and never add a bypass or exclusion.
- CI network access to the pinned GitHub archive may be intermittent; mitigation is Gradle output caching and clear checksum/download failure, never an unverified fallback mirror.

## Completion Criteria

- Every task executes in order with recorded RED/GREEN evidence and focused commits.
- Builder spec and this plan remain committed/pushed checkpoints before spoke implementation.
- Full automated, packaging, Pester, and security verification pass.
- Official PawnIO install either passes all gates without reboot or stops safely disabled.
- Candidate and production each pass three refresh windows with recorded CPU/process/Defender/service evidence, or CPU temperature remains deliberately disabled with a documented provider blocker.
- PR gates pass, the PR merges, the exact merge release deploys, and production remains healthy.
- Builder test report, spoke update, review, work closure, session memory, indexes, validation, and main push are complete.
