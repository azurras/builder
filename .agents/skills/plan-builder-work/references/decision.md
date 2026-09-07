# Optional Decision Mode

Normally record decisions and reasons in the current spec, plan, or continuity artifact. Create a separate record only when requested or when an enduring cross-work decision needs its own reference. Use `docs/templates/decision-record.md`: context, decision, options, consequences, status, related work, and follow-ups.

Pass complete Markdown on stdin to `python .agents/skills/plan-builder-work/scripts/save_decision_record.py --root . --title 'Decision title'`. It creates `docs/decisions/` on demand and saves there and refuses duplicates without `--overwrite`. Finish the current artifact phase with the [phase finalizer](../../maintain-builder-hub/references/phase-finalization.md); no extra memory cycle is required.
