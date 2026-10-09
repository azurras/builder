# Admin Java slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 15a of the style migration ([plan](../implementation-plans/2026-10-09-10-54-christopherbell-dev-admin-java-slice-conforms-to-chris-street-style.md)): admin endpoints stay protected and command-center sampling keeps working

## Branch
`claude/style-admin-20261009` at candidate `3887b55`

## Pass / Fail

> [!TIP]
> 13 of 13 cases passed on candidate `3887b55`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Readiness is UP through the database health indicator | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create admin_user_check through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Anonymous command-center snapshot matches production (403) | ✅ PASS | Expected exit code 0 |
| 4 | Anonymous command-center logs match production (403) | ✅ PASS | Expected exit code 0 |
| 5 | Anonymous admin activity matches production (403) | ✅ PASS | Expected exit code 0 |
| 6 | Anonymous admin activity query matches production (403) | ✅ PASS | Expected exit code 0 |
| 7 | A USER cannot read the command-center snapshot (403) | ✅ PASS | Expected status 403 |
| 8 | A USER cannot read command-center logs (403) | ✅ PASS | Expected status 403 |
| 9 | A USER cannot create an action challenge (403) | ✅ PASS | Expected status 403 |
| 10 | A USER cannot confirm an action (403) | ✅ PASS | Expected status 403 |
| 11 | A USER cannot cancel a pending action (403) | ✅ PASS | Expected status 403 |
| 12 | A USER cannot read admin activity (403) | ✅ PASS | Expected status 403 |
| 13 | Background metrics sampling ran without unexpected errors (the log shows only the known optional-provider warnings) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Readiness is UP through the database health indicator**: http `GET http://127.0.0.1:55521/actuator/health/readiness`
2. **Create admin_user_check through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:55521 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad admin_user_check`
3. **Anonymous command-center snapshot matches production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/command-center/2026-07-12/snapshot https://www.christopherbell.dev/api/admin/command-center/2026-07-12/snapshot 403`
4. **Anonymous command-center logs match production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/command-center/2026-07-12/logs https://www.christopherbell.dev/api/admin/command-center/2026-07-12/logs 403`
5. **Anonymous admin activity matches production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/activity/2026-05-09 https://www.christopherbell.dev/api/admin/activity/2026-05-09 403`
6. **Anonymous admin activity query matches production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/activity/2026-07-26 https://www.christopherbell.dev/api/admin/activity/2026-07-26 403`
7. **A USER cannot read the command-center snapshot (403)**: http `GET http://127.0.0.1:55521/api/admin/command-center/2026-07-12/snapshot`
8. **A USER cannot read command-center logs (403)**: http `GET http://127.0.0.1:55521/api/admin/command-center/2026-07-12/logs`
9. **A USER cannot create an action challenge (403)**: http `POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/action-challenges`
10. **A USER cannot confirm an action (403)**: http `POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/actions`
11. **A USER cannot cancel a pending action (403)**: http `POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/actions/cancel`
12. **A USER cannot read admin activity (403)**: http `GET http://127.0.0.1:55521/api/admin/activity/2026-07-26`
13. **Background metrics sampling ran without unexpected errors (the log shows only the known optional-provider warnings)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/admin_log_check.py C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-daac6cf0c6a74a0eb868a5f4d4896e06/candidate.out.log`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (command-center actions simulated by default) |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:55520 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:55521, commit 3887b558, sampled for about 20 seconds before the checks |
| Credentials | one disposable USER; password generated and never recorded; bearer token masked and token file deleted |
| Coverage limit | admin success paths need an ADMIN, which has no supported local path; they rely on the controller, action and metrics tests |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:55521/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:55521 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad admin_user_check` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/command-center/2026-07-12/snapshot https://www.christopherbell.dev/api/admin/command-center/2026-07-12/snapshot 403` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/command-center/2026-07-12/logs https://www.christopherbell.dev/api/admin/command-center/2026-07-12/logs 403` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/activity/2026-05-09 https://www.christopherbell.dev/api/admin/activity/2026-05-09 403` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/activity/2026-07-26 https://www.christopherbell.dev/api/admin/activity/2026-07-26 403` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `GET http://127.0.0.1:55521/api/admin/command-center/2026-07-12/snapshot` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `GET http://127.0.0.1:55521/api/admin/command-center/2026-07-12/logs` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/action-challenges` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/actions` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/actions/cancel` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `GET http://127.0.0.1:55521/api/admin/activity/2026-07-26` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/admin_log_check.py C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-daac6cf0c6a74a0eb868a5f4d4896e06/candidate.out.log` in `A:\Projects\christopherbell.dev-worktrees\style-admin`
- **Candidate identity:** `3887b55`
- **Cleanup:** Candidate and mongod stopped; both ports have no listeners; production mongod on 27017 untouched

## Data Sent

### 1. Readiness is UP through the database health indicator

```http
GET http://127.0.0.1:55521/actuator/health/readiness
```

### 2. Create admin_user_check through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:55521 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad admin_user_check
```

### 3. Anonymous command-center snapshot matches production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/command-center/2026-07-12/snapshot https://www.christopherbell.dev/api/admin/command-center/2026-07-12/snapshot 403
```

### 4. Anonymous command-center logs match production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/command-center/2026-07-12/logs https://www.christopherbell.dev/api/admin/command-center/2026-07-12/logs 403
```

### 5. Anonymous admin activity matches production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/activity/2026-05-09 https://www.christopherbell.dev/api/admin/activity/2026-05-09 403
```

### 6. Anonymous admin activity query matches production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:55521/api/admin/activity/2026-07-26 https://www.christopherbell.dev/api/admin/activity/2026-07-26 403
```

### 7. A USER cannot read the command-center snapshot (403)

```http
GET http://127.0.0.1:55521/api/admin/command-center/2026-07-12/snapshot
Authorization: [REDACTED]
```

### 8. A USER cannot read command-center logs (403)

```http
GET http://127.0.0.1:55521/api/admin/command-center/2026-07-12/logs
Authorization: [REDACTED]
```

### 9. A USER cannot create an action challenge (403)

```http
POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/action-challenges
Authorization: [REDACTED]
Content-Type: application/json

{"action":"RESTART_SITE"}
```

### 10. A USER cannot confirm an action (403)

```http
POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/actions
Authorization: [REDACTED]
Content-Type: application/json

{"challengeId":"x","action":"RESTART_SITE","password":"not-a-password","confirmationPhrase":"RESTART SITE"}
```

### 11. A USER cannot cancel a pending action (403)

```http
POST http://127.0.0.1:55521/api/admin/command-center/2026-07-12/actions/cancel
Authorization: [REDACTED]
```

### 12. A USER cannot read admin activity (403)

```http
GET http://127.0.0.1:55521/api/admin/activity/2026-07-26
Authorization: [REDACTED]
```

### 13. Background metrics sampling ran without unexpected errors (the log shows only the known optional-provider warnings)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/admin_log_check.py C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-daac6cf0c6a74a0eb868a5f4d4896e06/candidate.out.log
```

## Response Received

### 1. Readiness is UP through the database health indicator

```text
HTTP 200 
X-Request-Id: ba4b1a29-2449-4e45-a37c-baa9bc8821b1
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791561242
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
Date: Fri, 09 Oct 2026 15:53:02 GMT
Connection: close

{"status":"UP"}
```

### 2. Create admin_user_check through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
admin_user_check create 201 login 200
```

### 3. Anonymous command-center snapshot matches production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/command-center/2026-07-12/snapshot'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/command-center/2026-07-12/snapshot'}
```

### 4. Anonymous command-center logs match production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/command-center/2026-07-12/logs'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/command-center/2026-07-12/logs'}
```

### 5. Anonymous admin activity matches production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/activity/2026-05-09'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/activity/2026-05-09'}
```

### 6. Anonymous admin activity query matches production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/activity/2026-07-26'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/admin/activity/2026-07-26'}
```

### 7. A USER cannot read the command-center snapshot (403)

```text
HTTP 403 
X-Request-Id: e9b3668c-6b7d-4f14-87fe-a3df46d7ad40
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791561246
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
Date: Fri, 09 Oct 2026 15:53:06 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 8. A USER cannot read command-center logs (403)

```text
HTTP 403 
X-Request-Id: 21f2571e-c2dc-437c-a410-39b5e596c640
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791561246
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
Date: Fri, 09 Oct 2026 15:53:06 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 9. A USER cannot create an action challenge (403)

```text
HTTP 403 
X-Request-Id: f8b8ad0b-0bcb-4e42-b33c-ef9111f7c7cb
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791561246
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
Date: Fri, 09 Oct 2026 15:53:06 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 10. A USER cannot confirm an action (403)

```text
HTTP 403 
X-Request-Id: eed8654e-beb1-407b-bda8-1c2e4da0e7b8
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791561246
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
Date: Fri, 09 Oct 2026 15:53:06 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 11. A USER cannot cancel a pending action (403)

```text
HTTP 403 
X-Request-Id: 96de1e00-6d5e-4d41-a7eb-1379d5c155aa
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791561247
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
Date: Fri, 09 Oct 2026 15:53:07 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 12. A USER cannot read admin activity (403)

```text
HTTP 403 
X-Request-Id: 9a1021b1-e618-4cf2-93a6-a51f048f109d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791561247
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
Date: Fri, 09 Oct 2026 15:53:07 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 13. Background metrics sampling ran without unexpected errors (the log shows only the known optional-provider warnings)

```text
exit code: 0
--- stdout ---
metrics samples logged: 0
   6  ACCESS_DENIED status=403 type=AuthorizationDeniedException
   2  HV000271: Using `@Valid` on a container (java.util.List) is deprecated. You should apply t
   2  Unable to locate English counter names in registry Perflib 009. Assuming English counters.
   1  SpringDoc /v3/api-docs endpoint is enabled by default. To disable it in production, set th
   1  SpringDoc /swagger-ui.html endpoint is enabled by default. To disable it in production, se
```

## Evidence
- Case 1 started 2026-10-09T10:53:02-05:00, took 47 ms, candidate `3887b55`
- Case 2 started 2026-10-09T10:53:02-05:00, took 719 ms, candidate `3887b55`
- Case 3 started 2026-10-09T10:53:03-05:00, took 422 ms, candidate `3887b55`
- Case 4 started 2026-10-09T10:53:04-05:00, took 407 ms, candidate `3887b55`
- Case 5 started 2026-10-09T10:53:05-05:00, took 327 ms, candidate `3887b55`
- Case 6 started 2026-10-09T10:53:05-05:00, took 483 ms, candidate `3887b55`
- Case 7 started 2026-10-09T10:53:06-05:00, took 94 ms, candidate `3887b55`
- Case 8 started 2026-10-09T10:53:06-05:00, took 47 ms, candidate `3887b55`
- Case 9 started 2026-10-09T10:53:06-05:00, took 31 ms, candidate `3887b55`
- Case 10 started 2026-10-09T10:53:06-05:00, took 47 ms, candidate `3887b55`
- Case 11 started 2026-10-09T10:53:07-05:00, took 46 ms, candidate `3887b55`
- Case 12 started 2026-10-09T10:53:07-05:00, took 46 ms, candidate `3887b55`
- Case 13 started 2026-10-09T10:53:07-05:00, took 47 ms, candidate `3887b55`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
