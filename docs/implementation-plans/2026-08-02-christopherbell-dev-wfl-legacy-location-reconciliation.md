# christopherbell.dev What's for Lunch Legacy Location Reconciliation Plan

## Document Status

complete

## Objective

Expand What's for Lunch OpenStreetMap coverage to all 393 unique current Census places intersecting the four existing import rectangles, make city resolution coordinate-aware, enforce the same rectangle ownership at the persistence boundary, and reconcile production legacy rows from an exact Census-backed manifest.

## Goals

- Preserve every legacy OSM restaurant whose real Census place can be resolved.
- Delete only records that still have no incorporated-place or Census-designated-place match after the merged importer is deployed and a fresh reimport completes.
- Support same-name places in different states without last-write-wins behavior.
- Keep client and service validation independent and aligned.
- Complete focused/full tests, alternate-port runtime validation, PR/CI/merge/deployment, backup, production reconciliation, and public verification.

## Inputs

- Spec: `docs/specs/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md`
- Prior strict-import spec and plan dated 2026-08-02
- User decision: **Expand and reconcile**
- Merged/deployed strict importer: PR `#1342`, SHA `178d90caca58d2f6284f54ab2ef4514d10df2918`
- Fresh read-only inventory: 7,268 OSM rows; 5,493 canonical; 1,596 official named/noncanonical; 163 coordinate-resolved; 16 unresolved
- Official source: Census 2025 Gazetteer and TIGERweb January 1, 2025 place layers 4 and 5

## Branch

- Existing isolated worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-import-location-integrity-20260802`
- Existing branch: `codex/wfl-import-location-integrity`
- Base/merged ancestor: `origin/main` containing `178d90caca58d2f6284f54ab2ef4514d10df2918`
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`.

## Non-Goals

- No runtime Census/geocoder dependency.
- No rectangle changes, public schema changes, MongoDB schema migration, or import schedule changes.
- No nearest-city, ZIP, county, airport, neighborhood, or metro-label inference.
- No broad deletion query; production mutation is exact-ID manifest driven.

## Assumptions

- The existing four Overpass rectangles remain the product coverage boundary.
- Current Census incorporated places and CDPs are the authoritative supported-locality set.
- A restaurant is owned by a metro only when its coordinates fall within that metro's configured rectangle.
- Production MongoDB remains locally reachable; protected release directories may remain unreadable without elevation.
- The previous full backup remains available, but a new backup is mandatory before this reconciliation.

## Open Questions

None.

## Task Breakdown

### Task 1 - Check in complete official place coverage

Sequence / dependencies:
- Runs first because client and service tests must bind the final coverage set.
- Use the pinned Census rectangle-intersection result; deduplicate California `Mountain View` by canonical city/state.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Invoke the skill before changing configuration or Java defaults.
- Before-Edit Brief:
  - Behavior: every official Census place intersecting a configured rectangle is a supported canonical locality.
  - Invariants: four rectangles and metro states do not change; duplicate city/state ownership stays invalid; YAML/default sets stay equal.
  - Boundary/API: internal configuration only; public APIs and property names remain compatible.
  - Effects and failures: startup validation rejects malformed or duplicate ownership; no network effects are introduced.
  - Tests and evidence: first add coverage-count/set assertions, then prove binding/startup and focused WFL tests pass.

#### Code Edit 1.1
- File: `website/src/main/resources/application.yml`
- Lines: 721-737
- Action: replace

Current:
```yaml
      metros:
        - name: Austin
          state: TX
          cities: [Austin, Round Rock, Cedar Park, Georgetown, Pflugerville, Leander, Hutto, Manor, Buda, Kyle, Bee Cave, Lakeway, Dripping Springs, Bastrop, San Marcos]
          bounds: { south: 29.95, west: -98.25, north: 30.75, east: -97.15 }
        # Three more short metro city lists follow.
```

Proposed:
```yaml
      metros:
        - name: Austin
          state: TX
          cities: [Austin, Barton Creek, Bastrop, Bear Creek, Bee Cave, Belterra, Bertram, Briarcliff, Brushy Creek, Buda, Burnet, Camp Swift, Canyon Lake, Cedar Creek, Cedar Park, Circle D-KC Estates, Coupland, Creedmoor, Double Horn, Driftwood, Dripping Springs, Elgin, Garfield, Georgetown, Granger, Hays, Hornsby Bend, Hudson Bend, Hutto, Jonestown, Kyle, Lago Vista, Lakeway, Leander, Liberty Hill, Lost Creek, Manchaca, Manor, Marble Falls, McDade, Mountain City, Mustang Ridge, Niederwald, Pflugerville, Point Venture, Red Rock, Rollingwood, Rosanky, Round Rock, San Leanna, San Marcos, Santa Rita Ranch, Serenada, Shady Hollow, Smithville, Steiner Ranch, Sunset Valley, Taylor, The Hills, Thorndale, Thrall, Uhland, Volente, Webberville, Weir, Wells Branch, West Lake Hills, Wimberley, Woodcreek, Wyldwood]
          bounds: { south: 29.95, west: -98.25, north: 30.75, east: -97.15 }
        # Mirror the pinned 154 CA, 46 LA, and 123 Dallas unique place sets.
```

Verification:
- Bind configuration in the focused property/client tests and assert exact metro counts `70, 154, 46, 123` and total `393`.

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/config/WflProperties.java`
- Lines: 177-196
- Action: replace

Current:
```java
    private static List<Metro> defaultMetros() {
      return new ArrayList<>(List.of(
          metro("Austin", "TX",
              List.of("Austin", "Round Rock", "Cedar Park", "Georgetown", "Pflugerville",
                  "Leander", "Hutto", "Manor", "Buda", "Kyle", "Bee Cave", "Lakeway",
                  "Dripping Springs", "Bastrop", "San Marcos"),
              29.95, -98.25, 30.75, -97.15),
          // Three more short defaults.
```

Proposed:
```java
    private static List<Metro> defaultMetros() {
      return new ArrayList<>(List.of(
          metro("Austin", "TX", AUSTIN_CENSUS_PLACES, 29.95, -98.25, 30.75, -97.15),
          metro("San Francisco Bay Area", "CA", BAY_AREA_CENSUS_PLACES,
              37.20, -122.65, 38.20, -121.65),
          metro("New Orleans", "LA", NEW_ORLEANS_CENSUS_PLACES,
              29.70, -90.45, 30.25, -89.65),
          metro("Dallas", "TX", DALLAS_CENSUS_PLACES,
              32.45, -97.35, 33.15, -96.35)));
    }
```

Verification:
- `./gradlew :website:test --tests '*WflPropertiesTest' --tests '*OpenStreetMapRestaurantClientTest'`

#### Code Edit 1.3
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/WflPropertiesTest.java`
- Lines: after 67
- Action: add

Proposed:
```java
  @Test
  void defaultsContainPinnedCensusPlaceCoverage() {
    var metros = new WflProperties().getRestaurantImport().getOsm().getMetros();
    assertEquals(List.of(70, 154, 46, 123),
        metros.stream().map(metro -> metro.getCities().size()).toList());
    assertEquals(393, metros.stream().mapToInt(metro -> metro.getCities().size()).sum());
  }
```

Verification:
- The new test fails before coverage replacement and passes afterward.

### Task 2 - Resolve city ownership with coordinates and state aliases

Sequence / dependencies:
- Runs after Task 1 so `Fairview`, `Rollingwood`, and `Sunnyvale` expose the cross-state collision.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Invoke the skill before changing client behavior or tests.
- Before-Edit Brief:
  - Behavior: resolve one canonical location only when city evidence, coordinates, optional state, and optional country agree.
  - Invariants: missing/unsupported locality remains excluded; country contradictions remain excluded; output stays canonical.
  - Boundary/API: private client internals change from one city value to candidate lists; the public client method is unchanged.
  - Effects and failures: malformed OSM input is omitted without writes; no geocoder/network call beyond existing Overpass is added.
  - Tests and evidence: add red cases for same-name cities, full names, and coordinate contradictions before the implementation.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 34-42
- Action: replace

Current:
```java
  private final Map<String, SupportedLocation> supportedLocations;

  public OpenStreetMapRestaurantClient(ObjectMapper objectMapper, WflProperties wflProperties) {
    this.objectMapper = objectMapper;
    this.properties = wflProperties.getRestaurantImport().getOsm();
    this.supportedLocations = configuredLocations(properties.getMetros());
```

Proposed:
```java
  private final Map<String, List<SupportedLocation>> supportedLocations;

  public OpenStreetMapRestaurantClient(ObjectMapper objectMapper, WflProperties wflProperties) {
    this.objectMapper = objectMapper;
    this.properties = wflProperties.getRestaurantImport().getOsm();
    this.supportedLocations = configuredLocations(properties.getMetros());
```

Verification:
- Compile focused client tests after all Task 2 edits.

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 115-173
- Action: replace

Current:
```java
    var location = supportedLocation(tags);
    var latitude = coordinate(element, "lat");
    var longitude = coordinate(element, "lon");
    if (name == null || name.isBlank() || location.isEmpty()
        || !isCoordinate(latitude, -90.0, 90.0)
        || !isCoordinate(longitude, -180.0, 180.0)) {
      return Optional.empty();
    }
```

Proposed:
```java
    var latitude = coordinate(element, "lat");
    var longitude = coordinate(element, "lon");
    if (name == null || name.isBlank()
        || !isCoordinate(latitude, -90.0, 90.0)
        || !isCoordinate(longitude, -180.0, 180.0)) {
      return Optional.empty();
    }
    var location = supportedLocation(tags, latitude, longitude);
    if (location.isEmpty()) {
      return Optional.empty();
    }
```

Verification:
- Focused client tests prove invalid coordinates are rejected before resolution.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- Lines: 148-173
- Action: replace

Current:
```java
  private Optional<SupportedLocation> supportedLocation(JsonNode tags) {
    var locality = firstText(tags, "addr:city", "addr:town", "addr:village", "addr:municipality");
    var location = supportedLocations.get(normalizeLocation(locality));
    if (location == null) {
      return Optional.empty();
    }
    // One global city value is checked against state/country.
  }
```

Proposed:
```java
  private Optional<SupportedLocation> supportedLocation(
      JsonNode tags, double latitude, double longitude) {
    var locality = firstText(tags, "addr:city", "addr:town", "addr:village", "addr:municipality");
    var suppliedState = text(tags, "addr:state");
    var suppliedCountry = text(tags, "addr:country");
    if (suppliedCountry != null && !suppliedCountry.isBlank() && !isUnitedStates(suppliedCountry)) {
      return Optional.empty();
    }
    var matches = supportedLocations.getOrDefault(normalizeLocation(locality), List.of()).stream()
        .filter(location -> location.contains(latitude, longitude))
        .filter(location -> suppliedState == null || suppliedState.isBlank()
            || stateMatches(suppliedState, location.state()))
        .toList();
    return matches.size() == 1 ? Optional.of(matches.getFirst()) : Optional.empty();
  }
```

Verification:
- Tests prove CA/TX `Sunnyvale` resolve by coordinates, `Texas`/`California`/`Louisiana` canonicalize, and Austin-at-Dallas-coordinates is rejected.

#### Code Edit 2.4
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- Lines: 94-154
- Action: add

Proposed:
```java
  @Test
  void parseRestaurants_disambiguatesSameNamePlacesByCoordinates() throws Exception {
    var restaurants = parseRestaurants(fixtureWithCaliforniaAndTexasSunnyvale());
    assertEquals(List.of("CA", "TX"),
        restaurants.stream().map(item -> item.getAddress().getState()).toList());
  }

  @Test
  void parseRestaurants_acceptsFullStateNamesAndRejectsCoordinateContradictions() throws Exception {
    var restaurants = parseRestaurants(fullStateAndWrongRectangleFixture());
    assertEquals(List.of("Livermore", "Fort Worth"),
        restaurants.stream().map(item -> item.getAddress().getCity()).toList());
  }
```

Verification:
- New tests fail on the single-value map and pass on coordinate-aware candidates.

### Task 3 - Enforce metro rectangle ownership in the service

Sequence / dependencies:
- Runs after Tasks 1-2 so the service uses the same expanded coverage and rectangle semantics.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Invoke the skill before changing service validation or tests.
- Before-Edit Brief:
  - Behavior: prepared candidates outside the owning rectangle are counted invalid and never persisted.
  - Invariants: existing ID/name dedupe and merge behavior is unchanged; country and coordinate validation remains mandatory.
  - Boundary/API: private persistence validation only; import result shape is unchanged.
  - Effects and failures: invalid candidates produce `skippedInvalid`; repository methods are not called for them.
  - Tests and evidence: add one red valid-expanded case and one red out-of-rectangle case, then run focused service tests.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 1297-1310
- Action: replace

Current:
```java
    return wflProperties.getRestaurantImport().getOsm().getMetros().stream()
        .anyMatch(metro -> normalizeCity(metro.getState()).equals(state)
            && metro.getCities().stream().anyMatch(candidate -> normalizeCity(candidate).equals(city)));
```

Proposed:
```java
    return wflProperties.getRestaurantImport().getOsm().getMetros().stream()
        .anyMatch(metro -> normalizeCity(metro.getState()).equals(state)
            && metro.getCities().stream().anyMatch(candidate -> normalizeCity(candidate).equals(city))
            && contains(metro.getBounds(), address.getLatitude(), address.getLongitude()));
```

Verification:
- `./gradlew :website:test --tests '*RestaurantServiceTest'`

#### Code Edit 3.2
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- Lines: 1020-1060
- Action: add

Proposed:
```java
  @Test
  @DisplayName("OpenStreetMap import: accepts expanded coverage and rejects wrong rectangle")
  void testPreparedImport_whenCoverageAndCoordinatesDisagree_skipsOnlyMismatch() throws Exception {
    var livermore = importedRestaurant("Livermore", "CA", 37.6819, -121.7680);
    var misplaced = importedRestaurant("Livermore", "CA", 30.2672, -97.7431);
    var result = applyPrepared(livermore, misplaced);
    assertEquals(1, result.imported());
    assertEquals(1, result.skippedInvalid());
  }
```

Verification:
- Verify the repository saves only the in-rectangle candidate.

### Task 4 - Document and verify the checked-in behavior

Sequence / dependencies:
- Runs after Tasks 1-3.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Invoke the skill before editing executable examples or tests.
- Before-Edit Brief:
  - Behavior: operators understand that coverage is Census-derived and normal imports do not geocode missing locality.
  - Invariants: existing preview/apply operator contract stays intact.
  - Boundary/API: documentation only; no new endpoint.
  - Effects and failures: no runtime effect; stale coverage is called out as a deliberate refresh concern.
  - Tests and evidence: run Markdown/diff checks plus the focused and full Gradle suites.

#### Code Edit 4.1
- File: `website/README.md`
- Lines: after 73
- Action: add

Proposed:
```markdown
Configured OSM coverage uses current U.S. Census incorporated-place and
Census-designated-place names intersecting each import rectangle. City/state
values are canonicalized, rectangle ownership is enforced, and elements without
a supported locality are omitted; the normal importer does not call a geocoder.
```

Verification:
- `git diff --check`

#### Code Edit 4.2
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/WflPropertiesTest.java`
- Lines: after 67
- Action: add

Proposed:
```java
  @Test
  void censusCoverageAllowsSameCityNameInDifferentStates() {
    assertTrue(defaultMetros().stream().filter(metro -> metro.getCities().contains("Sunnyvale")).count() == 2);
    assertTrue(new WflProperties().getRestaurantImport().getOsm().isMetroCoverageUnique());
  }
```

Verification:
- Focused property test passes with state-qualified uniqueness.

### Task 5 - Run local verification and publish through production

Sequence / dependencies:
- Runs after all code edits.

Implementation notes:
- Run focused red/green tests, then `:website:test` and `:website:check` with a private Gradle user home.
- Package and start on a non-8080 port with an isolated MongoDB database and deterministic loopback Overpass fixture.
- Fixture must cover Livermore CA, Fort Worth TX, Sunnyvale CA/TX, a full state name, a contradictory state, an out-of-rectangle city, and missing locality.
- Record request/response and Mongo evidence in an updated Builder test report.
- Request code review, publish the existing branch, create/update the PR, wait for every required CI check, merge, and verify the exact deployed SHA.

Verification:
- Focused WFL tests pass.
- Full test/check pass.
- Alternate-port readiness/liveness, import preview/apply, canonical Mongo rows, and invalid absence pass.
- GitHub required checks pass and production reports the exact merged commit.

### Task 6 - Reimport and reconcile production from a fresh exact manifest

Sequence / dependencies:
- Runs only after Task 5 exact-SHA production deployment and health verification.

Implementation notes:
- Complete a production preview/apply import first.
- Take a new full compressed MongoDB backup and run restore dry-run validation.
- Rerun Census TIGERweb point resolution against every remaining invariant violation.
- Save target/update/delete manifests under `A:\Backups\christopherbell.dev`, record SHA-256, counts, samples, and source timestamps.
- Abort if any resolved point is outside its configured rectangle, maps to another state, yields multiple places, or if pre-mutation IDs/counts differ from the manifest.
- Update exact resolved IDs; delete only exact no-place IDs and their direct favorite/rating references; preserve historical sessions.
- Verify zero remaining violations and exercise public nearby results in all four metros.

Verification:
- Backup exists, hash is recorded, and dry-run restore succeeds.
- Manifest matched/modified/deleted counts reconcile exactly.
- Every retained OSM row satisfies canonical city/state/country/coordinate/rectangle ownership.
- No synthetic metro label appears in Mongo or public nearby responses.
- Readiness, liveness, public home/WFL endpoints, Mongo ping, service state, and production commit identity pass.

## Code Changes

- `application.yml`: replace four short city lists with pinned official intersecting place coverage.
- `WflProperties.java`: mirror exact defaults.
- `OpenStreetMapRestaurantClient.java`: replace single city owner with coordinate-aware candidate resolution and state aliases.
- `RestaurantService.java`: add rectangle ownership to persistence validation.
- WFL tests: add coverage, disambiguation, state alias, expanded-location, and wrong-rectangle regressions.
- `website/README.md`: document the source and no-runtime-geocoder contract.

## Files and Modules

- `website/src/main/resources/application.yml`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/config/WflProperties.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/WflPropertiesTest.java`
- `website/README.md`
- Builder spec, plan, test report, spoke update/review, work closure, and session memory artifacts

## Unit Testing

- `./gradlew :website:test --tests '*WflPropertiesTest' --tests '*OpenStreetMapRestaurantClientTest' --tests '*RestaurantServiceTest'`
- Assert exact coverage counts and same-name cross-state behavior.
- Assert canonical output for full state names.
- Assert unsupported, contradictory, ambiguous, invalid-coordinate, and wrong-rectangle inputs are omitted/skipped.

## Local Testing

- `./gradlew :website:test`
- `./gradlew :website:check`
- Package with a private `GRADLE_USER_HOME`.
- Start the packaged app on a free non-8080 port with both Mongo URI and database overrides pointing to a task-specific isolated database.
- Use deterministic Overpass fixture data and capture URL/port, input body, response status/body, Mongo rows, and cleanup.
- Never rotate production 8080 during candidate validation.

## Validation

- Mechanical plan validator and human execution-readiness review pass before code.
- Focused/full/check/runtime verification passes locally.
- PR diff review and all required CI pass.
- Exact merged SHA deploys and reports healthy.
- Fresh backup, import, manifest, reconciliation, and public behavior evidence pass.

## Rollback or Recovery

- Revert/redeploy the prior production SHA for application regressions.
- Restore the fresh pre-reconciliation MongoDB backup for data discrepancies.
- Keep production mutation idempotent and exact-ID scoped so a stopped run can be audited and resumed.
- Do not weaken ACLs to access protected release files; use service/listener/endpoint/commit evidence.

## Risks

- A global city-name map corrupts cross-state names: eliminate it and test three known duplicates.
- Place polygons intersect rectangle edges: include the place in config, but require the individual restaurant point inside the rectangle.
- Census or production data drift between discovery and mutation: regenerate after deploy/reimport and abort on checksum/count mismatch.
- Large configuration lists diverge: assert exact counts/sets and mirror a single pinned evidence source.
- Cleanup affects dependent rows: count first, scope exact IDs, remove direct favorites/ratings only for deleted restaurants, preserve sessions, and retain backup rollback.

## Completion Criteria

- Spec and plan checkpoints are committed/pushed in Builder.
- Implementation and tests satisfy all six tasks.
- Local focused/full/check and alternate-port runtime evidence pass.
- PR required checks pass, PR is merged, exact SHA is deployed and healthy.
- Fresh production reimport, backup, restore dry run, exact manifest, reconciliation, and zero-violation audit pass.
- Final test report, spoke review/update, work closure, and session memory are saved, indexed, validated, committed, and pushed.
