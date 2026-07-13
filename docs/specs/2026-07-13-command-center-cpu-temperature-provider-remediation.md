# christopherbell.dev Command Center CPU Temperature Provider Remediation

## Document Status

ready-for-review

## Purpose

Replace the command center's legacy WinRing0-based CPU-temperature dependency with a verified modern provider path that Windows Defender does not flag, while keeping the production website available, fail-closed, and recoverable throughout installation and rollout.

## Background

The July 12 CPU-temperature work successfully removed the telemetry-path timeout and recurring PowerShell child-process leak, preserved an explicit unavailable state, and changed system/application uptime presentation from raw seconds to concise hours and days. Production deployment then exposed a separate provider problem: the bundled `jLibreHardwareMonitor` 1.0.6 artifact contains `LibreHardwareMonitorLib` 0.9.4.0 and exercises the legacy WinRing0 driver path.

Microsoft Defender detected that path as `VulnerableDriver:WinNT/Winring0`, with evidence that the threat executed. The service also entered a restart loop while an orphan Java process retained port 8080. Emergency containment replaced the installed service startup script with an otherwise identical copy that sets `COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED=false`, stopped only the verified service process tree, and restarted the website. The contained production state returned HTTP 200 with the expected homepage marker, and the sensor-library flag remains disabled.

No PawnIO software has been installed. The downloaded audit copy of the official PawnIO 2.2.0 installer was not executed. Its 3,410,960-byte SHA-256 is `1F519A22E47187F70A1379A48CA604981C4FCF694F4E65B734AAA74A9FBA3032`, matching the digest published by the official GitHub release. Windows reports a valid Authenticode signature from `namazso.eu`, thumbprint `F380DCC9F706E2756A5047B832FFE719E1BC35F5`, with a Microsoft timestamp.

LibreHardwareMonitor 0.9.6 is the current official release and uses PawnIO modules for low-level hardware access. Its standard .NET Framework release ZIP has published and locally reproduced SHA-256 `086D9F1B5A99E643EDC2CFAAAC16051685B551E4C5AC0B32A57C58C0E529C001`. The contained `LibreHardwareMonitorLib.dll` identifies as version 0.9.6.0 and has SHA-256 `6EBC194316536BA61AF5BE24508AD9FCBB2ECC685E716C12E787C79530F66BF0`; the library itself is not Authenticode-signed, so release-archive provenance and exact checksum pinning are required.

## Goals

- Remove the legacy WinRing0-based library and transitive packaging path from the website.
- Make the emergency sensor-disable containment a durable, checked-in production default until the replacement is validated.
- Use only the official PawnIO 2.2.0 installer and official LibreHardwareMonitor 0.9.6 release artifacts, with exact source, hash, and signature verification.
- Preserve the existing bounded, one-shot PowerShell process and non-blocking cached CPU-temperature architecture.
- Keep hardware sensor access limited to the SYSTEM production boundary and fixed, server-owned inputs.
- Enable CPU temperature only after alternate-port and production acceptance checks prove a valid reading without Defender activity, process leakage, port conflicts, or service instability.
- Fail closed to explicit CPU-temperature unavailable state without affecting CPU usage, RAM, GPU, logs, uptime, or other command-center features.
- Provide deterministic rollback and uninstall/disable procedures.

## Non-Goals

- Do not suppress, exclude, allow-list, or weaken Microsoft Defender.
- Do not restore, rename, or retain WinRing0 binaries.
- Do not auto-approve an unverified publisher, artifact, driver identity, or installer result.
- Do not expose PawnIO to non-administrator accounts.
- Do not add a LibreHardwareMonitor GUI or permanent monitoring service.
- Do not replace the bounded sensor probe with a request-driven command path.
- Do not reboot, shut down, or power-cycle the host automatically.
- Do not change the already-correct uptime formatting or unrelated command-center features.

## Requirements

### Immediate and Durable Containment

- Production must keep `COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED=false` until every enablement gate passes.
- The checked-in Windows service startup template must carry the safe disabled default so `install`, redeploy, or service repair cannot silently re-enable the flagged path.
- Deployment verification must assert the intended sensor-enabled state instead of relying on an undocumented manual edit.
- The pre-containment startup-script backup may remain for forensic comparison, but it must never be used to restore WinRing0 execution.

### Legacy Dependency Removal

- Remove `io.github.pandalxb:jLibreHardwareMonitor:1.0.6` from the Gradle runtime graph.
- Remove or replace all resource extraction logic, version labels, hashes, tests, and documentation tied to the 0.9.4.0 DLL.
- Prove the built application artifact does not contain the legacy DLL, WinRing0 driver names, or the obsolete dependency.
- Preserve checksum-pinned, ACL-restricted extraction for the replacement library and script.

### Verified PawnIO Installation

- Download only `PawnIO_setup.exe` from the official `namazso/PawnIO.Setup` 2.2.0 GitHub release URL.
- Require the exact published SHA-256 and a valid Authenticode chain whose publisher and certificate thumbprint match the reviewed values.
- Scan the installer with Microsoft Defender before execution and reject any detection.
- Run the installer only from an elevated, non-request-controlled operations command.
- Treat every non-success exit code explicitly. If the installer reports reboot required, stop with sensors disabled and request separate reboot approval.
- After installation, verify the uninstall registry version, installed driver/service identity, binary location, startup state, signature chain, device availability, and administrator-only access.
- Run a post-install Defender scan and query current detections before starting any sensor probe.
- Never add a Defender exclusion as part of installation or recovery.

### LibreHardwareMonitor Integration

- Use the official LibreHardwareMonitor 0.9.6 .NET Framework release archive and pin both archive and extracted library hashes.
- Package only the minimum reviewed runtime files required for the CPU-only PowerShell probe.
- Keep CPU-only hardware enablement; do not enumerate storage, motherboard, network, or unrelated devices.
- Continue passing only the provisioned script and library paths through the existing fixed PowerShell argument list.
- Continue parsing a single finite Celsius value greater than zero and no more than 125.
- Continue concurrent bounded output capture, full process-tree termination, cached refresh, last-good expiration, and lifecycle cleanup.
- Detect missing or unhealthy PawnIO before probing and return explicit unavailable state without repeatedly launching doomed processes.

### Enablement Gates

- The default branch, production startup template, and deployed service must remain sensor-disabled through code review, CI, merge, and initial deployment.
- Validate the provider first in a controlled elevated harness, then in a candidate app on a non-8080 port while production remains on 8080 with sensors disabled.
- Require at least three CPU refresh windows with a plausible positive temperature, no PowerShell accumulation, no orphan Java process, no port conflict, no Defender detection, and no service instability.
- Re-run the full automated build and security-focused diff review before publication.
- Enable production through a documented, reversible configuration change only after all gates pass.
- Observe production through at least three additional refresh windows and verify the exact deployed release, service, homepage body marker, command-center reading, and process tree.

### Failure and Recovery Behavior

- Any checksum, signature, installer, driver, Defender, probe, timeout, or service-health failure must leave sensors disabled.
- CPU temperature must show an explicit unavailable/degraded reason without causing the general telemetry collector to report `PROVIDER_TIMEOUT`.
- Recovery commands must target only verified PawnIO, ChristopherBellDev, Java, or PowerShell identities and process relationships.
- Rollback must disable the provider first, restore the prior known-good application release if necessary, and uninstall PawnIO only through its verified uninstall path.
- The website must remain usable even if PawnIO is absent, disabled, unhealthy, or removed.

## Proposed Approach

Use the existing one-shot sensor architecture with a provider replacement rather than introducing a monitoring service. Add a guarded Windows operations workflow that downloads and verifies the pinned official PawnIO installer, performs Defender checks, installs with explicit exit-code handling, and validates the installed driver identity. Keep this workflow outside HTTP request handling and require elevation.

Replace the old Maven wrapper dependency with explicitly provisioned LibreHardwareMonitor 0.9.6 runtime resources derived from the pinned official release. The Java provisioner continues creating an ACL-restricted fresh directory owned by SYSTEM, verifies every extracted resource before and after ACL hardening, and supplies fixed paths to the bounded PowerShell probe. The PowerShell script checks PawnIO availability, enables only CPU hardware, samples one maximum CPU temperature, and always closes the computer object.

The checked-in service startup script initially forces sensors off. Installation and deployment do not automatically enable them. A separate guarded enable operation may change the production configuration only after installation, Defender, elevated harness, alternate-port, automated, and CI evidence are all green. Any failed gate returns to or retains the disabled state.

## Alternatives Considered

### Separate LibreHardwareMonitor Service and WMI Consumer

This isolates low-level access from the Java process, but adds another long-running elevated service, lifecycle, update channel, log source, failure mode, and attack surface. It is not justified when the existing bounded one-shot boundary can use PawnIO directly.

### Permanently Leave CPU Temperature Unavailable

This is the lowest-risk fallback and remains acceptable if PawnIO or the host fails validation. It does not meet the desired CPU-temperature capability, so it is the fallback rather than the primary implementation.

## Files and Modules Involved

- `website/build.gradle.kts`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbe.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClient.java`
- `website/src/main/resources/lib/cpu-temperature.ps1`
- replacement sensor runtime resources and their focused tests
- `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- `ops/production/windows/modules/Production.Install.psm1`
- `ops/production/windows/modules/Production.Operations.psm1`
- `ops/production/windows/prod.ps1`
- Windows production Pester tests and command-center Java tests
- command-center and production operations documentation

## Security Boundaries

- Browser and API clients cannot choose executables, scripts, DLLs, installer URLs, hashes, paths, arguments, driver settings, or enablement state.
- Admin authentication continues gating command-center data; no remote endpoint installs, updates, enables, or uninstalls PawnIO.
- Only the local elevated operations workflow may mutate the driver or production sensor setting.
- SYSTEM and Administrators remain the only principals with write access to provisioned sensor files.
- Supply-chain trust is anchored to reviewed official release URLs, exact hashes, publisher validation where available, and the repository's pinned configuration.
- Defender remains an independent blocking control before and after installation and during acceptance.

## Validation Plan

1. Add failing tests for the safe startup default, legacy-dependency absence, pinned artifact metadata, invalid hash/signature rejection, installer exit handling, reboot-required behavior, and fail-closed operations.
2. Add failing tests for PawnIO-unavailable probe behavior and the replacement resource hashes/version.
3. Implement the minimum production changes needed to pass each test.
4. Run focused Java, JavaScript, PowerShell/Pester, dependency, packaging, and static security checks.
5. Run the complete Gradle build with an isolated `GRADLE_USER_HOME` when required.
6. Run a security diff scan before publication.
7. Verify the official installer with Defender and Windows signature tools, then install only after all pre-install gates pass.
8. If no reboot is required, validate a direct elevated CPU-only probe and record actual Celsius output and process cleanup.
9. Run the application on a non-production port with isolated data and sensors enabled while production remains sensor-disabled on 8080.
10. Observe at least three refresh windows and record response markers, readings, process counts, ports, service state, driver state, and Defender state.
11. Publish a pull request, require all CI and CodeQL gates, merge, and let native Windows deployment select the exact merge SHA.
12. Verify the initial production deployment remains sensor-disabled, then perform a separately recorded enablement only if every gate is green.
13. Observe production for at least three refresh windows and record full acceptance evidence in a Builder test report.

## Rollback

1. Set or retain the production sensor-library flag as disabled.
2. Restart only the ChristopherBellDev service through the guarded production operations path and verify homepage HTTP 200 plus expected body marker.
3. If application stability regressed, roll back to the prior known-good release while preserving the disabled flag.
4. If PawnIO caused a Defender or driver-health issue, use its verified uninstall command; do not delete driver files manually.
5. If uninstall reports reboot required, stop and request explicit approval before rebooting.
6. Confirm PawnIO registry/service/device removal, no active Defender detection, stable website service state, and no orphan process tree.

## Acceptance Criteria

- Defender does not report WinRing0 or PawnIO-related active threats before, during, or after acceptance.
- The application runtime and distribution contain no `jLibreHardwareMonitor` 1.0.6, LibreHardwareMonitor 0.9.4.0, or WinRing0 artifact.
- The official pinned PawnIO 2.2.0 install is verified, healthy, administrator-only, and reversible, or the feature remains safely disabled.
- The official pinned LibreHardwareMonitor 0.9.6 CPU-only probe returns a plausible positive Celsius value under the production privilege boundary.
- No PowerShell or Java child process accumulates across at least three candidate and three production refresh windows.
- ChristopherBellDev remains Running/Automatic, owns port 8080 without conflicts, and returns HTTP 200 with `<title>CB | Home</title>`.
- CPU temperature never blocks the general telemetry snapshot and fails closed to explicit unavailable state.
- The startup template and deployment tooling cannot silently restore the legacy provider.
- No automatic reboot, shutdown, Defender exclusion, or arbitrary process termination occurs.
- Automated tests, full build, security review, PR CI/CodeQL, deployment, live browser verification, Builder test report, closure, and session memory complete successfully.

## Open Questions

None. Christopher approved the recommended direct PawnIO plus LibreHardwareMonitor 0.9.6 design and the rule to stop before any required reboot.
