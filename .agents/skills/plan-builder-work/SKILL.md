---
name: plan-builder-work
description: Create or save a Builder spec or implementation plan, review or validate an existing plan, or preserve a separately requested decision record.
---

# Plan Builder Work

Select only the requested mode. Spec-only work ends after its published checkpoint. Review and validate modes are read-only: return findings/readiness without rewriting artifacts, saving memory, committing, or starting implementation unless requested.

| Mode | Instructions |
| --- | --- |
| Spec | [Spec content and save command](references/spec.md) |
| Plan | [Inspected task contracts and save command](references/plan.md) |
| Review | [Semantic readiness review](references/review.md) |
| Validate | [Structural validator](references/validation.md) |
| Decision | [Optional durable decision](references/decision.md) |

Every code-changing task requires `write-jane-street-style-code` and a task-specific Before-Edit Brief. Reject the plan when its targets, dependencies, authority, verification, or recovery remain unresolved for the proposed ready state. Mechanical validation cannot establish semantic readiness. Exact line ranges and prewritten code are optional for inspected contracts; preserve valid historical literal-edit plans.

Save Markdown using the local date and a stable title. Read existing content before intentional replacement with `--overwrite`. Spec and plan artifacts must be committed and pushed before moving to the next delivery phase through the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md). Do not add a new session-memory artifact at every internal review or validation step.
