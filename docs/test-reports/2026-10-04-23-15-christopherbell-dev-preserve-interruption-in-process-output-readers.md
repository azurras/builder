# Preserve Interruption in Process Output Readers: Test Report

## Story/Issue
The Chris Street Style codebase audit requested in this task. Individual plan: [Preserve Interruption in Process Output Readers](../implementation-plans/2026-10-04-22-46-christopherbell-dev-preserve-interruption-in-process-output-readers.md).

## Branch
`codex/chris-street-style-codebase-20261004` at `d1d8b79c`

## Pass / Fail

> [!TIP]
> **4 of 4 passed** on candidate `d1d8b79c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Output-wait interruption propagation | ✅ PASS | Both helpers rethrow `InterruptedException` and cancel the reader task; both regressions failed on clean baseline because interruption was swallowed. |
| 2 | Output-wait failure fallbacks | ✅ PASS | Execution failure, timeout, and cancellation still produce empty truncated output in both readers. |
| 3 | Website and library native checks | ✅ PASS | Full checks succeeded; 2,041 Java tests had 0 failures/errors (110 opt-in skips), Pester reported 203 passed/1 skipped and 75 passed, and JavaScript was up to date. |
| 4 | Packaged application runtime | ✅ PASS | Isolated candidate readiness and home-page requests returned 200; app used only the copied MongoDB fixture and isolated web port. |

## Test Cases
1. **Output-wait interruption propagation:** Interrupt the calling thread before awaiting a pending `FutureTask`; both helpers throw `InterruptedException` and cancel the reader.
2. **Output-wait failure fallbacks:** Exercise exceptional, timed-out, and cancelled `FutureTask` outcomes; each helper returns empty text with `truncated=true`.
3. **Website and library native checks:** Run focused regressions and Gradle `check` tasks, including Java, JavaScript, and PowerShell/Pester checks.
4. **Packaged application runtime:** Start the committed website jar in the test profile, request readiness and the home page, and stop the exact candidate process tree.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev website |
| Runtime | Java 25.0.3, Spring Boot 4.1.1, `test` profile, port 8081 |
| Database | Isolated copied database `cbell_candidate_76681a5ca5ab_d3f08074f6e54200aa366ad5` on temporary MongoDB 127.0.0.1:27018; startup log confirmed the connection |
| Disabled effects | Scheduling, command-center sampling, mail, federation discovery/inbound/outbound, and shared-folder feature |
| Artifact | `website/build/libs/website.jar`, SHA-256 `1056CBB978565D771E2B8D52710762AB0C24DEAD9C80E96D97021E6BFE438829` |

## Local Run Details
- **Local command:** `java -jar website/build/libs/website.jar --server.port=8081 --app.scheduling.enabled=false --command-center.enabled=false --app.federation.discovery-enabled=false --app.federation.inbound-enabled=false --app.federation.outbound-enabled=false --app.shared-folder.enabled=false`
- **Environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:27018/cbell_candidate_76681a5ca5ab_d3f08074f6e54200aa366ad5`; `APP_MAIL_ENABLED=false`; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\tmp\jds`.
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\chris-street-style-codebase-20261004`.
- **Candidate process:** PID 47540; started 2026-10-04 23:10 local; Spring reported ready in 4.333 seconds.
- **Logs:** `%TEMP%\chris-style-interruption-d1d8b79\candidate.out.log` and `candidate.err.log`.
- **Cleanup:** Stopped candidate PID 47540 and child PID 43556 with `taskkill /PID 47540 /T /F`; verified PID 47540 was gone and port 8081 had no listener. The temporary MongoDB listener remained for this audit session. Production ports 8080 (PID 14252) and 27017 (PID 5236) were unchanged.

## Data Sent

### 1. Output-wait interruption propagation

```text
FutureTask: pending
Input: calling thread interrupted before awaitOutput(FutureTask)
```

### 2. Output-wait failure fallbacks

```text
FutureTask outcomes: ExecutionException, timeout, cancellation
Expected output: text="", truncated=true
```

### 3. Website and library native checks

```text
./gradlew.bat :website:test --tests '*JdkMusicProcessRunnerTest' --tests '*PowerShellCpuTemperatureProbeTest'
./gradlew.bat :website:check :cbell-lib:check
```

### 4. Packaged application runtime

```http
GET /actuator/health/readiness HTTP/1.1
Host: 127.0.0.1:8081

GET / HTTP/1.1
Host: 127.0.0.1:8081
```

## Response Received

### 1. Output-wait interruption propagation

```text
JdkMusicProcessRunnerTest > interruptionWhileCollectingOutputReachesTheProcessOwner() PASSED
PowerShellCpuTemperatureProbeTest > interruptionWhileCollectingOutputReachesTheProcessOwner() PASSED
```

### 2. Output-wait failure fallbacks

```text
JdkMusicProcessRunnerTest > outputWaitFailuresKeepReturningEmptyTruncatedOutput() PASSED
PowerShellCpuTemperatureProbeTest > outputWaitFailuresKeepReturningEmptyTruncatedOutput() PASSED
```

### 3. Website and library native checks

```text
BUILD SUCCESSFUL in 4m 7s
24 actionable tasks: 13 executed, 11 up-to-date
Java tests: 2,041; failures: 0; errors: 0; skipped: 110 opt-in MongoDB integration tests
Production.Install Pester: 203 passed, 0 failed, 1 skipped
SharedFolderWorker Pester: 75 passed, 0 failed
```

### 4. Packaged application runtime

```http
HTTP/1.1 200 OK
GET /actuator/health/readiness
{"status":"UP"}

HTTP/1.1 200 OK
GET /
Content-Type: text/html; charset=UTF-8
Bytes: 3981
SHA-256: 1B903B323E177E2074E856C33B16AA4F373CF5DF9C96433AC73BD810A862B508
```

## Evidence
- Focused regression output and complete Gradle gate observed on committed candidate `d1d8b79c`.
- Website JUnit XML summary: `website/build/test-results/test/`; Pester output showed both suites with no failures.
- Candidate startup log identified profile `test`, Mongo host `127.0.0.1:27018`, and Tomcat port 8081.
- Listener checks confirmed candidate PID 47540 on 8081 during requests, test Mongo PID 25328, production website PID 14252 and production Mongo PID 5236; cleanup confirmed 8081 was free.
- Candidate artifact hash recorded above; worktree was clean at `d1d8b79c` during runtime proof.

## Bugs / Follow-ups
None for this correction. Pull request, required CI, merge, and supported deployment readback remain pending in the delivery plan.

## Document Status
complete

## Project
christopherbell-dev
