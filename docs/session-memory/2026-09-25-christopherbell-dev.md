# 2026-09-25 - christopherbell-dev Session Memory

Work, decisions, events, and evidence for this date.

## 2026-09-25 09:46 Central Daylight Time - Production recovery and guarded rollback fix

The user asked whether the site could be brought back. Continued the authorized Task 42 production recovery from the 2026-09-24 incident. The first guarded helper had been waiting for missing mandatory PowerShell parameters; fixed the parameter splat and ran the supported rollback after confirming exact release pointers and target schemas under `deploy.lock`.

The rollback changed active to prior release `4b552a63a08c9333bdaa0d7827b23eb811920f37` and previous to failed candidate `fb10948cc4d0b3b2d5f739789b8a810713456301`, but timed out on readiness because the protected marker still named the candidate. Logs show Spring started and connected to MongoDB. Reconciled the marker to the selected prior release under the lock; `prod.ps1 restart` then passed the local production smoke suite. Local readiness and liveness returned HTTP 200; 11 smoke routes on each public hostname returned HTTP 200 (22/22). MongoDB and cloudflared were running. Restored normal service recovery under lock and verified `sc.exe qfailure`: reset 3600 seconds, restart actions at 10000 and 30000 ms. No application data or database was changed.

Task 42 source changes were in PR #1440, merged as `19c986368396ea45cb8e0467ef7a4fa65bf19889`. Focused PowerShell 7/Pester suites passed 170/170; PowerShell 5.1 parser checks passed; required Windows, macOS, Ubuntu, CodeQL, and dependency-review gates passed.

Attempted to deploy merged main. The deployer built in its own clean protected worktree; the build failed before release switch with `gradlew.bat exited with code 1`. The protected Gradle daemon log recorded `Unable to establish loopback connection` and `SocketException: Invalid argument: connect`. Post-failure protected readback showed active+marker SHA still `4b552a...`, service Running, and public routes healthy. This corrects an earlier mistaken attribution to the local dirty `gradlew.bat`; preserve that unrelated edit. Pester created an untracked `testResults.xml`; do not include it in commits.

Runtime details are in [the 2026-09-25 recovery report](../test-reports/2026-09-25-christopherbell-dev-target-release-recovery-and-public-verification.md). Task 42 remains in progress: diagnose the production Gradle loopback failure, deploy merged main, verify the guarded poller once, then enable recurring polling after healthy status readback. Automatic deployment task remains Disabled.
