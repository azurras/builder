# Preserve command-center action failure cause: Test Report

## Story/Issue
User-requested whole-codebase Chris Street Style audit correction. PR #1477 is explicitly excluded and was not used as source or evidence.

## Branch
`codex/preserve-command-action-failure-cause-20261005` at `453b3c5`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed** on candidate `453b3c5`; local application startup is blocked because the isolated test database cannot be reached.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Command action failure characterization | ✅ PASS | Baseline action tests passed; the new cause-preservation and runtime-propagation expectations failed on broad catch behavior and pass on the candidate. |
| 2 | Full native check and package gate | ✅ PASS | Website and library checks plus bootJar completed successfully; 2,165 Java tests, 110 skipped, no failures or errors. |
| 3 | Committed application startup against isolated test database | ⏸️ BLOCKED | Read-only preflight to `127.0.0.1:27018/test` was refused; startup was not attempted. |

## Test Cases
1. **Command action failure characterization:** The existing I/O launch failure retains its safe `InvalidRequestException`, `launch-failed` path and pending-action rollback; the exception now retains the IOException cause. A separate runtime defect must propagate unchanged.
2. **Full native check and package gate:** Website, shared library, browser, PowerShell, and executable package checks ran against the committed candidate.
3. **Committed application startup:** Read-only preflight checked the isolated MongoDB `test` endpoint before attempting the packaged app; database identity could not be read, so launch was withheld.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot application |
| Candidate | Commit `453b3c5cda45c90dce4bf7242bdaa2fc8631c0b3`; JAR SHA-256 `3D507E38097990CCC76568D93005B315622C24FE218CB6B73A3CB4FAE5F0B5DE` |
| Runtime | JDK 25; candidate package produced by full native gate |
| Database | Expected `mongodb://127.0.0.1:27018/test`; connection refused |
| Candidate HTTP port | Not selected; app was not launched after DB identity preflight failed |
| Candidate application process | None launched |

## Local Run Details
- **Local command:** `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\preserve-command-center-action-failure-cause-20261005`
- **Candidate identity:** Committed `HEAD` `453b3c5`; JAR built by the full gate.
- **Process details:** Application startup was not attempted because database isolation could not be verified. No listener was present on port 27018; no database service was started or modified.
- **Logs:** No application logs; startup did not run.
- **Cleanup:** No candidate process was created. No database write was attempted.

## Data Sent

### 1. Command action failure characterization

```text
Gradle: :website:test --tests dev.christopherbell.admin.commandcenter.action.CommandCenterActionServiceTest
Revisions: baseline 695a3ed; candidate 453b3c5
```

### 2. Full native check and package gate

```text
Gradle: :website:check :cbell-lib:check :website:bootJar
Options: --no-parallel --max-workers=4
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
```

### 3. Committed application startup

```text
mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'
```

## Response Received

### 1. Command action failure characterization

```text
Baseline CommandCenterActionServiceTest: BUILD SUCCESSFUL.
Before implementation, 32 tests had 2 failures: the runtime defect was swallowed and the IOException cause was absent.
Candidate 453b3c5: 32 tests, 0 failures, 0 errors, 0 skipped.
```

### 2. Full native check and package gate

```text
BUILD SUCCESSFUL in 4m 20s.
Java test results: 2,165 total; 110 skipped; 0 failures; 0 errors.
Browser, PowerShell, website checks, cbell-lib checks, and website bootJar tasks completed successfully.
```

### 3. Committed application startup

```text
MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27018
Read-only database identity: unavailable.
Listener check: no listener on 127.0.0.1:27018.
Startup: not attempted because the effective database could not be verified as isolated test data.
```

## Evidence
- Baseline and candidate focused command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:test --tests dev.christopherbell.admin.commandcenter.action.CommandCenterActionServiceTest` — baseline suite passed; candidate 32/32 passed.
- New characterization assertions before implementation — 2 failures in 32 tests: broad catch hid the runtime defect and omitted the IOException cause.
- Full gate command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar` — `BUILD SUCCESSFUL`.
- Read-only DB check: `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'` — connection refused.
- Candidate JAR SHA-256: `3D507E38097990CCC76568D93005B315622C24FE218CB6B73A3CB4FAE5F0B5DE`.

## Bugs / Follow-ups
- Local runtime verification and PR publication remain blocked until a supported isolated test database endpoint is available and its identity can be verified. No database service was started, no direct database writes were attempted, and no PR was created.

## Document Status
blocked

## Project
christopherbell-dev
