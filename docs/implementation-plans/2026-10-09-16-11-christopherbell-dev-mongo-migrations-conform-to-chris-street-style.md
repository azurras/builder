# Mongo Migrations Conform to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The `configuration.mongo.migration` package conforms to write-chris-street-style-code, and the migration runner, its durable records, the domain cutover ledger and every migration's effect are unchanged.

## Background
This is slice 18f of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 18e](2026-10-09-16-01-christopherbell-dev-mongo-runtime-configuration-conforms-to-chris-street-style.md).

Migrations have already run in production. The runner refuses to start if a migration's checksum differs from its durable record. Each checksum is a string constant, not a hash of the code, so code-only edits keep the records valid as long as each migration's effect on a fresh database is unchanged. Inspection of the 24 files at `e72f8114` found:

1. **`MongoMigrationRunner`:** it checks a stored record with `isPresent()` then `orElseThrow()` inside one long method, and a catch named `ignored` handles a failed failure record.
2. **`V011HardenWhatsForLunchData`:** it dates timestamp-less sessions with `Instant.now()` instead of the application `Clock`.
3. **`V012RetainSharedFolderWork`:** it has five one-line `if` statements, a fully qualified `Consumer`, and one-line overrides.
4. **`DomainCollectionCutoverLedger`:** `exactSources` returns null for an invalid source list.
5. **Mechanical issues in 18 files:** fully qualified names (ledger, release metadata, V009, V011, V012); blank-line splits in imports (preflight, state store, V003 to V008, V010, V015); and one-line overrides (V013, V014).
6. **Conforming:** `ApplicationMigration`, `MigrationProperties`, `MigrationRecord`, `MigrationStatus`, `V001` and `V002`.

## Goals
- Every migration file has a recorded verdict and conforms (AC-1, AC-2).
- Startup migrations and the cutover preflight behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing any checksum, id, description or migration effect | Durable records in production depend on them |
| Removing applied migrations | They document and guard the schema history |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every migration file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker; no checksum constant changes |
| AC-3 | On isolated MongoDB `test`, the published test report records that a fresh database starts to readiness (the runner throws on any failed migration or preflight, so readiness proves every migration applied) and the log has no errors |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit, which proves production's durable records still match |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `e72f8114`:
  - All 24 `configuration/mongo/migration` files.
  - `MongoMigrationRunnerTest`, which uses literal checksums.
  - The migration tests for V008, V011, V012 and V014, the cutover ledger and the startup preflight.

## Branch
`claude/style-mongo-migration-20261009` from spoke `origin/main` `e72f8114`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.

## Open Questions
None.

## Design
- **Runner:** `state.find(id).ifPresentOrElse(requireApplied, apply)`. `requireApplied` throws on a checksum mismatch or an incomplete record, and `apply` runs and records the migration as before.
- **V011:** it takes the application `Clock` and dates timestamp-less sessions with `clock.instant()`.
- **Ledger:** `exactSources` returns `Optional<List<String>>`. The completion check reads `exactMetrics(...) && exactSources(...).filter(countsMatch).isPresent()`. Both checks are pure, so the order change is safe.
- **V012:** block `if`s and a documented nullable `instant` reader.
- **Mechanical:** imports and override layout.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/MongoMigrationRunner.java` | changed | `ifPresentOrElse`, named steps, catch name |
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V011HardenWhatsForLunchData.java` | changed | Injected `Clock`; imports |
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V012RetainSharedFolderWork.java` | changed | Block `if`s, imports, override layout |
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java` | changed | `Optional` sources; `countsMatch`; imports |
| `DomainCollectionReleaseMetadata`, `V009MoveSocialRelationshipsToEdges` | changed | Imported names |
| `DomainCollectionStartupPreflight`, `MigrationStateStore`, `V003` to `V008`, `V010`, `V013`, `V014`, `V015` | changed | Import and override layout |
| `ApplicationMigration`, `MigrationProperties`, `MigrationRecord`, `MigrationStatus`, `V001EnsureMigrationInfrastructure`, `V002EnsureRestaurantImportPreviewIndexes` | conforming | No change |
| `website/src/test/java/dev/christopherbell/configuration/mongo/migration/V011HardenWhatsForLunchDataTest.java` | changed | Construct with a `Clock` |
| `DomainCollectionCutoverLedgerTest`, `DomainCollectionStartupPreflightTest`, `MigrationStateStoreTest`, `V008RemoveAccountApprovalFieldsTest`, `V014ConsolidateMusicRuntimeStateMongoTest`, `V014ConsolidateMusicRuntimeStateTest` | changed | Imported names |

## Task Breakdown

### Task 1 - Conform the mongo migrations

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `MongoMigrationRunner.applyIfPending`, `requireApplied`, `apply`; `V011HardenWhatsForLunchData`; `DomainCollectionCutoverLedger.exactSources`, `countsMatch` |
| **Inspection** | All files in Inputs at `e72f8114` |
| **Behavior** | Same migration order, records, effects and preflight decisions |
| **Invariants** | Checksums, ids and descriptions byte-identical |
| **Boundary/API** | V011 gains a `Clock` constructor; Spring supplies the application clock |
| **Effects and failures** | None new |
| **Tests and evidence** | Mongo and migration suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar`, plus a diff showing no `CHECKSUM` line changed |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; checksum diff check | Covered by AC-3 |
| AC-3 | Runner, ledger, preflight and migration tests | verify-local-app: start on a fresh database and read readiness and the log. The already-applied path on restart needs the same database twice, which the candidate script does not support; `MongoMigrationRunnerTest` covers it, and production's own restart on deploy proves it against real records |
| AC-4 | Required PR checks | `wait_for_github.py live`; production starting proves its records still match |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. Durable records are untouched, so either version starts.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Production refuses to start on a checksum mismatch | Very low | No checksum constant changes, which the diff check proves; checksums are not derived from code |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 18e was in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1521 (`96903df`) and auto-deployed. Production serves `5b7ef3c`, which contains it, and `/robots.txt` returns 200. Later merges landed before the deploy finished, so production went straight to the newer head. Production restarted on its existing durable migration records, which proves their checksums still match.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every migration file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-16-19-christopherbell-dev-mongo-migrations-conform-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 4 of 4 runtime cases passed on candidate `6b0da31`; a fresh database applied every migration ([report](../test-reports/2026-10-09-16-19-christopherbell-dev-mongo-migrations-conform-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1521](https://github.com/azurras/christopherbell.dev/pull/1521) merged as `96903df` after all checks passed; production `/actuator/info` reports `5b7ef3c`, which contains it |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
