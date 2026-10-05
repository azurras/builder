# Add repository-local Chris Street Style guidance

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Give christopherbell.dev contributors concise repository-local coding guidance aligned with the Builder Chris Street Style standard and existing project rules.

## Background
The repository already defines package ownership, effect boundaries, tests, and documentation expectations, but its `AGENTS.md` does not state the cross-language naming and failure-handling conventions the user selected for this whole-codebase audit. A short guidance section can make future edits consistently reviewable without copying the full Builder skill or changing application behavior.

## Goals
- Add actionable cross-language rules for descriptive names, distinct names for materially transformed values, validation at boundaries, explicit effects, preserved causes, and behavior-focused tests (AC-1).
- Preserve existing architecture, security, frontend, testing, and worktree instructions (AC-1).
- Verify the changed application repository locally and record startup outcome before any PR (AC-2).

## Non-Goals
| Not doing | Why |
|---|---|
| Replacing the Builder skill or copying its full text into the spoke | Keep one complete standard and only the concise local adaptation here. |
| Changing source code, build configuration, tests, or runtime behavior | This change only aligns agent instructions. |
| Creating or updating PR #1477 | The user explicitly excluded that draft. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `AGENTS.md` states concise, actionable Chris Street Style rules and existing instructions remain intact with no contradictory guidance. |
| AC-2 | The committed application is run locally and readiness/representative flow is verified, or the startup blocker and cleanup are recorded and no PR is created. |

## Inputs
- **Request:** User asked for the complete codebase to conform to the `write-chris-street-style-code` skill with targeted changes and an independent plan/report for each change; PR #1477 is untrusted.
- **Reviewed file:** `AGENTS.md` on `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Existing rules:** Architecture, frontend, security, documentation, testing, and worktree sections already cover package ownership, cause-aware failures, unit tests, and focused diffs; this change adds only the missing naming, transformation, boundary, effects, and proof emphasis.

## Branch
`codex/document-chris-street-style-guidance-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- The existing Builder skill remains available to contributors and is the detailed standard.
- The same incomplete migration-015 durable record may block packaged startup against the isolated test database.

## Open Questions
None.

## Design
Add a compact `Chris Street Style` subsection adjacent to the architecture/testing guidance. Direct contributors to read calls as sentences; use names that describe domain role and units; give materially transformed data a new name; validate external input before reliance; preserve error causes and keep effects/ownership explicit; choose direct structure and tests that prove observable behavior. Existing project architecture and native tool guidance remain authoritative.

| Alternative | Why not |
|---|---|
| Paste the entire Builder skill into `AGENTS.md` | It would duplicate a larger evolving policy and burden routine repository orientation. |
| Add only a link to the skill | The repository has useful concise local rules; directly state the few principles needed for everyday review. |

## Expected Changes
| File or area | Change |
|---|---|
| `AGENTS.md` | Add one concise language-neutral style section that complements existing project rules. |

## Task Breakdown
### Task 1 - Add concise repository style rules
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `AGENTS.md`; inspected at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `Chris Street Style` subsection and its concise principles. |
| **Inspection** | Read the complete root `AGENTS.md`, website README, and Builder skill summary and implementation rules. |
| **Behavior** | Agent/contributor instructions direct code toward readable, explicit, causally safe changes without changing runtime behavior. |
| **Invariants** | Preserve all existing architecture, security, frontend, testing, deployment and worktree instructions; no duplicate skill bundle. |
| **Boundary/API** | Markdown-only instruction contract; no source, API, configuration, or build interface changes. |
| **Effects and failures** | No runtime effects; instruction must not authorize unverified production actions or weaken security guidance. |
| **Tests and evidence** | Inspect full final diff, verify links/heading structure and `git diff --check`; record packaged startup attempt as required for an application repository. |
| **Verification** | Validate the instruction diff and package with `:website:bootJar`; run the committed application with test profile, isolated Mongo database `test`, test storage, disabled schedules/integrations, and free loopback port. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review Markdown structure, existing guidance preservation, links and `git diff --check`. No code-specific unit test applies. | Start the packaged application and verify readiness plus a representative existing flow; the document itself has no runtime path. |
| AC-2 | Build the committed candidate with `:website:bootJar`; confirm `git diff --check` and inspect the complete instruction diff. | Verify isolated configuration and candidate readiness, or record the startup blocker, process cleanup, database identity, and free port. |

Regressions and edge cases:
- Ensure wording does not contradict existing language/framework, security, or test instructions.
- Keep the section short and actionable; avoid copying the entire Builder skill.

## Rollback or Recovery
Remove the added subsection from `AGENTS.md` if review finds a conflict. No application or data recovery is required. If packaged startup is blocked by migration 015, stop only the candidate and do not alter database state.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Guidance conflicts with existing repository conventions | Low | Place only cross-cutting principles in the new section and inspect adjacent instructions. |
| Application runtime remains unavailable | High based on current audit evidence | Record the exact blocker and do not create a PR before local verification succeeds. |

## Implementation Log

### 2026-10-05 - Begin documentation implementation

- **Change:** Started the documentation-only change in its isolated worktree; narrowed native checks to Markdown/diff validation and packaging rather than rerunning behavior suites unchanged by the instruction file.
- **Reason:** The sole target is `AGENTS.md`; a source-code test suite cannot validate instruction wording, while the application startup requirement still applies.
- **Impact:** Task 1 is in progress; AC-1 still needs content/compatibility review and AC-2 still requires package build and local runtime evidence.

### 2026-10-05 - Verify guidance and block on database availability

- **Change:** Added a concise `Chris Street Style` section to spoke `AGENTS.md` on candidate `322fb12`; reviewed the full diff, passed `git diff --check`, and built `:website:bootJar` successfully.
- **Reason:** Local instructions now surface the selected standard's core cross-language rules without duplicating the full Builder skill or conflicting with project rules.
- **Impact:** AC-1 is satisfied; AC-2 is blocked because MongoDB `127.0.0.1:27018` refused the read-only identity check for database `test`, so candidate startup was not attempted. See the [test report](../test-reports/2026-10-05-04-47-christopherbell-dev-add-repository-chris-street-style-guidance.md); no PR was created.

## Outcome
> [!CAUTION]
> Repository guidance and packaging checks are complete on candidate `322fb12`; local app verification is blocked because isolated MongoDB database identity cannot be checked while port 27018 refuses connections, so no PR was created.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Satisfied | Added concise, actionable cross-language Chris Street Style guidance; full diff review and `git diff --check` passed. |
| AC-2 | ⏸️ Blocked | `:website:bootJar` passed on `322fb12`, but `mongosh .../test ... db.getName()` returned `ECONNREFUSED` for `127.0.0.1:27018`; app startup was not attempted without verified isolated data. See [test report](../test-reports/2026-10-05-04-47-christopherbell-dev-add-repository-chris-street-style-guidance.md). |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
