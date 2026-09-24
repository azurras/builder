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
- Cane's public history API on 2026-09-23 reported only 9 snapshots from 2026-06-01 through 2026-09-07; no snapshots existed for the scheduled 2026-09-14 or 2026-09-21 weeks. The latest snapshot was complete (50/50 metro entries, collected 2026-09-07T11:00:16.849Z). The Monday 06:00 America/Chicago schedule's root cause for the missing weeks remains unconfirmed.
- The production WFL scheduler is configured by default for the 15th at 03:00 America/Chicago; the import startup catch-up compares only the prior month's successful completion month.
- Protected application logs are unreadable to this account; do not change their ACLs. The import's exact production failure cause remains unconfirmed.
- `:website:check` passed on `origin/main` SHA `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c` after setting a per-process short JDK Unix-domain socket temp path. No environment or `.env` overrides were present in the isolated worktree. The full check used mocked/unit boundaries; external PostgreSQL contract tests were skipped because the local test role has no configured password.
- The authoritative checkout has unrelated local changes; implementation uses `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`.

## Branch
`codex/site-bug-audit-20260923` from refreshed `origin/main` `feb3f78ae24cf4b22c4035b25068fb78a1b68d5c` delivered PR #1398. Cane's follow-up was developed in `codex/site-bug-audit-round2-20260923`, based on merged SHA `f1db692c7b5dff1de7ce4490c07908935ee8f8b0`, and delivered PR #1399. Preserve the dirty authoritative checkout.

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
- Verification: Confirmed the monthly schedule and catch-up comparison in source. Startup catch-up fails to retry after the current month's scheduled occurrence when the prior successful completion predates that occurrence; add a deterministic regression test in Task 2. A targeted scan found no other monthly prior-completion-month check. It did surface a separate stale Cane's weekly history symptom; its startup recovery is specified in Task 3 while the reason for missed scheduled executions remains unconfirmed.

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

### Task 3 - Catch up an overdue Cane's weekly collection on startup
- Dependencies: Task 1 live freshness and scheduler audit.
- Files: `website/src/main/java/dev/christopherbell/canesboxtracker/CanesBoxTrackerService.java`, `website/src/main/java/dev/christopherbell/canesboxtracker/model/CanesBoxTrackerProperties.java`, `website/src/test/java/dev/christopherbell/canesboxtracker/CanesBoxTrackerServiceTest.java`, and `website/src/main/java/dev/christopherbell/canesboxtracker/README.md`.
- Symbols: `collectCurrentWeek`, current week selection, `CanesBoxPriceSnapshot.collectedOn`, the weekly cron and zone, and the durable `canes-box-price-collection` lease.
- Inspection: Public history currently has a complete Sep 7 snapshot (50 metros) but no Sep 14 or Sep 21 snapshots despite a Monday 06:00 America/Chicago cron. `fetchMetroPrice` converts per-metro exceptions into failed datapoints and `collectWeek` still saves a full snapshot; absent week records therefore show that no complete scheduled workflow was persisted, but do not identify why. The current service has no startup catch-up.
- Required skills: `write-jane-street-style-code` and focused regression tests before implementation.
- Behavior: At application readiness, when the feature is enabled and `deploy-smoke` is not active, inspect recent snapshots and retry the current week's collection through the existing lease-protected method if a configured weekly cron occurrence after the latest complete metro snapshot is due. A current-week full snapshot suppresses duplicate startup collection. A manually entered partial current-week snapshot does not hide an overdue scheduled collection. With no history, perform the existing first-data catch-up behavior.
- Invariants: Keep the Monday cron and configured time zone, current-week key semantics, provider failure capture, coordinator/lease ownership, and admin APIs. Do not start collection in `deploy-smoke` or when disabled. No schema/API changes; no local request reaches production data or the external Cane's service during unit tests.
- Boundary/API: Existing weekly history repository, schedule configuration, and coordinator only.
- Effects and failures: An overdue startup collection can make the existing configured provider calls for the metro set and persist the current week's snapshot. Lease contention skips work. Existing per-metro failures remain recorded. No change to cutover or local candidate scheduling behavior.
- Tests and evidence: Add regression coverage for an overdue prior complete snapshot, no retry before the next scheduled occurrence, duplicate suppression when this week's complete snapshot already exists, and incomplete current-week manual data. Run focused `CanesBoxTrackerServiceTest`, full `:website:check`, then the packaged candidate on an isolated port and disposable database; startup network effects remain disabled in `deploy-smoke`.
- Verification: Live API read at 2026-09-23 22:32:23 UTC confirmed latest week `2026-09-07`, collected at `2026-09-07T11:00:16.849Z`, with 50/50 successful metro prices and no week entries for Sep 14 or Sep 21. The API returned HTTP 200. Regression tests failed before the catch-up logic and passed afterward; focused `CanesBoxTrackerServiceTest` and full `:website:check` passed. The packaged candidate ran with `test,deploy-smoke` on port 8082 against a disposable PostgreSQL 18 `test` cluster; all seven health/page/API GETs returned HTTP 200 and both candidate and cluster were stopped. Report: [Cane weekly catch-up runtime verification](../test-reports/2026-09-23-2026-09-23-christopherbell-dev-cane-weekly-catch-up-runtime-verification.md). PR #1399 passed dependency review, CodeQL, Java and JavaScript analysis, and macOS, Ubuntu and Windows builds; it was squash-merged at 2026-09-23 23:06:42 UTC as `5f89e5c286e9c96b1d45dcfbd88bc036cc39c34c`. Post-merge CI Build passed on Windows (9m03s), macOS (4m08s), and Ubuntu (3m44s). Latest public read at approximately 2026-09-23 23:16 CDT still shows the Sep 7 Cane's snapshot and stale WFL freshness timestamp `2026-08-02T22:44:50.963Z`; production remains on listener PID 14424. No protected state or logs were read. Deployment and production acceptance remain blocked because the local token cannot read protected deployment state or start the SYSTEM task, and the platform rejected an elevation request. Do not weaken ACLs or bypass the supported deployment path; resume from an authorized elevated deployment session.

### Task 4 - Make the Windows SYSTEM deployment test run pass
- Dependencies: PR #1399 merge; production deployment acceptance of its runtime build.
- Files: `website/src/test/java/dev/christopherbell/configuration/persistence/migration/FinalizeEvidenceLoaderTest.java`.
- Symbols: `productionAuthorityRootIsFixedAndSelfMintedOwnerOnlyFilesAreRejected`, `AclFileAttributeView`, and production write-principal validation.
- Inspection: After the user approved elevation, read the protected auto-deploy state and confirmed `ChristopherBellAutoDeploy` had been disabled since 2026-09-05. The supported `prod.cmd auto-install -WhatIf` preflight passed; running documented `prod.cmd auto-install` from the worktree whose Git tree matches merged `origin/main` restored the SYSTEM poller. It detected remote SHA `5f89e5c286e9c96b1d45dcfbd88bc036cc39c34c`, built 2,282 tests, and failed one after 6m45s. The Gradle daemon report names `FinalizeEvidenceLoaderTest.productionAuthorityRootIsFixedAndSelfMintedOwnerOnlyFilesAreRejected` with `UserPrincipalNotFoundException` at the current-user lookup line. A first alias qualification fix was merged as PR #1400, but the subsequent actual SYSTEM build at `de7904065c202b839ad9d4e3be477c6fd287127e` failed the same test and exception class. The auto-deploy cleanup removed the failed release worktree and test XML; the live service was never stopped. The poller remains enabled and records the SHA as failed.
- Required skills: `write-jane-street-style-code` and focused regression verification.
- Behavior: Remove dependence on the SYSTEM process account name from this fixture. Make the self-minted Windows file carry an explicit untrusted `Everyone` write ACE so production write-principal validation must reject it; preserve the fixed production-root assertion.
- Invariants: Test-only change; preserve production ACL policy and evidence-authority checks; never leave owner-only ACLs or test artifacts in ProgramData; keep production service and listener untouched until the fully guarded deployment reaches cutover.
- Boundary/API: Local Windows test fixture principal lookup only; no production endpoint, schema or runtime authorization changes.
- Effects and failures: Only the isolated Gradle test fixture is affected. The existing automatic deploy uses the protected Gradle home; do not manually delete or modify its caches.
- Tests and evidence: Both actual SYSTEM builds provide the red case: merged `5f89e5c` failed with one test failure after 6m45s; PR #1400 SHA `de790406` failed the same test after 5m53s (2,283 tests, one failed, 300 skipped). The first fix passed all eight focused tests and native Windows `:website:check` locally but did not survive the SYSTEM execution context. Revised fixture now adds an explicit untrusted `Everyone` write ACE. All eight focused tests pass normally and with JVM `user.name=SYSTEM`; full native Windows `:website:check` passed in 5m27s. PR #1401 SHA `943da3b5a9e3fbc4a4116f235b5ce180fa7854cd` is open; required Ubuntu, macOS, Windows, CodeQL and dependency-review checks are pending. After merge, record active release SHA, listener rotation, readiness/routes, and both freshness APIs.
- Verification: In progress. PR #1400 merged at 2026-09-24 00:47:23 UTC. At 00:54:43 UTC the enabled poller recorded `de7904065c202b839ad9d4e3be477c6fd287127e` as failed; production service remained Running with port 8080/PID 14424 and no candidate listener. Public readiness returned HTTP 200, WFL freshness was still `2026-08-02T22:44:50.963Z` and current=false, and Cane's history remained nine weeks through Sep 7. PR #1401 checks and production acceptance remain pending.

## Code Changes
Task 2 is limited to WFL startup catch-up selection, direct unit tests and the owning feature README's scheduling contract. Task 3 extends the existing Cane's weekly collector's startup behavior without changing its persistence schema or API. Reinspect all targets before edits.

## Files and Modules
Spring services for WFL restaurant imports and Cane's weekly price collection, their unit tests, and their owning feature READMEs.

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
Both reported cadence defects have regression tests that fail before and pass after their fixes; native checks and alternate-port runtime proof pass; required CI passes and each reviewed fix merges. Supported production deployment and exact production acceptance evidence, dated Builder session record/index validation/publication, and explicit reporting of remaining stale-data causes or verification limitations remain required. The Builder plan stays in-progress until those steps finish.
