## Story/Issue
Show accepted party HP and TP in the Survive viewport under UI-01.

## Branch
`codex/survive-party-vitals` at `55edfdee9f5d81881f6914378f881ba1711b1b07`.

## Pass / Fail
All local checks passed. CI and production readback are pending.

## Test Cases
1. Invite a second survivor. Confirm the pending invitation does not show a vitals row.
2. Accept and confirm both desktop clients display the ally's name, health and TP.
3. Move the ally to the meadow hog and let a combat round resolve. Confirm the observer sees both values change while the row remains inside the viewport card and separate from chat.
4. Leave the party and confirm both rows disappear. Verify old payloads without vitals clear the row in the JavaScript regression test.

## App / Environment
Two isolated desktop Chrome contexts with software WebGL. Candidate at 127.0.0.1:56618 and disposable MongoDB on 127.0.0.1:56617/test.

## Local Run Details
Verified the actuator build identity before browser launch. The exact candidate passed the Survive Java tests, Checkstyle main and test, the JavaScript suite and bootJar. The initial feature commit 64da7166 passed the full Java suite and 474 JavaScript tests.

## Data Sent
```text
Invite, accept, travel to the meadow hog, engage and observe a combat round, then leave.
```

## Response Received
```text
PASS: ally vitals updated to HP 9/10 and TP 50
PASS: invitation hid vitals, acceptance showed both partners, and leave cleared both rows.
port 56618 listeners: 0
port 56617 listeners: 0
```

## Evidence
Native check logs and the two-browser proof are in the local temporary directory. The confirmation run removed its disposable database and JDK socket directories. A prior run on the initial feature commit timed out during browser travel. The corrected harness emulates desktop focus and confirms the movement view before driving.

## Bugs / Follow-ups
Larger parties and MP remain part of the living parity plan. The candidate uses the existing status poll and changes no public presence or saved data.

## Document Status
complete

## Project
christopherbell-dev
