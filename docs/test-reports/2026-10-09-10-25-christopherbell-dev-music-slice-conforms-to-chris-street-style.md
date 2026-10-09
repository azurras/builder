# Music slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 13 of the style migration ([plan](../implementation-plans/2026-10-09-10-18-christopherbell-dev-music-slice-conforms-to-chris-street-style.md)): the Music page, its scripts, the entry probe and the protected Music API behave as before

## Branch
`claude/style-music-20261009` at candidate `c50a86e`

## Pass / Fail

> [!TIP]
> 14 of 14 cases passed on candidate `c50a86e`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create music_user through the API and log in (password generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | The Music page renders | ✅ PASS | Expected status 200 and body containing '/js/music.js' |
| 4 | The Music page script is served | ✅ PASS | Expected status 200 and body containing 'function fileDataUrl(file) {' |
| 5 | The Music library module is served | ✅ PASS | Expected status 200 and body containing 'Object.freeze({ ...value, ...text })' |
| 6 | Anonymous Music entry asks the visitor to sign in | ✅ PASS | Expected status 200 and body containing '{"authenticated":false,"allowed":false,"canManage":false,"reason":"SIGN_IN_REQUIRED"}' |
| 7 | A USER without Music permission is told Music read is required | ✅ PASS | Expected status 200 and body containing '{"authenticated":true,"allowed":false,"canManage":false,"reason":"MUSIC_READ_REQUIRED"}' |
| 8 | Anonymous catalog gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 9 | Anonymous radio gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 10 | Anonymous queue gets the same status and body as production (403) | ✅ PASS | Expected exit code 0 |
| 11 | A USER without Music permission cannot read the catalog (403) | ✅ PASS | Expected status 403 |
| 12 | A USER without Music permission cannot change track preferences (403) | ✅ PASS | Expected status 403 |
| 13 | A USER without Music permission cannot queue a track (403) | ✅ PASS | Expected status 403 |
| 14 | A USER cannot read the Music access log (403) | ✅ PASS | Expected status 403 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:56769/actuator/health/readiness`
2. **Create music_user through the API and log in (password generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:56769 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad music_user`
3. **The Music page renders**: http `GET http://127.0.0.1:56769/music`
4. **The Music page script is served**: http `GET http://127.0.0.1:56769/js/music.js`
5. **The Music library module is served**: http `GET http://127.0.0.1:56769/js/lib/music.js`
6. **Anonymous Music entry asks the visitor to sign in**: http `GET http://127.0.0.1:56769/api/music/2026-07-28/access`
7. **A USER without Music permission is told Music read is required**: http `GET http://127.0.0.1:56769/api/music/2026-07-28/access`
8. **Anonymous catalog gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/catalog https://www.christopherbell.dev/api/music/2026-07-28/catalog 403`
9. **Anonymous radio gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/radio https://www.christopherbell.dev/api/music/2026-07-28/radio 403`
10. **Anonymous queue gets the same status and body as production (403)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/queue https://www.christopherbell.dev/api/music/2026-07-28/queue 403`
11. **A USER without Music permission cannot read the catalog (403)**: http `GET http://127.0.0.1:56769/api/music/2026-07-28/catalog`
12. **A USER without Music permission cannot change track preferences (403)**: http `PATCH http://127.0.0.1:56769/api/music/2026-07-28/library/tracks/track-1/preferences`
13. **A USER without Music permission cannot queue a track (403)**: http `POST http://127.0.0.1:56769/api/music/2026-07-28/queue`
14. **A USER cannot read the Music access log (403)**: http `GET http://127.0.0.1:56769/api/music/2026-07-28/admin/access-attempts`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (Music disabled, as in the default configuration) |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:56768 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:56769, commit c50a86e4 |
| Credentials | one disposable USER in the throwaway database; password generated and never recorded; bearer token masked and token file deleted |
| Coverage limit | granting MUSIC_READ or MUSIC_WRITE needs an ADMIN, which has no supported local path; catalog, preference, queue, radio and metadata success paths are covered by the Music service tests and the Mongo contract tests that run in CI |
| Production | compared with read-only GETs only; the production entry probe was not called because it records an audit attempt |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:56769/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:56769 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad music_user` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/music` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/js/music.js` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/js/lib/music.js` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/api/music/2026-07-28/access` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/api/music/2026-07-28/access` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/catalog https://www.christopherbell.dev/api/music/2026-07-28/catalog 403` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/radio https://www.christopherbell.dev/api/music/2026-07-28/radio 403` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/queue https://www.christopherbell.dev/api/music/2026-07-28/queue 403` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/api/music/2026-07-28/catalog` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `PATCH http://127.0.0.1:56769/api/music/2026-07-28/library/tracks/track-1/preferences` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `POST http://127.0.0.1:56769/api/music/2026-07-28/queue` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Local command:** `GET http://127.0.0.1:56769/api/music/2026-07-28/admin/access-attempts` in `A:\Projects\christopherbell.dev-worktrees\style-music`
- **Candidate identity:** `c50a86e`
- **Cleanup:** Candidate and mongod stopped; both ports have no listeners; production mongod on 27017 untouched

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:56769/actuator/health/readiness
```

### 2. Create music_user through the API and log in (password generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:56769 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad music_user
```

### 3. The Music page renders

```http
GET http://127.0.0.1:56769/music
```

### 4. The Music page script is served

```http
GET http://127.0.0.1:56769/js/music.js
```

### 5. The Music library module is served

```http
GET http://127.0.0.1:56769/js/lib/music.js
```

### 6. Anonymous Music entry asks the visitor to sign in

```http
GET http://127.0.0.1:56769/api/music/2026-07-28/access
```

### 7. A USER without Music permission is told Music read is required

```http
GET http://127.0.0.1:56769/api/music/2026-07-28/access
Authorization: [REDACTED]
```

### 8. Anonymous catalog gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/catalog https://www.christopherbell.dev/api/music/2026-07-28/catalog 403
```

### 9. Anonymous radio gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/radio https://www.christopherbell.dev/api/music/2026-07-28/radio 403
```

### 10. Anonymous queue gets the same status and body as production (403)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_status_and_body.py http://127.0.0.1:56769/api/music/2026-07-28/queue https://www.christopherbell.dev/api/music/2026-07-28/queue 403
```

### 11. A USER without Music permission cannot read the catalog (403)

```http
GET http://127.0.0.1:56769/api/music/2026-07-28/catalog
Authorization: [REDACTED]
```

### 12. A USER without Music permission cannot change track preferences (403)

```http
PATCH http://127.0.0.1:56769/api/music/2026-07-28/library/tracks/track-1/preferences
Authorization: [REDACTED]
Content-Type: application/json

{"expectedFavorite":false,"expectedExcludedFromRadio":false,"favorite":true,"excludedFromRadio":false}
```

### 13. A USER without Music permission cannot queue a track (403)

```http
POST http://127.0.0.1:56769/api/music/2026-07-28/queue
Authorization: [REDACTED]
Content-Type: application/json

{"trackId":"track-1","expectedVersion":0}
```

### 14. A USER cannot read the Music access log (403)

```http
GET http://127.0.0.1:56769/api/music/2026-07-28/admin/access-attempts
Authorization: [REDACTED]
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: c04cfe8b-7e61-4bcd-a345-01dd752f1819
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559543
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
Date: Fri, 09 Oct 2026 15:24:43 GMT
Connection: close

{"status":"UP"}
```

### 2. Create music_user through the API and log in (password generated, not recorded)

```text
exit code: 0
--- stdout ---
music_user create 201 login 200
```

### 3. The Music page renders

<details><summary>138 lines</summary>

```text
HTTP 200 
X-Request-Id: 3893f458-4f34-4a1b-bc0e-25fc19b66314
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559544
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
Date: Fri, 09 Oct 2026 15:24:44 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  
    <meta name="description" content="Private music on christopherbell.dev." />
    <meta name="robots" content="noindex,nofollow" />
    <link rel="canonical" href="https://www.christopherbell.dev/music" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | Music" />
    <meta property="og:description" content="Private music on christopherbell.dev." />
    <meta property="og:url" content="https://www.christopherbell.dev/music" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Music on christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | Music" />
    <meta name="twitter:description" content="Private music on christopherbell.dev." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="Music on christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  
  <title>Music</title>
  <link rel="stylesheet" type="text/css" href="/4bde45fabdcee234ef25/css/main.css" />
  <link rel="stylesheet" type="text/css" href="/4bde45fabdcee234ef25/css/music.css" />
</head>
<body class="site-page void-shell-page music-page">
  <div id="nav"></div>
  <main class="site-main music-main" aria-labelledby="music-title">
    <header class="music-hero">
      <div>
        <p class="music-kicker">One shared library</p>
        <h1 id="music-title">Music</h1>
        <p>Browse the collection, shape the queue, or drop into the live station.</p>
      </div>
      <button id="music-radio" class="music-radio-button" type="button" disabled>
        <span aria-hidden="true">◉</span><span>Join live radio</span>
      </button>
    </header>
    <section id="music-access" class="music-access" aria-live="polite">
      <p>Checking Music access…</p>
    </section>
    <section id="music-library" class="music-workspace d-none" aria-label="Music library">
      <aside class="music-sidebar" aria-label="Music views">
        <nav class="music-view-nav">
          <button class="is-active" type="button" data-view="all">All music</button>
          <button type="button" data-view="favorites">Favorites</button>
          <button type="button" data-view="history">Radio history</button>
        </nav>
        <div class="music-sidebar-heading"><h2>Playlists</h2><button id="music-new-playlist" type="button" hidden>＋</button></div>
        <div id="music-playlists" class="music-playlists"></div>
      </aside>
      <section class="music-browser">
        <form id="music-search" class="music-search" role="search">
          <label class="visually-hidden" for="music-search-query">Search music</label>
          <span aria-hidden="true">⌕</span>
          <input id="music-search-query" type="search" maxlength="100" placeholder="Search songs, artists, albums, genres…" />
          <button type="submit">Search</button>
        </form>
        <div class="music-filters" aria-label="Library filters">
          <select id="music-artist-filter" aria-label="Filter by artist"><option value="">All artists</option></select>
          <select id="music-album-filter" aria-label="Filter by album"><option value="">All albums</option></select>
          <select id="music-genre-filter" aria-label="Filter by genre"><option value="">All genres</option></select>
          <span id="music-count"></span>
        </div>
        <div id="music-results" class="music-results" aria-live="polite"></div>
        <nav id="music-pagination" class="music-pagination" aria-label="Music result pages" hidden></nav>
      </section>
      <aside class="music-activity" aria-label="Shared queue">
        <div class="music-panel-heading"><div><span>Up next</span><h2>Shared queue</h2></div><span id="music-queue-count">0</span></div>
        <div id="music-queue" class="music-queue"></div>
      </aside>
    </section>
  </main>
  <dialog id="music-playlist-dialog" class="music-dialog">
    <form method="dialog" id="music-playlist-form">
      <input type="hidden" id="music-playlist-id" />
      <h2>Playlist</h2>
      <label>Name<input id="music-playlist-name" maxlength="100" required /></label>
      <p>Select tracks from the library after creating the playlist.</p>
      <div><button type="submit" value="cancel" formnovalidate>Cancel</button><button id="music-save-playlist" type="submit" value="default">Save</button></div>
    </form>
  </dialog>
  <dialog id="music-metadata-dialog" class="music-dialog">
    <form method="dialog" id="music-metadata-form">
      <h2>Edit track details</h2>
      <input type="hidden" id="music-edit-track-id" />
      <div class="music-form-grid">
        <label>Title<input id="music-edit-title" maxlength="300" /></label>
        <label>Artist<input id="music-edit-artist" maxlength="300" /></label>
        <label>Album artist<input id="music-edit-album-artist" maxlength="300" /></label>
        <label>Album<input id="music-edit-album" maxlength="300" /></label>
        <label>Track<input id="music-edit-track" type="number" min="1" max="9999" /></label>
        <label>Disc<input id="music-edit-disc" type="number" min="1" max="999" /></label>
        <label>Genre<input id="music-edit-genre" maxlength="300" /></label>
        <label>Year<input id="music-edit-year" type="number" min="1000" max="9999" /></label>
      </div>
      <label>Replace artwork<input id="music-edit-artwork" type="file" accept="image/jpeg,image/png" /></label>
      <label class="music-check"><input id="music-edit-remove-artwork" type="checkbox" /> Remove existing artwork</label>
      <p id="music-edit-status" aria-live="polite"></p>
      <div><button type="submit" value="cancel" formnovalidate>Cancel</button><button id="music-save-metadata" type="submit" value="default">Save changes</button></div>
    </form>
  </dialog>
  <div id="music-toast" class="music-toast" hidden aria-live="polite"></div>
  <footer id="footer"></footer>
  <script type="module" src="/4bde45fabdcee234ef25/js/app.js"></script>
  <script type="module" src="/4bde45fabdcee234ef25/js/music.js"></script>
</body>
</html>
```

</details>

### 4. The Music page script is served

<details><summary>430 lines</summary>

```text
HTTP 200 
X-Request-Id: 18e8695d-b780-4b8d-b268-c4837d5e2984
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559545
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 15:18:25 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 17038
Date: Fri, 09 Oct 2026 15:24:45 GMT
Connection: close

import { API } from './lib/api.js';
import {
  musicCatalog,
  musicCatalogParameters,
  musicPaginationMarkup,
  musicPlaylists,
  musicQueue,
  musicQueueMarkup,
  musicTrack,
  musicTrackMarkup,
} from './lib/music.js';
import { playMusicRadio, playMusicTrack } from './lib/site-media-loader.js';
import { fetchJson, loginRedirectUrl, sanitize } from './lib/util.js';

const elements = Object.freeze({
  access: document.getElementById('music-access'),
  library: document.getElementById('music-library'),
  results: document.getElementById('music-results'),
  search: document.getElementById('music-search'),
  query: document.getElementById('music-search-query'),
  radio: document.getElementById('music-radio'),
  artist: document.getElementById('music-artist-filter'),
  album: document.getElementById('music-album-filter'),
  genre: document.getElementById('music-genre-filter'),
  count: document.getElementById('music-count'),
  pagination: document.getElementById('music-pagination'),
  queue: document.getElementById('music-queue'),
  queueCount: document.getElementById('music-queue-count'),
  playlists: document.getElementById('music-playlists'),
  newPlaylist: document.getElementById('music-new-playlist'),
  playlistDialog: document.getElementById('music-playlist-dialog'),
  playlistForm: document.getElementById('music-playlist-form'),
  metadataDialog: document.getElementById('music-metadata-dialog'),
  metadataForm: document.getElementById('music-metadata-form'),
  toast: document.getElementById('music-toast'),
});

const state = {
  canManage: false,
  catalog: {
    tracks: [], facets: { artists: [], albums: [], genres: [], years: [] },
    page: 0, size: 50, totalTracks: 0, totalPages: 0,
  },
  queue: { version: 0, items: [] },
  playlists: [],
  history: [],
  view: 'all',
};
let catalogRequestController = null;

function deniedMarkup(status) {
  if (!status?.authenticated) {
    return `<h2>Sign in to Music</h2><p>Music is available to authorized listeners.</p>
      <a class="btn btn-warning" href="${sanitize(loginRedirectUrl('/music'))}">Sign in</a>`;
  }
  return '<h2>Music access required</h2><p>Your account does not currently have Music access. This attempt was recorded for an administrator.</p>';
}

async function loadWorkspace() {
  const [catalogResponse, queueResponse, playlistsResponse, historyResponse] = await Promise.all([
    fetchJson(API.music.catalog(), { redirectOnUnauthorized: false, cache: 'no-store' }),
    fetchJson(API.music.queue, { redirectOnUnauthorized: false, cache: 'no-store' }),
    fetchJson(API.music.library.playlists, { redirectOnUnauthorized: false, cache: 'no-store' }),
    fetchJson(API.music.library.history(50), { redirectOnUnauthorized: false, cache: 'no-store' }),
  ]);
  state.catalog = musicCatalog(catalogResponse);
  state.queue = musicQueue(queueResponse);
  state.playlists = musicPlaylists(playlistsResponse);
  state.history = Array.isArray(historyResponse) ? historyResponse.slice(0, 100) : [];
  renderWorkspace();
}

async function loadCatalog(page = 0) {
  catalogRequestController?.abort();
  const requestController = new AbortController();
  const requestedView = state.view;
  catalogRequestController = requestController;
  elements.results.innerHTML = '<p class="music-empty">Searching the library…</p>';
  elements.pagination.hidden = true;
  try {
    const response = await fetchJson(API.music.catalog(musicCatalogParameters({
      view: requestedView,
      page,
      q: String(elements.query?.value || '').trim(),
      artist: elements.artist?.value || '',
      album: elements.album?.value || '',
      genre: elements.genre?.value || '',
    })), {
      redirectOnUnauthorized: false,
      cache: 'no-store',
      signal: requestController.signal,
    });
    if (catalogRequestController !== requestController || state.view !== requestedView) return;
    state.catalog = musicCatalog(response);
    renderWorkspace();
  } catch (error) {
    if (error?.name !== 'AbortError') throw error;
  } finally {
    if (catalogRequestController === requestController) catalogRequestController = null;
  }
}

function renderWorkspace() {
  renderFilters();
  renderPlaylists();
  renderQueue();
  renderResults();
  renderPagination();
}

function renderFilters() {
  fillSelect(elements.artist, 'All artists', state.catalog.facets.artists);
  fillSelect(elements.album, 'All albums', state.catalog.facets.albums);
  fillSelect(elements.genre, 'All genres', state.catalog.facets.genres);
}

function fillSelect(select, label, values) {
  if (!select) return;
  const selected = select.value;
  select.replaceChildren(new Option(label, ''), ...values.map(value => new Option(value, value)));
  if (values.includes(selected)) select.value = selected;
}

function renderResults() {
  document.querySelectorAll('[data-view]').forEach(button => {
    button.classList.toggle('is-active', button.dataset.view === state.view);
  });
  if (state.view === 'history') {
    elements.count.textContent = `${state.history.length} recent plays`;
    elements.results.innerHTML = historyMarkup();
    return;
  }
  const tracks = state.catalog.tracks;
  const count = state.catalog.totalTracks.toLocaleString();
  const page = state.catalog.totalPages > 0
    ? ` · Page ${state.catalog.page + 1} of ${state.catalog.totalPages}` : '';
  elements.count.textContent = `${count} track${state.catalog.totalTracks === 1 ? '' : 's'}${page}`;
  elements.results.innerHTML = tracks.length
    ? tracks.map(track => musicTrackMarkup(track, {
      canManage: state.canManage,
      playlists: state.playlists,
    })).join('')
    : '<p class="music-empty">No tracks matched this view.</p>';
}

function renderPagination() {
  if (state.view === 'history') {
    elements.pagination.replaceChildren();
    elements.pagination.hidden = true;
    return;
  }
  const markup = musicPaginationMarkup(state.catalog);
  elements.pagination.innerHTML = markup;
  elements.pagination.hidden = markup.length === 0;
}

function renderQueue() {
  elements.queueCount.textContent = String(state.queue.items.length);
  elements.queue.innerHTML = musicQueueMarkup(state.queue, { canManage: state.canManage });
}

function renderPlaylists() {
  elements.playlists.innerHTML = state.playlists.length
    ? state.playlists.map(item => `<button type="button" data-view="playlist:${sanitize(item.id)}">
      ${sanitize(item.name)} <small>${item.trackIds.length}</small></button>`).join('')
    : '<p class="music-empty">No playlists yet.</p>';
}

function historyMarkup() {
  if (!state.history.length) return '<p class="music-empty">The radio has no history yet.</p>';
  const byId = new Map(state.catalog.tracks.map(track => [track.id, track]));
  return state.history.map(event => {
    const track = byId.get(event?.trackId);
    const title = track?.title || 'Unavailable track';
    const detail = [event?.artist || track?.artist, event?.source].filter(Boolean).join(' · ');
    return `<article class="music-track"><span></span><div class="music-track-art"><span>↺</span></div>
      <div class="music-track-copy"><strong>${sanitize(title)}</strong><span>${sanitize(detail)}</span></div>
      <time>${sanitize(new Date(event?.occurredAt).toLocaleString())}</time><span></span></article>`;
  }).join('');
}

async function trackAction(action, track) {
  if (action === 'play') {
    await playMusicTrack(track);
    return;
  }
  if (!state.canManage) return;
  if (action === 'favorite' || action === 'exclude') {
    const updated = await fetchJson(API.music.library.preferences(track.id), {
      method: 'PATCH',
      body: JSON.stringify({
        expectedFavorite: track.favorite,
        expectedExcludedFromRadio: track.excludedFromRadio,
        favorite: action === 'favorite' ? !track.favorite : track.favorite,
        excludedFromRadio: action === 'exclude'
          ? !track.excludedFromRadio : track.excludedFromRadio,
      }),
    });
    if (action === 'favorite' && state.view === 'favorites') {
      await loadCatalog(state.catalog.page);
    } else {
      replaceTrack(updated);
    }
  } else if (action === 'queue') {
    state.queue = musicQueue(await fetchJson(API.music.queue, {
      method: 'POST', body: JSON.stringify({ trackId: track.id, expectedVersion: state.queue.version }),
    }));
    renderQueue();
  } else if (action === 'edit') {
    openMetadata(track);
  }
}

function replaceTrack(updated) {
  const validated = musicTrack(updated);
  state.catalog = { ...state.catalog, tracks: state.catalog.tracks.map(
    track => track.id === validated.id ? validated : track) };
  renderResults();
}

async function addToPlaylist(playlistId, track) {
  const playlist = state.playlists.find(item => item.id === playlistId);
  if (!playlist || playlist.trackIds.includes(track.id)) return;
  const updated = await fetchJson(API.music.library.playlist(playlist.id), {
    method: 'PUT',
    body: JSON.stringify({
      expectedVersion: playlist.version,
      name: playlist.name,
      trackIds: [...playlist.trackIds, track.id],
    }),
  });
  state.playlists = musicPlaylists(state.playlists.map(
    item => item.id === updated.id ? updated : item));
  renderWorkspace();
  showToast(`Added “${track.title}” to ${playlist.name}.`);
}

function openMetadata(track) {
  document.getElementById('music-edit-track-id').value = track.id;
  document.getElementById('music-edit-title').value = track.title || '';
  document.getElementById('music-edit-artist').value = track.artist || '';
  document.getElementById('music-edit-album-artist').value = track.albumArtist || '';
  document.getElementById('music-edit-album').value = track.album || '';
  document.getElementById('music-edit-track').value = track.trackNumber || '';
  document.getElementById('music-edit-disc').value = track.discNumber || '';
  document.getElementById('music-edit-genre').value = track.genre || '';
  document.getElementById('music-edit-year').value = track.year || '';
  document.getElementById('music-edit-artwork').value = '';
  document.getElementById('music-edit-remove-artwork').checked = false;
  document.getElementById('music-edit-status').textContent = '';
  elements.metadataDialog.showModal();
}

async function saveMetadata() {
  const id = document.getElementById('music-edit-track-id').value;
  const track = state.catalog.tracks.find(item => item.id === id);
  if (!track) return;
  const artworkFile = document.getElementById('music-edit-artwork').files?.[0];
  if (artworkFile?.size > 5 * 1024 * 1024) throw new Error('Artwork must be 5 MB or smaller.');
  const artworkDataUrl = artworkFile ? await fileDataUrl(artworkFile) : null;
  const result = await fetchJson(API.music.metadata(id), {
    method: 'PATCH',
    body: JSON.stringify({
      expectedObservedToken: track.observedToken,
      title: input('music-edit-title'), artist: input('music-edit-artist'),
      albumArtist: input('music-edit-album-artist'), album: input('music-edit-album'),
      trackNumber: integer('music-edit-track'), discNumber: integer('music-edit-disc'),
      genre: input('music-edit-genre'), year: integer('music-edit-year'), artworkDataUrl,
      removeArtwork: document.getElementById('music-edit-remove-artwork').checked,
    }),
  });
  replaceTrack(result.track);
  elements.metadataDialog.close();
  showToast('Track details saved.', {
    label: 'Undo', action: () => undoMetadata(result.editId, result.observedToken),
  });
}

async function undoMetadata(editId, observedToken) {
  const result = await fetchJson(API.music.metadataUndo(editId), {
    method: 'POST', body: JSON.stringify({ expectedObservedToken: observedToken }),
  });
  replaceTrack(result.track);
  showToast('Metadata edit undone.');
}

function showToast(message, option = null) {
  elements.toast.replaceChildren(document.createTextNode(message));
  if (option) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = option.label;
    button.addEventListener('click', () => void option.action().catch(showError), { once: true });
    elements.toast.append(button);
  }
  elements.toast.hidden = false;
  window.setTimeout(() => { elements.toast.hidden = true; }, 8_000);
}

function showError(error) {
  showToast(error?.status === 409 ? 'Music changed. Refresh and try again.' : error?.message || 'Music request failed.');
}

function input(id) {
  return String(document.getElementById(id)?.value || '').trim() || null;
}

function integer(id) {
  const value = input(id);
  return value === null ? null : Number(value);
}

function fileDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(new Error('Artwork could not be read.'));
    reader.readAsDataURL(file);
  });
}

elements.search?.addEventListener('submit', event => {
  event.preventDefault();
  void loadCatalog(0).catch(showError);
});
for (const filter of [elements.artist, elements.album, elements.genre]) {
  filter?.addEventListener('change', () => void loadCatalog(0).catch(showError));
}
elements.radio?.addEventListener('click', async () => {
  elements.radio.disabled = true;
  try {
    const response = await playMusicRadio();
    elements.radio.querySelector('span:last-child').textContent =
      response?.status === 'EMPTY' ? 'Radio is empty' : 'Listening live';
  } catch (error) {
    showError(error);
  } finally {
    elements.radio.disabled = false;
  }
});
elements.library?.addEventListener('click', event => {
  const requestedPage = Number(event.target.closest('[data-page]')?.dataset.page);
  if (Number.isSafeInteger(requestedPage) && requestedPage >= 0) {
    void loadCatalog(requestedPage).catch(showError);
    return;
  }
  const view = event.target.closest('[data-view]')?.dataset.view;
  if (view) {
    state.view = view;
    if (view === 'history') renderWorkspace();
    else void loadCatalog(0).catch(showError);
    return;
  }
  const action = event.target.closest('[data-action]')?.dataset.action;
  const row = event.target.closest('[data-track-id]');
  const track = state.catalog.tracks.find(item => item.id === row?.dataset.trackId);
  if (action && track) void trackAction(action, track).catch(showError);
  if (action === 'remove-queue') {
    const queueId = event.target.closest('[data-queue-id]')?.dataset.queueId;
    void fetchJson(`${API.music.queueItem(queueId)}?expectedVersion=${state.queue.version}`, {
      method: 'DELETE',
    }).then(response => { state.queue = musicQueue(response); renderQueue(); }).catch(showError);
  }
});
elements.library?.addEventListener('change', event => {
  if (event.target.dataset.action !== 'playlist' || !event.target.value) return;
  const id = event.target.closest('[data-track-id]')?.dataset.trackId;
  const track = state.catalog.tracks.find(item => item.id === id);
  if (track) void addToPlaylist(event.target.value, track).catch(showError);
  event.target.value = '';
});
elements.newPlaylist?.addEventListener('click', () => elements.playlistDialog.showModal());
elements.playlistForm?.addEventListener('submit', event => {
  if (event.submitter?.value === 'cancel') return;
  event.preventDefault();
  const name = input('music-playlist-name');
  void fetchJson(API.music.library.playlists, {
    method: 'POST', body: JSON.stringify({ name, trackIds: [] }),
  }).then(created => {
    state.playlists = musicPlaylists([...state.playlists, created]);
    elements.playlistDialog.close();
    elements.playlistForm.reset();
    renderWorkspace();
  }).catch(showError);
});
elements.metadataForm?.addEventListener('submit', event => {
  if (event.submitter?.value === 'cancel') return;
  event.preventDefault();
  document.getElementById('music-edit-status').textContent = 'Saving…';
  void saveMetadata().catch(error => {
    document.getElementById('music-edit-status').textContent = error?.message || 'Save failed.';
  });
});

async function initialize() {
  try {
    const status = await fetchJson(API.music.access, { redirectOnUnauthorized: false, cache: 'no-store' });
    if (!status?.allowed) { elements.access.innerHTML = deniedMarkup(status); return; }
    state.canManage = status.canManage === true;
    elements.access.classList.add('d-none');
    elements.library.classList.remove('d-none');
    elements.radio.disabled = false;
    elements.newPlaylist.hidden = !state.canManage;
    await loadWorkspace();
  } catch (error) {
    elements.access.innerHTML = '<h2>Music is temporarily unavailable</h2><p>Please try again shortly.</p>';
  }
}

void initialize();
```

</details>

### 5. The Music library module is served

<details><summary>208 lines</summary>

```text
HTTP 200 
X-Request-Id: 926b4d13-bd96-4762-9f6a-280dcc3f7f48
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559545
Cache-Control: max-age=3600, public
Last-Modified: Fri, 09 Oct 2026 15:18:25 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 9255
Date: Fri, 09 Oct 2026 15:24:45 GMT
Connection: close

import { API } from './api.js';
import { sanitize } from './util.js';
export { accountHasMusicRead } from './account-capabilities.js';

const TEXT_LIMIT = 512;

function optionalText(value) {
  return value === null || value === undefined
    ? null
    : typeof value === 'string' && value.length <= TEXT_LIMIT ? value : undefined;
}

/** Validate one catalog track before it reaches markup, URLs, or the player. */
export function musicTrack(value) {
  const text = {
    title: optionalText(value?.title),
    artist: optionalText(value?.artist),
    albumArtist: optionalText(value?.albumArtist),
    album: optionalText(value?.album),
    genre: optionalText(value?.genre),
  };
  if (typeof value?.id !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/u.test(value.id)
      || typeof value.observedToken !== 'string' || !/^[0-9a-f]{64}$/u.test(value.observedToken)
      || typeof text.title !== 'string' || Object.values(text).some(item => item === undefined)
      || !Number.isFinite(value.durationSeconds) || value.durationSeconds <= 0
      || value.durationSeconds > 604800
      || typeof value.artworkAvailable !== 'boolean'
      || typeof value.favorite !== 'boolean'
      || typeof value.excludedFromRadio !== 'boolean') {
    throw new Error('Music returned an invalid track.');
  }
  return Object.freeze({ ...value, ...text });
}

export function musicCatalog(value) {
  const validPage = Number.isSafeInteger(value?.page) && value.page >= 0;
  const validSize = Number.isSafeInteger(value?.size) && value.size >= 1 && value.size <= 100;
  const validTotal = Number.isSafeInteger(value?.totalTracks) && value.totalTracks >= 0;
  const validPages = Number.isSafeInteger(value?.totalPages) && value.totalPages >= 0;
  const expectedPages = validSize && validTotal ? Math.ceil(value.totalTracks / value.size) : -1;
  const pageInRange = value?.totalPages === 0
    ? value?.page === 0 && value?.tracks?.length === 0
    : value?.page < value?.totalPages;
  if (!Array.isArray(value?.tracks) || typeof value?.facets !== 'object'
      || !validPage || !validSize || !validTotal || !validPages
      || value.totalPages !== expectedPages || !pageInRange || value.tracks.length > value.size) {
    throw new Error('Music returned an invalid catalog.');
  }
  return Object.freeze({
    tracks: Object.freeze(value.tracks.map(musicTrack)),
    facets: musicFacets(value.facets),
    page: value.page,
    size: value.size,
    totalTracks: value.totalTracks,
    totalPages: value.totalPages,
  });
}

/** Return a compact set of zero-based page numbers for accessible pagination controls. */
export function musicPageNumbers(page, totalPages) {
  if (!Number.isSafeInteger(page) || !Number.isSafeInteger(totalPages) || totalPages < 1) return [];
  const last = totalPages - 1;
  const current = Math.max(0, Math.min(last, page));
  if (totalPages <= 7) return Array.from({ length: totalPages }, (_, index) => index);
  if (current <= 1) return [0, 1, 2, last];
  if (current >= last - 1) return [0, last - 2, last - 1, last];
  return [0, current - 1, current, current + 1, last];
}

/** Translate a validated Music sidebar view into server-side catalog constraints. */
export function musicViewFilter(view) {
  if (view === 'all') return {};
  if (view === 'favorites') return { favorite: true };
  if (typeof view === 'string' && view.startsWith('playlist:')) {
    const playlistId = view.substring('playlist:'.length);
    if (/^[A-Za-z0-9_-]{1,100}$/u.test(playlistId)) return { playlistId };
  }
  throw new Error('Music view is invalid.');
}

/** Build one bounded catalog request from browser-owned view and filter state. */
export function musicCatalogParameters({ view, page, q, artist, album, genre }) {
  if (!Number.isSafeInteger(page) || page < 0) throw new Error('Music page is invalid.');
  return {
    q, artist, album, genre, page, size: 50, ...musicViewFilter(view),
  };
}

/** Render accessible page controls from trusted, validated catalog metadata. */
export function musicPaginationMarkup({ page, totalPages }) {
  const pages = musicPageNumbers(page, totalPages);
  if (pages.length <= 1) return '';
  const previous = Math.max(0, page - 1);
  const next = Math.min(totalPages - 1, page + 1);
  const parts = [`<button type="button" data-page="${previous}"${page === 0 ? ' disabled' : ''}>Previous</button>`];
  pages.forEach((value, index) => {
    if (index > 0 && value - pages[index - 1] > 1) {
      parts.push('<span class="music-page-gap" aria-hidden="true">…</span>');
    }
    parts.push(`<button type="button" data-page="${value}"${value === page ? ' aria-current="page"' : ''}>${value + 1}</button>`);
  });
  parts.push(`<button type="button" data-page="${next}"${page === totalPages - 1 ? ' disabled' : ''}>Next</button>`);
  return parts.join('');
}

export function musicQueue(value) {
  if (!Number.isSafeInteger(value?.version) || value.version < 0 || !Array.isArray(value.items)) {
    throw new Error('Music returned an invalid queue.');
  }
  return Object.freeze({
    version: value.version,
    items: Object.freeze(value.items.slice(0, 1000).map(item => {
      if (typeof item?.id !== 'string' || !/^[A-Za-z0-9_-]{1,100}$/u.test(item.id)) {
        throw new Error('Music returned an invalid queue item.');
      }
      return Object.freeze({ ...item, track: musicTrack(item.track) });
    })),
  });
}

export function musicPlaylists(value) {
  if (!Array.isArray(value)) throw new Error('Music returned invalid playlists.');
  return Object.freeze(value.slice(0, 100).map(playlist => {
    if (typeof playlist?.id !== 'string' || !/^[A-Za-z0-9_-]{1,100}$/u.test(playlist.id)
        || typeof playlist.name !== 'string' || playlist.name.length < 1 || playlist.name.length > 100
        || !Number.isSafeInteger(playlist.version) || playlist.version < 0
        || !Array.isArray(playlist.trackIds) || playlist.trackIds.length > 1000
        || playlist.trackIds.some(id => typeof id !== 'string'
          || !/^[A-Za-z0-9_-]{1,128}$/u.test(id))) {
      throw new Error('Music returned an invalid playlist.');
    }
    return Object.freeze({ ...playlist, trackIds: Object.freeze([...playlist.trackIds]) });
  }));
}

export function formatMusicDuration(seconds) {
  const total = Number.isFinite(seconds) ? Math.max(0, Math.round(seconds)) : 0;
  const minutes = Math.floor(total / 60);
  return `${minutes}:${String(total % 60).padStart(2, '0')}`;
}

export function musicTrackMarkup(track, { canManage = false, playlists = [] } = {}) {
  const value = musicTrack(track);
  const subtitle = [value.artist, value.album].filter(Boolean).join(' · ') || 'Unknown artist';
  const art = value.artworkAvailable
    ? `<img src="${sanitize(API.music.artwork(value.id))}" alt="" loading="lazy" />`
    : '<span aria-hidden="true">♫</span>';
  return `<article class="music-track" data-track-id="${sanitize(value.id)}">
    <button class="music-track-play" type="button" data-action="play" aria-label="Play ${sanitize(value.title)}">▶</button>
    <div class="music-track-art">${art}</div>
    <div class="music-track-copy"><strong>${sanitize(value.title)}</strong><span>${sanitize(subtitle)}</span></div>
    <time>${formatMusicDuration(value.durationSeconds)}</time>
    <div class="music-track-actions">
      ${canManage ? `<button type="button" data-action="favorite" aria-pressed="${value.favorite}">${value.favorite ? '★' : '☆'}</button>
      <button type="button" data-action="queue">Queue</button>
      <button type="button" data-action="exclude" aria-pressed="${value.excludedFromRadio}">${value.excludedFromRadio ? 'Radio off' : 'Radio on'}</button>
      <select data-action="playlist" aria-label="Add ${sanitize(value.title)} to playlist">
        <option value="">Playlist…</option>${playlists.map(item => `<option value="${sanitize(item.id)}">${sanitize(item.name)}</option>`).join('')}
      </select>
      <button type="button" data-action="edit">Edit</button>` : ''}
    </div>
  </article>`;
}

export function musicQueueMarkup(queue, { canManage = false } = {}) {
  const value = musicQueue(queue);
  if (!value.items.length) return '<p class="music-empty">The shared queue is empty.</p>';
  return value.items.map((item, index) => `<article class="music-queue-item" data-queue-id="${sanitize(item.id)}">
    <span>${index + 1}</span><div><strong>${sanitize(item.track.title)}</strong>
    <small>${sanitize(item.track.artist || 'Unknown artist')}</small></div>
    ${canManage ? '<button type="button" data-action="remove-queue" aria-label="Remove from queue">×</button>' : ''}
  </article>`).join('');
}

function strings(value) {
  return Object.freeze(Array.isArray(value)
    ? value.filter(item => typeof item === 'string' && item.length <= TEXT_LIMIT).slice(0, 500) : []);
}

function musicFacets(value) {
  return Object.freeze({
    artists: strings(value.artists),
    albums: strings(value.albums),
    genres: strings(value.genres),
    years: Object.freeze(Array.isArray(value.years)
      ? value.years.filter(Number.isSafeInteger).slice(0, 500) : []),
  });
}
```

</details>

### 6. Anonymous Music entry asks the visitor to sign in

```text
HTTP 200 
X-Request-Id: bc32c4d3-ba63-4a52-b460-d6a5f4908776
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559545
Cache-Control: no-store
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 15:24:45 GMT
Connection: close

{"authenticated":false,"allowed":false,"canManage":false,"reason":"SIGN_IN_REQUIRED"}
```

### 7. A USER without Music permission is told Music read is required

```text
HTTP 200 
X-Request-Id: e60f5d9b-f2dd-481b-be7e-769612549ec7
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559545
Cache-Control: no-store
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 15:24:45 GMT
Connection: close

{"authenticated":true,"allowed":false,"canManage":false,"reason":"MUSIC_READ_REQUIRED"}
```

### 8. Anonymous catalog gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/music/2026-07-28/catalog'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/music/2026-07-28/catalog'}
```

### 9. Anonymous radio gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/music/2026-07-28/radio'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/music/2026-07-28/radio'}
```

### 10. Anonymous queue gets the same status and body as production (403)

```text
exit code: 0
--- stdout ---
candidate 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/music/2026-07-28/queue'}
production 403 {'status': 403, 'error': 'Forbidden', 'path': '/api/music/2026-07-28/queue'}
```

### 11. A USER without Music permission cannot read the catalog (403)

```text
HTTP 403 
X-Request-Id: 769a9c22-b940-4ca4-b3b8-c46fdf8d79ac
Cache-Control: private, no-store
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559547
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 121
Date: Fri, 09 Oct 2026 15:24:47 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 12. A USER without Music permission cannot change track preferences (403)

```text
HTTP 403 
X-Request-Id: 8f381c70-db00-4f4b-b9aa-8a9cb907a9f9
Cache-Control: private, no-store
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 119
X-RateLimit-Reset: 1791559548
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 121
Date: Fri, 09 Oct 2026 15:24:48 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 13. A USER without Music permission cannot queue a track (403)

```text
HTTP 403 
X-Request-Id: 5b0a22ab-270b-4e53-a3ae-56e359359fec
Cache-Control: private, no-store
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 118
X-RateLimit-Reset: 1791559548
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 121
Date: Fri, 09 Oct 2026 15:24:48 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

### 14. A USER cannot read the Music access log (403)

```text
HTTP 403 
X-Request-Id: c2c939ea-f44d-4fc0-915a-aaf870d5c5bd
Cache-Control: private, no-store
X-Content-Type-Options: nosniff
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791559548
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 121
Date: Fri, 09 Oct 2026 15:24:48 GMT
Connection: close

{"messages":[{"code":"ACCESS_DENIED","description":"Access is denied."}],"payload":null,"requestId":null,"success":false}
```

## Evidence
- Case 1 started 2026-10-09T10:24:43-05:00, took 47 ms, candidate `c50a86e`
- Case 2 started 2026-10-09T10:24:44-05:00, took 670 ms, candidate `c50a86e`
- Case 3 started 2026-10-09T10:24:44-05:00, took 45 ms, candidate `c50a86e`
- Case 4 started 2026-10-09T10:24:45-05:00, took 32 ms, candidate `c50a86e`
- Case 5 started 2026-10-09T10:24:45-05:00, took 31 ms, candidate `c50a86e`
- Case 6 started 2026-10-09T10:24:45-05:00, took 46 ms, candidate `c50a86e`
- Case 7 started 2026-10-09T10:24:45-05:00, took 61 ms, candidate `c50a86e`
- Case 8 started 2026-10-09T10:24:46-05:00, took 515 ms, candidate `c50a86e`
- Case 9 started 2026-10-09T10:24:46-05:00, took 390 ms, candidate `c50a86e`
- Case 10 started 2026-10-09T10:24:47-05:00, took 359 ms, candidate `c50a86e`
- Case 11 started 2026-10-09T10:24:47-05:00, took 46 ms, candidate `c50a86e`
- Case 12 started 2026-10-09T10:24:48-05:00, took 61 ms, candidate `c50a86e`
- Case 13 started 2026-10-09T10:24:48-05:00, took 45 ms, candidate `c50a86e`
- Case 14 started 2026-10-09T10:24:48-05:00, took 45 ms, candidate `c50a86e`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
