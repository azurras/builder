## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Allow a packed weapon to be offered for supplies under ECON-01.

## Branch
codex/survive-trade-weapons at 42f62a786b352c8275b57a9586356c858b66688c.

## Pass / Fail
Passed Survive and Mongo codec tests, 481 JavaScript tests, Checkstyle, bootJar, and the exact-candidate Chrome trade.

## Test Cases
Review a weapon's condition, accept the exchange, and verify its identity and durability. Reject acceptance after the sender equips the offered copy.

## App / Environment
Two Chrome browser contexts against 127.0.0.1:50514 with disposable MongoDB at 127.0.0.1:50513/test.

## Local Run Details
Actuator matched the commit. The starting inventory was seeded in the disposable test database.

## Data Sent
```text
Offer a packed club with three uses left for one stone and accept as the recipient.
```

## Response Received
```text
PASS: reviewed a packed weapon, transferred the exact copy with three uses left, and recorded the result in chat.
```

## Evidence
The receiver got the original copy ID and condition. Service tests preserved the recipient's stone when the sender equipped the offered copy.

## Bugs / Follow-ups
Requesting another player's weapon, weapon-for-weapon trades, and multi-item offers remain open.
