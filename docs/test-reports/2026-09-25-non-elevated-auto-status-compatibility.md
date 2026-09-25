## Document Status

complete

## Story/Issue

Task 42 in `docs/implementation-plans/2026-09-23-christopherbell-dev-site-bug-audit-and-fixes.md`: keep public auto-deploy status readable without elevation when an older schema-version-1 record omits the optional `failureDetail` field.

## Branch

`codex/auto-status-legacy-schema-20260925`, based on merged `main` `427530f6f195dbffaa81c8557feaad3e899bdf6a`. PR #1443 passed CI Build, CodeQL, and Dependency Review and squash-merged to `main` as `7639e3f1b552013a72cb59f0e32807fc6356daf3`.

## App / Environment

Production status implementation from the current mainline was run on the native Windows production host as the current non-elevated user. The status record is at the standard-user-readable `C:\ProgramData\christopherbell.dev-status\auto-deploy.json`. Live application base URL: `https://www.christopherbell.dev/`. PowerShell 7, Pester 5.9.0.

## Local Run Details

No application candidate was started and no production files, task configuration, release pointer, service settings, or database were changed. Ran `prod.cmd auto-status` from the clean current-main worktree to read the existing public status record, query current service health, and report the scheduler permission result. The checked-in production CLI in the protected root remains older and still fails before status rendering when it reads protected `config\deploy.json`; this report verifies the current-main CLI implementation before any protected tool refresh.

## Test Cases

- Schema-version-1 status record without the optional `failureDetail` field remains readable.
- Scheduler `ACCESS_DENIED` is reported separately without hiding deployment status.
- Existing deployment failure status, service health, and status freshness are preserved.
- Current-main status command and live site continuity on the running host.

## Data Sent

No database reads or writes. Read the public deployment status JSON; queried the website service and task scheduler read-only; sent `GET https://www.christopherbell.dev/` with no request body.

## Response Received

- Before the fix, the same legacy status record returned `available=False`, `reason=INVALID`; the record has `schemaVersion=1` and does not contain `failureDetail`.
- The new Pester regression failed before the code fix and passed afterward.
- After the fix, current-main `prod.cmd auto-status` returned `available=True`, `freshness=STALE`, `status=DEPLOYMENT_FAILED`, `deploymentStatus=DEPLOYMENT_FAILED`, `serviceState=RUNNING`, `siteHealth=HEALTHY`, and `failureCategory=DEPLOYMENT`. It returned no failure detail, did not expose protected diagnostics, and separately reported `pollerState=UNKNOWN`, `pollerReason=ACCESS_DENIED`.
- At `2026-09-25T12:51:58-05:00`, the public homepage returned HTTP 200, title `CB | Home`, with a 4,348-byte response body; `ChristopherBellDev` was Running/Automatic.

## Pass / Fail

- Legacy status compatibility regression: passed after failing before implementation.
- Full Windows production PowerShell suite: 815 passed, 0 failed, 28 skipped.
- PR #1443 hosted CI Build, CodeQL, and Dependency Review: all passed; merged to `main` as `7639e3f1b552013a72cb59f0e32807fc6356daf3`.
- Current-main non-elevated status command: passed and exposed the stored deployment outcome, healthy service/site, stale timestamp, and scheduler access denial as separate fields.
- Public website continuity: passed.
- Protected installed-tool refresh and application release activation: not performed; this non-elevated session cannot inspect or refresh the protected task/tools.

## Evidence

- Pester: `pwsh -NoLogo -NoProfile -Command "Invoke-Pester -CI -Path 'ops/production/windows/tests' -Output Minimal"` from the clean branch.
- Live status command: `prod.cmd auto-status` from the current-main worktree.
- Continuity check: `Invoke-WebRequest -Uri 'https://www.christopherbell.dev/' -TimeoutSec 20` and `Get-Service ChristopherBellDev`.
- `git diff --check` and PowerShell parser checks passed.

## Bugs / Follow-ups

With strict mode enabled, status validation unconditionally accessed `$record.failureDetail` after its first optional-property check. Older schema-version-1 records correctly omit that field, but the access threw and converted a readable deployment failure to `reason=INVALID`. The validator now checks and validates that field only when present, preserving compatibility with existing records. Poller inspection still requires protected scheduler access, so the CLI reports it as unknown with `ACCESS_DENIED` while keeping deployment state visible. Protected tool refresh and production release-level verification remain pending.
