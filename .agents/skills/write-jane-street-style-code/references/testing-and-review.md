# Testing and Review Standard

Use this reference for every behavior change, bug fix, refactor, test change, and code review. Tests are executable explanations of the contract; review is an independent search for incorrect assumptions, hidden effects, and needless complexity.

## Table of Contents

- [Testing sequence](#testing-sequence)
- [Evidence by change type](#evidence-by-change-type)
- [Test-selection matrix](#test-selection-matrix)
- [Choose the boundary under test](#choose-the-boundary-under-test)
- [Require semantic-change evidence](#require-semantic-change-evidence)
- [Write examples and boundaries](#write-examples-and-boundaries)
- [Use property and generative tests](#use-property-and-generative-tests)
- [Use scenario, expect, and snapshot tests](#use-scenario-expect-and-snapshot-tests)
- [Use integration and contract tests](#use-integration-and-contract-tests)
- [Test concurrency and time](#test-concurrency-and-time)
- [Control doubles and fixtures](#control-doubles-and-fixtures)
- [Review process](#review-process)
- [Blockers](#blockers)
- [Warnings](#warnings)
- [Finding format](#finding-format)
- [No-finding outcome](#no-finding-outcome)
- [Primary sources](#primary-sources)

## Testing Sequence

For implementation work:

1. State the behavior and risk in the Before-Edit Brief.
2. Select the narrowest public boundary that can prove it.
3. Select the starting evidence from Evidence by Change Type.
4. Run it and inspect the result before editing production code.
5. Implement the smallest change that satisfies or preserves the stated contract.
6. Add only the boundary, property, integration, or concurrency coverage justified by remaining risk.
7. Run focused tests, then the repository's proportionate regression suite.
8. Inspect the production and test diff together.

Follow `superpowers:test-driven-development` for features, bug fixes, and behavior changes. This reference selects evidence for type-level work, analyzer corrections, behavior-preserving refactors, and non-source artifacts without manufacturing a behavioral failure.

## Evidence by Change Type

| Change type | Starting evidence | Completion evidence |
|---|---|---|
| Feature, behavior change, or bug fix | Failing behavioral test or existing regression | The same test passes, relevant boundary coverage passes, and the regression suite remains green. |
| Type-level contract | Compiler or type-check failure | The intended invalid program is rejected and valid runtime behavior remains covered. |
| Static policy or analyzer correction | Reproduced analyzer finding | The finding is absent and semantic behavior is tested when it changed. |
| Behavior-preserving refactor | Passing characterization baseline | The same observable contract passes after the refactor; add characterization coverage before editing when necessary. |
| Configuration, migration, or executable example | Failing validator, dry-run, migration check, compilation, or reproducible command | The same artifact-level command passes plus any required runtime or rollback evidence. |
| Code review | Supplied tests, commands, diff, and reviewable contract | Non-mutating verification and findings; review does not manufacture RED evidence or edit code. |

RED evidence is required when the claim is that behavior, a type constraint, a static rule, or an executable artifact is currently wrong. A pure behavior-preserving refactor starts from a green characterization baseline because the claim is preservation.

## Test-Selection Matrix

| Risk or question | Primary test shape | Add when needed | Common mistake |
|---|---|---|---|
| Representative business rule | Focused example test | Boundary examples | Asserting private calls instead of result. |
| Parsing or validation | Valid, invalid, and boundary examples | Property/generative coverage | Testing only happy-path syntax. |
| Large input space or algebraic law | Property or generative test | Minimal named examples | Generating data that cannot reach important states. |
| Multi-step workflow or diagnostic trace | Scenario or expect test | Focused assertions for critical fields | Approving a changed trace without reading it. |
| Stable structured rendering | Targeted snapshot | Semantic assertions | Snapshotting volatile or irrelevant output. |
| Database, HTTP, filesystem, serialization, or queue boundary | Integration or contract test | Unit tests for pure core behavior | Mocking the boundary's actual contract. |
| Compatibility or migration | Old/new contract matrix | Round-trip or replay fixtures | Proving only the new reader or writer. |
| Concurrency, retry, timeout, or cancellation | Deterministic concurrency test | Stress test as supplemental evidence | Sleeping and hoping ordering occurs. |
| Performance claim or capacity invariant | Benchmark or bounded measurement | Profiling evidence | Timing a noisy end-to-end path once. |
| Security boundary | Negative and authorization tests | Integration test at enforcement point | Testing validation but not bypass paths. |

Use the smallest set of test shapes that covers the actual risks. More tests are not automatically better; redundant brittle tests can obscure the contract.

## Choose the Boundary Under Test

Default to the narrowest public or module boundary whose result proves the behavior. Public means the supported boundary for its consumer, not necessarily a language-level `public` keyword.

- Test a pure domain function directly when it owns the rule.
- Test a service boundary when orchestration, transactionality, or effect sequencing is the behavior.
- Test an HTTP or UI boundary only when serialization, routing, authorization, rendering, or integration is part of the contract.
- Avoid reaching through several layers solely because the highest-level test is convenient.
- Avoid testing private helpers independently when their behavior is fully expressed through a stable boundary.

If a test needs extensive mocking or detailed knowledge of internal call order, reconsider the production boundary. A difficult-to-test interface is often difficult to use safely.

## Require Semantic-Change Evidence

Every semantic production change must have observable evidence appropriate to the change type. For runtime behavior, meet this rule in one of two ways:

1. Add or change a test, witness it fail, and then make it pass; or
2. Record that an existing test failed before the production edit and passes afterward, including the failing behavior it proved.

A formatting-only or comment-only change has no semantic production change. A behavior-preserving refactor requires a passing characterization baseline before and after; add characterization coverage first when existing coverage is insufficient, but do not manufacture a failure.

Do not claim that compilation alone proves runtime behavior unless the entire change is a type-level constraint and the compiler failure was the explicit RED evidence.

## Write Examples and Boundaries

Use named examples to make the contract readable:

- One ordinary valid case.
- The smallest and largest meaningful boundary values.
- Each distinct failure category that callers handle differently.
- A regression example that would have caught the reported bug.
- Empty, missing, duplicated, malformed, or reordered inputs when relevant.

Name the behavior and condition: `rejects_end_before_start`, not `test_validation_2`.

Avoid combining unrelated behaviors in one test. If the test name contains several “and” clauses, split it unless the sequence itself is the behavior.

## Use Property and Generative Tests

Use property-based or generative testing when the state space is larger than a handful of meaningful examples or when behavior follows a law.

Good candidates include:

- Parse/print or serialize/deserialize round trips.
- Ordering, equality, normalization, and comparison laws.
- Validated constructors and state transitions.
- Collections under arbitrary sizes and duplicates.
- Protocol encoders/decoders.
- Idempotency, monotonicity, reversibility, or conservation properties.

Define generators in terms of the domain. Generate valid values directly when testing a property over valid states; generate invalid partitions deliberately when testing rejection. Ensure failures shrink to a readable counterexample.

Keep at least one named example for reader orientation. Properties complement examples; they do not replace a clear explanation of representative behavior.

## Use Scenario, Expect, and Snapshot Tests

Scenario or expect tests are valuable when the important output is a multi-step trace, structured diagnostic, rendering, command transcript, or workflow state. They can serve as executable documentation because inputs and observed outputs remain adjacent.

Use them when:

- A sequence is easier to understand as a complete story.
- Many related output fields must be inspected together.
- Diagnostic quality is part of the behavior.
- Exploring a new behavior benefits from seeing the actual output before narrowing assertions.

Snapshot safeguards:

1. Keep the scenario small and deterministic.
2. Remove timestamps, random identifiers, order instability, and unrelated fields.
3. Read the entire diff before accepting it.
4. Add focused semantic assertions for safety-critical or easy-to-overlook facts.
5. Never bulk-update snapshots merely to make CI green.

A large snapshot that changes on unrelated implementation details is not a contract; it is review noise.

## Use Integration and Contract Tests

Use integration evidence where correctness depends on a real boundary behavior that a unit test cannot establish:

- Database constraints, transactions, indexes, queries, and migrations.
- HTTP serialization, routing, authentication, and status mapping.
- Framework binding or lifecycle behavior.
- Filesystem permissions and path behavior.
- Message schemas, queue semantics, and third-party API compatibility.
- Template escaping and browser-visible structure.

Keep pure domain rules in faster focused tests as well. Integration tests should prove the seam, not re-test every internal branch through a slow environment.

For external providers that cannot run locally, use the provider's published contract or a recorded sandbox response, then state the unverified gap honestly.

## Test Concurrency and Time

Make concurrency tests deterministic:

- Inject or control clocks, schedulers, deadlines, and randomness when the repository supports it.
- Coordinate with barriers, latches, events, promises, or explicit task handles.
- Assert ownership, ordering, cancellation, timeout, retry count, idempotency, or final state directly.
- Test the losing and winning sides of a race when both outcomes are valid.
- Bound every wait and surface diagnostic state on timeout.

Do not use arbitrary sleeps as the primary synchronization mechanism. Stress loops may supplement a deterministic invariant test, but a test that passes only probabilistically is weak evidence.

## Control Doubles and Fixtures

Use a real implementation when it is fast, deterministic, and local. Use a fake when a small in-memory implementation faithfully represents the contract. Use a mock only when the interaction itself is the behavior or no practical fake exists.

Rules:

- Do not mock code you do not understand.
- Do not reproduce the production algorithm inside the test expectation.
- Assert meaningful effect requests, not every incidental call.
- Keep fixtures small enough that a reviewer can see why each field matters.
- Prefer builders or factories that produce valid defaults, with explicit overrides for the behavior under test.
- Prevent shared mutable fixtures from leaking state between tests.

## Review Process

Review production and tests as one change:

1. Restate the behavior, invariants, boundary, effects/failures, and evidence from the brief.
2. Read the smallest relevant context around the diff, including parallel interfaces and callers.
3. Trace untrusted input to the validation boundary and trusted representation.
4. Trace each effect and failure to its owner and caller-visible contract.
5. Check the test-selection matrix against the risks.
6. Run or verify the stated commands when practical.
7. Classify findings as blockers or warnings using the definitions below.
8. Confirm the change is cohesive and excludes unrelated work.

Review for correctness first, then clarity, maintainability, and style. Repository-native tooling decides mechanical formatting.

## Blockers

Report a blocker when merge or completion would leave a correctness, contract, or evidence gap:

- Invalid states can cross a validation boundary into trusted code.
- A security or authorization boundary can be bypassed.
- Effects, mutation ownership, blocking work, or failure behavior are hidden from callers that must reason about them.
- Parallel APIs use inconsistent names, arguments, results, or failure conventions without a domain reason.
- Expected domain failure is confused with absence, programmer error, or infrastructure failure.
- Original error context required for diagnosis is discarded.
- Concurrency lifetime, ordering, cancellation, retry, or idempotency is undefined where callers depend on it.
- A semantic production change lacks observed RED/GREEN evidence.
- Tests assert incidental implementation or mocks while the real behavior remains unproved.
- A compatibility surface changes without migration or consumer evidence.
- The diff contains unrelated behavior or refactoring that prevents safe review.
- Required formatters, analyzers, tests, or integration checks fail.

Do not downgrade a blocker because the issue seems unlikely or the deadline is close. Either correct it or record the work as blocked with the missing evidence.

## Warnings

Report a warning when the change may be correct but carries avoidable design or maintenance cost:

- An abstraction protects no invariant, isolates no effect, and has no demonstrated reuse.
- Names hide units, ownership, remote work, or domain meaning.
- Error messages are vague even though causal data remains available.
- Performance costs or cardinality assumptions are surprising but bounded.
- Tests duplicate coverage, depend on volatile output, or use oversized fixtures.
- A snapshot is broader than the behavior under review.
- Comments repeat syntax or are likely to drift from the actual constraint.
- Compatibility cleanup lacks a named removal condition.
- Local mutation is safe but its owner is harder to identify than necessary.

Warnings should still be actionable. Do not use them for personal style preferences already governed by repository conventions.

## Finding Format

Write every finding in this shape:

```markdown
[Blocker|Warning] Short outcome-focused title
Location: path and tight line range
Contract: violated behavior, invariant, boundary, effect/failure rule, or evidence requirement
Evidence: concrete execution path, counterexample, failing command, or missing proof
Required change: smallest correction or evidence needed
```

Lead with the consequence, not a vague label. “Concurrent refresh can publish stale state” is better than “possible race.” Include enough evidence that the author can reproduce or reason about the issue without guessing.

## No-Finding Outcome

When no actionable findings remain, say so directly and report:

- Commands or evidence reviewed.
- Any unverified runtime or external-system gap.
- Residual risks that are acceptable but worth preserving.

Do not invent findings to make a review look thorough.

## Primary Sources

- [Ironing out your development style](https://blog.janestreet.com/ironing-out-your-development-style/)
- [Testing with expectations](https://blog.janestreet.com/testing-with-expectations/)
- [The joy of expect tests](https://blog.janestreet.com/the-joy-of-expect-tests/)
- [Jane Street code review](https://www.janestreet.com/tech-talks/janestreet-code-review/)
- [What the interns have wrought: property testing](https://blog.janestreet.com/what-the-interns-have-wrought-2022/)

These sources motivate the emphasis on small changes, executable examples, properties, and high-scrutiny review. Apply the concrete Builder standard above through the repository's own testing tools.
