# 2026-07-04 - Create save project spec skill

## 18:40 - Create save project spec skill

### Request
The user asked to create a new skill for saving specs to `docs/specs`. Requirements: every project starts from the azurras repo, specs created for any work should be saved under `docs/specs`, spec filenames should use `YYYY-MM-DD-{title}.md`, and all spec files should be Markdown.

### Project Context
This repository is being built as an AI workflow hub. Existing repo-local skills are stored under `/Users/cbell/Developer/azurras/skills`. Session memory is now stored under `/Users/cbell/Developer/azurras/docs/session-memory` using the previously created `save-session-memory` skill.

### Work Completed
Created a new repo-local skill at `/Users/cbell/Developer/azurras/skills/save-project-spec`. The skill includes `/Users/cbell/Developer/azurras/skills/save-project-spec/SKILL.md`, `/Users/cbell/Developer/azurras/skills/save-project-spec/agents/openai.yaml`, and `/Users/cbell/Developer/azurras/skills/save-project-spec/scripts/save_project_spec.py`.

The skill instructions define `docs/specs/` as the default spec storage location, require filenames in the form `YYYY-MM-DD-title.md`, require Markdown output, and include guidance for durable spec content: purpose, background, goals, non-goals, requirements, proposed approach, involved files/modules, validation plan, and open questions.

The helper script `save_project_spec.py` reads a complete Markdown spec from stdin, creates `docs/specs/` as needed, slugifies the title, writes `YYYY-MM-DD-title.md`, and refuses to overwrite an existing matching spec unless `--overwrite` is passed. This keeps accidental replacement of specs from happening silently.

### Decisions
Named the skill `save-project-spec` to keep it action-oriented and specific to the azurras workflow. Added a helper script because path, date, slug, extension, and overwrite behavior should be deterministic across agents. Chose fail-closed duplicate handling for specs because specs are full planning documents and replacing one with a partial draft would be risky.

No actual repo spec file was created under `docs/specs` during this request because the user asked for the skill that saves specs, not for a specific project spec document.

### Validation
Tested the helper in `/private/tmp/save-project-spec-test` using date `2099-03-04` and title `Inbox & Routing Spec`. The first run created `/private/tmp/save-project-spec-test/docs/specs/2099-03-04-inbox-routing-spec.md`. A second run without `--overwrite` failed as intended with an existing-file message. A third run with `--overwrite` replaced the file, and the saved Markdown content was verified.

Ran `PYTHONPYCACHEPREFIX=/private/tmp/save-project-spec-pycache python3 -m py_compile skills/save-project-spec/scripts/save_project_spec.py`, which passed. Ran a standard-library equivalent of the skill frontmatter checks from `quick_validate.py`, which passed. Attempted the official `quick_validate.py`, but it still fails in this environment because `PyYAML` is not installed.

### Current State
The repo has untracked generated files under `skills/` and `docs/`, plus untracked `.DS_Store` files. No commit has been created. The new skill is repo-local only; it has not been installed or symlinked into global Codex skill discovery.

### Follow-ups
When an actual project spec is created, use `/Users/cbell/Developer/azurras/skills/save-project-spec/scripts/save_project_spec.py` or the `save-project-spec` skill instructions to save it under `/Users/cbell/Developer/azurras/docs/specs/YYYY-MM-DD-title.md`.
