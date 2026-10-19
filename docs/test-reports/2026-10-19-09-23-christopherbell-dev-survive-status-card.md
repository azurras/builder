# Survive status card: Test Report

## Story/Issue
User request 2026-10-19 "the tabs are not a great experience" (too much switching); plan docs/implementation-plans/2026-10-19-09-10-christopherbell-dev-survive-status-card.md

## Branch
`claude/survive-status-card-20261019` at candidate `0112cc7`

## Pass / Fail

> [!TIP]
> 16 of 16 cases passed on candidate `0112cc7`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate is ready and reports its build | ✅ PASS | Expected status below 400 and body containing '"build"' |
| 2 | Survive page serves the status card with the recent events list | ✅ PASS | Expected status below 400 and body containing 'id="surviveRecentEvents"' |
| 3 | Survive page serves the Camp & sharing collapsible section | ✅ PASS | Expected status below 400 and body containing '<details id="surviveSectionCamp"' |
| 4 | Panel module is served | ✅ PASS | Expected status below 400 and body containing 'export function mountPanelSections' |
| 5 | Survive page no longer contains a tab strip | ✅ PASS | Expected exit code 0 |
| 6 | Read-only query: the candidate wrote only to database test on the disposable mongod | ✅ PASS | Expected exit code 0 |
| 7 | API survivor Alice joins the camp as a gift recipient | ✅ PASS | Expected exit code 0 |
| 8 | After joining, the status card shows every field with no clicks; no tab strip; sections start closed | ✅ PASS | Name, guest line, health 10/10, fullness 10/10, wood/food/stone 0, carried 0/10, Bare hands, stats 2 · 10 · 0/1, Recent "Tester arrived at camp."; Camp, Journal and Guide closed; 0 tablists |
| 9 | Menu moves update the card in place: the newest 3 events first, inventory, and a marker on the closed journal | ✅ PASS | Recent equals the server's 3 newest events in order; wood 2, carried 2/10, fullness 7/10; journal marker shown |
| 10 | The Full journal link opens the Journal section and clears its marker | ✅ PASS | Journal open with 4 entries; marker hidden; stored "open"; URL stays /survive |
| 11 | Enter on the Camp summary opens it, and a 5-second poll leaves every section as it was | ✅ PASS | Camp open after Enter; after the poll Camp and Journal open, Guide closed |
| 12 | After a reload the remembered sections are restored | ✅ PASS | Camp open, Journal open, Guide closed |
| 13 | The Camp summary counts survivors, and Give supplies works from the Camp section | ✅ PASS | Summary "0 shelters · 0 boats · 2 survivors"; "You gave 1 wood to Alice."; newest Recent entry is the gift; Camp stays open |
| 14 | Scene hotspots still send moves | ✅ PASS | Clicking the trees: revision 4 to 5, wood gathered |
| 15 | At 375x812 the status card fits, inventory stays on one row and nothing scrolls sideways | ✅ PASS | Card 343 px wide; four 69 px inventory cells on one row; no horizontal scroll |
| 16 | The browser console logged no errors | ✅ PASS | No console messages |

## Test Cases
1. **Candidate is ready and reports its build**: http `GET http://127.0.0.1:56807/actuator/info`
2. **Survive page serves the status card with the recent events list**: http `GET http://127.0.0.1:56807/survive`
3. **Survive page serves the Camp & sharing collapsible section**: http `GET http://127.0.0.1:56807/survive`
4. **Panel module is served**: http `GET http://127.0.0.1:56807/js/survive-panel.js`
5. **Survive page no longer contains a tab strip**: command `python -c "import urllib.request,sys; html=urllib.request.urlopen('http://127.0.0.1:56807/survive').read().decode(); print('tablist present' if 'role=\"tablist\"' in html else 'no tablist'); sys.exit('role=\"tablist\"' in html)"`
6. **Read-only query: the candidate wrote only to database test on the disposable mongod**: command `mongosh --quiet --port 56805 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name)})"`
7. **API survivor Alice joins the camp as a gift recipient**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/status-candidate.json snapshot`

## Browser Cases
Cases 8 to 16 ran in the Claude desktop app's browser pane against `http://127.0.0.1:56807/survive` on 2026-10-19 from 14:21 to 14:27 UTC, by day. Pointer cases used real clicks and keyboard cases used real key presses. After each step, a read-only `GET /api/survive/v1/game` and the page's DOM confirmed the result.

## Automated Checks
- `.\ops\local\Invoke-Gradle.ps1 :website:build :website:bootJar` on `0112cc7`: BUILD SUCCESSFUL, with 2,166 Java tests (0 failed), Checkstyle clean and `jsTest` 426 of 426.
- The panel tests failed before `survive-panel.js` existed and passed once it was written.

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a disposable loopback mongod (port 56805), removed after the run |
| Candidate | website.jar built from the committed HEAD, http://127.0.0.1:56807 |
| Browser | Claude desktop browser pane, 1024x768 and the 375x812 mobile preset |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:56807/actuator/info` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Local command:** `GET http://127.0.0.1:56807/survive` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Local command:** `GET http://127.0.0.1:56807/survive` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Local command:** `GET http://127.0.0.1:56807/js/survive-panel.js` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Local command:** `python -c "import urllib.request,sys; html=urllib.request.urlopen('http://127.0.0.1:56807/survive').read().decode(); print('tablist present' if 'role=\"tablist\"' in html else 'no tablist'); sys.exit('role=\"tablist\"' in html)"` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Local command:** `mongosh --quiet --port 56805 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name)})"` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/status-candidate.json snapshot` in `A:\Projects\christopherbell.dev.worktrees\survive-status`
- **Candidate identity:** `0112cc7`
- **Cleanup:** Stopped the candidate process tree; no fixtures remain.

## Data Sent

### 1. Candidate is ready and reports its build

```http
GET http://127.0.0.1:56807/actuator/info
```

### 2. Survive page serves the status card with the recent events list

```http
GET http://127.0.0.1:56807/survive
```

### 3. Survive page serves the Camp & sharing collapsible section

```http
GET http://127.0.0.1:56807/survive
```

### 4. Panel module is served

```http
GET http://127.0.0.1:56807/js/survive-panel.js
```

### 5. Survive page no longer contains a tab strip

```text
python -c "import urllib.request,sys; html=urllib.request.urlopen('http://127.0.0.1:56807/survive').read().decode(); print('tablist present' if 'role=\"tablist\"' in html else 'no tablist'); sys.exit('role=\"tablist\"' in html)"
```

### 6. Read-only query: the candidate wrote only to database test on the disposable mongod

```text
mongosh --quiet --port 56805 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name)})"
```

### 7. API survivor Alice joins the camp as a gift recipient

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/status-candidate.json snapshot
```

## Response Received

### 1. Candidate is ready and reports its build

```text
HTTP 200 
X-Request-Id: 89d92138-97ae-4554-b401-afd7bd343978
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792419706
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
Date: Mon, 19 Oct 2026 14:20:46 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-10-19T14:13:51.957Z","version":"0.0.0-dev.0112cc7bb267a1dbb205e523342825d7a0eecb0d","group":"christopherbell.dev"}}
```

### 2. Survive page serves the status card with the recent events list

<details><summary>196 lines</summary>

```text
HTTP 200 
X-Request-Id: bc0f9e32-b2f4-40f4-9e40-1e733bbc8758
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792419706
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
Date: Mon, 19 Oct 2026 14:20:46 GMT
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
  <link rel="stylesheet" href="/3d2f59414637ff3e57c0/css/main.css" />
  <link rel="stylesheet" href="/3d2f59414637ff3e57c0/css/survive.css" />
</head>
<body class="site-page void-shell-page survive-page">
  <div id="nav"></div>
  <main class="site-main survive-main">
    <header class="survive-hero">
      <p class="survive-eyebrow">A shared world · A text adventure</p>
      <h1>Survive<span aria-hidden="true">.</span></h1>
      <p>Gather, build and make it through the nights together.</p>
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
        <div class="survive-section-heading">
          <div id="surviveClock" class="survive-clock" data-phase="DAY" role="group" aria-label="World time">
            <strong id="survivePhase">Day</strong><span id="surviveDay"></span>
            <span class="survive-countdown"><span id="surviveNextPhase">Dusk in</span> <strong id="surviveCountdown"></strong></span>
          </div>
          <span id="surviveStatus" class="survive-badge"></span>
        </div>
        <svg id="surviveCampScene" class="survive-scene" role="img" aria-label="The camp" viewBox="0 0 960 540"></svg>
        <h2 id="surviveScene">At the edge of the wilderness</h2>
        <p id="surviveMessage" class="survive-message" role="status" aria-live="polite" aria-atomic="true"></p>
        <div id="surviveEnemy" class="survive-enemy" hidden><strong id="surviveEnemyName">Wild hog</strong><span id="surviveEnemyHealth"></span></div>
        <div id="surviveActionBar" class="survive-action-bar">
          <div id="surviveMenus" class="survive-menus" role="group" aria-label="Moves">
          <div class="survive-menu">
            <button type="button" id="surviveMenuExploreButton" class="survive-menu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuExplore" data-menu-button>Explore <span class="survive-menu-count" data-menu-count>0</span></button>
            <div id="surviveMenuExplore" class="survive-menu-list" role="menu" aria-labelledby="surviveMenuExploreButton" hidden>
              <button type="button" role="menuitem" data-action="GATHER">Gather wood <small>50% chance · +1 wood</small></button>
              <button type="button" role="menuitem" data-action="GATHER_STONE">Gather stone <small>40% chance · +1 stone</small></button>
              <button type="button" role="menuitem" data-action="HUNT">Hunt <small>Hogs by day · Wolves and bears after dark</small></button>
            </div>
          </div>
          <div class="survive-menu">
            <button type="button" id="surviveMenuBuildButton" class="survive-menu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuBuild" data-menu-button>Build <span class="survive-menu-count" data-menu-count>0</span></button>
            <div id="surviveMenuBuild" class="survive-menu-list" role="menu" aria-labelledby="surviveMenuBuildButton" hidden>
              <button type="button" role="menuitem" data-action="BUILD_SHELTER">Build shelter <small>5 wood · Two beds for the camp</small></button>
              <button type="button" role="menuitem" data-action="BUILD_BOAT">Build boat <small>10 wood · One escape</small></button>
              <button type="button" role="menuitem" id="surviveCraftButton" class="survive-submenu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuCraft" data-submenu-button>Craft <small>Weapons from wood and stone</small><span aria-hidden="true">▸</span></button>
              <div id="surviveMenuCraft" class="survive-menu-list survive-submenu" role="menu" aria-labelledby="surviveCraftButton" hidden>
                <button type="button" role="menuitem" data-action="CRAFT_CLUB">Club <small>2 wood · +1 damage · 8 uses</small></button>
                <button type="button" role="menuitem" data-action="CRAFT_AXE">Stone axe <small>2 wood, 2 stone · +2 damage · Better wood gathering</small></button>
                <button type="button" role="menuitem" data-action="CRAFT_SPEAR">Spear <small>3 wood, 3 stone · +3 damage · Reach</small></button>
              </div>
            </div>
          </div>
          <div class="survive-menu">
            <button type="button" id="surviveMenuCampButton" class="survive-menu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuCamp" data-menu-button>Camp <span class="survive-menu-count" data-menu-count>0</span></button>
            <div id="surviveMenuCamp" class="survive-menu-list" role="menu" aria-labelledby="surviveMenuCampButton" hidden>
              <button type="button" role="menuitem" data-action="EAT">Eat food <small>1 food · +5 fullness, +2 health</small></button>
              <button type="button" role="menuitem" data-action="REST">Rest <small>In a shelter · +2 health</small></button>
              <button type="button" role="menuitem" data-action="GUARD">Stand guard <small>Defend the camp from tonight's raid</small></button>
              <button type="button" role="menuitem" data-action="SLEEP">Sleep <small>Uses a shelter bed · Heal through the night</small></button>
              <button type="button" role="menuitem" data-action="ESCAPE">Sail away <small>Use a shared boat · Survive</small></button>
            </div>
          </div>
          </div>
          <div id="surviveDirectActions" class="survive-direct-actions" role="group" aria-label="Moves right now">
            <button type="button" data-action="ATTACK">Attack <small>The animal bites back</small></button>
            <button type="button" data-action="DEFEND">Defend <small>Block the next bite</small></button>
            <button type="button" data-action="FLEE">Flee <small>Return to camp · Take one bite</small></button>
            <button type="button" data-action="WAKE">Wake up <small>Keep the health you have recovered</small></button>
            <button id="surviveStartOver" type="button" class="survive-primary" hidden>Start a new survivor</button>
          </div>
        </div>
      </section>

      <aside class="survive-sidebar" aria-label="Survivor and camp">
        <section class="survive-panel survive-status-card" aria-labelledby="survivePlayerName">
          <div class="survive-status-head"><h2 id="survivePlayerName"></h2><p id="surviveSaveStatus" class="survive-muted" role="status"></p></div>
          <label class="survive-health-label" for="surviveHealth">Health <strong id="surviveHealthText"></strong></label>
          <meter id="surviveHealth" min="0" max="10" low="3" high="7" optimum="10" value="10"></meter>
          <label class="survive-health-label" for="surviveHunger">Fullness <strong id="surviveHungerText"></strong></label>
          <meter id="surviveHunger" min="0" max="10" low="4" high="7" optimum="10" value="10"></meter>
          <p id="surviveHungerWarning" class="survive-warning" role="status" hidden>You are hungry. Eat soon: at 0, every effort costs health.</p>
          <dl class="survive-inventory" aria-label="Inventory">
            <div><dt>Wood</dt><dd id="surviveWood"></dd></div>
            <div><dt>Food</dt><dd id="surviveFood"></dd></div>
            <div><dt>Stone</dt><dd id="surviveStone"></dd></div>
            <div><dt>Carried</dt><dd id="surviveInventoryCount"></dd></div>
          </dl>
          <p class="survive-card-line"><span class="survive-muted">Weapon</span> <strong id="surviveWeapon"></strong></p>
          <p class="survive-card-line survive-muted">Strength <strong id="surviveStrength"></strong> · Stamina <strong id="surviveStamina"></strong> · XP <strong id="surviveExperience"></strong></p>
          <div class="survive-recent-heading"><h3>Recent</h3><a href="#surviveSectionJournal" id="surviveFullJournal">Full journal</a></div>
          <ol id="surviveRecentEvents" class="survive-recent"></ol>
          <div class="survive-card-footer"><span id="survivePublicId" class="survive-muted"></span><span class="survive-secondary"><button id="surviveRefresh" type="button">Refresh world</button><button id="surviveRestart" type="button">New survivor</button></span></div>
        </section>
        <details id="surviveSectionCamp" class="survive-panel survive-section">
          <summary><span class="survive-section-title">Camp &amp; sharing</span> <span id="surviveCampSummary" class="survive-muted"></span></summary>
            <h3 class="survive-panel-title">Shared camp <span class="survive-muted">· One world, built together</span></h3>
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
        </details>
        <details id="surviveSectionJournal" class="survive-panel survive-section">
          <summary><span class="survive-section-title">Journal</span> <span id="surviveJournalUnread" class="survive-unread" hidden><span class="survive-visually-hidden">(new events)</span></span> <span class="survive-muted">Last 30 events, newest first</span></summary>
          <ol id="surviveEvents" reversed></ol>
        </details>
        <details id="surviveSectionGuide" class="survive-panel survive-section survive-guide">
          <summary><span class="survive-section-title">Guide</span> <span class="survive-muted">How to play, costs and odds</span></summary>
      <p>The camp picture shows the shared world as it is now. Click the trees to gather wood, the rocks for stone, the dark forest edge to hunt, the fire to stand guard or rest, a tent to sleep or wake, a boat to sail away, and an animal to attack it. Glowing places are the moves you can make now; every move is also in the menus below the picture.</p>
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
      </aside>
    </div>
    <p class="survive-attribution">Adapted from <a href="https://github.com/azurras/survive">azurras/Survive</a> · Java game engine · <a href="/licenses/survive-MIT.txt">MIT license</a>. Browser adaptation completes the original's unfinished combat and food actions.</p>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/3d2f59414637ff3e57c0/js/app.js"></script>
  <script type="module" src="/3d2f59414637ff3e57c0/js/survive.js"></script>
</body>
</html>
```

</details>

### 3. Survive page serves the Camp & sharing collapsible section

<details><summary>196 lines</summary>

```text
HTTP 200 
X-Request-Id: b9f9f1e7-7a01-4c28-b2f1-04d9ea6b021c
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792419706
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
Date: Mon, 19 Oct 2026 14:20:46 GMT
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
  <link rel="stylesheet" href="/3d2f59414637ff3e57c0/css/main.css" />
  <link rel="stylesheet" href="/3d2f59414637ff3e57c0/css/survive.css" />
</head>
<body class="site-page void-shell-page survive-page">
  <div id="nav"></div>
  <main class="site-main survive-main">
    <header class="survive-hero">
      <p class="survive-eyebrow">A shared world · A text adventure</p>
      <h1>Survive<span aria-hidden="true">.</span></h1>
      <p>Gather, build and make it through the nights together.</p>
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
        <div class="survive-section-heading">
          <div id="surviveClock" class="survive-clock" data-phase="DAY" role="group" aria-label="World time">
            <strong id="survivePhase">Day</strong><span id="surviveDay"></span>
            <span class="survive-countdown"><span id="surviveNextPhase">Dusk in</span> <strong id="surviveCountdown"></strong></span>
          </div>
          <span id="surviveStatus" class="survive-badge"></span>
        </div>
        <svg id="surviveCampScene" class="survive-scene" role="img" aria-label="The camp" viewBox="0 0 960 540"></svg>
        <h2 id="surviveScene">At the edge of the wilderness</h2>
        <p id="surviveMessage" class="survive-message" role="status" aria-live="polite" aria-atomic="true"></p>
        <div id="surviveEnemy" class="survive-enemy" hidden><strong id="surviveEnemyName">Wild hog</strong><span id="surviveEnemyHealth"></span></div>
        <div id="surviveActionBar" class="survive-action-bar">
          <div id="surviveMenus" class="survive-menus" role="group" aria-label="Moves">
          <div class="survive-menu">
            <button type="button" id="surviveMenuExploreButton" class="survive-menu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuExplore" data-menu-button>Explore <span class="survive-menu-count" data-menu-count>0</span></button>
            <div id="surviveMenuExplore" class="survive-menu-list" role="menu" aria-labelledby="surviveMenuExploreButton" hidden>
              <button type="button" role="menuitem" data-action="GATHER">Gather wood <small>50% chance · +1 wood</small></button>
              <button type="button" role="menuitem" data-action="GATHER_STONE">Gather stone <small>40% chance · +1 stone</small></button>
              <button type="button" role="menuitem" data-action="HUNT">Hunt <small>Hogs by day · Wolves and bears after dark</small></button>
            </div>
          </div>
          <div class="survive-menu">
            <button type="button" id="surviveMenuBuildButton" class="survive-menu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuBuild" data-menu-button>Build <span class="survive-menu-count" data-menu-count>0</span></button>
            <div id="surviveMenuBuild" class="survive-menu-list" role="menu" aria-labelledby="surviveMenuBuildButton" hidden>
              <button type="button" role="menuitem" data-action="BUILD_SHELTER">Build shelter <small>5 wood · Two beds for the camp</small></button>
              <button type="button" role="menuitem" data-action="BUILD_BOAT">Build boat <small>10 wood · One escape</small></button>
              <button type="button" role="menuitem" id="surviveCraftButton" class="survive-submenu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuCraft" data-submenu-button>Craft <small>Weapons from wood and stone</small><span aria-hidden="true">▸</span></button>
              <div id="surviveMenuCraft" class="survive-menu-list survive-submenu" role="menu" aria-labelledby="surviveCraftButton" hidden>
                <button type="button" role="menuitem" data-action="CRAFT_CLUB">Club <small>2 wood · +1 damage · 8 uses</small></button>
                <button type="button" role="menuitem" data-action="CRAFT_AXE">Stone axe <small>2 wood, 2 stone · +2 damage · Better wood gathering</small></button>
                <button type="button" role="menuitem" data-action="CRAFT_SPEAR">Spear <small>3 wood, 3 stone · +3 damage · Reach</small></button>
              </div>
            </div>
          </div>
          <div class="survive-menu">
            <button type="button" id="surviveMenuCampButton" class="survive-menu-button" aria-haspopup="menu" aria-expanded="false" aria-controls="surviveMenuCamp" data-menu-button>Camp <span class="survive-menu-count" data-menu-count>0</span></button>
            <div id="surviveMenuCamp" class="survive-menu-list" role="menu" aria-labelledby="surviveMenuCampButton" hidden>
              <button type="button" role="menuitem" data-action="EAT">Eat food <small>1 food · +5 fullness, +2 health</small></button>
              <button type="button" role="menuitem" data-action="REST">Rest <small>In a shelter · +2 health</small></button>
              <button type="button" role="menuitem" data-action="GUARD">Stand guard <small>Defend the camp from tonight's raid</small></button>
              <button type="button" role="menuitem" data-action="SLEEP">Sleep <small>Uses a shelter bed · Heal through the night</small></button>
              <button type="button" role="menuitem" data-action="ESCAPE">Sail away <small>Use a shared boat · Survive</small></button>
            </div>
          </div>
          </div>
          <div id="surviveDirectActions" class="survive-direct-actions" role="group" aria-label="Moves right now">
            <button type="button" data-action="ATTACK">Attack <small>The animal bites back</small></button>
            <button type="button" data-action="DEFEND">Defend <small>Block the next bite</small></button>
            <button type="button" data-action="FLEE">Flee <small>Return to camp · Take one bite</small></button>
            <button type="button" data-action="WAKE">Wake up <small>Keep the health you have recovered</small></button>
            <button id="surviveStartOver" type="button" class="survive-primary" hidden>Start a new survivor</button>
          </div>
        </div>
      </section>

      <aside class="survive-sidebar" aria-label="Survivor and camp">
        <section class="survive-panel survive-status-card" aria-labelledby="survivePlayerName">
          <div class="survive-status-head"><h2 id="survivePlayerName"></h2><p id="surviveSaveStatus" class="survive-muted" role="status"></p></div>
          <label class="survive-health-label" for="surviveHealth">Health <strong id="surviveHealthText"></strong></label>
          <meter id="surviveHealth" min="0" max="10" low="3" high="7" optimum="10" value="10"></meter>
          <label class="survive-health-label" for="surviveHunger">Fullness <strong id="surviveHungerText"></strong></label>
          <meter id="surviveHunger" min="0" max="10" low="4" high="7" optimum="10" value="10"></meter>
          <p id="surviveHungerWarning" class="survive-warning" role="status" hidden>You are hungry. Eat soon: at 0, every effort costs health.</p>
          <dl class="survive-inventory" aria-label="Inventory">
            <div><dt>Wood</dt><dd id="surviveWood"></dd></div>
            <div><dt>Food</dt><dd id="surviveFood"></dd></div>
            <div><dt>Stone</dt><dd id="surviveStone"></dd></div>
            <div><dt>Carried</dt><dd id="surviveInventoryCount"></dd></div>
          </dl>
          <p class="survive-card-line"><span class="survive-muted">Weapon</span> <strong id="surviveWeapon"></strong></p>
          <p class="survive-card-line survive-muted">Strength <strong id="surviveStrength"></strong> · Stamina <strong id="surviveStamina"></strong> · XP <strong id="surviveExperience"></strong></p>
          <div class="survive-recent-heading"><h3>Recent</h3><a href="#surviveSectionJournal" id="surviveFullJournal">Full journal</a></div>
          <ol id="surviveRecentEvents" class="survive-recent"></ol>
          <div class="survive-card-footer"><span id="survivePublicId" class="survive-muted"></span><span class="survive-secondary"><button id="surviveRefresh" type="button">Refresh world</button><button id="surviveRestart" type="button">New survivor</button></span></div>
        </section>
        <details id="surviveSectionCamp" class="survive-panel survive-section">
          <summary><span class="survive-section-title">Camp &amp; sharing</span> <span id="surviveCampSummary" class="survive-muted"></span></summary>
            <h3 class="survive-panel-title">Shared camp <span class="survive-muted">· One world, built together</span></h3>
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
        </details>
        <details id="surviveSectionJournal" class="survive-panel survive-section">
          <summary><span class="survive-section-title">Journal</span> <span id="surviveJournalUnread" class="survive-unread" hidden><span class="survive-visually-hidden">(new events)</span></span> <span class="survive-muted">Last 30 events, newest first</span></summary>
          <ol id="surviveEvents" reversed></ol>
        </details>
        <details id="surviveSectionGuide" class="survive-panel survive-section survive-guide">
          <summary><span class="survive-section-title">Guide</span> <span class="survive-muted">How to play, costs and odds</span></summary>
      <p>The camp picture shows the shared world as it is now. Click the trees to gather wood, the rocks for stone, the dark forest edge to hunt, the fire to stand guard or rest, a tent to sleep or wake, a boat to sail away, and an animal to attack it. Glowing places are the moves you can make now; every move is also in the menus below the picture.</p>
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
      </aside>
    </div>
    <p class="survive-attribution">Adapted from <a href="https://github.com/azurras/survive">azurras/Survive</a> · Java game engine · <a href="/licenses/survive-MIT.txt">MIT license</a>. Browser adaptation completes the original's unfinished combat and food actions.</p>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/3d2f59414637ff3e57c0/js/app.js"></script>
  <script type="module" src="/3d2f59414637ff3e57c0/js/survive.js"></script>
</body>
</html>
```

</details>

### 4. Panel module is served

<details><summary>119 lines</summary>

```text
HTTP 200 
X-Request-Id: c720f77e-f129-44ae-b4b5-1d4a2b759263
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792419706
Cache-Control: max-age=3600, public
Last-Modified: Mon, 19 Oct 2026 14:13:57 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 3698
Date: Mon, 19 Oct 2026 14:20:46 GMT
Connection: close

/**
 * Side panel behavior for the Survive page: remembered collapsible sections, the journal's
 * new-events marker and the camp summary. Display only; renders never open or close sections.
 */
const SECTION_NAMES = ['camp', 'journal', 'guide'];
const SECTION_STORAGE_PREFIX = 'survive.section.';

/** Restores each section's remembered open state and remembers changes. Returns its disposer. */
export function mountPanelSections(documentRoot, storage = browserStorage()) {
  const sections = SECTION_NAMES.map(name => ({ name, element: sectionElement(documentRoot, name) }));
  for (const { name, element } of sections) {
    element.open = readSafely(storage, SECTION_STORAGE_PREFIX + name) === 'open';
  }
  const togglers = sections.map(({ name, element }) => {
    const onToggle = () => {
      writeSafely(storage, SECTION_STORAGE_PREFIX + name, element.open ? 'open' : 'closed');
      if (name === 'journal' && element.open) {
        markJournalRead(documentRoot);
      }
    };
    element.addEventListener('toggle', onToggle);
    return { element, onToggle };
  });
  const fullJournalLink = documentRoot.getElementById('surviveFullJournal');
  const openJournal = event => {
    event.preventDefault();
    const journal = sectionElement(documentRoot, 'journal');
    journal.open = true;
    writeSafely(storage, SECTION_STORAGE_PREFIX + 'journal', 'open');
    markJournalRead(documentRoot);
    journal.scrollIntoView?.({ block: 'nearest', behavior: 'smooth' });
  };
  fullJournalLink.addEventListener('click', openJournal);
  return {
    dispose() {
      for (const { element, onToggle } of togglers) {
        element.removeEventListener('toggle', onToggle);
      }
      fullJournalLink.removeEventListener('click', openJournal);
    },
  };
}

/** Marks the journal heading when the world changed since the journal was last open. */
export function noteJournalEvents(documentRoot, worldRevision) {
  const journal = sectionElement(documentRoot, 'journal');
  const revision = String(worldRevision);
  journal.dataset.latestRevision = revision;
  if (journal.open || journal.dataset.seenRevision === undefined) {
    journal.dataset.seenRevision = revision;
  }
  documentRoot.getElementById('surviveJournalUnread').hidden = journal.dataset.seenRevision === revision;
}

/** One line describing the shared camp, for the closed Camp heading. */
export function summarizeCamp(state) {
  return [countOf(state.shelters, 'shelter'), countOf(state.boats, 'boat'), countOf(state.survivors.length, 'survivor')]
    .join(' · ');
}

function markJournalRead(documentRoot) {
  const journal = sectionElement(documentRoot, 'journal');
  if (journal.dataset.latestRevision !== undefined) {
    journal.dataset.seenRevision = journal.dataset.latestRevision;
  }
  documentRoot.getElementById('surviveJournalUnread').hidden = true;
}

function sectionElement(documentRoot, name) {
  return documentRoot.getElementById(`surviveSection${name[0].toUpperCase()}${name.slice(1)}`);
}

function countOf(count, singular) {
  return `${count} ${count === 1 ? singular : `${singular}s`}`;
}

function browserStorage() {
  return {
    read: key => globalThis.localStorage?.getItem(key) ?? null,
    write: (key, value) => globalThis.localStorage?.setItem(key, value),
  };
}

/** Storage can be missing or blocked (private windows, previews); the page works without it. */
function readSafely(storage, key) {
  try {
    return storage.read(key);
  } catch (storageFailure) {
    return null;
  }
}

function writeSafely(storage, key, value) {
  try {
    storage.write(key, value);
  } catch (storageFailure) {
    // The section still opens or closes; it just will not be remembered.
  }
}
```

</details>

### 5. Survive page no longer contains a tab strip

```text
exit code: 0
--- stdout ---
no tablist
```

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
  ]
}
```

### 7. API survivor Alice joins the camp as a gift recipient

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
Alice: POST /api/survive/v1/game {"name": "Alice"} -> 200 {"name":"Alice","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Tester","Alice"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Tester: The tree resists y...
PASS join or replace succeeds
  state: {"status": "EXPLORING", "phase": "DAY", "day": 204, "secondsToNextPhase": 235, "health": 10, "hunger": 10, "wood": 0, "food": 0, "stone": 0, "weapon": null, "weaponDurability": 0, "enemy": null, "enemyHealth": 0, "shelters": 0, "boats": 0, "bedsInUse": 0, "beds": 0, "guarding": false, "actions": ["GATHER", "GATHER_STONE", "HUNT"]}
PASS phase DAY matches the wall clock
PASS countdown is within one phase
PASS new survivor defaults
PASS stone gathering is offered
```

## Evidence
- Case 1 started 2026-10-19T09:20:45-05:00, took 63 ms, candidate `0112cc7`
- Case 2 started 2026-10-19T09:20:46-05:00, took 313 ms, candidate `0112cc7`
- Case 3 started 2026-10-19T09:20:46-05:00, took 47 ms, candidate `0112cc7`
- Case 4 started 2026-10-19T09:20:46-05:00, took 30 ms, candidate `0112cc7`
- Case 5 started 2026-10-19T09:20:47-05:00, took 125 ms, candidate `0112cc7`
- Case 6 started 2026-10-19T09:20:47-05:00, took 297 ms, candidate `0112cc7`
- Case 7 started 2026-10-19T09:22:05-05:00, took 141 ms, candidate `0112cc7`

## Bugs / Follow-ups
- Two clicks in this run landed beside their target after the page scrolled between measuring and clicking: the gift button once, and the scene measurement once. Both were repeated with fresh coordinates, and the misses are not counted. They were test-harness coordinate issues, not page defects.
- Right after Enter on the Camp summary, storage still read empty, because the browser fires `toggle` asynchronously. The reload in case 12 shows the state was saved.
- Cleanup: `Stop-Candidate.ps1` stopped the candidate and mongod and removed their temporary folders. Ports 56805 and 56807 have no listeners. All fixtures were created through the application's endpoints.

## Document Status
complete

## Project
christopherbell-dev
