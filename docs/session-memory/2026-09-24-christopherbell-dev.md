# 2026-09-24 - christopherbell-dev Session Memory

Work, decisions, events, and evidence for this date.

## 2026-09-24 00:19 Central Daylight Time - Deployer CLI warnings and merge

Continued the user's authorized site bug audit, prioritizing deployer robustness/observability and avoiding any elevation prompt while the user is away.

- Confirmed the current live poller remains on its old bundle: non-elevated `prod.cmd auto-status` reports `STORE_NOT_INITIALIZED`. Public readiness is UP, but the WFL freshness marker remains stale (`2026-08-02T22:44:50.963Z`) and Cane's history remains through 2026-09-07.
- Diagnosed a separate CLI observability defect: `prod.cmd auto-status` repeated the same `Production.Deploy` unapproved-verb warning three times. Added a Pester regression, observed it fail before the fix (21 pass/1 fail), then suppressed only the name-check warning at the three direct/nested module import points. AutoDeploy Pester passes 22/22; Production Operations passes 91/91; `git diff --check`, standard-user CLI smoke, Windows PowerShell 5.1 CLI help, and module import pass.
- Opened and attached PR #1406, merged after required PR CI passed; merge-triggered CodeQL and macOS, Ubuntu, and Windows CI also passed. Merge SHA: `e352dbaef7bd2da4b10e591961230d5182a1d897`.
- Plan and a dated CLI test report were updated. Report: `docs/test-reports/2026-09-24-christopherbell-dev-deployer-cli-warning-suppression.md`.
- Production remains unverified. The new status publisher and tool refresh require the existing SYSTEM task to be bootstrapped once with elevated `prod.cmd auto-install`. No prompt was launched; the user previously asked to avoid prompts while away. Routine refreshes are designed to run through SYSTEM after bootstrap.

## 2026-09-24 01:02 Central Daylight Time - Public profile viewer failure fix merged

Continued the authorized site bug audit. No site display-name change was present in the current checkout; the active ready change was an account public-profile correctness fix. Asked which name change the user meant while continuing the independent bug-fix delivery.

- Narrowed `AccountProfileService.getOptionalSelfAccount()` so anonymous and missing-viewer cases keep anonymous state, while an authenticated account repository failure propagates instead of silently returning `self=false` and `followedByMe=false`.
- Added regression coverage for anonymous state, a missing authenticated viewer, and propagated `DataAccessResourceFailureException`; documented the behavior in the account README. Focused test passed 48/48; full `:website:check` passed; isolated PostgreSQL candidate smoke passed on port 8082. Detailed report: `docs/test-reports/2026-09-24-christopherbell-dev-account-profile-viewer-failure-runtime-verification.md`.
- Published the updated implementation plan, runtime report, and report index in Builder commit `41d6652`.
- Opened and attached PR #1407, all PR checks passed, and it squash-merged at 2026-09-24 01:02 CDT as `0028642e712f1e0e1dedd41e0e75bbbc79960dd7`. Merge-triggered CodeQL and CI Build were still running when this entry was recorded.
- The fix is merged but not deployed. Standard-user `prod.cmd auto-status` reports `STORE_NOT_INITIALIZED`; `prod.cmd auto-install` requires an elevated PowerShell session. The user asked not to open approval prompts while away, so no prompt was opened and production was left untouched. The prepared clean deployment checkout is `A:\Projects\christopherbell.dev-worktrees\christopherbell-production-bootstrap-20260924`; resume only when the user is available to approve the required prompt.
- The site fix worktree retains an unrelated line-ending-only `gradlew.bat` modification; it was not staged or committed.


## 2026-09-24 01:24 - Post-merge CI and deployment readiness

The merged code is through post-merge verification. The first merge-triggered Windows run failed one unrelated `AsyncDispatcherSecurityIntegrationTest.authenticatedStreamingRequestCompletesThroughAsyncRedispatch` case with `ConcurrentModificationException` at its initial MockMvc request. The PR Windows check had passed; rerunning only the failed post-merge job passed, and the complete rerun CI workflow passed on Windows, macOS, and Ubuntu. Post-merge CodeQL passed. A local reproduction attempt stopped before test execution because Gradle could not establish its loopback connection, so the isolated CI failure remains classified as a transient test/environment issue rather than a confirmed product regression.

Production readiness is unchanged: standard-user `prod.cmd auto-status` reports `STORE_NOT_INITIALIZED`; service `ChristopherBellDev` is Running/Automatic and the local readiness endpoint returned HTTP 200. The site display-name change the user referred to was not present in the current checkout; clarification is pending. PR #1407's account-profile fix is merged and fully verified but not deployed. Its deployment requires elevated `prod.cmd auto-install`; no prompt was opened while the user is away.


## 2026-09-24 02:20 - Automatic deploy timestamp fixes merged; production awaits elevation

Continued the authorized deployer robustness and observability work while respecting the user's request not to trigger a prompt while away.

- Fixed PowerShell-version-dependent timestamp handling in automatic deployment. Future-dated status is now unavailable instead of falsely fresh, UTC instants are preserved when reading status, and same-SHA backoff compares true instants across PowerShell 7 and Windows PowerShell 5.1.
- Fixed Windows PowerShell 5.1 test-only staging failures caused by synthetic paths exceeding its path limit; shortening the unique Pester temp roots keeps the copy and partial-cleanup tests portable.
- PR #1408 merged at `8b0bcf0e1eca37645bd8a6df3fc603055c679336`; PR #1409 merged at `62f9b92ca744b0de4a6c36e1e59a68f20f4ffc51`. All required PR checks passed. Post-merge CI Build passed on Windows, macOS, and Ubuntu, and post-merge CodeQL passed.
- The automatic-deploy, operations, and command suites passed 135/135 under both PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Non-elevated `prod.cmd auto-status` and `help` passed; status reports `STORE_NOT_INITIALIZED`.
- The current deployment checkout `A:\Projects\christopherbell.dev-worktrees\christopherbell-production-bootstrap-20260924` is clean at `62f9b92` and its Git tree matches `origin/main`. Read-only production probes show `ChristopherBellDev` Running/Automatic and readiness UP.
- No site display-name changes were present in these changes. Production has not been modified. `prod.cmd auto-install -WhatIf` itself requires elevated PowerShell and returned without opening a prompt. The user is away and previously requested no prompt until they return; wait for them to approve the required elevated bootstrap before installing or deploying.
- Builder implementation plan has Tasks 9-11 updated and published; latest checkpoint commit `5010b78`.


## 2026-09-24 02:57 - Merged deployer failure visibility fix and deployment readiness

Continued the authorized christopherbell.dev audit, prioritizing deployer robustness and preparing to deploy merged site fixes without opening an elevation prompt.

- Fixed an automatic-deploy failure-visibility defect: if trusted tool refresh and saving its FAILED status both fail, the SYSTEM poller previously swallowed the persistence error and proceeded with old state. It now preserves both causes, stops before release checking, publishes CHECK_FAILED best-effort using in-memory FAILED state, returns a failed scheduled-task result, and retries on the next tick. If FAILED status was saved, the trusted bundle still continues to release checking.
- Added two Pester regressions. The stop-on-double-failure test failed before the fix because stale tools were allowed to reach deployment; both focused tests now pass. The auto-deploy, operations, and command suites pass 137/137 under PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Non-elevated CLI smoke and git diff --check pass.
- PR #1410 passed required checks and merged at `706c11554048db3f042926f9407997e9e8595873`. Post-merge CodeQL and CI Build passed; the CI Build included Windows, macOS, and Ubuntu. PR #1410 is attached to the Codex task.
- The clean deployment-preparation checkout `A:\Projects\christopherbell.dev-worktrees\christopherbell-production-bootstrap-20260924` is now detached at `706c1155`, exactly matching `origin/main`. Live read-only checks at 2026-09-24 07:37 UTC found readiness `UP`, public homepage HTTP 200, and ChristopherBellDev, MongoDB, and cloudflared Running/Automatic. Standard-user `prod.cmd auto-status` still reports `STORE_NOT_INITIALIZED`; the one-time `prod.cmd auto-install` must run elevated to initialize the SYSTEM poller. No production mutation or elevation prompt occurred.
- PR #1407's merged account-profile viewer repository-failure fix remains ready but not deployed. Its patch changes profile error propagation and tests; it does not change display names. No display-name change is present in the release checked here. The user asked to deploy the name changes and to be told when elevated approval is needed; clarify target wording while explaining that the account-profile fix is the only matching ready site change.
- Builder plan Task 12 now records implementation, test, merge, and post-merge CI evidence. Deployment and site-audit goal remain in progress pending the elevated bootstrap and production acceptance.

## 2026-09-24 03:30 - Deployer precondition status fix merged; release still awaits bootstrap

Continued the authorized site bug audit and deployer robustness work while avoiding an elevation prompt during the user's absence.

- Fixed the automatic-deploy loop leaving operator status at `CHECKING` when protected configuration could not be read or the configured fixed-root boundary failed. It now best-effort publishes `CHECK_FAILED` with `PROTECTED_PRECONDITION` using only the existing static status store and in-memory state, then preserves and rethrows the original exception. A status-write failure also preserves the original failure.
- The three regression tests failed on the old behavior and passed after the change. The automatic-deploy, operations, and command suites passed 140/140 in PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Non-elevated `prod.cmd help` and `prod.cmd auto-status` passed.
- PR #1411 passed dependency review, CodeQL, and Windows/macOS/Ubuntu checks; it squash-merged as `89d909f3a0dd9319b0f6c6b669a21a7450faed69`. Post-merge CodeQL and CI Build passed on all three platforms. The clean deployment-preparation checkout is detached at that SHA and matches `origin/main`.
- The user asked whether name changes were ready to deploy. Inspection confirms PR #1407 is titled “Propagate public profile viewer lookup failures”; it changes profile lookup/error behavior, not display names. No public display-name change exists in the release set.
- Production has not been modified. The latest non-elevated `prod.cmd auto-status` remains `STORE_NOT_INITIALIZED`. Initializing the SYSTEM poller requires one elevated `prod.cmd auto-install` run from the clean deployment checkout. No elevation prompt was opened or attempted; production deployment and acceptance remain pending until the user is available for that one-time bootstrap.


## 2026-09-24 05:39 Central Daylight Time - Merged deployer task and service hardening

Continued the user's authorized site bug audit with the requested focus on deployer robustness and observability. The user approved broad work but specifically asked to avoid any action requiring an approval prompt while away. No elevation prompt was requested or opened.

- PR #1412 fixed swallowed candidate-output write/truncation and surviving-process cleanup failures. Required checks passed; merged as `b5db92681a5b8bd3b1efd5549eafc1587504c9ec`. Post-merge CI Build and CodeQL passed.
- PR #1413 made automatic poller tool refresh staged and rollback-safe, disabled the scheduled trigger during cutover, and surfaced rollback/cleanup failures. The deploy, auto-deploy, operations, and command suites passed 237/237 under PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Required checks and post-merge CI Build/CodeQL passed; merged as `a4c03e8040c772f64e527ed96b601c45d03eadaf`.
- PR #1414 fixed `auto-remove` swallowing task stop/unregister failures and falsely reporting success. It now takes the shared deployment lock, disables and verifies the task before stopping it, verifies unregister completion, restores prior enabled state on failure, and preserves primary plus rollback errors. Automatic-deploy, operations, and command suites passed 154/154 under both PowerShell versions. All required PR checks and post-merge CI Build/CodeQL passed; merged as `b5de55a1c1225d48f4c278b4b3706ef02a091387`.
- PR #1415 fixed production service uninstall treating service-query errors as absence, hiding stop failures, and trusting WinSW without checking the service was removed. It now distinguishes an actually absent service, validates WinSW exists before stopping, waits for stop, captures WinSW's exit code, and verifies service absence. Nine focused regressions passed. Install, operations, and command suites passed 211 tests with one existing skip under PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Required PR checks and post-merge CI Build/CodeQL passed; merged as `15288bebf60e7e330956ae3b8aaf6f2d22f3770b`.
- Non-elevated `prod.cmd help` and `prod.cmd auto-status` passed; automatic-deploy status still reports `STORE_NOT_INITIALIZED`. A subsequent non-elevated `prod.cmd status` could not read protected `C:\ProgramData\christopherbell.dev\config\deploy.json` and returned Access Denied. This is the existing ACL boundary; no ACL was changed. No live service, release, task, data, or site configuration was changed. The one-time `prod.cmd auto-install` bootstrap and production acceptance still require an elevated session; defer it until the user is available.
- Updated and published the implementation plan through Builder commits `72b1085`, `8ab4be7`, `843e87a`, `7330758`, `9ecd7e1`, `128b335`, `c07de2b`. The plan and CI evidence are in `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`.

The broader site-audit goal remains active. Resume source discovery on current `origin/main`; do not claim production deployment or acceptance from merged source and CI alone.


## 2026-09-24 06:06 Central Daylight Time - Production status diagnostics merged

## 2026-09-24 06:15 Central Daylight Time - Production status diagnostics merged

Continued the authorized site audit's deployer robustness and observability work. The user asked to avoid any action that requires an approval prompt while away; no prompt was opened.

- Fixed `Get-ProductionStatus` hiding unexpected failures from website/MongoDB/cloudflared service queries and the production listener query. Genuine missing services remain `NotInstalled`, no listener remains a null PID, and a successful listener still reports its owning PID. Existing status object fields are unchanged.
- Added regressions for service-query failure, listener-query failure, the native missing-service error, absent service/no listener, and listener PID reporting. Operations, command, and automatic-deploy Pester suites passed 158/158 under PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Non-elevated `prod.cmd help` passed; `prod.cmd auto-status` correctly reported `STORE_NOT_INITIALIZED`; `git diff --check` passed.
- PR #1416 passed dependency review, CodeQL, and Windows/macOS/Ubuntu CI, then merged as `d03a34c2d666c34615c8b20f340a1e0d0c801067`. Post-merge CI Build and CodeQL passed. PR: https://github.com/azurras/christopherbell.dev/pull/1416.
- No public display-name changes were part of this fix and no production mutation occurred. The automatic-deploy store remains uninitialized; `prod.cmd auto-install` bootstrap and production acceptance require an elevated approval. The user is away, so leave production unchanged and continue non-elevated source audit.
- Updated Task 18's implementation plan verification; publish the plan and this memory entry together after refreshing and validating Builder indexes.


## 2026-09-24 06:06 Central Daylight Time - Correct status diagnostics entry timestamp

Correction: The entry immediately above was recorded at 06:06 Central Daylight Time. Its body accidentally repeated a heading and named 06:15, which was a mistyped future time. Treat the content as one 06:06 activity record; this correction preserves the append-only history.


## 2026-09-24 06:33 Central Daylight Time - Release retention fix merged and diagnostics follow-up planned

Continued the authorized site bug audit with a focus on deployer robustness and operator observability. The user asked to avoid any prompt requiring approval while away; no prompt or production mutation occurred.

- PR #1417 fixed release cleanup treating an enumeration failure as an empty release set. The regression failed before implementation; deploy, auto-deploy, operations, and command suites passed 252/252 in both PowerShell 7/Pester 5.9 and Windows PowerShell 5.1/Pester 5.9. Non-elevated CLI help passed and auto-status reported `STORE_NOT_INITIALIZED`.
- PR #1417 passed dependency review, CodeQL, and Windows/macOS/Ubuntu checks; squash-merged as `1478029f872d29a27c7a31a37300264dfc2c8544`. Post-merge CI Build and CodeQL passed. PR: https://github.com/azurras/christopherbell.dev/pull/1417.
- Read-only source review found the operator `logs` and `releases` commands also suppress `Get-ChildItem` failures, misreporting query errors as "no log file" or no releases. The install-root initializer creates both directories. Task 20 is planned to surface those errors while preserving valid empty-directory results.
- Production remains unchanged. The automatic-deploy status store is uninitialized and one-time SYSTEM task bootstrap still requires elevated approval; avoid prompting while the user is away.
