# Disable Test Profile Scheduling: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit; see the [implementation plan](../implementation-plans/2026-10-05-04-06-christopherbell-dev-disable-test-profile-scheduling.md).

## Branch
`codex/disable-test-profile-scheduling-20261005` at `2a24d6c`

## Pass / Fail

> [!CAUTION]
> **3 of 4 verification cases passed** on candidate `2a24d6c`; local application readiness is blocked by the isolated test database's existing incomplete migration 015 record.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Test-profile scheduling regression | ✅ PASS | The regression failed before the YAML change and passed when the actual test profile disabled scheduler registration; all 5 focused configuration tests passed. |
| 2 | Full native checks and package | ✅ PASS | Website and shared-library checks plus `bootJar` succeeded; 2,042 Java tests, 110 skipped, zero failures/errors; browser suite 382/382. |
| 3 | Committed candidate startup on isolated test DB | ⏸️ BLOCKED | The packaged candidate connected to MongoDB `test`, then migration 015 stopped Spring context initialization before readiness. |
| 4 | Runtime cleanup and database isolation | ✅ PASS | Candidate exited, its port was free, and read-only database identity remained `test`. |

## Test Cases
1. **Test-profile scheduling regression:** Loaded `application-test.yml` through Spring's YAML property loader and verified `SchedulingConfiguration` did not register scheduled-task processing. The same test failed on the audit base because the profile property was absent.
2. **Full native checks and package:** Ran the complete website/shared-library check and packaged the boot JAR.
3. **Committed candidate startup on isolated test DB:** Started the committed JAR with profile `test` and isolated MongoDB database `test`, without a scheduling-property override.
4. **Runtime cleanup and database isolation:** Checked candidate process, listener port, and database identity after startup failed.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, `test` profile |
| Database | MongoDB `127.0.0.1:27018/test`; read-only `db.getName()` returned `test` before and after launch |
| Port | `58066`, selected from an OS-assigned free port; free after exit |
| Artifact | `website/build/libs/website.jar`, SHA-256 `8C499D44486469C29B89465DDBA850EE862AB9713730313033A16C40B5822C2A` |
| Isolation | No scheduling override; command center, federation, shared-folder service, music, and mail disabled; scratch roots placed under the system temporary directory |
| JDK workaround | `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=58066 --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\disable-test-profile-scheduling-20261005`
- **Candidate identity:** committed HEAD `2a24d6c7232e2771a86f85395a69f2709f1af1ff`.
- **Environment:** `SPRING_PROFILES_ACTIVE=test`, `SPRING_DATA_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`, `APP_MAIL_ENABLED=false`, temporary shared-folder roots, and the JDK workaround above. No `APP_SCHEDULING_ENABLED` or `SPRING_APPLICATION_JSON` override was set.
- **Process details:** Hidden Java process PID `16024` exited with code `1` after about four seconds.
- **Logs:** `C:\Users\CHRIST~1\AppData\Local\Temp\cbdev-disable-test-profile-scheduling-20261005\candidate-2a24d6c7.stdout.log` and matching `.stderr.log`.
- **Cleanup:** Confirmed PID `16024` absent and port `58066` free. No direct database writes were performed.

## Data Sent

### 1. Test-profile scheduling regression

```text
Load classpath resource application-test.yml with YamlPropertySourceLoader.
Install its property source in SchedulingConfiguration's ApplicationContextRunner.
Expected: no ScheduledAnnotationBeanPostProcessor bean.
Baseline: profile omitted app.scheduling.enabled, so the scheduler bean was present.
```

### 2. Full native checks and package

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar
```

### 3. Committed candidate startup on isolated test DB

```text
Profile: test
MongoDB URI: mongodb://127.0.0.1:27018/test
Port: 58066
No scheduling-property override
Start committed boot JAR and wait for readiness.
```

### 4. Runtime cleanup and database isolation

```text
Read-only command before and after: mongosh mongodb://127.0.0.1:27018/test --quiet --eval db.getName()
Process check: PID 16024
Listener check: TCP port 58066
```

## Response Received

### 1. Test-profile scheduling regression

```text
Baseline: testProfileDisablesScheduledWork failed because scheduling remained enabled.
Candidate focused configuration suite: 5 passed, 0 failed.
The loaded application-test.yml property source disabled ScheduledAnnotationBeanPostProcessor registration.
```

### 2. Full native checks and package

```text
BUILD SUCCESSFUL in 4m 23s
:website:check: passed
:cbell-lib:check: passed
:website:bootJar: passed
Java test results: 2,042 tests, 110 skipped, 0 failures, 0 errors
Browser suite: 382 passed, 0 failed
PowerShell suites included by the full check: passed
```

### 3. Committed candidate startup on isolated test DB

```text
Application active profile: test
Mongo client target: 127.0.0.1:27018
ApplicationContext initialization failed:
Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1.
Readiness was not reached.
```

### 4. Runtime cleanup and database isolation

```text
Process PID 16024: absent after exit
Port 58066: free
mongosh db.getName(): test before and after
No direct database writes were made.
```

## Evidence
- Baseline: `695a3ed8617f9b4ab07abb7413baf369c58acf6`; focused configuration regression failed because the test profile had no shared scheduler switch.
- Candidate: `2a24d6c7232e2771a86f85395a69f2709f1af1ff`; candidate worktree is clean.
- Full gate and packaged startup were run from `A:\Projects\christopherbell.dev-worktrees\disable-test-profile-scheduling-20261005`.
- The test-profile test loads the resource itself; runtime had no scheduling-property override.
- The candidate startup log identifies migration `015-require-domain-collection-schema`; database inspection was read-only.
- The audit excludes draft PR #1477; no PR was created.

## Bugs / Follow-ups
AC-3 remains blocked until supported isolated test-database recovery or provisioning allows the committed application to reach readiness. Do not modify migration state directly or bypass the startup guard. No PR was created.

## Document Status
blocked

## Project
christopherbell-dev
