# Post Java slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 16a of the style migration ([plan](../implementation-plans/2026-10-09-11-20-christopherbell-dev-post-java-slice-conforms-to-chris-street-style.md)): posting, replies, likes, edits, threads, feeds, discovery, hiding and deletion behave as before

## Branch
``claude/style-post-20261009` at candidate `58ded013`` at candidate `58ded01`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `58ded01`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create post_a and post_b through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and deletion behave as before | ✅ PASS | Expected exit code 0 |
| 4 | Anonymous discovery people answers like production (200, list payload) | ✅ PASS | Expected exit code 0 |
| 5 | Anonymous discovery new arrivals has production's page shape | ✅ PASS | Expected exit code 0 |
| 6 | Anonymous global feed page has production's page shape | ✅ PASS | Expected exit code 0 |
| 7 | Anonymous own-feed read gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 8 | An anonymous post creation is rejected (403) | ✅ PASS | Expected status 403 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:50540/actuator/health/readiness`
2. **Create post_a and post_b through the API and log both in (passwords generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:50540 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_a post_b`
3. **Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and deletion behave as before**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_checks.py http://127.0.0.1:50540 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
4. **Anonymous discovery people answers like production (200, list payload)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-28/discovery/people C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-people.json application/json`
5. **Anonymous discovery new arrivals has production's page shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-28/discovery/new?size=12 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-new.json application/json`
6. **Anonymous global feed page has production's page shape**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-26/feed?size=5 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-feed.json application/json`
7. **Anonymous own-feed read gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:50540/api/posts/2026-07-26/me/feed https://www.christopherbell.dev/api/posts/2026-07-26/me/feed 403`
8. **An anonymous post creation is rejected (403)**: http `POST http://127.0.0.1:50540/api/posts/2025-09-14/create`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod at 127.0.0.1:50539 |
| Candidate | packaged website.jar at 127.0.0.1:50540, commit 58ded013 |
| Credentials | two disposable USERs in the throwaway database; passwords generated per run and never recorded; bearer tokens masked; token files deleted |
| Production | read-only GETs only (discovery people, discovery new arrivals, global feed page, anonymous own feed) |
| Coverage limit | the admin-only account post history route needs an ADMIN, which has no supported local path; PostControllerTest covers it |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:50540/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:50540 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_a post_b` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_checks.py http://127.0.0.1:50540 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-28/discovery/people C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-people.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-28/discovery/new?size=12 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-new.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-26/feed?size=5 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-feed.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:50540/api/posts/2026-07-26/me/feed https://www.christopherbell.dev/api/posts/2026-07-26/me/feed 403` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Local command:** `POST http://127.0.0.1:50540/api/posts/2025-09-14/create` in `A:\Projects\christopherbell.dev-worktrees\style-post`
- **Candidate identity:** `58ded01`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token files deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:50540/actuator/health/readiness
```

### 2. Create post_a and post_b through the API and log both in (passwords generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:50540 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_a post_b
```

### 3. Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and deletion behave as before

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_checks.py http://127.0.0.1:50540 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 4. Anonymous discovery people answers like production (200, list payload)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-28/discovery/people C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-people.json application/json
```

### 5. Anonymous discovery new arrivals has production's page shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-28/discovery/new?size=12 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-new.json application/json
```

### 6. Anonymous global feed page has production's page shape

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:50540/api/posts/2026-07-26/feed?size=5 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-prod-feed.json application/json
```

### 7. Anonymous own-feed read gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:50540/api/posts/2026-07-26/me/feed https://www.christopherbell.dev/api/posts/2026-07-26/me/feed 403
```

### 8. An anonymous post creation is rejected (403)

```http
POST http://127.0.0.1:50540/api/posts/2025-09-14/create
Content-Type: application/json

{"text":"anonymous"}
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: d694a893-d258-47b4-a26e-b62ebd125710
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791563076
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
Date: Fri, 09 Oct 2026 16:23:36 GMT
Connection: close

{"status":"UP"}
```

### 2. Create post_a and post_b through the API and log both in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
post_a create 201 login 200
post_b create 201 login 200
```

### 3. Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and deletion behave as before

```text
exit code: 0
--- stdout ---
PASS post_a creates a root post with its topic (201)
PASS post_b replies to the root (201)
PASS post_b likes the root idempotently (200, liked, count 1)
PASS a repeated like keeps the count at 1
PASS post_b removes the like (200, count 0)
PASS the legacy toggle likes the root again (200)
PASS post_a edits the root (200, editedOn set)
PASS post_b cannot edit post_a's root (404)
PASS the anonymous thread read returns root then reply
PASS the anonymous single-post read returns the edited text
PASS the anonymous global feed page lists both posts
PASS the legacy global feed lists the root
PASS post_a's public user feed page lists the root
PASS post_a's own feed page lists the root
PASS post_a's post history page lists the root
PASS post_b follows post_a (200)
PASS post_b's following feed page lists post_a's root
PASS discovery new arrivals lists the root
PASS discovery for #styletest lists the root
PASS discovery topics include styletest
PASS anonymous people suggestions answer (200)
PASS signed-in people suggestions leave out followed accounts (200)
PASS post_b hides the thread (200)
PASS the hidden thread leaves post_b's global feed
PASS post_b unhides the thread (200)
PASS post_b cannot delete post_a's root (400)
PASS post_a deletes the root (200)
PASS the reply was deleted with its root (404)
```

### 4. Anonymous discovery people answers like production (200, list payload)

```text
exit code: 0
--- stdout ---
shape matches production
```

### 5. Anonymous discovery new arrivals has production's page shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 6. Anonymous global feed page has production's page shape

```text
exit code: 0
--- stdout ---
shape matches production
```

### 7. Anonymous own-feed read gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/posts/2026-07-26/me/feed'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/posts/2026-07-26/me/feed'}
```

### 8. An anonymous post creation is rejected (403)

```text
HTTP 403 
X-Request-Id: 29394151-156a-4de5-a0cb-9f21e5cec85d
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
Date: Fri, 09 Oct 2026 16:23:40 GMT
Connection: close

{"timestamp":"2026-10-09T16:23:40.453Z","status":403,"error":"Forbidden","path":"/api/posts/2025-09-14/create"}
```

## Evidence
- Case 1 started 2026-10-09T11:23:36-05:00, took 31 ms, candidate `58ded01`
- Case 2 started 2026-10-09T11:23:37-05:00, took 734 ms, candidate `58ded01`
- Case 3 started 2026-10-09T11:23:37-05:00, took 796 ms, candidate `58ded01`
- Case 4 started 2026-10-09T11:23:38-05:00, took 125 ms, candidate `58ded01`
- Case 5 started 2026-10-09T11:23:39-05:00, took 108 ms, candidate `58ded01`
- Case 6 started 2026-10-09T11:23:39-05:00, took 109 ms, candidate `58ded01`
- Case 7 started 2026-10-09T11:23:39-05:00, took 579 ms, candidate `58ded01`
- Case 8 started 2026-10-09T11:23:40-05:00, took 30 ms, candidate `58ded01`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
