# Survive moves into menus and a tabbed side panel

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> The Survive page is calmer: moves live in Explore, Build (with a Craft submenu) and Camp menus that list only what is possible, situation moves appear directly, and survivor, camp, journal and guide details share one tabbed panel under always-visible vitals. Live in production.

## Background
On 2026-10-18 the user said the Survive UI has "kind of a lot going on" and suggested menus and submenus. The page showed the scene, 17 action buttons (most disabled), survivor stats, inventory, weapon, the shared camp with the gift form, the journal and a long field guide at once. In the brainstorm the user chose category menus listing only possible moves and a tabbed side panel, and approved the design in chat.

## Goals
- Moves are reached through Explore, Build, Craft and Camp menus that list only allowed moves, with situation moves shown directly. (AC-1)
- Menus follow the keyboard and screen-reader menu-button pattern and survive polling. (AC-2)
- Details live in Survivor, Camp, Journal and Guide tabs under always-visible vitals. (AC-3)
- Gameplay, scene clicks and gifts behave exactly as before. (AC-4)
- The change is verified locally, merged through required CI and served by production. (AC-5)

## Non-Goals
| Not doing | Why |
|---|---|
| Java, API, schema or data changes | Layout only; the server keeps every rule. |
| Showing locked moves with costs in menus | The user chose menus listing only possible moves; costs live in the Guide tab. |
| Changing the scene art or hotspots | Out of scope; scene clicks keep working. |
| A settings or sound menu | Not requested. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | While exploring, the action bar shows Explore (gather wood, gather stone, hunt), Build (shelter, boat, Craft submenu with club, stone axe and spear) and Camp (eat, rest, guard, sleep, sail away); each lists only moves in the latest `state.actions`, shows the count, is disabled at zero, and Craft appears only when a craft is allowed. In combat the bar shows Attack, Defend and Flee directly; asleep only Wake; dead or escaped only Start a new survivor. Choosing a move sends it once through the existing serialized action path and closes the menu. |
| AC-2 | Menu buttons use `aria-haspopup="menu"` and `aria-expanded`; Enter, Space or Arrow Down opens and focuses the first item; arrows, Home and End move; Escape and Tab close and Escape returns focus; Arrow Right opens Craft and Arrow Left closes it; a click outside closes; only one menu is open; a poll that changes allowed moves updates an open menu in place without closing it or losing focus unless the focused move disappeared. |
| AC-3 | Health, fullness and the hunger warning stay visible above a `role="tablist"` with Survivor, Camp, Journal and Guide tabs using roving focus and arrow keys; the chosen tab persists in `localStorage` with a safe fallback to Survivor; the Journal tab shows an unread marker when new events arrive while another tab is selected; the field guide moves into Guide. |
| AC-4 | Existing Survive JS tests pass, adjusted only for the new structure; scene clicks, gifts, joining, restart, refresh and polling behave as before. |
| AC-5 | JS tests, `:website:build` and semantic review pass; the committed candidate runs locally against disposable MongoDB with a published runtime report including desktop and phone browser checks; the PR merges after required CI through the deployment queue; production serves the merge and `/survive` shows the menus and tabs. |

## Inputs
- **Request:** "Need to clean up the UI a bit.... kind of a lot going on... maybe some menus and sub menus?" (2026-10-18).
- **User decisions (2026-10-18):** category menus listing only possible moves; tabbed side panel; design approved in chat.
- **Inspected spoke:** origin/main `ad110ad`: `templates/survive.html`, `static/js/survive.js` (`renderSurviveState`, `mountSurvive`, `act`), `static/js/survive-scene.js`, `static/css/survive.css`, `src/test/js/survive.test.js` fixture, `src/test/js/a11y-markup.test.js` (buttons declare `type`).

## Branch
`claude/survive-menus-20261018` from origin/main `ad110ad` in an isolated worktree of the christopherbell-dev spoke.

## Assumptions
- Menu items keep their `data-action` attributes, so the existing click handler and serialization need no new path.
- A small fake DOM in the test directory is enough to test menu and tab keyboard behavior under Node's test runner.

## Open Questions
None.

## Design
The template keeps every move as a `button` with `data-action`, now placed in three menus inside `#surviveActionBar`: each menu is a `button` with `aria-haspopup="menu"` and a `role="menu"` list of `role="menuitem"` buttons, and Build contains a Craft `menuitem` that opens a nested `role="menu"`. Situation moves (Attack, Defend, Flee, Wake) and a Start a new survivor button sit in a direct group. `renderSurviveState` sets each move's `hidden` and `disabled` from `state.actions` and the pending flag, shows the menus only while exploring, then calls `syncActionMenus` to update counts, disabled menu buttons, Craft visibility and focus. A new `survive-menus.js` owns menu and tab behavior: `mountActionMenus` wires opening, closing, keyboard movement, outside clicks and closing after a choice; `syncActionMenus` keeps open menus valid across renders; `mountPanelTabs` wires tabs with roving `tabindex`, persists the choice through guarded `localStorage`, and `noteJournalEvents` marks unread journal activity. The side panel shows vitals first and the tabs below; the Journal and Guide sections move into tabs.

| Alternative | Why not |
|---|---|
| Native `<details>` menus | No menu semantics or arrow-key movement, and they stay open across polls inconsistently. |
| Building menus in JavaScript from a table | Duplicates the move labels and costs that the template already holds. |
| Showing locked moves | The user chose menus that list only possible moves. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/resources/static/js/survive-menus.js` | New menu, submenu and tab behavior. |
| `website/src/main/resources/static/js/survive.js` | Move visibility by state and menus; mount and dispose menus and tabs; journal unread marker. |
| `website/src/main/resources/templates/survive.html` | Action bar menus, direct moves, vitals, tablist and panels; guide and journal moved into tabs; shorter hero. |
| `website/src/main/resources/static/css/survive.css` | Menu, submenu, tab and layout styles, including phone layout. |
| `website/src/main/java/dev/christopherbell/survive/README.md` | Browser layout note. |
| `website/src/test/js/survive-menus.test.js`, `website/src/test/js/support/fake-dom.js` | New menu and tab tests with a minimal DOM. |
| `website/src/test/js/survive.test.js` | Fixture and assertions for the new structure. |

## Task Breakdown
### Task 1 - Menu and tab behavior
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `static/js/survive-menus.js` (new, beside `survive-scene.js`), `src/test/js/survive-menus.test.js`, `src/test/js/support/fake-dom.js` (new). |
| **Symbols** | `mountActionMenus`, `syncActionMenus`, `mountPanelTabs`, `noteJournalEvents`. |
| **Inspection** | Read the `act` handler and render flow in `survive.js` at `ad110ad`. |
| **Behavior** | AC-2 and AC-3 keyboard, pointer, persistence and polling behavior. |
| **Invariants** | No game rules; no `innerHTML`; every listener removed on dispose; storage failures never break the page. |
| **Boundary/API** | New ES module exports only. |
| **Effects and failures** | Focus and attribute changes inside the page; storage read and write guarded. |
| **Tests and evidence** | RED then GREEN fake-DOM tests. |
| **Verification** | `node --test website/src/test/js/survive-menus.test.js` |

### Task 2 - Page structure, rendering and styles
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1. |
| **Files** | `templates/survive.html`, `static/js/survive.js`, `static/css/survive.css`, `survive/README.md`, `src/test/js/survive.test.js`. |
| **Symbols** | `renderSurviveState`, `mountSurvive`. |
| **Inspection** | Read the template, render function and fixture at `ad110ad`. |
| **Behavior** | AC-1 and AC-4. |
| **Invariants** | One request at a time; server-allowed actions only; text nodes only; existing ids kept where tests and scripts use them. |
| **Boundary/API** | Same endpoints and request bodies. |
| **Effects and failures** | Unchanged request failure handling. |
| **Tests and evidence** | Updated and new render tests; full JS suite. |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 :website:build` |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Render tests for menu contents, counts, Craft visibility and direct moves per status | Browser: open each menu while exploring, use Craft, fight, sleep and die or escape states where reachable |
| AC-2 | Fake-DOM keyboard, outside-click and polling tests | Browser keyboard run through a menu and the Craft submenu; menu stays open across a poll |
| AC-3 | Tab keyboard, persistence, fallback and unread tests | Browser tab switching, reload keeps the tab, journal marker appears |
| AC-4 | Existing Survive JS tests | Scene click and a gift still work |
| AC-5 | `:website:build`, semantic review | verify-local-app report before the PR; production readback after merge |

- **Regressions:** scene tests, a11y markup tests and the full JS suite stay green.

## Rollback or Recovery
Revert the merge commit; the deployment pipeline serves the previous build. Front end only, with no stored data.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Polling closes menus or steals focus | Medium | `syncActionMenus` updates in place; polling test. |
| Moves become hard to find | Low | Counts on menu buttons; scene hotspots still glow; Guide lists every move. |
| Keyboard traps in nested menus | Low | Escape and Tab always close; tests for each key. |

## Implementation Log

### 2026-10-18 - Pending requests mark the action bar busy instead of disabling moves

- **Change:** While a request is pending, `renderSurviveState` now marks `#surviveActionBar` with `aria-busy="true"` and a busy style instead of setting `disabled` on every allowed move. The click handler's pending guard still blocks double sends.
- **Reason:** The browser run on `eed2dd1` showed every 5-second poll dropping keyboard focus out of an open menu, because disabling the focused button blurs it. Escape then had nothing to close.
- **Impact:** Design and AC-2 behavior hold; page tests now assert `aria-busy` instead of disabled moves.

### 2026-10-18 - Focus stays in the action bar when a menu empties

- **Change:** `syncActionMenus` moves focus to the first enabled menu button when the focused menu button becomes disabled.
- **Reason:** In the same run, crafting the last affordable item disabled the Build button that had just received focus, and focus fell to the page body.
- **Impact:** New test `focus moves to an enabled menu button when the focused menu empties`.

### 2026-10-18 - Shared camp heading kept in the Camp tab

- **Change:** The Camp tab keeps a "Shared camp" heading.
- **Reason:** `ViewControllerTest` asserts the page names the shared camp, and the tab reads better with a heading.
- **Impact:** Template only.

### 2026-10-18 - Focus returns to the action bar when it changes shape

- **Change:** New `keepFocusInActionBar`: when focus was in the action bar before a render and the focused control is now hidden or disabled, focus moves to the bar's first usable control.
- **Reason:** The browser run on `c3c620d` showed focus falling to the page body when a fight started (the menus group hides), when sleeping, and when the fight ended (Attack hides).
- **Impact:** AC-2 focus behavior now covers the bar changing shape; new test `focus that was in the bar moves to the first usable control when the bar changes shape`.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
