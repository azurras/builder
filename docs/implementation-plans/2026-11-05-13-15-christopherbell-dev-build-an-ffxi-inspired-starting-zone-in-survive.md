# Build an FFXI-inspired starting zone in Survive

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> Give Survive a starting zone where two players can meet in a distinctive settlement, follow a route into the field, assess the same enemy, and win a fight together.

## Background

This is the first playable slice in the [living Survive FFXI parity plan](2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md). Use this child plan for implementation and test evidence, and update the parity ledger when the slice changes scope or delivery state.
The user recognizes the FFXI influence in the menus. The reference screenshots frame a human-proportioned adventurer low in the landscape. Paths, high banks, masonry, a bridge and water divide the scene into places with different uses. Survive's camera looks down on a mostly open clearing. The new actors and canopy add detail, while the landscape still feels similar in several directions.

FFXI's official controls make targeting, camera orbit, zoom, lock-on and confirm distinct actions. The manual describes approaching a target, auto-attacking with an equipped weapon and forming a party. The battle guide describes TP weapon skills and follow-ups timed by different players. Survive's current enemies reserve a private fight and disappear for others, so exploring together rarely becomes fighting together. [Controls](https://www.playonline.com/ff11newplayer/tips/en/list.html) [Manual](https://support.na.square-enix.com/document/manual/20/FFXI_manual_vc09_AE5.pdf) [Battle](https://www.playonline.com/ff11us/guide/system/battle.html?pageID=system)

FFXI's original art director describes local texture, color, weather and ecology as parts of making each area feel like a real place. The starting-area concept gallery shows individual roads, buildings and silhouettes with different purposes. [Ryosuke Aiba interview](https://we-are-vanadiel.finalfantasyxi.com/post/?id=569&lang=en) [Starting-area art](https://we-are-vanadiel.finalfantasyxi.com/gallery/season/?lang=en&s=11&vol=5)

## Goals
- Establish a visually distinct camp and field route with player-scale framing. (AC-1)
- Make selecting, assessing and engaging a target continuous in the game view. (AC-2)
- Let two players share an encounter and coordinate a finish. (AC-3)
- Give the route a reason to exist and verify a complete first outing. (AC-4)

## Non-Goals
| Area | Scope |
|---|---|
| Menu redesign | Retain the current menu presentation and chat placement. |
| Whole-game parity | One playable starting route establishes the standard for later zones and systems. |
| FFXI game assets | Use original Survive art and documented reusable assets. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Desktop captures from camp, the crossing and the field show distinct silhouettes and destinations. The low follow camera frames a textured, human-proportioned adventurer and the next landmark. |
| AC-2 | Keyboard, mouse and controller support movement, independent camera control, target cycling, Check, lock-on and Engage. The selected enemy keeps its identity as it moves and enters combat. |
| AC-3 | Two browsers see the same enemy and health pool. Both can contribute and time TP skills against one server-owned fight and one outcome. |
| AC-4 | Players take a short assignment from a visible NPC, complete the encounter and return for one reward. The committed build passes runtime proof, CI and live readback. |

## Inputs
- User's two reference screenshots and feedback that the menu style works.
- Current movement, chat, server clock and persistence inspected at gameplay candidate 80dc648ce5c5f17cee82c45bdcb9cfc08485d16d.
- [Official jobs overview](https://www.playonline.com/ff11us/intro/about/job01.html?pageid=about), [quests and missions](https://www.playonline.com/ff11us/guide/system/quests.html) and [fishing and synthesis](https://www.playonline.com/ff11eu/guide/system/other.html).

## Branch
Use codex/survive-starting-zone from the verified gameplay baseline.

## Assumptions
- The first delivery is one cohesive, desktop-first route and encounter.
- Existing request transport and the world clock can support a two-player field playtest.

## Open Questions
- Scene and texture budgets need measurement on the candidate.
- Settlement and NPC names can follow the established Survive naming.

## Design
Frame the outpost at player height. Lead through banks and an old gate, cross water beside weathered stone, then open into a field. Compose the route from several eye-level views. Make the character's planted feet, attack weight and weapon silhouette legible at the actual camera distance. Use footsteps, impacts and outdoor ambience as confirmation alongside the chat log.

Use the same target flow for enemies, people and resource nodes. Check should report useful difficulty before battle. Explicit target IDs preserve the player's intent and allow approach and weapon range to use the real scene coordinates. Keep the camera independently operable and allow the player to release lock.

Own shared health, threat, deadlines and rewards on the server. Start with one frontline and one support ability, plus a two-person TP timing window. Build the first NPC assignment around the route and award useful equipment and experience. Later jobs, synthesis, gathering and fishing can build on the same progression.

| Alternative | Tradeoff |
|---|---|
| More standalone prop replacements | A more detailed asset leaves camera, sight lines and interaction flow to separate work. |
| More solo weapons and jobs first | Jobs depend on shared encounters for meaningful party roles. |
| Several new zones together | A complete route establishes a benchmark before content expands. |

## Expected Changes
| Area | Change |
|---|---|
| Island art, camera and controller | Lower framing, distinct route, independently controlled camera, lock and zoom. |
| Java world, presence and snapshots | Shared enemy identity, authoritative timing, threat and rewards. |
| Survive interaction and progression | First NPC assignment, equipment reward, readable animation and sound. |

## Task Breakdown
### Task 1 - Frame and build the route
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | HUD and gameplay baseline. |
| **Files** | static/js/survive-world-model.js, survive-world-art.js, survive-world-renderer.js, survive-world.js and survive-controller.js. |
| **Symbols** | cameraMatrix, islandMesh, encounterPosition and controller input. |
| **Inspection** | Read the follow camera, radial terrain, tree generator and viewport input at the gameplay candidate. |
| **Behavior** | Walk from outpost to field with clear landmarks, zoom and independent orbit. |
| **Invariants** | Preserve desktop input, menus, chat and map position tracking. |
| **Boundary/API** | Display uses server-owned island coordinates. |
| **Effects and failures** | Bound geometry, preserve WebGL fallback and release camera input on disposal. |
| **Tests and evidence** | Camera projections, asset budgets and comparable desktop captures. |
| **Verification** | node --check, jsTest and an isolated desktop browser candidate. |

### Task 2 - Share the encounter
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 coordinates and target framing. |
| **Files** | SurviveWorld, SurviveService, SurviveWildlife, SurvivePresence, saved model and target commands. |
| **Symbols** | Encounter identity, action dispatch, timed combat and snapshot. |
| **Inspection** | Read per-survivor combat, creature claims, persistence and interpolation at the gameplay candidate. |
| **Behavior** | Select an exact enemy and share its health, threat and attack timeline. |
| **Invariants** | Existing saves load and duplicate requests cannot duplicate rewards. |
| **Boundary/API** | Validated target ID and additive encounter fields. |
| **Effects and failures** | One durable settlement per exchange, with stale or out-of-range actions rejected. |
| **Tests and evidence** | Shared damage, threat, skill timing, disconnect and restart. |
| **Verification** | Java and browser tests plus two isolated browser sessions. |

#### Shared fight handoff

Party membership is saved with the world. The current field claim still lives in SurviveWildlife and hides the enemy from everyone except the claimant. The current combat loop stores health and attack deadlines on each player. The next implementation slice needs to replace these two sources of truth for party fights in the same change.

- Key a party fight by its route ID and a unique fight ID. Save its claim, initial pose, shared health, participants and deadlines in the versioned world. Resolve the selected route against the server's acknowledged player position when starting or joining the fight.
- Keep claimed enemies visible with one identity. Members can Check and Engage within range. Outsiders can see the claim and Check it. The server rejects their attempts to join or attack.
- Settle due player strikes and enemy retaliation in deterministic order. Keep TP and equipment wear on the acting character. Resolve a finish and the eligible rewards in one world save. A retry, restart or simultaneous strike must read the committed outcome.
- Keep the existing text encounters and night raid on their current paths. After a party fight ends, derive release and respawn from saved state so restarting the server cannot immediately restore a defeated spawn.
- Prove shared health first with three independent sessions. Have two members land damage, reject a third player's Engage, then repeat through a disconnect and a final-strike race. Add the timed two-player skillchain and NPC objective once this proof is green.

### Task 3 - Complete the first outing
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 and 2. |
| **Files** | Survive world domain, snapshot and scene modules, feature docs and tests. |
| **Symbols** | NPC interaction, objective progress, chat, payout and audio cues. |
| **Inspection** | Read ownership, action confirmation and chat synchronization. |
| **Behavior** | Accept an assignment, fight together and return for one useful reward. |
| **Invariants** | Keep outcomes in chat and award progress once. |
| **Boundary/API** | Add assignment state to existing world and player contracts. |
| **Effects and failures** | Keep progress durable and gameplay operable with audio muted. |
| **Tests and evidence** | Repeat turn-in, reconnect, missing assets and first outing. |
| **Verification** | Native checks, runtime report, CI, merge and production readback. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Projection and geometry budget. | Compare camp, crossing and field at the same desktop viewport. |
| AC-2 | Target identity, lock and input lifecycle. | Walk, orbit, Check, Engage and disengage with keyboard, mouse and controller. |
| AC-3 | Timing, persistence and reward bounds. | Two players chain skills on the same enemy. |
| AC-4 | Assignment and save compatibility. | Run the exact committed build using verify-local-app, publish evidence and read back the release. |

## Rollback or Recovery
Release the camera independently from durable combat. Preserve additive fields in older player records and finish active encounters before rolling back combat.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Frame rate drops in dense scenes | Medium | Measure frame time and bound distant geometry and transparency. |
| Camera hides player or target | Medium | Check the camera line against authored obstacles. |
| Shared encounters duplicate results | High | Use explicit identity, durable transitions and concurrent tests. |

## Implementation Log

### 2026-11-05 - Verify the first north gate route

- **Change:** Built the initial north gate route and checked it on the committed desktop candidate 3ec810b75b5b2eb544b506e0a4957ad53c1e9ffa. It includes raised banks, a timber bridge, a waystation, and lower framing with zoom and combat camera lock.
- **Reason:** The user wanted recognizable world and movement cues before expanding MMO systems.
- **Impact:** The route, camera and map are implemented. Target identity, shared combat and the NPC assignment remain open.

### 2026-11-05 - Preserve the selected field target

- **Change:** Implemented target cycling, pointer selection, Check in chat and exact-ID Engage. The Java server refuses missing, claimed and distant targets.
- **Reason:** The previous nearest-animal flow could act on a different creature from the one in view.
- **Impact:** The target-selection part of AC-2 is implemented. Shared health, party roles, timed follow-ups and the NPC assignment remain open.

### 2026-11-05 - Verify the first party commands

- **Change:** Implemented and verified durable two-player invitation, acceptance, decline, cancellation and leave in the Party menu. The candidate uses the active survivor roster to invite and shows private state changes in chat.
- **Reason:** Shared combat needs explicit party membership to decide who can participate and earn credit. The menu gives the current desktop and text clients a common entry point.
- **Impact:** Party formation is verified locally at 3a14da91. In-world player targeting, shared HP, threat, skillchain coordination and the NPC assignment remain open. The initial BSON UUID write failure was corrected and retested. [Runtime report](../test-reports/2026-11-05-15-19-christopherbell-dev-survive-two-player-parties.md)

### 2026-11-05 - Specify the shared fight handoff

- **Change:** Added a shared fight handoff based on the current server combat and wildlife code.
- **Reason:** The existing field claim and player-owned health are separate, so a party-only health view could still allow duplicate fights or rewards.
- **Impact:** Task 2 now specifies the shared fight state, exact route validation, one durable outcome and the three-session verification order.

### 2026-11-05 - Verify party formation in production

- **Change:** PR #1576 passed CI and deployed as 074d39ca04a4cef759771b62063df1dcd9abb9c0. Production build readback matched the merge.
- **Reason:** The first shared outing needs durable membership before an encounter can grant party access and rewards.
- **Impact:** The two-player menu and private invitations are live. Shared HP, coordinated weapon skills and the NPC assignment remain open. [PR #1576](https://github.com/azurras/christopherbell.dev/pull/1576) · [Runtime report](../test-reports/2026-11-05-15-19-christopherbell-dev-survive-two-player-parties.md)

### 2026-11-05 - Verify one shared roaming encounter

- **Change:** Implemented durable party claims and shared enemy health for roaming fights. Party members can join within five metres, outsiders can see the claim, and one defeat commits the food drop and cooldown.
- **Reason:** The starting-zone outing requires a single server-owned fight before a two-player weapon skill sequence can be added.
- **Impact:** COM-01 and starting-zone AC-3 have local runtime evidence at 7913c3e8. Retaliation currently targets the attacker, and coordinated skillchains and the NPC objective remain open. [Runtime report](../test-reports/2026-11-05-21-39-christopherbell-dev-survive-shared-roaming-combat.md)

### 2026-11-05 - Verify shared roaming combat in production

- **Change:** PR #1577 passed CI and deployed as 191ca3d5c229cc1ada69f203617f3ccc0e0201ce. Production build readback matched the merge.
- **Reason:** A durable shared fight is the foundation for coordinated weapon skills and the first NPC assignment.
- **Impact:** Shared health, visible claims and one defeat with a bounded food drop are live. The starting-zone AC-3 remains open for the two-player skillchain. [PR #1577](https://github.com/azurras/christopherbell.dev/pull/1577) · [Runtime report](../test-reports/2026-11-05-21-39-christopherbell-dev-survive-shared-roaming-combat.md)

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
