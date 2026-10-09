# What's for Lunch Workflow Engine Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The What's for Lunch workflow engine conforms to write-chris-street-style-code and behaves as before.

## Background
This is slice 17a of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Slice 17 (whatsforlunch: 96 main and 18 test files) is split by package, smallest first:

| Part | Scope |
|---|---|
| 17a | Workflow engine (18 main files, 2 tests) |
| 17b | Restaurant importing and configuration |
| 17c | Restaurant core: service, controller, models, sessions, votes |
| 17d | Front end |

Inspection at `3f4af8b1` found:

1. **Hidden time.** `WorkflowExecutor` and `WhatsForLunchWorkflow` call `Instant.now()` eleven times.
2. **Broad catches.** `catch (Exception e)` appears where only runtime exceptions can be thrown.
3. **Duplication and layout:**
   - Three identical result builders.
   - A `try` block indented by five spaces.
   - Public helper methods that only the executor uses.
4. **Naming:**
   - An unused pattern variable.
   - `ctx` parameters.
   - `getType()` names its own constant instead of calling `name()`.
   - `Workflow.execute` Javadoc says it returns the context.

The package has no production caller: only its own two tests use it. Removing it is a product decision, outside a conformance slice, so it is recorded as a follow-up.

## Goals
- Every workflow file has a recorded verdict and conforms (AC-1, AC-2).
- The application still starts and serves What's for Lunch (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Deleting the unused workflow package | Removing a feature's code is the owner's decision; recorded as a follow-up |
| Making the retry loop wait `retryDelay` before retrying | It logs a delay but retries immediately; changing that is a behavior change in unused code |
| Removing the log-only `stopWorkflowExecution`, `monitorWorkflowStatus` and `notifyWorkflowCompletion` methods | Public API of the unused package; it goes with the follow-up decision |
| `WhatsForLunchWorkflowResult.builder()` returning the parent type | Lombok `@Builder` inheritance; changing it changes the result type |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every workflow file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the candidate reaches readiness with both workflow beans constructed from the application `Clock`, and `/whatsforlunch` and the restaurant list answer as production does |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `3f4af8b1`:
  - All 18 files under `whatsforlunch/workflow`.
  - `WorkflowExecutorTest` and `WhatsForLunchWorkflowTest`.
  - A repository-wide search for `whatsforlunch.workflow` outside the package, which found no caller.

## Branch
`claude/style-lunch-workflow-20261009` from spoke `origin/main` `3f4af8b1`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.

## Open Questions
None.

## Design
- **Clock:** both components take the application `Clock` through their single constructor.
- **Catches:** they catch `RuntimeException`. `Workflow.execute` and `Operation.execute` declare no checked exceptions, so the set of caught failures is unchanged.
- **Result builder:** `resultWithStatus` builds every failure result.
- **Helpers:** the success, stop and save helpers become private `markCompleted`, `markStopped` and `saveContext`. Their return values were unused.
- **Javadoc:** `executeOperation` and `executeWorkflow` document that failures become statuses.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/workflow/engine/WorkflowExecutor.java` | changed | Injected `Clock`, narrow catches, one result builder, private helpers, `@Override`, indentation |
| `website/src/main/java/dev/christopherbell/whatsforlunch/workflow/WhatsForLunchWorkflow.java` | changed | Injected `Clock`; no unused pattern variable |
| `website/src/main/java/dev/christopherbell/whatsforlunch/workflow/WhatsForLunchWorkflowType.java` | changed | `name()` |
| `website/src/main/java/dev/christopherbell/whatsforlunch/workflow/engine/Workflow.java`, `engine/operation/Operation.java` | changed | `context` parameters; true Javadoc |
| The other 13 workflow main files | conforming | No change |
| `website/src/test/java/dev/christopherbell/whatsforlunch/workflow/engine/WorkflowExecutorTest.java`, `WhatsForLunchWorkflowTest.java` | changed | Construct with a `Clock` |

## Task Breakdown

### Task 1 - Conform the workflow engine

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `WorkflowExecutor`, `WhatsForLunchWorkflow`, `WhatsForLunchWorkflowType.getType`, `Workflow.execute`, `Operation.execute` |
| **Inspection** | All files in Inputs at `3f4af8b1` |
| **Behavior** | Same statuses, history entries, retries and exceptions |
| **Invariants** | No route, job or stored data uses the package |
| **Boundary/API** | Both constructors take a `Clock`; four helper methods become private |
| **Effects and failures** | None new |
| **Tests and evidence** | Workflow tests; startup and lunch reads |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Workflow tests | verify-local-app: readiness, the bean wiring in the startup log, `/whatsforlunch` and the restaurant list compared with production |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Startup fails because a constructor now needs a `Clock` | Low | The application defines one `Clock` bean; the candidate start proves the wiring |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slices 16a and 16b were in progress.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
