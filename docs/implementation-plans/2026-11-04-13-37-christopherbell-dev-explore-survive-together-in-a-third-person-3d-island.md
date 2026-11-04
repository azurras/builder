# Explore Survive together in a third-person 3D island

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Turn the website's Survive game into an explorable shared 3D island, retaining Java-owned survival and existing saved progress, and deliver through verified deployment.

## Background
The user requested an explorable 3D world, explicitly chose visible real-time multiplayer, approved expanding the browser game rather than rebuilding in an engine, and accepted the third-person island design. The current game renders an SVG camp and polls durable snapshots every five seconds; it has no positions. Current main also includes day/night, hunger, weapons, raids and saved characters, which must remain intact.

## Goals
- Walk a third-person stylized island with keyboard/mouse and touch controls. (AC-1)
- See named other survivors move live with bounded server-authoritative positions. (AC-2)
- Connect physical landmarks to existing gathering, hunting, building and escape mechanics without losing progress. (AC-3)
- Verify locally, merge after CI and confirm automatic deployment. (AC-4)

## Non-Goals
| Not doing | Why |
|---|---|
| Game-engine rebuild, npm or frontend framework | User selected expansion of existing browser game. |
| PvP, chat, procedural infinite terrain or new economy | Beyond the approved first island. |
| Durable positions | Reconnects return to camp; inventory and character progress retain existing persistence. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | /survive renders a genuine perspective 3D island, third-person survivor and follow camera; keyboard and touch movement reach distinct landmarks; fallback controls remain usable when WebGL is unavailable. |
| AC-2 | Two independent clients see distinct named survivors and live motion; Java validates identities, finite coordinates, sequence, speed, island bounds and immobile states; stale presence disappears and requests/resources are bounded. |
| AC-3 | The forest, quarry, hunting grounds, camp and shore provide contextual actions; original survival rules and saved character ownership remain authoritative, new spatial sessions cannot use actions at the wrong landmark, and refresh/restart recovers safely. |
| AC-4 | Native tests and semantic review pass, committed candidate is exercised locally with disposable test Mongo and two browser clients, report is published before PR, CI passes, PR merges and deployment is read back. |

## Inputs
- **Request:** This chat; real-time shared exploration and third-person island accepted.
- **Inspected revision:** origin/main 908a5159 in christopherbell.dev; authoritative checkout remains untouched.
- **Inspected files:** spoke AGENTS.md, README.md, survive/README.md, SurviveService, SurviveWorld, SurviveController, SurviveSavedWorld, SurviveSnapshot, SurviveServiceTest, SurviveControllerTest, survive.js, survive-scene.js, survive.html, survive.test.js, lib/api.js, SecurityConfig, RateLimitProperties, Start-Candidate.ps1 and frontend README files.
- **History:** Builder session-memory 2026-10-19 records the status-card design; current source is authoritative.

## Branch
codex/survive-3d-world-20261104 from origin/main 908a5159 in isolated managed worktree.

## Assumptions
- First island uses simple locally generated low-poly meshes and native WebGL, avoiding external assets, dependencies and build tooling.
- Live presence is process-local, matching the site's single app runtime; restarts reset locations to camp while durable survival progress remains unchanged.

## Open Questions
None. Routine visual and transport choices are implementation decisions within the approved design.

## Design
Use a low-poly island with ocean, forest, rocky quarry, hunting clearing, campfire, shelters and shoreline boats. Native WebGL renders meshes with perspective projection, depth and a following third-person camera. WASD/arrows move relative to the camera, dragging rotates it, and touch direction buttons support phones. A contextual interaction button and existing accessible menus dispatch the same Java commands. Day/night colors, structures, enemies and survivor labels reflect server state.

A separate bounded Java presence owner stores transient positions keyed only by authenticated public survivor identity resolved through SurviveService. A CSRF-protected POST pulse every 500 milliseconds while the world is visible submits sequenced desired positions and returns authoritative self and other active poses; interpolation hides transport intervals. Java bounds movement speed, time allowance and island radius. Presence does not rewrite durable world state or survivor command revisions. Existing API rate limits stay enabled. Idle poses expire after a short deadline; stale sequence cannot overwrite a newer pose. Client failures stop speculative movement and reconcile from server positions, never replaying survival mutations.

A joined 3D session opts into location rules enforced at the existing action service boundary, so direct command requests cannot bypass landmarks. Traditional controls remain available for non-WebGL clients and older clients; this compatibility path does not grant spatial rewards. Flee returns a spatial survivor to camp. Sleeping, combat and terminal survivors cannot walk. Reconnection after presence expiry respawns at camp. Positions carry no private credentials and text labels use textContent.

| Alternative | Why not |
|---|---|
| Dedicated game engine | User selected browser expansion and existing Java progress. |
| External 3D library and bundler | Native WebGL suffices for a small island and follows the no-npm repository contract. |
| Persist every movement in Mongo | Unnecessary writes and contention with atomic survival progress. |
| WebSocket infrastructure | A bounded two-Hz pulse fits the existing transport/security and first-release scale. |

## Expected Changes
| File or area | Change |
|---|---|
| survive/SurvivePresence.java and model/SurviveMovement.java | Bounded poses, movement validation and landmark rules. |
| survive/SurviveService.java and SurviveController.java | Resolve ownership, movement pulse, spatial action enforcement. |
| configuration/security/SecurityConfig.java and static/js/lib/api.js | Exact public movement route and browser API constant. |
| static/js/survive-world.js, survive-world-renderer.js, survive-world-model.js | Scene geometry, camera, input, presence transport and contextual interactions. |
| static/js/survive.js, templates/survive.html, static/css/survive.css | Mount/dispose world, state updates, responsive canvas and fallback. |
| survive Java tests and JS world tests | Identity, movement, proximity, lifecycle and input regressions. |
| Feature and frontend README files | Explain positions, controls, compatibility and resource ownership. |

## Task Breakdown
### Task 1 - Authoritative live presence and landmark commands
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | SurvivePresence.java and model/SurviveMovement.java new beside inspected SurviveService, SurviveController and model requests; update SecurityConfig, survive Java tests and survive/README.md. |
| **Symbols** | pulseForOwner, movement request/pose/view records, presence lifecycle and location permission checks. |
| **Inspection** | Service ownerKey and detached durable transactions, controller cookie/account resolution, current main action enum, security exact routes and 300/minute mutations. |
| **Behavior** | Live poses are authenticated, finite, bounded and sequenced; opted-in actions require their physical landmark. |
| **Invariants** | Durable inventory/ownership remains unchanged; no credential disclosure, speed bypass, teleport, stale pose overwrite or movement during combat/sleep/death. |
| **Boundary/API** | Add POST /api/survive/v1/movement; existing action and save contracts remain compatible. |
| **Effects and failures** | Synchronized bounded in-memory poses, no durable writes for pulses; 404 missing owner, 400 malformed movement/location and 409 stale command retain existing conventions. |
| **Tests and evidence** | Deterministic clocks cover movement, teleport, bounds, expiry, sequence, account isolation, status and landmark actions; controller tests prove public CSRF access and payload validation. |
| **Verification** | Invoke-Gradle.ps1 :website:test --tests dev.christopherbell.survive.* plus full :website:build. |

### Task 2 - Explorable third-person world and controls
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 movement/view contract. |
| **Files** | New survive-world-model.js, survive-world-renderer.js and survive-world.js beside inspected survive-scene.js; update survive.js, survive.html, survive.css, lib/api.js, frontend README files and JS tests. |
| **Symbols** | Pure landmark/movement/camera helpers, WebGL renderer, mountSurviveWorld and setState/dispose. |
| **Inspection** | Existing renderSurviveState, mountSurvive request serialization/dispose and action menus, SVG fallback and responsive adventure panel at 908a5159. |
| **Behavior** | Perspective 3D island with visible players, contextual actions and keyboard/touch exploration; server-confirmed survival state continues to drive UI. |
| **Invariants** | No gameplay reward computed in JavaScript, no HTML from names, no page-level key capture outside world, no movement when hidden, clean request/frame/listener disposal and clear unsupported/offline feedback. |
| **Boundary/API** | Existing fetchJson with exact movement route; actions dispatched through the current serialized command path. |
| **Effects and failures** | Own animation frame, GPU buffers, input listeners and bounded pulse; reconcile rejected movement and show connection failures; WebGL failure exposes existing SVG and buttons. |
| **Tests and evidence** | Pure tests detect incorrect movement, diagonal speed, landmark rules and camera transforms; lifecycle tests and two-client browser execution verify rendered behavior. |
| **Verification** | node --check on changed modules; Invoke-Gradle.ps1 :website:jsTest and :website:build; local desktop/mobile and two-client checks. |

### Task 3 - Candidate proof, publication and readback
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 and 2. |
| **Files** | This plan, Builder runtime report and dated session memory; spoke candidate reviewed as a whole. |
| **Symbols** | Acceptance evidence and delivery identities. |
| **Inspection** | verify-local-app and candidate start/stop scripts, Builder phase finalizer and spoke publication workflow. |
| **Behavior** | Deliver a locally proven candidate through CI, merge and supported automatic deployment. |
| **Invariants** | Disposable test database only; preserve unrelated work; report before PR; no bypassed checks. |
| **Boundary/API** | Public /survive and movement/action endpoints; deployment actuator readback. |
| **Effects and failures** | Own candidate process and Mongo cleanup; repair failed checks and preserve incomplete state honestly if external access blocks delivery. |
| **Tests and evidence** | Two independent survivors, visible movement, gathering near trees, blocked teleport, reconnect, phone controls and original status/actions. |
| **Verification** | Start-Candidate.ps1 and Stop-Candidate.ps1; preflight_spoke_pr.py; wait_for_github.py queue and deployed. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | JS movement, projection and landmark tests; syntax and full jsTest. | verify-local-app desktop and phone browser renders genuine 3D, follows movement and offers accessible fallback. |
| AC-2 | Java deterministic identity, validation, speed, sequence, expiry and status tests; controller CSRF tests. | Two separate browser identities see named moving avatars; malformed and teleport requests are rejected/reconciled. |
| AC-3 | Spatial action and saved-service regressions plus complete :website:build. | Walk to forest/quarry/hunt/shore, exercise contextual command and compare inventory/revisions with server; refresh preserves progress and returns safely. |
| AC-4 | Hub validation and spoke PR preflight with report naming candidate. | Run committed candidate using verify-local-app with disposable loopback Mongo database test, record inputs/results as run, clean up, publish report before PR, CI/merge/deployment readback. |

- Rerun affected local proof after runtime-affecting edits before PR publication or update.
- Verify tab hiding, focus, resize, lost WebGL context, stale movement and failed request recovery.

## Rollback or Recovery
Revert the spoke change through a checked PR. No saved-world schema changes are required; old progress remains readable. Presence is disposable and resets on restart. Stop only owned candidate and Mongo processes using the repository helper.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Low-powered device cannot render WebGL | Medium | Bound geometry/pixel ratio and keep existing accessible SVG/action fallback. |
| Latency makes players jump | Medium | Local prediction, bounded server correction and remote interpolation. |
| Presence and durable revisions interfere | Medium | Separate pose sequence from survival revisions and avoid movement persistence. |
| Large shared-IP groups hit existing rate limit | Medium | Two pulses/second per active client, pause hidden tabs and back off visibly on failure; do not weaken limits. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
