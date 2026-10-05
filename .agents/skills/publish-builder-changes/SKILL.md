---
name: publish-builder-changes
description: Validate the Builder hub and publish selected Builder files to main, or retry pushing an existing Builder commit. Use for authorized Builder artifact checkpoints, completed hub changes, and hub index refresh or document validation.
---

# Publish Builder Changes

Use only in the primary Builder checkout on `main`, never in a spoke or linked worktree. The helper refuses any other root, branch, origin or worktree.

## Choose the Operation

- **Commit selected files:** a nonblank `--message` and one `--path` per repository-relative file. Paths are literal files; name both sides of a rename. Tracked deletions work.
- **Retry a push:** `--push-only` pushes existing main commits without staging or committing, even when the working tree is clean.

## What You Own

The helper validates paths, refuses to commit when files outside the selection are staged, and makes no changes in `--dry-run`. These decisions are yours:

1. **Selection.** Name exactly the task's files, plus the index of each document folder where you added, renamed or removed a document: `docs/implementation-plans/index.md`, `docs/test-reports/index.md` or `docs/session-memory/index.md`. `check_hub.py refresh` regenerates them; select only those it changed for your documents. Other people's staged or working changes stay as they are; resolve who owns them before touching the index.
2. **Message.** A short imperative subject in sentence case with no trailing period, as in the history: `Plan <change>` for a plan checkpoint, and the outcome itself for the change commit, which usually also carries the completed plan and memory (`Accept staged deletions in publish-builder-changes`). A separate report or memory checkpoint uses `Record <what>`. Add any attribution trailer your harness requires after a blank line.
3. **Outgoing commits.** A push publishes every commit in `git log --oneline origin/main..HEAD`. Fetch and inspect them first; every one must be yours or explicitly approved. When `origin/main` has commits you lack, run `git pull --rebase origin main`, resolve conflicts by keeping both sides' intent, rerun `check_hub.py check`, then push with `--push-only`. If Git refuses because of uncommitted changes, commit your own task files first; never stash, reset or discard files you do not own. Never force push.
4. **Dry run first.** Review the dry-run output, then run the same command without `--dry-run`.
5. **Failure.** If the commit succeeds and the push fails, keep the commit, find the cause, and use `--push-only`. A clean tree does not prove publication, and an empty recovery commit is never correct.

Report the commit hash and push result.

```powershell
python .agents/skills/publish-builder-changes/scripts/publish_builder_changes.py --message 'Save reviewed workflow update' --path 'docs/implementation-plans/2026-09-06-example.md' --path 'docs/implementation-plans/index.md' --dry-run
python .agents/skills/publish-builder-changes/scripts/publish_builder_changes.py --push-only
```

## Hub Check

`python .agents/skills/publish-builder-changes/scripts/check_hub.py check --root .` runs a read-only check of the indexes, document conventions, links, skill frontmatter and the `.claude/skills` symlink. `refresh` also regenerates the three indexes. Eight historical pre-schema plans remain warnings; add no new exemptions.

## Checkpoints

Run the [phase finalizer](references/phase-finalization.md) after `write-implementation-plan` plan mode, `write-test-report` report mode, `save-session-memory`, and other authorized Builder persistence. Keep the delivery loop's phase commits separate. A Git or network failure leaves the checkpoint failed until the commit is published.
