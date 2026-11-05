# Survive in-world menu verification

## Story/Issue
Remove the sidebar from the game and use Final Fantasy XI-style in-world menus.

## Branch
codex/survive-ffxi-menus at a9b85fd3c1a1de1ba25033027aeee96af046b8ce.

## Pass / Fail
Pass. The full-width world and in-world windows worked on desktop and at phone width.

## Test Cases
1. Open Main Menu, move to Items with the arrow key, inspect inventory and close with Escape.
2. Walk to Hunting grounds from Map, open Commands, Hunt, select a hog and use Check, Engage, Defend and Disengage.
3. Open Equipment at 390 × 844 and check that the sidebar is gone and there is no horizontal overflow.
4. Stop the isolated candidate and verify listener cleanup.

## App / Environment
http://127.0.0.1:53090/survive, exact test profile, disposable Mongo database test at 127.0.0.1:53089.

## Local Run Details
Invoke-Gradle.ps1 ran bootJar and jsTest. Start-Candidate.ps1 confirmed readiness. Actuator build version matched the exact candidate.

## Data Sent
Joined as Window Scout and used keyboard and pointer commands through the game UI. No production mutations or direct database writes were used.

```text
Survivor name: Window Scout
Keyboard: Minus, ArrowDown, Enter, Escape
Map: Hunting grounds
Commands: Hunt, Check, Engage, Defend, Disengage
Viewport: 390 × 844
```

## Response Received
Items displayed the inventory. Map walking reached the hunting grounds. Check showed low threat and 5 health. Disengage showed that automatic attacks stopped. Equipment showed Bare hands at phone width.

```text
0.0.0-dev.a9b85fd3c1a1de1ba25033027aeee96af046b8ce
{ hasSidebar: false, scrollWidth: 375, width: 390 }
port 53090 listeners: 0
port 53089 listeners: 0
```

## Evidence
All 451 JavaScript tests passed. Node syntax checks and git diff --check passed. The responsive browser viewport was reset and the isolated candidate directories removed.

## Bugs / Follow-ups
The earlier candidate exposed decorative arrows in accessible action names. The final candidate uses decorative CSS borders and was verified using the exact accessible names Hunt, Check and Engage. Map lists the existing destinations.

## Document Status
complete

## Project
christopherbell-dev
