# Account slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 14 of the style migration ([plan](../implementation-plans/2026-10-09-10-33-christopherbell-dev-account-slice-conforms-to-chris-street-style.md)): sign-up, login, sessions, password reset, profiles, follows, trust, consent and admin protection behave as before

## Branch
`claude/style-account-20261009` at candidate `963e714`

## Pass / Fail

> [!TIP]
> 21 of 21 cases passed on candidate `963e714`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Sign-up, wrong password, cookie login, /me, logout and password reset behave as before (generated password, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Create acct_a and acct_b through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 4 | acct_a reads its own account | ✅ PASS | Expected status 200 and body containing '"username":"acct_a"' |
| 5 | acct_a sees acct_b's profile, not followed and not self | ✅ PASS | Expected status 200 and body containing '"followedByMe":false,"self":false' |
| 6 | acct_a sees its own profile as self | ✅ PASS | Expected status 200 and body containing '"self":true' |
| 7 | acct_a follows acct_b | ✅ PASS | Expected status 200 and body containing '"followerCount":1,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":true,"self":false' |
| 8 | An anonymous viewer sees acct_b's follower count without viewer state | ✅ PASS | Expected status 200 and body containing '"followerCount":1,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":false,"self":false' |
| 9 | acct_a cannot follow itself (400) | ✅ PASS | Expected status 400 |
| 10 | acct_a unfollows acct_b | ✅ PASS | Expected status 200 and body containing '"followerCount":0,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":false' |
| 11 | Username search suggests acct_b and leaves out the caller | ✅ PASS | Expected status 200 and body containing '"payload":[{"username":"acct_b"},{"username":"acct_cookie"}]' |
| 12 | acct_a mutes acct_b | ✅ PASS | Expected status 200 and body containing '"targetUsername":"acct_b","type":"MUTE"' |
| 13 | acct_a clears the mute | ✅ PASS | Expected status 200 and body containing '"success":true' |
| 14 | acct_a's federation consent starts disabled | ✅ PASS | Expected status 200 and body containing '"enabled":false' |
| 15 | A USER cannot list accounts (403) | ✅ PASS | Expected status 403 |
| 16 | A USER cannot read the admin account page (403) | ✅ PASS | Expected status 403 |
| 17 | A USER cannot change Music permissions (403) | ✅ PASS | Expected status 403 |
| 18 | A USER cannot change shared-folder permissions (403) | ✅ PASS | Expected status 403 |
| 19 | A USER cannot delete an account (403) | ✅ PASS | Expected status 403 |
| 20 | Anonymous account list gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 21 | Anonymous /me gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:51687/actuator/health/readiness`
2. **Sign-up, wrong password, cookie login, /me, logout and password reset behave as before (generated password, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/account_checks.py http://127.0.0.1:51687`
3. **Create acct_a and acct_b through the API and log both in (passwords generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:51687 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad acct_a acct_b`
4. **acct_a reads its own account**: http `GET http://127.0.0.1:51687/api/accounts/2025-09-03/me`
5. **acct_a sees acct_b's profile, not followed and not self**: http `GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b`
6. **acct_a sees its own profile as self**: http `GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_a`
7. **acct_a follows acct_b**: http `POST http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b/follow`
8. **An anonymous viewer sees acct_b's follower count without viewer state**: http `GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b`
9. **acct_a cannot follow itself (400)**: http `POST http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_a/follow`
10. **acct_a unfollows acct_b**: http `DELETE http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b/follow`
11. **Username search suggests acct_b and leaves out the caller**: http `GET http://127.0.0.1:51687/api/accounts/2025-09-14/search?username=acct`
12. **acct_a mutes acct_b**: http `PUT http://127.0.0.1:51687/api/accounts/2026-06-02/trust/acct_b`
13. **acct_a clears the mute**: http `DELETE http://127.0.0.1:51687/api/accounts/2026-06-02/trust/acct_b/MUTE`
14. **acct_a's federation consent starts disabled**: http `GET http://127.0.0.1:51687/api/accounts/2026-07-28/self/federation`
15. **A USER cannot list accounts (403)**: http `GET http://127.0.0.1:51687/api/accounts/2024-12-15`
16. **A USER cannot read the admin account page (403)**: http `GET http://127.0.0.1:51687/api/accounts/2026-07-26/admin`
17. **A USER cannot change Music permissions (403)**: http `PATCH http://127.0.0.1:51687/api/accounts/2026-07-28/acct-b-id/music-permissions`
18. **A USER cannot change shared-folder permissions (403)**: http `PATCH http://127.0.0.1:51687/api/accounts/2026-07-17/acct-b-id/shared-folder-permissions`
19. **A USER cannot delete an account (403)**: http `DELETE http://127.0.0.1:51687/api/accounts/2026-07-26/acct-b-id`
20. **Anonymous account list gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:51687/api/accounts/2024-12-15 https://www.christopherbell.dev/api/accounts/2024-12-15 403`
21. **Anonymous /me gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:51687/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:51686 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:51687, commit 963e7140 |
| Credentials | four disposable USERs in the throwaway database; passwords generated per run and never recorded; bearer tokens masked; token files deleted |
| Earlier run | a first run on another fresh database was discarded: the disposable database has no unique email or username index (production applies them through the ops DomainCollectionManifest.js script), so a duplicate sign-up succeeded and the later checks cascaded; two message expectations were also wrong (the shared handler answers INVALID_TOKEN with a generic message). The duplicate sign-up case was removed and the expectations corrected; see the plan's implementation log |
| Coverage limit | admin success paths need an ADMIN, which has no supported local path; they rely on AccountServiceTest, AccountDeletionServiceTest and the Mongo contract tests |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:51687/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/account_checks.py http://127.0.0.1:51687` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:51687 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad acct_a acct_b` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2025-09-03/me` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_a` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `POST http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b/follow` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `POST http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_a/follow` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `DELETE http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b/follow` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2025-09-14/search?username=acct` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `PUT http://127.0.0.1:51687/api/accounts/2026-06-02/trust/acct_b` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `DELETE http://127.0.0.1:51687/api/accounts/2026-06-02/trust/acct_b/MUTE` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2026-07-28/self/federation` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2024-12-15` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `GET http://127.0.0.1:51687/api/accounts/2026-07-26/admin` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `PATCH http://127.0.0.1:51687/api/accounts/2026-07-28/acct-b-id/music-permissions` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `PATCH http://127.0.0.1:51687/api/accounts/2026-07-17/acct-b-id/shared-folder-permissions` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `DELETE http://127.0.0.1:51687/api/accounts/2026-07-26/acct-b-id` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:51687/api/accounts/2024-12-15 https://www.christopherbell.dev/api/accounts/2024-12-15 403` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:51687/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403` in `A:\Projects\christopherbell.dev-worktrees\style-account`
- **Candidate identity:** `963e714`
- **Cleanup:** Candidate and mongod stopped; both ports have no listeners; production mongod on 27017 untouched

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:51687/actuator/health/readiness
```

### 2. Sign-up, wrong password, cookie login, /me, logout and password reset behave as before (generated password, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/account_checks.py http://127.0.0.1:51687
```

### 3. Create acct_a and acct_b through the API and log both in (passwords generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:51687 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad acct_a acct_b
```

### 4. acct_a reads its own account

```http
GET http://127.0.0.1:51687/api/accounts/2025-09-03/me
Authorization: [REDACTED]
```

### 5. acct_a sees acct_b's profile, not followed and not self

```http
GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b
Authorization: [REDACTED]
```

### 6. acct_a sees its own profile as self

```http
GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_a
Authorization: [REDACTED]
```

### 7. acct_a follows acct_b

```http
POST http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b/follow
Authorization: [REDACTED]
```

### 8. An anonymous viewer sees acct_b's follower count without viewer state

```http
GET http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b
```

### 9. acct_a cannot follow itself (400)

```http
POST http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_a/follow
Authorization: [REDACTED]
```

### 10. acct_a unfollows acct_b

```http
DELETE http://127.0.0.1:51687/api/accounts/2025-09-14/profile/acct_b/follow
Authorization: [REDACTED]
```

### 11. Username search suggests acct_b and leaves out the caller

```http
GET http://127.0.0.1:51687/api/accounts/2025-09-14/search?username=acct
Authorization: [REDACTED]
```

### 12. acct_a mutes acct_b

```http
PUT http://127.0.0.1:51687/api/accounts/2026-06-02/trust/acct_b
Authorization: [REDACTED]
Content-Type: application/json

{"type":"MUTE"}
```

### 13. acct_a clears the mute

```http
DELETE http://127.0.0.1:51687/api/accounts/2026-06-02/trust/acct_b/MUTE
Authorization: [REDACTED]
```

### 14. acct_a's federation consent starts disabled

```http
GET http://127.0.0.1:51687/api/accounts/2026-07-28/self/federation
Authorization: [REDACTED]
```

### 15. A USER cannot list accounts (403)

```http
GET http://127.0.0.1:51687/api/accounts/2024-12-15
Authorization: [REDACTED]
```

### 16. A USER cannot read the admin account page (403)

```http
GET http://127.0.0.1:51687/api/accounts/2026-07-26/admin
Authorization: [REDACTED]
```

### 17. A USER cannot change Music permissions (403)

```http
PATCH http://127.0.0.1:51687/api/accounts/2026-07-28/acct-b-id/music-permissions
Authorization: [REDACTED]
Content-Type: application/json

{"read":true,"write":false}
```

### 18. A USER cannot change shared-folder permissions (403)

```http
PATCH http://127.0.0.1:51687/api/accounts/2026-07-17/acct-b-id/shared-folder-permissions
Authorization: [REDACTED]
Content-Type: application/json

{"read":true,"write":false}
```

### 19. A USER cannot delete an account (403)

```http
DELETE http://127.0.0.1:51687/api/accounts/2026-07-26/acct-b-id
Authorization: [REDACTED]
```

### 20. Anonymous account list gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:51687/api/accounts/2024-12-15 https://www.christopherbell.dev/api/accounts/2024-12-15 403
```

### 21. Anonymous /me gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:51687/api/accounts/2025-09-03/me https://www.christopherbell.dev/api/accounts/2025-09-03/me 403
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 85533177-ede5-4a86-afdc-a395064c89b3
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560491
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
Date: Fri, 09 Oct 2026 15:40:31 GMT
Connection: close

{"status":"UP"}
```

### 2. Sign-up, wrong password, cookie login, /me, logout and password reset behave as before (generated password, not recorded)

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

### 3. Create acct_a and acct_b through the API and log both in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
acct_a create 201 login 200
acct_b create 201 login 200
```

### 4. acct_a reads its own account

```text
HTTP 200 
X-Request-Id: f575040c-2aa5-4ebc-b19d-e4886b1cf8e4
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560492
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
Date: Fri, 09 Oct 2026 15:40:32 GMT
Connection: close

{"messages":null,"payload":{"id":"2361cea2-c99d-407e-bc08-f25e6fec5e1d","createdBy":"anonymousUser","createdOn":"2026-10-09T15:40:32.343Z","email":"acct_a@example.test","federationEnabled":false,"firstName":"Acct","lastName":"Check","lastLoginOn":"2026-10-09T15:40:32.407Z","lastModifiedBy":"anonymousUser","lastUpdatedOn":"2026-10-09T15:40:32.343Z","role":"USER","permissions":[],"status":"ACTIVE","type":"account","username":"acct_a"},"requestId":null,"success":true}
```

### 5. acct_a sees acct_b's profile, not followed and not self

```text
HTTP 200 
X-Request-Id: 45484425-3074-43f5-bce3-1c66bfc927c3
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560492
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
Date: Fri, 09 Oct 2026 15:40:32 GMT
Connection: close

{"messages":null,"payload":{"id":"d4a25f30-a7a2-4f46-945f-b5cc00c304a8","username":"acct_b","status":"ACTIVE","followerCount":0,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":false,"self":false},"requestId":null,"success":true}
```

### 6. acct_a sees its own profile as self

```text
HTTP 200 
X-Request-Id: bf03940b-4960-4c3f-8766-2c3da12167b5
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560493
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
Date: Fri, 09 Oct 2026 15:40:33 GMT
Connection: close

{"messages":null,"payload":{"id":"2361cea2-c99d-407e-bc08-f25e6fec5e1d","username":"acct_a","status":"ACTIVE","followerCount":0,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":false,"self":true},"requestId":null,"success":true}
```

### 7. acct_a follows acct_b

```text
HTTP 200 
X-Request-Id: cd83f7eb-b2e2-42a4-bd32-9a75a71bc52e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791560493
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
Date: Fri, 09 Oct 2026 15:40:33 GMT
Connection: close

{"messages":null,"payload":{"id":"d4a25f30-a7a2-4f46-945f-b5cc00c304a8","username":"acct_b","status":"ACTIVE","followerCount":1,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":true,"self":false},"requestId":null,"success":true}
```

### 8. An anonymous viewer sees acct_b's follower count without viewer state

```text
HTTP 200 
X-Request-Id: 070daf8d-8f61-44e0-a82f-980a9ac074e7
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560493
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
Date: Fri, 09 Oct 2026 15:40:33 GMT
Connection: close

{"messages":null,"payload":{"id":"d4a25f30-a7a2-4f46-945f-b5cc00c304a8","username":"acct_b","status":"ACTIVE","followerCount":1,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":false,"self":false},"requestId":null,"success":true}
```

### 9. acct_a cannot follow itself (400)

```text
HTTP 400 
X-Request-Id: 035b3114-a4f5-4cef-8df7-6d41618b1119
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791560493
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
Content-Length: 129
Date: Fri, 09 Oct 2026 15:40:33 GMT
Connection: close

{"messages":[{"code":"INVALID_REQUEST","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

### 10. acct_a unfollows acct_b

```text
HTTP 200 
X-Request-Id: b87b16a3-7a54-4381-90c2-f0a133fe589f
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791560493
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
Date: Fri, 09 Oct 2026 15:40:33 GMT
Connection: close

{"messages":null,"payload":{"id":"d4a25f30-a7a2-4f46-945f-b5cc00c304a8","username":"acct_b","status":"ACTIVE","followerCount":0,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":false,"self":false},"requestId":null,"success":true}
```

### 11. Username search suggests acct_b and leaves out the caller

```text
HTTP 200 
X-Request-Id: 914dbc3c-912b-4d13-9339-c6f8347cf9d4
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560494
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
Date: Fri, 09 Oct 2026 15:40:34 GMT
Connection: close

{"messages":null,"payload":[{"username":"acct_b"},{"username":"acct_cookie"}],"requestId":null,"success":true}
```

### 12. acct_a mutes acct_b

```text
HTTP 200 
X-Request-Id: e2690534-cf62-48c1-911f-9410acdd9b25
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791560494
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
Date: Fri, 09 Oct 2026 15:40:34 GMT
Connection: close

{"messages":null,"payload":{"ownerAccountId":"2361cea2-c99d-407e-bc08-f25e6fec5e1d","targetAccountId":"d4a25f30-a7a2-4f46-945f-b5cc00c304a8","targetUsername":"acct_b","type":"MUTE"},"requestId":null,"success":true}
```

### 13. acct_a clears the mute

```text
HTTP 200 
X-Request-Id: 9b14779e-a19c-41ca-8c30-0c83949805ea
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791560494
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
Date: Fri, 09 Oct 2026 15:40:34 GMT
Connection: close

{"messages":null,"payload":null,"requestId":null,"success":true}
```

### 14. acct_a's federation consent starts disabled

```text
HTTP 200 
X-Request-Id: b4b84c56-205c-4a53-8a1d-8a5218d2db02
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560494
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
Date: Fri, 09 Oct 2026 15:40:34 GMT
Connection: close

{"messages":null,"payload":{"enabled":false,"enrollmentAvailable":false},"requestId":null,"success":true}
```

### 15. A USER cannot list accounts (403)

```text
HTTP 403 
X-Request-Id: 93cbe611-d81b-4e80-ba82-4476015c0d57
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560494
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
Date: Fri, 09 Oct 2026 15:40:34 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 16. A USER cannot read the admin account page (403)

```text
HTTP 403 
X-Request-Id: 692df892-5f17-45b3-9bbc-7e295e647dbe
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791560495
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
Date: Fri, 09 Oct 2026 15:40:35 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 17. A USER cannot change Music permissions (403)

```text
HTTP 403 
X-Request-Id: 646a7cb0-0438-483b-9ab2-ed295a793c9b
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791560495
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
Date: Fri, 09 Oct 2026 15:40:35 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 18. A USER cannot change shared-folder permissions (403)

```text
HTTP 403 
X-Request-Id: 41109c17-bec5-407f-ab1c-84c4e9077d7c
Cache-Control: private, no-store
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791560495
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 121
Date: Fri, 09 Oct 2026 15:40:35 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 19. A USER cannot delete an account (403)

```text
HTTP 403 
X-Request-Id: 0c09fe9f-2924-4ab8-8ac7-2474ef9d69f1
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791560495
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
Date: Fri, 09 Oct 2026 15:40:35 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 20. Anonymous account list gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2024-12-15'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2024-12-15'}
```

### 21. Anonymous /me gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2025-09-03/me'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/accounts/2025-09-03/me'}
```

## Evidence
- Case 1 started 2026-10-09T10:40:31-05:00, took 61 ms, candidate `963e714`
- Case 2 started 2026-10-09T10:40:31-05:00, took 797 ms, candidate `963e714`
- Case 3 started 2026-10-09T10:40:32-05:00, took 344 ms, candidate `963e714`
- Case 4 started 2026-10-09T10:40:32-05:00, took 47 ms, candidate `963e714`
- Case 5 started 2026-10-09T10:40:32-05:00, took 77 ms, candidate `963e714`
- Case 6 started 2026-10-09T10:40:33-05:00, took 31 ms, candidate `963e714`
- Case 7 started 2026-10-09T10:40:33-05:00, took 31 ms, candidate `963e714`
- Case 8 started 2026-10-09T10:40:33-05:00, took 31 ms, candidate `963e714`
- Case 9 started 2026-10-09T10:40:33-05:00, took 47 ms, candidate `963e714`
- Case 10 started 2026-10-09T10:40:33-05:00, took 45 ms, candidate `963e714`
- Case 11 started 2026-10-09T10:40:34-05:00, took 47 ms, candidate `963e714`
- Case 12 started 2026-10-09T10:40:34-05:00, took 46 ms, candidate `963e714`
- Case 13 started 2026-10-09T10:40:34-05:00, took 31 ms, candidate `963e714`
- Case 14 started 2026-10-09T10:40:34-05:00, took 31 ms, candidate `963e714`
- Case 15 started 2026-10-09T10:40:34-05:00, took 31 ms, candidate `963e714`
- Case 16 started 2026-10-09T10:40:35-05:00, took 32 ms, candidate `963e714`
- Case 17 started 2026-10-09T10:40:35-05:00, took 47 ms, candidate `963e714`
- Case 18 started 2026-10-09T10:40:35-05:00, took 30 ms, candidate `963e714`
- Case 19 started 2026-10-09T10:40:35-05:00, took 31 ms, candidate `963e714`
- Case 20 started 2026-10-09T10:40:35-05:00, took 358 ms, candidate `963e714`
- Case 21 started 2026-10-09T10:40:36-05:00, took 391 ms, candidate `963e714`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
