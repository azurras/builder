# PostgreSQL authority ownership compatibility

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Resolve the proven Windows authority-file ownership mismatch and resume the approved migration without weakening protected ACLs.

## Goals
Accept the owner created by the supported PowerShell protection routine; retain rejection of untrusted owners and writes, invalid signatures, expired leases, and reparse paths.

## Inputs
Production audit on September 8 confirms release `39867e9e1f1da44373fda19f82cfb41da08d5129`, ROLLED_BACK after MONGO_ARCHIVED, no authority marker, and healthy Mongo-backed website. Java read-only probe rejects all protected authority nodes owned by BUILTIN\Administrators. PowerShell New-ProtectedProductionAcl explicitly sets that owner. PR 1385 previously merged with all CI passing.

## Branch
`codex/fix-postgresql-authority-owner` in `A:\Projects\christopherbell.dev-worktrees\postgresql-cutover`, from refreshed origin/main.

## Non-Goals
No production ACL changes, credential disclosure, signature bypass, Mongo retirement, or broad persistence refactor.

## Assumptions
The existing production cutover approval remains valid for up to thirty minutes downtime. Automatic deployment remains paused pending PostgreSQL-aware ordinary deployment.

## Open Questions
No unresolved design choice for the owner fix. Any subsequent cutover failure must be diagnosed before retrying; successful authority transfer is not assumed.

## Task Breakdown

### Task 1 - Align protected Windows owner policy
Required skill: write-jane-street-style-code.
- Dependencies: None; read-only production reproduction completed.
- Files: `website/src/main/java/dev/christopherbell/configuration/persistence/migration/FinalizeEvidenceLoader.java`; `docs/operations/postgresql-migration.md`.
- Symbols: protectedAttributes, trustedProductionPrincipal, trustedProductionWritePrincipal.
- Inspection: current main 39867e9e and Production.Common.psm1/New-ProtectedProductionAcl; Java trusts Administrator writes but not Administrator ownership, while PowerShell creates Administrator-owned files.
- Behavior: Java accepts protected SYSTEM/service/Administrators-owned nodes and rejects untrusted owners.
- Invariants: exact trusted principals only; write ACL, symlink, HMAC, lease and path checks remain intact. No production permissions are altered.
- Boundary/API: reuse the existing private trusted-write predicate for owner validation; CLI behavior remains fail closed.
- Effects and failures: source/test/doc edits only; unknown ownership continues to reject evidence.
- Tests and evidence: user explicitly requested no new regression tests. Reuse existing evidence tamper tests and the actual read-only native-file rejection/acceptance probe.
- Verification: focused FinalizeEvidenceLoaderTest and migration tests; required CI on all operating systems; independent semantic review.

### Task 2 - Verify and deliver through guarded cutover
- Dependencies: Task 1 tested, reviewed, CI green, merged.
- Files: existing `ops/production/windows/prod.ps1`, migration module, protected journal; dated Builder runtime report and session memory.
- Symbols: postgres-cutover, ROLLED_BACK recovery evidence, read-only candidate and production verification.
- Inspection: previous attempt is terminal pre-authority rollback; runtime source snapshot still passes and production readiness is UP.
- Behavior: publish the corrected release and resume approved cutover only after verified evidence and backup prerequisites.
- Invariants: preserve failed attempts, explicit identity checks, thirty-minute budget, no Mongo fallback after authority, no production test fixtures.
- Boundary/API: supported deployment command; no ad hoc production application start.
- Effects and failures: authorized archive/release build and cutover; rollback before authority, PostgreSQL-only forward recovery after authority.
- Tests and evidence: native read-only evidence acceptance; service/listener/HTTP and role proof; backup/restore and journal readback.
- Verification: healthy alternate-port acceptance within supported procedure, production readiness/public endpoints, exact release and authority journal; save runtime report before closure.

### Task 3 - Preserve safe migration CLI failure classification
Required skill: write-jane-street-style-code.
- Dependencies: Task 2 cutover failed with `MigrationStorageException` / `PSQLException`, SQLSTATE `42P01`; schema bootstrap failed with Java exit code 1. Read-only inventory confirms Flyway history and all migration ledger tables are absent.
- Files: `website/src/main/java/dev/christopherbell/configuration/persistence/migration/PostgresqlMigrationSourceSnapshotCli.java`; `website/src/main/java/dev/christopherbell/configuration/persistence/migration/PostgresqlMigrationCli.java`; `website/src/main/java/dev/christopherbell/configuration/persistence/migration/ProductionPostgresqlSchemaMigrator.java`; `ops/production/windows/modules/Production.Common.psm1`; `ops/production/windows/modules/Production.PostgreSqlMigration.psm1`; `ops/production/windows/modules/Production.PostgreSql.psm1`; existing CLI contract assertions only.
- Symbols: migration CLI `execute` failure handlers; schema migrator `main`; `Invoke-CheckedProcess`; both migration modules' `$script:DefaultProcessAction`.
- Inspection: merged `0b1531e2` and `49880434` expose allowlisted class lines for migration cutover CLIs; merged `f38554e1` also exposes SQLSTATE for those CLIs. Bootstrap invokes `ProductionPostgresqlSchemaMigrator` but its PowerShell process action still discards stderr. Production evidence confirms that invocation failed and no Flyway or migration-ledger schema was created.
- Behavior: preserve nonzero exit codes and success stdout while forwarding bounded, allowlisted exception class and SQLSTATE lines for the snapshot, migration, and production-schema-migrator Java entry points.
- Invariants: never print exception messages, stack traces, SQL text, SQL parameters, URIs, credentials, or source records; do not forward arbitrary stderr; do not alter migration semantics or production data.
- Boundary/API: an opt-in safe-diagnostic switch on the checked process helper; enable only for the three exact migration Java main classes. Filter exception class lines and five-character SQLSTATE lines only. Update existing contract assertions as needed, without adding tests.
- Effects and failures: no database writes; report includes only strict class-name lines and the existing generic process failure.
- Tests and evidence: the user explicitly requested no new regression tests or local test runs; compile the changed Java source, retain the existing assertion update, and rely on required CI plus guarded production outcome.
- Verification: run `:website:classes`, review the allowlist and call-site scope, then wait for required CI before merge and cutover retry.

## Code Changes
Separate explicit trusted ownership from ordinary user ownership, reusing the established trusted write-principal set. Do not change ACL creation or relax cryptographic evidence verification. Preserve and forward only allowlisted exception class metadata and SQLSTATE when migration or schema-migrator Java entry points fail; do not print exception messages or sensitive data. The finalize failure category is `42P01`, and schema bootstrap currently exits 1 without creating migration tables; expose its safe cause metadata before retrying bootstrap.

## Files and Modules
Task 1 owns the Java loader and migration runbook. Task 2 reuses existing operational modules. Task 3 owns both Java migration CLI boundaries, the production schema migrator boundary, and their narrow PowerShell stderr bridge; update only existing contract assertions and add no regression test.

## Unit Testing
Run `:website:test --tests '*FinalizeEvidenceLoaderTest'` first, then migration-focused tests. These policy/file tests require no database. Database-backed tests, if needed, must target only database `test` with an isolated role.

## Local Testing
Run a read-only Java probe against actual protected production metadata and signed evidence using a historical clock solely to diagnose the expired prior attempt, never to authorize writes. Deployment acceptance uses the existing read-only viewer candidate gate; no production fixtures.

## Validation
Plan semantic review: ready; inspected counterexample supports the narrow fix. Required evidence includes focused checks, native probe, full CI and actual supported deployment outcome.

## Rollback or Recovery
Before authority preserve/validate prior journals and let the supported procedure restore untouched MongoDB. After authority never switch to stale Mongo. Preserve all evidence and repair forward. Retain stopped Mongo for fourteen-day soak and final archive for ninety days.

## Risks
An ownership fix may reveal another latent finalization issue. Do not treat successful metadata validation as proof of migration completion. Existing ordinary deployment still needs PostgreSQL-aware backup/candidate support before reenabling automation.

## Completion Criteria
Owner mismatch fixed with existing tests and native proof; reviewed commit merged after passing CI; protected cutover outcome and runtime evidence recorded truthfully. Full migration remains open until post-authority soak, restore proof, safe retirement and ordinary deployment support are complete.
