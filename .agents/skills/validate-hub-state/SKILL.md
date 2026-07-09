---
name: validate-hub-state
description: Validate Builder hub state for Markdown artifact conventions, canonical statuses, links, indexes, templates, and repo-scoped skills. Use after creating or updating hub records, specs, plans, spoke tasks, updates, reviews, decisions, closures, templates, or indexes.
---

# Validate Hub State

## Overview

Check that the hub remains navigable and consistent as artifacts accumulate.

## Checks

- Required directories and templates exist.
- Markdown artifact filenames use `YYYY-MM-DD-title.md`, except approved index/state files.
- Work statuses use the canonical status model.
- Quality-gated implementation plans and test reports satisfy required artifact structure.
- Markdown links to local docs resolve.
- Repo-scoped skills have valid frontmatter.
- Generated index files exist.

## Workflow

1. Run `update-hub-indexes` first when records changed.
2. Run the helper script.
3. Fix reported errors.
4. Save session memory and use `commit-push-builder-main` after fixes.

## Helper Script

```bash
python3 .agents/skills/validate-hub-state/scripts/validate_hub_state.py
```

The script exits non-zero when validation errors are found. Warnings are reported but do not fail the command.
