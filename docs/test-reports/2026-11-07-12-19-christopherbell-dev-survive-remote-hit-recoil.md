# Survive remote hit recoil: Test Report

## Story/Issue
Show nearby adventurers reacting to confirmed combat damage under ART-03 in the [parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md). [Implementation plan](../implementation-plans/2026-11-06-22-27-christopherbell-dev-survive-remote-hit-recoil.md).

## Branch
`codex/survive-remote-hit-recoil` at `6cebcc6ba3f7cde52e7ba8f99b3415e71e4122b8`, including live main `125bd326`.

## Pass / Fail
| # | Test case | Result | Evidence |
|---|---|---|---|
| 1 | Observe committed combat health without another fighter movement pulse | PASS | Java movement service test saw 9 HP after the first hog exchange. |
| 2 | Trigger one reaction per observed loss and tolerate old responses | PASS | Mounted world kept the receipt time on a repeat. Pose tests reject missing, invalid, healing, first-seen and noncombat values. |
| 3 | Draw a remote fighter after damage | PASS | Normal desktop Chrome captured the remote fighter at 400 ms after the observed decrease. |
| 4 | Draw the same exchange in reduced motion | PASS | Separate Chrome run confirmed the preference, received damage and captured the stationary combat stance at 391 ms. |

## Test Cases
1. Join a fighter and observer; advance the authoritative clock through one attack and verify the observer's appearance.
2. Feed consecutive movement responses to the mounted world; compare receipt times and test bounded recoil.
3. Resume the armed fighter and join an independent Chrome observer. Walk the observer south of camp. Engage the prepared personal encounter from the target menu. Capture the remote adventurer after the observer receives lower health.
4. Repeat in a fresh runtime with the observer's reduced-motion preference set before navigation.

## App / Environment
| Setting | Value |
|---|---|
| Normal runtime | http://127.0.0.1:64986; MongoDB 127.0.0.1:64985/test |
| Reduced-motion runtime | http://127.0.0.1:59326; MongoDB 127.0.0.1:59325/test |
| Browser | Desktop Chrome with software WebGL, two independent contexts per run |

## Local Run Details
- Verified exact actuator identity `0.0.0-dev.6cebcc6ba3f7cde52e7ba8f99b3415e71e4122b8` before opening each browser.
- Game commands prepared the weapon and encounter; a read-only browser hook recorded movement responses and captured the rendered frame.
- Both test databases, both candidate listeners, and temporary runtime directories were cleaned up.

## Data Sent
```text
Join Fighter and Observer; prepare the Fighter's club and encounter
Select the enemy and ENGAGE in the Fighter browser
Observe consecutive nearby movement appearances in the separate browser
Repeat with prefers-reduced-motion: reduce for the observer
```

## Response Received
```text
PASS: normal observer saw confirmed health 10 to 9 and captured the fighter at 400 ms.
PASS: reduced observer saw confirmed health 9 to 8 and captured the fighter at 391 ms.
port 64986 listeners: 0
port 64985 listeners: 0
port 59326 listeners: 0
port 59325 listeners: 0
```

## Evidence
- First Java and JS contract checks failed on the missing health field and missing pose functions. With the functions present but the reconciliation assignment removed, the mounted world test failed because the damage update never reached the renderer. All passed after restoring the implementation.
- Full Java suite and bootJar passed on initial commit `073a1f780127abc88f65b98e575fe19ec91abd92`. Targeted Survive and Mongo codec tests, 472 JavaScript tests and bootJar passed on the integrated candidate. Changed JS syntax passed.
- Inspected `survive-remote-hit-normal.png` and `survive-remote-hit-reduced.png` in the local temporary evidence directory. The normal view shows the remote adventurer in motion at contact; the reduced-motion view retains the ready stance. The normal frame includes the outgoing swing as well as the recoil. The pose tests separately verify torso movement with grounded feet.
- Earlier browser attempts failed on harness timing and assumed fixed HP. The corrected check samples frame time before PNG encoding and reads starting HP from the observer before Engage. No candidate code changed for the reruns.
- The requested independent review did not run because the reviewer hit its usage limit. Reviewed the final diff and compatibility boundaries directly.

## Bugs / Follow-ups
The observer test uses a personal encounter. Shared-party exchanges, enemy playback and player collapse still need direct coverage. Multiple losses between movement responses can coalesce; an offsetting heal can hide a loss. No sustained browser or server performance claim is made. The desktop frames still show weak facial definition and identical player silhouettes.

## Shared North Gate Patrol on current main
Candidate `210f4d3a53bd39f4592d1c7d95863000f9f9e838` includes main `e5d948e2`, timed fishing and enemy defeat motion. Targeted Survive and Mongo codec tests, 475 JavaScript tests and bootJar passed. Exact build verified at 127.0.0.1:53950 with MongoDB 127.0.0.1:53949/test.

Two desktop Chrome contexts accepted an invite and North Gate Patrol, entered the same roaming bear encounter, and received each other's Heavy Strike and Crushing Blow cues. An observer saw the ally's combat health decrease from 9 to 6 in consecutive movement responses. Both players received patrol credit and turned in their assignments through the game UI. Both listeners closed and temporary runtime directories were removed.

This run verifies the shared-fight input to the recoil renderer and the full patrol loop. The earlier personal-encounter frames remain the evidence for the normal and reduced-motion poses. The shared run did not capture the recoil frame or require an actual Impact bonus when the closing strike was lethal.
## Confirmed strike integration
Candidate `2eddf372d7c140b7f1fdaacd0b6727746861dc8e` integrates main `cec581eb` and retains the tests for both nearby recoil and confirmed local strike ownership. Survive Java tests, Checkstyle main and test, 476 JavaScript tests and bootJar passed. Two desktop Chrome sessions with exact actuator identity at 127.0.0.1:57253 repeated North Gate Patrol, received each other's weapon-skill cues, saw confirmed ally HP fall from 4 to 1 and turned in both quests. The image captured 324 ms after damage did not show the fighters clearly, so it does not verify shared-fight pose readability. Earlier personal-fight frames and the mounted tests remain the visual evidence. Candidate and MongoDB listeners at 57253 and 57252 closed and both disposable runtime directories were removed.


## Document Status
complete

## Project
christopherbell-dev
