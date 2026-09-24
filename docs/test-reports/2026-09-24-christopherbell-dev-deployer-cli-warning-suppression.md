## Document Status

blocked

## Story/Issue

Suppress duplicate PowerShell unapproved-verb discovery warnings emitted by the production deployment CLI, while leaving unrelated warnings observable.

## Branch

`codex/auto-deploy-observability-20260923`, PR #1406, implementation commit `86f6b4ecd911193097ab88760b96ab995ed7649a`, squash-merged as `e352dbaef7bd2da4b10e591961230d5182a1d897`.

## App / Environment

Native Windows PowerShell deployment CLI. PowerShell 7.5/Pester 5.9.0 for focused suites; Windows PowerShell 5.1 for compatibility checks. No application server/port or database was started. Production service, listener, scheduled task, and protected state were not modified.

## Local Run Details

Ran from `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20260923`. The Pester regression invokes `ops/production/windows/prod.ps1 help` in-process and captures warnings. `prod.cmd auto-status` was run as a non-elevated CLI smoke check. Windows PowerShell 5.1 ran the help command and imported `Production.AutoDeploy.psm1` successfully.

## Test Cases

1. Verify the `help` CLI command does not emit the repeated `Production.Deploy` unapproved-verb discovery warning.
2. Verify non-elevated `auto-status` prints a concise unavailable-store result without the import warnings.
3. Run AutoDeploy and Production Operations Pester suites.
4. Verify Windows PowerShell 5.1 CLI/module compatibility and required PR CI.

## Data Sent

No HTTP request, credentials, request body, database write, production configuration access, or production mutation. Pester used isolated fixtures. `help` and `auto-status` were local CLI invocations.

## Response Received

Before the fix, AutoDeploy Pester reported 21 passed and 1 failed at the new warning assertion, capturing the repeated warning. After the fix, it reported 22 passed and 0 failed. Production Operations Pester reported 91 passed and 0 failed. The standard-user CLI returned `available=False`, `freshness=UNAVAILABLE`, `reason=STORE_NOT_INITIALIZED`, and a safe fixed message, with no PowerShell import warnings. Windows PowerShell 5.1 CLI help and module import passed.

## Pass / Fail

- Warning regression: failed before the fix as expected; passed after it.
- AutoDeploy Pester: pass, 22/22.
- Production Operations Pester: pass, 91/91.
- Standard-user CLI smoke: pass; concise result without import warnings or a prompt.
- Windows PowerShell 5.1 CLI and module import: pass.
- `git diff --check`: pass.
- PR #1406 dependency review, CodeQL, language analyses, and macOS, Ubuntu, and Windows builds/tests: pass.
- Merge-triggered CodeQL and macOS, Ubuntu, and Windows builds/tests: pass.

## Evidence

- Red run: `Invoke-Pester -Path 'ops/production/windows/tests/Production.AutoDeploy.Tests.ps1' -Output Normal` â€” 21 passed, 1 failed at the warning assertion.
- Green run: same command â€” 22/22 passed.
- `Invoke-Pester -Path 'ops/production/windows/tests/Production.Operations.Tests.ps1' -Output Normal` â€” 91/91 passed.
- `.\prod.cmd auto-status` â€” returned `STORE_NOT_INITIALIZED` without import warnings.
- Windows PowerShell 5.1 `prod.ps1 help` and `Production.AutoDeploy.psm1` import â€” passed.
- `gh pr checks 1406` â€” all checks passed; merge SHA `e352dbaef7bd2da4b10e591961230d5182a1d897`.
- Merge-triggered CI Build and CodeQL for that SHA â€” passed on all required platforms.

## Bugs / Follow-ups

The repeated warnings are fixed by passing `-DisableNameChecking` only at the three direct/nested `Production.Deploy` import sites. General warnings remain enabled. Production status publication and deployment are not live-verified: the installed SYSTEM task still reports no initialized status store. One elevated `prod.cmd auto-install` bootstrap remains necessary before verifying live tool switching, release SHA, and stale-data recovery; the user asked not to trigger approval prompts while away.
