# View Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every file in the view slice conforms to write-chris-street-style-code, and every HTML route keeps its status, template, headers and model attributes.

## Background
This is slice 8 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `1d1516f9` found:

1. **Unused parameters.** Many handlers take an `HttpServletRequest` they never use.
2. **Duplicated origin.** The public origin is copied into three controllers as `PUBLIC_ROOT`.
3. **Unnamed exceptions.** Caught exceptions are named `exception`, and the invalid-topic 400 drops its cause.
4. **Unclear restaurant page code.** `RestaurantProfilePageService` names its entry point `profile` and its mapper `build`, and decides the coordinate pair by reassigning nulls.
5. **Vague handler names.** `getVoidCreateAccountPage` serves sign-up; `legacyTopRated` and `handleNoResource` do not say what they do.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Every view route behaves as in production (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing `/` from `@RequestMapping` to `@GetMapping` | It would change non-GET behavior on the home route |
| Sharing `PublicSiteUrls` with `configuration/PublicSitemapService` | That file belongs to the configuration slice |
| Changing template names, model attribute names or cache headers | Template contract |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, every public view route returns the same status as production (including 308, 404, 410 and the invalid-topic 400), and the not-found handler keeps its JSON body for `/api/` paths. Recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 8; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `1d1516f9`:
  - All `view` Java and the README.
  - `ViewControllerTest`, `VoidPostSocialPreviewTest` and `RestaurantProfilePageServiceTest`.
  - `configuration/PublicSitemapService` (also has `PUBLIC_ROOT`).

## Branch
`claude/style-view-20261006` from spoke `origin/main` `1d1516f9`.

## Assumptions
- Removing unused `HttpServletRequest` parameters does not change Spring MVC routing.

## Open Questions
None.

## Design
- **Unused parameters:** removed from the handlers that never use them.
- **Shared origin:** `view.PublicSiteUrls.ROOT` replaces the three copies.
- **Exceptions:** named for their meaning. The invalid-topic `ResponseStatusException` keeps its cause.
- **Restaurant page:** `RestaurantProfilePageService.pageFor(restaurantId)` and `pageFrom(detail)` decide `hasValidCoordinatePair` once.
- **Handler names:** `getVoidSignupPage`, `redirectLegacyTopRatedToTopLiked` and `notFound`.

| Alternative | Why not |
|---|---|
| Keep the request parameters for future use | Unused parameters mislead readers about what a handler depends on |
| Rename every `get*Page` handler | They already read as "get the X page"; churn without benefit |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/view/PublicSiteUrls.java` | new | Shared public origin (rule 9) |
| `website/src/main/java/dev/christopherbell/view/PublicRouteNotFoundHandler.java` | changed | `notFound`, role names (rules 1, 2) |
| `website/src/main/java/dev/christopherbell/view/account/AccountViewController.java` | changed | Unused parameters removed; `getVoidSignupPage` (rule 1) |
| `website/src/main/java/dev/christopherbell/view/voidroutes/VoidViewController.java` | changed | Unused parameters, shared origin, named exceptions with cause (rules 1, 8) |
| `website/src/main/java/dev/christopherbell/view/content/ContentViewController.java` | changed | Unused parameters removed (rule 1) |
| `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java` | changed | Shared origin, `redirectLegacyTopRatedToTopLiked`, `pageFor` (rule 1) |
| `website/src/main/java/dev/christopherbell/view/wfl/RestaurantProfilePageService.java` | changed | `pageFor`, `pageFrom`, single coordinate decision, `heroText` (rules 1, 3) |
| `website/src/main/java/dev/christopherbell/view/ViewIndexingPolicy.java`, `tools/ToolsViewController.java`, `voidroutes/VoidPostSocialPreview*.java`, `voidroutes/VoidUserSocialPreview*.java`, `wfl/RestaurantProfilePage.java`, `README.md` | conforming | No change |
| `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`, `wfl/RestaurantProfilePageServiceTest.java` | changed | `pageFor` |
| `website/src/test/java/dev/christopherbell/view/voidroutes/VoidPostSocialPreviewTest.java` | conforming | No change |

## Task Breakdown

### Task 1 - Conform the view slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | Handlers in the five controllers; `PublicRouteNotFoundHandler.notFound`; `RestaurantProfilePageService.pageFor`, `pageFrom`, `publicAddress`; `PublicSiteUrls.ROOT` |
| **Inspection** | All files in Inputs at `1d1516f9` |
| **Behavior** | Same templates, statuses, headers, redirects and model attributes for every route |
| **Invariants** | Canonical URLs and social metadata unchanged; coordinate pairs are kept only when both are valid |
| **Boundary/API** | `RestaurantProfilePageService.profile` renamed; its callers are the WFL controller and tests |
| **Effects and failures** | None beyond responses |
| **Tests and evidence** | `ViewControllerTest` (51), `RestaurantProfilePageServiceTest` (5), `VoidPostSocialPreviewTest` (3); runtime route sweep against production |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | The three view suites | verify-local-app: for every public view route, compare the candidate's status with production's; check the `/api/` not-found JSON body |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A route's status changes | Low | Route sweep against production and `ViewControllerTest` |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-06 - PR branch updated with main before merge

- **Change:** `gh pr update-branch` merged `main` `38907c6c` (message slice) into the PR branch, and CI passed on the merged head.
- **Reason:** The ruleset requires up-to-date branches, and force-pushing is a gate.
- **Impact:** None to the view diff.

### 2026-10-06 - How the post-deploy route check was verified

- **Change:** The post-deploy statement in the Outcome rests on comparing production's statuses after the deploy with the candidate's statuses recorded in the runtime report. All 40 routes matched.
- **Reason:** The first post-deploy command mistakenly compared production with itself, which proves nothing. It was replaced by this comparison before the claim was relied on.
- **Impact:** None to the result; the evidence is now the right one.

## Outcome

> [!TIP]
> Shipped in PR #1498 (`d83f96c`) and auto-deployed. All 40 view routes return the same statuses in production after the deploy as the candidate did.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check passed; `ViewControllerTest` 51/51 ([report](../test-reports/2026-10-06-21-01-christopherbell-dev-view-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | Route sweep: 40 of 40 routes matched production ([report](../test-reports/2026-10-06-21-01-christopherbell-dev-view-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1498](https://github.com/azurras/christopherbell.dev/pull/1498) merged as `d83f96c` after all six checks passed; production `/actuator/info` reports `d83f96c` |


## Project
christopherbell-dev

## Plan Format
task-contract-v2
