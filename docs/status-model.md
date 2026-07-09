# Status Model

Builder uses a small canonical status set for hub work records and related coordination artifacts.

## Statuses

- `proposed`: Work has been identified but is not yet active.
- `active`: Work is currently in progress.
- `blocked`: Work cannot proceed without a decision, dependency, access, or external change.
- `in-review`: Work is implemented or drafted and awaiting review.
- `ready-to-close`: Work appears complete but final hub closure has not been recorded.
- `closed`: Work is complete, final state is documented, and no required action remains.

## Usage

- Use lowercase status values exactly as written.
- Prefer one current status per work record.
- Explain blockers in the same record when status is `blocked`.
- Use `ready-to-close` before `closed` when final validation or closure documentation remains.
- Use `closed` only after the relevant spoke state, reviews, decisions, and closure notes are captured.

## Artifact Statuses

Specs, implementation plans, and test reports use status values that describe document readiness:

- `draft`: The artifact is incomplete and must not be treated as authoritative.
- `ready-for-review`: The artifact is complete enough for review but not execution.
- `ready-for-execution`: The artifact is approved for implementation or validation work.
- `in-progress`: The artifact is being executed or updated.
- `blocked`: The artifact cannot proceed until a decision, dependency, access, or file inspection is complete.
- `complete`: The artifact has served its purpose and no required edits remain.
- `superseded`: The artifact has been replaced by a newer artifact. Use only for test reports or other evidence records where historical preservation still matters.

Implementation plans must not use `ready-for-execution` while any Code Edit line range is `line range pending file inspection`.
