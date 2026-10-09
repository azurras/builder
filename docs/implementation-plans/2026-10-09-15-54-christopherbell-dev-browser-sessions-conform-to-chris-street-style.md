# Browser Sessions Conform to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The `configuration.security.browser` package conforms to write-chris-street-style-code, and browser session creation, authentication, rotation, renewal and revocation behave exactly as before.

## Background
This is slice 18d of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 18c](2026-10-09-15-50-christopherbell-dev-security-configuration-conforms-to-chris-street-style.md). Inspection of the 12 files at `2e31f376` found:

1. **`BrowserSessionService.authenticate`:**
   - One 80-line method resolves, validates, rotates, falls back after a lost rotation, and touches activity.
   - Two `orElse(null)` lookups.
   - Repeated `parsed.get()`.
   - Reassigned `session` and `account` locals.
   - Five validity checks written out three times.
2. **`BrowserSessionService` elsewhere:** one-line `if` statements in `revokeAll`, `validCredential`, `parse` and `constantTimeEquals`, and unnamed token length limits (256, 32 and 128).
3. **`InteractiveBrowserRequest`:** six one-line `if` statements, and a `toLowerCase()` that depends on the default locale.
4. **`BrowserSessionAccount`:** a one-line `if`.
5. **Mongo adapters:**
   - `MongoBrowserSessionRepository` has one-line methods and annotations on the method line.
   - The activity and authentication stores split their imports out of order.
6. **Conforming:** `AuthenticatedBrowserSession`, `BrowserSession`, `BrowserSessionAuthentication` and the three store ports.

## Goals
- Every browser session file has a recorded verdict and conforms (AC-1, AC-2).
- Cookie sessions behave exactly as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing lifetimes, rotation interval, overlap, activity interval or token format | Security behavior |
| Changing which requests count as interactive | Security behavior; the conditions are only regrouped |
| The Mongo aggregation that joins the account | Persistence behavior; only its import order changes |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every browser session file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that a cookie login authenticates `/me`, a tampered or malformed cookie is rejected and cleared, logout revokes the session, and a CSRF-protected mutation succeeds with its header and fails without it |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `2e31f376`:
  - All 12 `configuration/security/browser` files.
  - `BrowserSessionServiceTest`, which covers creation, expiry, rotation, the lost-rotation race, previous-token overlap, activity writes and revocation.
  - `JwtAuthenticationFilterTest`, which drives real sessions through the filter.

## Branch
`claude/style-browser-sessions-20261009` from spoke `origin/main` `2e31f376`.

## Assumptions
None.

## Open Questions
None.

## Design
- **`authenticate(rawToken, interactive)`:** it parses the cookie, loads the stored session and delegates to a private `authenticate(stored, credential, interactive, now)`.
- **Private `authenticate`:**
  - It rejects and revokes when the session is not `usable` (the current or overlapping credential, not expired, a complete snapshot) or the account no longer validates.
  - It then returns at once for background requests, rotates when `dueForRotation`, touches activity when `dueForActivityWrite`, or returns unchanged.
- **`rotate`:** it performs the atomic rotation. When the rotation is lost, `afterLostRotation` accepts the secret only as the previous token and revokes otherwise.
- **Equivalence:** every combined condition is the original sequence of early returns joined with `||`, in the same order, so the set of revocations and results is unchanged.
- **Constants:** `MAX_RAW_TOKEN_LENGTH`, `MIN_SECRET_LENGTH` and `MAX_SECRET_LENGTH`.
- **`InteractiveBrowserRequest`:** it groups its background paths by feature with identical conditions and lower-cases with `Locale.ROOT`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java` | changed | Small named steps; `Optional` flow; named limits; block `if`s; sorted imports |
| `website/src/main/java/dev/christopherbell/configuration/security/browser/InteractiveBrowserRequest.java` | changed | Block `if`s; grouped conditions; `Locale.ROOT` |
| `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionAccount.java` | changed | Block `if` |
| `website/src/main/java/dev/christopherbell/configuration/security/browser/MongoBrowserSessionRepository.java`, `MongoBrowserSessionActivityStore.java`, `MongoBrowserSessionAuthenticationStore.java` | changed | Layout and import order |
| `AuthenticatedBrowserSession`, `BrowserSession`, `BrowserSessionAuthentication`, `BrowserSessionRepository`, `BrowserSessionActivityStore`, `BrowserSessionAuthenticationStore` | conforming | No change |

## Task Breakdown

### Task 1 - Conform browser sessions

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `BrowserSessionService.authenticate`, `rotate`, `afterLostRotation`, `usable`, `dueForRotation`, `dueForActivityWrite`, `revoked`; `InteractiveBrowserRequest.isBackground` |
| **Inspection** | All files in Inputs at `2e31f376` |
| **Behavior** | Same sessions, rotations, overlaps, renewals and revocations |
| **Invariants** | Stored fields, cookie format, lifetimes and queries unchanged |
| **Boundary/API** | None; public methods keep their signatures |
| **Effects and failures** | None new |
| **Tests and evidence** | Browser session, JWT filter, security and account suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | `BrowserSessionServiceTest` (rotation race, overlap, expiry, activity) | verify-local-app: the cookie flow in AC-3. Daily rotation and the lost-rotation race need a day of clock time or two racing requests, so the service tests cover them |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. Existing sessions are unaffected because stored data does not change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A session is revoked or kept differently | Low | Conditions are the original early returns combined in order; `BrowserSessionServiceTest` covers every branch and passes unchanged |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 18c was in its full check.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1519 (`6fe45a0`) and auto-deployed. Production serves `5b7ef3c`, which contains it, and `/robots.txt` returns 200. Later merges landed before the deploy finished, so production went straight to the newer head.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every browser session file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-16-02-christopherbell-dev-browser-sessions-conform-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 6 of 6 runtime cases passed on candidate `92bc169`, including cookie login, forged-cookie rejection, logout revocation and CSRF ([report](../test-reports/2026-10-09-16-02-christopherbell-dev-browser-sessions-conform-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1519](https://github.com/azurras/christopherbell.dev/pull/1519) merged as `6fe45a0` after all checks passed; production `/actuator/info` reports `5b7ef3c`, which contains it |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
