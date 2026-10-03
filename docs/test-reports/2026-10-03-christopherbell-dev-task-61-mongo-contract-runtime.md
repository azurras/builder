# christopherbell.dev Task 61 Mongo Contract Runtime Verification

## Document Status

complete

## Story/Issue

Builder implementation plan Task 61: fix malformed lease validation, admin activity save semantics, and outdated Mongo restaurant contract fixtures.

## Branch

`codex/mongo-contract-failures-20261002`, based on `d4b73f8699d5faa12b1d5884a3ff52e37778d91a` (`origin/main`). The candidate was built from that revision plus the four reviewed source/test file changes. Candidate JAR SHA-256: `F5CC153E29B8F6F51D0C347D70A855BD1C2756EE4ABC5BFB93414EE28F50EA42`.

## App / Environment

Windows 11; Java 25.0.3; Spring Boot 4.1.1; MongoDB 8.3. Candidate profile `test`, bound to `127.0.0.1:18086`. The candidate's only database target was `mongodb://127.0.0.1:27024/test`, backed by a fresh loopback-only MongoDB process (PID 6156). A deterministic `TARGET_ACTIVE` cutover-ledger fixture matching `DomainCollectionCutoverLedgerTest` and the current `DomainCollectionManifest.DIGEST` was seeded in this isolated test database; no production records or business data were copied. `APP_SCHEDULING_ENABLED=false`; command-center, mail, federation, Cane's, WFL monthly import, and VIN collectors were explicitly disabled. The disposable Mongo database contained only the synthetic ledger before application startup.

## Local Run Details

Built artifact: `website/build/libs/website.jar`. Started with:

```powershell
$env:SPRING_PROFILES_ACTIVE='test'
$env:SPRING_MONGODB_URI='mongodb://127.0.0.1:27024/test'
$env:APP_SCHEDULING_ENABLED='false'
java -jar website/build/libs/website.jar --server.address=127.0.0.1 --server.port=18086
```

The process was PID 3532. Startup logs identified Spring Boot 4.1.1, the `test` profile, and Mongo server `127.0.0.1:27024`; its TCP connections were owned by PID 3532. The complete process-session log was captured during this task; the relevant startup and HTTP response evidence is recorded below. The app was stopped with Ctrl+C. The candidate listener was confirmed closed. Isolated Mongo PIDs 6156, 20420, and 1944 were shut down through Mongo's admin shutdown command; ports 27022, 27023, and 27024 were confirmed closed. Production listeners remained on 8080 and 27017, with `ChristopherBellDev`, `MongoDB`, and `cloudflared` still Running/Automatic.

## Test Cases

1. Public liveness endpoint on the packaged candidate.
2. Public readiness endpoint, including the candidate's Mongo readiness contributor.
3. Public home route.
4. Candidate-to-database connection and migration ledger status.
5. Real-Mongo repository contract regressions and repository-wide checks.

## Data Sent

- `GET http://127.0.0.1:18086/actuator/health/liveness`, no body or special headers.
- `GET http://127.0.0.1:18086/actuator/health/readiness`, no body or special headers.
- `GET http://127.0.0.1:18086/`, no body or special headers.
- Automated database contracts used the isolated database named `test`; no production URI or port was supplied.

## Response Received

- Liveness HTTP response: status code 200; response body `{"status":"UP"}`.
- Readiness HTTP response: status code 200; response body `{"status":"UP"}`.
- Home HTTP response: status code 200; 3,981 UTF-8 bytes; page title `CB | Home`.
- Windows TCP inspection showed established connections from candidate PID 3532 to `127.0.0.1:27024`; Mongo reported database `test`. Startup completed successfully. The isolated test DB then contained 16 migration/ledger documents and zero migration records with status `FAILED`.
- Focused real-Mongo contract tests: 34 passed, 0 failed, including malformed lease no-write behavior, `AdminActivityRepository.save` update-vs-insert behavior, and restaurant fixture constraints. The full opt-in `:website:test` suite also completed successfully.
- Default `:website:check` rerun exited 0. Its Java XML reports contained 1,975 tests, 0 failures, 0 errors, and 108 opt-in skips. JavaScript tests reported 372 passed and 0 failed; native installer/operations Pester reported 203 passed, 0 failed, 1 skipped; shared-folder worker Pester reported 75 passed, 0 failed.

## Pass / Fail

All listed candidate HTTP, database-connection, focused-contract, and default-check cases passed. During final review, a temporary `createdOn` assertion failed for a restaurant with an explicit ID because auditing correctly treats it as existing and does not set the creation timestamp; the stale assertion was removed while retaining the `lastUpdatedOn` and cursor-order checks. The final focused Mongo run then passed all 34 tests. The first default-check process was interrupted mid-suite with Windows exit `0x40010004`; its rerun completed successfully with exit code 0. Two preliminary candidate starts were rejected by the site's schema guard: the reused test fixture failed migration 009 and a blank database lacked the required active cutover ledger at migration 015. The final candidate used a fresh isolated database with the repository's deterministic valid ledger fixture and started successfully.

## Evidence

- Candidate startup log: Spring Boot `4.1.1`, active profile `test`, Mongo server `127.0.0.1:27024`, `Tomcat started on port 18086`, and `Started Application`.
- HTTP probe results and process/port ownership were collected live from PowerShell on 2026-10-03.
- Focused contracts and full opt-in suite were run against a disposable MongoDB bound only to loopback.
- `:website:check --no-daemon --console=plain --quiet` exited 0; Java XML results are under the worktree's ignored `website/build/test-results/test`.
- Candidate artifact: `website/build/libs/website.jar`, SHA-256 listed above.
- A read-only check of production health returned HTTP 200 for liveness, readiness, and `/`; this was observation only and did not point the candidate at production MongoDB.

## Bugs / Follow-ups

No runtime failure remains for this candidate. The first two startup failures were test-fixture setup issues and were not repaired by bypassing the schema guard.

PR #1462 passed Dependency Review, CodeQL, and Java 25 builds on Ubuntu, macOS, and Windows. It was squash-merged as `df3a1e0143e2f909c7c9ced389fbea4a3ea73fbf`. The supported SYSTEM auto-deployer activated that exact SHA. During candidate build/validation, `auto-status` reported `DEPLOYING` and later `STALE` while the previous release continued to serve healthy responses; it subsequently refreshed to `SUCCEEDED`, then `UP_TO_DATE`, with `activeSha` and `successfulSha` equal to the merge SHA. The transient stale period cleared without manual intervention.

Post-deployment proof on 2026-10-03: `ChristopherBellDev`, `MongoDB`, and `cloudflared` were Running/Automatic; port 8080 was owned by the website process and MongoDB listened on 127.0.0.1:27017. Local liveness and readiness returned HTTP 200 with `{"status":"UP"}`. Local and public `https://www.christopherbell.dev/` home requests returned HTTP 200 with title `CB | Home`. No manual deploy, restart, production database write, or migration command was issued.

The deployment is complete. Follow-up: assess whether the long-running deployment status should publish progress heartbeats so operators can distinguish a slow active candidate validation from a hung deploy without treating a recoverable stale interval as terminal.
