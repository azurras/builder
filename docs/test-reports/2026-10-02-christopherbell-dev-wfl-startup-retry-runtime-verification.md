## Document Status

complete

## Story/Issue

Task 51 in the christopherbell.dev site bug audit: prevent restart-based same-day repeats of an overdue failed WFL import.

## Branch

`codex/site-bug-audit-20261001`, based on `origin/main` SHA `ccad01fb711f4299e3b59c423dc17966a29be499`. Candidate JAR SHA-256: `587e5e747f60fd11f365699d9cc6d413633942c375349346c2d735be456d8da5`. Source changes were uncommitted at runtime.

## App / Environment

Spring Boot 4.1, Java 25.0.3. Candidate base URL `http://127.0.0.1:18081`, profiles `test,deploy-smoke`. Candidate MongoDB was a byte-for-byte and SHA-256 verified copy of the restored test fixture at `C:\Users\Christopher\AppData\Local\Temp\codex-mongodb-only-restored-20260924T193158Z`, served by disposable MongoDB 8.3 bound only to `127.0.0.1:27019`; the application URI explicitly targeted `mongodb://127.0.0.1:27019/test`. `mongosh` confirmed database `test`, standalone server (`setName=null`), and successful ping. WFL and Cane's collectors, application scheduling, and mail were disabled. Production remained on ports 8080 and 27017.

## Local Run Details

Built `website/build/libs/website.jar` with the repository Gradle wrapper task `:website:bootJar`; the copied candidate artifact SHA matched the WSL build artifact. Started Java PID 10268 with `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, `SERVER_PORT=18081`, and `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp`; command-line properties also set the isolated Mongo URI, port, and disabled scheduled import. The application process output was captured in the verification terminal. MongoDB PID 544 wrote `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20261001\website\build\verification\wfl-startup-repeat-mongod.log`. The candidate app was stopped with Ctrl+C. MongoDB was stopped only after verifying its executable and command line referenced this candidate database path. Ports 18081 and 27019 were closed afterward; production listeners 8080 and 27017 remained present.

## Test Cases

1. Check candidate readiness with the MongoDB dependency available.
2. Load the homepage.
3. Read public WFL data freshness from the versioned API route.
4. Confirm candidate cleanup and production listener preservation.

## Data Sent

Unauthenticated GET requests only:

- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/api/whatsforlunch/restaurant/2026-07-26/freshness`

An initial probe used the wrong, unversioned freshness path and returned 403; the documented API-version path above returned 200. No state-changing request was sent.

## Response Received

- Readiness: status code: 200; response body: `{"status":"UP"}`.
- Homepage: status code: 200; UI result: title `CB | Home`.
- WFL freshness: status code: 200; response body identified source `OpenStreetMap`, `lastRefreshedOn=2026-08-02T22:44:50.963Z`, `current=false`. This old timestamp is expected in the restored test fixture and does not represent production freshness.
- Mongo log records Java-driver clients connecting to `127.0.0.1:27019`.
- After candidate shutdown, candidate ports were absent and the existing production listeners remained present.

## Pass / Fail

- Focused `RestaurantImportWorkflowServiceTest`: 17 tests passed after the fix. The same-day restart regression failed before the fix; the next-Central-day eligibility regression passed after it.
- `:website:check`: passed on rerun, including JavaScript, Java, Windows production checks, and static verification. One initial full-suite attempt hit a `ConcurrentModificationException` in Spring `MockHttpServletResponse` in the unrelated async streaming integration test; that test passed in isolation and the subsequent complete gate passed.
- Candidate readiness, homepage, freshness read, and cleanup: passed.

## Evidence

- `git diff --check` passed.
- Focused test and full `:website:check` ran from `/home/cbell/site-bug-audit-20261001` under WSL Debian, using the isolated worktree's Git metadata. Full gate output ended with `BUILD SUCCESSFUL in 1m 25s`.
- Candidate JAR checksum was verified equal at its WSL build path and isolated Windows worktree path before startup.
- All 360 files in the isolated database copy matched source file lengths and SHA-256 values.
- Candidate Mongo log: `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20261001\website\build\verification\wfl-startup-repeat-mongod.log`.

## Bugs / Follow-ups

The confirmed bug is covered by service-level regressions: startup catch-up now suppresses an overdue retry when the latest unresolved failure is already on the current Central calendar date, while a later local date remains eligible. Candidate startup runs with `deploy-smoke`, so it intentionally does not invoke the import workflow. The candidate used read-only HTTP requests; no production data or listeners were changed. Production deployment acceptance remains to be recorded after required PR CI and supported deployment.
