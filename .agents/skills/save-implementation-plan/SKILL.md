---
name: save-implementation-plan
description: Save implementation plans as Markdown files under docs/implementation-plans with dated filenames. Use when Codex creates, drafts, updates, or preserves an implementation plan, execution plan, engineering task breakdown, rollout plan, migration plan, or step-by-step build plan in the builder workflow hub.
---

# Save Implementation Plan

## Overview

Save implementation plans in a predictable place and filename format so execution details for builder projects are easy to find. Implementation plans must be Markdown files under `docs/implementation-plans/`.

## Storage Rules

- Write implementation plans under `docs/implementation-plans/` at the active builder repository root unless the user explicitly chooses another root.
- Name every implementation plan file `YYYY-MM-DD-title.md`, where the date is the local date and `title` is a short slug derived from the plan title.
- Slug titles with lowercase ASCII words separated by hyphens. Remove punctuation and collapse repeated hyphens.
- Keep filenames short, descriptive, and stable enough to reference from memory notes, specs, tasks, or PRs.
- Write only Markdown files. Do not create `.txt`, `.docx`, `.pdf`, or companion metadata files for implementation plans unless the user explicitly asks.
- If a matching dated title already exists, update that plan intentionally rather than creating a near-duplicate filename.

## Plan Content

Write implementation plans as execution artifacts, not broad specs or chat transcripts. Include sections that fit the work, usually:

- Objective: the implementation outcome.
- Inputs: related specs, constraints, user decisions, and repository context.
- Assumptions: facts the plan relies on.
- Phases or steps: ordered work units with clear completion criteria.
- Files or modules involved: expected code, docs, config, or test locations.
- Validation: commands, test cases, manual checks, and acceptance criteria.
- Rollback or recovery: how to undo or mitigate risky changes when relevant.
- Risks and dependencies: sequencing constraints, unknowns, or external blockers.
- Completion criteria: what must be true before the work is considered done.

Prefer concrete steps over vague intent. Keep enough detail that another agent can execute the plan without needing the original conversation.

## Workflow

1. Determine the active builder repo root before writing.
2. Draft the implementation plan as Markdown with a clear H1 title.
3. Choose a concise title for the filename. Prefer the plan H1 or the user's project title.
4. Save the plan under `docs/implementation-plans/YYYY-MM-DD-title.md`, preferring the helper script below.
5. If the target file already exists, read it before replacing it. Use `--overwrite` only when the new content is intended to be the complete updated plan.
6. After the implementation plan is saved, use `commit-push-builder-main` to commit and push the builder repo changes to `main`.
7. Mention the saved implementation plan path and commit/push result in the response.

## Helper Script

Use `scripts/save_implementation_plan.py` to save a complete Markdown implementation plan from stdin:

```bash
python3 /path/to/save-implementation-plan/scripts/save_implementation_plan.py \
  --root /path/to/builder \
  --title "Plan Title" \
  <<'PLAN'
# Plan Title

## Objective
...
PLAN
```

The script creates `docs/implementation-plans/` when needed and writes `YYYY-MM-DD-plan-title.md`. It refuses to overwrite an existing plan unless `--overwrite` is provided. Use `--date YYYY-MM-DD` only when the user asks to save a plan for a specific date.

## Post-Save Git Rule

Every successful implementation plan save in the builder repo should be followed by `commit-push-builder-main`. Commit and push only this builder repo, and do not use that commit/push workflow for other repositories.

## Minimal Plan Template

```markdown
# Title

## Objective

## Inputs

## Assumptions

## Steps

## Files and Modules

## Validation

## Risks and Dependencies

## Completion Criteria
```
