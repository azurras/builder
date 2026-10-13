# Gradle Build Scripts Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Slice 25 conforms to write-chris-street-style-code with unchanged behavior.

## Background
Slice 25 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) covers the Gradle scripts, workflows and application YAML. Inspection found:
- **Duplication:** in `website/build.gradle.kts`, the four Pester tasks repeat one roughly 25-line inline PowerShell script, differing only in the host preamble, files and report name.
- **Qualified names:** the script names `java.nio.file.Path` and `org.gradle.api.file.FileCollection` with their packages.
- **Conforming:** the root and `cbell-lib` builds, `settings.gradle.kts`, the workflows (actions pinned to commit SHAs with explicit permissions and timeouts) and the application YAML.

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
| AC-3 | All four Pester tasks run through the helper with the same test counts as before: 189, 76, 208 and 208. The full check and `bootJar` pass |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the files in scope at spoke `origin/main` `a0709b0e`.

## Branch
`claude/style-build-20261012` from spoke `origin/main`; it merges `origin/main` before its PR when an earlier slice has changed the same file.

## Assumptions
None.

## Open Questions
None.

## Design
- **`PesterHost`:** an enum that names each host's label and preamble. Windows PowerShell 5.1 keeps its version check and module-path setup.
- **`pesterScript`:** builds the same command text the tasks used before.
- **`registerPesterTask`:** registers each task with the same name, description, inputs, report file and executable setting.
- **Imports:** the qualified types become imports.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/build.gradle.kts` | changed | One Pester task helper; imported types |
| `build.gradle.kts`, `cbell-lib/build.gradle.kts`, `settings.gradle.kts`, `.github/workflows/*`, application YAML | conforming | No change |

## Task Breakdown

### Task 1 - Conform slice 25

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
| **Verification** | `.\\ops\\local\\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

**Runtime proof not applicable:** the change refactors build configuration only; it alters no application code, configuration or dependency. The proof is the build itself: the four Pester tasks running with unchanged counts, and the full check.

| AC | Check |
|---|---|
| AC-1 | Plan review against the inspection |
| AC-2 | Full check |
| AC-3 | The four Pester tasks, compared with earlier counts |
| AC-4 | Required PR checks and `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A Pester task runs different files or under the wrong host | Low | Each task keeps its files, report name and host; the counts match the earlier full checks |

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
