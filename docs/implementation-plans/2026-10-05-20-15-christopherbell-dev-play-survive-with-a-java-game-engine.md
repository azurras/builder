# Play Survive on the website with a Java game engine

## Document Status
complete

## Objective
> [!IMPORTANT]
> Deliver a public interactive Survive game at /survive, implemented in Java and verified locally and after automatic deployment.

## Background
The user requested a playable website adaptation of azurras/survive and explicitly required Java. The inspected Python master is 24d50be92e1609e6e983b7dda9231bd77777b3d1. It implements wood gathering, progression, inventory, construction and attack; defend/run and food acquisition are unfinished.

## Goals
- Visitors can play without an account using Java-owned rules and separate survivors in one shared world. (AC-1)
- The original mechanics become a complete playable loop. (AC-2)
- Accessible controls fit the existing website and expose clear feedback. (AC-3)
- Publish and verify the merged deployment. (AC-4)

## Non-Goals
| Not doing | Why |
|---|---|
| Chat, matchmaking, leaderboards, permanent saves | Not requested; avoid database and account coupling. |
| Changes to the Python repository | The requested target is the website. |
| New frontend framework | The website uses vanilla modules. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Java owns all gameplay; anonymous CSRF-protected APIs isolate survivors within one shared world, validate inputs, cap capacity and expire inactive state. |
| AC-2 | Gathering has 50 percent success, inventory caps at ten, strength/stamina advance, shelter costs five wood, boat costs ten, hunting finds fresh hogs, attack/defend/flee/eat/rest/escape and restart work, death and escape end actions. |
| AC-3 | /survive provides keyboard-operable mobile controls, stats, inventory, bounded narrative feedback, instructions, source attribution and a navigation entry. |
| AC-4 | Native checks and semantic review pass, committed candidate runs with disposable test MongoDB, report is published before PR, PR merges after CI and production serves the game. |

## Inputs
- **Request:** Play the linked game on christopherbell.dev; implement in Java.
- **Inspected source:** Python controllers and player, inventory, attribute and hog models at source master above; existing local develop checkout has unrelated edits and remains untouched.
- **Inspected website:** ef15adc000e0e363e91ee7d9df3ddb19c4ff88d6; AGENTS.md, README.md, ToolsViewController, view README, SecurityConfig, PublicSitemapService, zip-coordinates template, app.js, components/nav.js, lib/api.js, lib/util.js, ViewControllerTest, SecurityConfigTest and nav tests.
- **History:** Latest project entries in Builder docs/session-memory/2026-10-05.md; production deployment is automatic after verified main CI.

## Branch
codex/survive-java-20261005 from origin/main ef15adc0 in an isolated worktree.

## Assumptions
- One shared in-memory world per application process is sufficient for this multiplayer foundation; survivor identity expires after two idle hours and server restart resets the world, disclosed on the page.
- Completing listed but unfinished actions serves the requested playable adaptation.

## Open Questions
None.

## Design
Use a focused survive feature: a single Java SurviveWorld aggregate containing separate SurvivePlayer objects, a shared camp and shared bounded event log, with enums and immutable snapshots, a synchronized bounded service with opaque random tokens and injected clock/randomness for tests, and a thin controller. A private SameSite cookie scopes identity to the API. GET returns the current game or no content without creating state; POST starts/restarts and performs validated enum actions. Existing CSRF and rate limits remain. Keep up to 1000 players with two-hour idle expiry and bounded logs. Shared shelters allow every survivor to rest; boats are camp resources consumed when one survivor escapes. Each player retains private inventory, skill progression and fresh personal combat encounters. A survivor restart replaces only that survivor and preserves the world. Poll current snapshots every five seconds while visible to display shared camp changes. Each mutation requires the latest survivor revision to reject stale double submissions across tabs; browser controls serialize requests. No automatic mutation retries. The existing tools controller serves the page; method-specific public matchers expose only this shell and exact game endpoints. Frontend renders strings with textContent. Complete missing original actions with defend reducing damage, flee ending combat with one damage, hog victory granting food, eating consuming food and restoring capped health, shelter enabling rest and boat enabling escape. Preserve original starting values, gathering probability and exponential experience thresholds; cap progression to keep arithmetic bounded. Include source and GPL attribution with the original license asset.

| Alternative | Why not |
|---|---|
| JavaScript game engine | User explicitly requires Java. |
| Launch Python per visitor | Wrong language and unnecessary process ownership. |
| MongoDB permanent saves | Adds schema/account persistence beyond request. |

## Expected Changes
| File or area | Change |
|---|---|
| survive Java package and tests | Domain engine, snapshots, bounded service and controller contracts. |
| view/tools/ToolsViewController.java and view/README.md | Public /survive page route and documentation. |
| configuration/security/SecurityConfig.java and configuration/PublicSitemapService.java | Exact public API/page routes and sitemap. |
| templates/survive.html, static/js/survive.js, static/css/survive.css | Responsive interactive game. |
| static/js/lib/api.js and components/nav.js | API paths and discovery. |
| static/js/README.md, static/css/README.md, security/README.md | Ownership and access documentation. |
| static/licenses/survive-GPL-3.0.txt | Upstream attribution license. |
| Java view/security/sitemap tests, architecture/LegacyModuleDependencyRules.java and JS tests | Integration, access and rendering behavior. |

## Task Breakdown
### Task 1 - Implement the Java gameplay and bounded browser service
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | New survive/SurviveWorld.java, survive/SurvivePlayer.java, survive/model/SurviveAction.java, survive/model/SurviveSnapshot.java, survive/model/SurviveRequests.java, survive/SurviveService.java, survive/SurviveController.java, survive/README.md; neighboring tools controller and security configuration inspected above. |
| **Symbols** | World and survivor transitions, immutable snapshot, token lifetime, player revision and controller DTOs. |
| **Inspection** | Python master controllers/models and website ef15adc0 security CSRF/matchers and frontend fetchJson. |
| **Behavior** | Server-authoritative shared playable world with bounded players and clear rejection. |
| **Invariants** | Health and inventory bounded, fresh enemy each hunt, no survivor actions after death/escape, private tokens never exposed, no production data access. |
| **Boundary/API** | GET /api/survive/v1/game, POST /api/survive/v1/game and POST /api/survive/v1/actions with private cookie and revision. |
| **Effects and failures** | In-memory mutation under service lock; missing/expired token returns 404, stale revision 409, malformed request 400, capacity 503; GET absence 204. |
| **Tests and evidence** | Deterministic Java transitions, isolation, expiry/capacity, stale actions, HTTP validation and CSRF/access coverage. |
| **Verification** | Gradle :website:test with focused survive/view/security tests, then full :website:check and :website:bootJar. |

### Task 2 - Integrate the playable page and discovery
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 API contract. |
| **Files** | Expected frontend, route, security, sitemap, documentation, attribution and test files above. |
| **Symbols** | Page renderer, serialized action requests, game action controls, navigation items and public matchers. |
| **Inspection** | Existing zip-coordinates template, app bootstrap, util.fetchJson, toolsMenuItems, sitemap and tests at ef15adc0. |
| **Behavior** | Start, act, refresh/resume, restart, readable outcomes on desktop and mobile without login. |
| **Invariants** | JavaScript contains no game rules; no untrusted innerHTML; errors visible and controls recover; no hidden game API writes. |
| **Boundary/API** | Use lib/api.js and fetchJson; disable controls while pending and retain revision; warn on uncertain mutation failure and allow reload. |
| **Effects and failures** | Browser requests only; no localStorage game secrets; network failure surfaces feedback and refresh recovers authoritative state. |
| **Tests and evidence** | JS rendered snapshot and request/error tests, Java routes and public method boundary tests. |
| **Verification** | node --check touched JS; Gradle :website:jsTest; browser play on local candidate including narrow viewport and restart. |

### Task 3 - Verify, publish and read back deployment
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 and 2 pass checks and semantic review. |
| **Files** | Builder plan, runtime report, dated session memory and respective indexes. |
| **Symbols** | Candidate identity, runtime cases and acceptance outcomes. |
| **Inspection** | Website isolated MongoDB README and Builder publication/preflight helpers. |
| **Behavior** | Verified candidate merges and the automatically deployed game is playable. |
| **Invariants** | Publish runtime proof before PR, keep production running, preserve unrelated checkouts. |
| **Boundary/API** | Supported automatic deployment after main CI; public non-destructive readback. |
| **Effects and failures** | Owned disposable MongoDB/application processes cleaned; CI failures diagnosed and fixed; publication failures retain commits. |
| **Tests and evidence** | Report includes isolation, API responses, actual browser play, cleanup, candidate SHA and deployed identity. |
| **Verification** | verify-local-app, record_run.py, preflight_spoke_pr.py, CI wait/merge and live deployment identity. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Java service/controller tests and SecurityConfigTest | Two cookie jars with separate survivors and shared camp, no-CSRF denial, invalid/stale actions and no-store responses. |
| AC-2 | Deterministic domain transition tests | Gather, craft, combat, eat, rest, escape/death and restart through API and browser. |
| AC-3 | View, nav and JS rendering/request tests, syntax checks | Anonymous rendered page and keyboard/mobile browser play with feedback. |
| AC-4 | Full website check, semantic diff review and CI | verify-local-app on committed candidate using exact test profile and disposable loopback MongoDB; report before PR; production identity and game readback. |

After runtime-affecting edits rerun affected checks and local verification before PR creation/update. Exercise unknown actions, insufficient materials, full inventory, terminal states and stale revisions. Record commands and HTTP evidence with record_run.py as executed.

## Rollback or Recovery
Revert the merged feature through a verified PR and the supported automatic pipeline. No database migration or durable game data exists. Server restart naturally discards the world; disclose that behavior in the page.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Anonymous state exhaustion | Medium | Fixed capacity, idle expiration and existing rate limiting. |
| Lost responses or duplicate tabs | Medium | Revision precondition, serialized controls, no mutation retry and resume read. |
| Unfinished original gameplay | Known | Document completed actions and test each branch. |

## Implementation Log
### 2026-10-05 - User requires a multiplayer foundation
- **Change:** One authoritative world with separate survivors, shared camp structures and recent events replaces independent browser games.
- **Reason:** User requested a single game state and selected separate survivors in the same world.
- **Evidence:** Direct user instructions in this chat.
- **Impact:** Shared world state and separate survivors are the acceptance boundary; no database persistence is introduced.
- **Validation:** Tests will prove two survivors share camp construction while retaining private inventory, health and revision; restarts preserve other players and camp.

### 2026-10-05 - Implement shared world and fix browser lifecycle review finding

- **Change:** Implemented a single SurviveWorld with separate survivors, shared shelter/boat counts, 30 recent events, server-owned allowed actions and revisions, exact anonymous CSRF-protected routes, a vanilla display-only UI and source license attribution. Registered the new survive area in the architecture catalog and updated its sitemap/navigation coverage.
- **Reason:** The user explicitly requires Java and a shared game state with separate survivors. Existing architecture checks require every new area to be cataloged. Completing unfinished mechanics makes the requested game playable.
- **Impact:** No database/schema changes. In-memory world survives character replacement but resets on process restart; fixed bounds limit players, structures, names and events. Skill progression caps strength at 20. Browser Back retains controls when the document is cached.
- **Evidence:** Initial tests failed on absent implementation/routes; the Java model tests now pass. Independent reviewer found the pagehide/back-forward-cache lifecycle defect; it was corrected with a regression. Native Gradle tests needed JAVA_TOOL_OPTIONS as well as GRADLE_OPTS so child JVMs use the short socket directory. Full checks are running; runtime proof remains required before PR.

### 2026-10-05 - Refresh candidate after main advanced

- **Change:** Merged current origin/main into the work branch after CI passed but merge was refused by the up-to-date branch requirement; candidate is now 6bf3c148.
- **Reason:** Preserve all required checks without bypassing branch protection. Incoming changes only concern photography.
- **Impact:** Full website checks and actual isolated API/browser runtime proof repeated on the new jar; all passed. Updated runtime report before pushing the refreshed candidate.

## Outcome
> [!TIP]
> Delivered and verified live at [Play Survive](https://www.christopherbell.dev/survive). [PR #1489](https://github.com/azurras/christopherbell.dev/pull/1489) merged candidate 6bf3c148 as a42d4b8e5af103d3c91fdcbb3cc943ca8bb8402f after every CI check passed. Main CI passed and automatic deployment readback reports that exact active revision, UP_TO_DATE and HEALTHY.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Java-owned single shared world, private survivors, bounded state, CSRF and revision checks | [Runtime report](../test-reports/2026-10-05-20-35-christopherbell-dev-shared-java-survive-world.md), service/controller tests and PR |
| AC-2 | ✅ Complete gathering, crafting, combat, food, rest, escape/death and survivor replacement | Deterministic model tests and two-survivor actual API playthrough in report |
| AC-3 | ✅ Responsive keyboard-operable page, stats, inventory, camp journal, guide, attribution, navigation | Browser play, mobile/desktop layout and lifecycle evidence in report; verified live join form with no console errors |
| AC-4 | ✅ Checks, review, candidate runtime, report publication, merge and deployment readback complete | Full checks twice, 386 final JS tests, all PR checks successful, public build identity a42d4b8 and read-only live checks |

Live readback on 2026-10-05 at 21:16 CDT verified build identity, readiness, /survive, anonymous game GET 204, JS/CSS, sitemap and GPL license. The generic Python user agent was denied 403 by the public edge; the ordinary browser and browser-user-agent requests succeeded. No production survivor or fixture was created. Separate game states are not persisted: one in-memory world per server process resets on restart; distributed replicas need durable shared state before scaling.

Owned test processes stopped and ports closed, remote/local task branch deleted and owned worktree removed. Temporary logs/screenshots and disposable database files are retained because automatic approval review rejected recursive cleanup. No source issue; external closure does not apply.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
