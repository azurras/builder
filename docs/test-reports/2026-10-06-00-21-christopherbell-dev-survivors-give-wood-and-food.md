# Survivors give wood and food: Test Report

## Story/Issue
User requested direct survivor interaction and selected giving wood or food.

## Branch
`codex/survivor-interactions-20261006` at candidate `05ca114`

## Pass / Fail

> [!TIP]
> 7 of 7 cases passed on candidate `05ca114`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Final gift candidate identity | ✅ PASS | Expected status below 400 and body containing '05ca1149' |
| 2 | Final candidate two-survivor wood and food giving | ✅ PASS | Expected exit code 0 |
| 3 | Final browser gift reaches independent recipient session | ✅ PASS | Expected exit code 0 |
| 4 | Recipient departs by replacing their own survivor | ✅ PASS | Expected exit code 0 |
| 5 | Final browser mobile focus and departed-recipient safety | ✅ PASS | Expected exit code 0 |
| 6 | Final candidate readiness | ✅ PASS | Expected status below 400 and body containing 'UP' |
| 7 | Final candidate isolation and process cleanup | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Final gift candidate identity**: http `GET http://127.0.0.1:57284/actuator/info`
2. **Final candidate two-survivor wood and food giving**: command `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-api.py http://127.0.0.1:57284 C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies`
3. **Final browser gift reaches independent recipient session**: command `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-receiver.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies`
4. **Recipient departs by replacing their own survivor**: command `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-departure.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies`
5. **Final browser mobile focus and departed-recipient safety**: command `python -c "import json,os; from pathlib import Path; t=Path(os.environ['TEMP']); focus=json.loads((t/'survivor-gifts-browser.json').read_text()); departed=json.loads((t/'survivor-gifts-departure.json').read_text()); assert focus['focus']=='surviveGiftQuantity' and not focus['disabled'] and focus['width']<=focus['viewport']; assert departed['recipient']=='' and departed['giveDisabled'] and departed['amount']=='2'; print(focus); print(departed)"`
6. **Final candidate readiness**: http `GET http://127.0.0.1:57284/actuator/health/readiness`
7. **Final candidate isolation and process cleanup**: command `powershell -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-cleanup.ps1`

## App / Environment

| Setting | Value |
|---|---|
| Application | http://127.0.0.1:57284 |
| MongoDB | mongodb://127.0.0.1:57280/test |

## Automated checks and review



Full `gradlew.bat :website:check :website:bootJar` passed in 4m 59s: 1,998 Java tests passed, 110 skipped, no failures/errors; Pester and architecture checks passed. Final `:website:jsTest` passed all 389 tests after the polling fix. `node --check` on survive.js and lib/api.js, and git diff --check passed. Independent semantic review found gift-field focus interruption on background reads; fixed with red-then-green delayed-read regression, and reviewer confirmed no remaining blockers. The committed jar was rebuilt after commit to include build identity 05ca1149.



## Resource isolation and browser proof



Launched fresh MongoDB bound only to 127.0.0.1:57280 using an owned temporary db directory. Before app startup read-only ping=1, database=test and collections=[]; no direct fixture writes. App launched hidden with `SPRING_PROFILES_ACTIVE=test`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:57280/test`, `APP_MAIL_ENABLED=false`, temporary random JWT secret, and short socket JAVA_TOOL_OPTIONS. Command: `java -jar website/build/libs/website.jar --server.address=127.0.0.1 --server.port=57284`. Actual app PID 81028 connections after startup targeted MongoDB 57280; read-only db.getName() confirmed test. Startup output/error and Mongo logs are retained in the temporary evidence directory.



Actual API sessions Gift Alice, Gift Bob and Gift Charlie joined through the application. Alice gathered four wood, gave two WOOD to Bob's public ID, then earned food by combat and gave one FOOD; Bob received exactly those amounts and Charlie remained unaffected. Both revisions and messages changed, and the public journal recorded the gift. No-CSRF returned 403, stale sender returned 409, invalid quantities/resource, unavailable supply, self-gift and full recipient returned 400, replaced recipient returned 404. All failed gifts conserved supplies.



Actual browser Gift Browser gathered two wood, chose Gift Bob replacement and gave one WOOD with Enter from Amount. Sender then showed one wood and the gift narrative/journal; an independent cookie session confirmed receiver wood=1 and message 'Gift Browser gave you 1 wood.' At mobile 390x844, amount remained focused/enabled/value=2 and recipient unchanged across the five-second polling period; document width=375, viewport=390. Screenshots retained as temporary survivor-gifts-desktop.png and survivor-gifts-mobile.png. Viewport reset and owned tab closed. Owned processes stopped with identity checks; ports closed, only the verified stopped session's db directory removed. Evidence/logs retained.



Final UI safety review identified silent retargeting when the chosen recipient disappeared. Fixed by requiring an explicit recipient selection and retaining an empty choice across later polls; independent reviewer verified no remaining blockers. Repeated actual API and browser proof on the new committed jar. Recipient owner replaced their survivor; browser refreshed twice, retained WOOD/amount=2, displayed Choose a survivor with Give disabled, and Enter did not send a gift or change sender wood=1. Browser error console was empty. Native Java code is unchanged by this UI-only correction; all 389 final JS tests and committed bootJar passed.

## Local Run Details
- **Local command:** `GET http://127.0.0.1:57284/actuator/info` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-api.py http://127.0.0.1:57284 C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-receiver.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-departure.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `python -c "import json,os; from pathlib import Path; t=Path(os.environ['TEMP']); focus=json.loads((t/'survivor-gifts-browser.json').read_text()); departed=json.loads((t/'survivor-gifts-departure.json').read_text()); assert focus['focus']=='surviveGiftQuantity' and not focus['disabled'] and focus['width']<=focus['viewport']; assert departed['recipient']=='' and departed['giveDisabled'] and departed['amount']=='2'; print(focus); print(departed)"` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `GET http://127.0.0.1:57284/actuator/health/readiness` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Local command:** `powershell -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-cleanup.ps1` in `A:\Projects\christopherbell.dev.worktrees\survivor-interactions`
- **Candidate identity:** `05ca114`
- **Cleanup:** Owned processes stopped, ports closed, verified disposable database directory removed; logs and screenshots retained.

## Data Sent

### 1. Final gift candidate identity

```http
GET http://127.0.0.1:57284/actuator/info
```

### 2. Final candidate two-survivor wood and food giving

```text
python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-api.py http://127.0.0.1:57284 C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies
```

### 3. Final browser gift reaches independent recipient session

```text
python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-receiver.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies
```

### 4. Recipient departs by replacing their own survivor

```text
python C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-departure.py C:\Users\CHRIST~1\AppData\Local\Temp\survivor-gifts-996d22e10f6f46febf34628e795b2112\recipient.cookies
```

### 5. Final browser mobile focus and departed-recipient safety

```text
python -c "import json,os; from pathlib import Path; t=Path(os.environ['TEMP']); focus=json.loads((t/'survivor-gifts-browser.json').read_text()); departed=json.loads((t/'survivor-gifts-departure.json').read_text()); assert focus['focus']=='surviveGiftQuantity' and not focus['disabled'] and focus['width']<=focus['viewport']; assert departed['recipient']=='' and departed['giveDisabled'] and departed['amount']=='2'; print(focus); print(departed)"
```

### 6. Final candidate readiness

```http
GET http://127.0.0.1:57284/actuator/health/readiness
```

### 7. Final candidate isolation and process cleanup

```text
powershell -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp/survivor-gifts-cleanup.ps1
```

## Response Received

### 1. Final gift candidate identity

```text
HTTP 200 
X-Request-Id: 9eb5cfc7-8d9e-40d4-a179-7bb3f0d37c9d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791264449
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
Date: Tue, 06 Oct 2026 05:26:29 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-10-06T05:25:30.463Z","version":"0.0.0-dev.05ca1149b0a31df08533f5e86561257ae8de84ed","group":"christopherbell.dev"}}
```

### 2. Final candidate two-survivor wood and food giving

```text
exit code: 0
--- stdout ---
PASS cookie-independent public IDs, targeted wood transfer, both revisions/messages, journal, CSRF403/stale409
PASS malformed/unavailable/self/full-inventory400; rejection conserves supplies
PASS actual hunt/combat-earned food transferred into recipient inventory
PASS replaced recipient404, no inventory change
ALL PASS: gifts only through app endpoints; no direct DB writes
```

### 3. Final browser gift reaches independent recipient session

```text
exit code: 0
--- stdout ---
PASS separate recipient session: Gift Bob replacement wood 1 revision 1 message Gift Browser gave you 1 wood.
```

### 4. Recipient departs by replacing their own survivor

```text
exit code: 0
--- stdout ---
PASS recipient owner replaced their survivor; old public ID is no longer eligible
```

### 5. Final browser mobile focus and departed-recipient safety

```text
exit code: 0
--- stdout ---
{'amount': '2', 'disabled': False, 'focus': 'surviveGiftQuantity', 'message': 'You gave 1 wood to Gift Bob replacement.', 'recipient': 'Gift Bob replacement · a2488460', 'viewport': 390, 'width': 375}
{'amount': '2', 'giveDisabled': True, 'recipient': '', 'resource': 'WOOD', 'wood': '1'}
```

### 6. Final candidate readiness

```text
HTTP 200 
X-Request-Id: c97a4c6e-70cc-4183-8003-93641cc80a5a
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791264524
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
Date: Tue, 06 Oct 2026 05:27:44 GMT
Connection: close

{"status":"UP"}
```

### 7. Final candidate isolation and process cleanup

```text
exit code: 0
--- stdout ---
{"database":"test","ping":1}

RemoteAddress RemotePort OwningProcess
------------- ---------- -------------
127.0.0.1          57280         81028
127.0.0.1          57280         81028
127.0.0.1          57280         81028
127.0.0.1          57280         81028


PASS: owned Java and MongoDB stopped; verification ports closed. Logs and evidence retained.
```

## Evidence
- Case 1 started 2026-10-06T00:26:29-05:00, took 156 ms, candidate `05ca114`
- Case 2 started 2026-10-06T00:26:29-05:00, took 937 ms, candidate `05ca114`
- Case 3 started 2026-10-06T00:26:56-05:00, took 156 ms, candidate `05ca114`
- Case 4 started 2026-10-06T00:27:18-05:00, took 139 ms, candidate `05ca114`
- Case 5 started 2026-10-06T00:27:43-05:00, took 30 ms, candidate `05ca114`
- Case 6 started 2026-10-06T00:27:44-05:00, took 62 ms, candidate `05ca114`
- Case 7 started 2026-10-06T00:27:44-05:00, took 1796 ms, candidate `05ca114`

## Bugs / Follow-ups
Supersedes candidate 2b594f75 on the same date because the final UI review required explicit recipient reselection after departure. All affected runtime proof repeated on 05ca1149; no unresolved blockers.

## Document Status
complete

## Project
christopherbell-dev
