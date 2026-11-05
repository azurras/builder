# Survive chat log verification

## Story/Issue
Show combat, gains, camp events and system messages in a scrolling Final Fantasy XI-style chat log.

## Branch
codex/survive-world-chat-log at 0165213db7cdf09439f594acec5c88bf311dc30d.

## Pass / Fail
Pass. Local browser and automated coverage confirmed chronological logging and an expandable scrollback.

## Test Cases
1. Join, hunt, Check and Engage from the 3D island.
2. Observe repeated damage lines and the victory reward in the same log.
3. Expand with plus and collapse with Escape, then check phone width and teardown.
4. Verify repeated snapshots do not append duplicate events and updates preserve scrollback.

## App / Environment
http://127.0.0.1:56632/survive, exact test profile, disposable Mongo test on 127.0.0.1:56631.

## Local Run Details
Built with Invoke-Gradle.ps1 :website:bootJar :website:jsTest and started with Start-Candidate.ps1. Actuator matched the committed build.

## Data Sent
```text
Survivor name: Log Scout
Map: Hunting grounds
Commands: Hunt, Check, Engage
Keyboard: Plus, Escape
Phone viewport: 390 × 844
```

## Response Received
```text
Wild hog · 5 health · Low threat.
Log Scout: You dealt 2 damage. The hog bit you for 1 damage.
Log Scout: You dealt 2 damage. The hog bit you for 1 damage.
Log Scout: You defeated the hog. You gathered 1 food. The hog bit you for 1 damage.
{ documentWidth: 375, scrollbackFocused: true, viewport: 390 }
port 56632 listeners: 0
port 56631 listeners: 0
```

## Evidence
All 452 JavaScript tests passed. Node syntax checks and git diff --check passed. The browser check used ordinary game commands. The phone viewport reset and isolated runtime cleanup succeeded.

PR #1562 merged as 1d31740c48e97416a530bb958f6fdba4ce02dc76. Merged CI and CodeQL passed. Production returned HTTP 200 for Survive and survive-log.js, and the page included the chat scrollback and Main Menu.

## Bugs / Follow-ups
The window shows world events and local system messages. Player-to-player chat and channel filters are separate MMO features.

## Document Status
complete

## Project
christopherbell-dev
