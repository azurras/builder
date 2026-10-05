# Name Music Search Text by Its Role: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit; draft PR #1477 is explicitly excluded. [Implementation plan](../implementation-plans/2026-10-05-01-53-christopherbell-dev-name-music-search-text-by-its-role.md).

## Branch
`codex/music-search-text-name-20261005` at `3b7c064`

## Pass / Fail

> [!CAUTION]
> **2 of 3 checks passed** on candidate `3b7c064`; local application readiness is blocked by the test database's incomplete durable migration record.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Catalog search parameter contract | ✅ PASS | Focused `MusicReadControllerTest` passed (4 tests), including explicit public `q` binding and existing query-value forwarding. |
| 2 | Full project checks and package | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` completed successfully. |
| 3 | Packaged candidate startup and catalog route | ⏸️ BLOCKED | Candidate reached Tomcat initialization on port 8081, then startup stopped at migration 015 before readiness; no HTTP route could be exercised. |

## Test Cases
1. **Catalog search parameter contract:** Verified the controller binds the old `q` key and forwards its value into the `MusicQuery`.
2. **Full project checks and package:** Ran website and library checks and produced the bootable JAR.
3. **Packaged candidate startup and catalog route:** Attempted startup with the isolated test database and side-effecting features disabled; attempted no route after startup failed before readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Spring Boot website |
| Candidate | `3b7c064748a30ff8f60bd2f40953c5d19b80be1d` |
| Runtime | Java 25.0.3, `test` profile, packaged `website.jar` |
| Database | `mongodb://127.0.0.1:27018/test`; read-only preflight returned `database=test` |
| Port / URL | 8081 / `http://127.0.0.1:8081`; port was free before launch |
| Environment | `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\\Temp\\site-audit-jdk` |
| Artifact | `website/build/libs/website.jar`, SHA-256 `324CD6614F34C2446D89C25279C4A5234015FB94216AAA8E6E60EAE9E2AD709D` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Working directory:** `A:\\Projects\\christopherbell.dev-worktrees\\music-search-text-name-20261005`
- **Candidate identity:** branch `codex/music-search-text-name-20261005`, commit `3b7c064748a30ff8f60bd2f40953c5d19b80be1d`.
- **Process details:** Java process PID 44888 exited with code 1 after the migration exception; no listener remained on port 8081.
- **Logs:** Captured directly from the local command output; no persistent log file was configured.
- **Cleanup:** Process exited during failed startup; port 8081 was confirmed released. No database mutation was performed.

## Data Sent

### 1. Catalog search parameter contract

```text
Gradle focused test: :website:test --tests dev.christopherbell.music.web.MusicReadControllerTest
Input contract: catalog request parameter q; expected controller value name searchText and unchanged MusicQuery forwarding.
```

### 2. Full project checks and package

```text
Gradle: :website:check :cbell-lib:check :website:bootJar --no-daemon --max-workers=1 --console=plain
```

### 3. Packaged candidate startup and catalog route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
```

## Response Received

### 1. Catalog search parameter contract

```text
BUILD SUCCESSFUL; MusicReadControllerTest: 4 tests passed.
```

### 2. Full project checks and package

```text
BUILD SUCCESSFUL in 4m 35s
24 actionable tasks: 17 executed, 7 up-to-date
```

### 3. Packaged candidate startup and catalog route

```text
Tomcat initialized with port 8081 (http)
ApplicationContext startup failed before readiness.
Caused by: java.lang.IllegalStateException: Migration 015-require-domain-collection-schema has an incomplete durable record.
Process exit code: 1
No HTTP response: the application did not become ready.
Port 8081 after exit: free.
```

## Evidence
- Full Gradle gate exited successfully on 2026-10-05 local time; candidate JAR SHA-256 recorded above.
- Runtime attempt used Java 25.0.3 with the `test` profile, and read-only Mongo preflight confirmed database name `test`.
- Startup error was `Migration 015-require-domain-collection-schema has an incomplete durable record`; startup did not become ready, so route behavior remains unverified.
- `git diff --check` passed before commit. Only the controller and its focused test were committed; unrelated `gradlew.bat` worktree modification was left untouched.

## Bugs / Follow-ups
Runtime proof is blocked until the test database migration record is repaired through an authorized, supported recovery path. No PR was opened. Route behavior and runtime-ready application behavior remain unverified.

## Document Status
blocked

## Project
christopherbell-dev
