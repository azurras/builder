# christopherbell.dev Command Center CPU Temperature and Uptime Spec

## Document Status

ready-for-execution

## Purpose

Fix the production Mission Control CPU-temperature provider so it cannot block the five-second telemetry collector or leak PowerShell processes, while giving the privileged Windows sensor enough time to initialize. Improve system and application uptime presentation by formatting raw seconds as human-readable minutes, hours, and days.

## Background

The deployed command center samples all host providers behind one two-second deadline. `LibreHardwareCpuTemperatureClient` opens a jPowerShell session, provisions a checksum-pinned LibreHardwareMonitor assembly, and runs a script that constructs, opens, queries, and closes a new LibreHardwareMonitor `Computer` every sample. The sensor work exceeds two seconds on this i5-13600K Windows host.

The timeout is not clean: production retained one Java-descendant PowerShell process approximately every seven seconds. The dashboard therefore shows `PROVIDER_TIMEOUT` while the service steadily accumulates abandoned processes. A direct official sensor scan completed within the longer default window and detected the CPU, but returned zero CPU temperatures without administrative privileges. Production already runs as SYSTEM, which is the correct privilege boundary for a final live test.

Uptime values currently reach the browser as seconds and render as values such as `32,072 s`, which is technically correct but poor for at-a-glance operations.

## Goals

- Keep the five-second command-center snapshot collection responsive regardless of CPU-sensor latency.
- Run CPU-temperature acquisition on a separate, slower refresh cadence with a longer bounded deadline.
- Terminate the entire sensor process tree on timeout, cancellation, shutdown, or abnormal completion.
- Preserve secure checksum-pinned, ACL-restricted native-library provisioning.
- Preserve last-good CPU temperature between slower refreshes and transient failures.
- Return an explicit unavailable reading until the first valid value and whenever no last-good value exists.
- Remove the recurring production PowerShell-process leak.
- Render uptime in concise human units while preserving raw seconds in the API.

## Non-Goals

- Do not install or depend on HWiNFO, Core Temp, Armoury Crate APIs, a new Windows service, or a remote monitoring agent.
- Do not weaken the native-library ACL or checksum boundary.
- Do not change the global five-second telemetry interval or the raw uptime API unit.
- Do not add persistent telemetry storage.
- Do not reboot or shut down the computer during validation.
- Do not use ACPI thermal-zone values as a substitute for CPU package temperature.

## Requirements

### CPU Temperature Execution

- Replace the jPowerShell session used by the command-center CPU provider with a one-shot, fixed-argument `ProcessBuilder` invocation of Windows PowerShell.
- Execute only a bundled, checksum-pinned PowerShell script from the ACL-restricted provisioned directory.
- Pass only the provisioned LibreHardwareMonitor DLL path as a fixed trusted argument; accept no request-controlled executable, path, script, or argument.
- Capture stdout and stderr concurrently with bounded output so a full pipe cannot deadlock the process.
- Use a CPU-sensor process timeout of 20 seconds by default, independent of the two-second general provider deadline.
- On timeout or interruption, destroy descendants and the root process, wait briefly, then force-destroy any survivors.
- Parse only one finite temperature greater than zero and no more than 125 degrees Celsius.
- Treat empty, zero, malformed, non-zero exit, and timeout results as unavailable without publishing fabricated data.

### Cached Refresh

- `readCelsius()` must return without waiting for the external sensor process.
- The first read schedules a refresh and returns unavailable.
- Refresh at most once every 30 seconds by default; do not launch another refresh while one is running.
- Publish a successful value atomically and keep it as last-good across transient failures.
- Mark the value unavailable only before any valid reading has ever succeeded; existing command-center stale semantics may indicate age separately.
- Shut down the refresh executor and terminate an active process when Spring destroys the client.

### Uptime Formatting

- Keep backend metric values and units as seconds.
- Format durations in the JavaScript display layer:
  - below 60 seconds: `42s`;
  - below one hour: `12m 34s`;
  - below one day: `8h 54m`;
  - one day or more: `3d 8h`.
- Apply the formatter to both system and application uptime.
- Preserve accessible labels and trend data.

### Observability and Safety

- Log one concise warning for sensor timeout or non-zero exit without emitting script bodies, library paths, or unbounded stderr.
- Do not surface recurring `PROVIDER_TIMEOUT` alerts from the general provider collector because the provider call itself must remain non-blocking.
- The metric may remain explicitly unavailable if the SYSTEM account cannot obtain a valid CPU reading.
- Deployment verification must measure PowerShell-process count across at least three refresh windows and prove it does not grow.

## Proposed Approach

Add a small process-runner boundary owned by the CPU-temperature client. The runner receives a fixed executable, fixed script path, fixed provisioned DLL path, and timeout; it owns stdout/stderr draining and process-tree cleanup. The client owns a single-thread refresh executor, an atomic last-good result, the next allowed refresh time, and one in-flight flag. The existing provider continues calling `readCelsius()`, but that call only reads cache and opportunistically schedules refresh work, so the global provider deadline remains irrelevant to native initialization time.

Provision `cpu-temperature.ps1` alongside the two existing DLL resources and verify its checksum before execution. The script constructs one LibreHardwareMonitor `Computer`, enables only CPU hardware, reads the maximum positive CPU temperature, prints one invariant-culture number, closes the computer in `finally`, and exits.

Add a pure `formatDuration(seconds)` JavaScript helper and route `seconds` units through it before generic number formatting.

## Modules Involved

- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClient.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- new focused process-runner class under the same metrics package if needed to keep lifecycle logic isolated
- `website/src/main/resources/lib/cpu-temperature.ps1`
- `website/src/main/resources/application.yml`
- `website/src/main/resources/static/js/lib/command-center.js`
- Java unit tests for the client, provisioner, and runner
- `website/src/test/js/command-center.test.js`
- command-center operations documentation

## Validation Plan

- Write failing tests before production edits.
- Verify exact fixed process arguments, output bounds, successful parsing, timeout tree termination, interrupted cleanup, non-zero exit, and no request-controlled input.
- Verify immediate cache return, one in-flight refresh, 30-second throttle, last-good retention, and shutdown.
- Verify duration boundary cases at 59, 60, 3,599, 3,600, 86,399, and 86,400 seconds.
- Run targeted tests, all command-center tests, JavaScript tests, full Java tests, and the complete Gradle build with isolated `GRADLE_USER_HOME` if necessary.
- Start a candidate on a non-8080 port and confirm the app remains responsive while the sensor refresh runs.
- Require all PR CI and CodeQL gates.
- After native auto-deployment, verify exact release SHA, service state, homepage 200, a valid CPU temperature or explicit hardware-level unavailable state, human uptime display, and a stable PowerShell-process count across at least 90 seconds.

## Rollback

Revert the spoke PR and redeploy the prior release through the native auto-deployer. The prior behavior is degraded and leaks processes, so rollback should be used only if the new runner affects service stability; otherwise keep the bounded unavailable behavior while investigating hardware access.

## Acceptance Criteria

- No additional PowerShell sensor processes accumulate during three production refresh windows.
- The main five-second snapshot remains responsive during CPU refresh.
- CPU temperature displays a valid positive Celsius value when SYSTEM hardware access succeeds; otherwise it displays an explicit unavailable state without `PROVIDER_TIMEOUT` from the general collector.
- System and application uptime display in human-readable minutes, hours, or days.
- Tests, full build, safe candidate runtime, CI, deployment, and live verification pass.

## Open Questions

None. Christopher approved the recommended self-contained approach and requested human-readable uptime.
