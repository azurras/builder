# What's for Lunch Restaurant Controller Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> `RestaurantController` conforms to write-chris-street-style-code, and every lunch route answers as before.

## Background
This is slice 17f, the last Java part of slice 17 in the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). It follows [slice 17e](2026-10-09-14-59-christopherbell-dev-whats-for-lunch-restaurant-service-conforms-to-chris-street.md), which narrowed the service signatures it depends on. Inspection at `67abb24d` found:

1. **Broad exceptions.** 22 endpoints declare `throws Exception`. Their service calls declare at most `IOException`, `InterruptedException`, `InvalidRequestException`, `ResourceExistsException` and `ResourceNotFoundException`, and `getRestaurants` declares none.
2. **Imports.** They are split into three blank-separated groups and out of order.
3. **Javadoc.** The import preview's Javadoc describes an import rather than a preview.
4. **Long lines.** Two mapping annotations exceed 120 characters.
5. **Undocumented null.** The import status endpoint unwraps an `Optional` to a null payload without saying it is the JSON contract.

## Goals
- `RestaurantController` has a recorded verdict and conforms (AC-1, AC-2).
- Every route keeps its status and body at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the import status payload from null to an absent field | The JSON contract |
| Changing routes, permissions, versions or response bodies | Product and security behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for the controller and its tests |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the public reads, invalid nearby requests and anonymous rejections answer like production, and a USER's preferences, favorites, votes and sessions behave as in slices 17c and 17e |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 17; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `67abb24d`:
  - `RestaurantController`.
  - The `throws` clauses of every `RestaurantService`, `WhatsForLunchSessionService` and `RestaurantImportWorkflowService` method it calls.
  - `RestaurantControllerTest` and `RestaurantControllerMemberSecurityTest`.

## Branch
`claude/style-lunch-controller-20261009` from spoke `origin/main` `67abb24d`.

## Assumptions
None.

## Open Questions
None.

## Design
Each endpoint declares exactly the checked exceptions its service call declares; `getRestaurants` declares none. The exception handlers already map these types, so responses are unchanged.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantController.java` | changed | Narrow `throws`; sorted imports; true preview Javadoc; wrapped annotations; documented null payload |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantControllerTest.java`, `RestaurantControllerMemberSecurityTest.java` | conforming | No change; they pass unchanged |

## Task Breakdown

### Task 1 - Conform the restaurant controller

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Slice 17e on main |
| **Files** | As listed in Expected Changes |
| **Symbols** | The 22 endpoints that declared `throws Exception`; `getOpenStreetMapImportStatus`; `previewOpenStreetMapRestaurants` |
| **Inspection** | All files in Inputs at `67abb24d` |
| **Behavior** | Same statuses and bodies |
| **Invariants** | Routes, permissions and JSON unchanged |
| **Boundary/API** | Narrower `throws` on controller methods only |
| **Effects and failures** | None new |
| **Tests and evidence** | Lunch and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Controller and member security tests | verify-local-app: the shared lunch reads, the slice 17e USER checks and the slice 17c session checks. ADMIN success paths need an ADMIN, which has no supported local path |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| None material | Low | Declaring fewer checked exceptions cannot change runtime behavior; the compiler proves each declaration is sufficient |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits.
- **Reason:** The edit was prepared while slice 17e was in CI and applied once it merged.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
