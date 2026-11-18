## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Give pines recognizable needle boughs and a different crown shape for ART-02.

## Branch
codex/survive-woodland-trunks at 131e06e0af6dee73d029f01b56885c8960404249, built in the woodland canopy checkout. The combined candidate contains the trunk work and foliage atlas. Comparison build 0641a60e7512c22c60e5fb42510c29d85c80c2c6 matches the tree of main at e734f93aac4fcc085cb2333e8467ec217abf4b5b.

## Pass / Fail
Passed JavaScript syntax checks, all 480 browser-side tests, the exact application build, matching desktop daylight and dusk views, and a keyboard walk into the forest.

## Test Cases
Verify that pines and broadleaf trees select the correct padded halves of the atlas and that the single foliage texture uploads as 512 × 256. Compare the combined woodland candidate with current main at the same camera position and light. Check that the canopy and trunk variations remain visible while entering the grove.

## App / Environment
Desktop Chrome with a 1366 × 900 window and 1350 × 805 captures. Hardware WebGL used the NVIDIA GeForce RTX 4070 through ANGLE and D3D11. Baseline http://127.0.0.1:50404/survive and candidate http://127.0.0.1:62157/survive used separate disposable loopback MongoDB test databases.

## Local Run Details
Both builds reported the exact commit on the actuator. The views used the same acknowledged position, camera keys and displayed lighting. A single atlas combines the original broadleaf cutout with an original painted pine bough. Runtime listeners closed and the test databases and socket directories were cleaned up.

## Data Sent
```text
Walk to (-17, -10), reset the camera and turn right twelve times. Capture DUSK and DAY. Walk into the grove with W.
```

## Response Received
```text
480 JavaScript tests passed. Main has 54,795 static triangles and the combined candidate has 54,647.
Foliage PNG payload 394,776 to 203,260 bytes.
One texture sampler. Atlas grows from 256 × 256 to 512 × 256 on the GPU, about 0.33 MiB additional RGBA storage including mipmaps.
Server-confirmed walk ended at x = -24.2295.
```

## Evidence
Dark needle boughs and shorter upper tiers distinguish pines from the brighter broadleaf crowns. The terrain, trail and canopy remain readable in both matched lighting phases. The view from inside the grove shows the new foliage and root shapes together.

## Bugs / Follow-ups
The foliage remains cutout cards, and one pine bough is reused across trees. Night lighting, sustained frame cost and the full desktop route review remain open.
