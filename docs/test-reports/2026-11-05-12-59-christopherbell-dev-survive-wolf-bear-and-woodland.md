# Survive wolf, bear and woodland verification

## Story/Issue
Replace the remaining procedural wildlife with textured models and build less angular tree crowns and more underbrush.

## Branch
codex/survive-authored-wolf-and-bear at a683d76e1310c533537b35506f70a2df48604d6f.

## Pass / Fail
Pass for the new wildlife and woodland. The overall FFXI graphics benchmark remains open.

## Test Cases
1. Join the desktop candidate and walk to the ridge patrols.
2. Inspect the textured roaming bear and wolf with their hostile labels.
3. Inspect the layered canopy and trail underbrush from camp.
4. Verify the rebased build identity, static assets and isolated cleanup.

## App / Environment
Local desktop browser on the test profile with disposable loopback Mongo. Wildlife visual candidate used port 53788 and the combined candidate used port 54656. The rebased commit used http://127.0.0.1:63089/survive and an identical Git tree.

## Local Run Details
Built via Invoke-Gradle.ps1 bootJar and jsTest. Started and stopped each candidate via the repository scripts. The rebase onto the merged adventurer update preserved tree dd11996702421caf674c2f05da5ed84562e82eb3 exactly. The rebased candidate's actuator identity matched its commit.

## Data Sent
```text
Survivors Wildlife Scout and Forest Scout
Keyboard D, W, S, A and Q
GET /survive and the wolf, bear, atlas and woodland assets
```

## Response Received
```text
Bear and wolf roaming with hostile labels
Layered canopy and underbrush visible
Browser warnings or errors []
All five HTTP responses 200
Ports 63089 and 63088 listeners 0
```

## Evidence
455 JavaScript tests passed for the identical tree. The static island contains 51246 triangles, below its 55000-triangle test budget. Node syntax checks and git diff --check passed. The desktop browser showed both animals and the new canopy in the expected world locations.

## Bugs / Follow-ups
Bear gait uses baked mesh deformation. Movement around the ridge exposed existing avatar clipping into scenery. The visual check did not benchmark frame rate on low-power laptops or crowded multiplayer scenes.

## Document Status
complete

## Project
christopherbell-dev
