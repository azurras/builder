# Shared Folder Audit and Web Layer Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The shared-folder `audit` and `web` packages conform to write-chris-street-style-code, and audit records, no-store headers and every shared-folder route behave as before.

## Background
This is slice 19b of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 19a](2026-10-09-16-36-christopherbell-dev-shared-folder-access-models-maintenance-and-radio-conform-to.md). Because production auto-deploy needs merges spaced out, the planned 19b (audit) and 19c (web) are combined here; later parts keep their letters.

Inspection at `5b7ef3ce` found:

1. **`SharedFolderAuditRecorder`:**
   - `currentRequest()` returns null outside a request, and three callers null-check it.
   - `failureCategory` assigns a variable through an if-chain instead of returning.
   - `"unknown"` is written five times.
   - Two one-line `if` statements.
2. **`SharedFolderNoStoreFilter`:** six one-line `if (...) return` statements in the audit classification.
3. **The three web controllers:** about 30 fully qualified names each.
4. **Layout:** `MongoSharedFolderAuditRepository` and `SharedFolderAuditCommand` have one-line overrides and split imports.
5. **Conforming:** `SharedFolderAuditEvent`, `SharedFolderAuditFilter`, `SharedFolderAuditQueryService`, `SharedFolderAuditRepository`, `SharedFolderAuditSink` and `MongoSharedFolderAuditSink`.

## Goals
- Every audit and web file has a recorded verdict and conforms (AC-1, AC-2).
- Routes and audit behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Replacing the audit classification `if` chain with a table | Its conditions mix exact paths, patterns and methods in a priority order; a table would be less clear |
| Changing audit actions, resources, failure categories or retention | Audit behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every audit and web file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that shared-folder routes answer anonymous callers exactly as production does, a USER without a grant is denied every read, write and admin route, shared-folder responses carry no-store caching, and the log has no errors |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 19; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `5b7ef3ce`:
  - All 13 `audit` and `web` files.
  - The shared-folder audit, filter, controller and security integration tests.

## Branch
`claude/style-shared-audit-web-20261009` from spoke `origin/main` `5b7ef3ce`.

## Assumptions
None.

## Open Questions
None.

## Design
- **`currentRequest()`:** returns `Optional<HttpServletRequest>`. Callers `map`, `filter` and `ifPresent` it, and `currentClientIp` falls back to `UNKNOWN` exactly when the request or the resolved address is missing or blank.
- **`failureCategory`:** returns directly from each branch.
- **`UNKNOWN`:** names the fallback.
- **Single-line `if`s:** become blocks.
- **Names:** fully qualified names become imports.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditRecorder.java` | changed | `Optional` request; direct returns; named fallback |
| `website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderNoStoreFilter.java` | changed | Block `if`s; layout |
| `website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderAdminController.java`, `SharedFolderReadController.java`, `SharedFolderWriteController.java` | changed | Imported names |
| `website/src/main/java/dev/christopherbell/sharedfolder/audit/MongoSharedFolderAuditRepository.java`, `SharedFolderAuditCommand.java` | changed | Layout and imports |
| `SharedFolderAuditEvent`, `SharedFolderAuditFilter`, `SharedFolderAuditQueryService`, `SharedFolderAuditRepository`, `SharedFolderAuditSink`, `MongoSharedFolderAuditSink` | conforming | No change |

## Task Breakdown

### Task 1 - Conform audit and web

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SharedFolderAuditRecorder.currentRequest`, `currentRequestAlreadyRecorded`, `markCurrentRequest`, `currentClientIp`, `failureCategory`; `SharedFolderNoStoreFilter` audit classification |
| **Inspection** | All files in Inputs at `5b7ef3ce` |
| **Behavior** | Same audit records, markers, categories, headers and responses |
| **Invariants** | Routes, actions and stored audit fields unchanged |
| **Boundary/API** | None public |
| **Effects and failures** | None new |
| **Tests and evidence** | Shared-folder and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Audit recorder, filter and controller tests | verify-local-app: the slice 19a access checks plus a no-store header check. Granted operations and the admin audit view need a grant or an ADMIN, neither of which has a supported local path |
| AC-4 | Required PR checks | `wait_for_github.py live`, merged through the deploy gate |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| An audit record loses its client address | Low | The `Optional` chain falls back to `UNKNOWN` in exactly the old cases; the recorder tests cover requests with and without a context |

## Implementation Log

### 2026-10-09 - Audit and web combined

- **Change:** The planned 19b (audit) and 19c (web) are delivered together.
- **Reason:** Production auto-deploy ships only `main`'s newest green commit, so fewer, spaced merges keep it current.
- **Impact:** The umbrella ledger row 19 lists the combined part.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
