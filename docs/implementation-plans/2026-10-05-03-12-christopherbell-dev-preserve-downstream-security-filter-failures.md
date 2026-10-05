# Preserve Downstream Security Filter Failures

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Keep credential rejection fail-closed while allowing downstream servlet-chain failures to reach their normal error handling exactly once.

## Background
`JwtAuthenticationFilter.doFilterInternal()` catches `Exception` around bearer/cookie authentication and `chain.doFilter()`. A downstream `IOException` or `ServletException` can therefore be converted into an unauthorized response for a protected request, or cause a public request's chain to be invoked again from `rejectCredential`. Existing tests cover valid/invalid credentials but not downstream failure propagation.

## Goals
- Keep invalid credentials and authentication lookup failures rejected, with public routes continuing anonymously as before (AC-1).
- Invoke the downstream chain outside the credential-failure catch so downstream checked failures propagate once without becoming 401 (AC-2).
- Add direct filter regressions and run full checks/package plus local runtime attempt/report (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change token validation, cookie rotation, or account fingerprint rules | The correction is limited to the exception boundary around downstream processing. |
| Change security matcher configuration or authorization decisions | Existing route visibility and role checks remain unchanged. |
| Translate downstream application failures into filter responses | The owning downstream filter/controller/error handler must receive its original failure. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Invalid bearer/cookie credentials still produce the established rejection behavior and authentication lookup runtime failures remain fail-closed. |
| AC-2 | For valid credentials, downstream `IOException`/`ServletException` reaches the caller unchanged and the chain is invoked once for both public and protected paths. |
| AC-3 | Focused filter tests and full website/library/browser/PowerShell checks/package pass; committed app receives a local startup attempt and candidate-specific report before PR. |

## Inputs
- **Request:** Full `christopherbell.dev` Chris Street Style audit with small targeted corrections and individual plans/reports; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java`, `doFilterInternal`, and `rejectCredential` at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- **Inspected tests:** `website/src/test/java/dev/christopherbell/configuration/JwtAuthenticationFilterTest.java`; existing valid/invalid bearer and browser-cookie tests do not assert downstream exception propagation.
- **Guidance:** Spoke `AGENTS.md`; Chris Street Style Java, design/API, errors, naming and test-review references.

## Branch
Create `codex/preserve-downstream-filter-failures-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c` after publishing this plan.

## Assumptions
- Bearer validation/account lookup and browser session resolution expose authentication failures as unchecked exceptions.
- Servlet downstream failures must remain owned by the servlet chain, including on public endpoints.
- Packaged app startup remains blocked by migration 015 on isolated test database `test`.

## Open Questions
None. Keep the catch only around credential resolution and rejection.

## Design
Resolve bearer or browser credentials inside a narrow `RuntimeException` boundary. On a credential-resolution failure, preserve the current `rejectCredential` behavior and return. After successful identity resolution, invoke `chain.doFilter` outside that boundary. If no credential resolves, keep the current rejection/anonymous path. Add tests with a valid signed token and a downstream chain that throws a known `IOException`, for both public and protected request matching; assert object identity and exactly one invocation. Retain existing invalid-token and account-lookup rejection tests.

| Alternative | Why not |
|---|---|
| Catch only `IOException` around the whole method | Servlet downstream `IOException` is not an authentication failure and must propagate. |
| Keep a broad catch and rethrow based on current authentication state | Adds hidden conditional translation after the chain has already failed. |
| Remove all authentication error handling | Invalid credentials and transient identity-store failures would not preserve established fail-closed responses. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java` | Separate credential resolution from downstream chain invocation and narrow credential handling to runtime failures. |
| `website/src/test/java/dev/christopherbell/configuration/JwtAuthenticationFilterTest.java` | Assert checked downstream failures propagate unchanged and the chain runs exactly once for public/protected requests. |

## Task Breakdown
### Task 1 - Separate credential and downstream failures
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the filter and test class on base `695a3ed8617f9b4ab07abb7413baf369c58acf6c`. |
| **Symbols** | `doFilterInternal`, `rejectCredential`, bearer lookup, browser session resolution, and valid/invalid credential tests. |
| **Inspection** | `chain.doFilter()` currently appears inside a broad `catch (Exception)`; rejection for public paths re-enters the chain. |
| **Behavior** | Credential rejection and successful identity are unchanged; downstream failures propagate without a second dispatch. |
| **Invariants** | Invalid identity remains unauthenticated; downstream chain executes at most once; no downstream exception is reclassified as bad credentials. |
| **Boundary/API** | No URL, role, token, cookie or response contract changes for valid/invalid authentication. |
| **Effects and failures** | Credential lookup may access account/session stores; the downstream servlet chain remains responsible for its own errors. |
| **Tests and evidence** | Baseline filter suite; add one checked-failure propagation case for public and protected valid-token flows; retain invalid-token/lookup tests. |
| **Verification** | Focused filter suite, full project check/package and committed local application startup using isolated test DB with report. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing invalid bearer, invalid cookie and lookup failure tests pass. | Start committed candidate using the test profile. |
| AC-2 | Downstream `IOException` is the same instance observed by the caller; chain invocation count equals one for public and protected requests. | Check readiness and representative route if startup succeeds. |
| AC-3 | Run full website/library/browser/PowerShell checks and `bootJar`; `git diff --check`. | Record startup result against isolated MongoDB `test`. |

Regression: a public invalid-token request still continues anonymously once; a protected invalid-token request still returns 401.

## Rollback or Recovery
Revert only the filter boundary/test change if established credential rejection behavior changes. Do not alter route matchers or authorization configuration as a runtime workaround.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Some expected credential failure is checked rather than unchecked | Low | Inspect the called authentication APIs and preserve their declared failure forms before narrowing. |
| Downstream failure handling changes status for a public/protected route | Low | Add both-route propagation tests and preserve all invalid-token tests. |
| Runtime remains blocked before readiness | High | Record exact migration blocker and do not create a PR without local runtime acceptance. |

## Implementation Log

### 2026-10-05 - Begin isolated implementation

- **Change:** Started the isolated candidate from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c` in `codex/preserve-downstream-filter-failures-20261005`.
- **Reason:** The reviewed plan is published and authentication API inspection confirmed credential failures are unchecked while servlet-chain failures are checked.
- **Impact:** Task 1 begins as designed; no acceptance criteria or scope changed.

### 2026-10-05 - Record checks and runtime blocker

- **Change:** Implemented the planned narrow credential-resolution catch and added public/protected `IOException` and `ServletException` propagation regressions. Candidate `9820b394` passed 18 focused tests, the full native gate (2,045 website tests; 110 skipped), and the standalone 99-test deployment suite. The committed JAR startup attempt was blocked at migration 015; see the [candidate test report](../test-reports/2026-10-05-03-27-christopherbell-dev-preserve-downstream-security-filter-failures.md).
- **Reason:** The baseline regressions showed downstream failures being reclassified as credential rejection or dispatched twice. Runtime acceptance remains required before PR creation, and the test database has an incomplete migration record.
- **Impact:** AC-1 and AC-2 pass. AC-3 native checks pass but runtime proof is blocked; no PR was created. Await supported isolated database provisioning or recovery, then rerun startup and a route.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
