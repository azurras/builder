# Browser JavaScript branches and loops are braced: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-20-06-christopherbell-dev-browser-javascript-branches-and-loops-are-braced.md): every changed browser file is served as committed, the main pages render anonymously and for the administrator, and all JavaScript tests pass.

## Branch
`claude/style-browser-js-20261012` at candidate `738e55c`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `738e55c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root | ✅ PASS | Expected exit code 0 |
| 2 | The candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 3 | Changed browser files are served as committed and the main pages render anonymously and for the administrator | ✅ PASS | Expected exit code 0 |
| 4 | Browser-side JavaScript tests pass (node --test, all files) | ✅ PASS | Expected exit code 0 |
| 5 | A USER without a grant is refused and a granted USER can read | ✅ PASS | Expected exit code 0 |
| 6 | Shared-folder responses carry no-store caching | ✅ PASS | Expected exit code 0 |
| 7 | The candidate log has no ERROR line and no administrator password | ✅ PASS | Expected exit code 0 |
| 8 | Stop-Candidate stops the candidate and removes the root with the credential file | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root**: command `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-browser-js\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-browser-js' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"`
2. **The candidate reports readiness UP**: http `GET http://127.0.0.1:57742/actuator/health/readiness`
3. **Changed browser files are served as committed and the main pages render anonymously and for the administrator**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\browser_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json A:\Projects\christopherbell.dev-worktrees\style-browser-js origin/main`
4. **Browser-side JavaScript tests pass (node --test, all files)**: command `bash -c "node --test website/src/test/js/*.test.js"`
5. **A USER without a grant is refused and a granted USER can read**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json`
6. **Shared-folder responses carry no-store caching**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:57742`
7. **The candidate log has no ERROR line and no administrator password**: command `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"`
8. **Stop-Candidate stops the candidate and removes the root with the credential file**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-browser-js C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-logs`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| Candidate options | -WithTestAdministrator -EnableSharedFolder |
| Full check | passed on 738e55c9 including jsTest |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-browser-js\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-browser-js' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `GET http://127.0.0.1:57742/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\browser_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json A:\Projects\christopherbell.dev-worktrees\style-browser-js origin/main` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `bash -c "node --test website/src/test/js/*.test.js"` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:57742` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-browser-js C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-logs` in `A:\Projects\christopherbell.dev-worktrees\style-browser-js`
- **Candidate identity:** `738e55c`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and the disposable root and JDK socket directory were removed; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Start-Candidate -WithTestAdministrator -EnableSharedFolder starts an isolated candidate whose credential file lives in the disposable root

```text
pwsh -NoLogo -NoProfile -Command "& 'A:\Projects\christopherbell.dev-worktrees\style-browser-js\ops\local\Start-Candidate.ps1' -StateFile 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' -Checkout 'A:\Projects\christopherbell.dev-worktrees\style-browser-js' -WithTestAdministrator -EnableSharedFolder | Out-Null; $s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' | ConvertFrom-Json; \"ready=$($s.ready) db=$($s.databaseName) credentialFileInRoot=$($s.testAdministratorFile.StartsWith($s.testMongoRoot))\"; if (-not ($s.ready -and $s.databaseName -eq 'test' -and $s.testAdministratorFile.StartsWith($s.testMongoRoot))) { exit 1 }"
```

### 2. The candidate reports readiness UP

```http
GET http://127.0.0.1:57742/actuator/health/readiness
```

### 3. Changed browser files are served as committed and the main pages render anonymously and for the administrator

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\browser_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json A:\Projects\christopherbell.dev-worktrees\style-browser-js origin/main
```

### 4. Browser-side JavaScript tests pass (node --test, all files)

```text
bash -c "node --test website/src/test/js/*.test.js"
```

### 5. A USER without a grant is refused and a granted USER can read

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s2_admin_checks.py C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json
```

### 6. Shared-folder responses carry no-store caching

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\shared_nostore_check.py http://127.0.0.1:57742
```

### 7. The candidate log has no ERROR line and no administrator password

```text
pwsh -NoLogo -NoProfile -Command "$s = Get-Content -Raw 'C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json' | ConvertFrom-Json; $a = Get-Content -Raw $s.testAdministratorFile | ConvertFrom-Json; $log = Get-Content -Raw $s.candidateLog; $created = $log.Contains('Created test administrator candidate-admin'); $leak = $log.Contains($a.password); $errors = @(Select-String -LiteralPath $s.candidateLog -CaseSensitive -Pattern '^\S+\s+ERROR\s').Count; \"created=$created passwordInLog=$leak errorLines=$errors\"; if (-not $created -or $leak -or $errors) { exit 1 }"
```

### 8. Stop-Candidate stops the candidate and removes the root with the credential file

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\style-browser-js C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\j-logs
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
X-Request-Id: 23676cae-e70d-4c82-a05f-4ff61a724888
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791854586
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
Date: Tue, 13 Oct 2026 01:22:06 GMT
Connection: close

{"status":"UP"}
```

### 3. Changed browser files are served as committed and the main pages render anonymously and for the administrator

```text
exit code: 0
--- stdout ---
PASS all 53 changed static files are served exactly as committed: all identical
PASS every main page answers an anonymous visitor without a server error: {'/': 200, '/void': 200, '/void/explore': 200, '/messages': 200, '/notifications': 200, '/profile': 200, '/wfl/top-rated': 200, '/wfl': 200, '/survive': 200, '/music': 200, '/vin-decoder': 200, '/canes-box-tracker': 200, '/site-monitor': 200, '/back-office': 200, '/command-center': 200, '/zip-coordinates': 200}
PASS the administrator signs in with a browser session: 200
PASS every main page renders for the signed-in administrator: {'/': 200, '/void': 200, '/void/explore': 200, '/messages': 200, '/notifications': 200, '/profile': 200, '/wfl/top-rated': 200, '/wfl': 200, '/survive': 200, '/music': 200, '/vin-decoder': 200, '/canes-box-tracker': 200, '/site-monitor': 200, '/back-office': 200, '/command-center': 200, '/zip-coordinates': 200}
```

### 4. Browser-side JavaScript tests pass (node --test, all files)

<details><summary>600 lines</summary>

```text
exit code: 0
--- stdout ---
TAP version 13
# Subtest: main stylesheet includes visible focus states for Void controls
ok 1 - main stylesheet includes visible focus states for Void controls
  ---
  duration_ms: 20.489535
  type: 'test'
  ...
# Subtest: Cane’s index cards stack into a shrinkable column on mobile
ok 2 - Cane’s index cards stack into a shrinkable column on mobile
  ---
  duration_ms: 9.403257
  type: 'test'
  ...
# Subtest: post template exposes thread controls as a labelled group
ok 3 - post template exposes thread controls as a labelled group
  ---
  duration_ms: 5.189925
  type: 'test'
  ...
# Subtest: image lightbox keeps keyboard behavior in its module
ok 4 - image lightbox keeps keyboard behavior in its module
  ---
  duration_ms: 2.759483
  type: 'test'
  ...
# Subtest: command center shell exposes labelled regions and an accessible action dialog
ok 5 - command center shell exposes labelled regions and an accessible action dialog
  ---
  duration_ms: 10.76951
  type: 'test'
  ...
# Subtest: back office links admins to the dedicated command center
ok 6 - back office links admins to the dedicated command center
  ---
  duration_ms: 6.765017
  type: 'test'
  ...
# Subtest: WFL decision console is labelled, non-ranked, and keyboard visible
ok 7 - WFL decision console is labelled, non-ranked, and keyboard visible
  ---
  duration_ms: 17.194217
  type: 'test'
  ...
# Subtest: restaurant profile uses the accessible Void profile shell
ok 8 - restaurant profile uses the accessible Void profile shell
  ---
  duration_ms: 7.12441
  type: 'test'
  ...
# Subtest: WFL list vote controls are scoped, wrapping, and keyboard visible
ok 9 - WFL list vote controls are scoped, wrapping, and keyboard visible
  ---
  duration_ms: 13.640516
  type: 'test'
  ...
# Subtest: back office Music permissions expose labelled read and write controls
ok 10 - back office Music permissions expose labelled read and write controls
  ---
  duration_ms: 4.868668
  type: 'test'
  ...
# Subtest: Void Explore exposes five independently labelled live regions
ok 11 - Void Explore exposes five independently labelled live regions
  ---
  duration_ms: 7.552028
  type: 'test'
  ...
# Subtest: every button declares its intended type explicitly
ok 12 - every button declares its intended type explicitly
  ---
  duration_ms: 54.429391
  type: 'test'
  ...
# Subtest: The Bell archive pages expose one main landmark and one page heading
ok 13 - The Bell archive pages expose one main landmark and one page heading
  ---
  duration_ms: 9.248146
  type: 'test'
  ...
# Subtest: authentication forms provide stable names and autocomplete purposes
ok 14 - authentication forms provide stable names and autocomplete purposes
  ---
  duration_ms: 15.682327
  type: 'test'
  ...
# Subtest: static graph counts cycles once and excludes dynamic imports
ok 15 - static graph counts cycles once and excludes dynamic imports
  ---
  duration_ms: 15.322992
  type: 'test'
  ...
# Subtest: lightweight routes keep the app static graph within 86,434 raw bytes
ok 16 - lightweight routes keep the app static graph within 86,434 raw bytes
  ---
  duration_ms: 58.06607
  type: 'test'
  ...
# Subtest: audit page URL sends stable pagination and nonblank filters
ok 17 - audit page URL sends stable pagination and nonblank filters
  ---
  duration_ms: 2.079662
  type: 'test'
  ...
# Subtest: audit page parser and navigation enforce authoritative bounds
ok 18 - audit page parser and navigation enforce authoritative bounds
  ---
  duration_ms: 3.010485
  type: 'test'
  ...
# Subtest: moderation audit summary exposes only allowlisted state and a bounded reason
ok 19 - moderation audit summary exposes only allowlisted state and a bounded reason
  ---
  duration_ms: 0.491813
  type: 'test'
  ...
# Subtest: canes box index operation markup summarizes a forced pull
ok 20 - canes box index operation markup summarizes a forced pull
  ---
  duration_ms: 1.831634
  type: 'test'
  ...
# Subtest: canes box index operation markup handles missing averages
ok 21 - canes box index operation markup handles missing averages
  ---
  duration_ms: 0.251519
  type: 'test'
  ...
# Subtest: denied Music access markup escapes account and IP values
ok 22 - denied Music access markup escapes account and IP values
  ---
  duration_ms: 14.837678
  type: 'test'
  ...
# Subtest: denied Music access markup has a useful empty state
ok 23 - denied Music access markup has a useful empty state
  ---
  duration_ms: 0.182087
  type: 'test'
  ...
# Subtest: report queue URL sends only bounded nonblank filters
ok 24 - report queue URL sends only bounded nonblank filters
  ---
  duration_ms: 2.39799
  type: 'test'
  ...
# Subtest: report page parser copies items and rejects malformed totals
ok 25 - report page parser copies items and rejects malformed totals
  ---
  duration_ms: 2.109667
  type: 'test'
  ...
# Subtest: report page navigation uses exact server bounds
ok 26 - report page navigation uses exact server bounds
  ---
  duration_ms: 0.322075
  type: 'test'
  ...
# Subtest: recycle pagination uses authoritative next-page state even for a terminal full page
ok 27 - recycle pagination uses authoritative next-page state even for a terminal full page
  ---
  duration_ms: 2.472337
  type: 'test'
  ...
# Subtest: shared-folder audit markup escapes untrusted values and shows bounded event facts
ok 28 - shared-folder audit markup escapes untrusted values and shows bounded event facts
  ---
  duration_ms: 14.015038
  type: 'test'
  ...
# Subtest: recycle markup exposes restore, explicit replace, and purge controls without HTML injection
ok 29 - recycle markup exposes restore, explicit replace, and purge controls without HTML injection
  ---
  duration_ms: 0.36713
  type: 'test'
  ...
# Subtest: audit filters omit blanks and typed purge confirmation is exact
ok 30 - audit filters omit blanks and typed purge confirmation is exact
  ---
  duration_ms: 0.556971
  type: 'test'
  ...
# Subtest: invalid audit dates are omitted instead of breaking the admin filter
ok 31 - invalid audit dates are omitted instead of breaking the admin filter
  ---
  duration_ms: 0.210817
  type: 'test'
  ...
# Subtest: restore replace and purge actions call only the explicitly confirmed API operation
ok 32 - restore replace and purge actions call only the explicitly confirmed API operation
  ---
  duration_ms: 0.580674
  type: 'test'
  ...
# Subtest: purge action rejects a mismatched phrase before calling the API
ok 33 - purge action rejects a mismatched phrase before calling the API
  ---
  duration_ms: 0.799991
  type: 'test'
  ...
# Subtest: actual Back Office handler wires delegation URLs methods bodies and refresh
ok 34 - actual Back Office handler wires delegation URLs methods bodies and refresh
  ---
  duration_ms: 0.789841
  type: 'test'
  ...
# Subtest: admin account URL sends bounded paging and filter controls
ok 35 - admin account URL sends bounded paging and filter controls
  ---
  duration_ms: 2.166032
  type: 'test'
  ...
# Subtest: admin account page parser validates the network boundary and copies items
ok 36 - admin account page parser validates the network boundary and copies items
  ---
  duration_ms: 1.60536
  type: 'test'
  ...
# Subtest: admin account navigation reflects exact page bounds
ok 37 - admin account navigation reflects exact page bounds
  ---
  duration_ms: 0.218118
  type: 'test'
  ...
# Subtest: role promotion options only move users to higher-privilege roles
ok 38 - role promotion options only move users to higher-privilege roles
  ---
  duration_ms: 0.238546
  type: 'test'
  ...
# Subtest: promotion action parser refuses demotion actions
ok 39 - promotion action parser refuses demotion actions
  ---
  duration_ms: 0.28271
  type: 'test'
  ...
# Subtest: shared-folder controls keep write dependent on read
ok 40 - shared-folder controls keep write dependent on read
  ---
  duration_ms: 0.222225
  type: 'test'
  ...
# Subtest: shared-folder controls preserve default ADMIN access as checked and disabled
ok 41 - shared-folder controls preserve default ADMIN access as checked and disabled
  ---
  duration_ms: 0.178399
  type: 'test'
  ...
# Subtest: music controls preserve unrelated grants and keep write dependent on read
ok 42 - music controls preserve unrelated grants and keep write dependent on read
  ---
  duration_ms: 0.235685
  type: 'test'
  ...
# Subtest: music controls preserve default ADMIN access as checked and disabled
ok 43 - music controls preserve default ADMIN access as checked and disabled
  ---
  duration_ms: 0.331529
  type: 'test'
  ...
# Subtest: empty post list renders an explicit Blog empty state
ok 44 - empty post list renders an explicit Blog empty state
  ---
  duration_ms: 2.283958
  type: 'test'
  ...
# Subtest: configured post content continues to render as literal text
ok 45 - configured post content continues to render as literal text
  ---
  duration_ms: 0.332433
  type: 'test'
  ...
# Subtest: browser authentication uses only the non-secret cookie marker
ok 46 - browser authentication uses only the non-secret cookie marker
  ---
  duration_ms: 2.530877
  type: 'test'
  ...
# Subtest: unsafe JSON requests send same-origin cookies and the CSRF token
ok 47 - unsafe JSON requests send same-origin cookies and the CSRF token
  ---
  duration_ms: 58.166618
  type: 'test'
  ...
# Subtest: a stale readable marker is rejected by the server session boundary
ok 48 - a stale readable marker is rejected by the server session boundary
  ---
  duration_ms: 5.01136
  type: 'test'
  ...
# Subtest: formatUsd renders prices and empty state labels
ok 49 - formatUsd renders prices and empty state labels
  ---
  duration_ms: 2.596146
  type: 'test'
  ...
# Subtest: canesBoxChartPoints maps priced weeks into SVG coordinates
ok 50 - canesBoxChartPoints maps priced weeks into SVG coordinates
  ---
  duration_ms: 0.526666
  type: 'test'
  ...
# Subtest: canesBoxChartMarkup renders an empty state without prices
ok 51 - canesBoxChartMarkup renders an empty state without prices
  ---
  duration_ms: 0.333696
  type: 'test'
  ...
# Subtest: canesBoxIndexTrend calculates higher and lower percentage movement
ok 52 - canesBoxIndexTrend calculates higher and lower percentage movement
  ---
  duration_ms: 1.719303
  type: 'test'
  ...
# Subtest: canesBoxPeriodTrend calculates month over month from closest priced week
ok 53 - canesBoxPeriodTrend calculates month over month from closest priced week
  ---
  duration_ms: 0.761964
  type: 'test'
  ...
# Subtest: formatPeriodTrendContext identifies the latest priced and comparison weeks
ok 54 - formatPeriodTrendContext identifies the latest priced and comparison weeks
  ---
  duration_ms: 0.459359
  type: 'test'
  ...
# Subtest: canesBoxPeriodTrends calculates month over month and year over year
ok 55 - canesBoxPeriodTrends calculates month over month and year over year
  ---
  duration_ms: 0.493677
  type: 'test'
  ...
# Subtest: canesBoxPeriodTrend returns null without enough history for the period
ok 56 - canesBoxPeriodTrend returns null without enough history for the period
  ---
  duration_ms: 0.209389
  type: 'test'
  ...
# Subtest: formatIndexTrend renders signed percentages and empty states
ok 57 - formatIndexTrend renders signed percentages and empty states
  ---
  duration_ms: 0.585173
  type: 'test'
  ...
# Subtest: formatQualityStatus labels quality states for public readers
ok 58 - formatQualityStatus labels quality states for public readers
  ---
  duration_ms: 0.571629
  type: 'test'
  ...
# Subtest: formatCollectedDate renders stable collection date labels
ok 59 - formatCollectedDate renders stable collection date labels
  ---
  duration_ms: 0.532291
  type: 'test'
  ...
# Subtest: canesBoxOfficialApiCurl renders a reproducible official menu request for a metro store
ok 60 - canesBoxOfficialApiCurl renders a reproducible official menu request for a metro store
  ---
  duration_ms: 0.406284
  type: 'test'
  ...
# Subtest: Cane’s curl copy reports when the clipboard API is unavailable
ok 61 - Cane’s curl copy reports when the clipboard API is unavailable
  ---
  duration_ms: 0.391465
  type: 'test'
  ...
# Subtest: Cane’s curl copy reports rejected clipboard writes
ok 62 - Cane’s curl copy reports rejected clipboard writes
  ---
  duration_ms: 0.441577
  type: 'test'
  ...
# Subtest: Cane’s curl copy confirms success and restores the original button label
ok 63 - Cane’s curl copy confirms success and restores the original button label
  ---
  duration_ms: 0.25043
  type: 'test'
  ...
# Subtest: canesBoxMetroRowsMarkup renders source and last collection date without quality or status columns
ok 64 - canesBoxMetroRowsMarkup renders source and last collection date without quality or status columns
  ---
  duration_ms: 0.809401
  type: 'test'
  ...
# Subtest: canesBoxMetroTrend returns verified priced weeks for one metro
ok 65 - canesBoxMetroTrend returns verified priced weeks for one metro
  ---
  duration_ms: 0.721204
  type: 'test'
  ...
# Subtest: canesBoxMetroTrendMarkup renders metro-only trend content
ok 66 - canesBoxMetroTrendMarkup renders metro-only trend content
  ---
  duration_ms: 0.666001
  type: 'test'
  ...
# Subtest: command center API contract uses the five fixed protected paths
ok 67 - command center API contract uses the five fixed protected paths
  ---
  duration_ms: 3.256038
  type: 'test'
  ...
# Subtest: security exposes only the data-free page shell, never command center APIs
ok 68 - security exposes only the data-free page shell, never command center APIs
  ---
  duration_ms: 12.237347
  type: 'test'
  ...
# Subtest: metric display distinguishes unavailable and stale readings
ok 69 - metric display distinguishes unavailable and stale readings
  ---
  duration_ms: 14.757159
  type: 'test'
  ...
# Subtest: metric display formats service state, start timestamps, and commit identifiers
ok 70 - metric display formats service state, start timestamps, and commit identifiers
  ---
  duration_ms: 0.634244
  type: 'test'
  ...
# Subtest: commit display keeps the unavailable fallback when detail is absent
ok 71 - commit display keeps the unavailable fallback when detail is absent
  ---
  duration_ms: 0.388165
  type: 'test'
  ...
# Subtest: commit display only shortens safe commit identifiers
ok 72 - commit display only shortens safe commit identifiers
  ---
  duration_ms: 0.767738
  type: 'test'
  ...
# Subtest: commit cards suppress duplicate detail and retain the full accessible title
ok 73 - commit cards suppress duplicate detail and retain the full accessible title
  ---
  duration_ms: 1.039378
  type: 'test'
  ...
# Subtest: metric card renderer uses pure detail and accessible title rules
ok 74 - metric card renderer uses pure detail and accessible title rules
  ---
  duration_ms: 4.409381
  type: 'test'
  ...
# Subtest: metric display compacts byte values for fixed-width command cards
ok 75 - metric display compacts byte values for fixed-width command cards
  ---
  duration_ms: 0.804594
  type: 'test'
  ...
# Subtest: metric display formats uptime as seconds, minutes, hours, and days
ok 76 - metric display formats uptime as seconds, minutes, hours, and days
  ---
  duration_ms: 0.571452
  type: 'test'
  ...
# Subtest: metric cards reserve a full row for values and wrap exceptional text
ok 77 - metric cards reserve a full row for values and wrap exceptional text
  ---
  duration_ms: 4.11687
  type: 'test'
  ...
# Subtest: polling uses five seconds then bounded 10, 20, and 30 second backoff
ok 78 - polling uses five seconds then bounded 10, 20, and 30 second backoff
  ---
  duration_ms: 0.353473
  type: 'test'
  ...
# Subtest: polling pauses for hidden tabs or explicit log pause
ok 79 - polling pauses for hidden tabs or explicit log pause
  ---
  duration_ms: 0.198827
  type: 'test'
  ...
# Subtest: poll requests start once, queue behind one in-flight request, or stop when inactive
ok 80 - poll requests start once, queue behind one in-flight request, or stop when inactive
  ---
  duration_ms: 0.216658
  type: 'test'
  ...
# Subtest: stale polling generations and request cursors cannot apply log pages
ok 81 - stale polling generations and request cursors cannot apply log pages
  ---
  duration_ms: 0.320223
  type: 'test'
  ...
# Subtest: log page state honors empty cursors and rejects same-cursor duplicate batches
ok 82 - log page state honors empty cursors and rejects same-cursor duplicate batches
  ---
  duration_ms: 0.239718
  type: 'test'
  ...
# Subtest: visible log copy preserves each row as exact plain text separated by newlines
ok 83 - visible log copy preserves each row as exact plain text separated by newlines
  ---
  duration_ms: 0.374983
  type: 'test'
  ...
# Subtest: only unauthorized and forbidden request errors revoke command center access
ok 84 - only unauthorized and forbidden request errors revoke command center access
  ---
  duration_ms: 0.257329
  type: 'test'
  ...
# Subtest: access loss revokes even when the failed poll generation became stale
ok 85 - access loss revokes even when the failed poll generation became stale
  ---
  duration_ms: 0.235275
  type: 'test'
  ...
# Subtest: fetchJson preserves forbidden HTTP status for access revocation
ok 86 - fetchJson preserves forbidden HTTP status for access revocation
  ---
  duration_ms: 1.295946
  type: 'test'
  ...
# Subtest: dangerous actions require exact fixed phrases
ok 87 - dangerous actions require exact fixed phrases
  ---
  duration_ms: 0.192295
  type: 'test'
  ...
# Subtest: dialog cleanup clears every sensitive and status field
ok 88 - dialog cleanup clears every sensitive and status field
  ---
  duration_ms: 0.400814
  type: 'test'
  ...
# Subtest: pending action countdown is bounded at zero and reports cancellability
ok 89 - pending action countdown is bounded at zero and reports cancellability
  ---
  duration_ms: 0.373565
  type: 'test'
  ...
# Subtest: page orchestration inserts log records as text and clears passwords
ok 90 - page orchestration inserts log records as text and clears passwords
  ---
  duration_ms: 5.484562
  type: 'test'
  ...
# Subtest: composerPreviewModel trims empty text and reports remaining characters
ok 91 - composerPreviewModel trims empty text and reports remaining characters
  ---
  duration_ms: 1.816041
  type: 'test'
  ...
# Subtest: composerPreviewModel detects over-limit drafts
ok 92 - composerPreviewModel detects over-limit drafts
  ---
  duration_ms: 0.192657
  type: 'test'
  ...
# Subtest: composerPreviewMarkup links mentions and renders supported rich embeds
ok 93 - composerPreviewMarkup links mentions and renders supported rich embeds
  ---
  duration_ms: 2.058101
  type: 'test'
  ...
# Subtest: composerPreviewMarkup renders a quiet empty state
ok 94 - composerPreviewMarkup renders a quiet empty state
  ---
  duration_ms: 0.193844
  type: 'test'
  ...
# Subtest: composerPreviewMarkup escapes malicious draft text before innerHTML injection
ok 95 - composerPreviewMarkup escapes malicious draft text before innerHTML injection
  ---
  duration_ms: 0.343364
  type: 'test'
  ...
# Subtest: composerPreviewMarkup escapes URL attribute breakout attempts
ok 96 - composerPreviewMarkup escapes URL attribute breakout attempts
  ---
  duration_ms: 0.680458
  type: 'test'
  ...
# Subtest: feature-only selectors have one dedicated stylesheet owner
ok 97 - feature-only selectors have one dedicated stylesheet owner
  ---
  duration_ms: 10.202826
  type: 'test'
  ...
# Subtest: feature templates link their versioned dedicated stylesheets
ok 98 - feature templates link their versioned dedicated stylesheets
  ---
  duration_ms: 33.270556
  type: 'test'
  ...
# Subtest: command center preserves the shared Void shell cascade
ok 99 - command center preserves the shared Void shell cascade
  ---
  duration_ms: 5.083464
  type: 'test'
  ...
# Subtest: stylesheet ownership documentation names every split feature file
ok 100 - stylesheet ownership documentat
... [61545 more characters not recorded]
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
port 57742 listeners: 0
port 57741 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-8290720897b9450d9b56f78cb7cfbcea
removed C:\Temp\cbell-jdk-bbc64dc60f64432abae80a7350191bae
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

## Evidence
- Case 1 started 2026-10-12T20:21:56-05:00, took 9500 ms, candidate `738e55c`
- Case 2 started 2026-10-12T20:22:06-05:00, took 30 ms, candidate `738e55c`
- Case 3 started 2026-10-12T20:22:06-05:00, took 952 ms, candidate `738e55c`
- Case 4 started 2026-10-12T20:22:07-05:00, took 3608 ms, candidate `738e55c`
- Case 5 started 2026-10-12T20:22:11-05:00, took 421 ms, candidate `738e55c`
- Case 6 started 2026-10-12T20:22:11-05:00, took 109 ms, candidate `738e55c`
- Case 7 started 2026-10-12T20:22:12-05:00, took 265 ms, candidate `738e55c`
- Case 8 started 2026-10-12T20:22:12-05:00, took 5828 ms, candidate `738e55c`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
