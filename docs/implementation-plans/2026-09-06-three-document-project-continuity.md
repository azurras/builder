# Three-document Project Continuity

## Plan Format
task-contract-v1

## Document Status
complete

## Objective
Reconfigure Builder around implementation plans, test reports, and append-only project session memory; consolidate existing records without losing history or evidence links.

## Goals
Replace per-request memory and parallel spoke/work/spec/closure records with corresponding project memory documents. Remove active.md and obsolete document folders. Keep implementation plans and test reports independently reviewable. Update tools, instructions, metadata, and tests so old structures are not recreated.

## Inputs
User explicitly authorized consolidation and folder removal. Inspected all artifact categories, filenames, headings, repository registry, existing memory writer, index generator, and validator. Initial projects are Builder, christopherbell.dev, and personal-computer cleanup; independent grouping review resolves exceptions before migration.

## Branch
Builder main at 5f6b02e; preserve unrelated state and publish selected files.

## Non-Goals
No source repository operations, live deployment, deletion of historical substantive content, inferred current production status, or global Codex memory modification.

## Assumptions
Project identity is stable across dates and tasks. Historical source paths and commit provenance are retained in each imported entry. Existing stale states are labeled historical, not presented as current truth.

## Open Questions
None requiring user input; resolve ambiguous record grouping by content inspection before migration.

## Task Breakdown

### Task 1 - Consolidate historical documents with verified traceability
Dependencies: None.
Files: docs/session-memory, docs/specs, docs/spoke-reviews, docs/spoke-tasks, docs/spoke-updates, docs/spokes, docs/work, docs/work-closures, docs/templates, docs/active.md, docs/status-model.md, docs/skill-migration.md, new migration helper under .agents/skills/save-session-memory/scripts.
Symbols: Source inventory, project assignment, source anchors, Markdown target rewriting, coverage verification.
Inspection: Current filenames and headings establish app versus Builder tooling records; registry contains one app repository; personal-computer-cleanup is a separate unexecuted project. Existing links cross artifact folders.
Required skill: write-jane-street-style-code before code changes.
Behavior: Every substantive source record appears once in its project memory with date/type/source provenance; plan/report links target new anchors. Generated dashboards/indexes are retired or regenerated for the three retained folders.
Invariants: Preserve complete bodies except explicit heading/link relocation; verify coverage before deletion; no live state inference. Preserve dates and externally linked evidence.
Boundary/API: Stable project filenames and explicit source anchors replace historical per-request paths. Existing plan/report documents retain their names.
Effects and failures: Stage transformed memory before deleting sources; refuse collisions or unresolved project mapping; verify source hashes/content and local links. Git retains exact originals.
Tests and evidence: Migration fixture with cross-file and fragment links, dates, code fences, duplicate headings and unknown projects; actual source-by-source transformed-content audit.
Verification: Compare inventory and imported markers, inspect project grouping, resolve internal links, ensure no substantive source missing.

### Task 2 - Make project memory the only continuity sink
Dependencies: Task 1 format and mapping established.
Files: .agents/skills/save-session-memory, .agents/skills/coordinate-builder-work, .agents/skills/review-spoke-work, .agents/skills/manage-spoke-repositories, .agents/skills/plan-builder-work, .agents/lib, .agents/tests.
Symbols: Project-keyed append API, CLI arguments, repository inspect/snapshot, coordination and review persistence.
Inspection: Current helpers write dated request files and separate coordination artifacts; registry/snapshot use docs/spokes; shared artifact writer serves obsolete record types.
Required skill: write-jane-street-style-code before code changes.
Behavior: Explicit --project chooses one stable memory file; progress/decisions/reviews/closure append with date and evidence. Repository inspect remains read-only; explicit snapshot appends to the chosen project memory. Plans carry requirements directly.
Invariants: Different dates/titles cannot create separate files for the same project; malformed identity fails before mutation; no silent default to the wrong project. Preserve existing memory bytes when appending.
Boundary/API: Replace obsolete artifact commands and registry storage with project memory; document new invocation arguments and remove dead helpers.
Effects and failures: Append-only local writes; read-only Git inspection uses bounded subprocess calls and surfaces failures. No network/source mutations.
Tests and evidence: Different dates append same file, different projects remain separate, invalid input cannot write, inspection does not write, snapshot captures honest errors.
Verification: Focused tests plus full suite and helper startup checks.

### Task 3 - Align guidance, validation, navigation and publish
Dependencies: Tasks 1-2.
Files: AGENTS.md, README.md, .agents/skills/complete-builder-work, .agents/skills/maintain-builder-hub, current skill metadata, docs/implementation-plans, docs/test-reports, docs/session-memory.
Symbols: Three-folder indexes, project-memory validation, runtime report template reference, delivery checkpoints.
Inspection: Existing maintenance creates active.md and many artifact indexes; validation requires seven templates and per-request memory names.
Required skill: write-jane-street-style-code before code changes.
Behavior: Maintenance generates navigation only for the three document types, without active status inference. Validate project memory names, provenance and links; preserve plan/runtime schema gates. Progress is appended within project memory rather than copied into parallel records.
Invariants: Read-only checks remain read-only; reviewed plan and runtime/continuity evidence and trusted-comment boundary remain. No stale folder regeneration.
Boundary/API: Skill roles remain useful but share the single continuity sink. Retire obsolete template/status guidance after preserving source history.
Effects and failures: Remove only verified migrated sources and obsolete generated navigation. Publish reviewed selected files and append final Builder continuity.
Tests and evidence: Three-folder fixture; migration coverage and links; metadata validation; independent final review.
Verification: Full unittest suite, all skills validate, hub refresh/check, diff review, source-coverage audit, commit/push and clean synchronized main.

## Code Changes
Migration and project-memory helpers, simplified maintenance, repository inspection without registry storage, and removal of dead artifact wrappers.

## Files and Modules
Explicit targets and contracts are listed per task.

## Unit Testing
Test lossless migration transformation and source coverage, stable project append behavior, three-folder maintenance, and retained delivery guards.

## Local Testing
Use temporary-directory and Git CLI scenarios; no application runtime behavior changes, so no runtime test report applies.

## Validation
Semantic review: scoped targets, effects, acceptance criteria and recovery are concrete. Validate this plan before publication; independent content grouping and final review run before migration completion.

## Acceptance Criteria
Only implementation-plans, test-reports and session-memory remain under docs. All historical substantive records are represented in corresponding project memories with usable evidence links. active.md is gone and cannot regenerate. Future progress appends to the stable project document. All tests and migration audits pass.

## Rollback or Recovery
Restore the pre-migration commit from Git if verification fails; do not delete source records until transformed content and mappings are verified. Never force push.

## Risks
Large app history needs source navigation and targeted reading. Mixed historical records require manual mapping. Markdown fragments and relative links must be re-rooted without changing code examples. Archived instructions must not override current AGENTS.md.

## Completion Criteria
Migration verified, obsolete folders removed, tools and skills aligned, implementation and final continuity published.

## Completion Evidence
Implementation published as `9127288`. All 267 source documents were verified against `78f0183`: 36 Builder, 229 christopherbell.dev, and 2 personal-computer cleanup records. Only the three requested document folders remain. All 56 tests, 525 local fragment links, 11 helper startup checks, hub validation, and independent review passed. Eight pre-existing historical-plan schema warnings remain. Tooling-only changes require no application runtime report. Final continuity is appended to [Builder project memory](../session-memory/builder.md).
