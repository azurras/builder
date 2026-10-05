# Let Agents Operate Production Without Administrator Rights: Test Report

## Story/Issue
User request to let an agent do the DevOps work end to end without an admin user, then "Let's fix all of these problems." [Implementation plan](../implementation-plans/2026-10-05-12-55-christopherbell-dev-let-agents-operate-production-without-administrator-rights.md).

## Branch
`claude/agent-operations-20261005` at `406eeaa`

## Pass / Fail

> [!TIP]
> **5 of 5 passed** on candidate `406eeaa`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Request-only change detection with real git | ✅ PASS | A request-only commit is detected; a code commit is not |
| 2 | Request reading and validation with real git | ✅ PASS | The `.json` request is listed and validated READY; the non-JSON file and the request-free commit yield nothing |
| 3 | Diagnostics publish and read | ✅ PASS | Real service and scheduler queries; email, Resend key and Mongo password masked; request IDs kept; record FRESH |
| 4 | Non-elevated `prod.cmd diagnostics` | ✅ PASS | Runs without elevation and explains that nothing is published yet, which is true until production runs this code |
| 5 | Native gate | ✅ PASS | Full build: 3,256 tests, 0 failed, 112 opt-in skips |

## Test Cases
1. **Request-only change detection with real git:** `Test-AutoDeployOpsOnlyChange` on a scratch repository with three commits: code, request-only, code.
2. **Request reading and validation with real git:** `Get-AutoDeployOpsRequestFiles` on the request commit and on the code commit, then `Test-AutoDeployOpsRequestDocument` with the current clock.
3. **Diagnostics publish and read:** `Publish-AutoDeployDiagnostics` and `Get-AutoDeployDiagnostics` with a scratch program-data root and an ECS log fixture containing secrets. Only the ACL assertions are shadowed, because a non-admin shell cannot create the protected status folder.
4. **Non-elevated `prod.cmd diagnostics`:** the real entry point against the production status store.
5. **Native gate:** `gradlew.bat build`.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev production tooling (`prod.cmd`, `Production.AutoDeploy.psm1`) at the candidate |
| Runtime | PowerShell 7, Windows 11, non-elevated (`IsInRole(Administrator)` False); Git for Windows |
| Fixtures | Scratch git repository and scratch program-data root under the session scratchpad; production status store read-only |
| Website | Unchanged in this candidate apart from the Pester input list in `website/build.gradle.kts`; no website candidate run applies |

## Local Run Details
- **Local command:** `.\prod.cmd diagnostics`, plus direct module calls (`Test-AutoDeployOpsOnlyChange`, `Get-AutoDeployOpsRequestFiles`, `Test-AutoDeployOpsRequestDocument`, `Publish-AutoDeployDiagnostics`, `Get-AutoDeployDiagnostics`)
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\agent-operations-20261005`
- **Candidate identity:** `406eeaa`, clean tree. The runtime cases ran on byte-identical content minutes before the commit message was reworded; `git commit --amend` changed only the message.
- **Logs:** command output below.
- **Cleanup:** scratch repository and program-data root left in the session scratchpad only; nothing was started or written in production.

## Data Sent

### 1. Request-only change detection with real git

Command arguments: three commit SHAs from the scratch repository.

```text
C1: App.java   C2: + ops/requests/verify-now.json, ops/requests/notes.txt   C3: App.java changed
Test-AutoDeployOpsOnlyChange C1->C2 and C2->C3
```

### 2. Request reading and validation with real git

Input file `ops/requests/verify-now.json` at C2:

```json
{"id":"verify-now","action":"verify-startup","reason":"Runtime check of request reading.","requestedAt":"<now - 2 minutes>"}
```

### 3. Diagnostics publish and read

Input file `logs\application.json.log`:

```text
application.json.log lines:
{"log":{"level":"WARN",...},"message":"delivery to person@example.com failed with token=re_SecretKeyValue123456","requestId":"verify-cicd-0001","error":{"message":"mongodb://admin:hunter2@127.0.0.1:27017/x\nstack line"}}
{"log":{"level":"INFO",...},"message":"GET \"/blog\", parameters={}","requestId":"b4eab325-0c1f-41bd-aa90-b8cacd1d632b"}
```

### 4. Non-elevated `prod.cmd diagnostics`

Command arguments: `diagnostics`.

```text
.\prod.cmd diagnostics   (elevated=False)
```

### 5. Native gate

```text
gradlew.bat build
```

## Response Received

### 1. Request-only change detection with real git

```text
request-only C1->C2: True
code change C2->C3: False
```

### 2. Request reading and validation with real git

```text
request files at C2: verify-now
verdict: READY action=verify-startup (Valid request.)
request files at C1: 0
```

### 3. Diagnostics publish and read

Input file `logs\application.json.log`:

```text
bytes=1330 secrets present: (none)
freshness=FRESH scheduler.reason=ACCESS_DENIED services=ChristopherBellDev:Running,MongoDB:Running,cloudflared:Running
log: [WARN] [verify-cicd-0001] delivery to [REDACTED_EMAIL] failed with token=[REDACTED] | mongodb://[REDACTED]@127.0.0.1:27017/x
log: [INFO] [b4eab325-0c1f-41bd-aa90-b8cacd1d632b] GET "/blog", parameters={} |
```

### 4. Non-elevated `prod.cmd diagnostics`

Command arguments: `diagnostics`.

```text
exit status: 1
Exception: No diagnostics have been published yet; the automatic deployment poller publishes them every minute.
```

### 5. Native gate

```text
exit status: 0
BUILD SUCCESSFUL in 5m 13s; 3,256 tests, 3,144 passed, 0 failed, 112 skipped
```

## Evidence
- Pester: AutoDeploy 148/148; watch, request validator and command suites 49/49.
- A live read-only Production Watch token-expiry check returns "No token expiry has been recorded", as expected before this deploys.
- Runtime cases ran at about 13:55 CDT.

## Bugs / Follow-ups
- A real `verify-startup` request through production, and `prod.cmd diagnostics` returning a published record, are verified after merge and deploy (AC-9).
- Rollback is covered by Pester only; running it in production would cause a real outage response.

## Document Status
complete

## Project
christopherbell-dev
