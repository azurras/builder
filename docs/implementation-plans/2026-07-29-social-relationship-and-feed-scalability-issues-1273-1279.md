# Social Relationship and Feed Scalability Issues 1273-1279 Implementation Plan

## Document Status

complete

## Objective

Resolve #1273-#1279 by moving likes/follows into unique edge collections, making desired relationship mutations retry-safe, batching feed engagement, filtering before cursor limits, bounding legacy account histories, and moving expiration repair/synchronization out of GET paths.

## Goals

- Unique atomic like/follow edges with migrated legacy arrays.
- Explicit idempotent like/unlike API plus preserved deprecated toggle compatibility.
- Constant-query feed/thread/discovery engagement mapping.
- Mongo-side expiration/trust/hidden filtering before capacity/cursors.
- Stable bounded account-history pages and capped legacy routes.
- Read-only feed GETs, atomic root reply metrics, and bulk reply expiration propagation.

## Inputs

- Campaign spec `docs/specs/2026-07-29-complete-christopherbell-dev-issues-1258-1307.md`.
- Trusted GitHub issues #1273-#1279 by `azurras`; no comments or attachments.
- `origin/main` commit `f31535f29312d24573a6031b0162aa8ebc4b5318`.
- Mandatory test-first execution and `chris-street-style`.

## Branch

`codex/issues-1273-1279-rebased-20260729` in `A:\Projects\christopherbell.dev-worktrees\issues-1273-1279-rebased-20260729`, rebased onto `a6a88e91` and squash-merged by PR #1323 as `e3afbf3c9eeb65525f573f299f82287ef8665554`.

## Non-Goals

- Redesign post content, notifications, trust semantics, moderation, or federation payload formats.
- Require replica-set transactions; production MongoDB is standalone.
- Remove old API routes in this release.

## Assumptions

- Deterministic edge IDs and exact `$setOnInsert`/delete operations provide single-document retry safety.
- Display truth comes from edge/post aggregations; embedded counters are only expiration bookkeeping.
- V009/V010 run before request service startup and backfill all legacy relationship/expiration state.
- Trust and hidden-thread exclusion sets are bounded by their owning features.

## Open Questions

None. V20260729 PUT/DELETE is the retry-safe like contract; POST toggle stays deprecated and edge-backed.

## Task Breakdown

### Task 1 - Edge collections and migrations (#1273, #1274, #1278, #1279)

Sequence / dependencies:
- First, because all service/query changes depend on migrated edge and expiration state.

Implementation notes:
- Before-Edit Brief:
  - Behavior: legacy arrays become deterministic edges; arrays are unset only after copies; roots get thread reply counts; reply expiration matches roots.
  - Invariants: unique edge pairs, bounded batches, migration lease/checksum enforcement, no unrelated field changes.
  - Boundary: owning edge stores expose collection names; migration reads raw legacy documents.
  - Effects/failures: startup stops on migration failure with retryable durable state.
  - Tests: duplicate collapse, indices, field cleanup, large-thread counts/expiration.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V009MoveSocialRelationshipsToEdges.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist. Likes live in posts.likedBy and follows in accounts.followingIds.
```

Proposed:
```java
@Override
public void apply(MongoTemplate mongo) {
  ensureUniqueEdgeIndexes(mongo);
  migrateLikesInBoundedBatches(mongo);
  migrateFollowsInBoundedBatches(mongo);
  mongo.updateMulti(new Query(), new Update().unset("likedBy"), "posts");
  mongo.updateMulti(new Query(), new Update().unset("followingIds"), "accounts");
}
```

Add `post.like.PostLike`, `account.follow.AccountFollow`, their deterministic edge stores, immutable checksums, and V010 bounded thread-count/root-expiration/reply-propagation backfill. Add V009/V010 migration tests.

Verification:
- `./gradlew.bat :website:test --tests '*V009*' --tests '*V010*'`

### Task 2 - Atomic idempotent relationship mutations (#1273, #1274)

Sequence / dependencies:
- After Task 1 models/stores.

Implementation notes:
- Desired-state PUT/DELETE returns current state; retries do not duplicate notifications or extension deltas.
- Follow timestamps use targeted account updates, never whole-document saves.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/post/interaction/PostInteractionService.java`
- Lines: 24-105
- Action: replace

Current:
```java
post.getLikedBy().add(selfId);
post.setLikesCount(post.getLikesCount() + 1);
postRepository.save(post);
```

Proposed:
```java
public PostFeedItem setLiked(String postId, String selfId, boolean desiredLiked) {
  var transition = desiredLiked
      ? postLikes.like(postId, selfId, now)
      : postLikes.unlike(postId, selfId);
  expiration.applyLikeTransition(post, transition.delta(), now);
  if (transition.created()) notifications.createPostLikeNotification(post, actor, author);
  return feedItems.single(post, author.getUsername(), selfId);
}
```

Replace `AccountFollowService` lines 20-76 with deterministic edge insert/delete and targeted timestamp touch. Add APIVersion V20260729, controller PUT/DELETE like routes, edge-backed deprecated toggle, and update `api.js`, `feed-context.js`, and `feed-render.js` to send desired state. Add concurrency/idempotence tests.

Verification:
- `./gradlew.bat :website:test --tests '*PostInteraction*' --tests '*AccountFollow*' --tests '*PostControllerTest'`
- `./gradlew.bat :website:jsTest`

### Task 3 - Constant-query engagement assembly (#1275)

Sequence / dependencies:
- After like edges are authoritative.

Implementation notes:
- One reply aggregation, one like aggregation, and at most one viewer-like query per collection of items.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/post/feed/PostFeedItemAssembler.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist. PostFeedService, PostThreadService, VoidDiscoveryService, and PostInteractionService each map items and call countByParentId per post.
```

Proposed:
```java
public List<PostFeedItem> assemble(
    List<Post> posts, Map<String, String> usernames, String viewerId) {
  var ids = posts.stream().map(Post::getId).toList();
  var replies = engagement.replyCounts(ids);
  var likes = postLikes.counts(ids);
  var liked = postLikes.likedPostIds(viewerId, ids);
  return posts.stream().map(post -> map(post, usernames, replies, likes, liked)).toList();
}
```

Add `PostEngagementQueryRepository` group-by-parent aggregation. Replace mapper blocks in `PostFeedService` lines 247-270, `PostThreadService` lines 54-73, `VoidDiscoveryService` lines 72-91, and `PostInteractionService` lines 88-105. Add page-size query-count tests at 1/50/100 items.

Verification:
- `./gradlew.bat :website:test --tests '*PostFeedItemAssemblerTest' --tests '*PostFeed*' --tests '*VoidDiscovery*'`

### Task 4 - Filter before page capacity and join follow edges (#1274, #1276)

Sequence / dependencies:
- After Tasks 1 and 3.

Implementation notes:
- Expiration, muted/blocked authors, and hidden roots become Mongo predicates before sort/limit/cursor.
- Following pages use a bounded `$lookup` into `account_follows`, not an unbounded Java ID list and `$in`.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/post/feed/PostFeedQueryRepository.java`
- Lines: 1-80
- Action: replace

Current:
```java
var query = new Query(criteria)
    .with(Sort.by(Sort.Direction.DESC, "createdOn", "_id"))
    .limit(size + 1);
```

Proposed:
```java
var criteria = visible(scope, cursor, new PostFeedVisibility(
    excludedAccountIds, excludedRootIds, expirationCutoff));
var query = new Query(criteria)
    .with(Sort.by(Sort.Direction.DESC, "createdOn", "_id"))
    .limit(size + 1);
```

Add `PostFeedVisibility`. Add `following(followerId, cursor, size, visibility)` with posts-first `$lookup`/match against `account_follows`. Replace `PostFeedService` lines 56-245 to create visibility before queries and remove post-fetch filtering/repair. Add hidden/expired-dominated capacity and stable continuation tests, plus a query-shape test proving no followed-ID `$in`.

Verification:
- `./gradlew.bat :website:test --tests '*PostFeedQueryRepositoryTest' --tests '*PostServiceTest'`

### Task 5 - Stable bounded account-history pages (#1277)

Sequence / dependencies:
- Reuses Task 4 account query.

Implementation notes:
- V20260729 returns `PostDetailPage(items,nextCursor)` capped at 100.
- V20250914 stays compatible but caps at 100 and advertises deprecation/successor headers.
- Back Office consumes the stable page and only displays its first bounded result.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/post/PostController.java`
- Lines: 60-157
- Action: replace

Current:
```java
@GetMapping(V20250914 + "/me")
public ResponseEntity<Response<List<PostDetail>>> getMyPosts() { ... }

@GetMapping(V20250914 + "/account/{accountId}")
public ResponseEntity<Response<List<PostDetail>>> getPostsByAccountId(...) { ... }
```

Proposed:
```java
@GetMapping(V20260729 + "/me")
public ResponseEntity<Response<PostDetailPage>> getMyPostsPage(
    @RequestParam(required = false) String cursor,
    @RequestParam(defaultValue = "25") int size) { ... }

@GetMapping(V20260729 + "/account/{accountId}")
public ResponseEntity<Response<PostDetailPage>> getPostsByAccountPage(...) { ... }
```

Add `PostDetailPage`; implement pages in PostService/PostFeedService. Cap legacy methods at 100 and add `Deprecation`/`Link` headers. Update `api.js` and `back-office.js` caller. Add compatibility, cap, large-history, and cursor tests.

Verification:
- `./gradlew.bat :website:test --tests '*PostControllerTest' --tests '*PostServiceTest'`
- `./gradlew.bat :website:jsTest`

### Task 6 - Pure reads and atomic/bulk expiration maintenance (#1278, #1279)

Sequence / dependencies:
- V010 supplies initial state before reads stop repairing.

Implementation notes:
- `ensureActive` only reads `expiresOn`.
- Root reply count/like-extension counters update with atomic Mongo operations.
- Reply expiration propagates by one `updateMulti`; scheduled repair processes fixed-size pages.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/post/expiration/PostExpirationService.java`
- Lines: 1-235
- Action: replace

Current:
```java
public void ensureExpirationSet(Post post) {
  refreshExpiration(post);
  postRepository.save(post);
  synchronizeReplyExpirations(post);
}

postRepository.findByRootIdOrderByCreatedOnAsc(rootId).stream()
    .forEach(reply -> postRepository.save(reply));
```

Proposed:
```java
public void ensureActive(Post post) throws ResourceNotFoundException {
  if (isExpired(post, clock.instant())) throw notFound(post);
}

public void synchronizeReplyExpirations(Post root) {
  mongo.updateMulti(rootReplies(root.getId()),
      new Update().set("expiresOn", root.getExpiresOn()), Post.class);
}
```

Add atomic `applyLikeTransition`, `recordReplyCreated`, and deletion decrement; `Post.threadReplyCount`; creation initialization; bounded pageable missing/expired queries. Remove `ensureExpirationSet` from every feed/thread GET. Add read-purity, 10,000-reply bulk, and concurrent counter tests.

Verification:
- `./gradlew.bat :website:test --tests '*PostExpirationServiceTest' --tests '*PostServiceTest'`

### Task 7 - Replace all legacy-array consumers and cleanup paths

Sequence / dependencies:
- Final integration task.

Implementation notes:
- Profile counts/followed state, federation collections, people suggestions, deletion, and post subtree cleanup must use edge stores.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/account/profile/AccountProfileService.java`
- Lines: 50-85
- Action: replace

Current:
```java
var following = account.getFollowingIds().size();
var followerCount = accountRepository.countByFollowingIdsContaining(account.getId());
var followedByMe = self.getFollowingIds().contains(account.getId());
```

Proposed:
```java
var following = follows.countFollowing(account.getId());
var followerCount = follows.countFollowers(account.getId());
var followedByMe = selfId.map(id -> follows.exists(id, account.getId())).orElse(false);
```

Replace followingIds consumers in `FederationCollectionService` and `VoidPeopleDiscoveryService`; replace likedBy interest queries with recent post-like edge IDs. Update `MongoAccountDeletionOperations` to remove `post_likes`/`account_follows`; post subtree deletion removes likes by post IDs. Remove arrays from Account/Post model creation, mapper, tombstone, READMEs, and obsolete indexes. Update integration tests.

Verification:
- `./gradlew.bat :website:test --tests '*AccountProfile*' --tests '*FederationCollection*' --tests '*VoidPeople*' --tests '*AccountDeletion*'`
- `rg -n "likedBy|followingIds" website/src/main/java` returns only V009 legacy compatibility literals.

## Code Changes

Seven literal edit boundaries above cover relationship persistence/migrations, mutation services/API/browser caller, feed assembly/querying, pagination, expiration, and integration consumers. New code remains in owning feature packages.

## Files and Modules

- `cbell-lib`: API version constant.
- `website` Java: post-like/account-follow edges and stores, V009/V010, feed assembler/query/visibility, post/account/controller/expiration/deletion/discovery/federation integration.
- `website` JavaScript: explicit like state and bounded admin history caller.
- `website` tests: migrations, concurrency, query counts, visibility/cursors, pagination, expiration bulk/read purity, integration cleanup.
- Builder: plan, report, spoke update/review, memory, ledger.

## Unit Testing

1. Failing migration and edge idempotence tests first.
2. Failing concurrent desired-state mutations before service changes.
3. Failing fixed-query-count tests before assembler.
4. Failing capacity/cursor tests before Mongo visibility/join changes.
5. Failing compatibility/cap/page tests before history routes.
6. Failing GET-purity/bulk/counter tests before expiration refactor.
7. Focused integration suites, then full gate.

## Local Testing

1. External `GRADLE_USER_HOME=A:\GradleUserHomes\cbdev-issues-1273-1279`.
2. Run `./gradlew.bat :website:check --no-daemon --console=plain`.
3. Run exact JAR on a non-8080 port with explicit disposable Mongo URI/database.
4. Seed legacy arrays and a large mixed-visible thread/feed; verify V009/V010 edges, array removal, metrics, and migration records.
5. Exercise concurrent/retried like/follow PUT/DELETE, stable capacity/cursors, bounded histories, and absence of GET writes.
6. Stop exact PID, confirm port free, drop exact disposable database.

## Validation

- #1273-#1279 acceptance criteria have automated evidence.
- No embedded relationship arrays remain after migration.
- Like/follow desired-state retries are idempotent.
- Engagement queries remain constant at page sizes 1/50/100.
- Hidden/expired rows do not consume capacity or advance cursors incorrectly.
- Legacy history <=100; stable routes cursor/cap correctly.
- Feed/thread/discovery GETs do not repair/save posts.
- Root reply count is atomic; reply expiration propagation is bulk.
- Full local/CI/security/production gates pass.

## Rollback or Recovery

- Revert the batch merge as one PR if necessary.
- V009 copies arrays before unsetting them; restore arrays from edges only if a true rollback requires old code.
- V010 is deterministic/idempotent from current posts/edges.
- Use only an exact disposable database and exact alternate PID locally.
- Preserve dirty authoritative checkout and production port 8080.

## Risks

- Standalone Mongo cannot transact across documents; edge aggregation is presentation truth, while extension counters have bounded maintenance reconciliation.
- Following `$lookup` must keep indexed cursor sorting; query-shape tests guard it.
- Startup backfill cost is controlled by fixed batches and the migration lease.
- Compatibility routes must never regain unbounded reads.

## Completion Criteria

- V009/V010 apply with reviewed checksums and runtime evidence.
- Only migration compatibility contains `likedBy`/`followingIds` literals.
- Focused concurrency/query/cursor/pagination/expiration suites pass.
- Full check, isolated runtime, review, PR matrix, main checks, production rotation, and live acceptance pass.
- #1273-#1279 close with full evidence and Builder artifacts.
