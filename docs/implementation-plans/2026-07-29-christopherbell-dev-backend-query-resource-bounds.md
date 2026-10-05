# christopherbell.dev Backend Query and Resource Bounds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep conversation query count constant, bound VIN anti-abuse memory and upstream response work, and make scheduled writers explicitly safe for multi-instance execution.

**Architecture:** Mongo aggregation replaces row-by-row unread counts. Existing bounded Bucket4j storage becomes the VIN limiter's ownership boundary. A transport-neutral bounded body reader is shared by multiple synchronous clients, while public VIN requests use a finite bulkhead. Every scheduled writer is recorded as leased, atomically claimed, duplicate-safe, tracked by an existing issue, or unsupported.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB aggregation, Bucket4j, JDK `HttpClient`, JUnit 5.

## Global Constraints

- Query groups remain constant from one through fifty conversations.
- Changed process-local stores define both maximum cardinality and inactivity expiry.
- Upstream bodies are byte-bounded before conversion to strings or JSON.
- Slow public upstream work has a finite concurrency bound and releases permits on every outcome.
- Lease loss stops subsequent writes; scheduled jobs never rely only on an in-process lock for multi-instance exclusivity.
- Existing issues #1273-#1279, #1281-#1287, and #1290-#1297 remain the owners of overlapping scaling work.
- Do not modify the dirty checkout at `A:\Projects\christopherbell.dev`; execute in an isolated `codex/` worktree.
- Invoke `write-chris-street-style-code` and `superpowers:test-driven-development` before production behavior edits.
- Implementation requires separate explicit user authorization.

---

## Document Status

ready-for-execution

## Objective

Implement the bounded backend batch from the approved performance specification and produce repeatable query/cardinality/body/concurrency evidence.

## Goals

- Replace conversation-summary N+1 unread counts with one aggregation.
- Cap VIN limiter keys at 10,000 and expire inactive keys after twice the configured rate window.
- Bound NHTSA, OpenStreetMap, Random VIN, robots, and Canes response bodies.
- Permit at most eight concurrent public NHTSA decode calls per application instance.
- Classify every current `@Scheduled` writer and lease the unowned multi-instance-sensitive jobs not already covered by an open issue.

## Inputs

- Approved Builder performance specification.
- Current source inspected at `origin/main` commit `f31535f29312d24573a6031b0162aa8ebc4b5318`.
- Existing `RateLimitBucketStore` and Mongo lease infrastructure.
- Existing campaign issues #1273-#1297.

## Branch

- Create `codex/backend-query-resource-bounds` from refreshed `origin/main` in an isolated worktree.
- If the issue campaign changes an overlapping file first, refresh the ranges and preserve the issue's accepted contract.

## Non-Goals

- Do not introduce Redis or a distributed rate-limit service.
- Do not redesign response models or retry policies.
- Do not duplicate post, WFL, or Shared Folder issue work.
- Do not make scheduled candidate/smoke deployments write production data.

## Assumptions

- Conversation summary limit remains capped at 50.
- A per-process VIN limit remains acceptable until multi-instance abuse evidence justifies distributed enforcement.
- Existing synchronous clients can consume `InputStream` response bodies.
- Mongo leases remain the repository-standard durable coordination mechanism.

## Open Questions

None.

## File Structure

- `ConversationQueryRepository` owns summary-related aggregations.
- `RateLimitBucketStore` remains a generic website-level Bucket4j store for this batch.
- `dev.christopherbell.libs.http.BoundedResponseBodyReader` is JDK-only and serves five proven consumers.
- `VinDecodeBulkhead` stays in the VIN feature because only public decode currently needs that admission policy.
- `docs/operations/scheduled-writers.md` is the canonical classification table.

## Task Breakdown

### Task 1 - Batch conversation unread counts

Sequence / dependencies:
- Independent first task; complete it before resource-bound changes so query-count evidence stays reviewable.

Implementation notes:
- Required skill: `write-chris-street-style-code` before code edits; invoke `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: summaries retain ordering, archived visibility, display names, and unread semantics while unread counts arrive from one aggregation.
  - Invariants: only unread messages addressed to the current account count; missing senders produce zero.
  - Boundary/API: `ConversationQueryRepository.unreadCounts(String, Collection<String>)` returns an immutable sender-id map; HTTP response shape is unchanged.
  - Effects and failures: one Mongo aggregation replaces up to fifty repository counts; Mongo failures retain the existing service failure behavior.
  - Tests and evidence: RED service test verifies the old per-row method is invoked; GREEN verifies one aggregation call for one and fifty rows and zero legacy count calls.

- [ ] Add repository aggregation-shape and service query-count tests.
- [ ] Run the focused tests and capture RED.
- [ ] Implement `unreadCounts` and pass the map into pure summary mapping.
- [ ] Remove the unused count repository method.
- [ ] Run message tests and commit.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/message/conversation/ConversationUnreadCount.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.message.conversation;

/** Mongo aggregation row for unread messages grouped by sender. */
record ConversationUnreadCount(String id, long count) {}
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/message/conversation/ConversationQueryRepository.java`
- Lines: after 55
- Action: add

Proposed:
```java
  /** Counts unread incoming messages for all returned conversation peers in one query. */
  public java.util.Map<String, Long> unreadCounts(
      String recipientAccountId,
      java.util.Collection<String> senderAccountIds) {
    if (senderAccountIds.isEmpty()) return java.util.Map.of();
    var aggregation = Aggregation.newAggregation(
        Aggregation.match(new Criteria().andOperator(
            Criteria.where("recipientAccountId").is(recipientAccountId),
            Criteria.where("senderAccountId").in(senderAccountIds),
            Criteria.where("read").is(false))),
        Aggregation.group("senderAccountId").count().as("count"));
    return mongo.aggregate(
            aggregation, "messages", ConversationUnreadCount.class)
        .getMappedResults().stream()
        .collect(java.util.stream.Collectors.toUnmodifiableMap(
            ConversationUnreadCount::id, ConversationUnreadCount::count));
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.message.conversation.ConversationQueryRepositoryTest`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/message/conversation/ConversationService.java`
- Lines: 87-92
- Action: replace

Current:
```java
    var accounts = accountRepository.findAllById(latestByOtherId.keySet());
    var accountById = new HashMap<String, Account>();
    accounts.forEach(account -> accountById.put(account.getId(), account));
    return latestByOtherId.entrySet().stream()
        .map(entry -> summary(entry.getKey(), entry.getValue(), self, accountById.get(entry.getKey())))
        .toList();
```

Proposed:
```java
    var accounts = accountRepository.findAllById(latestByOtherId.keySet());
    var accountById = new HashMap<String, Account>();
    accounts.forEach(account -> accountById.put(account.getId(), account));
    var unreadBySender = conversationQueries.unreadCounts(
        self.getId(), latestByOtherId.keySet());
    return latestByOtherId.entrySet().stream()
        .map(entry -> summary(
            entry.getKey(), entry.getValue(), accountById.get(entry.getKey()),
            unreadBySender.getOrDefault(entry.getKey(), 0L)))
        .toList();
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.message.conversation.*`

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/message/conversation/ConversationService.java`
- Lines: 104-115
- Action: replace

Current:
```java
  private ConversationSummary summary(String otherId, Message message, Account self, Account other) {
    return ConversationSummary.builder()
        .accountId(otherId)
        .username(other == null ? null : other.getUsername())
        .displayName(displayName(other))
        .latestText(message.getText())
        .lastMessageOn(message.getCreatedOn())
        .unreadCount(messageRepository.countByRecipientAccountIdAndSenderAccountIdAndReadFalse(
            self.getId(),
            otherId))
        .build();
  }
```

Proposed:
```java
  private ConversationSummary summary(
      String otherId, Message message, Account other, long unreadCount) {
    return ConversationSummary.builder()
        .accountId(otherId)
        .username(other == null ? null : other.getUsername())
        .displayName(displayName(other))
        .latestText(message.getText())
        .lastMessageOn(message.getCreatedOn())
        .unreadCount(unreadCount)
        .build();
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.message.conversation.*`

#### Code Edit 1.5
- File: `website/src/main/java/dev/christopherbell/message/MessageRepository.java`
- Lines: 13-15
- Action: replace

Current:
```java
  List<Message> findByParticipantIdsContainingOrderByCreatedOnDesc(String accountId, Pageable pageable);

  long countByRecipientAccountIdAndSenderAccountIdAndReadFalse(String recipientAccountId, String senderAccountId);
```

Proposed:
```java
  List<Message> findByParticipantIdsContainingOrderByCreatedOnDesc(String accountId, Pageable pageable);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.message.*`

#### Code Edit 1.6
- File: `website/src/test/java/dev/christopherbell/message/conversation/ConversationQueryRepositoryTest.java`
- Lines: after 54
- Action: add

Proposed:
```java
  @Test
  void unreadCountsGroupsAllRequestedSendersInOneAggregation() {
    when(mongo.aggregate(any(Aggregation.class), eq("messages"),
        eq(ConversationUnreadCount.class)))
        .thenReturn(new AggregationResults<>(
            List.of(new ConversationUnreadCount("other-a", 2L)), new Document()));

    var counts = repository.unreadCounts("self", List.of("other-a", "other-b"));

    assertThat(counts).containsEntry("other-a", 2L).doesNotContainKey("other-b");
    var aggregation = ArgumentCaptor.forClass(Aggregation.class);
    verify(mongo).aggregate(
        aggregation.capture(), eq("messages"), eq(ConversationUnreadCount.class));
    assertThat(aggregation.getValue().toString())
        .contains("recipientAccountId", "senderAccountId", "$in", "read", "$group", "$count");
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.message.conversation.ConversationQueryRepositoryTest`

### Task 2 - Bound VIN limiter cardinality and inactivity

Sequence / dependencies:
- Runs after Task 1; independent of outbound body handling.

Implementation notes:
- Required skill: `write-chris-street-style-code` before code edits; invoke `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: VIN capacity and batch-token charging are unchanged while no more than 10,000 client buckets remain resident and inactive entries expire.
  - Invariants: the same key reuses its bucket inside the inactivity window; concurrent access never produces multiple active buckets for one key.
  - Boundary/API: adds validated `maximum-buckets`; controller/service API is unchanged.
  - Effects and failures: least-recently-used eviction can reset a rarely used client's local allowance, which is acceptable for a process-local defense; invalid token costs still reject.
  - Tests and evidence: cardinality, expiry, reuse, token cost, and concurrent-access tests use a controllable monotonic clock.

- [ ] Add failing limiter cardinality and expiry tests.
- [ ] Expose bounded-store metrics safely and replace the map.
- [ ] Add configuration validation/default and documentation.
- [ ] Run focused vehicle/config tests and commit.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitBucketStore.java`
- Lines: 63-68
- Action: replace

Current:
```java
  synchronized boolean contains(String key) {
    return entries.containsKey(key);
  }

  synchronized int size() {
    return entries.size();
  }
```

Proposed:
```java
  synchronized boolean contains(String key) {
    return entries.containsKey(key);
  }

  public synchronized int size() {
    removeExpired(nanoTime.getAsLong());
    return entries.size();
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.filter.RateLimitBucketStoreTest`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/vehicle/model/VehicleProperties.java`
- Lines: 113-124
- Action: replace

Current:
```java
  public static class VinDecoder {
    @Min(1)
    private int rateLimitCapacity = 20;
    @NotNull @DurationMin(seconds = 1)
    private Duration rateLimitWindow;
    @NotBlank
    private String decoderVersion = "vpic-2026-07";
    @NotNull @DurationMin(seconds = 1)
    private Duration cacheTtl = Duration.ofDays(30);
    @Min(1) @Max(50)
    private int maxBatchSize = 20;
  }
```

Proposed:
```java
  public static class VinDecoder {
    @Min(1)
    private int rateLimitCapacity = 20;
    @NotNull @DurationMin(seconds = 1)
    private Duration rateLimitWindow;
    @Min(100) @Max(100_000)
    private int maximumBuckets = 10_000;
    @NotBlank
    private String decoderVersion = "vpic-2026-07";
    @NotNull @DurationMin(seconds = 1)
    private Duration cacheTtl = Duration.ofDays(30);
    @Min(1) @Max(50)
    private int maxBatchSize = 20;
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.*PropertiesTest`

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/vehicle/nhtsa/decode/VehicleVinDecodeRateLimiter.java`
- Lines: 1-35
- Action: replace

Current:
```java
package dev.christopherbell.vehicle.nhtsa.decode;

import dev.christopherbell.vehicle.model.VehicleProperties;
import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.Bucket4j;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@RequiredArgsConstructor
@Component
public class VehicleVinDecodeRateLimiter {
  private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();
  private final VehicleProperties vehicleProperties;

  public void check(String key) {
    check(key, 1);
  }

  public void check(String key, long tokens) {
    var bucket = buckets.computeIfAbsent(key, ignored -> newBucket());
    if (tokens < 1 || !bucket.tryConsume(tokens)) {
      throw new VehicleVinDecodeRateLimitException("Too many VIN decode requests. Please try again later.");
    }
  }

  private Bucket newBucket() {
    var properties = vehicleProperties.getVinDecoder();
    return Bucket4j.builder()
        .addLimit(Bandwidth.simple(properties.getRateLimitCapacity(), properties.getRateLimitWindow()))
        .build();
  }
}
```

Proposed:
```java
package dev.christopherbell.vehicle.nhtsa.decode;

import dev.christopherbell.configuration.filter.RateLimitBucketStore;
import dev.christopherbell.vehicle.model.VehicleProperties;
import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.Bucket4j;
import org.springframework.stereotype.Component;

@Component
public class VehicleVinDecodeRateLimiter {
  private final VehicleProperties vehicleProperties;
  private final RateLimitBucketStore buckets;

  public VehicleVinDecodeRateLimiter(VehicleProperties vehicleProperties) {
    this(vehicleProperties, new RateLimitBucketStore(
        vehicleProperties.getVinDecoder().getMaximumBuckets(), System::nanoTime));
  }

  VehicleVinDecodeRateLimiter(
      VehicleProperties vehicleProperties, RateLimitBucketStore buckets) {
    this.vehicleProperties = vehicleProperties;
    this.buckets = buckets;
  }

  public void check(String key) {
    check(key, 1);
  }

  public void check(String key, long tokens) {
    var properties = vehicleProperties.getVinDecoder();
    Bucket bucket = buckets.getOrCreate(
        key, properties.getRateLimitWindow().multipliedBy(2), this::newBucket);
    if (tokens < 1 || !bucket.tryConsume(tokens)) {
      throw new VehicleVinDecodeRateLimitException(
          "Too many VIN decode requests. Please try again later.");
    }
  }

  int bucketCount() {
    return buckets.size();
  }

  private Bucket newBucket() {
    var properties = vehicleProperties.getVinDecoder();
    return Bucket4j.builder()
        .addLimit(Bandwidth.simple(
            properties.getRateLimitCapacity(), properties.getRateLimitWindow()))
        .build();
  }
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.nhtsa.decode.VehicleVinDecodeRateLimiterTest --tests dev.christopherbell.configuration.filter.RateLimitBucketStoreTest`

#### Code Edit 2.4
- File: `website/src/main/resources/application.yml`
- Lines: 676-681
- Action: replace

Current:
```yaml
  vin-decoder:
    rate-limit-capacity: 20
    rate-limit-window: 1m
    decoder-version: vpic-2026-07
    cache-ttl: 30d
    max-batch-size: 20
```

Proposed:
```yaml
  vin-decoder:
    rate-limit-capacity: 20
    rate-limit-window: 1m
    maximum-buckets: 10000
    decoder-version: vpic-2026-07
    cache-ttl: 30d
    max-batch-size: 20
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.*PropertiesTest`

### Task 3 - Bound upstream bodies and public VIN concurrency

Sequence / dependencies:
- Runs after Task 2 so limiter and bulkhead evidence can be tested together; independent of scheduled work.

Implementation notes:
- Required skill: `write-chris-street-style-code` before code edits; invoke `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: each reviewed client rejects an oversized body before string/JSON materialization; at most eight public VIN upstream calls are active per instance.
  - Invariants: status checks, timeouts, parsing, cooldowns, redirects, and safe diagnostic messages remain feature-owned.
  - Boundary/API: shared reader accepts `InputStream`, byte limit, and charset; typed feature exceptions translate limit failures.
  - Effects and failures: streams and permits close in `finally`/try-with-resources; oversized and saturated outcomes are safe service-unavailable/rate-limit failures without body logging.
  - Tests and evidence: exact-limit, limit-plus-one, interrupted read, permit exhaustion, exception release, and client-specific malformed/status tests.

- [ ] Add RED shared-reader and VIN bulkhead tests.
- [ ] Add the JDK-only reader to `cbell-lib` and consume it from all five client families.
- [ ] Switch client handlers from `ofString`/`ofByteArray` to `ofInputStream` and translate `BodyLimitExceededException`.
- [ ] Add the eight-permit VIN admission boundary around only the remote call, not cache reads.
- [ ] Run client suites and commit.

#### Code Edit 3.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/http/BodyLimitExceededException.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.libs.http;

import java.io.IOException;

/** Signals that a remote response exceeded its caller-declared byte contract. */
public final class BodyLimitExceededException extends IOException {
  public BodyLimitExceededException(long maximumBytes) {
    super("Remote response exceeded the " + maximumBytes + " byte limit.");
  }
}
```

Verification:
- `./gradlew :cbell-lib:test`

#### Code Edit 3.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/http/BoundedResponseBodyReader.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.libs.http;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;

/** Reads a remote body without allocating beyond a declared maximum plus one byte. */
public final class BoundedResponseBodyReader {
  private static final int BUFFER_SIZE = 8_192;

  private BoundedResponseBodyReader() {}

  public static byte[] read(InputStream input, long maximumBytes) throws IOException {
    if (maximumBytes < 0 || maximumBytes > Integer.MAX_VALUE - 1L) {
      throw new IllegalArgumentException("maximum response bytes are invalid");
    }
    try (input; var output = new ByteArrayOutputStream((int) Math.min(maximumBytes, BUFFER_SIZE))) {
      byte[] buffer = new byte[BUFFER_SIZE];
      long total = 0;
      while (true) {
        int count = input.read(buffer);
        if (count < 0) return output.toByteArray();
        total += count;
        if (total > maximumBytes) throw new BodyLimitExceededException(maximumBytes);
        output.write(buffer, 0, count);
      }
    }
  }

  public static String readString(
      InputStream input, long maximumBytes, Charset charset) throws IOException {
    return new String(read(input, maximumBytes), charset);
  }
}
```

Verification:
- `./gradlew :cbell-lib:test --tests dev.christopherbell.libs.http.BoundedResponseBodyReaderTest`

#### Code Edit 3.2a
- File: `cbell-lib/src/test/java/dev/christopherbell/libs/http/BoundedResponseBodyReaderTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.libs.http;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.ByteArrayInputStream;
import org.junit.jupiter.api.Test;

class BoundedResponseBodyReaderTest {
  @Test
  void acceptsAResponseAtTheExactLimit() throws Exception {
    assertThat(BoundedResponseBodyReader.readString(
        new ByteArrayInputStream("four".getBytes(UTF_8)), 4, UTF_8))
        .isEqualTo("four");
  }

  @Test
  void rejectsBeforeMaterializingPastTheLimit() {
    assertThatThrownBy(() -> BoundedResponseBodyReader.read(
        new ByteArrayInputStream(new byte[9]), 8))
        .isInstanceOf(BodyLimitExceededException.class);
  }

  @Test
  void rejectsInvalidMaximums() {
    assertThatThrownBy(() -> BoundedResponseBodyReader.read(
        new ByteArrayInputStream(new byte[0]), -1))
        .isInstanceOf(IllegalArgumentException.class);
  }
}
```

Verification:
- `./gradlew :cbell-lib:test --tests dev.christopherbell.libs.http.BoundedResponseBodyReaderTest`

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/vehicle/nhtsa/decode/VinDecodeBulkhead.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.vehicle.nhtsa.decode;

import java.util.Optional;
import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicBoolean;
import org.springframework.stereotype.Component;

/** Owns the finite per-instance concurrency budget for public VIN upstream calls. */
@Component
final class VinDecodeBulkhead {
  private final Semaphore permits;

  VinDecodeBulkhead() {
    this(8);
  }

  VinDecodeBulkhead(int maximumConcurrentRequests) {
    permits = new Semaphore(maximumConcurrentRequests, true);
  }

  Optional<Permit> tryAcquire() {
    return permits.tryAcquire() ? Optional.of(new Permit(permits)) : Optional.empty();
  }

  static final class Permit implements AutoCloseable {
    private final Semaphore permits;
    private final AtomicBoolean closed = new AtomicBoolean();

    private Permit(Semaphore permits) {
      this.permits = permits;
    }

    @Override
    public void close() {
      if (closed.compareAndSet(false, true)) permits.release();
    }
  }
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.nhtsa.decode.VinDecodeBulkheadTest`

#### Code Edit 3.3a
- File: `website/src/main/java/dev/christopherbell/vehicle/nhtsa/decode/VehicleVinDecodeService.java`
- Lines: 32-194
- Action: replace

Current:
```java
  private final VehicleVinDecodeRateLimiter rateLimiter;
  private final Map<String, Object> vinLocks = new ConcurrentHashMap<>();
```

Proposed:
```java
  private final VehicleVinDecodeRateLimiter rateLimiter;
  private final VinDecodeBulkhead bulkhead;
  private final Map<String, Object> vinLocks = new ConcurrentHashMap<>();
```

Implementation:
- Add `VinDecodeBulkhead bulkhead` as the final constructor argument and assign it.
- In `decodeAndCache`, acquire a permit immediately before `nhtsaVinClient.decodeVin`; use try-with-resources so every success and exception releases it. If no permit is available, throw `temporarilyUnavailable()` without starting a remote request.
- In the batch miss path, acquire and close one permit around `nhtsaVinClient.decodeVins` using the same rule.
- Do not acquire a permit for validation, rate limiting, cache reads, cache writes, cooldown checks, or result mapping.
- Extend `VehicleVinDecodeServiceTest` with an exhausted-permit case for single and batch requests and a subsequent-success case proving permit release after an upstream exception.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.nhtsa.decode.VehicleVinDecodeServiceTest --tests dev.christopherbell.vehicle.nhtsa.decode.VinDecodeBulkheadTest`

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/vehicle/nhtsa/decode/NhtsaVinClient.java`
- Lines: 93-98
- Action: replace

Current:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      throw new VehicleVinDecodeUnavailableException("NHTSA VIN decoding is temporarily unavailable.");
    }

    var nhtsaResponse = objectMapper.readValue(response.body(), RESPONSE_TYPE);
```

Proposed:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofInputStream());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      response.body().close();
      throw new VehicleVinDecodeUnavailableException(
          "NHTSA VIN decoding is temporarily unavailable.");
    }
    String body = dev.christopherbell.libs.http.BoundedResponseBodyReader.readString(
        response.body(), 2L * 1024 * 1024, java.nio.charset.StandardCharsets.UTF_8);
    var nhtsaResponse = objectMapper.readValue(body, RESPONSE_TYPE);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.*Nhtsa*Test`

#### Code Edit 3.5
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 52-57
- Action: replace

Current:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      throw new IllegalStateException("OpenStreetMap restaurant import failed.");
    }

    return parseRestaurants(response.body());
```

Proposed:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofInputStream());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      response.body().close();
      throw new IllegalStateException("OpenStreetMap restaurant import failed.");
    }
    String body = dev.christopherbell.libs.http.BoundedResponseBodyReader.readString(
        response.body(), 16L * 1024 * 1024, java.nio.charset.StandardCharsets.UTF_8);
    return parseRestaurants(body);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.whatsforlunch.restaurant.OpenStreetMapRestaurantClientTest`

#### Code Edit 3.6
- File: `website/src/main/java/dev/christopherbell/vehicle/randomvin/importing/RandomVinClient.java`
- Lines: 50-55
- Action: replace

Current:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      throw new IllegalStateException("Random VIN source returned an unsuccessful response.");
    }

    return response.body();
```

Proposed:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofInputStream());
    if (response.statusCode() < 200 || response.statusCode() >= 300) {
      response.body().close();
      throw new IllegalStateException("Random VIN source returned an unsuccessful response.");
    }
    return dev.christopherbell.libs.http.BoundedResponseBodyReader.readString(
        response.body(), 4 * 1024, java.nio.charset.StandardCharsets.UTF_8);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.randomvin.*`

#### Code Edit 3.7
- File: `website/src/main/java/dev/christopherbell/vehicle/randomvin/policy/RandomVinRobotsPolicy.java`
- Lines: 61-65
- Action: replace

Current:
```java
      var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() < 200 || response.statusCode() >= 300) {
        return unavailableDecision();
      }
      return evaluate(response.body());
```

Proposed:
```java
      var response = httpClient.send(request, HttpResponse.BodyHandlers.ofInputStream());
      if (response.statusCode() < 200 || response.statusCode() >= 300) {
        response.body().close();
        return unavailableDecision();
      }
      String body = dev.christopherbell.libs.http.BoundedResponseBodyReader.readString(
          response.body(), 256 * 1024, java.nio.charset.StandardCharsets.UTF_8);
      return evaluate(body);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.vehicle.randomvin.policy.*`

#### Code Edit 3.8
- File: `website/src/main/java/dev/christopherbell/canesboxtracker/OfficialCanesBoxPriceClient.java`
- Lines: 182-349
- Action: replace

Current:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    if (response.statusCode() != 200) {
      throw new IllegalStateException(
          "Official GraphQL API returned HTTP " + response.statusCode() + ": " + response.body());
    }
    var body = response.body();
```

Proposed:
```java
    var response = httpClient.send(request, HttpResponse.BodyHandlers.ofInputStream());
    if (response.statusCode() != 200) {
      response.body().close();
      throw new IllegalStateException(
          "Official GraphQL API returned HTTP " + response.statusCode() + ".");
    }
    String body = dev.christopherbell.libs.http.BoundedResponseBodyReader.readString(
        response.body(), 4L * 1024 * 1024, java.nio.charset.StandardCharsets.UTF_8);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.canesboxtracker.*`

Additional required replacements in the same file:
- At lines 209-218, use `ofInputStream`, read at most 4 MiB as UTF-8, and preserve the existing status and audit-metadata behavior without logging the body.
- At lines 342-349, use `ofInputStream`, read at most 8 MiB as bytes, and pass those bounded bytes to the existing `responseBody` decoding boundary. Close the stream on non-2xx responses.
- Add client tests at exact limit and limit-plus-one for GraphQL, restaurant JSON, and public-menu fallback responses.

### Task 4 - Classify and lease scheduled writers

Sequence / dependencies:
- Runs after Tasks 1-3. It may use the shared lease package at its current website path; the library-boundary plan later moves that package without changing behavior.

Implementation notes:
- Required skill: `write-chris-street-style-code` before code/config edits; invoke `superpowers:test-driven-development` for lease behavior.
- Before-Edit Brief:
  - Behavior: WFL daily picks, Music catalog reconciliation, and Music metadata cleanup have one durable owner; already-safe jobs keep their current claim model; issue-owned jobs are linked.
  - Invariants: lease duration exceeds maximum owned operation or is renewed; loss prevents later writes; manual entry points retain authorization and behavior.
  - Boundary/API: scheduled methods remain parameterless; owned helpers accept `CollectorLeaseGuard` when work spans multiple writes.
  - Effects and failures: contention logs/records a skip, lease infrastructure failure fails closed, expiry permits a later retry.
  - Tests and evidence: deterministic contention, renewal, expiry, ownership-loss, and smoke-profile-disable tests.

- [ ] Write the complete scheduled-writer classification table from the current `@Scheduled` inventory.
- [ ] Add RED contention tests for the three unowned multi-instance-sensitive jobs.
- [ ] Wrap WFL daily selection, Music catalog scan, and metadata cleanup in `ScheduledCollectorCoordinator`; place guard checks before writes.
- [ ] Confirm all other writers are leased, atomically claimed, duplicate-safe with an explicit proof, issue-owned, or unsupported.
- [ ] Run scheduling/feature tests and commit.

#### Code Edit 4.1
- File: `docs/operations/scheduled-writers.md`
- Lines: before 1
- Action: add

Proposed:
```markdown
# Scheduled Writer Ownership

| Job | Classification | Durable owner | Retry after loss |
|---|---|---|---|
| Canes weekly collection | Mongo lease | `ScheduledCollectorCoordinator` | next schedule/manual run |
| WFL OSM import | Mongo lease | import lease/coordinator | next schedule/startup catch-up |
| WFL daily picks | Mongo lease | `ScheduledCollectorCoordinator` | next request/schedule |
| NHTSA enrichment | Mongo lease | `ScheduledCollectorCoordinator` | next fixed delay |
| Random VIN import | Mongo lease | `ScheduledCollectorCoordinator` | next fixed delay |
| Music radio tick | Mongo lease | `MongoLeaseService` | next tick |
| Music catalog scan | Mongo lease | `ScheduledCollectorCoordinator` | next scan |
| Music metadata cleanup | Mongo lease | `ScheduledCollectorCoordinator` | next cleanup |
| Federation reconcile/deliver | atomic cursor and per-job claims | federation store | next scan/claim expiry |
| Shared Folder maintenance | host lock plus Mongo lease | maintenance service | next pass |
| Post expiration cleanup | tracked scaling work | issues #1278 and #1279 | issue contract |
| Shared Folder media admission/retention | tracked scaling work | issues #1294, #1296, #1297 | issue contract |

Candidate production-profile validation must keep all scheduled writers disabled.
```

Verification:
- `rg -n "@Scheduled" website/src/main/java` must have one table row per scheduled writer; reconcile any new source before marking the task complete.

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 69-916
- Action: replace

Current:
```java
  @Scheduled(
      cron = "${wfl.restaurant-of-the-day.cron}",
      zone = "${wfl.restaurant-of-the-day.zone:America/Chicago}"
  )
  public void setRestaurantOfTheDay() {
    if (!wflProperties.getRestaurantOfTheDay().isEnabled()) {
      return;
    }
    log.info("Restaurant of the day job started.");
    try {
      var today = LocalDate.now(getRestaurantOfTheDayZone());
      var picks = refreshDailyLunchPicks(today);
      log.info("Restaurant of the day selected {} picks for {}.", picks.getRestaurantIds().size(), today);
    } finally {
      log.info("Restaurant of the day job completed.");
    }
  }
```

Proposed:
```java
  @Scheduled(
      cron = "${wfl.restaurant-of-the-day.cron}",
      zone = "${wfl.restaurant-of-the-day.zone:America/Chicago}"
  )
  public void setRestaurantOfTheDay() {
    if (!wflProperties.getRestaurantOfTheDay().isEnabled()) return;
    scheduledCollectors.run(
        "wfl-daily-picks", DAILY_PICK_LEASE_DURATION, guard -> {
          var today = LocalDate.now(getRestaurantOfTheDayZone());
          var picks = refreshDailyLunchPicks(today, guard);
          log.info("Restaurant of the day selected {} picks for {}.",
              picks.getRestaurantIds().size(), today);
          return null;
        });
  }
```

Additional exact changes in the same class:
```java
  private static final java.time.Duration DAILY_PICK_LEASE_DURATION =
      java.time.Duration.ofMinutes(10);
  private final dev.christopherbell.configuration.mongo.lease.ScheduledCollectorCoordinator
      scheduledCollectors;

  DailyLunchPicks refreshDailyLunchPicks(LocalDate pickDate) {
    return refreshDailyLunchPicks(
        pickDate, dev.christopherbell.configuration.mongo.lease.CollectorLeaseGuard.NONE);
  }

  private DailyLunchPicks refreshDailyLunchPicks(
      LocalDate pickDate,
      dev.christopherbell.configuration.mongo.lease.CollectorLeaseGuard guard) {
    var candidates = orderLunchCandidates(getSupportedMetroRestaurants());
    var restaurantIds = candidates.stream()
        .limit(dailyPickCount())
        .map(Restaurant::getId)
        .toList();
    var pick = DailyLunchPicks.builder()
        .id(pickDate.toString())
        .pickDate(pickDate.toString())
        .restaurantIds(restaurantIds)
        .generatedOn(Instant.now())
        .build();
    guard.verifyHeld();
    return dailyLunchPicksRepository.save(pick);
  }
```

Test changes:
- Supply a mocked `ScheduledCollectorCoordinator` in every direct `RestaurantService` construction.
- Make the coordinator test answer execute its `Work` with `CollectorLeaseGuard.NONE`.
- Add one locked outcome test proving no daily-pick save and one ownership-loss test proving the guard runs before `dailyLunchPicksRepository.save`.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest`

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/music/catalog/MusicCatalogReconciler.java`
- Lines: 18-92
- Action: replace

Current:
```java
  @Scheduled(fixedDelayString = "${app.music.scan-interval:5m}")
  public void scheduledReconcile() {
    if (properties.enabled()) reconcile();
  }
```

Proposed:
```java
  @Scheduled(fixedDelayString = "${app.music.scan-interval:5m}")
  public void scheduledReconcile() {
    if (!properties.enabled()) return;
    scheduledCollectors.run("music-catalog-reconcile", SCAN_LEASE_DURATION, guard -> {
      reconcile(guard);
      return null;
    });
  }
```

Additional exact changes in the same class:
```java
  private static final Duration SCAN_LEASE_DURATION = Duration.ofMinutes(30);
  private final dev.christopherbell.configuration.mongo.lease.ScheduledCollectorCoordinator
      scheduledCollectors;

  public MusicReconcileResult reconcile() {
    return reconcile(dev.christopherbell.configuration.mongo.lease.CollectorLeaseGuard.NONE);
  }

  private MusicReconcileResult reconcile(
      dev.christopherbell.configuration.mongo.lease.CollectorLeaseGuard guard) {
    if (!properties.enabled()) return new MusicReconcileResult(0, 0, 0, 0, 0, 0);
    Path root = safeRoot();
    var candidates = discover(root);
    Set<String> presentPaths = new HashSet<>();
    int probed = 0;
    int updated = 0;
    int unchanged = 0;
    int failed = 0;
    for (Path source : candidates) {
      String relative = relative(root, source);
      presentPaths.add(relative);
      MusicFileRevision revision;
      try {
        revision = MusicFileRevision.observe(source);
      } catch (IOException failure) {
        failed++;
        continue;
      }
      var existing = tracks.findByPath(relative).orElse(null);
      boolean changed = existing == null
          || existing.indexStatus() != MusicIndexStatus.READY
          || existing.missingSince() != null
          || !revision.token().equals(existing.observedToken());
      if (!changed || retryDeferred(existing, revision)) {
        unchanged++;
        continue;
      }
      if (probed >= properties.scanBatchSize()) continue;
      probed++;
      try {
        var metadata = probe.probe(source.toAbsolutePath().normalize());
        var artworkRevision = metadata.hasArtwork()
            ? artwork.extract(source, relative, revision).orElse(null)
            : null;
        guard.verifyHeld();
        tracks.save(MusicTrack.indexed(
            existing, relative, revision.token(), metadata, artworkRevision, clock.instant()));
        updated++;
      } catch (dev.christopherbell.configuration.mongo.lease.LeaseOwnershipLostException failure) {
        throw failure;
      } catch (RuntimeException failure) {
        guard.verifyHeld();
        tracks.save(MusicTrack.probeFailed(
            existing, relative, revision.token(), failureCategory(failure), clock.instant()));
        failed++;
      }
    }

    int missing = 0;
    for (MusicTrack track : tracks.findAllByMissingSinceIsNull()) {
      if (!presentPaths.contains(track.path())) {
        guard.verifyHeld();
        tracks.save(track.markMissing(clock.instant()));
        missing++;
      }
    }
    return new MusicReconcileResult(
        candidates.size(), probed, updated, unchanged, missing, failed);
  }
```

Constructor and configuration changes:
- Add `ScheduledCollectorCoordinator scheduledCollectors` before `Clock clock` in the constructor and assign it.
- In `MusicCatalogConfiguration.musicCatalogReconciler` add the coordinator parameter and pass it to the constructor.
- Update direct test construction. Add a contention test proving the scheduled path does not scan, and an ownership-loss test proving no later track write occurs.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.music.catalog.MusicCatalogReconcilerTest`

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/music/metadata/MusicMetadataService.java`
- Lines: 29-170
- Action: replace

Current:
```java
  @Scheduled(fixedDelayString = "${app.music.metadata.cleanup-delay:1h}")
  public void cleanupExpired() {
    for (MusicMetadataEdit edit : edits.findTop100ByExpiresAtBeforeOrderByExpiresAtAsc(clock.instant())) {
      try {
        files.delete(edit.backupFileName());
        edits.delete(edit);
      } catch (RuntimeException ignored) {
        // A later bounded cleanup pass retries the same private artifact.
      }
    }
  }
```

Proposed:
```java
  @Scheduled(fixedDelayString = "${app.music.metadata.cleanup-delay:1h}")
  public void cleanupExpired() {
    scheduledCollectors.run(
        "music-metadata-cleanup", CLEANUP_LEASE_DURATION, guard -> {
          for (MusicMetadataEdit edit
              : edits.findTop100ByExpiresAtBeforeOrderByExpiresAtAsc(clock.instant())) {
            guard.verifyHeld();
            try {
              files.delete(edit.backupFileName());
              guard.verifyHeld();
              edits.delete(edit);
            } catch (RuntimeException ignored) {
              // A later bounded cleanup pass retries the same private artifact.
            }
          }
          return null;
        });
  }
```

Additional exact changes:
```java
  private static final java.time.Duration CLEANUP_LEASE_DURATION =
      java.time.Duration.ofMinutes(10);
  private final dev.christopherbell.configuration.mongo.lease.ScheduledCollectorCoordinator
      scheduledCollectors;
```

- Add the coordinator immediately before `Clock clock` in the explicit constructor and assign it.
- Add the coordinator parameter to `MusicCatalogConfiguration.musicMetadataService` and pass it to the constructor.
- Update `MusicMetadataServiceTest` construction. Add locked-skip, ownership-loss-before-file-delete, and ownership-loss-before-repository-delete cases.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.music.metadata.MusicMetadataServiceTest --tests dev.christopherbell.configuration.SchedulingConfigurationTest`

### Task 5 - Run proportional and runtime verification

Sequence / dependencies:
- Final merge gate after Tasks 1-4.

Implementation notes:
- Required skill: `write-chris-street-style-code` before edits to executable measurement tooling.
- Before-Edit Brief:
  - Behavior: repeatable evidence proves constant query groups and all declared bounds.
  - Invariants: before/after workloads use identical data cardinality; runtime validation uses a non-8080 listener.
  - Boundary/API: tests plus local HTTP/Mongo observation only.
  - Effects and failures: use disposable data; no production listener or persistent data mutation.
  - Tests and evidence: focused suites, `:cbell-lib:test`, `:website:check`, query-count/cardinality/body/bulkhead/lease results, alternate-port VIN and messages flows.

- [ ] Run all focused tests named below.
- [ ] Run `:cbell-lib:test` and `:website:check`.
- [ ] Exercise one- and fifty-conversation data sets and record equal query group counts.
- [ ] Exercise exact-limit/oversized upstream fixtures and eight-permit saturation.
- [ ] Start on an alternate port and verify messages/VIN failure envelopes and scheduled jobs disabled in the smoke profile.
- [ ] Save a Builder test report during authorized execution.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/message/conversation/README.md`
- Lines: after 10
- Action: add

Proposed:
```markdown
- Conversation summaries hydrate peer accounts and aggregate all unread counts in bounded
  batch queries, so Mongo query groups do not grow with the summary page size.
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.message.conversation.*`

## Code Changes

- Add one Mongo aggregation for conversation unread counts and remove per-row count calls.
- Reuse bounded expiring Bucket4j storage for VIN keys with validated cardinality.
- Add JDK-only bounded response reading in `cbell-lib` and migrate five client families.
- Add an eight-permit VIN bulkhead.
- Add the scheduled-writer ownership table and durable leases for WFL daily picks and Music jobs.

## Files and Modules

- Message conversation service/query repository and tests.
- Vehicle VIN limiter/properties/client and tests.
- WFL, Random VIN, robots, Canes outbound clients and tests.
- `cbell-lib` HTTP utility and tests.
- Scheduled WFL/Music services, lease tests, and operations documentation.

## Unit Testing

- Aggregation contents and service query-call counts at 1 and 50 conversations.
- Store cardinality/expiry/concurrency and VIN token charging.
- Reader exact boundary, oversized, interrupted and throwing-stream cases.
- Bulkhead saturation and permit release on success/failure.
- Client-specific status/malformed/oversized translations.
- Lease contention, renewal, ownership loss, and expiry retry.

## Local Testing

- `./gradlew :cbell-lib:test`
- `./gradlew :website:test --tests dev.christopherbell.message.* --tests dev.christopherbell.vehicle.* --tests dev.christopherbell.whatsforlunch.* --tests dev.christopherbell.canesboxtracker.* --tests dev.christopherbell.music.*`
- `./gradlew :website:check`
- Start with disposable Mongo data on port 8092 and run authenticated messages plus valid/invalid/saturated VIN flows.

## Validation

- Conversation Mongo query groups are constant from one to fifty rows.
- VIN bucket count never exceeds 10,000 and expired buckets are removed.
- Every reviewed upstream rejects limit-plus-one without logging response bodies.
- The ninth concurrent VIN upstream admission is rejected and all permits recover.
- Every scheduled writer appears exactly once in the classification and sensitive jobs have durable ownership.

## Rollback or Recovery

- Each task is separately revertible. Restoring the old conversation count method is schema-neutral.
- Reverting the VIN store restores old behavior but should be treated as an emergency rollback because it reopens unbounded growth.
- Bounded-reader failures can be rolled back one client at a time; keep safe status logging that omits bodies.
- Lease additions are schema-compatible; reverting them leaves existing lease documents to expire naturally.

## Risks

- Body limits may be too low for legitimate upstream data. Mitigation: fixtures from current production shapes, explicit per-client bounds, and safe operational metrics before adjustment.
- LRU eviction weakens a local limiter for very high key cardinality. Mitigation: retain global capacity, measure evictions, and defer distributed enforcement until deployment evidence exists.
- A lease shorter than work can permit overlap. Mitigation: renewable guard and loss checks before writes; validation rejects unsafe durations.
- Issue campaign overlap can invalidate ranges. Mitigation: refresh main and preserve accepted issue contracts.

## Completion Criteria

- Spec acceptance criteria 4-6 and the backend portion of criterion 5 pass.
- Focused tests, `:cbell-lib:test`, and `:website:check` pass.
- Alternate-port evidence and bounds are recorded in a Builder test report.
- Authorized PR/CI/merge/production verification and Builder closeout are complete.
