## Document Status

blocked

## Story/Issue

Task 38 in the christopherbell.dev audit plan: determine why production is unreachable while automatic-deploy status reports the active release as current.

## Branch

Production status identified active release `4b552a63a08c9333bdaa0d7827b23eb811920f37`, matching the recorded remote main SHA at probe time. PR #1436 was still open; it changes test-profile-only configuration and does not affect production behavior.

## App / Environment

Production site `https://www.christopherbell.dev`, native Windows service `ChristopherBellDev`, MongoDB service `MongoDB`, Cloudflare tunnel service `cloudflared`, and production listener port 8080. Checks were non-mutating. No database or application state was changed.

## Local Run Details

Read-only probes ran on the production host on 2026-09-24. Non-elevated `prod.ps1 auto-status` returned a fresh record at 20:28:58 UTC with `status=UP_TO_DATE`, `remoteSha=activeSha=4b552a63a08c9333bdaa0d7827b23eb811920f37`, and successful tool refresh. Windows service and listener queries showed `ChristopherBellDev=Stopped`, `MongoDB=Running`, `cloudflared=Running`, and no port-8080 listener.

The documented `prod.ps1 verify-startup` and guarded `prod.ps1 restart` commands both stopped while reading protected production configuration, before service mutation. This Codex task's approval policy is `never`, so it cannot request an elevated token or show a user approval prompt. The service was not restarted through a raw command.

## Test Cases

1. Request production homepage, liveness, readiness, and sitemap.
2. Compare sanitized automatic-deploy status with the service state and production listener.
3. Read recent Service Control Manager termination events and query the website service recovery configuration.

## Data Sent

Unauthenticated `GET https://www.christopherbell.dev/`, `/actuator/health/liveness`, `/actuator/health/readiness`, and `/sitemap.xml`. Local commands were `prod.ps1 auto-status`, `prod.ps1 verify-startup`, `prod.ps1 restart`, `Get-Service`, `Get-NetTCPConnection`, filtered System event-log reads, and `sc.exe qfailure ChristopherBellDev`.

## Response Received

- All four public routes returned HTTP status code 502 from Cloudflare; the body was `error code: 502`.
- `ChristopherBellDev` was stopped with Automatic startup; MongoDB and `cloudflared` were running. No process listened on port 8080.
- System log contained Service Control Manager event 7034 twice, at 14:59:08 and 14:59:13 CDT, saying the website service terminated unexpectedly.
- `sc.exe qfailure ChristopherBellDev` succeeded but showed a zero reset period and no failure actions in its output. Whether that is an intentionally suspended deployment guard or a recovery defect remains unconfirmed.
- Both guarded verification and restart returned access denied while reading protected configuration. They stopped before service mutation.

## Pass / Fail

- Production availability: failed; the public site was returning 502 and the local website service was stopped.
- Automatic-deploy health projection: failed; it reported fresh `UP_TO_DATE` solely from matching release SHAs while the service was stopped and public endpoints were failing.
- Production state safety: passed; no service, listener, configuration, ACL, deployment, or database mutation occurred.

## Evidence

- `prod.ps1 auto-status` sanitized output with fresh timestamps and matching active/remote SHA.
- Public HTTP probes returned 502 with `Server: cloudflare` and a DFW Cloudflare Ray ID.
- Service state, local listener query, event IDs 7034, and `sc.exe qfailure` were read without modifying state.
- `prod.ps1 verify-startup` and `prod.ps1 restart` both failed before their intended checks/effects because protected deployment configuration was unreadable to this account.

## Bugs / Follow-ups

- Task 38 is implemented in PR #1437: prevent false `UP_TO_DATE` status when production service/readiness is down; recover only through the existing lock and schema-direction guards; bound retries; and surface sanitized recovery status. Hosted CI is running; merge and production recovery remain pending.
- Immediate recovery requires the user to run the documented `prod.cmd restart` from an Administrator PowerShell. The task has already provided the exact command and reason; the current approval policy cannot surface an elevation prompt.
- Do not restore SCM failure actions or start the service directly until the guarded deployment/migration state is verified. Root cause of the unexpected exits remains unknown because protected app logs/configuration are inaccessible.

## Follow-up Evidence (2026-09-24 20:45 UTC)

After PR #1436 merged at 20:41:20 UTC as `e166f7db9334b117f45e43e3bb7978bdcaf70ca3`, read-only `prod.ps1 auto-status` returned `BACKING_OFF`, `failureCategory=DEPLOYMENT`, `remoteSha=e166f7db9334b117f45e43e3bb7978bdcaf70ca3`, and `activeSha=4b552a63a08c9333bdaa0d7827b23eb811920f37`. It did not report `UP_TO_DATE` for this differing SHA. `ChristopherBellDev` remained stopped, MongoDB and cloudflared remained running, and public readiness still returned HTTP 502. Poller status remained `UNKNOWN/ACCESS_DENIED`.

Filtered Application and System events for 2026-09-24 14:55-15:05 CDT show PR #1432 had merged at 14:51 CDT. At 14:59:04, the website service startup type changed from automatic to disabled. At 14:59:05, WinSW failed in `ProcessHelper.GetChildren` / `StopProcessTree` with `Win32Exception (6): The handle is invalid`; Windows recorded a .NET Runtime 1026 and Application Error 1000 for `ChristopherBellDev.exe` 2.12.0. The website launcher process started at 14:59:10; its child exited with code 1 at 14:59:13, and the service terminated. This makes the production transition the likely outage trigger. The launcher child error is not present in the accessible event excerpt. Reading the protected service log directory returned `UnauthorizedAccessException`; no protected log or configuration contents were read.

No production mutation was made. Recovery and exact application-level root cause remain unverified pending the supported guarded restart from an elevated context and access to the protected startup diagnostic.

## Candidate Status Projection and Regression Verification (2026-09-24 21:10 UTC)

The Task 38 candidate from worktree `A:\Projects\christopherbell.dev-worktrees\auto-deploy-live-health-20260924`, based on merged main `e166f7db9334b117f45e43e3bb7978bdcaf70ca3`, was run read-only against the production host. `prod.ps1 auto-status` exited 0 and reported fresh status `SERVICE_UNHEALTHY`, `deploymentStatus=BACKING_OFF`, `reason=SERVICE_STOPPED`, `serviceState=STOPPED`, `siteHealth=UNHEALTHY`, and `siteHealthReason=SERVICE_STOPPED`. It retained sanitized remote/active revisions and poller `UNKNOWN/ACCESS_DENIED`. The production service remained stopped and public readiness returned HTTP 502. This verifies the candidate CLI no longer presents the stored healthy-looking state without live health context; the candidate poller recovery implementation has not been deployed or run against the production service.

Regression verification on the candidate source passed the automatic-deploy (69), deployment (97), operations (102), and command (17) Pester suites under both PowerShell 7.6.6/Pester 5.9 and Windows PowerShell 5.1.26100.9444/Pester 5.9: 285/285 in each runtime. PowerShell parser checks and `git diff --check` passed. These are code checks plus a read-only production CLI probe; they do not prove service recovery or startup.

No production service, listener, configuration, ACL, deployment task, or database state was changed. The outage and root launcher failure remain unresolved; the current host still cannot surface an elevated prompt.

## Post-Merge Guarded Recovery Attempt (2026-09-24 21:29 UTC)

PR #1437 passed all required hosted checks and merged at 2026-09-24 21:22 UTC as `3b11df8a10846adf5a686f1917254ec7583e3e2f`. The SYSTEM poller refreshed its tools to the merged SHA and attempted the candidate guarded recovery. The sanitized status changed to `DEPLOYMENT_FAILED` / `CANDIDATE_STARTUP`; service remained `STOPPED` and the public readiness endpoint still returned HTTP 502. A read-only query of System and Application event logs for matching service/recovery events returned no records. This establishes that the automatic recovery path ran but did not restore service; sanitized status and available event records do not identify the underlying exception.

An elevated launch of the supported `prod.cmd restart` was attempted using the already-authorized UAC route. Windows returned `The operation was canceled by the user` before the elevated PowerShell process started; the restart command did not execute and no administrator-level production mutation occurred. The remaining recovery step is to run `prod.cmd restart` from Administrator PowerShell, inspect its guarded diagnostic output, then verify local and public readiness. The deployment fix is merged; production recovery is not complete.
