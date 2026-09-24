## Document Status

blocked

## Story/Issue

Remove PostgreSQL as a supported application and production deployment backend. Verify the MongoDB-only working tree and attempt isolated Spring runtime validation.

## Branch

`codex/mongodb-only-persistence-20260924`, based on `f4382d118db9db43efc952dc08e96649e2c70753`. The application candidate was built from the uncommitted working tree on this branch.

## App / Environment

- App: christopherbell.dev Spring Boot application.
- Profile: `test`.
- Candidate URL/port: `http://127.0.0.1:18081`.
- MongoDB: installed MongoDB 8.3 binary run as a disposable standalone process on `127.0.0.1:27019`, database `test`, fresh temporary dbpath. `SPRING_MONGODB_URI` explicitly targeted this listener with a 1-second server-selection timeout; the production/default listener on port 27017 was not used.
- External behavior flags: shared folder, music, Canes box tracker, and federation discovery/inbound/outbound disabled. A temporary non-production JWT secret was set and is omitted here.

## Local Run Details

Started with:

```text
./gradlew --no-daemon --max-workers=1 :website:bootRun --args='--spring.profiles.active=test --server.port=18081 --app.shared-folder.enabled=false --app.music.enabled=false --canes-box-tracker.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false' --console=plain
```

Gradle used the isolated cache `A:\Projects\christopherbell.dev-worktrees\.gradle-mongodb-only-persistence` and `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Windows\Temp`. Candidate Java PID 22980 exited with code 1 before readiness. Disposable MongoDB PID 34312 was stopped. Port 18081 is not left listening. Temporary MongoDB data files remain under `%TEMP%\codex-mongodb-only-89e30307754a4adbb1ca537a4ae4105e`; deletion was blocked by the command policy. The production MongoDB listener on port 27017 (PID 5388) remained running and was not stopped or reconfigured.

## Test Cases

1. Full Gradle website check (`:website:check`) with Mongo integration opt-ins unset and an explicit disposable Mongo URI.
2. Local Spring Boot startup and readiness attempt against the disposable MongoDB database.

## Data Sent

- Automated tests: no production database URI or production credentials; database integration contracts requiring `MONGODB_INTEGRATION_TESTS` or `DOMAIN_COLLECTION_TEST_URI` were not enabled.
- Runtime: no HTTP request was sent because the application failed during startup before opening port 18081.

## Response Received

- `:website:check`: `BUILD SUCCESSFUL` in 5m 2s. JUnit XML reports 1,960 tests, 0 failures, 0 errors, and 108 skipped. JavaScript: 343 passed, 0 failed. Deployment Pester suite: 201 passed, 0 failed, 1 skipped. Shared-folder worker Pester suite: 75 passed, 0 failed, 0 skipped.
- Runtime startup logs: Spring connected to `127.0.0.1:27019`, then failed closed at migration `015-require-domain-collection-schema` because the fresh disposable database did not contain the exact active domain-cutover ledger. The application did not reach readiness. No ledger was fabricated or copied from production.
- Read-only listener inspection showed port 27017 owned by PID 5388 and no listener left on ports 18081 or 27019 after cleanup.

## Pass / Fail

- Full Gradle check: PASS.
- MongoDB-only configuration and deployment checks: PASS within the full Gradle check.
- Runtime readiness: BLOCKED by the intentional migration-015 cutover-ledger prerequisite on an empty database; this does not establish a PostgreSQL-removal regression.
- Production deployment: not performed.

## Evidence

- Gradle console output from the completed `:website:check` invocation.
- JUnit XML under `website/build/test-results/test/` for full Java-suite counts.
- BootRun console output showed test profile, Tomcat configured for port 18081, Mongo connection to the disposable port 27019, and migration 015 failure before server readiness.
- Read-only listener inspection showed port 27017 owned by PID 5388 and no listener left on ports 18081 or 27019 after the Mongo process stopped.

## Bugs / Follow-ups

The disposable empty database cannot satisfy the migration-015 cutover guard. Runtime readiness needs validation against an authorized restored backup in a separate disposable database containing the valid cutover ledger. Do not bypass or synthesize that ledger. No production files, services, or data were changed.
