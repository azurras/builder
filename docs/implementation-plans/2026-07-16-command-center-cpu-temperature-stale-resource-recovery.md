# Command Center CPU Temperature Stale Resource Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire securely owned stale LibreHardwareMonitor extraction directories, wait for one lazy live directory, and complete production CPU-temperature acceptance.

**Architecture:** Keep fresh nonce-based extraction and the exact-one-live-directory verifier. Before creating a new nonce directory, the Java provisioner will strictly validate and delete only matching current-version children beneath the protected base; the PowerShell verifier will poll for up to 15 seconds while that cleanup and the first asynchronous metrics sample complete. All checksum, ACL, Defender, PawnIO, and fail-closed gates remain unchanged.

**Tech Stack:** Java 25, Spring Boot, JUnit 5, AssertJ, PowerShell 7, Pester 5, Gradle, PawnIO 2.2.0.0, LibreHardwareMonitor 0.9.6, Windows services, GitHub Actions, CodeQL.

## Global Constraints

- Do not weaken ProgramData ACLs, Defender checks, PawnIO signature checks, checksum validation, or fail-closed behavior.
- Delete only direct current-version children that match `librehardwaremonitor-0.9.6-<valid nonce>`.
- Do not follow symbolic links, junctions, or other reparse points.
- Do not select a newest directory while ignoring ambiguity.
- Keep the operational wait at exactly 15 seconds with 250-millisecond polls.
- Do not reinstall PawnIO, reboot, power off, or modify MongoDB or cloudflared.
- Keep `sensorLibrariesEnabled=false` until the merged release is deployed and pre-enable checks pass.

---

## Document Status

`complete`

Execution of this plan ended at its independent-review gate after the reviewer identified a transient-one-directory race and a parallel deployment-candidate ownership race. Corrective execution continues in `docs/implementation-plans/2026-07-16-command-center-cpu-temperature-resource-publication-review-fixes.md`.

## Objective

Implement and deploy a test-driven stale-resource lifecycle fix so a sensor-enabled production restart converges from multiple protected stale directories to exactly one live directory and produces stable plausible CPU temperatures.

## Goals

- Observe focused Java and Pester regressions fail against the current code.
- Strictly remove stale current-version extraction trees before fresh provisioning.
- Abort provisioning if cleanup validation or deletion fails.
- Wait conditionally for lazy provisioning without weakening exact-one validation.
- Pass focused and complete local test suites.
- Obtain independent review and pass all GitHub CI gates.
- Deploy the immutable merge and enable CPU temperature successfully.
- Preserve production stability, Defender health, and bounded probe processes.
- Save Builder test, review, closure, and session-memory evidence.

## Inputs

- Approved spec: `docs/specs/2026-07-16-command-center-cpu-temperature-stale-resource-recovery.md`
- Parent recovery plan: `docs/implementation-plans/2026-07-16-christopherbell-dev-winsw-log-rotation-recovery.md`
- Active work record: `docs/work/2026-07-12-command-center-cpu-temperature-and-uptime.md`
- Elevated trace: 90 samples from `2026-07-16T10:10:02.1446012-05:00` through `2026-07-16T10:10:37.0158954-05:00`.
- Root-cause evidence: five current-version directories existed before enabled restart; a sixth appeared at `2026-07-16T10:10:07.8092340-05:00`; maximum observed CPU probe count was two during overlapping direct/application probes.
- Safety evidence after diagnostic: sensors disabled, all three production services `Running` and `Automatic`, one port 8080 listener, local homepage `200`, 3912 bytes, title `CB | Home`.

## Branch

- Base: `origin/main` at `d33a2c41e1e9b23c4b313ff6fb19ac389f8d7699`
- Branch: `codex/cpu-temperature-stale-resources`
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\winsw-log-rotation-recovery-merged`

## Non-Goals

- No generic filesystem cleanup command.
- No change to the sensor HTTP contract or command-center UI.
- No provider dependency upgrade.
- No WinSW, MongoDB, cloudflared, or application-log policy change.
- No manual broad deletion under `C:\ProgramData`.
- No restart, shutdown, or reboot acceptance action.

## Assumptions

- The production Java service runs as SYSTEM and owns the protected sensor base.
- The existing ACL policy accepts only SYSTEM or Administrators as trusted owners and rewrites accepted paths to SYSTEM ownership.
- `Files.walk` does not follow symbolic links unless explicitly requested.
- Only one production website instance should provision sensor resources at a time.
- Lazy command-center sampling creates the live directory within 15 seconds on this host; the captured trace showed creation approximately four seconds after service start.

## Open Questions

None.

## File Structure

- `SecureNativeLibraryProvisioner.java`: owns protected resource extraction, stale-tree validation, and cleanup.
- `SecureNativeLibraryProvisionerTest.java`: owns extraction and cleanup security regressions.
- `Production.Sensors.psm1`: owns elevated provider verification and direct Celsius probing.
- `Production.Sensors.Tests.ps1`: owns operational wait and fail-closed regressions.
- `windows-production.md`: owns operator-facing sensor lifecycle and recovery guidance.

## Task Breakdown

### Task 1 - Retire stale extraction trees before fresh provisioning

Sequence / dependencies:
- Runs first because the PowerShell verifier must not accept ambiguity that the application itself continues creating.
- Follow Java red-green-refactor before modifying production code.

Implementation notes:
- Replace the prior blanket rejection of a preexisting current-version directory with secure stale retirement.
- Enumerate only direct children using the exact version prefix.
- Validate the candidate name, parent, type, link state, descendants, and ACL before deleting any entry.
- Collect and validate the full tree first; delete bottom-up only after every entry passes.
- Keep existing best-effort cleanup for the live owned directory on close.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: 27-37
- Action: replace

Current:
```java
  @Test
  void refusesPreexistingVersionDirectoryWithoutLoadingItsFiles() throws Exception {
    Path existing = Files.createDirectories(
        tempDir.resolve("librehardwaremonitor-0.9.6-fixed"));
    Files.writeString(existing.resolve("LibreHardwareMonitorLib.dll"), "malicious", UTF_8);
    var provisioner = provisioner("trusted", hash("trusted"), path -> {}, "fixed");

    assertThatThrownBy(provisioner::provision).isInstanceOf(SecurityException.class);
    assertThat(Files.readString(existing.resolve("LibreHardwareMonitorLib.dll"), UTF_8))
        .isEqualTo("malicious");
  }
```

Proposed:
```java
  @Test
  void removesStaleVersionDirectoryBeforeProvisioningFreshResources() throws Exception {
    Path stale = Files.createDirectories(
        tempDir.resolve("librehardwaremonitor-0.9.6-stale"));
    Files.writeString(stale.resolve("LibreHardwareMonitorLib.dll"), "malicious", UTF_8);
    var provisioner = provisioner("trusted", hash("trusted"), path -> {}, "fresh");

    var libraries = provisioner.provision();

    assertThat(stale).doesNotExist();
    assertThat(libraries.directory().getFileName().toString())
        .isEqualTo("librehardwaremonitor-0.9.6-fresh");
    assertThat(Files.readString(libraries.libreHardwareMonitor(), UTF_8))
        .isEqualTo("trusted");
    libraries.close();
  }
```

Verification:
- Run `$env:GRADLE_USER_HOME=Join-Path $env:TEMP 'gradle-codex-cpu-stale-red'; .\gradlew.bat :website:test --tests "dev.christopherbell.admin.commandcenter.metrics.SecureNativeLibraryProvisionerTest.removesStaleVersionDirectoryBeforeProvisioningFreshResources" --no-daemon`.
- Expect failure because the current provisioner leaves the stale directory and only attempts to create the fresh directory.

#### Code Edit 1.2
- File: `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`
- Lines: after 131
- Action: add

Proposed:
```java
  @Test
  void staleCleanupRefusesSymbolicLinksWithoutDeletingTheirTarget() throws Exception {
    Path outside = Files.writeString(tempDir.resolve("outside.txt"), "outside", UTF_8);
    Path stale = Files.createDirectories(
        tempDir.resolve("librehardwaremonitor-0.9.6-stale-link"));
    try {
      Files.createSymbolicLink(stale.resolve("linked.txt"), outside);
    } catch (UnsupportedOperationException | IOException failure) {
      org.junit.jupiter.api.Assumptions.abort("Symbolic links unavailable: " + failure.getMessage());
    }
    var provisioner = provisioner("trusted", hash("trusted"), path -> {}, "fresh-link");

    assertThatThrownBy(provisioner::provision)
        .isInstanceOf(SecurityException.class)
        .hasMessageContaining("link");
    assertThat(outside).exists();
  }
```

Verification:
- Run the complete `SecureNativeLibraryProvisionerTest`.
- Before production edits, expect the stale-removal test to fail. The link test may be skipped if Windows denies symlink creation; otherwise it must fail for the intended missing-cleanup reason or pass only through the existing fail-closed create collision.

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 27-29
- Action: replace

Current:
```java
final class SecureNativeLibraryProvisioner {
  static final String VERSION = "0.9.6";
  private final Path baseDirectory;
```

Proposed:
```java
final class SecureNativeLibraryProvisioner {
  static final String VERSION = "0.9.6";
  private static final String DIRECTORY_PREFIX = "librehardwaremonitor-" + VERSION + "-";
  private static final String VALID_DIRECTORY_NAME =
      java.util.regex.Pattern.quote(DIRECTORY_PREFIX) + "[A-Za-z0-9-]{1,64}";
  private final Path baseDirectory;
```

Verification:
- Compile through the focused Gradle test command after all Task 1 production edits.

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: 58-65
- Action: replace

Current:
```java
    Path versionDirectory = baseDirectory.resolve(
        "librehardwaremonitor-" + VERSION + "-" + nonce);
    boolean created = false;
    try {
      createTrustedBaseDirectory();
      verifyNotLinkOrReparsePoint(baseDirectory);
      aclPolicy.hardenAndVerify(baseDirectory);
      Files.createDirectory(versionDirectory);
```

Proposed:
```java
    Path versionDirectory = baseDirectory.resolve(DIRECTORY_PREFIX + nonce);
    boolean created = false;
    try {
      createTrustedBaseDirectory();
      verifyNotLinkOrReparsePoint(baseDirectory);
      aclPolicy.hardenAndVerify(baseDirectory);
      removeStaleVersionDirectories();
      Files.createDirectory(versionDirectory);
```

Verification:
- The focused stale-removal test must pass after Code Edit 1.5.

#### Code Edit 1.5
- File: `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`
- Lines: before 103
- Action: add

Proposed:
```java
  private void removeStaleVersionDirectories() throws IOException {
    try (var candidates = Files.newDirectoryStream(baseDirectory, DIRECTORY_PREFIX + "*")) {
      for (Path candidate : candidates) {
        Path normalized = candidate.toAbsolutePath().normalize();
        if (!baseDirectory.equals(normalized.getParent())
            || !normalized.getFileName().toString().matches(VALID_DIRECTORY_NAME)) {
          throw new SecurityException("Invalid stale native library directory.");
        }
        verifyNotLinkOrReparsePoint(normalized);
        if (!Files.isDirectory(normalized, LinkOption.NOFOLLOW_LINKS)) {
          throw new SecurityException("Stale native library resource is not a directory.");
        }
        deleteTreeStrict(normalized);
      }
    }
  }

  private void deleteTreeStrict(Path directory) throws IOException {
    List<Path> paths;
    try (var tree = Files.walk(directory)) {
      paths = new ArrayList<>(tree.toList());
    }
    for (Path path : paths) {
      verifyNotLinkOrReparsePoint(path);
      aclPolicy.hardenAndVerify(path);
    }
    paths.sort(java.util.Comparator.reverseOrder());
    for (Path path : paths) {
      Files.delete(path);
    }
  }
```

Verification:
- Re-run `SecureNativeLibraryProvisionerTest` and expect all tests green, with the symlink regression either green or explicitly skipped due unavailable OS capability.
- Run `git diff --check`.

- [ ] **Step 1: Apply Code Edits 1.1 and 1.2 only.**
- [ ] **Step 2: Run the focused Java tests and record the expected red result.**
- [ ] **Step 3: Apply Code Edits 1.3 through 1.5.**
- [ ] **Step 4: Re-run the focused Java tests and expect green.**
- [ ] **Step 5: Inspect the Java diff for path, link, ACL, and delete-order safety.**

### Task 2 - Wait for stale cleanup and lazy live provisioning

Sequence / dependencies:
- Runs after Task 1 is green because the wait must converge to a state the application can actually produce.
- Follow Pester red-green-refactor before modifying the PowerShell module.

Implementation notes:
- Treat a missing base as zero observed directories while the first metrics sample provisions resources.
- Poll both zero and multiple counts because the trace proved multiple protected stale directories can exist before Java cleanup.
- Return only when exactly one directory is present.
- Include the final observed count in timeout evidence.

#### Code Edit 2.1
- File: `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- Lines: after 143
- Action: add

Proposed:
```powershell
        It 'waits for stale resources to collapse to one live directory' {
            $script:directoryEnumerations = 0
            Mock Test-Path { $true }
            Mock Get-ChildItem {
                $script:directoryEnumerations++
                if ($script:directoryEnumerations -eq 1) {
                    return @(
                        [pscustomobject]@{ FullName='C:\sensors\stale-a' },
                        [pscustomobject]@{ FullName='C:\sensors\stale-b' })
                }
                return @([pscustomobject]@{ FullName='C:\sensors\live' })
            }
            Mock Start-Sleep {}

            $directory = Wait-ProductionSensorResourceDirectory `
                -Base 'C:\sensors' `
                -Timeout ([timespan]::FromSeconds(1))

            $directory.FullName | Should -Be 'C:\sensors\live'
            Should -Invoke Get-ChildItem -Times 2 -Exactly
            Should -Invoke Start-Sleep -Times 1 -Exactly -ParameterFilter {
                $Milliseconds -eq 250
            }
        }

        It 'reports the unresolved resource count when the wait expires' {
            Mock Test-Path { $true }
            Mock Get-ChildItem {
                @(
                    [pscustomobject]@{ FullName='C:\sensors\stale-a' },
                    [pscustomobject]@{ FullName='C:\sensors\stale-b' })
            }
            Mock Start-Sleep {}

            {
                Wait-ProductionSensorResourceDirectory `
                    -Base 'C:\sensors' `
                    -Timeout ([timespan]::Zero)
            } | Should -Throw '*found 2*'

            Should -Invoke Start-Sleep -Times 0 -Exactly
        }
```

Verification:
- Run `pwsh -NoLogo -NoProfile -Command "Import-Module Pester -MinimumVersion 5.0; Invoke-Pester -Path 'ops/production/windows/tests/Production.Sensors.Tests.ps1' -Output Detailed"`.
- Expect two failures because `Wait-ProductionSensorResourceDirectory` does not exist.

#### Code Edit 2.2
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: before 82
- Action: add

Proposed:
```powershell
function Wait-ProductionSensorResourceDirectory {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Base,
        [timespan]$Timeout = ([timespan]::FromSeconds(15)),
        [ValidateRange(1,5000)][int]$PollMilliseconds = 250
    )

    $deadline = (Get-Date).Add($Timeout)
    $observedCount = 0
    while ($true) {
        $directories = if (Test-Path -LiteralPath $Base -PathType Container) {
            @(Get-ChildItem -LiteralPath $Base -Directory `
                -Filter 'librehardwaremonitor-0.9.6-*' -ErrorAction Stop)
        } else {
            @()
        }
        $observedCount = $directories.Count
        if ($observedCount -eq 1) {
            return $directories[0]
        }
        if ((Get-Date) -ge $deadline) {
            throw "Expected exactly one live CPU temperature resource directory; found $observedCount."
        }
        Start-Sleep -Milliseconds $PollMilliseconds
    }
}
```

Verification:
- Run the focused Pester suite after Code Edit 2.3 and expect both new tests green.

#### Code Edit 2.3
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: 86-94
- Action: replace

Current:
```powershell
    $base = Join-Path $Root 'config\command-center-sensors'
    if (-not (Test-Path -LiteralPath $base -PathType Container)) {
        throw 'Live CPU temperature resources are unavailable.'
    }
    $directories = @(Get-ChildItem -LiteralPath $base -Directory -Filter 'librehardwaremonitor-0.9.6-*' -ErrorAction Stop)
    if ($directories.Count -ne 1) {
        throw 'Expected exactly one live CPU temperature resource directory.'
    }
    $directory = $directories[0].FullName
```

Proposed:
```powershell
    $base = Join-Path $Root 'config\command-center-sensors'
    $directory = (
        Wait-ProductionSensorResourceDirectory -Base $base
    ).FullName
```

Verification:
- Run the focused Pester suite and expect all sensor tests green.
- Confirm existing hash, ACL, completeness, direct process, timeout, and plausibility code remains unchanged below this edit.

- [ ] **Step 1: Apply Code Edit 2.1 only.**
- [ ] **Step 2: Run focused Pester and record the expected two red failures.**
- [ ] **Step 3: Apply Code Edits 2.2 and 2.3.**
- [ ] **Step 4: Re-run focused Pester and expect green.**
- [ ] **Step 5: Run `git diff --check` and inspect the PowerShell diff.**

### Task 3 - Document, verify, review, and publish

Sequence / dependencies:
- Runs after Tasks 1 and 2 are green.
- Must finish and merge before production mutation.

Implementation notes:
- Document that stale current-version directories are retired by the protected application lifecycle.
- Use isolated Gradle state.
- Request independent review focused on deletion scope, reparse-point safety, concurrent instance risk, and bounded-wait semantics.

#### Code Edit 3.1
- File: `docs/operations/windows-production.md`
- Lines: after 162
- Action: add

Proposed:
```markdown
CPU sensor resources use fresh nonce directories beneath the protected
`config\command-center-sensors` base. If Windows keeps a DLL locked during
shutdown, the next sensor-enabled process validates and removes matching
current-version stale trees before extracting a fresh copy. Startup
verification waits up to 15 seconds for that lazy cleanup and extraction to
converge to exactly one live directory; unresolved zero or multiple counts
still fail closed and sensors must be disabled.
```

Verification:
- Run `rg -n "fresh nonce directories|15 seconds|fail closed" docs/operations/windows-production.md`.

Verification:
- Run the complete Windows suite:
  `pwsh -NoLogo -NoProfile -Command "Import-Module Pester -MinimumVersion 5.0; Invoke-Pester -Path 'ops/production/windows/tests' -Output Detailed"`.
- Run the focused Java test:
  `$env:GRADLE_USER_HOME=Join-Path $env:TEMP 'gradle-codex-cpu-stale'; .\gradlew.bat :website:test --tests "dev.christopherbell.admin.commandcenter.metrics.SecureNativeLibraryProvisionerTest" --no-daemon`.
- Run the full build:
  `$env:GRADLE_USER_HOME=Join-Path $env:TEMP 'gradle-codex-cpu-stale'; .\gradlew.bat build --no-daemon`.
- Run `git diff --check`, `git status --short --branch`, and review `git diff origin/main...HEAD`.
- Request independent review and resolve findings test-first.

- [ ] **Step 1: Apply Code Edit 3.1.**
- [ ] **Step 2: Run focused Java and Pester tests.**
- [ ] **Step 3: Run the complete Windows suite.**
- [ ] **Step 4: Run the full Gradle build.**
- [ ] **Step 5: Request independent review and resolve findings test-first.**
- [ ] **Step 6: Commit the spoke changes.**
- [ ] **Step 7: Push the branch and open a draft PR.**
- [ ] **Step 8: Wait for all required GitHub checks, mark ready, and squash-merge.**

### Task 4 - Deploy and prove CPU temperature in production

Sequence / dependencies:
- Runs only after Task 3 is merged and the immutable merge SHA is known.
- Uses the existing guarded one-click elevated acceptance path, updated to the new merged worktree.

Implementation notes:
- Verify production is healthy with sensors disabled before deployment.
- Deploy through the supported native Windows production command.
- Do not manually remove the six stale directories; prove the merged Java lifecycle removes them.
- Keep automatic sensor-disable rollback on every failure.

Verification:
- Confirm installed release SHA equals the merge SHA.
- Confirm `sensor-status` reports version `2.2.0.0`, driver `Running`, signature `Valid`, uninstall registration present, zero active threats, and disabled state.
- Capture the sensor-directory count before enablement; expect the six protected stale directories may remain.
- Run `sensor-enable`.
- During enablement, poll the directory count and record convergence to exactly one.
- Run `verify-startup`; require direct CPU Celsius `>0` and `<126`.
- Observe three 30-second windows and require plausible temperature values.
- Require no more than one application CPU probe process except brief overlap with the explicit direct verifier; require no monotonic accumulation.
- Confirm `ChristopherBellDev`, MongoDB, and cloudflared remain `Running` and `Automatic`.
- Confirm no new Service Control Manager event 7031.
- Confirm local and public homepage status `200`, response body marker `<title>CB | Home</title>`, and local byte count.
- Recheck Defender after the observation window.
- If any check fails, run `sensor-disable` and verify the site.

- [ ] **Step 1: Prepare a merged-source detached worktree and update the guarded acceptance launcher.**
- [ ] **Step 2: Run elevated pre-deploy and provider checks.**
- [ ] **Step 3: Deploy the immutable merge if needed.**
- [ ] **Step 4: Enable sensors and capture stale-to-one directory convergence.**
- [ ] **Step 5: Capture direct Celsius and three refresh-window samples.**
- [ ] **Step 6: Recheck probe counts, Defender, services, restart events, and HTTP bodies.**
- [ ] **Step 7: Preserve the success result or disable sensors automatically on failure.**

### Task 5 - Save delivery evidence and close the active work

Sequence / dependencies:
- Runs after successful production acceptance.

Implementation notes:
- Save concrete runtime evidence rather than status codes alone.
- Refresh indexes and validate Builder state before each required checkpoint.

Verification:
- Test report includes red/green tests, full local suites, PR/merge, deployed SHA, pre/post directory counts, direct and refresh Celsius values, probe counts, Defender state, services, event record IDs, local/public response bodies, and rollback behavior.
- Spoke update and review link the branch, commit, PR, merge, and test report.
- Closure updates the active command-center work record.
- Session memory records the stale-directory root cause, secure cleanup boundary, and production result.

- [ ] **Step 1: Save and validate the production test report.**
- [ ] **Step 2: Commit and push the Builder test-report checkpoint.**
- [ ] **Step 3: Ingest and review the spoke result.**
- [ ] **Step 4: Close the active work with validation links and known gaps.**
- [ ] **Step 5: Save session memory, refresh indexes, validate hub state, commit, and push Builder main.**

## Code Changes

### `SecureNativeLibraryProvisionerTest.java`

- Replace the preexisting-directory rejection test with Code Edit 1.1.
- Add the stale-link safety regression in Code Edit 1.2.

### `SecureNativeLibraryProvisioner.java`

- Add the extraction-directory naming constants in Code Edit 1.3.
- Invoke stale cleanup before creation in Code Edit 1.4.
- Add strict validated cleanup helpers in Code Edit 1.5.

### `Production.Sensors.Tests.ps1`

- Add bounded-wait convergence and timeout-count regressions in Code Edit 2.1.

### `Production.Sensors.psm1`

- Add the bounded resource wait in Code Edit 2.2.
- Route direct verification through it in Code Edit 2.3.

### `windows-production.md`

- Add Code Edit 3.1 documenting the stale cleanup and exact-one wait contract.

## Files and Modules

- Modify `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java`.
- Modify `website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java`.
- Modify `ops/production/windows/modules/Production.Sensors.psm1`.
- Modify `ops/production/windows/tests/Production.Sensors.Tests.ps1`.
- Modify `docs/operations/windows-production.md`.

## Unit Testing

- Java red/green regression for stale directory removal.
- Java safety regression for stale-tree symbolic links.
- Pester red/green regression for multiple-to-one convergence.
- Pester timeout regression containing the final observed count.
- Complete Java test class and Windows production suite.
- Full Gradle build including JavaScript and sensor resource verification.

## Local Testing

- Run all development tests in the isolated spoke worktree.
- Use an isolated `GRADLE_USER_HOME`.
- Do not touch production before merge.
- Inspect the full deletion diff for direct-child containment, `NOFOLLOW_LINKS`, ACL validation, validation-before-deletion, and bottom-up ordering.
- Inspect the wait diff for bounded duration, exact poll interval, and unchanged downstream security checks.

## Validation

- New Java and Pester tests are observed failing for the intended missing behavior.
- Focused tests pass after minimal implementation.
- Complete Pester and Gradle suites pass.
- Independent review reports no blockers.
- Required GitHub checks pass and PR is merged.
- Production converges from stale directories to exactly one live directory without manual deletion.
- Direct and cached CPU temperatures are plausible across three windows.
- Probe processes, Defender, services, event records, and HTTP responses remain healthy.
- Builder artifacts are validated, committed, and pushed.

## Rollback or Recovery

- Keep sensors disabled until merged deployment.
- Revert the spoke commit before merge if validation or review finds unsafe deletion scope.
- Use existing release rollback if the merged application cannot start.
- Run `sensor-disable` automatically on any production acceptance failure.
- Leave PawnIO installed unless separately proven invalid.
- Do not broaden deletion or ACL permissions to force cleanup.

## Risks

- A matching stale tree could contain a reparse point. Mitigation: validate every path without following links before deleting any entry.
- A second application instance could still own a directory. Mitigation: the service contract permits one instance; active DLL locks cause strict deletion failure and fail-closed enablement rather than forced removal.
- Strict cleanup could fail on a lingering Windows lock. Mitigation: provisioning fails safely, the bounded verifier reports the count, and sensors roll back to disabled.
- A 15-second wait could delay failure reporting. Mitigation: this is bounded and matches observed first-sample timing with margin.
- Pester mocks could accidentally test only mock behavior. Mitigation: tests assert the actual helper loop and command invocation counts; production acceptance proves real filesystem convergence.
- Existing six directories are protected and inaccessible to the interactive user. Mitigation: cleanup runs in the SYSTEM service under the existing ACL contract.

## Completion Criteria

- The stale-resource repair PR is merged and deployed.
- The six-directory production state converges to exactly one live protected directory during enablement.
- `verify-startup` returns a plausible direct CPU temperature.
- Three refresh windows produce plausible CPU temperatures without process accumulation.
- Defender reports no active PawnIO or WinRing0 threat.
- All production services remain `Running` and `Automatic`, no new 7031 event occurs, and local/public homepage checks pass.
- CPU-temperature sensors remain enabled only if every acceptance gate passes.
- Builder test, update, review, closure, and session-memory artifacts are validated, committed, and pushed.
