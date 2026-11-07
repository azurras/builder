# Show accepted party member vitals in Survive

## Document Status
in-progress

## Objective
Give party members a glanceable HP and TP row during exploration and combat.

## Background
The Party menu shows names and invitations, while the in-world panel shows only the local survivor. An ally's remaining health and TP affect guard and skillchain decisions.

## Goals
- Show the accepted ally's confirmed HP and TP beside the local status (AC-1).
- Keep pending invitations private and clear the row when the party ends (AC-2).

## Non-Goals
| Area | Scope |
|---|---|
| MP and additional party slots | Add MP when spells introduce a real pool. The existing two-player party remains the current scope. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Two browser sessions see their ally's name, HP and TP in the viewport. A real combat round updates those numbers through the existing poll. |
| AC-2 | Pending or ended parties and old responses without vitals hide the ally row. |
| AC-3 | Native checks, exact isolated browser proof, CI and production readback are recorded. |

## Inputs
- Parent UI-01 and shared party combat. Main 99b7edfe.
- Existing party snapshot, survivor vitals pane and party fixtures.

## Branch
codex/survive-party-vitals

## Assumptions
Reuse the existing status poll. Vitals appear for accepted members regardless of pose distance while the party is current.

## Open Questions
Future MP, larger parties and targeting actions stay in the living plan.

## Design
Add a nullable partner vitals record to the requesting survivor's private party view. Render an optional second row inside the existing viewport card using text nodes. Clear it as soon as the accepted view disappears.

## Expected Changes
| Area | Change |
|---|---|
| Party snapshot | Include confirmed health, max health and TP for the accepted partner |
| Viewport | Add a compact ally row with the existing palette and responsive bounds |
| Tests | Check private invitations and live updates after a combat round |

## Task Breakdown
### Task 1 - Publish and render private ally vitals
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| Dependencies | Existing accepted-party view and snapshot poll |
| Files | SurviveParty.java, SurviveParties.java, survive.js, survive.html, survive.css and associated tests |
| Symbols | SurviveParty.MemberVitals, SurviveParties.viewFor, renderSurviveState |
| Inspection | Current party states and local vitals card on 99b7edfe |
| Behavior | Accepted partner vitals update in the viewport |
| Invariants | No vitals on invitations or public presence. Same polling cadence. |
| Boundary/API | Additive nullable party view field |
| Effects and failures | Missing or ended member clears the row and its contents |
| Tests and evidence | Party service privacy and timed round, browser renderer and two-context candidate |
| Verification | Native Java, JS, Checkstyle, exact bootJar and desktop Chrome |

## Test Plan
| AC | Check |
|---|---|
| AC-1 | Timed round in Java and two browser sessions watching the ally row |
| AC-2 | Invitation, leave and old payload regressions |
| AC-3 | Runtime report, CI and production readback |

## Rollback or Recovery
Revert the additive view and its presentation. No saved schema change.

## Risks
The row consumes viewport space. Verify it remains inside the existing card at desktop dimensions, with a readable name and no combat menu overlap.

## Implementation Log

### 2026-11-07 - Verify party HP and TP in the viewport

- **Change:** Added a private accepted-party HP and TP row to the viewport status panel.
- **Reason:** A party member's remaining HP and TP inform guard and weapon-skill timing during exploration and combat.
- **Impact:** Candidate 55edfdee verified two desktop clients, hidden invitations, an HP and TP update after a combat round and clearing both rows on leave. The existing status poll carries the values. Larger parties and MP remain open. [Runtime report](../test-reports/2026-11-07-13-39-christopherbell-dev-survive-party-vitals.md)

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
