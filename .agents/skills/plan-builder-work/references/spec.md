# Optional Spec Mode

Use a separate spec only for substantial requirements exploration, work spanning multiple implementation plans, or an explicit user request. Ordinary delivery starts directly with an implementation plan.

Save `docs/specs/YYYY-MM-DD-title.md`. Include Document Status, purpose/background, goals/non-goals, requirements, approach and ownership, acceptance/validation plan, and open questions. Review for missing acceptance criteria, risky ambiguity, and weak validation; resolve blockers before ready-for-execution.

Pass complete Markdown through stdin to `python .agents/skills/plan-builder-work/scripts/save_project_spec.py --root . --title 'Spec title'`. Use a reviewed draft file as stdin. `--overwrite` intentionally replaces the entire existing spec; read it first. Preserve local-date filenames and Markdown-only storage unless the user requests another format.

An optional spec can be saved and published with its implementation plan checkpoint. For a spec-only request, run the [phase finalizer](../../maintain-builder-hub/references/phase-finalization.md) and stop after publication; do not start planning or implementation unless requested.
