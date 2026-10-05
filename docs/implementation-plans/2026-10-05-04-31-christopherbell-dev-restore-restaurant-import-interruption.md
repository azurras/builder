# Restore restaurant import interruption after cleanup

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Preserve thread cancellation for interrupted OpenStreetMap imports while allowing failure-state persistence and lease release to finish before the interrupt flag is restored.

## Background
A read-only source review found that `safeCategory` already recognizes `InterruptedException` and restores the interrupt flag. It does so inside the failure catch, however, before `saveState` records the failed import and before the `finally` block releases the import lease. Interruptible persistence or cleanup can therefore be cut short. The scheduled wrapper catches and logs the checked exception after `runWithLease`; it is not itself the point where the flag is lost. This plan corrects the actual ordering risk identified by inspecting the source.

## Goals
- Keep interrupted import status categorized as `INTERRUPTED` and preserve the original exception (AC-1).
- Persist failed state and release the exact lease while the thread is not yet interrupted, then restore the flag even when finalization throws (AC-1).
- Run focused and full native checks and attempt the committed application before any PR (AC-2, AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing public/manual import exception contracts or scheduled logging policy | The existing code already propagates manual checked exceptions and logs scheduled failures. |
| Changing lease semantics, retry policy, or import persistence shape | The correction only changes interrupt restoration order. |
| Creating or updating PR #1477 | The user explicitly excluded that draft as evidence. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | An interrupted import records `FAILED` with `INTERRUPTED`, preserves and rethrows the same `InterruptedException`, persists failure and releases its owned lease before setting the thread flag, and returns with the flag set. |
| AC-2 | A regression fails on the base revision, then focused and full native checks pass on the committed candidate. |
| AC-3 | The committed application runs locally against isolated test resources, or startup blocker and cleanup are recorded and no PR is created. |

## Inputs
- **Request:** User requested repository-wide Chris Street Style corrections with one implementation plan and test report for every change; draft PR #1477 is untrusted and excluded.
- **Reviewed source:** `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowService.java` and `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowServiceTest.java` at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Review refinement:** The suggested swallowed-interrupt finding was narrowed after reading `safeCategory`: the flag is restored, but too early, before failure persistence and lease release.
- **Style guidance:** `write-chris-street-style-code` Java, design/API, naming/readability, and testing/review references.

## Branch
`codex/restore-restaurant-import-interruption-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- An `InterruptedException` from an import dependency is a cancellation request and must be visible to the caller after cleanup.
- Failure-state persistence and owner-scoped release remain mandatory on the exception path.
- The application startup gate may remain blocked by the incomplete migration-015 record in isolated MongoDB `test`.

## Open Questions
None.

## Design
Make `safeCategory` a pure classifier that returns `INTERRUPTED` without mutating the current thread. In `runWithLease`, retain the caught interruption in a clearly named local variable before saving failure state. Keep rethrowing the same checked exception. In `finally`, release the lease, then restore the flag in a nested `finally` so it is restored even if release throws. Test the persisted failed state and assert both failure persistence and lease release observe an un-interrupted thread; after the call propagates, assert the same cause and a set interrupt flag, then clear the flag in test cleanup.

| Alternative | Why not |
|---|---|
| Restore the flag inside `safeCategory` | It interrupts the failure persistence and lease-release effects whose completion this workflow owns. |
| Translate the interruption to a new unchecked exception | The manual import method already exposes checked exceptions and the same exception should remain the cause and outward failure. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowService.java` | Defer interruption restoration until after lease release and keep failure categorization side-effect free. |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowServiceTest.java` | Assert failure status/category, original exception identity, un-interrupted persistence/release, and restored flag. |

## Task Breakdown
### Task 1 - Defer import interruption restoration until finalization
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowService.java`; `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowServiceTest.java`. |
| **Symbols** | `runWithLease`; `safeCategory`; interruption regression. |
| **Inspection** | Read the workflow, import failure-state writer, lease cleanup, existing workflow tests, representative callers, and repository instructions at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Behavior** | Interrupted remote/import work remains categorized and rethrown, but failure persistence and owner release complete before cancellation is exposed again. |
| **Invariants** | Preserve import states, error-category values, checked exception identity, lease identity, and retry behavior. |
| **Boundary/API** | No public signature or HTTP contract changes; scheduled execution continues to log ordinary failures. |
| **Effects and failures** | Keep Mongo persistence and lease release in their existing owner boundary; restore interruption from a nested `finally` even if release fails. |
| **Tests and evidence** | Demonstrate baseline failure when persistence/release sees the interrupt too early; candidate verifies failed state, category, same exception, cleanup order, final interrupt flag, and flag cleanup. |
| **Verification** | `:website:test --tests dev.christopherbell.whatsforlunch.restaurant.importing.RestaurantImportWorkflowServiceTest`; full website/library/browser/PowerShell/package gate; committed local app with isolated MongoDB `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused regression observes flag state during failed-state save and lease release, then checks exception identity, error category, and final interrupt flag. | Startup and exercise the committed application with the test profile and isolated resources; no production listener or data. |
| AC-2 | Focused workflow suite and full `:website:check :cbell-lib:check :website:bootJar` gate. | Run the committed packaged candidate on a free loopback port. |
| AC-3 | Confirm JAR contains the committed candidate code. | Verify meaningful readiness or record exact startup failure, database identity, process cleanup, and free port. |

Regressions and edge cases:
- Non-interruption exceptions keep existing categories and cleanup behavior.
- The same `InterruptedException` instance is propagated.
- Clear the interrupt flag in test cleanup even when an assertion fails.

## Rollback or Recovery
The correction only changes interruption timing and its focused regression. Revert the candidate commit to restore current behavior. If candidate startup stops at migration 015, stop only that candidate and leave database state untouched.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| The saved failed state or lease cleanup still runs while interrupted | Low | Assert both effects observe a clear flag in the regression. |
| The flag is not restored when lease release throws | Low | Restore it from a nested `finally`; retain a dedicated finalization edge check if test seams permit. |
| Application startup remains blocked by migration 015 | High based on current audit evidence | Record candidate and cleanup; do not bypass migration validation or create a PR. |

## Implementation Log

### 2026-10-05 - Begin implementation after source review

- **Change:** Began the published correction on an isolated candidate worktree from `origin/main` `695a3ed`; source inspection refined the reviewer note from a lost flag to premature restoration before failure persistence and lease release.
- **Reason:** `safeCategory` already recognizes `InterruptedException`, so the concrete defect is restoration timing rather than loss at `runScheduled`.
- **Impact:** Task 1 is in progress; ACs and scope are unchanged.

### 2026-10-05 - Verify and block publication on migration record

- **Change:** Candidate `2001573` defers restoring an import interruption until after failed-state persistence and lease release; the base regression failed, focused tests passed 18/18, and the full native check/package gate passed with 2,165 Java tests, 110 skipped, and no failures/errors.
- **Reason:** `safeCategory` already recognized interruption, but set the flag before cleanup; source inspection narrowed the initial reviewer note to this ordering defect.
- **Impact:** AC-1 and AC-2 are satisfied; AC-3 is blocked because committed startup on isolated database `test` stopped at the incomplete durable record for migration 015. See the [test report](../test-reports/2026-10-05-04-41-christopherbell-dev-restore-restaurant-import-interruption.md); no PR was created.

## Outcome
> [!CAUTION]
> Source correction and automated verification are complete on candidate `2001573`; application startup is blocked by the existing incomplete migration-015 durable record, so no PR was created.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Satisfied | The baseline ordering regression failed; candidate focused workflow tests passed 18/18 and prove `FAILED/INTERRUPTED`, same exception identity, un-interrupted failed-state persistence and exact lease release, and the restored flag. |
| AC-2 | ✅ Satisfied | Full `:website:check :cbell-lib:check :website:bootJar` passed; Java reported 2,165 total tests, 110 skipped, with no failures/errors. See [test report](../test-reports/2026-10-05-04-41-christopherbell-dev-restore-restaurant-import-interruption.md). |
| AC-3 | ⏸️ Blocked | Candidate JAR `2001573` targeted isolated MongoDB database `test` and failed startup on `Migration 015-require-domain-collection-schema has an incomplete durable record`; no listener remained on port 53179. No PR was created. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
