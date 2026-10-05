# Name raw migration field values

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Make the untrusted values read from persisted BSON documents explicit in the strict music-state migration parser without changing validation or migration behavior.

## Background
The migration support already names several trust-boundary values precisely (`rawEntries`, `rawEntry`, `rawSource`, `parsedEntries`), but five field readers call the raw `Object` fetched from a BSON document simply `value`. The parser immediately validates each value and binds it to a typed, validated pattern variable. Naming the first stage `rawFieldValue` makes that boundary consistent and clearer.

## Goals
- Name each unvalidated document field explicitly as raw input before type validation (AC-1).
- Preserve exact accepted BSON types, error categories, migration output, and persisted schema (AC-1).
- Establish passing baseline tests, then run focused and full native checks; attempt committed runtime with isolated test resources (AC-2, AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing BSON validation, coercion, migration data, or error behavior | This is a behavior-preserving naming correction only. |
| Renaming contextual parameters or typed pattern variables | Their current names already express their roles. |
| Creating or updating PR #1477 | The user explicitly excluded that draft. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | All five raw field locals in the shared field readers are named `rawFieldValue`; parsing, rejection, and mapped migration output are unchanged. |
| AC-2 | Existing migration characterization tests pass before and after the edit, and the committed candidate passes the focused suite and full native gate. |
| AC-3 | The committed app is verified locally against isolated test resources, or the startup blocker and cleanup are recorded and no PR is created. |

## Inputs
- **Request:** User requested a full Chris Street Style code audit with a separate implementation plan and test report per change; PR #1477 is excluded.
- **Reviewed source:** `website/src/main/java/dev/christopherbell/music/radio/MusicRuntimeStateMigrationSupport.java` and `website/src/test/java/dev/christopherbell/configuration/mongo/migration/V014ConsolidateMusicRuntimeStateTest.java` at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Existing evidence boundary:** `queueState`, `radioState`, and `requireEquivalent` already distinguish raw documents, raw fields, typed values, and parsed results; tests cover accepted documents and malformed value rejection.

## Branch
`codex/name-raw-migration-field-values-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- The five `Object value` locals all represent unvalidated persisted field contents, and `rawFieldValue` accurately describes each role.
- Existing V014 tests fully exercise the field readers relevant to these local names.
- Local MongoDB test endpoint `127.0.0.1:27018` may remain unavailable; no database will be changed directly.

## Open Questions
None.

## Design
Rename the local `Object value` in `requireString`, `requireDocument`, `requireInstant`, `requireIntegral`, and `requireDouble` to `rawFieldValue`. Keep each pattern variable (`string`, `nested`, `date`, `longValue`, `integerValue`, `doubleValue`) as the validated representation. Do not alter conditions, return types, exception construction, or migration ordering.

| Alternative | Why not |
|---|---|
| Use five type-specific names for each raw local | They all have the same semantic role—unvalidated BSON field content—so one consistent name is precise without noise. |
| Add tests that only assert variable names | Existing migration tests prove input/output behavior; identifier-only tests would echo implementation. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/music/radio/MusicRuntimeStateMigrationSupport.java` | Rename five untrusted field locals while retaining the typed validated names. |

## Task Breakdown
### Task 1 - Name unvalidated BSON values
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/java/dev/christopherbell/music/radio/MusicRuntimeStateMigrationSupport.java`; `website/src/test/java/dev/christopherbell/configuration/mongo/migration/V014ConsolidateMusicRuntimeStateTest.java`. |
| **Symbols** | `requireString`; `requireDocument`; `requireInstant`; `requireIntegral`; `requireDouble`. |
| **Inspection** | Read the five field readers, their parsed callers, the V014 migration tests, and project instructions at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Behavior** | Parsed migration state and malformed-input rejection are byte-for-byte/semantically unchanged. |
| **Invariants** | Preserve exact BSON type checks, no coercion, strict field shape, safe migration failures, schema and target documents. |
| **Boundary/API** | Private local identifier changes only; no signatures or persisted fields change. |
| **Effects and failures** | No new effects; each raw value remains checked before being returned as a typed value. |
| **Tests and evidence** | Capture existing focused tests before edits; run them after edits and full native checks; review final complete diff. |
| **Verification** | `:website:test --tests dev.christopherbell.configuration.mongo.migration.V014ConsolidateMusicRuntimeStateTest`; full `:website:check :cbell-lib:check :website:bootJar`; committed local application check. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Compare exact diff; run existing V014 tests that cover valid migration documents, missing/null fields, unsupported types, and versions. | Not observable through a distinct page action; launch the committed app and verify readiness and the existing health flow. |
| AC-2 | Baseline and candidate V014 class, then full website/library/browser/PowerShell/package gate. | Run the exact committed JAR with isolated MongoDB `test` and disabled background work. |
| AC-3 | Confirm the packaged JAR was built from committed HEAD. | Verify readiness or record DB identity/startup error, process cleanup, and free port. |

Regressions and edge cases:
- Existing type checks reject wrong BSON field types without coercion.
- Typed pattern variables continue to carry validated values.

## Rollback or Recovery
Revert the single naming-only commit if focused checks show an accidental expression change. If packaged startup is blocked, stop only the candidate and leave the database untouched.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A rename accidentally alters a type check or return value | Low | Keep each diff to identifier substitution and run existing parser/migration tests. |
| Local packaged startup remains blocked by unavailable MongoDB or migration 015 | High based on current audit evidence | Record actual preflight/runtime state; do not bypass database isolation or migration checks. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
