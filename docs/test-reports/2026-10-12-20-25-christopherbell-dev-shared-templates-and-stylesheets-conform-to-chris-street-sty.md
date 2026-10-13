# Shared templates and stylesheets conform to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-20-06-christopherbell-dev-shared-templates-and-stylesheets-conform-to-chris-street-sty.md): The Bell pages match production apart from the moved heading style, and the stylesheet is served as committed.

## Branch
`claude/style-templates-20261012` at candidate `09ed774`

## Pass / Fail

> [!TIP]
> 5 of 5 cases passed on candidate `09ed774`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | The Bell pages match production apart from the moved heading style, and the stylesheet is served as committed | ✅ PASS | Expected exit code 0 |
| 4 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 5 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-templates\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-templates' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:51785/actuator/health/readiness`
3. **The Bell pages match production apart from the moved heading style, and the stylesheet is served as committed**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\template_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json A:\Projects\christopherbell.dev-worktrees\style-templates`
4. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
5. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-templates C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Production comparison | read-only GETs of https://www.christopherbell.dev/thebell and /thebell/tony, masking per-build values and the edge analytics beacon |
| Checks | full check passed on 2dc44f14; bootJar rebuilt on 09ed7742 |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-templates\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-templates' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-templates`
- **Local command:** `GET http://127.0.0.1:51785/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-templates`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\template_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json A:\Projects\christopherbell.dev-worktrees\style-templates` in `A:\Projects\christopherbell.dev-worktrees\style-templates`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-templates`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-templates C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-logs` in `A:\Projects\christopherbell.dev-worktrees\style-templates`
- **Candidate identity:** `09ed774`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-templates\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-templates' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:51785/actuator/health/readiness
```

### 3. The Bell pages match production apart from the moved heading style, and the stylesheet is served as committed

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\template_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json A:\Projects\christopherbell.dev-worktrees\style-templates
```

### 4. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 5. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-templates C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\t-logs
```

## Response Received

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
exit code: 0
--- stdout ---
ready=True db=test credentialFileInRoot=True
```

### 2. The candidate reports readiness UP

```text
HTTP 200 
X-Request-Id: 2e53ff4b-3898-4de4-babc-27742cbddaec
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791854757
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
Date: Tue, 13 Oct 2026 01:24:57 GMT
Connection: close

{"status":"UP"}
```

### 3. The Bell pages match production apart from the moved heading style, and the stylesheet is served as committed

```text
exit code: 0
--- stdout ---
PASS /thebell renders a plain heading: 200
PASS /thebell matches production apart from the moved heading style: 6978 characters
PASS /thebell/tony renders a plain heading: 200
PASS /thebell/tony matches production apart from the moved heading style: 2942 characters
PASS thebell.css is served as committed apart from fingerprinted url() references, and sizes h1 at 70px: 200
```

### 4. The candidate log has no ERROR line and no administrator password

```text
exit code: 0
--- stdout ---
created=True passwordInLog=False errorLines=0
```

### 5. Stop-Candidate stops the candidate and removes the root with the credential file

```text
exit code: 0
--- stdout ---
port 51785 listeners: 0
port 51784 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-a60664f16fd1426bb70fd0b39275e3af
removed C:\Temp\cbell-jdk-7d9018139f194f268035a274af69b492
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-12T20:24:46-05:00, took 10687 ms, candidate `09ed774`
- Case 2 started 2026-10-12T20:24:57-05:00, took 32 ms, candidate `09ed774`
- Case 3 started 2026-10-12T20:24:57-05:00, took 796 ms, candidate `09ed774`
- Case 4 started 2026-10-12T20:24:58-05:00, took 266 ms, candidate `09ed774`
- Case 5 started 2026-10-12T20:24:58-05:00, took 5218 ms, candidate `09ed774`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
