# Command Center CPU Temperature Selection and Application Commit

## Document Status

`ready-for-execution`

## Purpose

Correct two authenticated production command-center defects discovered after
the native CPU sensor provider passed its guarded acceptance:

- CPU temperature currently reports thermal headroom because the probe selects
  the maximum of every temperature-typed CPU sensor.
- Application commit remains unavailable because the native Windows service
  launcher never exports the deployed release SHA to Spring.

## Background

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

## Goals

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

## Non-Goals

- Do not calibrate values to match one third-party tool.
- Do not subtract headroom from a hard-coded TjMax.
- Do not change CPU warning thresholds in this work.
- Do not change PawnIO, LibreHardwareMonitor, ACLs, resource publication, or
  provider refresh timing.
- Do not expose filesystem paths or raw sensor inventories through the API.
- Do not derive the commit from the mutable source checkout or a Git command at
  service startup.

## Requirements

### CPU Temperature Selection

- Ignore sensors whose names end with `Distance to TjMax`, case-insensitively.
- Select a positive finite `CPU Package` value when present.
- Otherwise select a positive finite `Core Max` value.
- Otherwise select the maximum remaining actual CPU temperature.
- Continue returning no value when all candidates are absent, non-finite,
  non-positive, or above the existing plausibility ceiling.
- Keep the public metric key `cpu.temperature`.
- Change the metric label to `CPU package temperature` so the preferred
  semantic is visible to administrators.

### Application Commit

- Read the release SHA only from `release.json` in the application's active
  release working directory.
- Require exactly one lowercase hexadecimal SHA with 40 characters.
- Prefer an explicitly configured safe commit label when present; otherwise
  use the validated active release SHA.
- Missing or malformed release metadata must keep the card explicitly
  unavailable without stopping the website.
- Preserve the existing Java allowlist for displayed commit identifiers.

### Application Commit Card UI Amendment

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

### Rollback-Aware Sensor Verification

- Operational verification must derive the expected probe-script hash from the
  active `current\app.jar` resource.
- The active JAR must contain exactly one
  `BOOT-INF/classes/lib/cpu-temperature.ps1` entry.
- The protected extracted script must match that active-release hash.
- Do not pin one operational hash that makes the previous release unverifiable
  after rollback.

### Production Safety

- Test on a non-production candidate before switching release junctions.
- Keep CPU sensors enabled only while all existing provider and Defender gates
  pass.
- Do not manually edit production configuration or release metadata.
- On failed deployment verification, use the existing automatic release
  rollback.

## Proposed Approach

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

## Files and Modules

- `website/src/main/resources/lib/cpu-temperature.ps1`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProvider.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProviderTest.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java`
- `ops/production/windows/modules/Production.Sensors.psm1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `docs/operations/windows-production.md`

## Validation Plan

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

## Open Questions

None. CPU Package is the recommended stable host-level metric; Core Max and
remaining actual sensors provide explicit fallbacks without inventing values.
