# Browser JavaScript Branches and Loops Are Braced

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Slice 22 conforms to write-chris-street-style-code with unchanged behavior.

## Background
Slice 22 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) covers shared browser JavaScript (`lib`, `components`, `auth`, `app.js`) and the JS tests no feature owns. A scan for single-line `if`, `else`, `for` and `while` bodies found about 900 more across 66 files. Most are in feature page scripts whose earlier slices were marked done; those slices fixed other smells but missed these forms. A second scan found bare `else statement;` lines after an `if` block. The scan found no loose equality outside deliberate `== null` checks in the What's for Lunch script, no `forEach(async`, and no unescaped dynamic `innerHTML`. Every markup builder that used `innerHTML` already applied `sanitize`.

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
| AC-3 | On isolated MongoDB `test`, the published report records that every changed module is served byte for byte as committed, that the pages using them render, that all 390 JS tests pass and that the log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the files in scope at spoke `origin/main` `a0709b0e`.

## Branch
`claude/style-browser-js-20261012` from spoke `origin/main`; it merges `origin/main` before its PR when an earlier slice has changed the same file.

## Assumptions
None.

## Open Questions
None.

## Design
- **Scope widened:** this slice braces every non-shared-folder browser JS file and test, not only the shared modules, so the whole browser layer meets the rule. Slice 19i covers the shared-folder files.
- **Fixers:** a scratch brace fixer handles single-line bodies whose condition balances on the line. A second pass joins bare `else` lines onto the preceding block's closing brace. A final scan confirms that no single-line or next-line unbraced body remains.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| 66 browser JS and JS test files with single-line bodies (all except shared-folder files) | changed | Block bodies |
| Remaining browser JS files | conforming | No change |

## Task Breakdown

### Task 1 - Conform slice 22

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

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | `node --check` on each changed file, the full check with `jsTest`, and a full-diff review | Covered by AC-3 |
| AC-3 | 390 JS tests | verify-local-app: changed modules compared byte for byte with the checkout; key pages rendered anonymously and as the administrator |
| AC-4 | Required PR checks | `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A braced body changes control flow, for example an `else` binding | Low | Only whole single statements are wrapped, `node --check` passes, and the JS suites cover the touched modules |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** These are mechanical or Settled-Decision edits made while earlier slices merged.
- **Impact:** No PR exists yet; the plan and evidence are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
