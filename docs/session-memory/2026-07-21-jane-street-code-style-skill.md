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

## 21:20 - Expand the skill into the authoritative coding standard

### Request

The user reported that the initial skill felt light on guidance. They approved replacing the lightweight checklist with an authoritative, progressively disclosed design, testing, and review standard and asked Codex to implement it immediately for user review.

### Work Completed

- Revised and published the approved specification in commit `1359c23`.
- Replaced the short entrypoint with a mandatory sequence, a five-field Before-Edit Brief, explicit reference routing, house defaults, stop conditions, and a final evidence gate.
- Replaced the 301-word catch-all language reference with six focused references:
  - `design-and-api.md` for domain states, validation boundaries, uniform interfaces, failure categories, error context, effects, concurrency, abstraction, dependency direction, performance, naming, and compatibility.
  - `testing-and-review.md` for a risk-based test-selection matrix, semantic-change evidence, properties, scenario/expect/snapshot tests, integration, concurrency, doubles, blockers, warnings, and a concrete finding format.
  - `java.md`, `javascript.md`, `python.md`, and `templates-and-configuration.md` for repository-native decision guides, paired good/bad examples, testing guidance, and review checklists.
- Updated skill UI metadata so the default prompt requires reference loading, the Before-Edit Brief, test-first work, and the review rubric.
- Updated `save-implementation-plan`, `review-implementation-plan`, and `dispatch-spoke-task` so code-changing work carries a task-specific Before-Edit Brief instead of merely naming the skill.
- Updated `review-spoke-work` so reviews compare the diff with the brief, distinguish blockers from warnings, and use the shared finding format.
- Expanded `.agents/tests/test_jane_street_code_style.py` from four to six methods that enforce the deeper package and workflow contract.
- Committed and pushed the implementation as `c2ca68d` (`Expand Jane Street coding standard`).

### Decisions

- Kept `SKILL.md` as the always-loaded dispatcher and mandatory process, with detailed material one reference level below it.
- Required `design-and-api.md` by observable design scope, `testing-and-review.md` for all behavior changes and reviews, and only the language guides actually involved.
- Made guidance structural where omission was the failure: the Before-Edit Brief has fixed fields and review findings have a fixed evidence shape.
- Kept language-specific examples idiomatic and subordinate to repository-native versions, frameworks, formatters, and security rules.
- Did not run subagent forward-testing because the active coordination policy prohibited subagent use without explicit user authorization. The user's direct skill review is the next evaluation surface.

### Validation

- RED: the expanded focused suite ran six methods and failed eight assertions/subtests for the missing references, brief enforcement, and review rubric.
- GREEN: `python -m unittest discover -s .agents/tests -p 'test_jane_street_code_style.py' -v` passed 6 of 6 methods.
- Full regression: `python -m unittest discover -s .agents/tests -p 'test_*.py' -v` passed 25 of 25 tests.
- Skill validation reported `Skill is valid!`.
- All 22 repo-scoped `agents/openai.yaml` files parsed successfully.
- `git diff --check` passed with only line-ending notices.
- `update-hub-indexes` reported indexes current.
- `validate-hub-state` passed with only the existing legacy-plan warnings from July 8-9.
- The six reference files total 1,087 lines and approximately 8,803 words; every file longer than 100 lines includes a table of contents.

### Current State

- Builder branch `main` is pushed through implementation commit `c2ca68d`.
- No spoke repositories or running services changed.
- The user intends to review the completed skill and may request refinements.

### Follow-Ups

- Incorporate concrete findings from the user's review through the same test-first contract cycle.
- If the user explicitly authorizes independent agent evaluation later, run fresh-context forward tests without leaking the intended outcomes.
