# Vehicle Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the vehicle slice conforms to write-chris-street-style-code, and vehicle CRUD, VIN creation, public VIN decoding and the scheduled collectors behave as before.

## Background
This is slice 12 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection of the 44 main Java files, 12 READMEs, 14 test files and two request fixtures at `50389992` found:

1. **Broad exceptions.** Every `VehicleController` endpoint declares `throws Exception`, although the services declare narrow checked exceptions.
2. **Duplicated VIN rules.**
   - Three services each compile the same VIN pattern and upper-case without a locale.
   - A fourth service repeats the normalization.
3. **Stringly typed outcomes.** Batch-decode statuses and error codes are string literals repeated across the service, the entry and the response.
4. **A long method.** `VehicleVinDecodeService.decodeBatch` runs about 95 lines through three phases.
5. **Smaller issues:**
   - Single-letter exception names.
   - Fully qualified names.
   - Four one-line Mongo repositories.
   - An unused `clientKey` parameter.
   - `Optional.ofNullable(...).orElse` used for defaults.
   - A locale-less `toLowerCase` in robots parsing.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Admin protection and public VIN decoding behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the published batch `status` and `errorCode` strings or the entry's field types | They are the public JSON contract; the enum supplies them by name |
| Merging the NHTSA and RandomVIN import-state handling | Different stored types; a shared base is a larger design change |
| Removing the coordinator-free service constructors | Tests run collection directly through them |
| Changing routes, payloads, rate limits, bulkhead, cooldowns or collector schedules | Product behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with a disposable USER, the published test report records that: anonymous admin reads match production; USER admin actions are rejected; single decode validates and normalizes; batch decode returns ordered SUCCESS and INVALID_VIN entries with the same published code and message; batch envelope limits hold |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 12; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `50389992`:
  - All `vehicle` main and test sources, READMEs and the request fixtures.
  - `application.yml` vehicle settings: NHTSA enrichment is on, RandomVIN is off, and there is no test-profile override.
  - The `static/js/lib/api.js` routes.

## Branch
`claude/style-vehicle-20261009` from spoke `origin/main` `50389992`.

## Assumptions
- The JVM default locale on every host is not one where upper-casing ASCII letters differs from `Locale.ROOT` (for example Turkish). The shared helper now uses `Locale.ROOT`, which can only change behavior in such a locale.

## Open Questions
None.

## Design
- **VIN rules:**
  - `vehicle.model.VehicleVins` owns `normalize` (trim, upper-case with `Locale.ROOT`) and `isValid` (the 17-character pattern).
  - Each caller keeps its own messages and null handling.
- **Batch outcomes:**
  - `VehicleVinDecodeBatchFailure` names `INVALID_VIN`, `CACHE_UNAVAILABLE`, `UPSTREAM_UNAVAILABLE` and `UPSTREAM_NO_RESULT`, each with its published message.
  - `VehicleVinDecodeBatchEntry.error` takes the enum, and `SUCCESS` is one constant.
  - The entry keeps its String fields so the JSON is unchanged.
- **Batch decode:**
  - `decodeBatch` validates and rate-limits, then runs three named steps: `lookUpCached`, `decodeMisses` and `entryFor`.
  - A private `BatchLookup` record carries their shared working state.
- **Controller:** declares the services' checked exceptions, names its two request bodies, and drops the unused parameter.

| Alternative | Why not |
|---|---|
| Enum-typed `status` and `errorCode` record fields | Same JSON, but every consumer and test would change for no behavior gain; strings stay the contract |
| One shared VIN normalization that also throws | Callers publish different messages and treat null differently |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/vehicle/model/VehicleVins.java`, `VehicleVinDecodeBatchFailure.java` | new | Shared VIN rules; closed outcome set |
| `website/src/main/java/dev/christopherbell/vehicle/model/VehicleVinDecodeBatchEntry.java`, `VehicleVinDecodeBatchResponse.java` | changed | Enum-backed errors, one `SUCCESS` constant, a named count helper |
| `website/src/main/java/dev/christopherbell/vehicle/VehicleController.java`, `VehicleControllerExceptionHandler.java` | changed | Narrow `throws`, names, unused parameter |
| `website/src/main/java/dev/christopherbell/vehicle/nhtsa/decode/VehicleVinDecodeService.java` | changed | Named batch steps, shared VIN rules, exception names |
| `website/src/main/java/dev/christopherbell/vehicle/core/VehicleCrudService.java`, `vin/VehicleVinService.java`, `nhtsa/enrichment/NhtsaVinEnrichmentService.java`, `randomvin/importing/RandomVinImportService.java`, `randomvin/policy/RandomVinRobotsPolicy.java`, `nhtsa/decode/NhtsaVinClient.java` | changed | Shared VIN rules, exception names, imports, defaults, locale |
| `website/src/main/java/dev/christopherbell/vehicle/core/MongoVehicleRepository.java`, `nhtsa/decode/MongoVehicleVinDecodeCacheRepository.java`, `nhtsa/enrichment/MongoNhtsaVinImportStateRepository.java`, `randomvin/importing/MongoRandomVinImportStateRepository.java` | changed | One statement per line; parameter names |
| Remaining 29 vehicle main Java files (service facade, mapper, repository interfaces, models, properties, exceptions, rate limiter, bulkhead, RandomVIN client) and the 12 READMEs | conforming | No change |
| `website/src/test/java/dev/christopherbell/vehicle/VehicleControllerTest.java`, `VehicleServiceTest.java`, `VehicleVinDecodeServiceTest.java`, `nhtsa/decode/VehicleVinDecodeBulkheadTest.java`, `randomvin/RandomVinImportServiceTest.java` | changed | The enum error factory; imported names |
| Remaining 9 vehicle test files and `test/resources/request/vehicle-*.json` | conforming | No change |

## Task Breakdown

### Task 1 - Conform the vehicle slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `VehicleVins`; `VehicleVinDecodeBatchFailure`; `VehicleVinDecodeBatchEntry.error`; `VehicleVinDecodeService.decodeBatch`, `lookUpCached`, `decodeMisses`, `entryFor`; the `VehicleController` endpoints |
| **Inspection** | All files in Inputs at `50389992` |
| **Behavior** | Same responses, statuses, codes, messages, validation order, cache and cooldown handling |
| **Invariants** | Routes, payloads and stored fields unchanged |
| **Boundary/API** | `VehicleVinDecodeBatchEntry.error` takes the enum instead of two strings; callers are the slice and its tests |
| **Effects and failures** | None new |
| **Tests and evidence** | All vehicle suites and the architecture tests; runtime admin, decode and batch checks |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | The vehicle suites | verify-local-app: anonymous admin reads compared with production; USER admin actions; single and batch decode, including one real NHTSA decode of a sample VIN that the batch then serves from cache |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Batch decode classifies a VIN differently | Low | Existing ordered-results, cache-failure, cooldown and bulkhead tests, plus the runtime batch checks |
| Admin actions become reachable | Very low | Annotations untouched; runtime USER rejection checks |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while the federation slice was in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
