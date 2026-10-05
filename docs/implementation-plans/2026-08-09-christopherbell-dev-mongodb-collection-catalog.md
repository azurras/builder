# christopherbell.dev MongoDB Collection Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an enforced, domain-oriented catalog for every website MongoDB collection and a read-only production command that compares live collection metadata without reading documents or authorizing cleanup.

**Architecture:** Keep all active physical collections unchanged. A Java architecture test discovers Spring Data `@Document` mappings without starting Spring or connecting to MongoDB and compares them with a structured Markdown catalog plus an explicit list of current manual `MongoTemplate` references. Native Windows operations use the already configured `mongosh` executable to return allowlisted collection, stats, and index metadata from loopback; Pester proves that the command is metadata-only, fails closed, and is wired through the existing production CLI.

**Tech Stack:** Java 25, Spring Data MongoDB mapping metadata, JUnit 5, AssertJ, PowerShell 7 and Windows PowerShell 5.1, Pester 5.9.0, MongoDB 8.3 `mongosh`, Gradle Wrapper.

## Global Constraints

- Preserve the single native Windows MongoDB service on `127.0.0.1:27017`, the `christopherbell` database, and the existing `ChristopherBellDev` service dependency.
- Do not merge, rename, drop, compact, repair, rewrite, or sample any MongoDB collection or document.
- Inventory output is limited to collection names/types/allowlisted options, counts, sizes, and index definitions; it must never contain document bodies, credentials, or secret-bearing command lines.
- A missing or malformed source or live inventory fails closed and cannot produce an orphan conclusion.
- A live-only collection is an unreviewed extra, not removal authority; cleanup requires a separate approved backup-gated workflow.
- Preserve all current collection names, mappings, indexes, document shapes, retention rules, and application behavior.
- Do not add an HTTP endpoint, Mission Control surface, or public/admin UI for the inventory.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; implementation must use an isolated worktree from refreshed `origin/main`.
- Use a private `GRADLE_USER_HOME`; validate a packaged candidate on a non-8080 port before any production deployment.
- Invoke `chris-street-style` before every code edit and use test-driven development for behavior changes.

---

## Document Status

complete

## Objective

Implement the approved specification at `docs/specs/2026-08-09-christopherbell-dev-mongodb-collection-catalog.md` as one cohesive website delivery. The resulting repository must explain every current collection boundary, reject undocumented mappings, provide a bounded metadata-only live inventory, and leave production data untouched.

## Goals

1. Catalog all 51 current physical collection names represented by 52 `@Document` mappings at spoke commit `2f025762`.
2. Record owner, mapping/manual owner, role, cardinality/retention, index contract, sensitivity, logical name, and status for every collection.
3. Detect a new undocumented `@Document` mapping or duplicate/invalid catalog entry in JUnit.
4. Record current manual `MongoTemplate` collection references explicitly without centralizing production collection names across modules.
5. Add `prod.cmd mongo-inventory`, backed by configured `mongosh`, with loopback-only and metadata-only behavior.
6. Reject malformed, incomplete, wrong-database, duplicate-name, or unsorted inventory results.
7. Document exact operator usage and the boundary between observation and separately approved cleanup.
8. Verify focused Java/Pester tests, full repository checks, disposable-Mongo behavior, alternate-port application health, CI/CodeQL, and post-deploy metadata-only production behavior.

## Inputs

- Approved Builder spec: `docs/specs/2026-08-09-christopherbell-dev-mongodb-collection-catalog.md`.
- Spoke remote: `https://github.com/azurras/christopherbell.dev.git`.
- Inspected base: refreshed `origin/main` at `2f025762e248cab5befe0fb699e0560f57006572`.
- Production topology: native MongoDB, `ChristopherBellDev`, and `cloudflared` Windows services; production MongoDB is not a Docker container.
- Existing operations seams: `Read-ProductionConfig`, configured `mongoShellExe`, `Invoke-CheckedProcess`, `Production.Operations.psm1`, `prod.ps1`, Pester operations tests, and native Windows runbook.
- Existing architecture seam: `website/src/test/java/dev/christopherbell/architecture/` and JUnit/AssertJ.

## Branch

- Base: refreshed `origin/main` at execution time.
- Branch: `codex/mongodb-collection-catalog`.
- Worktree: a clean sibling worktree created with `superpowers:using-git-worktrees`; never implement in `A:\Projects\christopherbell.dev`.

## Non-Goals

- No collection consolidation, rename, deletion, archival, TTL change, index change, or schema migration.
- No live document inspection, aggregation, sampling, export, or profiling.
- No change to application controllers, services, repositories, MongoDB mappings, or domain behavior.
- No MongoDB authentication redesign or network exposure change.
- No generic runtime schema registry or global production collection-name dependency.
- No automatic orphan classification or cleanup action.

## Assumptions

- The configured production `mongoShellExe` remains installed and validated by `Read-ProductionConfig`.
- The production MongoDB URI remains the fixed IPv4 loopback endpoint already used by backup, restore validation, and candidate cleanup tooling.
- All current manual collection references target collections that also have an explicit Spring Data mapping; the test records those references as additional owners rather than additional physical names.
- `ClassPathScanningCandidateComponentProvider` with an `AnnotationTypeFilter(Document.class)` can discover the current annotated persistence types from test runtime classpath without application startup.
- `mongosh` supports `getCollectionInfos`, `collStats`, `getIndexes`, and JSON serialization on MongoDB 8.3.
- Live inventory may reveal system or historical collections not present in source; those remain observations only.

## Open Questions

None. The user approved the written specification on 2026-08-09.

## Task Breakdown

### Task 1 - Add the collection catalog and architecture enforcement

Sequence / dependencies:
- First implementation task after creating the isolated worktree.
- Produces the catalog contract consumed by documentation and production comparison in later tasks.

Interfaces:
- Consumes: Spring Data `@Document` annotations on the test runtime classpath and `docs/operations/mongodb-collection-catalog.md`.
- Produces: `MongoCollectionCatalogTest.catalogEntriesAreCompleteAndValid()` and `MongoCollectionCatalogTest.everyMappedAndManualCollectionIsCataloged()`.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: A focused JUnit test reports every missing, extra, duplicate, invalid, or undocumented current collection entry without starting the application or connecting to MongoDB.
  - Invariants: Active physical names remain unchanged; each catalog row has exactly one owner/role/status; the two vehicle import-state document types intentionally resolve to one physical name; manual references add ownership evidence but cannot add an undocumented name.
  - Boundary/API: The boundary is the test-only catalog parser and Spring classpath scanner; production modules remain independent and do not import a global catalog class.
  - Effects and failures: The test reads one repository Markdown file and class metadata only. Missing files, unloaded classes, malformed rows, blank fields, invalid enums, duplicate names, or set differences fail the test with actionable diagnostics.
  - Tests and evidence: RED is `MongoCollectionCatalogTest` failing because the catalog file does not exist. GREEN is both focused tests passing after the complete catalog is added, followed by the architecture test suite.

- [x] **Step 1: Create the failing catalog test.**

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java`
- Lines: 1-149
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Pattern;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider;
import org.springframework.core.annotation.AnnotatedElementUtils;
import org.springframework.core.type.filter.AnnotationTypeFilter;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.util.ClassUtils;

class MongoCollectionCatalogTest {
  private static final Path CATALOG =
      repositoryRoot().resolve("docs/operations/mongodb-collection-catalog.md");
  private static final Pattern PHYSICAL_NAME = Pattern.compile("[a-z][a-z0-9_]*");
  private static final Set<String> VALID_ROLES = Set.of(
      "audit", "cache", "edge", "entity", "event-history", "job", "lease",
      "preference", "singleton-state");
  private static final Set<String> VALID_SENSITIVITY = Set.of(
      "audit", "confidential", "internal", "public-reference", "security", "user");
  private static final Set<String> VALID_STATUSES = Set.of("active", "legacy-named");
  private static final Set<String> MANUAL_COLLECTION_REFERENCES = Set.of(
      "account_follows",
      "account_trust_relationships",
      "accounts",
      "browser_sessions",
      "conversation_archive_states",
      "federation_delivery_jobs",
      "hidden_post_threads",
      "messages",
      "notification_delivery_guards",
      "notification_preferences",
      "notification_rate_limits",
      "notifications",
      "post_likes",
      "posts",
      "shared_folder_media_jobs",
      "shared_folder_upload_sessions",
      "whatsforlunch",
      "whatsforlunch_favorites",
      "whatsforlunch_preferences",
      "whatsforlunch_ratings",
      "whatsforlunch_sessions");

  @Test
  void catalogEntriesAreCompleteAndValid() throws IOException {
    var entries = readCatalog();

    assertThat(entries).hasSize(51);
    assertThat(entries).extracting(CatalogEntry::physicalName).doesNotHaveDuplicates();
    assertThat(entries).allSatisfy(entry -> {
      assertThat(entry.physicalName()).matches(PHYSICAL_NAME);
      assertThat(entry.logicalName()).isNotBlank();
      assertThat(entry.ownerAndMapping()).isNotBlank();
      assertThat(entry.role()).isIn(VALID_ROLES);
      assertThat(entry.cardinalityAndRetention()).isNotBlank();
      assertThat(entry.indexContract()).isNotBlank();
      assertThat(entry.sensitivity()).isIn(VALID_SENSITIVITY);
      assertThat(entry.status()).isIn(VALID_STATUSES);
    });
  }

  @Test
  void everyMappedAndManualCollectionIsCataloged() throws IOException {
    var expected = new TreeSet<>(mappedCollectionNames());
    expected.addAll(MANUAL_COLLECTION_REFERENCES);

    assertThat(readCatalog())
        .extracting(CatalogEntry::physicalName)
        .containsExactlyInAnyOrderElementsOf(expected);
  }

  private static Set<String> mappedCollectionNames() {
    var scanner = new ClassPathScanningCandidateComponentProvider(false);
    scanner.addIncludeFilter(new AnnotationTypeFilter(Document.class));
    var classLoader = MongoCollectionCatalogTest.class.getClassLoader();
    var names = new TreeSet<String>();
    for (var candidate : scanner.findCandidateComponents("dev.christopherbell")) {
      var className = candidate.getBeanClassName();
      assertThat(className).isNotBlank();
      var documentType = ClassUtils.resolveClassName(className, classLoader);
      var document = AnnotatedElementUtils.findMergedAnnotation(documentType, Document.class);
      assertThat(document).as("@Document on %s", className).isNotNull();
      assertThat(document.collection()).as("explicit collection for %s", className).isNotBlank();
      names.add(document.collection());
    }
    return names;
  }

  private static List<CatalogEntry> readCatalog() throws IOException {
    try (var lines = Files.lines(CATALOG)) {
      return lines
          .filter(line -> line.startsWith("| `"))
          .map(MongoCollectionCatalogTest::parseCatalogRow)
          .toList();
    }
  }

  private static CatalogEntry parseCatalogRow(String line) {
    var cells = Arrays.stream(line.substring(1, line.length() - 1).split("\\|", -1))
        .map(String::trim)
        .toList();
    assertThat(cells).as("catalog row: %s", line).hasSize(8);
    return new CatalogEntry(
        unquoteCode(cells.get(0)),
        cells.get(1),
        cells.get(2),
        cells.get(3),
        cells.get(4),
        cells.get(5),
        cells.get(6),
        cells.get(7));
  }

  private static String unquoteCode(String value) {
    assertThat(value).startsWith("`").endsWith("`");
    return value.substring(1, value.length() - 1);
  }

  private static Path repositoryRoot() {
    var current = Path.of("").toAbsolutePath().normalize();
    if (Files.isDirectory(current.resolve(".github"))) {
      return current;
    }
    var parent = current.getParent();
    if (parent != null && Files.isDirectory(parent.resolve(".github"))) {
      return parent;
    }
    throw new IllegalStateException("Cannot locate repository root from " + current);
  }

  private record CatalogEntry(
      String physicalName,
      String logicalName,
      String ownerAndMapping,
      String role,
      String cardinalityAndRetention,
      String indexContract,
      String sensitivity,
      String status) {}
}
```

Verification:
- Run `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.architecture.MongoCollectionCatalogTest`.
- Expected RED: test fails because `docs/operations/mongodb-collection-catalog.md` does not exist.

- [x] **Step 2: Run the focused test and record the expected missing-catalog failure.**
- [x] **Step 3: Add the complete collection catalog.**

#### Code Edit 1.2
- File: `docs/operations/mongodb-collection-catalog.md`
- Lines: 1-84
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```markdown
# MongoDB Collection Catalog

This catalog is the source of truth for physical collection ownership in the
`christopherbell` database. Logical groups do not merge storage. A
`legacy-named` entry remains active under its physical name until a separately
approved migration proves compatibility and rollback.

The catalog describes source expectations. Use `prod.cmd mongo-inventory` for
metadata-only live comparison. A live-only name is an unreviewed extra, not
permission to drop it. Never infer disposability from an empty count.

| Physical name | Logical name | Owner and mapping | Role | Cardinality and retention | Index contract | Sensitivity | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `application_leases` | Application leases | platform and `MongoLeaseDocument` | lease | Bounded by active lease keys; expired leases are reclaimable | `_id` lease key and V001 expiration index | internal | active |
| `scheduled_collector_runs` | Scheduled collector runs | platform and `ScheduledCollectorRun` | event-history | One redacted record per collector attempt; durable | V003 collector and start-time query indexes | internal | active |
| `account_deletion_jobs` | Account deletion jobs | account and `AccountDeletionJob` | job | One pseudonymous retry checkpoint per deletion | `_id` pseudonym | security | active |
| `account_follows` | Account follows | account and `AccountFollow`; manual social queries | edge | Account-owned social edges; deleted with either account | Unique follower/followed pair plus directional lookups | user | active |
| `accounts` | Accounts | account and `Account`; manual session/deletion/federation access | entity | One durable document per account | Unique username and email identity indexes plus lookup indexes | security | active |
| `account_trust_relationships` | Account trust relationships | account and `AccountTrustRelationship`; manual deletion/query access | edge | Account-owned trust edges | Unique owner/target pair plus owner and target indexes | user | active |
| `command_center_pending_actions` | Pending command-center actions | admin and `PendingActionDocument` | singleton-state | Fixed machine-power action key; cleared after execution/cancel | `_id` fixed key | security | active |
| `admin_activity` | Administrative activity | admin and `AdminActivity` | audit | Append-only bounded/redacted audit history | Created, action, target, and actor descending indexes | audit | active |
| `canes_box_price_snapshots` | Canes price snapshots | canesboxtracker and `CanesBoxPriceSnapshot` | event-history | One durable weekly market snapshot | `_id` weekly identity | public-reference | active |
| `application_migrations` | Application migrations | platform and `MigrationRecord` | audit | One durable status/checksum record per migration ID | `_id` migration ID and V001 status protection | internal | active |
| `browser_sessions` | Browser sessions | account security and `BrowserSession`; manual auth/deletion access | entity | Per-browser session; absolute-expiry TTL | Account lookup and absolute-expiry TTL indexes | security | active |
| `federation_delivery_jobs` | Federation delivery jobs | federation and `FederationDeliveryJob`; manual outbox access | job | Bounded retry metadata; no payloads or keys | V007 state, retry, claim, post, and peer indexes | internal | active |
| `federation_scan_state` | Federation scan checkpoint | federation and `FederationScanState` | singleton-state | One durable outbound reconciliation cursor | `_id` fixed cursor key | internal | active |
| `location_zip_coordinates` | ZIP coordinates | location and `ZipCoordinate` | entity | One reference row per supported ZIP | ZIP identity and geographic lookup indexes | public-reference | active |
| `zip_coordinate_import_state` | ZIP import state | location and `ZipCoordinateImportState` | singleton-state | One durable dataset checksum/outcome | `_id` importer key | internal | active |
| `conversation_archive_states` | Conversation archive states | message and `ConversationArchiveState`; manual deletion/query access | preference | Per-account conversation archive edge | Unique account/conversation pair and account query index | user | active |
| `messages` | Messages | message and `Message`; manual conversation/deletion aggregation | entity | Durable direct-message history | Conversation, participant, and unread indexes | confidential | active |
| `music_tracks` | Music tracks | music and `MusicTrack` | entity | One catalog row per observed track revision | Unique path plus artist, album, and genre indexes | user | active |
| `music_playlists` | Music playlists | music and `MusicPlaylist` | entity | One durable document per playlist | Unique normalized name | user | active |
| `music_metadata_edits` | Music metadata edits | music and `MusicMetadataEdit` | audit | Per-track edit history with application-managed expiry | Track and expiry indexes | audit | active |
| `music_queue_state` | Music queue state | music and `MusicQueueState` | singleton-state | One global optimistic queue document | `_id` fixed key and optimistic version | user | active |
| `music_radio_history` | Music radio history | music and `MusicRadioHistoryEvent` | event-history | Append-only playback history | Station sequence and occurrence-time indexes | user | active |
| `music_radio_state` | Music radio state | music and `MusicRadioState` | singleton-state | One global optimistic station document | `_id` fixed key and optimistic version | user | active |
| `music_access_attempts` | Music access attempts | music and `MusicAccessAttempt` | audit | Short-lived bounded security attempts | Absolute-expiry TTL | security | active |
| `notification_delivery_guards` | Notification delivery guards | notification and `NotificationDeliveryGuard`; manual deletion access | lease | Short-lived unique fanout claims | `_id` dedupe key and absolute-expiry TTL | internal | active |
| `notification_rate_limits` | Notification rate limits | notification and `NotificationRateLimit`; manual deletion access | singleton-state | Short-lived fixed-window counters | `_id` scope key and absolute-expiry TTL | internal | active |
| `notifications` | Notifications | notification and `Notification`; manual inbox/deletion access | entity | Per-account notification history | Account/time and account/read indexes | user | active |
| `notification_preferences` | Notification preferences | notification and `NotificationPreference`; manual deletion access | preference | One document per account | Unique account ID | user | active |
| `hidden_post_threads` | Hidden post threads | post and `HiddenPostThread`; manual deletion access | edge | Per-account hidden-thread edges | Unique account/root pair plus directional indexes | user | active |
| `post_likes` | Post likes | post and `PostLike`; manual engagement/deletion access | edge | Per-account post-like edges | Unique post/account pair and query indexes | user | active |
| `posts` | Posts | post and `Post`; manual feed/discovery/federation access | entity | Durable social content with application-managed expiration | Account, creation, thread, parent, and expiration indexes | user | active |
| `post_link_preview_cache` | Post link-preview cache | post and `PostLinkPreviewCacheEntry` | cache | One expiring result per normalized URL; application cleanup | URL `_id` and V003 expiry index | internal | active |
| `post_reports` | Post reports | report and `PostReport` | entity | Durable moderation queue records | Queue/time indexes and sparse unique open-dedupe key | confidential | active |
| `shared_folder_audit` | Shared-folder audit | sharedfolder and `SharedFolderAuditEvent` | audit | Redacted audit events with absolute-expiry TTL | Account, action, outcome, path, occurrence, and TTL indexes | audit | active |
| `shared_folder_maintenance_leases` | Shared-folder maintenance lease | sharedfolder and `SharedFolderMaintenanceLeaseDocument` | lease | One fixed-key process coordination lease | `_id` fixed key and expiry field | internal | active |
| `shared_folder_media_jobs` | Shared-folder media jobs | sharedfolder and `MediaJob`; manual V012 access | job | Bounded job/cache lifecycle with terminal TTL | Owner, cache, status, LRU, claim, and terminal TTL indexes | confidential | active |
| `shared_folder_radio` | Shared-folder radio state | sharedfolder and `SharedFolderRadioDocument` | singleton-state | One optimistic station document with bounded duration knowledge | `_id` fixed key and optimistic version | confidential | active |
| `shared_folder_recycle_items` | Shared-folder recycle items | sharedfolder and `SharedFolderRecycleItem` | entity | Private recycle metadata through restore/expiry workflow | State, deletion, recovery, expiry, and retry indexes | confidential | active |
| `shared_folder_mutation_recoveries` | Shared-folder mutation recoveries | sharedfolder and `SharedFolderMutationRecovery` | job | Retryable mutation recovery journal | Owner and update-time indexes | confidential | active |
| `shared_folder_upload_sessions` | Shared-folder upload sessions | sharedfolder and `SharedFolderUploadSession`; manual V012 access | job | Bounded resumable uploads with terminal TTL | Owner/state, expiry, and terminal TTL indexes | confidential | active |
| `vehicles` | Vehicles | vehicle and `Vehicle` | entity | One durable vehicle document per VIN | Unique VIN | user | active |
| `vehicle_vin_decode_cache` | VIN decode cache | vehicle and `VehicleVinDecodeCache` | cache | One expiring provider response per VIN | VIN `_id` and V003 expiry index | public-reference | active |
| `vehicle_import_state` | Vehicle import state | vehicle and both VIN import-state mappings | singleton-state | One collision-proof key per import provider | Provider-specific `_id` keys | internal | active |
| `restaurant_import_previews` | Restaurant import previews | whatsforlunch and `RestaurantImportPreviewDocument` | lease | Short-lived reviewed-import authorization | V002 actor, expiry, and consumed-state indexes | security | active |
| `whatsforlunch_daily_picks` | Daily lunch picks | whatsforlunch and `DailyLunchPicks` | cache | One durable generated result per lunch date | Date-derived `_id` | user | active |
| `whatsforlunch` | Restaurants | whatsforlunch and `Restaurant`; manual inventory/dedupe access | entity | Durable restaurant catalog | Normalized name, source, location, and search indexes | public-reference | legacy-named |
| `whatsforlunch_favorites` | Restaurant favorites | whatsforlunch and `RestaurantFavorite`; manual deletion access | edge | Per-account favorite edges | Unique restaurant/account pair plus directional indexes | user | active |
| `restaurant_import_state` | Restaurant import state | whatsforlunch and `RestaurantImportState` | singleton-state | One durable scheduler state per source | Source `_id` | internal | active |
| `whatsforlunch_ratings` | Restaurant votes | whatsforlunch and `RestaurantVote`; manual query/deletion access | edge | Per-account thumbs vote per restaurant | Unique restaurant/account pair plus account index | user | legacy-named |
| `whatsforlunch_preferences` | Lunch preferences | whatsforlunch and `WhatsForLunchPreference`; manual deletion access | preference | One document per account | Account `_id` | user | active |
| `whatsforlunch_sessions` | Lunch sessions | whatsforlunch and `WhatsForLunchSession`; manual mutation/deletion access | entity | Collaborative sessions with terminal absolute-expiry TTL | Short code, creator, state, archive, and TTL indexes | user | active |

Naming Rules
------------

- Use lowercase `snake_case`.
- Prefix ambiguous names with their owning domain.
- Use plural nouns for entities, edges, jobs, events, histories, and audits.
- Use `_state` for singleton/checkpoint documents and lifecycle suffixes such as
  `_jobs`, `_history`, `_audit`, `_cache`, `_guards`, and `_leases` when applicable.
- Keep active legacy physical names until a separate migration is approved.
- Document every intentionally shared mapping and its collision-proof ID scheme.

Live Comparison Rules
---------------------

`prod.cmd mongo-inventory` returns metadata only. Compare its physical names with
this table. Source-only names may be features that have never persisted data.
Live-only names remain unreviewed extras until current source, migrations,
operations scripts, history, count, size, options, and indexes establish their
ownership. No result from this command authorizes deletion.
```

Verification:
- Re-run the focused catalog test; expected GREEN: 2 tests pass.
- Run `gradlew.bat --no-daemon :website:test --tests dev.christopherbell.architecture.*`.
- Run `git diff --check` and the repository Java formatter/check task used by `:website:check`.

- [x] **Step 4: Commit Task 1.**

```powershell
git add docs/operations/mongodb-collection-catalog.md website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java
git commit -m "Document MongoDB collection ownership"
```

### Task 2 - Add the metadata-only native Windows inventory command

Sequence / dependencies:
- Runs after Task 1 so live output has a source catalog to compare against.
- Produces the operator command documented in Task 3.

Interfaces:
- Consumes: `Read-ProductionConfig()`, `Invoke-CheckedProcess()`, and configured `mongoShellExe`.
- Produces: `Get-ProductionMongoCollectionInventoryScript()`, `ConvertFrom-ProductionMongoCollectionInventory(string)`, public `Get-ProductionMongoCollectionInventory()`, and `prod.cmd mongo-inventory`.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: An operator can run `prod.cmd mongo-inventory` and receive a complete, sorted object containing only allowlisted metadata for non-system collections in `christopherbell`.
  - Invariants: URI and database are fixed to IPv4 loopback and `christopherbell`; the script performs no document reads or mutations; any child-process, JSON, database, completeness, duplicate-name, or ordering failure stops with no partial inventory.
  - Boundary/API: The public PowerShell function owns production configuration and process execution. A private script builder owns the audited JavaScript, and a private converter validates untrusted `mongosh` JSON before returning trusted PowerShell objects.
  - Effects and failures: The only external effect is read-only `mongosh` metadata I/O. Infrastructure failures preserve the existing checked-process exit behavior; malformed output becomes `InvalidDataException` with the parse cause; partial/wrong-database output becomes a specific validation failure.
  - Tests and evidence: RED is new Pester tests failing because the functions and CLI command do not exist. GREEN is focused Pester passing, followed by an integration run against disposable MongoDB and both supported PowerShell hosts.

- [x] **Step 1: Add failing Pester coverage for script safety, invocation, and fail-closed parsing.**

#### Code Edit 2.1
- File: `ops/production/windows/tests/Production.Operations.Tests.ps1`
- Lines: before 397
- Action: add

Current:
```powershell
        It 'uses attached IPv4 URI and archive arguments for native backups' {
```

Proposed:
```powershell
        It 'builds a metadata-only MongoDB inventory script' {
            $script = Get-ProductionMongoCollectionInventoryScript

            $script | Should -Match 'getCollectionInfos'
            $script | Should -Match 'collStats'
            $script | Should -Match 'getIndexes'
            $script | Should -Not -Match '\.find\s*\('
            $script | Should -Not -Match '\.aggregate\s*\('
            $script | Should -Not -Match '\.(drop|renameCollection|compact|repairDatabase)\s*\('
            $script | Should -Not -Match '\$(out|merge)'
        }

        It 'invokes mongosh against only the fixed loopback production database' {
            Mock Read-ProductionConfig {
                [pscustomobject]@{
                    mongoShellExe = 'C:\tools\mongosh.exe'
                    repositoryPath = 'C:\repo'
                }
            }
            Mock Invoke-CheckedProcess {
                '{"complete":true,"database":"christopherbell","generatedAt":"2026-08-09T12:00:00.000Z","collections":[]}'
            }

            $inventory = Get-ProductionMongoCollectionInventory

            $inventory.complete | Should -BeTrue
            $inventory.database | Should -Be 'christopherbell'
            Should -Invoke Invoke-CheckedProcess -Times 1 -Exactly -ParameterFilter {
                $FilePath -eq 'C:\tools\mongosh.exe' -and
                $WorkingDirectory -eq 'C:\repo' -and
                $ArgumentList.Count -eq 4 -and
                $ArgumentList[0] -eq '--quiet' -and
                $ArgumentList[1] -eq 'mongodb://127.0.0.1:27017/admin' -and
                $ArgumentList[2] -eq '--eval'
            }
        }

        It 'rejects incomplete MongoDB inventory output' {
            $json = '{"complete":false,"database":"christopherbell","generatedAt":"2026-08-09T12:00:00.000Z","collections":[]}'

            { ConvertFrom-ProductionMongoCollectionInventory -Json $json } |
                Should -Throw '*complete*'
        }

        It 'rejects malformed, wrong-database, duplicate, and unsorted inventory output' {
            { ConvertFrom-ProductionMongoCollectionInventory -Json 'not-json' } |
                Should -Throw '*valid JSON*'
            $wrongDatabase = '{"complete":true,"database":"admin","generatedAt":"2026-08-09T12:00:00.000Z","collections":[]}'
            { ConvertFrom-ProductionMongoCollectionInventory -Json $wrongDatabase } |
                Should -Throw '*christopherbell*'
            $missingCollections = '{"complete":true,"database":"christopherbell","generatedAt":"2026-08-09T12:00:00.000Z"}'
            { ConvertFrom-ProductionMongoCollectionInventory -Json $missingCollections } |
                Should -Throw '*collections*'
            $systemCollection = '{"complete":true,"database":"christopherbell","generatedAt":"2026-08-09T12:00:00.000Z","collections":[{"name":"system.profile","type":"collection","options":{},"count":0,"sizeBytes":0,"storageSizeBytes":0,"totalIndexSizeBytes":0,"indexes":[]}]}'
            { ConvertFrom-ProductionMongoCollectionInventory -Json $systemCollection } |
                Should -Throw '*system*'
            $duplicates = '{"complete":true,"database":"christopherbell","generatedAt":"2026-08-09T12:00:00.000Z","collections":[{"name":"accounts","type":"collection","options":{},"count":1,"sizeBytes":1,"storageSizeBytes":1,"totalIndexSizeBytes":1,"indexes":[]},{"name":"accounts","type":"collection","options":{},"count":1,"sizeBytes":1,"storageSizeBytes":1,"totalIndexSizeBytes":1,"indexes":[]}]}'
            { ConvertFrom-ProductionMongoCollectionInventory -Json $duplicates } |
                Should -Throw '*unique*'
            $unsorted = '{"complete":true,"database":"christopherbell","generatedAt":"2026-08-09T12:00:00.000Z","collections":[{"name":"posts","type":"collection","options":{},"count":1,"sizeBytes":1,"storageSizeBytes":1,"totalIndexSizeBytes":1,"indexes":[]},{"name":"accounts","type":"collection","options":{},"count":1,"sizeBytes":1,"storageSizeBytes":1,"totalIndexSizeBytes":1,"indexes":[]}]}'
            { ConvertFrom-ProductionMongoCollectionInventory -Json $unsorted } |
                Should -Throw '*sorted*'
        }

        It 'uses attached IPv4 URI and archive arguments for native backups' {
```

Verification:
- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Operations.Tests.ps1 -Output Detailed"`.
- Expected RED: failures report that `Get-ProductionMongoCollectionInventoryScript`, `ConvertFrom-ProductionMongoCollectionInventory`, and `Get-ProductionMongoCollectionInventory` do not exist.

#### Code Edit 2.2
- File: `ops/production/windows/tests/Production.Command.Tests.ps1`
- Lines: before 102
- Action: add

Current:
```powershell
    It 'rejects unknown commands' {
```

Proposed:
```powershell
    It 'exposes MongoDB inventory as one JSON-producing command' {
        $root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
        $script = Get-Content (Join-Path $root 'ops\production\windows\prod.ps1') -Raw
        $makefile = Get-Content (Join-Path $root 'Makefile') -Raw
        $help = & pwsh.exe -NoLogo -NoProfile -File (
            Join-Path $root 'ops\production\windows\prod.ps1') help

        ($help -join "`n") | Should -Match '\bmongo-inventory\b'
        $script | Should -Match "'mongo-inventory'\s*=\s*\{"
        $script | Should -Match 'Get-ProductionMongoCollectionInventory\s*\|\s*ConvertTo-Json -Depth 100'
        $makefile | Should -Match '\bprod-mongo-inventory\b'
    }

    It 'rejects unknown commands' {
```

Verification:
- Run `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Command.Tests.ps1 -Output Detailed"`.
- Expected RED: the new test cannot find `mongo-inventory` in the command, help, or Make surfaces.

- [x] **Step 2: Run focused Pester and record the expected missing-function failures.**
- [x] **Step 3: Implement the audited script, validation boundary, and public operation.**

#### Code Edit 2.3
- File: `ops/production/windows/modules/Production.Operations.psm1`
- Lines: before 163
- Action: add

Current:
```powershell
function Test-ProductionStartup {
```

Proposed:
```powershell
function Get-ProductionMongoCollectionInventoryScript {
    @'
const target = db.getSiblingDB('christopherbell');
const has = (value, key) => Object.prototype.hasOwnProperty.call(value || {}, key);
const numberOrNull = (value) => typeof value === 'number' ? value : null;
const safeOptions = (options) => {
  const result = {};
  for (const key of ['capped', 'size', 'max', 'validator', 'validationLevel',
                     'validationAction', 'collation']) {
    if (has(options, key)) {
      result[key] = options[key];
    }
  }
  return result;
};
const safeIndex = (index) => ({
  name: index.name,
  key: index.key,
  unique: index.unique === true,
  sparse: index.sparse === true,
  expireAfterSeconds: has(index, 'expireAfterSeconds') ? index.expireAfterSeconds : null,
  partialFilterExpression: has(index, 'partialFilterExpression')
      ? index.partialFilterExpression
      : null
});
const collections = target.getCollectionInfos()
    .filter((info) => !info.name.startsWith('system.'))
    .sort((left, right) => left.name === right.name ? 0 : left.name < right.name ? -1 : 1)
    .map((info) => {
      const stats = target.runCommand({ collStats: info.name });
      if (stats.ok !== 1) {
        throw new Error(`collStats failed for ${info.name}`);
      }
      const indexes = info.type === 'view'
          ? []
          : target.getCollection(info.name).getIndexes()
              .map(safeIndex)
              .sort((left, right) => left.name === right.name ? 0 : left.name < right.name ? -1 : 1);
      return {
        name: info.name,
        type: info.type,
        options: safeOptions(info.options),
        count: numberOrNull(stats.count),
        sizeBytes: numberOrNull(stats.size),
        storageSizeBytes: numberOrNull(stats.storageSize),
        totalIndexSizeBytes: numberOrNull(stats.totalIndexSize),
        indexes
      };
    });
print(JSON.stringify({
  complete: true,
  database: target.getName(),
  generatedAt: new Date().toISOString(),
  collections
}));
'@
}

function ConvertFrom-ProductionMongoCollectionInventory {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$Json)

    try {
        $inventory = $Json | ConvertFrom-Json -ErrorAction Stop
    } catch {
        throw [IO.InvalidDataException]::new(
            'MongoDB collection inventory did not return valid JSON.',
            $_.Exception)
    }
    if ($inventory.PSObject.Properties.Name -notcontains 'complete' -or
        $inventory.complete -ne $true) {
        throw 'MongoDB collection inventory is not complete.'
    }
    if ([string]$inventory.database -ne 'christopherbell') {
        throw 'MongoDB collection inventory must target christopherbell.'
    }
    $generatedAt = [DateTimeOffset]::MinValue
    if (-not [DateTimeOffset]::TryParse(
        [string]$inventory.generatedAt,
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::AssumeUniversal,
        [ref]$generatedAt)) {
        throw 'MongoDB collection inventory generatedAt is invalid.'
    }
    if ($inventory.PSObject.Properties.Name -notcontains 'collections') {
        throw 'MongoDB collection inventory collections are missing.'
    }
    $names = [Collections.Generic.List[string]]::new()
    $uniqueNames = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($collection in @($inventory.collections)) {
        if ([string]::IsNullOrWhiteSpace([string]$collection.name) -or
            [string]$collection.type -notin @('collection','view')) {
            throw 'MongoDB collection inventory contains an invalid collection.'
        }
        if ([string]$collection.name -like 'system.*') {
            throw 'MongoDB collection inventory must exclude system collections.'
        }
        foreach ($property in 'options','count','sizeBytes','storageSizeBytes',
            'totalIndexSizeBytes','indexes') {
            if ($collection.PSObject.Properties.Name -notcontains $property) {
                throw "MongoDB collection inventory is missing collection property: $property"
            }
        }
        $name = [string]$collection.name
        if (-not $uniqueNames.Add($name)) {
            throw 'MongoDB collection inventory names must be unique.'
        }
        [void]$names.Add($name)
        foreach ($index in @($collection.indexes)) {
            $indexProperties = @(
                'name','key','unique','sparse','expireAfterSeconds','partialFilterExpression')
            if (@($indexProperties | Where-Object {
                    $index.PSObject.Properties.Name -notcontains $_
                }).Count -gt 0 -or
                [string]::IsNullOrWhiteSpace([string]$index.name) -or $null -eq $index.key) {
                throw 'MongoDB collection inventory contains an invalid index.'
            }
        }
    }
    [string[]]$sortedNames = $names.ToArray()
    [Array]::Sort($sortedNames, [StringComparer]::Ordinal)
    if ([string]::Join([char]0, $names.ToArray()) -cne
        [string]::Join([char]0, $sortedNames)) {
        throw 'MongoDB collection inventory names must be sorted.'
    }
    return $inventory
}

function Get-ProductionMongoCollectionInventory {
    $config = Read-ProductionConfig
    $json = Invoke-CheckedProcess `
        -FilePath $config.mongoShellExe `
        -ArgumentList @(
            '--quiet'
            'mongodb://127.0.0.1:27017/admin'
            '--eval'
            (Get-ProductionMongoCollectionInventoryScript)
        ) `
        -WorkingDirectory $config.repositoryPath
    ConvertFrom-ProductionMongoCollectionInventory -Json $json
}

function Test-ProductionStartup {
```

Verification:
- Re-run focused Pester; expected GREEN: all new inventory behavior tests pass.
- Confirm the script safety test proves absence of document-read and mutation APIs.

#### Code Edit 2.4
- File: `ops/production/windows/modules/Production.Operations.psm1`
- Lines: 191
- Action: replace

Current:
```powershell
Export-ModuleMember -Function Get-ProductionStatus,Invoke-ProductionRollback,Watch-ProductionLogs,Restart-ProductionService,Get-ProductionReleases,Assert-AutoDeployTaskContract,Test-ProductionStartup
```

Proposed:
```powershell
Export-ModuleMember -Function Get-ProductionStatus,Invoke-ProductionRollback,Watch-ProductionLogs,Restart-ProductionService,Get-ProductionReleases,Assert-AutoDeployTaskContract,Get-ProductionMongoCollectionInventory,Test-ProductionStartup
```

Verification:
- Import the module and run `Get-Command Get-ProductionMongoCollectionInventory`; expected: one exported function.
- Run the repository PowerShell parser/static checks included by `:website:check`.

- [x] **Step 4: Wire the CLI, help output, and Make target.**

#### Code Edit 2.5
- File: `ops/production/windows/prod.ps1`
- Lines: 1-8
- Action: replace

Current:
```powershell
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
    [string]$Command = 'help',
    [switch]$WhatIf,
    [string]$CloudflareTokenPath
)
```

Proposed:
```powershell
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','mongo-inventory','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
    [string]$Command = 'help',
    [switch]$WhatIf,
    [string]$CloudflareTokenPath
)
```

Verification:
- Run `pwsh -NoLogo -NoProfile -File ops/production/windows/prod.ps1 invalid`; expected parameter validation failure lists `mongo-inventory` as an allowed command.

#### Code Edit 2.6
- File: `ops/production/windows/prod.ps1`
- Lines: 17-37
- Action: replace

Current:
```powershell
$handlers = @{
    help = { Show-ProductionHelp }
    install = { Install-ProductionRuntime -WhatIf:$WhatIf -CloudflareTokenPath $CloudflareTokenPath }
    deploy = { Invoke-ProductionDeploy -WhatIf:$WhatIf }
    status = { Get-ProductionStatus }
    logs = { Watch-ProductionLogs }
    restart = { Restart-ProductionService -Verify }
    releases = { Get-ProductionReleases }
    rollback = { Invoke-ProductionRollback -WhatIf:$WhatIf }
    backup = { New-ProductionBackup }
    'verify-startup' = { Test-ProductionStartup }
    uninstall = { Uninstall-ProductionRuntime -WhatIf:$WhatIf }
    'auto-install' = { Install-AutoDeployTask -WhatIf:$WhatIf }
    'auto-deploy' = { Start-AutoDeployLoop }
    'auto-status' = { Get-AutoDeployStatus }
    'auto-remove' = { Remove-AutoDeployTask -WhatIf:$WhatIf }
    'sensor-install' = { Install-PawnIoProvider -WhatIf:$WhatIf }
    'sensor-status' = { Get-ProductionSensorStatus }
    'sensor-enable' = { Set-ProductionSensorState -Enabled $true -WhatIf:$WhatIf }
    'sensor-disable' = { Set-ProductionSensorState -Enabled $false -WhatIf:$WhatIf }
}
```

Proposed:
```powershell
$handlers = @{
    help = { Show-ProductionHelp }
    install = { Install-ProductionRuntime -WhatIf:$WhatIf -CloudflareTokenPath $CloudflareTokenPath }
    deploy = { Invoke-ProductionDeploy -WhatIf:$WhatIf }
    status = { Get-ProductionStatus }
    logs = { Watch-ProductionLogs }
    restart = { Restart-ProductionService -Verify }
    releases = { Get-ProductionReleases }
    rollback = { Invoke-ProductionRollback -WhatIf:$WhatIf }
    backup = { New-ProductionBackup }
    'mongo-inventory' = {
        Get-ProductionMongoCollectionInventory | ConvertTo-Json -Depth 100
    }
    'verify-startup' = { Test-ProductionStartup }
    uninstall = { Uninstall-ProductionRuntime -WhatIf:$WhatIf }
    'auto-install' = { Install-AutoDeployTask -WhatIf:$WhatIf }
    'auto-deploy' = { Start-AutoDeployLoop }
    'auto-status' = { Get-AutoDeployStatus }
    'auto-remove' = { Remove-AutoDeployTask -WhatIf:$WhatIf }
    'sensor-install' = { Install-PawnIoProvider -WhatIf:$WhatIf }
    'sensor-status' = { Get-ProductionSensorStatus }
    'sensor-enable' = { Set-ProductionSensorState -Enabled $true -WhatIf:$WhatIf }
    'sensor-disable' = { Set-ProductionSensorState -Enabled $false -WhatIf:$WhatIf }
}
```

Verification:
- Run `pwsh -NoLogo -NoProfile -File ops/production/windows/prod.ps1 help`; expected output includes `mongo-inventory`.
- Mocked/module verification must prove the handler emits one valid JSON document rather than formatted PowerShell table output.

#### Code Edit 2.7
- File: `ops/production/windows/modules/Production.Common.psm1`
- Lines: 519-527
- Action: replace

Current:
```powershell
function Show-ProductionHelp {
    @'
Usage: prod.cmd <command> [-WhatIf]

Commands: install, deploy, status, logs, restart, releases, rollback, backup,
          verify-startup, uninstall, auto-install, auto-deploy, auto-status,
          auto-remove, sensor-install, sensor-status, sensor-enable,
          sensor-disable
'@ | Write-Output
}
```

Proposed:
```powershell
function Show-ProductionHelp {
    @'
Usage: prod.cmd <command> [-WhatIf]

Commands: install, deploy, status, logs, restart, releases, rollback, backup,
          mongo-inventory, verify-startup, uninstall, auto-install, auto-deploy,
          auto-status, auto-remove, sensor-install, sensor-status,
          sensor-enable, sensor-disable
'@ | Write-Output
}
```

Verification:
- Run the help command and assert `mongo-inventory` appears exactly once.

#### Code Edit 2.8
- File: `Makefile`
- Lines: 1-4
- Action: replace

Current:
```make
.PHONY: prod-install prod-deploy prod-status prod-logs prod-restart prod-releases prod-rollback prod-backup prod-verify-startup prod-uninstall prod-auto-install prod-auto-deploy prod-auto-status prod-auto-remove prod-cloudflare-upgrade

prod-install prod-deploy prod-status prod-logs prod-restart prod-releases prod-rollback prod-backup prod-verify-startup prod-uninstall prod-auto-install prod-auto-deploy prod-auto-status prod-auto-remove:
	@cmd.exe /d /c prod.cmd $(@:prod-%=%)
```

Proposed:
```make
.PHONY: prod-install prod-deploy prod-status prod-logs prod-restart prod-releases prod-rollback prod-backup prod-mongo-inventory prod-verify-startup prod-uninstall prod-auto-install prod-auto-deploy prod-auto-status prod-auto-remove prod-cloudflare-upgrade

prod-install prod-deploy prod-status prod-logs prod-restart prod-releases prod-rollback prod-backup prod-mongo-inventory prod-verify-startup prod-uninstall prod-auto-install prod-auto-deploy prod-auto-status prod-auto-remove:
	@cmd.exe /d /c prod.cmd $(@:prod-%=%)
```

Verification:
- Run `make -n prod-mongo-inventory`; expected command is `cmd.exe /d /c prod.cmd mongo-inventory` and no operation executes.

- [x] **Step 5: Run focused Pester in PowerShell 7 and Windows PowerShell 5.1.**

Run:
```powershell
pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Operations.Tests.ps1 -Output Detailed"
pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Command.Tests.ps1 -Output Detailed"
powershell.exe -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Operations.Tests.ps1 -Output Detailed"
```

Expected: zero failures in both hosts.

- [x] **Step 6: Commit Task 2.**

```powershell
git add Makefile ops/production/windows/prod.ps1 ops/production/windows/modules/Production.Common.psm1 ops/production/windows/modules/Production.Operations.psm1 ops/production/windows/tests/Production.Command.Tests.ps1 ops/production/windows/tests/Production.Operations.Tests.ps1
git commit -m "Add read-only MongoDB collection inventory"
```

### Task 3 - Document operator usage and cleanup boundaries

Sequence / dependencies:
- Runs after Tasks 1 and 2 because command and catalog paths must be final.
- Documentation-only task; it does not authorize or execute database changes.

Interfaces:
- Consumes: `prod.cmd mongo-inventory` and `docs/operations/mongodb-collection-catalog.md`.
- Produces: discoverable README and native Windows runbook instructions.

Implementation notes:
- Required skill: `chris-street-style` before editing copy-ready command examples.
- Before-Edit Brief:
  - Behavior: Operators can discover the catalog, run the exact metadata-only command, save JSON safely, and understand that live-only/empty collections are not deletion candidates by default.
  - Invariants: Documentation never prints secret-bearing configuration, suggests document reads, or weakens backup/approval rules.
  - Boundary/API: README and native Windows runbook only; the MongoDB backup/restore runbook remains the authority for recovery.
  - Effects and failures: Documentation has no runtime effect. Commands describe a read-only operation; incomplete output must be discarded rather than interpreted.
  - Tests and evidence: Starting evidence is the current docs omitting the catalog and command. Completion evidence is link validation, command/help consistency, and full hub/repository documentation checks.

- [x] **Step 1: Link the catalog and command from the repository README.**

#### Code Edit 3.1
- File: `README.md`
- Lines: 452-462
- Action: replace

Current:
````markdown
Common operations:

```powershell
.\prod.cmd status
.\prod.cmd logs
.\prod.cmd releases
.\prod.cmd rollback
.\prod.cmd backup
.\prod.cmd auto-status
.\prod.cmd verify-startup
```

````

Proposed:
````markdown
Common operations:

```powershell
.\prod.cmd status
.\prod.cmd logs
.\prod.cmd releases
.\prod.cmd rollback
.\prod.cmd backup
.\prod.cmd mongo-inventory
.\prod.cmd auto-status
.\prod.cmd verify-startup
```

````

Verification:
- Run the README command block review and verify `mongo-inventory` appears between backup and auto-status.

#### Code Edit 3.2
- File: `README.md`
- Lines: 487
- Action: replace

Current:
```markdown
### MongoDB Backups and Restores
```

Proposed:
```markdown
### MongoDB Backups, Catalog, and Restores
```

Verification:
- Verify the renamed heading still precedes the existing Windows, backup/restore, and migration runbook links.

#### Code Edit 3.3
- File: `README.md`
- Lines: after 492
- Action: add

Current:
```text
The existing MongoDB section ends after its migration-runbook sentence.
```

Proposed:
```markdown

Use the [MongoDB collection catalog][mongodb-collection-catalog] to understand
physical ownership and `prod.cmd mongo-inventory` for a metadata-only live
comparison.

[mongodb-collection-catalog]: docs/operations/mongodb-collection-catalog.md
```

Verification:
- Verify the new reference-style catalog link resolves with the existing three inline runbook links.
- Verify the README does not describe `mongo-inventory` as cleanup or collection consolidation.

- [x] **Step 2: Add the native Windows inventory runbook.**

#### Code Edit 3.4
- File: `docs/operations/windows-production.md`
- Lines: 286-300
- Action: replace

Current:
````markdown
```powershell
.\prod.cmd status
.\prod.cmd logs
.\prod.cmd releases
.\prod.cmd restart
.\prod.cmd backup
.\prod.cmd rollback -WhatIf
.\prod.cmd rollback
.\prod.cmd verify-startup
```

Equivalent Makefile targets include `prod-status`, `prod-deploy`,
`prod-backup`, and `prod-verify-startup`.
````

Proposed:
````markdown
```powershell
.\prod.cmd status
.\prod.cmd logs
.\prod.cmd releases
.\prod.cmd restart
.\prod.cmd backup
.\prod.cmd mongo-inventory
.\prod.cmd rollback -WhatIf
.\prod.cmd rollback
.\prod.cmd verify-startup
```

Equivalent Makefile targets include `prod-status`, `prod-deploy`,
`prod-backup`, `prod-mongo-inventory`, and `prod-verify-startup`.
````

Verification:
- Compare every daily-operation command spelling with `prod.ps1`, `Show-ProductionHelp`, and `Makefile`.

#### Code Edit 3.5
- File: `docs/operations/windows-production.md`
- Lines: before 507
- Action: add

Current:
```text
No MongoDB collection-inventory section exists before the backup and restore section.
```

Proposed:
````markdown
MongoDB Collection Inventory
----------------------------

Run the fixed, metadata-only inventory locally on the production host:

```powershell
.\prod.cmd mongo-inventory |
  Set-Content -LiteralPath .\mongo-collection-inventory.json -Encoding utf8
$inventory = Get-Content -LiteralPath .\mongo-collection-inventory.json -Raw |
  ConvertFrom-Json
```

The command connects only to `mongodb://127.0.0.1:27017/admin`, selects the
`christopherbell` database inside the audited script, and returns collection
names/types, allowlisted collection options, counts, storage/index sizes, and
index definitions. It excludes `system.*` names and never reads document
bodies. Delete the local JSON after the comparison if it is not being retained
as a reviewed test-report attachment.

Compare the returned names with the checked-in
`docs/operations/mongodb-collection-catalog.md`. A source-only name may be an
unused feature that has never materialized. A live-only or empty name is an
unreviewed extra, not permission to drop it. If output is incomplete, malformed,
or for a different database, stop and discard it.

Collection cleanup requires a separate approved plan with a current compressed
backup, SHA-256, restore validation, exact-namespace backup, impact report,
one-at-a-time removal, rollback retention, and Mongo-backed website verification.
This command cannot rename, merge, drop, compact, repair, or clean collections.
````

Verification:
- Run the repository Markdown/link checks included by `:website:check`.
- Verify the new section appears immediately before `Native MongoDB Backup and Restore`.

- [x] **Step 3: Commit Task 3.**

```powershell
git add README.md docs/operations/windows-production.md
git commit -m "Document MongoDB collection inventory"
```

### Task 4 - Verify, review, publish, and observe production metadata

Sequence / dependencies:
- Runs after all code and documentation tasks.
- No code edits are planned; any discovered defect returns to the owning task with a new RED/GREEN cycle.

Interfaces:
- Consumes: complete spoke diff, focused tests, disposable MongoDB, packaged candidate, GitHub CI, protected deployment path.
- Produces: review evidence, Builder test report/update/closure/session memory, and a live metadata comparison with no cleanup action.

Implementation notes:
- Required skill: `chris-street-style` in review mode for the final code/test diff.
- Use `superpowers:verification-before-completion` before any success claim.
- Use `verify-local-spring-app` for alternate-port application verification.
- Before-Edit Brief:
  - Behavior: The delivered catalog and command work from source through production while the website and database remain unchanged.
  - Invariants: No test or verification step reads document bodies or mutates production MongoDB; port 8080 is untouched until the protected post-merge deployment; live-only results remain observations.
  - Boundary/API: JUnit architecture test, Pester operations module, production CLI, packaged application health, GitHub PR/CI, and local production operations.
  - Effects and failures: Disposable Mongo and alternate-port app effects are isolated and cleaned up exactly. Production effect is metadata reads plus ordinary protected deployment. Any incomplete inventory, failed test, CI failure, readiness failure, or Mongo-backed smoke failure blocks completion.
  - Tests and evidence: Focused RED/GREEN records from Tasks 1-2, full test outputs, exact disposable-Mongo JSON, alternate-port URL/status/body, CI/CodeQL conclusions, listener rotation, service state, and final metadata comparison.

- [x] **Step 1: Run focused and full automated verification.**

```powershell
$env:GRADLE_USER_HOME = Join-Path $env:TEMP 'christopherbell-dev-mongo-catalog-gradle'
.\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.architecture.MongoCollectionCatalogTest
.\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.architecture.*
pwsh -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Operations.Tests.ps1 -Output Detailed"
powershell.exe -NoLogo -NoProfile -Command "Invoke-Pester -Path ops/production/windows/tests/Production.Operations.Tests.ps1 -Output Detailed"
.\gradlew.bat --no-daemon :website:check --stacktrace
git diff --check
```

Expected: zero failures/errors; only documented pre-existing skips are acceptable.

- [x] **Step 2: Exercise the JavaScript inventory against disposable MongoDB.**

Use the installed MongoDB Server and configured `mongosh` to start a separate `mongod` on port `27018` with a newly created temporary dbpath. Seed only synthetic collections and indexes, run the exact script from `Get-ProductionMongoCollectionInventoryScript` against `mongodb://127.0.0.1:27018/admin`, and verify:

- `complete=true` and `database=christopherbell`;
- synthetic collection names and indexes are sorted;
- counts/sizes/index sizes are numeric or null as specified;
- no document fields or values appear;
- a forced `collStats`/connection failure exits nonzero and yields no trusted partial object.

Stop only the disposable PID bound to `27018`, verify its resolved dbpath remains under the task-specific temporary directory, then remove that temporary directory. Never stop PID 5620 or anything bound to production port `27017` based on the planning-time snapshot; resolve current ownership at execution time.

- [x] **Step 3: Run packaged alternate-port application verification.**

Build the boot JAR, start it on a non-8080 port such as `8097` against the disposable MongoDB instance with scheduling and mail disabled, and record:

- `http://127.0.0.1:8097/actuator/health/liveness` status/body;
- `http://127.0.0.1:8097/actuator/health/readiness` status/body;
- `http://127.0.0.1:8097/` status/title/body signature;
- one Mongo-backed read flow with exact request and response;
- absence of collection creation beyond expected source mappings for exercised features.

Stop only the candidate PID identified on port `8097`.

- [x] **Step 4: Review the final diff.**

Apply the Jane Street review rubric to catalog parsing, manual-reference completeness, metadata allowlisting, process arguments, failure causes, PowerShell 5.1 compatibility, and test evidence. Treat any semantic gap as a blocker and return to the owning task.

- [x] **Step 5: Push the branch and open a focused draft PR.**

The PR must state that it performs no collection merge, rename, deletion, document read, or schema/index change. Include focused/full test evidence and the disposable/alternate-port runtime evidence.

- [x] **Step 6: Wait for all required CI, CodeQL, and dependency checks.**

Fix failures through a focused RED/GREEN cycle, update evidence, and require a final review of the new HEAD before merge.

- [x] **Step 7: Merge and deploy through the protected native Windows path.**

Wait through listener rotation. A transient readiness `503` is acceptable only during rotation and must become `200`/`UP` on recheck. Confirm `MongoDB`, `ChristopherBellDev`, and `cloudflared` remain Running and Automatic.

- [x] **Step 8: Run and record the live metadata-only comparison.**

Run the installed `prod.cmd mongo-inventory`. Record URL/host boundary (`127.0.0.1:27017`, database `christopherbell`), command input, completeness, collection total, index total, and the set difference against the checked-in catalog. Do not preserve document data because none should be returned. Do not call any collection an orphan until current source, migrations, scripts, history, and ownership are reviewed; do not remove anything in this delivery.

- [x] **Step 9: Complete durable Builder evidence and source-work closure.**

Use `save-test-report`, `ingest-spoke-update`, `review-spoke-work`, `close-story-issue` if a source issue exists, `save-session-memory`, `update-hub-indexes`, `validate-hub-state`, and `close-hub-work` as applicable. Commit/push Builder artifacts through `commit-push-builder-main`.

## Code Changes

| Task | File | Action | Purpose |
| --- | --- | --- | --- |
| 1 | `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java` | add | Discover mapped names and enforce catalog validity/completeness. |
| 1 | `docs/operations/mongodb-collection-catalog.md` | add | Human-readable 51-collection ownership and lifecycle catalog. |
| 2 | `ops/production/windows/tests/Production.Operations.Tests.ps1` | add tests | Prove metadata-only script, fixed target, and fail-closed validation. |
| 2 | `ops/production/windows/tests/Production.Command.Tests.ps1` | add test | Prove CLI/help/Make wiring and one JSON-producing handler. |
| 2 | `ops/production/windows/modules/Production.Operations.psm1` | add functions/export | Build audited JavaScript, validate untrusted JSON, and invoke configured `mongosh`. |
| 2 | `ops/production/windows/prod.ps1` | modify | Add `mongo-inventory` command dispatch. |
| 2 | `ops/production/windows/modules/Production.Common.psm1` | modify | Add the command to help output. |
| 2 | `Makefile` | modify | Add dry, predictable `prod-mongo-inventory` target. |
| 3 | `README.md` | modify | Link the catalog and common operation. |
| 3 | `docs/operations/windows-production.md` | modify | Document metadata scope, saving output, failure behavior, and cleanup gate. |

## Files and Modules

- Builder controlling spec and plan: `docs/specs/2026-08-09-christopherbell-dev-mongodb-collection-catalog.md` and this plan.
- Spoke architecture tests: `website/src/test/java/dev/christopherbell/architecture/`.
- Spoke MongoDB operations docs: `docs/operations/`.
- Native Windows production operations: `ops/production/windows/`.
- Repository entry points: `README.md`, `Makefile`, and `prod.cmd`/`prod.ps1`.

## Unit Testing

- JUnit catalog row shape, allowed values, uniqueness, exact count, mapped-name discovery, and manual-reference union.
- Pester script allowlist/denylist, exact loopback invocation, complete JSON acceptance, malformed/incomplete/wrong-database/duplicate/unsorted rejection.
- Help/CLI command validation and Make dry-run consistency.
- RED must be witnessed before adding the corresponding production/catalog implementation.

## Local Testing

- Run focused JUnit and Pester in PowerShell 7 and Windows PowerShell 5.1.
- Run full `:website:check` with a private Gradle home and no short outer timeout.
- Run the exact JavaScript against a disposable `mongod` on port `27018` with synthetic data only.
- Run the packaged application on port `8097`, not 8080, against disposable MongoDB.
- Capture exact command, target port/database, status/output, and cleanup ownership.

## Validation

- Catalog contains exactly the expected current physical names and explains intentional shared/legacy mappings.
- A new undocumented `@Document` mapping fails JUnit.
- `prod.cmd mongo-inventory` uses only the configured `mongosh`, fixed loopback URI, fixed database, and audited metadata APIs.
- Invalid or partial output never becomes a trusted inventory object.
- No documents, secrets, or secret-bearing command lines appear in output/evidence.
- Full repository tests, PR checks, CodeQL, alternate-port app verification, deployment, service state, and live metadata comparison pass.
- No MongoDB data, names, indexes, schemas, or retention rules change.

## Rollback or Recovery

- Before merge: revert the focused task commit or revise through a new RED/GREEN cycle.
- After merge but before deployment: redeploy the previous application release; MongoDB needs no recovery because this feature is read-only and schema-neutral.
- After deployment: application rollback is sufficient. The operations command can be removed by deploying the previous release; it creates no MongoDB state.
- If inventory output is malformed or incomplete, discard it and investigate the command/configuration. Do not infer source/live differences.
- No collection restore path is exercised because collection cleanup is explicitly outside this plan.

## Risks

- **Scanner misses a mapping:** Spring classpath scanning behavior may exclude an unusual persistence type. Mitigation: compare the first run with the inspected 52 annotations/51 names and keep manual references explicit.
- **Manual-reference drift:** A new `MongoTemplate` literal may not add a new `@Document`. Mitigation: architecture review must update the explicit set; future work may add a source analyzer only if real drift demonstrates the need.
- **Catalog parser couples to Markdown:** Table format changes can fail tests. Mitigation: keep one deliberately structured table and return actionable row diagnostics.
- **Inventory exposes too much metadata:** Collection validators or partial indexes can contain constants. Mitigation: allowlist collection option keys, never include raw `collStats`, and inspect final JSON before retention.
- **PowerShell compatibility:** JSON parsing and exception construction must work in both required hosts, while CLI serialization runs under the PowerShell 7-only `prod.cmd` contract. Mitigation: run focused module Pester in PowerShell 7 and Windows PowerShell 5.1 and exercise the real CLI under PowerShell 7.
- **Large catalog becomes stale:** Manual prose can drift. Mitigation: automated physical-name coverage and owner/index review in every persistence change.
- **Live-only names are misclassified:** Historical/rollback collections can look unused. Mitigation: report only set differences and preserve the separate approval/backup gate.
- **Dirty checkout damage:** Authoritative spoke has unrelated changes. Mitigation: isolated worktree from refreshed `origin/main` and exact path verification before edits.

## Completion Criteria

- Approved plan tasks are implemented in an isolated worktree with cohesive commits.
- Catalog JUnit tests witnessed RED, then pass with exactly 51 current physical names.
- Pester inventory tests witnessed RED, then pass in both PowerShell hosts.
- Disposable MongoDB integration proves metadata-only output and fail-closed behavior.
- Full `:website:check`, formatting/static validation, and `git diff --check` pass.
- Alternate-port packaged runtime evidence is recorded.
- Final Jane Street review has no blockers.
- PR checks and CodeQL pass on the final reviewed HEAD; PR merges.
- Protected production deployment completes; readiness/liveness and services recover to healthy state.
- Live metadata inventory completes and source/live differences are reported without cleanup.
- Builder test report, review/update, closure, indexes, and session memory are committed and pushed.
