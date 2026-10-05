# Keep One Session Memory File per Day

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every session-memory event for a date, whatever its project, is appended to one file named `docs/session-memory/YYYY-MM-DD.md`, and the existing per-project files are merged into those dated files.

## Background
The user reported on 2026-10-04 that save-session-memory "appears to be behaving not as intended": the intent was one file per day holding every event, appended to for later edits, not divided by project, and named only by the date. The skill, `project_memory.py`, the hub check, the index generator and AGENTS.md instead write and enforce `YYYY-MM-DD-project.md`, so 2026-10-04 already has two files and 2026-07-09 has three. The user chose to merge the existing 45 files into dated files rather than leave them.

## Goals
- New entries for any project land in the single file for their date, tagged with their project (AC-1, AC-2).
- The hub check and generated index treat `YYYY-MM-DD.md` as the only memory filename (AC-3, AC-4).
- Existing memory is merged into dated files without losing a byte of entry content, and every link still resolves (AC-5, AC-6).
- The archival migration audit still proves the imported July 2026 sections are intact (AC-7).
- Policy and skill text describe the new model (AC-8), delivered on Builder main (AC-9).

## Non-Goals

| Not doing | Why |
|---|---|
| Re-sorting old entries from different projects into one timeline | Old imported sections have no per-entry times; keeping each former file as one verbatim block preserves history and the audit |
| Changing how plans and test reports are named or grouped | The request is about session memory only |
| Locking for concurrent writers | Same append-without-lock model as today; the skill's concurrent-writer rule still applies |
| Rerunning the archival consolidation `--apply` | Forbidden by the migration audit reference |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `save_session_memory.py --project <slug>` appends to `docs/session-memory/YYYY-MM-DD.md`; two projects on one date share that file and a later date gets a new file, proven by `test_project_memory.py` |
| AC-2 | Each new entry carries a `**Project:** <slug>` line under its heading, and unknown or retired slugs are still refused |
| AC-3 | `check_hub.py check` rejects a memory file named other than `YYYY-MM-DD.md` and a `**Project:**` line naming an unregistered slug |
| AC-4 | `docs/session-memory/index.md` lists one line per date, not grouped by project |
| AC-5 | No `YYYY-MM-DD-project.md` file remains; each date file holds every former file of that date as a verbatim block under a heading naming its project, proven by a merge readback that finds every former body in its new file |
| AC-6 | Every link in the repository that pointed at a former memory file points at its dated file, and `check_hub.py check` reports no broken links |
| AC-7 | `consolidate_project_memory.py --root . --source-commit 78f0183 --verify` passes against the merged files and still fails on an unrecorded edit |
| AC-8 | AGENTS.md, README.md, save-session-memory SKILL.md and openai.yaml describe one file per date with project-tagged entries |
| AC-9 | The plan, change and dated memory are on Builder origin/main, confirmed by `git ls-remote` |

## Inputs
- **Request:** user in chat on 2026-10-04, quoted in Background; decision "Merge into dated files" chosen through a question.
- **Inspected:** Builder `main` at `2c92cac`: `.agents/lib/project_memory.py` (`project_path`, `append_entry`), `save_session_memory.py`, `manage_spoke_repositories.py` snapshot mode, `validate_hub_state.py` memory rule, `update_hub_indexes.py` (`project_group_of`, `build_index`), `consolidate_project_memory.py` (`prepare`, `verify_sections`, `apply_later_link_retargets`, `main`), `test_project_memory.py`, the memory references in `test_skill_consolidation.py`, `test_spoke_registry.py`, `test_artifact_quality.py`, `test_test_report_workflow.py`, `test_publish_spoke_changes.py`, the skill text, AGENTS.md and README.md, and `git grep` of 62 links into dated memory files outside `docs/session-memory` plus 68 inside it.

## Branch
Builder primary checkout `main` at `2c92cac`; publish the exact task files through publish-builder-changes.

## Assumptions
- Link checks compare paths only, not anchors, so `#source-...` anchors keep working once the target file is renamed (they are unique per source).
- Another session is active on Builder; the merge runs only on a tree where no other session has unpublished memory edits.

## Open Questions
None.

## Design
**Writing.** `project_memory.memory_path(root, date)` returns `docs/session-memory/YYYY-MM-DD.md`. `append_entry` keeps its signature, still requires an active project, writes the header `# YYYY-MM-DD Session Memory` on the first write of a date, and writes each entry as `## YYYY-MM-DD HH:MM zone - Title`, a blank line, `**Project:** slug`, a blank line and the body. `project_entries(text, project)` returns the entries tagged with a project, so the spoke snapshot's duplicate check looks only at that project's last snapshot.

**Checking and indexing.** The hub check requires memory filenames to be `YYYY-MM-DD.md` with a real date and every `**Project:**` line to name a registered slug (retired allowed, for history). The index lists memory files by date with no project grouping.

**Merging.** A one-off script in the session scratchpad, recorded in the Implementation Log, builds each `YYYY-MM-DD.md` from the date's former files in project order: the new header, then for each former file a `## Merged record - slug` heading, a `**Project:** slug` line and the former body after its H1, unchanged. It then rewrites every Markdown link whose target resolves to a former memory file to the dated file, keeping the anchor, with the shared `merged_memory_link` rule. It deletes the former files only after reading back that every former body is present in its new file.

**Audit.** `--verify` reads each migrated session from its dated file and applies the same `merged_memory_link` rewrite to the expected sections, as a recorded later rename, so any other edit still fails.

| Alternative | Why not |
|---|---|
| Interleave old entries chronologically | Imported sections lack per-entry times and would break the audit's verbatim check |
| Leave the old files and accept both names | The user chose to merge |
| Keep the project only in the heading text | A separate `**Project:**` line is unambiguous to parse when titles contain " - " |

## Expected Changes

| File or area | Change |
|---|---|
| `.agents/lib/project_memory.py` | Dated path, project-tagged entries, `project_entries`, `merged_memory_link` |
| `.agents/skills/save-session-memory/scripts/save_session_memory.py` | Help text only |
| `.agents/skills/deliver-change/scripts/manage_spoke_repositories.py` | Snapshot path and per-project duplicate check |
| `.agents/skills/publish-builder-changes/scripts/validate_hub_state.py` | Dated memory filename rule and Project-line check |
| `.agents/skills/publish-builder-changes/scripts/update_hub_indexes.py` | Memory index by date |
| `.agents/skills/save-session-memory/scripts/consolidate_project_memory.py` | Audit reads dated files and applies the merged-link rename |
| `.agents/tests/*` memory tests | Expect dated files and Project lines |
| AGENTS.md, README.md, save-session-memory SKILL.md, openai.yaml, migration-audit.md | New model |
| `docs/session-memory/*` | 45 files merged into dated files; index regenerated |
| `docs/implementation-plans/*`, `docs/test-reports/*` | Links to former memory files retargeted |

## Task Breakdown

### Task 1 - Write and check dated memory

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `.agents/lib/project_memory.py`; `save_session_memory.py`; `manage_spoke_repositories.py`; `validate_hub_state.py`; `update_hub_indexes.py`; memory tests |
| **Symbols** | `project_path` (becomes `memory_path`), `append_entry`, `project_entries`, `merged_memory_link`, snapshot branch of `main`, memory branch of `validate_hub_state.main`, `project_group_of`, `build_index` |
| **Inspection** | Read each listed symbol and test at `2c92cac` |
| **Behavior** | One file per date; entries tagged with project; index by date |
| **Invariants** | Append-only bytes; unknown and retired projects refused; invalid input writes nothing |
| **Boundary/API** | CLI flags of `save_session_memory.py` unchanged; `append_entry` signature unchanged |
| **Effects and failures** | Appends to one file; `ValueError` exits 2 as now |
| **Tests and evidence** | Update `test_project_memory.py` first so it fails against the old naming, then passes; rest of suite passes |
| **Verification** | `python -m unittest discover -s .agents/tests` |

### Task 2 - Merge existing memory and retarget links

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1, for `merged_memory_link` and the new header |
| **Files** | `docs/session-memory/*.md`; linking files under `docs/` |
| **Symbols** | Scratchpad merge script |
| **Inspection** | Listed all 45 memory files and the dates with several files; grepped links |
| **Behavior** | Each date has one file containing every former body verbatim |
| **Invariants** | No entry content lost; no link broken |
| **Boundary/API** | File names change; anchors kept |
| **Effects and failures** | Writes new files, then deletes old ones only after readback |
| **Tests and evidence** | Readback in the script; hub check |
| **Verification** | `check_hub.py refresh --root .`; `git grep` for former names returns nothing |

### Task 3 - Keep the archival audit honest

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 2 |
| **Files** | `consolidate_project_memory.py`; `migration-audit.md`; `test_project_memory.py` |
| **Symbols** | `main` verify branch, `verify_sections` |
| **Inspection** | Read the audit and its tests at `2c92cac` |
| **Behavior** | Audit passes on merged files and still fails on other edits |
| **Invariants** | `--apply` behavior unchanged |
| **Boundary/API** | CLI unchanged |
| **Effects and failures** | Read-only |
| **Tests and evidence** | `test_real_repository_passes_migration_audit`, fixture test |
| **Verification** | The `--verify` command in AC-7 |

### Task 4 - Update policy and skill text

| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 to 3 |
| **Files** | AGENTS.md; README.md; save-session-memory SKILL.md, agents/openai.yaml, references/migration-audit.md |
| **Symbols** | AGENTS.md Documents section; SKILL.md helper section |
| **Inspection** | Read each file at `2c92cac` |
| **Behavior** | Text describes one file per date with project-tagged entries |
| **Invariants** | Other policy unchanged |
| **Boundary/API** | Skill name unchanged |
| **Effects and failures** | Documentation only |
| **Tests and evidence** | Skill and doc tests in the suite |
| **Verification** | `git grep "YYYY-MM-DD-project"` finds no current-policy use |

## Test Plan
Builder has no runnable application: these are command-line helpers and documents, so the native test suite, the hub check and real helper runs are the runtime evidence.

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | `test_project_memory.py` same-day and cross-project test | Save this change's memory entry with the helper and read the file |
| AC-2 | Same test asserts the Project line and refusals | Read the saved entry |
| AC-3 | `test_skill_consolidation.py` hub-check cases | `check_hub.py check --root .` |
| AC-4 | `test_skill_consolidation.py` index case | Read `docs/session-memory/index.md` |
| AC-5 | Merge script readback | `ls docs/session-memory` |
| AC-6 | Hub check link validation | `git grep` for former memory names |
| AC-7 | `test_real_repository_passes_migration_audit` and fixture test | The `--verify` command |
| AC-8 | Skill consistency tests | Read the diff |
| AC-9 | None | `git ls-remote origin main` |

- Regression: the full suite `python -m unittest discover -s .agents/tests` passes.

## Rollback or Recovery
Revert the change commit: the former files and links come back exactly from Git. If the merge runs but readback fails, the script leaves the former files in place; delete only the new dated files it wrote.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Another session writes old-style memory during or after the merge | Medium | Check `git status` and origin before merging; the hub check rejects stray old names so they get noticed |
| A link rewrite touches a non-memory link | Low | Rewrite only links whose resolved target is a former memory file |
| The audit change accepts unintended edits | Low | The rewrite applies only the merged-link rule; the fixture test still requires failure |

## Implementation Log

### 2026-10-04 - Tag recent entries individually and index projects per date

- **Change:** Former files without imported sections whose content starts with a dated entry had a `**Project:**` line added under each dated `## ` heading instead of one `## Merged record - slug` heading; files with imported sections or other leading text use the merged-record heading. The memory index line for each date also names the projects the date holds. The library function is `memory_day_path`, not `memory_path`, and `append_entry` now separates entries with one blank line instead of two.
- **Reason:** Per-entry tags let `project_entries` and the snapshot duplicate check see recent entries by project. Imported sections must stay verbatim for the audit. Naming the projects in the index replaces the old per-project grouping for finding one project's history.
- **Impact:** Design and Task 2 behavior refined; acceptance criteria unchanged. The merge script `merge_memory_days.py` ran from the session scratchpad: 44 former files into 37 dated files, 24 other documents retargeted, readback before deletion.

### 2026-10-04 - Leave plain-text file names in historical plans

- **Change:** 17 earlier plans still name former memory files such as `docs/session-memory/2026-10-04-builder.md` in plain text, not as links; they were left unchanged.
- **Reason:** They record which files that change touched at the time; only links must resolve, and the hub check confirms none is broken.
- **Impact:** AC-6 covers links only, as written.

## Outcome

> [!TIP]
> Session memory is one file per date for every project. All acceptance criteria are met, and existing memory is merged into dated files. This shipped as planned, with the refinements recorded in the Implementation Log.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | `test_every_project_on_a_date_appends_to_that_date_file`; the helper appended this change's entry to [2026-10-04.md](../session-memory/2026-10-04.md) |
| AC-2 | ✅ Met | Same test asserts the exact Project line; `test_invalid_or_missing_project_and_empty_body_do_not_write` still refuses unknown and retired slugs |
| AC-3 | ✅ Met | `test_check_read_only_and_refresh_only_three_folders` rejects `2099-01-03-sample.md` and a `stranger` Project line |
| AC-4 | ✅ Met | [Session memory index](../session-memory/index.md) lists one line per date with its projects |
| AC-5 | ✅ Met | Merge readback passed for 44 former files into 37 dated files; no `YYYY-MM-DD-project.md` file remains |
| AC-6 | ✅ Met | `check_hub.py check` passes with no broken links; 24 documents retargeted |
| AC-7 | ✅ Met | `--verify` prints "Every imported source body matches"; the fixture test still fails on "Rewritten history." |
| AC-8 | ✅ Met | AGENTS.md, README.md, SKILL.md, openai.yaml and migration-audit.md updated in `b03ddd9` |
| AC-9 | ✅ Met | Change commit `b03ddd9` pushed to origin/main; this plan and memory are published in the following commit |

Full suite: 115 tests pass. Follow-up: none.

## Project
builder

## Plan Format
task-contract-v2
