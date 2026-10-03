## Document Status

complete

## Story/Issue

Task 68: keep automatic deployment status fresh during long builds and candidate readiness checks. No separate source issue exists.

## Branch

`codex/autodeploy-progress-heartbeat-20261003`, source commit `64a23bda6e024a78f83f996fec9c7ddad40f9250`; merged PR [#1470](https://github.com/azurras/christopherbell.dev/pull/1470) as `682f50e568036c5db282fc9384c715cfaceac5f0`.

## App / Environment

Application runtime under test: the live Windows production service. The base URL under test was `https://christopherbell.dev/`; the alternate public base URL was `https://www.christopherbell.dev/`. The supported SYSTEM auto-deployer refreshed its tools and deployed the merged revision. Status checks ran as a normal user through `prod.cmd auto-status`, without reading protected configuration or task definitions.

## Local Run Details

No local application process was started. The production deployment built and validated the candidate through the supported mechanism. Tool refresh was reported at `2026-10-03T22:26:44Z`; deployment began at `22:27:10Z` and completed at `22:33:08Z`. The deployer performed its normal cleanup; no manual restart was used.

Local `:website:check` with Java 25 and Gradle 9.6.1 stopped before project configuration with `Unable to establish loopback connection`. A standalone Java `Selector.open()` reproduced the same error. No elevation or firewall/ACL changes were attempted. GitHub CI passed the Java 25 build on Windows, macOS, and Ubuntu.

## Test Cases

1. Full Windows production Pester suite on PowerShell 7.
2. Focused common-process and auto-deploy Pester tests on Windows PowerShell 5.1 with Pester 5.9.0.
3. PR validation: Java 25 build on Windows, macOS, and Ubuntu; CodeQL; Dependency Review.
4. Live status during the real SYSTEM deployment.
5. Public home page GET requests on both public base URLs after deployment.

## Data Sent

- Read-only `prod.cmd auto-status` polling every 15 seconds from `2026-10-03T22:26:17Z` through completion. It reads the sanitized status record and runs its standard live health check.
- HTTP GET `/` to `https://christopherbell.dev/` and `https://www.christopherbell.dev/`; no body, custom credentials, or custom headers.
- No application data was manually written for verification.

## Response Received

- PowerShell 7 full production Pester suite: 820 passed, 28 skipped, 0 failed.
- Windows PowerShell 5.1 focused suite: 108 passed, 0 failed.
- `git diff --check`: passed.
- PR checks passed: Windows/macOS/Ubuntu Java 25 builds, CodeQL, and Dependency Review.
- Six fresh `DEPLOYING` timestamps: `22:27:10.747Z`, `22:28:10.839Z`, `22:29:11.326Z`, `22:30:11.804Z`, `22:31:12.309Z`, `22:32:12.839Z`. They span 302 seconds, beyond the prior 180-second stale threshold. Service stayed `RUNNING` and site health `HEALTHY` throughout.
- Terminal status at `22:33:08Z` was fresh `UP_TO_DATE`. Remote, active, attempted, successful, and tool source SHAs all matched `682f50e568036c5db282fc9384c715cfaceac5f0`; tool bundle SHA was `3ba44ebe09febd29ca95d43910c77a9edb28d76e`. Service `RUNNING`, site `HEALTHY`.
- At `22:35:11Z`, status remained fresh `UP_TO_DATE` with those matching revisions and health.
- Both public home requests returned HTTP status code: 200, title `CB | Home`, body size 4,348 bytes.

## Pass / Fail

Pass. The heartbeat stayed observable for over five minutes during the real deployment, then the merged revision became active and healthy. Pester, required CI, and public endpoint checks passed. The local Gradle check limitation was environmental; the CI matrix and production build/candidate validation passed.

## Evidence

- [PR #1470](https://github.com/azurras/christopherbell.dev/pull/1470)
- Merge SHA: `682f50e568036c5db282fc9384c715cfaceac5f0`
- Status snapshots and HTTP results are recorded above.
- Gradle and standalone Java both reproduced the local loopback-selector failure.

## Bugs / Follow-ups

The deployment-status regression is fixed and verified. The heartbeat made no schema, production configuration, or manual application-data changes. Standard-user scheduler details remain `UNKNOWN` with sanitized reason `ACCESS_DENIED`; the status record itself is fresh and site health is confirmed. No further Task 68 action remains.
