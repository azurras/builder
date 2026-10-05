# christopherbell.dev Browser Delivery Optimization Implementation Plan

> **For agentic workers:** Execute this plan task by task. Before editing production code, tests, build logic, templates, or executable examples, invoke `chris-street-style` and `superpowers:test-driven-development`. Use a clean `codex/` worktree from refreshed `origin/main`; do not edit the authoritative dirty checkout.

## Global Constraints

- Preserve plain ES modules, Thymeleaf URL rewriting, Bootstrap, and the current no-npm build.
- Preserve direct URLs, browser history, logout, media resume, accessibility, and versioned relative imports.
- Do not introduce a frontend framework, package manager, bundler, service worker, or CDN migration.
- Every lazy import must be triggered by explicit DOM state, persisted playback state, or a user action; no timer-only loading.
- Keep `/version/...` assets immutable for one year and unversioned assets bounded to one hour.
- The approved global-entry budget is 86,434 raw bytes for login, signup, VIN, and ZIP pages.

## Document Status

ready-for-execution

## Objective

Reduce browser parsing, transfer, and cache churn on routes that do not use blog, gallery, or media features; split feature-exclusive CSS; and consolidate repeated browser behavior into stable `static/js/lib` modules.

## Goals

- Cut the global `app.js` static dependency graph from 172,868 raw bytes to at most 86,434 bytes on lightweight routes.
- Load blog, gallery, and the full site-media runtime only when needed.
- Remove command-center, Shared Folder, Void discovery, and player-only selectors from the global stylesheet.
- Version immutable assets by static-content fingerprint rather than unrelated backend commits.
- Move demonstrated WFL, status/alert, URL punctuation, and sanitization reuse into browser library modules.

## Inputs

- Approved spec: `docs/specs/2026-07-29-christopherbell-dev-performance-scalability-library-optimization.md`
- Source baseline: `origin/main` at `f31535f29312d24573a6031b0162aa8ebc4b5318`
- Inspected worktree: `A:\Projects\christopherbell.dev-worktrees\performance-planning-20260729`
- Measured baseline: 14 global modules, 172,868 bytes, 3,956 lines; `main.css` 154,946 bytes.

## Branch

Create a fresh isolated branch named `codex/browser-delivery-optimization` from refreshed `origin/main` at execution time.

## Non-Goals

- No visual redesign or user-flow changes.
- No image transcoding campaign.
- No server-side API changes beyond the asset fingerprint configuration.
- No extraction of one-off page code into generic libraries.

## Assumptions

- Node remains available through the repository's current `jsTest` task.
- Spring's fixed resource strategy continues rewriting Thymeleaf asset links and relative ES-module imports.
- The media resume key remains `cbellSiteMediaResumeV1`.

## Open Questions

None. If a new direct media consumer appears after the pinned commit, add it to the loader migration before deleting any static player import.

## File Structure

- `website/src/main/resources/static/js/app.js` — minimal global bootstrap.
- `website/src/main/resources/static/js/lib/site-media-loader.js` — lazy media runtime boundary.
- `website/src/main/resources/static/js/lib/wfl-ui.js` — WFL display primitives.
- `website/src/main/resources/static/js/lib/status-message.js` — safe reusable alert/status rendering.
- `website/src/main/resources/static/css/{command-center,shared-folder,void-discovery,site-media-player}.css` — route/runtime CSS.
- `website/src/test/js/app-entry-budget.test.js` — dependency-graph and byte budget.

## Task Breakdown

### Task 1 - Lock the global entry budget before changing imports

Sequence / dependencies:
- First task; its RED result proves the current graph exceeds the approved budget.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before test or source edits.
- Before-Edit Brief:
  - Behavior: recursively follow only static relative imports from `app.js`, report sorted files and raw byte total, and fail above 86,434 bytes.
  - Invariants: dynamic imports are excluded from the initial graph; cycles are counted once; paths cannot escape `static/js`.
  - Boundary/API: Node built-ins only; no npm dependency.
  - Effects and failures: read-only test; malformed imports or missing local files fail with a useful path.
  - Tests and evidence: current graph fails, optimized graph passes, fixture cycle counts once.

- [ ] Add the graph-budget test and run it RED against the baseline.
- [ ] Record the reported baseline in the test name/comment and Builder test report.
- [ ] Keep the test in `jsTest` permanently.

#### Code Edit 1.1
- File: `website/src/test/js/app-entry-budget.test.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const JS_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../main/resources/static/js');
const MAX_INITIAL_BYTES = 86_434;
const STATIC_IMPORT = /(?:^|\n)\s*import(?:[\s\S]*?from\s*)?['"](\.\.?\/[^'"]+)['"];?/g;

async function initialGraph(entry, visited = new Set()) {
  const resolved = path.resolve(entry);
  assert.ok(resolved.startsWith(`${JS_ROOT}${path.sep}`), `Import escaped static/js: ${resolved}`);
  if (visited.has(resolved)) return visited;
  visited.add(resolved);
  const source = await readFile(resolved, 'utf8');
  for (const match of source.matchAll(STATIC_IMPORT)) {
    const child = path.resolve(path.dirname(resolved), match[1]);
    await initialGraph(path.extname(child) ? child : `${child}.js`, visited);
  }
  return visited;
}

test('lightweight routes keep the app static graph within 86,434 raw bytes', async () => {
  const files = [...await initialGraph(path.join(JS_ROOT, 'app.js'))].sort();
  const sizes = await Promise.all(files.map(file => stat(file).then(value => value.size)));
  const total = sizes.reduce((sum, size) => sum + size, 0);
  assert.ok(total <= MAX_INITIAL_BYTES,
    `app.js initial graph is ${total} bytes across ${files.length} modules:\n${files.join('\n')}`);
});
```

Verification:
- `./gradlew :website:jsTest` (the failing output must name `app-entry-budget.test.js` and report the current graph bytes)

### Task 2 - Make page widgets and media runtime demand-loaded

Sequence / dependencies:
- Runs after Task 1. Complete before stylesheet splitting because the player stylesheet follows the runtime.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before test or source edits.
- Before-Edit Brief:
  - Behavior: nav/footer remain immediate; blog/gallery load only when their mount exists; media loads for persisted resume or a play action.
  - Invariants: one player host in the top document, one runtime promise, logout always clears an active player, navigation interception exists only after media loads.
  - Boundary/API: page modules import async wrappers from `site-media-loader.js`, not the full implementation.
  - Effects and failures: a rejected dynamic import produces the existing page error boundary; retries reset the cached rejected promise.
  - Tests and evidence: no heavy imports on login/signup/VIN/ZIP; blog/gallery mount; resume/play/logout/navigation tests.

- [ ] Add RED loader tests for once-only loading, resume, and failed-import retry.
- [ ] Add the loader and migrate both media consumers.
- [ ] Convert blog/gallery static imports to guarded dynamic imports.
- [ ] Run `jsTest` and confirm Task 1 turns GREEN.

#### Code Edit 2.1
- File: `website/src/main/resources/static/js/app.js`
- Lines: 9-65
- Action: replace

Current:
```javascript
import './components/nav.js';
import './components/footer.js';
import './components/blog.js';
import './components/gallery.js';
import './components/site-media-player.js';
import pubsub from './components/pubsub.js';
import { API } from './lib/api.js';
import { clearAuthState, fetchJson } from './lib/util.js';
import {
    handleSiteNavigationClick,
    siteMediaPlayerHost,
    stopSiteMediaPlayback,
} from './lib/site-media-player.js';
```

Proposed:
```javascript
import './components/nav.js';
import './components/footer.js';
import pubsub from './components/pubsub.js';
import { API } from './lib/api.js';
import { clearAuthState, fetchJson } from './lib/util.js';
import { resumeSiteMediaIfPresent, stopSiteMediaPlayback } from './lib/site-media-loader.js';
```

Implementation:
- In `DOMContentLoaded`, replace eager blog/gallery construction with `await import('./components/blog.js')` and `await import('./components/gallery.js')` inside their existing mount guards.
- Call `void resumeSiteMediaIfPresent()` after core layout mounting.
- In logout, await `stopSiteMediaPlayback()` before clearing auth state; derive the redirect window before stopping.
- Delete the global capture-phase click listener. The loader installs it once when a player runtime exists.

Verification:
- `./gradlew :website:jsTest`

#### Code Edit 2.2
- File: `website/src/main/resources/static/js/lib/site-media-loader.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
const RESUME_KEY = 'cbellSiteMediaResumeV1';
let runtimePromise;

async function loadRuntime() {
  if (!runtimePromise) {
    runtimePromise = Promise.all([
      import('../components/site-media-player.js'),
      import('./site-media-player.js'),
    ]).then(([, api]) => {
      if (window.top === window && !api.siteMediaPlayerHost()) {
        document.body.appendChild(document.createElement(api.SITE_MEDIA_PLAYER_TAG));
      }
      document.addEventListener('click', api.handleSiteNavigationClick, true);
      return api;
    }).catch(error => {
      runtimePromise = undefined;
      throw error;
    });
  }
  return runtimePromise;
}

export async function resumeSiteMediaIfPresent(storage = window.localStorage) {
  if (!storage.getItem(RESUME_KEY)) return false;
  await loadRuntime();
  return true;
}

export async function playSharedFolderMedia(...args) {
  return (await loadRuntime()).playSharedFolderMedia(...args);
}

export async function playSharedFolderRadio(...args) {
  return (await loadRuntime()).playSharedFolderRadio(...args);
}

export async function playMusicTrack(...args) {
  return (await loadRuntime()).playMusicTrack(...args);
}

export async function playMusicRadio(...args) {
  return (await loadRuntime()).playMusicRadio(...args);
}

export async function stopSiteMediaPlayback() {
  if (!runtimePromise) return;
  try {
    (await runtimePromise).stopSiteMediaPlayback();
  } catch {
    // Logout and access-loss cleanup must continue if a dynamic import failed.
  }
}
```

Verification:
- `./gradlew :website:jsTest`

#### Code Edit 2.3
- File: `website/src/main/resources/static/js/music.js`
- Lines: 13
- Action: replace

Current:
```javascript
import { playMusicRadio, playMusicTrack } from './lib/site-media-player.js';
```

Proposed:
```javascript
import { playMusicRadio, playMusicTrack } from './lib/site-media-loader.js';
```

Verification:
- `./gradlew :website:jsTest`

#### Code Edit 2.4
- File: `website/src/main/resources/static/js/shared-folder.js`
- Lines: 39-44
- Action: replace

Current:
```javascript
import {
  playSharedFolderMedia,
  playSharedFolderRadio as joinSharedFolderRadio,
  stopSiteMediaPlayback,
} from './lib/site-media-player.js';
```

Proposed:
```javascript
import {
  playSharedFolderMedia,
  playSharedFolderRadio as joinSharedFolderRadio,
  stopSiteMediaPlayback,
} from './lib/site-media-loader.js';
```

Implementation:
- Await `stopSiteMediaPlayback()` in the access-loss path or explicitly discard its promise with `void`; preserve immediate redirect behavior.

Verification:
- `./gradlew :website:jsTest`

### Task 3 - Split feature-exclusive CSS and lazy-load player styles

Sequence / dependencies:
- Runs after Task 2 so player CSS ownership matches runtime ownership.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before CSS, template, test, or source edits.
- Before-Edit Brief:
  - Behavior: route appearance is unchanged; lightweight routes do not download feature-only selectors.
  - Invariants: selector order within each moved block stays unchanged; shared variables/base selectors remain in `main.css`.
  - Boundary/API: feature templates use Thymeleaf-versioned links; player loader uses a version-preserving relative URL.
  - Effects and failures: missing feature CSS is a visible regression and fails template/browser checks.
  - Tests and evidence: selector ownership test plus screenshots at desktop/mobile widths.

- [ ] Add RED tests for selector ownership and required route stylesheet links.
- [ ] Move—not copy—the four contiguous CSS blocks.
- [ ] Add feature links and lazy player link.
- [ ] Run JS/template tests and visual smoke.

#### Code Edit 3.1
- File: `website/src/main/resources/static/css/main.css`
- Lines: 9-7202
- Action: move

Current:
```text
All four feature-exclusive selector blocks are embedded in static/css/main.css.
```

Proposed:
```text
9-249    -> static/css/void-discovery.css
251-485  -> static/css/command-center.css
6265-6800 -> static/css/shared-folder.css
6802-7202 -> static/css/site-media-player.css
```

Verification:
- `./gradlew :website:jsTest`

#### Code Edit 3.2
- File: `website/src/main/resources/templates/{command-center,shared-folder,void/explore,void/topic}.html`
- Lines: 8
- Action: add

Proposed:
```html
<link rel="stylesheet" href="/css/command-center.css" th:href="@{/css/command-center.css}" />
<link rel="stylesheet" href="/css/shared-folder.css" th:href="@{/css/shared-folder.css}" />
<link rel="stylesheet" href="/css/void-discovery.css" th:href="@{/css/void-discovery.css}" />
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.PublicDeliveryConfigurationTest`

#### Code Edit 3.3
- File: `website/src/main/resources/static/js/lib/site-media-loader.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
function ensurePlayerStyles(documentRoot = document) {
  if (documentRoot.querySelector('link[data-site-media-player-styles]')) return;
  const link = documentRoot.createElement('link');
  link.rel = 'stylesheet';
  link.dataset.siteMediaPlayerStyles = 'true';
  link.href = new URL('../../css/site-media-player.css', import.meta.url).href;
  documentRoot.head.appendChild(link);
}
```

- Call `ensurePlayerStyles()` once before creating the player. From `/VERSION/js/lib/site-media-loader.js`, `../../css/...` resolves to `/VERSION/css/...` and preserves immutable-cache versioning.

Verification:
- `./gradlew :website:jsTest`

### Task 4 - Consolidate demonstrated browser library reuse

Sequence / dependencies:
- Independent of Task 3; execute after Task 2 to minimize merge conflicts in imports.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before test or source edits.
- Before-Edit Brief:
  - Behavior: markup/text remains byte-for-byte equivalent for valid inputs; unsafe values still pass through `sanitize` before HTML insertion.
  - Invariants: helpers are pure except the explicit status renderer; no hidden global DOM lookup.
  - Boundary/API: WFL helpers accept data and return strings; status helper accepts an explicit host; URL punctuation has one export in `util.js`.
  - Effects and failures: null/invalid values preserve current fallbacks.
  - Tests and evidence: table-driven equivalence tests before deleting duplicates.

- [ ] Characterize current WFL/address/rating/nav and alert outputs with tests.
- [ ] Add `wfl-ui.js` and `status-message.js`.
- [ ] Migrate all named consumers, then remove duplicates.
- [ ] Export `trimUrlPunctuation` from `util.js` and consume it in `feed-render.js`.

#### Code Edit 4.1
- File: `website/src/main/resources/static/js/lib/wfl-ui.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
const NAV_ITEMS = Object.freeze([
  { key: 'picks', href: '/wfl', label: 'Picks' },
  { key: 'top-rated', href: '/wfl/top-rated', label: 'Top 10 Rated' },
  { key: 'favorites', href: '/wfl/favorites', label: 'Favorites' },
]);

export function wflSecondaryNavigation(active = 'picks') {
  return `
    <nav class="wfl-secondary-nav" aria-label="What's For Lunch navigation">
      ${NAV_ITEMS.map((item) => `
        <a class="${active === item.key ? 'active' : ''}" href="${item.href}">${item.label}</a>
      `).join('')}
    </nav>
  `;
}

export function restaurantAddressLine(address = {}, includeStreet2 = false) {
  return [address.street1, includeStreet2 ? address.street2 : null,
    address.city, address.state, address.postalCode].filter(Boolean).join(', ');
}

export function formatCuisine(value) {
  return String(value || '').split(/([;,/|])/)
    .map(part => /^[;,/|]$/.test(part) ? `${part} ` : part.trim()
      .replace(/[_-]+/g, ' ').split(/\s+/).filter(Boolean)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' '))
    .join('').replace(/\s+/g, ' ').trim();
}

export function ratingSummary(restaurant = {}) {
  const sum = Number.parseInt(String(restaurant.ratingSum ?? 0), 10) || 0;
  const count = Number.parseInt(String(restaurant.ratingCount ?? 0), 10) || 0;
  const myRating = Number.parseInt(String(restaurant.myRating ?? 0), 10) || 0;
  return Object.freeze({
    count,
    myRating,
    overall: count > 0 ? `${Math.round(sum / count)}/5` : 'No Ratings',
  });
}
```

- Move exact characterized implementations from `restaurant-profile.js`, `wfl-list.js`, and `whats-for-lunch.js`; keep page-specific CSS classes/outer markup in each page.

Verification:
- `./gradlew :website:jsTest`

#### Code Edit 4.2
- File: `website/src/main/resources/static/js/lib/status-message.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
import { sanitize } from './util.js';

export function renderAlert(host, message, type = 'danger') {
  if (!host) return;
  const allowedType = ['danger', 'info', 'success', 'warning'].includes(type) ? type : 'danger';
  host.innerHTML = `<div class="alert alert-${allowedType}" role="alert">${sanitize(message || '')}</div>`;
}
```

- Migrate the equivalent `showAlert` functions in auth forgot/reset, messages, report, user-feed, VIN, ZIP, Canes, and back-office. Keep page-specific scrolling/focus behavior at the call site.

Verification:
- `./gradlew :website:jsTest`

#### Code Edit 4.3
- File: `website/src/main/resources/static/js/lib/{util,feed-render}.js`
- Lines: 1-330
- Action: replace

Current:
```javascript
// Both files define a private trimUrlPunctuation implementation.
```

Proposed:

Proposed:
```javascript
// util.js
export function trimUrlPunctuation(value) {
  let trimmed = String(value || '');
  while (/[.,!?;:]$/.test(trimmed)) trimmed = trimmed.slice(0, -1);
  return trimmed;
}

// feed-render.js import list
import { sanitize, trimUrlPunctuation } from './util.js';
```

- Delete the private `feed-render.js` copy. Replace remaining custom HTML escaping only where tests prove it is semantically identical to `sanitize`; retain intentionally different attribute/URL validation.

Verification:
- `./gradlew :website:jsTest`

### Task 5 - Fingerprint static content instead of backend commits

Sequence / dependencies:
- Runs after CSS/JS moves so the first fingerprint reflects the optimized asset tree.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before build, configuration, test, or documentation edits.
- Before-Edit Brief:
  - Behavior: identical static bytes yield identical version; any path/content change yields a new version; backend-only commits do not.
  - Invariants: relative paths and bytes are hashed in deterministic order; no timestamps or absolute paths enter the digest.
  - Boundary/API: embedded fallback token becomes `@staticAssetFingerprint@`; optional override is `ASSET_VERSION`.
  - Effects and failures: unreadable assets fail the build; no silent fallback to Git SHA.
  - Tests and evidence: repeat-build equality, one-byte fixture change inequality, immutable cache tests.

- [ ] Add RED build/config tests for fingerprint shape and backend-only stability.
- [ ] Replace the Git provider with content hashing.
- [ ] Update configuration docs/tests and build twice.

#### Code Edit 5.1
- File: `website/build.gradle.kts`
- Lines: 137-153
- Action: replace

Current:
```kotlin
val releaseGitCommit = providers.exec {
    commandLine("git", "rev-parse", "HEAD")
    workingDir(rootProject.projectDir)
}.standardOutput.asText.map { output ->
    val commit = output.trim().lowercase()
    if (!commit.matches(Regex("[0-9a-f]{40}"))) {
        throw GradleException("Git HEAD must resolve to a full 40-character commit SHA.")
    }
    commit
}
```

Proposed:
```kotlin
val staticAssetFiles = fileTree("src/main/resources/static") { exclude("**/.DS_Store") }
val staticAssetFingerprint = providers.provider {
    val digest = java.security.MessageDigest.getInstance("SHA-256")
    staticAssetFiles.files.filter { it.isFile }.sortedBy {
        it.relativeTo(file("src/main/resources/static")).invariantSeparatorsPath
    }.forEach { asset ->
        val relative = asset.relativeTo(file("src/main/resources/static")).invariantSeparatorsPath
        digest.update(relative.toByteArray(Charsets.UTF_8))
        digest.update(0.toByte())
        asset.inputStream().use { input ->
            val buffer = ByteArray(8192)
            while (true) {
                val count = input.read(buffer)
                if (count < 0) break
                digest.update(buffer, 0, count)
            }
        }
    }
    java.util.HexFormat.of().formatHex(digest.digest()).take(20)
}
```

- Rename the `processResources` input to `staticAssetFingerprint` and replace `@staticAssetFingerprint@` in `application.yml`.

Verification:
- `./gradlew :website:processResources :website:test --tests dev.christopherbell.configuration.PublicDeliveryConfigurationTest`

#### Code Edit 5.2
- File: `website/{src/main/resources/application.yml,src/test/java/dev/christopherbell/configuration/PublicDeliveryConfigurationTest.java,src/main/java/dev/christopherbell/configuration/README.md}`
- Lines: 13-116
- Action: replace

Current:
```yaml
version: ${GIT_COMMIT:@releaseGitCommit@}
```

Proposed:
```yaml
version: ${ASSET_VERSION:@staticAssetFingerprint@}
```

- Assert the packaged fallback matches `\$\{ASSET_VERSION:[0-9a-f]{20}}`.
- Keep all existing versioned/unversioned cache-control assertions.
- Document that operators normally leave `ASSET_VERSION` unset; it exists only for an explicit emergency cache namespace override.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.PublicDeliveryConfigurationTest`

### Task 6 - Verify route weight and behavior

Sequence / dependencies:
- Final merge gate after Tasks 1-5.

- [ ] Run `:website:jsTest` and `:website:check`.
- [ ] Build twice and prove the asset version is identical.
- [ ] Measure login/signup/VIN/ZIP initial JS graph and confirm each is at most 86,434 raw bytes.
- [ ] On a non-8080 port, exercise blog, gallery, Music, Shared Folder media, resume, logout, and in-player navigation.
- [ ] Capture desktop/mobile screenshots for Command Center, Shared Folder, Void explore/topic, and an active player.
- [ ] Save exact before/after bytes, request counts, and behavior evidence in a Builder test report.

Verification:
- `./gradlew :website:jsTest :website:check`
- Alternate-port browser verification through `verify-local-spring-app` during authorized execution.

## Code Changes

- Shrink the global static import graph and add a retry-safe media loader.
- Split four feature-only CSS regions and preserve versioned paths.
- Add WFL/status library modules and remove duplicated punctuation/sanitization helpers.
- Replace Git-SHA asset versioning with deterministic static-content hashing.

## Files and Modules

- Browser entry/runtime: `app.js`, player component/library, Music, Shared Folder.
- Styling/templates: `main.css`, four new CSS files, four feature templates.
- Shared browser code: `lib/wfl-ui.js`, `lib/status-message.js`, `lib/util.js`, `lib/feed-render.js`.
- Delivery/build: `website/build.gradle.kts`, `application.yml`, configuration tests/docs.

## Unit Testing

- Graph cycles/path escape/dynamic import exclusion and byte threshold.
- Lazy-loader once/retry/resume/play/stop behavior.
- WFL and alert helper equivalence including unsafe input.
- CSS selector ownership and template asset links.
- Deterministic fingerprint format and cache policy.

## Local Testing

Use a disposable profile/database and a non-8080 port. Verify lightweight routes first with the network cache disabled, then feature routes and persisted player resume. Do not change the production listener.

## Validation

- `./gradlew :website:jsTest`
- `./gradlew :website:test --tests dev.christopherbell.configuration.PublicDeliveryConfigurationTest`
- `./gradlew :website:check`
- Before/after raw bytes and browser network evidence in the test report.

## Rollback or Recovery

Revert the plan's single PR. If only a lazy-load regression occurs, restore the affected static import and feature stylesheet link while keeping the graph-budget test adjusted only through explicit review. `ASSET_VERSION` can provide an emergency cache namespace without changing source.

## Risks

- Async media calls may expose missing `await`/promise handling; tests cover every caller.
- A CSS selector may depend on source order across moved blocks; visual checks cover each feature.
- Regex import parsing intentionally supports repository-native static import syntax only; new syntax must extend the test explicitly.
- Content fingerprints can churn if generated files enter `static`; the build excludes only `.DS_Store`, so additions remain visible by design.

## Completion Criteria

- The approved 86,434-byte global graph limit passes.
- Blog, gallery, player, and feature CSS load only at their defined boundaries.
- All named duplicate helpers have one tested library owner.
- Backend-only source changes leave the asset version unchanged; static changes rotate it.
- Focused tests, `:website:check`, alternate-port browser evidence, authorized PR/CI/merge/production verification, and Builder closeout are complete.
