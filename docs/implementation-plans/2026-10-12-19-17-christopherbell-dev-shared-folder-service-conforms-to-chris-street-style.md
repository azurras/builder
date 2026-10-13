# Shared Folder Service Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The shared-folder `service` package conforms to write-chris-street-style-code, and Checkstyle guards it, while its behavior is unchanged.

## Background
This is slice 19g of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md); the split is listed in [slice 19a](2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md). Inspection of the 16 main files and the 19 package-level shared-folder tests at spoke `origin/main` `c0dec3eb` found:

1. **Checkstyle, with the service and package-level test suppressions removed:** 237 mechanical violations, most of them in the package-level tests.
2. **`SharedFolderMutationService`:** `claimExpiredRecovery` returns null or uses `orElse(null)`, and its caller null-checks the result.
3. **`SharedFolderCatalogService`:** `decodeCursor` returns null for a first page, and two call sites null-check it.
4. **Kept:** the download audit's `ignored` catch only explains why audit degradation never interrupts a body. The native `OrNull` lookups are kept and documented.

## Goals
- Every service file conforms and Checkstyle guards it (AC-1, AC-2).
- Behavior is unchanged at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing shared-folder rules, limits, leases or error mapping | Behavior belongs to the feature, not the style migration |
| Renaming catches named `ignored` whose handlers do nothing by design | The Java guide's Settled Decisions keep them |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every service file and the suppression line |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass with Checkstyle covering `service`, and a full-diff style review finds no blocker |
| AC-3 | On isolated MongoDB `test` with the test administrator and the shared folder enabled, the published report records that the test administrator creates, renames, moves and deletes folders. A stale observed token gets 409. Search pages one entry at a time through cursors to the end with private no-store caching, a malformed cursor gets 400, a file downloads byte for byte, and the log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the 16 main files and the 19 package-level shared-folder tests at `c0dec3eb`, Checkstyle output with the suppression removed, and every `null`, `orElse(null)` and `ignored` site.

## Branch
`claude/style-shared-service-20261012` from spoke `origin/main` `c0dec3eb`; it merges `origin/main` before the PR when earlier slices land.

## Assumptions
None.

## Open Questions
None.

## Design
- **`claimExpiredRecovery`:** returns `Optional`, and its caller becomes `ifPresent(this::reconcileClaimedRecovery)`.
- **`decodeCursor`:** returns `Optional`. The generation conflict uses `filter`, and the page loop computes `isAfterCursor` with `map(...).orElse(true)`, which matches the old null checks.
- **Checkstyle:** mechanical fixes come from the checked fixers on the lines Checkstyle reports, and the suppression line is removed.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sharedfolder/service/*` flagged files | changed | As in Design; block bodies, imports, layout |
| Remaining service files | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The 19g line is removed |

## Task Breakdown

### Task 1 - Conform service

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SharedFolderMutationService.reconcileRecovery`, `claimExpiredRecovery`; `SharedFolderCatalogService.search`, `decodeCursor` |
| **Inspection** | Inputs |
| **Behavior** | Same mutations, recovery, catalog ordering, cursors and errors |
| **Invariants** | No stored field, route or status code changes |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | Shared-folder and architecture suites; runtime below |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check with Checkstyle; full-diff review | Covered by AC-3 |
| AC-3 | Shared-folder suites | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder`: mutations, search cursors and downloads |
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

### 2026-10-12 - Merged main before the PR

- **Change:** The branch merged `origin/main` `a0709b0`. The suppressions file was resolved by keeping the lines both sides kept. Compilation, Checkstyle, `bootJar` and the runtime check were then rerun on the merged candidate `52c74735`.
- **Reason:** The upload and media slices removed neighboring suppression lines, and the merge changed the candidate commit.
- **Impact:** None on scope. The full check ran on `d98e3294` before the merge.

## Outcome

> [!TIP]
> Shipped in PR #1534 (`fcd0d52`) through the deploy-aware queue; production serves it. Checkstyle and the style guide now hold for the shared-folder service.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in scope |
| AC-2 | ✅ Met | The full check passed ([report](../test-reports/2026-10-12-19-57-christopherbell-dev-shared-folder-service-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 7 of 7 runtime cases passed on candidate `52c7473` ([report](../test-reports/2026-10-12-19-57-christopherbell-dev-shared-folder-service-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1534](https://github.com/azurras/christopherbell.dev/pull/1534) merged as `fcd0d52` after all checks; `wait_for_github.py queue` confirmed it live |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
