# Repair the Historical Migration Audit

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
`consolidate_project_memory.py --root . --source-commit 78f0183 --verify` passes on Builder main and keeps passing when later skill renames move files, while still rejecting any unrecorded edit to an imported section.

## Background
While filling skill detail gaps on 2026-10-04 ([plan](2026-10-04-fill-builder-skill-detail-gaps.md)), the audit failed with "Source preservation failed: docs/skill-migration.md", independent of that change. The user asked to fix it. Inspection found two causes in the one differing line of `docs/session-memory/2026-09-06-builder.md`:
1. `relocate_link` in `.agents/lib/memory_migration.py` relocates a link only when its target exists in the current working tree. At migration time `.agents/skills/maintain-builder-hub/references/phase-finalization.md` existed, so the link became `../../.agents/skills/maintain-builder-hub/...`. Commit `33b3965` retired that skill, so the audit now leaves the link unrelocated (`../.agents/...`) and expects text that never existed on disk. Expectations drift whenever a file moves.
2. Commits `33b3965` and `4cdd6c8` deliberately retargeted that link on disk (to `commit-push-builder-main`, then `publish-builder-changes`) so the hub link check stays green. The audit has no way to accept a recorded correction.

## Goals
- The audit's expected text depends only on the source commit, not on the current tree (AC-1).
- A reviewed list of later link retargets is accepted, and any other change still fails (AC-2, AC-3).
- The real repository passes the audit and a test keeps it that way (AC-4).
- Delivered on Builder main (AC-5).

## Non-Goals
- No rerun of `--apply`. Reason: the migration is complete; the reference forbids it.
- No revert of the retargeted link. Reason: the old target no longer exists and the hub link check would fail.
- No generic "ignore link targets" comparison. Reason: it would accept any link edit, weakening the audit.
- No change to how imported sections are rendered. Reason: the on-disk record is correct.

## Acceptance Criteria
- AC-1: `transform` accepts the set of paths present at the source commit and uses it to decide whether a link target exists; the audit passes that set built from `git ls-tree -r` of the source commit. A unit test shows a link whose target exists in the set but not on disk is relocated.
- AC-2: The audit applies each entry of a reviewed `LATER_LINK_RETARGETS` list to the expected section of its memory file before comparing, and fails when an entry no longer matches anything.
- AC-3: An unrecorded edit inside an imported section still fails `--verify`; the existing fixture test in `test_project_memory.py` keeps passing.
- AC-4: `--verify` on the real Builder root exits 0 with "Every imported source body matches", and a new test runs it (skipped when commit `78f0183` is absent, for shallow clones).
- AC-5: The plan, change and dated memory are on Builder origin/main, confirmed by `git ls-remote`.

## Inputs
- User request in chat on 2026-10-04: "let's fix that save session memory issue".
- Inspected on Builder `main` at `a52297a`, clean tree: `consolidate_project_memory.py` (`prepare`, `verify_sections`, `main`), `.agents/lib/memory_migration.py` (`relocate_link`, `transform`), `.agents/tests/test_project_memory.py`, `save-session-memory/references/migration-audit.md`, `git show 78f0183:docs/skill-migration.md` line 39, the diffs of `33b3965` and `4cdd6c8` to `docs/session-memory/2026-09-06-builder.md`, and a diff of the audit's expected section against disk showing that one line as the only difference.

## Branch
Builder primary checkout `main` at `a52297a`; publish the exact task files through publish-builder-changes.

## Assumptions
- Directories referenced by links are implied by the files under them, so the existing-path set includes every parent folder of each listed file.
- Builder has no CI workflow, so the real-repository test runs where developers run the suite, which have full history.

## Open Questions
None.

## Design
Pass existence explicitly. `relocate_link` and `transform` gain an optional `existing_paths` set of resolved paths; when present, a target "exists" only if it is in the set, otherwise the current filesystem check remains (keeping existing callers and tests unchanged). `prepare` builds the set from the source commit's full tree, so the expected text is fixed by the commit.

Record corrections explicitly. A module constant `LATER_LINK_RETARGETS` holds `(memory file, migrated link, current link)` tuples with a comment saying why each exists. `verify_sections` against disk replaces `](<migrated link>)` with `](<current link>)` in the expected sections of that file. An entry that matches no expected section raises, so stale entries cannot linger. The self-consistency check of generated outputs runs without retargets, as now.

Alternatives considered:
- Ignore link targets when comparing: rejected (Non-Goals).
- Store the retarget in the memory file as a later entry and restore the old link: rejected because the old link is dead and the hub check rejects dead links.
- Snapshot the expected sections into a fixture file: rejected; it duplicates 267 documents and hides the transformation.

## Expected Changes
- `.agents/lib/memory_migration.py`: `existing_paths` parameter on `relocate_link` and `transform`.
- `.agents/skills/save-session-memory/scripts/consolidate_project_memory.py`: build the existing-path set from the source commit; `LATER_LINK_RETARGETS`; retarget-aware verification.
- `.agents/tests/test_project_memory.py`: unit test for commit-based existence; real-repository audit test; unrecorded-edit test.
- `.agents/skills/save-session-memory/references/migration-audit.md`: explain recorded retargets and that a rename touching an imported link adds an entry in the same change.
- This plan, today's Builder session memory and regenerated indexes.

## Task Breakdown

### Task 1 - Make the audit deterministic and accept recorded retargets
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: .agents/lib/memory_migration.py; .agents/skills/save-session-memory/scripts/consolidate_project_memory.py; .agents/tests/test_project_memory.py; .agents/skills/save-session-memory/references/migration-audit.md.
Symbols: `relocate_link`, `transform`, `prepare`, `verify_sections`, new `LATER_LINK_RETARGETS`, new helper building existing paths, new tests in the migration test class.
Inspection: Read all four files and the relevant commits at `a52297a`; diffed expected and actual sections.
Behavior: The audit passes on the real repository; unrecorded edits fail; stale retarget entries fail.
Invariants: `--apply` output for a fresh corpus is unchanged; imported sections on disk are not edited; the audit stays read-only.
Boundary/API: New keyword-only optional parameter; existing calls keep working.
Effects and failures: One extra read-only `git ls-tree` call. Failures stay `ValueError` with the source path.
Tests and evidence: The real-repository test fails before the fix with the current error and passes after; new unit tests for existence and unrecorded edits.
Verification: python -B -m unittest discover -s .agents/tests; the audit command above; check_hub.py check; git diff --check.

### Task 2 - Record and publish verified delivery
Dependencies: Task 1 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day Builder memory and the phase finalizer at `a52297a`.
Behavior: The completed change and its dated evidence are on origin/main.
Invariants: Only selected files are committed.
Boundary/API: publish-builder-changes helper.
Effects and failures: Scoped commit and push; a failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Runtime verification does not apply: Builder has no runnable application; the audit is a standalone read-only helper exercised end to end against the real repository and temporary Git fixtures.
- AC-1: new unit test calling `transform` with `existing_paths` containing a target that is absent on disk.
- AC-2: real-repository audit passes only with the retarget entry; a unit test of the retarget helper raises for an entry that matches nothing.
- AC-3: new fixture test edits an imported line after `--apply` and expects `--verify` to fail; existing `test_nested_examples_are_preserved_and_unknown_sources_rejected` passes.
- AC-4: new `test_real_repository_passes_migration_audit`, run before the fix (fails) and after (passes); manual audit command output.
- AC-5: helper output and `git ls-remote origin refs/heads/main` compared with local HEAD.

## Rollback or Recovery
Revert the change commit; the audit returns to its failing state with no data effect. A failed push keeps the commit and recovers with `--push-only`.

## Risks
- The commit-based existence set changes expectations for other links. Mitigation: the real-repository audit compares all 267 sections, so any shift fails the test.
- Future renames will need a retarget entry. Mitigation: the real-repository test fails until one is added, and migration-audit.md says so.

## Implementation Log

### 2026-10-04 - Ignore retargets for memory files the corpus does not produce

- Change: `apply_later_link_retargets` skips an entry whose memory file the audited corpus does not produce; staleness is checked only for produced files.
- Reason: the fixture test's small corpus has no 2026-09-06 builder file, and the first version rejected the real entry there as stale.
- Impact: AC-2 unchanged in intent; the stale-entry unit test uses a produced file.

## Outcome
Delivered on 2026-10-04 with one logged refinement.
- AC-1: Met. `relocate_link` and `transform` take keyword-only `existing_paths`; the audit builds it from `git ls-tree -r` of the source commit with `paths_in_commit`. `test_link_existence_comes_from_the_supplied_source_tree` shows a target present in the set but absent on disk is relocated, and left alone without the set.
- AC-2: Met. `LATER_LINK_RETARGETS` holds the one recorded retarget (maintain-builder-hub to publish-builder-changes in the 2026-09-06 Builder memory). `test_stale_link_retarget_is_rejected` shows a non-matching entry raises.
- AC-3: Met. The fixture test now rewrites an imported line after `--apply` and `--verify` fails with "Source preservation failed"; the rest of that test passes unchanged.
- AC-4: Met. `test_real_repository_passes_migration_audit` failed before the fix with "Source preservation failed: docs/skill-migration.md" and passes now; the audit command prints "Every imported source body matches the full migration transformation." across all 267 sources.
- AC-5: Met when the delivery commit's `git ls-remote origin refs/heads/main` matches local HEAD; see the [2026-10-04 Builder memory](../session-memory/2026-10-04.md).
Checks: the full test suite passes, the hub check passes and `git diff --check` is clean. Runtime verification does not apply: no runnable application.
Shipped versus planned: as planned plus the produced-file refinement. No follow-ups.
