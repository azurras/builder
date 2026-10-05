# Testing and Review

Use the current Before-Edit Brief and the entrypoint's evidence-by-change table. Each check must establish a stated claim. See the [paired examples](good-and-bad-examples.md) for result-based assertions and actionable review comments.

## Choose Evidence from the Risk

| Risk | Evidence to choose | Check that matters |
|---|---|---|
| Business rule or input validation | Focused valid, invalid, and boundary examples | The rule is actually enforced and rejection precedes effects |
| Large input space or algebraic law | Properties with domain-aware generators | Important valid/invalid partitions are reached and failures shrink meaningfully |
| Database, HTTP, filesystem, or serialization seam | Real integration or contract checks | Native constraints, transactions, status/body shape, encoding, or resource behavior |
| Compatibility or migration | Old/new readers and writers, replay or round-trip fixtures | The supported transition matrix and recovery path |
| Concurrency, retries, or timeouts | Controlled clocks/signals/schedulers with bounded waits | Ordering, cancellation, duplicates, late responses, and partial completion |
| Performance claim | Reproducible measurement and stated conditions | Actual work or cost changes while the observable contract remains valid |
| Security boundary | Negative and bypass cases at the enforcement point | Unauthorized/invalid work cannot reach the protected effect |
| Rendered or structured output | Small deterministic scenarios/snapshots plus semantic assertions | Meaningful fields and branches; every changed expected output is inspected |

Use the narrowest supported boundary that proves the claim. Test the pure rule directly; test orchestration when transactions/effect order matter; test HTTP/browser behavior when routing, serialization, accessibility, or event ordering is the contract. Do not reach through unrelated layers merely to reuse a convenient fixture.

## Build a Useful Test

1. Name the behavior and condition in ordinary domain terms.
2. Arrange the smallest realistic input demonstrating that condition.
3. Invoke the supported operation with clear parameter/argument roles.
4. Assert the observable value, error category/cause, state change, or protected absence of an effect.
5. Check that a plausible wrong implementation would fail the assertion.
6. Keep deterministic clocks, randomness, and ordering when those affect the result.

Prefer real temporary files, small faithful fakes, and explicit outcomes. Mock at an effect boundary when the external dependency is not the behavior under test. Test call order only when that order is an observable or safety-relevant contract. Avoid sleeps as synchronization and tests that restate the implementation's formula.

An example test should cover a normal case and the distinct boundary/failure partitions relevant to the change. Avoid a large suite of nearly identical assertions. Properties, integration tests, and focused examples complement one another when they establish different claims.

For concrete scenarios, keep inputs and expected outputs together and read output diffs before acceptance. This follows the rationale in [Testing with expectations](https://blog.janestreet.com/testing-with-expectations/). Remove volatile noise and add semantic assertions for important facts that a broad snapshot could obscure.

## Review Sequence

Read the trusted requirement and brief, then the complete production and test diff. Inspect callers and parallel APIs. Trace input through validation and transformations, identify effects and cleanup owners, enumerate outcomes, and look for a concrete counterexample.

Apply the naming guide at definitions and actual calls: methods and parameters must complement one another; arguments reveal roles; units are clear; transformations do not leave values under misleading old names. Inspect public keyword-argument compatibility before recommending a rename.

Check whether tests actually detect a relevant wrong outcome. Review assertions as closely as implementation. Formatters and static checks help with syntax and declared rules; semantic review must still evaluate the contract.

## Track the Content Being Reviewed

Record the reviewed revision and scope. After later edits, merges, or rebases, inspect the changed content and conflict resolutions before reusing approval. If the comparison is unclear, review the affected final change again. This applies the content-coverage principle in [How Jane Street Does Code Review](https://www.janestreet.com/tech-talks/janestreet-code-review/).

For high-impact paths, follow repository ownership and review requirements. Name the affected path and reason for scrutiny rather than requiring the same number of reviewers for every file. Review-only authority remains read-only; collaboration practices do not imply permission to write comments or code elsewhere.

## Findings and Completion

| Severity | Use when | Required response |
|---|---|---|
| Blocker | Concrete correctness, security, compatibility, unsafe effect, or required-evidence gap | Explain counterexample and correction; resolve before claiming the change complete |
| Warning | Actionable naming, maintainability, abstraction, or brittle-test cost with correctness otherwise established | Explain the cost and a specific improvement |
| No finding | Inspected evidence establishes the contract and no actionable defect remains | State reviewed revision, scope, evidence, and genuine limits |

A finding includes severity, exact file/symbol location, violated contract, concrete evidence or counterexample, and the required correction. Label a suggestion as optional when it expresses a preference with no established cost. Do not invent defects to fill a review, discount blockers to close a task, or claim peer review from self-review.

Bad: “Make this cleaner.” Good: “Warning at `copyFile` callers: two string arguments obscure direction. Use source/destination names and labels or a role-bearing value; verify the call cannot be silently reversed.”

Before approval, verify the final behavior still matches the brief, the important failure paths are covered, required checks actually ran, and later edits have not invalidated the evidence. Application runtime changes still require the repository's real runtime proof; unit tests alone cannot establish that boundary.
