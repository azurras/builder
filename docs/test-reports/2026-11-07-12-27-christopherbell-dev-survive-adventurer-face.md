# Survive adventurer face verification

## Story/Issue
Improve facial readability for ART-01 in the [living parity plan](../implementation-plans/2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md). [Child plan](../implementation-plans/2026-11-07-12-23-christopherbell-dev-survive-adventurer-face.md).

## Branch
`codex/survive-adventurer-face` at `4ef4f6e50e1d1e75de7db7845cf39835c20960ba`, including main `bf51abaf`.

## Pass / Fail
| Check | Result |
|---|---|
| Texture staging and upload | PASS. Facial paint reaches the existing 1024 px authored actor atlas before upload. |
| Desktop front and three-quarter views | PASS for visible eye and brow definition. Mouth remains subtle at the tested distance. |
| Native checks | PASS. Syntax, 473 JavaScript tests and candidate build. |

## Test Cases
1. Run the texture staging regression on the baseline implementation and again with the new paint.
2. Join a fresh survivor at camp and orbit the camera by 26 Q steps and seven R steps. Capture both views at default distance.
3. Repeat on the integrated candidate and verify each runtime's build identity and cleanup.

## App / Environment
| Build | Isolated runtime |
|---|---|
| Baseline `125bd326` | 127.0.0.1:53895 with MongoDB 127.0.0.1:53894/test |
| First candidate `522aa5e3` | 127.0.0.1:57874 with MongoDB 127.0.0.1:57873/test |
| Integrated candidate `4ef4f6e5` | 127.0.0.1:51437 with MongoDB 127.0.0.1:51436/test |

## Local Run Details
Used the test profile and disposable MongoDB, with desktop Chrome at 1366 × 900 using software WebGL. Checked exact actuator identity before each browser run. All six listeners closed during cleanup.

## Data Sent
```text
Join Portrait Scout at camp
Rotate camera 26 KeyQ presses for front view
Rotate 7 KeyR presses for three-quarter view
```

## Response Received
```text
PASS: desktop Chrome captured the authored adventurer from front and three-quarter views.
473 JavaScript tests, zero failures on 4ef4f6e5.
port 51437 listeners: 0
port 51436 listeners: 0
```

## Evidence
- The staging regression failed on the original code because the uploaded atlas had no face paint. It passed after the change, including the check that the other actor atlas receives its original image.
- Local evidence files in the temporary directory use `survive-face-{baseline,candidate,integrated}-{front,quarter}.png`. The first candidate front view and baseline front view use the same position, camera, zoom and daylight phase. The candidate three-quarter view crossed into dusk. The integrated front view shows that the features remain readable at dusk.
- The current atlas slot and dimensions are unchanged. The paint runs at upload time. No frame-time or GPU memory measurement was made.

## Bugs / Follow-ups
The paint follows the existing mirrored UV chart. It improves eye and brow definition while the mouth is subtle, the head is still faceted, and players share the same silhouette. A matched-lighting three-quarter review and broader character art remain open under ART-01.

## Production readback
PR #1598 shipped as `e5d948e26f3ac54245f4450d108656687695a2d9`. Verified the production actuator identity and HTTP 200 from the public material module containing `paintAdventurerFace`. The matched-lighting three-quarter comparison remains open.
## Document Status
complete

## Project
christopherbell-dev
