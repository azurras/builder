# Survive relicensed to MIT across its repository and the website

## Document Status
ready-for-execution

## Objective
> [!IMPORTANT]
> Every part of christopherbell.dev ships under a permissive license: azurras/survive becomes MIT and the website's Survive adaptation, attribution and served license say MIT instead of GPL-3.0.

## Background
The user asked on 2026-10-11 that their website's license be very permissive. The repository is already MIT, but the `/survive` game is adapted from azurras/survive, which is GPL-3.0 (copyleft), and the site serves that GPL text and labels the port GPL-3.0. Every commit in azurras/survive is authored by Christopher Bell (several of his email addresses), and GitHub lists azurras as the only contributor, so he can relicense it. The user approved relicensing in chat.

## Goals
- azurras/survive's default branch carries the MIT license (AC-1).
- The website labels, serves and allowlists an MIT Survive license instead of GPL-3.0 (AC-2, AC-3).
- The change is verified locally and merged to christopherbell.dev `main` (AC-4).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing the website's own MIT LICENSE | Already the requested permissive license |
| Relicensing vendored jsmediatags (BSD-3-Clause) | Third-party code, already permissive |
| Keeping a redirect from the old GPL license URL | A static license file has no known external links; a stale GPL label would mislead |
| Touching the user's uncommitted work on Survive's local `develop` checkout | Not ours; the Survive change is made in a separate worktree from `origin/master` |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | azurras/survive `master` has an MIT `LICENSE` (Copyright (c) 2016 Christopher Bell) and GitHub reports `MIT` for the repository. |
| AC-2 | christopherbell.dev serves `/licenses/survive-MIT.txt` publicly with the same MIT text, and no longer contains the GPL file, path or GPL-3.0 labels for Survive. |
| AC-3 | The Survive page attribution links "MIT license" to `/licenses/survive-MIT.txt`; SecurityConfig and its test permit exactly that GET path. |
| AC-4 | The website change passes `./gradlew :website:test`, is verified on a locally running candidate with a published test report, and its PR is merged. |

## Inputs
- **Request:** user chat on 2026-10-11, "make sure the license for my website is one that is very permissive", then "yes, relicense".
- **christopherbell.dev:** inspected at `280b3c61` (`main`): `LICENSE`, `SecurityConfig.java` PUBLIC_URLS, `SecurityConfigTest.surviveExposesOnlyItsPageAndExactGameCommands`, `templates/survive.html` line 95, `survive/README.md`, `SurviveWorld.java` class Javadoc, `configuration/security/README.md`, `static/licenses/survive-GPL-3.0.txt`.
- **azurras/survive:** inspected at `24d50be92e1609e6e983b7dda9231bd77777b3d1` (`master`): `LICENSE` (GPL-3.0), README (no license text), commit authors, branch protection (one approving review required, admins not enforced, no required status checks).

## Branch
christopherbell.dev: `relicense-survive-mit` from `main` at `280b3c61`. azurras/survive: `relicense-mit` from `master` at `24d50be`.

## Assumptions
- All Survive authorship belongs to Christopher Bell, as the commit history and contributor list show.
- Nothing outside the site links to `/licenses/survive-GPL-3.0.txt`.

## Open Questions
- azurras/survive `master` requires one approving review, which the author cannot give to their own PR. Merging needs either the user's approval to merge with the admin bypass or another reviewer; this is a user gate under AGENTS.md.

## Design
Replace Survive's GPL `LICENSE` with the standard MIT text dated from the first commit (2016). On the website, rename the served file to `survive-MIT.txt` holding the same MIT text so the page keeps a one-click license link next to its attribution, then update every reference: the PUBLIC_URLS entry, its unit test, the page attribution, the package README, the `SurviveWorld` Javadoc and the security README.

| Alternative | Why not |
|---|---|
| Drop the served file and rely on the site's root LICENSE | The page would lose its visible attribution link, and the upstream notice belongs with the adapted work |
| Keep the old GPL path but change its contents | The path name would mislabel the license |
| Dual-license Survive | Adds complexity; the user asked for a very permissive license |

## Expected Changes
| File or area | Change |
|---|---|
| survive `LICENSE` | GPL-3.0 text replaced by MIT, Copyright (c) 2016 Christopher Bell |
| website `static/licenses/survive-GPL-3.0.txt` → `survive-MIT.txt` | Renamed; contents become the same MIT text |
| website `SecurityConfig.java` | PUBLIC_URLS entry `GET:/licenses/survive-MIT.txt` |
| website `SecurityConfigTest.java` | Asserts the MIT path is public and the old GPL path is not |
| website `templates/survive.html` | Attribution reads "MIT license" with the new link |
| website `survive/README.md`, `SurviveWorld.java` Javadoc, `configuration/security/README.md` | GPL-3.0 wording becomes MIT |

## Task Breakdown
### Task 1 - Relicense azurras/survive to MIT
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `LICENSE` |
| **Symbols** | License text |
| **Inspection** | Read `LICENSE`, README and history at `24d50be` on `origin/master`. |
| **Behavior** | The repository grants MIT permissions; code is unchanged. |
| **Invariants** | The user's uncommitted `develop` work in the local checkout is untouched. |
| **Boundary/API** | GitHub license detection must report MIT. |
| **Effects and failures** | One commit on a branch and a PR; merging needs the review gate. |
| **Tests and evidence** | No runnable application change; GitHub license API readback. |
| **Verification** | `gh api /repos/azurras/survive --jq .license.spdx_id` prints `MIT` after merge. |

### Task 2 - Website serves and labels the MIT license
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None; the user's approval to relicense is the authority, independent of the Survive merge. |
| **Files** | `website/src/main/resources/static/licenses/survive-GPL-3.0.txt`, `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`, `website/src/test/java/dev/christopherbell/configuration/SecurityConfigTest.java`, `website/src/main/resources/templates/survive.html`, `website/src/main/java/dev/christopherbell/survive/README.md`, `website/src/main/java/dev/christopherbell/survive/SurviveWorld.java`, `website/src/main/java/dev/christopherbell/configuration/security/README.md` |
| **Symbols** | `SecurityConfig.PUBLIC_URLS`, `SecurityConfigTest.surviveExposesOnlyItsPageAndExactGameCommands`, `.survive-attribution`, `SurviveWorld` Javadoc |
| **Inspection** | Read each file at `280b3c61`; grep shows no other GPL or license-path references. |
| **Behavior** | GET `/licenses/survive-MIT.txt` returns the MIT text without login; the page links to it. |
| **Invariants** | No other route becomes public; Survive gameplay and APIs are unchanged. |
| **Boundary/API** | The old GPL URL stops being public (intentional). |
| **Effects and failures** | Static file rename; no data or schema change. |
| **Tests and evidence** | `SecurityConfigTest` covers the new and old path; local run shows the file and attribution. |
| **Verification** | `./gradlew :website:test`; local GET of `/licenses/survive-MIT.txt` and `/survive`. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | GitHub license API reports MIT after merge | Not applicable: license text only, no runnable change in Survive |
| AC-2 | `SecurityConfigTest`; grep finds no `GPL` reference for Survive | GET `/licenses/survive-MIT.txt` returns 200 with the MIT text; the old GPL path no longer returns the GPL text |
| AC-3 | `SecurityConfigTest` | GET `/survive` page shows "MIT license" linked to the new path |
| AC-4 | `./gradlew :website:test` | verify-local-app run of the committed candidate, recorded with write-test-report |

- **Regression:** Survive page and API remain reachable; no new public route.

## Rollback or Recovery
Revert the website PR and the Survive PR. No data changes. Licenses already granted under MIT remain valid for copies taken meanwhile, which is the intended outcome.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Survive PR cannot merge without review | High | Ask the user to approve an admin-bypass merge or merge it themselves |
| An external link to the old GPL path breaks | Low | Acceptable; the label would be wrong anyway |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
