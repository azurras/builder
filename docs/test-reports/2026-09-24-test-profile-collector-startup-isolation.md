## Document Status

complete

## Story/Issue

Task 37 in the christopherbell.dev site bug-audit plan: prevent external collector catch-up during test-profile startup.

## Branch

`codex/test-profile-wfl-catchup-20260924`, candidate worktree `A:\Projects\christopherbell.dev-worktrees\test-profile-wfl-catchup-20260924`, based on `4b552a63a08c9333bdaa0d7827b23eb811920f37`. The candidate included uncommitted changes to `application-test.yml` and three regression test files. An unrelated line-ending-only change to `gradlew.bat` was preserved and excluded.

## App / Environment

Spring Boot 4.1, Java 25, `test` profile. Candidate web listener: `127.0.0.1:18081`. Mongo target: `mongodb://127.0.0.1:27019/test`, served only by a disposable local MongoDB process bound to loopback. No production database or website listener was targeted. Mail was disabled. The test profile set `wfl.restaurant-import.monthly.enabled=false` and `canes-box-tracker.enabled=false`; no WFL or Cane's command-line overrides were supplied during the final run.

The database was seeded from `A:\Projects\christopherbell.dev-backups\christopherbell-native-20260924T193158Z.archive.gz` (SHA-256 `E94D6664691190AFF6680969977908A9638F7250C0587424CDFC41B4F26DB477`) by remapping `christopherbell.*` to `test.*`. MongoDB reported 78,239 documents restored and zero failures.

## Local Run Details

The final candidate was started with `:website:bootRun --no-daemon --max-workers=1 --console=plain`, `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, and `SERVER_PORT=18081`. The attached Gradle output was the application log. The app reported startup complete in 4.394 seconds. Candidate PID 34120 and isolated MongoDB PID 14100 were stopped after verification. Ports 18081 and 27019 were confirmed closed; production MongoDB PID 5388 remained running.

An initial launch against an empty disposable `test` database failed at migration `015-require-domain-collection-schema`, which requires the site's existing migration/schema state. It did not start the app or touch production. After seeding the disposable `test` database from the verified archive, runtime verification succeeded.

The restored disposable data directory remains under `%LOCALAPPDATA%\Temp\codex-mongodb-only-restored-20260924T193158Z`. A prior host review blocked recursive deletion; the cleanup restriction was not bypassed.

## Test Cases

1. Verify configuration overlay: test profile disables monthly WFL import and Cane's collector while default application configuration retains their production defaults.
2. Verify disabled WFL startup returns before state lookup, lease acquisition, or remote preparation.
3. Verify disabled Cane's startup performs no repository work.
4. Start the default `test` profile without collector command-line overrides; check application readiness and homepage, and inspect startup output for external collector activity.

## Data Sent

The candidate made MongoDB connections to the isolated loopback server. HTTP checks were unauthenticated `GET /actuator/health/readiness` and `GET /` at `http://127.0.0.1:18081`. No request was sent to Overpass or Cane's by the final candidate according to startup logs; no manual collector action was invoked.

## Response Received

- Readiness returned status code: 200; body reported `UP`.
- Homepage returned status code: 200; rendered title was present; response size was 3,981 bytes.
- Startup logged `Started Application in 4.394 seconds`; no WFL catch-up or Cane's collection log appeared.
- During the exploratory run before adding the Cane's test-profile opt-out, the test profile did call the public Cane's API and wrote a 50/50 metro snapshot only into disposable database `test`. That observation motivated the additional Cane's regression and configuration setting.

## Pass / Fail

- Before adding the Cane's setting, `CanesBoxTrackerConfigurationTest.testProfileDisablesExternalCollector` failed as intended because the test profile inherited `enabled=true`.
- Focused final suites passed: Cane's configuration 2/2, Cane's service 19/19, WFL properties 7/7, WFL workflow 9/9 (37 passed, zero failed).
- Full native `:website:check` passed in 5m06s (21 actionable Gradle tasks; 13 executed and 8 up-to-date). The suite included the Windows production Pester checks, 75 passed and zero failed.
- Final alternate-port runtime checks passed for both endpoints. No collector startup activity appeared in logs.

## Evidence

- Commands: focused Gradle test run for the four suites; full `:website:check`; MongoDB `mongorestore` with namespace remapping; final `:website:bootRun`; PowerShell HTTP probes; process/port checks; `git diff --check`.
- Full-check and runtime output was captured in the local Codex execution sessions on 2026-09-24. `git diff --check` passed on the candidate diff.
- Regression proof is configuration-only in production terms: default `application.yml` collector settings are unchanged; only `application-test.yml` opts out.

## Bugs / Follow-ups

- Task 37 is locally verified but still needs PR publication, required hosted checks, and merge.
- The runtime test profile avoids the observed WFL and Cane's startup collectors. No packet capture was performed; absence of collection activity was established through the application logs and focused no-interaction tests.
- The restored disposable MongoDB data directory remains in the temp folder noted above because cleanup was blocked by host review.
