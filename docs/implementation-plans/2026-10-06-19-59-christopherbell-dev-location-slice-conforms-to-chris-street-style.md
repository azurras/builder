# Location Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the location (ZIP coordinate) slice conforms to write-chris-street-style-code, and ZIP lookup, Census import and the ZIP coordinates page behave exactly as before.

## Background
This is slice 4 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `07859a2f` found the following:

1. **Hidden mutation.** In `ZipCoordinateService`, a boolean `mergeChangedValues(existing, imported)` both answers whether a row changed and mutates the stored row.
2. **Long import method.** One method classifies rows, writes them and records state.
3. **Side-effecting stream.** The checksum updates a digest inside a stream `forEach`.
4. **Vague lookup names.** `getZipCoordinate` and `normalizeZipCode` do not say what they return.
5. **Unclear reader names.** The Gazetteer reader uses `read`, `coordinate(line)` and `e`.
6. **Mongo adapters.** They pack methods onto single lines and fill lists with `forEach` side effects.
7. **Page script.** It names module elements `form`, `input`, `button` and `result`, and its catch variable `err`.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- ZIP lookup (200, 400, 404), admin-only import and the page behave as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the `ZipCoordinate` and `ZipCoordinateImportState` documents to records | They are persisted Mongo documents with audit fields and existing data; a mapping change belongs to a data migration |
| Changing the import counts, checksum format or stored state id | Stored checksums would stop matching and force a full re-import |
| Moving `/zip-coordinates` routing out of `ToolsViewController` | Belongs to the view slice |
| Renaming `RestaurantService.getZipCoordinateOrigin` | Belongs to the whatsforlunch slice; only its call to the renamed lookup changes here |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for each slice file and each caller change |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the packaged candidate: imports the bundled Census data as an ADMIN, re-imports as a no-op with the same checksum, returns the coordinate for `78701` and `78701-1234`, returns 400 for `zip` and 404 for an absent ZIP, rejects an anonymous import, and serves `/zip-coordinates` with its script. The error envelopes are byte-identical to production. All of this is recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 4; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `07859a2f`:
  - All `location` Java, plus `location/README.md` and `location/model/README.md`.
  - `ZipCoordinateServiceTest`, `ZipCoordinateGazetteerReaderTest`, `LocationControllerTest` and `LocationControllerSecurityTest`.
  - `static/js/zip-coordinates.js`, `templates/zip-coordinates.html`, `zip-coordinates.test.js` and `zip-coordinates-browser.test.js`.
  - The caller `whatsforlunch/restaurant/RestaurantService` and `RestaurantServiceTest`, plus `ToolsViewController`.

## Branch
`claude/style-location-20261006` from spoke `origin/main` `07859a2f`, in a linked worktree.

## Assumptions
- Lombok setters on the persisted `ZipCoordinate` stay the supported way to update a stored row in place, keeping its audit dates.

## Open Questions
None.

## Design
The import is split into "plan, then apply". `planCensusImport` classifies imported rows against the stored ones and returns a private `CensusImportPlan` record: rows to save, stale rows, and counts. The import method then applies saves and deletes and records state. `hasSameImportedValues` is a pure question. `copyImportedValues(imported, stored)` is the visible in-place update. The checksum builds sorted row fingerprints and then updates the digest in a loop. Lookup becomes `findCoordinateForZip(requestedZipCode)` with `fiveDigitZipCodeOf`, and the reader exposes `readCoordinatesFrom(gazetteerResource)`. Both Mongo adapters use ordinary formatting and loops.

| Alternative | Why not |
|---|---|
| Keep one import method and only rename locals | The method mixes classification, writes and state; separating the plan makes the effects visible |
| Return new coordinate objects instead of updating stored rows | Would lose the stored audit dates or need a persistence mapping change |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/location/zip/ZipCoordinateService.java` | changed | Plan, then apply; pure comparison and explicit copy; loop for the digest; `findCoordinateForZip` (rules 1, 3, 7, 9) |
| `website/src/main/java/dev/christopherbell/location/zip/LocationController.java` | changed | `findZipCoordinate(@PathVariable("zipCode") requestedZipCode)`; `ResponseEntity.ok` (rule 1) |
| `website/src/main/java/dev/christopherbell/location/zip/ZipCoordinateGazetteerReader.java` | changed | `readCoordinatesFrom`, `coordinateFromRow`, named failures, precompiled patterns (rules 1, 2, 8) |
| `website/src/main/java/dev/christopherbell/location/zip/MongoZipCoordinateRepository.java` | changed | Loops and role names (rules 2, 9) |
| `website/src/main/java/dev/christopherbell/location/zip/MongoZipCoordinateImportStateRepository.java` | changed | Readable formatting and parameter names (rule 2) |
| `website/src/main/java/dev/christopherbell/location/zip/ZipCoordinateRepository.java` | conforming | No change |
| `website/src/main/java/dev/christopherbell/location/zip/ZipCoordinateImportStateRepository.java` | conforming | No change |
| `website/src/main/java/dev/christopherbell/location/model/ZipCoordinate.java` | conforming | Persisted document; see Non-Goals |
| `website/src/main/java/dev/christopherbell/location/model/ZipCoordinateImportState.java` | conforming | Persisted document; see Non-Goals |
| `website/src/main/java/dev/christopherbell/location/model/ZipCoordinateDetail.java` | conforming | Record |
| `website/src/main/java/dev/christopherbell/location/model/ZipCoordinateImportResult.java` | conforming | Record |
| `website/src/main/java/dev/christopherbell/location/README.md`, `location/model/README.md`, `location/zip/README.md` | conforming | No renamed names are documented |
| `website/src/main/resources/static/js/zip-coordinates.js` | changed | Role names for elements, helpers and the failure (rules 1, 2) |
| `website/src/main/resources/templates/zip-coordinates.html` | conforming | No change |
| `website/src/test/java/dev/christopherbell/location/*Test.java` (4 files) | changed | Follow the renamed methods |
| `website/src/test/js/zip-coordinates.test.js`, `zip-coordinates-browser.test.js` | conforming | Exported names unchanged |
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`, `RestaurantServiceTest.java` | changed (call site) | Use `findCoordinateForZip` |

## Task Breakdown

### Task 1 - Conform the location slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Slice 2 merged |
| **Files** | As listed in Expected Changes |
| **Symbols** | `ZipCoordinateService.importCensusZipCoordinates`, `planCensusImport`, `CensusImportPlan`, `hasSameImportedValues`, `copyImportedValues`, `datasetChecksum`, `findCoordinateForZip`, `fiveDigitZipCodeOf`; `LocationController.findZipCoordinate`; `ZipCoordinateGazetteerReader.readCoordinatesFrom`, `coordinateFromRow`; the Mongo adapters; `zip-coordinates.js` internals |
| **Inspection** | All files in Inputs at `07859a2f` |
| **Behavior** | Same lookup normalization and errors, same import counts, ordering of saved rows, checksum and no-op path, same page behavior |
| **Invariants** | Route `/api/location/zip/{zipCode}`, admin-only import, JSON shapes, stored fields and state id `census-zcta` unchanged |
| **Boundary/API** | `ZipCoordinateService` lookup renamed with its only cross-slice caller updated |
| **Effects and failures** | Saves happen before deletes, then state is saved, as before; reader failures keep their messages and causes |
| **Tests and evidence** | Existing location, restaurant and JS tests pass with renamed calls; runtime import, re-import and lookups |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | `ZipCoordinateServiceTest`, `ZipCoordinateGazetteerReaderTest`, `LocationController*Test`, `RestaurantServiceTest`, JS tests | verify-local-app on isolated MongoDB `test`: make an ADMIN through a test-profile path or an existing endpoint, import Census data, import again (no-op with the same checksum), look up `78701`, `78701-1234`, `zip` (400) and `00000` (404), make an anonymous import (401 or 403), and load `/zip-coordinates` |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data or schema change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Import counts or the saved-row order change | Low | The existing `importRefreshCreatesUpdatesLeavesUnchangedAndDeletesStaleCensusRows` test, plus a runtime re-import that must be a no-op |
| No ADMIN can be created locally to exercise import | Medium | Use an existing supported path. If none exists, record the import as covered by tests and say so in the report |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the permission slice's check ran.
- **Reason:** I worked ahead while CI and checks for earlier slices ran.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
