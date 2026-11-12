# Survive fishing bank artwork: Test Report

## Story/Issue
Add shoreline structure around the fishing approach under ART-02 in the [living parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-fishing-bank-art` at `aa38c563cd39133cdf6ada799adcc08d24b49f5d`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `aa38c563`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Desktop shoreline at the fishing bank | ✅ PASS | Chrome rendered the rock groups, bent reeds, dock and sand transition after acknowledged travel from camp. |

## Test Cases
1. Travel to the bank using acknowledged movement, resume in Chrome and face the shoreline at the default desktop camera.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:63092 |
| Database | Disposable MongoDB at 127.0.0.1:63091/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Verified exact actuator identity before opening Chrome.
- Stopped both listeners and removed both temporary runtime directories.

## Data Sent
```text
Move from camp to (-11, 66) in acknowledged steps
Resume in Chrome and face the shoreline using Home
Capture the viewport at the default follow distance
```

## Response Received
```text
Reached the fishing bank using acknowledged movement.
PASS: desktop Chrome resumed the angler at the bank and captured its shoreline at the default follow distance.
port 63092 listeners: 0
port 63091 listeners: 0
```

## Evidence
- All 468 JavaScript tests, changed-script syntax checks and bootJar passed.
- Inspected the daylight desktop capture. Groups of reeds and textured stones frame the short dock.
- The static scenery test still passes its finite geometry and 55,000-triangle budget.

## Bugs / Follow-ups
This improves the bank composition but leaves the broader actor and environment benchmark open. The sand transition is subtle at the default camera. Night, full-route and physical GPU performance comparisons remain unmeasured. Driftwood is partly obscured from the captured angle.

## Current-main integration verification
Candidate 41fbd62e06ea7b5019cfde2f0933aba2025162e6 includes main 012bb295. All 469 JavaScript tests, changed-script syntax checks and bootJar passed. Exact actuator identity was verified at http://127.0.0.1:63504 with disposable MongoDB at 127.0.0.1:63503/test. Prepared the angler using acknowledged game movement, resumed in Chrome and inspected the default-distance bank capture. Reeds and stones frame the dock; broader water, terrain and actor finish remain below the benchmark. Both listeners closed and temporary runtime directories were removed.

An earlier integration-browser invocation omitted the required cookie-file argument and exited before launching Chrome. Its runtime at ports 52181/52180 was stopped. The corrected invocation above passed against the same committed candidate.
## Party update integration
Candidate `62360467e12596e53dfa87283cbc4ae0c316efbb` includes main `9fe53463`. All 475 JavaScript tests and bootJar passed. The exact candidate at 127.0.0.1:60478 resumed the angler at the fishing bank in desktop Chrome after acknowledged movement. The daylight capture at default follow distance shows reeds and textured stones framing the dock. The sand gradient is subtle, and the water horizon has a bright horizontal seam. Broader water, landscape and actor finish remain open. The candidate and MongoDB listeners at 60478 and 60477 closed and the disposable directories were removed.


## Document Status
complete

## Project
christopherbell-dev
