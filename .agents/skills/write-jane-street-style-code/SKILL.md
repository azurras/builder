---
name: write-jane-street-style-code
description: Apply the house coding standard to implementation or read-only review of code, tests, scripts, migrations, code-bearing configuration and executable examples.
---

# Coding and Review Standard

Use repository-native conventions and tools. Keep invalid states out of trusted code, interfaces consistent, effects explicit, errors causal, and changes cohesive.

## Implementation
Reuse the current plan's Before-Edit Brief or write a short one: Behavior, Invariants, Boundary/API, Effects and failures, Tests and evidence. Resolve contradictions through inspection before editing; revise only when assumptions change.

Choose evidence that can disprove the claim:
- Behavior changes/bugs: observe a failing regression or focused behavioral test, then the passing result.
- Type constraints/static corrections: reproduce the compiler/analyzer finding.
- Behavior-preserving refactors: passing characterization before and after; do not manufacture failures.
- Configuration/migrations/executable examples: relevant validator, dry-run or reproducible failure, followed by passing and applicable runtime/recovery evidence.

Test supported behavior at the narrowest meaningful boundary. Run required formatters, analyzers and risk-appropriate integration checks. Once adequate checks pass, repeat only when relevant changes or uncertainty justify it.

## Review
Review requests remain read-only unless edits are authorized. Inspect requirements, diff, callers, boundary/failure behavior, compatibility and verification. Reconstruct missing context from evidence; do not start delivery or persist findings without authority.

Report findings by severity with location, violated contract, concrete evidence and required correction. Blockers are correctness, security, contract or required-evidence gaps; warnings are actionable maintenance/design costs. Never downgrade blockers to finish or invent findings. If none remain, state evidence reviewed and genuine verification gaps.

## Selective References
Load only details needed beyond the rules above:
- [Design/API](references/design-and-api.md): state, boundary, concurrency, compatibility or performance decisions.
- [Testing/review](references/testing-and-review.md): test selection or detailed evidence review.
- Language-specific constraints for touched code: [Java](references/java.md), [JavaScript/TypeScript](references/javascript.md), [Python](references/python.md).
- [Configuration/templates](references/templates-and-configuration.md): executable rendering or configuration risks.

Fix resolvable issues autonomously within authorized scope. Missing user authority, not an ordinary design choice, requires user input.
