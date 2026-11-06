# Survive two-player parties: Test Report

## Story/Issue

Verify the party-formation step in the [FFXI starting-zone plan](../implementation-plans/2026-11-05-13-15-christopherbell-dev-build-an-ffxi-inspired-starting-zone-in-survive.md).

## Branch

`codex/survive-party-invites` at `d4f15bf2b6fa76a0d2a5d414cac295bb7732a52f`.

## Pass / Fail

> [!TIP]
> **2 of 2 passed** on candidate `d4f15bf2`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Party menu and private chat | ✅ PASS | Three isolated Chrome contexts confirmed invite, accept, leave and spectator isolation. |
| 2 | Party command boundaries | ✅ PASS | Three HTTP sessions confirmed owner checks, invite identity, membership, leave and decline. |

## Test Cases

1. **Party menu and private chat.** Invite through Main Menu → Party, accept as the recipient and leave. Observe the chat log and a third player's Party window.
2. **Party command boundaries.** Use three independent guest cookies. Try accepting as an observer and as the inviter. Accept as the recipient, repeat the command, leave, invite again, try the original ID and decline the new invite.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev Survive |
| Runtime | Test profile at `http://127.0.0.1:58218` |
| Database | Disposable MongoDB bound to loopback at `127.0.0.1:58217/test` |
| Browser | Desktop Chrome headless at 1366×900 with independent browser contexts |

## Local Run Details

- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree on the branch above.
- **Identity:** Actuator returned `0.0.0-dev.d4f15bf2b6fa76a0d2a5d414cac295bb7732a52f`. Startup confirmed database `test`.
- **Cleanup:** Stop-Candidate confirmed zero listeners on both ports and removed the temporary database and JDK socket directories. The browser probe closed its Chrome process and removed its profile.

## Data Sent

### 1. Party menu and private chat

```text
Join Browser Scout, Browser Guard and Browser Observer in separate contexts.
Scout selects Browser Guard in Main Menu → Party and submits Invite.
Guard clicks Accept, then Leave party.
```

### 2. Party command boundaries

```text
POST /api/survive/v1/game for Scout, Guard and Observer
POST /api/survive/v1/party with INVITE and Guard's public survivor ID
POST ACCEPT as Observer, Scout and Guard with the invitation ID
POST duplicate ACCEPT, then LEAVE, INVITE, stale ACCEPT and DECLINE
```

## Response Received

### 1. Party menu and private chat

```text
PASS: Chrome, three isolated contexts, Party menu invite/accept/leave, private invitations and chat feedback
```

### 2. Party command boundaries

```text
PASS: 3 independent HTTP sessions, private invitation, exclusive acceptance, membership, leave, decline, stale invite rejection
Unauthorized participant and stale invitation attempts returned 409.
```

## Evidence

- 71 targeted Java tests passed, including service restart, invite expiry, CSRF and Mongo mapping. All 460 JavaScript tests and touched JavaScript syntax checks passed.
- Candidate JAR and Checkstyle passed before startup, and both probes used the same verified runtime.

## Bugs / Follow-ups

Candidate `36b429b1` failed the first Mongo-backed invite because the driver had no BSON UUID representation configured. The verified candidate stores party IDs as canonical strings, matching survivor IDs, and covers that mapping in a regression test. Candidate 3a14da91 was superseded after CI required an import style correction. Both probes passed again on d4f15bf2. Physical controller input, shared enemy health and quest rewards are still open.

## Document Status

complete

## Project

christopherbell-dev
