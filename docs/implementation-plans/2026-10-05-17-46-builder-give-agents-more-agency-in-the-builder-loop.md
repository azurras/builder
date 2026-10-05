# Give Agents More Agency in the Builder Loop

## Document Status
ready-for-execution

## Objective

> [!IMPORTANT]
> Agents can wait on their own PRs and deploys, prove changes without keyword-matching or ceremonial reports, deliver small changes without a full plan, and run Gradle and Builder tests on this machine without workarounds.

## Background
At the end of the 2026-10-05 christopherbell.dev work, the user asked what limited the agent and then asked to fix items 3, 4, 5, 6, 8, 9 and 10 of its answer (item 7, Git long paths, the user fixed):

1. **(3)** The agent could not wait for CI success or a deploy without the user nudging it; the user said: "you should be able to poll when you need to."
2. **(4)** The test-report validator matches keywords, so three reports were reworded only to include phrases such as `HTTP/1.1 200`.
3. **(5)** The spoke preflight demands a complete report even for workflow-only or request-only PRs with no runnable change.
4. **(6)** Every change needs a full plan; the user said "small changes do not need a full plan".
5. **(8)** Gradle fails with "Unable to establish loopback connection" in agent shells unless the client gets `-Djdk.net.unixdomain.tmpdir`. A test showed the Gradle client alone needs it, and that a short `TEMP` does not help.
6. **(9)** `pytest` is not installed and Builder's tests are not importable as a package, so they ran file by file; Git Bash rewrote `origin/main:path` arguments.
7. **(10)** More than 100 stale worktrees accumulate beside christopherbell.dev.

## Goals
- A bounded Builder helper waits on a PR (re-running infrastructure-cancelled checks once, optionally merging) and on a live deploy (AC-1).
- A report section passes with a non-empty fenced block of real input or output, with keyword phrases still accepted (AC-2).
- The preflight accepts a published plan's recorded "runtime proof not applicable" reason instead of a report (AC-3).
- AGENTS.md and the plan skill define a small-change path without a new plan (AC-4).
- Gradle runs in agent shells without per-command setup, and the remedy is documented (AC-5).
- One command runs every Builder test without `pytest`, and the Git Bash path issue is documented (AC-6).
- A safe worktree pruning mode removes only clean worktrees already merged into the default branch, and it is run on christopherbell.dev (AC-7).
- All published to Builder `main` (AC-8).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the harness's own CI-polling guidance | Outside Builder; the user's instruction is recorded in policy and memory |
| Auto-applying Dependabot checksums | Not requested in this round |
| Pruning worktrees with changes, unmerged branches, or production deploy worktrees | Could discard work; ProgramData worktrees belong to production |
| Installing `pytest` | A stdlib runner avoids a new dependency |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `deliver-change/scripts/wait_for_github.py` has `pr` and `live` modes with interval and timeout bounds; unit tests prove merged, failed, infrastructure re-run, merge-when-green and live-match outcomes; deliver-change and publish-spoke-changes reference it |
| AC-2 | `validate_test_report_text` accepts Data Sent and Response Received that each contain a non-empty fenced block; keyword phrases still pass; empty sections still fail; tests prove all three |
| AC-3 | `preflight_spoke_pr.py --no-runtime-plan <plan>` passes for a published plan of the spoke that contains `**Runtime proof not applicable:** <reason>`, and fails when it is unpublished, belongs to another project or lacks the reason; tests prove it; `--report` behavior is unchanged |
| AC-4 | AGENTS.md, deliver-change and write-implementation-plan state when a change is small and how it is recorded instead of a new plan |
| AC-5 | User environment `GRADLE_OPTS` includes `-Djdk.net.unixdomain.tmpdir=C:\Temp\jdk-unix-sockets` and the folder exists; `gradlew.bat help` succeeds in a fresh process inheriting it; verify-local-app documents the remedy |
| AC-6 | `python .agents/run_tests.py` runs every Builder test file and reports pass or fail; AGENTS.md names it and the `MSYS_NO_PATHCONV=1` guidance |
| AC-7 | `manage_spoke_repositories.py prune-worktrees --spoke <slug> [--dry-run]` removes only linked worktrees under the spoke's sibling worktrees folder whose HEAD is reachable from `origin/<default>` and whose tracked content is unchanged (ignoring CR at end of line); tests prove kept and pruned cases; a dry run then a real run on christopherbell.dev are recorded |
| AC-8 | `run_tests.py` and the hub check pass, and the changes are on Builder `origin/main` |

## Inputs
- **Request:** the user's 2026-10-05 reply to the agent's limitations list.
- **Inspected:** Builder `main`: `.agents/lib/artifact_quality.py` (`validate_test_report_text` and its patterns), `.agents/tests/test_artifact_quality.py`, `publish-spoke-changes/scripts/preflight_spoke_pr.py`, `.agents/tests/test_publish_spoke_changes.py`, `deliver-change/scripts/manage_spoke_repositories.py`, `.agents/lib/spoke_registry.py`, AGENTS.md, and the SKILL.md files for deliver-change, publish-spoke-changes, write-implementation-plan and verify-local-app.
- **Observed:** Gradle `help` fails without `-Djdk.net.unixdomain.tmpdir` and succeeds with `GRADLE_OPTS` alone; `TEMP` is 36 characters.

## Branch
Builder primary checkout, `main`.

## Assumptions
- `gh` is authenticated wherever the wait helper runs.
- New agent shells inherit user environment variables after the desktop app restarts.

## Open Questions
None.

## Design
**Wait helper.** `wait_for_github.py pr --repo R --number N [--merge squash] --timeout-minutes 60 --interval-seconds 60` reads `gh pr view --json state,mergeStateStatus,headRefOid,statusCheckRollup` each interval. It exits 0 when the PR is merged, or after merging it with `--match-head-commit` once every check passes (with `--merge`). It exits 1 on a failed check, naming the failures. A check concluded `CANCELLED` or `STARTUP_FAILURE` gets one `gh run rerun --failed` per run. It exits 2 at the timeout.

`wait_for_github.py live --url U --expect TEXT` fetches the URL until the body contains TEXT. Both modes take injectable runners for tests.

**Report validation.** A section counts when it contains a fenced block with non-whitespace content, or one of the existing phrases.

**Preflight.** `--report` and `--no-runtime-plan` are mutually exclusive. The plan must sit under `docs/implementation-plans/`, be identical on `origin/main`, carry the spoke's Project and contain the bold label with a reason. The PR snippet links the plan and quotes the reason.

**Small changes.** A change is small when it stays inside an existing plan's goals (a follow-up), or touches at most three files with no data, schema, security or deployment-behavior change. A follow-up is recorded as an Implementation Log entry in that plan. Otherwise it is recorded as a session memory entry with the change, reason and verification. The existing verification and publication rules still apply.

**Gradle.** Set the user-level `GRADLE_OPTS`, preserving any existing value, create the folder, and document the symptom and remedy in verify-local-app.

**Tests.** `.agents/run_tests.py` discovers `test_*.py` under `.agents`, runs each file in its own process, and prints a summary.

**Prune.** The new mode lists `git worktree list --porcelain` for the spoke checkout. It keeps:

- the primary checkout;
- any worktree outside `<checkout>-worktrees` or `<checkout>.worktrees`;
- a worktree whose HEAD is not an ancestor of `origin/<default>`;
- a worktree with tracked changes beyond CR-at-end-of-line, or untracked non-ignored files;
- a locked worktree.

It removes the rest with `git worktree remove --force`, falling back to a long-path delete of the folder followed by `git worktree prune`. It also deletes a local branch when that branch is merged.

| Alternative | Why not |
|---|---|
| Install pytest | A new dependency for something stdlib does |
| `JAVA_TOOL_OPTIONS` user variable | Prints a notice from every Java process; only the Gradle client needs it |
| Removing keyword checks entirely | Older reports rely on them; additive acceptance is enough |

## Expected Changes

| File or area | Change |
|---|---|
| `.agents/skills/deliver-change/scripts/wait_for_github.py` (new) | PR and live wait helper |
| `.agents/tests/test_wait_for_github.py` (new) | Tests |
| `.agents/lib/artifact_quality.py`, `.agents/tests/test_artifact_quality.py` | Fenced-block acceptance and tests |
| `publish-spoke-changes/scripts/preflight_spoke_pr.py`, `.agents/tests/test_publish_spoke_changes.py` | `--no-runtime-plan` and tests |
| `deliver-change/scripts/manage_spoke_repositories.py`, `.agents/tests/test_spoke_worktree_prune.py` (new) | `prune-worktrees` mode and tests |
| `.agents/run_tests.py` (new) | Test runner |
| `AGENTS.md` | Small-change path, test runner, Git Bash note, wait helper |
| SKILL.md files: deliver-change, publish-spoke-changes, write-implementation-plan, verify-local-app, write-test-report | Wait helper, no-runtime path, small changes, Gradle remedy, report blocks |
| User environment (not tracked) | `GRADLE_OPTS` and `C:\Temp\jdk-unix-sockets` |

## Task Breakdown

### Task 1 - Wait helper
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | New `wait_for_github.py` (neighbor pattern: `triage_github_comments.py`), new `test_wait_for_github.py` |
| **Symbols** | `wait_for_pull_request`, `wait_for_live_text`, `main` |
| **Inspection** | `triage_github_comments.py` CLI style and `gh` usage |
| **Behavior** | Bounded waits with clear exit codes; optional merge; one re-run per infrastructure-cancelled run |
| **Invariants** | Never bypasses required checks; merges only the observed head; always ends by the timeout |
| **Boundary/API** | New CLI under deliver-change scripts |
| **Effects and failures** | `gh` calls and HTTP GETs; `gh` errors are retried on the next interval and reported at the timeout |
| **Tests and evidence** | Fake runner sequences for each outcome |
| **Verification** | `python .agents/run_tests.py`; a live `wait_for_github.py live` against production |

### Task 2 - Structural report validation
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `artifact_quality.py`, `test_artifact_quality.py`, `write-test-report` references |
| **Symbols** | `validate_test_report_text`, new `_has_nonempty_fenced_block` |
| **Inspection** | `artifact_quality.py:413-491` and the report tests |
| **Behavior** | Fenced input and output blocks satisfy the sections |
| **Invariants** | Empty sections fail; the unit-test-only rule and the application-run rule are unchanged |
| **Boundary/API** | Validator result list |
| **Effects and failures** | None |
| **Tests and evidence** | New accept and reject cases; the existing suite stays green |
| **Verification** | `run_tests.py` |

### Task 3 - No-runtime preflight
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `preflight_spoke_pr.py`, `test_publish_spoke_changes.py`, publish-spoke-changes and verify-local-app SKILL.md |
| **Symbols** | `check_no_runtime_plan`, `main` argument group |
| **Inspection** | Whole preflight script and its tests |
| **Behavior** | A plan-recorded reason replaces the report for non-runnable changes |
| **Invariants** | Checkout, branch, committed and ahead checks unchanged; `--report` unchanged |
| **Boundary/API** | New mutually exclusive flag |
| **Effects and failures** | Read-only |
| **Tests and evidence** | Pass, unpublished, wrong project and missing reason cases |
| **Verification** | `run_tests.py` |

### Task 4 - Small changes, Gradle, test runner, Git Bash
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | AGENTS.md, deliver-change, write-implementation-plan and verify-local-app SKILL.md, new `.agents/run_tests.py` |
| **Symbols** | "Small changes" paragraph; `run_tests.py main` |
| **Inspection** | AGENTS.md Documents and Quality sections; skill step 2 |
| **Behavior** | Small changes skip a new plan; tests run in one command; Gradle works |
| **Invariants** | Verification and publication rules unchanged |
| **Boundary/API** | Policy text; new CLI |
| **Effects and failures** | User environment variable write |
| **Tests and evidence** | `run_tests.py` itself; Gradle `help` in a fresh process |
| **Verification** | `run_tests.py`; `gradlew.bat help` |

### Task 5 - Worktree pruning
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 4 (runner) |
| **Files** | `manage_spoke_repositories.py`, new `test_spoke_worktree_prune.py`, deliver-change repository-inspection reference |
| **Symbols** | `prune_worktrees`, `prune-worktrees` subcommand |
| **Inspection** | `manage_spoke_repositories.py` and `spoke_registry.resolve_spoke_location` |
| **Behavior** | Clean, merged worktrees under the spoke's worktrees folder are removed; everything else is kept with a reason |
| **Invariants** | Never touches the primary checkout, unmerged or changed work, locked worktrees or paths outside the folder |
| **Boundary/API** | New subcommand with `--dry-run` |
| **Effects and failures** | Deletes folders and merged local branches; failures listed, not fatal |
| **Tests and evidence** | Temporary repositories with merged, unmerged, dirty, phantom-CRLF and outside-folder worktrees |
| **Verification** | `run_tests.py`; a dry run then a real run on christopherbell.dev |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | `test_wait_for_github.py` | `wait_for_github.py live` against production `/actuator/info` |
| AC-2 | `test_artifact_quality.py` | No runnable application: validator library |
| AC-3 | `test_publish_spoke_changes.py` | No runnable application: read-only CLI exercised by tests |
| AC-4 | Hub check | No runnable application: policy text |
| AC-5 | None | `gradlew.bat help` in a new process using the user environment |
| AC-6 | `run_tests.py` | Its own run output |
| AC-7 | `test_spoke_worktree_prune.py` | Dry run and real run on christopherbell.dev |
| AC-8 | `run_tests.py`; `check_hub.py refresh` | Publication readback |

## Rollback or Recovery
1. Revert the Builder commits.
2. Remove `GRADLE_OPTS` from the user environment.
3. Pruned worktrees cannot be restored, but only clean, merged ones are removed, so their content stays reachable from `main`.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Prune removes something wanted | Low | Strict keep rules, a dry run first, and a reason printed for every decision |
| The wait helper merges an unexpected head | Low | `--match-head-commit` with the head it observed green |
| The user `GRADLE_OPTS` affects other Gradle projects | Low | It only sets the socket folder |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
builder

## Plan Format
task-contract-v2
