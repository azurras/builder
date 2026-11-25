# Survive layered adventurer armor test report

## Story/Issue

Consolidate the layered shoulders and boots from [#1626](https://github.com/azurras/christopherbell.dev/pull/1626) with the fitted chest and belt from [#1627](https://github.com/azurras/christopherbell.dev/pull/1627).

## Branch

`codex/survive-layered-armor` at `44d76b156eaddeb4c4c1dea94027359dc95aa104`, based on main at `4eb43e0a`.

## Pass / Fail

> [!TIP]
> **3 of 3 passed** on candidate `44d76b15`.

| # | Test case | Result | Observation |
|---|---|---|---|
| 1 | Asset and texture compatibility | ✅ PASS | 483 browser-side tests passed and the committed application built. |
| 2 | Armor while walking | ✅ PASS | Chrome rendered the shoulder rims, chest bands, belt and boots. The server accepted the step. |
| 3 | Club combat | ✅ PASS | The server recorded a club strike against a meadow hog, then accepted Disengage. |

## Test Cases

1. **Asset and texture compatibility.** Check the original torso PR model against the consolidated asset. Run the atlas, animation and full JavaScript tests.
2. **Armor while walking.** Inspect the front, side and rear views, then walk with motion enabled and inspect two frames.
3. **Club combat.** Craft a club, approach a roaming hog with keyboard movement, choose Engage, observe an actual strike, then choose Disengage.

## App / Environment

| Setting | Value |
|---|---|
| App | Survive at `http://127.0.0.1:62314/survive` |
| Profile | Spring `test` with disposable MongoDB at `127.0.0.1:62313/test` |
| Browser | Desktop Chrome, 1366 × 900 window, NVIDIA GeForce RTX 4070 via ANGLE and Direct3D 11 |

## Local Run Details

- **Local command:** `./ops/local/Start-Candidate.ps1 -StateFile $stateFile` from the isolated armor checkout after building the committed JAR.
- The actuator returned build version `0.0.0-dev.44d76b156eaddeb4c4c1dea94027359dc95aa104`. The walking setup displayed daylight and used reduced motion for idle angles, then enabled motion for walking. The combat browser used normal motion and the server's phase.
- The candidate process and its database had zero listeners after shutdown. The candidate helper removed both disposable directories.

## Data Sent

### 1. Asset and texture compatibility

```text
git diff --quiet f4216f53 HEAD -- website/src/main/resources/static/images/survive/adventurer.json
node --check on all three changed JavaScript files
node --test website/src/test/js/survive-world-art.test.js website/src/test/js/survive-world-materials.test.js
./ops/local/Invoke-Gradle.ps1 :website:jsTest :website:bootJar
```

### 2. Armor while walking

```text
Open /survive at (-6, -9), orbit and zoom for front, side and rear views.
Enable motion and hold S. Capture two walking frames and release S.
```

### 3. Club combat

```text
Gather wood and craft a club. Walk into range of meadow-hog.
Select the hog and choose Engage. After the first club strike choose Disengage.
```

## Response Received

### 1. Asset and texture compatibility

```text
Original PR asset comparison: exit 0
Syntax checks: exit 0
27 targeted tests passed
483 full JavaScript tests passed
BUILD SUCCESSFUL
```

### 2. Armor while walking

```text
Server-confirmed step: -0.758400000000014 (z)
PASS: desktop front and profile rendered with authored asset.
```

### 3. Club combat

```json
{"revision":5,"at":"2026-11-25T00:00:31.015Z","weapon":"CLUB","weaponSkill":false}
```

The browser observed a scheduled strike on Engage and a cleared strike time after Disengage. The engaged screenshot shows the hog at 2 health.

## Evidence

Eight desktop captures covered idle angles, two walking frames and engaged/disengaged combat. Visual review showed the shoulder rims following the arms, chest bands aligned on the torso, and the boot soles touching the ground in the side view. The committed character asset was byte-identical to the original torso PR head. The updated atlas test exercised the foliage, actor materials, face and armor paint on the current texture units.

## Bugs / Follow-ups

The combat target label partially covers the upper body in the engaged screenshot. The unobstructed walking and idle captures show the armor detail.

## Document Status

complete

## Project

christopherbell-dev

## November 25 release verification

After the lighting merge, candidate `cd7288af37e712c41ba86b682df15f120b39a918` passed all 487 JavaScript tests, the application build and syntax checks on the three changed JavaScript files. The adventurer asset matched the original torso PR byte for byte.

Desktop Chrome on the RTX 4070 captured eight views at `http://127.0.0.1:59600/survive` against the identity-verified build. The server confirmed a walking step and recorded a club strike against a roaming hog at 14:42:29 UTC. The target menu accepted Disengage. After shutdown, both candidate and test database ports had zero listeners and both disposable directories were removed.
