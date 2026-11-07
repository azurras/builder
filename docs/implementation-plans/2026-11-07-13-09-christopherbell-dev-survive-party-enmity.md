# Route shared enemy retaliation by enmity

## Document Status
ready-for-review

## Objective
Give party members a reason to manage enemy attention and defend for each other during a shared fight.

## Background
Each surviving shared strike currently makes the enemy counter the striker. Square Enix describes FFXI targeting the highest combined time-volatile and damage-volatile enmity. [Developer explanation](https://forum.square-enix.com/ffxi/threads/30629-Enmity-System-Explanation-and-Planned-Adjustments)

## Goals
- Track durable and fading damage enmity for each participant (AC-1).
- Route retaliation and guard consumption to the leading living fighter (AC-2).

## Non-Goals
| Area | Scope |
|---|---|
| Full jobs and encounter scheduler | Provoke, healing threat and independent monster attack rounds remain separate parent-plan slices. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Damage builds both components, the temporary part fades, taking damage reduces the durable part, and saved fights restore scores. |
| AC-2 | Another attacker can act without taking the next bite. The chosen fighter can guard, both players get correct chat, and defeated or departed fighters lose their entries. |
| AC-3 | Native tests, exact isolated shared-fight runtime, CI and deployment evidence are recorded. |

## Inputs
- Parent COM-02 and JOB-01. Main e5d948e2.
- Existing SurviveFieldFight persistence, timed counter and chat.

## Branch
Initial implementation is codex/survive-party-enmity. The release candidate is codex/survive-party-enmity-stack, based on the confirmed local strike ownership branch and main 99b7edfe.

## Assumptions
Initial Survive weights are 1,000 durable and 3,000 fading points per damage. Fading threat loses one point per millisecond. A received HP removes 1,000 durable points. Ties favor the earlier participant in the fight. A finisher has no retaliation.

## Open Questions
Exact job ability tuning and movement-dependent enemy attacks are outside this first shared target change.

## Design
Store the scores and last sample time on the shared fight. Add effective damage before selecting the counter target. Evaluate decay at the strike timestamp so catch-up uses the original timeline. Consume the selected fighter's guard and record incoming damage for that player. Persist changes with the existing world replacement.

## Expected Changes
| Area | Change |
|---|---|
| Shared fight model | Bounded score map with a legacy empty default |
| World | Select recipient by enmity and record truthful combat messages |
| Tests | Round trip, decay, guard, target change and legacy saves |

## Task Breakdown
### Task 1 - Persist and use shared enmity
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| Dependencies | Shared field combat and current Mongo world codec |
| Files | SurviveEnmity.java, SurviveFieldFight.java, SurviveWorld.java, SurviveWorldTest.java, SurviveWorldMongoCodecTest.java and feature README |
| Symbols | SurviveEnmity, SurviveFieldFight.enmity, strikeFieldEnemy |
| Inspection | Existing shared fight progress, counter handling, guard and native codec tests |
| Behavior | The highest living threat receives the next surviving exchange |
| Invariants | Scores belong to current participants and clear on defeat or leaving |
| Boundary/API | Additive field on the saved encounter with empty legacy default |
| Effects and failures | The selected fighter receives the damage and chat revision in the same committed save |
| Tests and evidence | Unit tests for threat transitions and shared routing, codec round trip, isolated party proof |
| Verification | Native Survive and codec tests, Checkstyle and isolated candidate |

## Test Plan
| AC | Check |
|---|---|
| AC-1 | Scoring tests and old/new saved encounter codec cases |
| AC-2 | Party hit, guard and target change tests, then shared playtest |
| AC-3 | Exact runtime report, CI and production readback |

## Rollback or Recovery
Revert the shared targeting change and leave existing saved score fields unused.

## Risks
Retaliation still occurs per surviving strike. Concentrated damage changes party balance and needs direct playtesting.

## Implementation Log

### 2026-11-07 - Use confirmed strike ownership for the defender

- **Change:** Stack the release candidate on confirmed local strike ownership from PR #1596 and extend its mounted regression to include a consumed guard.
- **Reason:** Receiving a counter advances a defender's revision while shared enemy HP drops. The old renderer inferred an outgoing attack from those changes.
- **Impact:** The combined mounted test sees the enemy's counter cue and no invented defender strike. Enmity release depends on strike ownership. The current stack also includes the merged movement quota fix. [Strike ownership PR](https://github.com/azurras/christopherbell.dev/pull/1596)

### 2026-11-07 - Verify the stacked shared fight

- **Change:** Shared field fights now store lasting and fading damage enmity and counter the living fighter with the highest combined score. Receiving damage reduces the lasting part, and a defender can guard against an ally-triggered counter.
- **Reason:** Party roles need durable enemy attention and truthful combat feedback. The child uses initial Survive weights for the two-component design described by Square Enix.
- **Impact:** The stacked candidate 453f361c passed two-player state proof, including a consumed guard, shared HP and no new defender strike. It depends on the local strike ownership fix. Independent enemy timing, Provoke, healing threat and visual facing remain open. [Child plan](2026-11-07-13-09-christopherbell-dev-survive-party-enmity.md) · [Runtime report](../test-reports/2026-11-07-13-21-christopherbell-dev-survive-shared-party-enmity.md)

### 2026-11-07 - Verify enmity after strike ownership merged

- **Change:** Integrated the enmity candidate after the strike ownership fix merged to main.
- **Reason:** Both sides of the shared counter need to retain correct strike ownership and health after integration.
- **Impact:** Candidate cba4a7ac repeated the two-player bear proof with correct guard consumption and matching enemy health. CI and production are pending. [Runtime report](../test-reports/2026-11-07-13-21-christopherbell-dev-survive-shared-party-enmity.md)

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
