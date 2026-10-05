# christopherbell.dev What's for Lunch Import Location Integrity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task in the current session. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent fabricated OpenStreetMap restaurant locations, reject unresolved candidates at both client and service boundaries, and remove the existing exact placeholder population from production after a verified backup.

**Architecture:** `OpenStreetMapRestaurantClient` resolves the first genuine locality tag through configured city/state ownership before it constructs a restaurant. `RestaurantService` independently enforces the persisted import invariant. Production cleanup is a post-deployment, backup-first operation scoped to exact `osm:` records with city `Imported Metro` and their direct favorite/rating references.

**Tech Stack:** Java 25, Spring Boot 4.1, Jackson, MongoDB, JUnit 5, Mockito, Gradle, PowerShell, native Windows production tooling, GitHub Actions, CodeQL.

## Global Constraints

- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; execute code changes only in an isolated worktree refreshed from `origin/main`.
- Use branch `codex/wfl-import-location-integrity` from `origin/main` commit `0dd388fb096c924453bdbab8b66a3215d3e63452` or a newer explicitly re-inspected `origin/main`.
- Invoke `chris-street-style` before every production code, test, or documentation edit described by a code-changing task.
- Use test-driven development: run each named regression red before implementation and green afterward.
- Never use port `8080` for pre-merge validation; use an isolated MongoDB database and a non-production application port.
- Do not add a reverse-geocoding dependency or infer a city from bounds, ZIP, street, or nearest-city distance.
- Do not change public API response shapes, MongoDB restaurant schema, unique-name behavior, remote timeouts, response-size bounds, lease behavior, or error causality.
- Accept locality tags in order: `addr:city`, `addr:town`, `addr:village`, `addr:municipality`.
- Store canonical configured city/state values; reject unsupported locality, conflicting state/country, or invalid coordinates.
- Back up and verify production before cleanup. Delete only exact `osm:` records whose `address.city` equals `Imported Metro` and direct favorite/rating references to those exact IDs.
- Preserve historical lunch sessions and all unrelated data.

---

## Document Status

ready-for-execution

## Objective

Deliver the approved import-location integrity behavior through regression-first implementation, alternate-port runtime proof, pull request and required CI, exact merged production deployment, backup-first placeholder cleanup, recurrence verification, and Builder closure.

## Goals

- Remove every synthetic `Imported Metro` and default `TX` import fallback.
- Retain valid OpenStreetMap candidates through supported alternate locality tags.
- Make unsupported, contradictory, or coordinate-less candidates impossible to persist through normal import paths.
- Keep preview/apply invalid counts aligned.
- Remove the existing production placeholder population and its direct favorite/rating references with exact reconciliation.
- Prove the bad population is not recreated.

## Inputs

- Approved spec: `docs/specs/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md`.
- Active work record: `docs/work/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md`.
- User decisions: strict genuine-location validation; discard unresolved records; clean the existing placeholder population.
- Inspected source base: `azurras/christopherbell.dev` `origin/main` at `0dd388fb096c924453bdbab8b66a3215d3e63452`.
- Production: native Windows services on the development host, application listener on port `8080`, MongoDB database `christopherbell`, protected auto-deployment, backup command `A:\Projects\christopherbell.dev\prod.cmd backup`.

## Branch

- Base: refreshed `origin/main`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-import-location-integrity-20260802`.
- Branch: `codex/wfl-import-location-integrity`.
- If `origin/main` advances before worktree creation, re-inspect every planned current block and line range, update this plan if needed, and rerun plan validation before editing.

## Non-Goals

- No reverse geocoder, locality polygons, geospatial nearest-city lookup, or new remote API.
- No supported-metro expansion.
- No street/postal-code requirement for otherwise valid imported locations.
- No manual-restaurant cleanup.
- No historical session deletion or rewrite.
- No general restaurant cascade-delete redesign.
- No unrelated import, UI, schema, or repository refactor.

## Assumptions

- `WflProperties.Osm.isMetroCoverageUnique()` continues to enforce unique configured city ownership.
- Every configured WFL metro is United States coverage.
- `RestaurantStub.getRestaurantStub` supplies a supported Pflugerville, TX, US address with valid coordinates.
- Existing session rendering already omits restaurant IDs that no longer resolve.
- Native backup tooling produces a compressed archive and validates it with `mongorestore --dryRun`.

## Open Questions

None.

## Task Breakdown

### Task 1 - Enforce genuine configured locations in the OpenStreetMap client

Sequence / dependencies:
- First code task. Create the isolated worktree and private Gradle home before running it.
- Complete the red/green client cycle before changing the service boundary.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Required skill: `superpowers:test-driven-development` for the regression-first cycle.
- Before-Edit Brief:
  - Behavior: return only named OSM elements with a supported genuine locality, compatible optional state/country evidence, and finite in-range coordinates; store canonical configured city/state plus `US`.
  - Invariants: query construction, response limits, timeouts, sorting, website sanitization, phone/cuisine/amenity mapping, and street/postal optionality remain unchanged.
  - Boundary/API: the public method remains `List<Restaurant> getConfiguredMetroRestaurants()`; filtering occurs before a `Restaurant` enters that list.
  - Effects and failures: network and JSON failures remain causal; individual incomplete elements are omitted without throwing; constructor uses startup-validated metro configuration.
  - Tests and evidence: replace the fallback test with a red exclusion test, add positive alternate-locality and negative integrity cases, and keep the complete client test class green.

- [ ] Create the isolated worktree through `superpowers:using-git-worktrees`, set a worktree-private `GRADLE_USER_HOME`, and verify branch/base/status.
- [ ] Invoke `chris-street-style` and record its Before-Edit Brief before touching the client tests.
- [ ] Apply Code Edits 1.1, 1.2, and 1.3 only.
- [ ] Run the missing-locality regression and verify RED because the current client returns one `Imported Metro, TX` restaurant.
- [ ] Apply Code Edits 1.4, 1.5, and 1.6.
- [ ] Run the complete client test class and verify GREEN.
- [ ] Commit the task as `Reject unresolved OSM restaurant locations`.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- Lines: 3-6
- Action: replace

Current:
```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
```

Proposed:
```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
```

Verification:
- `./gradlew.bat :website:compileTestJava --no-daemon`

#### Code Edit 1.2
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- Lines: 89-161
- Action: replace

Current:
```java
  @Test
  void parseRestaurants_defaultsMissingAddressCityToImportedMetro() throws Exception {
    var client = client();
    var method = OpenStreetMapRestaurantClient.class.getDeclaredMethod("parseRestaurants", String.class);
    method.setAccessible(true);
    var body = """
        {
          "elements": [
            {
              "type": "way",
              "id": 789,
              "center": {
                "lat": 30.3001,
                "lon": -97.7002
              },
              "tags": {
                "name": "Metro Lunch"
              }
            }
          ]
        }
        """;

    @SuppressWarnings("unchecked")
    var restaurants = (java.util.List<dev.christopherbell.whatsforlunch.restaurant.model.Restaurant>)
        method.invoke(client, body);

    assertEquals(1, restaurants.size());
    var restaurant = restaurants.getFirst();
    assertEquals("osm:way:789", restaurant.getId());
    assertEquals("Imported Metro", restaurant.getAddress().getCity());
    assertEquals("TX", restaurant.getAddress().getState());
    assertEquals(30.3001, restaurant.getAddress().getLatitude());
    assertEquals(-97.7002, restaurant.getAddress().getLongitude());
    assertNull(restaurant.getAddress().getStreet1());
  }

  @Test
  void parseRestaurants_sortsByNameWithoutFastFoodPenalty() throws Exception {
    var client = client();
    var method = OpenStreetMapRestaurantClient.class.getDeclaredMethod("parseRestaurants", String.class);
    method.setAccessible(true);
    var body = """
        {
          "elements": [
            {
              "type": "node",
              "id": 1,
              "tags": {
                "name": "A Taco Bell",
                "amenity": "fast_food"
              }
            },
            {
              "type": "node",
              "id": 2,
              "tags": {
                "name": "Z Bistro",
                "amenity": "restaurant"
              }
            }
          ]
        }
        """;

    @SuppressWarnings("unchecked")
    var restaurants = (java.util.List<dev.christopherbell.whatsforlunch.restaurant.model.Restaurant>)
        method.invoke(client, body);

    assertEquals(2, restaurants.size());
    assertEquals("A Taco Bell", restaurants.getFirst().getName());
    assertEquals("Z Bistro", restaurants.get(1).getName());
  }
```

Proposed:
```java
  @Test
  void parseRestaurants_rejectsMissingLocalityInsteadOfInventingOne() throws Exception {
    var restaurants = parseRestaurants("""
        {
          "elements": [{
            "type": "way",
            "id": 789,
            "center": {"lat": 30.3001, "lon": -97.7002},
            "tags": {"name": "Metro Lunch"}
          }]
        }
        """);

    assertTrue(restaurants.isEmpty());
  }

  @Test
  void parseRestaurants_acceptsSupportedLocalityTagsWithCanonicalCityAndState() throws Exception {
    var restaurants = parseRestaurants("""
        {
          "elements": [
            {"type":"node","id":1,"lat":30.2672,"lon":-97.7431,
             "tags":{"name":"A City","addr:city":"austin"}},
            {"type":"node","id":2,"lat":37.8044,"lon":-122.2712,
             "tags":{"name":"B Town","addr:town":"OAKLAND","addr:state":"CA"}},
            {"type":"node","id":3,"lat":29.9841,"lon":-90.1529,
             "tags":{"name":"C Village","addr:village":"Metairie","addr:country":"USA"}},
            {"type":"node","id":4,"lat":33.0198,"lon":-96.6989,
             "tags":{"name":"D Municipality","addr:municipality":"Plano","addr:country":"United States"}}
          ]
        }
        """);

    assertEquals(java.util.List.of("Austin", "Oakland", "Metairie", "Plano"), restaurants.stream()
        .map(restaurant -> restaurant.getAddress().getCity())
        .toList());
    assertEquals(java.util.List.of("TX", "CA", "LA", "TX"), restaurants.stream()
        .map(restaurant -> restaurant.getAddress().getState())
        .toList());
    assertTrue(restaurants.stream()
        .allMatch(restaurant -> "US".equals(restaurant.getAddress().getCountry())));
  }

  @Test
  void parseRestaurants_rejectsUnsupportedContradictoryOrCoordinateLessLocations() throws Exception {
    var restaurants = parseRestaurants("""
        {
          "elements": [
            {"type":"node","id":1,"lat":30.2672,"lon":-97.7431,
             "tags":{"name":"Unsupported","addr:city":"Houston"}},
            {"type":"node","id":2,"lat":30.2672,"lon":-97.7431,
             "tags":{"name":"Wrong State","addr:city":"Austin","addr:state":"CA"}},
            {"type":"node","id":3,"lat":30.2672,"lon":-97.7431,
             "tags":{"name":"Wrong Country","addr:city":"Austin","addr:country":"CA"}},
            {"type":"node","id":4,"lon":-97.7431,
             "tags":{"name":"Missing Latitude","addr:city":"Austin"}},
            {"type":"node","id":5,"lat":30.2672,
             "tags":{"name":"Missing Longitude","addr:city":"Austin"}}
          ]
        }
        """);

    assertTrue(restaurants.isEmpty());
  }

  @Test
  void parseRestaurants_sortsByNameWithoutFastFoodPenalty() throws Exception {
    var restaurants = parseRestaurants("""
        {
          "elements": [
            {"type":"node","id":1,"lat":30.2672,"lon":-97.7431,
             "tags":{"name":"A Taco Bell","amenity":"fast_food","addr:city":"Austin"}},
            {"type":"node","id":2,"lat":30.2673,"lon":-97.7432,
             "tags":{"name":"Z Bistro","amenity":"restaurant","addr:city":"Austin"}}
          ]
        }
        """);

    assertEquals(2, restaurants.size());
    assertEquals("A Taco Bell", restaurants.getFirst().getName());
    assertEquals("Z Bistro", restaurants.get(1).getName());
  }
```

Verification:
- RED: `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.OpenStreetMapRestaurantClientTest.parseRestaurants_rejectsMissingLocalityInsteadOfInventingOne --no-daemon`
- Expected before implementation: assertion failure because one restaurant is returned.

#### Code Edit 1.3
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- Lines: before 234
- Action: add

Proposed:
```java
  @SuppressWarnings("unchecked")
  private java.util.List<dev.christopherbell.whatsforlunch.restaurant.model.Restaurant>
      parseRestaurants(String body) throws Exception {
    var method = OpenStreetMapRestaurantClient.class.getDeclaredMethod("parseRestaurants", String.class);
    method.setAccessible(true);
    return (java.util.List<dev.christopherbell.whatsforlunch.restaurant.model.Restaurant>)
        method.invoke(client(), body);
  }
```

Verification:
- `./gradlew.bat :website:compileTestJava --no-daemon`

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 14-41
- Action: replace

Current:
```java
import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import org.springframework.stereotype.Component;

/**
 * Client for importing restaurant-like places from OpenStreetMap via Overpass.
 */
@Component
public class OpenStreetMapRestaurantClient {
  private static final long MAXIMUM_RESPONSE_BYTES = 16L * 1024 * 1024;

  private final HttpClient httpClient;
  private final ObjectMapper objectMapper;
  private final WflProperties.Osm properties;

  public OpenStreetMapRestaurantClient(
      ObjectMapper objectMapper,
      WflProperties wflProperties
  ) {
    this.objectMapper = objectMapper;
    this.properties = wflProperties.getRestaurantImport().getOsm();
    this.httpClient = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .build();
  }
```

Proposed:
```java
import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Component;

/**
 * Client for importing restaurant-like places from OpenStreetMap via Overpass.
 */
@Component
public class OpenStreetMapRestaurantClient {
  private static final long MAXIMUM_RESPONSE_BYTES = 16L * 1024 * 1024;

  private final HttpClient httpClient;
  private final ObjectMapper objectMapper;
  private final WflProperties.Osm properties;
  private final Map<String, SupportedLocation> supportedLocations;

  public OpenStreetMapRestaurantClient(
      ObjectMapper objectMapper,
      WflProperties wflProperties
  ) {
    this.objectMapper = objectMapper;
    this.properties = wflProperties.getRestaurantImport().getOsm();
    this.supportedLocations = configuredLocations(properties.getMetros());
    this.httpClient = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .build();
  }
```

Verification:
- `./gradlew.bat :website:compileJava --no-daemon`

#### Code Edit 1.5
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 110-135
- Action: replace

Current:
```java
  private java.util.Optional<Restaurant> toRestaurant(JsonNode element) {
    var tags = element.path("tags");
    var name = text(tags, "name");
    if (name == null || name.isBlank()) {
      return java.util.Optional.empty();
    }

    return java.util.Optional.of(Restaurant.builder()
        .id("osm:" + element.path("type").asText() + ":" + element.path("id").asText())
        .name(name.strip())
        .address(Address.builder()
            .street1(street1(tags))
            .city(defaultText(text(tags, "addr:city"), "Imported Metro"))
            .state(defaultText(text(tags, "addr:state"), "TX"))
            .country(defaultText(text(tags, "addr:country"), "US"))
            .latitude(coordinate(element, "lat"))
            .longitude(coordinate(element, "lon"))
            .postalCode(text(tags, "addr:postcode"))
            .build())
        .cuisine(text(tags, "cuisine"))
        .phoneNumber(firstText(tags, "contact:phone", "phone"))
        .sourceAmenity(text(tags, "amenity"))
        .website(RestaurantWebsiteUrlPolicy.safeOrNull(
            firstText(tags, "contact:website", "website")))
        .build());
  }
```

Proposed:
```java
  private Optional<Restaurant> toRestaurant(JsonNode element) {
    var tags = element.path("tags");
    var name = text(tags, "name");
    var location = supportedLocation(tags);
    var latitude = coordinate(element, "lat");
    var longitude = coordinate(element, "lon");
    if (name == null || name.isBlank() || location.isEmpty()
        || !isCoordinate(latitude, -90.0, 90.0)
        || !isCoordinate(longitude, -180.0, 180.0)) {
      return Optional.empty();
    }
    var supportedLocation = location.orElseThrow();

    return Optional.of(Restaurant.builder()
        .id("osm:" + element.path("type").asText() + ":" + element.path("id").asText())
        .name(name.strip())
        .address(Address.builder()
            .street1(street1(tags))
            .city(supportedLocation.city())
            .state(supportedLocation.state())
            .country("US")
            .latitude(latitude)
            .longitude(longitude)
            .postalCode(text(tags, "addr:postcode"))
            .build())
        .cuisine(text(tags, "cuisine"))
        .phoneNumber(firstText(tags, "contact:phone", "phone"))
        .sourceAmenity(text(tags, "amenity"))
        .website(RestaurantWebsiteUrlPolicy.safeOrNull(
            firstText(tags, "contact:website", "website")))
        .build());
  }
```

Verification:
- `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.OpenStreetMapRestaurantClientTest.parseRestaurants_rejectsMissingLocalityInsteadOfInventingOne --no-daemon`

#### Code Edit 1.6
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 150-180
- Action: replace

Current:
```java
  private String firstText(JsonNode tags, String... keys) {
    for (String key : keys) {
      var value = text(tags, key);
      if (value != null && !value.isBlank()) {
        return value;
      }
    }
    return null;
  }

  private String text(JsonNode node, String fieldName) {
    var value = node.path(fieldName);
    return value.isMissingNode() || value.isNull() ? null : value.asText();
  }

  private Double coordinate(JsonNode element, String fieldName) {
    var direct = element.path(fieldName);
    if (direct.isNumber()) {
      return direct.asDouble();
    }

    var center = element.path("center").path(fieldName);
    return center.isNumber() ? center.asDouble() : null;
  }

  private String defaultText(String value, String defaultValue) {
    return value == null || value.isBlank() ? defaultValue : value;
  }

  private String normalize(String value) {
    return value == null ? "" : value.strip().toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9 -]", "");
  }
```

Proposed:
```java
  private Optional<SupportedLocation> supportedLocation(JsonNode tags) {
    var locality = firstText(tags, "addr:city", "addr:town", "addr:village", "addr:municipality");
    var location = supportedLocations.get(normalizeLocation(locality));
    if (location == null) {
      return Optional.empty();
    }
    var suppliedState = text(tags, "addr:state");
    if (suppliedState != null
        && !suppliedState.isBlank()
        && !normalizeLocation(suppliedState).equals(normalizeLocation(location.state()))) {
      return Optional.empty();
    }
    var suppliedCountry = text(tags, "addr:country");
    return suppliedCountry == null || suppliedCountry.isBlank() || isUnitedStates(suppliedCountry)
        ? Optional.of(location)
        : Optional.empty();
  }

  private Map<String, SupportedLocation> configuredLocations(List<WflProperties.Metro> metros) {
    var locations = new LinkedHashMap<String, SupportedLocation>();
    for (var metro : metros) {
      for (var city : metro.getCities()) {
        locations.put(normalizeLocation(city), new SupportedLocation(city.strip(), metro.getState().strip()));
      }
    }
    return Map.copyOf(locations);
  }

  private String firstText(JsonNode tags, String... keys) {
    for (String key : keys) {
      var value = text(tags, key);
      if (value != null && !value.isBlank()) {
        return value;
      }
    }
    return null;
  }

  private String text(JsonNode node, String fieldName) {
    var value = node.path(fieldName);
    return value.isMissingNode() || value.isNull() ? null : value.asText();
  }

  private Double coordinate(JsonNode element, String fieldName) {
    var direct = element.path(fieldName);
    if (direct.isNumber()) {
      return direct.asDouble();
    }

    var center = element.path("center").path(fieldName);
    return center.isNumber() ? center.asDouble() : null;
  }

  private boolean isCoordinate(Double value, double minimum, double maximum) {
    return value != null
        && !value.isNaN()
        && !value.isInfinite()
        && value >= minimum
        && value <= maximum;
  }

  private boolean isUnitedStates(String value) {
    return List.of("us", "usa", "unitedstates").contains(normalizeLocation(value));
  }

  private String normalizeLocation(String value) {
    return value == null ? "" : value.strip().toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9]", "");
  }

  private String normalize(String value) {
    return value == null ? "" : value.strip().toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9 -]", "");
  }

  private record SupportedLocation(String city, String state) {
  }
```

Verification:
- `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.OpenStreetMapRestaurantClientTest --no-daemon`
- Expected: all client tests pass; no assertion contains `Imported Metro`.

### Task 2 - Add service-level import-location defense in depth

Sequence / dependencies:
- Runs after Task 1 so normal client output already satisfies the invariant.
- Characterizes prepared snapshots that bypass the client before changing service validation.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Required skill: `superpowers:test-driven-development` for the regression-first cycle.
- Before-Edit Brief:
  - Behavior: preview and apply classify unsupported city/state/country or missing-coordinate candidates as invalid and never query or mutate persistence for them.
  - Invariants: valid candidates, ID/name matching, rename-collision handling, representative changes, checksum construction, and result shapes remain unchanged.
  - Boundary/API: no method signatures change; `isValidImportRestaurant` becomes the shared internal gate already called by both preview and apply.
  - Effects and failures: invalid values increment existing counts and emit the existing throwable-free debug path; persistence exceptions for valid candidates remain causal.
  - Tests and evidence: add a prepared-snapshot regression that is red because current validation accepts address-bearing invalid locations, then run all service tests green.

- [ ] Invoke `chris-street-style` and record its Before-Edit Brief before touching the service test.
- [ ] Apply Code Edit 2.1 only.
- [ ] Run the named service regression and verify RED because current validation reaches repository lookup.
- [ ] Apply Code Edit 2.2.
- [ ] Run the named regression and complete `RestaurantServiceTest` class GREEN.
- [ ] Commit the task as `Validate imported restaurant coverage`.

#### Code Edit 2.1
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- Lines: after 1014
- Action: add

Proposed:
```java
  @Test
  @DisplayName("OpenStreetMap import: skips candidates without supported real locations")
  void testPreparedImport_whenLocationIsUnsupportedOrCoordinatesMissing_skipsInvalid()
      throws Exception {
    var placeholder = RestaurantStub.getRestaurantStub("osm:node:location-1");
    placeholder.getAddress().setCity("Imported Metro");
    var wrongState = RestaurantStub.getRestaurantStub("osm:node:location-2");
    wrongState.getAddress().setState("CA");
    var missingCoordinates = RestaurantStub.getRestaurantStub("osm:node:location-3");
    missingCoordinates.getAddress().setLatitude(null);
    var wrongCountry = RestaurantStub.getRestaurantStub("osm:node:location-4");
    wrongCountry.getAddress().setCountry("CA");

    when(openStreetMapRestaurantClient.getConfiguredMetroRestaurants())
        .thenReturn(List.of(placeholder, wrongState, missingCoordinates, wrongCountry));

    var snapshot = restaurantService.prepareConfiguredMetroImport();
    var result = restaurantService.applyPreparedImport(snapshot, RestaurantImportLeaseGuard.NONE);

    assertEquals(4, snapshot.counts().fetched());
    assertEquals(4, snapshot.counts().invalid());
    assertEquals(0, snapshot.counts().created());
    assertEquals(0, snapshot.counts().updated());
    assertEquals(4, result.fetched());
    assertEquals(4, result.skippedInvalid());
    assertEquals(0, result.imported());
    assertEquals(0, result.updated());
    verifyNoInteractions(restaurantRepository);
  }
```

Verification:
- RED: `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest.testPreparedImport_whenLocationIsUnsupportedOrCoordinatesMissing_skipsInvalid --no-daemon`
- Expected before implementation: Mockito verification failure because repository lookups occur for the invalid candidates.

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 1285-1295
- Action: replace

Current:
```java
  private boolean isValidImportRestaurant(Restaurant restaurant) {
    return restaurant != null
        && restaurant.getId() != null
        && !restaurant.getId().isBlank()
        && restaurant.getName() != null
        && !restaurant.getName().isBlank()
        && restaurant.getAddress() != null
        && (restaurant.getWebsite() == null
            || restaurant.getWebsite().isBlank()
            || RestaurantWebsiteUrlPolicy.safeOrNull(restaurant.getWebsite()) != null);
  }
```

Proposed:
```java
  private boolean isValidImportRestaurant(Restaurant restaurant) {
    return restaurant != null
        && restaurant.getId() != null
        && !restaurant.getId().isBlank()
        && restaurant.getName() != null
        && !restaurant.getName().isBlank()
        && hasSupportedImportLocation(restaurant)
        && (restaurant.getWebsite() == null
            || restaurant.getWebsite().isBlank()
            || RestaurantWebsiteUrlPolicy.safeOrNull(restaurant.getWebsite()) != null);
  }

  private boolean hasSupportedImportLocation(Restaurant restaurant) {
    if (!hasCoordinates(restaurant)) {
      return false;
    }
    var address = restaurant.getAddress();
    var city = normalizeCity(address.getCity());
    var state = normalizeCity(address.getState());
    if (city.isBlank() || state.isBlank() || !isUnitedStates(address.getCountry())) {
      return false;
    }
    return wflProperties.getRestaurantImport().getOsm().getMetros().stream()
        .anyMatch(metro -> normalizeCity(metro.getState()).equals(state)
            && metro.getCities().stream().anyMatch(candidate -> normalizeCity(candidate).equals(city)));
  }

  private boolean isUnitedStates(String value) {
    var normalized = normalizeCity(value).replaceAll("[^a-z]", "");
    return List.of("us", "usa", "unitedstates").contains(normalized);
  }
```

Verification:
- `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest.testPreparedImport_whenLocationIsUnsupportedOrCoordinatesMissing_skipsInvalid --no-daemon`
- `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --no-daemon`
- Expected: regression and complete service class pass; invalid candidates cause no repository interaction.

### Task 3 - Document the strict import contract

Sequence / dependencies:
- Runs after Tasks 1 and 2 so documentation describes proven behavior.

Implementation notes:
- Required skill: `chris-street-style` before any documentation edit because this package README is part of the production behavior contract.
- Before-Edit Brief:
  - Behavior: maintainers can identify the accepted locality precedence, canonical ownership rule, coordinate requirement, and exclusion behavior.
  - Invariants: scheduler, catch-up, rename-collision, and manual-import documentation remain accurate.
  - Boundary/API: documentation only; no runtime interface changes.
  - Effects and failures: prevents reintroduction of synthetic fallbacks by making the invariant explicit at the feature boundary.
  - Tests and evidence: search for stale fallback language and run documentation/build checks with the final diff.

- [ ] Invoke `chris-street-style` and record its Before-Edit Brief.
- [ ] Apply Code Edit 3.1.
- [ ] Search the spoke diff and tracked source for stale synthetic fallback claims.
- [ ] Commit the task as `Document strict OSM location imports`.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`
- Lines: 73-79
- Action: replace

Current:
```markdown
- Manual imports still run through the admin endpoint.
- The default Overpass import covers Austin, the San Francisco Bay Area, New Orleans, and Dallas through semicolon-separated bounding boxes in `wfl.restaurant-import.osm.bbox`.
- Missing OpenStreetMap `addr:city` values default to `Imported Metro` instead of an Austin-specific city label.
- Automated imports run monthly on the fifteenth using `wfl.restaurant-import.monthly.cron`.
- The scheduler logs start, completion, and failure events.
- `RestaurantImportState` stores the last completed import month. On application startup, WFL checks whether the previous month has a completed import; if not, it runs a catch-up import immediately.
- If an existing OpenStreetMap id is renamed to a normalized name owned by another restaurant, preview reports it unchanged and apply skips it without mutation so the remaining import can complete.
```

Proposed:
```markdown
- Manual imports still run through the admin endpoint.
- The default Overpass import covers configured bounding boxes for Austin, the San Francisco Bay Area, New Orleans, and Dallas.
- Imported locality is the first nonblank `addr:city`, `addr:town`, `addr:village`, or `addr:municipality` value that matches a configured supported city. The canonical configured city and state are stored.
- Missing, unsupported, state/country-conflicting, or coordinate-less locations are excluded; the importer never invents a city or state.
- Street and postal-code tags remain optional when the supported locality and coordinates are valid.
- Automated imports run monthly on the fifteenth using `wfl.restaurant-import.monthly.cron`.
- The scheduler logs start, completion, and failure events.
- `RestaurantImportState` stores the last completed import month. On application startup, WFL checks whether the previous month has a completed import; if not, it runs a catch-up import immediately.
- If an existing OpenStreetMap id is renamed to a normalized name owned by another restaurant, preview reports it unchanged and apply skips it without mutation so the remaining import can complete.
```

Verification:
- `rg -n "Imported Metro|default.*TX|addr:city.*default" website/src/main website/src/test`
- Expected after test replacement and documentation edit: no production fallback and no test expecting the sentinel.

### Task 4 - Run full automated and alternate-port runtime verification

Sequence / dependencies:
- Runs after all code tasks and task commits.
- Must pass before publishing the spoke branch or saving a completed test report.

Implementation notes:
- Required skills: `verify-local-spring-app`, `save-test-report`, and `superpowers:verification-before-completion`.
- Use a loopback HTTP server that returns a deterministic Overpass payload containing one valid Austin candidate and several invalid candidates matching Task 1 cases.
- Use an isolated database such as `christopherbell_wfl_location_integrity_20260802`, application port `8097`, and a distinct loopback Overpass port.
- Keep production port `8080` and the `ChristopherBellDev` service untouched.

- [ ] Run `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.OpenStreetMapRestaurantClientTest --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --no-daemon`.
- [ ] Run `./gradlew.bat :website:test --no-daemon`.
- [ ] Run `./gradlew.bat :website:check --no-daemon`.
- [ ] Start the loopback Overpass fixture and the production-like packaged app on `127.0.0.1:8097` with the isolated database and `app.shared-folder.enabled=false`, `command-center.enabled=false`.
- [ ] Exercise readiness and the admin import preview/apply path using the established deploy-smoke authorization fixture.
- [ ] Query the isolated `whatsforlunch` collection and prove only the supported canonical candidate exists, with no `Imported Metro` value.
- [ ] Exercise `GET /api/whatsforlunch/restaurant/2026-05-17/nearby` with the valid candidate's coordinates and capture HTTP status/body.
- [ ] Stop only task-owned processes and drop only the verified isolated database.
- [ ] Obtain independent code review and resolve all Critical and Important findings; document any accepted Minor residual risk.
- [ ] Save, validate, index, commit, and push the Builder test report before publication continues.

## Code Changes

- `OpenStreetMapRestaurantClientTest.java`: replace synthetic-fallback expectation; add alternate locality, contradiction, and coordinate rejection coverage; add reflection helper; keep sorting fixture valid.
- `OpenStreetMapRestaurantClient.java`: add immutable configured locality ownership, strict optional evidence checks, coordinate validation, canonical city/state storage, and remove default values.
- `RestaurantServiceTest.java`: add prepared-snapshot defense-in-depth regression.
- `RestaurantService.java`: extend existing preview/apply validity gate with configured city/state, US country, and coordinate requirements.
- `README.md`: replace stale fallback contract with strict source-integrity behavior.

## Files and Modules

- Spoke client and tests under `website/src/{main,test}/java/dev/christopherbell/whatsforlunch/restaurant/`.
- Spoke restaurant feature README.
- Builder spec, work record, implementation plan, test report, spoke update/review, session memory, and closure.
- Existing production backup/deployment tooling; no production-operations source edit is planned.

## Unit Testing

- RED/GREEN client exclusion: `OpenStreetMapRestaurantClientTest.parseRestaurants_rejectsMissingLocalityInsteadOfInventingOne`.
- Client positive coverage: accepted locality precedence and canonical city/state for Austin, Oakland, Metairie, and Plano.
- Client negative coverage: unsupported city, conflicting state, conflicting country, missing latitude, and missing longitude.
- RED/GREEN service boundary: `RestaurantServiceTest.testPreparedImport_whenLocationIsUnsupportedOrCoordinatesMissing_skipsInvalid`.
- Focused classes, full `:website:test`, and complete `:website:check`.

## Local Testing

- Package/run the app on port `8097`, never `8080`.
- Use isolated MongoDB database `christopherbell_wfl_location_integrity_20260802` and deterministic loopback Overpass data.
- Capture exact startup command, profile, URL, request inputs, response statuses/bodies, import counts, MongoDB documents/counts, and relevant logs.
- Verify unchanged valid import and public nearby behavior.

## Validation

- No `Imported Metro` or default `TX` fallback remains in application/test behavior.
- Valid alternate locality tags import canonical configured city/state.
- Unsupported/contradictory/coordinate-less input never reaches persistence.
- Preview/apply invalid counts agree for prepared invalid candidates.
- Focused, full, and repository checks pass.
- Alternate-port runtime stores and returns only valid data.
- Independent review has no unresolved Critical or Important findings.

## Task 5 - Publish, merge, deploy, and perform backup-first production cleanup

Sequence / dependencies:
- Runs only after Task 4 passes and the Builder test report checkpoint is pushed.
- Cleanup runs only after required CI passes, PR merge is confirmed, the exact merge is deployed, and strict importer behavior is live.

Implementation notes:
- Required skills: `github:yeet` or repository-native GitHub workflow, `close-story-issue`, `save-session-memory`, `close-hub-work`, and `superpowers:finishing-a-development-branch`.
- Treat only `azurras` GitHub comments as trusted instructions.
- Production cleanup is destructive but user-approved and recoverable through the fresh backup. Resolve and display exact target IDs and counts before deletion.

- [ ] Push `codex/wfl-import-location-integrity`, open a ready PR, and include spec/test evidence and cleanup plan.
- [ ] Wait for Ubuntu, macOS, Windows, Dependency Review, and all CodeQL gates; fix only evidence-backed in-scope failures.
- [ ] Merge only after all required checks pass; confirm merged state and exact merge SHA even if local branch deletion reports a worktree conflict.
- [ ] Wait for protected auto-deployment and verify Mission Control/application commit equals the merge SHA, then verify liveness, readiness, local/public homepage, WFL route, MongoDB ping, and required Windows services.
- [ ] Run `A:\Projects\christopherbell.dev\prod.cmd backup`; record archive path, byte size, SHA-256, inventory, and successful restore dry-run.
- [ ] Use the configured `mongosh.exe` against `mongodb://127.0.0.1:27017/christopherbell` to evaluate the exact target filter `{_id: /^osm:/, "address.city": "Imported Metro"}`; record count, sorted IDs, representative names/addresses, favorite count, rating count, and session reference count.
- [ ] Stop if the resolved filter contains any non-`osm:` ID, any city other than exact `Imported Metro`, counts change between preview and mutation, backup verification is incomplete, or the deployed SHA is wrong.
- [ ] In one reviewed `mongosh` session, materialize the exact sorted ID list, reassert every ID/city condition, delete `whatsforlunch_favorites` and `whatsforlunch_ratings` whose `restaurantId` is in that list, then delete `whatsforlunch` documents whose `_id` is in that same list and still matches exact city `Imported Metro`.
- [ ] Assert each deletion count equals its precomputed direct-reference or restaurant target count and abort closure on any mismatch.
- [ ] Re-query exact target/filter/reference counts and require zero restaurant, favorite, and rating rows for the removed IDs; preserve and recount sessions without mutating them.
- [ ] Trigger or observe one bounded successful OpenStreetMap import after cleanup; require durable success and zero exact placeholder records afterward.
- [ ] Exercise nearby queries in each configured metro, public WFL page, readiness/liveness, MongoDB ping, application commit identity, and Windows service state; search current-release logs for `Imported Metro`, import failures, and unexpected persistence errors.
- [ ] Record spoke update/review, close the work record, save session memory, update indexes, validate Builder state, and commit/push each required Builder checkpoint.

## Rollback or Recovery

- Before merge: revert only the feature branch commits or close the PR.
- After merge but before cleanup: deploy the previous verified release only if strict import runtime behavior regresses; pause imports rather than accepting synthetic locations.
- After cleanup: restore the fresh verified archive if target/delete reconciliation fails or public/member behavior shows unexpected data loss.
- Preserve the backup, ID manifest, before/after counts, and exact commands until closure is complete.

## Risks

- Strict matching will reduce catalog size; this is the approved correctness trade-off.
- OSM full state names do not equal configured abbreviations and will be excluded; this is conservative and documented.
- Client/service rules can drift; paired tests and README documentation constrain both boundaries.
- Cleanup may touch user references; exact ID materialization, precomputed counts, direct-reference cleanup, session preservation, and backup-first rollback limit impact.
- Monthly import result limits can make recurrence checks misleading; require durable success and direct database zero-count evidence rather than logs alone.
- Production readiness can return transient `503` during listener rotation; recheck liveness/readiness after the restart window before declaring failure.

## Completion Criteria

- Plan tasks and checkboxes are complete with task commits and final diff review.
- Focused, full, repository, alternate-port runtime, and independent-review gates pass.
- Spoke branch is pushed, PR checks all pass, and merge SHA is confirmed/deployed.
- Fresh production backup and restore dry-run evidence exist.
- Exact placeholder catalog records and their favorite/rating references are removed with reconciled counts; historical sessions remain.
- Successful post-cleanup import and database checks prove zero recurrence.
- Production commit identity, routes, database, logs, and Windows services are healthy.
- Test report, spoke update/review, work closure, and session memory are saved, indexed, validated, committed, and pushed.
