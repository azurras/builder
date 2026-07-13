# christopherbell.dev Mobile Command Center Production Verification

## Document Status

complete

## Story/Issue

Direct July 12, 2026 request for an administrator-only mobile command center for the Windows desktop hosting `christopherbell.dev`. Hub work record: `docs/work/2026-07-12-christopherbell-dev-mobile-command-center.md`.

## Branch

- Feature delivery: PR #1199, merged as `3c52c1e486e296386b079d96aea8df0704172fe1`.
- SYSTEM deployment compatibility: PR #1200, merged as `79f37213f99acfe7085b5d93d24a2b030b0bcafe`, and PR #1201, merged/deployed as `729e0e7cf442dd7b85530e87219f73c269175435`.
- Production readability regression fix: branch `codex/mobile-command-center-layout`, commit `2446d663`, PR #1202, merged/deployed as `eff05e36a27bdb84ebfddf8073ed1792880b4e57`.

## App / Environment

- Native Windows 11 production host running Java 25.0.3, MongoDB, the `ChristopherBellDev` Windows service, and cloudflared.
- Spring profile `prod`, production URL `http://localhost:8080`, authenticated UI `http://localhost:8080/command-center`.
- Release directory `C:\ProgramData\christopherbell.dev\releases\eff05e36a27bdb84ebfddf8073ed1792880b4e57` selected through the `current` junction.
- Auto-deploy runs under the production service account and kept the previous release live while building the replacement.
- Destructive computer restart and shutdown features remained disabled by default and were not executed.

## Local Run Details

The already-running production app was exercised in place after safe candidate verification on port 8090 and CI validation. The native auto-deployer detected each merged release, built it under the production service account, atomically changed the release junction, and restarted only the website service. No manual `java -jar` process was left running.

For the final release, `auto-deploy.json` reported `remoteSha`, `attemptedSha`, and `successfulSha` as `eff05e36a27bdb84ebfddf8073ed1792880b4e57`, with `failedSha` and `error` null. The website wrapper service was running as PID 2212 and Java listened on port 8080 as PID 35832. The application log recorded Java PID 35832, profile `prod`, Tomcat on port 8080, and `Started Application` in 7.082 seconds.

A separate real website-only restart was exercised through Mission Control on release `729e0e7c`: Java PID 6788 stopped and Java PID 36664 started; the wrapper service PID changed to 35784. Wrapper logs showed the stop at 2026-07-12 20:01:14 CDT and restart at 20:01:15 CDT. Port 8080 returned HTTP 200 after the restart.

## Test Cases

| Test case | Result | Evidence |
| --- | --- | --- |
| CI and merge gate for final regression fix | Pass | CodeQL and actions/java-kotlin/javascript-typescript analyses passed; macOS, Ubuntu, and Windows Java 25 builds passed for PR #1202 |
| Native auto-deployment | Pass | `successfulSha=eff05e36...`; release junction targets the exact SHA; no deployment error |
| Production homepage | Pass | `GET http://localhost:8080/` returned 200, 3912 bytes, and `<title>CB \| Home</title>` |
| Admin access | Pass | Existing authenticated ADMIN session loaded `/command-center`; anonymous and regular-user denial was already covered in the candidate report |
| Live telemetry | Pass with known degradation | CPU usage, RAM, disk, network, GPU usage/temperature/power/memory, Mongo connectivity, service state, port, response time, and uptimes updated live |
| CPU temperature | Pass for safe-unavailable behavior | Dashboard displayed `DEGRADED` and `PROVIDER_TIMEOUT — LibreHardwareCpuTemperatureProvider exceeded its sampling timeout.` rather than a fabricated value |
| Delayed production logs | Pass | UI streamed the final release startup records, including PID, prod profile, Mongo connection, Tomcat port, and application startup |
| Website-only restart | Pass | Protected `RESTART_SITE` produced accepted/launched audit rows in WINDOWS mode and changed Java PID while restoring HTTP 200 |
| Metric readability regression | Pass | Bytes render as GiB/TiB and rates as KiB/s or MiB/s; each of 23 cards has one computed grid column; values use `overflow-wrap:anywhere`; page has no horizontal overflow |
| Desktop visual inspection | Pass | Live screenshot shows labels, compact values, states, and sparklines without the previous overlap |
| Mobile layout regression | Pass | Existing 390x844 browser verification remained green; final 115/115 JavaScript tests cover byte/rate formatting and card layout |
| Computer restart/shutdown safety | Pass | Controls remain step-up protected and disabled by production configuration; neither action was executed |

## Data Sent

- Browser navigation and authenticated refresh: `GET /command-center` using the existing ADMIN browser session. No password was read, logged, or persisted during final verification.
- Telemetry/log polling initiated by the page against the versioned administrator APIs.
- Homepage smoke request: `GET http://localhost:8080/` with no authentication.
- One earlier protected `RESTART_SITE` flow submitted a fresh server challenge, the authenticated administrator password, and the exact confirmation phrase. The password and challenge value are intentionally omitted.
- Read-only operating-system queries inspected the `ChristopherBellDev` service, port 8080 listener, release junction, and auto-deploy state.

No request was sent for `RESTART_COMPUTER` or `SHUTDOWN_COMPUTER`.

## Response Received

- Homepage: status 200, response body length 3912 bytes, expected title marker present.
- Mission Control: status connected with a sample age of approximately five seconds and 23 metric cards.
- Example compact values observed live: disk activity `1.5 MiB/s`, disk free `3.4 TiB`, disk used `3.9 TiB`, memory total `31.7 GiB`, memory used `22.1 GiB`, and network received `242.2 KiB/s`.
- Computed layout response: `gridTemplates=['290.75px']`, every sampled value had equal `clientWidth` and `scrollWidth`, `overflowWrap='anywhere'`, and `pageHorizontalOverflow=false`.
- Delayed logs included `Starting Application using Java 25.0.3 with PID 35832`, active profile `prod`, Tomcat port 8080, and `Started Application in 7.082 seconds`.
- Restart audit query returned `COMMAND_CENTER_ACTION_ACCEPTED` and `COMMAND_CENTER_ACTION_LAUNCHED` for `RESTART_SITE`, mode `WINDOWS`.
- CPU temperature response explicitly reported `PROVIDER_TIMEOUT`; all other primary requested telemetry was live.

## Pass / Fail

Overall production verification result: **PASS WITH ONE KNOWN DEGRADED SENSOR**.

The command center is deployed and usable both beside and away from the host. Admin gating, telemetry, delayed logs, safe website restart, responsive layout, and conservative power-action defaults passed. The CPU temperature provider timeout is visible and non-misleading but still needs a provider-level follow-up if a live CPU temperature is required.

## Evidence

- Final production SHA: `eff05e36a27bdb84ebfddf8073ed1792880b4e57`.
- PRs: #1199, #1200, #1201, and #1202 in `azurras/christopherbell.dev`.
- Final local regression run: 576 Java tests plus 115 JavaScript tests; `BUILD SUCCESSFUL in 1m 58s`.
- PR #1202 checks: all three CodeQL analyses, aggregate CodeQL, and Java 25 builds on macOS, Ubuntu, and Windows passed.
- Production state file: `C:\ProgramData\christopherbell.dev\state\auto-deploy.json`.
- Production release junction: `C:\ProgramData\christopherbell.dev\current` -> exact `eff05e36...` release.
- Mobile candidate screenshot: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center\.superpowers\runtime\command-center-mobile-viewport.png`.
- Desktop candidate screenshot: `A:\Projects\christopherbell.dev-worktrees\mobile-command-center\.superpowers\runtime\command-center-desktop.png`.
- Final live authenticated browser tab retained as the deliverable at `http://localhost:8080/command-center`.

## Bugs / Follow-ups

- CPU temperature remains unavailable because `LibreHardwareCpuTemperatureProvider` exceeds its sampling timeout under the hardened production path. The dashboard correctly reports this as degraded; investigate the provider/driver boundary separately.
- Application commit remains `Unavailable` in the dashboard despite release-level SHA evidence from the deployer. Injecting the release SHA into application metadata would improve at-a-glance diagnosis.
- The delayed log surfaced a pre-existing OpenStreetMap restaurant import duplicate-key error for normalized name `aama's kitchen`. It did not prevent startup or Mission Control operation and is outside this feature's scope.
- SpringDoc production warnings remain pre-existing and outside this feature's scope.
- A real computer restart or shutdown was intentionally not tested. Those actions remain disabled until explicitly enabled after a separate operational review.
