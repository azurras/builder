# Design and API

- Validate external inputs at the boundary; use enums, validated values or sum types when they prevent invalid combinations. Avoid partial objects and interdependent boolean flags.
- Match neighboring API names, argument order, return shapes and failure conventions. Document intentional incompatibilities.
- Distinguish legitimate absence, domain rejection, programming defects and infrastructure failure. Catch only to recover or translate; retain causes and redact secrets.
- Give mutable state one owner. Make I/O, blocking, time and external effects visible; inject controls when tests require determinism.
- Define concurrency ordering, cancellation, retry and idempotency where callers depend on them. Own every background task; avoid locks across unbounded I/O.
- Start with direct code. Extract an abstraction only for demonstrated reuse, a protected invariant or an isolated effect. Avoid cycles and hidden service lookups.
- For stored formats and public behavior, inspect old/new consumers and verify the transition. Do not retain shims without a demonstrated compatibility need.
- Make expensive scans/remote calls explicit. Measure performance claims; define freshness, invalidation and bounds before caching.

Resolve violations through inspection or redesign before editing; they do not by themselves require user approval.

Rationale: [uniform interfaces](https://blog.janestreet.com/core-principles-uniformity-of-interface/), [explicit failures](https://blog.janestreet.com/how-to-fail-introducing-or-error-dot-t/).
