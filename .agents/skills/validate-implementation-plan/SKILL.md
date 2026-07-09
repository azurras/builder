---
name: validate-implementation-plan
description: Use when reviewing, saving, or preparing to execute a Builder implementation plan that must prove it has status, branch, ordered tasks, literal line-range code edit blocks, testing, risks, and completion criteria.
---

# Validate Implementation Plan

## Overview

Reject vague implementation plans before execution. A plan is only ready when it contains executable tasks with literal Code Edit blocks tied to files, line ranges, current code, proposed code, and task-level verification.

## Workflow

1. Read the implementation plan Markdown.
2. Run the helper script below.
3. Treat any reported error as a blocker for execution.
4. If the plan contains `line range pending file inspection`, keep the document status as `draft` or `blocked`.
5. Use `review-implementation-plan` when a human-readable review verdict is needed.

## Helper Script

```bash
python3 .agents/skills/validate-implementation-plan/scripts/validate_implementation_plan.py \
  docs/implementation-plans/YYYY-MM-DD-title.md
```

The script exits non-zero when required sections, task headings, Code Edit blocks, line ranges, current/proposed code, or verification details are missing.
