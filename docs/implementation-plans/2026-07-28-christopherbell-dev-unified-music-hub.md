# christopherbell.dev Unified Music Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver one shared, permissioned Music hub with an indexed library, server-owned radio and queue, persistent site-wide playback, direct tag editing with undo, denied-access auditing, and durable browser sessions.

**Architecture:** Extend the existing Spring Boot/MongoDB/shared-folder foundation with a dedicated `music` bounded context. Music authorization remains independent of shared-folder authorization, while filesystem confinement and progressive media primitives are reused behind Music-specific APIs that never expose download semantics. The existing top-document player remains the sole browser media owner and switches between an expanded `/music` presentation and its compact site-wide bar without replacing the media element.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Security 7, Spring Data MongoDB, Thymeleaf, vanilla JavaScript web components, CSS, Node test runner, FFmpeg/FFprobe, Gradle.

## Global Constraints

- Work in `A:\Projects\christopherbell.dev-worktrees\unified-music-hub` on branch `codex/unified-music-hub`, based on refreshed `origin/main`.
- Preserve the dirty production checkout at `A:\Projects\christopherbell.dev`; never implement or commit from it.
- Use one feature branch and one pull request for the complete Music Hub delivery.
- Invoke `chris-street-style` before every production-code, test, executable-template, configuration, migration, or automation edit.
- `MUSIC_READ` and `MUSIC_WRITE` are independent of `SHARED_FOLDER_READ` and `SHARED_FOLDER_WRITE`.
- `MUSIC_WRITE` implies `MUSIC_READ`; `ADMIN` receives both music capabilities effectively; removing read removes write.
- Neither music capability grants downloads. Shared-folder download access remains governed only by shared-folder capabilities.
- Music is a top-level navigation item visible to everyone.
- Anonymous and authenticated denied Music entry attempts are recorded; anonymous IP data expires after 30 days and repeated attempts are aggregated.
- The shared radio timeline, queue, playlists, favorites, exclusions, and history are global, not per-user silos.
- Browser sessions use a seven-day sliding inactivity limit and a 30-day absolute limit; streaming, radio polling, and other background traffic do not renew sessions.
- The player remains same-tab only and must not pause, reload, or seek when moving between `/music` and another site route.
- Direct metadata edits must preserve audio streams, use exact-revision checks, create private 30-day backups, validate staged output, replace atomically, and support revision-checked undo.
- Validate locally on a non-8080 port before any production listener rotation.

---

## Document Status

complete

## Objective

Replace the shared-folder-only radio experience with a first-class Music hub that is fast to browse, safe to administer, available across the site through the persistent player, and governed by purpose-built permissions.

## Goals

- Add and enforce `MUSIC_READ` and `MUSIC_WRITE` throughout account administration and Music APIs.
- Create a Mongo-backed, incrementally reconciled catalog for `A:\Shared\Music` with server-probed metadata, duration, and artwork.
- Add one durable shared smart-radio timeline and queue with global playlists, favorites, exclusions, and listening history.
- Provide a responsive `/music` page with search, library facets, queue, history, playlists, and writer-only management.
- Keep the same media element alive as the Music player expands on `/music` and collapses elsewhere.
- Support safe direct tag and artwork changes with backups and undo.
- Record denied Music access in a filterable Back Office view.
- Replace the one-day browser cookie behavior with revocable seven-day-idle/30-day-absolute browser sessions without changing explicit bearer-token semantics.

## Inputs

- Approved specification: `docs/specs/2026-07-28-christopherbell-dev-unified-music-hub.md`.
- Current spoke baseline: `origin/main` at `bf1b7468` (`Keep radio timeline continuous between listeners (#1311)`).
- Baseline verification on 2026-07-28: `GRADLE_USER_HOME=A:\Temp\gradle-unified-music-hub .\gradlew.bat :website:test --no-daemon`; 1,202 tests, 0 failures, 0 errors, 3 skipped.
- Existing foundations: `SharedFolderAccessService`, rooted shared-folder boundaries, media transcode worker, `SharedFolderRadioService`, `site-media-player`, Back Office account drawer, and trusted `ClientIpResolver`.

## Branch

- Base: `origin/main` at `bf1b7468`.
- Work branch: `codex/unified-music-hub`.
- Delivery: one pull request into `main`, then automated deployment and production smoke verification.

## Non-Goals

- No per-user libraries, stations, queues, favorites, or playlists.
- No public or anonymous Music streaming.
- No Music download endpoint and no attachment content disposition from Music APIs.
- No replacement with Jellyfin, Navidrome, FTP, or another external media server.
- No audio re-encoding during metadata-only edits.
- No multi-tab playback coordination.
- No pagination requirement for the Music library; bounded search and grouped views are sufficient.

## Assumptions

- Production continues to expose the shared root as `A:\Shared` and the music subtree as `A:\Shared\Music`.
- FFmpeg and FFprobe are provisioned by the existing Windows production media-tool workflow.
- MongoDB is available to the native Windows application service.
- Existing progressive transcode jobs and rooted path validation remain the authoritative low-level media/file boundaries.
- The current automatic push-to-main deployment remains the release mechanism.

## Open Questions

None.

## File Structure

- `website/src/main/java/dev/christopherbell/music/security/`: fresh account authorization and denied-entry audit recording.
- `website/src/main/java/dev/christopherbell/music/catalog/`: durable tracks, bounded reconciliation, FFprobe boundary, search/facets, artwork.
- `website/src/main/java/dev/christopherbell/music/playback/`: Music-only direct/range/transcode delivery with inline-only semantics.
- `website/src/main/java/dev/christopherbell/music/radio/`: shared station state, selection policy, queue, and transition history.
- `website/src/main/java/dev/christopherbell/music/library/`: global playlists, favorites, exclusions, and history queries.
- `website/src/main/java/dev/christopherbell/music/metadata/`: staged tag rewrite, private backups, validation, replacement, and undo.
- `website/src/main/java/dev/christopherbell/music/web/`: access probe and Music read/write/admin HTTP boundaries.
- `website/src/main/resources/templates/music.html`: data-free responsive Music shell.
- `website/src/main/resources/static/js/music.js` and `static/js/lib/music.js`: UI effects and pure response/state helpers.
- `website/src/main/resources/static/css/music.css`: Music layout and expanded player presentation.
- `website/src/main/java/dev/christopherbell/configuration/security/browser/`: opaque browser-session persistence, rotation, renewal classification, and revocation.

## Task Breakdown

### Task 1 - Add independent Music permissions and Back Office controls

Sequence / dependencies:
- Runs first because every later Music boundary depends on a single effective-permission model.

Expected files or modules:
- Modify `website/src/main/java/dev/christopherbell/account/model/AccountPermission.java`.
- Create `website/src/main/java/dev/christopherbell/account/model/dto/MusicPermissionUpdate.java`.
- Create `website/src/main/java/dev/christopherbell/music/security/MusicAccessService.java`.
- Modify `AccountService.java`, `AccountController.java`, `back-office.html`, `back-office.js`, `lib/back-office-users.js`, and `lib/api.js`.
- Add Java and JavaScript permission-matrix tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: admins can grant/revoke Music read/write separately from Shared Folder permissions; Music write always entails Music read.
  - Invariants: changing one capability family preserves the other family; admins have effective Music read/write without stored grants; removing Music read removes Music write.
  - Boundary/API: add `PATCH /api/accounts/2026-07-28/{accountId}/music-permissions` with `{read, write}`; retain the existing shared-folder endpoint.
  - Effects and failures: one account document update plus an admin audit event; malformed write-without-read is 400, missing accounts are 404, stale/deactivated callers fail closed.
  - Tests and evidence: start with effective permission and family-preservation failures, then controller and Back Office state tests.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/account/model/AccountPermission.java`
- Lines: 6-9
- Action: replace

Current:
```java
public enum AccountPermission {
  SHARED_FOLDER_READ,
  SHARED_FOLDER_WRITE
}
```

Proposed:
```java
public enum AccountPermission {
  SHARED_FOLDER_READ,
  SHARED_FOLDER_WRITE,
  MUSIC_READ,
  MUSIC_WRITE
}
```

Verification:
- `./gradlew.bat :website:test --tests "*MusicAccessServiceTest" --tests "*AccountServiceTest"`

- [x] Write failing tests for every role/capability combination and cross-family preservation.
- [x] Implement the enum, access service, DTO, account endpoint, and audit event.
- [x] Add the Music checkboxes to the existing user drawer with admin-disabled defaults.
- [x] Run focused Java and Node tests and commit the independently passing permission slice.

### Task 2 - Add durable browser sessions with sliding inactivity and revocation

Sequence / dependencies:
- Runs after Task 1 so permission changes can revoke browser sessions consistently.

Expected files or modules:
- Create `configuration/security/browser/BrowserSession.java`, `BrowserSessionRepository.java`, `BrowserSessionService.java`, and `InteractiveBrowserRequest.java`.
- Modify `BrowserAuthenticationCookies.java`, `JwtAuthenticationFilter.java`, `AccountController.java`, account moderation/deletion/password-reset services, and browser-security configuration.
- Add deterministic clock-based tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: normal browser login creates an opaque revocable session with seven-day idle and 30-day absolute limits; interactive requests renew and rotate it.
  - Invariants: explicit bearer JWT validation/lifetime is unchanged; raw session tokens are never stored; absolute expiry never moves; background/media requests never extend idle expiry.
  - Boundary/API: `CBELL_AUTH` becomes an opaque browser session credential only in cookie mode; bearer headers remain JWTs.
  - Effects and failures: login stores one hashed session; eligible requests may update/rotate it; logout, reset, suspension, deletion, and role/capability changes revoke sessions; repository failures fail closed.
  - Tests and evidence: fake-clock tests cover day 7, day 30, rotation overlap, excluded routes, and every revocation trigger.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/BrowserAuthenticationCookies.java`
- Lines: 10-46
- Action: replace

Current:
```java
public class BrowserAuthenticationCookies {
  public static final String AUTH_COOKIE_NAME = "CBELL_AUTH";
  public static final String AUTH_STATE_COOKIE_NAME = "CBELL_AUTH_STATE";
  private static final Duration AUTH_LIFETIME = Duration.ofDays(1);

  public List<ResponseCookie> authenticated(String jwt) {
    return List.of(
        cookie(AUTH_COOKIE_NAME, jwt, true, AUTH_LIFETIME),
        cookie(AUTH_STATE_COOKIE_NAME, "1", false, AUTH_LIFETIME));
  }
}
```

Proposed:
```java
public class BrowserAuthenticationCookies {
  public static final String AUTH_COOKIE_NAME = "CBELL_AUTH";
  public static final String AUTH_STATE_COOKIE_NAME = "CBELL_AUTH_STATE";
  static final Duration ABSOLUTE_LIFETIME = Duration.ofDays(30);

  public List<ResponseCookie> authenticated(String opaqueSessionToken) {
    if (opaqueSessionToken == null || opaqueSessionToken.isBlank()) {
      throw new IllegalArgumentException("Authenticated browser cookie requires a session token.");
    }
    return List.of(
        cookie(AUTH_COOKIE_NAME, opaqueSessionToken, true, ABSOLUTE_LIFETIME),
        cookie(AUTH_STATE_COOKIE_NAME, "1", false, ABSOLUTE_LIFETIME));
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*BrowserSession*" --tests "*JwtAuthenticationFilterTest" --tests "*AccountControllerTest"`

- [x] Write fake-clock failures for idle expiry, absolute expiry, rotation, and excluded background traffic.
- [x] Implement hashed opaque sessions and bearer/cookie credential separation.
- [x] Add revocation hooks to logout and sensitive account mutations.
- [x] Run security tests and commit the browser-session slice.

### Task 3 - Build the bounded Mongo Music catalog and server metadata probe

Sequence / dependencies:
- Runs after Task 1; it can proceed independently of the browser-session internals.

Expected files or modules:
- Create catalog document/repository/query/probe/reconciliation/artwork classes under `music/catalog`.
- Create `MusicProperties.java` and add `app.music` configuration to all profiles.
- Add Mongo index migration and scanner/probe tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: `/music` reads a durable catalog containing path, exact revision, tags, duration, codecs, and artwork for files below `Music/`.
  - Invariants: paths remain rooted and relative; a catalog row is playable only when its revision matches disk; scans are bounded; malformed probe output never becomes trusted metadata.
  - Boundary/API: `MusicCatalog.search(MusicQuery)` returns bounded grouped results; `MusicProbe.probe(Path)` returns a validated `MusicProbeResult`.
  - Effects and failures: scheduled reconciliation probes at most 100 changed files per pass, marks missing rows, and never blocks request threads on a full-tree scan; probe timeout/error preserves the last valid row and records status.
  - Tests and evidence: fixture probe JSON, changed/unchanged/missing files, cursor restart, malicious tags, huge artwork, and Mongo query bounds.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/music/catalog/MusicTrack.java`
- Lines: 1-31
- Action: add

Proposed:
```java
@Document("music_tracks")
public record MusicTrack(
    @Id String id,
    @Indexed(unique = true) String path,
    String observedToken,
    String title,
    String artist,
    String albumArtist,
    String album,
    Integer trackNumber,
    Integer discNumber,
    String genre,
    Integer year,
    double durationSeconds,
    String audioCodec,
    String container,
    String artworkRevision,
    boolean favorite,
    boolean excludedFromRadio,
    Instant indexedAt,
    Instant missingSince) {
  public boolean present() {
    return missingSince == null;
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*MusicCatalog*" --tests "*MusicProbe*" --tests "*MusicArtwork*"`

- [x] Write probe-boundary and reconciliation failures from fixed filesystem fixtures.
- [x] Implement documents, indexes, validated FFprobe invocation, and bounded scanner state.
- [x] Add artwork extraction/thumbnail caching with byte and dimension limits.
- [x] Run catalog tests and commit the catalog slice.

### Task 4 - Add Music entry auditing and stream-only read APIs

Sequence / dependencies:
- Runs after Tasks 1 and 3 because access responses expose catalog readiness and streams resolve exact catalog revisions.

Expected files or modules:
- Create `music/security/MusicAccessAttempt.java`, repository, recorder, query service, and controller.
- Create `music/playback/MusicPlaybackService.java` and `music/web/MusicReadController.java`.
- Modify `ContentViewController.java`, `SecurityConfig.java`, `SharedFolderNoStoreFilter.java`, and API constants.
- Add Back Office audit panel and filters.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: Music is visible in nav to everyone; the public shell distinguishes sign-in-required from permission-denied, records the attempt, and authorized listeners can search/stream without downloading.
  - Invariants: access reloads fresh account state; anonymous identity is only a trusted resolved IP; Music responses are private/no-store; no Music route emits attachment disposition.
  - Boundary/API: public `GET /api/music/2026-07-28/access`; protected `GET /catalog`, `/tracks/{id}/stream`, `/tracks/{id}/artwork`; admin `GET /admin/access-attempts`.
  - Effects and failures: denied entries upsert a bounded aggregation bucket and expire after 30 days; invalid ranges return 416; changed files return 409 and trigger reindex; all repository failures fail closed.
  - Tests and evidence: anonymous/account audit identity, proxy trust, aggregation, TTL, read denial, byte ranges, `Content-Disposition: inline`, and absence of any download endpoint.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/view/content/ContentViewController.java`
- Lines: after 83
- Action: add

Proposed:
```java
  /** Serves the data-free Music hub shell; API authorization decides the rendered access state. */
  @GetMapping(value = "/music")
  public String getMusicPage() {
    return "music.html";
  }
```

Verification:
- `./gradlew.bat :website:test --tests "*MusicAccess*" --tests "*MusicReadControllerTest" --tests "*ContentViewControllerTest"`

- [x] Write denied-access, trusted-IP, aggregation, and negative-download tests.
- [x] Implement public access probe, audit persistence/query, and Back Office panel.
- [x] Implement revision-checked range streaming and Music-specific transcode admission.
- [x] Run focused security/controller tests and commit the access/stream slice.

### Task 5 - Replace the basic radio with a server-owned smart timeline and shared queue

Sequence / dependencies:
- Runs after Tasks 3 and 4 because the station selects catalog rows and returns Music stream identities.

Expected files or modules:
- Create radio state, queue item, history event, repositories, selector, timeline service, and read/write controllers under `music/radio`.
- Modify the existing site player radio client to use Music APIs and catalog-owned durations.
- Retire browser duration-report writes and the shared-folder radio UI entry point.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: all listeners join approximately the same durable station position; queued songs override radio and smart radio resumes when the queue empties.
  - Invariants: duration comes only from the catalog; immediate track repeats are forbidden when alternatives exist; exclusions never play; one transition creates one history event; queue mutations require Music write.
  - Boundary/API: `GET /radio`, `GET /queue`, and writer-only `POST/PATCH/DELETE /queue`; response identity is `(stationSequence, trackId, observedToken)`.
  - Effects and failures: one lock/compare-and-set owns transitions; missing/unplayable queued items are skipped and recorded; restarts reconstruct position from durable start/duration without a listener.
  - Tests and evidence: deterministic clock/random tests cover favorites weighting, least-recently-heard preference, track/artist cooldowns, occasional exploration, queue precedence, multi-song catch-up, restart, and no-listener advancement.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioState.java`
- Lines: 1-23
- Action: add

Proposed:
```java
@Document("music_radio_state")
public record MusicRadioState(
    @Id String id,
    long stationSequence,
    String trackId,
    String observedToken,
    Instant startedAt,
    double durationSeconds,
    Source source,
    long version) {
  public static final String ID = "global";

  public enum Source {
    RADIO,
    QUEUE
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*MusicRadio*" --tests "*MusicQueue*" && node --test website/src/test/js/site-media-player.test.js`

- [x] Write deterministic selection and timeline failures first.
- [x] Implement durable station/queue/history state and atomic transitions.
- [x] Switch the player from shared-folder radio endpoints to Music radio endpoints and delete duration reporting.
- [x] Run radio/player tests and commit the station slice.

### Task 6 - Add global playlists, favorites, exclusions, and listening history

Sequence / dependencies:
- Runs after Task 5 because queue/radio transitions consume shared preference and playlist state.

Expected files or modules:
- Create `music/library/MusicPlaylist.java`, repository/service/controller, preference mutations, and history queries.
- Extend catalog/radio query projections.
- Add authorization and concurrency tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: listeners can view shared playlists/history; writers can create/edit/delete playlists, favorite tracks, and exclude tracks from radio.
  - Invariants: preferences and playlists are global; exclusion affects radio only and does not hide manual playback; mutations use exact version checks; history is append-only and bounded in reads.
  - Boundary/API: read endpoints under `/api/music/2026-07-28/library`; writer mutations use CSRF-protected POST/PATCH/DELETE and return the saved version.
  - Effects and failures: Mongo writes are optimistic; conflicts return 409; removed tracks remain identifiable in history but are skipped in playlists/queue.
  - Tests and evidence: read/write permission matrix, lost-update conflict, favorite weight input, exclusion behavior, and bounded history ordering.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/music/library/MusicPlaylist.java`
- Lines: 1-17
- Action: add

Proposed:
```java
@Document("music_playlists")
public record MusicPlaylist(
    @Id String id,
    @Indexed(unique = true) String normalizedName,
    String name,
    List<String> trackIds,
    long version,
    String updatedByAccountId,
    Instant updatedAt) {
  public MusicPlaylist {
    trackIds = List.copyOf(trackIds);
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*MusicPlaylist*" --tests "*MusicPreference*" --tests "*MusicHistory*"`

- [x] Write global-state, authorization, conflict, and bounds tests.
- [x] Implement playlist, preference, and history services/controllers.
- [x] Wire preference projections into smart-radio selection.
- [x] Run focused tests and commit the shared-library slice.

### Task 7 - Add safe direct metadata editing, private backups, and undo

Sequence / dependencies:
- Runs after Task 3 because editing is revision-checked against the catalog and refreshes the same track identity.

Expected files or modules:
- Create metadata request/result, process boundary, backup document/store, edit service, cleanup, and write controller under `music/metadata`.
- Add configuration for private backup root, process timeouts, size limits, and 30-day retention.
- Add FFmpeg fixture and failure-injection tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: writers can change approved text tags and embedded artwork without re-encoding audio, and can undo a selected edit while its backup is retained.
  - Invariants: exact observed revision is rechecked before stage and replacement; original is backed up privately before mutation; staged output retains audio codec/duration within tolerance; replacement is atomic; unsupported containers remain read-only.
  - Boundary/API: `PATCH /tracks/{id}/metadata` accepts expected revision and typed fields; `POST /metadata-edits/{id}/undo` accepts the current expected revision.
  - Effects and failures: bounded FFmpeg/FFprobe processes write only private staging; any failure leaves the original unchanged; success refreshes catalog and records an audit; backups expire after 30 days.
  - Tests and evidence: supported/unsupported formats, revision race, process timeout, malformed output, artwork bounds, codec/duration preservation, atomic swap failure, cleanup, and undo conflict.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/music/metadata/MusicMetadataUpdate.java`
- Lines: 1-14
- Action: add

Proposed:
```java
public record MusicMetadataUpdate(
    String expectedObservedToken,
    String title,
    String artist,
    String albumArtist,
    String album,
    Integer trackNumber,
    Integer discNumber,
    String genre,
    Integer year,
    String artworkDataUrl,
    boolean removeArtwork) {
}
```

Verification:
- `./gradlew.bat :website:test --tests "*MusicMetadata*" --tests "*MusicBackup*" --tests "*MusicTagProcess*"`

- [x] Write revision, process, preservation, atomicity, and undo failures first.
- [x] Implement strict request validation and configured process boundary.
- [x] Implement private checksum-bound backups, staged probe validation, atomic replace, audit, refresh, and cleanup.
- [x] Run fixture tests and commit the metadata slice.

### Task 8 - Build the responsive Music hub and expanded/compact player handoff

Sequence / dependencies:
- Runs after Tasks 4-7 so UI work binds to stable read/write response contracts.

Expected files or modules:
- Create `music.html`, `music.js`, `lib/music.js`, and `music.css`.
- Modify `nav.js`, `app.js`, `components/site-media-player.js`, `lib/site-media-player.js`, `main.css`, and API constants.
- Add Node tests plus desktop/mobile browser flows.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: everyone sees Music in main nav; authorized listeners get search, Albums/Artists/Songs/Genres/Folders, playlists, queue, history, and an expanded player; elsewhere the same player collapses to the bottom bar.
  - Invariants: one top-document media element owns playback; route changes move/present that element without changing its source/currentTime/paused state; unauthorized shells never fetch catalog or stream data; writer controls remain absent or disabled for readers.
  - Boundary/API: Music page coordinates with the player through typed custom events and explicit `setPresentation('expanded'|'compact')`; persistent navigation stays same-origin and same-tab.
  - Effects and failures: catalog requests are abortable and bounded; failed artwork/search does not stop playback; browser autoplay denial restores position and shows one tap-to-resume control.
  - Tests and evidence: pure response validation, permission rendering, search/facet state, player node identity/currentTime preservation, refresh restoration, mobile selected-content placement, and desktop/mobile visual smoke.

#### Code Edit 8.1
- File: `website/src/main/resources/static/js/components/nav.js`
- Lines: 45-51
- Action: replace

Current:
```javascript
export function topLevelNavItems(isAuthenticated) {
    return [
        { href: '/void', label: 'Feed' },
        { href: messagesNavHref(isAuthenticated), label: 'Messages' },
    ];
}
```

Proposed:
```javascript
export function topLevelNavItems(isAuthenticated) {
    return [
        { href: '/void', label: 'Feed' },
        { href: '/music', label: 'Music' },
        { href: messagesNavHref(isAuthenticated), label: 'Messages' },
    ];
}
```

Verification:
- `node --test website/src/test/js/music.test.js website/src/test/js/site-media-player.test.js website/src/test/js/nav.test.js`

- [x] Write response, permission, navigation, and player-handoff failures first.
- [x] Build the responsive shell and pure state/render helpers.
- [x] Add expanded player presentation while retaining the existing compact bar and media owner.
- [x] Verify desktop and mobile flows through the local app and commit the UI/player slice.

### Task 9 - Integrate configuration, run full verification, deliver, and deploy

Sequence / dependencies:
- Runs after all implementation tasks and is the only integration/release task.

Expected files or modules:
- Modify application profiles, production environment examples, rate limits, README/operations docs, and deployment smoke checks only as required by implemented contracts.
- Add or update end-to-end and production smoke tests.

Implementation notes:
- Required skill: `chris-street-style` before any code/config/test/automation edits.
- Before-Edit Brief:
  - Behavior: a push to `main` deploys the complete Music Hub non-interactively and production serves the expected access/nav/player/radio flows.
  - Invariants: no interactive `Y` prompts or Windows elevation dialogs in deployment; live port 8080 is untouched until alternate-port verification passes; unrelated dirty production checkout state is preserved.
  - Boundary/API: configuration names and environment variables are documented and validated at startup; production smoke uses only safe test accounts/data and read-only probes except an explicitly reversible admin grant test.
  - Effects and failures: CI or alternate-port failure prevents merge/cutover; deployment failure keeps the previous release recoverable; migrations/index creation are idempotent.
  - Tests and evidence: full Gradle/Node/Pester suite, alternate-port app verification, PR CI/CodeQL, merge, automatic deployment logs, external production smoke, and service/listener status.

#### Code Edit 9.1
- File: `website/src/main/resources/application.yml`
- Lines: after 132
- Action: add

Proposed:
```yaml
  music:
    root: ${APP_MUSIC_ROOT:${app.shared-folder.root}/Music}
    reconcile-delay: 30s
    reconcile-batch-size: 100
    probe-timeout: 20s
    artwork-max-bytes: 5MB
    access-audit-retention: 30d
    metadata-backup-retention: 30d
    radio-track-cooldown: 50
    radio-artist-cooldown: 10
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-unified-music-hub'; .\gradlew.bat clean test check --no-daemon`
- `node --test website/src/test/js/*.test.js`
- `Invoke-Pester ops/production/windows/tests -CI`
- Start with `SPRING_PROFILES_ACTIVE=prod` on a non-8080 port and exercise anonymous denial, authorized catalog/radio/stream, writer mutation, session renewal exclusion, and player navigation.

- [x] Add startup validation, production defaults, dedicated rate limits, and non-interactive deployment smoke.
- [x] Run all automated suites and fix every regression.
- [x] Run alternate-port desktop/mobile/local runtime verification and save the Builder test report.
- [x] Commit/push the spoke branch, open one PR, wait for CI/CodeQL, merge, verify automatic production deployment, smoke production, close work, and save session memory.

## Code Changes

- Account authorization: extend `AccountPermission`, add Music-specific effective access and capability-family-preserving admin mutations.
- Browser security: replace JWT-in-cookie handling with opaque durable browser sessions while retaining explicit bearer JWT behavior.
- Catalog: add Music track/index/probe/reconciliation/artwork documents and services.
- Access and playback: add public access-status auditing plus protected Music-only catalog, artwork, range stream, and transcode boundaries.
- Radio: add durable smart selection, global queue, and one-event-per-transition history; remove browser duration authority.
- Shared library: add global playlists, favorites, exclusions, and history queries/mutations.
- Metadata: add revision-checked tag/artwork rewrite, private backups, atomic replace, cleanup, and undo.
- Front end: add top-level Music nav, responsive Music hub, and expanded/compact presentation of the same persistent player.
- Operations: add bounded configuration, rate limits, smoke checks, and idempotent Mongo indexes.

## Files and Modules

- Existing: account model/service/controller, Spring security filter/cookies/config, shared-folder boundaries/media worker, content routes, persistent player, nav, Back Office, application profiles, deployment tests.
- New: `music/security`, `music/catalog`, `music/playback`, `music/radio`, `music/library`, `music/metadata`, `music/web`, browser-session persistence, Music template/JS/CSS, and focused tests.

## Unit Testing

- Use TDD for each task: failing focused test, minimal implementation, focused pass, then integration pass.
- Java: permission matrix, session clock/revocation, probe validation, reconciliation, stream ranges/no-download, access aggregation/TTL, radio selection/timeline/queue, playlist/preference conflicts, metadata atomicity/undo.
- JavaScript: response validators, nav visibility, Music state/rendering, shared player node identity, expanded/compact presentation, autoplay recovery, and radio synchronization.
- PowerShell: production configuration/startup validation and fully non-interactive deployment behavior.

## Local Testing

- Use isolated `GRADLE_USER_HOME=A:\Temp\gradle-unified-music-hub` to avoid Windows Gradle registry locks.
- Run the full app against test/local Mongo with a fixture Music root containing MP3, FLAC, M4A, MKV/video negative cases, embedded artwork, missing metadata, unsupported tag-write formats, and revision races.
- Start on a non-8080 port and verify anonymous, Music reader, Music writer, Shared-only reader, combined permission, and admin accounts.
- Verify desktop and mobile layouts, selection placement, continuous playback across `/music`, `/void`, `/messages`, and Shared Folder navigation, same-position refresh restore, and tap-to-resume handling.
- Confirm radio state remains close across two independent browsers, advances without a listener, obeys queue overrides, and survives restart.
- Confirm Music routes cannot produce attachment downloads and Shared Folder download continues to work only for shared-folder readers.

## Validation

- `:website:test`, repository `check`, Node tests, and Windows Pester tests pass with zero failures.
- Security negative tests prove every forbidden permission/download combination.
- Alternate-port runtime demonstrates all key API and UI flows before live listener changes.
- PR CI and CodeQL are green.
- Push to `main` deploys without prompts or approval dialogs.
- Production external smoke confirms navigation, access denial/logging, catalog/search, radio/queue, streaming, player handoff, and Back Office permission/audit views.

## Rollback or Recovery

- Before merge, rollback is branch deletion; production remains unchanged.
- Deployment retains the prior release so service rollback can point WinSW to the previous verified artifact.
- New Mongo collections and fields are additive; older application versions ignore them.
- Music metadata mutation backups are private and retained for 30 days; undo remains revision-checked.
- If Music startup validation fails, disable the Music scanner/API through configuration without weakening Shared Folder protections, then roll back the application release.
- Never reset or clean the dirty `A:\Projects\christopherbell.dev` checkout; production recovery uses release artifacts and service controls.

## Risks

- Large libraries can overload disk/process/Mongo resources; mitigate with bounded scan batches, one probe pool, strict timeouts, cached thumbnails, and bounded queries.
- FFmpeg format behavior varies; allow metadata writes only for fixture-proven containers and fail closed otherwise.
- Radio transition races can duplicate history or skip queue items; use one durable versioned state and atomic compare-and-set transitions.
- Browser autoplay can prevent immediate sound after refresh; preserve state and provide a single explicit tap-to-resume path because browsers prohibit guaranteed silent-free autoplay.
- Reusing shared media internals could accidentally inherit Shared Folder authorization or download disposition; expose Music-specific controllers and test the negative matrix explicitly.
- Sliding sessions can be renewed by background traffic accidentally; centralize interactive-request classification and test every Music polling/stream route as excluded.
- Production host doubles as the development host; validate on a non-8080 port and rotate only through the established automatic deploy path.

## Completion Criteria

- All nine tasks are implemented on `codex/unified-music-hub` with focused commits and no unrelated checkout changes.
- All approved specification acceptance criteria are mapped to passing automated or local runtime evidence.
- One PR is merged after green CI/CodeQL.
- Automatic production deployment completes without prompts or Windows approval dialogs.
- External production verification passes for anonymous, reader, writer, combined Shared Folder/Music, and admin scenarios.
- Builder test report, spoke review, closure, and session memory are saved, indexed, validated, committed, and pushed.
