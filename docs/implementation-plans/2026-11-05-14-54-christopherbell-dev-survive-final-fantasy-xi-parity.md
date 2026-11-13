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
| COM-01 | Shared encounters | Two-player parties share roaming enemy health, claim and respawn. This slice is live in [#1577](https://github.com/azurras/christopherbell.dev/pull/1577). | Extend range and facing, species-specific detection, chase and leash. Verify full retreat and contested finishing blows across the complete outing. |
| COM-02 | Tactical combat | Shared TP skillchains and confirmed strike playback exist. Distinct weapon delays are verified locally in #1595; release pending. | Give weapons distinct cadence, enemies readable moves, and parties threat management, spell timing and recovery. Prove a compatible two-player skillchain and a correctly timed magic burst, including invalid timing and interrupted casts. |
| JOB-01 | Jobs and progression | Strength/stamina growth and a private weapon slot. | Introduce a small set of changeable roles, job XP, weapon skill, equipment slots, spells and skill eligibility. Evaluate support jobs and level sync after party roles work. |
| ART-01 | Actors and resources | Authored adventurer and wildlife, painted textures, mixed asset finish. | Review player and enemy turntables at gameplay distance, then captures in motion. Improve faces, gear layering, contact poses, creature anatomy and authored resource silhouettes, including trees, ore, shoreline and tools. |
| ART-02 | Landscape | Textured island with a clearer North Gate route. | Author distinct route grades and silhouettes, material transitions, weathered structures, foliage layers, water edges and lighting by time of day. Use same-height desktop captures with route landmarks visible. |
| ART-03 | Motion and sound | Engaged stance, confirmed shared strikes and local hit recoil are live. Defeat motion (#1591) and local strike ownership (#1596) are live. | Read locomotion, weapon draw, wind-up, impact, hit reaction and defeat at play speed. Show tool contact for logging and mining, cast/bite/reel for fishing, and readable synthesis and sleep. Add original environmental beds and distinct action cues with volume controls. |
| ECON-01 | Gathering and trade | Location-based resource commands, basic crafting and camp gifts are live. Timed cast, bite, reel and expiry are live in #1592; rod/bait inventory and named fish remain missing. | Add targetable nodes, tool and skill checks, timed fishing, recipe inputs and meaningful outputs. Use direct trade first, then evaluate bazaars and auction listings with ownership and duplication checks. |
| SOC-01 | Social and travel | Shared presence and camp, process-local positions and routes. Two-player party commands verified live in [#1576](https://github.com/azurras/christopherbell.dev/pull/1576). | Extend party formation to field targeting, add party chat and recovery, then add persistent travel checkpoints, region transitions and distinct mission versus quest progression. |
| PERF-01 | Browser and server | Render reuse and version-checked movement reads are verified live. Nearby-pose filtering is live in #1593. | Profile long sessions and concurrent play with the same scene and action mix. Track browser memory slope and frame-time percentiles, server heap and p95 latency, DB bytes and writes, bandwidth and shared-IP behavior. Distinguish stored-character capacity from measured concurrency. |

### Child plan ledger

| Slice | State and next action |
|---|---|
| 01 · One playable party outing | In progress. Keep the existing starting-zone plan as the implementation record for the route, target selection, shared encounter and NPC assignment. [Starting-zone plan](2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md) |
| 02 · Desktop finish and feedback | In progress. Fixed review route is defined below; stance, strike and recoil work is live. Defeat, local strike ownership and bank artwork have current-main candidate proof. Actor and landscape parity, complete action motion and audio remain open. |
| 03 · Party roles and progression | In progress. Shared skillchains are playable and distinct weapon cadence has candidate proof. Protector/healer roles, enmity, spell timing, magic bursts and recovery remain open. |
| 04 · Gathering, fishing and economy | In progress. Timed fishing has candidate proof. Complete rod/bait, named catch, cooking or synthesis and safe item transfer before calling the first supply chain complete. |
| 05 · World, travel and community | Planned. Expand outward after the first assignment and party loop work. |
| P · Performance and reliability | Ongoing across all slices. Record browser and server evidence separately. See the implementation log for baseline fixes. |

### First outing playbook

These are proposed Survive rules for the first outing and follow-up slices. FFXI supplies the interaction reference. The child plan will record tuning values and how the rules apply to older saves.

| Step | First playable outing | Evidence |
|---|---|---|
| 1 · Meet at camp | Target another player, invite from Commands and accept or decline through the party menu. Put the invitation and membership changes in chat. Keep a compact party status display in the game view. | Keyboard and controller can form the same party. A stale invite cannot join a new party or the wrong character. |
| 2 · Take an assignment | Confirm on the waystation NPC to speak. Give each player their own assignment state and use a named landmark on the map. Make acceptance and completion readable in chat. | Either player can reread the objective, find the route from the map and return to the same NPC. |
| 3 · Check and pull | Check explains relative danger. The field has a passive creature and a threatening patrol. Free, party-claimed and other-party targets stay visible and have a readable label or marker alongside any color cue. Use existing movement and Engage for the first pull. | Both players can avoid an aggressive patrol, or choose one and bring it into a clear area. A third session can identify the claim and cannot take the final blow. |
| 4 · Fight together | Party members attack one enemy with one health pool. A second player's compatible TP skill within the timing window completes the chain. Chat shows the sequence and the field shows the hit and chain effect. | Both clients agree on enemy identity, HP, chain outcome and defeat. Repeat with a late closer and with one client hidden. |
| 5 · Recover or retreat | Disengage stops that player's auto-attacks. Remaining participants keep fighting. Define how a chase ends and when the enemy resets after the last participant leaves. The follow-up roles slice adds field healing with a visible recovery pose and interruption by movement or damage. | With one player disengaged, the other can finish. If everyone retreats, the enemy returns to its route and the encounter yields no reward. |
| 6 · Award and return | Record fight credit separately from NPC turn-in. Use the same defeat for all eligible players and issue each assignment reward once. Report inventory limits or a missed credit in chat. | Simultaneous finishing attacks, repeated turn-in and a reconnect after a confirmed result yield one defeat and one reward per eligible character. |

The Windows manual documents contextual Confirm actions, party invites through the log, distinct target colors, Call for Help, and healing that stops when the player moves or takes a hit. The official battle guide describes coordinated weapon skills and magic bursts. These are the references for the interactions above. [Windows manual, printed pp. 20–27](https://support.na.square-enix.com/document/manual/20/FFXI_manual_vc09_AE5.pdf) · [Official battle guide](https://www.playonline.com/ff11us/guide/system/battle.html?pageID=system)

### Follow-up decisions to keep visible

| Decision | Where it belongs |
|---|---|
| Party discovery, leader transfer, chat filters and support for up to six players | SOC-01. Two players prove the first outing. Test a full party before calling party controls complete. |
| Ranged pulls, social aggro, threat from damage and healing, and Call for Help | COM-02. Document enemy-family behavior and what opening a claim does to fight credit before enabling outside attacks. |
| Knockout, return point, Raise-style assistance and recovery costs | JOB-01 and COM-02. Survive currently has terminal death. Decide how MMO knockout applies to existing characters and survival rules before changing that behavior. |
| XP eligibility, drop distribution and lot/pass for rare party loot | JOB-01 and ECON-01. Keep assignment rewards separate and settle distance, disconnect, full inventory and tie cases before introducing contested loot. |

### Desktop art and animation review

Use the supplied adventurer and waterway screenshots as the quality reference. The first pass prioritizes the player and enemies because the player called them out after the world improved. Review the rest of the island along the same route so new art and existing resources hold up together. FFXI art director Ryosuke Aiba describes painted shading, visible equipment and region-specific colors and textures. Use those principles to guide original Survive assets. [Art director interview](https://we-are-vanadiel.finalfantasyxi.com/post/?id=569&lang=en) · [Starting-area and character art galleries](https://we-are-vanadiel.finalfantasyxi.com/gallery/season/?lang=en&s=11&vol=5)

| Review stop | What has to read during play | Evidence |
|---|---|---|
| Camp spawn and road | The adventurer has believable proportions, distinct layered gear and a grounded shadow. Hair, clothing, leather and metal read as different materials. Feet plant on the road and sloped banks during idle, walking and turns. | Rear and three-quarter views at default follow distance, then one clip walking uphill, turning and stopping. Include a remote player in the same frame. |
| North Gate, bridge and waystation | Paths lead the eye from one landmark to the next. Banks have readable relief and the bridge, stonework and water meet at believable edges. The route and NPC are readable at dusk. | Repeat the same approach at daylight and dusk. Walk across the bridge and turn the camera past the gate to check clipping and abrupt texture or lighting changes. |
| Woodland and hunting route | Hog, wolf and bear have distinct proportions, gaits and attack tells at the distance where the player decides to approach or avoid them. A raider reads as armed and hostile during the night approach. | Capture patrol, alert, attack and defeat from the player's camera. Repeat one attack with two players and compare the animation, health change and chat order. |
| Forest, quarry and fishing bank | Mature trees, harvestable trunks, mineral faces and the fishable bank have clear shapes and surfaces. The axe or pick makes contact with the selected resource. The line, bite and reel are readable during fishing. | Record one success and one interrupted or rejected attempt for each action the child changes. Confirm the animation and chat distinguish a completed action from a failed one. |
| Camp work and rest | Crafting shows a tool or material being worked. Sleep and wake have clear poses at the shelter. Action, result and recovery stay readable without adding notification windows. | Capture a short sequence for each action as it becomes available, including the matching chat line. |

For each stop, save a before and after capture from the same position, camera heading, zoom, resolution and lighting on named builds. Use the normal HUD and chat view for acceptance. Review close-ups separately when diagnosing defects. Record each failed check with a clip or frame and the asset or action responsible, then repeat it on the fix. An improved still frame leaves the motion check open until the clip passes.

The November 6 desktop review found three visible gaps on the starting route. The site framing took nearly half the browser height before the world began. The adventurer's large head and short lower legs weakened the silhouette, and the keeper read as another copy of the player. The camp props and waystation had simple shapes and the ground had little variation beyond the path. Address the framing separately, then use the camp-to-keeper stretch for a single art pass that pairs an improved adventurer rig and distinct keeper with a stronger building silhouette and denser vegetation at the route edges. Compare those changes in motion at the default camera distance before extending the pass across the island.

Run the same route once for visual capture and again for timing with capture overhead removed. Compare frame time, memory over repeated loops and initial asset transfer on the same desktop and browser. Exercise both solo and two-player views. Record any budget change and its measured cost in the performance row. Favor painted materials, reusable rigs and shared scenery when they pass the play-distance checks.

### First gathering, fishing and trade loop

Survive currently awards generic supplies through location commands, turns a successful cast into food, and supports camp gifts. The first economy slice should give a small set of items a reason to exist. FFXI documents rod and bait, fishing skill, crystal synthesis and direct trade. Its 2014 fishing update is a separate reference for readable input cues and fish resistance. The proposed Survive loop below uses those ideas and keeps hunger as the reason to prepare a meal. [FFXI Windows manual](https://support.na.square-enix.com/document/manual/20/FFXI_manual_vc09_AE5.pdf) · [Synthesis and trade](https://www.playonline.com/ff11eu/guide/system/other.html) · [2014 fishing update](https://forum.square-enix.com/ffxi/threads/40665-dev1191-Fishing-System-Renovation?mode=hybrid)

| Step | Proposed first loop | What to verify |
|---|---|---|
| Get equipped | Offer a starter rod, bait and hatchet through an existing camp or waystation interaction. Show what is equipped and how much bait remains in the existing menus. | A fresh character can reach the first catch without a market purchase. Missing tools and bait produce clear chat messages without spending supplies. |
| Gather at a visible node | Target a marked deadwood trunk at the forest edge and select Gather. Show the axe strike at the trunk, then put the material and result in chat. Use the same interaction for ore in a follow-up. | A player out of reach cannot gather. Two players reaching the same node observe one consistent availability state. A retry cannot repeat a grant. |
| Land a fish | Cast at the fishing bank, wait for the bite, respond to a readable rod cue and reel. Use the same actions on keyboard and controller. Rod, bait and fishing skill affect what can be landed. Keep bites and actions timed independently of rendering speed. | A successful reel lands a named fish once. An expired bite, interrupted cast or disconnected session settles without awarding a phantom catch. The child documents when bait is spent. |
| Make something useful | Use the fish and gathered fuel at the camp cooking spot for a portable meal that restores fullness. Show the inputs and output before confirming. Follow this with a simple tool or gear recipe once the first recipe works. | Verify input consumption and output together. If the pack cannot hold the result after consumption, preserve the inputs and explain the refusal in chat. Eating the meal updates fullness once. |
| Trade the meal | Target a nearby player, open Trade and show both offers. Each player confirms the same offer. Any edit clears both confirmations. Keep existing camp gifts available for their current purpose. | The meal can change hands in two browser sessions. A changed offer, full pack, departure or replay cannot produce a partial transfer or duplicate item. |

Start with one wood resource, one fish and one meal. Add skill growth that can be felt in repeat outings before expanding fish tables, tool tiers, synthesis ingredients, guilds or market listings. Keep fishing skill separate from cooking skill. Decide how early synthesis will introduce crystal-like catalysts when the first equipment recipe has a clear use. Treat loss on failure, yield bonuses and shared-node respawn timing as tuning decisions to measure in the child plan.

Keep the first loop within the existing island and inventory capacity. Define old-save defaults and behavior for the text fallback before implementation. Put action cues on the character, tool or target and confirmed results in chat. Record the browser and server cost of the timed fishing flow alongside the two-player trade checks.

### First job progression and party fight

Build this slice after the two-player outing proves shared combat. Start with three jobs on the same character, using the role names below as working labels. FFXI's jobs guide distinguishes protection, recovery and offensive magic. Its battle guide ties job abilities to level, weapon skills to the equipped weapon and magic bursts to coordinated timing. The fight and progression rules below are proposed for Survive. [FFXI jobs](https://www.playonline.com/ff11us/intro/about/job01.html?pageid=about) · [FFXI battle](https://www.playonline.com/ff11us/guide/system/battle.html?pageID=system)

| Role | First decisions | What to verify |
|---|---|---|
| Protector | Engage with a melee weapon, use a threat ability to regain attention, and guard against a telegraphed heavy attack. Open a skillchain when the other melee weapon is ready. | Damage or healing can pull attention away. The protector can regain it, and the enemy's target is readable in the world and chat. |
| Healer | Select an ally, spend MP on a heal with a cast time, and decide whether to heal now or wait through a dangerous enemy wind-up. | The intended ally receives the heal. Invalid targets and interrupted casts settle with a clear reason and consistent resource costs. |
| Damage dealer | Use melee attacks to build TP, close a compatible skillchain, then time an elemental cast to land during the burst window. | An early or late cast still resolves according to its normal spell rules. A matching spell that lands in the window adds one burst. |

Teach the sequence on a tougher roaming enemy near the existing route. Its wind-up and target changes should be visible from the default camera. Keep a passive encounter nearby for solo practice. Give the first coordinated fight enough time to use each role and repeat it with a deliberately mistimed chain or burst. Server deadlines determine the result, while animation, sound and ordered chat explain it. Preserve the existing policy that an engaged fight can continue when a browser is hidden or disconnected.

Use a camp job menu to change jobs outside combat. Keep job level and XP per job on the same character. Track weapon skill separately from job XP and decide how job and weapon proficiency limit available techniques. The first unlock should introduce a visible tactical choice, such as an alternate weapon skill that changes which chain the party can make. Show why a job, spell, ability or piece of gear is unavailable before the player commits. Test returning to a previously trained job after reconnecting, and specify old-save defaults for existing equipment and progression in the implementation plan.

Keep the first reward rules small. Define who earns job XP and weapon skill credit and when each is settled. Test a nearby contributor, a distant party member, and a reconnect after defeat. Capture health, MP, TP and the combat log in three independent sessions. Support jobs, Level Sync, additional spell families, and knockout penalties stay separate decisions. Choose exact threat values, cast and chain timings, and progression rates in the child plan after establishing a repeatable fight.

### First trip beyond North Gate

Expand after the first party outing works. Use one neighboring field and one inhabited stop, with the existing waystation as the departure point. FFXI distinguishes personal requests from assignments given by a nation. Survive can use that distinction at island scale with one camp story assignment and one optional request from a resident. The route and content below are proposals. [FFXI quests, missions and conquest](https://www.playonline.com/ff11us/guide/system/quests.html) · [FFXI transportation](https://www.playonline.com/ff11eu/guide/system/other.html)

| Step | Proposed experience | What to verify |
|---|---|---|
| Leave the waystation | A visible camp representative sends the party to deliver a message to the next settlement. The road, signs and map show where it goes. Open the map to check position, crossings and named landmarks. | Fresh players can find the road and the destination from the map and scenery. Opening, inspecting or closing the map leaves the character in place. |
| Cross into the next field | Each player walks across a marked boundary and arrives on the connected road. Show the area name in chat. Party membership and party chat span the boundary. | One player can cross first, send a party message and wait for the other. Repeat with a failed area load and a reconnect during the crossing. Each character resumes at one valid side. |
| Discover the settlement | Give the field a different approach, skyline and enemy mix from camp. A named resident at the stop offers an optional request, such as repairing a trail sign. The story contact advances the camp assignment independently. | One player can complete the story step while the other takes the optional request. Neither receives credit for the other's turn-in. Shared objectives award credit according to their own rules. |
| Register a return point | Interact with a visible landmark at the settlement to register a saved checkpoint. Use it to resume travel on a later sign-in. Put the registration and arrival results in chat. | After crossing, claiming the checkpoint and signing back in, each player returns to the correct region with their quest state and inventory. An older save with no checkpoint still starts at camp. |
| Walk back together | Keep the return route open. Party chat can help players regroup after splitting up. Existing map and input rules apply in both areas. | Rejoin on the correct side of the boundary, return to the waystation, and finish the story assignment once even if a turn-in is retried. |

The child plan owns when an area crossing commits, how an active encounter affects crossing, and how returning players are placed if their previous checkpoint becomes unavailable. Keep the committed region, checkpoint and quest state consistent across failed saves and reconnects. Preserve party chat privacy and verify that a nonmember receives none of the party's messages. Exercise the boundary on keyboard and mouse and on controller. Compare asset loading, memory and movement latency on repeat crossings before expanding the map again.

Later slices can add travel unlocks, ferry routes, more story ranks and regional participation after this round trip is proven. Keep story assignments and optional requests discoverable through NPCs and the existing menus. Record updates and outcomes in chat.

### Performance and capacity playbook

Use the published desktop route and first party outing as repeatable workloads. Compare the current shipped build with the committed candidate against separate disposable test databases seeded with equivalent saves. Record browser, hardware, viewport, graphics settings, server resources, network conditions and workload duration. Keep scene quality, movement cadence and player limits fixed for the comparison. Run load only against an isolated local candidate and baseline.

| Workload | What to measure | What the run must demonstrate |
|---|---|---|
| Cold start and warm return | Asset bytes and requests, time until movement and Commands work, browser process memory after entry. | Separate cold-cache from warm-cache results. Report the cost of new models, textures and audio alongside time to play. |
| Desktop route and soak | Frame-time p50, p95 and p99, browser process memory and JS heap. Start with a five-minute warm-up and 30 minutes of repeated camp, gate and woodland movement. | Compare the warmed baseline, peak and final memory plus the trend across loops. Run with recording off and repeat idle, active and hidden-to-visible cases separately. |
| Two players in one encounter | Time from input to accepted command and visible result, state payload bytes, movement acceptance and combat event order. | Compare the same workload on both builds. Once shared combat exists, verify agreement on health, skillchain and reward while one player reconnects. Record current private encounters as their own baseline. |
| Increasing concurrency | Successful actions, movement p95 latency, errors, conflicts and throttles, process CPU, heap and GC, Mongo reads, writes and response bytes. | Step through 2, 5, 10 and 20 simulated sessions as exploratory test points. Keep the action mix and sampling window fixed. Report offered and accepted rates and the first bottleneck. |
| Shared-network and reconnect burst | Per-IP rate-limit responses, retries, traffic, time until movement resumes and correctness of recovered state. | Run shared-IP and distributed-IP cases separately with normal limits enabled. Verify reconnects and conflicting requests preserve saved progress and never repeat a reward. |

Record client and server costs separately. Use a real desktop browser for frame and memory checks, and lightweight sessions for server load. Compare the same workload at least three times before classifying a difference that overlaps run-to-run variation. Include failed requests and timeouts when reporting throughput and errors. The workload counts above are measurement points. The cap of 1,000 saved characters remains distinct from the supported number of simultaneous players.

The first profiling child sets measurable budgets from the baseline and records the acceptance thresholds before optimization. Investigate misses using the traces for the affected path. If a richer scene exceeds its budget, profile allocation, draw work and asset transfer. If movement or combat exceeds its budget, profile request volume, world restoration, conflicts and database writes. Re-run the same case after each fix and keep its evidence with the affected ledger row.

### Inventory and equipment parity

The first equipment pass makes the Main slot interactive. Players can keep a crafted spare, inspect its damage and durability, and equip or remove it without losing the previous weapon. Keep the existing Items and Equipment windows and return command results through chat. FFXI's manual describes sortable carried items and a slot-first Equipment window that filters candidates and shows their stats and requirements. [FFXI Windows manual, printed pp. 24–25](https://support.na.square-enix.com/document/manual/20/FFXI_manual_vc09_AE5.pdf)

| Slice | Player-facing result | Evidence |
|---|---|---|
| Main slot and spare weapons | Crafting into an occupied Main slot places the new weapon in the pack. Select Main to see owned weapons with damage and condition. Equip swaps with the packed weapon and Remove stows the equipped weapon if there is room. | Keep two different weapons, switch between them, confirm damage and skill names, reconnect and verify exact condition. Reject a stale item ID and a full-pack removal. |
| Item list | Show named rows, quantities, descriptions and usable actions. Add sorting while preserving selection, and use separate item records for fish, food and crafting materials. | Verify stable focus on keyboard and controller, item use, stack limits and preserved quantities from old saves. |
| Armor, tools and accessories | Add slots with real items and compatible choices as crafting and jobs provide them. Show requirements and stat differences before confirm. Worn gear should appear on the character when the asset exists. | Equip a useful armor piece and field tool, reject an incompatible item, and verify the difference in play. |
| Storage and loadouts | Add camp storage and equipment sets once the gear catalog justifies them. | Move items between containers, preserve ownership on retries and reconnects, and recover an incomplete loadout cleanly. |

Keep current resource counts and the active weapon on old saves. The first pass keeps the ten-unit carrying limit and existing durability. Packed weapons take one unit each, and the equipped weapon remains outside that count. Decide stack sizes, job requirements and a durability policy when the item catalog and job progression are ready.

### How to record changes and fixes

Give each newly discovered need a ledger ID or attach it to the closest existing row. For a fix, record the player-visible symptom, the reproduction, the owning child plan and the check that proves recovery. Record what changed in the child and append a dated entry here when it changes scope, an acceptance check or the delivery state. Link the evidence before marking a row verified local or verified live.

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
| AC-1 | Invitation lifecycle, shared HP, claim, concurrency, restart, chain timing and idempotent reward tests. | Two independent browser sessions complete the outing, then repeat a disconnect, contested final strike and full retreat. Use a third session to verify claim visibility and outsider access. |
| AC-2 | Asset, renderer and control checks plus capture reproducibility. | Run the desktop art and animation review stops. Save matched captures, solo and co-op clips, and review decisions. Compare route timing separately from recording. |
| AC-3 | Tests for threat changes, targeting, spell interrupts, chain and burst timing, XP eligibility, job switching and old saves. | Run the three-role fight in independent sessions. Repeat a threat handoff, interrupted heal and mistimed burst, then switch jobs at camp and verify progression after reconnecting. |
| AC-4 | Tests for tools, node contention, catch expiry, recipe consumption and output, trade offer revisions and atomicity, and old saves. | Gather fuel, land a fish, cook and trade the meal in two sessions. Repeat an interrupted cast, full inventory, changed offer and reconnect before collecting results. |
| AC-5 | Tests for party membership and chat access, region crossing, checkpoint recovery, independent quest transitions and replayed turn-in. | Take two accounts on the first trip beyond North Gate. Split at the boundary, regroup, complete different objectives, reconnect and return. Repeat a failed crossing and verify party chat isolation with a third account. |
| AC-6 | Run affected Gradle and browser checks and validate Builder reports. | Run the performance playbook on baseline and committed candidate builds against isolated test-profile Mongo. Record latency, errors, memory, frame times and database cost. Verify live build identity after deployment. |

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

### 2026-11-05 - Specify the first party outing

- **Change:** Added the first-outing playbook, follow-up combat decisions and instructions for recording needs and fixes. Added third-player claim and full-retreat checks.
- **Reason:** The first shared fight needs player-visible rules for forming a party, reading claims, disengaging and collecting credit.
- **Impact:** AC-1 keeps the same delivery boundary and gains concrete checks. Later role and economy slices own knockout, field healing and contested loot.

### 2026-11-05 - Define the desktop visual review route

- **Change:** Added the desktop art and animation review route, with the adventurer and enemies first, and matched captures for scenery, resources and action feedback.
- **Reason:** The player reported that the world improved while the character and enemies still fell short of the FFXI benchmark. The art pass also needs to preserve desktop performance.
- **Impact:** ART-01 through ART-03 now share an observable AC-2 review route. PERF-01 compares the same route in separate timing runs.

### 2026-11-05 - Specify the first gathering and trade loop

- **Change:** Added a first economy loop from camp equipment through a visible gathering node, timed fishing, cooking and two-player trade.
- **Reason:** The current generic supplies and single-roll catch do not yet connect field actions to the camp or other players in the way the parity plan requires.
- **Impact:** ECON-01 and AC-4 now have a concrete first playthrough and failure checks. Exact fishing timing, skill curves and synthesis catalysts remain child-plan decisions.

### 2026-11-05 - Specify the first jobs and party fight

- **Change:** Added a three-role fight and the first job progression rules, with distinct checks for threat, healing, skillchain timing and a magic burst.
- **Reason:** Party roles need to change what players do together, and job progression needs to unlock a choice players can demonstrate.
- **Impact:** JOB-01 and COM-02 now share a concrete AC-3 playtest. The child plan owns balance values, gear compatibility and old-save defaults.

### 2026-11-05 - Specify the first trip beyond North Gate

- **Change:** Added a first trip beyond North Gate covering map navigation, region crossing, party chat, optional requests, a story assignment and saved checkpoints.
- **Reason:** The first expansion needs to show how a party explores an inhabited world and resumes travel together.
- **Impact:** SOC-01 and AC-5 now have a concrete round trip and checks for split parties, failed transitions, old saves and private party chat.

### 2026-11-05 - Define performance workloads and verify movement build

- **Change:** Added a repeatable browser and server performance playbook. Read back the deployed build and matched it to the merge commit for #1575.
- **Reason:** The user asked to improve performance while retaining game capacity and quality. The movement read optimization has live build evidence, while sustained memory and concurrency still need measurement.
- **Impact:** PERF-01 and AC-6 now specify workloads, metrics and comparison rules. No live load test or concurrency target is claimed. [Movement read PR](https://github.com/azurras/christopherbell.dev/pull/1575)

### 2026-11-05 - Verify the first party commands

- **Change:** Implemented and verified durable two-player invitation, acceptance, decline, cancellation and leave in the Party menu. The candidate uses the active survivor roster to invite and shows private state changes in chat.
- **Reason:** Shared combat needs explicit party membership to decide who can participate and earn credit. The menu gives the current desktop and text clients a common entry point.
- **Impact:** Party formation is verified locally at 3a14da91. In-world player targeting, shared HP, threat, skillchain coordination and the NPC assignment remain open. The initial BSON UUID write failure was corrected and retested. [Runtime report](../test-reports/2026-11-05-15-19-christopherbell-dev-survive-two-player-parties.md)

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

### 2026-11-05 - Verify the first party skillchain

- **Change:** Implemented the Impact skillchain. Unarmed Heavy Strike opens a saved window and a different member can close it with a club's Crushing Blow at least one second and less than five seconds later.
- **Reason:** The first shared outing needs a timing decision that lets two players produce a combined result.
- **Impact:** COM-02 and starting-zone AC-3 have local proof of a two-player chain and one defeat at 3616ac27. The initial pairing adds three damage. Magic bursts, enmity and the NPC objective remain open. [Runtime report](../test-reports/2026-11-05-22-16-christopherbell-dev-survive-impact-skillchain.md)

### 2026-11-05 - Verify Impact in production

- **Change:** PR #1578 passed CI and deployed as 57396651a22fc46ace1e94284a5f7dc62421f0f6. Production build readback matched the merge.
- **Reason:** The first shared outing needs a weapon skill sequence that rewards two players for timing their actions.
- **Impact:** Impact is live. The first NPC assignment and the complete outing playtest remain open. [PR #1578](https://github.com/azurras/christopherbell.dev/pull/1578)

### 2026-11-05 - Verify the first waystation patrol

- **Change:** Added the Waystation Keeper and North Gate Patrol. Each survivor accepts, contributes to a shared roaming victory and returns for two food and one experience point.
- **Reason:** The starting route needs a visible reason to leave camp and a clear return objective.
- **Impact:** Candidate 95c6f1b5 passed desktop NPC interaction and the two-session patrol and turn-in flow. The first reward uses supplies and experience. A full two-browser outing and physical controller play remain open. [Runtime report](../test-reports/2026-11-05-22-56-christopherbell-dev-survive-north-gate-patrol.md)

### 2026-11-05 - Verify North Gate Patrol in production

- **Change:** PR #1579 passed CI and deployed as 1b5de80cafad03cb1ec33de06af1ac9e766d1608. The live build matches the merge.
- **Reason:** North Gate Patrol connects the starting route, shared enemy and skillchain with a return reward.
- **Impact:** The assignment is live. The desktop NPC check and two-session HTTP round trip passed. Keep the child plan open for a complete two-browser outing and physical controller evidence. [PR #1579](https://github.com/azurras/christopherbell.dev/pull/1579)

### 2026-11-06 - Verify the two-browser North Gate outing

- **Change:** Verified the complete two-browser North Gate Patrol outing on deployed revision 1b5de80c using isolated test Mongo. Both players used the game UI for party formation, movement, assignment acceptance, Impact and reward turn-in.
- **Reason:** The previous report covered the full round trip through the HTTP contract and only the keeper interaction in a browser.
- **Impact:** The desktop two-browser evidence is recorded for AC-3 and AC-4. Physical controller play remains open. [Runtime report](../test-reports/2026-11-06-06-26-christopherbell-dev-survive-north-gate-two-browser-playthrough.md)

### 2026-11-06 - Define inventory and equipment parity

- **Change:** Added inventory and equipment parity slices and a first Main-slot acceptance check.
- **Reason:** The user asked for FFXI-style inventory and equipment. Current crafting replaces the active weapon and the equipment menu is read-only.
- **Impact:** JOB-01 and ECON-01 now have a shared equipment path. Start with retained weapons, a slot picker and old-save compatibility.

### 2026-11-06 - Verify Main equipment and packed weapons

- **Change:** Implemented the Main slot chooser and retained crafted spare weapons. Items shows packed gear and counts it toward the ten-unit cap.
- **Reason:** Players need to keep and compare useful weapons before the gear catalog expands.
- **Impact:** The first equipment slice is verified locally at 616b11b7. Sorting, armor, tools, job requirements and storage remain open. [Runtime report](../test-reports/2026-11-06-06-34-christopherbell-dev-survive-main-weapon-slot.md)

### 2026-11-06 - Verify Main equipment in production

- **Change:** PR #1580 passed CI and deployed as 355b10e62d7c9b41d407cf7f6d2a81166ed3ab6c. The production build matches the merge.
- **Reason:** The first inventory and equipment release lets players retain and manage the weapons they craft.
- **Impact:** The Main slot and spare-weapon list are live. Named item use and sorting, armor and tools, and storage remain open. [PR #1580](https://github.com/azurras/christopherbell.dev/pull/1580)

### 2026-11-06 - Verify sortable Items and food use

- **Change:** Added a sortable Items list for carried resources and spare weapons. Item descriptions and Use Food share the existing confirmed game action flow.
- **Reason:** Players need to inspect and use carried items from the menu.
- **Impact:** Candidate 578ed55a passed desktop sorting, refresh focus and food use. New item types and armor, tools and storage remain open. [Runtime report](../test-reports/2026-11-06-07-05-christopherbell-dev-survive-sortable-items.md)

### 2026-11-06 - Verify sortable Items in production

- **Change:** PR #1581 passed CI and deployed as 0c217e70306dd107c780d6ebc4e16e9e319e683a.
- **Reason:** The Items window needs usable selections and stable refresh behavior before expanding the item catalog.
- **Impact:** Sorting, descriptions and direct food use are live. Armor, tools and storage remain open. [PR #1581](https://github.com/azurras/christopherbell.dev/pull/1581)

### 2026-11-06 - Review the desktop look and verify game framing

- **Change:** Captured the starting route and verified a browser-filling desktop view with a reversible page-view switch.
- **Reason:** The player reported the game still looked and felt far from FFXI. The desktop capture showed that the website frame and unfinished scene both contributed.
- **Impact:** Candidate db8c9969 passed the desktop view checks. The art review now names the character and waystation changes needed for the next pass. [Runtime report](../test-reports/2026-11-06-08-17-christopherbell-dev-survive-desktop-game-view.md)

### 2026-11-06 - Verify desktop game framing in production

- **Change:** PR #1582 passed CI and deployed as e73b4e0d83414e5c17cb31774f726471016b6d20.
- **Reason:** Active desktop play needs the browser space for the world and its HUD.
- **Impact:** Browser-filling play and the page-view switch are live. The camp-to-keeper art and motion pass remains open. [PR #1582](https://github.com/azurras/christopherbell.dev/pull/1582)

### 2026-11-06 - Verify the first North Gate art pass

- **Change:** Adjusted adventurer head and leg proportions across baked clips, differentiated the keeper with a mantle and cap, and added roof courses, stone trim, a pennant and clustered plants to the approach.
- **Reason:** The default desktop camera showed overly similar character silhouettes and an underdeveloped waystation.
- **Impact:** Candidate 2789796a passed the route probe and art tests. ART-01 through ART-03 remain open for cloth, stronger environmental materials, combat motion and comparable captures. [Runtime report](../test-reports/2026-11-06-08-50-christopherbell-dev-survive-north-gate-art.md)

### 2026-11-06 - Verify independent enemy counters

- **Change:** Separated the enemy counter from player swings. A confirmed bite or consumed guard now drives a wind-back and lunge, and the raider no longer swings from the player's pose.
- **Reason:** A viewer should be able to tell who attacked and when the enemy responded.
- **Impact:** Candidate 6f1de67e passed the Chrome fight and motion tests. ART-03 remains open for telegraphs, hit reactions, ally playback and sound. [Runtime report](../test-reports/2026-11-06-09-05-christopherbell-dev-survive-enemy-counter-motion.md)

### 2026-11-06 - Verify the art and enemy counter releases

- **Change:** PR #1583 merged as ad3ab6b and PR #1584 merged as 9ff6562. Live build readback confirmed 9ff6562 contains both changes.
- **Reason:** The desktop visual pass and independent enemy counter passed their release checks.
- **Impact:** North Gate art and enemy counters are live. ART-01 through ART-03 remain open for the remaining visual and motion benchmark. [Art PR](https://github.com/azurras/christopherbell.dev/pull/1583) · [Motion PR](https://github.com/azurras/christopherbell.dev/pull/1584)

### 2026-11-06 - Verify the engaged stance

- **Change:** The local adventurer draws their equipped weapon in an engaged ready stance between attacks and stows it after Disengage.
- **Reason:** Engage needs a persistent visual signal between timed strikes.
- **Impact:** Desktop Chrome verified both poses on candidate 193449c2. ART-03 remains open for remote playback, hit reactions and sound. [Runtime report](../test-reports/2026-11-06-16-24-christopherbell-dev-survive-engaged-stance.md)

### 2026-11-06 - Verify the adventurer shading pass

- **Change:** Baked smooth adventurer shading across shallow edges while retaining creases, with the original triangle count and atlas.
- **Reason:** Flat triangle lighting made small face and armor surfaces read as harder facets at the desktop camera.
- **Impact:** Candidate c7721fbc passed the geometry tests and a desktop Chrome render. ART-02 remains open for matched lighting comparisons and face, hand and cloth artwork. [Runtime report](../test-reports/2026-11-06-16-27-christopherbell-dev-survive-adventurer-shading.md)

### 2026-11-06 - Verify the armed stance release

- **Change:** PR #1585 merged as a2fd1c4. Live build readback matched that commit.
- **Reason:** The armed ready pose passed its release checks.
- **Impact:** The local ready stance is live. Remote combat playback and transitions remain open. [Stance PR](https://github.com/azurras/christopherbell.dev/pull/1585)

### 2026-11-06 - Verify campfire and local firelight

- **Change:** Replaced the starting fire's opaque facets with soft flames and embers, added warm local falloff and textured the stone and timber pit.
- **Reason:** The campfire is prominent from the opening desktop camera on the North Gate review route.
- **Impact:** Candidate 8216f232 passed the Chrome motion comparison. ART-02 remains open for night, full-route and matched-lighting review. GPU cost remains unmeasured. [Runtime report](../test-reports/2026-11-06-17-11-christopherbell-dev-survive-campfire-and-local-firelight.md)

### 2026-11-06 - Verify nearby fighters draw and guard

- **Change:** Nearby adventurers show their confirmed equipped weapon and draw it when engaged. Guarding has a distinct pose, and fighters face a known encounter.
- **Reason:** Party members need to read each other's combat state from the world view.
- **Impact:** Two desktop Chrome contexts verified weapon draw and stance updates on candidate b3362b39 in a personal encounter. ART-03 remains open for shared-fight captures, strike playback and hit reactions. [Runtime report](../test-reports/2026-11-06-17-19-christopherbell-dev-survive-remote-combat-stance.md)

### 2026-11-06 - Verify nearby automatic strike playback

- **Change:** Committed strikes carry a short-lived cue, and nearby clients animate each cue once using the weapon that landed the hit.
- **Reason:** Observers need to see resolved attacks and should not replay repeated polls or old rounds settled after an absence.
- **Impact:** Two Chrome contexts confirmed an automatic strike and its visible swing on candidate a5de7699. ART-03 remains open for shared fights, weapon-skill browser proof and hit reactions. This branch builds on the nearby stance change. [Runtime report](../test-reports/2026-11-06-17-28-christopherbell-dev-survive-remote-strike-playback.md)

### 2026-11-06 - Verify weapon-skill cues across a shared fight

- **Change:** Ran the shared North Gate Patrol on the strike-playback candidate and verified that each participant received the other's weapon-skill cue.
- **Reason:** A personal encounter cannot verify visibility of the opening and closing attacks of a party skillchain.
- **Impact:** Both players completed Impact and turned in the patrol. The full Java suite passed. Shared-fight animation captures and the remaining hit and defeat cases stay open. [Runtime report](../test-reports/2026-11-06-17-28-christopherbell-dev-survive-remote-strike-playback.md)

### 2026-11-06 - Verify the local hit reaction

- **Change:** A confirmed damaging counter adds an upper-body recoil timed to enemy contact. Foot placement, camera and collision stay anchored.
- **Reason:** Players need to tell a landed bite from a blocked bite by watching the combatants.
- **Impact:** Chrome captured both exchanges on candidate 96838ea7. ART-03 still requires defeat and remote hit reactions. [Runtime report](../test-reports/2026-11-06-17-35-christopherbell-dev-survive-player-hit-recoil.md)

### 2026-11-06 - Verify the character shading release

- **Change:** PR #1586 merged as e76399b and the production build readback matched.
- **Reason:** Confirm the adventurer shading release reached the game.
- **Impact:** Smooth face and armor lighting is live. ART-01 and ART-02 remain open for geometry, materials and matched desktop captures. [Shading PR](https://github.com/azurras/christopherbell.dev/pull/1586)

### 2026-11-06 - Verify enemy defeat motion

- **Change:** A confirmed victory leaves the defeated enemy visible briefly to fall at the contact point while targeting and chat update immediately.
- **Reason:** The finishing attack needs a readable result in the world.
- **Impact:** Chrome captured a standing, fallen and cleared meadow hog on candidate 5baf77f6. ART-03 still requires shared and raider defeat captures, player collapse, audio and reduced-motion verification. [Runtime report](../test-reports/2026-11-06-17-41-christopherbell-dev-survive-enemy-defeat-motion.md)

### 2026-11-06 - Verify timed island fishing

- **Change:** Island fishing now saves a cast deadline, projects a bite by the bobber and accepts Reel In for five seconds after the bite. A missed bite, movement out of range or cancellation ends the cast.
- **Reason:** AC-4 and ART-03 require an observable cast, bite and reel instead of an instant food roll on the island.
- **Impact:** Chrome verified the cue, focus and expiry on candidate cb05119b. Server tests verified the catch and duplicate protection. Named fish, bait, skills, cooking, trade and controller proof remain open. [Runtime report](../test-reports/2026-11-06-17-51-christopherbell-dev-survive-timed-fishing.md)

### 2026-11-06 - Verify the campfire release

- **Change:** Campfire PR #1587 is live at 0c000f7. Nearby combat stance PR #1588 merged as 9b84b43 and is awaiting production readback.
- **Reason:** Record the delivery state independently of candidate checks.
- **Impact:** The starting camp has soft flames and local firelight. Shared strike playback still depends on the stance release. [Campfire PR](https://github.com/azurras/christopherbell.dev/pull/1587) · [Stance PR](https://github.com/azurras/christopherbell.dev/pull/1588)

### 2026-11-06 - Measure nearby movement payloads

- **Change:** Movement returns remote player poses within 64 metres and keeps the online count island-wide.
- **Reason:** Sending distant poses on every pulse wastes bandwidth and browser work while the renderer already stops drawing players past 60 metres.
- **Impact:** A matched eight-player layout dropped the camp pulse from 2,444 to 1,236 bytes. Chrome still showed eight online. PERF-01 remains open for sustained, clustered, browser, server and database measurements. [Runtime report](../test-reports/2026-11-06-17-55-christopherbell-dev-survive-nearby-presence-payload.md)

### 2026-11-06 - Refresh shared strike integration evidence

- **Change:** Integrated the strike branch with the merged stance, campfire and pending hit reaction, then reran the two-player patrol.
- **Reason:** The draft needed current-base evidence before it could follow the hit reaction into release.
- **Impact:** Candidate 88cdbed7 passed both shared weapon-skill cue checks and both patrol turn-ins. The missing main CI run for stance commit 9b84b43 was dispatched as run 42315295304. [Runtime report](../test-reports/2026-11-06-17-28-christopherbell-dev-survive-remote-strike-playback.md)

### 2026-11-06 - Verify live combat poses and ready shared strikes

- **Change:** Stance PR #1588 and hit reaction PR #1590 are live at 129c2c13. Strike candidate e821ea0a was verified against this main tree.
- **Reason:** Confirm released behavior independently of candidate tests and ready the shared strike follow-up.
- **Impact:** Shared strike delivery and the fresh personal strike check passed. The nearby-payload candidate passed a full Java rerun in its own checkout after the earlier mixed-class run was invalidated. [Strike report](../test-reports/2026-11-06-17-28-christopherbell-dev-survive-remote-strike-playback.md) · [Presence report](../test-reports/2026-11-06-17-55-christopherbell-dev-survive-nearby-presence-payload.md)

### 2026-11-06 - Verify the fishing bank composition

- **Change:** Framed the fishing dock with stone groups, driftwood and bent reeds, extended sand below the ocean plane and darkened the wet edge.
- **Reason:** The shoreline capture showed an empty bank and a hard sand-to-water boundary.
- **Impact:** Candidate aa38c563 passed the desktop bank capture and 468 JavaScript tests. ART-02 stays open for stronger water and terrain finish, nighttime and matched route review. The sand transition is subtle from the default camera. [Runtime report](../test-reports/2026-11-06-21-56-christopherbell-dev-survive-fishing-bank-artwork.md)

### 2026-11-06 - Verify distinct weapon cadence

- **Change:** Equipped weapons use distinct automatic-attack delays, shown in Equipment and weapon item details. The interval is recomputed after impact so breakage uses bare hands next.
- **Reason:** COM-02 calls for weapons with distinct combat cadence.
- **Impact:** Candidate 2c94362c passed the club deadline and Equipment browser check. Club 3.2s, axe 3.8s and spear 4.2s are initial Survive balance values. COM-02 remains open for TP scaling, shared-fight balance, spell timing and recovery. [Runtime report](../test-reports/2026-11-06-22-01-christopherbell-dev-survive-weapon-cadence.md)

### 2026-11-06 - Verify fishing and presence with shared strikes

- **Change:** Refreshed fishing and nearby-pose candidates against merged strike playback. Cast state and strike cues now coexist in saved progress.
- **Reason:** New releases must preserve both gameplay state and nearby combat presentation.
- **Impact:** Fishing repeated the bite, reel and expiry checks. The eight-player layout still sent one nearby pose and counted eight online. Weapon cadence passed its full Java suite. [Fishing report](../test-reports/2026-11-06-17-51-christopherbell-dev-survive-timed-fishing.md) · [Presence report](../test-reports/2026-11-06-17-55-christopherbell-dev-survive-nearby-presence-payload.md)

### 2026-11-06 - Verify local strike ownership

- **Change:** The local adventurer animates their own committed strike cue instead of inferring an attack from shared enemy HP.
- **Reason:** A party member's hit could make the local fighter swing without attacking.
- **Impact:** The mounted-world regression and two-browser cue check passed on candidate 222271f0. A shared-party visual capture remains open. [Runtime report](../test-reports/2026-11-06-22-10-christopherbell-dev-survive-local-strike-ownership.md)

### 2026-11-06 - Verify defeat motion and its reduced-motion path

- **Change:** Integrated enemy defeat motion with shared-strike playback and verified normal and reduced motion in separate browser runs.
- **Reason:** The finishing blow needs readable motion while respecting the player's motion preference.
- **Impact:** Candidate 812ac98e showed the fall normally and cleared the defeated target in reduced motion. Shared-fight and raider captures and player collapse remain open. [Runtime report](../test-reports/2026-11-06-17-41-christopherbell-dev-survive-enemy-defeat-motion.md)

### 2026-11-06 - Verify live shared strike playback

- **Change:** Shared strike playback PR #1589 is live at 48d17010. Nearby-payload PR #1593 merged as 012bb295 and awaits production verification.
- **Reason:** Keep release state distinct from candidate proof.
- **Impact:** Other players' confirmed strikes are live. The local strike-ownership correction passed its full Java suite. [Strike PR](https://github.com/azurras/christopherbell.dev/pull/1589) · [Presence PR](https://github.com/azurras/christopherbell.dev/pull/1593)

### 2026-11-06 - Verify gameplay on nearby-presence main

- **Change:** Integrated fishing and weapon cadence with the merged nearby-presence payload and reran their normal browser entry points.
- **Reason:** The next gameplay releases must work with the current multiplayer response.
- **Impact:** Fishing repeated bite, reel and expiry. Weapon cadence repeated the club interval and Equipment label. Both candidates passed targeted Java, JavaScript and build checks. [Fishing report](../test-reports/2026-11-06-17-51-christopherbell-dev-survive-timed-fishing.md) · [Cadence report](../test-reports/2026-11-06-22-01-christopherbell-dev-survive-weapon-cadence.md)

### 2026-11-06 - Verify motion with nearby multiplayer payloads

- **Change:** Integrated defeat motion and local strike ownership with nearby-presence main 012bb295 and repeated their browser checks.
- **Reason:** Attack and defeat presentation must remain correct after multiplayer payload filtering.
- **Impact:** Normal hog fall and owner/observer strike revision 18 passed on exact candidates d791612d and 14e40a7b. Shared-party defeat and broader motion/asset parity remain open. [Defeat report](../test-reports/2026-11-06-17-41-christopherbell-dev-survive-enemy-defeat-motion.md) · [Ownership report](../test-reports/2026-11-06-22-10-christopherbell-dev-survive-local-strike-ownership.md)

### 2026-11-06 - Verify bank artwork on current multiplayer main

- **Change:** Integrated the fishing bank artwork with current main and repeated the desktop bank capture.
- **Reason:** Static world artwork must coexist with current shared-strike rendering and nearby-player payloads.
- **Impact:** Candidate 41fbd62e passed 469 JavaScript tests and the corrected browser invocation. The dock composition is verified; water, terrain, actor quality and measured hardware performance remain open. [Bank report](../test-reports/2026-11-06-21-56-christopherbell-dev-survive-fishing-bank-artwork.md)

### 2026-11-07 - Verify live fishing and its defeat motion integration

- **Change:** Nearby-player payload filtering and timed fishing reached production at 125bd326. Rebased the enemy fall candidate by merging that live main.
- **Reason:** Keep the defeat and fishing cues working together in the same graphics loop.
- **Impact:** Candidate c672dee1 passed 472 JavaScript tests and the normal hog fall, projected bite, reel and expiry paths in isolated Chrome. Rod, bait, named catch and party defeat review remain open. [Defeat integration report](../test-reports/2026-11-06-17-41-christopherbell-dev-survive-enemy-defeat-motion.md) · [Fishing PR](https://github.com/azurras/christopherbell.dev/pull/1592)

### 2026-11-07 - Verify nearby fighter hit reaction

- **Change:** Added a brief torso recoil when a nearby fighter's confirmed combat health decreases. Stance and strike remain independent and reduced motion suppresses recoil.
- **Reason:** Other players' attacks and their consequences both need to read in the world, including when their own browser is not controlling the observed animation.
- **Impact:** Candidate 6cebcc6b passed 472 JavaScript tests, targeted Java checks and two Chrome observer captures. Shared-party capture, enemy playback and collapse remain open. The capture also exposes weak facial definition and identical player silhouettes for ART-01. [Child plan](2026-11-06-22-27-christopherbell-dev-survive-remote-hit-recoil.md) · [Runtime report](../test-reports/2026-11-07-12-19-christopherbell-dev-survive-remote-hit-recoil.md)

### 2026-11-07 - Verify mapped adventurer facial detail

- **Change:** Painted eyes, brows and soft lip contours on the original adventurer's mirrored face chart before the existing atlas upload.
- **Reason:** Front desktop captures exposed an almost featureless face despite the modeled nose and cheeks.
- **Impact:** Candidate 4ef4f6e5 passed 473 JavaScript tests and repeated the desktop orbit with merged enemy defeat. Eyes and brows are clearer. Mouth definition, head geometry, character variation and matched lighting at all angles remain open. [Child plan](2026-11-07-12-23-christopherbell-dev-survive-adventurer-face.md) · [Runtime report](../test-reports/2026-11-07-12-27-christopherbell-dev-survive-adventurer-face.md)

### 2026-11-07 - Measure shared-network movement and find the first throttle

- **Change:** Measured the fixed 2, 5, 10 and 20 session camp ladder. Two baseline builds reproduced 420 throttles out of 480 attempts at the 20-session stage. The isolated dedicated quota accepted all 2,664 measured pulses across three repetitions.
- **Reason:** Half-second movement polls share the 300-per-minute mutation quota with commands. The first bottleneck in this loopback test was admission, with 19 of 20 departures also throttled on main bf51abaf.
- **Impact:** Candidate e0dbaed5 reached 40 accepted movement requests per second in the short 20-session windows. Keep it local pending protection against invalid-owner database lookups under the shared game lock. Longer browser and mixed multiplayer workloads remain open. [Child plan](2026-11-07-12-34-christopherbell-dev-survive-movement-rate-limit.md) · [Runtime report](../test-reports/2026-11-07-12-40-christopherbell-dev-survive-shared-network-movement-quota.md)

### 2026-11-07 - Verify live defeat animation

- **Change:** Verified that the enemy defeat animation from PR #1591 is live at bf51abaf. The adventurer face update passed independent review and entered the release queue.
- **Reason:** Track production behavior separately from isolated runtime proof.
- **Impact:** Personal hog defeat is live. Shared-fight and raider defeat capture remain open. [Defeat PR](https://github.com/azurras/christopherbell.dev/pull/1591) · [Face PR](https://github.com/azurras/christopherbell.dev/pull/1598)

### 2026-11-07 - Verify live adventurer facial detail

- **Change:** Verified production build e5d948e2 from PR #1598 and confirmed the public material module serves the face paint.
- **Reason:** Keep the shipped art state distinct from isolated desktop capture evidence.
- **Impact:** Eyes and brows are live. Head geometry, mouth definition and character silhouettes remain open under ART-01. [Face PR](https://github.com/azurras/christopherbell.dev/pull/1598)

### 2026-11-07 - Verify guarded shared-network movement

- **Change:** Added durable owner admission ahead of the dedicated movement budget's database path. Fixed compatibility with legacy persisted UUID spellings.
- **Reason:** Unknown and expired credentials should stop before the shared game monitor or Mongo. Movement still verifies the latest owner after admission.
- **Impact:** Final candidate 33e8270b accepted 888 of 888 pulses and all departures in the short ladder. The positive control accessed the world once, and 102 invalid credentials accessed it zero times. The full native suites and isolated proof passed. Release and longer workloads remain open. [Child plan](2026-11-07-12-34-christopherbell-dev-survive-movement-rate-limit.md) · [Runtime report](../test-reports/2026-11-07-12-40-christopherbell-dev-survive-shared-network-movement-quota.md)

### 2026-11-07 - Verify club and axe cadence through Equipment

- **Change:** Integrated distinct weapon delays with timed fishing, enemy defeat and face art. Repeated the club case and equipped the packed stone axe through the Main picker in a second desktop session.
- **Reason:** Equipment and field combat need to agree on cadence for more than one weapon.
- **Impact:** Candidate 31563f15 confirmed club 3.2s and axe 3.8s in both Equipment and consecutive strike deadlines. Spear, shared-fight timing and broader balance remain open. [Runtime report](../test-reports/2026-11-06-22-01-christopherbell-dev-survive-weapon-cadence.md)

### 2026-11-07 - Verify confirmed ally damage on North Gate Patrol

- **Change:** Verified remote hit feedback on the shared North Gate Patrol route with two desktop browsers.
- **Reason:** A personal encounter alone does not prove a party member receives confirmed damage during a shared fight.
- **Impact:** Candidate 210f4d3a delivered both skill cues and a confirmed 9-to-6 ally health change. Both patrol rewards were collected. Shared recoil frames, player collapse and broader party roles remain open. [Runtime report](../test-reports/2026-11-07-12-19-christopherbell-dev-survive-remote-hit-recoil.md)

### 2026-11-07 - Refresh local strike and movement release proof

- **Change:** Revalidated local strike ownership with current fishing and defeat motion. Corrected the movement candidate's Checkstyle failure and repeated the invalid-owner profiler probe.
- **Reason:** Preserve distinct player action feedback and verify the admission guard on the exact CI correction.
- **Impact:** Candidate d0959e56 delivered club revision 16 to both browsers. Candidate e62d3dde passed local Checkstyle and again rejected 102 invalid credentials without a world access. Both releases await CI and production. [Strike report](../test-reports/2026-11-06-22-10-christopherbell-dev-survive-local-strike-ownership.md) · [Movement report](../test-reports/2026-11-07-12-40-christopherbell-dev-survive-shared-network-movement-quota.md)

### 2026-11-07 - Verify party enmity and guard routing

- **Change:** Shared field fights now store lasting and fading damage enmity and counter the living fighter with the highest combined score. Receiving damage reduces the lasting part, and a defender can guard against an ally-triggered counter.
- **Reason:** Party roles need durable enemy attention and truthful combat feedback. The child uses initial Survive weights for the two-component design described by Square Enix.
- **Impact:** The stacked candidate 453f361c passed two-player state proof, including a consumed guard, shared HP and no new defender strike. It depends on the local strike ownership fix. Independent enemy timing, Provoke, healing threat and visual facing remain open. [Child plan](2026-11-07-13-09-christopherbell-dev-survive-party-enmity.md) · [Runtime report](../test-reports/2026-11-07-13-21-christopherbell-dev-survive-shared-party-enmity.md)

### 2026-11-07 - Verify live shared-network movement quota

- **Change:** Verified the guarded shared-network movement quota live at 99b7edfe from PR #1599.
- **Reason:** Record deployment separately from the isolated traffic measurements.
- **Impact:** Dedicated movement and early owner admission are shipped. PERF-01 still requires sustained desktop, distributed and mixed combat workloads. [Movement PR](https://github.com/azurras/christopherbell.dev/pull/1599) · [Runtime report](../test-reports/2026-11-07-12-40-christopherbell-dev-survive-shared-network-movement-quota.md)

### 2026-11-07 - Verify party HP and TP in the viewport

- **Change:** Added a private accepted-party HP and TP row to the viewport status panel.
- **Reason:** A party member's remaining HP and TP inform guard and weapon-skill timing during exploration and combat.
- **Impact:** Candidate 55edfdee verified two desktop clients, hidden invitations, an HP and TP update after a combat round and clearing both rows on leave. The existing status poll carries the values. Larger parties and MP remain open. [Runtime report](../test-reports/2026-11-07-13-39-christopherbell-dev-survive-party-vitals.md)

### 2026-11-07 - Verify enmity after strike ownership merged

- **Change:** Integrated the enmity candidate after the strike ownership fix merged to main.
- **Reason:** Both sides of the shared counter need to retain correct strike ownership and health after integration.
- **Impact:** Candidate cba4a7ac repeated the two-player bear proof with correct guard consumption and matching enemy health. CI and production are pending. [Runtime report](../test-reports/2026-11-07-13-21-christopherbell-dev-survive-shared-party-enmity.md)

### 2026-11-07 - Verify weapon cadence alongside confirmed strikes

- **Change:** Integrated distinct weapon attack delays alongside confirmed local strikes.
- **Reason:** Equipment delay and the animation cue must both survive the same combat response.
- **Impact:** Exact candidate 2b1437da repeated the club and axe deadline checks in desktop Chrome. Spear and shared-fight cadence still need direct browser coverage. [Runtime report](../test-reports/2026-11-06-22-01-christopherbell-dev-survive-weapon-cadence.md)

### 2026-11-07 - Verify live confirmed local strikes

- **Change:** Verified PR #1596 live at production build cec581eb.
- **Reason:** A shared fight can change a survivor's health or revision without that survivor swinging.
- **Impact:** Local attack playback now follows the owning survivor's confirmed strike. The released change is the baseline for the enmity and nearby hit feedback checks. [Strike PR](https://github.com/azurras/christopherbell.dev/pull/1596) · [Runtime report](../test-reports/2026-11-06-22-10-christopherbell-dev-survive-local-strike-ownership.md)

### 2026-11-07 - Verify nearby ally damage alongside confirmed strikes

- **Change:** Integrated nearby adventurer hit feedback with confirmed local strike ownership.
- **Reason:** Shared combat must distinguish the attacking survivor from the ally who receives damage.
- **Impact:** Candidate 2eddf372 repeated confirmed ally damage and two completed patrols. The shared capture did not clearly show the fighters, so shared pose readability stays open. [Runtime report](../test-reports/2026-11-07-12-19-christopherbell-dev-survive-remote-hit-recoil.md)

### 2026-11-12 - Verify live party enmity and vitals

- **Change:** Released damage-based enmity and the accepted-party HP and TP panel.
- **Reason:** Party members need to manage which fighter draws the enemy's attention and see how an ally is doing without opening a menu.
- **Impact:** Production reports build 9fe53463, which contains both changes. The isolated browser runs verified guard consumption and shared enemy HP, and confirmed that ally HP and TP update and clear on departure. Independent enemy attack timing, healing enmity, MP and larger parties remain open. [Enmity PR](https://github.com/azurras/christopherbell.dev/pull/1600) · [Party vitals PR](https://github.com/azurras/christopherbell.dev/pull/1601)

### 2026-11-12 - Review the fishing bank on the party release baseline

- **Change:** Integrated the fishing-bank artwork with the live party combat and HUD baseline.
- **Reason:** Recheck the shoreline from the default desktop camera before releasing it.
- **Impact:** Candidate 62360467 passed the daylight capture and 475 JavaScript tests. The reeds and rocks frame the dock. The bright water horizon seam, subtle sand transition and matched nighttime comparison remain open. [Runtime report](../test-reports/2026-11-06-21-56-christopherbell-dev-survive-fishing-bank-artwork.md)

### 2026-11-12 - Remove the bright shoreline horizon seam

- **Change:** Give the full sky dome an explicit shader material so its lower hemisphere uses the horizon color.
- **Reason:** Elevation-based shading sent the visible bottom of the white dome through ground lighting at the waterline.
- **Impact:** Candidate 55e135b4 removed the bright strip in the default-distance daylight desktop comparison. Night and route-wide comparisons remain open. [Runtime report](../test-reports/2026-11-12-15-10-christopherbell-dev-survive-sky-horizon.md)

### 2026-11-12 - Prioritize FFXI-style menu navigation

- **Change:** Prioritize menu parity under UI-01. Escape closes the focused child panel and restores its opening row. The top-level keyboard list includes the view toggle and skips rows hidden by the map.
- **Reason:** FFXI assigns a dedicated Cancel control, and the previous Survive behavior closed the entire Main Menu from Equipment.
- **Impact:** Candidate e5d9446a passed the three-step desktop Equipment cancel flow. Compact category navigation, consistent child panels, inventory and equipment browsing, and a physical controller pass remain open. [Runtime report](../test-reports/2026-11-12-15-13-christopherbell-dev-survive-menu-navigation.md)

### 2026-11-12 - Give Main Menu categories separate desktop panels

- **Change:** Give the selected Main Menu category its own framed panel to the left of a compact desktop category list. Only one category opens at a time.
- **Reason:** Map and Equipment should be easy to switch between while leaving the game visible and preserving the menu hierarchy.
- **Impact:** Desktop candidate 894546f2 verified panel bounds, Map to Equipment switching and three levels of cancellation. Narrow viewport and physical controller checks remain open. [Runtime report](../test-reports/2026-11-12-15-16-christopherbell-dev-survive-menu-panels.md)

### 2026-11-12 - Verify narrow desktop menu panels and gamepad cancel

- **Change:** Keep category rows compact in the narrow desktop layout by removing inherited section padding.
- **Reason:** The first narrow-window capture showed that opening Map pushed its contents below the visible menu.
- **Impact:** Candidate 42702357 passed the narrow Map and Equipment flow and restored focus after simulated gamepad B and keyboard Escape. A physical controller pass remains open. [Runtime report](../test-reports/2026-11-12-15-16-christopherbell-dev-survive-menu-panels.md)

### 2026-11-12 - Browse carried items with the controller D-pad

- **Change:** Browse carried items using vertical D-pad input and move to the next menu control at the end of the list.
- **Reason:** D-pad Down previously skipped the item rows while the inventory list had focus.
- **Impact:** Candidate fe481a33 confirmed item selection and detail updates in desktop Chrome with a simulated controller. Physical controller testing remains open. [Runtime report](../test-reports/2026-11-12-15-22-christopherbell-dev-survive-controller-item-browsing.md)

### 2026-11-12 - Verify menu navigation after shoreline integration

- **Change:** Integrated the menu navigation candidate with the merged fishing bank artwork.
- **Reason:** Verify the release candidate against the current main branch.
- **Impact:** Exact candidate 9b8c494a repeated the Equipment cancellation flow in desktop Chrome. CI and production readback are pending. [Runtime report](../test-reports/2026-11-12-15-13-christopherbell-dev-survive-menu-navigation.md)

### 2026-11-12 - Browse the weapon picker with arrow keys

- **Change:** Use Up and Down to move between available buttons and summaries inside the current menu panel.
- **Reason:** Keyboard arrows previously moved only between top-level rows and left equipment choices to Tab.
- **Impact:** Candidate 0f189563 verified focus on the packed stone axe and confirmed its equipment change in Chrome. [Runtime report](../test-reports/2026-11-12-15-28-christopherbell-dev-survive-weapon-picker-keys.md)

### 2026-11-12 - Verify the fishing-bank horizon at night

- **Change:** Verified the fishing-bank sky fix with night shading at the default desktop camera.
- **Reason:** The daylight capture alone did not exercise the darker horizon colors.
- **Impact:** Candidate 04158c52 showed no bright seam with a browser-supplied night snapshot. Natural phase transition and route-wide lighting remain open. [Runtime report](../test-reports/2026-11-12-15-10-christopherbell-dev-survive-sky-horizon.md)

### 2026-11-12 - Verify live fishing-bank artwork

- **Change:** Verified the fishing-bank artwork live in production build 0cefdc29.
- **Reason:** Confirm that the dock, reed groups, shoreline rocks and submerged sand made it into the public game build.
- **Impact:** The public build identity matches the merged shoreline PR. The horizon shader correction is separately verified in desktop Chrome and awaits its own release. [Shoreline PR](https://github.com/azurras/christopherbell.dev/pull/1594) · [Horizon PR](https://github.com/azurras/christopherbell.dev/pull/1603)

### 2026-11-12 - Verify desktop menu layout and input together

- **Change:** Verify the compact layout, keyboard equipment browsing and gamepad inventory controls together on the same release candidate.
- **Reason:** These changes share the same menus and need to work together across both desktop layouts.
- **Impact:** Candidate 0f189563 passed all three desktop browser flows and the weapon picker check. Use PR #1607 to release the layout and input changes together after #1604. Physical controller playtesting remains open. [Runtime report](../test-reports/2026-11-12-15-28-christopherbell-dev-survive-weapon-picker-keys.md)

### 2026-11-12 - Verify restored party weapon timers

- **Change:** Verify independent weapon timers after a shared fight is saved and restored.
- **Reason:** A party fight needs to keep each fighter's cadence while sharing enemy HP.
- **Impact:** Candidate 2514301b passed the shared-fight regression and a desktop Chrome axe check. Browser verification of simultaneous weapon timings remains open. [Runtime report](../test-reports/2026-11-06-22-01-christopherbell-dev-survive-weapon-cadence.md)

### 2026-11-12 - Verify combined menu candidate after cancellation merge

- **Change:** Integrated the combined menu candidate with merged menu cancellation.
- **Reason:** Confirm that layout and input behavior survive integration with main.
- **Impact:** Candidate 2c7ec5ff passed all four desktop browser flows. CI, production readback and physical controller playtesting remain open. [Runtime report](../test-reports/2026-11-12-15-28-christopherbell-dev-survive-weapon-picker-keys.md)

### 2026-11-12 - Verify separate weapon intervals in a shared browser fight

- **Change:** Verified barehanded and club strike cadence in one shared bear fight through two desktop Chrome sessions.
- **Reason:** The shared-world regression and solo axe run did not prove two clients could observe independent deadlines during the same encounter.
- **Impact:** Candidate 2514301b confirmed 3,000 ms and 3,200 ms intervals. Shared spear timing and longer catch-up remain open. [Runtime report](../test-reports/2026-11-06-22-01-christopherbell-dev-survive-weapon-cadence.md)

### 2026-11-12 - Verify live menu cancellation and focus restoration

- **Change:** Verified the one-panel-at-a-time menu cancellation release live in production build 98f64390.
- **Reason:** Confirm the deployed game includes the focus restoration verified in the Equipment browser flow.
- **Impact:** The public build matches PR #1604. The combined menu layout, item browsing and equipment navigation remain tracked in #1607. [Cancellation PR](https://github.com/azurras/christopherbell.dev/pull/1604) · [Combined menu PR](https://github.com/azurras/christopherbell.dev/pull/1607)

### 2026-11-12 - Show enemy attention during shared combat

- **Change:** Show the current enmity leader in the viewport vitals panel for both active shared fighters.
- **Reason:** A protector needs to see who has drawn the enemy's attention while coordinating guard and attacks.
- **Impact:** Candidate 1531a119 passed the two-client bear check on the merged desktop menu baseline. Ability-driven and healing enmity, independent enemy attacks and visual facing remain open. [Runtime report](../test-reports/2026-11-12-15-53-christopherbell-dev-survive-enemy-attention.md)

### 2026-11-12 - Verify live desktop menu layout and input

- **Change:** Verified desktop menu layout and input live at production build 2d9f6e91.
- **Reason:** Confirm the public build includes the compact category list, separate desktop panels, D-pad item browsing and keyboard equipment navigation.
- **Impact:** The deployed build matches PR #1607. Physical controller playtesting and broader equipment slots remain open. [Menu PR](https://github.com/azurras/christopherbell.dev/pull/1607)

### 2026-11-12 - Face shared enemies toward their attention target

- **Change:** Use the confirmed enmity leader's survivor ID to turn shared enemies toward that fighter's position.
- **Reason:** Both clients previously rendered the enemy facing their own player, even when the ally drew its attention.
- **Impact:** Commit 27e5bfa4 passed the Survive Java suite, Checkstyle and 480 JavaScript tests, including local, remote and missing-pose cases. A matched two-player combat capture and release remain open.

### 2026-11-12 - Inspect shared enemy facing in two desktop clients

- **Change:** Ran the shared enemy facing candidate in two desktop Chrome sessions and inspected both captures.
- **Reason:** Verify that the remote fighter's confirmed identity resolves to a visible pose in the running game.
- **Impact:** Candidate 27e5bfa4 delivered the same target identity to both clients. The capture exposed muzzle overlap and an obscured scout, so combat spacing and a clear two-fighter visual comparison remain open. [Runtime report](../test-reports/2026-11-12-15-53-christopherbell-dev-survive-enemy-attention.md)

### 2026-11-12 - Keep shared enemies at their confirmed position

- **Change:** Render shared enemies at their confirmed world location on both clients.
- **Reason:** The local approach could pull the same bear to different positions and crowd the fighter.
- **Impact:** Candidate aabc0979 passed the mounted position regression and the two-client bear attention check. The scout capture shows separation. Quarry rocks obscure the ally view, leaving combat camera framing and a clear two-angle check open. [Runtime report](../test-reports/2026-11-12-15-53-christopherbell-dev-survive-enemy-attention.md)

### 2026-11-12 - Reject quarry camera pull-in after desktop capture

- **Change:** Tested a quarry-aware follow camera against the shared bear route on candidate b9b25bb7.
- **Reason:** The ally camera could lose both fighters behind rocks.
- **Impact:** All 482 JavaScript tests passed, but the ally capture showed an extreme close-up that hid the encounter. Reverted the camera pull-in at f83f90ca. Keep camera framing open and require full fighter and target visibility in the obstructed view before accepting another camera adjustment.

### 2026-11-12 - Verify ally damage on the enemy attention baseline

- **Change:** Verified ally damage feedback and both patrol turn-ins on the enemy attention baseline.
- **Reason:** Confirm shared damage and strike cues still reach the observing client after the party HUD change.
- **Impact:** Candidate 373405a8 confirmed an ally HP drop from 6 to 3 and both patrol rewards. The frame was obstructed by quarry rock, leaving shared recoil readability open. [Runtime report](../test-reports/2026-11-07-12-19-christopherbell-dev-survive-remote-hit-recoil.md)

### 2026-11-12 - Update the in-game guide for real-time play

- **Change:** Update the in-game Guide and fullness warning for current real-time systems.
- **Reason:** The Guide described obsolete per-action hunger and one-step fishing rules.
- **Impact:** Candidate 0223ef9a passed 480 JavaScript tests and a desktop Main Menu Guide check. [Runtime report](../test-reports/2026-11-12-20-43-christopherbell-dev-survive-real-time-field-guide.md)

### 2026-11-12 - Clarify automatic attack state in the enemy panel

- **Change:** Show Ready to engage in the enemy panel when automatic attacks are idle. Keep the enemy name and HP visible during the encounter.
- **Reason:** The previous proximity heading was ambiguous after Disengage, when the enemy was still in the encounter.
- **Impact:** Commit 328c9d24 passed all 479 JavaScript tests. The HUD regression covers active attacks, idle engagement and encounter exit. Desktop runtime verification and release remain open.

### 2026-11-12 - Verify the enemy panel through Engage and Disengage

- **Change:** Verified Engage and Disengage in desktop Chrome against the merged shared positioning build.
- **Reason:** The enemy panel must show whether automatic attacks are active while keeping the target readable.
- **Impact:** Candidate eb44d965 showed In combat while attacking and Ready to engage after Disengage, with hog HP still visible. [Runtime report](../test-reports/2026-11-12-20-46-christopherbell-dev-survive-combat-target-status.md)

### 2026-11-12 - Keep target Check available during combat

- **Change:** Keep Check available on a selected target during automatic combat.
- **Reason:** Players previously had to stop automatic attacks to inspect the target again.
- **Impact:** Candidate 11e0e84a passed 481 JavaScript tests and a desktop hog fight in which Check reported to chat while the strike timer remained active. [Runtime report](../test-reports/2026-11-12-20-53-christopherbell-dev-survive-check-during-combat.md)

### 2026-11-13 - Add pack management before player trade

- **Change:** Add confirmed one-item discard and persistent camp pack upgrades from ten to thirty slots.
- **Reason:** Players need to manage pack space before gathering, crafting and exchanging items.
- **Impact:** Candidate d554c9ca passed the desktop upgrade and cancel flow and verified permanent supply discard through the service. Direct trade remains an explicit ECON-01 deliverable. Require both players to confirm the same offer and atomically check both inventories, capacity and eligibility before transferring either side. [Runtime report](../test-reports/2026-11-13-09-07-christopherbell-dev-survive-pack-management.md)

### 2026-11-13 - Add confirmed player supply trades

- **Change:** Add private, expiring offers through Camp & sharing. Sending an offer confirms the sender's terms. The recipient can accept or decline, and the sender can withdraw.
- **Reason:** Both players need to see and agree to the same exchange before their inventories change.
- **Impact:** Candidate 11aa2ebf verified supply exchanges in separate Chrome sessions. The server checks ownership, camp eligibility, stock, and both pack capacities before saving the exchange. The first slice covers one stack per player. Equipment and multi-item trades remain open. [Runtime report](../test-reports/2026-11-13-09-19-christopherbell-dev-survive-player-trade.md)

### 2026-11-13 - Release expired and abandoned trades

- **Change:** End pending offers at the two-minute deadline or when one of the survivors leaves the camp roster.
- **Reason:** The remaining survivor needs to trade again immediately if their partner replaces their character.
- **Impact:** Chrome verified the released slot, intact stock, and the sender's chat notice. The service test verified both packs at the exact timeout. [Runtime report](../test-reports/2026-11-13-09-24-christopherbell-dev-survive-trade-lifecycle.md)

### 2026-11-13 - Offer packed weapons in player trade

- **Change:** Let a sender offer one packed weapon for supplies. The recipient sees its remaining uses before accepting.
- **Reason:** A packed weapon needs to retain its individual condition when it changes owners.
- **Impact:** The Chrome playthrough verified that the same copy and condition transfer together with payment. The service rejects a weapon that was equipped after the offer. Multi-item offers and requests for another survivor's equipment remain open. [Runtime report](../test-reports/2026-11-13-09-28-christopherbell-dev-survive-packed-weapon-trade.md)

### 2026-11-13 - Let both players set trade terms

- **Change:** The recipient can counter an offer with their own supply stack or packed weapon. Revised terms replace the old offer and require the original sender's acceptance.
- **Reason:** A counteroffer lets the recipient propose a different exchange before either pack changes.
- **Impact:** The service rejected acceptance of the superseded offer. Two Chrome sessions reviewed and exchanged two clubs with distinct wear. Multi-item trades remain open. [Runtime report](../test-reports/2026-11-13-09-34-christopherbell-dev-survive-trade-counteroffers.md)

### 2026-11-13 - Support multi-item trade offers

- **Change:** Players can offer up to eight distinct supply stacks or packed weapons. Counteroffers preserve the exact bundle offered by the other player.
- **Reason:** A bundle lets both players agree to an exchange involving multiple lots.
- **Impact:** Chrome verified a revised exchange of two distinct weapons and one wood. The server rejects duplicate lots and validates the entire exchange before moving stock. Initial offers still request one supply stack. [Runtime report](../test-reports/2026-11-13-09-40-christopherbell-dev-survive-trade-bundles.md)

### 2026-11-13 - Verify proximity for island trades

- **Change:** Require two recent island poses within five metres for offers, counteroffers and acceptance. Text-mode players can trade at their shared camp.
- **Reason:** Island trade requires the players to be near each other when they agree to an exchange.
- **Impact:** A committed two-player candidate rejected acceptance at six metres and kept both packs intact. Moving within five metres allowed the same exchange. [Runtime report](../test-reports/2026-11-13-09-45-christopherbell-dev-survive-nearby-trade.md)

### 2026-11-13 - Show nearby partners in the Trade menu

- **Change:** Use the server-confirmed range to filter trade partners and disable acceptance and counteroffers while the other survivor is out of reach.
- **Reason:** Use the server range decision to guide player actions.
- **Impact:** The service test verified the five-metre boundary and Chrome verified a complete nearby exchange. The menu shows a range message while an offer is out of reach. [Runtime report](../test-reports/2026-11-13-09-50-christopherbell-dev-survive-trade-targets.md)

### 2026-11-13 - Identify timed shore catches

- **Change:** Timed fishing reports shore herring, reef bream, or night eel. Rare catches depend on the phase at cast and yield up to two food within the pack limit.
- **Reason:** Identify the catch and reflect the fishing conditions at cast time.
- **Impact:** Candidate 17ea406d passed the Survive Java suite and Checkstyle. Tests verified a named catch through the movement and reel flow, and verified that a night eel with one free slot awards one food. Desktop runtime, separate fish inventory items, rods, and bait remain open.

## Outcome

Pending.

## Project

christopherbell-dev

## Plan Format

task-contract-v2

### 2026-11-13 - Review the North Gate approach at desktop scale

- **Change:** Candidate 10f6bfca gave the North Gate banks different profiles and softened the grass-to-earth transition with the existing texture samples.
- **Evidence:** JavaScript tests and bootJar passed. Chrome rendered the exact committed build at desktop scale. The nighttime camp capture shows the arch framed by the banks and readable ground texture.
- **Remaining:** AC-2 stays open. The captured adventurer silhouette, stone silhouette, understory density and tree variation still fall short of the references. Compare a matched daylight route with both references before claiming visual parity.

### 2026-11-13 - Add layered understory on the North Gate approach

- **Change:** Candidate 63aafae5 groups shrub and grass stands along the banks and varies shrub crown height and tint. Placement preserves the trail and stream.
- **Evidence:** All 476 JavaScript tests and bootJar passed. The committed desktop Chrome capture shows visible shrub groups beneath the canopy and a clear arch opening.
- **Remaining:** The capture is at night. Ground cover still reads as separate clumps, and the character and quarry silhouettes need authored asset work. Daylight route and motion comparison remain open.

### 2026-11-13 - Texture quarry outcrops

- **Change:** Candidate 9b6e13da uses angled profiles, weathered footings, textured stone and mineral seams on selected outcrops.
- **Evidence:** The first mesh exceeded the existing static triangle budget. The revised profiles passed the budget and all 476 JavaScript tests. The committed desktop Chrome capture shows the textured outcrop on the right ridge.
- **Remaining:** The screenshot is a nighttime camp view. Close daylight quarry review, character assets and visual parity remain open.

### 2026-11-13 - Review armor material separation in daylight

- **Change:** Candidate 19c577ae lifts the painted steel on the adventurer chart and adds reflected sky fill after sunset using the existing texture sample.
- **Evidence:** All 476 JavaScript tests and bootJar passed. The exact desktop Chrome build rendered the camp in daylight at 06:40. Steel, leather and cloth read separately in the rear view. This capture does not verify the sunset fill.
- **Remaining:** AC-2 is open. The broad pauldrons, boot silhouette, simple masonry and sparse low vegetation still differ from the references. Compare the model in motion and capture matched daylight and night views.

### 2026-11-13 - Refine the adventurer shoulder silhouette

- **Change:** Candidate 96fef650 pulls the outer shoulder plates inward across the baked clips using rest-mesh weights.
- **Evidence:** All 476 JavaScript tests and bootJar passed. The model test verified a narrower shoulder profile across clip starts with unchanged topology and attachment coverage. The exact committed Chrome build rendered the narrower shoulders in the daylight camp view.
- **Remaining:** The desktop capture verifies the rear silhouette at rest. The full motion review, boot silhouette and AC-2 comparison remain open.

### 2026-11-13 - Refine the adventurer boot profile

- **Change:** Candidate 2a493bd6 extends the toe and heel near the sole in the baked poses without changing vertical foot contact.
- **Evidence:** All 476 JavaScript tests and bootJar passed. The regression checks toe extension and existing height through every walk frame. The committed desktop Chrome build rendered the idle scene at 09:34.
- **Remaining:** The rear idle capture mostly hides the toe. A side view and recorded walk cycle are still needed to assess the boot profile and contact in motion. Visual parity remains open.

### 2026-11-13 - Inspect the adventurer from the side in motion

- **Evidence:** Chrome rendered candidate 2a493bd6 at desktop gameplay distance in daylight. The check orbited to a side view, drove lateral movement, captured four stride frames and confirmed movement on the server. The sole and toe are visible in profile.
- **Remaining:** The side capture exposes a boxy face, sharp hair silhouette and a thin forefoot. Discrete movement frames show different poses but do not establish continuous foot contact or animation parity. ART-01, ART-03 and AC-2 remain open.

### 2026-11-13 - Taper the adventurer jaw and hair

- **Change:** Candidate 08f5d76f narrows the jaw and pulls in protruding hair points across the baked poses.
- **Evidence:** All 476 JavaScript tests and bootJar passed. Chrome captured the exact candidate from the side at rest and in four moving frames. The rear hair spikes are shorter. The face remains angular at gameplay distance.
- **Remaining:** ART-01 still needs authored facial topology and texture detail. ART-03 still needs continuous motion review.

### 2026-11-13 - Advance the walk cycle with distance

- **Change:** Candidate aa304835 advances the walk by rendered displacement for the local adventurer and nearby survivors. Full-speed cadence is retained, with slower steps at partial movement speed.
- **Evidence:** All 476 JavaScript tests and bootJar passed. Desktop Chrome captured four moving poses with server-acknowledged movement on the committed build.
- **Remaining:** Chrome covered keyboard movement. Analog input and continuous foot contact on slopes still need visual verification.

### 2026-11-13 - Verify walk phase with partial controller input

- **Evidence:** Candidate 3d964d9d passed all 477 JavaScript tests. The world test drove the normal controller-axis input and checked rendered displacement at half and full input, a stop, and a reversal. Half input advances half as far, stopping holds the walk phase, and reversing advances by distance in the new direction.
- **Remaining:** The test simulates controller axes. Physical controller play and continuous foot contact on slopes remain open under ART-03 and AC-2.

### 2026-11-13 - Blend walk starts and stops

- **Change:** Candidate 8bfcb1dd blends the local adventurer between idle and the distance-driven walk over 160 ms. Starting increases the walk weight and stopping fades the last phase toward idle.
- **Evidence:** All 478 JavaScript tests and bootJar passed. Tests cover intermediate model coordinates and start and stop weights. The committed desktop Chrome build completed the keyboard movement route and rendered four moving poses.
- **Remaining:** The Chrome check used discrete frames. Continuous contact and transition quality on slopes, remote-player transitions and a physical controller review remain open.

### 2026-11-13 - Blend nearby survivors into and out of walking

- **Change:** Candidate d8330d0a carries the 160 ms idle-to-walk blend across movement updates for nearby detailed player models. Combat poses take priority and reduced motion suppresses the walk blend.
- **Evidence:** The regression failed before the change and passed after it. It verifies the intermediate and settled blend weights as a nearby survivor starts and stops from server pose updates. All 479 JavaScript tests and bootJar passed.
- **Remaining:** The remote transition check uses a simulated observer. Two-client visual review, physical controller play and continuous foot contact on slopes remain open.

### 2026-11-13 - Observe a nearby survivor moving in a second client

- **Evidence:** Exact candidate d8330d0a ran against disposable MongoDB. Two desktop Chrome contexts shared camp. The observer received the scout's server-confirmed positions, rendered the scout mid-stride, and still showed the scout after keyboard input stopped.
- **Limits:** Still frames and server poses verify the multiplayer render path. They do not establish continuous transition timing, foot contact on slopes, or physical controller behavior. ART-03 and AC-2 remain open.

### 2026-11-13 - Align boot height with sloping terrain

- **Change:** Candidate 0cdf0219 samples terrain under the authored adventurer's boots during idle and walking. The height adjustment fades up the lower leg.
- **Evidence:** The North Gate slope regression reproduced a planted boot intersecting the ground and passed after the correction. All 480 JavaScript tests and bootJar passed.
- **Remaining:** The regression checks planted geometry against the terrain height function. Continuous in-game footage on slopes, physical controller play, and performance measurements remain open under ART-03 and AC-2.

### 2026-11-13 - Avoid inactive terrain work during actor grounding

- **Change:** Candidate aa687ef1 skips rolling-ground and ridge terms where their weight is zero and skips the channel outside its maximum reach.
- **Evidence:** The old and new height functions returned identical values at 410,881 points on a quarter-metre grid. In a local Node benchmark of 500 frames with seven authored walkers, the median of seven measured batches fell from 183.7 ms to 171.7 ms, with identical output checksums. All 480 JavaScript tests and bootJar passed.
- **Remaining:** The benchmark measures CPU-side actor mesh generation on a camp route. Browser frame times, long-session memory, multiplayer server measurements and the full AC-6 comparison remain open.

### 2026-11-13 - Compare terrain sampling in two-player Chrome

- **Evidence:** Exact baseline 0cdf0219 and candidate aa687ef1 each ran in an isolated application with disposable MongoDB. The same 1366×900 headless Chrome configuration with SwiftShader observed a second player moving back and forth in camp. The ten-second sampling window yielded 47 frame intervals per build. Baseline median/p95/p99 were 215.3/236.1/236.2 ms. Candidate values were 215.2/229.2/236.1 ms.
- **Decision:** The CPU microbenchmark improvement did not produce a clear browser frame-time improvement in this short software-rendered workload. Keep the height-equivalent optimization. AC-6 still requires hardware-rendered repeated runs, sustained memory measurements and server measurements.

### 2026-11-13 - Measure sky submission order

- **Evidence:** Exact candidate 0db5c8f1 drew the sky after opaque scenery in the existing static draw. All 480 JavaScript tests and bootJar passed. The two-player SwiftShader workload yielded 47 frame intervals with median/p95/p99 of 215.2/236.1/243.0 ms. The prior order yielded 215.2/229.2/236.1 ms in the same workload.
- **Decision:** Reverted the ordering experiment because the short run showed no clear benefit. The result does not establish a hardware GPU regression. AC-6 still requires repeated hardware-rendered profiling and sustained memory and server measurements.

### 2026-11-13 - Measure hardware-rendered two-player camp frames

- **Evidence:** Exact baseline 0cdf0219 and candidate d99b0ada ran separately with disposable MongoDB. Chrome reported ANGLE Direct3D 11 on an RTX 4070. At 1366×900, each 30-second observer run recorded 4,320 intervals with 6.9 ms median, 7.2 ms p95 and 7.2 ms p99. Peak sampled JavaScript heap was 53.68 MB baseline and 53.72 MB candidate.
- **Decision:** Frame intervals tied at the observed refresh cadence. The first and last heap samples fell at different points in garbage collection cycles, so they do not establish a memory trend. Sustained browser and server memory and the longer mixed route remain open under AC-6.

### 2026-11-13 - Compare post-collection JavaScript heap on the camp route

- **Evidence:** Exact baseline 0cdf0219 and candidate d99b0ada each ran two Chrome contexts on an RTX 4070 with an isolated application and MongoDB. The observer remained at camp while the scout repeated four ten-second movement loops. Chrome DevTools collected garbage before each heap sample. Baseline retained heap was 19.565, 19.720, 19.751, 19.733 and 19.724 MB. Candidate retained heap was 19.573, 19.839, 19.801, 19.694 and 19.703 MB.
- **Decision:** Both builds showed an initial increase followed by a plateau over the 41-second route. The sample supports short-run JavaScript retention only. Multi-minute mixed routes, native browser and GPU memory, and server capacity remain open under AC-6.
