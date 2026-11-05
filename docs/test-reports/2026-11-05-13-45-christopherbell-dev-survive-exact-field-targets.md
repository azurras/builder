# Survive exact field targets verification

## Story/Issue
Let the player select, Check and Engage an exact roaming creature.

## Branch
codex/survive-exact-field-targets at 713644f6cbc5a5b215384747eb067e344608494e.

## Pass / Fail
Pass.

## Test Cases
1. Select a roaming hog with Tab and open Commands.
2. Confirm Check writes the creature threat in chat and Engage becomes unavailable outside reach.
3. Send the ID of an out-of-range hog and then the exact in-range target.
4. Confirm the movement encounter ID, initial timed hit, and tactical points.
5. Verify the final committed build and shut down the isolated runtime.

## App / Environment
Desktop WebGL and HTTP on http://127.0.0.1:49170/survive using the test profile and disposable loopback Mongo. Rebased runtime at http://127.0.0.1:55296/survive.

## Local Run Details
Built with Invoke-Gradle.ps1 bootJar, test and jsTest. Used Start-Candidate.ps1 and Stop-Candidate.ps1. Rebase preserved the exact tree used for browser and HTTP verification.

## Data Sent
```text
Tab, Enter and Check at the Hunting grounds
POST /api/survive/v1/actions with ENGAGE and targetId shore-hog then meadow-hog
GET /api/survive/v1/game after one scheduled round
```

## Response Received
```text
Chat: hog · Low threat.
Out-of-range target HTTP 400
Exact target meadow-hog, status COMBAT
After first strike: enemy HP 3, TP 50
Browser warnings or errors []
```

## Evidence
All 459 JavaScript tests and the Survive Java tests passed. Node syntax and diff checks passed. Browser verification covered keyboard selection, contextual commands and chat. The isolated HTTP test covered successful Engage and the first timed round. Targeting tests cover selecting a farther creature without falling back to a closer one.

## Bugs / Follow-ups
A moving target can leave reach between opening the command menu and choosing Engage. The menu updates its availability and the server checks distance again. Shared encounter health and coordinated skills remain separate work.

## Document Status
complete

## Project
christopherbell-dev
