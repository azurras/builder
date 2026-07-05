---
name: sync-spoke-state
description: Snapshot current Git state for registered spoke repositories into the Azurras hub. Use when checking active cross-repo work, auditing dirty spoke repos, refreshing branch/commit/remote status, or reconciling hub state with external repos.
---

# Sync Spoke State

## Overview

Read registered spoke repositories and write a hub-side state snapshot. This skill helps answer what is active, dirty, ahead/behind, blocked, or ready across spoke repos.

## Storage Rules

- Read spoke registrations from `docs/spokes/repos.md`.
- Write the latest snapshot to `docs/spokes/state.md`.
- Write Markdown only.
- Do not modify spoke repositories.

## Workflow

1. Ensure spoke repos are registered with `register-spoke-repo`.
2. Run the helper script from the Azurras root.
3. Review any missing paths or non-Git directories.
4. Save session memory and use `commit-push-azurras-main` when the snapshot changed.

## Helper Script

```bash
python3 .agents/skills/sync-spoke-state/scripts/sync_spoke_state.py
```
