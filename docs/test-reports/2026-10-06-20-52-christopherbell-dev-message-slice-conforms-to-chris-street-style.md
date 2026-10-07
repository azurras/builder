# Message slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 7 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-20-47-christopherbell-dev-message-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-message-20261006` at candidate `4c2175f`

## Pass / Fail

> [!TIP]
> 16 of 16 cases passed on candidate `4c2175f`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Alice sends Bob a message (201, mine=true for the sender) | ✅ PASS | Expected status 201 and body containing '"mine":true' |
| 4 | Alice sends a second message | ✅ PASS | Expected status 201 and body containing '"text":"Second hello"' |
| 5 | Bob's conversation list shows alice_msg with two unread | ✅ PASS | Expected status 200 and body containing '"unreadCount":2' |
| 6 | Paged open with size 1 returns the newest message and a cursor | ✅ PASS | Expected status 200 and body containing '"text":"Second hello"' |
| 7 | The cursor loads the older message | ✅ PASS | Expected status 200 and body containing '"text":"First hello"' |
| 8 | Opening the pages marked Bob's incoming messages read | ✅ PASS | Expected status 200 and body containing '"unreadCount":0' |
| 9 | Bob archives the conversation for himself | ✅ PASS | Expected status 200 and body containing '"conversationKey"' |
| 10 | The archived conversation leaves Bob's list | ✅ PASS | Expected status 200 and body containing '"payload":[]' |
| 11 | Alice still sees the conversation (archive is per account) | ✅ PASS | Expected status 200 and body containing '"username":"bob_msg"' |
| 12 | Anonymous conversation list gets the same 403 status and body as production (timestamp ignored) | ✅ PASS | Expected exit code 0 |
| 13 | Messaging yourself is rejected with the standard 400 envelope (fresh account carol_msg) | ✅ PASS | Expected status 400 and body containing '"code":"INVALID_REQUEST"' |
| 14 | Carol messages Bob | ✅ PASS | Expected status 201 |
| 15 | Carol's own-name conversation is empty | ✅ PASS | Expected status 200 and body containing '"payload":[]' |
| 16 | Carol's sent message stays unread until Bob opens it | ✅ PASS | Expected status 200 and body containing '"read":false' |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:49621/actuator/health/readiness`
2. **Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded)**: command `python message_fixture_accounts.py http://127.0.0.1:49621 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
3. **Alice sends Bob a message (201, mine=true for the sender)**: http `POST http://127.0.0.1:49621/api/messages/2025-09-14`
4. **Alice sends a second message**: http `POST http://127.0.0.1:49621/api/messages/2025-09-14`
5. **Bob's conversation list shows alice_msg with two unread**: http `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations`
6. **Paged open with size 1 returns the newest message and a cursor**: http `GET http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg?size=1`
7. **The cursor loads the older message**: http `GET http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg?size=1&cursor=djEKMjAyNi0xMC0wN1QwMTo1MjowMC4wMjBaCjMzY2JjZTQyLTg0ZmItNGM5Zi04Mjg0LWY4OGUxMTJiM2VhMA`
8. **Opening the pages marked Bob's incoming messages read**: http `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations`
9. **Bob archives the conversation for himself**: http `POST http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg/archive`
10. **The archived conversation leaves Bob's list**: http `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations`
11. **Alice still sees the conversation (archive is per account)**: http `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations`
12. **Anonymous conversation list gets the same 403 status and body as production (timestamp ignored)**: command `python compare_status_and_body.py http://127.0.0.1:49621/api/messages/2025-09-14/conversations https://www.christopherbell.dev/api/messages/2025-09-14/conversations 403`
13. **Messaging yourself is rejected with the standard 400 envelope (fresh account carol_msg)**: http `POST http://127.0.0.1:49621/api/messages/2025-09-14`
14. **Carol messages Bob**: http `POST http://127.0.0.1:49621/api/messages/2025-09-14`
15. **Carol's own-name conversation is empty**: http `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversation/carol_msg`
16. **Carol's sent message stays unread until Bob opens it**: http `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversation/bob_msg`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:49620 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:49621, base 6dad824b |
| Credentials | three disposable USERs in the throwaway database; passwords generated and never recorded; bearer tokens masked |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:49621/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `python message_fixture_accounts.py http://127.0.0.1:49621 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `POST http://127.0.0.1:49621/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `POST http://127.0.0.1:49621/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg?size=1` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg?size=1&cursor=djEKMjAyNi0xMC0wN1QwMTo1MjowMC4wMjBaCjMzY2JjZTQyLTg0ZmItNGM5Zi04Mjg0LWY4OGUxMTJiM2VhMA` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `POST http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg/archive` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `python compare_status_and_body.py http://127.0.0.1:49621/api/messages/2025-09-14/conversations https://www.christopherbell.dev/api/messages/2025-09-14/conversations 403` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `POST http://127.0.0.1:49621/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `POST http://127.0.0.1:49621/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversation/carol_msg` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Local command:** `GET http://127.0.0.1:49621/api/messages/2025-09-14/conversation/bob_msg` in `A:\Projects\christopherbell.dev-worktrees\style-message`
- **Candidate identity:** `4c2175f`
- **Cleanup:** Stopped candidate PID 42884 and mongod PID 21968 by process tree; both ports have zero listeners; scratch token files deleted; production MongoDB 27017 untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:49621/actuator/health/readiness
```

### 2. Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded)

```text
python message_fixture_accounts.py http://127.0.0.1:49621 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 3. Alice sends Bob a message (201, mine=true for the sender)

```http
POST http://127.0.0.1:49621/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"bob_msg","text":"First hello"}
```

### 4. Alice sends a second message

```http
POST http://127.0.0.1:49621/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"bob_msg","text":"Second hello"}
```

### 5. Bob's conversation list shows alice_msg with two unread

```http
GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations
Authorization: [REDACTED]
```

### 6. Paged open with size 1 returns the newest message and a cursor

```http
GET http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg?size=1
Authorization: [REDACTED]
```

### 7. The cursor loads the older message

```http
GET http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg?size=1&cursor=djEKMjAyNi0xMC0wN1QwMTo1MjowMC4wMjBaCjMzY2JjZTQyLTg0ZmItNGM5Zi04Mjg0LWY4OGUxMTJiM2VhMA
Authorization: [REDACTED]
```

### 8. Opening the pages marked Bob's incoming messages read

```http
GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations
Authorization: [REDACTED]
```

### 9. Bob archives the conversation for himself

```http
POST http://127.0.0.1:49621/api/messages/2026-07-26/conversation/alice_msg/archive
Authorization: [REDACTED]
```

### 10. The archived conversation leaves Bob's list

```http
GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations
Authorization: [REDACTED]
```

### 11. Alice still sees the conversation (archive is per account)

```http
GET http://127.0.0.1:49621/api/messages/2025-09-14/conversations
Authorization: [REDACTED]
```

### 12. Anonymous conversation list gets the same 403 status and body as production (timestamp ignored)

```text
python compare_status_and_body.py http://127.0.0.1:49621/api/messages/2025-09-14/conversations https://www.christopherbell.dev/api/messages/2025-09-14/conversations 403
```

### 13. Messaging yourself is rejected with the standard 400 envelope (fresh account carol_msg)

```http
POST http://127.0.0.1:49621/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"carol_msg","text":"me"}
```

### 14. Carol messages Bob

```http
POST http://127.0.0.1:49621/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"bob_msg","text":"Carol says hi"}
```

### 15. Carol's own-name conversation is empty

```http
GET http://127.0.0.1:49621/api/messages/2025-09-14/conversation/carol_msg
Authorization: [REDACTED]
```

### 16. Carol's sent message stays unread until Bob opens it

```http
GET http://127.0.0.1:49621/api/messages/2025-09-14/conversation/bob_msg
Authorization: [REDACTED]
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 41608f38-c8db-4bc4-bb5f-0ad284ce821c
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337978
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
Date: Wed, 07 Oct 2026 01:51:58 GMT
Connection: close

{"status":"UP"}
```

### 2. Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
alice_msg create 201 login 200
bob_msg create 201 login 200
```

### 3. Alice sends Bob a message (201, mine=true for the sender)

```text
HTTP 201 
X-Request-Id: f7a2a108-28b6-45aa-92a9-e0453d0df801
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791337979
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
Date: Wed, 07 Oct 2026 01:51:59 GMT
Connection: close

{"messages":null,"payload":{"id":"16b848a2-ec71-4c26-a048-407c013b32ef","senderAccountId":"763ec32f-90fa-4562-9432-20230f4d814c","senderUsername":"alice_msg","recipientAccountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","recipientUsername":"bob_msg","text":"First hello","read":false,"mine":true,"createdOn":"2026-10-07T01:51:59.826871500Z"},"requestId":null,"success":true}
```

### 4. Alice sends a second message

```text
HTTP 201 
X-Request-Id: 29b5e9d9-4514-4bdc-ab2d-62460348dfa4
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791337980
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
Date: Wed, 07 Oct 2026 01:52:00 GMT
Connection: close

{"messages":null,"payload":{"id":"33cbce42-84fb-4c9f-8284-f88e112b3ea0","senderAccountId":"763ec32f-90fa-4562-9432-20230f4d814c","senderUsername":"alice_msg","recipientAccountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","recipientUsername":"bob_msg","text":"Second hello","read":false,"mine":true,"createdOn":"2026-10-07T01:52:00.020200800Z"},"requestId":null,"success":true}
```

### 5. Bob's conversation list shows alice_msg with two unread

```text
HTTP 200 
X-Request-Id: 9bc96cb0-79a1-4d0d-a89a-36848326608b
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337980
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
Date: Wed, 07 Oct 2026 01:52:00 GMT
Connection: close

{"messages":null,"payload":[{"accountId":"763ec32f-90fa-4562-9432-20230f4d814c","username":"alice_msg","displayName":"Alice Check","latestText":"Second hello","lastMessageOn":"2026-10-07T01:52:00.020Z","unreadCount":2}],"requestId":null,"success":true}
```

### 6. Paged open with size 1 returns the newest message and a cursor

```text
HTTP 200 
X-Request-Id: 0cb83c33-05bb-4425-9194-b5c0f204b92e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337980
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
Date: Wed, 07 Oct 2026 01:52:00 GMT
Connection: close

{"messages":null,"payload":{"items":[{"id":"33cbce42-84fb-4c9f-8284-f88e112b3ea0","senderAccountId":"763ec32f-90fa-4562-9432-20230f4d814c","senderUsername":"alice_msg","recipientAccountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","recipientUsername":"bob_msg","text":"Second hello","read":true,"mine":false,"createdOn":"2026-10-07T01:52:00.020Z"}],"nextCursor":"djEKMjAyNi0xMC0wN1QwMTo1MjowMC4wMjBaCjMzY2JjZTQyLTg0ZmItNGM5Zi04Mjg0LWY4OGUxMTJiM2VhMA"},"requestId":null,"success":true}
```

### 7. The cursor loads the older message

```text
HTTP 200 
X-Request-Id: eeff2483-fbf7-46b1-8001-f87aed797725
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337980
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
Date: Wed, 07 Oct 2026 01:52:00 GMT
Connection: close

{"messages":null,"payload":{"items":[{"id":"16b848a2-ec71-4c26-a048-407c013b32ef","senderAccountId":"763ec32f-90fa-4562-9432-20230f4d814c","senderUsername":"alice_msg","recipientAccountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","recipientUsername":"bob_msg","text":"First hello","read":true,"mine":false,"createdOn":"2026-10-07T01:51:59.826Z"}],"nextCursor":null},"requestId":null,"success":true}
```

### 8. Opening the pages marked Bob's incoming messages read

```text
HTTP 200 
X-Request-Id: 7858d415-877f-4a8c-9747-63b31a3c3b51
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337980
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
Date: Wed, 07 Oct 2026 01:52:00 GMT
Connection: close

{"messages":null,"payload":[{"accountId":"763ec32f-90fa-4562-9432-20230f4d814c","username":"alice_msg","displayName":"Alice Check","latestText":"Second hello","lastMessageOn":"2026-10-07T01:52:00.020Z","unreadCount":0}],"requestId":null,"success":true}
```

### 9. Bob archives the conversation for himself

```text
HTTP 200 
X-Request-Id: 232b817f-b4aa-4018-82a5-21477fff07b0
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791337981
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
Date: Wed, 07 Oct 2026 01:52:01 GMT
Connection: close

{"messages":null,"payload":{"conversationKey":"09687bc0-96b6-4a1e-a79d-7512a5669846:763ec32f-90fa-4562-9432-20230f4d814c","archivedAt":"2026-10-07T01:52:01.257424500Z"},"requestId":null,"success":true}
```

### 10. The archived conversation leaves Bob's list

```text
HTTP 200 
X-Request-Id: 16b28925-f805-4dad-9355-804eba55c1f6
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337981
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
Date: Wed, 07 Oct 2026 01:52:01 GMT
Connection: close

{"messages":null,"payload":[],"requestId":null,"success":true}
```

### 11. Alice still sees the conversation (archive is per account)

```text
HTTP 200 
X-Request-Id: 4b63e63e-d48a-4506-be73-f3f5639135e5
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791337981
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
Date: Wed, 07 Oct 2026 01:52:01 GMT
Connection: close

{"messages":null,"payload":[{"accountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","username":"bob_msg","displayName":"Bob Check","latestText":"Second hello","lastMessageOn":"2026-10-07T01:52:00.020Z","unreadCount":0}],"requestId":null,"success":true}
```

### 12. Anonymous conversation list gets the same 403 status and body as production (timestamp ignored)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/messages/2025-09-14/conversations'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/messages/2025-09-14/conversations'}
```

### 13. Messaging yourself is rejected with the standard 400 envelope (fresh account carol_msg)

```text
HTTP 400 
X-Request-Id: df426a08-6959-43f2-9e0e-5fe677fbf106
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791337999
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
Date: Wed, 07 Oct 2026 01:52:19 GMT
Connection: close

{"messages":[{"code":"INVALID_REQUEST","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

### 14. Carol messages Bob

```text
HTTP 201 
X-Request-Id: 11a51b30-77fe-46f9-80e8-728ff555246a
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791337999
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
Date: Wed, 07 Oct 2026 01:52:19 GMT
Connection: close

{"messages":null,"payload":{"id":"603862be-5994-4a6c-ac0a-159794d2b3ac","senderAccountId":"0f07f32c-393d-400f-bf47-ebec0b8910b1","senderUsername":"carol_msg","recipientAccountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","recipientUsername":"bob_msg","text":"Carol says hi","read":false,"mine":true,"createdOn":"2026-10-07T01:52:19.880898800Z"},"requestId":null,"success":true}
```

### 15. Carol's own-name conversation is empty

```text
HTTP 200 
X-Request-Id: a40ea287-0714-4624-95da-42879972ab14
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791338000
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
Date: Wed, 07 Oct 2026 01:52:20 GMT
Connection: close

{"messages":null,"payload":[],"requestId":null,"success":true}
```

### 16. Carol's sent message stays unread until Bob opens it

```text
HTTP 200 
X-Request-Id: a2d3d8c2-57ff-4e30-a444-49bc15e85435
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791338000
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
Date: Wed, 07 Oct 2026 01:52:20 GMT
Connection: close

{"messages":null,"payload":[{"id":"603862be-5994-4a6c-ac0a-159794d2b3ac","senderAccountId":"0f07f32c-393d-400f-bf47-ebec0b8910b1","senderUsername":"carol_msg","recipientAccountId":"09687bc0-96b6-4a1e-a79d-7512a5669846","recipientUsername":"bob_msg","text":"Carol says hi","read":false,"mine":true,"createdOn":"2026-10-07T01:52:19.880Z"}],"requestId":null,"success":true}
```

## Evidence
- Case 1 started 2026-10-06T20:51:58-05:00, took 46 ms, candidate `4c2175f`
- Case 2 started 2026-10-06T20:51:58-05:00, took 640 ms, candidate `unknown`
- Case 3 started 2026-10-06T20:51:59-05:00, took 78 ms, candidate `4c2175f`
- Case 4 started 2026-10-06T20:51:59-05:00, took 62 ms, candidate `4c2175f`
- Case 5 started 2026-10-06T20:52:00-05:00, took 78 ms, candidate `4c2175f`
- Case 6 started 2026-10-06T20:52:00-05:00, took 62 ms, candidate `4c2175f`
- Case 7 started 2026-10-06T20:52:00-05:00, took 32 ms, candidate `4c2175f`
- Case 8 started 2026-10-06T20:52:00-05:00, took 30 ms, candidate `4c2175f`
- Case 9 started 2026-10-06T20:52:01-05:00, took 46 ms, candidate `4c2175f`
- Case 10 started 2026-10-06T20:52:01-05:00, took 62 ms, candidate `4c2175f`
- Case 11 started 2026-10-06T20:52:01-05:00, took 31 ms, candidate `4c2175f`
- Case 12 started 2026-10-06T20:52:01-05:00, took 265 ms, candidate `unknown`
- Case 13 started 2026-10-06T20:52:19-05:00, took 32 ms, candidate `4c2175f`
- Case 14 started 2026-10-06T20:52:19-05:00, took 46 ms, candidate `4c2175f`
- Case 15 started 2026-10-06T20:52:20-05:00, took 32 ms, candidate `4c2175f`
- Case 16 started 2026-10-06T20:52:20-05:00, took 30 ms, candidate `4c2175f`

## Bugs / Follow-ups
- **Native checks on the candidate:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m39s. Message suites: service 9/9, controller 6/6, query repository 4/4 and archive 2/2; the Mongo contract tests are skipped without their database, as in CI. `ModularMonolithArchitectureTest` passed 5/5. JS and Pester suites passed.
- **Harness note:** two first-run cases had wrong inputs, and both are excluded above:
  - The self-message case expected the internal message text, but the API returns the standard generic 400 envelope.
  - The sender-view case asked for Alice's conversation with herself.

  Both were rerun correctly with a fresh account, `carol_msg`, and passed.

## Document Status
complete

## Project
christopherbell-dev
