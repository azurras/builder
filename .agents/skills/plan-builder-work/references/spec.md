# Spec Mode

Save `docs/specs/YYYY-MM-DD-title.md`. Include Document Status, purpose/background, goals/non-goals, requirements, approach and ownership, acceptance/validation plan, and open questions. Review for missing acceptance criteria, risky ambiguity, and weak validation; resolve blockers before ready-for-execution.

Pass complete Markdown through stdin to `python .agents/skills/save-project-spec/scripts/save_project_spec.py --root . --title 'Spec title'`. Use a reviewed draft file as stdin. `--overwrite` intentionally replaces the entire existing spec; read it first. Preserve local-date filenames and Markdown-only storage unless the user requests another format.

Run the [phase finalizer](../../maintain-builder-hub/references/phase-finalization.md). The project spec must be committed and pushed before moving to the next phase. A spec-only request stops at this checkpoint.
