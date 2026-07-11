# Native Windows Production Migration Implementation Plan

## Document Status

ready-for-execution

## Objective

Replace the WSL-dependent `christopherbell.dev` production runtime with native Windows MongoDB and a native Windows Java service, and provide a tested, versioned, atomic deployment system that always deploys the latest merged `origin/main` commit.

## Goals

- Build, test, deploy, operate, and recover production without WSL.
- Start MongoDB and `ChristopherBellDev` automatically during Windows boot without user login.
- Preserve every live MongoDB collection and index through a verified WSL-to-Windows migration.
- Keep production on port 8080 until a native candidate passes port-8081 smoke checks.
- Provide `prod install|migrate|deploy|status|logs|restart|releases|rollback|backup|uninstall`.
- Deploy exact `origin/main` commits from disposable clean Windows worktrees.
- Use versioned releases, atomic junction switching, bounded health checks, and automatic rollback.
- Keep WSL data and existing BSON/JSON backups intact until reboot acceptance and soak closure.
- Document the complete installation, migration, deployment, rollback, recovery, and removal workflow.

## Inputs

- Approved spoke design: `A:\Projects\christopherbell.dev-worktrees\boot-persistent-deploy-20260711\docs\superpowers\specs\2026-07-11-native-windows-production-deployment-design.md`.
- Spoke repository: `A:\Projects\christopherbell.dev` with remote `https://github.com/azurras/christopherbell.dev.git`.
- Existing native Windows MongoDB 8.3 service named `MongoDB`, currently disabled after the WSL incident.
- Live source MongoDB: Debian WSL `mongodb://127.0.0.1:27017/christopherbell`.
- Verified backups under `A:\Projects\christopherbell.dev-backups`.
- Java 25, Gradle Wrapper, native Git, PowerShell, Node for `:website:jsTest`, and MongoDB Database Tools.
- WinSW v2.12.0 x64 official release URL with SHA-256 `05B82D46AD331CC16BDC00DE5C6332C1EF818DF8CEEFCD49C726553209B3A0DA`.

## Branch

- Base: `origin/main` at or after merge commit `2d88d6ce244d17b71371f419c66dc104b47989f8`.
- Implementation branch: `codex/boot-persistent-deploy`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\boot-persistent-deploy-20260711`.
- All implementation must merge through a pull request; do not commit directly to remote `main`.

## Non-Goals

- Deleting or unregistering WSL during this project.
- Automatically deploying on GitHub push.
- Deploying PR branches or arbitrary local commits.
- Moving production to a remote server, VM, Docker, or Kubernetes.
- Rewriting application features unrelated to deployment safety.
- Deleting old WSL MongoDB files or backups during the initial soak period.

## Assumptions

- The app remains a portable Spring Boot executable JAR and has no Linux-only runtime dependency.
- Native Java 25 and Node are installable and their paths can be stored in non-secret deployment configuration.
- The Windows MongoDB service can use a dedicated native data directory and starts before the website service.
- WinSW 2.12.0 remains the pinned stable wrapper until a separately reviewed upgrade.
- Directory junction creation, service installation, ACL changes, and MongoDB configuration require elevated PowerShell.
- A short, coordinated write freeze is acceptable during final MongoDB cutover.
- The production hostname routing issue is outside this migration unless it blocks the final smoke check.

## Open Questions

None for implementation planning. The operator must choose the final soak-period duration before WSL production components are retired; the default recommendation is seven days with at least one successful reboot.

## Task Breakdown

### Task 1 - Add a mutation-safe deployment smoke profile

Sequence / dependencies:
- First implementation task because every later deployment and migration smoke check depends on running a second process without scheduled or startup mutations.

Implementation notes:
- Move scheduling enablement behind a property-controlled configuration class.
- Preserve current behavior when `app.scheduling.enabled` is absent.
- The `deploy-smoke` profile disables Spring scheduling and WFL monthly startup catch-up while retaining the `prod` database and security configuration.
- Write the configuration tests first and observe failure before changing production code.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/Application.java`
- Lines: 1-23
- Action: replace

Current:
```java
package dev.christopherbell;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Spring Boot application entry point.
 *
 * <p>Bootstraps the application context and starts the embedded web server.</p>
 */
@SpringBootApplication
@EnableScheduling
public class Application {
  /**
   * Starts the Spring Boot application.
   *
   * @param args command-line arguments
   */
  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
```

Proposed:
```java
package dev.christopherbell;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Boot application entry point.
 *
 * <p>Bootstraps the application context and starts the embedded web server.</p>
 */
@SpringBootApplication
public class Application {
  /**
   * Starts the Spring Boot application.
   *
   * @param args command-line arguments
   */
  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.SchedulingConfigurationTest`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/configuration/SchedulingConfiguration.java`
- Lines: after 0
- Action: add

Proposed:
```java
package dev.christopherbell.configuration;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

/** Enables application schedulers except in explicitly mutation-free runtime profiles. */
@Configuration
@EnableScheduling
@ConditionalOnProperty(
    name = "app.scheduling.enabled",
    havingValue = "true",
    matchIfMissing = true
)
public class SchedulingConfiguration {
}
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.SchedulingConfigurationTest`

#### Code Edit 1.3
- File: `website/src/main/resources/application-deploy-smoke.yml`
- Lines: after 0
- Action: add

Proposed:
```yaml
app:
  scheduling:
    enabled: false
wfl:
  restaurant-import:
    monthly:
      enabled: false
```

Verification:
- Start the candidate with `--spring.profiles.active=prod,deploy-smoke --server.port=8081` and confirm logs contain no scheduler or OpenStreetMap catch-up start message.

#### Code Edit 1.4
- File: `website/src/test/java/dev/christopherbell/configuration/SchedulingConfigurationTest.java`
- Lines: after 0
- Action: add

Proposed:
```java
package dev.christopherbell.configuration;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.scheduling.annotation.ScheduledAnnotationBeanPostProcessor;

class SchedulingConfigurationTest {

  private final ApplicationContextRunner contextRunner = new ApplicationContextRunner()
      .withUserConfiguration(SchedulingConfiguration.class);

  @Test
  void enablesSchedulingByDefault() {
    contextRunner.run(context -> assertThat(context)
        .hasSingleBean(ScheduledAnnotationBeanPostProcessor.class));
  }

  @Test
  void disablesSchedulingForMutationFreeSmokeRuns() {
    contextRunner
        .withPropertyValues("app.scheduling.enabled=false")
        .run(context -> assertThat(context)
            .doesNotHaveBean(ScheduledAnnotationBeanPostProcessor.class));
  }
}
```

Verification:
- Before Code Edits 1.1-1.2, the disabled case must fail because scheduling is unconditionally enabled.
- After implementation, both tests pass.

#### Code Edit 1.5
- File: `website/src/test/java/dev/christopherbell/configuration/MongoProfileConfigurationTest.java`
- Lines: 12-29
- Action: replace

Current:
```java
class MongoProfileConfigurationTest {

  @ParameterizedTest
  @ValueSource(strings = {"application-local.yml", "application-prod.yml"})
  void profileUsesSpringBootFourMongoConnectionProperties(String resourceName) throws IOException {
    var sources = new YamlPropertySourceLoader()
        .load(resourceName, new ClassPathResource(resourceName));

    assertThat(sources).isNotEmpty();
    var source = sources.getFirst();
    assertThat(source.getProperty("spring.mongodb.database")).isEqualTo("christopherbell");
    assertThat(source.getProperty("spring.mongodb.uri")).isEqualTo("mongodb://localhost:27017");
    assertThat(source.getProperty("spring.data.mongodb.auto-index-creation")).isEqualTo(true);
    assertThat(Stream.of("spring.data.mongodb.database", "spring.data.mongodb.uri")
        .map(source::getProperty)
        .toList()).containsOnlyNulls();
  }
}
```

Proposed:
```java
class MongoProfileConfigurationTest {

  @ParameterizedTest
  @ValueSource(strings = {"application-local.yml", "application-prod.yml"})
  void profileUsesSpringBootFourMongoConnectionProperties(String resourceName) throws IOException {
    var source = load(resourceName);
    assertThat(source.getProperty("spring.mongodb.database")).isEqualTo("christopherbell");
    assertThat(source.getProperty("spring.mongodb.uri")).isEqualTo("mongodb://localhost:27017");
    assertThat(source.getProperty("spring.data.mongodb.auto-index-creation")).isEqualTo(true);
    assertThat(Stream.of("spring.data.mongodb.database", "spring.data.mongodb.uri")
        .map(source::getProperty)
        .toList()).containsOnlyNulls();
  }

  @org.junit.jupiter.api.Test
  void deploySmokeProfileDisablesMutationSources() throws IOException {
    var source = load("application-deploy-smoke.yml");
    assertThat(source.getProperty("app.scheduling.enabled")).isEqualTo(false);
    assertThat(source.getProperty("wfl.restaurant-import.monthly.enabled")).isEqualTo(false);
  }

  private org.springframework.core.env.PropertySource<?> load(String resourceName)
      throws IOException {
    var sources = new YamlPropertySourceLoader()
        .load(resourceName, new ClassPathResource(resourceName));
    assertThat(sources).isNotEmpty();
    return sources.getFirst();
  }
}
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.MongoProfileConfigurationTest`

### Task 2 - Add the native Windows command surface and configuration contracts

Sequence / dependencies:
- Runs after Task 1 so every command can assume the smoke profile exists.

Implementation notes:
- `prod.cmd` is the dependency-free Windows entry point.
- An optional Makefile delegates only; PowerShell remains the implementation language.
- The dispatcher refuses unknown commands and returns child exit codes.
- Configuration is stored outside Git under ProgramData; checked-in examples contain no real credentials.

#### Code Edit 2.1
- File: `prod.cmd`
- Lines: after 0
- Action: add

Proposed:
```bat
@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%ops\production\windows\prod.ps1" %*
exit /b %ERRORLEVEL%
```

Verification:
- `prod.cmd help` exits 0 and lists every supported command.
- `prod.cmd unknown-command` exits non-zero without changing services or files.

#### Code Edit 2.2
- File: `Makefile`
- Lines: after 0
- Action: add

Proposed:
```makefile
.PHONY: prod-install prod-migrate prod-deploy prod-status prod-logs prod-restart prod-releases prod-rollback prod-backup prod-uninstall

prod-install prod-migrate prod-deploy prod-status prod-logs prod-restart prod-releases prod-rollback prod-backup prod-uninstall:
	@cmd.exe /d /c prod.cmd $(@:prod-%=%)
```

Verification:
- Where Make is installed, `make prod-status` invokes the same status path as `prod.cmd status`.

#### Code Edit 2.3
- File: `ops/production/windows/prod.ps1`
- Lines: after 0
- Action: add

Proposed:
```powershell
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('help','install','migrate','deploy','status','logs','restart','releases','rollback','backup','uninstall')]
    [string]$Command = 'help',
    [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
$moduleRoot = Join-Path $PSScriptRoot 'modules'
Import-Module (Join-Path $moduleRoot 'Production.Common.psm1') -Force
Import-Module (Join-Path $moduleRoot 'Production.Deploy.psm1') -Force
Import-Module (Join-Path $moduleRoot 'Production.Install.psm1') -Force
Import-Module (Join-Path $moduleRoot 'Production.Migrate.psm1') -Force
Import-Module (Join-Path $moduleRoot 'Production.Operations.psm1') -Force

$handlers = @{
    help = { Show-ProductionHelp }
    install = { Install-ProductionRuntime -WhatIf:$WhatIf }
    migrate = { Invoke-ProductionMigration -WhatIf:$WhatIf }
    deploy = { Invoke-ProductionDeploy -WhatIf:$WhatIf }
    status = { Get-ProductionStatus }
    logs = { Watch-ProductionLogs }
    restart = { Restart-ProductionService -Verify }
    releases = { Get-ProductionReleases }
    rollback = { Invoke-ProductionRollback -WhatIf:$WhatIf }
    backup = { New-ProductionBackup }
    uninstall = { Uninstall-ProductionRuntime -WhatIf:$WhatIf }
}

& $handlers[$Command]
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1`

#### Code Edit 2.4
- File: `ops/production/windows/config/deploy.example.json`
- Lines: after 0
- Action: add

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
  "candidatePort": 8081,
  "productionPort": 8080,
  "smokeAccountEmail": "operator@example.com",
  "releaseRetention": 5
}
```

Verification:
- Config loader rejects missing paths, invalid ports, retention below two, or a smoke email that is still `operator@example.com`.

#### Code Edit 2.5
- File: `ops/production/windows/config/app.env.example`
- Lines: after 0
- Action: add

Proposed:
```dotenv
APP_JWT_SECRET=replace-with-at-least-32-random-characters
RESEND_API_KEY=re_your_resend_api_key
APP_MAIL_FROM=noreply@your-verified-domain.com
SPRING_MONGODB_URI=mongodb://127.0.0.1:27017
```

Verification:
- Installer creates only the example when the real ProgramData `app.env` is absent and never overwrites an existing secret file.

### Task 3 - Implement testable deployment primitives

Sequence / dependencies:
- Runs after Task 2 because modules consume the checked-in configuration schema and command surface.

Implementation notes:
- Write Pester tests first using `$TestDrive` and stub command scripts.
- Centralize path validation, process execution, locking, environment parsing, port polling, and secret-safe logging.
- Never interpolate secret values into a process command line or log message.

#### Code Edit 3.1
- File: `ops/production/windows/modules/Production.Common.psm1`
- Lines: after 0
- Action: add

Proposed:
```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Read-ProductionConfig {
    param([string]$Path = 'C:\ProgramData\christopherbell.dev\config\deploy.json')
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing deploy config: $Path" }
    $config = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    foreach ($name in 'repositoryPath','programDataRoot','javaExe','nodeExe','mongoToolsPath','smokeAccountEmail') {
        if ([string]::IsNullOrWhiteSpace($config.$name)) { throw "Missing deploy config value: $name" }
    }
    if ($config.candidatePort -eq $config.productionPort) { throw 'Candidate and production ports must differ.' }
    if ([int]$config.releaseRetention -lt 2) { throw 'releaseRetention must be at least 2.' }
    return $config
}

function Invoke-CheckedProcess {
    param([string]$FilePath, [string[]]$ArgumentList, [string]$WorkingDirectory)
    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory -Wait -NoNewWindow -PassThru
    if ($process.ExitCode -ne 0) { throw "$FilePath exited with code $($process.ExitCode)." }
}

function Enter-DeploymentLock {
    param([string]$LockPath)
    New-Item -ItemType Directory -Force -Path (Split-Path $LockPath) | Out-Null
    try { return [IO.File]::Open($LockPath, 'OpenOrCreate', 'ReadWrite', 'None') }
    catch { throw 'Another production operation is already running.' }
}

function Wait-HttpStatus {
    param([uri]$Uri, [int]$ExpectedStatus, [timespan]$Timeout)
    $deadline = [DateTime]::UtcNow + $Timeout
    do {
        $status = $null
        $response = $null
        try {
            $response = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec 5
            $status = [int]$response.StatusCode
        } catch [System.Net.WebException] {
            if ($_.Exception.Response) {
                $status = [int]$_.Exception.Response.StatusCode
                $response = $_.Exception.Response
            }
        }
        if ($status -eq $ExpectedStatus) { return $response }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $deadline)
    throw "Timed out waiting for HTTP $ExpectedStatus from $Uri."
}

Export-ModuleMember -Function Read-ProductionConfig,Invoke-CheckedProcess,Enter-DeploymentLock,Wait-HttpStatus
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Common.Tests.ps1`
- Tests cover invalid config, exclusive lock contention, non-zero child exit, successful polling, and timeout.

#### Code Edit 3.2
- File: `ops/production/windows/tests/Production.Common.Tests.ps1`
- Lines: after 0
- Action: add

Proposed:
```powershell
BeforeAll {
    Import-Module "$PSScriptRoot\..\modules\Production.Common.psm1" -Force
}

Describe 'production common operations' {
    It 'rejects concurrent deployment locks' {
        $path = Join-Path $TestDrive 'deploy.lock'
        $first = Enter-DeploymentLock -LockPath $path
        try { { Enter-DeploymentLock -LockPath $path } | Should -Throw '*already running*' }
        finally { $first.Dispose() }
    }

    It 'rejects candidate and production port collisions' {
        $path = Join-Path $TestDrive 'deploy.json'
        @{ repositoryPath='C:\repo'; programDataRoot='C:\data'; javaExe='java'; nodeExe='node';
           mongoToolsPath='C:\mongo'; smokeAccountEmail='admin@example.com'; candidatePort=8080;
           productionPort=8080; releaseRetention=5 } | ConvertTo-Json | Set-Content $path
        { Read-ProductionConfig -Path $path } | Should -Throw '*must differ*'
    }
}
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Common.Tests.ps1` reports zero failures.

### Task 4 - Implement clean origin/main builds, candidate verification, switching, and rollback

Sequence / dependencies:
- Runs after Task 3 because deploy orchestration uses the validated process, lock, and HTTP helpers.

Implementation notes:
- Build SHA must come from fetched `refs/remotes/origin/main`, not the caller's current branch.
- Use a deployment-local `GRADLE_USER_HOME`, explicit `NODE_EXE`, and `gradlew.bat --no-daemon :website:build`.
- Candidate process receives secrets through a generated temporary environment block/launcher file whose ACL is restricted and which is deleted in `finally`.
- Junction replacement must validate that every resolved target remains below `releases`.
- Automatic rollback is mandatory after any failed port-8080 verification.

#### Code Edit 4.1
- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: after 0
- Action: add

Proposed:
```powershell
Set-StrictMode -Version Latest

function Resolve-OriginMainRelease {
    param($Config)
    Invoke-CheckedProcess git @('-C',$Config.repositoryPath,'fetch',$Config.remote,$Config.branch) $Config.repositoryPath
    return (& git -C $Config.repositoryPath rev-parse "$($Config.remote)/$($Config.branch)").Trim()
}

function New-ReleaseFromOriginMain {
    param($Config, [string]$Sha)
    $worktree = Join-Path $Config.programDataRoot "worktrees\$Sha"
    $release = Join-Path $Config.programDataRoot "releases\$Sha"
    if (Test-Path $release) { return $release }
    try {
        Invoke-CheckedProcess git @('-C',$Config.repositoryPath,'worktree','add','--detach',$worktree,$Sha) $Config.repositoryPath
        $env:GRADLE_USER_HOME = Join-Path $Config.programDataRoot 'gradle-home'
        $env:NODE_EXE = $Config.nodeExe
        Invoke-CheckedProcess (Join-Path $worktree 'gradlew.bat') @('--no-daemon',':website:build') $worktree
        $jars = @(Get-ChildItem (Join-Path $worktree 'website\build\libs') -Filter '*.jar' |
            Where-Object Name -NotLike '*-plain.jar')
        if ($jars.Count -ne 1) { throw "Expected one executable boot JAR, found $($jars.Count)." }
        $jar = $jars[0]
        $staging = "$release.staging"
        New-Item -ItemType Directory -Force $staging | Out-Null
        Copy-Item $jar.FullName (Join-Path $staging 'app.jar')
        @{ sha=$Sha; source="$($Config.remote)/$($Config.branch)"; builtAt=(Get-Date).ToUniversalTime() } |
            ConvertTo-Json | Set-Content (Join-Path $staging 'release.json') -Encoding utf8
        Move-Item $staging $release
        return $release
    } finally {
        git -C $Config.repositoryPath worktree remove --force $worktree 2>$null
        git -C $Config.repositoryPath worktree prune
    }
}

function Test-CandidateRelease {
    param($Config, [string]$Release)
    $process = Start-ProductionJar -Config $Config -Release $Release -Port $Config.candidatePort `
        -Profiles 'prod,deploy-smoke'
    try { Test-ProductionEndpoints -Config $Config -Port $Config.candidatePort }
    finally { Stop-Process -Id $process.Id -ErrorAction SilentlyContinue; $process.WaitForExit(10000) | Out-Null }
}

function Switch-ProductionRelease {
    param($Config, [string]$Release)
    $old = Get-JunctionTarget (Join-Path $Config.programDataRoot 'current')
    Stop-Service ChristopherBellDev -ErrorAction Stop
    try {
        if ($old) { Set-AtomicJunction (Join-Path $Config.programDataRoot 'previous') $old }
        Set-AtomicJunction (Join-Path $Config.programDataRoot 'current') $Release
        Start-Service ChristopherBellDev
        Test-ProductionEndpoints -Config $Config -Port $Config.productionPort
    } catch {
        if ($old) {
            Stop-Service ChristopherBellDev -ErrorAction SilentlyContinue
            Set-AtomicJunction (Join-Path $Config.programDataRoot 'current') $old
            Start-Service ChristopherBellDev
            Test-ProductionEndpoints -Config $Config -Port $Config.productionPort
        }
        throw
    }
}

function Invoke-ProductionDeploy {
    param([switch]$WhatIf)
    $config = Read-ProductionConfig
    $lock = Enter-DeploymentLock (Join-Path $config.programDataRoot 'locks\deploy.lock')
    try {
        $sha = Resolve-OriginMainRelease $config
        if ($WhatIf) { Write-Host "Would deploy origin/main at $sha"; return }
        $release = New-ReleaseFromOriginMain $config $sha
        Test-CandidateRelease $config $release
        Switch-ProductionRelease $config $release
        Remove-ExpiredReleases $config
    } finally { $lock.Dispose() }
}

Export-ModuleMember -Function Invoke-ProductionDeploy,Resolve-OriginMainRelease,New-ReleaseFromOriginMain,Test-CandidateRelease,Switch-ProductionRelease
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Deploy.Tests.ps1`
- `prod.cmd deploy -WhatIf` prints the fetched `origin/main` SHA without changing services or releases.

#### Code Edit 4.2
- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: after 0
- Action: add

Proposed:
```powershell
BeforeAll {
    Import-Module "$PSScriptRoot\..\modules\Production.Common.psm1" -Force
    Import-Module "$PSScriptRoot\..\modules\Production.Deploy.psm1" -Force
}

Describe 'native Windows deployment' {
    It 'resolves the fetched remote main instead of the checked-out branch' {
        Mock Invoke-CheckedProcess {}
        Mock git { '0123456789abcdef' }
        $config = [pscustomobject]@{ repositoryPath='C:\repo'; remote='origin'; branch='main' }
        Resolve-OriginMainRelease $config | Should -Be '0123456789abcdef'
    }

    It 'restores the former current release after production verification fails' {
        Mock Stop-Service {}
        Mock Start-Service {}
        Mock Get-JunctionTarget { 'C:\ProgramData\christopherbell.dev\releases\old' }
        Mock Set-AtomicJunction {}
        Mock Test-ProductionEndpoints { if ($script:attempt++ -eq 0) { throw 'failed verification' } }
        $script:attempt = 0
        { Switch-ProductionRelease ([pscustomobject]@{programDataRoot='C:\ProgramData\christopherbell.dev'; productionPort=8080}) 'C:\ProgramData\christopherbell.dev\releases\new' } |
            Should -Throw '*failed verification*'
        Should -Invoke Set-AtomicJunction -ParameterFilter { $Target -like '*\old' }
    }
}
```

Verification:
- Pester covers candidate failure without switch, successful switch, production failure rollback, junction containment, worktree cleanup, and active-release retention.

### Task 5 - Install the native Windows Java service securely

Sequence / dependencies:
- Runs after Task 4 so installation can finish through the same tested deploy path.

Implementation notes:
- Pin WinSW v2.12.0 and verify the downloaded binary hash before installation.
- Use `LocalSystem` only if ACL and outbound mail/network tests pass; otherwise configure a dedicated local service identity with least privilege.
- The service launcher reads only allowlisted `app.env` keys and never writes values to output.
- Configure Windows service dependency on `MongoDB`, automatic startup, delayed recovery, and rotated logs.

#### Code Edit 5.1
- File: `ops/production/windows/service/ChristopherBellDev.xml`
- Lines: after 0
- Action: add

Proposed:
```xml
<service>
  <id>ChristopherBellDev</id>
  <name>ChristopherBellDev</name>
  <description>christopherbell.dev Spring Boot production service</description>
  <executable>powershell.exe</executable>
  <arguments>-NoLogo -NoProfile -ExecutionPolicy Bypass -File "%BASE%\Start-ChristopherBellDev.ps1"</arguments>
  <workingdirectory>C:\ProgramData\christopherbell.dev\current</workingdirectory>
  <depend>MongoDB</depend>
  <startmode>Automatic</startmode>
  <stoptimeout>30sec</stoptimeout>
  <onfailure action="restart" delay="10 sec" />
  <onfailure action="restart" delay="30 sec" />
  <resetfailure>1 hour</resetfailure>
  <logpath>C:\ProgramData\christopherbell.dev\logs</logpath>
  <log mode="roll-by-size-time">
    <sizeThreshold>10485760</sizeThreshold>
    <pattern>yyyyMMdd</pattern>
    <autoRollAtTime>00:00:00</autoRollAtTime>
    <zipOlderThanNumDays>7</zipOlderThanNumDays>
    <zipDateFormat>yyyyMMdd</zipDateFormat>
  </log>
</service>
```

Verification:
- `Get-Service ChristopherBellDev | Select Status,StartType,ServicesDependedOn` shows Automatic and MongoDB dependency.

#### Code Edit 5.2
- File: `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- Lines: after 0
- Action: add

Proposed:
```powershell
$ErrorActionPreference = 'Stop'
$root = 'C:\ProgramData\christopherbell.dev'
$config = Get-Content (Join-Path $root 'config\deploy.json') -Raw | ConvertFrom-Json
Get-Content (Join-Path $root 'config\app.env') | ForEach-Object {
    if ($_ -match '^\s*(APP_JWT_SECRET|RESEND_API_KEY|APP_MAIL_FROM|SPRING_MONGODB_URI)=(.*)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
& $config.javaExe '-Xrs' '-jar' (Join-Path $root 'current\app.jar') `
    '--spring.profiles.active=prod' '--server.port=8080'
exit $LASTEXITCODE
```

Verification:
- Process command line contains the JAR/profile/port but no secret value.
- Service account can read only required release/config paths and can write only logs/temp paths.

#### Code Edit 5.3
- File: `ops/production/windows/modules/Production.Install.psm1`
- Lines: after 0
- Action: add

Proposed:
```powershell
$script:WinSwUri = 'https://github.com/winsw/winsw/releases/download/v2.12.0/WinSW-x64.exe'
$script:WinSwSha256 = '05B82D46AD331CC16BDC00DE5C6332C1EF818DF8CEEFCD49C726553209B3A0DA'

function Assert-Administrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]$identity
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'This operation requires elevated PowerShell.'
    }
}

function Install-ProductionRuntime {
    param([switch]$WhatIf)
    Assert-Administrator
    $config = Read-ProductionConfig
    if ($WhatIf) { Write-Host 'Would install ProgramData layout, ACLs, WinSW, and services.'; return }
    New-ProductionDirectories $config
    Install-ConfigurationExamples $config
    Protect-ProductionSecrets $config
    $binary = Join-Path $config.programDataRoot 'service\ChristopherBellDev.exe'
    Invoke-WebRequest $script:WinSwUri -OutFile "$binary.download"
    if ((Get-FileHash "$binary.download" -Algorithm SHA256).Hash -ne $script:WinSwSha256) {
        Remove-Item "$binary.download" -Force
        throw 'WinSW SHA-256 verification failed.'
    }
    Move-Item "$binary.download" $binary -Force
    Copy-Item "$PSScriptRoot\..\service\ChristopherBellDev.xml" (Split-Path $binary)
    Copy-Item "$PSScriptRoot\..\service\Start-ChristopherBellDev.ps1" (Split-Path $binary)
    & $binary install
    sc.exe config ChristopherBellDev start= auto depend= MongoDB | Out-Null
    sc.exe failure ChristopherBellDev reset= 3600 actions= restart/10000/restart/30000 | Out-Null
}

Export-ModuleMember -Function Install-ProductionRuntime,Uninstall-ProductionRuntime
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Install.Tests.ps1`
- Installer preserves an existing `app.env`, rejects a hash mismatch, and is idempotent.

### Task 6 - Implement collection-and-index-verified WSL-to-Windows MongoDB migration

Sequence / dependencies:
- Runs after Task 5 so the native candidate and service infrastructure are available, but before the native website service owns production port 8080.

Implementation notes:
- Migration requires explicit confirmation and an exclusive lock.
- Take a new archive and dry-run verification immediately before freezing writes.
- Inventory collection counts and indexes as canonical JSON on both sides.
- Restore first to `christopherbell_restore_check`; never `--drop` the final target until validation succeeds and the operator confirms cutover.
- Stop only the WSL website for the write freeze; retain WSL MongoDB as rollback source.

#### Code Edit 6.1
- File: `ops/production/windows/modules/Production.Migrate.psm1`
- Lines: after 0
- Action: add

Proposed:
```powershell
function Get-MongoInventory {
    param([string]$MongoShell, [string]$Uri, [string]$Database)
    $script = @'
const d = db.getSiblingDB(process.env.INVENTORY_DATABASE);
const result = {};
d.getCollectionNames().sort().forEach(name => {
  result[name] = {
    count: d.getCollection(name).countDocuments({}),
    indexes: d.getCollection(name).getIndexes().map(i => ({name:i.name,key:i.key,unique:!!i.unique})).sort((a,b)=>a.name.localeCompare(b.name))
  };
});
print(EJSON.stringify(result));
'@
    $env:INVENTORY_DATABASE = $Database
    $json = (& $MongoShell $Uri --quiet --eval $script)
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($json)) {
        throw "MongoDB inventory failed for $Database."
    }
    return $json.Trim()
}

function Assert-MongoInventoryEqual {
    param([string]$Source, [string]$Target)
    if ($Source -cne $Target) { throw 'MongoDB collection/count/index inventory mismatch.' }
}

function Invoke-ProductionMigration {
    param([switch]$WhatIf)
    Assert-Administrator
    $config = Read-ProductionConfig
    $lock = Enter-DeploymentLock (Join-Path $config.programDataRoot 'locks\migration.lock')
    try {
        $archive = New-WslMongoBackup -Config $config
        Test-MongoArchive -Config $config -Archive $archive
        $source = Get-WslMongoInventory -Config $config
        if ($WhatIf) { Write-Host 'Backup and source inventory verified; no cutover performed.'; return }
        Stop-WslWebsite -Config $config
        Assert-WslWebsiteStopped -Config $config
        Start-Service MongoDB
        Restore-MongoValidationDatabase -Config $config -Archive $archive
        $validation = Get-WindowsMongoInventory -Config $config -Database 'christopherbell_restore_check'
        Assert-MongoInventoryEqual $source $validation
        Test-NativeCandidate -Config $config -Database 'christopherbell_restore_check'
        Promote-ValidatedMongoDatabase -Config $config -Archive $archive
        $final = Get-WindowsMongoInventory -Config $config -Database 'christopherbell'
        Assert-MongoInventoryEqual $source $final
        Test-NativeCandidate -Config $config -Database 'christopherbell'
    } catch {
        Restore-WslProduction -Config $config
        throw
    } finally { $lock.Dispose() }
}

Export-ModuleMember -Function Invoke-ProductionMigration,Get-MongoInventory,Assert-MongoInventoryEqual
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Migrate.Tests.ps1`
- Dry-run proves backup and source inventory without stopping WSL production.
- Migration rehearsal restores into a temporary Windows database and detects an intentionally removed document or index.

#### Code Edit 6.2
- File: `ops/production/windows/tests/Production.Migrate.Tests.ps1`
- Lines: after 0
- Action: add

Proposed:
```powershell
BeforeAll {
    Import-Module "$PSScriptRoot\..\modules\Production.Migrate.psm1" -Force
}

Describe 'MongoDB migration inventory' {
    It 'accepts identical collection counts and indexes' {
        $inventory = '{"accounts":{"count":20,"indexes":[{"name":"_id_","key":{"_id":1},"unique":false}]}}'
        { Assert-MongoInventoryEqual $inventory $inventory } | Should -Not -Throw
    }

    It 'rejects a missing target document' {
        $source = '{"accounts":{"count":20,"indexes":[]}}'
        $target = '{"accounts":{"count":19,"indexes":[]}}'
        { Assert-MongoInventoryEqual $source $target } | Should -Throw '*inventory mismatch*'
    }
}
```

Verification:
- Pester covers count mismatch, missing collection, missing index, changed uniqueness, write-freeze failure, restore failure, and WSL rollback invocation.

### Task 7 - Add operational backup, status, logs, releases, restart, rollback, retention, and uninstall

Sequence / dependencies:
- Runs after Tasks 4-6 because these commands reuse release, service, and Mongo helpers.

Implementation notes:
- `backup` creates a compressed native Windows MongoDB archive, dry-runs restore parsing, writes SHA-256, and never deletes the previous verified backup.
- `rollback` refuses to run without valid current/previous junctions and uses the same production verification as deploy.
- `uninstall` removes the app service only; preserving data, secrets, releases, and MongoDB is the default.

#### Code Edit 7.1
- File: `ops/production/windows/modules/Production.Operations.psm1`
- Lines: after 0
- Action: add

Proposed:
```powershell
function Get-ProductionStatus {
    $config = Read-ProductionConfig
    [pscustomobject]@{
        WebsiteService = (Get-Service ChristopherBellDev -ErrorAction SilentlyContinue).Status
        MongoService = (Get-Service MongoDB -ErrorAction SilentlyContinue).Status
        CurrentRelease = Get-JunctionTarget (Join-Path $config.programDataRoot 'current')
        PreviousRelease = Get-JunctionTarget (Join-Path $config.programDataRoot 'previous')
        ProductionPort = (Get-NetTCPConnection -LocalPort $config.productionPort -State Listen -ErrorAction SilentlyContinue).OwningProcess
    }
}

function Invoke-ProductionRollback {
    param([switch]$WhatIf)
    $config = Read-ProductionConfig
    $current = Get-JunctionTarget (Join-Path $config.programDataRoot 'current')
    $previous = Get-JunctionTarget (Join-Path $config.programDataRoot 'previous')
    if (-not $current -or -not $previous) { throw 'Both current and previous releases are required.' }
    if ($WhatIf) { Write-Host "Would roll back from $current to $previous"; return }
    Stop-Service ChristopherBellDev
    Set-AtomicJunction (Join-Path $config.programDataRoot 'current') $previous
    Set-AtomicJunction (Join-Path $config.programDataRoot 'previous') $current
    Start-Service ChristopherBellDev
    Test-ProductionEndpoints $config $config.productionPort
}

function New-ProductionBackup {
    $config = Read-ProductionConfig
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    $archive = Join-Path $config.programDataRoot "backups\christopherbell-$stamp.archive.gz"
    & (Join-Path $config.mongoToolsPath 'mongodump.exe') --uri mongodb://127.0.0.1:27017 --db christopherbell --archive $archive --gzip
    if ($LASTEXITCODE -ne 0 -or (Get-Item $archive).Length -eq 0) { throw 'mongodump failed.' }
    & (Join-Path $config.mongoToolsPath 'mongorestore.exe') --archive $archive --gzip --dryRun
    if ($LASTEXITCODE -ne 0) { throw 'mongorestore dry run failed.' }
    Get-FileHash $archive -Algorithm SHA256 | ConvertTo-Json | Set-Content "$archive.sha256.json"
    return $archive
}

Export-ModuleMember -Function Get-ProductionStatus,Invoke-ProductionRollback,New-ProductionBackup,Watch-ProductionLogs,Restart-ProductionService,Get-ProductionReleases
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Operations.Tests.ps1`
- Manually verify `prod status`, `prod releases`, `prod backup`, `prod rollback -WhatIf`, and `prod logs`.

### Task 8 - Replace WSL-oriented production documentation with native Windows operations

Sequence / dependencies:
- Runs after command behavior stabilizes so documentation reflects tested commands exactly.

Implementation notes:
- Keep developer onboarding concise in the root README and place operational detail in a dedicated runbook.
- Rewrite the MongoDB runbook with native Windows commands while preserving WSL migration fallback instructions.
- Document WinSW version/hash, ProgramData ACLs, native prerequisites, service recovery, migration gates, reboot test, soak period, and uninstall.

#### Code Edit 8.1
- File: `README.md`
- Lines: 350-398
- Action: replace

Current:
```markdown
 ## Production

Build:

```bash
./gradlew :website:build
```

Set production configuration with environment variables:

```bash
export SPRING_PROFILES_ACTIVE=prod
export SPRING_DATA_MONGODB_URI=mongodb://<host>:<port>/<db>
export SERVER_PORT=8080
export RESEND_API_KEY=re_your_resend_key
export APP_MAIL_FROM=noreply@your-verified-domain.com
```

Run:

```bash
java -jar website/build/libs/<jar-name>.jar
```

 ### MongoDB Backups and Restores

Use `docs/operations/mongodb-backup-restore.md`
for production backup commands, expected archive storage, restore steps, and
restore smoke checks.

 ## Troubleshooting

Gradle wrapper has Windows line endings in WSL:

```bash
sed -i 's/\r$//' gradlew
chmod +x gradlew
```

Cannot connect to MongoDB:

- Confirm MongoDB is running.
- Confirm the URI matches the active profile.
- Override with `SPRING_DATA_MONGODB_URI` if needed.

Static JS changes are not visible:

- Hard-refresh the browser.
- Restart `:website:bootRun` if template or server config changed.
```

Proposed:
```markdown
 ## Production

Production runs natively on Windows through the `MongoDB` and
`ChristopherBellDev` Windows services. WSL is not part of the production or
deployment path.

From an elevated PowerShell prompt, install or update the runtime with:

```powershell
.\prod.cmd install
.\prod.cmd deploy
```

`deploy` always fetches and deploys the exact latest `origin/main` commit from
a clean detached Windows worktree. It builds and tests the candidate, validates
it on port 8081, atomically switches the active release, restarts port 8080, and
rolls back automatically when verification fails.

Common operations:

```powershell
.\prod.cmd status
.\prod.cmd logs
.\prod.cmd releases
.\prod.cmd rollback
.\prod.cmd backup
```

See `docs/operations/windows-production.md` and
`docs/operations/mongodb-backup-restore.md`.

 ## Troubleshooting

Run `.\prod.cmd status` first for production failures. Use `.\prod.cmd logs` for
application and WinSW wrapper output. Confirm both Windows services are running
and that `SPRING_MONGODB_URI` targets `mongodb://127.0.0.1:27017`.

For development asset changes, hard-refresh the browser and restart
`:website:bootRun` when templates or server configuration changed.
```

Verification:
- Every documented command exists and matches dispatcher help output.
- No production section recommends WSL, `bootRun`, or `SPRING_DATA_MONGODB_URI`.

#### Code Edit 8.2
- File: `docs/operations/windows-production.md`
- Lines: after 0
- Action: add

Proposed:
```markdown
# Native Windows Production Operations

This runbook is the source of truth for prerequisites, ProgramData layout,
WinSW provenance, first installation, configuration and ACLs, WSL-to-Windows
MongoDB migration, candidate validation, daily deployment, service status,
logs, release listing, rollback, backup, restore, failed-deployment recovery,
native development, upgrades, uninstall, WSL fallback, soak closure, and the
full reboot acceptance checklist.

Never delete the WSL database or verified archives during migration. Any
collection-count or index mismatch blocks cutover. Production never leaves port
8080 until the port-8081 candidate passes.
```

Verification:
- Follow the runbook on a clean test installation and record every command/output needed to complete install, migration rehearsal, rollback, and reboot acceptance.

#### Code Edit 8.3
- File: `docs/operations/mongodb-backup-restore.md`
- Lines: 1-154
- Action: replace

Current:
```markdown
# MongoDB Backup and Restore Runbook

Use this runbook for production MongoDB backups, restore preparation, and
restore smoke checks for `christopherbell.dev`. Run the commands from a host
that has network access to MongoDB and the MongoDB Database Tools installed.

The current document uses Bash environment variables, `/var/backups`,
`mongodump`, and `mongorestore` commands for the former WSL runtime.
```

Proposed:
```markdown
# MongoDB Backup and Restore Runbook

Native Windows production backups are created with `.\prod.cmd backup` under
`C:\ProgramData\christopherbell.dev\backups`. Each compressed archive must be
non-empty, pass `mongorestore.exe --dryRun`, and have a recorded SHA-256 hash.

Restore into `christopherbell_restore_check` first, compare collection counts
and indexes, and run the application on a non-production port. Restoring into
`christopherbell` requires a maintenance window and explicit target
confirmation. The WSL source and `A:\Projects\christopherbell.dev-backups`
archives remain fallback evidence until migration soak closure.
```

Verification:
- Execute native backup and validation-restore commands against Windows MongoDB and confirm the runbook captures archive path, hash, counts, indexes, and HTTP smoke evidence.

### Task 9 - Execute migration rehearsal and controlled native cutover

Sequence / dependencies:
- Runs only after Tasks 1-8 pass automated review and merge through a PR.
- Requires a fresh production backup and explicit maintenance-window announcement.

Implementation notes:
- Run `prod install -WhatIf`, `prod migrate -WhatIf`, and `prod deploy -WhatIf` first.
- Install native tools/services without touching WSL production port 8080.
- Restore to the Windows validation database and exercise the native candidate on port 8081.
- Freeze writes only for the final fresh backup/inventory and final restore.
- Do not delete WSL data or disable the WSL MongoDB service during cutover.

Verification:
- Fresh WSL archive is non-empty, dry-run readable, and SHA-256 recorded.
- Source and Windows validation inventories match collection-for-collection and index-for-index.
- Native candidate returns home 200, Mongo-backed read success, and `INVALID_TOKEN` for the configured known account with a wrong diagnostic password.
- Windows production returns the same results on port 8080.
- Native `MongoDB` and `ChristopherBellDev` services report Running and Automatic.
- Rehearse application rollback and WSL migration rollback before ending the maintenance window.

### Task 10 - Prove boot persistence, publish, and close the migration

Sequence / dependencies:
- Runs after Task 9 native cutover is stable.

Implementation notes:
- Reboot the Windows computer during an approved window without logging in immediately.
- Verify externally or after delayed login that both services started at boot and port 8080 became available.
- Monitor through the soak period before explicitly retiring WSL production components.
- Open a PR, wait for all CI/CodeQL gates, merge, and preserve test/migration evidence in Builder.

Verification:
- `Get-Service MongoDB,ChristopherBellDev` reports Running/Automatic after reboot.
- `Get-CimInstance Win32_Service` shows service start times preceding interactive login where observable.
- Home returns HTTP 200 and the known-account diagnostic returns `INVALID_TOKEN`.
- Native MongoDB inventory still matches the frozen migration inventory.
- `prod deploy` successfully deploys a subsequent no-op/current `origin/main` release or reports it already active without downtime.
- Save a Builder test report, spoke review, closure record, and session memory; update indexes and validate hub state.

## Code Changes

- `website/src/main/java/dev/christopherbell/Application.java`: remove unconditional scheduling.
- `website/src/main/java/dev/christopherbell/configuration/SchedulingConfiguration.java`: add property-controlled scheduling.
- `website/src/main/resources/application-deploy-smoke.yml`: add mutation-free candidate profile.
- `website/src/test/java/dev/christopherbell/configuration/*`: add scheduling/profile regression coverage.
- `prod.cmd`, `Makefile`: add operator command interfaces.
- `ops/production/windows/prod.ps1`: add command dispatcher.
- `ops/production/windows/modules/*.psm1`: add common, deploy, install, migration, and operations logic.
- `ops/production/windows/service/*`: add WinSW configuration and secret-safe Java launcher.
- `ops/production/windows/config/*`: add non-secret configuration examples.
- `ops/production/windows/tests/*.Tests.ps1`: add Pester coverage.
- `README.md`: replace WSL/manual production instructions.
- `docs/operations/windows-production.md`: add complete native Windows operations runbook.
- `docs/operations/mongodb-backup-restore.md`: replace WSL-first backup/restore instructions with native Windows workflow and fallback preservation.

## Files and Modules

- Spring configuration: `website/src/main/java/dev/christopherbell/configuration`, `website/src/main/resources`.
- Windows command surface: `prod.cmd`, optional `Makefile`.
- Deployment implementation: `ops/production/windows`.
- Service artifacts: `ops/production/windows/service`.
- PowerShell tests: `ops/production/windows/tests`.
- Operations documentation: `README.md`, `docs/operations`.
- External runtime state: `C:\ProgramData\christopherbell.dev`, Windows services, native MongoDB data directory.
- Preserved fallback state: Debian WSL MongoDB and `A:\Projects\christopherbell.dev-backups`.

## Unit Testing

- Use Pester 5 to test PowerShell modules in `$TestDrive` with mocked/stubbed Git, Gradle, Java, service, MongoDB tools, junction, and HTTP commands.
- Pin the development/test prerequisite to Pester 5.x and document `Install-Module Pester -Scope CurrentUser -MinimumVersion 5.0 -MaximumVersion 5.99` when it is absent; production runtime commands must not require Pester.
- Observe failing tests before implementing each module.
- Required command: `Invoke-Pester ops/production/windows/tests -Output Detailed`.
- Run targeted Java tests:
  - `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.SchedulingConfigurationTest`
  - `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.MongoProfileConfigurationTest`
- Run PowerShell syntax analysis for every `.ps1` and `.psm1` using the PowerShell parser API.
- Run `gradlew.bat --no-daemon :website:build` with explicit `NODE_EXE` and deployment-local `GRADLE_USER_HOME`.

## Local Testing

- Run all `prod` commands with `-WhatIf` before elevated host changes.
- Start the merged candidate natively on port 8081 with profiles `prod,deploy-smoke`.
- Send `GET /` and expect HTTP 200.
- Send a MongoDB-backed read request and record response/status.
- Send a login request for the configured smoke email with a deliberately invalid password; expect HTTP 401 and `INVALID_TOKEN`, never 404 `RESOURCE_NOT_FOUND`.
- Confirm no startup import or scheduled mutation starts in candidate logs.
- Restore the fresh archive into `christopherbell_restore_check`, compare canonical inventories, and run the candidate against it.
- Install services, test stop/start/recovery, switch releases, and rehearse rollback.
- Perform a controlled Windows reboot and verify automatic startup without interactive login.

## Validation

- All Java, JavaScript, and Pester tests pass.
- Git worktree remains clean and unrelated checkout changes are preserved.
- WinSW download hash matches the pinned SHA-256 before installation.
- No secrets appear in Git diff, process command lines, service XML, release metadata, or logs.
- `prod deploy` proves the deployed SHA equals freshly fetched `origin/main`.
- Candidate and production checks prove the app reads native Windows `christopherbell`.
- Frozen WSL source and final Windows MongoDB inventories match exactly.
- Automatic rollback restores a known-good release after an induced verification failure.
- Windows reboot proves boot-started MongoDB and website services.
- PR CI and CodeQL pass before merge.

## Rollback or Recovery

- Before migration: retain the current WSL site, WSL MongoDB, fresh compressed archive, JSON exports, checksum, and inventory.
- Candidate failure: stop candidate and leave production untouched.
- Native application failure after switch: atomically restore `previous`, restart `ChristopherBellDev`, and verify.
- Mongo migration mismatch: stop native candidate, preserve validation database for inspection, and resume WSL production without changing source data.
- Native cutover failure: stop Windows website service and MongoDB service, restart WSL MongoDB/site, and verify the original account/data counts.
- Reboot failure: start services manually, collect Service Control Manager/WinSW/MongoDB logs, and keep WSL fallback available.
- Uninstall defaults to removing only `ChristopherBellDev`; MongoDB data, backups, secrets, and releases require separate explicit confirmation.

## Risks

- MongoDB data loss or divergence during cutover: mitigate with a write freeze, fresh archive, dry-run restore, canonical collection/index inventory, validation database, and untouched WSL fallback.
- Windows service secrets exposure: mitigate with allowlisted environment loading, restrictive ACLs, no secret arguments, and diff/process/log scans.
- WinSW supply-chain risk: pin v2.12.0 and verify exact SHA-256 before installation.
- Native tool path drift: validate Java, Node, Git, MongoDB tools, and PowerShell paths during install and every deploy.
- Gradle daemon/cache contention: use deployment-local `GRADLE_USER_HOME` and `--no-daemon`.
- Candidate mutating production: use `deploy-smoke`, disable scheduling and WFL startup catch-up, and assert logs.
- Junction mistakes: resolve and validate every target under the configured releases root before delete/move/switch.
- Windows reboot interrupts the development host: require an explicit maintenance window and verified backups first.
- Service account lacks filesystem/network privileges: validate ACLs, MongoDB access, mail/network access, and temp-file behavior before cutover.
- Native and WSL MongoDB both binding 27017: stop/disable the non-target service at each controlled phase and identify the listener PID/service before testing.

## Completion Criteria

- The native-Windows design and this plan are reviewed and approved.
- Implementation is merged through a PR with all CI and CodeQL checks passing.
- `prod` command interface and optional Make aliases are documented and tested.
- Native MongoDB and `ChristopherBellDev` run as Automatic Windows services.
- Final Windows MongoDB inventory matches the frozen WSL source exactly.
- Native candidate and production smoke checks pass without data mutation.
- Deployment from latest `origin/main`, automatic rollback, manual rollback, backup, logs, status, restart, retention, and uninstall are verified.
- A full Windows reboot proves both services and port 8080 start without user login.
- WSL production state remains intact through the agreed soak period and is retired only by a separately confirmed cleanup step.
- Builder test report, spoke review, closure, session memory, indexes, and validation are complete and pushed.
