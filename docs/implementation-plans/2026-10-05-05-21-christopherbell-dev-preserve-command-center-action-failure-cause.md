# Preserve unexpected command-center action failures

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Translate only expected host-command launch I/O failures into the safe request error while preserving the original I/O cause and allowing programming defects to remain visible.

## Background
`CommandCenterActionService.executeNow` calls the `CommandExecutor` boundary, whose contract declares `IOException`, but catches every `Exception`. This converts unexpected runtime defects into the same failed-launch request outcome and loses the I/O cause. The code has a clear checked failure type, so it can translate that type precisely without changing the safe public message or launch-failure audit behavior.

## Goals
- Limit launch-failure translation and audit to the declared `IOException` outcome (AC-1).
- Preserve the original launch `IOException` as the safe `InvalidRequestException` cause and prove unrelated runtime failures propagate (AC-2).
- Pass native checks and attempt committed local app verification, or record the verified test-database blocker with no PR (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing accepted admin actions, command arguments, confirmation, audit vocabulary, or safe public error text | This correction narrows failure classification while preserving the existing contract. |
| Changing `CommandExecutor`'s `IOException` signature or Windows process behavior | The declared I/O boundary already represents expected process-launch failures. |
| Editing or relying on PR #1477 | The user explicitly excluded the pre-style draft. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `executeNow` records `launch-failed` and returns the safe request error for `IOException`, without translating unrelated runtime defects. |
| AC-2 | Tests assert the safe exception message and original IOException cause, and prove an unexpected `IllegalStateException` propagates. |
| AC-3 | The committed package passes full native checks and local runtime verification uses verified isolated test resources, or the exact blocker is reported and no PR is created. |

## Inputs
- **Request:** User requested a whole-codebase Chris Street Style audit with separate plan/report per correction; PR #1477 is excluded.
- **Inspected revision:** Website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Instructions:** Builder and website AGENTS.md plus Builder Chris Street Style naming/readability, design/API, Java, and testing references.
- **Inspected contract:** `CommandExecutor.execute(CommandCenterActionType)` declares `IOException`; `WindowsCommandExecutor` emits `IOException` for unsupported host, timeout, nonzero exit, and interrupted waits; `InvalidRequestException` supports a cause constructor.

## Branch
`codex/preserve-command-action-failure-cause-20261005` from website `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.

## Assumptions
- `IOException` is the intended recoverable launch failure because it is the explicit `CommandExecutor` checked failure contract.
- Runtime exceptions are not part of that contract and should propagate to ordinary server failure handling.
- The read-only isolated MongoDB preflight may remain unavailable; startup must not run without verified test database identity.

## Open Questions
None.

## Design
In `executeNow`, catch only `IOException`, keep auditing the expected launch failure, and construct `InvalidRequestException` with the existing safe message and the I/O exception as its cause. Leave success auditing after the try block. Add one characterization to the existing I/O launch-failure test and one focused runtime-defect test using the same immediate action setup. This keeps the action executor boundary and recovery policy direct.

| Alternative | Why not |
|---|---|
| Keep catching all `Exception` | It erases the declared `IOException` boundary and hides programming defects as ordinary launch failure. |
| Expose the process error message to the API | Process details are not needed by the caller and may reveal host-specific information. |
| Wrap in a new exception type | The existing `InvalidRequestException` already provides the required safe API boundary and causal chain. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java` | Catch `IOException` only and preserve it as the cause of the safe request exception. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionServiceTest.java` | Assert cause preservation for an expected I/O launch failure and propagation of an unrelated runtime defect. |

## Task Breakdown
### Task 1 - Keep host action I/O failures distinct from defects
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Command service and its existing test class, inspected on `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `CommandCenterActionService.executeNow`; `CommandExecutor.execute`; `failedPowerLaunchDoesNotLeaveAPhantomPendingAction`; new unexpected failure regression. |
| **Inspection** | Read action service orchestration, executor interface and Windows implementation, safe exception type, admin instructions, and existing action tests. |
| **Behavior** | Expected process I/O failure still audits the failed launch and yields the same safe request message; successful actions and other failures retain their prior outcomes. |
| **Invariants** | Never expose host command details; roll back pending state after a failed synchronous action; do not classify programming defects as command I/O failures. |
| **Boundary/API** | Keep challenge/action routes and safe `InvalidRequestException` message unchanged; preserve causal `IOException` internally. |
| **Effects and failures** | `CommandExecutor` owns host process I/O; only its declared `IOException` is translated and audited as launch failure. |
| **Tests and evidence** | Run `CommandCenterActionServiceTest` on baseline; characterize IOException cause and unexpected runtime propagation; run full native checks. |
| **Verification** | Focused Gradle service test; full `:website:check :cbell-lib:check :website:bootJar`; committed candidate runtime against isolated test MongoDB if preflight succeeds. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing failed-launch recovery test remains passing; focused test checks `launch-failed` recovery path. | Run committed app and verify readiness and a representative command-center read if DB isolation is available. |
| AC-2 | Assert safe message and original IOException cause; assert unrelated IllegalStateException propagates. | Exercise only read-only command-center state; do not invoke host actions during local runtime verification. |
| AC-3 | Full website/library/browser/PowerShell/package gate passes on committed candidate. | Verify candidate readiness using isolated MongoDB `test`, or record exact preflight/startup blocker and cleanup. |

Regression cases:
- Expected process I/O failure remains an audited safe request error and clears phantom pending state.
- Unexpected executor defects propagate and are not mislabeled as a recoverable host launch failure.
- Successful command execution and completion-audit handling remain unchanged.

## Rollback or Recovery
Revert the isolated correction if I/O launch failures no longer return the safe request error or pending-action rollback regresses. If database isolation cannot be proven, do not start the app, perform host actions, alter database state, or create a PR.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A production executor relies on an undeclared checked exception being translated | Low | Verify all implementations against `CommandExecutor` and keep its explicit IOException semantics. |
| The cause is exposed by an error serializer | Low | Confirm the exception handler emits only the safe message and never serializes cause details. |
| Local runtime remains blocked | High based on current database endpoint evidence | Repeat read-only test identity check and stop if unavailable. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
