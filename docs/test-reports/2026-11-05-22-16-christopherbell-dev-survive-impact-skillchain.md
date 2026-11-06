# Survive Impact skillchain: Test Report

## Story/Issue
Prove the first two-player weapon skill sequence in the [starting-zone plan](../implementation-plans/2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md).

## Branch
`codex/survive-party-skillchains` at `3616ac27c5fdad21467a7dcc59282bd29ba99102`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `3616ac27`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Two players close Impact | ✅ PASS | Both earned TP using normal commands, chained the named skills and saw one bear defeat. |

## Test Cases
1. **Two players close Impact.** Charge TP through hunting, craft a club, form a party and walk to the ridge bear. Open with Heavy Strike and close with Crushing Blow.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Committed website JAR with test profile on `http://127.0.0.1:62031` |
| Database | Disposable loopback MongoDB at `127.0.0.1:62030/test` |
| Clients | Two independent HTTP cookie sessions |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.3616ac27c5fdad21467a7dcc59282bd29ba99102`. Startup confirmed database `test`.
- **Cleanup:** Stop-Candidate confirmed zero listeners on both ports and removed the temporary Mongo and JDK socket directories.

## Data Sent
### 1. Two players close Impact
```text
Join Impact Scout and Impact Guard in separate sessions.
Gather two wood. Both hunt and earn TP through defended timed strikes.
Craft Club as Guard. Invite and accept. Walk together toward ridge-bear.
Guard Engages the bear claimed by Scout.
Scout uses WEAPON_SKILL. After 1.12 seconds Guard uses WEAPON_SKILL.
```

## Response Received
### 1. Two players close Impact
```text
PASS: earned TP through normal commands; Heavy Strike opened Impact; second survivor closed with Crushing Blow for 3 bonus damage; both saw one bear defeat
port 62031 listeners: 0
port 62030 listeners: 0
```

## Evidence
- Targeted Java tests, JavaScript tests, changed-file syntax check and Checkstyle for main and test sources passed.
- The initial regression test failed without skillchain support. Candidate tests pass for the opening restored from saved state and for follow-ups at 999 milliseconds and five seconds dealing normal damage.
- The runtime probe verified the names returned by the Commands data and both chat events.

## Bugs / Follow-ups
This probe used the HTTP contract. Browser and physical controller play, additional skill properties, enmity, magic bursts and the NPC assignment remain separate checks.

## Document Status
complete

## Project
christopherbell-dev
