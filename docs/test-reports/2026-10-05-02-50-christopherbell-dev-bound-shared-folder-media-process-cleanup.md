# Bound Shared Folder Media Process Cleanup: Test Report

## Story/Issue
Full `christopherbell.dev` Chris Street Style code audit; draft PR #1477 is excluded. See [the dedicated implementation plan](../implementation-plans/2026-10-05-02-28-christopherbell-dev-bound-shared-folder-media-process-cleanup.md).

## Branch
`codex/bound-shared-folder-process-cleanup-20261005` at `e840c6dd`

## Pass / Fail

> [!CAUTION]
> **2 passed, 1 blocked** on candidate `e840c6dd`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Simulated process-tree termination failure | ✅ PASS | Cleanup returned within its 100 ms process wait, reported the surviving PID and kill failure, and the aggregate retained the original timeout first. |
| 2 | Full native checks and package | ✅ PASS | Website/library checks, browser checks, both full PowerShell suites and the bootable JAR completed successfully. Targeted worker suite passed 76/76; website tests had 2,041 cases with 110 skipped and no failures/errors. |
| 3 | Packaged application startup | ⏸️ BLOCKED | Candidate connected to isolated MongoDB `test`, then startup failed before readiness because migration 015 has an incomplete durable record. |

## Test Cases
1. **Simulated process-tree termination failure:** run a real sleeping child, force its termination callback to fail, and verify bounded cleanup, process identity and failure causality.
2. **Full native checks and package:** website, shared library, browser and Windows PowerShell checks plus bootable JAR packaging.
3. **Packaged application startup:** launch the committed candidate with the test profile and side-effecting jobs and integrations disabled.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, test profile |
| PowerShell | PowerShell 7, Pester 5.9.0; targeted worker suite also covers Windows PowerShell 5.1 extraction behavior |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before launch; candidate log confirmed connection to `127.0.0.1:27018`. |
| Port | 8081; free before startup and after process exit. |
| Artifact | `website/build/libs/website.jar`, SHA-256 `7FE654A8F8740F523188B2554517993167843FA7F75169B10905055AD9648726` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\bound-shared-folder-process-cleanup-20261005`
- **Candidate identity:** committed HEAD `e840c6dd53f4fc2eb582b535315683c04ae0f22b`.
- **Environment:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`.
- **Process details:** PID 16112 exited with code 1 during Spring context initialization in about 3 seconds.
- **Logs:** `%TEMP%\christopherbell-bound-media-runtime-20261005\candidate.out.log` and `candidate.err.log`.
- **Cleanup:** process exited; verified port 8081 had no listener. No database writes were made; no application route was exercised.

## Data Sent

### 1. Simulated process-tree termination failure

```text
Child process: pwsh.exe running Start-Sleep -Seconds 10
StopProcessTree callback: throws "Simulated process-tree termination failure."
Exit wait: 100 ms
Primary operation failure: TimeoutException("Media job exceeded its deadline.")
```

### 2. Full native checks and package

```text
Invoke-Pester -Path ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1 -Output Detailed
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

### 1. Simulated process-tree termination failure

```text
ProcessExited: false
Surviving child PID reported: true
Cleanup failures: simulated termination failure and bounded-wait TimeoutException
Aggregate inner exception 0: Media job exceeded its deadline.
Aggregate inner exception 1: Simulated process-tree termination failure.
Elapsed: under 3 seconds; child stopped by test cleanup.
```

### 2. Full native checks and package

```text
Focused worker Pester suite: 76 passed, 0 failed, 0 skipped.
Full PowerShell suites: 203 passed, 0 failed, 1 skipped in each suite.
Website Java tests: 2,041 total, 110 skipped, 0 failures, 0 errors.
Browser checks, :website:check, and :cbell-lib:check passed.
Bootable JAR produced.
BUILD SUCCESSFUL in 4m 10s; 24 actionable tasks.
```

### 3. Packaged application startup

```text
MongoClient connected to 127.0.0.1:27018.
ApplicationContext initialization failed: Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness and changed route were not reached.
```

## Evidence
- Candidate commit `e840c6dd53f4fc2eb582b535315683c04ae0f22b` and artifact SHA-256 recorded above.
- Final focused Pester run and serialized full gate occurred after the last code edit.
- The candidate startup log confirms the isolated database endpoint and migration blocker; the process exited and port cleanup was verified.
- An earlier overlapped Gradle invocation failed when its in-progress test-results file disappeared; the subsequent single serialized final gate passed.
- `git diff --check` passed before commit.

## Bugs / Follow-ups
Runtime acceptance remains blocked by the incomplete durable record for migration 015 in isolated database `test`. Obtain supported test fixture provisioning or recovery instructions, then rerun startup and exercise a representative route. Do not modify migration records directly or bypass the guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
