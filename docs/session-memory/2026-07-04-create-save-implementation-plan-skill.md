# 2026-07-04 - Create save implementation plan skill

## 18:51 - Create save implementation plan skill

### Request
The user asked to create a new skill similar to the project spec skill, but for saving implementation plans.

### Project Context
This repository is being built as an AI workflow hub. Repo-local skills live under `/Users/cbell/Developer/azurras/skills`. Specs are saved by the existing `save-project-spec` skill under `docs/specs/YYYY-MM-DD-title.md`. Session memory is stored under `/Users/cbell/Developer/azurras/docs/session-memory` using the `save-session-memory` skill.

### Work Completed
Created a new repo-local skill at `/Users/cbell/Developer/azurras/skills/save-implementation-plan`. The skill includes `/Users/cbell/Developer/azurras/skills/save-implementation-plan/SKILL.md`, `/Users/cbell/Developer/azurras/skills/save-implementation-plan/agents/openai.yaml`, and `/Users/cbell/Developer/azurras/skills/save-implementation-plan/scripts/save_implementation_plan.py`.

The skill instructions define `docs/implementation-plans/` as the default storage location, require filenames in the form `YYYY-MM-DD-title.md`, require Markdown output, and include guidance for execution-focused plan content: objective, inputs, assumptions, ordered steps, files/modules involved, validation, rollback or recovery, risks/dependencies, and completion criteria.

The helper script `save_implementation_plan.py` reads a complete Markdown implementation plan from stdin, creates `docs/implementation-plans/` as needed, slugifies the title, writes `YYYY-MM-DD-title.md`, and refuses to overwrite an existing matching plan unless `--overwrite` is passed.

### Decisions
Named the skill `save-implementation-plan` to mirror `save-project-spec` while keeping its purpose distinct. Used `docs/implementation-plans` rather than `docs/specs` because implementation plans are execution artifacts, while specs are planning/requirements artifacts. Kept duplicate handling fail-closed, matching the spec skill, to avoid replacing a full plan with an incomplete draft by accident.

No actual implementation plan was created under `docs/implementation-plans` during this request because the user asked for the skill, not for a specific plan document.

### Validation
Tested the helper in `/private/tmp/save-implementation-plan-test` using date `2099-04-05` and title `Search Index Rollout Plan`. The first run created `/private/tmp/save-implementation-plan-test/docs/implementation-plans/2099-04-05-search-index-rollout-plan.md`. A second run without `--overwrite` failed as intended with an existing-file message. A third run with `--overwrite` replaced the file, and the saved Markdown content was verified.

Ran `PYTHONPYCACHEPREFIX=/private/tmp/save-implementation-plan-pycache python3 -m py_compile skills/save-implementation-plan/scripts/save_implementation_plan.py`, which passed. Ran a standard-library equivalent of the skill frontmatter checks from `quick_validate.py`, which passed. Attempted the official `quick_validate.py`, but it still fails in this environment because `PyYAML` is not installed.

### Current State
The repo has untracked generated files under `skills/` and `docs/`, plus untracked `.DS_Store` files. No commit has been created. The new skill is repo-local only; it has not been installed or symlinked into global Codex skill discovery.

### Follow-ups
When an actual implementation plan is created, use `/Users/cbell/Developer/azurras/skills/save-implementation-plan/scripts/save_implementation_plan.py` or the `save-implementation-plan` skill instructions to save it under `/Users/cbell/Developer/azurras/docs/implementation-plans/YYYY-MM-DD-title.md`.
