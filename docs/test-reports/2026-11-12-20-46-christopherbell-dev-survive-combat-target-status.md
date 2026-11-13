## Story/Issue
Distinguish automatic attack state in the Survive enemy panel.

## Branch
`codex/survive-combat-target-status` at `eb44d965eb1fc86b6a4faa7222590a31986b7476`.

## Pass / Fail
JavaScript and desktop browser checks passed.

## Test Cases
Engage a hog, disengage, then confirm the enemy name and HP remain visible.

## App / Environment
Desktop Chrome and isolated candidate at 127.0.0.1:62339, MongoDB at 127.0.0.1:62338/test.

## Local Run Details
Actuator matched the committed candidate. JavaScript suite and bootJar passed.

## Data Sent
```text
Select roaming hog, Engage, then Disengage.
```

## Response Received
```text
PASS: Engage showed In combat, Disengage showed Ready to engage, and the hog HP remained visible.
port 62339 listeners: 0
port 62338 listeners: 0
```

## Evidence
The unit test reproduces the old nearby label after Disengage. The desktop run verified the visible state with normal combat commands. Disposable runtime directories were removed.

## Bugs / Follow-ups
Production deployment remains open.

## Document Status
complete

## Project
christopherbell-dev
