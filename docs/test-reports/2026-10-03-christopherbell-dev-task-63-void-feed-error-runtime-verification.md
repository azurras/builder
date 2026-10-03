# Void Signed-Out Feed Error Runtime Verification

## Document Status
complete

## Story/Issue
Builder implementation plan Task 63: keep public Void feed errors visible to signed-out visitors.

## Branch
`codex/void-alert-visible-to-signed-out` at `43575ed5156fa8b73565798ef8167ed682a95a9d`, based on `origin/main` `dd87087f4d9c6f43cb6730408a315cd640820e69`. PR #1465 is open with all required checks passing.

## App / Environment
- App: `christopherbell.dev` Spring Boot web application, Java 25.0.3.
- Profiles: `test,deploy-smoke`; scheduled work and email disabled.
- Candidate URL: `http://127.0.0.1:18089/void`.
- Candidate MongoDB: isolated standalone process on `127.0.0.1:27028`, database `test`, data directory under the isolated worktree. It contains synthetic candidate migration/cutover fixtures and candidate startup state. Startup logs confirm the application connected to `127.0.0.1:27028`; no production database was accessed.
- Production was not changed during candidate verification.

## Local Run Details
- Build: `$env:TEMP='C:\t'; $env:TMP='C:\t'; .\gradlew.bat --no-daemon :website:check` (exit 0).
- Candidate command: `java -Djdk.net.unixdomain.tmpdir=C:/Windows/Temp -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27028/test --app.scheduling.enabled=false --app.mail.enabled=false --server.address=127.0.0.1 --server.port=18089`.
- Candidate processes: website PID 14600; isolated MongoDB PID 21920. Both processes were stopped after verification. Ports 18089 and 27028 were confirmed closed afterward.
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
- Before the template edit, the new regression failed because `#homeAlert` was nested under `#composer`. After the edit, it passed.

## Pass / Fail
- PASS: signed-out feed errors are visible while the composer remains hidden.
- PASS: first-load failure clears skeletons, and recovery clears the alert.
- PASS: `:website:jsTest` passed, 373 tests, 0 failures.
- PASS: `:website:check` passed, including 1,975 Java tests (0 failures, 0 errors, 108 skipped) and native Windows checks.
- PASS: PR #1465 Dependency Review, CodeQL, and Java 25 Linux/macOS/Windows CI all passed.
- PASS: candidate cleanup completed; production listeners and services were not changed.

## Evidence
- `website/build/test-results/test/` and `website/build/test-results/jsTest/results.xml` in the isolated worktree.
- Browser script and result: `build/runtime-smoke-feed-error-20261003/browser-check.mjs` and `browser-result.txt` in the isolated worktree.
- Candidate startup logs: `website.stdout.log` and `mongod.log` in the same runtime directory.
- PR: https://github.com/azurras/christopherbell.dev/pull/1465

## Bugs / Follow-ups
Candidate verification is complete. PR #1465 has passed CI but has not yet been merged or deployed, so no production behavior claim is made here. Add the merge SHA, supported deployment result, and production health/page verification after delivery.
