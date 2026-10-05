# Limit Anonymous Identity Fallback to Missing Authentication: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-00-17-christopherbell-dev-limit-anonymous-identity-fallback-to-missing-authentication.md).

## Branch
`codex/anonymous-identity-fallback-20261005` at `0838538`

## Pass / Fail

> [!CAUTION]
> **2 checks passed; candidate runtime is blocked** on `0838538` because migration 015 refuses the current isolated `test` database.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Focused post and restaurant service tests | ✅ PASS | 89 tests passed, including anonymous behavior and propagation regressions. |
| 2 | Full module checks | ✅ PASS | Gradle check passed; Java XML reports 2,166 tests, 0 failures/errors and 110 skipped; browser and PowerShell checks also passed. |
| 3 | Packaged candidate startup and public route | ⏸️ BLOCKED | Startup exited before readiness because migration 015 found a failed durable record; no HTTP response was available. |

## Test Cases
1. **Focused post and restaurant service tests:** confirms missing authentication retains anonymous behavior and unrelated identity failures propagate.
2. **Full module checks:** runs website and shared-library native validation, browser tests, and production PowerShell test suites.
3. **Packaged candidate startup and public route:** starts the committed candidate against the isolated MongoDB database `test` and requests `/` on port 8081 if readiness is reached.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `083853851a3c09a0792d5b75b0ee11a4bbb48281`; JAR SHA-256 `92C74379275FF33160E57299C533E644990D8DA525DF9D13EBE678EDBFD5E8CC` |
| Runtime | Java 25; Spring profile `test`; mail and scheduled/background integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; Java loopback workaround configured through `JAVA_TOOL_OPTIONS` (host temporary path omitted).
- **Working directory:** Repository root of the isolated spoke worktree (`.`).
- **Candidate process:** PID 33112; application exited during migration initialization before readiness.
- **Logs:** `%TEMP%\chris-style-anonymous-identity-08385385.log`.
- **Cleanup:** Candidate process exited; port 8081 was free afterward. The isolated MongoDB listener on port 27018 remained running. No database records were modified directly.

## Data Sent

### 1. Focused post and restaurant service tests

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:test --tests dev.christopherbell.post.PostServiceTest --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --console=plain
```

### 2. Full module checks

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:check :cbell-lib:check --console=plain
```

### 3. Packaged candidate startup and public route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
GET http://127.0.0.1:8081/
```

## Response Received

### 1. Focused post and restaurant service tests

```text
BUILD SUCCESSFUL in 7s
PostServiceTest: 27 tests, 0 failures
RestaurantServiceTest: 62 tests, 0 failures
```

### 2. Full module checks

```text
BUILD SUCCESSFUL in 4m 23s
:website:check and :cbell-lib:check passed
Java XML totals: 2166 tests, 0 failures, 0 errors, 110 skipped
Production.Install Pester: 203 passed, 0 failed, 1 skipped
SharedFolderWorker Pester: 75 passed, 0 failed
```

### 3. Packaged candidate startup and public route

```text
MongoDB read-only check: db.getName() = test
Read-only domain cutover ledger lookup: no active ledger found
Startup: Application run failed
Cause: Migration 015-require-domain-collection-schema has an incomplete durable record
HTTP GET /: not reached; port 8081 never became ready
```

## Evidence
- Focused red-green evidence: both new propagation tests failed on the original broad catches; after narrowing the catches, both service suites passed.
- `:website:check :cbell-lib:check` passed on the committed candidate. The `JAVA_TOOL_OPTIONS` setting used the established short temporary directory workaround for the Windows JDK loopback issue.
- Candidate JAR was built from commit `083853851a3c09a0792d5b75b0ee11a4bbb48281`; its SHA-256 is recorded above.
- The existing migration record in database `test` is marked `FAILED` for `015-require-domain-collection-schema`; its stored start time is `2026-10-05T04:52:18.967Z`. Read-only inspection confirmed the separate domain cutover ledger is absent.
- Candidate startup stopped before serving requests. The candidate PID exited and port 8081 was free afterward; the MongoDB process and production listener were not changed.

## Bugs / Follow-ups
The missing active cutover ledger caused the earlier app-owned migration attempt to persist a failed migration-015 record in the isolated database `test`; the current candidate therefore fails before the migration body can retry. Do not repair or delete it through direct database writes and do not bypass the guard. A supported test fixture/provisioning or recovery procedure is needed before runtime proof and PR creation. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
