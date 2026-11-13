## Story/Issue
Allow players to discard carried items and expand their packs at camp under ECON-01.

## Branch
`codex/survive-pack-management` at `d554c9ca78505b9a80f06b0f4c0d03cd07a0a261`.

## Pass / Fail
Targeted Java, Mongo codec, JavaScript, Checkstyle, bootJar and the desktop upgrade and cancel checks passed.

## Test Cases
Upgrade a pack, discard a supply, reject an unowned item and stale revision, and restore the upgraded pack from storage. Open Items in Chrome, cancel a discard, then expand the pack.

## App / Environment
Isolated desktop Chrome candidate at 127.0.0.1:50763 with disposable MongoDB at 127.0.0.1:50762/test.

## Local Run Details
Actuator matched the committed build. Both listeners closed and disposable directories were removed.

## Data Sent
```text
Open Items, select wood, request a drop, cancel, then buy the first expansion.
```

## Response Received
```text
PASS: Items opened the discard confirmation, Cancel preserved supplies, and Expand pack raised capacity to 15.
```

## Evidence
Service and save tests verified a committed supply discard and restart persistence. The browser verified cancel and upgrade. The initial Checkstyle run flagged missing braces, corrected before the final passing run.

## Bugs / Follow-ups
The browser did not confirm a permanent discard. Player trade is a separate deliverable. Production release is pending.

## Document Status
complete

## Project
christopherbell-dev
