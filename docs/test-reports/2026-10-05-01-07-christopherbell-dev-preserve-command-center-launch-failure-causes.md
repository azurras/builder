# Preserve Command Center Launch Failure Causes: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-01-00-christopherbell-dev-preserve-command-center-launch-failure-causes.md).

## Branch
`codex/command-center-launch-causes-20261005` at `ad758de`

## Pass / Fail

> [!CAUTION]
> **3 native checks passed; candidate runtime is blocked** on `ad758de` before application readiness by Mongo migration 015.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Baseline launch failure regressions | ✅ PASS | Both new assertions failed before the implementation, detecting cause loss and runtime exception wrapping. |
| 2 | Focused command-center action tests | ✅ PASS | All 33 cases passed, including cause retention and reservation rollback. |
| 3 | Full module checks | ✅ PASS | `:website:check :cbell-lib:check` completed successfully, including JavaScript and PowerShell checks. |
| 4 | Packaged candidate startup and home route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; no HTTP request could be sent. |

## Test Cases
1. **Baseline launch failure regressions:** verifies the current implementation drops the `IOException` cause and translates unrelated runtime failures.
2. **Focused command-center action tests:** verifies safe error text with retained cause, runtime exception propagation, and cleanup of a reserved power action.
3. **Full module checks:** runs the website and shared library checks with native project tooling.
4. **Packaged candidate startup and home route:** starts the committed candidate against isolated MongoDB database `test`; requests `/` on port 8081 only if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `ad758ded9eb10286441e4908bf2abb2efcd50998`; JAR SHA-256 `638F73C5E14321FC549DADA432413E632CE775BC326FFCCB78EEB852C18FB88A` |
| Runtime | Java 25; Spring profile `test`; mail, scheduling, command center, federation and shared-folder integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before and after launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; Java loopback workaround configured using `JAVA_TOOL_OPTIONS` (local temporary directory omitted).
- **Working directory:** Repository root of isolated worktree at candidate `ad758de`.
- **Candidate process:** Foreground Java process exited with code 1 during migration initialization.
- **Logs:** `%TEMP%\chris-style-command-center-launch-ad758ded.log`.
- **Cleanup:** Candidate exited; port 8081 was free afterward. The isolated MongoDB listener on port 27018 remained running. No database records were directly modified.

## Data Sent

### 1. Baseline launch failure regressions

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.action.CommandCenterActionServiceTest --console=plain
```

### 2. Focused command-center action tests

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.action.CommandCenterActionServiceTest --console=plain
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

### 1. Baseline launch failure regressions

```text
CommandCenterActionServiceTest: both new assertions failed on baseline
IOException cause assertion: failed
Unexpected runtime propagation assertion: failed
```

### 2. Focused command-center action tests

```text
BUILD SUCCESSFUL in 8s
33 tests passed, 0 failed
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
- Candidate `ad758ded9eb10286441e4908bf2abb2efcd50998` was built; its JAR SHA-256 is recorded above.
- The focused baseline run failed both new assertions; the committed candidate passes all 33 action-service tests.
- Full `:website:check :cbell-lib:check` and `git diff --check` passed.
- Runtime logs show the migration runner failed before readiness. Read-only verification confirmed database `test`; the route was not exercised.

## Bugs / Follow-ups
A supported fixture/provisioning or recovery procedure is required before runtime proof and PR creation. Do not repair migration state through direct Mongo writes or bypass the startup guard. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
