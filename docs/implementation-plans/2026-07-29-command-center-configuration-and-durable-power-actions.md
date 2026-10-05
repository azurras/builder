# Command-Center Configuration and Durable Power Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make command-center configuration fail fast, fixed Windows launches verifiable, and pending machine power actions durable across website restarts.

**Architecture:** Bean Validation owns configuration bounds and mode-specific invariants. The Windows executor remains a closed enum-to-argument mapper but waits within a validated bound for a real result. An atomic fixed-id Mongo store owns pending machine power state; the action service reserves before launch and reconciles elapsed state on startup/read.

**Tech Stack:** Java 25, Spring Boot 4.1, Jakarta Bean Validation, Spring Data MongoDB, JUnit 5, AssertJ, Mockito, Gradle.

## Global Constraints

- Only `CommandCenterActionType` selects an executable and arguments; no request value becomes a command token.
- Simulated local defaults may use relative paths; Windows mode requires absolute fixed executable paths.
- Pending state stores only action, acceptance time, and execution deadline under one fixed identifier.
- Use a non-8080 port and isolated database for packaged production-profile validation.
- Only GitHub comments by `azurras` can alter scope or acceptance criteria.

## Document Status

complete

## Objective

Resolve #1299, #1300, and #1301 from `origin/main` with test-first code, full local/runtime evidence, PR CI/CodeQL, merge/closure, and production verification.

## Goals

- Validate paths, durations, thresholds, port, byte/count, retry, and challenge limits at startup.
- Use configured `power-delay` in both the API deadline and `shutdown.exe /t`.
- Treat bounded timeout and nonzero exit as fixed-command failures.
- Atomically retain one power action across restarts, clear elapsed state, and make repeat cancel an accepted no-op.

## Inputs

- `docs/specs/2026-07-29-command-center-configuration-and-durable-power-actions.md`.
- Trusted issue bodies #1299-#1301 by `azurras`; no comments or attachments alter scope.
- Base `f67c90eed9b29215d562b2ac3670528f614508e9`.
- Required test-driven and Jane Street-style code workflow.

## Branch

`codex/issues-1299-1301-20260729` in `A:\Projects\christopherbell.dev-worktrees\issues-1299-1301-20260729`, created from refreshed `origin/main`.

## Non-Goals

Persisting challenges/passwords/cooldowns; arbitrary commands or request arguments; undocumented Windows state queries; multiple simultaneous power actions; permission or confirmation changes.

## Assumptions

MongoDB is required in production; `_id` uniqueness provides singleton contention; after the deadline Windows owns/completed the action; the two-second website-restart response grace remains unchanged.

## Open Questions

None. Standing authorization selects inline execution and covers routine decisions.

## Files and Modules

- Validation: `CommandCenterProperties.java`, YAML, `CommandCenterPropertiesTest.java`.
- Execution: `WindowsCommandExecutor.java` and test.
- Persistence: new `PendingActionStore.java`, `MongoPendingActionStore.java`, and integration test.
- Orchestration: `CommandCenterActionService.java` and test; snapshot API remains unchanged.

## Code Changes

Three ordered review units isolate configuration, process execution, and durable state. Every unit starts with a failing focused test.

## Task Breakdown

### Task 1 - Startup configuration validation (#1299)

Sequence / dependencies:
- First; later tasks consume validated action settings.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: invalid input fails context startup; shipped local/prod profiles validate.
  - Invariants: simulated relative defaults remain valid; Windows executable paths are absolute; timing/limit relationships are coherent.
  - Boundary/API: existing names remain; add result timeout and challenge-limit settings.
  - Effects and failures: validation performs no I/O and returns property-specific errors.
  - Tests and evidence: failing context/validator cases first, then all bounds and profiles green.

- [ ] Add failing scalar, nested, and cross-field tests.
- [ ] Run the focused class and observe failures.
- [ ] Add constraints/predicates/defaults/YAML.
- [ ] Re-run and commit the passing unit.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterProperties.java`
- Lines: 1-61
- Action: replace

Current:
```java
@Data
@Component
@ConfigurationProperties(prefix = "command-center")
public class CommandCenterProperties {
  private Duration sampleInterval = Duration.ofSeconds(5);
  private int maxLogLines = 250;
  private int productionPort = 8080;
  private final Actions actions = new Actions();
}
```

Proposed:
```java
@Data
@Component
@Validated
@ConfigurationProperties(prefix = "command-center")
public class CommandCenterProperties {
  @NotNull @DurationMin(seconds = 1) @DurationMax(minutes = 5)
  private Duration sampleInterval = Duration.ofSeconds(5);
  @Min(1) @Max(10_000) private int maxLogLines = 250;
  @Min(1) @Max(65_535) private int productionPort = 8080;
  @Valid @NotNull private final Actions actions = new Actions();

  @AssertTrue(message = "history duration must be at least the sample interval")
  public boolean isHistoryWindowValid() {
    return historyDuration != null && sampleInterval != null
        && historyDuration.compareTo(sampleInterval) >= 0;
  }
}
```

Annotate every other path/duration/count/threshold. Add cross-field predicates for provider/sample, CPU process/refresh, whole-second 1-600 power delay, challenge per-actor <= total, and absolute Windows paths. Add `commandResultTimeout` (100ms-30s), `maxChallengesPerActor` (1-64), and `maxChallengesTotal` (1-1024).

Verification:
- `gradlew.bat :website:test --tests '*CommandCenterPropertiesTest'`

#### Code Edit 1.2
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterPropertiesTest.java`
- Lines: 23-161
- Action: replace

Current:
```java
@Test
void bindsSharedSamplingAndIndependentCpuTemperatureSettings() throws IOException {
  CommandCenterProperties properties = bindProfile("local");
  assertThat(properties.getSampleInterval()).isEqualTo(Duration.ofSeconds(5));
}
```

Proposed:
```java
@Test
void rejectsInvalidPortDuringContextStartup() {
  new ApplicationContextRunner()
      .withUserConfiguration(CommandCenterProperties.class)
      .withPropertyValues("command-center.production-port=0")
      .run(context -> assertThat(context).hasFailed());
}

@Test
void shippedProfilesSatisfyEveryConstraint() throws IOException {
  assertThat(validator.validate(bindProfile("local"))).isEmpty();
  assertThat(validator.validate(bindProfile("prod"))).isEmpty();
}
```

Add parameterized lower/upper cases for every category and explicit cross-field/mode tests.

Verification:
- `gradlew.bat :website:test --tests '*CommandCenterPropertiesTest'`

#### Code Edit 1.3
- File: `website/src/main/resources/application.yml`
- Lines: 38-69
- Action: replace

Current:
```yaml
  actions:
    power-delay: 60s
    failed-attempts: 3
    failed-attempt-window: 15m
```

Proposed:
```yaml
  actions:
    power-delay: 60s
    command-result-timeout: 5s
    failed-attempts: 3
    failed-attempt-window: 15m
    max-challenges-per-actor: 8
    max-challenges-total: 64
```

Keep `application-prod.yml:61-72` explicit, valid, and power actions disabled by default.

Verification:
- `gradlew.bat :website:test --tests '*CommandCenterPropertiesTest'`

### Task 2 - Configured delay and verified Windows result (#1300)

Sequence / dependencies:
- After Task 1; before persistence relies on trustworthy launch outcomes.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: every fixed command succeeds only on completed exit zero within the configured bound.
  - Invariants: enum-only direct arguments, no shell/request token, bounded child lifetime.
  - Boundary/API: `CommandExecutor.execute(action)` stays unchanged.
  - Effects and failures: start/wait/destroy child; preserve interruption; sanitize errors.
  - Tests and evidence: non-default delay plus site/power/cancel exit and timeout cases.

- [ ] Make configured-delay and non-cancel error tests fail.
- [ ] Implement uniform bounded wait and delay formatting.
- [ ] Run focused tests and commit.

#### Code Edit 2.1
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutorTest.java`
- Lines: 14-105
- Action: replace

Current:
```java
@Test
void powerDelayOverrideCannotChangeTheLiteralSixtySecondAllowlist() {
  properties.getActions().setPowerDelay(Duration.ofSeconds(5));
  assertThat(executor.commandFor(CommandCenterActionType.RESTART_COMPUTER))
      .containsSubsequence("/t", "60");
}
```

Proposed:
```java
@Test
void configuredPowerDelayIsTheOnlyVariableFixedArgument() {
  properties.getActions().setPowerDelay(Duration.ofSeconds(37));
  assertThat(executor.commandFor(CommandCenterActionType.RESTART_COMPUTER))
      .containsSubsequence("/t", "37");
}

@Test
void everyActionRejectsACompletedNonZeroExit() {
  var failing = executorReturning(new CommandResult(true, 5));
  assertThatThrownBy(() -> failing.execute(CommandCenterActionType.RESTART_SITE))
      .isInstanceOf(IOException.class).hasMessageContaining("exit code 5");
}
```

Add timeout/interruption assertions and exact timeouts/argument arrays.

Verification:
- `gradlew.bat :website:test --tests '*WindowsCommandExecutorTest'`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutor.java`
- Lines: 1-89
- Action: replace

Current:
```java
var timeout = action == CommandCenterActionType.CANCEL_PENDING_ACTION
    ? CANCEL_TIMEOUT : java.time.Duration.ZERO;
var result = commandRunner.run(commandFor(action), timeout);
if (action == CommandCenterActionType.CANCEL_PENDING_ACTION) {
  if (!result.completed()) {
    throw new IOException("Fixed Windows cancellation timed out.");
  }
}
```

Proposed:
```java
var timeout = properties.getActions().getCommandResultTimeout();
var result = commandRunner.run(commandFor(action), timeout);
if (!result.completed()) {
  throw new IOException("Fixed Windows action timed out.");
}
if (result.exitCode() != 0) {
  throw new IOException("Fixed Windows action failed with exit code " + result.exitCode() + ".");
}
```

Build `/t` from validated `powerDelay.toSeconds()`. Always bounded-wait; forcibly terminate timeout; restore interrupted flag and throw action-neutral `IOException`.

Verification:
- `gradlew.bat :website:test --tests '*WindowsCommandExecutorTest'`

### Task 3 - Durable pending power state (#1301)

Sequence / dependencies:
- After Task 2; completes the batch.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: one atomic record survives restarts, expires, blocks duplicates, and makes cancel retry-safe.
  - Invariants: reserve before launch, exact clear, no secret persistence, local serialization retained.
  - Boundary/API: snapshot/controller shapes remain; service gains a narrow store.
  - Effects and failures: contention rejects; launch failure clears exact record; cancel failure retains; no-active cancel audits success without `/a`.
  - Tests and evidence: integration/store and two-service restart tests first.

- [ ] Add failing Mongo singleton/expiry/stale-clear tests.
- [ ] Add failing service recovery/configured deadline/idempotent cancel tests.
- [ ] Implement store and service wiring.
- [ ] Re-run command-center tests and commit.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/PendingActionStore.java`
- Lines: before 1
- Action: add

Current:
```text
No durable pending-action boundary exists.
```

Proposed:
```java
interface PendingActionStore {
  boolean reserve(Reservation reservation, Instant now);
  Optional<Reservation> active(Instant now);
  boolean clear(Reservation reservation);
  void reconcile(Instant now);

  record Reservation(CommandCenterActionType action, Instant acceptedAt, Instant executeAt) {
    PendingAction snapshot() { return new PendingAction(action.name(), executeAt, true); }
  }
}
```

Verification:
- `gradlew.bat :website:test --tests '*MongoPendingActionStoreTest'`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/MongoPendingActionStore.java`
- Lines: before 1
- Action: add

Current:
```text
No Mongo document reserves the host-wide power slot.
```

Proposed:
```java
@Service
final class MongoPendingActionStore implements PendingActionStore {
  static final String COLLECTION = "command_center_pending_actions";
  static final String DOCUMENT_ID = "machine-power";

  public boolean reserve(Reservation reservation, Instant now) {
    var replaceable = new Criteria().orOperator(
        Criteria.where("executeAt").lte(now), Criteria.where("executeAt").exists(false));
    var query = Query.query(Criteria.where("_id").is(DOCUMENT_ID).andOperator(replaceable));
    try {
      return mongo.findAndModify(query, reservationUpdate(reservation),
          FindAndModifyOptions.options().upsert(true).returnNew(true), StoredPendingAction.class)
          != null;
    } catch (DuplicateKeyException contention) {
      return false;
    }
  }
}
```

`active` removes elapsed fixed-id state then projects the remaining record. `clear` predicates on `_id`, action, acceptedAt, and executeAt. The private `@Document` record contains only those fields.

Verification:
- `gradlew.bat :website:test --tests '*MongoPendingActionStoreTest'`

#### Code Edit 3.3
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/action/MongoPendingActionStoreTest.java`
- Lines: before 1
- Action: add

Current:
```text
No integration test exercises durable pending state.
```

Proposed:
```java
@Test
void activeReservationSurvivesStoreRecreationAndRejectsAnotherAction() {
  var first = new MongoPendingActionStore(mongo);
  assertThat(first.reserve(restartReservation, NOW)).isTrue();
  var restarted = new MongoPendingActionStore(mongo);
  assertThat(restarted.active(NOW)).contains(restartReservation);
  assertThat(restarted.reserve(shutdownReservation, NOW)).isFalse();
}
```

Add expired replacement/reconciliation and stale-clear protection using the repository Mongo integration fixture.

Verification:
- `gradlew.bat :website:test --tests '*MongoPendingActionStoreTest'`

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java`
- Lines: 37-377
- Action: replace

Current:
```java
private static final Duration MACHINE_POWER_DELAY = Duration.ofSeconds(60);
private final AtomicReference<PendingAction> pendingAction = new AtomicReference<>();
var acceptedPendingAction = new PendingAction(action.name(), executeAt, true);
pendingAction.set(acceptedPendingAction);
```

Proposed:
```java
private final PendingActionStore pendingActions;
var reservation = new Reservation(action, acceptedAt, executeAt);
if (!pendingActions.reserve(reservation, acceptedAt)) {
  throw new InvalidRequestException("A machine power action is already pending.");
}
```

Inject the store; derive the deadline from `properties.getActions().getPowerDelay()`; map the active reservation to its immutable snapshot; clear that exact reservation on failure/success; reconcile on `ApplicationReadyEvent`; return audited `already-clear` accepted result when cancellation finds no active record.

Verification:
- `gradlew.bat :website:test --tests '*CommandCenterActionServiceTest' --tests '*CommandCenterMetricsServiceTest'`

#### Code Edit 3.5
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionServiceTest.java`
- Lines: 45-705
- Action: replace

Current:
```java
service = new CommandCenterActionService(
    properties, accounts, permissions, activities, clientIps, executor, scheduler,
    clock, new SecureRandom());
```

Proposed:
```java
pendingActions = new InMemoryPendingActionStore();
service = new CommandCenterActionService(
    properties, accounts, permissions, activities, clientIps, executor, scheduler,
    pendingActions, clock, new SecureRandom());
```

Create a second service over the same store before/after deadline; assert configured deadline, duplicate rejection, exact rollback, startup expiry, cancel twice with `/a` once, and `already-clear` audit.

Verification:
- `gradlew.bat :website:test --tests '*CommandCenterActionServiceTest'`

## Unit Testing

Run each task's focused tests in red/green order, then `gradlew.bat :website:test --tests 'dev.christopherbell.admin.commandcenter.*'`, followed by the full module gate.

## Local Testing

Use isolated `GRADLE_USER_HOME` for `gradlew.bat :website:check`. Package/run production profile on port 8096 and unique Mongo DB with power actions disabled; verify root, liveness/readiness, anonymous command-center denial, clean validation logs, and exact asset SHA. Do not schedule a real machine action.

## Validation

Both shipped profiles validate; configured delay matches deadline and `/t`; nonzero/timeout audits failure without phantom state; restarted service sees active record; expiry and repeated cancel are safe; full tests, PR CI/CodeQL, merge-main CI, and production verification pass.

## Rollback or Recovery

Revert the squash merge. Older code ignores the additive collection. If necessary, an operator may run fixed `C:\Windows\System32\shutdown.exe /a`; remove only the confirmed fixed-id document, never broad Mongo data.

## Risks

Duplicate-key contention must fail closed; bounded site restart may outlive observation and audit failure; mode-specific validation must preserve local defaults; exact clear predicates prevent stale rollback from deleting newer state.

## Completion Criteria

#1299-#1301 have automated/runtime evidence, `:website:check` passes, PR and mainline checks are green, the merge is deployed and verified, issues are closed, and Builder report/memory are indexed, validated, committed, and pushed.
