## Document Status
complete

## Story/Issue
2026-09-23 christopherbell.dev site bug audit. Reproduction and correction of overdue WFL monthly startup catch-up selection.

## Branch
`codex/site-bug-audit-20260923`, source base `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c`; packaged candidate SHA-256 `093DA56E274CF7DDA8446A20F623B1B23CD3D5A845B751052A597F3AA2770347`.

## App / Environment
`christopherbell.dev`, Spring Boot 4.1.0 / Java 25.0.3. Candidate ran at `http://127.0.0.1:8082` with profiles `test,deploy-smoke`, against a disposable PostgreSQL 18 cluster on `127.0.0.1:5433`, database `test`, user `christopherbell_test`, schema prefix `cbtest_sitebugaudit_`. Production remained on port 8080 (listener PID 14424); candidate used PID 26956. The separate cluster was initialized specifically for this run and never connected to production data.

## Local Run Details
Working directory: `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`.
Start command: `java -jar website/build/libs/website.jar --spring.flyway.placeholders.schema_prefix=cbtest_sitebugaudit_ --spring.flyway.default-schema=public --spring.flyway.schemas=public` with `SERVER_PORT=8082`, `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5433/test`, `SPRING_DATASOURCE_USERNAME=christopherbell_test`, empty test password, `SPRING_DATASOURCE_HIKARI_SCHEMA=cbtest_sitebugaudit`, `APP_TEST_SCHEMA=cbtest_sitebugaudit`, and `APP_PERSISTENCE_SCHEMA_PREFIX=cbtest_sitebugaudit_`. Java used `-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk` due to the host's Java 25 loopback socket temp-path issue. Logs were captured in the local process session. Candidate and temporary PostgreSQL cluster were stopped after verification. The production listener was not changed.

## Test Cases
- GET /actuator/health/liveness.
- GET /actuator/health/readiness.
- GET /.
- GET /wfl/top-liked.
- GET /api/whatsforlunch/restaurant/2026-07-26/freshness.
- Verify candidate's PostgreSQL identity and latest Flyway schema version from the disposable cluster.

## Data Sent
Unauthenticated GET requests to http://127.0.0.1:8082/actuator/health/liveness, http://127.0.0.1:8082/actuator/health/readiness, http://127.0.0.1:8082/, http://127.0.0.1:8082/wfl/top-liked, and http://127.0.0.1:8082/api/whatsforlunch/restaurant/2026-07-26/freshness. No query parameters, headers, or request bodies. No production write or account mutation was performed.

## Response Received
All five HTTP requests returned HTTP status code 200. Both health probes returned `{"status":"UP"}`. The homepage and WFL ranking returned HTML (3,981 and 3,112 bytes). Freshness returned JSON (6,580 bytes; the isolated database had no imported OSM freshness state, so its `lastRefreshedOn` was null). PostgreSQL reported database `test`, latest successful Flyway version `27`. At verification time, port 8082 was owned by candidate PID 26956 and production port 8080 remained owned by PID 14424.

## Pass / Fail
Pass. Candidate startup completed; liveness and readiness were UP; homepage, ranking and freshness API returned HTTP status code 200; database identity was the isolated `test` DB; both candidate and disposable database were stopped afterward.

## Evidence
- Candidate startup log: Spring Boot 4.1.0, port 8082, `Started Application in 5.633 seconds`.
- Timestamped HTTP and listener observations: 2026-09-23, approximately 17:00 America/Chicago.
- `psql` on port 5433 reported `current_database=test`, `version=27` from `public.flyway_schema_history`.
- `Get-NetTCPConnection` showed ports 8082/PID 26956 and 8080/PID 14424.
- Candidate SHA-256: `093DA56E274CF7DDA8446A20F623B1B23CD3D5A845B751052A597F3AA2770347`.
- Live production freshness was separately read-only checked before the fix and showed `lastRefreshedOn=2026-08-02T22:44:50.963Z`, `current=false`. Production freshness was not expected to change during this local smoke run.

## Bugs / Follow-ups
The stale live OpenStreetMap freshness marker establishes data age, not the sole cause of scheduled import failure. The fix retries when the latest configured monthly occurrence is due, using the existing lease-protected workflow. Confirm live freshness and import recovery after authorized deployment; protected application logs remain ACL-denied and were not accessed by changing permissions.
