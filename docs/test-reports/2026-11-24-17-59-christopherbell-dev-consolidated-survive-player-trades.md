# Consolidated Survive player trades

## Story/Issue

Consolidate the trade lifecycle, packed weapons, counteroffers, bundles and nearby-partner changes from PRs #1615 through #1620 on the Survive menu shipped by #1633.

## Branch

`codex/consolidate-survive-trade-20261124` at `87272a0b4f08ae8066639970f954bc5a8ed3985d`, based on `4eb43e0a33381168725d11bc1326c18850ebb6fa`.

## Pass / Fail

> [!TIP]
> **2 of 2 runtime cases passed** on candidate `87272a0b`.

| # | Test case | Result | Observation |
|---|---|---|---|
| 1 | Identify the running application | ✅ PASS | The actuator build version matched the full committed source SHA. |
| 2 | Confirm a nearby two-player bundle counteroffer | ✅ PASS | Both players reviewed the terms before acceptance and received the expected weapon. The original recipient also received one wood. |

## Test Cases

1. **Candidate identity.** Start the built JAR and read its version from the running process.
2. **Two-player trade.** Use separate browser sessions to open Main Menu, move to the second page, open Camp and then Trade. Send a bundle and counteroffer. Check the visible terms and inventories before acceptance, then check both inventories and the accepting player's chat afterward.

## App / Environment

| Setting | Value |
|---|---|
| Application | christopherbell.dev, Survive |
| Runtime | Windows, Spring test profile, two isolated desktop Chrome sessions |
| Application URL | `http://127.0.0.1:56620` |
| MongoDB | `mongodb://127.0.0.1:56619/test`, fresh disposable instance |
| Fixture | Two guest players created through the game API. The disposable world was seeded with known resources and packed weapons. |

## Local Run Details

- **Local command:** `pwsh -NoProfile -File "$env:TEMP/survive-trade-consolidated-20261124-verify.ps1"`
- **Working directory:** Candidate checkout for `codex/consolidate-survive-trade-20261124`.
- **Processes:** Repository start and stop scripts managed Java and MongoDB. The browser harness launched and closed Chrome.
- **Logs:** The runtime and Gradle transcripts were captured as `survive-trade-consolidated-20261124-runtime.log` and `survive-trade-consolidated-20261124-checks.log` in the local temporary directory.
- **Cleanup:** The stop script confirmed zero listeners on both ports and removed the database and JDK socket directories. The harness removed the temporary cookie file and Chrome profile.

## Data Sent

### 1. Candidate identity

```http
GET /actuator/info HTTP/1.1
Host: 127.0.0.1:56620
```

### 2. Two-player trade

```text
Trade Scout offered a packed club with three uses plus one wood to Trade Smith for one stone.
Trade Smith reviewed the terms and countered with a distinct club with two uses.
Trade Scout reviewed the new terms and accepted the counteroffer.
```

## Response Received

### 1. Candidate identity

```text
build.version = 0.0.0-dev.87272a0b4f08ae8066639970f954bc5a8ed3985d
```

### 2. Two-player trade

```text
PASS: both players confirmed a revised bundle and exchanged two distinct weapons and one wood.
port 56620 listeners: 0
port 56619 listeners: 0
```

The harness confirmed that the nearby partner picker was visible in both sessions. Each player still held their original club before acceptance. After acceptance both pending offers cleared, each player held the other club's exact ID, Trade Smith held one wood, and Trade Scout's chat named both weapons' remaining uses.

## Evidence

Node syntax checking passed for the changed game script. Gradle passed all 102 Survive and Mongo codec tests, all 481 JavaScript tests, main and test Checkstyle, and the boot JAR build. Service tests exercised trade expiry and replacement, weapon identity, bundle validation, superseded offers, and the five-metre boundary at acceptance.

## Bugs / Follow-ups

Expiry and the distance boundary were verified in service tests. The browser playthrough covered a nearby exchange. Main advanced by a workflow-only commit after this branch was created.

## Document Status

complete

## Project

christopherbell-dev
