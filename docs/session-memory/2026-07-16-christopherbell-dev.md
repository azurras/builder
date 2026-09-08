# 2026-07-16 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/specs/2026-07-16-christopherbell-dev-winsw-log-rotation-recovery.md](#source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md)
- [docs/specs/2026-07-16-command-center-cpu-temperature-selection-and-commit.md](#source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md)
- [docs/specs/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md](#source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md)

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md"></a>
## 2026-07-16 | specs | christopherbell.dev WinSW Log Rotation Recovery

Original source: `docs/specs/2026-07-16-christopherbell-dev-winsw-log-rotation-recovery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `417a62a6c523d733c488ca820c3fd5b5d622250c6b80b6855549149c59f0a8c0`.

<!-- migrated-source: docs/specs/2026-07-16-christopherbell-dev-winsw-log-rotation-recovery.md -->
<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--christopherbelldev-winsw-log-rotation-recovery"></a>
### christopherbell.dev WinSW Log Rotation Recovery

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--document-status"></a>
#### Document Status

`ready-for-execution`

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--purpose"></a>
#### Purpose

Restore `ChristopherBellDev` to a healthy, continuously managed Windows service before enabling the command center CPU-temperature provider, and prevent the midnight WinSW log-rotation failure from recurring.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--background"></a>
#### Background

Production still returns HTTP `200` on port 8080, but Windows reports the `ChristopherBellDev` service as stopped with exit code `1067`. Port 8080 is owned by a SYSTEM-session `java.exe` whose parent is a SYSTEM-session `pwsh.exe`, while Service Control Manager has repeatedly attempted and failed to restart the wrapper.

The first unexpected termination occurred at exactly `2026-07-13 00:00:02`, immediately after the configured WinSW `roll-by-size-time` boundary of `00:00:00`. Subsequent WinSW events repeatedly report that the log cannot be rolled because another process is using it. The current `roll-by-size-time` configuration matches the open upstream WinSW defect in which time-based rotation during active console output closes the logging stream, deadlocks or detaches the wrapped application, and leaves the service wrapper unhealthy.

The orphaned Java process has kept the public site reachable, but it is not acceptable production state: Windows service recovery, startup verification, release switching, and sensor enablement all depend on the service owning its process tree correctly.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--goals"></a>
#### Goals

- Replace the unsafe combined time-and-size WinSW rotation mode with bounded size-only rotation.
- Add regression coverage that rejects `roll-by-size-time` and its midnight trigger.
- Preserve the existing command-center log path and bounded retention.
- Deploy the fix through the guarded native Windows workflow.
- Recover production by terminating only the verified orphaned website process tree and restarting the `ChristopherBellDev` service.
- Prove that the service remains `Running`, owns port 8080, serves the expected homepage, and does not resume a restart loop.
- Resume PawnIO status verification and CPU-temperature enablement only after service stability is established.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--non-goals"></a>
#### Non-Goals

- Do not upgrade to a WinSW prerelease.
- Do not change MongoDB or cloudflared.
- Do not reboot or power off the computer.
- Do not weaken ProgramData ACLs, Defender settings, installer verification, or sensor fail-closed behavior.
- Do not terminate unrelated Java or PowerShell processes.
- Do not enable sensors while the website is running outside the Windows service.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--service-logging"></a>
##### Service Logging

- `ChristopherBellDev.xml` must use WinSW `roll-by-size`.
- The size threshold must be 10 MiB, expressed in WinSW 2.12.0's documented
  KiB units as `10240`.
- Retention must be explicitly bounded to seven rolled files.
- The configuration must not contain `roll-by-size-time`, `autoRollAtTime`, or a time-based filename pattern.
- The active output filename must remain `C:\ProgramData\christopherbell.dev\logs\ChristopherBellDev.out.log` so the command center continues reading the same protected log.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--automated-validation"></a>
##### Automated Validation

- A Pester regression must parse the real service XML.
- The regression must fail against the current combined rotation configuration.
- The regression must prove size-only mode, the 10 MiB threshold, seven-file retention, and absence of time-rotation elements.
- The complete Windows production Pester suite and full Gradle build must pass.
- Independent review and all GitHub CI gates must pass before merge.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--production-recovery"></a>
##### Production Recovery

- Refresh the installed production service XML from the merged source through the supported elevated production installer or equivalent guarded operation.
- Stop the service recovery loop before process cleanup.
- Resolve port 8080 to its owning process and verify the tree is the expected `java.exe` child of the production `Start-ChristopherBellDev.ps1` PowerShell process.
- Terminate only that verified orphan tree.
- Start `ChristopherBellDev` and verify its service PID/process tree owns the new listener.
- Verify `MongoDB`, `ChristopherBellDev`, and `cloudflared` are all `Running` and `Automatic`.
- Verify local and public homepage responses return `200` with `<title>CB | Home</title>`.
- Observe the service for at least two minutes and confirm the restart-event count does not increase.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--sensor-continuation"></a>
##### Sensor Continuation

- Confirm PawnIO Windows product version `2.2.0.0`, running driver, valid driver signature, verified uninstall registration, and zero active WinRing0/PawnIO Defender threats.
- Confirm `sensorLibrariesEnabled` remains `false` until all service recovery gates pass.
- Enable sensors through the guarded production command only after recovery.
- Run `verify-startup` and prove a plausible direct CPU-temperature reading.
- Observe at least three 30-second command-center refresh windows with no accumulating PowerShell children.
- If enablement or direct verification fails, restore `sensorLibrariesEnabled=false` and keep the website service healthy.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--proposed-approach"></a>
#### Proposed Approach

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--recommended-size-only-winsw-rotation"></a>
##### Recommended: Size-Only WinSW Rotation

Change only the service XML logging strategy from combined time-and-size rotation to size-only rotation with seven retained files. This preserves bounded logs and avoids the upstream time-boundary failure without changing the pinned WinSW binary or the command-center log contract.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--rejected-append-only-logs"></a>
##### Rejected: Append-Only Logs

Append-only logging avoids rotation failures but allows unbounded disk growth and weakens production safety.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--rejected-winsw-upgrade"></a>
##### Rejected: WinSW Upgrade

Upgrading to a newer or prerelease WinSW expands the trust, compatibility, checksum, deployment, and rollback surface. The upstream issue remains open, so an upgrade does not provide evidence that combined time rotation is safe.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--files-and-modules"></a>
#### Files and Modules

- Spoke service definition: `ops/production/windows/service/ChristopherBellDev.xml`
- Spoke regression suite: `ops/production/windows/tests/Production.Command.Tests.ps1`
- Spoke operations documentation: `docs/operations/windows-production.md`
- Existing production installation path: `ops/production/windows/modules/Production.Install.psm1`
- Existing sensor lifecycle: `ops/production/windows/modules/Production.Sensors.psm1`

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--validation-plan"></a>
#### Validation Plan

1. Add the failing XML regression and record the expected failure against `roll-by-size-time`.
2. Apply the minimal service XML and documentation change.
3. Run focused Pester, the full Windows production suite, and the full Gradle build with an isolated Gradle home.
4. Request independent review.
5. Push a dedicated branch, open a draft PR, wait for all required checks, and squash-merge.
6. Perform the guarded elevated production recovery and verify process ownership, services, local/public HTTP, and restart-loop stability.
7. Verify PawnIO and Defender state, enable sensors, run startup verification, and observe temperature/process stability.
8. Save a production test report, update the active Builder work record, close the work when all gates pass, and save session memory.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--rollback"></a>
#### Rollback

- Before sensor enablement, rollback consists of keeping `sensorLibrariesEnabled=false` and restoring the prior service XML only if size-only logging fails validation.
- If the new release cannot start after orphan cleanup, use the existing production release rollback command while preserving MongoDB and cloudflared.
- If sensor enablement fails, immediately disable sensors and restart only `ChristopherBellDev`.
- PawnIO remains installed unless a verified provider or Defender problem requires its registered uninstaller under explicit operator control.

<a id="source-docs-specs-2026-07-16-christopherbell-dev-winsw-log-rotation-recovery-md--open-questions"></a>
#### Open Questions

None. Christopher approved the recommended size-only rotation and guarded recovery sequence on July 16, 2026.

<!-- /migrated-source: docs/specs/2026-07-16-christopherbell-dev-winsw-log-rotation-recovery.md -->

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md"></a>
## 2026-07-16 | specs | Command Center CPU Temperature Selection and Application Commit

Original source: `docs/specs/2026-07-16-command-center-cpu-temperature-selection-and-commit.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `77db09b4c9c295bb434f16b58f5bbf77a36890809f2646cf2bafc0c68a0b7744`.

<!-- migrated-source: docs/specs/2026-07-16-command-center-cpu-temperature-selection-and-commit.md -->
<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--command-center-cpu-temperature-selection-and-application-commit"></a>
### Command Center CPU Temperature Selection and Application Commit

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--document-status"></a>
#### Document Status

`ready-for-execution`

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--purpose"></a>
#### Purpose

Correct two authenticated production command-center defects discovered after
the native CPU sensor provider passed its guarded acceptance:

- CPU temperature currently reports thermal headroom because the probe selects
  the maximum of every temperature-typed CPU sensor.
- Application commit remains unavailable because the native Windows service
  launcher never exports the deployed release SHA to Spring.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--background"></a>
#### Background

Production release `1fc00914f8aa65b0b4cc931db2ff4a11b2cfb7f3`
successfully enabled PawnIO and returned direct readings from 60 to 66 Celsius.
The authenticated command center then showed approximately 68 Celsius while a
separate measuring tool showed approximately 34 Celsius.

A read-only elevated inventory at
`2026-07-16T14:29:57.4793319-05:00` proved the mismatch:

- Core Average: `37.57 C`
- Core Max: `45 C`
- CPU Package: `48 C`
- Actual individual cores: `34-45 C`
- Distance-to-TjMax sensors: `55-66 C`

LibreHardwareMonitor exposes both actual temperatures and
`Distance to TjMax` headroom through the Temperature sensor type. The current
script takes the maximum of every positive value, so it selected `66 C` from
`E-Core #5 Distance to TjMax`. Higher headroom means a cooler core; displaying
that value as CPU temperature is semantically inverted.

Every production release already contains protected `current\release.json`
metadata with a validated 40-character lowercase SHA. The service launcher
starts the JAR without setting `GIT_COMMIT`, so
`command-center.commit-identifier: ${GIT_COMMIT:unknown}` resolves to
`unknown` and the command center correctly marks Application commit
unavailable.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--goals"></a>
#### Goals

- Select a meaningful actual CPU temperature rather than thermal headroom.
- Prefer the CPU Package sensor because it represents the processor package
  temperature used for thermal management.
- Fall back deterministically when CPU Package is unavailable.
- Exclude every `Distance to TjMax` sensor from all fallbacks.
- Preserve empty output when no plausible actual temperature exists.
- Resolve the exact deployed release SHA inside the application from the active
  release's protected metadata so merge-only deployment remains sufficient.
- Reject missing or malformed release metadata instead of accepting an
  attacker-controlled or ambiguous commit label.
- Prove both fixes with red-green automated tests, complete local suites,
  independent review, GitHub CI, immutable deployment, and authenticated UI
  acceptance.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--non-goals"></a>
#### Non-Goals

- Do not calibrate values to match one third-party tool.
- Do not subtract headroom from a hard-coded TjMax.
- Do not change CPU warning thresholds in this work.
- Do not change PawnIO, LibreHardwareMonitor, ACLs, resource publication, or
  provider refresh timing.
- Do not expose filesystem paths or raw sensor inventories through the API.
- Do not derive the commit from the mutable source checkout or a Git command at
  service startup.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--cpu-temperature-selection"></a>
##### CPU Temperature Selection

- Ignore sensors whose names end with `Distance to TjMax`, case-insensitively.
- Select a positive finite `CPU Package` value when present.
- Otherwise select a positive finite `Core Max` value.
- Otherwise select the maximum remaining actual CPU temperature.
- Continue returning no value when all candidates are absent, non-finite,
  non-positive, or above the existing plausibility ceiling.
- Keep the public metric key `cpu.temperature`.
- Change the metric label to `CPU package temperature` so the preferred
  semantic is visible to administrators.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--application-commit"></a>
##### Application Commit

- Read the release SHA only from `release.json` in the application's active
  release working directory.
- Require exactly one lowercase hexadecimal SHA with 40 characters.
- Prefer an explicitly configured safe commit label when present; otherwise
  use the validated active release SHA.
- Missing or malformed release metadata must keep the card explicitly
  unavailable without stopping the website.
- Preserve the existing Java allowlist for displayed commit identifiers.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--application-commit-card-ui-amendment"></a>
##### Application Commit Card UI Amendment

Production visual acceptance showed that the metric renderer uses
`reading.detail` twice for commit readings: `displayMetric` renders the full SHA
as the primary value, then the generic card renderer appends the same detail as
a `<small>` secondary line. The duplicate full SHA adds no information and can
extend beyond a narrow mobile card.

The considered approaches are:

1. Keep the full SHA as the value and suppress only the duplicate detail line.
   This removes redundancy but leaves a visually dominant 40-character value.
2. Show the first eight SHA characters, suppress the duplicate detail line,
   and retain the complete SHA as the value node's accessible title. This is
   the approved approach because it is compact without discarding the precise
   deployed identity.
3. Add a dedicated copy control. This is deferred because the command center
   does not currently expose copy controls for other metric cards and the
   reported defect does not require a new interaction.

Approved UI behavior:

- Keep the card label `Application commit`.
- Display the first eight characters of an available commit identifier.
- Do not render a secondary line when the detail is the same commit identifier
  already represented by the primary value.
- Preserve the complete commit identifier in the value node's `title`
  attribute for accessible detail and desktop inspection.
- Keep unavailable and malformed commit behavior unchanged.
- Do not change the API response or server-side release-metadata validation.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--rollback-aware-sensor-verification"></a>
##### Rollback-Aware Sensor Verification

- Operational verification must derive the expected probe-script hash from the
  active `current\app.jar` resource.
- The active JAR must contain exactly one
  `BOOT-INF/classes/lib/cpu-temperature.ps1` entry.
- The protected extracted script must match that active-release hash.
- Do not pin one operational hash that makes the previous release unverifiable
  after rollback.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--production-safety"></a>
##### Production Safety

- Test on a non-production candidate before switching release junctions.
- Keep CPU sensors enabled only while all existing provider and Defender gates
  pass.
- Do not manually edit production configuration or release metadata.
- On failed deployment verification, use the existing automatic release
  rollback.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--proposed-approach"></a>
#### Proposed Approach

Extract the CPU selection into the bundled PowerShell probe using named
preference groups. Collect only finite positive actual temperature sensors,
drop every TjMax-distance row, then choose CPU Package, Core Max, or the maximum
remaining value in that order. Keep stdout numeric-only so the bounded Java
probe contract remains unchanged.

Extend the application's existing operational probe result with an optional
active-release commit. The default probe reads a small regular `release.json`
from the process working directory, parses it with the application's JSON
library, and passes only the validated SHA through the existing safe-commit
allowlist.

Replace the operational fixed script hash with a helper that opens the active
`current\app.jar`, hashes its embedded CPU probe resource, and compares the
protected extracted script against that active-release hash. This keeps
verification compatible when `current` points back to a prior release.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--files-and-modules"></a>
#### Files and Modules

- `website/src/main/resources/lib/cpu-temperature.ps1`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProvider.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProviderTest.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java`
- `ops/production/windows/modules/Production.Sensors.psm1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `docs/operations/windows-production.md`

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--validation-plan"></a>
#### Validation Plan

1. Add source-contract and launch-environment tests first; observe failures.
2. Implement named CPU sensor preference and release-metadata export.
3. Update the application-bundle script SHA in Java and make operational
   verification derive the active-release script hash from the JAR.
4. Run focused Java and Pester tests.
5. Run complete Windows Pester and full Gradle build.
6. Obtain independent review with no Critical or Important findings.
7. Pass every required GitHub check and squash-merge.
8. Deploy the immutable merge through native Windows automation.
9. Re-run the read-only CPU inventory and require the website selection to
   equal CPU Package when available.
10. Confirm the authenticated command center shows a plausible CPU package
    temperature and the deployed commit SHA.
11. Confirm services, Defender state, probe bounds, local/public HTTP bodies,
    and uptime formatting remain healthy.
12. Add a failing JavaScript regression proving a full commit is shortened to
    eight characters and the card renderer suppresses duplicate commit detail.
13. Confirm the rendered value retains the full SHA as accessible title text.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-selection-and-commit-md--open-questions"></a>
#### Open Questions

None. CPU Package is the recommended stable host-level metric; Core Max and
remaining actual sensors provide explicit fallbacks without inventing values.

<!-- /migrated-source: docs/specs/2026-07-16-command-center-cpu-temperature-selection-and-commit.md -->

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md"></a>
## 2026-07-16 | specs | Command Center CPU Temperature Stale Resource Recovery

Original source: `docs/specs/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `6f8f8597372e3659f907235cc7be572731e3c5aecef86007d625db054e59c604`.

<!-- migrated-source: docs/specs/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md -->
<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--command-center-cpu-temperature-stale-resource-recovery"></a>
### Command Center CPU Temperature Stale Resource Recovery

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--document-status"></a>
#### Document Status

`in-progress`

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--purpose"></a>
#### Purpose

Make CPU-temperature enablement reliable after production service restarts by atomically publishing one fully verified LibreHardwareMonitor extraction directory, removing securely owned stale siblings, disabling native sensor extraction in deployment candidates, and allowing startup verification to wait briefly for the one live directory.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--background"></a>
#### Background

The merged WinSW recovery release restored normal service ownership and production stability, but the guarded CPU-temperature acceptance run failed closed with:

`Expected exactly one live CPU temperature resource directory.`

An elevated diagnostic then sampled `C:\ProgramData\christopherbell.dev\config\command-center-sensors` every 250 milliseconds while sensors were briefly enabled. Five directories already existed before the enabled service restart. At `2026-07-16T10:10:07.8092340-05:00`, the new Java process created a sixth directory. The count remained six through the observation window. The diagnostic disabled sensors afterward; `ChristopherBellDev`, MongoDB, and cloudflared remained `Running` and `Automatic`, and the local homepage returned `200`, 3912 bytes, and `<title>CB | Home</title>`.

The application intentionally extracts checksum-pinned sensor resources into a fresh nonce directory. Shutdown cleanup is best-effort because Windows may retain a short-lived lock on the DLL after a probe exits. No startup path currently retires prior owned directories, so each affected restart can leave another validly named protected directory. The operational verifier correctly refuses to choose among multiple candidates.

The first merged recovery, PR `#1209` at merge
`24dcd245c584f20280fb5e066c1690f4b8b7482e`, fixed stale-resource ownership and
deployed successfully. Its elevated acceptance advanced to protected-tree
verification, then failed closed because Java NIO replaced the intended ACL
entries without disabling Windows DACL inheritance on the freshly published
directory. The acceptance script restored `sensorLibrariesEnabled=false`; the
website remained healthy. This acceptance-discovered gap is part of the same
recovery objective and requires an explicit Windows protected-DACL operation.

The protected-DACL follow-up, PR `#1210` at merge
`cc41865e14aef50e7ccb32c9d3f6b47cd6c85feb`, then passed resource ownership and
ACL verification. Raw elevated sampling established the next incompatibility:
PowerShell 7 returned exit code zero with empty stdout while stderr reported
that LibreHardwareMonitor 0.9.6 could not find the full .NET Framework
`Mutex(Boolean, String, Boolean ByRef, MutexSecurity)` constructor. The same
pinned resources under Windows PowerShell 5.1 produced six clean readings from
64 to 68 Celsius in approximately 0.7 seconds each. Production verification
must therefore use the same fixed full-framework host as the application probe,
and the script must make PowerShell errors terminating.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--goals"></a>
#### Goals

- Extract and verify a fresh current-version resource set under a protected nonmatching staging name.
- Atomically rename the complete staging directory to its final matching nonce name.
- Remove every prior matching current-version sibling while excluding the newly published live directory.
- Validate each cleanup target as a direct, non-link child of the ACL-protected sensor base before deletion.
- Fail closed if stale cleanup cannot complete.
- Disable native sensor libraries in the parallel `prod,deploy-smoke` candidate so a candidate cannot create or delete production sensor resources.
- Preserve checksum verification, ACL hardening, nonce validation, and fresh-directory extraction.
- Disable and verify Windows DACL inheritance on every hardened sensor path.
- Run the pinned LibreHardwareMonitor 0.9.6 script only through Windows
  PowerShell 5.1, not PowerShell 7.
- Make probe-script errors terminating so stderr failures cannot exit zero with
  empty output.
- Let elevated startup verification poll for the lazy first-sample extraction instead of assuming it already exists.
- Keep the exact-one-live-directory requirement after the bounded wait.
- Prove the fix locally, through independent review and GitHub CI, and on the production service.
- Remove the six existing stale directories only through the merged application lifecycle, not through an ad hoc broad deletion command.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--non-goals"></a>
#### Non-Goals

- Do not weaken the ProgramData ACL, Defender checks, PawnIO signature checks, or sensor fail-closed behavior.
- Do not select the newest directory while silently ignoring stale siblings.
- Do not add a generic recursive-cleanup production command.
- Do not delete directories for other LibreHardwareMonitor versions.
- Do not reinstall PawnIO.
- Do not reboot, power off, or change MongoDB or cloudflared.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--secure-stale-cleanup"></a>
##### Secure Stale Cleanup

- `SecureNativeLibraryProvisioner` must enumerate only direct children matching its exact `librehardwaremonitor-0.9.6-<nonce>` naming contract.
- Every cleanup target and descendant must be checked with `NOFOLLOW_LINKS`; symbolic links, junctions, or other reparse points must stop provisioning.
- The existing ACL policy must harden and verify every stale path before deletion.
- Deletion must be strict for pre-provision cleanup: any failure must abort provisioning instead of being ignored.
- The new resource set must be extracted under a nonmatching protected staging name so the operational verifier cannot observe incomplete resources.
- Publishing must use an atomic same-directory rename to the final matching nonce name; unsupported atomic movement must fail closed.
- Cleanup must exclude the freshly published directory and remove every other matching current-version sibling before provisioning returns.
- If provisioning or cleanup fails, a strict validated rollback must delete the owned staging or published tree; rollback failures must be reported rather than ignored.
- A cross-process file lease beneath the protected base must be acquired before staging or cleanup and held for the complete `NativeLibraries` lifetime.
- A second process that cannot acquire the lease must fail closed without creating, deleting, or probing resource directories.
- Every unsuccessful lease acquisition path must close its file channel.
- After stale cleanup succeeds, the application must atomically publish a protected owner marker containing its current Java PID and process start timestamp.
- The Windows ACL policy must use the fixed JNA bridge to reapply the verified
  DACL with `PROTECTED_DACL_SECURITY_INFORMATION`, then confirm
  `SE_DACL_PROTECTED`; Java NIO ACL entries alone are insufficient.
- Production and candidate JVM launchers must explicitly allow native access
  for the fixed JNA bridge.
- The final owner marker must not exist while resources are staging or stale cleanup is incomplete.
- Owner-marker atomic publication must be the final fallible provisioning operation so an unsuccessful provision can never leave a readiness signal.
- Best-effort deletion is permitted only during normal `NativeLibraries.close()`; the next provisioning cycle is the authoritative stale recovery boundary.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--candidate-isolation"></a>
##### Candidate Isolation

- `Test-CandidateRelease` must force `COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED=false`.
- The candidate override must remain present when a restore-check database override is also supplied.
- Deployment candidates must not provision, probe, clean, or otherwise mutate the production sensor directory.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--bounded-operational-wait"></a>
##### Bounded Operational Wait

- `Production.Sensors.psm1` must wait up to 15 seconds for exactly one live current-version directory.
- Polling must occur every 250 milliseconds.
- Zero or multiple directories may be transient during cleanup and lazy provisioning.
- A directory counts as live only when its protected owner marker matches both
  the Java PID currently listening on the configured production port and that
  process's exact integer epoch-millisecond start timestamp.
- PowerShell enumeration must apply the same exact nonce-name regex as Java before counting or inspecting markers.
- A sole stale directory with an absent or old owner marker must not satisfy startup verification.
- The timeout error must include the final observed live and total directory counts.
- Once exactly one directory exists, all existing ACL, hash, file-completeness, direct-probe, and Celsius plausibility checks remain mandatory.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--automated-validation"></a>
##### Automated Validation

- A Java regression must prove a stale current-version directory is removed before a fresh directory is provisioned.
- The prior test that required rejection of every preexisting current-version directory must be replaced because secure cleanup is now the intended behavior.
- Pester regressions must prove multiple directories are retried until one remains and that unresolved ambiguity times out with the observed count.
- Focused Java and Pester tests must be observed failing before implementation and passing afterward.
- The complete Windows production suite, full Gradle build, independent review, and all required GitHub checks must pass.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--production-acceptance"></a>
##### Production Acceptance

- Deploy only the merged release.
- Confirm sensors are disabled and production is healthy before enablement.
- Enable through `prod.ps1 sensor-enable`.
- Run `verify-startup`; require one protected resource directory and a direct Celsius value greater than `0` and less than `126`.
- Observe three 30-second refresh windows.
- Confirm probe processes do not accumulate, Defender reports no active PawnIO or WinRing0 threat, and the service does not restart.
- Confirm local and public homepage responses remain `200` with `<title>CB | Home</title>`.
- If any gate fails, disable sensors and preserve production health.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--proposed-approach"></a>
#### Proposed Approach

Add protected nonmatching staging to `SecureNativeLibraryProvisioner`. Populate, checksum-verify, and ACL-harden every resource in staging, then atomically rename the complete directory to its final matching nonce name. Cleanup excludes that live directory, walks every other matching sibling without following links, validates each entry, applies the existing ACL policy, and deletes bottom-up. If cleanup fails, the published directory is removed by the existing failure path. This ordering prevents the directory count from transiently reaching one while the sole remaining directory is stale and prevents the verifier from observing incomplete fresh resources.

Force the native sensor switch to `false` in `Test-CandidateRelease` so the parallel deployment smoke process cannot race the production service or create stale extraction directories when it is forcibly stopped.

Add a private PowerShell wait helper that polls the protected sensor base for exactly one current-version directory. `Get-ProductionCpuTemperature` will use that helper before performing its existing protected-tree, checksum, and direct-probe validation.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--files-and-modules"></a>
#### Files and Modules

- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- `website/build.gradle.kts`
- `build.gradle.kts`
- `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- `website/src/main/resources/lib/cpu-temperature.ps1`
- `ops/production/windows/modules/Production.Sensors.psm1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `ops/production/windows/modules/Production.Deploy.psm1`
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- `docs/operations/windows-production.md`

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--validation-plan"></a>
#### Validation Plan

1. Add the Java and Pester regressions without production-code changes and record their expected failures.
2. Implement strict Java stale cleanup and the bounded PowerShell resource wait.
3. Run focused Java and Pester tests.
4. Run the complete Windows production test suite and full Gradle build with isolated Gradle state.
5. Request independent code review.
6. Push a dedicated branch, open a pull request, wait for all required checks, and squash-merge.
7. Deploy the immutable merge through the native Windows production workflow.
8. Run the guarded CPU-temperature acceptance sequence and record directory, Celsius, process, Defender, service, and HTTP evidence.
9. Save Builder test, spoke review, closure, and session-memory artifacts.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--rollback"></a>
#### Rollback

- Keep `sensorLibrariesEnabled=false` until the merged release is deployed and all provider checks pass.
- If local or CI validation fails, do not deploy.
- If production enablement fails, run `sensor-disable`; the service restart returns the provider to disabled mode.
- If the new release cannot start, use the existing guarded production release rollback.
- Do not manually delete protected sensor directories unless a separately reviewed recovery path becomes necessary.

<a id="source-docs-specs-2026-07-16-command-center-cpu-temperature-stale-resource-recovery-md--open-questions"></a>
#### Open Questions

None. The elevated trace established stale current-version directories as the ambiguity source, and the user authorized the recommended full repair path.

<!-- /migrated-source: docs/specs/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md -->

