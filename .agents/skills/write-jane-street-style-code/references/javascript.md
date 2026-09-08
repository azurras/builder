# JavaScript and TypeScript

Follow repository lint, module, browser-target and test conventions.
- Validate untrusted JSON, DOM and network input at runtime; TypeScript types alone are insufficient.
- Prefer discriminated unions and exhaustive handling over flags and partially populated objects. Keep null/undefined meaning consistent.
- Own promises and background work: await/return them, handle rejections, propagate cancellation and prevent stale responses from overwriting newer state.
- Pair listener/timer/subscription setup with cleanup. Track the owner of mutable UI state.
- Treat DOM insertion, URL construction, HTML and script contexts as distinct security boundaries; use context-appropriate escaping and trusted rendering APIs.
- Exercise browser behavior when routing, focus, accessibility, event ordering or rendering changes. Keep fixtures and selectors stable without asserting private implementation details.
