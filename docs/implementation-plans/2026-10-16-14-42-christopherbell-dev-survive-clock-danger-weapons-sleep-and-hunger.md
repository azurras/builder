# Survive gains a day-night clock, raids, enemies, weapons, sleep and hunger

## Document Status
ready-for-review

## Objective
> [!IMPORTANT]
> Survive on christopherbell.dev becomes a game of real danger over time: a shared day-night clock, camp raids, ambushes and tougher enemies, stone and craftable weapons, shelter sleep and hunger, all owned by Java and live in production.

## Background
Survive today has no time, a single enemy (the hog) that appears only when a survivor chooses to hunt, no weapons and no reason to eat beyond healing. On 2026-10-16 the user asked for time, enemies to fight, weapons and building weapons, then added sleeping in shelters to regain health and a hunger level that goes down. Each design choice was settled with the user in a brainstorming conversation on 2026-10-16 (see Inputs).

## Goals
- A shared real-time clock moves every survivor through day, dusk and night, settled lazily and safely across restarts and processes. (AC-1)
- Nightfall raids threaten shared camp structures, and survivors defend by guarding at dusk. (AC-2)
- Wolves and bears join hogs, and actions outside camp can be ambushed, more often at night. (AC-3)
- Stone is a gatherable, giftable resource, and survivors craft one of three wearing weapons. (AC-4)
- Survivors sleep in shelter beds through the night to regain health, and wake early or at dawn. (AC-5)
- Hunger drains with effort, starvation hurts, and eating restores fullness and some health. (AC-6)
- The live world and saved survivors load unchanged, and the page shows every new state accessibly. (AC-7)
- The change is verified locally, merged through required CI and served by production. (AC-8)

## Non-Goals
| Not doing | Why |
|---|---|
| A background scheduler or ticker | Lazy settlement fits the single versioned world document and multiple processes; chosen with the user. |
| Harming absent survivors through hunger or ambush | The user accepted the rule that absence only risks shared structures, not people. |
| Armor, multiple weapon slots, weapon repair or trading weapons | Not requested; weapons replace on craft and break when worn out. |
| New resources beyond stone | The user chose stone only. |
| Changes to the azurras/survive Python repository | The target is the website adaptation. |
| Leaderboards, chat or day-survived scores | Not requested. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Phase and day derive from the injected clock against a fixed world epoch with a 24-minute cycle (day 14, dusk 4, night 6 minutes); snapshots expose `phase`, `day` and `secondsToNextPhase`; GET and actions settle past nightfalls and dawns at most 3 at a time and record `lastSettledNight`; settlement is idempotent across reloads. |
| AC-2 | `GUARD` is offered at dusk at camp; at each settled nightfall raid strength `3 + day/2` (capped at 20) meets the sum of guards' `1 + strength + weapon bonus`; a repelled raid rewards each guard 1 food if room else 1 XP; a lost raid destroys one structure plus one per 3 points of shortfall; guarding clears on dawn or any action outside camp; the journal records each raid. |
| AC-3 | Enemies hog (5 health, bite 1, 1 food), wolf (8, 2, 1 food) and bear (14, 3, 3 food up to room) exist; hunting keeps 61% discovery with phase-weighted species (day all hog; night 50/35/15 hog/wolf/bear; dusk hog or wolf); gathering and hunting are first ambushed at 5/12/25 percent by phase; camp actions are never ambushed; flee costs the enemy's bite; defend blocks one bite. |
| AC-4 | `GATHER_STONE` succeeds 40 percent and grants gathering XP; stone shares the 10-slot inventory; `STONE` gifts follow existing gift rules; `CRAFT_CLUB` (2 wood, +1, 8 uses), `CRAFT_AXE` (2 wood 2 stone, +2, 12 uses, wood 70 percent) and `CRAFT_SPEAR` (3 wood 3 stone, +3, 12 uses, first attack each fight takes no bite) are offered only when affordable, replace the held weapon, lose 1 durability per attack and break at 0. |
| AC-5 | `SLEEP` is offered at dusk or night at camp when beds in use are fewer than `2 x shelters`; a sleeper has status `SLEEPING` and only `WAKE`; healing is 1 per 2 slept minutes capped at 10 and full at dawn, none while starving; dawn settlement wakes every sleeper; destroyed shelters wake their sleepers with 2 damage, which can kill; `REST` remains a +2 daytime heal with a shelter. |
| AC-6 | `hunger` runs 0 to 10 from 10; each action outside camp, each combat round and each guard shift costs 1 and a night's sleep costs 2 on waking; at 0 every action costs 1 health; `EAT` gives +5 hunger and +2 health and is offered while either is below 10; the UI warns at 3 or below. |
| AC-7 | A saved world and saved survivors written before this change load with hunger 10, no stone, no weapon, hog enemies for existing combat, not sleeping and not guarding; saved-world validation enforces every new bound; the page renders phase, countdown, hunger, stone, weapon and durability, enemy name, beds and the new actions with text nodes and keyboard-operable buttons. |
| AC-8 | Native tests and semantic review pass; the committed candidate runs locally against disposable MongoDB with a published runtime report; the PR merges after required CI through the deployment queue; production `/actuator/info` serves the merge commit and `/survive` shows the clock. |

## Inputs
- **Request:** 2026-10-16: "survive needs time, enemies to fight (danger), weapons, building weapons"; then "we also need a way to sleep in the shelters to regain health"; then "We need a hunger level that goes down too".
- **User decisions (2026-10-16):** real-time shared clock; ambushes plus camp raids; stone as a new resource; lazy settlement with guards (section 1 approved); enemy roster and ambush rates (section 2 approved); stone, weapons and crafting (section 3 approved); shelter sleep with 2 beds per shelter; hunger drained by effort rather than wall time.
- **Inspected spoke:** `A:\Projects\christopherbell.dev` at `c702553d` (origin/main, clean): `survive/README.md`, `SurviveWorld`, `SurvivePlayer`, `SurviveService`, `SurviveController` symbols, `model/SurviveAction`, `SurviveSnapshot`, `SurviveSavedWorld`, `SurviveResource`, `SurviveRequests`, `DomainMongoOperationsFactory` survive kind registration, `SurviveWorldMongoCodecTest`, and `static/js/survive.js` exports.
- **History:** [original Survive plan](2026-10-05-20-15-christopherbell-dev-play-survive-with-a-java-game-engine.md), [saved account survivors](2026-10-06-12-49-christopherbell-dev-saved-account-survivors.md), [gifting](2026-10-06-00-08-christopherbell-dev-give-supplies-to-another-survivor.md); session memory 2026-10-16.

## Branch
`claude/survive-clock-danger-weapons-20261016` from origin/main `c702553d` in an isolated worktree of the christopherbell-dev spoke.

## Assumptions
- Spring Data maps a missing record component to `null` for reference types and `0` for primitives, so new saved fields must be boxed and normalized in the compact constructor; the codec test with a pre-change document proves it.
- The fixed world epoch can be a constant instant; a configured value is unnecessary because only phase alignment matters.
- Bounded settlement of at most 3 nights per load is acceptable for a world nobody visited for longer; older nights are skipped and summarized in one journal entry.
- The existing 5-second poll is precise enough for a countdown that the browser decrements locally between polls.

## Open Questions
None.

## Design
Keep the single authoritative `SurviveWorld` aggregate and the service's synchronized load, mutate and commit cycle. Add a small pure `SurviveClock` value (epoch, cycle lengths) that maps an `Instant` to phase, day and the instants of each nightfall and dawn. On every service entry point after `loadWorld()`, call `world.settle(now, rollPercent)` before any find, join, action or gift; it walks nightfalls and dawns after `lastSettledNight` in order, capped at 3 nights, resolving raids at nightfall and wakes at dawn, and commits only when it changed the world. GET still never applies a survivor command, but it may persist settlement, which is world time and not gameplay by a player; the README states this change.

Enemies become an `Enemy` enum carrying health, bite and food reward. Weapons become a `Weapon` enum carrying wood and stone cost, damage bonus, durability and perk. `SurvivePlayer` gains `stone`, `hunger`, `enemy`, `weapon`, `weaponDurability`, `guarding`, `sleptAt` and a per-fight `struckFirst` flag for the spear. `SurviveWorld.perform` first applies hunger cost and starvation damage, then the ambush roll for outside actions, then the action. New actions are `GATHER_STONE`, `CRAFT_CLUB`, `CRAFT_AXE`, `CRAFT_SPEAR`, `GUARD`, `SLEEP` and `WAKE`; `actionsFor` gates them by phase, status, supplies and beds. Status gains `SLEEPING`. Raid destruction removes boats before shelters when both exist only if boats outnumber shelters, otherwise shelters first, so beds and escape are both at stake; destroyed shelters wake the survivors assigned to them, chosen as the most recent sleepers beyond the remaining bed count.

Persistence stays one document. `SurviveSavedWorld` gains a boxed `lastSettledNight`; `SurviveSavedWorld.Player` gains boxed `stone`, `hunger`, `enemy`, `weapon`, `weaponDurability`, `guarding`, `sleptAt` and `struckFirst`, normalized from null to their defaults, with validation extended (inventory `wood + food + stone <= 10`, `enemyHealth <= enemy.health`, durability within the weapon's maximum and zero without a weapon, `SLEEPING` iff `sleptAt` is present). Existing combat without an enemy loads as a hog. The snapshot gains the fields the UI needs; credentials still never enter it. The browser keeps owning no rules: it renders new fields with text nodes, decrements the countdown locally and refetches at phase change.

| Alternative | Why not |
|---|---|
| Scheduled ticker for raids and dawn | Background writes race player commands on the version check and need leader election across processes. |
| Client-driven ticks | The browser would control the clock and could cheat. |
| Hunger drained by wall time | Starves survivors in forgotten tabs and needs presence tracking; the user chose effort. |
| Shared camp armory | The user chose personal weapons from stone. |
| Primitive new saved fields | Missing fields would load as 0, making every existing survivor starving. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/survive/SurviveClock.java` | New pure phase and day calculator with nightfall and dawn instants. |
| `website/src/main/java/dev/christopherbell/survive/model/SurviveEnemy.java`, `SurviveWeapon.java` | New enums with stats, costs and perks. |
| `website/src/main/java/dev/christopherbell/survive/model/SurviveAction.java` | Add stone, craft, guard, sleep and wake actions. |
| `website/src/main/java/dev/christopherbell/survive/model/SurviveResource.java` | Add `STONE`. |
| `website/src/main/java/dev/christopherbell/survive/model/SurviveSnapshot.java` | Add `SLEEPING`, phase, day, countdown, hunger, stone, weapon, durability, enemy and beds. |
| `website/src/main/java/dev/christopherbell/survive/model/SurviveSavedWorld.java` | Boxed new fields with defaults and extended validation. |
| `website/src/main/java/dev/christopherbell/survive/SurvivePlayer.java` | New survivor state and hunger, weapon wear and sleep helpers. |
| `website/src/main/java/dev/christopherbell/survive/SurviveWorld.java` | Settlement, raids, ambushes, enemies, crafting, sleep, hunger, stone gifts, restore and save. |
| `website/src/main/java/dev/christopherbell/survive/SurviveService.java` | Settle after every load and commit when settlement changed the world; stone gift availability. |
| `website/src/main/resources/static/js/survive.js`, `templates/survive.html`, `static/css/survive.css` | Phase banner and countdown, hunger, stone, weapon, enemy, beds, new action labels and instructions. |
| `website/src/main/java/dev/christopherbell/survive/README.md` | Mechanics, clock and settlement contract, compatibility. |
| `website/src/test/...survive/*Test.java`, `SurviveWorldMongoCodecTest`, `src/test/js/survive.test.js` | Tests for every AC, including a pre-change saved document. |

## Task Breakdown
### Task 1 - Clock, enemies, weapons and saved-state compatibility
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `survive/SurviveClock.java` (new, beside `SurvivePlayer.java`), `model/SurviveEnemy.java` and `model/SurviveWeapon.java` (new, beside `model/SurviveResource.java`), `model/SurviveSavedWorld.java`, `model/SurviveSnapshot.java`, `SurvivePlayer.java`, `SurviveWorld.java` restore and saveState. |
| **Symbols** | `SurviveClock.phaseAt`, `dayAt`, `nightfallAfter`; `SurviveEnemy`; `SurviveWeapon`; `SurviveSavedWorld`, `SurviveSavedWorld.Player`, `SurviveSnapshot.Status.SLEEPING`; `SurviveWorld.restore`, `saveState`. |
| **Inspection** | Read all listed existing files at `c702553d`; the saved-world compact constructor validates bounds and the codec registers kind `survive_world` version 1. |
| **Behavior** | Old documents restore with defaults and round-trip; new fields persist. |
| **Invariants** | One world document; credentials never in snapshots; every saved bound validated; kind version unchanged. |
| **Boundary/API** | Mongo document is additive; snapshot JSON only gains fields. |
| **Effects and failures** | Invalid saved values throw as today; no writes in this task beyond the save path. |
| **Tests and evidence** | RED then GREEN clock boundary tests and a codec test decoding a pre-change document. |
| **Verification** | `./gradlew :website:test --tests '*Survive*'` |

### Task 2 - Raids, ambushes, combat, crafting, sleep and hunger
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 for types and saved fields. |
| **Files** | `SurviveWorld.java`, `SurvivePlayer.java`, `model/SurviveAction.java`, `model/SurviveResource.java`, `SurviveWorldTest.java`. |
| **Symbols** | `SurviveWorld.settle`, `perform`, `actionsFor`, `giveSupplies`, `attack`, `flee`, `hunt`, `eat`, `rest`; new private handlers for stone, crafting, guard, sleep and wake. |
| **Inspection** | Read `perform`, `actionsFor`, `attack`, `hunt`, `flee`, `eat`, `rest` and `giveSupplies` at `c702553d`. |
| **Behavior** | Every AC-2 to AC-6 rule with injected rolls and instants. |
| **Invariants** | Dead and escaped survivors cannot act; sleepers only wake; one recorded event per settled raid, wake batch and action; arithmetic bounded. |
| **Boundary/API** | New enum constants accepted by the existing action and gift endpoints. |
| **Effects and failures** | Unavailable actions still return 400 through the service. |
| **Tests and evidence** | RED then GREEN world tests per rule, including missed-night cap and shelter destruction waking sleepers. |
| **Verification** | `./gradlew :website:test --tests '*SurviveWorldTest*'` |

### Task 3 - Service settlement, controller contract and UI
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 2 for world behavior. |
| **Files** | `SurviveService.java`, `SurviveController.java` (contract unchanged, tests extended), `static/js/survive.js`, `templates/survive.html`, `static/css/survive.css`, `README.md`, `SurviveServiceTest.java`, `SavedSurviveServiceTest.java`, `SurviveControllerTest.java`, `src/test/js/survive.test.js`. |
| **Symbols** | `SurviveService.find`, `findForOwner`, `join`, `joinForOwner`, `act`, `actForOwner`, `giveSuppliesForOwner`, `loadWorld`, `commitWorld`; `renderSurviveState`, `mountSurvive`. |
| **Inspection** | Read the service entry points and `survive.js` exports at `c702553d`. |
| **Behavior** | Every entry point settles before responding and commits settlement once; the page shows all new state and refetches at phase change. |
| **Invariants** | Storage conflicts return 409 without replay; failed saves leak no speculative state; JavaScript owns no rules; text nodes only. |
| **Boundary/API** | Same endpoints, CSRF, rate limits and status codes. |
| **Effects and failures** | Settlement on GET is persisted; a conflicting concurrent settlement yields 409 and the client reconciles with GET. |
| **Tests and evidence** | Service tests across restart and competing processes; controller tests for new actions and stone gifts; JS rendering tests. |
| **Verification** | `./gradlew :website:build` and the repository's JS test command. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | `SurviveClock` boundary tests; service settlement idempotency and 3-night cap tests | Two candidates with controlled clocks show matching phase, day and countdown; reload after a phase boundary settles once. |
| AC-2 | World raid tests for repelled, lost by margin and guard reset | Guard at dusk, cross nightfall, read journal and structures. |
| AC-3 | World tests for species weights, ambush per phase, flee and defend per enemy | Hunt and gather at night until an ambush or a wolf appears; flee cost observed. |
| AC-4 | World tests for stone, each craft, durability and perks; controller stone gift test | Gather stone, craft each weapon, attack until a weapon breaks; give stone. |
| AC-5 | World tests for beds, healing, dawn wake, early wake and raid damage to sleepers | Sleep at night, wake early, then sleep through a dawn. |
| AC-6 | World tests for each drain, starvation and eat | Act to low hunger, see the warning, eat. |
| AC-7 | Codec test with a pre-change document; saved-world validation tests; JS rendering tests | Start the candidate on a disposable Mongo seeded with a pre-change world document; old survivors resume. |
| AC-8 | `./gradlew :website:build`, Checkstyle, semantic review | verify-local-app runtime report published before the PR; production readback after merge. |

- **Regressions:** existing gathering odds, shelter and boat costs, gifts, account and guest isolation, capacity, expiry, stale revision 409 and storage-conflict tests stay green.
- **Reruns:** rerun the affected checks and the runtime cases after any runtime-affecting edit before PR creation or update.

## Rollback or Recovery
Revert the merge commit on main; the deployment pipeline serves the previous build. New saved fields are additive, so the previous build ignores them when loading; survivors keep wood, food and progress, while stone, weapons, hunger and sleep state are dropped on the next save. A sleeping survivor saved by the new build would fail old validation only if status `SLEEPING` were written, so if rolling back, first deploy nothing else and accept that the old build rejects such a document: recovery is to run the new build's wake (dawn settlement) before reverting, or revert both the code and the runtime document's `SLEEPING` statuses to `EXPLORING` through a reviewed one-off change.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Old documents load new primitives as 0 (starving survivors) | Medium | Boxed fields with null defaults and a pre-change codec test. |
| GET settlement increases write conflicts | Low | Commit only when settlement changed the world; conflicts already return 409 and clients reconcile. |
| Raids wipe camp structures and frustrate players | Medium | Cap raid strength, scale damage with shortfall, reward guards. |
| Rollback with sleeping survivors breaks old validation | Low | Documented recovery: settle dawn before revert or a reviewed status reset. |
| Snapshot growth breaks the UI tests | Low | Additive fields; JS tests updated in Task 3. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
