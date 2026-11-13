## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Require verified proximity for direct island trades under ECON-01.

## Branch
codex/survive-nearby-trade at 9252b941b61d254e2795456bb2dddf29d485956d.

## Pass / Fail
Passed affected Survive Java tests, Checkstyle, bootJar and a two-player HTTP playthrough against the committed build.

## Test Cases
Offer at the same point, walk apart, attempt acceptance, move back within range and accept.

## App / Environment
Candidate at 127.0.0.1:57180 with disposable MongoDB at 127.0.0.1:57179/test.

## Local Run Details
Actuator matched the commit. Starting supplies were seeded in the disposable database. Both listeners closed and temporary directories were removed.

## Data Sent
```text
Offer one wood for one stone. Move the recipient to x=6 and accept, then move to x=5 and retry.
```

## Response Received
```text
PASS: acceptance at six metres preserved both inventories; acceptance at five metres moved both stacks.
```

## Evidence
The service regression also rejects a spatial offer when the other player has no verified pose.

## Bugs / Follow-ups
The proximity boundary was verified through HTTP. The recipient chooser still lists active survivors outside trading range.
