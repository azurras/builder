# Treat only missing viewer identity as anonymous: Test Report

## Story/Issue
User-requested whole-codebase Chris Street Style audit correction. PR #1477 is explicitly excluded and was not used as source or evidence.

## Branch
`codex/only-anonymous-identity-as-absence-20261005` at `6f7aede`

## Pass / Fail

> [!CAUTION]
> **2 of 3 verification cases passed** on candidate `6f7aede`; local application startup is blocked because the isolated test database cannot be reached.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Anonymous identity and unexpected-failure characterization | ✅ PASS | Both focused suites passed before the edit; the new propagation regressions failed on baseline, then passed after narrowing the catches. |
| 2 | Full native check and package gate | ✅ PASS | Website and library checks plus bootJar completed successfully; 2,166 Java tests, 110 skipped, no failures or errors. |
| 3 | Committed application startup against isolated test database | ⏸️ BLOCKED | Read-only preflight to `127.0.0.1:27018/test` was refused; startup was not attempted. |

## Test Cases
1. **Anonymous identity and unexpected-failure characterization:** Ran `RestaurantServiceTest` and `PostServiceTest`; existing anonymous behavior remains and new `IllegalArgumentException` propagation assertions distinguish unexpected defects from missing authentication.
2. **Full native check and package gate:** Website, shared library, browser, PowerShell, and executable package checks ran against the committed candidate.
3. **Committed application startup:** Read-only preflight checked the isolated MongoDB `test` endpoint before attempting the packaged app; database identity could not be read, so launch was withheld.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot application |
| Candidate | Commit `6f7aede848af34d8ad0ac17149c4979e675e3462`; JAR SHA-256 `8B22946B853A9AA48A1D0E7BD2C2D6B3774818F3725C61B71A1CB5DDE2AC68E8` |
| Runtime | JDK 25; candidate package produced by full native gate |
| Database | Expected `mongodb://127.0.0.1:27018/test`; connection refused |
| Candidate HTTP port | Not selected; app was not launched after DB identity preflight failed |
| Candidate application process | None launched |

## Local Run Details
- **Local command:** `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\only-anonymous-identity-as-absence-20261005`
- **Candidate identity:** Committed `HEAD` `6f7aede`; JAR built by the full gate.
- **Process details:** Application startup was not attempted because database isolation could not be verified. No listener was present on port 27018; no database service was started or modified.
- **Logs:** No application logs; startup did not run.
- **Cleanup:** No candidate process was created. No database write was attempted.

## Data Sent

### 1. Anonymous identity and unexpected-failure characterization

```text
Gradle: :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --tests dev.christopherbell.post.PostServiceTest
Revisions: baseline 695a3ed; candidate 6f7aede
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

### 1. Anonymous identity and unexpected-failure characterization

```text
Baseline existing suites: BUILD SUCCESSFUL.
New regressions before implementation: 89 tests, 2 failures; both expected IllegalArgumentException propagation but observed swallowed failures.
Candidate 6f7aede: PostServiceTest 27 tests, RestaurantServiceTest 62 tests; 0 failures, 0 errors, 0 skips.
```

### 2. Full native check and package gate

```text
BUILD SUCCESSFUL in 4m 21s.
Java test results: 2,166 total; 110 skipped; 0 failures; 0 errors.
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
- Focused baseline command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --tests dev.christopherbell.post.PostServiceTest` — passed before the correction.
- New regression run before implementation — both new assertions failed because `IllegalArgumentException` was caught and converted to anonymous behavior.
- Candidate focused command: same command — PostService 27/27, RestaurantService 62/62 passed.
- Full gate command: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar` — `BUILD SUCCESSFUL`.
- Read-only DB check: `mongosh mongodb://127.0.0.1:27018/test --quiet --eval 'db.getName()'` — connection refused.
- Candidate JAR SHA-256: `8B22946B853A9AA48A1D0E7BD2C2D6B3774818F3725C61B71A1CB5DDE2AC68E8`.

## Bugs / Follow-ups
- Local runtime verification and PR publication remain blocked until a supported isolated test database endpoint is available and its identity can be verified. No database service was started, no direct database writes were attempted, and no PR was created.

## Document Status
blocked

## Project
christopherbell-dev
