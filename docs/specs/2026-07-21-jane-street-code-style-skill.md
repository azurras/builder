# Jane Street Code Style Skill

## Document Status

`ready-for-review`

## Purpose

Create a repo-scoped Codex skill that applies Jane Street-inspired engineering principles whenever Builder workflows produce or change code, and make the requirement durable across planning, implementation, delegation, and review.

## Background

Builder coordinates work in its own Python helpers and in multi-language spoke repositories. The active `christopherbell.dev` spoke currently includes Java, JavaScript, templates, and related automation. Jane Street's public engineering material is centered on OCaml, but its broadly reusable principles include uniform interfaces, explicit invariants, extensive behavior-focused testing, small reviewable changes, and careful review for clarity and correctness.

The new skill will translate those principles into language-agnostic guidance. Repository instructions, established local patterns, native language idioms, formatters, and linters will continue to control syntax and formatting.

Primary public references:

- [Core Principles: uniformity of interface](https://blog.janestreet.com/core-principles-uniformity-of-interface/)
- [Ironing out your development style](https://blog.janestreet.com/ironing-out-your-development-style/)
- [Scrutinize your code in style](https://blog.janestreet.com/scrutinizing-your-code-in-style/)
- [Formal methods and the future of programming](https://blog.janestreet.com/formal-methods-at-jane-street-index/)

## Goals

- Create one discoverable repo-scoped skill named `write-jane-street-style-code`.
- Require the skill before Codex creates, modifies, or rewrites code through Builder workflows.
- Carry the requirement from plans and spoke task briefs into implementation and review.
- Make compliance testable through Builder contract tests.
- Preserve language-native conventions while applying a consistent engineering standard.

## Non-Goals

- Do not impose OCaml syntax, Jane Street libraries, or OCaml-specific naming on Java, JavaScript, Python, templates, or other languages.
- Do not replace repository-specific instructions, formatters, linters, security rules, or test frameworks.
- Do not require the skill for read-only inspection or validation commands that do not create or modify a code artifact.
- Do not introduce custom multi-language linters in this change.
- Do not restyle unrelated existing code solely to make it resemble the new guidance.

## Requirements

### Invocation Boundary

Invoke `write-jane-street-style-code` before creating or modifying:

- Production source code.
- Tests and test utilities.
- Reusable scripts and automation.
- Migrations and code-bearing configuration.
- Templates with executable behavior.
- Copy-ready code examples intended for implementation.

Generated files, vendored code, lockfiles, and read-only shell commands are outside the invocation boundary. When generated output is intentionally edited by hand, the skill applies to the hand-written change.

### House-Style Contract

The skill must direct Codex to:

- Understand the local module and its invariants before editing.
- Encode valid states and important invariants in types, constructors, validation boundaries, or the strongest mechanism the language provides.
- Prefer small, composable units with narrow and uniform interfaces.
- Keep data flow, mutation, side effects, and failure behavior explicit.
- Use precise names and straightforward control flow instead of clever compression.
- Add abstraction only when it removes demonstrated duplication or protects an invariant.
- Write behavior-focused tests, including property-based or generative tests when they materially improve state-space coverage.
- Keep diffs small, cohesive, reviewable, and free of unrelated refactors.
- Run repository-native formatting, static analysis, and focused tests.
- Review the final diff for clarity, correctness, invariant preservation, and unnecessary complexity.

### Workflow Enforcement

The requirement must exist at every layer that can authorize, describe, perform, or approve code-writing work:

- `AGENTS.md`: repository-wide rule and invocation boundary.
- `complete-story-issue`: invoke the skill before the Develop phase and record compliance in the completion checklist.
- `save-implementation-plan`: require code-changing tasks and Code Edit blocks to name the skill as an execution constraint.
- `review-implementation-plan`: reject ready plans that omit the skill for code-changing work.
- `dispatch-spoke-task`: require implementation briefs to tell the spoke agent to invoke the skill before code changes.
- `review-spoke-work`: include house-style compliance in review scope and merge readiness.
- Relevant `agents/openai.yaml` files: keep UI-facing prompts aligned with each updated skill contract.

The new skill must include its own `agents/openai.yaml` with implicit invocation enabled by default.

## Proposed Approach

### Skill Structure

Create `.agents/skills/write-jane-street-style-code/` containing:

- `SKILL.md`: concise workflow, core contract, quick reference, one representative Java example, common mistakes, and final review checklist.
- `agents/openai.yaml`: display name, short description, default prompt, and implicit invocation policy.
- `references/language-adaptations.md`: focused Java, JavaScript, Python, and template guidance loaded only when relevant.

The main skill will remain language-agnostic and concise. Language-specific details will live one reference level below it to preserve context efficiency.

### Contract Testing

Add `.agents/tests/test_jane_street_code_style.py` before implementing the skill or changing workflow contracts. The initial test run must fail because the new contract does not yet exist.

The tests will verify:

- Required skill files and metadata exist.
- The skill description triggers before code-writing work.
- The skill contains the approved core principles and invocation boundary.
- Repository and workflow layers explicitly require the skill.
- Planning, dispatch, and review contracts carry complementary requirements.
- Companion `agents/openai.yaml` prompts remain aligned.

After implementation, run the focused test, the full `.agents/tests` suite, skill validation, index refresh, and hub-state validation.

## Expected Files

- `AGENTS.md`
- `.agents/skills/write-jane-street-style-code/SKILL.md`
- `.agents/skills/write-jane-street-style-code/agents/openai.yaml`
- `.agents/skills/write-jane-street-style-code/references/language-adaptations.md`
- `.agents/skills/complete-story-issue/SKILL.md`
- `.agents/skills/complete-story-issue/agents/openai.yaml`
- `.agents/skills/save-implementation-plan/SKILL.md`
- `.agents/skills/save-implementation-plan/agents/openai.yaml`
- `.agents/skills/review-implementation-plan/SKILL.md`
- `.agents/skills/review-implementation-plan/agents/openai.yaml`
- `.agents/skills/dispatch-spoke-task/SKILL.md`
- `.agents/skills/dispatch-spoke-task/agents/openai.yaml`
- `.agents/skills/review-spoke-work/SKILL.md`
- `.agents/skills/review-spoke-work/agents/openai.yaml`
- `.agents/tests/test_jane_street_code_style.py`

## Validation Plan

1. Run the new contract test before implementation and confirm it fails for missing house-style integration.
2. Validate the completed skill's frontmatter, directory name, and companion metadata.
3. Run the focused house-style contract test and confirm it passes.
4. Run all Builder tests under `.agents/tests`.
5. Regenerate Builder indexes and review the diff.
6. Run `validate-hub-state` and resolve new errors.
7. Inspect the final diff to confirm no code-writing workflow was missed and unrelated files were not changed.

## Acceptance Criteria

- `write-jane-street-style-code` is a valid repo-scoped skill with aligned UI metadata.
- Every Builder workflow that plans, dispatches, performs, or reviews code changes explicitly invokes or enforces the skill.
- The style remains language-agnostic and defers syntax and formatting to repository-native conventions.
- A focused regression test proves the cross-layer contract.
- The full Builder test suite and hub validation pass.

## Open Questions

None. The user approved language-agnostic Jane Street principles with layered enforcement across all Builder code-writing paths.
