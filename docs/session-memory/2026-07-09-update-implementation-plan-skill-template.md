# 2026-07-09 - Update implementation plan skill template

## 20:56 - Update implementation plan skill template

### Request
The user noticed that the repo-scoped `save-implementation-plan` skill was too bare and specifically missing sections for non-goals, open questions, unit testing, local testing, and actual code being added/deleted. The user approved a narrow design to strengthen the skill instructions and template rather than add a content-linting helper.

### Project Context
`C:\Users\Christopher\Developer\builder` is the builder workflow hub. Repo-scoped skills live under `.agents/skills/`, and behavior changes should keep the skill instructions and `agents/openai.yaml` aligned. The implementation-plan helper script only writes Markdown files, so content guidance belongs in `SKILL.md` unless stricter validation is requested later.

### Work Completed
Updated `C:\Users\Christopher\Developer\builder\.agents\skills\save-implementation-plan\SKILL.md` so implementation plans now explicitly include `Non-Goals`, `Open Questions`, `Code Changes`, `Unit Testing`, and `Local Testing`. The new guidance asks for concrete code additions, modifications, deletions, snippets, pseudo-diffs, or exact symbols/files when full code is deferred.

Updated `C:\Users\Christopher\Developer\builder\.agents\skills\save-implementation-plan\agents\openai.yaml` so the skill listing describes complete implementation plans with scope, code-change, and testing details.

### Decisions
Kept `save_implementation_plan.py` unchanged because it is a deterministic file-writing utility. The requested behavior is about what future agents write in implementation plans, so the skill body and metadata are the right place for this pass. A future linter could be added if the hub needs hard enforcement for required headings.

### Validation
Ran a required-heading check before editing; it failed as expected with missing headings for `## Non-Goals`, `## Open Questions`, `## Code Changes`, `## Unit Testing`, and `## Local Testing`.

After editing, reran the same heading check and it passed. Ran `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed. Ran `python -m py_compile .agents\skills\save-implementation-plan\scripts\save_implementation_plan.py .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed.

### Current State
The worktree had only the intended skill and metadata changes before saving this memory entry. Index regeneration and final hub validation should run before committing.

### Follow-ups
Consider adding an optional implementation-plan content validator later if agents continue saving plans without the required headings.
