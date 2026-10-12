# Local candidate scripts and Windows Gradle wrapper: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-11-19-19-christopherbell-dev-checked-in-local-candidate-scripts-and-windows-gradle-wrappe.md): the checked-in Invoke-Gradle, Start-Candidate and Stop-Candidate scripts run a real isolated candidate and clean up only what they created.

## Branch
`claude/local-candidate-tooling-20261011` at candidate `e30f63f`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `e30f63f`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Invoke-Gradle runs Gradle with JAVA_TOOL_OPTIONS unset in the caller (local candidate Pester) | ✅ PASS | Expected exit code 0 |
| 2 | Start-Candidate starts an isolated test candidate and leaves the caller environment unchanged | ✅ PASS | Expected exit code 0 |
| 3 | The started candidate reports readiness UP | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 4 | The started candidate serves the home page | ✅ PASS | Expected status 200 |
| 5 | Stop-Candidate frees both ports, stops both process trees, copies logs and removes both owned directories | ✅ PASS | Expected exit code 0 |
| 6 | Stop-Candidate keeps directories a tampered state file names but the tooling did not create | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Invoke-Gradle runs Gradle with JAVA_TOOL_OPTIONS unset in the caller (local candidate Pester)**: command `env -u JAVA_TOOL_OPTIONS -u GRADLE_OPTS pwsh -NoLogo -NoProfile -File A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\ops\local\Invoke-Gradle.ps1 :website:automationPester --console=plain -q`
2. **Start-Candidate starts an isolated test candidate and leaves the caller environment unchanged**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_start_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-state.json`
3. **The started candidate reports readiness UP**: http `GET http://127.0.0.1:51690/actuator/health/readiness`
4. **The started candidate serves the home page**: http `GET http://127.0.0.1:51690/`
5. **Stop-Candidate frees both ports, stops both process trees, copies logs and removes both owned directories**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-logs`
6. **Stop-Candidate keeps directories a tampered state file names but the tooling did not create**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_guard_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`

## App / Environment

| Setting | Value |
|---|---|
| SPRING_PROFILES_ACTIVE | test (candidate process only) |
| SPRING_MONGODB_URI | mongodb://127.0.0.1:<OS-selected port>/test (disposable mongod) |
| JAVA_TOOL_OPTIONS | unset in the calling shell |
| Full check | .\ops\local\Invoke-Gradle.ps1 :website:check :cbell-lib:check :website:bootJar passed (BUILD SUCCESSFUL, 76 automation Pester tests) on d88278d8; e30f63f2 changes only Start-Candidate.ps1's java launch |

## Local Run Details
- **Local command:** `env -u JAVA_TOOL_OPTIONS -u GRADLE_OPTS pwsh -NoLogo -NoProfile -File A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\ops\local\Invoke-Gradle.ps1 :website:automationPester --console=plain -q` in `A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_start_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-state.json` in `A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`
- **Local command:** `GET http://127.0.0.1:51690/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`
- **Local command:** `GET http://127.0.0.1:51690/` in `A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-logs` in `A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_guard_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling` in `A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling`
- **Candidate identity:** `e30f63f`
- **Cleanup:** Stop-Candidate.ps1 stopped both process trees, both ports had no listeners, and both generated directories were removed; the tampered-state decoys were removed by the check itself; production MongoDB on 27017 kept listening.

## Data Sent

### 1. Invoke-Gradle runs Gradle with JAVA_TOOL_OPTIONS unset in the caller (local candidate Pester)

```text
env -u JAVA_TOOL_OPTIONS -u GRADLE_OPTS pwsh -NoLogo -NoProfile -File A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\ops\local\Invoke-Gradle.ps1 :website:automationPester --console=plain -q
```

### 2. Start-Candidate starts an isolated test candidate and leaves the caller environment unchanged

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_start_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-state.json
```

### 3. The started candidate reports readiness UP

```http
GET http://127.0.0.1:51690/actuator/health/readiness
```

### 4. The started candidate serves the home page

```http
GET http://127.0.0.1:51690/
```

### 5. Stop-Candidate frees both ports, stops both process trees, copies logs and removes both owned directories

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_stop_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-state.json C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1-logs
```

### 6. Stop-Candidate keeps directories a tampered state file names but the tooling did not create

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\s1_guard_check.ps1 A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling
```

## Response Received

### 1. Invoke-Gradle runs Gradle with JAVA_TOOL_OPTIONS unset in the caller (local candidate Pester)

<details><summary>213 lines</summary>

```text
exit code: 0
--- stdout ---
[95mPester v5.9.0[0m
[95m
[95mStarting discovery in 5 files.[0m
[33;1mWARNING: The names of some imported commands from the module 'Production.Deploy' include unapproved verbs that might make them less discoverable. To find the commands with unapproved verbs, run the Import-Module command again with the Verbose parameter. For a list of approved verbs, type Get-Verb.[0m
[95mDiscovery found 189 tests in 912ms.[0m
[95mRunning tests.[0m
[95m
[95mRunning tests from 'A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\.github\scripts\tests\Test-ProductionSite.Tests.ps1'[0m
[92mDescribing Production Watch verdict[0m
[32m  [+] is healthy when every route answers, the deployment succeeded and main is live[0m[90m 327ms (305ms|21ms)[0m
[32m  [+] fails the readiness route after three refused attempts and names the cause[0m[90m 97ms (95ms|2ms)[0m
[32m  [+] recovers when a route fails once and then answers[0m[90m 34ms (34ms|1ms)[0m
[32m  [+] fails when the latest Production deployment failed[0m[90m 27ms (26ms|1ms)[0m
[32m  [+] passes when no Production deployment has been recorded[0m[90m 21ms (21ms|1ms)[0m
[32m  [+] fails when main passed CI more than the threshold ago and is still not live[0m[90m 49ms (48ms|1ms)[0m
[32m  [+] measures lag in UTC when the API client already converted the timestamp to a DateTime[0m[90m 30ms (30ms|1ms)[0m
[32m  [+] tolerates a newer main within the deploy window or before CI passes[0m[90m 54ms (54ms|0ms)[0m
[32m  [+] reads the live commit from actuator JSON delivered as bytes[0m[90m 28ms (27ms|0ms)[0m
[32m  [+] fails when main has had no CI run for longer than the threshold[0m[90m 28ms (27ms|1ms)[0m
[32m  [+] fails when the CI run for main has been unfinished for longer than the threshold[0m[90m 26ms (26ms|0ms)[0m
[32m  [+] accepts a manual CI run and ignores pull request runs for main[0m[90m 35ms (34ms|0ms)[0m
[32m  [+] reports a red main as refused rather than stalled[0m[90m 23ms (23ms|0ms)[0m
[32m  [+] warns about the deployment token within 14 days[0m[90m 34ms (33ms|2ms)[0m
[32m  [+] warns about the deployment token after it expired[0m[90m 28ms (28ms|1ms)[0m
[32m  [+] warns about the deployment token not when it is far off[0m[90m 27ms (26ms|1ms)[0m
[32m  [+] passes the token check when no expiry was recorded[0m[90m 24ms (23ms|0ms)[0m
[32m  [+] treats a main that differs from live only by operations requests as live[0m[90m 23ms (22ms|0ms)[0m
[32m  [+] still reports lag when main also changed deployable code[0m[90m 47ms (47ms|0ms)[0m
[32m  [+] fails build info that does not identify a release commit[0m[90m 41ms (41ms|0ms)[0m
[0m
[92mDescribing Production alert issue[0m
[32m  [+] opens one labeled issue when production becomes unhealthy[0m[90m 23ms (21ms|2ms)[0m
[32m  [+] comments on the open issue while production stays unhealthy[0m[90m 9ms (9ms|1ms)[0m
[32m  [+] comments and closes the open issue on recovery[0m[90m 9ms (9ms|1ms)[0m
[32m  [+] does nothing when healthy with no open issue[0m[90m 11ms (11ms|1ms)[0m
[0m
[92mDescribing Production Watch report[0m
[32m  [+] renders each check and escapes table separators in details[0m[90m 7ms (6ms|1ms)[0m
[95m
[95mRunning tests from 'A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\.github\scripts\tests\Write-TestSummary.Tests.ps1'[0m
[92mDescribing Write-TestSummary[0m
[32m  [+] totals JUnit and Pester NUnit results by result directory and lists failures[0m[90m 108ms (106ms|2ms)[0m
[32m  [+] reports that no results exist when the build stopped before tests ran[0m[90m 22ms (21ms|1ms)[0m
[32m  [+] lists an unreadable result file and still summarizes the readable ones[0m[90m 37ms (36ms|1ms)[0m
[32m  [+] writes the summary to output when no summary path is supplied[0m[90m 29ms (29ms|1ms)[0m
[95m
[95mRunning tests from 'A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\ops\local\tests\CandidateRuntime.Tests.ps1'[0m
[92mDescribing local candidate guards[0m
[32m  [+] accepts only a generated directory directly under its parent[0m[90m 16ms (15ms|1ms)[0m
[32m  [+] adds the socket directory to JAVA_TOOL_OPTIONS unless one is already set[0m[90m 4ms (4ms|1ms)[0m
[32m  [+] restores the caller environment after running the action, even when it fails[0m[90m 30ms (29ms|1ms)[0m
[32m  [+] resolves the newest MongoDB Server install when mongod is not on PATH[0m[90m 78ms (77ms|1ms)[0m
[32m  [+] never returns a reserved port[0m[90m 25ms (24ms|1ms)[0m
[95m
[95mRunning tests from 'A:\Projects\christopherbell.dev-worktrees\local-candidate-tooling\ops\production\windows\tests\Production.AutoDeploy.Tests.ps1'[0m
[92mDescribing automatic origin main deployment[0m
[33;1mWARNING: Automatic deployment status could not be published (WRITE_FAILED); operator-visible status may be stale.[0m
[32m  [+] warns once with sanitized details when status publication fails[0m[90m 89ms (88ms|1ms)[0m
[33;1mWARNING: Automatic deployment status could not be published (ACCESS_DENIED); operator-visible status may be stale.[0m
[32m  [+] classifies access-denied status writes without exposing exception details[0m[90m 54ms (53ms|0ms)[0m
[32m  [+] does not warn when automatic-deploy status publication succeeds[0m[90m 49ms (48ms|1ms)[0m
[32m  [+] resets status-warning suppression at the start of each automatic-deploy invocation[0m[90m 79ms (78ms|0ms)[0m
[32m  [+] rejects an alternate root before auto state, marker, remote, or deploy effects[0m[90m 71ms (70ms|0ms)[0m
[33;1mWARNING: Automatic deployment status could not be published (ACCESS_DENIED); operator-visible status may be stale.[0m
[32m  [+] does not write an auto-deploy error log when the configured root is unsafe[0m[90m 134ms (133ms|1ms)[0m
[32m  [+] publishes a terminal status when protected configuration cannot be read[0m[90m 71ms (70ms|1ms)[0m
[32m  [+] publishes a terminal status when the fixed root boundary is rejected[0m[90m 66ms (66ms|1ms)[0m
[33;1mWARNING: Automatic deployment status could not be published (WRITE_FAILED); operator-visible status may be stale.[0m
[32m  [+] preserves the configuration failure when terminal status publication fails[0m[90m 59ms (59ms|0ms)[0m
[32m  [+] refuses automatic deploy before remote access while legacy reconciliation is required[0m[90m 63ms (63ms|1ms)[0m
[32m  [+] reports a protected marker read failure as a failed check, not a migration block[0m[90m 59ms (58ms|0ms)[0m
[32m  [+] refuses automatic deploy before remote access when schema direction is absent[0m[90m 55ms (55ms|1ms)[0m
[32m  [+] does not deploy when the remote SHA is already active[0m[90m 115ms (114ms|0ms)[0m
[32m  [+] does not report the active release up to date when the website service is stopped[0m[90m 100ms (99ms|1ms)[0m
[32m  [+] recovers an unhealthy active release before applying the failed-revision deployment backoff[0m[90m 127ms (127ms|1ms)[0m
[32m  [+] deploys a newer main release even when active-service recovery fails[0m[90m 130ms (130ms|1ms)[0m
[32m  [+] deploys a newer main release while active-service recovery is rate limited[0m[90m 124ms (124ms|1ms)[0m
[32m  [+] reports a remote-check failure after recovery failure without losing protected retry state[0m[90m 85ms (85ms|1ms)[0m
[32m  [+] recovers the active service even when remote main cannot be queried[0m[90m 72ms (71ms|1ms)[0m
[32m  [+] backs off a repeated failed service recovery without restarting every poll[0m[90m 67ms (67ms|1ms)[0m
[32m  [+] records a failed service recovery and publishes a sanitized startup failure[0m[90m 89ms (88ms|1ms)[0m
[32m  [+] publishes the recovery failure even when protected retry-state persistence fails[0m[90m 86ms (85ms|0ms)[0m
[32m  [+] deploys exactly once when remote main changes[0m[90m 94ms (93ms|1ms)[0m
[32m  [+] publishes another deploying update when the heartbeat callback runs[0m[90m 117ms (117ms|1ms)[0m
[32m  [+] backs off the same failed SHA[0m[90m 89ms (88ms|1ms)[0m
[32m  [+] retries the same failed SHA after the backoff expires[0m[90m 107ms (106ms|0ms)[0m
[32m  [+] surfaces an automatic deployment failure after persisting its failed SHA[0m[90m 99ms (99ms|1ms)[0m
[32m  [+] reads operator status without loading protected deployment configuration[0m[90m 101ms (100ms|1ms)[0m
[32m  [+] reports access denied when the status-store directory query fails[0m[90m 120ms (120ms|1ms)[0m
[32m  [+] reports invalid status when the status-file query fails[0m[90m 89ms (89ms|1ms)[0m
[32m  [+] distinguishes a missing status store from a missing status record[0m[90m 69ms (69ms|1ms)[0m
[32m  [+] reports a missing poller independently of a fresh backing-off status record[0m[90m 76ms (75ms|1ms)[0m
[32m  [+] distinguishes a denied scheduler query from a confirmed missing task[0m[90m 52ms (52ms|1ms)[0m
[32m  [+] keeps the status record visible when the scheduler query is access denied[0m[90m 67ms (66ms|0ms)[0m
[32m  [+] reads version-one status records without the optional failure detail field[0m[90m 76ms (76ms|0ms)[0m
[32m  [+] reports safe registered scheduler states without exposing the task action[0m[90m 68ms (67ms|1ms)[0m
[32m  [+] reports safe registered scheduler states without exposing the task action[0m[90m 65ms (64ms|1ms)[0m
[32m  [+] reports safe registered scheduler states without exposing the task action[0m[90m 64ms (63ms|1ms)[0m
[32m  [+] keeps valid status available and sanitizes scheduler query failures[0m[90m 69ms (68ms|1ms)[0m
[32m  [+] overrides a fresh up-to-date status when the live website service is stopped[0m[90m 71ms (70ms|0ms)[0m
[32m  [+] reports readiness failure when the website service is running but not ready[0m[90m 73ms (73ms|0ms)[0m
[32m  [+] reports unknown live health when the website service query is denied[0m[90m 68ms (67ms|0ms)[0m
[32m  [+] keeps the production CLI free of unapproved-verb discovery warnings[0m[90m 136ms (136ms|0ms)[0m
[32m  [+] creates a standard-user-readable status store with no untrusted write rights[0m[90m 103ms (101ms|2ms)[0m
[32m  [+] publishes only sanitized status and marks old status stale without protected configuration[0m[90m 138ms (138ms|1ms)[0m
[32m  [+] identifies only approved smoke routes in safe failure details[0m[90m 67ms (66ms|1ms)[0m
[32m  [+] reports a future-dated status as unavailable instead of fresh[0m[90m 73ms (72ms|1ms)[0m
[32m  [+] reports malformed status as unavailable without returning record contents[0m[90m 77ms (77ms|0ms)[0m
[32m  [+] rejects a versioned tool bundle whose file hash changed after staging[0m[90m 95ms (95ms|0ms)[0m
[32m  [+] stages trusted versioned tools before switching the poller action[0m[90m 454ms (453ms|0ms)[0m
[32m  [+] cleans a partial tools stage and preserves the task action when copying fails[0m[90m 185ms (185ms|1ms)[0m
[33;1mWARNING: Automatic deployment status could not be published (ACCESS_DENIED); operator-visible status may be stale.[0m
[33;1mWARNING: Automatic deployment diagnostics could not be published; operator diagnostics may be stale.[0m
[32m  [+] checks once and exits without keeping a console process alive[0m[90m 121ms (121ms|1ms)[0m
[32m  [+] surfaces tool refresh failure when its protected state cannot be persisted[0m[90m 109ms (109ms|1ms)[0m
[33;1mWARNING: Automatic deployment diagnostics could not be published; operator diagnostics may be stale.[0m
[32m  [+] continues with the trusted bundle when a refresh failure is persisted[0m[90m 78ms (77ms|1ms)[0m
[32m  [+] registers the startup task with an absolute PowerShell 7 executable when PATH is empty[0m[90m 287ms (287ms|0ms)[0m
[32m  [+] does not overwrite tools or stop the task while a deployment is active[0m[90m 73ms (72ms|1ms)[0m
[32m  [+] waits for transient lock contention before refreshing the automatic-deploy task[0m[90m 85ms (84ms|1ms)[0m
[32m  [+] re-enables the existing task and does not start it when it refuses to stop[0m[90m 133ms (133ms|1ms)[0m
[32m  [+] keeps the previous poller bundle when staging copy fails[0m[90m 98ms (97ms|0ms)[0m
[32m  [+] restores the old bundle and scheduled task when registration fails after switching[0m[90m 245ms (245ms|0ms)[0m
[32m  [+] stops a partially registered first-install task before restoring the old bundle[0m[90m 253ms (252ms|0ms)[0m
[32m  [+] surfaces both registration and task cleanup failures during first-install recovery[0m[90m 225ms (225ms|1ms)[0m
[32m  [+] replaces and protects the installed tools tree before SYSTEM task registration[0m[90m 200ms (199ms|1ms)[0m
[0m
[92mDescribing automatic deployment task removal[0m
[32m  [+] keeps WhatIf read-only after the administrator check[0m[90m 14ms (12ms|2ms)[0m
[32m  [+] treats an absent task as an idempotent no-op[0m[90m 35ms (35ms|0ms)[0m
[32m  [+] disables, stops, unregisters, and verifies a running task in order[0m[90m 45ms (44ms|1ms)[0m
[32m  [+] removes a disabled task without changing its state or issuing a stop[0m[90m 33ms (33ms|0ms)[0m
[32m  [+] surfaces a stop failure and restores the prior enabled state[0m[90m 49ms (49ms|0ms)[0m
[32m  [+] does not unregister when the scheduler fails to disable the task[0m[90m 37ms (36ms|0ms)[0m
[32m  [+] surfaces an unregister failure and restores the prior enabled state[0m[90m 38ms (37ms|0ms)[0m
[32m  [+] rejects a scheduler no-op and reports when enabled-state recovery also fails[0m[90m 43ms (43ms|0ms)[0m
[32m  [+] verifies the task was re-enabled after a scheduler no-op[0m[90m 40ms (40ms|0ms)[0m
[32m  [+] does not inspect or change the task when deployment-lock acquisition fails[0m[90m 32ms (32ms|1ms)[0m
[0m
[92mDescribing automatic deployment state reads[0m
[32m  [+] keeps malformed automatic-deploy state JSON diagnostics sanitized[0m[90m 9ms (8ms|1ms)[0m
[32m  [+] preserves automatic-deploy state file read failures[0m[90m 25ms (25ms|0ms)[0m
[0m
[92mDescribing automatic deployment CI gate and GitHub reporting[0m
[32m  [+] waits without deploying while CI for the new commit is pending[0m[90m 68ms (67ms|1ms)[0m
[32m  [+] refuses a commit whose CI failed and reuses that verdict until the failure backoff ends[0m[90m 145ms (145ms|0ms)[0m
[32m  [+] reports a CI lookup failure as a failed CI check without deploying[0m[90m 53ms (53ms|0ms)[0m
[32m  [+] still surfaces a failed service recovery while CI holds the new commit[0m[90m 59ms (59ms|0ms)[0m
[32m  [+] records a successful deployment in the Production environment when a token is installed[0m[90m 109ms (109ms|0ms)[0m
[32m  [+] records a failed deployment with a sanitized description and still surfaces the failure[0m[90m 87ms (87ms|0ms)[0m
[32m  [+] deploys normally and warns once without the token when GitHub reporting fails[0m[90m 87ms (86ms|1ms)[0m
[32m  [+] makes no GitHub writes when no token is installed[0m[90m 68ms (67ms|0ms)[0m
[32m  [+] refuses to install first tools for a commit that has not passed CI[0m[90m 71ms (70ms|0ms)[0m
[0m
[92mDescribing automatic deployment CI conclusion[0m
[32m  [+] maps the newest push or manual CI run on a commit to PENDING (no run)[0m[90m 22ms (20ms|2ms)[0m
[32m  [+] maps the newest push or manual CI run on a commit to PENDING (running)[0m[90m 14ms (12ms|2ms)[0m
[32m  [+] maps the newest push or manual CI run on a commit to SUCCESS (passed)[0m[90m 12ms (12ms|1ms)[0m
[32m  [+] maps the newest push or manual CI run on a commit to FAILED (cancelled)[0m[90m 9ms (8ms|1ms)[0m
[32m  [+] maps the newest push or manual CI run on a commit to SUCCESS (green re-run)[0m[90m 9ms (8ms|1ms)[0m
[32m  [+] maps the newest push or manual CI run on a commit to SUCCESS (manual run recovers a missed push)[0m[90m 10ms (9ms|1ms)[0m
[32m  [+] maps the newest push or manual CI run on a commit to PENDING (pull request runs never count)[0m[90m 13ms (12ms|1ms)[0m
[32m  [+] falls back to anonymous reads once when the installed token is rejected[0m[90m 43ms (43ms|1ms)[0m
[32m  [+] does not hide a non-authentication failure behind an anonymous retry[0m[90m 17ms (16ms|0ms)[0m
[32m  [+] parses the GitHub repository from the configured HTTPS remote https://github.com/azurras/christopherbell.dev.git[0m[90m 11ms (10ms|1ms)[0m
[32m  [+] parses the GitHub repository from the configured HTTPS remote https://github.com/azurras/christopherbell.dev[0m[90m 14ms (14ms|1ms)[0m
[32m  [+] rejects a remote that is not an HTTPS GitHub repository[0m[90m 9ms (8ms|0ms)[0m
[0m
[92mDescribing GitHub deployment token[0m
[32m  [+] reads no token when reporting is not configured[0m[90m 8ms (7ms|1ms)[0m
[32m  [+] reads a token only from a protected file[0m[90m 19ms (19ms|0ms)[0m
[32m  [+] rejects a token file that does not hold a GitHub token[0m[90m 13ms (13ms|0ms)[0m
[32m  [+] verifies then stores the token in a file protected before the secret is written[0m[90m 49ms (49ms|0ms)[0m
[32m  [+] stores nothing when the token is malformed or GitHub rejects it[0m[90m 36ms (36ms|1ms)[0m
[32m  [+] rejects an empty or blank token file with a clear message before calling GitHub (empty)[0m[90m 28ms (28ms|1ms)[0m
[32m  [+] rejects an empty or blank token file with a clear message before calling GitHub (blank)[0m[90m 26ms (26ms|1ms)[0m
[32m  [+] requires elevated PowerShell before reading the protected configuration[0m[90m 14ms (13ms|1ms)[0m
[0m
[92mDescribing automatic deployment CI status outcomes[0m
[32m  [+] publishes and reads back AWAITING_CI with category NONE[0m[90m 39ms (38ms|1ms)[0m
[32m  [+] publishes and reads back CI_FAILED with category CI_RESULT[0m[90m 31ms (31ms|1ms)[0m
[32m  [+] publishes and reads back CHECK_FAILED with category CI_CHECK[0m[90m 32ms (29ms|3ms)[0m
[0m
[92mDescribing operator diagnostics[0m
[32m  [+] redacts a fine-grained token[0m[90m 7ms (5ms|1ms)[0m
[32m  [+] redacts a classic token[0m[90m 2ms (2ms|1ms)[0m
[32m  [+] redacts a Resend key[0m[90m 2ms (2ms|1ms)[0m
[32m  [+] redacts a Bearer [REDACTED][0m[90m 5ms (5ms|1ms)[0m
[32m  [+] redacts a JWT[0m[90m 2ms (2ms|1ms)[0m
[32m  [+] redacts Mongo credentials[0m[90m 2ms (2ms|0ms)[0m
[32m  [+] redacts a password assignment[0m[90m 2ms (2ms|0ms)[0m
[32m  [+] redacts an email address[0m[90m 2ms (2ms|0ms)[0m
[32m  [+] flattens and bounds a redacted message[0m[90m 4ms (3ms|0ms)[0m
[32m  [+] keeps only allowlisted, redacted fields from the newest structured log lines[0m[90m 16ms (16ms|0ms)[0m
[32m  [+] keeps an older error visible after newer INFO lines push it out of the latest entries[0m[90m 52ms (52ms|0ms)[0m
[32m  [+] returns only the newest problems within the scanned lines[0m[90m 12ms (11ms|1ms)[0m
[32m  [+] keeps the first redacted stack frames of an error[0m[90m 11ms (10ms|0ms)[0m
[32m  [+] publishes a bounded record that standard users read back[0m[90m 243ms (242ms|0ms)[0m
[32m  [+] sheds routine entries before problems when the record is too large[0m[90m 175ms (174ms|0ms)[0m
[32m  [+] reports the poller's published scheduler state when a standard user is denied[0m[90m 16ms (16ms|0ms)[0m
[32m  [+] keeps UNKNOWN when the published scheduler state is stale[0m[90m 15ms (14ms|0ms)[0m
[0m
[92mDescribing operations request validation[0m
[32m  [+] accepts a well-formed request[0m[90m 16ms (15ms|1ms)[0m
[32m  [+] rejects malformed JSON[0m[90m 7ms (7ms|1ms)[0m
[32m  [+] rejects an id that differs from the file name[0m[90m 4ms (2ms|1ms)[0m
[32m  [+] rejects an unknown action[0m[90m 3ms (2ms|1ms)[0m
[32m  [+] rejects an unknown property[0m[90m 2ms (2ms|1ms)[0m
[32m  [+] rejects a missing reason[0m[90m 4ms (3ms|1ms)[0m
[32m  [+] rejects a timestamp without a zone[
... [2980 more characters not recorded]
```

</details>

### 2. Start-Candidate starts an isolated test candidate and leaves the caller environment unchanged

```text
exit code: 0
--- stdout ---
ready=True databaseName=test baseUrl=http://127.0.0.1:51690 mongoPort=51689
caller environment before: SPRING_PROFILES_ACTIVE=caller-sentinel; SPRING_MONGODB_URI=; APP_JWT_SECRET=; JAVA_TOOL_OPTIONS=; APP_FEDERATION_DISCOVERYENABLED=; APP_FEDERATION_KEYENCRYPTIONSECRET=
caller environment after:  SPRING_PROFILES_ACTIVE=caller-sentinel; SPRING_MONGODB_URI=; APP_JWT_SECRET=; JAVA_TOOL_OPTIONS=; APP_FEDERATION_DISCOVERYENABLED=; APP_FEDERATION_KEYENCRYPTIONSECRET=
caller environment unchanged: True
```

### 3. The started candidate reports readiness UP

```text
HTTP 200 
X-Request-Id: cd940466-5e86-4b81-94ab-3414e577a1de
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791765700
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/vnd.spring-boot.actuator.v3+json
Transfer-Encoding: chunked
Date: Mon, 12 Oct 2026 00:40:40 GMT
Connection: close

{"status":"UP"}
```

### 4. The started candidate serves the home page

<details><summary>100 lines</summary>

```text
HTTP 200 
X-Request-Id: 52f52a9f-870f-4b9d-a677-4a09d7e5f65f
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791765700
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/html;charset=UTF-8
Content-Language: en-US
Transfer-Encoding: chunked
Date: Mon, 12 Oct 2026 00:40:40 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell" />
    <meta name="keywords" content="cbell,blog" />
    
    <meta name="description" content="A working corner of the internet for Void posts, lunch picks, and practical utilities." />
    
    <link rel="canonical" href="https://www.christopherbell.dev/" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="christopherbell.dev" />
    <meta property="og:description" content="A working corner of the internet for Void posts, lunch picks, and practical utilities." />
    <meta property="og:url" content="https://www.christopherbell.dev/" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="christopherbell.dev" />
    <meta name="twitter:description" content="A working corner of the internet for Void posts, lunch picks, and practical utilities." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  

    <title>CB | Home</title>

    <link rel="stylesheet" type="text/css" href="/ba07ef3ecb9fe0381733/css/main.css"/>
</head>

<body class="site-page void-shell-page home-page">
    <div id="nav"></div>
    <main role="main" class="site-main home-void-gateway">
        <section class="home-void-shell" aria-labelledby="homeTitle">
            <div class="container home-void-hero">
                <div class="home-void-copy">
                    <p class="home-kicker">christopherbell.dev</p>
                    <h1 id="homeTitle">Drop into the Void.</h1>
                    <p class="home-intro">
                        The Void is the front door here: short posts, replies, signals, and the latest noise from the feed.
                    </p>
                    <a class="btn btn-primary home-void-primary" href="/void">
                        Enter Void
                        <i class="fa fa-arrow-right" aria-hidden="true"></i>
                    </a>
                </div>

                <aside class="home-void-signal-panel" aria-label="Void signals">
                    <div class="home-void-panel-header">
                        <span class="thread-status-pill is-live">Live</span>
                        <span>Signal Rail</span>
                    </div>
                    <div id="homeActivePost" class="home-void-active" aria-live="polite">
                        <div class="home-void-empty">
                            <span class="home-void-eyebrow">Finding signal</span>
                            <strong>Loading the most active post.</strong>
                            <span>The rail updates every few seconds.</span>
                        </div>
                    </div>
                </aside>
            </div>
        </section>
    </main>
    <footer id="footer"></footer>
</body>

<script type="module" src="/ba07ef3ecb9fe0381733/js/app.js"></script>
<script type="module" src="/ba07ef3ecb9fe0381733/js/home.js"></script>

</html>
```

</details>

### 5. Stop-Candidate frees both ports, stops both process trees, copies logs and removes both owned directories

```text
exit code: 0
--- stdout ---
port 51690 listeners: 0
port 51689 listeners: 0
removed C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-9cd893e5840f4c19994a537e18f5fbd0
removed C:\Temp\cbell-jdk-4285e3c5dedf4d5a9c5a253886386076
ports still listening: 0; processes still running: 0; directories left: 0
candidate log copied: True; ERROR lines: 0
production MongoDB 27017 still listening: True
```

### 6. Stop-Candidate keeps directories a tampered state file names but the tooling did not create

```text
exit code: 0
--- stdout ---
port 1 listeners: 0
port 2 listeners: 0
kept C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-not-owned: not a directory this tooling created
kept C:\Users\Christopher\AppData\Local\Temp\cbell-jdk-c90ca390d88e4ce8b1fedecf4d977e8b: not a directory this tooling created
decoy directories kept: True
```

## Evidence
- Case 1 started 2026-10-11T19:40:15-05:00, took 15952 ms, candidate `e30f63f`
- Case 2 started 2026-10-11T19:40:31-05:00, took 8468 ms, candidate `e30f63f`
- Case 3 started 2026-10-11T19:40:40-05:00, took 31 ms, candidate `e30f63f`
- Case 4 started 2026-10-11T19:40:40-05:00, took 172 ms, candidate `e30f63f`
- Case 5 started 2026-10-11T19:40:41-05:00, took 4875 ms, candidate `e30f63f`
- Case 6 started 2026-10-11T19:40:46-05:00, took 3358 ms, candidate `e30f63f`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
