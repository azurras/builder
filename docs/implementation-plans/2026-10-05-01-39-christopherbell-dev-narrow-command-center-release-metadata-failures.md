# Narrow Command Center Release Metadata Failures

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Keep malformed or unreadable release metadata as an unavailable commit metric while catching only the file I/O and JSON parse failures that the reader expects.

## Background
`ApplicationHostMetricsProvider.readReleaseCommit(Path)` treats every `Exception` as absent metadata. The inspected operations have two expected failure types: `IOException` from bounded file access and Jackson 3 `JacksonException` from malformed JSON. Jackson 3's `JacksonException` extends `RuntimeException`, so narrowing the catch also lets unrelated programming defects propagate.

## Goals
- Preserve empty metadata results for malformed JSON and malformed/missing SHA fields (AC-1).
- Catch only `IOException` and Jackson `JacksonException`; let unrelated runtime failures propagate (AC-2).
- Run focused/full native checks and attempt packaged local runtime verification for the committed candidate (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change release metadata size limits, symlink policy, SHA format or metric display | These are existing compatibility/security contracts. |
| Change other operational probe failure boundaries | Separate methods and plans keep each correction reviewable. |
| Repair or bypass Mongo migration 015 | Requires supported test provisioning/recovery. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Malformed JSON, malformed SHA and non-regular/absent metadata continue to produce `Optional.empty()`. |
| AC-2 | The catch names only file-read and Jackson parse failures; other runtime defects are not converted into absent metadata. |
| AC-3 | Focused provider tests, full required checks and packaged local startup/representative route attempt are recorded for the committed candidate; PR remains gated on readiness. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `ApplicationHostMetricsProvider.readReleaseCommit(Path)`, its focused test and admin ownership README at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Guidance:** Chris Street Style Java, naming and testing references; website `AGENTS.md`; Jackson 3 `JacksonException` inheritance confirmed with `javap` on the resolved dependency.

## Branch
Create a fresh isolated worktree and branch from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6` after publishing this plan.

## Assumptions
- Malformed release metadata remains an optional/unavailable metric rather than a startup failure.
- `IOException` covers the file operations; Jackson 3 parse failures are represented by `tools.jackson.core.JacksonException`.
- Isolated MongoDB `test` still stops startup at migration 015; this is an evidence gap, not a reason to edit durable migration state.

## Open Questions
None. Use native exceptions confirmed from the pinned dependency and preserve current metadata fallback behavior.

## Design
Catch `IOException | JacksonException` around the existing bounded metadata read and JSON parse. Keep all current early returns and SHA checks. Extend the current metadata test to characterize malformed JSON and a non-regular path as empty results. Do not add a mapper seam or translate unexpected runtime failures.

| Alternative | Why not |
|---|---|
| Keep `catch (Exception)` | It also hides unrelated runtime defects as missing release metadata. |
| Catch `IOException` only | Jackson 3 parse exceptions are runtime exceptions and would break the established malformed-metadata fallback. |
| Inject a new mapper abstraction only for tests | No existing invariant or effect ownership requires another seam. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java` | Catch only `IOException` and Jackson parse failures. |
| `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java` | Characterize malformed JSON and non-regular metadata fallbacks. |

## Task Breakdown
### Task 1 - Bound metadata fallback to expected failures
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the provider, its focused tests, package ownership README, dependency class hierarchy and application test/build configuration. |
| **Symbols** | `readReleaseCommit(Path)` and `readsOnlyAValidBoundedReleaseMetadataSha()`. |
| **Inspection** | Fresh website revision `695a3ed8617f9b4ab07abb7413baf369c58acf6`; resolved Jackson 3 class declares `JacksonException extends RuntimeException`. |
| **Behavior** | Valid bounded release metadata is read; expected malformed/unreadable/absent metadata produces no commit metric value. |
| **Invariants** | Existing 4,096-byte bound, no-follow regular-file check and 40-character lowercase SHA validation remain unchanged. |
| **Boundary/API** | No metric keys, release metadata format, method visibility or public API changes. |
| **Effects and failures** | File I/O and JSON parse failures remain optional absence; unexpected programming defects propagate. |
| **Tests and evidence** | Establish focused provider baseline; add malformed JSON and non-regular-file characterization; run focused provider/collector tests and full project checks. |
| **Verification** | `:website:test --tests dev.christopherbell.admin.commandcenter.metrics.ApplicationHostMetricsProviderTest --tests dev.christopherbell.admin.commandcenter.metrics.CommandCenterMetricsServiceTest`, `:website:check :cbell-lib:check`, `:website:bootJar`; then packaged runtime attempt on isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused tests for malformed JSON, non-regular metadata and malformed SHA. | Candidate startup and `/` route after readiness. |
| AC-2 | Review exact multi-catch and confirmed Jackson inheritance; compile and run focused provider tests. | Candidate startup and `/` route after readiness. |
| AC-3 | Focused provider/collector tests, full module checks, package and `git diff --check`. | Test profile, isolated MongoDB `test`, non-production port and disabled side effects; report actual startup/route/cleanup outcome. |

Regression: malformed JSON continues to fall back to unavailable metadata; invalid but parseable SHA and non-regular inputs stay empty; valid commit SHA remains available.

## Rollback or Recovery
Revert the narrow catch change if malformed metadata stops following the established unavailable path. Do not alter release files, production configuration, database records or migration guards during verification.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Jackson parse exceptions are not included in the catch and break fallback | Low | Dependency inheritance was inspected; add malformed JSON characterization and compile. |
| Candidate runtime remains blocked | High | Record actual startup attempt; no PR before supported fixture/provisioning or recovery and readiness. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
