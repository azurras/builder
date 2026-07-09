---
name: start-hub-work
description: Create a central Builder work ledger record before coordinating work across one or more spoke repositories. Use when starting a new initiative, cross-repo task, project, feature, bugfix, migration, or investigation from the hub.
---

# Start Hub Work

## Overview

Create one canonical work record that ties together specs, implementation plans, spoke repos, dispatched tasks, updates, reviews, decisions, and final closure.

## Storage Rules

- Store work records under `docs/work/`.
- Name files `YYYY-MM-DD-title.md`.
- Write Markdown only.
- Create one durable record per initiative.

## Work Record Content

Include the objective, status, owner/agent context, related specs/plans, spoke repos, dispatched tasks, current state, blockers, validation, and next steps.

## Workflow

1. Identify the work title and scope.
2. Link any existing specs or implementation plans.
3. List involved spoke repos or mark them as TBD.
4. Save the work ledger file, preferring the helper script.
5. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/start-hub-work/scripts/start_hub_work.py \
  --title "Work Title" \
  < work-record.md
```

The helper writes `docs/work/YYYY-MM-DD-title.md` and refuses to overwrite unless `--overwrite` is passed.
