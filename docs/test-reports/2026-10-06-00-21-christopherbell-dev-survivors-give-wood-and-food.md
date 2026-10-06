# Survivors give wood and food: Test Report

## Story/Issue
User requested direct survivor interaction and selected giving wood or food.

## Branch
`codex/survivor-interactions-20261006` at candidate `2b594f7`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `2b594f7`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Committed gift candidate identity | ✅ PASS | Expected status below 400 and body containing '2b594f75' |
| 2 | Candidate readiness UP | ✅ PASS | Expected status below 400 and body containing 'UP' |
| 3 | Two survivors give wood and food through the Java API | ✅ PASS | Expected exit code 0 |
| 4 | Browser gift received by independent survivor session | ✅ PASS | Expected exit code 0 |
| 5 | Candidate target isolation and owned process cleanup | ✅ PASS | Expected exit code 0 |
| 6 | Actual browser keyboard transfer and mobile polling focus | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Committed gift candidate identity**: http `GET http://127.0.0.1:57284/actuator/info`
2. **Candidate readiness UP**: http `GET http://127.0.0.1:57284/actuator/health/readiness`
3. **Two survivors give wood and food through the Java API**: command `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-api.py http://127.0.0.1:57284 C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies`
4. **Browser gift received by independent survivor session**: command `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-receiver.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies`
5. **Candidate target isolation and owned process cleanup**: command `powershell -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-cleanup.ps1`
6. **Actual browser keyboard transfer and mobile polling focus**: command `python -c "import json,os; from pathlib import Path; p=Path(os.environ['TEMP'])/'survivor-gifts-browser.json'; observed=json.loads(p.read_text()); assert observed['focus']=='surviveGiftQuantity' and not observed['disabled'] and observed['width']<=observed['viewport']; print(observed)"`

## App / Environment

| Setting | Value |
|---|---|
| Application | http://127.0.0.1:57284 |
| MongoDB | mongodb://127.0.0.1:57280/test |

## Automated checks and review

Full `gradlew.bat :website:check :website:bootJar` passed in 4m 59s: 1,998 Java tests passed, 110 skipped, no failures/errors; Pester and architecture checks passed. Final `:website:jsTest` passed all 388 tests after the polling fix. `node --check` on survive.js and lib/api.js, and git diff --check passed. Independent semantic review found gift-field focus interruption on background reads; fixed with red-then-green delayed-read regression, and reviewer confirmed no remaining blockers. The committed jar was rebuilt after commit to include build identity 2b594f75.

## Resource isolation and browser proof

Launched fresh MongoDB bound only to 127.0.0.1:57280 using an owned temporary db directory. Before app startup read-only ping=1, database=test and collections=[]; no direct fixture writes. App launched hidden with `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:57280/test`, `APP_MAIL_ENABLED=false`, temporary random JWT secret, and short socket JAVA_TOOL_OPTIONS. Command: `java -jar website/build/libs/website.jar --server.address=127.0.0.1 --server.port=57284`. Actual app PID 14292 connections after startup targeted MongoDB 57280; read-only db.getName() confirmed test. Startup output/error and Mongo logs are retained in the temporary evidence directory.

Actual API sessions Gift Alice, Gift Bob and Gift Charlie joined through the application. Alice gathered four wood, gave two WOOD to Bob's public ID, then earned food by combat and gave one FOOD; Bob received exactly those amounts and Charlie remained unaffected. Both revisions and messages changed, and the public journal recorded the gift. No-CSRF returned 403, stale sender returned 409, invalid quantities/resource, unavailable supply, self-gift and full recipient returned 400, replaced recipient returned 404. All failed gifts conserved supplies.

Actual browser Gift Browser gathered two wood, chose Gift Bob replacement and gave one WOOD with Enter from Amount. Sender then showed one wood and the gift narrative/journal; an independent cookie session confirmed receiver wood=1 and message 'Gift Browser gave you 1 wood.' At mobile 390x844, amount remained focused/enabled/value=1 and recipient unchanged across the five-second polling period; document width=375, viewport=390. Screenshots retained as temporary survivor-gifts-desktop.png and survivor-gifts-mobile.png. Viewport reset and owned tab closed. Owned processes stopped with identity checks; ports closed, only the verified stopped session's db directory removed. Evidence/logs retained.

## Local Run Details
- **Local command:** `GET http://127.0.0.1:57284/actuator/info` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `GET http://127.0.0.1:57284/actuator/health/readiness` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-api.py http://127.0.0.1:57284 C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-receiver.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `powershell -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-cleanup.ps1` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python -c "import json,os; from pathlib import Path; p=Path(os.environ['TEMP'])/'survivor-gifts-browser.json'; observed=json.loads(p.read_text()); assert observed['focus']=='surviveGiftQuantity' and not observed['disabled'] and observed['width']<=observed['viewport']; print(observed)"` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Candidate identity:** `2b594f7`
- **Cleanup:** Owned Java and MongoDB stopped; ports closed; session-owned disposable database directory removed; logs and screenshots retained.

## Data Sent

### 1. Committed gift candidate identity

```http
GET http://127.0.0.1:57284/actuator/info
```

### 2. Candidate readiness UP

```http
GET http://127.0.0.1:57284/actuator/health/readiness
```

### 3. Two survivors give wood and food through the Java API

```text
python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-api.py http://127.0.0.1:57284 C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies
```

### 4. Browser gift received by independent survivor session

```text
python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-receiver.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies
```

### 5. Candidate target isolation and owned process cleanup

```text
powershell -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-cleanup.ps1
```

### 6. Actual browser keyboard transfer and mobile polling focus

```text
python -c "import json,os; from pathlib import Path; p=Path(os.environ['TEMP'])/'survivor-gifts-browser.json'; observed=json.loads(p.read_text()); assert observed['focus']=='surviveGiftQuantity' and not observed['disabled'] and observed['width']<=observed['viewport']; print(observed)"
```

## Response Received

### 1. Committed gift candidate identity

```text
HTTP 200 
X-Request-Id: 0ba3d93f-2316-4be8-b816-3151f0eea63e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791263975
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
Content-Length: 176
Date: Tue, 06 Oct 2026 05:18:35 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-10-06T05:18:07.081Z","version":"0.0.0-dev.2b594f75ce796dd01a02c2e2041a59517f939e44","group":"christopherbell.dev"}}
```

### 2. Candidate readiness UP

```text
HTTP 200 
X-Request-Id: ac29dc31-2440-4cc9-a784-58f8b1c1b6da
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791263975
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
Date: Tue, 06 Oct 2026 05:18:35 GMT
Connection: close

{"status":"UP"}
```

### 3. Two survivors give wood and food through the Java API

```text
exit code: 0
--- stdout ---
PASS cookie-independent public IDs, targeted wood transfer, both revisions/messages, journal, CSRF403/stale409
PASS malformed/unavailable/self/full-inventory400; rejection conserves supplies
PASS actual hunt/combat-earned food transferred into recipient inventory
PASS replaced recipient404, no inventory change
ALL PASS: gifts only through app endpoints; no direct DB writes
```

### 4. Browser gift received by independent survivor session

```text
exit code: 0
--- stdout ---
PASS separate recipient session: Gift Bob replacement wood 1 revision 1 message Gift Browser gave you 1 wood.
```

### 5. Candidate target isolation and owned process cleanup

```text
exit code: 0
--- stdout ---
{"database":"test","ping":1}

RemoteAddress RemotePort OwningProcess
------------- ---------- -------------
127.0.0.1          57280         14292
127.0.0.1          57280         14292
127.0.0.1          57280         14292
127.0.0.1          57280         14292


PASS: owned Java and MongoDB stopped; verification ports closed. Logs and evidence retained.
```

### 6. Actual browser keyboard transfer and mobile polling focus

```text
exit code: 0
--- stdout ---
{'amount': '1', 'disabled': False, 'focus': 'surviveGiftQuantity', 'message': 'You gave 1 wood to Gift Bob replacement.', 'recipient': 'Gift Bob replacement · 9c7a8bd6', 'viewport': 390, 'width': 375}
```

## Evidence
- Case 1 started 2026-10-06T00:18:35-05:00, took 157 ms, candidate `2b594f7`
- Case 2 started 2026-10-06T00:18:35-05:00, took 46 ms, candidate `2b594f7`
- Case 3 started 2026-10-06T00:18:35-05:00, took 952 ms, candidate `2b594f7`
- Case 4 started 2026-10-06T00:19:42-05:00, took 156 ms, candidate `2b594f7`
- Case 5 started 2026-10-06T00:20:30-05:00, took 1750 ms, candidate `2b594f7`
- Case 6 started 2026-10-06T00:20:32-05:00, took 47 ms, candidate `2b594f7`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
