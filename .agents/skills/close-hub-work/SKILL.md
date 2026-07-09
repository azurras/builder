---
name: close-hub-work
description: Save a final closure record for Builder hub-and-spoke work. Use when a cross-repo initiative, spoke task set, feature, migration, investigation, or project is complete and the hub needs final status, links, validation, and residual follow-ups.
---

# Close Hub Work

## Overview

Close the loop on cross-repo work by writing a final hub-side completion record.

## Storage Rules

- Store closure records under `docs/work-closures/`.
- Name files `YYYY-MM-DD-title.md`.
- Write Markdown only.
- Link the central work record and all relevant spoke artifacts.

## Closure Content

Include final status, completed scope, spoke repos changed, commits/PRs, validation, decisions, known gaps, follow-ups, and where future agents should resume if needed.

## Workflow

1. Confirm related work records, updates, reviews, specs, and plans are current.
2. Verify spoke work is merged, pushed, intentionally parked, or clearly documented.
3. Save the closure record with the helper script.
4. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/close-hub-work/scripts/close_hub_work.py \
  --title "Closure Title" \
  < closure.md
```
