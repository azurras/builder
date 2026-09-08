# Testing and Review

Use the entrypoint's evidence rules; do not repeat the brief or manufacture failing evidence for preservation work.

| Risk | Evidence |
|---|---|
| Business rule or input validation | Focused valid, invalid and boundary examples |
| Large input space or algebraic law | Properties with meaningful generators and minimal examples |
| Database, HTTP, filesystem or serialization seam | Real integration/contract tests at the seam |
| Compatibility or migration | Old/new readers and writers, replay or round-trip fixtures |
| Concurrency, retries or timeouts | Controlled clocks/schedulers and deterministic ordering; bound waits |
| Performance claim | Reproducible measurement with stated conditions |
| Security boundary | Negative/bypass tests at the enforcement point |
| Rendered or structured output | Narrow snapshots plus semantic assertions; inspect every changed snapshot |

Prefer real temporary files and small faithful fakes. Avoid reproducing the implementation in tests, mocking private call order or using sleeps as synchronization. Compilation alone does not establish runtime behavior.

Review production and tests together: trace inputs to validation, effects to their owner, errors to callers and changed behavior to evidence. Check branch/commit scope and neighboring consumers. A passing validator does not prove semantic correctness.

Findings include severity, tight location, violated contract, concrete counterexample/evidence and required correction. Missing required verification, unsafe effects, broken compatibility and correctness/security gaps block completion. Unsupported abstractions, vague names and redundant tests are warnings when correctness is established. Return no findings when none exist, with evidence and actual limits.

Rationale: [expectation tests](https://blog.janestreet.com/testing-with-expectations/), [review practice](https://www.janestreet.com/tech-talks/jane-street-code-review/).
