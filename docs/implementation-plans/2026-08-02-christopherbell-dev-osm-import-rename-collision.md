# christopherbell.dev OpenStreetMap Import Rename Collision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. This plan will execute inline because no subagent delegation was requested. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent an OpenStreetMap ID-based rename from aborting an import when another restaurant owns the incoming normalized name.

**Architecture:** Keep the existing unique-name data model and repository boundary. Add one private collision predicate in `RestaurantService`, invoke it before preview classification and before apply mutation, and reuse the existing skipped/unchanged result states rather than adding a new API or schema concept.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, JUnit 5, Mockito, Gradle Wrapper, PowerShell, MongoDB.

## Global Constraints

- Preserve the unique `normalizedName` index; do not add a migration or repository method.
- Do not delete, merge, re-key, or directly rewrite production restaurant records.
- Resolve an ID/name-owner collision before calling `mergeImportedRestaurant` or `restaurantRepository.save`.
- Preview reports the collision as unchanged; apply reports it as skipped existing.
- Expected collisions are throwable-free `DEBUG`; genuine persistence and workflow failures retain causal `ERROR` diagnostics.
- Preserve the dirty authoritative checkout and work only in `A:\Projects\christopherbell.dev-worktrees\restaurant-import-duplicate-name-20260802`.
- Validate runtime behavior on a non-8080 port and an isolated MongoDB database before touching production.

---

## Document Status

`complete`

## Objective

Implement the approved unique-name collision rule with RED/GREEN evidence, documentation, alternate-port runtime proof, pull-request delivery, required CI, exact-SHA deployment, and production recurrence verification.

## Goals

- Reproduce the exact `China Villa` to `Aama's Kitchen` collision in a focused service test.
- Ensure preview and apply make the same collision decision.
- Leave both persisted records unchanged and continue to a later candidate.
- Eliminate the expected duplicate-key error without suppressing unrelated persistence exceptions.
- Complete the normal Builder test-report, review, merge, production, closure, and session-memory workflow.

## Inputs

- Approved specification: `docs/specs/2026-08-02-christopherbell-dev-osm-import-rename-collision.md`.
- Supplied production stack trace from 2026-08-02 12:00:49 CDT.
- Read-only production evidence for `osm:node:8178213204` and `osm:node:13485126044`.
- Current spoke baseline `origin/main` commit `5bd14e994a6130a32166602a6f272581abc53525`.
- Full clean-baseline `:website:test` result: `BUILD SUCCESSFUL` in 4m12s.

## Branch

- Repository: `azurras/christopherbell.dev`.
- Base: refreshed `origin/main` at `5bd14e994a6130a32166602a6f272581abc53525`.
- Branch: `codex/restaurant-import-duplicate-name`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\restaurant-import-duplicate-name-20260802`.

## Non-Goals

- Allowing same-name restaurants by city, coordinates, or address.
- Automatically deleting or merging stale restaurant identities.
- Catching `DuplicateKeyException` around arbitrary import saves.
- Changing the import lease, schedule, preview-token workflow, result DTOs, controller endpoints, or public page behavior.
- Refactoring the large `RestaurantService` outside the four literal edits below.

## Assumptions

- A valid imported restaurant and a persisted ID match both have nonblank IDs after the existing validation boundary.
- `findRestaurantByNormalizedName` remains the authoritative compatibility lookup for indexed and legacy records.
- The unique index remains defense in depth for races and unexpected persistence paths.
- The production catch-up workflow will run after deployment while the prior month remains incomplete.
- Port `8096` and isolated database `christopherbell_osm_collision_test_20260802` will be checked immediately before runtime testing and changed only if already occupied.

## Open Questions

None. The written specification was approved on 2026-08-02.

## Task Breakdown

### Task 1 - Add the rename-collision regression and minimal service fix

Sequence / dependencies:
- Run first; no production edit may occur until Code Edit 1.1 is applied and its focused test is observed failing for the expected preview/apply behavior.
- Apply Code Edits 1.2 through 1.5 only after RED evidence is captured.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Required sub-skill: `superpowers:test-driven-development`; do not edit `RestaurantService.java` before the focused test fails.
- Before-Edit Brief:
  - Behavior: an incoming OpenStreetMap ID whose new normalized name belongs to another persisted ID is classified unchanged/skipped, neither persisted record is mutated, and later candidates still import.
  - Invariants: `normalizedName` remains globally unique; an expected collision never reaches `save`; unrelated remote, lease, validation, and persistence failures remain failures with their existing causes.
  - Boundary/API: change only the private matching flow behind `prepareConfiguredMetroImport` and `applyPreparedImport`; preserve all public methods, repository signatures, DTOs, Mongo indexes, and endpoint contracts.
  - Effects and failures: normalized-name owner lookup is an existing Mongo read; apply mutation and save remain owned by `RestaurantService`; expected collision is a non-throwing branch; unexpected Mongo failures are not caught or downgraded.
  - Tests and evidence: RED is the new JUnit scenario failing because current preview reports updated and current apply mutates/saves the ID match; GREEN is the same scenario passing with a later candidate saved, followed by the complete service and website suites.
- Test mutation check: removing either collision guard, moving the apply guard after merge, comparing only names without IDs, or saving the matched record must fail Code Edit 1.1's literal count/state assertions.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- Lines: after 1074
- Action: add

Proposed:
```java
  @Test
  @DisplayName("OpenStreetMap import: skips an ID rename owned by another restaurant")
  public void testPreparedImport_whenIdRenameCollidesWithAnotherOwner_skipsAndContinues()
      throws Exception {
    var persistedById = RestaurantStub.getRestaurantStub("osm:node:8178213204");
    persistedById.setName("China Villa");
    persistedById.setNormalizedName("china villa");
    persistedById.setDedupeKey("china villa");
    persistedById.getAddress().setCity("Livermore");

    var importedRename = RestaurantStub.getRestaurantStub("osm:node:8178213204");
    importedRename.setName("Aama's Kitchen");
    importedRename.getAddress().setCity("Livermore");

    var normalizedNameOwner = RestaurantStub.getRestaurantStub("osm:node:13485126044");
    normalizedNameOwner.setName("Aama's Kitchen");
    normalizedNameOwner.setNormalizedName("aama's kitchen");
    normalizedNameOwner.setDedupeKey("aama's kitchen");
    normalizedNameOwner.getAddress().setCity("Hayward");

    var laterCandidate = RestaurantStub.getRestaurantStub("osm:node:99999999999");
    laterCandidate.setName("Later Candidate Cafe");

    when(openStreetMapRestaurantClient.getConfiguredMetroRestaurants())
        .thenReturn(List.of(importedRename, laterCandidate));
    when(restaurantRepository.findById(eq(importedRename.getId())))
        .thenReturn(Optional.of(persistedById));
    when(restaurantRepository.findByNormalizedName(eq("aama's kitchen")))
        .thenReturn(Optional.of(normalizedNameOwner));
    when(restaurantRepository.findById(eq(laterCandidate.getId()))).thenReturn(Optional.empty());
    when(restaurantRepository.findByNormalizedName(eq("later candidate cafe")))
        .thenReturn(Optional.empty());
    when(restaurantRepository.findAll()).thenReturn(List.of());
    when(restaurantRepository.save(eq(laterCandidate))).thenReturn(laterCandidate);

    var snapshot = restaurantService.prepareConfiguredMetroImport();
    var result = restaurantService.applyPreparedImport(snapshot, RestaurantImportLeaseGuard.NONE);

    assertEquals(2, snapshot.counts().fetched());
    assertEquals(1, snapshot.counts().created());
    assertEquals(0, snapshot.counts().updated());
    assertEquals(1, snapshot.counts().unchanged());
    assertEquals(2, result.fetched());
    assertEquals(1, result.imported());
    assertEquals(0, result.updated());
    assertEquals(1, result.skippedExisting());
    assertEquals("China Villa", persistedById.getName());
    assertEquals("china villa", persistedById.getNormalizedName());
    assertEquals("Aama's Kitchen", normalizedNameOwner.getName());
    verify(restaurantRepository, never()).save(eq(persistedById));
    verify(restaurantRepository, never()).save(eq(normalizedNameOwner));
    verify(restaurantRepository).save(eq(laterCandidate));
  }
```

Verification:
- Run `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest.testPreparedImport_whenIdRenameCollidesWithAnotherOwner_skipsAndContinues --no-daemon`.
- Expected RED: the test fails because preview reports one update/zero unchanged and apply mutates or saves `persistedById` instead of reporting one skipped-existing candidate.

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 713-727
- Action: replace

Current:
```java
      applyNormalizedName(restaurant);
      var existing = restaurantRepository.findById(restaurant.getId())
          .or(() -> findRestaurantByNormalizedName(restaurant.getNormalizedName()));
      if (existing.isEmpty()) {
        created++;
        addRepresentativeChange(representativeChanges, "CREATE", restaurant);
      } else if (hasSameImportValues(existing.get(), restaurant)) {
        unchanged++;
      } else if (existing.get().getId().equals(restaurant.getId())
          || hasSameNameAndAddress(existing.get(), restaurant)) {
        updated++;
        addRepresentativeChange(representativeChanges, "UPDATE", restaurant);
      } else {
        unchanged++;
      }
```

Proposed:
```java
      applyNormalizedName(restaurant);
      var existingById = restaurantRepository.findById(restaurant.getId());
      if (existingById.isPresent()
          && hasConflictingNormalizedNameOwner(existingById.get(), restaurant)) {
        unchanged++;
        continue;
      }
      var existing = existingById
          .or(() -> findRestaurantByNormalizedName(restaurant.getNormalizedName()));
      if (existing.isEmpty()) {
        created++;
        addRepresentativeChange(representativeChanges, "CREATE", restaurant);
      } else if (hasSameImportValues(existing.get(), restaurant)) {
        unchanged++;
      } else if (existing.get().getId().equals(restaurant.getId())
          || hasSameNameAndAddress(existing.get(), restaurant)) {
        updated++;
        addRepresentativeChange(representativeChanges, "UPDATE", restaurant);
      } else {
        unchanged++;
      }
```

Verification:
- The focused test from Code Edit 1.1 must progress past the preview count assertions after this edit but remain failing until the apply guard is added.

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: 761-773
- Action: replace

Current:
```java
      var existingById = restaurantRepository.findById(restaurant.getId());
      if (existingById.isPresent()) {
        if (mergeImportedRestaurant(existingById.get(), restaurant, true)) {
          restaurantRepository.save(existingById.get());
          updated++;
          log.info("Updated existing OpenStreetMap restaurant id: {}, name: {}",
              existingById.get().getId(), existingById.get().getName());
        } else {
          skippedExisting++;
          log.debug("Skipping unchanged OpenStreetMap restaurant id: {}", restaurant.getId());
        }
        continue;
      }
```

Proposed:
```java
      var existingById = restaurantRepository.findById(restaurant.getId());
      if (existingById.isPresent()) {
        if (hasConflictingNormalizedNameOwner(existingById.get(), restaurant)) {
          skippedExisting++;
          log.debug(
              "Skipping OpenStreetMap restaurant id {} because normalized name {} belongs to another restaurant.",
              restaurant.getId(), restaurant.getNormalizedName());
        } else if (mergeImportedRestaurant(existingById.get(), restaurant, true)) {
          restaurantRepository.save(existingById.get());
          updated++;
          log.info("Updated existing OpenStreetMap restaurant id: {}, name: {}",
              existingById.get().getId(), existingById.get().getName());
        } else {
          skippedExisting++;
          log.debug("Skipping unchanged OpenStreetMap restaurant id: {}", restaurant.getId());
        }
        continue;
      }
```

Verification:
- Re-run the focused test from Code Edit 1.1.
- Expected GREEN after Code Edit 1.4 exists: all preview/apply counts and state assertions pass; only `laterCandidate` is saved.

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- Lines: after 1542
- Action: add

Proposed:
```java
  /** Returns whether another restaurant owns an imported rename before mutation occurs. */
  private boolean hasConflictingNormalizedNameOwner(
      Restaurant persistedById,
      Restaurant imported
  ) {
    if (java.util.Objects.equals(
        persistedById.getNormalizedName(), imported.getNormalizedName())) {
      return false;
    }
    return findRestaurantByNormalizedName(imported.getNormalizedName()).stream()
        .anyMatch(owner -> !java.util.Objects.equals(owner.getId(), persistedById.getId()));
  }
```

Verification:
- Compile and run the focused test from Code Edit 1.1.
- Confirm the existing same-ID/same-name import tests do not add a normalized-name lookup because the fast equality branch returns false.

#### Code Edit 1.5
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`
- Lines: after 78
- Action: add

Proposed:
```markdown
- If an existing OpenStreetMap id is renamed to a normalized name owned by another restaurant, preview reports it unchanged and apply skips it without mutation so the remaining import can complete.
```

Verification:
- Inspect the OpenStreetMap Import section for consistency with the unique-name, same-address, monthly, and startup-catch-up behavior.

- [x] **Step 1: Apply only Code Edit 1.1.**
- [x] **Step 2: Run the focused test and capture expected RED evidence.**
- [x] **Step 3: Apply Code Edits 1.2 through 1.5 without unrelated refactoring.**
- [x] **Step 4: Re-run the focused test and capture GREEN evidence.**
- [x] **Step 5: Run the complete `RestaurantServiceTest` class.**
- [x] **Step 6: Inspect the diff with the coding-standard review rubric and fix blockers only.**
- [x] **Step 7: Commit the cohesive code, test, and feature-documentation change.**

### Task 2 - Run full automated and alternate-port runtime verification

Sequence / dependencies:
- Runs after Task 1 is GREEN and committed.
- Runtime testing starts only after the full automated suite passes.

Implementation notes:
- No repository code changes are planned in this task.
- Run the full website suite with a private Gradle home.
- Use `verify-local-spring-app` before starting or restarting any Spring process.
- Verify port `8096` is free and keep production port `8080` untouched.
- Use MongoDB database `christopherbell_osm_collision_test_20260802`, seed only the two collision documents, and remove only that exact isolated database after evidence is saved.
- Run a loopback OpenStreetMap stub on a separately verified free port that returns the renamed node and one later non-conflicting candidate.
- Start the app with profiles `prod,deploy-smoke`, override `wfl.restaurant-import.monthly.enabled=true` so the startup listener runs, and set `SPRING_MONGODB_URI=mongodb://127.0.0.1:27017`, `SPRING_MONGODB_DATABASE=christopherbell_osm_collision_test_20260802`, `APP_MAIL_ENABLED=false`, a non-placeholder task-only `APP_JWT_SECRET`, `app.federation.discovery-enabled=false`, the loopback stub endpoint, and `--server.port=8096`.

- [x] **Step 1: Run focused service regression.**
  - Command: `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --no-daemon`.
  - Expected: every `RestaurantServiceTest` passes.
- [x] **Step 2: Run the full website suite.**
  - Command: `./gradlew.bat :website:test --no-daemon`.
  - Expected: `BUILD SUCCESSFUL`, zero failures.
- [x] **Step 3: Run repository-level verification.**
  - Command: `./gradlew.bat :website:check --no-daemon` and `git diff --check`.
  - Expected: both exit zero.
- [x] **Step 4: Seed deterministic isolated Mongo data and start the loopback OSM stub.**
  - Inputs: persisted `osm:node:8178213204` as `China Villa`, persisted `osm:node:13485126044` as `Aama's Kitchen`, upstream candidate `8178213204` renamed to `Aama's Kitchen`, and one `Later Candidate Cafe` node.
- [x] **Step 5: Start the app on `http://127.0.0.1:8096` and wait on readiness.**
  - Request: `GET /actuator/health/readiness`.
  - Expected: HTTP 200 with status `UP`.
- [x] **Step 6: Capture runtime import evidence.**
  - Mongo checks: `China Villa` remains unchanged; the existing `Aama's Kitchen` remains unchanged; `Later Candidate Cafe` exists; import state status is succeeded/completed.
  - Log checks: one concise collision skip diagnostic, successful import completion, and no `E11000`, `DuplicateKeyException`, or workflow `ERROR` for the deterministic run.
- [x] **Step 7: Check an unaffected public flow on the alternate port.**
  - Request: `GET /api/whatsforlunch/restaurant/2026-05-17/nearby` with valid deterministic latitude, longitude, and radius inputs supported by the isolated data.
  - Expected: record exact request, status, and bounded JSON response; no server error.
- [x] **Step 8: Stop only the alternate-port app and stub, then drop only `christopherbell_osm_collision_test_20260802`.**
- [x] **Step 9: Save and validate the Builder local app test report before publication.**

### Task 3 - Publish, merge, deploy, verify, and close

Sequence / dependencies:
- Runs only after Task 2 passes and the validated Builder test report checkpoint is committed and pushed.

Implementation notes:
- No new code scope is authorized here; CI failures are handled only when caused by this branch.
- Re-fetch `origin/main` and reconcile safely if it advanced, preserving the focused diff.
- Create a pull request that links the Builder spec/test evidence and describes why arbitrary duplicate-key failures remain visible.
- Wait for Ubuntu, macOS, Windows, dependency-review, CodeQL, and any branch-required checks.
- Use the repository's native Windows production deployment workflow and respect `deploy.lock`; never weaken production ACLs.
- Deploy only the exact merged SHA after alternate-port validation and required CI pass.

- [x] **Step 1: Perform final diff review and verification-before-completion.**
- [x] **Step 2: Push `codex/restaurant-import-duplicate-name` and open a ready pull request.**
- [x] **Step 3: Wait for required CI, diagnose in-scope failures, and merge only when green.**
- [x] **Step 4: Confirm the merge SHA and deploy that exact commit.**
- [x] **Step 5: Verify `ChristopherBellDev`, MongoDB, cloudflared, and media worker service states plus local/public HTTP 200, readiness `UP`, and security headers.**
- [x] **Step 6: Verify the production catch-up import completes, the durable import month advances, and the supplied duplicate-key signature does not recur during a bounded observation window.**
- [x] **Step 7: Confirm the two existing restaurant documents were not directly rewritten by the fix outside normal import behavior.**
- [x] **Step 8: Save spoke update/review, close the source task, save session memory, refresh Builder indexes, validate hub state, close the work record, and commit/push all required Builder checkpoints.**

## Code Changes

- `RestaurantServiceTest.java`, add after line 1074: exact regression for an ID-based upstream rename colliding with another normalized-name owner and proof that a later candidate proceeds.
- `RestaurantService.java`, replace lines 713-727: preview collision classification before general existing-record classification.
- `RestaurantService.java`, replace lines 761-773: apply collision skip before merge/save with throwable-free debug logging.
- `RestaurantService.java`, add after line 1542: one private predicate that protects the unique-name/mutation invariant and avoids extra lookup for unchanged normalized names.
- Restaurant feature `README.md`, add after line 78: durable documentation of the collision behavior.

## Files and Modules

- Modify `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`.
- Modify `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`.
- Modify `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`.
- No new source file, repository method, DTO, controller route, migration, configuration property, or dependency.

## Unit Testing

- RED/GREEN command: `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest.testPreparedImport_whenIdRenameCollidesWithAnotherOwner_skipsAndContinues --no-daemon`.
- Focused regression command: `./gradlew.bat :website:test --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantServiceTest --no-daemon`.
- Full regression command: `./gradlew.bat :website:test --no-daemon`.
- Repository verification command: `./gradlew.bat :website:check --no-daemon`.
- Required behavioral assertions: preview created `1`, updated `0`, unchanged `1`; apply imported `1`, updated `0`, skipped existing `1`; old and owner records unchanged; later candidate saved.

## Local Testing

- Invoke `verify-local-spring-app` and use alternate port `8096` after confirming it is unoccupied.
- Use a loopback OSM response stub and isolated MongoDB database `christopherbell_osm_collision_test_20260802` so the live production collection is never mutated.
- Seed the exact two persisted records and return the exact renamed plus later candidate input.
- Capture readiness URL/status/body, WFL request input/status/body, exact Mongo document states, import status, relevant log lines, and absence of `E11000`/`DuplicateKeyException`.
- Stop only task-owned processes and remove only the exact isolated database after the test report is saved.

## Validation

- Mechanical implementation-plan validation passes before execution.
- Human-readable plan review reports no blockers.
- RED fails for the intended missing collision branch; GREEN passes after the minimal implementation.
- Focused, full, and `:website:check` Gradle commands pass.
- Alternate-port production-profile import completes with correct state and no duplicate-key error.
- PR required checks pass, merge is confirmed, and the exact merged SHA is deployed.
- Production health and post-deploy recurrence checks pass before closure.

## Rollback or Recovery

- Before merge: revert only the focused branch commit or amend it; do not touch the authoritative checkout.
- After merge: create a revert of the focused PR, pass required checks, and deploy the exact prior known-good or revert SHA through the normal locked deployment workflow.
- Runtime-test cleanup: stop only recorded task-owned process IDs and drop only `christopherbell_osm_collision_test_20260802` after resolving the database name literally.
- Production data recovery is not expected because the fix performs no migration or direct data rewrite; if an unexpected import mutation is observed, stop further imports, preserve logs/state, and use the existing MongoDB backup/restore runbook rather than ad hoc edits.

## Risks

- Preview/apply drift: mitigated by one shared predicate and one test exercising both phases.
- Extra lookup cost: limited to ID matches whose normalized name actually changed; unchanged ID/name records return before repository lookup.
- Stale `China Villa` display remains: accepted by the approved non-destructive scope and documented for future administrative reconciliation.
- Race after lookup: MongoDB uniqueness still rejects a competing write, and arbitrary persistence failures remain visible rather than being suppressed.
- Production catch-up may depend on upstream availability: verify durable status and distinguish an upstream outage from recurrence of this collision.

## Completion Criteria

- The new regression was observed RED and then GREEN.
- The focused and full automated suites, repository check, and diff check pass.
- Alternate-port runtime evidence proves skip/continue/completion and absence of the duplicate-key signature.
- The implementation is committed, pushed, reviewed, merged after required CI, and deployed as the exact merged SHA.
- Production services, readiness, public response, security headers, catch-up completion, and bounded recurrence window pass.
- Builder test report, spoke update/review, closure, session memory, work record, and indexes are saved, validated, committed, and pushed.
