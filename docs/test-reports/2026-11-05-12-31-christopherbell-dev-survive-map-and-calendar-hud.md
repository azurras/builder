# Survive map and calendar HUD verification

## Story/Issue
Put the date and time inside the game view, replace map travel buttons with a map, and keep event history in chat.

## Branch
codex/survive-world-clock-map-and-raids at a7facd1072395582e29160388c042a3bb1de8b56.

## Pass / Fail
Pass.

## Test Cases
1. Verify the calendar advances and rolls into the next date at midnight.
2. Open the island map and check that it fits in the viewport.
3. Close the map, walk by keyboard and reopen the map to verify the marker follows.
4. Check the journal and bottom movement buttons are removed.
5. Shut down the isolated runtime and check listener cleanup.

## App / Environment
http://127.0.0.1:57588/survive with the exact test profile and disposable Mongo on loopback port 57587.

## Local Run Details
Built the committed candidate using Invoke-Gradle.ps1 bootJar and jsTest. Started it using Start-Candidate.ps1. Actuator matched the commit.

## Data Sent
```text
Survivor Calendar Scout
Minus > Map > Escape > W for 720 ms > Map
```

## Response Received
```text
Calendar 05/19/1003 · 23:13
Marker transform moved from translate(0.0 0.0) to translate(0.0 -4.4)
Calendar in viewport true
Map fits true
Journal absent
Movement buttons 0
Ports 57588 and 57587 listeners 0
```

## Evidence
All 454 JavaScript tests passed. Node syntax checks and git diff --check passed. Desktop browser showed the full map in the viewport with the calendar visible.

## Bugs / Follow-ups
The game calendar starts in year 1000 and advances one game minute per real second. Controller hardware was unavailable for this check. Hunger and raiders are separate gameplay changes.

## Document Status
complete

## Project
christopherbell-dev
