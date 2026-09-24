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


## 2026-09-23 18:16 - Cane weekly recovery and merged fix

## Request and authority
Continued the user's authorized broad site bug audit and fixes. Kept work in the isolated spoke worktree and preserved the dirty authoritative checkout.

## Second confirmed defect and fix
- Production Cane's history had no weekly snapshots for 2026-09-14 or 2026-09-21; its latest snapshot was 2026-09-07 with 50/50 successful metros. The exact cause remains unconfirmed.
- Added startup catch-up for overdue weekly collection in `CanesBoxTrackerService`, using the existing collector lease, schedule cron/time zone and metro snapshot history. Added coverage for overdue runs, no-history first collection, next-run timing, duplicate suppression, partial manual snapshots, duplicate metro rows, disabled/deploy-smoke modes, and failure containment. Updated the feature README.
- Regression tests reproduced three gaps before implementation (missed startup catch-up, duplicate metro rows incorrectly appearing complete, and startup catch-up exception escaping readiness); fixes pass afterward. Focused `CanesBoxTrackerServiceTest` and full `:website:check` passed.
- Packaged candidate ran on port 8082 with `test,deploy-smoke` and isolated disposable PostgreSQL 18 `test` DB at 5433. Liveness, readiness, homepage, Cane's page/history API, WFL ranking and freshness API all returned HTTP 200. Candidate and cluster were stopped. Runtime evidence is in `docs/test-reports/2026-09-23-2026-09-23-christopherbell-dev-cane-weekly-catch-up-runtime-verification.md` (Builder commit `e4bf356`).

## Review and merge
- Committed `586ec6c1` on `codex/site-bug-audit-round2-20260923`; opened and attached [PR #1399](https://github.com/azurras/christopherbell.dev/pull/1399).
- Dependency review, CodeQL, Java and JavaScript analysis, and macOS, Ubuntu and Windows PR builds passed. Squash merge SHA: `5f89e5c286e9c96b1d45dcfbd88bc036cc39c34c` at 2026-09-23 23:06:42 UTC. Post-merge CI Build passed on Windows (9m03s), macOS (4m08s), and Ubuntu (3m44s). PR artifact is attached to the task.
- Additional source scan of `@Scheduled` jobs did not identify another confirmed missed-run defect of this type.

## Production status and outstanding blocker
- No automatic deploy workflow is configured; merge does not publish to the production host. At approximately 2026-09-23 23:16 CDT, public Cane's history still showed only nine weeks through 2026-09-07; WFL freshness still read `2026-08-02T22:44:50.963Z`, `current=false`; production port 8080 still belonged to PID 14424.
- The deployment remains unverified because the current Windows shell cannot read protected deployment state or start the SYSTEM scheduled task. A prior `RunAs` elevation request for a non-mutating dry run was rejected by platform policy. Do not weaken ACLs or bypass the supported deployment procedure.
- Updated implementation plan `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md` with both merged fixes, CI and runtime evidence, and the deployment limitation. The plan remains in progress pending an authorized elevated deployment and production acceptance.


## 2026-09-23 23:18 Central Daylight Time - Deployer robustness implementation

## 2026-09-23 23:16 Central Daylight Time - Deployer robustness implementation

User narrowed the ongoing site-bug goal to deployer robustness and observability without elevated access, and authorized deployment once ready while asking to be told when approval is needed. Continued in `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923` on `codex/auto-deploy-observability-20260923`; the authoritative dirty checkout remained untouched.

- Implemented a fixed sibling status store with SYSTEM/Administrators write and standard-user read ACLs, reparse and file-size checks, allowlisted sanitized JSON, atomic file replacement, freshness, unavailable reason codes, deployment phases, SHAs, retry time, tool refresh result, and no protected-config read in `auto-status`.
- Deployment exceptions now remain failures after state persistence. Protected marker read errors report as check failures; actual migration gates remain blocked outcomes. Best-effort status/log failures do not mask the deployment cause.
- Added SYSTEM tool refresh from fetched trusted main. A temporary detached worktree must match the commit; tool bundles are immutable and keyed by the `ops/production/windows` Git tree hash to avoid duplicate versions for application-only commits. The protected manifest records the source commit and hashes every file. The updater holds `deploy.lock`, validates ACLs/reparse paths and manifest, cleans partial stages, changes only the task action after complete publication, and lets the next poll run the new version.
- Documented standard-user status and the first elevated `auto-install` bootstrap requirement in `docs/operations/windows-production.md`.
- Verification: AutoDeploy Pester 21/21; Production Operations Pester 91/91; PowerShell 5.1 module import passed; standard-user `prod.cmd auto-status` returned `STORE_NOT_INITIALIZED` with a safe message rather than Access Denied; `git diff --check` passed. Pester 3.4 on Windows PowerShell cannot run the repository's Pester 5 assertions. Native `:website:check` failed before task execution twice with JDK `PipeImpl` loopback `Invalid argument`, including using a private `GRADLE_USER_HOME`.
- The installed SYSTEM task and production listener/data were not changed. Tool refresh and sanitized status publication are not yet live-verified. First bootstrap needs an approved elevated `auto-install`; routine refreshes after that are autonomous. Full evidence: `docs/test-reports/2026-09-23-2026-09-23-christopherbell-dev-auto-deployer-robustness.md`. The implementation plan remains in progress pending publication, CI, bootstrap approval, and live acceptance.
