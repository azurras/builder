# Application Architecture Tests Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Slice 20 conforms to write-chris-street-style-code with unchanged behavior.

## Background
Slice 20 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) covers test-only code that no feature slice owns: the 28 `architecture` tests (4,892 lines) and `testsupport.HeadersThenStallServer`. With the architecture suppression removed, Checkstyle reported 45 mechanical violations. `LegacyModuleDependencyRules` also tests an `Optional` with `isEmpty() || get()`. `testsupport` already conforms.

## Goals
- Every file in scope conforms (AC-1, AC-2).
- Behavior is unchanged (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Behavior, contract or layout changes | The migration preserves behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in scope |
| AC-2 | The full check passes and a full-diff style review finds no blocker |
| AC-3 | The architecture and full test suites pass with Checkstyle covering the architecture tests |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the files in scope at spoke `origin/main` `a0709b0e`.

## Branch
`claude/style-app-tests-20261012` from spoke `origin/main`; it merges `origin/main` before its PR when an earlier slice has changed the same file.

## Assumptions
None.

## Open Questions
None.

## Design
- **Mechanical rules:** applied by the checked fixers on the reported lines, and the architecture suppression line is removed.
- **`LegacyModuleDependencyRules`:** reads the physical area with `map("permission"::equals).orElse(true)`, which is the same truth table as before.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/test/java/dev/christopherbell/architecture/*` flagged files | changed | Block bodies, imports, `Optional` read |
| `website/src/test/java/dev/christopherbell/testsupport/HeadersThenStallServer.java` | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The slice 20 line is removed |

## Task Breakdown

### Task 1 - Conform slice 20

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | As named in Design |
| **Inspection** | Inputs |
| **Behavior** | Unchanged |
| **Invariants** | No route, contract, stored field or rendered value changes |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | As in Test Plan |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

**Runtime proof not applicable:** the slice changes test sources only. No application code, configuration or dependency changes, so the full test run is the proof.

| AC | Check |
|---|---|
| AC-1 | Plan review against the diff |
| AC-2 | Full check with Checkstyle |
| AC-3 | Architecture suite inside the full check |
| AC-4 | Required PR checks and `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| An architecture rule silently changes meaning | Low | The rule tests (`LegacyModuleDependencyRulesTest`) exercise the permission-area branch |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** These are mechanical or Settled-Decision edits made while earlier slices merged.
- **Impact:** No PR exists yet; the plan and evidence are published before it.

### 2026-10-12 - Merged main before the PR

- **Change:** The branch merged `origin/main` `f1c0269`, resolving the suppressions file. Checkstyle and the architecture tests were rerun on `f4564de1`.
- **Reason:** The shared-folder slices removed neighboring suppression lines.
- **Impact:** None on scope. The full check passed on `0b8f4154` before the merge.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
