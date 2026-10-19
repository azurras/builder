# Survive side panel becomes a status card with collapsible extras

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> Players see everything they use every turn without switching: an always-visible status card holds vitals, inventory, weapon, stats and the latest events, and camp, journal and guide sit in remembered collapsible sections. Live in production.

## Background
On 2026-10-19 the user said the tabs from [the menus and tabs plan](2026-10-18-08-45-christopherbell-dev-survive-menus-and-tabs.md) are "not a great experience" and, asked why, chose "too much switching": inventory, weapon and recent events were hidden behind tabs. The user chose a status card with collapsible extras and approved the design in chat.

## Goals
- An always-visible status card shows name, save status, health, fullness, hunger warning, inventory with capacity, weapon and uses, stats and the last 3 events. (AC-1)
- Camp and sharing, the full journal and the guide are native collapsible sections, closed by default, remembered per browser and never toggled by polling. (AC-2)
- Closed sections summarize themselves, and the journal marks new events until opened. (AC-3)
- Menus, scene clicks, gifts and polling behave as before. (AC-4)
- The change is verified locally, merged through required CI and served by production. (AC-5)

## Non-Goals
| Not doing | Why |
|---|---|
| Changing menus, the scene or game rules | Out of scope; only the side panel changes. |
| Java, API or data changes | Layout only. |
| Custom disclosure widgets | Native `details` and `summary` are accessible without custom keyboard code. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The status card always shows name, save line, health and fullness meters, hunger warning, Wood, Food and Stone with `carried / capacity`, weapon with uses or Bare hands, Strength, Stamina and XP, the 3 newest events newest first, camp ID, Refresh world and New survivor; no tab strip remains. |
| AC-2 | Camp & sharing, Journal and Guide are `details` sections closed on first visit; opening or closing one is remembered in `localStorage` and restored on load, with a safe fallback when storage fails; renders and polls never change their open state; a Full journal link opens and reveals the Journal section. |
| AC-3 | The Camp summary reads like "2 shelters · 1 boat · 3 survivors"; the Journal summary shows a new-events marker when the world changed while it was closed and clears it when opened. |
| AC-4 | Survive JS tests for menus, scene, gifts and polling pass; gifts still work from the Camp section. |
| AC-5 | JS tests, `:website:build` and semantic review pass; the committed candidate runs locally against disposable MongoDB with a published runtime report including desktop and phone browser checks; the PR merges after required CI through the deployment queue; production serves the merge and `/survive` shows the status card. |

## Inputs
- **Request:** "the tabs are not a great experience" (2026-10-19); reason chosen: too much switching; layout chosen: status card plus collapsible extras; design approved in chat.
- **Inspected spoke:** origin/main `43e0be3`: `templates/survive.html` side panel and tabs, `static/js/survive.js` (`renderSurviveState`, `mountSurvive`, `noteJournalEvents` use), `static/js/survive-menus.js` (`mountPanelTabs`, `noteJournalEvents`), `static/css/survive.css` tab rules, `src/test/js/survive-menus.test.js` tab tests, `src/test/js/survive.test.js` fixture tabs, `ViewControllerTest` "Shared camp" assertion.

## Branch
`claude/survive-status-card-20261019` from origin/main `43e0be3` in an isolated worktree of the christopherbell-dev spoke.

## Assumptions
- Native `details` elements fire `toggle` when opened or closed by the user, which is enough to remember their state.

## Open Questions
None.

## Design
The side panel keeps the vitals panel and grows it into a status card: inventory row, weapon line, compact stats line, a Recent list of the 3 newest events and a footer with camp ID, Refresh world and New survivor. Below it, three `details` sections with `summary` headings replace the tablist. A new module `survive-panel.js` owns panel behavior and replaces the tab code in `survive-menus.js`: `mountPanelSections` restores and remembers each section's open state through guarded `localStorage` and wires the Full journal link; `noteJournalEvents` marks the Journal summary while closed and clears it on open; `summarizeCamp` builds the Camp summary text. `renderSurviveState` fills the new fields with text nodes only and never touches `open`.

| Alternative | Why not |
|---|---|
| Keep tabs and move inventory above them | The user chose no tabs. |
| Everything expanded | A long column; the user chose collapsible extras. |
| Custom accordion buttons | Native `details` already give keyboard and screen-reader behavior. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/resources/templates/survive.html` | Status card fields and footer; three `details` sections replace the tablist and panels. |
| `website/src/main/resources/static/js/survive-panel.js` | New section memory, journal marker, camp summary and Full journal link. |
| `website/src/main/resources/static/js/survive-menus.js` | Tab functions removed. |
| `website/src/main/resources/static/js/survive.js` | Render the status card, recent events and summaries; mount the panel instead of tabs. |
| `website/src/main/resources/static/css/survive.css` | Status card and section styles; tab styles removed. |
| `website/src/main/java/dev/christopherbell/survive/README.md` | Side panel description. |
| `website/src/test/js/survive-panel.test.js`, `survive-menus.test.js`, `survive.test.js` | Panel tests replace tab tests; page fixture updated. |

## Task Breakdown
### Task 1 - Status card and collapsible sections
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `templates/survive.html`, `static/js/survive-panel.js` (new, beside `survive-menus.js`), `static/js/survive-menus.js`, `static/js/survive.js`, `static/css/survive.css`, `survive/README.md`, `src/test/js/survive-panel.test.js` (new), `src/test/js/survive-menus.test.js`, `src/test/js/survive.test.js`. |
| **Symbols** | `mountPanelSections`, `noteJournalEvents`, `summarizeCamp`, `renderSurviveState`, `mountSurvive`; removed `mountPanelTabs`. |
| **Inspection** | Read the side panel template, render and mount code, and tab tests at `43e0be3`. |
| **Behavior** | AC-1 to AC-4. |
| **Invariants** | Text nodes only; renders never toggle sections; storage failures never break the page; every listener removed on dispose. |
| **Boundary/API** | Same endpoints; existing element ids used by tests and scripts kept. |
| **Effects and failures** | `localStorage` reads and writes guarded. |
| **Tests and evidence** | RED then GREEN panel tests; updated page tests. |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 :website:build` |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Page render tests for every status card field and recent events | Browser desktop and phone: card visible while playing; no tabs |
| AC-2 | Panel tests for restore, remember, fallback, Full journal link and renders not toggling | Open Camp, reload, still open; poll leaves sections alone |
| AC-3 | Summary and marker tests | Camp summary text; journal marker appears while closed and clears on open |
| AC-4 | Existing Survive JS tests | A gift from the Camp section; a menu move; a scene click |
| AC-5 | `:website:build`, semantic review | verify-local-app report before the PR; production readback after merge |

- **Regressions:** menus, scene and a11y markup tests stay green; `ViewControllerTest` still finds "Shared camp".

## Rollback or Recovery
Revert the merge commit; the deployment pipeline serves the previous build. Front end only, with no stored data.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| The status card grows too tall on phones | Medium | Compact rows; check at 375 px. |
| Polling overwrites open sections | Low | Render never touches `open`; test. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
