# Keep Recent Production Problems Visible in Diagnostics

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> A standard user or agent reading `prod.cmd diagnostics` sees the recent warnings and errors, with the top stack frames, even when routine INFO lines have pushed them out of the latest-entries window.

## Background
`diagnostics.json` already publishes the newest 100 structured log entries for standard users. On 2026-10-05 the record held 73 INFO and 21 WARN entries covering about seven hours, so an error from earlier in the day was gone, and entries carry only the first line of an error message. Diagnosing a production failure therefore still needed an administrator to read `C:\ProgramData\christopherbell.dev\logs\application.json.log`. The user approved closing that gap (item 2 of the agent's improvement list). The Builder side is [its own plan](2026-10-05-19-27-builder-close-the-remaining-agent-friction-in-the-builder-loop.md).

## Goals
- Diagnostics add `recentProblems`: the newest 50 WARN and ERROR entries from a much longer stretch of the log (AC-1).
- Problem and log entries carry `errorStack`, the first three redacted `at` frames of the stack trace (AC-2).
- The record stays within its size bound and redaction rules, and existing readers keep working (AC-3).
- Delivered through a merged PR, deployed by the poller, and read back in production (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing log file permissions | The SYSTEM-owned logs folder stays protected; the sanitized record is the supported path |
| Full stack traces or new fields | Bounded, allowlisted fields keep the record safe to share with every local user |
| A schema version bump | The change only adds fields |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `Publish-AutoDeployDiagnostics` writes `recentProblems` with up to 50 WARN/ERROR entries found in the last 10,000 log lines; a Pester test shows an old ERROR survives behind 200 newer INFO lines |
| AC-2 | Entries with `error.stack_trace` carry `errorStack` with at most three redacted frames; a Pester test proves it and that secrets inside frames are masked |
| AC-3 | The size-bound test still passes with `recentProblems` present; `schemaVersion` stays 1; existing diagnostics tests pass |
| AC-4 | The PR is merged after required CI, production serves the merge commit, and `prod.cmd diagnostics` shows `recentProblems` |

## Inputs
- **Inspected:** `ops/production/windows/modules/Production.AutoDeploy.psm1` lines 2073-2290 (`ConvertTo-AutoDeployRedactedText`, `Read-AutoDeployRecentLogEntries`, `Publish-AutoDeployDiagnostics`, `Get-AutoDeployDiagnostics`), `ops/production/windows/tests/Production.AutoDeploy.Tests.ps1` 'operator diagnostics', `docs/operations/windows-production.md` Delegated Operations, `website/src/main/resources/application-prod.yml` logging.
- **Observed:** live `prod.cmd diagnostics` on `49700a7`: 94 entries, 73 INFO and 21 WARN, spanning 15:53 to 22:34 UTC.

## Branch
`claude/diagnostics-recent-problems-20261005` in a linked worktree of christopherbell.dev.

## Assumptions
- Spring Boot's ECS file format nests `error.type`, `error.message` and `error.stack_trace`, as the existing reader already assumes for the first two.

## Open Questions
None.

## Design
Split the per-line conversion out of `Read-AutoDeployRecentLogEntries` into `ConvertTo-AutoDeployLogEntry`, which adds `errorStack`: up to three trimmed lines starting with `at ` from `error.stack_trace`, joined with ` | `, redacted and bounded to 600 characters, or `$null`.

`Read-AutoDeployRecentProblemEntries` reads the last 10,000 lines, keeps only lines whose text matches `"level"\s*:\s*"(WARN|ERROR)"` before parsing JSON (so INFO lines cost a regex test, not a parse), converts them and returns the newest 50.

`Publish-AutoDeployDiagnostics` adds `recentProblems`. When the record is too large it sheds the oldest half of `recentLogEntries` first, then of `recentProblems`.

| Alternative | Why not |
|---|---|
| Grant users read access to the logs folder | Exposes unredacted request data and widens a protected boundary |
| Raise the latest-entries limit | INFO volume still decides what survives |

## Expected Changes

| File or area | Change |
|---|---|
| `ops/production/windows/modules/Production.AutoDeploy.psm1` | New converter and problem reader; `recentProblems` in the record |
| `ops/production/windows/tests/Production.AutoDeploy.Tests.ps1` | Problem window, stack frames, size bound |
| `docs/operations/windows-production.md` | Describe `recentProblems` and `errorStack` |

## Task Breakdown

### Task 1 - Recent problems in diagnostics
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | The three files above |
| **Symbols** | `ConvertTo-AutoDeployLogEntry`, `Read-AutoDeployRecentLogEntries`, `Read-AutoDeployRecentProblemEntries`, `Publish-AutoDeployDiagnostics` |
| **Inspection** | Module lines 2073-2290 and the 'operator diagnostics' tests |
| **Behavior** | Older WARN/ERROR entries and their top frames stay visible |
| **Invariants** | Only allowlisted, redacted fields; record at most 512 KB; schema version 1 |
| **Boundary/API** | Additive JSON fields read by `prod.cmd diagnostics` |
| **Effects and failures** | Reads the log tail each poll; a read failure still falls to the best-effort publisher |
| **Tests and evidence** | Pester cases for the window, the frames and redaction, and the size bound |
| **Verification** | Pester for the AutoDeploy tests; local run of `Publish-AutoDeployDiagnostics` against a fixture log |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Pester problem-window test | Publish against a fixture log under a temporary root and read the record back with `Get-AutoDeployDiagnostics` |
| AC-2 | Pester stack-frame test | The same local run, inspecting `errorStack` |
| AC-3 | Pester size-bound and existing diagnostics tests | Record size from the local run |
| AC-4 | Required CI | `prod.cmd diagnostics` in production after the poller deploys |

## Rollback or Recovery
1. Revert the merge commit on `main`; the poller deploys the revert. Readers ignore the missing field.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Reading 10,000 lines each minute slows the poller | Low | Tail read plus a regex prefilter; measured in the local run |
| A stack frame leaks a secret | Low | Frames go through the same redaction as messages, with a test |

## Implementation Log

### 2026-10-05 - Local verification through a module-scope harness

- **Change:** Candidate `3571135` was verified locally with a harness. It runs the real reader, publisher and `Get-AutoDeployDiagnostics` on a 20,001-line fixture log. Only the SYSTEM-only ACL guards and the SYSTEM task query are replaced in module scope, as the Pester tests do. Evidence was captured with Builder's new `record_run.py`.
- **Reason:** The production status folder requires SYSTEM-only ACLs that a standard user cannot create. The guards are not part of this change, and Pester already covers them.
- **Impact:** Publishing took about 310 ms and produced a 37 KB record. The in-window ERROR kept three frames, with `password=[REDACTED]`. The ERROR outside the 10,000-line window was dropped as designed. The full production Pester suite passed: 910 passed, 0 failed.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
