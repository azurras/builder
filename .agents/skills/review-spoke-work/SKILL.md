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

Use the Blockers and Warnings definitions from `write-jane-street-style-code/references/testing-and-review.md`. A blocker prevents merge readiness. A warning records actionable design or maintenance cost without overstating correctness risk.

Use this finding format:

```markdown
[Blocker|Warning] Short outcome-focused title
Location: path and tight line range
Contract: violated behavior, invariant, boundary, effect/failure rule, or evidence requirement
Evidence: concrete path, counterexample, failing command, or missing proof
Required change: smallest correction or evidence needed
```

## Workflow

1. Inspect the spoke update or repo diff. When code changed, invoke `write-jane-street-style-code`, read its testing-and-review reference, and compare the diff with the final Before-Edit Brief.
2. Classify concrete findings as blockers or warnings and use the required finding format.
3. Save the review, preferring the helper script.
4. Save session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/review-spoke-work/scripts/review_spoke_work.py \
  --title "Review Title" \
  < review.md
```
