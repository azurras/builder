# ChristopherBell.dev Music Catalog Pagination Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the hidden 100-track Music result ceiling with complete, stable, 50-track server pages while preserving full-library radio selection.

**Architecture:** Extend the existing typed Music catalog boundary with page metadata and full-query counting. The browser owns only current view/filter/page state and fetches one page at a time; global radio continues using its separate 10,000-track candidate query.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, vanilla JavaScript modules, Thymeleaf, CSS, Node test runner, Gradle.

## Global Constraints

- Work from refreshed `origin/main` in an isolated worktree; preserve `A:\Projects\christopherbell.dev` unchanged.
- Use page size 50 in the UI and bound server page sizes to 1-100.
- Apply search, facets, favorites, and playlist selection before count and paging.
- End every catalog sort with unique `id` ordering.
- Never pass UI page/filter state into `radioCandidates(10_000)`.
- Keep Music authorization, no-store headers, path secrecy, and inline-only playback unchanged.
- Use one focused branch and PR; require CI, Dependency Review, and CodeQL before merge.

---

## Document Status

complete

## Objective

Show the true indexed Music result count and make every matching track reachable through accessible numbered pages without affecting playback or radio eligibility.

## Goals

- Return `page`, `size`, `totalTracks`, and `totalPages` with each catalog response.
- Fetch at most 50 tracks per normal browser request.
- Page All Music, Favorites, and playlist views over their complete server-side matches.
- Keep full-result facets and stable ordering.
- Prove radio still queries all eligible indexed tracks independently.

## Inputs

- Approved spec: `docs/specs/2026-07-28-christopherbell-dev-music-catalog-pagination.md`.
- Production evidence: 1,549 supported audio files below `A:\Shared\Music`; visible catalog reports 98 because the current API clamps at 100.
- Existing release: `baf8910dd6707260ec02af94c13d36c1eb2d6979`.

## Branch

- Base: refreshed `origin/main` at `baf8910dd6707260ec02af94c13d36c1eb2d6979` or its current descendant.
- Branch: `codex/music-catalog-pagination`.

## Non-Goals

- No radio weighting, playback, metadata, queue, history, or permission changes.
- No infinite scrolling or full-catalog browser download.
- No pagination for the bounded radio-history panel.

## Assumptions

- The Music reconciler continues incrementally indexing supported files independently of browsing.
- Global playlists remain bounded to 1,000 track IDs.
- The indexed READY count may be lower than the filesystem count when files fail probing; the UI total reports indexed playable matches truthfully.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add complete server-side catalog paging

Sequence / dependencies:
- First task; establishes the response contract consumed by the browser.

Expected files or modules:
- Modify catalog query/result/service, read controller/view, library playlist lookup, package documentation, and focused Java tests.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: a catalog request returns one stable page plus the full matching count; favorite and playlist queries operate before paging.
  - Invariants: only present READY tracks are returned; page size is 1-100; page is nonnegative and clamped after counting; path and download semantics remain hidden; radio uses a separate query.
  - Boundary/API: extend `MusicQuery`, `MusicCatalogResult`, and `MusicCatalogView`; keep `/api/music/2026-07-28/catalog` compatible through defaults while adding `page`, `size`, `favorite`, and `playlistId` parameters.
  - Effects and failures: Mongo count/distinct/page reads are bounded; an unknown playlist is a domain 404; empty playlists return an empty valid page; authorization remains checked before playlist lookup.
  - Tests and evidence: first add failing catalog/controller tests for 1,549 matches, page 1 size 50, clamped final page, favorite/playlist criteria, and a radio query whose limit remains 10,000.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/music/catalog/MusicQuery.java`
- Lines: 3-21
- Action: replace

Current:
```java
/** Bounded catalog search and optional exact facets. */
public record MusicQuery(
    String text,
    String artist,
    String album,
    String genre,
    int limit) {
  private static final int MAX_TEXT = 100;
  private static final int MAX_FACET = 300;

  public MusicQuery {
    text = bounded(text, MAX_TEXT);
    artist = bounded(artist, MAX_FACET);
    album = bounded(album, MAX_FACET);
    genre = bounded(genre, MAX_FACET);
    limit = Math.max(1, Math.min(100, limit));
  }
```

Proposed:
```java
/** Bounded catalog search, server-side view constraint, and page request. */
public record MusicQuery(
    String text,
    String artist,
    String album,
    String genre,
    Boolean favorite,
    List<String> trackIds,
    int page,
    int size) {
  private static final int MAX_TEXT = 100;
  private static final int MAX_FACET = 300;

  public MusicQuery {
    text = bounded(text, MAX_TEXT);
    artist = bounded(artist, MAX_FACET);
    album = bounded(album, MAX_FACET);
    genre = bounded(genre, MAX_FACET);
    trackIds = trackIds == null ? null : List.copyOf(trackIds);
    if (trackIds != null && trackIds.size() > 1_000) {
      throw new IllegalArgumentException("Music track filter is too large.");
    }
    page = Math.max(0, page);
    size = Math.max(1, Math.min(100, size));
  }
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-music-pagination'; .\gradlew.bat :website:test --tests "*MusicCatalog*" --tests "*MusicReadController*" --tests "*MusicRadioService*" --no-daemon`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/music/catalog/MusicCatalogResult.java`
- Lines: 5-9
- Action: replace

Current:
```java
public record MusicCatalogResult(
    List<MusicTrack> tracks,
    List<MusicAlbumGroup> albums,
    MusicFacets facets) {
}
```

Proposed:
```java
public record MusicCatalogResult(
    List<MusicTrack> tracks,
    List<MusicAlbumGroup> albums,
    MusicFacets facets,
    int page,
    int size,
    long totalTracks,
    int totalPages) {
}
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-music-pagination'; .\gradlew.bat :website:test --tests "*MusicCatalog*" --tests "*MusicReadController*" --no-daemon`

- [x] Write and run the backend RED tests.
- [x] Implement page/count/facet criteria and stable `id` tie ordering.
- [x] Resolve optional playlist IDs through the authorized library service and add favorite filtering.
- [x] Prove `radioCandidates(10_000)` remains independent, run focused tests, and commit Task 1.

### Task 2 - Render complete numbered pages and deliver

Sequence / dependencies:
- Runs after Task 1 because the UI validator and state require the final response contract.

Expected files or modules:
- Modify Music API builder, response validator, page controller, template, CSS, frontend documentation, JavaScript tests, and production smoke coverage where appropriate.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: listeners see the real result total and can move through compact numbered pages while search/filter/view changes reset to page zero.
  - Invariants: only current-page tracks live in browser catalog state; active media is untouched; all URL values are encoded; invalid response metadata fails closed before rendering.
  - Boundary/API: `API.music.catalog` accepts page/view filters; `musicCatalog` validates pagination; `/music` gains one navigation region below results.
  - Effects and failures: each navigation causes one abort-safe catalog GET; failed pages retain an actionable error; double clicks cannot apply stale responses; boundary buttons disable correctly.
  - Tests and evidence: first add failing JS tests for metadata validation and compact page windows, then source/DOM assertions for accessible controls and view-specific requests.

#### Code Edit 2.1
- File: `website/src/main/resources/static/js/lib/music.js`
- Lines: 32-45
- Action: replace

Current:
```javascript
export function musicCatalog(value) {
  if (!Array.isArray(value?.tracks) || typeof value?.facets !== 'object') {
    throw new Error('Music returned an invalid catalog.');
  }
  return Object.freeze({
    tracks: Object.freeze(value.tracks.map(musicTrack)),
    facets: Object.freeze({
      artists: strings(value.facets.artists),
      albums: strings(value.facets.albums),
      genres: strings(value.facets.genres),
      years: Object.freeze(Array.isArray(value.facets.years)
        ? value.facets.years.filter(Number.isSafeInteger).slice(0, 500) : []),
    }),
  });
}
```

Proposed:
```javascript
export function musicCatalog(value) {
  const validPage = Number.isSafeInteger(value?.page) && value.page >= 0;
  const validSize = Number.isSafeInteger(value?.size) && value.size >= 1 && value.size <= 100;
  const validTotal = Number.isSafeInteger(value?.totalTracks) && value.totalTracks >= 0;
  const validPages = Number.isSafeInteger(value?.totalPages) && value.totalPages >= 0;
  if (!Array.isArray(value?.tracks) || typeof value?.facets !== 'object'
      || !validPage || !validSize || !validTotal || !validPages
      || value.tracks.length > value.size) {
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
```

Verification:
- `node --test website/src/test/js/music.test.js`

#### Code Edit 2.2
- File: `website/src/main/resources/templates/music.html`
- Lines: after 51
- Action: add

Proposed:
```html
        <nav id="music-pagination" class="music-pagination" aria-label="Music result pages" hidden></nav>
```

Verification:
- `node --test website/src/test/js/music.test.js`
- `node --check website/src/main/resources/static/js/music.js`

- [x] Write and run the frontend RED tests.
- [x] Add typed page URL construction, validated state, compact page-window rendering, and accessible controls.
- [x] Make All Music, Favorites, and playlists request complete server-filtered pages without touching the media player.
- [x] Run focused and full checks, validate on a non-8080 port, commit/push, open one PR, merge after green CI/CodeQL, and smoke production totals plus radio.

## Code Changes

- `MusicQuery.java`: replace the single result limit with typed page/view constraints.
- `MusicCatalogResult.java`, `MusicCatalogView.java`: add page metadata.
- `MusicCatalog.java`: count full criteria, clamp page, fetch stable page, compute full-result facets, preserve radio query.
- `MusicReadController.java`, `MusicLibraryService.java`: accept favorite/playlist page constraints and resolve playlists safely.
- `api.js`, `lib/music.js`, `music.js`: build, validate, own, and render page state.
- `music.html`, `music.css`: add responsive accessible pagination controls.
- Java/JavaScript tests and Music documentation: prove the new contract and full-library radio independence.

## Files and Modules

- `website/src/main/java/dev/christopherbell/music/catalog/*`
- `website/src/main/java/dev/christopherbell/music/library/MusicLibraryService.java`
- `website/src/main/java/dev/christopherbell/music/web/MusicReadController.java`
- `website/src/main/java/dev/christopherbell/music/web/MusicCatalogView.java`
- `website/src/main/resources/static/js/{lib/api.js,lib/music.js,music.js}`
- `website/src/main/resources/{templates/music.html,static/css/music.css}`
- Focused tests under `website/src/test/java/.../music` and `website/src/test/js/music.test.js`

## Unit Testing

- Java: page normalization, full counts, page clamp, stable sort, full facets, favorite/playlist constraints, empty results, and 10,000-track radio query independence.
- JavaScript: response metadata rejection, page-window calculation, boundary controls, true totals, page reset, encoded view filters, and template safety.

## Local Testing

- Use isolated `GRADLE_USER_HOME=A:\Temp\gradle-music-pagination`.
- Run the packaged app on a non-8080 port with a fixture catalog exceeding 100 tracks.
- Send authenticated catalog requests for pages 0, 1, and final; verify 50-track bounds, stable non-overlapping IDs, true totals, search/favorite/playlist results, and 403 anonymous denial.
- Verify page navigation on desktop/mobile does not interrupt the persistent player; join radio and confirm its track can originate outside the visible page.

## Validation

- Focused Java and Node tests pass from RED to GREEN.
- `:website:check` passes.
- One PR passes Ubuntu, macOS, Windows, Dependency Review, and CodeQL.
- Automatic deployment publishes the merge SHA without prompts.
- Production All Music reports the indexed total and page count; later pages load; radio continues normally.

## Rollback or Recovery

- Before merge, delete only the isolated branch/worktree if abandoned.
- After merge, automatic release rollback can restore the prior application artifact; Mongo schema is unchanged.
- The old API call shape remains accepted through default page and size values.

## Risks

- Count/facet queries add Mongo work; keep criteria indexed where possible and responses bounded.
- Non-unique sort fields can duplicate/skip rows; always append unique `id`.
- Playlist/favorite filtering after paging would remain incomplete; apply every view constraint in Mongo before count/skip/limit.
- UI pagination could accidentally recreate the player; change only Music result DOM and leave the top-document player untouched.

## Completion Criteria

- The approved spec is mapped to passing tests and runtime evidence.
- All indexed matching tracks are reachable through 50-track pages with truthful totals.
- All Music, Favorites, and playlists are complete server-filtered views.
- Radio remains independent and eligible for all present READY non-excluded tracks up to its 10,000 bound.
- PR is merged after required checks, automatic production deployment completes, and production paging/radio smoke passes.
- Builder test report, closure, session memory, indexes, validation, commit, and push are complete.
