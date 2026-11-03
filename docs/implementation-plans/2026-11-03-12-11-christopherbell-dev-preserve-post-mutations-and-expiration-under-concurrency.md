# Preserve post mutations and expiration under concurrency

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Edits never overwrite engagement or recreate deleted posts; completed opposite like transitions leave correct counters; expiry matches current counters; cleanup cannot delete an extended root.

## Background
The user selected all nine security/concurrency findings from the November 3 scan for repair. This coupled change addresses findings 2, 4, 5 and 6 on refreshed main 5e1126f0, rather than relying on the older scan baseline.

## Goals
- Edits never overwrite engagement or recreate deleted posts; completed opposite like transitions leave correct counters; expiry matches current counters; cleanup cannot delete an extended root. (AC-1).
- Deliver verified code and records through the normal merge and deployment pipeline (AC-2).

## Non-Goals
| Not doing | Why |
|---|---|
| Unselected audit expansion or production data maintenance | The request selects the nine reported defects |
| Changing product permissions or user workflows | Preserve existing behavior except the defect |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Edits never overwrite engagement or recreate deleted posts; completed opposite like transitions leave correct counters; expiry matches current counters; cleanup cannot delete an extended root. Deterministic regression checks fail before and pass after the correction. |
| AC-2 | Candidate runs locally with isolated database test, runtime report is published, PR passes CI and merges, deployment identity is read back, and dated delivery memory is published. |

## Inputs
- **Request:** Fix findings 1 through 9 from this chat.
- **Inspected:** Refreshed main 5e1126f0; website/src/main/java/dev/christopherbell/post/editing/PostEditingService.java; post/expiration/PostExpirationService.java; post/expiration/MongoPostExpirationStore.java; post/interaction/PostInteractionService.java; post/like/MongoPostLikeStore.java; configuration/mongo/domain/KindScopedMongoOperations.java and its implementation; website/src/test/java/dev/christopherbell/post/editing/PostEditingServiceTest.java; post/PostExpirationServiceTest.java; post/like/PostLikeStoreTest.java and Mongo parity contracts; owning feature instructions and existing callers reviewed in this session and the preceding source scan.
- **Related work:** Routing, sessions, music and message UI have separate plans; these four findings share the post lifecycle and counter invariant.

## Branch
`codex/fix-scan-20261103` from `origin/main` at `5e1126f0`, isolated linked worktree. Independent changes share one reviewed delivery candidate and retain separate reports.

## Assumptions
- Existing API routes and authorization contracts remain compatible.
- Disposable exact test-profile MongoDB is available through the repository candidate helper.

## Open Questions
None. Routine implementation details are delegated to source inspection and regression evidence.

## Design
The repaired guarantee covers the selected overlapping successful operations. Crash recovery and general subtree admission redesign are not claimed solved by process-local locks or a lease. Cleanup selects and conditionally removes root posts only; reply expiration is authoritative at the root. If a new persistence field or API becomes necessary, update this log and validate the manifest rather than bypassing its allowlist.

Use targeted conditional post edits without upsert; apply commuting signed engagement deltas and derived expiry in one atomic Mongo pipeline; resolve reply expiry from its authoritative root; atomically remove only roots still due at cleanup, with descendant cleanup after that claim. Preserve existing standalone Mongo support and reject mutations when their post/root disappears. The Builder delivery contract already authorizes these corrective implementation choices and publication; no additional product decision is introduced.

| Alternative | Why not |
|---|---|
| Add a process-local mutex or disable overlapping requests | Does not establish the actual cross-request storage or late-response invariant |
| Rewrite the feature | Unnecessary compatibility and scope risk |

## Expected Changes
| File or area | Change |
|---|---|
| website/src/main/java/dev/christopherbell/post/editing/PostEditingService.java; post/expiration/PostExpirationService.java; post/expiration/MongoPostExpirationStore.java; post/interaction/PostInteractionService.java; post/like/MongoPostLikeStore.java; configuration/mongo/domain/KindScopedMongoOperations.java and its implementation and its persistence/helper interfaces and callers | Use targeted conditional post edits without upsert; apply commuting signed engagement deltas and derived expiry in one atomic Mongo pipeline; resolve reply expiry from its authoritative root; atomically remove only roots still due at cleanup, with descendant cleanup after that claim. Preserve existing standalone Mongo support and reject mutations when their post/root disappears. |
| website/src/test/java/dev/christopherbell/post/editing/PostEditingServiceTest.java; post/PostExpirationServiceTest.java; post/like/PostLikeStoreTest.java and Mongo parity contracts and adjacent native integration contracts | Deterministic reproduction and regression evidence |
| Owning feature README | Describe the corrected concurrency or boundary contract |

## Task Breakdown
### Task 1 - Correct the selected invariant
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None; coordinate shared build execution with the parent. |
| **Files** | website/src/main/java/dev/christopherbell/post/editing/PostEditingService.java; post/expiration/PostExpirationService.java; post/expiration/MongoPostExpirationStore.java; post/interaction/PostInteractionService.java; post/like/MongoPostLikeStore.java; configuration/mongo/domain/KindScopedMongoOperations.java and its implementation; website/src/test/java/dev/christopherbell/post/editing/PostEditingServiceTest.java; post/PostExpirationServiceTest.java; post/like/PostLikeStoreTest.java and Mongo parity contracts; adjacent persistence ports, callers, and feature README. |
| **Symbols** | Existing affected entrypoint and storage/browser completion functions; preserve public DTO shape. |
| **Inspection** | Current baseline 5e1126f0 implementation, affected callers and native tests; recheck all touched seams before edits. |
| **Behavior** | Edits never overwrite engagement or recreate deleted posts; completed opposite like transitions leave correct counters; expiry matches current counters; cleanup cannot delete an extended root. |
| **Invariants** | Current permissions, valid credentials, unrelated state and successful concurrent mutations remain authoritative. |
| **Boundary/API** | Preserve supported routes and response envelopes; reject invalid or stale work through existing error conventions. |
| **Effects and failures** | Own each write or asynchronous completion; propagate causal failures; never resurrect revoked/deleted state. |
| **Tests and evidence** | Add controlled failing regression first; run focused native tests then appropriate wider checks and actual candidate behavior. |
| **Verification** | Windows Invoke-Gradle.ps1 :website:check :cbell-lib:check :website:bootJar; node syntax/tests for browser changes; verify-local-app candidate proof. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused deterministic regression and affected contract tests; broader website and library checks | Exercise edited posts with concurrent likes/deletion, opposite like transitions, expiry updates and conditional cleanup in exact disposable test-profile Mongo through the candidate API and integration harness. Assert persisted final state, not just response success. |
| AC-2 | Full required checks, branch semantic review, PR/CI and merge readback | Start-Candidate.ps1 exact test profile, verify database isolation before/after, exercise changed behavior, Stop-Candidate.ps1 and listener cleanup; publish write-test-report before PR creation. |

Rerun affected local evidence after runtime-affecting edits. Record commands and outputs as executed with record_run.py. No tests or fixtures use production data.

## Rollback or Recovery
Revert the scoped commit through a verified PR if necessary. No production data migration is planned. Preserve unrelated work and never discard another session's changes.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A sibling writer or late response bypasses the correction | Medium | Trace callers and test distinct interleavings at the actual boundary |
| Unit fixtures conceal production semantics | Medium | Real Mongo/servlet/browser proof on the local candidate |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
