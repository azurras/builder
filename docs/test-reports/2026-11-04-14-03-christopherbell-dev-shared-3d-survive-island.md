# Shared 3D Survive island: Test Report

## Story/Issue
User-approved third-person shared island with live visible multiplayer, browser-native rendering and Java-owned survival. [Plan](../implementation-plans/2026-11-04-13-37-christopherbell-dev-explore-survive-together-in-a-third-person-3d-island.md).

## Branch
`codex/survive-3d-world-20261104` at `3eb9788e7acefddec1a9a113751d607101f3273c`.

## Pass / Fail

> [!TIP]
> **8 of 8 final cases passed** on candidate `3eb9788e`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Committed candidate readiness and isolated test database | PASS | Observed expected runtime behavior below. |
| 2 | Candidate build identity | PASS | Observed expected runtime behavior below. |
| 3 | Two-survivor movement and survival API contracts | PASS | Observed expected runtime behavior below. |
| 4 | Public island page includes the new accessible viewport | PASS | Observed expected runtime behavior below. |
| 5 | Two independent browsers share live movement and forest gathering | PASS | Observed expected runtime behavior below. |
| 6 | Phone controls and reload preserve progress | PASS | Observed expected runtime behavior below. |
| 7 | Quarry, hunting, combat, phase change and departure | PASS | Observed expected runtime behavior below. |
| 8 | Owned candidate and Mongo cleanup | PASS | Observed expected runtime behavior below. |

## Test Cases
1. **Committed candidate readiness and isolated test database:** pwsh -NoProfile -File ops/local/Start-Candidate.ps1 -StateFile <scratch>/survive-3d-candidate.json
2. **Candidate build identity:** GET http://127.0.0.1:63008/actuator/info
3. **Two-survivor movement and survival API contracts:** python <scratch>/survive-3d-runtime.py http://127.0.0.1:63008
4. **Public island page includes the new accessible viewport:** GET http://127.0.0.1:63008/survive
5. **Two independent browsers share live movement and forest gathering:** Chrome: join Coast Scout. IAB: join Island Scout. Walk Island Scout to Pine forest; then walk Coast Scout to Pine forest. Click contextual Gather wood.
6. **Phone controls and reload preserve progress:** Set IAB viewport 390x844; choose Boat shore. Hold Walk forward pointer button for 1000 ms; focus canvas and hold W for 1000 ms. Reload. Reset viewport override.
7. **Quarry, hunting, combat, phase change and departure:** Walk to Stone ridge and Gather stone. Walk to Hunting grounds and Hunt; then Defend and Flee to camp. Close Coast Scout browser and observe presence expiry.
8. **Owned candidate and Mongo cleanup:** pwsh -NoProfile -File ops/local/Stop-Candidate.ps1 -StateFile <scratch>/survive-3d-candidate.json

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev / Survive |
| Candidate URL | http://127.0.0.1:63008 |
| Profile | Exactly test |
| Mongo | Disposable loopback 63007, database test; effective URI verified by candidate helper before startup and db.getName() after startup |
| Browsers | Independent IAB and Chrome cookie stores; desktop and IAB 390x844 override |
| Native checks | Full :website:build passed; 2199 Java tests with 0 failures/errors and 126 configured skips; all 438 JS tests passed; Checkstyle and Windows Pester gates passed |

## Local Run Details
- **Local command:** `pwsh -NoProfile -File ops/local/Start-Candidate.ps1 -StateFile <scratch>/survive-3d-candidate.json`
- **Working directory:** isolated Survive worktree at candidate `3eb9788e`.
- **Identity:** /actuator/info returned the built candidate commit `3eb9788e7acefddec1a9a113751d607101f3273c`.
- **Processes:** candidate launcher 42304 and disposable Mongo 5996; app port 63008 and Mongo port 63007.
- **Logs:** disposable candidate output/error logs under the owned test Mongo directory; sanitized runtime records retained in scratch as survive-3d-evidence.jsonl and survive-3d-browser-evidence.txt.
- **Cleanup:** Both browser tabs closed, viewport override reset; Stop-Candidate stopped owned process trees, confirmed zero listeners on both ports and removed owned Mongo/JDK temporary directories.

## Data Sent

### 1. Committed candidate readiness and isolated test database

```text
pwsh -NoProfile -File ops/local/Start-Candidate.ps1 -StateFile <scratch>/survive-3d-candidate.json
```

### 2. Candidate build identity

```text
GET http://127.0.0.1:63008/actuator/info
```

### 3. Two-survivor movement and survival API contracts

```text
python <scratch>/survive-3d-runtime.py http://127.0.0.1:63008
```

### 4. Public island page includes the new accessible viewport

```text
GET http://127.0.0.1:63008/survive
```

### 5. Two independent browsers share live movement and forest gathering

```text
Chrome: join Coast Scout. IAB: join Island Scout. Walk Island Scout to Pine forest; then walk Coast Scout to Pine forest. Click contextual Gather wood.
```

### 6. Phone controls and reload preserve progress

```text
Set IAB viewport 390x844; choose Boat shore. Hold Walk forward pointer button for 1000 ms; focus canvas and hold W for 1000 ms. Reload. Reset viewport override.
```

### 7. Quarry, hunting, combat, phase change and departure

```text
Walk to Stone ridge and Gather stone. Walk to Hunting grounds and Hunt; then Defend and Flee to camp. Close Coast Scout browser and observe presence expiry.
```

### 8. Owned candidate and Mongo cleanup

```text
pwsh -NoProfile -File ops/local/Stop-Candidate.ps1 -StateFile <scratch>/survive-3d-candidate.json
```

## Response Received

### 1. Committed candidate readiness and isolated test database

```text
exit code: 0
--- stdout ---
{
  "baseUrl": "http://127.0.0.1:63008",
  "candidatePid": 42304,
  "candidatePort": 63008,
  "mongoPid": 5996,
  "mongoPort": 63007,
  "testMongoRoot": "<scratch>\\christopherbell-test-mongo-e26962cf82e744d894aee5bd66c3ff21",
  "javaSocketRoot": "<temporary-root>\\cbell-jdk-8e93601afdc641f4878c0f2c1aa273c8",
  "candidateLog": "<scratch>\\christopherbell-test-mongo-e26962cf82e744d894aee5bd66c3ff21\\candidate.out.log",
  "candidateErrorLog": "<scratch>\\christopherbell-test-mongo-e26962cf82e744d894aee5bd66c3ff21\\candidate.err.log",
  "testAdministratorFile": null,
  "databaseName": "test",
  "ready": true
}
```

### 2. Candidate build identity

```text
HTTP 200 
X-Request-Id: 76cc6464-1366-457d-a6be-b40930c9af7e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1793822347
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
Date: Wed, 04 Nov 2026 19:58:07 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-11-04T19:57:27.881Z","version":"0.0.0-dev.3eb9788e7acefddec1a9a113751d607101f3273c","group":"christopherbell.dev"}}
```

### 3. Two-survivor movement and survival API contracts

```text
exit code: 0
--- stdout ---
PASS readiness: GET /actuator/health/readiness => 200 UP
PASS independent guest joins: Field Scout and Camp Scout have distinct public IDs
PASS live public presence: second client sees first; pulses preserve survival revision
PASS physical command guard: gathering at camp => 400
PASS route validation: missing CSRF => 403; out-of-island coordinate => 400
PASS shared movement: ten timed steps reach forest (-24,-15), independently observed by Camp Scout
PASS teleport and stale sequence rejected without moving the survivor
PASS forest action: GATHER => 200, revision advanced once; wood=0, status=EXPLORING
PASS refresh retains survivor, inventory and authoritative revision
PASS text fallback: leave => 204 removes only own pose and preserves saved survivor
All local API runtime checks passed. No direct database writes or production requests.
```

### 4. Public island page includes the new accessible viewport

```text
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
            <canvas id="surviveWorldCanvas" tabindex="0" aria-label="Third-person island. WASD or arrows to walk; drag to turn the camera. Q and R rotate, E interacts, Escape stops walking." aria-describedby="surviveWorldHelp"></canvas>
```

### 5. Two independent browsers share live movement and forest gathering

```text
Separate survivors 41d767e6 and 5b6a6d17. Both browsers reached Pine forest / 1 m. Remote Coast Scout projected label moved from left=65.7709%, top=17.6779% to left=50.0342%, top=41.7%. Gathering returned: You gathered one piece of wood. Your strength and stamina increased! Wood=1. Console warnings/errors inspected: none.
```

### 6. Phone controls and reload preserve progress

```text
Body width=375 and scrollWidth=375; canvas=299x400 with controls wrapping within page width. Boat shore / 1 m -> 6 m after held pointer -> 12 m after held W. Reload retained wood=1, Camp ID=41d767e6 and live presence. SVG fallback isVisible=false. Perspective screenshot showed player, ocean, dock, paths and named other player.
```

### 7. Quarry, hunting, combat, phase change and departure

```text
Stone ridge / 1 m: You found no loose stone. Hunting grounds / 1 m: A wild hog appears! It has 5 health. Context controls became Attack/Defend/Flee to camp. Defend blocked the bite. Flee returned to Camp / 0 m with health=9/10 after acknowledgement. Phase changed from day to dusk; Stand guard became available at camp. Departed player expired; Live island / 1 online. No inspected console warnings/errors.
```

### 8. Owned candidate and Mongo cleanup

```text
exit code: 0
--- stdout ---
port 63008 listeners: 0
port 63007 listeners: 0
removed <scratch>\christopherbell-test-mongo-e26962cf82e744d894aee5bd66c3ff21
removed <temporary-root>\cbell-jdk-8e93601afdc641f4878c0f2c1aa273c8
```

## Evidence
- Machine-specific temporary path prefixes are abbreviated as `<scratch>` and `<temporary-root>`; original absolute paths remain in local raw evidence.
- Candidate-specific API/startup/identity/cleanup were recorded as they ran using record_run.py; browser inputs and actual observations were recorded during CUA verification.
- Native commands: Invoke-Gradle.ps1 :website:build; node --check for touched JS modules; final all-JS runner; committed Invoke-Gradle.ps1 :website:jsTest :website:bootJar.
- Full native build: BUILD SUCCESSFUL in 7m 1s. Java XML summary: tests=2199, failures=0, errors=0, skipped=126. JS final: 438 passed, 0 failed.
- Independent semantic review found one disconnected-avatar defect; failing regression was observed before correction, then seven world tests passed and reviewer confirmed no remaining blockers.

## Bugs / Follow-ups
- Resolved verification-harness attempt: the first API probe used protected /actuator/health and correctly received 403. It was corrected to documented /actuator/health/readiness (200 UP), and the complete API case passed on the same unchanged candidate. The failed attempt remains in the raw evidence; final cases above use its successful retest.
- Accepted first-release limits: positions are transient and reset after idle reconnection/restart; presence assumes one app process; existing 300 mutations/minute/IP limit can cause visible backoff for larger shared-IP groups. No production data was accessed during local verification.
- Native Java reported 126 configured skips: 123 Mongo contract/integration cases and 3 platform/environment-specific filesystem cases. None are counted as passes. The changed HTTP and persistence-facing behavior was exercised against the disposable local test database.

## Document Status
complete

## Project
christopherbell-dev
