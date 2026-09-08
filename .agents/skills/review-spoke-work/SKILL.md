---
name: review-spoke-work
description: Review spoke repository changes and preserve authorized findings in the existing project session-memory document.
---

# Review Spoke Work

## Overview

Record review findings for spoke repo work in the hub so quality decisions and residual risks are preserved.

## Storage Rules

Append authorized review findings to `docs/session-memory/YYYY-MM-DD-project.md` for the date of the review through `save-session-memory`. Use the existing project slug and link the reviewed plan, commit/PR and runtime report. Do not create a separate review document. Review-only scope without persistence returns findings without writing or committing.

## Review Content

Lead with findings ordered by severity. Include reviewed repo, branch/commit/PR, scope reviewed, validation checked, house-style compliance against `write-jane-street-style-code`, risks, requested changes, and merge readiness.

Use the Blockers and Warnings definitions from `write-jane-street-style-code/references/testing-and-review.md`. A blocker prevents merge readiness. A warning records actionable design or maintenance cost without overstating correctness risk.

Use this finding format:

```markdown
[Blocker|Warning] Short outcome-focused title
Location: path and tight line range
Contract: violated behavior, invariant, boundary, effect/failure rule, or evidence requirement
Evidence: concrete path, counterexample, failing command, or missing proof
Required change: correction or evidence needed to resolve the finding
```

## Workflow

1. Inspect the spoke update or repo diff. When code changed, invoke `write-jane-street-style-code`, read its testing-and-review reference, and compare the diff with the final Before-Edit Brief.
2. Classify concrete findings as blockers or warnings and use the required finding format.
3. When persistence is requested or part of authorized delivery, append the findings with `save-session-memory --project <existing-project>` using the helper command in that skill.
4. Use the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md) for the review entry; do not add a second continuity artifact.
