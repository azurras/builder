## Story/Issue
Show the current enmity leader during a shared Survive fight under COM-02.

## Branch
`codex/survive-enemy-attention` at `9eef533220f67a76b35356896286b2b0a53f0ab4`.

## Pass / Fail
Initial server and desktop browser verification passed. Main integration and release remain pending.

## Test Cases
Verify that two fighters see the same leader after damage, with self and ally labels. Check that observers and the remaining solo fighter receive no label. Verify the renderer clears an absent value.

## App / Environment
Two desktop Chrome contexts, isolated candidate at 127.0.0.1:60635 and MongoDB 127.0.0.1:60634/test.

## Local Run Details
Actuator matched the candidate. Targeted Survive Java tests, Checkstyle, 477 JavaScript tests and bootJar passed. The browser used normal UI movement and party controls, with authenticated combat commands to isolate the enmity leader.

## Data Sent
```text
Form a party and join one bear fight. Use Heavy Strike, stop automatic strikes, then compare both private snapshots and vitals panels.
```

## Response Received
```text
PASS: the targeted fighter saw You, and their ally saw Impact Scout in the vitals panel.
port 60635 listeners: 0
port 60634 listeners: 0
```

## Evidence
The initial browser attempt asserted a fixed counter target after a second attack. The counter went to the attacker instead. The corrected scenario isolates the opener and checks current enmity before another attack changes it. Both runtimes closed their listeners and removed their disposable directories.

## Bugs / Follow-ups
The HUD shows current attention. Ability-driven threat, healing threat and independent enemy attack timing remain open.

## Desktop menu integration
Candidate `1531a119c2250eed7c247937e26da657d25629ce` includes main `2d9f6e91`. Survive Java tests, Checkstyle, JavaScript tests and bootJar passed. Two desktop Chrome contexts on the exact build at 127.0.0.1:57795 agreed on the bear's current enmity leader and showed the correct self and ally labels. Both listeners at 57795 and 57794 closed and disposable directories were removed.


## Shared facing verification
Candidate `27e5bfa4a080ff276ed39f0cea90db30de4feee1` passed Survive Java tests, Checkstyle, 480 JavaScript tests and bootJar. The heading regression covers the local fighter, an identified remote fighter and a missing remote pose. Two desktop Chrome sessions at 127.0.0.1:53976 agreed on the attention target's survivor ID and confirmed the remote target pose was available. Both screenshots show the bear turning toward the scout's side, but the scout is obscured from the ally camera and overlaps the bear's muzzle in the local view. A clear separated-fighter comparison remains open. Both listeners at 53976 and 53975 closed and disposable directories were removed.


## Document Status
complete

## Project
christopherbell-dev
