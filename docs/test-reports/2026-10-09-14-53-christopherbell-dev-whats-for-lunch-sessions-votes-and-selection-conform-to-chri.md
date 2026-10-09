# Whats for Lunch sessions votes and selection conform to Chris Street Style: Test Report

## Story/Issue
Slice 17c of the style migration ([plan](../implementation-plans/2026-10-09-14-46-christopherbell-dev-whats-for-lunch-sessions-votes-and-selection-conform-to-chri.md)): sessions, votes, favorites, preferences and selection behave as before

## Branch
``claude/style-lunch-sessions-20261009` at candidate `a6c1020e`` at candidate `a6c1020`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `a6c1020`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create lunch_b through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Preferences, favorites, session validation and missing-session paths behave as before for a USER | ✅ PASS | Expected exit code 0 |
| 4 | Top-liked restaurants (the vote-total aggregation) has production's shape | ✅ PASS | Expected exit code 0 |
| 5 | An anonymous session list gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 6 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:64409/actuator/health/readiness`
2. **Create lunch_b through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:64409 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_b`
3. **Preferences, favorites, session validation and missing-session paths behave as before for a USER**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:64409 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
4. **Top-liked restaurants (the vote-total aggregation) has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64409/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json`
5. **An anonymous session list gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64409/api/whatsforlunch/restaurant/2026-05-17/sessions https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/sessions 403`
6. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-90ea88efe782423b865548b031d2c4bd/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (monthly OpenStreetMap import disabled) |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:64409, commit a6c1020e |
| Credentials | one disposable USER; password generated and never recorded; token file deleted |
| Production | read-only GETs only (top-liked, anonymous session list) |
| Coverage limit | restaurants can only be created by an ADMIN or a live import, so a session with real picks cannot be built locally; WhatsForLunchSessionMutationStoreTest and the MusicAndLunch mutation-safety Mongo tests cover join, vote, reset, full, expired, not-participant, invalid-restaurant and not-host |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:64409/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:64409 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_b` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:64409 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64409/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-sessions`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64409/api/whatsforlunch/restaurant/2026-05-17/sessions https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/sessions 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-sessions`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-90ea88efe782423b865548b031d2c4bd/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-sessions`
- **Candidate identity:** `a6c1020`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token file deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:64409/actuator/health/readiness
```

### 2. Create lunch_b through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:64409 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_b
```

### 3. Preferences, favorites, session validation and missing-session paths behave as before for a USER

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:64409 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 4. Top-liked restaurants (the vote-total aggregation) has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64409/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json
```

### 5. An anonymous session list gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64409/api/whatsforlunch/restaurant/2026-05-17/sessions https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/sessions 403
```

### 6. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-90ea88efe782423b865548b031d2c4bd/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 0fb8df03-5690-4b47-9b90-0199ae2738ff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791575637
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
Date: Fri, 09 Oct 2026 19:52:57 GMT
Connection: close

{"status":"UP"}
```

### 2. Create lunch_b through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
lunch_b create 201 login 200
```

### 3. Preferences, favorites, session validation and missing-session paths behave as before for a USER

```text
exit code: 0
--- stdout ---
PASS the USER saves preferences (200, radius 10): got 200
PASS the USER reads the saved preferences back (200, radius 10): got 200
PASS the USER has no favorites (200, empty list): got 200
PASS the USER has no sessions (200, empty list): got 200
PASS a session with two picks is rejected (400): got 400
PASS a session with unknown restaurants is rejected (404): got 404
PASS a missing session read is rejected (404): got 404
PASS joining a missing session is rejected (404, classified MISSING): got 404
PASS voting in a missing session is rejected (404, classified MISSING): got 404
PASS a blank session vote is rejected (400): got 400
PASS an anonymous session list is rejected (403): got 403
```

### 4. Top-liked restaurants (the vote-total aggregation) has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 5. An anonymous session list gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2026-05-17/sessions'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2026-05-17/sessions'}
```

### 6. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T14:52:56-05:00, took 47 ms, candidate `a6c1020`
- Case 2 started 2026-10-09T14:52:57-05:00, took 797 ms, candidate `a6c1020`
- Case 3 started 2026-10-09T14:52:58-05:00, took 344 ms, candidate `a6c1020`
- Case 4 started 2026-10-09T14:52:58-05:00, took 172 ms, candidate `a6c1020`
- Case 5 started 2026-10-09T14:52:59-05:00, took 592 ms, candidate `a6c1020`
- Case 6 started 2026-10-09T14:52:59-05:00, took 47 ms, candidate `a6c1020`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
