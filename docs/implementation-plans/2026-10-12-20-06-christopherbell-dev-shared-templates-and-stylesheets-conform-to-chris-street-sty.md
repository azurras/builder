# Shared Templates and Stylesheets Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Slice 23 conforms to write-chris-street-style-code with unchanged behavior.

## Background
Slice 23 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) covers templates and stylesheets that no feature slice owns. Inspection of the 30 templates and 10 stylesheets found:
- **Inline styles:** two inline `style` attributes, the `font-size: 70px` headings in The Bell pages.
- **Dead declarations:** `thebell.css` has an empty `background-image: url('')` and a `font-size:` with no value.
- **Escaping:** the only `th:utext` renders restaurant JSON-LD whose `<` is already escaped as `\u003c`.
- **`!important`:** the remaining uses are reduced-motion overrides or deliberate Bootstrap overrides.

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
| AC-3 | On isolated MongoDB `test`, the published report records that both The Bell pages render with plain `<h1>` headings, that the stylesheet is served as committed apart from fingerprinted `url()` references, with the 70px rule and no empty `url()`, that the rest of each page matches production after removing the inline style, and that the log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the files in scope at spoke `origin/main` `a0709b0e`.

## Branch
`claude/style-templates-20261012` from spoke `origin/main`; it merges `origin/main` before its PR when an earlier slice has changed the same file.

## Assumptions
None.

## Open Questions
None.

## Design
- **Headings:** the 70px size moves into `thebell.css`'s `h1` rule, replacing the declaration with no value, and the inline styles are deleted.
- **Background:** the empty `background-image` is removed. Browsers already ignored both dead declarations, so rendering is unchanged.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/resources/static/css/thebell.css` | changed | `h1` size; dead declarations removed (two empty `background-image` values, a `font-size` with no value and the invalid `font: bold` rule) |
| `website/src/main/resources/templates/thebell/index.html`, `tony.html` | changed | Inline styles removed |
| Remaining shared templates and stylesheets | conforming | No change |

## Task Breakdown

### Task 1 - Conform slice 23

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
| AC-2 | Full check | Covered by AC-3 |
| AC-3 | Template rendering in the view tests | verify-local-app: The Bell pages compared with production after the documented normalization, and the stylesheet compared byte for byte |
| AC-4 | Required PR checks | `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The heading renders at a different size | Low | The same 70px value moves from the attribute to the rule, which applies to both pages |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** These are mechanical or Settled-Decision edits made while earlier slices merged.
- **Impact:** No PR exists yet; the plan and evidence are published before it.

### 2026-10-12 - More dead declarations; check corrections

- **Change:** The runtime check found two more dead declarations in `thebell.css`: an empty `background-image:url()` on `.article-text`, and `.article-title { font: bold; }`, an invalid shorthand browsers ignore. Both were removed in `09ed7742`. Three runtime runs were discarded while the check was corrected. The production edge injects a Cloudflare analytics beacon that the origin never renders, the resource chain rewrites `url()` references to fingerprinted paths, and text decoding had hidden line endings.
- **Reason:** Rendering is unchanged by removing ignored declarations, and the comparison has to mask only what the edge and the resource chain add.
- **Impact:** Expected Changes and AC-3 were updated. The full check ran on `2dc44f14`; `09ed7742` changes only the stylesheet and was rebuilt with `bootJar`.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
