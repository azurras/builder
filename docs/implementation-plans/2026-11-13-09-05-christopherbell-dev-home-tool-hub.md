# Make the homepage a public tools hub

## Document Status

complete

## Objective

> [!IMPORTANT]
> Put the public tools on the homepage with a direct link to each destination.

## Background

The homepage at ff051791 leads with the Void feed and polls for active posts. The Tools menu already identifies six destinations available to all visitors.

## Goals

- Make all six public tools discoverable on the homepage (AC-1).
- Keep admin and file-sharing tools out of the homepage and retain a secondary Void link (AC-2).
- Deliver through verified merge and production readback (AC-3).

## Non-Goals

| Outside scope | Reason |
| --- | --- |
| Tool authorization or feature behavior | This change concerns discovery on the homepage. |
| Tool menus on other routes | Existing access and navigation continue there. |

## Acceptance Criteria

| ID | Done when |
| --- | --- |
| AC-1 | The responsive homepage links to Raising Canes Box Index, Website Monitor, Survive, VIN Decoder, What's For Lunch, and ZIP Coordinates. |
| AC-2 | The homepage menu and cards omit privileged destinations even for admin accounts. The Void has a secondary link and the homepage stops polling its feed. |
| AC-3 | The tested change passes required CI, merges, and is served in production. |

## Inputs

- User request for a tools-led homepage excluding admin and file-sharing tools.
- Current origin/main ff051791, including index.html, nav.js, main.css, ToolsViewController, SecurityConfig, and the homepage route and navigation tests.

## Branch

codex/home-tool-hub-20261113 from origin/main ff051791.

## Assumptions

- The signed-out Tools menu defines the public tool inventory. Music is capability-gated and remains off the homepage.

## Open Questions

None.

## Design

Render a responsive grid of direct links on the server so the homepage works before scripts load. Give each tool a short description. Keep the Void as a secondary link and restrict the homepage's shared Tools menu to its public entries.

| Alternative | Tradeoff |
| --- | --- |
| Generate the cards in JavaScript from the Tools menu | A shared list would reduce drift, with the cost of delaying all homepage links until JavaScript initializes. |

## Expected Changes

| File or area | Change |
| --- | --- |
| templates/index.html and static/css/main.css | Replace the Void hero and live rail with the tool grid and secondary Void link. |
| static/js/components/nav.js | Show public tools only in the homepage Tools menu. |
| static/js/home.js and its two JS tests | Remove the retired active-post polling and its dedicated tests. |
| ViewControllerTest and nav-messages-link.test.js | Assert the public homepage destinations and restricted navigation. |
| Static CSS and JS READMEs | Document the homepage layout and menu behavior. |

## Task Breakdown

### Task 1 - Render and verify the public tools hub

Required skill: write-chris-street-style-code

| Contract | Detail |
| --- | --- |
| **Dependencies** | None. |
| **Files** | The index.html template, main.css, nav.js, home.js, adjacent static READMEs, ViewControllerTest.java, and affected JS tests under website/src. |
| **Symbols** | Homepage main content, home-page layout selectors, toolsMenuItems, and the homepage route assertion. |
| **Inspection** | At ff051791 the homepage loads home.js, main.css owns the Void hero, toolsMenuItems adds optional Music and admin or shared links, and existing tests exercise the homepage and navigation menu. |
| **Behavior** | The homepage lists the six public tools with a secondary Void link. |
| **Invariants** | Only public tools are offered on the homepage. Other routes keep their existing menus and access. |
| **Boundary/API** | Existing GET routes and session behavior. |
| **Effects and failures** | Direct links render before scripts load. The retired homepage poll has no remaining caller. |
| **Tests and evidence** | Adapt the existing route and menu tests to witness old behavior fail and new behavior pass. |
| **Verification** | Run the view test and JS suite, build the committed candidate, then verify its identity and rendered homepage on loopback. |

## Test Plan

| AC | Native check | Local runtime check |
| --- | --- | --- |
| AC-1 | ViewControllerTest checks the six direct links. | Inspect rendered cards at desktop and mobile sizes and check the six destinations. |
| AC-2 | ViewControllerTest checks the Void link and absence of the polling mount. Navigation JS tests exercise homepage and other-route menus. | Exercise the homepage navigation in a browser and verify the live feed script is absent. |
| AC-3 | Review the full diff and wait for required CI. | Use verify-local-app with the committed packaged candidate and isolated test-profile MongoDB, then publish a runtime report before creating the PR. Repeat affected checks for runtime changes and read back production after merge. |

## Rollback or Recovery

Revert the homepage PR through the normal reviewed deployment pipeline if needed.

## Risks

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| Cards and menu drift apart | Low | Verify all six rendered destinations against the public navigation list. |

## Implementation Log

No entries yet.

## Outcome

> [!TIP]
> The public tools hub is live. Production liveness and readiness reported UP, and the homepage served the six public cards and secondary Void link.

| AC | Result | Evidence |
| --- | --- | --- |
| AC-1 | Met | Chrome verified six cards at 1440 and 390 pixels wide, and each tool returned HTTP 200. [Runtime report](../test-reports/2026-11-13-09-13-christopherbell-dev-home-tool-hub.md). |
| AC-2 | Met | The signed-in admin homepage menu listed only public tools. The homepage had a secondary Void link and made no Void feed requests. [Runtime report](../test-reports/2026-11-13-09-13-christopherbell-dev-home-tool-hub.md). |
| AC-3 | Met | All PR checks passed, and main CI succeeded. Production reported build 9e89eeee746b267a7a06be9d6f9ef44b5ac82be3 and returned the new homepage with HTTP 200. [Pull request](https://github.com/azurras/christopherbell.dev/pull/1613). |

## Project

christopherbell-dev

## Plan Format

task-contract-v2
