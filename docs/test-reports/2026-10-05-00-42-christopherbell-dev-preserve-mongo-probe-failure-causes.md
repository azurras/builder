# Preserve Mongo Probe Failure Causes: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-00-34-christopherbell-dev-preserve-mongo-probe-failure-causes.md).

## Branch
`codex/precise-mongo-probe-failures-20261005` at `0fb75ef`

## Pass / Fail

> [!CAUTION]
> **4 verification checks passed; packaged runtime is blocked** on `0fb75ef` because database `test` contains a failed migration-015 record and lacks the active cutover ledger.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Focused Mongo probe tests | ✅ PASS | 3 tests passed for ping failure, identity cause retention and oversized timeout handling. |
| 2 | Database health configuration test | ✅ PASS | The existing health indicator contract passed. |
| 3 | Full module checks | ✅ PASS | Gradle checks passed; Java XML reports 2,167 tests, 0 failures/errors and 110 skipped. |
| 4 | Packaged candidate startup and public route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; the home request could not be sent. |

## Test Cases
1. **Focused Mongo probe tests:** verifies a failed ping returns false, identity failures retain the wrapped Mongo cause, and an oversized timeout fails before Mongo work starts.
2. **Database health configuration test:** confirms the backend-neutral database health contributor remains UP with its established safe details.
3. **Full module checks:** runs website and shared-library checks, including JavaScript and PowerShell checks.
4. **Packaged candidate startup and public route:** starts the committed candidate against isolated database `test` and requests `/` on port 8081 if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `0fb75ef3e3d9233eac7228afce27b2e1288ae6ba`; JAR SHA-256 `DF2954A5F23BB1D1F85A678F80AAC924DD25F4130526B956ABF84F66B067C438` |
| Runtime | Java 25; Spring profile `test`; mail and scheduled/background integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; Java loopback workaround configured through `JAVA_TOOL_OPTIONS` (host temporary path omitted).
- **Working directory:** Repository root of the isolated spoke worktree (`.`).
- **Candidate process:** Foreground Java process exited during migration initialization before readiness.
- **Logs:** `%TEMP%\chris-style-mongo-probe-0fb75ef3.log`.
- **Cleanup:** Candidate process exited; port 8081 was free afterward. Isolated MongoDB listener on port 27018 remained running. No database records were modified directly.

## Data Sent

### 1. Focused Mongo probe tests

```text
ping(Duration.ofSeconds(1)) with MongoTemplate.executeCommand throwing IllegalStateException
identity(Duration.ofSeconds(1)) with MongoDatabase.getName throwing IllegalArgumentException
ping(Duration.ofSeconds(Long.MAX_VALUE))
```

### 2. Database health configuration test

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.metrics.DatabaseHealthConfigurationTest --console=plain
```

### 3. Full module checks

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:check :cbell-lib:check --console=plain
```

### 4. Packaged candidate startup and public route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
GET http://127.0.0.1:8081/
```

## Response Received

### 1. Focused Mongo probe tests

```text
MongoDatabaseConnectivityProbeTest: 3 tests passed, 0 failed
BUILD SUCCESSFUL in 6s
```

### 2. Database health configuration test

```text
DatabaseHealthConfigurationTest: passed
BUILD SUCCESSFUL in 21s
```

### 3. Full module checks

```text
BUILD SUCCESSFUL in 4m 30s
:website:check and :cbell-lib:check passed
Java XML totals: 2167 tests, 0 failures, 0 errors, 110 skipped
```

### 4. Packaged candidate startup and public route

```text
MongoDB read-only check: db.getName() = test
Migration 015 record: status FAILED
Domain cutover ledger lookup: no active ledger found
Startup: Application run failed
Cause: Migration 015-require-domain-collection-schema has an incomplete durable record
HTTP GET /: not reached; port 8081 never became ready
```

## Evidence
- The new focused tests failed on the original code for two cases: identity failure lost its cause, and oversized timeout conversion was swallowed. The ping failure fallback passed on baseline. All three focused tests pass on candidate `0fb75ef`.
- Full module checks passed on the candidate; Java XML totals are recorded above. The Windows JDK loopback workaround used the established short temporary directory setting.
- Candidate JAR SHA-256 is recorded above and was built from commit `0fb75ef3e3d9233eac7228afce27b2e1288ae6ba`.
- Read-only inspection confirmed the active database name is `test`, migration 015 is already `FAILED`, and the required domain cutover ledger is absent. Candidate startup exited before serving requests; port 8081 was free afterward.

## Bugs / Follow-ups
The application refuses to retry the failed durable migration record. Do not repair or delete it through direct database writes and do not bypass the startup guard. A supported test fixture or recovery procedure is required before runtime proof and PR creation. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
