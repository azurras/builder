# Preserve Mongo Probe Failure Causes

## Document Status
blocked

## Objective
> [!IMPORTANT]
> The Mongo connectivity probe should translate only expected future outcomes, preserve the cause of identity failures, and expose invalid timeout conversion before starting background work.

## Background
`MongoDatabaseConnectivityProbe` catches every `Exception` around `FutureTask.get`. Its identity method translates failures into `IllegalStateException` without a cause, and timeout conversion happens after launching the virtual thread. The command-center health caller intentionally converts a failed identity result to DOWN, while the probe itself should retain the cause for diagnosis.

## Goals
- Catch only expected future outcomes and keep interrupted/future causes on translated identity failures (AC-1).
- Prove failed pings remain false, identity failures keep their cause, and invalid timeout conversion does not start database work (AC-2).
- Run the committed candidate locally on the permitted isolated `test` database and complete separate PR delivery (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change database health status or public health response details | Health configuration already owns the DOWN translation and redaction. |
| Change Mongo connection settings, timeout values or retry behavior | The correction is limited to the probe's future boundary. |
| Repair or modify the existing MongoDB `test` database | Direct writes are prohibited and require separate supported provisioning authority. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Probe future catches name `ExecutionException`, `TimeoutException` and `CancellationException`; identity translations retain their causes and timeout conversion occurs before task launch. |
| AC-2 | Focused tests prove ping failure fallback, identity cause retention and invalid timeout visibility without Mongo work; full module checks pass. |
| AC-3 | Packaged candidate reaches readiness and a representative route on isolated database `test`; the report is published and the reviewed PR merges with supported deployment health readback. |

## Inputs
- **Request:** Whole-codebase Chris Street Style audit with small targeted corrections and one plan/report per change; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `MongoDatabaseConnectivityProbe`, `DatabaseConnectivityProbe`, `PersistenceIdentityProbe`, `PersistenceIdentity`, `DatabaseHealthConfiguration`, and migration 015 at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected tests:** `DatabaseHealthConfigurationTest`; no direct probe test existed.
- **Guidance:** Website `AGENTS.md`; Builder Chris Street Style naming, Java, design/API, and testing references.
- **Baseline:** `DatabaseHealthConfigurationTest` passes on the clean isolated worktree.

## Branch
`codex/precise-mongo-probe-failures-20261005` from website `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- `ExecutionException`, `TimeoutException`, and `CancellationException` are the recoverable `Future.get` outcomes represented by the probe contracts.
- A timeout too large to convert to milliseconds is invalid caller input and must fail before database work begins.
- Health remains DOWN when an identity probe fails; cause retention is internal diagnostic context only.

## Open Questions
- The only permitted isolated MongoDB database, `test`, lacks an active cutover ledger and now contains a failed migration-015 record. Candidate runtime and PR creation remain blocked pending a supported fixture or recovery procedure; direct writes and guard bypass are prohibited.

## Design
Convert the duration to milliseconds before creating or starting a task. Keep interruption as its own branch, restore the thread flag, cancel the task and retain the cause. Handle only expected future failures; `ping` returns false for them, while `identity` throws its existing safe message with the failure chain attached.

| Alternative | Why not |
|---|---|
| Keep catching every exception | It hides programming errors and turns invalid durations into ordinary probe failure. |
| Include raw failure text in health details | That would change the safe external health contract and could expose infrastructure details. |
| Add a new executor abstraction | One focused test seam is unnecessary; controlled MongoTemplate mocks exercise the actual probe boundary. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/MongoDatabaseConnectivityProbe.java` | Move timeout conversion before task start, narrow future catches, preserve translated causes. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/MongoDatabaseConnectivityProbeTest.java` | Add direct focused tests for ping failure, identity cause and timeout conversion. |

## Task Breakdown
### Task 1 - Make Mongo probe outcomes explicit
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the probe, interfaces, value type, health caller and existing health test on clean `origin/main`. |
| **Symbols** | `MongoDatabaseConnectivityProbe.ping()` and `.identity()`, plus new probe tests. |
| **Inspection** | Base `695a3ed8617f9b4ab07abb7413baf369c58acf6`; `DatabaseHealthConfigurationTest` passed. |
| **Behavior** | Expected ping failures remain false; identity continues to throw a safe `IllegalStateException`; causes are retained; invalid timeout conversion happens before task launch. |
| **Invariants** | Interruption restores the flag and cancels work; no change to health response details or database effects. |
| **Boundary/API** | Probe interface signatures, units and sanitized messages remain stable. |
| **Effects and failures** | A bounded virtual task owns database calls; every expected failure cancels the task; unexpected defects remain visible. |
| **Tests and evidence** | Add deterministic tests at MongoTemplate and FutureTask boundaries; run the focused class, full module checks, and packaged runtime verification. |
| **Verification** | Run `:website:test --tests '*MongoDatabaseConnectivityProbeTest'`; run `:website:check :cbell-lib:check`; inspect the complete diff; verify candidate startup and `/` on isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review exact catches, task start order, cause chain and interruption handling. | Start committed candidate on isolated database `test`. |
| AC-2 | Focused probe tests, full module checks, final diff review. | Candidate readiness and representative home route succeed. |
| AC-3 | Required CI and merge readback. | Publish actual runtime evidence and confirm supported deployment health for the merge SHA. |

Regressions: failed Mongo ping remains false; identity failure keeps the underlying exception reachable through its cause chain; oversized duration fails before MongoTemplate is called; interruption remains cancelled and restored.

## Rollback or Recovery
Before merge, revert this isolated correction if behavior or checks regress. After merge, use a reviewed revert PR and supported automatic deployment. Do not alter MongoDB records directly or bypass startup guards.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A new Future failure type is introduced by the supported JDK | Low | The supported Java 25 contract is enumerated and native checks compile against it. |
| Test database remains unavailable for runtime proof | High | Keep this candidate unpushed until a supported fixture/recovery procedure is available. |

## Implementation Log

### 2026-10-05 - Record Mongo probe verification and runtime blocker

- **Change:** The regression tests failed on baseline for lost identity cause and swallowed timeout conversion; the probe now moves conversion before task launch, catches named future outcomes, and retains identity causes. Three probe tests and the existing health configuration test pass; full module checks passed. Candidate `0fb75ef` fails packaged startup on the required `test` database; the [blocked test report](../test-reports/2026-10-05-00-42-christopherbell-dev-preserve-mongo-probe-failure-causes.md) records the evidence.
- **Reason:** Broad catches hid programming errors and cause loss violated the diagnostic contract. The test database has a failed migration-015 record and no active cutover ledger; repair and guard bypass are prohibited.
- **Impact:** AC-1 and AC-2 are met. AC-3 and PR creation are blocked pending supported test database provisioning or recovery.

## Outcome
> [!WARNING]
> The Mongo probe correction is implemented and native checks pass. Candidate startup and PR creation are blocked because database `test` has a failed migration-015 record and lacks the active cutover ledger.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Probe catches name expected future outcomes; identity translation keeps the cause chain; timeout conversion precedes task launch in candidate `0fb75ef`. |
| AC-2 | ✅ Met | Three focused probe tests, the health configuration test and full module checks passed; see the [test report](../test-reports/2026-10-05-00-42-christopherbell-dev-preserve-mongo-probe-failure-causes.md). |
| AC-3 | ⏸️ Blocked | Candidate startup stopped at migration 015 before readiness. A supported fixture or recovery procedure is required; no PR was opened. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
