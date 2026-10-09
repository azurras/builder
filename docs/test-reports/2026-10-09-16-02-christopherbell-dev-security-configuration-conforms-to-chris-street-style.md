# Security configuration conforms to Chris Street Style: Test Report

## Story/Issue
Slice 18c of the style migration ([plan](../implementation-plans/2026-10-09-15-50-christopherbell-dev-security-configuration-conforms-to-chris-street-style.md)): authentication, CSRF, headers, public routes and rate limiting behave as before

## Branch
``claude/style-config-security-20261009` at candidate `2cd4670a`` at candidate `2cd4670`

## Pass / Fail

> [!TIP]
> 5 of 5 cases passed on candidate `2cd4670`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (rate-limit and browser-session beans built with the application Clock) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create sec_c through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Bearer, forged bearer, cookie session, CSRF, public post matchers and security headers behave as before | ✅ PASS | Expected exit code 0 |
| 4 | An anonymous /me gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 5 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (rate-limit and browser-session beans built with the application Clock)**: http `GET http://127.0.0.1:61911/actuator/health/readiness`
2. **Create sec_c through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:61911 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_c`
3. **Bearer, forged bearer, cookie session, CSRF, public post matchers and security headers behave as before**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/security_checks.py http://127.0.0.1:61911 https://www.christopherbell.dev C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_c`
4. **An anonymous /me gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:61911/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403`
5. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-96b85dd997dd4407848994e8ece12364/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:61911, commit 2cd4670a |
| Credentials | disposable USERs; passwords generated per run and never recorded; bearer tokens masked; token files deleted |
| Production | read-only GETs only (/, anonymous /me) |
| Earlier run | a first run on the same candidate was discarded: production was restarting for the slice 17f deploy and answered with a Cloudflare 502, so the header and anonymous /me comparisons compared against an error page. Every candidate-only check passed in that run too. The comparisons were rerun once production answered 200 |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:61911/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-config-security`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:61911 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_c` in `A:\Projects\christopherbell.dev-worktrees\style-config-security`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/security_checks.py http://127.0.0.1:61911 https://www.christopherbell.dev C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_c` in `A:\Projects\christopherbell.dev-worktrees\style-config-security`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:61911/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403` in `A:\Projects\christopherbell.dev-worktrees\style-config-security`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-96b85dd997dd4407848994e8ece12364/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-config-security`
- **Candidate identity:** `2cd4670`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token files deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (rate-limit and browser-session beans built with the application Clock)

```http
GET http://127.0.0.1:61911/actuator/health/readiness
```

### 2. Create sec_c through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:61911 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_c
```

### 3. Bearer, forged bearer, cookie session, CSRF, public post matchers and security headers behave as before

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/security_checks.py http://127.0.0.1:61911 https://www.christopherbell.dev C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad sec_c
```

### 4. An anonymous /me gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:61911/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403
```

### 5. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-96b85dd997dd4407848994e8ece12364/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (rate-limit and browser-session beans built with the application Clock)

```text
HTTP 200 
X-Request-Id: 6d3dddfd-2441-47ab-b9a6-6e7133c8adb3
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791579798
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
Date: Fri, 09 Oct 2026 21:02:18 GMT
Connection: close

{"status":"UP"}
```

### 2. Create sec_c through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
sec_c create 201 login 200
```

### 3. Bearer, forged bearer, cookie session, CSRF, public post matchers and security headers behave as before

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

### 4. An anonymous /me gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2025-09-03/me'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2025-09-03/me'}
```

### 5. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T16:02:18-05:00, took 30 ms, candidate `2cd4670`
- Case 2 started 2026-10-09T16:02:18-05:00, took 281 ms, candidate `2cd4670`
- Case 3 started 2026-10-09T16:02:19-05:00, took 858 ms, candidate `2cd4670`
- Case 4 started 2026-10-09T16:02:20-05:00, took 389 ms, candidate `2cd4670`
- Case 5 started 2026-10-09T16:02:20-05:00, took 47 ms, candidate `2cd4670`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
