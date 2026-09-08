# 2026-08-10 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/specs/2026-08-10-christopherbell-dev-domain-collection-consolidation.md](#source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- [docs/spoke-tasks/2026-08-10-christopherbell-dev-domain-collection-consolidation.md](#source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- [docs/work/2026-08-10-christopherbell-dev-domain-collection-consolidation.md](#source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md"></a>
## 2026-08-10 | specs | christopherbell.dev Domain Collection Consolidation

Original source: `docs/specs/2026-08-10-christopherbell-dev-domain-collection-consolidation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `f941a1aaa1ae9ad13e4d98f059f17410297b84b5655dcaff26fe3b337028e202`.

<!-- migrated-source: docs/specs/2026-08-10-christopherbell-dev-domain-collection-consolidation.md -->
<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--christopherbelldev-domain-collection-consolidation"></a>
### christopherbell.dev Domain Collection Consolidation

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--purpose"></a>
#### Purpose

Reduce the production `christopherbell` MongoDB database from 48 physical
collections to approximately 14 domain-owned collections, remove every
superseded source collection during the same guarded maintenance cutover, and
preserve the website's HTTP behavior, data, uniqueness constraints, retention
rules, and operational safety.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--background"></a>
#### Background

Production already uses one MongoDB process and one database. The first
consolidation moved one queue document and one radio document into
`music_runtime_state`, but retained the two legacy collections for rollback.
The user rejected that narrow result and approved an aggressive structural
consolidation with these decisions:

- Target approximately 15 physical collections; the proposed model has 14.
- Use one guarded maintenance cutover instead of a multi-release dual-write
  period.
- Delete superseded collections immediately after full migrated-state and
  runtime verification.
- Prefer a materially smaller, domain-oriented collection list over preserving
  one physical collection per Java document type.

The verified production baseline on 2026-08-10 is 48 collections and 164
indexes. The largest active datasets include 33,791 ZIP-coordinate documents,
7,340 restaurant documents, 7,035 shared-folder audit events, 4,328 music radio
history events, 2,284 scheduled collector runs, and 1,549 music tracks.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--goals"></a>
#### Goals

1. Produce a stable physical collection model with approximately one collection
   per bounded domain.
2. Preserve every existing document and required index semantic.
3. Make document kind and ownership explicit in every shared collection.
4. Prevent cross-kind identifier collisions and cross-kind query leakage.
5. Remove all superseded source collections in the successful maintenance
   transaction window.
6. Leave production, automatic deployment, backup, rollback, and collection
   inventory tooling compatible with the new schema.
7. Present the MongoDB collection inventory as a concise domain-level view.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--non-goals"></a>
#### Non-Goals

- Do not combine all data into one universal collection.
- Do not merge data across the `christopherbell` database boundary.
- Do not change public HTTP routes, request/response contracts, authorization,
  or user-visible feature behavior.
- Do not weaken unique constraints, TTL behavior, audit retention, or
  optimistic concurrency.
- Do not delete backup archives or unrelated historical release artifacts.
- Do not retain compatibility reads from superseded collections after the
  successful cutover.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--target-physical-collections"></a>
#### Target Physical Collections

| Target | Source document kinds and collections |
|---|---|
| `accounts` | accounts, account follows, trust relationships, account deletion jobs |
| `sessions` | browser sessions and conversation archive states |
| `communications` | messages, notifications, notification preferences, delivery guards, and rate limits |
| `content` | posts, post likes, post reports, hidden threads, and link-preview cache entries |
| `federation` | federation scan state and outbound delivery jobs |
| `music` | tracks, playlists, metadata edits, runtime state, radio history, and access attempts |
| `whatsforlunch` | restaurants, votes, favorites, preferences, sessions, daily picks, import state, and import previews |
| `shared_folder` | audit events, maintenance leases, media jobs, mutation recovery, radio state, recycle items, and upload sessions |
| `vehicles` | vehicles, VIN decode cache, and import state |
| `location` | ZIP coordinates and ZIP import state |
| `canes_box_tracker` | price snapshots |
| `application_runtime` | application leases and scheduled collector runs |
| `application_migrations` | migration ledger |
| `admin_activity` | administrative audit activity and command-center pending actions |

The successful cutover drops all source collections not present in this target
list, including `music_queue_state`, `music_radio_state`, and the intermediate
`music_runtime_state` collection.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--shared-collection-contract"></a>
#### Shared Collection Contract

Every document in a shared physical collection must contain:

- `_id`: the canonical BSON document `{ kind: <_kind>, legacyId: <original
  BSON _id> }`, with fields encoded in that exact order, so identifiers cannot
  collide across document kinds and original BSON identifier types remain
  lossless;
- `_kind`: an exact, lower-case, allowlisted discriminator owned by the target
  domain;
- `schemaVersion`: the kind-specific persisted schema version;
- the original domain fields without lossy conversion.

Repository and store boundaries must always constrain reads, updates, deletes,
counts, and uniqueness checks by `_kind`. A generic unscoped repository API is
not allowed. Each domain owns one mapping layer that translates between domain
IDs and canonical persisted IDs. Runtime code must reject a persisted `_id`
whose `kind` member differs from the document's `_kind`.

Unknown kinds, malformed namespaced IDs, duplicate source IDs, unsupported
numeric BSON types, and unexpected source fields fail migration before any live
rename or deletion.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--index-model"></a>
#### Index Model

Each target collection has one `_id` index plus the union of required
kind-scoped indexes. Indexes that apply to only one kind must use an exact
`partialFilterExpression` on `_kind`. Unique indexes must remain unique within
their kind and retain their existing sparse or partial behavior.

MongoDB does not allow `sparse: true` and `partialFilterExpression` on the
same index. A legacy sparse index moved into a shared target therefore omits
the literal sparse flag and uses one combined partial filter requiring both
the exact `_kind` and existence of the original indexed field. Verification
compares effective index participation and uniqueness semantics, including
absent versus explicit-null fields, rather than requiring an impossible flag
combination.

The migration must build and validate all target indexes before live rename.
The index verifier compares keys, order, uniqueness, sparsity, partial filter,
TTL, collation, and index count. Index consolidation is allowed only when two
kinds have identical semantics; otherwise their partial indexes remain
separate.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--migration-and-maintenance-cutover"></a>
#### Migration and Maintenance Cutover

1. Acquire the protected deployment lock and suspend website service recovery.
2. Create and checksum a fresh `mongodump`; verify it with a dry-run restore.
3. Stop the website writer and prove production port 8080 is closed. MongoDB and
   cloudflared remain running.
4. Restore the backup to an isolated candidate database.
5. Run the complete consolidation against the candidate database using the
   exact release candidate.
6. Verify per-kind source/target counts, canonical BSON checksums, representative
   readbacks, indexes, and absence of unexpected collections.
7. Start the candidate application on the alternate port against the migrated
   candidate database and run the full smoke suite.
8. Re-run the migration against the stopped production database, writing only
   to uniquely named temporary target collections.
9. Re-run exact counts, checksums, document-shape validation, and index
   validation before publication.
10. Rename existing target-name collections to bounded temporary legacy names,
    then rename the validated temporary collections to the 14 target names.
11. Start the new release under an exact schema-direction marker and run local
    liveness, readiness, route, authentication-failure, and public endpoint
    checks.
12. Verify live per-kind counts/checksums and the exact 14-collection catalog.
13. Drop every bounded temporary legacy collection immediately.
14. Verify that no superseded collection exists, restore normal service
    recovery, refresh automatic-deploy tooling, and release the deployment lock.

No collection is dropped before the new release passes both candidate-database
and live-database verification.

MongoDB does not provide one transaction spanning all collection renames.
Publication therefore uses a durable, compare-and-set migration ledger with an
ordered manifest of all old, temporary, and final names. Each per-collection
rename is atomic, and the ledger records the next permitted operation after
every successful rename. The website writer may start only when the ledger is
`TARGET_ACTIVE` and the exact 14-name manifest is complete. Recovery resumes
an incomplete forward publication or reverses the recorded operations under
the same deployment lock; it never infers state from names alone.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--failure-and-rollback-rules"></a>
#### Failure and Rollback Rules

- Any failure before live publication removes only marker-owned temporary
  target collections and leaves the old application and collections active.
- Any failure after live rename but before source deletion restores the original
  names and old release under the same deployment lock.
- Any failure after source deletion restores the verified backup and old release
  while the website remains stopped and recovery remains suspended.
- Cleanup scripts must validate the exact database, collection allowlist,
  migration marker, source and target counts, release SHA, process identity, and
  deployment-lock ownership before a destructive command.
- A failed rollback never starts a writer against an unproven schema direction.
- Backup, migration, rename, deletion, and rollback evidence must not expose
  MongoDB URIs, service command lines, application secrets, or Cloudflare
  credentials.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--application-architecture"></a>
#### Application Architecture

Each of the 14 physical collections has one owning module and one explicit
persistence boundary. Existing Spring Data repositories that assume one Java
type per physical collection must be replaced or adapted behind domain stores.
Controllers and services continue to use domain types and must not depend on
the shared persisted envelope.

The canonical collection catalog and architecture tests must enforce:

- exactly 14 target collection names;
- exactly one owning module per target;
- every mapped kind appears once;
- no source collection name remains in runtime mappings or migration-exempt
  paths;
- no unscoped cross-kind Mongo query is present.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--operational-interfaces"></a>
#### Operational Interfaces

Production tooling must add:

- a read-only consolidation preview showing source/target mapping, counts,
  indexes, estimated bytes, and collision results;
- a guarded consolidation command requiring explicit confirmation;
- a restore command bound to the exact backup and migration marker;
- post-cutover inventory that reports target collection and per-kind counts.

Automatic deployment remains blocked while the consolidation marker is pending,
failed, or requires rollback.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--automated"></a>
##### Automated

- Mapping, namespaced-ID, discriminator, and malformed-BSON unit tests.
- Repository contract tests proving every operation scopes by `_kind`.
- Index-definition tests for exact partial, unique, sparse, TTL, and collation
  behavior.
- Migration tests for all 48 source collections, empty optional sources,
  identifier collisions, stale targets, interrupted publication, and exact
  deletion allowlists.
- Real disposable MongoDB tests for full migration, rename, rollback, checksum,
  index, concurrency, and drop semantics.
- Architecture tests for the 14-name catalog and module ownership.
- Full Java, JavaScript, PowerShell 7, and required Windows PowerShell 5.1
  suites.
- Independent implementation and security reviews before publication.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--production-acceptance"></a>
##### Production acceptance

- Verified backup path, size, SHA-256, and dry-run restore.
- Candidate database migration and alternate-port application smoke evidence.
- Before/after collection and index inventories.
- Per-kind document counts and canonical checksums before and after cutover.
- Exact active release and schema-direction marker.
- Local liveness/readiness and public root responses with status and body.
- MongoDB, website, and cloudflared service states.
- Proof that all superseded source and temporary collections are absent.
- Proof that automatic deployment uses the current protected tool bundle.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--acceptance-criteria"></a>
#### Acceptance Criteria

The work is complete only when:

1. Production contains exactly the approved target collection set, subject only
   to MongoDB system collections.
2. Every pre-cutover document is represented exactly once under its target
   `_kind` and passes canonical checksum verification.
3. All required indexes and application behaviors pass automated and live
   verification.
4. Every superseded source collection has been dropped.
5. The verified backup and tested restore path are retained.
6. The new release and automatic-deploy tooling are active and healthy.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--approved-decisions"></a>
#### Approved Decisions

- Physical target: approximately 15 collections; this design specifies 14.
- Cutover mode: one guarded maintenance window.
- Cleanup: immediate deletion of superseded collections after successful live
  verification.
- Design approach: domain-owned shared collections, not one universal
  collection and not a cosmetic inventory-only grouping.

<a id="source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--open-questions"></a>
#### Open Questions

None. Implementation must stop and return to design review if a source
collection cannot preserve its ID, uniqueness, TTL, or query semantics within
the shared-collection contract.

<!-- /migrated-source: docs/specs/2026-08-10-christopherbell-dev-domain-collection-consolidation.md -->

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md"></a>
## 2026-08-10 | spoke-tasks | Dispatch: christopherbell.dev Domain Collection Consolidation

Original source: `docs/spoke-tasks/2026-08-10-christopherbell-dev-domain-collection-consolidation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `a765fb700599fcebb9fbf6065372de33be7670ab2800135dcc3d126a9c24ea94`.

<!-- migrated-source: docs/spoke-tasks/2026-08-10-christopherbell-dev-domain-collection-consolidation.md -->
<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--dispatch-christopherbelldev-domain-collection-consolidation"></a>
### Dispatch: christopherbell.dev Domain Collection Consolidation

- Status: `closed`
- Work record: [Domain Collection Consolidation](#source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- Specification: [Domain Collection Consolidation](#source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- Implementation plan: [Domain Collection Consolidation](../implementation-plans/2026-08-10-christopherbell-dev-domain-collection-consolidation.md)

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--target"></a>
#### Target

- Repository: `azurras/christopherbell.dev`
- Registered authoritative path: `A:\Projects\christopherbell.dev`
- Isolated implementation path: `A:\Projects\christopherbell.dev-worktrees\domain-collection-consolidation`
- Branch: `codex/domain-collection-consolidation`
- Base: refreshed `origin/main` at `f4bc817d22abba70901fe4f17a93b4e52081085c`

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--objective"></a>
#### Objective

Execute the approved ten-task implementation plan through code, tests, review, PR/CI,
merge, guarded production cutover, immediate deletion of the exact superseded MongoDB
collection allowlist, runtime verification, and Builder closeout.

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--strict-scope"></a>
#### Strict Scope

- Implement exactly the 14 target physical collections and 52-kind manifest in the plan.
- Preserve public behavior, authorization, BSON values, optimistic concurrency, TTL,
  unique/sparse/partial indexes, collation, and retention.
- Replace direct runtime collection ownership with the kind-scoped persistence boundary.
- Add manifest-driven preview/stage/verify/publish/drop/reverse/restore migration behavior.
- Generalize protected Windows schema-direction, deploy, writer-start, inventory, backup,
  candidate, rollback, and automatic-deploy gates for this cutover.
- Do not modify the authoritative checkout or unrelated dirty worktree state.
- Do not touch production until the merged release has passed every Task 8 gate.

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--required-engineering-practice"></a>
#### Required Engineering Practice

- Required skill: `write-jane-street-style-code` before any production source, test,
  reusable script, migration, executable configuration, or code-bearing template edit.
- Execute through `superpowers:subagent-driven-development`: one implementer, one
  task-scoped review, and reviewed fix loops before the next task.
- Use TDD: establish the intended RED, implement the minimum complete boundary, then run
  focused and proportionate regression evidence.

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--before-edit-brief"></a>
##### Before-Edit Brief

Each task implementer must complete or refine these fields after read-only investigation
and before changing files:

- Behavior: the exact externally observable and persisted result for that plan task.
- Invariants: kind isolation, BSON/ID fidelity, index/concurrency semantics, and all
  unchanged domain/runtime properties the task must preserve.
- Boundary/API: service-facing ports, shared persistence interfaces, manifest entries,
  and production command contracts changed or consumed by the task.
- Effects and failures: reads/writes/process/service/database effects, ownership, exact
  fail-closed conditions, and redacted failure categories.
- Tests and evidence: first failing test, focused green command, real-boundary evidence
  when applicable, and regression command before commit.

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--validation"></a>
#### Validation

- Run the exact task-level commands in the plan and record discovered/passed/failed/skipped.
- Use private Gradle state and marker-owned disposable MongoDB roots/listeners.
- Run full `:website:test :website:bootJar`, full PowerShell 7 Pester, required Windows
  PowerShell 5.1 subsets, parser checks, disposable Mongo, restored production clone,
  alternate-port HTTP smoke, implementation review, and security diff review before PR.
- Require green CI/CodeQL and exact merge/deploy SHA before production cutover.
- For production, retain before/after inventories, per-kind counts/checksums/indexes,
  backup SHA/dry restore, URL/input/status/body, services, marker, and exact deletion proof.

<a id="source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--expected-return-format"></a>
#### Expected Return Format

Each agent writes the full report to the SDD workspace file named in its dispatch and
returns only:

- `STATUS`: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`
- `COMMITS`: exact commit SHA(s), or `none`
- `TESTS`: one-line commands and pass/fail/skip counts
- `CONCERNS`: one-line residual concerns or `none`

No agent may claim completion without a commit, current-head verification, self-review,
and the required report file. Production changes require the explicit Task 9 protected
command path and may not be approximated with ad hoc shell or Mongo commands.

<!-- /migrated-source: docs/spoke-tasks/2026-08-10-christopherbell-dev-domain-collection-consolidation.md -->

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md"></a>
## 2026-08-10 | work | christopherbell.dev Domain Collection Consolidation

Original source: `docs/work/2026-08-10-christopherbell-dev-domain-collection-consolidation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `d052279ba255b622bac78706f238fa4683e15d50079b2eda197c1a3da596a7fa`.

<!-- migrated-source: docs/work/2026-08-10-christopherbell-dev-domain-collection-consolidation.md -->
<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--christopherbelldev-domain-collection-consolidation"></a>
### christopherbell.dev Domain Collection Consolidation

- Status: `closed`
- Owner context: Builder hub coordinating design, implementation, production migration,
  immediate superseded-collection retirement, and closeout
- Related spec: [Domain Collection Consolidation](#source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--objective"></a>
#### Objective

Reduce the production `christopherbell` MongoDB database from 48 physical collections
to exactly 14 domain-owned collections while preserving every document and index
semantic, then delete all superseded collections during the same verified maintenance
cutover.

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--owner-and-scope"></a>
#### Owner and Scope

- Builder hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `azurras/christopherbell.dev`
- Authoritative spoke path: `A:\Projects\christopherbell.dev` (preserve unrelated dirty state)
- Implementation worktree: create from current `origin/main` before code edits
- Current deployed release: `f4bc817d22abba70901fe4f17a93b4e52081085c`
- Verified production baseline: 48 collections and 164 indexes on 2026-08-10
- Target: the 14 physical collections named in the approved specification
- Destructive boundary: immediate drop of the exact superseded allowlist is authorized
  only after candidate and live counts, checksums, indexes, catalog, runtime, and backup
  restore verification succeed under the protected deployment lock

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--related-artifacts"></a>
#### Related Artifacts

- Project specification: [Domain Collection Consolidation](#source-docs-specs-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- Prior narrow work: [Music Runtime State Consolidation](2026-08-09-christopherbell-dev.md#source-docs-work-2026-08-09-christopherbell-dev-music-runtime-state-consolidation-md)
- Implementation plan: [Domain Collection Consolidation](../implementation-plans/2026-08-10-christopherbell-dev-domain-collection-consolidation.md)
- Spoke task: [Domain Collection Consolidation](#source-docs-spoke-tasks-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)
- Spoke update: [Merged and Production-Verified Delivery](2026-08-12-christopherbell-dev.md#source-docs-spoke-updates-2026-08-12-christopherbell-dev-domain-collection-consolidation-completion-md)
- Spoke review: [Final Delivery Review](2026-08-12-christopherbell-dev.md#source-docs-spoke-reviews-2026-08-12-christopherbell-dev-domain-collection-consolidation-review-md)
- Test report: [Production Test Report](../test-reports/2026-08-12-christopherbell-dev-domain-collection-consolidation-test-report.md)
- Closure: [Domain Collection Consolidation Closure](2026-08-12-christopherbell-dev.md#source-docs-work-closures-2026-08-12-christopherbell-dev-domain-collection-consolidation-md)
- Session memory: [Domain Collection Consolidation](2026-08-12-christopherbell-dev.md#source-docs-session-memory-2026-08-12-christopherbell-dev-domain-collection-consolidation-md)

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--final-state"></a>
#### Final State

- Production contains exactly the approved 14 physical collections, 52 canonical kinds,
  and 126 manifest-defined indexes; every inventory compliance check is true.
- All superseded sources were removed by the guarded cutover after backup, candidate,
  checksum, index, and stopped-writer verification.
- Release `62e1c7193414ecab266a217d221141120c8ecaef` is live; the website, MongoDB,
  and cloudflared services are Running and local/public health checks return HTTP 200.
- The final read-only inventory load-order repair merged in PR #1369 and may ride the
  next ordinary deployment; it is not required for current application or schema health.

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--guardrails"></a>
#### Guardrails

- Use an isolated spoke worktree refreshed from `origin/main`; preserve the dirty
  authoritative checkout and unrelated worktree artifacts.
- Invoke `write-jane-street-style-code` before every production code, test, migration,
  script, or executable configuration edit.
- Prove the full migration against a disposable MongoDB and a restored production-data
  clone on an alternate application port before stopping the production writer.
- Fail closed on any unexpected database, collection, kind, BSON type, ID, count,
  checksum, index, schema marker, release, lock, process, path, or ACL state.
- Do not expose MongoDB URIs, service command lines, application secrets, or Cloudflare
  credentials in logs or evidence.
- Do not drop a source until the exact verified backup has passed a dry restore and the
  target release has passed live database and HTTP acceptance.

<a id="source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md--next-steps"></a>
#### Next Steps

None required. Retain the verified backup and normal monitoring; deploy PR #1369 with a
future ordinary release rather than forcing an otherwise unnecessary production restart.

<!-- /migrated-source: docs/work/2026-08-10-christopherbell-dev-domain-collection-consolidation.md -->

