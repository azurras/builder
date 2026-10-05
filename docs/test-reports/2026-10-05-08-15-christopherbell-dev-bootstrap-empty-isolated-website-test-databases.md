# Bootstrap Empty Isolated Website Test Databases: Test Report

## Story/Issue
User request to remove the isolated application runtime blocker and make the supported test-profile workflow repeatable for future agents.

## Branch
codex/chris-street-style-audit-20261005 at dd206c0ef2498e0d400eccce519990e8050bd021

## Pass / Fail

> [!TIP]
> **5 of 5 passed** on candidate dd206c0e.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Focused migration regressions | ✅ PASS | All 19 migration gate, preflight, and V015 tests passed. |
| 2 | Full native repository checks | ✅ PASS | Gradle completed :website:check :cbell-lib:check :website:bootJar; PowerShell suites reported 203 passed/0 failed/1 skipped and 76 passed/0 failed. |
| 3 | Fresh isolated test-profile startup | ✅ PASS | The committed JAR applied migrations 001–015 in database test; domain collections stayed empty and no cutover ledger was created. |
| 4 | Readiness endpoint | ✅ PASS | GET /actuator/health/readiness returned 200 and {"status":"UP"}. |
| 5 | Home page | ✅ PASS | GET / returned 200, 3,981 bytes, and <title>CB | Home</title>. |

## Test Cases
1. **Focused migration regressions:** exercised the exact test profile gate, persisted migration envelopes, migration lease, lifecycle states, and fail-closed cases.
2. **Full native repository checks:** ran the spoke's complete Gradle check and package tasks.
3. **Fresh isolated test-profile startup:** launched the candidate against an owned fresh MongoDB process and read back database and migration state.
4. **Readiness endpoint:** requested the application's readiness health URL.
5. **Home page:** requested the public home route and checked the rendered title.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev |
| OS / runtime | Windows 11, Java 25.0.3, Spring Boot 4.1.1 |
| MongoDB | 8.3, fresh disposable process bound to 127.0.0.1:49354 |
| Profile / database | Exact active profile test; database test |
| Candidate URL | http://127.0.0.1:49355 |
| Environment | SPRING_PROFILES_ACTIVE=test; SPRING_MONGODB_URI=mongodb://127.0.0.1:49354/test; transient random APP_JWT_SECRET (value omitted); generated short jdk.net.unixdomain.tmpdir path |

## Local Run Details
- **Local command:** java -jar website\build\libs\website.jar --server.address=127.0.0.1 --server.port=49355
- **Build command:** .\gradlew.bat :website:bootJar --no-daemon
- **Working directory:** A:\Projects\christopherbell.dev-worktrees\chris-street-style-audit-20261005
- **Candidate identity:** committed HEAD dd206c0ef2498e0d400eccce519990e8050bd021; JAR SHA-256 1EB9BDB48E33B2AD705318D3C146F3520731E2ACF422CA7869A9C4E20B325799.
- **Processes:** candidate Java PID 22520 owned port 49355; disposable mongod PID 3872 owned port 49354. The Mongo URI and listeners were loopback-only.
- **Logs:** C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-de81b8651c314dcfbf423aa8d0c2bbf2\candidate.out.log and candidate.err.log.
- **Cleanup:** stopped the exact candidate and mongod processes; confirmed both ports had zero listeners and both PIDs were gone. Generated database/log and short JDK socket-temp directories remain because automatic command review rejected recursive removal outside the workspace; no alternate deletion method was used. Shell environment variables were cleared.

## Data Sent

### 1. Focused migration regressions

~~~text
$env:JAVA_TOOL_OPTIONS = '-Djdk.net.unixdomain.tmpdir=C:\Temp\cbell-jdk-eed675bdea2c4292b93633aeacf07764'
.\gradlew.bat :website:test --tests 'dev.christopherbell.configuration.mongo.migration.DomainCollectionCutoverLedgerTest' --tests 'dev.christopherbell.configuration.mongo.migration.DomainCollectionStartupPreflightTest' --tests 'dev.christopherbell.configuration.mongo.migration.V015RequireDomainCollectionSchemaTest' --no-daemon
~~~

### 2. Full native repository checks

~~~text
$env:JAVA_TOOL_OPTIONS = '-Djdk.net.unixdomain.tmpdir=C:\Temp\cbell-jdk-eed675bdea2c4292b93633aeacf07764'
.\gradlew.bat :website:check :cbell-lib:check :website:bootJar --no-daemon
~~~

### 3. Fresh isolated test-profile startup

~~~text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:49354/test
APP_JWT_SECRET=<transient random 32-byte secret>
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<generated short directory>
java -jar website\build\libs\website.jar --server.address=127.0.0.1 --server.port=49355
~~~

### 4. Readiness endpoint

~~~http
GET http://127.0.0.1:49355/actuator/health/readiness
~~~

### 5. Home page

~~~http
GET http://127.0.0.1:49355/
~~~

## Response Received

### 1. Focused migration regressions

~~~text
BUILD SUCCESSFUL in 13s
19 migration and startup-gate tests passed.
~~~

### 2. Full native repository checks

~~~text
Pester shared-folder operations: 203 passed, 0 failed, 1 skipped.
Pester shared-folder worker: 76 passed, 0 failed, 0 skipped.
Gradle: BUILD SUCCESSFUL in 4m 11s; 24 actionable tasks.
~~~

### 3. Fresh isolated test-profile startup

~~~text
Application started on 127.0.0.1:49355.
Mongo listener: 127.0.0.1:49354, owned by mongod PID 3872.
Database: test.
application_migrations: 15 records; migrations 001 through 015 all APPLIED.
application_runtime: one released migration lease.
application_leases: 0 records.
All source and target domain collections: 0 documents.
Synthetic TARGET_ACTIVE cutover records: 0.
~~~

### 4. Readiness endpoint

~~~http
HTTP/1.1 200
{"status":"UP"}
~~~

### 5. Home page

~~~http
HTTP/1.1 200
Content-Length: 3981
<title>CB | Home</title>
~~~

## Evidence
- Full check output ended with BUILD SUCCESSFUL in 4m 11s and exit code 0.
- Focused test command ended with BUILD SUCCESSFUL in 13s and exit code 0.
- The application log records profile test, Mongo host 127.0.0.1:49354, and successful startup on port 49355.
- Read-only mongosh inspection returned database test, 15 APPLIED migration records, a single runtime lease record, zero documents in the domain namespaces, and zero cutover ledger rows.
- Process and listener readback after cleanup showed candidate PID 22520 and mongod PID 3872 stopped; ports 49355 and 49354 had zero listeners. Production MongoDB port 27017 remained owned by PID 5236 and was not used.

## Bugs / Follow-ups
- Two failed startup attempts exposed and corrected (a) the Java 25 Windows loopback temp-directory prerequisite and (b) the actual Mongo persistence envelope and migration-lease collection. Final evidence above is from the corrected committed candidate.
- The first PowerShell readiness polling harness treated response content bytes as text and timed out despite a successful app. A direct request verified the 200 response; the app itself did not fail.
- Automatic command review rejected recursive deletion of generated scratch directories outside the workspace. Their processes are stopped and their paths are uniquely generated; the leftover files require manual cleanup.

## Document Status
complete

## Project
christopherbell-dev
