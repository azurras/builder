# Survive authored adventurer and boar verification

## Story/Issue
Replace the procedural close-up adventurer and boar with painted animated game models.

## Branch
codex/survive-authored-actors at d512793463c773b03bb6f422261ed41ca52ed0a5.

## Pass / Fail
Pass for the adventurer and boar update. The broader graphics benchmark remains open.

## Test Cases
1. Join camp and inspect the adventurer from the desktop follow camera.
2. Walk to Hunting grounds, turn the camera and inspect the roaming boar and player.
3. Confirm the asset URLs return data and compare baked walking, attack and equipment poses.
4. Stop the isolated runtime and check listeners.

## App / Environment
http://127.0.0.1:51239/survive with test profile and disposable Mongo on loopback port 51238.

## Local Run Details
Invoke-Gradle.ps1 bootJar and jsTest, then Start-Candidate.ps1. The candidate build identity matched the branch head.

## Data Sent
```text
Survivor Armor Scout
Keyboard A, S, W and Q
GET /images/survive/adventurer.json
GET /images/survive/boar.json
GET /images/survive/authored-actors.jpg
```

## Response Received
```text
Hunting grounds · 5 m
Painted armored adventurer and passive boar visible
Browser warnings or errors []
Asset responses 200, 200, 200
Ports 51239 and 51238 listeners 0
```

## Evidence
All 455 JavaScript tests passed. Node syntax and git diff checks passed. The desktop browser showed painted armor and the roaming boar together. Tests verified changing walk and strike poses, action geometry and texture bounds. Runtime directories were removed.

## Bugs / Follow-ups
The armored character remains stylized and the wolves, bears and environment use their existing meshes. The detailed adventurer is limited to the local character and up to six other nearby characters. Equipment gestures had geometry coverage. The local browser check focused on walking and turning the camera.

## Document Status
complete

## Project
christopherbell-dev
