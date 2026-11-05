# Survive in-world feedback verification

## Story/Issue
Show action outcomes, gains and combat in the 3D view.

## Branch
codex/survive-world-feedback-20261104 at 95f6f904aed7579dcdcecb120c44520533e91901.

## Pass / Fail
Pass. The final candidate rendered a readable combat encounter on a phone-sized viewport. All 447 JavaScript tests passed.

## Test Cases
1. Check committed build identity and isolated startup.
2. Hunt, attack and flee in the phone-sized 3D view.
3. Stop the candidate and confirm listener cleanup.

## App / Environment
Survive at http://127.0.0.1:64243/survive. Exact test profile, disposable loopback Mongo on port 64242 with database test, and a 390 by 844 browser viewport.

## Local Run Details
Built with Invoke-Gradle.ps1 :website:bootJar. Started and stopped with the repository candidate helpers. The startup helper confirmed readiness and database test. Both ports reported zero listeners after shutdown.

## Data Sent
1. GET /actuator/info.
2. Join as Release Scout. Walk to Hunting grounds. Use the in-world Hunt, Attack and Flee to camp controls.
3. Close the test tab, reset the viewport and run Stop-Candidate.ps1.

## Response Received
1. HTTP 200 with the 95f6f904 build identity.
2. In combat, Grey wolf with 8 health and player health 10/10. Attack showed distinct −2 health and −3 enemy health labels, wolf health 5 and player health 8/10. Screenshot showed the wolf and red marker beside the player. Flee hid the combat HUD and displayed the retreat and two damage in the view.
3. Ports 64243 and 64242 reported zero listeners. The owned Mongo and socket directories were removed.

## Evidence
Final :website:jsTest reported 447 passed and zero failures. Projection tests verify visible enemy placement at four camera angles. Browser screenshots confirmed the compact HUD and visible controls. Candidate identity was recorded through record_run.py.

## Bugs / Follow-ups
Earlier candidate 684d4c83 showed +1 wood and Level up on separate lines after gathering, rejected a camp gather with an in-world notice and no reward, and cleared transient labels after expiry. The final revision only moves the enemy sideways and updates its projection regression. Earlier layout iterations corrected overlapping labels and an oversized combat notice.

## Document Status
complete

## Project
christopherbell-dev
