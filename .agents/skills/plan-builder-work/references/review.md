# Review Mode

Run `plan-builder-work` validate mode, then review whether the work is executable and appropriately scoped. Lead with concrete blockers and their task/file references.

## Review Contract

Reject the plan when:

- A task has neither an inspected file/symbol contract nor a valid legacy Code Edit block.
- Targets, dependencies, acceptance checks, risks, or rollback are vague or unresolved for the proposed ready state.
- A code-changing task omits `Required skill: write-jane-street-style-code` before code edits or its task-specific Before-Edit Brief: Behavior, Invariants, Boundary/API, Effects and failures, Tests and evidence.
- Claimed inspection is unsupported by the actual files/callers, or the branch has changed in a way that invalidates the contract.
- Application runtime impact lacks a local verification plan; non-runtime changes lack appropriate native checks or a reason runtime testing is not applicable.
- Required verification commands or completion criteria cannot establish the proposed result.

Preserve unversioned historical literal-plan compatibility; when revising one for new execution, prefer the task-contract-v1 format and reinspect the affected scope.

Exact line ranges and replacement code are optional for inspected task contracts. Do not reject such a plan solely because the implementation has not been written. When literal Code Edit blocks are used, check the supplied range and code against the inspected file; additions may omit Current, while replace/delete/move require it.

## Outcome

Report blockers, actionable warnings, and `ready | not ready`. Explain the violated contract and the smallest correction needed. When ready, name the evidence reviewed and any remaining accepted risk. Reinspect changed targets at execution time instead of treating old line numbers as authoritative.

Return blockers, warnings, and readiness. Do not change files or start execution in review-only scope.
