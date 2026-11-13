## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Let both players choose an item and confirm revised trade terms under ECON-01.

## Branch
codex/survive-trade-counteroffers at 0d31c0cc25908c863bccaf6f99a719e226f3d52e.

## Pass / Fail
Survive Java tests, Mongo codec, 481 JavaScript tests, Checkstyle, bootJar and two-player Chrome verification passed.

## Test Cases
Counter a weapon-for-supply offer with another weapon. Attempt to accept the superseded offer in the service test. Confirm the revised terms and compare both weapon IDs.

## App / Environment
Two Chrome contexts at 127.0.0.1:64482 with disposable MongoDB at 127.0.0.1:64481/test.

## Local Run Details
Actuator matched the commit. The starting packs were seeded in the disposable database.

## Data Sent
```text
Offer the club with three uses left for one stone. Counter with the club with two uses left. Accept the revised offer.
```

## Response Received
```text
PASS: both players reviewed revised terms and exchanged their exact weapons only after acceptance.
```

## Evidence
The original offer ID returned 404 after being replaced. Chrome showed both original packs before acceptance and both exact weapon IDs after it.

## Bugs / Follow-ups
Each side can contribute one supply stack or one weapon. Multi-item offers remain open.
