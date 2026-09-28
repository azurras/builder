## Document Status

complete

## Story/Issue

Task 50: verify response-only cleanup of legacy Cane's history failure messages containing literal `null` placeholders.

## Branch

`codex/canes-legacy-failure-text-20260928`, based on `0d159a118b760c5afee693005a4c6caf2a6ea623`. Candidate artifact: `website/build/libs/website.jar` built by the passing `:website:check` run.

## App / Environment

Spring Boot candidate, profile `test,deploy-smoke`, HTTP port `18081`, base URL `http://127.0.0.1:18081`. MongoDB URI `mongodb://127.0.0.1:27019/test`; this is a disposable local copy of a prior test database, not production. WFL and Cane's external collectors were disabled by the test profile, application scheduling was disabled, and mail was disabled. Production remained on HTTP `8080` and MongoDB `27017`.

## Local Run Details

Started the packaged JAR in a foreground verification session with `SERVER_PORT=18081`, `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `APP_SCHEDULING_ENABLED=false`, mail disabled, and a disposable runtime JWT secret. Candidate app PID was `13140`; candidate MongoDB PID was `10948`. App log: `website/build/verification/canes-legacy-projection-app.log`; Mongo log: `website/build/verification/canes-legacy-projection-mongod.log`. The candidate became ready and was stopped after the checks. The app listener on `18081` and Mongo listener on `27019` were confirmed closed; production listeners on `8080` (PID `14892`) and `27017` (PID `4512`) remained present. The disposable database copy and its inserted fixture were preserved.

## Test Cases

1. Exercise the weekly history API with a legacy failed snapshot as the latest record.
2. Confirm a response-only placeholder replacement while failure counts and unavailable pricing remain accurate.
3. Read the fixture back from the isolated database after the API request to confirm the stored text was not rewritten.

## Data Sent

`GET http://127.0.0.1:18081/api/canes-box-tracker/2026-06-04/history`; no request body or special headers. Before the request, inserted a candidate-only `2026-09-28` fixture cloned from an existing test snapshot, with 50 failed/excluded metro rows, no prices, and stored diagnostic text `Official Canes GraphQL API failed: null; null; public menu fallback is disabled.` No production data or external source was touched.

## Response Received

Readiness returned status code 200 with `{"status":"UP"}`. The history request returned status code 200, `success=true`, latest week `2026-09-28`, 50 metro entries, `successfulMetroCount=0`, `verifiedMetroCount=0`, `excludedMetroCount=50`, and `averagePrice=null`. The public failure reason was `Official Canes GraphQL API failed: details unavailable; details unavailable; public menu fallback is disabled.` The post-request database read still returned the original stored `... null; null; ...` reason and the same 50-row count state.

After deployment, local readiness on port `8080` returned `UP`. The public `GET https://www.christopherbell.dev/api/canes-box-tracker/2026-06-04/history` returned status code `200`, latest week `2026-09-28`, 50 metro entries, 0 successful, 0 verified, 50 excluded, `averagePrice=null`, and the same sanitized diagnostic. This request was read-only.

The supported SYSTEM poller reported `FRESH` / `SUCCEEDED`, `siteHealth=HEALTHY`, `serviceState=RUNNING`, and matching remote, attempted, successful, and active SHA `ccad01fb711f4299e3b59c423dc17966a29be499`. Its tool refresh reported `SUCCEEDED`. The prior active SHA was `0d159a118b760c5afee693005a4c6caf2a6ea623`. The unprivileged scheduler-registration projection remains `UNKNOWN` / `ACCESS_DENIED`; the successful poller run confirms execution for this release. No rollback was needed.

## Pass / Fail

- Production deployment and acceptance: PASS - active revision matches the merged SHA, readiness is UP, and the public history route returned the sanitized response.
- Readiness: PASS - status code 200 and status `UP`.
- Legacy history projection: PASS - status code 200, placeholder text sanitized in the response, zero-success/zero-verified state and null average retained.
- Persistence isolation: PASS - stored failure text remained unchanged after the GET.
- Candidate cleanup: PASS - candidate ports closed while both production listeners remained present. MongoDB's orderly shutdown closed its client connection (`ECONNRESET`); the subsequent listener check confirmed shutdown.

## Evidence

The full `:website:check` passed before runtime startup (21 Gradle tasks; Java, JavaScript and Pester checks green). `git diff --check` passed. Candidate startup and dispatcher logs are in the app log listed above. Runtime execution was approximately `2026-09-28 14:34` CDT. The API response and database readback values are recorded above.

PR #1450 required CI passed (Windows, macOS, Ubuntu, CodeQL and dependency review) and squash-merged as `ccad01fb711f4299e3b59c423dc17966a29be499`. The supported automatic deployer completed successfully; deployment status, deployed SHA, readiness and public route evidence are recorded above.

## Bugs / Follow-ups

The code regression test and full suite cover the implementation. No production fixture or manual storage update was made; legacy text is normalized in the public history projection. The unprivileged scheduled-poller registration query remains unavailable as `ACCESS_DENIED`, although this successful deployment confirms the poller executed.
