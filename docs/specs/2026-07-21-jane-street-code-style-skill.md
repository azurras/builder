# Jane Street Code Style Skill

## Document Status

`ready-for-review`

Revision: expand the implemented skill from a lightweight checklist into the authoritative Builder standard for code design, implementation, testing, and review.

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
- Give agents concrete decision procedures, not only high-level principles.
- Make the required reasoning observable through a compact pre-edit brief and a consistent review rubric.
- Use progressive disclosure so every coding task receives the mandatory process while deeper guidance is loaded only when relevant.

## Non-Goals

- Do not impose OCaml syntax, Jane Street libraries, or OCaml-specific naming on Java, JavaScript, Python, templates, or other languages.
- Do not replace repository-specific instructions, formatters, linters, security rules, or test frameworks.
- Do not require the skill for read-only inspection or validation commands that do not create or modify a code artifact.
- Do not introduce custom multi-language linters in this change.
- Do not restyle unrelated existing code solely to make it resemble the new guidance.
- Do not turn `SKILL.md` into a monolithic language handbook that consumes unnecessary context on every coding task.
- Do not prescribe one error model, abstraction style, or testing framework when the host language or repository already supplies a stronger idiom.

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

### Required Pre-Edit Brief

Before the first code edit, the skill must require a short, explicit brief with these fields:

- **Behavior:** the externally observable change or preserved behavior.
- **Invariants:** the facts that must always hold, including invalid states that must be rejected or made unrepresentable.
- **Boundary/API:** the public or module boundary affected, including compatibility constraints and uniformity with parallel interfaces.
- **Effects and failures:** I/O, mutation, time, randomness, concurrency, external services, expected failures, and unexpected faults.
- **Tests and evidence:** the first failing test, the risks it covers, and the verification required after implementation.

The brief may be one sentence per field for a narrow change. It must be written before editing and revised when investigation invalidates an assumption. It is a design aid, not a long planning artifact.

### Design and API Guidance

The detailed standard must give decision procedures and paired examples for:

- Modeling domain states with value objects, sums/unions, enums, sealed hierarchies, validated constructors, or boundary validation.
- Choosing where validation belongs and ensuring invalid data does not silently cross a trusted boundary.
- Designing uniform families of functions, methods, commands, and endpoints with predictable names, argument order, return shapes, and throwing versus non-throwing variants.
- Distinguishing absence, expected domain failure, programmer error, and infrastructure failure.
- Preserving causal error context while translating errors at module boundaries.
- Making mutation ownership, I/O, clocks, randomness, concurrency, and external dependencies visible and controllable.
- Choosing direct code, a local helper, a module boundary, or a reusable abstraction based on protected invariants and demonstrated reuse.
- Keeping dependency direction and data flow easy to trace.
- Making meaningful performance costs visible without premature optimization.
- Choosing names and comments that explain domain meaning, units, ownership, and non-obvious constraints.
- Preserving compatibility deliberately and keeping changes cohesive.

Each rule must distinguish the default from legitimate exceptions. The standard must prefer explicit conditional rules over vague phrases such as “when appropriate.”

### Testing and Review Guidance

The detailed standard must provide a risk-based test-selection matrix covering:

- Example tests for readable representative behavior.
- Boundary and negative tests for validation and failure contracts.
- Property or generative tests for large input spaces, algebraic laws, parsers, serializers, and state transitions.
- Scenario or expect/snapshot tests for multi-step behavior and diagnostic traces, with safeguards against indiscriminate snapshot approval.
- Integration or contract tests for boundaries that cannot be proven by isolated units.
- Concurrency tests for ownership, ordering, cancellation, timeout, and race-sensitive behavior.

Tests should normally exercise the narrowest public boundary that proves the behavior. Every semantic production change must have an observable test change or a recorded explanation that an existing test already failed and now passes.

The final review rubric must separate:

- **Blockers:** invalid states can enter trusted code, effects or failures are hidden, parallel APIs are inconsistent without reason, a semantic change lacks evidence, tests assert incidental implementation, or the diff contains unrelated work.
- **Warnings:** an abstraction protects no invariant, error context is lost, names hide units or ownership, performance costs are surprising, tests are brittle, or comments repeat syntax instead of explaining constraints.

Review findings must cite concrete code and describe the violated invariant, boundary, behavior, or evidence gap.

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

Updated workflow skills must continue to enforce invocation and, where they review or approve work, require the new pre-edit brief and review rubric rather than merely checking that the skill name appears.

## Proposed Approach

### Skill Structure

Create `.agents/skills/write-jane-street-style-code/` containing:

- `SKILL.md`: concise mandatory workflow, pre-edit brief, reference-routing table, core defaults, stop conditions, and final evidence gate.
- `agents/openai.yaml`: display name, short description, default prompt, and implicit invocation policy.
- `references/design-and-api.md`: authoritative language-neutral design and API standard with decision procedures and one canonical worked example.
- `references/testing-and-review.md`: test-selection guidance, evidence rules, review rubric, and finding format.
- `references/java.md`: Java-specific applications of the standard.
- `references/javascript.md`: JavaScript and TypeScript-specific applications of the standard.
- `references/python.md`: Python-specific applications of the standard.
- `references/templates-and-configuration.md`: executable template and code-bearing configuration guidance.

The main skill will remain language-agnostic and concise. All references will be linked directly from `SKILL.md`; references longer than 100 lines will include a table of contents. The former catch-all `references/language-adaptations.md` will be removed after its useful content is incorporated into the focused guides.

### Reference Routing

The entrypoint must require agents to load references according to observable work scope:

- Read `design-and-api.md` when changing domain logic, state, public or module APIs, validation, error handling, effects, concurrency, abstraction boundaries, or performance-sensitive behavior.
- Read `testing-and-review.md` for every behavior change and every code review.
- Read exactly the language guide for each language being edited. Load multiple language guides only for a genuinely cross-language change.
- Read `templates-and-configuration.md` for executable templates and code-bearing configuration, in addition to a language guide when both apply.

Read-only investigation may occur before the brief. Code editing must not begin until the brief is coherent and the required references have been read.

### Contract Testing

Add `.agents/tests/test_jane_street_code_style.py` before implementing the skill or changing workflow contracts. The initial test run must fail because the new contract does not yet exist.

The tests will verify:

- Required skill files and metadata exist.
- The skill description triggers before code-writing work.
- The skill contains the approved core principles and invocation boundary.
- Repository and workflow layers explicitly require the skill.
- Planning, dispatch, and review contracts carry complementary requirements.
- Companion `agents/openai.yaml` prompts remain aligned.
- The pre-edit brief has all five required fields and is required before editing.
- Every deep reference exists and `SKILL.md` routes work to it explicitly.
- Design guidance covers states, boundaries, uniform interfaces, failures, effects, abstraction, concurrency, compatibility, and performance transparency.
- Testing guidance includes the risk-based matrix, semantic-change evidence rule, blockers, warnings, and finding format.
- Each language reference contains idiomatic decision guidance and good-versus-bad examples without overriding repository-native conventions.
- Long references contain a table of contents and remain one link away from `SKILL.md`.

After implementation, run the focused test, the full `.agents/tests` suite, skill validation, index refresh, and hub-state validation.

## Expected Files

- `AGENTS.md`
- `.agents/skills/write-jane-street-style-code/SKILL.md`
- `.agents/skills/write-jane-street-style-code/agents/openai.yaml`
- `.agents/skills/write-jane-street-style-code/references/design-and-api.md`
- `.agents/skills/write-jane-street-style-code/references/testing-and-review.md`
- `.agents/skills/write-jane-street-style-code/references/java.md`
- `.agents/skills/write-jane-street-style-code/references/javascript.md`
- `.agents/skills/write-jane-street-style-code/references/python.md`
- `.agents/skills/write-jane-street-style-code/references/templates-and-configuration.md`
- `.agents/skills/write-jane-street-style-code/references/language-adaptations.md` (remove after migration)
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
8. Confirm the entrypoint remains concise while the reference package contains enough concrete guidance to answer realistic design and review questions without reconstructing the standard from first principles.

## Acceptance Criteria

- `write-jane-street-style-code` is a valid repo-scoped skill with aligned UI metadata.
- Every Builder workflow that plans, dispatches, performs, or reviews code changes explicitly invokes or enforces the skill.
- The style remains language-agnostic and defers syntax and formatting to repository-native conventions.
- A five-field pre-edit brief is required before the first code edit.
- The package contains detailed, routed guidance for design/API work, testing/review, Java, JavaScript/TypeScript, Python, templates, and code-bearing configuration.
- Review outcomes use the shared blocker/warning rubric and cite concrete evidence.
- A focused regression test proves the cross-layer contract.
- The full Builder test suite and hub validation pass.

## Open Questions

None. The user approved an authoritative, progressively disclosed standard with detailed decision procedures, examples, testing guidance, review rubrics, and deeper language adaptations.
