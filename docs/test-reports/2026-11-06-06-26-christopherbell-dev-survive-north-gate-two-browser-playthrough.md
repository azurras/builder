# Survive North Gate two-browser playthrough: Test Report

## Story/Issue
Exercise the complete desktop outing in the [starting-zone plan](../implementation-plans/2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md).

## Branch
`codex/survive-two-browser-playtest` at `1b5de80cafad03cb1ec33de06af1ac9e766d1608`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `1b5de80c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Two-browser North Gate Patrol | ✅ PASS | Both browser contexts formed a party, accepted the patrol, completed Impact and turned in their assignments through the game UI. |

## Test Cases
1. **Two-browser North Gate Patrol.** Resume two independently prepared survivors in Chrome. Use the Party menu, walk to the keeper with keyboard input, accept the patrol, walk to the bear, Engage, execute both weapon skills and return to the keeper.

## App / Environment
| Setting | Value |
|---|---|
| App | Survive from merged website main |
| Runtime | Test profile at `http://127.0.0.1:53515` |
| Database | Disposable loopback MongoDB at `127.0.0.1:53514/test` |
| Clients | Two isolated desktop Chrome contexts with software WebGL |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.1b5de80cafad03cb1ec33de06af1ac9e766d1608`.
- **Cleanup:** Both runtime ports had zero listeners after Stop-Candidate. The disposable database, JDK socket directory, Chrome profile and temporary session fixture were removed.

## Data Sent
### 1. Two-browser North Gate Patrol
```text
Prepare two guests through normal hunt and craft requests. Each earns at least 100 TP and one equips a club.
Resume each guest in its own Chrome context.
Submit Invite from Party and accept in the second context.
Use WASD to reach the keeper, then Talk from Commands in both contexts.
Walk to ridge-bear, select it and join the shared fight.
Use Heavy Strike and then Crushing Blow from the respective Commands menus.
Return to the keeper, turn in both assignments and check the reward lines in chat.
```

## Response Received
### 1. Two-browser North Gate Patrol
```text
PASS: two isolated desktop Chrome contexts formed a party, accepted North Gate Patrol, completed Impact and turned in both assignments through the game UI
port 53515 listeners: 0
port 53514 listeners: 0
```

## Evidence
- Both clients observed ACTIVE, then RETURN, then COMPLETE in their game snapshots.
- The opener and closer appeared in chat. Both clients displayed the patrol reward.
- The harness observed game responses and drove keyboard events and existing controls. It prepared TP and equipment through normal HTTP commands before the browser outing.

## Bugs / Follow-ups
The first harness needed page observation enabled and had assumed a fixed player would draw the bear's aggro. The passing run allowed either player to draw aggro. Physical controller input remains open. Windows reported an Xbox controller device entry, and all four XInput slots returned device disconnected during this check.

## Document Status
complete

## Project
christopherbell-dev
