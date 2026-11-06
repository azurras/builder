# Survive remote combat stance: Test Report

## Story/Issue
Show another survivor's combat state on their model in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-remote-combat-stance` at `b3362b392869749f3d24eee975cc6a1a552fcf2b`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `b3362b39`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Observer reads settled combat without another fighter pulse | ✅ PASS | Movement service test verifies target-only, engaged, guarding and disengaged states. |
| 2 | Two Chrome contexts see an armed fighter | ✅ PASS | The observer receives all stance states and the captures show the club move from back to hand. |

## Test Cases
1. Run the movement service test and pose test. Check that the rendered ready and guard geometry differ.
2. Join an armed fighter with a prepared personal encounter and join a second context as an observer. Use the combat target menu from the fighter context.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:53645 |
| Database | Disposable MongoDB at 127.0.0.1:53644/test |
| Browser | Two isolated desktop Chrome contexts with software WebGL |

## Local Run Details
- Confirmed the exact actuator build before opening Chrome.
- Closed both listeners and removed both temporary directories at teardown.

## Data Sent
```text
Fighter fixture: CRAFT_CLUB, CRAFT_AXE, HUNT
Observer: join, then walk south of camp
Fighter target menu: ENGAGE, DEFEND, DISENGAGE
```

## Response Received
```text
PASS: second Chrome context received equipped club, engagement, guard, and disengagement from a live encounter.
port 53645 listeners: 0
port 53644 listeners: 0
```

## Evidence
- All 466 JavaScript tests, changed-script syntax checks and candidate build passed.
- Movement service regression passed with the same Java sources as the committed candidate.
- Inspected observer captures before and after Engage at the same position. The club moved from the fighter's back to their hand.

## Bugs / Follow-ups
The first field setup timed out while walking the observer into place. The passing browser case used a personal encounter near camp. Shared-target facing and actual remote attack playback still require direct browser proof, and the latter is not implemented by this change.

## Document Status
complete

## Project
christopherbell-dev
