# Windows-only website CI: Test Report

## Story/Issue
User request: update the christopherbell.dev CI build workflow so it only targets Windows. [Implementation plan](../implementation-plans/2026-10-04-23-31-christopherbell-dev-windows-only-ci.md).

## Branch
`codex/windows-only-ci-20261004` at `b0fc64b`

## Pass / Fail

> [!CAUTION]
> **1 of 2 verification cases passed** on candidate `b0fc64b`; application runtime proof is blocked by the database cutover safety gate.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Windows-only workflow validation and full build | ✅ PASS | YAML assertions confirmed the sole runner and retained Windows steps; `gradlew.bat build` completed with 2,164 tests, 0 failures, and 110 skipped. |
| 2 | Candidate application readiness and homepage request | ⏸️ BLOCKED | The app connected to isolated database `test`, then failed migration `015-require-domain-collection-schema` because a fresh test database has no verified target cutover ledger. No HTTP request was sent. |

## Test Cases
1. **Windows-only workflow validation and full build:** parsed `.github/workflows/ci.yml`, asserted its sole runner and required Windows build/Pester/artifact steps, then ran the complete Windows Gradle build.
2. **Candidate application readiness and homepage request:** attempted to start the committed application on a temporary local port against a new, authenticated MongoDB `test` database; startup was blocked before readiness by migration 015.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `codex/windows-only-ci-20261004` at `b0fc64b` |
| Host | Windows 11, Java 25.0.3, Gradle 9.6.1 |
| Runtime profile | `local`; mail, Command Center and Cane's tracker disabled for the candidate run |
| MongoDB | Separate temporary MongoDB 8.3 instance on `127.0.0.1:64004`; authenticated database `test`; app user had `readWrite` on `test` only |
| App URL | `http://127.0.0.1:64005/` was reserved for the candidate; the HTTP listener never became ready |
| Secret handling | Random temporary credentials and JWT secret were not recorded; the running candidate used `SPRING_MONGODB_URI` for the isolated test database. |

## Local Run Details
- **Local command:** `python - .github/workflows/ci.yml` with YAML/runner assertions; `.\gradlew.bat build`; `java.exe -jar website\build\libs\website.jar --server.port=64005` with local overrides.
- **Working directory:** isolated `christopherbell.dev-worktrees/windows-only-ci-20261004` checkout.
- **Candidate identity:** committed `b0fc64b`; the full build ran on the identical tree immediately before commit.
- **Process details:** candidate JVM PID 19960 exited with code 1 during Spring startup; temporary MongoDB and application listeners were stopped and ports 64004/64005 were confirmed free. Production MongoDB on port 27017 remained running and was not used.
- **Logs:** captured to task-owned temporary files outside both repositories. Three temporary scratch directories remain on the host; the tool rejected the recursive cleanup command under its safety policy.
- **Cleanup:** candidate application and isolated MongoDB processes stopped; temporary database files and logs remain in those scratch directories. No test data was written to production.

## Data Sent

### 1. Windows-only workflow validation and full build

```text
Workflow assertions: jobs.build.runs-on == windows-latest; no OS strategy matrix; Pester 5.9.0 present; .\gradlew.bat build present; failure artifact step present; no Ubuntu/macOS runner in the build job.
Command: .\gradlew.bat build
```

### 2. Candidate application readiness and homepage request

```text
Command: java.exe -jar website\build\libs\website.jar --server.port=64005
Profile: local
SPRING_MONGODB_URI: mongodb://runtimeApp:[redacted]@127.0.0.1:64004/test?authSource=test&directConnection=true
Intended requests after startup: GET /actuator/health/readiness, then GET /
```

## Response Received

### 1. Windows-only workflow validation and full build

```text
Workflow YAML parsed; Windows runner, Pester, Gradle build, and failure artifacts verified.
BUILD SUCCESSFUL in 5m 1s
2,164 JUnit tests: 0 failures, 110 skipped
```

### 2. Candidate application readiness and homepage request

```text
Mongo client connected to isolated MongoDB at 127.0.0.1:64004 using database/user source test.
Candidate process exit code: 1
Root cause: Migration 015-require-domain-collection-schema failed because its required verified TARGET_ACTIVE cutover ledger is absent from a fresh test database.
HTTP readiness/homepage requests: not sent; the application did not finish startup.
```

## Evidence
- PyYAML parsed the workflow and verified a single `windows-latest` job with the retained Windows checks and failure artifact upload.
- Focused `GitHubAutomationConfigurationTest` passed all 10 tests.
- Full ` .\gradlew.bat build` passed, including JavaScript checks, Java tests and the Windows PowerShell suite; test-result XMLs report 2,164 tests, 0 failures and 110 skips.
- Application logs confirmed the temporary authenticated `test` database and the intentional failure at migration 015. `DomainCollectionCutoverLedger` requires a valid target-active record, which a fresh empty database does not have.
- Candidate app and MongoDB processes stopped. The production MongoDB listener remained untouched.

## Bugs / Follow-ups
This blocked report is superseded by the [completed 2026-10-05 report](../test-reports/2026-10-05-06-49-christopherbell-dev-windows-only-website-ci.md).

## Document Status
superseded

## Project
christopherbell-dev
