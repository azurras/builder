# Command Center CPU Temperature Stale Resource Recovery

## Document Status

`ready-for-execution`

## Purpose

Make CPU-temperature enablement reliable after production service restarts by atomically publishing one fully verified LibreHardwareMonitor extraction directory, removing securely owned stale siblings, disabling native sensor extraction in deployment candidates, and allowing startup verification to wait briefly for the one live directory.

## Background

The merged WinSW recovery release restored normal service ownership and production stability, but the guarded CPU-temperature acceptance run failed closed with:

`Expected exactly one live CPU temperature resource directory.`

An elevated diagnostic then sampled `C:\ProgramData\christopherbell.dev\config\command-center-sensors` every 250 milliseconds while sensors were briefly enabled. Five directories already existed before the enabled service restart. At `2026-07-16T10:10:07.8092340-05:00`, the new Java process created a sixth directory. The count remained six through the observation window. The diagnostic disabled sensors afterward; `ChristopherBellDev`, MongoDB, and cloudflared remained `Running` and `Automatic`, and the local homepage returned `200`, 3912 bytes, and `<title>CB | Home</title>`.

The application intentionally extracts checksum-pinned sensor resources into a fresh nonce directory. Shutdown cleanup is best-effort because Windows may retain a short-lived lock on the DLL after a probe exits. No startup path currently retires prior owned directories, so each affected restart can leave another validly named protected directory. The operational verifier correctly refuses to choose among multiple candidates.

## Goals

- Extract and verify a fresh current-version resource set under a protected nonmatching staging name.
- Atomically rename the complete staging directory to its final matching nonce name.
- Remove every prior matching current-version sibling while excluding the newly published live directory.
- Validate each cleanup target as a direct, non-link child of the ACL-protected sensor base before deletion.
- Fail closed if stale cleanup cannot complete.
- Disable native sensor libraries in the parallel `prod,deploy-smoke` candidate so a candidate cannot create or delete production sensor resources.
- Preserve checksum verification, ACL hardening, nonce validation, and fresh-directory extraction.
- Let elevated startup verification poll for the lazy first-sample extraction instead of assuming it already exists.
- Keep the exact-one-live-directory requirement after the bounded wait.
- Prove the fix locally, through independent review and GitHub CI, and on the production service.
- Remove the six existing stale directories only through the merged application lifecycle, not through an ad hoc broad deletion command.

## Non-Goals

- Do not weaken the ProgramData ACL, Defender checks, PawnIO signature checks, or sensor fail-closed behavior.
- Do not select the newest directory while silently ignoring stale siblings.
- Do not add a generic recursive-cleanup production command.
- Do not delete directories for other LibreHardwareMonitor versions.
- Do not reinstall PawnIO.
- Do not reboot, power off, or change MongoDB or cloudflared.

## Requirements

### Secure Stale Cleanup

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
- The final owner marker must not exist while resources are staging or stale cleanup is incomplete.
- Owner-marker atomic publication must be the final fallible provisioning operation so an unsuccessful provision can never leave a readiness signal.
- Best-effort deletion is permitted only during normal `NativeLibraries.close()`; the next provisioning cycle is the authoritative stale recovery boundary.

### Candidate Isolation

- `Test-CandidateRelease` must force `COMMAND_CENTER_SENSOR_LIBRARIES_ENABLED=false`.
- The candidate override must remain present when a restore-check database override is also supplied.
- Deployment candidates must not provision, probe, clean, or otherwise mutate the production sensor directory.

### Bounded Operational Wait

- `Production.Sensors.psm1` must wait up to 15 seconds for exactly one live current-version directory.
- Polling must occur every 250 milliseconds.
- Zero or multiple directories may be transient during cleanup and lazy provisioning.
- A directory counts as live only when its protected owner marker matches both the Java PID currently listening on the configured production port and that process's start timestamp within a one-second platform-precision tolerance.
- PowerShell enumeration must apply the same exact nonce-name regex as Java before counting or inspecting markers.
- A sole stale directory with an absent or old owner marker must not satisfy startup verification.
- The timeout error must include the final observed live and total directory counts.
- Once exactly one directory exists, all existing ACL, hash, file-completeness, direct-probe, and Celsius plausibility checks remain mandatory.

### Automated Validation

- A Java regression must prove a stale current-version directory is removed before a fresh directory is provisioned.
- The prior test that required rejection of every preexisting current-version directory must be replaced because secure cleanup is now the intended behavior.
- Pester regressions must prove multiple directories are retried until one remains and that unresolved ambiguity times out with the observed count.
- Focused Java and Pester tests must be observed failing before implementation and passing afterward.
- The complete Windows production suite, full Gradle build, independent review, and all required GitHub checks must pass.

### Production Acceptance

- Deploy only the merged release.
- Confirm sensors are disabled and production is healthy before enablement.
- Enable through `prod.ps1 sensor-enable`.
- Run `verify-startup`; require one protected resource directory and a direct Celsius value greater than `0` and less than `126`.
- Observe three 30-second refresh windows.
- Confirm probe processes do not accumulate, Defender reports no active PawnIO or WinRing0 threat, and the service does not restart.
- Confirm local and public homepage responses remain `200` with `<title>CB | Home</title>`.
- If any gate fails, disable sensors and preserve production health.

## Proposed Approach

Add protected nonmatching staging to `SecureNativeLibraryProvisioner`. Populate, checksum-verify, and ACL-harden every resource in staging, then atomically rename the complete directory to its final matching nonce name. Cleanup excludes that live directory, walks every other matching sibling without following links, validates each entry, applies the existing ACL policy, and deletes bottom-up. If cleanup fails, the published directory is removed by the existing failure path. This ordering prevents the directory count from transiently reaching one while the sole remaining directory is stale and prevents the verifier from observing incomplete fresh resources.

Force the native sensor switch to `false` in `Test-CandidateRelease` so the parallel deployment smoke process cannot race the production service or create stale extraction directories when it is forcibly stopped.

Add a private PowerShell wait helper that polls the protected sensor base for exactly one current-version directory. `Get-ProductionCpuTemperature` will use that helper before performing its existing protected-tree, checksum, and direct-probe validation.

## Files and Modules

- `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- `ops/production/windows/modules/Production.Sensors.psm1`
- `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- `ops/production/windows/modules/Production.Deploy.psm1`
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- `docs/operations/windows-production.md`

## Validation Plan

1. Add the Java and Pester regressions without production-code changes and record their expected failures.
2. Implement strict Java stale cleanup and the bounded PowerShell resource wait.
3. Run focused Java and Pester tests.
4. Run the complete Windows production test suite and full Gradle build with isolated Gradle state.
5. Request independent code review.
6. Push a dedicated branch, open a pull request, wait for all required checks, and squash-merge.
7. Deploy the immutable merge through the native Windows production workflow.
8. Run the guarded CPU-temperature acceptance sequence and record directory, Celsius, process, Defender, service, and HTTP evidence.
9. Save Builder test, spoke review, closure, and session-memory artifacts.

## Rollback

- Keep `sensorLibrariesEnabled=false` until the merged release is deployed and all provider checks pass.
- If local or CI validation fails, do not deploy.
- If production enablement fails, run `sensor-disable`; the service restart returns the provider to disabled mode.
- If the new release cannot start, use the existing guarded production release rollback.
- Do not manually delete protected sensor directories unless a separately reviewed recovery path becomes necessary.

## Open Questions

None. The elevated trace established stale current-version directories as the ambiguity source, and the user authorized the recommended full repair path.
