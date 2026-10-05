# Register the Production Watch Workflow: Test Report

## Story/Issue
GitHub never registered `production-watch.yml`: `gh workflow run production-watch.yml` returned HTTP 404 and `/actions/workflows` omitted it, because the push event for `06c3718`, which added it, was dropped. Logged in the [follow-up plan](../implementation-plans/2026-10-05-10-11-christopherbell-dev-recover-missed-ci-runs-and-clarify-token-install-failures.md).

## Branch
`claude/register-production-watch-20261005` at `e0728a8`

## Pass / Fail

> [!TIP]
> **3 of 3 passed** on candidate `e0728a8`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Workflow contract | ✅ PASS | `GitHubAutomationConfigurationTest` passes with the edited file: triggers, permissions and pins unchanged |
| 2 | Watch script against live production | ✅ PASS | The script the workflow runs reports production healthy on `ca98b1e`, with all six checks passing |
| 3 | Renormalized Gradle wrapper | ✅ PASS | `gradlew.bat` is stored LF and checked out CRLF; builds through it pass and leave the tree clean |

## Test Cases
1. **Workflow contract:** parse and assert the edited workflow file.
2. **Watch script against live production:** `Get-ProductionWatchVerdict` from the candidate checkout against https://www.christopherbell.dev and GitHub, read-only, with the production thresholds.
3. **Renormalized Gradle wrapper:** after `git add --renormalize gradlew.bat`, run the build and supply-chain tests through the wrapper and confirm `git status` stays clean.

## App / Environment

| Setting | Value |
|---|---|
| App | `.github/scripts/Test-ProductionSite.ps1` from the candidate checkout; production website `ca98b1e` |
| Runtime | PowerShell 7, Windows 11; GitHub API with the operator's `gh` token held in a process variable only |
| Change | Comment-only edit to `.github/workflows/production-watch.yml` plus a line-ending renormalization of `gradlew.bat` (no content change); the website and tooling are unchanged, so no website candidate run applies |

## Local Run Details
- **Local command:** `Get-ProductionWatchVerdict -Repository azurras/christopherbell.dev -SiteUrl https://www.christopherbell.dev -DeployLagThresholdMinutes 45 -ProbeAttempts 3 -ProbeRetryDelaySeconds 10`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\register-watch-20261005`
- **Candidate identity:** `e0728a8`, clean tree before and after the Gradle run.
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

### 3. Renormalized Gradle wrapper

```text
git ls-files --eol gradlew.bat
gradlew.bat :website:test --tests GitHubAutomationConfigurationTest --tests BuildSupplyChainConfigurationTest --tests BuildAutomationConfigurationTest
git status --porcelain
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

### 3. Renormalized Gradle wrapper

```text
i/lf    w/crlf  attr/text eol=crlf    gradlew.bat
exit status: 0 (BUILD SUCCESSFUL in 5s; 14 tests passed)
git status --porcelain: empty before and after
```

## Evidence
- `gh api repos/azurras/christopherbell.dev/actions/workflows` lists every other workflow but not `production-watch.yml`, while `contents/.github/workflows?ref=main` contains it.
- Run at about 10:59 CDT.

## Bugs / Follow-ups
- Superseded candidate `0e2bf8a`: preflight refused it because `gradlew.bat` showed a phantom line-ending modification on every fresh checkout. `e0728a8` renormalizes the file.
- After merge, confirm the workflow is listed and complete one manual run.

## Document Status
complete

## Project
christopherbell-dev
