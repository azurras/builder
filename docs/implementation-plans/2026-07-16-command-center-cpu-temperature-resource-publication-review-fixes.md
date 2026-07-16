# Command Center CPU Temperature Resource Publication Review Fixes

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the pre-merge resource-liveness and concurrent-candidate findings so exactly one visible sensor directory is always complete, fresh, and owned by the production process.

**Architecture:** Extract into a protected directory whose name cannot match the operational verifier, then atomically publish the fully verified directory into the matching namespace. Hold an exclusive cross-process file lease for the entire live-resource lifetime, delete every matching sibling except the published directory, and force deployment candidates to keep native sensors disabled. The PowerShell waiter remains exact-one but uses a monotonic bounded timeout.

**Tech Stack:** Java 25 NIO channels and atomic moves, JUnit 5, AssertJ, PowerShell 7, Pester 5, Gradle, Windows services, PawnIO 2.2.0.0, LibreHardwareMonitor 0.9.6.

## Global Constraints

- Do not expose a matching directory before all pinned resources are copied, checksum-verified, and ACL-hardened.
- Publish only with `StandardCopyOption.ATOMIC_MOVE`; fail closed if atomic publication is unavailable.
- Hold one exclusive file lease beneath the protected base until `NativeLibraries.close()`.
- Publish a protected current-Java-PID and process-start owner marker only after stale cleanup succeeds.
- Delete only validated current-version siblings and abandoned nonmatching staging directories.
- Force `COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED=false` for every deployment candidate.
- Keep the verifier wait at 15 seconds with at most 250 milliseconds per sleep.
- Preserve all existing ACL, checksum, Defender, PawnIO, and rollback gates.

---

## Document Status

`ready-for-execution`

## Objective

Amend commit `3be9fa6fb5790368b0d83d30d273ea56b997c3f7` so independent review reports no Important findings and production can converge from six stale directories to one complete live directory without cross-process deletion.

## Goals

- Observe candidate-isolation, nonmatching-staging, and exclusive-lease tests fail against the current commit.
- Prevent the PowerShell verifier from seeing incomplete fresh resources or a transient final stale directory.
- Prevent a sole stale directory from being accepted before the new process publishes its owner marker.
- Prevent a candidate or second process from deleting resources owned by the production service.
- Use a monotonic timeout and clamp the final wait interval.
- Re-run complete local verification and independent review before publishing.
- Preserve the production acceptance and Builder closure steps from the superseded plan.

## Inputs

- Spec: `docs/specs/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md`
- Superseded plan: `docs/implementation-plans/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md`
- Independent review findings against `3be9fa6f`.
- Current branch: `codex/cpu-temperature-stale-resources`
- Current worktree: `A:\Projects\christopherbell.dev-worktrees\winsw-log-rotation-recovery-merged`

## Branch

- Base: `origin/main` at `d33a2c41e1e9b23c4b313ff6fb19ac389f8d7699`
- Branch: `codex/cpu-temperature-stale-resources`
- Current amendable commit: `3be9fa6fb5790368b0d83d30d273ea56b997c3f7`

## Non-Goals

- No provider upgrade or PawnIO reinstall.
- No generic cleanup command.
- No public API or UI change.
- No manual deletion of the six protected production directories.
- No reboot, shutdown, MongoDB, cloudflared, or WinSW change.

## Assumptions

- The sensor base and lease file are writable only by SYSTEM and Administrators.
- NTFS supports atomic same-parent directory rename.
- The supported deployment path is the only intentional parallel application process and will be explicitly sensor-disabled.
- OS process termination releases the file lease.

## Open Questions

None.

## Task Breakdown

### Task 1 - Disable native sensors in deployment candidates

Sequence / dependencies:
- Runs first because the existing candidate path is a proven concurrent prod-profile process.

Implementation notes:
- Preserve any optional restore-check database override.
- Add the native sensor override unconditionally.

#### Code Edit 1.1
- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: after 37
- Action: add

Proposed:
```powershell
        It 'forces native sensor libraries off in deployment candidates' {
            $process = [pscustomobject]@{ Id=1234; HasExited=$true }
            $process | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value {
                param($milliseconds) $true
            }
            Mock Start-ProductionJar { $process }
            Mock Test-ProductionEndpoints {}
            $config = [pscustomobject]@{ candidatePort=8081 }

            Test-CandidateRelease $config 'C:\data\releases\new' 'restore_check'

            Should -Invoke Start-ProductionJar -Times 1 -Exactly -ParameterFilter {
                $AdditionalEnvironment.COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED -eq 'false' -and
                $AdditionalEnvironment.SPRING_MONGODB_DATABASE -eq 'restore_check'
            }
        }
```

Verification:
- Run focused `Production.Deploy.Tests.ps1`.
- Expect one failure because the current candidate environment omits the native sensor override.

#### Code Edit 1.2
- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 74-78
- Action: replace

Current:
```powershell
function Test-CandidateRelease {
    param($Config, [Parameter(Mandatory)][string]$Release, [string]$Database)
    $additionalEnvironment = @{}
    if (-not [string]::IsNullOrWhiteSpace($Database)) { $additionalEnvironment.SPRING_MONGODB_DATABASE = $Database }
    $process = Start-ProductionJar -Config $Config -Release $Release -Port $Config.candidatePort -Profiles 'prod,deploy-smoke' -AdditionalEnvironment $additionalEnvironment
```

Proposed:
```powershell
function Test-CandidateRelease {
    param($Config, [Parameter(Mandatory)][string]$Release, [string]$Database)
    $additionalEnvironment = @{
        COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED = 'false'
    }
    if (-not [string]::IsNullOrWhiteSpace($Database)) {
        $additionalEnvironment.SPRING_MONGODB_DATABASE = $Database
    }
    $process = Start-ProductionJar -Config $Config -Release $Release -Port $Config.candidatePort -Profiles 'prod,deploy-smoke' -AdditionalEnvironment $additionalEnvironment
```

Verification:
- Re-run focused deploy Pester and expect green.

- [ ] **Step 1: Add Code Edit 1.1 only and observe red.**
- [ ] **Step 2: Apply Code Edit 1.2 and observe green.**

### Task 2 - Publish complete resources atomically under an exclusive lease

Sequence / dependencies:
- Runs after Task 1.
- Follow Java red-green-refactor.

Implementation notes:
- Extend the existing stale cleanup rather than adding a second unbounded cleanup mechanism.
- Use a nonmatching staging prefix and clean abandoned staging siblings only after the lease is acquired.
- Return final paths after the atomic rename; do not retain staging paths.
- Release the lease only after best-effort live-directory cleanup.

#### Code Edit 2.1
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: 27-45
- Action: replace

Current:
```java
  @Test
  void removesStaleVersionDirectoryBeforeProvisioningFreshResources() throws Exception {
    Path stale = Files.createDirectories(
        tempDir.resolve("librehardwaremonitor-0.9.6-stale"));
    Files.writeString(stale.resolve("LibreHardwareMonitorLib.dll"), "malicious", UTF_8);
    var provisioner = provisionerWithLibraryCompanionAndScript(path -> {}, "fresh");

    var libraries = provisioner.provision();

    assertThat(stale).doesNotExist();
    assertThat(libraries.directory().getFileName().toString())
        .isEqualTo("librehardwaremonitor-0.9.6-fresh");
    assertThat(Files.readString(libraries.libreHardwareMonitor(), UTF_8))
        .isEqualTo("trusted");
    libraries.close();
  }
```

Proposed:
```java
  @Test
  void publishesCompleteFreshResourcesBeforeRetiringStaleSiblings() throws Exception {
    Path stale = Files.createDirectories(
        tempDir.resolve("librehardwaremonitor-0.9.6-stale"));
    Files.writeString(stale.resolve("LibreHardwareMonitorLib.dll"), "malicious", UTF_8);
    Path fresh = tempDir.resolve("librehardwaremonitor-0.9.6-fresh");
    boolean[] finalVisibleDuringCopy = {false};
    boolean[] finalCompleteDuringCleanup = {false};
    boolean[] ownerMarkerVisibleDuringCleanup = {false};
    var provisioner = provisionerWithLibraryCompanionAndScript(path -> {
      if (path.equals(stale)) {
        finalCompleteDuringCleanup[0] =
            Files.exists(fresh.resolve("LibreHardwareMonitorLib.dll"))
                && Files.exists(fresh.resolve("cpu-temperature.ps1"));
        ownerMarkerVisibleDuringCleanup[0] =
            Files.exists(fresh.resolve("live-owner.pid"));
      }
    }, "fresh", () -> finalVisibleDuringCopy[0] |= Files.exists(fresh));

    var libraries = provisioner.provision();

    assertThat(finalVisibleDuringCopy[0]).isFalse();
    assertThat(finalCompleteDuringCleanup[0]).isTrue();
    assertThat(ownerMarkerVisibleDuringCleanup[0]).isFalse();
    assertThat(stale).doesNotExist();
    assertThat(libraries.directory()).isEqualTo(fresh);
    assertThat(Files.readString(libraries.libreHardwareMonitor(), UTF_8))
        .isEqualTo("trusted");
    String marker = Files.readString(fresh.resolve("live-owner.pid"), UTF_8);
    assertThat(marker).contains("pid=" + ProcessHandle.current().pid());
    assertThat(marker).contains("startedAtEpochMillis=");
    libraries.close();
  }
```

Verification:
- Run the single test and expect red because the current final matching directory exists during resource copy and stale cleanup happens before it is complete.

#### Code Edit 2.2
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: after 45
- Action: add

Proposed:
```java
  @Test
  void holdsExclusiveLeaseForTheOwnedResourceLifetime() throws Exception {
    var first = provisionerWithLibraryCompanionAndScript(path -> {}, "first");
    var second = provisionerWithLibraryCompanionAndScript(path -> {}, "second");
    var firstLibraries = first.provision();

    assertThatThrownBy(second::provision)
        .isInstanceOf(SecurityException.class)
        .hasMessageContaining("already in use");

    firstLibraries.close();
    var secondLibraries = second.provision();
    secondLibraries.close();
  }
```

Verification:
- Before production changes, expect red because the second provisioner deletes the first directory and succeeds.

#### Code Edit 2.3
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: 80-92
- Action: replace

Current:
```java
  private SecureNativeLibraryProvisioner provisionerWithLibraryCompanionAndScript(
      SecureNativeLibraryProvisioner.AclPolicy acl,
      String nonce) {
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

Proposed:
```java
  private SecureNativeLibraryProvisioner provisionerWithLibraryCompanionAndScript(
      SecureNativeLibraryProvisioner.AclPolicy acl,
      String nonce) {
    return provisionerWithLibraryCompanionAndScript(acl, nonce, () -> {});
  }

  private SecureNativeLibraryProvisioner provisionerWithLibraryCompanionAndScript(
      SecureNativeLibraryProvisioner.AclPolicy acl,
      String nonce,
      Runnable beforeResourceCopy) {
    return new SecureNativeLibraryProvisioner(
        tempDir,
        List.of(
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "LibreHardwareMonitorLib.dll", hash("trusted"), () -> {
                  beforeResourceCopy.run();
                  return new ByteArrayInputStream("trusted".getBytes(UTF_8));
                }),
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "HidSharp.dll", hash("trusted-hid"), () -> {
                  beforeResourceCopy.run();
                  return new ByteArrayInputStream("trusted-hid".getBytes(UTF_8));
                }),
            new SecureNativeLibraryProvisioner.ResourceSpec(
                "cpu-temperature.ps1", hash("trusted-script"), () -> {
                  beforeResourceCopy.run();
                  return new ByteArrayInputStream("trusted-script".getBytes(UTF_8));
                })),
        acl,
        () -> nonce);
  }
```

Verification:
- Compile and run the complete provisioner test class after production edits.

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: after 2
- Action: add

Proposed:
```java
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.nio.channels.OverlappingFileLockException;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
```

Verification:
- Compile through the focused Gradle test.

#### Code Edit 2.5
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 27-32
- Action: replace

Current:
```java
  static final String VERSION = "0.9.6";
  private static final String DIRECTORY_PREFIX = "librehardwaremonitor-" + VERSION + "-";
  private static final String VALID_DIRECTORY_NAME =
      java.util.regex.Pattern.quote(DIRECTORY_PREFIX) + "[A-Za-z0-9-]{1,64}";
```

Proposed:
```java
  static final String VERSION = "0.9.6";
  private static final String DIRECTORY_PREFIX = "librehardwaremonitor-" + VERSION + "-";
  private static final String STAGING_PREFIX = ".librehardwaremonitor-" + VERSION + "-";
  private static final String STAGING_SUFFIX = "-staging";
  private static final String LEASE_FILE = "librehardwaremonitor.lock";
  private static final String VALID_DIRECTORY_NAME =
      java.util.regex.Pattern.quote(DIRECTORY_PREFIX) + "[A-Za-z0-9-]{1,64}";
  private static final String VALID_STAGING_NAME =
      java.util.regex.Pattern.quote(STAGING_PREFIX)
          + "[A-Za-z0-9-]{1,64}"
          + STAGING_SUFFIX;
```

Verification:
- Compile through the focused Gradle test.

#### Code Edit 2.6
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 60-114
- Action: replace

Current:
```java
  NativeLibraries provision() {
    // Current cleanup-before-create implementation.
  }
```

Proposed:
```java
  NativeLibraries provision() {
    String nonce = nonceSupplier.get();
    if (nonce == null || !nonce.matches("[A-Za-z0-9-]{1,64}")) {
      throw new SecurityException("Invalid native library extraction nonce.");
    }
    Path versionDirectory = baseDirectory.resolve(DIRECTORY_PREFIX + nonce);
    Path stagingDirectory =
        baseDirectory.resolve(STAGING_PREFIX + nonce + STAGING_SUFFIX);
    Path ownedDirectory = null;
    SensorLease lease = null;
    try {
      createTrustedBaseDirectory();
      verifyNotLinkOrReparsePoint(baseDirectory);
      aclPolicy.hardenAndVerify(baseDirectory);
      lease = acquireSensorLease();
      removeOwnedDirectories(
          STAGING_PREFIX + "*",
          VALID_STAGING_NAME,
          null);
      Files.createDirectory(stagingDirectory);
      ownedDirectory = stagingDirectory;
      verifyNotLinkOrReparsePoint(stagingDirectory);
      aclPolicy.hardenAndVerify(stagingDirectory);
      Path libre = null;
      Path cpuTemperatureScript = null;
      for (var resource : resources) {
        Path target = stagingDirectory.resolve(resource.fileName()).normalize();
        if (!target.getParent().equals(stagingDirectory)) {
          throw new SecurityException("Invalid bundled native library name.");
        }
        try (InputStream input = resource.input().get()) {
          if (input == null) {
            throw new SecurityException("Bundled native library is missing.");
          }
          Files.copy(input, target);
        }
        verifyNotLinkOrReparsePoint(target);
        if (!resource.expectedSha256().equalsIgnoreCase(sha256(target))) {
          throw new SecurityException("Bundled native library checksum mismatch.");
        }
        aclPolicy.hardenAndVerify(target);
        if (!resource.expectedSha256().equalsIgnoreCase(sha256(target))) {
          throw new SecurityException("Native library changed after ACL hardening.");
        }
        if (resource.fileName().equals("LibreHardwareMonitorLib.dll")) {
          libre = target;
        } else if (resource.fileName().equals("cpu-temperature.ps1")) {
          cpuTemperatureScript = target;
        }
      }
      if (libre == null || cpuTemperatureScript == null) {
        throw new SecurityException("Required CPU sensor resources are missing.");
      }
      Files.move(stagingDirectory, versionDirectory, StandardCopyOption.ATOMIC_MOVE);
      ownedDirectory = versionDirectory;
      verifyNotLinkOrReparsePoint(versionDirectory);
      aclPolicy.hardenAndVerify(versionDirectory);
      Path finalLibre = versionDirectory.resolve(libre.getFileName());
      Path finalScript = versionDirectory.resolve(cpuTemperatureScript.getFileName());
      removeOwnedDirectories(DIRECTORY_PREFIX + "*", VALID_DIRECTORY_NAME, versionDirectory);
      return NativeLibraries.owned(
          versionDirectory, finalLibre, finalScript, lease);
    } catch (IOException | RuntimeException failure) {
      if (ownedDirectory != null) deleteTree(ownedDirectory);
      if (lease != null) lease.close();
      if (failure instanceof SecurityException securityException) {
        throw securityException;
      }
      throw new SecurityException("Secure native library provisioning failed.", failure);
    }
  }
```

Verification:
- Run the two new focused Java tests and expect green after Code Edits 2.7 through 2.9.

#### Code Edit 2.7
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 129-144
- Action: replace

Current:
```java
  private void removeStaleVersionDirectories() throws IOException {
    // Current matching-directory cleanup.
  }
```

Proposed:
```java
  private void removeOwnedDirectories(
      String glob,
      String validNamePattern,
      Path excludedDirectory) throws IOException {
    var trees = new ArrayList<List<Path>>();
    try (var candidates = Files.newDirectoryStream(baseDirectory, glob)) {
      for (Path candidate : candidates) {
        Path normalized = candidate.toAbsolutePath().normalize();
        if (!baseDirectory.equals(normalized.getParent())
            || !normalized.getFileName().toString().matches(validNamePattern)) {
          throw new SecurityException("Invalid native library resource directory.");
        }
        if (excludedDirectory != null && excludedDirectory.equals(normalized)) {
          continue;
        }
        verifyNotLinkOrReparsePoint(normalized);
        if (!Files.isDirectory(normalized, LinkOption.NOFOLLOW_LINKS)) {
          throw new SecurityException("Native library resource is not a directory.");
        }
        var tree = new ArrayList<Path>();
        collectTrustedTree(normalized, tree);
        trees.add(tree);
      }
    }
    for (List<Path> tree : trees) {
      tree.sort(java.util.Comparator.reverseOrder());
      for (Path path : tree) {
        Files.delete(path);
      }
    }
  }
```

Verification:
- Tests must prove the final directory is excluded and all stale siblings are removed.

#### Code Edit 2.8
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: before 171
- Action: add

Proposed:
```java
  private SensorLease acquireSensorLease() throws IOException {
    Path leasePath = baseDirectory.resolve(LEASE_FILE);
    if (Files.exists(leasePath, LinkOption.NOFOLLOW_LINKS)) {
      verifyNotLinkOrReparsePoint(leasePath);
    } else {
      try {
        Files.createFile(leasePath);
      } catch (java.nio.file.FileAlreadyExistsException ignored) {
        verifyNotLinkOrReparsePoint(leasePath);
      }
    }
    verifyNotLinkOrReparsePoint(leasePath);
    aclPolicy.hardenAndVerify(leasePath);
    FileChannel channel = FileChannel.open(leasePath, StandardOpenOption.WRITE);
    try {
      FileLock lock = channel.tryLock();
      if (lock == null) {
        channel.close();
        throw new SecurityException("CPU sensor resources are already in use.");
      }
      return new SensorLease(channel, lock);
    } catch (OverlappingFileLockException failure) {
      channel.close();
      throw new SecurityException("CPU sensor resources are already in use.", failure);
    }
  }
```

Verification:
- The exclusive-lease test must fail the second provisioner and allow it after the first closes.

#### Code Edit 2.9
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 228-262
- Action: replace

Current:
```java
  static final class NativeLibraries implements AutoCloseable {
    // Current fields, constructors, owned factories, and close.
  }
```

Proposed:
```java
  static final class NativeLibraries implements AutoCloseable {
    private final Path directory;
    private final Path libreHardwareMonitor;
    private final Path cpuTemperatureScript;
    private final boolean owned;
    private final SensorLease lease;

    NativeLibraries(Path directory, Path libreHardwareMonitor) {
      this(directory, libreHardwareMonitor, directory.resolve("cpu-temperature.ps1"), false, null);
    }

    NativeLibraries(Path directory, Path libreHardwareMonitor, Path cpuTemperatureScript) {
      this(directory, libreHardwareMonitor, cpuTemperatureScript, false, null);
    }

    private NativeLibraries(
        Path directory,
        Path libreHardwareMonitor,
        Path cpuTemperatureScript,
        boolean owned,
        SensorLease lease) {
      this.directory = directory;
      this.libreHardwareMonitor = libreHardwareMonitor;
      this.cpuTemperatureScript = cpuTemperatureScript;
      this.owned = owned;
      this.lease = lease;
    }

    static NativeLibraries owned(
        Path directory, Path libre, Path script, SensorLease lease) {
      return new NativeLibraries(directory, libre, script, true, lease);
    }

    Path directory() { return directory; }
    Path libreHardwareMonitor() { return libreHardwareMonitor; }
    Path cpuTemperatureScript() { return cpuTemperatureScript; }

    @Override
    public void close() {
      if (owned) deleteTree(directory);
      if (lease != null) lease.close();
    }
  }

  private static final class SensorLease implements AutoCloseable {
    private final FileChannel channel;
    private final FileLock lock;

    private SensorLease(FileChannel channel, FileLock lock) {
      this.channel = channel;
      this.lock = lock;
    }

    @Override
    public void close() {
      try {
        if (lock.isValid()) lock.release();
      } catch (IOException ignored) {
      } finally {
        try {
          channel.close();
        } catch (IOException ignored) {
        }
      }
    }
  }
```

Verification:
- Run the complete `SecureNativeLibraryProvisionerTest`.
- Run `git diff --check`.

#### Code Edit 2.10
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: after 128
- Action: add

Proposed:
```java
      publishOwnerMarker(versionDirectory);
```

```java
  private void publishOwnerMarker(Path directory) throws IOException {
    long ownerPid = ProcessHandle.current().pid();
    long startedAtEpochMillis = ProcessHandle.current().info().startInstant()
        .orElseThrow(() -> new SecurityException(
            "CPU sensor owner process start time is unavailable."))
        .toEpochMilli();
    String owner = "pid=" + ownerPid + System.lineSeparator()
        + "startedAtEpochMillis=" + startedAtEpochMillis + System.lineSeparator();
    Path stagingMarker = directory.resolve(".live-owner.pid-staging");
    Path ownerMarker = directory.resolve("live-owner.pid");
    Files.writeString(
        stagingMarker,
        owner,
        java.nio.charset.StandardCharsets.US_ASCII,
        StandardOpenOption.CREATE_NEW,
        StandardOpenOption.WRITE);
    verifyNotLinkOrReparsePoint(stagingMarker);
    aclPolicy.hardenAndVerify(stagingMarker);
    if (!owner.equals(Files.readString(
        stagingMarker, java.nio.charset.StandardCharsets.US_ASCII))) {
      throw new SecurityException("CPU sensor owner marker changed before publication.");
    }
    Files.move(stagingMarker, ownerMarker, StandardCopyOption.ATOMIC_MOVE);
    verifyNotLinkOrReparsePoint(ownerMarker);
    aclPolicy.hardenAndVerify(ownerMarker);
    if (!owner.equals(Files.readString(
        ownerMarker, java.nio.charset.StandardCharsets.US_ASCII))) {
      throw new SecurityException("CPU sensor owner marker changed after publication.");
    }
  }
```

Verification:
- The publication test must prove the marker is absent during cleanup and equals the current JVM PID after provisioning returns.

- [ ] **Step 1: Apply Code Edits 2.1 through 2.3 only and observe red.**
- [ ] **Step 2: Apply Code Edits 2.4 through 2.9.**
- [ ] **Step 3: Run the focused tests and expect green.**

### Task 3 - Make the exact-one wait monotonic and bounded

Sequence / dependencies:
- Runs after Java publication is green.

Implementation notes:
- Preserve immediate success when one complete published directory exists.
- Do not accept success after the timeout has elapsed.
- Clamp the final sleep to the remaining duration.

#### Code Edit 3.1
- File: `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- Lines: after 186
- Action: add

Proposed:
```powershell
        It 'clamps a nonzero unresolved wait to the remaining monotonic timeout' {
            Mock Test-Path { $true }
            Mock Get-ChildItem {
                @(
                    [pscustomobject]@{ FullName='C:\sensors\stale-a' },
                    [pscustomobject]@{ FullName='C:\sensors\stale-b' })
            }
            $elapsed = Measure-Command {
                {
                    Wait-ProductionSensorResourceDirectory `
                        -Base 'C:\sensors' `
                        -Timeout ([timespan]::FromMilliseconds(20)) `
                        -PollMilliseconds 250
                } | Should -Throw '*found 2*'
            }
            $elapsed.TotalMilliseconds | Should -BeLessThan 200
        }
```

Verification:
- Expect the test to take approximately the current full 250-millisecond sleep and fail the `<200` assertion.

#### Code Edit 3.2
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: 82-108
- Action: replace

Current:
```powershell
function Wait-ProductionSensorResourceDirectory {
    # Current wall-clock implementation.
}
```

Proposed:
```powershell
function Wait-ProductionSensorResourceDirectory {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Base,
        [Parameter(Mandatory)][int]$OwnerPid,
        [Parameter(Mandatory)][datetime]$OwnerStartedAt,
        [timespan]$Timeout = ([timespan]::FromSeconds(15)),
        [ValidateRange(1,5000)][int]$PollMilliseconds = 250
    )

    $stopwatch = [Diagnostics.Stopwatch]::StartNew()
    $observedCount = 0
    while ($true) {
        $allDirectories = if (Test-Path -LiteralPath $Base -PathType Container) {
            @(Get-ChildItem -LiteralPath $Base -Directory `
                -Filter 'librehardwaremonitor-0.9.6-*' -ErrorAction Stop)
        } else {
            @()
        }
        $directories = @($allDirectories | Where-Object {
            Test-ProductionSensorOwnerMarker `
                -Directory $_ `
                -OwnerPid $OwnerPid `
                -OwnerStartedAt $OwnerStartedAt
        })
        $observedCount = $directories.Count
        $remainingMilliseconds = $Timeout.TotalMilliseconds - $stopwatch.Elapsed.TotalMilliseconds
        if ($observedCount -eq 1 -and $remainingMilliseconds -ge 0) {
            return $directories[0]
        }
        if ($remainingMilliseconds -le 0) {
            throw "Expected exactly one live CPU temperature resource directory; found $observedCount live of $($allDirectories.Count) total."
        }
        Start-Sleep -Milliseconds ([int][math]::Ceiling(
            [math]::Min($PollMilliseconds, $remainingMilliseconds)))
    }
}
```

Verification:
- Re-run focused sensor Pester and expect green.

#### Code Edit 3.3
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: before 82
- Action: add

Proposed:
```powershell
function Test-ProductionSensorOwnerMarker {
    param(
        [Parameter(Mandatory)]$Directory,
        [Parameter(Mandatory)][int]$OwnerPid,
        [Parameter(Mandatory)][datetime]$OwnerStartedAt
    )
    $marker = Join-Path $Directory.FullName 'live-owner.pid'
    if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) {
        return $false
    }
    $raw = Get-Content -LiteralPath $marker -ErrorAction Stop
    $values = @{}
    foreach ($line in $raw) {
        if ($line -match '^([A-Za-z]+)=(\d+)$') {
            $values[$Matches[1]] = $Matches[2]
        }
    }
    [long]$markerPid = 0
    [long]$markerStartedAt = 0
    if (-not [long]::TryParse([string]$values.pid, [ref]$markerPid) -or
        -not [long]::TryParse([string]$values.startedAtEpochMillis, [ref]$markerStartedAt)) {
        return $false
    }
    $markerStart = [DateTimeOffset]::FromUnixTimeMilliseconds($markerStartedAt).UtcDateTime
    $delta = [math]::Abs(($markerStart - $OwnerStartedAt.ToUniversalTime()).TotalMilliseconds)
    return $markerPid -eq $OwnerPid -and $delta -le 1000
}
```

Verification:
- Add Pester coverage showing an old PID marker is ignored and the current PID marker is selected.

#### Code Edit 3.4
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: 110-118
- Action: replace

Current:
```powershell
    $base = Join-Path $Root 'config\command-center-sensors'
    $directory = (
        Wait-ProductionSensorResourceDirectory -Base $base
    ).FullName
```

Proposed:
```powershell
    $config = Get-Content -LiteralPath (Join-Path $Root 'config\deploy.json') -Raw |
        ConvertFrom-Json
    $listeners = @(
        Get-NetTCPConnection -LocalPort ([int]$config.productionPort) `
            -State Listen -ErrorAction SilentlyContinue
    )
    if ($listeners.Count -ne 1) {
        throw "Expected exactly one production listener for CPU sensor ownership; found $($listeners.Count)."
    }
    $base = Join-Path $Root 'config\command-center-sensors'
    $ownerProcess = Get-Process -Id ([int]$listeners[0].OwningProcess) -ErrorAction Stop
    $directory = (
        Wait-ProductionSensorResourceDirectory `
            -Base $base `
            -OwnerPid ([int]$listeners[0].OwningProcess) `
            -OwnerStartedAt $ownerProcess.StartTime
    ).FullName
```

Verification:
- Existing direct-probe verification must use only the resource directory owned by the current production Java listener.

- [ ] **Step 1: Add Code Edit 3.1 only and observe red.**
- [ ] **Step 2: Apply Code Edit 3.2 and observe green.**

### Task 4 - Re-verify, review, publish, deploy, and close

Sequence / dependencies:
- Runs after Tasks 1 through 3 are green.

Implementation notes:
- Amend the existing branch commit rather than layering an unexplained broken intermediate commit.
- Request a fresh independent review against the complete diff.
- Continue the production and Builder steps from the superseded plan.

Verification:
- Complete Windows Pester: zero failures; two administrator-only skips allowed.
- Full Gradle build: success, including JavaScript and sensor runtime verification.
- `git diff --check`.
- Fresh independent review: no Critical or Important findings.
- Push, draft PR, all required CI, ready, squash-merge.
- Deploy immutable merge.
- During CPU acceptance, record directory counts transitioning from stale-plus-published down to exactly one published directory.
- Require both direct Celsius and the application cached `cpu.temperature` metric to become available across three refresh windows.
- Require no probe accumulation, no active Defender threat, no new 7031, all services healthy, and local/public homepage bodies correct.
- Save Builder test, spoke update/review, closure, and session memory.

- [ ] **Step 1: Run complete local verification.**
- [ ] **Step 2: Amend the branch commit and request independent review.**
- [ ] **Step 3: Push, open PR, pass CI, and merge.**
- [ ] **Step 4: Deploy and complete live acceptance.**
- [ ] **Step 5: Save and push all Builder closure artifacts.**

## Code Changes

- Candidate sensor isolation in `Production.Deploy.psm1` and its Pester test.
- Atomic staged resource publication, strict sibling cleanup, and lifetime file lease in `SecureNativeLibraryProvisioner.java`.
- Publication and exclusive-lease Java regressions.
- Monotonic bounded exact-one wait and timing regression.

## Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- `ops/production/windows/modules/Production.Sensors.psm1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- `docs/operations/windows-production.md`

## Unit Testing

- Candidate environment override red/green Pester.
- Nonmatching complete publication red/green Java test.
- Exclusive lifetime lease red/green Java test.
- Existing stale-link Java safety regression.
- Monotonic timeout clamp red/green Pester.

## Local Testing

- Focused tests first, then complete Windows Pester and full Gradle build.
- Use isolated Gradle state.
- Inspect the final diff for atomic publication, lease release ordering, candidate isolation, and no-follow cleanup.

## Validation

- Matching directories are never incomplete.
- The only transition to one matching directory leaves the fresh published directory.
- A second process cannot mutate the resource base while the first owns it.
- Deployment candidates never enable native sensors.
- Wait timeout is monotonic and bounded.
- Full local, review, CI, production, and Builder gates pass.

## Rollback or Recovery

- Keep sensors disabled until merged deployment.
- If atomic move is unsupported or lease acquisition fails, provisioning fails closed and sensor enablement rolls back.
- Use existing release rollback if the merged app cannot start.
- Do not weaken the lease, atomic move, ACL, or Defender requirements.

## Risks

- Atomic directory move support could differ by filesystem. Mitigation: production uses one NTFS parent; fail closed elsewhere.
- A leaked staging directory could remain after an abrupt crash. Mitigation: the next exclusive owner validates and removes abandoned staging directories.
- A lock release failure could delay future provisioning. Mitigation: OS process exit releases the channel lock; failures remain fail closed.
- The timing test could be noisy on a heavily loaded host. Mitigation: use a 20-millisecond requested wait with a generous 200-millisecond assertion that distinguishes it from the former 250-millisecond sleep.

## Completion Criteria

- Independent review has no Critical or Important findings.
- The repair is merged, deployed, and produces stable direct and cached CPU temperature.
- Exactly one complete protected live directory remains.
- Candidate deployment, service health, Defender, probe counts, restart events, and HTTP checks are all healthy.
- Builder closure artifacts are validated, committed, and pushed.
