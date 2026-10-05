# Restore restaurant import interruption: Test Report

## Story/Issue
User-requested Chris Street Style audit correction; draft PR #1477 remains excluded and was not used as evidence.

## Branch
`codex/restore-restaurant-import-interruption-20261005` at `2001573`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed; local application startup is blocked** on candidate `2001573`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Import interruption-order regression and focused workflow suite | ✅ PASS | The new regression failed on base `695a3ed`, then all 18 workflow tests passed on the candidate. |
| 2 | Full native check and package gate | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` completed successfully; 2,165 Java tests were reported, 110 skipped, with no failures or errors. |
| 3 | Committed application startup against isolated test database | ⏸️ BLOCKED | The candidate connected to database `test` and stopped at the existing incomplete durable record for migration 015 before readiness. |

## Test Cases
1. **Import interruption-order regression and focused suite:** Verified failed state `FAILED/INTERRUPTED`, the same propagated `InterruptedException`, an un-interrupted thread during failed-state persistence and exact lease release, and a restored flag after cleanup. The regression failed on base `695a3ed`; the candidate workflow suite passed 18/18.
2. **Full native check and package gate:** Ran browser, Java, PowerShell, production build checks, and executable package task.
3. **Committed application startup:** Launched the candidate JAR with test profile, explicit MongoDB database `test`, loopback-only port 53179, scheduling disabled, and isolated test storage paths.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot application |
| Candidate | Commit `2001573`; JAR SHA-256 `10B8E3F84DB56CEA2E94ECB73D80DCA6010C7FF8B73614FC2300F9C3E0FA318C` |
| Runtime | JDK 25; `test` profile; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk` |
| Database | `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before startup |
| HTTP binding | `127.0.0.1:53179`; OS-assigned candidate port was confirmed free before startup |
| Background work | Scheduling, Canes tracker, monthly restaurant import, mail, and federation switches disabled |
| Test storage | `C:\Temp\restaurant-import-interruption-20261005\shared` and `...\system` |

## Local Run Details
- **Local command:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk java.exe -jar website\build\libs\website.jar --spring.profiles.active=test --spring.data.mongodb.uri=mongodb://127.0.0.1:27018/test --server.address=127.0.0.1 --server.port=53179 --app.scheduling.enabled=false --app.shared-folder.root=C:/Temp/restaurant-import-interruption-20261005/shared --app.shared-folder.system-root=C:/Temp/restaurant-import-interruption-20261005/system --canes-box-tracker.enabled=false --wfl.restaurant-import.monthly.enabled=false --app.mail.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\restore-restaurant-import-interruption-20261005`
- **Candidate identity:** Committed `HEAD` `2001573`, built by `:website:bootJar` in the full gate.
- **Process details:** Hidden `Start-Process` candidate PID 46468 exited during Spring context startup; no listener remained on port 53179.
- **Logs:** `C:\Temp\restaurant-import-candidate.out.log` and `C:\Temp\restaurant-import-candidate.err.log`.
- **Cleanup:** Confirmed candidate exited and port 53179 had no listener. MongoDB data was not changed directly.

## Data Sent

### 1. Import interruption-order regression and focused suite

```text
Gradle: :website:test --tests dev.christopherbell.whatsforlunch.restaurant.importing.RestaurantImportWorkflowServiceTest
Dependency behavior: restaurantService.applyPreparedImport throws one InterruptedException instance
```

### 2. Full native check and package gate

```text
Gradle: :website:check :cbell-lib:check :website:bootJar
Gradle options: --no-parallel --max-workers=4
```

### 3. Committed application startup

```text
Profile: test
Mongo URI: mongodb://127.0.0.1:27018/test
Address/port: 127.0.0.1:53179
Scheduling, Canes tracker, monthly restaurant import, mail, and federation: disabled
Shared-folder roots: C:\Temp\restaurant-import-interruption-20261005\shared and C:\Temp\restaurant-import-interruption-20261005\system
```

## Response Received

### 1. Import interruption-order regression and focused suite

```text
Base 695a3ed: new interruption-order regression FAILED because failed-state persistence observed the thread already interrupted.
Candidate 2001573: 18 tests completed, 0 failed; BUILD SUCCESSFUL.
```

### 2. Full native check and package gate

```text
BUILD SUCCESSFUL in 4m 24s
Java test results: 2,165 total; 110 skipped; 0 failures; 0 errors.
Browser, PowerShell, website checks, cbell-lib checks, and website bootJar tasks completed successfully.
```

### 3. Committed application startup

```text
Candidate log: Migration 015-require-domain-collection-schema has an incomplete durable record.
Database identity verified read-only before launch: test.
Readiness: not reached.
Listener after exit: none on 127.0.0.1:53179.
```

## Evidence
- Full gate command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar` — `BUILD SUCCESSFUL`.
- Focused command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:test --tests dev.christopherbell.whatsforlunch.restaurant.importing.RestaurantImportWorkflowServiceTest` — 18/18 passed.
- Read-only isolation check: `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'` — `test`.
- Candidate JAR SHA-256: `10B8E3F84DB56CEA2E94ECB73D80DCA6010C7FF8B73614FC2300F9C3E0FA318C`.

## Bugs / Follow-ups
- Runtime verification and PR publication are blocked by the existing incomplete durable record for migration 015 in isolated database `test`. No database writes or bypasses were attempted. Resume only after supported test-database provisioning or recovery makes startup verifiable.
- A source-review note initially described the scheduled wrapper as losing interruption; source inspection showed that `safeCategory` restores the flag too early instead. The plan records this refinement and the corrected cleanup-order contract.

## Document Status
blocked

## Project
christopherbell-dev
