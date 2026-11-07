# Show nearby fighters reacting to damage

## Document Status
ready-for-review

## Objective
Show a nearby adventurer recoiling after confirmed combat damage, completing the shared fight's visible exchange.

## Background
Main 012bb295 sends weapon and strike appearance but no health. The observer renders strikes and stance while incoming hits affect only the owner's pose.

## Goals
- Show one brief recoil per observed combat health loss (AC-1).
- Preserve reduced motion and compatibility with older payloads (AC-2).

## Non-Goals
| Area | Reason |
|---|---|
| Remote enemy lunges and player collapse | Separate motion work; this slice owns the receiving player's hit reaction. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | An independent observer sees a nearby fighter recoil after damage. Duplicate updates, healing, first appearance and noncombat loss cause no recoil. |
| AC-2 | Missing health fields are safe; reduced motion suppresses recoil; strike and stance still render. |
| AC-3 | Native checks, isolated candidate Chrome proof, report, CI and live readback are recorded. |

## Inputs
- Parent: 2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md, ART-03.
- Inspected: SurvivePresence.Appearance, SurviveService.describePlayers, pulse reconciliation, renderer and motion tests on 012bb295.

## Branch
codex/survive-remote-hit-recoil from origin/main 012bb295.

## Assumptions
Movement requests are serialized. Health compares consecutive confirmed nearby appearances. Reconnect establishes a new baseline rather than replaying absent combat.

## Open Questions
None for this bounded motion slice.

## Design
Add confirmed health to nearby appearance only. Detect a decrease between the same survivor's consecutive combat appearances, retain its local receipt time and overlay a bounded torso recoil on strike or stance. Use the existing animation preference to suppress it. No persistent effect or new timer is needed.

| Alternative | Why not |
|---|---|
| Infer damage from another player's strike | Does not prove who took damage. |
| Add a durable hit-event collection | Unnecessary storage for a transient visual; long-hidden damage is not replayed. |

## Expected Changes
| Area | Change |
|---|---|
| Presence/service | Include current health in the existing nearby appearance. |
| Action poses/world/renderer | Validate health delta, retain receipt time and apply a bounded recoil. |
| Tests/docs | Server source-of-truth test, duplicate and invalid-payload cases, mounted-world wiring and Chrome observer proof. |

## Task Breakdown
### Task 1 - Confirm and render observed damage
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| Dependencies | Current main shared strikes and local recoil |
| Files | SurvivePresence.java; SurviveService.java; survive-action-pose.js; survive-world.js; survive-world-renderer.js; associated tests and READMEs |
| Symbols | Appearance.health; receivedCombatDamage; hitRecoil |
| Inspection | Main 012bb295 source and callers described above |
| Behavior | Health loss between consecutive combat appearances starts one recoil |
| Invariants | No invented damage, rewards, save writes or repeated cue on an unchanged health update |
| Boundary/API | Additive health number in appearance, old browser ignores it and new browser tolerates absence |
| Effects and failures | Existing pulse lifecycle owns transient receipt time; disconnect drops observed players |
| Tests and evidence | Observe failing regression, then passing server and browser tests; two-context Chrome runtime |
| Verification | Java movement/service tests, all JS tests, touched JS syntax, bootJar and isolated test runtime |

## Test Plan
| AC | Check |
|---|---|
| AC-1 | Source-of-truth Java test, delta edge cases, mounted-world pulse test, normal Chrome observer capture |
| AC-2 | Missing/invalid health, noncombat/heal/duplicate cases and reduced-motion Chrome check |
| AC-3 | Published report naming exact committed build; PR and production build identity |

## Rollback or Recovery
Revert the slice. No saved schema changes.

## Risks
Observed health deltas coalesce damage between polls and omit a hit offset by healing in the same interval. This presentation slice does not claim full event playback. Sustained multiplayer performance and complete shared encounter motion remain parent-plan work.

## Implementation Log

### 2026-11-07 - Verify normal and reduced motion

- **Change:** Implemented appearance health, local receipt timing and bounded remote recoil; integrated timed fishing main 125bd326.
- **Reason:** Render only a confirmed health decrease and preserve old-server and reduced-motion behavior.
- **Impact:** AC-1 and AC-2 have local evidence on 6cebcc6b. AC-3 awaits CI and production readback. [Runtime report](../test-reports/2026-11-07-12-19-christopherbell-dev-survive-remote-hit-recoil.md)

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
