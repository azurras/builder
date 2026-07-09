---
name: update-hub-indexes
description: Generate and refresh Builder hub Markdown index files from docs artifacts. Use when work records, spoke registries, decisions, specs, implementation plans, task briefs, updates, reviews, closures, or session memory change and the hub needs current index pages or docs/active.md.
---

# Update Hub Indexes

## Overview

Regenerate navigational Markdown indexes so the hub can answer what exists and what is active without scanning every artifact manually.

## Generated Files

- `docs/active.md`
- `docs/work/index.md`
- `docs/spokes/index.md`
- `docs/decisions/index.md`
- `docs/specs/index.md`
- `docs/implementation-plans/index.md`
- `docs/test-reports/index.md`
- `docs/spoke-tasks/index.md`
- `docs/spoke-updates/index.md`
- `docs/spoke-reviews/index.md`
- `docs/work-closures/index.md`
- `docs/session-memory/index.md`

## Workflow

1. Run the helper script from the Builder root.
2. Review generated index changes.
3. Run `validate-hub-state`.
4. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/update-hub-indexes/scripts/update_hub_indexes.py
```

Use `--check` to report stale indexes without rewriting files.
