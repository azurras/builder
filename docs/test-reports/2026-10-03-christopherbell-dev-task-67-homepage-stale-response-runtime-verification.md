# christopherbell.dev Task 67 Homepage Signal Rail Runtime Verification

## Document Status

draft

## Story/Issue

Builder implementation plan Task 67: prevent older homepage active-post feed responses from overwriting newer results.

## Branch

Branch `codex/home-active-post-stale-response-20261003`, based on merged `origin/main` `bde35ffae5d23e7754bd49ee00fc940f19123c2`. Candidate source commit: `bde35ffae5d23e7754bd49ee00fc940f19123c2`, with local Task 67 changes. Candidate JAR SHA-256: `5B2152476655CD9A0CDFD6FCFCD6B45C4DE710C1D53CE90A23F59453D168D318`.

## App / Environment

Windows 11; Java 25.0.3; Spring Boot 4.1.1; MongoDB 8.3.2. Candidate profile `test,deploy-smoke`; app URL `http://127.0.0.1:18093`; isolated MongoDB URL `mongodb://127.0.0.1:27030/test`. MongoDB bound only to loopback and used the previously verified synthetic `TARGET_ACTIVE` fixture under `build/runtime-smoke-photos-usage-20261003/mongodb-valid`; it contains no production data. Scheduled jobs and mail were disabled.

## Local Run Details

- Red regression command: `node --test website/src/test/js/home-active-post-refresh.test.js`. A controlled first fetch remained pending while the five-second interval started a second fetch. Resolving the newer result first and the first request last failed at the expected assertion because `result older` replaced `result newer`.
- Green focused commands: `node --test website/src/test/js/home-active-post-refresh.test.js website/src/test/js/home-active-post.test.js`; `node --check` on both changed JavaScript files; `git diff --check`. Six focused tests passed; the regression includes stale success and stale failure completions.
- Full check command: set process-local `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp` and private `GRADLE_USER_HOME=C:\Users\Christopher\AppData\Local\Temp\gradle-cbell-home-active-post-20261003`, then ran `./gradlew.bat :website:jsTest --no-daemon --console=plain` and `./gradlew.bat :website:check --no-daemon --console=plain`. Both succeeded. The native check took 12m37s.
- Candidate MongoDB PID 32368 listened on `127.0.0.1:27030`; fixture verification returned database `test`, state `TARGET_ACTIVE`, 50 sources, 52 kind metrics, and manifest digest `576fa007a848780ff8f1e21e4a492f3758ad92ed72d829a75819bdfaf41a9b24`.
- Candidate app PID 36668 listened on `127.0.0.1:18093`, profile `test,deploy-smoke`, with `--spring.mongodb.uri=mongodb://127.0.0.1:27030/test`, scheduling disabled, and mail disabled. Process connection inspection confirmed MongoDB connections only to port 27030; its host-metrics probe also connected to local production HTTP port 8080. Production MongoDB port 27017 was not a candidate connection.
- Candidate processes were stopped after verification. Ports 18093 and 27030 closed; production listeners 8080 and 27017 remained. MongoDB log confirms clean shutdown with exit code 0. The app log's Mongo connection reset was caused by that intentional shutdown.
- An initial readiness polling script did not recognize PowerShell's byte-array response body; the corrected body decoding confirmed status code 200 and `{"status":"UP"}`. No application startup failure occurred.

## Test Cases

1. Reproduce stale content with two deferred feed requests in the browser-side module.
2. Verify a stale success and a stale failure cannot overwrite the newest signal-rail result.
3. Run full JavaScript and native project checks.
4. Run the packaged candidate against the isolated test database; verify readiness, home page, and the fingerprinted `home.js` asset in HTTP and Chrome accessibility output.
5. Confirm candidate cleanup and preserve production service/database listeners.

## Data Sent

- The deterministic Node harness issued mocked `GET /api/posts/2025-09-14/feed?limit=20` fetches with controlled response order; it made no network request or production write.
- A read-only `mongosh` query against `mongodb://127.0.0.1:27030/test` verified the synthetic cutover ledger before startup.
- GET `http://127.0.0.1:18093/actuator/health/readiness` and `GET http://127.0.0.1:18093/` with no authentication.
- GET the fingerprinted candidate JavaScript URL `/f4b9c94c387688cbe513/js/home.js`.
- The application database URI pointed only to `mongodb://127.0.0.1:27030/test`.

## Response Received

- Baseline regression failed as expected: after request 2 returned `result newer`, request 1 later rendered `result older`; the active rail contained the stale post.
- After the sequence guard, focused tests passed 6/6. When an older request completed after the latest success, the newer content remained. When an older request failed after the latest success, the newer content remained and the error markup did not appear.
- `:website:jsTest` passed 375/375. `:website:check` succeeded: Java tests 1,975, 0 failures, 0 errors, 108 skipped; PowerShell deployment checks 203 passed, 0 failed, 1 skipped under each of PowerShell 7 and Windows PowerShell 5.1; shared-folder worker checks 75 passed, 0 failed.
- Candidate readiness returned status code 200 with `{"status":"UP"}`. Candidate homepage returned status code 200 with title `CB | Home`, one page h1, and the `homeActivePost` mount. The fingerprinted `home.js` returned status code 200 and contained the refresh sequence guard.
- Chrome accessibility tree showed the expected intentional empty-feed state, `No active posts yet.`; the isolated API had no post fixture.
- Candidate shutdown left no listeners on ports 18093 or 27030. Production service on 8080 and MongoDB on 27017 remained listening.

## Pass / Fail

- PASS: The new regression failed on the baseline for the stale-success assertion.
- PASS: Stale success and stale failure completions are ignored after a newer refresh starts.
- PASS: Focused JavaScript checks, syntax checks, `git diff --check`, full `:website:jsTest`, and `:website:check` succeeded.
- PASS: The packaged candidate started against only the isolated `test` database; readiness, homepage, and fingerprinted asset returned HTTP 200.
- PASS: Chrome exposed the expected home page and empty-feed state; this state matched the isolated empty feed response.
- PASS: Candidate resources were stopped and production listeners remained intact.
- PENDING: Required PR CI, merge, supported production deployment, and post-deployment homepage acceptance.

## Evidence

- Implementation and regression: `website/src/main/resources/static/js/home.js`, `website/src/test/js/home-active-post-refresh.test.js`.
- Candidate app logs and identity: `build/runtime-smoke-home-active-post-20261003/website.stdout.log`, `website.stderr.log`, `website.pid`, and `mongod.log`.
- Full test results: `website/build/test-results/test/` and `website/build/test-results/jsTest/results.xml`.
- Candidate database fixture verification: `build/runtime-smoke-photos-usage-20261003/verify-cutover-ledger.js`.

## Bugs / Follow-ups

The request-order defect is fixed in the candidate. Required PR CI, supported deployment, and public post-deployment verification remain pending. The public production feed was empty during inspection; this is an expected data state, not a second defect.
