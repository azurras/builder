# Narrow Command Center Release Metadata Failures: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-01-39-christopherbell-dev-narrow-command-center-release-metadata-failures.md).

## Branch
`codex/host-probe-release-metadata-20261005` at `ae96a270`

## Pass / Fail

> [!CAUTION]
> **4 native checks passed; candidate runtime is blocked** on `ae96a270` before application readiness by Mongo migration 015.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Baseline provider tests | ✅ PASS | Four existing `ApplicationHostMetricsProviderTest` cases passed before editing. |
| 2 | Malformed metadata characterization | ✅ PASS | New malformed JSON/non-regular path test passed against baseline and candidate, preserving intended empty metadata behavior. |
| 3 | Focused provider and collector tests | ✅ PASS | 17 provider/collector tests passed after narrowing the catch. |
| 4 | Full module checks and packaged build | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` succeeded; 2,165 Java tests passed with 110 skips, 380 JS tests passed, and PowerShell Pester passed with one elevation-dependent test skipped. |
| 5 | Packaged candidate startup and home route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; no HTTP request could be sent. |

## Test Cases
1. **Baseline provider tests:** verifies current release metadata and unavailable-metric behavior before editing.
2. **Malformed metadata characterization:** verifies malformed JSON and a non-regular path continue to return empty metadata.
3. **Focused provider and collector tests:** checks metadata parsing, host readings, defect boundaries and collector isolation.
4. **Full module checks and packaged build:** runs website/shared-library checks and packages the candidate.
5. **Packaged candidate startup and home route:** starts against isolated MongoDB database `test`; requests `/` on port 8081 only if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `ae96a270901cd2e2a306214abf5b387f5bf3b8d6`; JAR SHA-256 `02C6F0C002FA7C91957A4F605CAC3FA8E3FC4669BFA7395D848225A032B640` |
| Runtime | Java 25; Spring profile `test`; mail, scheduling, command center, federation and shared-folder integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before and after launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`.
- **Working directory:** Repository root of isolated candidate worktree.
- **Candidate process:** Foreground Java process exited with code 1 during migration initialization.
- **Logs:** `%TEMP%\chris-style-release-metadata-ae96a270.log`.
- **Cleanup:** Candidate exited; port 8081 was free afterward. Isolated MongoDB listener on port 27018 remained running. No database records were directly modified.

## Data Sent

### 1. Baseline provider tests

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.metrics.ApplicationHostMetricsProviderTest --console=plain --no-daemon --max-workers=1
```

### 2. Malformed metadata characterization

```text
Malformed JSON file content: {
Metadata path: a directory
Expected result for both: Optional.empty()
```

### 3. Focused provider and collector tests

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.metrics.ApplicationHostMetricsProviderTest --tests dev.christopherbell.admin.commandcenter.metrics.CommandCenterMetricsServiceTest --no-daemon --max-workers=1 --console=plain
```

### 4. Full module checks and packaged build

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat :website:check :cbell-lib:check :website:bootJar --no-daemon --max-workers=1 --console=plain
```

### 5. Packaged candidate startup and home route

```text
SPRING_PROFILES_ACTIVE=test
SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test
APP_MAIL_ENABLED=false
java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false
GET http://127.0.0.1:8081/
```

## Response Received

### 1. Baseline provider tests

```text
BUILD SUCCESSFUL in 27s
4 tests passed, 0 failed
```

### 2. Malformed metadata characterization

```text
Baseline: malformedOrNonRegularReleaseMetadataReturnsEmpty passed with the original broad catch.
Candidate: the same characterization passed with IOException | JacksonException.
```

### 3. Focused provider and collector tests

```text
BUILD SUCCESSFUL in 11s
17 provider/collector tests passed, 0 failed.
Malformed JSON, non-regular metadata, malformed SHA, valid SHA, expected unavailable readings, and collector isolation remained green.
```

### 4. Full module checks and packaged build

```text
BUILD SUCCESSFUL in 4m 41s
:website:check :cbell-lib:check :website:bootJar passed.
Website Java tests: 2,042 total, 0 failures/errors, 110 skipped.
Shared-library Java tests: 123 total, 0 failures/errors, 0 skipped.
Browser JavaScript tests: 380 passed, 0 failed.
Native PowerShell Pester checks passed; one elevation-dependent test was skipped.
```

### 5. Packaged candidate startup and home route

```text
MongoDB read-only check: db.getName() = test
Candidate exit code: 1
Startup: Application run failed
Cause: Migration 015-require-domain-collection-schema has an incomplete durable record.
HTTP GET /: not reached; port 8081 never became ready
Post-run listener check: port 8081 free
```

## Evidence
- Candidate `ae96a270901cd2e2a306214abf5b387f5bf3b8d6` contains only the metadata catch and its focused test.
- The new test confirms malformed JSON remains caught even though Jackson 3 parse failures are runtime exceptions; the exact catch is limited to `IOException | JacksonException`.
- Focused metrics tests, full module checks, `:website:bootJar`, and `git diff --check` passed.
- Packaged startup log records migration 015 failure before readiness. MongoDB inspection was read-only and confirmed database `test`; no route response was available.

## Bugs / Follow-ups
A supported fixture/provisioning or recovery procedure is required before runtime proof and PR creation. Do not repair migration state through direct Mongo writes or bypass the startup guard. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
