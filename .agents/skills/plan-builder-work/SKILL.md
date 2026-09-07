---
name: plan-builder-work
description: Create or review an implementation plan containing requirements and design decisions, or validate an existing plan.
---

# Plan Builder Work

Default to a self-contained implementation plan: requirements, acceptance criteria, relevant design decisions/tradeoffs, inspected targets, ordered task contracts, verification and recovery. Requirements exploration and specifications belong in this plan; decisions and progress belong in project session memory. Do not create separate spec or decision files.

| Mode | Instructions |
| --- | --- |
| Plan | [Inspected task contracts and save command](references/plan.md) |
| Review | [Semantic readiness review](references/review.md) |
| Validate | [Structural validator](references/validation.md) |

Every code-changing task requires `write-jane-street-style-code` and a task-specific Before-Edit Brief. Reject the plan when targets, dependencies, acceptance criteria, authority, verification, or recovery remain unresolved for its proposed status. Exact line ranges and replacement code are optional for inspected contracts; preserve valid historical plan schemas.

Review and validate are read-only unless changes were requested. A planning-only request ends at its published plan; do not start implementation. Read existing content before intentional full replacement with `--overwrite`.

Implementation plan artifacts must be committed and pushed before moving to the next delivery phase through the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md). Link the plan from the project's existing session memory when recording progress or completion; do not create another per-request memory file.
