# Rename Complete Builder Work to Deliver Change

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
The Builder delivery skill is named `deliver-change`. The name says what it does: take one change from plan to verified closure, in Builder or in any spoke.

## Background
The user asked for a better name for `complete-builder-work` and whether it is the dev loop. It is. It orchestrates scoping, planning, implementation, local verification, publication and closure, and hands each phase to another skill. The old name had two problems. "Complete" suggests only the closing step, not the whole loop. "Builder" suggests the skill only works on the hub, but most changes land in spokes. The plan is already defined as "the living record of one change", and the sibling skills use verb-object names, so `deliver-change` fits both. The user chose `deliver-change` in chat on 2026-10-04 and asked for a rename only. Splitting out the spoke script was offered and not taken up.

## Goals
- Every maintained file uses the skill name `deliver-change`, and the old name no longer works (AC-1, AC-2).
- Spoke helper behavior and CLI arguments stay exactly the same; only its path changes (AC-3).
- The change is published on Builder main (AC-4).

## Non-Goals
- No split of `manage_spoke_repositories.py` or repository inspection into a separate skill. The user approved a rename only, and a split would be a separate plan.
- No compatibility alias or stub folder for the old name. The earlier renames kept none, and a folder without SKILL.md fails skill discovery.
- No changes to the skill's workflow steps, references' content or the helper's logic. This is a rename.
- No renames inside dated plans, reports or session memory. They are historical records under AGENTS.md. A search found no links from them into the old folder, so none need retargeting.

## Acceptance Criteria
- AC-1: `.agents/skills/deliver-change/` contains SKILL.md (`name: deliver-change`, title `Deliver Change`), agents/openai.yaml, references/closure.md, references/coordination.md, references/repository-inspection.md and scripts/manage_spoke_repositories.py. `.agents/skills/complete-builder-work/` no longer exists.
- AC-2: A search of tracked files outside dated docs finds no `complete-builder-work`. Skill discovery lists exactly seven skills, including deliver-change.
- AC-3: The full native suite passes, including the spoke registry and repository inspection tests that run the helper from its new path. `manage_spoke_repositories.py list` runs from the new path. `check_hub.py check` passes.
- AC-4: The plan, the change and the dated delivery memory are on origin/main, confirmed by remote readback.

## Inputs
- User request in chat on 2026-10-04: "yes and rename to deliver-change", after I offered the rename with or without splitting out the spoke script.
- Inspected on Builder `main` at `4cdd6c8`, clean tree: the skill's SKILL.md, agents/openai.yaml, references/repository-inspection.md and folder listing; AGENTS.md; README.md; .agents/tests/test_skill_consolidation.py and test_spoke_registry.py; publish-builder-changes SKILL.md and phase finalizer; write-implementation-plan plan reference; the publish-builder-changes rename plan as precedent; today's Builder session memory; `git grep` for `complete-builder-work` across the repository and for `skills/complete-builder-work` under docs.

## Branch
Builder primary checkout `main` at `4cdd6c8`; publish the exact task files through publish-builder-changes.

## Assumptions
- The script stays at the same depth, so its import of `.agents/lib` from the Builder root still resolves.
- `.claude/skills` is a symlink to the folder, so Claude Code picks up the new name without other changes.

## Open Questions
None. The user chose the name and the scope.

## Design
Use `git mv` to move the skill folder, then update every maintained reference: the skill's frontmatter, title and Codex metadata; the three script paths in references/repository-inspection.md; AGENTS.md's spoke-locate command and delivery sentence; README's two commands and skill table; and the two test path constants plus the discovery set. README's heading says "Eight Skills" over a seven-row table; correct it to "Seven Skills" while editing that table, since the rename makes the count visible.

Alternatives considered:
- `run-dev-loop`: rejected because "dev loop" is not vocabulary the repository uses.
- `ship-change`: rejected because "ship" implies the work ends at merge or deploy, and the skill continues to closure.
- Keep an alias folder: rejected because discovery requires SKILL.md and an alias would show up as a duplicate skill.

## Expected Changes
- `.agents/skills/complete-builder-work/` â†’ `.agents/skills/deliver-change/` (all six files, history kept by `git mv`).
- SKILL.md: `name` and title. agents/openai.yaml: display name and `$deliver-change` in the default prompt.
- references/repository-inspection.md: three script paths.
- AGENTS.md: spoke-locate command path and the "Use complete-builder-work" sentence.
- README.md: two command paths, the skill table row and the skill count heading.
- .agents/tests/test_skill_consolidation.py: `RepositoryInspectionTests` script path and the SkillDiscoveryTests expected set. .agents/tests/test_spoke_registry.py: `SCRIPT`.
- This plan, today's Builder session memory and regenerated indexes.

## Task Breakdown

### Task 1 - Rename the skill and update references
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: .agents/skills/complete-builder-work/ (all files); AGENTS.md; README.md; .agents/tests/test_skill_consolidation.py; .agents/tests/test_spoke_registry.py.
Symbols: SKILL.md frontmatter `name` and `# Complete Builder Work` title; openai.yaml `interface.display_name` and `default_prompt`; repository-inspection.md command lines; AGENTS.md Hub and Spokes and Quality and Delivery paragraphs; README Start on Any Computer commands and the skills table; `RepositoryInspectionTests.setUp` script path; `SkillDiscoveryTests` expected set; test_spoke_registry `SCRIPT`.
Inspection: Read every listed file on main `4cdd6c8`. `git grep` found no other maintained references and no doc links into the folder.
Behavior: The spoke helper runs from the new path with the same arguments and results. Discovery lists deliver-change.
Invariants: Seven skills, each with SKILL.md and openai.yaml; skill workflow text and helper logic unchanged; dated history unchanged.
Boundary/API: The skill name and helper path change together, with no alias. CLI arguments are unchanged.
Effects and failures: `git mv` keeps the history. A missed reference fails discovery, the command-path check, the spoke tests or the identifier search.
Tests and evidence: Updated native tests; full suite; identifier search.
Verification: python -B -m unittest discover -s .agents/tests; git grep -n complete-builder-work excluding dated docs; python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py list; check_hub.py check; git diff --check.

### Task 2 - Record and publish verified delivery
Dependencies: Task 1 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day Builder memory and the phase finalizer at `4cdd6c8`.
Behavior: The completed change and its dated evidence are on origin/main.
Invariants: Only the selected files are committed; earlier history is preserved.
Boundary/API: publish-builder-changes helper.
Effects and failures: Scoped commit and push. A failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run, then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Runtime verification does not apply. Builder holds workflow instructions and standalone Python helpers, not a runnable application. The native checks below replace it.
- AC-1: `git ls-files .agents/skills/deliver-change`; confirm the old folder is absent; SkillDiscoveryTests.
- AC-2: `git grep -n complete-builder-work` excluding dated docs returns nothing; SkillDiscoveryTests checks the set of seven.
- AC-3: `python -B -m unittest discover -s .agents/tests`; `manage_spoke_repositories.py list` from the new path; `check_hub.py refresh --root .` then review the diff.
- AC-4: Helper output and `git ls-remote origin refs/heads/main` compared with the local HEAD.

## Rollback or Recovery
Revert the task commit to restore the old folder and references together. If a push fails, keep the commit and recover with `--push-only`.

## Risks
- A missed reference breaks spoke location or a test. Mitigation: the identifier search and the full suite. Likelihood: low.
- Sessions with a cached skill list may call the old name until they reload. Low impact; the error is visible.
- Another session edits the same files concurrently. Mitigation: confirm a clean tree immediately before editing and before publishing.

## Implementation Log
No entries yet.

## Outcome
Delivered as planned on 2026-10-04. No deviations.
- AC-1: Met. `git mv` moved all six files to `.agents/skills/deliver-change/`. SKILL.md has `name: deliver-change` and title `Deliver Change`, openai.yaml uses `Deliver Change` and `$deliver-change`, and the old folder is gone.
- AC-2: Met. `git grep -n complete-builder-work` outside dated docs returns nothing. SkillDiscoveryTests passes with the seven-skill set including deliver-change.
- AC-3: Met. `python -B -m unittest discover -s .agents/tests` ran 69 tests, all OK. `manage_spoke_repositories.py list` from the new path listed christopherbell-dev. `check_hub.py refresh` passed. `git diff --check` is clean.
- AC-4: Met. Published with publish-builder-changes and confirmed by `git ls-remote origin refs/heads/main` matching local HEAD; see the [2026-10-04 Builder memory](../session-memory/2026-10-04-builder.md).
Shipped versus planned: identical, including README's corrected "Seven Skills" heading. Follow-up offered but not authorized: move spoke management into its own skill.
