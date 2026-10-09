# Music Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the Music slice conforms to write-chris-street-style-code, and Music access, catalog, playback, queue, radio, playlists, preferences and metadata edits behave as before.

## Background
This is slice 13 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `be88be27` covered:
- The 82 main Java files, the README and the 25 test files.
- `music.js`, `lib/music.js`, `music.test.js`, `music.html` and `music.css`.

The code already has validated records, bounded queries and fail-closed file handling. The remaining gaps are:

1. **Hidden time.**
   - `MusicMetadataFileStore.markReplacement` reads `System.currentTimeMillis()`.
   - Three beans are built with `Clock.systemUTC()` instead of the application `Clock`.
2. **Boolean parameters.** `updatePreferences` takes four booleans through the service and the repository.
3. **Null where neighbors return `Optional`.**
   - `MusicRadioService.activeTrack` and `selectNext` return null.
   - `FfprobeMusicProbe.firstStream` returns null.
   - `MongoMusicAccessAttemptRepository.record` uses `isPresent()` then `get()`.
4. **Smaller issues:**
   - Fully qualified names in twelve main files and nine test files.
   - A repeated `artwork != null` branch.
   - One-line Mongo adapter methods.
   - An unused import and crammed helpers in `music.js`.
   - Positional `text[0]`–`text[4]` fields in `lib/music.js`.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The Music page, entry probe and protected API behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Brace style on one-line `if` statements | The repository's formatter accepts them and the guide sets no rule; churn without readability gain |
| Changing the preference request JSON (`expectedFavorite`, `expectedExcludedFromRadio`, `favorite`, `excludedFromRadio`) | Public contract with `music.js`; the request maps itself to two values |
| Logging inside the documented best-effort cleanups | Behavior change outside conformance |
| The radio loop's nullable `state` before the first transition | It is the persisted "no station yet" case; converting it is a larger redesign of the transition loop |
| Production music PowerShell and V014 migration tests | Slices 24 and 18 |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` and `node --test src/test/js/music.test.js` pass, and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with a disposable USER, the published test report records that: the Music page and both scripts are served; the entry probe answers anonymous and permissionless users as before; anonymous catalog, radio and queue reads match production; a USER without Music permission cannot read, change preferences, queue or read the access log |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 13; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `be88be27`:
  - All Music sources, tests, scripts, template and styles.
  - The callers in `architecture/MusicAndLunchMongoContractTest`, `MusicAndLunchMutationSafetyMongoTest` and `MusicComponentWiringTest`.
  - `ApplicationClockConfiguration`, which provides `Clock.systemUTC()`.
- **Production (read-only GETs, 2026-10-09):** anonymous catalog, radio and queue return 403; `/music` returns 200.

## Branch
`claude/style-music-20261009` from spoke `origin/main` `be88be27`.

## Assumptions
- The application `Clock` bean stays `Clock.systemUTC()`, so injecting it changes no runtime behavior.

## Open Questions
None.

## Design
- **Time:**
  - `MusicMetadataFileStore` takes a `Clock`.
  - `MusicCatalogConfiguration` passes the application `Clock` to the reconciler, file store and metadata service.
  - `MusicAccessAuditRecorder` has one constructor `(attempts, clock)`, and the wiring test asserts that shape.
- **Preferences:**
  - `MusicTrackPreferences(favorite, excludedFromRadio)` replaces the four booleans in `MusicLibraryService.updatePreferences` and `MusicTrackRepository.updatePreferences`.
  - `PreferenceUpdate` keeps its JSON fields and supplies `expected()` and `desired()`.
- **Optional:**
  - `activeTrack` and `selectNext` return `Optional`.
  - `snapshot` maps the active track into a new `playing` helper.
  - `firstStream` returns `Optional`.
  - `record` uses `orElseGet` with a named `insertFirst`.
- **JavaScript:** `musicTrack` validates named fields, and `music.js` drops the unused import and spells out its helpers.

| Alternative | Why not |
|---|---|
| Keep the boolean signature with comments | Four same-type arguments in a row invite swaps; the record makes expected and desired distinct |
| `Optional` for the radio loop's `state` | See Non-Goals |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/music/catalog/MusicTrackPreferences.java` | new | Named preference pair (boolean parameters) |
| `website/src/main/java/dev/christopherbell/music/catalog/MusicTrackRepository.java`, `MongoMusicTrackRepository.java`, `library/MusicLibraryService.java`, `web/MusicLibraryController.java` | changed | Preference values instead of four booleans; adapter formatting |
| `website/src/main/java/dev/christopherbell/music/metadata/MusicMetadataFileStore.java`, `catalog/MusicCatalogConfiguration.java`, `security/MusicAccessAuditRecorder.java` | changed | Injected `Clock` (hidden time) |
| `website/src/main/java/dev/christopherbell/music/radio/MusicRadioService.java`, `catalog/FfprobeMusicProbe.java`, `security/MongoMusicAccessAttemptRepository.java` | changed | `Optional` instead of null, no `isPresent()` then `get()`; imported names |
| `website/src/main/java/dev/christopherbell/music/catalog/JdkMusicProcessRunner.java`, `MongoMusicCatalogQueryRepository.java`, `MusicArtworkService.java`, `MusicCatalogReconciler.java`, `MusicExecutableResolver.java`, `metadata/MusicMetadataService.java`, `radio/MusicQueueService.java`, `radio/MusicRadioSelector.java`, `security/MusicAccessService.java` | changed | Imported names instead of fully qualified ones |
| `website/src/main/java/dev/christopherbell/music/metadata/FfmpegMusicTagProcess.java` | changed | One artwork branch |
| `website/src/main/java/dev/christopherbell/music/library/MongoMusicPlaylistRepository.java`, `metadata/MongoMusicMetadataEditRepository.java`, `radio/MongoMusicRadioHistoryRepository.java`, `radio/MongoMusicRuntimeStateRepository.java`, `radio/MusicRuntimeStateStore.java` | changed | One statement per line |
| Remaining 57 Music main Java files (records, enums, properties, ports, controllers, filters, playback, selector, migration support) and the README | conforming | No change |
| `website/src/main/resources/static/js/music.js`, `static/js/lib/music.js` | changed | Unused import, helper layout, named fields |
| `website/src/main/resources/templates/music.html`, `static/css/music.css`, `website/src/test/js/music.test.js` | conforming | No change |
| `website/src/test/java/dev/christopherbell/music/library/MusicLibraryServiceTest.java`, `metadata/MusicMetadataServiceTest.java`, `security/MusicComponentWiringTest.java` | changed | New signatures; the wiring test asserts the single Clock constructor |
| `website/src/test/java/dev/christopherbell/music/catalog/MusicArtworkServiceTest.java`, `MusicCatalogReconcilerTest.java`, `MusicCatalogTest.java`, `radio/MusicQueueServiceTest.java`, `radio/MusicRadioServiceTest.java`, `security/MusicAccessAuditMongoContractTest.java`, `web/MusicReadControllerTest.java` | changed | Imported names |
| `website/src/test/java/dev/christopherbell/architecture/MusicAndLunchMongoContractTest.java`, `MusicAndLunchMutationSafetyMongoTest.java` | changed | Follow the preference and recorder signatures (callers outside the slice) |
| Remaining 15 Music test files | conforming | No change |

## Task Breakdown

### Task 1 - Conform the Music slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `MusicTrackPreferences`; `updatePreferences` in the service, repository and adapter; `MusicMetadataFileStore`; `MusicAccessAuditRecorder`; `MusicRadioService.activeTrack`, `selectNext`, `snapshot`, `playing`; `FfprobeMusicProbe.firstStream`; `MongoMusicAccessAttemptRepository.record`, `insertFirst`; `musicTrack` |
| **Inspection** | All files in Inputs at `be88be27` |
| **Behavior** | Same responses, stored fields, radio transitions, audit aggregation and preference compare-and-set |
| **Invariants** | Routes, JSON shapes and stored documents unchanged |
| **Boundary/API** | `updatePreferences` and the two constructors change; all callers are in this change |
| **Effects and failures** | None new |
| **Tests and evidence** | Music Java suites, Music Mongo contract tests in CI, `music.test.js`; runtime boundary checks |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar`; `node --test src/test/js/music.test.js` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check, JS tests, full-diff style review | Covered by AC-3 |
| AC-3 | Music suites | verify-local-app: page, scripts, entry probe, anonymous reads compared with production, permissionless USER rejections. A Music-permitted user needs an ADMIN grant, which has no supported local path, so preference, queue and radio success paths rely on the service tests and Mongo contract tests |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Radio transitions change | Low | `MusicRadioServiceTest` covers catch-up, queue skips, exclusions and contention; the Optional mapping keeps each condition |
| Preference updates match the wrong state | Low | Mongo contract and mutation-safety tests exercise the compare-and-set |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while the federation and vehicle slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - Wiring test now asserts a single constructor

- **Change:** `MusicComponentWiringTest` asserted exactly one `@Autowired` constructor on `MusicAccessAuditRecorder`. With a single `(attempts, clock)` constructor there is nothing to designate, so the test now asserts that one constructor and its parameters.
- **Reason:** The test's purpose, unambiguous Spring wiring with an injectable clock, is kept by the new assertion.
- **Impact:** None beyond the test.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
