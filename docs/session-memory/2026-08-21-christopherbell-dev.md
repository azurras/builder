# 2026-08-21 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/session-memory/2026-08-21-postgresql-production-cutover-command-merged.md](#source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md)
- [docs/session-memory/2026-08-21-postgresql-shadow-rehearsal-merged.md](#source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md)
- [docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review.md](#source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md)
- [docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review.md](#source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md)
- [docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged.md](#source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md)
- [docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged.md](#source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md)

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md"></a>
## 2026-08-21 | session-memory | 2026-08-21 - PostgreSQL Production Cutover Command Merged

Original source: `docs/session-memory/2026-08-21-postgresql-production-cutover-command-merged.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `363de77bd371483e340d26b2ba56f1b353fa4da50a6588baa7ae7647b65e096b`.

<!-- migrated-source: docs/session-memory/2026-08-21-postgresql-production-cutover-command-merged.md -->
<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--2026-08-21---postgresql-production-cutover-command-merged"></a>
### 2026-08-21 - PostgreSQL Production Cutover Command Merged

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--1250---postgresql-production-cutover-command-merged"></a>
#### 12:50 - PostgreSQL Production Cutover Command Merged

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--request"></a>
##### Request

Continue the approved christopherbell.dev PostgreSQL migration autonomously until the project is finished. Commit and push completed work, merge it after CI, preserve the dirty authoritative checkout, and pause only for genuine new authority.

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--project-context"></a>
##### Project Context

Task 8 and the complete shadow rehearsal were already merged. Task 9 is the production persistence-authority transfer. Implementing and merging its guarded command is safe development work; executing it is materially different because it stops production, freezes the authoritative MongoDB source, finalizes PostgreSQL, publishes a one-way authority marker, stops MongoDB, and rotates the live website. That maintenance window requires separate explicit approval.

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--work-completed"></a>
##### Work Completed

- Created isolated worktree `A:\Projects\christopherbell.dev-worktrees\postgresql-cutover` from `origin/main` `bca4231b`; preserved the authoritative checkout's unrelated `M gradlew.bat` state.
- Added the public `prod.ps1 postgres-cutover -ConfirmPostgreSqlCutover` command and strict durable phase state machine.
- Added protected journal/evidence sidecars, release/database/catalog/target identity checks, explicit maintenance deadline checks, pre-authority Mongo recovery only after authenticated unlock proof, post-intent PostgreSQL-forward recovery, final Mongo and PostgreSQL archive/restore proof, candidate verification, environment/service authority publication, production verification, and 14-day/90-day soak evidence.
- Added the read-only `PostgresqlMigrationSourceSnapshotCli` and no-write live integration contract over all 52 kinds.
- Updated operations runbooks and exact architecture classification. V1-V27 migrations were unchanged.
- Committed the spoke as `88403a8d52dc455af442116dfc6502408976e16f`, pushed `codex/postgresql-cutover`, opened PR #1372, waited through all CI, and squash-merged to `main` as `ea6cead1a4fa14bd4ba3c5de65bb8dda91501d0c`.
- Refreshed `origin/main` explicitly and verified the merged cutover entry point.

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--decisions"></a>
##### Decisions

- The persisted `AUTHORITY_PUBLICATION_STARTED` intent is the conservative one-way boundary. Any uncertainty after that record is resolved forward in PostgreSQL, never by restarting Mongo-backed writers.
- `-WhatIf` performs no preflight, lock, journal, process, database, or service effect; ordinary execution requires the exact confirmation switch.
- Production operators may not call Java `finalize` directly; the Windows wrapper is the sole supported production boundary.
- No new test report was created for Task 9 because the production app was intentionally not started or exercised as part of this implementation-only step. The prior Task 8 candidate report remains the latest runtime-app acceptance artifact; Task 9 runtime evidence will be recorded only during the approved maintenance window.

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--validation"></a>
##### Validation

- State machine 16/16; operations Pester 781 total with 753 passed and 28 expected skips.
- Read-only source snapshot 3/3 against MongoDB `/test` and PostgreSQL 18.4 `/test`, proving source and target shapes unchanged.
- Correct live migration package passed in 2m31s, including V1-V27, all-52 SHADOW/authenticated FINALIZE, failure injection, adapter query verification, and Mongo freeze/reader tests.
- Definitive local gate: BUILD SUCCESSFUL in 6m30s; website 2,268 tests, zero failures/errors, 75 expected skips; cbell-lib 123/123.
- PR CI: all nine checks green, including Windows/Ubuntu/macOS Java 25, jOOQ, Dependency Review, and all CodeQL languages.
- Cleanup: zero owned PostgreSQL schemas/history; Mongo `test` dropped; disposable ports 55434/57313 closed; exact worktree runtime and Gradle directories recycled. Production PIDs/listeners remained 8080/19812, 5432/7808, and 27017/5712.

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--current-state"></a>
##### Current State

- Spoke `origin/main`: `ea6cead1a4fa14bdad963a4d33645b5bb61d88795c`.
- PR #1372: merged.
- Builder work remains `active` because production cutover and the post-cutover soak/retirement remain.
- Production is unchanged and available; no Task 9 production effect has run.

<a id="source-docs-session-memory-2026-08-21-postgresql-production-cutover-command-merged-md--follow-ups"></a>
##### Follow-ups

1. Obtain explicit approval for an up-to-30-minute production maintenance window.
2. Run the merged guarded cutover, capture exact backup/finalization/candidate/listener/runtime evidence, and save a local app test report.
3. Monitor 14 complete days of PostgreSQL production and restore evidence.
4. Only then execute Task 10 Mongo code/service/data retirement and close the project.

<!-- /migrated-source: docs/session-memory/2026-08-21-postgresql-production-cutover-command-merged.md -->

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md"></a>
## 2026-08-21 | session-memory | 2026-08-21 PostgreSQL Shadow Rehearsal Merged

Original source: `docs/session-memory/2026-08-21-postgresql-shadow-rehearsal-merged.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `d93dad8ff145db40df1eab073d765f6310cd8627b40aca6785fe08c5b24c81cc`.

<!-- migrated-source: docs/session-memory/2026-08-21-postgresql-shadow-rehearsal-merged.md -->
<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--2026-08-21-postgresql-shadow-rehearsal-merged"></a>
### 2026-08-21 PostgreSQL Shadow Rehearsal Merged

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--1118---task-8-delivery-and-pr-integration-complete"></a>
#### 11:18 - Task 8 delivery and PR integration complete

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--request"></a>
##### Request

Continue the approved christopherbell.dev PostgreSQL migration autonomously until the project is finished. Preserve the dirty authoritative checkout, keep production untouched during rehearsal, commit and push completed branch work, and stop only for a genuinely new authority requirement.

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--project-context"></a>
##### Project Context

- Builder hub: `C:\Users\Christopher\Developer\builder`, branch `main`.
- Spoke: `azurras/christopherbell.dev`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\postgresql-migration`, branch `codex/postgresql-migration`.
- Authoritative checkout: `A:\Projects\christopherbell.dev`; its unrelated `gradlew.bat` change remained untouched.
- Production remained the website on 8080, MongoDB on 27017, and PostgreSQL 16 on 5432. Task 8 did not mutate those services or production data.

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--work-completed"></a>
##### Work Completed

- Implemented, independently reviewed, and merged Tasks 1 through 8 of the PostgreSQL migration plan.
- Repeated all-52-kind SHADOW and RECONCILE operations against the read-only live Mongo source and a 63,230-document restored production archive.
- Verified the PostgreSQL-only candidate on port 18087 with separated application and bridge roles, 39 exact HTTP checks, scheduler/capacity/query-plan evidence, secret scans, and exact cleanup.
- Opened and merged [PR #1370](https://github.com/azurras/christopherbell.dev/pull/1370). Final branch head `ced5b7cb1f1c9feb3c4e973a09fea7058ffbb497` was squash-merged as `bca4231b4d36bdad963a4d33645b5bb61d88795c`; the trees match exactly.
- Corrected CI so PostgreSQL 18 generates exact-revision jOOQ sources once for the OS matrix and independently for Java CodeQL. Generated sources remain uncommitted.
- Set the website Gradle test worker to its proven 2 GiB heap after all three CI runners exhausted the default 512 MiB worker.
- Corrected the POSIX authority-test helper to protect files as `0600` and directories as `0700`; the prior helper removed owner directory traversal and caused `AccessDeniedException` on macOS/Linux.
- Added the merged spoke update and final review, and refreshed the active work record.

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--decisions"></a>
##### Decisions

- Used a squash merge to match the repository's existing PR history convention.
- Kept Task 8 strictly non-authoritative: no FINALIZE command, production listener rotation, service dependency mutation, or authority marker.
- Treated CI failures as product evidence: fixed exact missing jOOQ generation, heap capacity, and POSIX test portability rather than bypassing or skipping checks.
- Kept the overall Builder work `active`; Task 8 is complete, while Tasks 9 and 10 remain.

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--validation"></a>
##### Validation

- Definitive local gate: 2,386 Java tests, 2,311 passed, 75 expected skips, zero failures/errors.
- Candidate matrix: 39/39 exact expected statuses and 39/39 below 2,000 ms; maximum 75.298 ms.
- Live and archive migration evidence: all 52 kinds reconciled repeatedly; archive contained 63,230 documents.
- Final PR checks all passed: jOOQ code generation, macOS, Ubuntu, Windows, Java/JavaScript/Actions CodeQL, and dependency review.
- Merge readback: PR state `MERGED`, merge commit `bca4231b`, final branch/main tree equivalence true.
- Disposable candidates, databases, roles, PIDs, listeners, secrets, and scratch paths were cleaned; production remained unchanged.

<a id="source-docs-session-memory-2026-08-21-postgresql-shadow-rehearsal-merged-md--current-state-and-follow-ups"></a>
##### Current State and Follow-ups

- Task 8 is complete and on `origin/main`.
- Task 9 is a production authority cutover. It requires an explicitly approved maintenance window before stopping writers, taking the final backup, running FINALIZE, publishing the one-way authority marker, or rotating the live listener.
- After Task 9, retain Mongo stopped and frozen while collecting 14 full days of PostgreSQL soak and restore evidence. Task 10 then removes Mongo runtime code/service/data under its retention gates and closes the initiative.

<!-- /migrated-source: docs/session-memory/2026-08-21-postgresql-shadow-rehearsal-merged.md -->

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md"></a>
## 2026-08-21 | spoke-reviews | christopherbell.dev PostgreSQL Production Cutover Command Final Review

Original source: `docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4752a62a400eb3a15649f01e11eb8b8b012d79c0e185c2672d236e1a9e515a50`.

<!-- migrated-source: docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review.md -->
<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md--christopherbelldev-postgresql-production-cutover-command-final-review"></a>
### christopherbell.dev PostgreSQL Production Cutover Command Final Review

- Status: `approved`
- Work record: [PostgreSQL Migration](2026-08-13-christopherbell-dev.md#source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md)
- Spoke update: [PostgreSQL Production Cutover Command Merged](#source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md)
- Repository: `azurras/christopherbell.dev`
- Branch: `codex/postgresql-cutover`
- Reviewed commit: `88403a8d52dc455af442116dfc6502408976e16f`
- Pull request: [#1372](https://github.com/azurras/christopherbell.dev/pull/1372)
- Merge commit: `ea6cead1a4fa14bd4ba3c5de65bb8dda91501d0c`

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md--findings"></a>
#### Findings

No Blocker or Warning remains in the reviewed Task 9 implementation scope.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md--scope-reviewed"></a>
#### Scope Reviewed

The review covered the public production command boundary, explicit confirmation and `WhatIf`, strict durable journal and phase transition validation, release/database/catalog/target identity binding, secret handling, final Mongo and PostgreSQL backup/restore evidence, signed source snapshot and Java finalization handoff, pre-authority rollback, post-intent forward-only recovery, candidate verification, environment authority switch, service/listener activation, soak evidence, read-only source snapshot CLI, architecture classification, runbooks, and tests.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md--evidence"></a>
#### Evidence

- The final cached diff was clean and limited to 11 intended files; no migrations changed.
- Secret scans found only environment-key references and deliberate test sentinels. The bridge secret is passed through the child environment and is absent from command arguments and errors.
- The definitive local gate passed website 2,268 tests and cbell-lib 123 tests with zero failures/errors.
- All nine GitHub checks passed: jOOQ, Dependency Review, Actions/Java/JavaScript CodeQL, and Java 25 builds on Windows, Ubuntu, and macOS.
- PR #1372 had no untrusted comments or unresolved review instructions and was squash-merged to `main` as `ea6cead1`.
- Refreshed `origin/main` contains the exact guarded cutover entry point. The authoritative checkout's unrelated `gradlew.bat` edit remains untouched.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md--jane-street-style-compliance"></a>
#### Jane Street Style Compliance

The implementation makes the one-way authority transfer explicit in the interface, keeps secrets out of arguments/output, validates every resumable state and side effect, separates preparation from authority publication, makes rollback direction conservative and deterministic, and supplies focused counterexample tests plus live disposable integration evidence.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review-md--merge-readiness"></a>
#### Merge Readiness

Approved and merged. This approval covers the implementation, not execution of the live maintenance window. Production cutover remains a separate explicit-approval boundary.

<!-- /migrated-source: docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-final-review.md -->

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md"></a>
## 2026-08-21 | spoke-reviews | christopherbell.dev PostgreSQL Shadow Rehearsal Final Review

Original source: `docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `741da3b84a0d519a1be312b1740a5c0813d88225a387faf32d4ebad2e55088d3`.

<!-- migrated-source: docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review.md -->
<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md--christopherbelldev-postgresql-shadow-rehearsal-final-review"></a>
### christopherbell.dev PostgreSQL Shadow Rehearsal Final Review

- Status: `closed`
- Work record: [PostgreSQL Migration](2026-08-13-christopherbell-dev.md#source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md)
- Spoke update: [Shadow Rehearsal Merged](#source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md)
- Test report: [PostgreSQL Shadow Rehearsal](../test-reports/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-test-report.md)
- Pull request: [#1370](https://github.com/azurras/christopherbell.dev/pull/1370)
- Reviewed branch head: `ced5b7cb1f1c9feb3c4e973a09fea7058ffbb497`
- Merge commit: `bca4231b4d36bdad963a4d33645b5bb61d88795c`

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md--findings"></a>
#### Findings

No open Blocker or Warning remains in the Task 8 implementation, rehearsal evidence, CI integration, or merged tree.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md--scope-reviewed"></a>
#### Scope Reviewed

Independent review rounds covered the complete PostgreSQL migration foundation through shadow rehearsal: all 52 typed source-kind transformations and persistence adapters, Flyway migrations, jOOQ generation, transactional publication and reconciliation, crash recovery, opaque paging, authority evidence, Mongo writer freeze, role separation, Windows operations, backup/restore controls, candidate authentication and HTTP behavior, and production-safe cleanup.

The CI follow-up was reviewed against the same boundary and evidence standards. It keeps generated jOOQ sources uncommitted, generates them once from PostgreSQL 18 for the exact workflow revision, supplies the artifact to every OS build, independently generates Java CodeQL inputs, gives the full website suite its proven worker heap, and preserves secure POSIX directory traversal in the authority tests.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md--merge-readiness-and-evidence"></a>
#### Merge Readiness and Evidence

- House-style and testing requirements were applied throughout the implementation and review rounds.
- The definitive local test report records 2,386 Java tests with zero failures/errors, real PostgreSQL and Mongo acceptance, 39 exact candidate HTTP checks, role/capacity/query-plan evidence, secret scans, and exact cleanup.
- Final GitHub checks are all green: macOS, Ubuntu, Windows, jOOQ generation, three CodeQL languages, and dependency review.
- PR #1370 was mergeable and clean, had no untrusted comments or outstanding review request, and merged to `main` as `bca4231b`.
- The final branch and merged `main` trees match exactly.

<a id="source-docs-spoke-reviews-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review-md--residual-risk"></a>
#### Residual Risk

Task 9 is intentionally outside this review. It transfers production write authority and therefore requires an explicitly approved maintenance window plus fresh backup/restore, frozen-source, rollback-readiness, alternate-port, and one-way authority checks. Task 10 then requires 14 full days of PostgreSQL soak evidence before Mongo retirement.

<!-- /migrated-source: docs/spoke-reviews/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-final-review.md -->

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md"></a>
## 2026-08-21 | spoke-updates | christopherbell.dev PostgreSQL Production Cutover Command Merged

Original source: `docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `66a7de1bb0804455bb3ea472bfbaedd32d8e71dab0faa99992c487428ef3167b`.

<!-- migrated-source: docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged.md -->
<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md--christopherbelldev-postgresql-production-cutover-command-merged"></a>
### christopherbell.dev PostgreSQL Production Cutover Command Merged

- Status: `complete`
- Work record: [PostgreSQL Migration](2026-08-13-christopherbell-dev.md#source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md)
- Spoke: `azurras/christopherbell.dev`
- Reporting context: Task 9 guarded cutover implementation and merge

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md--changes"></a>
#### Changes

- Added the sole public `postgres-cutover -ConfirmPostgreSqlCutover` production authority-transfer command.
- Added a strict, tamper-evident phase journal and evidence sidecars spanning writer stop, final Mongo archive and dry restore, signed 52-kind finalization, reconciliation, PostgreSQL backup and dry restore, PostgreSQL-only candidate, one-way authority publication, production activation, verification, and soak entry.
- Added conservative recovery: Mongo is restored only before authority intent and only after authenticated `currentOp` proves it is unlocked; after intent, recovery is PostgreSQL-forward only.
- Added a read-only 52-kind source snapshot CLI that binds the frozen-source digest without database mutation or secret disclosure.
- Documented the maximum 30-minute maintenance window, exact phase chain, 14-day soak, and 90-day final Mongo archive retention.
- V1-V27 migration files remain unchanged.

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md--github"></a>
#### GitHub

- Branch commit: `88403a8d52dc455af442116dfc6502408976e16f`.
- Pull request: [#1372 Add guarded PostgreSQL production cutover](https://github.com/azurras/christopherbell.dev/pull/1372).
- Squash merge on `main`: `ea6cead1a4fa14bd4ba3c5de65bb8dda91501d0c`.

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md--validation"></a>
#### Validation

- Task 9 state machine: 16/16 passed.
- Operations Pester: 781 total, 753 passed, 28 expected skips, zero failures.
- Live disposable source-snapshot contract: 3/3 passed against MongoDB `/test` and PostgreSQL 18.4 `/test`, with database-shape equality before and after.
- Correctly configured live migration package passed, including all-52 SHADOW/authenticated FINALIZE, V1-V27 schema/upgrade, query verification, failure injection, and Mongo freeze/reader tests.
- Definitive local gate: `BUILD SUCCESSFUL` in 6m30s; website 2,268 tests with zero failures/errors and 75 expected skips; cbell-lib 123/123.
- CI: jOOQ generation, Dependency Review, all CodeQL analyses, and Java 25 builds on Windows, Ubuntu, and macOS all green.
- Disposable PostgreSQL/MongoDB data, processes, ports, and private Gradle state were cleaned; production listeners remained unchanged.

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged-md--authority-boundary-and-next-action"></a>
#### Authority Boundary and Next Action

The command is implemented and merged, but it has not been run against production. The up-to-30-minute maintenance window still requires explicit user approval because it stops the production writer, creates final archives, finalizes PostgreSQL, publishes a one-way authority marker, stops MongoDB, and rotates the live website. Task 10 remains gated on 14 complete days of successful PostgreSQL soak evidence.

<!-- /migrated-source: docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-production-cutover-command-merged.md -->

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md"></a>
## 2026-08-21 | spoke-updates | christopherbell.dev PostgreSQL Shadow Rehearsal Merged

Original source: `docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `0fc343ec29167429d852288883a5258969bdb83563b6e76516d2fe4df7670910`.

<!-- migrated-source: docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged.md -->
<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md--christopherbelldev-postgresql-shadow-rehearsal-merged"></a>
### christopherbell.dev PostgreSQL Shadow Rehearsal Merged

- Status: `active`
- Work record: [PostgreSQL Migration](2026-08-13-christopherbell-dev.md#source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md)
- Test report: [PostgreSQL Shadow Rehearsal](../test-reports/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-test-report.md)
- Spoke repository: `azurras/christopherbell.dev`
- Reporting task: Codex `/root`
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\postgresql-migration`
- Authoritative checkout preserved: `A:\Projects\christopherbell.dev`

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md--delivered"></a>
#### Delivered

- Completed Tasks 1 through 8 of the approved PostgreSQL migration plan: PostgreSQL 18/Flyway/jOOQ foundation, typed relational schemas and adapters for all 52 source kinds, guarded migration and reconciliation, native Windows operations, and production-shadow rehearsal.
- Rehearsed repeatable SHADOW and RECONCILE operations against the read-only live Mongo source and a restored 63,230-document production archive.
- Verified a PostgreSQL-only application candidate with separated app and bridge roles, exact HTTP behavior, scheduler behavior, query plans, capacity, latency, security, and cleanup evidence.
- Added CI-owned PostgreSQL 18 jOOQ generation, exact-run generated-source artifacts, independent Java CodeQL code generation, and a 2 GiB website test worker so every supported runner executes the complete suite.
- Corrected the POSIX authority-test helper to retain owner directory traversal while preserving owner-only permissions.

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md--commits-and-pull-request"></a>
#### Commits and Pull Request

- Final branch head: `ced5b7cb1f1c9feb3c4e973a09fea7058ffbb497`.
- Pull request: [#1370 Complete PostgreSQL shadow rehearsal](https://github.com/azurras/christopherbell.dev/pull/1370).
- Squash merge on `main`: `bca4231b4d36bdad963a4d33645b5bb61d88795c`.
- The merged `main` tree is byte-equivalent to the final reviewed branch tree.

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md--validation"></a>
#### Validation

- Definitive local gate: 2,386 Java tests, 2,311 passed, 75 expected skips, zero failures/errors.
- Candidate matrix: 39/39 exact statuses and 39/39 requests below 2,000 ms; maximum 75.298 ms.
- Restored archive: all 52 kinds and 63,230 documents reconciled repeatedly; live-source SHADOW replay and two RECONCILE digests were identical.
- Final PR checks passed: PostgreSQL 18 jOOQ generation; Java, JavaScript, and Actions CodeQL; dependency review; and Java 25 builds on macOS, Ubuntu, and Windows.
- Production remained unchanged; disposable candidates, databases, roles, processes, listeners, secrets, and temporary paths were removed.

<a id="source-docs-spoke-updates-2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged-md--residual-and-next-action"></a>
#### Residual and Next Action

Task 8 is complete. Task 9 is the guarded production authority transfer and remains gated by an explicitly approved maintenance window. Before the authority marker, rollback returns to untouched Mongo; after the marker and any PostgreSQL write, recovery must remain PostgreSQL-forward.

<!-- /migrated-source: docs/spoke-updates/2026-08-21-christopherbell-dev-postgresql-shadow-rehearsal-merged.md -->

