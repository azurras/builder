# Validate Mode

Run the shared validator against the supplied Markdown:

```powershell
python .agents/skills/write-implementation-plan/scripts/validate_implementation_plan.py docs/implementation-plans/YYYY-MM-DD-HH-MM-project-title.md
```

With no filename, the CLI reads stdin. The save and log helpers use the same validator and refuse invalid results before writing.

For `task-contract-v2` plans the validator checks that:

- Every section listed in [plan mode](plan.md#sections) is present and nonempty, and Document Status is a known status.
- Acceptance Criteria define sequential IDs from `AC-1`, and every ID appears in Test Plan.
- Each Implementation Log entry is titled `YYYY-MM-DD - Title` with a valid date and has nonempty Change, Reason and Impact lines.
- A complete plan's Outcome is not pending and mentions every AC ID.
- Each task has a complete contract or a valid legacy Code Edit block, task numbers are sequential, and ready, in-progress or complete plans contain no TBD, TODO or pending inspection.

Older formats keep their original checks: `task-contract-v1` plans validate each task and their original sections; unversioned literal-patch plans keep their whole-plan checks; named pre-schema plans are warnings only. Unknown formats fail.

Use review mode for semantic readiness: structural validation cannot prove that referenced files were inspected, that a non-goal's reason is sound, that tests can detect failure, or that the log records every divergence.
