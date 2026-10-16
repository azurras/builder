# Patch vulnerable dependencies and throttle password reset mail: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-16-14-35-christopherbell-dev-patch-vulnerable-dependencies-and-throttle-password-reset-ma.md): the candidate runs patched Tomcat and Jackson, and a second reset request within five minutes keeps the first token without sending mail.

## Branch
`claude/patch-deps-throttle-reset-20261016` at candidate `9b418a8`

## Pass / Fail

> [!TIP]
> 7 of 7 cases passed on candidate `9b418a8`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate with a test administrator starts an isolated candidate on database test | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | The candidate runs the patched Tomcat 11.0.26 | ✅ PASS | Expected exit code 0 |
| 4 | The patched Jackson accepts valid JSON and rejects truncated JSON and an oversized number with 400 | ✅ PASS | Expected exit code 0 |
| 5 | A second reset request within the cooldown keeps the first token and expiry; responses stay generic for known and unknown emails | ✅ PASS | Expected exit code 0 |
| 6 | The candidate log shows one issued reset and one skipped within the cooldown, and no ERROR line | ✅ PASS | Expected exit code 0 |
| 7 | Stop-Candidate stops the candidate, frees both ports and removes its disposable root | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate with a test administrator starts an isolated candidate on database test**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016' -WithTestAdministrator | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) url=$($s.baseUrl)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:52575/actuator/health/readiness`
3. **The candidate runs the patched Tomcat 11.0.26**: command `pwsh -NoLogo -NoProfile -Command "$line = Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -Pattern 'Apache Tomcat/\d' | Select-Object -First 1; $line.Line; if ($line.Line -notmatch 'Apache Tomcat/11\.0\.26') { exit 1 }"`
4. **The patched Jackson accepts valid JSON and rejects truncated JSON and an oversized number with 400**: command `python -I C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\json_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json`
5. **A second reset request within the cooldown keeps the first token and expiry; responses stay generic for known and unknown emails**: command `python -I C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\reset_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json`
6. **The candidate log shows one issued reset and one skipped within the cooldown, and no ERROR line**: command `pwsh -NoLogo -NoProfile -Command "$issued = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -SimpleMatch 'Password reset requested for account id').Count; $skipped = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -SimpleMatch 'skipped; a link was sent within PT5M').Count; $errors = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"issued=$issued skipped=$skipped errorLines=$errors\"; if ($issued -ne 1 -or $skipped -ne 1 -or $errors) { exit 1 }"`
7. **Stop-Candidate stops the candidate, frees both ports and removes its disposable root**: command `pwsh -NoLogo -NoProfile -Command "$st = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\candidate-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($st.candidatePort, $st.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $st.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Mail | disabled (test profile default), so no email left the machine |
| Checks | :website:build with strict dependency verification passed on 9b418a8c (2,140 tests, 0 failed); bootJar rebuilt on 9b418a8c |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016' -WithTestAdministrator | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) url=$($s.baseUrl)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Local command:** `GET http://127.0.0.1:52575/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$line = Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -Pattern 'Apache Tomcat/\d' | Select-Object -First 1; $line.Line; if ($line.Line -notmatch 'Apache Tomcat/11\.0\.26') { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Local command:** `python -I C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\json_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Local command:** `python -I C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\reset_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$issued = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -SimpleMatch 'Password reset requested for account id').Count; $skipped = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -SimpleMatch 'skipped; a link was sent within PT5M').Count; $errors = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"issued=$issued skipped=$skipped errorLines=$errors\"; if ($issued -ne 1 -or $skipped -ne 1 -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$st = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\candidate-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($st.candidatePort, $st.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $st.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016`
- **Candidate identity:** `9b418a8`
- **Cleanup:** Stop-Candidate.ps1 stopped the candidate and mongod process trees; both ports had no listeners and the disposable root (database, logs and the generated test-administrator credentials) was removed. Production MongoDB on 27017 kept listening. The reset requests touched only the disposable `test` database, and mail was disabled.
- **Cleanup:** Stopped the candidate process tree; no fixtures remain.

## Data Sent

### 1. Start-Candidate with a test administrator starts an isolated candidate on database test

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016' -WithTestAdministrator | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) url=$($s.baseUrl)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:52575/actuator/health/readiness
```

### 3. The candidate runs the patched Tomcat 11.0.26

```text
pwsh -NoLogo -NoProfile -Command "$line = Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -Pattern 'Apache Tomcat/\d' | Select-Object -First 1; $line.Line; if ($line.Line -notmatch 'Apache Tomcat/11\.0\.26') { exit 1 }"
```

### 4. The patched Jackson accepts valid JSON and rejects truncated JSON and an oversized number with 400

```text
python -I C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\json_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json
```

### 5. A second reset request within the cooldown keeps the first token and expiry; responses stay generic for known and unknown emails

```text
python -I C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\reset_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json
```

### 6. The candidate log shows one issued reset and one skipped within the cooldown, and no ERROR line

```text
pwsh -NoLogo -NoProfile -Command "$issued = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -SimpleMatch 'Password reset requested for account id').Count; $skipped = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -SimpleMatch 'skipped; a link was sent within PT5M').Count; $errors = @(Select-String -LiteralPath 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-dbbcb1d2ddcc40f290cc4799fe6e4163\candidate.out.log' -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"issued=$issued skipped=$skipped errorLines=$errors\"; if ($issued -ne 1 -or $skipped -ne 1 -or $errors) { exit 1 }"
```

### 7. Stop-Candidate stops the candidate, frees both ports and removes its disposable root

```text
pwsh -NoLogo -NoProfile -Command "$st = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev-worktrees\patch-deps-throttle-reset-20261016\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\9d76249e-7ed8-4027-8e34-3a5bf4b35163\scratchpad\candidate-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($st.candidatePort, $st.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $st.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"
```

## Response Received

### 1. Start-Candidate with a test administrator starts an isolated candidate on database test

```text
exit code: 0
--- stdout ---
ready=True db=test url=http://127.0.0.1:52575
```

### 2. The candidate reports readiness UP

```text
HTTP 200 
X-Request-Id: 794ca4df-9a26-4304-8be6-58ea8ac3ee13
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792180359
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
Date: Fri, 16 Oct 2026 19:51:39 GMT
Connection: close

{"status":"UP"}
```

### 3. The candidate runs the patched Tomcat 11.0.26

```text
exit code: 0
--- stdout ---
2026-10-16T14:51:26.133-05:00  INFO 39592 --- [           main] [] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/11.0.26]
```

### 4. The patched Jackson accepts valid JSON and rejects truncated JSON and an oversized number with 400

```text
exit code: 0
--- stdout ---
valid JSON: 200 {"messages":null,"payload":"If an account exists for that email, a password reset link has been sent.","requestId":null,
truncated JSON: 400 {"messages":[{"code":"REQUEST_ERROR","description":"The request body is malformed or invalid."}],"payload":null,"requestId":null,"success":false}
5000-digit number for email: 400
PASS
```

### 5. A second reset request within the cooldown keeps the first token and expiry; responses stay generic for known and unknown emails

```text
exit code: 0
--- stdout ---
database=test
before: hash set=False
first request: 200 'If an account exists for that email, a password reset link has been sent.'; hash set=True expiresOn=2026-10-16T20:52:30.823Z
second request: 200 'If an account exists for that email, a password reset link has been sent.'; hash unchanged=True expiry unchanged=True
unknown email: 200 'If an account exists for that email, a password reset link has been sent.'
PASS
```

### 6. The candidate log shows one issued reset and one skipped within the cooldown, and no ERROR line

```text
exit code: 0
--- stdout ---
issued=1 skipped=1 errorLines=0
```

### 7. Stop-Candidate stops the candidate, frees both ports and removes its disposable root

```text
exit code: 0
--- stdout ---
listeners=0 rootRemoved=True productionMongoListening=True
```

## Evidence
- Case 1 started 2026-10-16T14:51:21-05:00, took 10016 ms, candidate `9b418a8`
- Case 2 started 2026-10-16T14:51:39-05:00, took 62 ms, candidate `9b418a8`
- Case 3 started 2026-10-16T14:51:39-05:00, took 297 ms, candidate `9b418a8`
- Case 4 started 2026-10-16T14:51:55-05:00, took 203 ms, candidate `9b418a8`
- Case 5 started 2026-10-16T14:52:30-05:00, took 1031 ms, candidate `9b418a8`
- Case 6 started 2026-10-16T14:52:31-05:00, took 297 ms, candidate `9b418a8`
- Case 7 started 2026-10-16T14:52:39-05:00, took 5467 ms, candidate `9b418a8`

## Bugs / Follow-ups
- **Harness errors, not candidate failures:** three earlier records were dropped from the evidence file and rerun. Two passed a garbled path because PowerShell's case-insensitive `$S` and `$s` collided, so the scripts never reached the candidate. One looked up the account at the document root instead of under `payload` and failed before sending any reset request. Each rerun above is the first run that exercised the candidate.
- **Gap:** with mail disabled, the plain token of the first link is never visible, so the runtime check proves the stored hash and expiry survive the second request rather than completing a reset with the first link. `AccountServiceTest` covers confirming a valid token.
- **Follow-up:** GitHub's dependency graph sees only 11 manifest packages, so Dependabot cannot flag transitive CVEs such as these. Submitting the resolved Gradle graph would close that gap.

## Document Status
complete

## Project
christopherbell-dev
