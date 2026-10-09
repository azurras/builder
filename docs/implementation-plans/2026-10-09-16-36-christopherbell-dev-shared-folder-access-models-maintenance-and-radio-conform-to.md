# Shared Folder Access, Models, Maintenance and Radio Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The shared-folder `api`, `security`, `model`, `maintenance` and `radio` packages conform to write-chris-street-style-code, and access checks, maintenance passes and the radio station behave as before.

## Background
This is slice 19a of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Slice 19 (`sharedfolder`, 101 main files, 14,587 lines) is split by subpackage, smallest first:

| Part | Scope |
|---|---|
| 19a | `api`, `security`, `model`, `maintenance` and `radio` (28 files) |
| 19b | `audit` |
| 19c | `web` |
| 19d | `recycle` |
| 19e | `media` |
| 19f | `upload` |
| 19g | `service` |
| 19h | `fs` |
| 19i | The shared-folder front end |

Inspection at `96903df0` found the `api`, `security` and `model` code already conforming. The problems are in `maintenance` and `radio`:

1. **`SharedFolderMaintenanceService`:**
   - Eleven one-line `if` statements.
   - The pass alternates a step and a lease renewal five times by hand.
2. **`SharedFolderMaintenanceHostLock`:** four one-line `if` statements.
3. **`MongoSharedFolderMaintenanceLeaseStore`:**
   - `"unclaimed"` and `"released"` are unnamed owner markers, as they were in slice 18e's application lease store.
   - Split imports.
4. **`SharedFolderRadioDurationResolver`:**
   - Returns null for "no trusted duration".
   - Unwraps the music track with `orElse(null)`.
   - Uses one-line `if` statements.
5. **`SharedFolderRadioService`:** one-line `throw` statements and an undocumented nullable current-document parameter.
6. **Layout:** `SharedFolderMaintenanceLease` and `MongoSharedFolderRadioRepository` have one-line overrides and split imports.

## Goals
- Every file in the five packages has a recorded verdict and conforms (AC-1, AC-2).
- Shared-folder access and the radio station behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Converting the radio station's nullable current document to `Optional` throughout | The station is a concurrency-sensitive state machine built around that value; doing so is a redesign. The parameter is documented instead |
| Changing maintenance order, lease timing, audit actions or radio timing | Behavior |
| The other shared-folder packages | Slices 19b to 19i |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in the five packages |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the shared-folder pages and APIs reject anonymous and ordinary USER callers exactly as production does, and the candidate log has no maintenance or radio errors |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 19; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `96903df0`:
  - The 28 files in the five packages.
  - `SharedFolderMaintenanceServiceTest`, `MongoSharedFolderMaintenanceLeaseStoreTest`, `SharedFolderRadioDurationResolverTest`, `SharedFolderRadioServiceTest` and `SharedFolderSecurityIntegrationTest`.

## Branch
`claude/style-shared-small-20261009` from spoke `origin/main` `96903df0`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Maintenance:**
  - `runStepsRenewingBetween` runs an ordered list of `MaintenanceStep(failureAction, work)` records and renews the lease before every step after the first. That is the same sequence as the hand-written chain: step, renew, step, and so on.
  - Every `if` becomes a block.
- **Lease store:** it names `UNCLAIMED_OWNER` and `RELEASED_OWNER` with the same values.
- **Resolver:** it returns `Optional<Double>` through one `filter` with the same conditions.
- **Radio service:**
  - It unwraps the resolver result only where the stored document needs a nullable duration.
  - It rejects a contradicting report through `filter(...).isPresent()`.
  - It documents the nullable `current` parameter and `findTrack`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceService.java` | changed | Step list; block `if`s |
| `website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceHostLock.java` | changed | Block `if`s |
| `website/src/main/java/dev/christopherbell/sharedfolder/maintenance/MongoSharedFolderMaintenanceLeaseStore.java` | changed | Named owner markers; imports |
| `website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceLease.java`, `radio/MongoSharedFolderRadioRepository.java` | changed | Layout and imports |
| `website/src/main/java/dev/christopherbell/sharedfolder/radio/SharedFolderRadioDurationResolver.java` | changed | `Optional` result; block `if`s |
| `website/src/main/java/dev/christopherbell/sharedfolder/radio/SharedFolderRadioService.java` | changed | `Optional` use; block `if`s; documented nullable values |
| `api/SharedFolderAuditRetention`, `security/SharedFolderAccessService`, the 15 `model` files, `maintenance/SharedFolderMaintenanceLeaseDocument`, `maintenance/SharedFolderMaintenanceLeaseStore`, `radio/SharedFolderRadioDocument`, `radio/SharedFolderRadioRepository` | conforming | No change |
| `website/src/test/java/dev/christopherbell/sharedfolder/radio/SharedFolderRadioDurationResolverTest.java`, `SharedFolderRadioServiceTest.java` | changed | `Optional` results |
| `website/src/test/java/dev/christopherbell/sharedfolder/maintenance/MongoSharedFolderMaintenanceLeaseStoreTest.java` | changed | Imported names |

## Task Breakdown

### Task 1 - Conform access, models, maintenance and radio

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SharedFolderMaintenanceService.maintain`, `runStepsRenewingBetween`, `MaintenanceStep`; `SharedFolderRadioDurationResolver.resolve`; `SharedFolderRadioService.reportDuration`, `transition` |
| **Inspection** | All files in Inputs at `96903df0` |
| **Behavior** | Same maintenance order, renewals, audits, radio states and duration checks |
| **Invariants** | Stored lease and station documents unchanged |
| **Boundary/API** | `SharedFolderRadioDurationResolver.resolve` returns `Optional<Double>` |
| **Effects and failures** | None new |
| **Tests and evidence** | Shared-folder and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Maintenance, radio and security integration tests | verify-local-app: anonymous and USER access compared with production, and the startup log. Granted shared-folder access needs an ADMIN or a stored grant, neither of which has a supported local path, so the radio and maintenance tests cover granted behavior |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A maintenance step runs without a fresh lease | Low | The step list renews before every step after the first, exactly as before; the maintenance tests cover lost renewals |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 18 parts were in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
