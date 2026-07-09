---
name: save-decision-record
description: Save durable Builder decision records as Markdown under docs/decisions with dated filenames. Use when recording architecture decisions, workflow choices, cross-repo coordination decisions, tradeoffs, accepted constraints, or why a path was chosen.
---

# Save Decision Record

## Overview

Save decisions separately from session memory so important reasoning remains easy to find.

## Storage Rules

- Store decision records under `docs/decisions/`.
- Name files `YYYY-MM-DD-title.md`.
- Write Markdown only.
- Refuse accidental overwrite unless the update is intentional.

## Decision Content

Include context, decision, options considered, consequences, status, related work records, and follow-ups.

## Workflow

1. Identify the decision title.
2. Write a durable Markdown decision record.
3. Save it with the helper script.
4. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/save-decision-record/scripts/save_decision_record.py \
  --title "Decision Title" \
  < decision.md
```
