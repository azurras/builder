# Back Office JavaScript slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 15b of the style migration ([plan](../implementation-plans/2026-10-09-11-10-christopherbell-dev-back-office-javascript-slice-conforms-to-chris-street-style.md)): the Back Office page and its modules are served and the page script loads and gates as before

## Branch
`claude/style-back-office-20261009` at candidate `0332f5c`

## Pass / Fail

> [!TIP]
> 11 of 11 cases passed on candidate `0332f5c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | The Back Office page is served with its module script | ✅ PASS | Expected status 200 and body containing '/js/back-office.js' |
| 3 | back-office.js is served with the shared capability path | ✅ PASS | Expected status 200 and body containing 'function handleCapabilityPermissionChange(target, family) {' |
| 4 | back-office.js is served with the shared pager | ✅ PASS | Expected status 200 and body containing 'function wirePager({ previous, next, getQuery, setQuery, totalPages, refresh, noun }) {' |
| 5 | The new paging module is served | ✅ PASS | Expected status 200 and body containing 'export function parseServerPage(payload, invalidMessage) {' |
| 6 | The activity module imports the paging module | ✅ PASS | Expected status 200 and body containing "from './back-office-paging.js'" |
| 7 | The reports module imports the paging module | ✅ PASS | Expected status 200 and body containing "from './back-office-paging.js'" |
| 8 | The Music access module uses util.sanitize | ✅ PASS | Expected status 200 and body containing "import { sanitize } from './util.js';" |
| 9 | The shared-folder module uses util.sanitize | ✅ PASS | Expected status 200 and body containing "import { sanitize } from './util.js';" |
| 10 | The users module is served | ✅ PASS | Expected status 200 and body containing 'export function musicPermissionState' |
| 11 | The canes module is served | ✅ PASS | Expected status 200 and body containing 'export function canesBoxIndexResultMarkup' |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:57431/actuator/health/readiness`
2. **The Back Office page is served with its module script**: http `GET http://127.0.0.1:57431/back-office`
3. **back-office.js is served with the shared capability path**: http `GET http://127.0.0.1:57431/js/back-office.js`
4. **back-office.js is served with the shared pager**: http `GET http://127.0.0.1:57431/js/back-office.js`
5. **The new paging module is served**: http `GET http://127.0.0.1:57431/js/lib/back-office-paging.js`
6. **The activity module imports the paging module**: http `GET http://127.0.0.1:57431/js/lib/back-office-activity.js`
7. **The reports module imports the paging module**: http `GET http://127.0.0.1:57431/js/lib/back-office-reports.js`
8. **The Music access module uses util.sanitize**: http `GET http://127.0.0.1:57431/js/lib/back-office-music.js`
9. **The shared-folder module uses util.sanitize**: http `GET http://127.0.0.1:57431/js/lib/back-office-shared-folder.js`
10. **The users module is served**: http `GET http://127.0.0.1:57431/js/lib/back-office-users.js`
11. **The canes module is served**: http `GET http://127.0.0.1:57431/js/lib/back-office-canes-box-index.js`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:57430 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:57431, commit 0332f5c6, built by the clean --rerun-tasks full check |
| Browser check (built-in browser, recorded by hand, not by record_run) | an anonymous visit to /back-office ran the page script and redirected to /404, so the whole module graph including back-office-paging.js loaded; the only console error was the 404 status of /404 itself. A disposable USER bo_user, created and signed in with the app's cookie-mode login and a password generated in the page and never displayed, then loaded /back-office: the script fetched /api/accounts/2025-09-03/me (200) and redirected to /404 because the role is not ADMIN |
| Coverage limit | the admin dashboard needs an ADMIN, which has no supported local path; its modules are covered by the six Back Office test files and the full 390-test JavaScript suite |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:57431/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/back-office` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/back-office.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/back-office.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-paging.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-activity.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-reports.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-music.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-shared-folder.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-users.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Local command:** `GET http://127.0.0.1:57431/js/lib/back-office-canes-box-index.js` in `A:\Projects\christopherbell.dev-worktrees\style-back-office`
- **Candidate identity:** `0332f5c`
- **Cleanup:** Browser tab closed; candidate and mongod stopped; both ports have no listeners; production mongod on 27017 untouched

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:57431/actuator/health/readiness
```

### 2. The Back Office page is served with its module script

```http
GET http://127.0.0.1:57431/back-office
```

### 3. back-office.js is served with the shared capability path

```http
GET http://127.0.0.1:57431/js/back-office.js
```

### 4. back-office.js is served with the shared pager

```http
GET http://127.0.0.1:57431/js/back-office.js
```

### 5. The new paging module is served

```http
GET http://127.0.0.1:57431/js/lib/back-office-paging.js
```

### 6. The activity module imports the paging module

```http
GET http://127.0.0.1:57431/js/lib/back-office-activity.js
```

### 7. The reports module imports the paging module

```http
GET http://127.0.0.1:57431/js/lib/back-office-reports.js
```

### 8. The Music access module uses util.sanitize

```http
GET http://127.0.0.1:57431/js/lib/back-office-music.js
```

### 9. The shared-folder module uses util.sanitize

```http
GET http://127.0.0.1:57431/js/lib/back-office-shared-folder.js
```

### 10. The users module is served

```http
GET http://127.0.0.1:57431/js/lib/back-office-users.js
```

### 11. The canes module is served

```http
GET http://127.0.0.1:57431/js/lib/back-office-canes-box-index.js
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 8a81e412-3a4c-4596-aa1a-44eeb78ea455
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562233
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
Date: Fri, 09 Oct 2026 16:09:33 GMT
Connection: close

{"status":"UP"}
```

### 2. The Back Office page is served with its module script

<details><summary>329 lines</summary>

```text
HTTP 200 
X-Request-Id: fa9b5685-823f-4e43-a67a-748b56450410
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562233
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
Date: Fri, 09 Oct 2026 16:09:33 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  
    <meta name="description" content="Administrative tools for christopherbell.dev." />
    <meta name="robots" content="noindex,nofollow" />
    <link rel="canonical" href="https://www.christopherbell.dev/back-office" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | Back Office" />
    <meta property="og:description" content="Administrative tools for christopherbell.dev." />
    <meta property="og:url" content="https://www.christopherbell.dev/back-office" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | Back Office" />
    <meta name="twitter:description" content="Administrative tools for christopherbell.dev." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  
  <title>Back Office</title>
  <link rel="stylesheet" type="text/css" href="/12cd331559535d861fa5/css/main.css"/>
</head>
<body class="site-page back-office">
  <div id="nav"></div>
  <main class="site-main d-none" id="backOfficeContent" role="main">
    <section class="site-hero site-hero-office" aria-labelledby="officeTitle">
      <div class="container-fluid">
        <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
          <div>
            <p class="home-kicker">Admin</p>
            <h1 id="officeTitle">Back Office</h1>
            <p>Reports, users, and operational cleanup.</p>
          </div>
          <div class="d-flex align-items-center gap-2">
            <a class="btn btn-outline-light" href="/command-center">Command Center</a>
            <span class="badge text-bg-light">ADMIN</span>
          </div>
        </div>
      </div>
    </section>
    <section class="site-content back-office-content">
      <div class="container-fluid">
        <div id="backOfficeAlert" class="alert alert-danger d-none" role="alert"></div>
        <div class="admin-metrics" aria-label="Back office summary">
          <article class="admin-metric">
            <span>Total Reports</span>
            <strong id="metricTotalReports">—</strong>
          </article>
          <article class="admin-metric metric-open">
            <span>Open Reports</span>
            <strong id="metricOpenReports">—</strong>
          </article>
          <article class="admin-metric metric-pending">
            <span>Inactive Users</span>
            <strong id="metricInactiveUsers">—</strong>
          </article>
          <article class="admin-metric metric-suspended">
            <span>Suspended Users</span>
            <strong id="metricSuspendedUsers">—</strong>
          </article>
          <article class="admin-metric">
            <span>Recent Activity</span>
            <strong id="metricRecentActivity">—</strong>
          </article>
        </div>

        <div class="admin-dashboard-grid">
          <section class="admin-workspace" aria-label="Work queues">
            <ul class="nav nav-pills back-office-nav mb-3" id="backOfficeTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="tab-reports" data-bs-toggle="pill" data-bs-target="#panel-reports" type="button" role="tab">Reports</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab-users" data-bs-toggle="pill" data-bs-target="#panel-users" type="button" role="tab">Users</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab-operations" data-bs-toggle="pill" data-bs-target="#panel-operations" type="button" role="tab">Operations</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab-shared-folder" data-bs-toggle="pill" data-bs-target="#panel-shared-folder" type="button" role="tab">Shared Folder</button>
              </li>
            </ul>
            <div class="tab-content">
              <div class="tab-pane fade show active" id="panel-reports" role="tabpanel">
                <div class="queue-panel">
                  <div class="queue-panel-header">
                    <div>
                      <p class="home-kicker mb-1">Moderation</p>
                      <h2>Report Queue</h2>
                    </div>
                    <span class="queue-count" id="reportQueueCount">—</span>
                  </div>
                  <form id="reportFilters" class="admin-filter-bar" aria-label="Filter reports">
                    <label><span>Status</span><select class="form-select" name="status">
                      <option value="">All statuses</option><option value="OPEN">Open</option><option value="RESOLVED">Resolved</option>
                    </select></label>
                    <label><span>Report type</span><select class="form-select" name="reportType">
                      <option value="">All types</option><option value="SPAM">Spam</option><option value="HARASSMENT">Harassment</option><option value="VIOLENCE">Violence</option><option value="SEXUAL">Sexual</option><option value="COPYRIGHT">Copyright</option><option value="OTHER">Other</option>
                    </select></label>
                    <label><span>Target</span><select class="form-select" name="targetType">
                      <option value="">All targets</option><option value="POST">Post</option>
                    </select></label>
                    <label><span>Reporter</span><input class="form-control" name="reporter" maxlength="100" placeholder="Username"></label>
                    <label><span>From</span><input class="form-control" type="datetime-local" name="from"></label>
                    <label><span>To</span><input class="form-control" type="datetime-local" name="to"></label>
                    <button class="btn btn-primary align-self-end" type="submit">Apply filters</button>
                  </form>
                  <div id="reportQueue" class="queue-list" aria-live="polite"></div>
                  <nav class="queue-pagination" aria-label="Report pages">
                    <button class="btn btn-outline-secondary" id="reportPrevious" type="button">Previous</button>
                    <span id="reportPage" aria-live="polite">Page 0 of 0</span>
                    <button class="btn btn-outline-secondary" id="reportNext" type="button">Next</button>
                  </nav>
                </div>
              </div>
              <div class="tab-pane fade" id="panel-users" role="tabpanel">
                <div class="queue-panel">
                  <div class="queue-panel-header">
                    <div>
                      <p class="home-kicker mb-1">Accounts</p>
                      <h2>User Queue</h2>
                    </div>
                    <span class="queue-count" id="userQueueCount">—</span>
                  </div>
                  <form id="userFilters" class="admin-filter-bar" aria-label="Filter accounts">
                    <label>
                      <span>Search</span>
                      <input class="form-control" type="search" name="text" maxlength="100"
                             placeholder="Name, username, or email">
                    </label>
                    <label>
                      <span>Status</span>
                      <select class="form-select" name="status">
                        <option value="">All statuses</option>
                        <option value="ACTIVE">Active</option>
                        <option value="INACTIVE">Inactive</option>
                        <option value="SUSPENDED">Suspended</option>
                      </select>
                    </label>
                    <label>
                      <span>Role</span>
                      <select class="form-select" name="role">
                        <option value="">All roles</option>
                        <option value="USER">User</option>
                        <option value="MOD">Moderator</option>
                        <option value="ADMIN">Admin</option>
                      </select>
                    </label>
                    <label>
                      <span>Sort</span>
                      <select class="form-select" name="sort">
                        <option value="createdOn">Created</option>
                        <option value="lastUpdatedOn">Last updated</option>
                        <option value="username">Username</option>
                        <option value="email">Email</option>
                        <option value="status">Status</option>
                        <option value="role">Role</option>
                      </select>
                    </label>
                    <label>
                      <span>Direction</span>
                      <select class="form-select" name="direction">
                        <option value="desc">Descending</option>
                        <option value="asc">Ascending</option>
                      </select>
                    </label>
                    <button class="btn btn-primary align-self-end" type="submit">Apply filters</button>
                  </form>
                  <div id="userQueue" class="queue-list" aria-live="polite"></div>
                  <nav class="queue-pagination" aria-label="Account pages">
                    <button class="btn btn-outline-secondary" id="userPrevious" type="button">Previous</button>
                    <span id="userPage" aria-live="polite">Page 0 of 0</span>
                    <button class="btn btn-outline-secondary" id="userNext" type="button">Next</button>
                  </nav>
                </div>
              </div>
              <div class="tab-pane fade" id="panel-operations" role="tabpanel">
                <div class="operations-grid" id="operationsPanel" aria-live="polite">
                  <section class="operation-panel" aria-labelledby="wflToolsTitle">
                    <div class="queue-panel-header">
                      <div>
                        <p class="home-kicker mb-1">What's For Lunch</p>
                        <h2 id="wflToolsTitle">Restaurant Data</h2>
                      </div>
                    </div>
                    <div class="operation-actions">
                      <button type="button" class="btn btn-primary operation-button" data-operation="wfl-import">Import Restaurants</button>
                      <button type="button" class="btn btn-outline-secondary operation-button" data-operation="wfl-dedupe">Remove Duplicate Names</button>
                      <button type="button" class="btn btn-outline-secondary operation-button" data-operation="wfl-load">Refresh Counts</button>
                    </div>
                    <form id="wflInventoryFilters" class="operation-form mt-3">
                      <label>
                        <span>Name</span>
                        <input class="form-control" name="name" placeholder="Restaurant name">
                      </label>
                      <label>
                        <span>City</span>
                        <input class="form-control" name="city" placeholder="City">
                      </label>
                      <label>
                        <span>State</span>
                        <input class="form-control" name="state" maxlength="32" placeholder="State">
                      </label>
                      <button class="btn btn-outline-primary align-self-end" type="submit">Search inventory</button>
                    </form>
                    <div id="wflInventory" class="queue-list mt-3" aria-live="polite"></div>
                    <button id="wflInventoryMore" class="btn btn-outline-secondary mt-2 d-none" type="button">Load more</button>
                    <div id="wflOperationStatus" class="operation-result">Restaurant counts have not been loaded yet.</div>
                  </section>

                  <section class="operation-panel" aria-labelledby="locationToolsTitle">
                    <div class="queue-panel-header">
                      <div>
                        <p class="home-kicker mb-1">Location</p>
                        <h2 id="locationToolsTitle">ZIP Coordinate Data</h2>
                      </div>
                    </div>
                    <div class="operation-actions">
                      <button type="button" class="btn btn-primary operation-button" data-operation="location-zip-import">Import ZIP Coordinates</button>
                    </div>
                    <div id="locationOperationStatus" class="operation-result">Census ZIP coordinates have not been imported in this session.</div>
                  </section>

                  <section class="operation-panel" aria-labelledby="canesBoxIndexToolsTitle">
                    <div class="queue-panel-header">
                      <div>
                        <p class="home-kicker mb-1">Raising Canes</p>
                        <h2 id="canesBoxIndexToolsTitle">Box Index Data</h2>
                      </div>
                    </div>
                    <div class="operation-actions">
                      <button type="button" class="btn btn-primary operation-button" data-operation="canes-box-index-collect">Pull New Data Point</button>
                    </div>
                    <form class="operation-form mt-3" id="canesBoxManualPriceForm">
                      <label class="form-label" for="canesBoxManualMetro">Manual Verified Price</label>
                      <div class="row g-2">
                        <div class="col-md-4">
                          <input class="form-control" id="canesBoxManualMetro" name="metroName" autocomplete="off" placeholder="Metro name" required />
                        </div>
                        <div class="col-md-2">
                          <input class="form-control" name="price" inputmode="decimal" placeholder="12.99" required />
                        </div>
                        <div class="col-md-4">
                          <input class="form-control" name="sourceUrl" inputmode="url" placeholder="Evidence URL" required />
                        </div>
                        <div class="col-md-2">
                          <button class="btn btn-outline-light w-100" type="submit">Save</button>
                        </div>
                      </div>
                      <textarea class="form-control mt-2" name="note" rows="2" placeholder="Verification note"></textarea>
                    </form>
                    <div id="canesBoxIndexOperationStatus" class="operation-result">Raising Canes Box Index has not been pulled in this session.</div>
                  </section>

                  <section class="operation-panel" aria-labelledby="vehicleToolsTitle">
                    <div class="queue-panel-header">
                      <div>
                        <p class="home-kicker mb-1">Vehicles</p>
                        <h2 id="vehicleToolsTitle">VIN Data</h2>
                      </div>
                    </div>
                    <form class="operation-form" id="vehicleVinForm">
                      <label class="form-label" for="vehicleVinInput">Create Vehicle From VIN</label>
                      <div class="input-group">
                        <input class="form-control" id="vehicleVinInput" name="vin" autocomplete="off" maxlength="17" placeholder="17-character VIN" />
                        <button class="btn btn-primary" type="submit">Create Vehicle From VIN</button>
                      </div>
                    </form>
                    <form class="operation-form" id="vehicleVinBatchForm">
                      <label class="form-label" for="vehicleVinBatchInput">Create Vehicles From VINs</label>
                      <textarea class="form-control" id="vehicleVinBatchInput" name="vins" rows="4" placeholder="One VIN per line"></textarea>
                      <button class="btn btn-outline-primary mt-2" type="submit">Create Vehicles From VINs</button>
                    </form>
                    <div class="operation-actions">
                      <button type="button" class="btn btn-outline-secondary operation-button" data-operation="vehicle-state">Refresh Data State</button>
                      <button type="button" class="btn btn-outline-secondary operation-button" data-operation="vehicle-load">Refresh Vehicle Count</button>
                    </div>
                    <div id="vehicleOperationStatus" class="operation-result">Vehicle state has not been loaded yet.</div>
                  </section>

                  <section class="operation-panel" aria-labelledby="contentToolsTitle">
                    <div class="queue-panel-header">
                      <div>
                        <p class="home-kicker mb-1">Content</p>
                        <h2 id="contentToolsTitle">Admin Reads</h2>
                      </div>
                    </div>
                    <div class="operation-actions">
                      <button type="button" class="btn btn-outline-secondary operation-button" data-operation="blog-load">Load Blog Posts</button>
                    </div>
                    <div id="contentOperationStatus" class="operation-result">Content data has not been loaded yet.</div>
                  </section>
                </div>
              </div>
              <div class="tab-pane fade" id="panel-shared-folder" role="tabpanel">
      
... [8414 more characters not recorded]
```

</details>

### 3. back-office.js is served with the shared capability path

<details><summary>516 lines</summary>

```text
HTTP 200 
X-Request-Id: 0cbc8beb-7596-46f7-8b75-dc9ccdb1ea89
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562233
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 51193
Date: Fri, 09 Oct 2026 16:09:33 GMT
Connection: close

/**
 * Back Office access guard + admin dashboard.
 */
import { API } from './lib/api.js';
import { canesBoxIndexResultMarkup } from './lib/back-office-canes-box-index.js';
import { renderAlert } from './lib/status-message.js';
import {
  accountPageNavigation,
  parseAdminAccountPage,
  promotedRoleForAction,
  rolePromotionOptions,
  musicPermissionState,
  sharedFolderPermissionState,
} from './lib/back-office-users.js';
import {
  createSharedRecycleActionHandler,
  sharedAuditFilters,
  sharedAuditMarkup,
  sharedRecyclePagination,
  sharedRecycleButton,
  sharedRecycleMarkup,
} from './lib/back-office-shared-folder.js';
import {
  parseReportPage,
  reportFilterValue,
  reportPageNavigation,
} from './lib/back-office-reports.js';
import {
  activityFilterValue,
  activityPageNavigation,
  moderationActivitySummary,
  moderationReasonValue,
  parseActivityPage,
} from './lib/back-office-activity.js';
import { musicAccessAttemptMarkup } from './lib/back-office-music.js';
import { authHeaders, fetchJson, formatWhen, isLoggedIn, sanitize } from './lib/util.js';

const content = document.getElementById('backOfficeContent');
const alertBox = document.getElementById('backOfficeAlert');
const reportQueue = document.getElementById('reportQueue');
const reportFilters = document.getElementById('reportFilters');
const reportPrevious = document.getElementById('reportPrevious');
const reportNext = document.getElementById('reportNext');
const reportPage = document.getElementById('reportPage');
const userQueue = document.getElementById('userQueue');
const userFilters = document.getElementById('userFilters');
const userPrevious = document.getElementById('userPrevious');
const userNext = document.getElementById('userNext');
const userPage = document.getElementById('userPage');
const activityList = document.getElementById('activityList');
const activityFilters = document.getElementById('activityFilters');
const activityPrevious = document.getElementById('activityPrevious');
const activityNext = document.getElementById('activityNext');
const activityPage = document.getElementById('activityPage');
const drawer = document.getElementById('backOfficeDrawer');
const drawerBody = document.getElementById('drawerBody');
const drawerClose = document.getElementById('drawerClose');
const drawerKicker = document.getElementById('drawerKicker');
const drawerTitle = document.getElementById('drawerTitle');
const sharedFolderPermissionsTemplate = document.getElementById('sharedFolderPermissionsTemplate');
const musicPermissionsTemplate = document.getElementById('musicPermissionsTemplate');
const wflOperationStatus = document.getElementById('wflOperationStatus');
const wflInventoryFilters = document.getElementById('wflInventoryFilters');
const wflInventory = document.getElementById('wflInventory');
const wflInventoryMore = document.getElementById('wflInventoryMore');
const canesBoxIndexOperationStatus = document.getElementById('canesBoxIndexOperationStatus');
const canesBoxManualPriceForm = document.getElementById('canesBoxManualPriceForm');
const locationOperationStatus = document.getElementById('locationOperationStatus');
const vehicleOperationStatus = document.getElementById('vehicleOperationStatus');
const contentOperationStatus = document.getElementById('contentOperationStatus');
const vehicleVinForm = document.getElementById('vehicleVinForm');
const vehicleVinBatchForm = document.getElementById('vehicleVinBatchForm');
const sharedAuditForm = document.getElementById('sharedAuditFilters');
const sharedAuditList = document.getElementById('sharedAuditList');
const sharedRecycleList = document.getElementById('sharedRecycleList');
const sharedRecyclePrevious = document.getElementById('sharedRecyclePrevious');
const sharedRecycleNext = document.getElementById('sharedRecycleNext');
const sharedRecyclePage = document.getElementById('sharedRecyclePage');
const musicAccessAuditList = document.getElementById('musicAccessAuditList');

/** The account capability pairs edited from the user drawer. */
const CAPABILITY_FAMILIES = Object.freeze({
  sharedFolder: Object.freeze({
    hostId: 'sharedFolderPermissions',
    template: sharedFolderPermissionsTemplate,
    dataAttribute: 'shared-folder-permission',
    datasetKey: 'sharedFolderPermission',
    stateOf: sharedFolderPermissionState,
    updateUrl: API.accounts.updateSharedFolderPermissions,
    failureMessage: 'Failed to update shared-folder permissions.',
  }),
  music: Object.freeze({
    hostId: 'musicPermissions',
    template: musicPermissionsTemplate,
    dataAttribute: 'music-permission',
    datasetKey: 'musicPermission',
    stateOf: musicPermissionState,
    updateUrl: API.accounts.updateMusicPermissions,
    failureMessage: 'Failed to update Music permissions.',
  }),
});

let accounts = [];
let accountQuery = {
  page: 0,
  size: 25,
  sort: 'createdOn',
  direction: 'desc',
  status: '',
  role: '',
  text: '',
};
let accountPageState = {
  page: 0,
  size: 25,
  totalElements: 0,
  totalPages: 0,
  sort: 'createdOn',
  direction: 'DESC',
};
let reports = [];
let reportQuery = {
  page: 0,
  size: 25,
  status: '',
  reportType: '',
  targetType: '',
  reporter: '',
  from: '',
  to: '',
};
let reportPageState = { page: 0, size: 25, totalElements: 0, totalPages: 0 };
let activities = [];
let activityQuery = {
  page: 0,
  size: 25,
  action: '',
  targetType: '',
  actor: '',
  from: '',
  to: '',
};
let activityPageState = { page: 0, size: 25, totalElements: 0, totalPages: 0 };
let restaurants = [];
let restaurantInventoryQuery = { name: '', city: '', state: '', cursor: '', size: 25 };
let restaurantInventoryNextCursor = '';
let restaurantInventoryTotal = 0;
let duplicatePreviewCursor = '';
let vehicles = [];
let blogPosts = [];
let sharedAuditEvents = [];
let sharedRecycleItems = [];
let sharedRecyclePageNumber = 0;
let sharedRecycleHasNext = false;

function showAlert(message) {
  renderAlert(alertBox, message);
}

function clearAlert() {
  alertBox?.classList.add('d-none');
}

function setLoading() {
  renderState(reportQueue, 'Loading reports…');
  renderState(userQueue, 'Loading users…');
  renderState(activityList, 'Loading activity…');
  renderOperationResult(wflOperationStatus, 'Restaurant counts have not been loaded yet.');
  renderOperationResult(canesBoxIndexOperationStatus, 'Raising Canes Box Index has not been pulled in this session.');
  renderOperationResult(locationOperationStatus, 'Census ZIP coordinates have not been imported in this session.');
  renderOperationResult(vehicleOperationStatus, 'Vehicle state has not been loaded yet.');
  renderOperationResult(contentOperationStatus, 'Content data has not been loaded yet.');
  renderState(sharedAuditList, 'Loading shared-folder audit…');
  renderState(sharedRecycleList, 'Loading recycle items…');
  renderState(musicAccessAuditList, 'Loading denied Music access…');
}

function renderState(container, message) {
  if (!container) return;
  container.innerHTML = `<div class="empty-state">${sanitize(message)}</div>`;
}

function renderOperationResult(container, markup, tone = 'neutral') {
  if (!container) return;
  container.className = `operation-result operation-${tone}`;
  container.innerHTML = markup;
}

function statusClass(status) {
  const value = (status || '').toLowerCase();
  if (value === 'open') return 'status-open';
  if (value === 'resolved' || value === 'active') return 'status-resolved';
  if (value === 'suspended') return 'status-suspended';
  if (value === 'inactive') return 'status-pending';
  return 'status-neutral';
}

function reportSeverityClass(report) {
  if ((report.status || 'OPEN') === 'RESOLVED') return 'queue-resolved';
  const reason = (report.reason || '').toLowerCase();
  if (['harassment', 'violence', 'sexual'].includes(reason)) return 'queue-severe';
  return 'queue-open';
}

function userSeverityClass(account) {
  if ((account.status || '').toUpperCase() === 'SUSPENDED') return 'queue-suspended';
  if ((account.status || '').toUpperCase() === 'INACTIVE') return 'queue-pending';
  return 'queue-resolved';
}

function relativeAge(value) {
  if (!value) return '—';
  const seconds = Math.max(1, Math.floor((Date.now() - new Date(value).getTime()) / 1000));
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function fullName(account) {
  return [account.firstName, account.lastName].filter(Boolean).join(' ');
}

function renderMetrics() {
  const totalReports = reportPageState.totalElements;
  const openReports = reports.filter(report => (report.status || 'OPEN') === 'OPEN').length;
  const inactiveUsers = accounts.filter(
      account => (account.status || '').toUpperCase() === 'INACTIVE').length;
  const suspendedUsers = accounts.filter(account => (account.status || '').toUpperCase() === 'SUSPENDED').length;
  const metrics = {
    metricTotalReports: totalReports,
    metricOpenReports: openReports,
    metricInactiveUsers: inactiveUsers,
    metricSuspendedUsers: suspendedUsers,
    metricRecentActivity: activityPageState.totalElements,
    reportQueueCount: `${totalReports} total`,
    userQueueCount: `${accountPageState.totalElements} total`,
  };

  Object.entries(metrics).forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value);
  });
}

function renderReports() {
  if (!reportQueue) return;
  if (!reports.length) {
    renderState(reportQueue, 'No reports yet. The queue is clear.');
    return;
  }

  reportQueue.innerHTML = reports.map(report => {
    const status = report.status || 'OPEN';
    const reason = report.reason || 'other';
    const postText = sanitize(report.postText || 'No post text available.');
    return `
      <article class="queue-card ${reportSeverityClass(report)}" data-detail-type="report" data-id="${sanitize(report.id || '')}" tabindex="0">
        <div class="queue-main">
          <div class="queue-topline">
            <span class="status-pill ${statusClass(status)}">${sanitize(status)}</span>
            <span class="queue-age">${relativeAge(report.createdOn)}</span>
          </div>
          <h3>${sanitize(reason)}</h3>
          <p>${postText}</p>
          <div class="queue-meta">
            <span>Reporter @${sanitize(report.reporterUsername || 'unknown')}</span>
            <span>Reported @${sanitize(report.reportedUsername || 'unknown')}</span>
            <span>${sanitize(repeatReportSummary(report))}</span>
          </div>
        </div>
        <div class="queue-actions">
          ${reportActionSelect(report)}
        </div>
      </article>
    `;
  }).join('');
}

function reportActionSelect(report) {
  const status = report.status || 'OPEN';
  const options = status === 'OPEN'
      ? `
        <option value="CLOSE_NO_ACTION">Close</option>
        <option value="DELETE_POST">Delete post</option>
        <option value="DELETE_POST_AND_SUSPEND_USER">Delete + suspend</option>
      `
      : '<option value="REOPEN">Reopen</option>';

  return `
    <select class="form-select form-select-sm report-action" data-report="${sanitize(report.id || '')}" aria-label="Report action">
      <option value="" selected>Action…</option>
      ${options}
    </select>
  `;
}

function repeatReportSummary(report) {
  const open = report.openReportsForAccount ?? 0;
  const resolved = report.resolvedReportsForAccount ?? 0;
  return `${open} open / ${resolved} resolved reports for account`;
}

function renderUsers() {
  if (!userQueue) return;
  if (!accounts.length) {
    renderState(userQueue, 'No accounts found.');
    return;
  }

  userQueue.innerHTML = accounts.map(account => {
    const status = account.status || 'UNKNOWN';
    const name = fullName(account);
    return `
      <article class="queue-card ${userSeverityClass(account)}" data-detail-type="user" data-id="${sanitize(account.id || '')}" tabindex="0">
        <div class="queue-main">
          <div class="queue-topline">
            <span class="status-pill ${statusClass(status)}">${sanitize(status)}</span>
            <span class="queue-age">${account.createdOn ? `Joined ${relativeAge(account.createdOn)}` : 'No creation date'}</span>
          </div>
          <h3>@${sanitize(account.username || 'unknown')}</h3>
          <p>${sanitize(name || account.email || 'No profile details')}</p>
          <div class="queue-meta">
            <span>${sanitize(account.role || 'USER')}</span>
          </div>
        </div>
        <div class="queue-actions">
          ${userActionSelect(account)}
        </div>
      </article>
    `;
  }).join('');
}

function applyReportPage(payload) {
  const parsed = parseReportPage(payload);
  reports = parsed.items;
  reportPageState = {
    page: parsed.page,
    size: parsed.size,
    totalElements: parsed.totalElements,
    totalPages: parsed.totalPages,
  };
}

function renderReportNavigation() {
  const state = reportPageNavigation(reportPageState);
  if (reportPrevious) reportPrevious.disabled = state.previousDisabled;
  if (reportNext) reportNext.disabled = state.nextDisabled;
  if (reportPage) reportPage.textContent = state.label;
}

function renderUserNavigation() {
  const state = accountPageNavigation(accountPageState);
  if (userPrevious) userPrevious.disabled = state.previousDisabled;
  if (userNext) userNext.disabled = state.nextDisabled;
  if (userPage) userPage.textContent = state.label;
}

function applyActivityPage(payload) {
  const parsed = parseActivityPage(payload);
  activities = parsed.items;
  activityPageState = {
    page: parsed.page,
    size: parsed.size,
    totalElements: parsed.totalElements,
    totalPages: parsed.totalPages,
  };
}

function renderActivityNavigation() {
  const state = activityPageNavigation(activityPageState);
  if (activityPrevious) activityPrevious.disabled = state.previousDisabled;
  if (activityNext) activityNext.disabled = state.nextDisabled;
  if (activityPage) activityPage.textContent = state.label;
}

function applyAccountPage(payload) {
  const parsed = parseAdminAccountPage(payload);
  accounts = parsed.items;
  accountPageState = {
    page: parsed.page,
    size: parsed.size,
    totalElements: parsed.totalElements,
    totalPages: parsed.totalPages,
    sort: parsed.sort,
    direction: parsed.direction,
  };
}

function userActionSelect(account) {
  const status = (account.status || '').toUpperCase();
  const options = [];
  rolePromotionOptions(account).forEach(option => {
    options.push(`<option value="${sanitize(option.value)}">${sanitize(option.label)}</option>`);
  });
  if (status !== 'SUSPENDED') {
    options.push('<option value="SUSPEND">Suspend</option>');
  }
  if (status !== 'ACTIVE') {
    options.push('<option value="ACTIVATE">Activate</option>');
  }
  if (!options.length) {
    return '<span class="queue-age">No actions</span>';
  }
  return `
    <select class="form-select form-select-sm user-action" data-account="${sanitize(account.id || '')}" aria-label="User action">
      <option value="" selected>Action…</option>
      ${options.join('')}
    </select>
  `;
}

function renderActivity() {
  if (!activityList) return;
  if (!activities.length) {
    renderState(activityList, 'No admin activity recorded yet.');
    return;
  }

  activityList.innerHTML = activities.map(activity => {
    const audit = moderationActivitySummary(activity);
    return `
      <article class="activity-item">
        <div class="activity-dot ${activityClass(activity.action)}"></div>
        <div>
          <strong>${sanitize(activity.message || activity.action || 'Activity')}</strong>
          ${audit.reason ? `<span><b>Reason:</b> ${sanitize(audit.reason)}</span>` : ''}
          ${audit.transition ? `<span>${sanitize(audit.transition)}</span>` : ''}
          <span>${activity.createdOn ? formatWhen(activity.createdOn) : '—'}</span>
        </div>
      </article>
    `;
  }).join('');
}

function activityClass(action) {
  if (action === 'USER_SUSPENDED') return 'activity-danger';
  if (action === 'POST_DELETED') return 'activity-warning';
  if (action === 'REPORT_RESOLVED') return 'activity-success';
  return 'activity-neutral';
}

function openDrawer(type, id) {
  const item = type === 'report'
      ? reports.find(report => report.id === id)
      : accounts.find(account => account.id === id);
  if (!item || !drawer || !drawerBody || !drawerTitle || !drawerKicker) return;

  drawerKicker.textContent = type === 'report' ? 'Report Details' : 'User Details';
  drawerTitle.textContent = type === 'report'
      ? `${item.reason || 'Report'}`
      : `@${item.username || 'user'}`;
  drawerBody.innerHTML = type === 'report' ? reportDetails(item) : userDetails(item);
  if (type === 'user') {
    renderCapabilityPermissions(item, CAPABILITY_FAMILIES.sharedFolder);
    renderCapabilityPermissions(item, CAPABILITY_FAMILIES.music);
  }
  drawer.classList.remove('d-none');
  drawer.setAttribute('aria-hidden', 'false');
}

function closeDrawer() {
  drawer?.classList.add('d-none');
  drawer?.setAttribute('aria-hidden', 'true');
}

function detailRow(label, value) {
  return `
    <div class="detail-row">
      <span>${sanitize(label)}</span>
      <strong>${sanitize(value || '—')}</strong>
    </div>
  `;
}

function reportDetails(report) {
  return `
    <div class="detail-section">
      ${detailRow('Status', report.status || 'OPEN')}
      ${detailRow('Reason', report.reason)}
      ${detailRow('Reporter', `@${report.reporterUsername || 'unknown'}`)}
      ${detailRow('Reported', `@${report.reportedUsername || 'unknown'}`)}
      ${detailRow('Open reports for account', report.openReportsForAccount ?? 0)}
      ${detailRow('Resolved reports for account', report.resolvedReportsForAccount ?? 0)}
      ${detailRow('Created', report.createdOn ? formatWhen(report.createdOn) : '—')}
      ${detailRow('Resolved', report.resolvedOn ? formatWhen(report.resolvedOn) : '—')}
      ${detailRow('Resolution', report.resolution)}
    </div>
    <div class="detail-section">
      <span class="detail-label">Post</span>
      <p class="detail-copy">${sanitize(report.postText || 'No p
... [32328 more characters not recorded]
```

</details>

### 4. back-office.js is served with the shared pager

<details><summary>516 lines</summary>

```text
HTTP 200 
X-Request-Id: 60811a4c-60f8-4174-947e-ebff3e51f5c4
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562234
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 51193
Date: Fri, 09 Oct 2026 16:09:34 GMT
Connection: close

/**
 * Back Office access guard + admin dashboard.
 */
import { API } from './lib/api.js';
import { canesBoxIndexResultMarkup } from './lib/back-office-canes-box-index.js';
import { renderAlert } from './lib/status-message.js';
import {
  accountPageNavigation,
  parseAdminAccountPage,
  promotedRoleForAction,
  rolePromotionOptions,
  musicPermissionState,
  sharedFolderPermissionState,
} from './lib/back-office-users.js';
import {
  createSharedRecycleActionHandler,
  sharedAuditFilters,
  sharedAuditMarkup,
  sharedRecyclePagination,
  sharedRecycleButton,
  sharedRecycleMarkup,
} from './lib/back-office-shared-folder.js';
import {
  parseReportPage,
  reportFilterValue,
  reportPageNavigation,
} from './lib/back-office-reports.js';
import {
  activityFilterValue,
  activityPageNavigation,
  moderationActivitySummary,
  moderationReasonValue,
  parseActivityPage,
} from './lib/back-office-activity.js';
import { musicAccessAttemptMarkup } from './lib/back-office-music.js';
import { authHeaders, fetchJson, formatWhen, isLoggedIn, sanitize } from './lib/util.js';

const content = document.getElementById('backOfficeContent');
const alertBox = document.getElementById('backOfficeAlert');
const reportQueue = document.getElementById('reportQueue');
const reportFilters = document.getElementById('reportFilters');
const reportPrevious = document.getElementById('reportPrevious');
const reportNext = document.getElementById('reportNext');
const reportPage = document.getElementById('reportPage');
const userQueue = document.getElementById('userQueue');
const userFilters = document.getElementById('userFilters');
const userPrevious = document.getElementById('userPrevious');
const userNext = document.getElementById('userNext');
const userPage = document.getElementById('userPage');
const activityList = document.getElementById('activityList');
const activityFilters = document.getElementById('activityFilters');
const activityPrevious = document.getElementById('activityPrevious');
const activityNext = document.getElementById('activityNext');
const activityPage = document.getElementById('activityPage');
const drawer = document.getElementById('backOfficeDrawer');
const drawerBody = document.getElementById('drawerBody');
const drawerClose = document.getElementById('drawerClose');
const drawerKicker = document.getElementById('drawerKicker');
const drawerTitle = document.getElementById('drawerTitle');
const sharedFolderPermissionsTemplate = document.getElementById('sharedFolderPermissionsTemplate');
const musicPermissionsTemplate = document.getElementById('musicPermissionsTemplate');
const wflOperationStatus = document.getElementById('wflOperationStatus');
const wflInventoryFilters = document.getElementById('wflInventoryFilters');
const wflInventory = document.getElementById('wflInventory');
const wflInventoryMore = document.getElementById('wflInventoryMore');
const canesBoxIndexOperationStatus = document.getElementById('canesBoxIndexOperationStatus');
const canesBoxManualPriceForm = document.getElementById('canesBoxManualPriceForm');
const locationOperationStatus = document.getElementById('locationOperationStatus');
const vehicleOperationStatus = document.getElementById('vehicleOperationStatus');
const contentOperationStatus = document.getElementById('contentOperationStatus');
const vehicleVinForm = document.getElementById('vehicleVinForm');
const vehicleVinBatchForm = document.getElementById('vehicleVinBatchForm');
const sharedAuditForm = document.getElementById('sharedAuditFilters');
const sharedAuditList = document.getElementById('sharedAuditList');
const sharedRecycleList = document.getElementById('sharedRecycleList');
const sharedRecyclePrevious = document.getElementById('sharedRecyclePrevious');
const sharedRecycleNext = document.getElementById('sharedRecycleNext');
const sharedRecyclePage = document.getElementById('sharedRecyclePage');
const musicAccessAuditList = document.getElementById('musicAccessAuditList');

/** The account capability pairs edited from the user drawer. */
const CAPABILITY_FAMILIES = Object.freeze({
  sharedFolder: Object.freeze({
    hostId: 'sharedFolderPermissions',
    template: sharedFolderPermissionsTemplate,
    dataAttribute: 'shared-folder-permission',
    datasetKey: 'sharedFolderPermission',
    stateOf: sharedFolderPermissionState,
    updateUrl: API.accounts.updateSharedFolderPermissions,
    failureMessage: 'Failed to update shared-folder permissions.',
  }),
  music: Object.freeze({
    hostId: 'musicPermissions',
    template: musicPermissionsTemplate,
    dataAttribute: 'music-permission',
    datasetKey: 'musicPermission',
    stateOf: musicPermissionState,
    updateUrl: API.accounts.updateMusicPermissions,
    failureMessage: 'Failed to update Music permissions.',
  }),
});

let accounts = [];
let accountQuery = {
  page: 0,
  size: 25,
  sort: 'createdOn',
  direction: 'desc',
  status: '',
  role: '',
  text: '',
};
let accountPageState = {
  page: 0,
  size: 25,
  totalElements: 0,
  totalPages: 0,
  sort: 'createdOn',
  direction: 'DESC',
};
let reports = [];
let reportQuery = {
  page: 0,
  size: 25,
  status: '',
  reportType: '',
  targetType: '',
  reporter: '',
  from: '',
  to: '',
};
let reportPageState = { page: 0, size: 25, totalElements: 0, totalPages: 0 };
let activities = [];
let activityQuery = {
  page: 0,
  size: 25,
  action: '',
  targetType: '',
  actor: '',
  from: '',
  to: '',
};
let activityPageState = { page: 0, size: 25, totalElements: 0, totalPages: 0 };
let restaurants = [];
let restaurantInventoryQuery = { name: '', city: '', state: '', cursor: '', size: 25 };
let restaurantInventoryNextCursor = '';
let restaurantInventoryTotal = 0;
let duplicatePreviewCursor = '';
let vehicles = [];
let blogPosts = [];
let sharedAuditEvents = [];
let sharedRecycleItems = [];
let sharedRecyclePageNumber = 0;
let sharedRecycleHasNext = false;

function showAlert(message) {
  renderAlert(alertBox, message);
}

function clearAlert() {
  alertBox?.classList.add('d-none');
}

function setLoading() {
  renderState(reportQueue, 'Loading reports…');
  renderState(userQueue, 'Loading users…');
  renderState(activityList, 'Loading activity…');
  renderOperationResult(wflOperationStatus, 'Restaurant counts have not been loaded yet.');
  renderOperationResult(canesBoxIndexOperationStatus, 'Raising Canes Box Index has not been pulled in this session.');
  renderOperationResult(locationOperationStatus, 'Census ZIP coordinates have not been imported in this session.');
  renderOperationResult(vehicleOperationStatus, 'Vehicle state has not been loaded yet.');
  renderOperationResult(contentOperationStatus, 'Content data has not been loaded yet.');
  renderState(sharedAuditList, 'Loading shared-folder audit…');
  renderState(sharedRecycleList, 'Loading recycle items…');
  renderState(musicAccessAuditList, 'Loading denied Music access…');
}

function renderState(container, message) {
  if (!container) return;
  container.innerHTML = `<div class="empty-state">${sanitize(message)}</div>`;
}

function renderOperationResult(container, markup, tone = 'neutral') {
  if (!container) return;
  container.className = `operation-result operation-${tone}`;
  container.innerHTML = markup;
}

function statusClass(status) {
  const value = (status || '').toLowerCase();
  if (value === 'open') return 'status-open';
  if (value === 'resolved' || value === 'active') return 'status-resolved';
  if (value === 'suspended') return 'status-suspended';
  if (value === 'inactive') return 'status-pending';
  return 'status-neutral';
}

function reportSeverityClass(report) {
  if ((report.status || 'OPEN') === 'RESOLVED') return 'queue-resolved';
  const reason = (report.reason || '').toLowerCase();
  if (['harassment', 'violence', 'sexual'].includes(reason)) return 'queue-severe';
  return 'queue-open';
}

function userSeverityClass(account) {
  if ((account.status || '').toUpperCase() === 'SUSPENDED') return 'queue-suspended';
  if ((account.status || '').toUpperCase() === 'INACTIVE') return 'queue-pending';
  return 'queue-resolved';
}

function relativeAge(value) {
  if (!value) return '—';
  const seconds = Math.max(1, Math.floor((Date.now() - new Date(value).getTime()) / 1000));
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function fullName(account) {
  return [account.firstName, account.lastName].filter(Boolean).join(' ');
}

function renderMetrics() {
  const totalReports = reportPageState.totalElements;
  const openReports = reports.filter(report => (report.status || 'OPEN') === 'OPEN').length;
  const inactiveUsers = accounts.filter(
      account => (account.status || '').toUpperCase() === 'INACTIVE').length;
  const suspendedUsers = accounts.filter(account => (account.status || '').toUpperCase() === 'SUSPENDED').length;
  const metrics = {
    metricTotalReports: totalReports,
    metricOpenReports: openReports,
    metricInactiveUsers: inactiveUsers,
    metricSuspendedUsers: suspendedUsers,
    metricRecentActivity: activityPageState.totalElements,
    reportQueueCount: `${totalReports} total`,
    userQueueCount: `${accountPageState.totalElements} total`,
  };

  Object.entries(metrics).forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value);
  });
}

function renderReports() {
  if (!reportQueue) return;
  if (!reports.length) {
    renderState(reportQueue, 'No reports yet. The queue is clear.');
    return;
  }

  reportQueue.innerHTML = reports.map(report => {
    const status = report.status || 'OPEN';
    const reason = report.reason || 'other';
    const postText = sanitize(report.postText || 'No post text available.');
    return `
      <article class="queue-card ${reportSeverityClass(report)}" data-detail-type="report" data-id="${sanitize(report.id || '')}" tabindex="0">
        <div class="queue-main">
          <div class="queue-topline">
            <span class="status-pill ${statusClass(status)}">${sanitize(status)}</span>
            <span class="queue-age">${relativeAge(report.createdOn)}</span>
          </div>
          <h3>${sanitize(reason)}</h3>
          <p>${postText}</p>
          <div class="queue-meta">
            <span>Reporter @${sanitize(report.reporterUsername || 'unknown')}</span>
            <span>Reported @${sanitize(report.reportedUsername || 'unknown')}</span>
            <span>${sanitize(repeatReportSummary(report))}</span>
          </div>
        </div>
        <div class="queue-actions">
          ${reportActionSelect(report)}
        </div>
      </article>
    `;
  }).join('');
}

function reportActionSelect(report) {
  const status = report.status || 'OPEN';
  const options = status === 'OPEN'
      ? `
        <option value="CLOSE_NO_ACTION">Close</option>
        <option value="DELETE_POST">Delete post</option>
        <option value="DELETE_POST_AND_SUSPEND_USER">Delete + suspend</option>
      `
      : '<option value="REOPEN">Reopen</option>';

  return `
    <select class="form-select form-select-sm report-action" data-report="${sanitize(report.id || '')}" aria-label="Report action">
      <option value="" selected>Action…</option>
      ${options}
    </select>
  `;
}

function repeatReportSummary(report) {
  const open = report.openReportsForAccount ?? 0;
  const resolved = report.resolvedReportsForAccount ?? 0;
  return `${open} open / ${resolved} resolved reports for account`;
}

function renderUsers() {
  if (!userQueue) return;
  if (!accounts.length) {
    renderState(userQueue, 'No accounts found.');
    return;
  }

  userQueue.innerHTML = accounts.map(account => {
    const status = account.status || 'UNKNOWN';
    const name = fullName(account);
    return `
      <article class="queue-card ${userSeverityClass(account)}" data-detail-type="user" data-id="${sanitize(account.id || '')}" tabindex="0">
        <div class="queue-main">
          <div class="queue-topline">
            <span class="status-pill ${statusClass(status)}">${sanitize(status)}</span>
            <span class="queue-age">${account.createdOn ? `Joined ${relativeAge(account.createdOn)}` : 'No creation date'}</span>
          </div>
          <h3>@${sanitize(account.username || 'unknown')}</h3>
          <p>${sanitize(name || account.email || 'No profile details')}</p>
          <div class="queue-meta">
            <span>${sanitize(account.role || 'USER')}</span>
          </div>
        </div>
        <div class="queue-actions">
          ${userActionSelect(account)}
        </div>
      </article>
    `;
  }).join('');
}

function applyReportPage(payload) {
  const parsed = parseReportPage(payload);
  reports = parsed.items;
  reportPageState = {
    page: parsed.page,
    size: parsed.size,
    totalElements: parsed.totalElements,
    totalPages: parsed.totalPages,
  };
}

function renderReportNavigation() {
  const state = reportPageNavigation(reportPageState);
  if (reportPrevious) reportPrevious.disabled = state.previousDisabled;
  if (reportNext) reportNext.disabled = state.nextDisabled;
  if (reportPage) reportPage.textContent = state.label;
}

function renderUserNavigation() {
  const state = accountPageNavigation(accountPageState);
  if (userPrevious) userPrevious.disabled = state.previousDisabled;
  if (userNext) userNext.disabled = state.nextDisabled;
  if (userPage) userPage.textContent = state.label;
}

function applyActivityPage(payload) {
  const parsed = parseActivityPage(payload);
  activities = parsed.items;
  activityPageState = {
    page: parsed.page,
    size: parsed.size,
    totalElements: parsed.totalElements,
    totalPages: parsed.totalPages,
  };
}

function renderActivityNavigation() {
  const state = activityPageNavigation(activityPageState);
  if (activityPrevious) activityPrevious.disabled = state.previousDisabled;
  if (activityNext) activityNext.disabled = state.nextDisabled;
  if (activityPage) activityPage.textContent = state.label;
}

function applyAccountPage(payload) {
  const parsed = parseAdminAccountPage(payload);
  accounts = parsed.items;
  accountPageState = {
    page: parsed.page,
    size: parsed.size,
    totalElements: parsed.totalElements,
    totalPages: parsed.totalPages,
    sort: parsed.sort,
    direction: parsed.direction,
  };
}

function userActionSelect(account) {
  const status = (account.status || '').toUpperCase();
  const options = [];
  rolePromotionOptions(account).forEach(option => {
    options.push(`<option value="${sanitize(option.value)}">${sanitize(option.label)}</option>`);
  });
  if (status !== 'SUSPENDED') {
    options.push('<option value="SUSPEND">Suspend</option>');
  }
  if (status !== 'ACTIVE') {
    options.push('<option value="ACTIVATE">Activate</option>');
  }
  if (!options.length) {
    return '<span class="queue-age">No actions</span>';
  }
  return `
    <select class="form-select form-select-sm user-action" data-account="${sanitize(account.id || '')}" aria-label="User action">
      <option value="" selected>Action…</option>
      ${options.join('')}
    </select>
  `;
}

function renderActivity() {
  if (!activityList) return;
  if (!activities.length) {
    renderState(activityList, 'No admin activity recorded yet.');
    return;
  }

  activityList.innerHTML = activities.map(activity => {
    const audit = moderationActivitySummary(activity);
    return `
      <article class="activity-item">
        <div class="activity-dot ${activityClass(activity.action)}"></div>
        <div>
          <strong>${sanitize(activity.message || activity.action || 'Activity')}</strong>
          ${audit.reason ? `<span><b>Reason:</b> ${sanitize(audit.reason)}</span>` : ''}
          ${audit.transition ? `<span>${sanitize(audit.transition)}</span>` : ''}
          <span>${activity.createdOn ? formatWhen(activity.createdOn) : '—'}</span>
        </div>
      </article>
    `;
  }).join('');
}

function activityClass(action) {
  if (action === 'USER_SUSPENDED') return 'activity-danger';
  if (action === 'POST_DELETED') return 'activity-warning';
  if (action === 'REPORT_RESOLVED') return 'activity-success';
  return 'activity-neutral';
}

function openDrawer(type, id) {
  const item = type === 'report'
      ? reports.find(report => report.id === id)
      : accounts.find(account => account.id === id);
  if (!item || !drawer || !drawerBody || !drawerTitle || !drawerKicker) return;

  drawerKicker.textContent = type === 'report' ? 'Report Details' : 'User Details';
  drawerTitle.textContent = type === 'report'
      ? `${item.reason || 'Report'}`
      : `@${item.username || 'user'}`;
  drawerBody.innerHTML = type === 'report' ? reportDetails(item) : userDetails(item);
  if (type === 'user') {
    renderCapabilityPermissions(item, CAPABILITY_FAMILIES.sharedFolder);
    renderCapabilityPermissions(item, CAPABILITY_FAMILIES.music);
  }
  drawer.classList.remove('d-none');
  drawer.setAttribute('aria-hidden', 'false');
}

function closeDrawer() {
  drawer?.classList.add('d-none');
  drawer?.setAttribute('aria-hidden', 'true');
}

function detailRow(label, value) {
  return `
    <div class="detail-row">
      <span>${sanitize(label)}</span>
      <strong>${sanitize(value || '—')}</strong>
    </div>
  `;
}

function reportDetails(report) {
  return `
    <div class="detail-section">
      ${detailRow('Status', report.status || 'OPEN')}
      ${detailRow('Reason', report.reason)}
      ${detailRow('Reporter', `@${report.reporterUsername || 'unknown'}`)}
      ${detailRow('Reported', `@${report.reportedUsername || 'unknown'}`)}
      ${detailRow('Open reports for account', report.openReportsForAccount ?? 0)}
      ${detailRow('Resolved reports for account', report.resolvedReportsForAccount ?? 0)}
      ${detailRow('Created', report.createdOn ? formatWhen(report.createdOn) : '—')}
      ${detailRow('Resolved', report.resolvedOn ? formatWhen(report.resolvedOn) : '—')}
      ${detailRow('Resolution', report.resolution)}
    </div>
    <div class="detail-section">
      <span class="detail-label">Post</span>
      <p class="detail-copy">${sanitize(report.postText || 'No p
... [32328 more characters not recorded]
```

</details>

### 5. The new paging module is served

<details><summary>42 lines</summary>

```text
HTTP 200 
X-Request-Id: 3925409e-2404-4f1f-b94a-5b390563626b
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562234
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 1060
Date: Fri, 09 Oct 2026 16:09:34 GMT
Connection: close

/** Validate one server page of Back Office records, or throw with the caller's message. */
export function parseServerPage(payload, invalidMessage) {
  if (!payload || !Array.isArray(payload.items)
      || !Number.isInteger(payload.page) || payload.page < 0
      || !Number.isInteger(payload.size) || payload.size < 1
      || !Number.isFinite(payload.totalElements) || payload.totalElements < 0
      || !Number.isInteger(payload.totalPages) || payload.totalPages < 0) {
    throw new Error(invalidMessage);
  }
  return { ...payload, items: [...payload.items] };
}

/** Derive exact previous/next state and label from authoritative page totals. */
export function serverPageNavigation(page) {
  const totalPages = Math.max(0, Number(page?.totalPages || 0));
  const currentPageIndex = Math.max(0, Number(page?.page || 0));
  return {
    previousDisabled: currentPageIndex <= 0,
    nextDisabled: totalPages === 0 || currentPageIndex + 1 >= totalPages,
    label: totalPages === 0 ? 'Page 0 of 0' : `Page ${currentPageIndex + 1} of ${totalPages}`,
  };
}
```

</details>

### 6. The activity module imports the paging module

<details><summary>70 lines</summary>

```text
HTTP 200 
X-Request-Id: 23d275b5-0ee2-4ffc-ba43-2301af0bb5c5
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562234
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 1900
Date: Fri, 09 Oct 2026 16:09:34 GMT
Connection: close

import { parseServerPage, serverPageNavigation } from './back-office-paging.js';

const AUDIT_STATE_KEYS = ['role', 'status', 'resolution'];

/** Validate one server audit page before it reaches Back Office rendering. */
export function parseActivityPage(payload) {
  return parseServerPage(payload, 'Invalid audit page response.');
}

/** Derive exact navigation state from authoritative audit totals. */
export function activityPageNavigation(page) {
  return serverPageNavigation(page);
}

/** Convert audit form controls to the inclusive Instant query contract. */
export function activityFilterValue(form) {
  const values = new FormData(form);
  return {
    action: String(values.get('action') || '').trim(),
    targetType: String(values.get('targetType') || '').trim(),
    actor: String(values.get('actor') || '').trim(),
    from: toInstant(values.get('from')),
    to: toInstant(values.get('to')),
  };
}

/** Normalize a required moderator reason before sending any mutation. */
export function moderationReasonValue(value) {
  const reason = String(value || '').trim();
  return reason.length > 0 && reason.length <= 500 ? reason : '';
}

/** Present only the server's allowlisted moderation state and reason. */
export function moderationActivitySummary(activity) {
  const before = activity?.beforeValues || {};
  const after = activity?.afterValues || {};
  const transitions = AUDIT_STATE_KEYS
      .filter(key => Object.hasOwn(before, key) || Object.hasOwn(after, key))
      .map(key => `${key}: ${before[key] || '—'} → ${after[key] || '—'}`);
  return {
    reason: String(activity?.reason || '').trim(),
    transition: transitions.join('; '),
  };
}

function toInstant(value) {
  if (!value) return '';
  const parsed = new Date(String(value));
  return Number.isFinite(parsed.getTime()) ? parsed.toISOString() : '';
}
```

</details>

### 7. The reports module imports the paging module

<details><summary>51 lines</summary>

```text
HTTP 200 
X-Request-Id: 2b70fcc8-b757-4685-ba98-2e77931c995d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562234
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 1377
Date: Fri, 09 Oct 2026 16:09:34 GMT
Connection: close

import { parseServerPage, serverPageNavigation } from './back-office-paging.js';

/** Validate one server report page before it reaches Back Office rendering. */
export function parseReportPage(payload) {
  return parseServerPage(payload, 'Invalid report page response.');
}

/** Derive exact navigation state from authoritative report totals. */
export function reportPageNavigation(reportPage) {
  return serverPageNavigation(reportPage);
}

/** Convert local date controls to the inclusive Instant query contract. */
export function reportFilterValue(filterForm) {
  const filterValues = new FormData(filterForm);
  return {
    status: String(filterValues.get('status') || ''),
    reportType: String(filterValues.get('reportType') || ''),
    targetType: String(filterValues.get('targetType') || ''),
    reporter: String(filterValues.get('reporter') || '').trim(),
    from: isoInstantFromLocalDateTime(filterValues.get('from')),
    to: isoInstantFromLocalDateTime(filterValues.get('to')),
  };
}

/** Returns the ISO instant for a local date-time control value, or '' when empty or invalid. */
function isoInstantFromLocalDateTime(localDateTimeText) {
  if (!localDateTimeText) return '';
  const localDateTime = new Date(String(localDateTimeText));
  return Number.isFinite(localDateTime.getTime()) ? localDateTime.toISOString() : '';
}
```

</details>

### 8. The Music access module uses util.sanitize

<details><summary>38 lines</summary>

```text
HTTP 200 
X-Request-Id: b9195f21-c9f8-4cca-8e2e-018b54152145
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562234
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 825
Date: Fri, 09 Oct 2026 16:09:34 GMT
Connection: close

import { sanitize } from './util.js';

export function musicAccessAttemptMarkup(attempts) {
  if (!Array.isArray(attempts) || attempts.length === 0) {
    return '<div class="empty-state">No denied Music access attempts were recorded.</div>';
  }
  return attempts.map(attempt => `
    <article class="queue-card">
      <div class="queue-card-main">
        <strong>${sanitize(attempt.reason || 'ACCESS_DENIED')}</strong>
        <span>${sanitize(attempt.principalType || 'UNKNOWN')}: ${sanitize(attempt.principal || 'unknown')}</span>
      </div>
      <div class="queue-card-meta">
        <span>${sanitize(attempt.count || 0)} attempt(s)</span>
        <time>${sanitize(attempt.lastAttemptAt ? new Date(attempt.lastAttemptAt).toLocaleString() : '—')}</time>
      </div>
    </article>`).join('');
}
```

</details>

### 9. The shared-folder module uses util.sanitize

<details><summary>171 lines</summary>

```text
HTTP 200 
X-Request-Id: ddbab877-88f4-48df-994a-e82820b06f66
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562235
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 5282
Date: Fri, 09 Oct 2026 16:09:35 GMT
Connection: close

import { sanitize } from './util.js';

function when(value) {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : date.toLocaleString();
}

export function sharedAuditMarkup(events) {
  if (!Array.isArray(events) || events.length === 0) {
    return '<div class="empty-state">No shared-folder audit events match these filters.</div>';
  }
  return events.map(event => `
    <article class="queue-card shared-audit-card">
      <div class="queue-card-main">
        <strong>${sanitize(event.action || 'UNKNOWN')}</strong>
        <span>${sanitize(event.relativePath || 'unknown')}</span>
      </div>
      <div class="queue-card-meta">
        <span>${sanitize(event.accountId || 'unknown')}</span>
        <span>${sanitize(event.outcome || 'unknown')}</span>
        <span>Failure: ${sanitize(event.failureCategory || '—')}</span>
        <span>Client: ${sanitize(event.clientIp || 'unknown')}</span>
        <time>${sanitize(when(event.occurredAt))}</time>
      </div>
    </article>
  `).join('');
}

export function sharedRecyclePagination(page, hasNext) {
  const safePage = Number.isInteger(page) && page >= 0 ? page : 0;
  return {
    label: `Page ${safePage + 1}`,
    previousDisabled: safePage === 0,
    nextDisabled: hasNext !== true,
  };
}

export function sharedRecycleMarkup(items) {
  if (!Array.isArray(items) || items.length === 0) {
    return '<div class="empty-state">The recycle area is empty.</div>';
  }
  return items.map(item => {
    const id = sanitize(item.id);
    return `
      <article class="queue-card shared-recycle-card" data-recycle-id="${id}">
        <div class="queue-card-main">
          <strong>${sanitize(item.originalPath || 'unknown')}</strong>
          <span>${sanitize(item.size ?? 0)} bytes · deleted by ${sanitize(item.deletedByAccountId || 'unknown')}</span>
        </div>
        <div class="queue-card-meta">
          <span>Deleted ${sanitize(when(item.deletedAt))}</span>
          <span>Expires ${sanitize(when(item.expiresAt))}</span>
        </div>
        <div class="operation-actions">
          <button class="btn btn-sm btn-outline-primary" type="button" data-shared-recycle-action="restore" data-id="${id}">Restore</button>
          <button class="btn btn-sm btn-outline-warning" type="button" data-shared-recycle-action="replace" data-id="${id}">Restore and replace</button>
          <button class="btn btn-sm btn-outline-danger" type="button" data-shared-recycle-action="purge" data-id="${id}">Permanently purge</button>
        </div>
      </article>
    `;
  }).join('');
}

export function sharedAuditFilters(form) {
  const result = {};
  for (const name of ['accountId', 'action', 'outcome', 'path']) {
    const value = String(form?.elements?.[name]?.value || '').trim();
    if (value) result[name] = value;
  }
  for (const name of ['from', 'to']) {
    const value = String(form?.elements?.[name]?.value || '').trim();
    if (!value) continue;
    const date = new Date(value);
    if (!Number.isNaN(date.getTime())) result[name] = date.toISOString();
  }
  return result;
}

export function purgeConfirmation(id, value) {
  return String(value || '') === `PURGE ${id}`;
}

export async function runSharedRecycleAction({
  id,
  action,
  confirmReplace,
  promptPurge,
  restore,
  purge,
}) {
  if (!id || !['restore', 'replace', 'purge'].includes(action)) return false;
  if (action === 'restore') {
    await restore(id, false);
    return true;
  }
  if (action === 'replace') {
    if (!confirmReplace()) return false;
    await restore(id, true);
    return true;
  }
  const typed = promptPurge() || '';
  if (!purgeConfirmation(id, typed)) {
    throw new Error('Permanent purge confirmation did not match.');
  }
  await purge(id, typed);
  return true;
}

export function sharedRecycleButton(target, ButtonType) {
  const button = target?.closest?.('[data-shared-recycle-action]');
  return typeof ButtonType === 'function' && button instanceof ButtonType ? button : null;
}

export function createSharedRecycleActionHandler({
  api,
  fetchJson,
  authHeaders,
  refresh,
  clearAlert,
  showAlert,
  confirmReplace,
  promptPurge,
}) {
  return async button => {
    const id = button?.getAttribute?.('data-id');
    const action = button?.getAttribute?.('data-shared-recycle-action');
    if (!id || !action) return;
    button.disabled = true;
    clearAlert();
    try {
      const completed = await runSharedRecycleAction({
        id,
        action,
        confirmReplace,
        promptPurge: () => promptPurge(id),
        restore: (itemId, replace) => fetchJson(api.restore(itemId), {
          method: 'POST', headers: authHeaders(), body: JSON.stringify({ replace }),
        }),
        purge: (itemId, confirmation) => fetchJson(api.purge(itemId), {
          method: 'DELETE', headers: authHeaders(), body: JSON.stringify({ confirmation }),
        }),
      });
      if (completed) await refresh();
    } catch (error) {
      showAlert(error?.message || 'Shared-folder administration failed.');
    } finally {
      button.disabled = false;
    }
  };
}
```

</details>

### 10. The users module is served

<details><summary>103 lines</summary>

```text
HTTP 200 
X-Request-Id: cd512260-7627-47cb-a349-a06563556295
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562235
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 3102
Date: Fri, 09 Oct 2026 16:09:35 GMT
Connection: close

const ROLE_ORDER = ['USER', 'MOD', 'ADMIN'];

/**
 * Validates the administrative account page returned by the server.
 */
export function parseAdminAccountPage(payload) {
  const integerFields = ['page', 'size', 'totalElements', 'totalPages'];
  const hasValidIntegers = integerFields.every(field =>
    Number.isInteger(payload?.[field]) && payload[field] >= 0);
  const hasValidMetadata = typeof payload?.sort === 'string'
      && ['ASC', 'DESC'].includes(payload?.direction);
  if (!payload || !Array.isArray(payload.items) || !hasValidIntegers || !hasValidMetadata) {
    throw new TypeError('Server returned an invalid account page.');
  }
  return { ...payload, items: [...payload.items] };
}

/**
 * Produces the accessible Back Office previous/next state for an account page.
 */
export function accountPageNavigation({ page, totalPages }) {
  const hasPages = totalPages > 0;
  return {
    previousDisabled: !hasPages || page <= 0,
    nextDisabled: !hasPages || page + 1 >= totalPages,
    label: hasPages ? `Page ${page + 1} of ${totalPages}` : 'Page 0 of 0',
  };
}

/**
 * Returns role promotions that increase privilege without offering demotions.
 */
export function rolePromotionOptions(account) {
  const role = String(account?.role || 'USER').toUpperCase();
  const roleIndex = ROLE_ORDER.indexOf(role);
  if (roleIndex < 0) {
    return [];
  }
  return ROLE_ORDER.slice(roleIndex + 1).map(nextRole => ({
    value: `PROMOTE_${nextRole}`,
    label: `Promote to ${nextRole}`,
  }));
}

/**
 * Converts a promotion action value into the role stored by the account API.
 */
export function promotedRoleForAction(action) {
  const role = String(action || '').replace(/^PROMOTE_/, '');
  return ['MOD', 'ADMIN'].includes(role) ? role : null;
}

/**
 * Resolves the Back Office checkbox state while keeping shared-folder write access dependent on
 * read access. ADMINs always retain the role-provided default and therefore cannot be edited.
 */
export function sharedFolderPermissionState(account, change = {}) {
  return capabilityPermissionState(
      account, 'SHARED_FOLDER_READ', 'SHARED_FOLDER_WRITE', change);
}

/** Resolves Music checkbox state with the same write-implies-read invariant. */
export function musicPermissionState(account, change = {}) {
  return capabilityPermissionState(account, 'MUSIC_READ', 'MUSIC_WRITE', change);
}

function capabilityPermissionState(account, readCapability, writeCapability, change) {
  const isAdmin = String(account?.role || '').toUpperCase() === 'ADMIN';
  if (isAdmin) {
    return { read: true, write: true, disabled: true };
  }

  const permissions = new Set(account?.permissions || []);
  const currentRead = permissions.has(readCapability);
  const currentWrite = permissions.has(writeCapability);
  if (change.read === false) {
    return { read: false, write: false, disabled: false };
  }

  const write = change.write ?? currentWrite;
  const read = change.read ?? currentRead;
  return { read: read || write, write, disabled: false };
}
```

</details>

### 11. The canes module is served

<details><summary>55 lines</summary>

```text
HTTP 200 
X-Request-Id: 7a08f872-a3e5-47b9-872d-25f3a6a85cb6
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791562235
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 16:04:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 2094
Date: Fri, 09 Oct 2026 16:09:35 GMT
Connection: close

import { sanitize } from './util.js';

/** Format a Raising Canes Box Index price for Back Office summaries. */
export function formatCanesBoxIndexPrice(value) {
  if (value == null || Number.isNaN(Number(value))) return 'No data';
  return `$${Number(value).toFixed(2)}`;
}

/** Build Back Office status markup for a forced index pull. */
export function canesBoxIndexResultMarkup(result) {
  const provisionalRows = (result?.metroPrices || [])
      .filter(row => row?.qualityStatus === 'PROVISIONAL')
      .map(row => `
        <div class="operation-review-row">
          <span><strong>${sanitize(row.metroName || 'Metro')}</strong>${sanitize(row.sourceName || 'Source')} ${formatCanesBoxIndexPrice(row.price)}</span>
          <span class="operation-actions">
            <button type="button" class="btn btn-sm btn-outline-light" data-canes-box-review="approve" data-week-start-date="${sanitize(result?.weekStartDate || '')}" data-metro-name="${sanitize(row.metroName || '')}">Approve</button>
            <button type="button" class="btn btn-sm btn-outline-danger" data-canes-box-review="reject" data-week-start-date="${sanitize(result?.weekStartDate || '')}" data-metro-name="${sanitize(row.metroName || '')}">Reject</button>
          </span>
        </div>
      `)
      .join('');
  return `
    <p class="operation-message">Raising Canes Box Index pull complete.</p>
    <div class="operation-stat-grid">
      <span><strong>${formatCanesBoxIndexPrice(result?.averagePrice)}</strong>Average</span>
      <span><strong>${sanitize(result?.weekStartDate || '-')}</strong>Week</span>
      <span><strong>${result?.successfulMetroCount ?? 0}/${result?.totalMetroCount ?? 0}</strong>Metros</span>
      <span><strong>${result?.verifiedMetroCount ?? 0}</strong>Verified</span>
      <span><strong>${result?.provisionalMetroCount ?? 0}</strong>Provisional</span>
      <span><strong>${result?.excludedMetroCount ?? 0}</strong>Excluded</span>
    </div>
    ${provisionalRows ? `<div class="operation-review-list">${provisionalRows}</div>` : ''}
  `;
}
```

</details>

## Evidence
- Case 1 started 2026-10-09T11:09:33-05:00, took 45 ms, candidate `0332f5c`
- Case 2 started 2026-10-09T11:09:33-05:00, took 203 ms, candidate `0332f5c`
- Case 3 started 2026-10-09T11:09:33-05:00, took 31 ms, candidate `0332f5c`
- Case 4 started 2026-10-09T11:09:34-05:00, took 30 ms, candidate `0332f5c`
- Case 5 started 2026-10-09T11:09:34-05:00, took 15 ms, candidate `0332f5c`
- Case 6 started 2026-10-09T11:09:34-05:00, took 30 ms, candidate `0332f5c`
- Case 7 started 2026-10-09T11:09:34-05:00, took 47 ms, candidate `0332f5c`
- Case 8 started 2026-10-09T11:09:34-05:00, took 47 ms, candidate `0332f5c`
- Case 9 started 2026-10-09T11:09:35-05:00, took 30 ms, candidate `0332f5c`
- Case 10 started 2026-10-09T11:09:35-05:00, took 31 ms, candidate `0332f5c`
- Case 11 started 2026-10-09T11:09:35-05:00, took 30 ms, candidate `0332f5c`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
