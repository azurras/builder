# WFL and Location Imports Issues 1169-1175 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` inline. Do not dispatch subagents. Execute each task test-first and preserve the dirty authoritative checkout.

**Goal:** Complete issues #1169-#1175 with indexed WFL lookup paths, mutually exclusive observable imports, preview-before-apply maintenance, public freshness evidence, startup-validated metro/source configuration, and checksum-idempotent ZIP imports.

**Architecture:** Keep WFL and Location ownership in their existing feature packages. Reuse the existing atomic `MongoLeaseService` for import exclusion. Extract pure import planning from mutation so dry runs and apply use identical classification, persist short-lived preview identity rather than whole remote datasets, and re-fetch/revalidate before mutation. Validate typed WFL configuration at startup. Store only bounded operational state and safe error categories.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB/MongoTemplate, Jakarta Validation, Jackson 3, Gradle, JUnit 5, Mockito, AssertJ, Thymeleaf, and browser-native JavaScript.

## Document Status

complete

## Objective

Deliver approved campaign Batch 6 (#1169-#1175) as one reviewed, tested, production-safe change set, close its seven GitHub issues, and leave the final Batch 7 inventory ready for execution.

## Inputs

- Approved campaign specification: `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md`, Batch 6.
- GitHub issue bodies for #1169-#1175, all open with no comments or attachments as of 2026-07-26.
- Spoke base `5835a3c2b1dc032413e027568583859b9094ab9d` and green baseline `:website:check`.
- Repository guides: spoke `AGENTS.md`, root README, WFL README, and Location README.
- Existing `MongoLeaseService`, migration runner, WFL import state, coordinate-bounds query, Back Office operations UI, and ZIP Gazetteer importer.

## Assumptions

- MongoDB remains the production coordination and persistence boundary.
- The current four WFL metro regions remain the intended default coverage.
- Existing 2025/2026-05 API consumers require compatibility; additive `2026-07-26` routes are available for safer first-party workflows.
- Production auto-deployment continues to build and validate a candidate release before listener rotation.

## Branch

`codex/wfl-location-imports-1169-1175`

Worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-location-imports-1169-1175`

Base: `5835a3c2b1dc032413e027568583859b9094ab9d`

## Goals

- Prove nearby candidates come from the indexed coordinate-bounds repository query and aggregate top-rated ordering inside Mongo instead of loading every rating.
- Serialize manual and scheduled WFL mutation imports with the existing owner-scoped Mongo lease and expose bounded operator status.
- Require a fresh dry-run preview token before first-party manual WFL import apply.
- Preview duplicate groups, stable survivors, and observed versions before an explicitly confirmed delete.
- Show last successful WFL source, completion time, and metro/city coverage on public WFL pages, including an honest unavailable state.
- Bind and validate WFL metros, supported cities/states, bounding boxes, source URL, timeouts, limits, zones, and schedules at startup.
- Calculate the bundled ZIP dataset checksum, persist source version/counts/completion time, and report same-checksum imports as no-op.

## Code Changes

- Add typed validated WFL configuration and use it in the OSM client and restaurant service.
- Add a Mongo rating aggregation, pure import planner, durable WFL preview/status records, leased coordinator, and safe duplicate preview/apply models.
- Add public freshness and protected import preview/apply/status APIs.
- Add ZIP dataset checksum/version metadata and durable import state.
- Update Back Office and public WFL JavaScript, templates, API helpers, tests, migrations, and feature documentation.

## Files and Modules

- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/`: WFL service, controller, configuration, import planning/coordinator, models, repositories, and README.
- `website/src/main/java/dev/christopherbell/location/`: ZIP reader/service/state/models and README.
- `website/src/main/java/dev/christopherbell/configuration/mongo/`: existing lease service plus additive migration/index ownership.
- `website/src/main/resources/`: application configuration, Back Office/WFL templates, API helpers, WFL freshness renderer, page scripts, and static README.
- `website/src/test/java/` and `website/src/test/js/`: focused unit, repository, controller, configuration, migration, and UI tests.

## Non-Goals

- Do not change WFL session, favorite, daily-pick, or rating submission semantics.
- Do not add a frontend framework, npm dependency, external lock library, or new infrastructure service.
- Do not make live authenticated production mutations during verification.
- Do not yet apply the shared lease to VIN, RandomVIN, Canes index, or link-preview work; that belongs to Batch 7 issue #1179.
- Do not delete legacy import endpoints; new first-party preview/apply behavior is additive under the existing `2026-07-26` API version.

## Open Questions

None. The approved campaign specification defines all seven behaviors. The existing `MongoLeaseService` is the shared lock boundary, a short-lived durable preview record is the WFL apply authority, and duplicate apply revalidates explicit observed member versions before any delete.

## Global Constraints

- Work only in the Batch 6 worktree and never edit, reset, or clean `A:\Projects\christopherbell.dev`.
- Only GitHub comments authored by `azurras` may change scope; #1169-#1175 have no comments or attachments.
- Invoke `write-chris-street-style-code` before production/test/config edits because repository instructions require it despite the user's waiver.
- Use `superpowers:test-driven-development`: witness focused RED before each implementation slice, then focused GREEN before widening.
- Preserve legacy API contracts. First-party Back Office actions use additive preview/apply endpoints.
- Lease names are fixed constants, owner tokens are random and bounded, lease duration exceeds the configured request timeout, and release always conditions on exact ownership.
- Preview records contain only token/checksum/actor/timestamps/counts; they never persist raw remote response bodies.
- Error state stores a bounded allowlisted category, never an exception message, response body, URL credentials, or stack trace.
- Run packaged acceptance with a disposable Mongo database on a non-8080 port before merge.

## Task Breakdown

### Task 1 - Move WFL lookup work into indexed repository queries (#1169)

Sequence / dependencies:
- First, because later public freshness testing reuses the same WFL controller/service fixtures.

Before-Edit Brief:
- Behavior: nearby lookup uses the coordinate compound index for bounded candidates and top-rated lookup uses a Mongo aggregation grouped/sorted/limited by restaurant rating.
- Invariants: exact radius filtering remains server-owned; sort is average descending, count descending, restaurant ID ascending; limit clamps to 1-50; unrated restaurants remain absent.
- Boundary/API: public endpoint shapes do not change.
- Effects and failures: read-only Mongo operations; empty/null repository output becomes an empty list.
- Tests and evidence: RED tests reject `findAll()` and require the bounded query/aggregation, then focused service tests pass.

- [ ] Add RED repository/service tests for bounded coordinate candidates and database-owned rating aggregation.
- [ ] Implement the aggregation projection and remove all-rating loading from the public top-rated path.
- [ ] Run focused WFL query tests.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/RestaurantRatingRepository.java`
- Lines: 1-16
- Action: replace

Current:
```java
public interface RestaurantRatingRepository extends MongoRepository<RestaurantRating, String> {
  List<RestaurantRating> findByRestaurantIdIn(Collection<String> restaurantIds);
  Optional<RestaurantRating> findByRestaurantIdAndAccountId(String restaurantId, String accountId);
}
```

Proposed:
```java
public interface RestaurantRatingRepository extends MongoRepository<RestaurantRating, String> {
  List<RestaurantRating> findByRestaurantIdIn(Collection<String> restaurantIds);
  Optional<RestaurantRating> findByRestaurantIdAndAccountId(String restaurantId, String accountId);
  List<RestaurantRatingSummary> findTopRated(int boundedLimit); // custom Mongo group/sort/limit
}
```

Verification: focused repository aggregation integration test plus `RestaurantServiceTest` verifies no `findAll()` call.

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 217-1325
- Action: replace

Current:
```java
var restaurants = getNearbyCandidateRestaurants(latitude, longitude, radiusMiles);
var summaries = Optional.ofNullable(restaurantRatingRepository.findAll()).orElseGet(List::of).stream()
    .collect(Collectors.groupingBy(RestaurantRating::getRestaurantId));
```

Proposed:
```java
var restaurants = restaurantRepository.findByCoordinateBounds(/* indexed bounds */);
var summaries = restaurantRatingRepository.findTopRated(pageSize);
return hydrateRatedRestaurantsInSummaryOrder(summaries);
```

Verification: nearby service tests assert the coordinate query parameters and exact-radius post-filter; top-rated tests assert aggregation ordering and bounded limit.

### Task 2 - Validate WFL configuration at startup (#1174)

Sequence / dependencies:
- Before import planning because the planner, client, freshness response, and lease duration consume the same typed settings.

Before-Edit Brief:
- Behavior: bind named metros and import/source settings into one validated WFL properties object.
- Invariants: unique nonblank metro/city/state names; latitude/longitude ranges and south<north/west<east; HTTP/HTTPS endpoint without userinfo; positive bounded timeout/result limit/lease/preview TTL; valid zones and nonblank cron.
- Boundary/API: `wfl` YAML becomes a named metro list while retaining the same four default coverage areas.
- Effects and failures: invalid startup configuration fails with a field-specific message before imports can run.
- Tests and evidence: Binder tests cover every invalid partition and valid production defaults.

- [ ] Add RED binding/validation tests.
- [ ] Add typed properties/configuration and migrate service/client constructors away from scattered `@Value` fields.
- [ ] Update default YAML and package documentation.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/WflProperties.java`
- Lines: after 0
- Action: add

Proposed:
```java
@Validated
@ConfigurationProperties("wfl")
public record WflProperties(
    RestaurantOfTheDay restaurantOfTheDay,
    RestaurantImport restaurantImport) {
  public WflProperties { validateZonesSchedulesAndUniqueMetros(/* bounded fields */); }
  public record Metro(String name, List<String> cities, String state, BoundingBox bounds) {}
  public record BoundingBox(double south, double west, double north, double east) {}
}
```

Verification: `WflPropertiesTest` binds the checked-in YAML shape and rejects duplicate cities/metros, invalid ranges/order, unsafe endpoint schemes/userinfo, and dangerous numeric values.

#### Code Edit 2.2
- File: `website/src/main/resources/application.yml`
- Lines: 604-624
- Action: replace

Current:
```yaml
wfl:
  restaurant-import:
    monthly:
      enabled: true
    osm:
      endpoint: https://overpass-api.de/api/interpreter
      bbox: 29.95,-98.25,30.75,-97.15;...
```

Proposed:
```yaml
wfl:
  restaurant-import:
    lease-duration: 2m
    preview-ttl: 15m
    osm:
      endpoint: https://overpass-api.de/api/interpreter
      metros:
        - name: Austin
          state: TX
          cities: [Austin, Round Rock, Cedar Park]
          bounds: { south: 29.95, west: -98.25, north: 30.75, east: -97.15 }
```

Verification: application-context configuration test and focused `OpenStreetMapRestaurantClientTest` pass with all four configured metros.

### Task 3 - Add a leased, observable WFL import state machine (#1170)

Sequence / dependencies:
- Uses Task 2 typed durations and existing `MongoLeaseService`; Task 4 preview apply calls this state machine.

Before-Edit Brief:
- Behavior: scheduled and manual apply contend on fixed lease `wfl-openstreetmap-import`; state records RUNNING/SUCCEEDED/FAILED/SKIPPED_LOCKED, trigger, bounded actor ID, start/end, counts, and safe error category.
- Invariants: only exact owner releases; contention performs no fetch or mutation; terminal state follows mutation outcome; raw exception text is not persisted.
- Boundary/API: admin GET `.../2026-07-26/import/openstreetmap/status` returns bounded state.
- Effects and failures: Mongo lease/state writes and remote fetch; persistence/network failures surface safely for manual calls and are logged for scheduled calls.
- Tests and evidence: concurrent-owner/lease-contention, success, failure redaction, scheduled/manual common-path, and controller authorization tests.

- [ ] Add RED lease/status tests.
- [ ] Wrap WFL mutation execution in the existing lease and durable state.
- [ ] Expose authorized status without secrets.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 572-1155
- Action: replace

Current:
```java
void runTrackedOpenStreetMapImport(String trigger) {
  saveImportStarted(Instant.now(clock));
  try { saveImportCompleted(/* direct import */); }
  catch (Exception e) { saveImportFailed(/* exception message */); }
}
```

Proposed:
```java
RestaurantImportStatus runLeasedImport(ImportTrigger trigger, String actorId, PreviewToken token) {
  return restaurantImportCoordinator.run(trigger, actorId, token);
}
```

Verification: focused coordinator tests prove contention skips remote/persistence work, exact-owner release, terminal status/counts, and allowlisted failure categories.

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/RestaurantImportState.java`
- Lines: 13-38
- Action: replace

Current:
```java
private Instant lastStartedOn;
private Instant lastCompletedOn;
private Instant lastFailedOn;
private String lastFailureMessage;
private RestaurantImportResult lastResult;
```

Proposed:
```java
private RestaurantImportRunStatus status;
private String trigger;
private String actorAccountId;
private Instant startedOn;
private Instant completedOn;
private RestaurantImportResult result;
private String lastErrorCategory;
```

Verification: model serialization and service tests assert bounded fields and absence of exception messages.

### Task 4 - Add import dry-run preview and fresh-token apply (#1171)

Sequence / dependencies:
- Uses Task 3 coordinator and runs mutation only after a persisted short-lived token matches a re-fetched deterministic plan.

Before-Edit Brief:
- Behavior: preview computes create/update/delete/unchanged/invalid counts and bounded representative changes without writes; apply accepts the preview token, re-fetches/replans, and rejects expired, wrong-actor, consumed, or checksum-stale previews.
- Invariants: preview never writes restaurants; token is random and one-use; remote payload is not persisted; all classification comes from one pure planner.
- Boundary/API: ADMIN POST `.../2026-07-26/import/openstreetmap/preview`; ADMIN POST `.../apply` with `{previewToken}`.
- Effects and failures: preview performs remote read and preview-record write; apply performs remote read plus leased restaurant writes.
- Tests and evidence: side-effect-free preview, exact counts, expiration/actor/staleness/contention, successful one-use apply, and Back Office flow tests.

- [ ] Write RED pure-planner and token lifecycle tests.
- [ ] Extract planner and add durable bounded preview store.
- [ ] Add controller/API/Back Office preview then explicit apply.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportPlanner.java`
- Lines: after 0
- Action: add

Proposed:
```java
final class RestaurantImportPlanner {
  RestaurantImportPlan plan(List<Restaurant> existing, List<Restaurant> fetched) {
    // Pure deterministic create/update/unchanged/invalid classification and checksum.
  }
}
```

Verification: planner tests cover new, changed, unchanged, invalid, duplicate-name/different-address, deterministic checksum, and representative-change cap.

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantController.java`
- Lines: 425-468
- Action: replace

Current:
```java
@PostMapping(APIVersion.V20260517 + "/import/openstreetmap")
public ResponseEntity<Response<RestaurantImportResult>> importOpenStreetMapRestaurants() { /* direct apply */ }
```

Proposed:
```java
@PostMapping(APIVersion.V20260726 + "/import/openstreetmap/preview")
public Response<RestaurantImportPreview> previewOpenStreetMapRestaurants() { /* ADMIN */ }
@PostMapping(APIVersion.V20260726 + "/import/openstreetmap/apply")
public Response<RestaurantImportStateDetail> applyOpenStreetMapRestaurants(
    @RequestBody RestaurantImportApplyRequest request) { /* ADMIN */ }
```

Verification: MVC tests cover ADMIN success, anonymous/ordinary-user denial, invalid token 400, stale token 409, and legacy endpoint compatibility.

### Task 5 - Add duplicate preview and version-checked confirmation (#1172)

Sequence / dependencies:
- Reuses deterministic hashing from Task 4 but does not require a persisted token.

Before-Edit Brief:
- Behavior: preview returns duplicate group identity, proposed lowest-ID survivor, all candidate IDs/cities, and opaque observed versions; apply names exact groups and observed versions.
- Invariants: apply validates every requested group before any delete; stale/missing/extra member or changed survivor rejects the whole request; no unpreviewed group is touched.
- Boundary/API: ADMIN GET `.../2026-07-26/dedupe-names/preview`; ADMIN POST `.../apply` with explicit confirmations.
- Effects and failures: preview reads restaurants; apply conditionally deletes duplicates and normalizes survivors after full preflight.
- Tests and evidence: stable selection, no-preview deletion absence, stale confirmation atomic rejection, subset apply, and UI confirmation tests.

- [ ] Add RED preview/apply service tests.
- [ ] Replace direct UI cleanup with preview and explicit confirmation.
- [ ] Keep the legacy route for compatibility but move first-party UI to the safe additive flow.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 511-1449
- Action: replace

Current:
```java
public RestaurantDedupeResult removeDuplicateNamedRestaurants() {
  var restaurants = restaurantRepository.findAll();
  // immediately delete all non-survivors
}
```

Proposed:
```java
public RestaurantDedupePreview previewDuplicateNamedRestaurants() { /* no mutation */ }
public RestaurantDedupeResult applyDuplicatePreview(RestaurantDedupeApplyRequest request) {
  validateEveryObservedGroupBeforeMutation(request);
  return deleteOnlyConfirmedDuplicates(request);
}
```

Verification: focused service tests prove preview is read-only, survivor selection is stable, and stale/partial observations cannot cause deletion.

### Task 6 - Publish WFL freshness on public pages (#1173)

Sequence / dependencies:
- Consumes Task 2 coverage and Task 3 last-success state.

Before-Edit Brief:
- Behavior: public WFL pages show last successful completion, `OpenStreetMap`, and configured metro/city coverage, or “Freshness unavailable” before the first success.
- Invariants: never expose actor, lock owner, error, preview token, internal IDs, or configuration URL; timestamps use shared browser formatting.
- Boundary/API: public GET `.../2026-07-26/freshness` returns a minimal `RestaurantDataFreshness` payload.
- Effects and failures: one bounded state read; UI failure falls back honestly without hiding restaurant content.
- Tests and evidence: public MVC/security tests and pure JavaScript markup tests for available/unavailable/malformed states.

- [ ] Add RED freshness DTO/controller/UI tests.
- [ ] Add the public endpoint and shared freshness renderer.
- [ ] Render it on picks, favorites, and top-rated pages.

#### Code Edit 6.1
- File: `website/src/main/resources/static/js/lib/wfl-freshness.js`
- Lines: after 0
- Action: add

Proposed:
```javascript
export function wflFreshnessMarkup(value) {
  // Allowlist completion time, source label, metros, and cities; return honest unavailable text.
}
```

Verification: Node tests cover escaping, malformed timestamps/arrays, available coverage, and unavailable fallback; `node --check` passes.

#### Code Edit 6.2
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 404-832
- Action: replace

Current:
```javascript
function renderPicks(picks) {
  mount.innerHTML = `${wflSecondaryNav('picks')} ...`;
}
async function loadLunchPicks() { /* load picks/session only */ }
```

Proposed:
```javascript
function renderPicks(picks) {
  mount.innerHTML = `${wflSecondaryNav('picks')}${wflFreshnessMarkup(dataFreshness)} ...`;
}
async function loadLunchPicks() { await loadFreshness(); /* preserve pick fallback */ }
```

Verification: JavaScript tests assert all public WFL modes render safe freshness without blocking primary content.

### Task 7 - Make ZIP imports checksum-idempotent and observable (#1175)

Sequence / dependencies:
- Last backend slice; may reuse the shared Mongo lease for concurrent manual requests but is independent of WFL status.

Before-Edit Brief:
- Behavior: reader returns deterministic SHA-256/source-version metadata; service persists fixed import state with checksum/counts/completion; same completed checksum returns a reported no-op with zero writes.
- Invariants: checksum covers exact source bytes; parse succeeds before mutations; state is completed only after coordinate writes; rerun after partial/state failure safely converges.
- Boundary/API: existing admin endpoint returns additive `checksum`, `sourceVersion`, `completedOn`, and `noOp` fields.
- Effects and failures: bundled resource read, repository writes/deletes, then state save; malformed resource or state failure is surfaced without claiming completion.
- Tests and evidence: exact checksum, first import, same-checksum no-op, changed checksum, parse failure, and Back Office rendering.

- [ ] Add RED reader/service/controller/UI tests.
- [ ] Add dataset metadata and fixed import-state persistence.
- [ ] Update Back Office with no-op/checksum/completion evidence.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/location/zip/ZipCoordinateGazetteerReader.java`
- Lines: 20-73
- Action: replace

Current:
```java
public List<ZipCoordinate> readBundledCensusData() {
  return read(new ClassPathResource(CENSUS_RESOURCE));
}
```

Proposed:
```java
public ZipCoordinateDataset readBundledCensusData() {
  byte[] sourceBytes = readBoundedResourceBytes();
  return new ZipCoordinateDataset(parse(sourceBytes), CENSUS_SOURCE,
      Integer.toString(CENSUS_SOURCE_YEAR), sha256(sourceBytes));
}
```

Verification: reader tests assert an exact known checksum and that malformed/empty sources fail before a dataset is returned.

#### Code Edit 7.2
- File: `website/src/main/java/dev/christopherbell/location/zip/ZipCoordinateService.java`
- Lines: 21-68
- Action: replace

Current:
```java
var importedCoordinates = zipCoordinateGazetteerReader.readBundledCensusData();
// compare and mutate every invocation
return ZipCoordinateImportResult.builder().processed(importedCoordinates.size()).build();
```

Proposed:
```java
var dataset = zipCoordinateGazetteerReader.readBundledCensusData();
if (state.isCompletedChecksum(dataset.checksum())) return noOpResult(state);
var result = reconcile(dataset.coordinates());
stateRepository.save(completedState(dataset, result, clock.instant()));
return result;
```

Verification: service tests prove same-checksum no-op invokes no coordinate save/delete and changed/partial runs converge with truthful state.

### Task 8 - Complete Back Office, indexes, documentation, and delivery gates

Sequence / dependencies:
- Integrates Tasks 1-7 after their focused tests pass.

Before-Edit Brief:
- Behavior: Back Office separates Preview and Apply, shows import status, requires explicit duplicate confirmation, and reports ZIP no-op metadata; migration ensures preview TTL and query indexes.
- Invariants: mutations remain ADMIN-only and require CSRF; UI renders untrusted values through `sanitize`; no destructive action runs from page load.
- Boundary/API: only `lib/api.js` owns new endpoint strings; first-party code uses `2026-07-26` preview/apply/status/freshness routes.
- Effects and failures: safe retryable UI errors preserve previews/status; consumed/stale preview requires a new preview.
- Tests and evidence: JavaScript unit tests, focused Java tests, full check, packaged local Mongo acceptance, independent review, CI, merge, production smoke, issue closure, test report, and Builder continuity.

- [ ] Add migration/index tests and Back Office behavior tests before implementation.
- [ ] Implement templates/API helpers/JS and update WFL, Location, configuration, and static JS READMEs.
- [ ] Run focused then full verification and `git diff --check`.
- [ ] Package and run on a disposable Mongo database and non-8080 port; verify public freshness and protected admin routes.
- [ ] Commit/push, open PR, wait for all CI, obtain independent review, remediate findings, merge, verify production, and close #1169-#1175.

#### Code Edit 8.1
- File: `website/src/main/resources/static/js/back-office.js`
- Lines: 647-962
- Action: replace

Current:
```javascript
async function importRestaurants(button) { /* immediately POST direct import */ }
async function dedupeRestaurants(button) { /* immediately POST destructive cleanup */ }
async function importZipCoordinates(button) { /* counts only */ }
```

Proposed:
```javascript
async function previewRestaurants(button) { /* render counts and enable token-bound Apply */ }
async function applyRestaurantPreview(button) { /* POST exact preview token */ }
async function previewDedupe(button) { /* render groups/survivors */ }
async function applyDedupePreview(button) { /* exact confirmation payload */ }
async function importZipCoordinates(button) { /* render no-op/checksum/version/completion */ }
```

Verification: new `back-office-wfl-imports.test.js` exercises preview/apply URLs, exact bodies, escaping, button gates, stale preview recovery, and ZIP no-op markup; touched JS passes `node --check`.

#### Code Edit 8.2
- File: `website/src/main/resources/templates/back-office.html`
- Lines: 164-192
- Action: replace

Current:
```html
<button data-operation="wfl-import">Import Restaurants</button>
<button data-operation="wfl-dedupe">Remove Duplicate Names</button>
<button data-operation="location-zip-import">Import ZIP Coordinates</button>
```

Proposed:
```html
<button data-operation="wfl-import-preview">Preview Import</button>
<button data-operation="wfl-import-apply" disabled>Apply Preview</button>
<button data-operation="wfl-dedupe-preview">Preview Duplicates</button>
<button data-operation="wfl-dedupe-apply" disabled>Apply Confirmed Merge</button>
<button data-operation="location-zip-import">Import ZIP Coordinates</button>
```

Verification: template/JavaScript tests prove initial Apply buttons are disabled and become enabled only from valid preview state.

#### Code Edit 8.3
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V002EnsureWflLocationIndexes.java`
- Lines: after 0
- Action: add

Proposed:
```java
@Component
public final class V002EnsureWflLocationIndexes implements ApplicationMigration {
  public String id() { return "002"; }
  public void apply(MongoTemplate mongo) {
    // Named rating-group support, preview TTL, and import-state indexes; idempotent creation.
  }
}
```

Verification: migration test applies twice and asserts stable named indexes; migration checksum remains immutable after merge.

## Risks

- OSM data may change between preview and apply. The apply intentionally fails stale rather than mutating a different plan.
- The current unique sparse normalized-name index means most duplicates are legacy rows without the normalized field; preview uses normalized live names and observed versions to handle them safely.
- Lease expiry during a slow Overpass request could permit overlap. Configuration validation requires lease duration to exceed total request timeout with margin; the coordinator renews before mutation and aborts if ownership is lost.
- WFL configuration shape changes could break production startup. The checked-in default/prod context is tested, and deployment's candidate-port gate prevents switching a failed candidate live.
- ZIP state persistence can fail after coordinate writes. Rerun reconciliation is idempotent and saves a truthful completed state without duplicating rows.

## Validation

- Witness focused RED/GREEN for repository aggregation, configuration validation, lease/status behavior, import planning/token lifecycle, dedupe preflight, public freshness, and ZIP checksum no-op.
- Run focused Java classes, `node --check` on touched scripts, `:website:jsTest`, `:website:check`, and `git diff --check`.
- Exercise a packaged JAR on a non-8080 port and disposable Mongo database with seeded WFL/ZIP state.
- Require independent review, all GitHub CI/CodeQL/Dependency Review gates, merge, listener rotation, production public smoke, protected-route authorization smoke, and GitHub issue closure.

## Unit Testing

- `WflPropertiesTest`: valid bind plus every invalid metro/source/schedule/duration partition.
- `OpenStreetMapRestaurantClientTest`: typed metros produce the same four bounded Overpass clauses.
- `RestaurantRatingRepositoryIntegrationTest`: Mongo group/sort/limit ordering and empty result.
- `RestaurantServiceTest` / focused coordinator/planner tests: indexed candidates, dry-run purity, checksum staleness, lease contention/ownership, status redaction, duplicate preflight atomicity, and public freshness.
- `RestaurantControllerTest`: public freshness; ADMIN preview/apply/status; auth/CSRF/invalid/stale cases.
- `ZipCoordinateGazetteerReaderTest` and `ZipCoordinateServiceTest`: exact checksum, first apply, no-op rerun, changed source, parse failure, and state persistence.
- `V002EnsureWflLocationIndexesTest`: idempotent named index creation.
- `back-office-wfl-imports.test.js` and WFL freshness tests: safe preview/apply state and escaped public/admin markup.

## Local Testing

1. Confirm focused RED for each task before production code.
2. Run focused Java tests after every slice.
3. Run `node --check` on all touched JavaScript and `:website:jsTest`.
4. Run `:website:check`; baseline at merge `5835a3c2` passed in 1m46s with 231 JavaScript tests.
5. Run `git diff --check` and inspect the complete branch diff.
6. Build the executable JAR, start it on a non-8080 port with a unique disposable Mongo database, seed controlled WFL/ZIP records, and exercise public freshness plus protected preview/status routes.
7. Remove the exact disposable database and stop only the test PID; confirm production port 8080 stayed on its original PID throughout local testing.
8. After review and all GitHub gates pass, merge, wait for native auto-deployment, confirm the listener PID changes, smoke `/`, `/wfl`, `/wfl/top-rated`, freshness, and protected admin endpoints, then confirm #1169-#1175 are closed.

## Rollback or Recovery

- Before merge, revert only the Batch 6 branch commits or amend the isolated worktree; never mutate the authoritative checkout.
- Preview/apply staleness or lease loss fails before mutation and is recovered by generating a new preview after the current lease expires/releases.
- ZIP reruns reconcile by key and checksum, so a state-write failure after coordinate writes converges safely on retry.
- After merge, the native deployment pipeline retains the previous release and automatically rolls back if candidate or production smoke verification fails.
- Database additions are backward-compatible collections/fields/indexes; application rollback ignores them and no destructive reverse migration is required.

## Completion Criteria

- Each issue #1169-#1175 has direct automated and local runtime evidence matching the approved specification.
- Focused tests, 231-or-more JavaScript tests, full `:website:check`, diff hygiene, independent review, and every required GitHub gate pass at final head.
- The PR is merged, production rotates to the merge, WFL public pages/freshness remain healthy, protected admin endpoints deny anonymous callers, and all seven issues are closed.
- Builder contains a validated test report, spoke update, review, session memory, refreshed indexes, and an updated campaign ledger showing only #1176-#1181 remain.

## Completion Outcome

- PR [#1256](https://github.com/azurras/christopherbell.dev/pull/1256) passed every required gate and squash-merged as `abd2051e76155e5c01137ebec10c2d7550ec3556`.
- Production auto-deployed to listener PID `41176`; local and external public smoke checks passed while operator routes remained protected.
- Issues #1169-#1175 are closed. The campaign continues with only #1176-#1181 open.
