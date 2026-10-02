## Document Status

draft

## Story/Issue

Task 54 of the ongoing christopherbell.dev site bug audit: show an error when ZIP coordinate API/curl copy controls cannot access the clipboard.

## Branch

Site worktree: `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20261001`, branch `codex/zip-coordinate-clipboard-failure-20261002`, based on deployed `origin/main` SHA `eefd5da9e0bc6036c927e565314798314bc26145`. Candidate JAR SHA-256: `C598FDA0EBC48793F325F3B996BBF4330B42C88BF052DDE0087ED98B438F96F9`.

## App / Environment

Spring Boot 4.1, Java 25.0.3. Candidate URL `http://127.0.0.1:18081`, profiles `test,deploy-smoke`. MongoDB 8.3.2 listened only on `127.0.0.1:27019`; the app URI explicitly selected database `test` using the existing isolated test-only database copy under `website/build/verification/vin-decoder-mongodb`. Scheduling and mail were disabled. No production database connection was configured.

## Local Run Details

Built by the full `:website:check` gate using the process-only JDK socket path override `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp`. Started MongoDB with `--dbpath website/build/verification/vin-decoder-mongodb --bind_ip 127.0.0.1 --port 27019`; started `website/build/libs/website.jar` with `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, and `SERVER_PORT=18081`. Candidate app PID 35728 and MongoDB PID 36044 were stopped after verification. Ports 18081 and 27019 were closed afterward; production listeners 8080 and 27017 remained present. MongoDB output was written to the isolated worktree's ignored `website/build/verification/zip-coordinate-clipboard-mongod.log`; application startup and request output was captured in the foreground command session.

## Test Cases

1. Before the fix, reject `navigator.clipboard.writeText` during a ZIP API copy click and check whether the page alert reports the failure.
2. After the fix, run all browser-side JavaScript tests and check the touched module syntax.
3. Start the packaged candidate on alternate app and database ports; check readiness, homepage, ZIP coordinate page, and script.
4. Confirm the supported deployer still reports the previously deployed healthy revision before publishing this change.

## Data Sent

The candidate received unauthenticated requests: `GET /actuator/health/readiness`, `GET /`, `GET /zip-coordinates`, and `GET /js/zip-coordinates.js`. The browser-side harness clicked the ZIP API copy control with a simulated rejected clipboard permission. No ZIP lookup/API request was made, and no production data was read or changed.

## Response Received

- Before the fix, the new regression failed because `Permission denied` escaped `copyElementText`; 346 existing JS tests passed.
- After the fix, `:website:jsTest` passed 347/347 with no unhandled rejection; the existing alert received `Unable to copy text. Please copy it manually.`.
- `node --check website/src/main/resources/static/js/zip-coordinates.js` and `git diff --check` passed.
- `:website:check` passed all 21 tasks in 5m05s; both Windows PowerShell suites passed.
- Candidate readiness status 200 with response body `{"status":"UP"}`. Homepage, `/zip-coordinates`, and `/js/zip-coordinates.js` each returned HTTP status 200; the page contained its ZIP form and the served script contained the clipboard error handler.
- Before Task 54 deployment, production `prod.cmd auto-status` reported `FRESH`, `UP_TO_DATE`, `RUNNING`, and `HEALTHY`, with remote/active/attempted/successful SHA `eefd5da9e0bc6036c927e565314798314bc26145`.

## Pass / Fail

Candidate and local checks passed. Review, required CI, merge, supported deployment, and production acceptance remain pending; this report is a draft.

## Evidence

The permission-denied regression was observed failing before implementation and passing after. The full native check completed successfully; the JDK socket-path override was process-only. The packaged candidate started on port 18081 with the test-only profile and its explicit isolated Mongo target on 27019. After shutdown, port checks found only the production listeners on 8080 and 27017. Production status was read-only.

## Bugs / Follow-ups

`copyElementText` awaited clipboard access without catching rejection. Denied or unavailable clipboard access left the ZIP page without feedback and emitted an unhandled rejection. The fix reports clipboard errors through the existing ZIP coordinate alert and preserves the successful copy confirmation. Complete diff review, required CI, supported deployment, and production page/asset acceptance before marking this report complete.
