## Document Status

complete

## Story/Issue

Task 60 of the christopherbell.dev site bug audit: reject malformed feed pagination cursors and keep the failed page retryable.

## Branch

Site worktree: `A:\Projects\christopherbell.dev-worktrees\feed-cursor-shape-validation-20261002`, branch `codex/feed-cursor-shape-validation-20261002`, source/test commits through `dd7a489de4ebfe1bfc773d05133724224543763e`, based on `origin/main` `da393be28b89228d9cb20bd553118442dd61dcad`. PR #1461 passed all required CI and merged by squash as `d4b73f8699d5faa12b1d5884a3ff52e37778d91a` on 2026-10-02 at 23:12:54Z. Candidate JAR SHA-256: `E8648C822B5E5FEC5222C8B024F5E3421FCB7A2DF81F05C41B85E514C2937404`; the only later source-control change was a test-only regression.

## App / Environment

Candidate used Spring Boot 4.1.1, Java 25.0.3, MongoDB 8.3, at `http://127.0.0.1:18084`. Profiles `test,deploy-smoke`; `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, and `SPRING_MONGODB_URI=mongodb://127.0.0.1:27021/test`. Candidate MongoDB was bound only to loopback port 27021 and used a separate copy of the previously verified disposable test fixture. Production remained on application port 8080 and MongoDB port 27017.

## Local Run Details

Full check command: `$env:JAVA_TOOL_OPTIONS='-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp'; $env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\feed-cursor-shape-validation-20261002\website\build\verification\gradle-home'; .\gradlew.bat :website:check --no-daemon --console=plain --max-workers=1`. It completed successfully in 5m04s after the additional scroll-retry regression was added. The packaged candidate ran with `java -jar website/build/libs/website.jar --spring.mongodb.uri=mongodb://127.0.0.1:27021/test --server.port=18084 --app.scheduling.enabled=false --app.mail.enabled=false` and the environment above. Java PID 70760 logged Java 25.0.3, Boot 4.1.1, and a Mongo driver connection to `127.0.0.1:27021`. MongoDB PID 33552 wrote `website/build/verification/task60-mongod.log`. A Node harness on `127.0.0.1:18083` served a test page and the actual worktree `infinite.js` module to the browser. Candidate app and harness were stopped; MongoDB was shut down through its local admin command. Candidate ports 18084, 27021 and 18083 were closed; production ports 8080 and 27017 remained listening.

After merge, the SYSTEM automatic deployment path published the merged SHA. `prod.cmd auto-status` reported `FRESH`, `UP_TO_DATE`, `RUNNING`, and `HEALTHY`, with remote, active, and successful SHA all `d4b73f8699d5faa12b1d5884a3ff52e37778d91a`. It reported tool refresh `SUCCEEDED`. No manual service or release changes were made. The status projection could not query Task Scheduler as the standard user (`pollerState=UNKNOWN`, `pollerReason=ACCESS_DENIED`). `prod.cmd verify-startup` also returned access denied when it reached protected `C:\ProgramData\christopherbell.dev\config\deploy.json`; no elevation was used.

## Test Cases

1. Observe regressions for empty-string and non-string `nextCursor` values, requiring error reporting and retry.
2. Load one valid page, receive a malformed cursor on the next scroll request, and retry from the previous valid `cursor` and `before` values.
3. Run the focused infinite scroller suite, all browser-side JavaScript tests, syntax check, and full native `:website:check`.
4. Start the packaged candidate against isolated MongoDB, check readiness and representative routes/assets, and exercise malformed-cursor failure and retry in a browser.
5. After automatic production deployment, check deployer active SHA/health and public `/`, `/void`, and the versioned helper imported by the Void page.

## Data Sent

Candidate HTTP GET requests: `/actuator/health/readiness`, `/`, `/void`, and `/js/lib/infinite.js`. The browser harness passed `{items: [], nextCursor: {value: 'malformed'}}` to the real shared helper, then its Retry handler returned `{items: [{createdOn: 'recovered'}], nextCursor: null}`. Production acceptance used public GET requests to `https://www.christopherbell.dev/`, `/void`, `/02685ad8daaa748bfcfb/js/home-feed.js`, and `/02685ad8daaa748bfcfb/js/lib/infinite.js`. No account credentials or production database URI were sent.

## Response Received

- The two initial-load regressions failed before implementation because the empty string was treated as completion and the object cursor was accepted; they passed after validation. Final focused scroller tests passed 10/10, including scroll retry retaining the prior valid cursor and `before` value.
- `node --check` and `git diff --check` passed; `:website:jsTest` passed 372/372.
- `:website:check` passed all 21 tasks. Java XML totals: 1,975 tests, 0 failures, 0 errors, 108 skipped. Windows operations tests: 203 passed, 0 failed, 1 skipped; shared-folder worker tests: 75 passed, 0 failed, 0 skipped.
- Candidate readiness returned status 200 with body `{"status":"UP"}`. Candidate `/`, `/void`, and `/js/lib/infinite.js` each returned status 200; the helper contained the cursor-validation message.
- Candidate browser accessibility state showed `Feed failed and can be retried`, alert text `Feed page cursor must be a non-empty string or null.`, and the visible `Retry feed` button after one request. After retry, it showed `Feed loaded`, item `recovered`, and `2 requests`.
- Required PR gates all passed: Java 25 builds on Ubuntu, macOS, and Windows; CodeQL analyses; and dependency review. Read-only review found no Critical, Important, or Minor findings.
- Production `auto-status` reported `FRESH`, `UP_TO_DATE`, `RUNNING`, and `HEALTHY`; remote/active/successful SHA matched the merged SHA. The public root returned status 200 (4,348 bytes), `/void` returned status 200 (7,179 bytes), the page referenced versioned `home-feed.js` which imports `./lib/infinite.js`, and the versioned helper returned status 200 (3,456 bytes) with the cursor-validation message.
- `prod.cmd verify-startup` could not read protected `deploy.json` as the standard user. Direct deployer health and public route/asset checks passed; no elevated action was taken.

## Pass / Fail

Candidate checks, required CI, supported automatic deployment, and production public route/asset acceptance passed for merged SHA `d4b73f8699d5faa12b1d5884a3ff52e37778d91a`. The only unavailable check was `prod.cmd verify-startup`, blocked by its standard-user ACL read of protected `deploy.json`; the non-elevated deployer health projection and direct production responses independently confirmed the active release was healthy.

## Evidence

The API contract is `String nextCursor`, nullable for completion. Validation runs before updating `seenCursors` or pagination state. The scroll-retry regression confirms the same previous valid cursor and `before` value are sent again after malformed data. Candidate app logs and MongoDB logs confirm connection only to isolated candidate port 27021. Browser accessibility output captured failure and recovery. Production deployer status and public GET responses confirm the merged SHA and changed versioned helper were active; candidate ports were closed and production listeners remained available.

## Bugs / Follow-ups

An empty-string cursor was silently coerced to completion, and a non-string cursor could corrupt cursor identity and pagination progress. The shared helper now reports both through its existing retryable error callback before changing cursor state. The production startup helper remains inaccessible to the standard user because it reads protected deployment configuration; no ACL change or elevated access was attempted.
