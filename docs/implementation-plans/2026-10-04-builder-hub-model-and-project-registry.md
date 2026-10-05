# Builder Hub Model and Project Registry

## Plan Format
task-contract-v2

## Document Status
complete

## Project
builder

## Objective
An agent opening Builder can tell what the hub is for, which project every plan, test report and memory file belongs to, which project slugs are valid, and which tools are archival.

## Background
On 2026-10-04 the user asked what in Builder would confuse an agent about the hub-and-spoke goal. The review found eight gaps; the user asked to fix four of them:

- Gap 2: AGENTS.md and README describe how to find spokes but never say why the hub exists, what belongs in Builder versus a spoke, or that Builder is itself a project.
- Gap 3: plans and test reports do not record their spoke. The plan template has `Branch` but no project field, filenames are inconsistent (`2026-07-09-issue-1090-â€¦` has no slug), and the indexes are flat date lists.
- Gap 4: session memory uses the slugs `builder`, `christopherbell-dev`, `personal-computer-cleanup` and `software-handoff-kit`, but only one is a registered spoke. AGENTS.md lists three "current slugs" and omits the fourth, and no helper rejects an unknown slug.
- Gap 6: `consolidate_project_memory.py`, `memory_migration.py` and `migration-audit.md` exist only to audit the completed July consolidation, but they sit beside the daily tools without saying so.

User decisions: work that is not tied to a repository stays allowed and is registered (personal-computer-cleanup active, software-handoff-kit retired); existing plans and reports are not backfilled.

## Goals
- Agents read a stated purpose and a hub-versus-spoke responsibility table before any mechanics (AC-1).
- Every new plan and test report names its project in a `## Project` section and in its filename, and the indexes group records by project (AC-2, AC-3).
- One registry, spokes.json, defines every valid project slug, and every helper that writes a record refuses unknown or retired slugs (AC-4, AC-5).
- The migration tooling is marked archival where agents meet it (AC-6).

## Non-Goals
- Gap 1, a back-pointer in christopherbell.dev: a spoke change the user did not select.
- Gap 5, showing plan status in the index (`extract_status` does not read `## Document Status`): not selected; noted as a follow-up.
- Backfilling `## Project` into existing plans and reports: the user chose to leave history as is.
- Moving or deleting the migration tooling: a test added earlier today (`test_real_repository_passes_migration_audit`) runs it, and another session just changed it.
- Renaming spokes.json: it stays the single registry; renaming would churn every helper and document for no gain.
- A register mode for non-repository projects: they are rare; a hand edit is validated by the hub check.

## Acceptance Criteria
- AC-1: AGENTS.md opens its hub section with the purpose, a table of what Builder and spokes each hold, and the statement that Builder is itself the `builder` project; README carries the same model in brief.
- AC-2: `save_implementation_plan.py` and `save_test_report.py` refuse a new document without a `## Project` section naming an active project, and save it as `YYYY-MM-DD-<project>-<title>.md` without doubling a prefix the title already has. Overwriting an existing document without the section still works.
- AC-3: `check_hub.py refresh` groups each index by project, with plans and reports that predate the field listed last under their own heading.
- AC-4: spokes.json holds a `projects` list for non-repository work (personal-computer-cleanup active, software-handoff-kit retired). `builder`, registered spokes and listed projects are the only valid slugs; duplicates across those, or a spoke named `builder`, are rejected, and `register` refuses a slug already used by a project.
- AC-5: `save_session_memory.py`, the spoke helper's snapshot mode, the hub check and the spoke PR preflight enforce the registry: new memory needs an active project; the hub check rejects unknown slugs in memory filenames and Project sections, a Project section that disagrees with its filename and an invalid registry; preflight refuses a report whose Project is not the spoke.
- AC-6: both migration modules start with an archival notice naming migration-audit.md, and AGENTS.md and save-session-memory say the tooling is archival and not for daily memory.
- AC-7: the full test suite and the hub check pass on Builder `origin/main` with the change pushed.

## Inputs
- Request: the user's 2026-10-04 review question and "Let's fix 2, 3, 4, and 6", with the two decisions above.
- Builder `main` at `567912a`. Read AGENTS.md, README.md, spokes.json, every SKILL.md, `.agents/lib/{spoke_registry,artifact_quality,artifact_io,project_memory,builder_hub,memory_migration}.py`, `save_implementation_plan.py`, `save_test_report.py`, `save_session_memory.py`, `consolidate_project_memory.py`, `update_hub_indexes.py`, `validate_hub_state.py`, `check_hub.py`, `manage_spoke_repositories.py`, `preflight_spoke_pr.py`, the plan and report references and examples, and the tests that cover them.

## Branch
Primary Builder checkout on `main`, from `567912a`; published with publish-builder-changes.

## Assumptions
- No other session is editing the files in Expected Changes; recheck `git status` before editing and before publishing.
- The four memory slugs above are the only ones in use (verified with `ls docs/session-memory`).

## Open Questions
None. The user settled both policy questions.

## Design
**Registry.** spokes.json gains an optional `projects` list of `{slug, name, status, description}` with status `active` or `retired`. `spoke_registry.py` adds `HUB_PROJECT_SLUG = "builder"`, a `ProjectStatus` enum, a frozen `StandaloneProject`, `project_statuses_of(builder_root)` (every valid slug with its status, failing on duplicates or a reserved slug) and `require_active_project(builder_root, slug)`. `builder` is a constant rather than an entry because the hub is not something to register. Alternatives rejected: a separate projects.json, which would break "spokes.json is the only registry"; renaming the file to projects.json, which is churn.

**Project section.** Plans and reports gain `## Project` holding one slug. `artifact_quality.project_of` reads it and the text validators check its shape; registry membership needs the Builder root, so the save helpers, hub check and preflight check it. The section stays optional in the validators so the existing v2 plans and reports remain valid. The save helpers require it for new files, the same way they already require the current plan format for new files. Alternative rejected: a new plan format, which would leave reports uncovered and force every in-flight plan to migrate.

**Filenames.** The helper prefixes the filename with the project unless the title's slug already starts with it. The hub check requires a document that has a Project section to carry that prefix, so its name and section cannot drift. Because of that rule, adding the section to an old unprefixed document fails the check, which keeps history as the user chose.

**Indexes.** Plans and reports are grouped by their Project section, memory by its filename slug, in slug order, with plans and reports that have no section in a final "Before the Project field" group.

**Memory and snapshot.** `append_entry` calls `require_active_project`, so every memory write is guarded in one place. Snapshot mode also calls it before inspecting, so it fails before doing any work.

**Archival marking.** A notice in module docstrings and two documentation lines rather than a move, for the reason in Non-Goals.

## Expected Changes
- `spokes.json`: `projects` list with the two non-repository projects.
- `.agents/lib/spoke_registry.py`: project registry types and functions; `load_spokes` rejects the `builder` slug; `register_spoke` refuses project slugs.
- `.agents/lib/artifact_quality.py`: `project_of` and Project shape validation for plans and reports.
- `.agents/lib/artifact_io.py`: `project_prefixed_title`.
- `.agents/lib/project_memory.py`: `append_entry` requires an active project.
- `.agents/skills/write-implementation-plan/scripts/save_implementation_plan.py`, `.agents/skills/write-test-report/scripts/save_test_report.py`: require Project for new documents and prefix filenames.
- `.agents/skills/publish-builder-changes/scripts/update_hub_indexes.py`: grouped indexes.
- `.agents/skills/publish-builder-changes/scripts/validate_hub_state.py`: registry, slug and prefix checks.
- `.agents/skills/deliver-change/scripts/manage_spoke_repositories.py`: snapshot checks the project first.
- `.agents/skills/publish-spoke-changes/scripts/preflight_spoke_pr.py`: report project check.
- `.agents/lib/memory_migration.py`, `.agents/skills/save-session-memory/scripts/consolidate_project_memory.py`: archival notice.
- `AGENTS.md`, `README.md`: model section, slug policy, document names, archival note.
- Skill documents: write-implementation-plan `references/plan.md` and `references/example.md`; write-test-report `SKILL.md`, `references/report.md`, `references/template.md` and `references/example.md`; save-session-memory `SKILL.md`; deliver-change `references/repository-inspection.md`.
- Tests: `test_spoke_registry.py`, `test_artifact_quality.py`, `test_test_report_workflow.py`, `test_project_memory.py`, `test_skill_consolidation.py`, `test_publish_spoke_changes.py`.
- `docs/implementation-plans/index.md`, `docs/test-reports/index.md`, `docs/session-memory/index.md`: regenerated.

## Task Breakdown

### Task 1 - Register every project in spokes.json
Required skill: write-chris-street-style-code
- Dependencies: None.
- Files: `spokes.json`, `.agents/lib/spoke_registry.py`, `.agents/tests/test_spoke_registry.py`.
- Symbols: `HUB_PROJECT_SLUG`, `ProjectStatus`, `StandaloneProject`, `load_standalone_projects`, `project_statuses_of`, `require_active_project`, `load_spokes`, `register_spoke`.
- Inspection: read `spoke_registry.py` and its tests at `567912a`; `_read_registry_document` already validates the top-level shape.
- Behavior: valid slugs are `builder`, spokes and listed projects; retired projects are known but not active.
- Invariants: spokes.json holds no machine paths; a slug names exactly one thing; the file is unchanged when registration fails.
- Boundary/API: existing spoke functions keep their signatures; `projects` is optional so older registries still load.
- Effects and failures: reads spokes.json only, except `register_spoke`; malformed entries raise `ValueError` naming the index and field.
- Tests and evidence: new unit tests for project loading, duplicates across kinds, the reserved slug, retired refusal and register conflict; the real-registry test asserts the two projects.
- Verification: `python -m unittest discover -s .agents/tests -p test_spoke_registry.py`.

### Task 2 - Record the project in plans, reports and memory
Required skill: write-chris-street-style-code
- Dependencies: Task 1, for `require_active_project`.
- Files: `.agents/lib/artifact_quality.py`, `.agents/lib/artifact_io.py`, `.agents/lib/project_memory.py`, `save_implementation_plan.py`, `save_test_report.py`, `update_hub_indexes.py`, `validate_hub_state.py`, `manage_spoke_repositories.py`, `preflight_spoke_pr.py` and their tests.
- Symbols: `project_of`, `PROJECT_SECTION`, `project_prefixed_title`, `append_entry`, the two save helpers' `main`, `build_index`, `validate_hub_state.main`, snapshot handling in `manage_spoke_repositories.main`, `check_report`.
- Inspection: read each file at `567912a`; the save helpers compute the path with `dated_markdown_file` before saving, and the index builder lists files from `list_markdown`.
- Behavior: AC-2, AC-3 and AC-5 as written.
- Invariants: existing documents without the section stay valid and unchanged; memory files stay append-only; indexes stay deterministic.
- Boundary/API: CLI flags are unchanged; the only new requirement is the section in new documents and a registered project.
- Effects and failures: helpers exit nonzero without writing when the project is missing, unknown or retired; the hub check reports every violation rather than stopping at the first.
- Tests and evidence: tests that fail before the change for each refusal, prefix rule, grouping and preflight mismatch; fixtures write a spokes.json.
- Verification: `python -m unittest discover -s .agents/tests` and `python .agents/skills/publish-builder-changes/scripts/check_hub.py check --root .`.

### Task 3 - State the hub model and project policy
- Dependencies: Tasks 1 and 2, so the documents describe the behavior that exists.
- Files: `AGENTS.md`, `README.md`, the skill documents listed in Expected Changes.
- Symbols: AGENTS.md headings `Hub and Spokes` and `Documents`; README `Builder` introduction and `Documents`; plan.md `Sections`; report.md `Report Content`.
- Inspection: read each file at `567912a`.
- Behavior: AC-1, and the policy text for AC-4 and AC-6.
- Invariants: AGENTS.md stays agent-neutral; the trust wording that `test_github_trust_boundary.py` checks is kept.
- Boundary/API: documentation only.
- Effects and failures: none at runtime.
- Tests and evidence: link and discovery tests, plus the hub check; reading the result as a new agent would.
- Verification: `python -m unittest discover -s .agents/tests -p test_skill_consolidation.py` and the hub check.

### Task 4 - Mark the migration tooling archival
Required skill: write-chris-street-style-code
- Dependencies: None.
- Files: `.agents/lib/memory_migration.py`, `.agents/skills/save-session-memory/scripts/consolidate_project_memory.py`, `.agents/skills/save-session-memory/SKILL.md`.
- Symbols: module docstrings; the SKILL.md migration-audit sentence.
- Inspection: read both modules and migration-audit.md at `567912a`.
- Behavior: AC-6.
- Invariants: the audit's behavior and output are unchanged.
- Boundary/API: docstrings only.
- Effects and failures: none.
- Tests and evidence: `test_real_repository_passes_migration_audit` still passes.
- Verification: `python -m unittest discover -s .agents/tests -p test_project_memory.py`.

## Test Plan
Builder has no runnable application: these are command-line helpers and documents, so verify-local-app's application run does not apply, and the native checks below are the evidence.
- AC-1: read AGENTS.md and README after the edit; the hub check's link validation passes.
- AC-2: new tests in `test_artifact_quality.py` and `test_test_report_workflow.py` show a refusal without the section, refusal for an unknown or retired project, the prefixed filename, no doubled prefix, and an overwrite of an existing unprefixed document.
- AC-3: an index test with one labeled and one unlabeled document checks the group headings and order; `check_hub.py refresh` on the real repository yields grouped indexes.
- AC-4: `test_spoke_registry.py` cases for the registry rules; the real-registry test asserts both projects and their statuses.
- AC-5: memory tests refuse unregistered and retired projects; a snapshot test refuses an unregistered project before writing; hub-state tests reject an unknown memory slug, an unknown Project and a filename that disagrees with its Project; a preflight test refuses a report naming another project.
- AC-6: read the docstrings and documents; the real-repository migration audit test passes.
- AC-7: the full suite and `check_hub.py check --root .` pass before publishing, and `git log origin/main` shows the commit after the push.

## Rollback or Recovery
Revert the commit on `main` with a new commit. Documents saved under the new rule keep their Project sections and stay valid under the old validators, which ignore unknown sections.

## Risks
- A concurrent session saves a document while this change lands, and it lacks a Project section: medium likelihood. It stays valid because the section is optional for existing files; only new saves need it.
- Fixtures across six test files need a registry: some test may be missed. Mitigation: run the full suite.

## Implementation Log

### 2026-10-04 - Shared registry fixture for tests

- Change: Added `.agents/tests/project_registry_fixture.py`, which writes a spokes.json with sample projects; five test files use it.
- Reason: Every helper that writes a record now reads the registry, so each temporary Builder root needs one; one helper keeps the fixtures identical.
- Impact: One new test-support file beyond Expected Changes; no production effect.

### 2026-10-04 - Hub check requires the registry

- Change: The hub check now reports a missing or invalid spokes.json as an error, so `check_hub.py refresh` on an empty folder fails until a registry exists. `test_check_read_only_and_refresh_only_three_folders` now asserts that failure, then writes a registry.
- Reason: AC-5 makes the registry the source of valid slugs; without it the check cannot validate memory or Project sections.
- Impact: Only temporary roots without a registry are affected; Builder always has spokes.json.

### 2026-10-04 - Memory slug guidance tightened

- Change: save-session-memory's `--project` guidance no longer says to invent a new slug; work with no repository first gets an active entry under `projects`.
- Reason: The old sentence contradicted AC-4 once the helper refuses unregistered slugs.
- Impact: Documentation only; within Task 3's files.

## Outcome
Delivered in `4da4e7b` on Builder `origin/main` (plan `88fae91`). No source issue, so external closure does not apply.

- AC-1: Met. AGENTS.md's Hub and Spokes section opens with the purpose, a hub-versus-spoke table and the `builder` project; README has a new The Model section.
- AC-2: Met. `test_save_cli_names_the_project_in_new_plans`, `test_save_cli_requires_current_format_for_new_plans`, `test_saves_test_report_with_project_prefixed_dated_slug` and `test_new_report_must_name_an_active_project` cover refusal, prefixing, no doubled prefix and historical overwrite.
- AC-3: Met. `test_indexes_group_reports_by_project_and_validate_them` checks group order; the real indexes now open with `## builder` and end with `## Before the Project field`, and memory is grouped by its four slugs.
- AC-4: Met. spokes.json lists personal-computer-cleanup (active) and software-handoff-kit (retired); `test_project_slugs_are_the_hub_spokes_and_standalone_projects`, `test_rejects_invalid_projects` and `test_register_refuses_a_standalone_project_slug_and_keeps_projects` pass, and the real-registry test asserts both statuses.
- AC-5: Met. Memory, snapshot, hub-check and preflight tests cover each refusal. Live runs: saving memory for software-handoff-kit and snapshotting with project `nope` both exited 2 with the expected message and wrote nothing.
- AC-6: Met. Both modules carry an archival notice; AGENTS.md and save-session-memory say the tooling is archival. `test_real_repository_passes_migration_audit` still passes.
- AC-7: Met. 105 tests pass and `check_hub.py check --root .` passes at `4da4e7b`.

Shipped as planned, plus the three logged deviations. Follow-ups: gap 5 (the index status suffix never appears because `extract_status` does not read `## Document Status`); gap 1 (christopherbell.dev does not point back to Builder); the paused plan `2026-10-04-make-plans-and-test-reports-pleasant-to-read.md` changes the same templates and needs to keep the Project section when it resumes.
