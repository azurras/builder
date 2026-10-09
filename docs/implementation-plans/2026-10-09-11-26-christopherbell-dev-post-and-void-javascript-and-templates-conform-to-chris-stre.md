# Post and Void JavaScript and Templates Conform to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The post thread page, Void discovery scripts and the post and Void templates conform to write-chris-street-style-code, and the thread, explore and topic pages render and behave as before.

## Background
This is slice 16b of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). [Slice 16a](2026-10-09-11-20-christopherbell-dev-post-java-slice-conforms-to-chris-street-style.md) covers the post Java. Inspection at `3f4af8b1` found:

1. **`post.js`:**
   - `renderRoot` and `renderThread` take a `currentUser` parameter that shadows the module state of the same name.
   - The renderer context is built twice; one copy is a single 240-character line.
   - The status pill and reply count are set in duplicated code.
   - The root-context condition is repeated.
   - An empty `catch (_) {}` hides why a failed `/me` read is ignored.
   - `fillContext` promises are dropped silently.
   - Short names (`el`, `err`, `ctx`, `delta`, `byId`) and a magic day length and indent limit.
   - `renderThread` returns `undefined` without a list, so callers patch it with `|| []`.
2. **`void-discovery.js`:**
   - Topic links are built in two copies.
   - `renderPeople` mixes iteration with card building on a 130-character line.
   - The shared-topic limit `3` is unnamed.
3. **`lib/void-discovery.js`:** an unexplained `catch (_)`.
4. **Templates:** six discovery action rows put two buttons on one line.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The pages render and behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Shared feed libraries (`feed-render.js`, `feed-context.js`, `thread-navigation.js`, `util.js`) | Slice 22, shared JavaScript |
| CSS custom properties for the Void palette | Slice 23 owns the shared style system; `void-discovery.css` follows the site's current literal palette |
| Splitting `th:replace` social-preview expressions across lines | They are single Thymeleaf expressions; splitting them risks parse changes for no reader benefit |
| `home-active-post*.js` and the home feed | Home feature, slice 22 |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | The 390 JavaScript tests, `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On a candidate with isolated MongoDB `test`, a browser shows: the thread page for a nested reply with its root and parent context cards, status and reply-count pills, replies with depth labels, branch collapse and expand, newest-reply jump; an anonymous viewer's disabled reply composer; the explore page's five sections with topic chips and people; the topic page; and no console errors. The published test report records it |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 16; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `3f4af8b1`:
  - `static/js/post.js`, `static/js/void-discovery.js`, `static/js/lib/void-discovery.js`, `static/css/void-discovery.css`.
  - `templates/post.html`, `post-vanished.html`, `void/explore.html`, `void/index.html`, `void/login.html`, `void/sign_up.html`, `void/topic.html`.
  - `lib/feed-context.js` `makeRendererContext`, whose `onExpire` defaults to null.
  - `test/js/void-discovery.test.js`, which matches literal `textContent` assignments in the source; `a11y-markup.test.js` and `feature-stylesheets.test.js`, which read the templates.
  - `.void-discovery-actions` is a flex container, so whitespace between its buttons does not render.

## Branch
`claude/style-post-js-20261009` from spoke `origin/main` `3f4af8b1`.

## Assumptions
None.

## Open Questions
None.

## Design
- **`post.js`:**
  - Viewer parameters are named `viewer`.
  - `rendererContextFor(viewer, onExpire)` builds the one renderer context.
  - New helpers: `setStatusPill`, `replyCountLabel`, `showsRootContext` and `toggleBranch`.
  - `loadViewer` documents why a lapsed session reads anonymously.
  - `loadThreadPage` holds the page load, so the DOM handler only reports errors.
  - Context fills are marked `void`.
  - `renderThread` always returns an array.
- **`void-discovery.js`:** `appendTopicLinks` builds both kinds of topic link, and `personCard` and `personDetail` build people cards. The literal `textContent` lines the test reads are unchanged.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/resources/static/js/post.js` | changed | No shadowing, one renderer context, named helpers and constants, commented catch, explicit fire-and-forget |
| `website/src/main/resources/static/js/void-discovery.js` | changed | One topic-link builder, smaller people functions, named limit |
| `website/src/main/resources/static/js/lib/void-discovery.js` | changed | Commented catch without an unused binding |
| `website/src/main/resources/templates/void/explore.html`, `void/topic.html` | changed | One button per line |
| `website/src/main/resources/static/css/void-discovery.css`, `templates/post.html`, `post-vanished.html`, `void/index.html`, `void/login.html`, `void/sign_up.html` | conforming | No change |
| `website/src/test/js/void-discovery.test.js`, `post-editing.test.js` | conforming | No change; they pass unchanged |

## Task Breakdown

### Task 1 - Conform the post and Void front end

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `post.js`: `rendererContextFor`, `renderRoot`, `renderThread`, `loadViewer`, `loadThreadPage`; `void-discovery.js`: `appendTopicLinks`, `personCard`, `personDetail`; `loadDiscoverySection` |
| **Inspection** | All files in Inputs at `3f4af8b1` |
| **Behavior** | Same DOM, text, requests and error messages |
| **Invariants** | Element IDs, classes, data attributes and routes unchanged |
| **Boundary/API** | None; page scripts export nothing new |
| **Effects and failures** | None new |
| **Tests and evidence** | JavaScript suite; browser walk-through below |
| **Verification** | `node --test website/src/test/js/*.test.js` from the spoke root, then the full Gradle check |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | JavaScript suite; full check; full-diff style review | Covered by AC-3 |
| AC-3 | `void-discovery.test.js` | verify-local-app: build a nested thread through the API as two disposable USERs, then walk the pages in the built-in browser as an anonymous viewer, reading the DOM and console |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The thread page renders differently | Low | Same DOM calls in the same order; the browser walk-through reads the result |
| Discovery panels lose topic chips or people | Low | Literal text assignments unchanged; the explore page is read in the browser |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 16a was in CI.
- **Reason:** I worked ahead on files that 16a does not touch.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1508 (`7ec9ae1`) and auto-deployed. Production serves `7ec9ae1`, and `/void/explore` returns 200.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-11-33-christopherbell-dev-post-and-void-front-end-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 3 of 3 setup cases and all 12 browser walk-through checks passed on candidate `3d875c5`, with no console errors ([report](../test-reports/2026-10-09-11-33-christopherbell-dev-post-and-void-front-end-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1508](https://github.com/azurras/christopherbell.dev/pull/1508) merged as `7ec9ae1` after all checks passed; production `/actuator/info` reports `7ec9ae1` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
