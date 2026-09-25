## Document Status

complete

## Story/Issue

Task 42 in `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`: restore a reliable protected production build after the Windows Gradle daemon could not establish its loopback connection.

## Branch

PR #1442 branch `codex/gradle-unix-socket-temp-path-20260925`, head `178a09009f6a3877a17b09e278629544efd4d3da`; merged to `main` as `427530f6f195dbffaa81c8557feaad3e899bdf6a`.

## App / Environment

Application under runtime verification: the running production site at base URL `https://www.christopherbell.dev/`. Native Windows host, JDK 25.0.3, Gradle wrapper 9.6.1, Node from `node.exe`, PowerShell 7, Pester 5.9.0. The Gradle invocation ran as the current non-elevated user with a private `GRADLE_USER_HOME` under `%TEMP%`. The child environment included `CHRISTOPHERBELL_PRODUCTION_DEPLOYMENT=1` and `JAVA_TOOL_OPTIONS` with `-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp`, preserving any inherited Java options.

## Local Run Details

No application candidate was started. Ran the production deployer's `Invoke-CheckedProcess` against `gradlew.bat --no-daemon :website:build` in the clean PR worktree. The check completed successfully in 5m16s. Gradle daemon output was captured under `%TEMP%\christopherbell-gradle-child-env-check-home\daemon\9.6.1\daemon-6664.out.log`. The production service and active release were not modified.

## Test Cases

- Production release builder passes a short JDK Unix-domain socket temp path to Gradle and preserves an existing `JAVA_TOOL_OPTIONS` value.
- Full Windows production Pester suite.
- Previously timing-out media concurrency tests with ten-second bounded waits.
- Full website build through the deployer's checked-process runner.
- Public site continuity and Windows service state after merge.
- Non-elevated production status/task visibility.

## Data Sent

No database reads or writes. Gradle build used the checked-out source and normal build dependencies. Site continuity check sent `GET https://www.christopherbell.dev/` without a request body.

## Response Received

- Full Gradle build: `BUILD SUCCESSFUL in 5m 16s`.
- Full Pester suite: 814 passed, 0 failed, 28 skipped.
- Both focused `MediaPlaybackServiceTest` concurrency tests passed after their bounded waits changed from two to ten seconds.
- At `2026-09-25T12:41:17-05:00`, the HTTP response from the running production site for `GET https://www.christopherbell.dev/` had status code 200, title `CB | Home`, and a 4,348-byte response body.
- `ChristopherBellDev` was `Running`, startup type `Automatic`.
- `prod.cmd auto-status` failed reading protected `C:\ProgramData\christopherbell.dev\config\deploy.json` with `Access is denied`; the exact `ChristopherBellAutoDeploy` scheduler query also returned `Access is denied`.

## Pass / Fail

- Deployer child environment regression: passed; short socket path and inherited option preservation asserted.
- Production PowerShell suite: passed, 814 passed, 0 failed, 28 skipped.
- Focused media concurrency regressions: passed.
- Full website build using the deployer's child-process runner: passed.
- PR checks: Windows, macOS, Ubuntu, CodeQL, and dependency review passed; PR #1442 merged.
- Public site continuity: passed.
- Protected production tool/status refresh and application release activation: not performed; the non-elevated session cannot read the protected configuration or query the task. The existing production service remained healthy.

## Evidence

- Pester: `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -CI -Path 'ops/production/windows/tests' -Output Minimal"` from the clean PR worktree.
- Java concurrency test command filtered `:website:test` to `concurrentAdmissionsPublishExactlyOneWorkerDescriptor` and `cancellationAndAdmissionDoNotOverlapLifecycleDecisions`.
- Build runner: `Invoke-CheckedProcess` with `gradlew.bat @('--no-daemon',':website:build')` and the same environment assembled by `New-ReleaseFromOriginMain`.
- PowerShell parser check and `git diff --check` passed.
- PR #1442: https://github.com/azurras/christopherbell.dev/pull/1442; merged commit `427530f6f195dbffaa81c8557feaad3e899bdf6a`.
- Site continuity request and service readback were repeated after merge at the timestamp above.

## Bugs / Follow-ups

The JDK daemon startup failure was caused by the default Unix-domain socket temporary path being too long for the Windows JDK socket setup. Supplying the short system temp path through `JAVA_TOOL_OPTIONS` allows the actual deployer checked-process invocation to build successfully. The cold build also exposed two media concurrency tests with overly tight two-second deadlines; ten-second bounds preserve the latch-based ordering assertions and pass in the full build.

Production remains on its previous application release. The protected deployment task and status cannot be inspected or refreshed from this non-elevated session; a later authorized production-tool activation is still required for release-level verification. The homepage and Windows service remain healthy.
