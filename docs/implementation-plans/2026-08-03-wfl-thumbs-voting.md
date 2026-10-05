# What's For Lunch Thumbs Voting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace WFL's 1–5 restaurant ratings with migrated thumbs-up/thumbs-down votes across persistence, APIs, ranking, weighted selection, server rendering, and browser UI.

**Architecture:** V013 preflights and converts the existing rating collection to one binary vote field without moving the collection or weakening its uniqueness index. Focused vote aggregation and approval-weighted selection types feed the existing service/session boundaries, while shared SSR and browser formatters expose approval percentage plus vote counts and keep personal state authenticated.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, Thymeleaf, Jackson 3, vanilla JavaScript ES modules, Node test runner, CSS, Gradle 9.6.1, JUnit 5, Mockito, AssertJ, MockMvc, Pester, Windows PowerShell.

## Global Constraints

- Convert stored ratings `3–5` to `UP` and `1–2` to `DOWN`.
- Reject old numeric writes immediately; do not retain dual-schema reads after V013.
- Keep the physical `whatsforlunch_ratings` collection and unique restaurant/account index.
- Public summaries show rounded approval percentage plus up/down counts; zero votes show `No votes yet`.
- Top 10 Liked orders by raw approval percentage, total vote count, then restaurant ID.
- Selection uses `(upVotes + 1.5) / (upVotes + downVotes + 3)` and maps `0 → 0.35`, `0.5 → 1.0`, `1 → 2.0`.
- No vote deletion; an authenticated member may set or change one `UP`/`DOWN` vote.
- Preserve profile canonical, sitemap, 404/noindex, structured-data, public/private, and anonymous-zero-fetch boundaries.
- Preserve the dirty authoritative checkout and implement only in a new isolated worktree from refreshed `origin/main`.
- Invoke `write-chris-street-style-code` before every production-code, test, migration, template, JavaScript, CSS, or executable-documentation edit.
- Validate on a non-8080 port and disposable database before any production listener action.

---

## Document Status

complete

## Objective

Implement the approved specification at `docs/specs/2026-08-03-wfl-thumbs-voting.md` through regression-first code changes, migrated-database and browser validation, PR/CI/merge, protected production deployment, and Builder closeout.

## Goals

1. V013 converts all valid persisted ratings exactly and fails before writes on malformed or contradictory data.
2. Production Java and public JSON contracts use vote terminology and binary values only.
3. Aggregation, Top 10 Liked, daily picks, and shared-session picks use consistent vote summaries.
4. Profiles, picks, and Favorites show accessible thumb controls and approval summaries without star language.
5. Restaurant profile SEO/privacy behavior remains correct with percentage-based aggregateRating.
6. Automated, alternate-port, browser, CI, merge, deployment, production, and Builder evidence pass.

## Inputs

- Approved spec: `C:\Users\Christopher\Developer\builder\docs\specs\2026-08-03-wfl-thumbs-voting.md`.
- Approved decisions: clean V013 migration; reject numeric clients; percentage plus counts; Top 10 Liked; raw-percentage leaderboard; smoothed selection; idempotent active-thumb behavior.
- Current spoke main: `origin/main` at `363bb986581c4d20df3434154844807ce88701e4`.
- Existing migration sequence ends at V012.
- Existing profile SSR/SEO release is PR #1345 and must not regress.

## Branch

- Create at execution time with `superpowers:using-git-worktrees`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-thumbs-voting`.
- Branch: `codex/wfl-thumbs-voting`.
- Base: refreshed `origin/main` at exactly `363bb986581c4d20df3434154844807ce88701e4`; if main advances before execution, stop and refresh the inspected line ranges before changing this base.

## Non-Goals

- No Favorites semantics, shared-session participant vote, restaurant import, location, radius, or pick-count changes.
- No permanent legacy numeric write endpoint.
- No physical Mongo collection rename.
- No unrelated WFL redesign or shared-framework extraction.
- No vote clearing operation.

## Assumptions

- Rating document IDs, restaurant IDs, and account IDs remain strings.
- Existing valid production rating values are integers 1–5; V013 proves this before mutation.
- Application migrations execute in numeric order and a thrown V013 prevents candidate readiness.
- The restaurant/account unique index already prevents duplicate member votes.
- The protected production deploy path continues to build and candidate-smoke merged `origin/main`.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add the binary vote domain and fail-closed V013 migration

Sequence / dependencies:
- First task. It establishes the persisted and Java types consumed by every later task.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: valid legacy documents convert 1/2 to DOWN and 3/4/5 to UP while preserving identity and timestamps.
  - Invariants: one document per restaurant/account, stable collection/index, no partial mutation after a validation failure, retry-safe already-converted documents.
  - Boundary/API: Mongo field becomes exact enum string `vote`; numeric `rating` disappears after V013.
  - Effects and failures: two bounded stable-ID passes; preflight is read-only; malformed or contradictory documents throw before conversion.
  - Tests and evidence: first add V013 tests that fail because the migration/type does not exist, then prove exact conversion, preservation, retry, batching, and fail-closed behavior.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantVoteValue.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.whatsforlunch.restaurant.model;

/** Binary member sentiment for one WFL restaurant. */
public enum RestaurantVoteValue {
  UP,
  DOWN
}
```

Verification:
- `./gradlew.bat :website:test --tests "*V013ConvertRestaurantRatingsToVotesTest" --no-daemon`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantRating.java`
- Lines: 1-37
- Action: move

Current:
```java
@Document("whatsforlunch_ratings")
public class RestaurantRating {
  private final String type = "restaurant_rating";
  @Id private String id;
  @Indexed private String restaurantId;
  private String accountId;
  private Integer rating;
  private Instant createdOn;
  private Instant lastUpdatedOn;
}
```

Proposed:
```java
// Move to RestaurantVote.java; preserve annotations, collection, IDs, timestamps, and index.
@Document("whatsforlunch_ratings")
public class RestaurantVote {
  private final String type = "restaurant_vote";
  @Id private String id;
  @Indexed private String restaurantId;
  private String accountId;
  private RestaurantVoteValue vote;
  private Instant createdOn;
  private Instant lastUpdatedOn;
}
```

Verification:
- `./gradlew.bat :website:compileJava --no-daemon`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantRatingRequest.java`
- Lines: 1-4
- Action: move

Current:
```java
/** Request to set the caller's whole-number rating for a restaurant. */
public record RestaurantRatingRequest(Object rating) {}
```

Proposed:
```java
// Move to RestaurantVoteRequest.java.
/** Request to set the caller's binary vote for a restaurant. */
public record RestaurantVoteRequest(Object vote) {}
```

Verification:
- `./gradlew.bat :website:compileJava --no-daemon`

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantRatingSetRequest.java`
- Lines: 1-4
- Action: move

Current:
```java
/** Provider-ID-safe request to rate one restaurant. */
public record RestaurantRatingSetRequest(String restaurantId, Object rating) {}
```

Proposed:
```java
// Move to RestaurantVoteSetRequest.java.
/** Provider-ID-safe request to vote on one restaurant. */
public record RestaurantVoteSetRequest(String restaurantId, Object vote) {}
```

Verification:
- `./gradlew.bat :website:compileJava --no-daemon`

#### Code Edit 1.5
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V013ConvertRestaurantRatingsToVotes.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Component
public final class V013ConvertRestaurantRatingsToVotes implements ApplicationMigration {
  private static final int BATCH_SIZE = 250;
  private static final String COLLECTION = "whatsforlunch_ratings";
  private static final String CHECKSUM =
      "c10c2769b37044d866224770f7fb8b0877e02c2457c53d33ee25eeb879ab86f7";

  @Override public String id() { return "013-convert-restaurant-ratings-to-votes"; }
  @Override public String checksum() { return CHECKSUM; }
  @Override public String description() { return "Convert WFL 1-5 ratings to binary votes"; }

  @Override
  public void apply(MongoTemplate mongo) {
    forEachBatch(mongo, V013ConvertRestaurantRatingsToVotes::validateDocument);
    forEachBatch(mongo, document -> convert(mongo, document));
  }

  static RestaurantVoteValue targetVote(Document document) {
    Object raw = document.get("rating");
    if (!(raw instanceof Number number)
        || number.doubleValue() != number.intValue()
        || number.intValue() < 1
        || number.intValue() > 5) {
      throw new IllegalStateException("Legacy restaurant rating must be an integer from 1 to 5: "
          + document.get("_id"));
    }
    return number.intValue() >= 3 ? RestaurantVoteValue.UP : RestaurantVoteValue.DOWN;
  }

  static void validateDocument(Document document) {
    Object rating = document.get("rating");
    Object vote = document.get("vote");
    if (rating == null) {
      if (!RestaurantVoteValue.UP.name().equals(vote)
          && !RestaurantVoteValue.DOWN.name().equals(vote)) {
        throw new IllegalStateException("Restaurant vote is missing or invalid: " + document.get("_id"));
      }
      return;
    }
    RestaurantVoteValue expected = targetVote(document);
    if (vote != null && !expected.name().equals(vote)) {
      throw new IllegalStateException("Restaurant rating and vote conflict: " + document.get("_id"));
    }
  }

  private static void convert(MongoTemplate mongo, Document document) {
    if (document.get("rating") == null) return;
    mongo.updateFirst(Query.query(Criteria.where("_id").is(document.get("_id"))),
        new Update().set("vote", targetVote(document).name()).unset("rating")
            .set("type", "restaurant_vote"), COLLECTION);
  }

  private static void forEachBatch(MongoTemplate mongo, Consumer<Document> consumer) {
    String lastId = null;
    while (true) {
      Query query = lastId == null ? new Query() : Query.query(Criteria.where("_id").gt(lastId));
      query.with(Sort.by(Sort.Direction.ASC, "_id")).limit(BATCH_SIZE);
      List<Document> batch = mongo.find(query, Document.class, COLLECTION);
      if (batch.isEmpty()) return;
      batch.forEach(consumer);
      lastId = batch.getLast().getString("_id");
    }
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*V013ConvertRestaurantRatingsToVotesTest" --no-daemon`

#### Code Edit 1.6
- File: `website/src/test/java/dev/christopherbell/configuration/mongo/migration/V013ConvertRestaurantRatingsToVotesTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
@ExtendWith(MockitoExtension.class)
class V013ConvertRestaurantRatingsToVotesTest {
  @Mock MongoTemplate mongo;

  @Test void convertsOneAndTwoDownAndThreeThroughFiveUp() {
    assertThat(V013ConvertRestaurantRatingsToVotes.targetVote(
        new Document("_id", "one").append("rating", 1))).isEqualTo(RestaurantVoteValue.DOWN);
    assertThat(V013ConvertRestaurantRatingsToVotes.targetVote(
        new Document("_id", "two").append("rating", 2))).isEqualTo(RestaurantVoteValue.DOWN);
    assertThat(V013ConvertRestaurantRatingsToVotes.targetVote(
        new Document("_id", "three").append("rating", 3))).isEqualTo(RestaurantVoteValue.UP);
    assertThat(V013ConvertRestaurantRatingsToVotes.targetVote(
        new Document("_id", "four").append("rating", 4))).isEqualTo(RestaurantVoteValue.UP);
    assertThat(V013ConvertRestaurantRatingsToVotes.targetVote(
        new Document("_id", "five").append("rating", 5))).isEqualTo(RestaurantVoteValue.UP);
  }

  @Test void validatesTheWholeCollectionBeforeTheFirstWrite() {
    var documents = List.of(
        new Document("_id", "valid").append("rating", 5),
        new Document("_id", "invalid").append("rating", 6));
    when(mongo.find(any(Query.class), eq(Document.class), eq("whatsforlunch_ratings")))
        .thenReturn(documents);
    assertThatThrownBy(() -> new V013ConvertRestaurantRatingsToVotes().apply(mongo))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("invalid");
    verify(mongo, never()).updateFirst(any(Query.class), any(Update.class), anyString());
  }

  @Test void acceptsAlreadyConvertedDocumentsAndRejectsContradictions() {
    assertThatCode(() -> V013ConvertRestaurantRatingsToVotes.validateDocument(
        new Document("_id", "converted").append("vote", "UP"))).doesNotThrowAnyException();
    assertThatThrownBy(() -> V013ConvertRestaurantRatingsToVotes.validateDocument(
        new Document("_id", "conflict").append("rating", 2).append("vote", "UP")))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("conflict");
  }
}
```

Verification:
- RED: test does not compile before V013/type creation.
- GREEN: all V013 tests pass and `git diff --check` is clean.

- [x] Write the Task 1 migration/domain tests first.
- [x] Run the focused tests and record the expected RED failure.
- [x] Implement the minimal vote types and V013 behavior.
- [x] Run focused migration/model tests to GREEN.
- [x] Commit with `Migrate WFL ratings to binary votes`.

### Task 2 - Replace rating aggregation and selection with vote summaries

Sequence / dependencies:
- Runs after Task 1 because repositories and selectors consume `RestaurantVote` and `RestaurantVoteValue`.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Mongo returns up/down/total summaries and Top 10 Liked order; selection weight rises monotonically with adjusted approval.
  - Invariants: bounded queries, deterministic tie order, unique candidates, sampling without replacement, injected random validation.
  - Boundary/API: `RestaurantVoteSummary(String restaurantId, int upVotes, int downVotes, int voteCount)` is the shared immutable boundary.
  - Effects and failures: aggregate reads only; malformed summary counts fail before sampling.
  - Tests and evidence: aggregation-pipeline and selector tests fail on old rating shapes, then pass exact counts/order/anchors.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/RestaurantRatingSummary.java`
- Lines: 1-8
- Action: move

Current:
```java
public record RestaurantRatingSummary(String restaurantId, int ratingCount, int ratingSum) {}
```

Proposed:
```java
// Move to restaurant/vote/RestaurantVoteSummary.java.
public record RestaurantVoteSummary(
    String restaurantId,
    int upVotes,
    int downVotes,
    int voteCount
) {
  public RestaurantVoteSummary {
    if (restaurantId == null || restaurantId.isBlank()
        || upVotes < 0 || downVotes < 0 || voteCount != upVotes + downVotes) {
      throw new IllegalArgumentException("Restaurant vote summary is invalid");
    }
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*RestaurantVoteQueryRepositoryTest" --no-daemon`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/RestaurantRatingRepository.java`
- Lines: 1-16
- Action: move

Current:
```java
public interface RestaurantRatingRepository extends MongoRepository<RestaurantRating, String> {
  List<RestaurantRating> findByRestaurantIdIn(Collection<String> restaurantIds);
  Optional<RestaurantRating> findByRestaurantIdAndAccountId(String restaurantId, String accountId);
}
```

Proposed:
```java
// Move to restaurant/vote/RestaurantVoteRepository.java.
public interface RestaurantVoteRepository extends MongoRepository<RestaurantVote, String> {
  List<RestaurantVote> findByRestaurantIdIn(Collection<String> restaurantIds);
  Optional<RestaurantVote> findByRestaurantIdAndAccountId(String restaurantId, String accountId);
}
```

Verification:
- Repository/service/session tests compile against `RestaurantVote` only; no `RestaurantRatingRepository` import remains.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/RestaurantRatingQueryRepository.java`
- Lines: 1-59
- Action: move

Current:
```java
Aggregation.group("restaurantId")
    .count().as("ratingCount")
    .sum("rating").as("ratingSum")
```

Proposed:
```java
// Move to restaurant/vote/RestaurantVoteQueryRepository.java.
AggregationExpression up = ConditionalOperators
    .when(Criteria.where("vote").is(RestaurantVoteValue.UP.name())).then(1).otherwise(0);
AggregationExpression down = ConditionalOperators
    .when(Criteria.where("vote").is(RestaurantVoteValue.DOWN.name())).then(1).otherwise(0);
var aggregation = Aggregation.newAggregation(
    Aggregation.group("restaurantId")
        .sum(up).as("upVotes")
        .sum(down).as("downVotes")
        .count().as("voteCount"),
    Aggregation.project("upVotes", "downVotes", "voteCount")
        .and("_id").as("restaurantId")
        .andExpression("upVotes * 1.0 / voteCount").as("approvalRatio"),
    Aggregation.sort(Sort.by(
        Sort.Order.desc("approvalRatio"),
        Sort.Order.desc("voteCount"),
        Sort.Order.asc("restaurantId"))),
    Aggregation.limit(limit));
```

Verification:
- Assert generated aggregation JSON contains `upVotes`, `downVotes`, `voteCount`, conditional `vote`, approval division, and stable sort.

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/selection/RatingWeightedRestaurantSelector.java`
- Lines: 1-124
- Action: move

Current:
```java
private static final double PRIOR_RATING = 3.0;
private static final int PRIOR_RATING_COUNT = 3;
private static final double[] RATING_WEIGHTS = {0.35, 0.60, 1.00, 1.50, 2.00};
```

Proposed:
```java
// Move to ApprovalWeightedRestaurantSelector.java.
private static final double PRIOR_UP_VOTES = 1.5;
private static final double PRIOR_VOTE_COUNT = 3.0;

static double weightFor(RestaurantVoteSummary summary) {
  if (summary == null || summary.voteCount() == 0) return 1.0;
  double adjustedApproval =
      (summary.upVotes() + PRIOR_UP_VOTES) / (summary.voteCount() + PRIOR_VOTE_COUNT);
  return interpolateWeight(adjustedApproval);
}

static double interpolateWeight(double approval) {
  if (!Double.isFinite(approval) || approval < 0.0 || approval > 1.0) {
    throw new IllegalArgumentException("adjusted approval must be in [0, 1]");
  }
  return approval <= 0.5
      ? 0.35 + (1.0 - 0.35) * (approval / 0.5)
      : 1.0 + (2.0 - 1.0) * ((approval - 0.5) / 0.5);
}
```

Verification:
- `./gradlew.bat :website:test --tests "*ApprovalWeightedRestaurantSelectorTest" --no-daemon`

#### Code Edit 2.5
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/selection/RatingWeightedRestaurantSelectorTest.java`
- Lines: 1-127
- Action: move

Current:
```java
assertThat(RatingWeightedRestaurantSelector.interpolateWeight(1.0)).isEqualTo(0.35);
assertThat(RatingWeightedRestaurantSelector.interpolateWeight(5.0)).isEqualTo(2.0);
```

Proposed:
```java
assertThat(ApprovalWeightedRestaurantSelector.interpolateWeight(0.0)).isEqualTo(0.35);
assertThat(ApprovalWeightedRestaurantSelector.interpolateWeight(0.5)).isEqualTo(1.0);
assertThat(ApprovalWeightedRestaurantSelector.interpolateWeight(1.0)).isEqualTo(2.0);
assertThat(ApprovalWeightedRestaurantSelector.weightFor(null)).isEqualTo(1.0);
assertThat(ApprovalWeightedRestaurantSelector.weightFor(
    new RestaurantVoteSummary("up", 1, 0, 1))).isEqualTo(1.25);
assertThat(ApprovalWeightedRestaurantSelector.weightFor(
    new RestaurantVoteSummary("down", 0, 1, 1))).isEqualTo(0.8375);
```

Verification:
- Preserve deterministic without-replacement and invalid-random tests with vote summaries.

- [x] Write failing aggregation and selector tests.
- [x] Run focused tests to observe rating-shape failures.
- [x] Implement vote repository/summary/query and approval selector.
- [x] Run focused tests to GREEN and inspect aggregation JSON.
- [x] Commit with `Weight WFL picks by thumb approval`.

### Task 3 - Change service, session, controller, and JSON contracts to votes

Sequence / dependencies:
- Runs after Task 2 because service and session enrichment consume the vote repository, summary, and selector.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: members set/change UP or DOWN; details return vote totals/personal vote; Top 10 Liked and both selectors use the same summaries.
  - Invariants: authorization, CSRF, not-found, immutable response copy, timestamps, idempotent same-vote write, bounded leaderboard.
  - Boundary/API: replace `ratingSum/ratingCount/myRating` with `upVotes/downVotes/voteCount/myVote`; replace `/rating` with `/vote` and `/top-rated` with `/top-liked`.
  - Effects and failures: one upsert per member/restaurant; invalid strings/numbers return stable 400; repository failures propagate through established handlers.
  - Tests and evidence: service/controller/session tests fail on old methods/JSON, then pass set/change/idempotent/invalid/auth/aggregate cases.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantDetail.java`
- Lines: 34-36
- Action: replace

Current:
```java
private Integer ratingCount;
private Integer ratingSum;
private Integer myRating;
```

Proposed:
```java
private Integer upVotes;
private Integer downVotes;
private Integer voteCount;
private RestaurantVoteValue myVote;
```

Verification:
- Mapper ignores the four enriched fields and all model/controller tests compile.

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantMapper.java`
- Lines: 31-33
- Action: replace

Current:
```java
@Mapping(target = "ratingCount", ignore = true)
@Mapping(target = "ratingSum", ignore = true)
@Mapping(target = "myRating", ignore = true)
```

Proposed:
```java
@Mapping(target = "upVotes", ignore = true)
@Mapping(target = "downVotes", ignore = true)
@Mapping(target = "voteCount", ignore = true)
@Mapping(target = "myVote", ignore = true)
```

Verification:
- MapStruct generation succeeds and mapped base details leave every enriched vote field unset.

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 30-40
- Action: replace

Current:
```java
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantRating;
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantRatingRequest;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingQueryRepository;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingRepository;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingSummary;
import dev.christopherbell.whatsforlunch.restaurant.selection.RatingWeightedRestaurantSelector;
```

Proposed:
```java
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantVote;
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantVoteRequest;
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantVoteValue;
import dev.christopherbell.whatsforlunch.restaurant.selection.ApprovalWeightedRestaurantSelector;
import dev.christopherbell.whatsforlunch.restaurant.vote.RestaurantVoteQueryRepository;
import dev.christopherbell.whatsforlunch.restaurant.vote.RestaurantVoteRepository;
import dev.christopherbell.whatsforlunch.restaurant.vote.RestaurantVoteSummary;
```

Verification:
- `RestaurantService` contains no rating-domain import after the task.

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 91-93
- Action: replace

Current:
```java
private final RestaurantRatingRepository restaurantRatingRepository;
private final RestaurantRatingQueryRepository restaurantRatingQueryRepository;
private final RatingWeightedRestaurantSelector restaurantSelector;
```

Proposed:
```java
private final RestaurantVoteRepository restaurantVoteRepository;
private final RestaurantVoteQueryRepository restaurantVoteQueryRepository;
private final ApprovalWeightedRestaurantSelector restaurantSelector;
```

Verification:
- Constructor injection and Spring component wiring tests pass with the new focused dependencies.

#### Code Edit 3.5
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 369-483
- Action: replace

Current:
```java
public RestaurantDetail rateRestaurant(
    String restaurantId,
    RestaurantRatingRequest request
) throws InvalidRequestException, ResourceNotFoundException {
  var normalizedRestaurantId = validateRestaurantId(restaurantId);
  var rating = validateRating(request == null ? null : request.rating());
  var restaurant = restaurantRepository.findById(normalizedRestaurantId)
      .orElseThrow(() -> new ResourceNotFoundException("Restaurant not found: " + normalizedRestaurantId));
  var accountId = permissionService.getSelfId();
  var now = Instant.now(clock);
  var existing = restaurantRatingRepository.findByRestaurantIdAndAccountId(normalizedRestaurantId, accountId)
      .orElseGet(() -> RestaurantRating.builder()
          .id(UUID.randomUUID().toString())
          .restaurantId(normalizedRestaurantId)
          .accountId(accountId)
          .createdOn(now)
          .build());
  existing.setRating(rating);
  existing.setLastUpdatedOn(now);
  restaurantRatingRepository.save(existing);
  return toRatedDetail(restaurant);
}

public List<RestaurantDetail> getTopRatedRestaurants(int limit) {
  var pageSize = Math.max(1, Math.min(limit, 50));
  var summaries = Optional.ofNullable(restaurantRatingQueryRepository.topRated(pageSize))
      .orElseGet(List::of);
  var restaurantIds = summaries.stream().map(RestaurantRatingSummary::restaurantId).toList();
  var restaurantsById = new java.util.LinkedHashMap<String, Restaurant>();
  restaurantRepository.findAllById(restaurantIds)
      .forEach(restaurant -> restaurantsById.put(restaurant.getId(), restaurant));
  return toRatedDetails(restaurantIds.stream().map(restaurantsById::get)
      .filter(Objects::nonNull).toList());
}
```

Proposed:
```java
public RestaurantDetail voteRestaurant(String restaurantId, RestaurantVoteRequest request)
    throws InvalidRequestException {
  String id = validateRestaurantId(restaurantId);
  RestaurantVoteValue vote = validateVote(request == null ? null : request.vote());
  Restaurant restaurant = restaurantRepository.findById(id)
      .orElseThrow(() -> new ResourceNotFoundException("Restaurant not found"));
  String accountId = permissionService.getSelfId();
  RestaurantVote existing = restaurantVoteRepository
      .findByRestaurantIdAndAccountId(id, accountId)
      .orElseGet(() -> RestaurantVote.builder()
          .restaurantId(id).accountId(accountId).createdOn(Instant.now()).build());
  existing.setVote(vote);
  existing.setLastUpdatedOn(Instant.now());
  restaurantVoteRepository.save(existing);
  return enrichRestaurantDetails(List.of(restaurantMapper.toDetail(restaurant)), accountId).getFirst();
}

public List<RestaurantDetail> getTopLikedRestaurants(Integer limit) {
  int pageSize = Math.max(1, Math.min(limit == null ? 10 : limit, 50));
  List<RestaurantVoteSummary> summaries = restaurantVoteQueryRepository.topLiked(pageSize);
  List<String> restaurantIds = summaries.stream().map(RestaurantVoteSummary::restaurantId).toList();
  var restaurantsById = new LinkedHashMap<String, Restaurant>();
  restaurantRepository.findAllById(restaurantIds)
      .forEach(restaurant -> restaurantsById.put(restaurant.getId(), restaurant));
  return toRatedDetails(restaurantIds.stream().map(restaurantsById::get)
      .filter(Objects::nonNull).toList());
}

private RestaurantVoteValue validateVote(Object requestedVote) throws InvalidRequestException {
  if (!(requestedVote instanceof String value)) {
    throw new InvalidRequestException("Restaurant vote must be UP or DOWN.");
  }
  try {
    return RestaurantVoteValue.valueOf(value);
  } catch (IllegalArgumentException failure) {
    throw new InvalidRequestException("Restaurant vote must be UP or DOWN.");
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*RestaurantServiceTest" --no-daemon`

#### Code Edit 3.6
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 1056-1134
- Action: replace

Current:
```java
detail.setRatingCount(restaurantRatings.size());
detail.setRatingSum(restaurantRatings.stream().map(RestaurantRating::getRating).mapToInt(Integer::intValue).sum());
if (selfId != null) {
  restaurantRatings.stream()
      .filter(rating -> selfId.equals(rating.getAccountId()))
      .findFirst()
      .map(RestaurantRating::getRating)
      .ifPresent(detail::setMyRating);
}
Map<String, RestaurantRatingSummary> summariesByRestaurantId =
    restaurantRatingQueryRepository.summariesForRestaurants(candidateIds).stream()
        .collect(Collectors.toUnmodifiableMap(
            RestaurantRatingSummary::restaurantId,
            Function.identity()));
```

Proposed:
```java
int upVotes = (int) restaurantVotes.stream()
    .filter(vote -> vote.getVote() == RestaurantVoteValue.UP).count();
int downVotes = (int) restaurantVotes.stream()
    .filter(vote -> vote.getVote() == RestaurantVoteValue.DOWN).count();
detail.setUpVotes(upVotes);
detail.setDownVotes(downVotes);
detail.setVoteCount(upVotes + downVotes);
detail.setMyVote(restaurantVotes.stream()
    .filter(vote -> selfId.equals(vote.getAccountId()))
    .map(RestaurantVote::getVote).findFirst().orElse(null));

Map<String, RestaurantVoteSummary> summariesByRestaurantId =
    restaurantVoteQueryRepository.summariesForRestaurants(candidateIds).stream()
        .collect(Collectors.toUnmodifiableMap(RestaurantVoteSummary::restaurantId, Function.identity()));
return restaurantSelector.select(candidates, summariesByRestaurantId, requestedCount);
```

Verification:
- Daily pick tests assert the selector receives exact UP/DOWN summaries and candidate order remains stable.

#### Code Edit 3.7
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantController.java`
- Lines: 247-347
- Action: replace

Current:
```java
@GetMapping(value = APIVersion.V20260517 + "/top-rated", produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Response<List<RestaurantDetail>>> getTopRatedRestaurants(
    @RequestParam(value = "limit", required = false, defaultValue = "10") int limit) {
  var response = restaurantService.getTopRatedRestaurants(limit);
  return new ResponseEntity<>(Response.<List<RestaurantDetail>>builder()
      .payload(response).success(true).build(), HttpStatus.OK);
}

@PutMapping(value = APIVersion.V20260517 + "/rating",
    consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
@PreAuthorize("isAuthenticated()")
public ResponseEntity<Response<RestaurantDetail>> rateRestaurant(
    @RequestBody RestaurantRatingSetRequest request) throws Exception {
  var response = restaurantService.rateRestaurant(
      request == null ? null : request.restaurantId(),
      new RestaurantRatingRequest(request == null ? null : request.rating()));
  return new ResponseEntity<>(Response.<RestaurantDetail>builder()
      .payload(response).success(true).build(), HttpStatus.OK);
}
```

Proposed:
```java
@GetMapping(value = APIVersion.V20260517 + "/top-liked", produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Response<List<RestaurantDetail>>> getTopLikedRestaurants(
    @RequestParam(required = false) Integer limit) {
  return ResponseEntity.ok(Response.<List<RestaurantDetail>>builder()
      .payload(restaurantService.getTopLikedRestaurants(limit)).build());
}

@PutMapping(value = APIVersion.V20260517 + "/vote",
    consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
@PreAuthorize("isAuthenticated()")
public ResponseEntity<Response<RestaurantDetail>> voteRestaurant(
    @RequestBody RestaurantVoteSetRequest request) throws InvalidRequestException {
  RestaurantDetail detail = restaurantService.voteRestaurant(
      request == null ? null : request.restaurantId(),
      new RestaurantVoteRequest(request == null ? null : request.vote()));
  return ResponseEntity.ok(Response.<RestaurantDetail>builder().payload(detail).build());
}
```

Verification:
- Old `/rating` and `/top-rated` API routes return 404; numeric/invalid values at `/vote` return 400; valid authenticated values return 200.

#### Code Edit 3.8
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WhatsForLunchSessionService.java`
- Lines: 372-398
- Action: replace

Current:
```java
var ratingsByRestaurantId = restaurantRatingRepository.findByRestaurantIdIn(restaurantIds)
    .stream().collect(groupingBy(RestaurantRating::getRestaurantId));
detail.setRatingCount(ratings.size());
detail.setRatingSum(ratings.stream()
    .map(RestaurantRating::getRating)
    .filter(Objects::nonNull)
    .mapToInt(Integer::intValue)
    .sum());
ratings.stream()
    .filter(rating -> selfId.equals(rating.getAccountId()))
    .findFirst()
    .map(RestaurantRating::getRating)
    .ifPresent(detail::setMyRating);
```

Proposed:
```java
var votesByRestaurantId = restaurantVoteRepository.findByRestaurantIdIn(restaurantIds)
    .stream().collect(groupingBy(RestaurantVote::getRestaurantId));
var votes = votesByRestaurantId.getOrDefault(detail.getId(), List.of());
int up = (int) votes.stream().filter(v -> v.getVote() == RestaurantVoteValue.UP).count();
int down = (int) votes.stream().filter(v -> v.getVote() == RestaurantVoteValue.DOWN).count();
detail.setUpVotes(up);
detail.setDownVotes(down);
detail.setVoteCount(up + down);
detail.setMyVote(votes.stream().filter(v -> selfId.equals(v.getAccountId()))
    .map(RestaurantVote::getVote).findFirst().orElse(null));
```

Verification:
- `./gradlew.bat :website:test --tests "*WhatsForLunchSessionServiceTest" --no-daemon`

#### Code Edit 3.9
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WhatsForLunchSessionService.java`
- Lines: 18-55
- Action: replace

Current:
```java
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantRating;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingRepository;
private final RestaurantRatingRepository restaurantRatingRepository;
```

Proposed:
```java
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantVote;
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantVoteValue;
import dev.christopherbell.whatsforlunch.restaurant.vote.RestaurantVoteRepository;
private final RestaurantVoteRepository restaurantVoteRepository;
```

Verification:
- Session service and constructor-based tests compile without rating-domain types.

- [x] Write failing service/controller/session/security tests for the new contract.
- [x] Run focused tests and capture old rating API/field failures.
- [x] Implement vote enrichment, writes, Top 10 Liked, and both selector integrations.
- [x] Run focused tests to GREEN and confirm old routes are absent.
- [x] Commit with `Expose binary WFL vote contracts`.

### Task 4 - Update server-rendered profiles, structured data, routes, sitemap, and security

Sequence / dependencies:
- Runs after Task 3 because SSR consumes the new `RestaurantDetail` vote fields and the new API/page names.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: profiles render approval/counts and percentage JSON-LD; `/wfl/top-liked` is canonical; `/wfl/top-rated` permanently redirects.
  - Invariants: one canonical, valid-profile indexability, missing-profile 404 noindex/no JSON-LD, no personal/audit exposure, public API/page allowlists.
  - Boundary/API: immutable `RestaurantProfilePage.VoteSummary`; JSON-LD scale 0–100; public sitemap contains only canonical Top 10 Liked URL.
  - Effects and failures: page reads only; invalid vote counts omit aggregateRating; redirect has explicit permanent status and Location.
  - Tests and evidence: raw MockMvc/profile service tests fail on rating text then pass exact HTML, JSON-LD, routes, redirects, and security.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePage.java`
- Lines: 1-111
- Action: replace

Current:
```java
Rating rating,
public boolean hasRating() { return rating != null; }
public double averageRating() { return rating == null ? 0.0 : rating.average(); }
public record Rating(int count, int sum) {
  public Rating {
    if (count <= 0 || sum < count || sum > count * 5) {
      throw new IllegalArgumentException("Restaurant rating summary is invalid.");
    }
  }
  public double average() { return (double) sum / count; }
}
```

Proposed:
```java
VoteSummary votes,
public boolean hasVotes() { return votes != null; }
public int approvalPercentage() { return votes == null ? 0 : votes.approvalPercentage(); }

public record VoteSummary(int upVotes, int downVotes, int voteCount) {
  public VoteSummary {
    if (upVotes < 0 || downVotes < 0 || voteCount <= 0 || upVotes + downVotes != voteCount) {
      throw new IllegalArgumentException("Restaurant vote summary is invalid.");
    }
  }
  public int approvalPercentage() {
    return (int) Math.round(upVotes * 100.0 / voteCount);
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests "*RestaurantProfilePageServiceTest" --no-daemon`

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePageService.java`
- Lines: 47-72
- Action: replace

Current:
```java
var rating = publicRating(detail.getRatingCount(), detail.getRatingSum());
var description = hero + ". Details and ratings from What's For Lunch.";
```

Proposed:
```java
var votes = publicVotes(detail.getUpVotes(), detail.getDownVotes(), detail.getVoteCount());
var description = hero + ". Details and member approval from What's For Lunch.";

private static RestaurantProfilePage.VoteSummary publicVotes(
    Integer upVotes,
    Integer downVotes,
    Integer voteCount
) {
  int up = upVotes == null ? 0 : upVotes;
  int down = downVotes == null ? 0 : downVotes;
  int count = voteCount == null ? 0 : voteCount;
  if (up == 0 && down == 0 && count == 0) return null;
  return new RestaurantProfilePage.VoteSummary(up, down, count);
}
```

Verification:
- Complete, zero-vote, and malformed-count cases produce expected immutable pages.

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePageService.java`
- Lines: 136-170
- Action: replace

Current:
```java
if (rating != null) {
  restaurant.put("aggregateRating", orderedMap(
      "@type", "AggregateRating",
      "ratingValue", rating.average(),
      "ratingCount", rating.count()));
}
```

Proposed:
```java
if (votes != null) {
  restaurant.put("aggregateRating", orderedMap(
      "@type", "AggregateRating",
      "ratingValue", votes.approvalPercentage(),
      "bestRating", 100,
      "worstRating", 0,
      "ratingCount", votes.voteCount()));
}
```

Verification:
- Parse JSON-LD and assert exact numeric values and omission for zero votes.

#### Code Edit 4.4
- File: `website/src/main/resources/templates/restaurant.html`
- Lines: 23-48
- Action: replace

Current:
```html
<a href="/wfl/top-rated">Top 10 Rated</a>
<h2 id="restaurantRatingTitle">Aggregate rating</h2>
<p>4.5/5 from 2 ratings</p>
```

Proposed:
```html
<a href="/wfl/top-liked">Top 10 Liked</a>
<section class="restaurant-vote-signal" aria-labelledby="restaurantVoteTitle">
  <h2 id="restaurantVoteTitle">Member approval</h2>
  <p id="restaurant-public-votes" class="restaurant-vote-value"
     th:if="${restaurantProfile.hasVotes()}"
     th:text="${restaurantProfile.approvalPercentage() + '% liked · '
         + restaurantProfile.votes.upVotes + ' up · '
         + restaurantProfile.votes.downVotes + ' down'}">83% liked · 10 up · 2 down</p>
  <p id="restaurant-public-votes" class="restaurant-vote-value"
     th:unless="${restaurantProfile.hasVotes()}">No votes yet</p>
</section>
```

Verification:
- Raw HTML contains no star-scale phrases or private `myVote` value.

#### Code Edit 4.5
- File: `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- Lines: 49-59
- Action: replace

Current:
```java
@GetMapping("/wfl/top-rated")
public String topRated(Model model) {
  model.addAttribute("socialTitle", "CB | Top Rated Restaurants");
  model.addAttribute("socialUrl", PUBLIC_ROOT + "/wfl/top-rated");
  model.addAttribute("listMode", "top-rated");
  model.addAttribute("listTitle", "Top 10 Rated Restaurants");
  model.addAttribute("listDescription", "The highest rated restaurants from What's For Lunch.");
  return "wfl-list.html";
}
```

Proposed:
```java
@GetMapping("/wfl/top-liked")
public String topLiked(Model model) {
  model.addAttribute("socialTitle", "CB | Top 10 Liked Restaurants");
  model.addAttribute("socialUrl", PUBLIC_ROOT + "/wfl/top-liked");
  model.addAttribute("listMode", "top-liked");
  model.addAttribute("listTitle", "Top 10 Liked Restaurants");
  model.addAttribute("listDescription", "The restaurants with the highest member approval from What's For Lunch.");
  return "wfl-list.html";
}

@GetMapping("/wfl/top-rated")
public ResponseEntity<Void> legacyTopRated() {
  return ResponseEntity.status(HttpStatus.PERMANENT_REDIRECT)
      .location(URI.create("/wfl/top-liked")).build();
}
```

Verification:
- `/wfl/top-liked` returns 200/canonical mount; `/wfl/top-rated` returns 308 and exact Location.

#### Code Edit 4.6
- File: `website/src/main/java/dev/christopherbell/configuration/PublicSitemapService.java`
- Lines: 34-45
- Action: replace

Current:
```java
PUBLIC_ROOT + "/wfl/top-rated",
```

Proposed:
```java
PUBLIC_ROOT + "/wfl/top-liked",
```

Verification:
- Sitemap contains Top 10 Liked once and excludes Top 10 Rated.

#### Code Edit 4.7
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 110-158
- Action: replace

Current:
```java
"GET:/api/whatsforlunch/restaurant" + APIVersion.V20260517 + "/top-rated",
"/wfl/top-rated",
```

Proposed:
```java
"GET:/api/whatsforlunch/restaurant" + APIVersion.V20260517 + "/top-liked",
"/wfl/top-liked",
"/wfl/top-rated",
```

Verification:
- Anonymous GETs to canonical API/page and legacy redirect pass; vote PUT still requires USER.

- [x] Add failing profile, route, redirect, sitemap, and security tests.
- [x] Run focused view/config tests to RED.
- [x] Implement vote SSR/JSON-LD and canonical route/security changes.
- [x] Run focused tests to GREEN and parse JSON-LD.
- [x] Commit with `Render WFL thumb approval publicly`.

### Task 5 - Replace star UI with accessible thumb controls on every WFL surface

Sequence / dependencies:
- Runs after Task 4 because browser code targets final vote JSON fields, endpoints, mount IDs, and canonical list mode.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: shared format returns percentage/counts; logged-in controls send UP/DOWN and update state; anonymous profiles make no personal fetch.
  - Invariants: text sanitization, cookie/CSRF helper use, scoped Void CSS, visible focus, local error ownership, Favorites behavior.
  - Boundary/API: `voteSummary()` returns frozen `{upVotes, downVotes, voteCount, myVote, approvalPercentage, overall}`; `data-vote` is UP/DOWN.
  - Effects and failures: one fetch per member action, no optimistic public mutation before response, button busy state restored on error.
  - Tests and evidence: Node tests fail on rating helpers/markup, then pass summaries, navigation, payloads, aria state, stale-session, and failure isolation.

#### Code Edit 5.1
- File: `website/src/main/resources/static/js/lib/wfl-ui.js`
- Lines: 1-51
- Action: replace

Current:
```javascript
{ key: 'top-rated', href: '/wfl/top-rated', label: 'Top 10 Rated' }
export function ratingSummary(restaurant = {}) {
  const sum = Number.parseInt(String(restaurant.ratingSum ?? 0), 10) || 0;
  const count = Number.parseInt(String(restaurant.ratingCount ?? 0), 10) || 0;
  return Object.freeze({ count, myRating, overall: count > 0 ? `${Math.round(sum / count)}/5` : 'No Ratings' });
}
```

Proposed:
```javascript
{ key: 'top-liked', href: '/wfl/top-liked', label: 'Top 10 Liked' }
export function voteSummary(restaurant = {}) {
  const upVotes = Number.parseInt(String(restaurant.upVotes ?? 0), 10) || 0;
  const downVotes = Number.parseInt(String(restaurant.downVotes ?? 0), 10) || 0;
  const voteCount = Number.parseInt(String(restaurant.voteCount ?? 0), 10) || 0;
  const myVote = ['UP', 'DOWN'].includes(restaurant.myVote) ? restaurant.myVote : null;
  const approvalPercentage = voteCount > 0 ? Math.round(upVotes * 100 / voteCount) : null;
  return Object.freeze({
    upVotes,
    downVotes,
    voteCount,
    myVote,
    approvalPercentage,
    overall: voteCount > 0
      ? `${approvalPercentage}% liked · ${upVotes} up · ${downVotes} down`
      : 'No votes yet',
  });
}
```

Verification:
- `./gradlew.bat :website:jsTest --no-daemon`

#### Code Edit 5.2
- File: `website/src/main/resources/static/js/lib/api.js`
- Lines: 276-285
- Action: replace

Current:
```javascript
rateRestaurant: '/api/whatsforlunch/restaurant/2026-05-17/rating',
topRated: (limit = 10) => `/api/whatsforlunch/restaurant/2026-05-17/top-rated?limit=${encodeURIComponent(limit)}`,
```

Proposed:
```javascript
voteRestaurant: '/api/whatsforlunch/restaurant/2026-05-17/vote',
topLiked: (limit = 10) => `/api/whatsforlunch/restaurant/2026-05-17/top-liked?limit=${encodeURIComponent(limit)}`,
```

Verification:
- Static API contract test contains no rating write/top-rated API route.

#### Code Edit 5.3
- File: `website/src/main/resources/static/js/restaurant-profile.js`
- Lines: 1-138
- Action: replace

Current:
```javascript
const RATING_OPTIONS = Object.freeze([1, 2, 3, 4, 5]);
const rating = Number.parseInt(String(ratingButton.dataset.rating), 10);
await request(API.whatsForLunch.rateRestaurant, {
  method: 'PUT',
  headers: headers(),
  body: JSON.stringify({ restaurantId: state.restaurant.id, rating }),
});
```

Proposed:
```javascript
const VOTE_OPTIONS = Object.freeze([
  Object.freeze({ value: 'UP', label: 'Thumbs up', glyph: '👍' }),
  Object.freeze({ value: 'DOWN', label: 'Thumbs down', glyph: '👎' }),
]);

function memberMarkup(restaurant) {
  return `<p>Your vote: ${restaurant.myVote === 'UP' ? 'Thumbs up'
      : restaurant.myVote === 'DOWN' ? 'Thumbs down' : 'Not voted'}</p>
    <div class="lunch-vote-control" role="group" aria-label="Vote on ${sanitize(restaurant.name)}">
      ${VOTE_OPTIONS.map(option => `<button type="button" class="lunch-vote-button"
        data-vote="${option.value}" aria-label="${option.label}"
        aria-pressed="${restaurant.myVote === option.value}">${option.glyph}</button>`).join('')}
    </div>`;
}

async function saveVote(restaurantId, vote, request, headers) {
  if (!VOTE_OPTIONS.some(option => option.value === vote)) return null;
  return request(API.whatsForLunch.voteRestaurant, {
    method: 'PUT',
    headers: headers(),
    body: JSON.stringify({ restaurantId, vote }),
  });
}

const value = await saveVote(state.restaurant.id, vote, request, headers);
state.restaurant = memberRestaurant(value, state.restaurant.id);
publicMount.textContent = voteSummary(state.restaurant).overall;
mount.innerHTML = memberMarkup(state.restaurant);
```

Verification:
- Existing six profile tests are rewritten for UP/DOWN and extended for idempotent active vote and numeric-payload absence.

#### Code Edit 5.4
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 161-241
- Action: replace

Current:
```javascript
const ratingControls = isLoggedIn && id
  ? `<div class="lunch-rating-control" aria-label="Rate ${sanitize(restaurant.name || 'restaurant')}">
      ${RATING_OPTIONS.map((rating) => `<button class="lunch-rating-button"
        data-restaurant-id="${sanitize(id)}" data-rating="${rating}"
        aria-label="Rate ${rating} out of 5">${rating}</button>`).join('')}
    </div>`
  : '';
```

Proposed:
```javascript
const { myVote, overall } = voteSummary(restaurant);
const voteControls = isLoggedIn && id ? `<div class="lunch-vote-control" role="group"
    aria-label="Vote on ${sanitize(restaurant.name || 'restaurant')}">
  <button type="button" class="lunch-vote-button" data-restaurant-id="${sanitize(id)}"
    data-vote="UP" aria-label="Thumbs up" aria-pressed="${myVote === 'UP'}">👍</button>
  <button type="button" class="lunch-vote-button" data-restaurant-id="${sanitize(id)}"
    data-vote="DOWN" aria-label="Thumbs down" aria-pressed="${myVote === 'DOWN'}">👎</button>
</div>` : '';
const voteSummaryMarkup = `<p class="lunch-vote-summary">${overall}</p>`;
```

Verification:
- Picks and shared-session cards render two controls and send only string vote values.

#### Code Edit 5.5
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 897-1036
- Action: replace

Current:
```javascript
const ratingButton = event.target instanceof Element
  ? event.target.closest('.lunch-rating-button') : null;
if (ratingButton) {
  await rateRestaurant(ratingButton.dataset.restaurantId, ratingButton.dataset.rating);
  return;
}

async function rateRestaurant(restaurantId, rating) {
  const selectedRating = Number.parseInt(String(rating), 10);
  if (!restaurantId || !RATING_OPTIONS.includes(selectedRating)) return;
  const updatedRestaurant = await fetchJson(API.whatsForLunch.rateRestaurant, {
    method: 'PUT',
    headers: authHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ restaurantId, rating: selectedRating }),
  });
  currentPicks = currentPicks.map((restaurant) =>
    restaurant.id === restaurantId ? updatedRestaurant : restaurant);
  renderPicks(currentPicks);
}
```

Proposed:
```javascript
const restaurantVoteButton = event.target instanceof Element
  ? event.target.closest('.lunch-vote-button') : null;
if (restaurantVoteButton) {
  await setRestaurantVote(
      restaurantVoteButton.dataset.restaurantId,
      restaurantVoteButton.dataset.vote);
  return;
}

async function setRestaurantVote(restaurantId, vote) {
  if (!restaurantId || !['UP', 'DOWN'].includes(vote)) return;
  const button = Array.from(mount.querySelectorAll('.lunch-vote-button'))
    .find(candidate => candidate.dataset.restaurantId === restaurantId
      && candidate.dataset.vote === vote);
  if (button) button.disabled = true;
  try {
    const updatedRestaurant = await fetchJson(API.whatsForLunch.voteRestaurant, {
      method: 'PUT',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ restaurantId, vote }),
    });
    currentPicks = currentPicks.map(restaurant =>
      restaurant.id === restaurantId ? updatedRestaurant : restaurant);
    if (activeSession?.restaurants) {
      activeSession = {...activeSession, restaurants: activeSession.restaurants.map(restaurant =>
        restaurant.id === restaurantId ? updatedRestaurant : restaurant)};
    }
    renderPicks(currentPicks);
  } catch (error) {
    mount.insertAdjacentHTML('afterbegin', `<div class="alert alert-danger" role="alert">${
      sanitize(error.message || 'Could not save vote.')
    }</div>`);
  } finally {
    if (button) button.disabled = false;
  }
}
```

Verification:
- Node/static tests prove there is no numeric parse, `data-rating`, rating toggle, or rating endpoint in the picks mutation path.

#### Code Edit 5.6
- File: `website/src/main/resources/static/js/wfl-list.js`
- Lines: 1-130
- Action: replace

Current:
```javascript
const mode = mount?.dataset.listMode || 'top-rated';
const endpoint = mode === 'favorites'
  ? API.whatsForLunch.favorites
  : API.whatsForLunch.topRated(10);
const description = mode === 'favorites'
  ? 'Restaurants you saved for later.'
  : 'The highest-rated WFL restaurants with at least one member rating.';
```

Proposed:
```javascript
const mode = mount?.dataset.listMode || 'top-liked';
const endpoint = mode === 'favorites'
  ? API.whatsForLunch.favorites
  : API.whatsForLunch.topLiked(10);
const heading = mode === 'favorites' ? 'Favorite Restaurants' : 'Top 10 Liked';
const description = mode === 'favorites'
  ? 'Restaurants you saved for later.'
  : 'WFL restaurants with the highest member approval.';
const summary = voteSummary(restaurant);
const summaryMarkup = `<p class="lunch-vote-summary">${summary.overall}</p>`;
```

Verification:
- Top 10 Liked and Favorites tests prove correct endpoint/copy and personal-vote rendering.

#### Code Edit 5.7
- File: `website/src/main/resources/static/css/whats-for-lunch.css`
- Lines: 235-253
- Action: replace

Current:
```css
.lunch-void-page p.lunch-rating-summary,
.lunch-void-page .lunch-rating-summary p {
    color: var(--lunch-void-teal);
}
.lunch-void-page .lunch-rating-button {
    border-color: var(--lunch-void-line);
    background: #080e14;
    color: var(--lunch-void-text);
}
.lunch-void-page .lunch-rating-button:hover,
.lunch-void-page .lunch-rating-button:focus-visible,
.lunch-void-page .lunch-rating-button.active,
.lunch-void-page .btn-primary {
    border-color: var(--lunch-void-teal);
    background: var(--lunch-void-teal);
}
```

Proposed:
```css
.lunch-void-page p.lunch-vote-summary,
.lunch-void-page .lunch-vote-summary p { color: var(--lunch-void-teal); }
.lunch-void-page .lunch-vote-control { display: flex; gap: .65rem; flex-wrap: wrap; }
.lunch-void-page .lunch-vote-button {
  min-width: 3rem; min-height: 2.75rem; border: 1px solid var(--lunch-void-line);
  background: transparent; color: var(--lunch-void-text); border-radius: .35rem;
}
.lunch-void-page .lunch-vote-button:hover,
.lunch-void-page .lunch-vote-button:focus-visible,
.lunch-void-page .lunch-vote-button[aria-pressed="true"] {
  border-color: var(--lunch-void-teal); color: var(--lunch-void-teal);
}
```

Verification:
- Static ownership/a11y tests and desktop/mobile computed layout show visible focus and no overflow.

#### Code Edit 5.8
- File: `website/src/main/resources/static/css/whats-for-lunch.css`
- Lines: 312-489
- Action: replace

Current:
```css
grid-template-areas: "rating details";
.lunch-void-page .restaurant-rating-signal { grid-area: rating; }
.lunch-void-page .restaurant-rating-value { font-family: var(--lunch-void-display); }
.lunch-void-page .restaurant-member-panel .lunch-rating-control { display: flex; }
```

Proposed:
```css
grid-template-areas: "votes details";
.lunch-void-page .restaurant-vote-signal { grid-area: votes; }
.lunch-void-page .restaurant-vote-value { font-family: var(--lunch-void-display); }
.lunch-void-page .restaurant-member-panel .lunch-vote-control {
  display: flex;
  gap: .65rem;
  flex-wrap: wrap;
}
@media (max-width: 767.98px) {
  .lunch-void-page .restaurant-profile-void {
    grid-template-areas: "votes" "details" "member";
  }
  .lunch-void-page .restaurant-vote-value { font-size: 1.625rem; }
}
```

Verification:
- Profile template selectors match the scoped stylesheet; desktop/mobile rating-wrap regression tests become vote-layout tests and pass.

#### Code Edit 5.9
- File: `website/src/test/js/wfl-ui.test.js`
- Lines: 1-64
- Action: replace

Current:
```javascript
assert.deepEqual(ratingSummary({ ratingSum: '9', ratingCount: '2', myRating: '4' }), {
  count: 2, myRating: 4, overall: '5/5'
});
```

Proposed:
```javascript
assert.deepEqual(voteSummary({ upVotes: '10', downVotes: '2', voteCount: '12', myVote: 'UP' }), {
  upVotes: 10, downVotes: 2, voteCount: 12, myVote: 'UP',
  approvalPercentage: 83, overall: '83% liked · 10 up · 2 down'
});
assert.equal(voteSummary({}).overall, 'No votes yet');
assert.match(wflSecondaryNavigation('top-liked'), /Top 10 Liked/);
assert.doesNotMatch(wflSecondaryNavigation('top-liked'), /Rated|top-rated/);
```

Verification:
- `./gradlew.bat :website:jsTest --rerun-tasks --no-daemon`

- [x] Add failing shared-summary, API, profile, picks, and list tests.
- [x] Run JS tests and record rating-contract failures.
- [x] Implement shared vote helpers, endpoints, controls, markup, and scoped CSS.
- [x] Run JS/static tests to GREEN plus `node --check` on touched modules.
- [x] Commit with `Replace WFL ratings with thumb controls`.

### Task 6 - Update documentation and complete full migrated-runtime delivery

Sequence / dependencies:
- Runs after Tasks 1–5 because documentation and acceptance evidence describe the final contract.

Implementation notes:
- Required skill: `write-chris-street-style-code` before documentation edits that contain executable API examples.
- Before-Edit Brief:
  - Behavior: repository docs describe only vote semantics, migration, Top 10 Liked, and smoothed approval weighting.
  - Invariants: no historical claims are rewritten; operational commands use isolated port/database and protected deployment.
  - Boundary/API: README examples use `/vote`, `/top-liked`, `UP`/`DOWN`, and vote response fields.
  - Effects and failures: docs only; runtime validation uses disposable data and cleans only exact candidate resources.
  - Tests and evidence: stale-language scan, full check, migrated fixture inspection, raw HTTP, browser, CI, and production evidence.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`
- Lines: 1-82
- Action: replace

Current:
```markdown
- Whole-number restaurant ratings from logged-in members, plus public rating totals.
- `PUT /api/whatsforlunch/restaurant/2026-05-17/rating` accepts `restaurantId` and `rating`.
- `/wfl/top-rated` lists the public top 10 rated restaurants.
```

Proposed:
```markdown
- Binary thumbs-up/thumbs-down restaurant votes from logged-in members, plus public approval totals.
- `PUT /api/whatsforlunch/restaurant/2026-05-17/vote` accepts `restaurantId` and `vote: "UP" | "DOWN"`.
- Public details expose `upVotes`, `downVotes`, and `voteCount`; signed-in details add `myVote`.
- `/wfl/top-liked` lists the public Top 10 Liked by approval percentage, vote count, and stable ID.
- V013 maps legacy 3–5 ratings to UP and 1–2 ratings to DOWN before vote-only code reads the collection.
```

Verification:
- Focused `rg` finds no current-contract star-scale wording outside V013 tests/history and the intentional `/wfl/top-rated` redirect.

#### Code Edit 6.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/vote/README.md`
- Lines: before 1
- Action: add

Proposed:
```markdown
# Restaurant vote persistence

Owns one `UP` or `DOWN` vote per account and restaurant in the retained
`whatsforlunch_ratings` collection. `RestaurantVoteQueryRepository` calculates
bounded public summaries and Top 10 Liked order inside MongoDB. V013 is the only
supported bridge from legacy numeric documents; runtime code does not dual-read.
```

Verification:
- Package/model/WFL README files agree on collection, fields, endpoints, ordering, and weighting.

- [x] Update WFL, model, vote, selection, view, JavaScript, and CSS ownership documentation.
- [x] Run `rg` stale-language scan and fix only active-contract occurrences.
- [x] Run focused Java and JS suites, then `:website:check --rerun-tasks` with private Gradle home.
- [x] Build the packaged JAR and start it on a free non-8080 port with a disposable Mongo database seeded with 1–5 ratings.
- [x] Verify V013 documents, migration record/checksum, unique index, up/down totals, Top 10 Liked ordering, selector inputs, old/new API behavior, profiles, JSON-LD, sitemap, redirect, liveness, and readiness.
- [x] Use browser automation for anonymous, signed-in UP, DOWN, change vote, same-vote idempotence, Favorites, Top 10 Liked, desktop, mobile, keyboard, and console checks.
- [x] Save and validate the Builder test report; commit/push that checkpoint.
- [x] Review the complete spoke diff with `write-chris-street-style-code` review rules; resolve all blockers/warnings.
- [x] Push `codex/wfl-thumbs-voting`, open a ready PR, wait for Linux/macOS/Windows, Dependency Review, and CodeQL, and fix in-scope failures.
- [x] Squash-merge only after all required checks pass and record the merged SHA.
- [x] Deploy the merged SHA through the protected Windows path; verify listener rotation, local/public health, versioned assets, live migrated vote data, API/UI/SEO behavior, Mongo/service state, and rollback absence.
- [x] Ingest/review/close Builder work, mark spec/plan complete, save session memory, update indexes, validate hub state, and commit/push Builder main.

Verification:
- Final production evidence contains exact URLs, request bodies/UI inputs, status codes/bodies, asset paths, listener PID, migration state, and service state.

## Code Changes

- Task 1: add `RestaurantVoteValue`, move rating entity/requests to vote names, add V013 and migration tests.
- Task 2: move rating repository/summary/query/selector to vote/approval names and update their focused tests.
- Task 3: replace service, controller, session, mapper, model, security, and associated Java tests with vote contracts.
- Task 4: replace profile rating projection/JSON-LD/template, Top 10 route/sitemap/security, and raw-view tests.
- Task 5: replace shared UI summary, API paths, profile/picks/list scripts, scoped CSS selectors, and Node/static tests.
- Task 6: update WFL/model/vote/selection/view/JS/CSS documentation and execute the delivery loop.

## Files and Modules

- Migration: `configuration/mongo/migration/V013ConvertRestaurantRatingsToVotes*`.
- Domain: `restaurant/model/RestaurantVote*`, `RestaurantVoteValue`, `RestaurantDetail`, mapper.
- Aggregation: focused `restaurant/vote` repository, summary, query repository, README.
- Selection: `ApprovalWeightedRestaurantSelector` and tests.
- Orchestration: `RestaurantService`, `RestaurantController`, `WhatsForLunchSessionService` and tests.
- SSR/SEO: `RestaurantProfilePage*`, `WhatsForLunchViewController`, `restaurant.html`, sitemap/security and tests.
- Browser: `wfl-ui.js`, `api.js`, `whats-for-lunch.js`, `restaurant-profile.js`, `wfl-list.js`, scoped CSS and JS tests.
- Documentation: WFL, model, vote, selection, view, JS, and CSS READMEs.

## Unit Testing

- Migration: exact conversion matrix, timestamp/identity preservation, retry, batch cursor, malformed, contradiction, no-write-on-preflight-failure.
- Repository: conditional counts, percentage projection, sort/tie/limit, requested-ID summaries.
- Selector: anchors, prior, monotonicity, invalid summary/random, deterministic sampling without replacement.
- Service/session: UP/DOWN create/change/idempotent, enrichment, privacy, Top 10 ordering, daily/shared selector integration.
- Controller/security: valid/invalid/numeric/null/auth/content-type/old-route contracts.
- SSR/config: approval formatting, JSON-LD 0–100, zero omission, privacy, 404 noindex, redirect, sitemap, public allowlists.
- JavaScript: summary rounding/zero, navigation, API constants, accessible two-button state, payloads, response refresh, local failures, anonymous zero-fetch.

## Local Testing

- Use private `GRADLE_USER_HOME=A:\Projects\christopherbell.dev-gradle-homes\wfl-thumbs-voting`.
- Seed a disposable database such as `christopherbell_dev_wfl_thumbs_voting` with legacy ratings 1–5, zero-vote restaurant, complete profile, malformed-request targets, and a test account.
- Start packaged merged-content candidate on a confirmed free port such as `8094`; never stop production 8080 before acceptance.
- Capture raw HTTP for liveness/readiness, `/vote`, removed `/rating`, `/top-liked`, profile, legacy page redirect, robots, sitemap, and missing profile.
- Inspect exact migrated documents and migration record in the disposable database, then drop only that database after testing.
- Browser-check desktop 1440×900 and mobile 390×844 plus keyboard focus and console.

## Validation

- `git diff --check` clean; only intentional files staged.
- Focused RED/GREEN evidence per task.
- Full `./gradlew.bat :website:check --rerun-tasks --no-daemon --console=plain` passes.
- Alternate-port migrated runtime and browser acceptance pass with no production listener impact.
- Test report quality validator and hub validator pass.
- PR required CI and CodeQL pass; PR is merged.
- Merged-SHA protected deployment and public/local production evidence pass.

## Rollback or Recovery

- Before merge, revert task commits or close the PR; never edit the dirty authoritative checkout.
- V013 is forward-only and must not be modified after applying. Production rollback may run the prior application against vote-shaped documents only if the deployment framework proves compatibility; therefore the guarded candidate must validate migration/application startup before listener switch.
- If V013 preflight fails, fix the exact malformed production documents through a separately reviewed repair path; do not weaken validation or mark the migration applied.
- If post-switch verification fails, rely on the protected deployment's automatic release rollback and preserve both deployment and rollback failures.
- Candidate databases/processes are disposable and must be stopped/dropped by exact name/PID only.

## Risks

- Forward-only schema breaks old binaries after migration. Mitigation: guarded build/candidate/startup order, no partial preflight mutation, and immediate complete rollout.
- Mongo conditional aggregation syntax could drift from intended ordering. Mitigation: pipeline JSON tests plus real disposable-database results.
- Approval percentage can favor one-UP restaurants on the leaderboard. This is an approved raw-percentage rule; total votes break equal percentages and the lunch selector separately uses smoothing.
- Cached numeric clients will fail. This is approved; versioned assets update atomically and failures are stable 404/400.
- Renames can leave stale star terminology or imports. Mitigation: scoped `rg` scans, compile failures, full tests, and documentation review.
- Thumb glyphs can be ambiguous to assistive technology. Mitigation: explicit accessible labels, `aria-pressed`, text summaries, and keyboard checks.

## Completion Criteria

- Spec requirements map to implemented tasks with no unresolved deviation.
- V013 converts all valid production legacy ratings and the live migration record/checksum is verified.
- No active WFL UI/API/domain path accepts or exposes 1–5 ratings.
- Top 10 Liked, public summaries, weighted selection, profile SSR/JSON-LD, and personal controls meet approved behavior.
- Focused/full/local/browser/CI/production checks pass and no required service is degraded.
- PR is merged, production serves merged behavior, Builder test/update/review/closure/session artifacts are indexed, validated, committed, and pushed.
