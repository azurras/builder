# Survive shared party enmity verification

## Story/Issue
Route shared enemy counters to the fighter with the most enmity under COM-02. [Living plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md) · [Child plan](../implementation-plans/2026-11-07-13-09-christopherbell-dev-survive-party-enmity.md)

## Branch
`codex/survive-party-enmity-stack` at `453f361cb38778bf12e72d6e970b44b17f993b9d`, with the local strike fix from #1596 and main 99b7edfe.

## Pass / Fail
| Check | Result |
|---|---|
| Durable and fading scores | PASS. Early strike targets the existing leader and a later strike changes the target after decay. |
| Save compatibility | PASS. Mongo round trip retains scores and legacy encounter data without scores decodes empty. |
| Guard and departure | PASS. Counter consumes the target's guard and Flee removes that fighter's score. |
| Shared browser fight | PASS. Both players agree on enemy HP and the engaged defender receives the reply without advancing their own strike. |

## Test Cases
1. Open with Heavy Strike, save and restore the fight, then attack with the ally before and after the original fading points decay.
2. Arm guard on the enmity leader before the ally attacks. Verify both messages and the recipient's health and revision.
3. Verify Mongo round trip, old-data default, and leaving the fight.
4. In desktop Chrome, form a party, take North Gate Patrol and join one bear fight. Use authenticated game commands to open with Heavy Strike, defend while engaged, and attack with the ally. Compare both responses and the defender's scheduled strike.

## App / Environment
Desktop Chrome with separate contexts at 1366 × 900 and software WebGL. Exact integrated candidate at 127.0.0.1:62309 with disposable MongoDB 127.0.0.1:62308/test.

## Local Run Details
Verified actuator identity before Chrome. Used the normal route and party controls to reach the encounter. The harness submitted the precise combat commands via the normal API to avoid UI timing changing the case. Both listeners closed and temporary runtime directories were removed.

## Data Sent
```text
Party invite and accept, North Gate Patrol, engage the same ridge bear
Scout Heavy Strike, Scout Defend while still engaged, ally Attack
Read both survivor snapshots and compare guard, HP and strike cue
```

## Response Received
```text
PASS: the bear countered the enmity leader while the ally attacked; guard was consumed and both clients agreed on enemy HP.
port 62309 listeners: 0
port 62308 listeners: 0
```

## Evidence
- The initial guard and decay regressions failed before enmity and passed after implementation. The original `55d202377c267215adc00d6e6237e0e1ed6f4997` passed the full Java suite, 473 JavaScript tests, Checkstyle and bootJar.
- The integrated candidate passed targeted Survive and codec tests, Checkstyle, the JS task and bootJar. The mounted-world check renders the counter cue without a fabricated defender swing. The browser also verified the defender's original strike deadline and no newer own strike marker.
- Review identified the phantom swing from the former revision/HP heuristic. The integrated candidate includes confirmed strike ownership from #1596 as a release dependency.
- Earlier isolated probes at 64027/64026 and 62621/62620 stopped when the harness tried to arm guard while disengaged or received HTTP 400 during unrelated equipment gathering. The corrected test keeps the defender engaged and drops the unnecessary gear prep. All four listeners closed.

## Bugs / Follow-ups
The starting Survive coefficients are 1,000 durable and 3,000 fading points per damage, one fading point lost per millisecond, and 1,000 durable points lost per HP received. Ties favor the earlier fighter. Retaliation still follows surviving strikes. Jobs, Provoke, healing threat, independent monster attack timing and visual facing remain open. The browser run verifies routing and state, with the animation behavior covered by the mounted test.

## Main integration rerun
Exact candidate `cba4a7ac3c4860abca1f0a475daf5ccb4d0f008b` integrated main `cec581eb` after #1596 merged. The candidate tree matched the previously verified stack. JavaScript tests and bootJar passed after integration. Actuator confirmed the new build identity before launching both desktop Chrome contexts. The bear countered the enmity leader, consumed guard and preserved agreement on enemy HP. The candidate and MongoDB listeners at 64648 and 64647 closed, and both disposable directories were removed.


## Document Status
complete

## Project
christopherbell-dev
