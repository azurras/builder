# PostgreSQL cutover retry implementation plan

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Implement the approved attempt-scoped PostgreSQL cutover journal/evidence protocol so a verified pre-authority rollback can be retried safely without losing prior evidence.

## Goals
- Preserve historical journal and sidecar bytes under an immutable per-attempt directory.
- Make journal and sidecar reads/writes resolve to the validated active attempt while retaining compatibility with the existing flat legacy journal.
- Allow a new attempt only after `ROLLED_BACK`, `authorityPublished=false`, authority absence, MongoDB service running and unlocked, and Mongo-backed production endpoint health are verified.
- Keep `AUTHORITY_PUBLICATION_STARTED`, `FORWARD_RECOVERY_REQUIRED`, `SOAKING`, and nonterminal attempts non-retryable.
- Deliver through reviewed PR, required CI, the supported production command, and actual runtime evidence.

## Inputs
- Approved design: [PostgreSQL cutover retry design](2026-09-23-postgresql-cutover-retry-design.md).
- Freshly fetched `origin/main`: `577caed1f489c20909ee572ac817f3455f9a911b` (PR #1395 includes the current-release schema bootstrap fix).
- In this revision, journal and sidecar helpers in `ops/production/windows/modules/Production.PostgreSqlMigration.psm1` use singleton flat files. `Invoke-ProductionPostgreSqlCutover` returns the terminal `ROLLED_BACK` journal without a new run.
- The production cutover Pester file is `ops/production/windows/tests/Production.PostgreSqlCutover.Tests.ps1`; the runbook is `docs/operations/postgresql-migration.md`.
- PostgreSQL bootstrap/readback on 2026-09-23 confirms Flyway version 27 and required migration ledger tables. Production `current` remained unchanged at that time.
- User explicitly requested no new regression-test suite; this plan adds no tests and does not modify existing assertions. Existing tests and CI remain verification gates.

## Branch
Create isolated spoke worktree and branch `codex/postgresql-cutover-retry` from refreshed `origin/main` SHA `577caed1f489c20909ee572ac817f3455f9a911b`. Do not edit the dirty authoritative checkout or the existing `postgresql-cutover` worktree, which has an untracked `.gradle-agent/` directory.

## Non-Goals
- No production journal deletion, manual editing, evidence bypass, ACL changes, credential disclosure, or MongoDB retirement.
- No new test suite or test cases.
- No cutover retry from any phase other than a verified pre-authority `ROLLED_BACK` state.
- No enabling automatic deployment; ordinary PostgreSQL-aware deployment and restore proof remain separate migration requirements.

## Assumptions
- The existing production-cutover approval remains valid for up to 30 minutes of downtime.
- The existing protected production directory and `Protect-ProductionPath`, `Assert-ProtectedProductionPath`, `Assert-ProductionPathNotReparse`, and atomic replace patterns remain the security boundary.
- The previous failed attempt is safely rolled back; the retry path must verify live state rather than rely on this assumption.
- Runtime change requires the supported production deployment mechanism and post-cutover service/endpoint/database verification.

## Open Questions
None. If refreshed-main inspection contradicts the approved attempt-storage design or reveals ambiguous production authority, stop and report the specific evidence before changing scope.

## Task Breakdown

### Task 1 - Implement immutable attempt-scoped cutover evidence and guarded retry
Required skill: write-jane-street-style-code.
- Dependencies: approved written design and this published implementation plan.
- Files: `ops/production/windows/modules/Production.PostgreSqlMigration.psm1`; `docs/operations/postgresql-migration.md`.
- Symbols: `Get-ProductionPostgreSqlCutoverJournalPath`, `Read-ProductionPostgreSqlCutoverJournal`, `Write-ProductionPostgreSqlCutoverJournal`, `Get-ProductionPostgreSqlCutoverSidecarPath`, `Read-ProductionPostgreSqlCutoverSidecar`, `Write-ProductionPostgreSqlCutoverSidecar`, `Assert-ProductionPostgreSqlCutoverMongoUnlocked`, `Restore-ProductionPostgreSqlCutoverPreAuthority`, and `Invoke-ProductionPostgreSqlCutover`.
- Inspection: fetched `origin/main` at `577caed1f489c20909ee572ac817f3455f9a911b`; confirmed the journal is currently `migration/postgresql-cutover.json`, sidecars are fixed-name `migration/postgresql-cutover-<name>.json`, all operational producers/consumers route through the named helpers, journal digests bind ordered transitions, the Mongo unlock helper accepts only explicit `currentOp` `fsyncLock:false`, and rollback recovery checks authority absence and verifies endpoints. Reinspect the same callers in the new worktree before editing.
- Behavior: store each attempt under a directory keyed by its validated lock token; store that attempt's journal and sidecars together; maintain a protected active-attempt pointer; read legacy flat files when no pointer exists. On a legacy terminal rollback, copy the journal and every allowlisted existing sidecar into the legacy attempt directory and verify byte hashes before activating a fresh attempt. Do not overwrite the legacy files. Future attempts write into unique attempt directories.
- Invariants: all read/write paths remain under the configured production migration root and reject reparse points; preserve existing ACL protection and atomic-write behavior; validate the pointer schema/token against the journal; retain journal and evidence digests and exact phase order; never retry after authority publication or from soak/forward-recovery/nonterminal states; no writer stop until archive, pointer, Mongo-unlocked, Mongo-running, Mongo-backed service, and endpoint-health checks have succeeded; preserve the 30-minute budget and existing explicit confirmation boundary.
- Boundary/API: keep `prod.ps1 postgres-cutover -ConfirmPostgreSqlCutover` as the sole operator command. Do not add a reset/delete flag or expose lower-level journal mutation commands.
- Effects and failures: legacy archival and new pointer/journal creation happen before stopping writers; interruption before pointer activation leaves the legacy journal authoritative and intact; pointer activation is atomic; ambiguous/partial archive or pointer state fails closed without touching writers; the current attempt can resume only when active pointer and journal lock tokens match.
- Tests and evidence: add no tests or test cases. Run the existing `Production.PostgreSqlCutover.Tests.ps1` and the full Windows Pester suite unchanged; use PowerShell parser checks and byte/hash readback of existing production evidence to validate preservation. Required PR CI remains mandatory.
- Verification: compare original flat journal and all present allowlisted sidecar hashes with the attempt archive; inspect archive/active-pointer paths and ACL/reparse protections; parse touched PowerShell; run `Invoke-Pester -Path ops/production/windows/tests/Production.PostgreSqlCutover.Tests.ps1 -CI`; run `git diff --check`; complete required CI before merge.

### Task 2 - Deliver and execute the approved retry with runtime proof
- Dependencies: Task 1 reviewed, required CI green, PR merged, and read-only production preflight confirms the archived prior attempt, no authority marker, PostgreSQL schema version 27, MongoDB running/unlocked, Mongo-backed service health, and paused automatic deployment.
- Files: supported `ops/production/windows/prod.ps1` command; Builder `docs/test-reports/YYYY-MM-DD-postgresql-cutover-retry.md` and `docs/session-memory/YYYY-MM-DD-christopherbell-dev.md` after runtime proof.
- Symbols: `postgres-cutover`, active-attempt journal and sidecars, authority marker, production readiness and public endpoints.
- Inspection: current terminal journal is from 2026-09-22 with `authorityPublished=false`; the previous approved pre-authority failure left MongoDB authoritative. Re-read current protected state immediately before executing.
- Behavior: execute the sole supported command against the merged `origin/main` release, preserve the 30-minute downtime cap, and reach PostgreSQL authority only after the existing archive, reconciliation, backup/restore, candidate, and authority prerequisites succeed.
- Invariants: no manual production journal/file edits; no change to the active site before the supported procedure; before authority use the existing verified Mongo rollback; after authority, recover PostgreSQL forward only; keep auto-deploy paused.
- Boundary/API: `prod.ps1 postgres-cutover -ConfirmPostgreSqlCutover` under the supported elevated Windows operations path.
- Effects and failures: database writes, Mongo writer freeze/archive, bounded website downtime and service rotation are authorized only within the approved cutover procedure; stop on failed preflight and capture the terminal phase without repeating blindly.
- Tests and evidence: no production fixtures. Capture actual command outcome, attempt identity, journal phase, authority marker, database/service state, listener, readiness/public endpoint request/status/body, and rollback or forward-recovery result.
- Verification: confirm service and PostgreSQL role/database state, readiness and public endpoints, exact deployed release/authority journal, prior-attempt archive hashes, and automatic deployment remains paused; save and validate the Builder runtime report before subsequent publication or closure.

## Code Changes
Only the cutover journal/evidence storage and terminal retry control flow plus the migration runbook. Existing tests remain unchanged per user request.

## Files and Modules
The cutover state machine and evidence path helpers are in `Production.PostgreSqlMigration.psm1`; operational phase and retention rules are in `docs/operations/postgresql-migration.md`. CI runs the complete Windows Pester suite.

## Unit Testing
No test cases are added or modified. Run the existing `Production.PostgreSqlCutover.Tests.ps1` and full Windows Pester suite; report any existing failure without masking it.

## Local Testing
No production database is used by local tests. Validate path resolution and byte-preserving archive behavior only through existing Pester coverage and non-production temporary directories already used by those tests. Use production only for the approved guarded command and read-only preflight/postflight evidence.

## Validation
PowerShell AST parse for changed modules; focused cutover Pester and full CI; independent diff review of every journal/sidecar caller; legacy/current pointer compatibility checks; archive source/destination SHA-256 readback; required PR merge; production authority/service/endpoint proof; Builder runtime report validation.

## Rollback or Recovery
Before pointer activation, abort with legacy state untouched. After pointer activation but before writer stop, retain both attempt records and resume only if pointer/journal identity validates. Before authority publication, use existing `Restore-ProductionPostgreSqlCutoverPreAuthority` only after its explicit Mongo-unlocked and endpoint checks. At or after `AUTHORITY_PUBLICATION_STARTED`, never return to Mongo; follow the recorded PostgreSQL forward-recovery path.

## Risks
The singleton active pointer becomes a critical selector for all journal and sidecar consumers; a stale or mismatched pointer must fail closed. Legacy flat files may include orphaned evidence, so archive every file matching the strict sidecar allowlist rather than only sidecars referenced by the journal. Must verify ACL inheritance and atomic replacement on native Windows. No new tests are authorized, increasing reliance on existing CI coverage plus production evidence preservation checks.

## Completion Criteria
The approved attempt-storage protocol is implemented and reviewed; all existing relevant tests and required CI pass; prior production evidence remains byte-identical and recoverable; guarded cutover either reaches verified PostgreSQL authority or records a safe, explicit rollback; runtime report and dated session memory are saved/published. The overall migration remains open until PostgreSQL-aware ordinary deployment, backup/restore proof, soak, and safe MongoDB retirement are complete.
