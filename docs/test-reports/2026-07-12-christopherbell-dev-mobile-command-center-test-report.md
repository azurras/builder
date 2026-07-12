# christopherbell.dev Mobile Command Center Test Report

## Document Status

complete

## Story/Issue

Direct July 12, 2026 request for an admin-only mobile command center. Related work: `docs/work/2026-07-12-christopherbell-dev-mobile-command-center.md`.

## Branch

- Spoke: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center`
- Branch: `codex/mobile-command-center`
- Runtime-tested commit: `b7484d8d`
- Base: `origin/main` at `af034913`

## App / Environment

- Windows 11 production/development desktop, Java 25.0.3.
- Spring profile `local`; candidate URL `http://127.0.0.1:8090`.
- Production port 8080 remained running throughout.
- Isolated MongoDB database `christopherbell_command_center_test`, dropped afterward.
- Actions `SIMULATED`; power-action simulation enabled only for the candidate.
- Native sensor libraries disabled locally; CPU temperature stayed explicitly unavailable.
- Controlled log: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center\.superpowers\runtime\command-center-test.log`.
- Real read-only OSHI, `nvidia-smi`, production-service/port, response-time, and MongoDB probes.

## Local Run Details

The first attempt exposed ambiguous Spring component constructors and failed before serving traffic. A failing wiring test was added, every affected production constructor was marked for injection, the full suite passed, and commit `b7484d8d Fix command center component wiring` was created.

Successful start command:

```powershell
java -jar website\build\libs\website.jar --spring.profiles.active=local --server.port=8090 --spring.mongodb.uri=mongodb://127.0.0.1:27017/christopherbell_command_center_test --spring.mongodb.database=christopherbell_command_center_test --spring.data.mongodb.database=christopherbell_command_center_test --command-center.log-path=A:/Projects/christopherbell.dev-worktrees/mobile-command-center/.superpowers/runtime/command-center-test.log --command-center.actions.mode=SIMULATED --command-center.actions.power-actions-enabled=true --command-center.sensor-libraries-enabled=false --command-center.production-port=8080 --command-center.commit-identifier=b7484d8d
```

- Candidate PID: 36168.
- Tomcat started on 8090; shutdown was graceful via Ctrl+C.
- The temporary database was dropped and port 8090 closed.
- Production remained on port 8080, PID 22152.

## Test Cases

| Test case | Result | Evidence |
| --- | --- | --- |
| Automated regression/build | Pass | 576 Java and 113 JavaScript tests; full build successful |
| Public shell/anonymous boundary | Pass | `/` 200; `/command-center` 200 data-free shell; anonymous snapshot 403 |
| Regular user | Pass | USER login succeeded; snapshot 403 |
| Fresh administrator | Pass | Active approved ADMIN snapshot 200, 23 metrics |
| Host metrics | Pass | CPU, RAM, disk, network, GPU, uptime, service/port, MongoDB, latency, commit present; CPU temperature unavailable explicitly |
| Logs/filter/redaction | Pass | ALL four records; WARN literal query one; five fake secrets redacted |
| Rotation | Pass | Old cursor returned reset=true, status=ok, two fresh records, no secret |
| Wrong password | Pass | Action returned 400 and durable `wrong-password` audit |
| Simulated site restart | Pass | 202 `RESTART_SITE`; candidate homepage stayed 200 |
| Pending/cancel | Pass | Restart-computer 202, `ACTION_PENDING`, cancel 200, state cleared |
| Audit safety | Pass | Ten rows had action/outcome/source IP; no password or challenge ID |
| Mobile UI | Pass | 390x844; clientWidth and scrollWidth both 390 |
| Desktop UI | Pass | 1440x900 four-column grid |
| Dialog cleanup | Pass | Password and phrase empty after cancel/reopen |
| Browser console | Pass | No error entries |

## Data Sent

Two accounts were created through `POST /api/accounts/2024-12-15/create` in the isolated database. `cc_runtime_admin` was promoted only in that temporary database to active, approved ADMIN; `cc_runtime_user` remained USER. The temporary password is omitted. Accounts and hashes were removed with the database.

Authorization requests:

- Anonymous, USER bearer, and ADMIN bearer `GET /api/admin/command-center/2026-07-12/snapshot`.
- Tokens stayed only in a temporary PowerShell process and were not printed or persisted.

Log requests:

- `GET .../logs?level=ALL`
- `GET .../logs?level=WARN&query=rotation-needle`
- `GET .../logs?cursor=<opaque-cursor>` after controlled rotation

The fake log contained password, token, JSON password, Bearer authorization, nested escaped JSON password, and rotated-token values.

Action requests:

- Challenge and action for `RESTART_SITE`, first with a wrong password and then with the correct temporary password and exact server-returned phrase.
- Challenge and action for `RESTART_COMPUTER` in simulated mode.
- `POST .../actions/cancel`.

No real WinSW, restart, shutdown, or power command ran.

## Response Received

HTTP response evidence from the running app:

- Status code: 403 for anonymous and USER snapshot requests; status code: 200 for ADMIN.
- Anonymous snapshot 403; USER snapshot 403; ADMIN snapshot 200.
- Snapshot health `DEGRADED` because local native CPU temperature was intentionally unavailable.
- Log ALL 200/four records; WARN literal filter 200/one record.
- All five fake-secret leak checks false; five `[REDACTED]` markers.
- Rotation 200, reset=true, status=ok, two new records, rotated-secret leak false.
- Wrong-password action 400.
- Simulated restart-site 202 and homepage remained 200.
- Simulated restart-computer 202; snapshot `ACTION_PENDING`, cancellable true.
- Cancel 200; pending action cleared.
- Browser console errors: none.

## Pass / Fail

Overall local runtime result: **PASS**.

All safety-critical candidate behaviors passed. Production 8080 was not interrupted. Computer restart and shutdown were not executed.

## Evidence

- Java XML: 71 suites, 576 tests, 0 failures, 0 errors, 0 skipped.
- JavaScript: 113/113 passed.
- Full `:website:test :website:build`: `BUILD SUCCESSFUL`.
- Mobile: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center\.superpowers\runtime\command-center-mobile-viewport.png`.
- Desktop: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center\.superpowers\runtime\command-center-desktop.png`.
- Dialog: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center\.superpowers\runtime\command-center-action-dialog.png`.
- Audit outcomes observed: created, wrong-password, accepted, and launched for site restart, computer restart, and cancel.

## Bugs / Follow-ups

- Fixed during runtime: ambiguous Spring injection constructors prevented startup; regression coverage and explicit injection constructors are in `b7484d8d`.
- Anonymous requests receive 403 from the existing global Spring Security entry point while controller-level tests model 401. Both deny access; status normalization can be handled separately without broadening this feature.
- Candidate startup ran the existing OpenStreetMap catch-up only in the isolated database, which was dropped. A future smoke profile could disable unrelated startup jobs.
- CPU temperature was unavailable because secure native loading is production-only. Post-deploy verification must confirm a real reading or safe unavailable state.
- One real website-service restart remains deferred until merged production deployment. Computer restart and shutdown remain unexecuted.
