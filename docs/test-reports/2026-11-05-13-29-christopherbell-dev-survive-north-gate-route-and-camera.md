# Survive north gate route and camera verification

## Story/Issue
Build the first player-scale FFXI-inspired route and camera controls while preserving Survive's menus.

## Branch
codex/survive-starting-zone at 7855a84985adc4991e93c1439a1e9868d1545628.

## Pass / Fail
Pass for the route and camera slice.

## Test Cases
1. Join camp and inspect the lower follow camera and sight line through the banks to the gate.
2. Zoom in using Page Up, reset with Home and walk across the bridge to the waystation.
3. Open Map and confirm the route and location are visible.
4. Verify the exact rebased runtime and clean up the isolated candidate.

## App / Environment
Desktop WebGL and disposable loopback Mongo with profile test. Visual candidate at http://127.0.0.1:63958/survive. Rebased runtime at http://127.0.0.1:55885/survive.

## Local Run Details
Built with Invoke-Gradle.ps1 bootJar and jsTest. Start-Candidate.ps1 and Stop-Candidate.ps1 controlled the isolated runtimes. The rebase preserved the exact tree tested in the browser.

## Data Sent
```text
North Gate Scout
Page Up, Home, W, Minus, Map
GET /survive and camera modules
```

## Response Received
```text
Waystation · 0 m
Map expanded at the waystation
No browser warnings or errors
Rebased actuator matched candidate and asset responses returned 200
Candidate and Mongo listeners removed
```

## Evidence
All 458 JavaScript tests passed. Node syntax and diff checks passed. Desktop browser showed the framed gate, the walkable timber bridge over a stream and the stone waystation. Automated tests verify target lock, zoom reset, controller zoom routing, projection, bridge height and the static geometry budget.

## Bugs / Follow-ups
Controller routing was covered by automated tests. Physical controller hardware was unavailable. The waystation is an environmental landmark and has no assignment yet. Party combat and coordinated skills remain open in the starting-zone plan.

## Document Status
complete

## Project
christopherbell-dev
