# 2026-07-09 - Enforce artifact commit checkpoints

## 22:13 - Enforce artifact commit checkpoints

### Request
The user asked that every Builder skill which commits and pushes an artifact must enforce that the artifact is committed and pushed before moving to the next step in the development loop.

### Project Context
Builder uses repo-scoped skills under `.agents/skills/` and durable artifacts under `docs/`. The delivery loop is orchestrated by `complete-story-issue`, with focused save skills for specs, implementation plans, test reports, and session memory. Existing guidance said to commit/push after saves, but did not make each saved artifact a hard phase boundary.

### Work Completed
Added `.agents/tests/test_artifact_commit_checkpoints.py` to enforce the contract that the full delivery loop has artifact commit checkpoints and that each focused artifact-saving skill says saved artifacts must be committed and pushed before moving to the next step.

Updated `.agents/skills/complete-story-issue/SKILL.md` with an `Artifact Commit Checkpoints` section. The loop now says project specs, implementation plans, test reports, and session memory must each be committed and pushed before the loop continues to the next phase or final completion. The completion checklist and final loop-state template now include committed/pushed state per artifact phase.

Updated focused save skills to make the post-save commit/push rule mandatory instead of advisory: `.agents/skills/save-project-spec/SKILL.md`, `.agents/skills/save-implementation-plan/SKILL.md`, `.agents/skills/save-test-report/SKILL.md`, and `.agents/skills/save-session-memory/SKILL.md`. Each now states the saved artifact must be committed and pushed before moving to the next delivery-loop step.

Updated the corresponding `agents/openai.yaml` prompts for those skills and `complete-story-issue` so prompt-level guidance reinforces the same checkpoint behavior. Updated `AGENTS.md` to define Builder artifact saves as hard phase checkpoints in the completion workflow.

### Decisions
The checkpoint is expressed as a phase-boundary rule, not just a final checklist item, because the failure mode is batching artifacts and pushing later. This makes future agents stop after each artifact-producing skill and persist it before continuing.

### Validation
Added the contract test first and confirmed it failed against the previous skill wording. After updating the skills, `python .agents\tests\test_artifact_commit_checkpoints.py` passed. `python -m unittest discover -s .agents\tests` passed with 16 tests. `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py` passed with only existing legacy implementation-plan warnings.

### Current State
There are pre-existing untracked issue 1120 docs in the worktree that were not part of this request and should not be included in this commit. The intended commit scope is the checkpoint test, skill docs/prompts, AGENTS guidance, this session memory, and generated session-memory index.

### Follow-ups
If future artifact-save helpers grow dedicated scripts for commit/push checks, keep the same contract test or expand it so new artifact save skills cannot omit the phase-boundary language.
