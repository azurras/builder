# Plan-first Builder Workflow

## Plan Format
task-contract-v1

## Document Status
complete

## Objective
Make a reviewed implementation plan the default delivery entry point and remove unused artifact folders without deleting project history.

## Goals
Include requirements, acceptance criteria, and design decisions directly in the plan. Keep separate specs optional for substantial requirements exploration, multiple implementation plans, or explicit user requests. Remove the empty decisions folder and prevent optional artifact folders from being recreated by routine maintenance.

## Inputs
The user approved replacing the mandatory spec phase and requested unnecessary document-folder cleanup. Inspected all current docs directories: decisions has no records; all other artifact folders contain useful history.

## Branch
Builder main at fbd2808; selected-file publication.

## Non-Goals
No historical spec/report/review deletion, no Superpowers edits, no spoke or production changes, no removal of optional spec/decision capabilities.

## Assumptions
Existing plan structure remains compatible. Optional specs may be saved with the plan checkpoint; explicitly requested spec-only work still publishes its artifact.

## Open Questions
None.

## Task Breakdown

### Task 1 - Update planning policy and optional folder maintenance
Dependencies: None.
Files: AGENTS.md, README.md, .agents/skills/complete-builder-work, .agents/skills/plan-builder-work, .agents/skills/maintain-builder-hub, .agents/skills/commit-push-builder-main, .agents/tests/test_artifact_commit_checkpoints.py, .agents/tests/test_skill_consolidation.py, .agents/lib/builder_hub.py, docs/decisions/index.md.
Symbols: Delivery and checkpoint instructions, planning mode and review contract, INDEX_TARGETS iteration, optional index requirements, maintenance fixture tests.
Inspection: Read current delivery/plan/finalizer rules, generator main/build_index, validator ARTIFACT_DIRS/INDEX_FILES and main, existing tests, and folder record counts on clean main fbd2808.
Required skill: write-jane-street-style-code before code changes.
Behavior: Normal delivery begins with a self-contained implementation plan; optional specs do not add a mandatory phase. Empty optional specs/decisions folders are not generated or required. Optional records gain indexes when saved.
Invariants: Reviewed plan publication still precedes implementation; verification, publication, continuity and closure readback remain required. Keep all historical records and valid existing plan schemas. Maintenance check stays read-only.
Boundary/API: Preserve helper filenames and arguments. Optional folder policy is shared between generation and validation; decisions/specs records remain validated when present.
Effects and failures: Local instructions, tests and generated indexes change. Delete only the verified index-only decisions folder. Failed checks block publication; no production effects.
Tests and evidence: Add failing temporary-root cases proving absent optional directories stay absent and populated optional folders gain required indexes; update checkpoint assertions to the new contract.
Verification: Full unittest suite, skill validation and metadata parse, hub refresh/check, diff review, selected-file dry run and publication.

## Code Changes
Share optional-artifact index policy and update generator/validator consumers; update workflow instructions and metadata together.

## Files and Modules
Targets are listed in Task 1. Preserve historical docs and the optional decision template/helper.

## Unit Testing
Exercise absent and populated optional folders, required indexes, read-only checks, plan checkpoint rules, and full existing regressions.

## Local Testing
Temporary-root CLI scenarios are sufficient; no application runtime impact or runtime report applies.

## Validation
Semantic review: inspected targets and explicit acceptance checks cover the approved scope; no unresolved blockers. Mechanical plan validation runs before saving.

## Acceptance Criteria
Default delivery needs no separate spec. The plan records acceptance criteria and design decisions. Specs remain available for the three stated reasons. The decisions directory is absent after maintenance; existing specs and all other historical records remain. All required checks and selected-file publication pass.

## Rollback or Recovery
Revert this task's implementation commit; no historical data is removed apart from the empty generated decisions index.

## Risks
Old checkpoint wording can reintroduce a spec gate. Generator and validator must agree on optional folder policy. Historical references to the empty decisions index must be checked before deletion.

## Completion Criteria
New default documented consistently, optional-folder cases pass, unnecessary folder removed, evidence and continuity published.

## Completion Evidence

Published implementation `d5bd048` after plan checkpoint `c0ad2e5`. All 56 tests passed, all 11 skills and metadata validated, hub refresh/check passed with eight unchanged historical plan warnings, and independent review found no blockers. Only the empty decisions index was deleted; all historical records remain. See [session continuity](../session-memory/2026-09-06-plan-first-builder-workflow.md).
