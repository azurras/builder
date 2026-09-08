# 2026-08-13 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/session-memory/2026-08-13-christopherbell-dev-postgresql-migration-design.md](#source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md)
- [docs/specs/2026-08-13-christopherbell-dev-postgresql-migration.md](#source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md)
- [docs/work/2026-08-13-christopherbell-dev-postgresql-migration.md](#source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md)

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md"></a>
## 2026-08-13 | session-memory | 2026-08-13 christopherbell.dev PostgreSQL Migration Design

Original source: `docs/session-memory/2026-08-13-christopherbell-dev-postgresql-migration-design.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `cb880b83b020e714517267ce33f2e0cfc2f560e960d81688b3aea086002b4de3`.

<!-- migrated-source: docs/session-memory/2026-08-13-christopherbell-dev-postgresql-migration-design.md -->
<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--2026-08-13-christopherbelldev-postgresql-migration-design"></a>
### 2026-08-13 christopherbell.dev PostgreSQL Migration Design

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--0952---approved-postgresql-migration-design-checkpoint"></a>
#### 09:52 - Approved PostgreSQL migration design checkpoint

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--request"></a>
##### Request

Start the website's next database migration after completing the MongoDB collection
consolidation. Replace MongoDB with PostgreSQL, designate a PostgreSQL database named
`test` for local development and database-backed testing, and provide Compass-like visual
database viewer software for PostgreSQL.

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--project-context"></a>
##### Project Context

- Builder is the workflow hub; the spoke is `azurras/christopherbell.dev`.
- The authoritative spoke checkout at `A:\Projects\christopherbell.dev` has extensive
  unrelated dirty state and was inspected read-only. Future implementation must use a
  clean isolated worktree from refreshed `origin/main`.
- Planning used `origin/main` at
  `e073823d14ffed0b4c113707d16c0ad0cfe1b7fa`.
- The completed Mongo consolidation provides 14 domain collections, 52 canonical kinds,
  126 manifest indexes, and explicit kind-scoped persistence boundaries.
- The Windows development host is production. No application, database, GUI, service,
  listener, or production-data mutation occurred during this design checkpoint.

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--work-completed"></a>
##### Work Completed

- Created the active Builder work ledger:
  `docs/work/2026-08-13-christopherbell-dev-postgresql-migration.md`.
- Created the ready-for-review project specification:
  `docs/specs/2026-08-13-christopherbell-dev-postgresql-migration.md`.
- Recorded the target platform, relational boundaries, migration catalog and engine,
  shadow rehearsals, cutover, failure handling, PostgreSQL recovery, monitoring, pgAdmin
  access, Mongo soak/retirement, verification, delivery phases, and acceptance criteria.
- Self-reviewed the specification for placeholders, contradictions, scope, and ambiguity;
  no unresolved design question remains.

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--decisions"></a>
##### Decisions

- PostgreSQL becomes the sole durable database; no permanent hybrid remains.
- Use domain-relational schemas, Flyway versioned SQL, jOOQ-generated types, and explicit
  PostgreSQL adapters behind existing persistence ports.
- Run PostgreSQL 18 as a loopback-only native Windows service on the production host.
- Use repeated shadow imports followed by a stopped-writer final reconciliation; do not
  add production dual writes. Design against an assumed maximum 30-minute cutover.
- Use PostgreSQL database `test` for all local development and database-backed tests.
  Automated suites isolate through disposable uniquely named schemas inside `test`.
- Install pgAdmin 4 Desktop. Its `test` connection is read/write, while its production
  connection uses a database-enforced read-only viewer role. Privileged credentials are
  not registered in pgAdmin.
- Before the authority flip, fallback returns to untouched MongoDB. After PostgreSQL
  writes begin, recovery stays PostgreSQL-native and never switches silently to stale
  MongoDB.
- Stop and freeze MongoDB for a 14-day PostgreSQL soak, then remove Mongo runtime/service
  and exact live data after recovery evidence passes. Retain the final verified Mongo
  archive for 90 days with an exact evidence-gated deletion owner.

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--validation"></a>
##### Validation

- Verified Builder is clean on `main` with canonical `azurras/builder` origin before
  creating artifacts.
- Refreshed and inspected current spoke `origin/main` without touching the dirty checkout.
- Reviewed representative Mongo adapters, kind-scoped operations, Gradle dependencies,
  production configuration, and operational migration surfaces.
- Checked current primary documentation for PostgreSQL supported releases, Spring Boot
  SQL/jOOQ integration, jOOQ code generation, and pgAdmin Desktop capabilities.
- Placeholder scan found no unfinished markers, incomplete line ranges, or unresolved
  decisions in the work record or specification.
- No application tests or runtime checks were run because this checkpoint contains only
  Builder design artifacts and authorizes no implementation.

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--current-state"></a>
##### Current State

- Architecture and all interactive design sections are approved.
- The saved written specification remains at the required user-review gate.
- No PostgreSQL installation, pgAdmin installation, schema migration, data copy, website
  edit, spoke branch, service change, or production cutover has begun.

<a id="source-docs-session-memory-2026-08-13-christopherbell-dev-postgresql-migration-design-md--follow-ups"></a>
##### Follow-ups

1. Obtain explicit approval of the saved written specification.
2. Invoke the implementation-planning workflow and inspect a fresh spoke worktree for
   literal files and line ranges.
3. Review and validate the implementation plan before any production code or operational
   change.
4. After plan approval, execute the full Builder delivery loop through PR/CI/merge,
   protected cutover, 14-day soak, Mongo retirement, production verification, closure,
   and final archive-retention tracking.

<!-- /migrated-source: docs/session-memory/2026-08-13-christopherbell-dev-postgresql-migration-design.md -->

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md"></a>
## 2026-08-13 | specs | christopherbell.dev PostgreSQL Migration

Original source: `docs/specs/2026-08-13-christopherbell-dev-postgresql-migration.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `605041cac215665ab76bc7de9cdd6528b04c8a4d92b2c544b3e65c4c7588cfc4`.

<!-- migrated-source: docs/specs/2026-08-13-christopherbell-dev-postgresql-migration.md -->
<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--christopherbelldev-postgresql-migration"></a>
### christopherbell.dev PostgreSQL Migration

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--document-status"></a>
#### Document Status

ready-for-execution

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--purpose"></a>
#### Purpose

Replace MongoDB with PostgreSQL as the website's sole durable database, convert the
current document persistence model into typed relational domain schemas, migrate every
production record without loss or silent semantic drift, establish PostgreSQL-native
operations and recovery, and retire MongoDB after a verified production soak.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--background"></a>
#### Background

The website currently runs as one Spring Boot deployable on a Windows development host
that is also production. MongoDB is a native Windows service bound to loopback, the
website listens on port 8080, and cloudflared provides public delivery. The production
database is named `christopherbell`.

The completed MongoDB consolidation gives this migration an explicit source model:

- 14 domain-owned physical collections;
- 52 canonical document kinds;
- 126 manifest-defined indexes;
- kind-scoped repository and operations boundaries;
- guarded backup, migration, inventory, cutover, and recovery tooling.

Current source still depends deeply on MongoDB query, update, aggregation, lease, TTL,
index, configuration, and operational semantics. A dependency replacement alone would
not be a valid migration. PostgreSQL must reproduce the website's externally observable
behavior while replacing document envelopes with relational constraints, transactions,
queries, and recovery.

The authoritative checkout at `A:\Projects\christopherbell.dev` contains extensive
unrelated user state and must remain untouched. Implementation must use a clean isolated
worktree created from refreshed `origin/main`.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--approved-decisions"></a>
#### Approved Decisions

1. PostgreSQL is the final and only durable production database. MongoDB is not retained
   for caches, leases, history, or selected domains.
2. The target is a domain-relational model. The migration will not reproduce the 14
   Mongo envelopes as generic `kind + JSONB` tables.
3. Flyway SQL is the sole schema authority. jOOQ-generated schema types and explicit SQL
   implement persistence adapters behind existing domain ports.
4. PostgreSQL runs as a loopback-only native Windows service on the production host.
5. The transition uses repeatable shadow imports and reconciliation, then a bounded
   stopped-writer final cutover. There is no production dual-write period.
6. The assumed maximum maintenance window is 30 minutes. Rehearsal must prove adequate
   margin before production is stopped.
7. Local development and every database-backed automated or manual test use a PostgreSQL
   database named exactly `test`.
8. pgAdmin 4 Desktop is installed as the Compass-like visual viewer for PostgreSQL.
   Production browsing uses a database-enforced read-only role.
9. MongoDB remains stopped and frozen for a 14-day PostgreSQL soak. The verified final
   Mongo archive is retained for 90 days before exact deletion.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--goals"></a>
#### Goals

1. Preserve every production record, stable identifier, relationship, timestamp,
   external payload, uniqueness rule, expiration rule, and optimistic-concurrency rule.
2. Replace document storage with typed domain tables, foreign keys, checks, unique
   constraints, relational joins, and narrowly justified JSONB.
3. Keep controllers, services, public routes, authorization, frontend behavior, and
   public data contracts stable.
4. Keep one modular-monolith deployable while maintaining existing module and
   persistence-port boundaries.
5. Make schema evolution deterministic, reviewable, repeatable, and reproducible from
   an empty PostgreSQL database.
6. Make the data transformation deterministic, idempotent, resumable, bounded, and
   exactly reconcilable against the frozen Mongo source.
7. Provide a short, rehearsed cutover with a safe pre-authority rollback boundary.
8. Establish PostgreSQL-native backup, point-in-time recovery, restore testing,
   monitoring, and least-privilege administration.
9. Provide safe visual database inspection through pgAdmin without turning the GUI into
   the deployment or production-mutation control plane.
10. Remove MongoDB application code, dependencies, configuration, operations, service,
    and exact live data only after PostgreSQL acceptance and retirement gates pass.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--non-goals"></a>
#### Non-Goals

- Do not introduce a permanent MongoDB/PostgreSQL hybrid.
- Do not use JSONB as the default substitute for Mongo documents.
- Do not redesign user-facing features, HTTP contracts, URLs, authentication, or the
  frontend as part of the persistence migration.
- Do not split the modular monolith into services or deploy multiple application writers.
- Do not add a production dual-write or change-data-capture system solely to claim
  near-zero downtime.
- Do not use H2, an embedded database, or mocked SQL as proof of PostgreSQL behavior.
- Do not expose PostgreSQL or pgAdmin beyond loopback.
- Do not allow pgAdmin to hold privileged production owner, migration, or runtime
  credentials.
- Do not run ad hoc production schema or data mutations through pgAdmin.
- Do not delete MongoDB data, archives, code, or service state at initial cutover.
- Do not modify the dirty authoritative spoke checkout.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--target-platform"></a>
#### Target Platform

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--postgresql-service"></a>
##### PostgreSQL service

Production uses the current supported PostgreSQL 18 minor release available at the
implementation checkpoint, installed as a native Windows service under a dedicated
service identity. As of design approval on 2026-08-13, that release is PostgreSQL 18.4.
The implementation must pin and verify the exact installer or distribution checksum and
record its provenance before installation.

PostgreSQL must:

- bind only to `127.0.0.1` and `::1`;
- use SCRAM password authentication for application connections;
- store its data under a protected production path separate from application releases;
- store backups outside the live PostgreSQL data directory;
- start independently before the website and expose a bounded local readiness check;
- use data checksums when supported by the selected Windows distribution;
- use an explicitly configured locale, collation, character set, and time zone that are
  recorded before schema creation and reproduced in restore drills;
- accept no remote network connection, including from pgAdmin.

The production database is named `christopherbell`. It is not used for local
development or ordinary automated/manual tests.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--database-roles"></a>
##### Database roles

At minimum, production has separate roles for:

- **owner**: owns the database objects; no website or GUI login;
- **migrator**: executes reviewed Flyway DDL during guarded deployment; unavailable to
  the running website;
- **application**: receives only required schema usage, table DML, and sequence rights;
  cannot create/alter/drop database objects or manage roles;
- **migration bridge**: reads the frozen or shadow Mongo source and writes only the
  approved PostgreSQL staging and target objects during guarded migration commands;
- **viewer**: used by the pgAdmin production connection; can inspect schemas, tables,
  rows, indexes, plans, and health metadata but cannot perform DDL, DML, role changes,
  database creation, server-file access, or privileged functions;
- **backup**: receives only the capabilities required by the selected physical and
  logical backup procedures.

Privileges are granted explicitly and tested negatively. Role credentials are stored in
protected production configuration and never committed or printed. The owner, migrator,
migration-bridge, application, and backup credentials are never registered in pgAdmin.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--local-development-and-test-database"></a>
##### Local development and test database

All local website development and every database-backed automated or manual test use:

```text
jdbc:postgresql://127.0.0.1:5432/test
```

The exact credentials are environment-owned and are not committed. Local and CI roles
used for development/testing can connect to database `test` but cannot connect to the
production `christopherbell` database. Automated suites create uniquely named disposable
schemas within `test`, set an exact schema search path, and drop only the schema they
own. This permits parallel execution without creating alternative database names.

Startup and test guards fail before schema mutation when the active database name is not
exactly `test`, except for an explicitly identified protected production deployment or
migration command. Local development documentation names `test` as the only supported
development database. H2 is prohibited as a behavioral substitute.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--pgadmin-visual-viewer"></a>
##### pgAdmin visual viewer

pgAdmin 4 Desktop is a required installed component for the interactive Windows user. It
runs in desktop mode and is not exposed as a server or Windows service.

The standard connections are:

- `christopherbell-test`: read/write connection to database `test` for local development;
- `christopherbell-production-viewer`: read-only connection to production database
  `christopherbell` using only the viewer role.

The production viewer supports object browsing, rows, filters, query plans, schemas,
tables, keys, constraints, indexes, and safe health queries. Database privileges—not a
GUI checkbox—enforce read-only behavior. Flyway execution, restore, cutover, role
management, and production mutations remain guarded repository operations with captured
evidence.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--relational-architecture"></a>
#### Relational Architecture

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--bounded-context-schemas"></a>
##### Bounded-context schemas

One PostgreSQL database contains these initial application-owned schemas:

| Schema | Responsibility |
|---|---|
| `identity` | accounts, authentication, browser sessions, trust, and account lifecycle |
| `social` | posts, relationships, reactions, reports, hidden threads, and previews |
| `communication` | messages, notifications, preferences, guards, and rate limits |
| `federation` | discovery, actors, keys, scans, and outbound delivery |
| `music` | tracks, playlists, metadata, runtime state, radio history, and access events |
| `shared_folder` | audits, maintenance, media jobs, recovery, radio, recycle, and uploads |
| `mobility` | vehicles, VIN state/cache, ZIP coordinates, and location import state |
| `lunch` | restaurants, votes, favorites, preferences, sessions, picks, and imports |
| `canes` | Canes price snapshots and related collection state |
| `platform` | admin activity, pending actions, leases, scheduled runs, and migration ledgers |

These are ownership boundaries, not permission shortcuts. Cross-schema foreign keys are
allowed only where the domain model has an actual relationship. Domain modules remain
responsible for their adapters and mappings.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--table-design-rules"></a>
##### Table design rules

- Aggregate roots use typed tables with stable existing domain identifiers. Public and
  external identifiers do not change merely to adopt database-generated keys.
- Owned repeated values and embedded structures become child tables when they have
  relational identity, constraints, queries, or independent cardinality.
- Many-to-many and graph relationships use explicit association tables with foreign
  keys and domain-specific unique constraints.
- Status and type fields use constrained text or PostgreSQL enum/domain types only when
  their evolution and Flyway compatibility are explicit. Unknown legacy values fail
  migration rather than collapsing into a default.
- Timestamps use `timestamp with time zone` and are compared in UTC. The transformer
  must prove precision and nullability preservation.
- Monetary and measured values use exact numeric types with declared precision and
  scale; binary floating-point is retained only when the domain semantics require it.
- Case-insensitive identity uses explicit canonical columns and unique indexes so
  behavior is deterministic and does not depend on workstation locale.
- JSONB is allowed only for externally controlled or intrinsically open-ended payloads
  whose internal fields are not relationally queried or constrained. Every JSONB column
  requires a written justification and canonical-hash rule in the migration catalog.
- Arrays use PostgreSQL arrays only when ordering, duplication, atomic replacement, and
  query requirements make them a faithful value type; otherwise they become child
  tables.
- Every foreign key states deletion behavior explicitly. Cascades are never inferred
  from ORM defaults.
- Every high-volume query, sort, uniqueness rule, expiration scan, lease operation, and
  reconciliation lookup receives an explicit reviewed index.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--persistence-access"></a>
##### Persistence access

Flyway versioned SQL is the sole production schema source. A database created from an
empty cluster by applying all migrations is canonical. Applied migration checksums may
not be rewritten; corrections use new forward migrations.

jOOQ code generation consumes the canonical migrated schema and produces compile-time
table, column, key, and record types. Generated sources are reproducible and are not
hand-edited. Removing or renaming schema elements must produce corresponding compilation
failures in affected adapters.

Existing domain persistence interfaces remain the application boundary. New
`Postgres...` adapters implement them with jOOQ and explicit transactions. Controllers,
services, domain models, and frontend code do not depend on `DSLContext`, generated
jOOQ types, JDBC records, or PostgreSQL-specific exceptions.

The transition bridge can select `mongodb` or `postgresql` only at application startup.
Exactly one backend is active for the process, the chosen backend is visible in health
and deployment evidence without exposing credentials, and startup rejects an ambiguous
or missing production selection. There is no application dual write.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--concurrency-and-lifecycle-semantics"></a>
##### Concurrency and lifecycle semantics

- Routine multi-table aggregate mutations use PostgreSQL transactions.
- Optimistic concurrency uses a version column and conditional `UPDATE ... WHERE
  version = expected`, with a single-row success requirement.
- Lease acquisition, renewal, and release use database time plus atomic conditional
  statements, `INSERT ... ON CONFLICT`, and row locking where necessary. Application
  host clocks do not decide lease ownership.
- Counters, floor-at-zero decrements, ownership heartbeats, compare-and-set state
  transitions, and claim/complete job flows remain atomic at the database boundary.
- MongoDB TTL indexes become indexed expiration columns plus bounded PostgreSQL-backed
  cleanup jobs. Cleanup is observable, idempotent, batch-limited, and tested for the
  same eligibility semantics as the prior TTL behavior.
- Cursor pagination retains stable ordering and tie-breakers. Offset pagination is not
  introduced on unbounded paths that currently use stable cursors.
- Queries that previously used Mongo aggregation are rewritten as explicit joins,
  grouped queries, common table expressions, window functions, or bounded application
  composition, with result-parity and plan evidence.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--canonical-migration-catalog"></a>
#### Canonical Migration Catalog

The checked-in 52-kind Mongo manifest becomes the source inventory for a new canonical
Mongo-to-PostgreSQL migration catalog. Each kind entry must declare:

- source collection, kind, persisted schema version, identifier type, and source owner;
- target schema, tables, keys, and load order;
- field-to-column transformations, child-table decomposition, and JSONB justification;
- identifier preservation and foreign-key resolution rules;
- null, missing, enum, timestamp, numeric, Unicode, array, and nested-value handling;
- uniqueness, optimistic version, expiration, and deletion semantics;
- source and target canonicalization rules for record-level hashing;
- per-kind counts, relationship counts, and other reconciliation invariants;
- representative persistence-port queries that prove behavioral parity;
- transformer version and the minimum bridge release that understands it.

A kind cannot enter a shadow or production migration until the catalog entry, target
schema, transformer, PostgreSQL adapter, contract tests, and reconciliation checks are
complete. Unknown source kinds or fields fail closed.

Migration provenance is stored in protected migration ledgers, not in user-facing domain
tables unless the domain itself requires source identity. The ledger records the source
kind/identifier, transformer version, canonical hashes, batch/checkpoint state, target
release, and publication status needed for restart and audit.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--migration-engine"></a>
#### Migration Engine

The guarded migration engine is a bounded Java command that is unavailable from public
web routes and cannot be invoked by the ordinary running website role. It:

1. validates the exact Mongo source database, PostgreSQL target database, catalog
   version, application release, role, lock, and operating mode;
2. reads MongoDB only through approved kind-scoped boundaries;
3. orders source kinds and target tables according to explicit dependency metadata;
4. writes batch-bounded staging tables using deterministic transformers;
5. records durable checkpoints after committed batches;
6. validates the complete staged kind before one transactional publish step;
7. performs exact idempotent upserts and, only against a proven frozen source, exact
   deletion of target records absent from that source;
8. records canonical source/target hashes and reconciliation evidence;
9. resumes after interruption without guessing whether a batch or publication succeeded;
10. never mutates MongoDB.

Batch commits make progress durable in staging but never make an incomplete kind visible
to the PostgreSQL application adapter. Publication is transactional within PostgreSQL.
Re-running the same catalog and source state produces the same target state and hashes.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--shadow-rehearsals"></a>
#### Shadow Rehearsals

While MongoDB remains authoritative, PostgreSQL schemas are migrated and populated as a
non-public shadow. Rehearsals may replace shadow target state because no production
writer or public application reads it.

Every rehearsal records:

- exact source and target database identities without credentials;
- catalog, transformer, Flyway, application, and PostgreSQL versions;
- start/end time, batch sizes, checkpoints, and peak resource use;
- per-kind and per-table counts;
- canonical record hashes reconstructed from normalized target rows;
- foreign-key coverage and orphan counts;
- unique/check/enum/nullability constraint results;
- required index definitions and sequence/identity state;
- representative Mongo/PostgreSQL query-result parity;
- failure and resume behavior;
- estimated stopped-writer final-delta and acceptance duration.

Counts alone do not establish parity. At least one full migration rehearsal uses a
protected restored production-data clone, and a production shadow rehearsal must prove
enough margin to complete final reconciliation and acceptance inside the assumed
30-minute window. If the proven margin is insufficient, production cutover is blocked
and the design returns for review rather than silently extending downtime.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--production-cutover"></a>
#### Production Cutover

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--preconditions"></a>
##### Preconditions

Production cutover requires:

- all 52 catalog entries complete and reconciled;
- empty-database and upgrade-path Flyway verification;
- reproducible jOOQ generation;
- full Mongo and PostgreSQL persistence-port contract suites;
- a current full MongoDB backup with SHA-256 and successful restore proof;
- current PostgreSQL physical and logical backup restore proof;
- successful protected production-data rehearsal within the time budget;
- exact expected source kinds, counts, hashes, indexes, and schema version;
- exact expected PostgreSQL schemas, migrations, roles, grants, constraints, and indexes;
- a packaged bridge release validated on a non-8080 port;
- a protected deployment lock, suspended automatic deployment, exact process inventory,
  and an enumerated writer-stop plan;
- an explicit rollback command sequence proven against the same bridge release.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--authority-transfer-sequence"></a>
##### Authority transfer sequence

1. Acquire the protected deployment lock and enable maintenance mode.
2. Suspend service recovery and automatic deployment for the bounded window.
3. Stop the website, media worker, schedulers, importers, and every other Mongo writer.
4. Prove production port 8080 is closed, writer processes are absent, and Mongo
   connections/writes have ceased.
5. Create the final full Mongo archive, record its SHA-256, and prove it can be parsed
   and restored into an isolated target.
6. Reconcile the preloaded PostgreSQL state against the now-frozen Mongo source,
   including exact upserts and deletes authorized by the catalog.
7. Re-run all source/target counts, canonical hashes, foreign keys, constraints,
   indexes, Flyway state, role grants, and sequence checks.
8. Start the packaged bridge release against PostgreSQL on a non-8080 port with
   scheduling and all application mutations disabled.
9. Run read-only local acceptance across every bounded context and Mission Control.
10. If any pre-authority acceptance fails, stop the candidate and restart the same
    bridge release against untouched MongoDB.
11. If all pre-authority acceptance passes, rotate the production listener to the
    PostgreSQL-backed release while mutations remain disabled.
12. Verify local and public liveness/readiness, key routes, asset identity, and
    representative reads on the production listener.
13. Enable PostgreSQL application writes exactly once and record the authority marker.
14. Run bounded write/read/update/delete smoke flows plus lease/job and optimistic-lock
    checks, then restore ordinary scheduling and traffic.
15. Re-enable service recovery and automatic deployment only after they are proven to
    understand the PostgreSQL authority marker and schema state.
16. Release the deployment lock and begin the 14-day PostgreSQL soak.

The authority flip occurs at step 13. Before it, MongoDB remains the rollback authority.
After it, MongoDB is stale and must never be selected automatically.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--failure-handling-and-recovery"></a>
#### Failure Handling and Recovery

- Any unknown kind, field, enum, identifier, numeric conversion, timestamp conversion,
  duplicate logical identity, unresolved reference, hash mismatch, count mismatch,
  missing constraint/index, partial source read, checkpoint inconsistency, or privilege
  mismatch stops the affected stage.
- No source record is skipped, defaulted, truncated, or detached merely to finish a run.
- A staging failure removes or resumes only marker-owned staging state; it cannot make a
  partial kind visible.
- A cutover failure before the authority flip stops PostgreSQL acceptance and restarts
  the same bridge release on the untouched frozen MongoDB source.
- After PostgreSQL writes are enabled, rollback to MongoDB is prohibited because it
  would discard or fork new PostgreSQL writes. The site returns to maintenance while
  operators restore PostgreSQL, deploy a PostgreSQL-compatible prior release, or apply
  a forward fix.
- No failed recovery starts an application writer against an unproven database state.
- Destructive commands require exact database, schema/table/path allowlists, release,
  migration marker, lock ownership, service/process identity, backup hash, and dry-run
  impact output.
- ACL denial at protected production boundaries is not repaired by weakening ACLs.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--postgresql-backup-and-restore"></a>
#### PostgreSQL Backup and Restore

The production recovery model includes:

- continuous WAL archiving sufficient for point-in-time recovery;
- scheduled physical base backups;
- daily custom-format logical dumps for portable object/data recovery;
- SHA-256 and size records for backup artifacts;
- backup-age, WAL/archive, and failed-job monitoring;
- encrypted or ACL-protected storage outside the live data directory;
- retention rules that bound disk usage without deleting the only verified recovery
  point;
- regular automated verification plus scheduled full restore drills into an isolated
  protected target;
- documented database, role, schema, extension, locale, collation, and time-zone restore
  requirements;
- post-restore Flyway, constraint, index, reconciliation, and application acceptance.

The implementation plan must bind these requirements to exact protected paths, tasks,
service identities, schedules, and retention counts after inspecting the live Windows
operations boundary. Repository documentation and Mission Control must expose backup
freshness and restore-verification status without exposing secrets or user data.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--monitoring-and-operations"></a>
#### Monitoring and Operations

Windows production tooling and Mission Control add bounded PostgreSQL checks for:

- service state, startup type, local listener, and readiness;
- active application backend and Flyway schema version;
- connection count, pool saturation, rejected connections, and role identity;
- long-running transactions, blocking locks, deadlocks, and failed transactions;
- database/schema/table/index growth and unexpected objects;
- sequential-scan and query-plan regressions on critical paths;
- autovacuum/analyze health, dead tuples, wraparound risk, and maintenance age;
- WAL generation, archive success/failure, recovery-point age, and backup freshness;
- disk capacity for data, WAL, staging, and backup paths;
- scheduled cleanup, lease, and job health.

Operational commands distinguish read-only inspection from mutation. Schema migration,
restore, role management, cutover, and retirement remain confirmation-gated and produce
redacted evidence.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--mongodb-soak-and-retirement"></a>
#### MongoDB Soak and Retirement

Immediately after PostgreSQL cutover, MongoDB is stopped and disabled so no component
can write to it. Its exact final data directory and final verified archive remain frozen.
The bridge release retains an explicit emergency pre-authority Mongo backend only as
historical rollback capability; production configuration remains locked to PostgreSQL.

The 14-day soak requires:

- continuous healthy PostgreSQL-backed production operation;
- no unresolved parity, constraint, performance, or data-integrity finding;
- current point-in-time, physical, and logical backup evidence;
- a successful PostgreSQL restore drill using post-cutover data;
- all public/local acceptance flows and scheduled workloads passing;
- no unexpected Mongo process, listener, connection, or write;
- exact frozen Mongo archive/data identities unchanged.

After the soak passes, a final retirement release removes MongoDB dependencies, adapters,
query/update types, configuration, migration runner, inventory, backup/cutover tooling,
service dependencies, tests that assert Mongo behavior, and dormant backend selection.
It retains only historical documentation and the bounded offline archive-handling records
needed for the 90-day retention period.

MongoDB service uninstall and exact live-data-directory removal occur only after:

- the final PostgreSQL-only release passes full CI and production acceptance;
- the PostgreSQL restore drill and current backup hashes pass;
- a dry-run reports the exact service, files, directories, and configuration to remove;
- no other application or user-owned data shares those targets;
- the protected deletion operates only on resolved allowlisted absolute paths.

The final pre-cutover Mongo archive is retained for 90 days from authority transfer. Its
later deletion is an exact evidence-gated operation and does not delete PostgreSQL
backups, Builder evidence, or migration reconciliation reports.

The initiative is not complete merely because the site runs on PostgreSQL. Completion
requires the final PostgreSQL-only application, Mongo service/data retirement, and
90-day archive-retention action to be durably tracked. The work may close before the
scheduled archive deletion only if a durable dated follow-up owns that exact action and
all active Mongo runtime/service/data have already been removed.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--verification-strategy"></a>
#### Verification Strategy

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--persistence-contract-parity"></a>
##### Persistence contract parity

During transition, the same backend-neutral persistence-port contract suite runs against
real MongoDB and PostgreSQL. It covers:

- create, read, update, delete, bulk, and idempotent save behavior;
- exact and case-insensitive lookups;
- pagination, stable ordering, cursors, limits, and tie-breakers;
- optimistic concurrency and conditional mutation;
- unique, sparse/optional, null, and missing-value semantics;
- leases, claims, heartbeats, renewals, releases, and contention;
- atomic counters and floor-at-zero updates;
- expiration eligibility and bounded cleanup;
- domain joins, aggregations, projections, and counts;
- deletion cascades/restrictions and account-lifecycle behavior;
- exception translation at the domain boundary.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--schema-and-migration-tests"></a>
##### Schema and migration tests

- Build the current schema from an empty PostgreSQL 18 database using Flyway.
- Upgrade representative prior schema versions and reject migration checksum drift.
- Regenerate jOOQ sources and prove clean reproducibility.
- Cover all 52 kinds with representative and adversarial fixtures.
- Cover legacy identifiers, missing/null values, enum evolution, timestamp precision and
  zones, Unicode, decimals, arrays, nested values, external JSON, expiration, duplicates,
  broken references, large batches, interruption boundaries, resume, and repeat runs.
- Prove record-level source/target canonical hashes and relationship reconciliation.
- Prove MongoDB remains unmodified during every migration path.
- Prove an incomplete kind is never visible to PostgreSQL adapters.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--architecture-and-security-tests"></a>
##### Architecture and security tests

- Domain/application code cannot import MongoDB, jOOQ, JDBC, or generated schema types.
- MongoDB dependencies remain confined to transitional adapters and the guarded migrator,
  then disappear in the final retirement release.
- jOOQ and SQL remain confined to PostgreSQL adapters and migration infrastructure.
- Every target table and migration catalog entry has one owning bounded context.
- The application role cannot execute DDL, manage roles, access privileged schemas, or
  invoke the guarded migrator.
- The pgAdmin production viewer cannot insert, update, delete, truncate, alter, drop,
  create, grant, execute privileged functions, or access server files.
- PostgreSQL and pgAdmin are loopback-only and secrets do not enter logs or reports.
- Local/test startup fails when the database name is not exactly `test`.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--ci-and-local-runtime"></a>
##### CI and local runtime

CI provisions the real supported PostgreSQL major version and creates database `test` on
every supported operating-system lane. Each suite uses a disposable schema. CI and local
verification include focused tests, the full Gradle verification gate, JavaScript tests,
PowerShell 7 and required Windows PowerShell 5.1 operations tests, migration/restart
matrices, and security review.

The packaged candidate runs on a non-8080 port with exact URL, request/input, response
status/body, active database, Flyway version, and backend evidence. Runtime acceptance
exercises authentication, accounts/administration, content/social, messaging and
notifications, federation, Music, shared-folder state/workflows, vehicles/location,
What's for Lunch, Canes tracking, scheduled work, leases, and Mission Control.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--performance-and-capacity"></a>
##### Performance and capacity

- Record baseline and PostgreSQL results for latency-sensitive and high-volume queries.
- Capture `EXPLAIN (ANALYZE, BUFFERS)` or an equivalent safe plan for approved critical
  queries against representative data.
- Prove required indexes are used and query result limits remain bounded.
- Test connection-pool sizing, lease/job contention, deadlock handling, cleanup batches,
  cursor pagination, large imports, and shadow/final migration throughput.
- Record PostgreSQL data, index, WAL, staging, and backup storage estimates with safe
  headroom on the production host.
- Block cutover when the stopped-writer final sequence lacks demonstrated margin inside
  30 minutes.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--production-acceptance"></a>
#### Production Acceptance

Final acceptance must record:

- exact application release, PostgreSQL release, Flyway version, catalog version, and
  authority marker;
- PostgreSQL service state/startup type, loopback listener, database identity, roles,
  grants, schemas, tables, constraints, indexes, extensions, and unexpected-object scan;
- all 52 source-kind and target-table counts, canonical hashes, relationships, and
  reconciliation results;
- current Mongo final-archive path identifier, size, SHA-256, and restore proof without
  exposing credentials or data;
- current PostgreSQL physical/logical/WAL recovery evidence and isolated restore proof;
- non-8080 candidate URLs/commands, inputs, status, bodies/output, and pass/fail results;
- listener rotation and local/public liveness/readiness with exact status and body;
- representative reads and bounded write/read/update/delete flows for every domain;
- authentication, authorization, lease, job, cleanup, optimistic-lock, and failure-path
  behavior;
- pgAdmin `test` read/write and production-viewer read-only connections, including a
  negative production mutation test;
- website, PostgreSQL, media-worker, and cloudflared expected Windows service states;
- MongoDB stopped/disabled state after authority transfer;
- automatic deployment and service recovery compatibility with PostgreSQL schema and
  authority markers;
- no unexpected process, port, database, schema, table, writer, or credential exposure.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--delivery-phases"></a>
#### Delivery Phases

1. **Foundation:** install and secure local/test PostgreSQL, establish database `test`,
   add Flyway/jOOQ, schema build, role model, and pgAdmin connections without changing
   production authority.
2. **Relational slices:** implement schema and PostgreSQL adapters by bounded context,
   with dual-backend contract parity but single-backend runtime selection.
3. **Migration engine:** complete the 52-kind catalog, deterministic transformers,
   staging/publication, checkpoints, reconciliation, and protected operations.
4. **Rehearsal:** run disposable, restored-production-clone, candidate-runtime, and
   production-shadow rehearsals until parity and time margin pass.
5. **Authority transfer:** perform the stopped-writer final reconciliation, read-only
   acceptance, production listener rotation, and one-way PostgreSQL write enablement.
6. **Soak:** monitor PostgreSQL production and prove post-cutover recovery for 14 days
   while Mongo remains stopped and frozen.
7. **Retirement:** ship the PostgreSQL-only release, remove Mongo service/live data under
   exact guards, retain the verified final archive for 90 days, and close the initiative
   with a durable owner for its scheduled deletion.

Each phase requires its own reviewable commits, tests, Builder updates, and rollback or
recovery evidence. A locally edited adapter or running PostgreSQL service is a checkpoint,
not completion.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- **Relational semantic drift:** Mongo missing/null, arrays, nested structures, and
  conditional updates do not map automatically. Mitigation: per-kind contracts,
  adversarial fixtures, canonical hashes, and shared backend contract tests.
- **Hidden Mongo coupling:** explicit operations still appear widely in adapters and
  operational tools. Mitigation: architecture enforcement, bounded-context slices, and a
  final zero-dependency scan.
- **Foreign-key discovery:** legacy data may contain relationships Mongo did not enforce.
  Mitigation: shadow orphan reports; no silent deletion or fabricated parent.
- **Cutover overrun:** final delta or verification may exceed 30 minutes. Mitigation:
  repeated production-scale rehearsals and a hard pre-stop margin gate.
- **Unsafe post-flip rollback:** Mongo becomes stale after PostgreSQL writes. Mitigation:
  explicit one-way authority marker and PostgreSQL-native restore/forward-fix recovery.
- **GUI mutation:** a visual tool can make production edits easy. Mitigation: a dedicated
  database-enforced viewer role and no privileged pgAdmin credentials.
- **Single-host failure:** application and database share the production host. Mitigation:
  protected off-data-directory backups, WAL/PITR, restore drills, and capacity monitoring.
- **Test contamination:** local or automated work could touch the wrong database.
  Mitigation: database `test` only, disposable schemas, roles without production access,
  and fail-fast name guards.
- **Premature Mongo deletion:** a healthy first restart does not prove recovery.
  Mitigation: 14-day frozen soak, PostgreSQL restore proof, final PostgreSQL-only release,
  exact-path deletion guards, and 90-day archive retention.
- **Dirty checkout damage:** authoritative spoke state is unrelated and stale. Mitigation:
  refreshed isolated worktrees and explicit status verification before every phase.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--acceptance-criteria"></a>
#### Acceptance Criteria

The migration is complete only when:

1. PostgreSQL is the sole writable and sole runtime database for every website domain.
2. All 52 source kinds reconcile to typed relational target state with exact counts,
   canonical hashes, relationships, constraints, and query behavior.
3. Public HTTP, authorization, scheduled work, and user-visible feature behavior pass
   automated, alternate-port, and production acceptance.
4. Flyway can build the schema from empty and upgrade supported prior states; generated
   jOOQ sources are reproducible and all schema changes are forward migrations.
5. Local development, CI, and manual database testing use only database `test`, with
   disposable-schema isolation and no ability to connect to production.
6. PostgreSQL roles, loopback networking, pgAdmin production-viewer restrictions, and
   secret-handling tests pass.
7. Point-in-time, physical, and logical PostgreSQL recovery paths have current verified
   evidence, including an isolated post-cutover restore.
8. The final stopped-writer cutover completes inside the approved window and records the
   one-way PostgreSQL authority marker.
9. The 14-day soak passes without unresolved integrity, parity, performance, operational,
   or recovery findings.
10. The final application contains no MongoDB runtime dependency, adapter, backend
    selector, service dependency, active configuration, or ordinary operational command.
11. MongoDB is uninstalled and its exact live data/configuration is removed only after
    the approved evidence gate; the final verified archive remains protected for 90 days.
12. pgAdmin 4 Desktop is installed with a working read/write `test` connection and a
    proven read-only production viewer connection.
13. Builder contains the approved plan, task/update/review records, test evidence,
    production closeout, and a durable owner/date for final archive deletion if it occurs
    after initiative closure.

<a id="source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md--open-questions"></a>
#### Open Questions

None. Exact table/column mappings, SQL migrations, protected Windows paths, installer
checksums, backup schedules, batch sizes, connection-pool values, and literal code-edit
locations must be derived from current `origin/main` and the protected host during the
implementation plan. If any source kind cannot preserve its identity, relationship,
query, expiration, uniqueness, or concurrency semantics under this design, planning must
return to design review before implementation continues.

<!-- /migrated-source: docs/specs/2026-08-13-christopherbell-dev-postgresql-migration.md -->

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md"></a>
## 2026-08-13 | work | christopherbell.dev PostgreSQL Migration

Original source: `docs/work/2026-08-13-christopherbell-dev-postgresql-migration.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `96ed2de31a6e3f224d8db4612d93788050110f7027451423cc5d84d3b6a9baef`.

<!-- migrated-source: docs/work/2026-08-13-christopherbell-dev-postgresql-migration.md -->
<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--christopherbelldev-postgresql-migration"></a>
### christopherbell.dev PostgreSQL Migration

- Status: `active`
- Owner context: Builder hub coordinating architecture, relational redesign,
  migration rehearsals, native-Windows production cutover, PostgreSQL acceptance,
  MongoDB retirement, and closeout
- Related spec: [PostgreSQL Migration](#source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md)

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--objective"></a>
#### Objective

Replace MongoDB with PostgreSQL as the website's sole durable database, remodel the
current 52 persisted kinds into typed relational domain schemas, migrate every
production record through a rehearsed and reversible pre-cutover process, and retire
MongoDB only after PostgreSQL production and recovery evidence pass the approved soak.

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--owner-and-scope"></a>
#### Owner and Scope

- Builder hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `azurras/christopherbell.dev`
- Authoritative spoke path: `A:\Projects\christopherbell.dev` (preserve unrelated dirty state)
- Implementation surface: a clean isolated worktree refreshed from current `origin/main`
- Verified planning baseline: `origin/main` at `e073823d14ffed0b4c113707d16c0ad0cfe1b7fa`
- Current persistence baseline: 14 MongoDB domain collections, 52 canonical kinds,
  126 manifest-defined indexes, and explicit kind-scoped persistence boundaries
- Target: PostgreSQL 18 on native Windows, one production database named
  `christopherbell`, typed bounded-context schemas, Flyway migrations, jOOQ adapters,
  pgAdmin 4 Desktop, and no remaining MongoDB runtime dependency after retirement
- Development and database-test target: PostgreSQL database `test` only, using
  disposable schemas for automated-test isolation
- Cutover target: rehearsed shadow imports followed by a writer-stopped final
  reconciliation and an assumed maximum 30-minute maintenance window

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--related-artifacts"></a>
#### Related Artifacts

- Project specification: [PostgreSQL Migration](#source-docs-specs-2026-08-13-christopherbell-dev-postgresql-migration-md)
- Prior MongoDB consolidation closure: [Domain Collection Consolidation](2026-08-12-christopherbell-dev.md#source-docs-work-closures-2026-08-12-christopherbell-dev-domain-collection-consolidation-md)
- Prior MongoDB consolidation work: [Domain Collection Consolidation](2026-08-10-christopherbell-dev.md#source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- Implementation plan: [PostgreSQL Migration Implementation Plan](../implementation-plans/2026-08-13-christopherbell-dev-postgresql-migration.md)
- Spoke task, reviews, test reports, production evidence, closure, and session memory:
  create during the approved delivery loop

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--approved-decisions"></a>
#### Approved Decisions

- PostgreSQL will be the sole durable production database; no permanent hybrid remains.
- The target is a domain-relational model, not a lift of Mongo envelopes into JSONB.
- Flyway owns versioned DDL and jOOQ provides explicit, generated, type-safe SQL access
  behind the existing domain persistence ports.
- PostgreSQL runs as a loopback-only native Windows service on the production host.
- Migration uses repeated shadow imports and reconciliation while MongoDB remains
  authoritative, followed by one stopped-writer authority transfer; there is no
  production dual-write period.
- Local development and every database-backed test use PostgreSQL database `test`.
- pgAdmin 4 Desktop is a required visual database viewer. Its production connection
  uses a database-enforced read-only role; privileged roles are never registered in it.
- Before authority transfer, rollback returns to untouched MongoDB. After PostgreSQL
  writes begin, recovery remains PostgreSQL-native and never discards new writes by
  silently switching back to stale MongoDB.
- MongoDB remains stopped and frozen for a 14-day soak. Its verified final archive is
  retained for 90 days before exact, evidence-gated deletion.

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--guardrails"></a>
#### Guardrails

- Do not modify the authoritative spoke checkout or its unrelated dirty state.
- Do not install PostgreSQL, pgAdmin, change a Windows service, touch production data,
  or edit website code until the written spec and implementation plan are approved.
- Invoke `write-jane-street-style-code` before production source, test, migration,
  reusable script, or executable configuration changes.
- Keep the website one Spring Boot deployable and preserve public HTTP, authorization,
  frontend, and externally visible domain behavior.
- Fail closed on unknown kinds, fields, identifiers, enum values, references, counts,
  hashes, constraints, indexes, roles, versions, databases, processes, paths, locks,
  services, or backup state.
- Never use H2 as a PostgreSQL substitute. Local and automated database work must
  verify the active database is exactly `test` before it starts.
- Do not register the owner, migrator, or website-runtime credentials in pgAdmin.
- Do not expose database credentials, connection strings containing secrets, service
  command lines, archive paths with secrets, or user data in logs or Builder evidence.
- Do not weaken protected production ACLs.
- Do not start a PostgreSQL writer until the frozen-source reconciliation, read-only
  candidate acceptance, and rollback-readiness gates all pass.
- After the PostgreSQL authority flip, do not automatically fall back to MongoDB.
- Do not remove MongoDB code, service state, or exact data until the 14-day retirement
  gate and PostgreSQL restore evidence pass.

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--current-state"></a>
#### Current State

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--verified-resumption-on-2026-09-05-supersedes-the-historical-snapshot-below"></a>
##### Verified resumption on 2026-09-05 (supersedes the historical snapshot below)

- Maintenance downtime up to 30 minutes is already approved by Christopher; do not
  request the same approval again. Spring Data JPA/JDBC replaced jOOQ in PR #1376.
- PR #1385 was still open despite all checks passing. Astra resumed its delivery,
  retaining the clean isolated `postgresql-cutover` worktree and preserving the
  authoritative checkout.
- Read-only elevated production evidence: journal is `ROLLED_BACK`, no authority
  sidecar exists, and source snapshot emits five Mongo log lines plus one valid
  evidence record whose catalog digest matches the release.
- Production journal checksum passes only when timestamp strings are preserved;
  default PowerShell JSON DateTime conversion changes its canonical hash. The
  corrected reader uses `-DateKind String` with a real disk-round-trip regression.
- Additional pre-cutover defects found and being corrected: local-date writer
  lease rejected by Java Instant.parse; website still depending on MongoDB;
  persistent writer-start marker not advanced after cutover; and mutating startup
  recovery incompatible with read-only candidate acceptance.
- Full ops suite passed 795 tests, zero failures, 28 skips after the PowerShell
  corrections. Java startup recovery profile coverage and final PR checks remain
  underway. No new production authority transfer has been attempted this session.
- Ordinary deployment still uses Mongo backup/restore. Pause automatic deployment
  before cutover and implement PostgreSQL-aware deployment before reenabling it.
- Preserve the failed attempt's journal and sidecars before retrying; do not bypass
  checks or erase recovery evidence. The existing terminal ROLLED_BACK state is not
  automatically retried by the public command.
- Retirement requires 14 full days after verified PostgreSQL authority and restore
  proof; retain the final Mongo archive for 90 days. Calendar time before cutover
  does not count toward soak.

- Tasks 1 through 8 are implemented, reviewed, rehearsed, and merged through
  [PR #1370](https://github.com/azurras/christopherbell.dev/pull/1370) as
  `bca4231b4d36bdad963a4d33645b5bb61d88795c`.
- The Task 9 guarded production command is implemented, reviewed, and merged through
  [PR #1372](https://github.com/azurras/christopherbell.dev/pull/1372) as
  `ea6cead1a4fa14bd4ba3c5de65bb8dda91501d0c`; it has not been run in production.
- PostgreSQL 18/Flyway/jOOQ foundations, typed adapters for all 52 source kinds,
  the guarded migration engine, native Windows operations, and shadow/candidate
  verification are complete.
- Repeated live-source and 63,230-document restored-archive rehearsals reconciled all
  52 kinds. A PostgreSQL-only candidate passed the exact HTTP, role, scheduler,
  capacity, plan, latency, security, and cleanup matrix.
- Production Mongo, PostgreSQL 16, and the website listener remain unchanged. No
  FINALIZE, production authority marker, service dependency change, or cutover has run.

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--blockers"></a>
#### Blockers

Task 9 requires an explicitly approved maintenance window before it can stop production
writers, take the final backup, transfer authority, or rotate the production listener.
This is an intentional authorization gate because the operation interrupts production
and the post-authority rollback direction is PostgreSQL-forward only.

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--validation-state"></a>
#### Validation State

- Definitive Task 8 verification passed 2,386 Java tests with zero failures/errors,
  plus JavaScript and PowerShell/Pester gates.
- The PostgreSQL candidate passed 39/39 exact HTTP statuses and latency budgets;
  role separation showed app sessions and zero bridge sessions.
- Final CI passed PostgreSQL 18 jOOQ generation, Java/JavaScript/Actions CodeQL,
  dependency review, and Java 25 builds on macOS, Ubuntu, and Windows.
- Task 9's definitive local gate passed 2,268 website tests and 123 cbell-lib tests
  with zero failures/errors. The guarded cutover state machine passed 16/16, operations
  Pester passed 753 with 28 expected skips, and the read-only source snapshot plus live
  migration package passed against disposable MongoDB and PostgreSQL 18.4 `test` databases.
- PR #1372 passed all nine GitHub checks and merged to refreshed `origin/main` as
  `ea6cead1a4fa14bdad963a4d33645b5bb61d88795c`.
- Independent review found no remaining Critical, Important, Blocker, or Warning
  finding in the Task 8 scope. The merged tree exactly matches the reviewed branch.
- The authoritative dirty spoke checkout was preserved throughout isolated worktree
  development, testing, PR integration, and merge.

<a id="source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md--next-steps"></a>
#### Next Steps

1. Obtain explicit approval for the up-to-30-minute Task 9 maintenance window.
2. Execute the merged `postgres-cutover -ConfirmPostgreSqlCutover` boundary, which owns
   the final backup, writer freeze, all-kind FINALIZE/reconciliation,
   alternate-port acceptance, one-way authority marker, and production listener rotation.
3. Monitor PostgreSQL for 14 full days and prove post-cutover restore before Task 10
   removes Mongo runtime code, service state, and exact live data.

<!-- /migrated-source: docs/work/2026-08-13-christopherbell-dev-postgresql-migration.md -->

