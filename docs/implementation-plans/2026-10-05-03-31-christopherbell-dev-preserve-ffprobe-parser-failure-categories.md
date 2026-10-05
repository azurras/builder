# Preserve FFprobe Parser Failure Categories

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Translate malformed FFprobe JSON into the existing probe error while allowing unexpected runtime defects in the parser path to retain their original category and cause.

## Background
`FfprobeMusicProbe.probe()` rethrows expected `MusicProbeException` domain failures, then catches every other `Exception` and labels it malformed JSON. Jackson 3 exposes parser failures as `tools.jackson.core.JacksonException`; unrelated runtime defects from metadata processing should remain visible. Existing tests verify malformed input rejection but do not distinguish parser failure from an injected programming defect.

## Goals
- Preserve the existing bounded FFprobe command and metadata behavior (AC-1).
- Translate only Jackson parse failures into `MusicProbeException` with the original cause, while rethrowing unrelated runtime defects unchanged (AC-2).
- Run focused and full native checks, package the committed app, and record local startup evidence (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Change FFprobe invocation, output bounds, supported metadata fields, or validation limits | This correction changes only the parsing failure category. |
| Change public API or user-visible error text for malformed JSON | Existing `MusicProbeException` wording and boundary remain stable. |
| Change external media process failure classification | Process execution is already handled before JSON parsing. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Valid bounded audio metadata and existing missing/invalid result behavior remain unchanged. |
| AC-2 | Malformed JSON remains a `MusicProbeException` whose cause is Jackson's parser exception; an injected unrelated `IllegalStateException` from the mapper is the same object observed by the caller. |
| AC-3 | Focused tests, full website/library/browser/PowerShell checks and package pass; the committed candidate receives a local startup attempt and candidate-specific report before any PR. |

## Inputs
- **Request:** Full `christopherbell.dev` Chris Street Style code audit with small targeted corrections and an individual implementation plan and test report per change; draft PR #1477 is excluded.
- **Audit plan:** [Whole-codebase audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md).
- **Inspected code:** `website/src/main/java/dev/christopherbell/music/catalog/FfprobeMusicProbe.java`, `probe`, `objectMapper.readTree`, and the catch at website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.
- **Inspected tests:** `website/src/test/java/dev/christopherbell/music/catalog/FfprobeMusicProbeTest.java`; current malformed result is asserted only as a `MusicProbeException`.
- **Relevant contract:** Jackson 3 failures elsewhere in this repository are caught as `tools.jackson.core.JacksonException`; probe metadata/domain validation intentionally throws `MusicProbeException`.

## Branch
Create `codex/preserve-ffprobe-parser-failure-categories-20261005` from website `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c` after publishing this plan.

## Assumptions
- Jackson 3 reports malformed JSON as `JacksonException`.
- Unrelated runtime defects should not be translated to malformed input.
- Candidate startup remains blocked by migration 015's incomplete durable record in isolated MongoDB `test`.

## Open Questions
None.

## Design
Keep the existing explicit `MusicProbeException` passthrough and catch only `JacksonException` around parsing and metadata extraction. Attach that parser failure as the cause of the same safe malformed-JSON `MusicProbeException`. Add a regression using an `ObjectMapper` that throws a known `IllegalStateException`; assert the identical exception escapes. Strengthen the malformed JSON assertion to verify the wrapper and parser cause.

| Alternative | Why not |
|---|---|
| Catch `RuntimeException` and translate it as malformed JSON | Runtime failures include programming defects and do not prove the response is invalid JSON. |
| Remove the wrapper and expose Jackson's message | The existing probe boundary provides a stable safe domain error and should retain its parser cause. |
| Catch every exception but rethrow by inspecting messages | Message-based classification is fragile and hides the actual parser contract. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/music/catalog/FfprobeMusicProbe.java` | Catch `JacksonException` rather than every `Exception` while retaining domain failure passthrough. |
| `website/src/test/java/dev/christopherbell/music/catalog/FfprobeMusicProbeTest.java` | Assert malformed JSON cause and unchanged propagation of an injected unrelated runtime failure. |

## Task Breakdown
### Task 1 - Preserve parser failure categories
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | Inspected the probe and its test class at base `695a3ed8617f9b4ab07abb7413baf369c58acf6c`. |
| **Symbols** | `FfprobeMusicProbe.probe`, `MusicProbeException`, `ObjectMapper.readTree`, malformed-result assertions. |
| **Inspection** | `catch (Exception)` maps all non-domain parser-path failures to the malformed-JSON category. |
| **Behavior** | Jackson syntax failures remain safe probe failures with causes; unexpected runtime defects propagate unchanged. |
| **Invariants** | Valid metadata, process bounds and existing domain validation remain unchanged. |
| **Boundary/API** | No signature, public metadata, or error-message change. |
| **Effects and failures** | The process runner is invoked before parsing; only parsing-related error translation changes. |
| **Tests and evidence** | Characterize parser cause and injected runtime defect; retain all current probe behavior. |
| **Verification** | Focused test, full website/library/browser/PowerShell gate, bootable JAR, diff review, and committed local startup using isolated test DB. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Existing valid metadata, missing audio, timeout, truncation and process-failure tests. | Start committed JAR on the test profile and exercise readiness when startup succeeds. |
| AC-2 | Malformed JSON retains Jackson cause; injected runtime failure propagates by identity. | Exercise a representative existing route if ready. |
| AC-3 | Run focused probe suite, full project gate and `git diff --check`. | Record startup against isolated MongoDB `test`; do not bypass migration 015. |

## Rollback or Recovery
Revert only the catch narrowing and regression if malformed JSON changes category or known parser cause is lost. Do not change FFprobe validation or application startup migration behavior as a workaround.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Jackson malformed-input exception differs from the expected type | Low | Verify the actual thrown type in the focused test and catch the repository's Jackson 3 base exception. |
| Other expected input failures depend on the broad catch | Low | Existing malformed, process, and metadata tests cover the established domain boundary. |
| Runtime remains blocked before readiness | High | Record exact migration blocker and do not create a PR without runtime acceptance. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
