# Task 65 Cane's mobile layout runtime verification

## Document Status

draft

## Story/Issue

Task 65 in [the site bug audit plan](../implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md): prevent page-level horizontal overflow on the Cane's Box Index at mobile width.

## Branch

Repository branch: `codex/canes-box-mobile-overflow`; source under verification was based on `origin/main` at `979d7f3b10e89b9749870f679797daf88c0495bd`. The fix and regression assertion were uncommitted during this preview.

## App / Environment

- Public application: christopherbell.dev, Cane's Box Index route `/canes-box-tracker`.
- Browser candidate: isolated static preview from the repository's `canes-box-tracker.html` template and edited `main.css`, served at `http://127.0.0.1:18891/`.
- The preview removed module scripts and inserted the Bootstrap-compatible global `box-sizing: border-box` reset because it was not running the Spring Boot WebJar server. A 720px SVG fixture was inserted into the chart to exercise its internal scrolling.
- No application database or external integrations were used by the preview.
- Production baseline captured earlier on 2026-10-03: at a 360px document viewport, the live page's document scroll width was 387px.

## Local Run Details

- Preview source: checked-out Thymeleaf template and candidate stylesheet from the Task 65 worktree.
- Start command: `python -m http.server 18891 --directory <temporary preview directory>`.
- Browser viewport overrides: 375x812 (document viewport 360px) and 1280x900 (document viewport 1265px, accounting for the browser scrollbar).
- Cleanup: temporary preview server was stopped; browser viewport reset; preview tab closed. No application process was started.

## Test Cases

1. **Mobile card layout and page width** — render the tracker template and candidate CSS at outer viewport 375x812, then inspect grid tracks, card boxes, and document width.
2. **Chart overflow isolation** — render a 720px SVG in the chart panel and inspect the panel's client width, scroll width, and overflow mode.
3. **Desktop compatibility** — inspect card columns and document width at outer viewport 1280x900.
4. **Source regression** — run the focused markup test before the CSS change (expected failure) and after (pass), then run all browser-side JavaScript tests directly with Node.
5. **Gradle-native test task** — attempt `:website:jsTest` with the Gradle wrapper.

## Data Sent

No form input, mutation request, database operation, or external integration call. The local preview made only GET requests to its own static server.

## Response Received

- Mobile (outer viewport 375x812): `window.innerWidth=375`, `documentElement.clientWidth=360`, `documentElement.scrollWidth=360`; index grid has one `262px` column and both cards share that column. Chart panel has `clientWidth=272`, `scrollWidth=720`, and `overflow-x:auto`.
- Desktop (outer viewport 1280x900): document width and client width are both 1265px; index grid has two 489px columns; both cards remain side by side.
- Regression test: 14/14 tests passed after the CSS change. Before the change the new assertion failed because the existing 720px media rule omitted `.canes-box-index-grid`.
- Full browser-side suite: 374/374 tests passed with `node --test website/src/test/js/*.test.js`.
- Gradle `:website:jsTest`: did not reach task execution. Gradle 9.6.1 failed while establishing its Windows loopback connection (`java.io.IOException: Unable to establish loopback connection`; Java NIO reported `SocketException: Invalid argument: connect`). Retries with `--no-daemon`, empty `org.gradle.jvmargs`, and `-Djava.net.preferIPv4Stack=true` failed the same way.
- `git diff --check` passed.

## Pass / Fail

- Mobile and desktop CSS behavior in the isolated browser preview: **PASS**.
- Regression and full Node browser-side test suites: **PASS**.
- Gradle-native `:website:jsTest`: **BLOCKED** before task execution by the local Java loopback failure.
- Full Spring Boot candidate startup and production deployment: **NOT RUN**. The visual preview does not substitute for a Spring Boot candidate; required CI and the supported deployment path remain pending.

## Evidence

- Production baseline and CSS root-cause measurements are recorded in Task 65 of the linked plan.
- Focused red/green command: `node --test website/src/test/js/a11y-markup.test.js` (14 tests; failed 1 before the fix, passed 14 after).
- Full suite command: `node --test website/src/test/js/*.test.js` (374 passed, 0 failed).
- Gradle command: `./gradlew.bat :website:jsTest --no-daemon --console=plain`; failed before task startup as described above.
- Patch adds `.canes-box-index-grid` to the existing 720px media selector group, setting a shrinkable `minmax(0, 1fr)` column.
- Preview measurements were read from the rendered browser DOM. No screenshot artifact was retained.

## Bugs / Follow-ups

- Re-run the Gradle-native task and full `:website:check` in a functioning local Gradle environment or required CI.
- Start and inspect a Spring Boot candidate on an isolated port, then require CI, use the supported auto-deployer, and verify the mobile layout on production before marking this report complete.
