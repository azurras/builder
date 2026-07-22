---
name: review-implementation-plan
description: Use when Codex needs to review a Builder implementation plan before execution, especially to reject vague tasks, missing line ranges, missing Code Edit blocks, weak testing, unowned tasks, or missing rollback and risk details.
---

# Review Implementation Plan

## Overview

Review implementation plans from an execution-readiness stance. The review should lead with blockers, not a summary.

## Review Contract

Reject the plan if any of these are true:

- Document status is `ready-for-execution` but any Code Edit has `line range pending file inspection`.
- A code-changing task lacks a `Code Edit` block.
- A `Code Edit` block lacks `File`, `Lines`, `Action`, `Current`, `Proposed`, or `Verification`.
- A code-changing task omits `Required skill: write-jane-street-style-code` or does not direct execution to invoke it before code edits; reject the plan until the constraint is explicit.
- A code-changing task omits a Before-Edit Brief with Behavior, Invariants, Boundary/API, Effects and failures, and Tests and evidence; reject the plan until each field contains task-specific content.
- Testing sections do not name concrete commands or checks.
- Local testing is missing for runtime behavior.
- Rollback/recovery, risks, or completion criteria are empty.
- Tasks are not ordered or do not state dependencies.

## Workflow

1. Run `validate-implementation-plan` first.
2. Read the plan for execution clarity beyond mechanical validation.
3. Check each Before-Edit Brief against the proposed code and verification, not merely for the field names.
4. Report findings ordered by severity with file/section references when possible.
5. If no blockers remain, say the plan is ready for execution and list residual risks.

## Output Shape

```markdown
## Blockers
- ...

## Warnings
- ...

## Ready State
ready | not ready
```
