# Preserve Downstream Security Filter Failures: Test Report

## Story/Issue
Full `christopherbell.dev` Chris Street Style code audit; draft PR #1477 is explicitly excluded. See [the focused implementation plan](../implementation-plans/2026-10-05-03-12-christopherbell-dev-preserve-downstream-security-filter-failures.md).

## Branch
`codex/preserve-downstream-filter-failures-20261005` at `9820b394`

## Pass / Fail

> [!CAUTION]
> **3 passed, 1 blocked** on candidate `9820b394`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Filter regressions and full native checks | ✅ PASS | All 18 focused filter tests passed; the full website/library/browser/PowerShell/package gate passed with 2,045 website tests, 110 skipped and no failures/errors. |
| 2 | Standalone deployment PowerShell suite | ✅ PASS | Production deployment Pester suite passed all 99 tests. |
| 3 | Candidate startup on isolated test database | ⏸️ BLOCKED | The committed JAR connected to MongoDB database `test`, then startup stopped at the existing incomplete durable record for migration 015 before readiness. |
| 4 | Runtime cleanup and target isolation | ✅ PASS | Candidate exited with code 1, PID 19732 was absent, port 8081 was free, and read-only database identity remained `test`. |

## Test Cases
1. **Filter regressions and full native checks:** Valid bearer authentication reached a failing downstream chain on public and protected paths. The same `IOException` or `ServletException` object propagated, and each chain ran once. Then the full website/library/browser/PowerShell checks and bootable JAR task ran.
2. **Standalone deployment PowerShell suite:** Ran the repository deployment Pester suite.
3. **Candidate startup on isolated test database:** Started the committed bootable JAR with the `test` profile, isolated Mongo URI, disabled scheduled work/integrations and port 8081.
4. **Runtime cleanup and target isolation:** Checked candidate process exit, listener cleanup and database identity using read-only inspection.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, test profile |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before and after launch. |
| Port | 8081; free before and after startup attempt. |
| Artifact | `website/build/libs/website.jar`, SHA-256 `D000191AAD67A65B70A269E5E9A9420480345BF32F527AEC8116CE41B1D1DC30` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\preserve-downstream-filter-failures-20261005`
- **Candidate identity:** committed HEAD `9820b39462d0113854a5ae20523350a0fd1c6d57`.
- **Environment:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_DATA_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`.
- **Process details:** Java PID 19732 exited with code 1 during Spring context initialization in about 4 seconds.
- **Logs:** Foreground stdout/stderr captured by the verification command session; no repository log files created.
- **Cleanup:** Candidate exited; confirmed no PID 19732 and no listener on port 8081. No direct database writes were made; no application route was exercised.

## Data Sent

### 1. Filter regressions and full native checks

```text
Focused test: dev.christopherbell.configuration.JwtAuthenticationFilterTest
Valid signed bearer token and active account
For each of public and protected request matchers:
  downstream FilterChain throws one known IOException or ServletException object
Expected: same exception object reaches caller and FilterChain call count is 1

Full gate:
gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar
```

### 2. Standalone deployment PowerShell suite

```text
Invoke-Pester -Path ops/production/windows/tests/Production.Deploy.Tests.ps1 -Output Detailed
```

### 3. Candidate startup on isolated test database

```text
Profile: test
MongoDB URI: mongodb://127.0.0.1:27018/test
Port: 8081
Scheduling, command center, federation discovery/inbound/outbound, shared folder and mail disabled
```

### 4. Runtime cleanup and target isolation

```text
Read-only command: mongosh mongodb://127.0.0.1:27018/test --quiet --eval db.getName()
Process check: PID 19732
Listener check: TCP port 8081
```

## Response Received

### 1. Filter regressions and full native checks

```text
Baseline: both new downstream IOException regressions failed before the filter change.
Candidate focused filter suite: 18 passed, 0 failed.
Full gate: BUILD SUCCESSFUL in 4m 27s.
Website Java tests: 2,045 total, 110 skipped, 0 failures, 0 errors.
Embedded PowerShell suites: 203 passed, 0 failed, 1 skipped in each suite.
Additional shared-folder worker suite: 75 passed, 0 failed, 0 skipped.
Browser tests, :website:check, :cbell-lib:check and :website:bootJar passed.
git diff --check passed.
```

### 2. Standalone deployment PowerShell suite

```text
Tests Passed: 99
Failed: 0
Skipped: 0
```

### 3. Candidate startup on isolated test database

```text
Application started with active profile "test".
Mongo client cluster target: 127.0.0.1:27018.
ApplicationContext initialization failed:
Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness and application routes were not reached.
```

### 4. Runtime cleanup and target isolation

```text
Candidate process: exited; no PID 19732 remained.
Port 8081: free.
mongosh db.getName(): test.
```

## Evidence
- Baseline focused run failed at both new protected/public downstream IOException propagation assertions.
- Candidate focused run passed all 18 filter tests.
- Full serialized Gradle gate passed, including 2,045 website tests (110 skipped), browser checks, PowerShell check tasks and bootable package.
- Standalone deployment Pester suite passed 99/99.
- Runtime output from PID 19732 shows MongoDB target host 127.0.0.1:27018 and migration-015 startup blocker. Read-only database checks confirmed `test`.
- Candidate source commit `9820b39462d0113854a5ae20523350a0fd1c6d57`; the worktree was clean after commit.

## Bugs / Follow-ups
Runtime acceptance remains blocked by the incomplete durable record for migration 015 in isolated database `test`. Obtain supported test-fixture provisioning or recovery instructions, then rerun startup and exercise a representative route. Do not edit migration state directly or bypass the guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
