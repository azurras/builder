# Survive remote strike playback: Test Report

## Story/Issue
Animate committed attacks for other survivors in the [desktop parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md#desktop-art-and-animation-review).

## Branch
`codex/survive-remote-strikes` at `a5de769977508397d76515abae58b8c961ecbdc4`, based on remote combat stance candidate b3362b39.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `a5de7699`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Committed strikes and expiry | ✅ PASS | An observer gets the saved strike, expired cues are hidden, and the client ignores repeated revisions. |
| 2 | Render another player's automatic strike | ✅ PASS | Chrome captures show the observer's view at ready, mid-swing and recovered. |

## Test Cases
1. Verify cue expiry during world settlement, saved-world round trip, old saves, and client deduplication.
2. Join an armed fighter and a separate observer in Chrome. Engage a personal encounter, then capture the observer's canvas during a confirmed automatic strike.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:57586 |
| Database | Disposable MongoDB at 127.0.0.1:57585/test |
| Browser | Two isolated desktop Chrome contexts with software WebGL |

## Local Run Details
- Confirmed the exact actuator build before opening Chrome.
- Both ports closed and both temporary directories were removed.
- An earlier screenshot caught the recovered stance. The successful attempt captured directly after the WebGL actor draw during the cue.

## Data Sent
```text
Fighter fixture: CRAFT_CLUB, CRAFT_AXE, HUNT
Observer: join, then walk southwest of camp
Fighter target menu: ENGAGE
Wait for the committed automatic club strike in the observer's movement response
```

## Response Received
```text
PASS: Chrome observer received automatic club strike revision 16 and the cue expired.
port 57586 listeners: 0
port 57585 listeners: 0
```

## Evidence
- Targeted Survive Java tests, Mongo saved-world tests, all 467 JavaScript tests, changed-script syntax checks and candidate build passed.
- The observer capture shows the fighter turning their body and extending the club during the strike. The ready and recovered captures show the standing stance.

## Bugs / Follow-ups
Browser proof covers an automatic club strike in a personal encounter. Shared-fight playback, weapon skills, kill and weapon-break rendering, and reduced-motion behavior still need direct browser checks. The cue keeps only the latest confirmed strike per fighter, so a slow observer can miss an older strike.

## Document Status
complete

## Project
christopherbell-dev
