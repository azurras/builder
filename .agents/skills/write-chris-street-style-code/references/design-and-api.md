# Design and API

Apply these decision rules through native language mechanisms. The [paired examples](good-and-bad-examples.md) demonstrate state validation, failure classification, transformations, and effect boundaries. Consult [language adaptation](language-adaptation.md) for an unlisted language.

## Decide in This Order

1. State the observable behavior and supported inputs.
2. List valid states, forbidden combinations, and allowed transitions.
3. Identify the point where untrusted input becomes a trusted domain value.
4. Identify the interface its actual consumers use and inspect related interfaces.
5. List distinct absence and failure cases and what the caller can do about each.
6. Identify mutation, I/O, time, concurrency, resource owners, and cleanup.
7. Choose the smallest native representation enforcing these decisions.
8. Check compatibility and cost before introducing abstractions or optimizations.

## Represent States and Invariants

**Do:** write down the invariant, then enforce it at construction or a trusted transition. Use a constrained value or distinct alternatives when fields form one invariant. Keep construction and updates from creating invalid trusted values.

**Choose a mechanism when:** callers repeat the same validation, flags permit impossible combinations, two values must have an ordering, or a primitive hides an identity/unit. Use a validated time window for ordered endpoints; a named state for lifecycle alternatives; a unit-bearing quantity when arithmetic mixes units.

**Avoid:** partially initialized objects, arbitrary setters that break invariants, and comments promising validity while construction accepts invalid values. Use a simple boundary check when extra types would add complexity without preserving a useful guarantee.

**Verify:** ordinary valid states, each forbidden combination, boundary equality, and transitions that could invalidate a previously checked object.

## Validate at the Trust Boundary

Treat HTTP, command-line/configuration input, external files, database reads, messages, DOM data, and third-party responses as data requiring the contract appropriate to their source.

**Do:** parse syntax, validate shape and domain constraints, normalize only when the contract allows it, and return a trusted representation. Name stages distinctly: `response_text`, `decoded_fields`, `validated_order`.

**Avoid:** unchecked casts, repeated partial validation in every caller, silently repairing malformed input, or returning empty success after a parsing error. Identify the exact rejected field without leaking secrets or raw sensitive payloads.

**Verify:** malformed syntax, wrong shapes/types, missing fields, unsupported values, and valid edge cases before any dependent effect occurs.

## Keep Interfaces Uniform and Legible

Inspect neighboring APIs for established vocabulary, casing, parameter order, units, result shapes, and failure behavior. Use those conventions unless the current requirement calls for a deliberate transition. The principle's rationale is [uniformity of interface](https://blog.janestreet.com/core-principles-uniformity-of-interface/).

At each changed call site, read receiver + method + argument names as a sentence. Parameter names must express roles that complement the operation. Replace an opaque boolean mode with a domain enum or a distinct operation when callers otherwise cannot tell what it selects. Use labels or role-bearing values for easily swapped same-type arguments. Check named-parameter compatibility before renaming or reordering.

Public APIs require inspection of callers, documentation, serialization, and reflection where relevant. If callers cannot transition together, define and verify an intentional compatibility path. Keep private interfaces direct; do not create a migration layer without a consumer that needs it.

## Classify Outcomes Before Choosing Error Syntax

| Outcome | Contract | Action |
|---|---|---|
| Legitimate absence | No matching value exists | Use the established optional/null/explicit missing result |
| Domain rejection | Request is understood but violates a rule | Return a specific domain result or error that callers handle |
| Infrastructure or protocol failure | Work cannot be completed or external data violates its contract | Preserve causal context and surface failure distinctly from absence |
| Programming defect | An internal assumption or invariant is broken | Fail visibly using the native defect convention; correct the cause |

Select one coherent native mechanism at a boundary. The [explicit failure article](https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/) supplies rationale; the table is the house contract.

Catch a failure only to recover deliberately or translate it into the boundary's error vocabulary. Preserve the original cause and identify the operation. Recover only the intended category: a missing optional file can be absence, but an unreadable file is still a failure. Redact credentials and sensitive data in logs and messages. Let cancellation and interruption remain distinguishable from ordinary failure.

## Separate Decisions from Effects

Keep calculations and domain decisions independent of network, persistence, system clocks, and external commands when those effects do not define the rule. Put orchestration at a visible service/CLI/UI boundary. Pass dependencies explicitly; supply clock/randomness controls when meaningful tests need them.

For each mutation and resource, name its owner and lifetime. Acquire resources under a cleanup mechanism that runs on success, error, and cancellation. Bound transactions; avoid network waits while holding database locks. A `calculate`, `find`, or `is` name must accurately describe whether the operation is pure, reads externally, blocks, or mutates.

Verify effect ordering when ordering is part of behavior: validate before writing, commit before announcing success, and release resources after failure. Do not assert private call order merely because the implementation has several helpers.

## Own Concurrency and Background Work

Identify who starts, awaits/joins, cancels, and observes failures for every task. Make shared mutable state and synchronization explicit. Define ordering when results can arrive out of order. Decide how late results, duplicates, retries, timeouts, and partial completion affect state.

Use bounded retry policies only for failures known to be retryable; define idempotency before retrying a write. Propagate cancellation, avoid unbounded queues/work fan-out, and avoid locks across unbounded I/O. Verify required orderings with controlled signals or schedulers rather than sleeps.

## Earn Abstractions and Preserve Direct Data Flow

Start with direct code. Extract an abstraction when it removes demonstrated repetition, protects an invariant, or isolates an effect. Name that responsibility. Keep dependencies pointed toward stable domain contracts rather than hidden service locators or import-time effects.

Before adding an interface, generic type, factory, or options object, name its present consumer and the contract it simplifies. If no such consumer or invariant exists, keep the simpler implementation. Split materially different transformation stages into accurately named values rather than reusing a vague variable.

## Make Compatibility and Cost Explicit

For stored formats, schema changes, or public behavior, inspect the old and new readers/writers and deployment order. Verify the intended matrix and rollback path. For a large migration, choose bounded steps and observable progress rather than assuming one successful sample establishes completion.

Identify large scans, repeated work, remote calls, blocking, and allocations where their cost can surprise the caller. Establish a measurable baseline before claiming an optimization. Before adding caching, define key identity, invalidation, freshness, bounds, and the owner of the cache.

## Resolve Design Problems

Reinspect or redesign if you cannot distinguish valid states, expose a hidden effect, explain error outcomes, or choose a testable boundary. Those are ordinary implementation decisions within the authorized task. Request user input only for missing authority or a consequential conflict that evidence cannot resolve.
