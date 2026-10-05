# Preserve Command Center Launch Failure Causes

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Translate only declared command-launch `IOException`s into the existing safe request error and retain the cause. Let programming defects remain visible while preserving the service's existing rollback of accepted power-action state.

## Background
`CommandExecutor.execute(CommandCenterActionType)` declares only `IOException`, but `CommandCenterActionService.executeNow()` catches every `Exception` and drops the failure cause. Its callers already roll back accepted power-action state when an unexpected runtime failure escapes.

## Goals
- Translate expected launch I/O failure to the existing safe `InvalidRequestException`, retaining the `IOException` cause (AC-1).
- Preserve propagation of unrelated runtime failures and the accepted-action rollback contract (AC-2).
- Prove the focused behavior and run full module checks (AC-3).
- Verify the packaged application on isolated MongoDB `test` and publish candidate runtime evidence before any PR (AC-4).

## Non-Goals
| Not doing | Why |
|---|---|
| Change command allowlists, host effects, audit categories, or public error text | This correction changes only failure classification and cause retention. |
| Alter the migration guard or seed MongoDB directly | Runtime verification must follow the supported application and database boundaries. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | An `IOException` from the command executor produces the existing safe error with the original cause attached. |
| AC-2 | An unrelated runtime failure propagates and any reserved power-action state is rolled back. |
| AC-3 | Regression tests detect the old behavior; focused and full module checks pass. |
| AC-4 | The packaged candidate starts on isolated database `test`, a representative route succeeds, and a candidate-specific runtime report is published before PR creation. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `CommandCenterActionService.executeNow()`, all call sites and action-state rollback at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected contract:** `CommandExecutor.execute()` declares `IOException`; `InvalidRequestException` supports a cause; existing action tests cover launch failure and retry.
- **Guidance:** Chris Street Style Java, naming, design/API and testing references; website `AGENTS.md`.

## Branch
`codex/command-center-launch-causes-20261005` from `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- `IOException` is the expected host-launch failure contract; an unchecked exception indicates an unexpected defect.
- Existing API handling keeps the `InvalidRequestException` message safe and does not serialize its cause.
- Runtime verification still encounters the unresolved migration-015 test fixture blocker.

## Open Questions
- A supported fixture/provisioning or recovery procedure for isolated MongoDB `test` is still needed before runtime proof and PR creation.

## Design
Catch `IOException` at `executeNow()`, audit the same `launch-failed` outcome, and construct the same public message with the cause attached. Existing outer logic rolls back accepted power-action state for both checked launch errors (after translation) and runtime failures. Add one regression for retained `IOException` cause and one for runtime propagation plus rollback.

| Alternative | Why not |
|---|---|
| Keep catching every exception | It turns programming defects into normal request rejection and loses the launch cause. |
| Expose the process error text to the caller | The public message is intentionally generic. |
| Change the command-executor interface | Its current checked exception already expresses the narrow contract. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java` | Catch declared launch `IOException` and preserve it behind the generic public error. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionServiceTest.java` | Assert retained launch cause and unexpected runtime propagation with reservation rollback. |

## Task Breakdown
### Task 1 - Narrow and preserve command launch failures
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the command service, executor interface, exception type, all execution call sites and focused service tests. |
| **Symbols** | `CommandCenterActionService.executeNow()`, `execute()`, `CommandExecutor.execute()` and `CommandCenterActionServiceTest`. |
| **Inspection** | Clean main-based candidate at `695a3ed8617f9b4ab07abb7413baf369c58acf6`; existing launch-failure test inspected. |
| **Behavior** | Expected launch I/O failure remains a safe request error; unrelated runtime failures propagate; successful launch/audit behavior stays unchanged. |
| **Invariants** | Power-action reservation and accepted-action state roll back on failed launch. |
| **Boundary/API** | Keep command allowlist and public message stable; `IOException` cause stays server-side on the exception. |
| **Effects and failures** | Host effect remains in the existing executor; audit remains best effort; no additional I/O or database mutation. |
| **Tests and evidence** | Add cause and runtime-propagation regressions before editing; run focused test, full module checks and packaged runtime proof. |
| **Verification** | Run the existing focused test before edits, show new regressions fail on baseline, rerun focused tests and `:website:check :cbell-lib:check`, then verify candidate startup/route on database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Assert generic message and original `IOException` cause. | Start packaged candidate against isolated `test`. |
| AC-2 | Assert unexpected runtime exception propagates and pending reservation is empty. | Exercise a representative route after readiness. |
| AC-3 | Focused action-service tests and full module checks. | Same candidate runtime exercise. |
| AC-4 | Required CI and merge readback after proof. | Record startup, route response and cleanup in the candidate report. |

Regression: launch `IOException` retains its cause; runtime executor failure is not wrapped and does not leave a phantom pending power action.

## Rollback or Recovery
Before merge, revert only this isolated correction if public handling or rollback behavior changes. After merge, use a reviewed revert PR and supported automatic deployment. Do not change Mongo migration state directly.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Runtime failure reveals an unexpected defect through the normal server boundary | Low | Preserve current generic HTTP exception handling and test state rollback. |
| Runtime proof remains blocked | High | Do not open a PR until supported database fixture/recovery support is available. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
