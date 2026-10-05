# Harden christopherbell.dev CI/CD Robustness and Observability

## Document Status
complete

## Objective

> [!IMPORTANT]
> Red or untested code cannot reach `main` or production. Transient CI dependencies no longer fail builds. Deploy outcomes, test results and production availability show up in GitHub without anyone logging into the host.

## Background
On 2026-10-05 the user asked for a review of the christopherbell.dev CI/CD process for robustness and observability, then asked to fix all ten findings. The inspection of `origin/main` `b126b642`, 60 workflow runs and the `main` ruleset found:

1. The `main` ruleset requires a pull request, linear history and no force-push or deletion, but no status checks, so a red PR can merge.
2. The auto-deploy poller deploys and refreshes its own SYSTEM-run tools from the `origin/main` tip without consulting CI. `695a3ed8` failed CI on `main` on 2026-10-05 and was still deployable.
3. `Install-Module Pester` fails intermittently on PowerShell Gallery outages ("No match was found ... 'Pester'"); that failure turned `main` red on 2026-10-05 for an unchanged tree.
4. Every grouped Dependabot Gradle PR fails dependency verification because Dependabot never updates `gradle/verification-metadata.xml` (run 37301196194: `byte-buddy-1.18.14.pom` failed verification).
5. CI duration roughly doubled in two weeks (4–5 minutes to 8–11), with nothing reporting test counts or durations.
6. Deploy outcomes are written only to a protected JSON file on the production host.
7. Test results are uploaded only when CI fails, and about 110 skipped tests are invisible.
8. Nothing outside the single production host checks that the site is up; the in-app site monitor (#1474) runs inside the app it would need to detect.
9. Only `health` is exposed; nothing public shows which commit is live.
10. Logs are plain text with no request correlation.

Planning also found that CI runs only the shared-folder, install and operations Pester suites. `Production.AutoDeploy.Tests.ps1`, the suite for the code this change edits most, never runs in CI.

## Goals
- Merging to `main` requires the CI, CodeQL and dependency-review checks on a branch that is current with `main` (AC-1).
- Automatic deployment and the tool refresh act only on a commit whose `CI Build` push run succeeded, and report waiting or rejection in `auto-status` (AC-2).
- The Pester installation survives a PowerShell Gallery outage on a cache hit and retries transient misses (AC-3).
- A Dependabot Gradle PR that fails verification gets a regenerated, reviewable verification-metadata file and instructions (AC-4).
- Every CI run publishes test counts, skips, failures and the slowest suites to its job summary, and the auto-deploy Pester suite runs in CI (AC-5).
- Each automatic deploy attempt is recorded as a GitHub deployment in the existing `Production` environment once the user installs a token, and runs exactly as before without one (AC-6).
- A scheduled GitHub workflow detects site outages, failed deployments and stalled deploys, opens or updates one alert issue, and closes it on recovery (AC-7).
- `/actuator/info` publicly reports the running build version, which encodes the commit (AC-8).
- Production writes JSON (ECS) file logs, and every request carries a validated `X-Request-Id` through logs and response headers (AC-9).
- The change is verified locally, merged and deployed by the supported auto-deploy, and its runtime behavior is read back in production (AC-10).

## Non-Goals

| Not doing | Why |
|---|---|
| Restoring Ubuntu/macOS CI | The user chose Windows-only CI in #1479 the same day |
| Committing regenerated verification metadata automatically | That would trust whatever was downloaded; a person must review checksum changes |
| Prometheus/OpenTelemetry metrics or tracing backends | Needs hosting decisions the user has not made; request IDs and JSON logs give correlation now |
| Gradle build scans | Publishes build data to a third-party service |
| Creating the GitHub token | Only the user can create and handle the token; this change supplies the loader, install command and docs |
| CI gating for interactive `prod.cmd deploy` | An operator running deploy by hand is making an explicit decision; the gate covers the unattended path |
| Changing the WinSW console log the Mission Control log viewer reads | JSON there would degrade the in-app viewer; the JSON log is a separate file |
| Reworking the forward-only cutover or rollback semantics | Outside the findings; documented behavior stays |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | The `main` ruleset readback shows a `required_status_checks` rule with `build`, `Analyze (java-kotlin)`, `Analyze (javascript-typescript)`, `Analyze (actions)` and `dependency-review`, strict policy on, and the original four rules unchanged |
| AC-2 | Pester tests prove auto-deploy and tool refresh do not deploy or switch for pending, missing or failed CI, deploy for success, and publish `AWAITING_CI`/`CI_FAILED`; existing auto-deploy tests still pass |
| AC-3 | CI restores Pester 5.9.0 from an `actions/cache` keyed on the version and installs only on a miss, with bounded retries; the workflow contract test enforces both |
| AC-4 | A Dependabot-only workflow regenerates verification metadata on a failing Dependabot Gradle PR, uploads it as an artifact and writes apply instructions to the job summary, using a read-only token |
| AC-5 | A tested script writes a JUnit/NUnit summary (passed, failed, skipped, slowest suites) to the CI job summary on every run, and a Gradle Pester task runs the auto-deploy and CI-script suites in `build` on Windows |
| AC-6 | Pester tests prove a deploy attempt creates a `Production` deployment with `in_progress`, then `success` or `failure`; missing, rejected or failing GitHub calls never change the deploy result or leak the token; `github-token-install` stores the token in a protected file |
| AC-7 | `production-watch.yml` runs every 15 minutes and on demand; its tested script detects an unhealthy route, a failed latest Production deployment, and a live commit lagging a CI-green `main` by more than 45 minutes; it opens or comments on one `production-alert` issue and closes it on recovery |
| AC-8 | Unauthenticated `GET /actuator/info` returns 200 with `build.version` and no environment or detail data; protected actuator routes are unchanged |
| AC-9 | With the prod profile, logs go to a rolling ECS JSON file; requests get a valid `X-Request-Id` (echoed if well formed, generated otherwise) on the response and in log MDC, cleared after the request |
| AC-10 | Local runtime report published; PR merged with all required checks green; auto-deploy reaches `SUCCEEDED` (or `AWAITING_CI` then `SUCCEEDED`) for the merge; production `/actuator/info` reports the merge commit; Production Watch passes on a manual run |

## Inputs
- **Request:** 2026-10-05 inspection-only review, then "Let's fix all of these issues."
- **User decision:** Report deploys through GitHub Deployments with a user-provisioned token (chosen over Resend email).
- **Inspected:** spoke `christopherbell-dev` at `origin/main` `a9d20589`: `.github/workflows/{ci,codeql,dependency-review,stale}.yml`, `.github/dependabot.yml`, `GitHubAutomationConfigurationTest`, `website/build.gradle.kts` (Pester tasks, `buildInfo()`), `application.yml`, `application-prod.yml`, `SecurityConfig` (`PUBLIC_URLS`), `VersionedStaticAssetCacheFilter`, `DatabaseHealthHttpSecurityIntegrationTest`, `Production.AutoDeploy.psm1` (state, status store, `Invoke-AutoDeployOnce`, `Update-AutoDeployToolsFromOriginMain`, `Start-AutoDeployLoop`), `Production.Common.psm1` (`Read-ProductionConfig`, `Invoke-ProductionWebRequest`, protected-path helpers, `Show-ProductionHelp`), `Production.Install.psm1` (`CloudflareTokenPath` handling), `Production.Deploy.psm1` (`New-ReleaseFromOriginMain`, smoke paths), `prod.ps1`, `prod.cmd`, `Makefile`, `README.md`, `AGENTS.md`, `Production.AutoDeploy.Tests.ps1`.
- **GitHub state:** ruleset `main` (four rules, no bypass actors); environment `Production` exists; repository is public; latest `actions/cache` is v6.1.0 `55cc8345863c7cc4c66a329aec7e433d2d1c52a9`.
- **Memory:** [2026-10-05](../session-memory/2026-10-05.md) Windows-only CI delivery; [2026-10-04](../session-memory/2026-10-04.md).

## Branch
`claude/cicd-hardening-20261005` from `origin/main` `a9d20589`, in the linked worktree `christopherbell.dev-worktrees/cicd-hardening-20261005`.

## Assumptions
- The CI job, CodeQL matrix and dependency-review check names stay `build`, `Analyze (<language>)` and `dependency-review`; they are verified on this PR's checks before the ruleset changes.
- GitHub's REST API reports workflow runs by `head_sha` for the public repository without authentication, at 60 requests per hour per IP.
- Cloudflare does not challenge GitHub-hosted runner requests to the public site; the first manual Production Watch run proves this.
- The production service account can create files in `C:\ProgramData\christopherbell.dev\logs`, where WinSW already writes its logs; Logback reports but survives a file it cannot open.
- Production builds without `releaseVersion`, so `build.version` is `0.0.0-dev.<40-hex commit>`.

## Open Questions
- **User:** create the fine-grained token (this repository only; Deployments read/write, Actions read) and run `prod.cmd github-token-install`. Until then AC-6's live readback is not possible; the code path ships disabled and is proven by tests.

## Design
**CI gate (AC-2).** A new `Get-AutoDeployCiConclusion` asks GitHub for the `ci.yml` runs on the commit (`head_sha`, `event=push`, `branch=<config branch>`) and returns `SUCCESS`, `PENDING` (queued, in progress or not yet registered) or `FAILED` (any other completed conclusion), using the newest run. The repository slug comes from the configured remote URL through the trusted Git helper, with no new config key. `Invoke-AutoDeployOnce` checks it after recovery and the remote/active comparison and before backoff and deploy. On `PENDING` it publishes `AWAITING_CI` and returns. On `FAILED` it publishes `CI_FAILED` and caches the verdict in state for `autoDeployFailureBackoffSeconds`, so a failed commit costs four calls an hour. An API failure is a `CHECK_FAILED` with the new category `CI_CHECK`. A pending recovery failure is still rethrown, as in the existing up-to-date branch. `Update-AutoDeployToolsFromOriginMain` applies the same verdict to the resolved SHA and keeps the current tools unless it is `SUCCESS`. A host without tools still fails closed. The new outcomes and categories are added to every status allow-list and the message map. Reads use the token when one is installed and fall back to anonymous with one warning on 401 or 403.

**GitHub Deployments (AC-6).** The token lives in `config\github-deployments.token` under the protected program-data root and is checked with `Assert-ProtectedProductionPath`. `github-token-install -GitHubTokenPath <file>` validates the token's shape, writes the protected copy and tells the operator to delete the source, mirroring `CloudflareTokenPath`. Best-effort helpers create the deployment (`environment: Production`, `auto_merge: false`, `required_contexts: []`, because the gate already checked CI), post `in_progress` after `DEPLOYING`, then `success` with `environment_url` or `failure` with the 140-character safe failure detail. Every helper swallows its own failures behind one sanitized warning, and the token never enters messages, state or status. `Invoke-ProductionWebRequest` gains an optional `-Headers` parameter; existing callers are unchanged.

**Production Watch (AC-7).** Script `.github/scripts/Test-ProductionSite.ps1` probes readiness, `/`, `/blog` and `/actuator/info` on the canonical host, retrying each up to three times 10 seconds apart. It reads the latest `Production` deployment status, `main`'s head and its `CI Build` result. It flags lag when `main` has been CI-green for over 45 minutes and the live commit differs. It returns a structured result; the workflow (`issues: write`, `contents: read`, `actions: read`, `deployments: read`) opens or comments on the single open `production-alert` issue, and comments and closes it when healthy. Issue notifications cover the GitHub deployment-failure alerting gap.

**Pester resilience (AC-3).** An `actions/cache` step caches `~/Documents/PowerShell/Modules/Pester/5.9.0`, keyed `pester-5.9.0-${{ runner.os }}`. The install step skips when the cached module imports at the exact version. Otherwise it tries `Install-Module` up to three times with 15 and 45 second waits, then keeps the existing exact-version assertion.

**Test visibility (AC-5).** `.github/scripts/Write-TestSummary.ps1` parses `**/build/test-results/**/*.xml` (JUnit and Pester NUnit) into a Markdown table of totals and the 10 slowest suites, appended to `$GITHUB_STEP_SUMMARY` by an `if: always()` step. A new `automationPester` Gradle task runs `Production.AutoDeploy.Tests.ps1` and `.github/scripts/tests/*.Tests.ps1` under PowerShell 7 with NUnit output, joining `windowsPesterVerification`.

**Dependabot metadata (AC-4).** `dependency-verification.yml` runs on `pull_request` only when `github.actor == 'dependabot[bot]'` and Gradle files changed, with `contents: read`. On `windows-latest` it runs `gradlew.bat --write-verification-metadata sha256 --continue build`, so detached configurations (the failing `detachedConfiguration87`) and Windows-only tasks resolve exactly as in CI. If the file changed, it uploads it as an artifact and writes the diff summary and `gh run download` apply steps.

**App (AC-8, AC-9).** Expose `health,info`, add `GET:/actuator/info` to `PUBLIC_URLS`, and explicitly disable the env, java, os and process info contributors so only `build` and `git` data shows. A new `RequestCorrelationFilter` in `configuration.filter`, ordered highest precedence, accepts `X-Request-Id` matching `[A-Za-z0-9._-]{8,64}` or generates a UUID. It sets the MDC key `requestId` and the response header, and clears the MDC in `finally`. `application-prod.yml` sets `logging.file.name` to `C:/ProgramData/christopherbell.dev/logs/application.json.log`, `logging.structured.format.file: ecs`, and rolling at 10 MB with 14 files and a 256 MB cap. The console pattern gains the correlation field through `logging.pattern.correlation`.

**Ruleset (AC-1).** After this PR's checks report under the expected names, the ruleset gets a `required_status_checks` rule by `PUT`, preserving existing rules, with before and after JSON recorded in the log. Strict policy makes every PR test against current `main`.

| Alternative | Why not |
|---|---|
| Email via Resend for deploy alerts | User chose GitHub Deployments |
| Inbound webhook or GitHub runner on the host | Adds an inbound or privileged surface; README requires none |
| Gate on commit combined status | The repository uses check runs, not statuses; the workflow-run API is exact |
| Third-party JUnit reporter action | Needs `checks: write` and another pinned dependency; a small tested script does the job |
| Auto-commit regenerated verification metadata | Defeats checksum review; a GitHub-token push also never retriggers required checks |
| Ping service such as UptimeRobot | Needs a new external account; Actions is already trusted |
| JSON for the WinSW console log | Breaks the Mission Control log viewer |

## Expected Changes

| File or area | Change |
|---|---|
| `.github/workflows/ci.yml` | Pester cache, retrying install, `if: always()` test-summary step |
| `.github/workflows/dependency-verification.yml` | New Dependabot-only verification-metadata regeneration workflow |
| `.github/workflows/production-watch.yml` | New scheduled availability, deployment and lag watch |
| `.github/scripts/Write-TestSummary.ps1`, `Test-ProductionSite.ps1` | New CI and watch scripts |
| `.github/scripts/tests/*.Tests.ps1` | Pester tests for both scripts |
| `website/src/test/java/.../GitHubAutomationConfigurationTest.java` | Contracts for cache, retries, summary, new workflows' permissions, triggers and pins |
| `website/build.gradle.kts` | `automationPester` task added to Windows Pester verification |
| `ops/production/windows/modules/Production.AutoDeploy.psm1` | CI gate, tool-refresh gate, GitHub deployment reporting, status outcomes and categories |
| `ops/production/windows/modules/Production.Common.psm1` | `-Headers` on `Invoke-ProductionWebRequest`; help text |
| `ops/production/windows/modules/Production.Install.psm1` | `Install-ProductionGitHubToken` |
| `ops/production/windows/prod.ps1`, `Makefile` | `github-token-install` command and `-GitHubTokenPath` |
| `ops/production/windows/tests/Production.AutoDeploy.Tests.ps1`, `Production.Install.Tests.ps1`, `Production.Common.Tests.ps1` | Gate, reporting, token and header tests; default CI-success mock |
| `website/src/main/java/dev/christopherbell/configuration/filter/RequestCorrelationFilter.java` | New filter |
| `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java` | `GET:/actuator/info` public |
| `website/src/main/resources/application.yml`, `application-prod.yml` | `info` exposure and contributors, correlation pattern, prod JSON file logging |
| `website/src/test/java/...` | Filter tests; info endpoint security test |
| `README.md`, `configuration/README.md` | CI/CD, Production Watch, token setup, auto-status outcomes, info and request IDs |
| GitHub ruleset `main` | Required status checks with strict policy (settings, not files) |

## Task Breakdown

### Task 1 - Harden CI and surface test results
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `.github/workflows/ci.yml`; new `.github/scripts/Write-TestSummary.ps1`, `.github/scripts/tests/Write-TestSummary.Tests.ps1` (neighbor: ops Pester tests); `website/build.gradle.kts`; `GitHubAutomationConfigurationTest.java` |
| **Symbols** | Steps `Cache Pester 5.9.0`, `Install Pester 5.9.0`, `Summarize test results`; Gradle `automationPester`, `windowsPesterVerification`; contract tests `ciRunsPinnedWindowsPesterAndRetainsItsNunitResults`, new `ciCachesPesterAndRetriesInstall`, `ciAlwaysSummarizesTestResults` |
| **Inspection** | Read all listed files at `a9d20589`; Pester tasks run only worker, install and operations suites |
| **Behavior** | CI survives a Gallery miss on cache hit, retries otherwise, and always writes a results table; auto-deploy and script Pester suites run in `build` on Windows |
| **Invariants** | Exact Pester 5.9.0 assertion kept; actions pinned to full SHAs; failure-only 14-day upload kept; step timeouts bounded |
| **Boundary/API** | Required check name `build` unchanged; Gradle `build` on non-Windows still skips Windows Pester as today |
| **Effects and failures** | Summary script never fails the job on malformed or missing XML; it reports what it could not parse |
| **Tests and evidence** | Pester tests for summary parsing (JUnit, NUnit, empty, malformed); updated contract tests fail before the workflow edit |
| **Verification** | `gradlew.bat :website:test --tests *GitHubAutomationConfigurationTest`, `gradlew.bat :website:automationPester`, CI run on the PR shows the summary |

### Task 2 - Regenerate verification metadata for Dependabot PRs
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 (shared contract test file) |
| **Files** | New `.github/workflows/dependency-verification.yml`; `GitHubAutomationConfigurationTest.java`; `README.md` |
| **Symbols** | Job `regenerate-verification-metadata`; contract test `dependabotVerificationMetadataIsReadOnlyAndReviewable` |
| **Inspection** | `gradle/verification-metadata.xml` uses sha256 with `verify-metadata` true; failure in run 37301196194 |
| **Behavior** | On a Dependabot Gradle PR, a changed metadata file becomes an artifact with apply instructions; an unchanged file reports nothing to do |
| **Invariants** | `contents: read` only; no push; no `pull_request_target`; runs only for `dependabot[bot]` |
| **Boundary/API** | Does not report a required check name |
| **Effects and failures** | Gradle failure fails this job only; artifact retained 7 days |
| **Tests and evidence** | Contract test on trigger, actor guard, permissions and pins; local run of the regeneration command on the branch |
| **Verification** | Contract test; local `gradlew.bat --write-verification-metadata sha256 ...` leaves no diff on current `main` |

### Task 3 - Add Production Watch
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 (`automationPester` runs its tests); Task 4 for the `/actuator/info` live commit |
| **Files** | New `.github/workflows/production-watch.yml`, `.github/scripts/Test-ProductionSite.ps1`, `.github/scripts/tests/Test-ProductionSite.Tests.ps1`; `GitHubAutomationConfigurationTest.java`; `README.md` |
| **Symbols** | `Test-ProductionSite`, `Get-ProductionWatchVerdict`; workflow job `watch`; label `production-alert` |
| **Inspection** | Public smoke routes in `Production.Deploy.psm1`; environment `Production`; stale exemptions in `stale.yml` |
| **Behavior** | Healthy: closes any open alert with a recovery comment. Unhealthy: one open issue that gains a comment per failing run, naming each failed check |
| **Invariants** | Least privilege; no secrets beyond `GITHUB_TOKEN`; at most one open alert issue; probe retries bound runtime under 5 minutes |
| **Boundary/API** | `/actuator/info` lacking `build.version` is a reported check failure, not a crash |
| **Effects and failures** | Creates and closes issues and comments; creates the label if missing; GitHub API errors fail the run visibly |
| **Tests and evidence** | Pester tests with mocked HTTP for healthy, route failure, failed deployment, lag over and under 45 minutes, and retry recovery |
| **Verification** | Pester suite; local read-only run of the script against production; manual `workflow_dispatch` after merge |

### Task 4 - Expose build info, request IDs and JSON logs
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | New `configuration/filter/RequestCorrelationFilter.java` (neighbor `VersionedStaticAssetCacheFilter`); `SecurityConfig.java`; `application.yml`; `application-prod.yml`; new `RequestCorrelationFilterTest.java`; new `ActuatorInfoHttpSecurityIntegrationTest.java` (neighbor `DatabaseHealthHttpSecurityIntegrationTest`); `configuration/README.md`; `README.md` |
| **Symbols** | `RequestCorrelationFilter`, MDC key `requestId`, header `X-Request-Id`; `PUBLIC_URLS`; `management.endpoints.web.exposure.include`, `management.info.*.enabled`, `logging.structured.format.file`, `logging.file.name`, `logging.logback.rollingpolicy.*`, `logging.pattern.correlation` |
| **Inspection** | Actuator config, security matchers, filters and health security test at `a9d20589` |
| **Behavior** | `/actuator/info` public with build data only; every response carries `X-Request-Id`; prod writes ECS JSON lines to a rolling file |
| **Invariants** | `/actuator/health` stays protected; liveness/readiness unchanged; malformed or oversized inbound IDs are never echoed; MDC never leaks across requests; WinSW console log unchanged |
| **Boundary/API** | New public read-only endpoint and response header; no API shape changes |
| **Effects and failures** | File logging failure does not stop startup |
| **Tests and evidence** | Filter tests (valid echo, invalid replaced, absent generated, MDC cleared after exception); info endpoint unauthenticated 200 without env data, `/actuator/env` not exposed |
| **Verification** | Focused tests, full `gradlew.bat build`, local runtime check of `/actuator/info`, headers and JSON log file |

### Task 5 - Gate auto-deploy on CI and report GitHub deployments
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 (`automationPester` runs these tests in CI) |
| **Files** | `Production.AutoDeploy.psm1`, `Production.Common.psm1`, `Production.Install.psm1`, `prod.ps1`, `Makefile`, `Production.AutoDeploy.Tests.ps1`, `Production.Install.Tests.ps1`, `Production.Common.Tests.ps1`, `README.md` |
| **Symbols** | New `Get-AutoDeployGitHubRepository`, `Read-AutoDeployGitHubToken`, `Invoke-AutoDeployGitHubApi`, `Get-AutoDeployCiConclusion`, `Start-AutoDeployGitHubDeployment`, `Complete-AutoDeployGitHubDeployment`, `Install-ProductionGitHubToken`; changed `Invoke-AutoDeployOnce`, `Update-AutoDeployToolsFromOriginMain`, `Publish-AutoDeployStatus`, `Get-AutoDeployStatus`, `Get-AutoDeployStatusMessage`, `New-AutoDeployState` and `Read-AutoDeployState` (`ciSha`, `ciConclusion`, `ciCheckedAt`), `Invoke-ProductionWebRequest`, `Show-ProductionHelp`, `prod.ps1` handlers |
| **Inspection** | Functions listed under Inputs at `a9d20589`; test fixture `BeforeEach` mocks |
| **Behavior** | Only CI-green commits deploy or refresh tools; waiting and rejection are visible in `auto-status`; deploy attempts appear as `Production` deployments when a token is installed |
| **Invariants** | Recovery still runs before the gate; up-to-date path unchanged; deploy result never depends on reporting; token never logged or persisted outside its protected file; status schemaVersion stays 1 with additive enum values |
| **Boundary/API** | New `prod.cmd github-token-install -GitHubTokenPath`; `auto-status` adds `githubReporting` (`CONFIGURED`/`NOT_CONFIGURED`); existing commands unchanged |
| **Effects and failures** | GitHub reads: HTTP failure leads to `CHECK_FAILED`/`CI_CHECK`. Writes: best effort, one warning. Token file unprotected: reporting disabled with a warning |
| **Tests and evidence** | New tests fail first: pending, missing, failed and success verdicts; failed-verdict caching; tool refresh kept on non-success; deployment lifecycle; reporting failures ignored; token install validation and protection; header pass-through. Existing suite gets a default success mock |
| **Verification** | `Invoke-Pester` on the three suites under PowerShell 7 and Windows PowerShell 5.1 where the suite already runs there; `gradlew.bat build` |

### Task 6 - Require checks on main
Required skill: None (repository settings; no code)

| Contract | Detail |
|---|---|
| **Dependencies** | Tasks 1–5 pushed and the PR's checks reported |
| **Files** | None; GitHub ruleset `main` |
| **Symbols** | `required_status_checks` rule, `strict_required_status_checks_policy` |
| **Inspection** | `gh api repos/azurras/christopherbell.dev/rulesets/<id>` at planning: four rules, no bypass actors |
| **Behavior** | PRs cannot merge until all five checks pass on a branch current with `main` |
| **Invariants** | Existing rules and parameters unchanged; no bypass actors added |
| **Boundary/API** | Every open PR now needs these checks |
| **Effects and failures** | Wrong check name blocks all merges; fixed by reverting to the recorded before JSON |
| **Tests and evidence** | Before and after JSON in the log; this PR shows the five checks as required |
| **Verification** | `gh api .../rulesets/<id>` readback; `gh pr checks <n> --required` lists five |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Ruleset readback JSON | `gh pr checks --required` on this PR lists the five checks |
| AC-2 | `Production.AutoDeploy.Tests.ps1` gate tests, red before and green after | Read-only `Get-AutoDeployCiConclusion` against GitHub for `a9d20589` (SUCCESS) and `695a3ed8` (FAILED) |
| AC-3 | Contract tests | PR CI run log shows a cache restore or a single successful install; second run shows a cache hit |
| AC-4 | Contract test | Local regeneration command on the branch produces no diff |
| AC-5 | `Write-TestSummary.Tests.ps1`; `gradlew.bat build` includes `automationPester` | Script run over local `build/test-results` prints the table; PR CI job summary shows it |
| AC-6 | Deployment lifecycle, failure isolation and token install tests | No live token; documented as awaiting the user |
| AC-7 | `Test-ProductionSite.Tests.ps1` | Read-only script run against production; post-merge `workflow_dispatch` passes |
| AC-8 | `ActuatorInfoHttpSecurityIntegrationTest` | verify-local-app: candidate on the isolated `test` MongoDB returns 200 `/actuator/info` with `build.version` |
| AC-9 | `RequestCorrelationFilterTest` | Candidate echoes a valid ID, replaces an invalid one; with prod logging overrides pointed at a scratch path, ECS JSON lines contain `requestId` |
| AC-10 | Full `gradlew.bat build` | Published test report before the PR; post-merge `auto-status` and production `/actuator/info` readback |

- **Regressions:** full existing auto-deploy suite; health security test; Mission Control log viewer still reads the WinSW log; `GitHubAutomationConfigurationTest` pin rule covers new workflows.
- **Edge cases:** CI run not yet registered; re-run that turns a failure green after the cache window; token 401 falls back to anonymous; inbound ID with CRLF or more than 64 characters.
- **Reruns:** any runtime-affecting edit after the report triggers a rerun of the affected verification and a report update before pushing.

## Rollback or Recovery
1. Code: revert the merge commit through a PR; auto-deploy rolls forward to the revert. If the gate itself misbehaves (stuck at `AWAITING_CI`), an operator can still run `prod.cmd deploy` interactively.
2. Ruleset: `PUT` the recorded before JSON.
3. Token: delete `config\github-deployments.token`; reporting turns off and nothing else changes.
4. Watch alerts: disable `production-watch.yml` from the Actions tab; close the alert issue.
5. No data migrations; JSON log files can be deleted.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Wrong required-check name blocks every merge | Low | Names read from this PR's actual checks first; recorded before JSON for revert |
| Strict policy adds rebase churn for parallel agent PRs | Medium | Accepted by the user's "fix all"; reported in the outcome |
| GitHub API outage stalls deploys | Low | Visible as `CHECK_FAILED`/`CI_CHECK`; interactive deploy remains |
| Anonymous rate limit exhausted | Low | Failed verdict cached; token raises the limit |
| Cloudflare challenges runner probes | Medium | First manual run proves it; treated as a finding if it fails |
| Prod file log not writable | Low | Logback logs the error and continues; checked in post-deploy readback |
| `automationPester` flaky on hosted runners | Medium | Run locally under the same PowerShell first; failures fixed or logged |

## Implementation Log

### 2026-10-05 - Token install placement and status field

- **Change:** `Install-AutoDeployGitHubToken` lives in `Production.AutoDeploy.psm1` instead of `Production.Install.psm1`. `prod.ps1` routes `github-token-install`, covered by a new `Production.Command.Tests.ps1` case. The Makefile is unchanged. `auto-status` gains no `githubReporting` field; the install command verifies the token against GitHub before storing it. The runbook `docs/operations/windows-production.md` is also updated.
- **Reason:** The token loader, shape check and API helper all live in the auto-deploy module, so a second module would only re-export them. Makefile targets take no arguments, but the install needs a path. `auto-status` runs as a standard user who cannot read the protected config directory, so a status field there would misreport. Install-time verification proves the token works.
- **Impact:** Task 5 Files and Boundary/API; Expected Changes rows for Install, Makefile and docs. AC-6 is unchanged.

### 2026-10-05 - Production Watch timestamp bug found in live run

- **Change:** A live read-only run of `Test-ProductionSite.ps1` against production reported "passed CI -281 minutes ago". `Invoke-RestMethod` decodes `updated_at` into a UTC `DateTime`, and stringifying it drops the zone. Added `ConvertTo-UtcTimestamp` and a regression that uses the decoded `DateTime`; the regression fails on the old parse and passes now.
- **Reason:** Mocks returned strings, so only the real API exposed the conversion.
- **Impact:** Task 3 evidence; AC-7 lag detection is now correct.

### 2026-10-05 - Automation Pester wiring and local Gradle socket path

- **Change:** The `automationPester` task joins `check` through its own Windows-guarded dependency rather than `windowsPesterVerification`. The baseline auto-deploy suite passed 75/75 without elevation in 12 seconds before it was wired in. Gradle runs on this host need the README's short `jdk.net.unixdomain.tmpdir`, or they fail with "Unable to establish loopback connection".
- **Reason:** `windowsPesterVerification` also feeds the shared-folder-only `sharedFolderVerification` task.
- **Impact:** Task 1 Symbols. The local verification environment matches README guidance.

### 2026-10-05 - Nested test configuration captured slice tests

- **Change:** `ActuatorInfoHttpSecurityIntegrationTest` uses a nested plain `@Configuration` with `@EnableAutoConfiguration` instead of `@SpringBootConfiguration`.
- **Reason:** The first full build failed 4 tests (`AsyncDispatcherSecurityIntegrationTest` x3 and `SharedFolderWorkerStaticResourceTest`) with `UnreachableFilterChainException`. `@WebMvcTest` slices in `configuration.security` search parent packages for a `@SpringBootConfiguration`, found the new nested one in `configuration`, and combined its any-request chain with `SecurityConfig`.
- **Impact:** Task 4 test only; behavior and acceptance criteria unchanged. Full build rerun.

### 2026-10-05 - Build info version was unspecified

- **Change:** `website/build.gradle.kts` `springBoot.buildInfo` now sets `version` from `rootProject.version`, guarded by the new `BuildAutomationConfigurationTest.packagedBuildInfoCarriesTheCommitDerivedReleaseVersion`. Committed as `b5f7f5c`.
- **Reason:** Local runtime verification of `64cd652` and `1a00621` showed `/actuator/info` returning `build.version: "unspecified"`. The root project's commit-derived version never reached the `website` subproject. The plan assumed `build.version` was already `0.0.0-dev.<commit>`, and that assumption was false. The test failed before the fix and passed after; Mission Control's version display also had the unset value.
- **Impact:** Task 4 Files and the plan's version Assumption. AC-8 and AC-7 now hold at runtime.

### 2026-10-05 - Actuator responses arrive as bytes

- **Change:** `Test-ProductionSite.ps1` decodes byte responses (`ConvertTo-ResponseText`), with a regression that fails on `64cd652` and passes on `1a00621`.
- **Reason:** `Invoke-WebRequest` returns `application/vnd.spring-boot.actuator.v3+json` bodies as `byte[]`, as a live production readiness request confirmed. Stringifying them yields "123 34 ...", so the live commit would never have parsed in production.
- **Impact:** Task 3; AC-7 build-info check is correct against real actuator responses.

### 2026-10-05 - Merge push event was dropped; recovery shipped as follow-ups

- **Change:** #1481 merged as `06c3718` at 14:56 UTC, but GitHub recorded no push event or `pr_merge` activity for it, so no push workflow ran. The new gate correctly held production on `a9d2058` with `AWAITING_CI`, and the poller still refreshed its tools to `06c3718`, because the tools then installed predated the gate. Recovery, a stall alert, clearer token-install errors, workflow registration and a `gradlew.bat` renormalization shipped through the [follow-up plan](2026-10-05-10-11-christopherbell-dev-recover-missed-ci-runs-and-clarify-token-install-failures.md) as #1482 (`ca98b1e`) and #1483 (`4663692`). The first production deploy carrying this plan's code is therefore `ca98b1e`.
- **Reason:** `CI Build` had no manual trigger, and Production Watch could not register or see the stall.
- **Impact:** AC-7 and AC-10 are met through the follow-up PRs. The user installed the deployment token from the `06c3718` tooling after two attempts that exposed the elevation and empty-file messages.

## Outcome

> [!WARNING]
> Every finding is fixed and live in production on `ca98b1e`. AC-4's Dependabot path has not run yet; it awaits the next Dependabot Gradle PR. AC-9's production JSON log exists but is readable only by administrators, so its contents were verified locally, not on the host.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Ruleset 977691 readback lists `build`, the three `Analyze (...)` checks and `dependency-review` from GitHub Actions (integration 15368), strict policy on, with the four original rules unchanged; GitHub only added the default `required_reviewers: []`. #1481 showed `BLOCKED` until its checks passed. |
| AC-2 | ✅ Met | Pester gate tests. Live: `06c3718`, with no CI run, held at `AWAITING_CI` while `a9d2058` kept serving; `ca98b1e` deployed at 15:49 UTC only after its `CI Build` push run passed at 15:47. |
| AC-3 | ✅ Met | Contract test. On the PR and `main` runs the cache missed and `Get-Module -ListAvailable` found the runner image's Pester 5.9.0, so the Gallery was not contacted. The retry path is covered by the workflow script and the contract test. |
| AC-4 | ⚠️ Partly met | Workflow merged, registered and correctly skipped for non-Dependabot PRs; the regeneration command leaves `verification-metadata.xml` unchanged on current `main` ([report](../test-reports/2026-10-05-09-44-christopherbell-dev-harden-ci-cd-robustness-and-observability.md)). Not yet exercised on a Dependabot PR. |
| AC-5 | ✅ Met | Every CI run since #1481 shows the test summary; `automation-pwsh7` ran 121 tests in CI. |
| AC-6 | ✅ Met | GitHub `Production` deployment 6863501513 for `ca98b1e`: `in_progress` at 15:49:14 UTC, then `success` at 15:54:10 with `https://www.christopherbell.dev/`. Token installed by the user via `github-token-install`. |
| AC-7 | ✅ Met | Registered by #1483. Manual run [37339944271](https://github.com/azurras/christopherbell.dev/actions/runs/37339944271) concluded `success` with no alert issue; the read-only verdict passed all six checks on `ca98b1e`. |
| AC-8 | ✅ Met | Production `/actuator/info` returns `0.0.0-dev.ca98b1e249b2f91e33ab4286cb32a9036d8deda7`. |
| AC-9 | ⚠️ Partly met | Production responses carry `X-Request-Id`; `application.json.log` exists in the protected logs folder. ECS lines with `requestId` were verified on the local candidate, not read on the host. |
| AC-10 | ✅ Met | [Report](../test-reports/2026-10-05-09-44-christopherbell-dev-harden-ci-cd-robustness-and-observability.md) for `b5f7f5c`; #1481 merged as `06c3718` with required checks green. Deployed as part of `ca98b1e`: `auto-status` `SUCCEEDED`, healthy, active `ca98b1e`. |

- **Shipped versus planned:** everything planned, plus fixes found during runtime verification: the commit-derived build version, byte-decoded actuator JSON and UTC timestamps in the watch.
- **Follow-ups:** watch the next Dependabot Gradle PR for AC-4. Optionally have an administrator read one `application.json.log` line. The user's main checkout `A:\Projects\christopherbell.dev` is 105 commits behind with an untracked snapshot folder, left untouched.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
