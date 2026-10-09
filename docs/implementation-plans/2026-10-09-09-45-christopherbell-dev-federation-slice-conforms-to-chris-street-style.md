# Federation Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the federation slice conforms to write-chris-street-style-code, and ActivityPub discovery, collections, signing and outbound delivery behave as before.

## Background
This is slice 11 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection of all 40 main and 23 test files and the README at `50389992` found code that already meets most rules: validated records, named failures, explicit clocks and fail-closed cryptography. The remaining gaps are:

1. **Boolean flag parameter.** `FederationCollectionService.outbox` takes a `boolean page` that switches between two different results.
2. **Nulls instead of `Optional`.**
   - `FederationDeliveryStore.loadCursor` returns null when no cursor is saved.
   - `FederationOutboundCoordinator` unwraps lookups with `orElse(null)` and then checks for null.
3. **Duplication.** `FederationDiscoveryService.actor` repeats the checks in `actorAccount`.
4. **Qualified names, a braceless `if`, missing `@Override` and a redundant `String.valueOf`** in a few main files, and fully qualified names in four tests.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Discovery, the outbox and relationship collections, and consent behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR, and production federation responses are unchanged (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the shared `Optional<StableCursor>` page port | It is shared with the message and notification ports; the umbrella plan changes all three together |
| Changing routes, payloads, signing, SSRF policy, retry policy or stored fields | Product and security behavior |
| Replacing the stored delivery outcome strings with an enum | They are persisted values bounded at 64 characters; the set is internal to one repository |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, with discovery enabled for the disposable run and two disposable consenting USERs, the published test report records that: NodeInfo and WebFinger resolve; the actor, outbox summary, outbox page, followers and following answer with the same shape as production; an invalid outbox cursor is rejected; unknown and withdrawn actors return 404 |
| AC-4 | The PR merges after required checks pass, production `/actuator/info` reports the merge commit, and production federation responses equal the pre-deploy capture |

## Inputs
- **Request:** umbrella plan slice 11; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `50389992`:
  - All `federation` main and test sources.
  - The callers `AccountController`, `AccountService` and `PostRepository.findFederationEligibleAfter`.
  - `application.yml`: discovery, inbound and outbound are all disabled by default.
- **Production (read-only GETs, 2026-10-09):** discovery is enabled; NodeInfo, the actor, the outbox, the outbox page, followers and following return 200; an unknown actor returns 404.

## Branch
`claude/style-federation-20261006` from spoke `origin/main` `50389992`.

## Assumptions
- Production keeps outbound delivery off, so the outbox stays empty. The runtime check therefore covers the outbox with no items, and the unit and Mongo contract tests cover outbox items.

## Open Questions
None.

## Design
- **Outbox:**
  - `outbox(username)` returns the collection summary and `outboxPage(username, cursor, size)` returns one page.
  - A private `ActorOutbox` record holds the shared actor lookup and count.
  - The controller keeps its `page` query parameter and chooses the method.
- **Optional:**
  - `loadCursor` returns `Optional<FederationScanCursor>`; an incomplete stored state still reads as empty.
  - The coordinator filters the post and account lookups through `active` and keeps the same cancel reasons and order.
- **Discovery:** `actor(username)` is `actorForAccount(actorAccount(username))`, with the same checks in the same order.

| Alternative | Why not |
|---|---|
| Keep the boolean and document it | The two results differ in type and content; the flag hides two operations |
| Split the controller route | The `page` query parameter is the public ActivityPub contract |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/federation/discovery/FederationCollectionService.java` | changed | Split `outbox` into `outbox` and `outboxPage` (flag parameter) |
| `website/src/main/java/dev/christopherbell/federation/discovery/FederationDiscoveryController.java` | changed | Chooses the outbox method from `page` |
| `website/src/main/java/dev/christopherbell/federation/discovery/FederationDiscoveryService.java` | changed | `actor` reuses `actorAccount` (duplication) |
| `website/src/main/java/dev/christopherbell/federation/discovery/FederationOutboxQueryRepository.java` | changed | `@Override` and an imported `Pageable` |
| `website/src/main/java/dev/christopherbell/federation/outbound/FederationDeliveryStore.java`, `FederationDeliveryJobRepository.java` | changed | `Optional` cursor; braces; imported `DuplicateKeyException` |
| `website/src/main/java/dev/christopherbell/federation/outbound/FederationOutboundCoordinator.java` | changed | `Optional` lookups instead of null checks |
| `website/src/main/java/dev/christopherbell/federation/outbound/FederationActivityFactory.java` | changed | `Objects.requireNonNullElse` instead of `String.valueOf` with a ternary |
| `website/src/main/java/dev/christopherbell/federation/configuration/FederationOutboundProperties.java` | changed | Imported `Locale` |
| Remaining 31 federation main files (api, configuration, consent, discovery models, filter, identity, signing, outbound HTTP client, address policy, publication policy, records) and `federation/README.md` | conforming | No change |
| `website/src/test/java/dev/christopherbell/federation/discovery/FederationCollectionServiceTest.java`, `FederationDiscoveryControllerTest.java`, `outbound/FederationOutboundCoordinatorTest.java`, `outbound/FederationDeliveryParityContract.java` | changed | Follow the new signatures |
| `website/src/test/java/dev/christopherbell/federation/configuration/FederationPropertiesTest.java`, `consent/FederationConsentServiceTest.java`, `discovery/FederationOutboxParityContract.java` | changed | Imported names instead of fully qualified ones |
| Remaining 16 federation test files | conforming | No change |

## Task Breakdown

### Task 1 - Conform the federation slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `FederationCollectionService.outbox`, `outboxPage`; `FederationDiscoveryController.outbox`; `FederationDiscoveryService.actor`; `FederationDeliveryStore.loadCursor`; `FederationOutboundCoordinator.reconcile`, `deliver`, `configuredPeer` |
| **Inspection** | All files in Inputs at `50389992` |
| **Behavior** | Same responses, status codes, cancel reasons, scan cursor handling and checks in the same order |
| **Invariants** | Routes, payloads, signing, SSRF policy and stored fields unchanged |
| **Boundary/API** | `outbox(username, page, cursor, size)` becomes two methods; `loadCursor` returns `Optional`. All callers are in the slice and its tests |
| **Effects and failures** | None new |
| **Tests and evidence** | All federation suites; runtime discovery and collection checks |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | The federation suites | verify-local-app with discovery enabled for the disposable run: NodeInfo, WebFinger, actor, outbox summary and page, invalid cursor, followers, following, unknown and withdrawn actors, compared in shape with production |
| AC-4 | Required PR checks | `wait_for_github.py live`; production federation responses compared with the pre-deploy capture |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A production federation response changes | Low | Responses captured before the deploy and compared after |
| Outbound delivery behaves differently | Low | Coordinator tests cover cancel, success, permanent failure, retry and exhaustion; outbound is off in production |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead so the check could run during planning.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
