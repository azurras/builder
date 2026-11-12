## Story/Issue
Remove the bright seam at the Survive fishing-bank horizon under ART-02.

## Branch
`codex/survive-sky-material` at `55e135b489df2fa4957b0bf03377349bee5addef`, stacked on shoreline candidate 62360467.

## Pass / Fail
Daylight desktop comparison and local checks passed. Nighttime comparison and release are pending.

## Test Cases
1. Verify that both hemispheres of the dome use the sky material.
2. Walk to the fishing bank with acknowledged movement. Resume in desktop Chrome, reset the camera with Home, and compare the horizon at the same follow distance.

## App / Environment
Isolated candidate on 127.0.0.1:59058 and disposable MongoDB on 127.0.0.1:59057/test. Desktop Chrome with software WebGL.

## Local Run Details
Verified actuator build identity before opening Chrome. The geometry regression failed before the fix and passed afterward. Changed scripts passed syntax checks, all 476 JavaScript tests passed, and bootJar succeeded.

## Data Sent
```text
Acknowledged movement to (-11, 66), resume game, reset camera and capture the viewport.
```

## Response Received
```text
PASS: desktop Chrome resumed the angler at the bank and captured its shoreline at the default follow distance.
port 59058 listeners: 0
port 59057 listeners: 0
```

## Evidence
Compared the local images survive-bank-art-shore.png and survive-sky-shore.png. The bright strip was absent in the second image. The game clock differed, with both captures in daylight. The renderer now assigns the sky shader by dome material, so the lower hemisphere receives the horizon color.

## Bugs / Follow-ups
Nighttime, the full route and physical GPU comparison remain open.

## Document Status
complete

## Project
christopherbell-dev
