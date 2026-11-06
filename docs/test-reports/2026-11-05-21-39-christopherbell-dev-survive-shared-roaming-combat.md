# Survive shared roaming combat: Test Report

## Story/Issue
Verify the shared-health milestone in the [starting-zone plan](../implementation-plans/2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md#shared-fight-handoff).

## Branch
`codex/survive-shared-health` at `db583d122eaecfeef189a1885f6d8f84694e1b52`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `db583d12`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | One shared roaming fight | ✅ PASS | Two party sessions agreed on health and defeat, and a third could see the claim without joining. |

## Test Cases
1. **One shared roaming fight.** Form a party, walk three guest sessions to the same hog and Engage it as each member. Verify the outsider claim, timed exchanges, defeat and cooldown.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Committed website JAR with test profile on `http://127.0.0.1:56360` |
| Database | Disposable loopback MongoDB at `127.0.0.1:56359/test` |
| Clients | Three independent HTTP cookie sessions |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.db583d122eaecfeef189a1885f6d8f84694e1b52`. The startup helper confirmed database `test`.
- **Cleanup:** Stop-Candidate confirmed zero listeners on both ports and removed the temporary Mongo and JDK socket directories.

## Data Sent
### 1. One shared roaming fight
```text
Three guest sessions named Scout, Guard and Observer.
POST party INVITE as Scout and ACCEPT as Guard.
POST sequenced movement pulses from camp toward meadow-hog.
POST ENGAGE meadow-hog as Scout, Observer and Guard.
Read game snapshots after the first and second strike deadlines.
POST ATTACK as Guard with the pre-defeat revision.
Read Observer's movement wildlife list during cooldown.
```

## Response Received
### 1. One shared roaming fight
```text
PASS: three independent sessions; outsider sees claim and cannot engage; shared HP 5 → 1 → 0; one defeat, one food, stale strike rejected, respawn cooldown active
port 56360 listeners: 0
port 56359 listeners: 0
```

## Evidence
- 72 targeted Java tests passed, including restored encounter health and position, old saves, Mongo mapping and night raid behavior.
- JavaScript suite, changed-file syntax checks, Checkstyle for main and tests and the candidate build passed.
- The original test failed on the unmodified build when the second member tried to Engage the claimed hog.

## Bugs / Follow-ups
The first runtime probe reached its final success message but hit Windows console encoding on the arrow characters. Repeated the same probe with UTF-8 output against a fresh test database. Candidate 7913c3e8 was superseded after the CI style check required two braces in the regression test. The probe covered the HTTP contract and timed server exchanges. Browser field appearance, physical controller, enmity, coordinated skillchains and the NPC assignment remain separate checks.

## Document Status
complete

## Project
christopherbell-dev
