# Deploy-Aware Merges and Shared Verification Helpers

## Document Status
complete

## Objective

> [!IMPORTANT]
> Builder's helpers can serialize spoke merges behind an auto-deploy, compare a candidate's responses with production, and update an umbrella plan's ledger. The Java style guide also records the migration's recurring decisions, so agents stop rebuilding these in session scratchpads.

## Background
The christopherbell-dev style migration ([umbrella plan](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md)) ran about thirty spoke PRs. That exposed four gaps:

1. **No deploy-aware merges.** christopherbell.dev deploys only `main`'s newest commit after its CI passes. Back-to-back merges kept production on one commit for over 30 minutes. `wait_for_github.py` merges each PR on its own, so I hand-wrote `merge_when_deployed.sh`. I also wrote `watch_slice_pr4.sh`, which updates a branch that falls behind main, a case `pr` mode does not handle.
2. **Comparison helpers lived in the scratchpad.** `compare_json_shape.py`, `compare_status_and_body.py` and `compare_text_body.py` had to be re-debugged twice: once for an Accept header that caused 406s, and once because the edge blocked Python's default User-Agent.
3. **No ledger helper.** Each slice closed its umbrella ledger row through the scratchpad script `close_part.py`.
4. **Undocumented style decisions.** The same calls were re-argued in every slice plan's Non-Goals: block `if`s, imports over fully qualified names, `OrNull` lookups, named status sets and catch names.

The user asked for these fixes ("Fix 2, 3, 4, 5, 7"). This plan covers the Builder side of items 2, 3 and 5. The spoke's candidate start and stop scripts, its admin fixture, Checkstyle and the Windows build setup are spoke changes with their own plans.

## Goals
- Registered spokes can declare automatic deployment, and the hub check validates the declaration (AC-1).
- `wait_for_github.py` can serialize merges behind deployment, wait for a commit to be live, and update a branch that falls behind (AC-2).
- verify-local-app ships a tested response comparison helper (AC-3).
- write-implementation-plan ships a tested ledger-row helper and documents umbrella ledgers (AC-4).
- The Java guide records the recurring decisions, and the skills point at the new helpers (AC-5).

## Non-Goals

| Not doing | Why |
|---|---|
| Moving `start-candidate.ps1` into Builder | It encodes the spoke's run configuration, which the spoke owns; it moves to the spoke under its own plan |
| Running deploy status commands such as `prod.cmd auto-status` from Builder | Deployment commands belong to the spoke; the public live-commit URL is enough |
| Per-slice migration plans or parallel slice sessions | The user did not choose items 1 and 6 |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | A spoke entry may carry `autoDeploy` with an https `liveCommitUrl` and a `liveCommitPattern` that has exactly one capture group. The registry rejects anything else, and christopherbell-dev declares it |
| AC-2 | `wait_for_github.py` adds a `deployed` mode, which waits until the live commit equals or descends from a given commit, and a `queue` mode, which merges PRs one at a time, each only after production serves the default branch's head. `pr` mode updates a branch that falls behind, once per head. Unit tests cover each mode |
| AC-3 | `compare_responses.py shape` and `same` compare JSON shape or status and body against a reference, with a configurable Accept header, User-Agent and ignored fields. Tests run them against a local HTTP server |
| AC-4 | `update_ledger_row.py` replaces exactly one occurrence of the given text in the one ledger row it names, preserves line endings, validates the plan, and leaves the file unchanged on failure. Tests cover each case |
| AC-5 | `python .agents/run_tests.py` and `check_hub.py` pass, and the skills, AGENTS.md and the Java guide describe the new helpers and decisions |

## Inputs
- **Request:** "Fix 2, 3, 4, 5, 7", following my list of what would have given me more agency.
- **Inspected at Builder `1f6c824`:**
  - `.agents/skills/deliver-change/scripts/wait_for_github.py` and its tests.
  - `.agents/lib/spoke_registry.py` and its tests.
  - `spokes.json`.
  - The verify-local-app and publish-spoke-changes skills and their `openai.yaml`.
  - write-implementation-plan's update reference and `log_plan_change.py`.
  - The Java style reference.
- **Scratch sources:** `merge_when_deployed.sh`, `watch_slice_pr4.sh`, the three compare scripts and `close_part.py`.

## Branch
Builder `main` through publish-builder-changes.

## Assumptions
None.

## Open Questions
None.

## Design
- **Registry:** `autoDeploy` is an optional object on a spoke entry.
  - `Spoke.auto_deploy` holds an `AutoDeploy(live_commit_url, live_commit_pattern)`, or `None` when the spoke doesn't declare one.
  - Its presence means the default branch deploys automatically after CI.
- **Live commit:** `deployed` and `queue` read the commit from the spoke's live URL using its pattern.
  - A commit counts as live when GitHub's compare API reports the live commit `identical` to it or `ahead` of it.
  - `queue` reads the default branch head from `gh api repos/<repo>/commits/<branch>`.
- **Queue:** releases each PR only once the live commit equals the default branch head. It then runs the existing `pr` wait with merging. A failure stops the queue with that PR's exit code. After the last merge it waits for that merge to be live. `--timeout-minutes` bounds each PR's whole cycle.
- **Behind branches:** when `mergeStateStatus` is `BEHIND`, `pr` mode calls `gh pr update-branch` once per head commit, then keeps waiting.
- **Comparison:** `compare_responses.py` uses only the standard library. It sends the given Accept header and a non-default User-Agent, and treats HTTP error statuses as data. It exits 0 on a match, 1 on a difference and 2 on unusable input.
- **Ledger rows:**
  - The row is the table line whose first cell equals `--row`.
  - The replacement must occur exactly once in that row.
  - The write goes through `builder_hub.write_text`, with the original line endings restored.
  - `validate_implementation_plan_text` must pass before writing.

## Expected Changes

| File | Change |
|---|---|
| `.agents/lib/spoke_registry.py` | `AutoDeploy` and its validation |
| `spokes.json` | christopherbell-dev `autoDeploy` |
| `.agents/skills/deliver-change/scripts/wait_for_github.py` | `deployed` and `queue` modes; behind-branch update |
| `.agents/skills/verify-local-app/scripts/compare_responses.py` | New |
| `.agents/skills/write-implementation-plan/scripts/update_ledger_row.py` | New |
| `.agents/tests/test_spoke_registry.py`, `test_wait_for_github.py`, new `test_compare_responses.py`, new `test_update_ledger_row.py` | Tests |
| `.agents/skills/verify-local-app/SKILL.md`, `publish-spoke-changes/SKILL.md`, `write-implementation-plan/references/update.md`, `write-chris-street-style-code/references/java.md`, `AGENTS.md`, related `agents/openai.yaml` | Documentation |

## Task Breakdown

### Task 1 - Registry and waiter

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `spoke_registry.py`, `spokes.json`, `wait_for_github.py` and their tests |
| **Symbols** | `AutoDeploy`, `Spoke.auto_deploy`, `wait_for_deployed_commit`, `merge_queue`, `wait_for_pull_request` |
| **Inspection** | Inputs |
| **Behavior** | As in Design; `pr` and `live` behavior is otherwise unchanged |
| **Invariants** | Merges still use `--match-head-commit`; reruns stay at one per run |
| **Boundary/API** | New CLI modes; new optional registry field |
| **Effects and failures** | `gh` and HTTP failures are retried until the timeout, then reported with exit 2 |
| **Tests and evidence** | Fake `gh` and fake clock unit tests |
| **Verification** | `python .agents/run_tests.py wait_for_github spoke_registry` |

### Task 2 - Comparison and ledger helpers

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `compare_responses.py`, `update_ledger_row.py` and their tests |
| **Symbols** | `json_shape`, `shape_differences`, `comparable_body`, `replace_in_ledger_row` |
| **Inspection** | Scratch sources; `log_plan_change.py` for helper conventions |
| **Behavior** | As in Design |
| **Invariants** | The ledger helper never changes bytes outside the named row |
| **Boundary/API** | New CLIs |
| **Effects and failures** | Network errors exit 2 |
| **Tests and evidence** | Local `ThreadingHTTPServer`; temporary plan files |
| **Verification** | `python .agents/run_tests.py compare_responses update_ledger_row` |

### Task 3 - Skills and style decisions

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 and 2 |
| **Files** | Documentation in Expected Changes |
| **Symbols** | None |
| **Inspection** | Inputs |
| **Behavior** | The skills name the helpers; the Java guide records the decisions |
| **Invariants** | Each skill's entrypoint, references and metadata stay aligned |
| **Boundary/API** | None |
| **Effects and failures** | None |
| **Tests and evidence** | Skill consolidation tests |
| **Verification** | `python .agents/run_tests.py` and `python .agents/skills/publish-builder-changes/scripts/check_hub.py --root .` |

## Test Plan

**Runtime proof not applicable:** Builder helpers and skill documentation have no runnable application. The unit tests exercise the helpers, including a real local HTTP server for the comparison helper.

| AC | Check |
|---|---|
| AC-1 | Registry tests; hub check |
| AC-2 | Waiter tests |
| AC-3 | Comparison tests |
| AC-4 | Ledger tests |
| AC-5 | Full test run; hub check |

## Rollback or Recovery
Revert the Builder commit. The registry field is optional, so older readers ignore it.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The queue waits forever on a spoke whose deploy is broken | Low | Each PR's cycle is bounded and exits 2 with the last live commit it saw |

## Implementation Log
No entries yet.

## Outcome

> [!NOTE]
> Delivered as planned. Builder can now serialize spoke merges behind an auto-deploy, confirm that a merge is live, compare a candidate with production and update umbrella ledger rows. The Java guide records the migration's settled decisions.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | Pass | `AutoDeploy` validation and two new registry tests; christopherbell-dev declares `autoDeploy`, and its pattern read production commit `280b3c6` from `/actuator/info` |
| AC-2 | Pass | Seven new waiter tests (behind branch, deployed, queue order, queue stop, repository parsing); `deployed --spoke christopherbell-dev --commit b492f6a0` against production exited 0 ("Production serves 280b3c6, which contains b492f6a") |
| AC-3 | Pass | `test_compare_responses.py`: 6 tests against a local `ThreadingHTTPServer` |
| AC-4 | Pass | `test_update_ledger_row.py`: 3 tests, including CRLF preservation and unchanged files on failure |
| AC-5 | Pass | `python .agents/run_tests.py`: 16 of 16 files, 174 tests; `check_hub.py`: hub state validation passed |

Follow-up: the spoke-side items (candidate scripts and Windows build setup, the test admin fixture and Checkstyle) ship under their own christopherbell-dev plans.

## Project
builder

## Plan Format
task-contract-v2
