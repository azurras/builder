# Preserve sessions during concurrent renewal: Test Report

## Story/Issue
User requested fixes for all nine November 3 security/concurrency findings. This report covers findings 3.

## Branch
`codex/fix-scan-20261103` at `406620306cf4e4a97e6c7240747b0a7f057a91f6`

## Pass / Fail
> [!TIP]
> **5 of 5 passed** on candidate `40662030`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness | ✅ PASS | Observed expected output on this candidate |
| 2 | Candidate identity | ✅ PASS | Observed expected output on this candidate |
| 3 | Native checks | ✅ PASS | Observed expected output on this candidate |
| 4 | Changed behavior | ✅ PASS | Observed expected output on this candidate |
| 5 | Owned resource cleanup | ✅ PASS | Observed expected output on this candidate |

## Test Cases
1. **Candidate readiness:** Observed actual candidate readiness evidence below.
2. **Candidate identity:** Observed actual candidate identity evidence below.
3. **Native checks:** Observed actual native checks evidence below.
4. **Changed behavior:** All 12 authenticated requests returned 200 after the renewal interval; no response cleared authentication cookies. Deterministic native tests exercise a lost activity CAS, deletion, expiry, credential and fingerprint rejection.
5. **Owned resource cleanup:** Observed actual owned resource cleanup evidence below.

## App / Environment
| Setting | Value |
|---|---|
| App | christopherbell.dev, Java 25, Spring Boot, Windows |
| Profile | Exactly test; fresh disposable MongoDB/test started by the repository helper |
| Base URL | http://127.0.0.1:50542 |
| Application Mongo target | mongodb://127.0.0.1:50541/test; fresh process, no production credentials |
| Native/consumer Mongo target | Separate disposable loopback process with exact database test; opened target printed in evidence |
| Isolation | Resolved test profile/URI before launch; helper read databaseName=test after readiness; application startup logged the same loopback Mongo listener and isolated test administrator bootstrap |

## Local Run Details
- **Local command:** `./ops/local/Start-Candidate.ps1 -StateFile $verificationScratch/candidate.json -WithTestAdministrator`
- **Working directory:** Isolated spoke checkout resolved from the Builder registry and Git, on the branch and commit above.
- **Candidate:** Built with `./ops/local/Invoke-Gradle.ps1 :website:bootJar`; actuator identity matched the full commit before exercising behavior.
- **Logs:** Captured in the owned verification scratch directory; relevant actual inputs and outputs are retained below. Paths in commands are represented by their resolved variable roles.
- **Cleanup:** Candidate/helper processes stopped with the repository helper; both listener ports were verified free. Separate contract/consumer mongod stopped only after checking its recorded identity and owned path. Credentials and cookie values were never included in reports.

## Data Sent
### 1. Candidate readiness

```text
GET http://127.0.0.1:50542/actuator/health/readiness
```

### 2. Candidate identity

```text
GET http://127.0.0.1:50542/actuator/info
```

### 3. Native checks

```text
pwsh -NoProfile -File C:/Temp/cbell-scan-fixes/run-native.ps1
```

### 4. Changed behavior

```text
Create the test administrator through the existing test-profile bootstrap, exchange login for an opaque browser cookie, wait 306 seconds after login, then send 12 parallel interactive GET /api/accounts/2025-09-03/me requests with Accept: application/json, text/html. Cookie value omitted.
```

### 5. Owned resource cleanup

```text
pwsh -NoProfile -File C:/Temp/cbell-scan-fixes/cleanup.ps1
```

## Response Received
### 1. Candidate readiness

```text
HTTP 200 
X-Request-Id: 0e1b821a-3ce4-4586-b14b-8d847ae11903
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1793743778
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/vnd.spring-boot.actuator.v3+json
Transfer-Encoding: chunked
Date: Tue, 03 Nov 2026 22:08:38 GMT
Connection: close

{"status":"UP"}
```

### 2. Candidate identity

```text
HTTP 200 
X-Request-Id: 3a2b2f96-50d8-4e0e-9077-b80cb53adb3e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1793743778
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/vnd.spring-boot.actuator.v3+json
Content-Length: 176
Date: Tue, 03 Nov 2026 22:08:38 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-11-03T22:02:38.346Z","version":"0.0.0-dev.406620306cf4e4a97e6c7240747b0a7f057a91f6","group":"christopherbell.dev"}}
```

### 3. Native checks

```text
exit code: 0
--- stdout ---
> Task :cbell-lib:processTestResources UP-TO-DATE
> Task :cbell-lib:testClasses UP-TO-DATE
> Task :cbell-lib:checkstyleTest UP-TO-DATE
> Task :cbell-lib:checkstyleTestFixtures UP-TO-DATE
> Task :cbell-lib:test UP-TO-DATE
> Task :cbell-lib:check UP-TO-DATE

[Incubating] Problems report is available at: file:///A:/Projects/christopherbell.dev.worktrees/fix-scan-20261103/build/reports/problems/problems-report.html

Deprecated Gradle features were used in this build, making it incompatible with Gradle 10.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

For more on this, please refer to https://docs.gradle.org/9.6.1/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.

BUILD SUCCESSFUL in 5m 4s
30 actionable tasks: 16 executed, 14 up-to-date
Consider enabling configuration cache to speed up this build: https://docs.gradle.org/9.6.1/userguide/configuration_cache_enabling.html
Tests Passed: 189, Failed: 0, Skipped: 0, Inconclusive: 0, NotRun: 0
Tests Passed: 208, Failed: 0, Skipped: 1, Inconclusive: 0, NotRun: 0
Tests Passed: 208, Failed: 0, Skipped: 1, Inconclusive: 0, NotRun: 0
Tests Passed: 76, Failed: 0, Skipped: 0, Inconclusive: 0, NotRun: 0
website tests=2192 failures=0 skipped=18
cbell-lib tests=126 failures=0 skipped=0
```

### 4. Changed behavior

```text
COOKIE_LOGIN status=200; credential stored only in memory; idle interval starts
SESSION_IDLE waiting_seconds=304
SESSION_CONCURRENT after306s statuses=[200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200] authentication_cookie_clears=0
RUNTIME_BACKEND_PASS
```

### 5. Owned resource cleanup

```text
exit code: 0
--- stdout ---
port 50542 listeners: 0
port 50541 listeners: 0
removed $ownedCandidateMongoDirectory
removed $ownedJavaSocketDirectory
native Mongo port 52548 listeners: 0
removed owned native Mongo directory; isolated records and processes cleaned
```

## Evidence
- Captured as executed with Builder write-test-report record_run.py; runtime start 2026-11-03T16:08:08-06:00; native start 2026-11-03T16:02:20-06:00.
- Candidate source was committed and clean before final execution; no PR was created before these checks and cleanup completed.
- Independent review covered the selected controls and interleavings; the postcommit rollback correction was reviewed separately and its real-Mongo regression was observed red then green.
- All 12 authenticated requests returned 200 after the renewal interval; no response cleared authentication cookies. Deterministic native tests exercise a lost activity CAS, deletion, expiry, credential and fingerprint rejection.

## Bugs / Follow-ups
None for the selected finding.
Earlier candidates were superseded by `40662030` to correct postcommit read-failure rollback and preserve Ant route-rule compatibility. One earlier recording attempt hit the recorder's 300-second limit; another session attempt was invalidated when a concurrent build replaced the running application's jar. Final native checks completed before startup, with no build during runtime verification, and used explicit bounded timeouts of 900 seconds for native checks and 420 seconds for the session run. Those incomplete attempts are not counted as passes here.

## Document Status
complete

## Project
christopherbell-dev
