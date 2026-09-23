# christopherbell.dev site bug audit and fixes

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Find and fix reproducible bugs in the current christopherbell.dev site, verify each correction, and complete the authorized delivery and production acceptance workflow.

## Goals
- Surface real defects through the repository's existing checks, focused code-path review, and safe live-site smoke checks.
- Fix as many confirmed defects as can be completed and safely delivered in this workstream.
- Keep production data and user accounts unchanged during discovery and verification.

## Inputs
- User authorizes broad bug discovery, fixes, verification, and necessary delivery actions.
- Live GitHub issue inventory is empty; open PRs #1387 and #1388 are dependency updates.
- Live homepage returned HTTP 200 on 2026-09-23.
- `origin/main` refreshed to `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c`.
- The authoritative checkout has unrelated changes; implementation uses `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`.
- Existing dated Builder records and site delivery procedure govern publication and runtime acceptance.

## Branch
`codex/site-bug-audit-20260923` from refreshed `origin/main` `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c` in the isolated spoke worktree. Preserve the dirty authoritative checkout.

## Non-Goals
- No destructive or mutating production actions during discovery.
- No unrelated feature redesign, dependency-only changes, or opportunistic cleanup.
- Do not claim that an audit exhaustively proves the absence of all defects.

## Assumptions
- Read-only public production smoke checks and supported deployment for verified fixes are authorized.
- Repository tests may require database isolation; establish effective configuration before any database-backed command.
- Only independently reproducible or source-confirmed correctness failures are eligible for fixes.

## Open Questions
- Concrete code targets depend on audit evidence. Add reviewed task contracts and Before-Edit Briefs to this plan before implementation.

## Task Breakdown

### Task 1 - Establish audit evidence and identify confirmed defects
- Dependencies: None.
- Files: `AGENTS.md`, `README.md`, `website/src/main/java/dev/christopherbell/view/README.md`, `website/src/main/java/dev/christopherbell/configuration/README.md`, `website/src/main/resources/static/js/README.md`, current application and test configuration, existing route/controller tests, and public route templates.
- Symbols: Spring profiles/database configuration, page route mappings, public endpoint/security mappings, static resource delivery, native `:website:check` tasks, and test fixtures for those boundaries.
- Inspection: Read current repository guide and root overview; confirmed a clean isolated worktree at the refreshed `origin/main` SHA above and a live homepage HTTP 200. Inspect remaining targets in that worktree before checks.
- Behavior: Establish baseline build/test results and exercise safely observable public routes/assets; distinguish verified bugs from expected authorization, unavailable integrations, and stale documentation.
- Invariants: Do not mutate production; do not connect tests or candidate runtime to production data; preserve unrelated dirty authoritative checkout; do not infer bugs from unconfirmed annotations or HTTP status alone.
- Boundary/API: Discovery uses existing site routes, documented Gradle tasks, and non-mutating HTTP GET requests only.
- Effects and failures: Reads only; redact credentials and personal data from evidence; stop any database-backed verification if test isolation cannot be established.
- Tests and evidence: Inspect effective test/runtime profiles before execution; run the repository-native checks and record exact failures/results; use targeted read-only HTTP checks for route behavior.
- Verification: Confirm current branch/SHA/status; verify database target and enabled side effects; run `:website:check`; check representative public routes and assets; reproduce candidate defects and trace their source before proposing code changes.

## Code Changes
None before Task 1 identifies concrete causes. For each confirmed defect, add a task-specific code-edit contract and Before-Edit Brief here, rerun plan validation/review, and publish the revised plan before changing code.

## Files and Modules
Audit the Spring-rendered site, browser JavaScript modules, APIs/security, and project-native build/test configuration. Narrow implementation files only after evidence identifies a defective behavior.

## Unit Testing
Run existing focused tests for confirmed defects and add regression coverage where the behavior has no adequate test. Run only after verifying test database isolation.

## Local Testing
If application behavior changes, package and run the candidate on an isolated non-production port with verified non-production data configuration. Keep production running and capture exact safe request/response evidence.

## Validation
Review every code diff and run `git diff --check`, relevant native checks, and the repository `:website:check` gate. Required CI must pass before merge. For an application change, complete alternate-port runtime verification and post-deployment production checks.

## Rollback or Recovery
Use the site's documented protected deployment rollback procedure if production acceptance fails. Do not manually stop/replace production processes or alter protected state. Keep the merged revision and prior deployed artifact identity in the runtime report.

## Risks
The codebase spans many user-facing and operational features; one sweep may not exercise every authenticated, scheduled, or external-integration path. Candidate runtime configuration and background effects must be verified before startup.

## Completion Criteria
All confirmed defects selected for this workstream have reviewed fix contracts, appropriate automated evidence, a reviewed PR with required CI passing, supported deployment and exact production acceptance evidence, issue handling when a source issue exists, and dated Builder session records/index validation/publishing. Report any audit findings that remain unfixed with concrete reasons.
