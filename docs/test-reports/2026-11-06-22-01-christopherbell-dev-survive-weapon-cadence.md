# Survive weapon cadence: Test Report

## Story/Issue
Give weapons distinct cadence under COM-02 in the [living parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md).

## Branch
`codex/survive-weapon-cadence` at `2c94362cc353c22539a017d2daf4663c16207e89`.

## Pass / Fail
> [!TIP]
> **2 of 2 passed** on candidate `2c94362c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Weapon deadlines and breakage | ✅ PASS | Each weapon waits until its deadline; breaking the club switches the next interval to bare hands. |
| 2 | Desktop club cadence and Equipment | ✅ PASS | Chrome observed 3,200 ms between two confirmed strike deadlines and displayed the delay. |

## Test Cases
1. Run the Survive weapon and service tests, including timed exchanges and saved-world tests.
2. Craft a club, approach meadow-hog, Engage and compare the first two server deadlines in Chrome.

## App / Environment
| Setting | Value |
|---|---|
| Runtime | Test profile at http://127.0.0.1:53683 |
| Database | Disposable MongoDB at 127.0.0.1:53682/test |
| Browser | Desktop Chrome with software WebGL |

## Local Run Details
- Verified exact actuator version before Chrome.
- Closed both ports and removed both temporary directories after the run.

## Data Sent
```text
Craft a club through normal gathering and crafting
Walk to meadow-hog and ENGAGE
Compare consecutive nextStrikeAt values and inspect Equipment text
```

## Response Received
```text
PASS: Chrome confirmed a 3200 ms club cadence and showed 3.2s delay in Equipment.
port 53683 listeners: 0
port 53682 listeners: 0
```

## Evidence
- Full Java suite, including Survive and codec tests, 469 JavaScript tests, changed-script syntax and bootJar passed.
- Bare hands use 3 seconds, clubs 3.2, axes 3.8 and spears 4.2. These are initial Survive balance values.
- Existing saved next-strike deadlines retain their time. The following strike uses the current weapon delay.

## Bugs / Follow-ups
Browser proof covers the club in a personal encounter. Axe, spear, shared-fight cadence, long catch-up, and combat balance need broader playtesting. TP gain still uses the existing per-hit amount.

## Nearby-presence integration
Candidate 8b3a59e4f09997776fac10f6666ce5a4a1edc2e8 integrates the nearby-pose payload change. Targeted Survive Java and codec tests, JavaScript tests and bootJar passed. Exact actuator identity was checked at http://127.0.0.1:59425 with disposable MongoDB on 127.0.0.1:59424/test. Chrome repeated the 3,200 ms club interval and Equipment-label checks. Both listeners closed at teardown.

## Timed fishing and face integration
Candidate `31563f153d259e088cfba9eaa4efe3104bfbb5f2` includes main `e5d948e2`. The snapshot retains fishing timing alongside weapon delay. Targeted Survive and Mongo codec tests, 473 JavaScript tests and bootJar passed.

Two isolated desktop Chrome runs verified the exact candidate. The club test at 127.0.0.1:60935 with MongoDB 127.0.0.1:60934/test measured 3,200 ms between confirmed deadlines and showed 3.2s in Equipment. The axe test at 127.0.0.1:64569 with MongoDB 127.0.0.1:64568/test equipped the packed axe from the Main picker, measured 3,800 ms and showed 3.8s in Equipment. Both runs approached and engaged a roaming hog. All four listeners closed.

The first axe harness at 60548/60547 compared raw timestamp strings and treated a differently formatted value at the same parsed millisecond as a new deadline. It stopped with a measured delta of 0. The corrected harness waited for a later parsed instant and passed on the same build. Those two listeners also closed. Spear and shared-fight timing still need direct browser evidence.
## Document Status
complete

## Project
christopherbell-dev
