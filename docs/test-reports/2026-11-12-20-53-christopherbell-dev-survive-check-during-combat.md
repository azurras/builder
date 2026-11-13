## Story/Issue
Keep Check available on the selected target while automatic attacks are active.

## Branch
`codex/survive-combat-check` at `11e0e84a9bf7196aa029a9bbb551421e2dc46ed6`.

## Pass / Fail
JavaScript regression and desktop Chrome passed.

## Test Cases
Check a selected target during Engage. Verify the result appears in chat and automatic attacks stay active.

## App / Environment
Isolated desktop Chrome candidate 127.0.0.1:50516 and MongoDB 127.0.0.1:50514/test.

## Local Run Details
Verified exact actuator identity, syntax, all 481 JavaScript tests and bootJar. The command-list regression failed before the fix and passed afterward.

## Data Sent
```text
Walk to the hog, Engage, select the enemy marker, and choose Check.
```

## Response Received
```text
PASS: Check reported the hog in chat during active automatic attacks.
port 50516 listeners: 0
port 50514 listeners: 0
```

## Evidence
Desktop Chrome checked the chat output and confirmed the active strike deadline. The runtime removed both disposable directories.

## Bugs / Follow-ups
Production rollout remains pending.

## Document Status
complete

## Project
christopherbell-dev
