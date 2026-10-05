---
name: write-chris-street-style-code
description: Use when creating, changing, refactoring, or reviewing code, tests, scripts, migrations, code-bearing configuration, or executable examples in any language.
---

# Write Chris Street-Style Code

Apply this house adaptation of Jane Street engineering and review principles to **every language**. Use each repository's syntax, formatter, frameworks, and supported toolchain. The same contracts apply to production code, tests, reusable scripts, migrations, and executable examples. This skill supplements task-specific implementation and security guidance. [Sources and adaptation](references/sources-and-adaptation.md) explain the origin of the rules.

## Required Reference Selection

Read the applicable references before editing or reviewing the affected code. An unlisted language is covered by the shared rules and adaptation procedure.

| Work | Read |
|---|---|
| Any implementation or code review | [Naming and readability](references/naming-and-readability.md), [good and bad examples](references/good-and-bad-examples.md), [testing and review](references/testing-and-review.md) |
| State, validation, API, errors, effects, concurrency, compatibility, or performance | [Design and API](references/design-and-api.md) |
| Every language; especially one without a dedicated guide | [Language adaptation](references/language-adaptation.md) |
| Java | [Java](references/java.md) |
| JavaScript or TypeScript | [JavaScript/TypeScript](references/javascript.md) |
| Python | [Python](references/python.md) |
| Shell commands, SQL, templates, configuration, migrations, or generated code | [Configuration and templates](references/templates-and-configuration.md) |

Load only the dedicated language guides for the files in scope. Read the sections of the examples reference that address the affected contract.

## Mandatory Coding Rules

1. **All code must read like a sentence.** Read the receiver, method/function name, parameter names, and actual argument names together. They must explain the operation or question without requiring a comment to translate them. Parameter names must complement method names: `send_invoice_to(invoice, recipient)` expresses an action and both roles. Predicates read as questions, such as `invoice.isOverdueOn(asOfDate)`.
2. **Names describe the data and its role.** Use domain terms and distinguish IDs from objects, collections from items, raw input from validated values, and units such as milliseconds. Replace vague `data`, `result`, `temp`, `handle`, or `process` names when their role is not clear from a small local context.
3. **Different meanings get different variables.** When parsing, decoding, validating, aggregating, or otherwise changing the meaning or representation of data materially, introduce a new variable with the new meaning. Ordinary updates within one role, such as a running total or loop counter, may retain their variable.
4. **Encode the valid domain.** Identify allowed states and transitions before selecting types. Use validated construction and distinct alternatives when they exclude invalid combinations. In languages without useful type support, validate at the boundary and keep trusted data behind a clear module or function contract.
5. **Validate before relying on input.** Parse, normalize deliberately, and validate external input at the trust boundary. Reject malformed data with causal diagnostics. A type annotation, cast, database row, or JSON parse alone does not validate the domain.
6. **Make APIs predictable.** Match related operations' names, parameter order, units, return shapes, and failure conventions. Inspect callers before changing public signatures, named parameters, stored data, or externally visible behavior.
7. **Make effects and ownership visible.** Give mutable state, resources, transactions, listeners, and background work a clear owner. Show I/O, blocking, persistence, cancellation, and cleanup at the boundary that controls them. A read-only-sounding operation must not conceal a write.
8. **Preserve distinct outcomes.** Separate legitimate absence, domain rejection, infrastructure/protocol failure, and programming defects. Use native explicit results or exceptions consistently. Preserve the original cause when translating failures; redact secrets.
9. **Choose direct structure.** Keep one purpose per function and one coherent purpose per change. Extract an abstraction for demonstrated reuse, a protected invariant, or an isolated effect. Prefer named intermediate values and clear branches over compressed expressions that hide meaning.
10. **Prove the contract.** Select evidence that can detect the actual error at the smallest supported boundary. Read the final production and test changes together. Formatting and compilation establish their specific claims; they do not prove all runtime behavior.

For naming, a sentence is a readability requirement, not a requirement to spell English prose into every identifier. Respect idiomatic casing, operator names, framework protocols, and stable public contracts. Use labels, named arguments, an enum, or a meaningful value type when positional arguments obscure roles. Inspect compatibility before renaming a parameter that callers use by name.

## Implementation Mode

Use when changes are authorized. Follow these steps:

1. Read trusted requirements, repository instructions, adjacent code, affected callers, and existing tests. Identify the supported language version and native tooling.
2. Reuse the current plan's **Before-Edit Brief** if it still matches the task. Otherwise state: **Behavior**, **Invariants**, **Boundary/API**, **Effects and failures**, and **Tests and evidence**. Each field must name the actual behavior, boundary, and risk rather than restating this skill.
3. Select applicable references and starting evidence from the table below. Resolve missing facts and contradictions through inspection before choosing a design.
4. Implement the smallest complete change. Apply the mandatory rules to definitions, call sites, conditionals, transformations, and error paths. Revisit the brief when evidence changes an assumption.
5. Run the native formatter/analyzer and focused checks appropriate to the change. Exercise the real integration or runtime boundary when that boundary is part of the contract.
6. Review the complete final diff and its callers using the review sequence below. Correct actionable defects within the authorized scope; keep unrelated changes out of the diff.
7. Report what changed, the evidence actually observed, and any remaining limitation. Follow repository publication and delivery requirements.

| Change | Starting and final evidence |
|---|---|
| Feature or bug with observable behavior | Witness a failing regression or focused behavioral example, then its passing result |
| Type constraint or analyzer correction | Reproduce the compiler/analyzer finding, then show it resolved; add behavioral evidence when semantics change |
| Behavior-preserving refactor | Record passing characterization before and after; add coverage first if preservation cannot be checked |
| Configuration, migration, or executable example | Use an artifact-native parser, compile/run, dry-run, or reproducible validation; check effective behavior and recovery where applicable |
| Documentation-only instructions | Verify links, discoverability, metadata, examples, and whether a reader can choose the required action |

Do not invent a failing test for a preservation claim. Add meaningful tests for actual risk; do not add tests that only echo an implementation or document wording. Once adequate checks pass, broaden or repeat them when a relevant change, failure, or unresolved concern warrants it.

## Review Mode

Review-only requests remain read-only. This skill grants no permission to edit, publish findings, message other people, or begin delivery.

1. Identify the exact revision and full change being reviewed, trusted requirements, and supplied evidence. Reconstruct a missing contract from inspected requirements and callers.
2. Trace input through validation, transformations, and returned outcomes. Identify effects, owners, failure paths, and compatibility surfaces.
3. Read definitions and actual calls as sentences. Check parameter roles, argument order, units, vague names, and reused variables whose meaning changes.
4. Inspect the state model, control flow, abstraction, and changed callers. Look for a concrete counterexample to the proposed contract.
5. Read the tests and check that their assertions can detect the counterexample. Run proportionate available checks and report gaps rather than assuming unobserved results.
6. Compare the final content with the content previously reviewed. Revisit relevant later edits, rebases, merges, and conflict resolutions; old approval applies only to content and assumptions it actually covered.
7. Report each finding with **severity, exact location, violated contract, concrete evidence/counterexample, and required correction**. Correctness, security, compatibility, and required-evidence gaps are blockers; actionable readability or design costs are warnings when correctness is established.

Do not downgrade a blocker to finish, invent findings, or claim independent review when only self-review occurred. If no findings remain, say what revision and evidence were inspected and what could not be verified.

## Completion Gate

Before declaring the work complete, confirm:

- The implemented behavior matches the current brief and trusted requirements.
- Each touched definition and call explains its operation; parameters complement method names and transformed values keep accurate names.
- Input validation, valid states, ownership, effects, failure causes, and compatibility are clear at their actual boundaries.
- Required native checks and applicable runtime evidence were observed, with gaps disclosed.
- The final content and any conflict resolutions were reviewed; relevant later edits have not escaped review.
- No actionable blocker remains; publication and closure follow the repository's authorized workflow.

Resolve ordinary design issues through inspection and correction. Ask for user input when authority is genuinely missing or requirements conflict in a consequential way.
