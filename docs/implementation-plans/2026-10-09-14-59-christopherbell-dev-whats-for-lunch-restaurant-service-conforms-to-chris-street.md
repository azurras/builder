# What's for Lunch Restaurant Service Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> `RestaurantService` conforms to write-chris-street-style-code, and restaurant administration, daily and nearby picks, votes, favorites, preferences, duplicate cleanup and import classification behave as before.

## Background
This is slice 17e of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). While planning it, the controller was moved to its own slice (17f) and the front end to 17g, because the controller's `throws` can only narrow after the service's do. Inspection of the 1,654-line service at `7a1b0974` found:

1. **Hidden time.** Today's date uses `LocalDate.now(zone)` three times, and daily picks are stamped with `Instant.now()` twice, bypassing the injected `Clock`.
2. **Broad exceptions.** `createRestaurant` declares `throws Exception`.
3. **Duplication:**
   - Restaurants are loaded in requested order in three places.
   - Duplicate groups are collapsed identically in two places.
   - Preference details are built in three places.
   - Import candidates are classified and applied in two long `isPresent`/`get` chains, one of them mis-indented.
4. **Optional misuse:**
   - `orElse(null)` for today's stored picks.
   - `getSelfIdOrNull()`.
   - `owner.isPresent() && ... owner.get()`.
   - `Optional.ofNullable(...).orElseGet(List::of)` around repository results that are never null.
   - Null checks on injected repositories.
5. **Smaller issues:**
   - Unnamed limits: 100, 25, 10 and 50.
   - An inline list of United States names.
   - Single-letter catch names.
   - About 80 fully qualified names.
   - Unsorted imports.
   - No class Javadoc.

## Goals
- `RestaurantService` and its tests have recorded verdicts and conform (AC-1, AC-2).
- Reachable restaurant behavior is unchanged at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| `RestaurantController` | Slice 17f |
| Returning `Optional` from `toVoteDetail` | Its null result for a null restaurant maps into the public JSON; callers never pass null |
| User-visible messages that hard-code limits ("20 cuisine filters", the radius list) | Changing text is a behavior change |
| Changing pick counts, radii, selection, import matching or duplicate survivor rules | Product behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for the service and each test touched |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that: restaurant of the day, top-liked and freshness match production's shape; nearby picks by coordinates and by ZIP answer as production does for invalid input; a USER's preferences, favorites and votes on a missing restaurant behave as before; and ADMIN-only routes reject a USER |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `7a1b0974`:
  - All of `RestaurantService`.
  - `RestaurantServiceTest` (62 tests, Mockito `Clock` mock) and `RestaurantVoteServiceContractTest`.
  - `RestaurantWebsiteUrlPolicy`.
  - The controller's routes and permissions.

## Branch
`claude/style-lunch-service-20261009` from spoke `origin/main` `7a1b0974`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`, so `LocalDate.ofInstant(clock.instant(), zone)` yields the same date as `LocalDate.now(zone)`.

## Open Questions
None.

## Design
- **Time:**
  - `today()` returns `LocalDate.ofInstant(clock.instant(), restaurantOfTheDayZone)`.
  - Generation stamps use `Instant.now(clock)`.
  - `RestaurantServiceTest` gives its mock clock a lenient current-time default, so existing date stubs still match.
- **Exceptions:** `createRestaurant` declares `InvalidRequestException, ResourceExistsException`. Persistence failures stay unchecked `ServiceUnavailableException`.
- **Shared helpers:**
  - `restaurantsInOrder(ids)` loads restaurants in the requested order.
  - `collapseDuplicateGroup(...)` collapses one duplicate group.
  - `toPreferenceDetail(preference)` builds a preference detail.
- **Import:**
  - A private `ImportChange` enum names each candidate's outcome.
  - `classifyImport` (preview, no writes) and `applyImportedRestaurant` (writes) each return one outcome, and the loops count it.
  - The apply path keeps an explicit presence check, because the merge throws a checked exception, and a comment says why.
- **Optional:**
  - Stored picks use `findById(...).map(...).orElseGet(...)`.
  - `selfId()` returns `Optional<String>`.
  - Name ownership uses `filter`/`or`.
  - Repository results are used directly.
- **Constants:**
  - `ADMIN_LIST_PAGE_SIZE`, `DUPLICATE_CLEANUP_PAGE_SIZE` and `DUPLICATE_PREVIEW_PAGE_SIZE`.
  - `DEFAULT_TOP_LIKED_LIMIT` and `MAX_TOP_LIKED_LIMIT`.
  - `MAX_REPRESENTATIVE_CHANGES` and `UNITED_STATES_NAMES`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java` | changed | Clock, narrow `throws`, shared helpers, `Optional` use, constants, imports, Javadoc |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java` | changed | Lenient clock default; imported names |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantVoteServiceContractTest.java` | changed | Imported names |

## Task Breakdown

### Task 1 - Conform the restaurant service

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `RestaurantService` public methods; `today`, `selfId`, `restaurantsInOrder`, `collapseDuplicateGroup`, `toPreferenceDetail`, `classifyImport`, `applyImportedRestaurant` |
| **Inspection** | All files in Inputs at `7a1b0974` |
| **Behavior** | Same picks, votes, favorites, preferences, duplicate results, import counts and log messages |
| **Invariants** | Routes, JSON and stored documents unchanged |
| **Boundary/API** | `createRestaurant` declares narrower checked exceptions |
| **Effects and failures** | None new |
| **Tests and evidence** | Lunch, architecture and Mongo contract suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | `RestaurantServiceTest` (picks, nearby, preferences, votes, favorites, duplicates, import preview and apply) | verify-local-app: the reads and USER flow in AC-3. Restaurants exist only through ADMIN creation or a live import, so picks over real data, duplicate cleanup and import apply rely on the service tests |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| An import candidate is counted differently | Low | Classification and apply keep the same order of checks; service tests cover create, update, unchanged, conflicting owner and concurrent owner |
| Today's date shifts | Low | Same zone and the system clock; the runtime reads the restaurant of the day |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slices 17b to 17d were in progress.
- **Reason:** I worked ahead on a file that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - Controller and front end renumbered

- **Change:** The controller became slice 17f and the front end 17g.
- **Reason:** The controller's `throws` depend on this slice's service signatures.
- **Impact:** The umbrella ledger row 17 lists the new parts.

## Outcome

> [!TIP]
> Shipped in PR #1513 (`67abb24`) and auto-deployed. Production serves `67abb24`, and `/wfl` returns 200. Picks over real restaurants, duplicate cleanup and import apply rely on the 62 service tests, because restaurants cannot be created locally.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for the service and both tests touched |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-15-06-christopherbell-dev-whats-for-lunch-restaurant-service-conforms-to-chris-street.md)) |
| AC-3 | ✅ Met | 15 of 15 runtime cases, including all 13 USER sub-checks, passed on candidate `8eeb23f` ([report](../test-reports/2026-10-09-15-06-christopherbell-dev-whats-for-lunch-restaurant-service-conforms-to-chris-street.md)) |
| AC-4 | ✅ Met | [PR #1513](https://github.com/azurras/christopherbell.dev/pull/1513) merged as `67abb24` after all checks passed; production `/actuator/info` reports `67abb24` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
