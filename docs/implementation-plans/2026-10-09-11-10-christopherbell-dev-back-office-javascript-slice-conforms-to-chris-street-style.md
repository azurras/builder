# Back Office JavaScript Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The Back Office page script, its six library modules and its template conform to write-chris-street-style-code, and the page loads, gates and administers exactly as before.

## Background
This is slice 15b of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). It covers `back-office.js` (1,422 lines), the six `lib/back-office-*.js` modules, `back-office.html` and the six matching tests. Inspection at `00d898a2` found:

1. **Duplication:**
   - Shared-folder and Music permissions each have their own render function, update call and change handler, which are identical apart from names.
   - Report, audit and account paging each wire their own previous and next handlers with the same rollback logic, six handlers in total.
   - `back-office-music.js` and `back-office-shared-folder.js` each carry a private copy of `util.sanitize`.
   - The activity and report modules repeat the same page validation and navigation code.
2. **An unhandled rejection.** A failed user-post load in the drawer leaves "Loading posts…" with an unhandled promise rejection.
3. **Names:**
   - `err`, `msg` and `el`.
   - A `renderOperationResult` parameter that shadows the module-level `content`.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The page's module graph loads and gates as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Grouping the page's module-level `let` state into one object | A page-wide rewrite with no rule violation behind it |
| Changing markup, routes, request bodies or confirmation prompts | Product behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass (including all 390 JavaScript tests) and a style review of the full diff finds no blocker |
| AC-3 | On the local candidate, the published test report records that `/back-office` and all eight scripts (including the new paging module) are served, and that the page script loads its whole module graph and redirects an anonymous visitor and a USER to `/404` |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 15; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `00d898a2`:
  - The eight files above and their six tests.
  - `util.sanitize`, which is identical to both private copies.
  - The `jsTest` Gradle task, which runs from the repository root.

## Branch
`claude/style-back-office-20261009` from spoke `origin/main` `00d898a2`.

## Assumptions
None beyond Inputs.

## Open Questions
None.

## Design
- **Capabilities:**
  - `CAPABILITY_FAMILIES` describes the shared-folder and Music pairs: host, template, data attribute, state function, URL and failure message.
  - `renderCapabilityPermissions`, `updateCapabilityPermissions` and `handleCapabilityPermissionChange` take a family.
- **Paging:**
  - `wirePager` wires each previous and next pair with the same bounds, rollback and failure messages as before.
  - `lib/back-office-paging.js` holds `parseServerPage` and `serverPageNavigation`.
  - The activity and report modules keep their exported names and messages.
- **Escaping:** both modules import `sanitize` from `util.js`.
- **Promises:**
  - Fire-and-forget calls are marked `void`.
  - The user-post load now shows its failure in the page alert. This is the one intentional behavior change: a defect fix.

| Alternative | Why not |
|---|---|
| Keep separate permission handlers | Every permission change would have to be made twice |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/resources/static/js/lib/back-office-paging.js` | new | Shared page validation and navigation |
| `website/src/main/resources/static/js/back-office.js` | changed | One capability path, one pager, names, promise handling |
| `website/src/main/resources/static/js/lib/back-office-activity.js`, `back-office-reports.js` | changed | Delegate to the paging module |
| `website/src/main/resources/static/js/lib/back-office-music.js`, `back-office-shared-folder.js` | changed | Use `util.sanitize`; names |
| `website/src/main/resources/static/js/lib/back-office-canes-box-index.js`, `back-office-users.js`, `website/src/main/resources/templates/back-office.html` | conforming | No change |
| `website/src/test/js/back-office-*.test.js` (six files) | conforming | No change; they pass unchanged against the new modules |

## Task Breakdown

### Task 1 - Conform the Back Office JavaScript

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `CAPABILITY_FAMILIES`, `renderCapabilityPermissions`, `updateCapabilityPermissions`, `handleCapabilityPermissionChange`, `wirePager`, `parseServerPage`, `serverPageNavigation` |
| **Inspection** | All files in Inputs at `00d898a2` |
| **Behavior** | Same requests, messages, page bounds and rendering; user-post load failures now alert |
| **Invariants** | Exported names of the library modules unchanged |
| **Boundary/API** | None |
| **Effects and failures** | One new alert on user-post load failure |
| **Tests and evidence** | The six Back Office test files, the full JavaScript suite, runtime load and gate checks |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Back Office JavaScript tests | verify-local-app: page and module responses, and the built-in browser loading `/back-office` anonymously and as a USER. The admin dashboard itself needs an ADMIN, which has no supported local path |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A broken import blanks the page | Low | The browser check proves the module graph loads; `node --check` and module tests pass |
| A permission checkbox stops saving | Low | The family table holds the same selectors and URLs; the ADMIN path is reviewed line by line |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while the admin Java slice was in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - Full check rerun after a stash during the build

- **Change:** I briefly stashed the edits to compare JavaScript test results with and without them while the first full check was running. I then reran the full check with `--rerun-tasks`.
- **Reason:** The first build may have read the stashed files, so its jar and results could not be trusted. The comparison itself showed that 30 failures under a plain `node --test` from `website/` are pre-existing, and that running from the repository root, as the `jsTest` task does, passes all 390.
- **Impact:** Only the rerun's results are used as evidence.

## Outcome

> [!TIP]
> Shipped in PR #1506 (`9962afd`) and auto-deployed. Production serves `9962afd`, and `/back-office` returns 200.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-11-11-christopherbell-dev-back-office-javascript-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 11 of 11 runtime cases passed on candidate `0332f5c` ([report](../test-reports/2026-10-09-11-11-christopherbell-dev-back-office-javascript-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1506](https://github.com/azurras/christopherbell.dev/pull/1506) merged as `9962afd` after all checks passed; production `/actuator/info` reports `9962afd` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
