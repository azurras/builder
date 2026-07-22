---
name: review-spoke-work
description: Save a review record for work completed in a spoke repository. Use when reviewing a spoke repo diff, branch, pull request, CI result, implementation, validation evidence, or readiness to merge while preserving the review in Builder.
---

# Review Spoke Work

## Overview

Record review findings for spoke repo work in the hub so quality decisions and residual risks are preserved.

## Storage Rules

- Store review records under `docs/spoke-reviews/`.
- Name files `YYYY-MM-DD-title.md`.
- Write Markdown only.
- Link related work records, task briefs, updates, commits, and PRs.

## Review Content

Lead with findings ordered by severity. Include reviewed repo, branch/commit/PR, scope reviewed, validation checked, house-style compliance against `write-jane-street-style-code`, risks, requested changes, and merge readiness.

## Workflow

1. Inspect the spoke update or repo diff. When code changed, invoke `write-jane-street-style-code` and evaluate the diff against its final review checklist.
2. Write findings-first Markdown review.
3. Save the review, preferring the helper script.
4. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/review-spoke-work/scripts/review_spoke_work.py \
  --title "Review Title" \
  < review.md
```
