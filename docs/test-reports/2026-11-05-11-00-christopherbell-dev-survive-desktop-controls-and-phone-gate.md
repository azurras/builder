# Survive desktop controls and phone gate verification

## Story/Issue
Support keyboard, mouse, and standard controllers on desktop and laptop. Require fullscreen and a standard controller on phones.

## Branch
codex/survive-controller-play at 31580e2d19d50a007027719a0590eab02d03033d.

## Pass / Fail
Pass for desktop browser input and simulated controller behavior. Physical phone and controller hardware were not available.

## Test Cases
1. Join and use keyboard and mouse on the committed desktop build. Shrink the viewport and confirm the desktop remains unlocked.
2. Use native fullscreen in an isolated browser fixture running the same controller module. Simulate controller connection and disconnection.
3. Test analog movement, keyboard shortcut mapping, fullscreen exit and desktop controller use without fullscreen in JavaScript.
4. Confirm candidate and fixture cleanup.

## App / Environment
http://127.0.0.1:59085/survive, exact test profile, disposable Mongo test at 127.0.0.1:59084. Standalone loopback browser fixture on port 57224.

## Local Run Details
Invoke-Gradle.ps1 built the candidate and ran jsTest. Start-Candidate.ps1 started the isolated application. Actuator matched the candidate SHA. The fixture module matched the committed source after line-ending normalization.

## Data Sent
```text
Survivor: Control Scout
Keyboard: Minus
Mouse: Map, Pine forest
Desktop viewport: 390 × 844
Fixture: Enter fullscreen, connect simulated controller, disconnect simulated controller, exit fullscreen
```

## Response Received
```text
Desktop: { fullscreen: false, gateHidden: true, locked: false, webgl: 'true', width: 390 }
{"fullscreen":true,"locked":true,"axes":[0,0,0]}
{"fullscreen":true,"locked":false,"axes":[0.5,0.7,0.4]}
{"fullscreen":true,"locked":true,"axes":[0,0,0]}
port 59085 listeners: 0
port 59084 listeners: 0
```

## Evidence
454 JavaScript tests passed, including phone detection, gate transitions and desktop controller mapping. Node syntax checks and git diff --check passed. The final browser viewport was reset. The loopback fixture was stopped and the candidate directories removed.

PR #1565 merged as eec0fb34850d6af35204c02ae920377e7769988e. Merged CI and CodeQL passed. The live build matched the merge and returned HTTP 200 for Survive and the controller module. The page included the phone gate.

## Bugs / Follow-ups
Phone browsers without fullscreen, WebGL, or a standard controller mapping cannot unlock gameplay. Hardware compatibility was not verified.

## Document Status
complete

## Project
christopherbell-dev
