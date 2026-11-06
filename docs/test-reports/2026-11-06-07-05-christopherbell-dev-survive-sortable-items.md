# Survive sortable Items: Test Report

## Story/Issue
Verify the item selection and use flow in the [inventory and equipment plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#inventory-and-equipment-parity).

## Branch
`codex/survive-sortable-items` at `578ed55ae3e736ff7f7ebd996677a38431157856`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `578ed55a`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Inspect, sort, refresh and use | ✅ PASS | Chrome retained the selected food and list focus, then consumed one item and showed the confirmed result. |

## Test Cases
1. **Inspect, sort, refresh and use.** Prepare a survivor with food, wood and missing health. In Chrome inspect Food, sort the list, refresh with the list focused, then choose Use Food.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile on `http://127.0.0.1:56007` |
| Database | Disposable MongoDB at `127.0.0.1:56006/test` |
| Browser | Isolated desktop Chrome context |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.578ed55ae3e736ff7f7ebd996677a38431157856`.
- **Cleanup:** Both ports had zero listeners. The temporary database, JDK socket directory, browser profile and cookie fixture were removed.

## Data Sent
### 1. Inspect, sort, refresh and use
```text
Prepare Inventory Scout with carried food and wood using normal game commands.
Open Items, select Food and inspect its description.
Switch to name sort, focus the list, then refresh the world.
Choose Use Food and read the confirmed game state and chat.
```

## Response Received
### 1. Inspect, sort, refresh and use
```text
PASS: desktop Chrome inspected food, sorted Items, preserved selection and focus through refresh, used one food, and saw health and fullness recover in the confirmed state.
port 56007 listeners: 0
port 56006 listeners: 0
```

## Evidence
- JavaScript suite, syntax checks and candidate build passed.
- The Items regression test checks name order, quantity changes, retained selection and one Eat request.

## Bugs / Follow-ups
Physical controller input remains open. The current list covers food, wood, stone and packed weapons.

## Document Status
complete

## Project
christopherbell-dev
