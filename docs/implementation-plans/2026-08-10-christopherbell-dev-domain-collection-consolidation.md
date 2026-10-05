# christopherbell.dev Domain Collection Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the website's 48-collection MongoDB layout with exactly 14 domain-owned collections and delete every superseded collection during one verified maintenance cutover.

**Architecture:** Persist domain objects inside a canonical envelope with a lossless namespaced BSON `_id`, mandatory `_kind`, `schemaVersion`, and `payload`. One kind-scoped Mongo boundary performs all encoding, query prefixing, optimistic concurrency, and decoding; domain adapters retain existing service-facing repository APIs. A manifest-driven migration builds 14 temporary targets, proves counts/checksums/indexes on a restored clone and live database, publishes through a durable rename ledger, starts only a target-schema release, and drops the exact superseded allowlist after live verification.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, MongoDB 8, BSON, JUnit 5, AssertJ, Mockito, Gradle, JavaScript executed by `mongosh`, PowerShell 7, Windows PowerShell 5.1, Pester 5.9, native Windows services.

## Global Constraints

- The target catalog is exactly `accounts`, `sessions`, `communications`, `content`, `federation`, `music`, `whatsforlunch`, `shared_folder`, `vehicles`, `location`, `canes_box_tracker`, `application_runtime`, `application_migrations`, and `admin_activity`.
- Every migrated document has canonical `_id: { kind: <_kind>, legacyId: <original BSON _id> }` in that exact field order, mandatory lower-case allowlisted `_kind`, integer `schemaVersion`, and lossless `payload`.
- Every read, update, delete, count, uniqueness check, and index that is not global is scoped by exact `_kind`; direct unscoped domain use of `MongoTemplate`, `MongoRepository`, or raw `MongoCollection` is forbidden by architecture tests.
- Preserve public HTTP behavior, authorization, optimistic concurrency, BSON types, unique/sparse/partial indexes, TTL values, collation, and retention semantics.
- Translate a legacy sparse index into an exact `_kind AND field-exists` partial index when shared-collection scoping is required, because MongoDB forbids combining the literal sparse flag with a partial filter; preserve absent/null membership and uniqueness semantics in tests.
- Use the isolated branch `codex/domain-collection-consolidation` from current `origin/main`; never modify the authoritative dirty checkout.
- Invoke `chris-street-style` before every production source, test, migration, script, executable configuration, or code-bearing template edit.
- No production source collection is renamed or dropped until a checksummed backup has passed a dry restore and the exact migration has passed disposable-Mongo, restored-clone, alternate-port, and live pre-publication verification.
- Every destructive operation requires the protected deployment lock, stopped website writer, suspended service recovery, exact database/release/marker/manifest/process identity, and a literal collection allowlist.
- Do not expose MongoDB URIs, service command lines, application secrets, or Cloudflare credentials in commands, logs, reports, or error messages.

---

## Document Status

complete

## Objective

Deliver the approved 14-collection application schema, migration engine, production cutover and rollback tooling, automated verification, pull request, CI/merge, guarded live cutover, immediate exact-source deletion, and Builder closeout.

## Goals

1. Centralize BSON envelope, ID, query, update, and optimistic-lock behavior behind one tested kind-scoped boundary.
2. Move every current and dormant runtime mapping into one of the 14 target collections without changing service-facing APIs.
3. Build all partial indexes from one exact manifest and prove their semantic equivalence.
4. Provide preview, cutover, recovery, inventory, and rollback commands that fail closed.
5. Finish with exactly 14 production collections, verified data equivalence, healthy runtime behavior, and no superseded collection.

## Inputs

- Approved specification: `C:\Users\Christopher\Developer\builder\docs\specs\2026-08-10-christopherbell-dev-domain-collection-consolidation.md`
- Work ledger: `C:\Users\Christopher\Developer\builder\docs\work\2026-08-10-christopherbell-dev-domain-collection-consolidation.md`
- Spoke: `A:\Projects\christopherbell.dev`, remote `https://github.com/azurras/christopherbell.dev.git`
- Inspected baseline: `origin/main` at `f4bc817d22abba70901fe4f17a93b4e52081085c`
- Verified production baseline: 48 collections, 164 indexes, active release `f4bc817d22abba70901fe4f17a93b4e52081085c`
- Existing guarded deployment, writer-start, backup, inventory, music schema-direction, and rollback code is retained and generalized rather than bypassed.

## Branch

- Base: refreshed `origin/main`
- Feature branch: `codex/domain-collection-consolidation`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\domain-collection-consolidation`

## Non-Goals

- No universal collection, database-engine change, public route change, API redesign, feature redesign, or weakening of ACLs and service guards.
- No deletion of backup archives, unrelated release artifacts, or collections outside the exact migration manifest.
- No dual-write observation period and no legacy fallback reads after successful publication.

## Assumptions

- MongoDB 8 remains available locally as a disposable isolated process and as the protected production service.
- All current domain IDs are representable as original BSON values inside `legacyId`; unexpected BSON types fail preview.
- Maintenance downtime is acceptable for the bounded backup, migration, publication, verification, and deletion sequence.
- `application_migrations` can host both migration records and the cutover ledger as distinct `_kind` values.

## Open Questions

None. If any source index cannot be represented as a kind-scoped partial index, stop before publication and return to design review.

## File Structure

### Shared persistence boundary

- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainDocumentKind.java` — immutable kind metadata.
- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/NamespacedMongoId.java` — canonical ordered BSON ID.
- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainDocumentEnvelope.java` — raw envelope representation.
- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/MalformedDomainDocumentException.java` — redacted invalid-envelope failure.
- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainCollectionManifest.java` — exact 14 targets, source mapping, kinds, schemas, and indexes.
- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/KindScopedMongoOperations.java` — sole runtime CRUD/query/update boundary.
- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/MongoTemplateKindScopedOperations.java` — the only production implementation of that boundary.
- `website/src/test/java/dev/christopherbell/configuration/mongo/domain/*Test.java` — unit and disposable-Mongo contract tests.

### Domain adapters

- Existing repository interfaces remain service-facing ports but stop extending `MongoRepository`.
- New `Mongo*Store` adapters live beside their domain ports and use only `KindScopedMongoOperations`.
- Existing manual `MongoTemplate` query services are migrated to the same boundary.
- Existing model `@Document` annotations are removed so Spring cannot recreate old physical names.

### Migration and operations

- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V015RequireDomainCollectionSchema.java` — startup schema gate, not destructive migration.
- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java` — read-only runtime validation of the durable cutover record.
- `ops/production/windows/scripts/DomainCollectionManifest.js` — immutable target/source/index manifest shared by preview and cutover scripts.
- `ops/production/windows/scripts/Invoke-DomainCollectionMigration.js` — BSON-preserving stage, verify, publish, drop, and reverse operations.
- `ops/production/windows/modules/Production.DomainCollections.psm1` — protected process, marker, backup, clone, and operation orchestration.
- Existing deploy/operations/command/writer-start modules integrate the new schema marker and lock.
- `docs/operations/mongodb-collection-catalog.md` becomes the 14-target/per-kind operational catalog.

## Exact Kind Manifest

| Target | `_kind` | Legacy source | Java type or owner |
|---|---|---|---|
| `accounts` | `account` | `accounts` | `account.model.Account` |
| `accounts` | `account_follow` | `account_follows` | `account.follow.AccountFollow` |
| `accounts` | `account_trust_relationship` | `account_trust_relationships` | `account.trust.AccountTrustRelationship` |
| `accounts` | `account_deletion_job` | `account_deletion_jobs` | `account.deletion.AccountDeletionJob` |
| `sessions` | `browser_session` | `browser_sessions` | `configuration.security.browser.BrowserSession` |
| `sessions` | `conversation_archive_state` | `conversation_archive_states` | `message.conversation.ConversationArchiveState` |
| `communications` | `message` | `messages` | `message.model.Message` |
| `communications` | `notification` | `notifications` | `notification.model.Notification` |
| `communications` | `notification_preference` | `notification_preferences` | `notification.preference.NotificationPreference` |
| `communications` | `notification_delivery_guard` | `notification_delivery_guards` | `notification.delivery.NotificationDeliveryGuard` |
| `communications` | `notification_rate_limit` | `notification_rate_limits` | `notification.delivery.NotificationRateLimit` |
| `content` | `post` | `posts` | `post.model.Post` |
| `content` | `post_like` | `post_likes` | `post.like.PostLike` |
| `content` | `post_report` | `post_reports` | `report.model.PostReport` |
| `content` | `hidden_post_thread` | `hidden_post_threads` | `post.hide.HiddenPostThread` |
| `content` | `post_link_preview_cache` | `post_link_preview_cache` | `post.preview.PostLinkPreviewCacheEntry` |
| `federation` | `federation_scan_state` | `federation_scan_state` | `federation.outbound.FederationScanState` |
| `federation` | `federation_delivery_job` | `federation_delivery_jobs` | `federation.outbound.FederationDeliveryJob` |
| `music` | `music_track` | `music_tracks` | `music.catalog.MusicTrack` |
| `music` | `music_playlist` | `music_playlists` | `music.library.MusicPlaylist` |
| `music` | `music_metadata_edit` | `music_metadata_edits` | `music.metadata.MusicMetadataEdit` |
| `music` | `music_runtime_state` | `music_runtime_state` | `music.radio.MusicRuntimeStateDocument` |
| `music` | `music_radio_history` | `music_radio_history` | `music.radio.MusicRadioHistoryEvent` |
| `music` | `music_access_attempt` | `music_access_attempts` | `music.security.MusicAccessAttempt` |
| `whatsforlunch` | `restaurant` | `whatsforlunch` | `whatsforlunch.restaurant.model.Restaurant` |
| `whatsforlunch` | `vote` | `whatsforlunch_ratings` | `whatsforlunch.restaurant.model.RestaurantVote` |
| `whatsforlunch` | `favorite` | `whatsforlunch_favorites` | `whatsforlunch.restaurant.model.RestaurantFavorite` |
| `whatsforlunch` | `preference` | `whatsforlunch_preferences` | `whatsforlunch.restaurant.model.WhatsForLunchPreference` |
| `whatsforlunch` | `session` | `whatsforlunch_sessions` | `whatsforlunch.restaurant.model.WhatsForLunchSession` |
| `whatsforlunch` | `daily_picks` | `whatsforlunch_daily_picks` | `whatsforlunch.restaurant.model.DailyLunchPicks` |
| `whatsforlunch` | `import_state` | `restaurant_import_state` | `whatsforlunch.restaurant.model.RestaurantImportState` |
| `whatsforlunch` | `import_preview` | `restaurant_import_previews` | `whatsforlunch.restaurant.importing.RestaurantImportPreviewDocument` |
| `shared_folder` | `audit_event` | `shared_folder_audit` | `sharedfolder.audit.SharedFolderAuditEvent` |
| `shared_folder` | `maintenance_lease` | `shared_folder_maintenance_leases` | `sharedfolder.maintenance.SharedFolderMaintenanceLeaseDocument` |
| `shared_folder` | `media_job` | `shared_folder_media_jobs` | `sharedfolder.media.MediaJob` |
| `shared_folder` | `mutation_recovery` | `shared_folder_mutation_recoveries` | `sharedfolder.service.SharedFolderMutationRecovery` |
| `shared_folder` | `radio_state` | `shared_folder_radio` | `sharedfolder.radio.SharedFolderRadioDocument` |
| `shared_folder` | `recycle_item` | `shared_folder_recycle_items` | `sharedfolder.recycle.SharedFolderRecycleItem` |
| `shared_folder` | `upload_session` | `shared_folder_upload_sessions` | `sharedfolder.upload.SharedFolderUploadSession` |
| `vehicles` | `vehicle` | `vehicles` | `vehicle.model.Vehicle` |
| `vehicles` | `vin_decode_cache` | `vehicle_vin_decode_cache` | `vehicle.model.VehicleVinDecodeCache` |
| `vehicles` | `nhtsa_import_state` | `vehicle_import_state` | `vehicle.nhtsa.model.NhtsaVinImportState` |
| `vehicles` | `random_vin_import_state` | `vehicle_import_state` | `vehicle.randomvin.model.RandomVinImportState` |
| `location` | `zip_coordinate` | `location_zip_coordinates` | `location.model.ZipCoordinate` |
| `location` | `zip_import_state` | `zip_coordinate_import_state` | `location.model.ZipCoordinateImportState` |
| `canes_box_tracker` | `price_snapshot` | `canes_box_price_snapshots` | `canesboxtracker.model.CanesBoxPriceSnapshot` |
| `application_runtime` | `application_lease` | `application_leases` | `libs.mongo.lease.MongoLeaseDocument` |
| `application_runtime` | `scheduled_collector_run` | `scheduled_collector_runs` | `libs.mongo.lease.ScheduledCollectorRun` |
| `application_migrations` | `migration_record` | `application_migrations` | `configuration.mongo.migration.MigrationRecord` |
| `application_migrations` | `domain_collection_cutover` | none; created by cutover | `configuration.mongo.migration.DomainCollectionCutoverLedger` |
| `admin_activity` | `admin_activity` | `admin_activity` | `admin.model.AdminActivity` |
| `admin_activity` | `pending_action` | `command_center_pending_actions` | `admin.commandcenter.action.PendingActionDocument` |

`music_queue_state` and `music_radio_state` are rollback-retained artifacts from V014,
not authoritative inputs to V015. Preview must prove that the current release and marker
make `music_runtime_state` authoritative, record the retained collections in the exact
superseded allowlist, and never merge their potentially stale payloads into `music`.
All manifest indexes on original domain fields use `payload.<field>` keys and an exact
`partialFilterExpression: { _kind: <kind> }`; TTL remains on the corresponding
`payload.<expiryField>`.

## Task Breakdown

### Task 1 - Create the canonical kind-scoped persistence boundary

Sequence / dependencies:
- First implementation task; every later runtime adapter consumes these exact types.

Interfaces:
- Produces `DomainDocumentKind<T>(collection, kind, schemaVersion, javaType)`.
- Produces `NamespacedMongoId.of(String kind, Object legacyId)` with exact BSON order.
- Produces `KindScopedMongoOperations<T>` methods `findById`, `find`, `findOne`, `count`, `exists`, `insert`, `save`, `updateFirst`, `remove`, and `collectionName`.
- `save` performs insert when the legacy record is absent and compare-and-set on `payload.<versionField>` when metadata declares a version property.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: encode/decode losslessly and inject exact kind criteria into every operation.
  - Invariants: `_id.kind == _kind`, original BSON ID type survives round trip, caller queries cannot address envelope metadata, and stale versions never overwrite winners.
  - Boundary/API: domain code supplies domain field names; the boundary maps them under `payload.` and returns domain types.
  - Effects and failures: Mongo reads/writes only the kind's approved target; malformed envelopes, unapproved fields, and stale versions throw redacted typed failures.
  - Tests and evidence: first fail unit tests for ID order, query scoping, payload mapping, and version contention; finish with real Mongo insert/read/update/delete and index-backed query evidence.

- [ ] **Step 1: Write failing unit tests for envelope and query behavior.**
- [ ] **Step 2: Run the focused tests and confirm failures because the boundary types do not exist.**
- [ ] **Step 3: Implement the immutable metadata, envelope codec, query mapper, and operations boundary.**
- [ ] **Step 4: Add disposable-Mongo tests for BSON scalar IDs, ObjectId IDs, Long/Decimal128 payloads, version contention, and kind isolation.**
- [ ] **Step 5: Run focused unit and disposable tests, then commit `feat: add kind-scoped Mongo persistence`**.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainDocumentKind.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.domain;

import java.util.Objects;
import java.util.regex.Pattern;

public record DomainDocumentKind<T>(
    String collection, String kind, int schemaVersion, Class<T> javaType) {
  private static final Pattern NAME = Pattern.compile("[a-z][a-z0-9_]*");

  public DomainDocumentKind {
    if (!NAME.matcher(collection).matches() || !NAME.matcher(kind).matches()) {
      throw new IllegalArgumentException("Mongo collection and kind must be canonical.");
    }
    if (schemaVersion < 1) {
      throw new IllegalArgumentException("Mongo schema version must be positive.");
    }
    Objects.requireNonNull(javaType, "javaType");
  }
}
```

Verification:
- `.\gradlew.bat :website:test --tests 'dev.christopherbell.configuration.mongo.domain.*' --console=plain`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/domain/NamespacedMongoId.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.domain;

import org.bson.Document;

public record NamespacedMongoId(String kind, Object legacyId) {
  public NamespacedMongoId {
    if (kind == null || kind.isBlank() || legacyId == null) {
      throw new IllegalArgumentException("Namespaced Mongo identity is incomplete.");
    }
  }

  public Document toBson() {
    return new Document("kind", kind).append("legacyId", legacyId);
  }

  public static NamespacedMongoId require(Document id, String expectedKind) {
    if (id == null || !id.keySet().equals(java.util.Set.of("kind", "legacyId"))
        || !expectedKind.equals(id.getString("kind")) || id.get("legacyId") == null) {
      throw new MalformedDomainDocumentException("Mongo document identity is malformed.");
    }
    return new NamespacedMongoId(expectedKind, id.get("legacyId"));
  }
}
```

Verification:
- `.\gradlew.bat :website:test --tests '*NamespacedMongoIdTest' --console=plain`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/domain/KindScopedMongoOperations.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.domain;

import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.UpdateResult;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

public interface KindScopedMongoOperations<T> {
  Optional<T> findById(Object legacyId);
  Optional<T> findOne(Query domainQuery);
  List<T> find(Query domainQuery, Pageable page);
  long count(Query domainQuery);
  boolean exists(Query domainQuery);
  T insert(T value);
  T save(T value);
  UpdateResult updateFirst(Query domainQuery, Update domainUpdate);
  DeleteResult remove(Query domainQuery);
  String collectionName();
}
```

Verification:
- `.\gradlew.bat :website:test --tests '*KindScopedMongoOperationsTest' --console=plain`

### Task 2 - Lock the exact 14-target manifest and architecture

Sequence / dependencies:
- Runs after Task 1; metadata entries use `DomainDocumentKind`.

Interfaces:
- Produces `DomainCollectionManifest.ALL_COLLECTIONS`, `ALL_KINDS`, `forType(Class<?>)`, `forSource(String)`, and exact `IndexDefinition` records.
- Later migration JavaScript must be generated from or byte-for-byte checked against this manifest.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: make target names, kinds, sources, schema versions, and indexes compile-time visible and architecture-testable.
  - Invariants: exactly 14 unique targets, every current/dormant source maps once, every kind maps once, and no legacy runtime mapping survives.
  - Boundary/API: the manifest is immutable application infrastructure; modules own adapters, not arbitrary collection names.
  - Effects and failures: application startup fails before writers start if manifest uniqueness or generated-script digest is wrong.
  - Tests and evidence: replace the collection-name catalog with exact target/kind/source checks and pin the existing direct-access inventory so it cannot grow before Tasks 3-5 reduce it to zero.

- [ ] **Step 1: Change catalog tests to expect exactly 14 manifest targets while retaining an exact temporary baseline of legacy mappings.**
- [ ] **Step 2: Implement the manifest with all 52 runtime kinds, including dormant pending actions, federation scan state, account deletion jobs, and both vehicle import-state types.**
- [ ] **Step 3: Add a checked temporary inventory of every legacy `@Document`, `MongoRepository`, and direct `MongoTemplate` owner; fail if the inventory grows.**
- [ ] **Step 4: Make Tasks 3-5 delete entries from that inventory with their adapters; Task 5 must leave only approved migration infrastructure and the shared boundary.**
- [ ] **Step 5: Run architecture/catalog tests and commit `refactor: define fourteen Mongo domain collections`**.

#### Code Edit 2.1
- File: `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java`
- Lines: 27-125
- Action: replace

Current:
```java
class MongoCollectionCatalogTest {
  private static final Map<String, Set<String>> APPROVED_SHARED_DOCUMENT_MAPPINGS = Map.of(
      "vehicle_import_state", Set.of(
          "dev.christopherbell.vehicle.nhtsa.model.NhtsaVinImportState",
          "dev.christopherbell.vehicle.randomvin.model.RandomVinImportState"));
  private static final Map<String, Set<String>> MANUAL_COLLECTIONS_BY_OWNER = Map.ofEntries(
      manualOwner("dev.christopherbell.account.AdminAccountQueryService", "accounts"),
      manualOwner("dev.christopherbell.configuration.mongo.migration.V014ConsolidateMusicRuntimeState",
          "music_queue_state", "music_radio_state", "music_runtime_state"));
}
```

Proposed:
```java
class MongoCollectionCatalogTest {
  private static final Set<String> TARGETS = Set.of(
      "accounts", "sessions", "communications", "content", "federation", "music",
      "whatsforlunch", "shared_folder", "vehicles", "location", "canes_box_tracker",
      "application_runtime", "application_migrations", "admin_activity");

  @Test
  void manifestOwnsExactlyTheApprovedTargetsAndEveryKindOnce() {
    assertThat(DomainCollectionManifest.collectionNames()).containsExactlyInAnyOrderElementsOf(TARGETS);
    assertThat(DomainCollectionManifest.collectionNames()).hasSize(14);
    assertThat(DomainCollectionManifest.duplicateKinds()).isEmpty();
    assertThat(DomainCollectionManifest.unmappedLegacySources()).isEmpty();
  }

  @Test
  void legacyDirectAccessCannotGrowDuringTheAdapterMigration() {
    assertThat(sourceViolations("MongoRepository", "MongoTemplate", "MongoCollection"))
        .containsExactlyElementsOf(TEMPORARY_LEGACY_ACCESS_BASELINE);
  }
}
```

Verification:
- `.\gradlew.bat :website:test --tests dev.christopherbell.architecture.MongoCollectionCatalogTest --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest --console=plain`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainCollectionManifest.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.domain;

import java.util.List;
import java.util.Set;

public final class DomainCollectionManifest {
  public static final Set<String> COLLECTIONS = Set.of(
      "accounts", "sessions", "communications", "content", "federation", "music",
      "whatsforlunch", "shared_folder", "vehicles", "location", "canes_box_tracker",
      "application_runtime", "application_migrations", "admin_activity");
  public static final List<DomainDocumentKind<?>> KINDS = DomainKinds.all();

  private DomainCollectionManifest() {}
}
```

Verification:
- `.\gradlew.bat :website:test --tests dev.christopherbell.architecture.MongoCollectionCatalogTest --console=plain`

### Task 3 - Migrate accounts, sessions, communications, content, federation, and admin adapters

Sequence / dependencies:
- Runs after Tasks 1-2; these high-connectivity domains establish the adapter pattern before data-heavy domains.

Interfaces:
- Existing service-facing repository method signatures remain unchanged.
- Each concrete adapter requests a fixed `DomainDocumentKind<T>` and exposes no collection-name parameter.
- Account deletion scans target collections by allowlisted kinds rather than legacy collection names.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: preserve account/auth/session/message/notification/post/federation/admin behavior over the new envelopes.
  - Invariants: email/username uniqueness, session TTL, post expiration, notification ordering, federation lease semantics, and pending-action expiry remain exact.
  - Boundary/API: controllers/services retain their current ports; adapters translate field paths and IDs internally.
  - Effects and failures: writes affect one kind only; delete-account remains bounded to the account's documents; malformed cross-kind state fails redacted.
  - Tests and evidence: repository contract tests assert `_kind` on every generated query and existing service/controller tests remain unchanged and green.

Files:
- Accounts: `account/**/*Repository.java`, `AccountFollowStore.java`, `MongoAccountLoginStore.java`, `MongoAccountDeletionOperations.java`, `AdminAccountQueryService.java`.
- Sessions/communications: `configuration/security/browser/*Store.java`, `message/**/*Repository.java`, `ConversationArchiveService.java`, `notification/**/*Repository.java`, `NotificationFanoutGuard.java`.
- Content/federation/admin: `post/**/*Repository.java`, `PostLikeStore.java`, `report/query/ReportQueryService.java`, `federation/**/*Repository.java`, `admin/activity/AdminActivityQueryService.java`, `admin/commandcenter/action/MongoPendingActionStore.java`.

- [ ] **Step 1: Add failing adapter contract tests for every public repository method and manual query path in these domains.**
- [ ] **Step 2: Convert repository interfaces from Spring Data inheritance to explicit domain ports and remove `@Document` only from the model types owned by this task.**
- [ ] **Step 3: Add concrete Mongo adapters using kind-scoped operations and migrate manual query/update/delete paths.**
- [ ] **Step 4: Run focused domain, security, controller, and architecture tests.**
- [ ] **Step 5: Commit `refactor: move social domains into shared Mongo collections`**.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/account/AccountRepository.java`
- Lines: 10-36
- Action: replace

Current:
```java
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AccountRepository extends MongoRepository<Account, String> {
```

Proposed:
```java
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface AccountRepository {
  Account save(Account account);
  Optional<Account> findById(String id);
  boolean existsById(String id);
  void deleteById(String id);
  Page<Account> findAll(Pageable pageable);
```

Verification:
- `.\gradlew.bat :website:test --tests 'dev.christopherbell.account.*' --tests 'dev.christopherbell.configuration.security.browser.*' --console=plain`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/post/PostRepository.java`
- Lines: 8-15
- Action: replace

Current:
```java
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PostRepository extends MongoRepository<Post, String> {
```

Proposed:
```java
public interface PostRepository {
  Post save(Post post);
  java.util.Optional<Post> findById(String id);
  boolean existsById(String id);
  void delete(Post post);
  void deleteById(String id);
```

Verification:
- `.\gradlew.bat :website:test --tests 'dev.christopherbell.post.*' --tests 'dev.christopherbell.message.*' --tests 'dev.christopherbell.notification.*' --tests 'dev.christopherbell.federation.*' --tests 'dev.christopherbell.admin.*' --console=plain`

### Task 4 - Migrate music and Whats For Lunch adapters

Sequence / dependencies:
- Runs after Task 3; consumes the established adapter conventions and preserves the existing V014 runtime-state behavior until V015 publication.

Interfaces:
- Music runtime queue/radio keep separate optimistic versions under `_kind: "music_runtime_state"` and legacy IDs `queue`/`radio`.
- Whats For Lunch kinds are `restaurant`, `vote`, `favorite`, `preference`, `session`, `daily_picks`, `import_state`, and `import_preview`.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: route all music and WFL reads/writes to `music` and `whatsforlunch` with exact kind isolation.
  - Invariants: queue/radio independent CAS, track and playlist ordering, radio history, vote uniqueness, restaurant normalized-name uniqueness, session revision, import preview TTL, and pagination remain exact.
  - Boundary/API: services retain current Java domain types and methods; no envelope escapes the adapters.
  - Effects and failures: migration-state absence remains supported; stale CAS, duplicate vote/name, or malformed envelope fails without partial write.
  - Tests and evidence: run all music/WFL tests plus real Mongo version-winner/stale-loser and cross-kind collision tests.

- [ ] **Step 1: Write failing tests for new target names, kind filters, partial unique indexes, and runtime CAS.**
- [ ] **Step 2: Migrate all music repository/manual Mongo paths and remove their model `@Document` annotations.**
- [ ] **Step 3: Migrate all WFL repository/manual bounded-query paths and remove their model `@Document` annotations.**
- [ ] **Step 4: Run focused and disposable-Mongo suites.**
- [ ] **Step 5: Commit `refactor: consolidate music and lunch persistence`**.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRuntimeStateStore.java`
- Lines: 16-103
- Action: replace

Current:
```java
@Component
public final class MusicRuntimeStateStore {
  private final MongoTemplate mongo;

  public Optional<MusicQueueState> findQueue() {
    return Optional.ofNullable(mongo.findById(
        MusicRuntimeStateDocument.QUEUE_ID,
        MusicRuntimeStateDocument.class,
        MusicRuntimeStateDocument.COLLECTION)).map(MusicRuntimeStateDocument::toQueueState);
  }
}
```

Proposed:
```java
@Component
public final class MusicRuntimeStateStore {
  private final KindScopedMongoOperations<MusicRuntimeStateDocument> states;

  public Optional<MusicQueueState> findQueue() {
    return states.findById(MusicRuntimeStateDocument.QUEUE_ID)
        .map(MusicRuntimeStateDocument::toQueueState);
  }

  public MusicQueueState saveQueue(MusicQueueState state) {
    return states.save(MusicRuntimeStateDocument.forQueue(state)).toQueueState();
  }
}
```

Verification:
- `.\gradlew.bat :website:test --tests 'dev.christopherbell.music.*' --tests '*MusicRuntimeState*' --console=plain`

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/vote/RestaurantVoteRepository.java`
- Lines: 1-40
- Action: replace

Current:
```java
public interface RestaurantVoteRepository extends MongoRepository<RestaurantVote, String> {
  Optional<RestaurantVote> findBySessionIdAndRestaurantIdAndAccountId(
      String sessionId, String restaurantId, String accountId);
}
```

Proposed:
```java
public interface RestaurantVoteRepository {
  RestaurantVote save(RestaurantVote vote);
  Optional<RestaurantVote> findById(String id);
  Optional<RestaurantVote> findBySessionIdAndRestaurantIdAndAccountId(
      String sessionId, String restaurantId, String accountId);
  void deleteById(String id);
}
```

Verification:
- `.\gradlew.bat :website:test --tests 'dev.christopherbell.whatsforlunch.restaurant.*' --console=plain`

### Task 5 - Migrate shared-folder, vehicle, location, canes, lease, collector, and migration adapters

Sequence / dependencies:
- Runs after Task 4; completes runtime migration so architecture tests can forbid all direct legacy access.

Interfaces:
- Shared-folder kinds share `shared_folder`; vehicle import types remain distinct kinds in `vehicles`.
- `cbell-lib` exposes `MongoLeaseStore` and `ScheduledCollectorRunStore` ports; website supplies target-schema adapters so the reusable library no longer owns physical names.
- Migration state uses `_kind: "migration_record"`; cutover ledger uses `_kind: "domain_collection_cutover"`.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: complete kind-scoped persistence for remaining domains and shared lease/collector infrastructure.
  - Invariants: audit TTL, media job leases, upload recovery, VIN cache TTL, dual vehicle import states, ZIP uniqueness, collector history, global lease ownership, and migration CAS remain exact.
  - Boundary/API: cbell-lib depends on narrow store interfaces and has no website collection names.
  - Effects and failures: lease and migration state changes remain atomic; a kind mismatch or version loss blocks the caller.
  - Tests and evidence: existing domain tests plus new port contracts and real TTL/index/CAS checks.

- [ ] **Step 1: Add failing tests for shared-folder/vehicle/location/canes kind isolation and library store ports.**
- [ ] **Step 2: Convert remaining repositories/manual Mongo paths and remove their model `@Document` annotations.**
- [ ] **Step 3: Replace cbell-lib direct Mongo ownership with explicit store ports and website implementations.**
- [ ] **Step 4: Replace the temporary legacy-access inventory with the final zero-domain-bypass assertion, then run all remaining domain, cbell-lib, migration, and architecture tests.**
- [ ] **Step 5: Commit `refactor: consolidate remaining Mongo domains`**.

#### Code Edit 5.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/mongo/lease/MongoLeaseService.java`
- Lines: 3-54
- Action: replace

Current:
```java
@Service
@RequiredArgsConstructor
public class MongoLeaseService {
  public static final String COLLECTION = "application_leases";
  private final MongoTemplate mongo;
}
```

Proposed:
```java
@Service
@RequiredArgsConstructor
public class MongoLeaseService {
  private final MongoLeaseStore store;

  public boolean tryAcquire(String name, String ownerToken, Instant now, Instant expiresAt) {
    return store.tryAcquire(name, ownerToken, now, expiresAt);
  }

  public boolean renew(String name, String ownerToken, Instant now, Instant expiresAt) {
    return store.renew(name, ownerToken, now, expiresAt);
  }

  public boolean release(String name, String ownerToken) {
    return store.release(name, ownerToken);
  }
}
```

Verification:
- `.\gradlew.bat :cbell-lib:test :website:test --tests '*MongoLease*' --tests '*ScheduledCollector*' --console=plain`

#### Code Edit 5.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/mongo/lease/ScheduledCollectorCoordinator.java`
- Lines: 10-20
- Action: replace

Current:
```java
@Service
public class ScheduledCollectorCoordinator {
  private final MongoLeaseService leases;
  private final MongoTemplate mongo;
  private final Clock clock;
}
```

Proposed:
```java
@Service
public class ScheduledCollectorCoordinator {
  private final MongoLeaseService leases;
  private final ScheduledCollectorRunStore runs;
  private final Clock clock;
}
```

Verification:
- `.\gradlew.bat :cbell-lib:test :website:test --tests '*SharedFolder*' --tests '*Vehicle*' --tests '*ZipCoordinate*' --tests '*CanesBox*' --console=plain`

### Task 6 - Build the manifest-driven migration, checksum, index, publication, and rollback engine

Sequence / dependencies:
- Runs after all runtime adapters are target-schema ready.

Interfaces:
- Java startup gate `V015RequireDomainCollectionSchema` accepts only a completed `TARGET_ACTIVE` ledger matching release manifest digest.
- JavaScript actions: `preview`, `stage`, `verify-stage`, `publish-next`, `verify-live`, `drop-legacy`, `reverse-next`, and `restore-verify`.
- Every action returns one redacted JSON object with database, action, state, manifest digest, per-kind counts/checksums, index digests, and next operation.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: transform all source documents into 14 temporary targets, prove equivalence, resume ordered publication, delete exact legacy names, and reverse before deletion.
  - Invariants: canonical Extended JSON checksum preserves BSON type/order normalization; publication ledger is CAS-owned; per-collection rename is atomic; writer cannot start mid-sequence.
  - Boundary/API: scripts accept database/action/manifest digest through validated arguments and obtain credentials only from the existing protected process boundary.
  - Effects and failures: unexpected collection, ID, BSON type, target residue, count, checksum, index, or ledger owner stops before the next mutation; output is redacted.
  - Tests and evidence: raw unit fixtures plus real Mongo interruption at every stage/rename/drop boundary and exact reverse/restore proof.

- [ ] **Step 1: Write RED migration tests covering all source kinds, empty optional sources, collisions, malformed values, stale temp targets, and interruption at every ledger operation.**
- [ ] **Step 1a: Prove V014's target marker makes `music_runtime_state` authoritative and classify `music_queue_state`/`music_radio_state` as drop-only retained artifacts.**
- [ ] **Step 2: Implement immutable JS manifest and verify its SHA-256 against the Java manifest resource.**
- [ ] **Step 3: Implement BSON-preserving envelope conversion, canonical checksum, partial index creation, and exact verification.**
- [ ] **Step 4: Implement CAS ledger and resumable forward/reverse rename operations, then exact allowlisted drop.**
- [ ] **Step 5: Add V015 target-schema startup gate and release metadata `domainSchema: "TARGET"`.**
- [ ] **Step 6: Run JS tests and disposable Mongo full/interrupted/reverse/restore matrix on both PowerShell hosts; commit `feat: add domain collection migration engine`**.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V015RequireDomainCollectionSchema.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.migration;

import dev.christopherbell.configuration.mongo.domain.DomainCollectionManifest;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Component;

@Component
public final class V015RequireDomainCollectionSchema implements ApplicationMigration {
  @Override public String id() { return "015-require-domain-collection-schema"; }
  @Override public String checksum() { return DomainCollectionManifest.DIGEST; }
  @Override public String description() { return "Require the published 14-collection schema"; }

  @Override
  public void apply(MongoTemplate mongo) {
    DomainCollectionCutoverLedger.requireTargetActive(mongo, DomainCollectionManifest.DIGEST);
  }
}
```

Verification:
- `.\gradlew.bat :website:test --tests '*V015*' --tests '*MongoMigrationRunnerTest' --console=plain`

#### Code Edit 6.2
- File: `ops/production/windows/scripts/Invoke-DomainCollectionMigration.js`
- Lines: before 1
- Action: add

Proposed:
```javascript
const command = DomainCollectionCommand.parse(arguments);
const database = db.getSiblingDB(command.database);
const manifest = DomainCollectionManifest.requireDigest(command.manifestDigest);
const ledger = CutoverLedger.acquire(database, manifest, command.ownerToken, command.release);

const actions = Object.freeze({
  preview: () => Migration.preview(database, manifest),
  stage: () => Migration.stage(database, manifest, ledger),
  'verify-stage': () => Migration.verifyStage(database, manifest, ledger),
  'publish-next': () => Migration.publishNext(database, manifest, ledger),
  'verify-live': () => Migration.verifyLive(database, manifest, ledger),
  'drop-legacy': () => Migration.dropLegacy(database, manifest, ledger),
  'reverse-next': () => Migration.reverseNext(database, manifest, ledger),
  'restore-verify': () => Migration.verifyRestore(database, manifest, ledger)
});

print(JSON.stringify(actions[command.action]()));
```

Verification:
- `Invoke-Pester .\ops\production\windows\tests\Production.DomainCollections.Tests.ps1 -Output Detailed`

### Task 7 - Integrate guarded preview, backup/clone, cutover, deployment, deletion, and rollback commands

Sequence / dependencies:
- Runs after Task 6; wraps the migration engine in the existing protected Windows boundary.

Interfaces:
- Commands: `mongo-consolidation-preview`, `mongo-consolidate`, `mongo-consolidation-rollback`, and enhanced `mongo-inventory`.
- Mutating commands require `-ConfirmDomainCollectionCutover` or `-ConfirmDomainCollectionRollback`; automatic deploy can never set either switch.
- `Invoke-ProductionDomainCollectionCutover` owns one deployment lock across backup, stop, stage, publish, target start, verification, immediate drop, marker finalization, service recovery, and auto-deploy refresh.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: provide one interactive, auditable operation that produces the exact 14-collection live state and one restore-bound rollback operation.
  - Invariants: writer stopped for live mutation, recovery suspended, candidate uses non-production database/port, lock and fixed-root identity rechecked, backup dry-restored, manifest exact, deletion last.
  - Boundary/API: reuse protected config, fixed-root, service, backup, candidate, mongosh, and writer-start helpers; no direct ad hoc service/process invocation.
  - Effects and failures: any failure leaves either old schema running or writer stopped with exact recovery guidance; post-drop failure restores backup before old writer starts.
  - Tests and evidence: Pester mocks establish ordering/zero downstream effects; marker-owned real Mongo proves process identity and deletion boundaries; candidate test proves port/database isolation.

- [ ] **Step 1: Write RED Pester command-routing, confirmation, auto-deploy rejection, lock-ordering, and failure-containment tests.**
- [ ] **Step 2: Add `Production.DomainCollections.psm1` with marker, manifest, backup, clone, mongosh, candidate, publication, deletion, and rollback orchestration.**
- [ ] **Step 3: Generalize deploy/writer-start schema direction from music-only to exact domain-schema state while retaining music rollback compatibility.**
- [ ] **Step 4: Extend inventory output with per-kind counts and manifest compliance without exposing document values.**
- [ ] **Step 5: Run focused PS7/PS5 tests, marker-owned real Mongo tests, parser checks, and commit `feat: add guarded domain collection cutover`**.

#### Code Edit 7.1
- File: `ops/production/windows/prod.ps1`
- Lines: 2-73
- Action: replace

Current:
```powershell
[ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','mongo-inventory','music-runtime-rollback','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
[string]$Command = 'help',
[switch]$MusicSchemaCutover,
[switch]$ConfirmMusicRuntimeRollback
```

Proposed:
```powershell
[ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup',
    'mongo-inventory','mongo-consolidation-preview','mongo-consolidate',
    'mongo-consolidation-rollback','verify-startup','uninstall','auto-install','auto-deploy',
    'auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
[string]$Command = 'help',
[switch]$ConfirmDomainCollectionCutover,
[switch]$ConfirmDomainCollectionRollback
```

Verification:
- `Invoke-Pester .\ops\production\windows\tests\Production.Command.Tests.ps1,.\ops\production\windows\tests\Production.DomainCollections.Tests.ps1 -Output Detailed`

#### Code Edit 7.2
- File: `ops/production/windows/modules/Production.Operations.psm1`
- Lines: 447-538
- Action: replace

Current:
```powershell
function Get-ProductionMongoCollectionInventoryScript {
    @'
const target = db.getSiblingDB('christopherbell');
const collections = target.getCollectionInfos()
    .filter((info) => !info.name.startsWith('system.'));
print(JSON.stringify({ complete: true, database: target.getName(), collections }));
'@
}
```

Proposed:
```powershell
function Get-ProductionMongoCollectionInventoryScript {
    $manifest = Get-ProductionDomainCollectionManifestJson
    @"
const manifest = $manifest;
const target = db.getSiblingDB('christopherbell');
const inventory = DomainCollectionInventory.read(target, manifest);
print(JSON.stringify(inventory));
"@
}
```

Verification:
- `Invoke-Pester .\ops\production\windows\tests\Production.Operations.Tests.ps1 -Output Detailed`

#### Code Edit 7.3
- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 850-1013
- Action: replace

Current:
```powershell
function Invoke-ProductionDeploy {
    param([switch]$WhatIf, [switch]$MusicSchemaCutover, [switch]$Automatic)
    $direction = Read-ProductionMusicSchemaDirection -Config $config
    if ($MusicSchemaCutover) {
        Write-ProductionMusicSchemaDirection -State TARGET_CUTOVER_IN_PROGRESS
    }
}
```

Proposed:
```powershell
function Invoke-ProductionDeploy {
    param([switch]$WhatIf, [switch]$Automatic)
    $direction = Read-ProductionDomainSchemaDirection -Config $config
    Assert-ProductionDeployAllowedForDomainSchema `
        -Config $config -Direction $direction -Automatic:$Automatic
    Invoke-ProductionTargetSchemaDeployUnderHeldLock `
        -Config $config -Direction $direction -WhatIf:$WhatIf
}
```

Verification:
- `Invoke-Pester .\ops\production\windows\tests\Production.Deploy.Tests.ps1,.\ops\production\windows\tests\Production.WriterStart.Tests.ps1,.\ops\production\windows\tests\Production.AutoDeploy.Tests.ps1 -Output Detailed`

### Task 8 - Complete automated, restored-clone, runtime, review, PR, and CI gates

Sequence / dependencies:
- Runs after Tasks 1-7; no production mutation occurs in this task.

Implementation notes:
- Required skill: `chris-street-style` before any test/report code edits.
- Before-Edit Brief:
  - Behavior: prove the exact release and migration against isolated data and application ports before publication.
  - Invariants: production listener/database/services remain untouched; test Mongo roots/processes are marker-owned and removed.
  - Boundary/API: validation uses repository-native Gradle/Pester commands and existing candidate launcher.
  - Effects and failures: any failure blocks PR merge or production cutover; evidence records counts/statuses without secrets.
  - Tests and evidence: full Java/Pester, disposable Mongo, restored production clone, alternate-port HTTP, independent implementation review, and security diff scan.

- [ ] **Step 1: Run focused Java tests after every task, then full `.\gradlew.bat --no-daemon :website:test :website:bootJar` with private `GRADLE_USER_HOME`.**
- [ ] **Step 2: Run PS7 full Pester and required PS5.1 focused suites; parse every changed PowerShell file on both hosts and validate JS syntax.**
- [ ] **Step 3: Run the entire migration, interruption matrix, reverse path, drop path, and backup restore against a marker-owned disposable MongoDB.**
- [ ] **Step 4: Create a fresh backup through protected tooling, dry-restore it to a candidate database, migrate it, start the exact bootJar on a non-8080 port, and verify representative authenticated/unauthenticated routes.**
- [ ] **Step 5: Request independent implementation review and run a security diff scan; fix every validated blocker and repeat affected gates.**
- [ ] **Step 6: Commit final verification/docs, push branch, open PR, wait for all required CI/CodeQL checks, address failures, and merge only when green.**

#### Code Edit 8.1
- File: `docs/operations/mongodb-collection-catalog.md`
- Lines: 1-148
- Action: replace

Current:
```markdown
| Physical name | Logical name | Owner and mapping | Role | Cardinality and retention | Index contract | Sensitivity | Status |
```

Proposed:
```markdown
| Physical collection | Owning module | Kind | Legacy source | Schema version | Count | Index contract | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `accounts` | account | `account` | `accounts` | 1 | runtime inventory | manifest digest | target |
```

Verification:
- `.\gradlew.bat :website:test --tests dev.christopherbell.architecture.MongoCollectionCatalogTest --console=plain`

### Task 9 - Perform the guarded production maintenance cutover and immediate deletion

Sequence / dependencies:
- Runs only after Task 8 is merged to `main`, CI is green, the exact merge SHA is available, and the elevated PS7/PS5 ACL/native boundary gate succeeds.

Implementation notes:
- No code edits are permitted during the cutover; any required edit returns to Task 8 and repeats review/CI.
- Before-Edit Brief:
  - Behavior: publish the merged target schema, verify it live, and delete every exact superseded collection.
  - Invariants: one deployment lock, stopped writer during database mutation, suspended recovery, verified backup, exact release/manifest/marker, and literal allowlist.
  - Boundary/API: use only `prod.cmd`/`prod.ps1` protected commands from the merged release.
  - Effects and failures: pre-drop failure reverses renames; post-drop failure restores the verified backup while the writer remains stopped.
  - Tests and evidence: before/after inventory, backup SHA/dry restore, candidate smoke, live counts/checksums/indexes, HTTP status/body, service states, and absence proofs.

- [ ] **Step 1: Verify elevated PowerShell 7 and Windows PowerShell 5.1 ACL/native opt-in suites on disposable NTFS roots with zero residue.**
- [ ] **Step 2: Record current release, services, listener, 48-collection inventory, index count, per-source counts/checksums, and automatic-deploy state.**
- [ ] **Step 3: Run `.\prod.cmd mongo-consolidation-preview` and require the exact manifest, zero collisions, and zero unexpected sources/targets.**
- [ ] **Step 4: Run `.\prod.cmd mongo-consolidate -ConfirmDomainCollectionCutover` and retain its protected backup/restore/candidate/publication/deletion evidence.**
- [ ] **Step 5: Verify local liveness/readiness, authenticated failure boundary, public roots with status/body, exact active release, services, schema marker, and auto-deploy tool hashes.**
- [ ] **Step 6: Run `.\prod.cmd mongo-inventory`; require exactly 14 target collections, exact per-kind counts/checksums/indexes, and absence of every source/temp/legacy name.**
- [ ] **Step 7: Retain the verified backup and publish the production test report; do not remove backup evidence during closeout.**

### Task 10 - Close the spoke and Builder work

Sequence / dependencies:
- Runs after successful Task 9 production acceptance.

Implementation notes:
- No production code edit; save durable Markdown artifacts only.

- [ ] **Step 1: Save the local/production test report with exact request/response and collection evidence.**
- [ ] **Step 2: Ingest the spoke update, save the spoke review, and mark the implementation plan complete.**
- [ ] **Step 3: Save session memory, close the domain-consolidation work record, update hub indexes, and validate hub state.**
- [ ] **Step 4: Commit and push Builder `main`, then report commits, PR/merge, production release, 14-collection inventory, deleted collection count, and retained backup.**

## Code Changes

- Add shared envelope/ID/manifest/kind-scoped persistence infrastructure and tests.
- Remove legacy `@Document` mappings and direct Spring Data repository ownership.
- Add explicit adapters for every domain repository and manual query/update/delete path.
- Replace cbell-lib's physical Mongo ownership with lease and collector store ports.
- Add V015 target-schema startup gate, immutable JS manifest, migration engine, and real-Mongo tests.
- Add guarded PowerShell preview/cutover/rollback commands and generalize deploy/writer-start schema direction.
- Rewrite catalog/inventory output for 14 targets plus per-kind detail.

## Files and Modules

- `website/src/main/java/dev/christopherbell/configuration/mongo/domain/`
- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/`
- All current domain model/repository/manual Mongo store packages named in Tasks 3-5
- `cbell-lib/src/main/java/dev/christopherbell/libs/mongo/lease/`
- `ops/production/windows/scripts/`
- `ops/production/windows/modules/Production.DomainCollections.psm1`
- Existing deploy, operations, writer-start, auto-deploy, command, install, and tests
- `docs/operations/mongodb-collection-catalog.md`

## Unit Testing

- Envelope/ID/query/update codec unit tests, malformed data matrices, partial index definitions, optimistic-lock contention, all repository adapter contracts, manifest uniqueness, architecture rules, migration fixtures, interruption/recovery state machine, and Pester ordering/fail-closed tests.
- Every implementation task starts with a focused failing test and ends with its focused suite green before commit.

## Local Testing

```powershell
$env:GRADLE_USER_HOME = 'A:\Projects\christopherbell.dev-worktrees\domain-collection-consolidation\.gradle-user-home'
.\gradlew.bat --no-daemon :website:test :website:bootJar --console=plain
Invoke-Pester .\ops\production\windows\tests -Output Detailed
```

- Repeat required Pester subsets in Windows PowerShell 5.1 with the repository's private Pester 5.9 module path.
- Use only marker-owned disposable MongoDB ports and roots; verify PID/start time/dbPath/bind/port before each script and prove cleanup afterward.
- Start the candidate bootJar on a non-8080 port against the migrated restored clone and record URL, input, response status, and response body.

## Validation

- Full Gradle tests and bootJar succeed.
- Full PS7 and approved PS5.1 Pester gates succeed; all changed scripts parse on both hosts.
- Disposable and restored-clone migrations prove all kinds, BSON types, checksums, indexes, interruptions, reverse, deletion, and restore.
- Independent implementation review and security diff scan report no unresolved blockers.
- PR CI/CodeQL succeeds and merge SHA equals deployed SHA.
- Production ends healthy with exactly 14 target collections and zero superseded/temp/legacy collections.

## Rollback or Recovery

- Before publication: delete only marker-owned temporary targets and continue old release/schema.
- During ordered rename: use ledger `reverse-next` until every old name is restored, then start the exact old release.
- After live publication but before deletion: stop target writer, reverse the ledger, and start old release.
- After deletion: keep writer stopped and recovery suspended, restore the exact checksummed backup, verify counts/checksums/indexes, then start old release.
- Any uncertain marker, lock, release, process, database, collection, checksum, or backup identity leaves the writer stopped and requires manual investigation.

## Risks

- Shared-collection query leakage: mitigated by one boundary and source architecture tests forbidding bypasses.
- Identifier/type loss: mitigated by embedded original BSON ID and canonical Extended JSON real-Mongo tests.
- Index semantic drift: mitigated by exact manifest comparison of keys/order/unique/sparse/partial/TTL/collation.
- Multi-rename interruption: mitigated by CAS ledger, one-operation progress, exact resume/reverse, and writer-start gate.
- Post-deletion rollback cost: mitigated by mandatory checksummed backup and dry restore before mutation.
- Maintenance duration: mitigated by candidate-clone rehearsal and measuring stage/publish/delete time before live cutover.
- Production host ACL/elevation constraints: elevated disposable NTFS and protected command gates are mandatory before cutover; ACLs are never weakened.

## Completion Criteria

1. The merged/deployed application has no runtime mapping or unscoped access to a superseded collection.
2. All pre-cutover documents exist exactly once under the correct target/kind with matching canonical checksums.
3. Production has exactly the 14 approved physical collections and their exact manifest indexes.
4. Every superseded and temporary collection has been dropped by the guarded allowlist operation.
5. Local/public runtime checks, services, schema marker, release SHA, and automatic deployment are healthy.
6. The verified backup and restore evidence remain retained.
7. PR, CI, test report, reviews, Builder work closure, and session memory are complete and pushed.
