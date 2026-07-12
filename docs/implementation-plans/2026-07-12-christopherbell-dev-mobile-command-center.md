# christopherbell.dev Mobile Command Center Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a secure, admin-only, mobile-first command center that monitors the Windows production host, tails a bounded redacted website log, and performs only four allowlisted host actions with step-up confirmation and auditing.

**Architecture:** A focused `admin.commandcenter` feature samples OSHI and NVIDIA providers on a five-second schedule, retains a bounded in-memory history, tails one configured log path, and exposes cached data through method-secured admin APIs. Privileged actions use one-time account-bound challenges, current-password verification, fixed `ProcessBuilder` argument arrays, simulation by default, and the existing admin activity collection; a dedicated Thymeleaf/vanilla-JavaScript page renders the Mission Control Grid and polls only while visible.

**Tech Stack:** Java 25, Spring Boot 4.1, MongoDB, Spring Security method authorization, Thymeleaf, vanilla ES modules, Gradle, OSHI 7.4.0, jLibreHardwareMonitor 1.0.6, NVIDIA `nvidia-smi`, WinSW, Node's built-in test runner.

## Global Constraints

- Work only in a new isolated worktree at `A:\Projects\christopherbell.dev-worktrees\mobile-command-center` on branch `codex/mobile-command-center`, based on refreshed `origin/main` at or after `959621f1`; do not edit the divergent primary checkout.
- Preserve Java 25, Spring Boot 4.1, MongoDB, Thymeleaf, vanilla JavaScript, and the no-npm-workflow rule.
- All command-center APIs require an active, approved `ADMIN`; the public HTML shell contains no host data and all content remains hidden until the authenticated admin check succeeds.
- Do not accept executable paths, service names, log paths, filenames, command arguments, shell fragments, or regular expressions from a request.
- Only `RESTART_SITE`, `RESTART_COMPUTER`, `SHUTDOWN_COMPUTER`, and `CANCEL_PENDING_ACTION` exist; local/test execution is simulated and production execution requires explicit configuration.
- Never record passwords, JWTs, authorization headers, raw confirmation bodies, or unredacted log secrets.
- Poll and sample at five seconds by default, keep approximately 15 minutes of bounded in-memory history, and mark unsupported values unavailable rather than estimating them.
- Do not trigger a real Windows restart or shutdown in development or delivery validation.

---

## Document Status

ready-for-execution

## Objective

Implement the approved project spec in the current christopherbell.dev architecture, verify it safely on a non-production port, publish it through pull request and CI, deploy the merged build, and prove one real website-service restart recovers without touching the machine power state.

## Goals

- Deliver the approved Mission Control Grid at `/command-center` with CPU, CPU temperature, RAM, GPU, GPU temperature, storage, network, uptime, application, service, and MongoDB state.
- Deliver bounded 15-minute sparklines and explicit available, unavailable, stale, and error states.
- Deliver a five-second, cursor-based, fixed-path application-log tail with bounds, literal filtering, rotation recovery, redaction, and text-only rendering.
- Deliver challenge/password/phrase-protected website restart, computer restart, shutdown, and cancellation with rate limits, cooldowns, idempotency, and audit records.
- Complete automated, safe local runtime, Builder test report, PR, CI, merge, production restart, smoke, closure, and session-memory phases.

## Inputs

- Approved spec: `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-12-christopherbell-dev-mobile-command-center.md`.
- Hub work record: `C:\Users\Christopher\Developer\builder\docs\work\2026-07-12-christopherbell-dev-mobile-command-center.md`.
- Authoritative spoke: `A:\Projects\christopherbell.dev`, remote `https://github.com/azurras/christopherbell.dev.git`.
- Inspected base: refreshed `origin/main` at `959621f1` on July 12, 2026.
- Production service: `ChristopherBellDev`, automatic WinSW service running as `LocalSystem`; WinSW executable `C:\ProgramData\christopherbell.dev\service\ChristopherBellDev.exe`; stdout log `C:\ProgramData\christopherbell.dev\logs\ChristopherBellDev.out.log`.
- OSHI 7.4.0 official usage and Windows sensor guidance: https://www.oshi.ooo/ and https://www.oshi.ooo/oshi-core/apidocs/com.github.oshi.common/oshi/hardware/Sensors.html.
- NVIDIA fixed-query reference: https://docs.nvidia.com/deploy/nvidia-smi/index.html.
- Direct user approvals: full host controls in v1, password re-entry, application log only, dedicated page, Mission Control Grid, OSHI Windows sensor integration, embedded allowlisted architecture, security flow, and safe test boundary.

## Branch

- Create `codex/mobile-command-center` from refreshed `origin/main` using the `superpowers:using-git-worktrees` skill.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center`.
- Do not merge, rebase, reset, or clean the primary `A:\Projects\christopherbell.dev` checkout.

## Non-Goals

- No arbitrary terminal, shell, PowerShell console, process manager, service manager, file browser, registry access, remote desktop, or file transfer.
- No caller-selected log files or Windows Event Logs.
- No Prometheus, Grafana, Elasticsearch, WebSockets, server-sent events, frontend framework, npm dependency, or durable metrics collection.
- No MFA/authentication rewrite and no least-privilege Windows service-account migration in this change.
- No development-time real PC restart or shutdown.

## Assumptions

- MongoDB remains reachable from local and production profiles.
- `nvidia-smi` remains installed with the RTX 4070 driver; provider failure is non-fatal.
- WinSW accepts the fixed `restart` operation at its configured executable path.
- The existing JWT is sent as a bearer token by browser API calls, so `/command-center` must remain a public data-free shell like `/back-office` while API methods remain server-protected.
- The existing `PasswordUtil.verifyPassword` and `PermissionService.getSelfId()` are the source of truth for current-password and current-account verification.
- Existing production deployment tooling from `origin/main` remains the release path after merge.
- If OSHI 7.4.0 exposes a compile-time package name different from the published `SystemInfoFactory.create()` example, use the documented 7.4.0 package name without changing the dependency version or behavior.

## Open Questions

None.

## Task Breakdown

### Task 1 - Create the typed configuration and dependency foundation

Sequence / dependencies:
- First implementation task after the worktree and baseline test because all later providers and action mappings consume these types and properties.

Interfaces:
- Produces `CommandCenterProperties`, `CommandCenterConfiguration`, `APIVersion.V20260712`, OSHI `SystemInfoProvider`, and one configured `CommandExecutor` bean.
- Later tasks consume `CommandCenterProperties` and `/2026-07-12` without adding alternative configuration sources.

Files:
- Modify `website/build.gradle.kts:17-58`.
- Modify `cbell-lib/src/main/java/dev/christopherbell/libs/api/APIVersion.java:12-20`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterProperties.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterConfiguration.java`.
- Modify `website/src/main/resources/application.yml:8-15`.
- Modify `website/src/main/resources/application-local.yml:1-9`.
- Modify `website/src/main/resources/application-prod.yml:21-25`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterPropertiesTest.java`.

- [ ] **Step 1: Write the failing configuration-binding test** for five-second sampling, 15-minute history, 60-second power delay, simulated local actions, and fixed production paths.
- [ ] **Step 2: Run** `./gradlew :website:test --tests dev.christopherbell.admin.commandcenter.CommandCenterPropertiesTest` and expect failure because the properties class does not exist.
- [ ] **Step 3: Add the dependency, version constant, typed properties, factory beans, and profile configuration exactly once.**
- [ ] **Step 4: Run the targeted test and** `./gradlew :website:dependencies --configuration runtimeClasspath`; expect the test to pass and OSHI/jLibreHardwareMonitor to resolve once.
- [ ] **Step 5: Commit** with `git commit -m "Add command center configuration foundation"`.

#### Code Edit 1.1
- File: `website/build.gradle.kts`
- Lines: after 31
- Action: add

Proposed:
```kotlin
    // Host metrics and Windows hardware sensors
    implementation("com.github.oshi:oshi-core:7.4.0")
    implementation("io.github.pandalxb:jLibreHardwareMonitor:1.0.6")
```

Verification:
- `./gradlew :website:dependencies --configuration runtimeClasspath` lists both artifacts and no version conflict.

#### Code Edit 1.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/APIVersion.java`
- Lines: 17-20
- Action: replace

Current:
```java
  public static final String V20260509 = "/2026-05-09";
  public static final String V20260517 = "/2026-05-17";
  public static final String V20260604 = "/2026-06-04";
}
```

Proposed:
```java
  public static final String V20260509 = "/2026-05-09";
  public static final String V20260517 = "/2026-05-17";
  public static final String V20260604 = "/2026-06-04";
  public static final String V20260712 = "/2026-07-12";
}
```

Verification:
- `./gradlew :cbell-lib:test` passes and command-center controllers import the shared constant.

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterProperties.java`
- Lines: after 0
- Action: add

Proposed:
```java
@Data
@Component
@ConfigurationProperties(prefix = "command-center")
public class CommandCenterProperties {
  private boolean enabled = true;
  private Duration sampleInterval = Duration.ofSeconds(5);
  private Duration historyDuration = Duration.ofMinutes(15);
  private Duration providerTimeout = Duration.ofSeconds(2);
  private Path logPath = Path.of("logs", "application.log");
  private int maxLogLines = 250;
  private int maxLogBytes = 65_536;
  private final Actions actions = new Actions();
  private final Thresholds thresholds = new Thresholds();

  public enum ActionMode { SIMULATED, WINDOWS }

  @Data
  public static class Actions {
    private ActionMode mode = ActionMode.SIMULATED;
    private Path winSwExecutable = Path.of("ChristopherBellDev.exe");
    private Path shutdownExecutable = Path.of("shutdown.exe");
    private Duration challengeTtl = Duration.ofMinutes(2);
    private Duration cooldown = Duration.ofMinutes(2);
    private Duration powerDelay = Duration.ofSeconds(60);
    private int failedAttempts = 3;
    private Duration failedAttemptWindow = Duration.ofMinutes(15);
  }

  @Data
  public static class Thresholds {
    private double cpuWarningPercent = 90;
    private double cpuTemperatureWarningCelsius = 85;
    private double gpuTemperatureWarningCelsius = 80;
    private double diskFreeWarningPercent = 10;
  }
}
```

Verification:
- Binding test asserts exact defaults and profile overrides; no secret or request-controlled field exists.

#### Code Edit 1.4
- File: `website/src/main/resources/application-prod.yml`
- Lines: after 25
- Action: add

Proposed:
```yaml
command-center:
  enabled: true
  log-path: C:/ProgramData/christopherbell.dev/logs/ChristopherBellDev.out.log
  actions:
    mode: WINDOWS
    win-sw-executable: C:/ProgramData/christopherbell.dev/service/ChristopherBellDev.exe
    shutdown-executable: C:/Windows/System32/shutdown.exe
    power-delay: 60s
```

Verification:
- A production-context binding test resolves only these fixed host paths; local remains `SIMULATED`.

### Task 2 - Implement cached host metrics and bounded history

Sequence / dependencies:
- Runs after Task 1 because it consumes OSHI, typed thresholds, sample interval, and history duration.

Interfaces:
- Produces `CommandCenterSnapshot snapshot()`, `HostMetricsProvider.read(Instant)`, `NvidiaMetricsProvider.read(Instant)`, and nested snapshot records used by the API and browser.
- Task 5 consumes only the serialized `CommandCenterSnapshot` contract, not provider internals.

Files:
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/model/CommandCenterSnapshot.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/HostMetricsProvider.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/OshiHostMetricsProvider.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/NvidiaMetricsProvider.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsService.java`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsServiceTest.java`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/NvidiaMetricsProviderTest.java`.

- [ ] **Step 1: Write failing provider and aggregation tests** for initial CPU ticks, zero/NaN CPU temperature, RAM, disk, network deltas, NVIDIA CSV parsing, timeout/malformed/missing executable, independent provider failure, thresholds, stale-last-good state, and bounded history eviction.
- [ ] **Step 2: Run the two targeted test classes** and expect missing-type failures.
- [ ] **Step 3: Implement the immutable model and providers**, checking both zero and `NaN` for unavailable temperature and timing every external process.
- [ ] **Step 4: Implement one scheduled collector** that catches provider failures independently, pings MongoDB with a bounded call, includes build/app uptime, and publishes one atomic cached snapshot.
- [ ] **Step 5: Run targeted tests**, then `./gradlew :website:test`; expect all tests to pass without requiring NVIDIA on CI.
- [ ] **Step 6: Commit** with `git commit -m "Add cached command center host metrics"`.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/model/CommandCenterSnapshot.java`
- Lines: after 0
- Action: add

Proposed:
```java
public record CommandCenterSnapshot(
    HealthStatus health,
    Instant sampledAt,
    List<MetricReading> metrics,
    Map<String, List<MetricPoint>> history,
    List<Alert> alerts,
    PendingAction pendingAction,
    String applicationVersion,
    long applicationUptimeSeconds
) {
  public enum HealthStatus { HEALTHY, DEGRADED, ACTION_PENDING, OFFLINE }
  public enum MetricStatus { AVAILABLE, UNAVAILABLE, STALE, ERROR }
  public record MetricReading(
      String key, String label, Double value, String unit,
      MetricStatus status, Instant sampledAt, String detail) {}
  public record MetricPoint(Instant sampledAt, Double value) {}
  public record Alert(String code, String severity, String message) {}
  public record PendingAction(String action, Instant executeAt, boolean cancellable) {}
}
```

Verification:
- Serialization test proves null values remain explicit with status and no internal command/path fields leak.

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/HostMetricsProvider.java`
- Lines: after 0
- Action: add

Proposed:
```java
public interface HostMetricsProvider {
  Map<String, CommandCenterSnapshot.MetricReading> read(Instant sampledAt);
}
```

Verification:
- Metrics service test supplies deterministic fake providers without touching host hardware.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/NvidiaMetricsProvider.java`
- Lines: after 0
- Action: add

Proposed:
```java
static final List<String> QUERY_ARGUMENTS = List.of(
    "--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total,power.draw",
    "--format=csv,noheader,nounits");

static NvidiaSample parse(String csv) {
  var columns = csv.strip().split("\\s*,\\s*");
  if (columns.length != 5) throw new IllegalArgumentException("Unexpected NVIDIA metric count.");
  return new NvidiaSample(
      Double.parseDouble(columns[0]), Double.parseDouble(columns[1]),
      Double.parseDouble(columns[2]), Double.parseDouble(columns[3]),
      Double.parseDouble(columns[4]));
}
```

Verification:
- Parser tests cover valid host output `3, 37, 2076, 12282, 18.4`, `N/A`, extra text, timeout, and non-zero exit.

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsService.java`
- Lines: after 0
- Action: add

Proposed:
```java
@Service
public class CommandCenterMetricsService {
  private final AtomicReference<CommandCenterSnapshot> latest = new AtomicReference<>();
  private final Map<String, ArrayDeque<CommandCenterSnapshot.MetricPoint>> history =
      new ConcurrentHashMap<>();

  @Scheduled(fixedDelayString = "${command-center.sample-interval:5s}")
  public void collect() {
    var sampledAt = Instant.now(clock);
    var readings = providers.stream()
        .flatMap(provider -> safelyRead(provider, sampledAt).entrySet().stream())
        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (left, right) -> right));
    appendAndTrimHistory(readings, sampledAt.minus(properties.getHistoryDuration()));
    latest.set(buildSnapshot(readings, sampledAt));
  }

  public CommandCenterSnapshot snapshot() {
    return markStaleWhenRequired(latest.get());
  }
}
```

Verification:
- A fake clock proves samples older than two intervals become stale and history never exceeds the configured time window.

### Task 3 - Implement the fixed-path bounded log tail

Sequence / dependencies:
- Runs after Task 1; independent of metrics internals so failures cannot stop sampling.

Interfaces:
- Produces `CommandCenterLogService.read(String cursor, String level, String query)` returning `LogPage(nextCursor, records, reset, status)`.
- Controller accepts only cursor, fixed level enum, and a length-bounded literal query; it accepts no path or regex.

Files:
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/logs/CommandCenterLogService.java`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/logs/CommandCenterLogServiceTest.java`.

- [ ] **Step 1: Write failing `@TempDir` tests** for initial tail, cursor advance, byte/line bounds, literal filtering, severity filtering, invalid cursor, oversized query, rotation, truncation, missing file, UTF-8 replacement, and all redaction classes.
- [ ] **Step 2: Run the targeted log test** and expect failure because the service is absent.
- [ ] **Step 3: Implement fixed-path incremental reads** with `RandomAccessFile`, an opaque URL-safe cursor containing fingerprint and offset, and a reset flag when the file identity/size changes.
- [ ] **Step 4: Implement redaction before filtering/return**, classify only `TRACE`, `DEBUG`, `INFO`, `WARN`, and `ERROR`, and cap output by both configured lines and bytes.
- [ ] **Step 5: Run the targeted test and full website tests**; expect no real production log access from tests.
- [ ] **Step 6: Commit** with `git commit -m "Add bounded redacted command center logs"`.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/logs/CommandCenterLogService.java`
- Lines: after 0
- Action: add

Proposed:
```java
public record LogPage(String nextCursor, List<LogRecord> records, boolean reset, String status) {}
public record LogRecord(long sequence, String level, String text) {}

private static final List<Pattern> SECRET_PATTERNS = List.of(
    Pattern.compile("(?i)(authorization\\s*[:=]\\s*bearer\\s+)[^\\s,;]+"),
    Pattern.compile("(?i)(password|api[_-]?key|secret|token)(\\s*[:=]\\s*)[^\\s,;]+"),
    Pattern.compile("\\beyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\b"));

public LogPage read(String cursor, String requestedLevel, String literalQuery) {
  var level = LogLevel.parse(requestedLevel);
  var query = normalizeLiteralQuery(literalQuery, 100);
  var state = decodeAndValidateCursor(cursor);
  return readBounded(properties.getLogPath(), state, level, query,
      properties.getMaxLogLines(), properties.getMaxLogBytes());
}
```

Verification:
- Tests prove a crafted cursor cannot select another file or read more than the configured recent window, and returned text contains `[REDACTED]` instead of secrets.

### Task 4 - Implement one-time challenges and allowlisted Windows actions

Sequence / dependencies:
- Runs after Task 1 and before controller wiring; uses fixed properties, existing account storage, trusted client-IP resolution, and existing admin activity persistence.

Interfaces:
- Produces `createChallenge(ActionType)`, `execute(ActionConfirmation, HttpServletRequest)`, `cancel(HttpServletRequest)`, and `pendingAction()`.
- `CommandExecutor.execute(ActionType)` accepts only the enum; `WindowsCommandExecutor.commandFor(ActionType)` is package-visible for exact-array tests.

Files:
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionType.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandExecutor.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/action/SimulatedCommandExecutor.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutor.java`.
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java`.
- Modify `website/src/main/java/dev/christopherbell/admin/activity/AdminActivityService.java:25-49`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionServiceTest.java`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutorTest.java`.

- [ ] **Step 1: Write failing action-service tests** for active/approved/admin checks, correct and incorrect passwords, exact phrases, challenge ownership/action/expiry/replay/concurrent consumption, failure-window throttling, accepted-action cooldown, idempotency, disabled/non-Windows modes, cancellation, and safe audit metadata.
- [ ] **Step 2: Write failing executor tests** asserting every exact argument list and proving no request value can alter it.
- [ ] **Step 3: Run targeted tests** and expect missing-type failures.
- [ ] **Step 4: Implement a `SecureRandom` challenge store** with atomic removal and fake-clock seams; verify current account state and password with `AccountRepository`, `PermissionService`, and `PasswordUtil` at execution time.
- [ ] **Step 5: Implement simulated and Windows executors**; schedule website restart after the accepted response path and use a 60-second OS countdown for machine actions.
- [ ] **Step 6: Refactor admin auditing** to accept an explicit actor id/username for background completion while preserving the existing request-context `record(...)` API.
- [ ] **Step 7: Run targeted and full tests**, then commit with `git commit -m "Add protected command center actions"`.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionType.java`
- Lines: after 0
- Action: add

Proposed:
```java
public enum CommandCenterActionType {
  RESTART_SITE("RESTART SITE", true),
  RESTART_COMPUTER("RESTART COMPUTER", true),
  SHUTDOWN_COMPUTER("SHUTDOWN COMPUTER", true),
  CANCEL_PENDING_ACTION("", false);

  private final String confirmationPhrase;
  private final boolean requiresChallenge;
}
```

Verification:
- Enum test asserts the set and phrases exactly; no string-to-command fallback exists.

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutor.java`
- Lines: after 0
- Action: add

Proposed:
```java
List<String> commandFor(CommandCenterActionType action) {
  var actions = properties.getActions();
  var delay = Long.toString(actions.getPowerDelay().toSeconds());
  return switch (action) {
    case RESTART_SITE -> List.of(actions.getWinSwExecutable().toString(), "restart");
    case RESTART_COMPUTER -> List.of(actions.getShutdownExecutable().toString(),
        "/r", "/t", delay, "/d", "p:0:0", "/c", "christopherbell.dev admin command center");
    case SHUTDOWN_COMPUTER -> List.of(actions.getShutdownExecutable().toString(),
        "/s", "/t", delay, "/d", "p:0:0", "/c", "christopherbell.dev admin command center");
    case CANCEL_PENDING_ACTION -> List.of(actions.getShutdownExecutable().toString(), "/a");
  };
}
```

Verification:
- Exact-array tests compare every element, and repository grep finds no `cmd.exe`, `powershell`, `Runtime.exec`, or concatenated shell command in the feature.

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java`
- Lines: after 0
- Action: add

Proposed:
```java
public ActionChallenge createChallenge(CommandCenterActionType action) {
  var actor = requireCurrentAdmin();
  if (!action.isRequiresChallenge()) throw new InvalidRequestException("Action does not use a challenge.");
  enforceAttemptWindow(actor.getId());
  var challenge = new StoredChallenge(randomToken(), actor.getId(), action,
      Instant.now(clock).plus(properties.getActions().getChallengeTtl()));
  challenges.put(challenge.id(), challenge);
  return new ActionChallenge(challenge.id(), action, challenge.expiresAt(), action.getConfirmationPhrase());
}

public ActionResult execute(ActionConfirmation request, HttpServletRequest servletRequest) {
  var actor = requireCurrentAdmin();
  var challenge = consumeChallenge(request.challengeId(), actor.getId(), request.action());
  verifyPassword(actor, request.password());
  if (!challenge.action().getConfirmationPhrase().equals(request.confirmation())) {
    recordFailedAttempt(actor.getId());
    throw new InvalidRequestException("Confirmation phrase did not match.");
  }
  enforceCooldown(actor.getId(), request.action());
  return acceptAndAudit(actor, request.action(), clientIpResolver.resolveClientIp(servletRequest));
}
```

Verification:
- Tests prove challenges are removed before password/phrase evaluation, so every failure requires a fresh challenge and cannot be replayed.

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/admin/activity/AdminActivityService.java`
- Lines: 25-49
- Action: replace

Current:
```java
  public AdminActivity record(
      String action, String targetType, String targetId, String targetLabel,
      String message, Map<String, String> metadata) {
    var actorId = permissionService.getSelfId();
    var actorUsername = accountRepository.findById(actorId)
        .map(account -> account.getUsername() == null ? actorId : account.getUsername())
        .orElse(actorId);
    return adminActivityRepository.save(AdminActivity.builder()
        .actorAccountId(actorId)
        .actorUsername(actorUsername)
        .action(action)
        .targetType(targetType)
        .targetId(targetId)
        .targetLabel(targetLabel)
        .message(message.formatted(actorUsername))
        .metadata(metadata)
        .createdOn(Instant.now(clock))
        .build());
  }
```

Proposed:
```java
  public AdminActivity record(
      String action, String targetType, String targetId, String targetLabel,
      String message, Map<String, String> metadata) {
    var actorId = permissionService.getSelfId();
    var actorUsername = accountRepository.findById(actorId)
        .map(account -> account.getUsername() == null ? actorId : account.getUsername())
        .orElse(actorId);
    return recordForActor(actorId, actorUsername, action, targetType, targetId,
        targetLabel, message, metadata);
  }

  public AdminActivity recordForActor(
      String actorId, String actorUsername, String action, String targetType,
      String targetId, String targetLabel, String message, Map<String, String> metadata) {
    return adminActivityRepository.save(AdminActivity.builder()
        .actorAccountId(actorId).actorUsername(actorUsername).action(action)
        .targetType(targetType).targetId(targetId).targetLabel(targetLabel)
        .message(message.formatted(actorUsername)).metadata(Map.copyOf(metadata))
        .createdOn(Instant.now(clock)).build());
  }
```

Verification:
- Existing `AdminActivityServiceTest` remains green and new tests prove background outcome records do not depend on a request security context.

### Task 5 - Expose one method-secured command-center API

Sequence / dependencies:
- Runs after Tasks 2-4 because it composes metrics, logs, challenges, actions, and pending-action state without owning business rules.

Interfaces:
- Produces the five approved API routes under `/api/admin/command-center` plus `APIVersion.V20260712`.
- Every method uses `@PreAuthorize("@permissionService.hasAuthority('ADMIN')")`; service-level account checks remain for actions.

Files:
- Create `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterController.java`.
- Test `website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterControllerTest.java`.

- [ ] **Step 1: Write failing `@WebMvcTest` cases** for anonymous 401, user 403, admin 200/202, payload shapes, validation errors, and zero interactions on rejected callers for every route.
- [ ] **Step 2: Run the controller test** and expect failure because the controller is absent.
- [ ] **Step 3: Add thin endpoints** that use Bean Validation, never log request bodies, return `Response<T>`, and map accepted actions to HTTP 202.
- [ ] **Step 4: Run controller and full tests**, then commit with `git commit -m "Expose admin command center APIs"`.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterController.java`
- Lines: after 0
- Action: add

Proposed:
```java
@RequiredArgsConstructor
@RequestMapping("/api/admin/command-center")
@RestController
public class CommandCenterController {
  private final CommandCenterMetricsService metricsService;
  private final CommandCenterLogService logService;
  private final CommandCenterActionService actionService;

  @GetMapping(V20260712 + "/snapshot")
  @PreAuthorize("@permissionService.hasAuthority('ADMIN')")
  ResponseEntity<Response<CommandCenterSnapshot>> snapshot() { return ok(metricsService.snapshot()); }

  @GetMapping(V20260712 + "/logs")
  @PreAuthorize("@permissionService.hasAuthority('ADMIN')")
  ResponseEntity<Response<LogPage>> logs(
      @RequestParam(required = false) String cursor,
      @RequestParam(defaultValue = "ALL") String level,
      @RequestParam(defaultValue = "") @Size(max = 100) String query) {
    return ok(logService.read(cursor, level, query));
  }

  @PostMapping(V20260712 + "/action-challenges")
  @PreAuthorize("@permissionService.hasAuthority('ADMIN')")
  ResponseEntity<Response<ActionChallenge>> challenge(@Valid @RequestBody ChallengeRequest request) {
    return ok(actionService.createChallenge(request.action()));
  }

  @PostMapping(V20260712 + "/actions")
  @PreAuthorize("@permissionService.hasAuthority('ADMIN')")
  ResponseEntity<Response<ActionResult>> execute(
      @Valid @RequestBody ActionConfirmation request, HttpServletRequest servletRequest) {
    return ResponseEntity.accepted().body(success(actionService.execute(request, servletRequest)));
  }

  @PostMapping(V20260712 + "/actions/cancel")
  @PreAuthorize("@permissionService.hasAuthority('ADMIN')")
  ResponseEntity<Response<ActionResult>> cancel(HttpServletRequest servletRequest) {
    return ok(actionService.cancel(servletRequest));
  }
}
```

Verification:
- `CommandCenterControllerTest` proves security and response codes for all routes; request/response logging grep shows no password serialization.

### Task 6 - Build the dedicated Mission Control page and admin navigation

Sequence / dependencies:
- Runs after Task 5 so the page binds to stable API contracts.

Interfaces:
- Produces `/command-center`, `API.admin.commandCenter`, pure browser format/state helpers, five-second polling, literal log rendering, challenge modal, countdown, cancellation, and restart reconnection.

Files:
- Modify `website/src/main/java/dev/christopherbell/view/content/ContentViewController.java:45-54`.
- Modify `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java:39-88`.
- Modify `website/src/main/resources/templates/back-office.html:15-22`.
- Create `website/src/main/resources/templates/command-center.html`.
- Modify `website/src/main/resources/static/js/lib/api.js:6-10`.
- Create `website/src/main/resources/static/js/lib/command-center.js`.
- Create `website/src/main/resources/static/js/command-center.js`.
- Modify `website/src/main/resources/static/js/components/nav.js:331-339`.
- Modify `website/src/main/resources/static/css/main.css:after 5661`.
- Modify `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java:135-145`.
- Create `website/src/test/js/command-center.test.js`.
- Modify `website/src/test/js/a11y-markup.test.js` after its final test.

- [ ] **Step 1: Write failing route, markup, and pure-JavaScript tests** for the hidden shell, required landmarks/labels, admin link, API paths, formatting unavailable/stale readings, polling backoff/visibility decisions, exact phrases, countdown state, and log lines returned only as text.
- [ ] **Step 2: Run focused Java and JS tests** and expect missing route/module/template failures.
- [ ] **Step 3: Add the public data-free page shell route and `PUBLIC_URLS` entry**; keep every API absent from the public list.
- [ ] **Step 4: Add the responsive template and API constants**, using a native dialog for step-up confirmation and dedicated live regions for health/action/log state.
- [ ] **Step 5: Add pure helpers and page orchestration**; gate through `API.accounts.me`, poll only when visible, use `textContent` for logs, and clear password fields immediately after submission.
- [ ] **Step 6: Add Mission Control CSS** with phone-first one-column cards, desktop grid expansion, visible focus states, reduced-motion support, and a separate danger zone.
- [ ] **Step 7: Run `node --check` on both new modules, targeted Java/JS tests, `:website:jsTest`, and `:website:test`.**
- [ ] **Step 8: Commit** with `git commit -m "Add mobile command center page"`.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/view/content/ContentViewController.java`
- Lines: after 53
- Action: add

Proposed:
```java
  /** Serves the data-free admin command-center page shell. */
  @GetMapping(value = "/command-center")
  public String getCommandCenterPage() {
    return "command-center.html";
  }
```

Verification:
- `GET /command-center` renders the hidden shell; API requests remain 401 without a token.

#### Code Edit 6.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 81-87
- Action: replace

Current:
```java
      "/void",
      "/void/**",
      "/back-office",
      "/wfl",
      "/wfl/favorites",
      "/wfl/top-rated",
      "/wfl/restaurants/**"
```

Proposed:
```java
      "/void",
      "/void/**",
      "/back-office",
      "/command-center",
      "/wfl",
      "/wfl/favorites",
      "/wfl/top-rated",
      "/wfl/restaurants/**"
```

Verification:
- Security tests prove only the shell is public and `/api/admin/command-center/**` remains protected.

#### Code Edit 6.3
- File: `website/src/main/resources/static/js/lib/api.js`
- Lines: 6-10
- Action: replace

Current:
```javascript
export const API = {
  admin: {
    activity: '/api/admin/activity/2026-05-09',
  },
```

Proposed:
```javascript
export const API = {
  admin: {
    activity: '/api/admin/activity/2026-05-09',
    commandCenter: {
      snapshot: '/api/admin/command-center/2026-07-12/snapshot',
      logs: '/api/admin/command-center/2026-07-12/logs',
      challenges: '/api/admin/command-center/2026-07-12/action-challenges',
      actions: '/api/admin/command-center/2026-07-12/actions',
      cancel: '/api/admin/command-center/2026-07-12/actions/cancel',
    },
  },
```

Verification:
- JS test imports and deep-compares all five fixed paths.

#### Code Edit 6.4
- File: `website/src/main/resources/static/js/lib/command-center.js`
- Lines: after 0
- Action: add

Proposed:
```javascript
export const POLL_INTERVAL_MS = 5000;
export const ACTION_PHRASES = Object.freeze({
  RESTART_SITE: 'RESTART SITE',
  RESTART_COMPUTER: 'RESTART COMPUTER',
  SHUTDOWN_COMPUTER: 'SHUTDOWN COMPUTER',
});

export function displayMetric(reading) {
  if (!reading || reading.status === 'UNAVAILABLE' || reading.value == null) return 'Unavailable';
  const suffix = reading.unit ? ` ${reading.unit}` : '';
  return `${Number(reading.value).toLocaleString(undefined, { maximumFractionDigits: 1 })}${suffix}`;
}

export function nextPollDelay(failures) {
  return Math.min(30_000, POLL_INTERVAL_MS * (2 ** Math.min(Number(failures || 0), 3)));
}

export function shouldPoll(documentHidden, paused) {
  return !documentHidden && !paused;
}
```

Verification:
- Node tests cover null/unavailable/stale formatting, exact phrases, and 5/10/20/30-second bounded backoff.

#### Code Edit 6.5
- File: `website/src/main/resources/static/js/command-center.js`
- Lines: after 0
- Action: add

Proposed:
```javascript
async function gateCommandCenter() {
  const token = localStorage.getItem('cbellLoginToken');
  if (!token) return window.location.replace('/404');
  const response = await fetch(API.accounts.me, { headers: authHeaders() });
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body?.payload?.role !== 'ADMIN') return window.location.replace('/404');
  root.classList.remove('d-none');
  wireControls();
  await pollNow();
}

function appendLogRecord(record) {
  const line = document.createElement('div');
  line.className = `command-log-line level-${String(record.level || 'INFO').toLowerCase()}`;
  line.textContent = record.text || '';
  logOutput.append(line);
}

async function submitAction(action, challengeId, password, confirmation) {
  try {
    return await fetchJson(API.admin.commandCenter.actions, {
      method: 'POST', headers: authHeaders(),
      body: JSON.stringify({ action, challengeId, password, confirmation }),
    });
  } finally {
    actionForm.elements.password.value = '';
  }
}
```

Verification:
- Markup/JS tests and browser inspection prove log content never reaches `innerHTML`, password input clears, and non-admin content never becomes visible.

#### Code Edit 6.6
- File: `website/src/main/resources/static/js/components/nav.js`
- Lines: 335-337
- Action: replace

Current:
```javascript
                    <div class="dropdown-menu dropdown-menu-end profile-menu">
                        ${isAdmin ? `<a class="dropdown-item" href="/back-office">Back Office</a>` : ''}
                        <a class="dropdown-item" href="${profileHref}">Profile</a>
```

Proposed:
```javascript
                    <div class="dropdown-menu dropdown-menu-end profile-menu">
                        ${isAdmin ? `<a class="dropdown-item" href="/back-office">Back Office</a><a class="dropdown-item" href="/command-center">Command Center</a>` : ''}
                        <a class="dropdown-item" href="${profileHref}">Profile</a>
```

Verification:
- Nav regression test proves only stored `ADMIN` role renders the command-center link.

### Task 7 - Update ownership documentation and run the full safe verification matrix

Sequence / dependencies:
- Runs after all implementation tasks; documentation describes actual final contracts, then the full build and runtime evidence gate publishing.

Files:
- Modify `website/src/main/java/dev/christopherbell/admin/README.md:1-19`.
- Modify `website/src/main/java/dev/christopherbell/view/README.md:7-22`.
- Modify `website/src/main/java/dev/christopherbell/configuration/README.md:7-27`.
- Modify `website/src/main/resources/static/js/README.md:93-112`.
- Modify `website/src/main/resources/static/css/README.md:37-76`.
- Modify root `README.md` production/configuration sections only if new environment variables must be operator-visible.

- [ ] **Step 1: Update feature documentation** with package ownership, API routes, provider behavior, unavailable semantics, fixed log boundary, exact action set, simulation default, production enablement, and verification commands.
- [ ] **Step 2: Run Java format/static checks already configured by the build**, `node --check` on touched modules, and `git diff --check`.
- [ ] **Step 3: Run targeted command-center tests**, `:website:jsTest`, `:website:test`, and `:website:build` with isolated `GRADLE_USER_HOME` if the shared Windows daemon registry denies access.
- [ ] **Step 4: Search the diff** for `Runtime.exec`, `cmd.exe`, `powershell`, caller-provided paths, password logging, `innerHTML` log rendering, and secrets; expected result is no unsafe match.
- [ ] **Step 5: Commit** with `git commit -m "Document command center operations"`.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/admin/README.md`
- Lines: 7-15
- Action: replace

Current:
```markdown
- Admin activity recording and reads live under `activity`.
- Admin-facing DTOs under `model`.
- Cross-feature moderation/admin summaries, such as reports and recent operational state.
- Back Office work queues for reports and users.
- Back Office user moderation actions, including approval, suspension,
  activation, and role promotion through the account update API.
- Back Office operations for Location Census ZIP coordinate imports, What's For
  Lunch imports/dedupe, vehicle VIN admin actions, vehicle collection state, and
  admin-only content reads.
```

Proposed:
```markdown
- Admin activity recording and reads live under `activity`.
- `commandcenter` owns cached host metrics, the bounded configured log tail,
  one-time action challenges, fixed Windows command mappings, and the admin API.
- Command-center actions are simulated by default. Production enables only
  website restart, delayed computer restart, delayed shutdown, and cancellation.
- Back Office work queues, user moderation, content operations, and shared admin
  activity remain separate from host-control behavior.

### Security Boundary

Command-center APIs require an active approved admin. They never accept shell
fragments, executable paths, service names, log paths, or filenames. Passwords
are used only for immediate step-up verification and are never persisted or logged.
```

Verification:
- Documentation grep finds the four actions, simulation default, and fixed input boundary.

### Task 8 - Perform local runtime, publish, deployment, and closure phases

Sequence / dependencies:
- Runs only after Task 7 automated validation is green and the feature worktree is clean except intended commits.

Implementation notes:
- Use `verify-local-spring-app` for the alternate-port and production-safe runtime workflow.
- Use Builder spoke dispatch/update/review artifacts, `save-test-report`, `close-story-issue`, `close-hub-work`, and `save-session-memory` at their required checkpoints.
- Do not execute real restart/shutdown machine commands; only the merged website-service restart is exercised after production deployment.

- [ ] **Step 1: Start local MongoDB if needed and boot the worktree app** on port 8090 with a unique Gradle home, a controlled temporary log path, and `command-center.actions.mode=SIMULATED`; keep production port 8080 untouched.
- [ ] **Step 2: Exercise anonymous, regular-user, and admin API flows** with exact requests and responses; capture snapshot readings, sensor unavailable behavior, log redaction/filter/rotation, challenge failures, successful simulated commands, audit records, countdown/cancel state, and mobile/desktop screenshots.
- [ ] **Step 3: Save and validate the Builder test report**, update indexes/hub state, commit, and push the test-report checkpoint.
- [ ] **Step 4: Push `codex/mobile-command-center` and open a draft PR** summarizing security boundaries, test evidence, and `LocalSystem` residual risk.
- [ ] **Step 5: Wait for required Java matrix and CodeQL checks**, fix only in-scope failures with systematic debugging, and merge only when required gates pass.
- [ ] **Step 6: Deploy the merged production artifact** through the existing native Windows deployment workflow, then use the command center's real `Restart Website` action once.
- [ ] **Step 7: Verify service recovery**: WinSW running, port 8080 listening, `GET /` returns 200, admin command-center snapshot/log endpoints return 200, and no unexpected error-log entry appears.
- [ ] **Step 8: Record spoke update/review, close the hub work, save final session memory, update indexes, validate hub state, and commit/push Builder main.**

## Code Changes

- Dependencies/versioning: Code Edits 1.1-1.4.
- Host metric contracts/providers/cache: Code Edits 2.1-2.4.
- Fixed-path log tail: Code Edit 3.1.
- Challenge/action/audit workflow: Code Edits 4.1-4.4.
- Method-secured API: Code Edit 5.1.
- Route/security shell/API/frontend/navigation: Code Edits 6.1-6.6.
- Ownership documentation: Code Edit 7.1 plus the file-specific documentation updates listed in Task 7.

## Files and Modules

- `cbell-lib`: one shared API date constant.
- `website/admin/commandcenter`: typed configuration, snapshot model, metrics, logs, actions, controller.
- `website/admin/activity`: explicit-actor audit overload for asynchronous completion.
- `website/view/content` and `configuration/security`: public data-free page shell only.
- `templates`, `static/js`, `static/css`: Mission Control Grid and guarded polling/action UI.
- Java and Node tests: provider, service, controller, route, pure UI state, markup, security, and regression coverage.
- Package/frontend/CSS/root docs: operational and security contracts.

## Unit Testing

- Baseline: `./gradlew :website:test` before edits in the isolated worktree.
- Focused Java:
  - `./gradlew :website:test --tests 'dev.christopherbell.admin.commandcenter.*'`
  - `./gradlew :website:test --tests dev.christopherbell.admin.AdminActivityServiceTest`
  - `./gradlew :website:test --tests dev.christopherbell.view.ViewControllerTest`
  - `./gradlew :website:test --tests dev.christopherbell.configuration.SecurityConfigTest`
- Browser modules:
  - `node --check website/src/main/resources/static/js/lib/command-center.js`
  - `node --check website/src/main/resources/static/js/command-center.js`
  - `node --test website/src/test/js/command-center.test.js website/src/test/js/a11y-markup.test.js`
  - `./gradlew :website:jsTest`
- Wide gates:
  - `./gradlew :website:test`
  - `./gradlew :website:build`
- On Windows shared-cache failure, set `GRADLE_USER_HOME` to a new worktree-specific directory and rerun with `--no-daemon`; do not modify the shared cache.

## Local Testing

- Base URL: `http://localhost:8090`; production stays on `http://localhost:8080` until after merge.
- Runtime properties: local profile, controlled log file, `command-center.actions.mode=SIMULATED`, and explicit port 8090.
- Data sent:
  - anonymous/admin `GET /api/admin/command-center/2026-07-12/snapshot`;
  - `GET .../logs?level=WARN&query=needle` after appending controlled INFO/WARN/token/password lines and rotating the file;
  - action challenge requests for all three protected actions;
  - wrong and correct password/phrase confirmations;
  - replayed/expired/mismatched challenge ids;
  - cancel request after a simulated pending machine action.
- Expected responses: 401 anonymous, 403 non-admin, 200 snapshot/log/challenge/cancel, 202 accepted simulated action, bounded redacted log payload, conflict/rate responses for replay/cooldown/throttling.
- UI input: phone and desktop viewports; pause/resume logs; severity/search controls; typed phrases; password clearing; countdown/cancel; hidden-tab polling pause; reconnect state.
- Production validation after merge: one real website-service restart only, then public/admin smoke. Do not execute real computer restart or shutdown.

## Validation

- Every requested metric appears or has an explicit unavailable/stale state with sample time.
- Five-second server sampling is shared and browser polling stops while hidden.
- History and logs remain bounded under repeated sampling/polling.
- Anonymous and non-admin callers cannot read host/log data or invoke actions.
- Password/challenge/action substitution, replay, throttling, cooldown, and double-submit tests pass.
- Exact Windows arrays contain only configured executable paths and fixed arguments.
- Redacted logs never render through HTML injection.
- Full Java, JavaScript, build, local runtime, PR CI, production restart, and smoke gates pass.

## Rollback or Recovery

- Set production action mode back to `SIMULATED` or disable command-center actions to retain monitoring while removing host mutation.
- Remove the navigation link and `/command-center` public shell mapping for an emergency UI disable; APIs remain method-protected.
- Revert the feature merge and redeploy the prior known-good JAR through the existing WinSW deployment workflow.
- If website restart fails, use Windows service control locally to restore `ChristopherBellDev`, inspect wrapper/stdout/stderr logs, and keep the issue/work record open.
- No schema migration or durable metrics data requires rollback.

## Risks

- Admin compromise can now cause host power actions; mitigate with fresh account lookup, password re-verification, one-time challenges, exact phrases, rate limits, closed enums, fixed arrays, TLS, and audit records.
- The app runs as `LocalSystem`; keep the feature strictly allowlisted and record least-privilege service migration as a separate follow-up.
- CPU temperature may remain unavailable on a motherboard/driver combination; test real host output and preserve explicit unavailable state.
- OSHI/jLibre native behavior can differ across CI operating systems; provider creation and reads must degrade without preventing Spring startup.
- The app restarts itself; return acceptance before the fixed WinSW restart, persist accepted audit first, and make the browser reconnect.
- Log redaction is heuristic; fixed path, bounds, server redaction, text-only rendering, and no full-file download reduce exposure.
- The primary checkout is divergent; all code work remains in the isolated worktree.

## Completion Criteria

- Plan tasks and code edits are implemented on `codex/mobile-command-center` with focused commits.
- Automated tests, JS syntax/tests, full website tests, and build pass.
- Safe local app verification on port 8090 exercises real metrics/logs and simulated actions with exact evidence.
- Builder test report is saved, validated, committed, and pushed.
- PR is opened, required CI passes, PR is merged, and merge state is confirmed.
- Merged production build is deployed; real website restart and post-restart public/admin smoke pass.
- No real computer restart or shutdown occurs during delivery.
- Hub work, spoke updates/review, closure, final session memory, indexes, and validation are complete and pushed.

## Plan Self-Review

- Spec coverage: every approved metric, log, page, security, action, performance, test, deploy, and closure requirement maps to Tasks 1-8.
- Placeholder scan: the plan contains no deferred implementation marker or pending line range.
- Type consistency: `V20260712`, `CommandCenterSnapshot`, `LogPage`, `CommandCenterActionType`, `ActionChallenge`, `ActionConfirmation`, `ActionResult`, and API path names are consistent across producer and consumer tasks.

## Plan Review

### Blockers

None. The Builder implementation-plan validator passes, every code-changing task has concrete inspected line ranges and task-level Code Edit blocks, and runtime testing, rollback, risk, and completion gates are explicit.

### Warnings

- CPU temperature can remain unavailable despite the approved Windows sensor integration.
- Real computer restart and shutdown cannot be exercised safely during delivery; exact command-array and simulation evidence are the v1 proof.
- The first real website self-restart is intentionally deferred until the merged production deployment and must keep rollback access to local Windows service control.
- The existing `LocalSystem` service identity remains a residual host-privilege risk and should be evaluated separately after this feature.

### Ready State

ready
