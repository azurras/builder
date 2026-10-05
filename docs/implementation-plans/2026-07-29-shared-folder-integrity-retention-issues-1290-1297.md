# Shared-Folder Integrity and Retention Issues 1290-1297 Implementation Plan

## Document Status

complete

## Objective

Resolve #1290-#1297 with asynchronous bounded catalog generations, post-commit invalidation, stable search cursors, terminal download auditing, optimistic radio transitions using trusted Music metadata, and cleanup-before-TTL retention.

## Goals

- Remove recursive filesystem enumeration from request threads and bound every scan resource.
- Preserve and expose last-known-good, partial, stale, and building catalog state.
- Page search deterministically with a generation-bound opaque cursor and repeated authorization.
- Invalidate after every successful visible mutation and durable upload finalization.
- Audit completed, aborted, and failed transfers with actual bytes served.
- Make radio transitions safe across instances and prevent browsers from controlling duration.
- Retain completed uploads briefly and clean terminal media artifacts before diagnostic TTL.

## Inputs

- Focused spec `docs/specs/2026-07-29-shared-folder-integrity-retention-issues-1290-1297.md`.
- Trusted issues #1290-#1297 by `azurras`; no untrusted comments or attachments.
- Refreshed `origin/main` commit `b28031d535effef1fcbd547ba8f7dffdd4e76193`.
- Mandatory test-first execution and `write-chris-street-style-code`.

## Branch

`codex/issues-1290-1297-20260729` in `A:\Projects\christopherbell.dev-worktrees\issues-1290-1297-20260729`, based on `b28031d5`.

## Non-Goals

- Persist a second full catalog, replace capability boundaries/Music indexing, trust unknown client duration, TTL active/recoverable work, or change authorization policy.

## Assumptions

- `app.music.root` equals `app.shared-folder.root/Music`; exact-token READY `music_tracks` are trusted duration data.
- Changed catalog generations invalidate old cursors with a stable 409.
- Transfer audit is best effort; media `deleteAt` is absent until artifact cleanup succeeds.

## Open Questions

None. Standing user approval covers the focused spec.

## Files and Modules

- Catalog/config/API: catalog service, new properties/status/cursor types, read controller, response model, API/JavaScript/template.
- Mutation invalidation: write/admin controllers.
- Streaming audit: new audited Resource/InputStream and audit recorder.
- Radio: radio document/service, trusted duration resolver, Music repository read.
- Retention: upload session/service, media job/service, maintenance, properties, migration V012.
- Tests: catalog/controller/browser/radio/upload/media/maintenance/migration/integration suites.

## Code Changes

The ordered edits below keep filesystem enumeration, cursoring, transfer observation, radio compare-and-set, and retention in separate owning boundaries. Each edit begins with a failing focused test.

## Task Breakdown

### Task 1 - Bounded asynchronous catalog generations (#1290)

Add validated entry/directory/depth/time/refresh/page limits and one coalescing worker. Requests only read immutable state and trigger work; cold start returns BUILDING. Inaccessible children mark partial, while root/systemic failure retains the prior snapshot.

Sequence / dependencies:
- First. Tasks 2 and 3 consume the generation/snapshot/invalidation boundary.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 1 test/code edit.

Before-Edit Brief:
- Behavior: scans run only on the catalog worker and publish immutable bounded generations.
- Invariants: one active worker, finite budgets, no request-thread listing, prior good snapshot survives failure.
- Boundary/API: catalog callers receive status plus snapshot data; filesystem access remains behind `SharedFolderBrowserService`.
- Effects and failures: invalidation schedules/cancels work; inaccessible children are partial, systemic failure is fixed-category and non-destructive.
- Tests and evidence: deterministic executor/clock tests prove every bound, cancellation, fallback, and request-thread isolation.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderCatalogService.java`
- Lines: 20-132
- Action: replace

Current:
```java
CatalogSnapshot refreshed = new CatalogSnapshot(now, listBreadthFirst());
snapshot = refreshed;
return refreshed;
```

Proposed:
```java
public CatalogView current() {
  triggerRefreshIfNeeded();
  CatalogSnapshot current = snapshot.get();
  return current == null ? CatalogView.building(requestedGeneration.get())
      : current.view(clock.instant());
}
```

Add `SharedFolderCatalogProperties` before line 1, status/failure types, a named single-worker executor in `SharedFolderConfiguration.java:1-14`, explicit defaults in `application.yml:102-120`, and profile overrides. The worker checks entry, directory, depth, deadline, generation, and interruption bounds.

Verification:
- `./gradlew.bat :website:test --tests '*SharedFolderCatalogServiceTest' --tests '*SharedFolderCatalogPropertiesTest'`

Tests in `SharedFolderCatalogServiceTest.java:22-161` cover large trees, every budget, inaccessible continuation, timeout, cancellation, stale-result suppression, cold BUILDING, failure fallback, and no request-thread `browser.list`.

### Task 2 - Stable paginated search (#1292)

Sort by normalized path, exact path, type, and observation token. Encode generation plus last boundary in Base64URL. Default bounded pages, repeat `requireRead()` on every page, return 400 for malformed cursor and `SHARED_FOLDER_CATALOG_CHANGED` 409 for a replaced generation. Browser Load More appends only the same generation and exposes freshness/partial state.

Sequence / dependencies:
- After Task 1 immutable generations and before mutation invalidation acceptance.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 2 test/code edit.

Before-Edit Brief:
- Behavior: each page is a deterministic slice of one immutable generation with a bounded successor cursor.
- Invariants: size is bounded, cursor cannot cross generations, authorization repeats, no absolute path leaves the server.
- Boundary/API: `/search` adds cursor/size and replaces `truncated` with cursor/status fields; browser validates before render.
- Effects and failures: reads only; malformed cursor is 400 and unavailable generation is stable 409.
- Tests and evidence: service/controller/browser tests cover duplicate names, >200 matches, mutations between pages, auth, and append cancellation.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderSearchResponse.java`
- Lines: 1-11
- Action: replace

Current:
```java
public record SharedFolderSearchResponse(
    String query, List<SharedDirectoryEntry> entries, boolean truncated) {}
```

Proposed:
```java
public record SharedFolderSearchResponse(
    String query, List<SharedDirectoryEntry> entries, String nextCursor,
    long generation, Instant snapshotCreatedAt,
    CatalogFreshness freshness, boolean partial) {}
```

Add request/cursor/error types; update `SharedFolderReadController.java:77-93` with cursor/size parameters; update `lib/shared-folder.js:270-310`, `shared-folder.js:712-817`, API URL, and template with generation-safe Load More/status text.

Verification:
- `./gradlew.bat :website:test --tests '*SharedFolderCatalogServiceTest' --tests '*SharedFolderReadControllerTest'`
- `node --test website/src/test/js/shared-folder.test.js`

### Task 3 - Post-commit catalog invalidation (#1291)

Advance catalog generation only after successful create, rename, move, recycle, restore, purge, and durable COMPLETED upload finalization. Status/chunk/cancel/failure paths do not invalidate. One invalidation cancels obsolete scan work and coalesces the newest generation.

Sequence / dependencies:
- After Task 1 invalidation exists and Task 2 cursor semantics define the changed-generation response.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 3 test/code edit.

Before-Edit Brief:
- Behavior: every committed visible tree change advances generation before the successful HTTP response returns.
- Invariants: failed/non-visible operations never invalidate; newest generation wins; last good data remains available.
- Boundary/API: write/admin controllers call a narrow invalidation interface after service success.
- Effects and failures: catalog refresh is asynchronous and cannot roll back a completed filesystem mutation.
- Tests and evidence: controller tests verify every mutation, failure suppression, immediate generation change, and refresh-failure fallback.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderWriteController.java`
- Lines: 32-153
- Action: replace

Current:
```java
SharedDirectoryEntry result = mutations.rename(request);
return ResponseEntity.ok().body(result);
```

Proposed:
```java
SharedDirectoryEntry result = mutations.rename(request);
catalog.invalidate(SharedFolderCatalogInvalidation.MUTATION);
return ResponseEntity.ok().body(result);
```

Inject the invalidation boundary. Apply the same post-success rule in `SharedFolderAdminController.java:24-101` for restore/purge and in upload completion only when the returned state is COMPLETED.

Verification:
- `./gradlew.bat :website:test --tests '*SharedFolderWriteControllerTest' --tests '*SharedFolderCatalogServiceTest'`

### Task 4 - Transfer terminal auditing (#1293)

Wrap the actual Resource/InputStream without buffering. Count reads and emit exactly one COMPLETED at advertised length, ABORTED on early close, or FAILED on I/O/short read. Capture safe account/client facts before streaming and deduplicate range/media noise through the bounded logical-access window.

Sequence / dependencies:
- Independent of Tasks 1-3; complete before runtime transfer acceptance.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 4 test/code edit.

Before-Edit Brief:
- Behavior: audit terminal outcome follows actual stream consumption and byte count.
- Invariants: zero buffering, one callback, safe captured identity/path, audit degradation never breaks transfer.
- Boundary/API: Resource metadata delegates unchanged; recorder accepts a closed terminal outcome contract.
- Effects and failures: exact read records completion, early close records abort, I/O/short read records failure; sink exceptions are swallowed/logged safely.
- Tests and evidence: full/range/abort/short/failure/dedup tests inspect recorded actions, outcomes, and bytes.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderAuditedResource.java`
- Lines: before 1
- Action: add

Current:
```text
No Resource observes the terminal state of Spring's response stream.
```

Proposed:
```java
final class SharedFolderAuditedResource extends AbstractResource {
  public InputStream getInputStream() {
    return new TerminalAuditInputStream(
        delegate.getInputStream(), expectedBytes, terminalCallback);
  }
}
```

Delegate metadata/content length without opening the stream. Update `SharedFolderReadController.java:119-153` to wrap the resource and `SharedFolderAuditRecorder.java:70-110` to record captured terminal facts by account/action/path with bounded deduplication.

Verification:
- `./gradlew.bat :website:test --tests '*SharedFolderAuditedResourceTest' --tests '*SharedFolderReadControllerTest' --tests '*SharedFolderAuditRecorderTest'`

### Task 5 - Radio optimistic CAS and trusted duration (#1294, #1295)

Add Mongo versioning and bounded duplicate-key/optimistic-lock retries. Compute pure transition candidates and return only the committed version. Map `Music/...` to `music_tracks.path`; accept duration only from a READY/present/exact-observed-token Music record. Reject gross forged reports; matching reports trigger evaluation but persist server duration. Unknown metadata stays playable without auto-advance.

Sequence / dependencies:
- Uses Task 1 catalog track pool; otherwise independent and precedes V012 legacy-field cleanup.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 5 test/code edit.

Before-Edit Brief:
- Behavior: one versioned station transition commits across instances; trusted Music metadata owns timing.
- Invariants: bounded retries, monotonic sequence, no whole-document blind overwrite, no browser-derived persisted duration.
- Boundary/API: existing current/report routes remain; document gains version and resolver reads only ready exact-token Music rows.
- Effects and failures: optimistic conflicts retry; forged reports reject; unknown metadata leaves duration null; exhaustion is stable unavailable.
- Tests and evidence: two service instances race current/report against CAS storage and cover trusted, forged, stale, unknown, and exhaustion cases.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/radio/SharedFolderRadioService.java`
- Lines: 24-255
- Action: replace

Current:
```java
synchronized (stationLock) {
  SharedFolderRadioDocument current = repository.findById(ID).orElse(null);
  return transition(tracks, current, now, request.durationSeconds());
}
```

Proposed:
```java
return retryTransition(tracks, current -> transition(
    current, tracks, clock.instant(), durations.trusted(activeTrack, request)));
```

Add `@Version Long version` and remove browser-derived known-duration cache in `SharedFolderRadioDocument.java:13-126`. Add a resolver backed by `MusicTrackRepository.findByPath` and `MusicTrack.playable(observedToken)`, a fixed tolerance, and max CAS attempts.

Verification:
- `./gradlew.bat :website:test --tests '*SharedFolderRadioServiceTest' --tests '*SharedFolderReadControllerTest'`

Tests use two service instances and a CAS-enforcing repository for concurrent current/report calls, retry exhaustion, forged short/long reports, trusted exact duration, stale token, and unknown format.

### Task 6 - Completed upload retention (#1296)

Add a configurable short completion-history window. Set upload `deleteAt` only after durable COMPLETED transitions; clear/omit it for ACTIVE, APPENDING, FINALIZING, CANCEL_PENDING, recovery, CANCELLED, and EXPIRED paths.

Sequence / dependencies:
- After catalog invalidation identifies durable completion; V012 in Task 7 supplies legacy/index state.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 6 test/code edit.

Before-Edit Brief:
- Behavior: successfully completed upload metadata expires after a short window.
- Invariants: active/recoverable/finalizing work has no TTL; retry completion keeps a stable deadline; visible file durability precedes TTL assignment.
- Boundary/API: persistence model/properties change; public upload status remains compatible.
- Effects and failures: completion writes `deleteAt`; recovery clears it; Mongo TTL performs eventual metadata removal only.
- Tests and evidence: transition tests inspect every state, retry behavior, deadline, and absence on recoverable sessions.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadSession.java`
- Lines: 22-57
- Action: replace

Current:
```java
@Indexed private Instant expiresAt;
private SharedFolderUploadState state;
private Instant updatedAt;
```

Proposed:
```java
@Indexed private Instant expiresAt;
@Indexed(name = "shared_upload_delete_ttl", expireAfter = "0s")
private Instant deleteAt;
private SharedFolderUploadState state;
private Instant updatedAt;
```

Add completion retention plus a compatibility constructor to `SharedFolderProperties.java:14-38`. Update all completion/recovery sites in `SharedFolderUploadService.java:425-505,902-952,1120-1250,1815-1855`.

Verification:
- `./gradlew.bat :website:test --tests '*SharedFolderUploadServiceTest'`

### Task 7 - Terminal media cleanup and migration (#1297)

Give FAILED, CANCELED, INSUFFICIENT_SPACE, and TIMED_OUT state-specific `cleanupAfter`; bounded maintenance removes descriptor/partial/status/cancel artifacts and releases identity/reservation state. Only then redact owner/source/cache fields, set `artifactsCleaned`, and arm diagnostic `deleteAt`. Failure retains the full document with no TTL. READY and active jobs keep existing semantics.

Sequence / dependencies:
- After Task 5 final radio shape and Task 6 upload model; final code task before integration.

Required skill: `write-chris-street-style-code`; invoke it immediately before the first Task 7 test/code edit.

Before-Edit Brief:
- Behavior: terminal non-ready artifacts clean on state-specific deadlines, then redacted diagnostics expire.
- Invariants: bounded pages, idempotent deletion, active/READY immunity, no TTL before cleanup, reservation/private identity cleared after success.
- Boundary/API: media persistence/properties/repository/maintenance and additive V012; public descriptors remain bounded/compatible.
- Effects and failures: maintenance deletes owned artifacts then redacts/arms TTL; any failure retains retryable full metadata and no TTL.
- Tests and evidence: per-state, crash-before/after, retry, redaction, reservation, migration checksum/index/backfill/idempotence tests.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/sharedfolder/media/MediaPlaybackService.java`
- Lines: 170-570
- Action: replace

Current:
```java
private void terminal(MediaJob job, MediaJobStatus status, String category, Instant now) {
  job.setStatus(status);
  job.setActiveCacheKey(null);
  jobs.save(job);
}
```

Proposed:
```java
private void terminal(MediaJob job, MediaJobStatus status, String category, Instant now) {
  job.setStatus(status);
  job.setCleanupAfter(now.plus(properties.cleanupRetention(status)));
  job.setDeleteAt(null);
  jobs.save(job);
}
```

Add `cleanupAfter`, `artifactsCleaned`, and TTL `deleteAt` to `MediaJob.java:15-37`; per-state cleanup/diagnostic retention with compatibility constructor to `SharedFolderMediaProperties.java:14-33`; bounded `cleanupTerminalJobs()`; and a lease-renewed step in `SharedFolderMaintenanceService.java:48-87` before cache eviction.

Add `V012RetainSharedFolderWork.java` before line 1 to create upload/media TTL/query indexes, backfill only COMPLETED uploads and non-ready terminal media in bounded batches, and unset legacy radio duration cache. Seal checksum/idempotence/index/active-exclusion tests.

Verification:
- `./gradlew.bat :website:test --tests '*MediaPlaybackServiceTest' --tests '*SharedFolderMaintenanceServiceTest' --tests '*V012*'`

## Unit Testing

- Observe focused red failure before each production edit and rerun its exact verification after the smallest implementation.
- Catalog: all budgets, cancellation, partial/failure fallback, duplicate-name pages, and mutation between pages.
- Web/browser: authorization per page, stable errors, Load More/status, cancellation, and post-commit invalidation.
- Streaming: full, partial, exact bytes, early close, short read, I/O failure, and deduplication.
- Radio: two-instance races, bounded retry, forged/trusted/stale/unknown duration.
- Retention: per-state deadlines, active immunity, crash before/after cleanup, idempotent retry, redaction, reservation release, and TTL only after success.

## Local Testing

- Run `./gradlew.bat :website:check --no-daemon --console=plain`, using isolated Gradle state if Windows locks recur.
- Build the exact JAR and run on a non-8080 port against a disposable Mongo database and temporary shared/system/Music tree.
- Exercise large/partial scans, first/next pages, mutation invalidation, transfer outcomes, concurrent radio, forged/trusted duration, upload TTL, media cleanup, migration/indexes, and authorization.
- Stop the exact PID; prove the port free; remove only validated temporary tree/database; prove production port 8080 stayed untouched.

## Validation

- Review the diff for request-thread traversal, path leaks, cursor instability, missing authorization, duplicate audit, lost CAS, browser-controlled duration, and premature TTL.
- Run focused suites, full gate, `git diff --check`, exact-JAR acceptance, and security scan.
- Open one PR; require Ubuntu/macOS/Windows, dependency review, and all CodeQL languages.
- Merge only when green; verify issue closure, post-merge checks, deployment/listener rotation, exact merged behavior, health, migration/index/deadline state, services, and external reachability.

## Rollback or Recovery

- Catalog failure retains the prior immutable snapshot; cursor conflict restarts search without mutation.
- CAS exhaustion leaves the committed radio document unchanged.
- Upload TTL is absent outside durable COMPLETED.
- Media cleanup failure leaves the full descriptor and no `deleteAt`, allowing retry without orphaning artifacts.
- V012 is additive, bounded, and idempotent. On checksum/partial-state rejection, keep the prior release and correct code rather than editing records manually.

## Risks

- Invalidation churn: coalesce newest generation and cancel stale scans.
- Cursor interruption: explicit 409 instead of silent skip/duplication.
- Stream-close variance: complete at exact expected bytes and atomically guard one callback.
- CAS reselection: recompute from the newly observed version and return only saved state.
- Music metadata lag: require exact observation token; unknown is safer than browser authority.
- TTL orphaning: no media `deleteAt` before cleanup success.
- Config compatibility: explicit defaults and overloaded constructors.

## Completion Criteria

- Every acceptance statement in #1290-#1297 has focused automated and alternate-port runtime evidence.
- No recursive catalog work runs on request threads; search is bounded, deterministic, authorized, and safely invalidated.
- Transfer audits distinguish terminal outcomes with actual bytes.
- Concurrent radio retains one versioned sequence and only trusted duration.
- Active/recoverable work has no TTL; terminal artifacts are cleaned before redacted diagnostic TTL.
- Full tests, CI/CodeQL, merge, issue closure, production checks, exact cleanup, and Builder closeout pass.
