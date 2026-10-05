# Sources and Adaptation

This is an original house standard adapting public Jane Street engineering principles to every language. Its concrete recipes and good/bad examples are written for this skill. The user's sentence-like code, complementary parameter naming, descriptive variable naming, and distinct bindings for changed data meanings are explicit house requirements.

## Primary Sources

- [How Jane Street Does Code Review, Ian Henry](https://www.janestreet.com/tech-talks/janestreet-code-review/): review coverage follows changed content, including changes introduced by merges and rebases. The skill applies that idea through revision-aware review and appropriate scrutiny.
- [Core Principles: uniformity of interface, Yaron Minsky](https://blog.janestreet.com/core-principles-uniformity-of-interface/): predictable interfaces reduce relearning and repeated arbitrary decisions. The house adaptation asks readers to inspect neighboring APIs and keep naming, parameter order, units, results, and failure conventions coherent.
- [How to fail: introducing Or_error.t, David House](https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/): useful error results carry information that callers and operators need. The skill implements this using native result or exception conventions and preserved causal context.
- [Testing with expectations, Yaron Minsky](https://blog.janestreet.com/testing-with-expectations/): concrete scenarios can place inputs and observed outputs together. The house evidence guide uses small deterministic scenarios and requires inspecting changed expected output.

## Scope of the Adaptation

The supplied talk describes a review process and its tools. This skill supplies additional house coding rules, language adaptation, and original examples to satisfy the user's broader request. It does not claim to reproduce a complete official Jane Street manual for all languages.

Use the local rules to make a concrete decision. Use these links for rationale. Repository instructions and the user's scope still govern authority, persistence, review ownership, and publication; the talk's collaborative editing practices do not grant permission to mutate a review-only task.
