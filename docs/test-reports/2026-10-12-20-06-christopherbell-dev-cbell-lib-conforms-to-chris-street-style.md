# Cbell-lib conforms to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-20-06-christopherbell-dev-cbell-lib-conforms-to-chris-street-style.md): password hashing and verification through sign-up and login, and the application-wide sweep, behave as before.

## Branch
`claude/style-cbell-lib-20261012` at candidate `190e85e`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `190e85e`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | Password hashing and verification through sign-up and login behave as before | ✅ PASS | Expected exit code 0 |
| 4 | Anonymous, USER and ADMIN requests across the application behave as on main | ✅ PASS | Expected exit code 0 |
| 5 | A USER without a grant is refused and a granted USER can read | ✅ PASS | Expected exit code 0 |
| 6 | Shared-folder responses carry no-store caching | ✅ PASS | Expected exit code 0 |
| 7 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 8 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-cbell-lib\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-cbell-lib' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:53574/actuator/health/readiness`
3. **Password hashing and verification through sign-up and login behave as before**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\password_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json`
4. **Anonymous, USER and ADMIN requests across the application behave as on main**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3_sweep.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json`
5. **A USER without a grant is refused and a granted USER can read**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json`
6. **Shared-folder responses carry no-store caching**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:53574`
7. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
8. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-cbell-lib C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Full check | passed on 190e85ec with Checkstyle covering cbell-lib |
| Legacy hashes | covered by PasswordUtilTest; no API creates them |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-cbell-lib\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-cbell-lib' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `GET http://127.0.0.1:53574/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\password_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3_sweep.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:53574` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-cbell-lib C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-logs` in `A:\Projects\christopherbell.dev-worktrees\style-cbell-lib`
- **Candidate identity:** `190e85e`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-cbell-lib\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-cbell-lib' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:53574/actuator/health/readiness
```

### 3. Password hashing and verification through sign-up and login behave as before

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\password_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json
```

### 4. Anonymous, USER and ADMIN requests across the application behave as on main

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s3_sweep.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json
```

### 5. A USER without a grant is refused and a granted USER can read

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json
```

### 6. Shared-folder responses carry no-store caching

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:53574
```

### 7. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 8. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-cbell-lib C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\l-logs
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
X-Request-Id: c34a716e-ecfe-4de9-9294-9df387d60ecb
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791853576
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
Date: Tue, 13 Oct 2026 01:05:16 GMT
Connection: close

{"status":"UP"}
```

### 3. Password hashing and verification through sign-up and login behave as before

```text
exit code: 0
--- stdout ---
PASS the bootstrap administrator, hashed at startup, logs in: 200
PASS sign-up stores a new current-format hash: 201
PASS the new account logs in with its password: [REDACTED]
PASS a wrong password is rejected with the generic login failure: 401 ['INVALID_TOKEN']
PASS the correct password still works after a rejected attempt: 200
PASS an unknown account is rejected like a wrong password: [REDACTED]
```

### 4. Anonymous, USER and ADMIN requests across the application behave as on main

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

### 5. A USER without a grant is refused and a granted USER can read

```text
exit code: 0
--- stdout ---
PASS the test administrator logs in: 200
PASS the administrator reads /api/shared-folder/2026-07-17/admin/recycle: 200
PASS the administrator reads /api/shared-folder/2026-07-17/admin/audit: 200
PASS a disposable USER is created through the API: 201
PASS the USER logs in: 200
PASS the USER without a grant cannot list shared-folder entries: 403
PASS the USER cannot read the admin recycle bin: 403
PASS the administrator grants the USER shared-folder read through the account API: 200
PASS the granted USER lists shared-folder entries: 200
PASS the read-only USER still cannot create a folder: 403
```

### 6. Shared-folder responses carry no-store caching

```text
exit code: 0
--- stdout ---
PASS /api/shared-folder/2026-07-17/entries?path= (403) carries no-store caching: 'private, no-store'
PASS /api/shared-folder/2026-07-17/radio (403) carries no-store caching: 'private, no-store'
PASS /shared (200) carries no-store caching: 'no-cache, no-store, max-age=0, must-revalidate'
```

### 7. The candidate log has no ERROR line and no administrator password

```text
exit code: 0
--- stdout ---
created=True passwordInLog=False errorLines=0
```

### 8. Stop-Candidate stops the candidate and removes the root with the credential file

```text
exit code: 0
--- stdout ---
port 53574 listeners: 0
port 53573 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-c2f5e5861d7b4b96a783470f2b4a6011
removed C:\Temp\cbell-jdk-3cd60c0ab5544812a495b33da3d6f014
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-12T20:05:07-05:00, took 8922 ms, candidate `190e85e`
- Case 2 started 2026-10-12T20:05:16-05:00, took 46 ms, candidate `190e85e`
- Case 3 started 2026-10-12T20:05:16-05:00, took 655 ms, candidate `190e85e`
- Case 4 started 2026-10-12T20:05:17-05:00, took 766 ms, candidate `190e85e`
- Case 5 started 2026-10-12T20:05:18-05:00, took 327 ms, candidate `190e85e`
- Case 6 started 2026-10-12T20:05:19-05:00, took 108 ms, candidate `190e85e`
- Case 7 started 2026-10-12T20:05:19-05:00, took 266 ms, candidate `190e85e`
- Case 8 started 2026-10-12T20:05:19-05:00, took 5578 ms, candidate `190e85e`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
