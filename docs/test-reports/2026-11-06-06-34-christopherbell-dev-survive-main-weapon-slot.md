# Survive Main weapon slot: Test Report

## Story/Issue
Verify the first [inventory and equipment parity slice](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#inventory-and-equipment-parity).

## Branch
`codex/survive-main-equipment` at `616b11b76d02b60d90f01fb4604a3d20b0f54466`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `616b11b7`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Inspect, equip, remove and resume | ✅ PASS | Chrome showed the correct weapon stats and kept both weapons after reload. |

## Test Cases
1. **Inspect, equip, remove and resume.** Craft a club and axe through game commands, then use Equipment → Main and inspect Items in Chrome.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at `http://127.0.0.1:62679` |
| Database | Disposable loopback MongoDB at `127.0.0.1:62678/test` |
| Browser | Isolated desktop Chrome context |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.616b11b76d02b60d90f01fb4604a3d20b0f54466`.
- **Cleanup:** Both ports had zero listeners and temporary database, JDK, browser and cookie fixtures were removed.

## Data Sent
### 1. Inspect, equip, remove and resume
```text
Join Equipment Scout, gather four wood and two stone, craft a club and then a stone axe.
In Chrome open Equipment → Main, inspect the axe, select Equip, then Remove weapon.
Reload and inspect the two packed weapons, capacity and chat.
```

## Response Received
### 1. Inspect, equip, remove and resume
```text
PASS: desktop Chrome inspected an axe, equipped it, retained the club, removed the axe, and reloaded with both packed and counted.
port 62679 listeners: 0
port 62678 listeners: 0
```

## Evidence
- Targeted Java tests, Mongo codec tests, JavaScript tests, changed-script syntax and main/test Checkstyle passed.
- Tests covered worn durability on swap and restore, full-pack removal, invalid or stale item selection, and defaults for old saves.
- Candidate b4beb784 also passed the browser probe. The final candidate corrected the crafting description in the feature README and repeated runtime verification.

## Bugs / Follow-ups
The first pass covers Main and packed weapons. The wider item catalog, sort, armor, job requirements, storage and physical controller play remain open.

## Document Status
complete

## Project
christopherbell-dev
