# ChristopherBell.dev Void Keep Alive Relaunch Implementation Plan

> **For agentic workers:** Execute this plan task by task in one isolated spoke worktree. Do not add approval pauses between tasks.

**Goal:** Relaunch Void around its existing 24-hour survival mechanic so first-time visitors understand it, interactions say Keep alive, popularity sorting disappears, sharing improves, and expired post pages reveal no content.

**Architecture:** Keep the existing post-expiration and Like API domain behavior authoritative. Reframe only the public UI vocabulary and add a narrow server-side social-preview boundary that converts an active public post into bounded escaped metadata; missing or expired posts render a content-free 404 page.

**Tech Stack:** Java 25, Spring Boot 4.1, Thymeleaf, vanilla JavaScript modules, CSS, Node test runner, Gradle.

## Global Constraints

- Work from refreshed `origin/main` in a new isolated worktree; preserve `A:\Projects\christopherbell.dev` unchanged.
- Invoke `chris-street-style` and its Java, JavaScript, template, design/API, and testing references before editing.
- Use RED-to-GREEN behavioral tests; retain existing Like API names as compatibility boundaries.
- Do not change the 24-hour base lifespan, extension calculation, reply synchronization, authorization, or mutation routes.
- Do not rank posts using keep-alive, reply, follower, or lifespan totals.
- Never expose expired or missing post text, username, or derived excerpts in HTML metadata.
- Keep one focused branch and PR; require CI, dependency review, and CodeQL before merge.
- Validate locally on a non-8080 port before allowing the automatic main deployment to replace production.

---

## Document Status

complete

## Objective

Make Void's temporary-thread proposition immediately understandable and safe to share without altering the already-correct lifespan domain.

## Goals

- Explain the 24-hour survival contract within the first `/void` viewport.
- Present the existing Like mutation as Keep alive without breaking API compatibility.
- Remove popularity-derived ordering and retain chronological/expiration ordering.
- Add native sharing with a copy fallback.
- Render safe, meaningful active-post metadata and a content-free 404 for missing or expired posts.

## Inputs

- Approved program spec: `docs/specs/2026-07-28-void-public-growth-program.md`.
- Existing domain: every root starts with 24 hours; each active Like and each reply contributes 24 hours; reply expirations mirror the root.
- Base: refreshed `origin/main` at `7d7d042c26d7bbabee2cdf0bc430127a0020e65e` or its current descendant.

## Branch

- Branch: `codex/void-keep-alive-relaunch`.
- Spoke: `A:\Projects\christopherbell.dev`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\void-keep-alive-relaunch`.

## Non-Goals

- No discovery page, hashtags, recommendations, `lastExtendedOn`, or ActivityPub work.
- No database migration or lifespan-domain rewrite.
- No public leaderboard or analytics UI.
- No broad Void visual redesign unrelated to the survival proposition.

## Assumptions

- `PostService.getPostById` remains the authoritative active-public-post lookup and rejects expired content.
- The existing automatic deployment workflow publishes a successful merge to `main`.
- The existing generic 1200x630 site preview image remains suitable for Release 1.

## Open Questions

None.

## Task Breakdown

### Task 1 - Make Keep alive the visible Void contract

Sequence / dependencies:
- First task; the server API and expiration domain remain unchanged.

Expected files or modules:
- Void feed template, feed renderer, home-feed ordering, thread page copy, CSS, JavaScript tests, and view markup tests.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: `/void` explains all three survival rules; Like is presented as `Keep alive · +24h` and becomes `Kept alive` only after the server confirms; replies explain their whole-thread 24-hour effect; native Share falls back to copying the canonical URL; only Newest and Expiring Soon sorts remain.
  - Invariants: the browser never invents expiration; failed interactions preserve the previous control/count/countdown; server-returned `liked`, `likesCount`, and `expiresOn` remain authoritative; feed ordering never uses engagement totals.
  - Boundary/API: retain `ctx.onLike` and current REST routes for compatibility; rename only rendered classes, labels, status chips, and local variables where that makes the UI contract explicit.
  - Effects and failures: share may invoke `navigator.share`, clipboard, or prompt fallback; `AbortError` is a no-op; rejected keep-alives display the existing actionable error without optimistic state.
  - Tests and evidence: add failing JS tests for labels/state/share outcomes and failing MVC/source assertions for rules, reply copy, and removal of Active; existing expiration tests characterize server-confirmed countdown updates.

#### Code Edit 1.1
- File: `website/src/main/resources/templates/void/index.html`
- Lines: 9-73
- Action: replace

Current:
```html
<p class="home-kicker">Live Feed</p>
<h1 id="voidTitle">Void</h1>
<p>Short posts, quick replies, and the latest noise from the feed.</p>
```

Proposed:
```html
<p class="home-kicker">The temporary social feed</p>
<h1 id="voidTitle">Nothing lasts unless people care.</h1>
<p>Every post begins with 24 hours. Keep it alive or let it disappear.</p>
<ol class="void-rules" aria-label="How Void works">
  <li>Every thread starts with 24 hours.</li>
  <li>Each keep-alive adds 24 hours.</li>
  <li>Each reply adds 24 hours to the whole thread.</li>
</ol>
```

Additional changes:
- Update social-description and anonymous composer copy to the same proposition.
- Preserve `/void` in both login and signup return URLs.
- Remove the `Active` option, retaining `newest` and `expiring` only.

Verification:
- `node --test website/src/test/js/a11y-markup.test.js website/src/test/js/feed-render-lifespan.test.js`

#### Code Edit 1.2
- File: `website/src/main/resources/static/js/lib/feed-render.js`
- Lines: 343-777
- Action: replace

Current:
```javascript
if (liked) chips.push(['liked', 'Liked']);
```

Proposed:
```javascript
if (liked) chips.push(['kept-alive', 'Kept alive']);
```

Current:
```html
<button class="post-action post-like-btn ${liked ? 'is-liked' : ''}" data-post="${post.id}" data-liked="${liked}" aria-label="Like">
  <i class="fa ${liked ? 'fa-heart' : 'fa-heart-o'}" aria-hidden="true"></i>
  <span class="like-count">${likes}</span>
</button>
```

Proposed:
```html
<button class="post-action post-keep-alive-btn ${liked ? 'is-kept-alive' : ''}"
        data-post="${post.id}" data-kept-alive="${liked}"
        aria-label="${liked ? 'Remove keep alive and 24 hours' : 'Keep alive and add 24 hours'}">
  <i class="fa ${liked ? 'fa-heart' : 'fa-heart-o'}" aria-hidden="true"></i>
  <span class="keep-alive-label">${liked ? 'Kept alive' : 'Keep alive · +24h'}</span>
  <span class="keep-alive-count" aria-label="${likes} keep-alives">${likes}</span>
</button>
```

Additional changes:
- Export a pure `keepAlivePresentation(keptAlive, count)` helper and drive initial and confirmed states from it.
- Add `sharePost(postId, browser)` whose visible results are `shared`, `copied`, `prompted`, or `cancelled`; add a Share menu item beside Copy link.
- Update labels, count, classes, icon, countdown, and a restrained `+24h` feedback marker only after `ctx.onLike` resolves.
- Undo uses the same authoritative response and does not display the add-time marker.

Verification:
- `node --test website/src/test/js/feed-render-lifespan.test.js`

#### Code Edit 1.3
- File: `website/src/main/resources/static/js/home-feed.js`
- Lines: 65-75
- Action: replace

Current:
```javascript
if (ACTIVE_SORT === 'active') {
  items.sort((a, b) => ((b.likesCount || 0) + (b.replyCount || 0)) - ((a.likesCount || 0) + (a.replyCount || 0)));
} else if (ACTIVE_SORT === 'expiring') {
```

Proposed:
```javascript
if (ACTIVE_SORT === 'expiring') {
```

Verification:
- `node --test website/src/test/js/a11y-markup.test.js`

#### Code Edit 1.4
- File: `website/src/main/resources/templates/post.html`
- Lines: 43
- Action: replace

Current:
```html
<span id="replyComposerMeta">Replies extend the signal.</span>
```

Proposed:
```html
<span id="replyComposerMeta">Replies add 24 hours to the entire thread.</span>
```

Verification:
- `node --test website/src/test/js/a11y-markup.test.js website/src/test/js/feed-render-lifespan.test.js`

#### Code Edit 1.5
- File: `website/src/main/resources/static/js/post.js`
- Lines: 55-158
- Action: replace

Current:
```javascript
<h2>This post expired in the Void.</h2>
<p>The thread context may still show active replies until their own lifespan ends.</p>
// ...
meta.textContent = currentUser ? 'Replies extend the signal.' : 'Log in to reply.';
```

Proposed:
```javascript
<h2>This thread vanished into the Void.</h2>
<p>The root and its replies share one lifespan.</p>
// ...
meta.textContent = currentUser
    ? 'Replies add 24 hours to the entire thread.'
    : 'Log in to reply.';
```

Verification:
- `node --test website/src/test/js/a11y-markup.test.js website/src/test/js/post-editing.test.js`

#### Code Edit 1.6
- File: `website/src/main/resources/static/css/main.css`
- Lines: 3610-3657
- Action: replace

Current:
```css
.post-like-btn.is-liked {
  color: var(--site-danger);
}
```

Proposed:
```css
.post-keep-alive-btn.is-kept-alive {
  color: var(--site-danger);
}

.keep-alive-count {
  color: inherit;
  opacity: 0.72;
}
```

Additional changes:
- Style `.void-rules`, confirmed `+24h` feedback, and responsive labels without obscuring adjacent actions.

Verification:
- `node --test website/src/test/js/a11y-markup.test.js website/src/test/js/feed-render-lifespan.test.js`

- [x] Add and witness the Task 1 RED tests.
- [x] Implement hero/rules, Keep alive state, Share fallback, reply disclosure, and non-popularity sorts.
- [x] Run focused JS/MVC tests and commit Task 1.

### Task 2 - Render safe active previews and a content-free vanished page

Sequence / dependencies:
- Runs after Task 1; independent of the lifespan calculation but depends on active-post lookup semantics.

Expected files or modules:
- A focused preview value/service, Void view controller, active/vanished templates, view documentation, and Java tests.

Implementation notes:
- Before-Edit Brief:
  - Behavior: active `/p/{postId}` responses contain meaningful server-rendered metadata; missing or expired IDs return HTTP 404 with `This post vanished into the Void`, a `/void` route, and no original content or author metadata.
  - Invariants: only `PostService.getPostById` decides active visibility; preview excerpts are whitespace-normalized, code-point bounded, and template-escaped; infrastructure failures remain 500 and are not mislabeled as vanished.
  - Boundary/API: add immutable `VoidPostSocialPreview` and a service owning post lookup/time formatting; the controller maps only domain not-found to the vanished view.
  - Effects and failures: post lookup reads Mongo and may return domain not-found or infrastructure failure; canonical path segments are encoded; no raw body or private account fields are logged.
  - Tests and evidence: add failing unit tests for bounds/fallbacks and failing MVC tests for escaped active metadata, 404 status, generic metadata, and absence of sentinel secret text.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/view/voidroutes/VoidPostSocialPreview.java`
- Lines: 1-60
- Action: add

Proposed:
```java
record VoidPostSocialPreview(String title, String description) {
  private static final int MAX_EXCERPT_CODE_POINTS = 160;

  static VoidPostSocialPreview from(PostFeedItem post, Instant now) {
    // Collapse whitespace, bound by Unicode code points, and describe remaining temporary life.
  }
}
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-relaunch'; .\gradlew.bat :website:test --tests "*VoidPostSocialPreview*" --no-daemon`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/view/voidroutes/VoidPostSocialPreviewService.java`
- Lines: 1-45
- Action: add

Proposed:
```java
@Service
final class VoidPostSocialPreviewService {
  private final PostService posts;
  private final Clock clock;

  VoidPostSocialPreview preview(String postId) throws ResourceNotFoundException {
    return VoidPostSocialPreview.from(posts.getPostById(postId), clock.instant());
  }
}
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-relaunch'; .\gradlew.bat :website:test --tests "*VoidPostSocialPreview*" --no-daemon`

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/view/voidroutes/VoidViewController.java`
- Lines: 1-74
- Action: replace

Current:
```java
model.addAttribute("socialUrl", "https://www.christopherbell.dev/p/" + postId);
return "post.html";
```

Proposed:
```java
try {
  VoidPostSocialPreview preview = postPreviews.preview(postId);
  model.addAttribute("postSocialTitle", preview.title());
  model.addAttribute("postSocialDescription", preview.description());
  return "post.html";
} catch (ResourceNotFoundException exception) {
  response.setStatus(HttpServletResponse.SC_NOT_FOUND);
  return "post-vanished.html";
}
```

Additional changes:
- Constructor-inject the preview service.
- Encode the canonical path segment before placing `socialUrl` in the model.
- Catch only the established domain not-found type.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-relaunch'; .\gradlew.bat :website:test --tests "*ViewControllerTest*" --tests "*VoidPostSocialPreview*" --no-daemon`

#### Code Edit 2.4
- File: `website/src/main/resources/templates/post.html`
- Lines: 5-8
- Action: replace

Current:
```html
<th:block th:replace="~{fragments/social-preview :: socialPreview('CB | Void Post', 'A Void post thread with context, replies, and the rest of the conversation.', ${socialUrl}, 'https://www.christopherbell.dev/images/previews/christopherbell-dev.png', 'The Void preview for christopherbell.dev')}"></th:block>
```

Proposed:
```html
<th:block th:replace="~{fragments/social-preview :: socialPreview(${postSocialTitle}, ${postSocialDescription}, ${socialUrl}, 'https://www.christopherbell.dev/images/previews/christopherbell-dev.png', 'Void on christopherbell.dev')}"></th:block>
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-relaunch'; .\gradlew.bat :website:test --tests "*ViewControllerTest*" --no-daemon`

#### Code Edit 2.5
- File: `website/src/main/resources/templates/post-vanished.html`
- Lines: 1-45
- Action: add

Proposed:
```html
<h1>This post vanished into the Void.</h1>
<p>Nothing lasts unless people care.</p>
<a class="btn btn-primary" href="/void">Return to the Void</a>
```

Additional changes:
- Give the vanished template generic metadata only; do not load post APIs or embed the requested ID in visible/loggable copy.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-relaunch'; .\gradlew.bat :website:test --tests "*ViewControllerTest*" --tests "*VoidPostSocialPreview*" --no-daemon`

- [x] Add and witness the Task 2 RED tests.
- [x] Implement typed preview generation, controller mapping, active metadata, and vanished template.
- [x] Run focused Java/template tests and commit Task 2.

### Task 3 - Validate, publish, merge, deploy, and close

Sequence / dependencies:
- Runs after Tasks 1 and 2 are green.

Operational steps:
- Run JavaScript syntax/tests and full `:website:check` with an isolated Gradle cache.
- Review the final diff for authorization regressions, unsafe metadata, accidental popularity ordering, optimistic lifespan changes, and unrelated edits.
- Package and run the app on a non-8080 port; exercise anonymous `/void`, active `/p/{id}`, missing `/p/{id}`, login return links, and an authenticated Keep alive round trip against controlled test data.
- Save and validate a Builder local-app test report.
- Commit and push the spoke branch, open one PR, wait for required CI/dependency/CodeQL checks, fix in-scope failures, and merge.
- Confirm automatic deployment reached the merged SHA without prompts; smoke public `/void`, active and vanished post pages, Music persistent playback navigation, Messages, and Back Office authentication.
- Close/update any source issue if one exists; otherwise record this user-approved program release as the source item.
- Save session memory, refresh Builder indexes, validate Builder state, commit, and push Builder `main`.

- [x] Focused and full automated validation passes.
- [x] Non-8080 runtime validation passes and the test report is committed/pushed.
- [x] PR CI/CodeQL passes, PR merges, and production exact-SHA smoke passes.
- [x] Closure and session-memory artifacts are committed/pushed.

## Code Changes

- `void/index.html`, `home-feed.js`: explain survival and remove popularity ordering.
- `feed-render.js`, `main.css`: render and update Keep alive and Share controls from authoritative results.
- `post.html`, `post.js`: disclose reply effects and correct whole-thread expiry copy.
- `VoidPostSocialPreview*`, `VoidViewController`: isolate active lookup, bounded preview construction, and domain-not-found mapping.
- `post-vanished.html`: render a generic content-free 404.
- Java and JavaScript tests plus view documentation: prove the contract and failure boundaries.

## Files and Modules

- `website/src/main/java/dev/christopherbell/view/voidroutes/*`
- `website/src/main/resources/templates/{void/index.html,post.html,post-vanished.html}`
- `website/src/main/resources/static/js/{home-feed.js,post.js,lib/feed-render.js}`
- `website/src/main/resources/static/css/main.css`
- `website/src/test/java/dev/christopherbell/view/*`
- `website/src/test/js/{a11y-markup.test.js,feed-render-lifespan.test.js,post-editing.test.js}`

## Unit Testing

- JavaScript: visible Keep alive labels/counts, selected/unselected presentation, native-share success/cancel/fallback, server-confirmed countdown update, reply disclosure, and absence of Active sort.
- Java: Unicode code-point excerpt bounds, whitespace normalization, null/blank fallbacks, duration description, active metadata rendering, output escaping, missing/expired 404, and infrastructure-error propagation.
- Existing post-expiration and interaction suites remain unchanged and green to prove exact 24-hour semantics and reply synchronization.

## Local Testing

- Use `GRADLE_USER_HOME=A:\Temp\gradle-void-relaunch` and a non-8080 listener.
- Verify anonymous users see the proposition/rules and are returned to the source route after login/signup.
- With controlled active data, confirm Keep alive adds exactly 24 hours only after the response and undo restores the authoritative expiration.
- Confirm a reply adds 24 hours to every visible member of the thread.
- Inspect active page source for escaped bounded metadata; request missing/expired IDs and confirm 404, generic metadata, and no sentinel content.
- Confirm Share invokes native sharing where supported and Copy link fallback remains usable.

## Validation

- RED evidence is captured before production edits; focused tests then pass.
- `:website:check` passes with zero failures.
- Required GitHub Actions, dependency review, and CodeQL pass.
- Automatic deployment publishes the merge SHA with no interactive prompts.
- Production Void, login/signup, Messages, Music persistence, and Back Office smoke checks pass.

## Rollback or Recovery

- Before merge, remove only the isolated worktree/branch if abandoned.
- After merge, use the existing automatic release rollback to restore the previous artifact; there is no schema change.
- Existing Like API compatibility means old cached clients continue working through a rollback or forward deploy.

## Risks

- Dynamic metadata can leak expired text if lookup order is wrong; use the active-domain lookup before deriving any attribute.
- Template values can become attribute injection if rendered unescaped; use Thymeleaf expressions and assert escaped output.
- Native share cancellation can look like failure; treat `AbortError` as a quiet cancellation.
- UI renaming can accidentally become an API rename; keep the current backend route and callback boundary.
- A client sort can reintroduce popularity ranking; remove the branch and cover source behavior.

## Completion Criteria

- The approved Release 1 acceptance criteria are mapped to passing tests and runtime evidence.
- The lifespan domain remains unchanged and exact 24-hour behavior stays green.
- Keep alive, replies, countdown, sharing, and non-popularity ordering work on desktop and mobile.
- Active social metadata is useful and escaped; missing/expired pages are content-free 404s.
- The focused PR is merged after required checks, automatic production deployment completes, and exact-SHA smoke passes.
- Builder test report, closure record, session memory, indexes, validation, commit, and push are complete.
