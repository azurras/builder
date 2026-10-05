# Bootstrap Empty Isolated Website Test Databases

## Document Status
complete

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
- Test-profile infrastructure may be fresh, a contiguous applied migration prefix with at most one migration lease, V015 `RUNNING`, or V015 `APPLIED`; all known domain namespaces must remain empty.

## Open Questions
None. Keep the test bootstrap fail-closed and preserve the existing production path.

## Design
Outside exactly the `test` profile, the schema-readiness gate requires the existing genuine-ledger validation. In `test`, it first validates the configured and connected database, loopback host, and port, then requires every known legacy/target domain namespace to be empty and only approved schema collections to exist, even when a genuine ledger exists. It accepts an empty migration/lease state before migration, a contiguous applied migration prefix during preflight, V015 `RUNNING` with the runner lease, and the durable V015 `APPLIED` marker on later startup with zero or one released migration lease. Migration IDs remain sequential three-digit versions. The V015 application migration records its normal applied state without writing a `TARGET_ACTIVE` record. Update the spoke guide with explicit steps to start a disposable mongod on an OS-selected port, select the test profile and database, verify readiness, and clean up only the owned process and temp path.

| Alternative | Why not |
|---|---|
| Insert a fake production cutover ledger | It would lie about protected migration, backup, and evidence state. |
| Skip V015 or all migrations in tests | Tests would not exercise migration ordering and could hide unsafe state. |
| Depend on a restored production backup | The current verified backup has no target cutover ledger; local agents also should not need a production data copy. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java` | Keep genuine-ledger validation for non-test profiles and add the tightly scoped empty-test bootstrap. |
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionStartupPreflight.java`, `V015RequireDomainCollectionSchema.java` | Use the accurately named schema-readiness operation at both startup gates. |
| `website/src/test/java/dev/christopherbell/configuration/mongo/migration/` | Cover fresh preflight, V015 `RUNNING` and `APPLIED` states, genuine-ledger pass-through on empty domains, and fail-closed conditions. |
| `AGENTS.md`, `README.md`, `docs/operations/mongodb-migrations.md` | Document the isolated test database startup, candidate configuration, readiness check, and cleanup. |

## Task Breakdown

### Task 1 - Add the isolated empty test-database bootstrap
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java`, the startup preflight, V015, and matching migration tests. |
| **Symbols** | `DomainCollectionCutoverLedger`, `requireTargetSchemaReady`, test migration-state validation, the startup preflight, and V015. |
| **Inspection** | Current aggregate candidate `dc928832`; read the migration runner/preflight, cutover ledger validator, manifest sources, configuration profiles, and existing ledger tests. |
| **Behavior** | Preserve genuine `TARGET_ACTIVE` verification; permit only an explicit empty test database to complete V015 without creating a cutover ledger. |
| **Invariants** | The fallback requires exactly profile `test`, database name `test`, one loopback host, an explicit port other than 27017, and empty known domain namespaces. It allows only fresh preflight state, a contiguous applied migration prefix, V015 `RUNNING`, or V015 `APPLIED`, with zero or one named migration lease; IDs use a contiguous zero-padded three-digit sequence. Any cutover-shaped record that is not a genuine active ledger, unknown migration row, unrelated lease, legacy or target domain document, or unapproved collection fails closed. |
| **Boundary/API** | Preserve the `DomainCollectionCutoverLedger` injection type and the V015 ID, checksum, ordering, and production behavior. |
| **Effects and failures** | The test path performs read-only preflight; V015's existing migration record is the only bootstrap state it writes under the migration lease. No cutover ledger is fabricated. |
| **Tests and evidence** | Add focused tests for empty preflight, V015 `RUNNING` and `APPLIED`, real-ledger pass-through with empty domains, wrong profile/database/port, populated namespaces even with a ledger, unknown collections, and malformed ledger. |
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

Regression cases: malformed cutover records never fall back to empty initialization; any domain data or unknown collection blocks startup even with a genuine ledger; fresh preflight and later V015 `APPLIED` startup both pass; database `test` on production port 27017 is rejected; combined `prod,test` profiles require the genuine ledger.

## Rollback or Recovery
Revert only the test-profile implementation and guide changes on this feature branch. The production ledger class, migration IDs, production database, and production services remain unchanged. Verification owns only its unique temp root and process identity; terminate the candidate first, then mongod, verify the listener is gone, and remove only that resolved temp directory.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Test profile could accidentally relax production cutover | Low | Only the exact active profile set `test` uses the fallback; every other profile set retains the genuine ledger requirement. |
| A populated test DB could be mistaken for a fresh database | Medium | Allow only contiguous valid migration records, at most one named migration lease, and known empty manifest namespaces; test fresh preflight, V015 in progress, later startup, and populated-state rejection. |
| Verification could reach the existing MongoDB service | Low | Require database `test`, loopback, and non-27017 port; runtime instructions allocate a free OS port and confirm listener ownership. |

## Implementation Log

### 2026-10-05 - Constrain the test bootstrap to the migration runner state

- **Change:** The test bootstrap now validates the exact active `test` profile, the effective Mongo database name, loopback host and non-production port, migration records V001-V014 plus the current V015 `RUNNING` record, the migration lease, and empty approved domain namespaces.
- **Reason:** V015 is invoked only after its migration lease and normal durable `RUNNING` record exist; the bootstrap must recognize that runner-owned state without accepting a forged cutover row or other application data.
- **Impact:** Task 1 implementation is in progress; test coverage and runtime documentation remain to be completed.

### 2026-10-05 - Name and order the schema readiness gate

- **Change:** The startup gate is named `requireTargetSchemaReady` at both callers and checks safe test connection identity before accepting either a genuine ledger or the empty-database fallback.
- **Reason:** The operation can succeed through two explicitly different valid states, and even a genuine ledger must not let the `test` profile reach an unsafe database.
- **Impact:** Task 1 files, symbols, design, and connection invariants now match the implementation; acceptance criteria are unchanged.

### 2026-10-05 - Cover test-profile preflight and repeat startup

- **Change:** The preflight contract now covers an untouched database before migrations, V015 while `RUNNING`, and later startups after V015 is `APPLIED`; a genuine ledger also requires empty domains under the `test` profile.
- **Reason:** The preflight caller runs before lease acquisition, and the durable migration record is the test-only marker used on later launches.
- **Impact:** Task 1 design, invariants, tests, and regression cases updated; production acceptance remains unchanged.

### 2026-10-05 - Validate each test migration lifecycle state

- **Change:** The test bootstrap now accepts fresh preflight, a contiguous applied migration prefix, V015 `RUNNING`, and V015 `APPLIED` on repeat startup; it limits the migration lease to zero or one and rejects domain data even alongside a genuine ledger.
- **Reason:** The same readiness gate runs before lease acquisition, at V015, and on later managed-profile startups; each phase has a distinct valid infrastructure state.
- **Impact:** Task 1 invariants, implementation details, tests, risks, and recovery notes updated. Migration IDs are checked as a contiguous three-digit sequence and documented for future additions.

### 2026-10-05 - Complete native repository checks and review

- **Change:** Re-ran the focused migration tests and the full `:website:check :cbell-lib:check :website:bootJar` verification against the final lifecycle implementation; reviewed the production code, regression tests, callers, and runtime instructions together.
- **Reason:** The committed candidate must establish both the constrained bootstrap contract and the repository's broader checks before local application verification.
- **Impact:** Focused migration tests passed (18 tests); the full Gradle check completed successfully in 4m17s, including PowerShell groups and the Java suite. Local committed-candidate runtime proof and its Builder report remain pending.

### 2026-10-05 - Document the Windows JDK loopback prerequisite

- **Change:** The first committed-JAR launch reached application bean creation but Java 25 failed to create its internal loopback socket under the default temporary directory. Added a generated short socket-temp directory and `JAVA_TOOL_OPTIONS` setup/cleanup to the candidate instructions.
- **Reason:** This environment-specific JDK prerequisite is independent of Mongo isolation and must be explicit so a future agent can reach application readiness consistently.
- **Impact:** Runtime verification did not pass on candidate `13999417`; the candidate exited before readiness with `Unable to establish loopback connection`. This documentation-only follow-up will be committed and the new candidate rerun against a fresh database.

### 2026-10-05 - Match the real migration persistence envelopes

- **Change:** Runtime execution showed migration IDs are stored in the envelope `_id`, while the live migration lease is stored as the sole `application_lease` document in `application_runtime`. Updated the test guard, persisted-record fixtures, lease validation, and runbook to match those established shapes.
- **Reason:** The first JDK-corrected launch reached Mongo and ran V015, but the guard rejected the real runner-owned state because its tests modeled payload IDs and the legacy `application_leases` source collection.
- **Impact:** Candidate `9bde26f1` did not become ready; its application exited during V015 and wrote the normal `FAILED` migration state in its disposable database. The owned mongod process was stopped. This database is discarded; the fix will be tested on a new one.

### 2026-10-05 - Verify the corrected committed candidate

- **Change:** Re-ran all checks on the corrected implementation and launched the committed JAR against a newly created loopback MongoDB instance. The final gate reads migration IDs from the envelope, permits only the runner's lease record in `application_runtime`, and requires an owned lease while V015 is `RUNNING`.
- **Reason:** The prior runtime attempt exposed persistence details that the initial unit fixtures did not model; the final evidence must exercise the real MongoDB representation and the JDK 25 Windows loopback setup documented for future agents.
- **Impact:** Candidate `dd206c0e` passed 19 focused tests and the full `:website:check :cbell-lib:check :website:bootJar` check (4m11s). A fresh database applied migrations 001–015; readiness and the home page both returned 200; all source and target domain namespaces remained empty and no cutover ledger was written. The candidate and Mongo listeners were stopped and both ports closed. Builder runtime report: [2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md](../test-reports/2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md). Recursive cleanup of the generated scratch directories was rejected by command safety review; the processes are gone and the leftover temporary files are recorded in the report. PR publication and merge remain pending.

### 2026-10-05 - Merge and close the isolated test bootstrap

- **Change:** PR [#1480](https://github.com/azurras/christopherbell.dev/pull/1480) merged the verified candidate `dd206c0ef2498e0d400eccce519990e8050bd021` into `main` as `a9d20589363ed0ed139ef3c709877cca98d2d602`. Windows build, all three Analyze jobs, CodeQL, and Dependency Review passed.
- **Reason:** The local runtime proof, final code review, and CI confirmed that the bootstrap contract and the future-agent setup instructions work together on the committed candidate.
- **Impact:** AC-1 is met by the fresh isolated database applying migrations 001–015 with no synthetic ledger; AC-2 is covered by the fail-closed migration tests and unchanged non-test genuine-ledger gate; AC-3 is met by the documented repeatable setup, full native checks, and local readiness/home-page 200 responses. See the [runtime report](../test-reports/2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md). No production deployment was requested or performed. The temporary MongoDB and application processes and ports are closed; generated scratch directories remain because their recursive cleanup was rejected by command safety review.

## Outcome
| Criterion | Result | Evidence |
|---|---|---|
| AC-1 | Complete | Fresh isolated MongoDB `test` applied migrations 001–015; readiness and `/` returned 200; no `TARGET_ACTIVE` ledger was written. [Runtime report](../test-reports/2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md). |
| AC-2 | Complete | Focused fail-closed tests passed; non-test profiles retain genuine `TARGET_ACTIVE` validation. Full checks passed on candidate `dd206c0e`. |
| AC-3 | Complete | Setup is documented in spoke `AGENTS.md`, `README.md`, and migration runbook; runtime report records full checks and successful local HTTP proof. PR [#1480](https://github.com/azurras/christopherbell.dev/pull/1480) merged as `a9d20589363ed0ed139ef3c709877cca98d2d602`; all CI checks passed. |

No production deployment was authorized or performed. Runtime processes and listeners were stopped; generated scratch directories remain because command safety review rejected recursive removal.

## Project
christopherbell-dev

## Plan Format
task-contract-v2

