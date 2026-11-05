# Survive render allocation verification

## Story/Issue
Reduce memory churn without reducing game capacity or graphics quality.

## Branch
codex/survive-reuse-render-buffers at e86c43995e2cb9dfb974f2464c016760d45c0d8d.

## Pass / Fail
Pass.

## Test Cases
1. Compare ordinary and streamed vertex output.
2. Upload two same-sized frames and verify one GPU allocation.
3. Verify pose values fit the packed representation without loss.
4. Join in a desktop browser and walk across the bridge to the waystation.
5. Confirm exact candidate identity and clean up.

## App / Environment
http://127.0.0.1:57171/survive with test profile and disposable MongoDB on port 57170.

## Local Run Details
Invoke-Gradle.ps1 --no-daemon :website:bootJar :website:jsTest, then Start-Candidate.ps1 and Stop-Candidate.ps1.

## Data Sent
```text
Two identical render frames
Buffer Scout and keyboard W
```

## Response Received
```text
One GPU allocation for two frames
379707 pose values stored in 759414 bytes
Waystation · 0 m
Browser warnings and errors []
Both listeners removed
```

## Evidence
460 JavaScript tests passed. Node syntax and diff checks passed. Browser inspection showed the adventurer, foliage, camp and walkable route. The live heap and frame-rate impact was not benchmarked. Two idle Gradle processes using roughly 840 MB combined were stopped separately from the renderer changes.

## Bugs / Follow-ups
Whole-browser and website-service memory measurements under a busy multiplayer load remain open.

## Document Status
complete

## Project
christopherbell-dev
