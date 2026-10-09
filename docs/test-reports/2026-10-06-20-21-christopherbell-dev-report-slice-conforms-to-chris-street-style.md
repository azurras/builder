# Report slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 5 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-20-16-christopherbell-dev-report-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-report-20261006` at candidate `873fb78`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `873fb78`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create an author and a reporter through the API; the author posts (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Reporter submits a report and gets the stored OPEN report back (reportType SPAM from reason spam) | ✅ PASS | Expected status 200 and body containing '"status":"OPEN"' |
| 4 | A duplicate submission returns the same open report id instead of a second report | ✅ PASS | Expected status 200 and body containing '"id":"6ac59e6c6f71814d1cfa3c41"' |
| 5 | Original 2025-09-03 submission API accepts a report without returning a payload | ✅ PASS | Expected status 200 and body containing '"success":true' |
| 6 | USER is denied the admin report queue | ✅ PASS | Expected status 403 |
| 7 | Anonymous submission is rejected | ✅ PASS | Expected status 403 |
| 8 | USER is denied report resolution (valid CLOSE_NO_ACTION body) | ✅ PASS | Expected status 403 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:60172/actuator/health/readiness`
2. **Create an author and a reporter through the API; the author posts (passwords generated, not recorded)**: command `python report_fixture_accounts.py http://127.0.0.1:60172 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
3. **Reporter submits a report and gets the stored OPEN report back (reportType SPAM from reason spam)**: http `POST http://127.0.0.1:60172/api/reports/2026-07-26`
4. **A duplicate submission returns the same open report id instead of a second report**: http `POST http://127.0.0.1:60172/api/reports/2026-07-26`
5. **Original 2025-09-03 submission API accepts a report without returning a payload**: http `POST http://127.0.0.1:60172/api/reports/2025-09-03`
6. **USER is denied the admin report queue**: http `GET http://127.0.0.1:60172/api/reports/2026-07-26`
7. **Anonymous submission is rejected**: http `POST http://127.0.0.1:60172/api/reports/2026-07-26`
8. **USER is denied report resolution (valid CLOSE_NO_ACTION body)**: http `POST http://127.0.0.1:60172/api/reports/2025-09-03/6ac59e6c6f71814d1cfa3c41/resolve`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:60171 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:60172, rebased on main 17e24c43 |
| Credentials | disposable accounts in the throwaway database; passwords generated per run and never recorded; bearer tokens masked by the recorder |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:60172/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Local command:** `python report_fixture_accounts.py http://127.0.0.1:60172 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `POST http://127.0.0.1:60172/api/reports/2026-07-26` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Local command:** `POST http://127.0.0.1:60172/api/reports/2026-07-26` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Local command:** `POST http://127.0.0.1:60172/api/reports/2025-09-03` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Local command:** `GET http://127.0.0.1:60172/api/reports/2026-07-26` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Local command:** `POST http://127.0.0.1:60172/api/reports/2026-07-26` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Local command:** `POST http://127.0.0.1:60172/api/reports/2025-09-03/6ac59e6c6f71814d1cfa3c41/resolve` in `A:\Projects\christopherbell.dev-worktrees\style-report`
- **Candidate identity:** `873fb78`
- **Cleanup:** Stopped candidate PID 42332 and mongod PID 82404 by process tree; ports 60172 and 60171 have zero listeners; scratch token and id files deleted; production MongoDB 27017 (PID 5236) untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:60172/actuator/health/readiness
```

### 2. Create an author and a reporter through the API; the author posts (passwords generated, not recorded)

```text
python report_fixture_accounts.py http://127.0.0.1:60172 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 3. Reporter submits a report and gets the stored OPEN report back (reportType SPAM from reason spam)

```http
POST http://127.0.0.1:60172/api/reports/2026-07-26
Authorization: [REDACTED]
Content-Type: application/json

{"postId":"320bed37-e503-4fd9-82d4-1cd48e775ac2","reason":"spam","details":"local verification"}
```

### 4. A duplicate submission returns the same open report id instead of a second report

```http
POST http://127.0.0.1:60172/api/reports/2026-07-26
Authorization: [REDACTED]
Content-Type: application/json

{"postId":"320bed37-e503-4fd9-82d4-1cd48e775ac2","reason":"spam"}
```

### 5. Original 2025-09-03 submission API accepts a report without returning a payload

```http
POST http://127.0.0.1:60172/api/reports/2025-09-03
Authorization: [REDACTED]
Content-Type: application/json

{"postId":"320bed37-e503-4fd9-82d4-1cd48e775ac2","reason":"other"}
```

### 6. USER is denied the admin report queue

```http
GET http://127.0.0.1:60172/api/reports/2026-07-26
Authorization: [REDACTED]
```

### 7. Anonymous submission is rejected

```http
POST http://127.0.0.1:60172/api/reports/2026-07-26
Content-Type: application/json

{"postId":"320bed37-e503-4fd9-82d4-1cd48e775ac2","reason":"spam"}
```

### 8. USER is denied report resolution (valid CLOSE_NO_ACTION body)

```http
POST http://127.0.0.1:60172/api/reports/2025-09-03/6ac59e6c6f71814d1cfa3c41/resolve
Authorization: [REDACTED]
Content-Type: application/json

{"resolution":"CLOSE_NO_ACTION","reason":"USER must not resolve"}
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 7eb0028f-3844-4a5d-a907-6c9ce47e0ec6
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791336103
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
Date: Wed, 07 Oct 2026 01:20:43 GMT
Connection: close

{"status":"UP"}
```

### 2. Create an author and a reporter through the API; the author posts (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
report_author create 201 login 200
report_reporter create 201 login 200
post create 201 post id 320bed37-e503-4fd9-82d4-1cd48e775ac2
```

### 3. Reporter submits a report and gets the stored OPEN report back (reportType SPAM from reason spam)

```text
HTTP 200 
X-Request-Id: d156cafd-467a-4485-8f3b-35686770f114
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791336104
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
Date: Wed, 07 Oct 2026 01:20:44 GMT
Connection: close

{"messages":null,"payload":{"id":"6ac59e6c6f71814d1cfa3c41","postId":"320bed37-e503-4fd9-82d4-1cd48e775ac2","postText":"A post that will be reported during local verification.","reportedAccountId":"0c2aeda7-e88f-448d-af3c-d267c6bdd32c","reportedUsername":"report_author","reporterAccountId":"746b6a4e-fda5-423c-8da5-a3464832cb07","reporterUsername":"report_reporter","openDedupeKey":"61eb41e89cef9904ad6a209f382f5cf69fcaccb4708fb9df1b8e349b69570546","reportType":"SPAM","targetType":"POST","reason":"spam","details":"local verification","status":"OPEN","createdOn":"2026-10-07T01:20:44.361Z","lastUpdatedOn":"2026-10-07T01:20:44.361Z"},"requestId":null,"success":true}
```

### 4. A duplicate submission returns the same open report id instead of a second report

```text
HTTP 200 
X-Request-Id: 7dc31438-26d6-42de-8053-a32dc01a901c
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791336104
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
Date: Wed, 07 Oct 2026 01:20:44 GMT
Connection: close

{"messages":null,"payload":{"id":"6ac59e6c6f71814d1cfa3c41","postId":"320bed37-e503-4fd9-82d4-1cd48e775ac2","postText":"A post that will be reported during local verification.","reportedAccountId":"0c2aeda7-e88f-448d-af3c-d267c6bdd32c","reportedUsername":"report_author","reporterAccountId":"746b6a4e-fda5-423c-8da5-a3464832cb07","reporterUsername":"report_reporter","openDedupeKey":"61eb41e89cef9904ad6a209f382f5cf69fcaccb4708fb9df1b8e349b69570546","reportType":"SPAM","targetType":"POST","reason":"spam","details":"local verification","status":"OPEN","createdOn":"2026-10-07T01:20:44.361Z","lastUpdatedOn":"2026-10-07T01:20:44.361Z"},"requestId":null,"success":true}
```

### 5. Original 2025-09-03 submission API accepts a report without returning a payload

```text
HTTP 200 
X-Request-Id: a2b1c14c-153d-4d9c-baca-eca1d9781351
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791336104
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
Date: Wed, 07 Oct 2026 01:20:44 GMT
Connection: close

{"messages":null,"payload":null,"requestId":null,"success":true}
```

### 6. USER is denied the admin report queue

```text
HTTP 403 
X-Request-Id: 8acaedad-9cf6-42b8-b86a-ef7025cfe67b
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791336104
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
Date: Wed, 07 Oct 2026 01:20:44 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 7. Anonymous submission is rejected

```text
HTTP 403 
X-Request-Id: b94e3d0a-a19a-40eb-a686-be1dd87b22b6
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
Date: Wed, 07 Oct 2026 01:20:45 GMT
Connection: close

{"timestamp":"2026-10-07T01:20:45.271Z","status":403,"error":"Forbidden","path":"/api/reports/2026-07-26"}
```

### 8. USER is denied report resolution (valid CLOSE_NO_ACTION body)

```text
HTTP 403 
X-Request-Id: 2be764f2-e800-4337-88cf-c2161d06cac8
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791336119
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
Date: Wed, 07 Oct 2026 01:20:59 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

## Evidence
- Case 1 started 2026-10-06T20:20:43-05:00, took 32 ms, candidate `873fb78`
- Case 2 started 2026-10-06T20:20:43-05:00, took 703 ms, candidate `unknown`
- Case 3 started 2026-10-06T20:20:44-05:00, took 62 ms, candidate `873fb78`
- Case 4 started 2026-10-06T20:20:44-05:00, took 47 ms, candidate `873fb78`
- Case 5 started 2026-10-06T20:20:44-05:00, took 31 ms, candidate `873fb78`
- Case 6 started 2026-10-06T20:20:44-05:00, took 46 ms, candidate `873fb78`
- Case 7 started 2026-10-06T20:20:45-05:00, took 46 ms, candidate `873fb78`
- Case 8 started 2026-10-06T20:20:59-05:00, took 30 ms, candidate `873fb78`

## Bugs / Follow-ups
- **Native checks on `873fb78`:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m49s. Java: 2,256 tests, 0 failures or errors, 110 skipped. Report suites: controller 4/4, service 4/4, moderation lifecycle 4/4, query 3/3 and submission 3/3; the Mongo contract test is skipped as it is in CI. 390 JS tests passed, and the Pester suites passed.
- **Harness note:** the first resolve-denial case sent the invalid resolution `DISMISS` and got 400 from request parsing before authorization. It was rerun with a fresh USER and the valid `CLOSE_NO_ACTION`, and returned 403. The invalid case is excluded above.
- **Not exercised at runtime: ADMIN moderation** (queue contents, resolve, reopen, delete, suspend), because there is no supported local ADMIN. `ReportModerationLifecycleTest` and `ReportServiceTest` prove it.

## Document Status
complete

## Project
christopherbell-dev
