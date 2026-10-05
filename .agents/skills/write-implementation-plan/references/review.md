# Review Mode

Run validate mode, then review whether the work is executable, appropriately scoped and honestly recorded. Lead with concrete blockers and their section, task or file references.

## Review Contract

Reject the plan when:

- Background does not explain why the change is needed, or Goals and Objective describe activity rather than outcomes.
- A non-goal has no reason, or obvious adjacent work is neither a goal nor a non-goal.
- An acceptance criterion is not observable or testable, the criteria omit the delivery boundary, or a goal has no criterion that proves it.
- Design names no alternative where a real choice existed, or a decision has no reason.
- Expected Changes and the Task Breakdown disagree about which files or areas change.
- The Test Plan maps an AC only to evidence that cannot detect its failure, or relies on unit tests alone where runtime proof is required.
- A task has neither an inspected file/symbol contract nor a valid legacy Code Edit block.
- Targets, dependencies, acceptance checks, risks, or rollback are vague or unresolved for the proposed ready state.
- A code-changing task omits `Required skill: write-chris-street-style-code` before code edits or its task-specific Before-Edit Brief: Behavior, Invariants, Boundary/API, Effects and failures, Tests and evidence.
- Claimed inspection is unsupported by the actual files/callers, or the branch has changed in a way that invalidates the contract.
- Any change in an application repository lacks a plan to run and verify the candidate locally with verify-local-app and publish runtime evidence before PR creation, including draft PRs, regardless of language; runtime-affecting edits lack affected reruns before PR updates. Work with no runnable application lacks appropriate native checks or a concrete reason runtime execution is not applicable.

For an in-progress or complete plan, also reject it when:

- The diff or evidence shows a divergence (files, design, tests, scope) that the sections and Implementation Log do not record.
- A log entry rewrites history instead of appending a correction, or a scope change lacks the authority that decided it.
- A complete plan's Outcome does not report each acceptance criterion with its result and evidence, or claims results the evidence does not show.

Warn, without blocking, when a new plan ignores the [presentation conventions](plan.md#presentation): bare label lines that GitHub runs together, comparable facts in prose instead of a table, or a missing Objective or Outcome callout.

Review historical v1 and legacy plans against their original contract; do not reject them for lacking v2 sections. Exact line ranges and replacement code are optional for inspected task contracts. When literal Code Edit blocks are used, check the supplied range and code against the inspected file.

## Outcome

Report blockers, actionable warnings, and `ready | not ready`. Explain the violated contract and the smallest correction needed. When ready, name the evidence reviewed and any remaining accepted risk. Reinspect changed targets at execution time instead of treating old line numbers as authoritative.

Do not change files or start execution in review-only scope.
