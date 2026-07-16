# Command Center CPU Temperature Selection and Application Commit Implementation Plan

## Document Status

`ready-for-execution`

## Objective

Replace the incorrect maximum-of-all-temperature-sensors behavior with a
deterministic actual-temperature selection and populate Application commit from
the protected deployed release metadata.

## Goals

- Prefer `CPU Package`, then `Core Max`, then the maximum remaining actual CPU
  temperature.
- Exclude every `Distance to TjMax` headroom sensor.
- Keep the numeric-only bounded probe contract and safe-unavailable behavior.
- Label the metric `CPU package temperature`.
- Export the exact validated release SHA for candidate and production JARs.
- Pass focused red-green tests, complete local suites, independent review, CI,
  deployment, and authenticated production acceptance.

## Inputs

- Spec:
  `docs/specs/2026-07-16-command-center-cpu-temperature-selection-and-commit.md`
- Active work:
  `docs/work/2026-07-12-command-center-cpu-temperature-and-uptime.md`
- Production merge:
  `1fc00914f8aa65b0b4cc931db2ff4a11b2cfb7f3`
- Elevated inventory:
  `C:\Users\Christopher\AppData\Local\Temp\cbdev-cpu-sensor-inventory.json`
- Root-cause values: Core Average `37.57 C`, Core Max `45 C`, CPU Package
  `48 C`, and TjMax-distance headroom up to `66 C`.

## Branch

- Base: refreshed `origin/main`
- Branch: `codex/cpu-temperature-selection-and-commit`
- Worktree:
  `A:\Projects\christopherbell.dev-worktrees\winsw-log-rotation-recovery-merged`

## Non-Goals

- No third-party-tool-specific calibration.
- No hard-coded TjMax subtraction.
- No provider dependency, ACL, PawnIO, refresh interval, warning threshold, or
  API shape change.
- No mutable Git command at service startup.
- No manual production metadata edits.

## Assumptions

- LibreHardwareMonitor continues naming the preferred sensors `CPU Package` and
  `Core Max`.
- Every supported production release contains `release.json` with a lowercase
  40-character SHA.
- The production service and deployment candidates launch only from validated
  release directories.

## Open Questions

None.

## Independent Review Amendment

Independent review of initial commit `c352b94c` found that a fixed operational
probe hash would break verification after rollback and that launcher-based
`GIT_COMMIT` injection would not reach normal merge-only production without a
separate tools/service installation. The following rules supersede conflicting
edits below:

- Do not modify `Production.Deploy.psm1`,
  `Start-ChristopherBellDev.ps1`, or their tests for Application commit.
- Resolve commit metadata inside `ApplicationHostMetricsProvider` from the
  active working directory's `release.json`, falling back only when the
  configured commit is absent.
- Do not keep `CpuTemperatureScriptSha256` in
  `Production.Sensors.psm1`.
- Derive the expected script SHA from
  `current\app.jar!/BOOT-INF/classes/lib/cpu-temperature.ps1`.
- Keep the displayed label generic `CPU temperature` because fallback hardware
  may not expose CPU Package.

## Task Breakdown

### Task 1 - Select actual CPU temperature deterministically

Sequence / dependencies:

- Runs first because the current displayed value is semantically incorrect.
- Add a behavioral Pester regression before changing the bundled probe.

Implementation notes:

- Add one pure PowerShell selection function so tests can extract its AST and
  invoke it without loading hardware drivers.
- Collect sensor name/value rows from CPU hardware and subhardware.
- Ignore non-finite, non-positive, implausible, and TjMax-distance values.
- Preserve numeric-only stdout.

#### Code Edit 1.1

- File: `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- Lines: after 328
- Action: add

Proposed:

```powershell
        It 'prefers package temperature and excludes TjMax distance headroom' {
            $probePath = Join-Path $PSScriptRoot (
                '..\..\..\..\website\src\main\resources\lib\cpu-temperature.ps1'
            )
            $tokens = $null
            $errors = $null
            $ast = [Management.Automation.Language.Parser]::ParseFile(
                $probePath, [ref]$tokens, [ref]$errors)
            $function = $ast.Find({
                param($node)
                $node -is [Management.Automation.Language.FunctionDefinitionAst] -and
                $node.Name -eq 'Select-CpuTemperature'
            }, $true)
            $function | Should -Not -BeNullOrEmpty
            Invoke-Expression $function.Extent.Text
            $rows = @(
                [pscustomobject]@{ Name='Core Average'; Value=37.5 },
                [pscustomobject]@{ Name='Core Max'; Value=45.0 },
                [pscustomobject]@{ Name='CPU Package'; Value=48.0 },
                [pscustomobject]@{ Name='E-Core #5 Distance to TjMax'; Value=66.0 }
            )

            Select-CpuTemperature $rows | Should -Be 48.0
            Select-CpuTemperature @(
                [pscustomobject]@{ Name='Core Max'; Value=45.0 },
                [pscustomobject]@{ Name='P-Core #1'; Value=43.0 },
                [pscustomobject]@{ Name='P-Core #1 Distance to TjMax'; Value=57.0 }
            ) | Should -Be 45.0
        }
```

Verification:

- Run focused Sensors Pester.
- Expected RED: `Select-CpuTemperature` does not exist.

#### Code Edit 1.2

- File: `website/src/main/resources/lib/cpu-temperature.ps1`
- Lines: after 7
- Action: add

Proposed:

```powershell
function Select-CpuTemperature {
  param([Parameter(Mandatory)][object[]]$Sensors)
  $actual = @($Sensors | Where-Object {
    $value = [double]$_.Value
    -not [double]::IsNaN($value) -and
    -not [double]::IsInfinity($value) -and
    $value -gt 0 -and
    $value -le 125 -and
    [string]$_.Name -notmatch '(?i)\s+Distance to TjMax$'
  })
  foreach ($preferredName in 'CPU Package','Core Max') {
    $preferred = @($actual | Where-Object Name -eq $preferredName)
    if ($preferred.Count -gt 0) {
      return ($preferred | Measure-Object -Property Value -Maximum).Maximum -as [double]
    }
  }
  if ($actual.Count -gt 0) {
    return ($actual | Measure-Object -Property Value -Maximum).Maximum -as [double]
  }
  return $null
}
```

Verification:

- The AST-based Pester test can extract and execute the pure function under
  both PowerShell 7 and Windows PowerShell 5.1.

#### Code Edit 1.3

- File: `website/src/main/resources/lib/cpu-temperature.ps1`
- Lines: 20-42
- Action: replace

Current:

```powershell
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
```

Proposed:

```powershell

  $sensors = @()
  foreach ($hardware in $computer.Hardware) {
    if ($hardware.HardwareType -eq [LibreHardwareMonitor.Hardware.HardwareType]::Cpu) {
      $hardware.Update()
      $sensors += $hardware.Sensors | Where-Object {
        $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature
      } | ForEach-Object {
        [pscustomobject]@{ Name=[string]$_.Name; Value=$_.Value }
      }
      foreach ($subHardware in $hardware.SubHardware) {
        $subHardware.Update()
        $sensors += $subHardware.Sensors | Where-Object {
          $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature
        } | ForEach-Object {
          [pscustomobject]@{ Name=[string]$_.Name; Value=$_.Value }
        }
      }
    }
  }
  $selected = Select-CpuTemperature $sensors
  if ($null -ne $selected) {
    [Console]::Write($selected.ToString(
        [Globalization.CultureInfo]::InvariantCulture))
  }
```

Verification:

- Re-run focused Sensors Pester and expect green.
- Run the read-only child inventory selection against fixture rows.

#### Code Edit 1.4

- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProvider.java`
- Lines: 28-39
- Action: replace

Current:

```java
      return Map.of("cpu.temperature", value.isPresent()
          ? new MetricReading("cpu.temperature", "CPU temperature", value.getAsDouble(),
              "celsius", MetricStatus.AVAILABLE, sampledAt, null)
          : unavailable(sampledAt));
```

Proposed:

```java
      return Map.of("cpu.temperature", value.isPresent()
          ? new MetricReading(
              "cpu.temperature", "CPU package temperature", value.getAsDouble(),
              "celsius", MetricStatus.AVAILABLE, sampledAt, null)
          : unavailable(sampledAt));
```

```java
    return new MetricReading(
        "cpu.temperature", "CPU package temperature", null, "celsius",
        MetricStatus.UNAVAILABLE, sampledAt, "CPU package temperature unavailable");
```

Verification:

- Update `LibreHardwareCpuTemperatureProviderTest` to assert the label for both
  available and unavailable readings.
- Run the focused Java provider test.

#### Code Edit 1.5

- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 62
- Action: replace

Current:

```java
        resource("cpu-temperature.ps1", "f90a50a607b3c714512a4cf9070339cb8e03ac2759e649be68f907bb75aee30b")),
```

Proposed:

```java
        resource("cpu-temperature.ps1", "<new lowercase SHA-256>")),
```

Verification:

- Compute SHA-256 from the exact committed script bytes.
- Update the matching uppercase hash in
  `ops/production/windows/modules/Production.Sensors.psm1`.
- Run `:website:verifySensorRuntime`.

#### Code Edit 1.6

- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: 7-185
- Action: replace

Current:

```powershell
$script:CpuTemperatureScriptSha256 = '<one release-specific hash>'
```

```powershell
if ((Get-FileHash -LiteralPath $scriptPath -Algorithm SHA256).Hash -ne
    $script:CpuTemperatureScriptSha256) {
    throw 'Live CPU temperature resource verification failed.'
}
```

Proposed:

```powershell
function Get-ProductionCpuTemperatureScriptHash {
    param([Parameter(Mandatory)][string]$Root)
    $jar = Join-Path $Root 'current\app.jar'
    $archive = [IO.Compression.ZipFile]::OpenRead($jar)
    try {
        $entries = @($archive.Entries | Where-Object {
            $_.FullName -eq 'BOOT-INF/classes/lib/cpu-temperature.ps1'
        })
        if ($entries.Count -ne 1) {
            throw 'Active release CPU probe resource is unavailable.'
        }
        $stream = $entries[0].Open()
        $sha = [Security.Cryptography.SHA256]::Create()
        try {
            return -join (
                $sha.ComputeHash($stream) |
                ForEach-Object { $_.ToString('X2') }
            )
        } finally {
            $sha.Dispose()
            $stream.Dispose()
        }
    } finally {
        $archive.Dispose()
    }
}
```

Verification:

- Pester creates a synthetic active JAR and proves the returned hash matches
  its embedded probe.
- The prior release's probe hash must remain verifiable after `current`
  changes during rollback.

### Task 2 - Superseded launcher approach

Sequence / dependencies:

- Do not execute Code Edits 2.1 through 2.5 below. They are retained only as
  review history and are superseded by Task 2A.

Sequence / dependencies:

- Runs after Task 1 is green.
- Add helper and launcher-contract tests before production edits.

Implementation notes:

- Validate `release.json` beneath an already validated release path.
- Permit only lowercase 40-character hexadecimal SHA values.
- Candidate additional environment must not override the actual release SHA.
- The installed production script performs the same validation before Java.

#### Code Edit 2.1

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: after 14
- Action: add

Proposed:

```powershell
        It 'reads a strict release SHA for the candidate commit label' {
            $release = Join-Path $TestDrive 'release'
            New-Item -ItemType Directory $release | Out-Null
            @{ sha='0123456789abcdef0123456789abcdef01234567' } |
                ConvertTo-Json | Set-Content (Join-Path $release 'release.json')

            Get-ProductionReleaseSha $release |
                Should -Be '0123456789abcdef0123456789abcdef01234567'

            @{ sha='../not-a-release' } |
                ConvertTo-Json | Set-Content (Join-Path $release 'release.json')
            { Get-ProductionReleaseSha $release } | Should -Throw '*invalid SHA*'
        }
```

Verification:

- Run focused Deploy Pester.
- Expected RED: `Get-ProductionReleaseSha` does not exist.

#### Code Edit 2.2

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: before 49
- Action: add

Proposed:

```powershell
function Get-ProductionReleaseSha {
    param([Parameter(Mandatory)][string]$Release)
    $metadata = Join-Path $Release 'release.json'
    if (-not (Test-Path -LiteralPath $metadata -PathType Leaf)) {
        throw 'Release metadata is unavailable.'
    }
    $releaseMetadata = Get-Content -LiteralPath $metadata -Raw |
        ConvertFrom-Json
    $sha = $releaseMetadata.sha -as [string]
    if ($sha -notmatch '^[0-9a-f]{40}$') {
        throw 'Release metadata contains an invalid SHA.'
    }
    return $sha
}
```

Verification:

- Re-run the strict release SHA test and expect green.

#### Code Edit 2.3

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 49-69
- Action: replace

Current:

```powershell
    $environment = Read-ProductionEnvironment (Join-Path $Config.programDataRoot 'config\app.env')
    foreach ($entry in $AdditionalEnvironment.GetEnumerator()) { $environment[$entry.Key] = [string]$entry.Value }
```

Proposed:

```powershell
    $environment = Read-ProductionEnvironment (
        Join-Path $Config.programDataRoot 'config\app.env')
    foreach ($entry in $AdditionalEnvironment.GetEnumerator()) {
        $environment[$entry.Key] = [string]$entry.Value
    }
    $environment.GIT_COMMIT = Get-ProductionReleaseSha $release
```

Verification:

- Add a Pester process-start test that captures the `ProcessStartInfo`
  environment and requires `GIT_COMMIT` to equal the release SHA.

#### Code Edit 2.4

- File: `ops/production/windows/tests/Production.Install.Tests.ps1`
- Lines: 64-70
- Action: replace

Current:

```powershell
    It 'starts the website with the protected typed sensor switch' {
        $startup = Get-Content (Join-Path $PSScriptRoot '..\service\Start-ChristopherBellDev.ps1') -Raw
        $startup | Should -Match 'sensorLibrariesEnabled'
        $startup | Should -Match 'COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED'
        $startup | Should -Match '--enable-native-access=ALL-UNNAMED'
        $startup | Should -Not -Match "SetEnvironmentVariable\('COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED',\s*'true'"
    }
```

Proposed:

```powershell
    It 'starts the website with typed sensors native access and release commit' {
        $startup = Get-Content (
            Join-Path $PSScriptRoot '..\service\Start-ChristopherBellDev.ps1'
        ) -Raw
        $startup | Should -Match 'sensorLibrariesEnabled'
        $startup | Should -Match 'COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED'
        $startup | Should -Match '--enable-native-access=ALL-UNNAMED'
        $startup | Should -Match "Join-Path \$root 'current\\release\.json'"
        $startup | Should -Match "\^\[0-9a-f\]\{40\}\$"
        $startup | Should -Match "'GIT_COMMIT'"
        $startup | Should -Not -Match (
            "SetEnvironmentVariable\('COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED'," +
            "\s*'true'"
        )
    }
```

Verification:

- Run focused Install Pester.
- Expected RED: the startup script does not mention `release.json` or
  `GIT_COMMIT`.

#### Code Edit 2.5

- File: `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- Lines: after 10
- Action: add

Proposed:

```powershell
$releaseMetadata = Get-Content -LiteralPath (
    Join-Path $root 'current\release.json') -Raw | ConvertFrom-Json
$releaseSha = [string]$releaseMetadata.sha
if ($releaseSha -notmatch '^[0-9a-f]{40}$') {
    throw 'Current release metadata contains an invalid SHA.'
}
[Environment]::SetEnvironmentVariable('GIT_COMMIT', $releaseSha, 'Process')
```

Verification:

- Re-run focused Install Pester and expect green.
- Confirm installed launcher refresh occurs during production deployment
  acceptance.

### Task 2A - Resolve Application commit inside the active release

Sequence / dependencies:

- Runs after the independent-review amendment and Task 1.
- Does not depend on installed production tools or launcher refresh.

Implementation notes:

- Extend `ProbeResult` with an optional release commit.
- Read only a bounded regular `release.json` in the active process working
  directory.
- Parse JSON with the application's existing Jackson library.
- Reuse the existing safe-commit allowlist.

#### Code Edit 2A.1

- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java`
- Lines: 17-48
- Action: replace

Current:

```java
new ApplicationHostMetricsProvider.ProbeResult(
    Optional.of(true), OptionalDouble.of(12.5))
```

Proposed:

```java
new ApplicationHostMetricsProvider.ProbeResult(
    Optional.of(true),
    OptionalDouble.of(12.5),
    Optional.of("0123456789abcdef0123456789abcdef01234567"))
```

Verification:

- A configured safe commit remains preferred.
- Without one, the validated release SHA is available.
- Missing or malformed release metadata remains unavailable.

#### Code Edit 2A.2

- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java`
- Lines: 37-128
- Action: replace

Current:

```java
String commit = safeCommit(properties.getCommitIdentifier());
```

```java
record ProbeResult(Optional<Boolean> serviceRunning, OptionalDouble responseMillis) {}
```

Proposed:

```java
String commit = safeCommit(properties.getCommitIdentifier());
if (commit == null) {
  commit = safeCommit(result.releaseCommit().orElse(null));
}
```

```java
record ProbeResult(
    Optional<Boolean> serviceRunning,
    OptionalDouble responseMillis,
    Optional<String> releaseCommit) {}
```

Verification:

- Run `ApplicationHostMetricsProviderTest`.
- Run the complete command-center metrics tests.

### Task 3 - Document, verify, review, publish, and deploy

Sequence / dependencies:

- Runs after Tasks 1 and 2 are green.
- No production mutation occurs before merge.

Implementation notes:

- Document CPU Package semantics and protected release SHA sourcing.
- Use the existing guarded deployment and CPU acceptance helpers.
- Require authenticated UI evidence for both corrected cards.

#### Code Edit 3.1

- File: `docs/operations/windows-production.md`
- Lines: after 184
- Action: add

Proposed:

```markdown
The CPU card prefers LibreHardwareMonitor's `CPU Package` sensor, then
`Core Max`, then the maximum remaining actual CPU temperature.
`Distance to TjMax` values are thermal headroom and are never displayed as
temperature.

Candidate and production launchers read the protected release's
`release.json`, validate its 40-character SHA, and export it as `GIT_COMMIT`
for the administrator-only Application commit card.
```

Verification:

- Run `rg -n "CPU Package|Distance to TjMax|GIT_COMMIT" docs/operations/windows-production.md`.

## Code Changes

- `Production.Sensors.Tests.ps1`: add behavioral sensor-selection regression.
- `cpu-temperature.ps1`: add pure selection function and preferred fallback
  order.
- `LibreHardwareCpuTemperatureProvider.java` and test: clarify package label.
- `SecureNativeLibraryProvisioner.java` and `Production.Sensors.psm1`: update
  the synchronized probe hash.
- `Production.Deploy.Tests.ps1`: validate strict release metadata and candidate
  environment.
- `Production.Deploy.psm1`: add strict SHA reader and `GIT_COMMIT`.
- `Production.Install.Tests.ps1`: require production launcher commit export.
- `Start-ChristopherBellDev.ps1`: validate current release SHA and export it.
- `windows-production.md`: document both operational contracts.

## Files and Modules

- `website/src/main/resources/lib/cpu-temperature.ps1`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProvider.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProviderTest.java`
- `ops/production/windows/modules/Production.Deploy.psm1`
- `ops/production/windows/modules/Production.Sensors.psm1`
- `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- `ops/production/windows/tests/Production.Install.Tests.ps1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `docs/operations/windows-production.md`

## Unit Testing

- Pester AST-based red-green test for package/core/fallback selection and
  TjMax-distance exclusion.
- Java label regression for available and unavailable package temperature.
- Pester strict release metadata tests for valid, missing, and malformed SHA.
- Pester launch-contract tests for candidate and installed service
  `GIT_COMMIT`.

## Local Testing

- Focused:
  `Invoke-Pester ops/production/windows/tests/Production.Sensors.Tests.ps1`.
- Focused:
  `Invoke-Pester ops/production/windows/tests/Production.Deploy.Tests.ps1`.
- Focused:
  `Invoke-Pester ops/production/windows/tests/Production.Install.Tests.ps1`.
- Focused Gradle:
  `.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.metrics.LibreHardwareCpuTemperatureProviderTest`.
- Complete Windows Pester suite.
- Full Gradle build with isolated `GRADLE_USER_HOME`.
- `git diff --check` and final diff inspection.

## Validation

- Independent review reports no Critical or Important findings.
- All GitHub CI and CodeQL checks pass.
- Immutable merge deploys successfully.
- Elevated inventory shows the selected value equals CPU Package when present
  and excludes TjMax-distance values.
- Direct probe and three cached refresh windows remain plausible.
- Authenticated command center displays `CPU package temperature` near the
  package/inventory value and Application commit matching the deployed SHA.
- Uptime remains human-readable.
- Defender has zero active threats; all three services remain Running and
  Automatic; local/public homepage checks remain `200` with
  `<title>CB | Home</title>`.

## Rollback or Recovery

- Keep the prior release available through the existing `previous` junction.
- Deployment verification automatically restores the former release on
  startup failure.
- If sensor acceptance fails, run `sensor-disable` and preserve website
  health.
- Do not weaken sensor selection, release validation, ACLs, or commit
  allowlisting to force acceptance.

## Risks

- CPU Package may legitimately differ from a tool displaying core average or a
  motherboard socket sensor. Mitigation: label the semantic explicitly and
  preserve deterministic fallbacks.
- LibreHardwareMonitor sensor names may change in a future upgrade. Mitigation:
  pin version 0.9.6 and keep fallback behavior.
- Strict release metadata validation could stop a manually assembled release.
  Mitigation: supported deployment always creates valid metadata; fail closed
  for unsupported releases.
- Hash synchronization errors could disable the provider. Mitigation: compute
  once from exact bytes and verify through both focused and runtime tests.

## Completion Criteria

- The selected sensor is CPU Package when available and never a TjMax-distance
  row.
- Application commit equals the deployed release SHA.
- Focused and complete local tests pass.
- Independent review, CI, merge, deployment, and authenticated UI acceptance
  pass.
- Builder test report, spoke update/review, closure, and session memory are
  validated, committed, and pushed.

## Compact Application Commit Card Amendment

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this amendment task-by-task.
> Steps use checkbox syntax for tracking.

**Goal:** Remove the duplicate Application commit subtitle while showing a
mobile-friendly eight-character SHA and preserving the full commit as
accessible title text.

**Architecture:** Keep commit metadata and validation unchanged. Add pure
frontend presentation helpers for the optional secondary detail and accessible
title, then make the DOM renderer consume those helpers so behavior is directly
testable without a browser DOM dependency.

**Tech Stack:** ECMAScript modules, Node's built-in test runner, Gradle, Spring
Boot static resources.

### Global Constraints

- Keep the card label `Application commit`.
- Display the first eight characters of an available commit identifier.
- Do not render a secondary line for a commit reading.
- Preserve the complete commit identifier in the value node's `title`
  attribute.
- Keep unavailable and malformed commit behavior unchanged.
- Do not change the API response, Java provider, release metadata, CSS, or
  server-side validation.
- Use branch `codex/compact-application-commit-card` from refreshed
  `origin/main`.

### File Structure

- `website/src/main/resources/static/js/lib/command-center.js`: pure metric
  value, secondary-detail, and accessible-title presentation rules.
- `website/src/main/resources/static/js/command-center.js`: DOM assembly using
  the pure presentation rules.
- `website/src/test/js/command-center.test.js`: red-green regression coverage
  for short SHA, suppressed duplicate detail, full accessible title, and
  unchanged non-commit detail.

### Task 4: Add pure commit-card presentation rules

**Files:**

- Modify:
  `website/src/test/js/command-center.test.js:1-57`
- Modify:
  `website/src/main/resources/static/js/lib/command-center.js:10-39`

**Interfaces:**

- Consumes: API metric readings with `unit`, `status`, `value`, and `detail`.
- Produces:
  `displayMetric(reading): string`,
  `metricDetail(reading): string|null`, and
  `metricTitle(reading): string|null`.

- [ ] **Step 1: Write the failing short-SHA test**

Replace the commit assertion in
`metric display formats service state, start timestamps, and commit
identifiers` with:

```javascript
  const commit = {
    key: 'application.commit',
    status: 'AVAILABLE',
    value: 1,
    unit: 'commit',
    detail: '0123456789abcdef0123456789abcdef01234567',
  };
  assert.equal(displayMetric(commit), '01234567');
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
node --test website/src/test/js/command-center.test.js
```

Expected: FAIL because `displayMetric(commit)` returns the complete
40-character SHA instead of `01234567`.

- [ ] **Step 3: Implement the minimal short-SHA formatting**

Replace the commit branch in `displayMetric` with:

```javascript
  if (reading.unit === 'commit') {
    return String(reading.detail || 'Unavailable').slice(0, 8);
  }
```

- [ ] **Step 4: Re-run the focused test and verify GREEN**

Run:

```powershell
node --test website/src/test/js/command-center.test.js
```

Expected: all command-center JavaScript tests pass.

- [ ] **Step 5: Write the failing presentation-helper test**

Add this namespace import after the existing imports:

```javascript
import * as commandCenterHelpers
  from '../../main/resources/static/js/lib/command-center.js';
```

Add:

```javascript
test('commit cards suppress duplicate detail and retain the full accessible title', () => {
  assert.equal(typeof commandCenterHelpers.metricDetail, 'function');
  assert.equal(typeof commandCenterHelpers.metricTitle, 'function');
  const sha = '0123456789abcdef0123456789abcdef01234567';
  const commit = {
    key: 'application.commit',
    status: 'AVAILABLE',
    value: 1,
    unit: 'commit',
    detail: sha,
  };

  assert.equal(commandCenterHelpers.metricDetail(commit), null);
  assert.equal(commandCenterHelpers.metricTitle(commit), sha);
  assert.equal(commandCenterHelpers.metricDetail({
    unit: 'celsius',
    detail: 'Last successful reading',
  }), 'Last successful reading');
  assert.equal(commandCenterHelpers.metricTitle({
    unit: 'celsius',
    detail: 'Last successful reading',
  }), null);
});
```

- [ ] **Step 6: Run the focused test and verify RED**

Run:

```powershell
node --test website/src/test/js/command-center.test.js
```

Expected: FAIL on the first `typeof` assertion because `metricDetail` and
`metricTitle` do not exist.

- [ ] **Step 7: Implement the pure helpers**

Add after `displayMetric`:

```javascript
/** Return optional secondary metric text without duplicating commit values. */
export function metricDetail(reading) {
  const detail = reading?.detail == null ? '' : String(reading.detail);
  if (!detail || reading?.unit === 'commit') return null;
  return detail;
}

/** Preserve the complete commit identifier as accessible title text. */
export function metricTitle(reading) {
  if (reading?.unit !== 'commit' || !reading?.detail) return null;
  return String(reading.detail);
}
```

- [ ] **Step 8: Re-run the focused test and verify GREEN**

Run:

```powershell
node --test website/src/test/js/command-center.test.js
```

Expected: all command-center JavaScript tests pass.

- [ ] **Step 9: Commit the pure presentation rules**

```powershell
git add website/src/main/resources/static/js/lib/command-center.js `
  website/src/test/js/command-center.test.js
git commit -m "Compact application commit presentation"
```

### Task 5: Make the card renderer consume the presentation rules

**Files:**

- Modify:
  `website/src/test/js/command-center.test.js:75-84`
- Modify:
  `website/src/main/resources/static/js/command-center.js:3-16,283-302`

**Interfaces:**

- Consumes:
  `metricDetail(reading): string|null` and
  `metricTitle(reading): string|null` from Task 4.
- Produces: a commit card with eight-character primary value, no `<small>`
  duplicate, and the full SHA in `strong.command-metric-value[title]`.

- [ ] **Step 1: Write the failing renderer-contract test**

Add:

```javascript
test('metric card renderer uses pure detail and accessible title rules', () => {
  const source = fs.readFileSync(
    'website/src/main/resources/static/js/command-center.js',
    'utf8'
  );

  assert.match(source, /metricDetail\(reading\)/);
  assert.match(source, /metricTitle\(reading\)/);
  assert.doesNotMatch(source, /if \(reading\.detail\)/);
});
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
node --test website/src/test/js/command-center.test.js
```

Expected: FAIL because the DOM renderer still branches directly on
`reading.detail`.

- [ ] **Step 3: Import and apply the presentation helpers**

Add `metricDetail` and `metricTitle` to the import list from
`./lib/command-center.js`.

Replace the value/detail portion of `metricCard` with:

```javascript
  const valueNode = document.createElement('strong');
  valueNode.className = 'command-metric-value';
  valueNode.textContent = displayMetric(reading);
  const title = metricTitle(reading);
  if (title) valueNode.title = title;
  const status = document.createElement('span');
  status.className = 'command-metric-status';
  status.textContent = state === 'available' ? 'Live' : state;
  card.append(label, valueNode, status, sparkline(points, `${reading.label || reading.key} 15 minute trend`));
  const detailText = metricDetail(reading);
  if (detailText) {
    const detail = document.createElement('small');
    detail.textContent = detailText;
    card.append(detail);
  }
```

- [ ] **Step 4: Re-run the focused test and verify GREEN**

Run:

```powershell
node --test website/src/test/js/command-center.test.js
```

Expected: all command-center JavaScript tests pass.

- [ ] **Step 5: Run the complete application verification**

Run:

```powershell
$env:GRADLE_USER_HOME = Join-Path $env:TEMP (
  'christopherbell-dev-gradle-compact-commit')
.\gradlew.bat :website:jsTest :website:build --no-daemon
git diff --check
```

Expected: all JavaScript and Java tests pass, the executable JAR builds, and
`git diff --check` produces no output.

- [ ] **Step 6: Commit the renderer integration**

```powershell
git add website/src/main/resources/static/js/command-center.js `
  website/src/test/js/command-center.test.js
git commit -m "Remove duplicate commit card detail"
```

### Task 6: Review, publish, deploy, and confirm

**Files:**

- Update:
  `docs/test-reports/2026-07-16-command-center-cpu-temperature-selection-and-application-commit-test-report.md`
- Update:
  `docs/work/2026-07-12-command-center-cpu-temperature-and-uptime.md`
- Update the related spoke review, closure, and session-memory records.

**Interfaces:**

- Consumes: clean tested spoke commits from Tasks 4 and 5.
- Produces: merged immutable release, production acceptance, and closed Builder
  records.

- [ ] **Step 1: Request independent code review**

Require no Critical or Important findings before publication.

- [ ] **Step 2: Push and open a pull request**

Push `codex/compact-application-commit-card`, open a PR against `main`, and
include the red-green evidence and the production visual defect.

- [ ] **Step 3: Pass CI and merge**

Require all repository build and CodeQL checks to pass, then squash-merge.

- [ ] **Step 4: Deploy the immutable merge**

Use the native Windows production deployment workflow. Verify the active
`release.json` equals the merge SHA before visual acceptance.

- [ ] **Step 5: Verify production**

Require:

- Local and public homepages return HTTP 200 with `<title>CB | Home</title>`.
- `MongoDB`, `ChristopherBellDev`, and `cloudflared` remain Running and
  Automatic.
- CPU Package selection, PawnIO signature, Defender state, and probe-process
  bounds remain healthy.
- The authenticated Application commit card shows eight SHA characters, has
  no duplicate subtitle, and exposes the full SHA as title text.

- [ ] **Step 6: Finish Builder closure**

Mark the spec, implementation plan, and test report complete; record the spoke
update/review and hub closure; save session memory; update indexes; validate
hub state; commit and push each required Builder checkpoint.
