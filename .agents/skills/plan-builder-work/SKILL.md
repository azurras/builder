---
name: plan-builder-work
description: Create or review a Builder implementation plan, validate an existing plan, or save an optional spec or decision record.
---

# Plan Builder Work

Default to plan mode for delivery work, with requirements, acceptance criteria, and relevant design decisions in the plan. A separate spec is optional: use one for substantial requirements exploration, work spanning multiple implementation plans, or an explicit user request. Select only the requested mode. Spec-only work ends after its published checkpoint. Review and validate modes are read-only: return findings/readiness without rewriting artifacts, saving memory, committing, or starting implementation unless requested.

| Mode | Instructions |
| --- | --- |
| Plan | [Inspected task contracts and save command](references/plan.md) |
| Optional spec | [Spec content and save command](references/spec.md) |
| Review | [Semantic readiness review](references/review.md) |
| Validate | [Structural validator](references/validation.md) |
| Decision | [Optional durable decision](references/decision.md) |

Every code-changing task requires `write-jane-street-style-code` and a task-specific Before-Edit Brief. Reject the plan when its targets, dependencies, authority, verification, or recovery remain unresolved for the proposed ready state. Mechanical validation cannot establish semantic readiness. Exact line ranges and prewritten code are optional for inspected contracts; preserve valid historical literal-edit plans.

Save Markdown using the local date and a stable title. Read existing content before intentional replacement with `--overwrite`. Implementation plan artifacts must be committed and pushed before moving to the next delivery phase through the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md). An optional spec can be included in the plan checkpoint; a spec-only request publishes just that artifact. Do not add a new session-memory artifact at every internal review or validation step.
