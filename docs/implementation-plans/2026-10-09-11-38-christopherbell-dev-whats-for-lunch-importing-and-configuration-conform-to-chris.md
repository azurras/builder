# What's for Lunch Importing and Configuration Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The restaurant importing and configuration packages conform to write-chris-street-style-code, and previews, applies, scheduled and startup imports, status and public freshness behave as before.

## Background
This is slice 17b of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). See [slice 17a](2026-10-09-11-31-christopherbell-dev-whats-for-lunch-workflow-engine-conforms-to-chris-street-sty.md) for how slice 17 is split. Inspection at `9962afd9` found:

1. **`RestaurantImportWorkflowService`:**
   - `throws Exception` on the preview, apply and lease paths, whose callees throw only `IOException`, `InterruptedException` and `InvalidRequestException`.
   - Four `orElse(null)` unwraps followed by null checks.
   - The cron schedule is parsed and evaluated in two copies.
   - The monthly zone is looked up four times.
   - Fully qualified `java.time.Duration`, `java.net.http.HttpTimeoutException` and `java.io.IOException`.
   - An out-of-order import, and the `"system"` and `"OpenStreetMap"` literals.
   - Two broad catches without a comment saying why.
2. **`RestaurantImportPreviewStore`:** a blank line splits its imports out of order.
3. **`WflProperties`:** the 20-second lease margin is an unnamed literal.
4. **`RestaurantImportWorkflowServiceTest`:** fully qualified Mockito and JUnit calls.

## Goals
- Every importing and configuration file has a recorded verdict and conforms (AC-1, AC-2).
- Import endpoints and public freshness behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| `RestaurantController` import endpoints' `throws Exception` and status `orElse(null)` | Slice 17c owns the controller |
| `RestaurantService.prepareConfiguredMetroImport` and `applyPreparedImport` | Slice 17c owns the service |
| Removing the nullable `lastRefreshedOn` from `RestaurantDataFreshness` | It is the public JSON contract; the service unwraps once at that boundary |
| Changing schedules, lease timing, error categories or the census place lists | Product behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every importing and configuration file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the candidate starts with the monthly import disabled by the test profile, public freshness matches production's shape with no recorded import, and anonymous and USER import status, preview and apply calls are rejected as in production |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `9962afd9`:
  - All 12 `restaurant/importing` and 2 `restaurant/config` main files.
  - `RestaurantImportWorkflowServiceTest`.
  - The `RestaurantService` import signatures.
  - The controller's import endpoints.
  - `application-test.yml`, which disables the monthly import.
  - The architecture baseline, which pins only the `PermissionService` dependency.
- **Production (read-only GETs, 2026-10-09):** public freshness returns 200, and the anonymous import status read returns 403.

## Branch
`claude/style-lunch-import-20261009` from spoke `origin/main` `9962afd9`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.

## Open Questions
None.

## Design
- **Checked exceptions:** `previewOpenStreetMapImport`, `applyOpenStreetMapImport` and `runWithLease` declare `IOException, InterruptedException, InvalidRequestException`. The recording catch in `runWithLease` still catches `Exception`, because every failure must be recorded. It rethrows precisely, which a comment now says. The scheduled-run catch documents that it has no caller to report to.
- **Optional state lookups:**
  - Retry: `filter(...).isPresent()`.
  - Startup catch-up: `map(...).orElse(true)`, meaning a missing state is due.
  - Public freshness: one `map`, unwrapped once into the public record.
- **Schedule:** `isScheduledRunDue(after, now)` parses and evaluates the cron once for both completion sources, and `monthlyZone()` supplies the zone.
- **Constants:** `SOURCE_NAME`, `SYSTEM_ACTOR` and `REMOTE_REQUEST_MARGIN`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowService.java` | changed | Narrow `throws`, `Optional` use, one schedule check, imports, constants, commented catches |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportPreviewStore.java` | changed | Import order |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/config/WflProperties.java` | changed | Named lease margin |
| The other 10 importing files and `config/WflConfiguration.java` | conforming | No change |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowServiceTest.java` | changed | Imported names |

## Task Breakdown

### Task 1 - Conform importing and configuration

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `RestaurantImportWorkflowService` public methods, `isMonthlyCatchUpDue`, `isScheduledRunDue`, `runWithLease`; `WflProperties.RestaurantImport.isLeaseCoversRemoteRequest` |
| **Inspection** | All files in Inputs at `9962afd9` |
| **Behavior** | Same import outcomes, recorded state, lease handling, schedule decisions and freshness |
| **Invariants** | Routes, JSON, stored state and configuration keys unchanged |
| **Boundary/API** | Three methods declare narrower checked exceptions; callers declaring `Exception` still compile |
| **Effects and failures** | None new |
| **Tests and evidence** | `RestaurantImportWorkflowServiceTest` (schedule, contention, interruption, renewal), controller tests; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Import workflow tests | verify-local-app: readiness, startup log, freshness shape, anonymous and USER rejections. A real preview or apply needs an ADMIN, which has no supported local path, and an external Overpass call, so the unit tests cover them |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A startup or retry decision changes | Low | The four startup and retry schedule tests cover completed, overdue, same-day and next-day cases |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 17a was in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
