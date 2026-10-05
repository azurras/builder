# Bound Production Jar Setup Failure Cleanup: Test Report

## Story/Issue
Full `christopherbell.dev` Chris Street Style code audit; draft PR #1477 is excluded. See [the dedicated implementation plan](../implementation-plans/2026-10-05-03-00-christopherbell-dev-bound-production-jar-setup-failure-cleanup.md).

## Branch
`codex/bound-production-jar-setup-cleanup-20261005` at `2be74499`

## Pass / Fail

> [!CAUTION]
> **2 passed, 1 blocked** on candidate `2be74499`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate log setup failure cleanup | ✅ PASS | A real sleeping child was terminated after injected writer setup failure; the identical original exception was rethrown and no child remained within five seconds. |
| 2 | Full native checks and package | ✅ PASS | Website/library checks, browser checks, full PowerShell suites and bootable JAR packaging passed; website had 2,041 tests with 110 skipped and no failures/errors. |
| 3 | Packaged application startup | ⏸️ BLOCKED | Candidate connected to isolated MongoDB `test`, then startup failed before readiness because migration 015 has an incomplete durable record. |

## Test Cases
1. **Candidate log setup failure cleanup:** launch a real PowerShell child, inject a writer-construction failure after launch, and verify original failure identity plus child cleanup.
2. **Full native checks and package:** website, shared library, browser and Windows PowerShell checks plus bootable JAR packaging.
3. **Packaged application startup:** launch the committed candidate with test profile and side-effecting jobs and integrations disabled.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, test profile |
| PowerShell | PowerShell 7, Pester 5.9.0 |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before launch; candidate log confirmed connection to `127.0.0.1:27018`. |
| Port | 8081; free before startup and after process exit. |
| Artifact | `website/build/libs/website.jar`, SHA-256 `E3E00B2A7EF82FD587A462F66ACEB3E41CBD2E5BFB962DBCB416F234C7E5055D` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\bound-production-jar-setup-cleanup-20261005`
- **Candidate identity:** committed HEAD `2be74499c56b7f882be8f269adcf06a23ceca4b8`.
- **Environment:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`.
- **Process details:** PID 44888 exited with code 1 during Spring context initialization in about 3 seconds.
- **Logs:** `%TEMP%\christopherbell-prodjar-setup-runtime-20261005\candidate.out.log` and `candidate.err.log`.
- **Cleanup:** process exited; verified port 8081 had no listener. No database writes were made; no route was exercised.

## Data Sent

### 1. Candidate log setup failure cleanup

```text
Child process: pwsh.exe running Start-Sleep -Seconds 10
CreateLogWriter: throws the test's InvalidOperationException instance
Expected: exact same setup exception rethrown; child process gone within five seconds
```

### 2. Full native checks and package

```text
Invoke-Pester -Path ops/production/windows/tests/Production.Deploy.Tests.ps1 -Output Detailed
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

### 1. Candidate log setup failure cleanup

```text
Focused regression: 1 passed, 0 failed.
Full deployment Pester suite: 100 passed, 0 failed, 0 skipped.
The original InvalidOperationException object was preserved.
The child PID was absent after setup failure; elapsed time was under five seconds.
```

### 2. Full native checks and package

```text
Website Java tests: 2,041 total, 110 skipped, 0 failures, 0 errors.
Full PowerShell suites: 203 passed, 0 failed, 1 skipped in each suite.
Additional PowerShell suite: 75 passed, 0 failed, 0 skipped.
Browser checks, :website:check, :cbell-lib:check, and bootable JAR packaging passed.
BUILD SUCCESSFUL in 4m 45s; 24 actionable tasks.
```

### 3. Packaged application startup

```text
MongoClient connected to 127.0.0.1:27018.
ApplicationContext initialization failed: Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness and application route were not reached.
```

## Evidence
- Candidate commit `2be74499c56b7f882be8f269adcf06a23ceca4b8` and artifact SHA-256 recorded above.
- Focused regression, full deployment suite and full serialized gate ran after the last code edit.
- Startup log confirms isolated MongoDB endpoint and migration blocker; process exit and port cleanup were verified.
- `git diff --check` passed before commit.

## Bugs / Follow-ups
Runtime acceptance remains blocked by the incomplete durable record for migration 015 in isolated database `test`. Obtain supported test fixture provisioning or recovery instructions, then rerun startup and exercise a representative route. Do not directly edit migration state or bypass the guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
