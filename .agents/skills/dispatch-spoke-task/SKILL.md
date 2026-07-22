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

Include target repo, local path, branch policy, objective, strict scope, files likely involved, constraints, validation, expected output, and required return format. For every implementation or code-changing brief, include `Required skill: write-jane-street-style-code`, direct the spoke agent to invoke it before code changes, and require a Before-Edit Brief with Behavior, Invariants, Boundary/API, Effects and failures, and Tests and evidence.

## Workflow

1. Confirm the spoke repo is registered or record why it is not yet registered.
2. Draft a task brief that can be pasted directly to another agent. When code may change, place `Required skill: write-jane-street-style-code` and the five-field Before-Edit Brief before the implementation instructions.
3. Require the spoke agent to complete or revise the Before-Edit Brief after read-only investigation and before code changes.
4. Include instructions for the spoke agent to return commit/PR/status/test details, the final brief, and blocker/warning house-style review results.
5. Save the task brief, preferring the helper script.
6. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/dispatch-spoke-task/scripts/dispatch_spoke_task.py \
  --title "Task Title" \
  < task-brief.md
```
