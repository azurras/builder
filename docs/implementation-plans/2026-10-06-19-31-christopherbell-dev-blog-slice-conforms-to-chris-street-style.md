# Blog Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the blog slice of christopherbell.dev conforms to write-chris-street-style-code, and the blog API and page behave exactly as before.

## Background
Slice 2 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The user asked to continue slice by slice without pausing for review. Inspection found:

1. The controller turns the already-validated `UUID` path variable back into a string, and the service parses it again with its own null, blank and UUID checks. Those checks are unreachable from HTTP.
2. Configuration values are mutable Lombok beans.
3. The logger is unused.
4. Activity names (`getPosts`, `updatePosts`, `render`) don't say what is listed or rendered.
5. Test stubs are mutable and nondeterministic.
6. Tests compare a mock with itself.

## Goals
- Every blog slice file has a recorded verdict and conforms (AC-1, AC-2).
- `/api/blog/v1/posts`, `/api/blog/v1/posts/{id}` (200, 404 and 400 paths) and `/blog` behave as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the 400 or 404 envelopes or their messages | Public contract; the handler in cbell-lib owns them |
| Publishing blog posts | `blog-properties.posts` is empty by design; content is a separate decision |
| Moving `/blog` out of `ContentViewController` | Belongs to the view slice |
| Changing `back-office.js` blog loading | Belongs to the admin slice, and it is correct because `fetchJson` unwraps `payload` |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for each of the 13 existing slice files and the one new file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker or actionable warning |
| AC-3 | The packaged candidate on isolated MongoDB `test` returns the same status and byte-identical JSON as production `0202b97b` for the post list, an absent post ID (404) and a malformed post ID (400), and 200 for `/blog`, recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 2; on 2026-10-06 the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `0202b97b`: all blog Java and tests, `templates/blog.html`, `static/js/components/blog.js`, `src/test/js/blog-empty-state.test.js`, callers `app.js` (`blog-posts` lazy tag), `lib/api.js` (`API.blog.posts`), `back-office.js` `loadBlogPosts`, `lib/util.js` `fetchJson`, `ContentViewController`, `SecurityConfig` and `PublicSitemapService` `/blog` entries, `application.yml` `blog-properties`.

## Branch
`claude/style-blog-20261006` from spoke `origin/main` `0202b97b`, in a linked worktree.

## Assumptions
- Spring's UUID path conversion keeps rejecting malformed IDs with the standard 400 envelope before the controller runs, as `BlogControllerTest.malformedPostIdReturnsTheStandardBadRequestEnvelopeBeforeServiceInvocation` already proves.

## Open Questions
None.

## Design
This follows the photo slice pattern. The configuration values become records, registered by `BlogConfiguration`. `Post` requires an id and a title, and treats missing tags as no tags. The service takes the typed `UUID` it is actually given. That removes the string re-parsing and its unreachable `InvalidRequestException` paths. `findPostById` and `listPosts` say what they return. The blog component passes fetched posts into `renderPosts`, and article building moves to `articleFor`.

| Alternative | Why not |
|---|---|
| Keep the string ID and its checks in the service | Duplicates validation the HTTP boundary already performs and hides that the caller has a UUID |
| Return `Optional<Post>` from the service | The only caller turns absence into the standard 404, which `ResourceNotFoundException` already does |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/blog/BlogController.java` | changed | `findBlogPost(@PathVariable("id") UUID postId)`, `listBlogPosts`; no re-stringified ID (rules 1, 3, 5) |
| `website/src/main/java/dev/christopherbell/blog/BlogService.java` | changed | `findPostById(UUID)`, `listPosts`; unused logger and unreachable checks removed (rules 1, 5, 9) |
| `website/src/main/java/dev/christopherbell/blog/BlogConfiguration.java` | new | Registers `BlogProperties` (rule 7) |
| `website/src/main/java/dev/christopherbell/blog/model/BlogProperties.java` | changed | Record with an unmodifiable post list (rule 4) |
| `website/src/main/java/dev/christopherbell/blog/model/BlogResponse.java` | changed | Record; JSON name `posts` unchanged (rule 4) |
| `website/src/main/java/dev/christopherbell/blog/model/Post.java` | changed | Record requiring id and title (rules 4, 5) |
| `website/src/main/java/dev/christopherbell/blog/README.md` | changed | Names the classes and configuration |
| `website/src/main/java/dev/christopherbell/blog/model/README.md` | changed | States the record invariants |
| `website/src/test/java/dev/christopherbell/blog/BlogControllerTest.java` | changed | Asserts returned post fields (rule 10) |
| `website/src/test/java/dev/christopherbell/blog/BlogServiceTest.java` | changed | Real properties; lookup, absence, ordering, empty, title and tag invariants (rule 10) |
| `website/src/test/java/dev/christopherbell/blog/BlogStub.java` | changed | Final constants, fixed instant, two distinct posts (rules 2, 10) |
| `website/src/main/resources/static/js/components/blog.js` | changed | `renderPosts(blogPosts)`, `articleFor`, `renderEmptyContainer`, role names (rules 1, 2, 9) |
| `website/src/test/js/blog-empty-state.test.js` | changed | Drives `renderPosts` directly (rule 10) |
| `website/src/main/resources/templates/blog.html` | changed | Script moved inside `body` |

## Task Breakdown

### Task 1 - Conform the blog slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Slice 1 merged |
| **Files** | As listed in Expected Changes |
| **Symbols** | `BlogController.findBlogPost`, `BlogController.listBlogPosts`, `BlogService.findPostById`, `BlogService.listPosts`, `BlogConfiguration`, `Post`, `BlogProperties`, `BlogResponse`, `BlogStub`, `BlogPosts.renderPosts`, `articleFor` |
| **Inspection** | All slice files and callers at `0202b97b`, listed in Inputs |
| **Behavior** | The list returns `payload.posts` (currently empty); a valid absent ID returns the 404 envelope; a malformed ID returns the 400 envelope; `/blog` shows the empty state |
| **Invariants** | Path `/v1/posts/{id}`, JSON names, configuration prefix `blog-properties`, `API.blog.posts`, `blog-posts` tag and CSS classes `blogPosts` and `blogArticle` stay the same |
| **Boundary/API** | `BlogService` has no callers outside the slice |
| **Effects and failures** | A configured post without an id or title fails startup naming the field; fetch failures stay logged with their cause |
| **Tests and evidence** | Baseline blog tests passed in CI on `0202b97b`; changed tests pass; runtime JSON compared with production |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Blog Java tests and `:website:jsTest` | verify-local-app runs the packaged candidate on isolated MongoDB `test`; the three API responses are byte-identical to production `0202b97b`; `/blog` returns 200 with the `blog` mount and the script inside `body` |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls production forward. No data changes.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Binding an empty `posts: []` list to a record fails | Low | Runtime startup and `/api/blog/v1/posts` prove it |
| The 404 or 400 envelope changes | Low | Byte comparison with production |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the slice edits were made and while the full check ran. It should have been published first.
- **Reason:** Continuing straight from slice 1, I started inspecting and editing before saving the plan.
- **Impact:** No PR has been opened. Inspection evidence and design are unchanged; the plan is published before the runtime report and PR.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
