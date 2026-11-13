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
## Confirmed strike integration
Candidate `2b1437da3562b91d3b13ad61c8ee7d1215b43cc4` preserves both the weapon interval and confirmed strike cue in the survivor snapshot after merging main `cec581eb`. Survive Java tests, Checkstyle main and test, 474 JavaScript tests and bootJar passed. Desktop Chrome checked the exact candidate for both weapons. At 55659, the club showed 3.2s in Equipment and used 3,200 ms between strike deadlines. At 56013, selecting the packed axe showed 3.8s in Equipment and used 3,800 ms between deadlines. The initial axe browser attempt timed out during movement. The rerun used a longer route observation window on the same build. Both pairs of candidate and database listeners closed, and disposable directories were removed.


## Shared party timing integration
Candidate `2514301bfbd12431bc31a07006815d67bbdeed05` integrates main `0cefdc29`. Survive Java tests, Checkstyle, 475 JavaScript tests and bootJar passed on the integration. The added shared-fight regression and final bootJar also passed. The regression saves and restores a bear fight, then checks that the barehanded fighter attacks at 3,000 ms and the club fighter at 3,200 ms, with independent next deadlines and matching enemy HP. Desktop Chrome on the final exact build measured a 3,800 ms stone axe interval and matching Equipment text. Both listeners at 64789 and 64788 closed and disposable directories were removed. The Chrome case was a solo fight.


## First two-client timing attempt
On candidate `2514301bfbd12431bc31a07006815d67bbdeed05`, both Chrome clients reached and engaged the meadow hog. The second client never observed a later strike deadline within the observation window. This attempt leaves shared browser timing unverified. Both listeners at 55612 and 55611 closed and their disposable directories were removed. A bear scenario with a larger enemy health pool is the next test.


## Two desktop clients in a shared bear fight
Exact candidate `2514301bfbd12431bc31a07006815d67bbdeed05` passed at 127.0.0.1:55325. Two isolated Chrome contexts formed a party, walked to the bear and engaged it through the game UI. The harness retained distinct confirmed strike deadlines from the start of combat and sampled the normal status endpoint. The barehanded fighter advanced from 1794519824083 to 1794519827083 ms and the club fighter from 1794519827491 to 1794519830691 ms, for 3,000 and 3,200 ms intervals. Both listeners at 55325 and 55324 closed and disposable directories were removed. An earlier bear run at 64060/64059 timed out after the club fighter died before the observer captured a second deadline. Its listeners also closed. The successful run verifies one interval per fighter. Longer catch-up and shared spear timing remain open.


## Menu navigation baseline
Candidate `307408cd6efd8753bb8a15b48db254b8d748400f` integrates main `98f64390`. The Survive Java suite, Checkstyle main and test, JavaScript tests and bootJar passed. Two desktop Chrome contexts verified the exact build at 127.0.0.1:65507. In the same bear fight, the barehanded and club fighters advanced their deadlines by 3,000 ms and 3,200 ms. Listeners at 65507 and 65506 closed and disposable directories were removed. The integration did not change the observed timing.


## Shared positioning baseline
Candidate `86966d2e0acf5fb64d1a16a947460ba899e374c2` includes main `9a36420f`. The merged snapshot carries both weapon delay and enemy attention. Survive Java tests, Checkstyle, JavaScript tests and bootJar passed. Two desktop Chrome contexts repeated the shared bear fight on the exact build at 127.0.0.1:64288 and confirmed consecutive intervals of 3,000 ms and 3,200 ms. Candidate and MongoDB listeners at 64288 and 64287 closed and disposable directories were removed.


## Document Status
complete

## Project
christopherbell-dev
