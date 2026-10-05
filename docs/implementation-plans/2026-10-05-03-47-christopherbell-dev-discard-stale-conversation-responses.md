# Discard stale conversation responses

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Keep the selected private conversation consistent when history requests finish out of order, and prevent an older-page response from mutating a newly selected conversation.

## Background
The audit review of `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c` found that `openConversation()` and `loadOlderMessages()` mutate shared page state after awaiting fetches without checking whether their selected conversation is still current. Selecting B while A's request remains pending can render A's messages under B's title or merge A's older page into B.

## Goals
- Discard any conversation-page result that no longer belongs to the selected conversation (AC-1).
- Keep the correction small and cover both first-page and older-page ordering with deterministic browser tests (AC-1, AC-2).
- Run required native checks and attempt local candidate runtime verification before any PR (AC-2, AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing message API routes or response contracts | The race is entirely in browser response ownership. |
| Reworking conversation-list refresh, sending, or archive flows beyond invalidating responses when selection changes | Keep this correction limited to conversation history responses. |
| Creating or updating PR #1477 | The user said not to trust that draft; it is excluded from this audit and evidence. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | If A then B are selected and A resolves last, only B's history is rendered and B remains selected; a pending older-page response from A cannot alter B's history. |
| AC-2 | Focused JavaScript race regressions, the full website JavaScript suite, syntax checks, and the repository's required native checks pass on the committed candidate. |
| AC-3 | The committed candidate runs locally with isolated test resources, the Messages page reaches meaningful readiness, and both race scenarios are exercised; if the known migration-015 test-database blocker prevents startup, record the exact candidate and blocker and do not create a PR. |

## Inputs
- **Request:** User requested a whole-codebase Chris Street Style rewrite through small changes, each with an implementation plan and test report; user explicitly excluded trust in PR #1477.
- **Reviewed source:** `website/src/main/resources/static/js/messages.js`, `website/src/test/js/messages-rendering.test.js`, and `website/src/main/resources/static/js/README.md` at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- **Repository guidance:** Root `AGENTS.md` and `website/src/main/resources/static/js/README.md`.
- **Style guidance:** `write-chris-street-style-code` JavaScript, design/API, naming/readability, and testing/review references.

## Branch
`codex/discard-stale-conversation-responses-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.

## Assumptions
- Page-history fetches may overlap because the user can change selected conversation before an earlier request completes.
- A monotonically increasing selection generation can identify which pending request still owns the current selection without changing API behavior.
- The candidate's supported isolated runtime uses MongoDB database `test`; this does not authorize direct database writes or bypassing startup migrations.

## Open Questions
None.

## Design
Capture the normalized username and a selection generation when opening a conversation. Check both after each relevant await before writing `THREAD_STATE`, rendering history, or updating the URL. Capture the same ownership token and cursor before loading an older page, then discard stale success and stale error outcomes before changing shared state or alert UI. Reset the shared older-page button when selecting a new conversation so an abandoned request cannot leave the newly selected view disabled. Add controlled-promise tests against the page module's existing native test harness. Update the JavaScript feature guide to document stale-response ownership.

| Alternative | Why not |
|---|---|
| Abort in-flight requests | Cancellation does not guarantee a response already completing cannot race with state mutation; an ownership check is still needed. |
| Move all conversation state into a new controller abstraction | Adds a new abstraction for one page without a second consumer. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/resources/static/js/messages.js` | Name and check selection ownership around asynchronous history responses. |
| `website/src/test/js/messages-rendering.test.js` | Add deterministic late-first-page and late-older-page regressions. |
| `website/src/main/resources/static/js/README.md` | Document conversation history's stale-response guard. |

## Task Breakdown
### Task 1 - Guard conversation history mutations by selection
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/resources/static/js/messages.js`; `website/src/test/js/messages-rendering.test.js`; `website/src/main/resources/static/js/README.md`. |
| **Symbols** | `openConversation`, `loadOlderMessages`, selection-generation state, Messages page race tests. |
| **Inspection** | Read definitions, DOM setup, API behavior, test harness, feature guide, and applicable style references at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Behavior** | Only the currently selected conversation's latest first-page response can render or update its URL; an older-page response can merge only into the conversation and cursor it was requested for. |
| **Invariants** | No API changes; selected title/profile/form stay aligned with displayed messages; abandoned requests cannot change another selection; messages remain safely rendered. |
| **Boundary/API** | Private page-module functions only; do not change server endpoints or payload shape. |
| **Effects and failures** | Fetches remain awaited; stale success and failure cannot mutate current selection state or surface a misleading alert; shared control cleanup remains bounded to the current selection. |
| **Tests and evidence** | Witness controlled A/B request reordering and an older-page request completing after a selection change; run focused JS test, all `:website:jsTest`, syntax checks, full native gate and packaged local runtime check. |
| **Verification** | `node --check website/src/main/resources/static/js/messages.js`; `node --test website/src/test/js/messages-rendering.test.js`; `.\gradlew.bat --no-parallel --max-workers=4 :website:jsTest :website:check :cbell-lib:check :website:bootJar`; run and exercise committed candidate using `verify-local-app`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Controlled-promise browser tests for A/B first-page ordering and stale older-page completion; `:website:jsTest`; syntax check. | Select two conversations and switch selection while older history is pending; verify displayed messages, title, profile, and URL remain associated with the latest selection. |
| AC-2 | Full website and shared-library checks, browser suite, and packaged JAR build. | Run the committed packaged candidate on a free non-production port with isolated MongoDB `test` and app-owned scratch storage. |
| AC-3 | Build and all native checks identify the exact candidate artifact. | Readiness plus both selected-conversation flows and cleanup evidence; migration 015 failure means AC-3 blocked and no PR. |

Regressions and edge cases:
- Resolve A after B and verify A cannot replace B's messages or URL.
- Complete A's older-page request after switching to B and verify B's messages and cursor are unchanged.
- Confirm a current selection still loads, paginates, and reports current-request errors as before.

## Rollback or Recovery
The change is limited to page-local JavaScript, tests, and its feature guide. Revert the single candidate commit if native checks expose regressions; no persistent data or API migration is involved. If local startup fails at the known incomplete test migration, stop only the candidate process tree, confirm the port is free, retain database state, and leave the change unsubmitted.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A stale response guard is omitted after an await | Medium | Check ownership before each shared-state/UI mutation and test controlled completion order. |
| A stale pagination request leaves the shared button disabled | Medium | Reset the page control when selection changes and guard cleanup ownership. |
| Local runtime cannot reach readiness because migration 015 is incomplete | High based on current audit evidence | Record the exact candidate's failed startup, do not bypass or repair the database, and do not create a PR. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2

## Plan Format
task-contract-v2

