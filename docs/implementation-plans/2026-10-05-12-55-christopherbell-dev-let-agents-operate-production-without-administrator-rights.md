# Let Agents Operate christopherbell.dev Without Administrator Rights

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> A non-administrator agent can observe production and run allowlisted operations end to end by merging a request to `main`. The SYSTEM poller validates and runs each request and publishes its result, and the GitHub deployment token warns before it expires. Bootstrap and secret handling stay with the user.

## Background
After the [CI/CD hardening](2026-10-05-08-52-christopherbell-dev-harden-ci-cd-robustness-and-observability.md) and [follow-up](2026-10-05-10-11-christopherbell-dev-recover-missed-ci-runs-and-clarify-token-install-failures.md) shipped, the user asked what an agent needs to do all DevOps work end to end without an admin user, then asked to "fix all of these problems". Releases already flow from merge to deploy without admin. During that work a non-admin agent was blocked as follows:

1. `config\deploy.json`, the token and `logs\application.json.log` are readable only by SYSTEM and Administrators.
2. `auto-status` reported `pollerState: UNKNOWN` (`ACCESS_DENIED`), because a standard user cannot query the SYSTEM task.
3. `restart`, `rollback`, `backup`, `verify-startup` and `deploy` require an elevated prompt.
4. The fine-grained deployment token expires, and nothing warns before it does.

The user chose the safe set plus guarded rollback for agent requests, and chose to keep the token with an expiry alert rather than adopt a GitHub App.

## Goals
- The SYSTEM poller publishes a sanitized diagnostics record that standard users read through `prod.cmd diagnostics`: scheduler state, services, releases, redacted recent log lines, request results and token expiry. `auto-status` uses the published scheduler state when a direct query is denied (AC-1, AC-2).
- A JSON request under `ops/requests/` merged to `main` runs exactly once after its commit passes CI. Allowed actions are `restart`, `backup`, `verify-startup`, `redeploy` and `rollback`. A commit that only adds requests never triggers a deploy, and a rollback holds the rolled-away commit until `main` moves (AC-3, AC-4, AC-5).
- Request files are validated in CI before merge (AC-6).
- The token's expiry is captured at install and on each authenticated call. Production Watch fails when it is within 14 days (AC-7).
- Documentation separates agent-operable work from one-time administrator bootstrap (AC-8).
- Verified, merged and observed in production: one real request runs end to end (AC-9).

## Non-Goals

| Not doing | Why |
|---|---|
| GitHub App authentication | The user chose to keep the token with an expiry alert |
| Agent access to `config` or raw logs | Secrets stay protected; diagnostics publish a redacted view |
| Destructive data actions (restores, Mongo consolidation, migration-aware rollback) | Data loss risk; these keep their explicit human confirmations |
| Remote (off-host) diagnostics | Production Watch already covers external health; diagnostics serve operators on the host |
| Automating bootstrap (`install`, `auto-install`, sensor driver, tunnel token, token creation) | One-time administrator tasks that handle secrets or drivers |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Each poll writes `diagnostics.json` to the status store (protected writer, standard-user readable, size-bounded) with scheduler state, service states, releases, redacted log lines, recent request results and token expiry; Pester proves that secrets, emails and connection-string credentials are masked |
| AC-2 | `prod.cmd diagnostics` runs non-elevated and returns the record. `auto-status` reports the poller's published scheduler state instead of `UNKNOWN` when its own query is denied |
| AC-3 | Pester proves each request is validated (schema, id equals filename, `requestedAt` within 24 hours and not in the future, `expectedActiveSha` for rollback), runs once, and is recorded as SUCCEEDED, FAILED, REJECTED or EXPIRED. A fresh host records old requests as EXPIRED without running them |
| AC-4 | Pester proves a commit whose only changes are under `ops/requests/` does not deploy, and its requests run once it passes CI; Production Watch treats a live commit that differs from `main` only under `ops/requests/` as current |
| AC-5 | Pester proves a successful rollback holds the rolled-away `main` commit (`HELD`) until `main` moves, while a new commit deploys normally. Rollback and redeploy are recorded as GitHub `Production` deployments |
| AC-6 | A CI-run Pester test validates every file under `ops/requests/` against the schema |
| AC-7 | Pester proves the expiry header is parsed and published (deployment payload and diagnostics), that Production Watch fails within 14 days of expiry, and that `github-token-install` prints the expiry |
| AC-8 | README and runbook document the request format, the actions, diagnostics, and the remaining admin bootstrap steps |
| AC-9 | Runtime report published; PR merged with required checks green; production deploys it; a merged `verify-startup` request shows SUCCEEDED in `prod.cmd diagnostics` from a non-elevated shell, without deploying |

## Inputs
- **Request:** the user's question about agent DevOps without an admin user, then "Let's fix all of these problems."
- **User decisions:** safe set plus guarded rollback; keep the token and add an expiry alert.
- **Inspected:** spoke `origin/main` `4663692`:
  - `Production.AutoDeploy.psm1`: state, status store, `Invoke-AutoDeployOnce`, `Get-AutoDeployTaskSchedulerEntry`, `Get-AutoDeployStatus` and the GitHub helpers.
  - `Production.Operations.psm1`: `Restart-ProductionService`, `Invoke-ProductionRollback`, `Get-ProductionReleases`, `Test-ProductionStartup` and `Watch-ProductionLogs`.
  - `New-ProductionBackup` and `Read-ProductionConfig` in `Production.Common.psm1`; `Invoke-ProductionDeploy` and `Resolve-OriginMainRelease` in `Production.Deploy.psm1`.
  - `prod.ps1`, `.github/scripts/Test-ProductionSite.ps1`, `website/build.gradle.kts` (`automationPester`), README and the runbook.
- **Observed:** non-admin access denials on `deploy.json` and `application.json.log`; `pollerState: UNKNOWN` with reason `ACCESS_DENIED`.

## Branch
`claude/agent-operations-20261005` from `origin/main` `4663692`, in the worktree `christopherbell.dev-worktrees/agent-operations-20261005`.

## Assumptions
- Restart, rollback and deploy take the deploy lock themselves, and the poller holds no lock when it handles requests.
- GitHub returns `github-authentication-token-expiration` (for example `2026-11-04 15:00:00 UTC` or `… -0500`) on calls made with a fine-grained token.
- Reading the last 400 lines of `application.json.log` each minute is cheap.

## Open Questions
None.

## Design
**Diagnostics.** At the end of every poll, including failed ones and on a best-effort basis, `Publish-AutoDeployDiagnostics` writes `diagnostics.json` beside `auto-deploy.json`. It uses the same protected status directory and atomic write, with a 512 KiB limit. The record carries:

- `schemaVersion: 1` and `generatedAt`;
- `scheduler`: the task's state as seen by SYSTEM;
- `services`: the status and start type of `ChristopherBellDev`, `MongoDB` and `cloudflared`;
- `releases`: sha, builtAt, and current/previous flags;
- `recentLogEntries`: at most 100 entries from `application.json.log`, with only timestamp, level, logger, `requestId`, a 400-character message and the first line of the error type and message, all redacted;
- `opsRequests`: the last 20 results;
- `githubTokenExpiresAt`.

Redaction masks `github_pat_…` and `gh[opsu]_…` tokens, `Bearer …` values, JWTs, credentials inside `mongodb(+srv)://user:pass@`, `password=` and `secret=` values, and email addresses. `prod.cmd diagnostics` validates and prints the record. `Get-AutoDeployStatus` falls back to the record's scheduler state when its own query returns `ACCESS_DENIED`.

**Requests.** Files live at `ops/requests/<id>.json`:

```json
{ "id": "2026-10-05-verify-startup", "action": "verify-startup", "reason": "...", "requestedAt": "2026-10-05T18:00:00Z", "expectedActiveSha": "<40 hex, required for rollback>" }
```

The poller handles requests only when the `main` tip has passed CI and needs no deploy: either active equals remote, remote is held, or remote differs from active only under `ops/requests/`. It lists files with `git ls-tree` at the remote commit and reads them with `git show`, through the trusted Git helper after the existing fetch. It runs at most one unprocessed request per poll, oldest `requestedAt` first.

Validation rejects schema errors and an id that does not match its filename. A request first seen more than 24 hours after `requestedAt`, or more than 5 minutes in the future, is recorded as EXPIRED and never run, so a fresh host replays nothing. Processed ids live in state (bounded to the last 200) with their outcome.

The actions map as follows:

| Action | Runs |
|---|---|
| `restart` | `Restart-ProductionService -Verify` |
| `backup` | `New-ProductionBackup` |
| `verify-startup` | `Test-ProductionStartup` |
| `redeploy` | `Invoke-ProductionDeploy -Automatic`, recorded as a GitHub deployment |
| `rollback` | Requires `expectedActiveSha` equal to the active release, then `Invoke-ProductionRollback` behind its existing schema guards; recorded as a GitHub deployment of the restored commit |

A successful rollback stores `heldRemoteSha` equal to the current remote. `Invoke-AutoDeployOnce` reports `HELD` and does not deploy while remote equals `heldRemoteSha`, and clears the hold when remote moves. Ops-only commits are detected with `git diff --name-only <active> <remote>`; a commit whose every path is under `ops/requests/` is acknowledged as `opsOnlyAcknowledgedSha` and not deployed. Production Watch's lag check uses GitHub's compare API (`/compare/<live>...<main>`) and treats a request-only difference as live.

**Token expiry.** `Invoke-AutoDeployGitHubApi` captures the expiry header from authenticated responses in a script-scoped value. The poller copies it into state (`githubTokenExpiresAt`), diagnostics and each new deployment's `payload`. `github-token-install` prints the parsed expiry. Production Watch reads the latest `Production` deployment's `payload.tokenExpiresAt` and fails when it is within 14 days.

| Alternative | Why not |
|---|---|
| Request queue folder writable by an operators group | Needs ACL changes on the host and creates a second trust path beside `main`; PRs give audit, review and required checks for free |
| Rollback switching to any retained release | Bypasses the existing two-junction rollback guards; previous-release rollback behind holds is enough |
| Deploying request-only commits | Would replace `previous` with the bad release and defeat rollback |
| Running the agent elevated | Unrestricted control of the production machine |

## Expected Changes

| File or area | Change |
|---|---|
| `ops/production/windows/modules/Production.AutoDeploy.psm1` | Diagnostics publisher, request reader, validator and runner, hold and ops-only logic, token-expiry capture, status fallback, new outcomes `HELD` and `OPS_REQUEST` |
| `ops/production/windows/prod.ps1`, `Production.Common.psm1` (help) | `diagnostics` command |
| `ops/production/windows/tests/Production.AutoDeploy.Tests.ps1` | Tests for AC-1 through AC-5 and AC-7 |
| `ops/production/windows/tests/Production.OpsRequests.Tests.ps1` (new) | Validates repository request files (AC-6) |
| `ops/requests/README.md` (new) | Request format |
| `website/build.gradle.kts` | Adds the new Pester file to `automationPester` |
| `.github/scripts/Test-ProductionSite.ps1` and its tests | Token-expiry check; request-only difference treated as live |
| `ops/production/windows/tests/Production.Command.Tests.ps1` | Routes `diagnostics` |
| `README.md`, `docs/operations/windows-production.md` | Delegated operations and bootstrap sections |

## Task Breakdown

### Task 1 - Publish sanitized diagnostics
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `Production.AutoDeploy.psm1`, `prod.ps1`, `Production.Common.psm1`, `Production.AutoDeploy.Tests.ps1`, `Production.Command.Tests.ps1` |
| **Symbols** | New `Publish-AutoDeployDiagnostics`, `Get-AutoDeployDiagnostics`, `ConvertTo-AutoDeployRedactedText`, `Read-AutoDeployRecentLogEntries`; changed `Assert-AutoDeployStatusFile` (size limit parameter), `Get-AutoDeployStatus` (scheduler fallback), `Start-AutoDeployLoop` (publishes in `finally`) |
| **Inspection** | Status store functions and `Get-AutoDeployTaskSchedulerEntry` at `4663692` |
| **Behavior** | Standard users read current production diagnostics without access to `config` or raw logs |
| **Invariants** | No secret, email or credential text in the record; the record never blocks or fails a deploy; existing status record unchanged |
| **Boundary/API** | New `prod.cmd diagnostics`; `auto-status` gains no fields |
| **Effects and failures** | One bounded write per poll; read or format failures are warned once and skipped |
| **Tests and evidence** | Redaction cases; size bound; publish and read round trip; scheduler fallback |
| **Verification** | Pester; non-elevated `prod.cmd diagnostics` after deploy |

### Task 2 - Run requests merged to main
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 (results appear in diagnostics) |
| **Files** | `Production.AutoDeploy.psm1`, `Production.AutoDeploy.Tests.ps1`, new `ops/requests/README.md`, new `Production.OpsRequests.Tests.ps1`, `website/build.gradle.kts`, `.github/scripts/Test-ProductionSite.ps1` and its tests (ops-only lag) |
| **Symbols** | New `Get-AutoDeployOpsRequests`, `Test-AutoDeployOpsRequestDocument`, `Invoke-AutoDeployOpsRequest`, `Test-AutoDeployOpsOnlyChange`; state `processedOpsRequests`, `heldRemoteSha`, `opsOnlyAcknowledgedSha`; outcomes `HELD` and `OPS_REQUEST` |
| **Inspection** | `Invoke-AutoDeployOnce` flow and the operations functions at `4663692` |
| **Behavior** | Each valid request runs once after CI; request-only commits never deploy; rollback holds |
| **Invariants** | CI gate unchanged; recovery still runs first; destructive data actions unavailable; one request per poll; each operation keeps its own lock and guards |
| **Boundary/API** | Repository contract `ops/requests/*.json` |
| **Effects and failures** | Restart, rollback, deploy and backup effects as their commands; failures recorded and not retried; GitHub records best effort |
| **Tests and evidence** | Validation matrix, run-once, expiry on a fresh host, ops-only no-deploy, hold and release, rollback guard on stale `expectedActiveSha` |
| **Verification** | Pester; production `verify-startup` request after merge |

### Task 3 - Warn before the token expires
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 |
| **Files** | `Production.AutoDeploy.psm1`, `Production.AutoDeploy.Tests.ps1`, `.github/scripts/Test-ProductionSite.ps1`, its tests |
| **Symbols** | New `ConvertFrom-AutoDeployTokenExpirationHeader`; changed `Invoke-AutoDeployGitHubApi`, `Start-AutoDeployGitHubDeployment` (payload), `Install-AutoDeployGitHubToken` (prints expiry), `Test-LatestProductionDeployment` |
| **Inspection** | GitHub helpers and watch deployment check at `4663692` |
| **Behavior** | Expiry becomes visible in diagnostics and deployment payloads; the watch alerts 14 days ahead |
| **Invariants** | Token text never stored outside its file or logged |
| **Boundary/API** | Deployment payload gains `tokenExpiresAt` |
| **Effects and failures** | An unparseable header is ignored with one warning |
| **Tests and evidence** | Header formats; watch threshold cases |
| **Verification** | Pester; the next deployment's payload in production |

### Task 4 - Document delegated operations
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1 through 3 |
| **Files** | `README.md`, `docs/operations/windows-production.md`, `ops/requests/README.md` |
| **Symbols** | Sections "Delegated Operations" and "Administrator Bootstrap" |
| **Inspection** | README Production and Repository Automation sections; runbook Application Releases |
| **Behavior** | Readers can tell what an agent can do and what needs an administrator |
| **Invariants** | Existing runbook contracts that `Production.Command.Tests.ps1` asserts still hold |
| **Boundary/API** | Documentation only |
| **Effects and failures** | None |
| **Tests and evidence** | `Production.Command.Tests.ps1` |
| **Verification** | Pester; link check by reading |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Redaction and diagnostics Pester | Publish to a scratch status root from a live `application.json.log`-shaped file |
| AC-2 | Command routing and status fallback Pester | Non-elevated `prod.cmd diagnostics` against production after deploy |
| AC-3 | Request validation and run-once Pester | Repository request validated by the CI Pester test |
| AC-4 | Ops-only Pester | After merge, the request commit does not deploy (active stays put, `auto-status` UP_TO_DATE) |
| AC-5 | Hold, rollback and deployment-record Pester | Not exercised in production; a rollback is a real outage-response action |
| AC-6 | `Production.OpsRequests.Tests.ps1` in `automationPester` | CI on the request PR |
| AC-7 | Header parse and watch threshold Pester | Production deployment payload carries `tokenExpiresAt` after the deploy |
| AC-8 | Command tests over the runbook | Reading |
| AC-9 | Full `gradlew.bat build` | verify-local-app candidate run; production `verify-startup` request read back through `prod.cmd diagnostics` |

- **Regressions:** the full AutoDeploy, Command and watch suites.
- **Edge cases:** clock skew, duplicate ids, non-JSON files under `ops/requests/`, a request removed before it runs, a failed rollback (no hold), and an unreadable log file.

## Rollback or Recovery
1. Revert through a PR; the poller deploys the revert.
2. To clear a hold, merge any non-request change to `main`.
3. To skip a request, delete its file before merge, or let it expire (24 hours).
4. Diagnostics can be removed by deleting `diagnostics.json`; the next poll recreates it.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A redaction pattern misses a secret format | Low | Structured log fields only, length caps and conservative patterns; config and secrets are never read into diagnostics |
| An agent merges a harmful request | Low | Allowlist of non-destructive actions; required checks and PR review; rollback guarded by `expectedActiveSha` and schema checks |
| A hold leaves production behind `main` | Medium | `HELD` shows in `auto-status`, and Production Watch lag alerts after 45 minutes; any new commit clears it |
| The ops-only diff misclassifies a commit | Low | Paths must all start with `ops/requests/`; anything else deploys normally |
| The expiry header is absent or in a new format | Medium | Tolerant parse; absence leaves the watch check passing with a detail |

## Implementation Log

### 2026-10-05 - Tests followed implementation

- **Change:** Implementation was written before its Pester tests rather than test-first. The first test run still failed on three real defects:
  - `$script:autoDeployGitHubTokenExpiresAt` was uninitialized under strict mode, which broke deployment records.
  - The request-only detection test exercised a Describe-level mock instead of the function; it was moved to its own Describe.
  - Production Watch read deployment payloads through an array nested by `@()`, which hid them; the result is now flattened.
  The final suites pass: AutoDeploy 148, watch, request and command 49, full build 3,256 with 0 failures.
- **Reason:** Order of work; the defects were real and are fixed.
- **Impact:** Evidence order for Tasks 1-3; ACs unchanged.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
