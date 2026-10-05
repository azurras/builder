# Register the Production Watch Workflow: Test Report

## Story/Issue
GitHub never registered `production-watch.yml`: `gh workflow run production-watch.yml` returned HTTP 404 and `/actions/workflows` omitted it, because the push event for `06c3718`, which added it, was dropped. Logged in the [follow-up plan](../implementation-plans/2026-10-05-10-11-christopherbell-dev-recover-missed-ci-runs-and-clarify-token-install-failures.md).

## Branch
`claude/register-production-watch-20261005` at `0e2bf8a`

## Pass / Fail

> [!TIP]
> **2 of 2 passed** on candidate `0e2bf8a`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Workflow contract | ✅ PASS | `GitHubAutomationConfigurationTest` passes with the edited file: triggers, permissions and pins unchanged |
| 2 | Watch script against live production | ✅ PASS | The script the workflow runs reports production healthy on `ca98b1e`, with all six checks passing |

## Test Cases
1. **Workflow contract:** parse and assert the edited workflow file.
2. **Watch script against live production:** `Get-ProductionWatchVerdict` from the candidate checkout against https://www.christopherbell.dev and GitHub, read-only, with the production thresholds.

## App / Environment

| Setting | Value |
|---|---|
| App | `.github/scripts/Test-ProductionSite.ps1` from the candidate checkout; production website `ca98b1e` |
| Runtime | PowerShell 7, Windows 11; GitHub API with the operator's `gh` token held in a process variable only |
| Change | Comment-only edit to `.github/workflows/production-watch.yml`; the website and tooling are unchanged, so no website candidate run applies |

## Local Run Details
- **Local command:** `Get-ProductionWatchVerdict -Repository azurras/christopherbell.dev -SiteUrl https://www.christopherbell.dev -DeployLagThresholdMinutes 45 -ProbeAttempts 3 -ProbeRetryDelaySeconds 10`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\register-watch-20261005`
- **Candidate identity:** `0e2bf8a`, clean tree.
- **Logs:** command output below.
- **Cleanup:** the `GITHUB_TOKEN` process variable was cleared; nothing was started.

## Data Sent

### 1. Workflow contract

```text
gradlew.bat :website:test --tests dev.christopherbell.configuration.GitHubAutomationConfigurationTest
```

### 2. Watch script against live production

```text
GET https://www.christopherbell.dev/actuator/health/readiness, /, /blog, /actuator/info
GET https://api.github.com/repos/azurras/christopherbell.dev/deployments?environment=Production&per_page=1 (and its statuses)
GET https://api.github.com/repos/azurras/christopherbell.dev/commits/main and ci.yml runs for its head
```

## Response Received

### 1. Workflow contract

```text
exit status: 0
BUILD SUCCESSFUL in 22s
```

### 2. Watch script against live production

```text
All four routes answered HTTP/1.1 200 OK.
LiveCommit=ca98b1e249b2f91e33ab4286cb32a9036d8deda7
Production is healthy.
| GET /actuator/health/readiness | Passed | HTTP 200 |
| GET / | Passed | HTTP 200 |
| GET /blog | Passed | HTTP 200 |
| GET /actuator/info | Passed | HTTP 200 |
| Latest Production deployment | Passed | Deployment of ca98b1e is success: The new release is active. |
| Deployment lag | Passed | main ca98b1e is live. |
```

## Evidence
- `gh api repos/azurras/christopherbell.dev/actions/workflows` lists every other workflow but not `production-watch.yml`, while `contents/.github/workflows?ref=main` contains it.
- Run at about 10:59 CDT.

## Bugs / Follow-ups
- After merge, confirm the workflow is listed and complete one manual run.

## Document Status
complete

## Project
christopherbell-dev
