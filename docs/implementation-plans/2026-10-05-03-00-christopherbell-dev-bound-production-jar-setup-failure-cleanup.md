# Bound Production Jar Setup Failure Cleanup

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Ensure `Start-ProductionJar` terminates and disposes a Java child if candidate log setup fails after process start, while preserving the setup failure and reporting any incomplete cleanup.

## Background
`Start-ProductionJar` starts the candidate process, then adds log metadata, creates `BoundedProcessLog`, attaches asynchronous readers, and adds the writer property. If any setup step throws, the caller never receives the process handle and cannot stop the child. The `BoundedProcessLog` callback is intentionally best-effort for later write failures, but that does not cover setup failures from `Attach` or metadata creation.

## Goals
- Own the process from `Start()` through successful logging setup and terminate/dispose it on every setup failure (AC-1).
- Preserve the initiating setup exception and include cleanup failures or a surviving PID when cleanup is incomplete (AC-2).
- Add a real-child Pester regression and run full native checks plus packaged runtime attempt (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change process-log byte limits, callback behavior, or production health checks | Those are existing independent contracts. |
| Change normal deployment process lifetime or shutdown ownership | The caller owns the process only after setup succeeds. |
| Change release validation, environment, or port selection | Failure occurs after those steps have already completed. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Any post-start metadata/writer/attach failure attempts process-tree termination, waits only within a fixed cleanup bound, and disposes the owned process handle. |
| AC-2 | The original setup exception stays primary; cleanup failures and a still-running child PID are included when cleanup is incomplete. |
| AC-3 | Focused deployment Pester regression and full website/library/browser/PowerShell/package checks pass; the committed packaged app receives a local startup attempt and test report before any PR. |

## Inputs
- **Request:** Full `christopherbell.dev` Chris Street Style audit with targeted corrections and an individual plan/report per change; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `ops/production/windows/modules/Production.Deploy.psm1`, `Start-ProductionJar`, `BoundedProcessLog`, caller cleanup in candidate validation, and `Invoke-BoundedCheckedProcess` at website base `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- **Inspected tests:** `ops/production/windows/tests/Production.Deploy.Tests.ps1`, including normal bounded process-log capture and write-failure tests at the same base.
- **Guidance:** Spoke `AGENTS.md`; Chris Street Style PowerShell, design/API, naming, language adaptation, and testing references.

## Branch
Create `codex/bound-production-jar-setup-cleanup-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c` after publishing this plan.

## Assumptions
- The existing candidate process contract expects stdout and stderr readers attached before returning the handle.
- A fixed five-second cleanup bound matches adjacent process cleanup practice and is sufficient for termination/reaping.
- Local app startup remains blocked by migration 015 on isolated test database `test`.

## Open Questions
None. The caller receives the process only after all log setup succeeds.

## Design
Move process log metadata/writer attachment into a small setup helper that owns the process until it returns successfully. On failure, retain the setup exception, attempt to kill the process tree, wait up to five seconds, report a surviving PID if it remains, and dispose the process handle. If cleanup has no errors, rethrow the original exception unchanged; otherwise aggregate the original first with cleanup failures. Give the helper a narrow log-writer factory seam so a Pester regression can fail after a real child starts and verify the cleanup contract deterministically.

| Alternative | Why not |
|---|---|
| Let the outer deployment caller clean up | It has no process handle when `Start-ProductionJar` throws before returning. |
| Catch and ignore setup failure | Leaves an untracked Java child and loses the setup cause. |
| Use an unbounded `WaitForExit()` | Cleanup could stall deployment indefinitely. |

## Expected Changes
| File or area | Change |
|---|---|
| `ops/production/windows/modules/Production.Deploy.psm1` | Keep process ownership through log setup and perform bounded failure cleanup with causal reporting. |
| `ops/production/windows/tests/Production.Deploy.Tests.ps1` | Add a real child-process regression where log-writer setup fails. |

## Task Breakdown
### Task 1 - Own candidate startup through logging setup
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected deployment module and Pester suite at base `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `Start-ProductionJar`, `BoundedProcessLog.Attach`, candidate process properties, validation caller cleanup, and process-log Pester tests. |
| **Inspection** | Current function starts Java before log setup and has no local failure cleanup; successful and asynchronous log-write tests already exist. |
| **Behavior** | Successful launch returns the same Process with the same log metadata/writer; setup failures no longer strand the child. |
| **Invariants** | Only return a process after both readers attach; preserve the first exception; bound tree termination/reaping; dispose the process handle on failed setup. |
| **Boundary/API** | `Start-ProductionJar` successful return shape stays unchanged; private helper/test seam are internal to the module. |
| **Effects and failures** | Process start and ownership occur in one boundary; terminate process tree after setup error; aggregate cleanup failures without replacing the primary cause. |
| **Tests and evidence** | Establish Pester baseline, then fail log-writer construction with a real sleeping child and assert its process ID is gone within the cleanup bound. |
| **Verification** | Run focused deployment Pester, full project checks/package, then attempt committed packaged startup against isolated MongoDB `test` and record the outcome. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Real child process exits after injected post-start log setup failure. | Launch committed packaged application with jobs and integrations disabled. |
| AC-2 | Assert original setup exception is unchanged when cleanup succeeds; source review confirms aggregate includes primary first when cleanup fails. | Verify readiness and representative route if startup succeeds. |
| AC-3 | Full website/library/browser/PowerShell checks, package and `git diff --check`. | Record candidate startup against isolated database `test`. |

Regression: existing successful bounded log capture and best-effort asynchronous write-failure behavior remain unchanged.

## Rollback or Recovery
Revert only the process-setup helper and its test if normal deployment logging or returned process ownership changes. If cleanup reports a surviving PID, preserve its diagnostic and stop it using the authorized service/process recovery path.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Cleanup failure masks setup exception | Medium | Aggregate original first and test unchanged rethrow when cleanup succeeds. |
| Process survives tree kill | Low | Bounded wait and explicit PID in aggregate diagnostic. |
| Runtime remains blocked before readiness | High | Save blocked runtime report; do not create PR without required application proof. |

## Implementation Log

### 2026-10-05 - Begin production jar setup cleanup

- **Change:** Started implementation from `695a3ed8`; the existing deployment Pester suite passed all 99 tests before edits.
- **Reason:** Existing coverage proves successful bounded logging but does not cover a process whose post-start log setup fails before the caller receives its handle.
- **Impact:** AC-1/AC-2 implementation begins with a real-child regression for the post-start failure boundary.

### 2026-10-05 - Record process setup runtime blocker

- **Change:** Committed candidate `2be74499` passed the real-child setup-failure regression and full native checks/package, but packaged startup exited before readiness at migration 015; the candidate report records it.
- **Reason:** Isolated database `test` contains an incomplete durable migration record; direct repair or guard bypass is prohibited.
- **Impact:** AC-1 and AC-2 pass; AC-3 is blocked by runtime acceptance. No PR was created; supported test fixture provisioning or recovery is required.

## Outcome

> [!WARNING]
> Candidate process ownership and native checks are complete; application delivery remains runtime-blocked because startup cannot pass migration 015 on isolated database `test`.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | A real sleeping child was stopped, bounded and disposed after injected post-start writer setup failure. |
| AC-2 | ✅ Met | The original `InvalidOperationException` object was rethrown unchanged after successful cleanup; code aggregates the primary first when cleanup also fails. |
| AC-3 | ⚠️ Partly met | Targeted and full checks/package pass; [candidate report](../test-reports/2026-10-05-03-11-christopherbell-dev-bound-production-jar-setup-failure-cleanup.md) records startup blocked before readiness. |

The change is committed on its isolated spoke branch. No PR was opened. Resume runtime verification after supported isolated test fixture provisioning or recovery is available; do not modify migration records directly or bypass the guard.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
