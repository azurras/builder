## Document Status

blocked

## Story/Issue

Implementation plan: `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`, Tasks 6 and 7 (standard-user deployer status and autonomous trusted tool refresh).

## Branch

`codex/auto-deploy-observability-20260923`; implementation commit `281dccdf913e08134ae6dcee1653dfc33ed8fc51` was squash-merged through [PR #1405](https://github.com/azurras/christopherbell.dev/pull/1405) as `9d4929af94a7be916365552fad84d67bb56c4590`.

## App / Environment

Windows native deployment control plane, PowerShell 7. Standard-user session for CLI verification. No application port or database was started or accessed. Production service, listener, and SYSTEM task were not modified.

## Local Run Details

- `.\prod.cmd auto-status` ran from `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`. The wrapper used PowerShell 7 and exited normally.
- Focused AutoDeploy Pester suite ran with Pester 5.9.0. Production Operations Pester suite ran with the same runtime.
- Windows PowerShell 5.1 imported `Production.AutoDeploy.psm1`; only Pester 3.4 is installed there, so the repository's Pester 5 assertions could not run under that host.
- `.\gradlew.bat --no-daemon :website:check` was attempted with the default Gradle home and again with a private worktree-local `GRADLE_USER_HOME`. Both failed before Gradle task configuration. No application candidate process was started.

## Test Cases

1. Read the automatic deployment status from a standard-user command without loading protected deployment configuration.
2. Validate status ACLs, sanitized fields, stale/malformed data, deployment failure handling, trusted tool-tree identity and file hashes, partial-stage cleanup, old task-action preservation, and deployment-lock release ordering through Pester.
3. Check the deployment module syntax/import in Windows PowerShell 5.1.
4. Run the native website check as a broader repository build gate.

## Data Sent

- CLI input: `prod.cmd auto-status` (no request body, credentials, database connection, or HTTP request).
- Pester inputs were isolated test fixtures under Pester's temporary test directory and mocked scheduled-task/Git boundaries where the contract under test required them.
- Gradle input: `:website:check`; no application data was submitted.

## Response Received

The standard-user CLI returned:

```text
available : False
freshness : UNAVAILABLE
status    : UNKNOWN
reason    : STORE_NOT_INITIALIZED
updatedAt :
message   : The automatic deployment status store has not been initialized.
```

Pester reported `Tests Passed: 21, Failed: 0` for `Production.AutoDeploy.Tests.ps1` and `Tests Passed: 91, Failed: 0` for `Production.Operations.Tests.ps1`. Windows PowerShell 5.1 printed `module-import=passed`.

Both Gradle attempts failed with `java.io.IOException: Unable to establish loopback connection`; the nested cause was `java.net.SocketException: Invalid argument: connect` from JDK `PipeImpl` while connecting to the Gradle daemon. This occurred before project tasks ran.

## Pass / Fail

- Standard-user `auto-status`: pass. It returned a safe not-initialized reason instead of Access Denied or a protected-config read.
- AutoDeploy Pester: pass, 21/21.
- Operations Pester: pass, 91/91.
- Windows PowerShell 5.1 module import: pass.
- Windows PowerShell 5.1 Pester run: unavailable because installed Pester 3.4 does not support the Pester 5 `Should` operators used by the repository tests.
- Native `:website:check`: blocked by the JDK/Gradle loopback failure before task execution.
- PR #1405 CI: dependency review, CodeQL, Java/Kotlin analysis, JavaScript/TypeScript analysis, and Ubuntu, macOS, and Windows build/test all passed. The first Windows attempt failed during Pester Gallery module discovery before build execution; the rerun installed Pester and passed the Windows build/test job.
- Live SYSTEM status publication/tool switch: not run because the installed task still has its old bundle and requires one approved elevated `auto-install` bootstrap.

## Evidence

- `pwsh -NoProfile -Command "Invoke-Pester -Path 'ops/production/windows/tests/Production.AutoDeploy.Tests.ps1' -Output Normal"` â€” 21/21 passed.
- `pwsh -NoProfile -Command "Invoke-Pester -Path 'ops/production/windows/tests/Production.Operations.Tests.ps1' -Output Normal"` â€” 91/91 passed.
- `powershell.exe -NoProfile -Command 'Import-Module "./ops/production/windows/modules/Production.AutoDeploy.psm1" -Force; "module-import=passed"'` â€” passed.
- `git diff --check` â€” passed.
- `prod.cmd auto-status` â€” output recorded above.
- `gradlew.bat --no-daemon :website:check` and the private-Gradle-home retry â€” failed before task execution as described above.
- `gh pr checks 1405` â€” all required checks passed; PR squash-merge confirmed as `9d4929af94a7be916365552fad84d67bb56c4590`.

## Post-merge and current live readback

At approximately 2026-09-23 23:40 CDT, a standard-user `prod.cmd auto-status` still returned `available=False`, `freshness=UNAVAILABLE`, `reason=STORE_NOT_INITIALIZED`; it did not prompt or read protected deployment configuration. Public readiness and homepage returned HTTP 200, with readiness `UP`. The public WFL freshness endpoint returned HTTP 200 but still reported `lastRefreshedOn=2026-08-02T22:44:50.963Z`, `current=false`. The Cane's history endpoint returned HTTP 200 with nine snapshots; the latest was `2026-09-07`, collected at `2026-09-07T11:00:16.849Z`, with 50/50 successful metro prices. These reads confirm the merged code has not been activated in production and the data freshness defects remain visible.

The merge-triggered CodeQL workflow and CI Build workflow for `9d4929af94a7be916365552fad84d67bb56c4590` completed successfully. CI Build passed on Ubuntu, macOS, and Windows; the Windows build/test job completed in 8m14s.

The prerequisite deployer PRs are also merged: #1403 as `bcb883b89813ad20fb977e1ff89572464381717a` and #1404 as `9a9e39b28517436ca9beb361bd9c959a48baa067`. Their dependency review, CodeQL, language analyses, and Ubuntu, macOS, and Windows CI checks passed. Current standard-user/public evidence does not establish a fresh deployment attempt from those bundles because protected task state and logs remain unavailable.

## Bugs / Follow-ups

The existing SYSTEM task has not been bootstrapped with the merged implementation. One elevated `auto-install` is needed to activate standard-user status publication and versioned self-refresh. After that, tool refreshes should not require routine elevation. Verify status readability across the tool switch, current release SHA, service/listener/readiness, and public WFL/Cane's freshness after the user completes the one-time approval. Production acceptance is not claimed here.
