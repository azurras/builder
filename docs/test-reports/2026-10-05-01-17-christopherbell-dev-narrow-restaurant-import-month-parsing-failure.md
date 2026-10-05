# Narrow Restaurant Import Month Parsing Failure: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-01-09-christopherbell-dev-narrow-restaurant-import-month-parsing-failure.md).

## Branch
`codex/restaurant-import-month-parse-20261005` at `137bcec`

## Pass / Fail

> [!CAUTION]
> **3 native checks passed; candidate runtime is blocked** on `137bcec` before application readiness by Mongo migration 015.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Baseline import workflow characterization | ✅ PASS | Existing workflow tests passed before the implementation; valid month-only retry behavior was preserved. |
| 2 | Malformed legacy month characterization | ✅ PASS | The new fallback case passed before and after the precise exception change. |
| 3 | Full module checks | ✅ PASS | `:website:check :cbell-lib:check` completed successfully, including JavaScript and PowerShell checks. |
| 4 | Packaged candidate startup and home route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; no HTTP request could be sent. |

## Test Cases
1. **Baseline import workflow characterization:** verifies existing month-only state and retry behavior before editing.
2. **Malformed legacy month characterization:** verifies invalid stored month text follows the established missing-month retry path.
3. **Full module checks:** runs website and shared-library checks using native project tooling.
4. **Packaged candidate startup and home route:** starts the committed candidate against isolated MongoDB database `test`; requests `/` on port 8081 only if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `137bcec7f513ac5b2c07be3c5f229b2b264e473e`; JAR SHA-256 `C24D439FE9407CF9044C44C2ED4B8CE5486F55C3CF58CAE7FCFE5F0701015049` |
| Runtime | Java 25; Spring profile `test`; mail, scheduling, command center, federation and shared-folder integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before and after launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; Java loopback workaround configured using `JAVA_TOOL_OPTIONS` (local temporary directory omitted).
- **Working directory:** Repository root of isolated worktree at candidate `137bcec`.
- **Candidate process:** Foreground Java process exited with code 1 during migration initialization.
- **Logs:** `%TEMP%\chris-style-restaurant-month-137bcec7.log`.
- **Cleanup:** Candidate exited; port 8081 was free afterward. Isolated MongoDB listener on port 27018 remained running. No database records were directly modified.

## Data Sent

### 1. Baseline import workflow characterization

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.importing.RestaurantImportWorkflowServiceTest --console=plain
```

### 2. Malformed legacy month characterization

```text
RestaurantImportState.lastCompletedMonth = "invalid-month"
RestaurantImportState.lastFailedOn = 2026-09-15T08:01:00Z
Workflow time = 2026-09-16T09:00:00Z
Expected: overdue retry path attempts the existing lease boundary
```

### 3. Full module checks

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:check :cbell-lib:check --console=plain
```

### 4. Packaged candidate startup and home route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
GET http://127.0.0.1:8081/
```

## Response Received

### 1. Baseline import workflow characterization

```text
BUILD SUCCESSFUL in 23s
17 tests passed, 0 failed
```

### 2. Malformed legacy month characterization

```text
RestaurantImportWorkflowServiceTest: 18 tests passed, 0 failed
The new malformed-month characterization passed before and after implementation.
```

### 3. Full module checks

```text
BUILD SUCCESSFUL in 4m 20s
:website:check and :cbell-lib:check passed
```

### 4. Packaged candidate startup and home route

```text
MongoDB read-only check: db.getName() = test
Candidate exit code: 1
Startup: Application run failed
Cause: Migration 015-require-domain-collection-schema has an incomplete durable record.
HTTP GET /: not reached; port 8081 never became ready
Post-run listener check: port 8081 free
```

## Evidence
- Candidate `137bcec7f513ac5b2c07be3c5f229b2b264e473e` was built; its packaged JAR SHA-256 is recorded above.
- Existing workflow characterization passed before editing. The malformed-month characterization passed before and after narrowing the catch.
- Full module checks and `git diff --check` passed.
- Runtime logs show the migration runner failed before readiness. Read-only inspection confirmed database `test`; no route response was available.

## Bugs / Follow-ups
A supported fixture/provisioning or recovery procedure is required before runtime proof and PR creation. Do not repair migration state through direct Mongo writes or bypass the startup guard. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
