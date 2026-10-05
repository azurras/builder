# Retire Maintain Builder Hub Skill

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Remove the `maintain-builder-hub` skill and move its index and validation scripts under `commit-push-builder-main`, whose phase finalizer is their only real caller.

## Goals
- Keep index generation and hub validation behavior unchanged.
- Remove a thin skill entry that agents rarely invoke on its own.
- The phase finalizer runs the moved script directly.
- Align README, tests, index headers and the one historical link to the removed redirect stub.

## Inputs
User request in this chat after a review found the skill is a 13-line wrapper. Inspected the skill's SKILL.md, agents/openai.yaml, references/phase-finalization.md and three scripts; commit-push-builder-main SKILL.md and references/phase-finalization.md; README.md; AGENTS.md; three test modules; the three docs index files; and a repository-wide search for the skill name and script names.

## Branch
Builder primary checkout `main`, inspected at `726787e` with a clean working tree; publish the exact task files through the Builder helper.

## Non-Goals
Change validation rules, index format beyond the header line, the commit helper, application code or deployment.

## Assumptions
Scripts moved to `commit-push-builder-main/scripts` sit at the same depth, so their `parents[3] / "lib"` import path stays valid.

## Open Questions
None. Decision: retarget the single historical link in `docs/session-memory/2026-09-06-builder.md` to the current phase finalizer instead of keeping a stub folder, because the validator checks session-memory links and a folder without SKILL.md fails skill discovery. The precedent is the earlier rename plan, which updated references in historical documents. Record the change in today's memory.

## Task Breakdown

### Task 1 - Move scripts and remove the skill
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: .agents/skills/maintain-builder-hub/ (SKILL.md, agents/openai.yaml, references/phase-finalization.md, scripts/maintain_builder_hub.py, scripts/update_hub_indexes.py, scripts/validate_hub_state.py); .agents/skills/commit-push-builder-main/SKILL.md and references/phase-finalization.md; README.md; .agents/tests/test_skill_consolidation.py, test_artifact_quality.py, test_test_report_workflow.py; docs/*/index.md; docs/session-memory/2026-09-06-builder.md.
Symbols: wrapper `main` command paths; `update_hub_indexes` header line; MaintenanceModeTests script path; SkillDiscoveryTests expected set; script constants in the two other tests; README skill table and symlink sentence; finalizer step 2; commit-push Checkpoints section.
Inspection: Read every file listed on main 726787e; repository-wide search found no other maintained references (AGENTS.md has none).
Behavior: `python .agents/skills/commit-push-builder-main/scripts/check_hub.py [check|refresh] --root .` behaves exactly like the old wrapper; the skill no longer appears in discovery.
Invariants: Seven skills remain, each with SKILL.md and openai.yaml; validation rules, index contents other than the header, and the legacy-plan allowance are unchanged; dated history keeps its text apart from the one link target.
Boundary/API: Script location and wrapper filename change (`maintain_builder_hub.py` to `check_hub.py`); CLI arguments are unchanged. No alias is kept.
Effects and failures: `git mv` for the three scripts, `git rm` for the skill files; the wrapper resolves sibling scripts from its own folder; a stale path fails tests or link validation.
Tests and evidence: Existing maintenance, discovery, artifact-quality and test-report workflow tests at the new paths; full native suite.
Verification: python -B -m unittest discover -s .agents/tests; check_hub.py refresh then check; search for the old skill and script names outside dated records; git diff --check.

### Task 2 - Ignore code when validating document links
Required skill: write-chris-street-style-code
Dependencies: None; independent of Task 1, but the finalizer cannot pass on main until it lands.
Files: .agents/lib/builder_hub.py; .agents/tests/test_artifact_quality.py.
Symbols: `markdown_links`; a new regression test beside `test_hub_validates_new_plans_without_literal_code_edits`.
Inspection: On main 726787e the hub validator fails on docs/session-memory/2026-10-04-builder.md, where the inline code span `[this](std::stop_token stopToken)` matches the link pattern. `markdown_links` has one caller, validate_hub_state.py.
Behavior: Links inside fenced code blocks and inline code spans are not treated as links; real links in prose are still found and broken ones still reported.
Invariants: Return type and the link regex for prose are unchanged; no other helper changes.
Boundary/API: `markdown_links(markdown) -> list[str]` signature unchanged.
Effects and failures: Pure string processing; no I/O.
Tests and evidence: New unit test covering a fenced block, an inline span and a real prose link; the hub check passes on the current checkout.
Verification: python -B -m unittest discover -s .agents/tests; check_hub.py check --root .

### Task 3 - Record and publish verified delivery
Dependencies: Tasks 1 and 2 checks and semantic review pass.
Files: This plan, docs/session-memory/2026-10-04-builder.md and generated indexes.
Symbols: Appended delivery entry.
Inspection: Read same-day Builder entries and the phase finalizer.
Behavior: Publish the completed change and dated evidence on origin/main.
Invariants: Exact selected files only; earlier history preserved.
Boundary/API: Existing Builder publication helper and document layout.
Effects and failures: Scoped commit and push; a failed push stays incomplete and uses push-only recovery.
Tests and evidence: Passing native checks, reviewed diff and remote main readback.
Verification: Helper dry-run, then publication; inspect the commit and git ls-remote origin refs/heads/main.

## Code Changes
File moves, one wrapper path change, one header string, reference updates, and code-span stripping in `markdown_links`.

## Files and Modules
Listed in Tasks 1 to 3.

## Unit Testing
Run the existing native suite with updated paths and the seven-skill discovery set.

## Local Testing
Runtime verification does not apply: Builder holds workflow instructions and standalone Python helpers, with no runnable application. Run the moved helpers and native tests instead.

## Validation
Hub refresh and check, skill discovery, link checks, old-identifier search and whitespace check.

## Rollback or Recovery
Revert the task commit to restore the skill folder and references together. Recover a failed publication with the existing push-only workflow.

## Risks
A missed path breaks the finalizer or tests; the full suite and identifier search cover this. Agents with cached skill lists may still try the old skill until the session reloads.

## Completion Criteria
The skill folder is gone; scripts run from commit-push-builder-main; all maintained references updated; native checks and review pass; plan and dated delivery evidence published and confirmed on remote main.
