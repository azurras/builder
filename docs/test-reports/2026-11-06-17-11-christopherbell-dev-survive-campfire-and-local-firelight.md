# Survive campfire and local firelight: Test Report

## Story/Issue
Improve the first camp landmark in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-camp-firelight` at `8216f2326957ba3a491fa1b19f5f40547b8c068d`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `8216f232`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Geometry budget and rotation | ✅ PASS | The flame spans one UV-mapped quad across two tested camera angles. |
| 2 | Desktop fire and reduced motion | ✅ PASS | Chrome rendered soft fire and an ember, and reduced motion froze the fire region. |

## Test Cases
1. Check the flame geometry at two perpendicular camera angles.
2. Join the test island, capture two desktop frames per motion preference, inspect the fire and compare the same crop.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:57808 |
| Database | Disposable MongoDB at 127.0.0.1:57807/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Verified exact actuator build before the Chrome session.
- Stop-Candidate.ps1 closed both listeners and removed both runtime directories.

## Data Sent
```text
/survive
Join as Motion Scout
Emulation.setEmulatedMedia prefers-reduced-motion=reduce after the first two captures
Compare crop x=1030..1199 and y=380..569 in each pair
```

## Response Received
```text
PASS: desktop Chrome joined the island and rendered the adventurer at the default camp camera.
Campfire crop pixels changed: normal motion 12324, reduced motion 0
port 57808 listeners: 0
port 57807 listeners: 0
```

## Evidence
- All 466 JavaScript tests, changed-script syntax checks and candidate build passed.
- Inspected the daylight camp capture showing textured pit rocks and logs, translucent flame edges, one visible ember, and warm ground near the fire.
- The fire uses two dynamic triangles, down from twenty-one. The static pit has more detail.

## Bugs / Follow-ups
Only the daylight starting camera was captured. Nighttime firelight, the full route, and physical GPU cost remain unmeasured for this candidate.

## Document Status
complete

## Project
christopherbell-dev
