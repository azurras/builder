# Keep a selected island target through combat

## Project

christopherbell-dev

## Player experience

A player can click the visible body or name of a roaming animal, see which animal is selected, Check it and Engage when close enough. The same creature stays selected when Hunt or aggro starts a field encounter and when Disengage stops auto-attacks. Dragging turns the camera. Tab and Shift+Tab cycle through visible targets in both directions. Escape lets keyboard users leave the canvas. The baseline control reference is the [official FFXI basic actions guide](https://www.playonline.com/ff11newplayer/tips/en/list.html).

## Implementation

1. Return the route ID and world pose of the current solo or party animal in the game snapshot. Reuse the field encounter returned by movement.
2. Hand off the roaming model and label to combat using that identity. Exercise both orders of arrival of game and movement replies and keep other animals of the same species visible.
3. Pick the visible mesh on a primary click using one depth-tested pixel from the rendered frame. Distinguish a click from a drag and apply the same commands as selecting by label. Show the field target ring immediately.
4. Verify a mouse click on the hog itself in desktop Chrome, then Engage and Disengage without clicking another target. Run the native build and record the candidate and release.

## Scope

The island server continues to own encounter claims, range, health, attacks and respawn timing. The text adventure retains its non-spatial encounters.
