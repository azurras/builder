# Surface Invalid Host Probe Configuration

## Document Status
blocked

## Plan Format
task-contract-v2

## Objective
> [!IMPORTANT]
> Keep expected host-probe I/O and interruption outcomes unavailable while allowing configuration and programming defects to reach the command-center provider isolation boundary.

## Background
`ApplicationHostMetricsProvider.DefaultOperationalProbe.serviceRunning()` and `responseMillis()` catch `Exception` and turn every failure into `Optional.empty()`. Process launch and HTTP calls have specific I/O and interruption failures; malformed URI or other programming/configuration defects should not look like a normal unavailable metric. Existing focused tests establish the available/unavailable result shape.

## Goals
- Remove the runtime-exception fallback from `read()` and catch only expected process and HTTP I/O/interruption failures in the two helpers (AC-1).
- Preserve unavailable metrics for expected operational failures and propagate malformed configuration (AC-2).
- Run focused/full native checks and attempt local packaged runtime proof for the exact candidate (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change metrics keys, values, labels, timeout behavior or alert ownership | Those are stable collector contracts outside the failure-type correction. |
| Change release metadata parsing | That has its own independently planned correction and candidate report. |
| Change production service configuration or start/stop any production service | The audit is limited to code and safe local verification. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `read()` lets probe runtime defects propagate; `serviceRunning()` and `responseMillis()` catch only expected `IOException` and `InterruptedException` outcomes, restoring interruption. |
| AC-2 | Existing operational-unavailable behavior remains; a missing configured provider timeout propagates instead of becoming an unavailable metric. |
| AC-3 | Focused and full native checks pass, exact packaged candidate startup is attempted with database `test`, and runtime evidence is saved before any PR. |

## Inputs
- **Request:** Full Chris Street Style audit with small targeted corrections, separate plan/report per correction; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `ApplicationHostMetricsProvider.read()`, `DefaultOperationalProbe.serviceRunning()`, and `responseMillis()` at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected tests:** `ApplicationHostMetricsProviderTest`; the baseline focused test class passed all four tests before edits.
- **Guidance:** Website operating instructions and Builder Chris Street Style Java, naming/readability, design/API, and testing references.

## Branch
Create `codex/narrow-host-probe-failures-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6` after publishing this plan.

## Assumptions
- `IOException` and `InterruptedException` represent expected local probe unavailability; interruption must restore the thread flag.
- Invalid URI construction caused by a malformed configured port is a configuration defect and should not be represented as an unavailable reading.
- The local runtime is currently blocked by the incomplete durable record for migration 015 in test database `test`.

## Open Questions
None. Keep the current metric fallback for expected operating-system and network failures.

## Design
Let `read()` call the probe without catching its runtime defects. Catch `IOException` and `InterruptedException` in both helpers, restoring interruption. Leave malformed configuration and other unexpected runtime failures uncaught so `CommandCenterMetricsService` can isolate and report the provider failure. Add a focused regression that configures an invalid local production port and asserts the configuration exception propagates; retain the existing test that valid unavailable probe results map to `UNAVAILABLE`.

| Alternative | Why not |
|---|---|
| Keep catching all `Exception` | Configuration and programming defects continue to masquerade as expected probe unavailability. |
| Catch all `RuntimeException` as unavailable | It preserves the same failure conflation. |
| Add a new process/HTTP abstraction solely for tests | The current boundary can be verified with the configured URI and existing provider API without another seam. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java` | Remove `read()` catch-all; narrow process and HTTP probe catches to I/O/interruption outcomes and preserve interrupt status. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java` | Verify missing provider timeout configuration propagates while explicit unavailable probe results remain unavailable. |

## Task Breakdown
### Task 1 - Preserve operational failures and expose configuration defects
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the host metrics provider, command-center properties, and `ApplicationHostMetricsProviderTest` at base `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `read()`, `DefaultOperationalProbe.serviceRunning()`, `DefaultOperationalProbe.responseMillis()`, and host-probe tests. |
| **Inspection** | Four baseline provider tests pass; the probe methods catch broad `Exception`, although expected process/HTTP calls expose I/O and interruption outcomes. |
| **Behavior** | Expected absent/unreachable metrics remain unavailable; invalid local probe configuration propagates. |
| **Invariants** | Metric keys and status mapping remain unchanged; interruption is restored; no production operation is run. |
| **Boundary/API** | No public API, configuration name, route, or response contract changes. |
| **Effects and failures** | Process and local HTTP probes retain their existing ownership and timeout; expected I/O failure maps to unavailable, interruption restores thread status, other defects surface. |
| **Tests and evidence** | Add a direct regression for missing provider timeout; rerun focused tests and full `:website:check :cbell-lib:check :website:bootJar`. |
| **Verification** | Use the isolated `test` profile and non-production port for packaged startup attempt; no PR before runtime readiness and report. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Inspect the provider and helper catch types; run the focused provider test class. | Start packaged candidate with test profile and disabled side effects. |
| AC-2 | Assert missing provider timeout propagates; retain existing explicit-unavailable metric test. | Verify startup readiness and representative application route if the candidate reaches readiness. |
| AC-3 | Full website/library checks and boot JAR; `git diff --check`. | Record actual candidate startup and route attempt using isolated database `test`; report any prerequisite blocker. |

Regression: an invalid production port must throw during probe construction instead of returning a plausible `UNAVAILABLE` reading; actual network/process absence keeps the documented unavailable result.

## Rollback or Recovery
Revert only the catch/test changes if the failure classification or expected unavailable behavior regresses. Do not change the database or bypass migration guard to manufacture runtime readiness.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| An expected local probe exception is not included in the narrowed catch | Low | Retain focused expected-unavailable characterization and review the exact JDK checked exceptions. |
| Required local application runtime remains blocked | High | Record startup failure and do not open a PR until a supported isolated fixture/recovery path exists. |

## Implementation Log

### 2026-10-05 - Begin host probe correction

- **Change:** Baseline `ApplicationHostMetricsProviderTest` passed all four existing tests; starting the separate narrowing correction on its published plan.
- **Reason:** The existing coverage confirms metric availability mapping but does not show malformed probe configuration remains visible.
- **Impact:** Implementation begins for Task 1; no application source or test changes are committed yet.

### 2026-10-05 - Use invalid timeout regression

- **Change:** Replaced the planned invalid-port regression with a missing provider-timeout regression after an out-of-range integer port did not fail at URI construction; the JDK treated it as an ordinary connection failure. The new case targets a configuration invariant that the properties class marks `@NotNull` and demonstrates a swallowed `NullPointerException`.
- **Reason:** The first input could not distinguish a configuration defect from a legitimate unreachable endpoint; the null timeout makes the catch boundary defect concrete and reproducible.
- **Impact:** AC-2 and the design/test descriptions now use the validated timeout invariant; implementation remains limited to the two probe catch clauses and this focused test.

### 2026-10-05 - Include outer provider boundary

- **Change:** Expanded Task 1 to remove the outer `read()` runtime catch as well as narrow `serviceRunning()` and `responseMillis()`; the public provider boundary otherwise still swallows the invalid-timeout defect, as the focused test demonstrated.
- **Reason:** Changing only the helper catches leaves the behavior invisible because `read()` converts the propagated `NullPointerException` back into empty metrics. The adjacent `CommandCenterMetricsService` already owns timeout isolation, stale readings and provider-error alerts.
- **Impact:** Task 1 Symbols, Behavior, Effects and failures, Expected Changes, AC-1 and its test plan now cover all three failure boundaries in one coherent host-provider correction; separate provider-layer historical candidate evidence remains independently documented.

### 2026-10-05 - Record runtime blocker

- **Change:** Candidate `f3854fbd` removes the `read()` fallback and narrows both local probe catches; focused tests and full checks pass, but packaged startup fails at migration 015 before readiness.
- **Reason:** The isolated test database retains an incomplete durable migration record; direct mutation or bypass is prohibited, and no supported fixture/recovery is available in this run.
- **Impact:** AC-1 and AC-2 are met; AC-3 is blocked pending supported runtime verification. See the [test report](../test-reports/2026-10-05-02-14-christopherbell-dev-surface-invalid-host-probe-configuration.md). No PR opened.

## Outcome

> [!WARNING]
> The host metrics provider now preserves invalid configuration and programming failures for the command-center isolation boundary while retaining expected unavailable semantics. Native checks and packaging pass; packaged runtime is blocked before readiness by migration 015. No PR was opened.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Candidate `f3854fbd` removes the provider runtime fallback and narrows helper catches to I/O/interruption. |
| AC-2 | ✅ Met | The missing-timeout regression failed against baseline and passes on candidate; all five focused provider tests pass. |
| AC-3 | ⏸️ Blocked | [Test report](../test-reports/2026-10-05-02-14-christopherbell-dev-surface-invalid-host-probe-configuration.md): full checks/package pass; migration 015 stops startup before readiness, preventing route verification and PR creation.

## Project
christopherbell-dev
