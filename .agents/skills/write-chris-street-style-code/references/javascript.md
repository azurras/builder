# JavaScript and TypeScript

Follow repository lint, module, browser-target, and test conventions. This guide applies the shared rules and the [principles](jane-street-principles.md) to JavaScript, TypeScript, Node, and browser code. JavaScript gives few guarantees by default: values are loosely typed at runtime, promises can be forgotten, and the DOM is a security boundary. The style compensates by validating at runtime boundaries, modeling states as tagged unions, owning every promise and listener, and keeping TypeScript honest (types describe values that were actually checked).

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| `unknown` at boundaries, then a validator that returns a typed value | `any`, or `as User` on parsed JSON | A cast is a promise the compiler cannot check; a validator keeps it |
| Discriminated unions with a `kind` field and an `assertNever` default | Several optional fields and booleans describing one state | Impossible combinations cannot be built, and new states fail type-checking |
| String literal unions or `as const` objects | Bare string comparisons scattered through the code | Typos become compile errors |
| Branded or wrapper types for IDs that are easy to swap | Several `string` ID parameters | Swapped IDs fail type-checking |
| `===` and explicit checks: `value === undefined`, `Number.isFinite(value)` | `==`, and truthiness checks on numbers or strings | `0`, `""`, and `NaN` are valid or invalid for different reasons |
| One meaning for `null` and one for `undefined`, documented per module | Mixing them, or `?? ""` to hide missing data | Absence stays distinguishable from empty |
| `await` or `return` every promise; `for...of` with `await`, or `Promise.all` for intended concurrency | Floating promises, `forEach(async ...)` | Failures are observed and completion is real |
| `AbortController` for cancellation, and a check that a result is still current | Letting late responses overwrite newer state | Out-of-order completion is normal in UIs |
| Listener, timer, and subscription setup paired with cleanup | `addEventListener` with no removal | Leaks and duplicate handlers are hard to trace |
| `textContent`, safe templating, and URL builders | `innerHTML` with untrusted text, string-built URLs | Each output context has its own escaping rules |
| `toSorted`, spread copies, and returning new values | Mutating arguments: `sort`, `reverse`, `splice` on inputs | Callers keep their data; mutation is owned |
| Checking `response.ok` and status after `fetch` | Assuming `fetch` rejects on HTTP errors | `fetch` only rejects on network failure |
| `Error` subclasses with `{ cause }` | Throwing strings or objects; dropping the cause | Stack traces and causes survive |

## Smells Reviewers Flag

- `as SomeType` applied to data from `JSON.parse`, `response.json()`, `localStorage`, `postMessage`, or the DOM.
- `any` outside a narrow, commented interop seam; `// @ts-ignore` without an explanation and a tracking reason.
- An async call with no `await`, `return`, or `.catch`; `array.forEach(async ...)`.
- `if (!count)` where `count` may legitimately be `0`; `value || defaultValue` where `0` or `""` is valid (use `??`).
- Optional chaining on values that must exist: `order?.customer?.email` hides a bug instead of failing.
- `innerHTML`, `outerHTML`, `insertAdjacentHTML`, or `document.write` with any non-constant string.
- A `useEffect`, `addEventListener`, `setInterval`, or subscription with no cleanup.
- `array.sort()` on numbers without a comparator (it sorts as strings), or on a caller's array.
- `fetch` followed by `response.json()` without checking `response.ok`.
- Module-level mutable state shared across requests in a server.
- `catch (error) { return null; }` or `catch {}` around anything but a deliberately optional operation.

## Good and Bad Pairs

The cross-language catalogue has JavaScript and TypeScript pairs for [protocol failures and transformations](good-and-bad-examples.md#4-preserve-failure-categories-and-name-each-transformation), [tagged state](good-and-bad-examples.md#10-one-tagged-state-instead-of-loose-flags), [named stages](good-and-bad-examples.md#16-named-stages-instead-of-a-clever-chain), and [late async results](good-and-bad-examples.md#21-late-async-results-must-not-overwrite-newer-state). The pairs below are JavaScript-specific.

### Promise Ownership

Bad integration fragment (`userRepository` is the application's effect boundary):

```javascript
function saveUserTo(user, userRepository) {
  userRepository.save(user);
  return { saved: true };
}
```

This reports success before persistence succeeds and loses the rejection.

Good integration fragment:

```javascript
async function saveUserTo(user, userRepository) {
  const savedUser = await userRepository.save(user);
  return savedUser;
}
```

The caller must await or return the operation. A rejected save remains a failure, and `savedUser` describes the persisted result. Do not add catch-and-success around this boundary.

### A Cast Is Not a Validator

Bad (TypeScript fragment):

```typescript
const user = (await response.json()) as User;
sendWelcomeEmailTo(user.email.toLowerCase());
```

If the server returns `{ "error": "not found" }`, the code crashes far from the cause, or worse, sends mail to `undefined`.

Good (complete TypeScript example):

```typescript
type User = { id: number; email: string };

class UserShapeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "UserShapeError";
  }
}

function parseUserFrom(decodedJson: unknown): User {
  if (typeof decodedJson !== "object" || decodedJson === null || Array.isArray(decodedJson)) {
    throw new UserShapeError("User must be a JSON object");
  }
  const candidateFields = decodedJson as Record<string, unknown>;
  if (!Number.isSafeInteger(candidateFields.id) || (candidateFields.id as number) <= 0) {
    throw new UserShapeError("User id must be a positive integer");
  }
  if (typeof candidateFields.email !== "string" || !candidateFields.email.includes("@")) {
    throw new UserShapeError("User email must be a string containing @");
  }
  return { id: candidateFields.id as number, email: candidateFields.email };
}
```

The boundary accepts `unknown`, every field is checked before the `User` type is claimed, and the error says which rule failed. The narrow `as Record<string, unknown>` only reads fields that are then checked. Use the repository's schema library (such as Zod or Valibot) if it has one; the rule is the same.

Check: a valid object parses; `null`, arrays, a missing `id`, `id: 0`, and a malformed email each throw `UserShapeError`.

### Truthiness Is Not Validation

Bad (complete JavaScript example):

```javascript
function quantityLabelFor(quantity) {
  if (!quantity) {
    return "Quantity required";
  }
  return `Qty ${quantity}`;
}
```

`0` is a valid quantity for a zero-stock line but is reported as missing. `NaN` is also reported as missing instead of invalid, and `"abc"` renders as "Qty abc". One truthiness check is answering three different questions.

Good (complete JavaScript example):

```javascript
function quantityLabelFor(quantity) {
  if (quantity === undefined) {
    return "Quantity required";
  }
  if (!Number.isSafeInteger(quantity) || quantity < 0) {
    throw new RangeError(`Quantity must be a non-negative integer, got ${String(quantity)}`);
  }
  return `Qty ${quantity}`;
}
```

Absence and invalid values are distinct outcomes, and `0` is accepted because the domain allows it.

Check: `undefined` returns the prompt; `0` returns "Qty 0"; `-1`, `1.5`, `NaN`, and `"3"` throw `RangeError`.

### Loops with Async Work

Bad (JavaScript fragment):

```javascript
invoiceIds.forEach(async (invoiceId) => {
  await invoiceClient.send(invoiceId);
});
console.log("All invoices sent");
```

`forEach` ignores the returned promises. The message prints before anything is sent, and failures become unhandled rejections.

Good (complete JavaScript example):

```javascript
async function sendInvoicesInOrder(invoiceIds, invoiceClient) {
  const sentInvoiceIds = [];
  for (const invoiceId of invoiceIds) {
    await invoiceClient.send(invoiceId);
    sentInvoiceIds.push(invoiceId);
  }
  return sentInvoiceIds;
}

async function sendInvoicesConcurrently(invoiceIds, invoiceClient) {
  await Promise.all(invoiceIds.map((invoiceId) => invoiceClient.send(invoiceId)));
  return invoiceIds;
}
```

Choose deliberately: sequential when order or rate limits matter, `Promise.all` when concurrency is safe and bounded by a small input. The caller awaits the result, and the first failure rejects. For large inputs, use a concurrency limit; use `Promise.allSettled` only when partial success is part of the contract and each failure is reported.

Check: with a fake client, the sequential version sends in order; both reject when one send fails; neither resolves before the sends finish.

### Do Not Mutate the Caller's Array

Bad (complete JavaScript example):

```javascript
function highestScoresFrom(scores) {
  return scores.sort().reverse().slice(0, 3);
}
```

`sort()` without a comparator sorts as strings, so `[9, 10, 100]` sorts to `[10, 100, 9]`, and the function returns `[9, 100, 10]` for `[9, 100, 10, 1]`. It also reorders the caller's array in place.

Good (complete JavaScript example; `toSorted` needs Node 20 or a current browser):

```javascript
function highestScoresFrom(scores) {
  const scoresFromHighest = scores.toSorted((left, right) => right - left);
  return scoresFromHighest.slice(0, 3);
}
```

The comparator sorts numbers numerically, and `toSorted` returns a new array. On older targets, copy first: `[...scores].sort(...)`.

Check: `[9, 100, 10, 1]` returns `[100, 10, 9]`; the input array is unchanged.

### HTTP Errors Are Not Network Errors

Bad (JavaScript fragment):

```javascript
const response = await fetch(`/api/orders/${orderId}`);
const order = await response.json();
```

A 404 or 500 does not reject. The code parses an error body as an order, and a crafted `orderId` such as `../admin` changes the path.

Good (JavaScript fragment):

```javascript
const orderUrl = new URL(`/api/orders/${encodeURIComponent(orderId)}`, window.location.origin);
const response = await fetch(orderUrl, { signal: abortSignal });
if (response.status === 404) {
  return null;
}
if (!response.ok) {
  throw new OrderRequestError(`Order request failed with HTTP ${response.status}`);
}
const decodedOrderFields = await response.json();
const order = parseOrderFrom(decodedOrderFields);
```

The ID is encoded for a path segment, "not found" is legitimate absence, other statuses are failures, the request can be cancelled, and the body is validated before it is trusted.

### Untrusted Text Never Becomes HTML

Bad (browser fragment):

```javascript
commentElement.innerHTML = `<strong>${comment.authorName}</strong>: ${comment.text}`;
```

A comment containing `<img src=x onerror=...>` runs script in every reader's browser.

Good (browser fragment):

```javascript
const authorElement = document.createElement("strong");
authorElement.textContent = comment.authorName;
commentElement.replaceChildren(authorElement, `: ${comment.text}`);
```

`textContent` and text nodes never parse markup. When a framework renders templates, use its escaping and avoid its raw-HTML escape hatch (`dangerouslySetInnerHTML`, `v-html`) for untrusted content.

### Every Listener Has an Owner Who Removes It

Bad (browser fragment):

```javascript
function startResizeTracking(chart) {
  window.addEventListener("resize", () => chart.redraw());
}
```

Each call adds another listener that is never removed, and the chart can never be garbage-collected.

Good (browser fragment):

```javascript
function startResizeTracking(chart) {
  const resizeTracking = new AbortController();
  window.addEventListener("resize", () => chart.redraw(), { signal: resizeTracking.signal });
  return function stopResizeTracking() {
    resizeTracking.abort();
  };
}
```

Setup returns its own cleanup, so the owner (a component unmount, a page teardown) can stop it. In React, return the cleanup from `useEffect`.

## TypeScript Notes

- Turn on `strict` when the repository allows it; never weaken it for one change.
- Keep types truthful: a field typed `string` must never be `undefined` at runtime. If it can be absent, say `string | undefined` and handle it.
- Use `satisfies` to check a literal against a type without widening it.
- Prefer string literal unions to `enum` unless the repository already uses enums.
- Brand IDs when swaps are real risks: `type CustomerId = string & { readonly brand: "CustomerId" }`, created only by a validating function.
- Type errors are evidence. Do not silence them with `as`, `!`, or `@ts-ignore` to finish a change.

## Implementation Recipe

1. Inspect supported browser and Node targets, module conventions, TypeScript strictness, formatter, and tests.
2. Treat external values as untrusted at runtime. TypeScript `as User` is a cast, not a validator. Validate the shape and domain rules before creating a trusted value; give raw, parsed, and validated values distinct names.
3. Use discriminants for alternatives, one documented meaning for `null` and `undefined`, and explicit failure causes. Keep transport failure distinct from a missing domain object.
4. Read actual calls with their receiver and arguments: `sendInvoiceTo(invoice, recipient)`. For several positional values of the same type, use clearly named variables and a small options object when it improves the real contract.
5. Own asynchronous work. Await or return promises, observe rejection, propagate cancellation, and prevent stale responses from replacing newer state. Pair listener, timer, and subscription setup with removal.
6. Check lint, type, and syntax evidence and observable behavior. Exercise the browser when focus, DOM updates, navigation, accessibility, event order, or cleanup is the changed contract.

## Testing in JavaScript

- Test through public functions and rendered output, not component internals.
- Use fake timers or controlled promises for ordering; never `setTimeout` in tests to "wait a bit".
- For UI, query by role and accessible name, which also tests accessibility.
- Snapshot only small, stable output, and read every changed snapshot before accepting it.
- Run browser behavior in a real browser when focus, layout, or event order is the contract.

## Evidence and Review

Use the complete [user-decoding example](good-and-bad-examples.md#4-preserve-failure-categories-and-name-each-transformation) for parse and shape validation with preserved causes. For UI work, review event ordering and stale-state cleanup as well as the happy path. Escape for the actual DOM, URL, or script context; JSON encoding alone does not make data safe for every context. Check runtime support for newer features such as `Error` causes and `toSorted`.
