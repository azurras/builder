# Cane's Failure Diagnostics Runtime Verification

## Document Status

complete

## Story/Issue

Task 47 in the `christopherbell.dev` site bug audit: preserve useful exception diagnostics for failed official Cane's price requests.

## Branch

Candidate branch `codex/canes-null-failure-diagnostics-20260928`, commit `34d39a174c440b28b2ae1b3824b73a5879db4abb`. PR [#1447](https://github.com/azurras/christopherbell.dev/pull/1447) merged at `2026-09-28T16:22:15Z` as `a9b01063fc7ac086ee8ae43c2c4ff9344a7ec4d4`.

## App / Environment

Spring Boot 4.1, Java 25. Candidate: packaged `website/build/libs/website.jar`, `test` profile, base URL `http://127.0.0.1:18081`, MongoDB URI `mongodb://127.0.0.1:27019/test`, collector scheduling and mail disabled. The candidate used a fresh copy of the previously verified restored disposable fixture. Production validation used the local listener at `http://127.0.0.1:8080` and the apex and `www` HTTPS hosts. No production database or collection operation was used by the candidate.

## Local Run Details

Built with `./gradlew.bat :website:bootJar --no-daemon --console=plain --max-workers=1`. A first candidate attempt against an empty disposable database exited after migration 015 rejected the missing domain-collection schema. The retry used a fresh copy of fixture directory `C:\Users\Christopher\AppData\Local\Temp\codex-mongodb-only-restored-20260924T193158Z` at `C:\Users\Christopher\AppData\Local\Temp\codex-canes-diagnostics-mongodb-fixture-copy-20260928`. Disposable MongoDB PID 10648 listened only on `127.0.0.1:27019`; candidate PID 27072 listened on port 18081. The candidate was started with `java.exe -jar website/build/libs/website.jar --server.port=18081`. The candidate was stopped and the disposable database shut down; ports 18081 and 27019 were confirmed closed. Production listener/database remained on ports 8080 and 27017. Candidate logs are in the linked worktree under `build/verification/canes-diagnostics-candidate-fixture.stdout.log`, `canes-diagnostics-candidate-fixture.stderr.log`, and `canes-diagnostics-mongod.log`.

## Test Cases

1. Assert null and blank exception messages use the exception type, while a nonblank message is preserved.
2. Start the packaged candidate against an isolated `test` database and GET readiness and homepage.
3. After merge, GET readiness, homepage, Cane's page, Cane's history API, and WFL freshness on the local listener and both public hostnames.
4. Read the current public Cane's snapshot and WFL freshness without triggering collection or import.

## Data Sent

Candidate unauthenticated GETs:

- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`

Production unauthenticated GETs, repeated against each base URL `http://127.0.0.1:8080`, `https://christopherbell.dev`, and `https://www.christopherbell.dev`:

- `/actuator/health/readiness`
- `/`
- `/canes-box-tracker`
- `/api/canes-box-tracker/2026-06-04/history`
- `/api/whatsforlunch/restaurant/2026-07-26/freshness`

No request triggered collection, import, price application, or other production write.

## Response Received

- Running-app response body: readiness contains status `UP`; homepage contains `<title>CB | Home</title>`.
- Candidate readiness: HTTP 200, body status `UP`.
- Candidate homepage: HTTP 200, 3,981 response bytes, title `CB | Home` present.
- All 15 production GETs: HTTP 200. The local/home/page/API/freshness responses were respectively 51/3,981/6,576/390,913/6,601 bytes locally; apex was 51/4,348/6,943/390,913/6,601; `www` was 51/4,348/6,943/390,913/6,601.
- Public WFL freshness: HTTP 200, `source=OpenStreetMap`, `lastRefreshedOn=2026-09-28T15:37:50.362Z`, `current=true`.
- Public Cane's history: HTTP 200; latest snapshot remains week `2026-09-28`, collected `2026-09-28T13:32:01.532Z`, 0/50 successful, 50 excluded. Stored sample failure text remains `Official Cane's GraphQL API failed: null; null; public menu fallback is disabled.` because deployment does not rewrite an existing snapshot.
- `prod.cmd auto-status` after deployment: `UP_TO_DATE`, service `RUNNING`, health `HEALTHY`, active/successful SHA `a9b01063fc7ac086ee8ae43c2c4ff9344a7ec4d4`.

## Pass / Fail

- Exception message regression: PASS; focused client suite passed 17/17.
- Full `:website:test`: PASS (`BUILD SUCCESSFUL`).
- Packaged candidate: PASS using the copied restored fixture. The earlier empty-database candidate attempt failed the expected migration preflight and was replaced with the schema-bearing fixture; production was not involved.
- Production route smoke: PASS, all 15 requests returned HTTP 200.
- Deployment: PASS through the supported poller; the active SHA matches the merge commit and the service is healthy.
- New diagnostic observed in a production sample: NOT YET VERIFIED. No collection was triggered, so the stored historical failure text remains unchanged.
- PR CI: PASS on Windows, macOS, and Ubuntu, CodeQL analyses and dependency review; post-merge CI passed.

## Evidence

- Focused `OfficialCanesBoxPriceClientTest`: 17 passed.
- `./gradlew.bat :website:test --no-daemon --console=plain`: `BUILD SUCCESSFUL`.
- `./gradlew.bat :website:bootJar --no-daemon --console=plain --max-workers=1`: `BUILD SUCCESSFUL`.
- Candidate startup output in `build/verification/canes-diagnostics-candidate-fixture.stdout.log` and `.stderr.log`; disposable Mongo output in `build/verification/canes-diagnostics-mongod.log`.
- PR [#1447](https://github.com/azurras/christopherbell.dev/pull/1447), merge SHA `a9b01063fc7ac086ee8ae43c2c4ff9344a7ec4d4`; all required checks and post-merge CI passed.
- `git diff --check` passed before PR creation.
- The unprivileged scheduler-task view reports `UNKNOWN` / `ACCESS_DENIED`; no protected scheduler state or application logs were accessed.

## Bugs / Follow-ups

The new code is active in production, but its failure text has not yet been observed from a new production collection. The observed read-only official gateway request returned HTTP 403 from this host, so the upstream access failure remains unresolved. The public menu fallback stays disabled to avoid stale third-party prices; no data was fabricated or applied. The next scheduled collection is needed to confirm the improved text in a persisted sample.
