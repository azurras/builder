# Notification slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 9 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-21-07-christopherbell-dev-notification-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-notification-20261006` at candidate `ef4d9a5`

## Pass / Fail

> [!TIP]
> 16 of 16 cases passed on candidate `ef4d9a5`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Bob starts with no unread notifications | ✅ PASS | Expected status 200 and body containing '"payload":0' |
| 4 | Alice messages Bob | ✅ PASS | Expected status 201 |
| 5 | The message notifies Bob (unread count 1) | ✅ PASS | Expected status 200 and body containing '"payload":1' |
| 6 | Bob's notification list shows the MESSAGE notification from alice_msg | ✅ PASS | Expected status 200 and body containing '"notificationType":"MESSAGE"' |
| 7 | The paged inbox returns the same notification | ✅ PASS | Expected status 200 and body containing '"id":"3a31d6da-dbcb-4274-864b-39bc49ca3b8c"' |
| 8 | Bob marks the notification read | ✅ PASS | Expected status 200 and body containing '"read":true' |
| 9 | Alice cannot mark Bob's notification (404) | ✅ PASS | Expected status 404 |
| 10 | Alice messages Bob again | ✅ PASS | Expected status 201 |
| 11 | Bob marks all notifications read | ✅ PASS | Expected status 200 and body containing '"payload":{' |
| 12 | Unread count is back to 0 after read-all | ✅ PASS | Expected status 200 and body containing '"payload":0' |
| 13 | Bob turns off message notifications | ✅ PASS | Expected status 200 and body containing '"messages":false' |
| 14 | Alice messages Bob a third time | ✅ PASS | Expected status 201 |
| 15 | No notification is delivered while Bob has message notifications off | ✅ PASS | Expected status 200 and body containing '"payload":0' |
| 16 | Anonymous unread count gets the same 403 status and body as production (timestamp ignored) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:64698/actuator/health/readiness`
2. **Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded)**: command `python message_fixture_accounts.py http://127.0.0.1:64698 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad`
3. **Bob starts with no unread notifications**: http `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count`
4. **Alice messages Bob**: http `POST http://127.0.0.1:64698/api/messages/2025-09-14`
5. **The message notifies Bob (unread count 1)**: http `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count`
6. **Bob's notification list shows the MESSAGE notification from alice_msg**: http `GET http://127.0.0.1:64698/api/notifications/2025-09-14?limit=10`
7. **The paged inbox returns the same notification**: http `GET http://127.0.0.1:64698/api/notifications/2026-07-26?size=5`
8. **Bob marks the notification read**: http `POST http://127.0.0.1:64698/api/notifications/2025-09-14/3a31d6da-dbcb-4274-864b-39bc49ca3b8c/read`
9. **Alice cannot mark Bob's notification (404)**: http `POST http://127.0.0.1:64698/api/notifications/2025-09-14/3a31d6da-dbcb-4274-864b-39bc49ca3b8c/read`
10. **Alice messages Bob again**: http `POST http://127.0.0.1:64698/api/messages/2025-09-14`
11. **Bob marks all notifications read**: http `POST http://127.0.0.1:64698/api/notifications/2026-07-26/read-all`
12. **Unread count is back to 0 after read-all**: http `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count`
13. **Bob turns off message notifications**: http `PUT http://127.0.0.1:64698/api/notifications/2025-09-14/preferences`
14. **Alice messages Bob a third time**: http `POST http://127.0.0.1:64698/api/messages/2025-09-14`
15. **No notification is delivered while Bob has message notifications off**: http `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count`
16. **Anonymous unread count gets the same 403 status and body as production (timestamp ignored)**: command `python compare_status_and_body.py http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count https://www.christopherbell.dev/api/notifications/2025-09-14/unread-count 403`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:64697 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:64698, base 38907c6c |
| Credentials | two disposable USERs in the throwaway database; passwords generated and never recorded; bearer tokens masked |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:64698/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `python message_fixture_accounts.py http://127.0.0.1:64698 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `POST http://127.0.0.1:64698/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `GET http://127.0.0.1:64698/api/notifications/2025-09-14?limit=10` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `GET http://127.0.0.1:64698/api/notifications/2026-07-26?size=5` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `POST http://127.0.0.1:64698/api/notifications/2025-09-14/3a31d6da-dbcb-4274-864b-39bc49ca3b8c/read` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `POST http://127.0.0.1:64698/api/notifications/2025-09-14/3a31d6da-dbcb-4274-864b-39bc49ca3b8c/read` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `POST http://127.0.0.1:64698/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `POST http://127.0.0.1:64698/api/notifications/2026-07-26/read-all` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `PUT http://127.0.0.1:64698/api/notifications/2025-09-14/preferences` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `POST http://127.0.0.1:64698/api/messages/2025-09-14` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count` in `A:\Projects\christopherbell.dev-worktrees\style-notification`
- **Local command:** `python compare_status_and_body.py http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count https://www.christopherbell.dev/api/notifications/2025-09-14/unread-count 403` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Candidate identity:** `ef4d9a5`
- **Cleanup:** Stopped candidate PID 49684 and mongod PID 82396 by process tree; both ports have zero listeners; scratch token files deleted; production MongoDB 27017 untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:64698/actuator/health/readiness
```

### 2. Create alice_msg and bob_msg through the API and log both in (passwords generated, not recorded)

```text
python message_fixture_accounts.py http://127.0.0.1:64698 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad
```

### 3. Bob starts with no unread notifications

```http
GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count
Authorization: [REDACTED]
```

### 4. Alice messages Bob

```http
POST http://127.0.0.1:64698/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"bob_msg","text":"Ping"}
```

### 5. The message notifies Bob (unread count 1)

```http
GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count
Authorization: [REDACTED]
```

### 6. Bob's notification list shows the MESSAGE notification from alice_msg

```http
GET http://127.0.0.1:64698/api/notifications/2025-09-14?limit=10
Authorization: [REDACTED]
```

### 7. The paged inbox returns the same notification

```http
GET http://127.0.0.1:64698/api/notifications/2026-07-26?size=5
Authorization: [REDACTED]
```

### 8. Bob marks the notification read

```http
POST http://127.0.0.1:64698/api/notifications/2025-09-14/3a31d6da-dbcb-4274-864b-39bc49ca3b8c/read
Authorization: [REDACTED]
```

### 9. Alice cannot mark Bob's notification (404)

```http
POST http://127.0.0.1:64698/api/notifications/2025-09-14/3a31d6da-dbcb-4274-864b-39bc49ca3b8c/read
Authorization: [REDACTED]
```

### 10. Alice messages Bob again

```http
POST http://127.0.0.1:64698/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"bob_msg","text":"Ping two"}
```

### 11. Bob marks all notifications read

```http
POST http://127.0.0.1:64698/api/notifications/2026-07-26/read-all
Authorization: [REDACTED]
```

### 12. Unread count is back to 0 after read-all

```http
GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count
Authorization: [REDACTED]
```

### 13. Bob turns off message notifications

```http
PUT http://127.0.0.1:64698/api/notifications/2025-09-14/preferences
Authorization: [REDACTED]
Content-Type: application/json

{"mentions":true,"likes":true,"comments":true,"messages":false,"wflSessions":true}
```

### 14. Alice messages Bob a third time

```http
POST http://127.0.0.1:64698/api/messages/2025-09-14
Authorization: [REDACTED]
Content-Type: application/json

{"recipientUsername":"bob_msg","text":"Ping three"}
```

### 15. No notification is delivered while Bob has message notifications off

```http
GET http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count
Authorization: [REDACTED]
```

### 16. Anonymous unread count gets the same 403 status and body as production (timestamp ignored)

```text
python compare_status_and_body.py http://127.0.0.1:64698/api/notifications/2025-09-14/unread-count https://www.christopherbell.dev/api/notifications/2025-09-14/unread-count 403
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 34f2899f-7d32-4106-841e-5ed2429c7c29
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339218
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
Date: Wed, 07 Oct 2026 02:12:38 GMT
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

### 3. Bob starts with no unread notifications

```text
HTTP 200 
X-Request-Id: f7a73a6f-f41d-44b4-94e2-72e6b3557e12
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339219
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
Date: Wed, 07 Oct 2026 02:12:39 GMT
Connection: close

{"messages":null,"payload":0,"requestId":null,"success":true}
```

### 4. Alice messages Bob

```text
HTTP 201 
X-Request-Id: b8802e29-88db-4f77-9459-1e01a941a0c5
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791339219
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
Date: Wed, 07 Oct 2026 02:12:39 GMT
Connection: close

{"messages":null,"payload":{"id":"9b7939f6-289a-4afc-999f-2fff7e0c7b3b","senderAccountId":"c94f1261-3149-4cfb-8455-ec6741e04393","senderUsername":"alice_msg","recipientAccountId":"95a6ed2b-4ac2-4985-aade-972d800df083","recipientUsername":"bob_msg","text":"Ping","read":false,"mine":true,"createdOn":"2026-10-07T02:12:39.753123100Z"},"requestId":null,"success":true}
```

### 5. The message notifies Bob (unread count 1)

```text
HTTP 200 
X-Request-Id: aefdcf52-a2dc-4e71-8a0f-328150ba1345
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339219
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
Date: Wed, 07 Oct 2026 02:12:39 GMT
Connection: close

{"messages":null,"payload":1,"requestId":null,"success":true}
```

### 6. Bob's notification list shows the MESSAGE notification from alice_msg

```text
HTTP 200 
X-Request-Id: 52835f11-9300-45df-a92d-a263634216ed
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339220
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
Date: Wed, 07 Oct 2026 02:12:40 GMT
Connection: close

{"messages":null,"payload":[{"id":"3a31d6da-dbcb-4274-864b-39bc49ca3b8c","accountId":"95a6ed2b-4ac2-4985-aade-972d800df083","actorAccountId":"c94f1261-3149-4cfb-8455-ec6741e04393","actorUsername":"alice_msg","postId":null,"postText":null,"messageId":"9b7939f6-289a-4afc-999f-2fff7e0c7b3b","messageText":"Ping","whatsForLunchSessionId":null,"whatsForLunchSessionText":null,"notificationType":"MESSAGE","read":false,"createdOn":"2026-10-07T02:12:39.766Z"}],"requestId":null,"success":true}
```

### 7. The paged inbox returns the same notification

```text
HTTP 200 
X-Request-Id: 3f4c2cb8-7ede-4a8e-8a09-04d5bf2effb6
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339220
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
Date: Wed, 07 Oct 2026 02:12:40 GMT
Connection: close

{"messages":null,"payload":{"items":[{"id":"3a31d6da-dbcb-4274-864b-39bc49ca3b8c","accountId":"95a6ed2b-4ac2-4985-aade-972d800df083","actorAccountId":"c94f1261-3149-4cfb-8455-ec6741e04393","actorUsername":"alice_msg","postId":null,"postText":null,"messageId":"9b7939f6-289a-4afc-999f-2fff7e0c7b3b","messageText":"Ping","whatsForLunchSessionId":null,"whatsForLunchSessionText":null,"notificationType":"MESSAGE","read":false,"createdOn":"2026-10-07T02:12:39.766Z"}],"nextCursor":null},"requestId":null,"success":true}
```

### 8. Bob marks the notification read

```text
HTTP 200 
X-Request-Id: 8a4dcca9-54bb-44ee-a54c-993fdf4a59a8
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791339220
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
Date: Wed, 07 Oct 2026 02:12:40 GMT
Connection: close

{"messages":null,"payload":{"id":"3a31d6da-dbcb-4274-864b-39bc49ca3b8c","accountId":"95a6ed2b-4ac2-4985-aade-972d800df083","actorAccountId":"c94f1261-3149-4cfb-8455-ec6741e04393","actorUsername":"alice_msg","postId":null,"postText":null,"messageId":"9b7939f6-289a-4afc-999f-2fff7e0c7b3b","messageText":"Ping","whatsForLunchSessionId":null,"whatsForLunchSessionText":null,"notificationType":"MESSAGE","read":true,"createdOn":"2026-10-07T02:12:39.766Z"},"requestId":null,"success":true}
```

### 9. Alice cannot mark Bob's notification (404)

```text
HTTP 404 
X-Request-Id: 8afda8dc-25d9-4259-9dc3-c1cd076267d8
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791339220
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
Content-Length: 146
Date: Wed, 07 Oct 2026 02:12:40 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 10. Alice messages Bob again

```text
HTTP 201 
X-Request-Id: 051797ed-f92c-40e5-b3de-46daa34b21ab
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791339220
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
Date: Wed, 07 Oct 2026 02:12:40 GMT
Connection: close

{"messages":null,"payload":{"id":"c11096f3-6fd2-4c20-a347-d1d62411fc63","senderAccountId":"c94f1261-3149-4cfb-8455-ec6741e04393","senderUsername":"alice_msg","recipientAccountId":"95a6ed2b-4ac2-4985-aade-972d800df083","recipientUsername":"bob_msg","text":"Ping two","read":false,"mine":true,"createdOn":"2026-10-07T02:12:40.802660800Z"},"requestId":null,"success":true}
```

### 11. Bob marks all notifications read

```text
HTTP 200 
X-Request-Id: 45005ec7-54cc-424a-928a-48c04435beaf
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791339220
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
Date: Wed, 07 Oct 2026 02:12:40 GMT
Connection: close

{"messages":null,"payload":{"updatedCount":1},"requestId":null,"success":true}
```

### 12. Unread count is back to 0 after read-all

```text
HTTP 200 
X-Request-Id: da81fd5c-8c75-4c1f-b36d-2dd2c32a7a11
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339221
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
Date: Wed, 07 Oct 2026 02:12:41 GMT
Connection: close

{"messages":null,"payload":0,"requestId":null,"success":true}
```

### 13. Bob turns off message notifications

```text
HTTP 200 
X-Request-Id: bff1bc43-82e7-43f8-8665-d086d1fefefe
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791339221
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
Date: Wed, 07 Oct 2026 02:12:41 GMT
Connection: close

{"messages":null,"payload":{"mentions":true,"likes":true,"comments":true,"messages":false,"wflSessions":true},"requestId":null,"success":true}
```

### 14. Alice messages Bob a third time

```text
HTTP 201 
X-Request-Id: f1c6d94d-f47e-4e92-a38f-ee8ef2058e17
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791339221
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
Date: Wed, 07 Oct 2026 02:12:41 GMT
Connection: close

{"messages":null,"payload":{"id":"ab8dc136-030a-4644-b5f0-f5114be9626b","senderAccountId":"c94f1261-3149-4cfb-8455-ec6741e04393","senderUsername":"alice_msg","recipientAccountId":"95a6ed2b-4ac2-4985-aade-972d800df083","recipientUsername":"bob_msg","text":"Ping three","read":false,"mine":true,"createdOn":"2026-10-07T02:12:41.417274800Z"},"requestId":null,"success":true}
```

### 15. No notification is delivered while Bob has message notifications off

```text
HTTP 200 
X-Request-Id: 79a73ab0-4e91-4249-81fc-80ca33c2dff1
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791339221
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
Date: Wed, 07 Oct 2026 02:12:41 GMT
Connection: close

{"messages":null,"payload":0,"requestId":null,"success":true}
```

### 16. Anonymous unread count gets the same 403 status and body as production (timestamp ignored)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/notifications/2025-09-14/unread-count'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/notifications/2025-09-14/unread-count'}
```

## Evidence
- Case 1 started 2026-10-06T21:12:38-05:00, took 46 ms, candidate `ef4d9a5`
- Case 2 started 2026-10-06T21:12:38-05:00, took 640 ms, candidate `unknown`
- Case 3 started 2026-10-06T21:12:39-05:00, took 46 ms, candidate `ef4d9a5`
- Case 4 started 2026-10-06T21:12:39-05:00, took 78 ms, candidate `ef4d9a5`
- Case 5 started 2026-10-06T21:12:39-05:00, took 62 ms, candidate `ef4d9a5`
- Case 6 started 2026-10-06T21:12:40-05:00, took 47 ms, candidate `ef4d9a5`
- Case 7 started 2026-10-06T21:12:40-05:00, took 30 ms, candidate `ef4d9a5`
- Case 8 started 2026-10-06T21:12:40-05:00, took 31 ms, candidate `ef4d9a5`
- Case 9 started 2026-10-06T21:12:40-05:00, took 46 ms, candidate `ef4d9a5`
- Case 10 started 2026-10-06T21:12:40-05:00, took 46 ms, candidate `ef4d9a5`
- Case 11 started 2026-10-06T21:12:40-05:00, took 30 ms, candidate `ef4d9a5`
- Case 12 started 2026-10-06T21:12:41-05:00, took 31 ms, candidate `ef4d9a5`
- Case 13 started 2026-10-06T21:12:41-05:00, took 30 ms, candidate `ef4d9a5`
- Case 14 started 2026-10-06T21:12:41-05:00, took 32 ms, candidate `ef4d9a5`
- Case 15 started 2026-10-06T21:12:41-05:00, took 30 ms, candidate `ef4d9a5`
- Case 16 started 2026-10-06T21:12:41-05:00, took 469 ms, candidate `unknown`

## Bugs / Follow-ups
- **Native checks on the candidate:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m50s. Notification suites: delivery 9/9, controller 10/10, fanout guard 5/5, preference 4/4, query 2/2 and cleanup context 1/1; the Mongo contract tests are skipped without their database, as in CI. `ModularMonolithArchitectureTest` passed 5/5 after its frozen store dropped four resolved entries. JS and Pester suites passed.

## Document Status
complete

## Project
christopherbell-dev
