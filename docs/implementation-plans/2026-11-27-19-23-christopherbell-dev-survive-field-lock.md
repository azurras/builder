# Follow a field target into combat

## Project
christopherbell-dev

## Player experience
F8 selects the nearest visible creature or NPC. Players can lock the camera while approaching, open Commands and start combat with the same target. The lock releases on reset, loss of the target or an explicit unlock. Square Enix documents F8 for NPC targeting and keypad * or the left stick button for target lock. [FFXI basic actions](https://www.playonline.com/ff11newplayer/tips/en/list.html)

## Change and verification
1. Use the visible field labels for F8 and track a locked actor by its route or NPC ID. Carry a lock into combat only when the encounter ID matches.
2. Route the camera shortcut from the canvas and target Commands. Return focus to the world so keyboard or controller movement works after locking.
3. Test hidden and same-species candidates, refreshes, controller input and handoff to the same or a different encounter. Walk from beyond Engage range into combat in desktop Chrome and compare the rendered camera heading with the server-confirmed route.
