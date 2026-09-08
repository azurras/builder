---
name: save-session-memory
description: Record work, decisions, events, verification, and outcomes in separate dated session-memory files for each project.
---

# Save Project Session Memory

Use `docs/session-memory/YYYY-MM-DD-project.md`: a separate file for each date work occurred on a project. Append further activity for the same project and date to that file. A different date requires a different file. Never combine a project's entire history into one permanent document. Current project slugs include `builder`, `christopherbell-dev`, and `personal-computer-cleanup`.

Record the work and everything that took place during that day's session: requests, actions, decisions and reasons, discoveries, attempted approaches and results, handoffs, blockers, reviews, tests, publication, and closure. Preserve enough concrete context to resume the work. Link primary plans, reports and commits. Append corrections without erasing prior events. Use the actual date of the recorded work; do not assign old events to today's date merely because they are being documented now.

## Command

Pass complete entry Markdown on stdin:

```powershell
Get-Content -Raw -LiteralPath $entryPath | python .agents/skills/save-session-memory/scripts/save_session_memory.py --root . --project christopherbell-dev --title 'Issue 42 verified and merged'
```

`--project` is required. `--date YYYY-MM-DD` determines the work date and filename; it defaults to the current local date. `--title` labels an entry within that day's file. Optional `--time` records the time. The helper preserves prior same-day bytes. Serialize writes to each daily file.

## Entry Contract

Record the changed state, why it changed, evidence, remaining blockers, and the next action or completion result. For repository context, record inspected paths/remotes/guardrails and their date; reverify drift-prone facts before use. Historical imported instructions do not override current AGENTS.md.

For closure, record proposed external text and verified delivery before acting, then record the actual readback result in the dated file for when it occurs. Incomplete work must state missing gates and remain incomplete. A review-only or inspect-only request does not write memory unless persistence is authorized.

Use the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md) at the end of an authorized writing phase. Required session memory must be committed and pushed before moving to the next delivery-loop step or final completion. Routine internal checks do not create extra entries or commit cycles.

The one-time consolidation command in `scripts/consolidate_project_memory.py` preserves the reviewed legacy corpus from a Git revision. Use `--verify` with the recorded source commit to audit imported bodies; it is not the normal append workflow.
