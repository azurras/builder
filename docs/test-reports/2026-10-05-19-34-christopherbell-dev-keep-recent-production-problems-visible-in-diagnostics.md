# Keep recent production problems visible in diagnostics: Test Report

## Story/Issue
[Plan](../implementation-plans/2026-10-05-19-28-christopherbell-dev-keep-recent-production-problems-visible-in-diagnostics.md): diagnostics keep recent WARN/ERROR entries and top stack frames visible to standard users.

## Branch
`claude/diagnostics-recent-problems-20261005` at candidate `3571135`

## Pass / Fail

> [!TIP]
> 2 of 2 cases passed on candidate `3571135`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Diagnostics keep an in-window error with redacted stack frames | ✅ PASS | Expected exit code 0 |
| 2 | Operator diagnostics Pester suite | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Diagnostics keep an in-window error with redacted stack frames**: command `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\d271de53-3327-4d15-bf16-74cc3208e818\scratchpad\verify-diagnostics.ps1 -Checkout A:\Projects\christopherbell.dev-worktrees\diagnostics-recent-problems-20261005`
2. **Operator diagnostics Pester suite**: command `pwsh -NoLogo -NoProfile -Command "Import-Module Pester -RequiredVersion 5.9.0; $c = New-PesterConfiguration; $c.Run.Path = 'ops/production/windows/tests/Production.AutoDeploy.Tests.ps1'; $c.Filter.FullName = '*operator diagnostics*'; $c.Output.Verbosity = 'Detailed'; $c.Run.Exit = $true; Invoke-Pester -Configuration $c 3>$null"`

## App / Environment

| Setting | Value |
|---|---|
| Runtime | PowerShell 7 with the candidate production modules |
| Fixture | 20,001-line ECS log in a temporary root: 1 ERROR outside the 10,000-line window, 1 ERROR with a stack trace and a planted password inside it, 38 WARN, 19,959 INFO and 1 non-JSON line |
| Isolation | Temporary folder; only the SYSTEM-only ACL guards and the SYSTEM task query are replaced in module scope, as in Pester; no production files touched |

## Local Run Details
- **Local command:** `pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\d271de53-3327-4d15-bf16-74cc3208e818\scratchpad\verify-diagnostics.ps1 -Checkout A:\Projects\christopherbell.dev-worktrees\diagnostics-recent-problems-20261005` in `A:\Projects\christopherbell.dev-worktrees\diagnostics-recent-problems-20261005`
- **Local command:** `pwsh -NoLogo -NoProfile -Command "Import-Module Pester -RequiredVersion 5.9.0; $c = New-PesterConfiguration; $c.Run.Path = 'ops/production/windows/tests/Production.AutoDeploy.Tests.ps1'; $c.Filter.FullName = '*operator diagnostics*'; $c.Output.Verbosity = 'Detailed'; $c.Run.Exit = $true; Invoke-Pester -Configuration $c 3>$null"` in `A:\Projects\christopherbell.dev-worktrees\diagnostics-recent-problems-20261005`
- **Candidate identity:** `3571135`
- **Cleanup:** The harness deletes its temporary root; no processes remain.

## Data Sent

### 1. Diagnostics keep an in-window error with redacted stack frames

```text
pwsh -NoLogo -NoProfile -File C:\Users\CHRIST~1\AppData\Local\Temp\claude\A--Projects-builder\d271de53-3327-4d15-bf16-74cc3208e818\scratchpad\verify-diagnostics.ps1 -Checkout A:\Projects\christopherbell.dev-worktrees\diagnostics-recent-problems-20261005
```

### 2. Operator diagnostics Pester suite

```text
pwsh -NoLogo -NoProfile -Command "Import-Module Pester -RequiredVersion 5.9.0; $c = New-PesterConfiguration; $c.Run.Path = 'ops/production/windows/tests/Production.AutoDeploy.Tests.ps1'; $c.Filter.FullName = '*operator diagnostics*'; $c.Output.Verbosity = 'Detailed'; $c.Run.Exit = $true; Invoke-Pester -Configuration $c 3>$null"
```

## Response Received

### 1. Diagnostics keep an in-window error with redacted stack frames

<details><summary>45 lines</summary>

```text
exit code: 0
--- stdout ---
{
  "publishMilliseconds": 310,
  "recordBytes": 37128,
  "schemaVersion": 1,
  "freshness": "FRESH",
  "recentLogEntries": 100,
  "recentLogEntriesLevels": "INFO=100",
  "recentProblems": 20,
  "recentProblemsLevels": "ERROR=1,WARN=19",
  "errorProblems": [
    {
      "timestamp": "2026-10-05T11:00:00Z",
      "level": "ERROR",
      "logger": "dev.christopherbell.feed.FeedService",
      "requestId": "r-in-window-error",
      "message": "feed query failed",
      "errorType": "com.mongodb.MongoTimeoutException",
      "errorMessage": "timed out",
      "errorStack": "at com.mongodb.Cluster.select(Cluster.java:10) | at dev.christopherbell.feed.FeedService.load(FeedService.java:42) password=[REDACTED] | at dev.christopherbell.feed.FeedController.get(FeedController.java:7)"
    }
  ],
  "earlyErrorOutsideWindowPresent": false,
  "oldestProblem": {
    "timestamp": "2026-10-05T12:00:00Z",
    "level": "WARN",
    "logger": "dev.christopherbell.libs.api.ControllerExceptionHandler",
    "requestId": "r-warn-10000",
    "message": "INVALID_TOKEN status=401 Bearer [REDACTED]",
    "errorType": null,
    "errorMessage": null,
    "errorStack": null
  },
  "newestProblem": {
    "timestamp": "2026-10-05T12:00:00Z",
    "level": "WARN",
    "logger": "dev.christopherbell.libs.api.ControllerExceptionHandler",
    "requestId": "r-warn-19500",
    "message": "INVALID_TOKEN status=401 Bearer [REDACTED]",
    "errorType": null,
    "errorMessage": null,
    "errorStack": null
  }
}
```

</details>

### 2. Operator diagnostics Pester suite

<details><summary>31 lines</summary>

```text
exit code: 0
--- stdout ---
Pester v5.9.0

Starting discovery in 1 files.
Discovery found 152 tests in 509ms.
Filter 'FullName' set to ('*operator diagnostics*').
Filters selected 17 tests to run.
Running tests.

Running tests from 'A:\Projects\christopherbell.dev-worktrees\diagnostics-recent-problems-20261005\ops\production\windows\tests\Production.AutoDeploy.Tests.ps1'
Describing operator diagnostics
  [+] redacts a fine-grained token 64ms (44ms|20ms)
  [+] redacts a classic token 2ms (2ms|1ms)
  [+] redacts a Resend key 2ms (2ms|1ms)
  [+] redacts a Bearer [REDACTED] 2ms (2ms|1ms)
  [+] redacts a JWT 19ms (19ms|1ms)
  [+] redacts Mongo credentials 2ms (2ms|1ms)
  [+] redacts a password assignment 2ms (2ms|1ms)
  [+] redacts an email address 2ms (1ms|1ms)
  [+] flattens and bounds a redacted message 19ms (18ms|0ms)
  [+] keeps only allowlisted, redacted fields from the newest structured log lines 46ms (45ms|0ms)
  [+] keeps an older error visible after newer INFO lines push it out of the latest entries 40ms (39ms|1ms)
  [+] returns only the newest problems within the scanned lines 24ms (23ms|0ms)
  [+] keeps the first redacted stack frames of an error 22ms (22ms|0ms)
  [+] publishes a bounded record that standard users read back 364ms (364ms|0ms)
  [+] sheds routine entries before problems when the record is too large 180ms (178ms|1ms)
  [+] reports the poller's published scheduler state when a standard user is denied 27ms (27ms|0ms)
  [+] keeps UNKNOWN when the published scheduler state is stale 20ms (20ms|1ms)
Tests completed in 1.64s
Tests Passed: 17, Failed: 0, Skipped: 0, Inconclusive: 0, NotRun: 135
```

</details>

## Evidence
- Case 1 started 2026-10-05T19:33:37-05:00, took 1594 ms, candidate `3571135`
- Case 2 started 2026-10-05T19:33:38-05:00, took 2562 ms, candidate `3571135`

- Harness `verify-diagnostics.ps1` (scratch, not committed), which builds the fixture, publishes and reads back:

<details><summary>verify-diagnostics.ps1</summary>

```powershell
param([Parameter(Mandatory)][string]$Checkout)
$ErrorActionPreference = 'Stop'
$modules = Join-Path $Checkout 'ops\production\windows\modules'
foreach ($name in 'Production.Common', 'Production.WriterStart', 'Production.MusicRuntime', 'Production.Install',
    'Production.Deploy', 'Production.Operations', 'Production.AutoDeploy') {
    Import-Module (Join-Path $modules "$name.psm1") -Global -Force -WarningAction SilentlyContinue
}
$root = Join-Path ([IO.Path]::GetTempPath()) ("diagnostics-verify-" + [guid]::NewGuid().ToString('N'))
$statusRoot = Join-Path $root 'status'
New-Item -ItemType Directory -Path $statusRoot, (Join-Path $root 'logs'), (Join-Path $root 'state') -Force | Out-Null
$stack = "com.mongodb.MongoTimeoutException: timed out\n\tat com.mongodb.Cluster.select(Cluster.java:10)\n\tat dev.christopherbell.feed.FeedService.load(FeedService.java:42) password=hunter2\n\tat dev.christopherbell.feed.FeedController.get(FeedController.java:7)\n\tat org.springframework.web.Dispatcher.handle(Dispatcher.java:99)"
$lines = [Collections.Generic.List[string]]::new()
$lines.Add('{"@timestamp":"2026-10-05T08:00:00Z","log":{"level":"ERROR","logger":"dev.christopherbell.feed.FeedService"},"message":"feed query failed for person@example.com","requestId":"r-early-error","error":{"type":"com.mongodb.MongoTimeoutException","message":"timed out","stack_trace":"' + $stack + '"}}')
foreach ($number in 1..19998) {
    if ($number -eq 12000) {
        $lines.Add('{"@timestamp":"2026-10-05T11:00:00Z","log":{"level":"ERROR","logger":"dev.christopherbell.feed.FeedService"},"message":"feed query failed","requestId":"r-in-window-error","error":{"type":"com.mongodb.MongoTimeoutException","message":"timed out","stack_trace":"' + $stack + '"}}')
    } elseif ($number % 500 -eq 0) {
        $lines.Add('{"@timestamp":"2026-10-05T12:00:00Z","log":{"level":"WARN","logger":"dev.christopherbell.libs.api.ControllerExceptionHandler"},"message":"INVALID_TOKEN status=401 Bearer abc.def","requestId":"r-warn-' + $number + '"}')
    } else {
        $lines.Add('{"@timestamp":"2026-10-05T12:00:00Z","log":{"level":"INFO","logger":"dev.christopherbell.http"},"message":"GET /api/feed 200 ' + $number + '","requestId":"r-' + $number + '"}')
    }
}
$lines.Add('not json at all')
Set-Content -LiteralPath (Join-Path $root 'logs\application.json.log') -Value $lines
$config = [pscustomobject]@{ programDataRoot = $root }

$result = & (Get-Module Production.AutoDeploy) {
    param($Config, $StatusRoot)
    # Production status folders carry SYSTEM-only ACLs a standard user cannot create; replace only those
    # guards and the SYSTEM task query, as the Pester tests do, and run everything else for real.
    Set-Item function:script:Assert-AutoDeployStatusDirectory { param($Path) }
    Set-Item function:script:Assert-AutoDeployStatusFile { param($Path, $MaximumBytes) }
    Set-Item function:script:Get-AutoDeployTaskSchedulerEntry { [pscustomobject]@{ registered = $true; state = 3; reason = 'NONE' } }
    Write-AutoDeployState $Config (New-AutoDeployState)
    $elapsed = Measure-Command { Publish-AutoDeployDiagnostics -Config $Config -StatusRoot $StatusRoot }
    $record = Get-AutoDeployDiagnostics -StatusRoot $StatusRoot
    [pscustomobject][ordered]@{
        publishMilliseconds = [int]$elapsed.TotalMilliseconds
        recordBytes = (Get-Item -LiteralPath (Join-Path $StatusRoot 'diagnostics.json')).Length
        schemaVersion = $record.schemaVersion
        freshness = $record.freshness
        recentLogEntries = @($record.recentLogEntries).Count
        recentLogEntriesLevels = (@($record.recentLogEntries).level | Group-Object | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ','
        recentProblems = @($record.recentProblems).Count
        recentProblemsLevels = (@($record.recentProblems).level | Group-Object | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ','
        errorProblems = @(@($record.recentProblems) | Where-Object level -eq 'ERROR')
        earlyErrorOutsideWindowPresent = [bool](@($record.recentProblems) | Where-Object requestId -eq 'r-early-error')
        oldestProblem = @($record.recentProblems)[0]
        newestProblem = @($record.recentProblems)[-1]
    }
} $config $statusRoot
$result | ConvertTo-Json -Depth 4
Remove-Item -LiteralPath $root -Recurse -Force
```

</details>
- Before the candidate commit, the full production Pester suite passed: 910 passed, 0 failed, 28 skipped.

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
