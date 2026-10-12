# Checkstyle gate: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-11-19-47-christopherbell-dev-checkstyle-gate-for-mechanical-chris-street-style-rules.md): the candidate with about 110 files of mechanical style fixes behaves as main for anonymous, USER and ADMIN requests across account, admin, post, message, music access, site monitor, Survive, reports and the shared folder.

## Branch
`claude/style-lint-20261011` at candidate `8f1b90e`

## Pass / Fail

> [!TIP]
> 5 of 5 cases passed on candidate `8f1b90e`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | Anonymous, USER and ADMIN requests across every area the Checkstyle fixes touched behave as on main | ✅ PASS | Expected exit code 0 |
| 4 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 5 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-lint\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-lint' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:50672/actuator/health/readiness`
3. **Anonymous, USER and ADMIN requests across every area the Checkstyle fixes touched behave as on main**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3_sweep.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json`
4. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
5. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-lint C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Expectations | calibrated against main plus the test administrator (f9789ca) before this run |
| Full check | .\ops\local\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar passed on 8f1b90e8 with zero Checkstyle violations |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-lint\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-lint' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-lint`
- **Local command:** `GET http://127.0.0.1:50672/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-lint`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3_sweep.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-lint`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-lint`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-lint C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-logs` in `A:\Projects\christopherbell.dev-worktrees\style-lint`
- **Candidate identity:** `8f1b90e`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-lint\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-lint' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:50672/actuator/health/readiness
```

### 3. Anonymous, USER and ADMIN requests across every area the Checkstyle fixes touched behave as on main

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3_sweep.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json
```

### 4. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 5. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-lint C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3-logs
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
X-Request-Id: c5c021cc-0475-4e32-b64b-6ac204ac0077
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791768843
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
Date: Mon, 12 Oct 2026 01:33:03 GMT
Connection: close

{"status":"UP"}
```

### 3. Anonymous, USER and ADMIN requests across every area the Checkstyle fixes touched behave as on main

<details><summary>36 lines</summary>

```text
exit code: 0
--- stdout ---
PASS anonymous GET /api/posts/2026-07-28/discovery/new: 200
PASS anonymous GET /api/posts/2026-07-28/discovery/topics: 200
PASS anonymous GET /api/survive/v1/game has no character yet (204): 204
PASS anonymous GET /api/accounts/2025-09-03/me is refused: 403
PASS anonymous GET /api/messages/2025-09-14/conversations is refused: 403
PASS anonymous GET /api/admin/command-center/2026-07-12/snapshot is refused: 403
PASS anonymous GET /api/site-monitor/v1 is refused: 403
PASS alice_sweep is created: 201
PASS alice_sweep logs in: 200
PASS bob_sweep is created: 201
PASS bob_sweep logs in: 200
PASS USER reads own account: 200
PASS USER creates a post: 201
PASS another USER likes the post: 200
PASS USER reads own feed: 200
PASS USER sends a message: 201
PASS recipient lists conversations: 200
PASS USER joins Survive: 200
PASS USER resumes Survive: 200
PASS USER reads the site monitor workspace: 200
PASS USER without music access reads music access status: 200
PASS USER cannot read the command center: 403
PASS ADMIN logs in: 200
PASS ADMIN GET /api/admin/command-center/2026-07-12/snapshot: 200
PASS ADMIN GET /api/admin/command-center/2026-07-12/logs: 200
PASS ADMIN GET /api/admin/activity/2026-07-26: 200
PASS ADMIN GET /api/reports/2026-07-26: 200
PASS ADMIN GET /api/accounts/2026-07-26/admin: 200
PASS ADMIN GET /api/music/2026-07-28/admin/access-attempts: 200
PASS ADMIN GET /api/shared-folder/2026-07-17/admin/audit: 200
PASS ADMIN GET /api/shared-folder/2026-07-17/admin/recycle: 200
PASS ADMIN GET /api/shared-folder/2026-07-17/entries?path=: 200
PASS ADMIN updates a USER through account moderation: 200
PASS the moderated USER sees the new first name: Alicia
```

</details>

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
port 50672 listeners: 0
port 50671 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-cfd3668927594648a89224f827c64e93
removed C:\Temp\cbell-jdk-ba08abd2681c414890effa60c9128aea
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-11T20:32:55-05:00, took 8264 ms, candidate `8f1b90e`
- Case 2 started 2026-10-11T20:33:03-05:00, took 62 ms, candidate `8f1b90e`
- Case 3 started 2026-10-11T20:33:03-05:00, took 1000 ms, candidate `8f1b90e`
- Case 4 started 2026-10-11T20:33:04-05:00, took 264 ms, candidate `8f1b90e`
- Case 5 started 2026-10-11T20:33:05-05:00, took 4671 ms, candidate `8f1b90e`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
