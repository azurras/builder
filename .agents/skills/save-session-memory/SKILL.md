---
name: save-session-memory
description: Save detailed dated Markdown memory updates after completing a user request. Use when a user asks Codex to preserve session memory, maintain project continuity notes, write project handoff context, or record what happened after finishing work so future agents can understand project scope, decisions, changed files, validation, and next steps.
---

# Save Session Memory

## Overview

Record a durable Markdown handoff entry after a completed request. The entry should let another agent understand what changed, why it changed, how it was verified, and what project context matters next.

## Storage Rules

- Write memory updates under `docs/session-memory/` at the active project or repository root unless the user specifies another location.
- Use Markdown files named with the local date plus a short description of the work: `docs/session-memory/YYYY-MM-DD-short-description-of-work.md`.
- Generate the short description from the completed request title unless the user provides a specific filename description.
- Slug filenames with lowercase ASCII words separated by hyphens. Remove punctuation, collapse repeated hyphens, and keep the description short enough to scan.
- If the file for the current date and short description already exists, append a new entry to that file.
- If no matching file exists for the current date and short description, create it with a top-level date-and-description heading.
- Date files and entries using the user's local date and timezone when known. If timezone is unknown, use the environment's local date.
- Do not overwrite or rewrite unrelated prior entries unless the user explicitly asks for cleanup.

## Entry Content

Write enough detail that a future agent can resume without reading the entire conversation. Include:

- Request: what the user asked for, including important constraints.
- Project context: repo purpose, relevant conventions, and assumptions discovered.
- Work completed: concrete changes, files created or modified, and important implementation details.
- Decisions: notable choices and the reasoning behind them.
- Validation: commands run, checks passed or failed, and any unverified areas.
- Current state: branch/worktree notes, generated artifacts, running services, and any dirty files that matter.
- Follow-ups: next steps, open questions, or risks that future agents should know.

Prefer factual detail over conversation transcript. Mention absolute paths for important local files when useful.

## Workflow

1. Confirm the request is complete enough to summarize. If work is blocked, write a blocked-state memory only when the user asks for handoff or the session is ending.
2. Inspect relevant final state if needed with `git status --short`, focused file reads, or test output summaries.
3. Draft a detailed Markdown entry using the content checklist above.
4. Append the entry to the matching `docs/session-memory/` file, preferring the helper script below.
5. After the memory file is saved, use `commit-push-builder-main` to commit and push the builder repo changes to `main`.
6. Briefly mention the memory file path and commit/push result in the final response if the memory update was part of the user's request.

## Helper Script

Use `scripts/save_session_memory.py` to create or append the dated work-description file:

```bash
python3 /path/to/save-session-memory/scripts/save_session_memory.py \
  --root /path/to/project \
  --title "Short completed request title" \
  <<'MEMORY'
### Request
...

### Work Completed
...
MEMORY
```

The script creates `docs/session-memory/YYYY-MM-DD-short-completed-request-title.md` when missing and appends a timestamped entry when it already exists. Use `--date YYYY-MM-DD` only when the user asks to record memory for a specific date. Use `--file-description "different short description"` only when the filename should differ from the entry title.

## Post-Save Git Rule

Every successful session memory save in the builder repo should be followed by `commit-push-builder-main`. Commit and push only this builder repo, and do not use that commit/push workflow for other repositories.

## Entry Template

```markdown
## HH:MM - Title

### Request
Summarize the user's request and constraints.

### Project Context
Record repository purpose, conventions, architecture, and assumptions that mattered.

### Work Completed
List files and behavior changed with enough detail to orient a future agent.

### Decisions
Explain meaningful implementation or process choices.

### Validation
List checks run and their outcomes. Note anything not run.

### Follow-ups
Capture next steps, risks, and open questions.
```

Adjust section names when another structure is clearer, but keep the entry detailed and scannable.
