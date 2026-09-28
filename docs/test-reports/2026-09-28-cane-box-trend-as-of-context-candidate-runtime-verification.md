## Document Status

complete

## Story/Issue

Task 48 in `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`: make each Cane's price index identify the latest priced week used for the trend.

## Branch

Site worktree branch `codex/canes-trend-asof-context-20260928`; candidate source was the working tree on base commit `a9b01063fc7ac086ee8ae43c2c4ff9344a7ec4d4`. The packaged JAR was built after the caption change and documentation update.

## App / Environment

- App: christopherbell.dev Spring Boot candidate, Java 25.0.3, test fixture.
- Candidate URL: `http://127.0.0.1:18081/canes-box-tracker`.
- Active profiles: `test,deploy-smoke`.
- Effective database: isolated copy of the restored fixture, database `test`, URI `mongodb://127.0.0.1:27019/test`; no connection to production MongoDB `127.0.0.1:27017`.
- Candidate MongoDB used the MongoDB 8.3 server binary on loopback port 27019 with a copied 360-file, 244,733,546-byte data directory. The source fixture was left intact.
- Scheduled effects disabled by `deploy-smoke` and the test profile; WFL monthly import and Cane's collector disabled; mail disabled. Candidate JWT secret was a disposable local-only value. No credentials were sent.
- Production service and Mongo listeners remained on ports 8080 and 27017; those processes and data were not used or changed by the candidate.

## Local Run Details

- Artifact: `website/build/libs/website.jar` from the site worktree.
- Start command: `java.exe -jar A:\Projects\christopherbell.dev-worktrees\auto-status-legacy-schema-20260925\website\build\libs\website.jar`, with process-local environment `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `SERVER_PORT=18081`, `APP_MAIL_ENABLED=false`, blank `APP_MAIL_FROM`/`RESEND_API_KEY`, and a disposable candidate `APP_JWT_SECRET`.
- Candidate app process 6440 was stopped with Ctrl+C after the browser check. Candidate Mongo process 33384 was terminated after verifying its executable, candidate-only data path, and port 27019; the process no longer runs.
- Listener check after cleanup: candidate ports 18081 and 27019 closed; production listeners 8080 and 27017 still present.
- The isolated candidate-only 244,733,546-byte Mongo data copy remains under `%TEMP%\codex-canes-index-asof-candidate-20260928\mongo-data`. Its removal was rejected by the execution policy, so it was preserved. It is not running or connected to production.

## Test Cases

1. Packaged candidate readiness and page/API availability.
2. Candidate tracker browser rendering for the existing month-over-month value and the two dates that define it.
3. Full native repository check and focused JavaScript suite.

## Data Sent

- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/canes-box-tracker`
- `GET http://127.0.0.1:18081/api/canes-box-tracker/2026-06-04/history` (requested automatically by the page as well).
- Browser action: opened the candidate page; no form input, mutation, collector trigger, or authenticated request.

## Response Received

- Running-app response: status 200, readiness body `{"status":"UP"}`.
- Running-app response: status 200 for the home page, title `CB | Home`.
- Running-app response: status 200 for the tracker page, title `Raising Canes Box Index`.
- Running-app response: status 200 for the history API, 357,572 response bytes from the cloned `test` database.
- Browser UI result: month-over-month `+0.2%`; caption `Latest priced week: 2026-09-21. Compared with week of 2026-08-24.`; latest average `$12.54`; 50/50 verified metros.

## Pass / Fail

- `:website:jsTest`: PASS, 344 tests, 0 failed.
- `:website:check --no-daemon --console=plain --max-workers=1`: PASS, 21 Gradle tasks; Java, JavaScript, and Windows Pester suites completed successfully. Operations Pester: 203 passed, 0 failed, 1 existing skip. Shared-folder-worker Pester: 75 passed, 0 failed.
- Candidate readiness, home, tracker, history API: PASS (all status 200; readiness `UP`).
- Browser as-of display regression: PASS; rendered text names latest-priced date 2026-09-21 and comparison date 2026-08-24 beside the unchanged +0.2% trend.
- Candidate process and port cleanup: PASS; candidate ports closed and 8080/27017 remained listening.

## Evidence

- Full check command: `./gradlew :website:check --no-daemon --console=plain --max-workers=1`; result `BUILD SUCCESSFUL in 10m 10s`.
- Focused command: `./gradlew :website:jsTest --no-daemon --console=plain --max-workers=1`; result 344 passed, 0 failed.
- Candidate artifact identity: packaged `website/build/libs/website.jar` from branch `codex/canes-trend-asof-context-20260928`, based on `a9b01063fc7ac086ee8ae43c2c4ff9344a7ec4d4` plus the uncommitted Task 48 source diff.
- Candidate browser inspection used Codex's in-app browser at `127.0.0.1:18081`; visible DOM values are recorded above. No screenshot was captured.
- Post-stop listener check showed only the existing site listener on 8080 and MongoDB service listener on 27017; candidate listeners were absent.

## Bugs / Follow-ups

- Candidate verification is complete. Production deployment and production browser/runtime proof are pending the reviewed site PR merge and supported deployer. No production data or collector was changed or triggered.
- Existing `testResults.xml` in the site worktree was unrelated and preserved.
