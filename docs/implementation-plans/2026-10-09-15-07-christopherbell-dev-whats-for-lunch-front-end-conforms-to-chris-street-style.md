# What's for Lunch Front End Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The What's for Lunch scripts, templates and stylesheet conform to write-chris-street-style-code, and the picks, list and restaurant pages behave as before.

## Background
This is slice 17g of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 17e](2026-10-09-14-59-christopherbell-dev-whats-for-lunch-restaurant-service-conforms-to-chris-street.md). Inspection at `7a1b0974` found:

1. **`whats-for-lunch.js` (1,162 lines):**
   - One 125-line page click handler repeats the same `event.target instanceof Element ? closest(...) : null` lookup ten times, and inlines link copying, restaurant deletion and card navigation.
   - Errors are named `err`.
   - Seven catches bind an unused `_`.
2. **`wfl-list.js` and `lib/wfl-anonymous-session.js`:** one unused `_` catch binding each.
3. **Conforming:**
   - `lib/wfl-ui.js`, `lib/wfl-freshness.js` and `restaurant-profile.js`.
   - The templates `whatsforlunch.html`, `wfl-list.html` and `restaurant.html`. Their only long lines are single social-preview expressions.
   - `whats-for-lunch.css`. Its four `!important` rules are the reduced-motion override.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The pages render and respond to clicks as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Shared libraries (`util.js`, `api.js`, `restaurant-vote-mutation.js`, `safe-http-link.js`) | Slice 22 |
| Splitting `th:replace` social-preview expressions | Same reason as slice 16b: single Thymeleaf expressions |
| CSS custom properties beyond the existing `--lunch-void-*` tokens | Slice 23 owns the shared style system |
| `RestaurantController` | Slice 17f |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | The 390 JavaScript tests and `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On a candidate with isolated MongoDB `test`, the built-in browser shows `/wfl` rendering for an anonymous viewer; the tool tabs switching panels; filter clearing; a malformed ZIP blocked by validation and a well-formed but unknown ZIP reported as an error; the Top 10 Liked page rendering; and no console errors. The published test report records it |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `7a1b0974`:
  - `whats-for-lunch.js`, `wfl-list.js`, `restaurant-profile.js`, `lib/wfl-ui.js`, `lib/wfl-freshness.js` and `lib/wfl-anonymous-session.js`.
  - `whatsforlunch.html`, `wfl-list.html`, `restaurant.html` and `whats-for-lunch.css`.
  - The JavaScript tests that import these modules or match their source text: `whats-for-lunch-*.test.js`, `wfl-*.test.js` and `a11y-markup.test.js`.

## Branch
`claude/style-lunch-js-20261009` from spoke `origin/main` `7a1b0974`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Click handler:**
  - `closestTarget(event, selector)` replaces the repeated lookup.
  - `CLICK_ACTIONS` lists the ten selectors in their original priority order, each with a named action. The first match wins, exactly as the `if`/`return` chain did.
  - Clicks that match nothing fall through to `openPickCard`.
  - Link copying, deletion and card navigation become `copySessionLink`, `deleteRestaurant` and `openPickCard`.
- **Catches:** catches whose error is unused use `catch {`; the others name it `error`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/resources/static/js/whats-for-lunch.js` | changed | Action table and named actions; `error` names; no unused catch bindings |
| `website/src/main/resources/static/js/wfl-list.js`, `lib/wfl-anonymous-session.js` | changed | No unused catch binding |
| `website/src/main/resources/static/js/restaurant-profile.js`, `lib/wfl-ui.js`, `lib/wfl-freshness.js` | conforming | No change |
| `website/src/main/resources/templates/whatsforlunch.html`, `wfl-list.html`, `restaurant.html` | conforming | No change |
| `website/src/main/resources/static/css/whats-for-lunch.css` | conforming | No change |
| `website/src/test/js/whats-for-lunch-copy.test.js`, `whats-for-lunch-session-recovery.test.js`, `whats-for-lunch-vote.test.js`, `wfl-anonymous-session.test.js`, `wfl-freshness.test.js`, `wfl-ui.test.js`, `wfl-thumbs-contract.test.js` | conforming | No change; they pass unchanged |

## Task Breakdown

### Task 1 - Conform the lunch front end

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `whats-for-lunch.js`: `closestTarget`, `CLICK_ACTIONS`, `refreshLocation`, `clearFilters`, `showControlPanel`, `copySessionLink`, `deleteRestaurant`, `openPickCard` |
| **Inspection** | All files in Inputs at `7a1b0974` |
| **Behavior** | Same click priorities, requests, messages and DOM |
| **Invariants** | Element classes, data attributes and routes unchanged |
| **Boundary/API** | None; the module's exports are unchanged |
| **Effects and failures** | None new |
| **Tests and evidence** | JavaScript suite; browser walk-through below |
| **Verification** | `node --test website/src/test/js/*.test.js` from the spoke root, then the full Gradle check |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | JavaScript suite; full check; full-diff style review | Covered by AC-3 |
| AC-3 | Lunch JavaScript tests | verify-local-app: the anonymous browser walk-through in AC-3. Pick cards, votes, favorites, sessions and deletion need restaurants, which only an ADMIN or a live import can create; the vote and session-recovery tests cover those controllers |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A click reaches a different action | Low | The table keeps the original order and the first-match rule; the browser walk-through clicks the reachable controls |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slices 17d and 17e were in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
