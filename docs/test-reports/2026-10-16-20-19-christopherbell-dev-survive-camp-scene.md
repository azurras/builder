# Survive camp scene: Test Report

## Story/Issue
User request 2026-10-16 "give the game a gui"; plan docs/implementation-plans/2026-10-16-19-44-christopherbell-dev-survive-camp-scene.md

## Branch
`claude/survive-camp-scene-20261016` at candidate `8627fff`

## Pass / Fail

> [!TIP]
> 22 of 22 cases passed on candidate `8627fff`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate is ready and reports its build | ✅ PASS | Expected status below 400 and body containing '"build"' |
| 2 | Survive page embeds the labelled camp scene above the move buttons | ✅ PASS | Expected status below 400 and body containing 'id="surviveCampScene" class="survive-scene" role="img"' |
| 3 | Scene module is served with phone-sized hit areas | ✅ PASS | Expected status below 400 and body containing 'fire: { x: 518, y: 395, width: 145, height: 145 }' |
| 4 | Scene styles include the reduced-motion overrides | ✅ PASS | Expected status below 400 and body containing 'prefers-reduced-motion' |
| 5 | API survivor Carpenter builds two shelters for the scene to draw | ✅ PASS | Expected exit code 0 |
| 6 | Read-only query: the candidate wrote only to database test on the disposable mongod | ✅ PASS | Expected exit code 0 |
| 7 | Joining as `<img src=x onerror=alert(1)>` renders the name as literal SVG text | ✅ PASS | Scene label text equals the name; 0 `img` or `foreignObject` elements created |
| 8 | At night the scene shows stars and moon and its label names the phase | ✅ PASS | `data-phase` NIGHT; label "Night, day 50. 0 shelters, 0 boats, 1 survivor at camp. You are at camp." |
| 9 | Clicking the trees sends GATHER | ✅ PASS | Revision 0 to 1, wood 1, fullness 9, "You gathered one piece of wood." |
| 10 | Clicking the shore while escape is not allowed sends nothing | ✅ PASS | Revision stayed 1 |
| 11 | Clicking the rocks sends GATHER_STONE | ✅ PASS | Revision 2, "You found no loose stone." |
| 12 | Clicking the forest edge sends HUNT | ✅ PASS | Revision 3 "No animal found", then revision 4 a hog appeared |
| 13 | Clicking the forest edge mid-fight, when HUNT is not allowed, sends nothing | ✅ PASS | Revision stayed 4 |
| 14 | In combat the hog is drawn with a health bar and clicking it sends ATTACK | ✅ PASS | Bar 100 then 20 after 4 damage; second click defeated it, +1 food, enemy removed from the scene |
| 15 | Clicking the fire by day sends REST | ✅ PASS | Revision 7, health 8 to 10 |
| 16 | At 375x812 every hotspot is at least 44 pixels and the page has no horizontal scroll | ✅ PASS | Scene 301 px wide; smallest hotspot 44.9 px; no horizontal scroll |
| 17 | A tap on the trees at phone width sends GATHER | ✅ PASS | Revision 8, wood 2 |
| 18 | Clicking the fire at dusk sends GUARD and draws a torch | ✅ PASS | Revision 10, guarding true, 1 torch; label ends "You stand guard by the fire." |
| 19 | After nightfall the raid flashes the camp and the burned tent disappears | ✅ PASS | Event "Night 51: raiders of strength 6 overran a defense of 5 and destroyed 1 shelter and 0 boats."; 1 flash, 3 smoke puffs, 1 tent |
| 20 | Clicking the tent at night sends SLEEP; the player shows as asleep and the tent offers WAKE | ✅ PASS | Revision 12, SLEEPING, "z z" drawn, player figure hidden, tent hotspot WAKE |
| 21 | Clicking the tent while asleep sends WAKE | ✅ PASS | Revision 13, EXPLORING, player figure drawn again |
| 22 | The browser console logged no errors through all cases | ✅ PASS | No console messages |

## Test Cases
1. **Candidate is ready and reports its build**: http `GET http://127.0.0.1:64024/actuator/info`
2. **Survive page embeds the labelled camp scene above the move buttons**: http `GET http://127.0.0.1:64024/survive`
3. **Scene module is served with phone-sized hit areas**: http `GET http://127.0.0.1:64024/js/survive-scene.js`
4. **Scene styles include the reduced-motion overrides**: http `GET http://127.0.0.1:64024/css/survive.css`
5. **API survivor Carpenter builds two shelters for the scene to draw**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/scene-candidate.json build-shelters`
6. **Read-only query: the candidate wrote only to database test on the disposable mongod**: command `mongosh --quiet --port 64023 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name), surviveWorlds: db.getSiblingDB('test').application_runtime.countDocuments({_kind: 'survive_world'})})"`

## Browser Cases
Cases 7 to 22 ran in the Claude desktop app's browser pane against the candidate at `http://127.0.0.1:64024/survive` on 2026-10-17 UTC, from 01:07 (day 51, after a night that began the session) through dusk at 01:14 and nightfall at 01:18. Each click was a real pointer click at the hotspot's on-screen centre. After each click a read-only `GET /api/survive/v1/game` from the page confirmed the server state, and the scene's own DOM was read for the drawn elements. The phase-dependent cases waited for the real clock. Case 10 used the browser's 375x812 mobile preset.

## Automated Checks
- `.\ops\local\Invoke-Gradle.ps1 :website:build :website:bootJar` on `8627fff`: BUILD SUCCESSFUL, 2,166 Java tests with 0 failed and 110 skipped, Checkstyle clean, and `jsTest` with 26 Survive JS tests among 408, 0 failed.
- The new scene tests failed before `survive-scene.js` existed and passed once it was written.

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a disposable loopback mongod (port 64023), removed after the run |
| Candidate | website.jar built from the committed HEAD, http://127.0.0.1:64024 |
| Browser | Claude desktop browser pane, 1024x768 and the 375x812 mobile preset |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:64024/actuator/info` in `A:\Projects\christopherbell.dev.worktrees\survive-scene`
- **Local command:** `GET http://127.0.0.1:64024/survive` in `A:\Projects\christopherbell.dev.worktrees\survive-scene`
- **Local command:** `GET http://127.0.0.1:64024/js/survive-scene.js` in `A:\Projects\christopherbell.dev.worktrees\survive-scene`
- **Local command:** `GET http://127.0.0.1:64024/css/survive.css` in `A:\Projects\christopherbell.dev.worktrees\survive-scene`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/scene-candidate.json build-shelters` in `A:\Projects\christopherbell.dev.worktrees\survive-scene`
- **Local command:** `mongosh --quiet --port 64023 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name), surviveWorlds: db.getSiblingDB('test').application_runtime.countDocuments({_kind: 'survive_world'})})"` in `A:\Projects\christopherbell.dev.worktrees\survive-scene`
- **Candidate identity:** `8627fff`
- **Cleanup:** Stopped the candidate process tree; no fixtures remain.

## Data Sent

### 1. Candidate is ready and reports its build

```http
GET http://127.0.0.1:64024/actuator/info
```

### 2. Survive page embeds the labelled camp scene above the move buttons

```http
GET http://127.0.0.1:64024/survive
```

### 3. Scene module is served with phone-sized hit areas

```http
GET http://127.0.0.1:64024/js/survive-scene.js
```

### 4. Scene styles include the reduced-motion overrides

```http
GET http://127.0.0.1:64024/css/survive.css
```

### 5. API survivor Carpenter builds two shelters for the scene to draw

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/scene-candidate.json build-shelters
```

### 6. Read-only query: the candidate wrote only to database test on the disposable mongod

```text
mongosh --quiet --port 64023 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name), surviveWorlds: db.getSiblingDB('test').application_runtime.countDocuments({_kind: 'survive_world'})})"
```

## Response Received

### 1. Candidate is ready and reports its build

```text
HTTP 200 
X-Request-Id: 1708b623-b8ea-4ab9-b92f-fd5e6ef11b99
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792199282
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
Date: Sat, 17 Oct 2026 01:07:02 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-10-17T01:01:30.188Z","version":"0.0.0-dev.8627fffac7e6aef0df2a79999e6ee3f9d053fe5a","group":"christopherbell.dev"}}
```

### 2. Survive page embeds the labelled camp scene above the move buttons

<details><summary>169 lines</summary>

```text
HTTP 200 
X-Request-Id: e9acb010-50e3-4d31-b2da-fb86f7b1836d
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792199282
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
Date: Sat, 17 Oct 2026 01:07:02 GMT
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
  <link rel="stylesheet" href="/4bd43b978eaea51a6c72/css/main.css" />
  <link rel="stylesheet" href="/4bd43b978eaea51a6c72/css/survive.css" />
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
        <svg id="surviveCampScene" class="survive-scene" role="img" aria-label="The camp" viewBox="0 0 960 540"></svg>
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
      <p>The camp picture shows the shared world as it is now. Click the trees to gather wood, the rocks for stone, the dark forest edge to hunt, the fire to stand guard or rest, a tent to sleep or wake, a boat to sail away, and an animal to attack it. Glowing places are the moves you can make now; every move is also a button below.</p>
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
  <script type="module" src="/4bd43b978eaea51a6c72/js/app.js"></script>
  <script type="module" src="/4bd43b978eaea51a6c72/js/survive.js"></script>
</body>
</html>
```

</details>

### 3. Scene module is served with phone-sized hit areas

<details><summary>417 lines</summary>

```text
HTTP 200 
X-Request-Id: 1ee1f985-9f39-4575-93e5-4848ff56d105
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792199282
Cache-Control: max-age=3600, public
Last-Modified: Sat, 17 Oct 2026 01:01:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 16872
Date: Sat, 17 Oct 2026 01:07:02 GMT
Connection: close

/**
 * Draws the Survive camp as an SVG scene from the server snapshot. Display and transport only:
 * the Java world owns every rule, and hotspots carry the same actions as the buttons.
 */
const SVG_NS = 'http://www.w3.org/2000/svg';
const PHASES = ['DAY', 'DUSK', 'NIGHT'];
const PHASE_NAMES = { DAY: 'Day', DUSK: 'Dusk', NIGHT: 'Night' };
/** Phase lengths in seconds, used only to place the sun or moon along its arc. */
const PHASE_SECONDS = { DAY: 840, DUSK: 240, NIGHT: 360 };
/** Full health of each animal, used only to scale the health bar. */
const ENEMY_FULL_HEALTH = { HOG: 5, WOLF: 8, BEAR: 14 };
const ENEMY_NAMES = { HOG: 'hog', WOLF: 'wolf', BEAR: 'bear' };
const WEAPON_NAMES = { CLUB: 'club', STONE_AXE: 'stone axe', SPEAR: 'spear' };
const MAX_TENTS = 6;
const MAX_BOATS = 3;
const MAX_OTHER_SURVIVORS = 7;
const HEALTH_BAR_WIDTH = 100;
const LAYER_NAMES = ['sky', 'celestial', 'land', 'camp', 'survivors', 'enemy', 'effects', 'hotspots'];

const TENT_SLOTS = [[430, 330, 1], [535, 330, 1], [640, 330, 1], [480, 285, 0.8], [585, 285, 0.8], [690, 285, 0.8]];
const BOAT_SLOTS = [[800, 455], [880, 480], [820, 510]];
const SURVIVOR_SLOTS = [[470, 468], [440, 505], [502, 510], [728, 505], [760, 468], [410, 470], [700, 525]];
const PLAYER_SLOT = [680, 468];
const PLAYER_COMBAT_SLOT = [480, 470];
const PINES = [
  [30, 330, 130], [85, 345, 150], [140, 325, 120], [195, 350, 160], [250, 335, 135], [300, 345, 125],
  [55, 380, 120], [115, 390, 135], [170, 385, 125], [225, 395, 140], [280, 388, 115],
];
const ROCKS = [
  'M50 505 L80 455 L130 445 L160 480 L150 510 Z',
  'M140 512 L170 470 L215 462 L250 490 L240 515 Z',
  'M225 518 L250 488 L285 486 L300 510 Z',
];
const STARS = Array.from({ length: 28 }, (_, index) => [(index * 137 + 41) % 940 + 10, (index * 53 + 17) % 200 + 10]);

/**
 * Hit areas whose smaller side is at least 145 scene units: 44 CSS pixels when the scene is 300 pixels
 * wide, as it is inside the adventure panel on a 375-pixel-wide phone.
 */
const HOTSPOTS = {
  trees: { x: 0, y: 160, width: 318, height: 235 },
  rocks: { x: 30, y: 395, width: 280, height: 145 },
  forestEdge: { x: 318, y: 222, width: 145, height: 145 },
  tents: { x: 420, y: 200, width: 350, height: 145 },
  fire: { x: 518, y: 395, width: 145, height: 145 },
  boats: { x: 780, y: 395, width: 180, height: 145 },
  enemy: { x: 318, y: 375, width: 145, height: 160 },
};

const sceneMemory = new WeakMap();

/** Redraws the layers whose inputs changed since the last render of this SVG. */
export function renderSurviveScene(documentRoot, svgRoot, state, pending = false) {
  const memory = memoryFor(documentRoot, svgRoot);
  const draw = drawingKit(documentRoot);
  svgRoot.dataset.phase = phaseOf(state);
  svgRoot.setAttribute('aria-label', describeScene(state));
  svgRoot.setAttribute('class', pending ? 'survive-scene is-pending' : 'survive-scene');
  const layerViews = {
    sky: { phase: phaseOf(state) },
    celestial: celestialView(state),
    land: {},
    camp: campView(state),
    survivors: survivorsView(state),
    enemy: enemyView(state),
    effects: effectsView(state),
    hotspots: hotspotsView(state),
  };
  for (const name of LAYER_NAMES) {
    const signature = JSON.stringify(layerViews[name]);
    if (memory.signatures.get(name) !== signature) {
      memory.signatures.set(name, signature);
      memory.layers.get(name).replaceChildren(...LAYER_DRAWERS[name](draw, layerViews[name]));
    }
  }
}

/** A sentence-by-sentence account of the scene for screen readers. */
export function describeScene(state) {
  const sentences = [
    `${PHASE_NAMES[phaseOf(state)]}, day ${state.day}.`,
    `${countOf(state.shelters, 'shelter')}, ${countOf(state.boats, 'boat')}, `
      + `${countOf(state.survivors.length, 'survivor')} at camp.`,
    playerSentence(state),
  ];
  if (state.weapon) {
    sentences.push(`You hold a ${WEAPON_NAMES[state.weapon] ?? 'weapon'}.`);
  }
  return sentences.join(' ');
}

function playerSentence(state) {
  switch (state.status) {
    case 'COMBAT': {
      const enemyName = ENEMY_NAMES[state.enemy] ? `A ${ENEMY_NAMES[state.enemy]}` : 'A wild animal';
      return `${enemyName} with ${state.enemyHealth} health blocks your path.`;
    }
    case 'SLEEPING':
      return 'You are asleep in a shelter.';
    case 'DEAD':
      return 'You have died.';
    case 'ESCAPED':
      return 'You sailed away from the island.';
    default:
      return state.guarding ? 'You stand guard by the fire.' : 'You are at camp.';
  }
}

function countOf(count, singular) {
  return `${count} ${count === 1 ? singular : `${singular}s`}`;
}

function phaseOf(state) {
  return PHASES.includes(state.phase) ? state.phase : 'DAY';
}

function memoryFor(documentRoot, svgRoot) {
  if (!sceneMemory.has(svgRoot)) {
    const layers = new Map(LAYER_NAMES.map(name => {
      const layer = documentRoot.createElementNS(SVG_NS, 'g');
      layer.setAttribute('class', `scene-layer scene-layer-${name}`);
      svgRoot.appendChild(layer);
      return [name, layer];
    }));
    layers.get('hotspots').setAttribute('aria-hidden', 'true');
    svgRoot.setAttribute('viewBox', '0 0 960 540');
    sceneMemory.set(svgRoot, { layers, signatures: new Map() });
  }
  return sceneMemory.get(svgRoot);
}

/** Element and text factories bound to one document; values only ever reach attributes and text nodes. */
function drawingKit(documentRoot) {
  const shape = (tagName, attributes = {}, ...children) => {
    const element = documentRoot.createElementNS(SVG_NS, tagName);
    for (const [name, value] of Object.entries(attributes)) {
      element.setAttribute(name, String(value));
    }
    for (const child of children) {
      element.appendChild(child);
    }
    return element;
  };
  const label = (text, x, y, className) => {
    const element = shape('text', { x, y, class: className, 'text-anchor': 'middle' });
    element.textContent = text;
    return element;
  };
  return { shape, label };
}

function celestialView(state) {
  const phase = phaseOf(state);
  const phaseSeconds = PHASE_SECONDS[phase];
  const elapsedFraction = 1 - Math.min(phaseSeconds, Math.max(0, state.secondsToNextPhase)) / phaseSeconds;
  return { phase, progress: Math.round(elapsedFraction * 100) / 100 };
}

function campView(state) {
  return {
    tents: Math.min(state.shelters, MAX_TENTS),
    extraTents: Math.max(0, state.shelters - MAX_TENTS),
    boats: Math.min(state.boats, MAX_BOATS),
    extraBoats: Math.max(0, state.boats - MAX_BOATS),
    night: phaseOf(state) !== 'DAY',
  };
}

function survivorsView(state) {
  const others = Math.max(0, state.survivors.length - 1);
  return {
    others: Math.min(others, MAX_OTHER_SURVIVORS),
    extraOthers: Math.max(0, others - MAX_OTHER_SURVIVORS),
    name: state.name,
    status: state.status,
    guarding: state.status === 'EXPLORING' && state.guarding,
    weapon: state.weapon ?? null,
  };
}

function enemyView(state) {
  if (state.status !== 'COMBAT') {
    return null;
  }
  const fullHealth = Math.max(ENEMY_FULL_HEALTH[state.enemy] ?? state.enemyHealth, state.enemyHealth, 1);
  return { kind: state.enemy, healthWidth: Math.round(HEALTH_BAR_WIDTH * state.enemyHealth / fullHealth) };
}

function effectsView(state) {
  const newestEvent = state.events.at(-1) ?? '';
  const isRaid = newestEvent.includes('raiders');
  return { raid: isRaid ? newestEvent : null, burned: isRaid && newestEvent.includes('destroyed') };
}

function hotspotsView(state) {
  const fireAction = state.actions.includes('GUARD') ? 'GUARD' : 'REST';
  const tentAction = state.status === 'SLEEPING' ? 'WAKE' : 'SLEEP';
  const placements = [
    ['GATHER', HOTSPOTS.trees], ['GATHER_STONE', HOTSPOTS.rocks], ['HUNT', HOTSPOTS.forestEdge],
    [tentAction, HOTSPOTS.tents], [fireAction, HOTSPOTS.fire], ['ESCAPE', HOTSPOTS.boats],
  ];
  if (state.status === 'COMBAT') {
    placements.push(['ATTACK', HOTSPOTS.enemy]);
  }
  return placements.map(([action, area]) => ({ action, area, available: state.actions.includes(action) }));
}

function drawSky({ shape }, view) {
  const shapes = [
    shape('defs', {},
      shape('linearGradient', { id: 'surviveSkyGradient', x1: 0, y1: 0, x2: 0, y2: 1 },
        shape('stop', { offset: '0%', class: 'scene-sky-top' }),
        shape('stop', { offset: '100%', class: 'scene-sky-bottom' }))),
    shape('rect', { x: 0, y: 0, width: 960, height: 540, fill: 'url(#surviveSkyGradient)', class: 'scene-sky' }),
  ];
  if (view.phase === 'NIGHT') {
    STARS.forEach(([x, y], index) => {
      shapes.push(shape('circle', { cx: x, cy: y, r: 1.6, class: 'scene-star', style: `animation-delay: ${(index % 6) * 0.7}s` }));
    });
  }
  shapes.push(shape('path', { d: 'M0 330 Q160 250 330 300 T640 280 T960 300 L960 540 L0 540 Z', class: 'scene-hill-far' }));
  return shapes;
}

function drawCelestial({ shape }, view) {
  const x = 80 + view.progress * 800;
  const y = 190 - Math.sin(view.progress * Math.PI) * 120;
  const body = view.phase === 'NIGHT'
    ? shape('circle', { cx: x, cy: y, r: 22, class: 'scene-moon' })
    : shape('circle', { cx: x, cy: y + (view.phase === 'DUSK' ? 40 : 0), r: 28, class: 'scene-sun' });
  return [shape('path', { d: 'M80 190 Q480 -50 880 190', class: 'scene-phase-arc' }), body];
}

function drawLand({ shape }) {
  const shapes = [
    shape('path', { d: 'M0 380 Q240 340 480 370 T780 365 L780 540 L0 540 Z', class: 'scene-ground' }),
    shape('path', { d: 'M805 385 Q880 378 960 372 L960 540 L748 540 Q770 450 805 385 Z', class: 'scene-water' }),
    shape('path', { d: 'M748 540 Q770 450 805 385', class: 'scene-shore' }),
    shape('path', { d: 'M332 392 Q336 300 390 268 Q444 300 448 392 Z', class: 'scene-forest-edge' }),
    shape('path', { d: 'M362 392 Q372 340 390 326 Q408 340 418 392 Z', class: 'scene-trail' }),
  ];
  for (const [x, base, height] of PINES) {
    const halfWidth = height * 0.28;
    shapes.push(shape('rect', { x: x - 4, y: base - 14, width: 8, height: 16, class: 'scene-trunk' }));
    shapes.push(shape('path', { d: `M${x - halfWidth} ${base - 10} L${x} ${base - height} L${x + halfWidth} ${base - 10} Z`, class: 'scene-pine' }));
  }
  for (const outline of ROCKS) {
    shapes.push(shape('path', { d: outline, class: 'scene-rock' }));
  }
  return shapes;
}

function drawCamp({ shape, label }, view) {
  const shapes = [];
  TENT_SLOTS.slice(0, view.tents).forEach(([x, base, scale]) => {
    const width = 90 * scale;
    const height = 70 * scale;
    shapes.push(shape('g', { class: 'scene-tent' },
      shape('path', { d: `M${x} ${base} L${x + width / 2} ${base - height} L${x + width} ${base} Z`, class: 'scene-tent-canvas' }),
      shape('path', { d: `M${x + width / 2 - 9 * scale} ${base} L${x + width / 2} ${base - 28 * scale} L${x + width / 2 + 9 * scale} ${base} Z`, class: 'scene-tent-door' })));
  });
  if (view.extraTents > 0) {
    shapes.push(label(`+${view.extraTents}`, 770, 250, 'scene-count'));
  }
  BOAT_SLOTS.slice(0, view.boats).forEach(([x, y]) => {
    shapes.push(shape('g', { class: 'scene-boat' },
      shape('path', { d: `M${x} ${y} L${x + 60} ${y} L${x + 50} ${y + 14} L${x + 10} ${y + 14} Z`, class: 'scene-hull' }),
      shape('path', { d: `M${x + 30} ${y} L${x + 30} ${y - 38} L${x + 52} ${y - 6} Z`, class: 'scene-sail' })));
  });
  if (view.extraBoats > 0) {
    shapes.push(label(`+${view.extraBoats}`, 935, 445, 'scene-count'));
  }
  shapes.push(shape('g', { class: 'scene-fire' },
    shape('circle', { cx: 590, cy: 470, r: view.night ? 70 : 40, class: 'scene-fire-glow' }),
    shape('path', { d: 'M555 495 L625 475 M555 475 L625 495', class: 'scene-logs' }),
    shape('path', { d: 'M570 488 Q575 450 590 430 Q605 450 610 488 Z', class: 'scene-flame' }),
    shape('path', { d: 'M580 488 Q584 462 592 450 Q600 465 600 488 Z', class: 'scene-flame-core' })));
  return shapes;
}

function figure({ shape }, [x, y], className) {
  return shape('g', { class: className },
    shape('rect', { x: x - 12, y: y - 46, width: 24, height: 46, rx: 9, class: 'scene-body' }),
    shape('circle', { cx: x, cy: y - 59, r: 13, class: 'scene-head' }));
}

function weaponShape({ shape }, weapon, [x, y]) {
  switch (weapon) {
    case 'CLUB':
      return shape('path', { d: `M${x + 10} ${y - 20} L${x + 22} ${y - 44}`, class: 'scene-weapon scene-weapon-club' });
    case 'STONE_AXE':
      return shape('g', { class: 'scene-weapon scene-weapon-axe' },
        shape('path', { d: `M${x + 10} ${y - 18} L${x + 20} ${y - 48}`, class: 'scene-weapon-shaft' }),
        shape('path', { d: `M${x + 16} ${y - 50} L${x + 30} ${y - 46} L${x + 24} ${y - 38} Z`, class: 'scene-weapon-head' }));
    case 'SPEAR':
      return shape('g', { class: 'scene-weapon scene-weapon-spear' },
        shape('path', { d: `M${x + 12} ${y - 6} L${x + 26} ${y - 68}`, class: 'scene-weapon-shaft' }),
        shape('path', { d: `M${x + 22} ${y - 66} L${x + 28} ${y - 80} L${x + 30} ${y - 64} Z`, class: 'scene-weapon-head' }));
    default:
      return null;
  }
}

function drawSurvivors(draw, view) {
  const { shape, label } = draw;
  const shapes = SURVIVOR_SLOTS.slice(0, view.others).map(slot => figure(draw, slot, 'scene-survivor'));
  if (view.extraOthers > 0) {
    shapes.push(label(`+${view.extraOthers}`, 410, 420, 'scene-count'));
  }
  const [x, y] = view.status === 'COMBAT' ? PLAYER_COMBAT_SLOT : PLAYER_SLOT;
  switch (view.status) {
    case 'SLEEPING':
      shapes.push(label('z z', 590, 250, 'scene-sleep'));
      break;
    case 'DEAD':
      shapes.push(shape('path', { d: `M${x - 14} ${y} L${x - 14} ${y - 30} Q${x} ${y - 46} ${x + 14} ${y - 30} L${x + 14} ${y} Z`, class: 'scene-grave' }));
      shapes.push(label(view.name, x, y - 54, 'scene-name'));
      break;
    case 'ESCAPED':
      shapes.push(shape('g', { class: 'scene-escape-boat' },
        shape('path', { d: 'M880 420 L940 420 L930 434 L890 434 Z', class: 'scene-hull' }),
        shape('path', { d: 'M910 420 L910 380 L934 414 Z', class: 'scene-sail' })));
      shapes.push(label(view.name, 910, 370, 'scene-name'));
      break;
    default: {
      shapes.push(figure(draw, [x, y], 'scene-player'));
      const weapon = weaponShape(draw, view.weapon, [x, y]);
      if (weapon) {
        shapes.push(weapon);
      }
      if (view.guarding) {
        shapes.push(shape('g', { class: 'scene-torch' },
          shape('path', { d: `M${x - 12} ${y - 14} L${x - 18} ${y - 52}`, class: 'scene-torch-stick' }),
          shape('circle', { cx: x - 18, cy: y - 58, r: 7, class: 'scene-flame' })));
      }
      shapes.push(label(view.name, x, y - 82, 'scene-name'));
    }
  }
  return shapes;
}

const EYE_POSITIONS = {
  hog: { cx: 430, cy: 470 }, wolf: { cx: 434, cy: 455 }, bear: { cx: 440, cy: 441 }, unknown: { cx: 420, cy: 470 },
};

function drawEnemy({ shape }, view) {
  if (!view) {
    return [];
  }
  const kind = ENEMY_NAMES[view.kind] ? view.kind.toLowerCase() : 'unknown';
  const silhouettes = {
    hog: [shape('ellipse', { cx: 390, cy: 480, rx: 34, ry: 20 }), shape('circle', { cx: 425, cy: 474, r: 13 })],
    wolf: [shape('ellipse', { cx: 385, cy: 470, rx: 40, ry: 15 }), shape('path', { d: 'M418 466 L446 456 L436 448 L430 438 L424 452 Z' }),
      shape('path', { d: 'M355 480 L352 505 M372 482 L370 505 M398 482 L400 505 M415 478 L418 505', class: 'scene-legs' })],
    bear: [shape('ellipse', { cx: 385, cy: 465, rx: 50, ry: 32 }), shape('circle', { cx: 432, cy: 445, r: 20 }),
      shape('circle', { cx: 440, cy: 426, r: 7 })],
    unknown: [shape('ellipse', { cx: 390, cy: 475, rx: 40, ry: 22 })],
  };
  return [
    shape('g', { class: `scene-enemy scene-enemy-${kind}` }, ...silhouettes[kind]),
    shape('circle', { ...EYE_POSITIONS[kind], r: 3.5, class: 'scene-eye' }),
    shape('rect', { x: 340, y: 395, width: HEALTH_BAR_WIDTH, height: 8, rx: 4, class: 'scene-enemy-health-track' }),
    shape('rect', { x: 340, y: 395, width: view.healthWidth, height: 8, rx: 4, class: 'scene-enemy-health' }),
  ];
}

function drawEffects({ shape }, view) {
  if (!view.raid) {
    return [];
  }
  const shapes = [shape('rect', { x: 0, y: 0, width: 960, height: 540, class: 'scene-raid-flash' })];
  if (view.burned) {
    for (const [x, delay] of [[470, 0], [560, 0.4], [650, 0.8]]) {
      shapes.push(shape('circle', { cx: x, cy: 280, r: 24, class: 'scene-smoke', style: `animation-delay: ${delay}s` }));
    }
  }
  return shapes;
}

function drawHotspots({ shape }, placements) {
  return placements.map(({ action, area, available }) => {
    const hitArea = shape('rect', { ...area, rx: 18, class: available ? 'scene-hotspot is-available' : 'scene-hotspot' });
    hitArea.dataset.action = action;
    return hitArea;
  });
}

const LAYER_DRAWERS = {
  sky: drawSky,
  celestial: drawCelestial,
  land: drawLand,
  camp: drawCamp,
  survivors: drawSurvivors,
  enemy: drawEnemy,
  effects: drawEffects,
  hotspots: drawHotspots,
};
```

</details>

### 4. Scene styles include the reduced-motion overrides

<details><summary>160 lines</summary>

```text
HTTP 200 
X-Request-Id: 60d91811-8951-4496-8629-a70089d31da4
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792199283
Cache-Control: max-age=3600, public
Last-Modified: Sat, 17 Oct 2026 01:01:35 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/css
Content-Length: 11738
Date: Sat, 17 Oct 2026 01:07:03 GMT
Connection: close

.survive-main { max-width: 1180px; margin: 0 auto; padding: 40px 24px 64px; color: #e9ebe4; }
.survive-hero { padding: 36px 0 40px; border-bottom: 1px solid #384139; margin-bottom: 28px; background: radial-gradient(ellipse at 80% 50%, #1b382940, transparent 65%); }
.survive-eyebrow { color: #adc6a9; font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .16em; margin: 0 0 14px; }
.survive-hero h1 { font-family: Georgia, serif; font-size: clamp(3.5rem, 10vw, 6.5rem); letter-spacing: -.05em; line-height: 1; margin: 0 0 24px; }
.survive-hero h1 span { color: #e9ad75; }
.survive-hero > p:not(.survive-eyebrow) { color: #b8c0b6; font-size: 1.1rem; }
.survive-intro { margin-top: 22px; color: #e9ad75; font-family: monospace; }
.survive-intro > span { font-size: 1.6rem; margin-right: 12px; }
.survive-grid { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(280px, 1fr); gap: 20px; align-items: start; }
.survive-panel { background: #141c18; border: 1px solid #344238; border-radius: 14px; padding: 26px; }
.survive-panel h2 { font-family: Georgia, serif; font-size: 1.55rem; margin-bottom: 22px; }
.survive-panel h3 { font-size: .87rem; color: #c7d5c5; margin: 22px 0 12px; }
.survive-panel h3 span { float: right; font-family: monospace; }
.survive-section-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }
.survive-badge { border: 1px solid #607659; color: #c7d9b4; font-size: .7rem; padding: 5px 9px; border-radius: 30px; }
.survive-message { color: #ebd6bf; min-height: 88px; font-size: 1.1rem; line-height: 1.7; border-left: 2px solid #d39d6c; padding-left: 18px; }
.survive-actions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.survive-page button { border: 1px solid #52664c; background: #243222; color: #eef4e8; border-radius: 9px; padding: 13px 16px; font: inherit; text-align: left; cursor: pointer; }
.survive-page button:hover:not(:disabled) { background: #34482d; border-color: #9ba985; }
.survive-page button:focus-visible, .survive-page input:focus-visible, .survive-page select:focus-visible, .survive-guide summary:focus-visible { outline: 3px solid #f2b779; outline-offset: 3px; }
.survive-page button:disabled { opacity: .42; cursor: not-allowed; }
.survive-actions small { display: block; font-size: .69rem; color: #b9c2ae; margin-top: 6px; line-height: 1.5; }
.survive-secondary { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 26px; padding-top: 20px; border-top: 1px solid #344238; }
.survive-secondary button { padding: 8px 12px; background: transparent; color: #bfcab9; font-size: .8rem; }
.survive-sidebar { display: grid; gap: 20px; }
.survive-health-label { display: flex; justify-content: space-between; font-size: .8rem; margin-bottom: 8px; }
.survive-page meter { width: 100%; height: 14px; accent-color: #a9c879; }
.survive-stats { margin: 16px 0 0; }
.survive-stats > div { display: flex; justify-content: space-between; gap: 10px; padding: 8px 0; border-bottom: 1px solid #2d372f; font-size: .86rem; }
.survive-stats dt { font-weight: 400; color: #b8c1b3; }
.survive-stats dd { font-family: monospace; margin: 0; color: #f0dbc0; }
.survive-players { list-style: none; padding: 0; display: flex; gap: 6px; flex-wrap: wrap; max-height: 140px; overflow-y: auto; }
.survive-players li { font-size: .75rem; background: #273125; border-radius: 6px; padding: 5px 9px; overflow-wrap: anywhere; }
.survive-journal { grid-column: 1 / -1; }
.survive-journal ol { list-style: none; padding: 0; margin: 0; max-height: 280px; overflow-y: auto; }
.survive-journal li { padding: 12px 0; border-bottom: 1px solid #2d372f; color: #bfc9b7; font-size: .83rem; line-height: 1.7; overflow-wrap: anywhere; }
.survive-journal li:first-child { color: #ead3b4; }
.survive-join { display: flex; align-items: end; gap: 14px; flex-wrap: wrap; margin-bottom: 24px; }
.survive-join > div { width: 100%; }
.survive-join h2 { margin-bottom: 12px; }
.survive-join p { color: #b8c1b3; margin: 0; }
.survive-join label { align-self: center; font-size: .85rem; }
.survive-join input { border: 1px solid #52664c; border-radius: 9px; color: #eef4e8; background: #0f1712; padding: 13px; min-width: 0; max-width: 100%; }
.survive-page .survive-primary { background: #d4a075; color: #1b211a; border-color: #d4a075; font-weight: 700; }
.survive-enemy { display: flex; justify-content: space-between; padding: 16px; margin-bottom: 24px; border: 1px solid #9d6156; border-radius: 8px; color: #f1b29f; }
.survive-clock { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px; padding: 10px 14px; margin: 0 0 18px; border: 1px solid #5d6f7e; border-radius: 8px; color: #d6e2ea; }
.survive-clock[data-phase="DUSK"] { border-color: #a8774f; color: #f1cfa4; }
.survive-clock[data-phase="NIGHT"] { border-color: #6c6aa0; color: #c9c7f2; background: rgba(28, 26, 58, .45); }
.survive-countdown { margin-left: auto; font-variant-numeric: tabular-nums; }
.survive-warning { color: #f1c0a4; font-size: .85rem; margin: 6px 0 0; }
.survive-notice { color: #f1c0a4; border: 1px solid #946b58; padding: 18px; border-radius: 10px; }
.survive-guide { margin-top: 24px; color: #bdc7b8; line-height: 1.8; font-size: .88rem; }
.survive-guide summary { color: #e0ceb2; cursor: pointer; font-weight: 600; }
.survive-guide p { margin: 18px 0 0; }
.survive-muted, .survive-attribution { font-size: .73rem; color: #acb5a6; line-height: 1.7; }
.survive-attribution { margin-top: 24px; }
.survive-attribution a { color: #e7b582; }
.survive-gift { display: grid; gap: 10px; border-top: 1px solid #344238; margin-top: 20px; padding-top: 4px; }
.survive-gift label { display: block; font-size: .8rem; color: #c7d5c5; margin-bottom: 4px; }
.survive-gift select, .survive-gift input { width: 100%; min-width: 0; padding: 10px; border: 1px solid #52664c; border-radius: 9px; background: #0f1712; color: #eef4e8; font: inherit; }
.survive-gift select:disabled, .survive-gift input:disabled { opacity: .5; }
.survive-gift-amount { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 10px; }
.survive-page [hidden] { display: none !important; }
@media (max-width: 760px) {
  .survive-main { padding: 18px 16px 40px; }
  .survive-hero { padding: 24px 0; }
  .survive-grid { grid-template-columns: 1fr; }
  .survive-panel { padding: 20px; }
  .survive-sidebar { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .survive-section-heading { flex-wrap: wrap; }
}
@media (max-width: 500px) {
  .survive-sidebar { grid-template-columns: 1fr; }
  .survive-actions { grid-template-columns: 1fr; }
  .survive-join input, .survive-join .survive-primary { width: 100%; }
}

/* Camp scene: palettes follow the shared phase; hotspots glow only for moves the server allows. */
.survive-scene { display: block; width: 100%; height: auto; aspect-ratio: 16 / 9; margin: 0 0 18px; border-radius: 10px; border: 1px solid #3f4f3b; overflow: hidden;
  --sky-top: #8fc4e8; --sky-bottom: #d9eef7; --hill-far: #6f9a7a; --ground: #5d7d45; --pine: #2f5a3a; --forest-edge: #1f3324; --rock: #8c8f93; --water: #4f8fb3; --shore: #c9b58a; --tent: #d9a066; --tent-door: #7a4b2a; --figure: #e4d5bd; --name-stroke: #10170f; }
.survive-scene[data-phase="DUSK"] { --sky-top: #e98a5a; --sky-bottom: #f6c98a; --hill-far: #8a6a6a; --ground: #5a5a3c; --pine: #2c3f2c; --forest-edge: #1a2419; --rock: #7d7470; --water: #6a6f9c; --shore: #b39a78; --tent: #c88b5e; }
.survive-scene[data-phase="NIGHT"] { --sky-top: #0d1330; --sky-bottom: #26305a; --hill-far: #1f2a3f; --ground: #1d2a22; --pine: #12221a; --forest-edge: #070d0a; --rock: #4d5260; --water: #1d3550; --shore: #4a4637; --tent: #8a6a52; --tent-door: #3b2618; --figure: #b9b3c9; }
.scene-sky-top { stop-color: var(--sky-top); }
.scene-sky-bottom { stop-color: var(--sky-bottom); }
.scene-hill-far { fill: var(--hill-far); }
.scene-ground { fill: var(--ground); }
.scene-water { fill: var(--water); }
.scene-shore { fill: none; stroke: var(--shore); stroke-width: 16; stroke-linecap: round; }
.scene-trail { fill: #0b120d; opacity: .8; }
.scene-forest-edge { fill: var(--forest-edge); }
.scene-pine { fill: var(--pine); }
.scene-trunk { fill: #5a3b22; }
.scene-rock { fill: var(--rock); stroke: rgba(0, 0, 0, .25); stroke-width: 2; }
.scene-star { fill: #f4f1d0; animation: scene-twinkle 3.6s ease-in-out infinite; }
.scene-sun { fill: #ffd76a; }
.survive-scene[data-phase="DUSK"] .scene-sun { fill: #ff9f4a; }
.scene-moon { fill: #e9e6d2; }
.scene-phase-arc { fill: none; stroke: rgba(255, 255, 255, .25); stroke-width: 2; stroke-dasharray: 4 8; }
.scene-tent-canvas { fill: var(--tent); stroke: rgba(0, 0, 0, .3); stroke-width: 2; }
.scene-tent-door { fill: var(--tent-door); }
.scene-hull { fill: #6b4527; }
.scene-sail { fill: #efe6d0; }
.scene-logs { stroke: #4a2e1a; stroke-width: 7; stroke-linecap: round; }
.scene-fire-glow { fill: rgba(255, 170, 70, .18); }
.survive-scene[data-phase="NIGHT"] .scene-fire-glow { fill: rgba(255, 160, 60, .32); }
.scene-flame { fill: #ff8a2a; transform-box: fill-box; transform-origin: 50% 100%; animation: scene-flicker 1.1s ease-in-out infinite alternate; }
.scene-flame-core { fill: #ffd76a; }
.scene-head, .scene-body { fill: var(--figure); }
.scene-player .scene-head, .scene-player .scene-body { fill: #f0b46a; stroke: #fff4dd; stroke-width: 2; }
.scene-name { fill: #fffaf0; font: 600 18px system-ui, sans-serif; paint-order: stroke; stroke: var(--name-stroke); stroke-width: 4px; stroke-linejoin: round; }
.scene-count { fill: #fffaf0; font: 700 20px system-ui, sans-serif; paint-order: stroke; stroke: var(--name-stroke); stroke-width: 4px; }
.scene-sleep { fill: #dfe6ff; font: 700 26px system-ui, sans-serif; letter-spacing: 4px; animation: scene-drift 2.4s ease-in-out infinite; }
.scene-grave { fill: #9a9a9a; stroke: #555; stroke-width: 2; }
.scene-weapon path, .scene-weapon-club, .scene-weapon-shaft, .scene-torch-stick { stroke: #6b4527; stroke-width: 5; stroke-linecap: round; fill: none; }
.scene-weapon-head { fill: #a9adb3; stroke: #555; stroke-width: 1; }
.scene-weapon-club { stroke-width: 8; }
.scene-enemy { fill: #3a2a22; }
.scene-enemy-wolf { fill: #5a5f66; }
.scene-enemy-bear { fill: #4a3020; }
.survive-scene[data-phase="NIGHT"] .scene-enemy { stroke: #cdbb9e; stroke-width: 2; }
.scene-eye { fill: #ffd23a; }
.scene-legs { fill: none; stroke: #5a5f66; stroke-width: 5; stroke-linecap: round; }
.scene-enemy-health-track { fill: rgba(0, 0, 0, .45); }
.scene-enemy-health { fill: #e0604a; }
.scene-raid-flash { fill: #ff7a2a; opacity: 0; animation: scene-raid 1.6s ease-out 1; }
.scene-smoke { fill: rgba(70, 70, 70, .55); animation: scene-smoke 3s ease-out infinite; }
.scene-hotspot { fill: transparent; stroke: transparent; stroke-width: 3; pointer-events: none; }
.scene-hotspot.is-available { pointer-events: all; cursor: pointer; }
.scene-hotspot.is-available:hover { fill: rgba(255, 240, 200, .14); stroke: rgba(255, 230, 170, .75); }
.survive-scene.is-pending .scene-hotspot { pointer-events: none; }
@keyframes scene-twinkle { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }
@keyframes scene-flicker { from { transform: scaleY(1) skewX(0deg); } to { transform: scaleY(1.12) skewX(3deg); } }
@keyframes scene-drift { 0%, 100% { transform: translateY(0); opacity: 1; } 50% { transform: translateY(-6px); opacity: .6; } }
@keyframes scene-raid { 0% { opacity: .55; } 100% { opacity: 0; } }
@keyframes scene-smoke { 0% { transform: translateY(0); opacity: .7; } 100% { transform: translateY(-60px); opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .scene-star, .scene-flame, .scene-sleep, .scene-raid-flash, .scene-smoke { animation: none; }
  .scene-raid-flash { display: none; }
  .scene-smoke { opacity: .5; }
}
```

</details>

### 5. API survivor Carpenter builds two shelters for the scene to draw

<details><summary>77 lines</summary>

```text
exit code: 0
--- stdout ---
Carpenter: GET /api/survive/v1/game  -> 204 
Carpenter: GET /survive  -> 200 <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  

    <meta name="description" content="Gather, craft, and survive in a shared text adventure world." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/survive" />



    <meta property="og:site_name" content="christopherbell.dev" />
...
Carpenter: POST /api/survive/v1/game {"name": "Carpenter"} -> 200 {"name":"Carpenter","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":1,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp."],"actions":["GATHER","GATHER_STONE","HUNT"],"message":"You arrive at the camp. Gather wood, build togeth...
PASS join succeeds
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":1,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp."],"actions":["GATHER","GATHER_STONE","HUNT"],"message":"You arrive at the camp. Gather wood, build togeth...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":1,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp."],"actions":["GATHER","GATHER_STONE","HUNT"],"message":"You arrive at the camp. Gather wood, build togeth...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 0} -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":2,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!"],"actions":["GATHER","...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":2,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!"],"actions":["GATHER","...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":2,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!"],"actions":["GATHER","...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 1} -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 2} -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":4,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":4,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":1,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":3,"worldRevision":4,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 3} -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":4,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 4} -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":5,"worldRevision":6,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree resi...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":5,"worldRevision":6,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree resi...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":5,"status":"COMBAT","revision":5,"worldRevision":6,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree resi...
Carpenter: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 5} -> 200 {"name":"Carpenter","health":9,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":1,"status":"COMBAT","revision":6,"worldRevision":7,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree resis...
PASS ATTACK returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":9,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":1,"status":"COMBAT","revision":6,"worldRevision":7,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree resis...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":9,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":1,"status":"COMBAT","revision":6,"worldRevision":7,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree resis...
Carpenter: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 6} -> 200 {"name":"Carpenter","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":8,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree re...
PASS ATTACK returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":8,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree re...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":8,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree re...
Carpenter: POST /api/survive/v1/actions {"action": "EAT", "revision": 7} -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":9,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
PASS EAT returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":9,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":2,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":8,"worldRevision":9,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree r...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 8} -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":10,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree ...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":10,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree ...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":3,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":9,"worldRevision":10,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree ...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 9} -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":11,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":11,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":11,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 10} -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":12,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":12,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":12,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 11} -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: POST /api/survive/v1/actions {"action": "GATHER", "revision": 12} -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":13,"worldRevision":14,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
PASS GATHER returned 200, expected 200
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health":10,"strength":4,"stamina":12,"experience":1,"experienceToNextLevel":4,"wood":4,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":13,"worldRevision":14,"shelters":0,"boats":0,"survivors":["Carpenter"],"events":["Carpenter arrived at camp.","Carpenter: You gathered one piece of wood. Your strength and stamina increased!","Carpenter: The tree...
Carpenter: GET /api/survive/v1/game  -> 200 {"name":"Carpenter","health
... [45893 more characters not recorded]
```

</details>

### 6. Read-only query: the candidate wrote only to database test on the disposable mongod

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

## Evidence
- Case 1 started 2026-10-16T20:07:02-05:00, took 31 ms, candidate `8627fff`
- Case 2 started 2026-10-16T20:07:02-05:00, took 187 ms, candidate `8627fff`
- Case 3 started 2026-10-16T20:07:02-05:00, took 46 ms, candidate `8627fff`
- Case 4 started 2026-10-16T20:07:03-05:00, took 31 ms, candidate `8627fff`
- Case 5 started 2026-10-16T20:07:03-05:00, took 2531 ms, candidate `8627fff`
- Case 6 started 2026-10-16T20:07:06-05:00, took 264 ms, candidate `8627fff`

## Bugs / Follow-ups
- Superseded candidate `2d41ee9`: its phone-width check measured the smallest hotspot at 37 px, because the scene is 301 px wide inside the panel on a 375 px phone. Commit `8627fff` grew every hit area to at least 145 scene units, and every case above was rerun on it. The `2d41ee9` evidence is kept in the scratch evidence file and is not counted here.
- One dusk click landed on the stone hotspot after the browser pane resized between the screenshot and the click; it was repeated with fresh coordinates (case 18). This was a test-harness coordinate issue, not a scene defect.
- Reduced motion was verified by the served stylesheet (case 4) and by the loaded `prefers-reduced-motion` rule covering the scene animations; the browser pane cannot emulate the media feature, so the motion-off rendering itself was not observed.
- Cleanup: `Stop-Candidate.ps1` stopped the candidate and mongod and removed their temporary folders; ports 64023 and 64024 have no listeners. All fixtures were created through the application's endpoints.

## Document Status
complete

## Project
christopherbell-dev
