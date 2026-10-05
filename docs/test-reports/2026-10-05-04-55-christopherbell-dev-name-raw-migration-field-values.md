# Name raw migration field values: Test Report

## Story/Issue
User-requested Chris Street Style audit correction; draft PR #1477 remains excluded and was not used as evidence.

## Branch
`codex/name-raw-migration-field-values-20261005` at `d86dd03`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed; local application startup is blocked** because the isolated MongoDB endpoint is unavailable.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | V014 migration characterization before and after naming correction | ✅ PASS | Baseline and candidate both passed all 29 migration tests with no failures, errors, or skips. |
| 2 | Full native check and package gate | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` completed successfully; 2,164 Java tests were reported, 110 skipped, with no failures or errors. |
| 3 | Committed application startup against isolated test database | ⏸️ BLOCKED | MongoDB at `127.0.0.1:27018` refused a read-only identity check, so startup was not attempted without verified isolated data. |

## Test Cases
1. **V014 migration characterization:** Verified strict accepted/rejected document behavior before and after renaming raw field locals to `rawFieldValue`; all 29 tests passed on each revision.
2. **Full native check and package gate:** Ran browser, Java, PowerShell, production checks, and executable package task.
3. **Committed application startup:** Selected free loopback port 60763 and attempted read-only identity verification against database `test`; verification failed and the app was not launched.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot application |
| Candidate | Commit `d86dd03`; JAR SHA-256 `CACFD52240164348463FF487DF317936B546CD7476D5AEA8B8202F7D2042669D` |
| Runtime | JDK 25; packaged candidate built by full gate |
| Database | Expected `mongodb://127.0.0.1:27018/test`; preflight returned connection refused |
| HTTP binding | Candidate port `127.0.0.1:60763`; no listener occupied it |
| Candidate application process | None launched |

## Local Run Details
- **Local command:** `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\name-raw-migration-field-values-20261005`
- **Candidate identity:** Committed `HEAD` `d86dd03`; JAR built by `:website:bootJar` in the full gate.
- **Process details:** Application startup was not attempted because database isolation could not be verified. Read-only inspection found a `mongod` process but no listener on port 27018; no database service was started or modified.
- **Logs:** No application logs; startup did not run.
- **Cleanup:** No candidate process was created. Port 60763 remained free. No database write was attempted.

## Data Sent

### 1. V014 migration characterization

```text
Gradle: :website:test --tests dev.christopherbell.configuration.mongo.migration.V014ConsolidateMusicRuntimeStateTest
```

### 2. Full native check and package gate

```text
Gradle: :website:check :cbell-lib:check :website:bootJar
Gradle options: --no-parallel --max-workers=4
```

### 3. Committed application startup

```text
mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'
Candidate loopback port: 127.0.0.1:60763
```

## Response Received

### 1. V014 migration characterization

```text
Base 695a3ed: 29 tests, 0 failures, 0 errors, 0 skipped.
Candidate d86dd03: 29 tests, 0 failures, 0 errors, 0 skipped.
```

### 2. Full native check and package gate

```text
BUILD SUCCESSFUL in 4m 20s
Java test results: 2,164 total; 110 skipped; 0 failures; 0 errors.
Browser, PowerShell, website checks, cbell-lib checks, and website bootJar tasks completed successfully.
```

### 3. Committed application startup

```text
MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27018
Read-only database identity: unavailable.
Listener check: no listener on 127.0.0.1:27018 or candidate port 60763.
Startup: not attempted because the effective database could not be verified as isolated test data.
```

## Evidence
- Baseline and candidate focused command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:test --tests dev.christopherbell.configuration.mongo.migration.V014ConsolidateMusicRuntimeStateTest` — 29/29 passed on each revision.
- Full gate command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar` — `BUILD SUCCESSFUL`.
- Read-only DB check: `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'` — connection refused.
- Candidate JAR SHA-256: `CACFD52240164348463FF487DF317936B546CD7476D5AEA8B8202F7D2042669D`.

## Bugs / Follow-ups
- Runtime verification and PR publication remain blocked until the supported isolated test database endpoint is available and its identity can be verified. No database service was started, no direct database writes were attempted, and no PR was created.

## Document Status
blocked

## Project
christopherbell-dev
