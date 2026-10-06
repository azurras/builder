# Close the Remaining Agent Friction in the Builder Loop

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Agents record runtime evidence mechanically, clean up merged worktrees without a hand-off, pass Markdown to helpers without shell quoting, and trust the test runner and preflight to see current state.

## Background
After [the first agency round](2026-10-05-17-46-builder-give-agents-more-agency-in-the-builder-loop.md), the user asked what else could improve and approved items 1, 2, 3, 4 and 6 of the answer:

1. **(1)** The session's permission classifier refused the worktree prune run.
2. **(3)** Test reports were still written by hand, the slowest step of every delivery.
3. **(4)** About 100 kept worktrees were unmerged by ancestry, although many belonged to merged pull requests.
4. **(6)** Plan, report and memory helpers read bodies only from stdin, so shell quoting broke Markdown; the preflight read stale refs unless fetched first; concurrent memory writers could collide.

Item 2 (production log access) is a christopherbell.dev change with its own plan.

## Goals
- A project permission rule lets agents run `prune-worktrees` (AC-1).
- `record_run.py` records command and HTTP cases and renders a report the validator accepts (AC-2).
- `prune-worktrees --pull-requests` treats a merged pull request's exact head as merged and reports each kept branch's PR state (AC-3).
- Body-writing helpers take `--body-file`; the preflight takes `--fetch`; memory appends are serialized (AC-4).
- Published to Builder `main` (AC-5).

## Non-Goals

| Not doing | Why |
|---|---|
| Removing unpublished, closed-PR or modified worktrees | They may hold work only the user can judge |
| Auto-merging Dependabot PRs | The user did not choose item 5 |
| Wider permission rules | Only the prune command was requested |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `.claude/settings.json` allows exactly the `prune-worktrees` command for the Bash and PowerShell tools, and the real prune run completes |
| AC-2 | `write-test-report/scripts/record_run.py` has `run`, `http` and `render`; masks secrets; tests prove a passing render validates as complete and a failing one renders as draft naming the failure |
| AC-3 | `--pull-requests` prunes worktrees whose HEAD is a merged PR head (clean and idle) and annotates kept ones; tests cover it; a run on christopherbell.dev is recorded |
| AC-4 | `--body-file` on save_session_memory, log_plan_change, save_implementation_plan and save_test_report; `preflight_spoke_pr.py --fetch`; a cross-process lock around memory appends; tests prove each |
| AC-5 | `python .agents/run_tests.py` and the hub check pass and the change is on Builder `origin/main` |

## Inputs
- **Request:** the user's 2026-10-05 reply "1,2,3,4 and 6".
- **Inspected:** `manage_spoke_repositories.py`, `.agents/lib/spoke_worktrees.py`, `builder_hub.read_stdin_text`, `project_memory.append_entry`, `preflight_spoke_pr.py`, `save_test_report.py`, `artifact_quality.validate_test_report_text`, `.agents/run_tests.py`.

## Branch
Builder primary checkout, `main`.

## Assumptions
- `gh` is authenticated where `--pull-requests` runs.

## Open Questions
None.

## Design
**Permission.** Project `.claude/settings.json` allows `python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py prune-worktrees *` for Bash and PowerShell. The command's own keep rules remain the safeguard.

**Recorder.** `record_run.py run|http` appends one JSON line per case to a scratch evidence file: the sent input, the received output (bounded to 20,000 characters), pass or fail against an expectation, timing and the candidate commit. Secret headers and common token shapes are masked before writing. `render` emits all report sections with fenced Data Sent and Response Received blocks; the status is `complete` only when every case passed.

**Pull requests.** One `gh pr list --state all` call maps branches to PR heads. A worktree whose HEAD equals a merged PR's head commit counts as contained. Kept worktrees get a note: never published, closed without merging, merged with later commits, or open.

**Helpers.** `builder_hub.read_body_text(body_file)` reads a UTF-8 file without a byte-order mark, or stdin. Memory appends take an exclusive lock file in the system temp folder keyed by the target path, waiting up to 30 seconds and taking over locks older than 120 seconds. `--fetch` runs `git fetch origin` with prompts disabled in the spoke and Builder before the checks.

| Alternative | Why not |
|---|---|
| Lock file beside the memory file | Could be committed or trip the hub check |
| A broad `python *` permission | Far wider than the request |

## Expected Changes

| File or area | Change |
|---|---|
| `.claude/settings.json` (new) | Prune allow rules |
| `.agents/skills/write-test-report/scripts/record_run.py` (new), `.agents/tests/test_record_run.py` (new) | Recorder and tests |
| `.agents/lib/spoke_worktrees.py`, `manage_spoke_repositories.py`, `test_spoke_worktree_prune.py` | PR-aware pruning |
| `.agents/lib/builder_hub.py`, the four save/log scripts, `.agents/lib/project_memory.py`, `test_project_memory.py` | `--body-file` and the lock |
| `preflight_spoke_pr.py`, `test_publish_spoke_changes.py` | `--fetch` |
| `.agents/run_tests.py` | Load files through unittest and fail files where no test ran |
| AGENTS.md and the write-test-report, save-session-memory, publish-spoke-changes and deliver-change docs | Document the new options |

## Task Breakdown

### Task 1 - Recorder
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | New `record_run.py`, new `test_record_run.py` |
| **Symbols** | `record_command`, `record_http`, `render_report` |
| **Inspection** | Report reference and `validate_test_report_text` |
| **Behavior** | Recorded cases render as a valid report |
| **Invariants** | Secrets never reach the evidence file; failures render as draft |
| **Boundary/API** | New CLI |
| **Effects and failures** | Runs the given command or request; appends to the evidence file |
| **Tests and evidence** | Local HTTP server and real subprocesses |
| **Verification** | `run_tests.py` |

### Task 2 - PR-aware pruning and permission
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `spoke_worktrees.py`, `manage_spoke_repositories.py`, `test_spoke_worktree_prune.py`, `.claude/settings.json` |
| **Symbols** | `pull_requests_by_branch`, `merged_heads_of`, `pull_request_summary`, `decide` |
| **Inspection** | Existing prune rules |
| **Behavior** | A merged PR's exact head counts as merged |
| **Invariants** | Clean, idle, unlocked and in-folder rules unchanged |
| **Boundary/API** | New `--pull-requests` flag |
| **Effects and failures** | One `gh` call; failure stops before removal |
| **Tests and evidence** | A branch that cannot merge cleanly into main is stale only with its PR head |
| **Verification** | `run_tests.py`; a run on christopherbell.dev |

### Task 3 - Helper ergonomics
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `builder_hub.py`, four helper scripts, `project_memory.py`, `preflight_spoke_pr.py`, their tests, `run_tests.py` |
| **Symbols** | `read_body_text`, `exclusive_append_lock`, `fetch_origin`, `run_test_file` |
| **Inspection** | Every `read_stdin_text` caller |
| **Behavior** | File bodies, serialized memory writes, fetched refs, honest test counts |
| **Invariants** | Stdin still works; append-only memory bytes unchanged |
| **Boundary/API** | New optional flags |
| **Effects and failures** | Temp lock file; network fetch only with `--fetch` |
| **Tests and evidence** | Body file with quotes and a BOM; eight concurrent writers; stale lock; local bare origins for fetch |
| **Verification** | `run_tests.py` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | None | The real prune run |
| AC-2 | `test_record_run.py` | No runnable application: the tests run the recorder end to end |
| AC-3 | `test_spoke_worktree_prune.py` | Dry run and real run with `--pull-requests` on christopherbell.dev |
| AC-4 | `test_project_memory.py`, `test_publish_spoke_changes.py` | No runnable application: CLI helpers exercised by tests |
| AC-5 | `run_tests.py`; `check_hub.py refresh` | Publication readback |

## Rollback or Recovery
1. Revert the Builder commit and delete `.claude/settings.json`.
2. Pruned worktrees are not restorable, but each one's HEAD is a merged PR head or already on `main`, so its content is on `main`.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A merged PR head worktree holds later local work | Low | Its HEAD must equal the PR head and the tree must be clean |
| A crashed writer leaves a lock | Low | Locks older than 120 seconds are taken over |

## Implementation Log

### 2026-10-05 - Implemented before the plan; test runner skipped a file

- **Change:** The code for AC-1 to AC-4 was written and tested before this plan was saved. The real prune run found the 24 ancestry-merged worktrees already removed by the user. The `--pull-requests` run then removed 67 more, leaving 61 of 152. `.agents/run_tests.py` now loads each file through unittest, prints the number of tests that ran, and fails a file in which none ran.
- **Reason:** The plan should have come first; this records the deviation. While writing memory tests, `test_project_memory.py` reported 0.1 seconds: it has no `__main__` block, so the previous runner executed it as a script that defined tests and ran none. The 2026-10-05 agency round reported "13 of 13 passed" without running those 9 memory tests.
- **Impact:** The full suite now reports 153 tests across 14 files, all passing, including the memory tests the old runner skipped.

## Outcome
Pending.

## Project
builder

## Plan Format
task-contract-v2
