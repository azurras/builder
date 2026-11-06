# Survive North Gate art: Test Report

## Story/Issue
Review the first camp-to-waystation art pass in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-north-gate-art` at `2789796afcb91e70d0c78b97f6f4604d2d867098`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** for local runtime on candidate `2789796a`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Render and walk the starting route | ✅ PASS | Chrome rendered the adjusted adventurer, keeper and waystation and exposed Talk at the existing destination. |

## Test Cases
1. **Render and walk the starting route.** Join at camp, toggle page view and back, walk to the keeper using KeyW, capture the scene and open the replacement join form.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile on `http://127.0.0.1:63843` |
| Database | Disposable MongoDB at `127.0.0.1:63842/test` |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.2789796afcb91e70d0c78b97f6f4604d2d867098`.
- **Cleanup:** Both runtime ports closed and the disposable database and socket directory were removed.

## Data Sent
### 1. Render and walk the starting route
```text
Join a new survivor at camp, toggle page view and back.
Walk north using KeyW until Talk to Waystation Keeper appears.
Capture the scene and open the replacement join form.
```

## Response Received
### 1. Render and walk the starting route
```text
Game canvas height: 759.015625 Browser height: 805
PASS: browser-filling game, page view toggle, movement to the keeper, and replacement join form in page view
port 63843 listeners: 0
port 63842 listeners: 0
```

## Evidence
- JavaScript suite and candidate build passed. Asset tests checked unchanged clip topology and texture coordinates, hand attachments, animated motion and static geometry bounds.
- Desktop screenshots at camp and the waystation were inspected. The keeper cap, mantle, added frontage and road plants rendered. The waystation image was captured at dusk, so it is a qualitative review rather than a matched lighting comparison.

## Bugs / Follow-ups
The keeper's mantle still looks stiff. The first pass did not verify an improved contact pose, new enemy attacks, a matched lighting comparison, frame time or memory.

## Document Status
complete

## Project
christopherbell-dev
