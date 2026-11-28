# Survive nearest target and field camera lock

## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Select and follow a roaming target before entering melee range and retain the camera lock on Engage.

## Branch
codex/survive-field-lock at 4e27ab631aec0dce0bb3eb87e1822bd82a9323ed, based on main at 04937ce8.

## Pass / Fail
All 491 JavaScript tests passed. Syntax checks and the application build passed. Desktop Chrome verified nearest-target selection, walking toward the selected hog, combat handoff and unlock.

## Test Cases
1. F8 selects the nearest visible field label while a closer off-screen hog and a farther visible hog exist.
2. A refresh preserves a field lock, target cycling respects it, and only a matching route keeps it on entry into combat. A simulated left-stick click in Commands is delivered once.
3. In a running island, select the meadow hog from outside melee range, open Commands, lock with L, approach using W, Engage and unlock.

## App / Environment
Windows desktop Chrome at http://127.0.0.1:59282/survive. The committed JAR used the test profile and a disposable loopback MongoDB on port 59281.

## Local Run Details
The actuator identified the committed build. Browser input ran against the normal game page and command menu. The playthrough compared the WebGL camera heading with the direction to the acknowledged animal, then measured the change after manual orbit. Both candidate ports had zero listeners after shutdown.

## Data Sent
```text
node --check on changed scripts and tests
node --test website/src/test/js/survive-world.test.js website/src/test/js/survive-phone-play.test.js
./ops/local/Invoke-Gradle.ps1 :website:jsTest :website:bootJar
F8, Enter, L, walk forward, Engage, orbit while locked, L, orbit again
```

## Response Received
```text
491 JavaScript tests passed
BUILD SUCCESSFUL
Initial distance 10.8589 m, heading error 0.00091 radians
Engaged distance 0.5224 m, heading error below 0.00001 radians
Manual orbit after unlock 0.1200 radians
```

## Evidence
Field and combat screenshots were captured. The server returned meadow-hog as the active fight after the approach. Orbit input followed the normal camera step after unlocking.

## Bugs / Follow-ups
Desktop keyboard was exercised in Chrome. Controller routing was tested with a simulated standard gamepad. A physical controller remains unverified.
