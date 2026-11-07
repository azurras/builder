# Define the Survive adventurer face

## Document Status
in-progress

## Objective
Make the original adventurer's facial features readable from the desktop camera during normal play.

## Background
The live model has sculpted cheeks and a nose. Its mirrored skin chart in the shared actor atlas has weak eye and mouth definition at game scale.

## Goals
- Add brows, eyelids, irises and a subdued mouth line on the mapped face (AC-1).
- Keep the existing actor atlas size and draw path (AC-2).

## Non-Goals
| Area | Scope |
|---|---|
| Character choices | The parent ART-01 row tracks distinct silhouettes and equipment. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Matched desktop screenshots show the features aligned with the modeled face from front and three-quarter views. |
| AC-2 | The upload uses the same texture slot and dimensions, and the existing meshes and clips pass native checks. |
| AC-3 | Candidate proof, CI and production readback are recorded. |

## Inputs
- Parent plan 2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md, ART-01.
- Inspected live main 125bd326, adventurer.json, authored-actors.jpg and the texture upload.

## Branch
codex/survive-adventurer-face

## Assumptions
The current atlas and adventurer UV chart are a paired asset. Paint the original vector detail into the staging canvas once before uploading the shared atlas.

## Open Questions
None for the face pass.

## Design
Project eye, brow and mouth landmarks from the front of the idle mesh onto the mirrored skin island. Paint those details in atlas coordinates. Compare a fixed camera orbit on the live baseline and candidate.

## Expected Changes
| Area | Change |
|---|---|
| Island materials | Paint the authored adventurer face before uploading its existing shared atlas. |
| Browser tests and docs | Verify the staging and upload boundary and record matched desktop captures. |

## Task Breakdown
### Task 1 - Paint the face on the authored atlas
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| Dependencies | Existing authored adventurer and atlas |
| Files | survive-world-materials.js, survive-world-materials.test.js and JavaScript README |
| Symbols | createIslandMaterials and paintAdventurerFace |
| Inspection | Compare mapped head triangles to the texture and review default desktop camera captures |
| Behavior | Paint mirrored facial details before texture upload |
| Invariants | Same texture slot, dimensions, rig and pose data |
| Boundary/API | Existing material loader and texture atlas |
| Effects and failures | Paint on the existing short-lived staging canvas and release textures through existing ownership |
| Tests and evidence | Verify painted staging canvas reaches the expected texture slot and compare browser captures |
| Verification | Changed JS syntax, jsTest, bootJar and exact candidate runtime |

## Test Plan
| AC | Check |
|---|---|
| AC-1 | Match front and three-quarter views in isolated desktop Chrome on baseline and candidate |
| AC-2 | Texture loader regression and full JS suite |
| AC-3 | Publish report, CI and production readback |

## Rollback or Recovery
Revert the texture staging change.

## Risks
Atlas coordinates need review if the head UV chart is replaced. The visual comparison must catch misplaced or overly dark marks.

## Implementation Log

### 2026-11-07 - Verify atlas upload and desktop orbit

- **Change:** Painted eyes, brows and soft lip contours on the original adventurer's mirrored face chart before the existing atlas upload.
- **Reason:** Front desktop captures exposed an almost featureless face despite the modeled nose and cheeks.
- **Impact:** Candidate 4ef4f6e5 passed 473 JavaScript tests and repeated the desktop orbit with merged enemy defeat. Eyes and brows are clearer. Mouth definition, head geometry, character variation and matched lighting at all angles remain open. [Child plan](2026-11-07-12-23-christopherbell-dev-survive-adventurer-face.md) · [Runtime report](../test-reports/2026-11-07-12-27-christopherbell-dev-survive-adventurer-face.md)

### 2026-11-07 - Verify production build and material module

- **Change:** Verified production build e5d948e2 from PR #1598 and confirmed the public material module serves the face paint.
- **Reason:** Keep the shipped art state distinct from isolated desktop capture evidence.
- **Impact:** Eyes and brows are live. Head geometry, mouth definition and character silhouettes remain open under ART-01. [Face PR](https://github.com/azurras/christopherbell.dev/pull/1598)

## Outcome
PR #1598 shipped at e5d948e2.

| Criterion | Result |
|---|---|
| AC-1 | Partial. The front comparison shows improved eyes and brows. The three-quarter views need matched lighting. |
| AC-2 | Passed. Existing texture slot, dimensions and native tests verified. |
| AC-3 | Passed. CI, candidate and live readback recorded. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
