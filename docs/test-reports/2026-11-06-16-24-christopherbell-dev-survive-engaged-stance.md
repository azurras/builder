# Survive engaged stance: Test Report

## Story/Issue
Make the local adventurer's readiness visible between strikes in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-engaged-stance` at `193449c24b645fbd96c78ff7237faba316324778`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `193449c2`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Armed Engage and Disengage | ✅ PASS | Desktop Chrome captures showed the club in hand after Engage and on the back after Disengage. |

## Test Cases
1. Craft a club, walk to a roaming hog in Chrome, then use Engage and Disengage through the target menu.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:55616 |
| Database | Disposable MongoDB at 127.0.0.1:55615/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Started with Start-Candidate.ps1 from the Survive worktree and verified the exact actuator build version.
- Stop-Candidate.ps1 closed both ports and removed both temporary runtime directories.

## Data Sent
- Normal gather and crafting commands prepared a club in Main and a stone axe in the pack.
- Keyboard movement approached meadow-hog, followed by Engage and Disengage through the target menu.

```text
CRAFT_CLUB, CRAFT_AXE, ENGAGE, DISENGAGE
```

## Response Received
- The equipped club remained in Main. The combat state gained a next-strike timestamp after Engage and cleared it after Disengage.
- The chat log confirmed automatic attacks stopped after Disengage.

```text
PASS: Chrome engaged a roaming hog with the club equipped and disengaged using the target menu.
port 55616 listeners: 0
port 55615 listeners: 0
```

## Evidence
- All 465 JavaScript tests passed, including the authored spear ready pose regression. Changed-script syntax checks and the candidate build passed.
- Desktop captures inspected locally at survive-ready-engaged.png and survive-ready-disengaged.png showed the club attachment in both states.

## Bugs / Follow-ups
The stance reuses the existing brace motion and covers the local adventurer. Remote action playback and further character artwork remain open. Controller and physical GPU behavior were outside this run.

## Document Status
complete

## Project
christopherbell-dev
