# Bring Survive to Final Fantasy XI parity

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Make Survive feel like a party-driven Final Fantasy XI adventure in a desktop browser. Start with one complete outing that players can see, hear and play together, then carry that standard into jobs, gathering, trade and the wider island.

## Background

The player recognizes the influence in the menus. The larger gap is the experience between menus: approaching a place with a purpose, judging a roaming enemy, fighting alongside someone, reading what happened, and returning to a settlement that feels inhabited. The supplied desktop references also set a high bar for character proportions, materials, landscapes, vegetation, masonry and water.

Survive already has a shared island and camp, persistent player progress, a calendar and map inside the game view, and an exact Check and Engage flow. A roaming animal becomes a personal encounter on claim. Its health and combat outcome are per survivor, so a second player cannot join that fight. The first fishing pass resolves one cast into a chance at food. Movement poses and wildlife routes are process-local, while progression and combat deadlines are saved. These are starting points for parity work.

## Goals

- Make one settlement-to-field outing work for two players on a shared enemy. (AC-1)
- Match the desktop reference for world, character, enemy and resource presentation through direct comparisons. (AC-2)
- Build distinct combat roles, progression and clear in-world feedback around the existing commands and chat. (AC-3)
- Connect gathering, fishing and synthesis to equipment, food and other players. (AC-4)
- Expand the first outing into a navigable world with social and regional progression. (AC-5)
- Preserve current capacity and establish browser and server performance evidence as each slice ships. (AC-6)

## Non-Goals

| Area | Scope |
|---|---|
| Asset reuse | Use original or appropriately licensed Survive assets and audio. Square Enix materials serve as references. |
| Interface replacement | Retain the menu presentation the player likes. Improve focus, control coverage and contextual actions as the game expands. |
| Historical snapshot | Classic low-level party play guides the first milestones. Choose era-sensitive formulas and later conveniences in their own child plans. |
| Capacity reduction | Keep the current capacity and gameplay scope. Use measurements to guide rendering, transport and storage changes. |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Two independent sessions accept a visible NPC assignment, take the North Gate route, Check the same roaming enemy, engage it, combine TP skills and return for one reward per eligible player. Both see the same HP, defeat and respawn. |
| AC-2 | The owner reviews matching desktop play captures of camp, gate, forest, shore and a fight against the supplied reference bar. Review covers actor silhouette and gear, enemy gait and attacks, road and bank relief, foliage, masonry and water, resource readability and sound. |
| AC-3 | A small party can demonstrate a protector, healer and damage role, with equipment and skills that change decisions. Target selection, threat changes, enemy tells, TP, skillchains, magic bursts, recovery and rewards are legible through action animation and ordered chat. |
| AC-4 | A player can target a node, use the right tool, fish using rod and bait, use the result in synthesis or cooking, and transfer a finished item safely to another player. Skill, inventory and outcomes survive reconnects. |
| AC-5 | Players can use the map to navigate between settlements and fields, take distinct optional quests and story assignments, form and communicate with a party, and resume travel and progress across sessions. |
| AC-6 | Each child has baseline and candidate evidence, native checks, isolated runtime proof before PR creation, CI and deployment readback. Fixed browser and multiplayer workloads establish frame time, memory, latency and write load without reducing current capacity. |

## Inputs

- **Direction.** The player requested desktop-scale FFXI graphics, real-time co-op, keyboard and mouse plus controller on desktop, and fullscreen with a controller on phones. Events belong in chat. The map depicts location and geography.
- **Baseline.** Reviewed the Survive feature guide on website main at `9ed8d0aae127c7e752a08c7fdbf25ba05386ce82`. The live build read back during planning was `fb78dd1ddc0228b2d48ea59d1fb14128b93c1e59`. The database-read improvement was merged by then. Its live state is tracked separately below.
- **FFXI controls and feedback.** The Windows manual covers the HUD, status, targeting, contextual menus, text commands, party formation and battle. The official control chart separates movement, camera, target cycling, lock-on, confirm/cancel and macros. [Windows manual](https://support.na.square-enix.com/document/manual/20/FFXI_manual_vc09_AE5.pdf) · [Control chart](https://www.playonline.com/ff11newplayer/tips/en/list.html)
- **Combat and jobs.** The official battle guide ties skills to weapons and TP, and ties magic bursts to coordinated actions. Developer notes explain enmity as more than a first-hit lock. The jobs guide illustrates different party roles and changing jobs. [Battle](https://www.playonline.com/ff11us/guide/system/battle.html?pageID=system) · [Enmity](https://forum.square-enix.com/ffxi/threads/30629-Enmity-System-Explanation-and-Planned-Adjustments) · [Jobs](https://www.playonline.com/ff11us/intro/about/job01.html?pageid=about) · [Level Sync](https://www.playonline.com/pcd2/topics/ff11us/detail/3599/detail.html)
- **World and economy.** The official guides distinguish quests, nation missions and regional participation. They describe travel, trade, bazaars, auction houses, synthesis and fishing. [Quests, missions and conquest](https://www.playonline.com/ff11us/guide/system/quests.html) · [Travel, crafting and trade](https://www.playonline.com/ff11eu/guide/system/other.html)
- **Art and sound.** The art director discusses how local ecology, materials and color make places distinct. Starting-area, equipment and monster galleries are shape and material references. The composer interviews describe the development of FFXI's music. Use the player's in-game examples to judge final play captures. [Art direction](https://we-are-vanadiel.finalfantasyxi.com/post/?id=569&lang=en) · [Art gallery](https://we-are-vanadiel.finalfantasyxi.com/gallery/season/?lang=en&s=11&vol=5) · [Composer interview](https://we-are-vanadiel.finalfantasyxi.com/post/?id=847&lang=en)
- **Era distinction.** The modern guide describes Trust, Records of Eminence, faster travel and the level 99 path. Track these separately from the first party milestones. [Returning Adventurer Guide](https://we-are-vanadiel.finalfantasyxi.com/post/?id=678&lang=en)

## Branch

Builder main owns this plan. Start each implementation child from verified website main in its own scoped branch.

## Assumptions

- Classic starting-area party play is the reference for the first milestones. The player has set FFXI as the quality bar and has left the exact era open.
- Survive's island, camp, hunger and raids are part of its identity. Integrate them into the party loop and use playtest evidence to tune friction.
- Keep the menus, chat, viewport HUD, real map and existing input policies as design constraints.

## Open Questions

- Which FFXI era should govern exact combat formulas and recovery rules? Resolve before locking those tables. The first shared outing can proceed independently.
- What desktop hardware and concurrent population should define launch budgets? Record the hardware, browser, workload and measured baseline in the performance child before setting thresholds.
- Which modern conveniences belong after the shared loop? Review after real players complete the classic-style outing.

## Design

The first outing is the benchmark for the rest of the game. It tests world scale, camera, interaction, movement, claim, threat, animation, chat and rewards together. Set the rule for each gameplay transition on the server. Present confirmed outcomes through the world and chat, including failure, interruptions and reconnects. Keep shared events ordered with stable identifiers so both clients can recover without replaying rewards.

| Alternative | Why not |
|---|---|
| Expand the island first | More terrain would repeat the incomplete interaction loop. |
| Add jobs and crafting before shared encounters | Job roles and the equipment economy need real cooperation to validate their purpose. |
| Replace polling or storage up front | Use the baseline to identify where the current transport or world document limits the shared loop. |

### Needs and parity ledger

Update each row with a child plan and evidence. Use planned, in progress, verified local, merged, or verified live for delivery state. Record partial behavior in the baseline column and keep a row open until its exit evidence exists.

| ID | Area | Baseline and state | Needed change and evidence to close |
|---|---|---|---|
| WORLD-01 | First outing | In progress. North Gate, crossing and waystation are playable. | Put an NPC, reason for the route and reward at specific locations. Two fresh characters can complete the round trip without external instructions. |
| UI-01 | Input and HUD | Context menus, chat, map, calendar and creature targeting exist. | Extend selection to NPCs, party members, nodes and interactables. Verify confirm, cancel, target cycling, lock-on, chat focus, party HP/MP/TP and log filters on all desktop inputs. Add configurable shortcuts and macro palettes as the command set grows. |
| COM-01 | Shared encounters | Personal health after claim. Passive hogs and aggressive wolves and bears already roam. | Give one spawn one authoritative encounter, HP and respawn. Add party claims, range and facing, species-specific detection and leash, and deterministic simultaneous actions. Verify outsider access, late join, disconnect and two clients attempting the final blow. |
| COM-02 | Tactical combat | Three-second timed exchanges and a TP skill. | Give weapons distinct cadence, enemies readable moves, and parties threat management, spell timing and recovery. Prove a compatible two-player skillchain and a correctly timed magic burst, including invalid timing and interrupted casts. |
| JOB-01 | Jobs and progression | Strength/stamina growth and a private weapon slot. | Introduce a small set of changeable roles, job XP, weapon skill, equipment slots, spells and skill eligibility. Evaluate support jobs and level sync after party roles work. |
| ART-01 | Actors and resources | Authored adventurer and wildlife, painted textures, mixed asset finish. | Review player and enemy turntables at gameplay distance, then captures in motion. Improve faces, gear layering, contact poses, creature anatomy and authored resource silhouettes, including trees, ore, shoreline and tools. |
| ART-02 | Landscape | Textured island with a clearer North Gate route. | Author distinct route grades and silhouettes, material transitions, weathered structures, foliage layers, water edges and lighting by time of day. Use same-height desktop captures with route landmarks visible. |
| ART-03 | Motion and sound | Existing action poses and world feedback need a full playthrough review. | Read locomotion, weapon draw, wind-up, impact, hit reaction and defeat at play speed. Show tool contact for logging and mining, cast/bite/reel for fishing, and readable synthesis and sleep. Add original environmental beds and distinct action cues with volume controls. |
| ECON-01 | Gathering and trade | Location-based resource commands, one-roll fishing, basic crafting and camp gifts. | Add targetable nodes, tool and skill checks, timed fishing, recipe inputs and meaningful outputs. Use direct trade first, then evaluate bazaars and auction listings with ownership and duplication checks. |
| SOC-01 | Social and travel | Shared presence and camp, process-local positions and routes. | Add party invitations and recovery, party chat, persistent travel checkpoints, region transitions and distinct mission versus quest progression. Evaluate public chat, linkshell-like groups and travel unlocks once the first route works. |
| PERF-01 | Browser and server | Render reuse is live. Version-checked movement reads are merged at baseline. | Profile long sessions and concurrent play with the same scene and action mix. Track browser memory slope and frame-time percentiles, server heap and p95 latency, DB bytes and writes, bandwidth and shared-IP behavior. Distinguish stored-character capacity from measured concurrency. |

### Child plan ledger

| Slice | State and next action |
|---|---|
| 01 · One playable party outing | In progress. Keep the existing starting-zone plan as the implementation record for the route, target selection, shared encounter and NPC assignment. [Starting-zone plan](2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md) |
| 02 · Desktop finish and feedback | Planned. Establish a fixed capture route and asset checklist. Work can proceed alongside the shared fight where it leaves encounter state untouched. |
| 03 · Party roles and progression | Planned. Extend the shared encounter after Slice 01 proves one fight and one outcome. |
| 04 · Gathering, fishing and economy | Planned. Build one complete supply chain before adding multiple guilds or market features. |
| 05 · World, travel and community | Planned. Expand outward after the first assignment and party loop work. |
| P · Performance and reliability | Ongoing across all slices. Record browser and server evidence separately. See the implementation log for baseline fixes. |

## Expected Changes

| File or area | Change |
|---|---|
| Builder implementation plans and reports | Maintain this ledger, link child plans and record published evidence and scope decisions. |
| Survive Java feature package and browser modules | Child plans own changes to shared encounters, target/action handling, NPCs, progression and persistence. |
| Survive scene, original asset library and audio | Child plans own benchmark captures, asset review, rendering cost and input playtests. |

## Task Breakdown

The umbrella tasks govern evidence and scope. Child plans contain inspected code contracts before implementation.

### Task 1 - Maintain the parity baseline and child plans

| Contract | Detail |
|---|---|
| **Dependencies** | The published starting-zone plan and verified website baseline. |
| **Files** | This plan, the starting-zone plan, the Builder implementation plan index and related test reports. |
| **Symbols** | Needs and parity ledger, Child plan ledger, Implementation Log and Outcome. |
| **Inspection** | Reviewed the existing starting-zone plan, website main feature guide and Square Enix sources linked above. |
| **Behavior** | The next slice, its dependencies, its current delivery state and the evidence needed to close it are visible here. |
| **Invariants** | Keep previous evidence and retain desktop input, chat-only events, real map and capacity constraints. |
| **Boundary/API** | Builder Markdown and links only. Each child plan owns application changes. |
| **Effects and failures** | Publish only scoped documents. Failed verification leaves a row at its last proven state. |
| **Tests and evidence** | Validate the plan, check internal links, and compare the written baseline with website main and deployment identity. |
| **Verification** | Run Builder hub validation and verify the published document on Builder main. |

### Task 2 - Record playable and performance evidence for each slice

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1. Each child establishes a baseline before its candidate changes. |
| **Files** | Child plans and their Builder test reports. The existing North Gate, targeting, render allocation and database-read reports establish the evidence pattern. |
| **Symbols** | Child acceptance criteria, outcome and evidence links. |
| **Inspection** | Reviewed the starting-zone requirements and the website feature guide for player identity, world storage, movement, combat and fishing. |
| **Behavior** | Each release links evidence for its player-visible outcome, save/reconnect behavior and measured resource cost where relevant. |
| **Invariants** | Use isolated test-profile Mongo for runtime proof and preserve account progress, shared capacity and already accepted controls. |
| **Boundary/API** | Each child documents its exact endpoints, save format and compatibility. |
| **Effects and failures** | Keep artifacts and result claims tied to the candidate. Record failed checks and recoveries in the owning child and summarize material changes here. |
| **Tests and evidence** | Native checks, committed-candidate runtime report, desktop captures or two-session evidence as appropriate, CI and live readback. |
| **Verification** | Use verify-local-app and the Test Plan below before advancing the row. |

## Test Plan

This planning change modifies Builder documents only. Application runtime proof applies to the child releases.

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Shared HP, claim, concurrency, restart, chain timing and idempotent reward tests. | Two independent browser sessions complete the outing, then repeat a disconnect and contested final strike. |
| AC-2 | Asset, renderer and control checks plus capture reproducibility. | Repeat fixed desktop views and moving combat in daylight and dusk. Save matched captures, action clips and review decisions. |
| AC-3 | Tests for threat, range, TP, spell interrupts, XP and chat order. | Play the roles together and reproduce a valid chain/burst and a mistimed attempt. |
| AC-4 | Tests for skill gates, tool requirements, inventory, trade atomicity and old saves. | Complete the gather-to-trade loop and reconnect between steps. |
| AC-5 | Tests for party membership, travel, quest transitions and access. | Take separate accounts through invitations, a route transition, a quest and a reconnect. |
| AC-6 | Run affected Gradle and browser checks and validate Builder reports. | Use a committed candidate against isolated test-profile Mongo. Compare a fixed desktop route, idle and active soak and repeatable multiplayer workload. Verify live build identity after deployment. |

## Rollback or Recovery

Keep the last proven row state and append corrections when evidence changes. Revert a failed child release through its repository workflow. A child that introduces durable state must prove old-save loading, mixed-version behavior or a reversible rollout before delivery. Keep rollback evidence with that child.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Visible co-op masks private combat | High | Require the same HP, enemy ID, result and respawn in two sessions. |
| Improved screenshots leave movement and feedback unclear | High | Require moving play captures at desktop scale, including camera, audio, animations and chat. |
| Browser or storage costs rise with richer play | High | Compare the same workload across candidates. Measure shared-IP contention and database writes alongside render and heap metrics. |
| Legacy fights or saves break during transition | Medium | Test migration, guest and account isolation, reconnect, failure recovery and mixed-version behavior in the child. |
| Era disagreements stall core work | Medium | Decide formula-sensitive choices at the point they are needed. Keep classic party outcomes explicit. |

## Implementation Log

### 2026-11-05 - Establish the parity ledger

- **Change:** Linked the existing starting-zone plan and set the two-player outing as the first gameplay milestone. Recorded separate visual, economy, world and performance exit criteria.
- **Reason:** The player asked for a living plan grounded in FFXI and Survive's current behavior.
- **Impact:** Future changes and fixes should update the relevant ledger row, link the child and its evidence, and append material deviations here.

### 2026-11-05 - Record the current gameplay and performance changes

- **Change:** The North Gate route and exact target selection shipped. Browser allocation work in #1574 reused rendering buffers and was verified live by build identity. #1575 merged the version-checked movement snapshot path. Its isolated check measured 100 indexed version checks and zero full world reads for 100 accepted pulses.
- **Reason:** The user wants a richer world with less browser and server overhead while preserving capacity.
- **Impact:** WORLD-01 and UI-01 have usable foundations. COM-01 remains open. PERF-01 still needs live readback for #1575 and representative sustained browser and multiplayer measurements. [Route report](../test-reports/2026-11-05-13-29-christopherbell-dev-survive-north-gate-route-and-camera.md) · [Targeting report](../test-reports/2026-11-05-13-45-christopherbell-dev-survive-exact-field-targets.md) · [Browser allocation report](../test-reports/2026-11-05-14-19-christopherbell-dev-survive-render-allocation.md) · [Movement database report](../test-reports/2026-11-05-14-27-christopherbell-dev-survive-movement-database-reads.md)

## Outcome

Pending.

## Project

christopherbell-dev

## Plan Format

task-contract-v2
