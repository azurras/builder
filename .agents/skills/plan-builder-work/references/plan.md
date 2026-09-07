# Plan Mode

Save Markdown under `docs/implementation-plans/YYYY-MM-DD-title.md` at the active Builder root. Use the user's local date, a concise lowercase slug, and `--overwrite` only after reading an existing file and intentionally replacing its complete contents.

## Execution Contract

A plan names the work and the evidence needed to complete it. Exact line ranges and prewritten replacement code are optional. Prefer inspected files and stable symbols; use literal patches when they clarify a fragile edit. Reinspect targets before editing if the checkout has changed.

Include these document sections: Document Status, Objective, Goals, Inputs, Branch, Non-Goals, Assumptions, Open Questions, Task Breakdown, Code Changes, Files and Modules, Unit Testing, Local Testing, Validation, Rollback or Recovery, Risks, and Completion Criteria. Keep entries concise; explain when a section is not applicable.

For new plans, add `## Plan Format` with value `task-contract-v1`. Use sequential `### Task N - Title` headings. Every task needs its own task contract or a valid legacy Code Edit block. Every code-changing task must state `Required skill: write-jane-street-style-code` before code changes and include a task-specific Before-Edit Brief.

For the preferred task contract, use these labels with a nonempty value on the same line; bullets are optional:

- Dependencies: preceding tasks and why, or None.
- Files: inspected repository-relative paths; for new files name the intended path and inspected neighboring pattern.
- Symbols: functions, types, configuration keys, or document headings to change or add.
- Inspection: what was read and the relevant branch/commit or current checkout context. Planned targets alone are not inspection evidence.
- Behavior: observable outcome or behavior to preserve.
- Invariants: constraints that must remain true.
- Boundary/API: affected interfaces and compatibility requirements.
- Effects and failures: mutations, I/O, ownership, and expected failure handling.
- Tests and evidence: risk-appropriate starting and final evidence.
- Verification: concrete commands or observable acceptance checks for this task.

Behavior through Tests and evidence form the five-field Before-Edit Brief. Documentation-only tasks can name headings and documentation checks; they do not require application startup or implementation snippets.

Unversioned historical literal-patch plans retain their original whole-plan validation, including non-edit delivery tasks. New versioned plans validate each task independently. Legacy `#### Code Edit N.N` blocks remain supported: File, Lines, Action, Current for replace/delete/move, Proposed, fenced code, and Verification. Additions may omit Current. If literal line ranges are supplied, they must be valid; `line range pending file inspection` cannot appear in a ready or completed plan. Prefer converting a task to an inspected contract over maintaining stale line numbers.

## Workflow

1. Inspect repository instructions, relevant files, callers, and tests. Resolve material scope questions using existing authorization and context.
2. Draft the plan with a branch, concrete contracts, ordered dependencies, testing, recovery, and completion criteria. Use draft or blocked when inspection or execution prerequisites remain unresolved.
3. Run `plan-builder-work` review mode and correct blockers. Mechanical validation checks structure; it cannot prove that a symbol was inspected or that a proposed change is correct.
4. Save with the helper, which validates before writing. Use `plan-builder-work` validate mode to recheck saved plans. Do not mark ready-for-execution until validation and review pass.
5. Use the [phase finalizer](../../maintain-builder-hub/references/phase-finalization.md) with the exact saved plan and intended indexes. The implementation plan must be committed and pushed before moving to the next delivery-loop step.

## PowerShell Helper

Pass complete Markdown through stdin. For an existing draft file:

```powershell
Get-Content -Raw -LiteralPath $draftPath | python .agents/skills/plan-builder-work/scripts/save_implementation_plan.py --root . --title 'Implementation title'
```

Set `$draftPath` to the reviewed draft. The helper refuses accidental overwrite and exits nonzero on invalid plan structure. It retains `--date`, `--plan-dir`, and `--overwrite` for explicit requests.
