# Name Email Sanitizer Stages and Preserve Parse Causes: Test Report

## Story/Issue
User-requested Chris Street Style codebase audit. [Implementation plan](../implementation-plans/2026-10-05-00-46-christopherbell-dev-name-email-sanitizer-stages-and-preserve-parse-causes.md).

## Branch
`codex/email-sanitizer-causes-20261005` at `eb8e7bc`

## Pass / Fail

> [!CAUTION]
> **3 native checks passed; candidate runtime is blocked** on `eb8e7bc` before application readiness by Mongo migration 015.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Baseline sanitizer cause regressions | ✅ PASS | Both new cause assertions failed before implementation, detecting the dropped causes. |
| 2 | Focused EmailSanitizer suite | ✅ PASS | All 32 sanitizer cases passed, preserving accepted outputs and safe validation messages. |
| 3 | Full module checks | ✅ PASS | `:website:check :cbell-lib:check` completed successfully, including JavaScript and PowerShell checks. |
| 4 | Packaged candidate startup and home route | ⏸️ BLOCKED | Startup exited at migration 015 before readiness; no HTTP request could be sent. |

## Test Cases
1. **Baseline sanitizer cause regressions:** confirms malformed IPv6 and IDN translations do not retain their parser causes before the change.
2. **Focused EmailSanitizer suite:** checks normalization, valid wrapper/address examples, safe messages and low-level cause retention.
3. **Full module checks:** runs the website and shared library checks with the native project toolchain.
4. **Packaged candidate startup and home route:** starts the committed candidate against isolated database `test`; requests `/` on port 8081 only if startup reaches readiness.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` |
| Candidate | `eb8e7bc975bea0555598aca80aea80f66d8582d6`; JAR SHA-256 `44221E4DF12981BE2EC70C1CEBD0B48889BC5504B7F449C8CBCB01A0423AD45A` |
| Runtime | Java 25; Spring profile `test`; mail, scheduling, command center, federation and shared-folder integrations disabled |
| Database | `test` at `mongodb://127.0.0.1:27018/test`; read-only `db.getName()` returned `test` |
| App port | `8081`; free before and after launch |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/test`; `APP_MAIL_ENABLED=false`; Java loopback workaround configured using `JAVA_TOOL_OPTIONS` (local temporary directory omitted).
- **Working directory:** Repository root of the isolated spoke worktree at candidate `eb8e7bc`.
- **Candidate process:** Foreground Java process exited with code 1 during migration initialization.
- **Logs:** `%TEMP%\chris-style-email-sanitizer-eb8e7bc.log`.
- **Cleanup:** Candidate exited; port 8081 was free afterward. The isolated MongoDB listener on port 27018 remained running. No database records were directly modified.

## Data Sent

### 1. Baseline sanitizer cause regressions

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :cbell-lib:test --tests dev.christopherbell.libs.security.EmailSanitizerTest
```

### 2. Focused EmailSanitizer suite

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :cbell-lib:test --tests dev.christopherbell.libs.security.EmailSanitizerTest
```

### 3. Full module checks

```text
JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<short local temp directory>
.\gradlew.bat :website:check :cbell-lib:check
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

### 1. Baseline sanitizer cause regressions

```text
32 tests completed, 2 failed
The IPv6 cause assertion failed; the IDN cause assertion failed.
```

### 2. Focused EmailSanitizer suite

```text
BUILD SUCCESSFUL in 4s
32 tests passed, 0 failed
```

### 3. Full module checks

```text
BUILD SUCCESSFUL in 4m 36s
:website:check and :cbell-lib:check passed
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
- Candidate commit `eb8e7bc975bea0555598aca80aea80f66d8582d6` was built and its packaged JAR SHA-256 is recorded above.
- The focused baseline run produced two failures specifically at the new cause assertions; the candidate run passed all 32 cases.
- Full `:website:check :cbell-lib:check` passed after the implementation. `git diff --check` also passed.
- Runtime logs show the Mongo migration runner failed before application readiness. A read-only check confirmed database `test`; the route was therefore not exercised.

## Bugs / Follow-ups
A supported fixture/provisioning or recovery procedure is required before runtime proof and PR creation. Do not repair migration state through direct Mongo writes or bypass the startup guard. No PR was opened.

## Document Status
blocked

## Project
christopherbell-dev
