# Accept Versioned Auto-Deploy Tools in the Startup Task Contract: Test Report

## Story/Issue
The first agent `verify-startup` request ([#1485](https://github.com/azurras/christopherbell.dev/pull/1485)) failed in production: "ChristopherBellAutoDeploy must run the installed production auto-deploy command hidden and noninteractive." Logged in the [agent operations plan](../implementation-plans/2026-10-05-12-55-christopherbell-dev-let-agents-operate-production-without-administrator-rights.md).

## Branch
`claude/task-contract-versioned-tools-20261005` at `fb8e0bb`

## Pass / Fail

> [!TIP]
> **4 of 4 passed** on candidate `fb8e0bb`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Production failure reproduced and fixed | ✅ PASS | With tool refresh's exact task arguments, the `main` contract rejects the task and the candidate accepts it |
| 2 | Contract still rejects other scripts | ✅ PASS | Another root, a non-commit version folder, a nested path and a different script are all rejected |
| 3 | Second request validated | ✅ PASS | CI's validator accepts both request files |
| 4 | Native gate | ✅ PASS | Full build: 3,268 tests, 0 failed, 112 opt-in skips; Operations Pester 107/107 under PowerShell 7, contract cases 5/5 under Windows PowerShell 5.1 |

## Test Cases
1. **Production failure reproduced and fixed:** `Assert-AutoDeployTaskContract` from `origin/main` (`71848dd`) and from the candidate, run against a task whose action uses the argument string `Update-AutoDeployToolsFromOriginMain` writes.
2. **Contract still rejects other scripts:** new Pester cases in `Production.Operations.Tests.ps1`.
3. **Second request validated:** `Production.OpsRequests.Tests.ps1` (run in the full build).
4. **Native gate:** `gradlew.bat build`.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev production tooling (`Production.Operations.psm1`) |
| Runtime | PowerShell 7 and Windows PowerShell 5.1 on Windows 11, non-elevated |
| Inputs | Task action built with the same expressions as tool refresh, for root `C:\ProgramData\christopherbell.dev` |

## Local Run Details
- **Local command:** `pwsh -NoProfile -Command "Import-Module ...Production.Operations.psm1; Assert-AutoDeployTaskContract -Task <task> -Config <config>"`, once from each tree.
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\task-contract-20261005` (candidate) and `A:\Projects\christopherbell.dev-worktrees\prod-tools` (`origin/main`).
- **Candidate identity:** `fb8e0bb`, clean tree.
- **Logs:** command output below.
- **Cleanup:** nothing started or written.

## Data Sent

### 1. Production failure reproduced and fixed

Command arguments, as written by tool refresh:

```text
-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\ProgramData\christopherbell.dev\tools\versions\0123456789abcdef0123456789abcdef01234567\prod.ps1" auto-deploy
```

### 2. Contract still rejects other scripts

Command arguments `-File` targets:

```text
C:\Temp\christopherbell.dev\tools\prod.ps1
C:\ProgramData\christopherbell.dev\tools\versions\latest\prod.ps1
C:\ProgramData\christopherbell.dev\tools\versions\<sha>\x\prod.ps1
C:\ProgramData\christopherbell.dev\tools\other.ps1
```

### 3. Second request validated

Input file `ops/requests/2026-10-05-second-agent-verify-startup.json` (`action: verify-startup`).

### 4. Native gate

```text
gradlew.bat build
```

## Response Received

### 1. Production failure reproduced and fixed

```text
before (origin/main 71848dd): contract: REJECTED - ChristopherBellAutoDeploy must run the installed production auto-deploy command hidden and noninteractive.
after (candidate fb8e0bb): contract: ACCEPTED
```

### 2. Contract still rejects other scripts

```text
Operations (pwsh7): Passed=107 Failed=0
PS5.1 contract cases: Passed=5 Failed=0
exit status: 0
```

### 3. Second request validated

```text
committed operations requests: both files accepted (full build automation-pwsh7 suite)
```

### 4. Native gate

```text
exit status: 0
BUILD SUCCESSFUL in 5m 7s; 3,268 tests, 3,156 passed, 0 failed, 112 skipped
```

## Evidence
- The production request result in `prod.cmd diagnostics`: `{"id":"2026-10-05-first-agent-verify-startup","outcome":"FAILED","detail":"ChristopherBellAutoDeploy must run the installed production auto-deploy command hidden and noninteractive."}`.
- Tool versioning was introduced in `9d4929a` (#1405, 2026-09-23).

## Bugs / Follow-ups
- After merge and deploy, the second request should report `SUCCEEDED` in `prod.cmd diagnostics`.

## Document Status
complete

## Project
christopherbell-dev
