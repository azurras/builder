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
- Export the exact deployed release SHA to both candidate and production JARs.
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

- Read the release SHA only from the protected release directory's
  `release.json`.
- Require exactly one lowercase hexadecimal SHA with 40 characters.
- Set `GIT_COMMIT` in `Start-ProductionJar` for deployment candidates.
- Set `GIT_COMMIT` in `Start-ChristopherBellDev.ps1` before launching the
  production JAR.
- A missing or invalid release metadata file must stop that launch path.
- Preserve the existing Java allowlist for displayed commit identifiers.

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

Add one production PowerShell helper that reads and validates `release.json`.
Use it from candidate launch and mirror the same strict validation in the
installed service launcher, exporting the SHA as process-scoped `GIT_COMMIT`
before Java starts.

## Files and Modules

- `website/src/main/resources/lib/cpu-temperature.ps1`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProvider.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProviderTest.java`
- `ops/production/windows/modules/Production.Deploy.psm1`
- `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- `ops/production/windows/tests/Production.Install.Tests.ps1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `docs/operations/windows-production.md`

## Validation Plan

1. Add source-contract and launch-environment tests first; observe failures.
2. Implement named CPU sensor preference and release-metadata export.
3. Update the pinned script SHA in Java and PowerShell.
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

## Open Questions

None. CPU Package is the recommended stable host-level metric; Core Max and
remaining actual sensors provide explicit fallbacks without inventing values.
