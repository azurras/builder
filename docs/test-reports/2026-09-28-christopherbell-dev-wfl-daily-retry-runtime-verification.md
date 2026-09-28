## Document Status

complete

## Story/Issue

Task 45 in the christopherbell.dev site bug audit: daily retry for overdue failed WFL imports, including legacy month-only completion state.

## Branch

`codex/wfl-daily-import-retry-20260925`, based on `origin/main` SHA `375f527910d2beae8db6ff36dc1236656a31ff9e`, for the isolated candidate. Production deployment verified merged PR #1445 at `e45010373cfcf123815febc5869845bc968616b0` and readiness-timeout PR #1446 at `29e86bb4c959d989d81ee13e9da24a9177d313f3`.

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
5. After supported deployment, GET the 11 local smoke routes and the same 11 routes on both public hostnames; read public WFL freshness and non-elevated deployment status.

## Data Sent

Unauthenticated GET requests only:

- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/api/whatsforlunch/restaurant/2026-07-26/freshness`
- Production read-only smoke requests: all 11 paths from `ProductionSmokePaths` on `http://127.0.0.1:8080`, `https://christopherbell.dev`, and `https://www.christopherbell.dev`.
- `GET https://christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/freshness`

No manual import preview was applied and no import-write request was sent. Collector scheduling was disabled for this candidate.

## Response Received

- Readiness: status 200 (HTTP 200), body status `UP`.
- Homepage: HTTP 200, title `CB | Home`.
- WFL freshness: HTTP 200, source `OpenStreetMap`, `current=false`, `lastRefreshedOn=2026-08-02T22:44:50Z` in the restored test database.
- Candidate listener PID matched 9872 and was confirmed closed after stop. Disposable Mongo listener PID matched 14512 and was confirmed closed. Production listener remained on port 8080/PID 13988.
- After PR #1445 deployment, `prod.cmd auto-status` reported `SUCCEEDED`, active/successful SHA `e45010373cfcf123815febc5869845bc968616b0`, service `RUNNING`, and site health `HEALTHY`. Its overdue WFL freshness endpoint initially still showed the August 2 marker.
- After PR #1446 deployment, auto-status reported `UP_TO_DATE`, active/successful SHA `29e86bb4c959d989d81ee13e9da24a9177d313f3`, service `RUNNING`, and site health `HEALTHY`. All 33 local/public smoke requests returned HTTP 200.
- The production WFL freshness endpoint returned HTTP 200 with `source=OpenStreetMap`, `lastRefreshedOn=2026-09-28T15:37:50.362Z`, and `current=true`.

## Pass / Fail

- Focused `RestaurantImportWorkflowServiceTest`: 15 tests passed, zero failures, zero errors, zero skipped. The due-date regression for legacy month-only state failed before the fallback correction and passed afterward.
- Full `:website:check`: BUILD SUCCESSFUL in 5m22s. Browser JavaScript tests: 343/343. Production PowerShell suite: 203 passed, 0 failed, 1 skipped. Shared-folder worker PowerShell suite: 75 passed, 0 failed. Java test task completed successfully; Mongo contract tests remained skipped by their normal project configuration.
- Candidate readiness, homepage, freshness reads, and cleanup passed.
- Supported production acceptance passed after both merges: the poller first deployed PR #1445 following a safe rollback/retry, then deployed PR #1446 with the longer readiness window. The second activation remained unready temporarily but recovered within the new bounded window; the poller then reported `UP_TO_DATE` on the new SHA.
- All 33 post-deployment smoke requests passed, and public WFL freshness is current.

## Evidence

- Gradle output from the 2026-09-28 focused test and full check runs.
- Candidate logs: `A:\Projects\christopherbell.dev-worktrees\auto-status-legacy-schema-20260925\build\verification\candidate.stdout.log` and `candidate.stderr.log` for the first startup; the final foreground candidate startup output was captured in the local execution session.
- Production baseline at 2026-09-28 09:28 CDT: `prod.cmd auto-status` reported `UP_TO_DATE`, service `RUNNING`, site health `HEALTHY`, active/successful SHA `375f527910d2beae8db6ff36dc1236656a31ff9e`, and `pollerReason=ACCESS_DENIED`. Direct production reads showed readiness `UP` and public WFL freshness still false at the Aug 2 marker. This is the pre-deployment baseline only.
- `git diff --check` passed.
- Required PR #1445 checks passed on all three operating systems and CodeQL/dependency review; post-merge CI passed on Windows, macOS, and Ubuntu. PR #1446 required checks and post-merge CI passed, including CodeQL, dependency review, analysis, and Windows/macOS/Ubuntu builds.
- On the unprivileged host, scheduler-task registration remains `UNKNOWN` with reason `ACCESS_DENIED`; no protected task state or logs were accessed. The successful supported deployment and current public freshness are independently verified.

## Bugs / Follow-ups

The retry is merged and deployed. The candidate-only test intentionally used a restored isolated database, so its stale marker is expected; production subsequently reports current WFL data. The implementation permits at most one retry per local date through the existing lease, but a second-day production retry after a new transient failure has not been observed. Protected scheduler-task state and logs remain inaccessible without elevated access; no manual import was applied.
