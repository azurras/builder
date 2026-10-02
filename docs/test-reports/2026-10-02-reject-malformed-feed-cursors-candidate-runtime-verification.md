## Document Status

complete

## Story/Issue

Task 60 of the christopherbell.dev site bug audit: reject malformed feed pagination cursors and keep the failed page retryable.

## Branch

Site worktree: `A:\Projects\christopherbell.dev-worktrees\feed-cursor-shape-validation-20261002`, branch `codex/feed-cursor-shape-validation-20261002`, final source/test commits through `dd7a489de4ebfe1bfc773d05133724224543763e`, based on `origin/main` `da393be28b89228d9cb20bd553118442dd61dcad`. Candidate JAR SHA-256: `E8648C822B5E5FEC5222C8B024F5E3421FCB7A2DF81F05C41B85E514C2937404`; the only later source-control change was a test-only regression.

## App / Environment

Spring Boot 4.1.1, Java 25.0.3, MongoDB 8.3, application candidate at `http://127.0.0.1:18084`. Profiles `test,deploy-smoke`; `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, and `SPRING_MONGODB_URI=mongodb://127.0.0.1:27021/test`. Candidate MongoDB was bound only to loopback port 27021 and used a separate copy of the previously verified disposable test fixture. Production remained on application port 8080 and MongoDB port 27017.

## Local Run Details

Full check command: `$env:JAVA_TOOL_OPTIONS='-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp'; $env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\feed-cursor-shape-validation-20261002\website\build\verification\gradle-home'; .\gradlew.bat :website:check --no-daemon --console=plain --max-workers=1`. It completed successfully in 5m04s after the additional scroll-retry regression was added. The packaged candidate was run with `java -jar website/build/libs/website.jar --spring.mongodb.uri=mongodb://127.0.0.1:27021/test --server.port=18084 --app.scheduling.enabled=false --app.mail.enabled=false` and the environment above. Java PID 70760 logged Java 25.0.3, Boot 4.1.1, and a Mongo driver connection to `127.0.0.1:27021`. MongoDB PID 33552 wrote `website/build/verification/task60-mongod.log`. A small Node HTTP harness on `127.0.0.1:18083` served an HTML test page and the actual worktree `infinite.js` module to the browser. The candidate app and Node harness were interrupted after verification; MongoDB was shut down through its local admin command. Ports 18084, 27021 and 18083 were closed; production ports 8080 and 27017 remained listening.

## Test Cases

1. Observe regressions for empty-string and non-string `nextCursor` values, requiring error reporting and retry.
2. Load one valid page, receive a malformed cursor on the next scroll request, and retry from the previous valid `cursor` and `before` values.
3. Run the focused infinite scroller suite, all browser-side JavaScript tests, syntax check, and full native `:website:check`.
4. Start the packaged candidate against isolated MongoDB, check readiness and representative routes/assets, and exercise malformed-cursor failure and retry in a browser.

## Data Sent

Candidate HTTP GET requests: `/actuator/health/readiness`, `/`, `/void`, and `/js/lib/infinite.js`. The browser harness passed `{items: [], nextCursor: {value: 'malformed'}}` to the real shared helper, then its Retry button handler returned `{items: [{createdOn: 'recovered'}], nextCursor: null}`. No account credentials or production data were sent; no production MongoDB URI was configured.

## Response Received

- The two new initial-load regressions failed before implementation because the empty string was treated as completion and the object cursor was accepted; they passed after validation.
- The final focused scroller suite passed 10/10. `node --check` and `git diff --check` passed.
- `:website:jsTest` passed 372/372.
- `:website:check` passed all 21 tasks. Java XML totals: 1,975 tests, 0 failures, 0 errors, 108 skipped. Windows operations tests: 203 passed, 0 failed, 1 skipped; shared-folder worker tests: 75 passed, 0 failed, 0 skipped.
- Candidate readiness returned status 200 with body `{"status":"UP"}`. `/`, `/void`, and `/js/lib/infinite.js` each returned status 200; the served helper included the cursor-validation message.
- Browser accessibility state showed `Feed failed and can be retried`, alert text `Feed page cursor must be a non-empty string or null.`, and a visible `Retry feed` button after one request. After retry, it showed `Feed loaded`, the `recovered` item, and `2 requests`.
- Candidate shutdown closed its three ports, while production listeners on 8080 and 27017 remained.

## Pass / Fail

All candidate checks passed. The final source commits passed the full check, and the actual browser run demonstrated malformed-cursor feedback and recovery. Required PR CI, supported production deployment, and production acceptance were still pending when this candidate report was recorded.

## Evidence

The cursor contract is `String nextCursor`, nullable for completion. Validation runs before updating `seenCursors` or pagination state. The added scroll-retry regression confirms the same last valid cursor and `before` value are sent again after a malformed response. Candidate Java logs and the MongoDB log confirm that the packaged app connected only to the isolated candidate MongoDB port. Browser accessibility output captured both the failure and the recovered state.

## Bugs / Follow-ups

An empty-string cursor was silently coerced to completion, and a non-string cursor could corrupt cursor identity and pagination progress. The shared helper now reports both through its existing retryable error callback before changing cursor state. Production was not touched in this report; finish required CI, supported deployment, and production acceptance separately.
