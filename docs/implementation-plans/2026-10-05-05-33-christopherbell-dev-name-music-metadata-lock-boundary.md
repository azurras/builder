# Name Music Metadata Lock Boundary

## Document Status
blocked

## Plan Format
task-contract-v2

## Objective
> [!IMPORTANT]
> Make the Music metadata lock helper describe its operation and accept only the effect it currently needs, while preserving edit and undo outcomes.

## Background
The current private helper is named `locked`, takes an opaque `Callable<T> work`, and catches the checked `Exception` required by `Callable.call()`. The two inspected callers are local edit and undo operations whose lambdas return values and do not declare checked failures. The generic callback contract therefore obscures the lock boundary and creates an unnecessary broad exception translation path.

## Goals
- Name the helper and callback by their track-lock operation and metadata operation role (AC-1).
- Preserve existing lock acquisition, edit/undo behavior, failure translation for runtime exceptions, and lease release (AC-1).

## Non-Goals

| Not doing | Why |
|---|---|
| Change API responses, lease behavior, storage, or metadata rules | This correction only clarifies a private helper contract. |
| Refactor other Music metadata helpers | Each independent correction gets its own plan and report. |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | The helper reads as `withTrackLock(trackId, metadataOperation)`, uses a non-throwing supplier contract, and existing focused edit/undo tests pass without behavior changes. |
| AC-2 | The candidate passes the full native gate and receives a local packaged application runtime report before any PR is created or updated. |

## Inputs
- **Request:** Continue the repository-wide Chris Street Style audit; do not rely on draft PR #1477.
- **Instructions:** Builder AGENTS.md and the published master audit plan.
- **Style references:** Builder `write-chris-street-style-code` naming/readability and Java references.
- **Inspected candidate:** `preserve-command-center-action-failure-cause-20261005`, commit `453b3c5cda45c90dce4bf7242bdaa2fc8631c0b3`.
- **Inspected target:** `website/src/main/java/dev/christopherbell/music/metadata/MusicMetadataService.java`; its only callers are the `edit` and `undo` methods, both value-returning lambdas with no checked exceptions.

## Branch
Use an isolated worktree based on trusted website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`; do not edit the authoritative checkout or PR #1477.

## Assumptions
- Replacing `Callable<T>` with `Supplier<T>` is behavior-preserving because inspected lambdas do not throw checked exceptions.
- Existing `ResponseStatusException` pass-through, runtime exception translation, and `finally` lease release remain unchanged.

## Open Questions
None.

## Design
Rename `locked` to `withTrackLock`, rename `work` to `metadataOperation`, and use `Supplier<T>.get()`. Remove only the checked-exception catch made unnecessary by the more accurate callback contract. Keep explicit HTTP failure pass-through, current runtime failure translation with cause, and unconditional lease release. This makes the lock operation and callback effects legible at both call sites while preserving the existing runtime boundary.

| Alternative | Why not |
|---|---|
| Keep `Callable` and retain `catch (Exception)` | It advertises checked failures neither caller uses and keeps an overly broad translation path. |
| Remove all failure translation | That changes HTTP behavior and is outside this naming/effect-contract correction. |

## Expected Changes

| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/music/metadata/MusicMetadataService.java` | Clarify the private lock helper and callback names; replace `Callable` with `Supplier` and remove the now-unneeded checked exception branch. |
| `website/src/test/java/dev/christopherbell/music/metadata/` | No test source change expected; use existing edit/undo behavioral tests as characterization evidence. |

## Task Breakdown

### Task 1 - Clarify the Music metadata lock helper contract
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected `website/src/main/java/dev/christopherbell/music/metadata/MusicMetadataService.java` and adjacent Music metadata tests. |
| **Symbols** | Private `locked` helper and its `edit`/`undo` call sites. |
| **Inspection** | Candidate commit `453b3c5cda45c90dce4bf7242bdaa2fc8631c0b3`; only two call sites, neither declares checked exceptions. |
| **Behavior** | Track edit/undo return values, conflict handling, service-unavailable translation, original causes, and lease release stay unchanged. |
| **Invariants** | Lease is released in `finally`; caller owns the operation; no checked exception is swallowed or translated through a generic callback. |
| **Boundary/API** | Private helper only; no public, persisted, Spring, or serialized contract changes. |
| **Effects and failures** | Lock acquisition/release remain in the helper; existing response exception and runtime translation remain intact. |
| **Tests and evidence** | Run the existing Music metadata focused suite before and after; prove characterization equivalence and inspect cause/release assertions. Then run the required full native gate and `git diff --check`. |
| **Verification** | `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\Temp\site-audit-jdk .\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar`; verify isolated MongoDB `test` identity before packaged startup; record refusal and stop if unavailable. |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing Music metadata edit/undo tests before and after; `git diff --check`. | No runtime change is expected; packaged startup remains required by repository policy. |
| AC-2 | Full website/library gate and packaged JAR build. | Start the committed candidate only after read-only test DB identity preflight succeeds; verify a representative Music metadata read/edit flow without production resources. |

Regressions: preserve conflict and service-unavailable outcomes, causes, and release behavior in the existing tests; do not start the app if isolated DB identity cannot be verified.

## Rollback or Recovery
Revert the isolated candidate commit before publication if characterization or full checks fail. If test MongoDB is unavailable, save the blocked report and do not create or update a PR.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| An unchecked checked-exception trick relied on `Callable` | Low | Inspect every call site and prove the Java source compiles against `Supplier`; keep cause behavior for runtime failures. |
| Isolated application runtime cannot be verified | High based on prior refused port | Read-only preflight first; leave publication blocked if DB is unavailable. |

## Implementation Log

### 2026-10-05 - Narrow the lock callback contract

- **Change:** Renamed the helper to `withTrackLock`, named its callback `metadataOperation`, and replaced `Callable<T>` with `Supplier<T>`; the callback body now catches only `RuntimeException` after the explicit response exception pass-through. The focused Music metadata suite passed before and after, and the full native gate passed.
- **Reason:** The two inspected lambdas have no checked effects; `Callable` forced a broad exception path for a contract they do not use. The interface now states the actual effect boundary.
- **Impact:** AC-1 native checks pass; AC-2 packaged startup still requires isolated test database preflight and runtime evidence.

### 2026-10-05 - Record blocked runtime preflight

- **Change:** Committed candidate `26cf68d`; focused characterization and full native checks passed, but the read-only test database identity request returned `ECONNREFUSED`.
- **Reason:** Repository verification requires isolated MongoDB identity before startup; the endpoint on `127.0.0.1:27018` is unavailable, and no supported recovery/provisioning action was authorized for this continuation.
- **Impact:** AC-2 remains partly met. [Candidate report](../test-reports/2026-10-05-05-42-christopherbell-dev-name-music-metadata-lock-boundary.md) records the blocker; no startup or PR was attempted.

## Outcome
> [!WARNING]
> AC-1 is met. AC-2's native gate is met, but required local runtime proof is blocked because the isolated test MongoDB port refuses connections; no PR was created.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Baseline and candidate `MusicMetadataServiceTest` both passed 6/6; candidate diff was reviewed and `git diff --check` passed. Candidate `26cf68d16b011aafd70d3c0e84e43dfc24dfd9aa`. |
| AC-2 | ⚠️ Partly met | Full native gate passed with 2,165 Java tests, 0 failures/errors, 110 skipped, browser/PowerShell checks passed, and JAR built. Runtime report is [blocked](../test-reports/2026-10-05-05-42-christopherbell-dev-name-music-metadata-lock-boundary.md): isolated MongoDB `test` preflight returned `ECONNREFUSED`; startup and PR were not attempted. |

## Project
christopherbell-dev
