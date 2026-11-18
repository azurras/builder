## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Release the CPU-side copy of the uploaded scenery under PERF-01 and AC-6.

## Branch
codex/survive-render-residency at c3f72d867bae320b04d4bc4bcf769ac99240d2ab. Baseline build 131e06e0af6dee73d029f01b56885c8960404249 has the same tree as merged main at f39bbef53819f1f38af4c9438a39806927282438.

## Pass / Fail
Passed JavaScript syntax checks, all 481 browser-side tests, the exact application build, and the matched Chrome scenery and retained-heap checks.

## Test Cases
Verify that the renderer uploads static scenery once, draws the full vertex count repeatedly, and deletes the buffer on disposal. Compare the uploaded bytes, visual scene and retained JavaScript heap at the same North Gate position. Inspect heap retention paths after repeated camera movement.

## App / Environment
Desktop Chrome with a 1366 × 900 window and hardware WebGL on an NVIDIA GeForce RTX 4070 through ANGLE and D3D11. Baseline http://127.0.0.1:54624/survive and candidate http://127.0.0.1:54330/survive used separate disposable loopback MongoDB test databases.

## Local Run Details
The actuator matched both exact source commits. Each Chrome run started at server-acknowledged (-6, -9) with daylight held for comparison. The harness loaded the authored model and recorded the static upload without keeping the array. DevTools collected garbage before four heap samples and inspected the final snapshot. Both app and database listener pairs closed and the disposable directories were removed.

## Data Sent
```text
Open Survive at (-6, -9), warm up, then alternate the camera right and left every second for three 10-second loops.
Collect garbage and measure JS heap after warm-up and after each loop. Hash data provided to the static WebGL buffer.
```

## Response Received
```text
481 JavaScript tests passed.
Baseline retained JS heap bytes: 19,492,584; 19,364,788; 20,040,988; 20,045,980.
Candidate retained JS heap bytes: 4,612,368; 5,074,668; 5,092,752; 5,163,812.
Final retained JS heap difference: 14,882,168 bytes (14.19 MiB, approximately 74%).
Baseline scenery array retained 14,923,792 bytes. The candidate lacked that retaining path.
Both builds performed one 5,901,876-byte static upload with SHA-256:
15a53e24da20f03432cb936aa537ed53b0bf988342a6ba971eaa4dd193ea3b49
```

## Evidence
In the baseline snapshot a renderer context held the scenery object, which held its vertices array. The candidate draw closure keeps the vertex count and the GPU buffer. The matching upload hash and the rendered North Gate view verify that the full static scenery is still sent to WebGL.

## Bugs / Follow-ups
This sample measures retained JavaScript heap at one desktop scene over three short loops. Total browser process RAM, GPU memory, long-session retention and multiplayer load remain open under AC-6.
