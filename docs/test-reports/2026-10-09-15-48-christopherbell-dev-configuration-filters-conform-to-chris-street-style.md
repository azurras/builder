# Configuration filters conform to Chris Street Style: Test Report

## Story/Issue
Slice 18b of the style migration ([plan](../implementation-plans/2026-10-09-15-31-christopherbell-dev-configuration-filters-conform-to-chris-street-style.md)): rate limiting, request size limits, correlation ids and static caching behave as before

## Branch
``claude/style-config-filter-20261009` at candidate `95b7e542`` at candidate `95b7e54`

## Pass / Fail

> [!TIP]
> 3 of 3 cases passed on candidate `95b7e54`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (both filters built through the remaining constructors) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Rate-limit headers, correlation ids, login throttling and the 1 MB request limit behave as before | ✅ PASS | Expected exit code 0 |
| 3 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (both filters built through the remaining constructors)**: http `GET http://127.0.0.1:61099/actuator/health/readiness`
2. **Rate-limit headers, correlation ids, login throttling and the 1 MB request limit behave as before**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/filter_checks.py http://127.0.0.1:61099`
3. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-090358a3c57c4ba384f2ccfe80fc9bc3/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:61099, commit 95b7e542 |
| Credentials | none; login attempts used a nonexistent username and an invented password, and every attempt was rejected |
| Earlier runs | two runs of the filter case on the same candidate were discarded because the 413 check targeted the wrong endpoint, not because of the application: first posts/create, where security rejected the anonymous request with 403 before the size limit applied, then the VIN decoder, where CSRF rejected the anonymous POST with 403. The CSRF-exempt login endpoint reaches the size filter, which runs before the rate limiter. Each rerun waited 75 seconds for the login bucket to refill |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:61099/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-config-filter`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/filter_checks.py http://127.0.0.1:61099` in `A:\Projects\christopherbell.dev-worktrees\style-config-filter`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-090358a3c57c4ba384f2ccfe80fc9bc3/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-config-filter`
- **Candidate identity:** `95b7e54`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (both filters built through the remaining constructors)

```http
GET http://127.0.0.1:61099/actuator/health/readiness
```

### 2. Rate-limit headers, correlation ids, login throttling and the 1 MB request limit behave as before

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/filter_checks.py http://127.0.0.1:61099
```

### 3. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-090358a3c57c4ba384f2ccfe80fc9bc3/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (both filters built through the remaining constructors)

```text
HTTP 200 
X-Request-Id: 47206010-28cd-4f57-bde0-c79b34c1f4ac
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791578845
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
Date: Fri, 09 Oct 2026 20:46:25 GMT
Connection: close

{"status":"UP"}
```

### 2. Rate-limit headers, correlation ids, login throttling and the 1 MB request limit behave as before

```text
exit code: 0
--- stdout ---
PASS a response carries rate-limit headers: 200 {'X-RateLimit-Limit': '10000', 'X-RateLimit-Remaining': '9999', 'X-RateLimit-Reset': '1791578846'}
PASS a response carries a request correlation id: X-Request-Id present: True
PASS the first 20 failed logins in a minute are answered, not throttled: [400]
PASS the 21st login in a minute is throttled with Retry-After and RATE_LIMITED: 429 Retry-After=3 codes=['RATE_LIMITED']
PASS a JSON body over the 1 MB default limit on the CSRF-exempt login endpoint gets 413 REQUEST_TOO_LARGE: 413 codes=['REQUEST_TOO_LARGE']
```

### 3. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T15:46:25-05:00, took 32 ms, candidate `95b7e54`
- Case 2 started 2026-10-09T15:46:26-05:00, took 186 ms, candidate `95b7e54`
- Case 3 started 2026-10-09T15:46:26-05:00, took 31 ms, candidate `95b7e54`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
