# Preserve messages during overlapping browser actions

## Document Status
complete

## Objective
> [!IMPORTANT]
> A late archive does not clear a newer conversation, and send completion does not erase a newer draft.

## Background
The user selected all nine security/concurrency findings from the November 3 scan for repair. This independent change addresses the matching finding on refreshed main 5e1126f0, rather than relying on the older scan baseline.

## Goals
- A late archive does not clear a newer conversation, and send completion does not erase a newer draft. (AC-1).
- Deliver verified code and records through the normal merge and deployment pipeline (AC-2).

## Non-Goals
| Not doing | Why |
|---|---|
| Unselected audit expansion or production data maintenance | The request selects the nine reported defects |
| Changing product permissions or user workflows | Preserve existing behavior except the defect |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | A late archive does not clear a newer conversation, and send completion does not erase a newer draft. Deterministic regression checks fail before and pass after the correction. |
| AC-2 | Candidate runs locally with isolated database test, runtime report is published, PR passes CI and merges, deployment identity is read back, and dated delivery memory is published. |

## Inputs
- **Request:** Fix findings 1 through 9 from this chat.
- **Inspected:** Refreshed main 5e1126f0; website/src/main/resources/static/js/messages.js; website/src/test/js/messages-rendering.test.js; owning feature instructions and existing callers reviewed in this session and the preceding source scan.
- **Related work:** Other selected findings have their own independent plans; post persistence findings share one coupled plan.

## Branch
`codex/fix-scan-20261103` from `origin/main` at `5e1126f0`, isolated linked worktree. Independent changes share one reviewed delivery candidate and retain separate reports.

## Assumptions
- Existing API routes and authorization contracts remain compatible.
- Disposable exact test-profile MongoDB is available through the repository candidate helper.

## Open Questions
None. Routine implementation details are delegated to source inspection and regression evidence.

## Design
Capture recipient and selection generation for archive/send completion; clear only the submitted unchanged draft and update only the matching view. The Builder delivery contract already authorizes these corrective implementation choices and publication; no additional product decision is introduced.

| Alternative | Why not |
|---|---|
| Add a process-local mutex or disable overlapping requests | Does not establish the actual cross-request storage or late-response invariant |
| Rewrite the feature | Unnecessary compatibility and scope risk |

## Expected Changes
| File or area | Change |
|---|---|
| website/src/main/resources/static/js/messages.js and its persistence/helper interfaces and callers | Capture recipient and selection generation for archive/send completion; clear only the submitted unchanged draft and update only the matching view. |
| website/src/test/js/messages-rendering.test.js and adjacent native integration contracts | Deterministic reproduction and regression evidence |
| Owning feature README | Describe the corrected concurrency or boundary contract |

## Task Breakdown
### Task 1 - Correct the selected invariant
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None; coordinate shared build execution with the parent. |
| **Files** | website/src/main/resources/static/js/messages.js; website/src/test/js/messages-rendering.test.js; adjacent persistence ports, callers, and feature README. |
| **Symbols** | Existing affected entrypoint and storage/browser completion functions; preserve public DTO shape. |
| **Inspection** | Current baseline 5e1126f0 implementation, affected callers and native tests; recheck all touched seams before edits. |
| **Behavior** | A late archive does not clear a newer conversation, and send completion does not erase a newer draft. |
| **Invariants** | Current permissions, valid credentials, unrelated state and successful concurrent mutations remain authoritative. |
| **Boundary/API** | Preserve supported routes and response envelopes; reject invalid or stale work through existing error conventions. |
| **Effects and failures** | Own each write or asynchronous completion; propagate causal failures; never resurrect revoked/deleted state. |
| **Tests and evidence** | Add controlled failing regression first; run focused native tests then appropriate wider checks and actual candidate behavior. |
| **Verification** | Windows Invoke-Gradle.ps1 :website:check :cbell-lib:check :website:bootJar; node syntax/tests for browser changes; verify-local-app candidate proof. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused deterministic regression and affected contract tests; broader website and library checks | Run actual candidate browser modules with deferred responses; switch conversations and type a new draft before releasing responses. |
| AC-2 | Full required checks, branch semantic review, PR/CI and merge readback | Start-Candidate.ps1 exact test profile, verify database isolation before/after, exercise changed behavior, Stop-Candidate.ps1 and listener cleanup; publish write-test-report before PR creation. |

Rerun affected local evidence after runtime-affecting edits. Record commands and outputs as executed with record_run.py. No tests or fixtures use production data.

## Rollback or Recovery
Revert the scoped commit through a verified PR if necessary. No production data migration is planned. Preserve unrelated work and never discard another session's changes.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A sibling writer or late response bypasses the correction | Medium | Trace callers and test distinct interleavings at the actual boundary |
| Unit fixtures conceal production semantics | Medium | Real Mongo/servlet/browser proof on the local candidate |

## Implementation Log

### 2026-11-03 - Late completions and refresh failures guarded

**Change:** Two Node regressions reproduced archive selection loss and send draft loss; completion guards now include selection/input generations. Review found suppressed current refresh errors; fixed with stage-specific generations and three additional tests.

**Reason:** Keep newer user work authoritative while preserving visible failures for the current view.

**Impact:** All14 focused Node checks pass; browser proof remains. Tests live in existing message fixture.

### 2026-11-03 - Final candidate verification

**Change:** Completed native checks before launching committed candidate `406620306cf4e4a97e6c7240747b0a7f057a91f6`; then executed isolated HTTP, browser and production catalog-consumer proof without rebuilding the running artifact.

**Reason:** Final evidence must identify the exact reviewed candidate. Earlier timed-out or build-invalidated attempts are superseded explicitly in the report.

**Impact:** Native checks passed (2,192 website tests, 126 library tests; zero failures). All scoped runtime cases and owned-process/listener cleanup passed. Published runtime reports retain inputs, outputs and limits; PR/CI and automatic deployment remain the next delivery phase.

## Outcome
> [!TIP]
> Delivered findings 8 and 9; verified candidate `40662030` merged and deployed through the supported CI-gated pipeline.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met: selected invariants and negative cases pass native regression checks and actual local execution | [Runtime report](../test-reports/2026-11-03-16-13-christopherbell-dev-preserve-messages-during-overlapping-browser-actions.md) |
| AC-2 | ✅ Met: [PR #1557](https://github.com/azurras/christopherbell.dev/pull/1557) is MERGED as `908a51597d30f58b823cbf5c006529f5769cc2af`; required CI passed; automatic deployment readback passed; dated delivery memory published with this completed plan | [PR](https://github.com/azurras/christopherbell.dev/pull/1557), [production identity](https://www.christopherbell.dev/actuator/info), [dated memory](../session-memory/2026-11-03.md) |

No source issue; external closure does not apply. Details of independent review findings, corrections, failed attempts and reruns are preserved in Implementation Log and the runtime report. No further defect from this selected group is left pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
