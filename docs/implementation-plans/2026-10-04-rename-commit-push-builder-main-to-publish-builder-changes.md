# Rename Commit Push Builder Main to Publish Builder Changes

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
The Builder publication skill is named `publish-builder-changes`. The new name describes what it does: persist a phase of Builder work and keep the hub valid. Its SKILL.md holds only guidance that its helper does not already enforce.

## Background
The user asked for a better name for `commit-push-builder-main` and whether the skill is useful. Review found that it is useful. Its hub check regenerates the indexes and validates the hub, and three skills reach it through the phase finalizer. Its commit helper limits staging to the files you name and supports push-only recovery. The name describes only the git mechanics, which hides the hub-check role it gained when maintain-builder-hub was retired. AGENTS.md already calls these checkpoints "publish", and the other skills use a verb-object name. The user chose `publish-builder-changes` in chat on 2026-10-04.

## Goals
- Every maintained file uses the skill name `publish-builder-changes`, and the old name no longer works (AC-1, AC-2).
- Helper behavior and CLI arguments stay exactly the same (AC-3).
- SKILL.md is shorter and says only what the helper does not enforce (AC-4).
- The change is published on Builder main (AC-5).

## Non-Goals
- No compatibility alias or stub folder for the old name. The precedent renames kept none, and a folder without SKILL.md fails skill discovery.
- No changes to helper logic, validation rules, index format or checkpoint timing. This is a rename and a documentation trim.
- No renames inside dated plans, reports or session memory. They are historical records under AGENTS.md. The only exception is retargeting one link that the validator would otherwise report as broken.
- No merging of this skill into complete-builder-work. Three other skills call the finalizer on its own.

## Acceptance Criteria
- AC-1: `.agents/skills/publish-builder-changes/` contains SKILL.md (`name: publish-builder-changes`), agents/openai.yaml, references/phase-finalization.md and the scripts. The helper file is `publish_builder_changes.py`. `.agents/skills/commit-push-builder-main/` no longer exists.
- AC-2: A search of tracked files outside dated docs finds neither `commit-push-builder-main` nor `commit_push_builder_main`. Skill discovery lists exactly seven skills, including publish-builder-changes.
- AC-3: The renamed test module passes, and so does the full native suite. `check_hub.py check` and `refresh` succeed from the new path.
- AC-4: SKILL.md is shorter than the current 47 lines. It keeps the operation selection, the outgoing-commit and staged-ownership responsibilities, push-failure recovery, the hub check and the checkpoint triggers. It drops restated helper validation.
- AC-5: The plan, the change and the dated delivery memory are on origin/main, confirmed by remote readback.

## Inputs
- User request in chat on 2026-10-04: "do it and name it: publish-builder-changes".
- Inspected on Builder `main` at `0772c38`, clean tree: the skill's SKILL.md, agents/openai.yaml, references/phase-finalization.md and scripts (four files); AGENTS.md; README.md; save-session-memory, write-implementation-plan (SKILL.md, references/plan.md, references/update.md) and write-test-report SKILL.md files; .agents/tests/test_commit_push_builder_main.py, test_skill_consolidation.py, test_artifact_quality.py and test_test_report_workflow.py; the retire-maintain-builder-hub and rename-planning-skill plans; a `git grep` for both identifiers.

## Branch
Builder primary checkout `main` at `0772c38`; publish the exact task files through the Builder helper.

## Assumptions
- The scripts stay at the same depth, so their `parents[3]` import of `.agents/lib` still works.
- `.claude/skills` is a symlink to the folder, so Claude Code picks up the new name without other changes.

## Open Questions
None. The user chose the name and authorized the work.

## Design
Use `git mv` to move the skill folder, the helper script and its test module, then update every maintained reference. Retarget the one link in `docs/session-memory/2026-09-06-builder.md` that points into the old folder, as the retire plan did, and leave its text unchanged. Rewrite SKILL.md around decisions the agent has to make itself: which operation to use, the files it owns, outgoing commits and failure recovery. The helper already enforces dry-run, path rejection and staged-file refusal, so SKILL.md states those once instead of restating them.

Alternatives considered:
- Keep an alias folder: rejected because discovery requires SKILL.md and an alias would show up as a duplicate skill.
- Keep the script filename `commit_push_builder_main.py`: rejected because the folder and helper should share one name, as they did before.

## Expected Changes
- `.agents/skills/commit-push-builder-main/` â†’ `.agents/skills/publish-builder-changes/`, including the helper renamed to `publish_builder_changes.py` and a new argparse description.
- SKILL.md: new name and title, trimmed body. agents/openai.yaml: display name, short description and `$publish-builder-changes`.
- references/phase-finalization.md: new script path and skill name.
- Links in save-session-memory/SKILL.md, write-implementation-plan/SKILL.md, references/plan.md, references/update.md and write-test-report/SKILL.md.
- AGENTS.md checkpoint sentence; README.md skill table and symlink sentence.
- Tests: `test_commit_push_builder_main.py` â†’ `test_publish_builder_changes.py`, renaming its constants and the first class. Path updates in test_skill_consolidation.py, test_artifact_quality.py and test_test_report_workflow.py.
- `docs/session-memory/2026-09-06-builder.md`: one link target.
- This plan, today's Builder session memory and regenerated indexes.

## Task Breakdown

### Task 1 - Rename the skill and update references
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: .agents/skills/commit-push-builder-main/ (all files); .agents/skills/save-session-memory/SKILL.md; .agents/skills/write-implementation-plan/SKILL.md, references/plan.md, references/update.md; .agents/skills/write-test-report/SKILL.md; AGENTS.md; README.md; .agents/tests/test_commit_push_builder_main.py, test_skill_consolidation.py, test_artifact_quality.py, test_test_report_workflow.py; docs/session-memory/2026-09-06-builder.md.
Symbols: SKILL.md frontmatter `name` and title; openai.yaml `interface`; helper argparse description; test `SCRIPT`, module spec name and `CommitPushBuilderMainTests`; SkillDiscoveryTests expected set; script path constants; README skill table row.
Inspection: Read every listed file on main `0772c38`. `git grep` found no other maintained references.
Behavior: The helper and check_hub run from the new path with the same arguments and results. Discovery lists publish-builder-changes.
Invariants: Seven skills, each with SKILL.md and openai.yaml; helper logic unchanged; dated history text unchanged apart from one link target.
Boundary/API: The skill name and helper path change together, with no alias. CLI arguments are unchanged.
Effects and failures: `git mv` keeps the history. A missed reference fails discovery, link validation or the identifier search.
Tests and evidence: Renamed and updated native tests; full suite; identifier search.
Verification: python -B -m unittest discover -s .agents/tests; git grep for both old identifiers excluding dated docs; check_hub.py check; git diff --check.

### Task 2 - Trim SKILL.md
Dependencies: Task 1.
Files: .agents/skills/publish-builder-changes/SKILL.md
Symbols: Headings: Select the Operation, Workflow, PowerShell Examples, Hub Check, Checkpoints.
Inspection: Compared each workflow step with the guards in the helper: root, branch, origin and worktree checks, literal-path rejection, refusing unrelated staged files, dry-run without side effects.
Behavior: An agent can still choose commit or push-only, review outgoing commits, recover from a failed push and run the hub check.
Invariants: Fewer than 47 lines; links resolve; every command in the doc names an existing script.
Boundary/API: Documentation only.
Effects and failures: None at runtime. Discovery tests check links and commands.
Tests and evidence: SkillDiscoveryTests; line count.
Verification: python -B -m unittest discover -s .agents/tests; check_hub.py check.

### Task 3 - Record and publish verified delivery
Dependencies: Tasks 1 and 2 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day Builder memory and the phase finalizer.
Behavior: The completed change and its dated evidence are on origin/main.
Invariants: Only the selected files are committed; earlier history is preserved.
Boundary/API: The renamed publication helper.
Effects and failures: Scoped commit and push. A failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run, then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Runtime verification does not apply. Builder holds workflow instructions and standalone Python helpers, not a runnable application. The native checks below replace it.
- AC-1: `git ls-files .agents/skills/publish-builder-changes`; confirm the old folder is absent; SkillDiscoveryTests.
- AC-2: `git grep -n "commit-push-builder-main\|commit_push_builder_main"` excluding dated docs returns nothing; SkillDiscoveryTests checks the set of seven.
- AC-3: `python -B -m unittest discover -s .agents/tests`; `check_hub.py refresh --root .` then review the diff; a helper `--dry-run` from the new path during publication.
- AC-4: Line count of SKILL.md below 47; review against the retained-content list; discovery link and command checks.
- AC-5: Helper output and `git ls-remote origin refs/heads/main` compared with the local HEAD.

## Rollback or Recovery
Revert the task commit to restore the old folder and references together. If a push fails, keep the commit and recover with `--push-only` from the path the commit contains.

## Risks
- A missed reference breaks the finalizer or a test. Mitigation: the identifier search and the full suite. Likelihood: low.
- Sessions with a cached skill list may call the old name until they reload. Low impact; the error is visible.
- Trimming SKILL.md could drop guidance the helper does not enforce. Mitigation: Task 2 compares each step with the helper code.

## Implementation Log

### 2026-10-04 - Generated index keeps this plan title

- Change: The AC-2 search finds the old name once more, in the generated plans index. The index lists this plan by its title.
- Reason: The index is generated from dated plan titles, and the plan keeps its historical title.
- Impact: AC-2 holds for maintained files; the generated index is treated like the dated docs it lists. No task changes.

### 2026-10-04 - Helper rejects already-staged deletions

- Change: Unstaged the `git mv` renames before publishing. The helper then staged both the old and new paths.
- Reason: The helper checks a missing file with `git ls-files`, which reads the index. A deletion that is already staged is gone from the index, so the helper rejected it. Changing the helper is a non-goal here.
- Impact: Publication only; no AC change. Follow-up: the helper should also accept deletions already staged in the index.

## Outcome
- AC-1: Met. `git mv` moved the folder to `.agents/skills/publish-builder-changes/`, the helper to `scripts/publish_builder_changes.py` and the test to `test_publish_builder_changes.py`. The old folder is gone. SKILL.md and openai.yaml carry the new name, display name and description.
- AC-2: Met for maintained files. `git grep` outside dated docs finds only this plan's title in the generated index (see log). Discovery lists seven skills through `.agents/skills` and the `.claude/skills` symlink.
- AC-3: Met. 69 of 69 tests pass before and after. `check_hub.py check` and `refresh` pass from the new path. This change was published with the renamed helper.
- AC-4: Met. SKILL.md went from 47 to 37 lines. It keeps operation choice, file selection and ownership, outgoing-commit review, dry run, push-failure recovery, the hub check and checkpoints. It drops the restated helper validation steps.
- AC-5: Met when the delivery commit's push succeeds and remote readback matches; see [session memory](../session-memory/2026-10-04.md).
- Shipped as planned, plus one retargeted link in the 2026-09-06 session memory. Follow-ups: sessions with a cached skill list must reload to see the new name; the helper should accept deletions already staged in the index (see log).
