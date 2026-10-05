# Chris Street Style Audit Aggregate: Test Report

## Story/Issue
Record the final combined candidate checks for the user's repository-wide `christopherbell.dev` Chris Street Style audit. See the [living implementation plan](../implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md). The obsolete draft PR #1477 was not used.

## Branch
`codex/chris-street-style-audit-20261005` at `dc928832`

## Pass / Fail

> [!CAUTION]
> **1 of 2 verification cases passed** on candidate `dc928832`; local application runtime is blocked by unavailable isolated MongoDB `test`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Combined native checks and packaged build | ✅ PASS | Website and shared library checks passed; 2,186 Java tests, 0 failures, 0 errors, 110 skipped; PowerShell checks passed; browser checks passed; `website.jar` built. |
| 2 | Isolated test database identity preflight | ⏸️ BLOCKED | Read-only check for `test` on `127.0.0.1:27018` returned `ECONNREFUSED`; candidate startup was not attempted. |

## Test Cases
1. **Combined native checks and packaged build:** run the website and shared-library checks, including JavaScript and PowerShell tasks, and package the committed candidate.
2. **Isolated test database identity preflight:** confirm that the isolated MongoDB `test` endpoint is available before starting the candidate application.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` Spring Boot website |
| Candidate | Commit `dc928832d39c1e019483c9aca668e63ba333463d` |
| Runtime | Java 25; Gradle Wrapper 9.6.1; Windows PowerShell |
| Profile | `test` for the requested isolated database check |
| Database | MongoDB `test` at `127.0.0.1:27018`; connection refused |
| Artifact | `website/build/libs/website.jar`; SHA-256 `8664BAFD1C92BCF946271C039EE18B36E81E388DA9D65BB1C070CB720CDF7636` |

## Local Run Details
- **Local command:** `New-Item -ItemType Directory -Force -Path C:\tmp\gradle-sock-chris; $env:JAVA_TOOL_OPTIONS='-Djdk.net.unixdomain.tmpdir=C:\tmp\gradle-sock-chris'; .\gradlew.bat :website:check :cbell-lib:check :website:bootJar`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\chris-street-style-audit-20261005`.
- **Candidate identity:** `dc928832d39c1e019483c9aca668e63ba333463d`, committed on `codex/chris-street-style-audit-20261005`.
- **Logs:** Gradle console; Java XML test results under `website/build/test-results/test` and `cbell-lib/build/test-results/test`.
- **Application startup:** Not attempted after database identity preflight failed. The startup migration preflight requires the genuine active domain-collection cutover ledger; no marker was fabricated and no migration was run.
- **Cleanup:** No application or MongoDB process was started; no database data was read or written beyond the failed connection attempt.

## Data Sent

### 1. Combined native checks and packaged build

```text
New-Item -ItemType Directory -Force -Path C:\tmp\gradle-sock-chris
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\tmp\gradle-sock-chris
.\gradlew.bat :website:check :cbell-lib:check :website:bootJar
```

### 2. Isolated test database identity preflight

```text
mongosh --quiet --norc mongodb://127.0.0.1:27018/test --eval "db.getName()"
```

## Response Received

### 1. Combined native checks and packaged build

```text
BUILD SUCCESSFUL in 5m 31s
24 actionable tasks: 24 executed
Java XML totals: 2,186 tests; 0 failures; 0 errors; 110 skipped
PowerShell suites: 203 passed, 0 failed, 1 skipped; 76 passed, 0 failed, 0 skipped
Browser checks: passed
Packaged artifact: website/build/libs/website.jar
```

### 2. Isolated test database identity preflight

```text
Exit code: 1
MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27018
Application startup: not attempted
```

## Evidence
- Candidate `dc928832d39c1e019483c9aca668e63ba333463d` is a clean commit 24 commits above `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- `git diff --check` passed; worktree status was clean after the aggregate commit.
- Gradle completed `:website:check :cbell-lib:check :website:bootJar` successfully in 5m 31s.
- Java XML results aggregate to 2,186 tests, 0 failures, 0 errors and 110 skipped.
- The read-only MongoDB preflight returned `ECONNREFUSED`; `V015RequireDomainCollectionSchema` and `DomainCollectionStartupPreflight` require the genuine cutover state before startup.

## Bugs / Follow-ups
Local runtime proof and any spoke PR remain blocked until a supported isolated MongoDB `test` service with a valid genuine cutover state is available. Do not bypass V015 or create a synthetic ledger. PR #1477 remains excluded.

## Document Status
blocked

## Project
christopherbell-dev
