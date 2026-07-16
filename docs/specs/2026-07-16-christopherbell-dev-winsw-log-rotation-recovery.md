# christopherbell.dev WinSW Log Rotation Recovery

## Document Status

`ready-for-execution`

## Purpose

Restore `ChristopherBellDev` to a healthy, continuously managed Windows service before enabling the command center CPU-temperature provider, and prevent the midnight WinSW log-rotation failure from recurring.

## Background

Production still returns HTTP `200` on port 8080, but Windows reports the `ChristopherBellDev` service as stopped with exit code `1067`. Port 8080 is owned by a SYSTEM-session `java.exe` whose parent is a SYSTEM-session `pwsh.exe`, while Service Control Manager has repeatedly attempted and failed to restart the wrapper.

The first unexpected termination occurred at exactly `2026-07-13 00:00:02`, immediately after the configured WinSW `roll-by-size-time` boundary of `00:00:00`. Subsequent WinSW events repeatedly report that the log cannot be rolled because another process is using it. The current `roll-by-size-time` configuration matches the open upstream WinSW defect in which time-based rotation during active console output closes the logging stream, deadlocks or detaches the wrapped application, and leaves the service wrapper unhealthy.

The orphaned Java process has kept the public site reachable, but it is not acceptable production state: Windows service recovery, startup verification, release switching, and sensor enablement all depend on the service owning its process tree correctly.

## Goals

- Replace the unsafe combined time-and-size WinSW rotation mode with bounded size-only rotation.
- Add regression coverage that rejects `roll-by-size-time` and its midnight trigger.
- Preserve the existing command-center log path and bounded retention.
- Deploy the fix through the guarded native Windows workflow.
- Recover production by terminating only the verified orphaned website process tree and restarting the `ChristopherBellDev` service.
- Prove that the service remains `Running`, owns port 8080, serves the expected homepage, and does not resume a restart loop.
- Resume PawnIO status verification and CPU-temperature enablement only after service stability is established.

## Non-Goals

- Do not upgrade to a WinSW prerelease.
- Do not change MongoDB or cloudflared.
- Do not reboot or power off the computer.
- Do not weaken ProgramData ACLs, Defender settings, installer verification, or sensor fail-closed behavior.
- Do not terminate unrelated Java or PowerShell processes.
- Do not enable sensors while the website is running outside the Windows service.

## Requirements

### Service Logging

- `ChristopherBellDev.xml` must use WinSW `roll-by-size`.
- The size threshold must remain 10 MiB (`10485760` bytes).
- Retention must be explicitly bounded to seven rolled files.
- The configuration must not contain `roll-by-size-time`, `autoRollAtTime`, or a time-based filename pattern.
- The active output filename must remain `C:\ProgramData\christopherbell.dev\logs\ChristopherBellDev.out.log` so the command center continues reading the same protected log.

### Automated Validation

- A Pester regression must parse the real service XML.
- The regression must fail against the current combined rotation configuration.
- The regression must prove size-only mode, the 10 MiB threshold, seven-file retention, and absence of time-rotation elements.
- The complete Windows production Pester suite and full Gradle build must pass.
- Independent review and all GitHub CI gates must pass before merge.

### Production Recovery

- Refresh the installed production service XML from the merged source through the supported elevated production installer or equivalent guarded operation.
- Stop the service recovery loop before process cleanup.
- Resolve port 8080 to its owning process and verify the tree is the expected `java.exe` child of the production `Start-ChristopherBellDev.ps1` PowerShell process.
- Terminate only that verified orphan tree.
- Start `ChristopherBellDev` and verify its service PID/process tree owns the new listener.
- Verify `MongoDB`, `ChristopherBellDev`, and `cloudflared` are all `Running` and `Automatic`.
- Verify local and public homepage responses return `200` with `<title>CB | Home</title>`.
- Observe the service for at least two minutes and confirm the restart-event count does not increase.

### Sensor Continuation

- Confirm PawnIO Windows product version `2.2.0.0`, running driver, valid driver signature, verified uninstall registration, and zero active WinRing0/PawnIO Defender threats.
- Confirm `sensorLibrariesEnabled` remains `false` until all service recovery gates pass.
- Enable sensors through the guarded production command only after recovery.
- Run `verify-startup` and prove a plausible direct CPU-temperature reading.
- Observe at least three 30-second command-center refresh windows with no accumulating PowerShell children.
- If enablement or direct verification fails, restore `sensorLibrariesEnabled=false` and keep the website service healthy.

## Proposed Approach

### Recommended: Size-Only WinSW Rotation

Change only the service XML logging strategy from combined time-and-size rotation to size-only rotation with seven retained files. This preserves bounded logs and avoids the upstream time-boundary failure without changing the pinned WinSW binary or the command-center log contract.

### Rejected: Append-Only Logs

Append-only logging avoids rotation failures but allows unbounded disk growth and weakens production safety.

### Rejected: WinSW Upgrade

Upgrading to a newer or prerelease WinSW expands the trust, compatibility, checksum, deployment, and rollback surface. The upstream issue remains open, so an upgrade does not provide evidence that combined time rotation is safe.

## Files and Modules

- Spoke service definition: `ops/production/windows/service/ChristopherBellDev.xml`
- Spoke regression suite: `ops/production/windows/tests/Production.Command.Tests.ps1`
- Spoke operations documentation: `docs/operations/windows-production.md`
- Existing production installation path: `ops/production/windows/modules/Production.Install.psm1`
- Existing sensor lifecycle: `ops/production/windows/modules/Production.Sensors.psm1`

## Validation Plan

1. Add the failing XML regression and record the expected failure against `roll-by-size-time`.
2. Apply the minimal service XML and documentation change.
3. Run focused Pester, the full Windows production suite, and the full Gradle build with an isolated Gradle home.
4. Request independent review.
5. Push a dedicated branch, open a draft PR, wait for all required checks, and squash-merge.
6. Perform the guarded elevated production recovery and verify process ownership, services, local/public HTTP, and restart-loop stability.
7. Verify PawnIO and Defender state, enable sensors, run startup verification, and observe temperature/process stability.
8. Save a production test report, update the active Builder work record, close the work when all gates pass, and save session memory.

## Rollback

- Before sensor enablement, rollback consists of keeping `sensorLibrariesEnabled=false` and restoring the prior service XML only if size-only logging fails validation.
- If the new release cannot start after orphan cleanup, use the existing production release rollback command while preserving MongoDB and cloudflared.
- If sensor enablement fails, immediately disable sensors and restart only `ChristopherBellDev`.
- PawnIO remains installed unless a verified provider or Defender problem requires its registered uninstaller under explicit operator control.

## Open Questions

None. Christopher approved the recommended size-only rotation and guarded recovery sequence on July 16, 2026.
