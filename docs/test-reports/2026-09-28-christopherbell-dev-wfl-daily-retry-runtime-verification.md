## Document Status

draft

## Story/Issue

Task 45 in the christopherbell.dev site bug audit: daily retry for overdue failed WFL imports, including legacy month-only completion state.

## Branch

`codex/wfl-daily-import-retry-20260925`, based on `origin/main` SHA `375f527910d2beae8db6ff36dc1236656a31ff9e`. The candidate included the uncommitted Task 45 source, tests, and feature README changes.

## App / Environment

Spring Boot 4.1, Java 25, `test` profile. Packaged candidate URL: `http://127.0.0.1:18081`. Database target: `mongodb://127.0.0.1:27019/test`; disposable MongoDB process bound to loopback. The restored archive path was `C:\Users\Christopher\AppData\Local\Temp\codex-mongodb-only-restored-20260924T193158Z`. Candidate environment set `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, and `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp`. Production service and MongoDB were not used as candidate dependencies.

## Local Run Details

The final candidate used `java.exe -jar website/build/libs/website.jar`, PID 9872, on 2026-09-28 at approximately 09:23 CDT. The isolated MongoDB process used PID 14512 on port 27019. Readiness, homepage, and freshness requests completed; candidate and disposable MongoDB were then stopped. Both ports were confirmed closed. The production service remained Running on port 8080, PID 13988; production MongoDB remained Running on port 27017, PID 4512.

Automated verification used `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, and the short JDK socket temp path. Focused test: `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.importing.RestaurantImportWorkflowServiceTest --no-daemon --console=plain`. Native check: `./gradlew.bat :website:check --no-daemon --max-workers=1 --console=plain`.

## Test Cases

1. Verify focused WFL import workflow behavior for retry eligibility, daily suppression, success stop, legacy state, disabled configuration, and lease contention.
2. Run repository-native `:website:check`.
3. Start the packaged candidate on alternate loopback port 18081 against the isolated database named `test`.
4. GET readiness, homepage, and public WFL freshness; stop the candidate and disposable database.

## Data Sent

Unauthenticated GET requests only:

- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/api/whatsforlunch/restaurant/2026-07-26/freshness`

No manual import preview was applied and no import-write request was sent. Collector scheduling was disabled for this candidate.

## Response Received

- Readiness: HTTP 200, body status `UP`.
- Homepage: HTTP 200, title `CB | Home`.
- WFL freshness: HTTP 200, source `OpenStreetMap`, `current=false`, `lastRefreshedOn=2026-08-02T22:44:50Z` in the restored test database.
- Candidate listener PID matched 9872 and was confirmed closed after stop. Disposable Mongo listener PID matched 14512 and was confirmed closed. Production listener remained on port 8080/PID 13988.

## Pass / Fail

- Focused `RestaurantImportWorkflowServiceTest`: 15 tests passed, zero failures, zero errors, zero skipped. The due-date regression for legacy month-only state failed before the fallback correction and passed afterward.
- Full `:website:check`: BUILD SUCCESSFUL in 5m22s. Browser JavaScript tests: 343/343. Production PowerShell suite: 203 passed, 0 failed, 1 skipped. Shared-folder worker PowerShell suite: 75 passed, 0 failed. Java test task completed successfully; Mongo contract tests remained skipped by their normal project configuration.
- Candidate readiness, homepage, freshness reads, and cleanup passed.

## Evidence

- Gradle output from the 2026-09-28 focused test and full check runs.
- Candidate logs: `A:\Projects\christopherbell.dev-worktrees\auto-status-legacy-schema-20260925\build\verification\candidate.stdout.log` and `candidate.stderr.log` for the first startup; the final foreground candidate startup output was captured in the local execution session.
- Production baseline at 2026-09-28 09:28 CDT: `prod.cmd auto-status` reported `UP_TO_DATE`, service `RUNNING`, site health `HEALTHY`, active/successful SHA `375f527910d2beae8db6ff36dc1236656a31ff9e`, and `pollerReason=ACCESS_DENIED`. Direct production reads showed readiness `UP` and public WFL freshness still false at the Aug 2 marker. This is the pre-deployment baseline only.
- `git diff --check` passed.

## Bugs / Follow-ups

The retry code is not yet merged or deployed. Required CI, supported deployment, deployed SHA/readiness verification, and post-deployment WFL freshness readback remain pending. A successful scheduled retry is not proven by this local candidate because scheduling was deliberately disabled and no production import was applied. If the remote/database failure persists, the retry will keep recording failures once per day and the site may remain stale; protected scheduler logs were not read.
