# Restaurant Profiles Void and Search Indexing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Use `superpowers:subagent-driven-development` only if the user explicitly selects delegated execution. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render complete public restaurant profiles in raw HTML, add safe conditional Restaurant JSON-LD, preserve correct indexing boundaries, and apply the scoped WFL Void design while retaining signed-in personal controls as progressive enhancement.

**Architecture:** Replace the social-preview-only projection with one immutable public page model created from the canonical `RestaurantDetail` lookup. The controller passes only that public model to Thymeleaf; the template owns public content and the profile JavaScript owns only authenticated personal controls. Existing canonical/sitemap/robots boundaries remain in place, while scoped `whats-for-lunch.css` takes ownership of profile styling.

**Tech Stack:** Java 25, Spring Boot 4.1, Thymeleaf, Jackson 3 (`tools.jackson`), JavaScript ES modules, Node's built-in test runner, CSS, Gradle 9.6.1, MongoDB, MockMvc, AssertJ, Mockito.

## Global Constraints

- Every valid public restaurant profile is indexable.
- Public content is server-rendered; JavaScript only progressively enhances signed-in personal controls.
- Public HTML and JSON-LD never contain `myRating`, `myFavorite`, creator/modifier identity, or audit timestamps.
- JSON-LD is serialized safely and includes only valid, present public fields.
- Missing or malformed restaurant IDs remain content-free `404` responses with `noindex,nofollow` and no Restaurant JSON-LD.
- Favorites remains private/non-indexable; Top Rated, sitemap, robots policy, profile URL shape, rating rules, selection behavior, import behavior, and database schema remain unchanged.
- Top Rated and Favorites retain their existing visual design.
- Every source change follows regression-first TDD and `write-chris-street-style-code`.
- Work only in `A:\Projects\christopherbell.dev-worktrees\restaurant-profile-void-seo`; preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`.
- Validate on a non-8080 port before any production listener action.

---

## Document Status

complete

## Objective

Implement the approved project specification at `docs/specs/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md` as a cohesive, testable change through PR, CI, merge, protected deployment, production verification, and Builder closeout.

## Goals

1. A raw `GET /wfl/restaurants/{id}` response contains the useful public restaurant profile before JavaScript runs.
2. Valid responses carry unique metadata, one encoded canonical URL, and safe schema.org Restaurant JSON-LD.
3. Sparse and unrated records omit absent optional facts without placeholder geography or fabricated ratings.
4. Anonymous browsers make no redundant restaurant-detail request; signed-in browsers progressively load and mutate only personal rating/favorite controls.
5. The restaurant profile uses the approved responsive, accessible WFL Void design from its dedicated stylesheet.
6. Automated, alternate-port, PR CI, merged-SHA deployment, and production checks pass.

## Inputs

- Approved spec: `C:\Users\Christopher\Developer\builder\docs\specs\2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md`
- Approved user decisions: all valid profiles; server rendering plus progressive enhancement; one public-only model; conditional Restaurant JSON-LD; scoped Void profile layout; no Top Rated/Favorites redesign.
- Refreshed spoke base: `origin/main` at `9c69623049829394f245515b8d1751c9f7579271`.
- Baseline evidence: focused `ViewControllerTest`, `PublicSitemapServiceTest`, `PublicDeliveryConfigurationTest`, and `:website:jsTest` passed with `BUILD SUCCESSFUL` on 2026-08-02.
- Known checkout artifact: `gradlew.bat` appears modified by Windows line endings in a clean linked worktree and must not be staged.

## Branch

- Worktree: `A:\Projects\christopherbell.dev-worktrees\restaurant-profile-void-seo`
- Branch: `codex/restaurant-profile-void-seo`
- Base: `origin/main` at `9c69623049829394f245515b8d1751c9f7579271`

## Non-Goals

- No API response-shape, persistence, schema, import, selection, rating-rule, or URL-shape change.
- No crawler-only route or duplicated hidden SEO copy.
- No publication of personal member state or audit data.
- No Top Rated or Favorites redesign.
- No unrelated WFL or shared-site refactor.

## Assumptions

- `RestaurantService.getRestaurantById(String)` remains the canonical lookup and already normalizes unsafe persisted website values to `null`.
- Jackson's application `ObjectMapper` is available for injection through Spring Boot.
- The existing public sitemap continues to enumerate every persisted restaurant ID and encode it as a path segment.
- The browser session marker exposed through `getAuthClaims()` remains a UI-only signal; API authorization remains cookie/CSRF enforced server-side.
- Port `8094` and isolated database `christopherbell_dev_restaurant_profiles_void_seo` will be checked at execution time and replaced with another non-8080 port/name if occupied.

## Open Questions

None.

## File Structure and Ownership

- `RestaurantProfilePage.java`: immutable public-only page data and valid nested address/rating states.
- `RestaurantProfilePageService.java`: the single canonical lookup, normalization, safe canonical/directions construction, and HTML-safe JSON-LD serialization boundary.
- `WhatsForLunchViewController.java`: HTTP route/status mapping only.
- `restaurant.html`: complete semantic public rendering and the dedicated member-enhancement mount.
- `restaurant-profile.js`: browser-session detection plus personal rating/favorite enhancement; it never rebuilds public profile content.
- `whats-for-lunch.css`: exclusive owner of chooser and restaurant-profile Void styling.
- Focused Java and JavaScript tests: observable model, raw response, privacy, enhancement, failure, indexing, and stylesheet contracts.

## Task Breakdown

### Task 1 - Build the immutable public restaurant page boundary

Sequence / dependencies:
- First implementation task. It supplies the page interface consumed by the controller/template task.

Expected files:
- Create `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePage.java`.
- Create `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePageService.java`.
- Create `website/src/test/java/dev/christopherbell/view/wfl/RestaurantProfilePageServiceTest.java`.

Interfaces:
- Consumes: `RestaurantService.getRestaurantById(String)`, `RestaurantDetail`, `RestaurantWebsiteUrlPolicy.safeOrNull(String)`, injected Jackson `ObjectMapper`.
- Produces: `RestaurantProfilePageService.profile(String) -> RestaurantProfilePage`; nested `RestaurantProfilePage.Address` and `RestaurantProfilePage.Rating`; public methods `addressLine()`, `hasRating()`, `averageRating()`.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke it together with `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: A valid ID maps one canonical detail lookup into safe public display/search data; invalid/missing IDs map to the existing not-found contract.
  - Invariants: The page type cannot carry personal/audit fields; ratings exist only for a positive count and valid 1–5 sum; coordinates are either a valid pair or absent; JSON cannot close its script element.
  - Boundary/API: The new page service replaces the WFL view package's metadata-only preview service and remains the controller's only restaurant dependency.
  - Effects and failures: One repository/rating lookup occurs through `RestaurantService`; not-found stays `ResourceNotFoundException`; JSON serialization faults become causal `IllegalStateException`; malformed persisted optional facts are omitted.
  - Tests and evidence: RED tests assert fields/raw JSON that the preview service cannot provide, hostile `</script>` escaping, sparse/unrated omission, safe links, coordinate/address directions, and invalid-ID translation; GREEN is the same focused test class passing.

- [ ] **Step 1: Add the focused service tests and witness RED**

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/view/wfl/RestaurantProfilePageServiceTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.view.wfl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.when;

import dev.christopherbell.libs.api.exception.InvalidRequestException;
import dev.christopherbell.libs.api.exception.ResourceNotFoundException;
import dev.christopherbell.whatsforlunch.restaurant.RestaurantService;
import dev.christopherbell.whatsforlunch.restaurant.model.Address;
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantDetail;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import tools.jackson.databind.ObjectMapper;

@ExtendWith(MockitoExtension.class)
class RestaurantProfilePageServiceTest {
  @Mock private RestaurantService restaurants;

  @Test
  void profileBuildsCompletePublicPageAndSafeRestaurantJsonLd() throws Exception {
    when(restaurants.getRestaurantById("rest/one")).thenReturn(RestaurantDetail.builder()
        .id("rest/one")
        .name("Taco </script><script>alert(1)</script>")
        .cuisine("Mexican")
        .address(Address.builder().street1("100 Main St").city("Austin").state("TX")
            .postalCode("78701").country("US").latitude(30.2672).longitude(-97.7431).build())
        .phoneNumber("512-555-0100").website("https://example.com/menu")
        .sourceAmenity("restaurant").ratingCount(2).ratingSum(9)
        .myRating(5).myFavorite(true).createdBy("private-account").build());

    var page = service().profile("rest/one");

    assertThat(page.canonicalUrl()).endsWith("/wfl/restaurants/rest%2Fone");
    assertThat(page.addressLine()).isEqualTo("100 Main St, Austin, TX, 78701");
    assertThat(page.averageRating()).isEqualTo(4.5);
    assertThat(page.directionsUrl()).contains("destination=30.2672", "-97.7431");
    assertThat(page.structuredDataJson()).contains("\\u003c/script\\u003e");
    assertThat(page.structuredDataJson()).doesNotContain("</script>", "myRating", "myFavorite",
        "private-account", "createdBy");
    var json = new ObjectMapper().readTree(unescapeHtmlSafeJson(page.structuredDataJson()));
    assertThat(json.get("@type").asText()).isEqualTo("Restaurant");
    assertThat(json.at("/aggregateRating/ratingValue").asDouble()).isEqualTo(4.5);
    assertThat(json.at("/address/addressLocality").asText()).isEqualTo("Austin");
  }

  @Test
  void profileOmitsInvalidOptionalFactsAndFabricatedRating() throws Exception {
    when(restaurants.getRestaurantById("sparse")).thenReturn(RestaurantDetail.builder()
        .id("sparse").name("Sparse Cafe").website("javascript:alert(1)")
        .ratingCount(0).ratingSum(0).build());

    var page = service().profile("sparse");

    assertThat(page.hasRating()).isFalse();
    assertThat(page.website()).isNull();
    assertThat(page.address()).isNull();
    var json = new ObjectMapper().readTree(page.structuredDataJson());
    assertThat(json.has("aggregateRating")).isFalse();
    assertThat(json.has("address")).isFalse();
    assertThat(json.has("sameAs")).isFalse();
    assertThat(json.has("servesCuisine")).isFalse();
  }

  @Test
  void invalidIdUsesTheSameNotFoundBoundaryAsMissingRestaurant() throws Exception {
    when(restaurants.getRestaurantById("bad"))
        .thenThrow(new InvalidRequestException("internal validation detail"));

    assertThatThrownBy(() -> service().profile("bad"))
        .isInstanceOf(ResourceNotFoundException.class)
        .hasMessage("Restaurant not found.");
  }

  @Test
  void pageValueTypesRejectImpossibleRatingAndCoordinateStates() {
    assertThatThrownBy(() -> new RestaurantProfilePage.Rating(0, 0))
        .isInstanceOf(IllegalArgumentException.class);
    assertThatThrownBy(() -> new RestaurantProfilePage.Address(
        null, null, null, null, null, null, 91.0, 0.0))
        .isInstanceOf(IllegalArgumentException.class);
  }

  private RestaurantProfilePageService service() {
    return new RestaurantProfilePageService(restaurants, new ObjectMapper());
  }

  private static String unescapeHtmlSafeJson(String json) {
    return json.replace("\\u003c", "<").replace("\\u003e", ">").replace("\\u0026", "&");
  }
}
```

Verification:
- Run: `$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-gradle-homes\restaurant-profile-void-seo'; .\gradlew.bat :website:test --tests "dev.christopherbell.view.wfl.RestaurantProfilePageServiceTest" --no-daemon`
- Expected RED: compilation fails because `RestaurantProfilePageService` and `RestaurantProfilePage` do not exist.

- [ ] **Step 2: Add the immutable public page representation**

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePage.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.view.wfl;

import java.util.stream.Stream;

/** Immutable public-only data rendered by a restaurant profile page. */
public record RestaurantProfilePage(
    String id,
    String path,
    String canonicalUrl,
    String title,
    String description,
    String name,
    String cuisine,
    String heroMetadata,
    Address address,
    Rating rating,
    String phoneNumber,
    String website,
    String sourceType,
    String directionsUrl,
    String structuredDataJson
) {
  public RestaurantProfilePage {
    requireNonBlank(id, "Restaurant id");
    requireNonBlank(path, "Restaurant path");
    requireNonBlank(canonicalUrl, "Restaurant canonical URL");
    requireNonBlank(title, "Restaurant title");
    requireNonBlank(description, "Restaurant description");
    requireNonBlank(name, "Restaurant name");
    requireNonBlank(cuisine, "Restaurant display cuisine");
    requireNonBlank(heroMetadata, "Restaurant hero metadata");
    requireNonBlank(directionsUrl, "Restaurant directions URL");
    requireNonBlank(structuredDataJson, "Restaurant structured data");
  }

  /** Returns a display address without invented placeholders or punctuation. */
  public String addressLine() {
    return address == null ? "" : address.displayLine();
  }

  public boolean hasRating() {
    return rating != null;
  }

  public double averageRating() {
    return rating == null ? 0.0 : rating.average();
  }

  /** Public postal and optional coordinate data. */
  public record Address(
      String street1, String street2, String city, String state, String postalCode,
      String country, Double latitude, Double longitude
  ) {
    public Address {
      if ((latitude == null) != (longitude == null)) {
        throw new IllegalArgumentException("Restaurant coordinates must be present as a pair.");
      }
      if (latitude != null && (!Double.isFinite(latitude) || latitude < -90.0 || latitude > 90.0
          || !Double.isFinite(longitude) || longitude < -180.0 || longitude > 180.0)) {
        throw new IllegalArgumentException("Restaurant coordinates are outside valid ranges.");
      }
    }

    public String displayLine() {
      return Stream.of(street1, street2, city, state, postalCode)
          .filter(value -> value != null && !value.isBlank())
          .map(String::strip)
          .collect(java.util.stream.Collectors.joining(", "));
    }

    public boolean hasCoordinates() {
      return latitude != null;
    }
  }

  /** Valid non-empty aggregate rating. */
  public record Rating(int count, int sum) {
    public Rating {
      if (count <= 0 || sum < count || sum > count * 5) {
        throw new IllegalArgumentException("Restaurant rating summary is invalid.");
      }
    }

    public double average() {
      return (double) sum / count;
    }
  }

  private static void requireNonBlank(String value, String label) {
    if (value == null || value.isBlank()) {
      throw new IllegalArgumentException(label + " is required.");
    }
  }
}
```

Verification:
- Run the focused test command; expected RED moves to missing service implementation.

- [ ] **Step 3: Implement the public page builder**

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePageService.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.view.wfl;

import dev.christopherbell.libs.api.exception.InvalidRequestException;
import dev.christopherbell.libs.api.exception.ResourceNotFoundException;
import dev.christopherbell.whatsforlunch.restaurant.RestaurantService;
import dev.christopherbell.whatsforlunch.restaurant.RestaurantWebsiteUrlPolicy;
import dev.christopherbell.whatsforlunch.restaurant.model.RestaurantDetail;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.util.UriComponentsBuilder;
import org.springframework.web.util.UriUtils;
import tools.jackson.core.JacksonException;
import tools.jackson.databind.ObjectMapper;

/** Builds the immutable public page for one canonical restaurant detail. */
@RequiredArgsConstructor
@Service
public class RestaurantProfilePageService {
  private static final String PUBLIC_ROOT = "https://www.christopherbell.dev";
  private static final String MAPS_ROOT = "https://www.google.com/maps/search/";
  private final RestaurantService restaurants;
  private final ObjectMapper objectMapper;

  public RestaurantProfilePage profile(String restaurantId) throws ResourceNotFoundException {
    try {
      return build(restaurants.getRestaurantById(restaurantId));
    } catch (InvalidRequestException invalid) {
      throw new ResourceNotFoundException("Restaurant not found.");
    }
  }

  private RestaurantProfilePage build(RestaurantDetail detail) {
    var id = requiredValue(detail.getId(), "Restaurant id");
    var path = "/wfl/restaurants/" + UriUtils.encodePathSegment(id, StandardCharsets.UTF_8);
    var canonicalUrl = PUBLIC_ROOT + path;
    var name = valueOrFallback(detail.getName(), "Restaurant");
    var publicCuisine = valueOrNull(detail.getCuisine());
    var cuisine = publicCuisine == null ? "Restaurant" : publicCuisine;
    var address = publicAddress(detail.getAddress());
    var location = joinPresent(address == null ? null : address.city(),
        address == null ? null : address.state());
    var hero = location.isEmpty() ? cuisine : cuisine + " restaurant in " + location;
    var description = hero + ". Details and ratings from What's For Lunch.";
    var rating = publicRating(detail.getRatingCount(), detail.getRatingSum());
    var website = RestaurantWebsiteUrlPolicy.safeOrNull(detail.getWebsite());
    var phone = valueOrNull(detail.getPhoneNumber());
    var source = firstPresent(detail.getSourceAmenity(), detail.getType());
    var directions = directionsUrl(name, address);
    var structuredData = structuredData(
        canonicalUrl, name, publicCuisine, address, rating, phone, website);
    return new RestaurantProfilePage(id, path, canonicalUrl, "CB | " + name, description,
        name, cuisine, hero + ".", address, rating, phone, website, source, directions,
        serializeForHtml(structuredData));
  }

  private RestaurantProfilePage.Address publicAddress(
      dev.christopherbell.whatsforlunch.restaurant.model.Address address
  ) {
    if (address == null) return null;
    var latitude = validCoordinate(address.getLatitude(), -90.0, 90.0) ? address.getLatitude() : null;
    var longitude = validCoordinate(address.getLongitude(), -180.0, 180.0) ? address.getLongitude() : null;
    if (latitude == null || longitude == null) {
      latitude = null;
      longitude = null;
    }
    var result = new RestaurantProfilePage.Address(
        valueOrNull(address.getStreet1()), valueOrNull(address.getStreet2()),
        valueOrNull(address.getCity()), valueOrNull(address.getState()),
        valueOrNull(address.getPostalCode()), valueOrNull(address.getCountry()), latitude, longitude);
    return result.displayLine().isEmpty() && !result.hasCoordinates() && result.country() == null
        ? null : result;
  }

  private static RestaurantProfilePage.Rating publicRating(Integer count, Integer sum) {
    if (count == null || sum == null || count <= 0 || sum < count || sum > count * 5) return null;
    return new RestaurantProfilePage.Rating(count, sum);
  }

  private static String directionsUrl(String name, RestaurantProfilePage.Address address) {
    var destination = address != null && address.hasCoordinates()
        ? address.latitude() + "," + address.longitude()
        : joinPresent(name, address == null ? null : address.displayLine());
    return UriComponentsBuilder.fromUriString(MAPS_ROOT)
        .queryParam("api", "1").queryParam("destination", destination).build().encode().toUriString();
  }

  private Map<String, Object> structuredData(
      String canonicalUrl,
      String name,
      String cuisine,
      RestaurantProfilePage.Address address,
      RestaurantProfilePage.Rating rating,
      String phone,
      String website
  ) {
    Map<String, Object> json = new LinkedHashMap<>();
    json.put("@context", "https://schema.org");
    json.put("@type", "Restaurant");
    json.put("name", name);
    if (cuisine != null) json.put("servesCuisine", cuisine);
    json.put("url", canonicalUrl);
    if (address != null && hasPostalAddress(address)) json.put("address", schemaAddress(address));
    if (address != null && address.hasCoordinates()) {
      json.put("geo", Map.of("@type", "GeoCoordinates", "latitude", address.latitude(),
          "longitude", address.longitude()));
    }
    if (phone != null) json.put("telephone", phone);
    if (website != null) json.put("sameAs", website);
    if (rating != null) {
      json.put("aggregateRating", Map.of("@type", "AggregateRating",
          "ratingValue", rating.average(), "ratingCount", rating.count(),
          "bestRating", 5, "worstRating", 1));
    }
    return json;
  }

  private static Map<String, Object> schemaAddress(RestaurantProfilePage.Address address) {
    Map<String, Object> json = new LinkedHashMap<>();
    json.put("@type", "PostalAddress");
    putPresent(json, "streetAddress", joinPresent(address.street1(), address.street2()));
    putPresent(json, "addressLocality", address.city());
    putPresent(json, "addressRegion", address.state());
    putPresent(json, "postalCode", address.postalCode());
    putPresent(json, "addressCountry", address.country());
    return json;
  }

  private static boolean hasPostalAddress(RestaurantProfilePage.Address address) {
    return Stream.of(address.street1(), address.street2(), address.city(), address.state(),
        address.postalCode(), address.country()).anyMatch(value -> value != null && !value.isBlank());
  }

  private String serializeForHtml(Map<String, Object> value) {
    try {
      return objectMapper.writeValueAsString(value)
          .replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e");
    } catch (JacksonException failure) {
      throw new IllegalStateException("Restaurant structured data serialization failed", failure);
    }
  }

  private static void putPresent(Map<String, Object> target, String key, String value) {
    if (value != null && !value.isBlank()) target.put(key, value);
  }

  private static boolean validCoordinate(Double value, double min, double max) {
    return value != null && Double.isFinite(value) && value >= min && value <= max;
  }

  private static String requiredValue(String value, String label) {
    if (value == null || value.isBlank()) throw new IllegalStateException(label + " is missing.");
    return value.strip();
  }

  private static String valueOrFallback(String value, String fallback) {
    var present = valueOrNull(value);
    return present == null ? fallback : present;
  }

  private static String valueOrNull(String value) {
    return value == null || value.isBlank() ? null : value.strip();
  }

  private static String firstPresent(String... values) {
    for (var value : values) {
      var present = valueOrNull(value);
      if (present != null) return present;
    }
    return null;
  }

  private static String joinPresent(String... values) {
    List<String> present = new ArrayList<>();
    for (var value : values) {
      var normalized = valueOrNull(value);
      if (normalized != null) present.add(normalized);
    }
    return String.join(", ", present);
  }
}
```

Verification:
- Run the focused service test and require GREEN.
- Run `git diff --check`.

- [ ] **Step 4: Commit the public page boundary**

```powershell
git add website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePage.java `
  website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePageService.java `
  website/src/test/java/dev/christopherbell/view/wfl/RestaurantProfilePageServiceTest.java
git commit -m "Render public restaurant profile data"
```

Task-level verification:
- `:website:test --tests "dev.christopherbell.view.wfl.RestaurantProfilePageServiceTest"` passes.
- `rg "myRating|myFavorite|createdBy|lastModified" website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePage*` finds nothing.

### Task 2 - Server-render the complete indexable profile

Sequence / dependencies:
- Runs after Task 1 because the controller and template consume `RestaurantProfilePage`.

Expected files:
- Modify `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`.
- Delete `website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreview.java`.
- Delete `website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreviewService.java`.
- Replace `website/src/main/resources/templates/restaurant.html`.
- Modify `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`.

Interfaces:
- Consumes: `RestaurantProfilePageService.profile(String)`.
- Produces: model attribute `restaurantProfile`; raw semantic HTML, canonical/social metadata, JSON-LD, member mount `#restaurant-member-controls` with `data-restaurant-id`.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke it together with `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: Valid profiles return complete public content and JSON-LD without JavaScript; missing profiles retain the content-free noindex 404.
  - Invariants: One H1 and one main landmark; dynamic text remains escaped; only pre-serialized HTML-safe JSON uses unescaped output; external links are already policy-validated and carry safe rel attributes.
  - Boundary/API: The route and URL remain `/wfl/restaurants/{restaurantId}`; only the internal model/service name changes.
  - Effects and failures: Controller performs one page-service call; absence maps to 404; unexpected mapping/serialization faults remain 5xx rather than false 404.
  - Tests and evidence: RED MockMvc assertions require raw address/rating/contact/source content, Void stylesheet/classes, JSON-LD, privacy absence, canonical URL, and unchanged noindex 404; GREEN is focused controller tests.

- [ ] **Step 1: Add raw public-profile assertions and witness RED**

#### Code Edit 2.0
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: 158-174
- Action: replace

Current:
```java
@Test
@DisplayName("WFL restaurant page renders social preview metadata")
public void getWhatsForLunchRestaurantPage_rendersSocialPreviewMetadata() throws Exception {
  when(restaurantPreviews.preview("restaurant-123")).thenReturn(new RestaurantSocialPreview(
      "CB | Taco Place",
      "Mexican restaurant in Austin, Texas. Details and ratings from What's For Lunch.",
      "Taco Place",
      "Mexican restaurant in Austin, Texas."));

  mockMvc
      .perform(get("/wfl/restaurants/restaurant-123"))
      .andExpect(status().isOk())
      .andExpect(content().string(containsString("CB | Taco Place")))
      .andExpect(content().string(containsString("Mexican restaurant in Austin, Texas")))
      .andExpect(content().string(containsString("<h1 id=\"restaurantTitle\">Taco Place</h1>")))
      .andExpect(content().string(containsString("https://www.christopherbell.dev/wfl/restaurants/restaurant-123")));
}
```

Proposed:
```java
@Test
@DisplayName("WFL restaurant page renders complete public indexable content")
void getWhatsForLunchRestaurantPageRendersPublicProfile() throws Exception {
  when(restaurantPreviews.preview("restaurant-123")).thenReturn(new RestaurantSocialPreview(
      "CB | Taco Place",
      "Mexican restaurant in Austin, Texas. Details and ratings from What's For Lunch.",
      "Taco Place",
      "Mexican restaurant in Austin, Texas."));

  mockMvc.perform(get("/wfl/restaurants/restaurant-123"))
      .andExpect(status().isOk())
      .andExpect(content().string(containsString("CB | Taco Place")))
      .andExpect(content().string(containsString("100 Main St, Austin, TX, 78701")))
      .andExpect(content().string(containsString("4.5/5 from 2 ratings")))
      .andExpect(content().string(containsString("href=\"/css/whats-for-lunch.css\"")))
      .andExpect(content().string(containsString("type=\"application/ld+json\"")));
}
```

Verification:
- Run focused `ViewControllerTest` before any production or mock migration edit.
- Expected RED: response is `200`, but the raw address/rating/Void stylesheet/JSON-LD assertions fail because those facts are absent from the current template and metadata-only preview type.

- [ ] **Step 2: Migrate the test fixture to the approved public page boundary**

#### Code Edit 2.1a
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: 19-20
- Action: replace

Current:
```java
import dev.christopherbell.view.wfl.RestaurantSocialPreview;
import dev.christopherbell.view.wfl.RestaurantSocialPreviewService;
```

Proposed:
```java
import dev.christopherbell.view.wfl.RestaurantProfilePage;
import dev.christopherbell.view.wfl.RestaurantProfilePageService;
```

Verification:
- The test source resolves only the new public page types.

#### Code Edit 2.1b
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: 46
- Action: replace

Current:
```java
@MockitoBean private RestaurantSocialPreviewService restaurantPreviews;
```

Proposed:
```java
@MockitoBean private RestaurantProfilePageService restaurantProfiles;
```

Verification:
- `@WebMvcTest` receives a mock for the controller's new constructor dependency.

#### Code Edit 2.1c
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: 158-174
- Action: replace

Current:
```java
@Test
@DisplayName("WFL restaurant page renders complete public indexable content")
void getWhatsForLunchRestaurantPageRendersPublicProfile() throws Exception {
  when(restaurantPreviews.preview("restaurant-123")).thenReturn(new RestaurantSocialPreview(
      "CB | Taco Place",
      "Mexican restaurant in Austin, Texas. Details and ratings from What's For Lunch.",
      "Taco Place",
      "Mexican restaurant in Austin, Texas."));

  mockMvc.perform(get("/wfl/restaurants/restaurant-123"))
      .andExpect(status().isOk())
      .andExpect(content().string(containsString("CB | Taco Place")))
      .andExpect(content().string(containsString("100 Main St, Austin, TX, 78701")))
      .andExpect(content().string(containsString("4.5/5 from 2 ratings")))
      .andExpect(content().string(containsString("href=\"/css/whats-for-lunch.css\"")))
      .andExpect(content().string(containsString("type=\"application/ld+json\"")));
}
```

Proposed:
```java
@Test
@DisplayName("WFL restaurant page renders complete public indexable content")
void getWhatsForLunchRestaurantPageRendersPublicProfile() throws Exception {
  when(restaurantProfiles.profile("restaurant-123")).thenReturn(profilePage());

  mockMvc.perform(get("/wfl/restaurants/restaurant-123"))
      .andExpect(status().isOk())
      .andExpect(content().string(containsString("CB | Taco Place")))
      .andExpect(content().string(containsString("rel=\"canonical\" href=\"https://www.christopherbell.dev/wfl/restaurants/restaurant-123\"")))
      .andExpect(content().string(containsString("href=\"/css/whats-for-lunch.css\"")))
      .andExpect(content().string(containsString("void-shell-page lunch-page lunch-void-page restaurant-profile-page")))
      .andExpect(content().string(containsString("<h1 id=\"restaurantTitle\">Taco Place</h1>")))
      .andExpect(content().string(containsString("100 Main St, Austin, TX, 78701")))
      .andExpect(content().string(containsString("4.5/5 from 2 ratings")))
      .andExpect(content().string(containsString("512-555-0100")))
      .andExpect(content().string(containsString("https://example.com/menu")))
      .andExpect(content().string(containsString("type=\"application/ld+json\"")))
      .andExpect(content().string(containsString("\"@type\":\"Restaurant\"")))
      .andExpect(content().string(not(containsString("noindex"))))
      .andExpect(content().string(not(containsString("myRating"))))
      .andExpect(content().string(not(containsString("private-account"))));
}
```

Verification:
- The test now describes the complete reviewed page model while retaining the same RED expectations.

#### Code Edit 2.1d
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: after 174
- Action: add

Proposed:
```java

private static RestaurantProfilePage profilePage() {
  return new RestaurantProfilePage(
      "restaurant-123", "/wfl/restaurants/restaurant-123",
      "https://www.christopherbell.dev/wfl/restaurants/restaurant-123", "CB | Taco Place",
      "Mexican restaurant in Austin, TX. Details and ratings from What's For Lunch.",
      "Taco Place", "Mexican", "Mexican restaurant in Austin, TX.",
      new RestaurantProfilePage.Address("100 Main St", null, "Austin", "TX", "78701",
          "US", 30.2672, -97.7431),
      new RestaurantProfilePage.Rating(2, 9), "512-555-0100", "https://example.com/menu",
      "restaurant", "https://www.google.com/maps/search/?api=1&destination=30.2672%2C-97.7431",
      "{\"@context\":\"https://schema.org\",\"@type\":\"Restaurant\",\"name\":\"Taco Place\"}");
}
```

Verification:
- The fixture contains only fields available to the public template.

#### Code Edit 2.1e
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: 194-204
- Action: replace

Current:
```java
@Test
void getWhatsForLunchRestaurantPage_whenMissing_returnsNoIndex404() throws Exception {
  when(restaurantPreviews.preview("missing-restaurant"))
      .thenThrow(new ResourceNotFoundException("SECRET_RESTAURANT"));

  mockMvc.perform(get("/wfl/restaurants/missing-restaurant"))
      .andExpect(status().isNotFound())
      .andExpect(content().string(containsString("Page not found")))
      .andExpect(content().string(containsString("noindex,nofollow")))
      .andExpect(content().string(not(containsString("SECRET_RESTAURANT"))));
}
```

Proposed:
```java
@Test
void getWhatsForLunchRestaurantPage_whenMissing_returnsNoIndex404() throws Exception {
  when(restaurantProfiles.profile("missing-restaurant"))
      .thenThrow(new ResourceNotFoundException("SECRET_RESTAURANT"));

  mockMvc.perform(get("/wfl/restaurants/missing-restaurant"))
      .andExpect(status().isNotFound())
      .andExpect(content().string(containsString("Page not found")))
      .andExpect(content().string(containsString("noindex,nofollow")))
      .andExpect(content().string(not(containsString("application/ld+json"))))
      .andExpect(content().string(not(containsString("SECRET_RESTAURANT"))));
}
```

Verification:
- Compile the focused test source; route assertions remain RED until the controller/template steps.

- [ ] **Step 3: Change the controller to pass only the public page model**

#### Code Edit 2.2a
- File: `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- Lines: 6
- Action: delete

Current:
```java
import java.nio.charset.StandardCharsets;
```

Proposed:
```text
delete block
```

Verification:
- The compiler reports no unused `StandardCharsets` import after the route block changes.

#### Code Edit 2.2b
- File: `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- Lines: 12
- Action: delete

Current:
```java
import org.springframework.web.util.UriUtils;
```

Proposed:
```text
delete block
```

Verification:
- The controller delegates canonical encoding to the page service.

#### Code Edit 2.2c
- File: `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- Lines: 21
- Action: replace

Current:
```java
private final RestaurantSocialPreviewService restaurantPreviews;
```

Proposed:
```java
private final RestaurantProfilePageService restaurantProfiles;
```

Verification:
- Lombok's generated constructor requires the new focused dependency.

#### Code Edit 2.2d
- File: `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- Lines: 76-84
- Action: replace

Current:
```java
var encodedRestaurantId = UriUtils.encodePathSegment(restaurantId, StandardCharsets.UTF_8);
model.addAttribute("socialUrl", PUBLIC_ROOT + "/wfl/restaurants/" + encodedRestaurantId);
try {
  var preview = restaurantPreviews.preview(restaurantId);
  model.addAttribute("socialTitle", preview.title());
  model.addAttribute("socialDescription", preview.description());
  model.addAttribute("restaurantName", preview.name());
  model.addAttribute("restaurantHeroMetadata", preview.heroMetadata());
  return "restaurant.html";
```

Proposed:
```java
try {
  model.addAttribute("restaurantProfile", restaurantProfiles.profile(restaurantId));
  return "restaurant.html";
```

Retain the current catch block at lines 85-88 and `PUBLIC_ROOT` because the Favorites and Top Rated routes still use them.

Verification:
- Compile focused tests; expected failures now identify missing template output rather than controller/service symbols.

- [ ] **Step 4: Retire the metadata-only preview types after all consumers switch**

#### Code Edit 2.2e
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreviewService.java`
- Lines: 1-48
- Action: delete

Current:
```java
package dev.christopherbell.view.wfl;

import dev.christopherbell.libs.api.exception.InvalidRequestException;
import dev.christopherbell.libs.api.exception.ResourceNotFoundException;
import dev.christopherbell.whatsforlunch.restaurant.RestaurantService;
import java.util.ArrayList;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/** Builds public metadata from the canonical restaurant detail projection. */
@RequiredArgsConstructor
@Service
public class RestaurantSocialPreviewService {
  private final RestaurantService restaurants;

  /** Returns safe public metadata for an existing restaurant. */
  public RestaurantSocialPreview preview(String restaurantId) throws ResourceNotFoundException {
    try {
      var restaurant = restaurants.getRestaurantById(restaurantId);
      var name = valueOrFallback(restaurant.getName(), "Restaurant");
      var location = locationParts(
          restaurant.getAddress() == null ? null : restaurant.getAddress().getCity(),
          restaurant.getAddress() == null ? null : restaurant.getAddress().getState());
      var cuisine = valueOrFallback(restaurant.getCuisine(), "Restaurant");
      var heroMetadata = location.isEmpty() ? cuisine : cuisine + " restaurant in " + location;
      var description = heroMetadata + ". Details and ratings from What's For Lunch.";
      return new RestaurantSocialPreview("CB | " + name, description, name, heroMetadata + ".");
    } catch (InvalidRequestException exception) {
      throw new ResourceNotFoundException("Restaurant not found.");
    }
  }

  private static String locationParts(String city, String state) {
    List<String> parts = new ArrayList<>();
    if (city != null && !city.isBlank()) parts.add(city.strip());
    if (state != null && !state.isBlank()) parts.add(state.strip());
    return String.join(", ", parts);
  }

  private static String valueOrFallback(String value, String fallback) {
    return value == null || value.isBlank() ? fallback : value.strip();
  }
}
```

Proposed:
```text
delete block
```

Verification:
- The controller and tests compile without this Spring service.

#### Code Edit 2.2f
- File: `website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreview.java`
- Lines: 1-9
- Action: delete

Current:
```java
package dev.christopherbell.view.wfl;

/** Public, server-rendered metadata for a restaurant page. */
public record RestaurantSocialPreview(
    String title,
    String description,
    String name,
    String heroMetadata
) {}
```

Proposed:
```text
delete block
```

Verification:
- `rg "RestaurantSocialPreview" website/src/main website/src/test` returns no references.

- [ ] **Step 5: Replace the client-only mount with semantic server HTML**

#### Code Edit 2.3
- File: `website/src/main/resources/templates/restaurant.html`
- Lines: 1-39
- Action: replace

Current:
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell (cbell7@icloud.com)" />
    <th:block th:replace="~{fragments/social-preview :: socialPreview(${socialTitle}, ${socialDescription}, ${socialUrl}, 'https://www.christopherbell.dev/images/previews/christopherbell-dev.png', 'The Void preview for christopherbell.dev')}"></th:block>

    <title th:text="${socialTitle}">CB | Restaurant</title>

    <link rel="stylesheet" type="text/css" href="/css/main.css" th:href="@{/css/main.css}"/>
</head>

<body class="site-page lunch-page restaurant-profile-page">
    <div id="nav"></div>
    <main class="site-main" role="main">
        <section class="site-hero site-hero-lunch" aria-labelledby="restaurantTitle">
            <div class="container">
                <p class="home-kicker">What's For Lunch</p>
                <h1 id="restaurantTitle" th:text="${restaurantName}">Restaurant</h1>
                <p id="restaurantHeroText" th:text="${restaurantHeroMetadata}">Details, ratings, and ways to get there.</p>
            </div>
        </section>
        <section class="site-content">
            <div class="container">
                <div class="content-panel lunch-panel">
                    <div id="restaurant-profile"></div>
                </div>
            </div>
        </section>
    </main>
    <footer id="footer"></footer>
</body>

<script type="module" src="/js/app.js" th:src="@{/js/app.js}"></script>
<script type="module" src="/js/restaurant-profile.js" th:src="@{/js/restaurant-profile.js}"></script>

</html>
```

Proposed:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell (cbell7@icloud.com)" />
    <th:block th:replace="~{fragments/social-preview :: socialPreview(${restaurantProfile.title}, ${restaurantProfile.description}, ${restaurantProfile.canonicalUrl}, 'https://www.christopherbell.dev/images/previews/christopherbell-dev.png', 'The Void preview for christopherbell.dev')}"></th:block>
    <title th:text="${restaurantProfile.title}">CB | Restaurant</title>
    <link rel="stylesheet" type="text/css" href="/css/main.css" th:href="@{/css/main.css}"/>
    <link rel="stylesheet" type="text/css" href="/css/whats-for-lunch.css"
          th:href="@{/css/whats-for-lunch.css}"/>
    <script type="application/ld+json" th:utext="${restaurantProfile.structuredDataJson}">{"@context":"https://schema.org","@type":"Restaurant"}</script>
</head>
<body class="site-page void-shell-page lunch-page lunch-void-page restaurant-profile-page">
    <div id="nav"></div>
    <main class="site-main lunch-void-main" aria-labelledby="restaurantTitle">
        <div class="lunch-void-shell">
            <div class="container lunch-void-container restaurant-profile-container">
                <nav class="wfl-secondary-nav" aria-label="What's For Lunch navigation">
                    <a href="/wfl">Picks</a>
                    <a href="/wfl/top-rated">Top 10 Rated</a>
                    <a href="/wfl/favorites">Favorites</a>
                </nav>
                <header class="lunch-void-hero restaurant-profile-hero">
                    <p class="home-kicker">Restaurant signal</p>
                    <h1 id="restaurantTitle" th:text="${restaurantProfile.name}">Restaurant</h1>
                    <p th:text="${restaurantProfile.heroMetadata}">Restaurant details.</p>
                </header>
                <article class="restaurant-profile-void" aria-label="Restaurant profile">
                    <section class="restaurant-rating-signal" aria-labelledby="restaurantRatingTitle">
                        <p class="restaurant-profile-label">Public signal</p>
                        <h2 id="restaurantRatingTitle">Aggregate rating</h2>
                        <p id="restaurant-public-rating" class="restaurant-rating-value"
                           th:if="${restaurantProfile.hasRating()}"
                           th:text="${#numbers.formatDecimal(restaurantProfile.averageRating(), 1, 1) + '/5 from ' + restaurantProfile.rating.count + (restaurantProfile.rating.count == 1 ? ' rating' : ' ratings')}">4.5/5 from 2 ratings</p>
                        <p id="restaurant-public-rating" class="restaurant-rating-value"
                           th:unless="${restaurantProfile.hasRating()}">No ratings yet</p>
                        <p th:text="${restaurantProfile.cuisine}">Restaurant</p>
                    </section>
                    <section class="restaurant-profile-details" aria-labelledby="restaurantDetailsTitle">
                        <h2 id="restaurantDetailsTitle">Restaurant details</h2>
                        <dl class="restaurant-detail-list">
                            <div th:if="${!restaurantProfile.addressLine().isEmpty()}">
                                <dt>Address</dt><dd th:text="${restaurantProfile.addressLine()}">Address</dd>
                            </div>
                            <div th:if="${restaurantProfile.phoneNumber != null}">
                                <dt>Phone</dt><dd><a th:href="${'tel:' + restaurantProfile.phoneNumber}"
                                    th:text="${restaurantProfile.phoneNumber}">Phone</a></dd>
                            </div>
                            <div th:if="${restaurantProfile.website != null}">
                                <dt>Website</dt><dd><a th:href="${restaurantProfile.website}" target="_blank"
                                    rel="noopener noreferrer">Visit website</a></dd>
                            </div>
                            <div th:if="${restaurantProfile.sourceType != null}">
                                <dt>Source type</dt><dd th:text="${restaurantProfile.sourceType}">Restaurant</dd>
                            </div>
                        </dl>
                        <div class="restaurant-profile-actions">
                            <a class="btn btn-primary" th:href="${restaurantProfile.directionsUrl}"
                               target="_blank" rel="noopener noreferrer">Open in Maps</a>
                            <a class="btn btn-outline-secondary" href="/wfl">Back to WFL</a>
                        </div>
                    </section>
                    <section class="restaurant-member-panel" aria-labelledby="restaurantMemberTitle">
                        <p class="restaurant-profile-label">Member controls</p>
                        <h2 id="restaurantMemberTitle">Your signal</h2>
                        <div id="restaurant-member-controls" aria-live="polite"
                             th:attr="data-restaurant-id=${restaurantProfile.id}">
                            <p>Sign in to rate or favorite this restaurant.</p>
                            <a class="btn btn-outline-primary"
                               th:href="@{/login(redirect=${restaurantProfile.path})}">Sign in</a>
                        </div>
                    </section>
                </article>
            </div>
        </div>
    </main>
    <footer id="footer"></footer>
    <script type="module" src="/js/app.js" th:src="@{/js/app.js}"></script>
    <script type="module" src="/js/restaurant-profile.js" th:src="@{/js/restaurant-profile.js}"></script>
</body>
</html>
```

Verification:
- Run focused `ViewControllerTest`; require GREEN.
- Inspect rendered test HTML to confirm exactly one H1/main, escaped dynamic fields, canonical URL, raw public fields, and parseable JSON-LD.

- [ ] **Step 6: Commit server rendering**

```powershell
git add website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java `
  website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreview.java `
  website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreviewService.java `
  website/src/main/resources/templates/restaurant.html `
  website/src/test/java/dev/christopherbell/view/ViewControllerTest.java
git commit -m "Server render restaurant profiles"
```

Task-level verification:
- Focused service and controller test classes pass together.
- Missing profile still returns `404`, contains `noindex,nofollow`, omits the secret exception message, and contains no `application/ld+json` Restaurant object.

### Task 3 - Convert restaurant JavaScript to member-only enhancement

Sequence / dependencies:
- Runs after Task 2 because the entry module now targets `#restaurant-member-controls` and leaves public HTML intact.

Expected files:
- Replace `website/src/main/resources/static/js/restaurant-profile.js`.
- Create `website/src/test/js/restaurant-profile.test.js`.

Interfaces:
- Consumes: server-rendered `data-restaurant-id`, UI-only `getAuthClaims()`, existing API URLs, `fetchJson`, `authHeaders`, `ratingSummary`, and `sanitize`.
- Produces: exported `initializeRestaurantProfile(options)` for behavioral tests and automatic browser initialization; member controls only.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke it together with `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: Anonymous visitors make zero detail requests; signed-in visitors receive personal controls; member failures never replace public content; rating/favorite mutations remain functional.
  - Invariants: API response is used only after the existing fetch boundary; untrusted strings are escaped; every promise is awaited; one module-local state object owns the current member detail.
  - Boundary/API: Existing restaurant/rating/favorite endpoints and DOM IDs remain stable; the removed `#restaurant-profile` full-page renderer has no consumer after Task 2.
  - Effects and failures: Network work occurs only with a browser-session marker; `401` restores anonymous controls without an error banner; other faults render locally; mutation failures preserve controls.
  - Tests and evidence: RED behavioral tests use injected request/claims and a small fake mount to prove request count, signed-in rendering, local fallback, and mutation method/body; GREEN is the same Node test file plus full `jsTest`.

- [ ] **Step 1: Add behavioral initialization/mutation tests and witness RED**

#### Code Edit 3.1
- File: `website/src/test/js/restaurant-profile.test.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
import assert from 'node:assert/strict';
import test from 'node:test';

globalThis.localStorage = { getItem: () => null, removeItem() {}, setItem() {} };
globalThis.document = { cookie: '', getElementById: () => null };
globalThis.window = {
  location: { origin: 'https://www.christopherbell.dev', pathname: '/wfl/restaurants/restaurant-123' },
};
const profileModule = await import('../../main/resources/static/js/restaurant-profile.js');
const { initializeRestaurantProfile } = profileModule;

function requireInitializer() {
  assert.equal(typeof initializeRestaurantProfile, 'function',
    'restaurant profile must export its progressive-enhancement boundary');
}

function mount(id = 'restaurant-123') {
  return {
    dataset: { restaurantId: id },
    innerHTML: '<p>Sign in to rate or favorite this restaurant.</p>',
    listener: null,
    addEventListener(_type, listener) { this.listener = listener; },
    insertAdjacentHTML(_position, html) { this.innerHTML += html; },
  };
}

const DETAIL = Object.freeze({
  id: 'restaurant-123', name: 'Taco Place', ratingCount: 2, ratingSum: 9,
  myRating: 4, myFavorite: true,
});

test('anonymous profile keeps server fallback and makes no detail request', async () => {
  requireInitializer();
  const memberMount = mount();
  let requests = 0;
  await initializeRestaurantProfile({
    mount: memberMount,
    claims: () => null,
    request: async () => { requests += 1; return DETAIL; },
  });

  assert.equal(requests, 0);
  assert.match(memberMount.innerHTML, /Sign in to rate or favorite/);
});

test('signed-in profile renders only personal controls from the detail response', async () => {
  requireInitializer();
  const memberMount = mount();
  const urls = [];
  await initializeRestaurantProfile({
    mount: memberMount,
    claims: () => ({ sub: 'browser-session' }),
    request: async (url) => { urls.push(url); return DETAIL; },
    headers: () => ({ 'X-Test': 'yes' }),
  });

  assert.deepEqual(urls, ['/api/whatsforlunch/restaurant/2026-05-17/profile/restaurant-123']);
  assert.match(memberMount.innerHTML, /Your rating: 4\/5/);
  assert.match(memberMount.innerHTML, /Favorited/);
  assert.doesNotMatch(memberMount.innerHTML, /100 Main|Phone|Website|Source type/);
});

test('member load failure stays local and preserves the anonymous fallback', async () => {
  requireInitializer();
  const memberMount = mount();
  await initializeRestaurantProfile({
    mount: memberMount,
    claims: () => ({ sub: 'browser-session' }),
    request: async () => { throw new Error('Service unavailable'); },
  });

  assert.match(memberMount.innerHTML, /Sign in to rate or favorite/);
  assert.match(memberMount.innerHTML, /Service unavailable/);
});

test('stale browser session restores sign-in fallback without an error banner', async () => {
  requireInitializer();
  const memberMount = mount();
  const unauthorized = Object.assign(new Error('Authentication required.'), { status: 401 });
  await initializeRestaurantProfile({
    mount: memberMount,
    claims: () => ({ sub: 'browser-session' }),
    request: async () => { throw unauthorized; },
  });

  assert.match(memberMount.innerHTML, /Sign in to rate or favorite/);
  assert.doesNotMatch(memberMount.innerHTML, /alert-danger|Authentication required/);
});

test('rating interaction sends the existing mutation contract', async () => {
  requireInitializer();
  const memberMount = mount();
  const calls = [];
  await initializeRestaurantProfile({
    mount: memberMount,
    claims: () => ({ sub: 'browser-session' }),
    request: async (url, options = {}) => {
      calls.push([url, options]);
      return calls.length === 1 ? DETAIL : { ...DETAIL, myRating: 5, ratingCount: 3, ratingSum: 14 };
    },
    headers: (extra = {}) => extra,
  });
  await memberMount.listener({ target: { closest: selector => selector === '.lunch-rating-button'
    ? { dataset: { rating: '5' } } : null } });

  assert.equal(calls[1][0], '/api/whatsforlunch/restaurant/2026-05-17/rating');
  assert.equal(calls[1][1].method, 'PUT');
  assert.equal(calls[1][1].body, '{"restaurantId":"restaurant-123","rating":5}');
  assert.match(memberMount.innerHTML, /Your rating: 5\/5/);
});

test('favorite interaction preserves the existing method and payload contract', async () => {
  requireInitializer();
  const memberMount = mount();
  const calls = [];
  await initializeRestaurantProfile({
    mount: memberMount,
    claims: () => ({ sub: 'browser-session' }),
    request: async (url, options = {}) => {
      calls.push([url, options]);
      return calls.length === 1 ? DETAIL : { ...DETAIL, myFavorite: false };
    },
    headers: (extra = {}) => extra,
  });
  await memberMount.listener({ target: { closest: selector => selector === '.restaurant-favorite-toggle'
    ? {} : null } });

  assert.equal(calls[1][0], '/api/whatsforlunch/restaurant/2026-05-17/favorite');
  assert.equal(calls[1][1].method, 'DELETE');
  assert.equal(calls[1][1].body, '{"restaurantId":"restaurant-123"}');
  assert.match(memberMount.innerHTML, /> Favorite<\/button>/);
});
```

Verification:
- Run: `$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-gradle-homes\restaurant-profile-void-seo'; .\gradlew.bat :website:jsTest --no-daemon`
- Expected RED: each behavioral test fails the `requireInitializer()` assertion because the old module does not export the progressive-enhancement boundary; the guarded document fixture prevents an unrelated DOM-reference error.

- [ ] **Step 2: Replace full-page rendering with progressive enhancement**

#### Code Edit 3.2
- File: `website/src/main/resources/static/js/restaurant-profile.js`
- Lines: 1-171
- Action: replace

Current:
```javascript
import { API } from './lib/api.js';
import { authHeaders, fetchJson, getAuthClaims, loginRedirectUrl, sanitize } from './lib/util.js';
import { appendSafeHttpLink } from './lib/safe-http-link.js';
import {
  ratingSummary,
  restaurantAddressLine,
  wflSecondaryNavigation,
} from './lib/wfl-ui.js';

const mount = document.getElementById('restaurant-profile');
const title = document.getElementById('restaurantTitle');
const heroText = document.getElementById('restaurantHeroText');
const RATING_OPTIONS = [1, 2, 3, 4, 5];
let currentRestaurant = null;
let isLoggedIn = false;

function restaurantIdFromPath() {
  const match = window.location.pathname.match(/\/wfl\/restaurants\/([^/]+)$/);
  return match ? decodeURIComponent(match[1]) : '';
}

function ratingMarkup(restaurant) {
  const { myRating, overall } = ratingSummary(restaurant);
  if (!isLoggedIn) {
    return `<p class="restaurant-profile-rating">Rating: ${overall}</p>`;
  }
  return `
    <div class="restaurant-profile-rating">
      <p>Overall rating: ${overall}</p>
      <p>Your rating: ${myRating > 0 ? `${myRating}/5` : 'Not rated'}</p>
    </div>
    <div class="lunch-rating-control" aria-label="Rate ${sanitize(restaurant.name || 'restaurant')}">
      ${RATING_OPTIONS.map((value) => `
        <button type="button" class="lunch-rating-button ${myRating === value ? 'active' : ''}" data-rating="${value}" aria-label="Rate ${value} out of 5">${value}</button>
      `).join('')}
    </div>
  `;
}

function mapsUrl(restaurant) {
  const address = restaurant.address || {};
  const destination = address.latitude && address.longitude
    ? `${address.latitude},${address.longitude}`
    : [restaurant.name, restaurantAddressLine(address, true)].filter(Boolean).join(', ');
  const params = new URLSearchParams({ api: '1', destination });
  return `https://www.google.com/maps/search/?${params}`;
}

function renderRestaurant(restaurant) {
  currentRestaurant = restaurant;
  const address = restaurantAddressLine(restaurant.address, true);
  const favoriteAction = isLoggedIn
    ? `<button type="button" class="btn ${restaurant.myFavorite ? 'btn-success' : 'btn-outline-success'} restaurant-favorite-toggle" aria-pressed="${restaurant.myFavorite ? 'true' : 'false'}">
        <span aria-hidden="true">&hearts;</span> ${restaurant.myFavorite ? 'Favorited' : 'Favorite'}
      </button>`
    : `<a class="btn btn-outline-success" href="${sanitize(loginRedirectUrl())}">Sign in to favorite</a>`;
  if (title) title.textContent = restaurant.name || 'Restaurant';
  if (heroText) heroText.textContent = address || 'Restaurant details from What\'s For Lunch.';
  mount.innerHTML = `
    ${wflSecondaryNavigation('picks')}
    <article class="restaurant-profile">
      <div>
        <p class="home-kicker mb-2">${sanitize(restaurant.cuisine || 'Restaurant')}</p>
        <h2>${sanitize(restaurant.name || 'Restaurant')}</h2>
        ${ratingMarkup(restaurant)}
        ${address ? `<p>${sanitize(address)}</p>` : ''}
      </div>
      <dl class="restaurant-detail-list">
        <div>
          <dt>Phone</dt>
          <dd>${restaurant.phoneNumber ? `<a href="tel:${sanitize(restaurant.phoneNumber)}">${sanitize(restaurant.phoneNumber)}</a>` : 'Not listed'}</dd>
        </div>
        <div>
          <dt>Website</dt>
          <dd class="restaurant-website">${restaurant.website ? '' : 'Not listed'}</dd>
        </div>
        <div>
          <dt>Source type</dt>
          <dd>${sanitize(restaurant.sourceAmenity || 'Not listed')}</dd>
        </div>
      </dl>
      <div class="lunch-pick-actions">
        ${favoriteAction}
        <a class="btn btn-primary" href="${sanitize(mapsUrl(restaurant))}" target="_blank" rel="noopener">Open in Maps</a>
        <a class="btn btn-outline-secondary" href="/wfl">Back to WFL</a>
      </div>
    </article>
  `;
  appendSafeHttpLink(mount.querySelector('.restaurant-website'), restaurant.website, {
    label: restaurant.website,
  });
}

async function loadRestaurant() {
  if (!mount) return;
  isLoggedIn = !!getAuthClaims()?.sub;
  const restaurantId = restaurantIdFromPath();
  if (!restaurantId) {
    mount.innerHTML = '<div class="lunch-empty"><h2>Restaurant not found</h2></div>';
    return;
  }
  mount.innerHTML = '<div class="lunch-empty"><p>Loading restaurant...</p></div>';
  try {
    const restaurant = await fetchJson(API.whatsForLunch.restaurant(restaurantId), {
      headers: authHeaders(),
    });
    renderRestaurant(restaurant);
  } catch (err) {
    mount.innerHTML = `
      <div class="lunch-empty">
        <h2>Could not load restaurant</h2>
        <p>${sanitize(err.message || 'Please try again later.')}</p>
        <a class="btn btn-outline-secondary" href="/wfl">Back to WFL</a>
      </div>
    `;
  }
}

async function rateRestaurant(rating) {
  const restaurantId = currentRestaurant?.id;
  const selectedRating = Number.parseInt(String(rating), 10);
  if (!restaurantId || !RATING_OPTIONS.includes(selectedRating)) return;
  try {
    const updatedRestaurant = await fetchJson(API.whatsForLunch.rateRestaurant, {
      method: 'PUT',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ restaurantId, rating: selectedRating }),
    });
    renderRestaurant(updatedRestaurant);
  } catch (err) {
    mount.insertAdjacentHTML('afterbegin', `
      <div class="alert alert-danger" role="alert">${sanitize(err.message || 'Could not save rating.')}</div>
    `);
  }
}

async function toggleFavorite() {
  const restaurantId = currentRestaurant?.id;
  if (!restaurantId) return;
  try {
    const updatedRestaurant = await fetchJson(API.whatsForLunch.favoriteRestaurant, {
      method: currentRestaurant.myFavorite ? 'DELETE' : 'PUT',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ restaurantId }),
    });
    renderRestaurant(updatedRestaurant);
  } catch (err) {
    mount.insertAdjacentHTML('afterbegin', `
      <div class="alert alert-danger" role="alert">${sanitize(err.message || 'Could not update favorite.')}</div>
    `);
  }
}

mount?.addEventListener('click', async (event) => {
  const ratingButton = event.target instanceof Element
    ? event.target.closest('.lunch-rating-button')
    : null;
  if (ratingButton) {
    await rateRestaurant(ratingButton.dataset.rating);
    return;
  }

  const favoriteButton = event.target instanceof Element
    ? event.target.closest('.restaurant-favorite-toggle')
    : null;
  if (favoriteButton) {
    await toggleFavorite();
  }
});

loadRestaurant();
```

Proposed:
```javascript
import { API } from './lib/api.js';
import { authHeaders, fetchJson, getAuthClaims, sanitize } from './lib/util.js';
import { ratingSummary } from './lib/wfl-ui.js';

const RATING_OPTIONS = Object.freeze([1, 2, 3, 4, 5]);

function memberMarkup(restaurant) {
  const { myRating } = ratingSummary(restaurant);
  return `
    <p>Your rating: ${myRating > 0 ? `${myRating}/5` : 'Not rated'}</p>
    <div class="lunch-rating-control" role="group" aria-label="Rate ${sanitize(restaurant.name || 'restaurant')}">
      ${RATING_OPTIONS.map(value => `
        <button type="button" class="lunch-rating-button ${myRating === value ? 'active' : ''}"
          data-rating="${value}" aria-label="Rate ${value} out of 5">${value}</button>
      `).join('')}
    </div>
    <button type="button"
      class="btn ${restaurant.myFavorite ? 'btn-success' : 'btn-outline-success'} restaurant-favorite-toggle"
      aria-pressed="${restaurant.myFavorite ? 'true' : 'false'}">
      <span aria-hidden="true">&hearts;</span> ${restaurant.myFavorite ? 'Favorited' : 'Favorite'}
    </button>`;
}

function aggregateRatingText(restaurant) {
  const count = Number.parseInt(String(restaurant.ratingCount ?? 0), 10);
  const sum = Number.parseInt(String(restaurant.ratingSum ?? 0), 10);
  if (!Number.isInteger(count) || !Number.isInteger(sum)
      || count <= 0 || sum < count || sum > count * 5) {
    return 'No ratings yet';
  }
  return `${(sum / count).toFixed(1)}/5 from ${count} ${count === 1 ? 'rating' : 'ratings'}`;
}

export async function initializeRestaurantProfile({
  mount = typeof document === 'undefined' ? null : document.getElementById('restaurant-member-controls'),
  publicRating = typeof document === 'undefined' ? null : document.getElementById('restaurant-public-rating'),
  claims = getAuthClaims,
  request = fetchJson,
  headers = authHeaders,
} = {}) {
  if (!mount || !claims()?.sub) return;
  const restaurantId = String(mount.dataset.restaurantId || '').trim();
  if (!restaurantId) return;

  const anonymousFallback = mount.innerHTML;
  const state = { restaurant: null };
  mount.innerHTML = '<p class="restaurant-member-loading">Loading your rating and favorite...</p>';

  const render = restaurant => {
    state.restaurant = restaurant;
    mount.innerHTML = memberMarkup(restaurant);
  };
  const showError = error => {
    mount.insertAdjacentHTML('afterbegin',
      `<div class="alert alert-danger" role="alert">${sanitize(error.message || 'Could not update your restaurant controls.')}</div>`);
  };

  try {
    render(await request(API.whatsForLunch.restaurant(restaurantId), { headers: headers() }));
  } catch (error) {
    mount.innerHTML = anonymousFallback;
    if (error?.status !== 401) showError(error);
    return;
  }

  mount.addEventListener('click', async event => {
    const ratingButton = event.target?.closest?.('.lunch-rating-button');
    const favoriteButton = event.target?.closest?.('.restaurant-favorite-toggle');
    if (!ratingButton && !favoriteButton) return;

    try {
      if (ratingButton) {
        const rating = Number.parseInt(String(ratingButton.dataset.rating), 10);
        if (!RATING_OPTIONS.includes(rating)) return;
        const updated = await request(API.whatsForLunch.rateRestaurant, {
          method: 'PUT', headers: headers({ 'Content-Type': 'application/json' }),
          body: JSON.stringify({ restaurantId: state.restaurant.id, rating }),
        });
        render(updated);
        if (publicRating) {
          publicRating.textContent = aggregateRatingText(updated);
        }
        return;
      }

      render(await request(API.whatsForLunch.favoriteRestaurant, {
        method: state.restaurant.myFavorite ? 'DELETE' : 'PUT',
        headers: headers({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({ restaurantId: state.restaurant.id }),
      }));
    } catch (error) {
      showError(error);
    }
  });
}

initializeRestaurantProfile();
```

Verification:
- Run the new test file through `:website:jsTest`; require GREEN.
- Run all JavaScript tests; require no unhandled rejection or warning.

- [ ] **Step 3: Commit member-only enhancement**

```powershell
git add website/src/main/resources/static/js/restaurant-profile.js `
  website/src/test/js/restaurant-profile.test.js
git commit -m "Enhance restaurant member controls"
```

Task-level verification:
- Anonymous test observes zero network calls.
- Signed-in load, rating, favorite, `401`, and non-401 failure paths retain their reviewed behavior.

### Task 4 - Move restaurant profile styling into the scoped Void owner

Sequence / dependencies:
- Runs after Tasks 2–3 because selectors and semantic layout are final.

Expected files:
- Modify `website/src/main/resources/static/css/main.css`.
- Modify `website/src/main/resources/static/css/whats-for-lunch.css`.
- Modify `website/src/main/resources/static/css/README.md`.
- Modify `website/src/main/resources/static/js/README.md`.
- Modify `website/src/test/js/feature-stylesheets.test.js`.
- Modify `website/src/test/js/a11y-markup.test.js`.

Interfaces:
- Consumes: template classes from Task 2 and member-control classes from Task 3.
- Produces: exclusive scoped stylesheet ownership, two-column desktop/one-column mobile profile, visible focus, inline failure, and reduced-motion behavior.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke it together with `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: Profiles render in the approved Void visual language at desktop/mobile sizes without affecting Top Rated, Favorites, or unrelated pages.
  - Invariants: Every feature selector is beneath `.lunch-void-page`; focus stays visible; content remains usable without motion; responsive layout never overflows.
  - Boundary/API: `whats-for-lunch.css` becomes the sole profile-style owner; shared WFL list primitives unrelated to profiles remain in `main.css`.
  - Effects and failures: CSS changes presentation only; stale ownership documentation/static checks would fail the build; browser evidence covers cascade and layout.
  - Tests and evidence: RED static tests require the profile template stylesheet, scoped selectors, focus/reduced-motion, and removal from `main.css`; GREEN is full `jsTest` plus browser desktop/mobile checks.

- [ ] **Step 1: Tighten stylesheet/accessibility ownership tests and witness RED**

#### Code Edit 4.1
- File: `website/src/test/js/feature-stylesheets.test.js`
- Lines: 47-53
- Action: replace

Current:
```javascript
const templates = [
  ['templates/command-center.html', 'command-center.css'],
  ['templates/shared-folder.html', 'shared-folder.css'],
  ['templates/void/explore.html', 'void-discovery.css'],
  ['templates/void/topic.html', 'void-discovery.css'],
  ['templates/whatsforlunch.html', 'whats-for-lunch.css'],
];
```

Proposed:
```javascript
const templates = [
  ['templates/command-center.html', 'command-center.css'],
  ['templates/shared-folder.html', 'shared-folder.css'],
  ['templates/void/explore.html', 'void-discovery.css'],
  ['templates/void/topic.html', 'void-discovery.css'],
  ['templates/whatsforlunch.html', 'whats-for-lunch.css'],
  ['templates/restaurant.html', 'whats-for-lunch.css'],
];
```

Verification:
- Run `:website:jsTest`; expected RED while the profile selectors remain in `main.css` and the dedicated stylesheet lacks the new class.

#### Code Edit 4.1b
- File: `website/src/test/js/feature-stylesheets.test.js`
- Lines: 32-38
- Action: replace

Current:
```javascript
const ownership = [
  ['.void-discovery-hero', voidDiscovery],
  ['.command-center-page', commandCenter],
  ['.shared-folder-main', sharedFolder],
  ['.site-media-player-host', siteMediaPlayer],
  ['.lunch-void-page', whatsForLunch],
];
```

Proposed:
```javascript
const ownership = [
  ['.void-discovery-hero', voidDiscovery],
  ['.command-center-page', commandCenter],
  ['.shared-folder-main', sharedFolder],
  ['.site-media-player-host', siteMediaPlayer],
  ['.lunch-void-page', whatsForLunch],
  ['.restaurant-profile-void', whatsForLunch],
];
```

Verification:
- The ownership loop proves the profile selector is absent from `main.css` and present in `whats-for-lunch.css`.

#### Code Edit 4.2
- File: `website/src/test/js/a11y-markup.test.js`
- Lines: after 74
- Action: add

Proposed:
```javascript
test('WFL restaurant profile is server-rendered, labelled, and keyboard visible', () => {
  const html = fs.readFileSync(
    'website/src/main/resources/templates/restaurant.html', 'utf8');
  const css = fs.readFileSync(
    'website/src/main/resources/static/css/whats-for-lunch.css', 'utf8');

  assert.equal((html.match(/<main\b/g) || []).length, 1);
  assert.equal((html.match(/<h1\b/g) || []).length, 1);
  assert.match(html, /<main[^>]+aria-labelledby="restaurantTitle"/);
  assert.match(html, /class="[^"]*lunch-void-page[^"]*restaurant-profile-page/);
  assert.match(html, /id="restaurant-member-controls"[^>]+aria-live="polite"/);
  assert.match(html, /type="application\/ld\+json"/);
  assert.match(css, /\.lunch-void-page \.restaurant-profile-void/);
  assert.match(css, /\.lunch-void-page [^{]+:focus-visible/);
  assert.match(css, /@media \(prefers-reduced-motion: reduce\)/);
});
```

Verification:
- The test fails until the template/CSS contracts are complete.

- [ ] **Step 2: Remove the legacy light profile rules from the shared stylesheet**

#### Code Edit 4.3
- File: `website/src/main/resources/static/css/main.css`
- Lines: 1972-2011
- Action: delete

Current:
```css
.restaurant-profile {
    display: grid;
    gap: 1rem;
}

.restaurant-profile h2 {
    margin-bottom: 0.5rem;
}

.restaurant-profile-rating {
    margin-bottom: 0.5rem;
    font-weight: 800;
}

.restaurant-profile-rating p {
    margin: 0 0 0.15rem;
}

.restaurant-detail-list {
    display: grid;
    gap: 0.75rem;
    margin: 0;
}

.restaurant-detail-list div {
    display: grid;
    gap: 0.2rem;
}

.restaurant-detail-list dt {
    color: rgba(23, 32, 42, 0.58);
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
}

.restaurant-detail-list dd {
    margin: 0;
    overflow-wrap: anywhere;
}
```

Proposed:
```text
delete block
```

Verification:
- `rg "restaurant-profile|restaurant-detail-list" website/src/main/resources/static/css/main.css` returns no result.

- [ ] **Step 3: Add the scoped Void profile layout and states**

#### Code Edit 4.4
- File: `website/src/main/resources/static/css/whats-for-lunch.css`
- Lines: after 310
- Action: add

Proposed:
```css
.lunch-void-page .restaurant-profile-container {
    max-width: 1080px;
}

.lunch-void-page .restaurant-profile-hero {
    margin-top: 1.1rem;
}

.lunch-void-page .restaurant-profile-void {
    display: grid;
    grid-template-columns: minmax(15rem, 0.72fr) minmax(0, 1.28fr);
    gap: 0.9rem;
}

.lunch-void-page .restaurant-rating-signal,
.lunch-void-page .restaurant-profile-details,
.lunch-void-page .restaurant-member-panel {
    min-width: 0;
    padding: clamp(1rem, 2.4vw, 1.4rem);
    border: 1px solid var(--lunch-void-line);
    border-radius: 6px;
    background: var(--lunch-void-panel);
    color: var(--lunch-void-text);
}

.lunch-void-page .restaurant-rating-signal {
    background:
        linear-gradient(150deg, rgba(222, 177, 95, 0.08), transparent 55%),
        var(--lunch-void-panel-raised);
}

.lunch-void-page .restaurant-profile-details {
    grid-row: span 2;
}

.lunch-void-page .restaurant-profile-label {
    margin-bottom: 0.35rem;
    color: var(--lunch-void-gold);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.lunch-void-page .restaurant-profile-void h2 {
    color: var(--lunch-void-text);
}

.lunch-void-page .restaurant-rating-value {
    margin: 0.55rem 0;
    color: var(--lunch-void-teal);
    font-size: clamp(1.5rem, 4vw, 2.4rem);
    font-weight: 850;
}

.lunch-void-page .restaurant-detail-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
    margin: 1rem 0 0;
}

.lunch-void-page .restaurant-detail-list div {
    min-width: 0;
    padding: 0.75rem;
    border: 1px solid var(--lunch-void-line);
    background: #080e14;
}

.lunch-void-page .restaurant-detail-list dt {
    color: var(--lunch-void-muted);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.lunch-void-page .restaurant-detail-list dd {
    margin: 0.25rem 0 0;
    overflow-wrap: anywhere;
}

.lunch-void-page .restaurant-detail-list a,
.lunch-void-page .restaurant-member-panel a {
    color: var(--lunch-void-teal);
}

.lunch-void-page .restaurant-profile-actions,
.lunch-void-page #restaurant-member-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    align-items: center;
    margin-top: 1rem;
}

.lunch-void-page #restaurant-member-controls > p,
.lunch-void-page #restaurant-member-controls > .alert {
    flex-basis: 100%;
    margin-bottom: 0;
}

@media (max-width: 760px) {
    .lunch-void-page .restaurant-profile-void,
    .lunch-void-page .restaurant-detail-list {
        grid-template-columns: 1fr;
    }

    .lunch-void-page .restaurant-profile-details {
        grid-row: auto;
    }
}
```

Retain the existing page-wide focus-visible and reduced-motion blocks; add only selectors needed for profile layout/states.

Verification:
- Run full `:website:jsTest`; require GREEN.
- Inspect at 1440×900 and 390×844 with keyboard-only focus and reduced-motion emulation.

- [ ] **Step 4: Update ownership documentation**

#### Code Edit 4.5a
- File: `website/src/main/resources/static/css/README.md`
- Lines: 10-11
- Action: replace

Current:
```markdown
- `whats-for-lunch.css` owns the `/wfl` Void decision console while shared WFL
  list and restaurant-profile primitives remain in `main.css`.
```

Proposed:
```markdown
- `whats-for-lunch.css` owns the `/wfl` Void decision console and the public
  restaurant-profile Void layout. Shared Favorites and Top Rated list primitives remain in `main.css`.
```

Verification:
- `feature-stylesheets.test.js` documentation/ownership assertions pass.

#### Code Edit 4.5b
- File: `website/src/main/resources/static/css/README.md`
- Lines: 48-50
- Action: replace

Current:
```markdown
- WFL uses shared lunch classes for restaurant profiles, favorites, and top-rated
  lists in `main.css`; the picks page layers `.lunch-void-*` and scoped lunch
  overrides from `whats-for-lunch.css` without changing neighboring pages.
```

Proposed:
```markdown
- WFL Favorites and Top Rated retain shared lunch list classes in `main.css`.
  The picks page and public restaurant profiles use scoped `.lunch-void-*` and
  profile rules from `whats-for-lunch.css` without changing neighboring pages.
```

Verification:
- The documented split matches selector ownership after Code Edits 4.3–4.4.

#### Code Edit 4.6
- File: `website/src/main/resources/static/js/README.md`
- Lines: 75-78
- Action: replace

Current:
```markdown
- `restaurant-profile.js` renders the public WFL restaurant profile page from
  the restaurant detail API, including aggregate rating, personal rating, and
  favorite state when the visitor is signed in. It and the WFL cards construct
  validated HTTP(S) website anchors through DOM properties rather than HTML interpolation.
```

Proposed:
```markdown
- Restaurant profiles render their complete public restaurant data on the server.
  `restaurant-profile.js` makes no anonymous detail request and progressively adds only
  signed-in personal rating/favorite controls; failures remain inside that member panel.
  Restaurant website links are validated by the server-side display policy before rendering.
```

Verification:
- Review the documentation diff against actual ownership; no behavioral source-grep test is added for prose.

- [ ] **Step 5: Commit the Void profile styling**

```powershell
git add website/src/main/resources/static/css/main.css `
  website/src/main/resources/static/css/whats-for-lunch.css `
  website/src/main/resources/static/css/README.md `
  website/src/main/resources/static/js/README.md `
  website/src/test/js/feature-stylesheets.test.js `
  website/src/test/js/a11y-markup.test.js
git commit -m "Style restaurant profiles in Void"
```

Task-level verification:
- Full `:website:jsTest` passes.
- `git diff --check` passes.
- `main.css` no longer owns restaurant profile selectors.

### Task 5 - Prove search, privacy, runtime, and visual acceptance

Sequence / dependencies:
- Runs after Tasks 1–4. No source edits are allowed in this task unless a new failing regression test starts a fresh TDD cycle in the owning task.

Implementation notes:
- This is verification/review mode; `write-chris-street-style-code` is required if any correction becomes necessary.
- Before-Edit Brief:
  - Behavior: The integrated candidate proves raw indexable HTML, correct crawler boundaries, Void desktop/mobile presentation, and personal controls.
  - Invariants: Port 8080 is untouched until merge/deployment; isolated test data is used; exact merged/deployed SHA identity is recorded.
  - Boundary/API: Exercise raw HTTPS/HTTP, browser UI, robots, sitemap, controller/API, MongoDB health, and production listener.
  - Effects and failures: Candidate process/database are isolated and recoverable; PR/deployment are external effects; any failed check stops merge/closure.
  - Tests and evidence: Focused RED/GREEN history, full build, raw responses, JSON parse, desktop/mobile screenshots, CI, deployment identity, health, and production profile checks.

- [ ] **Step 1: Run focused and full automated verification**

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-gradle-homes\restaurant-profile-void-seo'
.\gradlew.bat :website:test --tests "dev.christopherbell.view.wfl.RestaurantProfilePageServiceTest" `
  --tests "dev.christopherbell.view.ViewControllerTest" `
  --tests "dev.christopherbell.configuration.PublicSitemapServiceTest" `
  --tests "dev.christopherbell.configuration.PublicDeliveryConfigurationTest" `
  :website:jsTest --no-daemon
.\gradlew.bat :website:test :website:check --no-daemon
git diff --check
git status --short
```

Expected:
- All focused tests, all JavaScript tests, `:website:test`, and `:website:check` pass.
- Only intended source/test/docs files plus the known unstaged `gradlew.bat` line-ending artifact are present.

- [ ] **Step 2: Run the packaged candidate on an isolated non-production port/database**

Invoke `verify-local-spring-app` before runtime work. Confirm port `8094` is free, package the JAR, start it with the repository's local profile and isolated MongoDB database `christopherbell_dev_restaurant_profiles_void_seo`, and record PID, port, database, SHA, and readiness/liveness responses. Do not stop or rotate port 8080.

Raw-response cases:
- complete rated profile;
- sparse/unrated profile;
- encoded ID containing `/`;
- missing and malformed IDs;
- `/robots.txt`;
- `/sitemap.xml` and the shard containing the fixtures.

For each valid profile, save status, canonical, absence of `noindex`, public body fields, and parsed JSON-LD. Prove the raw response contains none of `myRating`, `myFavorite`, creator/modifier identity, or audit timestamps. For missing cases, prove `404`, `noindex,nofollow`, no Restaurant JSON-LD, and no database/error detail.

- [ ] **Step 3: Exercise browser behavior and visual acceptance**

Use the in-app browser workflow at desktop (1440×900) and mobile (390×844):

- anonymous complete and sparse profiles render without a profile API request;
- scripts-disabled/raw content remains complete;
- navigation, phone, safe website, Maps, and Back to WFL actions work;
- signed-in member controls load and rating/favorite mutations update correctly;
- forced member API failure preserves public content and shows only a local status;
- `401` restores sign-in fallback without a red error banner;
- Tab traversal has visible focus and logical order;
- layout does not overflow; reduced-motion behavior is respected;
- Top Rated and Favorites retain their existing presentation.

Capture representative desktop/mobile screenshots and console/network evidence.

- [ ] **Step 4: Review the final diff against the code standard and spec**

Apply the `write-chris-street-style-code` review rubric:

- trace public/detail input into the immutable page model;
- prove invalid optional states cannot enter JSON-LD;
- verify unescaped template output is limited to HTML-safe serialized JSON;
- verify one lookup, explicit failure classification, and no personal/audit fields;
- inspect production and test changes together;
- confirm every semantic change has observed RED/GREEN evidence;
- confirm no unrelated refactor or style change entered the diff.

Resolve every blocker through a new RED/GREEN cycle. Record acceptable residual risks.

- [ ] **Step 5: Save the local app test report and publish the PR**

Use Builder `save-test-report`, `validate-test-report`, `ingest-spoke-update`, and `review-spoke-work`. Commit/push the Builder checkpoints required by their skills. Then in the spoke:

```powershell
git status --short --branch
git log --oneline origin/main..HEAD
git push -u origin codex/restaurant-profile-void-seo
```

Open a ready PR describing the public-only model, server rendering, JSON-LD safety, progressive enhancement, Void CSS ownership, RED/GREEN evidence, full checks, alternate-port raw/browser evidence, privacy checks, and rollback. Do not stage `gradlew.bat`.

- [ ] **Step 6: Pass CI, merge, deploy, and verify production**

- Wait for required CI, dependency review, and CodeQL checks; fix failures regression-first.
- Verify PR head SHA and reviewed diff, then squash-merge through the repository's normal protected workflow.
- Record the merged `main` SHA and wait for the protected Windows deployment to report that exact identity.
- Verify production liveness/readiness, MongoDB health, exact versioned CSS/JS assets, raw valid/missing profile responses, JSON-LD parse/safety, robots/sitemap discovery, anonymous no-fetch behavior, signed-in controls, and desktop/mobile Void presentation.
- Treat non-elevated ACL denial on protected production files/logs as expected; do not weaken ACLs. Use listener, exact asset, endpoint, database, service, and browser evidence.

- [ ] **Step 7: Close durable work**

Use `close-story-issue` if a source issue exists; otherwise document that the request was direct. Save final spoke update/review, session memory, and `close-hub-work`; refresh Builder indexes, validate hub state, and commit/push Builder `main`. Mark the spec/plan complete and work ledger closed only after production verification has passed.

## Code Changes

### Public page model and builder
- Add `RestaurantProfilePage.java` (Code Edit 1.2).
- Add `RestaurantProfilePageService.java` (Code Edit 1.3).
- Add `RestaurantProfilePageServiceTest.java` (Code Edit 1.1).

### Controller and server template
- Replace preview wiring with the public page service in `WhatsForLunchViewController.java` (Code Edits 2.2a–2.2d).
- Delete `RestaurantSocialPreview.java` and `RestaurantSocialPreviewService.java` after consumers migrate (Code Edits 2.2e–2.2f).
- Replace `restaurant.html` with semantic public HTML and JSON-LD (Code Edit 2.3).
- Expand raw response/404/privacy coverage in `ViewControllerTest.java` (Code Edit 2.1).

### Progressive enhancement
- Replace full-page browser rendering in `restaurant-profile.js` (Code Edit 3.2).
- Add behavioral member-enhancement tests (Code Edit 3.1).

### Void CSS and ownership
- Extend static ownership/accessibility checks (Code Edits 4.1–4.2).
- Delete legacy profile selectors from `main.css` (Code Edit 4.3).
- Add scoped profile layout/state rules to `whats-for-lunch.css` (Code Edit 4.4).
- Update CSS/JavaScript ownership documentation (Code Edits 4.5–4.6).

## Files and Modules

- WFL view boundary: `website/src/main/java/dev/christopherbell/view/wfl/`
- Restaurant view controller tests: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Template: `website/src/main/resources/templates/restaurant.html`
- Page entry: `website/src/main/resources/static/js/restaurant-profile.js`
- Dedicated style owner: `website/src/main/resources/static/css/whats-for-lunch.css`
- Shared stylesheet cleanup: `website/src/main/resources/static/css/main.css`
- Browser/static tests: `website/src/test/js/`
- Existing unchanged indexing boundaries: `PublicSitemapService`, `PublicMetadataController`, `static/robots.txt`, and their tests.

## Unit Testing

- `RestaurantProfilePageServiceTest`: complete, sparse, unrated, hostile, unsafe-link, encoded ID, coordinate/address, rating validity, not-found, and serialization behavior.
- `ViewControllerTest`: raw HTML, metadata, canonical, public body, JSON-LD, privacy absence, Void assets/classes, and missing-profile noindex 404.
- `restaurant-profile.test.js`: zero anonymous fetch, signed-in member rendering, 401/non-401 fallback, rating/favorite contracts, and public-rating refresh after mutation.
- `feature-stylesheets.test.js` and `a11y-markup.test.js`: stylesheet ownership, semantic labels, member live region, focus, mobile/reduced-motion source contracts.

## Local Testing

- Focused Java/JS RED/GREEN after every task.
- Full `:website:test` and `:website:check` with task-private Gradle home.
- Packaged alternate-port Spring app with isolated MongoDB data.
- Raw HTTP for complete/sparse/encoded/missing profiles, robots, sitemap, and JSON parsing.
- Anonymous/authenticated/error browser flows at desktop/mobile widths, keyboard-only, scripts-disabled, and reduced motion.
- Explicit confirmation that port 8080 remains untouched during candidate testing.

## Validation

- All approved spec acceptance criteria map to Tasks 1–5.
- A mutation that removes server body fields, canonical encoding, JSON escaping, noindex 404, anonymous no-fetch, local failure containment, stylesheet ownership, or responsive focus coverage fails at least one named test/check.
- PR required checks and post-merge production acceptance pass against exact SHA and exact fingerprinted assets.

## Rollback or Recovery

- No data or schema rollback is required.
- Before merge, stop/delete only the isolated candidate process/database and abandon the feature branch/worktree if needed.
- After merge, redeploy the previous known-good merged SHA to restore the client-rendered profile.
- Existing restaurant URLs, sitemap entries, ratings, favorites, and database records remain compatible with both versions.
- Never reset, clean, or modify the dirty authoritative checkout.

## Risks

- **Private-state leak:** mitigated by an immutable model with no personal/audit components and raw-response negative tests.
- **Script-element injection:** mitigated by Jackson serialization plus `<`, `>`, and `&` Unicode escaping and hostile-name tests.
- **False crawler success:** mitigated by raw body assertions, parsed JSON-LD, canonical/sitemap/robots checks, and explicit 404/noindex cases.
- **Duplicate public rendering drift:** mitigated by deleting JavaScript public rendering; server owns public facts and JS owns personal controls.
- **Stale aggregate after rating mutation:** mitigated by updating only the aggregate status node from the mutation response.
- **CSS cascade regression:** mitigated by page scoping, exclusive ownership tests, Top Rated/Favorites regression checks, and desktop/mobile browser evidence.
- **Sparse data layout gaps:** mitigated by conditional template branches and sparse/unrated fixtures.
- **Operational collision:** mitigated by a checked non-8080 port, isolated database, exact PID tracking, and protected production deployment.

## Completion Criteria

- Every planned RED test was observed failing for the intended missing behavior and later passes.
- Focused tests, all JavaScript tests, full `:website:test`, `:website:check`, and `git diff --check` pass.
- Alternate-port raw/browser evidence proves indexing, privacy, progressive enhancement, Void desktop/mobile layout, accessibility, and failure fallback.
- Independent code-standard review has no blockers.
- PR required checks pass, the reviewed change merges, and the exact merged SHA deploys.
- Production raw HTML, JSON-LD, canonical, robots/sitemap, health/database, assets, anonymous/signed-in behavior, and desktop/mobile UI pass.
- Builder test report, spoke update/review, closure, session memory, indexes, and work ledger are committed and pushed; work status is `closed`.
