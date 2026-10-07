# Saved survivors for logged-in accounts

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> Give each logged-in account one durable survivor that resumes across sessions and server restarts, retaining temporary guest play in one shared world.

## Background
The user requested saved account characters after supply sharing shipped in PR 1490. Current main 0202b97 identifies survivors only by guest cookies and keeps the world in memory. User confirmed keeping temporary guest play.

## Goals
- Bind survivor ownership to authenticated account identity. (AC-1)
- Persist complete character and camp state with atomic gifts. (AC-2)
- Preserve temporary guests and show clear saved-character behavior. (AC-3)
- Verify locally, merge and read back automatic deployment. (AC-4)

## Non-Goals
| Not doing | Why |
|---|---|
| Import existing guest progress into accounts | Ownership adoption was not requested; account and guest identities stay distinct. |
| Multiple worlds, chat or character slots | User requested one character and one shared world. |
| Change the historical database cutover manifest | Use an explicit additive application_runtime kind, following monitor storage. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Account identity overrides guest cookies; two sessions resume one character, cannot control another, and live characters cannot be replaced by repeated joins. |
| AC-2 | Stats, combat, inventory, identities, revisions, structures and journal survive app restart; gifts persist both sides atomically; failed/conflicting saves never publish speculative state. |
| AC-3 | Guests remain cookie-owned and expire; saved inactive survivors remain durable but are excluded from active camp targeting; UI explains saving and terminal restart; account deletion removes private character ownership. |
| AC-4 | Native checks, semantic review and isolated committed-candidate runtime proof pass; published report precedes PR; required CI passes, merge and live identity readback recorded. |

## Inputs
- **Request:** One saved character per logged-in account; retain temporary guests.
- **Inspected baseline:** origin/main 0202b97b6e311d11fa665ef8edbded66988118c5; spoke AGENTS.md and root README.
- **Inspected targets:** SurviveController, Service, World, Player, Snapshot, survive.js/template, PermissionService, MongoMonitorWorkspaceRepository, DomainMongoOperationsFactory, DomainDocumentKindRegistry, KindScopedMongoOperations, DomainAccountDeletionStore and existing service/controller tests.

## Branch
codex/saved-survivors-20261006 in isolated saved-survivors worktree, base 0202b97.

## Assumptions
- Existing Spring authentication name is stable account ID, established by PermissionService and current security filter.
- Single bounded world remains appropriate; saved accounts count toward the existing 1000-character cap.

## Open Questions
None.

## Design
Store the complete bounded world in one versioned Mongo document in an explicit additive application_runtime kind. Each service operation loads a detached world, validates and mutates it under the existing monitor, then commits one optimistic replacement before returning success. Conflicts return 409 without replay; storage failures remain failures and the next request reads durable truth. One document conserves gifts without Mongo multi-document transactions and prevents competing replicas from silently overwriting each other.

Authenticated account ID is derived exclusively from Spring security and uses a separate identity namespace; it overrides guest cookies. GET resumes a previously joined saved character. POST creates the first character, returns an existing live character without replacement, or replaces a terminal character. Public IDs remain distinct from owner identifiers. Guest cookies and idle expiry remain; inactive saved characters are retained but not shown as active recipients. Saving read presence does not advance character gameplay revision. Account deletion atomically removes its embedded player and advances storage version, so concurrent world writes cannot restore it.

| Alternative | Why not |
|---|---|
| Separate player documents plus camp | Gifts and structures require distributed atomicity across documents. |
| Per-account independent game | Violates the shared-world requirement. |
| Persist only at logout | Logout/browser close is unreliable and loses acknowledged moves. |

## Expected Changes
| File or area | Change |
|---|---|
| survive model and persistence subpackage | Immutable validated persisted world/player records and repository port/Mongo implementation. |
| SurviveService/World/Player/Controller | Account ownership, detached load/commit, persistence restoration and active-presence filtering. |
| Mongo domain factory and account deletion store | Explicit additive kind approval and scoped embedded-character cleanup. |
| survive.js/template and feature README | Saved/guest explanation, terminal restart controls and durable-world contract. |
| Native tests | Persistence, auth isolation, restart round trips, concurrent writes, failure reconciliation and guest regressions. |

## Task Breakdown
### Task 1 - Save and resume account survivors
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Published reviewed plan. |
| **Files** | Inspected Survive Java files, new survive/persistence repository and model/SurviveSavedWorld; inspected Mongo domain factory/deletion store and browser files. |
| **Symbols** | Account ownership resolution, saved player/world representation, repository load/save, detached command processing and presence filtering. |
| **Inspection** | Existing files and adjacent monitor additive persistence at 0202b97. |
| **Behavior** | Resume one saved character per account while guests continue temporary play. |
| **Invariants** | Private account/cookie IDs never in API; one atomic durable state, bounded inventory/world, stale commands never replayed, no state returned as saved before commit. |
| **Boundary/API** | Existing GET/POST game/actions/gifts; authenticated identity wins over cookies; additive saved flag only. |
| **Effects and failures** | Mongo read and versioned replacement per operation; 409 stale write, storage failure not hidden; deletion removes embedded account survivor. |
| **Tests and evidence** | Red tests for account resume, ownership isolation, guest expiry, persisted gifts/combat/structures, save failure and competing writers. |
| **Verification** | Focused Java tests, touched JS syntax, JS suite and full :website:check/:website:bootJar. |

### Task 2 - Verify and deliver persistence
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 checks and semantic review pass. |
| **Files** | Builder plan, runtime report and dated delivery memory. |
| **Symbols** | Candidate identity, persisted runtime cases and acceptance outcomes. |
| **Inspection** | Existing safe test-profile runtime and report helper contracts. |
| **Behavior** | Verified saved characters ship through supported automatic deployment. |
| **Invariants** | Disposable loopback test database only; no production account fixtures; report before PR. |
| **Boundary/API** | Actual signup/login/logout and survivor API/browser on committed jar, app restart against same owned database. |
| **Effects and failures** | Owned processes cleaned up; failures diagnosed and fixes reverified. |
| **Tests and evidence** | Two accounts, separate login sessions, logout/login, guest isolation, gifts, full restart, no stale overwrite and public readback. |
| **Verification** | verify-local-app, write-test-report, publication preflight, required CI/merge and exact deployed SHA. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Auth controller tests and duplicate-account join tests | Two login cookie jars resume same account; second account and guest cannot control it. |
| AC-2 | World codec round trips, storage failure/CAS and gift tests | Perform moves/gift/build/combat, restart app and resume identical saved state. |
| AC-3 | Guest expiry, presence and account deletion tests; JS tests | Guest play remains, saved UI appears, logout/relogin resumes, no account data leaks. |
| AC-4 | Full website check/build and semantic review | verify-local-app committed jar, published report before PR, CI and production readback. |

## Rollback or Recovery
Revert via checked PR and supported deployment. Additive saved document remains untouched by a revert; older ephemeral game will not consume it. Reinstating this feature resumes it. No cutover or production data maintenance is involved.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Concurrent gifts or multiple sessions lose updates | Medium | One versioned document and stale revisions; no mutation replay. |
| Corrupt persisted values enter gameplay | Low | Validate persisted records before restoration; fail closed. |
| Saved accounts exhaust bounded world | Low | Existing 1000-character cap remains explicit; deleted accounts release slots. |

## Implementation Log
### 2026-10-06 - Persist shared world and account ownership

- **Change:** Added additive versioned world storage, detached restoration and account identity precedence while retaining guest play. Native auth test uses the real bearer filter through an explicitly configured Spring security chain, avoiding duplicate MockMvc bean-filter registration.
- **Reason:** A saved character must resume independently of guest cookies and every acknowledged command must be durable; one document preserves gift atomicity without a replica-set transaction requirement.
- **Impact:** Added saved-state, storage-failure, competing-process, BSON round-trip, deletion-version and UI regressions. Independent review identified stale commands across account replacement; replacements now advance beyond the previous character revision. Corrected a status-text encoding warning. Full native checks and committed runtime proof remain in progress.

### 2026-10-06 - Serialize Gradle verification

- **Change:** Rerun the final full check as the only Gradle verification process.
- **Reason:** An overlapping focused test invocation replaced the full suite binary output while it was running, causing a NoSuchFileException in reporting.
- **Impact:** Discard that failed full-run result; use the serial final suite and its actual XML results for evidence.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
