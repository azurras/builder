# Survive North Gate Patrol: Test Report

## Story/Issue
Complete the first waystation assignment in the [starting-zone plan](../implementation-plans/2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md).

## Branch
`codex/survive-waystation-assignment` at `95c6f1b538bb1e756e14fb05614e67820b174d3d`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `95c6f1b5`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Desktop keeper interaction | ✅ PASS | Chrome reached the keeper and showed assignment acceptance in chat. |
| 2 | Shared patrol and return | ✅ PASS | Two sessions accepted, used Impact on a shared bear, returned and received one reward each. |

## Test Cases
1. **Desktop keeper interaction.** Join in Chrome, walk north using keyboard events and talk to the visible keeper through Commands.
2. **Shared patrol and return.** Earn TP using existing combat, craft a club, form a party, accept both assignments, defeat the bear together and return to claim both rewards.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile on `http://127.0.0.1:51743` |
| Database | Disposable MongoDB at `127.0.0.1:51742/test` |
| Clients | Desktop Chrome with WebGL software rendering and two independent HTTP cookie sessions |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.95c6f1b538bb1e756e14fb05614e67820b174d3d`.
- **Cleanup:** Stop-Candidate confirmed both ports had zero listeners and removed its temporary Mongo and JDK socket directories.

## Data Sent
### 1. Desktop keeper interaction
```text
Join as Waystation Browser Scout.
Walk north using KeyW and open Commands within keeper range.
Choose Talk to Waystation Keeper.
```

### 2. Shared patrol and return
```text
Join Scout and Guard, build TP, craft Club and form a party.
Move to the waystation and submit TALK_WAYSTATION as both players.
Walk to ridge-bear, join the same fight, use Heavy Strike then Crushing Blow.
Return to the waystation, turn in both assignments and repeat the command.
```

## Response Received
### 1. Desktop keeper interaction
```text
PASS: desktop Chrome walked North Gate, found the keeper label, opened Commands and accepted the assignment in chat
```

### 2. Shared patrol and return
```text
PASS: two players accepted North Gate Patrol, shared one bear victory with Impact, returned to the keeper and received exactly two reward food each
port 51743 listeners: 0
port 51742 listeners: 0
```

## Evidence
- Targeted Java, Mongo mapping, JavaScript tests, syntax checks and main/test Checkstyle passed.
- Java tests covered missing and distant poses, saved progress, deferred full-inventory rewards and repeat turn-in.

## Bugs / Follow-ups
The full round trip used two HTTP sessions. The browser probe exercised movement and NPC acceptance. Physical controller and a complete two-browser round trip remain open.

## Document Status
complete

## Project
christopherbell-dev
