## Document Status

complete

## Story/Issue

Task 44 in `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`: preserve safe, useful route identity in non-elevated automatic-deployment failure details, then deploy and verify the merged production revision.

## Branch

PR #1444, `codex/safe-smoke-failure-diagnostics-20260925`, final head `3ccd9b33f491b47b97f38fd397e6b1eb51cf3421`; merged as `375f527910d2beae8db6ff36dc1236656a31ff9e` at 2026-09-25 20:52:37 UTC.

## App / Environment

Application under runtime verification: `https://www.christopherbell.dev/` on native Windows production. The deployment ran through the installed `ChristopherBellAutoDeploy` SYSTEM poller. All inspection, Pester runs, route requests, and status reads in this session were non-elevated; no UAC prompt, protected log read, ACL change, database operation, or manual service/release mutation was used.

## Local Run Details

Runtime targets were the native Windows production listener at `http://127.0.0.1:8080/` and the public site at `https://christopherbell.dev/` and `https://www.christopherbell.dev/`.

Added an allowlist-only projection for local/public smoke-route labels in `Get-AutoDeploySafeFailureDetail`. It accepts only exact raw, case-sensitive paths and approved host/scheme/port combinations; arbitrary routes and URI credentials, queries, and fragments remain redacted. Regression tests cover credentials/query/fragment values, variable login paths, unknown hosts, wrong schemes, unsupported ports, trailing-dot aliases, URI dot segments, and case variants.

The AutoDeploy and Command Pester suites passed on PowerShell 7.6.6/Pester 5.9.0 and Windows PowerShell 5.1/Pester 5.9.0. The final PR passed Windows, macOS and Ubuntu CI, CodeQL and dependency review. Independent review found two path-classification edge cases during the PR and confirmed their fixes at the final head.

## Test Cases

- Allowlisted fixed smoke paths produce a short local/public route label.
- Credentials, query values, fragments, variable paths, unknown hosts, invalid schemes/ports, URI path aliases and case variants do not produce a route label or leak sensitive values.
- AutoDeploy and Command Pester suites under both supported PowerShell versions.
- Windows PowerShell 5.1 parser checks for the edited module and tests.
- Non-elevated post-deployment status and local/public smoke-route sweep.

## Data Sent

Read-only HTTP GET requests to each of the 11 smoke-route paths at `http://127.0.0.1:8080/`, `https://christopherbell.dev/`, and `https://www.christopherbell.dev/`, plus a public homepage request. These requests exercised the running production app without request bodies, database reads/writes, account changes, or protected-log access.

## Response Received

- At `2026-09-25T21:00:10.2220714Z`, non-elevated `prod.cmd auto-status` reported `SUCCEEDED`, `HEALTHY`, `remoteSha=activeSha=successfulSha=375f527910d2beae8db6ff36dc1236656a31ff9e`, and `toolRefreshStatus=SUCCEEDED` from the same source SHA. Installed tool bundle SHA: `0e20fc6282e42d01fb05f6fdaeb760785f208443`.
- At `2026-09-25T21:02:11.3627249Z`, a subsequent poll reported `UP_TO_DATE`, `HEALTHY`, no failed SHA, no retry deadline, and the same active/successful SHA. `ChristopherBellDev` was `Running`, startup type `Automatic`.
- The post-deployment sweep returned HTTP 200 for all 33 requests: 11 local routes and 22 requests across both public hostnames. Maximum observed request time was 1,250 ms. The homepage title was `CB | Home`.
- Each route response had status code: 200; the homepage returned the expected `CB | Home` title.

## Pass / Fail

- Safe route-detail regression: passed; pre-fix tests reproduced trailing-dot, dot-segment and case-folded false labels.
- AutoDeploy and Command Pester suites: passed, 91/91 under PowerShell 7 and 91/91 under Windows PowerShell 5.1.
- Windows PowerShell 5.1 parser checks and `git diff --check`: passed.
- PR #1444 required CI Build, CodeQL and Dependency Review: passed; independent final review had no remaining findings.
- Supported production tool refresh and release deployment: passed without elevation.
- Post-deployment status, service state, and 33 local/public route checks: passed.

## Evidence

- PR #1444: https://github.com/azurras/christopherbell.dev/pull/1444
- Merged commit: `375f527910d2beae8db6ff36dc1236656a31ff9e`.
- Production runtime evidence: non-elevated `prod.cmd auto-status` readbacks at the timestamps above, `Get-Service ChristopherBellDev`, and direct GET responses for the 33 smoke requests.

## Bugs / Follow-ups

Four automatic attempts to deploy the previous trusted revision `7639e3f1b552013a72cb59f0e32807fc6356daf3` timed out and used guarded rollback to keep the site on `4b552a63a08c9333bdaa0d7827b23eb811920f37`. The earlier installed tool had already redacted the failed URI in its persisted status, so the exact route and historical cause cannot be recovered from non-elevated status. Deployment of the next trusted revision, which included the safe route diagnostic, succeeded and left production `UP_TO_DATE` and healthy. Standard-user Scheduler queries remain `ACCESS_DENIED`; recurring task executions and successful tool refresh were observed through the public-readable status transitions.
