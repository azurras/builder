# Shared folder front end conforms to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-19-19-christopherbell-dev-shared-folder-front-end-conforms-to-chris-street-style.md): every changed shared-folder module is served exactly as committed, the page renders for a signed-in administrator, and the shared-folder JavaScript tests pass.

## Branch
`claude/style-shared-front-20261012` at candidate `7000ac6`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `7000ac6`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | The shared-folder page and every changed module are served exactly as committed | ✅ PASS | Expected exit code 0 |
| 4 | Browser-side JavaScript tests pass (node --test) | ✅ PASS | Expected exit code 0 |
| 5 | A USER without a grant is refused and a granted USER can read | ✅ PASS | Expected exit code 0 |
| 6 | Shared-folder responses carry no-store caching | ✅ PASS | Expected exit code 0 |
| 7 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 8 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-front\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-front' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:51061/actuator/health/readiness`
3. **The shared-folder page and every changed module are served exactly as committed**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\front_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json A:\Projects\christopherbell.dev-worktrees\style-shared-front`
4. **Browser-side JavaScript tests pass (node --test)**: command `node --test website/src/test/js/back-office-shared-folder.test.js website/src/test/js/shared-folder-page-initialization.test.js website/src/test/js/shared-folder-streaming.test.js website/src/test/js/shared-folder-worker-runtime.test.js website/src/test/js/shared-folder.test.js`
5. **A USER without a grant is refused and a granted USER can read**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json`
6. **Shared-folder responses carry no-store caching**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:51061`
7. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
8. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-front C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Checks | full check passed on 80ba6d67; on 7000ac6e jsTest (390 tests) and bootJar passed and node --check passed on every shared-folder file |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-front\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-front' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `GET http://127.0.0.1:51061/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\front_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json A:\Projects\christopherbell.dev-worktrees\style-shared-front` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `node --test website/src/test/js/back-office-shared-folder.test.js website/src/test/js/shared-folder-page-initialization.test.js website/src/test/js/shared-folder-streaming.test.js website/src/test/js/shared-folder-worker-runtime.test.js website/src/test/js/shared-folder.test.js` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:51061` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-front C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-logs` in `A:\Projects\christopherbell.dev-worktrees\style-shared-front`
- **Candidate identity:** `7000ac6`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-shared-front\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-shared-front' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:51061/actuator/health/readiness
```

### 3. The shared-folder page and every changed module are served exactly as committed

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\front_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json A:\Projects\christopherbell.dev-worktrees\style-shared-front
```

### 4. Browser-side JavaScript tests pass (node --test)

```text
node --test website/src/test/js/back-office-shared-folder.test.js website/src/test/js/shared-folder-page-initialization.test.js website/src/test/js/shared-folder-streaming.test.js website/src/test/js/shared-folder-worker-runtime.test.js website/src/test/js/shared-folder.test.js
```

### 5. A USER without a grant is refused and a granted USER can read

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json
```

### 6. Shared-folder responses carry no-store caching

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:51061
```

### 7. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 8. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-shared-front C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\i-logs
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
X-Request-Id: 84582362-3d2d-408f-ba9d-6171d025901d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791853437
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
Date: Tue, 13 Oct 2026 01:02:57 GMT
Connection: close

{"status":"UP"}
```

### 3. The shared-folder page and every changed module are served exactly as committed

```text
exit code: 0
--- stdout ---
PASS /js/shared-folder.js is served exactly as committed: 200 text/javascript 36838 bytes
PASS /js/lib/shared-folder.js is served exactly as committed: 200 text/javascript 20297 bytes
PASS /js/lib/back-office-shared-folder.js is served exactly as committed: 200 text/javascript 5406 bytes
PASS /js/lib/shared-folder-streaming.js is served exactly as committed: 200 text/javascript 3967 bytes
PASS /js/lib/shared-folder-worker-runtime.js is served exactly as committed: 200 text/javascript 884 bytes
PASS /shared-folder-auth-sw.js is served exactly as committed: 200 text/javascript 643 bytes
PASS the administrator signs in with a browser session: 200
PASS the shared-folder page renders for the signed-in administrator with its module: 200 text/html;charset=UTF-8
```

### 4. Browser-side JavaScript tests pass (node --test)

<details><summary>69 lines</summary>

```text
exit code: 0
--- stdout ---
✔ recycle pagination uses authoritative next-page state even for a terminal full page (0.8618ms)
✔ shared-folder audit markup escapes untrusted values and shows bounded event facts (11.7062ms)
✔ recycle markup exposes restore, explicit replace, and purge controls without HTML injection (0.1882ms)
✔ audit filters omit blanks and typed purge confirmation is exact (0.2932ms)
✔ invalid audit dates are omitted instead of breaking the admin filter (0.0871ms)
✔ restore replace and purge actions call only the explicitly confirmed API operation (0.2019ms)
✔ purge action rejects a mismatched phrase before calling the API (0.3294ms)
✔ actual Back Office handler wires delegation URLs methods bodies and refresh (0.3839ms)
✔ account-scoped resume storage isolates two accounts, removes legacy state unread, and resumes same-account work (1.0347ms)
✔ resume storage does not access browser state without an authenticated account identity (0.1091ms)
✔ terminal upload cleanup clears only the current account resume record (0.5254ms)
✔ page initialization unwraps the account DTO and renders entries for shared-folder READ (0.4666ms)
✔ page initialization stops before entries when the unwrapped account lacks shared-folder read (0.1504ms)
✔ folder navigation replaces only folder chrome and pushes the canonical path (0.123ms)
✔ folder navigation ignores stale responses and restores history without another push (0.1131ms)
✔ native shared-folder interception is restricted to the exact same-origin API prefix (0.9803ms)
✔ download correlation is an exact non-secret same-origin URL (0.4695ms)
✔ native denial states remain actionable (0.477ms)
✔ worker registration requires no readable credential or message staging (0.2136ms)
✔ shared-folder streaming code contains no bearer-token transport (0.97ms)
✔ cookie-authenticated native requests preserve credentials and Range headers (17.8589ms)
✔ authentication and authorization denials are reported to the initiating page (0.5353ms)
✔ a lost client does not reject the native response (0.227ms)
✔ the worker runtime never handles Bearer [REDACTED] or persistent browser storage (0.4659ms)
✔ shared-folder API paths encode each decoded relative path once (0.7494ms)
✔ shared-folder radio control delegates playback and reports an empty station safely (0.5455ms)
✔ shared-folder toolbar reports a rejected clipboard write without claiming success (0.1784ms)
✔ shared-folder toolbar reports when the clipboard API is unavailable (0.1123ms)
✔ shared-folder toolbar announces a link only after clipboard succeeds (0.1137ms)
✔ shared-folder search encodes queries and presents validated recursive results (0.3666ms)
✔ shared-folder search rejects every malformed result partition before row actions use it (0.7185ms)
✔ shared-folder search controller ignores stale results and clear restores the active folder (0.3884ms)
✔ shared-folder search controller loads the next stable page without duplicate rows (0.2823ms)
✔ search invalidates a deferred folder navigation before it can render or rewrite history (0.2402ms)
✔ search form submits, warns on an emptied active query, and clears through the DOM boundary (0.3684ms)
✔ media profiles and every public job state have clear browser text (0.2428ms)
✔ media fallback polling begins progressive playback at buffering and supports cache hits (33.362ms)
✔ media fallback polling stops on safe terminal state and disconnect (0.3017ms)
✔ progressive media remains observed after buffering and exposes terminal failure (30.5943ms)
✔ effective read access includes admins and stored write capability (0.1673ms)
✔ effective write access and resumable upload progress are explicit (0.1317ms)
✔ resume authenticates every committed server chunk and uses the configured chunk size (0.6275ms)
✔ bounded retry handles only network and 5xx failures (14.4834ms)
✔ operation gate rejects double submit and pause aborts without cancelling server state (0.2319ms)
✔ mocked browser workflow retries, chunks from server config, gates duplicates, and replaces explicitly (109.0693ms)
✔ replacement uses canonical server spelling and upload-session create is never retried (0.3867ms)
✔ case-insensitive resume still proves the committed local prefix (0.1579ms)
✔ resume revalidates the authoritative server destination before sending bytes (0.1455ms)
✔ mocked browser workflow pauses without cancel, resumes, and rejects changed local bytes (0.355ms)
✔ cancel waits for aborted append settlement and retries the normal APPENDING conflict (0.7908ms)
✔ shared-folder write API paths encode identifiers and expose resumable upload actions (0.1323ms)
✔ move payload requires an explicit observed replacement token (0.1047ms)
✔ breadcrumbs and copied links contain only internal decoded paths (0.1077ms)
✔ preview text is rendered as text and keyboard activation is explicit (0.0515ms)
✔ mobile file selection reveals the preview without moving the desktop viewport (0.0614ms)
✔ permission denial distinguishes 401 and 403 from other failures (0.046ms)
✔ file-browser presentation exposes familiar types, sizes, and folder-first ordering (11.9654ms)
✔ shared-folder shell presents an explorer layout with compact actions and responsive preview (0.9628ms)
✔ shared-folder command bar stacks before tablet controls can overflow (0.3531ms)
ℹ tests 59
ℹ suites 0
ℹ pass 59
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 295.2578
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
port 51061 listeners: 0
port 51060 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-cf74447e1d124edfb4540f0c163f55da
removed C:\Temp\cbell-jdk-09c2b914516c47e39a9bb47b7b6147dc
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
--- stderr ---
ERROR: The process with PID 24036 (child process of PID 40164) could not be terminated.
Reason: The operation attempted is not supported.

ERROR: The process with PID 43572 (child process of PID 42128) could not be terminated.
Reason: The operation attempted is not supported.

ERROR: The process with PID 40164 (child process of PID 20644) could not be terminated.
Reason: There is no running instance of the task.

ERROR: The process with PID 42128 (child process of PID 20644) could not be terminated.
Reason: There is no running instance of the task.
```

## Evidence
- Case 1 started 2026-10-12T20:02:48-05:00, took 8983 ms, candidate `7000ac6`
- Case 2 started 2026-10-12T20:02:57-05:00, took 32 ms, candidate `7000ac6`
- Case 3 started 2026-10-12T20:02:58-05:00, took 500 ms, candidate `7000ac6`
- Case 4 started 2026-10-12T20:02:58-05:00, took 328 ms, candidate `7000ac6`
- Case 5 started 2026-10-12T20:02:59-05:00, took 407 ms, candidate `7000ac6`
- Case 6 started 2026-10-12T20:02:59-05:00, took 125 ms, candidate `7000ac6`
- Case 7 started 2026-10-12T20:02:59-05:00, took 265 ms, candidate `7000ac6`
- Case 8 started 2026-10-12T20:03:00-05:00, took 4625 ms, candidate `7000ac6`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
