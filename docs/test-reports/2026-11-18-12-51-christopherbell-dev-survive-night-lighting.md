## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Distinguish night from dusk and make the waystation entrance readable under ART-02.

## Branch
codex/survive-moonlight at 8622d40d11d4070aa2f6f1285312379e74bd2b00 after incorporating woodland merge f39bbef53819f1f38af4c9438a39806927282438. The integrated comparison used woodland build 131e06e0af6dee73d029f01b56885c8960404249, which has an identical Git tree to the merge. The initial comparison used lighting candidate 7fe53d6ecc0967ab95e4ff2e6295d2a23d61343d and reference 0641a60e7512c22c60e5fb42510c29d85c80c2c6.

## Pass / Fail
Passed JavaScript syntax checks, all 479 browser-side tests, the exact application build, matched nighttime captures and a keyboard approach to the lit entrance.

The integrated candidate passed all 481 browser-side tests and repeated the three nighttime captures and the waystation approach. Frame interval p95 stayed within 7.1 to 7.2 ms in both builds across the measured forest and waystation windows.

## Test Cases
Verify that the point light sits inside the lantern and that the glass is attached beside the waystation door. Compare matching night views at the forest, stream bridge and waystation. Check that the lantern illuminates nearby stone and falls off toward the trail. Compare daytime wall and trail colors and walk up to the door.

## App / Environment
Desktop Chrome with a 1366 × 900 window and 1350 × 805 captures. Hardware WebGL used the NVIDIA GeForce RTX 4070 through ANGLE and D3D11. Baseline http://127.0.0.1:64960/survive and candidate http://127.0.0.1:64538/survive used separate disposable loopback MongoDB test databases.

Integrated visual comparison used http://127.0.0.1:56644/survive and http://127.0.0.1:55878/survive. Timing used baseline http://127.0.0.1:58617/survive and http://127.0.0.1:53928/survive and candidate http://127.0.0.1:52635/survive and http://127.0.0.1:53091/survive.

## Local Run Details
The actuator matched each exact source commit. The harness set the browser's displayed phase for matched screenshots and held the same water shader time. The normal movement API acknowledged the positions. Both candidate and database listener pairs closed and disposable directories were cleaned up.

The timing sessions used live shader time and kept screenshots in separate browser launches. Each build had two 22-second windows per site, with the camera turning one step per second from the same acknowledged positions. The initial baseline timing run completed the forest windows. The inactive waystation guest position expired before the next scene loaded, so a fresh fixture supplied the remaining baseline windows and each candidate scene. The integrated forest shutdown printed warnings for child processes but listener, directory and PID readback confirmed cleanup.

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
Integrated candidate uses 54,691 island triangles against 54,647 in the woodland baseline.
Integrated approach reached z = -36.2502.
Frame p95 in ms, two windows per site:
forest baseline 7.2, 7.2 and integrated candidate 7.2, 7.2
waystation baseline 7.1, 7.2 and integrated candidate 7.1, 7.1
Median 6.9 ms and p99 7.2 ms in each window, with zero intervals above 25 ms.
```

## Evidence
The lantern and nearby doorway are visibly warmer than the surrounding route. Cool fills retain trail and stream shape at night. The side-by-side daylight checks preserve the nearby stone and path colors while showing the unlit fixture.

## Bugs / Follow-ups
The shader limits light to the front half-space and does not calculate cast shadows. The integrated views cover the forest, bridge and waystation with the new foliage. The timing windows establish frame cadence at two viewpoints. Sustained memory, GPU processing time, multiplayer load and the remaining desktop route are still open.
