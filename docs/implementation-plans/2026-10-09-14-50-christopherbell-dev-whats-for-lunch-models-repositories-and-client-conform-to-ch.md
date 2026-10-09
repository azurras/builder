# What's for Lunch Models, Repositories and OpenStreetMap Client Conform to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The lunch models, root repositories and query adapters, mapper and OpenStreetMap client conform to write-chris-street-style-code, and restaurant storage, inventory and duplicate queries, website validation and OpenStreetMap parsing behave as before.

## Background
This is slice 17d of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 17c](2026-10-09-14-46-christopherbell-dev-whats-for-lunch-sessions-votes-and-selection-conform-to-chri.md). The slice covers 31 model files and 14 root files of `whatsforlunch/restaurant`, excluding `RestaurantService` and `RestaurantController` (slice 17e), plus 2 READMEs. Inspection at `7ec9ae11` found:

1. **`RestaurantInventoryQueryRepository`:**
   - The cursor decoder returns null, and the caller null-checks it.
   - The three normalized filters are passed around as loose nullable parameters and normalized twice for the count query.
   - The page-size message and the filter length repeat `100` as a literal.
2. **`RestaurantWebsite`:** its private normalizer returns null for "not a safe URL", and the catch variable is named `e`.
3. **`OpenStreetMapRestaurantClient`:**
   - `isEmpty()` then `orElseThrow()` on the matched location.
   - Out-of-order `tools.jackson` imports.
   - Unnamed timeouts and an inline list of United States names.
   - Undocumented nullable tag readers.
4. **Mongo adapters:** `MongoRestaurantRepository`, `MongoDailyLunchPicksRepository` and `MongoRestaurantImportStateRepository` put `@Override` on the method line, have one-line bodies and no member spacing, and split their imports out of order.
5. **Smaller issues:**
   - `RestaurantDuplicateQueryRepository` and `RestaurantInventoryQueryRepository` split their imports out of order.
   - `RestaurantDuplicateQueryRepository` uses a fully qualified `AggregationOperation`.
   - `RestaurantMapper` imports are out of order.
   - Two tests use fully qualified names.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Reachable restaurant reads behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| `RestaurantService`, `RestaurantController` | Slice 17e |
| Returning `Optional` from `RestaurantWebsite.validateForWrite` and `safeForDisplay`, or from the client's tag readers | They fill optional, nullable fields of the stored and public models; null is that contract's documented "absent" value |
| Changing OpenStreetMap filters, location matching, cursor encoding or inventory limits | Product behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the candidate starts, public restaurant reads (today, top-liked, freshness, an unknown public profile) answer like production, and a USER is rejected from the ADMIN inventory and duplicate previews |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `7ec9ae11`:
  - All 31 `restaurant/model` files and the 14 root files listed above, plus the 2 READMEs.
  - `OpenStreetMapRestaurantClientTest`, `RestaurantBoundedQueryRepositoryTest`, `RestaurantWebsiteUrlPolicyTest`, `RestaurantStub` and `WflPropertiesTest`.
  - The controller's ADMIN-only inventory and duplicate routes.

## Branch
`claude/style-lunch-models-20261009` from spoke `origin/main` `7ec9ae11`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Inventory:**
  - `decodeCursor` returns `Optional<Cursor>`, and the caller adds the position criteria with `ifPresent`.
  - A private `Filters` record holds the three normalized filters once, for both the page and count queries. A null component means unfiltered, as the record's Javadoc states.
  - `MAX_FILTER_LENGTH` names the filter limit.
- **Website:** `normalize` returns `Optional<String>`. The public methods keep their documented nullable results.
- **Client:**
  - It maps the matched location with `Optional.map`.
  - It names `CONNECT_TIMEOUT`, `RESPONSE_TIMEOUT_MARGIN` and `UNITED_STATES_NAMES`.
  - Its class Javadoc states why tag readers return null.
- **Adapters:** they are laid out one annotation and one statement per line, with sorted imports.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantInventoryQueryRepository.java` | changed | `Optional` cursor, filter record, named limit, imports, layout |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantWebsite.java` | changed | `Optional` normalizer, catch name |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java` | changed | `Optional.map`, constants, imports, documented nullable readers |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/MongoRestaurantRepository.java`, `MongoDailyLunchPicksRepository.java`, `MongoRestaurantImportStateRepository.java` | changed | Layout and import order |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantDuplicateQueryRepository.java`, `RestaurantMapper.java` | changed | Import order; imported name |
| The other 30 model files, the other 7 root files and the 2 READMEs | conforming | No change |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`, `RestaurantBoundedQueryRepositoryTest.java` | changed | Imported names |
| `RestaurantWebsiteUrlPolicyTest`, `RestaurantStub`, `WflPropertiesTest` | conforming | No change |

## Task Breakdown

### Task 1 - Conform models, repositories and the client

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `RestaurantInventoryQueryRepository.find`, `decodeCursor`, `Filters`; `RestaurantWebsite.normalize`; `OpenStreetMapRestaurantClient.toRestaurant` |
| **Inspection** | All files in Inputs at `7ec9ae11` |
| **Behavior** | Same queries, pages, cursors, website results and parsed restaurants |
| **Invariants** | Routes, JSON, stored fields and public method signatures unchanged |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | Lunch, architecture and Mongo contract suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Client parsing, bounded query and website policy tests | verify-local-app: readiness, public reads compared with production, USER rejections. Inventory paging and duplicate previews are ADMIN-only, and restaurants can only be created by an ADMIN or a live import, so `RestaurantBoundedQueryRepositoryTest` (real Mongo) covers cursors and filters |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| An inventory cursor or filter changes a page | Low | The bounded query repository test pages through filtered data with cursors |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slices 17b and 17c were in progress.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1512 (`787a281`) and auto-deployed. Production serves `06297e6`, which contains it, and `/wfl` returns 200. `#1513` and `#1514` merged on top before the deploy finished, so production went straight to the newer head.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-15-00-christopherbell-dev-whats-for-lunch-models-repositories-and-client-conform-to-ch.md)) |
| AC-3 | ✅ Met | 12 of 12 runtime cases passed on candidate `cadf7aa` ([report](../test-reports/2026-10-09-15-00-christopherbell-dev-whats-for-lunch-models-repositories-and-client-conform-to-ch.md)) |
| AC-4 | ✅ Met | [PR #1512](https://github.com/azurras/christopherbell.dev/pull/1512) merged as `787a281` after all checks passed; production `/actuator/info` reports `06297e6`, which contains `787a281` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
