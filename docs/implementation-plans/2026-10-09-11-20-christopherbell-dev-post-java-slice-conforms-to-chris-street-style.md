# Post Java Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every post (Void) Java file conforms to write-chris-street-style-code, and posting, replies, likes, edits, threads, feeds, discovery, hiding, link previews and expiration behave as before.

## Background
This is slice 16a of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The ledger said to split post when planning it. Slice 16a is the Java (68 main files, 10 READMEs, 35 tests). Slice 16b is the Void and post JavaScript and templates. Inspection at `8d5c68f8` found:

1. **Broad exceptions.** 19 `PostController` endpoints declare `throws Exception`.
2. **Optional misuse:**
   - `VoidPeopleDiscoveryService.suggestions` takes an `Optional` parameter.
   - `PostLinkPreviewService.findFresh` returns null.
   - `PostCreationService` unwraps the parent author with `orElse(null)`.
   - Cursor handling in `PostFeedQueryRepository` and `VoidDiscoveryQueryRepository` calls `isPresent()` then `get()`.
   - `PostExpirationService.setReplyExpirationFromRoot` tests `get() == null` on an `Optional` that can never hold null.
3. **Hidden time.** `PostLinkPreviewCleanupJob`'s Spring constructor uses `Clock.systemUTC()`.
4. **Stringly typed state.** Preview cache status strings are compared at the call site.
5. **Smaller issues:**
   - Fully qualified names throughout main code and tests.
   - Missing `@Override` on query adapters.
   - `get(size - 1)` and `get(0)` where `getLast()` and `getFirst()` exist.
   - One-letter lambda names.
   - A repository Javadoc that still calls the port a Spring Data repository.
   - One-line Mongo adapters.

## Goals
- Every post Java file has a recorded verdict and conforms (AC-1, AC-2).
- The post API behaves as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Void and post JavaScript and templates | Slice 16b |
| Removing the store-less test mode in `PostExpirationService` and the cache-less constructor in `PostLinkPreviewService` | Both are test seams used by many existing tests; replacing them with fakes is a test redesign, recorded as a follow-up |
| Making `activeThreadRootForReply` and the counter updates return `Optional` | Their nullable results flow through like and expiration paths that tests cover in detail; a separate change |
| Nullable viewer id for anonymous feed reads | It is the documented "no viewer" value threaded through every feed method |
| Changing routes, JSON, stored fields, expiration math, SSRF policy or preview categories | Product and security behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every post Java file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with two disposable USERs, the published test report records that: a post with a hashtag, a reply, idempotent likes, the legacy toggle, edits (own only), thread and single reads, global/user/own/history/following feeds, discovery (new, topic, topics, people), hide/unhide and delete (own only, cascading to the reply) behave as expected; discovery and feed pages match production's shape; anonymous writes are rejected |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 16; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `8d5c68f8`:
  - All `post` main and test sources.
  - `VoidDiscoveryController`, the only production caller of `suggestions`.
  - `PostLinkPreviewCleanupJobContextTest`, which checks Spring's constructor choice.
- **Production (read-only GETs, 2026-10-09):** discovery people, discovery new arrivals and the global feed page return 200.

## Branch
`claude/style-post-20261009` from spoke `origin/main` `8d5c68f8`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.

## Open Questions
None.

## Design
- **Controller:** each endpoint declares its service's checked exceptions.
- **People discovery:** `suggestionsFor(selfId, now)` and `anonymousSuggestions(now)` replace the `Optional` parameter. `suggestions()` chooses between them as before.
- **Previews:**
  - `findFresh` returns `Optional`.
  - `PostLinkPreviewCacheEntry` owns the `SUCCESS` and `FAILURE` values and answers `succeeded()`.
- **Cleanup job:** it takes the application `Clock`, and the context test registers one.
- **Cursors:** they use `map`/`ifPresent`.
- **Reply expiration:** it filters out an unchanged expiry instead of comparing a value that cannot be null.
- **Parent author:** an `Optional` delivers the comment notification with `ifPresent`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/post/PostController.java` | changed | Narrow `throws` and Javadoc, imported `Instant` |
| `website/src/main/java/dev/christopherbell/post/discovery/VoidPeopleDiscoveryService.java` | changed | No `Optional` parameter; no `orElse(null)` |
| `website/src/main/java/dev/christopherbell/post/preview/PostLinkPreviewService.java`, `PostLinkPreviewCacheEntry.java`, `PostLinkPreviewCleanupJob.java` | changed | `Optional`, named status values, injected `Clock` |
| `website/src/main/java/dev/christopherbell/post/creation/PostCreationService.java`, `expiration/PostExpirationService.java` | changed | `Optional` use, lambda names |
| `website/src/main/java/dev/christopherbell/post/feed/PostFeedQueryRepository.java`, `discovery/VoidDiscoveryQueryRepository.java`, `feed/PostEngagementQueryRepository.java`, `feed/PostFeedItemAssembler.java` | changed | Cursor `Optional` use, `@Override`, `getLast`/`getFirst`, imports |
| `website/src/main/java/dev/christopherbell/post/feed/PostFeedService.java`, `thread/PostThreadService.java`, `editing/PostEditingService.java`, `discovery/VoidPeopleDiscoveryQueryRepository.java`, `preview/JsoupPostLinkPreviewClient.java`, `preview/LinkPreviewHttpTransport.java`, `PostRepository.java` | changed | Names, imports, true Javadoc |
| `website/src/main/java/dev/christopherbell/post/MongoPostRepository.java`, `hide/MongoHiddenPostThreadRepository.java`, `preview/MongoPostLinkPreviewCacheRepository.java` | changed | One statement per line |
| Remaining 47 post main Java files and the 10 READMEs | conforming | No change |
| `website/src/test/java/dev/christopherbell/post/discovery/VoidPeopleDiscoveryServiceTest.java`, `preview/PostLinkPreviewCleanupJobContextTest.java` | changed | New method names; Clock bean |
| 17 other post test files (`PostControllerTest`, `PostExpirationServiceTest`, `PostLinkPreviewDestinationPolicyTest`, `PostLinkPreviewServiceTest`, `PostRepositoryParityContract`, `PostServiceTest`, `PostTopicExtractorTest`, `MongoPostDiscoveryContractTest`, `PostDiscoveryParityContract`, `VoidDiscoveryQueryRepositoryTest`, `VoidDiscoveryServiceTest`, `VoidPeopleDiscoveryQueryRepositoryTest`, `PostFeedItemAssemblerTest`, `PostFeedQueryRepositoryTest`, `PostReadModelParityContract`, `HiddenPostThreadParityContract`, `PostLikeStoreTest`) | changed | Imported names instead of fully qualified ones |
| Remaining 16 post test files | conforming | No change |

## Task Breakdown

### Task 1 - Conform the post Java slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `PostController` endpoints; `VoidPeopleDiscoveryService.suggestions`, `suggestionsFor`, `anonymousSuggestions`; `PostLinkPreviewService.findFresh`; `PostLinkPreviewCacheEntry.succeeded`; `PostLinkPreviewCleanupJob`; `PostExpirationService.setReplyExpirationFromRoot`; `PostCreationService.createPost` |
| **Inspection** | All files in Inputs at `8d5c68f8` |
| **Behavior** | Same responses, statuses, notifications, cache entries, cursors and expirations |
| **Invariants** | Routes, JSON and stored documents unchanged |
| **Boundary/API** | `suggestions(Optional, Instant)` becomes two methods; the cleanup job's Spring constructor gains `Clock` |
| **Effects and failures** | None new |
| **Tests and evidence** | Post suites, social contract tests; runtime flow below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Post suites | verify-local-app: the flow in AC-3 and shape comparisons with production. The admin-only account history route needs an ADMIN, which has no supported local path |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Discovery or feeds return different pages | Low | Repository tests cover cursors; the runtime flow reads every feed |
| Preview cache reads behave differently | Low | `PostLinkPreviewServiceTest` covers fresh success, fresh failure and misses |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - Context test registers the application Clock

- **Change:** `PostLinkPreviewCleanupJobContextTest` failed because the production constructor now needs a `Clock`. The test registers `Clock.systemUTC()`, as the application does.
- **Reason:** The test's purpose, Spring selecting the production constructor, is unchanged.
- **Impact:** None beyond the test.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
