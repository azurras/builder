# Clarify FFprobe metadata parsing names: Test Report

## Story/Issue
User-requested whole-codebase Chris Street Style audit. PR #1477 is explicitly excluded and was not used as source or evidence.

## Branch
`codex/clarify-ffprobe-metadata-names-20261005` at `fc33aad`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed** on candidate `fc33aad`; packaged application startup is blocked because the isolated test database cannot be reached.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | FFprobe characterization before and after naming correction | ✅ PASS | The focused suite passed 2/2 tests on baseline and candidate. |
| 2 | Full native check and package gate | ✅ PASS | Website and library checks plus bootJar completed successfully; 2,164 Java tests, 110 skipped, no failures or errors. |
| 3 | Committed application startup against isolated test database | ⏸️ BLOCKED | Read-only database identity preflight to `127.0.0.1:27018/test` was refused; startup was not attempted. |

## Test Cases
1. **FFprobe characterization:** The current focused suite exercises FFprobe process outcomes and metadata parsing on baseline and candidate.
2. **Full native check and package gate:** Website, shared library, browser, PowerShell, and executable package checks ran on the committed candidate.
3. **Committed application startup:** Read-only preflight checked the configured isolated MongoDB `test` endpoint before attempting the packaged app; DB identity was unavailable, so launch was withheld.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot application |
| Candidate | Commit `fc33aad80fdabcded3215e74c1231322f2579b3f`; JAR SHA-256 `CFA4F5956EB2851E45EE03FF8E690CE74253DBEF4F160B11397D6E90981CA874` |
| Runtime | JDK 25; candidate package produced by full native gate |
| Database | Expected `mongodb://127.0.0.1:27018/test`; connection refused |
| Candidate HTTP port | Not selected; app was not launched after DB identity preflight failed |
| Candidate application process | None launched |

## Local Run Details
- **Local command:** `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\clarify-ffprobe-metadata-names-20261005`
- **Candidate identity:** Committed `HEAD` `fc33aad`; JAR built by the full gate.
- **Process details:** Application startup was not attempted because database isolation could not be verified. Read-only inspection found no listener on port 27018; no database service was started or modified.
- **Logs:** No application logs; startup did not run.
- **Cleanup:** No candidate process was created. No database write was attempted.

## Data Sent

### 1. FFprobe characterization

```text
Gradle: :website:test --tests dev.christopherbell.music.catalog.FfprobeMusicProbeTest
Revisions: origin/main baseline 695a3ed; candidate fc33aad
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

### 1. FFprobe characterization

```text
Baseline 695a3ed: 2 tests, 0 failures, 0 errors, 0 skipped.
Candidate fc33aad: 2 tests, 0 failures, 0 errors, 0 skipped.
```

### 2. Full native check and package gate

```text
BUILD SUCCESSFUL in 4m 27s.
Java test results: 2,164 total; 110 skipped; 0 failures; 0 errors.
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
- Candidate focused command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:test --tests dev.christopherbell.music.catalog.FfprobeMusicProbeTest` — 2/2 passed.
- Full gate command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar` — `BUILD SUCCESSFUL`.
- Read-only DB check: `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'` — connection refused.
- Candidate JAR SHA-256: `CFA4F5956EB2851E45EE03FF8E690CE74253DBEF4F160B11397D6E90981CA874`.

## Bugs / Follow-ups
- Local runtime verification and PR publication remain blocked until a supported isolated test database endpoint is available and its identity can be verified. No database service was started, no direct database writes were attempted, and no PR was created.

## Document Status
blocked

## Project
christopherbell-dev
