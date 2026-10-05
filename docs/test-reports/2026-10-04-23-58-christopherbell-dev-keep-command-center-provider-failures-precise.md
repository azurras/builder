# Keep Command Center Provider Failures Precise: Test Report

## Story/Issue
The user-requested Chris Street Style codebase audit. Individual plan: [Keep Command Center Provider Failures Precise](../implementation-plans/2026-10-04-23-31-christopherbell-dev-keep-command-center-provider-failures-precise.md). Draft PR #1477 is excluded.

## Branch
`codex/command-center-provider-failure-boundaries-20261004` at `d34d8e78`

## Pass / Fail

> [!CAUTION]
> **3 passed; local application startup is blocked** on candidate `d34d8e78`. No PR was created.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Unexpected timeout conversion failure remains visible | ✅ PASS | The regression failed before the fix because the broad catch hid `ArithmeticException`; candidate rethrows it. |
| 2 | Provider cancellation and native service suite | ✅ PASS | All 14 focused service tests passed; cancellation retains the last good reading as stale and emits the existing warning. |
| 3 | Full native checks | ✅ PASS | `:website:check :cbell-lib:check` succeeded; 2,043 Java tests, 0 failures/errors, 110 opt-in skips. |
| 4 | Packaged candidate startup on the permitted test database | ⏸️ BLOCKED | MongoDB connection to isolated `127.0.0.1:27018/test` worked, but startup stopped at migration 015 because the required domain cutover ledger is absent; no readiness or home response was served. |

## Test Cases
1. **Unexpected timeout conversion failure remains visible:** Set provider timeout to `Duration.ofSeconds(Long.MAX_VALUE)` and assert that `collect()` propagates `ArithmeticException`; observed failure on the broad-catch baseline and pass after narrowing.
2. **Provider cancellation and native service suite:** Return a successful future followed by a cancelled future and assert stale value retention and the existing `PROVIDER_ERROR` alert; run the focused class.
3. **Full native checks:** Run Gradle checks for the website and shared library, including Java, JavaScript and PowerShell checks.
4. **Packaged candidate startup:** Launch the committed jar in profile `test` on port 8081 with Mongo URI `mongodb://127.0.0.1:27018/test`; request readiness and `/` after startup.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev website |
| Candidate | `d34d8e78`, jar SHA-256 `AB56DE85B69E0CDBAE3D008A2759241A7BB4ACC101389DA79C63D0DD5BDB0A2C` |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, profile `test`, candidate port 8081 |
| Database | Isolated MongoDB PID 25328 at `127.0.0.1:27018`, database `test`; production Mongo listener PID 5236 at port 27017 |
| Isolation | `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; the `test` database was read back before and after startup; Mongo logs show the app connected only to `127.0.0.1:27018` |
| Production | Automatic status previously confirmed SHA `695a3ed8617f9b4ab07abb7413baf369c58acf6` active and healthy; port 8080 listener remained PID 45028 during this candidate attempt |

## Local Run Details
- **Local command:** Set `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`, and `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\tmp\jds`; start `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false` with hidden `Start-Process` and redirected logs.
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\chris-street-style-provider-failures-20261004`.
- **Candidate process:** PID 47292; process exited during Spring context initialization.
- **Logs:** `%TEMP%\chris-style-provider-d34d8e78\candidate.out.log` and `candidate.err.log`.
- **Cleanup:** Confirmed PID 47292 exited and port 8081 had no listener. Kept the session-owned temporary MongoDB process running; no direct database writes or cleanup commands were used.

## Data Sent

### 1. Unexpected timeout conversion failure remains visible

```text
providerTimeout = Duration.ofSeconds(Long.MAX_VALUE)
Expected: CommandCenterMetricsService.collect() throws ArithmeticException from Duration.toNanos()
Baseline result: broad catch suppressed the exception and converted it to PROVIDER_ERROR
Candidate result: expected ArithmeticException propagated
```

### 2. Provider cancellation and native service suite

```text
First Future: completed with cpu.usage = 20
Second Future: cancelled
Expected: cpu.usage remains 20 with status STALE and alert PROVIDER_ERROR
Command: ./gradlew.bat :website:test --tests '*CommandCenterMetricsServiceTest'
```

### 3. Full native checks

```text
Command: ./gradlew.bat :website:check :cbell-lib:check
Environment: GRADLE_USER_HOME=%TEMP%\chris-style-gradle-20261004
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\tmp\jds
```

### 4. Packaged candidate startup

```text
Profile: test
Mongo URI: mongodb://127.0.0.1:27018/test
Web port: 8081
GET http://127.0.0.1:8081/actuator/health/readiness
GET http://127.0.0.1:8081/
```

## Response Received

### 1. Unexpected timeout conversion failure remains visible

```text
Before implementation: invalidProviderTimeoutIsNotReportedAsAProviderFailure FAILED
After implementation: invalidProviderTimeoutIsNotReportedAsAProviderFailure PASSED
```

### 2. Provider cancellation and native service suite

```text
BUILD SUCCESSFUL in 9s
14 tests completed, 0 failures, 0 errors
cancelledProviderFutureKeepsTheLastGoodReadingAsStale PASSED
```

### 3. Full native checks

```text
BUILD SUCCESSFUL in 4m 25s
24 actionable tasks: 14 executed, 10 up-to-date
Java XML totals: 2,043 tests, 0 failures, 0 errors, 110 skipped
PowerShell worker suite: 75 passed, 0 failed, 0 skipped
```

### 4. Packaged candidate startup

```text
GET /actuator/health/readiness: connection refused
GET /: connection refused
Candidate log: Error creating bean with name 'mongoMigrationRunner'; Migration 015-require-domain-collection-schema failed.
Read-only query: database=test; required domain_collection_cutover ledger record=null
Port 8081 after exit: no listener
```

## Evidence
- Focused and full native Gradle checks passed on committed candidate `d34d8e78`.
- Read-only `mongosh` verified `db.getName()` as `test` and found no required cutover ledger record.
- Candidate log records the `test` profile, Mongo host `127.0.0.1:27018`, and migration 015 failure; the migration source calls `DomainCollectionCutoverLedger.requireTargetActive()`.
- Production web and Mongo listeners remained on ports 8080 and 27017; only the isolated test database was targeted.

## Bugs / Follow-ups
Runtime verification is incomplete. Repository instructions require database `test`, but the current target release refuses startup without a previously established domain cutover ledger. Direct database writes and bypassing this migration guard are outside the approved verification procedure. No PR was created. Resume after a supported, isolated `test` database fixture or provisioning procedure is available; rerun the packaged candidate and update this report before PR creation.

## Document Status
blocked

## Project
christopherbell-dev
