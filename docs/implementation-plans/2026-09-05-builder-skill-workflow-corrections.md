# Builder Skill Workflow Corrections

## Plan Format
task-contract-v1

## Document Status
complete

## Objective
Implement the five approved skill corrections and their dependent contracts.

## Goals
Prevent unrelated commits, make delivery gates consistent, permit maintainable plans, and preserve production during local verification.

## Inputs
- [Approved scope](../session-memory/2026-09-05-builder.md#source-docs-specs-2026-09-05-builder-skill-workflow-corrections-md).
- User selected the five fixes from the preceding audit; no additional design approval is needed.

## Branch
`main` in the configured Builder root, using explicit file staging and scoped pushes.

## Non-Goals
No live deployment, spoke source changes, unselected skill consolidation, or Superpowers edits.

## Assumptions
The initial checkout is clean. Existing literal-patch plans must remain accepted.

## Open Questions
None.

## Task Breakdown

### Task 1 - Bound Git commits and support push recovery
Dependencies: None.
Files: `.agents/skills/commit-push-builder-main/scripts/commit_push_builder_main.py`, `.agents/tests/test_commit_push_builder_main.py`
Symbols: `parse_args`, `main`, Git behavior tests.
Inspection: Read current helper and tests on Builder main before edits.
Required skill: write-jane-street-style-code before code edits.
Before-Edit Brief:
- Behavior: Commit selected files only; an explicit push-only mode retries an existing commit without staging changes.
- Invariants: Root, branch, and remote remain pinned; unrelated staged changes cause refusal; invalid paths cannot select outside the repository.
- Boundary/API: `.agents/skills/commit-push-builder-main/scripts/commit_push_builder_main.py`, inspected `parse_args` and `main` (current lines 32-131); add repeatable `--path` and separate `--push-only` operation.
- Effects and failures: Git index, commits, and remote writes; surface failures and preserve the committed hash for recovery. Do not reset unrelated changes or force push.
- Tests and evidence: Real temporary Git repositories/local bare remotes exercise selected commits, unrelated index refusal, literal paths, dry runs, and rejected-push recovery; witness failures before implementation.
Verification: `python -B -m unittest discover -s .agents/tests -p test_commit_push_builder_main.py`.

### Task 2 - Accept task contracts while preserving legacy plans
Dependencies: Task 1 regression evidence captured; implementation may proceed independently.
Files: `.agents/lib/artifact_quality.py`, `.agents/tests/test_artifact_quality.py`, plan skill entrypoints and metadata.
Symbols: `validate_implementation_plan_text`, plan task schema, readiness guidance.
Inspection: Read shared validator, CLI wrappers, legacy fixture, and all three plan skills on Builder main.
Required skill: write-jane-street-style-code before code edits.
Before-Edit Brief:
- Behavior: Validate plans with inspected file/symbol task contracts and concrete verification without requiring prewritten patches.
- Invariants: Every task has its own contract or valid legacy Code Edit; empty status, missing required sections, empty task fields, and unresolved execution prerequisites fail.
- Boundary/API: `.agents/lib/artifact_quality.py`, inspected `validate_implementation_plan_text` (lines 152-199); save/review/validate skills, their metadata, `AGENTS.md`, and `docs/status-model.md` consume the same contract.
- Effects and failures: Pure text validation gates CLI file saves; errors must prevent partial artifact writes.
- Tests and evidence: Real valid/invalid Markdown fixtures and save CLI invocations prove both supported formats and reject mixed-plan tasks with missing evidence.
Verification: `python -B -m unittest discover -s .agents/tests -p test_artifact_quality.py` and the plan save CLI in a temporary directory.

### Task 3 - Align closure, Spring operations, and Windows registration
Dependencies: Baseline instruction scenarios captured.
Files: `.agents/skills/complete-story-issue/SKILL.md`, `.agents/skills/close-story-issue/SKILL.md`, `.agents/skills/verify-local-spring-app/SKILL.md`, `.agents/skills/register-spoke-repo/SKILL.md`, their metadata, `AGENTS.md`.
Symbols: Delivery sequence, runtime classification, deployment scope, root discovery.
Inspection: Read entrypoints, metadata, and root policy; independent baseline review confirmed contradictory instructions.
Required skill: write-jane-street-style-code before code-bearing edits.
Before-Edit Brief:
- Behavior: Runtime reports are conditional on runtime impact/request; continuity evidence precedes closure; verification-only requests leave production untouched; registration uses the actual Builder root.
- Invariants: Required runtime proof cannot be replaced by unit tests; production deployment needs existing authority, isolated candidate validation, an identified deployment mechanism, rollback, and health criteria.
- Boundary/API: Inspected `complete-story-issue`, `close-story-issue`, `verify-local-spring-app`, `register-spoke-repo` entrypoints and `agents/openai.yaml`; align `AGENTS.md`.
- Effects and failures: Instructions control external writes and services; local testing never implies permission to deploy. Effective database configuration is checked before any database-backed test or startup.
- Tests and evidence: Independent scenarios cover documentation-only closure, missing runtime proof, pre-existing authorization, Windows registration, and managed-service testing. Do not access production.
Verification: Independent skill scenario review plus existing Builder workflow tests.

### Task 4 - Verify and publish the completed correction
Dependencies: Tasks 1-3.
Files: `.agents/tests`, selected skill metadata, Builder docs/indexes.
Symbols: Test discovery, artifact validators, index generation, commit helper.
Inspection: Read existing tests, helper entrypoints, and hub validation results on Builder main.
Required skill: write-jane-street-style-code before code-bearing edits.
Before-Edit Brief:
- Behavior: Publish only the reviewed Builder changes and evidence.
- Invariants: Existing unrelated state is preserved and no live application is restarted.
- Boundary/API: Builder test suite, skill metadata/frontmatter, index generator, hub validator, and guarded commit helper.
- Effects and failures: Generated Markdown and scoped Git push; failed checks prevent completion.
- Tests and evidence: Full suite, CLI scenarios, independent review, diff check, and remote synchronization evidence.
Verification: `python -B -m unittest discover -s .agents/tests`; index/hub checks; `git diff --check`; reviewed commit and push result.

## Code Changes
Task 1 changes Git CLI behavior; Task 2 changes plan validation; Task 3 changes workflow policy and metadata.

## Files and Modules
Targets are named in each task's Boundary/API. Existing helper wrappers retain their interfaces unless explicitly stated.

## Unit Testing
Failing regression scenarios precede behavior changes; run the complete Builder unittest suite once the focused cases pass.

## Local Testing
Exercise the helper against real disposable Git repositories and local bare remotes. Invoke plan saving in a temporary directory. Application runtime smoke testing is not applicable: this task changes Builder tooling and instructions, not the Spring application.

## Validation
The task-contract format is the user-approved replacement for mandatory literal patches. This bootstrap plan intentionally supplies the new format before the validator supports it; its initial rejection is baseline evidence. Review found concrete targets, dependency order, invariants, verification, and rollback sufficient for execution under the approved change.

## Rollback or Recovery
Revert the correction commits. Retain literal-plan compatibility; never force push. A failed remote push is retried with the helper's explicit push-only operation after inspecting outgoing commits.

## Risks
Existing policy-string tests may need contract updates. Repository-relative paths need literal Git handling and index checks. Keep historical plans unchanged.

## Completion Criteria
Regression and compatibility cases pass, skill scenarios have no blocking ambiguity, hub validation passes, and reviewed changes are pushed to Builder main.
