# Survive menus and tabs: Test Report

## Story/Issue
User request 2026-10-18 "Need to clean up the UI a bit.... kind of a lot going on... maybe some menus and sub menus?"; plan docs/implementation-plans/2026-10-18-08-45-christopherbell-dev-survive-menus-and-tabs.md

## Branch
`claude/survive-menus-20261018` at candidate `56d2db9`

## Pass / Fail

> [!TIP]
> 20 of 20 cases passed on candidate `56d2db9`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate is ready and reports its build | ✅ PASS | Expected status below 400 and body containing '"build"' |
| 2 | Survive page serves the menus and the Craft submenu | ✅ PASS | Expected status below 400 and body containing 'aria-controls="surviveMenuCraft" data-submenu-button' |
| 3 | Survive page serves the Survivor, Camp, Journal and Guide tablist | ✅ PASS | Expected status below 400 and body containing 'role="tablist" aria-label="Survivor details"' |
| 4 | Menu module ships focus recovery for the action bar | ✅ PASS | Expected status below 400 and body containing 'export function keepFocusInActionBar' |
| 5 | Page script marks the action bar busy instead of disabling moves | ✅ PASS | Expected status below 400 and body containing "setAttribute('aria-busy', String(pending))" |
| 6 | Read-only query: the candidate wrote only to database test on the disposable mongod | ✅ PASS | Expected exit code 0 |
| 7 | API suppliers give the browser survivor 6 wood and 2 stone through gifts | ✅ PASS | Expected exit code 0 |
| 8 | After joining, menu buttons count only allowed moves and empty menus are disabled | ✅ PASS | Explore 3; Build 0 disabled; Camp 0 disabled (night, actions GATHER, GATHER_STONE, HUNT) |
| 9 | Clicking Explore opens it with focus on the first move; clicking Gather wood sends it and closes the menu | ✅ PASS | Opened with focus on GATHER; revision 1, wood 1; menu closed, focus on the Explore button |
| 10 | An open menu and keyboard focus survive a 5-second poll; Escape closes and returns focus | ✅ PASS | Focus GATHER_STONE before and after the poll, menu still open; after Escape the menu is closed and focus is on Explore |
| 11 | The Build menu lists Build shelter and the Craft submenu; clicking Build shelter builds it | ✅ PASS | Shown: BUILD_SHELTER plus Craft; shelters 1, wood 7 to 2; focus back on Build |
| 12 | At night Camp offers Sleep by keyboard; asleep, only Wake shows and holds focus; Enter wakes and focus returns to the menus | ✅ PASS | Camp menu at 14:34:43 showed SLEEP; asleep: menus hidden, direct WAKE, focus WAKE; awake: focus on Explore |
| 13 | Keyboard only: Arrow Down opens Build, Arrow Right opens Craft, Arrow Left closes it, Enter crafts the stone axe; focus moves on when Build empties | ✅ PASS | Focus Craft, then CRAFT_CLUB (Craft expanded), CRAFT_AXE, then Craft (collapsed); stone axe, 12 uses; Build disabled, focus on Explore |
| 14 | A fight hides the menus and shows Attack, Defend and Flee with focus on Attack; Enter attacks; focus returns after the fight | ✅ PASS | Wolf at 8 health; focus ATTACK; 6 damage, then defeated (+1 food); menus back with focus on Explore |
| 15 | Scene hotspots still send moves | ✅ PASS | Clicking the trees: revision 12 to 13, "The tree resists your efforts." |
| 16 | The Camp tab shows the shared camp, and Give supplies works there | ✅ PASS | Heading "Shared camp · One world, built together"; 3 recipients; "You gave 1 food to Supplierf0." |
| 17 | Tabs move with arrow keys, Home and End; opening Journal clears its new-events marker | ✅ PASS | Marker shown on Camp; Arrow Right to Journal (marker cleared, newest entry is the gift); End to Guide, Home to Survivor, Arrow Left wraps to Guide; stored "guide" |
| 18 | The chosen tab survives a reload, and Guide lists move costs | ✅ PASS | After reload Guide is selected and visible; Guide contains "A club costs 2 wood" |
| 19 | At 375x812 an open menu fits the screen with no horizontal scroll | ✅ PASS | Menu from 37 to 338 px; no horizontal scroll; each move is 75 px tall |
| 20 | The browser console logged no errors | ✅ PASS | No console messages |

## Test Cases
1. **Candidate is ready and reports its build**: http `GET http://127.0.0.1:50412/actuator/info`
2. **Survive page serves the menus and the Craft submenu**: http `GET http://127.0.0.1:50412/survive`
3. **Survive page serves the Survivor, Camp, Journal and Guide tablist**: http `GET http://127.0.0.1:50412/survive`
4. **Menu module ships focus recovery for the action bar**: http `GET http://127.0.0.1:50412/js/survive-menus.js`
5. **Page script marks the action bar busy instead of disabling moves**: http `GET http://127.0.0.1:50412/js/survive.js`
6. **Read-only query: the candidate wrote only to database test on the disposable mongod**: command `mongosh --quiet --port 50411 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name)})"`
7. **API suppliers give the browser survivor 6 wood and 2 stone through gifts**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/menus-candidate.json supply-tester`

## Browser Cases
Cases 8 to 20 ran in the Claude desktop app's browser pane against `http://127.0.0.1:50412/survive` on 2026-10-18 from 14:33 to 14:41 UTC, starting at night and running through dawn. Pointer cases used real clicks at each control's on-screen centre, and keyboard cases used real key presses. After each step, a read-only `GET /api/survive/v1/game` from the page confirmed the server state, and the page's DOM was read for the menu, tab and focus state.

## Automated Checks
- `.\ops\local\Invoke-Gradle.ps1 :website:build :website:bootJar` on `56d2db9`: BUILD SUCCESSFUL, with 2,166 Java tests (0 failed, 110 skipped), Checkstyle clean and `jsTest` 422 of 422.
- The menu and tab tests failed before `survive-menus.js` existed and passed once it was written.

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a disposable loopback mongod (port 50411), removed after the run |
| Candidate | website.jar built from the committed HEAD, http://127.0.0.1:50412 |
| Browser | Claude desktop browser pane, 1024x768 and the 375x812 mobile preset |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:50412/actuator/info` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Local command:** `GET http://127.0.0.1:50412/survive` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Local command:** `GET http://127.0.0.1:50412/survive` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Local command:** `GET http://127.0.0.1:50412/js/survive-menus.js` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Local command:** `GET http://127.0.0.1:50412/js/survive.js` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Local command:** `mongosh --quiet --port 50411 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name)})"` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/menus-candidate.json supply-tester` in `A:\Projects\christopherbell.dev.worktrees\survive-menus`
- **Candidate identity:** `56d2db9`
- **Cleanup:** Stopped the candidate process tree; no fixtures remain.

## Data Sent

### 1. Candidate is ready and reports its build

```http
GET http://127.0.0.1:50412/actuator/info
```

### 2. Survive page serves the menus and the Craft submenu

```http
GET http://127.0.0.1:50412/survive
```

### 3. Survive page serves the Survivor, Camp, Journal and Guide tablist

```http
GET http://127.0.0.1:50412/survive
```

### 4. Menu module ships focus recovery for the action bar

```http
GET http://127.0.0.1:50412/js/survive-menus.js
```

### 5. Page script marks the action bar busy instead of disabling moves

```http
GET http://127.0.0.1:50412/js/survive.js
```

### 6. Read-only query: the candidate wrote only to database test on the disposable mongod

```text
mongosh --quiet --port 50411 --eval "printjson({databases: db.adminCommand({listDatabases: 1}).databases.map(d => d.name)})"
```

### 7. API suppliers give the browser survivor 6 wood and 2 stone through gifts

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/survive_checks.py C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/ba214c78-6633-4862-b6c2-db0f2da035f8/scratchpad/menus-candidate.json supply-tester
```

## Response Received

### 1. Candidate is ready and reports its build

```text
HTTP 200 
X-Request-Id: f803ef0f-85d4-4ef7-8c1a-7d7c9af27b8b
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792334054
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
Date: Sun, 18 Oct 2026 14:33:14 GMT
Connection: close

{"build":{"artifact":"website","name":"website","time":"2026-10-18T14:27:18.649Z","version":"0.0.0-dev.56d2db98af1e2ab17d4da81478340c124333c205","group":"christopherbell.dev"}}
```

### 2. Survive page serves the menus and the Craft submenu

<details><summary>201 lines</summary>

```text
HTTP 200 
X-Request-Id: c66e7119-11b8-4739-a399-aadb0df93661
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792334054
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
Date: Sun, 18 Oct 2026 14:33:14 GMT
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
  <link rel="stylesheet" href="/95369a3350e82dc4f8c7/css/main.css" />
  <link rel="stylesheet" href="/95369a3350e82dc4f8c7/css/survive.css" />
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
        <section class="survive-panel survive-vitals" aria-labelledby="survivePlayerName">
          <h2 id="survivePlayerName"></h2>
          <label class="survive-health-label" for="surviveHealth">Health <strong id="surviveHealthText"></strong></label>
          <meter id="surviveHealth" min="0" max="10" low="3" high="7" optimum="10" value="10"></meter>
          <label class="survive-health-label" for="surviveHunger">Fullness <strong id="surviveHungerText"></strong></label>
          <meter id="surviveHunger" min="0" max="10" low="4" high="7" optimum="10" value="10"></meter>
          <p id="surviveHungerWarning" class="survive-warning" role="status" hidden>You are hungry. Eat soon: at 0, every effort costs health.</p>
        </section>
        <div class="survive-panel survive-tabs">
          <div id="surviveTabs" class="survive-tablist" role="tablist" aria-label="Survivor details">
            <button type="button" role="tab" id="surviveTabSurvivor" aria-controls="survivePanelSurvivor" aria-selected="true" data-tab="survivor">Survivor</button>
            <button type="button" role="tab" id="surviveTabCamp" aria-controls="survivePanelCamp" aria-selected="false" tabindex="-1" data-tab="camp">Camp</button>
            <button type="button" role="tab" id="surviveTabJournal" aria-controls="survivePanelJournal" aria-selected="false" tabindex="-1" data-tab="journal">Journal <span id="surviveJournalUnread" class="survive-unread" hidden><span class="survive-visually-hidden">(new events)</span></span></button>
            <button type="button" role="tab" id="surviveTabGuide" aria-controls="survivePanelGuide" aria-selected="false" tabindex="-1" data-tab="guide">Guide</button>
          </div>
          <section id="survivePanelSurvivor" class="survive-tab-panel" role="tabpanel" aria-labelledby="surviveTabSurvivor">
            <dl class="survive-stats"><div><dt>Strength</dt><dd id="surviveStrength"></dd></div><div><dt>Stamina</dt><dd id="surviveStamina"></dd></div><div><dt>Gathering XP</dt><dd id="surviveExperience"></dd></div></dl>
            <h3>Inventory <span id="surviveInventoryCount"></span></h3>
            <dl class="survive-stats"><div><dt>Wood</dt><dd id="surviveWood"></dd></div><div><dt>Food</dt><dd id="surviveFood"></dd></div><div><dt>Stone</dt><dd id="surviveStone"></dd></div></dl>
            <h3>Weapon</h3>
            <p id="surviveWeapon" class="survive-muted"></p>
            <p id="surviveSaveStatus" class="survive-muted" role="status"></p>
            <p id="survivePublicId" class="survive-muted"></p>
            <div class="survive-secondary"><button id="surviveRefresh" type="button">Refresh world</button><button id="surviveRestart" type="button">New survivor</button></div>
          </section>
          <section id="survivePanelCamp" class="survive-tab-panel" role="tabpanel" aria-labelledby="surviveTabCamp" hidden>
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
          </section>
          <section id="survivePanelJournal" class="survive-tab-panel" role="tabpanel" aria-labelledby="surviveTabJournal" hidden>
            <p class="survive-muted">The last 30 events, newest first.</p>
            <ol id="surviveEvents" reversed></ol>
          </section>
          <section id="survivePanelGuide" class="survive-tab-panel survive-guide" role="tabpanel" aria-labelledby="surviveTabGuide" hidden>
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
          </section>
        </div>
      </aside>
    </div>
    <p class="survive-attribution">Adapted from <a href="https://github.com/azurras/survive">azurras/Survive</a> · Java game engine · <a href="/licenses/survive-MIT.txt">MIT license</a>. Browser adaptation completes the original's unfinished combat and food actions.</p>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/95369a3350e82dc4f8c7/js/app.js"></script>
  <script type="module" src="/95369a3350e82dc4f8c7/js/survive.js"></script>
</body>
</html>
```

</details>

### 3. Survive page serves the Survivor, Camp, Journal and Guide tablist

<details><summary>201 lines</summary>

```text
HTTP 200 
X-Request-Id: 3c8bfb7b-bb81-4aa0-a249-e9826815ec66
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792334054
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
Date: Sun, 18 Oct 2026 14:33:14 GMT
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
  <link rel="stylesheet" href="/95369a3350e82dc4f8c7/css/main.css" />
  <link rel="stylesheet" href="/95369a3350e82dc4f8c7/css/survive.css" />
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
        <section class="survive-panel survive-vitals" aria-labelledby="survivePlayerName">
          <h2 id="survivePlayerName"></h2>
          <label class="survive-health-label" for="surviveHealth">Health <strong id="surviveHealthText"></strong></label>
          <meter id="surviveHealth" min="0" max="10" low="3" high="7" optimum="10" value="10"></meter>
          <label class="survive-health-label" for="surviveHunger">Fullness <strong id="surviveHungerText"></strong></label>
          <meter id="surviveHunger" min="0" max="10" low="4" high="7" optimum="10" value="10"></meter>
          <p id="surviveHungerWarning" class="survive-warning" role="status" hidden>You are hungry. Eat soon: at 0, every effort costs health.</p>
        </section>
        <div class="survive-panel survive-tabs">
          <div id="surviveTabs" class="survive-tablist" role="tablist" aria-label="Survivor details">
            <button type="button" role="tab" id="surviveTabSurvivor" aria-controls="survivePanelSurvivor" aria-selected="true" data-tab="survivor">Survivor</button>
            <button type="button" role="tab" id="surviveTabCamp" aria-controls="survivePanelCamp" aria-selected="false" tabindex="-1" data-tab="camp">Camp</button>
            <button type="button" role="tab" id="surviveTabJournal" aria-controls="survivePanelJournal" aria-selected="false" tabindex="-1" data-tab="journal">Journal <span id="surviveJournalUnread" class="survive-unread" hidden><span class="survive-visually-hidden">(new events)</span></span></button>
            <button type="button" role="tab" id="surviveTabGuide" aria-controls="survivePanelGuide" aria-selected="false" tabindex="-1" data-tab="guide">Guide</button>
          </div>
          <section id="survivePanelSurvivor" class="survive-tab-panel" role="tabpanel" aria-labelledby="surviveTabSurvivor">
            <dl class="survive-stats"><div><dt>Strength</dt><dd id="surviveStrength"></dd></div><div><dt>Stamina</dt><dd id="surviveStamina"></dd></div><div><dt>Gathering XP</dt><dd id="surviveExperience"></dd></div></dl>
            <h3>Inventory <span id="surviveInventoryCount"></span></h3>
            <dl class="survive-stats"><div><dt>Wood</dt><dd id="surviveWood"></dd></div><div><dt>Food</dt><dd id="surviveFood"></dd></div><div><dt>Stone</dt><dd id="surviveStone"></dd></div></dl>
            <h3>Weapon</h3>
            <p id="surviveWeapon" class="survive-muted"></p>
            <p id="surviveSaveStatus" class="survive-muted" role="status"></p>
            <p id="survivePublicId" class="survive-muted"></p>
            <div class="survive-secondary"><button id="surviveRefresh" type="button">Refresh world</button><button id="surviveRestart" type="button">New survivor</button></div>
          </section>
          <section id="survivePanelCamp" class="survive-tab-panel" role="tabpanel" aria-labelledby="surviveTabCamp" hidden>
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
          </section>
          <section id="survivePanelJournal" class="survive-tab-panel" role="tabpanel" aria-labelledby="surviveTabJournal" hidden>
            <p class="survive-muted">The last 30 events, newest first.</p>
            <ol id="surviveEvents" reversed></ol>
          </section>
          <section id="survivePanelGuide" class="survive-tab-panel survive-guide" role="tabpanel" aria-labelledby="surviveTabGuide" hidden>
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
          </section>
        </div>
      </aside>
    </div>
    <p class="survive-attribution">Adapted from <a href="https://github.com/azurras/survive">azurras/Survive</a> · Java game engine · <a href="/licenses/survive-MIT.txt">MIT license</a>. Browser adaptation completes the original's unfinished combat and food actions.</p>
  </main>
  <footer id="footer"></footer>
  <script type="module" src="/95369a3350e82dc4f8c7/js/app.js"></script>
  <script type="module" src="/95369a3350e82dc4f8c7/js/survive.js"></script>
</body>
</html>
```

</details>

### 4. Menu module ships focus recovery for the action bar

<details><summary>349 lines</summary>

```text
HTTP 200 
X-Request-Id: 0ba8531d-4af5-4180-9efb-c531b7448ba1
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792334054
Cache-Control: max-age=3600, public
Last-Modified: Sun, 18 Oct 2026 14:27:23 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 11753
Date: Sun, 18 Oct 2026 14:33:14 GMT
Connection: close

/**
 * Menu and tab behavior for the Survive page. Display only: which moves exist is decided by the
 * server snapshot, which `renderSurviveState` applies by hiding moves before `syncActionMenus` runs.
 * Menus follow the menu-button pattern; tabs use roving focus.
 */
const TAB_STORAGE_KEY = 'survive.tab';

/** Wires every menu button, item and submenu inside the action bar. Returns its disposer. */
export function mountActionMenus(documentRoot, actionBar) {
  const onClick = event => {
    const menuButton = event.target.closest('[data-menu-button]');
    if (menuButton && actionBar.contains(menuButton)) {
      if (!menuButton.disabled) {
        toggleMenu(documentRoot, actionBar, menuButton);
      }
      return;
    }
    const submenuButton = event.target.closest('[data-submenu-button]');
    if (submenuButton) {
      if (isExpanded(submenuButton)) {
        closeList(documentRoot, submenuButton);
      }
      else {
        openList(documentRoot, submenuButton, 'first');
      }
      return;
    }
    const chosenMove = event.target.closest('[data-action]');
    const chosenMenu = chosenMove?.closest('[role="menu"]');
    if (chosenMenu) {
      const topButton = topMenuButtonFor(documentRoot, actionBar, chosenMenu);
      closeAllMenus(documentRoot, actionBar);
      topButton?.focus();
    }
  };
  const onKeydown = event => {
    const menuButton = event.target.closest('[data-menu-button]');
    if (menuButton && (event.key === 'ArrowDown' || event.key === 'ArrowUp')) {
      event.preventDefault();
      if (!menuButton.disabled) {
        closeAllMenus(documentRoot, actionBar);
        openList(documentRoot, menuButton, event.key === 'ArrowDown' ? 'first' : 'last');
      }
      return;
    }
    const menu = event.target.closest('[role="menu"]');
    if (menu && actionBar.contains(menu)) {
      handleMenuKey(documentRoot, actionBar, menu, event);
    }
  };
  const onDocumentClick = event => {
    if (!actionBar.contains(event.target)) {
      closeAllMenus(documentRoot, actionBar);
    }
  };
  actionBar.addEventListener('click', onClick);
  actionBar.addEventListener('keydown', onKeydown);
  documentRoot.addEventListener('click', onDocumentClick);
  return {
    dispose() {
      actionBar.removeEventListener('click', onClick);
      actionBar.removeEventListener('keydown', onKeydown);
      documentRoot.removeEventListener('click', onDocumentClick);
    },
  };
}

/**
 * Brings menu buttons in line with the moves the latest render left visible: counts, disabled empty
 * menus, the Craft submenu and focus. Open menus stay open unless they emptied.
 */
export function syncActionMenus(documentRoot, actionBar) {
  repairFocus(documentRoot, actionBar);
  const menuButtons = [...actionBar.querySelectorAll('[data-menu-button]')];
  const focusedMenuButton = menuButtons.find(button => button === documentRoot.activeElement);
  for (const menuButton of menuButtons) {
    const list = listControlledBy(documentRoot, menuButton);
    for (const submenuButton of list.querySelectorAll('[data-submenu-button]')) {
      const submenuIsEmpty = visibleMoves(listControlledBy(documentRoot, submenuButton)).length === 0;
      if (submenuIsEmpty && isExpanded(submenuButton)) {
        closeList(documentRoot, submenuButton);
      }
      submenuButton.hidden = submenuIsEmpty;
    }
    const moveCount = visibleMoves(list).length;
    menuButton.querySelector('[data-menu-count]').textContent = String(moveCount);
    menuButton.disabled = moveCount === 0;
    if (moveCount === 0 && isExpanded(menuButton)) {
      closeList(documentRoot, menuButton);
    }
  }
  // A move that empties its own menu disables the button holding focus; keep focus in the bar.
  if (focusedMenuButton?.disabled) {
    menuButtons.find(button => !button.disabled)?.focus();
  }
}

/**
 * After a render changes the bar's shape (a fight starts, sleep, the end of the game), returns
 * focus that was in the bar to its first usable control instead of letting it fall to the page.
 */
export function keepFocusInActionBar(documentRoot, actionBar) {
  const focused = documentRoot.activeElement;
  const focusIsUsable = Boolean(focused) && actionBar.contains(focused) && !focused.disabled
    && !focused.closest('[hidden]');
  if (focusIsUsable) {
    return;
  }
  const usableControls = [...actionBar.querySelectorAll('button')]
    .filter(control => !control.disabled && !control.closest('[hidden]'));
  usableControls[0]?.focus();
}

/** Wires the side panel tabs, restoring the remembered tab. Returns its disposer. */
export function mountPanelTabs(documentRoot, tablist, storage = browserStorage()) {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const select = (tab, { moveFocus }) => {
    for (const candidate of tabs) {
      const isSelected = candidate === tab;
      candidate.setAttribute('aria-selected', String(isSelected));
      candidate.setAttribute('tabindex', isSelected ? '0' : '-1');
      documentRoot.getElementById(candidate.getAttribute('aria-controls')).hidden = !isSelected;
    }
    if (moveFocus) {
      tab.focus();
    }
    if (tab.id === 'surviveTabJournal') {
      markJournalRead(documentRoot);
    }
    writeSafely(storage, TAB_STORAGE_KEY, tab.dataset.tab);
  };
  const rememberedName = readSafely(storage, TAB_STORAGE_KEY);
  const initialTab = tabs.find(tab => tab.dataset.tab === rememberedName) ?? tabs[0];
  select(initialTab, { moveFocus: false });

  const onClick = event => {
    const tab = event.target.closest('[role="tab"]');
    if (tab) {
      select(tab, { moveFocus: true });
    }
  };
  const onKeydown = event => {
    const tab = event.target.closest('[role="tab"]');
    const index = tabs.indexOf(tab);
    const targetIndex = {
      ArrowRight: (index + 1) % tabs.length,
      ArrowLeft: (index - 1 + tabs.length) % tabs.length,
      Home: 0,
      End: tabs.length - 1,
    }[event.key];
    if (tab && targetIndex !== undefined) {
      event.preventDefault();
      select(tabs[targetIndex], { moveFocus: true });
    }
  };
  tablist.addEventListener('click', onClick);
  tablist.addEventListener('keydown', onKeydown);
  return {
    dispose() {
      tablist.removeEventListener('click', onClick);
      tablist.removeEventListener('keydown', onKeydown);
    },
  };
}

/** Marks the Journal tab when the world changed since the journal was last on screen. */
export function noteJournalEvents(documentRoot, worldRevision) {
  const journalTab = documentRoot.getElementById('surviveTabJournal');
  const revision = String(worldRevision);
  journalTab.dataset.latestRevision = revision;
  if (journalTab.getAttribute('aria-selected') === 'true' || journalTab.dataset.seenRevision === undefined) {
    journalTab.dataset.seenRevision = revision;
  }
  documentRoot.getElementById('surviveJournalUnread').hidden = journalTab.dataset.seenRevision === revision;
}

function markJournalRead(documentRoot) {
  const journalTab = documentRoot.getElementById('surviveTabJournal');
  if (journalTab.dataset.latestRevision !== undefined) {
    journalTab.dataset.seenRevision = journalTab.dataset.latestRevision;
  }
  documentRoot.getElementById('surviveJournalUnread').hidden = true;
}

function handleMenuKey(documentRoot, actionBar, menu, event) {
  const items = focusableItems(menu);
  const index = items.indexOf(event.target);
  const submenuButton = event.target.closest('[data-submenu-button]');
  const parentButton = buttonControlling(documentRoot, actionBar, menu);
  switch (event.key) {
    case 'ArrowDown':
    case 'ArrowUp':
    case 'Home':
    case 'End': {
      event.preventDefault();
      const targetIndex = {
        ArrowDown: (index + 1) % items.length,
        ArrowUp: (index - 1 + items.length) % items.length,
        Home: 0,
        End: items.length - 1,
      }[event.key];
      items[targetIndex]?.focus();
      return;
    }
    case 'ArrowRight':
      if (submenuButton) {
        event.preventDefault();
        openList(documentRoot, submenuButton, 'first');
      }
      return;
    case 'ArrowLeft':
      if (parentButton?.hasAttribute('data-submenu-button')) {
        event.preventDefault();
        closeList(documentRoot, parentButton);
        parentButton.focus();
      }
      return;
    case 'Escape':
      event.preventDefault();
      closeList(documentRoot, parentButton);
      parentButton.focus();
      return;
    case 'Tab':
      closeAllMenus(documentRoot, actionBar);
      return;
    default:
  }
}

function toggleMenu(documentRoot, actionBar, menuButton) {
  const wasOpen = isExpanded(menuButton);
  closeAllMenus(documentRoot, actionBar);
  if (!wasOpen) {
    openList(documentRoot, menuButton, 'first');
  }
}

function openList(documentRoot, button, focusTarget) {
  button.setAttribute('aria-expanded', 'true');
  const list = listControlledBy(documentRoot, button);
  list.hidden = false;
  const items = focusableItems(list);
  (focusTarget === 'first' ? items[0] : items.at(-1))?.focus();
}

/** Closes a menu or submenu and everything nested inside it. */
function closeList(documentRoot, button) {
  const list = listControlledBy(documentRoot, button);
  for (const nestedButton of list.querySelectorAll('[aria-haspopup="menu"]')) {
    closeList(documentRoot, nestedButton);
  }
  button.setAttribute('aria-expanded', 'false');
  list.hidden = true;
}

function closeAllMenus(documentRoot, actionBar) {
  for (const menuButton of actionBar.querySelectorAll('[data-menu-button]')) {
    closeList(documentRoot, menuButton);
  }
}

/** Keeps focus on a visible move when a render hides the focused one. */
function repairFocus(documentRoot, actionBar) {
  const focused = documentRoot.activeElement;
  if (!focused || !actionBar.contains(focused) || !focused.hidden) {
    return;
  }
  const menu = focused.closest('[role="menu"]');
  const replacement = menu ? focusableItems(menu)[0] : null;
  (replacement ?? (menu ? topMenuButtonFor(documentRoot, actionBar, menu) : null))?.focus();
}

function listControlledBy(documentRoot, button) {
  return documentRoot.getElementById(button.getAttribute('aria-controls'));
}

function buttonControlling(documentRoot, actionBar, menu) {
  return actionBar.querySelector(`[aria-controls="${menu.id}"]`);
}

function topMenuButtonFor(documentRoot, actionBar, menu) {
  let button = buttonControlling(documentRoot, actionBar, menu);
  while (button?.hasAttribute('data-submenu-button')) {
    button = buttonControlling(documentRoot, actionBar, button.closest('[role="menu"]'));
  }
  return button;
}

function isExpanded(button) {
  return button.getAttribute('aria-expanded') === 'true';
}

/** Items that belong to this menu itself, not to a submenu nested inside it. */
function ownItems(menu) {
  return [...menu.querySelectorAll('[role="menuitem"]')].filter(item => item.closest('[role="menu"]') === menu);
}

function focusableItems(menu) {
  return ownItems(menu).filter(item => !item.hidden && !item.disabled);
}

/** Moves left visible anywhere in a menu, including its submenus. */
function visibleMoves(menu) {
  return [...menu.querySelectorAll('[data-action]')].filter(move => !move.hidden);
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
    // The tab still changes; it just will not be remembered.
  }
}
```

</details>

### 5. Page script marks the action bar busy instead of disabling moves

<details><summary>325 lines</summary>

```text
HTTP 200 
X-Request-Id: 6fd8cb1e-e17b-4d07-82cd-85e9e1b2ffde
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1792334055
Cache-Control: max-age=3600, public
Last-Modified: Sun, 18 Oct 2026 14:27:23 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 14337
Date: Sun, 18 Oct 2026 14:33:15 GMT
Connection: close

/** Display and transport only: the Java world owns all rules and allowed actions. */
import { API } from './lib/api.js';
import { fetchJson } from './lib/util.js';
import {
  keepFocusInActionBar, mountActionMenus, mountPanelTabs, noteJournalEvents, syncActionMenus,
} from './survive-menus.js';
import { renderSurviveScene } from './survive-scene.js';

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
const HUNGER_WARNING_LEVEL = 3;

/** Minutes and seconds until the next phase, for example 4:05. */
export function formatCountdown(secondsLeft) {
  const wholeSeconds = Math.max(0, Math.floor(secondsLeft));
  return `${Math.floor(wholeSeconds / 60)}:${String(wholeSeconds % 60).padStart(2, '0')}`;
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
  renderSurviveScene(documentRoot, documentRoot.getElementById('surviveCampScene'), state, pending);
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
  // Menus and the direct group list only moves the server allows now; menus appear while exploring.
  const actionBar = documentRoot.getElementById('surviveActionBar');
  const focusWasInActionBar = actionBar.contains(documentRoot.activeElement);
  for (const move of actionBar.querySelectorAll('[data-action]')) {
    const isAllowed = state.actions.includes(move.dataset.action);
    move.hidden = !isAllowed;
    move.disabled = !isAllowed;
  }
  // Busy rather than disabled: disabling the focused move during a poll would drop keyboard focus.
  // The click handler already ignores every move while a request is in flight.
  actionBar.setAttribute('aria-busy', String(pending));
  documentRoot.getElementById('surviveMenus').hidden = state.status !== 'EXPLORING';
  const startOver = documentRoot.getElementById('surviveStartOver');
  startOver.hidden = !['DEAD', 'ESCAPED'].includes(state.status);
  startOver.disabled = pending;
  syncActionMenus(documentRoot, actionBar);
  if (focusWasInActionBar) {
    keepFocusInActionBar(documentRoot, actionBar);
  }
  noteJournalEvents(documentRoot, state.worldRevision);
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
  const startOver = documentRoot.getElementById('surviveStartOver');
  const actionBar = documentRoot.getElementById('surviveActionBar');
  const menus = mountActionMenus(documentRoot, actionBar);
  const tabs = mountPanelTabs(documentRoot, documentRoot.getElementById('surviveTabs'));
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
  // Buttons and scene hotspots share one path: only an action the latest snapshot allows, one at a time.
  const act = event => {
    const control = event.target.closest('[data-action]');
    if (!control || control.disabled || !state || pending) {
      return;
    }
    const action = control.dataset.action;
    if (!state.actions.includes(action)) {
      return;
    }
    void sendRequest(API.survive.actions, {
      method: 'POST', body: JSON.stringify({ action, revision: state.revision }),
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
  actionBar.addEventListener('click', act);
  startOver.addEventListener('click', showJoin);
  documentRoot.getElementById('surviveCampScene').addEventListener('click', act);
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
      actionBar.removeEventListener('click', act);
      startOver.removeEventListener('click', showJoin);
      menus.dispose();
      tabs.dispose();
      documentRoot.getElementById('surviveCampScene').removeEventListener('click', act);
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

### 7. API suppliers give the browser survivor 6 wood and 2 stone through gifts

<details><summary>92 lines</summary>

```text
exit code: 0
--- stdout ---
Supplierf0: GET /survive  -> 200 <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  

    <meta name="description" content="Gather, craft, and survive in a shared text adventure world." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/survive" />



    <meta property="og:site_name" content="christopherbell.dev" />
...
Supplierf0: POST /api/survive/v1/game {"name": "Supplierf0"} -> 200 {"name":"Supplierf0","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
PASS join succeeds
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":3,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 0} -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":4,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
PASS GATHER_STONE returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":4,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":0,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":1,"worldRevision":4,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: POST /api/survive/v1/actions {"action": "GATHER_STONE", "revision": 1} -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
PASS GATHER_STONE returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":2,"worldRevision":5,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: POST /api/survive/v1/actions {"action": "GATHER", "revision": 2} -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":3,"worldRevision":6,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
PASS GATHER returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":3,"worldRevision":6,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":10,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":3,"worldRevision":6,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
Supplierf0: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 3} -> 200 {"name":"Supplierf0","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":4,"status":"COMBAT","revision":4,"worldRevision":7,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived a...
PASS ATTACK returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":4,"status":"COMBAT","revision":4,"worldRevision":7,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived a...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":8,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":4,"status":"COMBAT","revision":4,"worldRevision":7,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived a...
Supplierf0: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 4} -> 200 {"name":"Supplierf0","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":8,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrive...
PASS ATTACK returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":8,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrive...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":5,"worldRevision":8,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrive...
Supplierf0: POST /api/survive/v1/actions {"action": "GATHER", "revision": 5} -> 200 {"name":"Supplierf0","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":9,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrive...
PASS GATHER returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":9,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrive...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":3,"stamina":11,"experience":1,"experienceToNextLevel":2,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":6,"worldRevision":9,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrive...
Supplierf0: POST /api/survive/v1/actions {"action": "GATHER", "revision": 6} -> 200 {"name":"Supplierf0","health":6,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":10,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
PASS GATHER returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":10,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":7,"worldRevision":10,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arriv...
Supplierf0: POST /api/survive/v1/actions {"action": "GATHER", "revision": 7} -> 200 {"name":"Supplierf0","health":6,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":8,"worldRevision":11,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
PASS GATHER returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":8,"worldRevision":11,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":6,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":8,"status":"COMBAT","revision":8,"worldRevision":11,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
Supplierf0: POST /api/survive/v1/actions {"action": "ATTACK", "revision": 8} -> 200 {"name":"Supplierf0","health":4,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":3,"status":"COMBAT","revision":9,"worldRevision":12,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
PASS ATTACK returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":4,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":3,"status":"COMBAT","revision":9,"worldRevision":12,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":4,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":3,"status":"COMBAT","revision":9,"worldRevision":12,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arrived ...
Supplierf0: POST /api/survive/v1/actions {"action": "FLEE", "revision": 9} -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
PASS FLEE returned 200, expected 200
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
PASS the browser survivor Tester is a gift recipient
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":1,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":10,"worldRevision":13,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
Supplierf0: POST /api/survive/v1/gifts {"recipientId": "59f66702-e6e4-465d-ba19-ee56470b6fd0", "resource": "WOOD", "quantity": 1, "revision": 10} -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":14,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
PASS Supplierf0 gave 1 wood to Tester
Supplierf0: GET /api/survive/v1/game  -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":11,"worldRevision":14,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
Supplierf0: POST /api/survive/v1/gifts {"recipientId": "59f66702-e6e4-465d-ba19-ee56470b6fd0", "resource": "STONE", "quantity": 2, "revision": 11} -> 200 {"name":"Supplierf0","health":2,"strength":4,"stamina":12,"experience":0,"experienceToNextLevel":4,"wood":0,"food":1,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":12,"worldRevision":15,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Supplierf0 arri...
PASS Supplierf0 gave 2 stone to Tester
Supplierf1: GET /survive  -> 200 <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  

    <meta name="description" content="Gather, craft, and survive in a shared text adventure world." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/survive" />



    <meta property="og:site_name" content="christopherbell.dev" />
...
Supplierf1: POST /api/survive/v1/game {"name": "Supplierf1"} -> 200 {"name":"Supplierf1","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":16,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0","Supplierf1"],"events":["Tester arrived at camp.","Tester: You gathered one piece of wood. Your strength and stamina increased!","Su...
PASS join succeeds
Supplierf1: GET /api/survive/v1/game  -> 200 {"name":"Supplierf1","health":10,"strength":2,"stamina":10,"experience":0,"experienceToNextLevel":1,"wood":0,"food":0,"inventoryCapacity":10,"enemyHealth":0,"status":"EXPLORING","revision":0,"worldRevision":16,"shelters":0,"boats":0,"survivors":["Tester","Supplierf0","Supplierf1"],"events":["Tester arrived at 
... [33991 more characters not recorded]
```

</details>

## Evidence
- Case 1 started 2026-10-18T09:33:14-05:00, took 46 ms, candidate `56d2db9`
- Case 2 started 2026-10-18T09:33:14-05:00, took 203 ms, candidate `56d2db9`
- Case 3 started 2026-10-18T09:33:14-05:00, took 47 ms, candidate `56d2db9`
- Case 4 started 2026-10-18T09:33:14-05:00, took 31 ms, candidate `56d2db9`
- Case 5 started 2026-10-18T09:33:15-05:00, took 30 ms, candidate `56d2db9`
- Case 6 started 2026-10-18T09:33:15-05:00, took 282 ms, candidate `56d2db9`
- Case 7 started 2026-10-18T09:34:11-05:00, took 1875 ms, candidate `56d2db9`

## Bugs / Follow-ups
- Superseded candidates, with their defects fixed and every case rerun on `56d2db9`:
  - `eed2dd1`: polling disabled the focused move and dropped keyboard focus from open menus, and focus fell to the page when crafting emptied the Build menu. Commit `c3c620d` fixed both: the action bar is marked `aria-busy`, and focus moves to an enabled menu button.
  - `c3c620d`: focus fell to the page when a fight began, during sleep and after a fight. Commit `56d2db9` added `keepFocusInActionBar`.
  - Earlier evidence is kept in scratch files and is not counted here.
- The test harness supplied wood and stone through the gift API. Its first attempts on `eed2dd1` and `c3c620d` failed in the harness itself: one supplier starved on a single stomach, and another overfilled Tester's inventory. Those runs were dropped, and case 7 uses short-lived suppliers with exact amounts.
- Stand guard at dusk was exercised by keyboard on `c3c620d` (guarding true, defense 7), but not on `56d2db9`, because this run spanned night and day only. The guard path through the Camp menu is the same code as every other Camp move, and page tests cover it.
- On a 375 px phone the three menu buttons wrap onto two rows. They stay usable, and this was left as is.
- Cleanup: `Stop-Candidate.ps1` stopped the candidate and mongod and removed their temporary folders. Ports 50411 and 50412 have no listeners. All fixtures were created through the application's endpoints.

## Document Status
complete

## Project
christopherbell-dev
