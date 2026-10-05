# Name Browser Feed Values by Their Roles

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Replace abbreviated browser-feed locals with names that identify matched paths, post items, reply items, sanitizing functions, and parent handles without changing feed rendering or navigation.

## Background
Four active feed modules use short locals (`m`, `p`, `s`, `r`, `h`) where the values have stable domain roles. The expressions are small but their names require readers to infer whether the value is a path match, post, reply, sanitizer or profile handle.

## Goals
- Name every selected browser-feed local for its role (AC-1).
- Preserve path extraction and rendered feed markup/links (AC-2).
- Run touched-file syntax checks, browser tests and package the candidate; attempt required runtime proof (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change DOM structure, user-visible text, API calls or feed order | This is a naming/readability correction only. |
| Rename conventional callback parameters or mathematical SVG coordinates | Those names are locally idiomatic and reveal their roles from the protocol/formula. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `post.js`, `user-feed.js`, `profile.js` and `lib/feed-render.js` use role-specific names for the inspected abbreviated values. |
| AC-2 | Path extraction, feed iteration and sanitized reply/parent rendering remain unchanged. |
| AC-3 | Touched JS syntax checks, `:website:jsTest`, and candidate packaging pass; local application startup and a representative route are attempted and reported before any PR. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** selected feed/path locals in `post.js`, `user-feed.js`, `profile.js`, and `lib/feed-render.js`; static JS README and browser-test conventions.
- **Guidance:** Chris Street Style JavaScript, naming and testing references; website `AGENTS.md`.

## Branch
`codex/browser-feed-role-names-20261005` from `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- The current regexes and feed-data roles are already correct; names and formatting alone need adjustment.
- `node --check` and the built-in browser suite are the native source-level checks for these files.
- Runtime verification still faces the unresolved migration-015 test database blocker.

## Open Questions
- A supported fixture/provisioning or recovery procedure for isolated MongoDB `test` remains necessary before runtime proof and PR creation.

## Design
Expand path matches to `postPathMatch` and `usernamePathMatch`; name iterated domain objects `replyPost`, `feedPost`, `post`, and `reply`; name the sanitizer `sanitizeText` and the rendered parent value `parentHandle`. Use a multiline body for `getPostId()` so extraction and decoding stages are readable. Leave the event callback and chart-coordinate names unchanged because their roles are protocol/formula-local.

| Alternative | Why not |
|---|---|
| Keep single-letter locals in the feed code | Their domain meaning is not conventional enough to infer reliably across parsing and rendering. |
| Mechanically rename every short browser identifier | Event parameters and x/y chart coordinates already have clear protocol or mathematical roles. |
| Change helper exports solely to test them | No public API change is needed for a local variable rename. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/resources/static/js/post.js` | Name path match and visible reply post values. |
| `website/src/main/resources/static/js/user-feed.js` | Name profile path match and page feed post values. |
| `website/src/main/resources/static/js/profile.js` | Name each rendered post. |
| `website/src/main/resources/static/js/lib/feed-render.js` | Name sanitizer, reply and parent handle values. |

## Task Breakdown
### Task 1 - Give browser-feed locals domain names
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the four browser modules, JS README, project tests and JavaScript style references. |
| **Symbols** | `getPostId()`, `getUsernameFromPath()`, feed loops, `createFeedItem()` and parent/reply rendering. |
| **Inspection** | Fresh source revision `695a3ed8617f9b4ab07abb7413baf369c58acf6`; baseline syntax and browser checks will run before editing. |
| **Behavior** | Keep URL decoding, feed order, renderer inputs, sanitization, markup and links unchanged. |
| **Invariants** | Untrusted post/reply text continues to pass through the supplied sanitizer before HTML construction. |
| **Boundary/API** | No exported API, route, request or DOM contract changes. |
| **Effects and failures** | No new effects; existing rendering and async ownership remain unchanged. |
| **Tests and evidence** | Compare native syntax/browser tests before and after; package the candidate and verify the runnable app locally. |
| **Verification** | Run `node --check` on each touched module, `:website:jsTest`, and `:website:bootJar`; then start the committed candidate against isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review the selected bindings and actual uses. | Start candidate on isolated database `test`. |
| AC-2 | Baseline/candidate syntax and browser suite; inspect markup-producing diff. | Request `/` after readiness. |
| AC-3 | `node --check`, `:website:jsTest`, `:website:bootJar`. | Record startup, route response and cleanup in a candidate report. |

Regression: decoded path identifiers and posts/replies render as before; untrusted content still uses `sanitizeText` at the same output points.

## Rollback or Recovery
Revert only the naming correction if output or route behavior differs. Do not change database state directly.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A rename misses one local use and breaks browser code | Low | Syntax-check every touched file, run JS tests, and inspect complete diff. |
| Runtime proof remains blocked | High | Do not create a PR without a successful candidate run and published report. |

## Implementation Log

### 2026-10-05 - Record runtime block

- **Change:** Candidate `b25cf6c8` renamed the inspected feed locals in four browser modules. All four syntax checks, the 380-test `:website:jsTest` suite and `:website:bootJar` passed; packaged startup on isolated database `test` exited before readiness at migration 015. See the [blocked test report](../test-reports/2026-10-05-01-25-christopherbell-dev-name-browser-feed-values-by-their-roles.md).
- **Reason:** Project policy requires successful local application runtime proof before PR creation. Startup is blocked by an incomplete durable migration-015 record; direct database writes and migration bypass are prohibited.
- **Impact:** AC-1 and AC-2 are met; AC-3 is partly met and blocked at runtime. No PR was opened. A supported test fixture/provisioning or recovery procedure is needed.

## Outcome
> [!CAUTION]
> Implementation is complete for source-level checks; required application runtime proof is blocked before readiness by migration 015.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Four browser modules now use role-specific names; candidate `b25cf6c8`. |
| AC-2 | ✅ Met | Syntax/browser checks passed and markup-producing diff preserves output operations. |
| AC-3 | ⏸️ Blocked | Syntax, 380 JS tests and packaging passed; runtime stopped at migration 015 before readiness. [Test report](../test-reports/2026-10-05-01-25-christopherbell-dev-name-browser-feed-values-by-their-roles.md). No PR opened. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
