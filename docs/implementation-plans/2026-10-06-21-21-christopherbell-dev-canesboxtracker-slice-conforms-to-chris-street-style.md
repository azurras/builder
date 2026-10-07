# Canesboxtracker Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the canesboxtracker (Raising Cane's Box Index) slice conforms to write-chris-street-style-code, and collection, review, manual prices and the public history behave as before.

## Background
This is slice 10 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `d83f96c0` found:

1. **Stringly typed state.** Each metro price carries four string fields, `status`, `qualityStatus`, `confidenceLevel` and `sourceName`, that are compared with string literals across the service, model and client.
2. **Hidden time.** `CanesBoxMetroPrice.failure`, `verify` and `exclude` read `Instant.now()`, and so does the price client.
3. **Broad exceptions.** The client declares `throws Exception` on every helper and catches `Exception`. The service catches `Exception` without logging the cause.
4. **Compilation and formatting.** The client recompiles its public-menu regex on every call and has a mis-indented method body.
5. **Duplicate method name.** The service has two `collectCurrentWeek` methods with different meanings.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The public history API, the page and admin protection behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the stored or published string fields to enum-typed fields | Production may hold snapshots that predate the current values; a strict enum mapping could fail to read them and break the public history. Enums are applied at the boundary instead |
| Changing collection schedule, index math, plausibility floor, matching or API endpoints | Product behavior |
| Removing the lease-free service constructor | Tests run collection directly through it |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` (collection disabled in that profile), the history API returns the empty envelope in production's shape, the page renders, and anonymous and USER admin actions are rejected. Recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit, with the production history still served |

## Inputs
- **Request:** umbrella plan slice 10; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `d83f96c0`:
  - All `canesboxtracker` Java and the README.
  - The four test classes.
  - `static/js/canes-box-tracker.js`, `templates/canes-box-tracker.html` and the Back Office caller.
  - `application.yml` and `application-test.yml`; collection is disabled under `test`.
  - The history of `CanesBoxMetroPrice` status values since its creation on 2026-06-05.

## Branch
`claude/style-canes-20261006` from spoke `origin/main` `d83f96c0`.

## Assumptions
- Every stored status value written since 2026-06-05 is one of the enum names; any other value is handled by the boundary fallbacks.

## Open Questions
None.

## Design
- **Enums at the boundary:** four enums name the values. `CanesBoxPriceSource` carries each source's initial quality and confidence.
  - `CanesBoxMetroPrice` keeps its stored string fields. Code reads them through `hasCollectedPrice()`, `effectiveQuality()` and `isFromSource(source)`, and writes them only from the enums.
  - A missing quality still reads as verified (collected) or excluded. An unrecognized quality now reads as excluded; before, it was left out of every count. Nothing has ever written such a value.
- **Explicit time:** factories and review methods take an explicit time.
- **Price client:** takes the application `Clock`, declares `IOException` and `InterruptedException`, and keeps its top-level failure recording.
- **Service:** names `collectAndLogWeek`, `averagePriceOf`, `countWithQuality` and `detailOf`. Fetch failures are logged with their cause.

| Alternative | Why not |
|---|---|
| Enum-typed persisted fields | Strict read mapping could break history on an unexpected stored value |
| Keep string comparisons | Typos compile and the valid set is not visible in the type |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/canesboxtracker/model/CanesBoxPriceStatus.java`, `CanesBoxPriceQuality.java`, `CanesBoxPriceConfidence.java`, `CanesBoxPriceSource.java` | new | Closed value sets (rule 4) |
| `website/src/main/java/dev/christopherbell/canesboxtracker/model/CanesBoxMetroPrice.java` | changed | Enum-backed factories and accessors, explicit times, `excludeAsImplausible` (rules 4, 7) |
| `website/src/main/java/dev/christopherbell/canesboxtracker/CanesBoxTrackerService.java` | changed | Enum reads, named steps, explicit times, logged fetch failures (rules 1, 4, 8) |
| `website/src/main/java/dev/christopherbell/canesboxtracker/OfficialCanesBoxPriceClient.java` | changed | `Clock`, narrowed exceptions, enum sources, precompiled pattern, indentation (rules 7, 8) |
| `website/src/main/java/dev/christopherbell/canesboxtracker/CanesBoxTrackerController.java` | changed | Request parameter names (rule 2) |
| `website/src/main/java/dev/christopherbell/canesboxtracker/MongoCanesBoxPriceSnapshotRepository.java` | changed | Formatting and names (rule 2) |
| `website/src/main/resources/static/js/canes-box-tracker.js` | changed | Role names (rule 2) |
| Remaining canes main files (client interface, repository interface, request and detail records, properties, snapshot, README) and `templates/canes-box-tracker.html` | conforming | No change |
| `website/src/test/java/dev/christopherbell/canesboxtracker/CanesBoxTrackerServiceTest.java`, `OfficialCanesBoxPriceClientTest.java` | changed | Enum sources, explicit failure times, client clock |
| `website/src/test/java/dev/christopherbell/canesboxtracker/CanesBoxTrackerControllerTest.java`, `CanesBoxTrackerConfigurationTest.java` | conforming | No change |

## Task Breakdown

### Task 1 - Conform the canesboxtracker slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | The four enums; `CanesBoxMetroPrice.success`, `failure`, `verify`, `exclude`, `excludeAsImplausible`, `hasCollectedPrice`, `effectiveQuality`, `isFromSource`; `CanesBoxTrackerService` collection, review and history methods; `OfficialCanesBoxPriceClient` constructor and fetch methods |
| **Inspection** | All files in Inputs at `d83f96c0` |
| **Behavior** | Same stored strings, index counts and average, plausibility exclusion, failure messages, lease checks and history ordering |
| **Invariants** | Routes, payloads and stored fields unchanged; collection still records any client failure as a failed metro price |
| **Boundary/API** | The client constructor gains `Clock`, and `failure`/`verify`/`exclude` gain a time; callers are the slice and its tests |
| **Effects and failures** | Fetch failures are now also logged with their cause; interrupts still restore the flag |
| **Tests and evidence** | Service 20, client 17, controller 6, configuration 2; runtime history and access checks |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | The four canes suites | verify-local-app: history API envelope and shape compared with production; page renders; anonymous and USER collect and manual-price calls rejected |
| AC-4 | Required PR checks | `wait_for_github.py live`; production history still returns weeks after deploy |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change: stored strings are unchanged.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Production history reads differently | Low | Strings stay the same and fallbacks match; post-deploy comparison of the production history counts |
| A collection run behaves differently | Low | Service and client tests cover success, fallback, failure, interrupt and lease loss |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
