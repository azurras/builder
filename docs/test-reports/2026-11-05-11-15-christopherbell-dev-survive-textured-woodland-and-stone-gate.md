# Survive textured woodland and stone gate verification

## Story/Issue
Use the user's Final Fantasy XI graphics screenshots as the visual benchmark. Improve the actual 3D scene with original materials, foliage, masonry, lighting, and a closer adventurer view.

## Branch
codex/survive-woodland-materials at b58d8cb8182bac6e221262128b0dcb8eee5eb6ad.

## Pass / Fail
Pass for the texture and camera pass. The reference images remain the quality target for future character and environment mesh detail.

## Test Cases
1. Join the committed build and inspect the default desktop camera, cloth and armor layers, stone gate, cutout leaves, bark, and paths.
2. Use Map to walk to Pine forest and check the active renderer and browser console.
3. Verify both texture files load over HTTP and geometry stays within budget.
4. Stop the isolated candidate and confirm listener cleanup.

## App / Environment
http://127.0.0.1:53748/survive, exact test profile, disposable Mongo test on 127.0.0.1:53747.

## Local Run Details
Built with Invoke-Gradle.ps1 bootJar and jsTest. Start-Candidate.ps1 started the isolated application. Actuator reported the exact candidate. Both new assets are original generated textures optimized for the game.

## Data Sent
```text
Survivor: Woodland Scout
Keyboard: Minus
Map destination: Pine forest
GET /images/survive/island-materials.jpg
GET /images/survive/foliage.png
```

## Response Received
```text
0.0.0-dev.b58d8cb8182bac6e221262128b0dcb8eee5eb6ad
Material atlas: 439272 bytes
Cutout foliage: 394776 bytes
{ active: 'true', canvasWidth: 1192 }
Pine forest · 1 m
Browser warning/error list: []
port 53748 listeners: 0
port 53747 listeners: 0
```

## Evidence
455 JavaScript tests passed. Node syntax checks and git diff --check passed. Browser screenshots showed the closer rear-view avatar, weathered stone arch, leaf silhouettes, dark patches under trees and separate grass and path textures. The browser closed and the isolated runtime was removed.

PR #1566 merged as c8fe7e444c2b616e61fb2187b0b1771bffcbbbc6. Merged CI and CodeQL passed. Production served the exact build, both texture files at their expected byte counts, and the WebGL material loader.

## Bugs / Follow-ups
Character, prop and terrain geometry still have less detail than the references. The gate is visual scenery and does not change collision, combat or movement rules. No direct performance benchmark or physical phone-controller test was run for this art change.

## Document Status
complete

## Project
christopherbell-dev
