# Whats for Lunch restaurant controller conforms to Chris Street Style: Test Report

## Story/Issue
Slice 17f of the style migration ([plan](../implementation-plans/2026-10-09-15-19-christopherbell-dev-whats-for-lunch-restaurant-controller-conforms-to-chris-stre.md)): every lunch route answers as before

## Branch
``claude/style-lunch-controller-20261009` at candidate `8da0de0f`` at candidate `8da0de0`

## Pass / Fail

> [!TIP]
> 16 of 16 cases passed on candidate `8da0de0`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | The What's for Lunch page renders | ✅ PASS | Expected status 200 and body containing "What's For Lunch" |
| 3 | Public source freshness has production's shape | ✅ PASS | Expected exit code 0 |
| 4 | Restaurant of the day has production's shape | ✅ PASS | Expected exit code 0 |
| 5 | An anonymous restaurant list gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 6 | An anonymous import status read gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 7 | An anonymous import preview is rejected (403) | ✅ PASS | Expected status 403 |
| 8 | Top-liked restaurants has production's shape | ✅ PASS | Expected exit code 0 |
| 9 | Anonymous nearby picks for Austin have production's shape | ✅ PASS | Expected exit code 0 |
| 10 | Nearby picks with an invalid latitude gets the same status and body as production (400) | ✅ PASS | Expected exit code 0 |
| 11 | Nearby picks for a malformed ZIP gets the same status and body as production (400) | ✅ PASS | Expected exit code 0 |
| 12 | An unknown public restaurant profile gets the same status and body as production (404) | ✅ PASS | Expected exit code 0 |
| 13 | Create lunch_b and lunch_d through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 14 | A USER's preferences, nearby picks, favorites and votes behave as before, and ADMIN routes reject the USER | ✅ PASS | Expected exit code 0 |
| 15 | A USER's session validation and missing-session paths behave as before | ✅ PASS | Expected exit code 0 |
| 16 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:64535/actuator/health/readiness`
2. **The What's for Lunch page renders**: http `GET http://127.0.0.1:64535/wfl`
3. **Public source freshness has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json`
4. **Restaurant of the day has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json`
5. **An anonymous restaurant list gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403`
6. **An anonymous import status read gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403`
7. **An anonymous import preview is rejected (403)**: http `POST http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview`
8. **Top-liked restaurants has production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json`
9. **Anonymous nearby picks for Austin have production's shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=30.27&longitude=-97.74&radiusMiles=15 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-nearby.json application/json`
10. **Nearby picks with an invalid latitude gets the same status and body as production (400)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=999&longitude=0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=999&longitude=0 400`
11. **Nearby picks for a malformed ZIP gets the same status and body as production (400)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/abcde https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/abcde 400`
12. **An unknown public restaurant profile gets the same status and body as production (404)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 404`
13. **Create lunch_b and lunch_d through the API and log both in (passwords generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_b lunch_d`
14. **A USER's preferences, nearby picks, favorites and votes behave as before, and ADMIN routes reject the USER**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_service_checks.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
15. **A USER's session validation and missing-session paths behave as before**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
16. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-fb621a488eeb43b9becb622047821885/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (monthly OpenStreetMap import disabled) |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:64535, commit 8da0de0f |
| Credentials | two disposable USERs; passwords generated and never recorded; token files deleted |
| Production | read-only GETs only |
| Coverage limit | ADMIN success paths need an ADMIN, which has no supported local path; RestaurantControllerTest covers them |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:64535/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `GET http://127.0.0.1:64535/wfl` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `POST http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=30.27&longitude=-97.74&radiusMiles=15 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-nearby.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=999&longitude=0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=999&longitude=0 400` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/abcde https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/abcde 400` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 404` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_b lunch_d` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_service_checks.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-fb621a488eeb43b9becb622047821885/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-controller`
- **Candidate identity:** `8da0de0`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token files deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:64535/actuator/health/readiness
```

### 2. The What's for Lunch page renders

```http
GET http://127.0.0.1:64535/wfl
```

### 3. Public source freshness has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/freshness C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-freshness.json application/json
```

### 4. Restaurant of the day has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/today C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-today.json application/json
```

### 5. An anonymous restaurant list gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2025-09-12 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2025-09-12 403
```

### 6. An anonymous import status read gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status 403
```

### 7. An anonymous import preview is rejected (403)

```http
POST http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview
```

### 8. Top-liked restaurants has production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/top-liked C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-top-liked.json application/json
```

### 9. Anonymous nearby picks for Austin have production's shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=30.27&longitude=-97.74&radiusMiles=15 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch-prod-nearby.json application/json
```

### 10. Nearby picks with an invalid latitude gets the same status and body as production (400)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=999&longitude=0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/nearby?latitude=999&longitude=0 400
```

### 11. Nearby picks for a malformed ZIP gets the same status and body as production (400)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/abcde https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/nearby/zip/abcde 400
```

### 12. An unknown public restaurant profile gets the same status and body as production (404)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:64535/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 https://www.christopherbell.dev/api/whatsforlunch/restaurant/2026-05-17/profile/osm:node:0 404
```

### 13. Create lunch_b and lunch_d through the API and log both in (passwords generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad lunch_b lunch_d
```

### 14. A USER's preferences, nearby picks, favorites and votes behave as before, and ADMIN routes reject the USER

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_service_checks.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 15. A USER's session validation and missing-session paths behave as before

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:64535 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 16. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-fb621a488eeb43b9becb622047821885/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 9d082dc8-cbaa-4dd9-b72d-68d7fb6174fd
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791577631
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
Date: Fri, 09 Oct 2026 20:26:11 GMT
Connection: close

{"status":"UP"}
```

### 2. The What's for Lunch page renders

<details><summary>84 lines</summary>

```text
HTTP 200 
X-Request-Id: df5dea9d-638b-4f4c-8b39-127e0391cc40
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791577631
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
Date: Fri, 09 Oct 2026 20:26:11 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell (cbell7@icloud.com)" />
    <meta name="keywords" content="cbell,blog" />
    
    <meta name="description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    
    <link rel="canonical" href="https://www.christopherbell.dev/wfl" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | What&#39;s For Lunch?" />
    <meta property="og:description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    <meta property="og:url" content="https://www.christopherbell.dev/wfl" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | What&#39;s For Lunch?" />
    <meta name="twitter:description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  

    <title>CB | What's For Lunch?</title>

    <link rel="stylesheet" type="text/css" href="/006e602dbdf934d741c3/css/main.css"/>
    <link rel="stylesheet" type="text/css" href="/006e602dbdf934d741c3/css/whats-for-lunch.css"/>
</head>

<body class="site-page void-shell-page lunch-page lunch-void-page">
    <div id="nav"></div>
    <main class="site-main lunch-void-main" aria-labelledby="lunchTitle">
        <div class="lunch-void-shell">
            <div class="container lunch-void-container">
                <header class="lunch-void-hero">
                    <p class="home-kicker">Decision console</p>
                    <h1 id="lunchTitle">What's For Lunch?</h1>
                    <p>Three signals. One good decision.</p>
                </header>
                <section class="lunch-void-console" aria-label="Lunch decision console">
                    <div id="whats-for-lunch"></div>
                </section>
            </div>
        </div>
    </main>
    <footer id="footer"></footer>
</body>

<script type="module" src="/006e602dbdf934d741c3/js/app.js"></script>
<script type="module" src="/006e602dbdf934d741c3/js/whats-for-lunch.js"></script>

</html>
```

</details>

### 3. Public source freshness has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 4. Restaurant of the day has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 5. An anonymous restaurant list gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2025-09-12'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2025-09-12'}
```

### 6. An anonymous import status read gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/status'}
```

### 7. An anonymous import preview is rejected (403)

```text
HTTP 403 
X-Request-Id: 8614dd54-77bc-4881-91d6-143eb79102b1
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
Date: Fri, 09 Oct 2026 20:26:14 GMT
Connection: close

{"timestamp":"2026-10-09T20:26:14.147Z","status":403,"error":"Forbidden","path":"/api/whatsforlunch/restaurant/2026-07-26/import/openstreetmap/preview"}
```

### 8. Top-liked restaurants has production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 9. Anonymous nearby picks for Austin have production's shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 10. Nearby picks with an invalid latitude gets the same status and body as production (400)

```text
exit code: 0
--- stdout ---
candidate 400 {'messages': [{'code': 'INVALID_REQUEST', 'description': 'The request is invalid.'}], 'payload': None, 'requestId': None, 'success': False}
production 400 {'messages': [{'code': 'INVALID_REQUEST', 'description': 'The request is invalid.'}], 'payload': None, 'requestId': None, 'success': False}
```

### 11. Nearby picks for a malformed ZIP gets the same status and body as production (400)

```text
exit code: 0
--- stdout ---
candidate 400 {'messages': [{'code': 'INVALID_REQUEST', 'description': 'The request is invalid.'}], 'payload': None, 'requestId': None, 'success': False}
production 400 {'messages': [{'code': 'INVALID_REQUEST', 'description': 'The request is invalid.'}], 'payload': None, 'requestId': None, 'success': False}
```

### 12. An unknown public restaurant profile gets the same status and body as production (404)

```text
exit code: 0
--- stdout ---
candidate 404 {'messages': [{'code': 'RESOURCE_NOT_FOUND', 'description': 'The requested resource was not found.'}], 'payload': None, 'requestId': None, 'success': False}
production 404 {'messages': [{'code': 'RESOURCE_NOT_FOUND', 'description': 'The requested resource was not found.'}], 'payload': None, 'requestId': None, 'success': False}
```

### 13. Create lunch_b and lunch_d through the API and log both in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
lunch_b create 201 login 200
lunch_d create 201 login 200
```

### 14. A USER's preferences, nearby picks, favorites and votes behave as before, and ADMIN routes reject the USER

```text
exit code: 0
--- stdout ---
PASS the USER saves cuisine and radius preferences (200): got 200
PASS the saved preferences read back normalized (200): got 200
PASS an unsupported radius is rejected (400): got 400
PASS nearby picks with saved preferences answer with a list (200): got 200
PASS nearby picks for a ZIP with no imported coordinate are rejected (400): got 400
PASS the USER has no favorites (200, empty): got 200
PASS favoriting a missing restaurant is rejected (404): got 404
PASS voting on a missing restaurant is rejected (404): got 404
PASS an invalid vote value is rejected (400): got 400
PASS a USER cannot list restaurants (403): got 403
PASS a USER cannot create a restaurant (403): got 403
PASS a USER cannot apply duplicate cleanup (403): got 403
```

### 15. A USER's session validation and missing-session paths behave as before

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

### 16. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T15:26:11-05:00, took 47 ms, candidate `8da0de0`
- Case 2 started 2026-10-09T15:26:11-05:00, took 233 ms, candidate `8da0de0`
- Case 3 started 2026-10-09T15:26:12-05:00, took 202 ms, candidate `8da0de0`
- Case 4 started 2026-10-09T15:26:12-05:00, took 188 ms, candidate `8da0de0`
- Case 5 started 2026-10-09T15:26:12-05:00, took 422 ms, candidate `8da0de0`
- Case 6 started 2026-10-09T15:26:13-05:00, took 436 ms, candidate `8da0de0`
- Case 7 started 2026-10-09T15:26:14-05:00, took 31 ms, candidate `8da0de0`
- Case 8 started 2026-10-09T15:26:14-05:00, took 156 ms, candidate `8da0de0`
- Case 9 started 2026-10-09T15:26:14-05:00, took 141 ms, candidate `8da0de0`
- Case 10 started 2026-10-09T15:26:14-05:00, took 468 ms, candidate `8da0de0`
- Case 11 started 2026-10-09T15:26:15-05:00, took 389 ms, candidate `8da0de0`
- Case 12 started 2026-10-09T15:26:16-05:00, took 438 ms, candidate `8da0de0`
- Case 13 started 2026-10-09T15:26:16-05:00, took 657 ms, candidate `8da0de0`
- Case 14 started 2026-10-09T15:26:17-05:00, took 312 ms, candidate `8da0de0`
- Case 15 started 2026-10-09T15:26:18-05:00, took 250 ms, candidate `8da0de0`
- Case 16 started 2026-10-09T15:26:18-05:00, took 31 ms, candidate `8da0de0`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
