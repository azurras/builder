# Survive actor and resource graphics verification

## Story/Issue
Raise character, enemy and resource visual quality toward the user's Final Fantasy XI reference.

## Branch
codex/survive-character-and-wildlife-art at 759d215edf62e03aa5bbbc7c791a56ed09e35de2.

## Pass / Fail
Pass for the model, material, and prop changes. The overall graphics benchmark remains open.

## Test Cases
1. Join the committed desktop build and inspect the adventurer and campfire.
2. Walk to Hunting grounds and inspect a roaming hog and terrain contact shadows.
3. Verify the actor atlas over HTTP and test all enemy meshes, action poses, shelter and boat geometry.
4. Stop the isolated candidate and check listener cleanup.

## App / Environment
http://127.0.0.1:65270/survive with exact test profile and disposable Mongo test on 127.0.0.1:65269.

## Local Run Details
Built with Invoke-Gradle.ps1 bootJar and jsTest. Start-Candidate.ps1 used the isolated runtime. Actuator matched the committed candidate.

## Data Sent
```text
Survivor: Model Scout
Map: Hunting grounds
Keyboard: Minus, W
GET /images/survive/actor-materials.jpg
```

## Response Received
```text
0.0.0-dev.759d215edf62e03aa5bbbc7c791a56ed09e35de2
Actor material atlas: 340830 bytes
{ location: 'Hunting grounds · 4 m', webgl: 'true' }
Browser warnings or errors: []
port 65270 listeners: 0
port 65269 listeners: 0
```

## Evidence
457 JavaScript tests passed, including distinct animal meshes, bounded local texture coordinates, valid animated poses, and finite shelter and boat geometry. Node syntax checks and git diff --check passed. Browser screenshots showed the new adventurer and roaming hog, dynamic fire, and soft shadows. Runtime directories were removed.

## Bugs / Follow-ups
An intermediate shader failed to compile because fragment-only code was in the vertex shader. The final browser check verified the corrected shader and active WebGL. Wolves, bears, shelters and boats had geometry tests and were not individually inspected in the browser. Detailed character rigs and authored model quality remain below the FFXI target.

## Document Status
complete

## Project
christopherbell-dev
