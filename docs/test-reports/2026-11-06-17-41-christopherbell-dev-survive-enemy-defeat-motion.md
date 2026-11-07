# Survive enemy defeat motion: Test Report

## Story/Issue
Keep the defeated target visible through a short fall in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-enemy-defeat-motion` at `5baf77f6a1dcdcb275ee954cdd739ba3fe5b2468`, based on the player hit-reaction branch.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `5baf77f6`.

| # | Test case | Result | Why |
|---|---|---|
| 1 | Distinguish victory from other exits and roll wildlife | ✅ PASS | Tests cover personal and party wins, flee, player death, cue expiry and boar geometry. |
| 2 | Defeat a roaming hog in desktop Chrome | ✅ PASS | Frames show the hog standing, fallen with the ring gone and cleared, with victory and reward in chat. |

## Test Cases
1. Verify victory detection, fall timing and UVs in the boar mesh.
2. Join, approach meadow-hog, engage, guard the first bite and wait for the finishing strike.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:51238 |
| Database | Disposable MongoDB at 127.0.0.1:51237/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Verified exact actuator version before opening Chrome. Both ports closed and temporary directories were removed.

## Data Sent
```text
Join as Motion Scout
Walk to meadow-hog, ENGAGE, DEFEND
Capture the WebGL view before and during the fall, then capture the cleared field and chat
```

## Response Received
```text
PASS: Chrome defeated the meadow hog, confirmed victory in chat and captured the falling and cleared target.
port 51238 listeners: 0
port 51237 listeners: 0
```

## Evidence
- All 470 JavaScript tests, changed-script syntax checks and candidate build passed.
- Inspected the standing, fallen and cleared images. The fallen frame shows the hog on its side at contact range with no red target ring. The cleared frame shows the victory and one food in chat.

## Bugs / Follow-ups
The runtime check covers a personal hog victory. Party victory detection is unit-tested. Shared-fight, raider and player collapse visuals still need direct browser checks or implementation. The defeat cue is local presentation without a new shared event.

## Refreshed release candidate
Candidate 5cb9e0bde7fa9a1f0b63516fa3a87a1df693cfb3 includes the live main stance and hit reaction. All 470 JavaScript tests, changed-script syntax checks and bootJar passed. Its exact actuator version was checked at http://127.0.0.1:59683 with disposable MongoDB at 127.0.0.1:59682/test. Chrome repeated the standing, falling and cleared meadow-hog case. Both listeners closed at teardown.

## Strike integration and reduced motion
Candidate 812ac98ea72a23e8d5b2f154bcc18ed69c40a9cf includes the merged shared-strike code. All 471 JavaScript tests, changed-script syntax and bootJar passed. Exact actuator identity was checked in two separate test runtimes.

Normal motion ran at http://127.0.0.1:59391 with MongoDB on 127.0.0.1:59390/test. Reduced motion ran at http://127.0.0.1:51418 with MongoDB on 127.0.0.1:51417/test. Both Chrome runs defeated the meadow hog and confirmed reward chat. The normal frame shows the hog on its side during the fall. The reduced-motion frame at the same point after victory shows the target already cleared. All four listeners closed at teardown.

## Nearby-presence integration verification
Candidate d791612d0e16921369f43ba7b0924f51ea5c82d0 includes merged main 012bb295. All 471 JavaScript tests and bootJar passed. Exact actuator identity was verified at http://127.0.0.1:55392 with disposable MongoDB at 127.0.0.1:55391/test. Chrome repeated the standing, falling and cleared meadow-hog sequence and victory chat. Inspected the captured fall: the hog is on its side at the finishing position. Both listeners closed during cleanup. Reduced motion was previously verified on 812ac98 with the same defeat implementation; this integration run repeated normal motion only.
## Timed-fishing integration verification
Candidate c672dee1d618e4b526ace9e45e77d36bc4756dbb includes live main 125bd326. The merge retained both fishing and defeat state in the render loop. All 472 JavaScript tests and bootJar passed. Verified exact actuator identity at http://127.0.0.1:54947 with disposable MongoDB at 127.0.0.1:54946/test. Chrome repeated the hog fall and victory chat, then independently reached the fishing bank, showed the bite, reeled in time and let a second cast expire. Both listeners closed. Reduced motion was verified on the earlier 812ac98 build.
## Document Status
complete

## Project
christopherbell-dev
