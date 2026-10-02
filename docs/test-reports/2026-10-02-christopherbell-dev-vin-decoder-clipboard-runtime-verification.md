## Document Status

draft

## Story/Issue

Task 53 of the ongoing christopherbell.dev site bug audit: surface clipboard failures from the VIN decoder's JSON and curl copy controls.

## Branch

Site worktree: `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20261001`, branch `codex/vin-decoder-clipboard-failure-20261002`, based on merged `origin/main` SHA `de1e2addc35c2d9ec232fcdb068bc992ce675357`. Candidate JAR SHA-256: `9C1F1B029E6971AEF8C4A215E2722F8229FB6850AE5A9647A7C11B814457900D`.

## App / Environment

Spring Boot 4.1, Java 25.0.3. Candidate URL `http://127.0.0.1:18081`, profiles `test,deploy-smoke`. MongoDB 8.3.2 was bound to `127.0.0.1:27019` and the app URI explicitly selected database `test`; it used the existing isolated test-only database copy at `website/build/verification/vin-decoder-mongodb`. No production database connection was configured. Scheduling and mail were disabled.

## Local Run Details

Built with the process-only setting `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp` and `.\gradlew.bat :website:check --no-daemon --console=plain --max-workers=1`, which also built the candidate JAR. Started the isolated MongoDB using `mongod.exe --dbpath website/build/verification/vin-decoder-mongodb --bind_ip 127.0.0.1 --port 27019`; started the JAR with `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, and `SERVER_PORT=18081`. Candidate app PID 10300 and MongoDB PID 35168 were stopped after verification. Ports 18081 and 27019 were closed afterward; production listeners 8080 and 27017 remained present.

## Test Cases

1. Before the fix, simulate rejection from `navigator.clipboard.writeText` and verify the copy control reports an actionable page error.
2. After the fix, run all browser-side JavaScript tests and check the touched script's syntax.
3. Start the packaged candidate on the alternate app and database ports; check readiness, homepage, VIN page, and VIN script.
4. Read production deployer status and public routes to confirm the previous merged VIN validation release remains healthy while this change is pending.

## Data Sent

The candidate received only unauthenticated GET requests to `/actuator/health/readiness`, `/`, `/vin-decoder`, and `/js/vin-decoder.js`. The JavaScript regression simulated a rejected clipboard permission for the JSON copy button. No VIN was submitted, no API calls were made, and no production data was read or changed.

## Response Received

- Before the fix, `:website:jsTest` showed the new regression failing with `Permission denied` escaping from `copyText`; 345 existing tests passed.
- After the fix, `:website:jsTest` passed 346/346 with no unhandled rejection; the existing alert received `Unable to copy text. Please copy it manually.`.
- `node --check website/src/main/resources/static/js/vin-decoder.js` and `git diff --check` passed.
- `:website:check` passed all 21 tasks in 5m13s. Both Windows PowerShell suites passed; the JS suite passed 346/346.
- Candidate readiness status 200 with response body `{"status":"UP"}`. Homepage, VIN page, and VIN script each returned HTTP status 200; the served script included the clipboard error handler.
- Before this new change, production `prod.cmd auto-status` reported `FRESH`, `UP_TO_DATE`, `RUNNING`, and `HEALTHY`, with remote/active/attempted/successful SHA `de1e2addc35c2d9ec232fcdb068bc992ce675357`. The production VIN page and script returned 200 with Task 52's input pattern and local format guard.

## Pass / Fail

Candidate and local checks passed. Review, required CI, merge, supported deployment, and deployed clipboard-failure behavior remain pending; this report is a draft.

## Evidence

The permission-denied regression failed before implementation and passed after. The full native check completed successfully; the JDK socket-path override was process-only. Candidate output showed the app started on 18081 with the test-only profile and its explicit Mongo target on 27019. After shutdown, port checks found only the production listeners on 8080 and 27017. Production status and HTTP checks were read-only.

## Bugs / Follow-ups

The VIN copy helper awaited `navigator.clipboard.writeText` without handling rejection. When browser permission was denied or the clipboard API was unavailable, the event handler produced an unhandled rejection and gave no page feedback. The fix catches clipboard failures and reports them in the existing alert region while preserving the success confirmation. Complete diff review, required CI, supported deployment, and post-deployment acceptance before marking this report complete.
