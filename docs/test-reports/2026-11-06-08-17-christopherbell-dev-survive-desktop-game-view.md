# Survive desktop game view: Test Report

## Story/Issue
Remove the site framing from active desktop play as part of the [desktop art and animation review](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-desktop-game-view` at `db8c996964deb1bd5c44f584942d552d7d605500`.

## Pass / Fail
> [!TIP]
> **1 of 1 passed** on candidate `db8c9969`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Desktop play and page view | ✅ PASS | The canvas filled the available height, the toggle restored the site, and the same survivor walked to the keeper. |

## Test Cases
1. **Desktop play and page view.** Join a survivor in Chrome, compare the viewport and canvas heights, toggle page view twice, walk to the keeper and open the replacement join form.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at `http://127.0.0.1:64356` |
| Database | Disposable loopback MongoDB at `127.0.0.1:64355/test` |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile`.
- **Working directory:** Survive 3D worktree.
- **Identity:** Actuator returned `0.0.0-dev.db8c996964deb1bd5c44f584942d552d7d605500`.
- **Cleanup:** Stop-Candidate confirmed both ports had zero listeners and removed its temporary Mongo and JDK socket directories.

## Data Sent
### 1. Desktop play and page view
```text
Join Desktop View Scout.
Measure the window and the game canvas.
Use Main Menu → Show page view and Fill browser window.
Walk north with KeyW until Talk to Waystation Keeper is available.
Open the replacement join form.
```

## Response Received
### 1. Desktop play and page view
```text
Game canvas height: 759.015625 Browser height: 805
PASS: browser-filling game, page view toggle, movement to the keeper, and replacement join form in page view
port 64356 listeners: 0
port 64355 listeners: 0
```

## Evidence
- JavaScript suite, script syntax check and committed build passed.
- Captured the baseline and candidate at the camp and waystation. The candidate keeps the chat, vitals and existing menus inside the active viewport.

## Bugs / Follow-ups
The change addresses website framing. Avatar proportions, the keeper silhouette, terrain and building finish remain open in the parity plan. The browser probe did not measure frame time or exercise a physical controller.

## Document Status
complete

## Project
christopherbell-dev
