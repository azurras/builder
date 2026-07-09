# 2026-07-09 - Require literal code edit blocks in implementation plans

## 21:41 - Require literal code edit blocks in implementation plans

### Request
The user said the implementation plan skill still was not concrete enough. They wanted implementation plans to show literal code blocks in the tasks themselves, including statements like "I am changing this code on line x-x to this code." The user approved a design requiring task-level Code Edit blocks.

### Project Context
`C:\Users\Christopher\Developer\builder` is the Builder workflow hub. Repo-scoped skills live under `.agents/skills/`. The `save-implementation-plan` skill had already been expanded with status, branch, goals, task breakdown, code changes, testing, and risk sections, but still allowed prose summaries and pseudo-diffs instead of forcing exact task-level code edits.

### Work Completed
Updated `C:\Users\Christopher\Developer\builder\.agents\skills\save-implementation-plan\SKILL.md` so task breakdowns must include one or more `Code Edit` blocks when code changes are planned. Each block must name the file path, current line range, action, current code for replace/delete, proposed code for add/replace, and task-level verification.

Added a `Task Code Edit Format` section with a rendered Markdown template showing a task, sequence/dependencies, implementation notes, `Code Edit N.1`, `File`, `Lines`, `Action`, `Current`, `Proposed`, and `Verification`. Updated the minimal plan template so the `Task Breakdown` section includes a concrete `Code Edit 1.1` skeleton.

Updated `C:\Users\Christopher\Developer\builder\.agents\skills\save-implementation-plan\agents\openai.yaml` so the default prompt mentions literal line-range code edit blocks.

### Decisions
Made `Code Changes` an index of task-level edit blocks rather than the only place where code is shown. This keeps the actual current/proposed code attached to the task that executes it. Required exact line ranges after file inspection; if a line range is not knowable yet, the skill now requires `line range pending file inspection` and says the plan must remain draft or blocked, not ready for execution.

### Validation
Ran a red structure check before editing for `Code Edit`, `Current:`, `Proposed:`, `Lines:`, `Action:`, and `line range pending file inspection`; it failed as expected. After editing, reran the check including four-backtick Markdown fences, and it passed.

Ran `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed. Ran `python -m py_compile .agents\skills\save-implementation-plan\scripts\save_implementation_plan.py .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed.

### Current State
Before saving this memory entry, only `.agents/skills/save-implementation-plan/SKILL.md` and `.agents/skills/save-implementation-plan/agents/openai.yaml` were modified. Index regeneration and final validation should run before committing.

### Follow-ups
Future implementation plans should inspect target files before marking the plan ready and should show exact before/after code blocks inside each relevant task.
