# Survive enemy counter motion: Test Report

## Story/Issue
Separate enemy counters from player swings in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-combat-motion` at `6f1de67ec3ceb783c246fdf196cc25355d986881`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `6f1de67e`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Guard and counter in a field fight | ✅ PASS | Chrome engaged a hog and observed both a consumed guard and a later damaging bite. |

## Test Cases
1. **Guard and counter in a field fight.** Walk to the meadow hog in Chrome, use Engage and Defend, then observe two confirmed exchanges.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile on `http://127.0.0.1:50733` |
| Database | Disposable MongoDB at `127.0.0.1:50732/test` |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.6f1de67ec3ceb783c246fdf196cc25355d986881`.
- **Cleanup:** Both ports closed and temporary runtime directories were removed.

## Data Sent
### 1. Guard and counter in a field fight
```text
Join as Motion Scout, walk toward meadow-hog and Engage through Commands.
Select the target and Defend before the first exchange.
Read confirmed HP, guard and chat on the next two exchanges.
```

## Response Received
### 1. Guard and counter in a field fight
```text
PASS: Chrome engaged a roaming hog, consumed a guard on the first exchange, and received the next bite with the confirmed damage in chat.
port 50733 listeners: 0
port 50732 listeners: 0
```

## Evidence
- All 464 JavaScript tests, changed-script syntax checks and candidate build passed.
- Motion tests verified that a player-only hit does not trigger the counter, a confirmed hit or guard does, and the pose winds back before lunging.
- Browser captures were taken after each exchange. The runtime probe verified state and chat. The pose timing itself was checked by the JavaScript tests.

## Bugs / Follow-ups
Enemy counters use confirmed snapshots. This slice does not add telegraphed attacks before server damage, player hit reactions, remote-player action playback or sound.

## Document Status
complete

## Project
christopherbell-dev
