## Document Status

blocked

## Story/Issue

Implementation plan: `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`, Tasks 6 and 7 (standard-user deployer status and autonomous trusted tool refresh).

## Branch

`codex/auto-deploy-observability-20260923`, based on merged `origin/main` commit `9a9e39b28517436ca9beb361bd9c959a48baa067`. The implementation is local and not yet committed during this report.

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
- Live SYSTEM status publication/tool switch: not run because the installed task still has its old bundle and requires one approved elevated `auto-install` bootstrap.

## Evidence

- `pwsh -NoProfile -Command "Invoke-Pester -Path 'ops/production/windows/tests/Production.AutoDeploy.Tests.ps1' -Output Normal"` â€” 21/21 passed.
- `pwsh -NoProfile -Command "Invoke-Pester -Path 'ops/production/windows/tests/Production.Operations.Tests.ps1' -Output Normal"` â€” 91/91 passed.
- `powershell.exe -NoProfile -Command 'Import-Module "./ops/production/windows/modules/Production.AutoDeploy.psm1" -Force; "module-import=passed"'` â€” passed.
- `git diff --check` â€” passed.
- `prod.cmd auto-status` â€” output recorded above.
- `gradlew.bat --no-daemon :website:check` and the private-Gradle-home retry â€” failed before task execution as described above.

## Bugs / Follow-ups

The existing SYSTEM task has not been bootstrapped with the new implementation. An elevated `auto-install` after merge is needed once to activate standard-user status publication and versioned self-refresh. After that, tool refreshes should not require routine elevation. Verify status readability across the tool switch, current release SHA, service/listener/readiness, and public WFL/Cane's freshness after the user approves the bootstrap. Production acceptance is not claimed here.
