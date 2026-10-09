# Mongo domain persistence conforms to Chris Street Style: Test Report

## Story/Issue
Slice 18g of the style migration ([plan](../implementation-plans/2026-10-09-16-22-christopherbell-dev-mongo-domain-persistence-conforms-to-chris-street-style.md)): kind-scoped reads, writes, aggregations and leases behave as before

## Branch
``claude/style-mongo-domain-20261009` at candidate `5b4e778d`` at candidate `5b4e778`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `5b4e778`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (domain preflight validated the collection manifest) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create post_a, post_b, lunch_b and lunch_d through the API and log in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and cascading deletion round-trip through the kind-scoped operations | ✅ PASS | Expected exit code 0 |
| 4 | Lunch preferences, favorites and session paths round-trip through the kind-scoped operations | ✅ PASS | Expected exit code 0 |
| 5 | Lunch preferences, votes and ADMIN rejections behave as before | ✅ PASS | Expected exit code 0 |
| 6 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (domain preflight validated the collection manifest)**: http `GET http://127.0.0.1:49691/actuator/health/readiness`
2. **Create post_a, post_b, lunch_b and lunch_d through the API and log in (passwords generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_a post_b lunch_b lunch_d`
3. **Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and cascading deletion round-trip through the kind-scoped operations**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
4. **Lunch preferences, favorites and session paths round-trip through the kind-scoped operations**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
5. **Lunch preferences, votes and ADMIN rejections behave as before**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_service_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
6. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-cee6f8fbac114d83bc37b61166786de1/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:49691, commit 5b4e778d |
| Credentials | four disposable USERs; passwords generated and never recorded; bearer tokens masked; token files deleted |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:49691/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-domain`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_a post_b lunch_b lunch_d` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-domain`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-domain`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-domain`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_service_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-domain`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-cee6f8fbac114d83bc37b61166786de1/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-domain`
- **Candidate identity:** `5b4e778`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token files deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (domain preflight validated the collection manifest)

```http
GET http://127.0.0.1:49691/actuator/health/readiness
```

### 2. Create post_a, post_b, lunch_b and lunch_d through the API and log in (passwords generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_a post_b lunch_b lunch_d
```

### 3. Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and cascading deletion round-trip through the kind-scoped operations

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 4. Lunch preferences, favorites and session paths round-trip through the kind-scoped operations

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_sessions_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 5. Lunch preferences, votes and ADMIN rejections behave as before

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/lunch_service_checks.py http://127.0.0.1:49691 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 6. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-cee6f8fbac114d83bc37b61166786de1/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (domain preflight validated the collection manifest)

```text
HTTP 200 
X-Request-Id: 76dd3815-bab4-454b-b958-2d76d191a020
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791581366
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
Date: Fri, 09 Oct 2026 21:28:26 GMT
Connection: close

{"status":"UP"}
```

### 2. Create post_a, post_b, lunch_b and lunch_d through the API and log in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
post_a create 201 login 200
post_b create 201 login 200
lunch_b create 201 login 200
lunch_d create 201 login 200
```

### 3. Posts, replies, likes, edits, threads, feeds, follows, discovery, hiding and cascading deletion round-trip through the kind-scoped operations

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

### 4. Lunch preferences, favorites and session paths round-trip through the kind-scoped operations

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

### 5. Lunch preferences, votes and ADMIN rejections behave as before

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

### 6. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T16:28:26-05:00, took 63 ms, candidate `5b4e778`
- Case 2 started 2026-10-09T16:28:26-05:00, took 968 ms, candidate `5b4e778`
- Case 3 started 2026-10-09T16:28:27-05:00, took 702 ms, candidate `5b4e778`
- Case 4 started 2026-10-09T16:28:28-05:00, took 250 ms, candidate `5b4e778`
- Case 5 started 2026-10-09T16:28:29-05:00, took 250 ms, candidate `5b4e778`
- Case 6 started 2026-10-09T16:28:29-05:00, took 47 ms, candidate `5b4e778`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
