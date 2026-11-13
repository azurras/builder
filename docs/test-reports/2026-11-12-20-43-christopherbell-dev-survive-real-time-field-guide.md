## Story/Issue
Align the in-game Guide and fullness warning with real-time Survive.

## Branch
`codex/survive-current-field-guide` at `0223ef9a859ebe6c3ca94468bc11637abb8f7b9e`.

## Pass / Fail
JavaScript and desktop browser checks passed.

## Test Cases
Verify the guide describes timed fishing, five-minute fullness, Equipment swaps and Engage. Open Guide through Main Menu.

## App / Environment
Isolated desktop Chrome candidate at 127.0.0.1:49639 and MongoDB at 127.0.0.1:49638/test.

## Local Run Details
Actuator matched the candidate. All 480 JavaScript tests and bootJar passed.

## Data Sent
```text
Open Main Menu and select Guide.
```

## Response Received
```text
PASS: opened Guide from Main Menu and saw timed fishing instructions.
port 49639 listeners: 0
port 49638 listeners: 0
```

## Evidence
The template regression covers the updated instructions. Chrome verified visible timed-fishing text. Both disposable directories were removed.

## Bugs / Follow-ups
This changes instructions. Gameplay and parity work continue in the living plan.

## Shared positioning baseline
Candidate `341bfc34821bd9d36741e4c9c4ff5648ae56ac7e` includes main `9a36420f`. All 482 JavaScript tests and bootJar passed. Desktop Chrome verified the Guide panel and timed fishing text on the exact build at 127.0.0.1:57058. Application and MongoDB listeners at 57058 and 57057 closed and disposable directories were removed.


## Document Status
complete

## Project
christopherbell-dev
