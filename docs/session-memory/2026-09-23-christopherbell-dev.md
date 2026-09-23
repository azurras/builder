# 2026-09-23 - christopherbell-dev Session Memory

Work, decisions, events, and evidence for this date.

## 2026-09-23 17:21 Central Daylight Time - Site bug audit and overdue WFL import retry

## Request and authority
The user requested a broad site bug audit and fixes, with authorization for necessary work and delivery. Scope included discovery, code changes, verification, PR, and production delivery.

## Repository and initial evidence
- Preserved the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; it had an unrelated `gradlew.bat` edit and an untracked directory. Work proceeded from refreshed `origin/main` in isolated worktree `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`, branch `codex/site-bug-audit-20260923`.
- GitHub live issue inventory was empty; open PRs #1387 and #1388 were Dependabot updates.
- Read-only live audit checked 7,372 sitemap URLs (7,340 restaurant detail URLs excluded from the bulk route sweep), sampled one restaurant detail and `/wfl/top-liked`, plus browser flows for homepage, Void, WFL top-liked, and Raising Cane's tracker. No route or console failures were found in those samples.
- Confirmed a live stale-data symptom: OpenStreetMap freshness API reported `lastRefreshedOn=2026-08-02T22:44:50.963Z`, `current=false` with a 45-day window. Protected production app logs were ACL-denied; their ACLs were not changed. Stale data alone does not prove the sole production cause.
- Source review found startup catch-up checked only whether the previous calendar month had a completed import. A prior success earlier in the same month could therefore suppress retry after the next scheduled monthly cron occurrence was missed.

## Implementation and verification
- Added regression tests for catch-up after an overdue cron occurrence and suppression before the next occurrence. The overdue regression failed against baseline as expected and passed after the fix; the focused service suite passed.
- Updated `RestaurantImportWorkflowService` to compare the next configured cron occurrence after `lastCompletedOn` with current time, retaining first-import behavior when no completion timestamp exists, the durable lease workflow, and the legacy month fallback.
- Updated the WFL restaurant package README to describe the cron-occurrence check.
- Full `:website:check` passed on the patched worktree (75 Pester tests, Java and JavaScript checks). Optional database-contract tests that lacked local DB credentials remained skipped. Host-specific Java 25 loopback initialization required only a per-process `jdk.net.unixdomain.tmpdir` override.
- Built the packaged candidate and ran it on port 8082 with `test,deploy-smoke` profiles against a separate disposable PostgreSQL 18 cluster on port 5433, DB `test`, schema prefix `cbtest_sitebugaudit_`. Liveness, readiness, `/`, `/wfl/top-liked`, and the WFL freshness endpoint returned HTTP 200; DB identity/version were `test`/Flyway 27. Candidate and temporary cluster were stopped; production listener remained on port 8080/PID 14424.
- Runtime report: `docs/test-reports/2026-09-23-2026-09-23-christopherbell-dev-site-bug-audit-runtime-verification.md`, published with report index in Builder commit `aa6659b`.

## PR and CI
- Committed spoke patch as `674b273a` and opened [PR #1398](https://github.com/azurras/christopherbell.dev/pull/1398).
- Dependency review, CodeQL, Java/JavaScript analysis, and macOS, Ubuntu, and Windows builds passed.
- PR was squash-merged as `f1db692c7b5dff1de7ce4490c07908935ee8f8b0` at 2026-09-23 22:12:41 UTC. GitHub CLI merge encountered a local-main worktree conflict; server-side GitHub merge API succeeded. The PR artifact was attached to the Codex task.

## Production status and blocker
- The production Windows host is not running an elevated session. `prod.cmd auto-status` could not read `C:\ProgramData\christopherbell.dev\config\deploy.json`; Task Scheduler query/start access was denied. `Start-Process -Verb RunAs` for a non-mutating deployment dry run was rejected by platform policy. No ACL was weakened and no manual process or release files were changed.
- At 2026-09-23 22:20 UTC and again at 22:20:06 UTC, service `ChristopherBellDev` was Running/Automatic with listener PID 14424, MongoDB and cloudflared were Running/Automatic, public homepage returned HTTP 200, but the WFL freshness API still showed the pre-merge timestamp. No post-merge production release SHA or import recovery is verified.
- The documented deployment path uses the hidden SYSTEM auto-deploy task after merge; manual `prod.cmd deploy` is a break-glass path. Continue checking the ordinary SYSTEM deployment path. If it has not deployed, resume in an authorized elevated production shell; do not bypass the platform elevation restriction or weaken ACLs.

## Builder plan and remaining work
- The in-progress plan is `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`; updated with test, CI, merge, and production-blocker evidence; quality validator passed.
- Remaining: verify post-merge release SHA, production liveness/readiness and representative routes, WFL freshness/import recovery and recurrence window; finish dated session entry after actual outcome; refresh Builder indexes, validate hub, and publish closeout. Do not mark the goal complete until production acceptance and closeout are complete.


## 2026-09-23 17:23 Central Daylight Time - Production readback remains unchanged

## Production readback update
At 2026-09-23 22:23 UTC, a fresh public homepage request still returned HTTP 200, `ChristopherBellDev`, MongoDB, and cloudflared remained Running/Automatic, and port 8080 remained PID 14424. The public WFL freshness API still returned `lastRefreshedOn=2026-08-02T22:44:50.963Z` with `current=false`. No evidence of cutover is available from the current unprivileged token. Earlier `RunAs` dry-run launch remained rejected by platform policy; the user had already authorized deployment. Keep the plan and goal active until an elevated deployment/readback or a user-provided environment change resolves this external blocker.


## 2026-09-23 17:26 Central Daylight Time - Related scheduler audit and live readback

## Related scheduler audit update
A source scan of `@Scheduled` and `ApplicationReadyEvent` code in the site found no second durable monthly/cron importer using the same last-completed-month startup check. Other listed recurring jobs use fixed-delay scheduling or have different startup-maintenance responsibilities; no additional confirmed instance of the WFL defect was found. At 2026-09-23 22:24:52 UTC, public homepage still returned HTTP 200, core services were Running/Automatic, port 8080 was still PID 14424, and public WFL freshness remained `2026-08-02T22:44:50.963Z` (`current=false`). `prod.cmd auto-status` again returned Access Denied for protected `deploy.json`. The goal remains active pending production deployment access and readback.
