# Browser sessions conform to Chris Street Style: Test Report

## Story/Issue
Slice 18d of the style migration ([plan](../implementation-plans/2026-10-09-15-54-christopherbell-dev-browser-sessions-conform-to-chris-street-style.md)): browser session creation, authentication, renewal and revocation behave as before

## Branch
``claude/style-browser-sessions-20261009` at candidate `92bc169e`` at candidate `92bc169`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `92bc169`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Sign-up, cookie login, /me through the session cookie, logout revocation and password reset behave as before (generated password, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Forged, short and malformed session cookies are rejected (401) and cleared | ✅ PASS | Expected exit code 0 |
| 4 | Create sec_b through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 5 | A fresh cookie session authenticates /me and enforces CSRF on a mutation; bearer and public matchers unchanged | ✅ PASS | Expected exit code 0 |
| 6 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:52711/actuator/health/readiness`
2. **Sign-up, cookie login, /me through the session cookie, logout revocation and password reset behave as before (generated password, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/account_checks.py http://127.0.0.1:52711`
3. **Forged, short and malformed session cookies are rejected (401) and cleared**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/cookie_tamper_checks.py http://127.0.0.1:52711`
4. **Create sec_b through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:52711 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_b`
5. **A fresh cookie session authenticates /me and enforces CSRF on a mutation; bearer and public matchers unchanged**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/security_checks.py http://127.0.0.1:52711 https://www.christopherbell.dev C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_b`
6. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a5ceb872a87047cd824a8aead7934767/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:52711, commit 92bc169e |
| Credentials | disposable USERs; passwords generated per run and never recorded; bearer tokens masked; token files deleted |
| Production | read-only GET of / for header comparison |
| Coverage limit | daily rotation and the lost-rotation race need a day of clock time or two racing requests; BrowserSessionServiceTest covers rotation, overlap, expiry and activity writes |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:52711/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-browser-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/account_checks.py http://127.0.0.1:52711` in `A:\Projects\christopherbell.dev-worktrees\style-browser-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/cookie_tamper_checks.py http://127.0.0.1:52711` in `A:\Projects\christopherbell.dev-worktrees\style-browser-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:52711 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_b` in `A:\Projects\christopherbell.dev-worktrees\style-browser-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/security_checks.py http://127.0.0.1:52711 https://www.christopherbell.dev C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_b` in `A:\Projects\christopherbell.dev-worktrees\style-browser-sessions`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a5ceb872a87047cd824a8aead7934767/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-browser-sessions`
- **Candidate identity:** `92bc169`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token files deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:52711/actuator/health/readiness
```

### 2. Sign-up, cookie login, /me through the session cookie, logout revocation and password reset behave as before (generated password, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/account_checks.py http://127.0.0.1:52711
```

### 3. Forged, short and malformed session cookies are rejected (401) and cleared

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/cookie_tamper_checks.py http://127.0.0.1:52711
```

### 4. Create sec_b through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:52711 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_b
```

### 5. A fresh cookie session authenticates /me and enforces CSRF on a mutation; bearer and public matchers unchanged

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/security_checks.py http://127.0.0.1:52711 https://www.christopherbell.dev C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_b
```

### 6. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-a5ceb872a87047cd824a8aead7934767/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 4180ae4f-b8df-4167-a4b4-8af5ca0c3be5
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791579781
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
Date: Fri, 09 Oct 2026 21:02:01 GMT
Connection: close

{"status":"UP"}
```

### 2. Sign-up, cookie login, /me through the session cookie, logout revocation and password reset behave as before (generated password, not recorded)

```text
exit code: 0
--- stdout ---
PASS sign-up creates acct_cookie (201)
PASS a wrong password is rejected as INVALID_TOKEN (401)
PASS cookie-mode login with a differently cased email returns no token payload (200)
PASS cookie-mode login sets an HttpOnly session cookie
PASS the session cookie authenticates /me as acct_cookie (200)
PASS logout succeeds and clears the session cookie (200)
PASS /me is rejected after logout (403)
PASS a reset request for a real account gets the generic reply (200)
PASS a reset request for an unknown email gets the same generic reply (200)
PASS a bogus reset token is rejected as INVALID_TOKEN (401)
```

### 3. Forged, short and malformed session cookies are rejected (401) and cleared

```text
exit code: 0
--- stdout ---
PASS a well-formed cookie for an unknown session is rejected (401) and cleared: 401 cleared=True
PASS a cookie whose secret is too short is rejected (401) and cleared: 401 cleared=True
PASS a cookie without a session id separator is rejected (401) and cleared: 401 cleared=True
```

### 4. Create sec_b through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
sec_b create 201 login 200
```

### 5. A fresh cookie session authenticates /me and enforces CSRF on a mutation; bearer and public matchers unchanged

```text
exit code: 0
--- stdout ---
PASS a valid Bearer [REDACTED] authenticates /me: 200
PASS a forged Bearer [REDACTED] is rejected on a protected route (401): 401
PASS an anonymous /me is rejected (403): 403
PASS an anonymous single-post read passes security and reaches the 404: 404
PASS the reserved /api/posts/.../me path is not public (403): 403
PASS a two-segment post path is not public (403): 403
PASS sign-up creates a cookie account with a generated password (201): 201
PASS cookie-mode login sets an HttpOnly session cookie: 200
PASS the session cookie authenticates /me: 200
PASS a cookie-authenticated mutation without the CSRF header is refused (403): 403
PASS the same mutation with the CSRF header succeeds (201): 201
PASS Content-Security-Policy matches production: same
PASS Permissions-Policy matches production: same
PASS Referrer-Policy matches production: same
PASS X-Content-Type-Options matches production: same
PASS X-Frame-Options matches production: same
```

### 6. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T16:02:01-05:00, took 30 ms, candidate `92bc169`
- Case 2 started 2026-10-09T16:02:02-05:00, took 1016 ms, candidate `92bc169`
- Case 3 started 2026-10-09T16:02:03-05:00, took 139 ms, candidate `92bc169`
- Case 4 started 2026-10-09T16:02:03-05:00, took 297 ms, candidate `92bc169`
- Case 5 started 2026-10-09T16:02:04-05:00, took 890 ms, candidate `92bc169`
- Case 6 started 2026-10-09T16:02:05-05:00, took 31 ms, candidate `92bc169`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
