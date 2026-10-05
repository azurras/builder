# Preserve scheduled collector interruption: Test Report

## Story/Issue
User-requested Chris Street Style audit correction; draft PR #1477 remains excluded and was not used as evidence.

## Branch
`codex/preserve-scheduled-collector-interruption-20261005` at `a1945a6`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed; local application startup is blocked** on candidate `a1945a6`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Interruption regression and focused coordinator suite | ✅ PASS | The regression failed on the untouched base, then the candidate focused suite passed 5/5. |
| 2 | Full native check and package gate | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` completed successfully; 2,165 Java tests were reported, 110 skipped, with no failures or errors. |
| 3 | Committed application startup against isolated test database | ⏸️ BLOCKED | The candidate connected to database `test` and stopped at the existing incomplete durable record for migration 015 before readiness. |

## Test Cases
1. **Interruption regression and focused suite:** Verified that interrupted work keeps the original cause, saves FAILED status, releases its exact lease owner, and restores the interrupt flag after cleanup. The new regression failed against base `695a3ed` before implementation; all five focused tests passed on the candidate.
2. **Full native check and package gate:** Ran browser, Java, PowerShell, production build checks, and the executable package task.
3. **Committed application startup:** Launched the candidate JAR with the test profile, explicit MongoDB database `test`, a loopback-only ephemeral candidate port, scheduling disabled, and test-local resource roots.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot application |
| Candidate | Commit `a1945a6`; JAR SHA-256 `F3EE0514A7A46AD204E3E424019C2DE41D5034BCC1F88A709CD929E7F3CC2A7A` |
| Runtime | JDK 25; `test` profile; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk` |
| Database | `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before startup |
| HTTP binding | `127.0.0.1:63216`; no listener occupied the port before startup |
| Background work | `app.scheduling.enabled=false`; Canes tracker, monthly restaurant import, mail, and federation switches disabled |
| Test storage | `C:\Temp\christopherbell-style-interruption-20261005\shared` and `...\system` |

## Local Run Details
- **Local command:** `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk java.exe -jar website\build\libs\website.jar --spring.profiles.active=test --spring.data.mongodb.uri=mongodb://127.0.0.1:27018/test --server.address=127.0.0.1 --server.port=63216 --app.scheduling.enabled=false --app.shared-folder.root=C:/Temp/christopherbell-style-interruption-20261005/shared --app.shared-folder.system-root=C:/Temp/christopherbell-style-interruption-20261005/system --canes-box-tracker.enabled=false --wfl.restaurant-import.monthly.enabled=false --app.mail.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\preserve-scheduled-collector-interruption-20261005`
- **Candidate identity:** Committed `HEAD` `a1945a6`, built by `:website:bootJar` in the full gate.
- **Process details:** `Start-Process` launched the candidate; it exited during Spring context startup. Port 63216 was free afterward, with no listener.
- **Logs:** `C:\Temp\candidate2.out.log` and `C:\Temp\candidate2.err.log`.
- **Cleanup:** Confirmed candidate startup had exited and port 63216 had no listener. MongoDB data was not changed directly.

## Data Sent

### 1. Interruption regression and focused suite

```text
Gradle: :cbell-lib:test --tests dev.christopherbell.libs.mongo.lease.ScheduledCollectorCoordinatorTest
Work input: throw the same InterruptedException instance from Work.execute
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
Address/port: 127.0.0.1:63216
Scheduling: disabled
Canes tracker, monthly restaurant import, mail, and federation: disabled
Shared-folder roots: C:\Temp\christopherbell-style-interruption-20261005\shared and C:\Temp\christopherbell-style-interruption-20261005\system
```

## Response Received

### 1. Interruption regression and focused suite

```text
Base 695a3ed: new interruption regression FAILED because the current thread interrupt flag was not restored.
Candidate a1945a6: 5 tests completed, 0 failed; BUILD SUCCESSFUL.
```

### 2. Full native check and package gate

```text
BUILD SUCCESSFUL in 4m 40s
Java test results: 2,165 total; 110 skipped; 0 failures; 0 errors.
Browser, PowerShell, website checks, cbell-lib checks, and website bootJar tasks completed successfully.
```

### 3. Committed application startup

```text
Candidate log: Caused by java.lang.IllegalStateException: Migration 015-require-domain-collection-schema has an incomplete durable record.
Database identity verified read-only before launch: test.
Readiness: not reached.
Listener after exit: none on 127.0.0.1:63216.
```

## Evidence
- Full gate command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar` — `BUILD SUCCESSFUL`.
- Focused command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :cbell-lib:test --tests dev.christopherbell.libs.mongo.lease.ScheduledCollectorCoordinatorTest` — 5/5 passed.
- Read-only isolation check: `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'` — `test`.
- Candidate JAR SHA-256: `F3EE0514A7A46AD204E3E424019C2DE41D5034BCC1F88A709CD929E7F3CC2A7A`.

## Bugs / Follow-ups
- Runtime verification and PR publication are blocked by the existing incomplete durable record for migration 015 in isolated database `test`. No database writes or bypasses were attempted. Resume only after supported test-database provisioning or recovery makes startup verifiable.
- The unrelated candidate-worktree `gradlew.bat` line-ending change was preserved and excluded from commit `a1945a6`.

## Document Status
blocked

## Project
christopherbell-dev
