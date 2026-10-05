# Narrow the Box Index Digest Failure: Test Report

## Story/Issue
Full `christopherbell.dev` Chris Street Style code audit; draft PR #1477 is excluded. See [the dedicated implementation plan](../implementation-plans/2026-10-05-02-20-christopherbell-dev-narrow-the-box-index-digest-failure.md).

## Branch
`codex/narrow-box-index-digest-failure-20261005` at `a6976822`

## Pass / Fail

> [!CAUTION]
> **2 passed, 1 blocked** on candidate `a6976822`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Focused digest client tests | ✅ PASS | All 17 `OfficialCanesBoxPriceClientTest` tests passed after the change. |
| 2 | Full native checks and package | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` passed; 2,041 website tests (110 skipped) and 123 library tests (0 skipped) had no failures or errors. |
| 3 | Packaged application startup | ⏸️ BLOCKED | Candidate connected to isolated MongoDB database `test`, then startup failed before readiness because migration 015 has an incomplete durable record. |

## Test Cases
1. **Focused digest client tests:** existing official response hash, metadata and source failure behavior.
2. **Full native checks and package:** website, shared library, JavaScript/browser checks, PowerShell checks and bootable JAR packaging.
3. **Packaged application startup:** launch the committed candidate with test profile and side-effecting jobs and integrations disabled.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, test profile |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before launch; candidate log confirmed connection to `127.0.0.1:27018`. |
| Port | 8081; no existing listener before startup and no listener remained afterward. |
| Artifact | `website/build/libs/website.jar`, SHA-256 `14B06CC34FB30C17721DE1B42889B0FE510B467880F78FFA507D7E0CDC72721B` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\narrow-box-index-digest-failure-20261005`
- **Candidate identity:** committed HEAD `a69768224c5f286737995c0e3c1bf71792ac3fa8`.
- **Environment:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`.
- **Process details:** PID 47320 exited with code 1 in about 3 seconds during Spring context initialization.
- **Logs:** `%TEMP%\christopherbell-digest-runtime-20261005\candidate.out.log` and `candidate.err.log`.
- **Cleanup:** process exited; verified port 8081 had no listener. No database writes were made; no route was exercised.

## Data Sent

### 1. Focused digest client tests

```text
gradlew.bat :website:test --tests dev.christopherbell.canesboxtracker.OfficialCanesBoxPriceClientTest
```

### 2. Full native checks and package

```text
gradlew.bat :website:check :cbell-lib:check :website:bootJar
```

### 3. Packaged application startup

```text
Profile: test
Database URI: mongodb://127.0.0.1:27018/test
Port: 8081
Scheduling, command center, federation, shared folder, and mail disabled
```

## Response Received

### 1. Focused digest client tests

```text
17 tests completed, 0 failed, 0 errors
```

### 2. Full native checks and package

```text
BUILD SUCCESSFUL
Website test result XML: 2,041 tests, 110 skipped, 0 failures, 0 errors.
cbell-lib test result XML: 123 tests, 0 skipped, 0 failures, 0 errors.
JavaScript/browser and Windows PowerShell checks passed.
Bootable JAR produced at website/build/libs/website.jar.
```

### 3. Packaged application startup

```text
MongoClient connected to 127.0.0.1:27018.
ApplicationContext initialization failed: Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness and changed route were not reached.
```

## Evidence
- Candidate commit: `a69768224c5f286737995c0e3c1bf71792ac3fa8`.
- Candidate artifact SHA-256 recorded above.
- Focused tests and full checks ran after the source edit; no source changes followed them before candidate commit.
- Startup log identifies the isolated Mongo endpoint and migration blocker; port cleanup was verified.
- `git diff --check` passed for the source change before commit.

## Bugs / Follow-ups
Runtime acceptance remains blocked by the incomplete durable record for migration 015 in the isolated `test` database. Obtain supported test fixture provisioning or recovery instructions, then rerun startup and exercise a representative route. Do not mutate the database directly or bypass the migration guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
