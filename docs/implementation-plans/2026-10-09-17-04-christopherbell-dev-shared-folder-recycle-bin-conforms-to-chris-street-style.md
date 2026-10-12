# Shared Folder Recycle Bin Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The shared-folder `recycle` package conforms to write-chris-street-style-code, and recycling, restoring, purging and crash reconciliation behave exactly as before.

## Background
This is slice 19d of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 19a](2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md). Inspection of the 7 files at `4c5aaa7e` found:

1. **`SharedFolderRecycleService`:**
   - 22 one-line `if (...) return/throw/yield` statements, two of them after a multi-line condition.
   - Ten unexplained Windows status codes compared inline.
   - Two catches named `ignored` that do handle a reconciliation failure.
   - Fully qualified names.
2. **`MongoSharedFolderRecycleRepository`:** one-line overrides and split imports.
3. **Conforming:** `SharedFolderRecycleEntry`, `SharedFolderRecycleItem`, `SharedFolderRecyclePage`, `SharedFolderRecycleRepository` and `SharedFolderRecycleState`.

## Goals
- Every recycle file has a recorded verdict and conforms (AC-1, AC-2).
- Recycle routes behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Converting reconciliation's `nativeMetadataOrNull` and `visibleNativeMetadataOrNull` to `Optional` | Crash reconciliation treats each lookup as a presence fact across a state machine; the `OrNull` names and a new Javadoc make the contract explicit, and `Optional` would obscure the branches |
| Changing recycle states, reconciliation rules, retention or native status classification | Data safety behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every recycle file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the test administrator recycles, restores and purges a folder, a wrong purge confirmation is refused, the audit log records RESTORE and PURGE, a USER without a grant is refused while a granted USER can read, responses carry no-store caching, and the log has no errors |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 19; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `4c5aaa7e`:
  - All 7 `recycle` files.
  - The recycle service and reconciliation tests.
  - The Windows status codes, against their documented meanings.

## Branch
`claude/style-shared-recycle-20261009` from spoke `origin/main` `4c5aaa7e`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Status codes:** `CONFLICT_STATUSES` and `MISSING_STATUSES` hold the same codes, each named in Javadoc. `Set.contains` on the boxed status matches exactly as the `==` chains did.
- **Single-line `if`s:** become blocks.
- **Catches:** named `reconciliationFailure`.
- **Javadoc:** documents why reconciliation lookups return null.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleService.java` | changed | Block `if`s, named status sets, catch names, imports, documented lookups |
| `website/src/main/java/dev/christopherbell/sharedfolder/recycle/MongoSharedFolderRecycleRepository.java` | changed | Layout and imports |
| The other 5 recycle files | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The recycle line is removed now that the slice conforms |

## Task Breakdown

### Task 1 - Conform the recycle bin

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SharedFolderRecycleService` reconciliation, `CONFLICT_STATUSES`, `MISSING_STATUSES`, `isNativeMissing` |
| **Inspection** | All files in Inputs at `4c5aaa7e` |
| **Behavior** | Same recycle, restore, purge and reconciliation outcomes |
| **Invariants** | Stored recycle records and native operations unchanged |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | Shared-folder and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Recycle service and reconciliation tests | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder`: real recycle, restore and purge as ADMIN, grant checks, no-store and log checks |
| AC-4 | Required PR checks | `wait_for_github.py live`, merged through the deploy gate |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A native status is classified differently | Very low | The sets hold exactly the old codes; the reconciliation tests cover conflict and missing outcomes |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slices 19a and 19b waited in the deploy gate.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-11 - Checkstyle and administrator-backed runtime

- **Change:** The branch merged `origin/main` `3217ce5`, which brought in the Checkstyle gate. It then deleted the recycle suppression line and braced five more single-statement `if`s in `SharedFolderRecycleService`, in commit `51187f89`. AC-3 now covers real recycle, restore and purge through the new test administrator.
- **Reason:** Checkstyle found branches the slice's brace regex had missed: multi-line `audit.record...(` calls and two field guards. The test administrator (PR #1528) gives this slice the ADMIN path its Test Plan had called unavailable.
- **Impact:** AC-3, the Test Plan and Expected Changes were updated. One runtime run was discarded because the check script parsed the audit list as an object; every product step in it had already passed.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
