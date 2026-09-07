# Validate Mode

Run the shared validator against the supplied Markdown. It accepts inspected file/symbol task contracts without requiring line ranges or replacement code, and retains support for legacy Code Edit blocks.

```powershell
python .agents/skills/plan-builder-work/scripts/validate_implementation_plan.py docs/implementation-plans/YYYY-MM-DD-title.md
```

With no filename, the CLI reads stdin. The save helper uses the same validator and refuses invalid artifacts before writing.

New plans use `## Plan Format` with value `task-contract-v1`; each task must independently satisfy a supported format. Unversioned historical literal-patch plans retain their former whole-plan checks so existing non-edit delivery tasks remain compatible. Unversioned plans without literal edits use the new contract checks. Contract fields and required document sections must be nonempty; task numbers must be sequential. An empty/invalid status fails. Unresolved task prerequisites such as pending inspection cannot appear in ready-for-execution, in-progress, or complete contracts. Legacy blocks retain their field and line-range checks.

Use `plan-builder-work` review mode for semantic readiness: structural validation cannot prove that referenced files were inspected, that commands cover the risks, or that scope and authority are correct. Draft plans may record unresolved inspection explicitly; they are not permission to start dependent implementation.
