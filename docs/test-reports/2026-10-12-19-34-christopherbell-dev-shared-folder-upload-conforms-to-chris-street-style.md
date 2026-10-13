# Shared folder upload conforms to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-19-17-christopherbell-dev-shared-folder-upload-conforms-to-chris-street-style.md): chunked uploads append, retry idempotently, verify digests, finalize, conflict, cancel and refuse readers.

## Branch
`claude/style-shared-upload-20261012` at candidate `5f1d1c8`

## Pass / Fail

> [!TIP]
> 7 of 7 cases passed on candidate `5f1d1c8`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | Chunked uploads append, retry idempotently, verify digests, finalize, conflict, cancel and refuse readers | ✅ PASS | Expected exit code 0 |
| 4 | A USER without a grant is refused and a granted USER can read | ✅ PASS | Expected exit code 0 |
| 5 | Shared-folder responses carry no-store caching | ✅ PASS | Expected exit code 0 |
| 6 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 7 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-upload\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-upload' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:60238/actuator/health/readiness`
3. **Chunked uploads append, retry idempotently, verify digests, finalize, conflict, cancel and refuse readers**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\upload_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json`
4. **A USER without a grant is refused and a granted USER can read**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json`
5. **Shared-folder responses carry no-store caching**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:60238`
6. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
7. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-upload C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Full check | passed on 6394178a with Checkstyle covering upload; after merging main (5f1d1c80) Checkstyle and bootJar passed again |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-upload\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-upload' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Local command:** `GET http://127.0.0.1:60238/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\upload_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:60238` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-upload C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-logs` in `A:\Projects\christopherbell.dev-worktrees\style-shared-upload`
- **Candidate identity:** `5f1d1c8`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-upload\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-upload' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:60238/actuator/health/readiness
```

### 3. Chunked uploads append, retry idempotently, verify digests, finalize, conflict, cancel and refuse readers

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\upload_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json
```

### 4. A USER without a grant is refused and a granted USER can read

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json
```

### 5. Shared-folder responses carry no-store caching

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:60238
```

### 6. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 7. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-upload C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\u-logs
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
X-Request-Id: 4a0e4f5f-7ab9-4d8b-aad7-fea7ba1be32d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791851693
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
Date: Tue, 13 Oct 2026 00:33:53 GMT
Connection: close

{"status":"UP"}
```

### 3. Chunked uploads append, retry idempotently, verify digests, finalize, conflict, cancel and refuse readers

```text
exit code: 0
--- stdout ---
PASS the administrator logs in: login
PASS an upload session is created (201): 201 {'id': '433146b7-e540-481a-bea8-c06933d04941', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 0, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T00:33:54.497715800Z', 'chunkSizeBytes': 8388608, 'committedChunks': []}
PASS the chunk is appended: 200 {'id': '433146b7-e540-481a-bea8-c06933d04941', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T00:33:54.497Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS an identical retry of the same chunk is idempotent: 200 {'id': '433146b7-e540-481a-bea8-c06933d04941', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T00:33:54.497Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS the owner reads upload progress: 200 {'id': '433146b7-e540-481a-bea8-c06933d04941', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T00:33:54.497Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS completion finalizes the upload: 200 {'id': '433146b7-e540-481a-bea8-c06933d04941', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'COMPLETED', 'expiresAt': '2026-10-14T00:33:54.497Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS the uploaded bytes read back exactly: 200 2048 bytes
PASS a chunk whose digest does not match is refused: 409
PASS completing onto an existing name without replace is refused (409): 409
PASS an upload whose completion was refused can no longer be canceled (409, as on main): 409
PASS the owner cancels an unfinished upload: 200 {'id': 'c2c54706-bd2f-4d6f-b0c2-709523407986', 'parentPath': '', 'name': 'upload-cancel.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'CANCELLED', 'expiresAt': '2026-10-14T00:33:54.721Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS a read-only USER cannot start an upload (403): 403
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
port 60238 listeners: 0
port 60237 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-2a5611bfdb9c41f1973f278d69176c80
removed C:\Temp\cbell-jdk-ddf9c96814b4423ab27a8ba23d6bb65b
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-12T19:33:44-05:00, took 9046 ms, candidate `5f1d1c8`
- Case 2 started 2026-10-12T19:33:53-05:00, took 47 ms, candidate `5f1d1c8`
- Case 3 started 2026-10-12T19:33:54-05:00, took 844 ms, candidate `5f1d1c8`
- Case 4 started 2026-10-12T19:33:55-05:00, took 344 ms, candidate `5f1d1c8`
- Case 5 started 2026-10-12T19:33:55-05:00, took 125 ms, candidate `5f1d1c8`
- Case 6 started 2026-10-12T19:33:55-05:00, took 265 ms, candidate `5f1d1c8`
- Case 7 started 2026-10-12T19:33:56-05:00, took 5109 ms, candidate `5f1d1c8`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
