# Lean Builder Skills

## Plan Format
task-contract-v1
## Document Status
ready-for-execution
## Objective
Reduce loaded instructions and unnecessary human input while preserving quality and dated work history.
## Goals
Consolidate eleven skills into eight; centralize shared policy; shorten coding guidance; retain deterministic helpers and evidence gates.
## Inputs
User approved the eight-skill assessment. Inspected AGENTS.md, all skill entrypoints, helper inventory, coding references, publication and discovery tests, and September 8 session memory.
## Branch
Builder main at bf99d89; clean starting checkout.
## Non-Goals
No application changes, production actions, historical memory rewrites, or Superpowers plugin edits.
## Assumptions
Existing delivery authority persists. Review-only tasks remain read-only. One dated memory file per project and work date remains mandatory.
## Open Questions
None requiring user input.
## Task Breakdown
### Task 1 - Consolidate instruction ownership and skill routing
Dependencies: None.
Files: AGENTS.md, README.md, .agents/skills entrypoints and metadata, complete-builder-work/references, write-jane-street-style-code/references, .agents/tests.
Symbols: Delivery routing, review mode, coordination reference, repository inspection helper path, phase-finalization, discovery expectations.
Inspection: Current coordination and review skills mostly repeat delivery/review plus persistence; repository inspection is a tested standalone helper; coding references repeat broad instruction tables and examples.
Required skill: write-jane-street-style-code before code changes.
Behavior: Eight discoverable skills; complete-builder-work owns coordination/repository context; code skill owns independent read-only review. Short entrypoints load only needed references and reuse verified progress without routine approval questions.
Invariants: Retain dated append semantics, all runtime/data isolation and publication gates, trusted-comment policy, exact-file Git safety, error visibility, plan review and evidence quality. No broadening external authority.
Boundary/API: Relocate repository inspection helper under complete-builder-work unchanged; update callers and tests. Remove three obsolete skill folders without wrappers. Keep inspection default read-only and snapshot explicitly requested.
Effects and failures: Local instruction edits and verified file move/deletions; preserve unrelated state. Helpers still reject invalid inputs and surface Git/runtime failures.
Tests and evidence: Passing behavior-preservation baseline; rerun behavioral suite after relocation. Replace brittle duplicated-wording tests with shared-owner/link/discovery checks. Review realistic planning-only, review-only, failed-push, and cross-day continuity scenarios. Measure Markdown words before and after without claiming exact model-token savings.
Verification: unittest suite, all eight skill metadata and local links, helper startup, hub validation, instruction size comparison, targeted review, selected-file publication.
## Code Changes
Relocate one helper, revise discovery tests, remove obsolete skill wrappers, simplify instruction sources.
## Files and Modules
Targets listed in Task 1; shared runtime libraries remain unchanged.
## Unit Testing
Preserve existing public-boundary tests for append dates, snapshots, read-only inspection, validation and Git safety.
## Local Testing
Native Python/Git fixture checks; no application runtime report applies.
## Validation
Plan reviewed: inspected targets, preserved contracts, scope, recovery and observable checks are concrete. No blockers.
## Rollback or Recovery
Restore reviewed files from bf99d89 through a normal corrective commit; never force push.
## Risks
Over-shortening can hide safeguards; preserve operational contracts and review realistic boundary scenarios. Word count is a size proxy, not measured conversation token usage.
## Completion Criteria
Eight skills, materially smaller maintained guidance, passing checks, published implementation and dated session continuity.
