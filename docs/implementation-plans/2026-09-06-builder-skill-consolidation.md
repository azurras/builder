# Builder Skill Consolidation

## Plan Format
task-contract-v1

## Document Status
complete

## Objective
Deliver the approved 22-to-11 Builder skill consolidation with compatible commands and verified operational boundaries.

## Goals
Reduce discovery overlap, deduplicate artifact writers, make repository state reliable, and centralize maintenance without weakening phase checkpoints.

## Inputs
[Approved specification](../session-memory/2026-09-06-builder.md#source-docs-specs-2026-09-06-builder-skill-consolidation-md), existing skill audit and repository session history.

## Branch
Builder main, canonical origin, explicit selected-file commits.

## Non-Goals
No Superpowers changes, spoke implementation, live service operation, or historical artifact rewrites.

## Assumptions
The checkout was clean before this task; existing helper CLI paths remain compatibility interfaces.

## Open Questions
None.

## Task Breakdown

### Task 1 - Consolidate dated artifact writers
Dependencies: None.
Files: `.agents/lib/artifact_io.py`, `.agents/lib/builder_hub.py`, `.agents/skills/start-hub-work/scripts/start_hub_work.py`, the five repeated artifact writers, `.agents/tests`.
Symbols: `save_dated_markdown`, `slugify`, legacy `main` entrypoints; new shared artifact CLI.
Inspection: Read shared helpers, repeated save implementations, and artifact save tests on main after commit 3f58c8e.
Required skill: write-jane-street-style-code before code edits.
Behavior: Legacy commands save the same artifact types and locations through shared code.
Invariants: Empty input and accidental overwrite fail; valid filenames/content and intentional overwrite remain compatible; plan/report validators and session append behavior remain intact.
Boundary/API: Preserve legacy arguments, exit success/failure, returned path, and output artifact; move mode-specific defaults to a shared catalog.
Effects and failures: Local Markdown writes only; no implicit Git, network, session-memory, or index operations.
Tests and evidence: Passing characterization tests across all six legacy writers before refactoring; rerun after shared implementation.
Verification: Run writer compatibility tests against temporary directories, including duplicate/overwrite and invalid inputs.

### Task 2 - Make repository inspection explicit and deterministic
Dependencies: None; can follow writer characterization.
Files: `.agents/skills/sync-spoke-state/scripts/sync_spoke_state.py`, `.agents/skills/register-spoke-repo/scripts/register_spoke_repo.py`, new manage-spoke-repositories command, `.agents/tests`.
Symbols: `git`, `parse_registry`, snapshot rendering and persistence, inspection/register command routing.
Inspection: Current sync helper ignores Git exit status, substitutes clean for empty output, and always writes a timestamp; registry CLI already accepts explicit root.
Required skill: write-jane-street-style-code before code edits.
Behavior: New inspection defaults read-only; explicit snapshots write only on semantic state change; legacy snapshot command remains available.
Invariants: A failed Git query cannot report clean; missing/broken repositories produce explicit errors and nonzero status; no source repository writes or fetches.
Boundary/API: Retain legacy --root command behavior; new interface distinguishes inspect, snapshot, and register.
Effects and failures: Read local Git state with bounded subprocess calls; optional hub snapshot write; retain error details.
Tests and evidence: Failing tests for read-only inspection, repeated snapshot preservation, and Git failure classification precede implementation.
Verification: Real temporary Git repo/registry plus missing and invalid repo cases; compare snapshot bytes/mtime across unchanged runs.

### Task 3 - Replace overlapping discovery with six focused entrypoints
Dependencies: Task 1 writer behavior understood; existing safety references inspected.
Files: `.agents/skills`, `AGENTS.md`, `README.md`, `.agents/tests/test_artifact_commit_checkpoints.py`, `.agents/tests/test_github_trust_boundary.py`, `.agents/tests/test_jane_street_code_style.py`.
Symbols: Six new SKILL entrypoints/metadata and focused references; retired entrypoints; active skill routing.
Inspection: Read all 22 Builder skills and metadata plus policy tests; read session history supporting checkpoints, runtime reports, reviews, and continuity.
Required skill: write-jane-street-style-code before code-bearing edits.
Behavior: Exactly 11 skills are discoverable. Spec-only, review-only, closure-only, coordination update, and maintenance check requests stay in their requested mode.
Invariants: Preserve coding standard, trust boundary, runtime evidence, committed continuity before closure, readback, separate phase commits, and existing authorization. Do not invent delegation or maintenance actions.
Boundary/API: Keep all legacy Python command paths; retire only old SKILL.md/UI metadata, route old names through a migration reference, and update current instructions/callers.
Effects and failures: Instruction/metadata edits only; each specialized mode loads its own reference; no historical evidence deletion.
Tests and evidence: Discovery/catalog and local-link checks plus independent realistic scenarios; update old policy-string tests to the new authoritative locations.
Verification: Exactly 11 valid skills, all metadata parses, no active references to retired skill invocations, and independent review has no blocking scope or gate regression.

### Task 4 - Centralize maintenance and publish evidence
Dependencies: Tasks 1-3.
Files: New maintain-builder-hub command; existing index/validation helpers; completed spec/plan and continuity record.
Symbols: check/refresh command sequencing and phase-finalization instructions.
Inspection: Index helper has read-only --check; validator is read-only; existing instructions redundantly create memory after index generation.
Required skill: write-jane-street-style-code before code edits.
Behavior: Check performs no writes; refresh updates indexes then validates; neither creates memory or commits. Phase owner writes artifacts first and publishes selected files after successful maintenance.
Invariants: Failed checks block completion; old helper commands remain usable; phase checkpoints stay separate.
Boundary/API: New maintenance modes compose existing tools through their public CLI interfaces.
Effects and failures: Refresh writes indexes only; Git publishing remains in commit-push-builder-main.
Tests and evidence: Check mode leaves fixture files unchanged; refresh restores indexes; full suite, metadata checks, and independent review before publishing.
Verification: Full unittest suite, skill validation, hub validation, git diff check, explicit selected-file dry run/commit/push, then clean synchronized main.

## Code Changes
Shared artifact CLI and snapshot behavior changes; six consolidated entrypoints with specialized references; compatibility commands retained.

## Files and Modules
Targets are listed per task. Five independent skills remain, with only routing/continuity wording updated where needed.

## Unit Testing
Characterization baseline for refactors; failing regressions for changed snapshot and maintenance behavior; full Builder suite after focused checks.

## Local Testing
Exercise actual CLI commands and Git in temporary directories. Application runtime report is not applicable because no application runtime behavior changes.

## Validation
Completed: 55 unittest cases passed, all 11 skill entrypoints and UI metadata validated, all 19 CLI --help checks passed, and hub validation passed with the same eight historical-plan warnings. Independent Python and mode-scenario reviews found no remaining blockers after correcting report-only scope and UI descriptions.

## Rollback or Recovery
Revert consolidation commits to restore old discovery. Legacy scripts and artifacts are retained throughout. Never force push or modify unrelated checkout state.

## Risks
Retired paths referenced by tests/current guidance must migrate; historical helper links remain valid. Snapshot errors must not masquerade as clean. Avoid replacing small entrypoints with large always-loaded manuals.

## Completion Criteria
11 discoverable skills; legacy command compatibility, snapshot and maintenance tests pass; checkpoints/safety scenarios preserved; docs/indexes validated; reviewed changes and continuity pushed.

## Completion Evidence

Implemented and pushed as `63ab5c8`. See the [migration map](../session-memory/2026-09-06-builder.md#source-docs-skill-migration-md) for all retired names and supported commands, and [completion continuity](../session-memory/2026-09-06-builder.md#source-docs-session-memory-2026-09-06-builder-skill-consolidation-md) for validation and final state. Runtime application testing is not applicable: these changes affect standalone Builder tools and workflow guidance; temporary-repository CLI scenarios supply native evidence.
