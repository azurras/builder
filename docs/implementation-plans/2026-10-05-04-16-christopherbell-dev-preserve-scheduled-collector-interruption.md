# Preserve interruption in scheduled collectors

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Preserve Java thread cancellation when scheduled collector work is interrupted, while recording the failed run and releasing its lease.

## Background
The review of `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6` found that `ScheduledCollectorCoordinator.Work.execute` permits checked exceptions, but `run()` handles `InterruptedException` in its generic checked-failure branch. The exception clears the thread interrupt flag; the coordinator records failure and releases the lease, but downstream shutdown/cancellation no longer sees the signal. Multiple collectors share this boundary.

## Goals
- Restore the thread interrupt flag when collector work throws `InterruptedException` (AC-1).
- Preserve the existing failed-run outcome, diagnostic cause, and exact lease release (AC-1).
- Run focused and full native checks and attempt the committed app before any PR (AC-2, AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing collector API checked-exception contracts | The existing `Work.execute` contract already allows checked failures. |
| Altering error categories or collector retry policy | Keep the correction limited to interruption preservation. |
| Creating or updating PR #1477 | The user explicitly excluded trust in that draft. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Interrupted work is durably marked failed, the thrown wrapper retains the same interruption as its cause, the thread's interrupt flag is restored, and the owned lease is released. |
| AC-2 | The baseline interruption regression fails, then focused and full native checks pass on the committed candidate. |
| AC-3 | The committed app runs locally against isolated test resources, or a startup blocker and cleanup are recorded and no PR is created. |

## Inputs
- **Request:** User requested whole-codebase Chris Street Style corrections with a separate plan and test report for every change; draft PR #1477 is untrusted.
- **Reviewed source:** `cbell-lib/src/main/java/dev/christopherbell/libs/lease/ScheduledCollectorCoordinator.java`, `cbell-lib/src/test/java/dev/christopherbell/libs/mongo/lease/ScheduledCollectorCoordinatorTest.java`, and `cbell-lib/README.md` at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Callers:** Canes index, Music catalog/metadata, VIN enrichment/import, and restaurant collectors use the shared coordinator.
- **Style guidance:** `write-chris-street-style-code` Java, design/API, naming/readability, and testing/review references.

## Branch
`codex/preserve-scheduled-collector-interruption-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- `InterruptedException` means the current collector thread is asked to stop and should remain interrupted when control returns to its owner.
- Existing run persistence and lease-release behavior remains part of the failure contract.
- Application runtime verification may remain blocked by the existing incomplete migration in the isolated `test` database.

## Open Questions
None.

## Design
Add a dedicated `InterruptedException` catch before the generic checked-exception branch. Restore `Thread.currentThread().interrupt()`, persist status `FAILED` with the existing safe category, and throw the same `IllegalStateException` wrapper used for other checked failures while retaining the original cause. Leave final status persistence and lease release in the existing `finally` block. Test the observable wrapper, persisted run state, release, and thread flag, clearing the flag in a test `finally` block.

| Alternative | Why not |
|---|---|
| Rethrow checked interruption from `run()` | Would change the public caller contract and require every scheduled collector to handle a checked exception. |
| Swallow interruption after persisting failure | Loses the cancellation signal and lets scheduled work continue as though the thread were not interrupted. |

## Expected Changes
| File or area | Change |
|---|---|
| `cbell-lib/src/main/java/dev/christopherbell/libs/lease/ScheduledCollectorCoordinator.java` | Restore interruption before returning the established checked-failure wrapper. |
| `cbell-lib/src/test/java/dev/christopherbell/libs/mongo/lease/ScheduledCollectorCoordinatorTest.java` | Assert failed persistence, original cause, interrupt flag, and lease release. |
| `cbell-lib/README.md` | Document the coordinator's interruption-preservation behavior. |

## Task Breakdown
### Task 1 - Preserve cancellation at the coordinator boundary
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `cbell-lib/src/main/java/dev/christopherbell/libs/lease/ScheduledCollectorCoordinator.java`; `cbell-lib/src/test/java/dev/christopherbell/libs/mongo/lease/ScheduledCollectorCoordinatorTest.java`; `cbell-lib/README.md`. |
| **Symbols** | `ScheduledCollectorCoordinator.run`; `Work.execute`; interruption regression. |
| **Inspection** | Read the coordinator, its outcome model, lease and status stores, focused tests, module README, and representative shared callers at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Behavior** | Interrupted collector work returns control with the thread still interrupted while retaining the durable failed-run and lease-release behavior. |
| **Invariants** | No public signature, status enum, error-category, or persistence schema changes; lease release remains in `finally`. |
| **Boundary/API** | Existing `run` call and checked `Work.execute` contract remain source compatible. |
| **Effects and failures** | Preserve the `InterruptedException` as wrapper cause, record the safe failure category, restore cancellation, and release the exact lease owner. |
| **Tests and evidence** | Demonstrate a baseline failure with interruption, captured failed status/cause and release on candidate; run focused coordinator tests and the full native gate. |
| **Verification** | `.\gradlew.bat --no-parallel --max-workers=4 :cbell-lib:test --tests dev.christopherbell.libs.mongo.lease.ScheduledCollectorCoordinatorTest`; full `:website:check :cbell-lib:check :website:bootJar`; committed app through `verify-local-app`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused regression verifies wrapper cause identity, failed persisted status, released lease, and restored interrupt flag; clear the flag in test cleanup. | Not independently visible over HTTP; exercise the committed app startup and verify cleanup. |
| AC-2 | Focused coordinator suite and full website/library/browser/PowerShell/package gate. | Run the committed packaged candidate with isolated MongoDB `test` and temporary storage. |
| AC-3 | Candidate JAR includes the committed shared-library code. | Readiness or explicit migration-015 blocker, with database identity and process/port cleanup. |

Regressions and edge cases:
- Non-interruption checked failures keep the existing wrapper and cause behavior.
- Runtime exceptions remain unwrapped.
- The interruption test clears the test thread's flag in `finally` so it does not contaminate later tests.

## Rollback or Recovery
The correction is limited to the coordinator boundary, a focused test, and module documentation. Revert the single candidate commit to restore existing checked-failure behavior. If candidate startup fails at migration 015, stop only the candidate and retain database state.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Interrupt flag leaks between unit tests | Low | Clear it explicitly in the new test's `finally` block. |
| Failure persistence or release behavior changes | Low | Assert captured failed status and exact lease release while keeping existing `finally` unchanged. |
| Application readiness remains blocked by migration 015 | High based on current audit evidence | Record the exact candidate and do not bypass the startup guard or create a PR. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
