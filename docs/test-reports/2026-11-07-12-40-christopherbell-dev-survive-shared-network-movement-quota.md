# Survive shared-network movement quota verification

## Story/Issue
Measure PERF-01 at the browser's two-pulse-per-second cadence and isolate movement from the command quota. [Living plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md) · [Child plan](../implementation-plans/2026-11-07-12-34-christopherbell-dev-survive-movement-rate-limit.md)

## Branch
Local experiment `codex/survive-movement-rate-limit` at `e0dbaed5db9a5f1382c4cb3daf8b8237723ed20a` from `bf51abafd2514a099ce35ebfebd7f24dac378c62`.

## Pass / Fail
| Check | Result |
|---|---|
| Reproduce shared-IP throttling | PASS. Both baseline builds rejected 420 of 480 movement requests at the 20-session step. |
| Dedicated candidate quota | PASS. Three ladders accepted all 2,664 measured pulses and all 111 departures. |
| Command and leave isolation | PASS in the rate-limit filter regression with the movement bucket exhausted. |
| Release readiness | HOLD. Review identified database access and a shared service lock before owner validation. |

## Test Cases
Join 20 independent guest sessions and reuse their HTTP connections. Stage 2, 5, 10 and 20 at camp, all on one loopback IP. Alternate x between 0 and 0.15 m. Give each step two seconds of warm-up and 12 measured seconds at 2 Hz, then release the step's poses. Stop after a throttled stage to avoid carrying depleted quota into another trial. Run the candidate ladder three times.

## App / Environment
Windows, Intel i5-13600K with 20 logical processors and about 32 GiB visible RAM. Requests and MongoDB are on the same machine. Test profile and disposable MongoDB for each exact build.

| Build | App / database |
|---|---|
| Before nearby-pose filtering `48d17010` | 127.0.0.1:61411 and 127.0.0.1:61410/test |
| Main baseline `bf51abaf` | 127.0.0.1:59185 and 127.0.0.1:59184/test |
| Candidate `e0dbaed5` | 127.0.0.1:58027 and 127.0.0.1:58026/test |

## Local Run Details
Build with Invoke-Gradle and use Start-Candidate and Stop-Candidate. Check actuator identity before each workload. Use the temporary `survive-camp-load.py` harness. Read Mongo server counters around each stage and Java heap at the start and end. All measured runtimes closed both listeners. Earlier setup misread BSON counters and attempted to attach to the launcher PID. The corrected harness converts counters to numbers and selects the Java listener PID.

## Data Sent
```text
20 distinct guest joins with independent session cookies
POST /api/survive/v1/movement, sequential per survivor at 500 ms intervals
Clustered steps: 2, 5, 10, 20. Two warm-up seconds and 12 measured seconds per step.
POST /api/survive/v1/movement/leave between steps
```

## Response Received
```text
bf51abaf at 20: 60 accepted, 420 HTTP 429, 19 of 20 leave requests throttled
Candidate at 20, trial 1: 480/480, p50 8.30 ms, p95 14.64 ms, p99 18.17 ms
Candidate at 20, trial 2: 480/480, p50 8.13 ms, p95 20.22 ms, p99 27.20 ms
Candidate at 20, trial 3: 480/480, p50 5.96 ms, p95 12.41 ms, p99 14.78 ms
Candidate totals: 2,664 accepted, 0 HTTP errors, 0 rejected poses, 111 successful departures
port 58027 listeners: 0
port 58026 listeners: 0
```

## Evidence
- Baseline accepted every request at 2, 5 and 10 in the short stepped trial, with p95 6.30, 9.79 and 11.13 ms. These stages consume the same IP bucket. The 20-player result describes the stepped workload with that carryover. The p95 of the few surviving baseline requests is not a latency comparison.
- Candidate p95 ranges across three trials were 3.29–6.49 ms at 2, 5.18–8.99 ms at 5, 6.68–11.60 ms at 10 and 12.41–20.22 ms at 20. At 20 the median body was 5,196–5,205 bytes with 19 nearby poses. All offered 40 pulses per second were accepted in those windows.
- Mongo returned 560 documents per candidate 20-session step including warm-up. No documents were inserted, updated or deleted within those windows. Server-wide bytes out include monitoring and the stats client. They are not a per-request Mongo byte count.
- Candidate Java used 13.98 CPU seconds over the whole run including setup, with working set 471,474,176 bytes initially, 512,847,872 final and 522,240,000 peak. Heap used was 110,061 KiB initially and 144,050 KiB at the final sample. Two samples do not establish a leak or steady-state memory slope. Baseline CPU was not captured correctly and is excluded.
- The filter regression failed before the dedicated rule and passed with it. Targeted rate-limit tests and candidate bootJar passed. A separate full Java run was started after the workload.

## Bugs / Follow-ups
The proposed quota raises sustained admission to the public movement route from 5 to 50 per second per IP. The service enters a shared monitor and performs a Mongo version read before checking the survivor. The measured legitimate workload passes, but it does not test invalid-owner traffic or malicious contention. The candidate remains local pending an admission check that protects database and command work. Distributed IPs, mixed command load, reconnects, and the long desktop soak are still open.

## Document Status
complete

## Project
christopherbell-dev
