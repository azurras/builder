# Agents fix what they hit and stop only at named approval gates

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Agents working from Builder carry a delivery request through to its completion boundary. They fix the failures they run into, and they stop for the user only at a short, explicit list of approval gates.

## Background
The user reported two habits that stop agents from finishing work:

1. Agents act as if an approval gate exists for routine steps when none does.
2. Agents meet a problem, record it, and wait for the user to tell them to fix it.

Evidence: on 2026-10-04 and 2026-10-05, more than twenty christopherbell-dev plans (for example [preserve Mongo probe failure causes](2026-10-05-00-34-christopherbell-dev-preserve-mongo-probe-failure-causes.md) and [disable test-profile scheduling](2026-10-05-04-06-christopherbell-dev-disable-test-profile-scheduling.md)) were set `blocked` on the same fixable cause: migration 015 failing in the isolated `test` database. Each one recorded that "an approved database fixture or provisioning procedure is required" and waited. A later change, [bootstrap isolated empty test database](2026-10-05-07-17-christopherbell-dev-bootstrap-isolated-empty-test-database.md), fixed the isolated setup in a single pass. The instructions add to the problem. AGENTS.md and the skills say "authorized", "authority" or "existing authority" dozens of times without listing which steps actually need the user. deliver-change's When Blocked section treats a red check or failed push as a reason to mark the plan blocked and report, with no instruction to fix the failure first.

## Goals
- AGENTS.md lists every approval gate and says that no other gate exists (AC-1).
- AGENTS.md and deliver-change tell agents to diagnose and fix failures, including prerequisites outside the plan, before they mark work blocked (AC-2).
- The skill phrases that read as extra gates point back to the AGENTS.md list, and verify-local-app says to repair a broken isolated environment instead of waiting for a fixture (AC-3).
- The hub check and Builder tests pass, and the change is published to Builder `origin/main` (AC-4).

## Non-Goals
| Not doing | Why |
|---|---|
| Unblocking the existing blocked christopherbell-dev plans | They are separate spoke work; the bootstrap change already removed their shared cause. |
| Loosening safety rules such as production isolation, no direct database writes, required CI or no force push | The user wants fewer invented gates, not fewer real safeguards. |
| Rewording every "authorized" in the skills | Most are harmless once AGENTS.md defines what they mean; a sweeping rewrite adds churn. |
| Changing the CLAUDE.md harness file | AGENTS.md is the shared policy that every agent reads. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | AGENTS.md Scope and Autonomy states that a delivery request covers every deliver-change step up to its boundary, gives the complete list of gates that need the user, and says that skill wording about authority adds no further gate. |
| AC-2 | AGENTS.md and deliver-change require diagnosing and fixing failed checks, builds, startups, pushes, helpers and environments, including out-of-plan prerequisites, before work is marked `blocked`. They allow `blocked` only for a listed gate or for a fix that is out of the agent's reach, and the record must say what was tried. |
| AC-3 | verify-local-app, publish-spoke-changes, save-session-memory and write-implementation-plan update mode match the new rules; verify-local-app says to repair or bootstrap an isolated environment that cannot reach readiness. |
| AC-4 | `check_hub.py check` and the Builder test suite pass, and the change commit is on Builder `origin/main`. |

## Inputs
- **Request:** The user, in chat on 2026-10-05, said that agents invent approval gates and wait instead of fixing the issues they hit.
- **Files read:** AGENTS.md; deliver-change, publish-builder-changes (with phase-finalization), publish-spoke-changes, save-session-memory, verify-local-app and write-implementation-plan (plan, update and review references), all at `f41a3e7`.
- **Evidence:** Blocked christopherbell-dev plans from 2026-10-04 and 2026-10-05, and the bootstrap plan that resolved their shared cause.

## Branch
Primary Builder checkout on `main` at `f41a3e7`.

## Assumptions
- Agents read AGENTS.md before the skills, so one authoritative gate list there governs the scattered skill phrases.
- No Builder test asserts the exact wording of the sections being changed. A grep found none, and the test suite will confirm this.

## Open Questions
None.

## Design
Put one authoritative list of approval gates in AGENTS.md Scope and Autonomy. State that a delivery request already covers every deliver-change step. Add a "fix what you hit" rule that says when `blocked` is allowed. In the skills, change only the sentences that currently create or imply a gate, or that send a failure straight to `blocked`. deliver-change's When Blocked becomes When Something Fails, which puts fixing first and asks agents to look for a shared cause when the same failure repeats. verify-local-app gets one explicit instruction to repair the isolated environment, because that was the observed failure.

| Alternative | Why not |
|---|---|
| Remove every "authorized" qualifier from the skills | Large churn, and limited-scope requests still need the distinction. |
| Add a separate autonomy reference file | AGENTS.md already owns authority policy; a second home would drift. |
| Only add a sentence to deliver-change | Agents also stall inside verify-local-app and publish-spoke-changes, and AGENTS.md is the shared policy. |

## Expected Changes
| File or area | Change |
|---|---|
| AGENTS.md | Rewrite Scope and Autonomy: what a delivery request covers, a table of gates, and the fix-what-you-hit rule. |
| .agents/skills/deliver-change/SKILL.md | Replace When Blocked with When Something Fails. |
| .agents/skills/verify-local-app/SKILL.md | Preflight: repair or bootstrap an isolated environment that cannot reach readiness; never fake guarded state. |
| .agents/skills/publish-spoke-changes/SKILL.md | State that a delivery request covers the change's own PR creation, comments and merge. |
| .agents/skills/save-session-memory/SKILL.md | State that delivery and change requests carry persistence authority. |
| .agents/skills/write-implementation-plan/references/update.md | Blocked: only after fix attempts, and log what was tried. |
| docs (plan, session memory, indexes) | This plan and the delivery memory. |

## Task Breakdown

### Task 1 - Define gates and the fix-first rule in AGENTS.md

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | AGENTS.md |
| **Symbols** | `## Scope and Autonomy` |
| **Inspection** | Read the full AGENTS.md at `f41a3e7`; Scope and Autonomy is a single paragraph. |
| **Behavior** | States what a delivery request covers, lists the gates that need the user, and requires fixing failures before `blocked`. |
| **Invariants** | Limited requests stay limited; the rules on production, data isolation, required checks and force pushes are unchanged; the trailing sentences on reading memory and reusing evidence stay. |
| **Boundary/API** | Policy text that every agent reads; no helper parses it. |
| **Effects and failures** | Documentation only. |
| **Tests and evidence** | Hub check; read the rendered section. |
| **Verification** | `python .agents/skills/publish-builder-changes/scripts/check_hub.py check --root .` |

### Task 2 - Align skills with the gates and the fix-first rule

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1, whose section these files refer to. |
| **Files** | .agents/skills/deliver-change/SKILL.md; .agents/skills/verify-local-app/SKILL.md; .agents/skills/publish-spoke-changes/SKILL.md; .agents/skills/save-session-memory/SKILL.md; .agents/skills/write-implementation-plan/references/update.md |
| **Symbols** | deliver-change `## When Blocked`; verify-local-app Preflight step 5; publish-spoke-changes intro paragraph; save-session-memory `## When to Write`; update.md `## When to Update` Blocked bullet |
| **Inspection** | Read each file at `f41a3e7`. |
| **Behavior** | Each file sends failures to diagnosis and repair first, and none implies a gate that is not in AGENTS.md. |
| **Invariants** | Skill frontmatter and links stay valid; the steps and their order are unchanged. |
| **Boundary/API** | Skill text only; the openai.yaml metadata stays accurate. |
| **Effects and failures** | Documentation only. |
| **Tests and evidence** | Hub check and the Builder unittest suite. |
| **Verification** | `python -m unittest discover -s .agents/tests` and `python -m unittest discover -s .agents/skills/publish-spoke-changes/tests`, then the hub check. |

## Test Plan
No runnable application applies: this change edits only policy and skill Markdown, so there is nothing to run locally. The native checks are the hub check and the Builder tests.

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Read the AGENTS.md diff against the criterion; the hub check passes. | Not applicable: policy text only. |
| AC-2 | Read the AGENTS.md and deliver-change diffs against the criterion. | Not applicable: policy text only. |
| AC-3 | Read each skill diff; the hub check validates frontmatter, links and the symlink. | Not applicable: skill text only. |
| AC-4 | Hub check, the `.agents/tests` suite, the publish-spoke-changes tests, and readback of `origin/main`. | Not applicable: no application. |

Regressions:
- Limited-scope wording (planning-only, review-only, inspection-only) is still present.
- The safety rules in verify-local-app (no direct database writes, production isolation) are unchanged.

## Rollback or Recovery
Revert the change commit on `main` with `git revert`; it touches only Markdown.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Agents read "fix it yourself" as permission to bypass safeguards | Medium | The rule says never to work around production, isolation or required-check rules, and to fix the isolated setup instead. |
| The gate list misses a real gate | Low | The list includes a general entry for consequential product decisions the repository cannot settle, plus access only the user holds. |
| Another session's uncommitted edits to today's memory file | Medium | Publish only this change's files; append memory after that session publishes, or commit only this session's entry. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
builder

## Plan Format
task-contract-v2
