# Survive body selection and encounter handoff

## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Click an animal directly and retain it as the target when the field encounter starts.

## Branch
codex/survive-persistent-target at e3cc327ee528aa7657cae1e0a4323908d4c0d8ac, based on main at 957adb1a.

## Pass / Fail
Passed the full website build, all 490 JavaScript tests, Java Checkstyle and desktop Chrome body selection. The build skipped environment-dependent tests according to their existing conditions.

## Test Cases
1. Reproduce lost Tab selection, the duplicate same-species body and the unhandled body click before the patch. Verify Tab wraps and a drag or an empty click cannot select a field target.
2. Exercise both arrival orders of combat and movement replies. Preserve the other hog and remove the selected hog's roaming label and mesh when combat takes over.
3. Verify the solo command and movement replies identify the same animal, and a shared encounter survives restart and clears at defeat.
4. Walk to the meadow hog, click its onscreen body, Engage, then Disengage without clicking another target.

## App / Environment
Desktop Chrome on Windows, local game at http://127.0.0.1:63637/survive with the exact test profile and disposable MongoDB on 127.0.0.1:63636.

## Local Run Details
The committed JAR's actuator build identity matched the branch SHA. The mouse input used Chrome's Input.dispatchMouseEvent on a point inside the canvas underneath the hog's label. Startup and shutdown used the repository's candidate helpers. Both listeners closed and the disposable database and JDK socket directories were removed.

## Data Sent
```text
node --test website/src/test/js/survive-world.test.js
node --check on each changed JavaScript file
./ops/local/Invoke-Gradle.ps1 :website:build
Mouse down and up on the rendered meadow hog, then select Engage and Disengage.
```

## Response Received
```text
490 JavaScript tests passed
BUILD SUCCESSFUL
PASS: real mouse body click selected meadow-hog, Engage used the same route, the roaming label was removed, and Disengage kept the same target.
```

## Evidence
The browser recorded selected, engaged and disengaged screenshots. The game response returned fieldEncounter.id equal to meadow-hog and the combat marker remained pressed after the strike timer stopped. The field-label DOM contained no second meadow-hog marker during combat.

## Bugs / Follow-ups
The browser playthrough covered a solo mouse encounter. Shared combat identity and keyboard cycling were covered by automated service and input tests. A physical controller was not exercised.
