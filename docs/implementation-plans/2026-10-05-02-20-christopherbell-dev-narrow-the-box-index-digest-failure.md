# Narrow the Box Index Digest Failure

## Document Status
ready-for-execution

## Plan Format
task-contract-v2

## Objective
> [!IMPORTANT]
> Preserve the existing causal hash-setup error while translating only the documented missing SHA-256 algorithm failure.

## Background
`OfficialCanesBoxPriceClient.sha256()` calls `MessageDigest.getInstance("SHA-256")`, whose declared setup failure is `NoSuchAlgorithmException`, but catches every `Exception` before wrapping it. This can convert unrelated programming defects into a misleading digest-setup error. Existing client tests cover successful audit metadata and failure description behavior.

## Goals
- Catch only the declared digest algorithm failure and preserve its cause (AC-1).
- Preserve the existing SHA-256 audit metadata and client fallback behavior (AC-2).
- Run focused/full native checks and attempt packaged runtime proof for the committed candidate (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change hash algorithm, stored audit field or wire behavior | The task is limited to the declared failure boundary. |
| Change external-service fallback or network exception handling | Those are separate source outcomes with established behavior and tests. |
| Add dependency injection or a digest provider for an unavailable JDK algorithm | That would add a seam solely for an effectively impossible platform condition. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The digest helper catches only `NoSuchAlgorithmException` and wraps it with the original cause. |
| AC-2 | Existing success tests confirm response hashes and metadata remain present and client failure behavior remains unchanged. |
| AC-3 | Focused client tests, full project checks and packaging pass; the committed candidate receives a local startup attempt and test report before any PR. |

## Inputs
- **Request:** Full Chris Street Style audit with small targeted corrections and a plan/report per correction; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `OfficialCanesBoxPriceClient.sha256()` and its callers in `applyAuditMetadata()` at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Inspected tests:** `OfficialCanesBoxPriceClientTest`; baseline focused suite passed all 17 tests before edits.
- **Guidance:** Root `AGENTS.md`, Canes Box Index package README, and Builder Chris Street Style Java, design/API, and testing references.

## Branch
Create `codex/narrow-box-index-digest-failure-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6` after publishing this plan.

## Assumptions
- JDK SHA-256 is mandatory for supported runtime versions; absence indicates a platform configuration defect and should retain a causal error.
- Existing external data, hashing and fallback semantics are correct and covered by the focused test class.
- Application runtime remains blocked by migration 015 on isolated test database `test`.

## Open Questions
None. Keep the change limited to the digest helper's declared checked exception.

## Design
Catch `NoSuchAlgorithmException` from `MessageDigest.getInstance` and wrap it in the existing `IllegalStateException` with the cause. Leave unrelated runtime failures unchanged. Existing client tests characterize the hash-bearing metadata path; because SHA-256 unavailability cannot be induced safely on the supported JDK, do not add a synthetic test seam for that impossible condition.

| Alternative | Why not |
|---|---|
| Keep catching `Exception` | Runtime defects continue to masquerade as unavailable digest setup. |
| Remove exception translation | Loses the operation-specific diagnostic while not improving the caller's action. |
| Inject a digest factory | Adds a test-only abstraction for an unsupported, effectively impossible JDK state. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/canesboxtracker/OfficialCanesBoxPriceClient.java` | Catch only `NoSuchAlgorithmException` in the SHA-256 helper and preserve cause translation. |

## Task Breakdown
### Task 1 - Narrow the digest setup failure
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the client and its focused test class at base `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Symbols** | `sha256(String)`, `applyAuditMetadata(...)`, and existing client tests for audit metadata and source failures. |
| **Inspection** | The baseline focused client suite passed all 17 tests; `MessageDigest.getInstance` declares `NoSuchAlgorithmException`. |
| **Behavior** | The digest output and success/fallback records remain unchanged; only failure classification narrows. |
| **Invariants** | SHA-256 remains the sole audit digest and the original cause is retained. |
| **Boundary/API** | No public method, stored field, URL or serialized value changes. |
| **Effects and failures** | No new I/O; unsupported digest setup remains an operation-specific `IllegalStateException`, unrelated runtime defects propagate. |
| **Tests and evidence** | Run `OfficialCanesBoxPriceClientTest`, the full website/library gates and package; inspect existing raw-response-hash assertions. |
| **Verification** | Attempt local packaged startup with test profile and isolated database `test`; save the actual runtime result, including any migration prerequisite blocker. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review exact checked exception contract and cause-preserving wrapper. | Start packaged candidate with side effects disabled. |
| AC-2 | Focused `OfficialCanesBoxPriceClientTest` including successful official audit metadata and fallback characterization. | Verify readiness and representative route if startup succeeds. |
| AC-3 | Full `:website:check :cbell-lib:check :website:bootJar`, then `git diff --check`. | Record the candidate startup and route attempt against isolated MongoDB `test`. |

Regression: successful official response continues to include `rawResponseHash`; fallback and expected source failures retain their current representations.

## Rollback or Recovery
Revert the isolated catch narrowing if the cause or existing client outcomes change. Do not bypass the migration guard or modify the database to obtain runtime readiness.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Unsupported SHA-256 provider is not reproducible in tests | Low | Keep the code change limited to the JDK's precise declared exception and verify existing metadata-path tests. |
| Runtime remains blocked before readiness | High | Record actual startup result and do not open a PR before supported runtime proof. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev
