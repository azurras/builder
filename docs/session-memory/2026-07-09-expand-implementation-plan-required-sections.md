# 2026-07-09 - Expand implementation plan required sections

## 21:11 - Expand implementation plan required sections

### Request
The user approved a follow-up update to the repo-scoped `save-implementation-plan` skill because implementation plans also need a goals section, a section that divides each item into ordered tasks, a risks section, document status, and the branch name the work will use.

### Project Context
`C:\Users\Christopher\Developer\builder` is the builder workflow hub. Repo-scoped skills live under `.agents/skills/`, and skill behavior changes should keep `SKILL.md` and `agents/openai.yaml` aligned. This was a continuation of the implementation-plan template hardening work from the prior commit.

### Work Completed
Updated `C:\Users\Christopher\Developer\builder\.agents\skills\save-implementation-plan\SKILL.md` so implementation plans now explicitly require `Document Status`, `Goals`, `Branch`, `Task Breakdown`, and `Risks` in addition to the previously added non-goals, open questions, code changes, unit testing, and local testing sections.

Changed the guidance from phase/step language to task-oriented execution guidance. `Task Breakdown` now requires ordered executable units with sequence/dependencies, expected files or modules, implementation notes, and task-level verification.

Updated `C:\Users\Christopher\Developer\builder\.agents\skills\save-implementation-plan\agents\openai.yaml` so the default prompt names status, branch, goals, ordered tasks, code changes, risks, and testing details.

### Decisions
Kept `Objective` as a separate one-sentence implementation outcome and added `Goals` for concrete success outcomes or acceptance targets. Replaced the exact template heading `Risks and Dependencies` with `Risks` because the user asked for a risks section; dependency/sequencing risk details are now part of the risks guidance and task breakdown.

### Validation
Ran a required-heading check before editing for `## Document Status`, `## Branch`, `## Goals`, `## Task Breakdown`, and `## Risks`; it failed as expected because the current template did not contain the new exact headings.

After editing, reran the heading check with exact Markdown heading matching and it passed. Ran `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed. Ran `python -m py_compile .agents\skills\save-implementation-plan\scripts\save_implementation_plan.py .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed.

### Current State
Before saving this memory entry, the worktree contained only the intended `save-implementation-plan` skill and metadata changes. Index regeneration and final hub validation should run before committing.

### Follow-ups
If future implementation plans still drift, add an optional content validator that checks for the required headings before saving.
