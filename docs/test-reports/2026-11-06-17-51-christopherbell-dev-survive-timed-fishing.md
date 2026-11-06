# Survive timed fishing: Test Report

## Story/Issue
Implement the timed cast, bite and reel in the [first economy loop](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#first-gathering-fishing-and-trade-loop).

## Branch
`codex/survive-timed-fishing` at `cb05119bb93c781d95d8bc5a329d1d819a239aca`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `cb05119b`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Server deadline and ownership of rewards | ✅ PASS | Early reel rejected, timely reel awards once, stale repeat fails, expiry and leaving the bank clear the cast. |
| 2 | Show the bite and allow reel or expiry in Chrome | ✅ PASS | The projected cue appears by the line, Reel In takes focus, and a second cast settles without a catch after the player waits. |

## Test Cases
1. Verify the fishing service, saved-world round trip, compatibility and browser timing helpers.
2. Travel to the bank by acknowledged movement, cast through Chrome, confirm focused Reel In during the bite, reel, then let a second bite expire.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:55866 |
| Database | Disposable MongoDB at 127.0.0.1:55865/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Verified exact actuator build before the Chrome run.
- Teardown closed both listeners and removed both temporary directories.

## Data Sent
```text
Movement from camp to (-11, 66) in acknowledged steps
Commands: Cast line, wait for Bite! Reel in, Reel in
Second Cast line, let the bite deadline pass
```

## Response Received
```text
Reached the fishing bank using acknowledged movement.
PASS: Chrome showed a projected bite cue, accepted a timely reel, and settled an untouched cast as escaped.
port 55866 listeners: 0
port 55865 listeners: 0
```

## Evidence
- Targeted Survive Java and saved-world codec tests, 468 JavaScript tests, changed-script syntax checks and bootJar passed.
- Inspected the desktop bite capture. The rod and line are visible, with the cue offset from the avatar and focus on Reel In.
- The browser check accepts either a successful catch or the game’s existing chance-based miss. The deterministic Java test establishes the one-food award.

## Bugs / Follow-ups
The island cast uses a two-second wait, a five-second reel window and the existing 60% catch chance. Named fish, gear, bait, skill progression, cooking and trade remain open. Controller hardware, reduced motion and full-route performance were outside the browser run.

## Document Status
complete

## Project
christopherbell-dev
