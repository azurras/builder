# Shared folder access models maintenance and radio conform to Chris Street Style: Test Report

## Story/Issue
Slice 19a of the style migration ([plan](../implementation-plans/2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md)): access checks, maintenance passes and the radio station behave as before

## Branch
``claude/style-shared-small-20261009` at candidate `fad01421`` at candidate `fad0142`

## Pass / Fail

> [!TIP]
> 12 of 12 cases passed on candidate `fad0142`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | The shared folder page renders for anonymous visitors | ✅ PASS | Expected status 200 |
| 3 | Anonymous GET /api/shared-folder/2026-07-17/entries?path= gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 4 | Anonymous GET /api/shared-folder/2026-07-17/search?query=a gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 5 | Anonymous GET /api/shared-folder/2026-07-17/radio gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 6 | Anonymous GET /api/shared-folder/2026-07-17/content?path=a.txt gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 7 | Anonymous GET /api/shared-folder/2026-07-17/preview?path=a.txt gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 8 | Anonymous GET /api/shared-folder/2026-07-17/admin/audit gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 9 | Anonymous GET /api/shared-folder/2026-07-17/admin/recycle gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 10 | Create share_a through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 11 | A USER without a shared-folder grant is denied every read, write and admin route | ✅ PASS | Expected exit code 0 |
| 12 | Candidate log has no ERROR lines and no maintenance or radio warnings | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:57002/actuator/health/readiness`
2. **The shared folder page renders for anonymous visitors**: http `GET http://127.0.0.1:57002/shared`
3. **Anonymous GET /api/shared-folder/2026-07-17/entries?path= gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/entries?path= https://www.christopherbell.dev/api/shared-folder/2026-07-17/entries?path= 403`
4. **Anonymous GET /api/shared-folder/2026-07-17/search?query=a gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/search?query=a https://www.christopherbell.dev/api/shared-folder/2026-07-17/search?query=a 403`
5. **Anonymous GET /api/shared-folder/2026-07-17/radio gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/radio https://www.christopherbell.dev/api/shared-folder/2026-07-17/radio 403`
6. **Anonymous GET /api/shared-folder/2026-07-17/content?path=a.txt gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/content?path=a.txt https://www.christopherbell.dev/api/shared-folder/2026-07-17/content?path=a.txt 403`
7. **Anonymous GET /api/shared-folder/2026-07-17/preview?path=a.txt gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/preview?path=a.txt https://www.christopherbell.dev/api/shared-folder/2026-07-17/preview?path=a.txt 403`
8. **Anonymous GET /api/shared-folder/2026-07-17/admin/audit gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/admin/audit https://www.christopherbell.dev/api/shared-folder/2026-07-17/admin/audit 403`
9. **Anonymous GET /api/shared-folder/2026-07-17/admin/recycle gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/admin/recycle https://www.christopherbell.dev/api/shared-folder/2026-07-17/admin/recycle 403`
10. **Create share_a through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:57002 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad share_a`
11. **A USER without a shared-folder grant is denied every read, write and admin route**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/shared_user_checks.py http://127.0.0.1:57002 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
12. **Candidate log has no ERROR lines and no maintenance or radio warnings**: command `python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a06e44ba6b0c4b4caeaf8ba360a0ac8a/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or (' WARN ' in l and ('maintenance' in l.lower() or 'radio' in l.lower()))];print('matching lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:57002, commit fad01421 |
| Credentials | one disposable USER without a shared-folder grant; password generated and never recorded; token file deleted |
| Production | read-only anonymous GETs only |
| Coverage limit | granted shared-folder access needs an ADMIN or a stored grant, neither of which has a supported local path; SharedFolderRadioServiceTest, SharedFolderMaintenanceServiceTest and SharedFolderSecurityIntegrationTest cover granted behavior |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:57002/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `GET http://127.0.0.1:57002/shared` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/entries?path= https://www.christopherbell.dev/api/shared-folder/2026-07-17/entries?path= 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/search?query=a https://www.christopherbell.dev/api/shared-folder/2026-07-17/search?query=a 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/radio https://www.christopherbell.dev/api/shared-folder/2026-07-17/radio 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/content?path=a.txt https://www.christopherbell.dev/api/shared-folder/2026-07-17/content?path=a.txt 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/preview?path=a.txt https://www.christopherbell.dev/api/shared-folder/2026-07-17/preview?path=a.txt 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/admin/audit https://www.christopherbell.dev/api/shared-folder/2026-07-17/admin/audit 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/admin/recycle https://www.christopherbell.dev/api/shared-folder/2026-07-17/admin/recycle 403` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:57002 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad share_a` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/shared_user_checks.py http://127.0.0.1:57002 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Local command:** `python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a06e44ba6b0c4b4caeaf8ba360a0ac8a/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or (' WARN ' in l and ('maintenance' in l.lower() or 'radio' in l.lower()))];print('matching lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-shared-small`
- **Candidate identity:** `fad0142`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token file deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:57002/actuator/health/readiness
```

### 2. The shared folder page renders for anonymous visitors

```http
GET http://127.0.0.1:57002/shared
```

### 3. Anonymous GET /api/shared-folder/2026-07-17/entries?path= gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/entries?path= https://www.christopherbell.dev/api/shared-folder/2026-07-17/entries?path= 403
```

### 4. Anonymous GET /api/shared-folder/2026-07-17/search?query=a gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/search?query=a https://www.christopherbell.dev/api/shared-folder/2026-07-17/search?query=a 403
```

### 5. Anonymous GET /api/shared-folder/2026-07-17/radio gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/radio https://www.christopherbell.dev/api/shared-folder/2026-07-17/radio 403
```

### 6. Anonymous GET /api/shared-folder/2026-07-17/content?path=a.txt gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/content?path=a.txt https://www.christopherbell.dev/api/shared-folder/2026-07-17/content?path=a.txt 403
```

### 7. Anonymous GET /api/shared-folder/2026-07-17/preview?path=a.txt gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/preview?path=a.txt https://www.christopherbell.dev/api/shared-folder/2026-07-17/preview?path=a.txt 403
```

### 8. Anonymous GET /api/shared-folder/2026-07-17/admin/audit gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/admin/audit https://www.christopherbell.dev/api/shared-folder/2026-07-17/admin/audit 403
```

### 9. Anonymous GET /api/shared-folder/2026-07-17/admin/recycle gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:57002/api/shared-folder/2026-07-17/admin/recycle https://www.christopherbell.dev/api/shared-folder/2026-07-17/admin/recycle 403
```

### 10. Create share_a through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:57002 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad share_a
```

### 11. A USER without a shared-folder grant is denied every read, write and admin route

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/shared_user_checks.py http://127.0.0.1:57002 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 12. Candidate log has no ERROR lines and no maintenance or radio warnings

```text
python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a06e44ba6b0c4b4caeaf8ba360a0ac8a/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or (' WARN ' in l and ('maintenance' in l.lower() or 'radio' in l.lower()))];print('matching lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: c486ea0c-a82b-479b-9978-396754f7fd38
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791582191
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
Date: Fri, 09 Oct 2026 21:42:11 GMT
Connection: close

{"status":"UP"}
```

### 2. The shared folder page renders for anonymous visitors

<details><summary>124 lines</summary>

```text
HTTP 200 
X-Request-Id: 01053721-51e0-4de4-a188-2bd5b97c2290
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791582191
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/html;charset=UTF-8
Content-Language: en-US
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 21:42:11 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  
    <meta name="description" content="Private files shared through christopherbell.dev." />
    <meta name="robots" content="noindex,nofollow" />
    <link rel="canonical" href="https://www.christopherbell.dev/shared" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | Shared Folder" />
    <meta property="og:description" content="Private files shared through christopherbell.dev." />
    <meta property="og:url" content="https://www.christopherbell.dev/shared" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | Shared Folder" />
    <meta name="twitter:description" content="Private files shared through christopherbell.dev." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  
  <title>Shared Folder</title>
  <link rel="stylesheet" type="text/css" href="/ba07ef3ecb9fe0381733/css/main.css" />
  <link rel="stylesheet" type="text/css" href="/ba07ef3ecb9fe0381733/css/shared-folder.css" />
</head>
<body class="site-page void-shell-page shared-folder-page">
  <div id="nav"></div>
  <main id="shared-folder-app" class="site-main shared-folder-main d-none" data-auth-required="true" aria-labelledby="shared-folder-title">
    <header class="shared-folder-hero">
      <div class="shared-folder-heading">
        <p class="thread-label">Private files</p>
        <h1 id="shared-folder-title">Shared Folder</h1>
        <p>Browse, preview, play, and download files shared with your account.</p>
      </div>
      <p id="shared-folder-status" role="status" aria-live="polite">Checking access</p>
    </header>
    <section class="shared-folder-browser-shell">
      <div class="shared-folder-command-bar">
        <nav id="shared-breadcrumbs" class="shared-folder-breadcrumbs" aria-label="Shared folder path"></nav>
        <form id="shared-folder-search-form" class="shared-folder-search" role="search" aria-label="Search shared folder">
          <label for="shared-folder-search-query" class="visually-hidden">Search all shared files and folders</label>
          <input id="shared-folder-search-query" class="form-control" type="search" name="query" maxlength="200" autocomplete="off" placeholder="Search all files" required />
          <button class="btn btn-warning" type="submit">Search</button>
          <button id="shared-folder-search-more" class="btn btn-outline-warning" type="button" hidden disabled>Load more</button>
          <button id="shared-folder-search-clear" class="btn btn-outline-light" type="button" disabled>Clear</button>
        </form>
        <section id="shared-toolbar" class="shared-folder-toolbar" aria-label="Folder actions"></section>
      </div>
      <section id="shared-upload-panel" class="shared-folder-upload" aria-labelledby="shared-upload-title" hidden>
        <div class="shared-folder-upload-heading">
          <div>
            <p class="thread-label">Add to this folder</p>
            <h2 id="shared-upload-title" class="h5">Upload files</h2>
          </div>
          <p>Drop a file here or choose one from your computer.</p>
        </div>
        <form id="shared-upload-form">
          <label for="shared-upload-file" class="visually-hidden">Choose a file</label>
          <input id="shared-upload-file" class="form-control" type="file" required />
          <div class="shared-folder-upload-actions">
            <button class="btn btn-warning" type="submit">Upload or resume</button>
            <button id="shared-upload-pause" class="btn btn-outline-light" type="button">Pause</button>
            <button id="shared-upload-cancel" class="btn btn-outline-light" type="button" hidden>Cancel</button>
          </div>
        </form>
        <label for="shared-upload-progress" class="visually-hidden">Upload progress</label>
        <progress id="shared-upload-progress" max="100" value="0">0%</progress>
        <p id="shared-upload-detail" aria-live="polite">No upload in progress.</p>
      </section>
      <div class="shared-folder-layout">
        <section class="shared-folder-file-panel" aria-label="Folder contents">
          <div class="shared-folder-list-header" aria-hidden="true">
            <span>Name</span>
            <span>Size</span>
            <span>Modified</span>
            <span>Actions</span>
          </div>
          <section id="shared-list" class="shared-folder-list" aria-live="polite"></section>
        </section>
        <section id="shared-preview" class="shared-folder-preview" aria-label="File preview">
          <div class="shared-folder-preview-empty">
            <span class="shared-folder-preview-empty-icon" aria-hidden="true">◇</span>
            <h2>Preview</h2>
            <p>Select a file to preview it.</p>
          </div>
        </section>
      </div>
    </section>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/ba07ef3ecb9fe0381733/js/app.js"></script>
  <script type="module" src="/ba07ef3ecb9fe0381733/js/shared-folder.js"></script>
</body>
</html>
```

</details>

### 3. Anonymous GET /api/shared-folder/2026-07-17/entries?path= gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/entries'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/entries'}
```

### 4. Anonymous GET /api/shared-folder/2026-07-17/search?query=a gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/search'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/search'}
```

### 5. Anonymous GET /api/shared-folder/2026-07-17/radio gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/radio'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/radio'}
```

### 6. Anonymous GET /api/shared-folder/2026-07-17/content?path=a.txt gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/content'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/content'}
```

### 7. Anonymous GET /api/shared-folder/2026-07-17/preview?path=a.txt gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/preview'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/preview'}
```

### 8. Anonymous GET /api/shared-folder/2026-07-17/admin/audit gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/admin/audit'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/admin/audit'}
```

### 9. Anonymous GET /api/shared-folder/2026-07-17/admin/recycle gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/admin/recycle'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/shared-folder/2026-07-17/admin/recycle'}
```

### 10. Create share_a through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
share_a create 201 login 200
```

### 11. A USER without a shared-folder grant is denied every read, write and admin route

```text
exit code: 0
--- stdout ---
PASS a USER without a grant gets 403 for GET /entries?path=: 403
PASS a USER without a grant gets 403 for GET /search?query=a: 403
PASS a USER without a grant gets 403 for GET /radio: 403
PASS a USER without a grant gets 403 for POST /radio/duration: 403
PASS a USER without a grant gets 403 for POST /folders: 403
PASS a USER without a grant gets 403 for GET /admin/audit: 403
PASS a USER without a grant gets 403 for GET /admin/recycle: 403
```

### 12. Candidate log has no ERROR lines and no maintenance or radio warnings

```text
exit code: 0
--- stdout ---
matching lines: 0
```

## Evidence
- Case 1 started 2026-10-09T16:42:11-05:00, took 31 ms, candidate `fad0142`
- Case 2 started 2026-10-09T16:42:11-05:00, took 202 ms, candidate `fad0142`
- Case 3 started 2026-10-09T16:42:11-05:00, took 483 ms, candidate `fad0142`
- Case 4 started 2026-10-09T16:42:12-05:00, took 609 ms, candidate `fad0142`
- Case 5 started 2026-10-09T16:42:13-05:00, took 407 ms, candidate `fad0142`
- Case 6 started 2026-10-09T16:42:13-05:00, took 468 ms, candidate `fad0142`
- Case 7 started 2026-10-09T16:42:14-05:00, took 375 ms, candidate `fad0142`
- Case 8 started 2026-10-09T16:42:14-05:00, took 391 ms, candidate `fad0142`
- Case 9 started 2026-10-09T16:42:15-05:00, took 358 ms, candidate `fad0142`
- Case 10 started 2026-10-09T16:42:16-05:00, took 422 ms, candidate `fad0142`
- Case 11 started 2026-10-09T16:42:16-05:00, took 219 ms, candidate `fad0142`
- Case 12 started 2026-10-09T16:42:16-05:00, took 32 ms, candidate `fad0142`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
