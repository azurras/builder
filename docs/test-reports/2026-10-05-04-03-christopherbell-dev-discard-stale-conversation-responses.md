# Discard Stale Conversation Responses: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit; see the [implementation plan](../implementation-plans/2026-10-05-03-47-christopherbell-dev-discard-stale-conversation-responses.md).

## Branch
`codex/discard-stale-conversation-responses-20261005` at `f5d1e60`

## Pass / Fail

> [!CAUTION]
> **4 of 5 verification cases passed** on candidate `f5d1e60`; local application readiness is blocked by the isolated test database's existing incomplete migration 015 record.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Conversation response ordering regressions | ✅ PASS | Both regressions failed against audit-base `messages.js`; both pass on the candidate, including stale older-page success and failure behavior. |
| 2 | Focused Messages page test and syntax | ✅ PASS | Nine Messages page tests passed and `node --check` accepted the changed module. |
| 3 | Full native checks and package | ✅ PASS | Website and shared-library checks plus `bootJar` succeeded; 2,041 Java tests, 110 skipped, zero failures/errors; browser suite 382/382. |
| 4 | Committed candidate startup and Messages runtime flows | ⏸️ BLOCKED | The candidate connected to MongoDB `test`, then migration 015 stopped Spring context initialization before readiness or page access. |
| 5 | Runtime cleanup and database isolation | ✅ PASS | Candidate exited, its port was free, and read-only database identity remained `test`. |

## Test Cases
1. **Conversation response ordering regressions:** Resolved B's first page before A's, then resolved A; separately completed A's older-page success and failure after selecting B. The audit-base module failed both recipient-isolation assertions.
2. **Focused Messages page test and syntax:** Ran the committed candidate's Messages page test file and JavaScript syntax check.
3. **Full native checks and package:** Ran the full Gradle website and shared-library gate with browser tests, PowerShell suites, and packaged boot JAR creation.
4. **Committed candidate startup and Messages runtime flows:** Attempted the packaged candidate with profile `test`, MongoDB database `test`, disabled scheduled/integration work, and a free port. Startup failed before UI readiness, so message-page runtime interactions could not be exercised.
5. **Runtime cleanup and database isolation:** Checked the Java process, selected listener port, and database identity after startup failed.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, `test` profile |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before and after launch |
| Port | `63218`, selected from an OS-assigned free port; free after exit |
| Artifact | `website/build/libs/website.jar`, SHA-256 `4602FF317A6E8B94C92DBA5F378239C3FFD5E43AE688C27B428B9138964B3E8C` |
| Isolation | Scheduling, command center, federation, shared-folder service, music, and mail disabled; scratch roots placed under the system temporary directory |
| JDK workaround | `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=63218 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\discard-stale-conversation-responses-20261005`
- **Candidate identity:** committed HEAD `f5d1e6001a6951cb5dd8c8c2f5c5b14b005e8e0c`.
- **Environment:** `SPRING_PROFILES_ACTIVE=test`, `SPRING_DATA_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`, temporary shared-folder roots, and the JDK workaround above.
- **Process details:** Hidden Java process PID `15248` exited with code `1` after about four seconds.
- **Logs:** `C:\Users\CHRIST~1\AppData\Local\Temp\cbdev-discard-stale-conversation-responses-20261005\candidate-f5d1e600.stdout.log` and matching `.stderr.log`.
- **Cleanup:** Confirmed PID `15248` absent and port `63218` free. No direct database writes were performed.

## Data Sent

### 1. Conversation response ordering regressions

```text
Case A: open alice; open bob; resolve bob's first page; resolve alice's first page.
Expected: title, profile URL, browser URL, and displayed message remain bob.

Case B: open alice and resolve its first page with cursor alice-older; request that older page; select bob and resolve bob's first page; resolve alice's older page.
Expected: only bob's message remains and the older-message button is not disabled by alice's stale request.

Case C: request alice's older page, select bob, then reject alice's request.
Expected: bob's message remains and no stale Alice error appears.
```

### 2. Focused Messages page test and syntax

```text
node --check website/src/main/resources/static/js/messages.js
node --test website/src/test/js/messages-rendering.test.js
```

### 3. Full native checks and package

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar
```

### 4. Committed candidate startup and Messages runtime flows

```text
Profile: test
MongoDB URI: mongodb://127.0.0.1:27018/test
Port: 63218
Scheduling, command center, federation, shared-folder service, music, and mail disabled
Launch committed boot JAR and wait for readiness, then exercise both Messages ordering cases if ready.
```

### 5. Runtime cleanup and database isolation

```text
Read-only command before and after: mongosh mongodb://127.0.0.1:27018/test --quiet --eval db.getName()
Process check: PID 15248
Listener check: TCP port 63218
```

## Response Received

### 1. Conversation response ordering regressions

```text
Audit-base implementation: 2 failed, 7 passed; the late first page rendered Alice under Bob, and the late older page merged Alice into Bob.
Committed candidate: 9 passed, 0 failed. Late first-page, stale older-page success, stale older-page error, selected title/profile/URL, and pagination-button assertions passed.
```

### 2. Focused Messages page test and syntax

```text
node --check: exit 0
Messages page tests: 9 passed, 0 failed
```

### 3. Full native checks and package

```text
BUILD SUCCESSFUL in 4m 44s
:website:check: passed
:cbell-lib:check: passed
:website:bootJar: passed
Java test results: 2,041 tests, 110 skipped, 0 failures, 0 errors
Browser suite on committed candidate: 382 passed, 0 failed
PowerShell suites included by the full check: passed
```

### 4. Committed candidate startup and Messages runtime flows

```text
Application active profile: test
Mongo client target: 127.0.0.1:27018
ApplicationContext initialization failed:
Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness was not reached; Messages page interactions were not run.
```

### 5. Runtime cleanup and database isolation

```text
Process PID 15248: absent after exit
Port 63218: free
mongosh db.getName(): test before and after
No direct database writes were made.
```

## Evidence
- Baseline commit: `695a3ed8617f9b4ab07abb7413baf369c58acf6`; the first-page and older-page recipient-isolation regressions both failed against its module.
- Candidate commit: `f5d1e6001a6951cb5dd8c8c2f5c5b14b005e8e0c`; candidate worktree is clean.
- Full gate and committed browser suite were run from `A:\Projects\christopherbell.dev-worktrees\discard-stale-conversation-responses-20261005`.
- Startup log identifies migration `015-require-domain-collection-schema` as the failure. Database checks were read-only.
- The audit excludes draft PR #1477; no PR was created.

## Bugs / Follow-ups
AC-3 remains blocked until supported isolated test-database recovery or provisioning allows the committed application to reach readiness. Do not modify migration state directly or bypass the startup guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
