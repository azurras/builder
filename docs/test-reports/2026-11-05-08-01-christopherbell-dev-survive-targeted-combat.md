# Survive targeted combat verification

## Story/Issue
Build the first Final Fantasy XI-inspired combat loop in the shared island.

## Branch
codex/survive-targeted-combat-20261105 at 77b1576ba00409342fa5c9e4279eda783dee31f8.

## Pass / Fail
Pass for targeted combat on the committed local candidate.

## Test Cases
1. Select, Check and Engage a wild hog in the 3D world, then use Heavy Strike after earning TP.
2. Engage as a separate guest, disconnect for 13 seconds, and observe the saved outcome on return.
3. Stop the isolated candidate and confirm cleanup.

## App / Environment
Survive at http://127.0.0.1:55262/survive with the test profile and disposable loopback Mongo on port 55261, database test.

## Local Run Details
Invoke-Gradle.ps1 ran bootJar and jsTest. Start-Candidate.ps1 checked readiness. Actuator build version matched the candidate commit.

## Data Sent
Blade Scout joined and walked to Hunting grounds. Browser commands were Hunt, select the hog, Check, Engage and Weapon skill. A separate guest sent Hunt and Engage through the normal game API and made no requests for 13 seconds.

## Response Received
The selected hog showed Low threat and 5 health. The first timed exchange showed 50 TP and 3 enemy health. Heavy Strike finished the hog and awarded 1 food. The disconnected guest returned to EXPLORING with a durable victory outcome and 150 TP. Re-reading did not replay the fight. Both test ports reported zero listeners after Stop-Candidate.ps1.

```text
After 13 seconds without requests: EXPLORING You defeated the hog. You gathered 1 food. The hog bit you for 1 damage. TP: 150
port 55262 listeners: 0
port 55261 listeners: 0
```

## Evidence
448 JavaScript tests passed. Focused Java tests for Survive and the Mongo codec passed, along with main and test Checkstyle. Node syntax checks and git diff --check passed.

## Bugs / Follow-ups
Browser verification used the default viewport. This slice uses individual encounters. Shared enemies and coordinated parties are future MMO work.

## Document Status
complete

## Project
christopherbell-dev
