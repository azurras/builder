# Shared Folder Media Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The shared-folder `media` package conforms to write-chris-street-style-code, and Checkstyle guards it, while playback, fallback admission, caching, streaming and cleanup behave exactly as before.

## Background
This is slice 19e of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md); the split is listed in [slice 19a](2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md). Inspection of the 14 main and 4 test files at `c0dec3eb` found:

1. **Checkstyle, with the media suppression removed:** 52 single-statement bodies without braces, 22 fully qualified names, one double statement and one unused import.
2. **`MediaPlaybackService`:**
   - `existing.isPresent()` then `get()` decides between reusing an active job and refusing with 429.
   - `orElse(null)` then a null check appears in `promoteQueuedJob` and `publishNextIfIdleLocked`.
   - `readyCache` returns null for no match.
   - `status.isPresent() && status.get()...`.
   - An `OptionalLong` is checked with `isPresent` and `getAsLong`.
3. **`MediaStorage`:** `readyMatches` compares an `OptionalLong` through `isPresent` and `getAsLong`. Catches named `ignored` only carry an explanatory comment, so they stay, per the Java guide's Settled Decisions.
4. **Layout:** one-line method bodies in `MediaStorage`, `MongoMediaJobRepository` and `ProgressiveMediaStreamer`.

## Goals
- Every media file conforms and Checkstyle guards the package (AC-1, AC-2).
- Media admission and cancellation behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing queue capacity, reservation, eviction, cleanup or worker protocol rules | Media behavior |
| Renaming catches named `ignored` whose handlers only explain why nothing is done | Settled Decisions keep `ignored` where the handler does not act |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every media file and the suppression line |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass with Checkstyle covering `media`, and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with the test administrator and the shared folder enabled, the published report records all of the following. Playback answers a direct-probe descriptor with no-store caching. A fallback is admitted as a queued job, the same owner reuses it, another granted account gets 429 and an ungranted account gets 403. The owner reads the job back and cancels it, a missing file gets 404, and the log has no errors |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected at spoke `origin/main` `c0dec3eb`:**
  - All 14 `media` files and the media tests.
  - Checkstyle output with the media suppression removed.

## Branch
`claude/style-shared-media-20261012` from spoke `origin/main` `c0dec3eb`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Active job:** `filter` keeps it only for its owner, `map` builds the descriptor, and `orElseThrow` raises 429. This is the same outcome as the old `if`.
- **Promoters:** `promoteQueuedJob` and `publishNextIfIdleLocked` test `isEmpty()` and then take `orElseThrow()`.
- **`readyCache`:** returns `Optional<MediaJob>` through `filter`. Its Javadoc says the match check also rejects an oversized derivative, as before.
- **`OptionalLong`:** `readyMatches` uses `equals(OptionalLong.of(expected))`, and cache totals use `orElse(0)`.
- **Mechanical rules:** applied by the checked fixers on the exact lines Checkstyle reports.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `MediaPlaybackService.java` | changed | `Optional` chains, block `if`s, imports |
| `MediaStorage.java` | changed | `OptionalLong` comparison, block `if`s, imports, layout |
| `MongoMediaJobRepository.java`, `ProgressiveMediaStreamer.java`, `MediaSourceBoundary.java`, `ProgressiveMediaController.java` and the other files Checkstyle flagged | changed | Block `if`s, imports, layout |
| Media tests | changed | Imports and block bodies |
| Remaining media files | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The media line is removed |

## Task Breakdown

### Task 1 - Conform media

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `MediaPlaybackService.requestFallback`, `promoteQueuedJob`, `publishNextIfIdleLocked`, `readyCache`, `cacheBytes`, `awaitWorkerTerminal`; `MediaStorage.readyMatches` |
| **Inspection** | Inputs |
| **Behavior** | Same descriptors, statuses, admission, eviction and cleanup |
| **Invariants** | The oversized-derivative rejection still runs when the cache is checked |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | Media and architecture suites; runtime below |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check with Checkstyle; full-diff review | Covered by AC-3 |
| AC-3 | Media service, storage and controller tests | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder` and a sample file in the disposable shared root |
| AC-4 | Required PR checks | `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The 429 or reuse branch changes | Low | The runtime check exercises both, and the service tests cover them |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** The fixes were mechanical and followed the Settled Decisions table, so planning and editing ran together while earlier work merged.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1531 (`e5ee5d9`) through the deploy-aware queue; production serves it. Checkstyle and the style guide now hold for shared-folder media.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in scope |
| AC-2 | ✅ Met | The full check passed ([report](../test-reports/2026-10-12-19-15-christopherbell-dev-shared-folder-media-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 7 of 7 runtime cases passed on candidate `e04a243` ([report](../test-reports/2026-10-12-19-15-christopherbell-dev-shared-folder-media-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1531](https://github.com/azurras/christopherbell.dev/pull/1531) merged as `e5ee5d9` after all checks; `wait_for_github.py queue` confirmed it live |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
