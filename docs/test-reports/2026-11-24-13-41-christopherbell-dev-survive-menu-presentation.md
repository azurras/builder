## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Make the active menu window, the selected item and its commands visible during play.

## Branch
codex/survive-command-windows at db716cd7bcffb0466b7647bb76eb93e64b7a6352.

## Pass / Fail
Passed JavaScript syntax checks, all 481 JavaScript tests, application build and desktop Chrome playthrough.

## Test Cases
Inspect two wood in Items, confirm the stack, open its Drop command and cancel. Verify the pack count, focus on return, the Map heading and the Back control.

## App / Environment
Windows desktop Chrome at 1366 × 900, http://127.0.0.1:61090/survive, disposable loopback MongoDB.

## Local Run Details
Confirmed build identity before play. A guest gathered wood and stone using game actions. The playthrough exercised keyboard, scripted button clicks and a simulated standard controller. Both local listeners closed after testing.

## Data Sent
```text
Open Items. Highlight Wood. Confirm. Choose Drop one. Escape. Escape. Escape.
Reopen Main Menu with X. Use the D-pad and A to open Map. Choose Back.
```

## Response Received
```text
Wood ×2 and Stone ×2 occupied 4 / 10 slots. Confirm moved focus to Drop one.
The prompt initially focused Cancel. Escape restored Drop one and kept the pack count.
A second Escape restored the list. Map Back restored the Map category cursor.
```

## Evidence
The screenshot shows the Items heading, selected wood, stack description and highlighted Drop command in one window next to the open category list.

## Bugs / Follow-ups
Physical controller feel and narrow-screen review remain open.
