# Bound Shared Folder Media Process Cleanup

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Keep media-worker cancellation and timeout handling bounded even when process-tree termination fails, while preserving the original job failure and identifying any surviving child process.

## Background
`Invoke-PinnedMediaTool` in `Production.SharedFolderWorker.psm1` catches cancellation, timeout, and launch/read failures, attempts `Process.Kill($true)`, catches only `InvalidOperationException`, then calls unbounded `WaitForExit()` and waits on output-reader tasks. If termination fails while the child remains alive, cleanup can exceed the job deadline and mask the original failure.

## Goals
- Bound child cleanup and reader draining after cancellation or failure (AC-1).
- Preserve the initiating failure and surface termination/reaping failures, including a surviving process identity (AC-2).
- Add focused PowerShell regressions and run packaged application verification for the committed candidate (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change media job deadline, cancellation markers, or successful output behavior | Those contracts are independent of failure cleanup. |
| Change production deployment launch behavior | That is a separate reviewed finding and needs its own plan. |
| Guarantee the operating system always terminates an uncooperative child | The runner can bound its own wait and report remaining process state, but cannot force OS-level termination after a termination API failure. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Failure cleanup uses bounded process and reader waits and does not block past its cleanup budget. |
| AC-2 | The original timeout/cancellation/operation error remains available when cleanup also fails; diagnostics identify cleanup failure and a still-running process. |
| AC-3 | Focused PowerShell regressions and full native checks pass; the committed packaged application receives a local startup attempt and candidate-specific report before any PR. |

## Inputs
- **Request:** Full `christopherbell.dev` Chris Street Style audit with small targeted fixes and a separate plan/report per correction; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected source:** `ops/production/windows/modules/Production.SharedFolderWorker.psm1`, especially `Invoke-PinnedMediaTool` cleanup, at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected tests:** `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`, including cancellation, timeout, process-tree and output-reader coverage at the same baseline.
- **Guidance:** Spoke root `AGENTS.md`; Chris Street Style PowerShell, language adaptation, naming, design/API, and test-review references.

## Branch
Create `codex/bound-shared-folder-process-cleanup-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6` after publishing this plan.

## Assumptions
- Cancellation/timeout must remain the primary reported outcome when cleanup also encounters an OS/process failure.
- A small fixed cleanup grace interval is suitable because job deadlines can already be expired when cleanup starts.
- The established isolated test database remains blocked by migration 015; runtime proof is still required and may remain blocked.

## Open Questions
None. Keep process ownership inside the runner and cleanup bounded.

## Design
Move child reaping into a small, testable helper that attempts tree termination, waits for process exit only within a fixed grace interval, and only drains readers after confirmed exit. Return or collect cleanup failures instead of replacing the active exception; include PID and remaining-running state when the child outlives the grace interval. Combine cleanup diagnostics with the original failure at the outer catch boundary. Keep successful output capture and existing truncation limits unchanged.

| Alternative | Why not |
|---|---|
| Keep unbounded `WaitForExit()` | Cleanup can outlive the job deadline indefinitely. |
| Ignore every termination failure | Hides a potentially surviving child and loses actionable diagnostics. |
| Wait on reader tasks when the process remains alive | Stream readers can remain blocked until child handles close. |

## Expected Changes
| File or area | Change |
|---|---|
| `ops/production/windows/modules/Production.SharedFolderWorker.psm1` | Bound process/readers cleanup and preserve initiating and cleanup failures. |
| `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1` | Add regression coverage for termination failure and bounded surviving-child diagnostics. |

## Task Breakdown
### Task 1 - Bound process failure cleanup
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the worker module and its Pester suite at base `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `Invoke-PinnedMediaTool`, its process kill/wait/read cleanup path, and cancellation/timeout tests. |
| **Inspection** | Existing normal timeout/cancellation coverage assumes `Kill($true)` succeeds; cleanup waits are unbounded and termination catches only `InvalidOperationException`. |
| **Behavior** | Successful execution/output is unchanged; cancellation and timeout remain primary failures; cleanup cannot wait indefinitely. |
| **Invariants** | Do not leave reader tasks awaited after a surviving child; preserve process-tree termination attempt and output limits; dispose owned process handles. |
| **Boundary/API** | No media manifest, service, job or client contract changes. |
| **Effects and failures** | Child process and redirected streams stay owned by the runner; surface cleanup failures with the original cause and surviving PID where relevant. |
| **Tests and evidence** | Establish focused Pester baseline, then prove the injected termination-failure path returns within a bounded interval and retains original and cleanup diagnostics. |
| **Verification** | Run focused Pester suite, all native website/library/browser/PowerShell checks, package the application, then attempt local packaged startup with isolated test settings and save runtime report. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Pester regression proves termination failure cannot cause unbounded process or reader waits. | Launch committed packaged application with jobs and integrations disabled. |
| AC-2 | Assert original cancellation/timeout remains present alongside kill failure and surviving PID. | Verify readiness and a representative route if startup succeeds. |
| AC-3 | Full native project checks and package; `git diff --check`. | Record startup and route result using isolated MongoDB `test`. |

Regression: normal media execution, output truncation, timeout kill and pre-canceled no-start behavior stay unchanged.

## Rollback or Recovery
Revert the isolated helper/test change if successful output or cancellation behavior changes. A reported surviving child requires operator cleanup according to service ownership; do not silently abandon its identity.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Cleanup grace is too short on a slow Windows host | Low | Use a fixed, explicit interval and report if the child survives. |
| Aggregation obscures the primary timeout/cancellation | Medium | Assert both exception identities/messages and maintain primary failure first. |
| Runtime remains blocked before application readiness | High | Record startup failure and do not create a PR without required runtime proof. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
