# Message Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the message slice conforms to write-chris-street-style-code, and sending, listing, opening, paging and archiving direct messages behave exactly as before.

## Background
This is slice 7 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `6dad824b` found:

1. **Hidden write behind a read name.** `getConversation` and `getConversationPage` mark incoming messages read inside a stream `peek`. A read-sounding name hides a write, against rule 7.
2. **Duplicated helpers.** The conversation-key and message-detail mapping is copied in `MessageDeliveryService` and `ConversationService`.
3. **Implicit time.** Delivery stamps `Instant.now()`, and the archive service hard-wires `Clock.systemUTC()` in its Spring constructor.
4. **Naming and structure.** Fully qualified names; anonymous `var` locals for criteria, aggregations and the latest message; one-line Mongo adapter methods; `err` and `value` names in `messages.js`.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Messaging behaves as before at runtime, including read state and archive visibility (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Replacing the `Optional<StableCursor>` parameter of `ConversationQueryPort.page` | The federation outbox and notification ports share this shape; changing one alone breaks API consistency (rule 6). It is left for a later cross-feature change |
| Changing `Message` to a record or dropping its constant `type` field | Persisted document shape |
| Changing routes, payloads, limits or the archive storage kind | Public and persisted contracts |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass, including the frozen architecture rules, and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with two disposable USERs: A messages B (201); messaging yourself gets 400; B's list shows one unread; B opens the conversation and the message is marked read; the paged API with size 1 returns a cursor that loads the older message; B archives the conversation and it leaves B's list; anonymous access is rejected. All recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 7; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `6dad824b`:
  - All `message` Java and READMEs.
  - The tests `MessageControllerTest`, `MessageServiceTest`, `ConversationArchiveServiceTest`, `ConversationQueryRepositoryTest`, `ConversationParityContract`, `MongoConversationContractTest`, `MongoMessageRepositoryContractTest` and `MessageRepositoryParityContract`.
  - The federation and notification query ports with the same `page` shape.
  - `static/js/messages.js`, `templates/messages.html` and `messages-rendering.test.js`.

## Branch
`claude/style-message-20261006` from spoke `origin/main` `6dad824b`.

## Assumptions
- The application `Clock` bean is system UTC, so delivery and archive timestamps are unchanged.

## Open Questions
None.

## Design
- **Shared helpers:** `ConversationKeys.between(a, b)` and `MessageDetail.from(message, viewerId, senderUsername, recipientUsername)` replace the copies. The helper takes usernames rather than `Account`, so the model adds no cross-area dependency.
- **`ConversationService`:**
  - `openConversation` and `openConversationPage` mark the viewer's unread incoming messages read in `markIncomingMessagesRead`.
  - `listConversations` lists summaries, and `archiveConversationWith` archives.
  - Participants resolve usernames by id through `ConversationParticipants.usernameOf`.
- **`ConversationQueryRepository.page`:** builds its cursor criteria in `olderThanCursor` and reads the slice in `newestFirstSlice`.
- **Clock:** delivery and archive take the application `Clock` bean.

| Alternative | Why not |
|---|---|
| Split the query port into `newestMessages` and `messagesBefore` | Tried first, then reverted: it makes the message port differ from the federation and notification ports |
| `MessageDetail.from(message, viewerId, Map<String, Account>)` | Adds a message-model dependency on the account model, which the frozen architecture rule would flag |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/message/conversation/ConversationService.java` | changed | `open*` names, explicit mark-read loop, shared helpers, imports (rules 1, 7, 9) |
| `website/src/main/java/dev/christopherbell/message/delivery/MessageDeliveryService.java` | changed | `Clock`, shared helpers, role names (rules 2, 7) |
| `website/src/main/java/dev/christopherbell/message/conversation/ConversationQueryRepository.java` | changed | Named criteria and slice helper, constants, imports (rules 2, 9) |
| `website/src/main/java/dev/christopherbell/message/conversation/ConversationQueryPort.java` | changed | Documented operations; `page` parameter named `olderThan` (rule 1) |
| `website/src/main/java/dev/christopherbell/message/conversation/ConversationArchiveService.java` | changed | Application `Clock` bean, named locals, import (rule 7) |
| `website/src/main/java/dev/christopherbell/message/model/ConversationKeys.java` | new | Shared conversation key (rule 9) |
| `website/src/main/java/dev/christopherbell/message/model/MessageDetail.java` | changed | `from` factory (rule 9) |
| `website/src/main/java/dev/christopherbell/message/MessageService.java`, `MessageController.java` | changed | `open*`, `listConversations`, `archiveConversationWith`, `ResponseEntity` helpers (rule 1) |
| `website/src/main/java/dev/christopherbell/message/MongoMessageRepository.java` | changed | Formatting, loop, names (rules 2, 9) |
| `website/src/main/java/dev/christopherbell/message/MessageRepository.java`, `model/Message.java`, `model/ConversationSummary.java`, `model/MessageCreateRequest.java`, `conversation/ConversationArchive*` (port, result, state), `ConversationMessageSlice`, `ConversationPage`, `ConversationUnreadCount`, READMEs | conforming | No change |
| `website/src/main/resources/static/js/messages.js` | changed | Role names for inputs and failures (rule 2) |
| `website/src/main/resources/templates/messages.html` | conforming | No change |
| `website/src/test/java/dev/christopherbell/message/MessageControllerTest.java`, `MessageServiceTest.java`, `conversation/MongoConversationContractTest.java` | changed | Renamed operations and the clock |
| Other message tests and JS tests | conforming | No change |

## Task Breakdown

### Task 1 - Conform the message slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `ConversationService.openConversation`, `openConversationPage`, `listConversations`, `archiveConversationWith`, `markIncomingMessagesRead`; `MessageDeliveryService.sendMessage`; `ConversationKeys.between`; `MessageDetail.from`; `ConversationQueryRepository.page`, `newestFirstSlice`, `olderThanCursor`; `ConversationArchiveService` constructor; facade and controller methods |
| **Inspection** | All files in Inputs at `6dad824b` |
| **Behavior** | Same send validation and errors, read marking limited to the page's incoming unread messages, oldest-first page order, cursor semantics, summary order and unread counts, archive visibility |
| **Invariants** | Routes, payloads, stored fields, indexes and archive kind unchanged; no new cross-area dependency |
| **Boundary/API** | `MessageService` and `ConversationService` renames have callers only in this slice and its tests |
| **Effects and failures** | Read-state save happens once per page with only the changed messages, as before |
| **Tests and evidence** | All message suites and the architecture rules; runtime two-user flow |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check including `ModularMonolithArchitectureTest`; full-diff style review | Covered by AC-3 |
| AC-3 | `MessageServiceTest` (9), `MessageControllerTest` (6), `ConversationQueryRepositoryTest` (4), `ConversationArchiveServiceTest` (2) | verify-local-app on isolated MongoDB `test`: the two-user send, list, open, page, archive and rejection flow in AC-3 |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Read marking or page order changes | Low | `openConversation_marksIncomingMessagesRead`; the runtime open and page cases |
| Archive marker loses its time source | Low | Spring constructor takes the `Clock` bean; runtime archive case |

## Implementation Log

### 2026-10-06 - Query port split tried, then reverted

- **Change:** The `page(key, Optional<StableCursor>, size)` port was first split into `newestMessages` and `messagesBefore`, then restored before commit, with clearer internals.
- **Reason:** The federation outbox and notification query ports share the `Optional` cursor shape. Changing one port alone would make sibling APIs inconsistent.
- **Impact:** The umbrella plan should change all three ports together in a later cross-feature step.

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
