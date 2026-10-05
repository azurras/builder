# Living Implementation Plans

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Make the implementation plan the living backbone of each change: what we want, what we do not, what we expect to change, how we will prove it, what actually changed along the way and how it ended.

## Goals
- Introduce plan format `task-contract-v2` with required, validated sections for Background, Goals, Non-Goals, numbered Acceptance Criteria, Design, Expected Changes, Test Plan, Implementation Log and Outcome.
- Make the plan the owner of change-specific deviations, discoveries and decisions; dated session memory records the day's work and links to the plan instead of duplicating it.
- Add an update mode and helper that appends dated Implementation Log entries and moves Document Status without rewriting the plan.
- Require new plans saved through the helper to use v2 while every existing v1, legacy and historical plan keeps validating unchanged.
- Close out the earlier rename plan, which was delivered without being marked complete.

## Inputs
- User request in this chat: the plan is the backbone of the work and must be a living document covering goals, non-goals, expected changes, testing and changes made during implementation.
- User decisions in this chat: the plan owns the implementation log with session memory linking to it; new structure is a new validated format and existing plans stay valid.
- Inspected at `33b3965` (clean main): write-implementation-plan SKILL.md, references/plan.md, review.md, validation.md, example.md, agents/openai.yaml, scripts/save_implementation_plan.py and validate_implementation_plan.py; .agents/lib/artifact_quality.py and artifact_io.py; commit-push-builder-main validate_hub_state.py and phase-finalization.md; complete-builder-work and save-session-memory SKILL.md; AGENTS.md; README.md; .agents/tests/test_artifact_quality.py; docs/implementation-plans formats in use (all 2026-10-04 plans are task-contract-v1).

## Branch
Builder primary checkout `main`, inspected at `33b3965`; publish exact task files through the Builder helper.

## Non-Goals
- Migrating existing plans to v2: they are historical records and v1 stays valid.
- Changing test report or session-memory formats or their validators: only their relationship to the plan changes.
- Enforcing semantic quality the validator cannot see (whether a non-goal's reason is sound, whether a design alternative is real): review mode owns that.
- Adding plan statuses or a separate change-request document: the log and existing statuses cover the lifecycle.

## Assumptions
- Agents edit plan sections in place with ordinary file edits; only log entries and status transitions need a helper to stay append-only and consistent.
- Another session may commit to this checkout concurrently; each checkpoint selects only this task's files.

## Open Questions
None. Both design decisions were answered by the user.

## Task Breakdown

### Task 1 - Validate task-contract-v2 plans
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: `.agents/lib/artifact_quality.py`; `.agents/tests/test_artifact_quality.py`
Symbols: `validate_implementation_plan_text`, `PLAN_REQUIRED_SECTIONS`, new `PLAN_V2_REQUIRED_SECTIONS`, supported Plan Format values, new v2 checks for acceptance IDs, test-plan coverage, log entries and outcome.
Inspection: Read the full validator and its tests at `33b3965`; v1 dispatch is keyed on `## Plan Format`, unversioned literal plans return early, and hub validation calls the same function for every non-legacy plan.
Behavior: v2 plans require Plan Format, Document Status, Objective, Background, Goals, Non-Goals, Acceptance Criteria, Inputs, Branch, Assumptions, Open Questions, Design, Expected Changes, Task Breakdown, Test Plan, Rollback or Recovery, Risks, Implementation Log and Outcome, all nonempty. Acceptance Criteria must define sequential `AC-1..n` IDs; every ID must appear in Test Plan. Implementation Log entries use `### YYYY-MM-DD - Title` headings with Change, Reason and Impact labels. A complete v2 plan must mention every AC ID in Outcome and must not leave Outcome pending. Task contracts keep the v1 fields.
Invariants: v1, unversioned literal and legacy plans produce exactly the same errors as today; unknown formats are still rejected.
Boundary/API: `validate_implementation_plan_text(markdown, path)` signature and error-string style unchanged.
Effects and failures: Pure text validation; returns error strings and performs no I/O.
Tests and evidence: New tests for a valid v2 plan, each missing v2 section, missing or non-sequential AC IDs, an AC absent from Test Plan, malformed log entry, complete plan with pending Outcome or a missing AC result; all existing v1 and legacy tests unchanged.
Verification: `python -B -m unittest discover -s .agents/tests`

### Task 2 - Require v2 for new saves and add the plan log helper
Required skill: write-chris-street-style-code
Dependencies: Task 1 validator.
Files: `.agents/skills/write-implementation-plan/scripts/save_implementation_plan.py`; new `.agents/skills/write-implementation-plan/scripts/log_plan_change.py` beside it, following save_implementation_plan.py's argparse, LIB import and exit-code pattern; `.agents/tests/test_artifact_quality.py`
Symbols: save CLI `main`; new log CLI with `--plan`, `--title`, `--date`, optional `--status`, entry body on stdin.
Inspection: Read save helper and `artifact_io.save_dated_markdown` at `33b3965`; save validates then writes, refusing existing files without `--overwrite`.
Behavior: Saving a new plan rejects any format other than task-contract-v2; `--overwrite` of an existing file accepts any currently valid format so in-flight v1 plans can still be replaced. The log helper inserts a dated entry at the end of `## Implementation Log` (creating that section before `## Outcome`, or at the end, when absent), optionally sets Document Status, validates the result and writes only when valid.
Invariants: Bytes outside the inserted entry and the status line are preserved; earlier log entries are never edited; an invalid result leaves the file unchanged.
Boundary/API: Existing save CLI flags unchanged; new CLI follows the save helper's conventions and exit codes (0 written, 1 validation or file error, 2 bad input).
Effects and failures: Writes one plan file; missing plan, blank title or body, unknown status, or validation failure exits nonzero without writing.
Tests and evidence: Save CLI refuses a new v1 plan and accepts v2; overwrite of an existing v1 plan still works; log helper appends in order, preserves other bytes, sets status, creates a missing section, and leaves the file untouched on invalid status.
Verification: `python -B -m unittest discover -s .agents/tests`; run both helpers against a temporary root and inspect the resulting files.

### Task 3 - Rewrite the skill guidance for living plans
Dependencies: Tasks 1-2, so guidance names real sections and commands.
Files: `.agents/skills/write-implementation-plan/SKILL.md`; `references/plan.md`, `review.md`, `validation.md`, `example.md`; new `references/update.md`; `agents/openai.yaml`
Symbols: Mode list (Plan, Update, Review, Validate); v2 section guidance; update rules; review blockers; v2 example.
Inspection: Read every listed file at `33b3965`; SKILL.md currently sends work and decisions to dated memory and has no update mode.
Behavior: Plan mode documents each v2 section and what good content looks like (goals with success measures, non-goals with reasons, observable AC IDs, design with alternatives and decisions, expected changes by area, test plan mapping ACs to native tests and local runtime checks). Update mode says: set in-progress when implementation starts; when work diverges, edit the affected sections to current truth and append a log entry with what changed, why and its impact; corrections are new entries; scope expansions need existing authority; write Outcome against every AC and mark complete at closure. Review mode adds v2 semantic blockers. The example is a complete v2 plan that passes the validator.
Invariants: Mode boundaries, read-only review and validation, and phase-finalizer checkpoints are unchanged; v1 remains documented as historical.
Boundary/API: Skill name and invocation unchanged; metadata prompt mentions update mode.
Effects and failures: Documentation only.
Tests and evidence: Example validates; skill link and frontmatter checks pass through the hub check.
Verification: `python .agents/skills/write-implementation-plan/scripts/validate_implementation_plan.py .agents/skills/write-implementation-plan/references/example.md`; `python .agents/skills/commit-push-builder-main/scripts/check_hub.py check --root .`

### Task 4 - Align policy and caller skills with plan ownership
Dependencies: Task 3 terminology.
Files: `AGENTS.md`; `.agents/skills/complete-builder-work/SKILL.md`; `.agents/skills/save-session-memory/SKILL.md`; `README.md`
Symbols: AGENTS Documents definitions and publication sentence; complete-builder-work steps 2, 3 and 6; save-session-memory recording scope; README skill table role.
Inspection: Read each file at `33b3965`.
Behavior: AGENTS defines implementation plans as the living record of one change (goals, non-goals, acceptance criteria, design, expected changes, test plan, implementation log, outcome) kept current through closure, and session memory as the dated record that links to plans for change-specific decisions. complete-builder-work marks the plan in-progress before implementation, logs deviations as they happen, and writes Outcome and complete status before closure. save-session-memory links the plan instead of copying change decisions.
Invariants: Agent-neutral policy stays in AGENTS.md; publication, trust and Git rules unchanged.
Boundary/API: No skill renamed or removed.
Effects and failures: Documentation only.
Tests and evidence: Hub check; reread the edited paragraphs for consistency with Task 3.
Verification: `python .agents/skills/commit-push-builder-main/scripts/check_hub.py check --root .`; `git diff --check`

### Task 5 - Close the rename plan and publish verified delivery
Dependencies: Tasks 1-4 checks pass and the diff is reviewed.
Files: `docs/implementation-plans/2026-10-04-rename-planning-skill-to-write-implementation-plan.md`; this plan; `docs/session-memory/2026-10-04-builder.md`; generated indexes.
Symbols: Document Status; Implementation Log and Outcome sections; appended memory entry.
Inspection: Read the rename plan at `33b3965`: status is ready-for-execution although delivered in `726787e`, and its Files list named four dated plans that were intentionally left unchanged as history.
Behavior: Rename plan becomes complete with a log entry recording the deviation and its reason; this plan records its own deviations and Outcome and becomes complete; memory gets a short entry linking this plan.
Invariants: Exact selected files only; earlier memory entries untouched.
Boundary/API: Existing Builder publication helper and document layout.
Effects and failures: Scoped commit and push; a failed push stays incomplete and is retried with push-only.
Tests and evidence: Full suite, hub refresh, reviewed diff, remote readback.
Verification: `check_hub.py refresh --root .`; helper dry-run then publication; `git ls-remote origin refs/heads/main` matches the commit.

## Code Changes
Tasks 1-2 change the shared plan validator, the save helper and add a log helper. Tasks 3-5 are Markdown guidance, policy and records.

## Files and Modules
Write-implementation-plan skill (entrypoint, references, metadata, scripts), `.agents/lib/artifact_quality.py`, `.agents/tests/test_artifact_quality.py`, AGENTS.md, README.md, complete-builder-work and save-session-memory entrypoints, the rename plan, this plan, dated memory and indexes.

## Unit Testing
Extend `test_artifact_quality.py` as listed in Tasks 1-2 and run the full native suite with `python -B -m unittest discover -s .agents/tests`.

## Local Testing
Application runtime verification does not apply: Builder holds workflow instructions and standalone Python helpers with no runnable application. Instead, actually run the save, log and validate helpers against a temporary root and the real repository, and run the hub check over every existing plan.

## Validation
Every existing plan in docs/implementation-plans still validates (hub check reports no new errors); the v2 example validates; a v1 plan saved as new is refused; full diff and whitespace review.

## Rollback or Recovery
Revert this change's commits; v1 plans never depended on v2 code, so reverting restores prior behavior. Any v2 plan saved in between would then fail validation as an unknown format, so check for v2 plans before reverting and convert them back if any exist. Recover a failed publication with push-only.

## Risks
- Over-structuring makes small plans heavy: keep sections short, allow "None" with a reason, and keep the example compact.
- A validator regression breaks existing plans: the hub check over all current plans and the unchanged v1 tests guard against it.
- Concurrent sessions in this checkout: select only this task's files and re-check status before each commit.

## Completion Criteria
- v2 format validated with the listed checks; new saves require v2; log helper works as specified; all existing plans still validate.
- Skill guidance, example, policy and caller skills describe the living-plan workflow consistently.
- Rename plan closed; this plan's log and outcome filled in; full suite and hub check pass; changes published to origin main with readback.

## Implementation Log
No entries yet.

## Outcome
Pending.
