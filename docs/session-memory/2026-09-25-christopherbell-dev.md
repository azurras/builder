# 2026-09-25 - christopherbell-dev Session Memory

Work, decisions, events, and evidence for this date.

## 2026-09-25 09:46 Central Daylight Time - Production recovery and guarded rollback fix

The user asked whether the site could be brought back. Continued the authorized Task 42 production recovery from the 2026-09-24 incident. The first guarded helper had been waiting for missing mandatory PowerShell parameters; fixed the parameter splat and ran the supported rollback after confirming exact release pointers and target schemas under `deploy.lock`.

The rollback changed active to prior release `4b552a63a08c9333bdaa0d7827b23eb811920f37` and previous to failed candidate `fb10948cc4d0b3b2d5f739789b8a810713456301`, but timed out on readiness because the protected marker still named the candidate. Logs show Spring started and connected to MongoDB. Reconciled the marker to the selected prior release under the lock; `prod.ps1 restart` then passed the local production smoke suite. Local readiness and liveness returned HTTP 200; 11 smoke routes on each public hostname returned HTTP 200 (22/22). MongoDB and cloudflared were running. Restored normal service recovery under lock and verified `sc.exe qfailure`: reset 3600 seconds, restart actions at 10000 and 30000 ms. No application data or database was changed.

Task 42 source changes were in PR #1440, merged as `19c986368396ea45cb8e0467ef7a4fa65bf19889`. Focused PowerShell 7/Pester suites passed 170/170; PowerShell 5.1 parser checks passed; required Windows, macOS, Ubuntu, CodeQL, and dependency-review gates passed.

Attempted to deploy merged main. The deployer built in its own clean protected worktree; the build failed before release switch with `gradlew.bat exited with code 1`. The protected Gradle daemon log recorded `Unable to establish loopback connection` and `SocketException: Invalid argument: connect`. Post-failure protected readback showed active+marker SHA still `4b552a...`, service Running, and public routes healthy. This corrects an earlier mistaken attribution to the local dirty `gradlew.bat`; preserve that unrelated edit. Pester created an untracked `testResults.xml`; do not include it in commits.

Runtime details are in [the 2026-09-25 recovery report](../test-reports/2026-09-25-christopherbell-dev-target-release-recovery-and-public-verification.md). Task 42 remains in progress: diagnose the production Gradle loopback failure, deploy merged main, verify the guarded poller once, then enable recurring polling after healthy status readback. Automatic deployment task remains Disabled.


## 2026-09-25 11:43 Central Daylight Time - Production deployer KISS pass

The user asked to make a KISS pass on the deployment tooling. Reused the existing Task 42 plan and published Task 43 before the code edit. Narrowed the refactor to the ordinary `TARGET_ACTIVE` path: `Invoke-ProductionDeploy` delegates to one helper that owns candidate activation, marker publication, recovery-policy restoration, and the single guarded prior-release recovery. First Music cutover and reconciliation code remains untouched.

On the original linked site worktree, the deployment suite passed 98/98 before extraction. The readiness failure characterization was then expanded with a marker-publication failure case; both pass. All 14 Windows production Pester suites passed: 814 passed, 0 failed, 28 skipped. Windows PowerShell 5.1 parser checks passed for the edited module and tests; `git diff --check` passed. The Windows, macOS and Ubuntu build jobs, CodeQL analyses and dependency review for PR #1441 all passed.

The clean branch `codex/deployer-kiss-pass-clean` was based on `origin/main`; its implementation commit was `e2dfc1b6`. PR #1441, [Simplify target release deployment path](https://github.com/azurras/christopherbell.dev/pull/1441), merged at 2026-09-25 16:39:37 UTC as `465858d1fe604a9883d31e1e5dc515e27aaa1b2a`. Builder plan Task 43 records the result. Runtime report: [deployer KISS pass](../test-reports/2026-09-25-christopherbell-dev-deployer-kiss-pass.md).

At 16:40:58 UTC, `ChristopherBellDev` was Running and `GET https://www.christopherbell.dev/` returned HTTP 200, page title `CB | Home`, body length 4,348. No production release pointer, application binary, service config, or database was changed by this behavior-preserving deployment-script refactor. This continuity check does not establish that a new production release or protected deployment-tool refresh occurred.

One initial post-edit marker-failure characterization run exposed a faulty test mock: the simulated candidate switch fell through into the prior-release mock behavior and made both junction identities point to the candidate. Added an early return to the candidate branch; both readiness and marker failure cases then passed. Preserved the unrelated modified `gradlew.bat` and untracked `testResults.xml` in the original site worktree.

Task 42 remains open for the separate protected production Gradle build failure and guarded poller verification. The production site was healthy after this KISS pass. The Builder plan and test report should be published after indexes and validation are refreshed.


## 2026-09-25 12:43 Central Daylight Time - Gradle socket workaround and production boundary

Continued Task 42 after the Task 43 KISS refactor merged as PR #1441. Reproduced the Windows JDK 25 Gradle daemon loopback failure in a clean worktree. Direct `Pipe.open()` succeeds, but Gradle fails during Unix-domain socket setup with the default temp directory; `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp` allows the daemon to start. Updated `New-ReleaseFromOriginMain` to pass this short path only to the Gradle child while appending to (and preserving) inherited `JAVA_TOOL_OPTIONS`.

The real full website build then reached tests and exposed two media concurrency tests with two-second waits. They timed out in the full build and in an isolated rerun. Increased only those bounded waits to ten seconds while retaining the latch and no-overlap checks. Both focused tests passed; the full `:website:build` passed in 5m16s via `Invoke-CheckedProcess`. The complete production Pester suite passed 814/814 with 28 skipped. PR #1442, [Fix Windows production Gradle build startup](https://github.com/azurras/christopherbell.dev/pull/1442), passed Windows/macOS/Ubuntu CI, CodeQL and dependency review and merged as `427530f6f195dbffaa81c8557feaad3e899bdf6a`.

After merge, the public site returned HTTP 200 with title `CB | Home` and a 4,348-byte body; `ChristopherBellDev` was Running/Automatic. Non-elevated `prod.cmd auto-status` was denied access to protected `C:\ProgramData\christopherbell.dev\config\deploy.json`; the exact `ChristopherBellAutoDeploy` task query was also denied. No protected deployment-tool refresh, release switch, or poller action was attempted. The production checkout's pre-existing modified `gradlew.bat` and untracked SHA-named directory, plus Pester-generated `testResults.xml` in worktrees, were left untouched and excluded.

The report is [Windows Gradle deployer verification](../test-reports/2026-09-25-windows-gradle-deployer-verification.md). The Task 42 plan now records the root cause, regression coverage, passing build and the unresolved production deployment boundary. Task 42 remains open until protected task/status readback and release-level production verification can be performed under the approved operational boundary.


## 2026-09-25 13:06 Central Daylight Time - Auto status legacy compatibility merge

Merged PR #1443 (`7639e3f1b552013a72cb59f0e32807fc6356daf3`) after confirming CI Build, CodeQL, and Dependency Review succeeded. The regression reproduced `available=False, reason=INVALID` for the live schema-version-1 status record that omits optional `failureDetail`; it now passes, and the full Windows production PowerShell suite passed 815 with 0 failures and 28 skipped. The merged-main non-elevated `prod.cmd auto-status` reads the live public status record and reports the stored deployment failure, stale freshness, running/healthy service separately from scheduler `ACCESS_DENIED`. Builder runtime report and Task 42 plan updated. No protected installed-tool refresh, scheduled poller action, application release switch, or production mutation was performed because the current non-elevated process receives Access Denied for protected deployment config and Scheduler queries. Public continuity evidence remains HTTP 200 with the service Running/Automatic; production deployment and poller activation remain open verification work.
