## Document Status
Complete

## Project
christopherbell-dev

## Story/Issue
Clarify the adventurer's shoulder layers and boot silhouette for ART-01.

## Branch
codex/survive-adventurer-armor at 78abf6d4f8df4123fe292deda3e85f1fe06c2b20. Face baseline 095cf662bb27d464ed651fa70d1c2f6351797c8b.

## Pass / Fail
Passed JavaScript syntax checks, all 478 browser-side tests, the exact application build, and matched front and side desktop captures plus walking.

## Test Cases
Verify the shoulder outline, boot sole contacts, baked frame lengths and layer swatches. Check that the packing and material upload still use the shared actor atlas and that existing hand attachments and motion tests pass. Compare the same adventurer position and camera angles before and after the armor changes. Check the new silhouette in sampled walking poses.

## App / Environment
Desktop Chrome with a 1366 × 900 window and 1350 × 805 captures. Hardware WebGL used the NVIDIA GeForce RTX 4070 through ANGLE and D3D11. Baseline http://127.0.0.1:53499/survive and candidate http://127.0.0.1:56880/survive both used disposable loopback MongoDB test databases.

## Local Run Details
The actuator on each application identified its exact source commit. The baseline uses the existing matched face verification captures. Both runs held the same displayed daylight phase and reduced motion for stills, then restored motion for the walking frames. Candidate startup and shutdown completed and the disposable database and listeners were cleaned up.

## Data Sent
```text
Move to (-6, -9). Capture the default view and the nearest in-game view with Page Up. Rotate the camera twelve times with R for the profile. Restore motion, rotate back with Q, and walk with S.
```

## Response Received
```text
478 JavaScript tests passed.
2,179 baseline triangles and 2,251 candidate triangles per adventurer.
Baseline asset 1,362,150 bytes and candidate asset 1,398,781 bytes.
Both have 13 clips and 81 frames. Server-confirmed movement endpoint z = -3.9162.
```

## Evidence
The front capture shows a narrower shoulder silhouette that leaves more of the leather sleeve visible. In profile the smaller plate is visible below the upper shell. The wider toe and brown outsole remain distinct at the closest in-game camera zoom. Both sampled walking frames show the armor following the arms and boots.

## Bugs / Follow-ups
The chest, hands and cloth still use the previous designs. These captures do not characterize continuous foot contact, action animation or GPU frame cost.
