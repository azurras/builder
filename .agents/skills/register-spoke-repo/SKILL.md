---
name: register-spoke-repo
description: Register or update an external spoke repository in the Azurras hub. Use when adding a repo that agents may work in from the hub, recording its local path, remote URL, default branch, purpose, active status, guardrails, or notes.
---

# Register Spoke Repo

## Overview

Maintain the canonical spoke repository registry for the Azurras hub-and-spoke workflow. This skill records which external repos are controlled or coordinated from the hub.

## Storage Rules

- Store the registry at `docs/spokes/repos.md`.
- Use one Markdown section per spoke repo.
- Update an existing section when the same repo slug is registered again.
- Keep entries factual: local path, remote, default branch, purpose, status, guardrails, and notes.

## Workflow

1. Confirm the active hub root is `/Users/cbell/Developer/azurras`.
2. Collect the spoke repo name, local path, remote URL, default branch, and purpose.
3. Record guardrails such as branch policy, test expectations, ownership, and whether direct pushes are allowed.
4. Update `docs/spokes/repos.md`, preferring the helper script.
5. Save session memory and use `commit-push-azurras-main`.

## Helper Script

```bash
python3 .agents/skills/register-spoke-repo/scripts/register_spoke_repo.py \
  --name "Repo Name" \
  --path "/path/to/repo" \
  --remote "https://github.com/org/repo.git" \
  --purpose "What this repo owns"
```

The helper creates or updates the matching repo section in `docs/spokes/repos.md`.
