# Vehicle slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 12 of the style migration ([plan](../implementation-plans/2026-10-09-10-04-christopherbell-dev-vehicle-slice-conforms-to-chris-street-style.md)): admin protection, single VIN decode and batch VIN decode behave as before, with the same published batch codes and messages

## Branch
`claude/style-vehicle-20261009` at candidate `aba533f`

## Pass / Fail

> [!TIP]
> 15 of 15 cases passed on candidate `aba533f`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create veh_user through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Anonymous vehicle list gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 4 | Anonymous data collection state gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 5 | A USER cannot list vehicles (403) | ✅ PASS | Expected status 403 |
| 6 | A USER cannot create a vehicle (403) | ✅ PASS | Expected status 403 |
| 7 | A USER cannot create vehicles from VINs (403) | ✅ PASS | Expected status 403 |
| 8 | A USER cannot delete a vehicle (403) | ✅ PASS | Expected status 403 |
| 9 | Single decode rejects a malformed VIN (400) | ✅ PASS | Expected status 400 |
| 10 | Single decode of a lower-case valid VIN returns NHTSA details | ✅ PASS | Expected status 200 and body containing '"vin":"1HGCM82633A004352"' |
| 11 | Batch decode returns the cached VIN as SUCCESS and the invalid one as INVALID_VIN, in order | ✅ PASS | Expected status 200 and body containing '"submittedCount":2,"successCount":1,"errorCount":1,"results":[{"index":0,"submittedVin":" 1hgcm82633a004352 ","normalizedVin":"1HGCM82633A004352","status":"SUCCESS"' |
| 12 | Batch error entries publish the same code and message as before | ✅ PASS | Expected status 200 and body containing '{"index":0,"submittedVin":"bad","normalizedVin":null,"status":"INVALID_VIN","decoded":null,"errorCode":"INVALID_VIN","errorMessage":"VIN must be 17 valid VIN characters."}' |
| 13 | Batch decode of a VIN with I, O or Q is INVALID_VIN | ✅ PASS | Expected status 200 and body containing '"status":"INVALID_VIN"' |
| 14 | An empty batch is rejected (400) | ✅ PASS | Expected status 400 |
| 15 | A batch over the 20-VIN limit is rejected (400) | ✅ PASS | Expected status 400 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:49398/actuator/health/readiness`
2. **Create veh_user through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:49398 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad veh_user`
3. **Anonymous vehicle list gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:49398/api/vehicles/2026-05-09 https://www.christopherbell.dev/api/vehicles/2026-05-09 403`
4. **Anonymous data collection state gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:49398/api/vehicles/2026-05-09/data-collection-state https://www.christopherbell.dev/api/vehicles/2026-05-09/data-collection-state 403`
5. **A USER cannot list vehicles (403)**: http `GET http://127.0.0.1:49398/api/vehicles/2026-05-09`
6. **A USER cannot create a vehicle (403)**: http `POST http://127.0.0.1:49398/api/vehicles/2026-05-09`
7. **A USER cannot create vehicles from VINs (403)**: http `POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vins`
8. **A USER cannot delete a vehicle (403)**: http `DELETE http://127.0.0.1:49398/api/vehicles/2026-05-09/some-id`
9. **Single decode rejects a malformed VIN (400)**: http `POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vin/decode`
10. **Single decode of a lower-case valid VIN returns NHTSA details**: http `POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vin/decode`
11. **Batch decode returns the cached VIN as SUCCESS and the invalid one as INVALID_VIN, in order**: http `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch`
12. **Batch error entries publish the same code and message as before**: http `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch`
13. **Batch decode of a VIN with I, O or Q is INVALID_VIN**: http `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch`
14. **An empty batch is rejected (400)**: http `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch`
15. **A batch over the 20-VIN limit is rejected (400)**: http `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:49397 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:49398, commit aba533fb |
| Credentials | one disposable USER in the throwaway database; password generated and never recorded; bearer token masked and token file deleted |
| External calls | one NHTSA vPIC decode of the public sample VIN 1HGCM82633A004352; production compared with read-only GETs only |
| Admin coverage | no supported way to create a local ADMIN, so admin success paths are covered by VehicleControllerTest and VehicleServiceTest |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:49398/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:49398 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad veh_user` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:49398/api/vehicles/2026-05-09 https://www.christopherbell.dev/api/vehicles/2026-05-09 403` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:49398/api/vehicles/2026-05-09/data-collection-state https://www.christopherbell.dev/api/vehicles/2026-05-09/data-collection-state 403` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `GET http://127.0.0.1:49398/api/vehicles/2026-05-09` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-05-09` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vins` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `DELETE http://127.0.0.1:49398/api/vehicles/2026-05-09/some-id` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vin/decode` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vin/decode` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Local command:** `POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch` in `A:\Projects\christopherbell.dev-worktrees\style-vehicle`
- **Candidate identity:** `aba533f`
- **Cleanup:** Candidate and mongod stopped; both ports have no listeners; production mongod on 27017 untouched

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:49398/actuator/health/readiness
```

### 2. Create veh_user through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:49398 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad veh_user
```

### 3. Anonymous vehicle list gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:49398/api/vehicles/2026-05-09 https://www.christopherbell.dev/api/vehicles/2026-05-09 403
```

### 4. Anonymous data collection state gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:49398/api/vehicles/2026-05-09/data-collection-state https://www.christopherbell.dev/api/vehicles/2026-05-09/data-collection-state 403
```

### 5. A USER cannot list vehicles (403)

```http
GET http://127.0.0.1:49398/api/vehicles/2026-05-09
Authorization: [REDACTED]
```

### 6. A USER cannot create a vehicle (403)

```http
POST http://127.0.0.1:49398/api/vehicles/2026-05-09
Authorization: [REDACTED]
Content-Type: application/json

{"vin":"1HGCM82633A004352","make":"Honda","model":"Accord","year":2003}
```

### 7. A USER cannot create vehicles from VINs (403)

```http
POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vins
Authorization: [REDACTED]
Content-Type: application/json

{"vins":["1HGCM82633A004352"]}
```

### 8. A USER cannot delete a vehicle (403)

```http
DELETE http://127.0.0.1:49398/api/vehicles/2026-05-09/some-id
Authorization: [REDACTED]
```

### 9. Single decode rejects a malformed VIN (400)

```http
POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vin/decode
Authorization: [REDACTED]
Content-Type: application/json

{"vin":"NOT-A-VIN"}
```

### 10. Single decode of a lower-case valid VIN returns NHTSA details

```http
POST http://127.0.0.1:49398/api/vehicles/2026-05-09/vin/decode
Authorization: [REDACTED]
Content-Type: application/json

{"vin":"1hgcm82633a004352"}
```

### 11. Batch decode returns the cached VIN as SUCCESS and the invalid one as INVALID_VIN, in order

```http
POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch
Authorization: [REDACTED]
Content-Type: application/json

{"vins":[" 1hgcm82633a004352 ","bad"]}
```

### 12. Batch error entries publish the same code and message as before

```http
POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch
Authorization: [REDACTED]
Content-Type: application/json

{"vins":["bad"]}
```

### 13. Batch decode of a VIN with I, O or Q is INVALID_VIN

```http
POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch
Authorization: [REDACTED]
Content-Type: application/json

{"vins":["1HGCM82633A00435O"]}
```

### 14. An empty batch is rejected (400)

```http
POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch
Authorization: [REDACTED]
Content-Type: application/json

{"vins":[]}
```

### 15. A batch over the 20-VIN limit is rejected (400)

```http
POST http://127.0.0.1:49398/api/vehicles/2026-07-26/vin/decode/batch
Authorization: [REDACTED]
Content-Type: application/json

{"vins":["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u"]}
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 56fed04f-d90e-44c4-931f-82ba888962d8
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791558602
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
Date: Fri, 09 Oct 2026 15:09:02 GMT
Connection: close

{"status":"UP"}
```

### 2. Create veh_user through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
veh_user create 201 login 200
```

### 3. Anonymous vehicle list gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/vehicles/2026-05-09'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/vehicles/2026-05-09'}
```

### 4. Anonymous data collection state gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/vehicles/2026-05-09/data-collection-state'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/vehicles/2026-05-09/data-collection-state'}
```

### 5. A USER cannot list vehicles (403)

```text
HTTP 403 
X-Request-Id: fdad293f-d7bf-4daf-9c9c-e06aad563a02
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791558604
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
Date: Fri, 09 Oct 2026 15:09:04 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 6. A USER cannot create a vehicle (403)

```text
HTTP 403 
X-Request-Id: 63643bd9-07f5-4d2e-9299-488d1e80074d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558605
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
Date: Fri, 09 Oct 2026 15:09:05 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 7. A USER cannot create vehicles from VINs (403)

```text
HTTP 403 
X-Request-Id: 647b5cbf-767e-40cb-b164-67b8b12aca38
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558605
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
Date: Fri, 09 Oct 2026 15:09:05 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 8. A USER cannot delete a vehicle (403)

```text
HTTP 403 
X-Request-Id: c40e48da-d31c-4f0f-b08f-69c870d2c4e2
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558605
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
Date: Fri, 09 Oct 2026 15:09:05 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 9. Single decode rejects a malformed VIN (400)

```text
HTTP 400 
X-Request-Id: f5e9cf09-6c81-4de6-8e48-f4662c932284
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1791558605
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
Date: Fri, 09 Oct 2026 15:09:05 GMT
Connection: close

{"messages":[{"code":"REQUEST_ERROR","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

### 10. Single decode of a lower-case valid VIN returns NHTSA details

```text
HTTP 200 
X-Request-Id: fa23b2d9-9ec0-43f3-89ff-9e64b62c4cc0
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
X-RateLimit-Reset: 1791558605
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
Date: Fri, 09 Oct 2026 15:09:06 GMT
Connection: close

{"messages":null,"payload":{"vin":"1HGCM82633A004352","make":"HONDA","model":"Accord","year":2003,"body":"Coupe","plantCity":"MARYSVILLE","plantState":"OHIO","plantCountry":"UNITED STATES (USA)","errorCode":"0","errorText":"0 - VIN decoded clean. Check Digit (9th position) is correct","rawDecodedValues":{"ABS":"","ActiveSafetySysNote":"","AdaptiveCruiseControl":"","AdaptiveDrivingBeam":"","AdaptiveHeadlights":"","AdditionalErrorText":"","AirBagLocCurtain":"1st and 2nd Rows","AirBagLocFront":"1st Row (Driver and Passenger)","AirBagLocKnee":"","AirBagLocSeatCushion":"","AirBagLocSide":"1st Row (Driver and Passenger)","AutoReverseSystem":"","AutomaticPedestrianAlertingSound":"","AxleConfiguration":"","Axles":"","BasePrice":"","BatteryA":"","BatteryA_to":"","BatteryCells":"","BatteryInfo":"","BatteryKWh":"","BatteryKWh_to":"","BatteryModules":"","BatteryPacks":"","BatteryType":"","BatteryV":"","BatteryV_to":"","BedLengthIN":"","BedType":"Not Applicable","BlindSpotIntervention":"","BlindSpotMon":"","BodyCabType":"Not Applicable","BodyClass":"Coupe","BrakeSystemDesc":"","BrakeSystemType":"","BusFloorConfigType":"Not Applicable","BusLength":"","BusType":"Not Applicable","CAN_AACN":"","CIB":"","CashForClunkers":"","ChargerLevel":"","ChargerPowerKW":"","CombinedBrakingSystem":"","CoolingType":"","CurbWeightLB":"","CustomMotorcycleType":"Not Applicable","DaytimeRunningLight":"","DestinationMarket":"","DisplacementCC":"2998.832712","DisplacementCI":"183","DisplacementL":"2.998832712","Doors":"2","DriveType":"","DriverAssist":"","DynamicBrakeSupport":"","EDR":"","ESC":"","EVDriveUnit":"","ElectrificationLevel":"","EngineConfiguration":"V-Shaped","EngineCycles":"","EngineCylinders":"6","EngineHP":"240","EngineHP_to":"","EngineKW":"","EngineManufacturer":"","EngineModel":"J30A4","EntertainmentSystem":"","ErrorCode":"0","ErrorText":"0 - VIN decoded clean. Check Digit (9th position) is correct","ForwardCollisionWarning":"","FuelInjectionType":"","FuelTankMaterial":"","FuelTankType":"","FuelTypePrimary":"Gasoline","FuelTypeSecondary":"","GCWR":"","GCWR_to":"","GVWR":"Class 1C: 4,001 - 5,000 lb (1,814 - 2,268 kg)","GVWR_to":"Class 1: 6,000 lb or less (2,722 kg or less)","KeylessIgnition":"","LaneCenteringAssistance":"","LaneDepartureWarning":"","LaneKeepSystem":"","LowerBeamHeadlampLightSource":"","Make":"HONDA","MakeID":"474","Manufacturer":"AMERICAN HONDA MOTOR CO., INC.","ManufacturerId":"988","Model":"Accord","ModelID":"1861","ModelYear":"2003","MotorcycleChassisType":"Not Applicable","MotorcycleSuspensionType":"Not Applicable","NCSABodyType":"","NCSAMake":"","NCSAMapExcApprovedBy":"","NCSAMapExcApprovedOn":"","NCSAMappingException":"","NCSAModel":"","NCSANote":"","NonLandUse":"","Note":"","OtherBusInfo":"","OtherEngineInfo":"","OtherMotorcycleInfo":"","OtherRestraintSystemInfo":"Seat Belt (Rr center position)","OtherTrailerInfo":"","ParkAssist":"","PedestrianAutomaticEmergencyBraking":"","PlantCity":"MARYSVILLE","PlantCompanyName":"","PlantCountry":"UNITED STATES (USA)","PlantState":"OHIO","PossibleValues":"","Pretensioner":"","RearAutomaticEmergencyBraking":"","RearCrossTrafficAlert":"","RearVisibilitySystem":"","SAEAutomationLevel":"","SAEAutomationLevel_to":"","SeatBeltsAll":"Manual","SeatRows":"","Seats":"","SemiautomaticHeadlampBeamSwitching":"","Series":"","Series2":"","SteeringLocation":"","SuggestedVIN":"","TPMS":"","TopSpeedMPH":"","TrackWidth":"","TractionControl":"","TrailerBodyType":"Not Applicable","TrailerLength":"","TrailerType":"Not Applicable","TransmissionSpeeds":"5","TransmissionStyle":"Automatic","Trim":"EX-V6","Trim2":"","Turbo":"","VIN":"1HGCM82633A004352","ValveTrainDesign":"Single Overhead Cam (SOHC)","VehicleDescriptor":"1HGCM826*3A","VehicleType":"PASSENGER CAR","WheelBaseLong":"","WheelBaseShort":"","WheelBaseType":"","WheelSizeFront":"","WheelSizeRear":"","WheelieMitigation":"","Wheels":"","Windows":""}},"requestId":null,"success":true}
```

### 11. Batch decode returns the cached VIN as SUCCESS and the invalid one as INVALID_VIN, in order

```text
HTTP 200 
X-Request-Id: bce46bf6-62d2-47e0-a60c-521653443723
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558606
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
Date: Fri, 09 Oct 2026 15:09:06 GMT
Connection: close

{"messages":null,"payload":{"submittedCount":2,"successCount":1,"errorCount":1,"results":[{"index":0,"submittedVin":" 1hgcm82633a004352 ","normalizedVin":"1HGCM82633A004352","status":"SUCCESS","decoded":{"vin":"1HGCM82633A004352","make":"HONDA","model":"Accord","year":2003,"body":"Coupe","plantCity":"MARYSVILLE","plantState":"OHIO","plantCountry":"UNITED STATES (USA)","errorCode":"0","errorText":"0 - VIN decoded clean. Check Digit (9th position) is correct","rawDecodedValues":{"ABS":"","ActiveSafetySysNote":"","AdaptiveCruiseControl":"","AdaptiveDrivingBeam":"","AdaptiveHeadlights":"","AdditionalErrorText":"","AirBagLocCurtain":"1st and 2nd Rows","AirBagLocFront":"1st Row (Driver and Passenger)","AirBagLocKnee":"","AirBagLocSeatCushion":"","AirBagLocSide":"1st Row (Driver and Passenger)","AutoReverseSystem":"","AutomaticPedestrianAlertingSound":"","AxleConfiguration":"","Axles":"","BasePrice":"","BatteryA":"","BatteryA_to":"","BatteryCells":"","BatteryInfo":"","BatteryKWh":"","BatteryKWh_to":"","BatteryModules":"","BatteryPacks":"","BatteryType":"","BatteryV":"","BatteryV_to":"","BedLengthIN":"","BedType":"Not Applicable","BlindSpotIntervention":"","BlindSpotMon":"","BodyCabType":"Not Applicable","BodyClass":"Coupe","BrakeSystemDesc":"","BrakeSystemType":"","BusFloorConfigType":"Not Applicable","BusLength":"","BusType":"Not Applicable","CAN_AACN":"","CIB":"","CashForClunkers":"","ChargerLevel":"","ChargerPowerKW":"","CombinedBrakingSystem":"","CoolingType":"","CurbWeightLB":"","CustomMotorcycleType":"Not Applicable","DaytimeRunningLight":"","DestinationMarket":"","DisplacementCC":"2998.832712","DisplacementCI":"183","DisplacementL":"2.998832712","Doors":"2","DriveType":"","DriverAssist":"","DynamicBrakeSupport":"","EDR":"","ESC":"","EVDriveUnit":"","ElectrificationLevel":"","EngineConfiguration":"V-Shaped","EngineCycles":"","EngineCylinders":"6","EngineHP":"240","EngineHP_to":"","EngineKW":"","EngineManufacturer":"","EngineModel":"J30A4","EntertainmentSystem":"","ErrorCode":"0","ErrorText":"0 - VIN decoded clean. Check Digit (9th position) is correct","ForwardCollisionWarning":"","FuelInjectionType":"","FuelTankMaterial":"","FuelTankType":"","FuelTypePrimary":"Gasoline","FuelTypeSecondary":"","GCWR":"","GCWR_to":"","GVWR":"Class 1C: 4,001 - 5,000 lb (1,814 - 2,268 kg)","GVWR_to":"Class 1: 6,000 lb or less (2,722 kg or less)","KeylessIgnition":"","LaneCenteringAssistance":"","LaneDepartureWarning":"","LaneKeepSystem":"","LowerBeamHeadlampLightSource":"","Make":"HONDA","MakeID":"474","Manufacturer":"AMERICAN HONDA MOTOR CO., INC.","ManufacturerId":"988","Model":"Accord","ModelID":"1861","ModelYear":"2003","MotorcycleChassisType":"Not Applicable","MotorcycleSuspensionType":"Not Applicable","NCSABodyType":"","NCSAMake":"","NCSAMapExcApprovedBy":"","NCSAMapExcApprovedOn":"","NCSAMappingException":"","NCSAModel":"","NCSANote":"","NonLandUse":"","Note":"","OtherBusInfo":"","OtherEngineInfo":"","OtherMotorcycleInfo":"","OtherRestraintSystemInfo":"Seat Belt (Rr center position)","OtherTrailerInfo":"","ParkAssist":"","PedestrianAutomaticEmergencyBraking":"","PlantCity":"MARYSVILLE","PlantCompanyName":"","PlantCountry":"UNITED STATES (USA)","PlantState":"OHIO","PossibleValues":"","Pretensioner":"","RearAutomaticEmergencyBraking":"","RearCrossTrafficAlert":"","RearVisibilitySystem":"","SAEAutomationLevel":"","SAEAutomationLevel_to":"","SeatBeltsAll":"Manual","SeatRows":"","Seats":"","SemiautomaticHeadlampBeamSwitching":"","Series":"","Series2":"","SteeringLocation":"","SuggestedVIN":"","TPMS":"","TopSpeedMPH":"","TrackWidth":"","TractionControl":"","TrailerBodyType":"Not Applicable","TrailerLength":"","TrailerType":"Not Applicable","TransmissionSpeeds":"5","TransmissionStyle":"Automatic","Trim":"EX-V6","Trim2":"","Turbo":"","VIN":"1HGCM82633A004352","ValveTrainDesign":"Single Overhead Cam (SOHC)","VehicleDescriptor":"1HGCM826*3A","VehicleType":"PASSENGER CAR","WheelBaseLong":"","WheelBaseShort":"","WheelBaseType":"","WheelSizeFront":"","WheelSizeRear":"","WheelieMitigation":"","Wheels":"","Windows":""}},"errorCode":null,"errorMessage":null},{"index":1,"submittedVin":"bad","normalizedVin":null,"status":"INVALID_VIN","decoded":null,"errorCode":"INVALID_VIN","errorMessage":"VIN must be 17 valid VIN characters."}]},"requestId":null,"success":true}
```

### 12. Batch error entries publish the same code and message as before

```text
HTTP 200 
X-Request-Id: 4e33405a-56a9-4ebc-ae6d-1dc8a7248324
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558606
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
Date: Fri, 09 Oct 2026 15:09:06 GMT
Connection: close

{"messages":null,"payload":{"submittedCount":1,"successCount":0,"errorCount":1,"results":[{"index":0,"submittedVin":"bad","normalizedVin":null,"status":"INVALID_VIN","decoded":null,"errorCode":"INVALID_VIN","errorMessage":"VIN must be 17 valid VIN characters."}]},"requestId":null,"success":true}
```

### 13. Batch decode of a VIN with I, O or Q is INVALID_VIN

```text
HTTP 200 
X-Request-Id: 7879b661-b24b-47fb-8d94-0696a8813c16
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1791558607
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
Date: Fri, 09 Oct 2026 15:09:07 GMT
Connection: close

{"messages":null,"payload":{"submittedCount":1,"successCount":0,"errorCount":1,"results":[{"index":0,"submittedVin":"1HGCM82633A00435O","normalizedVin":null,"status":"INVALID_VIN","decoded":null,"errorCode":"INVALID_VIN","errorMessage":"VIN must be 17 valid VIN characters."}]},"requestId":null,"success":true}
```

### 14. An empty batch is rejected (400)

```text
HTTP 400 
X-Request-Id: f2ee6f5a-491c-40a2-acef-12b8ef3c0091
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558607
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
Date: Fri, 09 Oct 2026 15:09:07 GMT
Connection: close

{"messages":[{"code":"INVALID_REQUEST","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

### 15. A batch over the 20-VIN limit is rejected (400)

```text
HTTP 400 
X-Request-Id: 2647ba65-c402-429d-8476-e744c58ffe8d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1791558607
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
Date: Fri, 09 Oct 2026 15:09:07 GMT
Connection: close

{"messages":[{"code":"INVALID_REQUEST","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

## Evidence
- Case 1 started 2026-10-09T10:09:02-05:00, took 31 ms, candidate `aba533f`
- Case 2 started 2026-10-09T10:09:02-05:00, took 640 ms, candidate `aba533f`
- Case 3 started 2026-10-09T10:09:03-05:00, took 609 ms, candidate `aba533f`
- Case 4 started 2026-10-09T10:09:03-05:00, took 687 ms, candidate `aba533f`
- Case 5 started 2026-10-09T10:09:04-05:00, took 77 ms, candidate `aba533f`
- Case 6 started 2026-10-09T10:09:05-05:00, took 47 ms, candidate `aba533f`
- Case 7 started 2026-10-09T10:09:05-05:00, took 47 ms, candidate `aba533f`
- Case 8 started 2026-10-09T10:09:05-05:00, took 32 ms, candidate `aba533f`
- Case 9 started 2026-10-09T10:09:05-05:00, took 45 ms, candidate `aba533f`
- Case 10 started 2026-10-09T10:09:05-05:00, took 593 ms, candidate `aba533f`
- Case 11 started 2026-10-09T10:09:06-05:00, took 61 ms, candidate `aba533f`
- Case 12 started 2026-10-09T10:09:06-05:00, took 32 ms, candidate `aba533f`
- Case 13 started 2026-10-09T10:09:07-05:00, took 46 ms, candidate `aba533f`
- Case 14 started 2026-10-09T10:09:07-05:00, took 45 ms, candidate `aba533f`
- Case 15 started 2026-10-09T10:09:07-05:00, took 47 ms, candidate `aba533f`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
