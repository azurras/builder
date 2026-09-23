# PostgreSQL cutover retry design

## Plan Format
task-contract-v1

## Document Status
draft

## Objective
Allow a fresh PostgreSQL authority-cutover attempt after a verified pre-authority rollback without destroying or overwriting the prior attempt's journal or evidence.

## Goals
- Preserve each attempt's journal and every evidence sidecar byte-for-byte in an immutable, attempt-scoped location.
- Permit a new attempt only from a valid terminal `ROLLED_BACK` journal after confirming `authorityPublished` is false, the authority marker is absent, the MongoDB writer is unlocked, and the Mongo-backed production service is healthy.
- Keep all journal digest, sidecar digest, ACL, path/reparse-point, writer-lock, source/target identity, and 30-minute maintenance-budget checks fail-closed.
- Keep the existing command as the only production entry point; no manual journal edits or evidence deletion.

## Inputs
- Current supported command returned the existing September 22 journal: `ROLLED_BACK`, `authorityPublished=false`, release `f38554e1cc238577d24dd51eee4842d9b6c7dda2`.
- `Invoke-ProductionPostgreSqlCutover` returns immediately for `ROLLED_BACK`; it does not start another attempt.
- `docs/operations/postgresql-migration.md` currently says not to delete or rewrite the journal or sidecars.
- The September 23 bootstrap completed and read-only inspection confirmed Flyway version 27 and migration ledger tables; production `current` remained on release `e073823d14ffed0b4c113707d16c0ad0cfe1b7fa`.
- User approved the design approach: preserve/archive the terminal failed attempt intact, then permit a guarded new run.

## Branch
Implementation must start from refreshed `origin/main` in an isolated spoke worktree. The current Builder plan/review branch is `main`; no spoke edits are authorized by this design document.

## Non-Goals
- No deletion, truncation, hand-editing, or weakening validation of production evidence.
- No retry from `AUTHORITY_PUBLICATION_STARTED`, `FORWARD_RECOVERY_REQUIRED`, or any nonterminal phase.
- No changes to MongoDB/PostgreSQL data semantics, automatic deployment policy, production ACLs, or credentials.
- No new regression-test suite. Existing relevant tests and required CI may be updated/run as needed to validate the behavior.
- No MongoDB retirement or claim that the migration is complete.

## Assumptions
- The previous rollback completed its pre-authority recovery; the new attempt must independently verify the live MongoDB and website safety conditions rather than trust that historical result.
- The current 30-minute downtime approval remains in force for a properly preflighted cutover.
- The protected production migration directory is the authoritative storage boundary for attempt records.

## Open Questions
None for this design review. The implementation plan must resolve exact filesystem transaction/rollback behavior after inspecting the protected-path and atomic-write helpers on refreshed `origin/main`.

## Proposed Design and Trade-offs
Introduce per-attempt storage keyed by the validated journal lock token. Each attempt owns its journal and sidecars in a dedicated protected directory; a small protected active-attempt pointer identifies the current run. The existing flat journal and sidecars are treated as a legacy attempt and preserved byte-for-byte during a one-time migration into that layout. The next attempt is created only after validating the terminal rollback, confirming authority is absent, confirming MongoDB reports `fsyncLock:false`, confirming the Mongo-backed website is healthy, and atomically recording the new active attempt. A failed archive, pointer update, or identity check aborts before stopping writers.

This avoids overwriting fixed-name sidecars on retries and keeps post-authority recovery forward-only. Compared with deleting/resetting the journal, it retains full forensic evidence and makes each run independently verifiable. Compared with a manual operator archive, it keeps the preservation and validation rules inside the supported command. It adds filesystem protocol complexity, so compatibility with the existing journal and crash-safe pointer updates must be demonstrated before production use.

## Task Breakdown

### Task 1 - Implement attempt-scoped journal/evidence and guarded retry
Required skill: write-jane-street-style-code.
- Dependencies: this written design must be reviewed and approved; implementation plan must then be reviewed and published.
- Files: `ops/production/windows/modules/Production.PostgreSqlMigration.psm1`; `ops/production/windows/prod.ps1` only if command wiring must change; `ops/production/windows/modules/Production.Common.psm1` only if an existing protected atomic-file helper proves insufficient; `docs/operations/postgresql-migration.md`; existing `ops/production/windows/tests/Production.PostgreSqlMigration.Tests.ps1` cases only as needed.
- Symbols: `Get-ProductionPostgreSqlCutoverJournalPath`, journal read/write helpers, `Get-ProductionPostgreSqlCutoverSidecarPath`, sidecar read/write helpers, `Invoke-ProductionPostgreSqlCutover`, and the existing supported `postgres-cutover` command.
- Inspection: reviewed these symbols and current documented phase rules in the cutover worktree at `1c48b46db75d0d1d10bcb376e00020dbb3a21223`; inspect again after refreshing `origin/main` because this is not the authoritative branch.
- Behavior: preserve the terminal failed attempt and enable a new `PLANNED` attempt only after the full pre-authority recovery preconditions pass.
- Invariants: attempt evidence is immutable and digest-validated; journal/sidecar identity and protected ACL/path checks remain strict; no authority reset; after authority publication, recovery stays forward-only; automatic deployment stays paused.
- Boundary/API: existing `prod.ps1 postgres-cutover -ConfirmPostgreSqlCutover` remains the sole supported entry point and keeps its explicit confirmation requirement.
- Effects and failures: archival and new-attempt metadata writes occur before any writer stop; any partial archival/pointer failure must be recoverable without losing the prior journal or its sidecars; refuse to proceed on ambiguous authority, lock, source-health, or archive state.
- Tests and evidence: do not add a new regression-test suite. Update only existing focused cutover assertions if the interface/contract changes; run existing focused PowerShell tests, parser checks, repository CI, and production read-only preflight before the approved retry.
- Verification: prove the original journal and sidecar hashes are unchanged in the attempt archive; prove invalid/ambiguous terminal evidence cannot start another run; prove the old command starts a new attempt only from the fully verified `ROLLED_BACK` state; then use the supported command and verify the authority journal, service, listener, readiness, source/target state, and recovery outcome.

## Code Changes
None in this design-review stage. Proposed changes are limited to the production cutover journal/evidence protocol, its existing runbook, and only the existing contract assertions needed for compatibility.

## Files and Modules
The behavior is concentrated in `Production.PostgreSqlMigration.psm1`; the runbook documents the durable protocol. Existing tests and `prod.ps1` are conditional on the implementation plan's refreshed-main inspection.

## Unit Testing
No tests are run for this design-only stage. Implementation should use the existing focused PowerShell test coverage; no new regression-test suite is requested.

## Local Testing
Not applicable to this design-only stage. Implementation verification will not connect tests to production databases; live production checks use only the guarded operational command and explicitly read-only probes.

## Validation
Before implementation, review the complete design and implementation plan; verify existing production journal/evidence hashes remain readable; verify protected atomic-write and reparse-path helpers on refreshed `origin/main`; pass relevant existing tests and required CI before cutover.

## Rollback or Recovery
Before any writer stop, abort safely and preserve all existing evidence on a failed archive or pointer operation. Before authority publication, use the existing verified Mongo recovery path. At or after authority publication, preserve PostgreSQL authority and continue forward only. Never delete the prior attempt archive to recover space or make a retry possible.

## Risks
The existing single journal and fixed-name sidecars are coupled throughout cutover helpers. A partial conversion could associate evidence with the wrong attempt or strand recovery; all journal and sidecar consumers must be included in the refreshed-main inspection and implementation review. Pointer replacement must be atomic and protected, and legacy evidence must remain discoverable after migration.

## Completion Criteria
User approves this written design; an implementation plan is reviewed and published; the supported retry path preserves prior evidence and fails closed under ambiguous conditions; required existing checks and CI pass; the approved cutover reaches verified PostgreSQL authority and runtime health. Migration remains incomplete until backup/restore proof, soak, PostgreSQL-aware ordinary deployment, and safe MongoDB retirement are complete.
