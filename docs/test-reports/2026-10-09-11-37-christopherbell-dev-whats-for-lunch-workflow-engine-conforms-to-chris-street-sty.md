# Whats for Lunch workflow engine conforms to Chris Street Style: Test Report

## Story/Issue
Slice 17a of the style migration ([plan](../implementation-plans/2026-10-09-11-31-christopherbell-dev-whats-for-lunch-workflow-engine-conforms-to-chris-street-sty.md)): the workflow beans start with the application Clock and What's for Lunch serves as before

## Branch
``claude/style-lunch-workflow-20261009` at candidate `26f4e20d`` at candidate `26f4e20`

## Pass / Fail

> [!TIP]
> 7 of 7 cases passed on candidate `26f4e20`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | The What's for Lunch page renders | ✅ PASS | Expected status 200 and body containing "What's For Lunch" |
| 3 | Public source freshness has production's shape | ✅ PASS | Expected exit code 0 |
| 4 | Restaurant of the day has production's shape | ✅ PASS | Expected exit code 0 |
| 5 | An anonymous restaurant list gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 6 | An anonymous import status read gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 7 | An anonymous import preview is rejected (403) | ✅ PASS | Expected status 403 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock)**: http `GET http://127.0.0.1:58557/actuator/health/readiness`
2. **The What's for Lunch page renders**: http `GET http://127.0.0.1:58557/wfl`
3. **Public source freshness has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json`
4. **Restaurant of the day has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json`
5. **An anonymous restaurant list gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403`
6. **An anonymous import status read gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403`
7. **An anonymous import preview is rejected (403)**: http `POST http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (monthly OpenStreetMap import disabled, so no remote call) |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:58557, commit 26f4e20d |
| Startup log | no ERROR lines |
| Production | read-only GETs only (freshness, restaurant of the day, anonymous restaurant list, anonymous import status) |
| Coverage limit | the workflow package has no route or job; WorkflowExecutorTest and WhatsForLunchWorkflowTest cover its behavior, and startup proves the Clock wiring |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:58557/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Local command:** `GET http://127.0.0.1:58557/wfl` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Local command:** `POST http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-workflow`
- **Candidate identity:** `26f4e20`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock)

```http
GET http://127.0.0.1:58557/actuator/health/readiness
```

### 2. The What's for Lunch page renders

```http
GET http://127.0.0.1:58557/wfl
```

### 3. Public source freshness has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json
```

### 4. Restaurant of the day has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json
```

### 5. An anonymous restaurant list gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403
```

### 6. An anonymous import status read gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403
```

### 7. An anonymous import preview is rejected (403)

```http
POST http://127.0.0.1:58557/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (every component, including the workflow beans, constructed from the application Clock)

```text
HTTP 200 
X-Request-Id: 57f0758b-8f70-4386-9386-e97e58a61b00
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791563919
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
Date: Fri, 09 Oct 2026 16:37:39 GMT
Connection: close

{"status":"UP"}
```

### 2. The What's for Lunch page renders

<details><summary>84 lines</summary>

```text
HTTP 200 
X-Request-Id: ca11647e-8d9e-4381-ba5d-5789cacf4c6a
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791563919
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
Date: Fri, 09 Oct 2026 16:37:39 GMT
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

    <link rel="stylesheet" type="text/css" href="/4bde45fabdcee234ef25/css/main.css"/>
    <link rel="stylesheet" type="text/css" href="/4bde45fabdcee234ef25/css/whats-for-lunch.css"/>
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

<script type="module" src="/4bde45fabdcee234ef25/js/app.js"></script>
<script type="module" src="/4bde45fabdcee234ef25/js/whats-for-lunch.js"></script>

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
X-Request-Id: 4c3156c2-1d35-4f0f-8ae6-0c9bbc080daf
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
Date: Fri, 09 Oct 2026 16:37:41 GMT
Connection: close

{"timestamp":"2026-10-09T16:37:41.375Z","status":403,"error":"Forbidden","path":"/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview"}
```

## Evidence
- Case 1 started 2026-10-09T11:37:39-05:00, took 30 ms, candidate `26f4e20`
- Case 2 started 2026-10-09T11:37:39-05:00, took 172 ms, candidate `26f4e20`
- Case 3 started 2026-10-09T11:37:39-05:00, took 108 ms, candidate `26f4e20`
- Case 4 started 2026-10-09T11:37:40-05:00, took 125 ms, candidate `26f4e20`
- Case 5 started 2026-10-09T11:37:40-05:00, took 422 ms, candidate `26f4e20`
- Case 6 started 2026-10-09T11:37:40-05:00, took 327 ms, candidate `26f4e20`
- Case 7 started 2026-10-09T11:37:41-05:00, took 47 ms, candidate `26f4e20`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
