# Preserve Interruption in Process Output Readers

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Process output collection propagates caller interruption to the process owner so cancellation, interrupt restoration, and process termination follow the existing contract.

## Background
Two bounded process-output readers catch `Exception` around `Future.get`. That also catches `InterruptedException`, returns truncated output, and suppresses the caller's cancellation signal. Their outer process owners already contain interruption branches that restore the interrupt flag and terminate the process, but those branches cannot run when interruption occurs during output collection.

## Goals
- Both output readers preserve interruption and let their existing process owners restore interruption and terminate the process (AC-1).
- Timeout, execution failure, and cancelled output tasks keep the existing bounded truncated-output fallback (AC-2).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing process timeout, output limits, exit codes, or termination behavior | Those are separate contracts and are not needed to preserve interruption |
| Refactoring process lifecycle or adding a shared process abstraction | The two owners have different dependencies and only share this narrow failure rule |
| Changing sensor availability or media-probe results for ordinary process failures | Preserve current behavior outside interruption |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | An interruption during either output wait cancels the reader and propagates to the existing owner handler, which restores the interrupt flag, terminates the process, and returns the existing interrupted/timed-out result |
| AC-2 | Timeout, execution failure, and cancellation still return empty truncated output and the existing callers retain their current behavior |
| AC-3 | The change is merged through the required spoke PR/CI flow and its supported deployment/runtime state is read back |

## Inputs
- **Request:** User requested a whole-code Chris Street Style audit, small targeted changes, and an individual plan and test report for each change; user explicitly rejected draft PR #1477 as trustworthy evidence.
- **Inspected:** `christopherbell.dev` clean branch `codex/chris-street-style-codebase-20261004` at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`; both process owners, output readers, existing sensor tests, process interfaces, root `AGENTS.md`, Gradle tasks, and Builder Java, API/concurrency, naming, testing, and adaptation references.
- **Baseline:** `:website:check :cbell-lib:check` passed on this branch; isolated candidate startup on port 8081 against a restored temporary Mongo database on port 27018 returned readiness 200 and `GET /` 200. This is baseline evidence only.

## Branch
`codex/chris-street-style-codebase-20261004` from website `origin/main` at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`.

## Assumptions
- The outer `InterruptedException` branches express the intended owner contract because they restore interruption, terminate the process, and produce explicit interrupted results.
- The established empty/truncated fallback remains correct for output timeout, failed reader execution, and cancellation.

## Open Questions
None.

## Design
Narrow each `Future.get` catch to its expected non-interruption failures and declare `InterruptedException` from the output-wait helper. Keep interruption handling at each existing process owner, where termination and the outward result are controlled. If the production methods cannot be tested through existing seams, extract only the shared future-wait logic into package-private helpers and test those with completed, timed-out, failed, cancelled, and interrupted futures; interruption tests must fail on the baseline implementation.

| Alternative | Why not |
|---|---|
| Keep catching `Exception` and inspect the interrupt flag afterward | This loses the original interruption distinction and can race with unrelated interrupt state |
| Return a third output state and handle it after each stream | Adds state when Java's checked interruption already models the case |
| Remove fallback handling for reader failures | Would change current timeout and bounded-output behavior unnecessarily |

## Expected Changes

| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/music/catalog/JdkMusicProcessRunner.java` | Preserve `InterruptedException` from bounded-output future waits; retain fallback for expected reader failures |
| `website/src/test/java/dev/christopherbell/music/catalog/JdkMusicProcessRunnerTest.java` | Add focused tests for interrupted and ordinary future outcomes |
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbe.java` | Preserve interruption from managed process output waits; retain fallback for expected reader failures |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbeTest.java` | Add focused tests for interrupted and ordinary future outcomes using a narrow package test seam if needed |

## Task Breakdown

### Task 1 - Preserve interruption while collecting bounded process output

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | The two production classes and focused test classes named above; root `AGENTS.md`; `website/build.gradle.kts` |
| **Symbols** | `JdkMusicProcessRunner.result`; `PowerShellCpuTemperatureProbe.JdkManagedProcess.output`; both outer interruption branches |
| **Inspection** | Read method bodies, callers, test seams, Gradle tasks, and process contracts at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b` |
| **Behavior** | Interruption during stream result collection reaches the process owner; expected future failures keep the bounded truncated-output fallback |
| **Invariants** | Preserve output cap, grace timeout, process termination, interrupt restoration, exit-code/timed-out semantics, and caller behavior |
| **Boundary/API** | Keep public constructors and `MusicProcessRunner` unchanged; any test seam remains package-private or private |
| **Effects and failures** | Process owners remain responsible for termination; output helpers cancel tasks on failure and do not swallow interruption |
| **Tests and evidence** | First add deterministic future-backed tests and observe baseline interruption failures; then pass focused tests, `:website:check :cbell-lib:check`, and isolated runtime proof on the committed candidate |
| **Verification** | `./gradlew.bat :website:test --tests '*JdkMusicProcessRunnerTest' --tests '*PowerShellCpuTemperatureProbeTest'`; `./gradlew.bat :website:check :cbell-lib:check`; start candidate with isolated Mongo/port, check readiness and `GET /`, verify logs/listener/cleanup |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Deterministic interrupted-`FutureTask` tests assert `InterruptedException` propagation and reader cancellation; inspect existing owner handlers for interrupt restoration and process termination | Run committed candidate on isolated test profile; readiness and home page return 200 |
| AC-2 | Timeout, failed, and cancelled future tests assert empty truncated fallback; run full website and library checks | Same candidate returns readiness 200 and home page 200 with integrations and scheduling disabled |
| AC-3 | Required PR checks and merge readback | Read supported deployment status and revision; no manual process rotation |

Regression cases:
- The interruption regression fails against pre-change code because the helper converts interruption to truncated output.
- Timeout or reader failure does not escape as a new exception or change bounded output behavior.
- Candidate uses only the isolated copied database and port 8081; production ports 8080 and 27017 remain untouched.

## Rollback or Recovery
Before merge, revert this focused change if tests or candidate verification fail. After merge, use the reviewed spoke revert PR and supported automatic deployment path; do not manually rotate production. No data or schema changes are involved.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Test seam exposes implementation details | Low | Keep any deterministic test seam package-private; production API remains unchanged |
| Narrow catches omit a future failure mode | Low | Explicitly cover timeout, execution failure, cancellation, and interruption from `Future.get` |
| Candidate proof reaches live resources | Low | Use temporary Mongo and copied allowlisted database, isolated port 8081, disabled scheduling/integrations, and verify actual connection logs |

## Implementation Log

### 2026-10-04 - Keep deterministic tests at a narrow boundary

- **Change:** The design allows a package-private future-wait seam only if existing construction seams cannot directly exercise the interruption case.
- **Reason:** The production JDK process wrappers are private and start OS processes, while the defect is specifically the checked exception contract of `Future.get`; a tiny seam makes interruption deterministic without changing public APIs or invoking a real child process in unit tests.
- **Impact:** Public process contracts and runtime behavior remain unchanged except that interruption now reaches existing owner handling.

### 2026-10-04 - Verify interruption propagation on the committed candidate

- **Change:** Added deterministic direct-boundary tests and package-private `awaitOutput` helpers; interruption is rethrown after reader cancellation, while `ExecutionException`, `TimeoutException`, and `CancellationException` keep the empty/truncated fallback. The focused regressions failed on clean baseline and passed on candidate `d1d8b79c`.
- **Reason:** The original broad catches swallowed `InterruptedException`; deterministic `FutureTask` tests exposed the defect without OS-specific process timing and verified the existing ordinary-failure contract.
- **Impact:** Task 1 implementation and Test Plan now describe the package-private test boundary; AC-1 and AC-2 are locally verified in [the candidate test report](../test-reports/2026-10-04-23-15-christopherbell-dev-preserve-interruption-in-process-output-readers.md). PR, merge and deployment acceptance remain pending.

## Outcome

> [!WARNING]
> Pending implementation and delivery.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | Pending | Pending |
| AC-2 | Pending | Pending |
| AC-3 | Pending | Pending |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
