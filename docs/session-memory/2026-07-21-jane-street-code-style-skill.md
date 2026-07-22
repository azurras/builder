# 2026-07-21 Jane Street Code Style Skill

## 21:01 - Enforce Jane Street-inspired code writing across Builder

### Request

The user asked for a skill that writes code in Jane Street house style and required every Builder code-writing path to use it. The user approved interpreting the style as language-agnostic engineering principles adapted to each language rather than imposing OCaml syntax on Java, JavaScript, Python, templates, or other spoke code.

### Project Context

Builder is the AI workflow hub. Its enforceable workflow contract spans `AGENTS.md`, repo-scoped `.agents/skills/*/SKILL.md` files, companion `agents/openai.yaml` prompts, and regression tests. The active spoke is multi-language, so repository-native conventions, formatters, linters, security rules, and existing patterns must continue to control syntax and formatting.

The approved design and implementation plan were saved as phase checkpoints:

- `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-21-jane-street-code-style-skill.md` in commit `53afe9c`.
- `C:\Users\Christopher\Developer\builder\docs\implementation-plans\2026-07-21-jane-street-code-style-skill.md` in commit `92f78d5`.

### Work Completed

- Added `.agents/skills/write-jane-street-style-code/SKILL.md` with a cross-language workflow centered on encoded invariants, narrow and uniform interfaces, explicit effects and failures, behavior-focused tests, small cohesive diffs, and final review.
- Added `agents/openai.yaml` with `$write-jane-street-style-code` in the default prompt and implicit invocation enabled.
- Added `references/language-adaptations.md` for Java, JavaScript, Python, templates, and code-bearing configuration.
- Added a `Code-Writing Standard` section to `AGENTS.md` defining the invocation boundary for production code, tests, scripts, automation, migrations, executable templates, and copy-ready implementation examples.
- Updated `complete-story-issue` so Develop invokes the style skill and the completion checklist records compliance.
- Updated `save-implementation-plan` so every code-changing task carries `Required skill: write-jane-street-style-code` before code edits.
- Updated `review-implementation-plan` to reject code-changing plans that omit the required skill.
- Updated `dispatch-spoke-task` so implementation briefs require the skill before spoke code changes and ask for house-style validation in the return report.
- Updated `review-spoke-work` so code reviews invoke the skill and evaluate actual diffs against its final-review checklist.
- Updated companion `agents/openai.yaml` files for every changed workflow skill.
- Added `.agents/tests/test_jane_street_code_style.py` to enforce the package, repository/orchestrator, planning/dispatch, and spoke-review contracts together.
- Committed and pushed the implementation as `edb76a4` (`Enforce Jane Street code style`).

### Decisions

- Applied Jane Street's broadly reusable principles rather than OCaml-specific syntax or dependencies.
- Gave repository-native conventions precedence for language syntax and formatting.
- Used layered enforcement rather than relying only on skill discovery: repository instructions, orchestration, planning, dispatch, review, metadata, and tests all carry the same rule.
- Kept the main skill concise at 478 words and moved language-specific guidance to a conditional reference.
- Treated read-only inspection commands, generated files, vendored code, and lockfiles as outside the invocation boundary unless intentionally edited by hand.
- Preserved the required skill-authoring bootstrap: the contract test was written and observed failing before the new skill existed; after the skill was created and loaded, every remaining code-bearing edit invoked it.

### Validation

- Baseline before edits: `python -m unittest discover -s .agents/tests -p 'test_*.py' -v` passed 19 tests.
- RED: the new focused test ran four test methods and failed on the missing skill plus repository, planning/dispatch, and review contracts. Three planning subtests produced separate expected assertion failures.
- GREEN: `python -m unittest discover -s .agents/tests -p 'test_jane_street_code_style.py' -v` passed 4 of 4 tests.
- Full regression: `python -m unittest discover -s .agents/tests -p 'test_*.py' -v` passed 23 of 23 tests.
- Skill validation: `quick_validate.py .agents/skills/write-jane-street-style-code` reported `Skill is valid!`.
- YAML validation: all repo-scoped `agents/openai.yaml` files parsed successfully with PyYAML.
- `update-hub-indexes` reported indexes current after implementation.
- `validate-hub-state` passed. It continued to report only the pre-existing warnings for legacy July 8-9 implementation plans missing quality-gated Code Edit blocks.
- `git diff --check` passed. No local application test report was created because no running application behavior changed.

### Current State

- Builder branch: `main`.
- Remote: `https://github.com/azurras/builder.git`.
- Implementation commit `edb76a4` is pushed to `origin/main`.
- No services or spoke repositories were changed.

### Follow-Ups

- No required follow-up remains for this request.
- Future code-writing plans, spoke briefs, and reviews should be covered by the regression test; update the new skill, companion metadata, and contract test together if the house style evolves.
