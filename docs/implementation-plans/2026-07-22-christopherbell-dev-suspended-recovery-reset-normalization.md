# ChristopherBell.dev Suspended Recovery Reset Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to execute this plan. Every production-code edit and review must use `write-jane-street-style-code` in the appropriate mode.

**Goal:** Align the controlled website-stop recovery mutation and verifier with Windows' canonical empty-action representation so pinned deployment can stop the service safely and restore normal recovery afterward.

**Architecture:** Preserve the existing `Suspended`/`Normal` state boundary. Derive one reset value from that state—`0` for suspended and `3600` for normal—and use it for both the `sc.exe failure` mutation and `qfailure` verification. Keep all bounded-process, restoration, stop-postcondition, and causal-error behavior unchanged.

**Tech Stack:** PowerShell 7, Pester 5, Windows Service Control Manager, WinSW 2.12.0, Gradle, GitHub Actions, CodeQL.

## Document Status

`ready-for-execution`

## Objective

Deliver the narrow SCM normalization correction, prove it test-first against the production-observed output, merge it through all gates, and rerun the rollback-ready shared-folder production acceptance through authenticated browser validation.

## Goals

- Send and require reset period `0` when recovery actions are suspended.
- Keep normal recovery at reset period `3600` with ordered 10-second and 30-second restarts.
- Reject missing, ambiguous, or policy-inappropriate reset/action state before service stop.
- Preserve normal recovery restoration after every suspension attempt.
- Complete focused/full verification, independent reviews, PR/CI/merge, exact-release deployment, browser acceptance, and Builder closeout.

## Inputs

- Approved spec: `docs/specs/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md`.
- Merged worker fix: PR 1222, commit `aed86dae3076fbee5fc14ee57025d78c0eddc3e1`, tree `92e44a1fb2f24fe53b7ccad2a3c35d88fd0cf37a`.
- Production evidence: suspended mutation requested empty actions and reset `3600`; Windows reported reset `0` and no actions; the verifier restored normal recovery and aborted before stop.
- Verified rollback evidence: `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-result.json` reports the safe baseline restored.
- User-approved design: suspended reset `0`, normal reset `3600`, no widened acceptance set.

## Branch

- Base: exact `origin/main` commit `aed86dae3076fbee5fc14ee57025d78c0eddc3e1`.
- Branch: `codex/suspended-recovery-reset-normalization`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker`.
- Preserve the dirty primary checkout at `A:\Projects\christopherbell.dev`.

## Non-Goals

- No WinSW, worker lifecycle, application, permission, storage, UI, or media changes.
- No acceptance of both `0` and `3600` for suspended policy.
- No change to normal recovery actions or reset period.
- No direct production module patch before merge.
- No shared-root or data cleanup.

## Assumptions

- Windows reports reset `0` when recovery actions are empty, as proven by the guarded elevated run.
- `sc.exe failure ... reset= 0 actions= ''` is the deliberate canonical suspended mutation.
- `Set-ProductionWebsiteRecoveryPolicy` remains the sole recovery mutation owner used by controlled stop.
- Production remains at the verified safe baseline until the follow-up merge.
- The corrected temporary installer and rollback scripts remain available for exact-identifier refresh after merge.

## Open Questions

None.

## Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: policy-specific reset mutation, verification, and diagnostic text.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: Windows-normalized fixture and controlled-stop regression assertions.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`: post-merge immutable SHA/tree refresh.
- `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`: matching rollback SHA/tree refresh.
- Builder test, update, review, closure, and session-memory artifacts: durable delivery evidence.

## Task Breakdown

### Task 1 - Normalize suspended recovery test-first

Required skill: `write-jane-street-style-code` in Implementation Mode.

Sequence and dependencies:

- Create the new branch from the exact merged base.
- Add the observed suspended-output regression only and capture RED before module changes.
- Make reset derivation policy-specific in mutation, verification, diagnostics, and the command double.
- Run focused/full Windows validation and task review before commit/push.

Before-Edit Brief:

- **Behavior:** `Suspended` requests and verifies reset `0` plus no actions; `Normal` requests and verifies reset `3600` plus two ordered restart actions.
- **Invariants:** Recovery commands remain bounded; no stop occurs until suspension is exactly verified; every suspension attempt restores and verifies normal recovery; normal recovery semantics do not change.
- **Boundary/API:** Keep the public `Assert-ProductionWebsiteRecoveryPolicy` and `Set-ProductionWebsiteRecoveryPolicy` signatures. Derive reset values internally from the existing validated policy enum.
- **Effects and failures:** Only the arguments passed to the existing bounded `sc.exe` mutation change for suspended policy. Missing/mismatched query fields throw policy-specific diagnostics before any service effect.
- **Tests and evidence:** Capture RED against reset `0` observed output, then assert exact suspended/normal mutation arguments, policy separation, mismatches, restoration ordering, parser success, and full suite counts.

#### Code Edit 1.1

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: after 113
- Action: add

Proposed:

```powershell
        It 'accepts the Windows-normalized suspended policy with reset period zero' {
            $queryOutput = New-RecoveryPolicyQueryOutput `
                -Policy Suspended -ResetPeriodSeconds 0

            {
                Assert-ProductionWebsiteRecoveryPolicy `
                    -Policy Suspended -QueryOutput $queryOutput
            } | Should -Not -Throw
        }
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.Deploy.Tests.ps1" -FullNameFilter "*accepts the Windows-normalized suspended policy with reset period zero*" -PassThru -Output Detailed; if ($r.FailedCount -ne 1) { exit 1 }'`.
- Expect one RED failure stating that suspended recovery expected reset `3600` but received reset `0`.
- Do not alter production code before recording that failure.

#### Code Edit 1.2

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 147-256
- Action: replace

Current:

```powershell
    $matchesExpectedPolicy = if ($Policy -eq 'Suspended') {
        $resetPeriodSeconds -eq 3600 -and
            $hasEmptyActions -and
            $delayLineCount -eq 0 -and
            $actualActions.Count -eq 0
    } else {
        $resetPeriodSeconds -eq 3600 -and
        # normal action checks
    }

    # Both mutation paths currently pass reset value 3600.
```

Proposed:

```powershell
    $expectedResetPeriodSeconds = if ($Policy -eq 'Suspended') { 0 } else { 3600 }
    $matchesExpectedPolicy = if ($Policy -eq 'Suspended') {
        $resetPeriodSeconds -eq $expectedResetPeriodSeconds -and
            $hasEmptyActions -and
            $delayLineCount -eq 0 -and
            $actualActions.Count -eq 0
    } else {
        $resetPeriodSeconds -eq $expectedResetPeriodSeconds -and
            $delayLineCount -eq 2 -and
            $actualActions.Count -eq 2 -and
            $actualActions[0] -eq 'RESTART:10000' -and
            $actualActions[1] -eq 'RESTART:30000'
    }

    # Diagnostic text uses $expectedResetPeriodSeconds.

    $resetPeriodSeconds = if ($Policy -eq 'Normal') { 3600 } else { 0 }
    Invoke-BoundedCheckedProcess -FilePath 'sc.exe' -ArgumentList @(
        'failure',
        'ChristopherBellDev',
        'reset=',
        [string]$resetPeriodSeconds,
        'actions=',
        $actions
    ) -TimeoutMilliseconds $RecoveryCommandTimeoutMilliseconds | Out-Null
```

Verification:

- Re-run Code Edit 1.1's focused test and require 1 passed, 0 failed.
- Run a parser check for `Production.Deploy.psm1` and require zero errors.
- Inspect that `Normal` still derives `3600` and its action list is unchanged.

#### Code Edit 1.3

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: 29-185
- Action: replace

Current:

```powershell
            function New-RecoveryPolicyQueryOutput {
                param(
                    [ValidateSet('Suspended','Normal')]
                    [string]$Policy,
                    [int]$ResetPeriodSeconds = 3600
                )
                # ...
            }

            # Successful controlled stop expects suspended reset argument 3600.
```

Proposed:

```powershell
            function New-RecoveryPolicyQueryOutput {
                param(
                    [ValidateSet('Suspended','Normal')]
                    [string]$Policy,
                    [Nullable[int]]$ResetPeriodSeconds
                )

                $effectiveResetPeriodSeconds = if ($null -ne $ResetPeriodSeconds) {
                    [int]$ResetPeriodSeconds
                } elseif ($Policy -eq 'Suspended') {
                    0
                } else {
                    3600
                }
                # Render $effectiveResetPeriodSeconds in RESET_PERIOD.
            }

            # Successful controlled stop expects suspended reset argument 0.
            # Normal restoration continues to expect reset argument 3600.
```

Add or update assertions proving:

```powershell
        It 'rejects reset period zero for normal recovery' {
            $queryOutput = New-RecoveryPolicyQueryOutput `
                -Policy Normal -ResetPeriodSeconds 0
            {
                Assert-ProductionWebsiteRecoveryPolicy `
                    -Policy Normal -QueryOutput $queryOutput
            } | Should -Throw '*Expected reset period 3600*received reset period 0*'
        }

        # Existing mismatch coverage keeps reset 42 invalid for suspended policy.
        # The successful stop assertion requires reset argument 0 for suspension.
        # Restoration still requires reset argument 3600 and both restart actions.
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.Deploy.Tests.ps1" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Run `git diff --check` and require exactly the module and deploy test file in scope.

- [ ] Step 1: Create `codex/suspended-recovery-reset-normalization` from exact `origin/main`.
- [ ] Step 2: Add Code Edit 1.1 only and capture the behavioral RED failure.
- [ ] Step 3: Apply Code Edit 1.2 and turn the observed-output regression green.
- [ ] Step 4: Apply Code Edit 1.3, preserving all existing failure and restoration tests.
- [ ] Step 5: Run focused/full Pester, parsers, scope, and diff checks.
- [ ] Step 6: Complete independent task review, then commit/push `Normalize suspended SCM recovery reset`.

### Task 2 - Validate, review, publish, and merge

Required skill: `write-jane-street-style-code` in Review Mode.

Sequence and dependencies:

- Run after Task 1 is committed and pushed.
- Perform clean full build and fresh whole-branch review before PR.
- Merge only after every required GitHub gate passes.

Before-Edit Brief:

- **Behavior:** This task introduces no new code behavior; it proves the policy-specific fix is isolated and release-ready.
- **Invariants:** Review remains read-only until a finding is accepted; fixes return to Implementation Mode with behavioral or static evidence.
- **Boundary/API:** Compare only `origin/main...HEAD`; preserve production and unrelated checkout state.
- **Effects and failures:** Any build, review, or CI failure blocks merge and production retry.
- **Tests and evidence:** Full Windows Pester, isolated clean Gradle build, parsers, diff/scope, independent review, Ubuntu/macOS/Windows CI, and all CodeQL analyses.

Verification:

- Run full Windows Pester with explicit counts and zero failures.
- Run `$env:GRADLE_USER_HOME = Join-Path $env:TEMP 'gradle-codex-suspended-recovery-reset'; .\gradlew.bat clean build --no-daemon` and require `BUILD SUCCESSFUL`.
- Require no unresolved Critical, Important, or Minor whole-branch findings.
- Open a ready PR with live root cause and RED/GREEN evidence.
- Require all CI and CodeQL checks before squash merge.

- [ ] Step 1: Run the complete local verification matrix.
- [ ] Step 2: Complete fresh whole-branch Review Mode review.
- [ ] Step 3: Open the ready PR and wait for every gate.
- [ ] Step 4: Squash-merge and record immutable merge SHA/tree.

### Task 3 - Retry exact-release production acceptance

Required skill: `write-jane-street-style-code` in Implementation Mode for identifier refresh and Review Mode for preflight.

Sequence and dependencies:

- Run only after Task 2 is merged.
- Re-prove the safe baseline before mutation.
- Update both temporary scripts to the new immutable merge SHA/tree.
- Obtain independent read-only preflight approval before UAC.

Before-Edit Brief:

- **Behavior:** Prove absent-worker install, existing-worker reinstall, pinned release deploy, worker start/security, startup health, authorization boundaries, and authenticated shared-folder use.
- **Invariants:** Feature enablement follows both install passes; pinned deployment cannot drift; rollback stays independent of mutable `origin/main`; every success result is evidence-backed.
- **Boundary/API:** Modify only exact identifiers in the reviewed temporary scripts unless a newly observed safety issue requires another reviewed change.
- **Effects and failures:** Elevated install changes worker registration, feature configuration, website release/process, and worker state. Any failed gate runs rollback and proves the safe baseline.
- **Tests and evidence:** Script parser/preflight, exact release, two install passes, service contracts, installed-worker Pester, startup, HTTP, authenticated browser download/playback, and rollback evidence if needed.

#### Code Edit 3.1

- File: `A:\Temp\cbdev-shared-folder-production-20260722-064200\install-and-verify.ps1`
- Lines: 9-10
- Action: replace

Current:

```powershell
$expectedSha = 'aed86dae3076fbee5fc14ee57025d78c0eddc3e1'
$expectedTree = '92e44a1fb2f24fe53b7ccad2a3c35d88fd0cf37a'
```

Proposed:

```powershell
$expectedSha = '<NEW_IMMUTABLE_SQUASH_MERGE_SHA>'
$expectedTree = '<NEW_IMMUTABLE_SQUASH_MERGE_TREE>'
```

Verification:

- Parse the script and require zero errors.
- Verify source `HEAD^{tree}` equals the expected tree and fetched `origin/main` equals the expected SHA.

#### Code Edit 3.2

- File: `A:\Temp\cbdev-shared-folder-production-20260722-064200\rollback-failed-install.ps1`
- Lines: 10-11
- Action: replace

Current:

```powershell
$expectedSha = 'aed86dae3076fbee5fc14ee57025d78c0eddc3e1'
$expectedTree = '92e44a1fb2f24fe53b7ccad2a3c35d88fd0cf37a'
```

Proposed:

```powershell
$expectedSha = '<NEW_IMMUTABLE_SQUASH_MERGE_SHA>'
$expectedTree = '<NEW_IMMUTABLE_SQUASH_MERGE_TREE>'
```

Verification:

- Parse the rollback script and require zero errors.
- Confirm rollback source validation uses the immutable tree and does not depend on mutable `origin/main`.

- [ ] Step 1: Re-prove production safe baseline.
- [ ] Step 2: Refresh identifiers and complete independent preflight review.
- [ ] Step 3: Warn immediately before UAC and launch the guarded installer.
- [ ] Step 4: Require infrastructure result `infrastructure-passed-browser-pending`.
- [ ] Step 5: Use the logged-in browser session to prove `/shared`, permitted listing, download bytes, and progressive playback where a suitable file exists.
- [ ] Step 6: Run rollback and prove baseline on any failure.

### Task 4 - Close durable Builder work

Sequence and dependencies:

- Run only after successful browser acceptance or verified rollback.
- Record actual evidence and remaining gaps honestly.
- Commit and push every Builder phase artifact.

- [ ] Step 1: Save the local app test report with requests, responses, counts, service facts, and production result.
- [ ] Step 2: Save spoke update and independent review artifacts.
- [ ] Step 3: Close the shared-folder work only if the accepted feature is genuinely live; otherwise record the blocker.
- [ ] Step 4: Save session memory, refresh indexes, validate hub state, and commit/push.

## Code Changes

- Derive suspended reset period `0` and normal reset period `3600` from the existing recovery policy state.
- Use the derived value for both bounded SCM mutation and exact verification diagnostics.
- Make recovery-query fixtures default to Windows' policy-specific values.
- Assert suspended/normal separation and preserve all restoration/stop gates.
- Refresh post-merge temporary production identifiers only after the new immutable merge exists.

## Unit Testing

- Suspended `qfailure` with reset `0`, explicit empty actions, and no delay lines passes.
- Suspended reset `42`, missing reset, nonempty actions, or any delay line fails.
- Normal reset `0` fails; normal reset `3600` with exact ordered actions passes.
- Suspended mutation sends reset `0` and empty actions.
- Normal restoration sends reset `3600` and `restart/10000/restart/30000`.
- Suspension verification failure blocks `Stop-Service` and still restores normal recovery.
- Existing mutation/query timeout and aggregate-cause tests remain green.

## Local Testing

- Focused RED/GREEN run for the observed suspended query output.
- Complete `Production.Deploy.Tests.ps1` Pester run with explicit counts.
- Full `ops/production/windows/tests` Pester run with zero failures and expected administrator-only skips recorded.
- PowerShell parser validation for both edited files.
- `git diff --check` and exact two-file scope.
- Clean isolated Gradle build.
- Independent task and whole-branch Review Mode passes.
- Guarded production runtime acceptance plus separate authenticated browser validation.

## Validation

- RED evidence proves the prior verifier rejects reset `0`.
- GREEN evidence proves exact suspended/normal semantics and restoration ordering.
- Local/full build and all GitHub checks pass.
- Production pinned deployment passes the previously failing suspension verification and completes exact-release switch.
- Worker and website contracts, HTTP health, authorization, download, and playback pass.
- Any failure restores and proves the safe baseline.

## Rollback or Recovery

- Before merge, production remains at the current verified safe baseline.
- During rollout, use the reviewed rollback script under the same exact source tree.
- Rollback removes the flag, proves or reloads a disabled runtime, removes or disables the worker, and asserts website/dependency/recovery/listener/root health.
- Never delete shared data, roots, current/previous releases, MongoDB data, or cloudflared configuration.

## Risks

- A policy-state mix-up could weaken normal recovery; explicit zero-versus-3600 separation tests prevent it.
- SCM output formatting may vary; labeled parsing remains fail-closed.
- Production can drift between merge and UAC; exact SHA/tree and in-lock pinning block unreviewed deployment.
- Browser acceptance depends on an authenticated permitted session and suitable shared files; infrastructure success remains explicitly pending until that gate passes.

## Completion Criteria

- Suspended recovery mutation and verification use reset `0`; normal recovery remains exact.
- Focused/full tests, parsers, build, and reviews pass.
- PR passes every CI/CodeQL gate and is squash-merged.
- Guarded production install reaches infrastructure-passed status without rollback.
- Authenticated shared-folder listing/download and applicable progressive playback pass.
- Builder evidence, closure, indexes, validation, and session memory are committed and pushed.
