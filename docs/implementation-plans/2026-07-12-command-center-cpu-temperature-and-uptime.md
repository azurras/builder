# christopherbell.dev Command Center CPU Temperature and Uptime Implementation Plan

## Document Status

ready-for-execution

## Objective

Replace the leaking, blocking CPU-temperature PowerShell session with a separately cached, one-shot bounded probe that kills its full process tree, and render uptime as concise minutes, hours, and days without changing the API's raw seconds.

## Goals

- Stop production from creating an abandoned PowerShell process every sampling cycle.
- Give privileged LibreHardwareMonitor initialization up to 20 seconds without delaying five-second snapshots.
- Retain the last valid CPU temperature across refreshes and transient failures.
- Preserve checksum-pinned, ACL-restricted sensor resources and fixed process arguments.
- Display uptime as `42s`, `12m 34s`, `8h 54m`, or `3d 8h`.
- Complete safe local runtime verification, PR/CI, merge, native deployment, live sensor verification, and Builder closure.

## Inputs

- Approved spec: `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-12-command-center-cpu-temperature-and-uptime.md`.
- Work record: `C:\Users\Christopher\Developer\builder\docs\work\2026-07-12-command-center-cpu-temperature-and-uptime.md`.
- Spoke: `A:\Projects\christopherbell.dev`, origin `https://github.com/azurras/christopherbell.dev.git`.
- Base: refreshed `origin/main` at `eff05e36a27bdb84ebfddf8073ed1792880b4e57` or later.
- Root-cause evidence: 14 Java-descendant PowerShell processes increased to 16 in 15 seconds; the current timeout is two seconds; official sensor scanning needs a longer privileged window.
- User decision: use the recommended self-contained fix and add human-readable uptime.

## Branch

- Create `codex/command-center-cpu-temperature` from refreshed `origin/main` in `A:\Projects\christopherbell.dev-worktrees\command-center-cpu-temperature`.
- Preserve the divergent primary checkout and all unrelated worktrees.

## Non-Goals

- No HWiNFO/Core Temp/Armoury Crate integration or new monitoring service.
- No ACPI thermal-zone substitution.
- No global telemetry-interval change, persistent history, or API unit change.
- No machine restart or shutdown.
- No unrelated command-center refactor.

## Assumptions

- Production continues to run as SYSTEM, which LibreHardwareMonitor requires for this host's privileged CPU sensors.
- Windows PowerShell remains present at the fixed system executable resolved by `powershell.exe`.
- Native auto-deployment stops the prior WinSW process tree when switching releases.
- Java 25 virtual threads and `ProcessHandle.descendants()` remain available.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add failing configuration and uptime-format tests

Sequence / dependencies:
- First task; establishes RED coverage before production changes.

Implementation notes:
- Extend configuration binding assertions for the independent 30-second refresh and 20-second process timeout.
- Add boundary assertions through `displayMetric` so the backend remains raw seconds.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterPropertiesTest.java`
- Lines: 80-93
- Action: replace

Current:
```java
  @Test
  void bindsSharedSamplingAndHistorySettings() throws IOException {
    CommandCenterProperties properties = bindProfile("local");

    assertThat(properties.getSampleInterval()).isEqualTo(Duration.ofSeconds(5));
    assertThat(properties.getHistoryDuration()).isEqualTo(Duration.ofMinutes(15));
    assertThat(properties.getProviderTimeout()).isEqualTo(Duration.ofSeconds(2));
    assertThat(properties.getActions().getChallengeTtl()).isEqualTo(Duration.ofMinutes(2));
    assertThat(properties.getActions().getCooldown()).isEqualTo(Duration.ofMinutes(2));
    assertThat(properties.getActions().getPowerDelay()).isEqualTo(Duration.ofSeconds(60));
    assertThat(properties.getActions().getFailedAttempts()).isEqualTo(3);
    assertThat(properties.getActions().getFailedAttemptWindow())
        .isEqualTo(Duration.ofMinutes(15));
  }
```

Proposed:
```java
  @Test
  void bindsSharedSamplingAndIndependentCpuTemperatureSettings() throws IOException {
    CommandCenterProperties properties = bindProfile("local");

    assertThat(properties.getSampleInterval()).isEqualTo(Duration.ofSeconds(5));
    assertThat(properties.getHistoryDuration()).isEqualTo(Duration.ofMinutes(15));
    assertThat(properties.getProviderTimeout()).isEqualTo(Duration.ofSeconds(2));
    assertThat(properties.getCpuTemperatureRefreshInterval()).isEqualTo(Duration.ofSeconds(30));
    assertThat(properties.getCpuTemperatureProcessTimeout()).isEqualTo(Duration.ofSeconds(20));
    assertThat(properties.getActions().getChallengeTtl()).isEqualTo(Duration.ofMinutes(2));
    assertThat(properties.getActions().getCooldown()).isEqualTo(Duration.ofMinutes(2));
    assertThat(properties.getActions().getPowerDelay()).isEqualTo(Duration.ofSeconds(60));
    assertThat(properties.getActions().getFailedAttempts()).isEqualTo(3);
    assertThat(properties.getActions().getFailedAttemptWindow())
        .isEqualTo(Duration.ofMinutes(15));
  }
```

Verification:
- Run `./gradlew :website:test --tests dev.christopherbell.admin.commandcenter.CommandCenterPropertiesTest`; expect compilation failure for the missing getters.

#### Code Edit 1.2
- File: `website/src/test/js/command-center.test.js`
- Lines: after 63
- Action: add

Current:
```javascript
test('metric display compacts byte values for fixed-width command cards', () => {
  assert.equal(displayMetric({ status: 'AVAILABLE', value: 34_028_523_520, unit: 'bytes' }), '31.7 GiB');
  assert.equal(displayMetric({ status: 'AVAILABLE', value: 4_315_924_926_464, unit: 'bytes' }), '3.9 TiB');
  assert.equal(displayMetric({ status: 'AVAILABLE', value: 46_564_906.8, unit: 'bytes/second' }), '44.4 MiB/s');
});
```

Proposed:
```javascript
test('metric display formats uptime as seconds, minutes, hours, and days', () => {
  const uptime = (value) => displayMetric({ status: 'AVAILABLE', value, unit: 'seconds' });
  assert.equal(uptime(59), '59s');
  assert.equal(uptime(60), '1m 0s');
  assert.equal(uptime(754), '12m 34s');
  assert.equal(uptime(3599), '59m 59s');
  assert.equal(uptime(3600), '1h 0m');
  assert.equal(uptime(32040), '8h 54m');
  assert.equal(uptime(86399), '23h 59m');
  assert.equal(uptime(86400), '1d 0h');
  assert.equal(uptime(288000), '3d 8h');
});
```

Verification:
- Run `./gradlew :website:jsTest`; expect the first duration assertion to fail because seconds still use generic number formatting.

### Task 2 - Add independent settings and human uptime formatting

Sequence / dependencies:
- Runs after Task 1 RED results.

Implementation notes:
- Preserve general provider timeout at two seconds.
- Route only `seconds` through a pure duration formatter.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterProperties.java`
- Lines: 14-25
- Action: replace

Current:
```java
  private boolean enabled = true;
  private Duration sampleInterval = Duration.ofSeconds(5);
  private Duration historyDuration = Duration.ofMinutes(15);
  private Duration providerTimeout = Duration.ofSeconds(2);
  private Path logPath = Path.of("logs", "application.log");
  private int maxLogLines = 250;
  private int maxLogBytes = 65_536;
  private int productionPort = 8080;
  private String productionServiceName = "ChristopherBellDev";
  private String commitIdentifier = "unknown";
  private boolean sensorLibrariesEnabled;
  private Path sensorLibraryDirectory = Path.of("command-center-sensors");
```

Proposed:
```java
  private boolean enabled = true;
  private Duration sampleInterval = Duration.ofSeconds(5);
  private Duration historyDuration = Duration.ofMinutes(15);
  private Duration providerTimeout = Duration.ofSeconds(2);
  private Duration cpuTemperatureRefreshInterval = Duration.ofSeconds(30);
  private Duration cpuTemperatureProcessTimeout = Duration.ofSeconds(20);
  private Path logPath = Path.of("logs", "application.log");
  private int maxLogLines = 250;
  private int maxLogBytes = 65_536;
  private int productionPort = 8080;
  private String productionServiceName = "ChristopherBellDev";
  private String commitIdentifier = "unknown";
  private boolean sensorLibrariesEnabled;
  private Path sensorLibraryDirectory = Path.of("command-center-sensors");
```

Verification:
- Re-run `CommandCenterPropertiesTest`; it must still fail until YAML values are added, proving binding rather than Java defaults is covered.

#### Code Edit 2.2
- File: `website/src/main/resources/application.yml`
- Lines: 13-18
- Action: replace

Current:
```yaml
command-center:
  enabled: true
  sample-interval: 5s
  history-duration: 15m
  provider-timeout: 2s
  log-path: logs/application.log
```

Proposed:
```yaml
command-center:
  enabled: true
  sample-interval: 5s
  history-duration: 15m
  provider-timeout: 2s
  cpu-temperature-refresh-interval: 30s
  cpu-temperature-process-timeout: 20s
  log-path: logs/application.log
```

Verification:
- Re-run `CommandCenterPropertiesTest`; expect it to pass.

#### Code Edit 2.3
- File: `website/src/main/resources/static/js/lib/command-center.js`
- Lines: 25-40
- Action: replace

Current:
```javascript
  if (reading.unit === 'commit') return String(reading.detail || 'Unavailable');
  if (reading.unit === 'bytes') return formatBinaryMetric(Number(reading.value), false);
  if (reading.unit === 'bytes/second') return formatBinaryMetric(Number(reading.value), true);
  const value = Number(reading.value).toLocaleString(undefined, { maximumFractionDigits: 1 });
  const units = {
    percent: '%',
    celsius: '°C',
    seconds: 's',
    megabytes: 'MB',
    watts: 'W',
    'bytes/second': 'B/s',
    state: '',
  };
  const suffix = Object.hasOwn(units, reading.unit) ? units[reading.unit] : (reading.unit || '');
  return suffix ? `${value} ${suffix}` : value;
}
```

Proposed:
```javascript
  if (reading.unit === 'commit') return String(reading.detail || 'Unavailable');
  if (reading.unit === 'bytes') return formatBinaryMetric(Number(reading.value), false);
  if (reading.unit === 'bytes/second') return formatBinaryMetric(Number(reading.value), true);
  if (reading.unit === 'seconds') return formatDuration(Number(reading.value));
  const value = Number(reading.value).toLocaleString(undefined, { maximumFractionDigits: 1 });
  const units = {
    percent: '%',
    celsius: '°C',
    megabytes: 'MB',
    watts: 'W',
    'bytes/second': 'B/s',
    state: '',
  };
  const suffix = Object.hasOwn(units, reading.unit) ? units[reading.unit] : (reading.unit || '');
  return suffix ? `${value} ${suffix}` : value;
}

function formatDuration(value) {
  const totalSeconds = Math.max(0, Math.floor(value));
  if (totalSeconds < 60) return `${totalSeconds}s`;
  const totalMinutes = Math.floor(totalSeconds / 60);
  if (totalMinutes < 60) return `${totalMinutes}m ${totalSeconds % 60}s`;
  const totalHours = Math.floor(totalMinutes / 60);
  if (totalHours < 24) return `${totalHours}h ${totalMinutes % 60}m`;
  return `${Math.floor(totalHours / 24)}d ${totalHours % 24}h`;
}
```

Verification:
- Run `./gradlew :website:jsTest`; all duration boundaries must pass.
- Commit Task 1-2 with `git commit -m "Format command center uptime for humans"`.

### Task 3 - Add failing secure probe and asynchronous-cache tests

Sequence / dependencies:
- Runs after the independent settings are green.

Implementation notes:
- Replace session-oriented client tests with desired cache behavior.
- Add a focused process/probe test using injected process control so timeout cleanup is observable without launching production PowerShell in CI.
- Extend provisioner coverage to require the pinned script path.

#### Code Edit 3.1
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClientTest.java`
- Lines: 1-114
- Action: replace

Current:
```java
class LibreHardwareCpuTemperatureClientTest {
  // Existing tests call a jPowerShell SensorSession synchronously and expect timeout recovery.
}
```

Proposed:
```java
class LibreHardwareCpuTemperatureClientTest {
  @Test
  void firstReadReturnsImmediatelyAndSchedulesOneRefresh() {
    var executor = new ManualExecutorService();
    var probe = new FakeProbe(OptionalDouble.of(64.25));
    var client = client(probe, executor);
    assertThat(client.readCelsius()).isEmpty();
    assertThat(client.readCelsius()).isEmpty();
    assertThat(executor.pending()).isEqualTo(1);
    executor.runNext();
    assertThat(client.readCelsius()).hasValue(64.25);
  }

  @Test
  void refreshIsThrottledAndRetainsLastGoodAcrossFailure() {
    var clock = new MutableClock();
    var executor = new ManualExecutorService();
    var probe = new FakeProbe(OptionalDouble.of(61), OptionalDouble.empty());
    var client = client(probe, executor, clock);
    client.readCelsius();
    executor.runNext();
    clock.advance(Duration.ofSeconds(29));
    assertThat(client.readCelsius()).hasValue(61);
    assertThat(executor.pending()).isZero();
    clock.advance(Duration.ofSeconds(1));
    assertThat(client.readCelsius()).hasValue(61);
    executor.runNext();
    assertThat(client.readCelsius()).hasValue(61);
  }

  @Test
  void closeCancelsRefreshAndClosesProbeExactlyOnce() {
    var executor = new ManualExecutorService();
    var probe = new FakeProbe(OptionalDouble.empty());
    var client = client(probe, executor);
    client.readCelsius();
    client.close();
    client.close();
    assertThat(executor.isShutdown()).isTrue();
    assertThat(probe.closeCalls()).isEqualTo(1);
  }
}
```

Verification:
- Run the class and expect compilation failures for the desired probe/executor constructors.

#### Code Edit 3.2
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbeTest.java`
- Lines: 1-1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class PowerShellCpuTemperatureProbeTest {
  @Test
  void usesOnlyFixedPowerShellArgumentsAndParsesSaneTemperature() {
    var process = FakeManagedProcess.completed("64.25", "", 0);
    var probe = probe(process);
    assertThat(probe.readCelsius()).hasValue(64.25);
    assertThat(process.command()).containsExactly(
        "powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass", "-File", "C:\\trusted\\cpu-temperature.ps1",
        "-LibreHardwareMonitorPath", "C:\\trusted\\LibreHardwareMonitorLib.dll");
  }

  @Test
  void timeoutTerminatesDescendantsAndRootAndReturnsUnavailable() {
    var process = FakeManagedProcess.timedOut();
    assertThat(probe(process).readCelsius()).isEmpty();
    assertThat(process.gracefulTreeTerminationRequested()).isTrue();
    assertThat(process.forcefulTreeTerminationRequested()).isTrue();
  }

  @Test
  void rejectsEmptyZeroMalformedOversizedAndNonZeroExitResults() {
    assertThat(probe(FakeManagedProcess.completed("0", "", 0)).readCelsius()).isEmpty();
    assertThat(probe(FakeManagedProcess.completed("NaN", "", 0)).readCelsius()).isEmpty();
    assertThat(probe(FakeManagedProcess.completed("64", "failure", 1)).readCelsius()).isEmpty();
    assertThat(probe(FakeManagedProcess.completed("x".repeat(9000), "", 0)).readCelsius()).isEmpty();
  }
}
```

Verification:
- Run the new class and expect missing-type failures.

#### Code Edit 3.3
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: 52-62
- Action: replace

Current:
```java
  @Test
  void verifiedCreateNewExtractionReturnsOnlyFreshLibraryAndCleansItUp() throws Exception {
    var provisioner = provisioner("trusted", hash("trusted"), path -> {}, "verified");

    var libraries = provisioner.provision();

    assertThat(Files.readString(libraries.libreHardwareMonitor(), UTF_8)).isEqualTo("trusted");
    Path directory = libraries.directory();
    libraries.close();
    assertThat(directory).doesNotExist();
  }
```

Proposed:
```java
  @Test
  void verifiedCreateNewExtractionReturnsPinnedLibraryAndScriptAndCleansThemUp() throws Exception {
    var provisioner = provisionerWithLibraryAndScript(path -> {}, "verified");
    var libraries = provisioner.provision();
    assertThat(Files.readString(libraries.libreHardwareMonitor(), UTF_8)).isEqualTo("trusted");
    assertThat(Files.readString(libraries.cpuTemperatureScript(), UTF_8)).isEqualTo("trusted-script");
    Path directory = libraries.directory();
    libraries.close();
    assertThat(directory).doesNotExist();
  }
```

Verification:
- Run `SecureNativeLibraryProvisionerTest`; expect compilation failure because `cpuTemperatureScript()` does not exist.

### Task 4 - Implement pinned one-shot probe and non-blocking cache

Sequence / dependencies:
- Runs only after all Task 3 tests fail for the intended missing behavior.

Implementation notes:
- One-shot PowerShell is deliberately slower but cannot leak a persistent session.
- Keep output bounded at 8 KiB and drain stdout/stderr concurrently.
- The probe owns the active process; `close()` and timeout use the same tree terminator.
- The client caches asynchronously and never waits for the probe.

#### Code Edit 4.1
- File: `website/src/main/resources/lib/cpu-temperature.ps1`
- Lines: 1-1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
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
      $values += $hardware.Sensors | Where-Object {
        $_.SensorType -eq [LibreHardwareMonitor.Hardware.SensorType]::Temperature -and
        $null -ne $_.Value -and [double]$_.Value -gt 0
      } | ForEach-Object { [double]$_.Value }
      foreach ($subHardware in $hardware.SubHardware) {
        $subHardware.Update()
        $values += $subHardware.Sensors | Where-Object {
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
- Run PowerShell parser validation without executing the script.
- Verify SHA-256 is `4d47eccfc836fe4d4ea771bf36b1b4fa4a4b91490b3f2ed8ab5e9c475687b2f3` for LF UTF-8 content with a final newline.

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 33-194
- Action: replace

Current:
```java
    this(baseDirectory, List.of(
        resource("HidSharp.dll", "8c58e5fba22acc751032dfe97ce633e4f8a4c96089749bf316d55283b36649c2"),
        resource("LibreHardwareMonitorLib.dll", "a0f2728f1734c236a9d02d9e25a88bc4f8cb7bd1faff1770726beb7af06bf8dc")),
        new WindowsAclPolicy(), () -> UUID.randomUUID().toString());
```

Proposed:
```java
    this(baseDirectory, List.of(
        resource("HidSharp.dll", "8c58e5fba22acc751032dfe97ce633e4f8a4c96089749bf316d55283b36649c2"),
        resource("LibreHardwareMonitorLib.dll", "a0f2728f1734c236a9d02d9e25a88bc4f8cb7bd1faff1770726beb7af06bf8dc"),
        resource("cpu-temperature.ps1", "4d47eccfc836fe4d4ea771bf36b1b4fa4a4b91490b3f2ed8ab5e9c475687b2f3")),
        new WindowsAclPolicy(), () -> UUID.randomUUID().toString());
```

Proposed continued behavior:
```java
      Path libre = null;
      Path cpuTemperatureScript = null;
      // Existing copy/checksum/ACL loop remains; assign both named resources.
      if (libre == null || cpuTemperatureScript == null) {
        throw new SecurityException("Required CPU sensor resources are missing.");
      }
      return NativeLibraries.owned(versionDirectory, libre, cpuTemperatureScript);

  static final class NativeLibraries implements AutoCloseable {
    private final Path directory;
    private final Path libreHardwareMonitor;
    private final Path cpuTemperatureScript;
    private final boolean owned;
    Path cpuTemperatureScript() { return cpuTemperatureScript; }
    // Preserve existing directory/library accessors and owned cleanup.
  }
```

Verification:
- Run `SecureNativeLibraryProvisionerTest`; all checksum, ACL, link, and cleanup tests must pass.

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbe.java`
- Lines: 1-1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
@Component
final class PowerShellCpuTemperatureProbe implements AutoCloseable {
  private static final int MAX_OUTPUT_BYTES = 8192;
  private final ProcessFactory processFactory;
  private final NativeLibraryResolver libraryResolver;
  private final Duration timeout;
  private final AtomicReference<ManagedProcess> active = new AtomicReference<>();
  private SecureNativeLibraryProvisioner.NativeLibraries libraries;

  synchronized OptionalDouble readCelsius() {
    try {
      if (libraries == null) libraries = libraryResolver.resolve();
      var command = List.of("powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive",
          "-ExecutionPolicy", "Bypass", "-File", libraries.cpuTemperatureScript().toString(),
          "-LibreHardwareMonitorPath", libraries.libreHardwareMonitor().toString());
      var process = processFactory.start(command, MAX_OUTPUT_BYTES);
      active.set(process);
      var result = process.await(timeout);
      if (result.timedOut() || result.exitCode() != 0) return OptionalDouble.empty();
      double value = Double.parseDouble(result.stdout().trim());
      return Double.isFinite(value) && value > 0 && value <= 125
          ? OptionalDouble.of(value) : OptionalDouble.empty();
    } catch (IOException | RuntimeException failure) {
      return OptionalDouble.empty();
    } finally {
      var process = active.getAndSet(null);
      if (process != null) process.terminateTree();
    }
  }

  @Override public synchronized void close() {
    var process = active.getAndSet(null);
    if (process != null) process.terminateTree();
    if (libraries != null) { libraries.close(); libraries = null; }
  }
}
```

Implementation detail required during execution:
- `ManagedProcess.await` drains both streams on virtual threads, caps retained output at 8 KiB, waits for the configured duration, and invokes graceful then forceful descendant/root termination on timeout.
- `ProcessFactory` is package-private and injected in tests; the production constructor always uses `new ProcessBuilder(fixedCommand).start()`.

Verification:
- Run `PowerShellCpuTemperatureProbeTest`; all fixed-command, parse, bound, exit, timeout, and cleanup cases must pass.
- Search production code for `Runtime.exec`, `cmd.exe`, caller-controlled paths, and jPowerShell imports; expected command-center result is none.

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClient.java`
- Lines: 1-139
- Action: replace

Current:
```java
/** Owns a bounded PowerShell session and explicitly closes every native computer instance. */
@Component
public final class LibreHardwareCpuTemperatureClient implements CpuTemperatureSensorClient {
  // Synchronous jPowerShell session, inline script, and discardSession implementation.
}
```

Proposed:
```java
/** Returns cached CPU temperature while refreshing the privileged probe off the sampling path. */
@Component
public final class LibreHardwareCpuTemperatureClient implements CpuTemperatureSensorClient {
  private final PowerShellCpuTemperatureProbe probe;
  private final ExecutorService refreshExecutor;
  private final Clock clock;
  private final Duration refreshInterval;
  private final boolean windows;
  private final AtomicReference<OptionalDouble> lastGood =
      new AtomicReference<>(OptionalDouble.empty());
  private final AtomicBoolean refreshInFlight = new AtomicBoolean();
  private final AtomicBoolean closed = new AtomicBoolean();
  private volatile Instant nextRefresh = Instant.MIN;

  @Override
  public OptionalDouble readCelsius() {
    var current = lastGood.get();
    if (windows && !closed.get() && !clock.instant().isBefore(nextRefresh)
        && refreshInFlight.compareAndSet(false, true)) {
      refreshExecutor.submit(this::refresh);
    }
    return current;
  }

  private void refresh() {
    try {
      var value = probe.readCelsius();
      if (value.isPresent()) lastGood.set(value);
    } finally {
      nextRefresh = clock.instant().plus(refreshInterval);
      refreshInFlight.set(false);
    }
  }

  @Override @PreDestroy
  public void close() {
    if (closed.compareAndSet(false, true)) {
      refreshExecutor.shutdownNow();
      probe.close();
    }
  }
}
```

Implementation detail required during execution:
- Production constructor injects properties, probe, and `Clock`, creates one lifecycle-owned virtual-thread executor, and derives the Windows-enabled flag from the existing property/OS boundary.
- Package-private constructor accepts executor and clock for deterministic tests.
- Rejected submission and interrupted refresh reset `refreshInFlight` without throwing into the provider.

Verification:
- Run `LibreHardwareCpuTemperatureClientTest` and `LibreHardwareCpuTemperatureProviderTest`.
- Run all command-center Java tests and confirm collection no longer emits `PROVIDER_TIMEOUT` for the cache read.
- Commit Task 3-4 with `git commit -m "Bound CPU temperature refresh processes"`.

### Task 5 - Update operations documentation and run the full validation loop

Sequence / dependencies:
- Runs after all focused tests are green.

Implementation notes:
- Document the slower cached refresh and bounded one-shot process.
- Perform safe candidate verification before publishing.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/admin/README.md`
- Lines: 30-34
- Action: replace

Current:
```markdown
- Host providers run concurrently behind independent timeouts on a private scheduler. CPU
  temperature uses a bounded, lifecycle-owned LibreHardwareMonitor PowerShell session on Windows.
- Bundled sensor DLLs are checksum-pinned and extracted with create-new semantics into a fresh,
  service-owned directory whose ACL permits only SYSTEM and Administrators.
```

Proposed:
```markdown
- Host providers run concurrently behind independent timeouts on a private scheduler. CPU
  temperature returns a non-blocking cache and refreshes every 30 seconds through a bounded,
  one-shot Windows PowerShell process whose full process tree is terminated on timeout.
- The bundled sensor DLLs and CPU-temperature script are checksum-pinned and extracted with
  create-new semantics into a fresh, service-owned directory whose ACL permits only SYSTEM and
  Administrators.
```

Verification:
- Review the doc against actual defaults and lifecycle code.

#### Code Edit 5.2
- File: `website/src/main/java/dev/christopherbell/configuration/README.md`
- Lines: 30-34
- Action: replace

Current:
```markdown
`command-center.enabled` gates host sampling and action acceptance;
`sample-interval`, `history-duration`, and `provider-timeout` control cached host
sampling. `log-path`, `max-log-lines`, and `max-log-bytes` define the server-owned
fixed log boundary. Threshold properties control warning evaluation without
changing raw readings.
```

Proposed:
```markdown
`command-center.enabled` gates host sampling and action acceptance;
`sample-interval`, `history-duration`, and `provider-timeout` control cached host
sampling. `cpu-temperature-refresh-interval` and `cpu-temperature-process-timeout`
separately bound the privileged CPU sensor without delaying other providers. `log-path`,
`max-log-lines`, and `max-log-bytes` define the server-owned fixed log boundary.
Threshold properties control warning evaluation without changing raw readings.
```

Verification:
- Search docs/config for the old lifecycle-owned session description; expect no stale match.

## Code Changes

- Task 1: failing Java property and JavaScript uptime tests.
- Task 2: two typed CPU sensor durations, YAML defaults, and pure uptime formatter.
- Task 3: failing asynchronous cache, process cleanup, fixed command, parser, and provisioner tests.
- Task 4: pinned PowerShell resource, extended secure provisioner, bounded one-shot probe, and non-blocking cache.
- Task 5: operations/configuration documentation.

## Files and Modules

- Existing: `CommandCenterProperties`, `LibreHardwareCpuTemperatureClient`, `SecureNativeLibraryProvisioner`, command-center JavaScript, tests, and READMEs.
- New: `PowerShellCpuTemperatureProbe.java`, `PowerShellCpuTemperatureProbeTest.java`, and `lib/cpu-temperature.ps1`.

## Unit Testing

- RED commands must be observed before each production edit.
- Focused Java:
  - `./gradlew :website:test --tests dev.christopherbell.admin.commandcenter.CommandCenterPropertiesTest`
  - `./gradlew :website:test --tests '*LibreHardwareCpuTemperature*' --tests '*PowerShellCpuTemperatureProbe*' --tests '*SecureNativeLibraryProvisioner*'`
- JavaScript: `./gradlew :website:jsTest`.
- Full: `./gradlew :website:test :website:build` with isolated `GRADLE_USER_HOME` if required.
- Static: `node --check` on command-center modules, PowerShell parser validation, `git diff --check`, and unsafe-command grep.

## Local Testing

1. Build the candidate in the isolated worktree.
2. Start it on port 8090 with an isolated MongoDB database, controlled log, `SIMULATED` actions, and sensor libraries disabled; confirm homepage 200 and admin shell behavior without touching 8080.
3. Exercise a deterministic test probe or focused integration harness that takes longer than two seconds and prove snapshots continue at five seconds while CPU temperature remains cached/unavailable.
4. Record process count before and after the candidate test and prove no child accumulation.
5. Confirm browser DOM renders system/application uptime in human units and has no horizontal overflow.
6. Stop the candidate, release port 8090, and remove the temporary database.

## Validation

- All focused and full tests pass.
- No jPowerShell import remains in command-center production code.
- No request value can influence process executable, script, or arguments.
- Candidate runtime and browser checks pass on a non-production port.
- PR Java 25 matrix and CodeQL gates pass before merge.
- Native auto-deployer selects the merge SHA with no error.
- Production `/` returns 200 and Mission Control stays connected.
- CPU temperature becomes a valid positive Celsius value under SYSTEM, or explicitly unavailable without general provider timeout.
- Java-descendant PowerShell process count remains stable across at least three 30-second refresh windows.
- Uptime displays hours/days rather than raw large second counts.

## Rollback or Recovery

- Revert the merged spoke PR and allow native auto-deploy to restore the prior release if service stability regresses.
- Do not manually kill arbitrary PowerShell processes. If abandoned children survive release replacement, identify only descendants of the retired website process and use the service's SYSTEM-owned process-tree stop path.
- Keep computer power actions disabled and never use reboot as cleanup during validation.

## Risks

- LibreHardwareMonitor may still return zero under SYSTEM because of driver or Windows security policy; mitigation is bounded explicit unavailable state plus stable process count.
- A child process may resist graceful termination; mitigation is descendant-first graceful destroy followed by bounded forceful destroy.
- A process can emit enough output to deadlock; mitigation is concurrent draining with an 8 KiB retained cap.
- Slow refresh can race shutdown; mitigation is one in-flight flag, executor interruption, active-process termination, and idempotent close.
- The script checksum is line-ending sensitive; mitigation is LF UTF-8 resource content, exact hash test, and Gradle resource preservation.
- Native tests cannot prove SYSTEM sensor access; final deployment verification is required after safe CI/merge.

## Completion Criteria

- Plan tasks executed in order with recorded RED/GREEN evidence.
- Automated and safe local runtime verification passes and a Builder test report is committed/pushed.
- Spoke commits are pushed, PR gates pass, PR merges, and exact release deploys.
- Production CPU-temperature behavior and process stability are observed for at least 90 seconds.
- Human uptime is verified in the authenticated live UI.
- Builder spoke update, review, closure, session memory, indexes, validation, and final main push are complete.
