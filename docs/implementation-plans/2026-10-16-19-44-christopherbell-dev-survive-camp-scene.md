# Survive gets an illustrated, clickable camp scene

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> Survive on christopherbell.dev shows a flat-vector SVG camp scene that mirrors the shared world and lets players act by clicking it, with the existing buttons kept as the accessible path, live in production.

## Background
On 2026-10-16 the user asked to "give the game a gui". Survive already has a panel-and-button page, so the request was read as a visual game view. In the brainstorm the same day the user chose an illustrated camp scene over a walkable map or a restyle, flat vector SVG over pixel art or painterly art, and a clickable scene alongside the buttons over a display-only scene. They approved all three design sections. The game's clock, raids, enemies, weapons, sleep and hunger shipped earlier that day in [the previous plan](2026-10-16-14-42-christopherbell-dev-survive-clock-danger-weapons-sleep-and-hunger.md).

## Goals
- The scene shows the phase, camp structures, survivors, the player's gear and state, and any enemy, from the server snapshot alone. (AC-1)
- Clicking scene objects sends the same server actions as the buttons, only when allowed and never twice. (AC-2)
- The scene stays accessible: a state-generated description, buttons as the keyboard path, reduced motion and phone-sized touch targets. (AC-3)
- Untrusted names are rendered safely. (AC-4)
- The change is verified locally, merged through required CI and served by production. (AC-5)

## Non-Goals
| Not doing | Why |
|---|---|
| A walkable map, positions or movement | The user chose the camp scene; movement would add server rules. |
| Any Java, API, schema or saved-data change | The scene renders the existing snapshot; the server keeps owning every rule. |
| Clickable building, crafting, eating or gifting in the scene | They have no natural place in the scene; buttons and the gift panel stay. |
| Image assets, a canvas or a new framework | The user chose code-drawn SVG; the site uses vanilla modules. |
| Removing or hiding the existing buttons | They remain the keyboard and screen-reader path. |
| Sound | Not requested. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `renderSurviveScene` draws: a sky for `DAY`, `DUSK` and `NIGHT` (stars and moon at night) with a phase progress arc; trees, rocks, forest edge and shore; a fire; up to 6 tents and 3 boats with a `+N` tag beyond; up to 8 survivors with the player highlighted and named, plus `+N`; a guard torch and sleeping `z z` for the player; a gravestone for `DEAD` and a sailing boat for `ESCAPED`; the held weapon; a hog, wolf or bear with a health bar in `COMBAT`; and a raid flash when the newest event is a raid. |
| AC-2 | Trees send `GATHER`, rocks `GATHER_STONE`, the forest edge `HUNT`, the fire `GUARD` when allowed and otherwise `REST`, a tent `SLEEP` or `WAKE`, a boat `ESCAPE` and the enemy `ATTACK`. A click sends only an action present in the latest `state.actions`, with the current revision, through the existing serialized request path; disallowed objects and clicks while a request is pending send nothing. |
| AC-3 | The SVG has `role="img"` and an `aria-label` from `describeScene(state)` naming phase, day, structures, survivors, enemy and the player's state; hotspots are `aria-hidden` and not tab stops; allowed hotspots glow and show a pointer; `prefers-reduced-motion` disables the fire flicker, twinkle, smoke and raid flash; at 375 px wide every hotspot is at least 44 px in its smaller dimension; the page has no horizontal scroll. |
| AC-4 | Names and every other server string reach the scene only through `textContent` or attribute setters; the test fixture that traps `innerHTML` passes with a hostile name. |
| AC-5 | JS tests, `:website:build` and semantic review pass; the committed candidate runs locally against disposable MongoDB with a published runtime report including browser screenshots by phase; the PR merges after required CI through the deployment queue; production serves the merge and `/survive` includes the scene. |

## Inputs
- **Request:** "give the game a gui" (2026-10-16).
- **User decisions (2026-10-16):** illustrated camp scene; flat vector SVG; clickable scene plus buttons; design sections 1 (what the scene shows), 2 (clicking and accessibility) and 3 (files and testing) approved.
- **Inspected spoke:** `A:\Projects\christopherbell.dev` at origin/main `4e2a2b0`: `static/js/survive.js` (`renderSurviveState`, `mountSurvive`, the `act` click handler and pending serialization), `templates/survive.html` (adventure panel, `surviveActions`, field guide), `static/css/survive.css`, `src/test/js/survive.test.js` (document fixture trapping `innerHTML`), `src/test/js/app-entry-budget.test.js` (budget applies to the `app.js` graph only), `src/test/js/a11y-markup.test.js` (buttons must declare a type), `website/build.gradle.kts` `jsTest` task, and the `SurviveSnapshot` fields.

## Branch
`claude/survive-camp-scene-20261016` from origin/main `4e2a2b0` in an isolated worktree of the christopherbell-dev spoke.

## Assumptions
- The existing 5-second poll and phase-change refresh are frequent enough to animate state changes; no extra endpoint is needed.
- Node's test runner can test SVG building through a fixture document that records `createElementNS` calls, as the existing fixture does for HTML elements.
- A scene of a few hundred SVG nodes rebuilt per render performs well on phones; layers are replaced only when their inputs change.

## Open Questions
None.

## Design
Add a focused module `survive-scene.js` that owns drawing. It exports `renderSurviveScene(documentRoot, svgRoot, state)` and `describeScene(state)` and imports nothing from the network layer. The scene is composed of named layer groups (`sky`, `land`, `camp`, `survivors`, `enemy`, `effects`), each rebuilt from a small derived view model (for example `{ phase, tents, extraTents }`). A layer whose view model is unchanged since the last render is left alone, which keeps the 5-second poll cheap and avoids restarting CSS animations. Shapes are built with `createElementNS(SVG_NS, ...)`, `setAttribute` and `textContent` only.

`survive.js` calls the scene renderer from `renderSurviveState`. Interactive groups carry `data-action`. The existing `act` click handler moves from the button container to a shared handler on the actions container and the scene, and continues to resolve `closest('[data-action]')`. It sends only when the action is in `state.actions` and nothing is pending. The fire resolves its action from state (`GUARD` if allowed, otherwise `REST`) and a tent resolves `WAKE` while sleeping, otherwise `SLEEP`; the renderer sets the resolved `data-action` and an `is-available` class on each render, so CSS shows the glow and click handling stays uniform. Hotspots are `aria-hidden="true"` with no `tabindex`. The SVG `aria-label` comes from `describeScene`.

CSS defines phase palettes through custom properties on the SVG (`data-phase`), the hover and focus-visible glow for `.is-available`, small keyframe animations, and a `prefers-reduced-motion: reduce` block that removes them. The viewBox is 960×540 and the SVG is `width: 100%`. Hotspot shapes are sized so that at 375 px wide the smallest is at least 44 px.

| Alternative | Why not |
|---|---|
| Static SVG in the template toggled by classes | Cannot draw variable counts of tents, boats and survivors. |
| Canvas renderer | The user chose vector; canvas also needs a parallel accessibility tree. |
| Making hotspots tab stops | Duplicates over 20 keyboard stops that the buttons already provide. |
| Drawing in `survive.js` | The file would mix transport and drawing; a separate module keeps both readable and testable. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/resources/static/js/survive-scene.js` | New SVG scene renderer and `describeScene`. |
| `website/src/main/resources/static/js/survive.js` | Render the scene each time; route scene clicks through the shared, state-checked action handler. |
| `website/src/main/resources/templates/survive.html` | Scene `<svg>` at the top of the adventure panel; field-guide line about clicking the scene. |
| `website/src/main/resources/static/css/survive.css` | Scene sizing, phase palettes, hotspot glow, animations, reduced-motion overrides. |
| `website/src/main/java/dev/christopherbell/survive/README.md` | The scene is display and transport only. |
| `website/src/test/js/survive-scene.test.js` | New rendering, safety, interaction and description tests. |
| `website/src/test/js/survive.test.js` | Fixture support for the scene element and click routing. |

## Task Breakdown
### Task 1 - Scene renderer and description
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `static/js/survive-scene.js` (new, beside `survive.js`), `src/test/js/survive-scene.test.js` (new, beside `survive.test.js`). |
| **Symbols** | `renderSurviveScene`, `describeScene`, layer builders and view models. |
| **Inspection** | Read `survive.js` render flow, the snapshot fields and the `survive.test.js` fixture at `4e2a2b0`. |
| **Behavior** | Every AC-1 element appears for its state; unchanged layers are not rebuilt. |
| **Invariants** | No `innerHTML`; no game rules; output depends only on the snapshot. |
| **Boundary/API** | New ES module exports; no server contract change. |
| **Effects and failures** | DOM mutation inside the SVG only; unknown enum values draw a neutral fallback, never throw. |
| **Tests and evidence** | RED then GREEN scene tests per layer and description. |
| **Verification** | `node --test website/src/test/js/survive-scene.test.js` |

### Task 2 - Clickable scene, page integration and styles
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 for the renderer. |
| **Files** | `static/js/survive.js`, `templates/survive.html`, `static/css/survive.css`, `survive/README.md`, `src/test/js/survive.test.js`. |
| **Symbols** | `renderSurviveState`, `mountSurvive` `act` handler and its listeners and disposal. |
| **Inspection** | Read the `act` handler, `setPending`, `dispose` and template action container at `4e2a2b0`. |
| **Behavior** | Scene clicks send allowed actions once with the current revision; the fire and tent resolve their action from state. |
| **Invariants** | One request at a time; no automatic replay; buttons unchanged; listeners removed on dispose. |
| **Boundary/API** | Same endpoints and request bodies. |
| **Effects and failures** | Request failures reconcile with GET exactly as button clicks do. |
| **Tests and evidence** | Interaction tests for allowed, disallowed and pending clicks; existing tests stay green. |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 :website:jsTest :website:build` |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Scene layer tests for each phase, count cap, survivor marks, enemy, weapon and raid flash | Browser screenshots of the candidate at day, dusk and night, in combat, and with built structures |
| AC-2 | Interaction tests for each hotspot, disallowed clicks and pending clicks | Click trees, rocks, forest edge, enemy, fire at dusk and a tent at night in the candidate; journal and state confirm each action |
| AC-3 | Description tests; a markup test for `role="img"` and `aria-hidden` hotspots | Read the accessibility tree; 375 px viewport screenshot and hotspot sizes; emulated reduced motion stops animations |
| AC-4 | Hostile-name test with the `innerHTML` trap | Join with a markup-like name and confirm it renders as text |
| AC-5 | `:website:build` including `jsTest`, semantic review | verify-local-app report published before the PR; production readback after merge |

- **Regressions:** existing Survive JS tests, button behavior, gift panel and the `app.js` entry budget stay green.
- **Reruns:** rerun affected checks and runtime cases after any runtime-affecting edit before PR creation or update.

## Rollback or Recovery
Revert the merge commit; the deployment pipeline serves the previous build. The change is front-end only with no stored data, so there is nothing to migrate or restore.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Rebuilding SVG on every poll restarts animations or janks phones | Medium | Rebuild a layer only when its view model changes. |
| Scene clicks bypass serialization and double-send | Low | One shared handler with the existing pending guard; interaction tests. |
| Hotspots too small on phones | Medium | Size shapes against a 375 px width and measure in the browser. |
| Art looks crude | Medium | Layered silhouettes, consistent palettes per phase, review screenshots before the PR. |

## Implementation Log

### 2026-10-16 - Hotspots sized for the scene width inside the panel

- **Change:** Every hotspot's smaller side grew from 120 to at least 145 scene units, and the 44-pixel target is measured at the scene's real width inside the panel (301 px on a 375 px phone) instead of the full 375 px.
- **Reason:** The runtime check on `2d41ee9` measured the smallest hotspot at 37 px, because the adventure panel's padding makes the scene narrower than the viewport.
- **Impact:** Design hotspot sizing updated; new size test `every hotspot is large enough to tap at phone width`; runtime proof rerun on `8627fff`.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
