# christopherbell.dev MongoDB-only persistence

## Plan Format

task-contract-v1

## Document Status

ready-for-execution

## Objective

Remove PostgreSQL as a supported application and production-operations backend, keeping MongoDB as the sole supported persistence system and preserving existing MongoDB data and behavior.

## Goals

- Remove PostgreSQL persistence adapters, selectors, dependencies, test infrastructure, migration and cutover tooling, configuration, and active operator documentation.
- Make local, test, candidate, and production configuration unambiguously MongoDB-only.
- Keep MongoDB repositories, versioned Mongo migrations, backups, restores, and domain collection tools working.
- Keep dated session records, test reports, and earlier Builder plans as historical evidence; remove obsolete PostgreSQL runbooks from the active spoke documentation.

## Inputs

- User confirmed PostgreSQL is no longer a target and authorized removing the PostgreSQL work.
- Refreshed spoke `origin/main` to `f4382d118db9db43efc952dc08e96649e2c70753`; the selected isolated worktree was clean before refresh.
- Inventory found 279 tracked text files with PostgreSQL references: 166 under application main sources, 90 under tests, and the remainder in build, deployer, configuration, and documentation.
- Inspected repository `AGENTS.md`, root README, configuration package README, Gradle dependencies/tasks, application profiles, production command dispatch, and Compose database services.
- MongoDB remains the production backend and its persistent data must not be altered by this source cleanup.

## Branch

`codex/mongodb-only-persistence-20260924`, based on refreshed `origin/main` at `f4382d118db9db43efc952dc08e96649e2c70753`. Work only in the isolated worktree at `A:\Projects\christopherbell.dev-worktrees\christopherbell-production-bootstrap-20260924`; preserve the dirty authoritative checkout.

## Non-Goals

- No production database writes, migration, cutover, service/task changes, or deletion of database files.
- No removal of MongoDB persistence, Mongo migration/backup/restore, or Mongo domain collection consolidation.
- No rewriting dated session memories or prior runtime reports; these are historical evidence.
- No unrelated feature behavior changes.

## Assumptions

- MongoDB is the permanent persistence target for this application.
- PostgreSQL-only source and active operating procedures may be deleted when no MongoDB caller depends on them.
- Existing generic contracts are retained only when MongoDB or another current feature still uses them.

## Open Questions

None. The requested target is MongoDB-only; ambiguous historical references will be retained only where they document past work.

## Task Breakdown

### Task 1 - Reduce application persistence and build to MongoDB

- Dependencies: None.
- Files: `website/build.gradle.kts`, `website/src/main/resources/application-local.yml`, `website/src/main/resources/application-test.yml`, `website/src/main/resources/db/**`, `website/src/main/java/dev/christopherbell/configuration/**`, PostgreSQL-named application classes and tests across `website/src/main/java` and `website/src/test/java`, feature package READMEs containing active backend guidance, and Mongo configuration/tests that must continue to pass.
- Symbols: persistence backend selection and startup validation; Mongo persistence auto-configuration; all PostgreSQL repositories, stores, schema guards, parity wiring, Flyway/JDBC migration runner and SQL resources; Gradle database dependencies and migration tasks; active feature migration verifiers that exist only for the abandoned target.
- Inspection: Refreshed `origin/main` at `f4382d1`; inspected project instructions, persistence package documentation, dependency/task declarations, runtime profiles, production settings validation, and source/test inventory. Reinspect all callers and Mongo equivalents immediately before deletions.
- Required skill: `write-jane-street-style-code` before code changes.
- Behavior: All supported application profiles start with MongoDB configuration; selection of PostgreSQL or PostgreSQL credentials is no longer accepted or needed. Mongo feature operations, versioned Mongo migrations, and their tests remain operational.
- Invariants: Preserve MongoDB document shapes and live data. Never write to production during verification. Do not remove a generic port or migration facility still used by MongoDB. Do not keep dead PostgreSQL adapters, profile branches, JDBC/JPA/Flyway dependencies, or PostgreSQL-only tests.
- Boundary/API: Internal persistence selection, build dependencies/tasks, local/test configuration, and internal admin migration endpoints tied solely to PostgreSQL. No unrelated public API or feature contract changes.
- Effects and failures: Startup fails with a clear Mongo configuration error if the Mongo URI is invalid or absent in a required environment; obsolete PostgreSQL selector/credential settings cannot silently select another backend. No database migration or writes are performed by this cleanup.
- Tests and evidence: Establish current focused test/build evidence from the refreshed branch. Add or adapt Mongo-only selection/configuration tests; remove PostgreSQL-only tests after callers are removed. Run configuration and feature tests, then the full `:website:test` and `:website:build` suites.
- Verification: Search all active source/build/config/test paths for PostgreSQL adapters, JDBC URLs, JPA/Flyway dependencies, and selectable backend branches; inspect the final diff and run the native Gradle checks. Confirm MongoDB profile configuration and versioned Mongo migration paths remain present.

### Task 2 - Remove PostgreSQL production operations and active guidance

- Dependencies: Task 1, so remaining application/backend contracts are known before removing operator commands.
- Files: `compose.yaml`, `ops/production/windows/prod.ps1`, production PowerShell modules/tests/config/service launcher, active `docs/operations/postgresql*.md`, MongoDB runbooks, root README, feature/configuration READMEs, and docs navigation/indexes.
- Symbols: PostgreSQL command aliases and confirmation switches, module imports and installers, PostgreSQL service/environment examples, PostgreSQL backup/restore/cutover helpers and tests, and active documentation links describing a supported PostgreSQL deployment.
- Inspection: Refreshed `origin/main`; inspected Compose, production command dispatch, application profiles, and counted references by source, test, configuration, and docs. Inspect every remaining caller before deletion and preserve Mongo production command contracts.
- Required skill: `write-jane-street-style-code` before code or executable configuration changes.
- Behavior: The production CLI, Compose stack, service launcher, examples, and active operator documentation describe and operate MongoDB only. Existing Mongo inventory/consolidation and backup/restore commands retain their existing safeguards.
- Invariants: Do not stop or uninstall any production services, scheduled tasks, database processes, or alter protected production files. Retain historical Builder session records and test reports without treating them as current procedures. Keep production secret handling and existing deploy safeguards.
- Boundary/API: Local operator command surface, examples, Compose service list, and active documentation only. Existing Mongo command names remain stable.
- Effects and failures: PostgreSQL operator commands/configuration are removed from source; invoking an obsolete command reports the normal unknown-command error. Production state is untouched.
- Tests and evidence: Add/adapt CLI tests proving PostgreSQL aliases are gone while Mongo commands remain; run focused Pester suites under supported PowerShells, Compose/config validators when available, and documentation/link checks.
- Verification: Search active code/config/operator docs for PostgreSQL instructions and command names; exclude immutable historical records and test reports from this active-surface search. Run appropriate repository checks and review the complete diff.

## Code Changes

Tasks 1 and 2 only. Do not touch live machine state. Keep changes limited to PostgreSQL removal and necessary MongoDB-only configuration/tests/docs.

## Files and Modules

Java/Spring persistence and feature packages, Gradle application configuration, Mongo and PostgreSQL test suites, Windows production operations, Compose, and active operations documentation.

## Unit Testing

Use Gradle/JUnit for application and configuration contracts. Use the repository's Pester suites for production command/module contracts under PowerShell 7 and Windows PowerShell 5.1 when available.

## Local Testing

Use the repository's MongoDB Compose service and existing isolated test database conventions. Do not connect local verification to production; avoid real external integrations unless the repository test harness isolates them.

## Validation

Run focused Mongo/configuration tests first, then `:website:test`, `:website:build`, relevant JavaScript and PowerShell checks, structural documentation/index validation, `git diff --check`, and a final active-surface PostgreSQL search. Review deleted files and remaining historical mentions.

## Rollback or Recovery

The change is source/configuration only. Revert the MongoDB-only source change to restore prior code if acceptance fails. Production MongoDB data, service state, and release remain untouched by local checks. Use the normal protected production deploy process only after CI succeeds and the Mongo-only app candidate is validated.

## Risks

PostgreSQL adapter classes share ports with Mongo implementations; careless deletion could remove behavior still required by Mongo. Migration verification endpoints may include non-PostgreSQL checks, so trace callers and split/remove them only when the remaining Mongo paths are preserved. Historical docs and records must not be mistaken for active instructions. Removing JDBC/Flyway dependencies can alter dependency-verification metadata and must be validated with a clean build.

## Completion Criteria

Application profiles and production ops are MongoDB-only; PostgreSQL source adapters, driver/dependency/config, operational commands, and active runbooks are gone; MongoDB features and tooling still pass tests/build; active-path search finds no PostgreSQL runtime, build, configuration, or operator procedures; historical dated records remain intact; CI passes and the change is published through the repository's normal PR workflow without touching production state.
