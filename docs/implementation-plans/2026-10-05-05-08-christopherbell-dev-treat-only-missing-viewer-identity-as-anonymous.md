# Treat only missing viewer identity as anonymous

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Preserve anonymous viewer behavior only for the explicit missing-authentication condition, while allowing unrelated identity-resolution defects to remain visible.

## Background
`RestaurantService.getSelfIdOrNull` and `PostService.getSelfIdOrNull` catch every `Exception` from `PermissionService.getSelfId()` and return `null`. The expected anonymous case is specifically `IllegalStateException` from `PermissionService.getSelf()` when there is no authenticated account; the broad catch also hides programming or unexpected runtime failures as anonymous feed/preferences reads. This is a targeted error-classification correction found during the remaining Java audit.

## Goals
- Map the explicit missing-authentication `IllegalStateException` to the existing nullable anonymous-viewer contract in both services (AC-1).
- Prove unrelated identity-resolution failures propagate and preserve existing anonymous behavior (AC-2).
- Run native checks and attempt committed local application verification, or record the supported isolated-database blocker with no PR (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing public endpoints, response shapes, or anonymous access rules | The intended absence contract remains unchanged. |
| Changing `PermissionService.getSelfId` or authentication filters | The established boundary already identifies absent authentication with `IllegalStateException`. |
| Editing PR #1477 or using it as evidence | The user explicitly excluded that draft and it predates the current style requirements. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Both optional viewer-ID helpers catch only the explicit missing-authentication exception and continue returning `null` for anonymous requests. |
| AC-2 | Focused tests in both service suites prove unrelated runtime failures propagate while the existing `IllegalStateException` anonymous case remains valid. |
| AC-3 | The committed package passes full native checks and local app verification runs against verified isolated test resources, or its exact blocker is reported and no PR is created. |

## Inputs
- **Request:** User requested a whole-codebase Chris Street Style audit with a separate plan and report for each correction; PR #1477 is excluded.
- **Inspected revision:** Website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Instructions:** Builder AGENTS.md and website AGENTS.md, plus Builder `write-chris-street-style-code` naming, design/API, Java, and testing references.
- **Repository behavior:** `PermissionService.getSelf()` throws `IllegalStateException` when no authenticated identity exists; RestaurantService already has an anonymous-default characterization, and PostService has parallel public-feed/thread entrypoints.

## Branch
`codex/only-anonymous-identity-is-absence-20261005` from website `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.

## Assumptions
- `IllegalStateException` is the only expected exception for the unauthenticated identity case because `PermissionService.getSelf()` explicitly throws it.
- Existing nullable viewer IDs are intentional for public content personalization and are independent from infrastructure/programming failure.
- The supported local MongoDB test endpoint may remain unavailable; app startup must not be attempted until database identity is verified.

## Open Questions
None.

## Design
Keep both helper names and nullable API contracts. Narrow each catch from `Exception` to `IllegalStateException`, matching the actual absence signal in `PermissionService`. Add a focused regression in each owning service test: the expected `IllegalStateException` still yields the anonymous result, and an unrelated `IllegalArgumentException` propagates. This distinguishes legitimate absence from defects without introducing an abstraction for two tiny feature-owned helpers.

| Alternative | Why not |
|---|---|
| Catch all `RuntimeException` | This would continue hiding unrelated programming failures. |
| Return `Optional<String>` and refactor every consumer | It expands public/internal call surfaces beyond the verified defect and adds no needed guarantee for this correction. |
| Remove the fallback entirely | That would break explicitly tested anonymous public-viewer behavior. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java` | Catch only `IllegalStateException` when resolving the optional viewer ID. |
| `website/src/main/java/dev/christopherbell/post/PostService.java` | Apply the same narrow missing-identity handling for public feed and thread personalization. |
| `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java` | Add an unexpected-identity-defect propagation regression beside the anonymous preferences case. |
| `website/src/test/java/dev/christopherbell/post/PostServiceTest.java` | Add an unexpected-identity-defect propagation regression for an anonymous-capable read path. |

## Task Breakdown
### Task 1 - Preserve only the explicit anonymous identity outcome
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | The four expected-change files; source and tests inspected at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `RestaurantService.getSelfIdOrNull`; `PostService.getSelfIdOrNull`; existing public read methods; service tests for anonymous and failure paths. |
| **Inspection** | Read the helpers, `PermissionService.getSelf`, all helper callers, repository instructions, and adjacent tests on the trusted baseline. |
| **Behavior** | Public reads remain anonymously personalized with a null viewer ID when no current identity exists; all other exceptions remain failures. |
| **Invariants** | Do not turn programming/infrastructure failure into a successful anonymous response; authenticated identity resolution is unchanged. |
| **Boundary/API** | Keep public method signatures, routes, response shapes and current nullable identity parameters unchanged. |
| **Effects and failures** | The helpers perform no effects beyond delegating to `PermissionService`; only its explicit unauthenticated `IllegalStateException` is translated to nullable absence. |
| **Tests and evidence** | Capture `RestaurantServiceTest` and `PostServiceTest` baseline; add propagation regressions and run focused suites plus full native checks. |
| **Verification** | Focused Gradle service tests; `:website:check :cbell-lib:check :website:bootJar`; committed packaged local app verification with isolated MongoDB `test` after read-only identity confirmation. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing anonymous RestaurantService behavior and public PostService reads remain passing. | Run committed app and exercise representative public feed/profile read if database isolation is available. |
| AC-2 | Both focused suites assert that `IllegalArgumentException` is propagated and that anonymous `IllegalStateException` remains mapped to absence. | Observe a public anonymous read through the app if startup is available. |
| AC-3 | Full website/library/browser/PowerShell/package gate passes on the committed candidate. | Verify readiness and a representative read against isolated MongoDB `test`, or report exact preflight/startup blocker and cleanup. |

Regression cases:
- Unauthenticated requests retain existing public response behavior.
- Unexpected exceptions from identity resolution are not swallowed as anonymous reads.
- Authenticated personalization continues receiving its identity.

## Rollback or Recovery
Revert the isolated correction commit if focused tests show a public anonymous behavior change. If isolated database identity cannot be verified, do not start the app, alter database state, or create a PR.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| An expected absence path uses a different exception than the inspected `PermissionService` implementation | Low | Verify both direct implementation and existing anonymous characterization before edits. |
| A broad native failure is unrelated to the four touched files | Low | Compare against baseline outputs and report any unrelated failure without expanding this correction. |
| Local runtime remains unavailable | High based on current endpoint evidence | Repeat read-only preflight; do not bypass test DB safeguards. |

## Implementation Log

### 2026-10-05 - Record candidate checks and runtime blocker

- **Change:** Candidate `6f7aede` narrows both optional viewer-ID catches to `IllegalStateException`; the new regressions failed on the broad catches and pass on the candidate. Both existing anonymous behavior and the unrelated-failure propagation contract are characterized.
- **Reason:** `PermissionService.getSelf()` uses `IllegalStateException` for missing authentication; mapping every exception to `null` hid unexpected defects as successful anonymous reads.
- **Impact:** AC-1 and AC-2 are met. AC-3 is blocked by the refused isolated MongoDB preflight; the candidate-specific report records the blocker, and no PR was created.

## Outcome

> [!WARNING]
> The two helper changes are committed and focused/full native checks pass; required local runtime proof remains blocked by unavailable isolated MongoDB.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Candidate `6f7aede` catches only `IllegalStateException` for the expected missing-identity outcome in both services. |
| AC-2 | ✅ Met | New regressions failed on baseline and pass on candidate; focused suites pass PostService 27/27 and RestaurantService 62/62. |
| AC-3 | ⏸️ Blocked | [Candidate report](../test-reports/2026-10-05-05-17-christopherbell-dev-treat-only-missing-viewer-identity-as-anonymous.md): MongoDB `test` identity preflight returned `ECONNREFUSED`, startup was not attempted, and no PR was created. |

Follow-up: verify the committed app against supported isolated test resources before considering PR publication.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
