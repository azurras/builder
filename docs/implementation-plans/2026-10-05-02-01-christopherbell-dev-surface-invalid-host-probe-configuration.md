# Surface Invalid Host Probe Configuration

## Document Status
ready-for-execution

## Plan Format
task-contract-v2

## Objective
> [!IMPORTANT]
> Keep expected host-probe I/O and interruption outcomes unavailable while allowing invalid probe configuration and programming defects to remain visible.

## Background
`ApplicationHostMetricsProvider.DefaultOperationalProbe.serviceRunning()` and `responseMillis()` catch `Exception` and turn every failure into `Optional.empty()`. Process launch and HTTP calls have specific I/O and interruption failures; malformed URI or other programming/configuration defects should not look like a normal unavailable metric. Existing focused tests establish the available/unavailable result shape.

## Goals
- Catch only expected process and HTTP I/O/interruption failures at the two probe boundaries (AC-1).
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
| AC-1 | `serviceRunning()` and `responseMillis()` catch only their expected `IOException` and `InterruptedException` outcomes, restoring interruption. |
| AC-2 | Existing operational-unavailable behavior remains; a malformed configured production port propagates instead of becoming an unavailable metric. |
| AC-3 | Focused and full native checks pass, exact packaged candidate startup is attempted with database `test`, and runtime evidence is saved before any PR. |

## Inputs
- **Request:** Full Chris Street Style audit with small targeted corrections, separate plan/report per correction; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `ApplicationHostMetricsProvider.DefaultOperationalProbe.serviceRunning()`, `responseMillis()`, and `read()` at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
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
Catch `IOException | InterruptedException` in both helpers and restore interruption on the interrupted path. Leave malformed URI construction and other unexpected runtime failures uncaught. Add a focused regression that configures an invalid local production port and asserts the configuration exception propagates; retain the existing test that valid unavailable probe results map to `UNAVAILABLE`.

| Alternative | Why not |
|---|---|
| Keep catching all `Exception` | Configuration and programming defects continue to masquerade as expected probe unavailability. |
| Catch all `RuntimeException` as unavailable | It preserves the same failure conflation. |
| Add a new process/HTTP abstraction solely for tests | The current boundary can be verified with the configured URI and existing provider API without another seam. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java` | Narrow process and HTTP probe catches to I/O/interruption outcomes and preserve interrupt status. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java` | Verify malformed production port configuration propagates while explicit unavailable probe results remain unavailable. |

## Task Breakdown
### Task 1 - Preserve operational failures and expose configuration defects
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the host metrics provider, command-center properties, and `ApplicationHostMetricsProviderTest` at base `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `DefaultOperationalProbe.serviceRunning()`, `DefaultOperationalProbe.responseMillis()`, and host-probe tests. |
| **Inspection** | Four baseline provider tests pass; the probe methods catch broad `Exception`, although expected process/HTTP calls expose I/O and interruption outcomes. |
| **Behavior** | Expected absent/unreachable metrics remain unavailable; invalid local probe configuration propagates. |
| **Invariants** | Metric keys and status mapping remain unchanged; interruption is restored; no production operation is run. |
| **Boundary/API** | No public API, configuration name, route, or response contract changes. |
| **Effects and failures** | Process and local HTTP probes retain their existing ownership and timeout; expected I/O failure maps to unavailable, interruption restores thread status, other defects surface. |
| **Tests and evidence** | Add a direct regression for malformed port; rerun focused tests and full `:website:check :cbell-lib:check :website:bootJar`. |
| **Verification** | Use the isolated `test` profile and non-production port for packaged startup attempt; no PR before runtime readiness and report. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Inspect both catch types and run the focused provider test class. | Start packaged candidate with test profile and disabled side effects. |
| AC-2 | Assert malformed port propagates; retain existing explicit-unavailable metric test. | Verify startup readiness and representative application route if the candidate reaches readiness. |
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
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev
