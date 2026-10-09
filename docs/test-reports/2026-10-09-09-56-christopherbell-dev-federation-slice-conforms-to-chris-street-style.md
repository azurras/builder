# Federation slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 11 of the style migration ([plan](../implementation-plans/2026-10-09-09-45-christopherbell-dev-federation-slice-conforms-to-chris-street-style.md)): ActivityPub discovery, the outbox and relationship collections, and consent behave as before, with responses shaped like production's

## Branch
`claude/style-federation-20261006` at candidate `95d5b5f`

## Pass / Fail

> [!TIP]
> 25 of 25 cases passed on candidate `95d5b5f`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test with discovery enabled | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create fed_alice and fed_bob through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | NodeInfo discovery links the 2.1 schema | ✅ PASS | Expected status 200 and body containing 'nodeinfo/2.1' |
| 4 | NodeInfo 2.1 has the same shape as production | ✅ PASS | Expected exit code 0 |
| 5 | fed_alice is not discoverable before consenting (404) | ✅ PASS | Expected status 404 |
| 6 | fed_alice turns federation on | ✅ PASS | Expected status 200 and body containing '"federationEnabled":true' |
| 7 | fed_bob turns federation on | ✅ PASS | Expected status 200 and body containing '"federationEnabled":true' |
| 8 | WebFinger resolves fed_alice to her actor | ✅ PASS | Expected status 200 and body containing '/ap/users/fed_alice' |
| 9 | WebFinger has the same shape as production | ✅ PASS | Expected exit code 0 |
| 10 | fed_alice's actor is served as activity JSON | ✅ PASS | Expected status 200 and body containing '"type":"Person"' |
| 11 | Actor has the same shape as production | ✅ PASS | Expected exit code 0 |
| 12 | Outbox summary is an OrderedCollection linking its first page | ✅ PASS | Expected status 200 and body containing '"type":"OrderedCollection"' |
| 13 | Outbox summary has the same shape as production | ✅ PASS | Expected exit code 0 |
| 14 | Outbox page is an OrderedCollectionPage | ✅ PASS | Expected status 200 and body containing '"type":"OrderedCollectionPage"' |
| 15 | Outbox page has the same shape as production | ✅ PASS | Expected exit code 0 |
| 16 | An invalid outbox cursor is rejected (400) | ✅ PASS | Expected status 400 |
| 17 | fed_bob follows fed_alice | ✅ PASS | Expected status 200 |
| 18 | fed_alice's followers list fed_bob's actor | ✅ PASS | Expected status 200 and body containing '/ap/users/fed_bob"' |
| 19 | fed_bob's following lists fed_alice's actor | ✅ PASS | Expected status 200 and body containing '/ap/users/fed_alice"' |
| 20 | Followers have the same shape as production | ✅ PASS | Expected exit code 0 |
| 21 | Following has the same shape as production | ✅ PASS | Expected exit code 0 |
| 22 | An unknown actor returns 404 | ✅ PASS | Expected status 404 |
| 23 | fed_alice turns federation off | ✅ PASS | Expected status 200 and body containing '"federationEnabled":false' |
| 24 | fed_alice's actor returns 404 after she withdraws | ✅ PASS | Expected status 404 |
| 25 | fed_alice's outbox returns 404 after she withdraws | ✅ PASS | Expected status 404 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test with discovery enabled**: http `GET http://127.0.0.1:61117/actuator/health/readiness`
2. **Create fed_alice and fed_bob through the API and log both in (passwords generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:61117 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad fed_alice fed_bob`
3. **NodeInfo discovery links the 2.1 schema**: http `GET http://127.0.0.1:61117/.well-known/nodeinfo`
4. **NodeInfo 2.1 has the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/nodeinfo/2.1 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/2.json application/json`
5. **fed_alice is not discoverable before consenting (404)**: http `GET http://127.0.0.1:61117/ap/users/fed_alice`
6. **fed_alice turns federation on**: http `PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation`
7. **fed_bob turns federation on**: http `PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation`
8. **WebFinger resolves fed_alice to her actor**: http `GET http://127.0.0.1:61117/.well-known/webfinger?resource=acct:fed_alice@localhost:8081`
9. **WebFinger has the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/.well-known/webfinger?resource=acct:fed_alice@localhost:8081 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/3.json application/jrd+json`
10. **fed_alice's actor is served as activity JSON**: http `GET http://127.0.0.1:61117/ap/users/fed_alice`
11. **Actor has the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/4.json`
12. **Outbox summary is an OrderedCollection linking its first page**: http `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox`
13. **Outbox summary has the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/outbox C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/5.json`
14. **Outbox page is an OrderedCollectionPage**: http `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true`
15. **Outbox page has the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/6.json`
16. **An invalid outbox cursor is rejected (400)**: http `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true&cursor=not-a-cursor`
17. **fed_bob follows fed_alice**: http `POST http://127.0.0.1:61117/api/accounts/2025-09-14/profile/fed_alice/follow`
18. **fed_alice's followers list fed_bob's actor**: http `GET http://127.0.0.1:61117/ap/users/fed_alice/followers`
19. **fed_bob's following lists fed_alice's actor**: http `GET http://127.0.0.1:61117/ap/users/fed_bob/following`
20. **Followers have the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/followers C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/7.json`
21. **Following has the same shape as production**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_bob/following C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/8.json`
22. **An unknown actor returns 404**: http `GET http://127.0.0.1:61117/ap/users/nobody_here`
23. **fed_alice turns federation off**: http `PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation`
24. **fed_alice's actor returns 404 after she withdraws**: http `GET http://127.0.0.1:61117/ap/users/fed_alice`
25. **fed_alice's outbox returns 404 after she withdraws**: http `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test, with app.federation discovery enabled and a random key-encryption secret for this run only |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:61116 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:61117, commit 95d5b5f4 |
| Credentials | two disposable USERs in the throwaway database; passwords generated and never recorded; bearer tokens masked and token files deleted |
| Production baseline | read-only GETs of www.christopherbell.dev federation routes on 2026-10-09 |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:61117/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:61117 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad fed_alice fed_bob` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/.well-known/nodeinfo` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/nodeinfo/2.1 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/2.json application/json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/.well-known/webfinger?resource=acct:fed_alice@localhost:8081` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/.well-known/webfinger?resource=acct:fed_alice@localhost:8081 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/3.json application/jrd+json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/4.json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/outbox C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/5.json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/6.json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true&cursor=not-a-cursor` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `POST http://127.0.0.1:61117/api/accounts/2025-09-14/profile/fed_alice/follow` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice/followers` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_bob/following` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/followers C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/7.json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_bob/following C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/8.json` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/nobody_here` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Local command:** `GET http://127.0.0.1:61117/ap/users/fed_alice/outbox` in `A:\Projects\christopherbell.dev-worktrees\style-federation`
- **Candidate identity:** `95d5b5f`
- **Cleanup:** Candidate and mongod stopped; both ports have no listeners; production mongod on 27017 untouched

## Data Sent

### 1. Candidate readiness on isolated MongoDB test with discovery enabled

```http
GET http://127.0.0.1:61117/actuator/health/readiness
```

### 2. Create fed_alice and fed_bob through the API and log both in (passwords generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:61117 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad fed_alice fed_bob
```

### 3. NodeInfo discovery links the 2.1 schema

```http
GET http://127.0.0.1:61117/.well-known/nodeinfo
```

### 4. NodeInfo 2.1 has the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/nodeinfo/2.1 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/2.json application/json
```

### 5. fed_alice is not discoverable before consenting (404)

```http
GET http://127.0.0.1:61117/ap/users/fed_alice
Accept: application/activity+json
```

### 6. fed_alice turns federation on

```http
PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation
Authorization: [REDACTED]
Content-Type: application/json

{"enabled":true}
```

### 7. fed_bob turns federation on

```http
PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation
Authorization: [REDACTED]
Content-Type: application/json

{"enabled":true}
```

### 8. WebFinger resolves fed_alice to her actor

```http
GET http://127.0.0.1:61117/.well-known/webfinger?resource=acct:fed_alice@localhost:8081
```

### 9. WebFinger has the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/.well-known/webfinger?resource=acct:fed_alice@localhost:8081 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/3.json application/jrd+json
```

### 10. fed_alice's actor is served as activity JSON

```http
GET http://127.0.0.1:61117/ap/users/fed_alice
Accept: application/activity+json
```

### 11. Actor has the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/4.json
```

### 12. Outbox summary is an OrderedCollection linking its first page

```http
GET http://127.0.0.1:61117/ap/users/fed_alice/outbox
Accept: application/activity+json
```

### 13. Outbox summary has the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/outbox C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/5.json
```

### 14. Outbox page is an OrderedCollectionPage

```http
GET http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true
Accept: application/activity+json
```

### 15. Outbox page has the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/6.json
```

### 16. An invalid outbox cursor is rejected (400)

```http
GET http://127.0.0.1:61117/ap/users/fed_alice/outbox?page=true&cursor=not-a-cursor
Accept: application/activity+json
```

### 17. fed_bob follows fed_alice

```http
POST http://127.0.0.1:61117/api/accounts/2025-09-14/profile/fed_alice/follow
Authorization: [REDACTED]
```

### 18. fed_alice's followers list fed_bob's actor

```http
GET http://127.0.0.1:61117/ap/users/fed_alice/followers
Accept: application/activity+json
```

### 19. fed_bob's following lists fed_alice's actor

```http
GET http://127.0.0.1:61117/ap/users/fed_bob/following
Accept: application/activity+json
```

### 20. Followers have the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_alice/followers C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/7.json
```

### 21. Following has the same shape as production

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_json_shape.py http://127.0.0.1:61117/ap/users/fed_bob/following C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/fed-before/8.json
```

### 22. An unknown actor returns 404

```http
GET http://127.0.0.1:61117/ap/users/nobody_here
Accept: application/activity+json
```

### 23. fed_alice turns federation off

```http
PATCH http://127.0.0.1:61117/api/accounts/2026-07-28/self/federation
Authorization: [REDACTED]
Content-Type: application/json

{"enabled":false}
```

### 24. fed_alice's actor returns 404 after she withdraws

```http
GET http://127.0.0.1:61117/ap/users/fed_alice
Accept: application/activity+json
```

### 25. fed_alice's outbox returns 404 after she withdraws

```http
GET http://127.0.0.1:61117/ap/users/fed_alice/outbox
Accept: application/activity+json
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test with discovery enabled

```text
HTTP 200 
X-Request-Id: e2a28f0b-7a4a-4936-b364-763ec0fc47c4
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557822
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
Date: Fri, 09 Oct 2026 14:56:02 GMT
Connection: close

{"status":"UP"}
```

### 2. Create fed_alice and fed_bob through the API and log both in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
fed_alice create 201 login 200
fed_bob create 201 login 200
```

### 3. NodeInfo discovery links the 2.1 schema

```text
HTTP 200 
X-Request-Id: f43a9723-5db6-4227-8f9d-17f761e67e45
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557823
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:03 GMT
Connection: close

{"links":[{"rel":"http://nodeinfo.diaspora.software/ns/schema/2.1","href":"http://localhost:8081/nodeinfo/2.1"}]}
```

### 4. NodeInfo 2.1 has the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 5. fed_alice is not discoverable before consenting (404)

```text
HTTP 404 
X-Request-Id: d97e0432-e117-4de6-ad67-b515c39f6166
Cache-Control: public, no-store
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557823
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Content-Length: 146
Date: Fri, 09 Oct 2026 14:56:03 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 6. fed_alice turns federation on

```text
HTTP 200 
X-Request-Id: 54262c57-ffa9-4209-9b56-2d57961f907a
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791557823
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
Date: Fri, 09 Oct 2026 14:56:04 GMT
Connection: close

{"messages":null,"payload":{"id":"f2314b13-92f1-495f-a043-08438fcc127d","createdBy":"anonymousUser","createdOn":"2026-10-09T14:56:02.782Z","email":"fed_alice@example.test","federationEnabled":true,"firstName":"Fed","lastName":"Check","lastLoginOn":"2026-10-09T14:56:02.873Z","lastModifiedBy":"f2314b13-92f1-495f-a043-08438fcc127d","lastUpdatedOn":"2026-10-09T14:56:04.174Z","role":"USER","permissions":[],"status":"ACTIVE","type":"account","username":"fed_alice"},"requestId":null,"success":true}
```

### 7. fed_bob turns federation on

```text
HTTP 200 
X-Request-Id: 27291eb7-97c0-4372-bb0a-9ca6ec108599
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791557824
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
Date: Fri, 09 Oct 2026 14:56:04 GMT
Connection: close

{"messages":null,"payload":{"id":"e32a102b-d48c-41a3-8f95-b05021e32ffd","createdBy":"anonymousUser","createdOn":"2026-10-09T14:56:02.999Z","email":"fed_bob@example.test","federationEnabled":true,"firstName":"Fed","lastName":"Check","lastLoginOn":"2026-10-09T14:56:03.048Z","lastModifiedBy":"e32a102b-d48c-41a3-8f95-b05021e32ffd","lastUpdatedOn":"2026-10-09T14:56:04.476Z","role":"USER","permissions":[],"status":"ACTIVE","type":"account","username":"fed_bob"},"requestId":null,"success":true}
```

### 8. WebFinger resolves fed_alice to her actor

```text
HTTP 200 
X-Request-Id: 695b516c-8036-46b2-a138-4e2558419741
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557824
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/jrd+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:04 GMT
Connection: close

{"subject":"acct:fed_alice@localhost:8081","aliases":["http://localhost:8081/ap/users/fed_alice"],"links":[{"rel":"self","type":"application/activity+json","href":"http://localhost:8081/ap/users/fed_alice"}]}
```

### 9. WebFinger has the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 10. fed_alice's actor is served as activity JSON

```text
HTTP 200 
X-Request-Id: d3985819-bf81-45a9-906c-2da619995a8a
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557825
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:05 GMT
Connection: close

{"@context":["https://www.w3.org/ns/activitystreams","https://w3id.org/security/v1"],"id":"http://localhost:8081/ap/users/fed_alice","type":"Person","preferredUsername":"fed_alice","name":"fed_alice","inbox":"http://localhost:8081/ap/users/fed_alice/inbox","outbox":"http://localhost:8081/ap/users/fed_alice/outbox","followers":"http://localhost:8081/ap/users/fed_alice/followers","following":"http://localhost:8081/ap/users/fed_alice/following","url":"http://localhost:8081/u/fed_alice","publicKey":{"id":"http://localhost:8081/ap/users/fed_alice#main-key","owner":"http://localhost:8081/ap/users/fed_alice","publicKeyPem":"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8zALa4I+htUJ6WcmPDCd\nlRGBbAtz6VXNU1rpe/PshlP7AOfPVrpx5fbU04AS62CMgQM7k9rE13iUen4+d+zx\nohM3L3JcPXfgremIt1a9A8Umowahoc81ALvN+W35Hq4xVh2hTSiHULawCYO+MMmB\nzjv7XcXNAuzI2y7NyLHBRq8mhNTMnmpMRk66cPwaDuHDpYmvUR6vQBAgvsYcJ3o2\nTci4c3vcJ4fu6PpnUvHxzg6fj/3K+pr1tbl9awwBZvbr7NLkoV40PqELqMRr1J4b\n9TyzPkScEU8fzqwOPfx0lObfNtov2xISBb0NFCdh7P6YUSoPxOrOY8ZmktWZKfzI\nUwIDAQAB\n-----END PUBLIC KEY-----"}}
```

### 11. Actor has the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 12. Outbox summary is an OrderedCollection linking its first page

```text
HTTP 200 
X-Request-Id: 520402cf-94ec-4c91-b3a6-90fa6abe7c19
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557825
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:05 GMT
Connection: close

{"@context":["https://www.w3.org/ns/activitystreams"],"id":"http://localhost:8081/ap/users/fed_alice/outbox","type":"OrderedCollection","totalItems":0,"first":"http://localhost:8081/ap/users/fed_alice/outbox?page=true"}
```

### 13. Outbox summary has the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 14. Outbox page is an OrderedCollectionPage

```text
HTTP 200 
X-Request-Id: c32e4458-1117-4f8b-bf7a-a0bb9257c3bc
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557826
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:06 GMT
Connection: close

{"@context":["https://www.w3.org/ns/activitystreams"],"id":"http://localhost:8081/ap/users/fed_alice/outbox?page=true","type":"OrderedCollectionPage","totalItems":0,"partOf":"http://localhost:8081/ap/users/fed_alice/outbox","orderedItems":[]}
```

### 15. Outbox page has the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 16. An invalid outbox cursor is rejected (400)

```text
HTTP 400 
X-Request-Id: 532bdc01-cdca-4c1e-8a79-ff6ca5359c08
Cache-Control: public, no-store
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557826
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Content-Length: 129
Date: Fri, 09 Oct 2026 14:56:06 GMT
Connection: close

{"messages":[{"code":"INVALID_REQUEST","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

### 17. fed_bob follows fed_alice

```text
HTTP 200 
X-Request-Id: b2edcf56-b403-4a70-a3aa-d1281eb87d71
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791557826
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
Date: Fri, 09 Oct 2026 14:56:06 GMT
Connection: close

{"messages":null,"payload":{"id":"f2314b13-92f1-495f-a043-08438fcc127d","username":"fed_alice","status":"ACTIVE","followerCount":1,"followingCount":0,"postCount":0,"replyCount":0,"followedByMe":true,"self":false},"requestId":null,"success":true}
```

### 18. fed_alice's followers list fed_bob's actor

```text
HTTP 200 
X-Request-Id: 3245c019-2511-44f0-9a02-7439934ffc62
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557827
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:07 GMT
Connection: close

{"@context":["https://www.w3.org/ns/activitystreams"],"id":"http://localhost:8081/ap/users/fed_alice/followers","type":"OrderedCollection","totalItems":1,"orderedItems":["http://localhost:8081/ap/users/fed_bob"]}
```

### 19. fed_bob's following lists fed_alice's actor

```text
HTTP 200 
X-Request-Id: e982e702-b77f-494d-8711-69bb95e4b21a
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557827
Cache-Control: no-store
Access-Control-Allow-Origin: *
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 14:56:07 GMT
Connection: close

{"@context":["https://www.w3.org/ns/activitystreams"],"id":"http://localhost:8081/ap/users/fed_bob/following","type":"OrderedCollection","totalItems":1,"orderedItems":["http://localhost:8081/ap/users/fed_alice"]}
```

### 20. Followers have the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 21. Following has the same shape as production

```text
exit code: 0
--- stdout ---
shape matches production
```

### 22. An unknown actor returns 404

```text
HTTP 404 
X-Request-Id: c90beb54-d7d9-4db9-abde-66e785871d55
Cache-Control: public, no-store
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557827
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Content-Length: 146
Date: Fri, 09 Oct 2026 14:56:07 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 23. fed_alice turns federation off

```text
HTTP 200 
X-Request-Id: ad141904-042b-40b6-802f-8885bc8a21fd
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791557828
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
Date: Fri, 09 Oct 2026 14:56:08 GMT
Connection: close

{"messages":null,"payload":{"id":"f2314b13-92f1-495f-a043-08438fcc127d","createdBy":"anonymousUser","createdOn":"2026-10-09T14:56:02.782Z","email":"fed_alice@example.test","federationEnabled":false,"firstName":"Fed","lastName":"Check","lastLoginOn":"2026-10-09T14:56:02.873Z","lastModifiedBy":"f2314b13-92f1-495f-a043-08438fcc127d","lastUpdatedOn":"2026-10-09T14:56:08.178Z","role":"USER","permissions":[],"status":"ACTIVE","type":"account","username":"fed_alice"},"requestId":null,"success":true}
```

### 24. fed_alice's actor returns 404 after she withdraws

```text
HTTP 404 
X-Request-Id: b7765edd-bd82-43e7-81a0-ae1739830f0d
Cache-Control: public, no-store
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557828
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Content-Length: 146
Date: Fri, 09 Oct 2026 14:56:08 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 25. fed_alice's outbox returns 404 after she withdraws

```text
HTTP 404 
X-Request-Id: 053d3116-06d2-48b8-9017-dd9913588260
Cache-Control: public, no-store
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791557828
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/activity+json
Content-Length: 146
Date: Fri, 09 Oct 2026 14:56:08 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

## Evidence
- Case 1 started 2026-10-09T09:56:02-05:00, took 46 ms, candidate `95d5b5f`
- Case 2 started 2026-10-09T09:56:02-05:00, took 717 ms, candidate `95d5b5f`
- Case 3 started 2026-10-09T09:56:03-05:00, took 30 ms, candidate `95d5b5f`
- Case 4 started 2026-10-09T09:56:03-05:00, took 125 ms, candidate `95d5b5f`
- Case 5 started 2026-10-09T09:56:03-05:00, took 47 ms, candidate `95d5b5f`
- Case 6 started 2026-10-09T09:56:03-05:00, took 217 ms, candidate `95d5b5f`
- Case 7 started 2026-10-09T09:56:04-05:00, took 140 ms, candidate `95d5b5f`
- Case 8 started 2026-10-09T09:56:04-05:00, took 61 ms, candidate `95d5b5f`
- Case 9 started 2026-10-09T09:56:04-05:00, took 125 ms, candidate `95d5b5f`
- Case 10 started 2026-10-09T09:56:05-05:00, took 31 ms, candidate `95d5b5f`
- Case 11 started 2026-10-09T09:56:05-05:00, took 108 ms, candidate `95d5b5f`
- Case 12 started 2026-10-09T09:56:05-05:00, took 32 ms, candidate `95d5b5f`
- Case 13 started 2026-10-09T09:56:05-05:00, took 125 ms, candidate `95d5b5f`
- Case 14 started 2026-10-09T09:56:06-05:00, took 47 ms, candidate `95d5b5f`
- Case 15 started 2026-10-09T09:56:06-05:00, took 125 ms, candidate `95d5b5f`
- Case 16 started 2026-10-09T09:56:06-05:00, took 31 ms, candidate `95d5b5f`
- Case 17 started 2026-10-09T09:56:06-05:00, took 45 ms, candidate `95d5b5f`
- Case 18 started 2026-10-09T09:56:06-05:00, took 47 ms, candidate `95d5b5f`
- Case 19 started 2026-10-09T09:56:07-05:00, took 32 ms, candidate `95d5b5f`
- Case 20 started 2026-10-09T09:56:07-05:00, took 125 ms, candidate `95d5b5f`
- Case 21 started 2026-10-09T09:56:07-05:00, took 125 ms, candidate `95d5b5f`
- Case 22 started 2026-10-09T09:56:07-05:00, took 31 ms, candidate `95d5b5f`
- Case 23 started 2026-10-09T09:56:08-05:00, took 45 ms, candidate `95d5b5f`
- Case 24 started 2026-10-09T09:56:08-05:00, took 31 ms, candidate `95d5b5f`
- Case 25 started 2026-10-09T09:56:08-05:00, took 30 ms, candidate `95d5b5f`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
