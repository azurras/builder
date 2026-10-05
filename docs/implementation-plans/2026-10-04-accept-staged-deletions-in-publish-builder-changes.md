# Accept Staged Deletions in Publish Builder Changes

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
`publish_builder_changes.py` publishes a selection that includes a deletion already staged in the index, such as the old side of a `git mv`, without the caller unstaging anything first.

## Background
While publishing the [deliver-change rename](2026-10-04-rename-complete-builder-work-to-deliver-change.md) on 2026-10-04, the helper refused `.agents/skills/complete-builder-work/SKILL.md` with "Selected file does not exist and is not a tracked deletion" and committed nothing. `selected_paths` treats a missing file as a deletion only when `git ls-files` still lists it in the index, but `git mv` and `git rm` remove the path from the index. A reproduction in a scratch repository showed a second failure behind the first: `git add -- old.md` exits 128 with "pathspec 'old.md' did not match any files" once the deletion is staged. The workaround was `git reset` on the moved paths so the helper could stage both sides. Every rename hits this. The user asked to fix the helper.

## Goals
- A staged deletion in the selection is committed with the rest of the selection (AC-1).
- An unstaged deletion of a tracked file works as it does today (AC-2).
- A path that is in neither HEAD nor the index is still rejected, and the unrelated-staged-files guard is unchanged (AC-3).
- The change is published on Builder main (AC-4).

## Non-Goals
- No change to staging scope: the helper still stages only the selected literal paths, never directories or globs.
- No new flags or output format changes. The fix is in path classification only.
- No SKILL.md wording change beyond what becomes inaccurate. "Tracked deletions work" stays true and now covers staged ones.

## Acceptance Criteria
- AC-1: In a test repository, after `git mv old.md new.md`, invoking the helper with `--path old.md --path new.md` exits 0, and HEAD's commit records `old.md` deleted and `new.md` added. The same holds after `git rm old.md` with `--path old.md`.
- AC-2: The existing `test_selected_deletion_is_committed` (file removed from disk, still in the index) passes unchanged.
- AC-3: Selecting `missing.md` (never tracked) still fails without changing the index, and the existing unrelated-staged, deleted-directory, dry-run, worktree and push-only tests pass unchanged. A dry run with a staged deletion leaves index, HEAD and remote unchanged.
- AC-4: The plan, the change and the dated delivery memory are on origin/main, confirmed by remote readback.

## Inputs
- User request in chat on 2026-10-04: "let's fix that helper", after I reported the staged-rename refusal.
- Inspected on Builder `main` at `6c59551`, clean tree: `.agents/skills/publish-builder-changes/scripts/publish_builder_changes.py` (`selected_paths`, `main`), `.agents/tests/test_publish_builder_changes.py` (`CommitPushBehaviorTests`), publish-builder-changes SKILL.md, write-chris-street-style-code SKILL.md and its Python reference; a scratch-repository reproduction of `git mv` followed by `git --literal-pathspecs add -- old.md new.md` and `git --literal-pathspecs ls-tree -z --name-only HEAD -- old.md`.

## Branch
Builder primary checkout `main` at `6c59551`; publish the exact task files through publish-builder-changes.

## Assumptions
- `git --literal-pathspecs ls-tree -z --name-only HEAD -- <path>` prints exactly `<path>\0` for a file tracked in HEAD and nothing otherwise, as the reproduction showed.
- `git diff --cached --name-only --no-renames` lists a staged deletion under its old path, so the existing unrelated-staged guard accepts it once it is selected. The reproduction showed `new.md` and `old.md`.

## Open Questions
None.

## Design
Classify each selected path by where it exists: on disk, in the index, in HEAD. A missing file is a valid deletion when it is still in the index (deletion not yet staged; `git add` stages it) or when it is in HEAD but not the index (deletion already staged). Anything else is rejected as today. `main` then runs `git add` only on paths that still need staging and skips paths whose deletion is already staged, because `git add` fails on them. The post-add check that the staged set stays within the selection is unchanged, and so is the empty-commit check.

`selected_paths` still returns the validated selection. Two named predicates, `is_in_index` and `is_in_head`, make the rule read directly at the call site. The staging list is computed in `main` as the selected paths that exist on disk or are still in the index.

Alternatives considered:
- `git add -A -- <paths>` or `git add --ignore-missing`: rejected. Both still fail or are dry-run-only for a pathspec that matches nothing in the index or working tree.
- `git rm --cached` for staged deletions: rejected because they are already staged; another index write adds a failure mode and nothing else.
- Have callers stop using `git mv`: rejected because the skill already says to name both sides of a rename, and `git mv` is the normal way to rename.

## Expected Changes
- `.agents/skills/publish-builder-changes/scripts/publish_builder_changes.py`: `is_in_index` and `is_in_head` helpers; `selected_paths` accepts a missing path found in either; `main` stages only paths on disk or in the index.
- `.agents/tests/test_publish_builder_changes.py`: tests for a staged `git mv` rename, a staged `git rm` deletion, and a dry run with a staged deletion.
- This plan, today's Builder session memory and regenerated indexes.

## Task Breakdown

### Task 1 - Accept and commit staged deletions
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: .agents/skills/publish-builder-changes/scripts/publish_builder_changes.py; .agents/tests/test_publish_builder_changes.py.
Symbols: `selected_paths`; new `is_in_index`, `is_in_head`; staging block in `main`; `CommitPushBehaviorTests` new test methods.
Inspection: Read the full helper and test module on main `6c59551`; reproduced both failures in a scratch repository.
Behavior: A selection containing a staged deletion commits it; unstaged deletions and additions behave as before; untracked missing paths are refused.
Invariants: Only selected literal paths are staged or committed; unrelated staged files still block the commit before any index write; dry run writes nothing.
Boundary/API: CLI arguments and output unchanged; error message for an unknown missing path unchanged.
Effects and failures: Adds read-only `git ls-tree` calls. Git failures still surface through `CalledProcessError` with stderr.
Tests and evidence: New tests fail on current code (staged rename refused) and pass after; existing tests unchanged.
Verification: python -B -m unittest .agents/tests/test_publish_builder_changes.py, run before and after the fix; python -B -m unittest discover -s .agents/tests; git diff --check.

### Task 2 - Record and publish verified delivery
Dependencies: Task 1 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day Builder memory and the phase finalizer at `6c59551`.
Behavior: The completed change and its dated evidence are on origin/main.
Invariants: Only the selected files are committed; earlier history is preserved.
Boundary/API: The fixed publish-builder-changes helper.
Effects and failures: Scoped commit and push. A failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run, then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Runtime verification does not apply. Builder holds workflow instructions and standalone Python helpers, not a runnable application. The helper's tests run it end to end against real temporary Git repositories and a bare remote.
- AC-1: New `test_staged_rename_is_committed` and `test_staged_removal_is_committed`; run first against current code to confirm they fail.
- AC-2: Existing `test_selected_deletion_is_committed`.
- AC-3: Existing `test_requires_selection_and_rejects_broad_or_outside_paths` (`missing.md`), unrelated-staged, deleted-directory, worktree and push-only tests; new `test_dry_run_with_staged_deletion_changes_nothing`.
- AC-4: Helper output and `git ls-remote origin refs/heads/main` compared with the local HEAD. Publishing this change's own files does not need the fix, but the next rename will.

## Rollback or Recovery
Revert the task commit; the helper returns to refusing staged deletions, which fails safe. If a push fails, keep the commit and recover with `--push-only`.

## Risks
- Accepting HEAD-only paths could let a caller select a path whose deletion someone else staged. Low impact: the caller already names the path explicitly, and the unrelated-staged guard is unchanged for everything not named.
- `ls-tree` on a repository with no commits fails. The helper already requires an existing main with a remote; the check treats a failed lookup as "not in HEAD".

## Implementation Log
- 2026-10-04 Discovery: `git ls-tree HEAD -- nested` lists a deleted folder as one entry, so the first `is_in_head` let `--path nested` through and `test_deleted_directory_cannot_expand_selection_or_mutate_index` failed. Decision: add `-r` so a folder lists its files and fails the exact-match check. Reason: the folder guard is a stated invariant; the existing test caught it.
- 2026-10-04 Discovery: another session's uncommitted spoke-registry edits (plan `3172504`) made seven spoke tests fail in the shared checkout. Decision: run the full suite in a temporary detached worktree at `3172504` with only this change applied, and publish only this change's files. Reason: preserve their work and prove this change in isolation.

## Outcome
Delivered on 2026-10-04 with one design correction (`ls-tree -r`, logged above).
- AC-1: Met. `test_staged_rename_is_committed` (`git mv`, both sides selected; HEAD records `D baseline.md`, `A renamed.md`, clean tree) and `test_staged_removal_is_committed` (`git rm`) failed on the old helper with "not a tracked deletion" and pass now.
- AC-2: Met. `test_selected_deletion_is_committed` passes unchanged.
- AC-3: Met. `missing.md` rejection, the unrelated-staged, deleted-directory, dry-run, worktree and push-only tests pass unchanged; `test_dry_run_with_staged_deletion_changes_nothing` passes. All 13 helper tests and all 72 suite tests pass on `3172504` plus this diff; `git diff --check` is clean.
- AC-4: Met. Published with the fixed helper and confirmed by `git ls-remote origin refs/heads/main` matching local HEAD; see the [2026-10-04 Builder memory](../session-memory/2026-10-04.md).
Shipped versus planned: as planned plus `-r`. No follow-ups.
