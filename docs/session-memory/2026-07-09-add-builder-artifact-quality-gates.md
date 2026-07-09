# 2026-07-09 - Add Builder artifact quality gates

## 21:54 - Add Builder artifact quality gates

### Request
The user asked to address a set of Builder core skill weaknesses: implementation plans were too bare, missing goals, non-goals, open questions, unit/local testing, risk, status, target branch, task ordering, and literal code-change detail. They also wanted a test-report skill for local app testing evidence, a full story/issue development loop, closure support, and broader improvements to core skills so future agents do not need to be told every step.

### Project Context
This repository is the Builder AI workflow hub. Repo-scoped skills live under `.agents/skills/`, shared helper code lives under `.agents/lib/`, durable artifacts live under `docs/`, and substantive completed updates should refresh hub indexes, validate hub state, save session memory, then commit and push `main`.

### Work Completed
Added shared artifact helpers in `.agents/lib/artifact_io.py` and `.agents/lib/artifact_quality.py`. The quality helpers validate implementation plans for required sections, document status, ordered tasks, task-level Code Edit blocks, literal file/line/action/current/proposed/verification fields, fenced code blocks, and no pending line ranges once a plan is ready for execution or complete. They validate test reports for required status, scope, environment, tested items, data sent, response received, pass/fail, evidence, issues, and sign-off sections.

Added unit tests in `.agents/tests/test_artifact_quality.py` and `.agents/tests/test_artifact_io.py`, and updated `.agents/tests/test_test_report_workflow.py` fixtures to satisfy the stricter report format.

Updated save helpers for project specs, implementation plans, and test reports to share `.agents/lib/artifact_io.py`. Implementation plan and test report save scripts now run quality validation before writing, so malformed new artifacts fail fast.

Added new repo-scoped skills: `.agents/skills/validate-implementation-plan/`, `.agents/skills/validate-test-report/`, `.agents/skills/review-implementation-plan/`, and `.agents/skills/close-story-issue/`. These make plan review, report validation, and story closure explicit workflow steps.

Updated existing workflow skills: `.agents/skills/save-implementation-plan/SKILL.md`, `.agents/skills/save-test-report/SKILL.md`, `.agents/skills/save-project-spec/SKILL.md`, `.agents/skills/complete-story-issue/SKILL.md`, and `.agents/skills/validate-hub-state/SKILL.md`. The complete-story loop now requires story/issue -> spec -> implementation plan -> plan review -> implementation -> local app testing -> test report -> closure -> session memory. The implementation plan skill now requires literal Code Edit blocks inside tasks. The test report skill now requires request data and observed response data. The spec skill now includes document status.

Updated `.agents/skills/validate-hub-state/scripts/validate_hub_state.py` so hub validation quality-checks all test reports and quality-gated implementation plans. Existing legacy implementation plans that do not yet contain `#### Code Edit` blocks emit warnings rather than blocking the repo.

Updated `AGENTS.md` to direct agents to use implementation plan review before execution, avoid vague plans, and close story/issue work with the new closure skill. Updated `docs/status-model.md` with artifact statuses. Added examples under `docs/templates/examples/implementation-plan-example.md` and `docs/templates/examples/test-report-example.md`.

### Decisions
Future implementation plans are gated at save time instead of relying on the agent to remember the format. Legacy plans are warned rather than failed so this improvement does not require rewriting historical artifacts in the same change. The plan validator only permits pending file-inspection line ranges while a plan is draft or blocked; ready-for-execution and complete plans need concrete file and line evidence.

### Validation
Ran `python -m unittest discover -s .agents\tests`, which completed 12 tests successfully. Ran the implementation plan and test report validators against the new examples; both passed. Ran `python -m py_compile` across the shared libraries and touched scripts; it exited successfully. Ran `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py`; hub validation passed with warnings for older legacy implementation plans missing Code Edit blocks.

### Current State
The work is on `main` in `C:\Users\Christopher\Developer\builder`. No app server was started because this change is to Builder workflow skills and Markdown/Python helpers, not a web app. Hub indexes still need to be refreshed after this memory entry, followed by final validation and commit/push.

### Follow-ups
Consider adding a stricter project spec validator later if specs need the same enforcement level as implementation plans and test reports. Existing legacy implementation plans can be migrated opportunistically if they become active again.
