# ChristopherBell.dev Void Public Discovery Implementation Plan

> **For agentic workers:** Execute this plan inline with `superpowers:executing-plans`; do not dispatch subagents. Track every task with the checkboxes below and keep one branch and one PR.

**Goal:** Add a public, non-popularity-ranked Explore surface with safe topics, genuine revival ordering, privacy-aware account suggestions, and stricter mutation limits for new accounts.

**Architecture:** Extend the Post document at the trusted write boundary with bounded topics and nullable root-only `lastExtendedOn`, then expose five independent, bounded discovery endpoints backed by explicit Mongo queries. Render `/void/explore` and `/void/topic/{topic}` as data-free server shells whose JavaScript sections fail independently, and keep all ranking inputs time- or topic-overlap-based.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, Thymeleaf, vanilla JavaScript modules, CSS, Node test runner, Gradle.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\void-public-discovery`; preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`.
- Invoke `write-chris-street-style-code` and its Java, JavaScript, template/configuration, design/API, and testing references before production edits.
- Use RED-to-GREEN behavioral tests and one focused commit per task.
- Never rank by likes, keep-alives, replies, followers, lifespan, or a composite engagement score.
- Every discovery query must filter active public data before sorting, use bounded sizes, and use an opaque cursor with a stable unique tie key.
- `lastExtendedOn` changes only for a confirmed lifespan addition; undo, edit, view, share, notification, and follow actions never update it.
- Historical posts retain `lastExtendedOn = null` until a genuine new extension.
- A post stores at most five unique topics, each at most 40 Unicode code points after normalization.
- Anonymous discovery must not expose email, permissions, follower totals, credentials, private relationships, or administrative state.
- Do not cache discovery responses; send `Cache-Control: no-store` so expired content cannot survive a cache window.
- Validate locally on a non-8080 port with both `SPRING_MONGODB_URI` and `SPRING_MONGODB_DATABASE` set before automatic deployment.

---

## Document Status

complete

## Objective

Make active Void conversations and people discoverable without turning survival or follower totals into popularity rankings.

## Goals

- Ship independently loaded New arrivals, Fading soon, Recently revived, Topics, and People sections.
- Make revival state an explicit, root-only persisted event timestamp.
- Parse, normalize, bound, deduplicate, store, query, and render hashtags safely.
- Recommend accounts using topic overlap and recent public activity, with privacy exclusions.
- Apply stricter configurable posting, reply, follow, and keep-alive budgets to accounts younger than seven days.
- Keep the Explore and topic pages public, mobile-friendly, and failure-isolated.

## Inputs

- Program spec: `docs/specs/2026-07-28-void-public-growth-program.md`.
- Release 1 production merge: `7e958e737b34563d6d49a078243437d5fa9e3377`.
- Existing stable cursor boundary: `StableCursor` and `StableCursorCodec`.
- Existing active-post authority: `PostExpirationService` and the `expiresOn` field.
- Existing relationship boundaries: `followingIds`, `AccountTrustService`, hidden threads, and active account status.

## Branch

- Branch: `codex/void-public-discovery`.
- Base: `origin/main` at `7e958e737b34563d6d49a078243437d5fa9e3377`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\void-public-discovery`.

## Non-Goals

- No ActivityPub, federation consent, WebFinger, inbox, or outbound delivery work.
- No personalized engagement ranking, leaderboard, trending score, or follower-count display.
- No historical `lastExtendedOn` inference from mutable fields.
- No database rewrite of historical post text.
- No redesign of the existing feed, Music, Messages, or Back Office.
- No separate PR for each Explore section.

## Assumptions

- The production deployment remains a single application instance, so a bounded in-process new-account limiter is proportionate for this release.
- Root posts persist `parentId` as null and every reply has a stable `rootId`.
- A topic on any active post in a thread makes that active root thread eligible for the topic feed.
- Public account suggestions may display shared topic names/counts, but never popularity totals.
- UTC is authoritative for daily anonymous rotation and account-age calculation.

## Open Questions

None. The approved defaults are a seven-day new-account window; per-hour limits of 10 root posts, 30 replies, 60 added keep-alives, and 30 new follows; eight people suggestions; and section page sizes capped at 24.

## Task Breakdown

### Task 1 - Persist safe topics and genuine revival events

Sequence / dependencies:
- First task; all later discovery queries depend on the stored fields and exact mutation semantics.

Expected files or modules:
- Post model/DTOs, topic value/extractor, creation/interaction/expiration services, mappers, tests, and post documentation.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: new posts store normalized unique hashtags; a confirmed keep-alive or reply sets the root's `lastExtendedOn`; undo leaves it unchanged.
  - Invariants: existing 24-hour calculations and shared reply expiration remain authoritative; only roots own revival state; malformed hashtags never reject otherwise-valid post text.
  - Boundary/API: `PostTopicExtractor.extract(String)` is the only text-to-topic trust boundary and returns at most five immutable `PostTopic` values; existing Like routes remain unchanged.
  - Effects and failures: creation writes one post and may update its root; keep-alive writes the target and root as today; persistence failure remains a server error and does not emit a false revival response.
  - Tests and evidence: first add failing extractor partitions and service tests for root/reply like, unlike, and reply creation; finish with focused post tests.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/post/model/Post.java`
- Lines: 82-90
- Action: replace

Current:
```java
  private Instant editedOn;

  @Builder.Default
  private List<PostEditAuditEvent> editAudit = new ArrayList<>();

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "uuuu-MM-dd'T'HH:mm:ss.SSS'Z'",
      timezone = "UTC")
  private Instant expiresOn;
```

Proposed:
```java
  private Instant editedOn;

  @Builder.Default
  private List<PostEditAuditEvent> editAudit = new ArrayList<>();

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "uuuu-MM-dd'T'HH:mm:ss.SSS'Z'",
      timezone = "UTC")
  private Instant expiresOn;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "uuuu-MM-dd'T'HH:mm:ss.SSS'Z'",
      timezone = "UTC")
  private Instant lastExtendedOn;

  @Builder.Default
  private List<PostTopic> topics = List.of();
```

Additional changes:
- Add explicit compound indexes for active-root creation, expiration, revival, and `topics.canonical` query paths.
- Add immutable `PostTopic(String canonical, String display)` and `PostTopicExtractor` files.
- Extend `PostFeedItem` and all three mapping sites with topics and `lastExtendedOn`.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*PostTopicExtractor*" --tests "*PostServiceTest*" --no-daemon`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/post/creation/PostCreationService.java`
- Lines: 80-97
- Action: replace

Current:
```java
    var post = Post.builder()
        .id(newId)
        .accountId(account.getId())
        .text(text)
        .rootId(rootId)
        .parentId(parentId)
        .level(level)
        .likedBy(new HashSet<>())
        .likesCount(0)
        .createdOn(now)
        .lastUpdatedOn(now)
        .expiresOn(postExpirationService.expirationForNewPost(now, inheritedReplyExpiration))
        .linkPreviews(postLinkPreviewService.resolveForText(text))
        .build();

    var saved = postRepository.save(post);
    postExpirationService.refreshThreadRootExpirationForNewReply(saved);
```

Proposed:
```java
    var post = Post.builder()
        .id(newId)
        .accountId(account.getId())
        .text(text)
        .rootId(rootId)
        .parentId(parentId)
        .level(level)
        .likedBy(new HashSet<>())
        .likesCount(0)
        .createdOn(now)
        .lastUpdatedOn(now)
        .expiresOn(postExpirationService.expirationForNewPost(now, inheritedReplyExpiration))
        .topics(postTopicExtractor.extract(text))
        .linkPreviews(postLinkPreviewService.resolveForText(text))
        .build();

    var saved = postRepository.save(post);
    postExpirationService.refreshThreadRootExpirationForNewReply(saved, now);
```

Additional changes:
- Inject `Clock` into creation and interaction services and replace mutation-path `Instant.now()` calls.
- On an added root keep-alive, set that root's `lastExtendedOn` before save.
- Change `refreshThreadRootExpiration(Post,int)` to accept the confirmed extension time only for positive deltas.
- Make reply creation recalculate/save the root immediately, set `lastExtendedOn`, and synchronize all reply expirations; undo never moves the timestamp.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*PostServiceTest*" --tests "*PostExpirationService*" --no-daemon`

- [x] Add and witness Task 1 RED tests.
- [x] Implement topic extraction/storage and revival mutation semantics.
- [x] Run focused tests and commit Task 1.

### Task 2 - Add bounded Explore and topic query APIs

Sequence / dependencies:
- Runs after Task 1 because queries require `topics` and `lastExtendedOn`.

Expected files or modules:
- `post/discovery` query/service/DTO/controller files, migration V004, API docs, and repository/controller tests.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: anonymous callers can page New arrivals, Fading soon, Recently revived, Topics, and one topic's active threads using stable opaque cursors.
  - Invariants: each query filters `expiresOn > now`; post sections return roots only; revived excludes null history; no query uses engagement totals.
  - Boundary/API: versioned GET endpoints live under `/api/posts/2026-07-28/discovery`; size is clamped to 1-24 and malformed cursors/topics return stable 400 responses.
  - Effects and failures: queries are read-only and no-store; one endpoint failure cannot affect another endpoint; database errors remain server errors.
  - Tests and evidence: add failing Mongo query tests for ordering/ties/expiration and MVC tests for bounds/no-store before implementation.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/post/discovery/VoidDiscoveryQueryRepository.java`
- Lines: 1-170
- Action: add

Proposed:
```java
@Repository
@RequiredArgsConstructor
public final class VoidDiscoveryQueryRepository {
  private static final int MAX_PAGE_SIZE = 24;
  private final MongoTemplate mongo;
  private final StableCursorCodec cursors;

  public VoidDiscoveryPage<Post> newArrivals(String cursor, int size, Instant now) {
    return rootPage("createdOn", Sort.Direction.DESC, cursor, size, now, false);
  }

  public VoidDiscoveryPage<Post> fadingSoon(String cursor, int size, Instant now) {
    return rootPage("expiresOn", Sort.Direction.ASC, cursor, size, now, false);
  }

  public VoidDiscoveryPage<Post> recentlyRevived(String cursor, int size, Instant now) {
    return rootPage("lastExtendedOn", Sort.Direction.DESC, cursor, size, now, true);
  }

  public VoidDiscoveryPage<Post> topic(String canonical, String cursor, int size, Instant now) {
    // Match active posts containing the canonical topic, group by rootId, load active roots,
    // and page roots newest-first by createdOn plus _id.
  }

  public VoidDiscoveryPage<VoidTopicSummary> topics(String cursor, int size, Instant now) {
    // Unwind active post topics and order each canonical topic by its latest active post or
    // confirmed extension timestamp, with canonical as the stable tie key.
  }
}
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*VoidDiscoveryQueryRepositoryTest*" --no-daemon`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/post/PostController.java`
- Lines: after 287
- Action: add

Proposed:
```java
  @GetMapping(value = V20260728 + "/discovery/new", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<Response<VoidDiscoveryPage<PostFeedItem>>> newArrivals(
      @RequestParam(defaultValue = "") String cursor,
      @RequestParam(defaultValue = "12") int size) {
    return noStore(discovery.newArrivals(cursor, size));
  }

  @GetMapping(value = V20260728 + "/discovery/fading", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<Response<VoidDiscoveryPage<PostFeedItem>>> fadingSoon(
      @RequestParam(defaultValue = "") String cursor,
      @RequestParam(defaultValue = "12") int size) {
    return noStore(discovery.fadingSoon(cursor, size));
  }

  @GetMapping(value = V20260728 + "/discovery/revived", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<Response<VoidDiscoveryPage<PostFeedItem>>> recentlyRevived(
      @RequestParam(defaultValue = "") String cursor,
      @RequestParam(defaultValue = "12") int size) {
    return noStore(discovery.recentlyRevived(cursor, size));
  }
```

Additional changes:
- Add `/discovery/topics`, `/discovery/people`, and `/discovery/topic/{canonical}` GET endpoints with identical no-store/bounds behavior.
- Add `VoidDiscoveryService`, `VoidDiscoveryPage<T>`, `VoidTopicSummary`, and focused mapping helpers.
- Add migration `V004EnsureVoidDiscoveryIndexes` with named indexes matching the query shapes; do not backfill `lastExtendedOn`.
- Update post/discovery documentation.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*VoidDiscovery*" --tests "*V004EnsureVoidDiscoveryIndexes*" --no-daemon`

- [x] Add and witness Task 2 RED query/controller/migration tests.
- [x] Implement bounded discovery APIs and indexes.
- [x] Run focused tests and commit Task 2.

### Task 3 - Add privacy-aware people discovery and new-account limits

Sequence / dependencies:
- Runs after Task 2 so people discovery can reuse normalized topics and active-post query boundaries.

Expected files or modules:
- Account discovery service/query DTOs, trust repository query, new-account limiter/properties, post/follow service wiring, configuration, and tests.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: signed-in people suggestions use topic overlap; anonymous suggestions rotate recent active accounts deterministically per UTC day; young accounts receive stricter mutation budgets.
  - Invariants: self, followed, blocked in either direction, muted, suspended, and missing accounts are excluded; follower/like/lifespan totals are never inputs; undo/unfollow do not consume add-action budgets.
  - Boundary/API: `VoidPeopleDiscoveryService.suggestions(Optional<String>, Instant)` returns at most eight public DTOs; `NewAccountVoidMutationLimiter.require(Account, VoidMutationKind)` is the only age/budget boundary.
  - Effects and failures: suggestions are read-only; limiter state is bounded process-local LRU state; a rejected mutation returns 429 with retryable generic copy before the domain write.
  - Tests and evidence: first add failing overlap/exclusion/daily-rotation tests and limiter age/action/window partitions; finish with service integration tests.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/post/discovery/VoidPeopleDiscoveryService.java`
- Lines: 1-155
- Action: add

Proposed:
```java
@Service
@RequiredArgsConstructor
public final class VoidPeopleDiscoveryService {
  private static final int MAX_SUGGESTIONS = 8;
  private final VoidPeopleDiscoveryQueryRepository queries;
  private final AccountRepository accounts;
  private final AccountTrustRepository trust;
  private final PermissionService permissions;
  private final Clock clock;

  public List<VoidPersonSuggestion> suggestions() {
    Optional<String> selfId = permissions.hasAuthority("USER")
        ? Optional.of(permissions.getSelfId())
        : Optional.empty();
    Instant now = clock.instant();
    return selfId.isPresent()
        ? signedInSuggestions(selfId.get(), now)
        : dailyRecentRotation(now);
  }
}
```

Additional changes:
- Build signed-in interests from topics the account posted, replied to, or kept alive.
- Score only distinct shared topics, then recent active public activity, then account ID.
- Use a bounded recent-active candidate pool and a UTC-date hash/rotation for anonymous results.
- Return only account ID, username, shared display topics, recent activity time, and current follow state.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*VoidPeopleDiscovery*" --no-daemon`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/post/abuse/NewAccountVoidMutationLimiter.java`
- Lines: 1-150
- Action: add

Proposed:
```java
@Service
public final class NewAccountVoidMutationLimiter {
  private static final Duration NEW_ACCOUNT_AGE = Duration.ofDays(7);
  private static final Duration WINDOW = Duration.ofHours(1);
  private final Clock clock;
  private final Map<MutationKey, Window> windows;

  public synchronized void require(Account account, VoidMutationKind kind) {
    if (account.getCreatedOn() == null
        || !account.getCreatedOn().plus(NEW_ACCOUNT_AGE).isAfter(clock.instant())) {
      return;
    }
    // Consume the configured per-kind budget from bounded LRU state or throw HTTP 429.
  }
}
```

Additional changes:
- Define `VoidMutationKind` capacities: ROOT_POST 10, REPLY 30, KEEP_ALIVE 60, FOLLOW 30 per hour.
- Call the limiter after loading the fresh persisted account and before root/reply creation, added keep-alive, and new follow persistence.
- Do not consume for keep-alive undo, unfollow, or failed target validation.
- Add typed configuration with the approved defaults and a maximum of 10,000 tracked account/action keys.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*NewAccountVoidMutationLimiter*" --tests "*AccountFollowService*" --tests "*PostServiceTest*" --no-daemon`

- [x] Add and witness Task 3 RED suggestion/limiter tests.
- [x] Implement privacy exclusions, deterministic anonymous rotation, and service-level limits.
- [x] Run focused tests and commit Task 3.

### Task 4 - Render the public Explore and topic experience

Sequence / dependencies:
- Runs after Tasks 1-3 because it consumes all discovery endpoints.

Expected files or modules:
- View routes, Explore/topic templates, discovery JavaScript modules/API constants, navigation, CSS, accessibility/source tests, and docs.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Explore is a public top-level destination; five sections load independently with local retry/empty/load-more states; topic chips open canonical topic pages.
  - Invariants: one failed request never blanks another section; rendered text uses DOM text nodes/sanitization; media keeps playing through ordinary navigation using the existing global player.
  - Boundary/API: `loadDiscoverySection` consumes one no-store page envelope and owns one section; feed cards reuse `createFeedItem`; topic routes use `encodeURIComponent` and server canonical validation.
  - Effects and failures: browser effects are GET-only and cancellable; repeated Load more uses the returned opaque cursor; 400 and 5xx responses render bounded local messages.
  - Tests and evidence: first add failing nav/markup/module tests for independence, escaping, and cursor flow; finish with desktop/mobile browser checks.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/view/voidroutes/VoidViewController.java`
- Lines: after 31
- Action: add

Proposed:
```java
  /** Serves the public Void discovery shell. */
  @GetMapping(value = "/void/explore")
  public String getVoidExplorePage(HttpServletResponse response) {
    response.setHeader("Cache-Control", "no-store, max-age=0");
    return "void/explore.html";
  }

  /** Serves one canonical public topic shell without embedding post data. */
  @GetMapping(value = "/void/topic/{topic}")
  public String getVoidTopicPage(
      @PathVariable String topic, HttpServletResponse response, Model model) {
    model.addAttribute("topic", PostTopic.canonicalizeRoute(topic));
    response.setHeader("Cache-Control", "no-store, max-age=0");
    return "void/topic.html";
  }
```

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:test --tests "*ViewControllerTest*" --no-daemon`

#### Code Edit 4.2
- File: `website/src/main/resources/static/js/components/nav.js`
- Lines: 46-53
- Action: replace

Current:
```javascript
export function topLevelNavItems(isAuthenticated) {
    return [
        { href: '/void', label: 'Feed' },
        { href: '/music', label: 'Music' },
        { href: messagesNavHref(isAuthenticated), label: 'Messages' },
    ];
}
```

Proposed:
```javascript
export function topLevelNavItems(isAuthenticated) {
    return [
        { href: '/void', label: 'Feed' },
        { href: '/void/explore', label: 'Explore' },
        { href: '/music', label: 'Music' },
        { href: messagesNavHref(isAuthenticated), label: 'Messages' },
    ];
}
```

Additional changes:
- Make `/void/explore` and `/void/topic/**` activate Explore rather than Feed.
- Add `void/explore.html`, `void/topic.html`, `void-discovery.js`, and focused pure helpers for page state and safe rendering.
- Add API builders for all discovery endpoints.
- Render five independent sections: New arrivals, Fading soon, Recently revived, Topics, and People you may want to follow/Recently active people.
- Reuse existing feed cards; add restrained topic chips, local error/retry blocks, empty explanations, and cursor-based Load more buttons.
- Add responsive CSS and update JavaScript/CSS/view documentation.

Verification:
- `node --test website/src/test/js/void-discovery.test.js website/src/test/js/nav-messages-link.test.js website/src/test/js/a11y-markup.test.js`

- [x] Add and witness Task 4 RED view/JavaScript tests.
- [x] Implement independent sections, topic pages, navigation, and responsive styles.
- [x] Run focused tests and commit Task 4.

### Task 5 - Validate, publish, deploy, and close Release 2

Sequence / dependencies:
- Runs after Tasks 1-4 are green.

Operational steps:
- Run `git diff --check`, focused Java/JavaScript tests, and full `:website:check` with `GRADLE_USER_HOME=A:\Temp\gradle-void-discovery`.
- Review the final diff for popularity inputs, unbounded queries, raw regex/topic use, expired-content leakage, relationship leaks, and unrelated edits.
- Start the app on port 8081 with both `SPRING_MONGODB_URI=mongodb://127.0.0.1:27017` and `SPRING_MONGODB_DATABASE=christopherbell_void_discovery_test`.
- Seed controlled active, fading, revived, topic, trust, and new-account fixtures only in that isolated database.
- Exercise all five APIs, cursor continuation, public Explore/topic UI, localized failure rendering, anonymous/signed-in people behavior, and 429 new-account limits on desktop and mobile.
- Save and validate the Builder test report, commit/push its checkpoint, push the spoke branch, open one PR, wait for CI/dependency-review/CodeQL, and merge.
- Confirm the automatic deployment reaches the exact merge SHA without prompts; smoke Explore, topic pages, Feed, Music persistent player, Messages, and Back Office.
- Update the program spec, complete this plan, save session memory, refresh indexes, validate Builder, and commit/push Builder `main`.

- [x] Focused and full automated validation passes.
- [x] Correctly isolated non-8080 runtime and browser verification passes.
- [x] One PR passes required checks, merges, and deploys automatically.
- [x] Production exact-SHA smoke and Builder closure artifacts pass.

## Code Changes

- `Post`, `PostTopic*`, creation/interaction/expiration services: persist normalized topics and genuine root revival timestamps.
- `post/discovery/*`, `PostController`, migration V004: provide bounded no-store discovery pages and matching indexes.
- Account/trust queries and `post/abuse/*`: provide relationship-safe people suggestions and stricter new-account budgets.
- `VoidViewController`, Explore/topic templates, JavaScript, nav, API constants, and CSS: render the public failure-isolated experience.
- Java and JavaScript tests/documentation: prove ordering, bounds, privacy, escaping, cursor, failure, and responsive contracts.

## Files and Modules

- `website/src/main/java/dev/christopherbell/post/{model,creation,interaction,expiration,discovery,abuse}/**`
- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V004EnsureVoidDiscoveryIndexes.java`
- `website/src/main/java/dev/christopherbell/view/voidroutes/VoidViewController.java`
- `website/src/main/resources/templates/void/{explore.html,topic.html}`
- `website/src/main/resources/static/js/{void-discovery.js,lib/void-discovery.js,lib/api.js,components/nav.js}`
- `website/src/main/resources/static/css/main.css`
- Focused Java and JavaScript tests under existing repository test roots.

## Unit Testing

- Topic extractor: Unicode boundaries, punctuation, malformed values, deduplication, display/canonical preservation, five-topic cap, and 40-code-point cap.
- Revival: root like, reply like, unlike, root/reply creation, edits, and historical null behavior.
- Query repository: each sort direction, stable ties, expired exclusion, roots-only sections, topic-from-reply thread mapping, cursor continuation, size caps, and malformed cursor/topic rejection.
- People: interest sources, overlap ranking, no-popularity inputs, exclusions in both block directions, following/self/deleted/suspended filtering, deterministic daily anonymous rotation, and public DTO fields.
- Limiter: account-age boundary, each action budget, independent windows, bounded eviction, undo/unfollow bypass, and 429 response.
- Browser modules: independent request failures, safe text/topic rendering, cursor flow, empty copy, retry, nav active state, and mobile markup.

## Local Testing

- Use port 8081 and database `christopherbell_void_discovery_test`; set both Mongo environment properties explicitly.
- Confirm production database counts for every controlled fixture ID remain zero before and after the run.
- Verify each Explore section independently with controlled timestamps and ties.
- Confirm a topic added in a reply makes its active root discoverable without exposing an expired thread.
- Confirm signed-in suggestions exclude self/followed/muted/blocked accounts and anonymous rotation is stable within one UTC day.
- Confirm new-account limits reject only the first over-budget add action and do not count undo/unfollow.
- Simulate one endpoint failure and confirm all other sections remain usable.
- Check desktop and mobile layouts for overflow, focus order, section labels, Load more, topic routes, and persistent media playback navigation.

## Validation

- Every Release 2 acceptance criterion maps to a focused automated test and runtime observation.
- No discovery query references `likesCount`, `likedBy` size, reply count, follower count, or calculated lifespan as an ordering input.
- All API results are bounded, stable, active-only, public-safe, escaped, and no-store.
- Full Gradle/Node verification, PR CI, dependency review, and CodeQL pass.
- Automatic production deployment serves the merge SHA and public smoke routes remain healthy.

## Rollback or Recovery

- Before merge, keep recovery to the isolated branch/worktree.
- After merge, the existing release rollback can restore the previous artifact; added Post fields are nullable/optional and old binaries ignore them.
- V004 creates indexes only and does not rewrite documents; rollback may leave harmless compatible indexes.
- If one discovery section fails, its independent UI boundary continues to isolate the failure while rollback is evaluated.

## Risks

- A compound Mongo query can accidentally use popularity or omit expiration; centralize active criteria and assert generated query/aggregation shapes.
- Multikey topic aggregation can grow; cap topics at write time, cap page/candidate pools, and create exact named indexes.
- Updating `lastExtendedOn` on undo would corrupt revival meaning; branch only on confirmed positive extension and test unchanged timestamps.
- Relationship exclusion can leak blocked accounts if checked one way; query both block directions and test each partition.
- Topic routes can become regex or HTML injection; canonicalize exact strings, never build raw regex, and render through text-safe boundaries.
- In-process abuse limits reset on application restart; this is accepted for the single-instance release and can move to a distributed store if deployment topology changes.
- Local profile Mongo URI and database are separate properties; omitting either can touch production data. The runtime command and test report must show both.

## Completion Criteria

- Release 2 APIs and pages satisfy all approved ordering, topic, people, failure-isolation, abuse, and privacy rules.
- `lastExtendedOn` and topic fields have explicit tested mutation semantics with no historical backfill.
- All queries are bounded, stable, indexed, active-only, and no-store.
- Desktop/mobile runtime evidence exists against an isolated database and production fixture counts remain zero.
- One focused PR is merged after required checks, automatic deployment completes, and exact-SHA production smoke passes.
- Builder test report, updated spec/plan, closure text, session memory, indexes, validation, commit, and push are complete.
