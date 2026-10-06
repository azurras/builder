# Give supplies to another survivor

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> Let survivors give wood or food directly to another survivor in the existing Java-owned shared world.

## Background
The user requested direct survivor interaction after the initial Survive delivery. Current main a42d4b8 provides shared camp construction but private inventories and no targeted commands. Resource giving is the stated first interaction while the user can steer the pending preference question.

## Goals
- Target a specific survivor without revealing credentials. (AC-1)
- Transfer supplies atomically with inventory and revision protection. (AC-2)
- Provide accessible controls and visible shared feedback. (AC-3)
- Verify, merge and read back automatic deployment. (AC-4)

## Non-Goals
| Excluded | Reason |
|---|---|
| Chat, PvP, shared combat, trade negotiation | Different interaction rules beyond this first cooperative action. |
| Persistent worlds or database changes | Preserve existing ephemeral world contract. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Separate public survivor IDs identify recipients, including duplicate names; private cookie tokens remain secret. |
| AC-2 | Java atomically gives 1–10 wood or food between distinct exploring survivors; insufficient supplies, full inventory, missing/expired/terminal recipients, stale sender revision and invalid requests cause no transfer. Both survivor revisions advance on success. |
| AC-3 | Camp UI selects recipient/resource/amount, preserves selections across polling, serializes requests without mutation retries and shows sender/recipient feedback plus a shared journal event. |
| AC-4 | Native tests, semantic review and committed-candidate local two-survivor API/browser proof pass before PR; required CI passes, PR merges and automatic deployment is verified. |

## Inputs
- **Request:** Survivors need a way to interact.
- **Inspection:** Main a42d4b8; SurviveWorld, SurvivePlayer, SurviveService, SurviveController, SurviveSnapshot, SurviveRequests, feature README, survive.js, survive.html, API paths, exact SecurityConfig matchers, service/controller/JS tests and spoke AGENTS.md.
- **History:** Initial delivery plan and 2026-10-05 session entry show one in-memory world with private survivors and disposable test-profile verification.

## Branch
codex/survivor-interactions-20261006 from origin/main a42d4b8 in an owned isolated worktree.

## Assumptions
The user selected supply giving as the first interaction. Both survivors must be at camp (EXPLORING). Receiving does not extend an idle survivor's lifetime; active recipients refresh normally. Existing names list remains compatible; new public recipient summaries carry identity/status.

## Open Questions
None. The user selected giving wood or food.

## Design
Each SurvivePlayer gets a public UUID independent of its private cookie. Snapshot adds own survivorId and a list of eligible recipients with public ID/name; preserve the existing survivors names array. Java computes eligibility. POST /api/survive/v1/gifts accepts recipientId, resource enum WOOD/FOOD, quantity and sender revision. The synchronized service expires inactive players, validates identities/revision/availability/capacity before any mutation, updates both inventories and revisions and records one event. Recipient IDs convey no action authority. Only the cookie controls the sender. UI adds a camp form, displays short IDs to distinguish duplicate names, preserves selected recipient across polling, uses existing serialized request/reconciliation flow and never retries gifts automatically. Feature documentation and field guide explain giving and recipient restrictions.

## Expected Changes
| Area | Change |
|---|---|
| survive domain/service/model/controller and README | Public identity, eligible recipients, atomic gift command and contract. |
| SecurityConfig and security README/tests | Exact CSRF-protected public gift endpoint. |
| survive.html, survive.js, survive.css, lib/api.js | Recipient/resource/amount controls and transport. |
| SurviveServiceTest, SurviveControllerTest, survive.test.js | Atomic giving, rejection, concurrency, secret isolation and UI behavior. |

## Task Breakdown
### Task 1 - Add atomic Java giving and camp controls
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected survive package/model and tests, template, script, CSS, API registry, SecurityConfig and feature/security READMEs. Add survive/model/SurviveResource.java following SurviveAction enum. |
| **Symbols** | Public survivor ID, snapshot recipient summaries, gift request, service giveSupplies, controller gift route and browser form handler. |
| **Inspection** | Main a42d4b8 files named in Inputs; existing service monitor and snapshot rendering/request lifecycle. |
| **Behavior** | Give supplies to a selected survivor and refresh both players' authoritative inventories. |
| **Invariants** | Inventory remains 0–10, transfer conserves supplies, both mutations atomic, credentials hidden, only owner cookie authorizes sender. |
| **Boundary/API** | POST /api/survive/v1/gifts with CSRF and cookie; preserve game/actions endpoints and names array. |
| **Effects and failures** | In-memory mutation only after all checks; 400 invalid/unavailable, 404 identity missing, 409 stale command; no mutation replay. |
| **Tests and evidence** | Start with failing gift tests, verify valid wood/food, duplicates, full inventories, stale/expired/terminal/self cases and competing senders. |
| **Verification** | Focused Java tests, all JS tests, touched JS syntax, full :website:check and :website:bootJar. |

### Task 2 - Verify and deliver the committed candidate
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 checks and review pass. |
| **Files** | Builder plan, runtime report and dated memory. |
| **Symbols** | Candidate identity, runtime evidence and acceptance outcomes. |
| **Inspection** | Existing test-profile startup/report and automatic-deployment contracts. |
| **Behavior** | Tested candidate merges and the live page offers giving controls. |
| **Invariants** | Fresh disposable loopback MongoDB test profile only; report precedes PR. |
| **Boundary/API** | Browser and two cookie jars against actual candidate; read-only production checks. |
| **Effects and failures** | Owned test processes stopped, CI failures diagnosed; preserve unrelated work. |
| **Tests and evidence** | Two survivors transfer supplies, recipient sees change, errors conserve inventories, real mobile/keyboard interaction, deployed SHA. |
| **Verification** | verify-local-app, write-test-report, preflight, PR required CI/merge and live readback. |

## Test Plan
| AC | Native checks | Runtime proof |
|---|---|---|
| AC-1 | Distinct public/private IDs and duplicate name tests | JSON has public recipients but no cookie tokens. |
| AC-2 | Valid/rejected/concurrent transfer tests | Actual API giving wood and food across two cookie jars, conservation and stale/full errors. |
| AC-3 | UI selection/serialization/render tests and syntax | Browser recipient form, keyboard submission, polling and mobile layout. |
| AC-4 | Full website checks and semantic review | verify-local-app on committed jar with disposable test MongoDB; published report before PR and public deployment identity. |

## Rollback or Recovery
Revert through a checked PR and supported automatic deployment. No persistent game data or schema changes; restart resets the ephemeral world as before.

## Risks
| Risk | Mitigation |
|---|---|
| Duplicate names choose wrong recipient | Independent public ID and short ID label in form. |
| Concurrent gifts overfill inventory | Validate and mutate under existing single service monitor. |
| Recipient receiving invalidates an in-flight action | Advance its revision; stale command refreshes without replay. |

## Implementation Log

### 2026-10-06 - Implement giving and preserve form editing during polls

- **Change:** User selected giving wood or food. Implemented public targeting IDs, recipient summaries, atomic gifts and the camp form. Independent review found background polls disabled focused gift fields; separated mutation/request pending and preserve unchanged native options.
- **Reason:** Confirmed interaction preference; receiving must not leak cookies or overfill inventory, and refresh must not interrupt typing.
- **Impact:** Scope remains supply sharing. Added invalid/stale/expiry/concurrency tests plus delayed-read focus regression; Java and focused JS checks pass, full checks/runtime proof remain in progress.

### 2026-10-06 - Prevent silent gift retargeting after recipient departure

- **Change:** Require an explicit recipient choice; a departed selection becomes empty and remains empty across polls. Pause automatic merge while verifying the UI-only correction; candidate is now 05ca1149.
- **Reason:** Final review confirmed falling back to the first remaining survivor could send a gift to someone the user did not choose.
- **Impact:** Added red/green regression and repeated committed-candidate API/browser proof, including recipient replacement and repeated refresh/Enter without a gift. All 389 final JS tests pass; Java implementation unchanged, reviewer finds no blockers. Report supersedes 2b594f75 before PR update.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2

