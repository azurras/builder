# Canesboxtracker slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 10 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-21-21-christopherbell-dev-canesboxtracker-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-canes-20261006` at candidate `2173a12`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `2173a12`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (collection disabled in this profile) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | History on empty data returns the standard envelope with no weeks | ✅ PASS | Expected status 200 and body containing '"payload":{"latest":null,"weeks":[]}' |
| 3 | Candidate history envelope has the same top-level and payload keys as production | ✅ PASS | Expected exit code 0 |
| 4 | Box Index page renders and loads its script | ✅ PASS | Expected status 200 and body containing 'canes-box-tracker.js' |
| 5 | Anonymous forced collection is rejected | ✅ PASS | Expected status 403 |
| 6 | Create a disposable USER through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 7 | USER forced collection is denied (ADMIN only), so no external price API is called | ✅ PASS | Expected status 403 |
| 8 | USER manual price entry is denied (ADMIN only) | ✅ PASS | Expected status 403 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (collection disabled in this profile)**: http `GET http://127.0.0.1:51492/actuator/health/readiness`
2. **History on empty data returns the standard envelope with no weeks**: http `GET http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/history`
3. **Candidate history envelope has the same top-level and payload keys as production**: command `python -c "`
4. **Box Index page renders and loads its script**: http `GET http://127.0.0.1:51492/canes-box-tracker`
5. **Anonymous forced collection is rejected**: http `POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/collect`
6. **Create a disposable USER through the API and log in (password generated, not recorded)**: command `python permission_signup_login.py http://127.0.0.1:51492 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/canes-token.txt`
7. **USER forced collection is denied (ADMIN only), so no external price API is called**: http `POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/collect`
8. **USER manual price entry is denied (ADMIN only)**: http `POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/manual-prices`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (canes-box-tracker.enabled=false, so no external price API calls) |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:51491 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:51492, base d83f96c0 |
| Baseline | production history captured before the run (12 weeks, latest 2026-10-05, average 12.58) |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:51492/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-canes`
- **Local command:** `GET http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/history` in `A:\Projects\christopherbell.dev-worktrees\style-canes`
- **Local command:** `python -c "` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:51492/canes-box-tracker` in `A:\Projects\christopherbell.dev-worktrees\style-canes`
- **Local command:** `POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/collect` in `A:\Projects\christopherbell.dev-worktrees\style-canes`
- **Local command:** `python permission_signup_login.py http://127.0.0.1:51492 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/canes-token.txt` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/collect` in `A:\Projects\christopherbell.dev-worktrees\style-canes`
- **Local command:** `POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/manual-prices` in `A:\Projects\christopherbell.dev-worktrees\style-canes`
- **Candidate identity:** `2173a12`
- **Cleanup:** Stopped candidate PID 13300 and mongod PID 81892 by process tree; both ports have zero listeners; scratch token file deleted; production MongoDB 27017 untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (collection disabled in this profile)

```http
GET http://127.0.0.1:51492/actuator/health/readiness
```

### 2. History on empty data returns the standard envelope with no weeks

```http
GET http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/history
```

### 3. Candidate history envelope has the same top-level and payload keys as production

```text
python -c "
import json,urllib.request
c=json.loads(urllib.request.urlopen('http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/history').read()); p=json.load(open('canes-history-prod-before.json'))
print(sorted(c), sorted(c['payload'])); print(sorted(p), sorted(p['payload']))
raise SystemExit(0 if sorted(c)==sorted(p) and sorted(c['payload'])==sorted(p['payload']) else 1)"
```

### 4. Box Index page renders and loads its script

```http
GET http://127.0.0.1:51492/canes-box-tracker
```

### 5. Anonymous forced collection is rejected

```http
POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/collect
```

### 6. Create a disposable USER through the API and log in (password generated, not recorded)

```text
python permission_signup_login.py http://127.0.0.1:51492 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/canes-token.txt
```

### 7. USER forced collection is denied (ADMIN only), so no external price API is called

```http
POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/collect
Authorization: [REDACTED]
```

### 8. USER manual price entry is denied (ADMIN only)

```http
POST http://127.0.0.1:51492/api/canes-box-tracker/2026-06-04/manual-prices
Authorization: [REDACTED]
Content-Type: application/json

{"metroName":"Dallas","price":12.99,"sourceUrl":"https://example.test","note":"check"}
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (collection disabled in this profile)

```text
HTTP 200 
X-Request-Id: 2b20f071-50cf-400e-a1c3-98ec8653b3bd
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791340019
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
Date: Wed, 07 Oct 2026 02:25:59 GMT
Connection: close

{"status":"UP"}
```

### 2. History on empty data returns the standard envelope with no weeks

```text
HTTP 200 
X-Request-Id: f81e3759-349f-42fa-a993-a6b38ef7c229
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791340019
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
Date: Wed, 07 Oct 2026 02:25:59 GMT
Connection: close

{"messages":null,"payload":{"latest":null,"weeks":[]},"requestId":null,"success":true}
```

### 3. Candidate history envelope has the same top-level and payload keys as production

```text
exit code: 0
--- stdout ---
['messages', 'payload', 'requestId', 'success'] ['latest', 'weeks']
['messages', 'payload', 'requestId', 'success'] ['latest', 'weeks']
```

### 4. Box Index page renders and loads its script

<details><summary>157 lines</summary>

```text
HTTP 200 
X-Request-Id: 9379a181-bce2-47a4-8e5c-5fed582b4a3c
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791340019
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
Date: Wed, 07 Oct 2026 02:26:00 GMT
Connection: close

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="utf-8" />

  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="author" content="Christopher Bell" />

  

    <meta name="description" content="Weekly average Box Combo prices across major Raising Canes metros." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/canes-box-tracker" />



    <meta property="og:site_name" content="christopherbell.dev" />

    <meta property="og:locale" content="en_US" />

    <meta property="og:type" content="website" />

    <meta property="og:title" content="CB | Raising Canes Box Index" />

    <meta property="og:description" content="Weekly average Box Combo prices across major Raising Canes metros." />

    <meta property="og:url" content="https://www.christopherbell.dev/canes-box-tracker" />

    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:type" content="image/png" />

    <meta property="og:image:width" content="1200" />

    <meta property="og:image:height" content="630" />

    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />



    <meta name="twitter:card" content="summary_large_image" />

    <meta name="twitter:title" content="CB | Raising Canes Box Index" />

    <meta name="twitter:description" content="Weekly average Box Combo prices across major Raising Canes metros." />

    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="theme-color" content="#17202a" />

  

  <title>Raising Canes Box Index</title>

  <link rel="stylesheet" type="text/css" href="/74bd3b16fa2b25604f28/css/main.css"/>

</head>

<body class="site-page void-shell-page canes-box-tracker-page">

  <div id="nav"></div>

  <main class="site-main canes-box-main" role="main">

    <section class="canes-box-shell" aria-labelledby="canesBoxTitle">

      <div class="canes-box-container">

        <header class="canes-box-hero">

          <p class="thread-label">Chicken signal</p>

          <h1 id="canesBoxTitle">Raising Canes Box Index</h1>

          <p>Tracks verified weekly pre-tax Box Combo prices across major Raising Canes metros. Public-menu matches stay provisional until reviewed.</p>

        </header>



        <section class="canes-box-index-panel" aria-live="polite" aria-label="Raising Canes Box Index trend">

          <p class="profile-label">Pricing index</p>

          <div class="canes-box-index-grid">

            <div class="canes-box-index-card">

              <p class="profile-label">Month over month</p>

              <strong id="canesBoxMonthIndexNumber" class="canes-box-index-number canes-box-index-neutral">No MoM yet</strong>

              <span id="canesBoxMonthIndexContext">Needs a priced week near one month ago.</span>

            </div>

            <div class="canes-box-index-card">

              <p class="profile-label">Year over year</p>

              <strong id="canesBoxYearIndexNumber" class="canes-box-index-number canes-box-index-neutral">No YoY yet</strong>

              <span id="canesBoxYearIndexContext">Needs a priced week near one year ago.</span>

            </div>

          </div>

        </section>



        <section class="canes-box-panel" aria-live="polite">

          <div class="canes-box-summary">

            <div>

              <p class="profile-label">Latest average</p>

              <strong id="canesBoxLatestPrice">No data</strong>

            </div>

            <div>

              <p class="profile-label">Week</p>

              <strong id="canesBoxLatestWeek">-</strong>

            </div>

            <div>

              <p class="profile-label">Metros included</p>

              <strong id="canesBoxMetroCount">-</strong>

            </div>

            <div>

              <p class="profile-label">Verified</p>

              <strong id="canesBoxVerifiedCount">-</strong>

            </div>

            <div>

              <p class="profile-label">Provisional</p>

              <strong id="canesBoxProvisionalCount">-</strong>

            </div>

            <div>

              <p class="profile-label">Excluded</p>

              <strong id="canesBoxExcludedCount">-</strong>

            </div>

          </div>

          <div id="canesBoxAlert" class="alert alert-danger d-none mt-3" role="alert"></div>

          <div id="canesBoxChart" class="canes-box-chart" aria-label="Weekly average Box Combo price chart"></div>

        </section>



        <section class="canes-box-panel" aria-labelledby="canesBoxMetroTrendTitle">

          <div class="canes-box-result-header">

            <div>

              <p class="profile-label">Metro trend</p>

              <h2 id="canesBoxMetroTrendTitle">One Metro Signal</h2>

            </div>

          </div>

          <div id="canesBoxMetroTrendPanel">

            <p class="canes-box-empty">Select a metro from the latest samples to see its weekly trend.</p>

          </div>

        </section>



        <section class="canes-box-panel" aria-labelledby="canesBoxMetroTitle">

          <div class="canes-box-result-header">

            <div>

              <p class="profile-label">Latest metro samples</p>

              <h2 id="canesBoxMetroTitle">Tracked Stores</h2>

            </div>

          </div>

          <div class="table-responsive">

            <table class="table table-dark table-sm canes-box-table">

              <thead>

                <tr>

                  <th scope="col">Metro</th>

                  <th scope="col">Store</th>

                  <th scope="col">Price</th>

                  <th scope="col">Source</th>

                  <th scope="col">Last collected</th>

                </tr>

              </thead>

              <tbody id="canesBoxMetroRows">

                <tr><td colspan="5">Loading tracker history...</td></tr>

              </tbody>

            </table>

          </div>

        </section>

      </div>

    </section>

  </main>

  <footer id="footer"></footer>

  <script type="module" src="/74bd3b16fa2b25604f28/js/app.js"></script>

  <script type="module" src="/74bd3b16fa2b25604f28/js/canes-box-tracker.js"></script>

</body>

</html>
```

</details>

### 5. Anonymous forced collection is rejected

```text
HTTP 403 
X-Request-Id: afff0c27-ff92-4dc7-bd26-1606d4080a6a
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
Date: Wed, 07 Oct 2026 02:26:00 GMT
Connection: close

{"timestamp":"2026-10-07T02:26:00.197Z","status":403,"error":"Forbidden","path":"/api/canes-box-tracker/2026-06-04/collect"}
```

### 6. Create a disposable USER through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
create status 201 username style_check role USER
login status 200 token segments 3
```

### 7. USER forced collection is denied (ADMIN only), so no external price API is called

```text
HTTP 403 
X-Request-Id: 2d65b295-1437-4e2f-958c-ad040c4cfc89
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791340020
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
Content-Length: 121
Date: Wed, 07 Oct 2026 02:26:00 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 8. USER manual price entry is denied (ADMIN only)

```text
HTTP 403 
X-Request-Id: bba4e6f8-60d0-4d9c-9bca-0a3cde825063
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791340021
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
Content-Length: 121
Date: Wed, 07 Oct 2026 02:26:01 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

## Evidence
- Case 1 started 2026-10-06T21:25:59-05:00, took 31 ms, candidate `2173a12`
- Case 2 started 2026-10-06T21:25:59-05:00, took 46 ms, candidate `2173a12`
- Case 3 started 2026-10-06T21:25:59-05:00, took 93 ms, candidate `unknown`
- Case 4 started 2026-10-06T21:25:59-05:00, took 172 ms, candidate `2173a12`
- Case 5 started 2026-10-06T21:26:00-05:00, took 30 ms, candidate `2173a12`
- Case 6 started 2026-10-06T21:26:00-05:00, took 391 ms, candidate `unknown`
- Case 7 started 2026-10-06T21:26:00-05:00, took 62 ms, candidate `2173a12`
- Case 8 started 2026-10-06T21:26:01-05:00, took 46 ms, candidate `2173a12`

## Bugs / Follow-ups
- **Native checks on the candidate:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m58s. Canes suites: service 20/20, client 17/17, controller 6/6 and configuration 2/2. `ModularMonolithArchitectureTest` passed 5/5. JS and Pester suites passed.
- **Not exercised at runtime:**
  - Collection and admin review, because there is no local ADMIN and collection is disabled under `test`. The service and client suites cover them.
  - Reading real stored snapshots. After deploy, the production history (12 weeks) will be compared with the copy captured before this change.

## Document Status
complete

## Project
christopherbell-dev
