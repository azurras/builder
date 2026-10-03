# Task 65 Cane's mobile layout runtime verification

## Document Status

complete

## Story/Issue

Task 65 in [the site bug audit plan](../implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md): prevent page-level horizontal overflow on the Cane's Box Index at mobile width.

## Branch

Repository branch: `codex/canes-box-mobile-overflow`, commit `d2ea1add339645bcf9d044307e090035557a1ab9`; merged PR [#1467](https://github.com/azurras/christopherbell.dev/pull/1467) as `02cc854e0642efd3dbd8bc9091edc01b57b09a88`.

## App / Environment

- Public application: christopherbell.dev, Cane's Box Index route `/canes-box-tracker`.
- Browser candidate: isolated static preview from the repository's `canes-box-tracker.html` template and edited `main.css`, served at `http://127.0.0.1:18891/`.
- The preview removed module scripts and inserted the Bootstrap-compatible global `box-sizing: border-box` reset because it was not running the Spring Boot WebJar server. A 720px SVG fixture was inserted into the chart to exercise its internal scrolling.
- No application database or external integrations were used by the preview.
- Production baseline captured earlier on 2026-10-03: at a 360px document viewport, the live page's document scroll width was 387px.
- Deployed production application: `https://www.christopherbell.dev/canes-box-tracker`, active release SHA `02cc854e0642efd3dbd8bc9091edc01b57b09a88`.

## Local Run Details

- Preview source: checked-out Thymeleaf template and candidate stylesheet from the Task 65 worktree.
- Start command: `python -m http.server 18891 --directory <temporary preview directory>`.
- Browser viewport overrides: 375x812 (document viewport 360px) and 1280x900 (document viewport 1265px, accounting for the browser scrollbar).
- Cleanup: temporary preview server was stopped; browser viewport reset; preview tab closed. The supported production auto-deployer built and validated the merged release, then reached fresh `UP_TO_DATE`; the application service remained healthy.

## Test Cases

1. **Mobile card layout and page width** — render the tracker template and candidate CSS at outer viewport 375x812, then inspect grid tracks, card boxes, and document width.
2. **Chart overflow isolation** — render a 720px SVG in the chart panel and inspect the panel's client width, scroll width, and overflow mode.
3. **Desktop compatibility** — inspect card columns and document width at outer viewport 1280x900.
4. **Source regression** — run the focused markup test before the CSS change (expected failure) and after (pass), then run all browser-side JavaScript tests directly with Node.
5. **Gradle-native test task** — attempt `:website:jsTest` with the Gradle wrapper.
6. **Production smoke** — request the public route and inspect the deployed page at mobile and desktop widths, including browser console errors.

## Data Sent

The isolated preview received a read-only `GET /` at `http://127.0.0.1:18891/`. After deployment, the public route received a read-only `GET /canes-box-tracker` at `https://www.christopherbell.dev/canes-box-tracker`. No form input, mutation request, database operation, or external integration call occurred.

## Response Received

- Mobile (outer viewport 375x812): `window.innerWidth=375`, `documentElement.clientWidth=360`, `documentElement.scrollWidth=360`; index grid has one `262px` column and both cards share that column. Chart panel has `clientWidth=272`, `scrollWidth=720`, and `overflow-x:auto`.
- Desktop (outer viewport 1280x900): document width and client width are both 1265px; index grid has two 489px columns; both cards remain side by side.
- Regression test: 14/14 tests passed after the CSS change. Before the change the new assertion failed because the existing 720px media rule omitted `.canes-box-index-grid`.
- Full browser-side suite: 374/374 tests passed with `node --test website/src/test/js/*.test.js`.
- Gradle `:website:jsTest`: did not reach task execution. Gradle 9.6.1 failed while establishing its Windows loopback connection (`java.io.IOException: Unable to establish loopback connection`; Java NIO reported `SocketException: Invalid argument: connect`). Retries with `--no-daemon`, empty `org.gradle.jvmargs`, and `-Djava.net.preferIPv4Stack=true` failed the same way.
- Required CI: Java 25 builds on Ubuntu, macOS, and Windows; CodeQL Actions, Java/Kotlin and JavaScript analyses; and Dependency Review all passed.
- Production GET `/canes-box-tracker`: HTTP 200, 6,943 response bytes, title `Raising Canes Box Index`, tracker grid markup present.
- The running production app returned HTTP/1.1 200 OK for `/canes-box-tracker`; the page UI rendered the tracker title, hero, and index cards.
- Production mobile (outer viewport 375x812): document viewport and scroll width both 360px, one 278px grid column, both cards within x=41..319, no page-level horizontal overflow. The stylesheet URL was the deployed release asset under `/0db8dcd2b6cfeed37877/css/main.css`.
- Production desktop (outer viewport 1280x900): document viewport and scroll width both 1265px, two 489px columns, cards side by side.
- Production chart panel retained `overflow-x:auto`; it had no wide SVG at the time of the production check. A 720px SVG fixture in the isolated browser preview confirmed internal scrolling (`clientWidth=272`, `scrollWidth=720`).
- Production browser console error/warning check returned no entries. Site and service health were healthy after deployment.
- `git diff --check` passed.

## Pass / Fail

- Mobile and desktop CSS behavior in the isolated browser preview: **PASS**.
- Regression and full Node browser-side test suites: **PASS**.
- Gradle-native `:website:jsTest`: **BLOCKED** before task execution by the local Java loopback failure.
- Required CI build, CodeQL, and dependency checks: **PASS**.
- Supported automatic Spring Boot candidate validation and production deployment: **PASS**; final status was fresh `UP_TO_DATE` with active, attempted, successful, and remote SHAs matching.
- Public route and deployed mobile/desktop behavior: **PASS**.

## Evidence

- Production baseline and CSS root-cause measurements are recorded in Task 65 of the linked plan.
- Focused red/green command: `node --test website/src/test/js/a11y-markup.test.js` (14 tests; failed 1 before the fix, passed 14 after).
- Full suite command: `node --test website/src/test/js/*.test.js` (374 passed, 0 failed).
- Gradle command: `./gradlew.bat :website:jsTest --no-daemon --console=plain`; failed before task startup as described above.
- CI checks passed for PR #1467 before merge.
- Deployer command: `prod.cmd auto-status`; final values were `FRESH`, `UP_TO_DATE`, service/site `RUNNING`/`HEALTHY`, and remote/active/attempted/successful SHA `02cc854e0642efd3dbd8bc9091edc01b57b09a88`.
- Production response and DOM measurements were collected after deployment. Mobile screenshot was visually checked; no image artifact was retained.
- Patch adds `.canes-box-index-grid` to the existing 720px media selector group, setting a shrinkable `minmax(0, 1fr)` column.
- Preview and production measurements were read from rendered browser DOMs.

## Bugs / Follow-ups

- Local Gradle remains unable to establish its Windows loopback connection; required CI provides the build/test evidence for this release.
- `auto-status` continues to report poller state as `UNKNOWN/ACCESS_DENIED` to this standard user, although the sanitized deployment state is fresh and up to date. This is an existing observability limitation, not a deployment failure.
