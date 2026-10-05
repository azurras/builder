# Limit Anonymous Identity Fallback to Missing Authentication

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Public post and restaurant reads should use anonymous defaults only when authentication is absent, while unexpected identity lookup failures remain visible.

## Background
`PostService.getSelfIdOrNull()` and `RestaurantService.getSelfIdOrNull()` catch every `Exception` and convert it to anonymous identity. `PermissionService.getSelf()` defines missing authentication as `IllegalStateException`, and the restaurant service documents anonymous preference defaults. The broad catches can conceal defects as normal anonymous reads.

## Goals
- Limit both anonymous fallbacks to the explicit missing-authentication exception (AC-1).
- Prove anonymous behavior remains stable and unexpected failures propagate (AC-2).
- Run the packaged application on the permitted isolated database `test`, then complete separate PR delivery (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change public feed or restaurant preference payloads | Current anonymous behavior is an established contract. |
| Change authentication policy or `PermissionService` | This correction is limited to the two anonymous-read callers. |
| Bundle other broad-catch cleanups | Each independent correction gets its own plan and report. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Both fallback helpers catch only `IllegalStateException` from identity lookup. |
| AC-2 | Focused tests show anonymous defaults remain and unrelated runtime failures propagate; affected native test classes pass. |
| AC-3 | Candidate startup and a representative route pass using database `test`, a complete test report is published, and the reviewed PR merges with supported deployment health readback. |

## Inputs
- **Request:** Whole-codebase Chris Street Style audit with targeted corrections and a separate plan/report for each; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** Both fallback helpers and `PermissionService.getSelf()` at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected tests:** `PostServiceTest`, `RestaurantServiceTest`; existing coverage confirms anonymous preference defaults.
- **Guidance:** Website `AGENTS.md` and Builder Chris Street Style naming, Java, design/API, and testing references.
- **Baseline:** Both affected test classes passed before edits on the isolated candidate worktree.

## Branch
`codex/anonymous-identity-fallback-20261005` from website `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- `IllegalStateException` from `PermissionService.getSelf()` means authenticated identity is unavailable for these calls.
- Other runtime exceptions indicate defects or operational failures and must not become anonymous results.

## Open Questions
- Isolated MongoDB database `test` currently lacks the active domain cutover ledger required by migration 015. Runtime proof and PR creation wait for a supported fixture or provisioning procedure; direct database writes and migration bypasses are prohibited.

## Design
Catch only the exact exception used by `PermissionService.getSelf()` to represent missing authentication. Add focused regressions that retain anonymous behavior and reject unrelated failures at both service boundaries.

| Alternative | Why not |
|---|---|
| Keep catching `Exception` and rely on logging | Failures remain converted into plausible anonymous responses. |
| Catch all `RuntimeException` | It still conflates missing authentication with programming and infrastructure failures. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/post/PostService.java` | Narrow the public-feed identity fallback to `IllegalStateException`. |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java` | Narrow anonymous preference identity fallback to `IllegalStateException`. |
| `website/src/test/java/dev/christopherbell/post/PostServiceTest.java` | Characterize anonymous identity and unexpected failure propagation. |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java` | Preserve anonymous defaults and verify unrelated failures propagate. |

## Task Breakdown
### Task 1 - Narrow missing-authentication fallbacks
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the two services, `PermissionService`, and their native test classes in a clean worktree from `origin/main`. |
| **Symbols** | Both `getSelfIdOrNull()` helpers and focused service tests. |
| **Inspection** | Base `695a3ed8617f9b4ab07abb7413baf369c58acf6`; baseline command passed both affected test classes. |
| **Behavior** | Anonymous public reads remain available; unrelated identity failures propagate. |
| **Invariants** | No authentication, API, or persistence contract changes; only explicit missing identity selects anonymous behavior. |
| **Boundary/API** | Public service signatures and response shapes stay unchanged. |
| **Effects and failures** | No new I/O; expected absence is handled locally and other failures remain visible. |
| **Tests and evidence** | Add regressions that fail with the broad catches, then run focused service classes and full module checks. |
| **Verification** | Focused Gradle tests, `:website:check :cbell-lib:check`, final diff review, and verify-local-app startup/readiness plus a representative route on isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review both catch clauses and the identity source contract. | Start the candidate on isolated database `test`. |
| AC-2 | Focused `PostServiceTest` and `RestaurantServiceTest`, then full module checks. | Candidate readiness and a representative public route succeed. |
| AC-3 | Required CI and merge readback. | Publish actual candidate runtime evidence and confirm supported deployment health for the merge SHA. |

Regressions: missing identity continues to produce anonymous results/default preferences; unrelated runtime exceptions from either identity lookup propagate unchanged.

## Rollback or Recovery
Before merge, revert only this isolated correction if behavior or checks regress. After merge, use a reviewed revert PR and supported automatic deployment; do not edit production data or restart services manually.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| An expected missing-identity path uses another exception | Low | Confirmed the exact `PermissionService.getSelf()` contract and existing anonymous test. |
| Candidate runtime remains blocked by the missing ledger | High | Keep the candidate unpushed until a supported `test` fixture is available. |

## Implementation Log

### 2026-10-05 - Record focused verification and runtime blocker

- **Change:** Added regressions for post and restaurant identity failure propagation, narrowed both fallbacks to `IllegalStateException`, and committed candidate `0838538`. Focused service tests and full module checks pass; the candidate JAR fails startup on the required `test` database at migration 015. The blocked [test report](../test-reports/2026-10-05-00-29-christopherbell-dev-limit-anonymous-identity-fallback-to-missing-authentication.md) records the exact evidence.
- **Reason:** The `test` database has no active domain cutover ledger and its existing migration-015 record is `FAILED`; the application refuses to retry the incomplete durable record. Direct writes and guard bypass are prohibited.
- **Impact:** AC-1 and AC-2 are met. AC-3 and PR creation are blocked pending a supported test fixture or recovery procedure.

## Outcome
> [!WARNING]
> The identity fallback correction is implemented and native checks pass. Candidate startup and PR creation are blocked because the required isolated `test` database lacks the active domain cutover ledger and contains a failed migration-015 record.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Both helpers catch only `IllegalStateException` in candidate `0838538`. |
| AC-2 | ✅ Met | 89 focused tests passed; full module checks passed with 2,166 Java tests, 0 failures/errors and 110 skips. See the [test report](../test-reports/2026-10-05-00-29-christopherbell-dev-limit-anonymous-identity-fallback-to-missing-authentication.md). |
| AC-3 | ⏸️ Blocked | The committed candidate stopped at migration 015 before readiness; a supported test fixture or recovery procedure is needed. No PR was created. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
