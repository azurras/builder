# Recover Missed CI Runs and Clarify Token Install Failures

## Document Status
complete

## Objective

> [!IMPORTANT]
> A `main` commit whose push never started CI can be recovered by hand and is reported by Production Watch. `github-token-install` explains elevation and empty-file mistakes instead of failing with a null error.

## Background
Follow-up to the [CI/CD hardening plan](2026-10-05-08-52-christopherbell-dev-harden-ci-cd-robustness-and-observability.md), merged as `06c3718` in #1481. Three problems surfaced after that merge:

1. GitHub recorded no push event or `pr_merge` activity for `06c3718`, unlike every earlier merge, so no push workflow ran. The new auto-deploy gate correctly reports `AWAITING_CI` and keeps `a9d2058` serving. However, `CI Build` has no manual trigger, so the only recovery is another commit.
2. Production Watch alerts on deploy lag only after `main` passes CI, so a `main` head that never gets a CI run stays silent indefinitely.
3. The user's `github-token-install` attempts failed with "You cannot call a method on a null-valued expression" twice. The first run was from a non-elevated terminal, where `deploy.json` access was denied. The second, elevated run read a 0-byte token file, so `Get-Content -Raw` returned nothing and `.Trim()` ran on null. `Read-AutoDeployGitHubToken` has the same empty-file defect.

## Goals
- `CI Build` can be started by hand on `main`, and the deploy gate accepts a successful manual run for the same commit (AC-1, AC-2).
- Production Watch fails when `main`'s head has no completed, successful CI run more than 45 minutes after its commit time (AC-3).
- `github-token-install` refuses a non-elevated prompt, and both the install and the poller reject an empty token file, each with a clear message (AC-4).
- The change is verified locally, merged, and deployed through the gate, with production serving the new `main` commit (AC-5).

## Non-Goals

| Not doing | Why |
|---|---|
| Auto-triggering CI from the host when no run appears | The host's token has no Actions write permission, and Production Watch surfaces the condition |
| Alerting on red `main` CI | GitHub already notifies on failed runs; the gate refuses red commits by design |
| Rewriting `Read-ProductionConfig`'s non-elevated error for every command | A pre-existing behavior of all protected commands; scoped to the new command |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `ci.yml` has a `workflow_dispatch` trigger, enforced by the workflow contract test |
| AC-2 | `Get-AutoDeployCiConclusion` counts the newest `push` or `workflow_dispatch` run on the configured branch, proven by Pester; other events are ignored |
| AC-3 | Pester proves Production Watch fails "no passing CI run" when `main`'s head has no run, or an unfinished one, older than 45 minutes; passes within 45 minutes; and accepts a successful `workflow_dispatch` run |
| AC-4 | Pester proves `Install-AutoDeployGitHubToken` throws "requires elevated PowerShell" before reading config when not elevated, and that the install and `Read-AutoDeployGitHubToken` reject empty and whitespace-only files with "does not contain a GitHub token" |
| AC-5 | Runtime report published; PR merged with required checks green; production `/actuator/info` reports the merged `main` commit and `auto-status` reports `UP_TO_DATE` or `SUCCEEDED` |

## Inputs
- **Request:** "Let's fix all of these issues", continuing delivery of the earlier plan; the user hit the token-install failures directly.
- **Evidence:** `gh api repos/azurras/christopherbell.dev/events` and `/activity` show no push for `06c3718`, and `/actions/runs?head_sha=06c3718...` is empty. `auto-status` reads `AWAITING_CI` with remote `06c3718` and active `a9d2058`. A 0-byte token file reproduces the null error at `Production.AutoDeploy.psm1:352`.
- **Inspected:** spoke `origin/main` `06c3718`: `.github/workflows/ci.yml`, `GitHubAutomationConfigurationTest`, `.github/scripts/Test-ProductionSite.ps1` (`Test-DeploymentLag`) and its tests, `Production.AutoDeploy.psm1` (`Get-AutoDeployCiConclusion`, `Read-AutoDeployGitHubToken`, `Install-AutoDeployGitHubToken`), `prod.ps1`, and the elevation checks `Assert-Administrator` (Install) and `Assert-SensorAdministrator` (Sensors).

## Branch
`claude/cicd-followup-20261005` from `origin/main` `06c3718`, in worktree `christopherbell.dev-worktrees/cicd-followup-20261005`.

## Assumptions
- A `workflow_dispatch` run on `main` reports `head_branch` `main` and the dispatched commit as `head_sha`.
- The next push to `main` delivers its event normally; if not, the new manual trigger recovers it.

## Open Questions
None.

## Design
**Recovery.** `ci.yml` gains `workflow_dispatch`. `Get-AutoDeployCiConclusion` drops the `event=push` query filter, requests up to 10 runs for the commit on the branch, and keeps only `push` and `workflow_dispatch` events before taking the newest run. Pull-request runs never count, because they test a merge preview, not the commit itself.

**Watch stall alert.** `Test-DeploymentLag` reads `main`'s commit time and applies the same event filter. It fails "no passing CI run" when there is no run, or the newest run is unfinished, and the commit is older than the threshold. A completed failed run passes the check, with a detail saying auto-deploy refuses it.

**Token install.** `Install-AutoDeployGitHubToken` asserts elevation first through a new `Assert-AutoDeployAdministrator`, matching the module-local pattern. Its `$Config` defaults to `$null` and is read after that check, because a default-value expression runs during parameter binding, before any check in the body. An empty token file is normalized to an empty string, so the existing shape check reports "does not contain a GitHub token". `Read-AutoDeployGitHubToken` gets the same normalization.

| Alternative | Why not |
|---|---|
| Keep `event=push` and recover by pushing an empty commit | `main` requires a PR, so every dropped event would cost a PR |
| Elevation check in `prod.ps1` only | Direct module callers would still hit the null error |

## Expected Changes

| File or area | Change |
|---|---|
| `.github/workflows/ci.yml` | `workflow_dispatch` trigger |
| `GitHubAutomationConfigurationTest.java` | CI trigger contract |
| `ops/production/windows/modules/Production.AutoDeploy.psm1` | Event filter, `Assert-AutoDeployAdministrator`, empty-file normalization, deferred config read |
| `ops/production/windows/tests/Production.AutoDeploy.Tests.ps1` | Event-filter, elevation and empty-file tests |
| `.github/scripts/Test-ProductionSite.ps1` and its tests | Stall alert and event filter |
| `README.md`, `docs/operations/windows-production.md` | Manual CI re-run and elevation notes |

## Task Breakdown

### Task 1 - Recover and report missed CI runs
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `.github/workflows/ci.yml`, `GitHubAutomationConfigurationTest.java`, `Production.AutoDeploy.psm1`, `Production.AutoDeploy.Tests.ps1`, `.github/scripts/Test-ProductionSite.ps1`, `.github/scripts/tests/Test-ProductionSite.Tests.ps1`, `README.md`, `docs/operations/windows-production.md` |
| **Symbols** | `on.workflow_dispatch`; `Get-AutoDeployCiConclusion`; `Test-DeploymentLag`; new contract test `ciCanBeRerunByHandForAMissedPush` |
| **Inspection** | Files read at `06c3718` |
| **Behavior** | A manual CI run on `main` unblocks the gate; Production Watch alerts when `main` has no passing run 45 minutes after its commit |
| **Invariants** | Pull-request runs never satisfy the gate; red CI still blocks; the existing lag rule is unchanged |
| **Boundary/API** | New manual trigger in the Actions tab; status values unchanged |
| **Effects and failures** | Read-only API calls; one extra field read per watch run |
| **Tests and evidence** | New Pester and contract tests fail before the change |
| **Verification** | `automationPester`, the contract test, full `gradlew.bat build` |

### Task 2 - Clear token install failures
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `Production.AutoDeploy.psm1`, `Production.AutoDeploy.Tests.ps1`, `docs/operations/windows-production.md` |
| **Symbols** | `Install-AutoDeployGitHubToken`, `Read-AutoDeployGitHubToken`, new `Assert-AutoDeployAdministrator` |
| **Inspection** | `Production.AutoDeploy.psm1:340-375` at `06c3718`; `Assert-Administrator` in `Production.Install.psm1` |
| **Behavior** | Non-elevated install fails with "requires elevated PowerShell"; an empty or whitespace-only file fails with "does not contain a GitHub token" |
| **Invariants** | Verification still precedes storage; the token never appears in messages |
| **Boundary/API** | `-Config` stays optional; callers that pass it are unchanged |
| **Effects and failures** | No new effects |
| **Tests and evidence** | Empty-file regression fails before the change; elevation test |
| **Verification** | `automationPester`; `Production.Command.Tests.ps1` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | `GitHubAutomationConfigurationTest` | `workflow_dispatch` of CI on `main` after merge, if the push event is missed again |
| AC-2 | AutoDeploy Pester event-filter cases | Read-only `Get-AutoDeployCiConclusion` against GitHub for `a9d2058` returns SUCCESS |
| AC-3 | Watch Pester stall cases | Read-only watch verdict against production now reports the `06c3718` stall |
| AC-4 | AutoDeploy Pester elevation and empty-file cases | Non-elevated `prod.cmd github-token-install` with an empty file prints the elevation message |
| AC-5 | Full `gradlew.bat build` | verify-local-app candidate run with `/actuator/info` and readiness; post-merge production readback |

- **Regressions:** the full AutoDeploy and watch suites; the earlier lag cases.

## Rollback or Recovery
Revert the merge through a PR. Without the event change, a missed push again needs a new commit.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The next push event is also dropped | Low | Manual CI trigger after merge |
| A stall alert fires during a normal deploy | Low | 45-minute threshold matches the lag rule; normal CI plus deploy takes about 20 minutes |

## Implementation Log

### 2026-10-05 - Production Watch was never registered

- **Change:** Added a third PR, `claude/register-production-watch-20261005` at `0e2bf8a`, which adds an explanatory comment to `.github/workflows/production-watch.yml`.
- **Reason:** After #1482 deployed (`ca98b1e`), `gh workflow run production-watch.yml` returned HTTP 404 and `/actions/workflows` omitted the file. GitHub indexes schedule- and dispatch-only workflows only from a main push that changes them, and the push that added this one (`06c3718`) was dropped.
- **Impact:** Expected Changes gains `production-watch.yml`. AC-3's live check passes against production, but a scheduled or manual run still waits on this merge.

### 2026-10-05 - Renormalize gradlew.bat for clean checkouts

- **Change:** The registration PR also renormalizes `gradlew.bat` (`git add --renormalize`), committed as `e0728a8`.
- **Reason:** The spoke preflight refused `0e2bf8a` because `gradlew.bat` showed as modified in a fresh worktree. The `main` blob was CRLF (`i/crlf`) while `.gitattributes` declares `text eol=crlf`, so every checkout reported a phantom line-ending change; the user's main checkout shows the same `M gradlew.bat`. Ignoring CRs, the content is identical.
- **Impact:** Expected Changes gains `gradlew.bat` (line endings only). Wrapper builds rerun green with a clean tree.

## Outcome

> [!TIP]
> Missed CI runs can now be recovered by hand and are reported. The token install explains its failures. Production Watch is registered and passing, and production serves `ca98b1e` after a gated deploy.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | `ci.yml` `workflow_dispatch` merged in #1482 (`ca98b1e`), enforced by `GitHubAutomationConfigurationTest.ciCanBeRerunByHandForAMissedPush`. |
| AC-2 | ✅ Met | Pester event-filter cases, including a manual run recovering a missed push and pull request runs never counting. Live, the gate returned SUCCESS for `a9d2058` and PENDING for `06c3718` ([report](../test-reports/2026-10-05-10-22-christopherbell-dev-recover-missed-ci-runs-and-clarify-token-install-failures.md)). |
| AC-3 | ✅ Met | Pester stall cases; the live verdict flagged the `06c3718` stall. Production Watch registered by #1483 (`4663692`); manual run [37339944271](https://github.com/azurras/christopherbell.dev/actions/runs/37339944271) passed with no alert ([report](../test-reports/2026-10-05-10-57-christopherbell-dev-register-the-production-watch-workflow.md)). |
| AC-4 | ✅ Met | Pester elevation and empty-file cases. A real non-elevated `prod.cmd github-token-install` printed "requires elevated PowerShell…" with exit 1. |
| AC-5 | ✅ Met | #1482 merged as `ca98b1e` with required checks green; its push event arrived, CI passed at 15:47 UTC, and the gate deployed at 15:49. Production `/actuator/info` reports `ca98b1e`, `auto-status` reads `SUCCEEDED`, and GitHub deployment 6863501513 shows `success`. #1483 merged as `4663692` and was at `AWAITING_CI` for its `main` run at closure. |

- **Shipped versus planned:** as planned, plus the workflow registration and the `gradlew.bat` renormalization logged above.
- **Follow-ups:** none required. `4663692` changes only a workflow comment and line endings and deploys when its CI passes.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
