# Notification Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every file in the notification slice conforms to write-chris-street-style-code, and delivery, inbox reads, read state and preferences behave exactly as before.

## Background
This is slice 9 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `38907c6c` found:

1. **Dead facade.** `notification.NotificationService` has no production callers; only its own test uses it. Its imports of post, message, account and WFL models hold four frozen cross-area violations open.
2. **Duplicated mapping.** `toDetail` is copied in `NotificationInboxService` and `NotificationQueryRepository`.
3. **Overloaded read name.** `getMyNotifications(limit)` and `getMyNotifications(cursor, size)` share a name but return different read models.
4. **Dense fanout guard.** `NotificationFanoutGuard` puts builder chains and statements on single lines and uses generic `query`, `update` and `value` names.
5. **Effects in a lambda.** Delivery saves and releases permits inside an `ifPresent` lambda.
6. **Hard-wired clock.** The cleanup job uses `Clock.systemUTC()` in its Spring constructor.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Notifications are delivered, read and configured as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing dedupe or rate-limit windows, hashes or stored claim ids | Stored guard documents and delivery semantics |
| Replacing the `Optional<StableCursor>` page parameter | Shared shape with the message and federation ports; a later cross-feature change |
| Changing `Notification` to a record | Persisted document shape |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass, the frozen architecture store only loses entries, and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with two disposable USERs, the published test report records that: a direct message notifies the recipient (unread count 1); the list and paged inbox show it; marking it read and marking all read update the count; turning off message notifications stops a new message from notifying; anonymous access is rejected as in production |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 9; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `38907c6c`:
  - All `notification` Java and READMEs.
  - All 13 notification test files.
  - Production callers: `NotificationDeliveryService` is called by post, message and WFL. The facade has no callers.
  - `static/js/notifications.js`, `templates/notifications.html`, and the frozen architecture store.

## Branch
`claude/style-notification-20261006` from spoke `origin/main` `38907c6c`.

## Assumptions
- The application `Clock` bean is system UTC.

## Open Questions
None.

## Design
- **Facade:** deleted. Its test becomes `NotificationDeliveryServiceTest`, which builds the delivery service directly, and the four frozen entries leave the store.
- **Shared mapping:** `NotificationDetail.from` replaces both copies.
- **Inbox:** `NotificationInboxService` exposes `listMyNotifications`, `myNotificationPage`, `markAllRead`, `countMyUnreadNotifications` and `markRead`.
- **Fanout guard:** `NotificationFanoutGuard` isolates claim acquisition in `claimEvent` with named queries and adds a `byId` helper. `sha256Hex` replaces `hash`.
- **Delivery:** `NotificationDeliveryService.deliver` returns early when no permit is granted, then saves, releasing the permit and suppressing release failures on a save failure.
- **Cleanup:** the cleanup job takes the `Clock` bean.

| Alternative | Why not |
|---|---|
| Keep the facade for "existing callers" | It has none; an unused abstraction misleads readers and keeps architecture debt alive |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/notification/NotificationService.java` | removed | Unused facade (rule 9) |
| `website/src/main/java/dev/christopherbell/notification/model/NotificationDetail.java` | changed | `from` factory (rule 9) |
| `website/src/main/java/dev/christopherbell/notification/inbox/NotificationInboxService.java` | changed | Distinct read names, shared mapping (rules 1, 6) |
| `website/src/main/java/dev/christopherbell/notification/inbox/NotificationQueryRepository.java` | changed | Named criteria, shared mapping, imports (rules 2, 9) |
| `website/src/main/java/dev/christopherbell/notification/delivery/NotificationFanoutGuard.java` | changed | `claimEvent`, named queries, formatting (rules 2, 9) |
| `website/src/main/java/dev/christopherbell/notification/delivery/NotificationDeliveryService.java` | changed | Explicit permit flow, named constant, role names (rules 7, 9) |
| `website/src/main/java/dev/christopherbell/notification/delivery/NotificationPersistenceCleanupJob.java` | changed | Application `Clock` (rule 7) |
| `website/src/main/java/dev/christopherbell/notification/NotificationController.java` | changed | `listMyNotifications`, `myNotificationPage`, `preferenceUpdate` (rule 1) |
| `website/src/main/java/dev/christopherbell/notification/MongoNotificationRepository.java`, `preference/MongoNotificationPreferenceRepository.java` | changed | Formatting and names (rule 2) |
| `website/src/main/java/dev/christopherbell/notification/preference/NotificationPreferenceService.java` | changed | `isEnabledFor`, `preferenceUpdate` (rule 1) |
| Remaining notification main files (models, ports, records, properties, configuration, READMEs) | conforming | No change |
| `website/src/test/java/dev/christopherbell/notification/NotificationDeliveryServiceTest.java` | changed (renamed from `NotificationServiceTest`) | Exercises the delivery service directly |
| `website/src/test/java/dev/christopherbell/notification/NotificationControllerTest.java`, `delivery/NotificationPersistenceCleanupJobContextTest.java` | changed | Renamed reads; `Clock` bean |
| `website/src/test/resources/architecture-baseline/e847d3fd-3e97-4258-ac91-4674dc7531ae` | changed | Four resolved entries removed |
| `website/src/main/resources/static/js/notifications.js`, `templates/notifications.html`, other notification tests | conforming | No change |

## Task Breakdown

### Task 1 - Conform the notification slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `NotificationDetail.from`; `NotificationInboxService` reads; `NotificationQueryRepository.page`, `olderThanCursor`; `NotificationFanoutGuard.tryAcquire`, `claimEvent`, `release`, `deleteExpired`; `NotificationDeliveryService.deliver`; cleanup job constructor; controller handlers |
| **Inspection** | All files in Inputs at `38907c6c` |
| **Behavior** | Same delivery rules, preference gating, dedupe, rate limit, permit release on failure, inbox paging, read marking and cleanup batches |
| **Invariants** | Routes, payloads, stored documents and claim ids unchanged; architecture store only shrinks |
| **Boundary/API** | `NotificationInboxService` read renames have callers only in the controller and tests |
| **Effects and failures** | Save failure still releases the permit and rethrows with release failures suppressed |
| **Tests and evidence** | All notification suites and architecture rules; runtime two-user flow |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check including `ModularMonolithArchitectureTest` | Covered by AC-3 |
| AC-3 | `NotificationDeliveryServiceTest` (9), `NotificationControllerTest` (10), `NotificationFanoutGuardTest` (5), preference, query and cleanup tests | verify-local-app: the two-user message, inbox, read, read-all, preference and anonymous flow in AC-3 |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Delivery permit handling changes | Low | `NotificationDeliveryServiceTest` covers release on save failure; runtime delivery |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1499 (`4ba1cf6`) and auto-deployed. Production serves the merge commit and `/notifications` returns 200 after the deploy.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check passed and the frozen store only lost four entries ([report](../test-reports/2026-10-06-21-13-christopherbell-dev-notification-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | Message notification, list, paged inbox, mark read, mark all read, opt-out and anonymous rejection recorded ([report](../test-reports/2026-10-06-21-13-christopherbell-dev-notification-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1499](https://github.com/azurras/christopherbell.dev/pull/1499) merged as `4ba1cf6` after all six checks passed; production `/actuator/info` reported `4ba1cf6` and `/notifications` returned 200 |


## Project
christopherbell-dev

## Plan Format
task-contract-v2
