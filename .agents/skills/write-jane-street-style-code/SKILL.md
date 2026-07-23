---
name: write-jane-street-style-code
description: Use when creating, modifying, refactoring, or reviewing production code, tests, reusable scripts, migrations, code-bearing configuration, executable templates, or copy-ready implementation examples in any language.
---

# Write Jane Street-Style Code

## Overview

Make invalid states difficult to express, interfaces predictable, effects and failures visible, and every semantic change easy to test and review. Apply these principles through repository-native language conventions; do not imitate OCaml syntax or replace local formatters, linters, frameworks, or security rules.

This is a cross-cutting coding standard. Compose it with task-specific implementation, debugging, security, review, and framework skills; it does not replace them.

**REQUIRED SUB-SKILL:** Use `superpowers:test-driven-development` for features, bug fixes, and behavior changes.

## Operating Mode

Choose implementation or review mode from the user's requested outcome and your authority. If the request includes both, complete review mode first, then enter implementation mode only for changes the user authorized.

In either mode:

1. Read repository instructions, adjacent implementation, tests, and public interfaces.
2. Load the references selected by the routing table below.
3. Identify the behavior, invariants, boundary, effects/failures, and relevant evidence.

### Implementation Mode

Use for creating, modifying, or refactoring code.

1. Write the Before-Edit Brief.
2. Resolve contradictions or missing facts through read-only investigation.
3. Select and witness the evidence required by Evidence by Change Type.
4. Implement a cohesive change that fully satisfies the stated contract.
5. Run repository-native formatting, static analysis, focused tests, and proportionate integration checks.
6. Apply the review rubric in `references/testing-and-review.md` to the final diff.

Do not edit code until the required references are read and the Before-Edit Brief is coherent. If investigation changes an assumption, revise the brief before continuing.

### Review Mode

Use for reviewing an existing change. Do not modify code unless explicitly requested.

1. Inspect the stated evidence: requirements, Before-Edit Brief, diff, tests, and validation results. If the brief is absent, reconstruct the contract from trusted requirements and report the missing artifact when the workflow requires it.
2. Inspect affected callers, parallel interfaces, trust boundaries, effects, failure paths, and compatibility surfaces.
3. Run available non-mutating verification proportionate to the risk.
4. Apply the blockers, warnings, and finding format in `references/testing-and-review.md`.
5. Report findings and evidence without implementing corrections.

Review mode does not require manufacturing a failing test or producing a passing change.

## Evidence by Change Type

Use the evidence type that can disprove the intended claim:

| Change type | Required starting evidence |
|---|---|
| Feature, behavior change, or bug fix | A failing behavioral test or existing regression that demonstrates the missing or incorrect behavior. Follow `superpowers:test-driven-development`. |
| Type-level contract | A compiler/type-check failure that demonstrates the absent constraint; add runtime tests as well when runtime behavior changes. |
| Static policy or analyzer-driven correction | The analyzer finding from the repository-native tool, plus behavioral evidence when semantics change. |
| Behavior-preserving refactor | A passing characterization baseline before and after the refactor. Add characterization coverage first when existing coverage is insufficient. Do not manufacture a failure. |
| Code-bearing configuration, migration, or executable example | A failing validation, dry-run, migration check, compilation, or reproducible command appropriate to the artifact and risk. |

Call the failing form **RED evidence**. A passing characterization baseline is preservation evidence, not RED; record it explicitly instead of pretending it failed.

## Before-Edit Brief

Write one concrete statement for each field. A narrow change may use one sentence per field.

- **Behavior:** State the externally observable change or behavior that must remain unchanged.
- **Invariants:** State what must always hold and which states must be rejected or made unrepresentable.
- **Boundary/API:** Name the affected public or module boundary, compatibility constraints, and neighboring interface pattern.
- **Effects and failures:** Identify I/O, mutation, time, randomness, concurrency, external services, expected failures, and unexpected faults.
- **Tests and evidence:** Name the selected RED evidence or passing characterization baseline, the risks it covers, and the final verification evidence.

## Reference Routing

| Observable work scope | Required reference |
|---|---|
| Domain state, validation, API, errors, effects, abstraction, concurrency, compatibility, or performance changes | Read `references/design-and-api.md`. |
| Any behavior change, refactor, bug fix, test change, or code review | Read `references/testing-and-review.md`. |
| Java source or tests | Read `references/java.md`. |
| JavaScript or TypeScript source or tests | Read `references/javascript.md`. |
| Python source or tests | Read `references/python.md`. |
| Executable templates or code-bearing configuration | Read `references/templates-and-configuration.md`. |

Load every applicable row and only the applicable language guides. A cross-language change may require multiple guides.

## House Defaults

| Concern | Default decision |
|---|---|
| State | Represent allowed cases directly; validate untrusted data once at the boundary. |
| Interface | Match parallel names, argument order, return shapes, and failure conventions. |
| Effects | Keep I/O and mutable ownership at explicit seams; pass clocks, randomness, and services when control matters. |
| Failures | Distinguish absence, expected domain failure, programmer error, and infrastructure failure. Preserve causal context. |
| Abstraction | Start direct; extract only to remove demonstrated duplication, protect an invariant, or isolate an effect. |
| Data flow | Prefer visible transformations and one clear owner for mutable state. |
| Performance | Make surprising cost, blocking, allocation, or remote work visible in the interface or name. |
| Tests | Prove behavior at the narrowest public boundary; use properties when examples cannot cover the state space. |
| Change size | Keep one coherent purpose per diff and exclude opportunistic restyling. |

## Stop Conditions

Stop and redesign before editing when any of these is unresolved:

- Valid and invalid domain states cannot be distinguished at a trusted boundary.
- Callers cannot tell whether a function mutates, blocks, performs I/O, or may fail.
- Parallel APIs would use inconsistent names, arguments, results, or error conventions without a documented reason.
- The test requires extensive mocking or private-state assertions because the boundary is too coupled.
- A proposed abstraction has no current reuse, protected invariant, or isolated effect.
- The change mixes unrelated behavior or restyling that can be separated safely.

## Final Evidence Gate

Before claiming completion:

- Confirm the Before-Edit Brief still describes the implemented behavior.
- Confirm invalid states are rejected before trusted code relies on them.
- Confirm effects, ownership, and failures are visible at their boundaries.
- Confirm every semantic production change has evidence appropriate to its change type; runtime behavior changes still require behavioral evidence.
- Confirm formatters, analyzers, focused tests, and required integration checks passed.
- Report every blocker from the review rubric; do not downgrade a blocker to a warning for convenience.
- Confirm the diff is complete, cohesive, and preserves repository-native conventions.

## Common Mistakes

- Treating the brief as generic ceremony instead of naming the actual boundary and risk.
- Wrapping malformed input in `null`, a sentinel, or a broad exception that erases the cause.
- Adding interfaces, factories, helpers, or configuration knobs before a real boundary exists.
- Compressing control flow until ownership or failure paths are difficult to trace.
- Approving snapshots without reading the semantic change.
- Manufacturing a failing test for a behavior-preserving refactor instead of recording a characterization baseline.
- Testing mocks or internal calls instead of behavior.
- Restyling unrelated code.

## Sources and Adaptation

This standard adapts public Jane Street engineering themes—uniform interfaces, explicit failure, strong representations, cohesive tested changes, and careful review—to the language and repository in scope. Consult the linked primary sources in `references/design-and-api.md`; use them as rationale, not as a substitute for the concrete rules in this skill.
