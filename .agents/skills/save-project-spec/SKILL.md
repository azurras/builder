---
name: save-project-spec
description: Save project specifications as Markdown files under docs/specs with dated filenames. Use when Codex creates, drafts, updates, or preserves a project spec, requirements document, implementation plan, technical design, product brief, or work specification in the builder workflow hub.
---

# Save Project Spec

## Overview

Save project specs in a predictable place and filename format so work that starts from the builder repo keeps its planning artifacts together. Specs must be Markdown files under `docs/specs/`.

## Storage Rules

- Write specs under `docs/specs/` at the active builder repository root unless the user explicitly chooses another root.
- Name every spec file `YYYY-MM-DD-title.md`, where the date is the local date and `title` is a short slug derived from the spec title.
- Slug titles with lowercase ASCII words separated by hyphens. Remove punctuation and collapse repeated hyphens.
- Keep spec filenames short, descriptive, and stable enough to reference later.
- Write only Markdown files. Do not create `.txt`, `.docx`, `.pdf`, or companion metadata files for specs unless the user explicitly asks.
- If a matching dated title already exists, update that spec intentionally rather than creating a near-duplicate filename.

## Spec Content

Write specs as durable planning artifacts, not chat transcripts. Include sections that fit the work, usually:

- Purpose: what the work is trying to accomplish.
- Document Status: draft, ready-for-review, ready-for-execution, in-progress, blocked, complete, or superseded.
- Background: relevant repo, product, user, or system context.
- Goals and non-goals: boundaries for the work.
- Requirements: functional and non-functional requirements.
- Proposed approach: implementation, workflow, or design details.
- Files or modules involved: expected locations and ownership boundaries when known.
- Validation plan: tests, review steps, acceptance criteria, or manual checks.
- Open questions: decisions still needed before or during implementation.

Adjust sections to the project. Keep enough detail that another agent can implement from the spec without needing the original conversation.

## Workflow

1. Determine the active builder repo root before writing.
2. Draft the spec as Markdown with a clear H1 title.
3. Choose a concise title for the filename. Prefer the spec H1 or the user's project title.
4. Save the spec under `docs/specs/YYYY-MM-DD-title.md`, preferring the helper script below.
5. If the target file already exists, read it before replacing it. Use `--overwrite` only when the new content is intended to be the complete updated spec.
6. After the spec is saved, use `commit-push-builder-main` to commit and push the builder repo changes to `main`.
7. Mention the saved spec path and commit/push result in the response.

## Helper Script

Use `scripts/save_project_spec.py` to save a complete Markdown spec from stdin:

```bash
python3 /path/to/save-project-spec/scripts/save_project_spec.py \
  --root /path/to/builder \
  --title "Spec Title" \
  <<'SPEC'
# Spec Title

## Purpose
...
SPEC
```

The script creates `docs/specs/` when needed and writes `YYYY-MM-DD-spec-title.md`. It refuses to overwrite an existing spec unless `--overwrite` is provided. Use `--date YYYY-MM-DD` only when the user asks to save a spec for a specific date.

## Post-Save Git Rule

Every successful project spec save in the builder repo should be followed by `commit-push-builder-main`. Commit and push only this builder repo, and do not use that commit/push workflow for other repositories.

## Minimal Spec Template

```markdown
# Title

## Document Status

Draft.

## Purpose

## Background

## Goals

## Non-Goals

## Requirements

## Proposed Approach

## Validation Plan

## Open Questions
```
