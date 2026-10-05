# Agents Watch and Merge Their Own Pull Requests

## Document Status
ready-for-execution

## Objective

> [!IMPORTANT]
> Agents treat watching a pull request through CI and merging it as part of the delivery loop, and contact the user only for what they cannot do themselves.

## Background
On 2026-10-05 the user told the agent working on christopherbell.dev: "don't wait for me to merge... part of the dev loop should be watching PRs and merging them yourself when it's time. human contact should only be needed for things you absolutely cannot do", then asked that the dev loop be updated. AGENTS.md already authorizes "the spoke branch, pull request, CI fixes and merge", but the agent still asked before every merge, for two reasons:

1. Nothing names watching and merging as the agent's own job, or how to do it without polling.
2. The production gate ("Production deployment ... the request did not name") reads as covering merges, because christopherbell.dev deploys automatically from `main` through its CI-gated poller.

The same day, CI jobs were cancelled when GitHub could not assign hosted runners. The loop says nothing about re-running them.

## Goals
- AGENTS.md states that watching and merging one's own PR is part of the loop, and that a spoke's supported automatic deployment from a verified merge is not a separate gate (AC-1).
- publish-spoke-changes says how to watch (auto-merge or the host monitor), to re-run infrastructure-cancelled jobs, and to merge without asking (AC-2).
- The hub check and skill tests still pass, and the change is published to Builder `main` (AC-3).

## Non-Goals

| Not doing | Why |
|---|---|
| Removing the production-data or non-pipeline deployment gate | Those still need the user |
| Changing Builder's own publication flow | Builder already commits straight to `main` |
| Enabling auto-merge on other repositories | Each spoke's settings are its own; christopherbell.dev enabled it 2026-10-05 |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | AGENTS.md has an "Own the PR to merge" rule, and its production gate row excludes a spoke's supported, CI-gated automatic deployment from a verified merge |
| AC-2 | publish-spoke-changes steps 5 and 7 name auto-merge or the host monitor, re-running infrastructure-cancelled jobs, and merging without asking the user |
| AC-3 | `check_hub.py refresh` and the publish-spoke-changes tests pass, and the commit is on Builder `origin/main` |

## Inputs
- **Request:** the user's 2026-10-05 instruction quoted above.
- **Inspected:** Builder `main` `AGENTS.md` (Scope and Autonomy, Quality and Delivery) and `.agents/skills/publish-spoke-changes/SKILL.md` (steps 5 to 7).

## Branch
Builder primary checkout, `main`.

## Assumptions
- Hosts without a PR monitor can use GitHub auto-merge or a bounded `gh pr checks --watch`.

## Open Questions
None.

## Design
Add one paragraph after the gate table in AGENTS.md and narrow the production row. Extend publish-spoke-changes step 5 with auto-merge, the monitor and infrastructure re-runs, and step 7 with "merge yourself; never ask". Alternative: a new skill for PR watching. It lost because the merge step already lives in publish-spoke-changes, and a second skill would split one procedure.

| Alternative | Why not |
|---|---|
| New PR-watching skill | Splits the merge procedure across two skills |
| Per-spoke instructions only | The rule applies to every spoke and agent |

## Expected Changes

| File or area | Change |
|---|---|
| `AGENTS.md` | Production gate row; new "Own the PR to merge" paragraph |
| `.agents/skills/publish-spoke-changes/SKILL.md` | Steps 5 and 7 |

## Task Breakdown

### Task 1 - Name merging as part of the loop
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `AGENTS.md`, `.agents/skills/publish-spoke-changes/SKILL.md` |
| **Symbols** | Section "Scope and Autonomy"; publish-spoke-changes "Steps" 5 and 7 |
| **Inspection** | Both files read at Builder `main` on 2026-10-05 |
| **Behavior** | Agents merge their own green PRs without asking, re-run infrastructure-cancelled jobs, and still stop at the remaining gates |
| **Invariants** | No required check is bypassed; production-data and non-pipeline deployment gates remain |
| **Boundary/API** | Shared policy for Claude Code, Codex and ChatGPT |
| **Effects and failures** | Documentation only |
| **Tests and evidence** | Hub check; publish-spoke-changes tests |
| **Verification** | `python .agents/skills/publish-builder-changes/scripts/check_hub.py refresh --root .`; `python -m pytest .agents/skills/publish-spoke-changes/tests -q` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Read the diff; hub check | No runnable application: policy text only |
| AC-2 | Read the diff; skill tests | No runnable application: policy text only |
| AC-3 | `check_hub.py refresh`; pytest | Publication readback on `origin/main` |

## Rollback or Recovery
Revert the commit on Builder `main`.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| An agent merges a PR the user wanted to review | Low | The user asked for this; scope, production-data and destructive gates remain |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
builder

## Plan Format
task-contract-v2
