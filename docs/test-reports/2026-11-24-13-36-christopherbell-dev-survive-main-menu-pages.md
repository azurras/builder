## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Align the island Main Menu with the two-page controls in the FFXI Windows manual, printed page 24.

## Branch
codex/survive-command-windows at 14298481a43b6af12d9400e49def9116cf8d2c6d.

## Pass / Fail
Passed 481 JavaScript tests, the application build and the desktop browser playthrough.

## Test Cases
Open Main Menu, select Party, turn to Map and enter it. Back out, return to the first page, open Items and cancel twice. Reopen with controller X and repeat Map navigation using the D-pad, A and B.

## App / Environment
Chrome at 1366 × 900 on Windows against http://127.0.0.1:57941/survive with an isolated test MongoDB.

## Local Run Details
The running application's build identity matched the commit. A guest entered the game through its normal join endpoint. Chrome received keyboard events and a simulated standard gamepad. Both listeners closed after the check.

## Data Sent
```text
Minus, Down, Right, Enter, Escape, Left, Down, Enter, Escape, Escape.
Controller X, Right, A, B, B.
```

## Response Received
```text
Map opened on page two. Cancel restored the Map row. Returning to page one restored Party.
Choosing Items focused the carried-item list. Cancel returned to Items, then to the island.
Controller X restored Items. Right restored Map. A opened it. B returned one level per press.
```

## Evidence
The browser verified actual focus and open panels. The first browser run found an Enter activation problem and the final build passed the same sequence.

## Bugs / Follow-ups
Physical controller play, active-window cycling across the chat log and battle commands, and menu coverage for future jobs and spells remain open.
