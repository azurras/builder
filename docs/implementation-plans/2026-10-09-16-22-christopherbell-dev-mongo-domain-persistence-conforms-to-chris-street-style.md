# Mongo Domain Persistence Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The `configuration.mongo.domain` package conforms to write-chris-street-style-code, and every kind-scoped read, write, aggregation, lease and account deletion behaves as before.

## Background
This is slice 18g, the last part of slice 18 in the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 18e](2026-10-09-16-01-christopherbell-dev-mongo-runtime-configuration-conforms-to-chris-street-style.md). Every domain repository depends on these 17 files.

Inspection at `f19a2750` found the package carefully written; its issues are mechanical:

1. **Fully qualified names** in seven files: `DomainAccountDeletionStore`, `DomainCollectionManifest`, `DomainDocumentCodec`, `DomainEnvelopeAggregationValidation`, `DomainMongoOperationsFactory`, `KindScopedRepositorySupport` and `MongoKindScopedOperations`.
2. **One-line accessors** in `MongoDatabaseLeaseMutation`.
3. **Undocumented nullable returns** in `DomainDocumentCodec`: `mappedIdFromSource` returns null when a value has no id, and `version` returns null when a kind has no `@Version` property.
4. **Reviewed and kept:**
   - `buildIndexes` in `DomainCollectionManifest` is a long declarative index list, not logic.
   - `acquireDatabaseLease` returns its `Optional` directly.
   - `KindScopedAggregation` uses `isPresent()` only to choose a sublist.
5. **Conforming:** the other nine files.

## Goals
- Every domain file has a recorded verdict and conforms (AC-1, AC-2).
- Persistence behaves as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the envelope format, field mapping, kind registry, index manifest or aggregation rules | Stored data and query semantics |
| Splitting `buildIndexes` | It is data; splitting it would scatter one manifest |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every domain file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the candidate starts (the domain preflight validates the manifest), accounts, posts, likes, follows and lunch preferences round-trip through the kind-scoped operations, and the log has no errors |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `f19a2750`:
  - All 17 `configuration/mongo/domain` files.
  - `MongoKindScopedOperationsTest`, `MongoKindScopedOperationsMongoTest`, `DomainCollectionManifestTest`, `MongoBackendComponentContextTest`, `SiteMonitorMongoIntegrationTest` and `SurviveWorldMongoCodecTest`.

## Branch
`claude/style-mongo-domain-20261009` from spoke `origin/main` `f19a2750`.

## Assumptions
None.

## Open Questions
None.

## Design
- Fully qualified names become imports.
- Accessors become one statement per line.
- The two nullable codec returns gain Javadoc that states when they are null.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainDocumentCodec.java` | changed | Imported names; documented nullable returns |
| `DomainAccountDeletionStore`, `DomainCollectionManifest`, `DomainEnvelopeAggregationValidation`, `DomainMongoOperationsFactory`, `KindScopedRepositorySupport`, `MongoKindScopedOperations` | changed | Imported names |
| `MongoDatabaseLeaseMutation` | changed | Accessor layout |
| `DomainDocumentKind`, `DomainDocumentKindRegistry`, `DomainMongoFieldMapper`, `KindScopedAggregation`, `KindScopedMongoOperations`, `MalformedDomainDocumentException`, `NamespacedMongoId`, `SanitizedMongoDuplicateKeyCause`, `UnapprovedDomainFieldException` | conforming | No change |
| `website/src/test/java/dev/christopherbell/configuration/mongo/domain/DomainCollectionManifestTest.java`, `MongoBackendComponentContextTest.java`, `MongoKindScopedOperationsMongoTest.java`, `MongoKindScopedOperationsTest.java`, `SiteMonitorMongoIntegrationTest.java`, `SurviveWorldMongoCodecTest.java` | changed | Imported names |

## Task Breakdown

### Task 1 - Conform mongo domain persistence

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `DomainDocumentCodec.mappedIdFromSource`, `version`; `MongoDatabaseLeaseMutation` accessors |
| **Inspection** | All files in Inputs at `f19a2750` |
| **Behavior** | Unchanged; only names, layout and documentation change |
| **Invariants** | Stored envelopes, ids, indexes and queries unchanged |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | Mongo, domain and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Kind-scoped operation tests against a real Mongo | verify-local-app: startup plus the post and lunch flows from slices 16a and 17c |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| None material | Low | The diff is imports, layout and Javadoc |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 18f was in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
