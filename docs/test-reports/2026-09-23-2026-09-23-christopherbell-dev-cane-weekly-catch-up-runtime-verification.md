## Document Status
complete

## Story/Issue
2026-09-23 christopherbell.dev site bug audit. Alternate-port runtime verification for Cane's weekly collection startup catch-up.

## Branch
`codex/site-bug-audit-round2-20260923`, based on `f1db692c7b5dff1de7ce4490c07908935ee8f8b0`; implementation changes remain uncommitted in the isolated spoke worktree during this smoke check. Candidate JAR SHA-256: `007FF916730242EC661FE4DA5FA5C7D09C8B08E3FEA8D022098F2BDF1A2DE703`.

## App / Environment
`christopherbell.dev`, Spring Boot 4.1.0 / Java 25.0.3. Candidate URL `http://127.0.0.1:8082`, profiles `test,deploy-smoke`, isolated disposable PostgreSQL 18 cluster on `127.0.0.1:5433`, database `test`, user `christopherbell_test`, schema prefix `cbtest_sitebugaudit_`. Production listener remained on port 8080. `deploy-smoke` disables startup external collection behavior during runtime smoke.

## Local Run Details
Working directory: `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`.

Started packaged `website/build/libs/website.jar` with `SERVER_PORT=8082`, `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5433/test`, `SPRING_DATASOURCE_USERNAME=christopherbell_test`, empty test password, `SPRING_DATASOURCE_HIKARI_SCHEMA=cbtest_sitebugaudit`, `APP_TEST_SCHEMA=cbtest_sitebugaudit`, and `APP_PERSISTENCE_SCHEMA_PREFIX=cbtest_sitebugaudit_`; Flyway schema arguments were `--spring.flyway.placeholders.schema_prefix=cbtest_sitebugaudit_ --spring.flyway.default-schema=public --spring.flyway.schemas=public`. Java used `-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk` for the host Java 25 loopback socket temp-path issue. Startup log reported `Started Application in 5.416 seconds` and port 8082. Candidate was stopped with Ctrl-C after requests; disposable PostgreSQL was stopped with `pg_ctl -m fast`. No listener remained on ports 8082 or 5433.

## Test Cases
- GET /actuator/health/liveness and /actuator/health/readiness.
- GET / and /canes-box-tracker.
- GET /api/canes-box-tracker/2026-06-04/history.
- GET /wfl/top-liked and /api/whatsforlunch/restaurant/2026-07-26/freshness.

## Data Sent
Unauthenticated GET requests to http://127.0.0.1:8082/actuator/health/liveness, http://127.0.0.1:8082/actuator/health/readiness, http://127.0.0.1:8082/, http://127.0.0.1:8082/canes-box-tracker, http://127.0.0.1:8082/api/canes-box-tracker/2026-06-04/history, http://127.0.0.1:8082/wfl/top-liked, and http://127.0.0.1:8082/api/whatsforlunch/restaurant/2026-07-26/freshness. No request bodies, query parameters, or special headers. All database state was confined to the disposable `test` cluster. No production writes or external Cane's collection calls were made.

## Response Received
HTTP status code 200 for all seven requests. Liveness/readiness returned `{"status":"UP"}`. Homepage was 3,981 bytes; tracker page 6,576 bytes; Cane's history returned `{"messages":null,"payload":{"latest":null,"weeks":[]},"requestId":null,"success":true}` from the empty isolated database. WFL ranking returned HTML (3,112 bytes). WFL freshness returned JSON (6,580 bytes; no imported OSM state existed in the isolated database).

## Pass / Fail
Pass. Candidate started on isolated port 8082, all health and public route checks returned 200, and the history API returned a valid empty-history response. Candidate and temporary database were stopped afterward. This smoke check verifies normal packaged startup and routes; startup network collection is intentionally excluded by `deploy-smoke` and is covered by unit regression cases.

## Evidence
- Captured startup log: Spring Boot 4.1.0, Java 25.0.3, port 8082, PID 20024.
- Timestamp: 2026-09-23, approximately 17:56 America/Chicago.
- `Invoke-WebRequest` status and response-size observations for each of the seven URLs.
- `pg_ctl status`/stop confirmed the isolated PostgreSQL cluster lifecycle; ports 8082 and 5433 were no longer listening after cleanup.
- Candidate SHA-256: `007FF916730242EC661FE4DA5FA5C7D09C8B08E3FEA8D022098F2BDF1A2DE703`.
- Production port 8080 was not changed.

## Bugs / Follow-ups
Runtime smoke did not exercise the scheduled Cane's data source or deployment. Confirm live history freshness after the supported production release; the cause of prior missing scheduled snapshots remains unconfirmed.
