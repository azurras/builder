# Let Command Center Report Host Probe Defects: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-01-34-christopherbell-dev-let-command-center-report-host-probe-defects.md).

## Branch
`codex/host-probe-defect-reporting-20261005` at `5a2bece4`

## Pass / Fail

> [!CAUTION]
> **4 native checks passed; candidate runtime is blocked** on `5a2bece4` before application readiness by Mongo migration 015.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Baseline command-center metrics tests | ✅ PASS | 16 provider and collector tests passed before editing. |
| 2 | Runtime-defect regression | ✅ PASS | The new propagation test failed against the old catch, then passed after its removal. |
| 3 | Focused command-center metrics tests | ✅ PASS | 17 provider and collector tests passed; existing unavailable and collector-isolation cases remained green. |
| 4 | Full module checks and packaged build | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` succeeded; 2,165 website/library Java tests passed with 110 skips, 380 browser tests passed, and native PowerShell checks passed. |
| 5 | Packaged candidate startup and home route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; no HTTP request could be sent. |

## Test Cases
1. **Baseline command-center metrics tests:** verifies existing provider readings and collector isolation before editing.
2. **Runtime-defect regression:** verifies an unexpected exception from the probe is propagated rather than converted into ordinary unavailable readings.
3. **Focused command-center metrics tests:** checks expected unavailable states, defect propagation, collector isolation, stale values and alert behavior.
4. **Full module checks and packaged build:** runs the website and shared library native checks and packages the candidate.
5. **Packaged candidate startup and home route:** starts the candidate against isolated MongoDB database `test`; requests `/` on port 8081 only if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `5a2bece44e035cc42593cda3acfb626d942e1156`; JAR SHA-256 `80B0D568BE6FE61E55310FECEE44E22444F417771C20C1C308F3DA46087E6453` |
| Runtime | Java 25; Spring profile `test`; mail, scheduling, command center, federation and shared-folder integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before and after launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk`.
- **Working directory:** Repository root of isolated candidate worktree.
- **Candidate process:** Foreground Java process exited with code 1 during migration initialization.
- **Logs:** `%TEMP%\chris-style-host-probe-5a2bece4.log`.
- **Cleanup:** Candidate exited; port 8081 was free afterward. Isolated MongoDB listener on port 27018 remained running. No database records were directly modified.

## Data Sent

### 1. Baseline command-center metrics tests

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk
.\gradlew.bat :website:test --tests dev.christopherbell.admin.commandcenter.metrics.ApplicationHostMetricsProviderTest --tests dev.christopherbell.admin.commandcenter.metrics.CommandCenterMetricsServiceTest --no-daemon --max-workers=1 --console=plain
```

### 2. Runtime-defect regression

```text
Probe: () -> throw new IllegalStateException("Unexpected probe defect")
Expected before implementation: direct provider test fails because the exception is replaced with unavailable metric values.
Expected after implementation: the same IllegalStateException propagates with its message.
```

### 3. Focused command-center metrics tests

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

### 1. Baseline command-center metrics tests

```text
BUILD SUCCESSFUL in 30s
16 provider and collector tests passed, 0 failed
```

### 2. Runtime-defect regression

```text
Before implementation: 1 test failed as expected because the old catch suppressed the IllegalStateException.
After implementation: propagatesUnexpectedProbeDefects passed and preserved the exception message.
```

### 3. Focused command-center metrics tests

```text
BUILD SUCCESSFUL in 11s
17 provider and collector tests passed, 0 failed
Expected empty-optionals unavailable characterization passed.
Collector isolation, cause logging/redaction, stale-value, and alert tests passed.
```

### 4. Full module checks and packaged build

```text
BUILD SUCCESSFUL in 4m 40s
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
- Candidate commit `5a2bece44e035cc42593cda3acfb626d942e1156` contains only the provider and its focused test.
- The new test failed against the baseline catch and passed after the catch was removed.
- Focused provider/collector tests, full module checks, `:website:bootJar`, and `git diff --check` passed.
- Packaged startup log records migration 015 failure before readiness. MongoDB inspection was read-only and confirmed database `test`; no route response was available.

## Bugs / Follow-ups
A supported fixture/provisioning or recovery procedure is required before runtime proof and PR creation. Do not repair migration state through direct Mongo writes or bypass the startup guard. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
