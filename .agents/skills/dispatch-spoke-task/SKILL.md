---
name: dispatch-spoke-task
description: Create a precise task brief for an agent working in a spoke repository while keeping the controlling state in Builder. Use when assigning implementation, investigation, review, migration, or validation work to another repo.
---

# Dispatch Spoke Task

## Overview

Write the handoff brief that tells a spoke agent exactly what to do in another repo and how to report back to the Builder hub.

## Storage Rules

- Store task briefs under `docs/spoke-tasks/`.
- Name files `YYYY-MM-DD-title.md`.
- Write Markdown only.
- Link the central `docs/work/` record when one exists.

## Task Brief Content

Include target repo, local path, branch policy, objective, strict scope, files likely involved, constraints, validation, expected output, and required return format. For every implementation or code-changing brief, include `Required skill: write-jane-street-style-code` and direct the spoke agent to invoke it before code changes.

## Workflow

1. Confirm the spoke repo is registered or record why it is not yet registered.
2. Draft a task brief that can be pasted directly to another agent. When code may change, include `Required skill: write-jane-street-style-code` before the implementation instructions.
3. Include instructions for the spoke agent to invoke the required skill before code changes and return commit/PR/status/test details plus house-style validation.
4. Save the task brief, preferring the helper script.
5. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/dispatch-spoke-task/scripts/dispatch_spoke_task.py \
  --title "Task Title" \
  < task-brief.md
```
