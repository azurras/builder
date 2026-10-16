# Mark proxied cookies Secure: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-16-13-45-christopherbell-dev-mark-proxied-cookies-secure.md): with secure cookies configured, the survive and CSRF cookies carry Secure on plain-HTTP (proxied) requests; with the default setting local HTTP still works.

## Branch
`claude/secure-proxied-cookies-20261016` at candidate `aeca69c`

## Pass / Fail

> [!TIP]
> 10 of 10 cases passed on candidate `aeca69c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate with secure cookies configured starts an isolated candidate on database test | ✅ PASS | Expected exit code 0 |
| 2 | The secure-cookie candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | With secure cookies configured, a plain-HTTP survive join returns Secure XSRF-TOKEN and CBELL_SURVIVOR cookies, rejects a join without the CSRF header, and the cookie plays a turn | ✅ PASS | Expected exit code 0 |
| 4 | The secure-cookie candidate log has no ERROR line | ✅ PASS | Expected exit code 0 |
| 5 | Stop-Candidate stops the secure-cookie candidate, frees both ports and removes its disposable root | ✅ PASS | Expected exit code 0 |
| 6 | Start-Candidate with the default cookie setting starts an isolated candidate on database test | ✅ PASS | Expected exit code 0 |
| 7 | The default-setting candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 8 | With the default setting, local HTTP keeps both cookies without Secure, still rejects a join without the CSRF header, and the cookie plays a turn | ✅ PASS | Expected exit code 0 |
| 9 | The default-setting candidate log has no ERROR line | ✅ PASS | Expected exit code 0 |
| 10 | Stop-Candidate stops the default-setting candidate, frees both ports and removes its disposable root | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate with secure cookies configured starts an isolated candidate on database test**: command `pwsh -NoLogo -NoProfile -Command "$env:APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE='true'; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' -Checkout 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies' | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) url=$($s.baseUrl)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"`
2. **The secure-cookie candidate reports readiness UP**: http `GET http://127.0.0.1:56960/actuator/health/readiness`
3. **With secure cookies configured, a plain-HTTP survive join returns Secure XSRF-TOKEN and CBELL_SURVIVOR cookies, rejects a join without the CSRF header, and the cookie plays a turn**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\cookie_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json secure`
4. **The secure-cookie candidate log has no ERROR line**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"errorLines=$errors\"; if ($errors) { exit 1 }"`
5. **Stop-Candidate stops the secure-cookie candidate, frees both ports and removes its disposable root**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($s.candidatePort, $s.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $s.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"`
6. **Start-Candidate with the default cookie setting starts an isolated candidate on database test**: command `pwsh -NoLogo -NoProfile -Command "Remove-Item Env:APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE -ErrorAction SilentlyContinue; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' -Checkout 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies' | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"`
7. **The default-setting candidate reports readiness UP**: http `GET http://127.0.0.1:60540/actuator/health/readiness`
8. **With the default setting, local HTTP keeps both cookies without Secure, still rejects a join without the CSRF header, and the cookie plays a turn**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\cookie_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json insecure`
9. **The default-setting candidate log has no ERROR line**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"errorLines=$errors\"; if ($errors) { exit 1 }"`
10. **Stop-Candidate stops the default-setting candidate, frees both ports and removes its disposable root**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($s.candidatePort, $s.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $s.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Run 1 | APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE=true, the production value |
| Run 2 | default setting (false), as in local development |
| Checks | :website:build passed on aeca69c2 (2,138 tests, 0 failed); bootJar rebuilt on aeca69c2 |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$env:APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE='true'; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' -Checkout 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies' | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) url=$($s.baseUrl)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `GET http://127.0.0.1:56960/actuator/health/readiness` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\cookie_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json secure` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"errorLines=$errors\"; if ($errors) { exit 1 }"` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($s.candidatePort, $s.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $s.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "Remove-Item Env:APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE -ErrorAction SilentlyContinue; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' -Checkout 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies' | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `GET http://127.0.0.1:60540/actuator/health/readiness` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\cookie_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json insecure` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"errorLines=$errors\"; if ($errors) { exit 1 }"` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($s.candidatePort, $s.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $s.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"` in `A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies`
- **Candidate identity:** `aeca69c`
- **Cleanup:** Stop-Candidate.ps1 stopped both runs' candidate and mongod process trees; their ports had no listeners and both disposable roots were removed. Production MongoDB on 27017 kept listening. The survivors joined during the runs lived only in the disposable databases.

## Data Sent

### 1. Start-Candidate with secure cookies configured starts an isolated candidate on database test

```text
pwsh -NoLogo -NoProfile -Command "$env:APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE='true'; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' -Checkout 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies' | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) url=$($s.baseUrl)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"
```

### 2. The secure-cookie candidate reports readiness UP

```http
GET http://127.0.0.1:56960/actuator/health/readiness
```

### 3. With secure cookies configured, a plain-HTTP survive join returns Secure XSRF-TOKEN and CBELL_SURVIVOR cookies, rejects a join without the CSRF header, and the cookie plays a turn

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\cookie_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json secure
```

### 4. The secure-cookie candidate log has no ERROR line

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"errorLines=$errors\"; if ($errors) { exit 1 }"
```

### 5. Stop-Candidate stops the secure-cookie candidate, frees both ports and removes its disposable root

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\secure-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($s.candidatePort, $s.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $s.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"
```

### 6. Start-Candidate with the default cookie setting starts an isolated candidate on database test

```text
pwsh -NoLogo -NoProfile -Command "Remove-Item Env:APP_BROWSERSECURITY_AUTHENTICATIONCOOKIESECURE -ErrorAction SilentlyContinue; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' -Checkout 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies' | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName)\"; if (-not ($s.ready -and $s.databaseName -eq 'test')) { exit 1 }"
```

### 7. The default-setting candidate reports readiness UP

```http
GET http://127.0.0.1:60540/actuator/health/readiness
```

### 8. With the default setting, local HTTP keeps both cookies without Secure, still rejects a join without the CSRF header, and the cookie plays a turn

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\cookie_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json insecure
```

### 9. The default-setting candidate log has no ERROR line

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"errorLines=$errors\"; if ($errors) { exit 1 }"
```

### 10. Stop-Candidate stops the default-setting candidate, frees both ports and removes its disposable root

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' | ConvertFrom-Json; & 'A:\Projects\christopherbell.dev.worktrees\secure-proxied-cookies\ops\local\Stop-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-state.json' -LogDestination 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\036dbc58-e65d-42c6-80f6-74a7c4b2fa19\scratchpad\default-logs' | Out-Null; $listening = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -in @($s.candidatePort, $s.mongoPort)).Count; $rootGone = -not (Test-Path -LiteralPath $s.testMongoRoot); $prod = @(Get-NetTCPConnection -State Listen -LocalPort 27017 -ErrorAction SilentlyContinue).Count -gt 0; \"listeners=$listening rootRemoved=$rootGone productionMongoListening=$prod\"; if ($listening -or -not $rootGone) { exit 1 }"
```

## Response Received

### 1. Start-Candidate with secure cookies configured starts an isolated candidate on database test

```text
exit code: 0
--- stdout ---
ready=True db=test url=http://127.0.0.1:56960
```

### 2. The secure-cookie candidate reports readiness UP

```text
HTTP 200 
X-Request-Id: 8e07f86c-1c04-4a44-8d85-ba3c9b3b83cf
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792177362
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
Date: Fri, 16 Oct 2026 19:01:42 GMT
Connection: close

{"status":"UP"}
```

### 3. With secure cookies configured, a plain-HTTP survive join returns Secure XSRF-TOKEN and CBELL_SURVIVOR cookies, rejects a join without the CSRF header, and the cookie plays a turn

```text
exit code: 0
--- stdout ---
XSRF-TOKEN cookie: XSRF-TOKEN=[REDACTED]; Path=/; Secure
join without CSRF header: 403
join with CSRF header: 200
CBELL_SURVIVOR cookie: CBELL_SURVIVOR=<token>; Path=/api/survive/v1; Secure; HttpOnly; SameSite=Strict
gather with survivor cookie: 200 revision 1
all checks passed
```

### 4. The secure-cookie candidate log has no ERROR line

```text
exit code: 0
--- stdout ---
errorLines=0
```

### 5. Stop-Candidate stops the secure-cookie candidate, frees both ports and removes its disposable root

```text
exit code: 0
--- stdout ---
listeners=0 rootRemoved=True productionMongoListening=True
```

### 6. Start-Candidate with the default cookie setting starts an isolated candidate on database test

```text
exit code: 0
--- stdout ---
ready=True db=test
```

### 7. The default-setting candidate reports readiness UP

```text
HTTP 200 
X-Request-Id: dc33dbef-a4c8-4feb-bcd4-c594850cda8e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792177404
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
Date: Fri, 16 Oct 2026 19:02:24 GMT
Connection: close

{"status":"UP"}
```

### 8. With the default setting, local HTTP keeps both cookies without Secure, still rejects a join without the CSRF header, and the cookie plays a turn

```text
exit code: 0
--- stdout ---
XSRF-TOKEN cookie: XSRF-TOKEN=[REDACTED]; Path=/
join without CSRF header: 403
join with CSRF header: 200
CBELL_SURVIVOR cookie: CBELL_SURVIVOR=<token>; Path=/api/survive/v1; HttpOnly; SameSite=Strict
gather with survivor cookie: 200 revision 1
all checks passed
```

### 9. The default-setting candidate log has no ERROR line

```text
exit code: 0
--- stdout ---
errorLines=0
```

### 10. Stop-Candidate stops the default-setting candidate, frees both ports and removes its disposable root

```text
exit code: 0
--- stdout ---
listeners=0 rootRemoved=True productionMongoListening=True
```

## Evidence
- Case 1 started 2026-10-16T14:01:25-05:00, took 9842 ms, candidate `aeca69c`
- Case 2 started 2026-10-16T14:01:42-05:00, took 46 ms, candidate `aeca69c`
- Case 3 started 2026-10-16T14:01:42-05:00, took 452 ms, candidate `aeca69c`
- Case 4 started 2026-10-16T14:01:58-05:00, took 281 ms, candidate `aeca69c`
- Case 5 started 2026-10-16T14:01:58-05:00, took 4687 ms, candidate `aeca69c`
- Case 6 started 2026-10-16T14:02:15-05:00, took 8578 ms, candidate `aeca69c`
- Case 7 started 2026-10-16T14:02:24-05:00, took 47 ms, candidate `aeca69c`
- Case 8 started 2026-10-16T14:02:24-05:00, took 436 ms, candidate `aeca69c`
- Case 9 started 2026-10-16T14:02:25-05:00, took 296 ms, candidate `aeca69c`
- Case 10 started 2026-10-16T14:02:25-05:00, took 4578 ms, candidate `aeca69c`

## Bugs / Follow-ups
- The first full build on the working tree failed `ModularMonolithArchitectureTest`: `survive` may not depend on `configuration.security.BrowserSecurityProperties`. The controller now reads `app.browser-security.authentication-cookie-secure` with `@Value`, and the rebuilt candidate `aeca69c` passed every check above.

## Document Status
complete

## Project
christopherbell-dev
