# 2026-09-28 - christopherbell-dev Session Memory

Work, decisions, events, and evidence for this date.

## 2026-09-28 10:41 - WFL retry deployment and readiness timeout

## 2026-09-28 10:41 Central Daylight Time - WFL retry deployment and readiness timeout

Continued the authorized christopherbell.dev site bug audit after the user approved one daily retry for overdue WFL import failures. PR #1445 (daily WFL retry and legacy month-only due-date correction) had merged as `e45010373cfcf123815febc5869845bc968616b0`. Focused workflow tests passed 15/15; native `:website:check` passed in 5m22s; the packaged candidate passed readiness and homepage requests against isolated MongoDB database `test` on port 27019, then candidate and disposable database processes were stopped.

The supported SYSTEM poller initially timed out twice on `[local smoke route: readiness]` after release activation. Each attempt restored the prior release and healthy service; the failure appeared while production readiness was temporarily `OUT_OF_SERVICE`. Source inspection found `Test-ProductionEndpoints` gave `/actuator/health/readiness` 30 seconds, although `/` already received 180 seconds. No protected logs or task state were accessed. Added plan Task 46 and published it in Builder commit `c6d31c5` before editing code.

On `codex/production-readiness-smoke-timeout-20260928`, changed only the local readiness timeout to 180 seconds and updated the Pester contract. The modified regression failed first on the old 30-second behavior; all 99 tests in `Production.Deploy.Tests.ps1` passed after the fix. Windows PowerShell parser checks and `git diff --check` passed. PR #1446 merged as `29e86bb4c959d989d81ee13e9da24a9177d313f3`; all required checks and post-merge CI passed across Windows/macOS/Ubuntu, analysis, CodeQL, and dependency review.

The supported poller refreshed tools from the merged SHA and deployed it. Production readiness returned 503 temporarily during startup, then recovered within the new 180-second bound. `prod.cmd auto-status` reported `UP_TO_DATE`, service `RUNNING`, health `HEALTHY`, and active/successful SHA `29e86bb4c959d989d81ee13e9da24a9177d313f3`. All 33 smoke requests passed (11 local and 22 public across apex and www). Public WFL freshness returned HTTP 200, `lastRefreshedOn=2026-09-28T15:37:50.362Z`, and `current=true`; no manual import was applied. Runtime evidence: [WFL daily retry runtime verification](../test-reports/2026-09-28-christopherbell-dev-wfl-daily-retry-runtime-verification.md); plan: [site bug audit and fixes](../implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md).

The unprivileged scheduled-task query still reports `ACCESS_DENIED`; successful poller executions are visible via status transitions. A subsequent daily retry after a new transient failure has not been independently observed. The broader site audit continues.

## 2026-09-28 11:33 Central Daylight Time - Cane's failure diagnostics

Continued site bug audit Task 47. The public Cane's API showed the 2026-09-28 snapshot had 0/50 successful metro samples and 50 excluded, with upstream failures rendered as `null`. Source inspection found both official-source catches directly concatenated exception messages. A read-only query to the configured official gateway from this host returned HTTP 403; no protected application logs were accessed. The third-party public-menu fallback remains disabled.

Added a null/blank exception-message fallback to the exception class name, a regression test, and feature README guidance. Focused client tests passed 17/17, full `:website:test` and packaged `:website:bootJar` succeeded. A candidate on port 18081 passed readiness 200/UP and homepage 200 (`CB | Home`) against an isolated copy of the previously verified restored fixture in Mongo database `test`; the initial blank-database attempt correctly failed migration 015's domain-schema preflight. The candidate and disposable Mongo listener were stopped.

PR #1447 merged at `a9b01063fc7ac086ee8ae43c2c4ff9344a7ec4d4`; all required checks and post-merge CI passed. The supported poller deployed the SHA and reported `UP_TO_DATE`, service `RUNNING`, and health `HEALTHY`. Fifteen read-only GETs across the local listener and both public hostnames (readiness, home, Cane's page/API, WFL freshness) returned HTTP 200. Production WFL remains current at `2026-09-28T15:37:50.362Z`.

The stored Cane's snapshot remains unchanged with the old `null` text, since no production collection was triggered. The improved diagnostic is active but its next real collection output remains unobserved; the upstream HTTP 403 remains unresolved. Runtime evidence: [Cane's failure diagnostics runtime verification](../test-reports/2026-09-28-christopherbell-dev-canes-diagnostic-runtime-verification.md). The audit continues.
