---
name: write-jane-street-style-code
description: Use when creating, modifying, refactoring, or reviewing production code, tests, reusable scripts, migrations, code-bearing configuration, executable templates, or copy-ready implementation examples in any language.
---

# Write Jane Street-Style Code

## Overview

Make invalid states difficult to express, interfaces predictable, effects and failures visible, and every semantic change easy to test and review. Apply these principles through repository-native language conventions; do not imitate OCaml syntax or replace local formatters, linters, frameworks, or security rules.

**REQUIRED SUB-SKILL:** Use `superpowers:test-driven-development` for features, bug fixes, refactors, and behavior changes.

## Mandatory Sequence

1. Read repository instructions, adjacent implementation, tests, and public interfaces.
2. Load the references selected by the routing table below.
3. Write the Before-Edit Brief.
4. Resolve contradictions or missing facts through read-only investigation.
5. Witness the smallest relevant failing test.
6. Implement the smallest cohesive passing change.
7. Run repository-native formatting, static analysis, focused tests, and proportionate integration checks.
8. Apply the review rubric in `references/testing-and-review.md` to the final diff.

Do not edit code until the required references are read and the Before-Edit Brief is coherent. If investigation changes an assumption, revise the brief before continuing.

## Before-Edit Brief

Write one concrete statement for each field. A narrow change may use one sentence per field.

- **Behavior:** State the externally observable change or behavior that must remain unchanged.
- **Invariants:** State what must always hold and which states must be rejected or made unrepresentable.
- **Boundary/API:** Name the affected public or module boundary, compatibility constraints, and neighboring interface pattern.
- **Effects and failures:** Identify I/O, mutation, time, randomness, concurrency, external services, expected failures, and unexpected faults.
- **Tests and evidence:** Name the first failing test, the risks it covers, and the final verification evidence.

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
- Confirm every semantic production change has observable test evidence or a recorded explanation that an existing failing test now passes.
- Confirm formatters, analyzers, focused tests, and required integration checks passed.
- Report every blocker from the review rubric; do not downgrade a blocker to a warning for convenience.
- Confirm the diff is the smallest complete change and preserves repository-native conventions.

## Common Mistakes

- Treating the brief as generic ceremony instead of naming the actual boundary and risk.
- Wrapping malformed input in `null`, a sentinel, or a broad exception that erases the cause.
- Adding interfaces, factories, helpers, or configuration knobs before a real boundary exists.
- Compressing control flow until ownership or failure paths are difficult to trace.
- Approving snapshots without reading the semantic change.
- Testing mocks or internal calls instead of behavior.
- Restyling unrelated code.

## Sources and Adaptation

This standard adapts public Jane Street engineering themes—uniform interfaces, explicit failure, strong representations, small tested changes, and careful review—to the language and repository in scope. Consult the linked primary sources in `references/design-and-api.md`; use them as rationale, not as a substitute for the concrete rules in this skill.
