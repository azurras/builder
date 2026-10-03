# Void Signed-Out Feed Error Runtime Verification

## Document Status
complete

## Story/Issue
Builder implementation plan Task 63: keep public Void feed errors visible to signed-out visitors.

## Branch
PR #1465 branch `codex/void-alert-visible-to-signed-out` at `43575ed5156fa8b73565798ef8167ed682a95a9d`, based on `origin/main` `dd87087f4d9c6f43cb6730408a315cd640820e69`; squash-merged at `9730446890122f72ab640a58abd9b958b706b433`.

## App / Environment
- App: `christopherbell.dev` Spring Boot web application, Java 25.0.3.
- Profiles: `test,deploy-smoke`; scheduled work and email disabled.
- Candidate URL: `http://127.0.0.1:18089/void`.
- Candidate MongoDB: isolated standalone process on `127.0.0.1:27028`, database `test`, data directory under the isolated worktree. It contains synthetic candidate migration/cutover fixtures and candidate startup state. Startup logs confirm the application connected to `127.0.0.1:27028`; no production database was accessed.
- Production deployment completed through the supported automatic deployer after the PR merge.

## Local Run Details
- Build: `$env:TEMP='C:\t'; $env:TMP='C:\t'; .\gradlew.bat --no-daemon :website:check` (exit 0).
- Candidate command: `java -Djdk.net.unixdomain.tmpdir=C:/Windows/Temp -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27028/test --app.scheduling.enabled=false --app.mail.enabled=false --server.address=127.0.0.1 --server.port=18089`.
- Candidate processes: website PID 14600; isolated MongoDB PID 21920. Both processes were stopped after verification. Ports 18089 and 27028 were confirmed closed afterward.
- Production baseline before merge: fresh `UP_TO_DATE` at `dd87087f4d9c6f43cb6730408a315cd640820e69`; service and site health were healthy.
- Logs and captured browser output: isolated worktree `build/runtime-smoke-feed-error-20261003/`.

## Test Cases
1. Confirm the packaged candidate starts against its isolated MongoDB `test` database.
2. Request readiness, liveness, and the signed-out Void page.
3. In Chrome, inject a 503 for the first public feed GET, inspect the signed-out UI, scroll to retry, allow the retry, and verify the alert clears.
4. Run the focused regression before and after the template fix, then run JavaScript and full website checks.

## Data Sent
- `GET http://127.0.0.1:18089/actuator/health/readiness`.
- `GET http://127.0.0.1:18089/actuator/health/liveness`.
- `GET http://127.0.0.1:18089/void`, with no authentication cookie.
- Browser feed request `GET /api/posts/2026-07-26/feed?size=20`; the first browser response was synthesized as HTTP 503. A later scroll caused the same GET to pass through to the isolated candidate API.

## Response Received
- Readiness: HTTP/1.1 200 OK, body `{"status":"UP"}`.
- Liveness: HTTP/1.1 200 OK, body `{"status":"UP"}`.
- `/void`: HTTP/1.1 200 OK.
- Browser initial state: composer had `d-none`; `#homeAlert` was visible with `Request failed: 503`; feed skeleton count was 0.
- First feed GET: HTTP/1.1 503; retry feed GET: HTTP/1.1 200. After retry, `#homeAlert` had `d-none` and empty text.
- After deployment, local readiness and liveness returned HTTP/1.1 200 OK. Local `http://127.0.0.1:8080/void` and public `https://www.christopherbell.dev/void` each returned HTTP/1.1 200 OK. Chrome confirmed in both pages that `#homeAlert` exists outside `#composer`, the signed-out composer has `d-none`, and the alert begins hidden.
- Before the template edit, the new regression failed because `#homeAlert` was nested under `#composer`. After the edit, it passed.

## Pass / Fail
- PASS: signed-out feed errors are visible while the composer remains hidden.
- PASS: first-load failure clears skeletons, and recovery clears the alert.
- PASS: `:website:jsTest` passed, 373 tests, 0 failures.
- PASS: `:website:check` passed, including 1,975 Java tests (0 failures, 0 errors, 108 skipped) and native Windows checks.
- PASS: PR #1465 Dependency Review, CodeQL, and Java 25 Linux/macOS/Windows CI all passed.
- PASS: Candidate cleanup completed; production listeners and services remained healthy.
- PASS: the fresh deployer record reached `SUCCEEDED` with remote, active, attempted, and successful SHA all equal to `9730446890122f72ab640a58abd9b958b706b433`; failure category `NONE`, tool refresh `SUCCEEDED`, website service `RUNNING`, and site health `HEALTHY`.
- PASS: production JavaScript/template behavior verified through both local and public signed-out browser loads.
- NOTE: `pollerState=UNKNOWN` / `pollerReason=ACCESS_DENIED` remains the existing non-elevated Task Scheduler query limitation; deployment status itself was fresh and successful.

## Evidence
- `website/build/test-results/test/` and `website/build/test-results/jsTest/results.xml` in the isolated worktree.
- Browser scripts/results: `browser-check.mjs`, `browser-result.txt`, `production-check.mjs`, and `production-result.txt` under `build/runtime-smoke-feed-error-20261003/` in the isolated worktree.
- Candidate startup logs: `website.stdout.log` and `mongod.log` in the same runtime directory.
- PR #1465 merged at 2026-10-03 17:51:12 UTC; merge SHA `9730446890122f72ab640a58abd9b958b706b433`.

## Bugs / Follow-ups
None for Task 63. The broader authorized site bug-finding goal remains active.
