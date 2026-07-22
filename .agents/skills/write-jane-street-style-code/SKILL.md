---
name: write-jane-street-style-code
description: Use when creating, modifying, refactoring, or reviewing production code, tests, reusable scripts, migrations, code-bearing configuration, executable templates, or copy-ready implementation examples in any language.
---

# Write Jane Street-Style Code

### Overview

Before writing or modifying code, make invariants obvious, interfaces uniform, behavior testable, and the diff easy to review. Follow repository-native syntax and formatting.

**REQUIRED SUB-SKILL:** Use `superpowers:test-driven-development` for features, bug fixes, refactors, and behavior changes.

### Workflow

1. Read repository instructions, adjacent code, tests, and public interfaces.
2. State the required behavior and invariants.
3. Witness the smallest relevant failing test.
4. Implement the smallest cohesive passing change.
5. Run native formatting, static analysis, and focused tests.
6. Review the diff for clarity, correctness, and unnecessary complexity.

### House-Style Contract

- Encode valid states and invariants in types, constructors, or validated boundaries.
- Prefer small composable units with narrow and uniform interfaces.
- Keep data flow, mutation, side effects, and failure behavior explicit.
- Use precise names and straightforward control flow.
- Add abstraction only for demonstrated duplication or a protected invariant.
- Use behavior-focused tests; add property-based or generative tests when state-space coverage matters.
- Keep changes small, cohesive, and reviewable. Exclude unrelated refactors.
- Preserve local conventions unless correctness, safety, or the approved requirement demands change.

Read `references/language-adaptations.md` only for the language being changed.

### Quick Reference

| Concern | Default |
|---|---|
| State | Represent allowed cases; reject invalid construction early. |
| Interface | Match neighboring names, argument order, and return shapes. |
| Effects | Isolate I/O, mutation, clocks, randomness, and services. |
| Errors | Expose domain failures; do not hide malformed states. |
| Abstraction | Prefer direct code until reuse or an invariant justifies a boundary. |
| Tests | Assert behavior and invariants, not incidental calls. |

### Example

```java
final class Ports {
    sealed interface ParseResult permits Valid, Invalid {}

    record Valid(int value) implements ParseResult {
        Valid {
            if (value < 1 || value > 65_535) {
                throw new IllegalArgumentException("port out of range");
            }
        }
    }

    record Invalid(String message) implements ParseResult {}

    static ParseResult parse(String raw) {
        try {
            return new Valid(Integer.parseInt(raw));
        } catch (IllegalArgumentException error) {
            return new Invalid(error.getMessage());
        }
    }
}
```

Callers must handle success and failure explicitly, and `Valid` cannot contain an out-of-range port.

### Common Mistakes

- Restyling unrelated code.
- Adding abstractions that protect no invariant.
- Hiding `null`, exceptions, or malformed input behind sentinel values.
- Compressing control flow until intent is harder to review.
- Testing mocks or internal calls instead of behavior.

### Final Review

- Are invalid states rejected or unrepresentable?
- Are interfaces consistent with neighboring code?
- Are effects and failures visible at their boundaries?
- Does each abstraction earn its cost?
- Do tests demonstrate behavior and important edge cases?
- Is the diff the smallest complete change?
