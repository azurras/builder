# Survive clock danger weapons sleep and hunger: Test Report

## Story/Issue
User request 2026-10-16: time, enemies, weapons, building weapons, shelter sleep and hunger for Survive; plan docs/implementation-plans/2026-10-16-14-42-christopherbell-dev-survive-clock-danger-weapons-sleep-and-hunger.md

## Branch
`claude/survive-clock-danger-weapons-20261016` at candidate `0a3d242`

## Pass / Fail

> [!TIP]
> 17 of 17 cases passed on candidate `0a3d242`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate is ready and reports its build | ✅ PASS | Expected status below 400 and body containing '"build"' |
| 2 | Candidate opened only the disposable test database | ✅ PASS | Expected exit code 0 |
| 3 | Survive page serves the clock, hunger, stone, weapon and new actions | ✅ PASS | Expected status below 400 and body containing 'data-action="CRAFT_SPEAR"' |
| 4 | Survive script ships the countdown and sleep controls | ✅ PASS | Expected status below 400 and body containing 'export function formatCountdown' |
| 5 | Survive API: snapshot | ✅ PASS | Expected exit code 0 |
| 6 | Survive API: day-rejects-night-actions | ✅ PASS | Expected exit code 0 |
| 7 | Survive API: stone-and-weapons | ✅ PASS | Expected exit code 0 |
| 8 | Survive API: hunt-and-eat | ✅ PASS | Expected exit code 0 |
| 9 | Survive API: gift-stone | ✅ PASS | Expected exit code 0 |
| 10 | Read-only query: the candidate wrote the survive world only to database test on the disposable mongod | ✅ PASS | Expected exit code 0 |
| 11 | Survive API: dusk-preparations | ✅ PASS | Expected exit code 0 |
| 12 | Survive API: after-nightfall | ✅ PASS | Expected exit code 0 |
| 13 | Survive API: after-dawn | ✅ PASS | Expected exit code 0 |
| 14 | Survive API: daytime-wood-for-shelter | ✅ PASS | Expected exit code 0 |
| 15 | Survive API: sleep-after-nightfall | ✅ PASS | Expected exit code 0 |
| 16 | Survive API: wake-early | ✅ PASS | Expected exit code 0 |
| 17 | Survive API: dawn-after-sleep | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate is ready and reports its build**: http `GET http://127.0.0.1:62452/actuator/info`
2. **Candidate opened only the disposable test database**: command `powershell -NoProfile -Command "Select-String -Path 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-fcf8cf3bcc0a419fa23d1e49be219c04\candidate.out.log' -Pattern 'mongodb://|database|profile' | Select-Object -First 6 | ForEach-Object { $_.Line }"`
3. **Survive page serves the clock, hunger, stone, weapon and new actions**: http `GET http://127.0.0.1:62452/survive`
4. **Survive script ships the countdown and sleep controls**: http `GET http://127.0.0.1:62452/js/survive.js`
5. **Survive API: snapshot**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json snapshot`
6. **Survive API: day-rejects-night-actions**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json day-rejects-night-actions`
7. **Survive API: stone-and-weapons**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json stone-and-weapons`
8. **Survive API: hunt-and-eat**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json hunt-and-eat`
9. **Survive API: gift-stone**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json gift-stone`
10. **Read-only query: the candidate wrote the survive world only to database test on the disposable mongod**: command `mongosh --quiet --port 62451 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name), surviveWorlds: db.getSiblingDB('test').application_runtime.countDocuments({_kind: 'survive_world'})})"`
11. **Survive API: dusk-preparations**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json dusk-preparations`
12. **Survive API: after-nightfall**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json after-nightfall`
13. **Survive API: after-dawn**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json after-dawn`
14. **Survive API: daytime-wood-for-shelter**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json daytime-wood-for-shelter`
15. **Survive API: sleep-after-nightfall**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json sleep-after-nightfall`
16. **Survive API: wake-early**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json wake-early`
17. **Survive API: dawn-after-sleep**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json dawn-after-sleep`

## Automated Checks
- `.\ops\local\Invoke-Gradle.ps1 :website:build :website:bootJar` on `0a3d242`: BUILD SUCCESSFUL, 2,164 tests, 0 failed, 110 skipped, Checkstyle clean; the JavaScript suite (`survive.test.js`) passed 11 of 11.
- The new `escapingWhileOnGuardLeavesASaveableSurvivor` test failed (`guarding` stayed `true`) on the previous full build, before the escape fix, and passes on `0a3d242`.

## Browser Check
In the desktop app's browser pane, the candidate's `/survive` page joined a guest named Tester and rendered the clock banner (`Day 39`, `Dusk in 13:12`, phase `DAY`), fullness `10 / 10`, `Bare hands`, beds `0 / 0` and the new action buttons, with guard and sleep shown but disabled by day. The countdown ticked locally (`13:07` to `13:05` across a 3-second wait). Clicking **Gather stone** returned "You gathered one stone." with fullness `9 / 10` and inventory `1 / 10`. The console logged no errors.

## Cycle Timing
Phase cases ran against the real wall clock on 2026-10-16 UTC: dusk preparations at 20:26:21, the first nightfall check at 20:30:24 and dawn at 20:36:22; the second cycle slept after nightfall at 20:54:23, woke Alice early at 20:58:40 and read the dawn at 21:00:22. On the first night a raid of strength 10 overran Alice's defense of 8, burned the only shelter and woke Bob with 2 damage, so the second cycle proved sleep healing and the full dawn wake.

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a disposable loopback mongod (port 62451), removed after the run |
| Candidate | website.jar built from the committed HEAD, http://127.0.0.1:62452 |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:62452/actuator/info` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `powershell -NoProfile -Command "Select-String -Path 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-fcf8cf3bcc0a419fa23d1e49be219c04\candidate.out.log' -Pattern 'mongodb://|database|profile' | Select-Object -First 6 | ForEach-Object { $_.Line }"` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `GET http://127.0.0.1:62452/survive` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `GET http://127.0.0.1:62452/js/survive.js` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json snapshot` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json day-rejects-night-actions` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json stone-and-weapons` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json hunt-and-eat` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json gift-stone` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `mongosh --quiet --port 62451 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name), surviveWorlds: db.getSiblingDB('test').application_runtime.countDocuments({_kind: 'survive_world'})})"` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json dusk-preparations` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json after-nightfall` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json after-dawn` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json daytime-wood-for-shelter` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json sleep-after-nightfall` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json wake-early` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json dawn-after-sleep` in `A:\Projects\christopherbell.dev.worktrees\survive-clock`
- **Candidate identity:** `0a3d242`
- **Cleanup:** Stopped the candidate process tree; no fixtures remain.

## Data Sent

### 1. Candidate is ready and reports its build

```http
GET http://127.0.0.1:62452/actuator/info
```

### 2. Candidate opened only the disposable test database

```text
powershell -NoProfile -Command "Select-String -Path 'C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-fcf8cf3bcc0a419fa23d1e49be219c04\candidate.out.log' -Pattern 'mongodb://|database|profile' | Select-Object -First 6 | ForEach-Object { $_.Line }"
```

### 3. Survive page serves the clock, hunger, stone, weapon and new actions

```http
GET http://127.0.0.1:62452/survive
```

### 4. Survive script ships the countdown and sleep controls

```http
GET http://127.0.0.1:62452/js/survive.js
```

### 5. Survive API: snapshot

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json snapshot
```

### 6. Survive API: day-rejects-night-actions

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json day-rejects-night-actions
```

### 7. Survive API: stone-and-weapons

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json stone-and-weapons
```

### 8. Survive API: hunt-and-eat

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json hunt-and-eat
```

### 9. Survive API: gift-stone

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json gift-stone
```

### 10. Read-only query: the candidate wrote the survive world only to database test on the disposable mongod

```text
mongosh --quiet --port 62451 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name), surviveWorlds: db.getSiblingDB('test').application_runtime.countDocuments({_kind: 'survive_world'})})"
```

### 11. Survive API: dusk-preparations

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json dusk-preparations
```

### 12. Survive API: after-nightfall

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json after-nightfall
```

### 13. Survive API: after-dawn

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json after-dawn
```

### 14. Survive API: daytime-wood-for-shelter

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json daytime-wood-for-shelter
```

### 15. Survive API: sleep-after-nightfall

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json sleep-after-nightfall
```

### 16. Survive API: wake-early

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json wake-early
```

### 17. Survive API: dawn-after-sleep

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/candidate.json dawn-after-sleep
```

## Response Received

### 1. Candidate is ready and reports its build

```text
HTTP 200 
X-Request-Id: 5a998d25-d127-4397-890b-a5918c7bf819
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792181597
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
Date: Fri, 16 Oct 2026 20:12:17 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-10-16T20:05:07.191Z","version":"0.0.0-dev.0a3d24289b4beb02c28f7d3e8cc60c17fd7d514b","group":"christopherbell.dev"}}
```

### 2. Candidate opened only the disposable test database

```text
exit code: 0
--- stdout ---
2026-10-16T15:10:44.272-05:00  INFO 36892 --- [           main] [] dev.christopherbell.Application          : The following 1 profile is active: "test"
```

### 3. Survive page serves the clock, hunger, stone, weapon and new actions

<details><summary>167 lines</summary>

```text
HTTP 200 
X-Request-Id: 981b3fde-aa26-4cc7-9c8a-ef281507a878
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792181598
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/html;charset=UTF-8
Content-Language: en-US
Transfer-Encoding: chunked
Date: Fri, 16 Oct 2026 20:12:18 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  
    <meta name="description" content="Gather, craft, and survive in a shared text adventure world." />
    
    <link rel="canonical" href="https://www.christopherbell.dev/survive" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | Survive" />
    <meta property="og:description" content="Gather, craft, and survive in a shared text adventure world." />
    <meta property="og:url" content="https://www.christopherbell.dev/survive" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Survive on christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | Survive" />
    <meta name="twitter:description" content="Gather, craft, and survive in a shared text adventure world." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="Survive on christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  
  <title>Survive | Christopher Bell</title>
  <link rel="stylesheet" href="/110bc58f54a50ffd1dd8/css/main.css" />
  <link rel="stylesheet" href="/110bc58f54a50ffd1dd8/css/survive.css" />
</head>
<body class="site-page void-shell-page survive-page">
  <div id="nav"></div>
  <main class="site-main survive-main">
    <header class="survive-hero">
      <p class="survive-eyebrow">A shared world · A text adventure</p>
      <h1>Survive<span aria-hidden="true">.</span></h1>
      <p>The wilderness is unforgiving. You don't have to face it alone.</p>
      <div class="survive-intro"><span aria-hidden="true">↟</span> Gather wood and stone. Build a camp. Survive the nights. Find your way out.</div>
    </header>

    <noscript><p class="survive-notice">Enable JavaScript for the controls. All gameplay runs on the Java server.</p></noscript>
    <p id="surviveError" class="survive-notice" role="alert" hidden></p>
    <form id="surviveJoin" class="survive-panel survive-join">
      <div><h2 id="surviveJoinTitle">Enter the wilderness</h2><p>Your survivor is yours. The camp belongs to everyone. Log in for one saved character, or play as a temporary guest.</p></div>
      <label for="surviveName">Survivor name</label>
      <input id="surviveName" name="name" required maxlength="32" autocomplete="nickname" value="Chris" />
      <button type="submit" class="survive-primary">Join camp</button>
      <button id="surviveCancel" type="button" hidden>Keep current survivor</button>
    </form>

    <div id="surviveGame" class="survive-grid" hidden>
      <section class="survive-panel survive-adventure" aria-labelledby="surviveScene">
        <div class="survive-section-heading"><p class="survive-eyebrow">Your adventure</p><span id="surviveStatus" class="survive-badge"></span></div>
        <div id="surviveClock" class="survive-clock" data-phase="DAY" role="group" aria-label="World time">
          <strong id="survivePhase">Day</strong><span id="surviveDay"></span>
          <span class="survive-countdown"><span id="surviveNextPhase">Dusk in</span> <strong id="surviveCountdown"></strong></span>
        </div>
        <h2 id="surviveScene">At the edge of the wilderness</h2>
        <p id="surviveMessage" class="survive-message" role="status" aria-live="polite" aria-atomic="true"></p>
        <div id="surviveEnemy" class="survive-enemy" hidden><strong id="surviveEnemyName">Wild hog</strong><span id="surviveEnemyHealth"></span></div>
        <p class="survive-eyebrow">Choose your next move</p>
        <div id="surviveActions" class="survive-actions">
          <button type="button" data-action="GATHER">Gather wood <small>50% chance · +1 wood</small></button>
          <button type="button" data-action="GATHER_STONE">Gather stone <small>40% chance · +1 stone</small></button>
          <button type="button" data-action="HUNT">Hunt <small>Hogs by day · Wolves and bears after dark</small></button>
          <button type="button" data-action="BUILD_SHELTER">Build shelter <small>5 wood · Two beds for the camp</small></button>
          <button type="button" data-action="BUILD_BOAT">Build boat <small>10 wood · One escape</small></button>
          <button type="button" data-action="CRAFT_CLUB">Craft club <small>2 wood · +1 damage · 8 uses</small></button>
          <button type="button" data-action="CRAFT_AXE">Craft stone axe <small>2 wood, 2 stone · +2 damage · Better wood gathering</small></button>
          <button type="button" data-action="CRAFT_SPEAR">Craft spear <small>3 wood, 3 stone · +3 damage · Reach</small></button>
          <button type="button" data-action="EAT">Eat food <small>1 food · +5 fullness, +2 health</small></button>
          <button type="button" data-action="REST">Rest <small>Requires shelter · +2 health</small></button>
          <button type="button" data-action="GUARD">Stand guard <small>Dusk only · Defend the camp from tonight's raid</small></button>
          <button type="button" data-action="SLEEP">Sleep <small>Dusk or night · Uses a shelter bed · Heal through the night</small></button>
          <button type="button" data-action="WAKE">Wake up <small>Keep the health you have recovered so far</small></button>
          <button type="button" data-action="ESCAPE">Sail away <small>Use a shared boat · Survive</small></button>
          <button type="button" data-action="ATTACK">Attack <small>Strike with your weapon · The animal bites back</small></button>
          <button type="button" data-action="DEFEND">Defend <small>Block the next bite</small></button>
          <button type="button" data-action="FLEE">Flee <small>Return to camp · Take one bite</small></button>
        </div>
        <div class="survive-secondary"><button id="surviveRefresh" type="button">Refresh world</button><button id="surviveRestart" type="button">New survivor</button></div>
      </section>

      <aside class="survive-sidebar" aria-label="Survivor and camp">
        <section class="survive-panel" aria-labelledby="survivePlayerName">
          <p class="survive-eyebrow">Your survivor</p><h2 id="survivePlayerName"></h2>
          <p id="surviveSaveStatus" class="survive-muted" role="status"></p>
          <p id="survivePublicId" class="survive-muted"></p>
          <label class="survive-health-label" for="surviveHealth">Health <strong id="surviveHealthText"></strong></label>
          <meter id="surviveHealth" min="0" max="10" low="3" high="7" optimum="10" value="10"></meter>
          <label class="survive-health-label" for="surviveHunger">Fullness <strong id="surviveHungerText"></strong></label>
          <meter id="surviveHunger" min="0" max="10" low="4" high="7" optimum="10" value="10"></meter>
          <p id="surviveHungerWarning" class="survive-warning" role="status" hidden>You are hungry. Eat soon: at 0, every effort costs health.</p>
          <dl class="survive-stats"><div><dt>Strength</dt><dd id="surviveStrength"></dd></div><div><dt>Stamina</dt><dd id="surviveStamina"></dd></div><div><dt>Gathering XP</dt><dd id="surviveExperience"></dd></div></dl>
          <h3>Inventory <span id="surviveInventoryCount"></span></h3>
          <dl class="survive-stats"><div><dt>Wood</dt><dd id="surviveWood"></dd></div><div><dt>Food</dt><dd id="surviveFood"></dd></div><div><dt>Stone</dt><dd id="surviveStone"></dd></div></dl>
          <h3>Weapon</h3>
          <p id="surviveWeapon" class="survive-muted"></p>
        </section>
        <section class="survive-panel" aria-labelledby="surviveCampTitle">
          <p class="survive-eyebrow">One world, built together</p><h2 id="surviveCampTitle">Shared camp</h2>
          <dl class="survive-stats"><div><dt>Shelters</dt><dd id="surviveShelters"></dd></div><div><dt>Beds in use</dt><dd id="surviveBeds"></dd></div><div><dt>Boats</dt><dd id="surviveBoats"></dd></div></dl>
          <h3>Survivors in camp <span id="survivePlayerCount"></span></h3><ul id="survivePlayers" class="survive-players"></ul>
          <form id="surviveGift" class="survive-gift" aria-labelledby="surviveGiftTitle">
            <h3 id="surviveGiftTitle">Share supplies</h3>
            <label for="surviveRecipient">Give to</label>
            <select id="surviveRecipient" name="recipientId" required></select>
            <div class="survive-gift-amount">
              <div><label for="surviveGiftResource">Supply</label><select id="surviveGiftResource" name="resource"><option value="WOOD">Wood</option><option value="FOOD">Food</option><option value="STONE">Stone</option></select></div>
              <div><label for="surviveGiftQuantity">Amount</label><input id="surviveGiftQuantity" name="quantity" type="number" min="1" max="10" step="1" value="1" required /></div>
            </div>
            <button id="surviveGive" type="submit">Give supplies</button>
            <p id="surviveGiftHint" class="survive-muted"></p>
          </form>
          <p class="survive-muted">Camp updates every 5 seconds while this page is visible.</p>
        </section>
      </aside>
      <section class="survive-panel survive-journal" aria-labelledby="surviveJournalTitle">
        <div class="survive-section-heading"><h2 id="surviveJournalTitle">Camp journal</h2><span class="survive-eyebrow">The last 30 events</span></div>
        <ol id="surviveEvents" reversed></ol>
      </section>
    </div>

    <details class="survive-panel survive-guide"><summary>Field guide · How to play</summary>
      <p>Time is shared by the whole world: each 24-minute day has 14 minutes of daylight, 4 of dusk and 6 of night. At every nightfall raiders attack the camp. Survivors who stand guard at dusk add their attack damage to the defense; if the raiders are stronger they burn shelters and boats. Raids build through a seven-night week and then begin again. Nobody is hurt while away, but the shared camp is.</p>
      <p>Outside camp you can be ambushed: rarely by day, more often at dusk and night. Hunting finds hogs by day; after dark wolves (8 health, bite 2) and bears (14 health, bite 3) roam. Fleeing costs one bite.</p>
      <p>Gather stone (40% chance) to craft weapons. A club costs 2 wood (+1 damage, 8 uses), a stone axe 2 wood and 2 stone (+2 damage, 12 uses, wood gathering rises to 70%), a spear 3 wood and 3 stone (+3 damage, 12 uses, and its reach spares you the first bite of each fight). Each attack wears your weapon down until it breaks; crafting replaces the one you hold.</p>
      <p>Every effort outside camp, every combat move and every guard shift costs 1 fullness, and a night's sleep costs 2. Food restores 5 fullness and 2 health. At 0 fullness every effort costs 1 health and sleep does not heal.</p>
      <p>Each shelter has two beds. Sleep at dusk or night to recover 1 health for every 2 minutes asleep, or fully if you sleep until dawn. If raiders burn your shelter while you sleep, you wake with 2 damage.</p>
      <p>Share supplies chooses another survivor by name and camp ID. Give 1–10 wood, food or stone while both of you are at camp. Gifts move items directly into their inventory, which must have room; both survivors and the camp journal receive an update.</p>
      <p>Gather wood to improve strength and stamina. Your inventory holds 10 items. Five wood builds a shelter everyone can rest in; ten wood builds a boat any survivor can use to escape.</p>
      <p>Your attack deals 1 + strength + weapon damage, and the animal bites back on every attack, even the final blow. Defend blocks one bite. Defeating a hog or wolf gives 1 food and a bear up to 3, as your inventory allows. A shared shelter restores 2 health per rest.</p>
      <p>Sail away to survive, or start again after death. New survivor replaces only your character. Saved account characters can start again after death or escape; joining again resumes a living character. Shelters, boats, and other players remain in the shared world. Names and recent actions are visible to other players; use a nickname.</p>
      <p>Your logged-in account has one saved survivor. Moves, supplies, combat and the shared camp are saved after each successful command and survive server restarts. Log in again to resume. Guests use a temporary browser session and expire after two idle hours. Saved survivors keep their progress while inactive and return to the active camp when resumed. Guest progress stays separate from your account character. This version has no chat or matchmaking.</p>
    </details>
    <p class="survive-attribution">Adapted from <a href="https://github.com/azurras/survive">azurras/Survive</a> · Java game engine · <a href="/licenses/survive-MIT.txt">MIT license</a>. Browser adaptation completes the original's unfinished combat and food actions.</p>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/110bc58f54a50ffd1dd8/js/app.js"></script>
  <script type="module" src="/110bc58f54a50ffd1dd8/js/survive.js"></script>
</body>
</html>
```

</details>

### 4. Survive script ships the countdown and sleep controls

<details><summary>301 lines</summary>

```text
HTTP 200 
X-Request-Id: d605bf40-7623-4e49-a371-e496473a8aba
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792181598
Cache-Control: max-age=3600, public
Last-Modified: Fri, 16 Oct 2026 20:05:12 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 12822
Date: Fri, 16 Oct 2026 20:12:18 GMT
Connection: close

/** Display and transport only: the Java world owns all rules and allowed actions. */
import { API } from './lib/api.js';
import { fetchJson } from './lib/util.js';

const STATUS_LABELS = {
  EXPLORING: 'At camp', COMBAT: 'In combat', SLEEPING: 'Asleep', DEAD: 'Game over', ESCAPED: 'Survived',
};
const SCENE_LABELS = {
  EXPLORING: 'At the edge of the wilderness', SLEEPING: 'Asleep in a shelter bed',
  DEAD: 'The wilderness claimed you', ESCAPED: 'A new horizon awaits',
};
const COMBAT_SCENES = { HOG: 'A wild hog blocks your path', WOLF: 'A wolf circles you', BEAR: 'A bear rears up before you' };
const ENEMY_LABELS = { HOG: 'Wild hog', WOLF: 'Grey wolf', BEAR: 'Brown bear' };
const WEAPON_LABELS = { CLUB: 'Club', STONE_AXE: 'Stone axe', SPEAR: 'Spear' };
const PHASE_LABELS = { DAY: 'Day', DUSK: 'Dusk', NIGHT: 'Night' };
const NEXT_PHASE_LABELS = { DAY: 'Dusk in', DUSK: 'Nightfall in', NIGHT: 'Dawn in' };
const COMBAT_ACTIONS = ['ATTACK', 'DEFEND', 'FLEE'];
const HUNGER_WARNING_LEVEL = 3;

/** Minutes and seconds until the next phase, for example 4:05. */
export function formatCountdown(secondsLeft) {
  const wholeSeconds = Math.max(0, Math.floor(secondsLeft));
  return `${Math.floor(wholeSeconds / 60)}:${String(wholeSeconds % 60).padStart(2, '0')}`;
}

/** Each status shows only its own controls: combat moves in a fight, waking while asleep. */
function isActionShownFor(status, action) {
  if (status === 'COMBAT') {
    return COMBAT_ACTIONS.includes(action);
  }
  if (status === 'SLEEPING') {
    return action === 'WAKE';
  }
  return !COMBAT_ACTIONS.includes(action) && action !== 'WAKE';
}

/** Render server-supplied text as text nodes, including names and public journal entries. */
export function renderSurviveState(documentRoot, state, pending = false, mutationPending = pending) {
  const setText = (id, text) => { documentRoot.getElementById(id).textContent = String(text); };
  documentRoot.getElementById('surviveGame').hidden = false;
  setText('survivePlayerName', state.name);
  setText('surviveSaveStatus', state.saved
    ? 'Saved to your account - Resume when you log in again.'
    : 'Temporary guest - Log in for a separate saved survivor.');
  documentRoot.getElementById('surviveRestart').disabled = pending
    || Boolean(state.saved && !['DEAD', 'ESCAPED'].includes(state.status));
  setText('survivePublicId', `Camp ID: ${state.survivorId.slice(0, 8)}`);
  const isGuarding = state.status === 'EXPLORING' && state.guarding;
  setText('surviveStatus', isGuarding ? 'On guard' : STATUS_LABELS[state.status] || state.status);
  setText('surviveScene', state.status === 'COMBAT'
    ? COMBAT_SCENES[state.enemy] || 'Something blocks your path'
    : SCENE_LABELS[state.status] || 'The wilderness');
  documentRoot.getElementById('surviveClock').dataset.phase = state.phase;
  setText('survivePhase', PHASE_LABELS[state.phase] || state.phase);
  setText('surviveDay', `Day ${state.day}`);
  setText('surviveNextPhase', NEXT_PHASE_LABELS[state.phase] || 'Next phase in');
  setText('surviveCountdown', formatCountdown(state.secondsToNextPhase));
  const message = documentRoot.getElementById('surviveMessage');
  if (message.textContent !== state.message) {
    message.textContent = state.message;
  }
  setText('surviveHealthText', `${state.health} / 10`);
  documentRoot.getElementById('surviveHealth').value = state.health;
  setText('surviveStrength', state.strength);
  setText('surviveStamina', state.stamina);
  setText('surviveExperience', `${state.experience} / ${state.experienceToNextLevel}`);
  setText('surviveHungerText', `${state.hunger} / 10`);
  documentRoot.getElementById('surviveHunger').value = state.hunger;
  documentRoot.getElementById('surviveHungerWarning').hidden = state.hunger > HUNGER_WARNING_LEVEL;
  setText('surviveWood', state.wood);
  setText('surviveFood', state.food);
  setText('surviveStone', state.stone);
  const carried = state.wood + state.food + state.stone;
  setText('surviveInventoryCount', `${carried} / ${state.inventoryCapacity}`);
  setText('surviveWeapon', state.weapon
    ? `${WEAPON_LABELS[state.weapon] || state.weapon} · ${state.weaponDurability} uses left`
    : 'Bare hands');
  setText('surviveShelters', state.shelters);
  setText('surviveBeds', `${state.bedsInUse} / ${state.beds}`);
  setText('surviveBoats', state.boats);
  setText('survivePlayerCount', state.survivors.length);
  documentRoot.getElementById('surviveEnemy').hidden = state.status !== 'COMBAT';
  setText('surviveEnemyName', ENEMY_LABELS[state.enemy] || 'Wild animal');
  setText('surviveEnemyHealth', `${state.enemyHealth} health`);
  for (const button of documentRoot.querySelectorAll('[data-action]')) {
    button.disabled = pending || !state.actions.includes(button.dataset.action);
    button.hidden = !isActionShownFor(state.status, button.dataset.action);
  }
  for (const [id, entries] of [['survivePlayers', state.survivors], ['surviveEvents', [...state.events].reverse()]]) {
    const list = documentRoot.getElementById(id);
    const items = entries.map(text => {
      const item = documentRoot.createElement('li');
      item.textContent = text;
      return item;
    });
    list.replaceChildren(...items);
  }
  const recipientPicker = documentRoot.getElementById('surviveRecipient');
  const previousRecipient = recipientPicker.value;
  const recipientSignature = JSON.stringify(state.recipients);
  // Preserve the native chooser and input focus when a poll has no recipient changes.
  if (recipientPicker.dataset.recipientSignature !== recipientSignature) {
    const chooseRecipient = documentRoot.createElement('option');
    chooseRecipient.value = '';
    chooseRecipient.textContent = 'Choose a survivor';
    recipientPicker.replaceChildren(chooseRecipient, ...state.recipients.map(recipient => {
      const option = documentRoot.createElement('option');
      option.value = recipient.survivorId;
      option.textContent = `${recipient.name} · ${recipient.survivorId.slice(0, 8)}`;
      return option;
    }));
    recipientPicker.dataset.recipientSignature = recipientSignature;
  }
  recipientPicker.value = state.recipients.some(recipient => recipient.survivorId === previousRecipient)
    ? previousRecipient : '';
  const unavailable = !state.recipients.length || carried === 0;
  for (const id of ['surviveRecipient', 'surviveGiftResource', 'surviveGiftQuantity']) {
    documentRoot.getElementById(id).disabled = mutationPending || unavailable;
  }
  documentRoot.getElementById('surviveGive').disabled = pending || unavailable || !recipientPicker.value;
  setText('surviveGiftHint', !state.recipients.length
    ? 'You and another survivor must be at camp to share supplies.'
    : 'Give supplies to help another survivor. Their inventory must have room.');
}

/** Serialize browser requests; failed mutations are never automatically repeated. */
export function mountSurvive(documentRoot = document, requestJson = fetchJson) {
  const joinForm = documentRoot.getElementById('surviveJoin');
  if (!joinForm) {
    return null;
  }
  let state = null;
  let pending = false;
  let mutationPending = false;
  let phaseEndsAtMilliseconds = 0;
  const errorBox = documentRoot.getElementById('surviveError');
  const restart = documentRoot.getElementById('surviveRestart');
  const refresh = documentRoot.getElementById('surviveRefresh');
  const cancel = documentRoot.getElementById('surviveCancel');
  const giftForm = documentRoot.getElementById('surviveGift');

  function setPending(isPending, isMutation = false) {
    pending = isPending;
    mutationPending = isPending && isMutation;
    for (const control of joinForm.querySelectorAll('input, button')) {
      control.disabled = pending;
    }
    restart.disabled = pending;
    refresh.disabled = pending;
    if (state) {
      renderSurviveState(documentRoot, state, pending, mutationPending);
    }
  }

  function acceptState(serverState) {
    state = serverState?.name ? serverState : null;
    documentRoot.getElementById('surviveGame').hidden = !state;
    joinForm.hidden = Boolean(state);
    cancel.hidden = !state;
    if (state) {
      phaseEndsAtMilliseconds = Date.now() + state.secondsToNextPhase * 1000;
      renderSurviveState(documentRoot, state, pending, mutationPending);
    }
  }

  async function sendRequest(url, options = {}) {
    if (pending) {
      return;
    }
    setPending(true, options.method === 'POST');
    errorBox.hidden = true;
    try {
      acceptState(await requestJson(url, { redirectOnUnauthorized: false, ...options }));
    } catch (error) {
      // Reconcile once with Java after any uncertain mutation outcome; never replay the command.
      if (options.method === 'POST') {
        try { acceptState(await requestJson(API.survive.game, { redirectOnUnauthorized: false })); }
        catch (_) { /* Keep the last confirmed view and show the original failure. */ }
      }
      errorBox.textContent = `${error.message || 'The server could not be reached.'} Refresh the world before trying another move.`;
      errorBox.hidden = false;
    } finally {
      setPending(false);
    }
  }

  const join = event => {
    event.preventDefault();
    void sendRequest(API.survive.game, {
      method: 'POST', body: JSON.stringify({ name: documentRoot.getElementById('surviveName').value.trim() }),
    });
  };
  const act = event => {
    const button = event.target.closest('[data-action]');
    if (!button || button.disabled || !state) {
      return;
    }
    void sendRequest(API.survive.actions, {
      method: 'POST', body: JSON.stringify({ action: button.dataset.action, revision: state.revision }),
    });
  };
  const showJoin = () => {
    joinForm.hidden = false;
    cancel.hidden = !state;
    documentRoot.getElementById('surviveJoinTitle').textContent = 'Replace your survivor';
    documentRoot.getElementById('surviveName').focus();
  };
  const cancelJoin = () => { joinForm.hidden = true; };
  const readWorld = () => { void sendRequest(API.survive.game); };
  const chooseRecipient = () => {
    if (state) {
      renderSurviveState(documentRoot, state, pending, mutationPending);
    }
  };
  const give = event => {
    event.preventDefault();
    if (!state || pending || documentRoot.getElementById('surviveGive').disabled) {
      return;
    }
    void sendRequest(API.survive.gifts, {
      method: 'POST', body: JSON.stringify({
        recipientId: documentRoot.getElementById('surviveRecipient').value,
        resource: documentRoot.getElementById('surviveGiftResource').value,
        quantity: Number(documentRoot.getElementById('surviveGiftQuantity').value),
        revision: state.revision,
      }),
    });
  };
  giftForm.addEventListener('submit', give);
  documentRoot.getElementById('surviveRecipient').addEventListener('change', chooseRecipient);
  joinForm.addEventListener('submit', join);
  documentRoot.getElementById('surviveActions').addEventListener('click', act);
  restart.addEventListener('click', showJoin);
  cancel.addEventListener('click', cancelJoin);
  refresh.addEventListener('click', readWorld);
  const isWatchingWorld = () => state && !pending && joinForm.hidden && !documentRoot.hidden;
  // Poll only when actively viewing a joined survivor; the server settles world time on each read.
  const timer = setInterval(() => {
    if (isWatchingWorld()) {
      readWorld();
    }
  }, 5000);
  // Count down locally between polls and read the world as soon as the phase changes.
  const clockTimer = setInterval(() => {
    if (!state) {
      return;
    }
    const secondsLeft = Math.max(0, Math.ceil((phaseEndsAtMilliseconds - Date.now()) / 1000));
    documentRoot.getElementById('surviveCountdown').textContent = formatCountdown(secondsLeft);
    if (secondsLeft === 0 && isWatchingWorld()) {
      readWorld();
    }
  }, 1000);
  readWorld();
  return {
    refresh: readWorld,
    dispose() {
      clearInterval(timer);
      clearInterval(clockTimer);
      joinForm.removeEventListener('submit', join);
      documentRoot.getElementById('surviveActions').removeEventListener('click', act);
      restart.removeEventListener('click', showJoin);
      cancel.removeEventListener('click', cancelJoin);
      refresh.removeEventListener('click', readWorld);
      giftForm.removeEventListener('submit', give);
      documentRoot.getElementById('surviveRecipient').removeEventListener('change', chooseRecipient);
    },
  };
}

/** Keep controls attached while the browser parks this document in its back/forward cache. */
export function disposeSurviveOnPageHide(mountedGame, event) {
  if (!event.persisted) {
    mountedGame?.dispose();
  }
}

if (typeof document !== 'undefined') {
  const mountedGame = mountSurvive();
  window.addEventListener('pagehide', event => disposeSurviveOnPageHide(mountedGame, event));
}
```

</details>

### 5. Survive API: snapshot

```text
exit code: 0
--- stdout ---
Alice: GET /survive  -> 200 <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  

    <meta name="description" content="Gather, craft, and survive in a shared text adventure world." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/survive" />



    <meta property="og:site_name" content="christopherbell.dev" />
...
Alice: POST /api/survive/v1/game {"name": "Alice"} -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":21,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS join or replace succeeds
  state: {"status": "EXPLORING", "phase": "DAY", "day": 39, "secondsToNextPhase": 822, "health": 10, "hunger": 10, "wood": 0, "food": 0, "stone": 0, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS phase DAY matches the wall clock
PASS countdown is within one phase
PASS new survivor defaults
PASS stone gathering is offered
```

### 6. Survive API: day-rejects-night-actions

```text
exit code: 0
--- stdout ---
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":21,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS run during the day
PASS sleep and guard are not offered by day
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":21,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "SLEEP", "revision": 0} -> 400 {"messages":[{"code":"REQUEST_ERROR","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
PASS SLEEP returned 400, expected 400
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":21,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GUARD", "revision": 0} -> 400 {"messages":[{"code":"REQUEST_ERROR","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
PASS GUARD returned 400, expected 400
```

### 7. Survive API: stone-and-weapons

<details><summary>60 lines</summary>

```text
exit code: 0
--- stdout ---
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":21,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":21,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 0} -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":22,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
  state: {"status": "EXPLORING", "phase": "DAY", "day": 39, "secondsToNextPhase": 821, "health": 10, "hunger": 9, "wood": 0, "food": 0, "stone": 0, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS outside effort spends one fullness
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":22,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":22,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 1} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":23,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":23,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":23,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 2} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":24,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":24,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":24,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 3} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":25,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":25,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":25,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 4} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":26,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":26,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":26,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 5} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":27,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":27,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":27,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 6} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":28,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":28,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":28,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 7} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":29,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":29,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":29,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "HUNT", "revision": 8} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":30,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
PASS HUNT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":30,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":30,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Ali...
Alice: POST /api/survive/v1/actions {"action": "HUNT", "revision": 9} -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":31,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose s...
PASS HUNT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":31,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose s...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":31,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose s...
Alice: POST /api/survive/v1/actions {"action": "HUNT", "revision": 10} -> 200 {"name":"Alice","health":9,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":32,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! ...
PASS HUNT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":9,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":32,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! ...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":9,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":32,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! ...
Alice: POST /api/survive/v1/actions {"action": "HUNT", "revision": 11} -> 200 {"name":"Alice","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":12,"worldRevision":33,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend...
PASS HUNT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":12,"worldRevision":33,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":12,"worldRevision":33,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend...
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 12} -> 200 {"name":"Alice","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":1,"status":"COMBAT","revision":13,"worldRevision":34,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 dam...
PASS ATTACK returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":1,"status":"COMBAT","revision":13,"worldRevision":34,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 dam...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":1,"status":"COMBAT","revision":13,"worldRevision":34,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 dam...
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 13} -> 200 {"name":"Alice","health":4,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":14,"worldRevision":35,"shelters":0,"boat
... [8146 more characters not recorded]
```

</details>

### 8. Survive API: hunt-and-eat

```text
exit code: 0
--- stdout ---
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":19,"worldRevision":40,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! ...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":19,"worldRevision":40,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! ...
Alice: POST /api/survive/v1/actions {"action": "HUNT", "revision": 19} -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":20,"worldRevision":41,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend...
PASS HUNT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":20,"worldRevision":41,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend...
PASS hunting or an ambush started a fight
  state: {"status": "COMBAT", "phase": "DAY", "day": 39, "secondsToNextPhase": 820, "health": 6, "hunger": 1, "wood": 0, "food": 0, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 12, "enemy": "HOG", "enemyHealth": 5, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["ATTACK", "DEFEND", "FLEE"]}
PASS the enemy is named (HOG)
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":20,"worldRevision":41,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend...
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 20} -> 200 {"name":"Alice","health":5,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":21,"worldRevision":42,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 ...
PASS ATTACK returned 200, expected 200
  state: {"status": "EXPLORING", "phase": "DAY", "day": 39, "secondsToNextPhase": 820, "health": 5, "hunger": 0, "wood": 0, "food": 1, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 11, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT", "EAT"]}
PASS attacking wears the weapon
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":5,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":21,"worldRevision":42,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 ...
  state: {"status": "EXPLORING", "phase": "DAY", "day": 39, "secondsToNextPhase": 820, "health": 5, "hunger": 0, "wood": 0, "food": 1, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 11, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT", "EAT"]}
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":5,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":21,"worldRevision":42,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 ...
Alice: POST /api/survive/v1/actions {"action": "EAT", "revision": 21} -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":22,"worldRevision":43,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 damage. The wolf bit you for 2 dama...
PASS EAT returned 200, expected 200
  state: {"status": "EXPLORING", "phase": "DAY", "day": 39, "secondsToNextPhase": 820, "health": 7, "hunger": 5, "wood": 0, "food": 0, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 11, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS eating restores five fullness
```

### 9. Survive API: gift-stone

```text
exit code: 0
--- stdout ---
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":43,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 damage. The wolf bit you for 2 damage...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":22,"worldRevision":43,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 damage. The wolf bit you for 2 dama...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":22,"worldRevision":43,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You dealt 3 damage. The wolf bit you for 2 dama...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 22} -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":23,"worldRevision":44,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You dealt 3 damage. The wolf bit you for 2 damage.","Alice: You fled from the wolf to camp, taking 2 damage on the way.","Alic...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":23,"worldRevision":44,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You dealt 3 damage. The wolf bit you for 2 damage.","Alice: You fled from the wolf to camp, taking 2 damage on the way.","Alic...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":23,"worldRevision":44,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You dealt 3 damage. The wolf bit you for 2 damage.","Alice: You fled from the wolf to camp, taking 2 damage on the way.","Alic...
Alice: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 23} -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":24,"worldRevision":45,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You fled from the wolf to camp, taking 2 damage on the way.","Alice: You found no loose stone.","Alice: You found no loose sto...
PASS GATHER_STONE returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":24,"worldRevision":45,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You fled from the wolf to camp, taking 2 damage on the way.","Alice: You found no loose stone.","Alice: You found no loose sto...
PASS Alice holds stone
Alice: POST /api/survive/v1/gifts {"recipientId": "edae40ae-9b8c-4bbe-9160-296f23ba5732", "resource": "STONE", "quantity": 1, "revision": 24} -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":25,"worldRevision":46,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone. You are starving and lost 1 health.","Alice: You starved before y...
PASS stone gift leaves the giver
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":46,"shelters":0,"boats":0,"survivors":["Bob","Alice"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone. You are starving and lost 1 health.","Alice: You starved before you...
PASS stone gift reaches the recipient
```

### 10. Read-only query: the candidate wrote the survive world only to database test on the disposable mongod

```text
exit code: 0
--- stdout ---
{
  databases: [
    'admin',
    'config',
    'local',
    'test'
  ],
  surviveWorlds: 1
}
```

### 11. Survive API: dusk-preparations

<details><summary>60 lines</summary>

```text
exit code: 0
--- stdout ---
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":25,"worldRevision":48,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You starved before you could act. You have died. Start a new survivor to try again.","Bob arrived at camp.","Alice ar...
PASS run at dusk
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":25,"worldRevision":48,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You starved before you could act. You have died. Start a new survivor to try again.","Bob arrived at camp.","Alice ar...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":25,"worldRevision":48,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You starved before you could act. You have died. Start a new survivor to try again.","Bob arrived at camp.","Alice ar...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 25} -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":26,"worldRevision":49,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Bob arrived at camp.","Alice arrived at camp.","Alice: You found no loose stone.","Alice: You gathered one stone. Your stren...
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":26,"worldRevision":49,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Bob arrived at camp.","Alice arrived at camp.","Alice: You found no loose stone.","Alice: You gathered one stone. Your stren...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":26,"worldRevision":49,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Bob arrived at camp.","Alice arrived at camp.","Alice: You found no loose stone.","Alice: You gathered one stone. Your stren...
Alice: POST /api/survive/v1/actions {"action": "HUNT", "revision": 26} -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":27,"worldRevision":50,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You gathered one stone. Your strength and stamina increased!...
PASS HUNT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":27,"worldRevision":50,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You gathered one stone. Your strength and stamina increased!...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":7,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":27,"worldRevision":50,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice arrived at camp.","Alice: You found no loose stone.","Alice: You gathered one stone. Your strength and stamina increased!...
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 27} -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":28,"worldRevision":51,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone. Your strength and stamina increased!","Alice: You found no...
PASS ATTACK returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":28,"worldRevision":51,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone. Your strength and stamina increased!","Alice: You found no...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":28,"worldRevision":51,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone. Your strength and stamina increased!","Alice: You found no...
Alice: POST /api/survive/v1/actions {"action": "EAT", "revision": 28} -> 200 {"name":"Alice","health":8,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":29,"worldRevision":52,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone. Your strength and stamina increased!","Alice: You found no loose stone.","Alice: You found no...
PASS EAT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":29,"worldRevision":52,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone. Your strength and stamina increased!","Alice: You found no loose stone.","Alice: You found no...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":4,"stamina":12,"experience":3,"experienceToNextLevel":4,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":29,"worldRevision":52,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone. Your strength and stamina increased!","Alice: You found no loose stone.","Alice: You found no...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 29} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":30,"worldRevision":53,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no...
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":30,"worldRevision":53,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":30,"worldRevision":53,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 30} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":31,"worldRevision":54,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You gathered...
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":31,"worldRevision":54,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You gathered...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":31,"worldRevision":54,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You gathered...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 31} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":32,"worldRevision":55,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You gathered one stone.","Alice: The tree resists ...
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":32,"worldRevision":55,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You gathered one stone.","Alice: The tree resists ...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":32,"worldRevision":55,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You found no loose stone.","Alice: You gathered one stone.","Alice: The tree resists ...
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 32} -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":33,"worldRevision":56,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone.","Alice: The tree resists your efforts. No wood gathered."...
PASS ATTACK returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":33,"worldRevision":56,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone.","Alice: The tree resists your efforts. No wood gathered."...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":33,"worldRevision":56,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone.","Alice: The tree resists your efforts. No wood gathered."...
Alice: POST /api/survive/v1/actions {"action": "EAT", "revision": 33} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":34,"worldRevision":57,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone.","Alice: The tree resists your efforts. No wood gathered.","Alice: No animal found. You retur...
PASS EAT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":34,"worldRevision":57,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone.","Alice: The tree resists your efforts. No wood gathered.","Alice: No animal found. You retur...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":34,"worldRevision":57,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone.","Alice: The tree resists your efforts. No wood gathered.","Alice: No animal found. You retur...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 34} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":35,"worldRevision":58,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: The tree resists your efforts. No wood gathered.","Alice: No animal found. You return to camp.","Alice: No animal found....
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":35,"worldRevision":58,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: The tree resists your efforts. No wood gathered.","Alice: No animal found. You return to camp.","Alice: No animal found....
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":35,"worldRevision":58,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: The tree resists your efforts. No wood gathered.","Alice: No animal found. You return to camp.","Alice: No animal found....
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 35} -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":36,"worldRevision":59,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp.","Alice: No animal found. You return to camp.","Alice: No animal found. You retu...
PASS ATTACK returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":36,"worldRevision":59,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp.","Alice: No animal found. You return to camp.","Alice: No animal found. You retu...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":36,"worldRevision":59,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp.","Alice: No animal found. You return to camp.","Alice: No animal found. You retu...
Alice: POST /api/survive/v1/actions {"action": "EAT", "revision": 36} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":37,"worldRevision":60,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp.","Alice: No animal found. You return to camp. You are starving and lost 1 health...
PASS EAT returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":37,"worldRevision":60,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp.","Alice: No animal found. You return to camp. You are starving and lost 1 health...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":37,"worldRevision":60,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp.","Alice: No animal found. You return to camp. You are starving and lost 1 health...
Alice: POST /api/survive/v1/actions {"action": "GATHER", "revision": 37} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":38,"worldRevision":61,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp. You are starving and lost 1 health.","Alice: A wild hog appears! It has 5 health. C...
PASS GATHER returned 200, expected 200
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":38,"worldRevision":61,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp. You are starving and lost 1 health.","Alice: A wild hog appears! It has 5 health. C...
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":38,"worldRevision":61,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: No animal found. You return to camp. You are starving and lost 1 health.","Alice: A wild hog appears! It has 5 health. C...
Alice: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 38} -> 200 {"name":"Alice","health":6,"strength":5,"stamina":13,"experience":0,"experienceToNextLevel":8,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":39,"worldRevision":62,"shelters":0,"boa
... [11878 more characters not recorded]
```

</details>

### 12. Survive API: after-nightfall

```text
exit code: 0
--- stdout ---
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":47,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. Y...
  state: {"status": "EXPLORING", "phase": "NIGHT", "day": 39, "secondsToNextPhase": 335, "health": 8, "hunger": 7, "wood": 0, "food": 0, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 7, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": true, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS run after nightfall
PASS the nightfall raid was settled into the journal: Night 39: raiders of strength 10 overran a defense of 8 and destroyed 1 shelter and 0 boats.
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":47,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. Y...
PASS reading again does not replay the raid
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You ...
  state: {"status": "EXPLORING", "phase": "NIGHT", "day": 39, "secondsToNextPhase": 335, "health": 8, "hunger": 8, "wood": 0, "food": 0, "stone": 1, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS the burned shelter woke its sleeper
PASS Bob was told his shelter burned: Raiders burned your shelter while you slept. You escaped with 2 damage.
```

### 13. Survive API: after-dawn

```text
exit code: 0
--- stdout ---
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You ...
  state: {"status": "EXPLORING", "phase": "DAY", "day": 40, "secondsToNextPhase": 817, "health": 8, "hunger": 8, "wood": 0, "food": 0, "stone": 1, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS run after dawn
PASS Bob is awake by day
Bob was woken by the raid before dawn; dawn had no sleeper to wake
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":48,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. Y...
PASS dawn ended guard duty
```

### 14. Survive API: daytime-wood-for-shelter

<details><summary>53 lines</summary>

```text
exit code: 0
--- stdout ---
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You ...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":71,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You ...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 3} -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":72,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: You found no loose stone.","Alice: You gathered...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":72,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: You found no loose stone.","Alice: You gathered...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":72,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: You found no loose stone.","Alice: You gathered...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 4} -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":73,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone.","Alice gave 1 stone to Bob.","Tester arrived at camp.","Test...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":73,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone.","Alice gave 1 stone to Bob.","Tester arrived at camp.","Test...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":73,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You found no loose stone.","Alice: You gathered one stone.","Alice gave 1 stone to Bob.","Tester arrived at camp.","Test...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 5} -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":74,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone.","Alice gave 1 stone to Bob.","Tester arrived at camp.","Tester: You gathered one stone. Your st...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":74,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone.","Alice gave 1 stone to Bob.","Tester arrived at camp.","Tester: You gathered one stone. Your st...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":74,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one stone.","Alice gave 1 stone to Bob.","Tester arrived at camp.","Tester: You gathered one stone. Your st...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 6} -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":75,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice gave 1 stone to Bob.","Tester arrived at camp.","Tester: You gathered one stone. Your strength and stamina increased!","A...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":75,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice gave 1 stone to Bob.","Tester arrived at camp.","Tester: You gathered one stone. Your strength and stamina increased!","A...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":75,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice gave 1 stone to Bob.","Tester arrived at camp.","Tester: You gathered one stone. Your strength and stamina increased!","A...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 7} -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":76,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Tester arrived at camp.","Tester: You gathered one stone. Your strength and stamina increased!","Alice: You gathered one piece ...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":76,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Tester arrived at camp.","Tester: You gathered one stone. Your strength and stamina increased!","Alice: You gathered one piece ...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":76,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Tester arrived at camp.","Tester: You gathered one stone. Your strength and stamina increased!","Alice: You gathered one piece ...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 8} -> 200 {"name":"Bob","health":8,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":77,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Tester: You gathered one stone. Your strength and stamina increased!","Alice: You gathered one piece of wood.","Alice: A wild h...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":77,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Tester: You gathered one stone. Your strength and stamina increased!","Alice: You gathered one piece of wood.","Alice: A wild h...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":77,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Tester: You gathered one stone. Your strength and stamina increased!","Alice: You gathered one piece of wood.","Alice: A wild h...
Bob: POST /api/survive/v1/actions {"action": "HUNT", "revision": 9} -> 200 {"name":"Bob","health":8,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":10,"worldRevision":78,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one piece of wood.","Alice: A wild hog appears! It has 5 health. Choose attack, defend, or flee.","Alice: You...
PASS HUNT returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":10,"worldRevision":78,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one piece of wood.","Alice: A wild hog appears! It has 5 health. Choose attack, defend, or flee.","Alice: You...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":8,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":10,"worldRevision":78,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one piece of wood.","Alice: A wild hog appears! It has 5 health. Choose attack, defend, or flee.","Alice: You...
Bob: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 10} -> 200 {"name":"Bob","health":7,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":79,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wild hog appears! It has 5 health. Choose attack, defend, or flee.","Alice: You defeated the hog. You gathered 1 food...
PASS ATTACK returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":7,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":79,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wild hog appears! It has 5 health. Choose attack, defend, or flee.","Alice: You defeated the hog. You gathered 1 food...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":7,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":79,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wild hog appears! It has 5 health. Choose attack, defend, or flee.","Alice: You defeated the hog. You gathered 1 food...
Bob: POST /api/survive/v1/actions {"action": "EAT", "revision": 11} -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":80,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You...
PASS EAT returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":80,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":80,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.","Alice: You ate one food and feel fuller. You...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 12} -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":13,"worldRevision":81,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: You gathered one piece of wood. Your strength ...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":13,"worldRevision":81,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: You gathered one piece of wood. Your strength ...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":13,"worldRevision":81,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: You gathered one piece of wood. Your strength ...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 13} -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":14,"worldRevision":82,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one piece of wood. Your strength and stamina increased!","Alice: The tree resists your efforts. No wood ga...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":14,"worldRevision":82,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one piece of wood. Your strength and stamina increased!","Alice: The tree resists your efforts. No wood ga...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":14,"worldRevision":82,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You gathered one piece of wood. Your strength and stamina increased!","Alice: The tree resists your efforts. No wood ga...
Bob: POST /api/survive/v1/actions {"action": "GATHER", "revision": 14} -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":5,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":15,"worldRevision":83,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: The tree resists your efforts. No wood gathered.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, ...
PASS GATHER returned 200, expected 200
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":5,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":15,"worldRevision":83,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: The tree resists your efforts. No wood gathered.","Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, ...
  state: {"status": "EXPLORING", "phase": "DAY", "day": 40, "secondsToNextPhase": 785, "health": 9, "hunger": 2, "wood": 5, "food": 0, "stone": 1, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT", "BUILD_SHELTER", "CRAFT_CLUB"]}
PASS Bob carries wood for a shelter
```

</details>

### 15. Survive API: sleep-after-nightfall

```text
exit code: 0
--- stdout ---
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":5,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":15,"worldRevision":84,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 fo...
PASS run after nightfall, once the raid has passed
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":5,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":15,"worldRevision":84,"shelters":0,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 fo...
Bob: POST /api/survive/v1/actions {"action": "BUILD_SHELTER", "revision": 15} -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":16,"worldRevision":85,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the wolf. You gathered 1 food. The wolf bit you for 2 damage.","Alice: You ate one food and feel fuller. Y...
PASS BUILD_SHELTER returned 200, expected 200
PASS a new shelter offers two beds
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":48,"worldRevision":85,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the wolf. You gathered 1 food. The wolf bit you for 2 damage.","Alice: You ate one food and feel fuller....
Alice: POST /api/survive/v1/actions {"action": "SLEEP", "revision": 48} -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"SLEEPING","revision":49,"worldRevision":86,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: A wolf ambushes you! It has 8 health. Choose ...
PASS SLEEP returned 200, expected 200
  state: {"status": "SLEEPING", "phase": "NIGHT", "day": 40, "secondsToNextPhase": 337, "health": 8, "hunger": 7, "wood": 0, "food": 0, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 7, "enemy": null, "enemyHealth": 0, "shelters": 1, "boats": 0, "bedsInUse": 1, "beds": 2, "guarding": false, "actions": ["WAKE"]}
PASS Alice sleeps
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":16,"worldRevision":86,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: A wolf ambushes you! It has 8 health. Choose a...
Bob: POST /api/survive/v1/actions {"action": "SLEEP", "revision": 16} -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"SLEEPING","revision":17,"worldRevision":87,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 foo...
PASS SLEEP returned 200, expected 200
  state: {"status": "SLEEPING", "phase": "NIGHT", "day": 40, "secondsToNextPhase": 337, "health": 9, "hunger": 2, "wood": 0, "food": 0, "stone": 1, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 1, "boats": 0, "bedsInUse": 2, "beds": 2, "guarding": false, "actions": ["WAKE"]}
PASS Bob sleeps
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"SLEEPING","revision":17,"worldRevision":87,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 foo...
PASS both beds are in use
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"SLEEPING","revision":49,"worldRevision":87,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 f...
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":9,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"SLEEPING","revision":17,"worldRevision":87,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 foo...
```

### 16. Survive API: wake-early

```text
exit code: 0
--- stdout ---
Alice: GET /api/survive/v1/game  -> 200 {"name":"Alice","health":8,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"SLEEPING","revision":49,"worldRevision":87,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: A wolf ambushes you! It has 8 health. Choose attack, defend, or flee.","Alice: You defeated the wolf. You gathered 1 f...
Alice: POST /api/survive/v1/actions {"action": "WAKE", "revision": 49} -> 200 {"name":"Alice","health":10,"strength":5,"stamina":13,"experience":3,"experienceToNextLevel":8,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":50,"worldRevision":88,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You defeated the wolf. You gathered 1 food. The wolf bit you for 2 damage.","Alice: You ate one food and feel fuller...
PASS WAKE returned 200, expected 200
  state: {"status": "EXPLORING", "phase": "NIGHT", "day": 40, "secondsToNextPhase": 79, "health": 10, "hunger": 5, "wood": 0, "food": 0, "stone": 0, "weapon": "STONE_AXE", "weaponDurability": 7, "enemy": null, "enemyHealth": 0, "shelters": 1, "boats": 0, "bedsInUse": 1, "beds": 2, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT", "SLEEP"]}
PASS Alice woke early
PASS four minutes asleep recovered two health
PASS waking costs two fullness
```

### 17. Survive API: dawn-after-sleep

```text
exit code: 0
--- stdout ---
Bob: GET /api/survive/v1/game  -> 200 {"name":"Bob","health":10,"strength":4,"stamina":12,"experience":2,"experienceToNextLevel":4,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":18,"worldRevision":89,"shelters":1,"boats":0,"survivors":["Bob","Alice","Tester"],"events":["Alice: You ate one food and feel fuller. You recovered up to 2 health.","Alice: A wolf ambushes you! It has 8 health. Choose ...
  state: {"status": "EXPLORING", "phase": "DAY", "day": 41, "secondsToNextPhase": 818, "health": 10, "hunger": 0, "wood": 0, "food": 0, "stone": 1, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 1, "boats": 0, "bedsInUse": 0, "beds": 2, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS run after dawn
PASS dawn woke Bob
PASS a fed sleeper wakes at full health
PASS a night of sleep costs two fullness
PASS the journal records the dawn
```

## Evidence
- Case 1 started 2026-10-16T15:12:17-05:00, took 31 ms, candidate `0a3d242`
- Case 2 started 2026-10-16T15:12:17-05:00, took 218 ms, candidate `0a3d242`
- Case 3 started 2026-10-16T15:12:18-05:00, took 32 ms, candidate `0a3d242`
- Case 4 started 2026-10-16T15:12:18-05:00, took 46 ms, candidate `0a3d242`
- Case 5 started 2026-10-16T15:12:18-05:00, took 139 ms, candidate `0a3d242`
- Case 6 started 2026-10-16T15:12:18-05:00, took 218 ms, candidate `0a3d242`
- Case 7 started 2026-10-16T15:12:19-05:00, took 921 ms, candidate `0a3d242`
- Case 8 started 2026-10-16T15:12:20-05:00, took 281 ms, candidate `0a3d242`
- Case 9 started 2026-10-16T15:12:20-05:00, took 266 ms, candidate `0a3d242`
- Case 10 started 2026-10-16T15:12:33-05:00, took 280 ms, candidate `0a3d242`
- Case 11 started 2026-10-16T15:26:21-05:00, took 1358 ms, candidate `0a3d242`
- Case 12 started 2026-10-16T15:30:24-05:00, took 187 ms, candidate `0a3d242`
- Case 13 started 2026-10-16T15:36:22-05:00, took 187 ms, candidate `0a3d242`
- Case 14 started 2026-10-16T15:36:55-05:00, took 515 ms, candidate `0a3d242`
- Case 15 started 2026-10-16T15:54:23-05:00, took 297 ms, candidate `0a3d242`
- Case 16 started 2026-10-16T15:58:41-05:00, took 156 ms, candidate `0a3d242`
- Case 17 started 2026-10-16T16:00:22-05:00, took 157 ms, candidate `0a3d242`

## Bugs / Follow-ups
- A first attempt at 20:10 UTC, still at night, used a driver that only gathered. Its survivor Alice met two wolves and failed nine stone rolls, then starved under the approved rules. The driver was rewritten to eat and hunt, readiness moved to `/actuator/info` because `/actuator/health` returns 403 to anonymous callers, and every case was rerun into a fresh evidence file. No candidate code changed.
- Cleanup: `Stop-Candidate.ps1` stopped the candidate and its mongod, removed the disposable MongoDB root and JDK socket directory, and ports 62451 and 62452 have no listeners. Every fixture was created through the application's endpoints.
- Compatibility with a world saved before this change is covered by `SurviveWorldMongoCodecTest`, not by this run; the production readback after merge confirms it against the live document.

## Document Status
complete

## Project
christopherbell-dev
