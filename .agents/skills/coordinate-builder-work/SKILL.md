---
name: coordinate-builder-work
description: Maintain a Builder work ledger, prepare an actual spoke-agent handoff, record returned updates, or close a hub initiative.
---

# Coordinate Builder Work

Choose start, dispatch, update, or close. Use only records that help coordinate the actual work. Same-agent spoke work can use a work ledger and primary evidence links without invented delegation or returned-update artifacts.

| Mode | Record and contract |
| --- | --- |
| Start | `docs/work/`: objective, canonical status, owner, specs/plans, repositories, current state, blockers, validation, next steps. One ledger per initiative. |
| Dispatch | `docs/spoke-tasks/`: actual target agent/repo/path, branch policy, objective, strict scope, constraints, inspected targets, validation and return format. |
| Update | `docs/spoke-updates/`: returned provenance, status, changes, commit/PR links, evidence, blockers and next actions. Link an existing brief when available; do not invent one. |
| Close | `docs/work-closures/`: final status, delivered/parked scope, publication and evidence links, known gaps and next owner/action. Update the ledger status too. |

Use matching templates under `docs/templates/` and canonical statuses in `docs/status-model.md`. The work ledger holds current status; reports/reviews hold primary evidence; the closure links those facts instead of copying full narratives. Parked or blocked work is not complete. Hub closure does not itself authorize external issue closure; use `complete-builder-work` closure mode when needed.

For every code-changing dispatch, require `write-jane-street-style-code` before code changes and a Before-Edit Brief covering Behavior, Invariants, Boundary/API, Effects and failures, Tests and evidence. The recipient must inspect and revise it before editing, then return commits/PRs, validation, final brief, blockers and warnings. Check repository context with `manage-spoke-repositories`; registration alone does not authorize source mutations.

Read [commands](references/commands.md) for persistence. After writing the intended records, use the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md). Save one continuity record at substantive completion or an authorized handoff, not after every coordination substep.
