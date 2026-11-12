## Story/Issue
Browse the carried item list with the controller D-pad under UI-01.

## Branch
`codex/survive-item-controller` at `fe481a3315fc2816eeff084ed447e2e093f402b9`.

## Pass / Fail
Local regression and desktop Chrome simulation passed. Physical controller remains open.

## Test Cases
Press D-pad Down while the item list has focus. Verify selection, description and focus. At the last item, verify another Down moves to the next menu control.

## App / Environment
Desktop Chrome and isolated candidate 127.0.0.1:63965 with MongoDB 127.0.0.1:63964/test.

## Local Run Details
Actuator matched the candidate. JavaScript syntax, 477 JavaScript tests and bootJar passed. The controller regression failed before implementation and passed afterward.

## Data Sent
```text
Prepare wood and a packed stone axe. Open Items, focus the first item, and simulate D-pad Down.
```

## Response Received
```text
PASS: D-pad Down selected the next item and updated its details with the list still focused.
port 63965 listeners: 0
port 63964 listeners: 0
```

## Evidence
The confirmation browser verified two options before sending the gamepad input. The first attempt timed out with a fixture that did not guarantee two options.

## Bugs / Follow-ups
Physical controller testing and the broader Items and Equipment workflows remain open.

## Document Status
complete

## Project
christopherbell-dev
