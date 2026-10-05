# Accounts, Messages, Notifications, Posts, and Moderation Issues 1155-1168 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` inline. Do not dispatch subagents. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete issues #1155, #1156, and #1158-#1168 with bounded server-side administration queries, retry-safe account deletion, stable cursor feeds, per-user conversation archive, notification fanout controls, author post editing, report deduplication, and complete moderation audit evidence.

**Architecture:** Add one small reusable opaque `(Instant,id)` cursor codec, then keep query and mutation ownership inside the existing account, message, notification, post, report, and admin subfeatures. New API page records are additive under `/2026-07-26`; existing list endpoints become bounded compatibility paths rather than unbounded reads. Account deletion is a durable idempotent workflow, while Mongo compound/sparse indexes and atomic template operations own race-sensitive dedupe, mark-all-read, stable cursor, and audit behavior.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB/MongoTemplate, Jakarta Validation, Jackson 3, Gradle, JUnit 5, Mockito, AssertJ, browser-native JavaScript, Node test runner, Thymeleaf.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\accounts-messages-moderation-1155-1168` on `codex/accounts-messages-moderation-1155-1168`.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; do not edit, reset, or clean it.
- Only comments authored by `azurras` may change scope. Issues #1155, #1156, and #1158-#1168 have no comments or attachments.
- Preserve existing API versions as bounded compatibility paths; publish page/cursor metadata on the additive `2026-07-26` routes and move first-party JavaScript to those routes.
- Page sizes are clamped server-side; opaque cursor text is strictly decoded and invalid cursors fail with `InvalidRequestException`.
- Pagination order is deterministic: every cursor query sorts by its timestamp descending and Mongo `_id` descending, and cursor predicates compare both fields.
- Conversation archive is per account, never deletes the other participant's data, and a newer message restores visibility.
- Account deletion retains public posts only after moving them to the single stable `deleted-user` identity, removes private/account-owned data, and preserves only bounded pseudonymous audit/report identifiers.
- Account cleanup steps are idempotent and durable so a partial failure can be retried without resurrecting or misattributing data.
- Notification dedupe identity includes actor, action/type, target, recipient, and a configured short window; high-volume rate state is recipient-pair scoped and cannot suppress unrelated recipients.
- Post author edits require the original author, an active non-expired post, and the configured 15-minute window; administrator moderation stays on the separate report path.
- Audit reason, before, and after values are bounded and redacted; never store passwords, tokens, request bodies, exception text, or unrelated personal fields in audit metadata.
- Invoke `chris-street-style` before every production/test/script/config code edit despite the user's request to waive it, because repository instructions require it.
- Verify the packaged app with a disposable Mongo database on a non-8080 port before merge; production port 8080 remains untouched until guarded post-merge deployment.

---

## Document Status

complete

## Objective

Finish approved campaign Batch 5 as one ordered implementation with witnessed RED/GREEN evidence, real Mongo-backed pagination/concurrency acceptance, Back Office/message/notification/feed UI verification, full regression, PR/CI/merge, production-safe verification, issue closure, and Builder closeout.

## Goals

- Return bounded account and report pages with safe filters, stable sorting, totals, and Back Office navigation.
- Delete an account through a resumable cleanup workflow that removes private data and anonymizes retained public/audit data.
- Aggregate latest distinct conversations in Mongo, page conversation history by `(createdOn,id)`, and archive visibility per user.
- Page notifications by `(createdOn,id)`, atomically mark the caller's unread notifications read, and prevent duplicate/high-volume fanout.
- Page all post feeds by opaque `(createdOn,id)` cursors and allow bounded 15-minute author edits with edited UI state and audit history.
- Enforce one open report per reporter/target under races and provide a filterable, paged report queue.
- Record and query moderator actor, target, reason, timestamp, and bounded before/after values for account and report actions.

## Inputs

- Approved spec: `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md`, Batch 5.
- Issues: #1155, #1156, #1158, #1159, #1160, #1161, #1162, #1163, #1164, #1165, #1166, #1167, and #1168.
- Base: `origin/main` at `ac74bbe30e7392781950bbc1f06f44e196adc46e`.
- Clean baseline: `check` passed in 1m39s; XML reports contain 1,173 Java tests, zero failures, and three expected skips.
- Existing account/report list paths call `findAll()`/`findAllByOrderByCreatedOnDesc()` and first-party Back Office fetches both whole payloads.
- Existing conversation summaries inspect only the newest 200 messages; message history, notifications, and posts use a timestamp or fixed limit without an ID tie-breaker.
- Existing `AdminActivity` records action/target/message/metadata, but account updates are not audited and report events do not retain explicit reason plus bounded before/after partitions.

## Branch

- Branch: `codex/accounts-messages-moderation-1155-1168` from `origin/main`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\accounts-messages-moderation-1155-1168`
- Isolated Gradle home: `A:\Projects\.gradle-codex-accounts-messages-moderation`

## Non-Goals

- Cross-device real-time push, WebSockets, full-text Atlas Search, or a new frontend framework.
- Destructive deletion of retained public post history or another conversation participant's data.
- Distributed event streaming or Redis; Mongo atomic documents and indexes are sufficient for the single deployed application contract.
- Editing replies after the same author window, administrator editing as an author, or revision restore UI.
- Replacing the existing response envelope, authentication cookie/bearer compatibility, trust rules, post expiry rules, or report resolution enum.
- Batch 6 WFL/location import work or Batch 7 VIN/scheduler/link-preview work.

## Assumptions

- Mongo string `_id` order is a stable secondary key when paired with the stored `Instant`.
- A versioned URL-safe Base64 cursor is opaque enough for traversal; strict parsing and query scoping make cursor tampering non-authorizing.
- Existing records without new sparse dedupe/archive/audit fields remain readable and do not block additive indexes.
- The single `deleted-user` account is a non-login tombstone with no credentials or personal data and gives every retained public post an honest stable author.
- The local MongoDB service supports aggregation, `updateMulti`, `findAndModify`, sparse unique indexes, and TTL indexes used by production.

## Open Questions

None. The approved spec fixes the product choices; exact implementation names below are selected from current repository patterns.

## Task Breakdown

### Task 1 - Add the stable cursor and additive API contract kernel

Sequence / dependencies:
- Runs first because message, notification, and post page APIs consume the same cursor semantics.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: encode and decode a versioned opaque cursor containing an exact UTC instant and bounded string id; expose the new API date constant.
  - Invariants: round trips preserve nanoseconds and id; null/blank means first page; malformed, oversized, wrong-version, or missing-field cursors fail closed.
  - Boundary/API: `StableCursorCodec.encode(StableCursor)` and `decode(String)` are the only cursor text boundary; feature services own query scope.
  - Effects and failures: pure computation only; invalid external text becomes `InvalidRequestException` without echoing the cursor.
  - Tests and evidence: focused codec partitions fail before types exist, then pass for round trip and each invalid class.

- [ ] Write `StableCursorCodecTest` and observe compile RED.
- [ ] Add the cursor record/codec and API version constant.
- [ ] Run the focused codec and API version tests.

#### Code Edit 1.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/APIVersion.java`
- Lines: 17-22
- Action: replace

Current:
```java
  public static final String V20260509 = "/2026-05-09";
  public static final String V20260517 = "/2026-05-17";
  public static final String V20260604 = "/2026-06-04";
  public static final String V20260712 = "/2026-07-12";
  public static final String V20260717 = "/2026-07-17";
```

Proposed:
```java
  public static final String V20260509 = "/2026-05-09";
  public static final String V20260517 = "/2026-05-17";
  public static final String V20260604 = "/2026-06-04";
  public static final String V20260712 = "/2026-07-12";
  public static final String V20260717 = "/2026-07-17";
  public static final String V20260726 = "/2026-07-26";
```

Verification:
- `.\gradlew.bat :cbell-lib:test --tests "*APIVersion*" --no-daemon --console=plain`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/pagination/StableCursorCodec.java`
- Lines: after 0
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
@Component
public final class StableCursorCodec {
  private static final String VERSION = "v1";
  private static final int MAX_ENCODED_LENGTH = 512;

  public String encode(StableCursor cursor) { /* v1\ninstant\nid -> URL-safe Base64 */ }

  public StableCursor decode(String encoded) throws InvalidRequestException {
    /* blank -> null; reject oversize, invalid Base64, wrong version, invalid Instant, or id outside 1..128 */
  }
}

public record StableCursor(Instant timestamp, String id) {}
```

Verification:
- `.\gradlew.bat :website:test --tests "*StableCursorCodecTest" --no-daemon --console=plain`

### Task 2 - Paginate and search the admin account list (#1155)

Sequence / dependencies:
- Runs after Task 1 only for the additive version constant; account paging itself is page-number based.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: administrators query page, bounded size, allowlisted sort/direction, optional status/role, and literal-safe text across username/email/first/last name; Back Office renders totals, filters, and previous/next controls.
  - Invariants: ADMIN authorization remains required; text search is escaped and capped; password/reset fields never enter DTO search output; old endpoint returns only a bounded compatibility list.
  - Boundary/API: new `GET /api/accounts/2026-07-26/admin` returns `AdminAccountPage`.
  - Effects and failures: read-only Mongo query; invalid enum/sort/page inputs return 400 rather than falling back ambiguously.
  - Tests and evidence: controller/service/query tests first fail because page types/methods are absent; JavaScript tests fail because the old unbounded endpoint and no navigation are rendered.

- [ ] Add failing account query/controller and Back Office pagination tests.
- [ ] Implement `AdminAccountQueryService` with `MongoTemplate`, escaped regex, allowlisted sort, and count/query pair.
- [ ] Keep the old list route bounded to the first 50 records and point Back Office to the additive page route.
- [ ] Run focused Java and `back-office-users` JavaScript tests.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/account/AccountService.java`
- Lines: 245-254
- Action: replace

Current:
```java
  public List<AccountDetail> getAccounts() {
    log.info("Getting all accounts");
    var accounts = accountRepository.findAll();
    return accounts.stream().map(accountMapper::toAccount).toList();
  }
```

Proposed:
```java
  public List<AccountDetail> getAccounts() {
    return adminAccountQueryService.query(AdminAccountQuery.firstCompatibilityPage()).items();
  }

  public AdminAccountPage getAdminAccounts(AdminAccountQuery query)
      throws InvalidRequestException {
    return adminAccountQueryService.query(query);
  }
```

Verification:
- `.\gradlew.bat :website:test --tests "*AccountServiceTest" --tests "*AdminAccountQueryServiceTest" --no-daemon --console=plain`

#### Code Edit 2.2
- File: `website/src/main/resources/static/js/back-office.js`
- Lines: 422-435
- Action: replace

Current:
```javascript
async function refreshDashboard() {
  clearAlert();
  [accounts, reports, activities] = await Promise.all([
    fetchJson(API.accounts.base, { headers: authHeaders() }),
    fetchJson(API.reports.list, { headers: authHeaders() }),
    fetchJson(API.admin.activity, { headers: authHeaders() }),
  ]);
  accounts = accounts || [];
  reports = reports || [];
  activities = activities || [];
  renderMetrics();
  renderReports();
  renderUsers();
  renderActivity();
}
```

Proposed:
```javascript
async function refreshDashboard() {
  clearAlert();
  const [accountPage, reportPage, activityPage] = await Promise.all([
    fetchJson(API.accounts.adminPage(accountQuery), { headers: authHeaders() }),
    fetchJson(API.reports.page(reportQuery), { headers: authHeaders() }),
    fetchJson(API.admin.activityPage(activityQuery), { headers: authHeaders() }),
  ]);
  ({ items: accounts = [], ...accountPageState } = accountPage || {});
  ({ items: reports = [], ...reportPageState } = reportPage || {});
  ({ items: activities = [], ...activityPageState } = activityPage || {});
  renderMetrics();
  renderReports();
  renderUsers();
  renderActivity();
  renderQueueNavigation();
}
```

Verification:
- `.\gradlew.bat :website:jsTest --no-daemon --console=plain`

### Task 3 - Make account deletion resumable, comprehensive, and privacy-preserving (#1156)

Sequence / dependencies:
- Runs after Task 2 so account administration returns the deletion result without reintroducing whole-collection loads.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: an admin deletion creates/resumes one durable job, moves public posts to `deleted-user`, removes credentials/reset state with the account, removes follows/trust/private messages/notifications/preferences/sessions/private feature state, and pseudonymizes reports/admin audit references.
  - Invariants: the tombstone cannot authenticate; another user's public post/history is untouched; retained report/audit rows contain only `deleted:<12 hex>` and `deleted-user`; each cleanup step can run twice safely.
  - Boundary/API: `AccountDeletionService.delete(String)` returns `AccountDeletionResult`; the existing DELETE route remains ADMIN-only.
  - Effects and failures: each idempotent Mongo step is checkpointed in `account_deletion_jobs`; a failure records safe step/category and returns 503, and retry resumes from the last completed step.
  - Tests and evidence: first tests fail because deletion only calls `accountRepository.delete`; final tests inject a failure between steps, retry, and prove exact collection cleanup/anonymization.

- [ ] Add unit tests for all cleanup categories, tombstone creation, pseudonym stability, double-delete, and injected partial failure/retry.
- [ ] Add a Mongo-backed disposable-database integration test that seeds cross-feature data and verifies collection outcomes.
- [ ] Implement the durable job, step enum, tombstone/pseudonym helpers, and bounded result.
- [ ] Route `AccountService.deleteAccount` through the deletion service and document retention.

Exact cleanup inventory:
- `accounts`: upsert the credential-free `deleted-user` tombstone, `$pull` the target id from every `followingIds`, and delete the target account last.
- `posts`: `updateMulti` the target `accountId` to `deleted-user`; retain created/edited timestamps and public text.
- `messages`, `notifications`, `notification_preferences`, `account_trust_relationships`, `hidden_post_threads`, `whatsforlunch_preferences`, `whatsforlunch_favorites`, and `whatsforlunch_ratings`: remove documents owned by or privately relating to the target.
- `whatsforlunch_sessions`: remove sessions whose creator/participants include the target because the whole object is private participant state.
- `shared_folder_upload_sessions` and `shared_folder_media_jobs`: cancel/expire through their owning service boundary before removing account-owned metadata so staging/cache cleanup semantics still run.
- `post_reports`, `admin_activity`, and `shared_folder_audit`: retain accountability while replacing target actor/reporter/reported ids with `deleted:<first 12 lowercase SHA-256 hex>` and labels/usernames with `deleted-user`; clear metadata keys outside the explicit audit allowlist.
- `account_deletion_jobs`: retain the completed pseudonymous job record as the retry/idempotency proof; it contains no email, names, username, credentials, or request content.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/account/AccountService.java`
- Lines: 129-148
- Action: replace

Current:
```java
  public AccountDetail deleteAccount(String accountId) throws ResourceNotFoundException {
    log.info("Deleting account with id: {}", accountId);
    var account =
        accountRepository
            .findById(accountId)
            .orElseThrow(
                () ->
                    new ResourceNotFoundException(
                        String.format("Account with id %s not found.", accountId)));
    accountRepository.delete(account);
    log.info("Successfully deleted account with id: {}", accountId);
    return accountMapper.toAccount(account);
  }
```

Proposed:
```java
  public AccountDeletionResult deleteAccount(String accountId)
      throws InvalidRequestException, ResourceNotFoundException {
    return accountDeletionService.delete(accountId);
  }
```

Verification:
- `.\gradlew.bat :website:test --tests "*AccountDeletionServiceTest" --tests "*AccountServiceTest" --tests "*AccountControllerTest" --no-daemon --console=plain`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/account/deletion/AccountDeletionService.java`
- Lines: after 0
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
@Service
public final class AccountDeletionService {
  public AccountDeletionResult delete(String accountId)
      throws InvalidRequestException, ResourceNotFoundException {
    /* load/create durable job; execute idempotent ordered steps; checkpoint each step;
       persist safe FAILED category or COMPLETE result */
  }

  private void anonymizePublicPosts(AccountDeletionJob job) { /* updateMulti accountId */ }
  private void removePrivateData(AccountDeletionJob job) { /* bounded exact collection queries */ }
  private void pseudonymizeRetainedAudit(AccountDeletionJob job) { /* bounded identifiers only */ }
}
```

Verification:
- `.\gradlew.bat :website:test --tests "*AccountDeletion*" --tests "*MongoIndexAnnotationTest" --no-daemon --console=plain`

### Task 4 - Aggregate, page, and archive conversations (#1158-#1160)

Sequence / dependencies:
- Runs after Task 1 for stable cursor encoding and after Task 3 so deletion cleanup includes archive state.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: Mongo aggregation returns the latest message for every distinct participant pair regardless of one thread's volume; history returns bounded cursor pages; an authenticated user archives only their view and any newer message restores it.
  - Invariants: participant authorization derives from the current account plus resolved username; archive never deletes or mutates the other participant's messages; returned history is chronological within each page while cursor traversal is newest-to-oldest.
  - Boundary/API: additive routes return `ConversationPage` and accept `cursor,size`; `POST .../conversation/{username}/archive` returns the archived summary state.
  - Effects and failures: aggregation/query reads, page-contained unread updates, and one owner-keyed archive upsert; invalid cursor/username is 400/404 and cross-user archive IDs are never accepted.
  - Tests and evidence: seed >200 messages in one thread plus an older second thread for RED; tie timestamps for cursor RED; archive/new-message visibility and authorization partitions.

- [ ] Add failing repository integration tests for distinct summaries and stable cursor ties.
- [ ] Add failing service/controller tests for archive ownership and new-message restore.
- [ ] Implement `ConversationQueryRepository` with Mongo aggregation/query and `ConversationArchiveState` owner/conversation unique index.
- [ ] Update messages UI with Load older and Archive controls while preserving send behavior.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/message/conversation/ConversationService.java`
- Lines: 30-86
- Action: replace

Current:
```java
  public List<MessageDetail> getConversation(String username, int limit)
      throws ResourceNotFoundException { /* first page by createdOn only */ }

  public List<ConversationSummary> getConversations(int limit) throws ResourceNotFoundException {
    var self = getSelfAccount();
    var pageSize = Math.max(1, Math.min(limit, 50));
    var page = PageRequest.of(0, 200, Sort.by(Sort.Direction.DESC, "createdOn"));
    var latestByOtherId = new LinkedHashMap<String, Message>();
    for (var message : messageRepository.findByParticipantIdsContainingOrderByCreatedOnDesc(self.getId(), page)) {
      /* fixed 200-message scan */
    }
    /* map summaries */
  }
```

Proposed:
```java
  public ConversationPage getConversation(String username, String cursor, int size)
      throws InvalidRequestException, ResourceNotFoundException {
    var participants = resolveParticipants(username);
    return conversationQueryRepository.page(
        participants.conversationKey(), participants.selfId(), cursorCodec.decode(cursor), size);
  }

  public List<ConversationSummary> getConversations(int limit) throws ResourceNotFoundException {
    var self = getSelfAccount();
    return conversationQueryRepository.latestDistinctVisible(self.getId(), boundedSummaryLimit(limit));
  }

  public ConversationArchiveResult archive(String username) throws ResourceNotFoundException {
    return conversationArchiveService.archive(resolveParticipants(username));
  }
```

Verification:
- `.\gradlew.bat :website:test --tests "*Message*" --tests "*Conversation*" --no-daemon --console=plain`

#### Code Edit 4.2
- File: `website/src/main/resources/static/js/messages.js`
- Lines: 174-199
- Action: replace

Current:
```javascript
  CONVERSATIONS = await fetchJson(`${API.messages.conversations}?limit=30`, {
    headers: authHeaders(),
    redirectOnUnauthorized: true,
  });
  // ...
  const messages = await fetchJson(`${API.messages.conversation(ACTIVE_USERNAME)}?limit=100`, {
    headers: authHeaders(),
    redirectOnUnauthorized: true,
  });
  renderMessages(messages || []);
```

Proposed:
```javascript
  CONVERSATIONS = await fetchJson(`${API.messages.conversations}?limit=30`, requestOptions());
  // ...
  const page = await fetchJson(API.messages.conversationPage(ACTIVE_USERNAME, null, 50), requestOptions());
  threadState = { items: page?.items || [], nextCursor: page?.nextCursor || null };
  renderMessages(threadState.items);
  renderConversationActions(threadState);
```

Verification:
- `.\gradlew.bat :website:jsTest --no-daemon --console=plain`

### Task 5 - Page, mark, deduplicate, and rate notifications (#1161-#1163)

Sequence / dependencies:
- Runs after Task 1 for cursor semantics and before account deletion completion so new guard/preferences collections join cleanup.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: notification pages use `(createdOn,id)`, UI appends without duplicates, mark-all-read atomically updates only the caller, and delivery claims a dedupe/rate permit before insert.
  - Invariants: recipient ownership scopes every inbox write; dedupe includes actor/type/target/recipient; per actor-recipient rate keys cannot suppress unrelated recipients or event types; preference-disabled events consume no permit.
  - Boundary/API: `NotificationPage`, `NotificationReadResult`, typed `NotificationDeliveryProperties`, and `NotificationFanoutGuard.tryAcquire(NotificationEventIdentity,Instant)`.
  - Effects and failures: `MongoTemplate.updateMulti` owns mark-all; guard uses atomic upsert/counter documents with TTL; duplicate key means already delivered, while persistence faults retain existing service-failure handling.
  - Tests and evidence: cursor ties, caller isolation, repeated event, concurrent duplicate, rate saturation, unrelated recipient/type, TTL renewal, and UI append/count tests.

- [ ] Add RED tests for page metadata, mark-all atomic scope, repeated/concurrent fanout, and unrelated-event isolation.
- [ ] Add typed validated properties and guard documents/indexes.
- [ ] Refactor all five delivery paths through one identity/permit helper.
- [ ] Add notification center Load more and Mark all read controls with deduplicating state.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/notification/inbox/NotificationInboxService.java`
- Lines: 22-55
- Action: replace

Current:
```java
  public List<NotificationDetail> getMyNotifications(int limit) {
    String selfId = permissionService.getSelfId();
    int pageSize = Math.max(1, Math.min(limit, 50));
    var page = PageRequest.of(0, pageSize, Sort.by(Sort.Direction.DESC, "createdOn"));
    return notificationRepository.findByAccountIdOrderByCreatedOnDesc(selfId, page).stream()
        .map(this::toDetail)
        .toList();
  }

  public NotificationDetail markRead(String notificationId) { /* one-row save */ }
```

Proposed:
```java
  public NotificationPage getMyNotifications(String cursor, int size)
      throws InvalidRequestException {
    return notificationQueryRepository.page(
        permissionService.getSelfId(), cursorCodec.decode(cursor), size);
  }

  public NotificationReadResult markAllRead() {
    return notificationQueryRepository.markAllRead(permissionService.getSelfId());
  }

  public NotificationDetail markRead(String notificationId) { /* retain owner-scoped one-row behavior */ }
```

Verification:
- `.\gradlew.bat :website:test --tests "*Notification*" --no-daemon --console=plain`

#### Code Edit 5.2
- File: `website/src/main/java/dev/christopherbell/notification/delivery/NotificationDeliveryService.java`
- Lines: 32-161
- Action: replace

Current:
```java
  public void createMessageNotification(Message message, Account actor, Account recipient) {
    if (message == null || actor == null || recipient == null) return;
    if (!shouldDeliver(recipient.getId(), NotificationType.MESSAGE)) return;
    notificationRepository.save(Notification.builder()
        /* direct insert without dedupe/rate identity */
        .build());
  }
```

Proposed:
```java
  public void createMessageNotification(Message message, Account actor, Account recipient) {
    deliver(NotificationEvent.message(message, actor, recipient));
  }

  private void deliver(NotificationEvent event) {
    if (!event.valid() || !shouldDeliver(event.recipientId(), event.type())) return;
    fanoutGuard.tryAcquire(event.identity(), clock.instant())
        .ifPresent(permit -> notificationRepository.save(event.toNotification(permit, clock.instant())));
  }
```

Verification:
- `.\gradlew.bat :website:test --tests "*NotificationDeliveryServiceTest" --tests "*NotificationFanoutGuardTest" --no-daemon --console=plain`

#### Code Edit 5.3
- File: `website/src/main/resources/static/js/notifications.js`
- Lines: 93-146
- Action: replace

Current:
```javascript
function renderNotifications(notifications) { /* replace entire list */ }
async function loadNotifications() {
  const [notifications] = await Promise.all([
    fetchJson(`${API.notifications.base}?limit=50`, requestOptions()),
    loadNotificationSettings()
  ]);
  renderNotifications(notifications);
}
```

Proposed:
```javascript
function appendNotifications(items) { /* merge by id, preserve order, render controls */ }
async function loadNotifications(cursor = null) {
  const page = await fetchJson(API.notifications.page(cursor, 25), requestOptions());
  notificationState.nextCursor = page?.nextCursor || null;
  appendNotifications(page?.items || []);
}
async function markAllRead() { /* POST mark-all-read, clear unread classes, refresh nav counter */ }
```

Verification:
- `.\gradlew.bat :website:jsTest --no-daemon --console=plain`

### Task 6 - Add stable post feed cursors and bounded author edits (#1164-#1165)

Sequence / dependencies:
- Runs after Task 1; account deletion in Task 3 already owns post tombstone reassignment.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: every global/user/self/following feed page compares timestamp and id; authors edit active posts within 15 minutes; response/UI exposes `editedOn` and an edited label.
  - Invariants: createdOn never changes; edit does not move a feed item; replies obey the same author/window rule; link previews are recomputed from final text; audit holds at most ten bounded before/after revisions per post.
  - Boundary/API: additive page routes return `PostFeedPage`; `PATCH /api/posts/2026-07-26/{id}` consumes validated `PostEditRequest`.
  - Effects and failures: one post save and bounded audit append; not-owner, expired, or late edits return safe 400/404 without leaking ownership; Mongo queries are compound stable.
  - Tests and evidence: tied timestamp page traversal, invalid cursor, 14:59/15:00 boundary with fixed Clock, owner/admin/non-owner, expired post, audit cap, link-preview refresh, and edited UI tests.

- [ ] Add RED stable-pagination and edit policy tests.
- [ ] Implement `PostFeedQueryRepository`, page DTO, compound `_id` indexes, and compatibility adapters.
- [ ] Implement `PostEditingService` with injected Clock, `posts.edit-window: 15m`, audit cap 10, and PATCH endpoint.
- [ ] Update feed render helpers and compose controls to show/edit eligible posts.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/post/feed/PostFeedService.java`
- Lines: 54-155
- Action: replace

Current:
```java
  public List<PostFeedItem> getGlobalFeed(Instant before, int limit, String selfId) {
    Pageable page = newFeedPage(limit);
    List<Post> posts = before != null
        ? postRepository.findByCreatedOnLessThanOrderByCreatedOnDesc(before, page)
        : postRepository.findAll(page).getContent();
    /* map list */
  }
```

Proposed:
```java
  public PostFeedPage getGlobalFeed(String cursor, int size, String selfId)
      throws InvalidRequestException {
    return mapPage(postFeedQueryRepository.global(cursorCodec.decode(cursor), size), selfId);
  }

  public PostFeedPage getUserFeed(String username, String cursor, int size, String selfId)
      throws InvalidRequestException, ResourceNotFoundException { /* scoped compound query */ }
```

Verification:
- `.\gradlew.bat :website:test --tests "*PostFeed*" --tests "*PostServiceTest" --no-daemon --console=plain`

#### Code Edit 6.2
- File: `website/src/main/java/dev/christopherbell/post/model/Post.java`
- Lines: 65-86
- Action: replace

Current:
```java
  @LastModifiedDate
  private Instant lastUpdatedOn;
  private Instant expiresOn;
  private Set<String> likedBy;
  private Integer likesCount;
  private Integer threadReplyLikesCount;
  private List<PostLinkPreview> linkPreviews;
```

Proposed:
```java
  @LastModifiedDate
  private Instant lastUpdatedOn;
  private Instant editedOn;
  @Builder.Default
  private List<PostEditAuditEvent> editAudit = new ArrayList<>();
  private Instant expiresOn;
  private Set<String> likedBy;
  private Integer likesCount;
  private Integer threadReplyLikesCount;
  private List<PostLinkPreview> linkPreviews;
```

Verification:
- `.\gradlew.bat :website:test --tests "*PostEditingServiceTest" --tests "*MongoIndexAnnotationTest" --no-daemon --console=plain`

### Task 7 - Enforce open-report uniqueness and a filterable report queue (#1166-#1167)

Sequence / dependencies:
- Runs after Task 2 so Back Office page state and controls already exist.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: a reporter/target has one open report under concurrency; the admin queue filters by status, report type, target type, reporter, and validated inclusive date range with bounded stable pages.
  - Invariants: resolved reports retain history; sparse open key is cleared on resolution and reclaimed on reopen; existing rows without a key remain readable; raw regex and unbounded dates are rejected.
  - Boundary/API: `ReportPage query(ReportQuery)` and additive controller route; submission returns the existing open report on pre-check and translates duplicate-key races consistently.
  - Effects and failures: unique sparse `openDedupeKey` owns concurrency; resolve/reopen updates key in the same saved document; read queries are count plus page.
  - Tests and evidence: sequential duplicate, concurrent duplicate-key, resolve/new report, reopen collision, each filter, tied sort, invalid range, and Back Office filter/navigation tests.

- [ ] Add RED submission race and filtered query tests.
- [ ] Add report type/target type and sparse unique open key/index.
- [ ] Implement `ReportQueryService`, bounded compatibility list, and additive page route.
- [ ] Extend Back Office report filters and navigation.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/report/submission/ReportSubmissionService.java`
- Lines: 33-58
- Action: replace

Current:
```java
  public PostReport submitReport(ReportCreateRequest request) {
    /* resolve reporter/post/reported */
    PostReport report = PostReport.builder()
        .postId(post.getId())
        .reporterAccountId(reporter.getId())
        .status(ReportStatus.OPEN)
        .build();
    return reportRepository.save(report);
  }
```

Proposed:
```java
  public PostReport submitReport(ReportCreateRequest request) {
    /* resolve reporter/post/reported and compute reporterId + POST + postId key */
    return reportRepository.findByOpenDedupeKey(openKey)
        .orElseGet(() -> saveOpenReport(openKey, request, reporter, reported, post));
  }

  private PostReport saveOpenReport(...) {
    try { return reportRepository.save(buildOpenReport(...)); }
    catch (DuplicateKeyException race) {
      return reportRepository.findByOpenDedupeKey(openKey).orElseThrow(() -> race);
    }
  }
```

Verification:
- `.\gradlew.bat :website:test --tests "*ReportSubmission*" --tests "*ReportServiceTest" --no-daemon --console=plain`

#### Code Edit 7.2
- File: `website/src/main/java/dev/christopherbell/report/ReportRepository.java`
- Lines: 11-15
- Action: replace

Current:
```java
public interface ReportRepository extends MongoRepository<PostReport, String> {
  List<PostReport> findByStatusOrderByCreatedOnDesc(ReportStatus status);
  List<PostReport> findAllByOrderByCreatedOnDesc();
  long countByReportedAccountIdAndStatus(String reportedAccountId, ReportStatus status);
}
```

Proposed:
```java
public interface ReportRepository extends MongoRepository<PostReport, String> {
  Optional<PostReport> findByOpenDedupeKey(String openDedupeKey);
  List<PostReport> findAllByOrderByCreatedOnDesc(Pageable pageable);
  long countByReportedAccountIdAndStatus(String reportedAccountId, ReportStatus status);
}
```

Verification:
- `.\gradlew.bat :website:test --tests "*Report*" --tests "*MongoIndexAnnotationTest" --no-daemon --console=plain`

### Task 8 - Expand bounded moderation audit and Back Office audit filters (#1168)

Sequence / dependencies:
- Runs after Tasks 2 and 7 because account/report moderation calls must provide before/after state and reason.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: account status/role changes and report resolve/reopen actions record actor, target, reason, timestamp, and allowlisted bounded before/after maps; authorized moderators page/filter entries.
  - Invariants: audit is append-only; mutation fails before state change when required reason is absent; passwords/email/body text never enter before/after maps; one moderation action creates one primary audit event.
  - Boundary/API: `ModerationAuditCommand` validates allowed keys and limits; `AdminActivityPage` route accepts action/target/actor/from/to/page/size.
  - Effects and failures: mutation saves domain state then audit; if audit persistence fails, surface 503 so the operator can retry idempotently; existing report resolution idempotence prevents duplicate side effects.
  - Tests and evidence: status, role, report resolve/reopen, absent/oversized reason, bounded values, forbidden keys, filter partitions, controller authorization, and UI detail rendering.

- [ ] Add RED tests showing account mutations currently create no audit and report audit lacks explicit partitions/reason.
- [ ] Extend `AdminActivity`, add query service/page controller, and central validated command.
- [ ] Require `moderationReason` for account role/status and `reason` for report resolution; update Back Office prompts/forms.
- [ ] Run all admin/account/report Java and Back Office JavaScript tests.

#### Code Edit 8.1
- File: `website/src/main/java/dev/christopherbell/admin/model/AdminActivity.java`
- Lines: 19-33
- Action: replace

Current:
```java
  @Id private String id;
  private String actorAccountId;
  private String actorUsername;
  private String action;
  private String targetType;
  private String targetId;
  private String targetLabel;
  private String message;
  private Map<String, String> metadata;
  private Instant createdOn;
```

Proposed:
```java
  @Id private String id;
  private String actorAccountId;
  private String actorUsername;
  private String action;
  private String targetType;
  private String targetId;
  private String targetLabel;
  private String reason;
  private String message;
  private Map<String, String> beforeValues;
  private Map<String, String> afterValues;
  private Map<String, String> metadata;
  private Instant createdOn;
```

Verification:
- `.\gradlew.bat :website:test --tests "*AdminActivity*" --tests "*AccountModeration*" --tests "*ReportModeration*" --no-daemon --console=plain`

#### Code Edit 8.2
- File: `website/src/main/java/dev/christopherbell/account/moderation/AccountModerationService.java`
- Lines: 47-54
- Action: replace

Current:
```java
  public AccountDetail updateAccount(AccountUpdateRequest request) {
    validateUpdateRequest(request);
    var existing = getExistingOrThrow(request.id());
    applyUpdates(existing, request);
    var saved = accountRepository.save(existing);
    return accountMapper.toAccount(saved);
  }
```

Proposed:
```java
  public AccountDetail updateAccount(AccountUpdateRequest request) {
    validateUpdateRequest(request);
    var existing = getExistingOrThrow(request.id());
    var before = ModerationAccountSnapshot.from(existing);
    applyUpdates(existing, request);
    var after = ModerationAccountSnapshot.from(existing);
    requireReasonForModerationChange(before, after, request.moderationReason());
    var saved = accountRepository.save(existing);
    recordModerationChange(before, after, request.moderationReason());
    return accountMapper.toAccount(saved);
  }
```

Verification:
- `.\gradlew.bat :website:test --tests "*AccountServiceTest" --tests "*AdminActivityServiceTest" --no-daemon --console=plain`

### Task 9 - Complete first-party UI, documentation, indexes, and full acceptance

Sequence / dependencies:
- Runs after Tasks 2-8 because it integrates every new page/action contract and performs the authoritative gate.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: Back Office, messages, notifications, home/user feeds expose the new controls and metadata accessibly; feature READMEs document pagination, retention, dedupe, edits, and moderation audit.
  - Invariants: mobile-first existing layout remains; buttons have labels/status regions; appended pages contain no duplicate IDs; compatibility endpoints remain bounded; no new npm/CDN dependency.
  - Boundary/API: first-party JavaScript uses only additive `2026-07-26` page/action endpoints through `lib/api.js`.
  - Effects and failures: failed loads preserve existing content and show safe retryable errors; destructive account deletion retains the existing admin authorization and requires an explicit confirmation phrase in UI.
  - Tests and evidence: JavaScript behavior/markup tests, full Java/JS/Pester gate, packaged runtime with seeded Mongo data, then test report.

- [ ] Finish templates/CSS/API helpers and update feature/static README contracts.
- [ ] Run focused Java classes and all Node tests.
- [ ] Run `cleanTest check`, count XML results, and run `git diff --check` plus a sensitive-value scan.
- [ ] Build `bootJar`; start the app on port 8090 with a disposable database and scheduling disabled.
- [ ] Seed admin/users/posts/messages/notifications/reports with tied timestamps; exercise account/report filters and pages, message/archive/older flow, notification load-more/mark-all, post cursor/edit, duplicate report, and audit filters through HTTP and rendered browser UI.
- [ ] Stop the exact test PID, drop only the exact disposable database, verify port 8090 free and production 8080 unchanged, and save/validate a Builder test report.

#### Code Edit 9.1
- File: `website/src/main/resources/static/js/lib/api.js`
- Lines: 8-145
- Action: replace

Current:
```javascript
  accounts: { base: '/api/accounts/2024-12-15', /* current helpers */ },
  reports: { list: '/api/reports/2025-09-03', /* current helpers */ },
  messages: { conversations: '/api/messages/2025-09-14/conversations', /* current helpers */ },
  notifications: { base: '/api/notifications/2025-09-14', /* current helpers */ },
```

Proposed:
```javascript
  accounts: { adminPage: query => withQuery('/api/accounts/2026-07-26/admin', query), /* compatibility helpers */ },
  reports: { page: query => withQuery('/api/reports/2026-07-26', query), /* resolve helpers */ },
  messages: { conversationPage: (user, cursor, size) => withQuery(`/api/messages/2026-07-26/conversation/${encodeURIComponent(user)}`, { cursor, size }), archive: user => `/api/messages/2026-07-26/conversation/${encodeURIComponent(user)}/archive` },
  notifications: { page: (cursor, size) => withQuery('/api/notifications/2026-07-26', { cursor, size }), markAllRead: '/api/notifications/2026-07-26/read' },
  posts: { feedPage: query => withQuery('/api/posts/2026-07-26/feed', query), edit: id => `/api/posts/2026-07-26/${encodeURIComponent(id)}` },
```

Verification:
- `.\gradlew.bat :website:jsTest --no-daemon --console=plain`

#### Code Edit 9.2
- File: `website/src/main/resources/templates/back-office.html`
- Lines: 71-246
- Action: replace

Current:
```html
<div class="tab-pane fade show active" id="panel-reports" role="tabpanel">
  <div id="reportQueue" class="queue-list" aria-live="polite"></div>
</div>
<div class="tab-pane fade" id="panel-users" role="tabpanel">
  <div id="userQueue" class="queue-list" aria-live="polite"></div>
</div>
<div id="activityList" class="activity-list" aria-live="polite"></div>
```

Proposed:
```html
<div class="tab-pane fade show active" id="panel-reports" role="tabpanel">
  <form id="reportFilters" class="queue-filters"><!-- status/type/target/reporter/from/to --></form>
  <div id="reportQueue" class="queue-list" aria-live="polite"></div>
  <nav id="reportPagination" aria-label="Report pages"></nav>
</div>
<div class="tab-pane fade" id="panel-users" role="tabpanel">
  <form id="accountFilters" class="queue-filters"><!-- text/status/role/sort/size --></form>
  <div id="userQueue" class="queue-list" aria-live="polite"></div>
  <nav id="accountPagination" aria-label="Account pages"></nav>
</div>
<form id="activityFilters" class="queue-filters"><!-- actor/action/target/date --></form>
<div id="activityList" class="activity-list" aria-live="polite"></div>
<nav id="activityPagination" aria-label="Audit pages"></nav>
```

Verification:
- `.\gradlew.bat :website:jsTest :website:test --tests "*ViewControllerTest" --no-daemon --console=plain`

## Code Changes

- `cbell-lib/.../APIVersion.java`: add `V20260726`.
- `website/.../pagination/*`: add strict shared stable cursor types/tests.
- `account/*`, `account/deletion/*`, `account/moderation/*`: bounded admin query, durable deletion workflow, tombstone/anonymization, moderation audit command, DTOs/tests/docs.
- `message/*`: aggregation repository, cursor page, archive state/service/routes, model indexes, tests, messages UI.
- `notification/*`: cursor query, atomic mark-all, fanout guard/properties/documents/indexes, tests, notification UI.
- `post/*`: compound cursor repository/page, edit request/service/audit metadata, edited DTOs/routes, tests, feed UI.
- `report/*`: sparse open dedupe key, filtered page query, resolution key lifecycle, reason/audit, tests.
- `admin/activity/*`: bounded moderation audit command, filtered page query/API, tests.
- `static/js/lib/api.js`, `back-office.js`, `messages.js`, `notifications.js`, feed modules, templates/CSS/tests`: first-party integration and accessible controls.
- `application*.yml` and feature READMEs: explicit edit/dedupe/rate defaults and retention/pagination contracts.

## Files and Modules

- New shared pagination package plus feature-specific page records/query repositories.
- New account deletion job/service/result/tombstone utilities.
- New conversation archive state/repository/service.
- New notification fanout guard properties and Mongo documents.
- Existing domain documents receive only additive fields/indexes.
- Existing controllers retain old bounded routes and add `V20260726` page/action routes.

## Unit Testing

- RED commands are the task-level focused Gradle/Node commands above.
- Mongo query integration tests must use tied timestamps and more data than legacy fixed windows.
- Concurrency tests use executor barriers, not sleeps, for duplicate report and notification claims.
- Clock-bound tests use fixed/mutable `Clock`; do not assert wall-clock ranges.
- Account deletion tests inject failure at a named step, rerun, and assert exact idempotent terminal state.
- Final focused matrix:
  - `.\gradlew.bat :website:test --tests "*Account*" --tests "*Message*" --tests "*Conversation*" --tests "*Notification*" --tests "*Post*" --tests "*Report*" --tests "*AdminActivity*" --no-daemon --console=plain`
  - `.\gradlew.bat :website:jsTest --no-daemon --console=plain`

## Local Testing

- Use `A:\Projects\.gradle-codex-accounts-messages-moderation` as `GRADLE_USER_HOME`.
- Build the packaged JAR and run `local` profile on port 8090 with scheduling disabled and a timestamped disposable database not equal to production.
- Seed at least: one admin, three users, 220 messages in one conversation plus an older distinct conversation, tied-ID history rows, 60 tied notifications, tied posts, duplicate report attempts, and existing admin activity.
- Authenticate as admin/user with the local API, capture exact requests/responses for every new page/action, and exercise Back Office/messages/notifications/feed UI with browser screenshots and console inspection.
- Verify account deletion by seeding every cleanup category, forcing/retrying a failure in automated tests, and verifying runtime tombstone/private cleanup on a disposable user.
- Confirm port 8080 listener PID and `/`/readiness before and after the alternate-port run.
- Stop only the recorded port-8090 PID and drop only the exact disposable database after name and production-inequality guards.

## Validation

- Every issue maps to a focused failing test and final passing test/runtime response.
- All pages clamp sizes and preserve deterministic no-skip/no-duplicate traversal under tied timestamps.
- Account deletion is retry-safe, public history is `deleted-user`, private data is removed, and retained audit/report identifiers are bounded pseudonyms.
- Conversation archive is caller-only and new messages restore visibility.
- Notification mark-all affects only caller; dedupe/rate guards do not suppress unrelated events.
- Post editing enforces author/active/15-minute policy and emits bounded audit plus edited UI state.
- Report uniqueness survives races; account/report/audit filters and UI navigation work.
- `cleanTest check`, `verifySensorRuntime`, Node tests, diff checks, local packaged acceptance, PR platform checks, Dependency Review, and CodeQL all pass.

## Rollback or Recovery

- All document/index changes are additive; older binaries ignore new fields/collections.
- Sparse dedupe indexes do not require backfilling existing rows. If rollout fails, roll back the application release; leave new fields/collections in place.
- Account deletion is irreversible only after explicit admin action. Its durable job and idempotent steps are the recovery mechanism for interruption; never manually delete the job before COMPLETE.
- If a cursor/UI defect appears, old bounded compatibility endpoints remain available during rollback.
- Production deployment uses the native Windows guarded release workflow and automatic rollback; do not manipulate junctions or protected state manually.

## Risks

- Batch size: thirteen issues touch related but distinct features. Mitigation: execute tasks in order, run a focused gate and diff review after each, and keep one commit per independently reviewable task group.
- Mongo query/index drift: derived and aggregation field names can compile but misquery. Mitigation: real Mongo integration tests and `MongoIndexAnnotationTest` assertions.
- Account cleanup omission or privacy leak: mitigation is an explicit cleanup inventory, pseudonym allowlist, seeded cross-feature runtime verification, and retry tests.
- Cursor mistakes under equal timestamps: mitigation is compound predicates/indexes and tied-value traversal tests for every feed.
- Notification races: mitigation is database-owned unique/atomic permits and deterministic concurrent tests.
- Audit failure after domain save can leave a retry requirement. Mitigation: idempotent mutation paths, explicit 503, and tests proving retries do not duplicate effects.
- First-party UI contract churn: mitigation is additive endpoints, shared API helpers, Node regression tests, and browser acceptance.

## Completion Criteria

- Issues #1155, #1156, and #1158-#1168 meet every approved required behavior.
- Implementation plan and test report are validated and committed/pushed to Builder at phase boundaries.
- Focused RED/GREEN evidence, final full tests, packaged runtime, UI checks, cleanup, and production isolation are recorded.
- Independent review has no remaining Blocker or Warning finding.
- Branch is pushed, ready PR is open, all required checks pass, PR is merged, issues are closed, and production auto-deployment is healthy.
- Builder spoke update/review, campaign ledger, indexes, validation, and session memory are complete and pushed; live issue inventory is reduced from 26 to 13.
