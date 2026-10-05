# Request Limits, Rate Limiting, and API Errors Issues 1139-1141 and 1157 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` inline. Do not dispatch subagents.

**Goal:** Complete issues #1139, #1140, #1141, and #1157 with configurable route-aware request limits, time-expiring bounded rate-limit state, standards-based 429 guidance, and explicit safe service failure exceptions.

**Architecture:** The existing servlet filters remain the single request-boundary owners. A typed request-size property supplies the ordinary-body limit while the existing shared-folder property continues to own upload-chunk size; both 413 and 429 responses use one standard API-envelope writer. Rate-limit buckets move into a small synchronized bounded store with per-entry inactivity expiry tied to the matched rule window, and Bucket4j consumption probes supply remaining/wait metadata. Explicit operational exceptions distinguish temporary persistence failures from internal credential-processing failures while the global advice owns safe public status/code/message mapping.

**Tech Stack:** Java 25, Spring Boot 4.1 configuration properties, Jakarta Servlet, Bucket4j, Jackson, MongoDB, Gradle, JUnit 5, Mockito, AssertJ.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\request-limits-api-errors-1139-1141-1157` on `codex/request-limits-api-errors-1139-1141-1157`.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; do not edit or clean it.
- Only comments by `azurras` may change scope. Issues #1139, #1140, #1141, and #1157 have no comments or attachments.
- Keep the existing filter order: request-size enforcement before rate limiting, then authentication and authorization.
- Oversized JSON and rate-limit responses must use the repository-standard `Response`/`Message` envelope without reflecting request content, client identifiers, exception messages, database details, or secrets.
- Unknown-length and streamed bodies remain bounded while shared-folder upload chunks retain their dedicated typed upload limit.
- Bucket expiry is sliding inactivity expiry, is never shorter than the matched rule window, and the store remains hard-bounded even when all entries are active.
- Translate only explicitly identified operational failures. Unanticipated programming faults continue through the generic 500 handler.
- Verify runtime behavior on a disposable database and non-8080 port before merge. Port 8080 and the live production database remain untouched before guarded deployment.

---

## Document Status

complete

## Objective

Finish Batch 4 of the approved 58-issue campaign in one cohesive pull request with witnessed RED/GREEN evidence, alternate-port JSON acceptance, full regressions, CI, merge, guarded production verification, issue closure, and Builder closeout.

## Goals

- Bind ordinary request-body size from `app.request-size.default-max` with explicit local and production defaults.
- Preserve the existing route-aware shared-folder upload-chunk limit and streaming enforcement.
- Return HTTP 413 with the standard API envelope for oversized JSON, including unknown-length streams.
- Replace access-order-only rate-limit storage with bounded sliding-expiry storage aligned to each rule window.
- Return correct `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` metadata with the standard 429 envelope.
- Replace all ten production `throw new RuntimeException(...)` service wrappers with named API exceptions while retaining original causes for internal logging.
- Map temporary persistence failures to a safe consistent 503 envelope and credential-processing failures to a safe consistent 500 envelope.

## Inputs

- Approved campaign spec: `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md`, Batch 4 lines 132-143.
- Issues: <https://github.com/azurras/christopherbell.dev/issues/1139>, <https://github.com/azurras/christopherbell.dev/issues/1140>, <https://github.com/azurras/christopherbell.dev/issues/1141>, and <https://github.com/azurras/christopherbell.dev/issues/1157>.
- Base: `origin/main` at `965b25bb3e703a2e67a5064d777a9ab1998f26a1`.
- Baseline: `cleanTest check` passed with 1,030 website tests, zero failures, three existing skips, the JavaScript test task, `bootJar`, and sensor runtime verification.
- Current request filter: streaming and shared-upload route limits exist, but the ordinary limit is hard-coded in `SecurityConfig` and 413 is a bare status.
- Current rate-limit filter: endpoint rules and a 10,000-entry LRU cap exist, but entries never expire by time and 429 responses omit standard guidance headers.
- Current explicit generic wrappers: account credential hashing (one), WFL restaurant persistence (four), vehicle CRUD persistence (three), and VIN-create persistence (two).

## Branch

- `codex/request-limits-api-errors-1139-1141-1157` from `origin/main`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\request-limits-api-errors-1139-1141-1157`

## Non-Goals

- Adding distributed/global rate limiting across application instances.
- Changing the trusted-proxy client-IP contract or current endpoint rule capacities.
- Introducing Caffeine, Redis, an npm dependency, or another cache framework.
- Redesigning every controller-specific exception type or masking arbitrary `RuntimeException`/programmer faults.
- Changing shared-folder upload-session semantics, chunk size ownership, authentication, or CSRF behavior.
- Implementing Batch 5 pagination, archive, notification, post, or moderation behavior.

## Assumptions

- Bucket4j `tryConsumeAndReturnRemaining(1)` supplies remaining tokens and refill wait nanoseconds for standards-based response metadata.
- A synchronized access-order `LinkedHashMap` capped at 10,000 entries is adequate because filter access is short and the store owns no blocking I/O.
- Sliding inactivity expiry at the matched rule window is safe: an inactive key receives a fresh bucket after one full rule window, while continuously active keys retain their bucket.
- The existing `SharedFolderProperties.uploadChunk()` value remains the authoritative route-specific upload limit.
- Spring Boot binds `DataSize` values such as `1MB`, `2MB`, and environment overrides before the security filter chain is constructed.
- Temporary Mongo/data-access failures are accurately represented by HTTP 503; password hashing provider failures are internal server failures and remain HTTP 500.

## Open Questions

None. The campaign spec fixes the observable behavior, and current code inspection supplies compatible repository-native boundaries without a new dependency.

## Task Breakdown

### Task 1 - Add RED contracts for configuration, envelopes, expiry, headers, and service failures

Sequence / dependencies:
- First task. Capture focused failures before production edits.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: tests define the missing typed limit, standard 413/429 envelopes, expiring bucket state, rate-limit headers, and explicit operational exception mappings.
  - Invariants: current route matching, trusted client IPs, shared upload sizes, exception causes, and generic programmer-fault handling remain unchanged.
  - Boundary/API: `app.request-size.default-max`, standard `Response` messages, HTTP rate-limit headers, and two named API exceptions are the new contracts.
  - Effects and failures: RED must be caused by missing types/headers/mappings or current bare/generic behavior, not a broken test harness.
  - Tests and evidence: run only the focused classes first and preserve the failure summaries in the final test report.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/configuration/RequestSizeLimitFilterTest.java`
- Lines: 22-131
- Action: replace

Current:
```java
public class RequestSizeLimitFilterTest {
  @Test
  public void rejectsLargeRequest() throws ServletException, IOException {
    RequestSizeLimitFilter filter = new RequestSizeLimitFilter(10);
    MockHttpServletRequest request = new MockHttpServletRequest();
    request.setContent(new byte[20]);
    MockHttpServletResponse response = new MockHttpServletResponse();
    FilterChain chain = mock(FilterChain.class);

    filter.doFilter(request, response, chain);

    assertEquals(413, response.getStatus());
    verify(chain, times(0)).doFilter(request, response);
  }
}
```

Proposed:
```java
class RequestSizeLimitFilterTest {
  private final ApiErrorResponseWriter errors =
      new ApiErrorResponseWriter(new ObjectMapper());

  @Test
  void oversizedJsonUsesStandardEnvelopeWithoutInvokingTheChain() throws Exception {
    var filter = new RequestSizeLimitFilter(
        new RequestSizeProperties(DataSize.ofBytes(10)), DataSize.ofBytes(8), errors);
    var request = new MockHttpServletRequest("POST", "/api/example");
    request.setContentType(MediaType.APPLICATION_JSON_VALUE);
    request.setContent(new byte[20]);
    var response = new MockHttpServletResponse();
    var chain = mock(FilterChain.class);

    filter.doFilter(request, response, chain);

    assertThat(response.getStatus()).isEqualTo(413);
    assertThat(response.getContentAsString())
        .contains("\"success\":false", "REQUEST_TOO_LARGE")
        .doesNotContain(new String(request.getContent(), StandardCharsets.UTF_8));
    verifyNoInteractions(chain);
  }

  @Test
  void unknownLengthJsonAndUploadChunksRemainIndependentlyBounded() throws Exception {
    var filter = new RequestSizeLimitFilter(
        new RequestSizeProperties(DataSize.ofBytes(10)), DataSize.ofBytes(8), errors);
    assertStreamingStatus(filter, "POST", "/api/example", 11, 413);
    assertStreamingStatus(
        filter, "PUT", "/api/shared-folder/2026-07-17/uploads/id/chunks/0", 8, 200);
    assertStreamingStatus(
        filter, "PUT", "/api/shared-folder/2026-07-17/uploads/id/chunks/0", 9, 413);
  }
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.RequestSizeLimitFilterTest`
- Expected RED: `RequestSizeProperties` and `ApiErrorResponseWriter` do not exist and the filter has no typed constructor or standard body.

#### Code Edit 1.2
- File: `website/src/test/java/dev/christopherbell/configuration/filter/RateLimitBucketStoreTest.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class RateLimitBucketStoreTest {
  @Test
  void inactiveBucketsExpireAtTheirRuleWindowWhileRecentBucketsRemain() {
    var now = new AtomicLong();
    var store = new RateLimitBucketStore(10, now::get);
    var first = store.getOrCreate("rule:first", Duration.ofSeconds(5), this::bucket);
    now.set(Duration.ofSeconds(4).toNanos());
    assertThat(store.getOrCreate("rule:first", Duration.ofSeconds(5), this::bucket))
        .isSameAs(first);
    store.getOrCreate("rule:second", Duration.ofSeconds(5), this::bucket);
    now.set(Duration.ofSeconds(9).toNanos());

    store.getOrCreate("rule:third", Duration.ofSeconds(5), this::bucket);

    assertThat(store.contains("rule:first")).isFalse();
    assertThat(store.contains("rule:second")).isFalse();
    assertThat(store.size()).isEqualTo(1);
  }

  @Test
  void activeCardinalityNeverExceedsTheConfiguredMaximum() {
    var store = new RateLimitBucketStore(2, () -> 0L);
    store.getOrCreate("one", Duration.ofMinutes(1), this::bucket);
    store.getOrCreate("two", Duration.ofMinutes(1), this::bucket);
    store.getOrCreate("three", Duration.ofMinutes(1), this::bucket);
    assertThat(store.size()).isEqualTo(2);
  }
}
```

Verification:
- Expected RED: `RateLimitBucketStore` does not exist.

#### Code Edit 1.3
- File: `website/src/test/java/dev/christopherbell/configuration/RateLimitFilterTest.java`
- Lines: 28-51
- Action: replace

Current:
```java
@Test
public void testRateLimitExceeded() throws ServletException, IOException {
  Supplier<Bucket> supplier = () -> Bucket4j.builder()
      .addLimit(Bandwidth.simple(1, Duration.ofMinutes(1)))
      .build();
  RateLimitFilter filter = new RateLimitFilter(supplier, new ClientIpResolver(new ClientIpProperties()));
  MockHttpServletRequest request = new MockHttpServletRequest();
  request.setRemoteAddr("1.1.1.1");
  MockHttpServletResponse response = new MockHttpServletResponse();
  FilterChain chain = mock(FilterChain.class);
  filter.doFilter(request, response, chain);
  MockHttpServletResponse response2 = new MockHttpServletResponse();
  filter.doFilter(request, response2, chain);
  assertEquals(429, response2.getStatus());
}
```

Proposed:
```java
@Test
void exhaustedBucketReturnsStandardEnvelopeAndRateLimitGuidance() throws Exception {
  var properties = new RateLimitProperties();
  properties.setRules(List.of(rule(
      "test", 1, Duration.ofSeconds(30), List.of("POST"), List.of("/api/test"))));
  var filter = new RateLimitFilter(
      new ClientIpResolver(new ClientIpProperties()),
      properties,
      new ApiErrorResponseWriter(new ObjectMapper()),
      Clock.fixed(Instant.parse("2026-07-25T12:00:00Z"), ZoneOffset.UTC));
  var request = request("POST", "/api/test");
  var chain = mock(FilterChain.class);
  filter.doFilter(request, new MockHttpServletResponse(), chain);
  var denied = new MockHttpServletResponse();

  filter.doFilter(request, denied, chain);

  assertThat(denied.getStatus()).isEqualTo(429);
  assertThat(denied.getHeader("Retry-After")).isEqualTo("30");
  assertThat(denied.getHeader("X-RateLimit-Limit")).isEqualTo("1");
  assertThat(denied.getHeader("X-RateLimit-Remaining")).isEqualTo("0");
  assertThat(denied.getHeader("X-RateLimit-Reset")).isEqualTo("1784980830");
  assertThat(denied.getContentAsString())
      .contains("\"success\":false", "RATE_LIMITED");
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.RateLimitFilterTest --tests dev.christopherbell.configuration.filter.RateLimitBucketStoreTest`
- Expected RED: the store and injected clock/writer constructor do not exist and current responses omit every asserted header.

#### Code Edit 1.4
- File: `cbell-lib/src/test/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandlerTest.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class ControllerExceptionHandlerTest {
  private final ControllerExceptionHandler handler = new ControllerExceptionHandler();

  @Test
  void serviceUnavailableUsesSafeConsistentEnvelopeAndPreservesInternalCause() {
    var cause = new IllegalStateException("database host secret");
    var exception = new ServiceUnavailableException("restaurant save failed", cause);

    var response = handler.handleServiceUnavailableException(exception);

    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.SERVICE_UNAVAILABLE);
    assertThat(response.getBody().getMessages().getFirst().getCode())
        .isEqualTo("SERVICE_UNAVAILABLE");
    assertThat(response.getBody().getMessages().getFirst().getDescription())
        .doesNotContain("database", "secret", "restaurant");
    assertThat(exception.getCause()).isSameAs(cause);
  }

  @Test
  void internalServiceFailureUsesGenericInternalEnvelope() {
    var response = handler.handleInternalServiceException(
        new InternalServiceException("credential hashing failed", new Exception("provider")));
    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR);
    assertThat(response.getBody().getMessages().getFirst().getCode())
        .isEqualTo("INTERNAL_SERVER_ERROR");
  }
}
```

Verification:
- `./gradlew :cbell-lib:test --tests dev.christopherbell.libs.api.controller.ControllerExceptionHandlerTest`
- Expected RED: both named exceptions and handler methods are absent.

#### Code Edit 1.5
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- Lines: 140-157
- Action: replace

Current:
```java
@Test
@DisplayName("Wraps DataAccessException into RuntimeException with message")
public void testCreateRestaurant_whenDataAccessFails_ThrowsRuntimeException() {
  when(restaurantRepository.save(eq(restaurant))).thenThrow(new DataAccessException("boom") {});
  var ex = assertThrows(RuntimeException.class, () -> restaurantService.createRestaurant(request));
  assertTrue(ex.getMessage().contains("Failed to save restaurant"));
}
```

Proposed:
```java
@Test
@DisplayName("Translates persistence failure into ServiceUnavailableException")
void createRestaurantWhenDataAccessFailsPreservesCauseInNamedException() {
  var failure = new DataAccessResourceFailureException("database-secret");
  when(restaurantRepository.save(eq(restaurant))).thenThrow(failure);
  var exception = assertThrows(
      ServiceUnavailableException.class,
      () -> restaurantService.createRestaurant(request));
  assertThat(exception.getCause()).isSameAs(failure);
}
```

Verification:
- Add equivalent create/delete/update and vehicle CRUD/VIN persistence partitions, plus an account credential-provider failure partition using scoped `mockStatic(PasswordUtil.class)`.
- Run `./gradlew :website:test --tests dev.christopherbell.account.AccountServiceTest --tests dev.christopherbell.vehicle.VehicleServiceTest --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest`.
- Expected RED: current paths return generic `RuntimeException` and named exceptions are absent.

### Task 2 - Implement typed request-size configuration and standard 413 envelopes

Sequence / dependencies:
- Runs after Task 1 records RED failures.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: ordinary JSON bodies use a typed environment-aware limit, shared upload chunks retain their own limit, and known/unknown-length overflows return a standard 413 envelope.
  - Invariants: filters remain before rate limiting; non-JSON upload streams do not echo content; exact-size bodies pass; size-plus-one fails.
  - Boundary/API: `app.request-size.default-max`, `APP_REQUEST_SIZE_DEFAULT_MAX`, `SharedFolderProperties.uploadChunk()`, and `REQUEST_TOO_LARGE` define the boundary.
  - Effects and failures: enforcement reads at most limit-plus-one bytes; envelope writing occurs only while the response is uncommitted; no database or downstream controller call occurs for known oversize content.
  - Tests and evidence: focused property/filter tests and an alternate-port oversized login request prove binding and response shape.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/configuration/RequestSizeProperties.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
package dev.christopherbell.configuration;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.util.unit.DataSize;

/** Typed ordinary-request body limit; feature-owned streaming limits remain separate. */
@ConfigurationProperties("app.request-size")
public record RequestSizeProperties(DataSize defaultMax) {
  private static final DataSize DEFAULT_MAX = DataSize.ofMegabytes(1);

  public RequestSizeProperties {
    defaultMax = defaultMax == null ? DEFAULT_MAX : defaultMax;
    if (defaultMax.toBytes() <= 0) {
      throw new IllegalArgumentException("app.request-size.default-max must be positive");
    }
  }
}
```

Verification:
- Add binding tests for missing default, `128KB`, zero, and negative values.

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/configuration/filter/ApiErrorResponseWriter.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
package dev.christopherbell.configuration.filter;

import dev.christopherbell.libs.api.model.Message;
import dev.christopherbell.libs.api.model.Response;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import org.springframework.http.MediaType;
import tools.jackson.databind.ObjectMapper;

/** Serializes filter-owned failures through the same envelope as controller advice. */
public final class ApiErrorResponseWriter {
  private final ObjectMapper objectMapper;

  public ApiErrorResponseWriter(ObjectMapper objectMapper) {
    this.objectMapper = objectMapper;
  }

  public void write(HttpServletResponse response, int status, String code, String description)
      throws IOException {
    if (response.isCommitted()) {
      return;
    }
    response.resetBuffer();
    response.setStatus(status);
    response.setContentType(MediaType.APPLICATION_JSON_VALUE);
    var body = Response.builder()
        .success(false)
        .messages(List.of(Message.builder().code(code).description(description).build()))
        .build();
    objectMapper.writeValue(response.getOutputStream(), body);
  }
}
```

Verification:
- Unit test status, media type, standard envelope, and committed-response no-op.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/configuration/filter/RequestSizeLimitFilter.java`
- Lines: 18-147
- Action: replace

Current:
```java
public class RequestSizeLimitFilter extends OncePerRequestFilter {
  private final long maxSizeBytes;
  private final long sharedUploadChunkMaxSizeBytes;
  public RequestSizeLimitFilter(long maxSizeBytes, long sharedUploadChunkMaxSizeBytes) {
    this.maxSizeBytes = maxSizeBytes;
    this.sharedUploadChunkMaxSizeBytes = sharedUploadChunkMaxSizeBytes;
  }
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain filterChain) throws ServletException, IOException {
    long limit = isUploadChunk(request) ? sharedUploadChunkMaxSizeBytes : maxSizeBytes;
    if (request.getContentLengthLong() > limit) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
      return;
    }
    try {
      filterChain.doFilter(new SizeLimitedRequestWrapper(request, limit), response);
    } catch (RequestPayloadTooLargeException e) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
    }
  }
}
```

Proposed:
```java
public class RequestSizeLimitFilter extends OncePerRequestFilter {
  private static final String ERROR_CODE = "REQUEST_TOO_LARGE";
  private static final String ERROR_MESSAGE = "The request body exceeds the allowed size.";
  private final long defaultMaxBytes;
  private final long sharedUploadChunkMaxBytes;
  private final ApiErrorResponseWriter errors;

  public RequestSizeLimitFilter(
      RequestSizeProperties properties,
      DataSize sharedUploadChunkMax,
      ApiErrorResponseWriter errors) {
    this.defaultMaxBytes = properties.defaultMax().toBytes();
    this.sharedUploadChunkMaxBytes = sharedUploadChunkMax.toBytes();
    this.errors = errors;
  }

  @Override
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain chain) throws ServletException, IOException {
    long limit = isUploadChunk(request) ? sharedUploadChunkMaxBytes : defaultMaxBytes;
    if (request.getContentLengthLong() > limit) {
      reject(request, response);
      return;
    }
    try {
      chain.doFilter(new SizeLimitedRequestWrapper(request, limit), response);
    } catch (RequestPayloadTooLargeException failure) {
      reject(request, response);
    }
  }

  private void reject(HttpServletRequest request, HttpServletResponse response) throws IOException {
    if (MediaType.APPLICATION_JSON_VALUE.equalsIgnoreCase(request.getContentType())) {
      errors.write(response, HttpStatus.PAYLOAD_TOO_LARGE.value(), ERROR_CODE, ERROR_MESSAGE);
    } else if (!response.isCommitted()) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
    }
  }
}
```

Verification:
- Preserve the existing limit-plus-one stream wrapper and route regex; replace only configuration/envelope ownership around it.
- Focused request-size unit tests pass.

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 42-229
- Action: replace

Current:
```java
@EnableConfigurationProperties({
    BrowserSecurityProperties.class, ClientIpProperties.class, RateLimitProperties.class,
    SharedFolderProperties.class})
public RequestSizeLimitFilter requestSizeLimitFilter(SharedFolderProperties sharedFolderProperties) {
  return new RequestSizeLimitFilter(1_000_000L, sharedFolderProperties.uploadChunk().toBytes());
}
```

Proposed:
```java
@EnableConfigurationProperties({
    BrowserSecurityProperties.class, ClientIpProperties.class, RateLimitProperties.class,
    RequestSizeProperties.class, SharedFolderProperties.class})
public RequestSizeLimitFilter requestSizeLimitFilter(
    RequestSizeProperties requestSizeProperties,
    SharedFolderProperties sharedFolderProperties,
    ObjectMapper objectMapper) {
  return new RequestSizeLimitFilter(
      requestSizeProperties,
      sharedFolderProperties.uploadChunk(),
      new ApiErrorResponseWriter(objectMapper));
}
```

Verification:
- `SecurityConfigTest` proves the typed bean is wired and the filter remains before rate limiting.

#### Code Edit 2.5
- File: `website/src/main/resources/application.yml`
- Lines: after 76
- Action: add

Current:
```yaml
app:
  jwt:
    secret: ${APP_JWT_SECRET:local-development-jwt-secret-change-me-at-least-32-bytes}
```

Proposed:
```yaml
app:
  jwt:
    secret: ${APP_JWT_SECRET:local-development-jwt-secret-change-me-at-least-32-bytes}
  request-size:
    default-max: ${APP_REQUEST_SIZE_DEFAULT_MAX:1MB}
```

Verification:
- Add `application-local.yml` override `${APP_REQUEST_SIZE_DEFAULT_MAX:2MB}` and `application-prod.yml` override `${APP_REQUEST_SIZE_DEFAULT_MAX:1MB}`; binding test asserts both defaults and an environment override.

### Task 3 - Implement bounded inactivity expiry and standards-based rate-limit responses

Sequence / dependencies:
- Runs after Task 2 because it reuses `ApiErrorResponseWriter`.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: rate-limit entries expire after one inactive rule window, total state stays bounded, and exhausted responses include correct guidance and the standard envelope.
  - Invariants: rule ordering, path/method matching, trusted proxy resolution, capacities, and Bucket4j token semantics stay unchanged.
  - Boundary/API: `rate-limit.max-buckets`, each `Rule.window`, Bucket4j `ConsumptionProbe`, and the four response headers define the boundary.
  - Effects and failures: synchronization is local and bounded; expiry uses monotonic nanoseconds; reset headers use UTC epoch seconds; invalid non-positive rules fail configuration.
  - Tests and evidence: deterministic fake-ticker store tests, real Bucket4j filter tests, and alternate-port exhausted-login requests prove behavior.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitBucketStore.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
package dev.christopherbell.configuration.filter;

import io.github.bucket4j.Bucket;
import java.time.Duration;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.LongSupplier;
import java.util.function.Supplier;

/** Bounded access-order bucket state with sliding inactivity expiry. */
public final class RateLimitBucketStore {
  private final int maximumSize;
  private final LongSupplier ticker;
  private final LinkedHashMap<String, Entry> entries = new LinkedHashMap<>(128, 0.75f, true);

  public RateLimitBucketStore(int maximumSize, LongSupplier ticker) {
    if (maximumSize <= 0) throw new IllegalArgumentException("maximumSize must be positive");
    this.maximumSize = maximumSize;
    this.ticker = ticker;
  }

  public synchronized Bucket getOrCreate(
      String key, Duration inactivityWindow, Supplier<Bucket> factory) {
    long now = ticker.getAsLong();
    evictExpired(now);
    var entry = entries.get(key);
    if (entry == null) {
      entry = new Entry(factory.get(), expiresAt(now, inactivityWindow));
      entries.put(key, entry);
      evictEldest();
    } else {
      entry.expiresAtNanos = expiresAt(now, inactivityWindow);
    }
    return entry.bucket;
  }

  private void evictExpired(long now) {
    Iterator<Map.Entry<String, Entry>> iterator = entries.entrySet().iterator();
    while (iterator.hasNext()) {
      if (iterator.next().getValue().expiresAtNanos <= now) iterator.remove();
    }
  }

  private void evictEldest() {
    while (entries.size() > maximumSize) entries.pollFirstEntry();
  }
}
```

Verification:
- Use saturating addition for `expiresAt` so overflow becomes `Long.MAX_VALUE`; expose package-private `size()`/`contains()` only for focused tests.
- Store tests pass for expiry, touch, exact boundary, overflow, and maximum size.

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/configuration/RateLimitProperties.java`
- Lines: 10-99
- Action: replace

Current:
```java
@ConfigurationProperties(prefix = "rate-limit")
@Data
public class RateLimitProperties {
  private List<Rule> rules = defaultRules();
  @Data
  public static class Rule {
    private String name = "default";
    private long capacity = 10_000;
    private Duration window = Duration.ofMinutes(1);
  }
}
```

Proposed:
```java
@ConfigurationProperties(prefix = "rate-limit")
@Validated
@Data
public class RateLimitProperties {
  @Min(1)
  private int maxBuckets = 10_000;
  @Valid
  @NotEmpty
  private List<Rule> rules = defaultRules();

  @Data
  public static class Rule {
    @NotBlank private String name = "default";
    @Min(1) private long capacity = 10_000;
    @NotNull private Duration window = Duration.ofMinutes(1);
    private List<String> methods = new ArrayList<>();
    private List<String> paths = new ArrayList<>(List.of("/**"));

    @AssertTrue(message = "rate-limit rule window must be positive")
    public boolean isWindowPositive() {
      return window != null && !window.isZero() && !window.isNegative();
    }
  }
}
```

Verification:
- Add binder tests for `max-buckets=2`, zero capacity, zero/negative window, blank name, and default rules.

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitFilter.java`
- Lines: 26-174
- Action: replace

Current:
```java
private static final int MAX_BUCKETS = 10_000;
private static final String RATE_LIMIT_BODY =
    "{\"code\":\"RATE_LIMITED\",\"message\":\"Too many requests. Try again later.\"}";
private final Map<String, Bucket> buckets = Collections.synchronizedMap(
    new LinkedHashMap<>(128, 0.75f, true));
Bucket bucket = buckets.computeIfAbsent(bucketKey(rule, ip), key -> newBucket(rule));
if (bucket.tryConsume(1)) {
  filterChain.doFilter(request, response);
} else {
  response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
  response.setContentType("application/json");
  response.getWriter().write(RATE_LIMIT_BODY);
}
```

Proposed:
```java
private static final String RATE_LIMITED = "RATE_LIMITED";
private static final String RATE_LIMIT_MESSAGE = "Too many requests. Try again later.";
private final RateLimitBucketStore buckets;
private final ApiErrorResponseWriter errors;
private final Clock clock;

Bucket bucket = buckets.getOrCreate(
    bucketKey(rule, ip), rule.getWindow(), () -> newBucket(rule));
var probe = bucket.tryConsumeAndReturnRemaining(1);
writeHeaders(response, rule, probe);
if (probe.isConsumed()) {
  filterChain.doFilter(request, response);
  return;
}
errors.write(
    response,
    HttpStatus.TOO_MANY_REQUESTS.value(),
    RATE_LIMITED,
    RATE_LIMIT_MESSAGE);

private void writeHeaders(
    HttpServletResponse response,
    RateLimitProperties.Rule rule,
    ConsumptionProbe probe) {
  long retrySeconds = probe.isConsumed()
      ? 0
      : Math.max(1, ceilSeconds(probe.getNanosToWaitForRefill()));
  long resetSeconds = clock.instant().getEpochSecond()
      + (probe.isConsumed() ? ceilSeconds(rule.getWindow().toNanos()) : retrySeconds);
  response.setHeader("X-RateLimit-Limit", Long.toString(rule.getCapacity()));
  response.setHeader("X-RateLimit-Remaining", Long.toString(probe.getRemainingTokens()));
  response.setHeader("X-RateLimit-Reset", Long.toString(resetSeconds));
  if (!probe.isConsumed()) response.setHeader("Retry-After", Long.toString(retrySeconds));
}
```

Verification:
- Preserve existing convenience constructors for current focused tests, but have every constructor delegate to one store/writer/clock boundary.
- All existing route/trusted-proxy tests plus new expiry/header/envelope tests pass.

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 180-189
- Action: replace

Current:
```java
@Bean
public RateLimitFilter rateLimitFilter(
    ClientIpResolver clientIpResolver,
    RateLimitProperties rateLimitProperties) {
  return new RateLimitFilter(clientIpResolver, rateLimitProperties);
}
```

Proposed:
```java
@Bean
public RateLimitFilter rateLimitFilter(
    ClientIpResolver clientIpResolver,
    RateLimitProperties rateLimitProperties,
    ObjectMapper objectMapper) {
  return new RateLimitFilter(
      clientIpResolver,
      rateLimitProperties,
      new ApiErrorResponseWriter(objectMapper),
      Clock.systemUTC());
}
```

Verification:
- Security configuration tests and full configuration tests pass without duplicate beans.

### Task 4 - Replace explicit generic service wrappers with safe named API exceptions

Sequence / dependencies:
- Runs after Task 1 RED contracts; independent of Tasks 2-3 production code but completed before full verification.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: known persistence outages consistently return safe 503 envelopes; account credential-provider failures return the generic safe 500 envelope; original causes remain attached internally.
  - Invariants: duplicate conflicts remain 409, not-found remains 404, invalid input remains 400, and unanticipated runtime/programmer failures remain generic 500.
  - Boundary/API: `ServiceUnavailableException`, `InternalServiceException`, and global controller advice are the only new public failure taxonomy.
  - Effects and failures: service methods translate only `DataAccessException` or named checked credential exceptions; handler bodies never expose exception messages or causes.
  - Tests and evidence: exception/handler tests plus every currently wrapped account/restaurant/vehicle operation prove type, status, code, message safety, and cause preservation.

#### Code Edit 4.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/exception/ServiceUnavailableException.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
package dev.christopherbell.libs.api.exception;

/** Operational dependency failure that may succeed when retried later. */
public class ServiceUnavailableException extends RuntimeException {
  public ServiceUnavailableException(String message, Throwable cause) {
    super(message, cause);
  }
}
```

Verification:
- Exception test proves message and cause constructors without adding mutable state.

#### Code Edit 4.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/exception/InternalServiceException.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
package dev.christopherbell.libs.api.exception;

/** Recognizable internal operation failure that must remain a safe HTTP 500. */
public class InternalServiceException extends RuntimeException {
  public InternalServiceException(String message, Throwable cause) {
    super(message, cause);
  }
}
```

Verification:
- Exception test proves message and cause constructors.

#### Code Edit 4.3
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`
- Lines: 22-176
- Action: replace

Current:
```java
private static final String INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR";
@ExceptionHandler(Exception.class)
public ResponseEntity<Response<?>> handleGenericException(Exception e) {
  return errorResponse(
      INTERNAL_SERVER_ERROR,
      "An unexpected error occurred. Please try again later.",
      HttpStatus.INTERNAL_SERVER_ERROR);
}
```

Proposed:
```java
private static final String INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR";
private static final String SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE";
private static final String INTERNAL_MESSAGE =
    "An unexpected error occurred. Please try again later.";
private static final String UNAVAILABLE_MESSAGE =
    "The service is temporarily unavailable. Please try again later.";

@ExceptionHandler(ServiceUnavailableException.class)
public ResponseEntity<Response<?>> handleServiceUnavailableException(
    ServiceUnavailableException exception) {
  log.error(SERVICE_UNAVAILABLE, exception);
  return errorResponse(SERVICE_UNAVAILABLE, UNAVAILABLE_MESSAGE, HttpStatus.SERVICE_UNAVAILABLE);
}

@ExceptionHandler(InternalServiceException.class)
public ResponseEntity<Response<?>> handleInternalServiceException(
    InternalServiceException exception) {
  log.error(INTERNAL_SERVER_ERROR, exception);
  return errorResponse(INTERNAL_SERVER_ERROR, INTERNAL_MESSAGE, HttpStatus.INTERNAL_SERVER_ERROR);
}
```

Verification:
- Existing generic/framework/resource handler tests remain unchanged; new handler tests prove safe mapping and retained causes.

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/account/AccountService.java`
- Lines: 97-99
- Action: replace

Current:
```java
} catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
  throw new RuntimeException("Can't create account due to password issues", e);
}
```

Proposed:
```java
} catch (NoSuchAlgorithmException | InvalidKeySpecException failure) {
  throw new InternalServiceException("Account credential hashing failed", failure);
}
```

Verification:
- Account service test uses scoped static mocking to force `InvalidKeySpecException`, asserts the named type/cause, and verifies no repository save.

#### Code Edit 4.5
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 112-754
- Action: replace

Current:
```java
} catch (DataAccessException e) {
  throw new RuntimeException("Failed to save restaurant", e);
}
```

Proposed:
```java
} catch (DataAccessException failure) {
  throw new ServiceUnavailableException("Restaurant persistence operation failed", failure);
}
```

Verification:
- Apply the same type to create, delete, delete-today, and update persistence catches; preserve duplicate-key conflict handling before the broader catch.
- Restaurant service tests assert each operation type and original cause.

#### Code Edit 4.6
- File: `website/src/main/java/dev/christopherbell/vehicle/core/VehicleCrudService.java`
- Lines: 39-124
- Action: replace

Current:
```java
} catch (DataAccessException e) {
  throw new RuntimeException("Failed to save vehicle", e);
}
```

Proposed:
```java
} catch (DataAccessException failure) {
  throw new ServiceUnavailableException("Vehicle persistence operation failed", failure);
}
```

Verification:
- Apply to create, delete, and update while preserving duplicate-key conflict handling.
- Vehicle service tests cover all three paths and cause identity.

#### Code Edit 4.7
- File: `website/src/main/java/dev/christopherbell/vehicle/vin/VehicleVinService.java`
- Lines: 49-81
- Action: replace

Current:
```java
} catch (DataAccessException e) {
  throw new RuntimeException("Failed to save vehicles", e);
}
```

Proposed:
```java
} catch (DataAccessException failure) {
  throw new ServiceUnavailableException("VIN vehicle persistence operation failed", failure);
}
```

Verification:
- Apply to single and batch VIN creation while preserving duplicate-key conflict handling.
- Vehicle service tests cover both paths and cause identity.

#### Code Edit 4.8
- File: `website/src/main/java/dev/christopherbell/configuration/README.md`
- Lines: 23-33
- Action: replace

Current:
```markdown
- Rate limiting and request size protection filters under `filter`.
- `RateLimitProperties` binds ordered `rate-limit.rules` so environments can tune per-endpoint capacity and window settings.
```

Proposed:
```markdown
- `app.request-size.default-max` owns the ordinary JSON/body limit; shared-folder upload chunks keep their feature-owned typed limit. Known and streamed JSON overflow returns the standard 413 envelope.
- `RateLimitProperties` binds ordered rules plus a hard bucket cap. Bucket state expires after one inactive matched-rule window and remains access-order bounded.
- Limited responses use the standard API envelope with `Retry-After`, limit, remaining, and epoch reset headers.
- Explicit operational dependency failures map to a safe 503 envelope; internal credential-processing failures map to a safe 500 envelope without exposing causes.
```

Verification:
- Update account, vehicle, and WFL READMEs with their operational-error mapping and preserve existing feature descriptions.

### Task 5 - Run alternate-port acceptance, full verification, review, and publication

Sequence / dependencies:
- Runs after Tasks 2-4 are GREEN.

Implementation notes:
- No production code edits are planned in this task; if verification exposes a defect, return to the owning task, invoke `chris-street-style`, add a RED regression, and update this plan if file scope changes materially.
- Build the production-profile JAR and start it on port `8090` against an exact disposable Mongo database named `christopherbell_request_limits_test_YYYYMMDDHHMMSS`.
- Supply all valid production settings, `APP_REQUEST_SIZE_DEFAULT_MAX=128B`, mail disabled, and a first-match login rate rule with capacity 1 and window 5 seconds through command-line properties.
- Send one 129-byte JSON login request and assert HTTP 413, `REQUEST_TOO_LARGE`, standard `success=false`, no echoed body, and no authentication call side effect.
- Send an unknown-length chunked 129-byte JSON request through `HttpClient` and assert the same 413 envelope.
- Restart with a larger body limit, send two small login requests from the same local client, and assert the second returns 429 with `Retry-After: 5`, limit 1, remaining 0, reset epoch near now plus five seconds, and `RATE_LIMITED` standard envelope.
- Confirm a different rule/client path still reaches the application and readiness remains 200.
- Stop only the recorded candidate PID, prove port 8090 is free, validate the disposable database name against `^christopherbell_request_limits_test_[0-9]{14}$`, drop only that database, prove it is absent, and recheck live production port 8080/PID/HTTP 200.

Verification:
- `./gradlew :cbell-lib:test --tests '*ControllerExceptionHandlerTest' --tests '*ServiceUnavailableExceptionTest' --tests '*InternalServiceExceptionTest'`
- `./gradlew :website:test --tests dev.christopherbell.configuration.RequestSizeLimitFilterTest --tests dev.christopherbell.configuration.RequestSizePropertiesTest --tests dev.christopherbell.configuration.RateLimitFilterTest --tests dev.christopherbell.configuration.RateLimitPropertiesTest --tests dev.christopherbell.configuration.filter.RateLimitBucketStoreTest`
- `./gradlew :website:test --tests dev.christopherbell.account.AccountServiceTest --tests dev.christopherbell.vehicle.VehicleServiceTest --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest`
- `./gradlew cleanTest check --no-daemon --console=plain`
- `git diff --check`
- Save and validate the Builder test report after the runtime steps.
- Review the staged diff for secret reflection, arbitrary exception masking, invalid header arithmetic, expiry overflow, unbounded state, filter order, and unrelated files.
- Commit/push the spoke branch, open one PR closing all four issues, wait for Ubuntu/macOS/Windows, Dependency Review, and CodeQL, address in-scope failures, squash merge, verify guarded production deployment, then close/reconcile each issue.

## Code Changes

- `website/src/test/java/dev/christopherbell/configuration/RequestSizeLimitFilterTest.java`: replace and extend request-limit contracts.
- `website/src/test/java/dev/christopherbell/configuration/filter/RateLimitBucketStoreTest.java`: add deterministic expiry/cardinality contracts.
- `website/src/test/java/dev/christopherbell/configuration/RateLimitFilterTest.java`: add standard 429 envelope/header contracts.
- `cbell-lib/src/test/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandlerTest.java`: add safe named-exception mapping contracts.
- Account, vehicle, and WFL service tests: replace generic-wrapper expectations and cover every translated operation.
- `RequestSizeProperties.java`: add typed ordinary-body configuration.
- `ApiErrorResponseWriter.java`: add shared standard filter-envelope serialization.
- `RequestSizeLimitFilter.java`: replace hard-coded ownership and bare JSON 413 behavior.
- `SecurityConfig.java`: wire typed request/rate limits, shared writer, and UTC clock.
- `application.yml`, `application-local.yml`, `application-prod.yml`: add documented environment-specific ordinary-body defaults.
- `RateLimitBucketStore.java`: add bounded sliding-inactivity state.
- `RateLimitProperties.java`: validate rules and expose the hard bucket cap.
- `RateLimitFilter.java`: use consumption probes, expiry store, standard envelope, and response headers.
- `ServiceUnavailableException.java` and `InternalServiceException.java`: add named API exception taxonomy.
- `ControllerExceptionHandler.java`: add safe 503/500 mappings.
- Account, WFL restaurant, and vehicle service classes: replace ten explicit generic wrappers.
- Configuration/account/vehicle/WFL READMEs: document the resulting contracts.

## Files and Modules

- `cbell-lib`: shared API exceptions, controller advice, and focused tests.
- `website/configuration`: typed settings, servlet filters, store, security wiring, config tests, and documentation.
- `website/account`: account credential hashing translation and test.
- `website/vehicle`: CRUD/VIN persistence translations and tests.
- `website/whatsforlunch`: restaurant persistence translations and tests.
- Builder: implementation plan, test report, spoke review/update, campaign ledger, and session memory.

## Unit Testing

- Request size: default/override/invalid binding; known length; unknown length; exact boundary; size-plus-one; ordinary JSON; upload chunk; standard envelope; no content reflection; committed response.
- Rate-limit store: exact expiry boundary; sliding touch; different windows; hard maximum; monotonic overflow saturation.
- Rate-limit filter: allowed/denied probes; all required headers; ceil-to-seconds behavior; safe reset epoch; standard envelope; route ordering; trusted/untrusted proxy separation.
- API exceptions: constructor/cause preservation; 503 mapping; safe 500 mapping; generic programmer failure remains generic 500.
- Services: account credential checked failure; restaurant create/delete/delete-today/update data access; vehicle create/delete/update and VIN single/batch data access; duplicate conflicts remain unchanged.

## Local Testing

- Use port 8090 only and a timestamped disposable Mongo database.
- Record exact candidate PIDs before stop operations and verify port ownership.
- Exercise both known-length and chunked/unknown-length JSON over HTTP.
- Exercise an exhausted five-second rate bucket and capture every header/body/status.
- Confirm readiness and one unrelated request path remain healthy.
- Clean up only the validated candidate and disposable database, then prove production port 8080 was unaffected.

## Validation

- All focused RED tests fail for the expected missing behavior before production edits.
- All focused tests pass after implementation.
- Full Java/JavaScript/build checks pass with no new skip or failure.
- Alternate-port HTTP returns standard safe 413 and 429 envelopes with correct limits and retry/reset metadata.
- No request content, client IP, database detail, or internal exception message appears in public bodies.
- Every explicit production `throw new RuntimeException(...)` wrapper identified at baseline is removed; test-only utility wrappers remain out of scope.
- Required GitHub checks pass, the PR merges, all four issues close/update, and guarded production remains healthy.

## Rollback or Recovery

- Revert the single squash merge to restore prior filter/exception behavior; no data migration or persistent schema change is introduced.
- If new configuration binding blocks deployment, the guarded deploy must retain the previous release. Correct the config/code on a follow-up branch rather than bypassing validation.
- Rate-limit buckets are process-local and ephemeral; rollback/restart safely discards them.
- If response headers are incorrect, do not merge. Fix the arithmetic/test boundary before publication.
- If a service translation misclassifies a programmer fault, remove that catch/translation and let the generic handler own it.

## Risks

- Bucket expiry based on wall time could move backward; use monotonic `System.nanoTime` only for store expiry and `Clock` only for HTTP epoch metadata.
- Duration-to-nanosecond or epoch addition may overflow; use saturating arithmetic and focused extreme-duration tests.
- Unknown-length overflow may surface through Spring MVC exception wrapping; preserve the recognizable overflow cause and verify the real packaged HTTP path, not only a direct filter-chain test.
- `Retry-After` must round up so clients never retry before refill; focused tests cover fractional seconds.
- A global 503 mapping could hide programmer faults if catches are too broad; translate only existing `DataAccessException` catches and keep generic handler behavior unchanged.
- Static password utility failure is rare; scope Mockito static mocking to one test and always close it.
- Environment-specific request defaults can drift; bind and test the profile YAML values and document the environment override.

## Completion Criteria

- Plan is mechanically valid, reviewed with no execution blockers, committed, and pushed to Builder `main` before code edits.
- Issues #1139, #1140, #1141, and #1157 acceptance criteria have direct RED/GREEN and runtime evidence.
- Focused and full checks pass; alternate-port 413/429 acceptance and cleanup are documented in a validated Builder test report.
- Staged review finds no blocker/warning, secret reflection, unbounded state, or generic operational wrapper.
- Spoke commits are pushed, PR checks pass, PR is squash-merged, and the four issues are closed or reconciled with exact evidence.
- Guarded production deployment is healthy and Builder session memory/indexes/validation are committed and pushed.
