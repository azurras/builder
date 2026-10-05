# Name Browser Feed Values by Their Roles: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-01-20-christopherbell-dev-name-browser-feed-values-by-their-roles.md).

## Branch
`codex/browser-feed-role-names-20261005` at `b25cf6c8`

## Pass / Fail

> [!CAUTION]
> **3 native checks passed; candidate runtime is blocked** on `b25cf6c8` before application readiness by Mongo migration 015.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Touched JavaScript syntax | ✅ PASS | `node --check` passed for all four changed modules. |
| 2 | Browser JavaScript suite | ✅ PASS | `:website:jsTest` passed all 380 tests. |
| 3 | Full packaged application build | ✅ PASS | `:website:bootJar` completed and produced the candidate JAR. |
| 4 | Packaged candidate startup and home route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; no HTTP request could be sent. |

## Test Cases
1. **Touched JavaScript syntax:** parses every edited browser module.
2. **Browser JavaScript suite:** runs the website's full native JS test suite.
3. **Full packaged application build:** packages the committed candidate.
4. **Packaged candidate startup and home route:** starts the candidate against isolated MongoDB database `test`; requests `/` on port 8081 only if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `b25cf6c82af97dbb5f84a1c49ac20edca525c44e`; JAR SHA-256 `D848EE42D2297AF1873A30A830505FE74A9DEFAD8D17C114473AA1F168DFEEFC` |
| Runtime | Java 25; Spring profile `test`; mail, scheduling, command center, federation and shared-folder integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before and after launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`.
- **Working directory:** Repository root of the isolated candidate worktree.
- **Candidate process:** Foreground Java process exited with code 1 during migration initialization.
- **Logs:** `%TEMP%\chris-style-browser-feed-b25cf6c8.log`.
- **Cleanup:** Candidate exited; port 8081 was free afterward. Isolated MongoDB listener on port 27018 remained running. No database records were directly modified.

## Data Sent

### 1. Touched JavaScript syntax

```text
node --check website/src/main/resources/static/js/post.js
node --check website/src/main/resources/static/js/user-feed.js
node --check website/src/main/resources/static/js/profile.js
node --check website/src/main/resources/static/js/lib/feed-render.js
```

### 2. Browser JavaScript suite

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat :website:jsTest --no-daemon --max-workers=1 --console=plain
```

### 3. Full packaged application build

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat :website:bootJar --no-daemon --max-workers=1 --console=plain
```

### 4. Packaged candidate startup and home route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
GET http://127.0.0.1:8081/
```

## Response Received

### 1. Touched JavaScript syntax

```text
All four node --check commands passed.
git diff --check passed.
```

### 2. Browser JavaScript suite

```text
BUILD SUCCESSFUL
380 tests passed, 0 failed
```

### 3. Full packaged application build

```text
BUILD SUCCESSFUL in 16s
:website:bootJar completed; 8 actionable tasks executed.
```

### 4. Packaged candidate startup and home route

```text
MongoDB read-only check: db.getName() = test
Candidate exit code: 1
Startup: Application run failed
Cause: Migration 015-require-domain-collection-schema has an incomplete durable record.
HTTP GET /: not reached; port 8081 never became ready
Post-run listener check: port 8081 free
```

## Evidence
- Candidate commit `b25cf6c82af97dbb5f84a1c49ac20edca525c44e` contains only the four planned JavaScript modules.
- All four JavaScript syntax checks, the 380-test browser suite, `:website:bootJar`, and `git diff --check` passed.
- Packaged startup log records migration 015 failure before readiness. MongoDB inspection was read-only and confirmed database `test`; no route response was available.

## Bugs / Follow-ups
A supported fixture/provisioning or recovery procedure is required before runtime proof and PR creation. Do not repair migration state through direct Mongo writes or bypass the startup guard. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
