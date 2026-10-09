# Security Configuration Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The root `configuration.security` package conforms to write-chris-street-style-code, and authentication, CSRF, headers, public routes and rate limiting behave as before.

## Background
This is slice 18c of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 18a](2026-10-09-15-25-christopherbell-dev-configuration-root-mail-and-persistence-conform-to-chris-str.md). While planning it, `security` was split into this root part (5 files) and the `security/browser` subpackage (12 files, slice 18d), and `mongo` became 18e. Inspection at `06297e60` found:

1. **`SecurityConfig`:**
   - The `RateLimitFilter` and `BrowserSessionService` beans are built with `Clock.systemUTC()` instead of the application `Clock`.
   - The single-post public matcher is an inline lambda with seven one-line `if` statements.
   - A helper class is named `Sec`.
   - Fully qualified `HttpServletRequest` and `HttpHeaders`, and an unnamed HSTS max age.
   - A whitespace-only line.
2. **`JwtAuthenticationFilter`:** it unwraps the bearer account with `orElse(null)`, checks the browser session with `isPresent()` then `get()`, and keeps two nullable locals across a long method.
3. **`BrowserSecurityProperties`:** a fully qualified `Locale`.
4. **Conforming:** `StaticAssetRequestMatcher` and `BrowserAuthenticationCookies`.

## Goals
- Every root security file has a recorded verdict and conforms (AC-1, AC-2).
- Authentication, CSRF, headers and public routes behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| The `throws Exception` on `securityFilterChain` and `authenticationManager` | Spring Security's `HttpSecurity.build()` and `getAuthenticationManager()` declare it; the Javadoc now says so |
| The JWT filter's nullable collaborators | They are the seams `JwtAuthenticationFilterTest` and the controller slice configuration use |
| The public URL list, CSP, permissions policy and cookie attributes | Security behavior |
| `security/browser` | Slice 18d |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every root security file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that a USER's bearer login reaches `/me`, a cookie login reaches `/me` and is refused without CSRF on a mutation, a forged bearer token is rejected, a public single post read is anonymous while `/api/posts/.../me` is not, and security headers and the anonymous `/me` rejection match production |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `06297e60`:
  - The 5 root `configuration/security` files.
  - `JwtAuthenticationFilterTest`, `SecurityConfigTest` and `ControllerSliceSecurityTestConfig`.
  - The four tests that import `SecurityConfig`: `AsyncDispatcherSecurityIntegrationTest`, `LocationControllerSecurityTest`, `SharedFolderSecurityIntegrationTest` and `SurviveControllerTest`.

## Branch
`claude/style-config-security-20261009` from spoke `origin/main` `06297e60`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.

## Open Questions
None.

## Design
- **`SecurityConfig`:**
  - The rate-limit and browser-session beans take the application `Clock`.
  - `isPublicSinglePostGet` replaces the inline lambda and keeps its rules.
  - `toMatcher` replaces the `Sec` class.
  - `HSTS_MAX_AGE_SECONDS` names the max age.
- **JWT filter:**
  - `authenticate` returns an `Optional` of a private `Authenticated` record holding the authentication and any rotated session token.
  - The filter then sets the context, adds rotated cookies or rejects, as before.
  - `bearerAccount` returns the matching active account.
  - Building the authentication token now happens inside the credential `try`, so an account without a role (which the account model never stores) is rejected as an invalid credential instead of failing the request.
- **Tests:** the four tests that import `SecurityConfig` also import `ApplicationClockConfiguration`, as the application does.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java` | changed | Injected `Clock`; named matcher method and constant; imports; whitespace; documented Spring `throws` |
| `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java` | changed | `Optional` authentication result; imports |
| `website/src/main/java/dev/christopherbell/configuration/security/BrowserSecurityProperties.java` | changed | Imported `Locale` |
| `StaticAssetRequestMatcher`, `BrowserAuthenticationCookies` | conforming | No change |
| `website/src/test/java/dev/christopherbell/configuration/security/AsyncDispatcherSecurityIntegrationTest.java`, `location/LocationControllerSecurityTest.java`, `sharedfolder/SharedFolderSecurityIntegrationTest.java`, `survive/SurviveControllerTest.java` | changed | Import the application clock configuration |

## Task Breakdown

### Task 1 - Conform root security configuration

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SecurityConfig.rateLimitFilter`, `browserSessionService`, `isPublicSinglePostGet`, `toMatcher`; `JwtAuthenticationFilter.doFilterInternal`, `authenticate`, `bearerAccount`, `Authenticated` |
| **Inspection** | All files in Inputs at `06297e60` |
| **Behavior** | Same authentication, rotation, rejection, CSRF, headers and public routes |
| **Invariants** | Public URL list, policies, cookies and filter order unchanged |
| **Boundary/API** | Two bean methods gain a `Clock` parameter |
| **Effects and failures** | An account without a role is rejected (401 or anonymous on public routes) instead of failing the request |
| **Tests and evidence** | Security, configuration, Survive and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | JWT filter, security config and integration tests | verify-local-app: the flow in AC-3 with disposable USERs |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A credential that used to authenticate is rejected | Low | The bearer and cookie paths keep their order and checks; `JwtAuthenticationFilterTest` covers fingerprints, inactive accounts, rotation and rejection; the runtime logs in both ways |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slices 18a and 18b were in progress.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - Stale inspection corrected

- **Change:** The first edit script was written against the main checkout, which was behind `origin/main` and lacked the injected `LoginTokens` from PR #1493. The script refused to apply, and it was rewritten against the worktree cut from `origin/main`.
- **Reason:** Every replacement asserts an exact match, so stale text cannot be applied.
- **Impact:** The main checkout is now fast-forwarded before inspection.

### 2026-10-09 - Tests import the application clock

- **Change:** Four tests that import `SecurityConfig` failed with no `Clock` bean once the beans took one. They now also import `ApplicationClockConfiguration`.
- **Reason:** That is how the application provides its `Clock`.
- **Impact:** Test configuration only.

### 2026-10-09 - First runtime run discarded

- **Change:** The first runtime run compared security headers and the anonymous `/me` with production while production was restarting for the slice 17f deploy; Cloudflare answered 502, so the comparison was against an error page. The candidate-only checks all passed. The comparisons were rerun on the same candidate once production answered 200.
- **Reason:** A comparison is only evidence when both sides answer normally.
- **Impact:** None on the code; the report records the discarded run.

## Outcome

> [!TIP]
> Shipped in PR #1518 (`f19a275`) and auto-deployed. Production serves `5b7ef3c`, which contains it, and `/robots.txt` returns 200. Later merges landed before the deploy finished, so production went straight to the newer head.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every root security file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-16-02-christopherbell-dev-security-configuration-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 5 of 5 runtime cases passed on candidate `2cd4670`, after the discarded first run logged above ([report](../test-reports/2026-10-09-16-02-christopherbell-dev-security-configuration-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1518](https://github.com/azurras/christopherbell.dev/pull/1518) merged as `f19a275` after all checks passed; production `/actuator/info` reports `5b7ef3c`, which contains it |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
