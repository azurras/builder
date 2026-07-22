# Design and API Standard

Use this reference for domain logic, state, validation, public or module APIs, error handling, effects, abstraction, concurrency, compatibility, or performance-sensitive behavior. Repository-native conventions control syntax and formatting.

## Table of Contents

- [Decision order](#decision-order)
- [Model states and invariants](#model-states-and-invariants)
- [Place validation at trust boundaries](#place-validation-at-trust-boundaries)
- [Keep interfaces uniform](#keep-interfaces-uniform)
- [Classify absence and failure](#classify-absence-and-failure)
- [Preserve error context](#preserve-error-context)
- [Expose effects and mutation ownership](#expose-effects-and-mutation-ownership)
- [Make concurrency ownership explicit](#make-concurrency-ownership-explicit)
- [Choose the smallest earned abstraction](#choose-the-smallest-earned-abstraction)
- [Keep dependency direction and data flow visible](#keep-dependency-direction-and-data-flow-visible)
- [Make performance costs legible](#make-performance-costs-legible)
- [Name domain meaning and constraints](#name-domain-meaning-and-constraints)
- [Preserve compatibility deliberately](#preserve-compatibility-deliberately)
- [Worked example](#worked-example)
- [Design review questions](#design-review-questions)
- [Primary sources](#primary-sources)

## Decision Order

Decide in this order before choosing classes, functions, or framework mechanisms:

1. Name the observable behavior.
2. List the valid states and transitions.
3. Identify untrusted inputs and the validation boundary where they become trusted.
4. Identify the public or module boundary callers use.
5. Classify absence and every important failure.
6. Identify effects, mutable owners, and concurrency owners.
7. Choose the most direct representation that enforces the preceding decisions.
8. Add an abstraction only if it protects one of those decisions or serves demonstrated reuse.
9. Check compatibility and meaningful cost.

Do not start with a preferred design pattern. Start with the invariant and boundary it must protect.

## Model States and Invariants

### Default

Represent valid alternatives directly with the strongest idiomatic mechanism available: enums, tagged unions, sealed hierarchies, value objects, validated constructors, records, dataclasses, or narrow modules. Make illegal states unrepresentable when doing so makes callers simpler and the domain clearer.

Use a single validated type when several fields form one invariant. A `StartTime` and `EndTime` that must be ordered may belong in a validated `TimeWindow`; two unrelated timestamps let invalid states propagate.

### Decision rule

- If every caller must repeat the same check, move the check into construction or the trusted boundary.
- If cases require different behavior, model distinct cases rather than boolean combinations.
- If a value carries a unit, identity, or constrained range, use a domain name or type rather than a primitive whose meaning is inferred from position.
- If the language cannot encode the invariant economically, validate once and keep the validated representation inside trusted code.

### Avoid

- Boolean flags whose combinations include impossible states.
- Partially initialized objects.
- Primitive strings or numbers whose units and constraints are implicit.
- Setters that can break an invariant after construction.
- Comments that promise validity while the representation permits invalid values.

The goal is not maximum type machinery. The goal is for trusted code to operate on values whose important invariants already hold.

## Place Validation at Trust Boundaries

A validation boundary is the point where external or weakly typed data becomes a trusted domain value. Typical boundaries include HTTP input, command-line arguments, database rows, configuration, deserialization, messages, file content, DOM data, and third-party responses.

### Default

Parse, normalize, and validate at the boundary. Return a validated value or a structured error. Do not repeatedly revalidate the same invariant throughout the core.

### Decision rule

- Validate syntax before domain rules.
- Normalize only when the normalization is part of the contract and cannot erase meaningful distinctions.
- Collect independent user-correctable errors when the interface benefits; stop on errors that make later checks meaningless.
- Keep security checks at every relevant trust transition even when domain validation already occurred.
- Revalidate persisted data when the storage source is not guaranteed to obey the current invariant.

Boundary validation should make the core simpler. If trusted code still handles malformed variants everywhere, the boundary is leaking.

## Keep Interfaces Uniform

Uniform interfaces make related operations predictable. Parallel functions, methods, commands, endpoints, and components should share naming, argument order, return shape, optionality, and failure conventions unless a semantic difference requires otherwise.

### Default

- Use the same verb for the same operation.
- Put equivalent parameters in the same order.
- Return equivalent result shapes for equivalent outcomes.
- Use one convention for optional lookup and a visibly different convention for operations that throw or raise.
- Keep synchronous and asynchronous differences visible.
- Make batch and single-item APIs preserve the same element semantics.

### Decision rule

Before adding an API, list its nearest parallel APIs. Copy their shape unless the new operation has a domain difference you can state in one sentence. Document that difference at the boundary.

Avoid a family where `findUser` returns `null`, `findTeam` throws, and `findProject` returns a result object without a domain reason. Callers should not memorize accidents of implementation.

## Classify Absence and Failure

Classify each non-success outcome before selecting syntax:

| Category | Meaning | Default representation |
|---|---|---|
| Absence | A value legitimately may not exist. | Option/Optional/nullable type only when the type and local convention make absence explicit. |
| Expected domain failure | The operation was valid to attempt, but the domain rejected it. | Explicit result, domain error, or documented checked outcome. |
| Programmer error | A trusted invariant or API precondition was violated. | Assertion, specific exception, or impossible branch that fails loudly. |
| Infrastructure failure | I/O, service, storage, timeout, or environment failed. | Specific fault with preserved cause and operational context. |

Do not use absence for expected domain failure. “No account found” differs from “account exists but is suspended.” Do not use an expected-failure result to hide a programmer error that indicates broken trusted code.

Sentinel strings, magic numbers, empty collections, and broad `null` values are acceptable only when the surrounding API already defines that exact meaning and changing it would violate compatibility. Translate them into an explicit internal representation at the boundary.

## Preserve Error Context

Translate failures at module boundaries, but preserve error context. A useful error tells the caller what operation failed, which safe identifier or input category was involved, and retains the original cause for diagnostics.

### Default

- Catch only where you can recover, add context, or translate to the boundary contract.
- Chain or attach the original cause.
- Use structured domain error data when callers must branch.
- Redact secrets and sensitive values before logging or returning details.
- Keep user-facing messages separate from diagnostic context.

### Avoid

- Catch-all handlers that return success, `null`, or an empty value.
- Replacing a specific cause with “operation failed.”
- Logging and rethrowing at every layer, producing duplicate noise.
- Branching on error-message text when a structured type or code is available.

## Expose Effects and Mutation Ownership

Effects include I/O, storage, network calls, process execution, logging, clocks, randomness, environment access, global state, and mutation visible outside a local expression.

### Default

Keep pure transformations separate from effect execution. Give mutable state one clear owner. Pass controllable dependencies—such as clocks or service clients—through the repository's normal injection mechanism when tests or policy need control.

### Decision rule

- If a function can block or perform remote work, make that discoverable from its type, name, module, or documentation.
- If callers need atomicity, expose one operation that owns the complete transition rather than a read-modify-write sequence.
- If mutation is strictly local and simplifies the implementation without escaping, use it directly; do not manufacture abstractions merely to appear pure.
- If an effect is irreversible or externally visible, make sequencing and retry semantics explicit.

Mutation ownership should answer: who may change this value, when, under what invariant, and how observers learn about the change?

## Make Concurrency Ownership Explicit

Concurrency adds state transitions across time. Treat ordering, cancellation, timeout, retry, and idempotency as part of the API rather than implementation trivia.

### Default

- Name the owner of shared mutable state.
- Prefer message passing, immutable snapshots, transactions, or one synchronization boundary over scattered locks.
- Define whether operations are safe to retry and whether duplicate delivery is possible.
- Propagate cancellation and deadlines through layers that can honor them.
- Define ordering only where callers may rely on it.

### Avoid

- Starting background work whose lifetime has no owner.
- Holding locks across I/O or user callbacks without a proven need.
- Retrying non-idempotent operations implicitly.
- Using sleeps as synchronization in tests or production.
- Treating a race as “unlikely” instead of defining the state transition.

## Choose the Smallest Earned Abstraction

Use this ladder:

1. Direct local code.
2. Named local helper for a coherent sub-operation.
3. Focused type or module that protects an invariant or effect boundary.
4. Reusable interface after multiple real consumers need substitution.
5. Framework only when the repeated structure and lifecycle justify its cost.

Move up only when the current level causes demonstrated duplication, permits invariant drift, tangles effects, or blocks independent testing. Similar-looking code is not automatically the same concept. Duplication is often cheaper than a false abstraction whose parameters encode unrelated cases.

An abstraction earns its cost when its name states one stable concept, its interface is smaller than the details it hides, and consumers do not need to know its internals.

## Keep Dependency Direction and Data Flow Visible

Core domain decisions should not depend on UI, transport, persistence, or framework details unless the domain is genuinely defined by them. Translate external representations at adapters or module boundaries.

Prefer data flow that can be read in one direction: input becomes validated domain data, domain behavior produces a result or effect request, and an outer boundary performs external work. Cycles, ambient service lookups, and hidden global state make this difficult to reason about and test.

Do not create layers solely to satisfy a diagram. A small module may combine parsing and behavior when there is no independent boundary and the result remains clear.

## Make Performance Costs Legible

Correctness comes first, but meaningful performance behavior is part of an interface.

- Make remote calls, blocking work, unbounded iteration, large allocation, and repeated parsing discoverable.
- Avoid an innocent-looking property or helper that performs I/O or scans an entire data set.
- State cardinality and complexity assumptions when they constrain correctness or capacity.
- Measure before optimizing, and preserve the simple implementation when evidence does not justify complexity.
- When introducing caching, define ownership, freshness, invalidation, memory bounds, and failure behavior.

Performance transparency is not micro-optimization. It prevents callers from accidentally composing expensive operations as if they were cheap.

## Name Domain Meaning and Constraints

Names should reveal domain role, unit, ownership, and effect when those are not obvious.

- Prefer `timeoutMillis`, `createdAtUtc`, or a duration type over `value` or `time`.
- Prefer verbs that distinguish lookup, creation, validation, persistence, and remote fetching.
- Reserve generic names such as `data`, `item`, `manager`, and `helper` for genuinely generic roles.
- Write comments for why an invariant, compatibility rule, or surprising choice exists. Do not narrate syntax.
- Keep comments near the constraint they protect and remove them when the code no longer matches.

## Preserve Compatibility Deliberately

Treat public behavior, stored data, messages, command output, selectors used by automation, and configuration keys as compatibility surfaces.

### Decision rule

- Identify consumers before changing a shape.
- Prefer additive migration when old and new consumers overlap.
- Validate both read and write paths during a format transition.
- Remove compatibility code only when usage evidence and rollout state make removal safe.
- Do not preserve accidental behavior merely because a test asserts it; decide whether the behavior is contractual.

Compatibility shims should have a named owner, a removal condition, and tests for both sides of the transition.

## Worked Example

Suppose a deployment request arrives as strings and may be scheduled or immediate.

### Bad shape

```text
deploy(version, scheduled, scheduledAt, force) -> null or throws
```

This permits `scheduled = false` with a non-empty `scheduledAt`, hides why `null` occurs, and leaves callers to guess which exceptions are expected.

### Better shape

```text
DeploymentTiming = Immediate | Scheduled(ValidatedUtcInstant)
DeploymentRequest = ValidatedVersion × DeploymentTiming
DeployResult = Accepted(DeploymentId) | Rejected(DomainReason)

parseDeploymentRequest(untrustedInput) -> ValidationResult<DeploymentRequest>
submitDeployment(request, deploymentGateway) -> DeployResult
```

The boundary parses and validates once. Trusted code receives only valid timing states. Expected rejection is explicit. Infrastructure faults from the gateway remain faults with preserved context. Tests can cover parsing independently from the external deployment effect.

This is the target pattern: a representation that removes invalid combinations, a uniform result contract, and a narrow effect seam. Do not copy these type names when the repository has a more idiomatic equivalent.

## Design Review Questions

- What invalid state can still enter trusted code?
- Which boundary first guarantees the invariant?
- Do parallel APIs use the same names, argument order, results, and failure conventions?
- Can a caller distinguish absence, expected domain failure, programmer error, and infrastructure failure?
- Where is the original cause preserved?
- Who owns mutation and concurrent lifetime?
- Is each effect visible and controllable where required?
- What invariant or reuse justifies every abstraction?
- Does dependency direction keep domain behavior independent from delivery details?
- Could a caller mistake expensive or blocking work for a cheap local operation?
- Which compatibility surface changes, and how is migration proven?

## Primary Sources

- [Core Principles: Uniformity of Interface](https://blog.janestreet.com/core-principles-uniformity-of-interface/)
- [How to fail: introducing Or_error.t](https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/)
- [Clearly failing](https://blog.janestreet.com/clearly-failing/)
- [Why None is better than NaN and null](https://blog.janestreet.com/making-something-out-of-nothing-or-why-none-is-better-than-nan-and-null/)
- [Formal methods at Jane Street](https://blog.janestreet.com/formal-methods-at-jane-street-index/)
- [A language-oriented approach to system design](https://www.janestreet.com/tech-talks/a-language-oriented-system-design/)
- [Introducing OxCaml](https://blog.janestreet.com/introducing-oxcaml/)

These sources motivate the standard. The rules above are Builder's cross-language adaptation and remain subordinate to repository-specific correctness, security, and compatibility requirements.
