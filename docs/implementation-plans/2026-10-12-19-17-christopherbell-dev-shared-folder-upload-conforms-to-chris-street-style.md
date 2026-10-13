# Shared Folder Upload Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The shared-folder `upload` package conforms to write-chris-street-style-code, and Checkstyle guards it, while its behavior is unchanged.

## Background
This is slice 19f of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md); the split is listed in [slice 19a](2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md). Inspection of the 10 main files and their tests at spoke `origin/main` `c0dec3eb` found:

1. **Checkstyle, with the upload suppression removed:** 26 mechanical violations, mostly single-statement bodies without braces.
2. **`SharedFolderUploadService`:**
   - `claimExpiredFinalization` returns null when another instance holds the lease.
   - The expiry loop reloads a session with `orElse(null)`.
   - A `markRestorePending` catch named `ignored` acts by returning the unsaved session.
3. **Already justified:** the native `...OrNull` lookups follow the recycle slice's state-machine decision but are not documented, and `normalizeDigest` returns null for a nullable stored field.
4. **Layout:** one-line members in `MongoSharedFolderUploadSessionRepository`.

## Goals
- Every upload file conforms and Checkstyle guards it (AC-1, AC-2).
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
| AC-1 | Expected Changes records a verdict for every upload file and the suppression line |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass with Checkstyle covering `upload`, and a full-diff style review finds no blocker |
| AC-3 | On isolated MongoDB `test` with the test administrator and the shared folder enabled, the published report records that the test administrator creates an upload, appends a chunk, retries it idempotently and finalizes it, and the bytes read back exactly. A wrong chunk digest is refused, completing onto an existing name without replace gets 409, and cancellation works. A read-only USER cannot upload, and the log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the 10 main files and their tests at `c0dec3eb`, Checkstyle output with the suppression removed, and every `null`, `orElse(null)` and `ignored` site.

## Branch
`claude/style-shared-upload-20261012` from spoke `origin/main` `c0dec3eb`; it merges `origin/main` before the PR when earlier slices land.

## Assumptions
None.

## Open Questions
None.

## Design
- **`claimExpiredFinalization`:** returns `Optional`, and its caller reloads the session when the result is empty, as before.
- **Expiry loop:** tests `isEmpty()` and then `orElseThrow()`, and skips non-expired sessions exactly as before.
- **`markRestorePending`:** the catch is named `saveFailure`, with a comment saying why the unsaved state is returned.
- **Documentation:** the `OrNull` lookups and `normalizeDigest` get comments explaining their null contract.
- **Checkstyle:** mechanical fixes come from the checked fixers on the lines Checkstyle reports, and the suppression line is removed.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sharedfolder/upload/*` flagged files | changed | As in Design; block bodies, imports, layout |
| Remaining upload files | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The 19f line is removed |

## Task Breakdown

### Task 1 - Conform upload

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SharedFolderUploadService.expireAbandoned`, `claimExpiredFinalization`, `markRestorePending`, `normalizeDigest`, native `...OrNull` lookups |
| **Inspection** | Inputs |
| **Behavior** | Same sessions, offsets, digests, finalization, conflicts, cancellation and expiry |
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
| AC-3 | Shared-folder suites | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder`: chunked upload, retry, digest refusal, finalize, read back, conflict, cancel and reader refusal |
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

### 2026-10-12 - Cancel expectation and merge

- **Change:** The first runtime run was discarded. Its cancellation check expected an upload whose completion had just been refused with 409 to be cancelable, but cancel answered 409. The same check against unchanged upload code (the 19g build) also answered 409. The check now asserts that 409 and cancels an unfinished upload instead. The branch then merged `origin/main` `e5ee5d9`, resolving the suppressions file by keeping the lines both sides kept, and the runtime check was rerun on the merged candidate.
- **Reason:** The 409 is existing behavior, not a regression from this slice. The merge changed the candidate commit.
- **Impact:** AC-3's cancellation case covers an unfinished upload. The behavior that an upload whose completion was refused cannot be canceled is recorded as an observation for the shared-folder feature, not changed here.

## Outcome

> [!TIP]
> Shipped in PR #1532 (`a0709b0`) through the deploy-aware queue; production serves it. Checkstyle and the style guide now hold for shared-folder upload.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in scope |
| AC-2 | ✅ Met | The full check passed ([report](../test-reports/2026-10-12-19-34-christopherbell-dev-shared-folder-upload-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 7 of 7 runtime cases passed on candidate `5f1d1c8` ([report](../test-reports/2026-10-12-19-34-christopherbell-dev-shared-folder-upload-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1532](https://github.com/azurras/christopherbell.dev/pull/1532) merged as `a0709b0` after all checks; `wait_for_github.py queue` confirmed it live |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
