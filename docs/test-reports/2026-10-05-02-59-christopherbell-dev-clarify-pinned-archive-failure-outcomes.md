# Clarify Pinned Archive Failure Outcomes: Test Report

## Story/Issue
Full `christopherbell.dev` Chris Street Style code audit; draft PR #1477 is excluded. See [the dedicated implementation plan](../implementation-plans/2026-10-05-02-51-christopherbell-dev-clarify-pinned-archive-failure-outcomes.md).

## Branch
`codex/clarify-pinned-archive-failures-20261005` at `a880cfd1`

## Pass / Fail

> [!CAUTION]
> **2 passed, 1 blocked** on candidate `a880cfd1`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Pinned archive resolver outcomes | ✅ PASS | Focused task preserves I/O translation, offline/cache/checksum/concurrency behavior, passes the original unchecked exception through unchanged, and verifies partial cleanup. |
| 2 | Full native checks and package | ✅ PASS | Website/library checks, browser checks, both full PowerShell suites and bootable JAR packaging passed; 2,041 website tests had 110 skips and no failures/errors. |
| 3 | Packaged application startup | ⏸️ BLOCKED | Candidate connected to isolated MongoDB `test`, then startup failed before readiness because migration 015 has an incomplete durable record. |

## Test Cases
1. **Pinned archive resolver outcomes:** task-native cache/download fixtures exercise online resolution, cached offline, missing offline cache, checksum failures, concurrent publication, I/O failure, and an unchecked programming defect.
2. **Full native checks and package:** website, shared library, browser and Windows PowerShell checks plus bootable JAR packaging.
3. **Packaged application startup:** launch the committed candidate with test profile and side-effecting jobs and integrations disabled.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, test profile |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before launch; candidate log confirmed connection to `127.0.0.1:27018`. |
| Port | 8081; free before startup and after process exit. |
| Artifact | `website/build/libs/website.jar`, SHA-256 `F0F56FCBFE105A788E3B6881D0F4CCBFA865F9EDF2D7274A2E4AA72BD1CBEC51` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\clarify-pinned-archive-failures-20261005`
- **Candidate identity:** committed HEAD `a880cfd195a053640ead97e3f0d2b540ab4f79d4`.
- **Environment:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`.
- **Process details:** PID 17016 exited with code 1 during Spring context initialization in about 3 seconds.
- **Logs:** `%TEMP%\christopherbell-archive-outcomes-runtime-20261005\candidate.out.log` and `candidate.err.log`.
- **Cleanup:** process exited; verified port 8081 had no listener. No database writes were made; no route was exercised.

## Data Sent

### 1. Pinned archive resolver outcomes

```text
gradlew.bat :website:verifySensorArchiveResolution
Injected unchecked failure: IllegalStateException("simulated downloader programming defect")
Expected result: same exception instance propagates and no partial archive remains.
```

### 2. Full native checks and package

```text
gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar
```

### 3. Packaged application startup

```text
Profile: test
Database URI: mongodb://127.0.0.1:27018/test
Port: 8081
Scheduling, command center, federation, shared folder, and mail disabled
```

## Response Received

### 1. Pinned archive resolver outcomes

```text
BUILD SUCCESSFUL in 2s
1 actionable task executed.
Existing online/offline/cache/checksum/concurrent/I/O checks passed.
Unchecked IllegalStateException propagated as the exact original instance.
No published or partial archive remained.
```

### 2. Full native checks and package

```text
Website Java tests: 2,041 total, 110 skipped, 0 failures, 0 errors.
Full PowerShell suites: 203 passed, 0 failed, 1 skipped in each suite.
Additional PowerShell suite: 75 passed, 0 failed, 0 skipped.
Browser checks, :website:check, :cbell-lib:check, and bootable JAR packaging passed.
BUILD SUCCESSFUL in 4m 48s; 24 actionable tasks.
```

### 3. Packaged application startup

```text
MongoClient connected to 127.0.0.1:27018.
ApplicationContext initialization failed: Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness and application route were not reached.
```

## Evidence
- Candidate commit `a880cfd195a053640ead97e3f0d2b540ab4f79d4` and artifact SHA-256 recorded above.
- The focused task and full serialized gate passed after the final source edit.
- Startup logs identify the isolated MongoDB endpoint and migration blocker; port cleanup was verified.
- `git diff --check` passed before commit.

## Bugs / Follow-ups
Runtime acceptance remains blocked by the incomplete durable record for migration 015 in isolated database `test`. Obtain supported test fixture provisioning or recovery instructions, then rerun startup and exercise a representative route. Do not alter migration records directly or bypass the guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
