# Sitemonitor slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 6 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-20-33-christopherbell-dev-sitemonitor-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-sitemonitor-20261006` at candidate `e5ad16d`

## Pass / Fail

> [!TIP]
> 12 of 12 cases passed on candidate `e5ad16d`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create a disposable USER through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | New USER has an empty workspace | ✅ PASS | Expected status 200 and body containing '"sites":[]' |
| 4 | A non-HTTPS origin is rejected with 400 | ✅ PASS | Expected status 400 and body containing 'publicly reachable HTTPS origin' |
| 5 | Add the fixed demonstration site | ✅ PASS | Expected status 200 and body containing '"label":"Demonstration website"' |
| 6 | Comparison before a baseline is refused with 409 | ✅ PASS | Expected status 409 and body containing 'Capture a healthy baseline' |
| 7 | Capture baseline on the demo site (read-only requests to the public demo pages); stored report status BASELINE | ✅ PASS | Expected status 200 and body containing '"status":"BASELINE"' |
| 8 | Reloaded workspace reads the stored BASELINE report back from MongoDB | ✅ PASS | Expected status 200 and body containing '"status":"BASELINE"' |
| 9 | Immediate re-check is refused with 429 (cooldown) | ✅ PASS | Expected status 429 and body containing 'once every 15 minutes' |
| 10 | Download the plain-text client report | ✅ PASS | Expected status 200 and body containing 'Result: BASELINE' |
| 11 | Removing the only site empties the workspace | ✅ PASS | Expected status 200 and body containing '"sites":[]' |
| 12 | Anonymous workspace read gets the same 403 status and body as production (timestamp ignored) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:65103/actuator/health/readiness`
2. **Create a disposable USER through the API and log in (password generated, not recorded)**: command `python permission_signup_login.py http://127.0.0.1:65103 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/sm-token.txt`
3. **New USER has an empty workspace**: http `GET http://127.0.0.1:65103/api/site-monitor/v1`
4. **A non-HTTPS origin is rejected with 400**: http `POST http://127.0.0.1:65103/api/site-monitor/v1/sites`
5. **Add the fixed demonstration site**: http `POST http://127.0.0.1:65103/api/site-monitor/v1/sites`
6. **Comparison before a baseline is refused with 409**: http `POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/check`
7. **Capture baseline on the demo site (read-only requests to the public demo pages); stored report status BASELINE**: http `POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/baseline`
8. **Reloaded workspace reads the stored BASELINE report back from MongoDB**: http `GET http://127.0.0.1:65103/api/site-monitor/v1`
9. **Immediate re-check is refused with 429 (cooldown)**: http `POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/check`
10. **Download the plain-text client report**: http `GET http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/reports/595fd365-0ead-43d6-8bb8-510c22e8919f`
11. **Removing the only site empties the workspace**: http `DELETE http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c`
12. **Anonymous workspace read gets the same 403 status and body as production (timestamp ignored)**: command `python compare_status_and_body.py http://127.0.0.1:65103/api/site-monitor/v1 https://www.christopherbell.dev/api/site-monitor/v1 403`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:65102 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:65103, base 1f1287d2 |
| Outbound | demo baseline made read-only GET/HEAD requests to the public demo pages on www.christopherbell.dev, as the feature does for any user |
| Credentials | disposable USER in the throwaway database; password generated and never recorded; bearer token masked |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:65103/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `python permission_signup_login.py http://127.0.0.1:65103 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/sm-token.txt` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:65103/api/site-monitor/v1` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `POST http://127.0.0.1:65103/api/site-monitor/v1/sites` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `POST http://127.0.0.1:65103/api/site-monitor/v1/sites` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/check` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/baseline` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `GET http://127.0.0.1:65103/api/site-monitor/v1` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/check` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `GET http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/reports/595fd365-0ead-43d6-8bb8-510c22e8919f` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `DELETE http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c` in `A:\Projects\christopherbell.dev-worktrees\style-sitemonitor`
- **Local command:** `python compare_status_and_body.py http://127.0.0.1:65103/api/site-monitor/v1 https://www.christopherbell.dev/api/site-monitor/v1 403` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Candidate identity:** `e5ad16d`
- **Cleanup:** Stopped candidate PID 4284 and mongod PID 50756 by process tree; both ports have zero listeners; scratch token file deleted; production MongoDB 27017 untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:65103/actuator/health/readiness
```

### 2. Create a disposable USER through the API and log in (password generated, not recorded)

```text
python permission_signup_login.py http://127.0.0.1:65103 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/sm-token.txt
```

### 3. New USER has an empty workspace

```http
GET http://127.0.0.1:65103/api/site-monitor/v1
Authorization: [REDACTED]
```

### 4. A non-HTTPS origin is rejected with 400

```http
POST http://127.0.0.1:65103/api/site-monitor/v1/sites
Authorization: [REDACTED]
Content-Type: application/json

{"label":"Client","origin":"http://example.com","paths":["/"],"demo":false}
```

### 5. Add the fixed demonstration site

```http
POST http://127.0.0.1:65103/api/site-monitor/v1/sites
Authorization: [REDACTED]
Content-Type: application/json

{"label":"ignored","demo":true}
```

### 6. Comparison before a baseline is refused with 409

```http
POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/check
Authorization: [REDACTED]
```

### 7. Capture baseline on the demo site (read-only requests to the public demo pages); stored report status BASELINE

```http
POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/baseline
Authorization: [REDACTED]
```

### 8. Reloaded workspace reads the stored BASELINE report back from MongoDB

```http
GET http://127.0.0.1:65103/api/site-monitor/v1
Authorization: [REDACTED]
```

### 9. Immediate re-check is refused with 429 (cooldown)

```http
POST http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/check
Authorization: [REDACTED]
```

### 10. Download the plain-text client report

```http
GET http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c/reports/595fd365-0ead-43d6-8bb8-510c22e8919f
Authorization: [REDACTED]
```

### 11. Removing the only site empties the workspace

```http
DELETE http://127.0.0.1:65103/api/site-monitor/v1/sites/695de744-10c4-457e-b5b5-ed7becb3be9c
Authorization: [REDACTED]
```

### 12. Anonymous workspace read gets the same 403 status and body as production (timestamp ignored)

```text
python compare_status_and_body.py http://127.0.0.1:65103/api/site-monitor/v1 https://www.christopherbell.dev/api/site-monitor/v1 403
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 1d18739e-de0d-47b3-ac09-f7b014aa1b4f
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337189
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
Date: Wed, 07 Oct 2026 01:38:49 GMT
Connection: close

{"status":"UP"}
```

### 2. Create a disposable USER through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
create status 201 username style_check role USER
login status 200 token segments 3
```

### 3. New USER has an empty workspace

```text
HTTP 200 
X-Request-Id: 6ae85813-3929-46d6-930e-982e500153f1
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337190
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:51 GMT
Connection: close

{"messages":null,"payload":{"id":null,"version":null,"accountId":"2ac66d3b-89c2-4e64-98be-c26b739e04b1","generation":null,"sites":[]},"requestId":null,"success":true}
```

### 4. A non-HTTPS origin is rejected with 400

```text
HTTP 400 
X-Request-Id: b5c5b32f-0baf-4b09-8319-50fd023cb428
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1791337191
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:51 GMT
Connection: close

{"messages":[{"code":"SITE_MONITOR_REJECTED","description":"Use a publicly reachable HTTPS origin and valid page paths."}],"payload":null,"requestId":null,"success":false}
```

### 5. Add the fixed demonstration site

```text
HTTP 200 
X-Request-Id: c941451d-2372-4f8d-9820-823d1b0d19d9
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1791337191
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:51 GMT
Connection: close

{"messages":null,"payload":{"id":"pilot-0","version":0,"accountId":"2ac66d3b-89c2-4e64-98be-c26b739e04b1","generation":"faefd0e9-3638-46ad-9d04-a866d0a6d6e0","sites":[{"id":"695de744-10c4-457e-b5b5-ed7becb3be9c","label":"Demonstration website","origin":"https://www.christopherbell.dev","paths":["/","/zip-coordinates","/vin-decoder"],"token":"c97b82b3-fc68-4a40-96b5-1700691e46c4-b0877bd4-d5c9-4ae1-9c01-988deb0ff91a","demo":true,"verifiedOn":null,"lastAttempt":null,"baselineOn":null,"baseline":[],"reports":[]}]},"requestId":null,"success":true}
```

### 6. Comparison before a baseline is refused with 409

```text
HTTP 409 
X-Request-Id: 3629a1d4-ecc6-461f-9e23-1937c241f76a
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1791337191
Cache-Control: no-store
Retry-After: 60
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:51 GMT
Connection: close

{"messages":[{"code":"SITE_MONITOR_REJECTED","description":"Capture a healthy baseline before running comparisons."}],"payload":null,"requestId":null,"success":false}
```

### 7. Capture baseline on the demo site (read-only requests to the public demo pages); stored report status BASELINE

```text
HTTP 200 
X-Request-Id: 518a5ff7-b0d5-4747-a9e4-eef1ffdd7934
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 6
X-RateLimit-Reset: 1791337191
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:55 GMT
Connection: close

{"messages":null,"payload":{"id":"pilot-0","version":2,"accountId":"2ac66d3b-89c2-4e64-98be-c26b739e04b1","generation":"faefd0e9-3638-46ad-9d04-a866d0a6d6e0","sites":[{"id":"695de744-10c4-457e-b5b5-ed7becb3be9c","label":"Demonstration website","origin":"https://www.christopherbell.dev","paths":["/","/zip-coordinates","/vin-decoder"],"token":"c97b82b3-fc68-4a40-96b5-1700691e46c4-b0877bd4-d5c9-4ae1-9c01-988deb0ff91a","demo":true,"verifiedOn":"2026-10-07T01:38:55.148Z","lastAttempt":"2026-10-07T01:38:51.844Z","baselineOn":"2026-10-07T01:38:55.148Z","baseline":[{"path":"/","status":200,"finalUrl":"https://www.christopherbell.dev/","title":"CB | Home","description":"A working corner of the internet for Void posts, lunch picks, and practical utilities.","canonical":"https://www.christopherbell.dev/","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/zip-coordinates","status":200,"finalUrl":"https://www.christopherbell.dev/zip-coordinates","title":"ZIP Coordinates","description":"Look up Census ZIP coordinate origins from christopherbell.dev.","canonical":"https://www.christopherbell.dev/zip-coordinates","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/vin-decoder","status":200,"finalUrl":"https://www.christopherbell.dev/vin-decoder","title":"VIN Decoder","description":"Paste a VIN and get a clean NHTSA-backed decode with summary fields and JSON.","canonical":"https://www.christopherbell.dev/vin-decoder","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false}],"reports":[{"id":"595fd365-0ead-43d6-8bb8-510c22e8919f","checkedOn":"2026-10-07T01:38:55.148Z","baselineOn":"2026-10-07T01:38:55.148Z","status":"BASELINE","findings":[],"pages":[{"path":"/","status":200,"finalUrl":"https://www.christopherbell.dev/","title":"CB | Home","description":"A working corner of the internet for Void posts, lunch picks, and practical utilities.","canonical":"https://www.christopherbell.dev/","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/zip-coordinates","status":200,"finalUrl":"https://www.christopherbell.dev/zip-coordinates","title":"ZIP Coordinates","description":"Look up Census ZIP coordinate origins from christopherbell.dev.","canonical":"https://www.christopherbell.dev/zip-coordinates","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/vin-decoder","status":200,"finalUrl":"https://www.christopherbell.dev/vin-decoder","title":"VIN Decoder","description":"Paste a VIN and get a clean NHTSA-backed decode with summary fields and JSON.","canonical":"https://www.christopherbell.dev/vin-decoder","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false}]}]}]},"requestId":null,"success":true}
```

### 8. Reloaded workspace reads the stored BASELINE report back from MongoDB

```text
HTTP 200 
X-Request-Id: a0f30dab-9467-491e-a477-9b13c7b4791f
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337195
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:55 GMT
Connection: close

{"messages":null,"payload":{"id":"pilot-0","version":2,"accountId":"2ac66d3b-89c2-4e64-98be-c26b739e04b1","generation":"faefd0e9-3638-46ad-9d04-a866d0a6d6e0","sites":[{"id":"695de744-10c4-457e-b5b5-ed7becb3be9c","label":"Demonstration website","origin":"https://www.christopherbell.dev","paths":["/","/zip-coordinates","/vin-decoder"],"token":"c97b82b3-fc68-4a40-96b5-1700691e46c4-b0877bd4-d5c9-4ae1-9c01-988deb0ff91a","demo":true,"verifiedOn":"2026-10-07T01:38:55.148Z","lastAttempt":"2026-10-07T01:38:51.844Z","baselineOn":"2026-10-07T01:38:55.148Z","baseline":[{"path":"/","status":200,"finalUrl":"https://www.christopherbell.dev/","title":"CB | Home","description":"A working corner of the internet for Void posts, lunch picks, and practical utilities.","canonical":"https://www.christopherbell.dev/","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/zip-coordinates","status":200,"finalUrl":"https://www.christopherbell.dev/zip-coordinates","title":"ZIP Coordinates","description":"Look up Census ZIP coordinate origins from christopherbell.dev.","canonical":"https://www.christopherbell.dev/zip-coordinates","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/vin-decoder","status":200,"finalUrl":"https://www.christopherbell.dev/vin-decoder","title":"VIN Decoder","description":"Paste a VIN and get a clean NHTSA-backed decode with summary fields and JSON.","canonical":"https://www.christopherbell.dev/vin-decoder","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false}],"reports":[{"id":"595fd365-0ead-43d6-8bb8-510c22e8919f","checkedOn":"2026-10-07T01:38:55.148Z","baselineOn":"2026-10-07T01:38:55.148Z","status":"BASELINE","findings":[],"pages":[{"path":"/","status":200,"finalUrl":"https://www.christopherbell.dev/","title":"CB | Home","description":"A working corner of the internet for Void posts, lunch picks, and practical utilities.","canonical":"https://www.christopherbell.dev/","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/zip-coordinates","status":200,"finalUrl":"https://www.christopherbell.dev/zip-coordinates","title":"ZIP Coordinates","description":"Look up Census ZIP coordinate origins from christopherbell.dev.","canonical":"https://www.christopherbell.dev/zip-coordinates","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false},{"path":"/vin-decoder","status":200,"finalUrl":"https://www.christopherbell.dev/vin-decoder","title":"VIN Decoder","description":"Paste a VIN and get a clean NHTSA-backed decode with summary fields and JSON.","canonical":"https://www.christopherbell.dev/vin-decoder","robots":"meta: ; header:","failedAssets":[],"checkedAssets":3,"omittedAssets":1,"problem":"","repeatedFailure":false}]}]}]},"requestId":null,"success":true}
```

### 9. Immediate re-check is refused with 429 (cooldown)

```text
HTTP 429 
X-Request-Id: 0c60bb81-df7f-4b86-862c-f535e5ad847d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 5
X-RateLimit-Reset: 1791337195
Cache-Control: no-store
Retry-After: 900
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:55 GMT
Connection: close

{"messages":[{"code":"SITE_MONITOR_REJECTED","description":"Checks are available once every 15 minutes per site."}],"payload":null,"requestId":null,"success":false}
```

### 10. Download the plain-text client report

<details><summary>33 lines</summary>

```text
HTTP 200 
X-Request-Id: 9740deff-fbfa-4e92-b7d1-e637ffce83cc
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337195
Cache-Control: no-store
Content-Disposition: attachment; filename=website-monitor-report.txt
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/plain;charset=UTF-8
Content-Length: 592
Date: Wed, 07 Oct 2026 01:38:55 GMT
Connection: close

Website Monitor — client report
Site: Demonstration website
Origin: https://www.christopherbell.dev
Baseline: 2026-10-07T01:38:55.148Z
Checked: 2026-10-07T01:38:55.148Z
Result: BASELINE

Coverage: configured HTML pages and up to ten same-origin assets using HEAD.
External/query assets, rendered layout, forms, logins and checkout are untested.
HEALTHY means these bounded checks passed; it is not an uptime or security guarantee.

/ — HTTP 200; assets checked 3, omitted 1
/zip-coordinates — HTTP 200; assets checked 3, omitted 1
/vin-decoder — HTTP 200; assets checked 3, omitted 1
```

</details>

### 11. Removing the only site empties the workspace

```text
HTTP 200 
X-Request-Id: 8070926d-3e10-4e57-afc1-8dc62dddf020
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 4
X-RateLimit-Reset: 1791337195
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:38:55 GMT
Connection: close

{"messages":null,"payload":{"id":null,"version":null,"accountId":"2ac66d3b-89c2-4e64-98be-c26b739e04b1","generation":null,"sites":[]},"requestId":null,"success":true}
```

### 12. Anonymous workspace read gets the same 403 status and body as production (timestamp ignored)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/site-monitor/v1'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/site-monitor/v1'}
```

## Evidence
- Case 1 started 2026-10-06T20:38:49-05:00, took 32 ms, candidate `e5ad16d`
- Case 2 started 2026-10-06T20:38:50-05:00, took 515 ms, candidate `unknown`
- Case 3 started 2026-10-06T20:38:50-05:00, took 62 ms, candidate `e5ad16d`
- Case 4 started 2026-10-06T20:38:51-05:00, took 94 ms, candidate `e5ad16d`
- Case 5 started 2026-10-06T20:38:51-05:00, took 62 ms, candidate `e5ad16d`
- Case 6 started 2026-10-06T20:38:51-05:00, took 62 ms, candidate `e5ad16d`
- Case 7 started 2026-10-06T20:38:51-05:00, took 3375 ms, candidate `e5ad16d`
- Case 8 started 2026-10-06T20:38:55-05:00, took 30 ms, candidate `e5ad16d`
- Case 9 started 2026-10-06T20:38:55-05:00, took 62 ms, candidate `e5ad16d`
- Case 10 started 2026-10-06T20:38:55-05:00, took 30 ms, candidate `e5ad16d`
- Case 11 started 2026-10-06T20:38:55-05:00, took 62 ms, candidate `e5ad16d`
- Case 12 started 2026-10-06T20:39:03-05:00, took 217 ms, candidate `unknown`

## Bugs / Follow-ups
- **Native checks on the candidate:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 5m07s. Java: 2,256 tests, 0 failures or errors, 110 skipped. Sitemonitor suites: controller 4/4, transport 2/2, `MonitorPolicyTest` 27/27, gateway 2/2, scanner 5/5 and service 8/8. The Mongo integration test is skipped without its database, as in CI. 390 JS tests and the Pester suites passed.
- **Cooldown header:** the 429 response included `Retry-After: 900`; see the response captured in that case.
- **Harness note:** the first anonymous-read case expected 401, which is what the controller slice test sees through its test-only security config. The real application returns 403, and production returns the same 403 body. The case was rerecorded as a production comparison, and the wrong-expectation artifact is excluded above.
- **Not exercised at runtime:** a scheduled check and a comparison that produces `CHANGES`. Both need time to pass, and the service and Mongo integration tests cover them with a controlled clock.

## Document Status
complete

## Project
christopherbell-dev
