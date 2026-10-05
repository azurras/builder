# WFL Session and Restaurant Safety/Scalability Issues 1280-1289 Implementation Plan

## Document Status

complete

## Objective

Resolve #1280-#1289 by preserving shared sessions during account deletion, bounding and atomically mutating session state, enforcing host/lifecycle rules, batching list hydration, paging restaurant administration and duplicate discovery, constraining restaurant URLs to HTTP(S), and minimizing expiring anonymous browser state.

## Goals

- Preserve sessions owned by other accounts while removing a deleted participant and vote.
- Enforce 20 total members on create, invite, and shared-link join with stable conflict codes.
- Make joins, votes, and restaurant resets atomic and retry-safe without replica-set transactions.
- Restrict restaurant resets to the host and expose that capability/revision in the API and UI.
- Keep sessions active for 24 hours, readable in a 30-day archive, and TTL-delete them afterward.
- Hydrate a 25-session history with one restaurant, one rating, and one favorite query group.
- Page/filter the admin inventory and page duplicate-name aggregation without collection-wide reads.
- Persist and render only safe absolute HTTP(S) restaurant URLs.
- Retain anonymous WFL state for at most 30 minutes without coordinates or full restaurant objects.

## Inputs

- Campaign spec `docs/specs/2026-07-29-complete-christopherbell-dev-issues-1258-1307.md`.
- Trusted GitHub issues #1280-#1289 by `azurras`; all have zero comments and no attachments.
- Refreshed `origin/main` commit `e3afbf3c9eeb65525f573f299f82287ef8665554`.
- Mandatory test-first execution and `chris-street-style`.

## Branch

`codex/issues-1280-1289-20260729` in `A:\Projects\christopherbell.dev-worktrees\issues-1280-1289-20260729`, based on `e3afbf3c`.

## Non-Goals

- Redesign restaurant selection, ratings, favorites, imports, or account-deletion orchestration.
- Require MongoDB replica-set transactions.
- Expose account IDs or precise browser coordinates in API/browser persistence.
- Remove existing WFL routes; bounded compatibility behavior remains.

## Assumptions

- Account IDs are application-generated safe identifiers and can be used in targeted Mongo map paths after explicit validation.
- A session has at most 20 total participants, including its creator.
- Session mutation revision is a monotonic `long`; targeted joins/votes increment it, and host resets compare the caller's expected revision before clearing votes.
- Active lifetime is 24 hours. Archive lifetime is 30 additional days. Mongo TTL deletion is based on `deleteOn`.
- Reset audit retains the latest 100 entries plus an all-time count, keeping the session document bounded during its finite lifetime.
- Inventory filter keys and duplicate keys are normalized at write/migration time so their indexes are usable.

## Open Questions

None. The stable session conflict codes are `WFL_SESSION_FULL`, `WFL_SESSION_EXPIRED`, and `WFL_SESSION_CHANGED`; non-host reset attempts return access denied.

## Task Breakdown

### Task 1 - Preserve shared sessions during account deletion (#1280)

Sequence / dependencies:
- First because deletion semantics must be reflected in all later session invariants.

Implementation notes:
- Delete sessions where the account is `createdByAccountId`.
- For every other session, atomically pull the participant ID and unset its username/vote map entries while incrementing revision.
- Keep the operation idempotent and do not rewrite remaining participant state.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/account/deletion/MongoAccountDeletionOperations.java`
- Lines: 56-76
- Action: replace

Current:
```java
remove("whatsforlunch_sessions", accountId,
    "createdByAccountId", "participantAccountIds");
```

Proposed:
```java
mongo.remove(exact("createdByAccountId", accountId), "whatsforlunch_sessions");
mongo.updateMulti(
    exact("participantAccountIds", accountId),
    new Update()
        .pull("participantAccountIds", accountId)
        .unset(safeMapPath("participantUsernamesByAccountId", accountId))
        .unset(safeMapPath("votesByAccountId", accountId))
        .inc("revision", 1),
    "whatsforlunch_sessions");
```

Add creator, invited participant, joined participant, idempotence, and remaining-member service-view tests.

Verification:
- `./gradlew.bat :website:test --tests '*MongoAccountDeletionOperationsTest' --tests '*WhatsForLunchSessionServiceTest'`

### Task 2 - Bounded atomic session persistence (#1281, #1282)

Sequence / dependencies:
- After deletion invariants; before service/lifecycle/UI changes.

Implementation notes:
- Add `WhatsForLunchSessionMutationStore` using `MongoTemplate.findAndModify` with server-side predicates and `$addToSet`/targeted `$set`.
- Creation rejects more than 19 invited non-creators; join adds only below 20 and repeated joins remain no-ops.
- Votes target only the caller's map entry. Every successful mutation updates `lastUpdatedOn` and increments revision.
- Add a WFL-specific conflict exception/advice returning a stable message code in the normal response envelope.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WhatsForLunchSessionService.java`
- Lines: 39-168
- Action: replace

Current:
```java
session.setParticipantAccountIds(List.copyOf(participantIds));
session = sessionRepository.save(session);
// votes and restaurant changes also load, mutate, and save the whole document
```

Proposed:
```java
var outcome = mutations.join(sessionId, self.getId(), self.getUsername(), now, MAX_MEMBERS);
return switch (outcome.status()) {
  case UPDATED, UNCHANGED -> assembler.one(outcome.session(), self.getId());
  case FULL -> throw conflict(WFL_SESSION_FULL);
  case EXPIRED -> throw conflict(WFL_SESSION_EXPIRED);
  case MISSING -> throw notFound(sessionId);
};
```

Add `WhatsForLunchSessionMutationStore`, `WflSessionConflictException`, and its controller advice. Add deterministic repeated, concurrent, and over-cap join tests plus concurrent vote/reset tests.

Verification:
- `./gradlew.bat :website:test --tests '*WhatsForLunchSessionMutationStoreTest' --tests '*WhatsForLunchSessionServiceTest' --tests '*RestaurantControllerTest'`

### Task 3 - Host authority, revision, lifecycle, and bounded audit (#1283, #1284)

Sequence / dependencies:
- Uses Task 2 atomic mutation store.

Implementation notes:
- Add `revision`, `activeUntil`, `deleteOn`, reset-audit count/history, and TTL/index coverage.
- Detail responses expose `revision`, `active`, and `canChangeRestaurants` but never creator account ID.
- Host reset requires matching expected revision, resets votes atomically, and appends a bounded attribution/timestamp/old/new-pick audit entry.
- Expired sessions remain visible to participants in history/direct reads until `deleteOn` but all mutations return `WFL_SESSION_EXPIRED`.
- Configure/validate 24-hour active and 30-day archive lifetimes in `WflProperties`.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/WhatsForLunchSession.java`
- Lines: 23-43
- Action: replace

Current:
```java
private Map<String, String> votesByAccountId;
private Instant createdOn;
private Instant lastUpdatedOn;
```

Proposed:
```java
private Map<String, String> votesByAccountId;
private long revision;
private Instant activeUntil;
@Indexed(name = "wfl_session_delete_ttl", expireAfter = "0s")
private Instant deleteOn;
private long restaurantResetCount;
private List<WhatsForLunchRestaurantResetAudit> restaurantResetAudit;
```

Update `WhatsForLunchSessionDetail` lines 11-22 and `WhatsForLunchSessionRestaurantsRequest` to carry capability/revision. Update `whats-for-lunch.js` lines 272-424 and 765-784 to show archived status and permit “Try 3 more” only when `canChangeRestaurants`, sending `expectedRevision`.

Verification:
- `./gradlew.bat :website:test --tests '*WhatsForLunchSession*'`
- `./gradlew.bat :website:jsTest`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V011HardenWhatsForLunchData.java`
- Lines: before 1
- Action: add

Current:
```text
No V011 exists. Existing sessions lack revision, lifecycle, bounded audit, or TTL metadata.
```

Proposed:
```java
public void apply(MongoTemplate mongo) {
  backfillSessionsInBatches(mongo);
  backfillRestaurantQueryKeysAndSafeWebsites(mongo);
  ensureSessionAndRestaurantIndexes(mongo);
}
```

Add checksum/idempotence/boundary tests, including a session exactly at `activeUntil`, archive visibility, TTL field/index, stale reset, host/participant authorization, and audit cap/count.

Verification:
- `./gradlew.bat :website:test --tests '*V011*' --tests '*WflPropertiesTest' --tests '*WhatsForLunchSession*'`
- `./gradlew.bat :website:jsTest`

### Task 4 - Batch session-list hydration (#1285)

Sequence / dependencies:
- After the final detail/lifecycle contract.

Implementation notes:
- Collect distinct restaurant IDs from the whole page, load restaurants once, ratings once, and caller favorites once.
- Build immutable maps and assemble every session without repository access inside the loop.
- Keep the list maximum at 25 and include active/archive state.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/WhatsForLunchSessionService.java`
- Lines: 84-354
- Action: replace

Current:
```java
return sessions.stream()
    .map(session -> toDetail(session, self.getId()))
    .toList();
```

Proposed:
```java
var sessions = sessionRepository.findRecentForParticipant(self.getId(), now, page);
return assembler.many(sessions, self.getId());
```

Add `WhatsForLunchSessionAssembler` with page-wide restaurant/rating/favorite maps. Tests assert identical query totals for one and 25 sessions and no query per session.

Verification:
- `./gradlew.bat :website:test --tests '*WhatsForLunchSessionAssemblerTest' --tests '*WhatsForLunchSessionServiceTest'`

### Task 5 - Paginated searchable admin inventory (#1286)

Sequence / dependencies:
- Independent of sessions; V011 supplies query keys/indexes first.

Implementation notes:
- Add stable cursor/page response at V20260729 with default 25, max 100, sort by normalized name then ID.
- Normalize optional name-prefix, city, and state filters; reject invalid sizes/cursors.
- Cap/deprecate the legacy array route so no route performs `findAll()`.
- Back Office renders filter fields, rows, and next-page action instead of loading the whole inventory to compute counts.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 137-146
- Action: replace

Current:
```java
public List<RestaurantDetail> getRestaurants() {
  return toRatedDetails(restaurantRepository.findAll());
}
```

Proposed:
```java
public RestaurantInventoryPage getRestaurantInventory(RestaurantInventoryQuery request) {
  var page = inventory.find(request.normalized(), MAX_INVENTORY_PAGE_SIZE);
  return hydrateInventory(page);
}
```

Add `RestaurantInventoryQueryRepository`, DTO/page records, stable controller route, and capped legacy adapter. Update `api.js` lines 239-281 and `back-office.js` lines 660-690 plus the WFL panel template.

Verification:
- `./gradlew.bat :website:test --tests '*RestaurantInventory*' --tests '*RestaurantControllerTest'`
- `./gradlew.bat :website:jsTest`

### Task 6 - Indexed paged duplicate discovery (#1287)

Sequence / dependencies:
- V011 supplies non-unique `dedupeKey` and index.

Implementation notes:
- Aggregate only `dedupeKey` groups with count > 1, ordered/cursor-paged by key.
- Fetch documents only for keys on the requested page; apply fetches only confirmed keys.
- Preserve exact version, survivor, and member-ID comparison before deletion.
- Back Office walks preview pages explicitly and applies only reviewed groups.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 487-647
- Action: replace

Current:
```java
return restaurantRepository.findAll().stream()
    .collect(groupingBy(restaurant -> normalizeRestaurantName(restaurant.getName())))
    .entrySet().stream().filter(group -> group.getValue().size() > 1).toList();
```

Proposed:
```java
var keys = duplicates.findDuplicateKeys(cursor, size + 1);
var members = duplicates.findMembers(keys.pageKeys());
return toPreviewPage(keys, members);
```

Add `RestaurantDuplicateQueryRepository` aggregation tests with a large unrelated corpus and command/query-shape assertions. Update preview controller query parameters and Back Office pagination.

Verification:
- `./gradlew.bat :website:test --tests '*RestaurantDuplicateQueryRepositoryTest' --tests '*RestaurantServiceTest' --tests '*RestaurantControllerTest'`
- `./gradlew.bat :website:jsTest`

### Task 7 - Safe restaurant website URLs at ingestion and rendering (#1288)

Sequence / dependencies:
- Apply in V011 before public rendering tests.

Implementation notes:
- Central Java policy accepts only absolute HTTP/HTTPS URLs with host and no user information; it trims and normalizes scheme case.
- Admin create/update reject invalid nonblank URLs. Imports discard invalid URL values. V011 removes unsafe existing values.
- Response mapping rechecks the policy as defense in depth.
- Browser code creates website anchors with DOM APIs from validated URLs; no website URL is interpolated into HTML.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 95-881
- Action: replace

Current:
```java
var restaurant = restaurantMapper.toRestaurant(request);
restaurantRepository.save(restaurant);
```

Proposed:
```java
var restaurant = restaurantMapper.toRestaurant(request);
restaurant.setWebsite(websiteUrls.requireSafe(request.website()));
prepareIndexedFields(restaurant);
restaurantRepository.save(restaurant);
```

Add `RestaurantWebsiteUrlPolicy` and apply it in `OpenStreetMapRestaurantClient`/import merge and response hydration.

Verification:
- `./gradlew.bat :website:test --tests '*RestaurantWebsiteUrl*' --tests '*RestaurantServiceTest' --tests '*OpenStreetMapRestaurantClientTest'`

#### Code Edit 7.2
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 213-424
- Action: replace

Current:
```javascript
`<a href="${sanitize(restaurant.website)}" target="_blank">Website</a>`
```

Proposed:
```javascript
const placeholder = '<span data-safe-restaurant-website></span>';
// after rendering, validate URL and append document.createElement('a')
```

Apply the same shared browser helper to `restaurant-profile.js` lines 90-100. Test mixed-case schemes, whitespace, protocol-relative URLs, credentials, `javascript:`, and `data:` in Java and browser suites.

Verification:
- `./gradlew.bat :website:test --tests '*RestaurantWebsiteUrl*' --tests '*RestaurantServiceTest' --tests '*OpenStreetMapRestaurantClientTest'`
- `./gradlew.bat :website:jsTest`

### Task 8 - Expiring minimal anonymous browser state (#1289)

Sequence / dependencies:
- Last browser integration task, reusing safe hydrated restaurant details.

Implementation notes:
- Version 2 stores only three restaurant IDs, optional normalized ZIP, and `expiresAt`; it never stores coordinates or restaurant payloads.
- Lifetime is 30 minutes. Expired/corrupt records are removed before use.
- Legacy records migrate in place by extracting valid restaurant IDs/ZIP and dropping coordinates/payloads; otherwise they are removed.
- Restore hydrates IDs through public restaurant-profile requests. Sign-in, logout pub/sub, and location-consent/mode changes clear the anonymous record.

#### Code Edit 8.1
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 15-998
- Action: replace

Current:
```javascript
localStorage.setItem(ANONYMOUS_SESSION_KEY, JSON.stringify({
  restaurants,
  location: currentLocation,
  zipCode: currentZipCode,
  createdOn: new Date().toISOString(),
}));
```

Proposed:
```javascript
storage.setItem(ANONYMOUS_SESSION_KEY, JSON.stringify({
  version: 2,
  restaurantIds: restaurants.map(({ id }) => id).slice(0, 3),
  zipCode: normalizeZipCode(currentZipCode),
  expiresAt: new Date(Date.now() + ANONYMOUS_TTL_MS).toISOString(),
}));
```

Extract a small testable storage module and subscribe to `auth:logout`. Add expiry, corrupt state, v1 migration, sign-in/logout, ZIP/location-consent, and no-coordinate/no-payload tests. Document behavior in WFL and JavaScript READMEs.

Verification:
- `./gradlew.bat :website:jsTest`
- `rg -n "cbellWflAnonymousSession|latitude|longitude" website/src/main/resources/static/js/whats-for-lunch.js website/src/main/resources/static/js/lib/wfl-anonymous-session.js`

## Code Changes

Eight literal edit boundaries cover account deletion, session mutations/lifecycle/assembly, inventory, dedupe aggregation, URL safety, and anonymous browser persistence. New query/store/policy classes live under the WFL feature rather than expanding controllers.

## Files and Modules

- `website` Java: V011 migration; session model/store/service/assembler/errors; deletion updates; inventory and duplicate query repositories; URL policy; controller/DTO contracts; WFL properties.
- `website` JavaScript/templates: WFL capability/archive UI, safe DOM links, minimal storage module, Back Office inventory/dedupe paging, API routes.
- `website` tests: migration, deletion, atomic concurrency, lifecycle, query counts, inventory/dedupe scale, URL policy, browser storage/UI.
- Builder: implementation plan, test report, spoke update/review, session memory, campaign ledger.

## Unit Testing

1. Add failing deletion preservation and member-cap tests.
2. Add failing atomic join/vote/reset concurrency and stable conflict-contract tests.
3. Add failing lifecycle/revision/audit/migration tests.
4. Add failing session-list query-count tests at 1 and 25 sessions.
5. Add failing inventory pagination/filter/invalid-size tests.
6. Add failing duplicate aggregation/page/apply version tests with unrelated scale rows.
7. Add failing server/browser URL scheme tests.
8. Add failing anonymous storage expiry/corruption/migration/clearing tests.
9. Run focused integration suites, then the full gate.

## Local Testing

1. Use isolated `GRADLE_USER_HOME=A:\GradleUserHomes\cbdev-issues-1280-1289`.
2. Run `./gradlew.bat :website:check --no-daemon --console=plain`.
3. Run the exact JAR on a non-8080 port with explicit disposable Mongo URI/database.
4. Seed pre-V011 sessions/restaurants, apply migration, and verify revision/lifecycle/TTL/query-key/safe-URL state.
5. Exercise creator/participant deletion, 20-member cap, repeated/concurrent joins/votes/resets, expiry/archive boundaries, and bounded audit.
6. Seed 25 sessions and a large restaurant corpus; verify list query counts, inventory/filter cursors, duplicate pages, and exact version conflicts.
7. Exercise public WFL pages with safe/unsafe links and browser storage expiry/migration/clearing.
8. Stop the exact PID, confirm alternate port free, and drop the exact disposable database.

## Validation

- #1280-#1289 acceptance criteria have automated and runtime evidence.
- Shared sessions survive participant deletion with remaining views/votes intact.
- Membership never exceeds 20 under retries/concurrency; full uses stable 409 code.
- Concurrent joins/votes/resets do not lose updates; stale reset conflicts.
- Only hosts can reset picks; API/UI capability and bounded audit agree.
- Expired sessions are read-only/archive-visible and TTL-indexed for deletion.
- One versus 25 history sessions use the same query-group count.
- Inventory and duplicate preview are bounded, stable, filterable/paged, and avoid `findAll()`.
- Restaurant links accept/render only safe HTTP(S) URLs and use DOM creation.
- Anonymous storage contains no coordinates/full restaurant objects, expires in 30 minutes, migrates v1, and clears at auth/consent boundaries.
- Full local/CI/security/production gates pass.

## Rollback or Recovery

- Revert the batch merge as one PR if necessary.
- V011 only adds/backfills bounded fields/indexes and removes unsafe website strings; restore a rejected website only after manual HTTP(S) validation.
- Legacy session fields remain readable during the deployment; new code supplies defaults if V011 retries.
- Use only an exact disposable database and exact alternate PID locally.
- Preserve the dirty authoritative checkout and production port 8080.

## Risks

- Standalone Mongo cannot combine unrelated documents transactionally; session invariants therefore use one-document atomic updates.
- Dynamic map paths require strict account-ID validation before Mongo updates.
- TTL deletion is asynchronous; authorization relies on `activeUntil`, never TTL timing.
- Prefix/exact normalized filters are deliberately chosen so inventory indexes remain usable.
- Duplicate-key migration must not collide with the existing unique normalized-name index; `dedupeKey` is separate and non-unique.
- Browser storage migration must never re-persist legacy coordinates or payload fields.

## Completion Criteria

- V011 applies with reviewed checksum and runtime evidence.
- Focused deletion, concurrency, lifecycle, hydration, pagination, aggregation, URL, and storage suites pass.
- No production WFL inventory/dedupe path calls `restaurantRepository.findAll()`.
- Full check, isolated runtime, review, PR matrix, post-merge main checks, production rotation/migration/index validation, and live acceptance pass.
- #1280-#1289 close with full evidence and Builder artifacts.
