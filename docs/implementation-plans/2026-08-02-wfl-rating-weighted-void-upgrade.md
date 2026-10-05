# WFL Rating-Weighted Picks and Void Decision Console Implementation Plan

> **For agentic workers:** Execute this plan in order. Invoke every named skill at the stated boundary, preserve the authoritative dirty checkout, and record RED/GREEN evidence before each production behavior edit.

## Document Status

ready-for-execution

## Objective

Replace uniform random selection in every What's for Lunch three-pick flow with confidence-adjusted rating-weighted sampling without replacement, and relaunch `/wfl` as a compact Void-style decision console without changing the behavior or appearance of neighboring WFL list and restaurant-profile pages.

## Goals

- Give highly rated restaurants a moderately higher chance of appearing.
- Give poorly rated restaurants a lower chance of appearing while keeping every eligible restaurant possible.
- Treat unrated restaurants as a neutral 3-star baseline.
- Temper sparse ratings with three neutral virtual ratings before weighting.
- Apply the same selector to daily picks, nearby/ZIP picks, and deleted-pick replacement.
- Preserve already persisted daily picks and active shared-session picks in stored order.
- Query rating totals once per candidate batch rather than once per restaurant.
- Show three equal, non-ranked restaurant cards in a responsive Void decision console.
- Preserve filters, geolocation, ZIP lookup, sessions, voting, rating, favorites, safe links, deletion, loading, empty, error, keyboard, and assistive-technology behavior.
- Verify on an unused non-8080 port before any production listener change.

## Inputs

- Approved specification: `docs/specs/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md`
- Builder work ledger: `docs/work/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md`
- Spoke repository: `A:\Projects\christopherbell.dev`
- Current reviewed base: `origin/main` at `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`
- User decisions:
  - Three neutral virtual ratings.
  - Adjusted rating: `(ratingSum + 3.0 * 3) / (ratingCount + 3)`.
  - Moderate piecewise-linear weights: 1 star `0.35`, 2 star `0.60`, 3 star `1.00`, 4 star `1.50`, 5 star `2.00`.
  - Weighted sampling without replacement.
  - Visual direction B, "Decision Console."
  - Equal cards with no rank implication.

## Branch

- Base: freshly fetched `origin/main`.
- Branch: `codex/wfl-rating-weighted-void`.
- Worktree: create an isolated worktree with `superpowers:using-git-worktrees`; do not edit or clean the authoritative checkout at `A:\Projects\christopherbell.dev`.

## Non-Goals

- Re-ranking Top 10 Rated or Favorites.
- Recomputing stored daily picks when they are read.
- Replacing active shared-session picks unless the existing host action requests new picks.
- Changing rating submission semantics, restaurant eligibility, supported metros, distance calculations, cuisine filters, or locality-integrity rules.
- Adding a database collection, persisted weight, cache, migration, or external recommendation service.
- Restyling `/wfl/top-rated`, `/wfl/favorites`, or `/wfl/restaurants/{id}`.
- Touching the production listener before alternate-port acceptance passes.

## Assumptions

- Candidate restaurants have stable non-blank IDs; duplicate or malformed IDs are programmer/data-integrity failures.
- Mongo rating aggregates contain a positive count and a sum between `count` and `5 * count`; malformed data must not silently become neutral.
- The daily scheduler remains protected by the existing collector lease.
- Existing WFL API response shapes remain unchanged.
- Node's built-in runner and Gradle `jsTest` remain the frontend test boundary.
- Shared WFL rules in `main.css` remain the owner for list/profile pages; `/wfl`-only Void rules belong in a dedicated stylesheet.

## Open Questions

None.

## Task Breakdown

### Task 0 - Establish the isolated execution baseline

Sequence / dependencies:

- Run first; no production files change.

Implementation notes:

- Invoke `superpowers:using-git-worktrees`.
- Fetch `origin`, confirm the reviewed base has not drifted incompatibly, create `codex/wfl-rating-weighted-void`, and verify the worktree with `Test-Path`, `git rev-parse --show-toplevel`, and `git status --short --branch`.
- Record clean focused baselines:
  - `.\gradlew.bat :website:test --tests "*RestaurantRatingQueryRepositoryTest" --tests "*RestaurantServiceTest"`
  - `.\gradlew.bat :website:jsTest`
- If the base changed materially around the line ranges below, update and revalidate this plan before editing.

Verification:

- The isolated worktree is on the planned branch, the authoritative checkout is untouched, and focused baselines pass.

### Task 1 - Add the pure confidence-adjusted weighted selector

Sequence / dependencies:

- Runs after Task 0 and creates the deterministic domain boundary used by Task 3.

Implementation notes:

- Required skill: `chris-street-style` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: select up to the requested number of unique restaurants using the approved confidence-adjusted weights.
  - Invariants: IDs are non-blank and unique; count is non-negative; summaries have valid ranges; random samples are finite in `[0, 1)`; inputs are not mutated; every candidate remains possible.
  - Boundary/API: a Spring component accepts candidates, summaries, and count; a package-private overload accepts `DoubleSupplier`.
  - Effects and failures: the public entry point owns thread-local randomness; the core is local/pure; malformed trusted inputs throw `IllegalArgumentException`.
  - Tests and evidence: add selector tests first, observe missing-class RED, then implement and retain exact formula/interpolation, deterministic draw, invariant, and fixed-seed distribution evidence.

#### Code Edit 1.1

- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/selection/RatingWeightedRestaurantSelectorTest.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.whatsforlunch.restaurant.selection;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.within;

import dev.christopherbell.whatsforlunch.restaurant.model.Restaurant;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingSummary;
import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("Rating-weighted restaurant selector")
class RatingWeightedRestaurantSelectorTest {
  private final RatingWeightedRestaurantSelector selector =
      new RatingWeightedRestaurantSelector();

  @Test
  void unratedRestaurantsUseTheNeutralWeight() {
    assertThat(RatingWeightedRestaurantSelector.weightFor(null)).isEqualTo(1.0);
  }

  @Test
  void oneFiveStarRatingBlendsWithThreeNeutralRatings() {
    var summary = new RestaurantRatingSummary("sparse", 1, 5);
    assertThat(RatingWeightedRestaurantSelector.weightFor(summary))
        .isCloseTo(1.25, within(0.000_000_001));
  }

  @Test
  void adjustedRatingWeightsInterpolateBetweenApprovedAnchors() {
    assertThat(RatingWeightedRestaurantSelector.interpolateWeight(1.0)).isEqualTo(0.35);
    assertThat(RatingWeightedRestaurantSelector.interpolateWeight(1.5)).isEqualTo(0.475);
    assertThat(RatingWeightedRestaurantSelector.interpolateWeight(2.5)).isEqualTo(0.80);
    assertThat(RatingWeightedRestaurantSelector.interpolateWeight(3.5)).isEqualTo(1.25);
    assertThat(RatingWeightedRestaurantSelector.interpolateWeight(4.5)).isEqualTo(1.75);
    assertThat(RatingWeightedRestaurantSelector.interpolateWeight(5.0)).isEqualTo(2.0);
  }

  @Test
  void deterministicDrawSelectsWithoutReplacementAndPreservesInput() {
    var first = restaurant("first");
    var second = restaurant("second");
    var third = restaurant("third");
    var candidates = List.of(first, second, third);
    var samples = new ArrayDeque<>(List.of(0.75, 0.25));

    var selected = selector.select(
        candidates, Map.of(), 2, () -> samples.removeFirst());

    assertThat(selected).containsExactly(third, first);
    assertThat(selected).doesNotHaveDuplicates();
    assertThat(candidates).containsExactly(first, second, third);
  }

  @Test
  void rejectsDuplicateCandidateIds() {
    assertThatThrownBy(() -> selector.select(
        List.of(restaurant("same"), restaurant("same")),
        Map.of(), 1, () -> 0.5))
        .isInstanceOf(IllegalArgumentException.class);
  }

  @Test
  void rejectsMalformedRatingSummary() {
    var candidate = restaurant("broken");
    var malformed = new RestaurantRatingSummary("broken", 2, 11);
    assertThatThrownBy(() -> selector.select(
        List.of(candidate), Map.of("broken", malformed), 1, () -> 0.5))
        .isInstanceOf(IllegalArgumentException.class);
  }

  @Test
  void fixedSeedDrawFavorsHighThenNeutralThenLowRatings() {
    var low = restaurant("low");
    var neutral = restaurant("neutral");
    var high = restaurant("high");
    var summaries = Map.of(
        "low", new RestaurantRatingSummary("low", 1_000, 1_000),
        "high", new RestaurantRatingSummary("high", 1_000, 5_000));
    var counts = new HashMap<String, Integer>();
    var random = new Random(20_260_802L);

    for (int draw = 0; draw < 20_000; draw++) {
      var selected = selector.select(
          List.of(low, neutral, high), summaries, 1, random::nextDouble);
      counts.merge(selected.getFirst().getId(), 1, Integer::sum);
    }

    int lowCount = counts.getOrDefault("low", 0);
    int neutralCount = counts.getOrDefault("neutral", 0);
    int highCount = counts.getOrDefault("high", 0);
    assertThat(highCount).isGreaterThan(neutralCount);
    assertThat(neutralCount).isGreaterThan(lowCount);
    assertThat((double) highCount / neutralCount).isBetween(1.8, 2.2);
    assertThat((double) lowCount / neutralCount).isBetween(0.30, 0.40);
  }

  private static Restaurant restaurant(String id) {
    return Restaurant.builder().id(id).name(id).build();
  }
}
```

Verification:

- RED: `.\gradlew.bat :website:test --tests "*RatingWeightedRestaurantSelectorTest"` fails because the selector is absent.

#### Code Edit 1.2

- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/selection/RatingWeightedRestaurantSelector.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.whatsforlunch.restaurant.selection;

import dev.christopherbell.whatsforlunch.restaurant.model.Restaurant;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingSummary;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.DoubleSupplier;
import org.springframework.stereotype.Component;

@Component
public final class RatingWeightedRestaurantSelector {
  private static final double PRIOR_RATING = 3.0;
  private static final int PRIOR_RATING_COUNT = 3;
  private static final double[] RATING_WEIGHTS = {0.35, 0.60, 1.00, 1.50, 2.00};

  public List<Restaurant> select(
      List<Restaurant> candidates,
      Map<String, RestaurantRatingSummary> summariesByRestaurantId,
      int requestedCount
  ) {
    return select(candidates, summariesByRestaurantId, requestedCount,
        ThreadLocalRandom.current()::nextDouble);
  }

  List<Restaurant> select(
      List<Restaurant> candidates,
      Map<String, RestaurantRatingSummary> summariesByRestaurantId,
      int requestedCount,
      DoubleSupplier random
  ) {
    Objects.requireNonNull(candidates, "candidates");
    Objects.requireNonNull(summariesByRestaurantId, "summariesByRestaurantId");
    Objects.requireNonNull(random, "random");
    if (requestedCount < 0) {
      throw new IllegalArgumentException("requestedCount must not be negative");
    }
    if (requestedCount == 0 || candidates.isEmpty()) {
      return List.of();
    }

    var seenIds = new HashSet<String>();
    var remaining = new ArrayList<WeightedRestaurant>(candidates.size());
    for (Restaurant candidate : candidates) {
      if (candidate == null || candidate.getId() == null || candidate.getId().isBlank()) {
        throw new IllegalArgumentException("candidate restaurant id must not be blank");
      }
      if (!seenIds.add(candidate.getId())) {
        throw new IllegalArgumentException(
            "candidate restaurant ids must be unique: " + candidate.getId());
      }
      var summary = summariesByRestaurantId.get(candidate.getId());
      if (summary != null && !candidate.getId().equals(summary.restaurantId())) {
        throw new IllegalArgumentException(
            "rating summary id does not match candidate: " + candidate.getId());
      }
      remaining.add(new WeightedRestaurant(candidate, weightFor(summary)));
    }

    var selected = new ArrayList<Restaurant>(
        Math.min(requestedCount, remaining.size()));
    while (selected.size() < requestedCount && !remaining.isEmpty()) {
      double totalWeight = remaining.stream().mapToDouble(WeightedRestaurant::weight).sum();
      double sample = random.getAsDouble();
      if (!Double.isFinite(sample) || sample < 0.0 || sample >= 1.0) {
        throw new IllegalArgumentException("random sample must be in [0, 1)");
      }
      double target = sample * totalWeight;
      double cumulativeWeight = 0.0;
      int selectedIndex = remaining.size() - 1;
      for (int index = 0; index < remaining.size(); index++) {
        cumulativeWeight += remaining.get(index).weight();
        if (target < cumulativeWeight) {
          selectedIndex = index;
          break;
        }
      }
      selected.add(remaining.remove(selectedIndex).restaurant());
    }
    return List.copyOf(selected);
  }

  static double weightFor(RestaurantRatingSummary summary) {
    if (summary == null) {
      return interpolateWeight(PRIOR_RATING);
    }
    if (summary.ratingCount() <= 0
        || summary.ratingSum() < summary.ratingCount()
        || (long) summary.ratingSum() > (long) summary.ratingCount() * 5L) {
      throw new IllegalArgumentException("rating summary count and sum are invalid");
    }
    double adjustedRating =
        (summary.ratingSum() + PRIOR_RATING * PRIOR_RATING_COUNT)
            / (summary.ratingCount() + (double) PRIOR_RATING_COUNT);
    return interpolateWeight(adjustedRating);
  }

  static double interpolateWeight(double adjustedRating) {
    if (!Double.isFinite(adjustedRating)
        || adjustedRating < 1.0
        || adjustedRating > 5.0) {
      throw new IllegalArgumentException("adjusted rating must be between 1 and 5");
    }
    int lowerAnchor = (int) Math.floor(adjustedRating);
    if (lowerAnchor == 5) {
      return RATING_WEIGHTS[4];
    }
    double lowerWeight = RATING_WEIGHTS[lowerAnchor - 1];
    double upperWeight = RATING_WEIGHTS[lowerAnchor];
    return lowerWeight + (upperWeight - lowerWeight) * (adjustedRating - lowerAnchor);
  }

  private record WeightedRestaurant(Restaurant restaurant, double weight) {}
}
```

Verification:

- GREEN: `.\gradlew.bat :website:test --tests "*RatingWeightedRestaurantSelectorTest"` passes.
- Mutation checks cover prior, anchors, removal, and interval calculation.
- Commit: `Weight WFL candidate selection by ratings`.

### Task 2 - Aggregate candidate rating summaries in one Mongo query

Sequence / dependencies:

- Runs after Task 1 and supplies the batch I/O boundary used by Task 3.

Implementation notes:

- Required skill: `chris-street-style` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: return count/sum for requested IDs using one aggregation; empty input performs no I/O.
  - Invariants: no per-candidate query; leaderboard ordering/limit stays unchanged; result shape stays `RestaurantRatingSummary`.
  - Boundary/API: add `summariesForRestaurants(Collection<String>)` beside `topRated(int)`.
  - Effects and failures: Mongo owns I/O; driver failures propagate; empty input is a valid no-op.
  - Tests and evidence: add aggregation-shape/empty tests, observe missing-method RED, implement, then focused GREEN.

#### Code Edit 2.1

- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantRatingQueryRepositoryTest.java`
- Lines: 3-55
- Action: replace

Current:

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
```

Proposed:

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;
```

Proposed test additions:

```java
  @Test
  void summariesForRestaurants_matchesAndGroupsInsideMongo() {
    var summary = new RestaurantRatingSummary("restaurant-1", 2, 9);
    when(mongo.aggregate(
        any(Aggregation.class),
        eq("whatsforlunch_ratings"),
        eq(RestaurantRatingSummary.class)))
        .thenReturn(new AggregationResults<>(List.of(summary), new Document()));

    assertThat(repository.summariesForRestaurants(
        List.of("restaurant-1", "restaurant-2"))).containsExactly(summary);

    var aggregation = ArgumentCaptor.forClass(Aggregation.class);
    verify(mongo).aggregate(
        aggregation.capture(),
        eq("whatsforlunch_ratings"),
        eq(RestaurantRatingSummary.class));
    assertThat(aggregation.getValue().toString())
        .contains("$match", "$in", "restaurant-1", "restaurant-2")
        .contains("$group", "restaurantId", "ratingCount", "ratingSum")
        .doesNotContain("$limit");
  }

  @Test
  void summariesForRestaurants_skipsMongoForEmptyCandidates() {
    assertThat(repository.summariesForRestaurants(List.of())).isEmpty();
    verifyNoInteractions(mongo);
  }
```

Verification:

- RED: focused repository test fails because `summariesForRestaurants` is absent.

#### Code Edit 2.2

- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/RestaurantRatingQueryRepository.java`
- Lines: 3-37
- Action: replace

Current:

```java
import java.util.List;
```

Proposed:

```java
import java.util.Collection;
import java.util.List;
import java.util.Objects;
```

Proposed method:

```java
  public List<RestaurantRatingSummary> summariesForRestaurants(
      Collection<String> restaurantIds
  ) {
    Objects.requireNonNull(restaurantIds, "restaurantIds");
    if (restaurantIds.isEmpty()) {
      return List.of();
    }
    var aggregation = Aggregation.newAggregation(
        Aggregation.match(
            org.springframework.data.mongodb.core.query.Criteria
                .where("restaurantId")
                .in(restaurantIds)),
        Aggregation.group("restaurantId")
            .count().as("ratingCount")
            .sum("rating").as("ratingSum"),
        Aggregation.project("ratingCount", "ratingSum")
            .and("_id").as("restaurantId"));
    return mongo.aggregate(aggregation, COLLECTION, RestaurantRatingSummary.class)
        .getMappedResults();
  }
```

Verification:

- GREEN: `.\gradlew.bat :website:test --tests "*RestaurantRatingQueryRepositoryTest"` passes.
- Captured pipeline shows one `$match`, one `$group`, and no leaderboard `$limit`.
- Commit: `Batch WFL candidate rating summaries`.

### Task 3 - Route every three-pick flow through the selector

Sequence / dependencies:

- Runs after Tasks 1 and 2.
- Keeps persistence and shared-session boundaries intact while replacing only new selection.

Implementation notes:

- Required skill: `chris-street-style` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: nearby/ZIP generation, daily refresh, and deleted-pick replacement consume the shared selector; stored daily picks continue to load in stored order.
  - Invariants: eligibility filters precede weighting; selected IDs are unique; no rating N+1; no existing pick is reweighted on read; replacement preserves survivors and fills only missing slots.
  - Boundary/API: `RestaurantService` orchestrates filtering, one batch query, selector invocation, persistence, and response mapping without API-shape changes.
  - Effects and failures: repository reads and pick writes stay explicit; selector owns randomness; lease verification remains immediately before the daily write.
  - Tests and evidence: first add a controlled selector fixture and flow-specific behavior tests; observe RED because service wiring is absent; then implement and run focused GREEN.

#### Code Edit 3.1

- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- Lines: 30-919
- Action: replace

Current:

```java
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingSummary;
import java.time.Clock;
...
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
...
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyDouble;
```

Proposed imports:

```java
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingSummary;
import dev.christopherbell.whatsforlunch.restaurant.selection.RatingWeightedRestaurantSelector;
import java.time.Clock;
import java.util.Map;
...
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
...
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyDouble;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.lenient;
```

Current:

```java
  @Mock private RestaurantRatingRepository restaurantRatingRepository;
  @Mock private RestaurantRatingQueryRepository restaurantRatingQueryRepository;
  @Mock private RestaurantRepository restaurantRepository;
```

Proposed:

```java
  @Mock private RestaurantRatingRepository restaurantRatingRepository;
  @Mock private RestaurantRatingQueryRepository restaurantRatingQueryRepository;
  @Mock private RatingWeightedRestaurantSelector restaurantSelector;
  @Mock private RestaurantRepository restaurantRepository;
```

Proposed fixture before line 95:

```java
  @BeforeEach
  void setUpWeightedSelectionDefaults() {
    lenient().when(restaurantRatingQueryRepository.summariesForRestaurants(any()))
        .thenReturn(List.of());
    lenient().when(restaurantSelector.select(any(), any(), anyInt()))
        .thenAnswer(invocation -> {
          List<Restaurant> candidates = invocation.getArgument(0);
          int requestedCount = invocation.getArgument(2);
          return candidates.stream().limit(requestedCount).toList();
        });
  }
```

Proposed nearby behavioral test after line 353:

```java
  @Test
  void nearbyLunchPicksReturnTheWeightedSelectorsChoice() throws Exception {
    var low = nearbyRestaurant("low", "Low", 30.2672, -97.7431);
    var neutral = nearbyRestaurant("neutral", "Neutral", 30.2673, -97.7432);
    var high = nearbyRestaurant("high", "High", 30.2674, -97.7433);
    var extra = nearbyRestaurant("extra", "Extra", 30.2675, -97.7434);
    var highDetail = RestaurantStub.getRestaurantDetailStub("high");
    var neutralDetail = RestaurantStub.getRestaurantDetailStub("neutral");
    var extraDetail = RestaurantStub.getRestaurantDetailStub("extra");
    var summaries = List.of(
        new RestaurantRatingSummary("low", 20, 20),
        new RestaurantRatingSummary("high", 20, 100));

    stubCoordinateCandidates(List.of(low, neutral, high, extra));
    when(restaurantRatingQueryRepository.summariesForRestaurants(
        List.of("low", "neutral", "high", "extra"))).thenReturn(summaries);
    when(restaurantSelector.select(
        List.of(low, neutral, high, extra),
        Map.of("low", summaries.get(0), "high", summaries.get(1)),
        3))
        .thenReturn(List.of(high, neutral, extra));
    when(restaurantMapper.toRestaurantDetail(high)).thenReturn(highDetail);
    when(restaurantMapper.toRestaurantDetail(neutral)).thenReturn(neutralDetail);
    when(restaurantMapper.toRestaurantDetail(extra)).thenReturn(extraDetail);

    assertThat(restaurantService.getNearbyLunchPicks(30.2672, -97.7431))
        .containsExactly(highDetail, neutralDetail, extraDetail);
  }
```

The existing ZIP test remains as the proof that ZIP coordinates enter the same
`getNearbyLunchPicksFromRestaurants` selection boundary. Add this exact daily
generation test:

```java
  @Test
  void refreshDailyLunchPicksPersistsTheWeightedSelectorsOrder() {
    var first = RestaurantStub.getRestaurantStub("first");
    var second = RestaurantStub.getRestaurantStub("second");
    var third = RestaurantStub.getRestaurantStub("third");
    var fourth = RestaurantStub.getRestaurantStub("fourth");
    List.of(first, second, third, fourth)
        .forEach(restaurant -> restaurant.getAddress().setCity("Austin"));
    var summaries = List.of(
        new RestaurantRatingSummary("first", 20, 20),
        new RestaurantRatingSummary("fourth", 20, 100));

    when(restaurantRepository.findAll())
        .thenReturn(List.of(first, second, third, fourth));
    when(restaurantRatingQueryRepository.summariesForRestaurants(
        List.of("first", "second", "third", "fourth"))).thenReturn(summaries);
    when(restaurantSelector.select(
        List.of(first, second, third, fourth),
        Map.of("first", summaries.get(0), "fourth", summaries.get(1)),
        3))
        .thenReturn(List.of(fourth, second, third));
    when(dailyLunchPicksRepository.save(any(DailyLunchPicks.class)))
        .thenAnswer(invocation -> invocation.getArgument(0));

    var pick = restaurantService.refreshDailyLunchPicks(
        LocalDate.of(2026, 8, 2));

    assertThat(pick.getRestaurantIds())
        .containsExactly("fourth", "second", "third");
  }
```

Replace the existing delete/replacement test with a fixture containing three
possible replacements, then control which two are returned:

```java
  @Test
  void deleteTodaysLunchPickPreservesSurvivorsAndUsesWeightedReplacements()
      throws Exception {
    var deleted = RestaurantStub.getRestaurantStub(RestaurantStub.ID);
    var kept = RestaurantStub.getRestaurantStub(RestaurantStub.ID_2);
    var first = RestaurantStub.getRestaurantStub("first");
    var second = RestaurantStub.getRestaurantStub("second");
    var third = RestaurantStub.getRestaurantStub("third");
    List.of(kept, first, second, third)
        .forEach(restaurant -> restaurant.getAddress().setCity("Austin"));
    var keptDetail = RestaurantStub.getRestaurantDetailStub(RestaurantStub.ID_2);
    var thirdDetail = RestaurantStub.getRestaurantDetailStub("third");
    var firstDetail = RestaurantStub.getRestaurantDetailStub("first");
    var today = LocalDate.now(ZoneId.of("America/Chicago")).toString();
    var existingPick = DailyLunchPicks.builder()
        .id(today)
        .pickDate(today)
        .restaurantIds(List.of(RestaurantStub.ID, RestaurantStub.ID_2))
        .build();

    when(restaurantRepository.findById(RestaurantStub.ID))
        .thenReturn(Optional.of(deleted));
    when(dailyLunchPicksRepository.findById(today))
        .thenReturn(Optional.of(existingPick));
    when(restaurantRepository.findAllById(List.of(RestaurantStub.ID_2)))
        .thenReturn(List.of(kept));
    when(restaurantRepository.findAll())
        .thenReturn(List.of(kept, first, second, third));
    when(restaurantSelector.select(List.of(first, second, third), Map.of(), 2))
        .thenReturn(List.of(third, first));
    when(dailyLunchPicksRepository.save(any(DailyLunchPicks.class)))
        .thenAnswer(invocation -> invocation.getArgument(0));
    when(restaurantRepository.findAllById(
        List.of(RestaurantStub.ID_2, "third", "first")))
        .thenReturn(List.of(kept, third, first));
    when(restaurantMapper.toRestaurantDetail(kept)).thenReturn(keptDetail);
    when(restaurantMapper.toRestaurantDetail(third)).thenReturn(thirdDetail);
    when(restaurantMapper.toRestaurantDetail(first)).thenReturn(firstDetail);

    var result = restaurantService.deleteRestaurantFromTodaysLunchPicks(
        RestaurantStub.ID);

    assertThat(result).containsExactly(keptDetail, thirdDetail, firstDetail);
  }
```

Retain `testGetTodaysLunchPicks_whenExistingPick_ReturnsStoredOrder` unchanged as
the read-stability regression.

Verification:

- RED: `.\gradlew.bat :website:test --tests "*RestaurantServiceTest"` fails because the service does not inject or invoke the selector.

#### Code Edit 3.2

- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 37-1123
- Action: replace

Current:

```java
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingRepository;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingQueryRepository;
...
import java.util.Collections;
...
import java.util.Random;
```

Proposed imports:

```java
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingRepository;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingQueryRepository;
import dev.christopherbell.whatsforlunch.restaurant.rating.RestaurantRatingSummary;
import dev.christopherbell.whatsforlunch.restaurant.selection.RatingWeightedRestaurantSelector;
```

Remove the now-unused `Collections` and `Random` imports.

Current:

```java
  private final RestaurantRatingRepository restaurantRatingRepository;
  private final RestaurantRatingQueryRepository restaurantRatingQueryRepository;
  private final RestaurantRepository restaurantRepository;
```

Proposed:

```java
  private final RestaurantRatingRepository restaurantRatingRepository;
  private final RestaurantRatingQueryRepository restaurantRatingQueryRepository;
  private final RatingWeightedRestaurantSelector restaurantSelector;
  private final RestaurantRepository restaurantRepository;
```

Current:

```java
    return toRatedDetails(orderLunchCandidates(candidates).stream()
        .limit(NEARBY_LUNCH_PICK_COUNT)
        .toList());
```

Proposed:

```java
    return toRatedDetails(selectLunchCandidates(
        candidates, NEARBY_LUNCH_PICK_COUNT));
```

Current:

```java
    var candidates = orderLunchCandidates(getSupportedMetroRestaurants());
    var restaurantIds = candidates.stream()
        .limit(dailyPickCount())
        .map(Restaurant::getId)
        .toList();
```

Proposed:

```java
    var selected = selectLunchCandidates(
        getSupportedMetroRestaurants(), dailyPickCount());
    var restaurantIds = selected.stream()
        .map(Restaurant::getId)
        .toList();
```

Current:

```java
      var candidates = orderLunchCandidates(getSupportedMetroRestaurants().stream()
          .filter(restaurant -> !selectedIds.contains(restaurant.getId()))
          .toList());
      for (Restaurant candidate : candidates) {
        if (selectedIds.size() >= dailyPickCount()) {
          break;
        }
        selectedIds.add(candidate.getId());
      }
```

Proposed:

```java
      int replacementCount = dailyPickCount() - selectedIds.size();
      var candidates = getSupportedMetroRestaurants().stream()
          .filter(restaurant -> !selectedIds.contains(restaurant.getId()))
          .toList();
      selectLunchCandidates(candidates, replacementCount).stream()
          .map(Restaurant::getId)
          .forEach(selectedIds::add);
```

Current:

```java
  private List<Restaurant> orderLunchCandidates(List<Restaurant> restaurants) {
    var candidates = new ArrayList<>(restaurants);
    Collections.shuffle(candidates, new Random());
    return candidates;
  }
```

Proposed:

```java
  private List<Restaurant> selectLunchCandidates(
      List<Restaurant> candidates,
      int requestedCount
  ) {
    if (candidates.isEmpty() || requestedCount == 0) {
      return List.of();
    }
    var candidateIds = candidates.stream()
        .map(Restaurant::getId)
        .toList();
    Map<String, RestaurantRatingSummary> summariesByRestaurantId =
        restaurantRatingQueryRepository.summariesForRestaurants(candidateIds).stream()
            .collect(Collectors.toUnmodifiableMap(
                RestaurantRatingSummary::restaurantId,
                Function.identity()));
    return restaurantSelector.select(
        candidates, summariesByRestaurantId, requestedCount);
  }
```

Verification:

- GREEN: `.\gradlew.bat :website:test --tests "*RatingWeightedRestaurantSelectorTest" --tests "*RestaurantRatingQueryRepositoryTest" --tests "*RestaurantServiceTest"` passes.
- Existing stored-order regression stays green; filtering precedes aggregation; lease verification remains immediately before save.
- Commit: `Use rating weights for every WFL pick flow`.

### Task 4 - Relaunch `/wfl` as the Void decision console

Sequence / dependencies:

- Runs after Task 3 so browser acceptance exercises the final selector and UI together.
- Shared WFL list/profile markup and base CSS remain unchanged.

Implementation notes:

- Required skill: `chris-street-style` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: `/wfl` renders a dark, compact, responsive console with three equal non-ranked cards and a plain-language weighting disclosure while existing controls/states remain operable.
  - Invariants: one main and one H1; controls retain accessible names, focus visibility, disabled states, and explicit button types; no first/second/third implication; neighboring WFL pages retain current styling.
  - Boundary/API: the template opts into `void-shell-page` and links `whats-for-lunch.css`; JavaScript retains event hooks and API calls while changing presentation markup only.
  - Effects and failures: DOM rendering remains owned by `whats-for-lunch.js`; stylesheet changes have no persistence effects; empty/loading/error/session states stay explicit.
  - Tests and evidence: extend ownership/accessibility tests first and observe missing-artifact RED; then add template, JS, CSS, and docs; run JS GREEN and browser acceptance.

#### Code Edit 4.1

- File: `website/src/test/js/feature-stylesheets.test.js`
- Lines: 16-75
- Action: replace

Current:

```javascript
  const [main, voidDiscovery, commandCenter, sharedFolder, siteMediaPlayer] = await Promise.all([
    resource('static/css/main.css'),
    resource('static/css/void-discovery.css'),
    resource('static/css/command-center.css'),
    resource('static/css/shared-folder.css'),
    resource('static/css/site-media-player.css'),
  ]);
```

Proposed:

```javascript
  const [
    main,
    voidDiscovery,
    commandCenter,
    sharedFolder,
    siteMediaPlayer,
    whatsForLunch,
  ] = await Promise.all([
    resource('static/css/main.css'),
    resource('static/css/void-discovery.css'),
    resource('static/css/command-center.css'),
    resource('static/css/shared-folder.css'),
    resource('static/css/site-media-player.css'),
    resource('static/css/whats-for-lunch.css'),
  ]);
```

Add `['.lunch-void-page', whatsForLunch]` to `ownership`, add `['templates/whatsforlunch.html', 'whats-for-lunch.css']` to `templates`, and add `'whats-for-lunch.css'` to the documented stylesheet list.

Verification:

- RED: `.\gradlew.bat :website:jsTest` fails because the stylesheet, link, and README ownership entry do not exist.

#### Code Edit 4.2

- File: `website/src/test/js/a11y-markup.test.js`
- Lines: after 69
- Action: add

Proposed:

```javascript
test('WFL decision console keeps one labelled main landmark and visible focus rules', () => {
  const html = fs.readFileSync(
    'website/src/main/resources/templates/whatsforlunch.html', 'utf8');
  const css = fs.readFileSync(
    'website/src/main/resources/static/css/whats-for-lunch.css', 'utf8');

  assert.equal((html.match(/<main\b/g) || []).length, 1);
  assert.equal((html.match(/<h1\b/g) || []).length, 1);
  assert.match(html, /<main[^>]+aria-labelledby="lunchTitle"/);
  assert.match(html, /class="[^"]*lunch-void-page/);
  assert.match(css, /\.lunch-void-page [^{]+:focus-visible/);
  assert.match(css, /@media \(prefers-reduced-motion: reduce\)/);
});
```

Verification:

- RED remains an expected missing-artifact/markup failure, not a syntax error.

#### Code Edit 4.3

- File: `website/src/main/resources/templates/whatsforlunch.html`
- Lines: 13-34
- Action: replace

Current:

```html
    <link rel="stylesheet" type="text/css" href="/css/main.css" th:href="@{/css/main.css}"/>
</head>

<body class="site-page lunch-page">
    <div id="nav"></div>
    <main class="site-main" role="main">
        <section class="site-hero site-hero-lunch" aria-labelledby="lunchTitle">
            <div class="container">
                <p class="home-kicker">Decision support</p>
                <h1 id="lunchTitle">What's For Lunch?</h1>
                <p>Restaurant picks for the moment when everybody is hungry and nobody has a plan.</p>
            </div>
        </section>
        <section class="site-content">
            <div class="container">
                <div class="content-panel lunch-panel">
                    <div id="whats-for-lunch"></div>
                </div>
            </div>
        </section>
    </main>
```

Proposed:

```html
    <link rel="stylesheet" type="text/css" href="/css/main.css" th:href="@{/css/main.css}"/>
    <link rel="stylesheet" type="text/css" href="/css/whats-for-lunch.css"
          th:href="@{/css/whats-for-lunch.css}"/>
</head>

<body class="site-page void-shell-page lunch-page lunch-void-page">
    <div id="nav"></div>
    <main class="site-main lunch-void-main" aria-labelledby="lunchTitle">
        <div class="lunch-void-shell">
            <div class="container lunch-void-container">
                <header class="lunch-void-hero">
                    <p class="home-kicker">Decision console</p>
                    <h1 id="lunchTitle">What's For Lunch?</h1>
                    <p>Three signals. One good decision.</p>
                </header>
                <section class="lunch-void-console" aria-label="Lunch decision console">
                    <div id="whats-for-lunch"></div>
                </section>
            </div>
        </div>
    </main>
```

Verification:

- Template keeps existing nav/footer/script hooks, one H1, and one labelled main.

#### Code Edit 4.4

- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 201-396
- Action: replace

Current:

```javascript
    <article class="lunch-pick" ${restaurantHref ? `data-restaurant-href="${sanitize(restaurantHref)}"` : ''}>
      <div class="lunch-pick-rank">${index + 1}</div>
      <div class="lunch-pick-body">
        ...
      </div>
    </article>
```

Proposed:

```javascript
    <article class="lunch-pick" ${restaurantHref ? `data-restaurant-href="${sanitize(restaurantHref)}"` : ''}>
      <div class="lunch-pick-body">
        ...
      </div>
    </article>
```

Current:

```javascript
    <div class="lunch-toolbar">
      <div>
        <p>${toolbarText}</p>
      </div>
      <button type="button" class="btn btn-primary lunch-location-refresh lunch-primary-refresh" ${activeSession && !activeSession.canChangeRestaurants ? 'disabled title="Only the active session host can change the picks"' : ''}>Try 3 more</button>
    </div>
```

Proposed:

```javascript
    <div class="lunch-toolbar">
      <div class="lunch-toolbar-copy">
        <p>${toolbarText}</p>
        <p class="lunch-weighting-note">Ratings influence the draw. Every eligible restaurant stays in the mix.</p>
      </div>
      <button type="button" class="btn btn-primary lunch-location-refresh lunch-primary-refresh" ${activeSession && !activeSession.canChangeRestaurants ? 'disabled title="Only the active session host can change the picks"' : ''}>Try 3 more</button>
    </div>
```

Verification:

- No `.lunch-pick-rank` markup remains; existing data/event hooks, URLs, and sanitization calls remain.

#### Code Edit 4.5

- File: `website/src/main/resources/static/css/whats-for-lunch.css`
- Lines: before 1
- Action: add

Proposed:

```css
.lunch-void-page {
    --lunch-void-bg: #070b10;
    --lunch-void-panel: #0c131a;
    --lunch-void-panel-raised: #111b24;
    --lunch-void-line: rgba(117, 202, 187, 0.24);
    --lunch-void-line-strong: rgba(117, 202, 187, 0.58);
    --lunch-void-teal: #75cabb;
    --lunch-void-gold: #deb15f;
    --lunch-void-text: #e6edf2;
    --lunch-void-muted: #9baab5;
    background:
        radial-gradient(circle at 16% 0%, rgba(117, 202, 187, 0.11), transparent 34rem),
        var(--lunch-void-bg);
    color: var(--lunch-void-text);
}

.lunch-void-main,
.lunch-void-shell {
    min-height: calc(100vh - 8rem);
}

.lunch-void-shell {
    padding: clamp(1.4rem, 4vw, 3.5rem) 0 4rem;
}

.lunch-void-container {
    max-width: 1240px;
}

.lunch-void-hero {
    max-width: 48rem;
    margin-bottom: 1.25rem;
}

.lunch-void-hero h1 {
    margin: 0.2rem 0 0.55rem;
    color: var(--lunch-void-text);
    font-size: clamp(2rem, 6vw, 4.4rem);
    letter-spacing: -0.045em;
}

.lunch-void-hero > p:last-child {
    margin: 0;
    color: var(--lunch-void-muted);
    font-size: clamp(1rem, 2vw, 1.2rem);
}

.lunch-void-console {
    padding: clamp(0.85rem, 2.4vw, 1.35rem);
    border: 1px solid var(--lunch-void-line);
    border-radius: 8px;
    background: rgba(8, 14, 20, 0.92);
    box-shadow: 0 1.5rem 4rem rgba(0, 0, 0, 0.28);
}

.lunch-void-page .wfl-secondary-nav,
.lunch-void-page .lunch-tools-nav {
    gap: 0.45rem;
}

.lunch-void-page .wfl-secondary-nav a,
.lunch-void-page .lunch-tool-tab {
    border-color: var(--lunch-void-line);
    border-radius: 4px;
    background: #0a1118;
    color: var(--lunch-void-muted);
}

.lunch-void-page .wfl-secondary-nav a:hover,
.lunch-void-page .wfl-secondary-nav a:focus-visible,
.lunch-void-page .wfl-secondary-nav a.active,
.lunch-void-page .lunch-tool-tab:hover,
.lunch-void-page .lunch-tool-tab:focus-visible,
.lunch-void-page .lunch-tool-tab.active {
    border-color: var(--lunch-void-line-strong);
    background: rgba(117, 202, 187, 0.10);
    color: var(--lunch-void-teal);
}

.lunch-void-page .wfl-freshness,
.lunch-void-page .lunch-toolbar,
.lunch-void-page .lunch-tools-nav,
.lunch-void-page .lunch-control-panel,
.lunch-void-page .lunch-session-panel,
.lunch-void-page .lunch-empty {
    border-color: var(--lunch-void-line);
    border-radius: 6px;
    background: var(--lunch-void-panel);
    color: var(--lunch-void-text);
}

.lunch-void-page .lunch-toolbar {
    grid-template-columns: minmax(0, 1fr) auto;
    margin-bottom: 0.8rem;
    padding: 0.85rem;
}

.lunch-void-page .lunch-toolbar-copy {
    display: grid;
    gap: 0.3rem;
}

.lunch-void-page .lunch-toolbar p,
.lunch-void-page .lunch-control-heading p,
.lunch-void-page .lunch-session-panel p,
.lunch-void-page .lunch-filter-status,
.lunch-void-page .lunch-pick-body > p,
.lunch-void-page .lunch-empty p,
.lunch-void-page .lunch-loading-state {
    color: var(--lunch-void-muted);
}

.lunch-void-page .lunch-weighting-note {
    color: var(--lunch-void-gold);
    font-size: 0.86rem;
}

.lunch-void-page .lunch-primary-refresh {
    min-height: 2.75rem;
    padding-inline: 1rem;
    border-radius: 4px;
}

.lunch-void-page .lunch-control-panel,
.lunch-void-page .lunch-session-panel {
    padding: 0.85rem;
}

.lunch-void-page .lunch-filters {
    background: var(--lunch-void-panel);
}

.lunch-void-page .lunch-radius-control,
.lunch-void-page .lunch-filter {
    color: var(--lunch-void-text);
}

.lunch-void-page .lunch-filter,
.lunch-void-page .form-control,
.lunch-void-page .form-select {
    border-color: var(--lunch-void-line);
    background: #080e14;
    color: var(--lunch-void-text);
}

.lunch-void-page .form-control::placeholder {
    color: #778792;
}

.lunch-void-page .form-control:focus,
.lunch-void-page .form-select:focus {
    border-color: var(--lunch-void-teal);
    box-shadow: 0 0 0 0.2rem rgba(117, 202, 187, 0.16);
}

.lunch-void-page .lunch-picks {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}

.lunch-void-page .lunch-pick {
    grid-template-columns: minmax(0, 1fr);
    min-width: 0;
    min-height: 100%;
    padding: 1rem;
    border-color: var(--lunch-void-line);
    border-radius: 6px;
    background:
        linear-gradient(180deg, rgba(117, 202, 187, 0.045), transparent 42%),
        var(--lunch-void-panel-raised);
    color: var(--lunch-void-text);
}

.lunch-void-page .lunch-pick:hover,
.lunch-void-page .lunch-pick:focus-within {
    border-color: var(--lunch-void-line-strong);
    box-shadow: 0 0 0 1px rgba(117, 202, 187, 0.08),
        0 1rem 2rem rgba(0, 0, 0, 0.24);
}

.lunch-void-page .lunch-pick-body {
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.lunch-void-page .lunch-pick-body h2 {
    color: var(--lunch-void-text);
    font-size: 1.15rem;
}

.lunch-void-page .lunch-cuisine,
.lunch-void-page .lunch-rating-summary {
    color: var(--lunch-void-teal);
}

.lunch-void-page .lunch-pick-actions {
    margin-top: auto;
    padding-top: 0.85rem;
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
    color: #07100f;
}

.lunch-void-page .btn-outline-primary,
.lunch-void-page .btn-outline-secondary,
.lunch-void-page .btn-outline-success {
    border-color: var(--lunch-void-line-strong);
    color: var(--lunch-void-teal);
}

.lunch-void-page .btn-success {
    border-color: var(--lunch-void-teal);
    background: rgba(117, 202, 187, 0.18);
    color: var(--lunch-void-teal);
}

.lunch-void-page .btn-outline-danger {
    border-color: rgba(236, 126, 126, 0.52);
    color: #ef9a9a;
}

.lunch-void-page button:disabled,
.lunch-void-page .btn:disabled {
    cursor: not-allowed;
    opacity: 0.48;
}

.lunch-void-page a:focus-visible,
.lunch-void-page button:focus-visible,
.lunch-void-page input:focus-visible,
.lunch-void-page select:focus-visible,
.lunch-void-page summary:focus-visible {
    outline: 3px solid var(--lunch-void-gold);
    outline-offset: 3px;
}

.lunch-void-page .lunch-loading-wheel {
    border-color: rgba(117, 202, 187, 0.18);
    border-top-color: var(--lunch-void-teal);
}

@media (max-width: 960px) {
    .lunch-void-page .lunch-picks {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 640px) {
    .lunch-void-page .lunch-toolbar {
        grid-template-columns: 1fr;
    }

    .lunch-void-page .lunch-primary-refresh,
    .lunch-void-page .lunch-zip-input {
        width: 100%;
    }
}

@media (prefers-reduced-motion: reduce) {
    .lunch-void-page *,
    .lunch-void-page *::before,
    .lunch-void-page *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
    }
}
```

Verification:

- Three equal columns at desktop, one column below 960px.
- All selectors are scoped under `.lunch-void-page`; list/profile pages cannot inherit the redesign.
- No rank selector is added.

#### Code Edit 4.6

- File: `website/src/main/resources/static/css/README.md`
- Lines: 7-48
- Action: replace

Current:

```markdown
- `void-discovery.css` owns the public Void Explore and topic discovery surfaces.
...
- WFL uses shared lunch classes for picks, restaurant profiles, favorites, and
  top-rated lists, plus `wfl-secondary-nav` for local WFL navigation and
  `lunch-controls` for the filters, location, and Lunch with Friends control tabs.
```

Proposed:

```markdown
- `void-discovery.css` owns the public Void Explore and topic discovery surfaces.
- `whats-for-lunch.css` owns the `/wfl` Void decision console while shared WFL
  list and restaurant-profile primitives remain in `main.css`.
...
- WFL uses shared lunch classes for restaurant profiles, favorites, and top-rated
  lists in `main.css`; the picks page layers `.lunch-void-*` and scoped lunch
  overrides from `whats-for-lunch.css` without changing neighboring pages.
```

Verification:

- GREEN: `.\gradlew.bat :website:jsTest` passes.
- `node --check website/src/main/resources/static/js/whats-for-lunch.js` passes.
- Commit: `Relaunch WFL as a Void decision console`.

### Task 5 - Review, verify, publish, deploy, and close

Sequence / dependencies:

- Runs after all code tasks are green.
- Any review defect starts a new RED/GREEN cycle.

Implementation notes:

- Invoke `superpowers:verification-before-completion`.
- Invoke `superpowers:requesting-code-review` for independent final-diff review.
- Apply the `chris-street-style` final rubric to production and tests.
- Invoke `verify-local-spring-app` for alternate-port startup, runtime evidence, and production restart boundaries.
- Invoke `save-test-report` after browser/API testing.
- Publish through a focused PR, wait for required CI/CodeQL, merge only when green, verify production, and close the Builder ledger with `close-hub-work`.
- Save session continuity with `save-session-memory`, refresh indexes, validate Builder state, and commit/push required Builder checkpoints.

Verification:

- Focused:
  - `.\gradlew.bat :website:test --tests "*RatingWeightedRestaurantSelectorTest" --tests "*RestaurantRatingQueryRepositoryTest" --tests "*RestaurantServiceTest"`
  - `.\gradlew.bat :website:jsTest`
- Full:
  - `.\gradlew.bat :website:check`
- Static:
  - `git diff --check`
  - inspect complete `git diff` and `git diff --stat`.
- Alternate-port runtime on an unused non-8080 port:
  - Record URL/port, UI or request input, status, and response/visible result.
  - Verify `/wfl` loads versioned `whats-for-lunch.css`.
  - Verify desktop has three equal non-ranked cards and narrow view stacks without overflow.
  - Exercise Try 3 more, filters, radius, location fallback, ZIP, rating, favorite, session/voting when authorized, safe links, and loading/empty/error states.
  - Verify keyboard focus and reduced motion.
  - Confirm disclosure: "Ratings influence the draw. Every eligible restaurant stays in the mix."
  - Confirm Top Rated, Favorites, and one restaurant profile retain existing treatment.
- Pull request and production:
  - Create PR from `codex/wfl-rating-weighted-void`.
  - Wait for every required check; fix failures under the appropriate skill.
  - Merge only when green; verify merged SHA.
  - Rotate through the approved native-Windows workflow.
  - Recheck readiness after transient 503 and verify exact assets, WFL endpoints/pages, database health, and services.

## Code Changes

- Add `RatingWeightedRestaurantSelector` and deterministic/domain/distribution tests.
- Extend `RestaurantRatingQueryRepository` with one candidate-batch aggregate and tests.
- Inject and use the selector in `RestaurantService` for nearby/ZIP, daily, and replacement flows.
- Update service tests for selected order while preserving stored-order coverage.
- Opt `whatsforlunch.html` into the Void shell and dedicated stylesheet.
- Remove numeric card rank and add the weighting disclosure in `whats-for-lunch.js`.
- Add scoped responsive rules in `whats-for-lunch.css`.
- Document and enforce CSS ownership in README/Node tests.

## Files and Modules

- Java selection: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/selection/`
- Java orchestration: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Mongo aggregation: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/`
- Java tests: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/`
- WFL runtime: `website/src/main/resources/templates/whatsforlunch.html`, `website/src/main/resources/static/js/whats-for-lunch.js`
- CSS: `website/src/main/resources/static/css/whats-for-lunch.css`, `website/src/main/resources/static/css/README.md`
- Frontend tests: `website/src/test/js/`

## Unit Testing

- Watch each selector, repository, service, and frontend test fail for the expected missing behavior before production edits.
- Selector: neutral fallback, sparse blend, anchors, no replacement, input immutability, invalid data/randomness, fixed-seed frequency order.
- Repository: match/group projection and empty no-I/O.
- Service: nearby/ZIP selected order, daily persisted order, replacement survivor/fill behavior, stored-read stability.
- Frontend: dedicated owner/link/docs, one labelled main/H1, focus-visible, and reduced-motion.

## Local Testing

- Use a private task-specific `GRADLE_USER_HOME`.
- Run focused RED/GREEN commands after each task, then `:website:check`.
- Start on an unused non-8080 port selected by `verify-local-spring-app`.
- Use the in-app browser skill for desktop/mobile/accessibility acceptance.
- Capture URL/port, input/action, status, and response/visible result; build output alone is insufficient.

## Validation

- Statistical contract matches the approved formula and weights.
- Every eligible restaurant has positive weight and selected IDs are unique.
- No selection flow performs rating N+1.
- Stored daily/shared-session picks are not silently rerolled.
- `/wfl` reads as three neutral options, not a ranking.
- Controls and states remain usable by mouse, keyboard, and assistive technology.
- Dedicated styling does not leak to adjacent WFL pages.
- Focused/full tests, alternate-port acceptance, PR CI, merged production health, and assets pass.

## Rollback or Recovery

- Before merge: revert focused branch commits or close the PR; the authoritative checkout remains untouched.
- After merge: revert the merge in a tested PR and deploy the last known-good merged SHA through the native workflow.
- No data rollback is required because there is no schema, migration, cache, or persisted weight.
- If weighting is disabled urgently, revert service wiring and UI disclosure together so behavior and copy stay truthful.

## Risks

- Sparse ratings dominate: three neutral virtual ratings plus formula tests.
- Randomness hides regression: controllable `DoubleSupplier`, exact weights, fixed seed.
- Malformed data biases selection: explicit ID/aggregate validation.
- Mongo N+1: one batch aggregation and pipeline test.
- Existing picks change: weight generation/replacement only and stored-order regression.
- CSS leaks: dedicated stylesheet plus `.lunch-void-page` scoping.
- Cards become cramped: 960px stack and browser widths.
- Rank implication persists: numeric badge removal and equal cards.
- Dirty checkout damage: isolated worktree verification.
- Production interruption: alternate-port evidence, controlled rotation, readiness recheck, rollback SHA.

## Completion Criteria

- All Code Edit blocks execute in order under observed RED/GREEN cycles.
- Exact confidence formula and weights are implemented and covered.
- Nearby/ZIP, daily, and replacement flows use the same selector with unique IDs.
- Existing stored picks remain stable on read.
- `/wfl` uses the dedicated Void stylesheet, equal non-ranked cards, and disclosure.
- Adjacent WFL pages remain visually unchanged.
- Focused Java/JS tests, `:website:check`, diff checks, and independent review pass.
- Alternate-port evidence is saved in a Builder test report.
- PR checks pass, PR merges, merged SHA deploys, and production WFL/service/database/assets verify.
- Builder closure, indexes, validation, and session memory are committed and pushed.
