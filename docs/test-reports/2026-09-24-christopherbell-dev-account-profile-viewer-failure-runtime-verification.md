## Document Status

complete

## Story/Issue

Runtime verification for the public-profile viewer lookup failure fix. An unexpected repository error resolving an authenticated viewer had been swallowed and represented as anonymous profile state.

## Branch

`codex/account-profile-viewer-read-failure-20260924`, based on `origin/main` SHA `e352dbaef7bd2da4b10e591961230d5182a1d897`. Candidate JAR SHA-256: `603AB56EAAB3A4586AA9D67D648CACD241F3D08763298958A475C2342C1019FC`. The candidate included the uncommitted service and test changes on this branch.

## App / Environment

Native Windows, Java 25.0.3, Spring Boot 4.1.0. Candidate URL `http://127.0.0.1:8082`, profiles `test,deploy-smoke`. Disposable PostgreSQL 18 cluster listened only on `127.0.0.1:5433`; database `test`, role `christopherbell_test`, schema `cbtest_profileviewer`, Flyway version 27. The test database guard accepted the target. The account fixture used an `.invalid` email address and existed only in this disposable database.

Production remained on port 8080, listener PID 14424; `ChristopherBellDev` remained Running/Automatic. Candidate did not connect to or mutate production storage.

## Local Run Details

Working tree: `A:\Projects\christopherbell.dev-worktrees\account-profile-viewer-read-failure-20260924`.

The packaged candidate was started as hidden Java process PID 8888 from `website/build/libs/website.jar` with `SERVER_PORT=8082`, `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5433/test`, `SPRING_DATASOURCE_USERNAME=christopherbell_test`, empty test password, `SPRING_DATASOURCE_HIKARI_SCHEMA=cbtest_profileviewer`, `APP_TEST_SCHEMA=cbtest_profileviewer`, `APP_PERSISTENCE_SCHEMA_PREFIX=cbtest_profileviewer_`, and JVM option `-Djdk.net.unixdomain.tmpdir=A:\Temp`. Flyway used `cbtest_profileviewer_` table prefixes and public migration metadata.

Candidate stdout/stderr were captured at `A:\Temp\site-account-profile-viewer-retry.stdout.log` and `A:\Temp\site-account-profile-viewer-retry.stderr.log`. An initial candidate launch exited because the disposable schema had not yet been created and the database guard correctly rejected `current_schema=public`. After creating `cbtest_profileviewer` in the disposable database, the candidate started successfully in 5.4 seconds. Candidate PID 8888 and the PostgreSQL 18 cluster were stopped after verification. Ports 8082 and 5433 were released; production port 8080 remained on PID 14424.

## Test Cases

1. Confirm PostgreSQL identity and test schema before candidate startup.
2. GET liveness and readiness on port 8082.
3. GET `/` on port 8082.
4. Obtain a local XSRF token from `/signup`, POST a synthetic test account, and GET its public profile without authentication.
5. Confirm the JavaScript, Java, and configured Windows PowerShell checks complete through `:website:check`.
6. Red/green regression: authenticated viewer repository failure initially failed its assertion, then propagated after the fix; missing-auth and missing-viewer fallbacks remained anonymous.

## Data Sent

All HTTP traffic targeted `127.0.0.1:8082` only.

- `GET /actuator/health/liveness`
- `GET /actuator/health/readiness`
- `GET /`
- `GET /signup` to obtain an XSRF cookie
- `POST /api/accounts/2024-12-15/create` with synthetic first/last names, username `profileaudit20260924`, email `profile-audit-20260924@example.invalid`, and a test-only password field (not retained here); the request included the matching XSRF header and cookie.
- `GET /api/accounts/2025-09-14/profile/profileaudit20260924` without authentication.

The isolated database identity check returned database `test`, role `christopherbell_test`, schema `cbtest_profileviewer`, and Flyway version 27. No external service was called by the `deploy-smoke` candidate profile.

## Response Received

- Liveness: status code 200, body `{"status":"UP"}`.
- Readiness: status code 200, body `{"status":"UP"}`.
- Homepage: status code 200, title `CB | Home`.
- Test account creation: status code 201.
- Anonymous profile read: status code 200; username `profileaudit20260924`, `self=false`, `followedByMe=false`, `postCount=0`.
- Final listener readback: candidate PID 8888 on port 8082 before stop; production PID 14424 on port 8080. After cleanup, port 8082 and the disposable PostgreSQL server were stopped; production remained Running/Automatic.

## Pass / Fail

- Focused `:website:test --tests dev.christopherbell.account.AccountServiceTest --no-daemon`: regression red before implementation (47 tests, one failure at the storage-error assertion); green after implementation and fallback coverage (48 tests, zero failures/errors).
- Full `:website:check --no-daemon`: pass in 3m50s. Java results: 2,287 tests, zero failures/errors, 302 skipped because database/provider contract prerequisites were unavailable or explicitly gated. JavaScript: 343/343 passed. Shared-folder operations Pester: 182 passed, one non-elevated real-ACL case skipped. Shared-folder worker Pester: 75/75 passed.
- Candidate readiness, liveness, homepage, test account creation, and anonymous profile read: pass.
- Candidate and disposable database cleanup: pass. Production service/listener remained unchanged.

## Evidence

- `:website:check --no-daemon` exited 0 (`BUILD SUCCESSFUL`).
- Final Java XML results under `website/build/test-results/test`: 362 suite files, 2,287 tests, zero failures/errors, 302 skipped.
- Focused account test XML: 48 tests, zero failures/errors/skips.
- Candidate startup log: `Started Application in 5.402 seconds`; `Tomcat started on port 8082`.
- Isolated database readback: `test|christopherbell_test|cbtest_profileviewer`, Flyway version `27`.
- Public local profile response: status code 200 with the expected anonymous viewer flags.
- `git diff --check`: pass.

## Bugs / Follow-ups

The fix is locally verified but not yet published or deployed. The storage-failure path is proved by the red/green service regression; runtime coverage verifies the adjacent anonymous profile path. Production deployment still requires the documented elevated `prod.cmd auto-install` approval before the protected SYSTEM deployer can refresh its bundle and deploy merged code.
