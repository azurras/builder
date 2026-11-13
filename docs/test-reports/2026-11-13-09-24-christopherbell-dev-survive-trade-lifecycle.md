## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Release pending trade slots on expiry or character replacement under ECON-01.

## Branch
codex/survive-trade-lifecycle at 83b0ae61f8714d99fe14fd49675d5f81cc3f9ed2, based on PR #1614.

## Pass / Fail
Passed affected Survive Java tests, Mongo codec, 481 JavaScript tests, Checkstyle, application build, and desktop Chrome against the exact committed artifact.

## Test Cases
Replace the recipient and open another offer. Expire an offer at its exact deadline and preserve both inventories. Verify a two-browser replacement reaches the sender's chat.

## App / Environment
Desktop Chrome at 127.0.0.1:52635 with disposable MongoDB at 127.0.0.1:52634/test.

## Local Run Details
Actuator matched the committed candidate. Seeded supplies in the disposable database. Closed both listeners and removed the test directories.

## Data Sent
```text
Trade Scout offers 1 wood for 1 stone. Replace Trade Smith with New Smith.
```

## Response Received
```text
PASS: replacing the recipient released the sender trade slot, preserved stock, and wrote to chat.
```

## Evidence
The replacement regression failed before the fix and passed afterward. The exact two-minute timeout passed with a controlled clock.

## Bugs / Follow-ups
The Chrome playthrough covered character replacement. The timeout was verified in the Java service tests.
