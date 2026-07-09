# 2026-07-09 - Add test report and story issue loop skills

## 21:20 - Add test report and story issue loop skills

### Request
The user noticed that Builder lacked a skill for generating local app test reports. They wanted reports that document what item was tested, what data was sent, and what came back. They also wanted Builder to know the default delivery loop without being told every step: Story/Issue -> Spec -> Implementation -> Local Testing against the app -> Test report -> Close story/issue -> Save session memory. The user approved the design but clarified that test reports do not need to reference the spec or implementation plan.

### Project Context
`C:\Users\Christopher\Developer\builder` is the Builder AI workflow hub. Repo-scoped skills live under `.agents/skills/`. Durable artifacts are stored under `docs/`, indexed by `update-hub-indexes`, validated by `validate-hub-state`, and committed/pushed to `main` with `commit-push-builder-main`.

### Work Completed
Added a new repo-scoped skill at `C:\Users\Christopher\Developer\builder\.agents\skills\save-test-report\` with `SKILL.md`, `agents/openai.yaml`, and `scripts/save_test_report.py`. The skill saves dated Markdown reports under `docs/test-reports/` and requires sections for document status, story/issue, branch, app/environment, local run details, test cases, data sent, response received, pass/fail, evidence, and bugs/follow-ups.

Added a new orchestration skill at `C:\Users\Christopher\Developer\builder\.agents\skills\complete-story-issue\` with `SKILL.md` and `agents/openai.yaml`. It encodes the default loop from story/issue intake through spec, implementation plan, development, local app testing, test report, story/issue closure, and session memory. It instructs Codex to run the loop by default unless the user scopes the request to one phase.

Added `docs/templates/test-report.md`, generated `docs/test-reports/index.md`, updated `update-hub-indexes` to index `docs/test-reports`, updated `validate-hub-state` to require the test report directory/index/template, and updated `AGENTS.md` so the durable artifact directory and default story/issue loop are repo instructions.

Added `.agents/tests/test_test_report_workflow.py` covering the new `save_test_report.py` helper and the index/validation support for `docs/test-reports`.

### Decisions
Kept test reports independent from specs and implementation plans per the user's clarification. The `save-test-report` skill says spec and implementation-plan links are optional only when directly useful for traceability.

Created a separate orchestration skill instead of making every focused skill carry the whole loop. Existing skills remain focused on saving a specific artifact or doing a specific hub operation; `complete-story-issue` is responsible for chaining them.

### Validation
Ran `python .agents\tests\test_test_report_workflow.py` before implementation and confirmed it failed because the save helper and test report index support did not exist. After implementation, the focused test passed.

Ran `python -m unittest discover -s .agents\tests`, which passed with 6 tests. Ran `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py`, which passed. Ran `python -m py_compile .agents\skills\save-test-report\scripts\save_test_report.py .agents\skills\update-hub-indexes\scripts\update_hub_indexes.py .agents\skills\validate-hub-state\scripts\validate_hub_state.py .agents\tests\test_test_report_workflow.py`, which passed.

### Current State
The builder worktree contains the intended new skills, new test report template/index, updated hub scripts, updated AGENTS.md, and new test coverage. Index regeneration and final validation should run once more after this memory entry is saved.

### Follow-ups
The next time the user gives Codex a story or issue to complete, use `complete-story-issue` as the default workflow and save a test report after local app testing.
