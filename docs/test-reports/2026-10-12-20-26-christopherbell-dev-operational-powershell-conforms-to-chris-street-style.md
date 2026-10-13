# Operational PowerShell conforms to Chris Street Style: Test Report

## Story/Issue
Runtime proof for [the plan](../implementation-plans/2026-10-12-20-13-christopherbell-dev-operational-powershell-conforms-to-chris-street-style.md): the strict-mode production command entry point passes its Pester suite and answers read-only commands exactly as main.

## Branch
`claude/style-ops-20261012` at candidate `73d0fbb`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `73d0fbb`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | The production command Pester suite passes against the strict-mode entry point | ✅ PASS | Expected exit code 0 |
| 2 | prod.cmd help (read-only) answers exactly as main under strict mode | ✅ PASS | Expected exit code 0 |
| 3 | prod.cmd status (read-only) answers exactly as main under strict mode | ✅ PASS | Expected exit code 0 |
| 4 | prod.cmd auto-status (read-only) answers exactly as main under strict mode | ✅ PASS | Expected exit code 0 |
| 5 | prod.cmd releases (read-only) answers exactly as main under strict mode | ✅ PASS | Expected exit code 0 |
| 6 | prod.cmd sensor-status (read-only) answers exactly as main under strict mode | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **The production command Pester suite passes against the strict-mode entry point**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_pester.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops`
2. **prod.cmd help (read-only) answers exactly as main under strict mode**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev help`
3. **prod.cmd status (read-only) answers exactly as main under strict mode**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev status`
4. **prod.cmd auto-status (read-only) answers exactly as main under strict mode**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev auto-status`
5. **prod.cmd releases (read-only) answers exactly as main under strict mode**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev releases`
6. **prod.cmd sensor-status (read-only) answers exactly as main under strict mode**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev sensor-status`

## App / Environment

| Setting | Value |
|---|---|
| Pester | 5.9.0 under PowerShell 7, Production.Command.Tests.ps1 run directly (not wired into Gradle) |
| Read-only commands | help, status, auto-status, releases, sensor-status through each checkout's prod.cmd, unelevated |
| Full check | passed on 73d0fbb4 including the wired Pester suites |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_pester.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops` in `A:\Projects\christopherbell.dev-worktrees\style-ops`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev help` in `A:\Projects\christopherbell.dev-worktrees\style-ops`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev status` in `A:\Projects\christopherbell.dev-worktrees\style-ops`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev auto-status` in `A:\Projects\christopherbell.dev-worktrees\style-ops`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev releases` in `A:\Projects\christopherbell.dev-worktrees\style-ops`
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev sensor-status` in `A:\Projects\christopherbell.dev-worktrees\style-ops`
- **Candidate identity:** `73d0fbb`
- **Cleanup:** No process, file or production state was created; the read-only commands only read production status.

## Data Sent

### 1. The production command Pester suite passes against the strict-mode entry point

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_pester.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops
```

### 2. prod.cmd help (read-only) answers exactly as main under strict mode

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev help
```

### 3. prod.cmd status (read-only) answers exactly as main under strict mode

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev status
```

### 4. prod.cmd auto-status (read-only) answers exactly as main under strict mode

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev auto-status
```

### 5. prod.cmd releases (read-only) answers exactly as main under strict mode

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev releases
```

### 6. prod.cmd sensor-status (read-only) answers exactly as main under strict mode

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad\ops_readonly.ps1 A:\Projects\christopherbell.dev-worktrees\style-ops A:\Projects\christopherbell.dev sensor-status
```

## Response Received

### 1. The production command Pester suite passes against the strict-mode entry point

```text
exit code: 0
--- stdout ---
[95m
[95mStarting discovery in 1 files.[0m
[95mDiscovery found 19 tests in 152ms.[0m
[95mRunning tests.[0m
[33;1mWARNING: The names of some imported commands from the module 'Production.Deploy' include unapproved verbs that might make them less discoverable. To find the commands with unapproved verbs, run the Import-Module command again with the Verbose parameter. For a list of approved verbs, type Get-Verb.[0m
[32m[+] A:\Projects\christopherbell.dev-worktrees\style-ops\ops\production\windows\tests\Production.Command.Tests.ps1[0m[90m 5.8s (5.32s|345ms)[0m
[97mTests completed in 5.81s[0m
[32mTests Passed: 19, [0m[90mFailed: 0, [0m[90mSkipped: 0, [0m[90mInconclusive: 0, [0m[37m[0m[90mNotRun: 0[0m
```

### 2. prod.cmd help (read-only) answers exactly as main under strict mode

```text
exit code: 0
--- stdout ---
candidate exit=0 baseline exit=0 strictModeErrors=0
candidate first line: Usage: prod.cmd <command> [-WhatIf]
baseline  first line: Usage: prod.cmd <command> [-WhatIf]
```

### 3. prod.cmd status (read-only) answers exactly as main under strict mode

```text
exit code: 0
--- stdout ---
candidate exit=1 baseline exit=1 strictModeErrors=0
candidate first line: [31;1mTest-Path: [31;1mAccess to the path 'C:\ProgramData\christopherbell.dev\config\deploy.json' is denied.[0m
baseline  first line: [31;1mTest-Path: [31;1mAccess to the path 'C:\ProgramData\christopherbell.dev\config\deploy.json' is denied.[0m
```

### 4. prod.cmd auto-status (read-only) answers exactly as main under strict mode

```text
exit code: 0
--- stdout ---
candidate exit=0 baseline exit=0 strictModeErrors=0
candidate first line: 
baseline  first line:
```

### 5. prod.cmd releases (read-only) answers exactly as main under strict mode

```text
exit code: 0
--- stdout ---
candidate exit=1 baseline exit=1 strictModeErrors=0
candidate first line: [31;1mTest-Path: [31;1mAccess to the path 'C:\ProgramData\christopherbell.dev\config\deploy.json' is denied.[0m
baseline  first line: [31;1mTest-Path: [31;1mAccess to the path 'C:\ProgramData\christopherbell.dev\config\deploy.json' is denied.[0m
```

### 6. prod.cmd sensor-status (read-only) answers exactly as main under strict mode

```text
exit code: 0
--- stdout ---
candidate exit=1 baseline exit=1 strictModeErrors=0
candidate first line: [31;1mGet-Content: [31;1mAccess to the path 'C:\ProgramData\christopherbell.dev\config\deploy.json' is denied.[0m
baseline  first line: [31;1mGet-Content: [31;1mAccess to the path 'C:\ProgramData\christopherbell.dev\config\deploy.json' is denied.[0m
```

## Evidence
- Case 1 started 2026-10-12T20:10:19-05:00, took 6703 ms, candidate `73d0fbb`
- Case 2 started 2026-10-12T20:10:26-05:00, took 2233 ms, candidate `73d0fbb`
- Case 3 started 2026-10-12T20:10:29-05:00, took 2625 ms, candidate `73d0fbb`
- Case 4 started 2026-10-12T20:10:32-05:00, took 2608 ms, candidate `73d0fbb`
- Case 5 started 2026-10-12T20:10:34-05:00, took 2171 ms, candidate `73d0fbb`
- Case 6 started 2026-10-12T20:10:37-05:00, took 2217 ms, candidate `73d0fbb`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
