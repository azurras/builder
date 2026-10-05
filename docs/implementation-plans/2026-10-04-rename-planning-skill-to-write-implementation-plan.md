# Rename Planning Skill to Write Implementation Plan

## Plan Format
task-contract-v1

## Document Status
complete

## Objective
Rename the planning skill to `write-implementation-plan` and align every maintained reference.

## Goals
- Align directory, frontmatter, heading, UI metadata, invocation prompt, callers and tests.
- Preserve helper behavior, shared Claude symlink and dated session history.

## Inputs
User request in this chat; inspected AGENTS.md, README.md, planning skill entrypoint/references/metadata/scripts, caller skills, migration helper and three test modules.

## Branch
Builder primary checkout `main`, inspected at `8971c01`; publish exact task files through the Builder helper.

## Non-Goals
Change planning behavior, application code, deployment or unrelated coding-style work.

## Assumptions
The shared `.claude/skills` symlink follows the canonical directory automatically.

## Open Questions
None.

## Task Breakdown

### Task 1 - Rename the canonical skill and maintained references
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: Existing planning skill directory; AGENTS.md; README.md; complete-builder-work and commit-push-builder-main entrypoints; save-session-memory/scripts/consolidate_project_memory.py; test_skill_consolidation.py, test_project_memory.py, test_artifact_quality.py; four inspected implementation plans with skill references.
Symbols: Skill name, heading, interface.display_name, interface.default_prompt, skill discovery expectation, planning helper paths and migration template destination.
Inspection: Read current entrypoint, metadata, references, both unchanged planning helpers, caller sites and existing discovery/save/migration tests on main 8971c01; repository-wide search found no additional active identifiers.
Behavior: Discover and invoke write-implementation-plan; existing plan save, validation and migration operations work at the renamed directory.
Invariants: One canonical skill folder; eight skills; unchanged CLI filenames/arguments and invocation policy; no edits to historical session entries or unrelated dirty files.
Boundary/API: Directory and invocation identifier change together; no compatibility alias requested.
Effects and failures: Move within .agents/skills and replace maintained references; preserve bytes outside intended text; helper failures prevent publication.
Tests and evidence: Existing discovery, plan save/invalid-input and migration tests; full native Python suite; skill validator and hub checks.
Verification: python -B -m unittest discover -s .agents/tests; official skill quick validation; hub refresh; old-identifier scan excluding dated memory; git diff --check.

### Task 2 - Record and publish verified delivery
Dependencies: Task 1 checks and semantic review pass.
Files: This plan, docs/session-memory/2026-10-04-builder.md and generated document indexes.
Symbols: Document Status and appended delivery evidence.
Inspection: Read same-day Builder entries and phase finalizer; unrelated coding-style files are dirty and must be excluded.
Behavior: Publish completed change and dated evidence on origin/main.
Invariants: Exact selected files only; preserve earlier history and unrelated working/staged changes.
Boundary/API: Existing Builder publication helper and permitted document layout.
Effects and failures: Scoped commit and push; failed push remains incomplete and uses push-only recovery.
Tests and evidence: Passing native checks, reviewed diff and remote main readback.
Verification: Helper dry-run followed by publication; inspect commit and git ls-remote origin refs/heads/main.

## Code Changes
Identifier and path substitutions only; planning helper implementations retain behavior.

## Files and Modules
Canonical planning skill, inspected callers/tests/documents, dated evidence and indexes listed above.

## Unit Testing
Run existing native suite covering discovery, save validation, migration destination and Git checkpoint mechanics.

## Local Testing
Application runtime verification does not apply: Builder contains workflow instructions and standalone Python helpers, with no runnable application affected. Execute the actual helpers and native tests instead.

## Validation
Skill schema, hub navigation/frontmatter/shared symlink, migrated references, complete diff and whitespace checks.

## Rollback or Recovery
Revert only task commits and restore matching directory/references together; preserve unrelated work. Recover failed publication using the existing push-only workflow.

## Risks
A stale helper path breaks discovery or execution; tests and complete identifier search cover this risk. Dated session history intentionally retains historical identifiers.

## Completion Criteria
Canonical folder and metadata use write-implementation-plan; all maintained references updated; native checks and semantic review pass; completed plan and dated delivery evidence published; remote main readback confirms publication.

## Implementation Log

### 2026-10-04 - Delivered without updating dated plans

- Change: Delivered in `726787e`. The four dated implementation plans listed under Task 1 Files were left with the old skill name, and this plan was not marked complete at delivery.
- Reason: Dated plans and session memory are historical records under AGENTS.md, so they keep the name in force when written. The close-out was missed because the delivering session did not find this plan; it was found while planning living implementation plans.
- Impact: Task 1 scope narrowed to maintained files; Completion Criteria met except the hub refresh, which ran with the next checkpoint. Closed by the living implementation plans work.

