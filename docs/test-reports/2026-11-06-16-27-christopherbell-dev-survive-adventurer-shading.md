# Survive adventurer shading: Test Report

## Story/Issue
Reduce flat triangle shading on the adventurer as part of the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-adventurer-shading` at `c7721fbc26276798d5eaaf70111390aca5feaeda`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `c7721fbc`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Smooth corners and retain a crease | ✅ PASS | Adjacent faces share shade at a shallow edge and differ at a steep edge. |
| 2 | Render at the desktop camp camera | ✅ PASS | A new survivor rendered with the existing texture and silhouette. |

## Test Cases
1. Verify uploaded corner shades, geometry size and shading around two angles.
2. Join the test island in Chrome and inspect a capture from the initial desktop camera.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:56741 |
| Database | Disposable MongoDB at 127.0.0.1:56740/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Started with Start-Candidate.ps1 and verified the exact actuator build version.
- Stop-Candidate.ps1 closed both ports and removed the runtime directories.

## Data Sent
```text
/survive
Join as Motion Scout
```

## Response Received
```text
PASS: desktop Chrome joined the island and rendered the adventurer at the default camp camera.
port 56741 listeners: 0
port 56740 listeners: 0
```

## Evidence
- All 465 JavaScript tests, changed-script syntax checks and the candidate build passed.
- Inspected survive-shading-camp.png from the isolated browser run.
- The mesh still uses the same number of vertices and the same atlas.

## Bugs / Follow-ups
The shot was taken at dusk. A matched before-and-after capture and physical GPU benchmark remain open. Face, hands and cloth still need work at desktop scale.

## Document Status
complete

## Project
christopherbell-dev
