# Survive nearby presence payload: Test Report

## Story/Issue
Reduce movement response size for distributed players under PERF-01 in the [living parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md).

## Branch
`codex/survive-presence-visibility` at `8d559142223c2bbe44bbe98ab67272092a75c7cd`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `8d559142`.

| # | Test case | Result | Why |
|---|---|---|
| 1 | Server visibility and count boundary | ✅ PASS | Includes 64 metres, excludes farther positions, preserves global count, and uses acknowledged rather than rejected movement. |
| 2 | Compare an eight-player layout and check Chrome | ✅ PASS | The camp response dropped from 2,444 to 1,236 bytes. Chrome showed eight online and received only the nearby scout. |

## Test Cases
1. Test movement validation, expired presence and exact radius.
2. Compare one camp pulse with two players at camp and six at x=72 on each isolated build, then resume the camp observer in Chrome.

## App / Environment
| Setting | Value |
|---|---|
| Baseline | 84544d76576d18c98970c5198b0defb1446b937b at http://127.0.0.1:60240, Mongo 60239/test |
| Candidate | 8d559142223c2bbe44bbe98ab67272092a75c7cd at http://127.0.0.1:59170, Mongo 59169/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Verified actuator identity for both builds. The baseline tree matches the merged main commit 9b84b43a.
- Both isolated runtimes were stopped and all four listeners closed.

## Data Sent
```text
Join Camp Observer, Nearby Scout and Far Scouts 1–6
Acknowledge each position; move the six far scouts east in twelve six-metre steps
Read the observer movement response at camp and resume the observer in Chrome
```

## Response Received
```text
Camp pulse: 2444 bytes, 7 other poses, online count None
Camp pulse: 1236 bytes, 1 other poses, online count 8
PASS: desktop Chrome showed eight online while receiving only the nearby scout.
```

## Evidence
- Targeted Survive Java tests, all 467 JavaScript tests, changed-script syntax and the candidate build passed.
- The uncompressed response was about 49% smaller in this distributed layout. The count still includes all eight active players.

## Bugs / Follow-ups
This is one sample per build with time-varying wildlife positions, not a latency or concurrency benchmark. Dense groups still send every nearby pose. Full-route frame times, heap, database throughput and sustained multiplayer measurements remain open.

## Document Status
complete

## Project
christopherbell-dev
