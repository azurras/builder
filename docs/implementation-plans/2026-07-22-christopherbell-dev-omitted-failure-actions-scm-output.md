# ChristopherBell.dev Omitted Failure-Actions SCM Output Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Every production-code edit and review must use `write-jane-street-style-code` in the appropriate mode.

**Goal:** Make the Windows recovery-policy verifier accept the single production-observed suspended SCM representation while rejecting every labeled or actionable suspended failure-actions state.

**Architecture:** Preserve the existing `Suspended`/`Normal` policy boundary and parser. Change only suspended failure-action label cardinality from exactly one empty field to exactly zero fields, update the fixture to reproduce the captured Windows output, and add a negative regression for the former empty-field representation. Keep normal parsing and all service effects unchanged.

**Tech Stack:** PowerShell 7.6, Pester 5, Windows Service Control Manager, WinSW 2.12.0, Gradle, GitHub Actions, CodeQL.

## Global Constraints

- Suspended policy accepts exactly reset `0`, no `FAILURE_ACTIONS` label, no delay fragments, and no parsed actions.
- Normal policy remains exactly reset `3600`, one labeled `RESTART` at `10000` milliseconds, and one unlabeled continuation `RESTART` at `30000` milliseconds.
- Do not accept both omitted and empty suspended fields.
- Preserve bounded SCM commands, stop gating, unconditional normal restoration, stop postconditions, and causal error aggregation.
- Do not modify worker, application, permission, storage, UI, media, or shared-data behavior.
- Do not deploy unmerged code or touch the dirty primary checkout beyond read-only fetch/ref operations used by reviewed production tooling.

---

## Document Status

`ready-for-execution`

## Objective

Deliver a test-first, two-file parser correction from exact `origin/main`, prove it locally and independently, merge it through all required gates, and hand the immutable merge identifiers back to the existing guarded production-acceptance plan.

## Goals

- Reproduce the live 196-byte suspended query shape in the Pester fixture.
- Capture RED from the current parser before changing production code.
- Require zero suspended failure-action labels and reject the former empty label.
- Preserve every normal-policy, mutation, timeout, restoration, and stop-gating test.
- Complete clean build, independent reviews, PR, CI, CodeQL, and squash merge.
- Resume Task 3 of `2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md` after recording the new immutable merge SHA and tree.

## Inputs

- Approved spec: `docs/specs/2026-07-22-christopherbell-dev-omitted-failure-actions-scm-output.md`.
- Current merged base: `bebd4cd9c3f9c37eab8cb311484e018e35834d6d`.
- Current merged tree: `dab47627201edae0eab1000839528e0224620b13`.
- Captured temporary evidence: `A:\Temp\cbdev-shared-folder-production-20260722-064200\suspended-qfailure-output.txt`.
- Capture result: parser rejected; normal recovery restoration succeeded; subsequent HTTP status was 200 with 3912 UTF-8 bytes.
- Rollback result: active release `bebd4cd9c3f9c37eab8cb311484e018e35834d6d`, worker absent, flag absent, normal recovery restored, shared roots preserved.
- Standing user authorization permits routine workflow, merge, UAC, and rollout checkpoints without repeated approval pauses.

## Branch

- Base: exact `origin/main` commit `bebd4cd9c3f9c37eab8cb311484e018e35834d6d`.
- Branch: `codex/omitted-failure-actions-scm-output`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker`.
- Preserve the dirty primary checkout at `A:\Projects\christopherbell.dev`.

## Non-Goals

- No second reset-period change.
- No acceptance of an empty suspended `FAILURE_ACTIONS` label.
- No normal recovery parser or action change.
- No refactor of the bounded process runner or controlled-stop workflow.
- No WinSW, worker lifecycle, application, permission, storage, UI, or media change.
- No direct production module patch before merge.
- No shared-root or data cleanup.

## Assumptions

- The captured 196-byte output is the canonical suspended representation on this production Windows build.
- The absence of `FAILURE_ACTIONS` is meaningful only together with reset `0`, zero delay fragments, and zero recognized action lines.
- `Assert-ProductionWebsiteRecoveryPolicy` remains the sole trusted parser boundary used before controlled website stop.
- Production remains at the rollback-proven safe baseline until the follow-up merge.
- The existing guarded installer and rollback scripts remain available for immutable identifier refresh after merge.

## Open Questions

None.

## Task Breakdown

### Task 1 - Correct the suspended parser contract test-first

Sequence / dependencies:

- Create the branch from the exact base before edits.
- Apply Code Edits 1.1 and 1.2 only, then run the focused RED command.
- Apply Code Edit 1.3 only after the RED failure proves the live-shaped fixture reaches the parser boundary.
- Complete focused/full verification and independent task review before committing.

Implementation notes:

- Required skill: `write-jane-street-style-code` in Implementation Mode before any code edits.
- Required skill: `superpowers:test-driven-development` for the RED/GREEN sequence.
- Before-Edit Brief:
  - Behavior: suspended `qfailure` output with reset `0` and an omitted action field passes; any suspended action label still fails.
  - Invariants: normal parsing and action ordering remain exact; malformed or duplicated fields fail closed; no stop occurs until suspension verifies; restoration remains unconditional.
  - Boundary/API: preserve the public module function signature `Assert-ProductionWebsiteRecoveryPolicy -Policy Suspended-or-Normal -QueryOutput string` and existing callers.
  - Effects and failures: the parser edit is pure; SCM mutation, bounded subprocesses, service stop, restoration, and causal exceptions remain unchanged.
  - Tests and evidence: the updated live-shaped fixture must fail against current production code, pass after the minimal branch correction, and the former empty-field fixture must fail.

**Files:**

- Modify: `ops/production/windows/tests/Production.Deploy.Tests.ps1:29-59,191-201`
- Modify: `ops/production/windows/modules/Production.Deploy.psm1:170-209`

**Interfaces:**

- Consumes: captured Windows `sc.exe qfailure` text and the existing `Policy`/`QueryOutput` verifier interface.
- Produces: one strict suspended representation and the unchanged strict normal representation.

#### Code Edit 1.1

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: 43-50
- Action: replace

Current:

```powershell
                $failureActions = if ($Policy -eq 'Normal') {
                    @(
                        'FAILURE_ACTIONS              : RESTART -- Delay = 10000 milliseconds.',
                        '                               RESTART -- Delay = 30000 milliseconds.'
                    )
                } else {
                    @('FAILURE_ACTIONS              :')
                }
```

Proposed:

```powershell
                $failureActions = if ($Policy -eq 'Normal') {
                    @(
                        'FAILURE_ACTIONS              : RESTART -- Delay = 10000 milliseconds.',
                        '                               RESTART -- Delay = 30000 milliseconds.'
                    )
                } else {
                    @()
                }
```

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.Deploy.Tests.ps1" -FullNameFilter "*accepts the Windows-normalized suspended policy with reset period zero*" -PassThru -Output Detailed; if ($r.FailedCount -ne 1) { exit 1 }'`.
- Expect one RED failure with `Suspended recovery policy verification failed` because current production code still requires one labeled field.

#### Code Edit 1.2

- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: 191-201
- Action: replace

Current:

```powershell
        It 'rejects an empty failure-actions field followed by an unrecognized duplicate field' {
            $queryOutput = @(
                New-RecoveryPolicyQueryOutput -Policy Suspended
                '        FAILURE_ACTIONS              : RESUME'
            ) -join [Environment]::NewLine

            {
                Assert-ProductionWebsiteRecoveryPolicy `
                    -Policy Suspended -QueryOutput $queryOutput
            } | Should -Throw '*Suspended recovery policy verification failed*'
        }
```

Proposed:

```powershell
        It 'rejects an empty failure-actions field for suspended recovery' {
            $queryOutput = @(
                New-RecoveryPolicyQueryOutput -Policy Suspended
                '        FAILURE_ACTIONS              :'
            ) -join [Environment]::NewLine

            {
                Assert-ProductionWebsiteRecoveryPolicy `
                    -Policy Suspended -QueryOutput $queryOutput
            } | Should -Throw '*Suspended recovery policy verification failed*'
        }

        It 'rejects an unrecognized failure-actions field for suspended recovery' {
            $queryOutput = @(
                New-RecoveryPolicyQueryOutput -Policy Suspended
                '        FAILURE_ACTIONS              : RESUME'
            ) -join [Environment]::NewLine

            {
                Assert-ProductionWebsiteRecoveryPolicy `
                    -Policy Suspended -QueryOutput $queryOutput
            } | Should -Throw '*Suspended recovery policy verification failed*'
        }
```

Verification:

- Do not run these negative tests alone before Code Edit 1.3; the empty-field case reflects the old accepted representation and is expected to pass only after the production correction.
- Parse the edited test file and require zero PowerShell parser errors before the RED command.

#### Code Edit 1.3

- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 170-209
- Action: replace

Current:

```powershell
    $failureActionFieldMatches = [regex]::Matches(
        $QueryOutput,
        '(?im)^[ \t]*FAILURE_ACTIONS[ \t]*:[ \t]*(?<Value>[^\r\n]*)\r?$')
    $hasSingleFailureActionField = $failureActionFieldMatches.Count -eq 1
    $failureActionFieldValue = if ($hasSingleFailureActionField) {
        $failureActionFieldMatches[0].Groups['Value'].Value.Trim()
    } else {
        $null
    }
    $actionMatches = [regex]::Matches(
        $QueryOutput,
        '(?im)^[ \t]*(?:(?<Label>FAILURE_ACTIONS)[ \t]*:[ \t]*)?(?<Action>RESTART|REBOOT|RUN COMMAND)[ \t]*--[ \t]*Delay[ \t]*=[ \t]*(?<Delay>\d+)[ \t]*milliseconds\.[ \t]*\r?$')
    $actualActions = @(
        $actionMatches | ForEach-Object {
            "$($_.Groups['Action'].Value):$($_.Groups['Delay'].Value)"
        }
    )
    $delayLineCount = [regex]::Matches(
        $QueryOutput,
        '(?im)--[ \t]*Delay[ \t]*=').Count

    $expectedResetPeriodSeconds = if ($Policy -eq 'Suspended') { 0 } else { 3600 }
    $matchesExpectedPolicy = if ($Policy -eq 'Suspended') {
        $hasSingleResetField -and
            $hasSingleFailureActionField -and
            [string]::IsNullOrEmpty($failureActionFieldValue) -and
            $resetPeriodSeconds -eq $expectedResetPeriodSeconds -and
            $delayLineCount -eq 0 -and
            $actualActions.Count -eq 0
    } else {
        $hasSingleResetField -and
            $hasSingleFailureActionField -and
            $resetPeriodSeconds -eq $expectedResetPeriodSeconds -and
            $delayLineCount -eq 2 -and
            $actualActions.Count -eq 2 -and
            $actionMatches[0].Groups['Label'].Success -and
            -not $actionMatches[1].Groups['Label'].Success -and
            $actualActions[0] -eq 'RESTART:10000' -and
            $actualActions[1] -eq 'RESTART:30000'
    }
```

Proposed:

```powershell
    $failureActionFieldMatches = [regex]::Matches(
        $QueryOutput,
        '(?im)^[ \t]*FAILURE_ACTIONS[ \t]*:[ \t]*(?<Value>[^\r\n]*)\r?$')
    $failureActionFieldCount = $failureActionFieldMatches.Count
    $actionMatches = [regex]::Matches(
        $QueryOutput,
        '(?im)^[ \t]*(?:(?<Label>FAILURE_ACTIONS)[ \t]*:[ \t]*)?(?<Action>RESTART|REBOOT|RUN COMMAND)[ \t]*--[ \t]*Delay[ \t]*=[ \t]*(?<Delay>\d+)[ \t]*milliseconds\.[ \t]*\r?$')
    $actualActions = @(
        $actionMatches | ForEach-Object {
            "$($_.Groups['Action'].Value):$($_.Groups['Delay'].Value)"
        }
    )
    $delayLineCount = [regex]::Matches(
        $QueryOutput,
        '(?im)--[ \t]*Delay[ \t]*=').Count

    $expectedResetPeriodSeconds = if ($Policy -eq 'Suspended') { 0 } else { 3600 }
    $matchesExpectedPolicy = if ($Policy -eq 'Suspended') {
        $hasSingleResetField -and
            $failureActionFieldCount -eq 0 -and
            $resetPeriodSeconds -eq $expectedResetPeriodSeconds -and
            $delayLineCount -eq 0 -and
            $actualActions.Count -eq 0
    } else {
        $hasSingleResetField -and
            $failureActionFieldCount -eq 1 -and
            $resetPeriodSeconds -eq $expectedResetPeriodSeconds -and
            $delayLineCount -eq 2 -and
            $actualActions.Count -eq 2 -and
            $actionMatches[0].Groups['Label'].Success -and
            -not $actionMatches[1].Groups['Label'].Success -and
            $actualActions[0] -eq 'RESTART:10000' -and
            $actualActions[1] -eq 'RESTART:30000'
    }
```

Verification:

- Re-run the focused suspended test and require 1 passed, 0 failed.
- Run the two suspended failure-action negative tests and require 2 passed, 0 failed.
- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests/Production.Deploy.Tests.ps1" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Run parser checks for both changed files and require zero errors.
- Run `git diff --check` and require exactly the module and deploy test file in scope.
- Complete an independent task review with no unresolved Critical, Important, or Minor findings.
- Commit and push with message `Accept omitted suspended SCM actions`.

- [ ] Step 1: Switch the clean worktree to `codex/omitted-failure-actions-scm-output` from exact `origin/main`.
- [ ] Step 2: Apply Code Edits 1.1 and 1.2 only.
- [ ] Step 3: Parse the test file and capture the focused RED failure.
- [ ] Step 4: Apply Code Edit 1.3 only.
- [ ] Step 5: Capture focused GREEN, negative-case GREEN, full deploy-test GREEN, parsers, scope, and diff evidence.
- [ ] Step 6: Complete independent task review, then commit and push.

### Task 2 - Validate, review, publish, and merge

Sequence / dependencies:

- Run only after Task 1 is committed and pushed.
- Treat any build, review, or CI failure as a merge blocker.
- Record the squash-merge commit and tree before resuming production acceptance.

Implementation notes:

- Required skill: `write-jane-street-style-code` in Review Mode; review stays read-only unless a finding is accepted.
- Before-Edit Brief:
  - Behavior: no new behavior is introduced in this task; it proves the exact parser correction is isolated and release-ready.
  - Invariants: compare only `origin/main...HEAD`, preserve production, and exclude unrelated checkout state.
  - Boundary/API: the reviewed interface remains `Assert-ProductionWebsiteRecoveryPolicy`; no caller or signature changes.
  - Effects and failures: local build effects remain isolated; PR publication and merge occur only after all gates pass.
  - Tests and evidence: full Windows Pester, isolated clean Gradle build, parsers, diff/scope, whole-branch review, platform CI, and CodeQL.

**Files:**

- Review: `ops/production/windows/modules/Production.Deploy.psm1`
- Review: `ops/production/windows/tests/Production.Deploy.Tests.ps1`

**Interfaces:**

- Consumes: Task 1 commit and its RED/GREEN evidence.
- Produces: immutable squash-merge SHA/tree for the existing guarded production-acceptance plan.

Verification:

- Run `pwsh -NoLogo -NoProfile -Command '$r = Invoke-Pester -Path "ops/production/windows/tests" -PassThru -Output Detailed; $r | Select-Object PassedCount,FailedCount,SkippedCount; if ($r.FailedCount -ne 0) { exit 1 }'`.
- Run an isolated `GRADLE_USER_HOME` clean build with `gradlew.bat clean build --no-daemon` and require `BUILD SUCCESSFUL`.
- Re-run both PowerShell parsers, `git diff --check`, and exact two-file scope.
- Complete a fresh whole-branch review with no unresolved Critical, Important, or Minor findings.
- Open a ready PR that includes the live output, rollback evidence, root cause, and RED/GREEN counts.
- Require Ubuntu, macOS, Windows, and all CodeQL checks to pass before squash merge.
- Record the exact merge SHA and `HEAD^{tree}`.
- Resume Task 3 of `docs/implementation-plans/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md` using those immutable identifiers.

- [ ] Step 1: Run the complete local verification matrix.
- [ ] Step 2: Complete fresh whole-branch Review Mode review.
- [ ] Step 3: Open the ready PR and wait for every required gate.
- [ ] Step 4: Squash-merge and record immutable merge SHA/tree.
- [ ] Step 5: Hand the merge identifiers to the existing guarded production-acceptance task.

## Code Changes

- `ops/production/windows/tests/Production.Deploy.Tests.ps1:43-50`: omit the suspended failure-actions field in the canonical fixture.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1:191-201`: split strict empty-field and unrecognized-field negative regressions.
- `ops/production/windows/modules/Production.Deploy.psm1:170-209`: require zero suspended action labels and exactly one normal action label.

## Files and Modules

- `ops/production/windows/modules/Production.Deploy.psm1`: trusted recovery-query parser boundary.
- `ops/production/windows/tests/Production.Deploy.Tests.ps1`: production-shaped fixtures, parser regressions, and controlled-stop tests.
- `docs/implementation-plans/2026-07-22-christopherbell-dev-suspended-recovery-reset-normalization.md`: existing post-merge deployment and browser-acceptance plan.

## Unit Testing

- Live-shaped suspended reset `0` with no action label passes.
- Suspended output with an empty action label fails.
- Suspended output with an unrecognized action field fails.
- Suspended nonzero, missing, or duplicate reset fields fail.
- Suspended delay fragments or recognized actions fail.
- Normal reset `3600` with exact ordered actions passes; zero/malformed/duplicate/reordered normal state fails.
- Controlled stop still gates on exact suspension and restores normal recovery after every attempt.

## Local Testing

- Focused RED/GREEN against the live-shaped suspended fixture.
- Focused strict negative cases for empty and unrecognized action fields.
- Complete `Production.Deploy.Tests.ps1` Pester run with explicit counts.
- Full `ops/production/windows/tests` Pester run with zero failures and expected administrator-only skips recorded.
- PowerShell parser validation for both edited files.
- `git diff --check` and exact two-file scope.
- Clean isolated Gradle build.
- Independent task and whole-branch reviews.

## Validation

- RED proves the current parser rejects the captured canonical output.
- GREEN proves the exact production shape passes without accepting the former empty-field fixture.
- Normal recovery behavior and all stop/restoration safety tests remain green.
- Local/full builds and all GitHub checks pass.
- The squash-merge SHA/tree are captured before any rollout-script edit.
- Production and browser acceptance continue under the already-approved existing plan.

## Rollback or Recovery

- Before merge, production remains at the rollback-proven safe baseline.
- Before deployment, the existing reviewed rollback script is refreshed to the same immutable merge tree as the installer.
- Any later rollout failure removes the flag, proves or reloads a disabled runtime, removes or disables the worker, and verifies website/dependency/recovery/listener/root health.
- Never delete shared data, roots, current/previous releases, MongoDB data, or cloudflared configuration.

## Risks

- Accepting both omitted and empty labels would weaken the canonical boundary; the empty-field negative regression prevents it.
- Merely counting recognized actions could miss malformed labels; the independent label count remains part of the trusted boundary.
- Normal parsing could drift while simplifying shared variables; explicit normal positive/negative coverage and unchanged action assertions prevent it.
- Production can advance between merge and rollout; the existing in-lock SHA/tree checks prevent unreviewed deployment.

## Completion Criteria

- The live-shaped suspended fixture fails before and passes after the production edit.
- Empty and unrecognized suspended failure-action fields fail closed.
- Focused/full Pester, parsers, diff/scope, clean Gradle build, and independent reviews pass.
- PR passes every CI and CodeQL gate and is squash-merged.
- Immutable merge SHA/tree are recorded and passed to the existing guarded production-acceptance plan.
