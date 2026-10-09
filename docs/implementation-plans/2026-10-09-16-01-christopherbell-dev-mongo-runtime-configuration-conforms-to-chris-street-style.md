# Mongo Runtime Configuration Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The `configuration.mongo` root and `configuration.mongo.runtime` packages conform to write-chris-street-style-code, and auditing, application leases and collector run history behave as before.

## Background
This is slice 18e of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The `mongo` package (45 files) is split by subpackage:

| Part | Scope |
|---|---|
| 18e | Root (1 file) and `runtime` (3 files) |
| 18f | `migration` (24 files) |
| 18g | `domain` (17 files) |

Inspection at `080a67e6` found:

1. **`MongoApplicationLeaseStore`:**
   - Calls `new LeaseIdentity(name, ownerToken)` four times only for its validation side effect, which reads like a mistake.
   - Uses `"unclaimed"` and `"released"` as unnamed owner markers.
   - Ends with a stray blank line.
2. **`MongoAuditingConfig` and `MongoScheduledCollectorRunStore`:** blank lines split their imports.
3. **Conforming:** `MongoLeaseConfiguration`. In `MongoScheduledCollectorRunStore`, the fully qualified `dev.christopherbell.libs.mongo.lease.ScheduledCollectorRun` deliberately distinguishes the persistence document from the imported domain type of the same name.

## Goals
- Every file in these packages has a recorded verdict and conforms (AC-1, AC-2).
- Leases and auditing behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| The same owner literals in `MongoSharedFolderMaintenanceLeaseStore` | Slice 19 owns the shared folder |
| Lease semantics, fencing and expiry | Concurrency behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in the two packages |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the candidate starts, its scheduled collectors run under leases without errors, and a created record carries auditing timestamps |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `080a67e6`:
  - The 4 files in the two packages.
  - `LeaseIdentity` in `cbell-lib`.
  - The remaining-domain Mongo contract tests, which exercise these adapters.

## Branch
`claude/style-mongo-runtime-20261009` from spoke `origin/main` `080a67e6`.

## Assumptions
None.

## Open Questions
None.

## Design
- **`requireValidIdentity`:** a documented private helper that applies `LeaseIdentity`'s rules (non-blank, at most 128 characters).
- **Owner markers:** `UNCLAIMED_OWNER` and `RELEASED_OWNER` name them.
- **Imports:** sorted without blank lines.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/mongo/runtime/MongoApplicationLeaseStore.java` | changed | Named validation and owner markers |
| `website/src/main/java/dev/christopherbell/configuration/mongo/MongoAuditingConfig.java`, `runtime/MongoScheduledCollectorRunStore.java` | changed | Import layout |
| `website/src/main/java/dev/christopherbell/configuration/mongo/runtime/MongoLeaseConfiguration.java` | conforming | No change |

## Task Breakdown

### Task 1 - Conform mongo root and runtime

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `MongoApplicationLeaseStore.requireValidIdentity`, `UNCLAIMED_OWNER`, `RELEASED_OWNER` |
| **Inspection** | All files in Inputs at `080a67e6` |
| **Behavior** | Same lease queries, updates and validation |
| **Invariants** | Stored owner markers unchanged |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | Lease, collector and Mongo contract suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Mongo contract tests | verify-local-app: startup, the candidate log, and a created post's `createdOn` |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| None material | Low | Constants hold the same strings; the helper performs the same construction |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits.
- **Reason:** I worked ahead while slices 18a to 18d were in progress.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1520 (`5b7ef3c`) and auto-deployed. Production serves `5b7ef3c`, and `/robots.txt` returns 200.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in the two packages |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-16-10-christopherbell-dev-mongo-runtime-configuration-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 4 of 4 runtime cases passed on candidate `47b65fe`, including auditing timestamps and a clean lease log ([report](../test-reports/2026-10-09-16-10-christopherbell-dev-mongo-runtime-configuration-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1520](https://github.com/azurras/christopherbell.dev/pull/1520) merged as `5b7ef3c` after all checks passed; production `/actuator/info` reports `5b7ef3c` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
