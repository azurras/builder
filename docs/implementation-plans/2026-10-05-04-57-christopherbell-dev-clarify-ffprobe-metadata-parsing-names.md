# Clarify FFprobe metadata parsing names

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Make FFprobe process outcomes and metadata parsing stages explicit in local names without changing accepted media metadata or failure behavior.

## Background
`FfprobeMusicProbe` validates process status and then maps untrusted JSON strings into typed metadata. Some intermediate names are generic (`result`, `value`) or compress representation changes into expressions, while nearby code already distinguishes `rawDuration` and cleaned metadata. This targeted naming pass will make input roles and parsed values clear at the FFprobe boundary.

## Goals
- Name the process outcome, tag identifier, and raw metadata strings by their role (AC-1).
- Introduce clear intermediate names when extracting a track/disc number or year prefix before parsing (AC-1).
- Preserve exact metadata output, bounds, and error outcomes through baseline/candidate tests and full checks (AC-2).
- Attempt the committed local application with isolated test resources, or record the blocker and cleanup (AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing FFprobe arguments, parsing rules, output size limits, or duration/tag bounds | Only names and intermediate readability change. |
| Changing the FFprobe parser exception policy | That separate correction has its own plan. |
| Creating or updating PR #1477 | The user explicitly excluded that draft. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The probe result, tag text, split numeric text, parsed integer, raw date prefix, and parsed seconds have names that state their roles. |
| AC-2 | Existing `FfprobeMusicProbeTest` passes before and after the change and the committed candidate passes the full native gate. |
| AC-3 | The committed app is verified locally against isolated test resources, or startup blocker and cleanup are recorded and no PR is created. |

## Inputs
- **Request:** User requested a full Chris Street Style code audit with a separate plan/report for each change; PR #1477 is excluded.
- **Reviewed source:** `website/src/main/java/dev/christopherbell/music/catalog/FfprobeMusicProbe.java` and `website/src/test/java/dev/christopherbell/music/catalog/FfprobeMusicProbeTest.java` at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Related plan:** The FFprobe malformed-input cause correction is recorded in the master audit; this change is limited to local name/representation clarity.

## Branch
`codex/clarify-ffprobe-metadata-names-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- Current tests characterize representative valid tags, slash-form track/disc values, fallback behavior, malformed JSON, and missing audio.
- The naming change preserves all existing edge behavior, including current exception types.
- MongoDB port 27018 may remain unavailable; no startup will occur without verified isolated test data.

## Open Questions
None.

## Design
Use `probeResult` for the `MusicProcessResult`, `tagName` for the queried metadata key, `rawTagValue` for the retrieved untrusted text, `rawDuration` and `parsedDurationSeconds` for the duration conversion, and `rawNumberTag`, `leadingNumberText`, and `parsedNumber` for slash-form number parsing. In `year`, name the raw four-character prefix before passing it to the shared bounded number parser. Keep operations and conditions unchanged.

| Alternative | Why not |
|---|---|
| Extract new parsing helper abstractions | The current methods are already small; descriptive intermediates are enough. |
| Add tests that assert identifiers | Existing output/failure tests are the right evidence for a behavior-preserving rename. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/music/catalog/FfprobeMusicProbe.java` | Clarify process result and raw-to-parsed metadata names. |

## Task Breakdown
### Task 1 - Name FFprobe parsing stages
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/java/dev/christopherbell/music/catalog/FfprobeMusicProbe.java`; `website/src/test/java/dev/christopherbell/music/catalog/FfprobeMusicProbeTest.java`. |
| **Symbols** | `probe`; `duration`; `tag`; `clean`; `number`; `year`. |
| **Inspection** | Read the parser, process result contract, existing test cases, and related FFprobe audit plan at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Behavior** | Same FFprobe command, bounds, mapped metadata and error translation. |
| **Invariants** | Preserve source validation, process termination/truncation/status gates, input/output bounds, and codec/audio checks. |
| **Boundary/API** | No public method or result record changes. |
| **Effects and failures** | No new effects; raw JSON text remains validated before being exposed as typed values. |
| **Tests and evidence** | Capture existing focused characterization before edits; run it after edits, then full native checks and committed local runtime. |
| **Verification** | `:website:test --tests dev.christopherbell.music.catalog.FfprobeMusicProbeTest`; full `:website:check :cbell-lib:check :website:bootJar`; local packaged application with isolated test resources. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Review complete diff and run focused metadata output/failure tests before and after. | Launch committed app and verify readiness/representative existing health flow. |
| AC-2 | Focused Ffprobe suite, then full website/library/browser/PowerShell/package gate. | Run exact committed JAR with isolated MongoDB `test`, disabled background work, and a free loopback port. |
| AC-3 | Confirm packaged artifact derives from committed HEAD. | Verify readiness or record preflight/startup error, DB identity, process cleanup, and free port. |

Regressions and edge cases:
- Slash-delimited track and disc metadata continues to select and bound the first number.
- Date metadata continues to use the first four characters as the year candidate.
- Malformed, missing, and non-audio results retain current rejection behavior.

## Rollback or Recovery
Revert the single naming-only commit if existing tests detect a behavior change. If database isolation cannot be verified or startup is blocked, do not alter database state and do not create a PR.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| An extraction or rename changes slash/date parsing behavior | Low | Keep each expression semantically equivalent and run the existing focused suite before and after. |
| Runtime verification remains blocked by unavailable MongoDB or migration 015 | High based on current audit evidence | Record actual preflight outcome; do not bypass database isolation or migration checks. |

## Implementation Log

### 2026-10-05 - Begin implementation with baseline characterization

- **Change:** Began the published parser-naming correction in an isolated worktree and captured the current focused FFprobe test suite before editing.
- **Reason:** The planned change preserves behavior; characterize the current metadata and rejection contracts first.
- **Impact:** Task 1 is in progress; ACs remain unchanged.

### 2026-10-05 - Record candidate verification and runtime blocker

- **Change:** Candidate `fc33aad` committed the planned FFprobe parsing-name correction; focused characterization and the full native gate passed, while local startup preflight was blocked by refused MongoDB connection on `127.0.0.1:27018`. The candidate-specific report records the evidence.
- **Reason:** The read-only preflight could not establish that the configured database was isolated test data; app startup and PR publication remain gated on runtime proof.
- **Impact:** AC-1 and AC-2 are met; AC-3 is blocked. No PR was created, and PR #1477 remains excluded.

## Outcome

> [!CAUTION]
> The naming correction is committed and its focused and full native checks pass; runtime verification and delivery remain blocked by unavailable isolated MongoDB.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Candidate `fc33aad` clarifies probe result, raw metadata, parsed duration, number, and year-prefix names. |
| AC-2 | ✅ Met | Focused suite passed 2/2 on baseline and candidate; full check/package gate passed (2,164 Java tests, 110 skipped, 0 failures/errors). |
| AC-3 | ⏸️ Blocked | [Candidate test report](../test-reports/2026-10-05-05-04-christopherbell-dev-clarify-ffprobe-metadata-parsing-names.md): database identity preflight refused connection; startup was not attempted and no PR was created. |

Follow-up: resume only when the supported isolated test database can be read and verified; then perform committed runtime verification before considering PR publication.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
