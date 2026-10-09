# What's for Lunch Sessions, Votes and Selection Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The lunch session, vote, favorite, preference and selection packages conform to write-chris-street-style-code, and sessions, votes, favorites, preferences and weighted selection behave as before.

## Background
This is slice 17c of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). See [slice 17a](2026-10-09-11-31-christopherbell-dev-whats-for-lunch-workflow-engine-conforms-to-chris-street-sty.md) for the split. While planning it, slice 17 was split further:

| Part | Scope |
|---|---|
| 17c | Sessions, votes, favorites, preferences and selection |
| 17d | Models, root repositories, mapper and OpenStreetMap client |
| 17e | `RestaurantService` and `RestaurantController` |
| 17f | Front end |

Inspection at `db86567f` found:

1. **`WhatsForLunchSessionMutationStore`:**
   - `isPresent()` then `orElseThrow()` three times.
   - Three `orElse(null)` lookups with repeated missing and expired checks.
   - A reset classifier whose two final branches both return `CHANGED`.
   - A fully qualified `java.util.Map`, and the member limits `1` and `100` as literals.
2. **`WhatsForLunchSessionService`:**
   - Fully qualified `Objects`, `Function` and `Set`.
   - `Optional.ofNullable(...).orElseGet(List::of)` used for null lists.
   - Activity computed three times.
   - Null checks on injected repositories that are never null.
   - An unused private `getRestaurantsInRequestedOrderUnchecked`.
   - An out-of-order import and a one-letter catch name.
3. **Session conflict codes:** the codes are strings, duplicated between the service and `WflSessionExceptionHandler`, which falls back to a default description for unknown codes.
4. **`RestaurantVoteQueryRepository`:** split, out-of-order imports and two copies of the vote-total grouping.
5. **`ApprovalWeightedRestaurantSelector`:** the weights `0.35`, `1.0`, `2.0` and `0.5` are unnamed.
6. **Four Mongo adapters:** split imports, `@Override` on the same line as the method, one-line bodies and no blank lines between members.

## Goals
- Every file in these packages has a recorded verdict and conforms (AC-1, AC-2).
- The reachable session, vote, favorite and preference behavior is unchanged at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| The "more than 20 total members" message, which ignores the configured limit | Changing user-visible text is a behavior change; recorded as a follow-up |
| `RestaurantController`, `RestaurantService`, models and root repositories | Slices 17d and 17e |
| Removing the frozen account and notification dependencies of `WhatsForLunchSessionService` | Architecture baseline work, outside a style slice |
| Changing session limits, lifetimes, codes, descriptions or selection weights | Product behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in `favorite`, `preference`, `selection`, `session` and `vote` |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records, for a disposable USER: the preferences round trip; empty favorites and sessions; session creation rejected with two picks (400) and with unknown picks (404); a missing session rejected on read, join and vote (404); top-liked matching production's shape; and anonymous session reads rejected (403) |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `db86567f`:
  - All 17 main files in the five packages.
  - `WhatsForLunchSessionServiceTest` (Mockito, every repository mocked), `WhatsForLunchSessionMutationStoreTest`, `WflSessionExceptionHandlerTest`, `ApprovalWeightedRestaurantSelectorTest` and `RestaurantVoteSummaryTest`.
  - The `MusicAndLunch` Mongo contract and mutation-safety tests.
  - The architecture baseline entries for the session service.
  - The controller's permissions: restaurant creation is ADMIN-only.

## Branch
`claude/style-lunch-sessions-20261009` from spoke `origin/main` `db86567f`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Mutation store:** each mutation maps a matched document to `UPDATED`, or else classifies the miss.
- **`classifyExisting`:** it handles `MISSING` and `EXPIRED` once, then applies the mutation's own rule. The reset rule documents that a host's miss is always a race (`CHANGED`).
- **`WflSessionConflict` enum:** it owns each public code and description. `WflSessionConflictException` carries it, and `code()` still returns the same string.
- **Session service:** it computes `active` and `hostCanManage` once and reads null lists through `restaurantIdsOf`. It calls the injected repositories directly, and the unused method is removed.
- **Vote queries:** `voteTotalsByRestaurant()` builds the grouping shared by both aggregations.
- **Selector:** it names its weight constants. The interpolation is arithmetically identical, because `1.0 - 0.5` is exactly `0.5`.
- **Adapters:** they are laid out one annotation and one statement per line, with sorted imports.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WhatsForLunchSessionMutationStore.java` | changed | `Optional` use, one miss classifier, named limits, imports |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WhatsForLunchSessionService.java` | changed | Imports, null-list helper, values computed once, no dead branches or method |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WflSessionConflict.java` | added | Enum of public conflict codes and descriptions |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WflSessionConflictException.java`, `WflSessionExceptionHandler.java` | changed | Typed conflict instead of strings |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/vote/RestaurantVoteQueryRepository.java` | changed | Imports; shared grouping |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/selection/ApprovalWeightedRestaurantSelector.java` | changed | Named weights |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/favorite/MongoRestaurantFavoriteRepository.java`, `preference/MongoWhatsForLunchPreferenceRepository.java`, `session/MongoWhatsForLunchSessionRepository.java`, `vote/MongoRestaurantVoteRepository.java` | changed | Layout and import order |
| The other 7 files (`RestaurantFavoriteRepository`, `WhatsForLunchPreferenceRepository`, `WhatsForLunchSessionRepository`, `WhatsForLunchSessionMutationPort`, `RestaurantVoteRepository`, `RestaurantVoteQueryPort`, `RestaurantVoteSummary`) | conforming | No change |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/WflSessionExceptionHandlerTest.java`, `WhatsForLunchSessionServiceTest.java` | changed | Typed conflict; imported names |
| `WhatsForLunchSessionMutationStoreTest`, `selection/ApprovalWeightedRestaurantSelectorTest`, `vote/RestaurantVoteSummaryTest` | conforming | No change |

## Task Breakdown

### Task 1 - Conform sessions, votes and selection

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `WhatsForLunchSessionMutationStore` mutations and `classifyExisting`; `WhatsForLunchSessionService`; `WflSessionConflict`; `RestaurantVoteQueryRepository.voteTotalsByRestaurant`; `ApprovalWeightedRestaurantSelector.interpolateWeight` |
| **Inspection** | All files in Inputs at `db86567f` |
| **Behavior** | Same statuses, conflict codes and descriptions, documents written, vote totals and selection weights |
| **Invariants** | Routes, JSON, stored fields and queries unchanged |
| **Boundary/API** | `WflSessionConflictException` takes a `WflSessionConflict`; `code()` keeps its string |
| **Effects and failures** | None new |
| **Tests and evidence** | Lunch, architecture and notification suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Session service, mutation store (real Mongo), handler, selector and vote tests | verify-local-app: the USER flow in AC-3. A session with real restaurants needs restaurants, which only an ADMIN can create and no supported local path provides, so joins, votes and resets on a live session rely on the mutation store and mutation-safety Mongo tests |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A miss is classified differently | Low | The classifier keeps the same order of checks; the mutation store tests cover full, expired, missing, not-participant, invalid restaurant and not-host |
| A conflict response changes | Low | The enum holds the same three codes and descriptions; the handler test checks the body |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 17b was in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - Slice 17 split further

- **Change:** The 17c "restaurant core" part became 17c sessions, votes and selection; 17d models and repositories; 17e service and controller; and 17f front end.
- **Reason:** The core held about 4,300 lines, too large for one reviewable slice.
- **Impact:** The umbrella ledger row 17 lists the new parts.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
