# Whats for Lunch models repositories and client conform to Chris Street Style: Test Report

## Story/Issue
Slice 17d of the style migration ([plan](../implementation-plans/2026-10-09-14-50-christopherbell-dev-whats-for-lunch-models-repositories-and-client-conform-to-ch.md)): restaurant storage, queries, website validation and OpenStreetMap parsing behave as before

## Branch
``claude/style-lunch-models-20261009` at candidate `cadf7aa2`` at candidate `cadf7aa`

## Pass / Fail

> [!TIP]
> 12 of 12 cases passed on candidate `cadf7aa`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | The What's for Lunch page renders | ✅ PASS | Expected status 200 and body containing "What's For Lunch" |
| 3 | Public source freshness has production's shape | ✅ PASS | Expected exit code 0 |
| 4 | Restaurant of the day has production's shape | ✅ PASS | Expected exit code 0 |
| 5 | An anonymous restaurant list gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 6 | An anonymous import status read gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 7 | An anonymous import preview is rejected (403) | ✅ PASS | Expected status 403 |
| 8 | Top-liked restaurants has production's shape | ✅ PASS | Expected exit code 0 |
| 9 | An unknown public restaurant profile gets the same status and body as production (404) | ✅ PASS | Expected exit code 0 |
| 10 | Create lunch_c through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 11 | A USER is rejected from the ADMIN inventory and duplicate previews | ✅ PASS | Expected exit code 0 |
| 12 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock)**: http `GET http://127.0.0.1:58796/actuator/health/readiness`
2. **The What's for Lunch page renders**: http `GET http://127.0.0.1:58796/wfl`
3. **Public source freshness has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json`
4. **Restaurant of the day has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json`
5. **An anonymous restaurant list gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403`
6. **An anonymous import status read gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403`
7. **An anonymous import preview is rejected (403)**: http `POST http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview`
8. **Top-liked restaurants has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json`
9. **An unknown public restaurant profile gets the same status and body as production (404)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 404`
10. **Create lunch_c through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:58796 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_c`
11. **A USER is rejected from the ADMIN inventory and duplicate previews**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_admin_reject_checks.py http://127.0.0.1:58796 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
12. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a91fccfb05174ea0a448bf543a252845/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (monthly OpenStreetMap import disabled) |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:58796, commit cadf7aa2 |
| Readiness label | case 1 names the 17a workflow beans because the shared script was written for that slice; for this slice it proves the candidate started with every bean wired |
| Credentials | one disposable USER; password generated and never recorded; token file deleted |
| Production | read-only GETs only (freshness, restaurant of the day, top-liked, unknown profile, anonymous restaurant list and import status) |
| Coverage limit | inventory paging and duplicate previews are ADMIN-only and restaurants exist only through ADMIN creation or a live import; RestaurantBoundedQueryRepositoryTest (real Mongo), OpenStreetMapRestaurantClientTest and RestaurantWebsiteUrlPolicyTest cover cursors, filters, parsing and website rules |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:58796/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `GET http://127.0.0.1:58796/wfl` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `POST http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 404` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:58796 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_c` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_admin_reject_checks.py http://127.0.0.1:58796 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a91fccfb05174ea0a448bf543a252845/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-models`
- **Candidate identity:** `cadf7aa`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token file deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock)

```http
GET http://127.0.0.1:58796/actuator/health/readiness
```

### 2. The What's for Lunch page renders

```http
GET http://127.0.0.1:58796/wfl
```

### 3. Public source freshness has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json
```

### 4. Restaurant of the day has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json
```

### 5. An anonymous restaurant list gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403
```

### 6. An anonymous import status read gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403
```

### 7. An anonymous import preview is rejected (403)

```http
POST http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview
```

### 8. Top-liked restaurants has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json
```

### 9. An unknown public restaurant profile gets the same status and body as production (404)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58796/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 404
```

### 10. Create lunch_c through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:58796 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_c
```

### 11. A USER is rejected from the ADMIN inventory and duplicate previews

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_admin_reject_checks.py http://127.0.0.1:58796 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 12. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a91fccfb05174ea0a448bf543a252845/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock)

```text
HTTP 200 
X-Request-Id: dba9e278-a4a0-4e87-b041-b71fae09472e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791576048
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
Date: Fri, 09 Oct 2026 19:59:48 GMT
Connection: close

{"status":"UP"}
```

### 2. The What's for Lunch page renders

<details><summary>84 lines</summary>

```text
HTTP 200 
X-Request-Id: a64f55c5-482e-4b93-aad5-711c7b92bef6
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791576048
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
Date: Fri, 09 Oct 2026 19:59:48 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell (cbell7@icloud.com)" />
    <meta name="keywords" content="cbell,blog" />
    
    <meta name="description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    
    <link rel="canonical" href="https://www.christopherbell.dev/wfl" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | What&#39;s For Lunch?" />
    <meta property="og:description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    <meta property="og:url" content="https://www.christopherbell.dev/wfl" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | What&#39;s For Lunch?" />
    <meta name="twitter:description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  

    <title>CB | What's For Lunch?</title>

    <link rel="stylesheet" type="text/css" href="/006e602dbdf934d741c3/css/main.css"/>
    <link rel="stylesheet" type="text/css" href="/006e602dbdf934d741c3/css/whats-for-lunch.css"/>
</head>

<body class="site-page void-shell-page lunch-page lunch-void-page">
    <div id="nav"></div>
    <main class="site-main lunch-void-main" aria-labelledby="lunchTitle">
        <div class="lunch-void-shell">
            <div class="container lunch-void-container">
                <header class="lunch-void-hero">
                    <p class="home-kicker">Decision console</p>
                    <h1 id="lunchTitle">What's For Lunch?</h1>
                    <p>Three signals. One good decision.</p>
                </header>
                <section class="lunch-void-console" aria-label="Lunch decision console">
                    <div id="whats-for-lunch"></div>
                </section>
            </div>
        </div>
    </main>
    <footer id="footer"></footer>
</body>

<script type="module" src="/006e602dbdf934d741c3/js/app.js"></script>
<script type="module" src="/006e602dbdf934d741c3/js/whats-for-lunch.js"></script>

</html>
```

</details>

### 3. Public source freshness has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 4. Restaurant of the day has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 5. An anonymous restaurant list gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2025-09-12'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2025-09-12'}
```

### 6. An anonymous import status read gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status'}
```

### 7. An anonymous import preview is rejected (403)

```text
HTTP 403 
X-Request-Id: bdb1e443-97ed-4a8a-819c-21ccd7336a5f
Set-Cookie: [REDACTED]
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 19:59:51 GMT
Connection: close

{"timestamp":"2026-10-09T19:59:51.156Z","status":403,"error":"Forbidden","path":"/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview"}
```

### 8. Top-liked restaurants has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 9. An unknown public restaurant profile gets the same status and body as production (404)

```text
exit code: 0
--- stdout ---
candidate 404 {'messages': [{'code': 'RESOURCE_NOT_FOUND', 'description': 'The requested resource was not found.'}], 'payload': None, 'requestId': None, 'success': False}
production 404 {'messages': [{'code': 'RESOURCE_NOT_FOUND', 'description': 'The requested resource was not found.'}], 'payload': None, 'requestId': None, 'success': False}
```

### 10. Create lunch_c through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
lunch_c create 201 login 200
```

### 11. A USER is rejected from the ADMIN inventory and duplicate previews

```text
exit code: 0
--- stdout ---
PASS a USER cannot page the restaurant inventory (403): got 403
PASS a USER cannot preview duplicate names (403): got 403
```

### 12. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T14:59:48-05:00, took 30 ms, candidate `cadf7aa`
- Case 2 started 2026-10-09T14:59:48-05:00, took 218 ms, candidate `cadf7aa`
- Case 3 started 2026-10-09T14:59:49-05:00, took 125 ms, candidate `cadf7aa`
- Case 4 started 2026-10-09T14:59:49-05:00, took 139 ms, candidate `cadf7aa`
- Case 5 started 2026-10-09T14:59:49-05:00, took 687 ms, candidate `cadf7aa`
- Case 6 started 2026-10-09T14:59:50-05:00, took 468 ms, candidate `cadf7aa`
- Case 7 started 2026-10-09T14:59:51-05:00, took 31 ms, candidate `cadf7aa`
- Case 8 started 2026-10-09T14:59:51-05:00, took 156 ms, candidate `cadf7aa`
- Case 9 started 2026-10-09T14:59:51-05:00, took 406 ms, candidate `cadf7aa`
- Case 10 started 2026-10-09T14:59:52-05:00, took 391 ms, candidate `cadf7aa`
- Case 11 started 2026-10-09T14:59:52-05:00, took 172 ms, candidate `cadf7aa`
- Case 12 started 2026-10-09T14:59:53-05:00, took 47 ms, candidate `cadf7aa`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
