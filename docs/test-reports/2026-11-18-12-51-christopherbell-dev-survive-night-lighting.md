## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Distinguish night from dusk and make the waystation entrance readable under ART-02.

## Branch
codex/survive-moonlight at 7fe53d6ecc0967ab95e4ff2e6295d2a23d61343d. Comparison build 0641a60e7512c22c60e5fb42510c29d85c80c2c6 has the same tree as main at e734f93aac4fcc085cb2333e8467ec217abf4b5b.

## Pass / Fail
Passed JavaScript syntax checks, all 479 browser-side tests, the exact application build, matched nighttime captures and a keyboard approach to the lit entrance.

## Test Cases
Verify that the point light sits inside the lantern and that the glass is attached beside the waystation door. Compare matching night views at the forest, stream bridge and waystation. Check that the lantern illuminates nearby stone and falls off toward the trail. Compare daytime wall and trail colors and walk up to the door.

## App / Environment
Desktop Chrome with a 1366 × 900 window and 1350 × 805 captures. Hardware WebGL used the NVIDIA GeForce RTX 4070 through ANGLE and D3D11. Baseline http://127.0.0.1:64960/survive and candidate http://127.0.0.1:64538/survive used separate disposable loopback MongoDB test databases.

## Local Run Details
The actuator matched each exact source commit. The harness set the browser's displayed phase for matched screenshots and held the same water shader time. The normal movement API acknowledged the positions. Both candidate and database listener pairs closed and disposable directories were cleaned up.

## Data Sent
```text
Compare NIGHT at forest (-17,-10) and bridge (0,-26), rotating the camera twelve steps.
Compare DAY and NIGHT looking north at the waystation (1.2,-33).
Walk north toward the lantern with W.
```

## Response Received
```text
479 JavaScript tests passed.
54,795 baseline and 54,839 candidate static triangles against the existing 55,000 limit.
The 16 × 16 nighttime masonry crop averaged RGB (60.2, 56.2, 38.8) baseline and (145.6, 93.4, 58.9) candidate.
The distant path crop averaged RGB (78.7, 68.5, 43.1) baseline and (57.4, 62.3, 55.1) candidate.
Both sampled areas matched in DAY. Server acknowledged the approach to z = -36.0.
```

## Evidence
The lantern and nearby doorway are visibly warmer than the surrounding route. Cool fills retain trail and stream shape at night. The side-by-side daylight checks preserve the nearby stone and path colors while showing the unlit fixture.

## Bugs / Follow-ups
The shader limits light to the front half-space and does not calculate cast shadows. This sample predates the woodland candidate and does not establish the combined canopy appearance, full-route coverage, or sustained frame cost.
