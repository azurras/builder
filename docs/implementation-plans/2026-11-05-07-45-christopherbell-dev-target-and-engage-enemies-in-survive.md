# Target and engage enemies in Survive

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Bring Final Fantasy XI-style targeting, engagement, timed attacks and Tactical Points (TP) weapon skills to the Survive island.

## Background
Survive discovers an animal through Hunt or an ambush and requires a separate attack command for each exchange. The user selected targeting and combat first and explicitly chose to let fights continue when a player hides the tab or disconnects.

## Goals
- Select and inspect an animal and explicitly Engage. (AC-1)
- Play timed combat with meaningful TP and weapon skills while the server owns outcomes. (AC-2)
- Preserve survivor continuity and deliver the verified island. (AC-3)

## Non-Goals
| Not doing | Why |
|---|---|
| Shared enemy health, party roles and skillchains | Prioritize the individual targeting and combat loop first. |
| Jobs, spells and new maps | Existing island and weapons provide the first playable slice. |
| Target menus for camp objects and other players | A separate world-interaction slice. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | A discovered animal is selectable by pointer, touch and keyboard. Check shows its name, health and danger. Engage starts combat. |
| AC-2 | The server resolves timed attacks while the player is absent, earns bounded TP and allows an affordable weapon skill. Defend and Disengage work, and time and revision validation prevent double hits and double-spending. |
| AC-3 | Existing saves load safely, the browser shows what happened on return, and the committed candidate passes runtime proof, CI, merge and live verification. |

## Inputs
- **User decisions:** Targeting and combat first. Continue engaged fights while away.
- **Reference:** [Official FFXI controls](https://www.playonline.com/ff11newplayer/tips/en/list.html) and [official battle guide](https://www.playonline.com/ff11us/guide/system/battle.html?pageID=system).
- **Inspection:** SurviveWorld hunt/attack/settleUntil, SurvivePlayer, SurviveService revision and Mongo transaction, SurviveSnapshot/Action/SavedWorld, SchedulingConfiguration and browser command/visibility lifecycle at feedback candidate 95f6f904.

## Branch
Use codex/survive-targeted-combat-20261105 from origin/main 7b91e7697621c4480a7f52174082f6d23e97b190. Integrate feedback PR #1559 before browser work and verify the combined candidate.

## Assumptions
- One personal encounter per survivor in the first pass.
- Use the existing island, animal types, weapon categories and action route.

## Open Questions
None about product scope. Set combat tuning from deterministic tests and a playtest.

## Design
Hunt reveals an animal that can be selected in the 3D view. A target menu offers Check and Engage, with accessible equivalent buttons. Warn at Engage that combat continues while away. Existing ambushes still present a threat, and old combat saves remain readable with additive defaults.

Use a durable next-exchange timestamp and TP under the existing world lock and optimistic save. Resolve elapsed exchanges from the persisted deadline when any Survive operation next observes the world, including reconnect and another survivor observing it. A closed tab does not pause the deadline, and an idle server needs no extra Mongo scan. Capture one server instant, settle the existing clock and due fights before returning state or validating commands, and advance each deadline from its previous value. Limit each batch and retain any overdue deadline. Persist due rounds even if they invalidate a submitted revision. Reject stale commands without replay and reconcile the browser to the latest committed result. Refresh engaged views near deadlines rather than relying on the five-second exploration poll.

Start with an approximately three-second rhythm. Tune early animal health, basic damage and TP gain together so ordinary fights offer a real opportunity to use a weapon skill. Keep hunger, inventory and weapon wear under the existing rules. Defend arms protection for the next retaliation. Disengage stops timed attacks, and Flee retains its retreat cost. Report the target, fight state, TP, and damage or reward through the existing island feedback. Persist a terminal combat summary separately from the ordinary status message. Retain existing saved status and enemy invariants. A legacy encounter has no deadline and requires explicit Engage before timed damage begins. Existing guest expiry still applies.

| Alternative | Why not |
|---|---|
| Have the browser send each automatic attack | Closing the page would stop the fight against the user's explicit preference. |
| Start with shared, freely roaming enemies | Claim and aggro rules and co-op tuning would delay the selected first slice. |

## Expected Changes
| File or area | Change |
|---|---|
| Survive Java domain, service, models and focused tests | Add engagement, bounded time settlement, TP and compatibility coverage. |
| Survive browser modules, template, styles and tests | Add target selection, contextual menu, TP display and combat feedback. |
| Feature and frontend documentation | Document controls, absence behavior and verification. |

## Task Breakdown
### Task 1 - Enforce timed combat and TP on the server
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Backend files are independent of PR #1559. Refresh trusted main before branching. |
| **Files** | SurviveWorld, SurvivePlayer, SurviveService, model records and focused tests. Inspect scheduling and Mongo codec before editing. |
| **Symbols** | Encounter transitions, settleUntil, actionsFor, snapshot and durable player state. |
| **Inspection** | Existing per-player encounter and revision, clock settlement and optimistic storage boundary read at 95f6f904. |
| **Behavior** | Engage begins server-owned timed combat. TP enables a weapon skill, and disengaging cancels further rounds. |
| **Invariants** | No double hit, reward or spend. Current revision and time bound all mutations. Existing saves load. |
| **Boundary/API** | Existing survivor-owned action route and additive snapshot/save fields. |
| **Effects and failures** | Clock settlement and the command share the existing synchronized and optimistic save boundary. Commit due rounds before stale rejection, preserve CAS conflict handling, and apply no rejected command effects. |
| **Tests and evidence** | Deterministic time, cadence, offline rounds, TP spend, terminal states and old records. |
| **Verification** | Focused Survive and persistence tests, then native site checks. |

### Task 2 - Make the encounter playable in the island
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 action and snapshot contracts, plus feedback PR #1559 on main. |
| **Files** | Survive JS, feedback renderer, template, CSS, tests and README files. |
| **Symbols** | Target selection, Check/Engage, combat menu and TP gauge. |
| **Inspection** | Current projected enemy marker, revision-driven feedback, serialized requests and lifecycle hooks at 95f6f904. |
| **Behavior** | Keyboard, pointer and touch select the animal and operate its menu. Timed attacks and skills are visible. |
| **Invariants** | Server confirms outcomes. Accessible fallback remains operable. |
| **Boundary/API** | Existing action fetch path and snapshots. |
| **Effects and failures** | Stop browser refresh on disposal. Resume shows saved combat outcome. |
| **Tests and evidence** | Target selection, stale action reconciliation, visible attacks, weapon skill and reconnect. |
| **Verification** | node --check, jsTest and committed desktop and phone runtime using verify-local-app before PR. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Selection and action-availability regressions. | Select, Check and Engage on desktop and phone. |
| AC-2 | Fake-clock timing, absence, TP, revision and terminal state tests. | Observe auto-attacks, spend TP, disconnect, return to the result and test disengage. |
| AC-3 | Compatibility, duplicate commands and fallback. | Isolated Mongo test, published report, CI, merge and live readback. |

## Rollback or Recovery
Use the existing deploy path. Old code must be able to read all retained status and enemy fields. A downgrade cannot retain active timelines if the older writer replaces survivor records, so stop engaged rounds before rollback and confirm normal encounter resume behavior.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Early fights end before TP is useful | Medium | Playtest with starter weapons and tune health and cadence together. |
| A missed command races a scheduled exchange | Medium | Serialize writes, check revision, and surface the new state. |
| Offline damage surprises players | Medium | Warn on Engage, make disengage visible, and report the outcome on return. |

## Implementation Log

### 2026-11-05 - Resolve offline combat and revision boundaries

- **Change:** Reuse the durable clock settlement model for offline combat. Add explicit command race, reconciliation and rollback rules.
- **Reason:** Independent review found that a new global scheduler would complicate isolated runtime and that a five-second poll could routinely lose commands to the combat clock. Persisted deadlines resolve the same elapsed rounds at the next observation without requiring a connected player or enabling unrelated jobs.
- **Impact:** Existing combat saves require explicit engagement before timed damage. Prove an absent survivor outcome with no intervening requests. Preserve durable outcome and update the browser near the deadline.

### 2026-11-05 - Separate server work from the feedback release

- **Change:** Begin the server work on trusted main while the feedback PR runs CI. Integrate the feedback changes before browser work.
- **Reason:** The feedback diff is confined to frontend files. Server work can proceed independently without disturbing its verified candidate.
- **Impact:** Maintain separate branch and runtime evidence. Browser integration and delivery require refreshed main with PR #1559 merged.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
