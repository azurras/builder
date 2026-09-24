## Document Status

complete

## Story/Issue

MongoDB-only persistence PR #1432. Follow-up runtime startup proof against a trusted MongoDB backup copy after the earlier empty-database attempt was blocked at migration 015. This report supplements, and does not replace, `2026-09-24-christopherbell-dev-mongodb-only-runtime-verification.md`.

## Branch

`codex/mongodb-only-persistence-20260924`, candidate commit `3935d3d735310264ee5e2b7e3eda11b801bdcee7`.

## App / Environment

- App: christopherbell.dev Spring Boot application, test profile.
- Candidate URL/port: `http://127.0.0.1:18081`.
- Database: `christopherbell` restored from `christopherbell-native-20260924T193158Z.archive.gz` to a fresh standalone MongoDB 8.3 process bound only to `127.0.0.1:27019`.
- Archive SHA-256 matched its sidecar: `E94D6664691190AFF6680969977908A9638F7250C0587424CDFC41B4F26DB477`.
- Effective `SPRING_MONGODB_URI` explicitly targeted `mongodb://127.0.0.1:27019/christopherbell`; no production URI or credentials were used. A temporary non-production `APP_JWT_SECRET` was set and is omitted.
- Candidate port 18081 was confirmed free before startup. Shared folder, music, Cane's tracker, federation discovery/inbound/outbound, and WFL monthly import/catch-up were disabled for the successful run.

## Local Run Details

From the MongoDB-only PR worktree, launched with Java 25.0.3 and the isolated Gradle cache `A:\Projects\christopherbell.dev-worktrees\.gradle-mongodb-only-persistence`:

```text
./gradlew --no-daemon --max-workers=1 :website:bootRun --args='--spring.profiles.active=test --server.port=18081 --app.shared-folder.enabled=false --app.music.enabled=false --canes-box-tracker.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --wfl.restaurant-import.monthly.enabled=false' --console=plain
```

The candidate started as PID 36252, reached Spring Boot `Started Application`, and was stopped with Ctrl+C after endpoint checks. The isolated MongoDB process (PID 24624) was stopped. Ports 18081 and 27019 no longer listen; the production MongoDB process (PID 5388) remained running. The restored temporary data directory remains at `%TEMP%\codex-mongodb-only-restored-20260924T193158Z` because host command review rejected recursive deletion; cleanup was not bypassed.

## Test Cases

1. Restore the checksum-verified backup into the isolated MongoDB and allow candidate startup to exercise the existing migration-015 ledger.
2. Verify actuator readiness and the public root route from the candidate.

## Data Sent

- `mongorestore` restored the `christopherbell.*` namespace only into the fresh listener on `127.0.0.1:27019`; 78,239 documents restored, 0 failed.
- `GET http://127.0.0.1:18081/actuator/health/readiness` with no request body or credentials.
- `GET http://127.0.0.1:18081/` with no request body or credentials.
- No requests were sent to the production application or production MongoDB listener.

## Response Received

- Candidate connected to MongoDB at `127.0.0.1:27019` and logged `Started Application` without the migration-015 cutover-ledger failure.
- Readiness: HTTP/1.1 200, body `{"status":"UP"}`.
- Root route: HTTP/1.1 200, `text/html; charset=UTF-8`, HTML title present.
- First exploratory run omitted the WFL monthly-disable override. Test-profile startup catch-up contacted Overpass and received HTTP/1.1 504 while the app remained available. The app used only the disposable restored database. The successful run disabled this catch-up explicitly; a separate follow-up is tracked because test-profile defaults should not make that network request.

## Pass / Fail

- Restored-backup Spring startup: PASS.
- Readiness: PASS (`UP`).
- Root page: PASS (HTTP/1.1 200 with title).
- External startup catch-up on first exploratory run: unexpected, received Overpass HTTP/1.1 504; follow-up tracked separately.
- Production state isolation: PASS; Mongo connection logs targeted only port 27019, candidate listened only on 18081, and production MongoDB stayed running.
- Temporary database filesystem cleanup: incomplete because recursive deletion was rejected by host command review; directory path is recorded above.

## Evidence

- Archive sidecar and current SHA-256 matched before restore.
- `mongorestore` reported 78,239 documents restored and 0 failures.
- Spring console showed profile `test`, Mongo server `127.0.0.1:27019`, port 18081, and successful application startup.
- Direct readiness and root HTTP requests returned the results above.
- Listener/process inspection after shutdown showed ports 18081 and 27019 closed and production MongoDB PID 5388 still present.

## Bugs / Follow-ups

- Earlier empty-database failure evidence remains in the linked original report; it was a data precondition, not a MongoDB-only startup regression.
- Test profile leaves monthly WFL import/catch-up enabled by default. Its startup event attempted an Overpass call in the exploratory run; plan a separate test-profile isolation fix.
- The restored backup directory remains in the local temporary directory because host review blocked recursive cleanup.
- No production deployment or database mutation occurred.
