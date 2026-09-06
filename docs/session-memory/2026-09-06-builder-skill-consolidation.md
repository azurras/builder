# 2026-09-06 - Builder Skill Consolidation

## 18:08 - Builder Skill Consolidation

### Request and Context

The user approved simplifying, combining, and removing redundant Builder skills after reviewing repository session history. Superpowers was excluded. The observed workflow favored a small number of entry points with specialized mode references while retaining explicit artifact publication checkpoints and runtime safeguards.

### Work Completed

Reduced discoverable skills from 22 to 11: six consolidated mode-based skills plus five retained specialists. See the [migration map](../skill-migration.md) and [approved spec](../specs/2026-09-06-builder-skill-consolidation.md) for the mapping and scope. Updated AGENTS.md, README, active references, UI metadata, and policy tests. Retired only old SKILL.md/UI metadata; historical artifacts, templates, and every legacy Python CLI path remain.

Six repeated record writers now share `.agents/lib/artifact_cli.py` and `artifact_io.py`, including legacy filename truncation quirks and overwrite refusal. Repository management defaults to read-only inspection; explicit snapshots preserve bytes/mtime when semantic state is unchanged. Git failures are surfaced as errors and nonzero status rather than clean repositories. Maintenance defaults to read-only checks; explicit refresh generates indexes and validates. Its caller owns publication, with no automatic extra memory cycle. Runtime-report save mode consumes completed evidence without restarting verification.

### Publication and Closure

Spec checkpoint `b4ee9aa` and plan checkpoint `c678ae0` were published before development. Implementation `63ab5c8` was committed and pushed to Builder main after selected-file dry run and validation. This continuity record and final spec/plan statuses form the completion checkpoint. No source issue was supplied, so external issue closure is not applicable. No spoke repository, production service, or Superpowers content was changed.

### Validation

- `python -B -m unittest discover -s .agents/tests`: 55 tests passed. New cases cover six legacy writers, duplicate/overwrite/slug behavior, actual temporary Git repositories, explicit Git errors, default management inspection, explicit registration/snapshot, snapshot byte/mtime preservation, maintenance check/refresh/failure, and exactly 11 discoverable skills with resolvable active links/commands.
- All 11 skill entrypoints passed skill-creator quick validation; all UI YAML parsed with matching invocation names. All 19 existing/new script `--help` commands succeeded.
- `maintain_builder_hub.py check --root .`: current indexes and valid hub state, retaining the same eight explicitly grandfathered pre-schema plan warnings. Final completion artifacts are refreshed and validated before their selected-file publication.
- `git diff --check`: passed before publication.
- Independent read-only Python review and scope scenarios covered spec-only, review-only, closure-only, returned spoke update, maintenance check, and snapshots. Two findings (runtime evidence reuse and truncated UI descriptions) were corrected; final review found no remaining blockers.
- Runtime Evidence Required: false. This is standalone tooling/instruction work without application runtime impact; actual CLI and temporary-Git scenarios are the applicable native checks. No fabricated app report was created.

### Decisions and Follow-ups

Keep the existing helper paths as compatibility interfaces and use the migration map for old skill invocations in historical session records. Preserve separate spec, plan, applicable runtime report, and continuity phase commits. Link primary evidence instead of copying it across work/closure/memory. Reverting the implementation commit restores old skill discovery if recovery is needed. No implementation follow-ups remain; the eight historical plan warnings are unchanged legacy documentation debt.
