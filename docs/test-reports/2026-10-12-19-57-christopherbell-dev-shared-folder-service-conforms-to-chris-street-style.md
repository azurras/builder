# Shared folder service conforms to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-19-17-christopherbell-dev-shared-folder-service-conforms-to-chris-street-style.md): folder mutations, catalog search cursors and downloads through the API.

## Branch
`claude/style-shared-service-20261012` at candidate `52c7473`

## Pass / Fail

> [!TIP]
> 7 of 7 cases passed on candidate `52c7473`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | Folder create, rename, move and delete, catalog search cursors and downloads behave as designed | ✅ PASS | Expected exit code 0 |
| 4 | A USER without a grant is refused and a granted USER can read | ✅ PASS | Expected exit code 0 |
| 5 | Shared-folder responses carry no-store caching | ✅ PASS | Expected exit code 0 |
| 6 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 7 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-service\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-service' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:53680/actuator/health/readiness`
3. **Folder create, rename, move and delete, catalog search cursors and downloads behave as designed**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\service_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json`
4. **A USER without a grant is refused and a granted USER can read**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json`
5. **Shared-folder responses carry no-store caching**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:53680`
6. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
7. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-service C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder; one small text file written into the disposable shared root |
| Full check | passed on d98e3294 with Checkstyle covering service and the package-level tests; after merging main (52c74735) compilation, Checkstyle and bootJar passed again |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-service\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-service' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Local command:** `GET http://127.0.0.1:53680/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\service_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:53680` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-service C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-logs` in `A:\Projects\christopherbell.dev-worktrees\style-shared-service`
- **Candidate identity:** `52c7473`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-service\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-service' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:53680/actuator/health/readiness
```

### 3. Folder create, rename, move and delete, catalog search cursors and downloads behave as designed

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\service_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json
```

### 4. A USER without a grant is refused and a granted USER can read

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json
```

### 5. Shared-folder responses carry no-store caching

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:53680
```

### 6. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 7. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-service C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\g-logs
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
X-Request-Id: 03064d7e-c91a-454a-b95e-b07d11264317
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791853064
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
Date: Tue, 13 Oct 2026 00:56:44 GMT
Connection: close

{"status":"UP"}
```

### 3. Folder create, rename, move and delete, catalog search cursors and downloads behave as designed

```text
exit code: 0
--- stdout ---
PASS the administrator logs in: 200
PASS three folders are created: ['alpha-notes', 'beta-notes', 'gamma-notes']
PASS a folder is renamed: 200 {'name': 'delta-notes', 'path': 'delta-notes', 'type': 'DIRECTORY', 'size': 0, 'modifiedAt': '2026-10-13T00:56:45.081936600Z', 'previewKind': 'NONE', 'observedToken': 'VL10Bw7v-o_CW2nch2bLStyy8YDek1D0junMU5p47Bg'}
PASS a folder is moved into another: 200 {'name': 'beta-notes', 'path': 'alpha-notes/beta-notes', 'type': 'DIRECTORY', 'size': 0, 'modifiedAt': '2026-10-13T00:56:45.072434200Z', 'previewKind': 'NONE', 'observedToken': 'zs26cKb845z5mOld-pIQX8p78UvRfV70gqGdY4aZbRQ'}
PASS listings reflect the rename and move: ['alpha-notes', 'delta-notes', 'notes-download.txt'] / ['beta-notes']
PASS search pages one entry at a time through cursors until done: 200 pages=4 ['alpha-notes', 'alpha-notes/beta-notes', 'delta-notes', 'notes-download.txt']
PASS search responses are private and never stored: private, no-store
PASS a malformed cursor is rejected (400): 400
PASS a file downloads byte for byte: 200 34
PASS a folder is deleted with its observed token: [REDACTED]
PASS a delete with a stale observed token is refused (409): 409
```

### 4. A USER without a grant is refused and a granted USER can read

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

### 5. Shared-folder responses carry no-store caching

```text
exit code: 0
--- stdout ---
PASS /api/shared-folder/2026-07-17/entries?path= (403) carries no-store caching: 'private, no-store'
PASS /api/shared-folder/2026-07-17/radio (403) carries no-store caching: 'private, no-store'
PASS /shared (200) carries no-store caching: 'no-cache, no-store, max-age=0, must-revalidate'
```

### 6. The candidate log has no ERROR line and no administrator password

```text
exit code: 0
--- stdout ---
created=True passwordInLog=False errorLines=0
```

### 7. Stop-Candidate stops the candidate and removes the root with the credential file

```text
exit code: 0
--- stdout ---
port 53680 listeners: 0
port 53679 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-1d599c4c7b2c4413a26f35ff3e1c9a7d
removed C:\Temp\cbell-jdk-5c40c463be04435a82a2db698d4afe23
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-12T19:56:35-05:00, took 8891 ms, candidate `52c7473`
- Case 2 started 2026-10-12T19:56:44-05:00, took 62 ms, candidate `52c7473`
- Case 3 started 2026-10-12T19:56:44-05:00, took 578 ms, candidate `52c7473`
- Case 4 started 2026-10-12T19:56:45-05:00, took 360 ms, candidate `52c7473`
- Case 5 started 2026-10-12T19:56:45-05:00, took 125 ms, candidate `52c7473`
- Case 6 started 2026-10-12T19:56:46-05:00, took 250 ms, candidate `52c7473`
- Case 7 started 2026-10-12T19:56:46-05:00, took 4796 ms, candidate `52c7473`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
