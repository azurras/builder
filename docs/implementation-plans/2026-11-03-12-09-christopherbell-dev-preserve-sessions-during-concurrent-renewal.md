# Preserve sessions during concurrent renewal

## Document Status
in-progress

## Objective
> [!IMPORTANT]
> Concurrent valid activity retains authentication while deleted, expired or fingerprint-invalid sessions remain rejected.

## Background
The user selected all nine security/concurrency findings from the November 3 scan for repair. This independent change addresses the matching finding on refreshed main 5e1126f0, rather than relying on the older scan baseline.

## Goals
- Concurrent valid activity retains authentication while deleted, expired or fingerprint-invalid sessions remain rejected. (AC-1).
- Deliver verified code and records through the normal merge and deployment pipeline (AC-2).

## Non-Goals
| Not doing | Why |
|---|---|
| Unselected audit expansion or production data maintenance | The request selects the nine reported defects |
| Changing product permissions or user workflows | Preserve existing behavior except the defect |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Concurrent valid activity retains authentication while deleted, expired or fingerprint-invalid sessions remain rejected. Deterministic regression checks fail before and pass after the correction. |
| AC-2 | Candidate runs locally with isolated database test, runtime report is published, PR passes CI and merges, deployment identity is read back, and dated delivery memory is published. |

## Inputs
- **Request:** Fix findings 1 through 9 from this chat.
- **Inspected:** Refreshed main 5e1126f0; website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java; website/src/test/java/dev/christopherbell/configuration/security/browser/BrowserSessionServiceTest.java; owning feature instructions and existing callers reviewed in this session and the preceding source scan.
- **Related work:** Other selected findings have their own independent plans; post persistence findings share one coupled plan.

## Branch
`codex/fix-scan-20261103` from `origin/main` at `5e1126f0`, isolated linked worktree. Independent changes share one reviewed delivery candidate and retain separate reports.

## Assumptions
- Existing API routes and authorization contracts remain compatible.
- Disposable exact test-profile MongoDB is available through the repository candidate helper.

## Open Questions
None. Routine implementation details are delegated to source inspection and regression evidence.

## Design
On a lost activity CAS reload the authoritative session and account and revalidate without another renewal or cookie rotation. The Builder delivery contract already authorizes these corrective implementation choices and publication; no additional product decision is introduced.

| Alternative | Why not |
|---|---|
| Add a process-local mutex or disable overlapping requests | Does not establish the actual cross-request storage or late-response invariant |
| Rewrite the feature | Unnecessary compatibility and scope risk |

## Expected Changes
| File or area | Change |
|---|---|
| website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java and its persistence/helper interfaces and callers | On a lost activity CAS reload the authoritative session and account and revalidate without another renewal or cookie rotation. |
| website/src/test/java/dev/christopherbell/configuration/security/browser/BrowserSessionServiceTest.java and adjacent native integration contracts | Deterministic reproduction and regression evidence |
| Owning feature README | Describe the corrected concurrency or boundary contract |

## Task Breakdown
### Task 1 - Correct the selected invariant
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None; coordinate shared build execution with the parent. |
| **Files** | website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java; website/src/test/java/dev/christopherbell/configuration/security/browser/BrowserSessionServiceTest.java; adjacent persistence ports, callers, and feature README. |
| **Symbols** | Existing affected entrypoint and storage/browser completion functions; preserve public DTO shape. |
| **Inspection** | Current baseline 5e1126f0 implementation, affected callers and native tests; recheck all touched seams before edits. |
| **Behavior** | Concurrent valid activity retains authentication while deleted, expired or fingerprint-invalid sessions remain rejected. |
| **Invariants** | Current permissions, valid credentials, unrelated state and successful concurrent mutations remain authoritative. |
| **Boundary/API** | Preserve supported routes and response envelopes; reject invalid or stale work through existing error conventions. |
| **Effects and failures** | Own each write or asynchronous completion; propagate causal failures; never resurrect revoked/deleted state. |
| **Tests and evidence** | Add controlled failing regression first; run focused native tests then appropriate wider checks and actual candidate behavior. |
| **Verification** | Windows Invoke-Gradle.ps1 :website:check :cbell-lib:check :website:bootJar; node syntax/tests for browser changes; verify-local-app candidate proof. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused deterministic regression and affected contract tests; broader website and library checks | Authenticate through concurrent interactive requests after controlled idle state using test-only fixtures and inspect status and Set-Cookie. |
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

### 2026-11-03 - Activity contention reproduced and repaired

**Change:** Regression reproduced touch CAS loser rejection; reload now validates current session/account and returns authentication without another renewal.

**Reason:** Contention is not invalid credentials; revocation, expiry and fingerprint mismatches must still reject.

**Impact:** 43 combined routing/session tests pass; candidate runtime still required.

### 2026-11-03 - Final candidate verification

**Change:** Completed native checks before launching committed candidate `406620306cf4e4a97e6c7240747b0a7f057a91f6`; then executed isolated HTTP, browser and production catalog-consumer proof without rebuilding the running artifact.

**Reason:** Final evidence must identify the exact reviewed candidate. Earlier timed-out or build-invalidated attempts are superseded explicitly in the report.

**Impact:** Native checks passed (2,192 website tests, 126 library tests; zero failures). All scoped runtime cases and owned-process/listener cleanup passed. Published runtime reports retain inputs, outputs and limits; PR/CI and automatic deployment remain the next delivery phase.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
