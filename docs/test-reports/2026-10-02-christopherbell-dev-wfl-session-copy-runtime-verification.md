# WFL Shared Session Copy Runtime Verification

## Document Status

complete

## Story/Issue

Task 55 in the christopherbell.dev site bug audit. Verify accessible feedback for shared-session link clipboard success, rejection, and unavailable Clipboard API.

## Branch

`codex/wfl-session-copy-feedback-20261002`, based on `b5ad92eb4ea8c3beb635643ca8c928bd1a25a1ae`, with the Task 55 working-tree changes packaged into the candidate. Candidate JAR SHA-256: `3291AEE70B97A99A8FB8C3FA2A6B4C3D455CAC17F0B8485A60A02B922E6B4146`.

## App / Environment

- App: christopherbell.dev Spring Boot candidate.
- Profiles: `test,deploy-smoke`; test profile disables Cane's and WFL scheduled imports, and deploy-smoke disables application scheduling.
- Candidate URL: `http://127.0.0.1:18081`.
- Database: `mongodb://127.0.0.1:27019/test`, verified by mongosh as database `test` with ping result `1`.
- MongoDB used a separate 245,095,083-byte copy of the existing disposable test fixture. It did not connect to production MongoDB on port 27017.
- The candidate used a temporary LEGACY release descriptor in its own runtime directory to avoid a production schema cutover. JWT configuration was a test-only placeholder; its value is not recorded.

## Local Run Details

Packaged with `.\\gradlew.bat :website:check --no-daemon --console=plain --max-workers=1` using process-local `JAVA_TOOL_OPTIONS=-Djava.io.tmpdir=C:\\t -Djdk.net.unixdomain.tmpdir=C:\\t`, `TEMP=C:\\t`, `TMP=C:\\t`, and a worktree-local Gradle cache. The check passed all 21 tasks in 3m55s. `:website:jsTest` passed 350/350; the focused copy regression passed 3/3; `node --check` and `git diff --check` passed.

The packaged JAR ran as Java PID 34456 from a hidden process. Isolated MongoDB 8.3 ran as PID 8412. Both processes were stopped after verification. Ports 18081 and 27019 closed; production listeners on 8080 and 27017 remained. The test database copy and logs remain under the ignored worktree path `website/build/verification/`; no process uses them.

## Test Cases

1. Readiness endpoint reports the candidate and isolated database are ready.
2. Public home and WFL routes load from the packaged candidate.
3. The served WFL JavaScript contains the live status region and failure feedback for clipboard rejection or an unavailable API.
4. Browser-side event-handler regressions exercise successful copy, rejected write, and unavailable API behavior.

## Data Sent

- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/wfl`
- `GET http://127.0.0.1:18081/js/whats-for-lunch.js?verification=task55b`
- Clipboard regression inputs: share link `https://www.christopherbell.dev/wfl?session=session-123`; clipboard outcomes were successful write, `Permission denied`, and missing `navigator.clipboard`.

## Response Received

- Readiness JSON status: `UP`.
- Home: HTTP status code 200.
- WFL page: HTTP status code 200.
- WFL script: HTTP status code 200, 41,171 bytes; contains `lunch-session-status`, `Unable to copy link. Select and copy it manually.`, and the unavailable-API check.
- Candidate PID 34456 and MongoDB PID 8412 exited after explicit stop; the two candidate ports were closed.

## Pass / Fail

All four runtime cases passed. The focused regression passed 3/3, the full JavaScript suite passed 350/350, and `:website:check` passed all 21 tasks. `node --check` and `git diff --check` passed.

## Evidence

Commands and outputs were observed in the isolated worktree on 2026-10-02. Candidate runtime logs are under the ignored `website/build/verification/` directory. Production ports 8080 and 27017 remained listening after candidate shutdown.

## Bugs / Follow-ups

The prior handler allowed a rejected clipboard write to escape and falsely reported success when Clipboard API was absent. The regression now verifies visible live feedback, no unhandled rejection, no false success, and unchanged success behavior. PR 1455 passed required CI, merged, and deployed successfully; production acceptance is complete.


## Production Acceptance

- PR 1455 passed Windows, macOS, Ubuntu, CodeQL Java/Kotlin, JavaScript/TypeScript, Actions analysis, and dependency review. It merged at 2026-10-02 17:55:27 UTC as bd1ede060d6135562230f14baf08d37df3457dcd.
- The supported production status command reported fresh UP_TO_DATE, RUNNING, and HEALTHY. Remote, active, attempted, and successful SHAs all matched bd1ede060d6135562230f14baf08d37df3457dcd; failure category was NONE.
- GET https://www.christopherbell.dev/actuator/health/readiness returned HTTP status 200 with JSON body status UP.
- GET https://www.christopherbell.dev/wfl returned HTTP status 200.
- GET https://www.christopherbell.dev/js/whats-for-lunch.js?verification=bd1ede0 returned HTTP status 200; the 41,195-byte asset contains the live status region, actionable failure text, and unavailable-API check.
- The read-only scheduled-poller field remains UNKNOWN / ACCESS_DENIED. No protected state or ACL was changed.
