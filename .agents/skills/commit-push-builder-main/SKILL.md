---
name: commit-push-builder-main
description: Commit and push completed changes to the main branch of only the builder repository. Use after saving session memory, project specs, implementation plans, or other completed builder workflow hub changes that should be persisted to GitHub main.
---

# Commit Push Builder Main

## Overview

Commit completed builder workflow hub changes and push them to `main`. This skill is intentionally scoped to `C:\Users\Christopher\Developer\builder` on Windows and `/Users/cbell/Developer/builder` on macOS, and must not be reused for other repositories.

## Guardrails

- Operate only on `C:\Users\Christopher\Developer\builder` on Windows or `/Users/cbell/Developer/builder` on macOS.
- Require the current Git branch to be `main`.
- Require `origin` to be `https://github.com/azurras/builder.git`.
- Never run this workflow from another repo, worktree, branch, or remote.
- Inspect `git status --short` before committing. Do not include unrelated or surprising changes without calling them out.
- Use a concise commit message that describes the completed workflow update.
- Push with `git push origin main` after the commit succeeds.

## When To Run

Run this after successful saves from these repo-local skills:

- `save-session-memory`
- `save-project-spec`
- `save-implementation-plan`

Also run it after other completed builder workflow hub changes when the user asks to persist them to `main`.

## Workflow

1. Confirm the repo root is `C:\Users\Christopher\Developer\builder` on Windows or `/Users/cbell/Developer/builder` on macOS.
2. Confirm the branch is `main` and the `origin` remote matches the builder GitHub repo.
3. Review `git status --short`.
4. Stage intended changes. Include generated docs and skills; exclude local junk such as `.DS_Store`.
5. Commit with a clear message.
6. Push to `origin main`.
7. Report the commit hash and push result.

## Helper Script

Use `scripts/commit_push_builder_main.py` for the guarded commit and push:

```bash
python3 /path/to/commit-push-builder-main/scripts/commit_push_builder_main.py \
  --message "Save workflow hub updates"
```

Use `--dry-run` to verify the repo, branch, remote, status, and intended commit message without staging, committing, or pushing.
