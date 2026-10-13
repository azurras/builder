# Shared Folder Front End Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The shared-folder front end (page module, library modules, back-office module, auth service worker and their tests) conforms to write-chris-street-style-code, and the page behaves exactly as before.

## Background
This is slice 19i of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md), the last shared-folder part. Inspection of the six browser files and five JavaScript test files at spoke `origin/main` `c0dec3eb` found:
- 78 single-line `if` statements (47 of them in `shared-folder.js`) and one single-line `while`;
- one multi-line `if` whose body spans lines without braces;
- seven single-line `if`s in `shared-folder.test.js`.

No other smell was found: there is no `innerHTML` with dynamic text, no `forEach(async`, no loose equality, and every fetch checks `response.ok`. The template and stylesheet already conform. The shared-folder PowerShell modules belong to slice 24.

## Goals
- Every shared-folder browser file and its tests conform (AC-1, AC-2).
- The page and its modules are served and behave as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Restructuring page modules or changing UI behavior | The migration preserves behavior |
| A JavaScript linter | Item 5 covered Java; a JS gate would be its own change |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every shared-folder browser and test file |
| AC-2 | `node --check` passes on every changed file, the full check including `jsTest` passes, and a full-diff review finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published report records that every changed module is served byte for byte as committed and that the shared-folder page renders for a signed-in administrator. The shared-folder JavaScript tests pass, and the log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the six shared-folder browser files, the template, the stylesheet and the five JS tests at `c0dec3eb`.

## Branch
`claude/style-shared-front-20261012` from spoke `origin/main` `c0dec3eb`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Single-line bodies:** a scratch fixer braces single-line `if` and `else` bodies only where the condition's parentheses balance on the line. It reports the rest.
- **By hand:** the multi-line `if`, the `while` and one multi-line test `if` are fixed manually.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/resources/static/js/shared-folder.js` | changed | Block bodies |
| `website/src/main/resources/static/js/lib/shared-folder.js`, `back-office-shared-folder.js`, `shared-folder-streaming.js`, `shared-folder-worker-runtime.js` | changed | Block bodies |
| `website/src/main/resources/static/shared-folder-auth-sw.js` | changed | Block body |
| `website/src/test/js/shared-folder.test.js`, `shared-folder-page-initialization.test.js`, `shared-folder-streaming.test.js` | changed | Block bodies |
| Template, stylesheet and the other two shared-folder JS tests | conforming | No change |

## Task Breakdown

### Task 1 - Conform the shared-folder front end

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | Conditionals throughout the listed modules |
| **Inspection** | Inputs |
| **Behavior** | Identical control flow |
| **Invariants** | No exported name, DOM contract or request changes |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | `jsTest`; runtime below |
| **Verification** | `node --check` on each file; `.\ops\local\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | `node --check`, full check with `jsTest` | Covered by AC-3 |
| AC-3 | Shared-folder JS tests | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder`: served modules compared byte for byte, the page rendered for a signed-in administrator, and the JS tests |
| AC-4 | Required PR checks | `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A refactored `Optional` path changes an outcome | Low | Runtime checks exercise each changed branch, and the suites cover recovery paths |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** These slices follow the Java guide's Settled Decisions and the checked fixers, so editing ran alongside earlier merges.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-12 - Second pass on unbraced bodies

- **Change:** The queued PR #1533 was stopped before merging. Eight more unbraced bodies were fixed in commit `7000ac6e`: bare `else` lines after an `if` block, and single-line `if`s whose body starts with a capital letter, such as `Object.defineProperty`. The runtime check and report were then rerun.
- **Reason:** The scan pattern that selected files and counted single-line conditionals matched only lowercase body starts, and the brace fixer handled `else` only when written as `} else`. Both gaps were found while widening the JavaScript slice.
- **Impact:** Expected Changes now also lists `shared-folder-page-initialization.test.js` and `shared-folder-streaming.test.js`. AC-3 evidence covers `7000ac6`.

## Outcome

> [!TIP]
> Shipped in PR #1533 (`7bef6fe`) through the deploy-aware queue; production serves it. Checkstyle and the style guide now hold for the shared-folder front end.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in scope |
| AC-2 | ✅ Met | The full check passed ([report](../test-reports/2026-10-12-19-36-christopherbell-dev-shared-folder-front-end-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 8 of 8 runtime cases passed on candidate `7000ac6` ([report](../test-reports/2026-10-12-19-36-christopherbell-dev-shared-folder-front-end-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1533](https://github.com/azurras/christopherbell.dev/pull/1533) merged as `7bef6fe` after all checks; `wait_for_github.py queue` confirmed it live |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
