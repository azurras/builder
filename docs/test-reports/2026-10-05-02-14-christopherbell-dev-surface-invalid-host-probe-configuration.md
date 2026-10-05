# Surface Invalid Host Probe Configuration: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit with separate evidence for each correction; draft PR #1477 is excluded. [Implementation plan](../implementation-plans/2026-10-05-02-01-christopherbell-dev-surface-invalid-host-probe-configuration.md).

## Branch
`codex/narrow-host-probe-failures-20261005` at `f3854fbd`

## Pass / Fail

> [!CAUTION]
> **2 of 3 checks passed** on candidate `f3854fbd`; packaged runtime proof is blocked by the test database migration 015 durable-record guard.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Host metrics failure classification | ✅ PASS | The missing-timeout regression failed against the broad catches and passed after correction; all 5 focused provider tests pass, including explicit unavailable readings. |
| 2 | Full checks and packaged artifact | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` succeeded. Website Java: 2,042 tests, 0 failures/errors, 110 skipped; cbell-lib and browser/PowerShell checks completed. |
| 3 | Packaged startup and application route | ⏸️ BLOCKED | Java started Spring/Tomcat initialization but the app failed before readiness at migration 015; no route could be requested. |

## Test Cases
1. **Host metrics failure classification:** A null provider timeout must propagate as `NullPointerException`; expected unavailable probe results remain `UNAVAILABLE`.
2. **Full checks and packaged artifact:** Ran the website, shared library, browser, operational PowerShell checks, and boot JAR task.
3. **Packaged startup and application route:** Started the committed JAR on port 8081 with `test` profile, isolated test MongoDB and side-effecting features disabled; the app did not reach readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot website |
| Candidate | `f3854fbdf3f62550ded80aeeef456a4b2503cf1a0` |
| Runtime | Java 25.0.3; `test` profile; packaged `website.jar` |
| Database | `mongodb://127.0.0.1:27018/test`; read-only preflight returned `database=test` |
| Port / URL | 8081 / `http://127.0.0.1:8081`; free before launch and after failed startup |
| Environment | `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\\Temp\\site-audit-jdk` |
| Artifact | `website/build/libs/website.jar`, SHA-256 `F71817F4FCFCDA3467CB8C5F3C88BB30AFA78FCB20D32AB2EEE1BB6CC3343954` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\\Projects\\christopherbell.dev-worktrees\\narrow-host-probe-failures-20261005`
- **Candidate identity:** branch `codex/narrow-host-probe-failures-20261005`, commit `f3854fbdf3f62550ded80aeeef456a4b2503cf1a0`.
- **Process details:** Java PID 1876 exited with code 1 during Spring context initialization; Tomcat initialization logged port 8081 before failure.
- **Logs:** Captured from the local Java command output; no persistent log file configured.
- **Cleanup:** Failed startup process exited; port 8081 was confirmed free. No database writes were performed.

## Data Sent

### 1. Host metrics failure classification

```text
Gradle focused test: :website:test --tests dev.christopherbell.admin.commandcenter.metrics.ApplicationHostMetricsProviderTest
Input: CommandCenterProperties.providerTimeout = null
Expected: ApplicationHostMetricsProvider.read(...) propagates NullPointerException rather than returning unavailable readings.
```

### 2. Full checks and packaged artifact

```text
Gradle: :website:check :cbell-lib:check :website:bootJar --no-daemon --max-workers=1 --console=plain
```

### 3. Packaged startup and application route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
```

## Response Received

### 1. Host metrics failure classification

```text
Original broad-catch regression: FAILED as expected (missing timeout was represented as unavailable).
Focused candidate suite: 5 tests passed, 0 failures.
```

### 2. Full checks and packaged artifact

```text
BUILD SUCCESSFUL in 4m 32s
24 actionable tasks: 17 executed, 7 up-to-date
website Java tests: 2042; failures: 0; errors: 0; skipped: 110
cbell-lib check: passed
PowerShell checks: 75 passed, 0 failed
```

### 3. Packaged startup and application route

```text
Tomcat initialized with port 8081 (http)
ApplicationContext startup failed before readiness.
Caused by: java.lang.IllegalStateException: Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1
No HTTP response: the application did not become ready.
Port 8081 after exit: free.
```

## Evidence
- Focused baseline `ApplicationHostMetricsProviderTest` passed all 4 pre-existing tests before adding the regression.
- New missing-timeout regression failed against the original catch-all boundaries, then all 5 focused tests passed after removing `read()`'s fallback and narrowing helper catches.
- Full project gate completed successfully; website Java XML results show 2,042 tests, 0 failures/errors, 110 skipped. PowerShell reported 75 passed, 0 failed.
- Read-only database preflight confirmed the test database name. Runtime attempt on 2026-10-05 reached Tomcat initialization, then failed at migration 015 before readiness.
- `git diff --check` passed. Candidate commit contains only the host metrics provider and its focused test.

## Bugs / Follow-ups
Runtime proof and any PR remain blocked until a supported test database fixture or recovery path is available. Do not directly change the migration record or bypass the guard. No application route behavior was verified.

## Document Status
blocked

## Project
christopherbell-dev
