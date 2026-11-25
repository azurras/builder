## Document Status

Complete

## Project

christopherbell-dev

## Story/Issue

Consolidate the fishing-bank horizon fix from PR #1603 with the moonlight and waystation lantern from PR #1629.

## Branch

`codex/survive-horizon-lighting` at `79ce257b69ad4688d2abeba812e5bbaac0bdfc70`, based on main `d71983888917677df858eb3dc7203cfaceaf7ee8`.

## Pass / Fail

Passed. All 483 browser-side tests passed and the committed application built. Desktop playthroughs covered six views across four locations.

## Test Cases

1. Check sky geometry above and below the water horizon, the lantern position inside the glass and the existing stream and bridge geometry.
2. Resume guests at the forest, bridge and waystation. Check the night uniform on a rendered WebGL frame and walk north toward the lit entrance.
3. Resume a guest at the fishing bank. Check the horizon and water from the same position and default follow distance in daylight and at night.

## App / Environment

Windows desktop Chrome, 1366 × 900 window. Forest, bridge and waystation rendered on an NVIDIA GeForce RTX 4070 through ANGLE D3D11. Shoreline views used Chrome's SwiftShader backend. The app ran at http://127.0.0.1:60727/survive with the test profile and a disposable MongoDB at 127.0.0.1:60726/test.

## Local Run Details

Checked syntax on all three changed scripts, ran the 26 world-art tests, then ran the repository's JavaScript suite and bootJar. The actuator identified the built application as 0.0.0-dev.79ce257b69ad4688d2abeba812e5bbaac0bdfc70. Normal game and movement requests established four guest positions. The browser harness selected the displayed phase for matched views and held water time steady in the hardware captures.

## Data Sent

```text
GET /actuator/info
GET /survive
POST /api/survive/v1/game to create the four guests
POST /api/survive/v1/movement to acknowledged forest (-17,-10), bridge (0,-26), waystation (1.2,-33) and fishing bank (-11,66)
Reset the camera with Home, compare DAY and NIGHT and approach the waystation with W.
```

## Response Received

```text
26 focused tests passed. Full JavaScript suite passed 483/483. BUILD SUCCESSFUL.
Verified candidate 79ce257b69ad4688d2abeba812e5bbaac0bdfc70
North approach: -36.003600000000034
PASS: desktop night forest, bridge and waystation captures.
Reached the fishing bank using acknowledged movement.
Both fishing-bank captures completed at (-11,66).
port 60727 listeners: 0
port 60726 listeners: 0
```

## Evidence

The night waystation capture shows amber glass and warm stone around the door, with the path and trees visibly cooler. The daytime capture shows the fixture against the sunlit masonry. The stream is visible beneath the bridge at night. Both shoreline captures show a continuous sea horizon without the previous bright band. Source material bands for the stream, lantern glass and sky sit on distinct half steps. The stop script removed the disposable database and JDK socket directories.

## Bugs / Follow-ups

On November 25, main added the renderer memory regression test. The refreshed
candidate at 62a09587a92005122800ee608df92fb8a2f17eaf retains that test and
both lighting material imports. All 485 JavaScript tests and the application
build passed. Desktop Chrome exercised the night forest, bridge and waystation
on an RTX 4070 against the identity-verified build at http://127.0.0.1:52290/survive.
The candidate and disposable database listeners closed after the playthrough.

The test covered fixed day and night views. It did not measure frame timing, exercise a natural clock transition, or verify a production deployment.

