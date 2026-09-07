# WFL Archived Session Recovery Test Report

## Document Status

complete

## Story/Issue

Builder work item: [WFL archived session recovery](../session-memory/christopherbell-dev.md#source-docs-work-2026-08-03-wfl-archived-session-recovery-md).

## Branch

- Repository: `azurras/christopherbell.dev`
- Branch: `codex/wfl-archived-session-recovery`
- Commit: `255df4d1` (`Recover archived WFL sessions locally`)

## App / Environment

- App: christopherbell.dev Spring Boot website
- Profile: `local`
- Candidate base URL: `http://127.0.0.1:8094`
- Candidate database: disposable MongoDB database `christopherbell_dev_wfl_archived_recovery_candidate`
- Production comparison URL: `http://127.0.0.1:8080`
- Fixture context: six synthetic Austin restaurants, synthetic ZIP `78701`, and synthetic member `archive-recovery@example.test`
- Gradle home: `A:\Projects\christopherbell.dev-gradle-homes\wfl-archived-session-recovery`

## Local Run Details

The packaged candidate JAR was built from the isolated worktree and started with:

```powershell
java -jar A:\Projects\christopherbell.dev-worktrees\wfl-archived-session-recovery\website\build\libs\website.jar --spring.profiles.active=local --server.port=8094 --spring.mongodb.uri=mongodb://127.0.0.1:27017 --spring.mongodb.database=christopherbell_dev_wfl_archived_recovery_candidate --command-center.enabled=false --canes-box-tracker.enabled=false --wfl.restaurant-import.monthly.enabled=false --wfl.restaurant-of-the-day.enabled=false --app.mail.enabled=false --app.browser-security.public-base-url=http://localhost:8094
```

The final candidate process was PID `65840`. Logs were captured under `A:\Projects\christopherbell.dev-worktrees\wfl-archived-session-recovery\build\wfl-archived-session-recovery-runtime\`. The candidate was stopped after testing, port `8094` was confirmed free, and the disposable database was dropped and confirmed absent.

## Test Cases

1. Candidate readiness and production isolation.
2. Active shared-session restaurant refresh remains mutable for the host.
3. An archived session restored implicitly from saved member state is discarded without a conflict error.
4. An explicit archived-session URL remains readable for a participant and exposes disabled voting.
5. Location selection from an explicit archive starts a new active session rather than mutating the archive.
6. `Try 3 more` from an explicit archive exits the archive and requests a fresh location instead of issuing an archived-session mutation.
7. Candidate browser console remains free of warnings and errors.
8. Automated regression and aggregate verification cover the final tree.

## Data Sent

- Browser UI signup/login used the synthetic account `archive-recovery@example.test` / `archive-recovery`.
- Browser UI input submitted ZIP `78701` with `Use ZIP` on `/wfl`.
- Browser clicks created a shared session with `Lunch with Friends` and selected `Try 3 more`.
- The exact synthetic session `f931fc45-0e2b-4fa6-b589-2426c8992e77` was archived in the disposable database by setting only its `activeUntil` to one minute in the past; its deletion deadline remained in the future.
- Browser navigation reloaded plain `/wfl`, opened `/wfl?session=f931fc45-0e2b-4fa6-b589-2426c8992e77`, submitted ZIP `78701` from the archive, and separately selected archived `Try 3 more`.
- Health requests: `GET http://127.0.0.1:8094/actuator/health/readiness` and `GET http://127.0.0.1:8080/actuator/health/readiness`.

## Response Received

- Status code: `200` with response body `{"status":"UP"}` from candidate readiness.
- Active shared refresh changed the restaurant IDs from `recovery-echo,recovery-charlie,recovery-bravo` to `recovery-delta,recovery-echo,recovery-foxtrot`; MongoDB revision advanced from `0` to `1` and `restaurantResetCount` from `0` to `1`.
- UI result: plain `/wfl` after archival rendered `Share your location` with the ZIP/location controls and no archived-session conflict alert.
- UI result: the explicit archive rendered `Archived lunch session`, the original three picks, read-only explanatory copy, disabled session vote buttons, and an enabled `Try 3 more` button.
- UI result: submitting ZIP `78701` from the explicit archive redirected to `/wfl` and created new active session `5c03a5ef-b91b-4aae-92b8-5d1a0d3bb671` at revision `0`.
- The archived session remained revision `1`, reset count `1`, and retained `recovery-delta,recovery-echo,recovery-foxtrot` after the new session was created.
- UI result: selecting `Try 3 more` directly from the archive redirected to `/wfl` and rendered `Share your location`; no archived-session mutation error appeared.
- Browser warning/error log query returned an empty list.
- Status code: `200` from production readiness on port `8080` after candidate shutdown and cleanup.

## Pass / Fail

- Candidate readiness and isolation: **PASS** â€” candidate was healthy on `8094`; production remained healthy on `8080`.
- Active shared-session refresh: **PASS** â€” the host mutation succeeded and advanced the exact session revision.
- Implicit archived-session recovery: **PASS** â€” saved archived state was discarded and normal initialization continued.
- Explicit archive readability: **PASS** â€” archived picks remained visible and voting stayed read-only.
- Fresh location flow from archive: **PASS** â€” a different active session was created while the archive was unchanged.
- Fresh `Try 3 more` flow from archive: **PASS** â€” the browser left the archive and requested location without a 409 conflict.
- Browser diagnostics: **PASS** â€” no warning or error entries.
- Cleanup: **PASS** â€” candidate stopped, port freed, disposable database removed, production ready.

## Evidence

- Focused regression: `node --test website/src/test/js/whats-for-lunch-session-recovery.test.js` â€” 7 passed, 0 failed.
- JavaScript suite: `gradlew.bat :website:jsTest --no-daemon --console=plain` â€” 343 passed, 0 failed.
- Aggregate suite: `gradlew.bat :website:check --no-daemon --console=plain` â€” `BUILD SUCCESSFUL` in 3m 4s; 21 actionable tasks (13 executed, 8 up-to-date), including Java, JavaScript, packaging/static checks, and Windows/Pester verification.
- Candidate database evidence recorded exact session IDs, restaurant IDs, revisions, activity deadlines, and reset counts before and after each browser action.
- Final cleanup evidence: MongoDB returned `{"ok":1,"dropped":"christopherbell_dev_wfl_archived_recovery_candidate"}`, the database existence check returned `false`, and production readiness returned status code `200`.

## Bugs / Follow-ups

Candidate testing initially found that explicit archive URLs attempted `POST .../join`, which correctly returned `WFL_SESSION_EXPIRED`, and that the archived `Try 3 more` control was disabled. Both gaps were added to the regression suite, corrected, rebuilt, and retested successfully. No open defects or intentional verification gaps remain for this work item.
