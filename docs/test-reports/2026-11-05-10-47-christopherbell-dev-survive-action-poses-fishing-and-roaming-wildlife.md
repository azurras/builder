# Survive action poses, fishing and roaming wildlife verification

## Story/Issue
Animate island actions, add fishing, and give wildlife shared routes with passive and hostile behavior. Improve the shoreline and world presentation.

## Branch
codex/survive-actions-fishing-wildlife at 9d2c28a9c33fadbb33b1be3d9d0b155fcae283a9.

## Pass / Fail
Pass for the first action-animation and wildlife release. Full Final Fantasy XI visual fidelity is a separate quality target.

## Test Cases
1. Use accepted movement to approach a passive hog and initiate Hunt explicitly.
2. Cross a wolf's aggro distance and verify the encounter is committed and the wolf is reserved.
3. Use the in-world Map and Commands to fish. Observe the rod, line, shoreline and chat results at desktop and phone width.
4. Verify action meshes, fishing validation, roaming and expiry behavior with native tests.

## App / Environment
http://127.0.0.1:50068/survive, exact test profile, disposable Mongo test at 127.0.0.1:50067.

## Local Run Details
Built the committed candidate with Invoke-Gradle.ps1. Start-Candidate.ps1 started the application with the exact isolated test profile. The actuator version matched the candidate.

## Data Sent
```text
Survivors: Meadow Tester, Pine Tester, Bank Scout
Movement requests: bounded steps towards meadow-hog and pine-wolf
Browser map destination: Fishing bank
Browser command: Fish
Phone viewport: 390 × 844
```

## Response Received
```text
Hostile wildlife: pine-wolf COMBAT The wolf spots you and attacks!
Passive wildlife: within four metres and still EXPLORING. Hunt revealed HOG
Bank Scout: You cast your line, but the fish got away.
Bank Scout: You reel in a fish. You gained 1 food.
{ scrollWidth: 375, webgl: 'true', width: 390 }
port 50068 listeners: 0
port 50067 listeners: 0
```

## Evidence
450 JavaScript tests, the focused Survive Java tests and both Checkstyle checks passed. Node syntax checks and git diff --check passed. Local runtime checks used the normal client API and browser controls. Browser viewport reset and the isolated runtime was removed.

The full Java suite ran 2,204 cases with zero failures or errors and 126 configured skips. PR #1564 merged as 936c59148222e638291415945ae6b4beb0039366. Merged CI and CodeQL passed, and production served the exact build and the Fishing bank control.

## Bugs / Follow-ups
Fishing is one cast command with an animated outcome. There is no gear or timing minigame. Action gestures are local. Roaming paths and reservations belong to one application process. Active combat still uses durable survivor state. The updated procedural meshes and effects are an art pass toward the FFXI target.

## Document Status
complete

## Project
christopherbell-dev
