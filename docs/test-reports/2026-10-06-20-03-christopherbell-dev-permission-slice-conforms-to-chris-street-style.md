# Permission slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 3 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-19-43-christopherbell-dev-permission-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-permission-20261006` at candidate `1436d1d`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `1436d1d`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (LoginTokens bean built at startup) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create a USER account through the API and log in (password generated per run, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Bearer login token reads the signed-in account | ✅ PASS | Expected status 200 and body containing '"style_check"' |
| 4 | USER bearer token is denied the ADMIN account list | ✅ PASS | Expected status 403 |
| 5 | Tampered bearer token is rejected | ✅ PASS | Expected status 401 |
| 6 | Request without a token gets the same 403 status and body as production (timestamp ignored; JSON Accept header) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (LoginTokens bean built at startup)**: http `GET http://127.0.0.1:54795/actuator/health/readiness`
2. **Create a USER account through the API and log in (password generated per run, not recorded)**: command `python permission_signup_login.py http://127.0.0.1:54795 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/permission-login-token.txt`
3. **Bearer login token reads the signed-in account**: http `GET http://127.0.0.1:54795/api/accounts/2025-09-03/me`
4. **USER bearer token is denied the ADMIN account list**: http `GET http://127.0.0.1:54795/api/accounts/2024-12-15`
5. **Tampered bearer token is rejected**: http `GET http://127.0.0.1:54795/api/accounts/2025-09-03/me`
6. **Request without a token gets the same 403 status and body as production (timestamp ignored; JSON Accept header)**: command `python compare_status_and_body.py http://127.0.0.1:54795/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:54794 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:54795, rebased on main c746d0e2 |
| Credentials | disposable account in the throwaway database; password generated per run and never recorded; bearer tokens masked by the recorder |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:54795/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-permission`
- **Local command:** `python permission_signup_login.py http://127.0.0.1:54795 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/permission-login-token.txt` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:54795/api/accounts/2025-09-03/me` in `A:\Projects\christopherbell.dev-worktrees\style-permission`
- **Local command:** `GET http://127.0.0.1:54795/api/accounts/2024-12-15` in `A:\Projects\christopherbell.dev-worktrees\style-permission`
- **Local command:** `GET http://127.0.0.1:54795/api/accounts/2025-09-03/me` in `A:\Projects\christopherbell.dev-worktrees\style-permission`
- **Local command:** `python compare_status_and_body.py http://127.0.0.1:54795/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Candidate identity:** `1436d1d`
- **Cleanup:** Stopped candidate PID 44660 and mongod PID 22796 by process tree; ports 54795 and 54794 have zero listeners; the scratch token file was deleted; production MongoDB 27017 (PID 5236) untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (LoginTokens bean built at startup)

```http
GET http://127.0.0.1:54795/actuator/health/readiness
```

### 2. Create a USER account through the API and log in (password generated per run, not recorded)

```text
python permission_signup_login.py http://127.0.0.1:54795 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/permission-login-token.txt
```

### 3. Bearer login token reads the signed-in account

```http
GET http://127.0.0.1:54795/api/accounts/2025-09-03/me
Authorization: [REDACTED]
```

### 4. USER bearer token is denied the ADMIN account list

```http
GET http://127.0.0.1:54795/api/accounts/2024-12-15
Authorization: [REDACTED]
```

### 5. Tampered bearer token is rejected

```http
GET http://127.0.0.1:54795/api/accounts/2025-09-03/me
Authorization: [REDACTED]
```

### 6. Request without a token gets the same 403 status and body as production (timestamp ignored; JSON Accept header)

```text
python compare_status_and_body.py http://127.0.0.1:54795/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (LoginTokens bean built at startup)

```text
HTTP 200 
X-Request-Id: 347b6dea-55eb-4f56-ba84-9a96aa2d1820
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335035
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
Date: Wed, 07 Oct 2026 01:02:55 GMT
Connection: close

{"status":"UP"}
```

### 2. Create a USER account through the API and log in (password generated per run, not recorded)

```text
exit code: 0
--- stdout ---
create status 201 username style_check role USER
login status 200 token segments 3
```

### 3. Bearer login token reads the signed-in account

```text
HTTP 200 
X-Request-Id: f1ce430d-a480-42e8-b639-d2218cf87155
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335036
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
Date: Wed, 07 Oct 2026 01:02:56 GMT
Connection: close

{"messages":null,"payload":{"id":"e52d23bc-60f8-4c94-ae73-91d4a984ae2f","createdBy":"anonymousUser","createdOn":"2026-10-07T01:02:56.262Z","email":"style-check@example.test","federationEnabled":false,"firstName":"Style","lastName":"Check","lastLoginOn":"2026-10-07T01:02:56.348Z","lastModifiedBy":"anonymousUser","lastUpdatedOn":"2026-10-07T01:02:56.262Z","role":"USER","permissions":[],"status":"ACTIVE","type":"account","username":"style_check"},"requestId":null,"success":true}
```

### 4. USER bearer token is denied the ADMIN account list

```text
HTTP 403 
X-Request-Id: 980c3ff7-184e-467b-824b-66c6d2d35d5f
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335036
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
Date: Wed, 07 Oct 2026 01:02:56 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 5. Tampered bearer token is rejected

```text
HTTP 401 
X-Request-Id: e42f42f1-875d-48a6-9fc3-afdf4808844d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335036
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Length: 0
Date: Wed, 07 Oct 2026 01:02:56 GMT
Connection: close
```

### 6. Request without a token gets the same 403 status and body as production (timestamp ignored; JSON Accept header)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2025-09-03/me'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2025-09-03/me'}
```

## Evidence
- Case 1 started 2026-10-06T20:02:55-05:00, took 31 ms, candidate `1436d1d`
- Case 2 started 2026-10-06T20:02:55-05:00, took 500 ms, candidate `unknown`
- Case 3 started 2026-10-06T20:02:56-05:00, took 46 ms, candidate `1436d1d`
- Case 4 started 2026-10-06T20:02:56-05:00, took 62 ms, candidate `1436d1d`
- Case 5 started 2026-10-06T20:02:56-05:00, took 46 ms, candidate `1436d1d`
- Case 6 started 2026-10-06T20:03:17-05:00, took 297 ms, candidate `unknown`

## Bugs / Follow-ups
- **Native checks on `1436d1d`:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m47s. Java: 2,256 tests, 0 failures or errors, 110 skipped. Focused suites: `LoginTokensTest` 11/11, `PermissionServiceTest` 15/15, `JwtAuthenticationFilterTest` 18/18, `BrowserSessionServiceTest` 24/24, `AccountServiceTest` 48/48 and `ModularMonolithArchitectureTest` 5/5. JS and Pester suites passed.
- **Architecture baseline:** two frozen violations (`configuration` to `permission.PermissionService`) were resolved and removed from the store. No entries were added.
- **Earlier attempts:**
  - The first full check failed on the frozen architecture rule and a test secret length. Both were fixed (see the plan log).
  - The first runtime run expected 401 for a request without a token. Production returns 403 for the same request, so the expectation was corrected. A comparison that raced the shutdown was rerun on a fresh candidate. Only the final run's cases are listed above.

## Document Status
complete

## Project
christopherbell-dev
