## Document Status

complete

## Story/Issue

Site bug audit Task 40: reject production MongoDB connection strings without a database name. Also records the post-merge production state for Task 41 recovery; candidate runtime evidence does not prove production acceptance.

## Branch

Candidate branch `codex/mongodb-uri-database-required`, source commit `bbef48a8e428a64f5efafbee198c00dda3ea8d80`. PR [#1439](https://github.com/azurras/christopherbell.dev/pull/1439) merged at 2026-09-24 23:29:33 UTC as `fb10948cc4d0b3b2d5f739789b8a810713456301`.

## App / Environment

Spring Boot website, Java 25.0.3, `test` profile. Candidate listener: `127.0.0.1:18081`. MongoDB target: `mongodb://127.0.0.1:27019/test`, served by a disposable `mongod.exe` bound only to loopback. The isolated data directory was cloned to `%LOCALAPPDATA%\Temp\codex-mongodb-uri-validator-20260924` from the existing restored fixture. The fixture copy matched 347 files and 35,268,322 bytes; the source backup archive SHA-256 was `E94D6664691190AFF6680969977908A9638F7250C0587424CDFC41B4F26DB477`. Production MongoDB remained at PID 5388 on port 27017; the candidate did not connect to it.

The production environment was separately observed after merge using non-elevated `prod.cmd auto-status` and a public readiness GET. It remained stopped and unhealthy; details are below.

## Local Run Details

From `A:\Projects\christopherbell.dev-worktrees\mongodb-uri-database-required-20260924`, set `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=A:\t`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, and `SERVER_PORT=18081`, then ran `.\gradlew.bat :website:bootRun --no-daemon --max-workers=1 --console=plain`.

Candidate PID 2388 started successfully and logged a connection to `127.0.0.1:27019`. It was stopped with Ctrl+C after the HTTP checks. The disposable MongoDB PID 24256 was stopped with `db.adminCommand({shutdown: 1})`. Subsequent process and listener checks confirmed both candidate ports 18081 and 27019 were closed; production MongoDB PID 5388 remained running. The cloned fixture directory remains on disk; no recursive cleanup was attempted.

## Test Cases

1. Start the candidate with a named database in `SPRING_MONGODB_URI`; verify startup and Mongo connection against the isolated `test` database.
2. Request application readiness and homepage on the alternate port.
3. Observe production service, deployment status, and public readiness after merge without modifying protected files or bypassing ACLs.

## Data Sent

Unauthenticated `GET http://127.0.0.1:18081/actuator/health/readiness` and `GET http://127.0.0.1:18081/`. The app used only the isolated test database URI. No production database, production listener, external collector, or authenticated endpoint was targeted.

The source regression tests cover missing and empty URI database paths and acceptance of a named database. The full `:website:check` passed locally in 5m07s; hosted PR checks passed on Windows, macOS, and Ubuntu plus CodeQL and dependency review before merge.

## Response Received

- Candidate readiness response: HTTP status 200; body `{"status":"UP"}`.
- Candidate homepage response: HTTP status 200; 3,981 bytes, title `CB | Home`.
- Candidate startup log: Spring Boot reported startup complete and MongoDB driver connected to `127.0.0.1:27019`.
- Production `prod.cmd auto-status` at 2026-09-24 23:30:53 UTC: `status=SERVICE_UNHEALTHY`, `serviceState=STOPPED`, `siteHealth=UNHEALTHY`, `deploymentStatus=DEPLOYMENT_FAILED`, `remoteSha=fb10948cc4d0b3b2d5f739789b8a810713456301`, `activeSha=4b552a63a08c9333bdaa0d7827b23eb811920f37`, `attemptedSha=failedSha=fb10948cc4d0b3b2d5f739789b8a810713456301`, `toolRefreshStatus=SUCCEEDED`, and `failureCategory=DEPLOYMENT`. The sanitized poller query remained `UNKNOWN/ACCESS_DENIED`.
- Public production readiness response: HTTP status 502 Bad Gateway.

## Pass / Fail

- Candidate startup and Mongo isolation: PASS.
- Candidate readiness and homepage: PASS.
- Production recovery and acceptance: FAIL / INCOMPLETE. The service remains stopped and the public readiness route returns 502. The guarded elevated recovery script was not executed; the task runner rejected elevation before a Windows prompt appeared. No protected production configuration, marker, service, ACL, or database state was changed by this runtime session.

## Evidence

- Focused initializer tests and `:website:check` output recorded in the active execution session; `:website:check` completed successfully before publication.
- Candidate Gradle session 90936; candidate PID 2388; disposable MongoDB PID 24256; log path `%LOCALAPPDATA%\Temp\codex-mongodb-uri-validator-20260924\mongod-27019.log`.
- HTTP probes to candidate port 18081; follow-up listener checks confirmed 18081 and 27019 closed.
- Read-only production observations: `prod.cmd auto-status`, `Get-Service ChristopherBellDev`, and `curl.exe -i https://www.christopherbell.dev/actuator/health/readiness`.
- Hosted PR checks were green before merge. Merge-triggered CI run `36072990717` was still in progress when this report was written.

## Bugs / Follow-ups

- The production outage is not resolved. The protected `SPRING_MONGODB_URI` still needs the existing database name `christopherbell`, and the guarded release marker needs reconciliation only after its preconditions pass. Run the prepared guarded recovery through an authorized elevated Windows prompt, then verify local/public readiness, service state, active SHA, and normal recovery policy.
- Do not treat this isolated candidate runtime as production verification. Re-record actual production acceptance after guarded recovery.
