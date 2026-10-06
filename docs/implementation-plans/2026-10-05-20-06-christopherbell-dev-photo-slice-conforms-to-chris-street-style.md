# Photo Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every file in the photo slice of christopherbell.dev conforms to write-chris-street-style-code, and the gallery API and pages behave exactly as before.

## Background
Slice 1 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md), chosen as the smallest feature so the per-slice workflow is proven first. Inspection found mutable Lombok beans for configuration values, a non-final injected field, an unused logger, activity names (`getAllImages`, `update`, `render`) that do not say what is listed or rendered, nondeterministic and mutable public test stubs, and a service test that compares a mock with itself.

## Goals
- Every photo slice file has a recorded verdict and conforms (AC-1, AC-2).
- `GET /api/photo/v1`, `/photos` and `/photos/usage` behave as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Removing or populating `createdOn` | The configuration's `date-added` key never binds to it, so the API always returns `createdOn: null`; changing that alters the JSON contract and is logged as a follow-up |
| Replacing the `n/a` description sentinel in configuration | It is data the gallery already handles; changing it is a content decision |
| Moving `/photos` routes out of `ContentViewController` | That controller belongs to the view slice |
| Showing a visible error when the gallery fetch fails | A UI behavior change; failures are already logged with their cause |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for each of the 14 existing slice files and the one new file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker or actionable warning |
| AC-3 | The packaged candidate on isolated MongoDB `test` returns 200 for `/api/photo/v1` with the same JSON as baseline `ef15adc0` and 200 for `/photos` and `/photos/usage`, recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 1; user chose full conformance, one PR per feature, smallest first.
- **Inspected:** spoke `origin/main` `ef15adc0`: all photo Java and tests, `photo/photography.html`, `photo/usage.html`, `static/js/components/gallery.js`, its callers `app.js` (`photo-gallery` lazy tag) and `lib/api.js` (`API.photos.images`), JS tests `public-content.test.js` and `lazy-component.test.js`, `ContentViewController` routes, `application.yml` `photo-properties`, and the record properties pattern in `configuration/mail`.

## Branch
`claude/style-photo-20261005` from spoke `origin/main` `ef15adc0`, in a linked worktree.

## Assumptions
- Spring Boot 4.1 binds a list of nested records through constructor binding, as `MailProperties` already relies on for flat records.
- Jackson serializes record components with the same property names as the current Lombok getters, and default inclusion keeps `createdOn: null`.

## Open Questions
None.

## Design
Configuration values become records registered by a small `PhotoConfiguration`, matching the `configuration/mail` pattern. `Photo` validates that its id, name and path are present at binding, so a broken gallery entry fails startup with the field name instead of rendering a broken image. Service and controller methods say what they list. The gallery component passes the fetched photos into the render step instead of parking them on a field.

| Alternative | Why not |
|---|---|
| Keep Lombok `@Data` beans and only rename methods | Leaves configuration values mutable after binding, against the record idiom |
| Bean Validation annotations on the record | The compact constructor states the same invariant with no validation starter wiring for configuration |
| Drop `createdOn` because it is always null | Changes the public JSON; out of scope |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/photo/PhotoController.java` | changed | `getImages` becomes `listGalleryPhotos`; `ResponseEntity.ok` (rule 1) |
| `website/src/main/java/dev/christopherbell/photo/PhotoService.java` | changed | `getAllImages` becomes `listGalleryPhotos`; `final` field; unused `@Slf4j` removed (rules 1, 7) |
| `website/src/main/java/dev/christopherbell/photo/PhotoConfiguration.java` | new | Registers `PhotoProperties` (rule 7, mail pattern) |
| `website/src/main/java/dev/christopherbell/photo/model/Photo.java` | changed | Record that rejects a missing id, name or path (rules 4, 5) |
| `website/src/main/java/dev/christopherbell/photo/model/PhotoProperties.java` | changed | `@ConfigurationProperties` record with an unmodifiable photo list (rule 4) |
| `website/src/main/java/dev/christopherbell/photo/model/PhotoResponse.java` | changed | Record with an unmodifiable `images` list; JSON name unchanged (rule 4) |
| `website/src/main/java/dev/christopherbell/photo/README.md` | changed | Names the configuration class |
| `website/src/main/java/dev/christopherbell/photo/model/README.md` | changed | Says photo entries are validated records |
| `website/src/test/java/dev/christopherbell/photo/PhotoControllerTest.java` | changed | Asserts the photo fields in the envelope (rule 10) |
| `website/src/test/java/dev/christopherbell/photo/PhotoServiceTest.java` | changed | Real properties in, same photos out; rejection of a photo without a path (rule 10) |
| `website/src/test/java/dev/christopherbell/photo/PhotoStub.java` | changed | Final constants, fixed instant, `UUID` id (rules 2, 10) |
| `website/src/test/java/dev/christopherbell/photo/PhotoPropertiesConfigurationTest.java` | changed | Record accessors; helper named for what it does (rule 1) |
| `website/src/main/resources/static/js/components/gallery.js` | changed | `renderGallery(photos)`, `renderEmptyGallery`, role names for elements (rules 1, 2, 9) |
| `website/src/main/resources/templates/photo/photography.html` | changed | Script moved inside `body` (valid document structure) |
| `website/src/main/resources/templates/photo/usage.html` | conforming | No change |

## Task Breakdown

### Task 1 - Conform the photo slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | As listed in Expected Changes |
| **Symbols** | `PhotoController.listGalleryPhotos`, `PhotoService.listGalleryPhotos`, `PhotoConfiguration`, `Photo`, `PhotoProperties`, `PhotoResponse`, `PhotoStub`, `galleryImagesFromResponse`, `galleryAltText`, `PhotoGallery` methods |
| **Inspection** | All slice files and their callers at `ef15adc0`, listed in Inputs |
| **Behavior** | `GET /api/photo/v1` returns the same envelope with `payload.images` holding the configured photos in order, including `createdOn: null`; pages render the same gallery |
| **Invariants** | Configuration prefix `photo-properties`, JSON property names, `API.photos.images`, exported JS function names and the `photo-gallery` tag stay the same |
| **Boundary/API** | `PhotoService` has no callers outside the slice; renames stay inside the slice |
| **Effects and failures** | Startup fails naming the field if a configured photo lacks an id, name or path; fetch failures stay logged with their cause |
| **Tests and evidence** | Baseline photo tests and JS tests pass before; the changed tests pass after; baseline and candidate JSON for `/api/photo/v1` compared |
| **Verification** | `./gradlew.bat :website:test --tests "dev.christopherbell.photo.*" :website:jsTest`, then the full check |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar`; full-diff style review | Covered by AC-3 |
| AC-3 | Photo Java tests and `:website:jsTest` | verify-local-app starts the baseline and candidate JARs on isolated MongoDB `test`; `/api/photo/v1` JSON identical; `/photos` and `/photos/usage` return 200 and reference `/js/app.js` |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` for the merge commit |

- **Regressions:** `public-content.test.js` and `lazy-component.test.js` cover the exported gallery helpers and the lazy tag.

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls production forward to the revert. No data changes.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Record binding of the nested photo list fails at startup | Low | `PhotoPropertiesConfigurationTest` binds the real `application.yml`; runtime startup proves it |
| JSON field order or nulls change | Low | Baseline and candidate responses compared byte for byte |

## Implementation Log

### 2026-10-05 - Missing gallery configuration yields an empty list

- **Change:** `PhotoProperties` turns an absent `photos` list into an empty unmodifiable list, so the API would return `images: []` instead of `images: null` when the `photo-properties` block is missing.
- **Reason:** A record with a defensive copy cannot hold `null` without a special case, and the gallery JavaScript already treats both as no photos.
- **Impact:** Only reachable with a configuration that has no gallery; the shipped `application.yml` has one, and the runtime JSON is byte-identical to production. Covered by `PhotoServiceTest.listsNoPhotosWhenNoneAreConfigured`.

### 2026-10-05 - Forked Gradle JVMs need the socket folder too

- **Change:** Ran Gradle with both `GRADLE_OPTS` and `JAVA_TOOL_OPTIONS` set to `-Djdk.net.unixdomain.tmpdir=C:\Temp\jdk-unix-sockets`, outside the command sandbox.
- **Reason:** With only `GRADLE_OPTS`, the test executor JVM failed with "Unable to establish loopback connection"; the spoke README already sets `JAVA_TOOL_OPTIONS` for the same reason.
- **Impact:** No spoke change. Later slices use the same environment.

## Outcome

> [!TIP]
> Shipped as planned in PR #1488 (`1d6c7d0`) and auto-deployed. The JSON contract is unchanged. The two deviations are recorded in the Implementation Log. Follow-up: the unbound `date-added` key leaves `createdOn` always null, which is a contract decision for later.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes gives a verdict for all 14 existing files plus the new `PhotoConfiguration` (13 changed, 1 conforming, 1 new) |
| AC-2 | ✅ Met | Full check passed: 2,215 Java tests with 0 failures, 382 JS tests, Pester suites; full-diff self-review found no blocker ([report](../test-reports/2026-10-05-20-15-christopherbell-dev-photo-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | Candidate `190cfc0` on isolated MongoDB `test`: 6 of 6 cases passed, and the gallery JSON is byte-identical to production `ef15adc0` ([report](../test-reports/2026-10-05-20-15-christopherbell-dev-photo-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1488](https://github.com/azurras/christopherbell.dev/pull/1488) merged as `1d6c7d0` after build, three Analyze, CodeQL and dependency-review passed; production `/actuator/info` reports `1d6c7d0`, and the production gallery JSON is unchanged |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
