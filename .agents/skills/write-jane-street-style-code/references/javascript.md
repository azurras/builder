# JavaScript and TypeScript Guidance

Apply the house standard through repository-native JavaScript or TypeScript conventions. Use the project's module system, type-checking level, formatter, linter, browser support, and test runner.

## Table of Contents

- [Decision guide](#decision-guide)
- [Boundary validation and states](#boundary-validation-and-states)
- [Interfaces and failures](#interfaces-and-failures)
- [Effects and async behavior](#effects-and-async-behavior)
- [DOM and browser boundaries](#dom-and-browser-boundaries)
- [Testing](#testing)
- [Good and bad](#good-and-bad)
- [Review checklist](#review-checklist)

## Decision Guide

| Need | Prefer | Avoid |
|---|---|---|
| External input | Parse and validate at network, storage, DOM, message, or config boundary | Trusting object shape after `JSON.parse` |
| Closed states in TypeScript | Discriminated union with exhaustive handling | Optional-field bags and boolean combinations |
| Closed states in JavaScript | Documented tagged object plus boundary validator | Magic strings spread across modules |
| Expected failure | Consistent result object or repository-standard typed error | `null`, `false`, and thrown strings for the same operation |
| Async effect | Explicit `async` boundary with cancellation/timeout policy | Floating promise or hidden fire-and-forget work |
| Shared state | One owning module/component and immutable snapshots | Cross-module mutation of exported objects |
| DOM contract | Stable selectors and explicit rendering boundary | Depending on incidental nesting or display text |

Do not add TypeScript-only patterns to a JavaScript module unless the project is intentionally migrating and the compatibility path is part of the change.

## Boundary Validation and States

- Treat `fetch` responses, `JSON.parse`, storage, query strings, DOM datasets, postMessage, worker messages, configuration, and third-party libraries as untrusted.
- Validate shape and domain constraints before core logic consumes the value.
- In TypeScript, remember that a type assertion does not validate runtime data.
- Use discriminated unions for cases that carry different fields or behavior.
- Keep optional properties for genuinely independent optional facts, not mutually exclusive modes.
- Normalize input only when the contract defines normalization; preserve distinctions that affect identity or security.
- Freeze or copy external mutable objects when ownership would otherwise remain ambiguous.

Boundary validation may use the repository's existing schema library. Do not introduce a competing validator for one endpoint.

## Interfaces and Failures

- Keep parallel exports consistent in verb, parameter order, return shape, and sync/async behavior.
- Use object parameters when several same-typed arguments are easy to swap or when optional inputs would otherwise create positional ambiguity.
- Keep result object tags stable and exhaustive: `{ ok: true, value } | { ok: false, error }` is useful only when every caller follows the same convention.
- Throw `Error` subclasses or errors with structured causes; never throw strings.
- Use `cause` where supported or attach the original error through the repository's established mechanism.
- Catch promises only where recovery, context, or boundary translation occurs.
- Distinguish legitimate absence from a rejected operation and from an unavailable service.
- Do not mix rejection, thrown exceptions, `undefined`, and sentinel objects for parallel APIs.

In JavaScript, document the return contract close to the export. In TypeScript, encode it and still validate external runtime values.

## Effects and Async Behavior

- Keep pure transformations separate from DOM, network, storage, analytics, and timer effects.
- Make async work visible in the function contract and await or return every promise unless a named owner intentionally supervises it.
- Use `AbortSignal` or the repository's cancellation mechanism for work whose caller owns the lifetime.
- Define timeout and retry policy at one boundary; avoid nested retries across layers.
- Make retries conditional on idempotency and failure class.
- Pass clock or scheduling functions when time behavior must be deterministic in tests.
- Give event listeners, intervals, observers, and subscriptions an explicit teardown owner.
- Avoid mutation of imported objects or shared caches without a single owning module and documented freshness policy.

`async` does not imply concurrency safety. State read before an `await` may be stale afterward; re-check or serialize the transition when the invariant requires it.

## DOM and Browser Boundaries

- Escape or render untrusted text through safe framework mechanisms; use raw HTML only at a reviewed sanitization boundary.
- Keep stable `data-*` hooks or semantic identifiers for scripts and tests instead of relying on incidental markup depth.
- Treat URL, history, local storage, cookies, and postMessage as boundary APIs with explicit parsing and security checks.
- Keep rendering functions deterministic from state where practical; isolate browser mutations in focused adapters or component effects.
- Clean up listeners and observers with the component or page lifecycle.
- Preserve accessibility semantics when changing interactive structure; behavior includes keyboard and assistive-technology use.

## Testing

- Use the repository's current runner and assertion style.
- Test exported behavior and boundary validation; avoid importing private helpers merely to increase coverage.
- Use table-driven cases for partitions and boundary values.
- Use a property library only when already available or justified by a substantial input space.
- Use fake timers only for behavior that genuinely depends on time, and advance them deliberately.
- Await asynchronous assertions and fail on unhandled rejections.
- Prefer a small DOM fixture and semantic queries over full-page snapshots.
- Use integration tests for browser APIs, framework lifecycle, serialization, or network contracts that unit tests cannot prove.

Snapshot only stable semantic output. Read every changed snapshot and pair critical behavior with focused assertions.

## Good and Bad

Bad: unchecked input and ambiguous async failure.

```javascript
export async function loadUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) return null;
  return response.json();
}
```

`null` conflates absence and infrastructure failure, and the JSON shape is trusted without boundary validation.

Good: boundary outcomes are explicit.

```javascript
class UserServiceProtocolError extends Error {
  constructor(message, options) {
    super(message, options);
    this.name = "UserServiceProtocolError";
  }
}

export async function loadUser(id, { signal, request = fetch }) {
  const response = await request(`/api/users/${encodeURIComponent(id)}`, { signal });
  if (response.status === 404) return { ok: false, error: { kind: "not-found" } };
  if (!response.ok) throw new Error(`user request failed: ${response.status}`);

  let body;
  try {
    body = await response.json();
  } catch (cause) {
    throw new UserServiceProtocolError("user service returned invalid JSON", { cause });
  }

  const parsed = parseUser(body);
  if (!parsed.ok) {
    throw new UserServiceProtocolError("user service returned invalid user data", {
      cause: parsed.error,
    });
  }

  return { ok: true, value: parsed.value };
}
```

Use this shape only if it matches neighboring APIs. Here, not-found is an ordinary caller-visible outcome; malformed remote data is an upstream protocol fault with preserved context. The other important decisions are visible cancellation and an injectable external effect.

## Review Checklist

- Does runtime boundary validation exist independently of TypeScript assertions?
- Do tagged states prevent impossible optional-field combinations?
- Are parallel exports consistent about promises, results, and thrown faults?
- Is every promise awaited, returned, or owned by a named supervisor?
- Are retries, cancellation, listeners, timers, and teardown explicit?
- Is DOM mutation isolated and untrusted content escaped?
- Are tests semantic and stable rather than snapshot-heavy?
- Does the change preserve repository-native browser and module compatibility?
