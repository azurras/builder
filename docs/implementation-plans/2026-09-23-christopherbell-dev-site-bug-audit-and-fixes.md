# christopherbell.dev site bug audit and fixes

## Plan Format
task-contract-v1

## Document Status
in-progress

## Objective
Find and fix reproducible bugs in the current christopherbell.dev site, verify each correction, and complete the authorized delivery and production acceptance workflow.

## Goals
- Surface real defects through the repository's existing checks, focused code-path review, and safe live-site smoke checks.
- Fix as many confirmed defects as can be completed and safely delivered in this workstream.
- Keep production data and user accounts unchanged during discovery and local verification.

## Inputs
- User authorizes broad bug discovery, fixes, verification, and necessary delivery actions.
- Live GitHub issue inventory is empty; open PRs #1387 and #1388 are dependency updates.
- Live homepage and all sitemap non-restaurant routes returned HTTP 200 on 2026-09-23.
- Live browser homepage, Void, WFL ranking and Raising Cane's tracker had no console errors; tracker loaded after its API request completed.
- WFL public freshness API reports `lastRefreshedOn=2026-08-02T22:44:50.963Z`, `current=false`, and a 45-day freshness window.
- The production WFL scheduler is configured by default for the 15th at 03:00 America/Chicago; the import startup catch-up compares only the prior month's successful completion month.
- Protected application logs are unreadable to this account; do not change their ACLs. The import's exact production failure cause remains unconfirmed.
- `:website:check` passed on `origin/main` SHA `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c` after setting a per-process short JDK Unix-domain socket temp path. No environment or `.env` overrides were present in the isolated worktree. The full check used mocked/unit boundaries; external PostgreSQL contract tests were skipped because the local test role has no configured password.
- The authoritative checkout has unrelated local changes; implementation uses `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`.

## Branch
`codex/site-bug-audit-20260923` from refreshed `origin/main` `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c` in the isolated spoke worktree. Preserve the dirty authoritative checkout.

## Non-Goals
- No destructive or mutating production actions during discovery or local verification.
- No unrelated feature redesign, dependency-only changes, or opportunistic cleanup.
- Do not claim that an audit exhaustively proves the absence of all defects or that the WFL catch-up gap is the only cause of stale production data.

## Assumptions
- Read-only public production smoke checks and supported deployment for verified fixes are authorized.
- Tests must use isolated PostgreSQL `test` data; no test or candidate may connect to production data.
- Only independently reproducible or source-confirmed correctness failures are eligible for fixes.
- On deployment, the existing startup catch-up mechanism is expected to perform its configured WFL import when its latest scheduled run is overdue.

## Open Questions
- Protected production import status/log details remain unavailable. Report this as a production-cause limitation; do not bypass protected ACLs.

## Task Breakdown

### Task 1 - Establish audit evidence and identify confirmed defects
- Dependencies: None.
- Files: `AGENTS.md`, `README.md`, `website/src/main/java/dev/christopherbell/view/README.md`, `website/src/main/java/dev/christopherbell/configuration/README.md`, `website/src/main/resources/static/js/README.md`, application profiles, public templates/routes, WFL import workflow and tests.
- Symbols: Test/runtime profile and persistence settings, page mappings/security, public freshness route, browser assets, WFL monthly cron and startup catch-up, native `:website:check` tasks.
- Inspection: Clean isolated worktree at refreshed `origin/main` SHA above. Verified PostgreSQL test profile resolves to database `test` and role `christopherbell_test`; no effective password is available. Live public routes and current WFL freshness API were read without mutation. Protected production log access returned ACL denial. Read the WFL import package README and traced `runMissedMonthlyOpenStreetMapImport`.
- Behavior: Establish baseline checks and safely observable public routes; distinguish verified bugs from expected authorization, unavailable integrations and status indicators.
- Invariants: No production writes during audit; no production database connections from tests/candidate; preserve dirty authoritative checkout; do not infer causation from freshness status alone.
- Boundary/API: Existing routes, documented Gradle tasks, and non-mutating HTTP GET requests only.
- Effects and failures: Reads only; redact credentials and personal data; protected logs remain untouched; stop database-backed execution if the target is not isolated.
- Tests and evidence: Verified test profile config; `:website:check` completed successfully on baseline; all sitemap routes excluding 7,340 restaurant-detail URLs returned 200, and one restaurant detail plus `/wfl/top-liked` returned 200. Browser checked homepage, Void and tracker state with no console errors. Live freshness endpoint returned stale status as recorded above.
- Verification: Confirmed monthly schedule and catch-up comparison in source. Startup catch-up fails to retry after the current month's scheduled occurrence when the prior successful completion predates that occurrence; add a deterministic regression test in Task 2. A targeted scan of site `@Scheduled` and `ApplicationReadyEvent` code found no other durable cron-import workflow using a prior-completion-month startup check; no second confirmed instance of this defect surfaced.

### Task 2 - Retry overdue monthly imports on application startup
- Dependencies: Task 1 audit evidence.
- Files: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowService.java`, `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/importing/RestaurantImportWorkflowServiceTest.java`, and `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`.
- Symbols: `runMissedMonthlyOpenStreetMapImport`, the monthly cron/zone properties, import state `lastCompletedOn`, and the `OpenStreetMap Import` scheduling description.
- Inspection: Read production scheduler and durable-state updates, the package README, WFL configuration, and existing workflow unit tests. The service records `lastCompletedOn` for successful imports, but startup catch-up compares only `lastCompletedMonth` to the previous calendar month. The live site freshness confirms data has remained unchanged since 2026-08-02, but protected logs prevent establishing the sole production cause.
- Required skill: `write-jane-street-style-code` before code changes.
- Behavior: After the latest configured monthly cron occurrence is due, startup retries when the latest successful completion predates that occurrence, even if an earlier success exists in the same month. Before the current month's scheduled occurrence, a successful run after the previous occurrence suppresses duplicate catch-up. Keep first-run catch-up behavior.
- Invariants: Preserve scheduled cron/zone behavior, the durable import lease and ownership checks, existing failure recording, deploy-smoke suppression, and admin API contracts. Disabled monthly imports remain disabled. No test/candidate connects to production data.
- Boundary/API: No endpoint or persistence schema changes. Use existing import state and cron configuration only.
- Effects and failures: Startup catch-up may fetch and apply configured OSM data through the existing lease-protected workflow. Preserve current logged failure behavior and never bypass the lease. Unit tests mock remote/import effects.
- Tests and evidence: Add regression cases for startup after an overdue monthly cron and startup before the next due occurrence; verify expected lease/import calls. Run focused `RestaurantImportWorkflowServiceTest`, full `:website:check`, then candidate runtime on an isolated port against a temporary PostgreSQL database named `test` and `deploy-smoke` profile so no scheduled external jobs run during smoke verification.
- Verification: The failing test reproduced the missed catch-up before implementation and the focused test passes after the fix. The full native `:website:check` passed, `git diff --check` was clean, and the packaged candidate passed readiness, homepage, ranking, and freshness requests against the disposable `test` database. PR #1398 was merged as `f1db692c7b5dff1de7ce4490c07908935ee8f8b0`; CodeQL, dependency review, and Java, JavaScript, macOS, Ubuntu, and Windows checks passed. The production release is not yet verified: on 2026-09-23 at 22:20, 22:23, and 22:24 UTC, the website service remained Running on PID 14424 and public WFL freshness remained `2026-08-02T22:44:50.963Z`. The unprivileged shell could not read protected deployment state or start the SYSTEM task, and the platform rejected a `RunAs` dry-run launch. Do not weaken ACLs or bypass the supported deployment path; resume with an authorized elevated deployment session, then verify release SHA, readiness, routes, and WFL import freshness.

## Code Changes
Task 2 is limited to startup catch-up selection, direct unit tests and the owning feature README's scheduling contract. Reinspect all targets before edits.

## Files and Modules
Spring service for WFL restaurant imports, its unit tests, and the owning restaurant feature README.

## Unit Testing
Run the focused import workflow test and existing JavaScript, Java and Windows production checks through `:website:check`. Do not run database-backed tests without verified database `test` isolation and credentials.

## Local Testing
Start the packaged candidate on an alternate port using an ephemeral isolated PostgreSQL cluster/database named `test`, with the `deploy-smoke` profile disabling external scheduled effects. Never touch production listeners or data.

## Validation
Review the source/test/documentation diff; run `git diff --check`, the focused test, and `:website:check`. Required PR CI must pass. Complete alternate-port runtime proof and post-deployment production checks through the supported deployment procedure.

## Rollback or Recovery
Use the site's documented protected deployment rollback procedure if production acceptance fails. Do not manually stop/replace production processes or alter protected state. Record the merged revision and prior deployed artifact identity.

## Risks
The stale freshness marker confirms data age, not why scheduled imports stopped succeeding. Startup retry addresses overdue successful-completion state; a persistent upstream, database, or environment failure can still leave data stale. Isolated runtime infrastructure must not share production databases or writers.

## Completion Criteria
The new regression test failed on baseline and passes after the fix; native checks and alternate-port runtime proof pass; PR #1398 merged after required CI passed. Remaining: supported production deployment and exact production acceptance evidence, dated Builder session record/index validation/publication, and explicit reporting of remaining stale-data cause or verification limitations. The Builder plan remains in-progress until those steps finish.
