# Cbell-lib Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Slice 21 conforms to write-chris-street-style-code with unchanged behavior.

## Background
Slice 21 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) covers `cbell-lib`'s 65 Java files (4,386 lines). With its suppression removed, Checkstyle reported 27 mechanical violations, including one star import in `EmailSanitizerTest`. `PasswordUtil.parse` returns null in seven places for "not the current hash format", and four callers check for it.

## Goals
- Every file in scope conforms (AC-1, AC-2).
- Behavior is unchanged (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Behavior, contract or layout changes | The migration preserves behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in scope |
| AC-2 | The full check passes and a full-diff style review finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published report records the following. The bootstrap administrator, hashed at startup, logs in, and a new account signs up and logs in. A wrong password and an unknown account get the generic rejection, and the correct password still works afterwards. The application-wide sweep behaves as on main, and the log has no errors. `PasswordUtilTest` covers the legacy branches, which no API can create |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the files in scope at spoke `origin/main` `a0709b0e`.

## Branch
`claude/style-cbell-lib-20261012` from spoke `origin/main`; it merges `origin/main` before its PR when an earlier slice has changed the same file.

## Assumptions
None.

## Open Questions
None.

## Design
- **`PasswordUtil.parse`:** returns `Optional<EncodedHash>`, with empty meaning a legacy or malformed stored value. Verification, rehash, upgrade and iteration choice read it with `map` and `orElse`, which preserves every branch: legacy values derive with the legacy salt and iteration count, malformed current-format values fail closed, and constant-time comparison and cost padding are unchanged. The validity checks short-circuit in the same order, so a value that fails the iteration check is never decoded.
- **Mechanical rules:** applied by the checked fixers, the star import is expanded, and the cbell-lib suppression line is removed.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `cbell-lib/src/main/java/dev/christopherbell/libs/security/PasswordUtil.java` | changed | `Optional` parse; block bodies |
| Other flagged `cbell-lib` main and test files | changed | Block bodies, imports, layout |
| Remaining `cbell-lib` files | conforming | No change |
| `config/checkstyle/suppressions.xml` | changed | The slice 21 line is removed |

## Task Breakdown

### Task 1 - Conform slice 21

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | As named in Design |
| **Inspection** | Inputs |
| **Behavior** | Unchanged |
| **Invariants** | No route, contract, stored field or rendered value changes |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | As in Test Plan |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check with Checkstyle; full-diff review | Covered by AC-3 |
| AC-3 | `PasswordUtilTest` including legacy, malformed and upgrade cases | verify-local-app with `Start-Candidate.ps1 -WithTestAdministrator -EnableSharedFolder`: password checks and the application sweep |
| AC-4 | Required PR checks | `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Password verification changes outcome for some stored value | Low | Identical branch logic; unit tests for current, legacy, malformed and upgrade paths; runtime sign-in checks |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** These are mechanical or Settled-Decision edits made while earlier slices merged.
- **Impact:** No PR exists yet; the plan and evidence are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
