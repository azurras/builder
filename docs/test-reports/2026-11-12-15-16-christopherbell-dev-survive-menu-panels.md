## Story/Issue
Keep the Main Menu categories visible while the selected section opens in its own panel under UI-01.

## Branch
`codex/survive-menu-panels` at `894546f2e13ece89198ada6c5b9a311c49b58490`, stacked on #1604.

## Pass / Fail
Desktop layout and cancellation passed. Narrow viewport and physical controller coverage remain open.

## Test Cases
Open Main Menu, select Map, verify its bounds beside the categories, switch to Equipment, open the weapon picker, and back out three times.

## App / Environment
Desktop Chrome, isolated candidate 127.0.0.1:57056 and MongoDB 127.0.0.1:57055/test.

## Local Run Details
Verified actuator build identity, JavaScript syntax, all 477 JavaScript tests and bootJar.

## Data Sent
```text
Minus, Map, Equipment, Main, Escape three times.
```

## Response Received
```text
PASS: the map opens beside visible categories, and switching to Equipment closes it.
PASS: successive Escape presses closed the weapon picker, Equipment and Main Menu with focus restored.
port 57056 listeners: 0
port 57055 listeners: 0
```

## Evidence
Inspected the final desktop Map capture. The first capture exposed the view toggle below the menu border. The final build moves category descriptions inside their panels and keeps the view toggle inside the category frame.

## Bugs / Follow-ups
Items and Equipment still need deeper browsing, and the narrow layout and physical controller need direct playtesting.

## Document Status
complete

## Project
christopherbell-dev
