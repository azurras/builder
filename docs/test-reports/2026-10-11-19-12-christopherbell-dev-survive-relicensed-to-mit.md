# Survive relicensed to MIT: Test Report

## Story/Issue
User request 2026-10-11 to keep the website very permissively licensed; relicense Survive from GPL-3.0 to MIT ([plan](../implementation-plans/2026-10-11-19-00-christopherbell-dev-survive-relicensed-to-mit.md))

## Branch
`claude/relicense-survive-mit-20261011` at candidate `57c53e0`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `57c53e0`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status below 400 and body containing '"UP"' |
| 2 | Candidate opened database test on the disposable mongod (read-only listing) | ✅ PASS | Expected exit code 0 |
| 3 | Anonymous GET /licenses/survive-MIT.txt serves the MIT license | ✅ PASS | Expected status 200 and body containing 'Permission is hereby granted, free of charge' |
| 4 | MIT license names the copyright holder | ✅ PASS | Expected status 200 and body containing 'Copyright (c) 2016 Christopher Bell' |
| 5 | Survive page attribution links the MIT license | ✅ PASS | Expected status 200 and body containing '<a href="/licenses/survive-MIT.txt">MIT license</a>' |
| 6 | Old GPL license path is no longer public (403) | ✅ PASS | Expected status 403 |
| 7 | Survive page contains no GPL reference | ✅ PASS | Expected exit code 0 |
| 8 | Regression: anonymous Survive game snapshot before joining returns 204 | ✅ PASS | Expected status 204 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:55297/actuator/health/readiness`
2. **Candidate opened database test on the disposable mongod (read-only listing)**: command `C:/Users/Christopher/AppData/Local/Programs/mongosh/mongosh.exe --quiet --norc mongodb://127.0.0.1:55296/test --eval "print(db.getName()); print(db.getCollectionNames().length > 0)"`
3. **Anonymous GET /licenses/survive-MIT.txt serves the MIT license**: http `GET http://127.0.0.1:55297/licenses/survive-MIT.txt`
4. **MIT license names the copyright holder**: http `GET http://127.0.0.1:55297/licenses/survive-MIT.txt`
5. **Survive page attribution links the MIT license**: http `GET http://127.0.0.1:55297/survive`
6. **Old GPL license path is no longer public (403)**: http `GET http://127.0.0.1:55297/licenses/survive-GPL-3.0.txt`
7. **Survive page contains no GPL reference**: command `python -c "import sys,urllib.request;b=urllib.request.urlopen('http://127.0.0.1:55297/survive').read().decode();print('GPL occurrences:',b.count('GPL'));sys.exit(1 if 'GPL' in b else 0)"`
8. **Regression: anonymous Survive game snapshot before joining returns 204**: http `GET http://127.0.0.1:55297/api/survive/v1/game`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod (8.3) on an OS-selected loopback port |
| Candidate | packaged website.jar at 127.0.0.1:55297 |
| Automated checks | ./gradlew :website:test: 2130 tests, 0 failures, 110 skipped |
| Production | not contacted |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:55297/actuator/health/readiness` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `C:/Users/Christopher/AppData/Local/Programs/mongosh/mongosh.exe --quiet --norc mongodb://127.0.0.1:55296/test --eval "print(db.getName()); print(db.getCollectionNames().length > 0)"` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `GET http://127.0.0.1:55297/licenses/survive-MIT.txt` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `GET http://127.0.0.1:55297/licenses/survive-MIT.txt` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `GET http://127.0.0.1:55297/survive` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `GET http://127.0.0.1:55297/licenses/survive-GPL-3.0.txt` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `python -c "import sys,urllib.request;b=urllib.request.urlopen('http://127.0.0.1:55297/survive').read().decode();print('GPL occurrences:',b.count('GPL'));sys.exit(1 if 'GPL' in b else 0)"` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Local command:** `GET http://127.0.0.1:55297/api/survive/v1/game` in `A:\Projects\christopherbell.dev.worktrees\relicense-survive-mit`
- **Candidate identity:** `57c53e0`
- **Cleanup:** Stopped the candidate and disposable mongod process trees, confirmed both ports stopped listening, and removed the generated mongo data root and JDK socket root. No fixtures were created.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:55297/actuator/health/readiness
```

### 2. Candidate opened database test on the disposable mongod (read-only listing)

```text
C:/Users/Christopher/AppData/Local/Programs/mongosh/mongosh.exe --quiet --norc mongodb://127.0.0.1:55296/test --eval "print(db.getName()); print(db.getCollectionNames().length > 0)"
```

### 3. Anonymous GET /licenses/survive-MIT.txt serves the MIT license

```http
GET http://127.0.0.1:55297/licenses/survive-MIT.txt
```

### 4. MIT license names the copyright holder

```http
GET http://127.0.0.1:55297/licenses/survive-MIT.txt
```

### 5. Survive page attribution links the MIT license

```http
GET http://127.0.0.1:55297/survive
```

### 6. Old GPL license path is no longer public (403)

```http
GET http://127.0.0.1:55297/licenses/survive-GPL-3.0.txt
```

### 7. Survive page contains no GPL reference

```text
python -c "import sys,urllib.request;b=urllib.request.urlopen('http://127.0.0.1:55297/survive').read().decode();print('GPL occurrences:',b.count('GPL'));sys.exit(1 if 'GPL' in b else 0)"
```

### 8. Regression: anonymous Survive game snapshot before joining returns 204

```http
GET http://127.0.0.1:55297/api/survive/v1/game
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: ed71b93f-abe8-4efd-b12a-203ee46f0251
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791764002
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
Date: Mon, 12 Oct 2026 00:12:22 GMT
Connection: close

{"status":"UP"}
```

### 2. Candidate opened database test on the disposable mongod (read-only listing)

```text
exit code: 0
--- stdout ---
test
true
```

### 3. Anonymous GET /licenses/survive-MIT.txt serves the MIT license

<details><summary>41 lines</summary>

```text
HTTP 200 
X-Request-Id: 369e13c0-2e43-4234-9353-0434281445a7
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791764003
Cache-Control: max-age=3600, public
Last-Modified: Mon, 12 Oct 2026 00:12:07 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/plain
Content-Length: 1073
Date: Mon, 12 Oct 2026 00:12:23 GMT
Connection: close

MIT License

Copyright (c) 2016 Christopher Bell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

### 4. MIT license names the copyright holder

<details><summary>41 lines</summary>

```text
HTTP 200 
X-Request-Id: 466f405b-da21-481e-a2f4-ba5c9ae9d348
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791764003
Cache-Control: max-age=3600, public
Last-Modified: Mon, 12 Oct 2026 00:12:07 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/plain
Content-Length: 1073
Date: Mon, 12 Oct 2026 00:12:23 GMT
Connection: close

MIT License

Copyright (c) 2016 Christopher Bell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

### 5. Survive page attribution links the MIT license

<details><summary>146 lines</summary>

```text
HTTP 200 
X-Request-Id: 318f4cf0-a69f-4c28-9ff0-7c5dfb5bc40b
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791764003
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
Date: Mon, 12 Oct 2026 00:12:23 GMT
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
  <link rel="stylesheet" href="/7dec6f3c6ee5087ba183/css/main.css" />
  <link rel="stylesheet" href="/7dec6f3c6ee5087ba183/css/survive.css" />
</head>
<body class="site-page void-shell-page survive-page">
  <div id="nav"></div>
  <main class="site-main survive-main">
    <header class="survive-hero">
      <p class="survive-eyebrow">A shared world · A text adventure</p>
      <h1>Survive<span aria-hidden="true">.</span></h1>
      <p>The wilderness is unforgiving. You don't have to face it alone.</p>
      <div class="survive-intro"><span aria-hidden="true">↟</span> Gather wood. Build a camp. Find your way out.</div>
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
        <h2 id="surviveScene">At the edge of the wilderness</h2>
        <p id="surviveMessage" class="survive-message" role="status" aria-live="polite" aria-atomic="true"></p>
        <div id="surviveEnemy" class="survive-enemy" hidden><strong>Wild hog</strong><span id="surviveEnemyHealth"></span></div>
        <p class="survive-eyebrow">Choose your next move</p>
        <div id="surviveActions" class="survive-actions">
          <button type="button" data-action="GATHER">Gather wood <small>50% chance · +1 wood</small></button>
          <button type="button" data-action="HUNT">Hunt <small>Search for a wild hog</small></button>
          <button type="button" data-action="BUILD_SHELTER">Build shelter <small>5 wood · Shared with camp</small></button>
          <button type="button" data-action="BUILD_BOAT">Build boat <small>10 wood · One escape</small></button>
          <button type="button" data-action="EAT">Eat food <small>1 food · Restore up to 5 health</small></button>
          <button type="button" data-action="REST">Rest <small>Requires shelter · +2 health</small></button>
          <button type="button" data-action="ESCAPE">Sail away <small>Use a shared boat · Survive</small></button>
          <button type="button" data-action="ATTACK">Attack <small>Strike the hog · Take 1 damage</small></button>
          <button type="button" data-action="DEFEND">Defend <small>Block the hog's bite</small></button>
          <button type="button" data-action="FLEE">Flee <small>Return to camp · Take 1 damage</small></button>
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
          <dl class="survive-stats"><div><dt>Strength</dt><dd id="surviveStrength"></dd></div><div><dt>Stamina</dt><dd id="surviveStamina"></dd></div><div><dt>Gathering XP</dt><dd id="surviveExperience"></dd></div></dl>
          <h3>Inventory <span id="surviveInventoryCount"></span></h3>
          <dl class="survive-stats"><div><dt>Wood</dt><dd id="surviveWood"></dd></div><div><dt>Food</dt><dd id="surviveFood"></dd></div></dl>
        </section>
        <section class="survive-panel" aria-labelledby="surviveCampTitle">
          <p class="survive-eyebrow">One world, built together</p><h2 id="surviveCampTitle">Shared camp</h2>
          <dl class="survive-stats"><div><dt>Shelters</dt><dd id="surviveShelters"></dd></div><div><dt>Boats</dt><dd id="surviveBoats"></dd></div></dl>
          <h3>Survivors in camp <span id="survivePlayerCount"></span></h3><ul id="survivePlayers" class="survive-players"></ul>
          <form id="surviveGift" class="survive-gift" aria-labelledby="surviveGiftTitle">
            <h3 id="surviveGiftTitle">Share supplies</h3>
            <label for="surviveRecipient">Give to</label>
            <select id="surviveRecipient" name="recipientId" required></select>
            <div class="survive-gift-amount">
              <div><label for="surviveGiftResource">Supply</label><select id="surviveGiftResource" name="resource"><option value="WOOD">Wood</option><option value="FOOD">Food</option></select></div>
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
      <p>Share supplies chooses another survivor by name and camp ID. Give 1–10 wood or food while both of you are at camp. Gifts move items directly into their inventory, which must have room; both survivors and the camp journal receive an update.</p>
      <p>Gather wood to improve strength and stamina. Your inventory holds 10 items. Five wood builds a shelter everyone can rest in; ten wood builds a boat any survivor can use to escape.</p>
      <p>Hunt to find hogs with 5 health. Your attack deals 1 + strength damage, and each attack costs 1 health, even the final blow. Defend blocks damage; flee returns you to camp at a cost of 1 health. Defeating a hog gives 1 food if you have room. Eating consumes it and restores up to 5 health. A shared shelter restores 2 health per rest.</p>
      <p>Sail away to survive, or start again after death. New survivor replaces only your character. Saved account characters can start again after death or escape; joining again resumes a living character. Shelters, boats, and other players remain in the shared world. Names and recent actions are visible to other players; use a nickname.</p>
      <p>Your logged-in account has one saved survivor. Moves, supplies, combat and the shared camp are saved after each successful command and survive server restarts. Log in again to resume. Guests use a temporary browser session and expire after two idle hours. Saved survivors keep their progress while inactive and return to the active camp when resumed. Guest progress stays separate from your account character. This version has no chat or matchmaking.</p>
    </details>
    <p class="survive-attribution">Adapted from <a href="https://github.com/azurras/survive">azurras/Survive</a> · Java game engine · <a href="/licenses/survive-MIT.txt">MIT license</a>. Browser adaptation completes the original's unfinished combat and food actions.</p>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/7dec6f3c6ee5087ba183/js/app.js"></script>
  <script type="module" src="/7dec6f3c6ee5087ba183/js/survive.js"></script>
</body>
</html>
```

</details>

### 6. Old GPL license path is no longer public (403)

```text
HTTP 403 
X-Request-Id: 367d859b-a245-4528-a62c-0b6a50adff20
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791764010
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
Date: Mon, 12 Oct 2026 00:12:30 GMT
Connection: close

{"timestamp":"2026-10-12T00:12:30.464Z","status":403,"error":"Forbidden","path":"/licenses/survive-GPL-3.0.txt"}
```

### 7. Survive page contains no GPL reference

```text
exit code: 0
--- stdout ---
GPL occurrences: 0
```

### 8. Regression: anonymous Survive game snapshot before joining returns 204

```text
HTTP 204 
X-Request-Id: 29b7981d-919a-46e8-bbfe-3741ae012621
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791764010
Cache-Control: no-store
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Date: Mon, 12 Oct 2026 00:12:30 GMT
Connection: close
```

## Evidence
- Case 1 started 2026-10-11T19:12:22-05:00, took 31 ms, candidate `57c53e0`
- Case 2 started 2026-10-11T19:12:22-05:00, took 296 ms, candidate `57c53e0`
- Case 3 started 2026-10-11T19:12:23-05:00, took 46 ms, candidate `57c53e0`
- Case 4 started 2026-10-11T19:12:23-05:00, took 32 ms, candidate `57c53e0`
- Case 5 started 2026-10-11T19:12:23-05:00, took 202 ms, candidate `57c53e0`
- Case 6 started 2026-10-11T19:12:30-05:00, took 31 ms, candidate `57c53e0`
- Case 7 started 2026-10-11T19:12:30-05:00, took 108 ms, candidate `57c53e0`
- Case 8 started 2026-10-11T19:12:30-05:00, took 47 ms, candidate `57c53e0`

## Bugs / Follow-ups
- Gradle on this machine needed `TEMP`/`TMP` pointed at `A:\Temp\relicense-tmp` and an isolated `GRADLE_USER_HOME`; with the session's default temp folder the daemon failed with "Unable to establish loopback connection".
- `mongod` 8.3 is not on PATH; the run prepended `C:\Program Files\MongoDB\Server\8.3\bin`.

## Document Status
complete

## Project
christopherbell-dev
