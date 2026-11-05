# Survive movement database read verification

## Story/Issue
Reduce server work on movement pulses while preserving capacity, progress and version checks.

## Branch
codex/survive-version-checked-pulses at a98109f1aa287751e5cd1edea293e199d50e41b3.

## Pass / Fail
Pass.

## Test Cases
1. Reuse the saved snapshot across 100 unchanged pulses.
2. Reload after a newer version and clear the snapshot after deletion.
3. Confirm the candidate uses the Mongo document ID index for movement reads.

## App / Environment
http://127.0.0.1:62980/survive with test profile and disposable Mongo at 127.0.0.1:62979/test.

## Local Run Details
Built using Invoke-Gradle.ps1 --no-daemon. Used Start-Candidate.ps1 and Stop-Candidate.ps1. Actuator matched the candidate.

## Data Sent
```text
POST /api/survive/v1/game as Pulse Scout
100 authenticated movement pulses with increasing sequences
```

## Response Received
```text
100 accepted pulses
100 IXSCAN { _id: 1 } version checks
0 full world reads during movement
13700 Mongo response bytes
Ports 62980 and 62979 listeners 0
```

## Evidence
Survive and Mongo adapter tests passed, along with Checkstyle and git diff --check. The Mongo profiler confirmed exact indexed queries and no full document responses during the steady-state loop.

## Bugs / Follow-ups
Production heap, latency and busy multiplayer load have not been benchmarked.

## Document Status
complete

## Project
christopherbell-dev
