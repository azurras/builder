# Status Model

Azurras uses a small canonical status set for hub work records and related coordination artifacts.

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
