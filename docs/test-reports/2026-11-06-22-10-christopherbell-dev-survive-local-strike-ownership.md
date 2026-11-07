# Survive local strike ownership: Test Report

## Story/Issue
Prevent an ally's damage from triggering a local swing under ART-03 and COM-02 in the [parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md).

## Branch
`codex/survive-local-strike-cues` at `222271f09d9734c1960359d8509b2364c8cfd441`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `222271f0`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Attribute local animation to the attacker's cue | ✅ PASS | The mounted world test leaves the local pose unchanged on ally damage and animates the owner's confirmed skill. |
| 2 | Deliver the same strike to owner and observer | ✅ PASS | Two Chrome contexts observed the same automatic club strike revision and expiry. |

## Test Cases
1. Verify snapshot cue ownership and expiry in the movement service and exercise the mounted browser world.
2. Join an armed fighter and separate observer, Engage and compare the committed cue sent to each browser.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:61564 |
| Database | Disposable MongoDB at 127.0.0.1:61563/test |
| Browser | Two isolated desktop Chrome contexts with software WebGL |

## Local Run Details
- Verified exact actuator build before opening Chrome.
- Closed both listeners and removed both temporary runtime directories.

## Data Sent
```text
Prepare a club and personal encounter through game commands
Join the fighter and observer, then ENGAGE
Compare owner snapshot strike and observer appearance strike
```

## Response Received
```text
PASS: Owner and observer received the same club strike revision 19 and the cue expired.
port 61564 listeners: 0
port 61563 listeners: 0
```

## Evidence
- Targeted Survive Java and codec tests, all 470 JavaScript tests, syntax checks and bootJar passed.
- The owner snapshot uses the same committed recent strike record as observer presence.
- Missing cue fields retain the older browser fallback during a mixed-version rollout.

## Bugs / Follow-ups
The ally-hit regression is covered through the mounted-world test. The live browser check covers cue ownership in a personal encounter. A shared-party visual capture and broader motion review remain open.

## Document Status
complete

## Project
christopherbell-dev
