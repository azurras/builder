# Name Email Sanitizer Stages and Preserve Parse Causes

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Make email normalization stages and domain roles clear by name, and preserve only the expected low-level parsing cause when invalid IPv6 or IDN input is translated to the sanitizer's safe validation message.

## Background
`EmailSanitizer` reuses one-character `s`, `lt`, `gt`, `at`, `addr`, and `c0` names across parsing stages. Its IPv6 and IDN branches catch every `Exception` and translate without retaining causes. The shared library's `EmailSanitizerTest` passes on the current baseline, including wrappers, Unicode domains, and invalid IPv6/IDN input.

## Goals
- Give email parsing and normalization stages role-specific names without changing accepted or rejected address forms (AC-1).
- Catch only the expected IPv6/IDN parse exceptions and retain causes behind the existing safe messages (AC-2).
- Add focused cause regressions, then run library and full module checks (AC-3).
- Verify the packaged app on isolated MongoDB database `test` and complete separate PR delivery (AC-4).

## Non-Goals
| Not doing | Why |
|---|---|
| Change the accepted email profile, canonical output, or error messages | This is a style and cause-retention correction; behavior stays stable. |
| Add DNS-based email deliverability checks | The sanitizer validates syntax and normalization only. |
| Repair the existing failed migration record in `test` | Database writes must follow a supported procedure; direct repair is prohibited. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Reused/abbreviated production locals are replaced with names for each parsing representation while output remains unchanged. |
| AC-2 | IPv6 parsing catches `UnknownHostException`; IDN conversion catches `IllegalArgumentException`; safe outer messages stay stable and causes remain attached. |
| AC-3 | Focused tests prove successful normalization and invalid IPv6/IDN causes; `:cbell-lib:check` and full module checks pass. |
| AC-4 | Packaged candidate starts and a representative route succeeds on isolated database `test`; report is published and PR merges with supported deployment health readback. |

## Inputs
- **Request:** User-requested whole-codebase Chris Street Style audit with targeted changes and separate plan/report evidence; draft PR #1477 is excluded.
- **Audit plan:** `docs/implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md`.
- **Inspected code:** `EmailSanitizer` and all website call sites at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected tests:** `EmailSanitizerTest`; baseline `:cbell-lib:test --tests dev.christopherbell.libs.security.EmailSanitizerTest` passed.
- **Guidance:** Builder Chris Street Style naming, Java, design/API and testing references; website `AGENTS.md` and `cbell-lib/README.md`.
- **Consumer contract:** Account registration/login/moderation use safe validation boundaries; password reset intentionally treats invalid email as no-op.

## Branch
`codex/email-sanitizer-causes-20261005` from website `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- `InetAddress.getByName` throws `UnknownHostException` for malformed IPv6 text; wrong address family remains a sanitizer `IllegalArgumentException`.
- `IDN.toASCII` reports invalid domain syntax as `IllegalArgumentException`.
- Attaching those parse causes does not expose them in public responses; external validation messages remain generic.

## Open Questions
- The isolated MongoDB database named `test` has a failed migration-015 record and no active cutover ledger. Runtime proof and PR creation remain blocked pending a supported fixture or recovery procedure.

## Design
Name each representation distinctly from stripped input through optional wrapper removal, control stripping, Unicode normalization, validated local part and normalized domain. Replace the IPv6 broad catch with `UnknownHostException` handling and retain the cause in the existing safe message. Retain the IDN conversion cause while catching only `IllegalArgumentException`; unrelated runtime failures remain visible.

| Alternative | Why not |
|---|---|
| Keep a single mutable `s` or `domain` through every stage | The stored representation changes several times and is not apparent at each validation. |
| Keep `catch (Exception)` to normalize every failure to invalid input | It can misclassify programming defects as user input and drops useful parsing context. |
| Include the raw email or JDK exception message in the user-facing error | Email is personal data; preserve the current safe generic messages. |

## Expected Changes
| File or area | Change |
|---|---|
| `cbell-lib/src/main/java/dev/christopherbell/libs/security/EmailSanitizer.java` | Name the normalization stages/roles and narrow translated parsing failures while retaining safe cause chains. |
| `cbell-lib/src/test/java/dev/christopherbell/libs/security/EmailSanitizerTest.java` | Preserve existing normalization cases, add cause assertions, and clarify touched test input names. |

## Task Breakdown
### Task 1 - Clarify email parsing stages and failures
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the sanitizer, its callers, feature error boundaries and existing test class in a clean main-based worktree. |
| **Symbols** | `EmailSanitizer.sanitize()`, `normalizeDomain()`, and focused tests. |
| **Inspection** | Base `695a3ed8617f9b4ab07abb7413baf369c58acf6`; baseline sanitizer tests passed. |
| **Behavior** | Existing wrappers, accepted addresses, normalized output, rejection categories and safe messages remain stable. |
| **Invariants** | Local part remains ASCII-only; IPv6 must be bracketed and resolve as IPv6; IDN uses STD3 rules. |
| **Boundary/API** | Public sanitizer signature and downstream account/password-reset behavior remain unchanged. |
| **Effects and failures** | No new I/O; syntax failures remain `IllegalArgumentException`; parse causes are attached without adding raw values to messages. |
| **Tests and evidence** | TDD for IPv6 and IDN cause retention; all existing normalization cases stay green; full module checks and local app runtime proof. |
| **Verification** | Run focused sanitizer tests, `:cbell-lib:check`, `:website:check :cbell-lib:check`, inspect the final diff, and verify packaged startup plus a representative route on isolated database `test`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review each transformed value's name and existing normalization examples. | Start the candidate on isolated database `test`. |
| AC-2 | Assert the public safe message and expected nested cause class for invalid IPv6 and IDN input. | Exercise a representative application route after readiness. |
| AC-3 | Focused sanitizer suite, library check and full module checks. | Same candidate runtime exercise. |
| AC-4 | Required CI and merge readback. | Publish actual startup/route evidence and confirm supported deployment health for merge SHA. |

Regressions: mixed-case email and wrappers normalize as before; malformed IPv6 and IDN keep the same outer messages; underlying parsing exceptions remain available as causes.

## Rollback or Recovery
Before merge, revert only this isolated correction if accepted input or messages change. After merge, use a reviewed revert PR and supported automatic deployment; do not edit database records directly.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A rename changes which input representation a validation sees | Low | Keep each transformation explicit and retain the existing corpus of boundary tests. |
| Parse cause contains the invalid host text | Low | Keep generic outer messages; causes stay on server-side exception objects. |
| Runtime remains blocked by the failed test migration record | High | Do not open a PR until a supported isolated fixture/recovery procedure is supplied. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
