# Narrow Restaurant Import Month Parsing Failure

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Treat only malformed persisted month text as an absent legacy month. Let unrelated runtime defects in the parsing boundary remain visible.

## Background
`RestaurantImportWorkflowService.parseYearMonth()` accepts a persisted string and calls `YearMonth.parse()`, but catches every `Exception`. The helper's only expected failure for nonblank text is `DateTimeParseException`; callers treat `Optional.empty()` as legacy or missing month state.

## Goals
- Catch the parser's documented format exception only while preserving current empty/valid outcomes (AC-1).
- Name the persisted month input for its actual role (AC-2).
- Characterize malformed legacy state, run module checks, and attempt required runtime proof (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change import scheduling or legacy state semantics | This is a precise parse-boundary correction only. |
| Rewrite other workflow exception boundaries | Their operations have broader declared effect contracts and require separate inspection/plans. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Valid month text parses and malformed/blank month text remains empty through a precise `DateTimeParseException` catch. |
| AC-2 | The helper parameter names the stored month role. |
| AC-3 | Focused characterization tests and full module checks pass; packaged runtime is verified on isolated `test` and documented before PR creation. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `RestaurantImportWorkflowService.parseYearMonth()`, its overdue-retry callers and the import workflow tests on website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Guidance:** Chris Street Style Java, naming, design/API and testing references; website `AGENTS.md`.

## Branch
`codex/restaurant-import-month-parse-20261005` from `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- A malformed stored month is treated as absent state so retry logic can use existing legacy/default behavior.
- `YearMonth.parse(CharSequence)` reports malformed month text using `DateTimeParseException`.
- Runtime verification will encounter the unresolved migration-015 test database blocker.

## Open Questions
- A supported fixture/provisioning or recovery procedure for isolated MongoDB `test` is needed before runtime proof and PR creation.

## Design
Rename the helper parameter from `value` to `persistedMonth`; preserve the null/blank empty result and valid parsing path; catch only `DateTimeParseException`. Add a focused workflow case for malformed legacy month state and use the existing month-only and valid-state cases as characterization evidence.

| Alternative | Why not |
|---|---|
| Keep catching every exception | That masks unexpected defects as malformed storage. |
| Reject malformed historic state | Existing behavior deliberately allows retry logic to continue without a parseable month. |
| Add a wrapper abstraction | There is one local parser call and no reused contract requiring another type. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowService.java` | Name persisted month input and catch only `DateTimeParseException`. |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowServiceTest.java` | Characterize malformed month fallback alongside valid legacy-month retry behavior. |

## Task Breakdown
### Task 1 - Clarify persisted month parsing boundary
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected workflow service, parse callers, current service tests and project instructions. |
| **Symbols** | `parseYearMonth()`, `runMissedMonthlyOpenStreetMapImport()`, `retryFailedMonthlyOpenStreetMapImport()` and workflow tests. |
| **Inspection** | Fresh main-based candidate at `695a3ed8617f9b4ab07abb7413baf369c58acf6`; current month-only legacy test reviewed. |
| **Behavior** | Null, blank or malformed stored month returns empty; valid month parses and schedule behavior remains unchanged. |
| **Invariants** | Retry scheduling and import lease/effect boundaries do not change. |
| **Boundary/API** | Private helper only; no public API or persisted schema changes. |
| **Effects and failures** | Parsing is pure; only malformed format is normalized to absent state. |
| **Tests and evidence** | Run focused baseline characterization, add malformed-state coverage, rerun focused tests and full module checks. |
| **Verification** | Run `RestaurantImportWorkflowServiceTest` before/after, `:website:check :cbell-lib:check`, then candidate startup on isolated `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Valid month and malformed month characterization tests. | Start candidate against isolated database `test`. |
| AC-2 | Review the helper call and parameter roles. | Exercise a representative route after readiness. |
| AC-3 | Focused workflow tests and full module checks. | Record startup, route result and cleanup in a candidate report. |

Regression: malformed month-only state follows current overdue-retry behavior; a valid legacy month remains respected.

## Rollback or Recovery
Revert only this isolated change if month retry behavior differs from the current characterization. Do not alter stored Mongo state directly.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Historic malformed text is treated as a different state | Low | Characterize existing fallback and valid legacy-state behavior. |
| Runtime proof remains blocked | High | Do not create a PR without supported isolated fixture/recovery and a successful candidate run. |

## Implementation Log

### 2026-10-05 - Record precise month parse boundary and runtime blocker

- **Change:** Candidate `137bcec` narrows persisted-month parsing to `DateTimeParseException` and names the stored input. Existing month-only workflow tests passed before editing; the new malformed-month characterization passes on baseline and candidate. Full module checks passed; runtime startup is blocked at migration 015.
- **Reason:** Malformed legacy text retains the established empty-state behavior, while unrelated runtime defects are no longer swallowed as parse failures. Required candidate runtime proof remains incomplete.
- **Impact:** AC-1 and AC-2 are met; AC-3 is partly met pending runtime proof. See [candidate test report](../test-reports/2026-10-05-01-17-christopherbell-dev-narrow-restaurant-import-month-parsing-failure.md). No database repair or PR was made.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
