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

- Task 38 is planned: prevent false `UP_TO_DATE` status when production service/readiness is down; safely recover only through the existing lock and schema-direction guards; bound retries; and surface the sanitized recovery result.
- Immediate recovery requires the user to run the documented `prod.cmd restart` from an Administrator PowerShell. The task has already provided the exact command and reason; the current approval policy cannot surface an elevation prompt.
- Do not restore SCM failure actions or start the service directly until the guarded deployment/migration state is verified. Root cause of the unexpected exits remains unknown because protected app logs/configuration are inaccessible.

## Follow-up Evidence (2026-09-24 20:45 UTC)

After PR #1436 merged at 20:41:20 UTC as `e166f7db9334b117f45e43e3bb7978bdcaf70ca3`, read-only `prod.ps1 auto-status` returned `BACKING_OFF`, `failureCategory=DEPLOYMENT`, `remoteSha=e166f7db9334b117f45e43e3bb7978bdcaf70ca3`, and `activeSha=4b552a63a08c9333bdaa0d7827b23eb811920f37`. It did not report `UP_TO_DATE` for this differing SHA. `ChristopherBellDev` remained stopped, MongoDB and cloudflared remained running, and public readiness still returned HTTP 502. Poller status remained `UNKNOWN/ACCESS_DENIED`.

Filtered Application and System events for 2026-09-24 14:55-15:05 CDT show PR #1432 had merged at 14:51 CDT. At 14:59:04, the website service startup type changed from automatic to disabled. At 14:59:05, WinSW failed in `ProcessHelper.GetChildren` / `StopProcessTree` with `Win32Exception (6): The handle is invalid`; Windows recorded a .NET Runtime 1026 and Application Error 1000 for `ChristopherBellDev.exe` 2.12.0. The website launcher process started at 14:59:10; its child exited with code 1 at 14:59:13, and the service terminated. This makes the production transition the likely outage trigger. The launcher child error is not present in the accessible event excerpt. Reading the protected service log directory returned `UnauthorizedAccessException`; no protected log or configuration contents were read.

No production mutation was made. Recovery and exact application-level root cause remain unverified pending the supported guarded restart from an elevated context and access to the protected startup diagnostic.
