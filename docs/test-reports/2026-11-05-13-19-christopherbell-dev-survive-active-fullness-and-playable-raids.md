# Survive active fullness and playable raids verification

## Story/Issue
Move fullness and starvation to active play time and let survivors see and fight the nightfall raider.

## Branch
codex/survive-visible-raiders at 80dc648ce5c5f17cee82c45bdcb9cfc08485d16d.

## Pass / Fail
Pass.

## Test Cases
1. Cast a fishing line and verify it consumes no fullness.
2. Poll normally for five real minutes and confirm one fullness tick.
3. Verify restarts preserve partial time and time away does not count.
4. Join before nightfall, see a raider approach, intercept it and verify the outcome in chat.
5. Confirm commit identity and shut down the isolated runtime.

## App / Environment
Desktop and HTTP tests against disposable loopback Mongo and the exact test profile. Fullness-only runtime was http://127.0.0.1:61370/survive at e6ce284e3f2a985811c17ad5c82525b772a87f63. The combined committed candidate ran at http://127.0.0.1:54855/survive.

## Local Run Details
Built with Invoke-Gradle.ps1 bootJar, test and jsTest. Start-Candidate.ps1 and Stop-Candidate.ps1 controlled both isolated runtimes.

## Data Sent
```text
Fullness Scout joined, cast once, then requested snapshots every five seconds.
Raid Scout joined before nightfall, turned toward the approach and walked forward.
```

## Response Received
```text
Joined and after cast: fullness 10, health 10
After 301 active seconds: fullness 9, health 10
Raider visible at 00:06 and entered combat with 6 health
At 00:22 the raider was defeated and chat recorded that the raid was repelled
No browser warnings or errors
Ports 54855 and 54854 listeners 0
```

## Evidence
Combined candidate identity matched 80dc648ce5c5f17cee82c45bdcb9cfc08485d16d. Java suite recorded 2206 tests, with 126 skipped by configuration and zero failures or errors. All 455 JavaScript tests passed. Focused tests cover starvation, saved state, idle time, raid defeat after restart and unresolved raid damage. Syntax and diff checks passed.

## Bugs / Follow-ups
A night raid currently sends one raider. Shared enemy health and party combat are tracked separately. The full five-minute HTTP timer check used the fullness-only commit and the final combined candidate repeated the automated time assertions.

## Document Status
complete

## Project
christopherbell-dev
