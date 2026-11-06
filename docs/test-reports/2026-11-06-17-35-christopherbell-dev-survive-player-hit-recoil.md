# Survive player hit recoil: Test Report

## Story/Issue
Show a visible reaction to landed counters in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-player-hit-reaction` at `96838ea76110a7b8d36b6106af9975f6eb19a068`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `96838ea7`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Preserve foot placement | ✅ PASS | Authored stance comparison keeps lower positions and moves upper-body vertices. |
| 2 | Block and take a hog counter | ✅ PASS | Chrome recorded both exchanges and captured a visible lean only on the landed bite. |

## Test Cases
1. Compare the authored ready mesh with and without recoil. Check that a blocked counter and wind-up produce no recoil.
2. Join in Chrome, walk to the meadow hog and Engage. Guard the first counter and capture the next damaging bite.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:65082 |
| Database | Disposable MongoDB at 127.0.0.1:65081/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Actuator confirmed the exact committed candidate before Chrome loaded.
- Stop-Candidate.ps1 closed both ports and removed the runtime directories.

## Data Sent
```text
Join as Motion Scout
Walk to meadow-hog, ENGAGE, DEFEND before the first exchange
Capture the WebGL frame after the blocked and landed counters
```

## Response Received
```text
PASS: Chrome engaged a roaming hog, consumed a guard on the first exchange, and received the next bite with the confirmed damage in chat.
port 65082 listeners: 0
port 65081 listeners: 0
```

## Evidence
- All 468 JavaScript tests, changed-script syntax checks and candidate build passed.
- Inspected blocked and landed frames at the same viewpoint. The latter shows the shoulders and head farther back while the foot placement reads consistently.

## Bugs / Follow-ups
The visual proof covers nonfatal local counters. Reduced motion uses the same gate as the counter animation but was not exercised in this browser run. Defeat and remote hit reactions remain open.

## Document Status
complete

## Project
christopherbell-dev
