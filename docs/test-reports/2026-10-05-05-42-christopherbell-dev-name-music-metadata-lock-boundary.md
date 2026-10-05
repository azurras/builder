# Name Music Metadata Lock Boundary: Test Report

## Story/Issue
Continue the authorized `christopherbell.dev` Chris Street Style audit with a separate report for the Music metadata lock helper correction. See the [implementation plan](../implementation-plans/2026-10-05-05-33-christopherbell-dev-name-music-metadata-lock-boundary.md). Draft PR #1477 was not used.

## Branch
`codex/preserve-command-action-failure-cause-20261005` at `26cf68d`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed** on candidate `26cf68d`; packaged runtime verification is blocked by unavailable isolated MongoDB `test`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Focused Music metadata characterization | ✅ PASS | `MusicMetadataServiceTest` passed all 6 tests on baseline `453b3c5` and candidate `26cf68d`. |
| 2 | Full native checks and packaged build | ✅ PASS | Website/library checks passed; 2,165 Java tests, 0 failures, 0 errors, 110 skipped; browser and PowerShell tasks passed; `website.jar` built. |
| 3 | Candidate packaged application runtime | ⏸️ BLOCKED | Read-only MongoDB database identity check for isolated `test` on port 27018 returned `ECONNREFUSED`; app startup was not attempted. |

## Test Cases
1. **Focused Music metadata characterization:** Exercise edit, undo, stale revision, rewrite validation, and cleanup behavior before and after the helper contract change.
2. **Full native checks and packaged build:** Run browser, PowerShell, Java, library, and website checks and build the runnable candidate JAR.
3. **Candidate packaged application runtime:** Verify the isolated MongoDB database identity before starting the committed candidate; stop if the database is unavailable.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot website |
| Candidate | `26cf68d16b011aafd70d3c0e84e43dfc24dfd9aa` |
| Runtime | Java 25; Gradle Wrapper 9.6.1; Windows PowerShell |
| Database | Isolated MongoDB `test`, `127.0.0.1:27018`; connection refused |
| Profile | `test` selected for candidate verification; no `.env` files or process-level Mongo overrides were present in this shell |
| Artifact | `website/build/libs/website.jar`; SHA-256 `4CBF8E16E78F4990D64183F6007F3BF30D9428564B515632E8DB3B9CA5F17A62` |

## Local Run Details
- **Local command:** `$env:JAVA_TOOL_OPTIONS='-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk'; .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\preserve-command-center-action-failure-cause-20261005`
- **Candidate identity:** Commit `26cf68d16b011aafd70d3c0e84e43dfc24dfd9aa` on `codex/preserve-command-action-failure-cause-20261005`.
- **Focused command:** `$env:JAVA_TOOL_OPTIONS='-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk'; .\gradlew.bat --no-parallel --max-workers=4 :website:test --tests dev.christopherbell.music.metadata.MusicMetadataServiceTest`
- **Logs:** Gradle console output; test XML under `website/build/test-results/test` and `cbell-lib/build/test-results/test`.
- **Cleanup:** No application or database process was started; no files or database records were changed by verification.

## Data Sent

### 1. Focused Music metadata characterization

```text
:website:test --tests dev.christopherbell.music.metadata.MusicMetadataServiceTest
```

### 2. Full native checks and packaged build

```text
:website:check :cbell-lib:check :website:bootJar
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
```

### 3. Candidate packaged application runtime

```text
mongosh --quiet --norc mongodb://127.0.0.1:27018/test --eval "db.getName()"
Expected identity: test
```

## Response Received

### 1. Focused Music metadata characterization

```text
Baseline 453b3c5: BUILD SUCCESSFUL; 6 tests passed.
Candidate 26cf68d: BUILD SUCCESSFUL; 6 tests passed.
```

### 2. Full native checks and packaged build

```text
BUILD SUCCESSFUL in 4m 15s
Java tests: 2,165; failures: 0; errors: 0; skipped: 110
PowerShell Pester: 203 passed, 0 failed, 1 skipped; 75 passed, 0 failed, 0 skipped
Website browser tests/checks: passed
Packaged artifact: website/build/libs/website.jar
```

### 3. Candidate packaged application runtime

```text
Exit code: 1
MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27018
App startup: not attempted
```

## Evidence
- Focused test XML: `website/build/test-results/test/TEST-dev.christopherbell.music.metadata.MusicMetadataServiceTest.xml`.
- Full Java test XML: `website/build/test-results/test` and `cbell-lib/build/test-results/test`; aggregated totals are 2,165 tests, 0 failures, 0 errors, 110 skipped.
- Full gate console ended with `BUILD SUCCESSFUL in 4m 15s`.
- Read-only `mongosh` test database identity preflight failed with `ECONNREFUSED`; no app process or port was opened.
- `git diff --check` passed before commit; candidate diff review contains only the planned helper contract/name change.

## Bugs / Follow-ups
Runtime proof remains blocked until the isolated MongoDB `test` service is available through a supported setup. Do not create or update a PR until candidate startup and a representative application flow pass. No direct database writes, service starts, production access, or PR #1477 activity occurred.

## Document Status
blocked

## Project
christopherbell-dev
