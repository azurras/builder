## Document Status

complete

## Story/Issue

Site bug audit Task 42: restore a prior target release after failed deployment. Runtime recovery is complete; deployment of merged main remains a follow-up.

## Branch

`codex/production-deploy-failure-rollback-20260925`, source `4daa85fa3d3751ac093c82fc15619cafa816be99`; PR #1440 merged to main as `19c986368396ea45cb8e0467ef7a4fa65bf19889` on 2026-09-25 14:35:27 UTC.

## App / Environment

Native Windows 11 production. Base URL: `http://127.0.0.1:8080`; MongoDB `127.0.0.1:27017`; public URLs `https://christopherbell.dev/` and `https://www.christopherbell.dev/`. Final active release and marker SHA `4b552a63a08c9333bdaa0d7827b23eb811920f37`; previous release `fb10948cc4d0b3b2d5f739789b8a810713456301`. Website, MongoDB, cloudflared running. Automatic deployment task remains disabled. No database or application data changed.

## Local Run Details

Recovery validated exact release pointers and target schemas under the deployment lock. The first supported rollback selected the prior release but readiness timed out while the marker still identified the candidate; it left the service stopped. The marker was then reconciled under lock to the active prior release. `ops/production/windows/prod.ps1 restart` passed its guarded local smoke suite, and the service was left running. Under the lock, service recovery was restored and `sc.exe qfailure ChristopherBellDev` verified reset 3600 seconds and restart delays 10000 and 30000 milliseconds.

Evidence logs: `%TEMP%\codex-supported-target-release-rollback.log`, `%TEMP%\codex-start-known-good-release.log`, `%TEMP%\codex-production-recovery-diagnostics.txt`, `%TEMP%\codex-deploy-main-after-recovery.log`.

## Test Cases

1. Probe both public homepages and local health before recovery.
2. Attempt guarded rollback while the marker still identified the candidate.
3. Align marker to active prior release and run guarded restart/local smoke.
4. Verify local health and Windows recovery policy.
5. Check 11 routes on each public hostname.
6. Attempt merged-main deployment and verify a failed build did not switch releases.

## Data Sent

- GET `/actuator/health/readiness` and `/actuator/health/liveness` at base URL `http://127.0.0.1:8080`.
- GET each of `/`, `/blog`, `/wfl`, `/canes-box-tracker`, `/robots.txt`, `/sitemap.xml`, `/favicon.ico`, `/actuator/health/liveness`, `/actuator/health/readiness`, `/.well-known/nodeinfo`, and `/nodeinfo/2.1` against each public URL.
- The guarded local smoke suite included an invalid-login request with an intentionally invalid password.
- The deployer attempted merged main SHA `19c986368396ea45cb8e0467ef7a4fa65bf19889` in its isolated protected worktree.

## Response Received

Before recovery, both public homepages returned HTTP 502 and local readiness had no listener. The first rollback failed its readiness check; logs show Spring started and connected to MongoDB while the marker named the other release. After marker reconciliation and guarded restart, local smoke passed; readiness and liveness each returned status 200. All 22 public route checks returned status 200. The normal service recovery policy passed its exact `sc.exe qfailure` check.

Merged-main deployment failed before release switch: `gradlew.bat exited with code 1`; the protected Gradle daemon log recorded `Unable to establish loopback connection` and `SocketException: Invalid argument: connect`. Post-failure state remained active+marker SHA `4b552a...`, service Running, public site healthy.

## Pass / Fail

- Production recovery and public smoke: PASS.
- Service restart recovery policy: PASS.
- Rollback before marker reconciliation: FAIL, fail-closed; reproduced Task 42's marker/release identity issue.
- Merged-main production build/deploy: FAIL at Gradle startup; no release pointer or data changes.
- Automatic poller end-to-end verification: NOT RUN; scheduled task remains disabled.

## Evidence

Fresh production probes and protected state readback were completed on 2026-09-25 America/Chicago. Focused Pester suites passed 170/170 and Windows PowerShell 5.1 parser checks passed for changed modules/tests. PR #1440 required CI passed on Windows, macOS, and Ubuntu; CodeQL and dependency review passed.

## Bugs / Follow-ups

Diagnose the production Gradle loopback failure and retry merged-main deployment. Keep the automatic deployment task disabled until deployment passes; then trigger the guarded poller once, verify status and release health, enable recurring polling, and complete Task 42.
