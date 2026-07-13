# christopherbell.dev Command Center CPU Temperature and Uptime Test Report

## Document Status

complete

## Story/Issue

Christopher's July 12, 2026 follow-up to fix the production CPU-temperature provider timeout/process leak and display system/application uptime in human units. Work record: `docs/work/2026-07-12-command-center-cpu-temperature-and-uptime.md`.

## Branch

- Spoke worktree: `A:\Projects\christopherbell.dev-worktrees\command-center-cpu-temperature`
- Branch: `codex/command-center-cpu-temperature`
- Base: `origin/main` at deployed release `eff05e36a27bdb84ebfddf8073ed1792880b4e57`
- Uptime commit: `82ab654b`
- Sensor-lifecycle commit: `98bf8dea`

## App / Environment

- Windows 11 desktop that also hosts native production.
- Candidate profiles: `local,deploy-smoke`.
- Candidate base URL: `http://127.0.0.1:8090`; production remained at `http://127.0.0.1:8080`.
- Candidate MongoDB database: `christopherbell_cpu_temperature_test`, dropped after verification.
- Candidate actions: `SIMULATED`; application scheduling disabled by `deploy-smoke`.
- Candidate sensor libraries disabled because the interactive non-elevated account cannot satisfy the production SYSTEM-only native-library ACL. The real privileged CPU reading remains a post-merge production check.

## Local Run Details

Exact start command:

```powershell
java -jar website\build\libs\website.jar --spring.profiles.active=local,deploy-smoke --server.port=8090 --spring.mongodb.uri=mongodb://127.0.0.1:27017/christopherbell_cpu_temperature_test --spring.mongodb.database=christopherbell_cpu_temperature_test --spring.data.mongodb.database=christopherbell_cpu_temperature_test --command-center.sensor-libraries-enabled=false --command-center.actions.mode=SIMULATED --command-center.commit-identifier=98bf8dea --command-center.log-path=A:/Projects/christopherbell.dev-worktrees/command-center-cpu-temperature/website/build/candidate-command-center.log
```

- Candidate Java PID: 40904.
- Started at 2026-07-12 21:01:09 CDT; Tomcat served port 8090 and startup completed in 4.266 seconds.
- Candidate stopped by Ctrl+C at 21:03:23 CDT; Spring logged graceful shutdown complete.
- Port 8090 closed, PID 40904 exited, and the temporary MongoDB database was dropped.
- Production port 8080 returned 200 before, during, and after candidate verification.

## Test Cases

| Test case | Result | Evidence |
| --- | --- | --- |
| TDD configuration RED | Pass | Test compilation failed only for missing 30-second refresh and 20-second timeout getters |
| TDD uptime RED | Pass | Expected `59s`; existing output was `59 s` |
| TDD sensor-cache/probe RED | Pass | Missing probe/cache APIs failed compilation before production code was added |
| Uptime boundaries | Pass | 59s, 1m 0s, 12m 34s, 59m 59s, 1h 0m, 8h 54m, 23h 59m, 1d 0h, and 3d 8h |
| Non-blocking CPU cache | Pass | First read returns unavailable and schedules one refresh; duplicate reads do not queue duplicates |
| Refresh and stale safety | Pass | 30-second throttle, last-good retention across one failure, expiration after two refresh intervals |
| Process safety | Pass | Fixed argument list, timeout cleanup contract, bounded/truncated output rejection, non-zero exit and invalid value rejection |
| Native resource safety | Pass | Script SHA-256 pinned; DLL/script checksum, ACL, link, and cleanup tests pass |
| Candidate homepage | Pass | HTTP 200, 3912 response bytes, `<title>CB \| Home</title>` |
| Candidate command-center shell | Pass | HTTP 200 and data-free HTML shell |
| Anonymous admin API boundary | Pass | Snapshot request returned 403 |
| Candidate browser asset | Pass | Served command-center JavaScript contains `formatDuration` |
| Candidate process stability | Pass | Java-descendant PowerShell count stayed 0 before and after 35 seconds |
| Production isolation | Pass | Production homepage stayed HTTP 200 |
| Automated regression | Pass | 72 suites, 581 Java tests, 0 failures/errors/skips; 116 JavaScript tests passed; full build passed |

## Data Sent

- `GET http://127.0.0.1:8090/`
- `GET http://127.0.0.1:8090/command-center`
- Anonymous `GET http://127.0.0.1:8090/api/admin/command-center/2026-07-12/snapshot`
- `GET http://127.0.0.1:8090/js/lib/command-center.js`
- `GET http://127.0.0.1:8080/` as the unchanged production smoke request
- Read-only WMI/CIM process-tree queries rooted at candidate PID 40904 before and after 35 seconds

No password, JWT, action challenge, machine action, computer restart, or shutdown was sent.

## Response Received

- Candidate homepage: status 200, body length 3912 bytes, expected title marker true.
- Candidate command-center shell: status 200; no `cpu.temperature` host data embedded in HTML.
- Anonymous candidate snapshot: status 403.
- Candidate JavaScript: status 200 and human duration formatter present.
- Production homepage: status 200.
- Candidate PowerShell descendants: 0 before and 0 after the observation window.
- Candidate startup log: active profiles `local` and `deploy-smoke`, MongoDB connected, Tomcat started on 8090, application started in 4.266 seconds.
- Candidate shutdown log: graceful shutdown complete.

## Pass / Fail

Overall safe local result: **PASS**.

The application stayed responsive on the alternate port, preserved admin API gating, served the new uptime formatter, did not spawn sensor PowerShell children with native sensors disabled, and left production untouched. Automated tests cover the new asynchronous/timeout behavior. The real CPU temperature and three-window production process-count stability check remain intentionally deferred to the SYSTEM deployment phase.

## Evidence

- Fresh full command: `./gradlew :website:test :website:build --rerun-tasks --no-daemon`.
- Java: 72 suites, 581 tests, 0 failures, 0 errors, 0 skipped.
- JavaScript: 116/116 passed.
- PowerShell parser: zero errors for `cpu-temperature.ps1`.
- Script SHA-256: `4d47eccfc836fe4d4ea771bf36b1b4fa4a4b91490b3f2ed8ab5e9c475687b2f3`.
- Node syntax checks passed for both command-center modules.
- `git diff --check` passed.
- Worktree was clean and two commits ahead of `origin/main` after verification.

## Bugs / Follow-ups

- A review-found issue was fixed before the report: an old cached CPU value could have appeared live indefinitely. Cache values now expire after two refresh intervals without another success.
- The interactive account cannot validate the real CPU sensor because the native-library directory deliberately permits only SYSTEM and Administrators under the production ACL boundary.
- Production verification must confirm either a positive CPU Celsius value or explicit unavailable behavior without general `PROVIDER_TIMEOUT`.
- Production verification must prove Java-descendant PowerShell process count remains stable across at least three 30-second refresh windows.
