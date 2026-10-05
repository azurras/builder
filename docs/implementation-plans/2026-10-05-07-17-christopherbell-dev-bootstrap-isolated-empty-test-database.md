# Bootstrap Empty Isolated Website Test Databases

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Let agents run the target-schema website against a fresh, isolated MongoDB `test` database without fabricating the production cutover ledger, while preserving the exact V015 gate for every non-test runtime.

## Background
The repository-wide style audit passed its combined native checks, but local application startup was blocked because the isolated MongoDB endpoint was unavailable and V015 requires a completed cutover ledger. The newest verified backup on this machine also lacks that ledger, so backup restoration cannot initialize this test. User directed that the cause be fixed so future agents can run the application without repeating this blocker.

## Goals
- Allow only the explicit `test` Spring profile on a loopback MongoDB port other than production port 27017 and database `test` to initialize a truly empty domain schema (AC-1).
- Keep production and other profiles bound to the unchanged genuine `TARGET_ACTIVE` ledger check, and reject non-empty or malformed test databases without modifying them (AC-2).
- Document a repeatable isolated MongoDB setup and verify the candidate application's readiness and a representative page using it (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Creating a synthetic `TARGET_ACTIVE` ledger | It would falsely assert a production cutover occurred. |
| Changing the production migration or cutover behavior | Production must continue requiring genuine migration evidence. |
| Restoring or modifying production MongoDB data | Runtime verification must stay on a separate loopback MongoDB process and the exact database `test`. |
| Building a general-purpose deployment orchestrator | The fix is limited to an explicit local test-profile bootstrap and its run instructions. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | A fresh empty database named `test` on a non-production loopback MongoDB port can complete migrations and start in the `test` profile without a synthetic cutover ledger. |
| AC-2 | Production keeps the existing `TARGET_ACTIVE` requirement; the test path rejects wrong profile/database/port, an invalid existing cutover ledger, and any pre-existing application data. |
| AC-3 | Repository instructions give agents a reproducible isolated MongoDB setup, and the committed candidate passes full checks plus local readiness and page-response verification against that database. |

## Inputs
- **Request:** User directed a whole-repository Chris Street Style audit, authorized fixing discovered blockers, rejected reliance on the old draft PR, and asked that future agents not hit this runtime blocker.
- **Repository state:** Isolated worktree `codex/chris-street-style-audit-20261005` at `dc928832d39c1e019483c9aca668e63ba333463d`, based on trusted `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- **Inspected:** `AGENTS.md`, root `README.md`, test and deploy-smoke profiles, `DomainCollectionCutoverLedger`, `DomainCollectionStartupPreflight`, `V015RequireDomainCollectionSchema`, `MongoMigrationRunner`, migration tests, and MongoDB migration/restore runbooks.
- **Observed:** A dedicated mongod on an OS-selected loopback port passed ping and archive dry-run; the current verified archive had no cutover ledger and could not satisfy V015.

## Branch
`codex/chris-street-style-audit-20261005` based on `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.

## Assumptions
- The test profile is for disposable local data and never selects the production writer service.
- Spring exposes the configured Mongo connection through `spring.mongodb.uri` / `SPRING_MONGODB_URI`; the test bootstrap independently checks the selected host, port, and database name before accepting an empty database.
- Existing applied migration records from V001-V014 and the current V015 `RUNNING` record are allowed; the migration lease is the only allowed lease; domain documents and unrelated collections are not.

## Open Questions
None. Keep the test bootstrap fail-closed and preserve the existing production path.

## Design
Use a profile-specific `DomainCollectionCutoverLedger` implementation selected only by `test` and not `prod`. It first accepts a genuine active ledger through the existing validator. If no cutover record exists, it accepts only a pristine database on loopback, database `test`, and a non-production port; it verifies that every known legacy/target domain namespace is empty, only approved schema collections exist, migration rows are limited to prior applied records plus the current V015 `RUNNING` record, and the only lease is the active migration lease. The V015 application migration then records its normal applied migration state without writing a `TARGET_ACTIVE` record. The test database's applied V015 record records the one-time empty-schema initialization. Non-test profiles continue using the existing ledger implementation unchanged. Update the spoke guide with explicit steps to start a disposable mongod on an OS-selected port, select the test profile and database, verify readiness, and clean up only the owned process and temp path.

| Alternative | Why not |
|---|---|
| Insert a fake production cutover ledger | It would lie about protected migration, backup, and evidence state. |
| Skip V015 or all migrations in tests | Tests would not exercise migration ordering and could hide unsafe state. |
| Depend on a restored production backup | The current verified backup has no target cutover ledger; local agents also should not need a production data copy. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java` | Select the genuine-ledger implementation outside `test`. |
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/TestDomainCollectionCutoverLedger.java` | Add a test-only empty-database gate that validates URI/profile/database/port and rejects existing application data. |
| `website/src/test/java/dev/christopherbell/configuration/mongo/migration/` | Cover genuine-ledger pass-through, empty database initialization, and fail-closed conditions. |
| `AGENTS.md`, `README.md`, `docs/operations/mongodb-migrations.md` | Document the isolated test database startup, candidate configuration, readiness check, and cleanup. |

## Task Breakdown

### Task 1 - Add the profile-specific empty database gate
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java`, neighboring migration classes, and matching migration tests. |
| **Symbols** | `DomainCollectionCutoverLedger`, new test-profile `TestDomainCollectionCutoverLedger`, `requireTargetActive`. |
| **Inspection** | Current aggregate candidate `dc928832`; read the migration runner/preflight, cutover ledger validator, manifest sources, configuration profiles, and existing ledger tests. |
| **Behavior** | Preserve genuine `TARGET_ACTIVE` verification; permit only an explicit empty test database to complete V015 without creating a cutover ledger. |
| **Invariants** | Test implementation requires profile `test` without `prod`, database name `test`, loopback URI, and port other than 27017; only known empty domain namespaces and V001-V014 migration records are allowed. Any cutover-shaped record that is not a genuine active ledger, unknown migration row, unrelated lease, legacy or target domain document, or unapproved collection fails closed. |
| **Boundary/API** | Preserve the `DomainCollectionCutoverLedger` injection type and the V015 ID, checksum, ordering, and production behavior. |
| **Effects and failures** | The test path performs read-only preflight; V015's existing migration record is the only bootstrap state it writes under the migration lease. No cutover ledger is fabricated. |
| **Tests and evidence** | Add focused tests for real ledger pass-through, pristine test database, wrong profile/database/port, populated namespaces, unknown collections, and malformed ledger. |
| **Verification** | Run the focused migration test classes, then `:website:check :cbell-lib:check :website:bootJar`. |

### Task 2 - Document isolated candidate runtime verification
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1. |
| **Files** | Root `AGENTS.md`, `README.md`, and `docs/operations/mongodb-migrations.md`. |
| **Symbols** | Local Mongo setup and test-profile verification sections. |
| **Inspection** | Read current test profile, README local setup, migration runbook, and isolated Mongo test harness. |
| **Behavior** | An agent can start a disposable loopback Mongo instance, bind only database `test`, run the committed JAR with profile `test`, verify readiness and `/`, and clean up its own resources. |
| **Invariants** | Never attach a candidate to port 27017 or database `christopherbell`; do not use production data or hand-create migration markers. |
| **Boundary/API** | Keep existing build and runtime commands and use the documented Windows/native tooling. |
| **Effects and failures** | Instructions stop on occupied ports, failed health/readiness, or unsafe database state and require cleanup of only the owned server. |
| **Tests and evidence** | Review commands against the tested application and disposable Mongo behavior; validate links and `git diff --check`. |
| **Verification** | Execute the documented flow on the committed candidate and save the actual runtime report in Builder. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Focused test-profile ledger and migration-runner tests; full website/library checks. | Start a fresh disposable MongoDB on a non-production loopback port, launch the committed JAR with database `test` and profile `test`, and confirm readiness plus `/`. |
| AC-2 | Regression tests assert the production implementation still requires the genuine ledger and the test implementation rejects unsafe state. | Verify only the `test` candidate connects to the owned listener; confirm 27017 remains owned by the existing service and untouched. |
| AC-3 | Documentation/link validation and full native checks. | Follow the committed guide exactly and record commands, response codes, database identity, process ownership, and cleanup. |

Regression cases: malformed cutover records never fall back to empty initialization; any domain data or unknown collection blocks startup; database `test` on production port 27017 is rejected; combined `prod,test` profiles have no test bootstrap bean.

## Rollback or Recovery
Revert only the test-profile implementation and guide changes on this feature branch. The production ledger class, migration IDs, production database, and production services remain unchanged. Verification owns only its unique temp root and process identity; terminate the candidate first, then mongod, verify the listener is gone, and remove only that resolved temp directory.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Test profile could accidentally relax production cutover | Low | Production and test implementations are profile-exclusive; a mixed `prod,test` profile fails closed. |
| A populated test DB could be mistaken for a fresh database | Medium | Allow only migration/lease infrastructure and known empty manifest namespaces before V015; cover unrelated and populated state in tests. |
| Verification could reach the existing MongoDB service | Low | Require database `test`, loopback, and non-27017 port; runtime instructions allocate a free OS port and confirm listener ownership. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
