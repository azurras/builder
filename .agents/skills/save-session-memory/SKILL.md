---
name: save-session-memory
description: Append project progress, decisions, reviews, blockers, verification, and closure to one stable project session-memory document.
---

# Save Project Session Memory

Use one file per project: `docs/session-memory/<project>.md`. Choose the existing project slug by reading the index and relevant entries; do not infer it from the current task title or date. Current projects include `builder`, `christopherbell-dev`, and `personal-computer-cleanup`.

Append dated entries for substantive progress, handoffs, decisions, blockers, review findings, repository facts, publication, and closure. The latest applicable entry supersedes earlier status; do not rewrite the historical record. Keep entries concise and factual, with commit/PR links and links to the implementation plan and test report. Avoid repeating full evidence already in a report.

## Command

Pass complete entry Markdown on stdin:

```powershell
Get-Content -Raw -LiteralPath $entryPath | python .agents/skills/save-session-memory/scripts/save_session_memory.py --root . --project christopherbell-dev --title 'Issue 42 verified and merged'
```

`--project` is required and determines the stable filename. `--title` labels only this entry. Dates/times are recorded inside the file, with optional explicit `--date` and `--time`; different dates and tasks append to the same project. The helper preserves prior bytes. Serialize writes to a project file; do not run concurrent append operations.

## Entry Contract

Record the changed state, why it changed, evidence, remaining blockers, and the next action or completion result. For repository context, record inspected paths/remotes/guardrails and their date; reverify drift-prone facts before use. Historical imported instructions do not override current AGENTS.md.

For closure, record proposed external text and verified delivery before acting, then append the actual readback result to this same file. Incomplete work must state missing gates and remain incomplete. A review-only or inspect-only request does not write memory unless persistence is authorized.

Use the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md) at the end of an authorized writing phase. Required session memory must be committed and pushed before moving to the next delivery-loop step or final completion. Routine internal checks do not create extra entries or commit cycles.

The one-time consolidation command in `scripts/consolidate_project_memory.py` preserves the reviewed legacy corpus from a Git revision. Use `--verify` with the recorded source commit to audit imported bodies; it is not the normal append workflow.
