# christopherbell.dev WinSW Log Rotation Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the WinSW rotation mode that orphaned production at midnight, recover service ownership safely, and then complete live CPU-temperature enablement.

**Architecture:** Keep the pinned WinSW 2.12.0 binary and change only its service logging policy from combined time-and-size rotation to bounded size-only rotation. Prove the XML contract with Pester, deploy through the existing guarded native Windows workflow, perform one verified orphan-tree recovery, and resume the already-merged PawnIO sensor acceptance sequence only after the Windows service is stable.

**Tech Stack:** PowerShell 7, Pester 5, WinSW 2.12.0, Windows Service Control Manager, Java 25, Spring Boot, Gradle, GitHub Actions, CodeQL, PawnIO 2.2.0.0, LibreHardwareMonitor 0.9.6, Microsoft Defender.

## Global Constraints

- Do not upgrade to a WinSW prerelease.
- Do not change MongoDB or cloudflared.
- Do not reboot or power off the computer.
- Do not weaken ProgramData ACLs, Defender settings, installer verification, or sensor fail-closed behavior.
- Do not terminate unrelated Java or PowerShell processes.
- Do not enable sensors while the website is running outside the Windows service.
- Keep the WinSW size threshold at exactly `10240` KiB (10 MiB) and retention at exactly seven rolled files.
- Keep `sensorLibrariesEnabled=false` until service recovery and stability checks pass.

---

## Document Status

`ready-for-execution`

## Objective

Deliver and deploy a narrow WinSW configuration correction, restore `ChristopherBellDev` as the actual owner of the production process tree and port 8080, prove the restart loop has stopped, and then finish CPU-temperature provider acceptance.

## Goals

- Add a regression that fails against `roll-by-size-time`.
- Switch `ChristopherBellDev.xml` to bounded `roll-by-size`.
- Preserve `C:\ProgramData\christopherbell.dev\logs\ChristopherBellDev.out.log`.
- Pass the complete local and GitHub verification suites.
- Recover the orphaned production process tree without touching unrelated processes.
- Confirm service stability for at least two minutes.
- Confirm PawnIO and Defender health, enable the provider, and prove a plausible CPU temperature across three refresh windows.
- Save Builder test, closure, and session-memory artifacts.

## Inputs

- Approved spec: `docs/specs/2026-07-16-christopherbell-dev-winsw-log-rotation-recovery.md`
- Existing CPU remediation spec: `docs/specs/2026-07-13-command-center-cpu-temperature-provider-remediation.md`
- Existing active work record: `docs/work/2026-07-12-command-center-cpu-temperature-and-uptime.md`
- Approved user decision: use size-only rotation and the guarded recovery sequence.
- Production evidence: first service failure at `2026-07-13 00:00:02`, current port 8080 listener is an orphaned SYSTEM Java/PowerShell tree, and Service Control Manager has repeatedly retried the stopped WinSW service.
- Upstream evidence: WinSW issue 1034 documents `roll-by-size-time` failing at time rollover while a Java application writes to console output.

## Branch

- Base: refreshed `origin/main` at or after merge `0459aafa24d5078767fd74141a8978d99f2e6e69`
- Branch: `codex/winsw-log-rotation-recovery`
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\winsw-log-rotation-recovery`

## Non-Goals

- No new HTTP endpoint or command-center action.
- No generic process-killer command.
- No WinSW binary or checksum change.
- No change to application logging format, command-center log redaction, or log API behavior.
- No PawnIO reinstall unless status verification proves the existing installation is invalid.
- No computer restart or shutdown acceptance test.

## Assumptions

- `origin/main` remains the canonical deployment source.
- The existing `prod.ps1 install` operation safely refreshes the service XML and restores standard service recovery settings.
- The current orphan tree can be distinguished by port 8080 ownership, SYSTEM session, `java.exe` child identity, and a `pwsh.exe` parent running `Start-ChristopherBellDev.ps1`.
- Size-only rotation is supported by pinned WinSW 2.12.0.
- Production elevation will be available for the final recovery and sensor operations; if not, execution stops without weakening permissions.

## Open Questions

None.

## File Structure

- `ops/production/windows/service/ChristopherBellDev.xml`: owns WinSW service lifecycle and output-log retention configuration.
- `ops/production/windows/tests/Production.Command.Tests.ps1`: owns command-surface, runbook, and real service-definition regression checks.
- `docs/operations/windows-production.md`: owns operator diagnostics and the warning against time-based WinSW rotation.
- Builder artifacts under `docs/test-reports`, `docs/spoke-updates`, `docs/spoke-reviews`, `docs/work-closures`, and `docs/session-memory`: own durable delivery evidence after production acceptance.

## Task Breakdown

### Task 1 - Enforce bounded size-only WinSW logging

Sequence / dependencies:
- Runs first because all later deployment and production recovery steps depend on a corrected service definition.
- Use test-driven development: add the XML regression, observe its expected failure, then change the XML.

Implementation notes:
- Parse the real XML rather than matching raw text so formatting changes do not weaken the test.
- Check positive requirements (`roll-by-size`, threshold, retention) and negative requirements (no time boundary or filename pattern).
- Keep the edit limited to logging configuration and runbook guidance.

#### Code Edit 1.1
- File: `ops/production/windows/tests/Production.Command.Tests.ps1`
- Lines: after 79
- Action: add

Proposed:
```powershell
    It 'uses bounded size-only WinSW log rotation' {
        $root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
        [xml]$service = Get-Content (
            Join-Path $root 'ops\production\windows\service\ChristopherBellDev.xml') -Raw
        $log = $service.service.log

        [string]$log.mode | Should -Be 'roll-by-size'
        [int]$log.sizeThreshold | Should -Be 10240
        [int]$log.keepFiles | Should -Be 7
        $log.autoRollAtTime | Should -BeNullOrEmpty
        $log.pattern | Should -BeNullOrEmpty
    }
```

Verification:
- Run `pwsh -NoLogo -NoProfile -Command "Import-Module Pester -MinimumVersion 5.0; Invoke-Pester -Path 'ops/production/windows/tests/Production.Command.Tests.ps1' -Output Detailed"`.
- Before Code Edit 1.2, expect one failure: actual mode `roll-by-size-time` does not equal `roll-by-size`.

#### Code Edit 1.2
- File: `ops/production/windows/service/ChristopherBellDev.xml`
- Lines: 15-21
- Action: replace

Current:
```xml
  <log mode="roll-by-size-time">
    <sizeThreshold>10240</sizeThreshold>
    <pattern>yyyyMMdd</pattern>
    <autoRollAtTime>00:00:00</autoRollAtTime>
    <zipOlderThanNumDays>7</zipOlderThanNumDays>
    <zipDateFormat>yyyyMMdd</zipDateFormat>
  </log>
```

Proposed:
```xml
  <log mode="roll-by-size">
    <sizeThreshold>10240</sizeThreshold>
    <keepFiles>7</keepFiles>
  </log>
```

Verification:
- Re-run the focused Pester command and expect all command-surface tests to pass.
- Parse the XML with `[xml] (Get-Content ... -Raw)` and expect no XML parser error.

#### Code Edit 1.3
- File: `docs/operations/windows-production.md`
- Lines: after 223
- Action: add

Proposed:
```markdown
- WinSW keeps seven 10 MiB output logs with size-only rotation. Do not use
  `roll-by-size-time` or `autoRollAtTime`: WinSW can break the output stream at
  a live time boundary and leave the Java child running outside the service.
- If `ChristopherBellDev` is stopped while port 8080 still responds, treat the
  listener as a possible orphan. Verify the listener PID and its full parent
  chain before terminating anything, refresh the installed service definition,
  and require `verify-startup` to pass before resuming sensor operations.
```

Verification:
- Run `rg -n "size-only rotation|possible orphan|roll-by-size-time" docs/operations/windows-production.md`.
- Expect all three diagnostic phrases and no documentation contradiction with the XML.

- [ ] **Step 1: Add Code Edit 1.1 only.**
- [ ] **Step 2: Run the focused Pester test and record the expected red failure.**
- [ ] **Step 3: Apply Code Edits 1.2 and 1.3.**
- [ ] **Step 4: Re-run focused Pester and expect all tests green.**
- [ ] **Step 5: Run `git diff --check` and inspect the complete task diff.**
- [ ] **Step 6: Commit with `git commit -m "Avoid WinSW time rotation deadlock"`.**

### Task 2 - Complete local verification and publish the fix

Sequence / dependencies:
- Runs after Task 1 is committed and focused tests are green.
- Must finish before any production mutation.

Implementation notes:
- Use an isolated `GRADLE_USER_HOME` because the shared daemon registry can be ACL-blocked on this host.
- Request independent review before pushing.
- Publish as a draft PR, wait for all required checks, then squash-merge and delete the remote branch.

Verification:
- Run the complete Windows suite:
  `pwsh -NoLogo -NoProfile -Command "Import-Module Pester -MinimumVersion 5.0; Invoke-Pester -Path 'ops/production/windows/tests' -Output Detailed"`.
- Expect zero failures; the two administrator-only ACL integration tests may be skipped in the non-elevated run.
- Run the full build:
  `$env:GRADLE_USER_HOME=Join-Path $env:TEMP 'gradle-codex-winsw-recovery'; .\gradlew.bat build --no-daemon`.
- Expect `BUILD SUCCESSFUL`, all Java tests green, all JavaScript tests green, and `verifySensorRuntime` green.
- Run `git status --short --branch`, `git diff --check origin/main...HEAD`, and independent review.

- [ ] **Step 1: Run the complete Pester suite.**
- [ ] **Step 2: Run the full Gradle build with isolated state.**
- [ ] **Step 3: Request independent review and resolve any findings test-first.**
- [ ] **Step 4: Push `codex/winsw-log-rotation-recovery`.**
- [ ] **Step 5: Open a draft PR with root-cause and verification evidence.**
- [ ] **Step 6: Wait for every required GitHub check to pass.**
- [ ] **Step 7: Mark ready and squash-merge.**

### Task 3 - Recover production service ownership

Sequence / dependencies:
- Runs only after Task 2 is merged and `origin/main` identifies the immutable merge SHA.
- Must complete before Task 4 can inspect or enable sensors.

Implementation notes:
- This is a guarded elevated operation. If elevation is unavailable, mark execution blocked and do not attempt ACL, Defender, or service bypasses.
- Capture all pre-recovery evidence before terminating the orphan.
- Temporarily clear service recovery actions so SCM cannot race the repair.
- The verified target must be the port 8080 `java.exe`, in session 0, with a `pwsh.exe` parent whose command line contains `C:\ProgramData\christopherbell.dev\service\Start-ChristopherBellDev.ps1`; the Java command line must reference the production `current\app.jar`.
- Terminate the Java child first and its verified PowerShell parent second. Refuse any mismatch.
- Run the merged `prod.ps1 install` to refresh XML and restore the configured recovery actions.

Verification:
- Record the pre-recovery System event count for Service Control Manager event 7031 and the current listener/parent chain.
- Confirm `sensorLibrariesEnabled` is Boolean `false`.
- Confirm the installed XML contains `roll-by-size`, threshold `10240`, and `keepFiles` `7`.
- Start `ChristopherBellDev`, then wait conditionally until it is `Running` and port 8080 has exactly one listener.
- Confirm the listener belongs to the new service-owned PowerShell/Java process tree, not the old PIDs.
- Run `prod.ps1 verify-startup`; expect all three services `Running` and `Automatic`, protected state valid, local status `200`, and public status `200`.
- Check local and public response bodies for `<title>CB | Home</title>`.
- Poll service state and 7031 count for at least two minutes; expect `Running` throughout and no count increase.

- [ ] **Step 1: Run the elevated read-only pre-recovery audit.**
- [ ] **Step 2: Disable SCM recovery actions temporarily.**
- [ ] **Step 3: Verify and terminate only the orphan Java/PowerShell tree.**
- [ ] **Step 4: Refresh installed service files through merged `prod.ps1 install`.**
- [ ] **Step 5: Start the service and verify its listener ownership.**
- [ ] **Step 6: Run startup, HTTP-body, ACL, task, and two-minute stability checks.**
- [ ] **Step 7: If any gate fails, keep sensors disabled and use the existing release rollback workflow.**

### Task 4 - Enable and prove CPU temperature

Sequence / dependencies:
- Runs only after Task 3 passes every service stability gate.

Implementation notes:
- Reuse the merged exact-version hotfix; do not reinstall PawnIO unless the existing installation fails verification.
- Enable only through `sensor-enable`, which rolls configuration back on endpoint failure.
- Direct startup verification is authoritative; a UI card alone is not enough.

Verification:
- Run elevated `sensor-status`; expect:
  - `PawnIoVersion=2.2.0.0`
  - driver `Running`
  - driver signature `Valid`
  - verified uninstall registration present
  - zero active WinRing0/PawnIO Defender threats
  - sensors disabled before enablement
- Run `sensor-enable`, followed immediately by `verify-startup`.
- Expect a direct CPU temperature strictly greater than `0` and less than `126` Celsius.
- Sample the command-center CPU-temperature metric for at least three 30-second refresh windows.
- Count production-descendant PowerShell probe processes during the window; expect no monotonic accumulation.
- Recheck Defender threats, service state, local/public HTTP, and service failure events.
- If any check fails, run `sensor-disable`, verify the site, and preserve the failure evidence.

- [ ] **Step 1: Capture verified provider, signature, Defender, and disabled-state evidence.**
- [ ] **Step 2: Run `sensor-enable`.**
- [ ] **Step 3: Run `verify-startup` and capture the direct Celsius value.**
- [ ] **Step 4: Observe three application refresh windows and process stability.**
- [ ] **Step 5: Recheck Defender, services, HTTP, and restart events.**
- [ ] **Step 6: Disable sensors immediately if any acceptance gate fails.**

### Task 5 - Save delivery evidence and close the active work

Sequence / dependencies:
- Runs after Task 4 succeeds, or records a blocked result if elevation or hardware verification prevents completion.

Implementation notes:
- Save concrete request/response and runtime evidence, not status codes alone.
- Update indexes and validate hub state before every Builder checkpoint commit.

Verification:
- Test report must name the merge SHA, installed production SHA, service PIDs, local/public response codes and title marker, 7031 stability interval, PawnIO state, direct Celsius samples, process counts, Defender result, and any gaps.
- Spoke update/review and closure records must link the PR, merge, test report, and active work.
- Session memory must explain the midnight WinSW root cause and the final CPU-temperature result.

- [ ] **Step 1: Save and validate the production test report.**
- [ ] **Step 2: Commit and push the Builder test-report checkpoint.**
- [ ] **Step 3: Ingest and review the spoke result.**
- [ ] **Step 4: Update or close the active CPU-temperature work record.**
- [ ] **Step 5: Save session memory, refresh indexes, validate hub state, commit, and push Builder main.**

## Code Changes

### `ops/production/windows/tests/Production.Command.Tests.ps1`

- Add Code Edit 1.1: parse the real service XML and enforce size-only bounded rotation.

### `ops/production/windows/service/ChristopherBellDev.xml`

- Apply Code Edit 1.2: replace combined time-and-size rotation with size-only rotation and seven-file retention.

### `docs/operations/windows-production.md`

- Add Code Edit 1.3: document the unsafe WinSW mode and guarded orphan diagnostic sequence.

## Files and Modules

- Modify `ops/production/windows/tests/Production.Command.Tests.ps1`.
- Modify `ops/production/windows/service/ChristopherBellDev.xml`.
- Modify `docs/operations/windows-production.md`.
- Use without modification:
  - `ops/production/windows/prod.ps1`
  - `ops/production/windows/modules/Production.Install.psm1`
  - `ops/production/windows/modules/Production.Operations.psm1`
  - `ops/production/windows/modules/Production.Sensors.psm1`

## Unit Testing

- Focused Pester red/green test for the real WinSW XML.
- Complete Pester production suite after implementation.
- Full Gradle build, including Java, JavaScript, and sensor resource verification.
- No new Java unit test is required because the defect and correction are confined to WinSW XML and PowerShell-run operational validation.

## Local Testing

- All local tests run in the isolated spoke worktree.
- No local production service mutation occurs before merge.
- Production recovery runs elevated only after the merge SHA is known.
- HTTP evidence includes response byte counts and `<title>CB | Home</title>`.
- Stability verification uses condition polling and event-count comparison rather than an arbitrary single snapshot.

## Validation

- XML regression observed red before implementation and green afterward.
- Complete local test suites pass.
- Independent review reports no blocking findings.
- Required GitHub checks pass and the PR is merged.
- Installed production XML matches the merged source.
- `ChristopherBellDev` remains `Running` and owns port 8080 for at least two minutes with no new event 7031 failures.
- Local and public sites return the expected homepage.
- PawnIO 2.2.0.0 and its driver pass signature and Defender checks.
- CPU temperature returns plausible direct values across three refresh windows without PowerShell accumulation.
- Builder test, review, closure, and memory artifacts are committed and pushed.

## Rollback or Recovery

- Keep `sensorLibrariesEnabled=false` until service recovery passes.
- If size-only XML fails local validation, revert the Task 1 commit before publishing.
- If the merged service cannot start after verified orphan cleanup, run the existing production rollback command and verify endpoints.
- If sensor enablement fails, run `sensor-disable` and verify the service before further investigation.
- Do not delete PawnIO driver files; use only its verified registered uninstaller if a provider or Defender issue requires removal.

## Risks

- The live orphan is currently serving production; terminating it creates a brief outage until the service starts. Mitigation: merge and install the corrected XML first, prepare all verification commands, and terminate only immediately before service start.
- SCM recovery can race the repair. Mitigation: temporarily clear recovery actions and restore them through `prod.ps1 install`.
- A wrong PID could terminate unrelated work. Mitigation: require port, executable, session, parent, command-line, and production-jar identity checks.
- Size-only rotation could expose another WinSW defect at 10 MiB. Mitigation: retain explicit monitoring, bounded files, and the ability to move to application-owned file logging in a separately approved design if evidence shows a size-rotation failure.
- Elevation may remain unavailable in Codex. Mitigation: stop safely and request the minimum explicit administrator action; do not weaken ACLs or Defender.
- Hardware access may still return no temperature. Mitigation: fail closed, disable sensors, and preserve a healthy service.

## Completion Criteria

- The service configuration fix is merged and deployed.
- The orphan process tree is gone.
- `ChristopherBellDev`, MongoDB, and cloudflared are `Running` and `Automatic`.
- Port 8080 belongs to the service-owned process tree.
- No new 7031 failure occurs during the stability interval.
- Local/public homepage checks pass with the expected title.
- Sensor verification either produces stable plausible Celsius readings with no process leak and clean Defender state, or records a precise blocked hardware/provider result while leaving sensors disabled and production healthy.
- All required Builder artifacts are validated, committed, and pushed.
