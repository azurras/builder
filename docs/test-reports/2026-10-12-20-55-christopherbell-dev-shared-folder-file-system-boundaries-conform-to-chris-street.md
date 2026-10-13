# Shared folder file system boundaries conform to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-19-17-christopherbell-dev-shared-folder-file-system-boundaries-conform-to-chris-street.md): mutations, search, download, chunked upload through private staging, and recycle, restore and purge exercise every file system boundary.

## Branch
`claude/style-shared-fs-20261012` at candidate `218f0e1`

## Pass / Fail

> [!TIP]
> 9 of 9 cases passed on candidate `218f0e1`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | File system operations through every boundary: mutations, search and download | ✅ PASS | Expected exit code 0 |
| 4 | Chunked uploads through the private staging boundary | ✅ PASS | Expected exit code 0 |
| 5 | Recycle, restore and purge through the native recycle boundary | ✅ PASS | Expected exit code 0 |
| 6 | A USER without a grant is refused and a granted USER can read | ✅ PASS | Expected exit code 0 |
| 7 | Shared-folder responses carry no-store caching | ✅ PASS | Expected exit code 0 |
| 8 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 9 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-fs\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-fs' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:64315/actuator/health/readiness`
3. **File system operations through every boundary: mutations, search and download**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\service_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json`
4. **Chunked uploads through the private staging boundary**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\upload_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json`
5. **Recycle, restore and purge through the native recycle boundary**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\recycle_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json`
6. **A USER without a grant is refused and a granted USER can read**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json`
7. **Shared-folder responses carry no-store caching**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:64315`
8. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
9. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-fs C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Full check | passed on c510b22b with Checkstyle covering fs; after merging main (218f0e12) compilation, Checkstyle and bootJar passed again |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-fs\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-fs' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `GET http://127.0.0.1:64315/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\service_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\upload_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\recycle_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:64315` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-fs C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-logs` in `A:\Projects\christopherbell.dev-worktrees\style-shared-fs`
- **Candidate identity:** `218f0e1`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-fs\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-fs' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:64315/actuator/health/readiness
```

### 3. File system operations through every boundary: mutations, search and download

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\service_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json
```

### 4. Chunked uploads through the private staging boundary

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\upload_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json
```

### 5. Recycle, restore and purge through the native recycle boundary

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\recycle_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json
```

### 6. A USER without a grant is refused and a granted USER can read

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json
```

### 7. Shared-folder responses carry no-store caching

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:64315
```

### 8. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 9. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-fs C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\h-logs
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
X-Request-Id: 96d7199c-0f80-47d1-8138-42108ba91036
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791856540
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
Date: Tue, 13 Oct 2026 01:54:40 GMT
Connection: close

{"status":"UP"}
```

### 3. File system operations through every boundary: mutations, search and download

```text
exit code: 0
--- stdout ---
PASS the administrator logs in: 200
PASS three folders are created: ['alpha-notes', 'beta-notes', 'gamma-notes']
PASS a folder is renamed: 200 {'name': 'delta-notes', 'path': 'delta-notes', 'type': 'DIRECTORY', 'size': 0, 'modifiedAt': '2026-10-13T01:54:41.089053900Z', 'previewKind': 'NONE', 'observedToken': '7-AYQ10wJRXC-ikA3OIhPnl3WFlw2UULpJ3GygZqgBE'}
PASS a folder is moved into another: 200 {'name': 'beta-notes', 'path': 'alpha-notes/beta-notes', 'type': 'DIRECTORY', 'size': 0, 'modifiedAt': '2026-10-13T01:54:41.078049600Z', 'previewKind': 'NONE', 'observedToken': 'ayLpyDdAOHyMgdDHnO7MT-DfugjLRPW5jGG-BUin5qY'}
PASS listings reflect the rename and move: ['alpha-notes', 'delta-notes', 'notes-download.txt'] / ['beta-notes']
PASS search pages one entry at a time through cursors until done: 200 pages=4 ['alpha-notes', 'alpha-notes/beta-notes', 'delta-notes', 'notes-download.txt']
PASS search responses are private and never stored: private, no-store
PASS a malformed cursor is rejected (400): 400
PASS a file downloads byte for byte: 200 34
PASS a folder is deleted with its observed token: [REDACTED]
PASS a delete with a stale observed token is refused (409): 409
```

### 4. Chunked uploads through the private staging boundary

```text
exit code: 0
--- stdout ---
PASS the administrator logs in: login
PASS an upload session is created (201): 201 {'id': '93bcc1f3-de61-46d4-b51e-e1a7e3948e55', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 0, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T01:54:41.521465700Z', 'chunkSizeBytes': 8388608, 'committedChunks': []}
PASS the chunk is appended: 200 {'id': '93bcc1f3-de61-46d4-b51e-e1a7e3948e55', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T01:54:41.521Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS an identical retry of the same chunk is idempotent: 200 {'id': '93bcc1f3-de61-46d4-b51e-e1a7e3948e55', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T01:54:41.521Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS the owner reads upload progress: 200 {'id': '93bcc1f3-de61-46d4-b51e-e1a7e3948e55', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'ACTIVE', 'expiresAt': '2026-10-14T01:54:41.521Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS completion finalizes the upload: 200 {'id': '93bcc1f3-de61-46d4-b51e-e1a7e3948e55', 'parentPath': '', 'name': 'upload-check.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'COMPLETED', 'expiresAt': '2026-10-14T01:54:41.521Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS the uploaded bytes read back exactly: 200 2048 bytes
PASS a chunk whose digest does not match is refused: 409
PASS completing onto an existing name without replace is refused (409): 409
PASS an upload whose completion was refused can no longer be canceled (409, as on main): 409
PASS the owner cancels an unfinished upload: 200 {'id': '87d68bee-36db-4e49-979e-5bb695059954', 'parentPath': '', 'name': 'upload-cancel.txt', 'expectedBytes': 2048, 'nextOffset': 2048, 'state': 'CANCELLED', 'expiresAt': '2026-10-14T01:54:41.683Z', 'chunkSizeBytes': 8388608, 'committedChunks': [{'offset': 0, 'length': 2048, 'sha256': 'd308hXcAziaQdneftdDYJDsJ1d2bVuywTMi6hxSw9Tc'}]}
PASS a read-only USER cannot start an upload (403): 403
```

### 5. Recycle, restore and purge through the native recycle boundary

```text
exit code: 0
--- stdout ---
PASS the administrator logs in: 200
PASS the administrator creates a folder: 201
PASS deleting the folder succeeds: 204
PASS the deleted folder appears in the recycle bin: 200 items=2
PASS restoring it returns the folder: 200
PASS the restored folder is listed again: 200 ['alpha-notes', 'notes-download.txt', 'recycle-check', 'upload-check.txt']
PASS the restored item left the recycle bin: 1
PASS deleting the restored folder succeeds: 204
PASS it is recycled again: 2
PASS a purge with the wrong confirmation is refused: 400
PASS a purge with the exact confirmation succeeds: 204
PASS the purged item is gone: 1
PASS the audit log records restore and purge: ['CREATE_FOLDER', 'DOWNLOAD_COMPLETED', 'DOWNLOAD_STARTED', 'LIST', 'MOVE', 'PERMISSION_CHANGE', 'PURGE', 'RECYCLE', 'RECYCLE_BROWSE', 'RENAME', 'RESTORE', 'SEARCH', 'UPLOAD_APPEND', 'UPLOAD_CANCEL', 'UPLOAD_FINALIZE', 'UPLOAD_START', 'UPLOAD_STATUS']
```

### 6. A USER without a grant is refused and a granted USER can read

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

### 7. Shared-folder responses carry no-store caching

```text
exit code: 0
--- stdout ---
PASS /api/shared-folder/2026-07-17/entries?path= (403) carries no-store caching: 'private, no-store'
PASS /api/shared-folder/2026-07-17/radio (403) carries no-store caching: 'private, no-store'
PASS /shared (200) carries no-store caching: 'no-cache, no-store, max-age=0, must-revalidate'
```

### 8. The candidate log has no ERROR line and no administrator password

```text
exit code: 0
--- stdout ---
created=True passwordInLog=False errorLines=0
```

### 9. Stop-Candidate stops the candidate and removes the root with the credential file

```text
exit code: 0
--- stdout ---
port 64315 listeners: 0
port 64314 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-89c7e56e18284c37a12a5187d36ad6f8
removed C:\Temp\cbell-jdk-bb07c52b2c534159b9bfa481154e1770
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-12T20:54:30-05:00, took 9453 ms, candidate `218f0e1`
- Case 2 started 2026-10-12T20:54:40-05:00, took 62 ms, candidate `218f0e1`
- Case 3 started 2026-10-12T20:54:40-05:00, took 610 ms, candidate `218f0e1`
- Case 4 started 2026-10-12T20:54:41-05:00, took 514 ms, candidate `218f0e1`
- Case 5 started 2026-10-12T20:54:42-05:00, took 280 ms, candidate `218f0e1`
- Case 6 started 2026-10-12T20:54:42-05:00, took 328 ms, candidate `218f0e1`
- Case 7 started 2026-10-12T20:54:42-05:00, took 125 ms, candidate `218f0e1`
- Case 8 started 2026-10-12T20:54:43-05:00, took 265 ms, candidate `218f0e1`
- Case 9 started 2026-10-12T20:54:43-05:00, took 4500 ms, candidate `218f0e1`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
