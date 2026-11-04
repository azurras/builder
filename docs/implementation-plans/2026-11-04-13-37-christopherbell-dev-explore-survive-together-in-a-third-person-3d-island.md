# Explore Survive together in a third-person 3D island

## Document Status
complete

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
| configuration/security/SecurityConfig.java, its README.md and static/js/lib/api.js | Exact public movement route and browser API constant. |
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

### 2026-11-04 - Begin approved island implementation

- **Change:** Started implementation in the managed worktree after independent design/plan review reported ready; initial behavioral tests expose missing movement and 3D model components.
- **Reason:** The user approved the third-person shared island. Review identified timeout, stale sequence, per-IP backoff and non-writing presence requirements, which are retained in implementation.
- **Impact:** The authoritative checkout remains untouched. Pulse uses read-only ownership resolution, adaptive backoff and explicit sequence reconciliation; survival commands retain durable atomicity.

### 2026-11-04 - Implement island and recoverable presence

- **Change:** Added an authenticated movement/leave fallback route, controller/service regression coverage and the native 3D world modules. Early checks passed four presence tests and 434 JavaScript tests; subsequent expanded checks exposed a CSRF-test fixture ordering dependency and a fake-DOM canvas capability mismatch, both corrected without weakening assertions.
- **Reason:** Graphics loss must release only the caller's transient pose so accessible text controls remain usable. Reviewer requirements also prompted bounded aborts, adaptive shared-IP backoff, sequence reconciliation and physical command checks under the service lock.
- **Impact:** No stored schema changes. Flee relocation occurs after durable commit. World rendering preserves status-card and SVG fallback behavior; test-only context isolation now prevents movement CSRF setup from contaminating the original cookie test.

### 2026-11-04 - Review and developmental layout findings

- **Change:** Independent implementation review found stale remote avatars after movement outages; a new lifecycle regression failed with six labels instead of five, then passed after clearing disconnected poses. Seven world tests now pass, including abort/dispose, prediction, projection, landmark filtering and fallback. A developmental browser layout check confirmed genuine perspective 3D and exposed SVG hidden-property incompatibility, corrected with the actual hidden attribute and a regression.
- **Reason:** Runtime and independent review must establish visible behavior, not only successful compilation. The layout run was developmental on the earlier packaged artifact and is not the final committed-candidate proof.
- **Impact:** Developmental candidate and disposable Mongo were stopped, both ports read back with zero listeners and owned temporary paths removed. The final candidate still requires fresh packaging, committed runtime verification, published report and delivery. The security README now includes both exact movement routes.

### 2026-11-04 - Prove committed candidate locally

- **Change:** Candidate 3eb9788e passed the full :website:build (2199 Java tests, zero failures/errors, 126 configured skips), all 438 JavaScript tests, Checkstyle and Windows Pester gates. Repackaged the committed candidate and verified its actuator build identity. Local API checks and independent Chrome/IAB browser sessions proved movement, physical action guards, sequence/teleport rejection, forest gathering, quarry, hunting, defend/flee, phase change, refresh preservation, player departure and phone-sized held pointer/keyboard controls.
- **Reason:** The user-facing multiplayer and 3D claims require actual rendered and cross-client evidence on the proposed commit. The scratch API probe initially requested protected /actuator/health; corrected it to the documented public readiness route, retained the failed attempt and passed the corrected probe without changing product code.
- **Impact:** Runtime uses only disposable loopback Mongo database test. Both browser test tabs closed and viewport override reset. Native database-contract skips are recorded, not represented as passes. Runtime report is being saved/published before PR creation.

### 2026-11-04 - Publish candidate and start deployment-aware merge queue

- **Change:** Published the complete eight-case runtime report on Builder main in 7fe4464, passed the candidate-specific spoke preflight, pushed 3eb9788e and opened christopherbell.dev PR #1558. Trusted-comment triage found no requested changes. Started the supported deployment-aware merge queue for PR 1558 after confirming production serves current main 908a515.
- **Reason:** The authorized delivery includes required CI, merge and supported automatic deployment; no handoff or separate merge approval is needed.
- **Impact:** Waiting on CI/deployment through the bounded queue helper. The code and verification are complete; merge and production readback remain outstanding.

### 2026-11-04 - Merge verified island after green CI

- **Change:** PR #1558 merged as 7b91e7697621c4480a7f52174082f6d23e97b190 with head 3eb9788e7acefddec1a9a113751d607101f3273c. Readback shows MERGED. Build, dependency-review, CodeQL and all language analyses passed; Windows build took 8m37s.
- **Reason:** Required checks passed on the reviewed, locally proven candidate, and the deployment-aware queue released the merge only after production served its previous main head.
- **Impact:** The supported automatic deployment of the merged main commit is now pending. The bounded queue continues until production serves the merge; no direct deployment or production-data changes are being performed.

### 2026-11-04 - Pass merged-main CI and clarify skipped checks

- **Change:** The merged main commit's CI Build run 41904580163 completed successfully. Native-check skip classification was read back from XML: 123 Mongo contract/integration cases and 3 platform/environment-specific filesystem cases; corrected the report's earlier overly broad skip description.
- **Reason:** Production release is CI-gated on the merged commit, and evidence must distinguish actual passes from configured skips accurately.
- **Impact:** The deployment-aware queue is still checking live commit identity. GitHub's Gradle cache-save annotations were non-blocking warnings; the build and tests succeeded. No runtime or product-code changes were made after candidate verification.

### 2026-11-04 - Verify live island and complete delivery

- **Change:** Production now serves exact merge 7b91e7697621c4480a7f52174082f6d23e97b190. The deployment-aware queue exited 0; independent read-only smoke checks returned 200 for the page and four game modules with candidate-matching content, and 204 for anonymous game GET. Recorded all acceptance criteria as met.
- **Reason:** Successful merge alone was insufficient; delivery required live commit and served-behavior readback after the supported automatic deployment.
- **Impact:** Delivery is complete with the documented first-release limits. Local candidate/Mongo and browser cleanup passed. Final plan, corrected skip accounting and dated memory are being published; no source issue requires external closure.

### 2026-11-04 - Read back workspace cleanup protection

- **Change:** Deleted the merged remote feature branch and verified the local worktree has no modified files. The native app refused archive_worktree with: The task's primary checkout cannot be removed.
- **Reason:** The worktree created for this delivery is now the chat's protected primary checkout. Removing it manually would work around the app's protection, so the clean checkout is retained.
- **Impact:** Product delivery remains complete and live, all Builder records are published, and candidate/Mongo/browser cleanup passed. Only the clean app-owned checkout remains; no unrelated checkout was changed or removed.

## Outcome
> [!TIP]
> Delivered and live. [PR #1558](https://github.com/azurras/christopherbell.dev/pull/1558) merged as `7b91e7697621c4480a7f52174082f6d23e97b190`; production reports that exact commit.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | Met: generated perspective 3D island, following third-person camera, keyboard, held pointer and destination movement; responsive layout and accessible fallback. | [Runtime report](../test-reports/2026-11-04-14-03-christopherbell-dev-shared-3d-survive-island.md), cases 4-6; seven world regressions and real desktop/phone rendering. |
| AC-2 | Met: independent Chrome and IAB survivors observed each other moving; ownership, finite coordinates, speed, sequence, expiry and status rules enforced by Java. | Runtime report cases 3 and 5; presence/service/controller tests; stale-avatar failure reproduced and corrected, then independent review confirmed no remaining blockers. |
| AC-3 | Met: forest, quarry, hunting grounds, camp and shore provide contextual actions while durable survival and existing saves remain intact. | Runtime report cases 3, 5-7: wood gathering, stone gathering, hunt, defend, flee, day/dusk, refresh inventory and departure; native saved-service regressions pass. |
| AC-4 | Met: committed local proof was published before PR; native checks, PR and merged-main CI passed; merge and automatic deployment verified. | Candidate `3eb9788e`, Builder report checkpoint `7fe4464`, PR #1558, merge `7b91e76`, CI Build runs 41903051616 and 41904580163, deployment-aware queue exited 0, production smoke readback below. |

Production GET checks returned 200 for `/survive` and all four game modules. After normalizing line endings, their contents match the verified candidate: survive.js `9ce628684b06297a`, survive-world.js `b09c3ec9bb312f3c`, survive-world-model.js `9b1d5c25795ac58b`, survive-world-renderer.js `6c9cc3d9859b79ff` (SHA-256 prefixes). Anonymous game GET returned 204 without creating a survivor. Production verification sent GETs only.

Local build: 2199 Java tests, zero failures/errors and 126 configured skips (123 Mongo cases and 3 filesystem/environment cases); all 438 JS tests and Windows Pester/Checkstyle gates passed. Both candidate processes and disposable Mongo listeners were stopped and owned directories removed; browser tabs closed and viewport override reset.

Accepted first-release limits remain those in Design/Risks: transient positions, one application process and existing per-IP rate limits with visible backoff. No source issue; external closure does not apply.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
