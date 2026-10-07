# Permission Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The permission slice conforms to write-chris-street-style-code. Login JWTs are issued and verified by one injected `LoginTokens` bean instead of a static, mutable signing key. Login, bearer authentication, browser sessions and role checks behave as before.

## Background
This is slice 3 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). `PermissionService` (281 lines) mixes three jobs: role checks, current-account lookup, and JWT issuing and verification. Inspection at `0202b97b` found these problems:

1. **Hidden global key.** The signing key is a `private static volatile` field. It is initialized at class load from the environment, then overwritten by a Spring instance setter. Static `generateToken` and `validateToken` read this hidden global, so tests and callers depend on whichever key was set last.
2. **Swallowed defects.** `hasAuthority` wraps its body in `catch (Exception)`, which logs and denies. A programming defect looks like an ordinary "no".
3. **Null handling by exception.** `knownRole` catches `NullPointerException` to handle null authority names.
4. **Test-only code.** `isAuthenticated` (password check) and `isAccountActive` are only called by tests. `isAccountActive` also declares an exception it never throws.
5. **Deprecated and implicit APIs.** Token parsing uses the deprecated jjwt `setSigningKey`, `parseClaimsJws` and `getBody`. Time comes from `new Date()` and `System.currentTimeMillis()`.
6. **Wrong README.** It says login tokens last one day. The code and test say seven days.

## Goals
- Each permission slice file and every changed call site has a recorded verdict and conforms (AC-1, AC-2).
- Account creation, login, bearer access, role denial and invalid-token rejection behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Renaming `hasAuthority` or `getSelfId` | Used in 117 and 156 places across every feature; the names already read as questions at their call sites |
| Removing static `PermissionService.getSelf()` | Its two callers belong to the account and post slices, which will move them to `getSelfId()` |
| Changing token lifetime, claims, secret precedence or error responses | Security contract; preserved exactly |
| Reworking `JwtAuthenticationFilter` or `BrowserSessionService` beyond taking `LoginTokens` | They belong to the configuration slice |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every changed file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass, including new `LoginTokensTest` and `PermissionServiceTest`, and a style review of the full diff finds no blocker |
| AC-3 | The packaged candidate on isolated MongoDB `test` passes these checks, recorded in a published test report: creates an account through the API and logs in; the returned bearer token reads `/me` (200); the token is denied the admin account list (403); a tampered token and a missing token get 401 |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 3; on 2026-10-06 the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `0202b97b`:
  - `permission/PermissionService.java` and `PermissionServiceTest.java`, and the README.
  - Callers: `AccountAuthenticationService`, `JwtAuthenticationFilter`, `BrowserSessionService`, `SecurityConfig`, `AccountProfileService`, `PostService`.
  - Every test that issues or verifies tokens: `JwtAuthenticationFilterTest`, `BrowserSessionServiceTest`, `AccountServiceTest`, `SharedFolderSecurityIntegrationTest`, `RestaurantControllerMemberSecurityTest`.
  - `ControllerSliceSecurityTestConfig`, plus the web slice tests that import `SecurityConfig`: `AsyncDispatcherSecurityIntegrationTest`, `LocationControllerSecurityTest`, `SurviveControllerTest`.
  - `ApplicationClockConfiguration`, `app.jwt.secret` in `application.yml` and `application-prod.yml`, and jjwt 0.13.0.

## Branch
`claude/style-permission-20261006` from spoke `origin/main` `0202b97b`, in a linked worktree.

## Assumptions
- Two `LoginTokens` built from the same secret derive the same HMAC key, so a test can issue a token with its own instance that the context's bean verifies.
- The application `Clock` bean is `Clock.systemUTC()`, so tokens are issued and checked for expiry on the same time base as before.

## Open Questions
None.

## Design
`LoginTokens` is a final class with a private constructor and a `fromConfiguration` factory. The factory keeps the existing secret precedence (`app.jwt.secret`, then `APP_JWT_SECRET`, then `JWT_SECRET`, then the local development secret, which production refuses) and the Base64 and 32-byte rules.

- `issueFor(Account)` and `verifiedClaimsOf(String)` use the injected `Clock` and the current jjwt API.
- `PermissionConfiguration` builds the one bean.
- `AccountAuthenticationService`, `JwtAuthenticationFilter` and `BrowserSessionService` take it as a constructor dependency. `SecurityConfig` passes it in.
- `PermissionService` keeps `hasAuthority`, `getSelfId` and the static `getSelf`. `hasAuthority` resolves role names without exceptions and has no catch-all. The test-only `isAuthenticated` and `isAccountActive` are removed.

| Alternative | Why not |
|---|---|
| Keep static methods and only rename them | Leaves the global mutable key, which is the slice's main defect |
| Make `PermissionService` itself own the key as an instance | It is a SpEL target used everywhere; mixing token crypto into it keeps two jobs in one class |
| Rename `hasAuthority` to `holdsRoleAtLeast` | 117 SpEL call sites across all features for a name that already reads well |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/account/api/LoginTokens.java` | new | Owns key, lifetime and clock; `issueFor`, `verifiedClaimsOf` (rules 1, 7, 9) |
| `website/src/main/java/dev/christopherbell/account/auth/LoginTokensConfiguration.java` | new | Builds the `LoginTokens` bean (rule 7) |
| `website/src/main/java/dev/christopherbell/account/README.md` | changed | Names `api.LoginTokens` and `auth.LoginTokensConfiguration` |
| `website/src/main/java/dev/christopherbell/permission/PermissionService.java` | changed | Role checks only; no catch-all; no dead code (rules 8, 9) |
| `website/src/main/java/dev/christopherbell/permission/README.md` | changed | Correct seven-day lifetime and the two collaborators |
| `website/src/main/java/dev/christopherbell/account/auth/AccountAuthenticationService.java` | changed (call site) | Injected `LoginTokens.issueFor` |
| `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java` | changed (call site) | Full constructor takes `LoginTokens`; bearer path needs it |
| `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java` | changed (call site) | Constructor takes `LoginTokens` |
| `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java` | changed (call site) | Passes the bean to both |
| `website/src/test/java/dev/christopherbell/account/api/LoginTokensTest.java` | new | Claims, lifetime, bearer prefix, expiry, foreign signature, secret precedence and length (rule 10) |
| `website/src/test/java/dev/christopherbell/account/api/LoginTokensFixture.java` | new | Local development tokens and a test configuration bean |
| `website/src/test/java/dev/christopherbell/permission/PermissionServiceTest.java` | changed | Full role-rank table, denial cases, current account id (rule 10) |
| `website/src/test/java/dev/christopherbell/configuration/JwtAuthenticationFilterTest.java`, `configuration/security/browser/BrowserSessionServiceTest.java`, `account/AccountServiceTest.java`, `sharedfolder/SharedFolderSecurityIntegrationTest.java`, `whatsforlunch/restaurant/RestaurantControllerMemberSecurityTest.java` | changed (call sites) | Issue and verify through `LoginTokens` |
| `website/src/test/resources/architecture-baseline/e847d3fd-3e97-4258-ac91-4674dc7531ae` | changed | Two resolved frozen violations removed |
| `website/src/test/java/dev/christopherbell/configuration/security/ControllerSliceSecurityTestConfig.java`, `configuration/security/AsyncDispatcherSecurityIntegrationTest.java`, `location/LocationControllerSecurityTest.java`, `survive/SurviveControllerTest.java` | changed (wiring) | Provide `LoginTokens` to the security beans |

## Task Breakdown

### Task 1 - Move login tokens into an injected owner and conform permission checks

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Slice 2 opened; independent code |
| **Files** | As listed in Expected Changes |
| **Symbols** | `LoginTokens.fromConfiguration`, `issueFor`, `verifiedClaimsOf`, `resolveSecret`, `TOKEN_LIFETIME`; `PermissionConfiguration.loginTokens`; `PermissionService.hasAuthority`, `getSelfId`, `getSelf`; constructors of `JwtAuthenticationFilter` and `BrowserSessionService`; `AccountAuthenticationService.loginAccount` |
| **Inspection** | All files in Inputs at `0202b97b` |
| **Behavior** | Same token claims (`role`, fingerprint, `jti`, subject), seven-day expiry, `Bearer ` prefix tolerance, secret precedence, production refusal and 32-byte rule; same role ranking and denials |
| **Invariants** | One signing key per application context; no static mutable state; no catch-all in authorization |
| **Boundary/API** | `@permissionService.hasAuthority(...)` and `getSelfId()` unchanged; token wire format unchanged so existing browser logins stay valid across the deploy |
| **Effects and failures** | Invalid, foreign-signed or expired tokens raise jjwt exceptions, which the filter already turns into credential rejection; startup fails for a missing production secret or a short secret, as before |
| **Tests and evidence** | New unit tests for both classes; all existing filter, session, account and security slice tests pass with the new wiring |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | `LoginTokensTest`, `PermissionServiceTest`, `JwtAuthenticationFilterTest`, `BrowserSessionServiceTest`, `AccountServiceTest` | verify-local-app: on isolated MongoDB `test`, create an account through `POST /api/accounts/2024-12-15/create`, log in, then call `/api/accounts/2025-09-03/me` (200), `GET /api/accounts/2024-12-15` (403), `/me` with a tampered token (401) and without a token (401) |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info`; production `/actuator/health` stays UP |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. Tokens issued before or after are interchangeable because the wire format and key derivation are unchanged.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A context lacks the `LoginTokens` bean and fails to start | Medium | Full test suite covers every web slice; runtime startup proves the application context |
| Existing user sessions break after deploy | Low | Same secret, key derivation and claims; checked by `tokensFromTheSameSecretVerifyAcrossInstances` |
| A defect in `hasAuthority` now surfaces as an error instead of a silent deny | Low | Intended: a defect fails closed with a visible error rather than looking like a normal denial |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I inspected and edited directly while slice 2's CI ran.
- **Impact:** No PR exists yet; the plan and runtime report are published before it.

### 2026-10-06 - LoginTokens lives in the account area's published API

- **Change:** `LoginTokens` moved from `permission` to `account.api`, its bean factory became `account.auth.LoginTokensConfiguration`, and the test and fixture moved to `account.api`.
- **Reason:** `ModularMonolithArchitectureTest.legacyInternalCrossAreaAccessDoesNotGrow` failed. `permission` belongs to the `account` area and is never published, so `JwtAuthenticationFilter`, `BrowserSessionService` and `SecurityConfig` reaching `permission.LoginTokens` counted as three new cross-area accesses. Growing the frozen baseline would weaken the safeguard; `account.api` is the published route the rule allows.
- **Impact:** Two frozen violations (`configuration` to `permission.PermissionService`) disappear because those classes no longer use it.

### 2026-10-06 - Foreign-signature test used a longer secret

- **Change:** `rejectsATokenSignedWithADifferentSecret` now uses a foreign secret of the same length as the configured one.
- **Reason:** jjwt picks HS384 for a 49-byte key, so verification failed with `WeakKeyException` instead of `SignatureException`.
- **Impact:** Test-only.

### 2026-10-06 - Rebased onto main c746d0e2

- **Change:** The unpushed candidate was rebased onto `c746d0e2`, which changed `SurviveControllerTest` from another session. The rebase was clean, and the full check reruns on the rebased candidate.
- **Reason:** The ruleset requires branches to be up to date.
- **Impact:** None to scope.

### 2026-10-06 - Frozen architecture store drops the two resolved entries

- **Change:** `website/src/test/resources/architecture-baseline/e847d3fd-...` lost its two `configuration -> account ... -> PermissionService` lines, regenerated by running the architecture test once with `archunit.freeze.store.default.allowStoreUpdate=true`.
- **Reason:** The store is read-only by default, so the rule fails when frozen violations are fixed until the store is shrunk. The diff is two deletions and no additions.
- **Impact:** One more file in the change; the safeguard is tighter, not weaker.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
