# JavaScript and TypeScript

Follow repository lint, module, browser-target and test conventions.
- Validate untrusted JSON, DOM and network input at runtime; TypeScript types alone are insufficient.
- Prefer discriminated unions and exhaustive handling over flags and partially populated objects. Keep null/undefined meaning consistent.
- Own promises and background work: await/return them, handle rejections, propagate cancellation and prevent stale responses from overwriting newer state.
- Pair listener/timer/subscription setup with cleanup. Track the owner of mutable UI state.
- Treat DOM insertion, URL construction, HTML and script contexts as distinct security boundaries; use context-appropriate escaping and trusted rendering APIs.
- Exercise browser behavior when routing, focus, accessibility, event ordering or rendering changes. Keep fixtures and selectors stable without asserting private implementation details.

## Implementation Recipe

1. Inspect supported browser/Node targets, module conventions, TypeScript strictness, formatter, and tests.
2. Treat external values as untrusted at runtime. TypeScript `as User` is a cast, not a validator. Validate the shape and domain rules before creating a trusted value; give raw, parsed, and validated values distinct names.
3. Use discriminants for alternatives, one documented meaning for null/undefined, and explicit failure causes. Keep transport failure distinct from a missing domain object.
4. Read actual calls with their receiver and arguments: `sendInvoiceTo(invoice, recipient)`. For several positional values of the same type, use clearly named variables and a small meaningful parameter object when it improves the real contract.
5. Own asynchronous work. Await or return promises, observe rejection, propagate cancellation through the operation, and prevent stale responses from replacing newer state. Pair listener/timer/subscription acquisition with removal.
6. Check lint/type/syntax evidence and observable behavior. Exercise the browser when focus, DOM updates, navigation, accessibility, event order, or cleanup is the changed contract.

## Good and Bad Promise Ownership

Bad integration fragment (`userRepository` is the application's effect boundary):

```javascript
function saveUserTo(user, userRepository) {
  userRepository.save(user);
  return { saved: true };
}
```

This can report success before persistence succeeds and loses rejection ownership.

Good integration fragment:

```javascript
async function saveUserTo(user, userRepository) {
  const savedUser = await userRepository.save(user);
  return savedUser;
}
```

The caller must await or return the operation. A rejected save remains a failure, and `savedUser` describes the actual persisted result. Do not add catch-and-success around this boundary.

## Evidence and Review

Use the complete [user-decoding example](good-and-bad-examples.md#4-preserve-failure-categories-and-name-each-transformation) for parse/shape validation and preserved causes. For UI work, review event ordering and stale-state cleanup as well as the happy path. Escape for the actual DOM/URL/script context; JSON encoding alone does not make data safe for every context. Check runtime support for features such as Error causes.
