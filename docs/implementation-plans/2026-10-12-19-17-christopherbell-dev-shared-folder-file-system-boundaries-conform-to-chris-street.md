# Shared Folder File System Boundaries Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The shared-folder `fs` package conforms to write-chris-street-style-code, and Checkstyle guards it, while its behavior is unchanged.

## Background
This is slice 19h of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md); the split is listed in [slice 19a](2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md). Inspection of the 13 main files and their tests at spoke `origin/main` `c0dec3eb` found:

1. **Checkstyle, with the fs suppression removed:** 107 mechanical violations, including compact `try` and `finally` one-liners inside `PortableSharedFolderPrivateBoundary`'s private channel.
2. **Kept:** every catch named `ignored` (directory creation races, native close failures, untrusted native names) does nothing by design, so per the Settled Decisions the names stay.
3. **Layout:** annotations on the same line as members in the private channel adapter.

## Goals
- Every fs file conforms and Checkstyle guards it (AC-1, AC-2).
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
| AC-1 | Expected Changes records a verdict for every fs file and the suppression line |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass with Checkstyle covering `fs`, and a full-diff style review finds no blocker |
| AC-3 | On isolated MongoDB `test` with the test administrator and the shared folder enabled, the published report records that every boundary is exercised through the API: mutations, search, download, chunked upload through private staging, and recycle, restore and purge. The log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the 13 main files and their tests at `c0dec3eb`, Checkstyle output with the suppression removed, and every `null`, `orElse(null)` and `ignored` site.

## Branch
`claude/style-shared-fs-20261012` from spoke `origin/main` `c0dec3eb`; it merges `origin/main` before the PR when earlier slices land.

## Assumptions
None.

## Open Questions
None.

## Design
- **Mechanical rules:** applied by the checked fixers on the reported lines.
- **Private channel:** the `try` and `finally` bodies are written out on separate lines by hand, and annotations sit on their own lines.
- **Checkstyle:** mechanical fixes come from the checked fixers on the lines Checkstyle reports, and the suppression line is removed.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sharedfolder/fs/*` flagged files | changed | As in Design; block bodies, imports, layout |
| Remaining fs files | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The 19h line is removed |

## Task Breakdown

### Task 1 - Conform fs

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `PortableSharedFolderPrivateBoundary` private channel, `WindowsSharedFolder*Boundary`, `JnaWindowsSharedFolderNativeBridge` |
| **Inspection** | Inputs |
| **Behavior** | Same path validation, private staging, native calls and errors |
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
| AC-3 | Shared-folder suites | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder`: mutations, search, download, upload and recycle through the boundaries |
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

### 2026-10-12 - Runtime correction and merge

- **Change:** The first runtime run's upload case was discarded. It hit the same existing 409 for cancelling an upload whose completion was refused, as recorded in the upload slice, and the upload check was corrected there. The line splitter also turned two compact private-channel `try`/`finally` bodies into a dangling `finally` line; these were rewritten by hand. The branch then merged `origin/main` `fcd0d52` (suppressions file resolved), and compilation, Checkstyle, `bootJar` and the runtime check were rerun on `218f0e12`.
- **Reason:** The 409 is existing behavior, and the merge changed the candidate.
- **Impact:** Design notes the private channel. The full check ran on `c510b22b` before the merge.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
