# Keep Command Center Provider Failures Precise

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Make asynchronous host-metric collection translate only actual provider execution and cancellation outcomes into the existing unavailable-metric response, so unrelated collector defects remain visible.

## Background
`CommandCenterMetricsService.collect()` handles timeout and interruption explicitly, then catches every remaining `Exception` around `Future.get`. The expected remaining future outcomes are `ExecutionException` and `CancellationException`; the broad catch can disguise defects in timeout calculations or collector logic as ordinary provider failure. The user requested a full Chris Street Style audit using small targeted corrections with a distinct plan and report for each. This correction comes from the restarted current-main audit and does not rely on draft PR #1477.

## Goals
- Translate only provider execution failure and cancellation into the existing sanitized `PROVIDER_ERROR` behavior (AC-1).
- Preserve timeout, interruption, stale-reading, logging and redaction behavior with focused regression coverage (AC-2).
- Verify the committed candidate locally and complete delivery through deployment readback (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change metric payloads, alert codes, timeouts or stale-reading policy | These are established contracts unrelated to this catch boundary. |
| Refactor provider scheduling or executor ownership | The correction is limited to exception typing. |
| Change database-probe failure handling | It is a separate correction with its own plan and report. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The provider future boundary catches only `ExecutionException` and `CancellationException` after explicit timeout and interruption branches. |
| AC-2 | Native tests show execution failure and cancellation retain sanitized fallback behavior while timeout and interruption behavior remain green. |
| AC-3 | A complete report names the candidate; its PR passes CI, merges, and supported production status reports that merge revision active and healthy. |

## Inputs
- **Request:** User requested a whole-codebase Chris Street Style rewrite with small safe changes and a separate plan/report per correction; rejected draft PR #1477 as stale style evidence.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`, in progress.
- **Inspected code:** `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsService.java`, `collect()` future outcome branches.
- **Inspected tests:** `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsServiceTest.java`, timeout, interruption and sanitized provider-failure scenarios.
- **Guidance:** Root and command-center package instructions, Builder Chris Street Style Java/testing references, native Gradle task.
- **Current base:** Website `origin/main` after PR #1478 at merge commit `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Branch
`codex/command-center-provider-failure-boundaries-20261004` from refreshed `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- Provider execution failures reach `Future.get` as `ExecutionException`; cancellation reaches it as `CancellationException`.
- Existing protected alert detail and last-good readings are intentional behavior.

## Open Questions
None.

## Design
Narrow the final `collect()` catch to the two remaining expected future outcomes. Keep timeout/interruption branches, cancellation cleanup, warning log, stale fallback and sanitized alert unchanged. Test through the metrics service and injected executor boundary.

| Alternative | Why not |
|---|---|
| Keep the broad catch and document it | It still disguises unexpected collector defects as provider failures. |
| Catch provider runtime exceptions separately | Provider code runs in the future, so failures arrive wrapped as `ExecutionException`. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsService.java` | Name the expected future-failure types in the catch clause. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsServiceTest.java` | Add deterministic evidence for uncovered expected outcomes only. |

## Task Breakdown
### Task 1 - Narrow the provider future failure boundary
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsService.java` and its corresponding test. |
| **Symbols** | `CommandCenterMetricsService.collect()` and provider future failure branches. |
| **Inspection** | Read target and test at website `origin/main` descendant `695a3ed8617f9b4ab07abb7413baf369c58acf6`, plus root/package guidance. |
| **Behavior** | Preserve current provider error fallback and stale value behavior. |
| **Invariants** | Timeout and interruption remain explicit; interruption restores the flag; sensitive causes never enter snapshots. |
| **Boundary/API** | Metric, alert and service APIs remain unchanged. |
| **Effects and failures** | Catch only recoverable future execution/cancellation outcomes; no new I/O or side effects. |
| **Tests and evidence** | Focused service tests, full module checks, diff review, isolated packaged runtime proof and a separate candidate-specific report. |
| **Verification** | `./gradlew.bat :website:test --tests '*CommandCenterMetricsServiceTest'`; `./gradlew.bat :website:check :cbell-lib:check`; isolated candidate readiness and representative page request. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused service tests and exact catch-boundary review. | Start committed packaged app on isolated port; readiness and representative page return 200. |
| AC-2 | Focused `CommandCenterMetricsServiceTest`; full `:website:check :cbell-lib:check`. | Same candidate; production services and database remain unchanged. |
| AC-3 | CI on reviewed head and PR merge readback. | Published report plus automatic production status/readiness proving the merge SHA active. |

Regressions: execution failure stays sanitized; cancellation uses the same provider warning; timeout remains distinguishable; interruption remains restored and cancels work; last-good readings remain available.

## Rollback or Recovery
Revert the isolated change before merge if behavior or checks fail. After merge, a confirmed regression requires a reviewed revert PR and the supported automatic deployment; do not manually restart production or edit its database.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Narrowing exposes a defect previously hidden as provider unavailability | Low | Surface and diagnose it, then keep any fix in authorized scope. |
| Cancellation test becomes timing-dependent | Low | Use an injected deterministic canceled future, not sleeps. |
| Deployment takes longer than the code change | Medium | Wait for supported status evidence; report any unresolved gap. |

## Implementation Log

### 2026-10-04 - Narrow the provider future failure boundary

- **Change:** Began Task 1 and added an invalid-timeout regression, observing the expected failure on the unmodified broad catch; narrowed the handler to `ExecutionException | CancellationException` and verified the focused service suite, including cancellation fallback.
- **Reason:** The current broad catch turns a timeout conversion defect into a misleading provider-unavailable result; exact future outcomes belong at the failure boundary.
- **Impact:** Document Status is now in-progress; implementation stays within the planned two files and existing metric contract.

### 2026-10-04 - Record isolated test database startup blocker

- **Change:** The final native checks pass on candidate `d34d8e78`, but its packaged startup against isolated MongoDB database `test` fails at migration `015-require-domain-collection-schema`; the required domain cutover ledger is absent. The failed attempt and missing runtime proof are recorded in the [candidate test report](../test-reports/2026-10-04-23-58-christopherbell-dev-keep-command-center-provider-failures-precise.md).
- **Reason:** Repository instructions require the database named `test`, while the target release refuses to start without a previously established domain cutover marker. Direct database writes or bypassing the migration guard would violate the verification constraints.
- **Impact:** AC-1 and AC-2 are met; AC-3 is blocked until a supported, isolated `test` database with the required ledger is available. No PR was created.

## Outcome

> [!WARNING]
> The focused correction is implemented and native checks pass, but local candidate startup and required runtime evidence are blocked by the missing domain cutover ledger in the only permitted database, `test`.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Catch boundary names `ExecutionException` and `CancellationException`; timeout overflow regression failed on the original code and passed on candidate `d34d8e78`. |
| AC-2 | ✅ Met | Provider failure, cancellation, timeout coverage and full native check passed on `d34d8e78`; see [blocked candidate report](../test-reports/2026-10-04-23-58-christopherbell-dev-keep-command-center-provider-failures-precise.md). |
| AC-3 | ⏸️ Blocked | The candidate exited during migration 015 before readiness. An approved database fixture or provisioning procedure is required before PR creation. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
