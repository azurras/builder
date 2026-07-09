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

Write implementation plans as execution artifacts, not broad specs or chat transcripts. Include enough concrete detail that an agent can execute the work without rediscovering scope, files, code shape, or verification expectations.

Every implementation plan should include:

- Document Status: the plan state, such as draft, ready for execution, in progress, blocked, or complete.
- Objective: the implementation outcome.
- Goals: concrete success outcomes or acceptance targets.
- Inputs: related specs, constraints, user decisions, and repository context.
- Branch: the branch name to work against or create, including the base branch when known.
- Non-Goals: work that is explicitly out of scope.
- Assumptions: facts the plan relies on.
- Open Questions: unresolved decisions, blockers, or unknowns; write "None" only after checking.
- Task Breakdown: ordered tasks that divide the work into executable units. Each task must include sequence/dependencies, expected files or modules, implementation notes, task-level verification, and one or more Code Edit blocks when code changes are planned.
- Code Edit blocks: literal edit instructions inside the relevant task. Each block must name the file path, current line range, action, current code for replace/delete, proposed code for add/replace, and task-level verification. Use real fenced code blocks, not prose summaries, when the code can be known from file inspection.
- Code Changes: an index of the task-level Code Edit blocks, grouped by file and action. Do not put the only code examples here; the literal code belongs in the task where it will be executed.
- Files or modules involved: expected code, docs, config, or test locations when a short file inventory helps scanning.
- Unit Testing: automated unit or narrow integration tests to add or update, including failing-test expectations when relevant.
- Local Testing: local commands, manual flows, smoke checks, service restarts, browser checks, or environment-specific verification.
- Validation: end-to-end acceptance criteria that combine automated and local checks when a separate summary is helpful.
- Rollback or recovery: how to undo or mitigate risky changes when relevant.
- Risks: technical, product, operational, sequencing, or external risks and mitigations.
- Completion criteria: what must be true before the work is considered done.

Prefer concrete tasks over vague intent. Keep enough detail that another agent can execute the plan without needing the original conversation. If the plan modifies existing code, inspect the file first and use exact line ranges. If a line range is genuinely not knowable yet, write `line range pending file inspection` and keep the document status as draft or blocked; do not mark the plan ready for execution.

## Task Code Edit Format

Use this format inside each task that changes code:

````markdown
### Task N - Short task title

Sequence / dependencies:
- Runs after Task N-1 because ...

Implementation notes:
- ...

#### Code Edit N.1
- File: `path/to/file.ext`
- Lines: 42-58
- Action: replace

Current:
```language
existing code from lines 42-58
```

Proposed:
```language
replacement code
```

Verification:
- `command that proves this task-level edit works`
````

For additions, use `Lines: after 58` or `Lines: before 42` and omit `Current:` only when no existing code is being replaced. For deletions, include `Current:` and write `Proposed: delete block`.

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

````markdown
# Title

## Document Status

## Objective

## Goals

## Inputs

## Branch

## Non-Goals

## Assumptions

## Open Questions

## Task Breakdown

### Task 1 - Short task title

Sequence / dependencies:

Implementation notes:

#### Code Edit 1.1
- File: `path/to/file.ext`
- Lines: line range pending file inspection
- Action: add | replace | delete | move

Current:
```text
existing code for replace/delete
```

Proposed:
```text
new code for add/replace, or delete block
```

Verification:

## Code Changes

## Files and Modules

## Unit Testing

## Local Testing

## Validation

## Rollback or Recovery

## Risks

## Completion Criteria
````
