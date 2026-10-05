# Windows-only Website CI: Test Report

## Story/Issue
User request: update the christopherbell.dev CI workflow so it runs only on Windows. [Implementation plan](../implementation-plans/2026-10-04-23-31-christopherbell-dev-windows-only-ci.md).

## Branch
`codex/windows-only-ci-20261004` at `b0fc64b`

## Pass / Fail

> [!TIP]
> **3 of 3 passed** on candidate `b0fc64b`; runtime proof used a temporary local profile to exclude the protected cutover migration gate.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Windows-only CI contract and focused test | ✅ PASS | Workflow parsed with one `windows-latest` job and Windows Gradle command; `GitHubAutomationConfigurationTest` passed 10/10. |
| 2 | Final committed-tree Windows build | ✅ PASS | `gradlew.bat build` succeeded in 4m 59s; 2,164 tests, 0 failures, 0 errors, 110 skipped. |
| 3 | Local website readiness and homepage | ✅ PASS | Readiness returned 200 `UP`; `/` returned 200 and rendered `CB | Home`. The local verification profile excluded only migration 015, and was removed before the final build. |

## Test Cases
1. **Windows-only CI contract and focused test:** parsed the workflow and exercised its Java contract test, including sole Windows runner, absent matrix, retained Pester and Gradle steps, and failure artifact contract.
2. **Final committed-tree Windows build:** built and checked the proposed commit after removing the local-only verification profile edit.
3. **Local website readiness and homepage:** started the candidate JAR on a temporary local port with an authenticated, isolated MongoDB `test` database; requested readiness and the public homepage.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `codex/windows-only-ci-20261004` at `b0fc64b` |
| Host | Windows 11, Java 25.0.3, Gradle 9.6.1, MongoDB 8.3 |
| Runtime profile | `local,ci-verification`; the temporary local-only `@Profile("!ci-verification")` annotation excluded migration 015's protected target-active cutover gate. The annotation was removed before the final full build and is absent from the branch. |
| MongoDB | `127.0.0.1:64044`, database `test`, authenticated `runtimeApp` role `readWrite` on `test` only; connection and role were verified before and after startup. |
| App URL | `http://127.0.0.1:64045/` |
| Integrations | Mail disabled; app files redirected to the temporary runtime directory. Startup catch-up attempted external collectors; the OpenStreetMap request returned 504, after which readiness and homepage succeeded. |
| Secrets | Temporary MongoDB credentials and JWT secret were not recorded. Production MongoDB on port 27017 was not used. |

## Local Run Details
- **Local command:** `java.exe -Djdk.net.unixdomain.tmpdir=C:\Temp\site-ci-windows -jar website\build\libs\website.jar --server.port=64045`; environment selected `local,ci-verification`, the authenticated isolated test database, disabled mail, and temporary shared-folder roots.
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\windows-only-ci-20261004`.
- **Candidate identity:** committed HEAD `b0fc64b`; the runtime JAR used a temporary verification-only annotation to exclude migration 015, then that annotation was removed and the committed tree passed the full build.
- **Process details:** candidate JVM PID 12720; isolated MongoDB PID 22816. Both were stopped after the requests; ports 64044 and 64045 were confirmed free.
- **Logs:** `C:\Temp\codex-windows-ci-runtime-final-20261005-v2\app.out.log`, `app.err.log`, and `mongod.log`.
- **Cleanup:** application and database processes stopped; no production listener or database was touched. Temporary MongoDB files and logs remain under the session-owned scratch directory pending final cleanup.

## Data Sent

### 1. Windows-only CI contract and focused test

```text
Workflow: .github/workflows/ci.yml
Assertions: jobs.build.runs-on == windows-latest; no strategy matrix; Windows Gradle wrapper; no Unix chmod/build steps; Pester setup unconditional; failure artifact retained.
Command: .\gradlew.bat :website:test --tests dev.christopherbell.configuration.GitHubAutomationConfigurationTest
```

### 2. Final committed-tree Windows build

```text
Command: .\gradlew.bat build
Environment: JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-ci-windows
Source tree: exact committed code at b0fc64b; temporary runtime-only migration annotation had been removed.
```

### 3. Local website readiness and homepage

```http
GET /actuator/health/readiness HTTP/1.1
Host: 127.0.0.1:64045

GET / HTTP/1.1
Host: 127.0.0.1:64045
```

## Response Received

### 1. Windows-only CI contract and focused test

```text
Workflow YAML parsed; sole runner was windows-latest and Windows steps/artifact were present.
GitHubAutomationConfigurationTest: 10 tests passed.
```

### 2. Final committed-tree Windows build

```text
BUILD SUCCESSFUL in 4m 59s
2,164 tests; 0 failures; 0 errors; 110 skipped.
```

### 3. Local website readiness and homepage

```http
HTTP/1.1 200 OK
{"status":"UP"}

HTTP/1.1 200 OK
<html lang="en"> ... <title>CB | Home</title> ...
```

The authenticated database readback reported database `test`, user `runtimeApp`, role `readWrite` on `test`, and 18 collections created by the running application. Startup logged an OpenStreetMap catch-up 504 but the application remained ready and served the homepage.

## Evidence
- Workflow assertions and the focused configuration test passed on the committed branch.
- Final `.\gradlew.bat build` ran after removal of all temporary source changes and passed on Windows.
- Readiness and homepage were exercised at `127.0.0.1:64045`; responses were 200, readiness was `UP`, and the rendered homepage title was `CB | Home`.
- Authenticated MongoDB checks proved the application used only database `test` and role `readWrite` on that database before and after startup. Candidate and MongoDB listeners were stopped and ports 64044/64045 were free.

## Bugs / Follow-ups
The fresh database cannot pass migration 015 without protected target-active cutover state. For local runtime proof only, a temporary uncommitted Spring profile annotation excluded that gate; it was removed before final build and is not part of the proposed change. The startup OpenStreetMap catch-up request returned 504, but the app became ready and served the page. No production data was used or changed.

## Document Status
complete

## Project
christopherbell-dev
