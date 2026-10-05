# Name Music Search Text by Its Role

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Rename the Music catalog's vague `q` parameter to `searchText` while explicitly preserving the public `q` request parameter contract.

## Background
`MusicReadController.catalog()` receives an optional search string as `q`, then passes it to `MusicQuery`. The one-letter name obscures the distinction between the external request key and the meaning of the value. Spring currently infers the query parameter name from the Java parameter name, so a rename without an explicit annotation value would silently change the API.

## Goals
- Name the controller value `searchText` at its Java boundary and use that role at the `MusicQuery` call (AC-1).
- Pin the public request key to `q` and prove the existing query contract (AC-2).
- Run focused/full checks, package and attempt local runtime verification for the committed candidate (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Rename the public query key or change filtering semantics | `q` is an existing browser/API contract. |
| Rework Music catalog paging, authorization or response shape | Those are separate behaviors with existing ownership and tests. |
| Change music UI labels or search normalization | Not necessary to make this Java parameter clear. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The controller names the incoming search text by role and passes it unchanged into `MusicQuery`. |
| AC-2 | Spring explicitly binds the existing public key `q`; a regression verifies the annotation contract and the resulting `MusicQuery` value. |
| AC-3 | Focused/full native checks and packaged local startup/representative route attempt are recorded for the exact candidate; PR remains gated on successful readiness. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `MusicReadController.catalog()`, `MusicReadControllerTest`, `MusicQuery`, music package README, and related controller/view/security tests at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Guidance:** Chris Street Style Java and testing references; website `AGENTS.md`.

## Branch
Create a fresh isolated worktree and branch from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6` after publishing this plan.

## Assumptions
- The search term is passed to `MusicQuery` unchanged and its original spelling/whitespace is part of current catalog behavior.
- Explicit `@RequestParam(name = "q")` pins the external query key while allowing the Java parameter name to improve.
- Isolated MongoDB `test` still fails candidate startup at migration 015; no direct writes or bypasses are allowed.

## Open Questions
None. Preserve the inspected API key and resolve the internal naming choice from the value's role.

## Design
Rename only the Java parameter from `q` to `searchText`, spell the external request parameter explicitly as `@RequestParam(name = "q", required = false)`, and pass `searchText` to `MusicQuery`. Extend `MusicReadControllerTest` to assert the mapping annotation retains `q` while its existing captured-query test confirms the value reaches the query object.

| Alternative | Why not |
|---|---|
| Leave `q` as the Java parameter | The role remains implicit and abbreviated. |
| Rename the external query key to `searchText` | Breaks the established browser/API contract. |
| Introduce a wrapper record for one optional string | Adds a type and mapping without protecting a real multi-value invariant. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/music/web/MusicReadController.java` | Name the input `searchText`, explicitly bind request key `q`, and pass the named value to `MusicQuery`. |
| `website/src/test/java/dev/christopherbell/music/web/MusicReadControllerTest.java` | Assert the explicit external query key and retain value-forwarding coverage. |

## Task Breakdown
### Task 1 - Name the search value without changing the request contract
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected controller, query record, focused test, owning README, route security tests and UI call sites. |
| **Symbols** | `MusicReadController.catalog(...)` and its `MusicQuery` construction; `MusicReadControllerTest`. |
| **Inspection** | Fresh website revision `695a3ed8617f9b4ab07abb7413baf369c58acf6`; repository callers use the versioned `/api/music/.../catalog` route and query key `q`. |
| **Behavior** | Search text and all neighboring filters/page inputs are passed with current semantics. |
| **Invariants** | Read authorization, no-store response, catalog paging and JSON output remain unchanged. |
| **Boundary/API** | Public query parameter remains `q`; only the Java local/parameter identifier changes. |
| **Effects and failures** | No new effects; catalog read authorization remains before query execution. |
| **Tests and evidence** | Establish focused controller baseline; extend tests to pin request key and verify captured `MusicQuery`; run full checks. |
| **Verification** | `:website:test --tests dev.christopherbell.music.web.MusicReadControllerTest`, `:website:check :cbell-lib:check`, `:website:bootJar`; then attempt packaged runtime on isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing captured `MusicQuery` assertion verifies exact unchanged search value. | Candidate startup and representative home/catalog route after readiness. |
| AC-2 | Test confirms `@RequestParam.name()` is `q` and captured query carries the input. | Candidate startup and representative home/catalog route after readiness. |
| AC-3 | Focused controller test, full module checks, package and diff check. | Test profile, isolated MongoDB `test`, non-production port and disabled side effects; report actual startup/route/cleanup. |

Regression: the old browser request key `q` continues to map to catalog search; no user-visible catalog output or route changes.

## Rollback or Recovery
Revert the two-file rename if the query key, captured `MusicQuery`, or route behavior changes. Preserve the `q` key on any correction.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Spring stops binding legacy `q` after the Java rename | Low | Set `@RequestParam(name = "q")` explicitly and assert the annotation contract. |
| Required candidate runtime remains blocked | High | Record actual startup attempt and do not open a PR before readiness and a supported test fixture/recovery path. |

## Implementation Log

### 2026-10-05 - Record runtime blocker

- **Change:** The `searchText` rename, explicit `q` mapping, focused regression and full project gate are complete on committed candidate `3b7c064`; packaged startup was attempted and blocked at migration 015 before readiness.
- **Reason:** The shared test database has an incomplete durable migration record, so application runtime and route behavior cannot be verified safely in this run.
- **Impact:** AC-1 and AC-2 pass; AC-3 is blocked pending supported database recovery and a new runtime attempt. See the [test report](../test-reports/2026-10-05-01-56-christopherbell-dev-name-music-search-text-by-its-role.md).

## Outcome

> [!CAUTION]
> The internal search value was renamed and the public `q` contract remains pinned, but local runtime proof is blocked before readiness by the test database's incomplete migration 015 record. No PR was opened.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ PASS | Focused controller test confirms unchanged `MusicQuery` forwarding; candidate `3b7c064`. |
| AC-2 | ✅ PASS | Focused controller test confirms explicit request key `q`; candidate `3b7c064`. |
| AC-3 | ⏸️ BLOCKED | [Runtime report](../test-reports/2026-10-05-01-56-christopherbell-dev-name-music-search-text-by-its-role.md): full checks and package pass, but application startup fails at migration 015 before readiness.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
