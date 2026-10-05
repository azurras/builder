## Document Status

blocked

## Story/Issue

Website-wide Chris Street Style coding standards audit requested 2026-10-04.

## Branch

Candidate source branch: `codex/chris-street-style-audit-20261004`, based on `origin/main` at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`. The source changes were uncommitted during verification. Candidate JAR SHA-256: `2BA46AC711E2FFDD92D44533D8E6E4F37698FF6DB9812313088C87E36124DE3F`.

## App / Environment

Spring Boot website, `test` profile, candidate port 8082. MongoDB database name was `test` in both attempts. The first attempt used the local Mongo service at `127.0.0.1:27017`; the second used an isolated temporary MongoDB instance bound to `127.0.0.1:27018`. The production website listener on port 8080 remained present throughout.

## Local Run Details

Candidate command: `java -jar website/build/libs/website.jar --server.port=8082`, with `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI` set to a URI ending in `/test`, and scoped Java 25 loopback temp configuration. Candidate process IDs were 5072 and 1672; both exited during Spring context initialization. Candidate logs: `%TEMP%\chris-style-20261004-182030-out.log` and `%TEMP%\chris-style-20261004-182259-out.log` (matching `-err.log` files). The temporary MongoDB process used PID 34208, port 27018, and was stopped. Its data directory remains under `%TEMP%\chris-street-style-mongo-20261004\data`; automatic review rejected recursive removal as blocked by policy. No service remains on port 27018.

## Test Cases

- Readiness: `GET http://127.0.0.1:8082/actuator/health/readiness`.
- Home page: `GET http://127.0.0.1:8082/` after startup failure.
- Native automated verification: `:website:check :cbell-lib:check`.

## Data Sent

The readiness request was a GET with no authentication or body. The home request was a GET with no authentication or body. Automated checks used the test profile and repository test fixtures. Candidate startup targeted only a Mongo database named `test`.

## Response Received

Neither startup produced an application listener on port 8082. With the local Mongo service, startup stopped with `Migration 015-require-domain-collection-schema has an incomplete durable record.` With the isolated temporary MongoDB instance, the driver connected to `127.0.0.1:27018`, then startup stopped with `Migration 015-require-domain-collection-schema failed.` The readiness and home requests received no HTTP response because startup had exited. The production website listener remained on port 8080. I did not manually change or reset the shared test database; startup may have applied any earlier pending migrations before encountering the existing incomplete 015 record.

The full native check completed successfully: `:website:check :cbell-lib:check` passed, including Java, JavaScript, Pester, deployment-context, sensor-runtime, and static-asset checks. Focused regression tests for process interruption, optional anonymous identity, restaurant creation exception contracts, and Mongo probe failure handling passed.

## Pass / Fail

Automated checks: pass. Candidate readiness and user-facing runtime proof: blocked by migration 015 before the web server opened its listener.

## Evidence

- Full check: `BUILD SUCCESSFUL in 4m 15s`.
- Isolated Mongo preflight: `1:test` on port 27018.
- Candidate log at `%TEMP%\chris-style-20261004-182259-out.log` confirms MongoDB driver host `127.0.0.1:27018` and migration 015 startup failure.
- Final listener inspection showed ports 8080 and 27017 still owned by their prior processes, with no listener on 8082 or 27018.
- `git diff --check` passed.

## Bugs / Follow-ups

Do not reset or bypass the incomplete migration record as part of this style audit. Runtime verification and any merge/deployment remain blocked until migration 015 can be exercised against an authorized, healthy disposable database. The temporary Mongo process is stopped; only its temporary data directory remains because the approval review rejected recursive removal.

## Follow-up Review and Checks

The continued source review found three additional exception-contract corrections: command-center action launch catches its declared `IOException` and retains it as the `InvalidRequestException` cause; metrics collection catches only `ExecutionException` or `CancellationException` from provider futures; restaurant import month parsing catches `DateTimeParseException`. `EmailSanitizer` now catches the expected IDN/address parse exceptions and preserves their causes. The email sanitizer test asserts the retained IDN cause.

Focused `EmailSanitizerTest`, `CommandCenterActionServiceTest`, `CommandCenterMetricsServiceTest`, and `RestaurantImportWorkflowServiceTest` passed. The full `:website:check :cbell-lib:check` passed in 4m13s after these edits, including JavaScript, Pester, deployment-context, sensor-runtime, and static-asset checks. The native PowerShell AST parser accepted all 29 tracked PowerShell files; PSScriptAnalyzer is not installed. `git diff --check` passed. The packaged candidate built by the full check has SHA-256 `0FF79B4C532306D467ADA2C665B96334E49B2429E9C5D77D2C6007BE00BA4E68`.

The new follow-up edits have not received isolated application runtime proof. The prior candidate startup evidence remains blocked at Mongo migration 015; no migration record was reset or bypassed. Merge and production activation remain blocked pending runtime proof against an authorized healthy disposable database.

Follow-up source commit `9e8c18db` is pushed to the existing draft PR branch. PR CI is running for that commit; update this report with its readback before the next delivery checkpoint.
