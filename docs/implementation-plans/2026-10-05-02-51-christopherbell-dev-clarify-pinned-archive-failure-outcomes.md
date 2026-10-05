# Clarify Pinned Archive Failure Outcomes

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Make each archive resolver call state its online/offline mode and translate only expected I/O failures into an upstream-unavailable error, while preserving partial-file cleanup and original defects.

## Background
`website/build.gradle.kts` uses positional `true`/`false` values at every `resolvePinnedArchive` call, hiding whether each path permits downloads. The resolver catches every `Exception` and translates all non-`GradleException` failures into an upstream timeout, so programming defects from the injected writer are mislabeled. Its temporary archive still needs cleanup for every failure category.

## Goals
- Name the resolver's offline mode at every call site (AC-1).
- Translate `IOException` as an upstream failure while passing through unrelated runtime defects and preserving partial cleanup/cause (AC-2).
- Run focused/full native checks, package, attempt local application startup, and record candidate evidence (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change the configured upstream URI, checksum, timeouts, or cache location | Those settings are unrelated to the failure classification and call readability. |
| Change verified cache/cold offline/corrupt checksum behavior | These are established archive safety contracts and have existing checks. |
| Redesign the archive resolver API or task graph | A named Boolean argument makes the existing mode explicit without introducing another abstraction. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Every call passes the offline mode by name, so online and cached-offline cases are explicit. |
| AC-2 | I/O failures retain the upstream-unavailable diagnostic and cause; programming defects propagate unchanged; all temporary partial files are cleaned or cleanup failure is attached to the original. |
| AC-3 | Focused resolver verification, full website/library/browser/PowerShell checks and packaging pass; the committed packaged app receives a local startup attempt and candidate report before any PR. |

## Inputs
- **Request:** Full `christopherbell.dev` Chris Street Style audit with small targeted changes and a separate plan/report per correction; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `website/build.gradle.kts`, `resolvePinnedArchive`, `downloadPinnedArchive`, and all resolver call sites at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- **Inspected tests:** `verifySensorArchiveResolution` in the same build file; current cases cover online/cache/offline/corrupt checksum/concurrent publication/I/O failure but not runtime defects.
- **Guidance:** Spoke `AGENTS.md`; Chris Street Style Kotlin, configuration, API/error, naming, adaptation and testing references; historical archive resolver requirements at [deterministic offline builds](2026-07-29-deterministic-offline-builds-and-bounded-windows-ci-implementation-plan.md).

## Branch
Create `codex/clarify-pinned-archive-failures-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c` after publishing this plan.

## Assumptions
- `Files` and the pinned downloader report operational I/O failures as `IOException`.
- Checksum mismatch and absent offline archive are deliberate `GradleException` domain/configuration outcomes.
- App runtime verification remains blocked by the incomplete migration-015 record on isolated test database `test`.

## Open Questions
None. Keep exception text and successful cache behavior stable.

## Design
Use named `offline = ...` arguments at all resolver call sites. In the resolver's cleanup catch, keep broad `Exception` only to remove the partial file; if cleanup also fails, attach it as suppressed to the initiating exception. Rethrow `GradleException` unchanged, wrap only `IOException` with the current upstream-unavailable message, and rethrow other exceptions unchanged. Add a task-native regression where the injected writer throws `IllegalStateException`; assert the exact defect propagates and the temporary partial file is removed.

| Alternative | Why not |
|---|---|
| Catch only `IOException` around the whole download/verify/move block | Runtime defects and checksum-domain failures would skip partial cleanup. |
| Continue translating all `Exception` types | Programming defects remain indistinguishable from unavailable upstream. |
| Replace the Boolean with a new mode type | Named arguments solve the call-site ambiguity without expanding the local API. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/build.gradle.kts` | Name online/offline mode at each call and preserve failure category while cleaning temporary files. |

## Task Breakdown
### Task 1 - Clarify archive mode and failure classification
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected `website/build.gradle.kts` and all eight resolver invocations on base `695a3ed8617f9b4ab07abb7413baf369c58acf6c`. |
| **Symbols** | `resolvePinnedArchive`, `downloadPinnedArchive`, `verifySensorArchiveResolution`, and each call site. |
| **Inspection** | Existing focused task exercises online/cache/offline/checksum/concurrent/I/O outcomes; broad catch currently disguises unchecked writer defects. |
| **Behavior** | Verified archive bytes, checksum and cache semantics remain the same; only mode readability and failure classification change. |
| **Invariants** | Partial downloads are removed on all failure paths; original exception cause is retained; unchecked defects are not reported as upstream I/O. |
| **Boundary/API** | Private build-script function and verification task only; no product runtime or public endpoint changes. |
| **Effects and failures** | Resolver may read/download/write a cache file; cleanup errors are suppressed on the initiating exception rather than masking it. |
| **Tests and evidence** | Add a defect-path regression alongside existing archive-resolution checks; run focused task and complete project gate. |
| **Verification** | Run `:website:verifySensorArchiveResolution :website:check :cbell-lib:check :website:bootJar`; start the committed app candidate locally with isolated test settings and save actual outcome. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review all resolver call sites and run `:website:verifySensorArchiveResolution`. | Launch committed packaged app with integrations disabled. |
| AC-2 | Verify I/O cause/diagnostic, runtime defect identity, and partial cleanup. | Check readiness and representative route if startup succeeds. |
| AC-3 | Run complete website/library/browser/PowerShell checks, packaging and `git diff --check`. | Record startup result against MongoDB `test`; report the migration blocker if it recurs. |

Regression: cached offline avoids a download; missing offline archive fails explicitly; corrupt download/cache remains rejected; verified concurrent publication stays unchanged.

## Rollback or Recovery
Revert only the `website/build.gradle.kts` correction if any existing cache or checksum outcome changes. Keep archive cache and source files intact; no database or production effects are part of this build helper.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A non-I/O upstream failure no longer receives the existing friendly diagnostic | Low | Inspect downloader declarations; preserve `IOException` as the wrapped upstream failure class. |
| Cleanup failure obscures original failure | Medium | Attach cleanup failure as suppressed and assert the original exception remains primary. |
| Runtime remains blocked before readiness | High | Record exact startup blocker and do not open a PR without required runtime proof. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
