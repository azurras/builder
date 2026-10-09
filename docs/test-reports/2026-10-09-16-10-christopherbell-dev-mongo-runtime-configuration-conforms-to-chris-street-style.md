# Mongo runtime configuration conforms to Chris Street Style: Test Report

## Story/Issue
Slice 18e of the style migration ([plan](../implementation-plans/2026-10-09-16-01-christopherbell-dev-mongo-runtime-configuration-conforms-to-chris-street-style.md)): auditing, application leases and collector history behave as before

## Branch
``claude/style-mongo-runtime-20261009` at candidate `47b65feb`` at candidate `47b65fe`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `47b65fe`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (startup migrations acquired and released the application lease) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create audit_a through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Mongo auditing set the new account's createdOn and lastUpdatedOn from the application clock | ✅ PASS | Expected exit code 0 |
| 4 | Candidate log has no ERROR lines, and no lease or collector warnings | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (startup migrations acquired and released the application lease)**: http `GET http://127.0.0.1:62163/actuator/health/readiness`
2. **Create audit_a through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:62163 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad audit_a`
3. **Mongo auditing set the new account's createdOn and lastUpdatedOn from the application clock**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/auditing_checks.py http://127.0.0.1:62163 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad audit_a`
4. **Candidate log has no ERROR lines, and no lease or collector warnings**: command `python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-f52336bad2b24358a0d61415d6101443/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or (' WARN ' in l and ('lease' in l.lower() or 'collector' in l.lower()))];print('matching lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:62163, commit 47b65feb |
| Credentials | one disposable USER; password generated and never recorded; bearer token masked; token file deleted |
| Coverage limit | lease contention and fenced renewal need concurrent owners; the remaining-domain Mongo contract tests cover them |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:62163/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-runtime`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:62163 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad audit_a` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-runtime`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/auditing_checks.py http://127.0.0.1:62163 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad audit_a` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-runtime`
- **Local command:** `python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-f52336bad2b24358a0d61415d6101443/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or (' WARN ' in l and ('lease' in l.lower() or 'collector' in l.lower()))];print('matching lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-runtime`
- **Candidate identity:** `47b65fe`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token file deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (startup migrations acquired and released the application lease)

```http
GET http://127.0.0.1:62163/actuator/health/readiness
```

### 2. Create audit_a through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:62163 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad audit_a
```

### 3. Mongo auditing set the new account's createdOn and lastUpdatedOn from the application clock

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/auditing_checks.py http://127.0.0.1:62163 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad audit_a
```

### 4. Candidate log has no ERROR lines, and no lease or collector warnings

```text
python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-f52336bad2b24358a0d61415d6101443/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or (' WARN ' in l and ('lease' in l.lower() or 'collector' in l.lower()))];print('matching lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (startup migrations acquired and released the application lease)

```text
HTTP 200 
X-Request-Id: dc4268c1-eb2b-4648-b07d-9c81cc56f485
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791580277
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
Date: Fri, 09 Oct 2026 21:10:17 GMT
Connection: close

{"status":"UP"}
```

### 2. Create audit_a through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
audit_a create 201 login 200
```

### 3. Mongo auditing set the new account's createdOn and lastUpdatedOn from the application clock

```text
exit code: 0
--- stdout ---
PASS auditing set createdOn to the current time: present=True recent=True
PASS auditing set lastUpdatedOn to the current time: present=True recent=True
```

### 4. Candidate log has no ERROR lines, and no lease or collector warnings

```text
exit code: 0
--- stdout ---
matching lines: 0
```

## Evidence
- Case 1 started 2026-10-09T16:10:17-05:00, took 32 ms, candidate `47b65fe`
- Case 2 started 2026-10-09T16:10:17-05:00, took 655 ms, candidate `47b65fe`
- Case 3 started 2026-10-09T16:10:18-05:00, took 156 ms, candidate `47b65fe`
- Case 4 started 2026-10-09T16:10:18-05:00, took 47 ms, candidate `47b65fe`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
