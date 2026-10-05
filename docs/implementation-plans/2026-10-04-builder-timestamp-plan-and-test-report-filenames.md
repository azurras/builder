# Timestamp Plan and Test Report Filenames

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> New implementation plans and test reports are saved as `YYYY-MM-DD-HH-MM-project-title.md`, so several records made on one day carry their creation time and sort in the order they were made.

## Background
The user asked on 2026-10-04 for plans and test reports to carry hours and minutes after the date, because more than one is often created on the same day. Today the save helpers write `YYYY-MM-DD-project-title.md`, the hub validator and index generator only understand that shape, and AGENTS.md, README.md and the two skills document it.

## Goals
- The plan and report save helpers name new files with the local creation time as `HH-MM` after the date (AC-1).
- Replacing a record with `--overwrite` still finds the record for that date and title, whatever time or older shape its name has (AC-2).
- The hub validator and index generator accept both the new and the older filename shapes and show the time in the indexes (AC-3).
- Policy and skill documentation describe the new shape (AC-4).
- The change is published to Builder `origin/main` (AC-5).

## Non-Goals
| Not doing | Why |
|---|---|
| Renaming existing plans and reports | History and links in memory, plans and PRs point at the current names; AGENTS.md says older records are not backfilled. |
| Making the validator reject new records without a time | Tests and fixtures use older-shape names; the save helpers are the sanctioned writers and enforce the shape. |
| Timestamping session memory files | AGENTS.md keeps exactly one memory file per date; its entries already carry `HH:MM`. |
| Timestamping Implementation Log entry headings | The request covers filenames only. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `save_implementation_plan.py` and `save_test_report.py` write `YYYY-MM-DD-HH-MM-<project>-<slug>.md`, using `--time HH:MM` when given and the current local time otherwise. |
| AC-2 | With `--overwrite`, the helpers replace the single existing record with the same date and slug (timed or older shape); without it they refuse; several matches are refused with their names. |
| AC-3 | `validate_hub_state.py` accepts both shapes and checks the project prefix after the time; `update_hub_indexes.py` lists timed records as `YYYY-MM-DD HH:MM`. |
| AC-4 | AGENTS.md, README.md, write-implementation-plan and write-test-report references name `YYYY-MM-DD-HH-MM-project-title.md`. |
| AC-5 | The change commit is on Builder `origin/main` and the plan Outcome reports each criterion. |

## Inputs
- **Request:** User chat on 2026-10-04: add hours and minutes to plan and report filenames as `YYYY-MM-DD-HH-MM`.
- **Files read:** `.agents/lib/artifact_io.py`, `.agents/lib/builder_hub.py`, both save helpers, `validate_hub_state.py`, `update_hub_indexes.py`, `test_artifact_io.py`, `test_artifact_quality.py`, `test_test_report_workflow.py`, AGENTS.md, README.md, plan.md, update.md, validation.md, write-test-report SKILL.md.
- **Inspected commit:** `79bd314` on Builder `main`.

## Branch
Builder primary checkout, `main` at `79bd314`.

## Assumptions
- No existing record's slug begins with a valid `HH-MM` pair; the inspected names (including `2026-09-23-2026-09-23-...`) do not.
- The local clock is the right source of the time, as it already is for the date.

## Open Questions
None.

## Design
`builder_hub.DATED_FILE_RE` gains an optional time group that only matches a valid `HH-MM` (00-23, 00-59), and `parse_dated_file` returns date, time (or None) and slug. `artifact_io` adds `parse_optional_time` and `dated_markdown_file` takes `artifact_time`; before naming a new file it looks for existing records in the directory with the same date and slug. One match is returned, so `--overwrite` replaces it and a plain save refuses it as before; several matches raise `ValueError` listing them. With no match it returns `date-HH-MM-slug.md`. The helpers add `--time HH:MM`. The validator reads the slug from `parse_dated_file` instead of slicing a fixed-width prefix, and the index generator shows `date HH:MM`. Within a day, timed names sort before older-shape names because digits sort before letters; that is acceptable since older-shape records stop being created.

| Alternative | Why not |
|---|---|
| Always name by the current time, even on overwrite | An overwrite later in the day would create a second file instead of replacing the record, breaking write-test-report's same-date replace rule. |
| Require `--time` | Adds friction to every save; the clock already supplies the date. |
| Rename existing records to a midnight time | Breaks links across memory, plans and PR bodies for no reader benefit. |

## Expected Changes
| File or area | Change |
|---|---|
| `.agents/lib/builder_hub.py` | Optional time group in `DATED_FILE_RE`; `parse_dated_file` returns time too. |
| `.agents/lib/artifact_io.py` | `parse_optional_time`; `dated_markdown_file` and `save_dated_markdown` take `artifact_time` and reuse an existing same-date same-slug record. |
| Save helpers for plans and reports | `--time` option, help text, `ValueError` handling around naming. |
| `validate_hub_state.py`, `update_hub_indexes.py` | Slug from the parser; messages name the new shape; index shows the time. |
| `.agents/tests/` | Timed names, overwrite reuse, ambiguity refusal, index time and validator messages. |
| AGENTS.md, README.md, plan.md, update.md, validation.md, write-test-report SKILL.md | Document `YYYY-MM-DD-HH-MM-project-title.md`. |

## Task Breakdown
### Task 1 - Name new records with the time and keep older names valid
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Published reviewed plan. |
| **Files** | `.agents/lib/builder_hub.py`; `.agents/lib/artifact_io.py`; `.agents/skills/write-implementation-plan/scripts/save_implementation_plan.py`; `.agents/skills/write-test-report/scripts/save_test_report.py`; `.agents/skills/publish-builder-changes/scripts/validate_hub_state.py`; `.agents/skills/publish-builder-changes/scripts/update_hub_indexes.py`; `.agents/tests/test_artifact_io.py`; `.agents/tests/test_artifact_quality.py`; `.agents/tests/test_test_report_workflow.py`. |
| **Symbols** | `DATED_FILE_RE`, `parse_dated_file`, `parse_optional_time`, `dated_markdown_file`, `save_dated_markdown`, both helpers' `parse_args` and `main`, `validate_record_project`, `item_line`. |
| **Inspection** | Read every listed file at `79bd314`; `parse_dated_file` is used only by the validator and index generator; `dated_markdown_file` and `save_dated_markdown` only by the two save helpers and `test_artifact_io.py`. |
| **Behavior** | New saves produce `date-HH-MM-project-slug.md`; overwrite replaces the one same-date same-slug record; older-shape files still validate and index. |
| **Invariants** | Existing records are never renamed; the date default and `--date` behavior are unchanged; a plain save never replaces an existing record. |
| **Boundary/API** | New optional keyword `artifact_time` and CLI `--time`; `parse_dated_file` returns a three-field tuple, with both callers updated. |
| **Effects and failures** | One directory listing per save. A bad `--time` exits 2 with `--time must use HH:MM format`; several matches exit 2 naming them. |
| **Tests and evidence** | Unit and CLI tests for timed names, `--time`, overwrite of a timed and an older-shape record, ambiguity refusal, index time and the validator's project-prefix message. |
| **Verification** | `python -B -m unittest discover -s .agents/tests`; a save into a temporary root showing the timed name; `check_hub.py check`; `git diff --check`. |

### Task 2 - Document the new filename shape
| Contract | Detail |
|---|---|
| **Dependencies** | Task 1, so documentation matches behavior. |
| **Files** | `AGENTS.md`; `README.md`; `.agents/skills/write-implementation-plan/references/plan.md`; `.agents/skills/write-implementation-plan/references/update.md`; `.agents/skills/write-implementation-plan/references/validation.md`; `.agents/skills/write-test-report/SKILL.md`. |
| **Symbols** | AGENTS.md `## Documents`; README document table; plan.md opening and PowerShell Helper; update.md Helper example; validation.md command; write-test-report filename and options paragraph. |
| **Inspection** | Located each `YYYY-MM-DD-...title.md` mention with `git grep` at `79bd314`. |
| **Behavior** | Every description of plan and report filenames names `YYYY-MM-DD-HH-MM-project-title.md` and the `--time` option; memory stays `YYYY-MM-DD.md`. |
| **Invariants** | No other policy text changes. |
| **Boundary/API** | Documentation only. |
| **Effects and failures** | None at runtime. |
| **Tests and evidence** | `check_hub.py check` validates links and skill frontmatter. |
| **Verification** | `git grep -n "YYYY-MM-DD-project-title\|YYYY-MM-DD-title"` finds no plan or report description left; `check_hub.py check`. |

### Task 3 - Record and publish verified delivery
| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 and 2. |
| **Files** | This plan; `docs/session-memory/2026-10-04.md`; generated indexes. |
| **Symbols** | Outcome, Document Status; dated memory entry. |
| **Inspection** | Current plan and memory file. |
| **Behavior** | Plan complete with evidence; memory links the plan. |
| **Invariants** | Earlier memory entries untouched. |
| **Boundary/API** | Documentation only. |
| **Effects and failures** | Commits and pushes to Builder `main`; a failed push leaves the work incomplete. |
| **Tests and evidence** | `check_hub.py refresh` and push readback. |
| **Verification** | `git log origin/main -1` shows the commits. |

## Test Plan
Builder has no runnable application: the change is to command-line helpers, so runtime proof is an actual helper run into a temporary root plus the native unit suite.

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Tests assert `2099-04-05-09-30-builder-...` names for `--time 09:30` and a timed name without `--time`. | Run `save_test_report.py` into a temporary root and read the printed path. |
| AC-2 | Tests overwrite a timed and an older-shape record, refuse without `--overwrite`, and refuse two matches. | Rerun the same save with `--overwrite` and confirm one file remains. |
| AC-3 | Index test expects `2099-04-05 09:30:`; validator test expects the `YYYY-MM-DD-HH-MM-builder-` message; both shapes validate. | `check_hub.py check` on the real hub passes with its older-shape records. |
| AC-4 | `check_hub.py check`. | `git grep` shows no stale plan or report filename description. |
| AC-5 | Push readback. | `git log origin/main` shows the commit. |

Regressions: the full `.agents/tests` suite, including the doubled-date report names and memory filename checks.

## Rollback or Recovery
Revert the change commit; older-shape names keep working under the old code, but any timed records saved meanwhile would then fail validation and need renaming to drop `-HH-MM`.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A future slug that starts with a valid `HH-MM` is misread as a time. | Low | The time group requires valid hour and minute values; titles rarely start with two two-digit numbers. |
| Overwrite picks the wrong record. | Low | It matches only the exact date and slug, and refuses when more than one exists. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
builder

## Plan Format
task-contract-v2
