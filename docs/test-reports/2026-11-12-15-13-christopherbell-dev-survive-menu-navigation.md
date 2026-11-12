## Story/Issue
Bring cancellation and focus behavior in the Survive Main Menu closer to FFXI under UI-01. [Square Enix controls reference](https://www.playonline.com/ff11newplayer/tips/en/list.html)

## Branch
`codex/survive-menu-navigation` at `e5d9446a8f4f733cd797707e6e54ba12739c687b`.

## Pass / Fail
Local menu regression and desktop Chrome sequence passed. Physical controller verification remains open.

## Test Cases
Open Main Menu with Minus, select Equipment and the Main weapon picker, then send Escape to each focused row. Check which panel closes and where focus returns.

## App / Environment
Exact isolated candidate at 127.0.0.1:62191 and disposable MongoDB at 127.0.0.1:62190/test. Desktop Chrome.

## Local Run Details
Actuator confirmed the candidate build. JavaScript syntax, all 476 JavaScript tests and bootJar passed. The focused Escape regression failed before implementation and passed afterward.

## Data Sent
```text
Minus on canvas, select Equipment and Main, then three Escape events.
```

## Response Received
```text
PASS: Minus opened Main Menu, and successive Escape presses closed the weapon picker, Equipment and Main Menu with focus restored.
port 62191 listeners: 0
port 62190 listeners: 0
```

## Evidence
The Chrome test exercised real DOM focus and panel state with scripted keyboard events. The controller maps B to the same Escape handler. The runtime removed both disposable directories.

## Bugs / Follow-ups
Native form controls keep their own input handling. Broader panel layout, command organization and a physical controller pass remain open.

## Document Status
complete

## Project
christopherbell-dev
