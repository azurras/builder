---
name: commit-push-builder-main
description: Commit selected Builder files to main or retry pushing an existing Builder commit. Use for authorized Builder artifact checkpoints and completed hub changes.
---

# Commit Push Builder Main

Operate only in `C:\Users\Christopher\Developer\builder` on Windows or `/Users/cbell/Developer/builder` on macOS, branch `main`, origin `https://github.com/azurras/builder.git`. Do not use this workflow in a spoke repository or linked worktree.

## Select the Operation

- **Commit selected files:** Supply a nonblank `--message` and repeat `--path` for each intended repository-relative file. Directories, outside paths, symlinks, `.git`, and machine metadata are rejected. Paths are literal filenames, not Git patterns. Include both old and new paths for a rename; tracked deletions are supported.
- **Retry a push:** Inspect the existing outgoing commits, then use `--push-only`. This pushes existing main commits without staging or committing, even when the working tree is clean. It does not accept `--path` or `--message`.

## Workflow

1. Verify root, branch, and origin; inspect `git status --short --branch` and the relevant working and staged diffs.
2. Refresh `origin/main` and inspect `git log --oneline origin/main..HEAD` before publishing; a push publishes all outgoing main commits. Resolve unexpected commits or divergence without force pushing.
3. Identify the exact files belonging to this task, including intended generated indexes. If any unrelated file is staged, stop before changing the index and resolve ownership with the existing context. Do not reset someone else's staged work.
4. Run the helper with the selected operation and `--dry-run`; review the paths, current state, and message. A dry run does not stage, commit, fetch, or push.
5. Run the same operation without `--dry-run`. The helper stages only selected files and refuses an index containing other files. Do not run concurrent index-changing commands.
6. Inspect the commit and push result. If commit succeeds but push fails, retain the commit; diagnose the failure and use `--push-only` after reviewing outgoing commits. Do not create an empty recovery commit or treat a clean working tree as proof of publication.
7. Report the commit hash and push result. If no selected changes exist, the commit operation does not push pending commits; use the explicit push operation when needed.

## PowerShell Examples

```powershell
python .agents/skills/commit-push-builder-main/scripts/commit_push_builder_main.py --message 'Save reviewed workflow update' --path 'docs/specs/2026-09-06-example.md' --path 'docs/specs/index.md' --dry-run
```

Replace example filenames with the exact files reviewed for the current task. Remove `--dry-run` to perform the authorized commit and push.

```powershell
python .agents/skills/commit-push-builder-main/scripts/commit_push_builder_main.py --push-only
```

## Checkpoints

Use this skill after `plan-builder-work` plan mode (or an explicitly requested spec-only save), `record-runtime-verification` report mode, and `save-session-memory`, and for other authorized Builder persistence checkpoints. Preserve the delivery loop's separate phase commits. Git/network failure is a failed checkpoint until the intended commit is published.
