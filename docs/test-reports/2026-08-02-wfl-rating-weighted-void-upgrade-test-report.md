# WFL Rating-Weighted Void Upgrade Test Report

## Document Status

complete

## Story/Issue

[WFL rating-weighted Void upgrade work record](../session-memory/2026-08-02-christopherbell-dev.md#source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md)

## Branch

- Spoke repository: `A:\Projects\christopherbell.dev-worktrees\wfl-rating-weighted-void`
- Branch: `codex/wfl-rating-weighted-void`
- Commit under test: `17583448ed2a4d6f425f766157a357a613037d17`
- Base: `origin/main` at `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`

## App / Environment

- App: `christopherbell.dev` Spring Boot website
- Profile: `local`
- Candidate base URL: `http://127.0.0.1:8081`
- Candidate process: Java PID `60080`
- Production isolation: existing `:8080` listener remained on PID `57904`
- Database: local MongoDB at `mongodb://localhost:27017`; driver connected successfully
- Mail: disabled with `APP_MAIL_ENABLED=false`
- Gradle home: `C:\Users\Christopher\AppData\Local\Codex\gradle\wfl-rating-weighted-void`

## Local Run Details

The candidate was started from the isolated worktree with a hidden PowerShell `Start-Process` invocation of:

```powershell
.\gradlew.bat :website:bootRun --no-daemon
```

The process environment set `GRADLE_USER_HOME` to the private task directory, `SPRING_PROFILES_ACTIVE=local`, `SERVER_PORT=8081`, `SPRING_MONGODB_URI=mongodb://localhost:27017`, `APP_MAIL_ENABLED=false`, a task-only local JWT secret, and `GIT_COMMIT=17583448ed2a4d6f425f766157a357a613037d17`.

Logs were captured at:

- `C:\Users\Christopher\AppData\Local\Temp\codex-wfl-rating-weighted-void\bootrun.out.log`
- `C:\Users\Christopher\AppData\Local\Temp\codex-wfl-rating-weighted-void\bootrun.err.log`

Spring Boot reported `Started Application in 4.935 seconds`. After verification, PID `60080` was stopped, `:8081` no longer listened, and production `:8080` still listened on PID `57904`.

## Test Cases

1. Verify candidate liveness, readiness, and WFL page delivery on the alternate port.
2. Exercise today's persisted public picks.
3. Exercise fresh rating-weighted nearby selection using browser coordinates.
4. Exercise fresh rating-weighted nearby selection using a ZIP code.
5. Use the page UI to submit a ZIP and render three restaurant cards.
6. Verify the desktop Void decision console, equal card geometry, disclosure, and absence of ranking badges.
7. Verify the 390 by 844 mobile breakpoint, single-column cards, and absence of horizontal overflow.
8. Verify the dedicated WFL stylesheet does not load on the neighboring Top Rated page.
9. Verify the browser console has no warnings or errors.
10. Run focused and repository-wide automated verification supporting the runtime checks.

## Data Sent

### HTTP requests

- `GET http://127.0.0.1:8081/actuator/health/liveness`
- `GET http://127.0.0.1:8081/actuator/health/readiness`
- `GET http://127.0.0.1:8081/wfl`
- `GET http://127.0.0.1:8081/api/whatsforlunch/restaurant/2026-05-17/today`
- `GET http://127.0.0.1:8081/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=33.0782&longitude=-96.8089&radiusMiles=20&useSavedPreferences=false`
- `GET http://127.0.0.1:8081/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/75024?radiusMiles=20&useSavedPreferences=false`

### Browser UI input

- Opened `http://127.0.0.1:8081/wfl` in Chrome.
- Entered ZIP code `75024` in the labelled ZIP input.
- Activated the unique `Use ZIP` button.
- Inspected the default 1276 by 1270 viewport and a temporary 390 by 844 viewport.
- Opened `http://127.0.0.1:8081/wfl/top-rated` to confirm stylesheet isolation.

## Response Received

### Health and page responses

- HTTP response status code: 200 for every health and page request below.
- Liveness: HTTP `200`, `application/vnd.spring-boot.actuator.v3+json`, body length 15.
- Readiness: HTTP `200`, `application/vnd.spring-boot.actuator.v3+json`, body length 15.
- `/wfl`: HTTP `200`, `text/html; charset=UTF-8`, body length 3161.

### Restaurant API responses

- Today's picks: HTTP `200`, `success=true`, three restaurant records.
- Coordinate nearby picks: HTTP `200`, `success=true`, three restaurant records: First Chinese BBQ-Richardson, 1418 Coffeehouse, and Sushi Poki.
- ZIP nearby picks: HTTP `200`, `success=true`, three restaurant records: Dunkin' Donuts, Black Agave, and Nuno's Tacos & Vegmex Grill.

### Browser response

- The ZIP submission rendered exactly three unranked cards with real addresses, including `3421 East Renner Road, Plano, TX, 75074`, `7949 Walnut Hill Lane, Dallas, TX, 75230`, and `6959 Lebanon Road, Frisco, TX, 75034`.
- The disclosure rendered visibly: `Ratings influence the draw. Every eligible restaurant stays in the mix.`
- Desktop card rectangles were all 373 pixels wide and 336 pixels high at distinct equal-grid positions.
- Desktop and mobile horizontal overflow were both zero pixels.
- The mobile viewport placed all three cards at the same 309-pixel width in one column.
- DOM checks found one H1 and zero `.lunch-pick-rank` elements.
- The page background computed to `rgb(7, 11, 16)`.
- The Top Rated page retained `bodyClass=site-page lunch-page`, loaded zero `whats-for-lunch.css` links, and had zero horizontal overflow.
- Browser console query returned an empty list for warning and error entries.

## Pass / Fail

| Test case | Result | Reason |
| --- | --- | --- |
| Candidate health and WFL delivery | Pass | All three requests returned HTTP 200. |
| Today's persisted picks | Pass | API returned `success=true` and three records. |
| Coordinate nearby selection | Pass | API returned `success=true` and three fresh records. |
| ZIP nearby selection | Pass | API returned `success=true` and three fresh records. |
| ZIP UI flow | Pass | Three addressed restaurant cards rendered after the submitted ZIP. |
| Desktop Void console | Pass | Three equal cards, disclosure, Void palette, and no ranking badges were observed. |
| Mobile responsive layout | Pass | One-column 309-pixel cards rendered with zero horizontal overflow. |
| Stylesheet isolation | Pass | Top Rated did not load the dedicated Picks stylesheet. |
| Browser diagnostics | Pass | No browser console warnings or errors were captured. |
| Automated support | Pass | Focused tests and full `:website:check` completed successfully. |

## Evidence

- Focused command: `.\gradlew.bat :website:test --tests "*RatingWeightedRestaurantSelectorTest" --tests "*RestaurantRatingQueryRepositoryTest" --tests "*RestaurantServiceTest" :website:jsTest --no-daemon`
- Focused result: 8 selector tests, 3 rating-query tests, 60 service tests, and 313 JavaScript tests passed.
- JavaScript syntax: `node --check website/src/main/resources/static/js/whats-for-lunch.js` passed.
- Full command: `.\gradlew.bat :website:check --no-daemon`
- Full result: `BUILD SUCCESSFUL` in 2 minutes 59 seconds, including Java, 313 JavaScript tests, 150 Pester tests, boot JAR, deployment build context, sensors, and static fingerprinting.
- Runtime process and listener checks recorded candidate PID `60080` on `:8081` and production PID `57904` on `:8080`.
- Full-page desktop and mobile screenshots were inspected in the in-app browser during this run.
- Application logs record Tomcat starting on port 8081 and MongoDB connecting to localhost.

## Bugs / Follow-ups

Independent review found one pre-publication accessibility defect not visible in the anonymous local browser pass: authenticated rating paragraphs received the shared light-theme paragraph color instead of the Void teal. A regression reproduced the CSS cascade, commit `58019300a65af830f40a9f7a39e334214e0d9eb7` added explicit scoped selectors for both anonymous and authenticated markup, and the final reviewer verdict was ready to merge with no remaining findings.

## Post-Review Verification

- The new regression failed against the previous stylesheet and passed after the scoped fix.
- `node --test website/src/test/js/a11y-markup.test.js`: 11 passed.
- `:website:jsTest`: 313 passed.
- Final `:website:check`: `BUILD SUCCESSFUL` in 2 minutes 56 seconds after the fix.
- The corrected teal `#75cabb` computes to 9.06:1 contrast against the raised card panel `#111b24`.

## Production Acceptance

- PR [#1344](https://github.com/azurras/christopherbell.dev/pull/1344) passed Windows, macOS, Ubuntu, dependency review, and CodeQL for Actions, Java/Kotlin, and JavaScript/TypeScript.
- The PR merged as `9c69623049829394f245515b8d1751c9f7579271`; its tree exactly matches the verified feature head tree.
- Automatic deployment rotated the production listener from PID `57904` to PID `55848` and published fingerprinted asset `/db0009f03ea001ffc654/css/whats-for-lunch.css`.
- Public HTTPS liveness, readiness, `/wfl`, today's picks, coordinate nearby picks, and ZIP nearby picks all returned HTTP status code: 200.
- All sampled production restaurants had real city/state data; no response contained `Imported Metro, TX`.
- Authenticated production browser verification rendered three equal 373 by 474 desktop cards, 309-pixel single-column mobile cards, zero horizontal overflow, no rank badges, and no console warnings or errors.
- All six authenticated overall/personal rating lines computed to `rgb(117, 202, 187)` on `rgb(17, 27, 36)` card panels.

No required bug or follow-up remains.
