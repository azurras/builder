## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Improve the water and timber crossing at North Gate under ART-02.

## Branch
codex/survive-north-gate-stream at b823187617abfac0573529cfcf04e923f810387f. Masonry baseline 67cd6e0390535f61cd4dfadb5bb4a334cd2fb01a.

## Pass / Fail
Passed JavaScript syntax checks, 476 browser-side tests, the candidate build, desktop day and dusk rendering, and keyboard traversal of the bridge in both directions.

## Test Cases
Check the water plane and bed depth at the center and edges, deck height and static geometry budget. Compare the same bridge view in day and dusk lighting. Advance the shader clock at the dusk viewpoint and verify that the water pixels change. Walk off the bridge in both directions with the keyboard and verify movement through the server.

## App / Environment
Desktop Chrome with a 1366 × 900 window and 1350 × 805 capture area. Hardware WebGL used the NVIDIA GeForce RTX 4070 through ANGLE and D3D11. Baseline http://127.0.0.1:63300/survive and candidate http://127.0.0.1:61401/survive used separate disposable loopback MongoDB test databases.

## Local Run Details
The actuator reported the exact build commit for both runs. The harness put both survivors at the same server-confirmed bridge position, turned the camera the same amount, and controlled the rendered phase and shader time for comparison. Both app and database listeners closed and temporary database and socket directories were removed.

## Data Sent
```text
Move to (0, -26) in range-limited steps. Reset camera with Home, then rotate with R twelve times. Capture DAY and DUSK at shader time 2.4 seconds. In DUSK advance shader time to 3.15 seconds, then reset the camera and walk north with W and south with S.
```

## Response Received
```text
476 JavaScript tests passed.
54,795 candidate static triangles, up from 54,303. Existing limit 55,000.
All 299 sampled water pixels changed against the dusk baseline. With time advanced, 287 of the same 299 pixels changed.
Server-confirmed north exit z = -35.9168 and south exit z = -16.7498.
```

## Evidence
The flat stream is now darker at depth, with a stony, lighter transition at the banks and narrow ripples colored by the sky. Under the bridge, the water and highlights darken beside the recessed supports. Chrome captures show the same features in cooler daylight and warmer dusk.

## Bugs / Follow-ups
The bridge banks, vegetation and silhouettes remain simpler than the supplied visual reference. Full-route nighttime review and GPU frame timing were outside this check. The local traversal confirms movement through the crossing but did not capture a continuous video.
