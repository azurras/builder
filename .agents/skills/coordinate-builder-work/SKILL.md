---
name: coordinate-builder-work
description: Coordinate project work and actual agent handoffs, recording progress and closure in the project session-memory document.
---

# Coordinate Builder Work

Read the implementation plan and the project's latest relevant dated session records. Record work intake, actual dispatch briefs, returned updates, blockers, decisions, and completion in `YYYY-MM-DD-project.md` for the date each occurred. Do not create separate work, spoke-task, update, or closure artifacts, or invent delegation for same-agent work.

For start/update entries, record objective, status, owner, repository, plan link, evidence, blockers, and next action. Use plain statuses such as active, blocked, complete, or cancelled; historical statuses are evidence of their time.

For actual handoffs, include target repo/path and branch policy, objective, scope, constraints, inspected targets, verification, and return format. Every code-changing dispatch requires `write-jane-street-style-code` before code changes and a Before-Edit Brief covering Behavior, Invariants, Boundary/API, Effects and failures, and Tests and evidence. The recipient inspects and revises the brief before edits, then returns commits/PRs, results, blockers and warnings.

Record returned updates with their provenance and links. Record completion with final publication, applicable verification, unresolved gaps and next ownership. Blocked or parked work is not complete. External issue closure still uses `complete-builder-work` and verified readback.

Persist with `save-session-memory` using the existing `--project` slug and actual work `--date`. Same-day updates append to that day's document; a different date gets a separate file. Use the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md) once at the authorized phase boundary, without a second memory record summarizing the first.
