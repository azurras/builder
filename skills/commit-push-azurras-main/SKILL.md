---
name: commit-push-azurras-main
description: Commit and push completed changes to the main branch of only the azurras repository at /Users/cbell/Developer/azurras. Use after saving session memory, project specs, implementation plans, or other completed azurras workflow hub changes that should be persisted to GitHub main.
---

# Commit Push Azurras Main

## Overview

Commit completed azurras workflow hub changes and push them to `main`. This skill is intentionally scoped to `/Users/cbell/Developer/azurras` and must not be reused for other repositories.

## Guardrails

- Operate only on `/Users/cbell/Developer/azurras`.
- Require the current Git branch to be `main`.
- Require `origin` to be `https://github.com/azurras/azurras.git`.
- Never run this workflow from another repo, worktree, branch, or remote.
- Inspect `git status --short` before committing. Do not include unrelated or surprising changes without calling them out.
- Use a concise commit message that describes the completed workflow update.
- Push with `git push origin main` after the commit succeeds.

## When To Run

Run this after successful saves from these repo-local skills:

- `save-session-memory`
- `save-project-spec`
- `save-implementation-plan`

Also run it after other completed azurras workflow hub changes when the user asks to persist them to `main`.

## Workflow

1. Confirm the repo root is `/Users/cbell/Developer/azurras`.
2. Confirm the branch is `main` and the `origin` remote matches the azurras GitHub repo.
3. Review `git status --short`.
4. Stage intended changes. Include generated docs and skills; exclude local junk such as `.DS_Store`.
5. Commit with a clear message.
6. Push to `origin main`.
7. Report the commit hash and push result.

## Helper Script

Use `scripts/commit_push_azurras_main.py` for the guarded commit and push:

```bash
python3 /path/to/commit-push-azurras-main/scripts/commit_push_azurras_main.py \
  --message "Save workflow hub updates"
```

Use `--dry-run` to verify the repo, branch, remote, status, and intended commit message without staging, committing, or pushing.
