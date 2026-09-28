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

## Cane trend as-of context and WFL retry confirmation

The user approved one daily retry for overdue WFL import failures. Confirmed that this behavior was already implemented in PR #1445 (`e45010373cfcf123815febc5869845bc968616b0`); its focused workflow tests passed 15/15, and the retry is present in the deployed release. No additional WFL code change was needed.

Completed site audit Task 48, clarifying that the existing Cane's month-over-month percentage uses the latest priced week and its comparison week. Added a pure JavaScript caption formatter, regression test, and feature README explanation without changing trend calculations, public API, stored data, or collector behavior. Focused JavaScript tests passed 344/344; `:website:check --no-daemon --console=plain --max-workers=1` passed 21 Gradle tasks, including Java, JavaScript, and Windows Pester checks. The isolated packaged candidate rendered `+0.2%` with `Latest priced week: 2026-09-21. Compared with week of 2026-08-24.`

PR #1448 passed required checks and merged as `ff60887f6fb914827815fd670f03782bc82286e9`. The supported deployer reached `UP_TO_DATE` / `RUNNING` / `HEALTHY` / `FRESH` with remote, active, attempted, and successful SHA values matching the merge. Production readiness and history API returned HTTP 200; the production browser showed the same trend caption. The newest Cane's snapshot remains 2026-09-28 with no average, 0/50 verified metros, and 50 excluded. No collection was triggered and no production data was altered. The non-elevated poller-registration detail remains `ACCESS_DENIED`. A candidate-only Mongo data copy remains isolated in `%TEMP%\codex-canes-index-asof-candidate-20260928\mongo-data` because removal was rejected by execution policy; its process and port were stopped/closed.

Evidence: [Task 48 plan](../implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md), [candidate and production runtime verification](../test-reports/2026-09-28-cane-box-trend-as-of-context-candidate-runtime-verification.md). The broader site bug audit continues.

## Cane's official source access diagnosis

For the still-empty 2026-09-28 Cane's snapshot, performed three read-only probes from the production host: one location-search GraphQL POST to the configured gateway, one GET to its legacy official `restaurants/byref` endpoint, and one GET to the official order page. Each returned HTTP 403 with `text/html; charset=UTF-8` from a `cloudflare` server and an 864,550-byte body rather than JSON. The evidence narrows the block to an edge response before client parsing, but does not reveal the provider's policy reason. No challenge was solved or bypassed, credentials were not supplied, and no collector or data mutation was run. The fix now depends on a permitted provider route/access or explicit manual price verification; public fallback remains disabled to avoid stale third-party prices. Evidence: [Cane's failure diagnostics runtime verification](../test-reports/2026-09-28-christopherbell-dev-canes-diagnostic-runtime-verification.md).


## 2026-09-28 12:54 - Reconfirm production status and tool refresh

Read-only `prod.ps1 auto-status` at 2026-09-28 17:53:12 UTC reported `UP_TO_DATE`, `RUNNING`, `HEALTHY`, and `FRESH`; remote, active, attempted, and successful SHAs all matched production merge `ff60887f6fb914827815fd670f03782bc82286e9`. Trusted deployment tools had refreshed successfully at 17:53:11 UTC from that source SHA. Poller registration still reports `UNKNOWN` / `ACCESS_DENIED`, so this confirms a recent poller run but not whether its scheduled task is enabled. No task, configuration, service, or deployment state was mutated. Updated the Task 48 production runtime report with this read-only evidence.


## 2026-09-28 13:43 Central Daylight Time - Workflow action test stability

Continued the authorized site bug audit with Task 49. The user approved one daily retry for an overdue failed WFL import; the existing Task 45 implementation is already merged as PR #1445 and deployed, so no duplicate code change was needed.

PR #1387's action updates exposed a CI test defect: `GitHubAutomationConfigurationTest` constants included the old full action SHAs, and `stepUsing` required an exact match. I temporarily applied the official updated Gradle and CodeQL pins from PR #1387; the focused suite reproduced exactly two failures (`codeQlPreservesAllDefaultSetupLanguagesAndBuildsJava` and `ciCachesGradleAndRetainsFailedReports`), while the global full-SHA assertion passed. Changed the test constants to action repository paths and made `stepUsing` match `<repository>@`; retained the separate 40-character immutable-SHA guard. With those same temporary workflow pins, the focused suite passed 10/10. Restored both workflow fixtures before reviewing or publishing.

`:website:check --no-daemon --console=plain --max-workers=1` passed all 21 tasks, including Windows Pester suites (203 passed, one expected skip; 75 passed), Java tests, and existing JavaScript checks; `git diff --check` passed. The first local Gradle attempt hit a Java 25 Windows loopback error under the deep default temporary path. Setting `TEMP`/`TMP` and `GRADLE_USER_HOME` under short `A:\` paths allowed the build to run; this was environment setup, not a product failure. Only `website/src/test/java/dev/christopherbell/configuration/GitHubAutomationConfigurationTest.java` was committed. The pre-existing untracked `testResults.xml` in the linked worktree was preserved.

PR #1449 passed dependency review, CodeQL for actions/Java/JavaScript, and Windows/macOS/Ubuntu builds, then merged at 2026-09-28 18:33:03 UTC as `0d159a118b760c5afee693005a4c6caf2a6ea623`. Post-merge CI Build and CodeQL also passed across those platforms and analyses. Because this change only affects workflow assertions, application runtime and production deployment do not apply. PR #1387 itself was not merged; package-only PR #1388 remains outside the scoped fix. Updated plan: [site bug audit and fixes](../implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md).


## 2026-09-28 15:04 Central Daylight Time - Cane history legacy diagnostics delivered

Continued the authorized site bug audit with Task 50 after recording the candidate runtime proof. The public projection now replaces whole-word `null` placeholders in legacy Cane's failure reasons with `details unavailable`, using detached metro copies so stored samples remain unchanged. The WFL daily retry the user approved was already implemented, merged and deployed as PR #1445; Task 45's production freshness readback on this date was `current=true`, so no duplicate WFL code change was needed.

Focused `CanesBoxTrackerServiceTest`, full `:website:check` (21 Gradle tasks), and `git diff --check` passed. The isolated packaged candidate on port 18081 against a copied MongoDB `test` database on 27019 returned readiness 200/UP and history 200 with week 2026-09-28, 0/50 verified, 50 excluded, no average, and sanitized failure text. Readback from the isolated database confirmed the source still contained `null; null`. Candidate app/Mongo ports were closed; production 8080/27017 stayed up.

PR #1450 passed Windows/macOS/Ubuntu CI, CodeQL (Actions, Java, JavaScript) and dependency review; it squash-merged as `ccad01fb711f4299e3b59c423dc17966a29be499`. The supported SYSTEM poller refreshed its trusted tools and automatically deployed the merge SHA from active `0d159a118b760c5afee693005a4c6caf2a6ea623`. Status reached `FRESH` / `SUCCEEDED` / `HEALTHY`, and production readiness returned `UP`. The public history GET returned HTTP 200 with 0/50 verified, 50 excluded, null average, and sanitized diagnostics. Verification was read-only; no production fixture or manual data update was made.

Remaining limitation: production's official Cane's GraphQL/order endpoints were previously observed returning Cloudflare HTTP 403. The current 2026-09-28 sample therefore remains 0/50 verified with no price; public menu fallback remains disabled and no data was fabricated. The non-elevated poller-registration projection remains `UNKNOWN` / `ACCESS_DENIED`, although this successful automatic deployment confirms poller execution. Protected task details/logs were not accessed.

Evidence: [Task 50 plan](../implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md), [candidate and production runtime report](../test-reports/2026-09-28-christopherbell-dev-canes-legacy-failure-projection-runtime-verification.md). The site bug audit work in this plan is complete with the upstream access limitation recorded.
