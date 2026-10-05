# Let Command Center Report Host Probe Defects

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Allow unexpected runtime defects from the application host probe to reach the command-center metrics boundary, which already isolates failed providers and reports an alert.

## Background
`ApplicationHostMetricsProvider.read()` catches every `RuntimeException` from its internal probe and turns it into an ordinary set of unavailable readings. Its production probe already represents expected absence and I/O failure with empty optionals; `CommandCenterMetricsService` owns provider isolation, logs the cause and exposes `PROVIDER_ERROR`. The inner catch therefore hides programming defects and bypasses the intended alert path.

## Goals
- Preserve expected unavailable readings when a probe returns empty optionals (AC-1).
- Propagate unexpected probe runtime failures to the metrics service's existing isolation boundary (AC-2).
- Run focused/full native checks, package and attempt required isolated local runtime verification (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change how operating-system or HTTP probe I/O failures become unavailable optionals | Those lower-level boundaries already own expected operational failures. |
| Change provider timeouts, public metric keys, or alert policy | The metrics service owns those existing contracts. |
| Repair or bypass Mongo migration 015 | Database recovery requires a supported fixture/provisioning procedure. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | A probe that reports absent service, response and release values still produces explicit unavailable metric readings. |
| AC-2 | An unexpected runtime failure from `OperationalProbe.read()` propagates from this provider and is isolated by the existing service boundary. |
| AC-3 | Focused and full required checks plus packaged local application verification are run and recorded for the exact committed candidate; PR creation remains gated on successful runtime readiness. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `ApplicationHostMetricsProvider`, `HostMetricsProvider`, `CommandCenterMetricsService`, `ApplicationHostMetricsProviderTest`, `CommandCenterMetricsServiceTest`, and `website/src/main/java/dev/christopherbell/admin/README.md` at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Guidance:** Chris Street Style Java and testing references; website `AGENTS.md`.

## Branch
Create a fresh isolated worktree and branch from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6` after publishing this plan.

## Assumptions
- Empty `Optional`/`OptionalDouble` results are the expected unavailable outcomes for this provider.
- `CommandCenterMetricsService` is the intended failure boundary for provider exceptions and emits a `PROVIDER_ERROR` while retaining stale data.
- The required isolated database `test` currently reaches the known migration-015 durable-record blocker; this must be recorded without direct database modification or guard bypass.

## Open Questions
None. Continue source-level work and stop only at the runtime-gated PR boundary if the known database prerequisite remains unavailable.

## Design
Remove only the `RuntimeException` catch around `probe.read()`. Keep unavailable behavior for returned empty optionals unchanged. Add a focused provider test asserting an `IllegalStateException` propagates, while retaining the existing test for explicit unavailable readings. The metrics service's existing catch remains responsible for logging the cause and preserving the command-center collection path.

| Alternative | Why not |
|---|---|
| Keep converting all probe runtime failures into empty values | It makes defects indistinguishable from expected absence and suppresses the service's diagnostic alert. |
| Remove provider isolation from the metrics service | That boundary protects unrelated telemetry and is outside this correction. |
| Add new exception abstractions or result types | Existing optionals and provider error handling already distinguish expected absence from unexpected defects. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java` | Let unexpected `probe.read()` runtime failures propagate. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java` | Characterize explicit unavailability and add defect-propagation assertion. |

## Task Breakdown
### Task 1 - Preserve the host metrics failure boundary
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the provider, metrics service caller, focused tests and admin ownership README. |
| **Symbols** | `ApplicationHostMetricsProvider.read(Instant)`, `OperationalProbe.read()`, and `ApplicationHostMetricsProviderTest`. |
| **Inspection** | Fresh website source revision `695a3ed8617f9b4ab07abb7413baf369c58acf6`; traced the provider future and `PROVIDER_ERROR` handling in `CommandCenterMetricsService`. |
| **Behavior** | Preserve unavailable values for empty probe results; unexpected runtime failures reach the service boundary. |
| **Invariants** | Failure of this provider stays isolated from other host metrics; expected platform absence remains an explicit unavailable state. |
| **Boundary/API** | No public provider or metric schema changes. |
| **Effects and failures** | Do not swallow programming/runtime defects; metrics service logs the original cause and reports its existing alert. |
| **Tests and evidence** | Run the existing unavailable characterization, add propagation characterization, run focused metrics tests and full required project checks. |
| **Verification** | `:website:test --tests dev.christopherbell.admin.commandcenter.metrics.ApplicationHostMetricsProviderTest --tests dev.christopherbell.admin.commandcenter.metrics.CommandCenterMetricsServiceTest`, `:website:check :cbell-lib:check`, `:website:bootJar`; then packaged runtime attempt on isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing provider test for empty optionals stays green. | Candidate startup plus representative home route after readiness. |
| AC-2 | Focused test proves an injected `IllegalStateException` propagates; metrics service tests preserve provider isolation and alert. | Candidate startup plus representative home route after readiness. |
| AC-3 | Focused metrics tests, full module checks and packaged build. | Use test profile, isolated MongoDB `test`, non-production port and disabled side effects; report actual startup/route/cleanup result. |

Regression: normal unavailable readings remain `UNAVAILABLE`; unexpected failure is no longer converted to a false healthy/unavailable-shaped provider result; neighboring providers remain collectable.

## Rollback or Recovery
Revert this single provider-boundary change if any expected absence or provider-isolation characterization fails. Do not mutate test database migration records or disable migration validation.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A latent runtime defect now surfaces to the metrics collector | Low | The collector already catches, logs and isolates provider failures; verify its focused suite. |
| Required candidate runtime remains blocked | High | Record the attempt and withhold PR creation until a supported fixture/provisioning or recovery procedure is available. |

## Implementation Log

### 2026-10-05 - Record runtime block

- **Change:** Removed the catch that turned every `RuntimeException` from the host operational probe into ordinary unavailable values; added `propagatesUnexpectedProbeDefects()`. Baseline regression failed as expected. Focused metrics tests, full project checks and packaging passed. Candidate startup against isolated `test` stopped at migration 015 before readiness; see the [blocked test report](../test-reports/2026-10-05-01-36-christopherbell-dev-let-command-center-report-host-probe-defects.md).
- **Reason:** The metrics collector already isolates provider failures, logs the original cause and emits `PROVIDER_ERROR`; the inner catch hid that signal and treated a defect as ordinary absence.
- **Impact:** AC-1 and AC-2 are met; AC-3 is partly met and blocked at runtime. No PR was opened. A supported test fixture/provisioning or recovery procedure is needed.

## Outcome
> [!WARNING]
> Provider behavior and all source-level checks are verified. Required packaged runtime proof is blocked before readiness by migration 015, so no PR was opened.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Existing empty-result characterization passed in focused provider suite. [Test report](../test-reports/2026-10-05-01-36-christopherbell-dev-let-command-center-report-host-probe-defects.md). |
| AC-2 | ✅ Met | New defect-propagation regression failed before and passed after; collector isolation/alert tests passed. [Test report](../test-reports/2026-10-05-01-36-christopherbell-dev-let-command-center-report-host-probe-defects.md). |
| AC-3 | ⏸️ Blocked | Full checks and package passed; candidate exited at migration 015 before readiness. No PR opened. [Test report](../test-reports/2026-10-05-01-36-christopherbell-dev-let-command-center-report-host-probe-defects.md). |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
