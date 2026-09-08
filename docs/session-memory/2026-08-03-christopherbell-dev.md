# 2026-08-03 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/session-memory/2026-08-03-wfl-archived-session-recovery.md](#source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md)
- [docs/session-memory/2026-08-03-wfl-thumbs-voting.md](#source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md)
- [docs/specs/2026-08-03-wfl-archived-session-recovery.md](#source-docs-specs-2026-08-03-wfl-archived-session-recovery-md)
- [docs/specs/2026-08-03-wfl-thumbs-voting.md](#source-docs-specs-2026-08-03-wfl-thumbs-voting-md)
- [docs/work-closures/2026-08-03-wfl-archived-session-recovery-closure.md](#source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md)
- [docs/work-closures/2026-08-03-wfl-thumbs-voting.md](#source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md)
- [docs/work/2026-08-03-wfl-archived-session-recovery.md](#source-docs-work-2026-08-03-wfl-archived-session-recovery-md)
- [docs/work/2026-08-03-wfl-thumbs-voting.md](#source-docs-work-2026-08-03-wfl-thumbs-voting-md)

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md"></a>
## 2026-08-03 | session-memory | 2026-08-03 - WFL Archived Session Recovery

Original source: `docs/session-memory/2026-08-03-wfl-archived-session-recovery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `75f5aa470b74b22f2379374984d451cfbfc376418315624787196a1b37d8a1cb`.

<!-- migrated-source: docs/session-memory/2026-08-03-wfl-archived-session-recovery.md -->
<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--2026-08-03---wfl-archived-session-recovery"></a>
### 2026-08-03 - WFL Archived Session Recovery

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--2145---wfl-archived-session-recovery"></a>
#### 21:45 - WFL Archived Session Recovery

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--request"></a>
##### Request

Fix the production What's For Lunch failure "This lunch session is archived and cannot be changed" through the complete Builder delivery loop. Preserve archived history, recover automatically from saved archived state, retain active shared-session behavior, and complete testing, PR/CI, merge, deployment, production verification, and durable closeout.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--project-context"></a>
##### Project Context

- Hub: `C:\Users\Christopher\Developer\builder`.
- Spoke: `azurras/christopherbell.dev`.
- The authoritative checkout at `A:\Projects\christopherbell.dev` was dirty/stale and was not modified.
- Implementation used isolated worktree `A:\Projects\christopherbell.dev-worktrees\wfl-archived-session-recovery` and private Gradle home `A:\Projects\christopherbell.dev-gradle-homes\wfl-archived-session-recovery`.
- Production is native Windows through automatic services `MongoDB`, `ChristopherBellDev`, and `cloudflared`; the SYSTEM auto-deploy pipeline is the supported release path.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--work-completed"></a>
##### Work Completed

- Added `createSessionRecoveryController` to the WFL browser module.
- Implicit saved-session restoration now accepts only session details whose `active` value is not false; archives clear saved/current state and return to normal initialization.
- Explicit session links now read participant state first and use join only after a 404, allowing retained participant archives to render without an expired join mutation.
- Archived new-pick actions route through `loadSoloSession({ forceNew: true })` instead of shared restaurant reset.
- Archived `Try 3 more` remains enabled, archived session voting remains disabled, active guests remain unable to replace shared picks, and archived polling does not start.
- Updated WFL JavaScript documentation and added seven dependency-injected behavior tests.
- Feature commit `255df4d101662b56b18f618fd3931e538f881b75` was pushed in branch `codex/wfl-archived-session-recovery`.
- PR [#1350](https://github.com/azurras/christopherbell.dev/pull/1350) passed every required check and merged by squash as `9c587103cb7f7df2ab52ed3e232f1ca67660fd6e`.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--decisions"></a>
##### Decisions

- Keep the backend `WFL_SESSION_EXPIRED` mutation conflict, 24-hour active lifetime, 30-day archive retention, and immutable archive semantics unchanged.
- Make recovery client-owned because the server lifecycle was correct and the browser was attempting the wrong transition.
- Read an explicit session as a participant before joining: active nonparticipants still join after the participant-only GET returns 404, while archived participants receive read-only history.
- Preserve the protected production ACL after non-elevated `prod.cmd status` and `auto-status` were denied; verify deployment through listener rotation, exact live asset content, UI behavior, MongoDB state, endpoints, and service state instead.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--validation"></a>
##### Validation

- RED first: the original four focused tests failed because the controller export was absent.
- Focused final tests: 7 passed, 0 failed.
- Full JavaScript: 343 passed, 0 failed.
- Final `:website:check`: BUILD SUCCESSFUL in 3m 4s, 21 tasks, including Java, JavaScript, static/package checks, and Windows/Pester verification.
- Packaged candidate on port 8094 used six synthetic restaurants, ZIP 78701, a synthetic member, and a disposable MongoDB database. Browser acceptance proved active reset, implicit fallback, explicit archive readability, new session creation, direct archived refresh behavior, and archive immutability. Browser warning/error logs were empty.
- Candidate PID 65840 stopped; port 8094 freed; disposable database dropped and confirmed absent; production readiness stayed HTTP 200.
- GitHub checks passed: Linux, macOS, Windows, CodeQL actions, CodeQL Java/Kotlin, CodeQL JavaScript/TypeScript, and Dependency Review.
- SYSTEM production deployment ran from 21:33:57 through cutover at 21:39:41 America/Chicago. Listener rotated from PID 74080 to PID 63840; the served WFL asset changed from `HasRecovery=False` to `HasRecovery=True`.
- Signed-in production plain `/wfl` rendered `Share your location`; explicit retained archive `09c38747-2cea-4c5c-b6f8-18535d993b19` rendered `Archived lunch session`, historical picks, disabled session votes, and enabled `Try 3 more`. Returning to plain `/wfl` again showed the clean location prompt, and browser warnings/errors were empty.
- Production archive remained revision 143 with the same restaurant IDs and lifecycle deadlines.
- Local liveness/readiness/WFL, apex WFL, and `www` WFL returned HTTP 200. All three native services remained Running/Automatic.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--durable-artifacts"></a>
##### Durable Artifacts

- Work: `docs/work/2026-08-03-wfl-archived-session-recovery.md`.
- Spec: `docs/specs/2026-08-03-wfl-archived-session-recovery.md`.
- Plan: `docs/implementation-plans/2026-08-03-wfl-archived-session-recovery.md`.
- Test report: `docs/test-reports/2026-08-03-wfl-archived-session-recovery-test-report.md`.
- Closure: `docs/work-closures/2026-08-03-wfl-archived-session-recovery-closure.md`.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--current-state"></a>
##### Current State

The defect is fixed, merged, deployed, and production-verified. The production browser tab was left on clean `https://www.christopherbell.dev/wfl`. The isolated host-managed worktree remains clean and preserved; no running candidate or disposable database remains.

<a id="source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md--follow-ups"></a>
##### Follow-ups

None required for this defect.

<!-- /migrated-source: docs/session-memory/2026-08-03-wfl-archived-session-recovery.md -->

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md"></a>
## 2026-08-03 | session-memory | 2026-08-03 WFL Thumbs Voting

Original source: `docs/session-memory/2026-08-03-wfl-thumbs-voting.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `72e42708ba1d4fc59c7e886d9e597955e63b0ba9ccd9f73203e23ec21d4a2f34`.

<!-- migrated-source: docs/session-memory/2026-08-03-wfl-thumbs-voting.md -->
<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--2026-08-03-wfl-thumbs-voting"></a>
### 2026-08-03 WFL Thumbs Voting

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--1919---completed-wfl-thumbs-voting-delivery"></a>
#### 19:19 - Completed WFL thumbs voting delivery

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--request"></a>
##### Request

Replace What's For Lunch 1-5 restaurant ratings with thumbs up/down, converting 3-5 to up and 1-2 to down. Make higher-rated/approved restaurants appear more often in three-restaurant selection, lower-approved restaurants less often, apply Void styling to the WFL page and restaurant profiles, and keep restaurant profiles indexable.

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--project-context"></a>
##### Project Context

Work was coordinated from `C:\Users\Christopher\Developer\builder` into `azurras/christopherbell.dev`. The authoritative checkout at `A:\Projects\christopherbell.dev` was dirty and preserved. Implementation used the isolated worktree `A:\Projects\christopherbell.dev-worktrees\wfl-thumbs-voting` from refreshed `origin/main` `363bb986581c4d20df3434154844807ce88701e4`, with private Gradle home `A:\Projects\christopherbell.dev-gradle-homes\wfl-thumbs-voting`.

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--work-completed"></a>
##### Work Completed

- Added immutable Mongo migration V013 with a complete preflight pass before any conversion writes.
- Replaced rating domain/models/repositories/services/controllers/session behavior with `UP`/`DOWN` votes and strict legacy-field rejection.
- Added vote aggregates, Top Liked ranking, approval weighting, vote summaries, SSR/JSON-LD, redirects, sitemap updates, thumb controls, race-safe list/profile mutations, Void styling, and ownership documentation.
- Updated Windows production deployment to restore the live backup into a bounded candidate database, validate V013 there, clean it, stop the old writer, and remain forward-only after live migration starts.
- Reviewed the complete branch and resolved all findings.
- Published PR #1349, passed all required CI/security checks, squash-merged as `3b9ee44ba29627c3595b8aebc16612cc2065a885`, and deployed that exact release.

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--decisions"></a>
##### Decisions

- Convert 3-5 to `UP`, 1-2 to `DOWN`; reject numeric clients immediately.
- Keep `whatsforlunch_ratings` and the unique restaurant/account index.
- Use raw approval then vote count then restaurant ID for Top Liked.
- Use adjusted approval `(up + 1.5) / (up + down + 3)` and selection weights 0.35 at zero approval, 1.0 neutral, and 2.0 at full approval.
- Show `NN% liked · U up · D down`; show `No votes yet` at zero.
- Preserve canonical/indexable restaurant profiles and encode approval JSON-LD on a 0-100 scale.
- Use an approved forward-only outage boundary; never restart the old binary after live V013 begins.

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--validation"></a>
##### Validation

- Final Pester production subset: 92/92.
- Final Gradle `:website:check`: `BUILD SUCCESSFUL` in 3m58s; 1,656 Java tests and 336 JavaScript tests passed.
- Alternate candidate on 8094: invalid legacy data failed before writes; valid fixture converted 6 up/3 down and retained indexes; strict API, redirect, sitemap, SEO, weighting sample, authenticated desktop, mobile, persistence, and console checks passed.
- GitHub: Ubuntu, macOS, Windows, Dependency Review, and all CodeQL analyzers passed.
- Production: release junction `3b9ee44b`; 8080 rotated PID 59036 to 74080; readiness/liveness 200; all services running.
- Live Mongo: V013 applied with exact checksum; 87 binary votes, 53 up, 34 down, zero legacy/invalid documents, unique index retained.
- Public/browser: Top Liked, redirect, sitemap, voted/zero/missing profiles, Void WFL/profile rendering, canonical/noindex/JSON-LD, horizontal fit, and empty warning/error console verified.

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--current-state"></a>
##### Current State

- Builder main already contains the approved spec, plan, work ledger, and local test report checkpoint at `ab2cd78`; this closure update will add completed statuses, closure, and session memory.
- Spoke PR #1349 is merged; the remote feature branch was deleted by the merge command. The local isolated worktree and `.superpowers/sdd/2026-08-03-wfl-thumbs-voting` evidence remain for audit.
- Production is serving the merged release and the disposable candidate databases were removed. The production backup and previous release remain under normal protected retention.

<a id="source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md--follow-ups"></a>
##### Follow-ups

No required follow-up remains. Do not edit V013 or its checksum; append a new migration for future vote schema changes. Preserve normal backup/release retention and remove the isolated worktree only during an intentional cleanup pass.

<!-- /migrated-source: docs/session-memory/2026-08-03-wfl-thumbs-voting.md -->

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md"></a>
## 2026-08-03 | specs | WFL Archived Session Recovery

Original source: `docs/specs/2026-08-03-wfl-archived-session-recovery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `5e965badb9250c855616417d6346d5551cc042c56c59eb1a762c9344bfda5a70`.

<!-- migrated-source: docs/specs/2026-08-03-wfl-archived-session-recovery.md -->
<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--wfl-archived-session-recovery"></a>
### WFL Archived Session Recovery

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--purpose"></a>
#### Purpose

Prevent the What's For Lunch browser from restoring an archived shared session as the caller's current mutable session. Preserve archived sessions as readable history while making requests for new picks leave the archived context and begin a fresh flow instead of sending a mutation that the server must reject.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--background"></a>
#### Background

WFL shared sessions are mutable for 24 hours and remain readable for 30 additional days before MongoDB TTL deletion. The browser stores the last member session ID under an account-scoped local key. On a normal `/wfl` visit, `loadStoredMemberSession()` fetches that ID and currently treats any successful session response as reusable, including details with `active: false`.

The page therefore sets an archived detail as `activeSession`. Later, `loadNearbyPicks()` branches on the presence of `activeSession` rather than its active state and calls the shared-session restaurant-reset endpoint. The mutation store correctly rejects the expired session, and the API returns HTTP 409 with code `WFL_SESSION_EXPIRED` and description “This lunch session is archived and cannot be changed.”

Production evidence on 2026-08-03 confirmed one retained archived session and one active session. The server lifecycle, immutable archive, and conflict response are correct; the client recovery path is wrong.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--goals"></a>
#### Goals

1. Never reuse an archived session restored implicitly from saved browser state.
2. Preserve explicit archived-session links as readable historical views.
3. Turn a request for new picks from an archived view into a fresh solo/new-session flow.
4. Guarantee the browser does not send join, vote, or restaurant-reset mutations for a session detail already known to be archived.
5. Preserve active shared-session behavior, archive retention, server conflict semantics, voting, favorites, filters, location, and weighted restaurant selection.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--non-goals"></a>
#### Non-Goals

- Do not reactivate, extend, delete early, or modify archived server documents.
- Do not change the 24-hour active lifetime or 30-day archive lifetime.
- Do not weaken the backend `WFL_SESSION_EXPIRED` conflict or mutation-store time predicate.
- Do not migrate production session data.
- Do not redesign the WFL control panel, session sharing, or history UI.
- Do not change restaurant thumb voting or selection weights.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--implicit-saved-session-restoration"></a>
##### Implicit saved-session restoration

- `loadStoredMemberSession()` must consider a fetched session reusable only when its public detail is active.
- When the fetched detail has `active: false`, the browser must clear the account-scoped saved session ID, clear the client `activeSession`, stop session polling, and return control to normal `/wfl` initialization.
- Normal initialization must then show the location prompt or load fresh picks using the caller's available location/ZIP state. It must not render the archived session as the current default.
- Missing, forbidden, or otherwise failed stored-session fetches must retain the existing clear-and-fallback behavior.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--explicit-archived-session-links"></a>
##### Explicit archived-session links

- Navigating to `/wfl?session=<archived-id>` must continue to load and render the archived session read-only when the caller is a participant.
- The archived heading, historical restaurants, votes, participants, link, and `active: false` state must remain visible.
- Session vote controls must remain disabled and no automatic mutation may be attempted.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--starting-fresh-from-an-archive"></a>
##### Starting fresh from an archive

- When a user requests new picks through refresh, applying filters, or changing location while `activeSession.active === false`, the browser must first leave the archived client context.
- Leaving the archive must clear the saved member-session ID, clear `activeSession`, stop polling, and remove the `session` query parameter.
- The request must continue through the normal solo picker using the selected filters and current ZIP/location behavior.
- If the signed-in picker returns exactly three restaurants, the existing behavior may create and save a new active shared session; it must never update the archived document.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--active-session-compatibility"></a>
##### Active-session compatibility

- When `activeSession.active !== false`, refresh/apply-filter behavior must continue to call the existing host-only shared-session restaurant reset with the current revision.
- Active session polling, votes, favorites, share links, and conflict handling must remain unchanged.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--failure-behavior"></a>
##### Failure behavior

- Genuine server 409 responses remain visible when an active-looking client races with expiry or another mutation.
- Location denial, empty results, authentication failures, and unexpected network/server errors must continue through existing error rendering.
- Recovery must not silently swallow unexpected fetch failures beyond the existing stored-session fallback contract.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--proposed-approach"></a>
#### Proposed Approach

Create one small browser-owned state transition that leaves an archived session without touching the server. Use it in two places:

1. After an implicitly restored session is fetched, reject `active: false` as a reusable saved session and fall back to normal initialization.
2. Before the nearby-picks branch, detect `activeSession.active === false`, run the local archive-exit transition, and continue into the solo picker rather than the shared-session reset.

Keep explicit URL loading unchanged so archives remain readable. Keep all server code unchanged because it already enforces the required immutable lifecycle.

The implementation should expose the smallest testable JavaScript boundary needed to prove the transition and orchestration. It must not add configuration knobs or broaden the API.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--files-and-modules"></a>
#### Files and Modules

- `website/src/main/resources/static/js/whats-for-lunch.js`: saved-session restoration, archive-exit state transition, and nearby-picks orchestration.
- `website/src/test/js/whats-for-lunch.test.js`: regression coverage using the real exported browser orchestration boundary and complete session detail fixtures.
- `website/src/main/resources/static/js/README.md` or the WFL feature README only if the existing documented session lifecycle requires a clarification.
- Server session services, mutation store, repository, model, and retention configuration should remain unchanged.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--automated-redgreen-evidence"></a>
##### Automated RED/GREEN evidence

- Add a failing JavaScript test proving an archived saved session is not retained as the current session and its saved ID is cleared.
- Add a failing JavaScript test proving a new-picks request from an explicit archived detail runs the solo picker and never invokes the shared-session reset request.
- Preserve a passing test proving an active session still uses the shared-session reset path.
- Run the focused Node test file, `node --check` on the touched module, full `:website:jsTest`, and full `:website:check` using a private Gradle home.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--runtime-evidence"></a>
##### Runtime evidence

- Start the packaged merged candidate on a non-8080 port against a disposable database with one active and one archived WFL session.
- In an authenticated browser, prove a normal `/wfl` visit does not restore the archived saved session.
- Open an explicit archived link and prove it remains readable.
- Apply filters or request new picks and prove the browser leaves the archive, obtains fresh picks, and does not receive `WFL_SESSION_EXPIRED`.
- Verify active shared-session refresh still mutates the current session successfully.
- Confirm browser console errors/warnings are empty and production port 8080 remains untouched until merge.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--publication-and-production"></a>
##### Publication and production

- Open a ready PR, pass Linux/macOS/Windows CI, Dependency Review, and all CodeQL analyzers, then squash merge.
- Deploy through the protected native Windows path.
- Verify listener rotation, readiness/liveness `UP`, exact current asset version, live `/wfl` recovery in a real browser, service state, and no new archived-session mutation error during the acceptance window.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--rollback-and-recovery"></a>
#### Rollback and Recovery

The change is browser-only and does not alter MongoDB data or server contracts. Before production deployment, rollback is the normal branch/PR process. After deployment, the previous application release remains compatible with the unchanged session schema, so normal application rollback remains available if necessary.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--risks"></a>
#### Risks

- Clearing any inactive detail too broadly could hide an explicitly opened archive. Mitigation: apply automatic discard only to the implicit stored-session path; explicit URL loading remains unchanged.
- Falling through with stale `activeSession` could still route into reset. Mitigation: make archive exit clear state before branch selection and prove the reset dependency is never called.
- A session may expire after a client check. Mitigation: retain the backend time predicate and visible HTTP 409 race handling.
- Tests that assert only helpers could miss orchestration. Mitigation: exercise the real exported flow boundary with dependency seams and assert observable calls/state.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--acceptance-criteria"></a>
#### Acceptance Criteria

- A normal `/wfl` visit never restores an archived saved session as current.
- An explicit archived URL remains readable and immutable.
- Refresh/apply filters/location from an archive starts a fresh flow without an expired-session mutation request or error.
- Active session reset behavior remains unchanged.
- Focused, full JavaScript, aggregate repository, alternate-port browser, CI, and production verification all pass.

<a id="source-docs-specs-2026-08-03-wfl-archived-session-recovery-md--open-questions"></a>
#### Open Questions

None. The user approved the automatic recovery approach on 2026-08-03.

<!-- /migrated-source: docs/specs/2026-08-03-wfl-archived-session-recovery.md -->

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md"></a>
## 2026-08-03 | specs | What's For Lunch Thumbs Voting

Original source: `docs/specs/2026-08-03-wfl-thumbs-voting.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `2c4a4a54cdf50082ab8cec479c52a61625afb93b96664cdd90a2aa063202e901`.

<!-- migrated-source: docs/specs/2026-08-03-wfl-thumbs-voting.md -->
<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--whats-for-lunch-thumbs-voting"></a>
### What's For Lunch Thumbs Voting

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--purpose"></a>
#### Purpose

Replace the What's For Lunch 1–5 restaurant rating system with a binary thumbs-up/thumbs-down vote system. Convert every valid stored rating deterministically, expose only vote-based API and UI contracts, preserve useful public ranking and structured data, and keep higher-approval restaurants more likely to appear in weighted lunch selections.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--background"></a>
#### Background

The current WFL domain stores one integer rating from 1 through 5 per account and restaurant in `whatsforlunch_ratings`. Public restaurant details expose `ratingSum` and `ratingCount`; authenticated details also expose `myRating`. The picks page, restaurant profiles, Favorites, and Top 10 Rated render star-scale summaries and controls. Mongo aggregation ranks Top 10 Rated by average rating and count. Daily and shared-session restaurant selection use a confidence-adjusted 1–5 rating weight.

The user approved a complete binary replacement with these decisions:

- Existing ratings `3`, `4`, and `5` become thumbs up.
- Existing ratings `1` and `2` become thumbs down.
- Top 10 Rated becomes Top 10 Liked.
- Public summaries show approval percentage plus up/down counts.
- Lunch selection uses smoothed weighting so one early vote does not dominate.
- Old numeric rating writes are rejected immediately rather than translated.
- Persisted data receives one clean versioned migration rather than indefinite dual-schema reads.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--goals"></a>
#### Goals

1. Store one `UP` or `DOWN` vote per account and restaurant.
2. Convert every valid existing 1–5 rating without losing account, restaurant, or timestamp identity.
3. Replace numeric rating request and response fields with vote-based contracts.
4. Show approval percentage, thumbs-up count, and thumbs-down count on every WFL restaurant surface.
5. Rename the public leaderboard to Top 10 Liked and rank it deterministically.
6. Use binary approval to make better-liked restaurants more frequent and disliked restaurants less frequent in both daily and shared-session picks.
7. Preserve server-rendered indexable restaurant profiles and safe structured data.
8. Deliver through regression-first implementation, local migrated-database/browser testing, PR/CI, protected production deployment, and production verification.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--non-goals"></a>
#### Non-Goals

- No change to Favorites, shared-session participant voting, restaurant import, location resolution, daily-pick count, or nearby-search radius rules.
- No permanent compatibility support for 1–5 write payloads.
- No vote deletion or neutral vote state after a member has voted; a member may change between `UP` and `DOWN`.
- No collection rename. The existing `whatsforlunch_ratings` collection and unique restaurant/account index remain to reduce migration risk.
- No change to the approved Void visual system beyond replacing star controls and score language with thumb controls and vote summaries.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--domain-and-persistence-requirements"></a>
#### Domain and Persistence Requirements

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--vote-model"></a>
##### Vote model

- Production code uses vote terminology, including `RestaurantVote`, vote requests, vote summaries, and vote services/repositories.
- Each document retains the existing `_id`, `restaurantId`, `accountId`, `createdOn`, and `lastUpdatedOn` values.
- The persisted binary field is `vote` with exactly `UP` or `DOWN`.
- The legacy `rating` field is absent after migration.
- The existing compound unique index on `restaurantId` plus `accountId` remains authoritative.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--v013-migration"></a>
##### V013 migration

- Add the next immutable application migration after V012.
- Before writing, validate that every document requiring conversion has a numeric integer rating from 1 through 5.
- If any legacy document is malformed, fail the migration without guessing, deleting, or partially converting data.
- Convert `3–5` to `vote: "UP"` and `1–2` to `vote: "DOWN"` in bounded, stable `_id` batches.
- Remove `rating` from each converted document.
- Treat already-converted valid vote documents as idempotently complete for retry safety.
- Reject documents that contain contradictory valid `rating` and `vote` values.
- Record a fixed migration checksum and test the migration against mixed legacy/already-converted, empty, malformed, and boundary datasets.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--api-requirements"></a>
#### API Requirements

- Add vote-only member write endpoints using request value `vote: "UP" | "DOWN"`.
- The provider-ID-safe request keeps `restaurantId` in JSON rather than requiring it in the path.
- Remove the numeric rating paths from browser API routing and do not accept numeric values on the new endpoint.
- Requests containing `rating`, numeric `vote`, unknown strings, null, or missing vote return the established stable invalid-request HTTP 400 envelope.
- Authenticated callers may change an existing vote by sending the other value.
- Sending the already-selected value is idempotent and returns current aggregate/personal state.
- Public restaurant details expose `upVotes`, `downVotes`, and `voteCount`.
- Authenticated restaurant details additionally expose `myVote`; anonymous responses omit or null personal state consistently with the existing privacy boundary.
- Legacy response fields `ratingSum`, `ratingCount`, and `myRating` are removed.
- Existing authentication, CSRF, rate limiting, and restaurant-not-found boundaries remain unchanged.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--public-summary-and-leaderboard-requirements"></a>
#### Public Summary and Leaderboard Requirements

- The shared summary format is `83% liked · 10 up · 2 down`.
- Approval percentage is the rounded whole-number value `100 * upVotes / voteCount`.
- Zero votes display `No votes yet`; code never divides by zero or fabricates a percentage.
- Top 10 Rated becomes Top 10 Liked in visible headings, navigation, documentation, accessibility labels, canonical metadata, and sitemap membership.
- The canonical page route is `/wfl/top-liked` and the canonical API resource is `/top-liked`.
- `/wfl/top-rated` permanently redirects to `/wfl/top-liked` to preserve public links and search equity.
- The old numeric rating write endpoints do not receive compatibility translation.
- Top 10 Liked ordering is:
  1. raw thumbs-up percentage descending;
  2. total vote count descending;
  3. restaurant ID ascending.
- Restaurants with zero votes are excluded from Top 10 Liked.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--selection-weighting-requirements"></a>
#### Selection Weighting Requirements

- Daily picks and shared-session restaurant selection consume the same immutable vote summary type.
- Unvoted restaurants have neutral selection weight `1.0`.
- Apply a neutral three-vote prior:

```text
adjustedApproval = (upVotes + 1.5) / (upVotes + downVotes + 3)
```

- Convert adjusted approval into the existing approved frequency range with piecewise linear interpolation:
  - adjusted `0.0` → weight `0.35`;
  - adjusted `0.5` → weight `1.0`;
  - adjusted `1.0` → weight `2.0`.
- Validate that vote counts are nonnegative and `upVotes + downVotes == voteCount`; reject malformed summaries.
- Keep weighted sampling without replacement, unique-candidate validation, bounded requested counts, and deterministic injected-random tests unchanged.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--browser-and-server-rendered-ui-requirements"></a>
#### Browser and Server-Rendered UI Requirements

- Picks, restaurant profiles, and Favorites use the same shared vote-summary formatter.
- Signed-in vote controls contain exactly two buttons: Thumbs up and Thumbs down.
- Buttons use meaningful text or accessible names, `aria-pressed`, visible focus, and the established Void control styling.
- Selecting the opposite button updates the personal vote and public aggregate without rebuilding unrelated server-rendered profile content.
- Selecting the active button is idempotent.
- Anonymous restaurant profiles remain meaningful without JavaScript and make no personal-detail request.
- Personal-control request failures remain local and never erase public profile content.
- New vote endpoints reject numeric payloads with the stable HTTP 400 envelope. Cached old assets that call removed numeric-rating routes receive HTTP 404; the new versioned assets use only the vote contract.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--search-and-structured-data-requirements"></a>
#### Search and Structured Data Requirements

- Valid restaurant profiles remain indexable with one canonical URL and sitemap membership.
- Missing profiles remain HTTP 404 with `noindex,nofollow` and no Restaurant JSON-LD.
- For voted restaurants, schema.org `aggregateRating` uses:
  - `ratingValue`: raw whole-number approval percentage;
  - `bestRating`: `100`;
  - `worstRating`: `0`;
  - `ratingCount`: total vote count.
- Profiles with zero votes omit `aggregateRating`.
- Personal `myVote`, account identity, and audit fields never appear in public HTML or JSON-LD.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--error-and-rollback-behavior"></a>
#### Error and Rollback Behavior

- Migration validation failures prevent the release from becoming ready and leave the prior production release serving.
- The migration never guesses malformed legacy values or silently drops votes.
- Invalid API writes return HTTP 400; missing restaurants preserve the existing not-found behavior; unauthenticated writes preserve the existing authentication response.
- A browser vote failure renders a bounded local error and retains the last server-rendered public summary.
- The production deployment remains governed by the protected candidate-smoke, listener-switch, endpoint verification, and automatic rollback path.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--expected-modules"></a>
#### Expected Modules

- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/model/`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/` or a focused renamed vote package
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/selection/`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantController.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/session/`
- `website/src/main/java/dev/christopherbell/view/wfl/`
- `website/src/main/resources/templates/restaurant.html`
- `website/src/main/resources/static/js/lib/wfl-ui.js`
- `website/src/main/resources/static/js/whats-for-lunch.js`
- `website/src/main/resources/static/js/restaurant-profile.js`
- `website/src/main/resources/static/js/wfl-list.js`
- `website/src/main/resources/static/css/whats-for-lunch.css`
- Focused Java and JavaScript tests plus WFL/model/rating documentation.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--validation-plan"></a>
#### Validation Plan

1. Regression-first migration tests prove exact 1/2 down and 3/4/5 up conversion, preservation of identity/timestamps, retry safety, bounded iteration, and fail-closed malformed handling.
2. Model/service/controller/security tests prove vote validation, idempotent writes, vote changes, public/personal fields, authentication, and stable errors.
3. Mongo aggregation tests prove counts, percentage ordering, vote-count tie-break, stable ID tie-break, limits, and zero-vote exclusion.
4. Selector tests prove neutral prior, approved anchor weights, monotonic behavior, malformed-summary rejection, deterministic sampling, and shared daily/session use.
5. JavaScript tests prove shared summary formatting, two-button accessible controls, request payloads, mutation updates, anonymous zero-fetch behavior, and local failures.
6. Raw view tests prove profile text, canonical metadata, percentage JSON-LD, zero-vote omission, privacy, 404 noindex, and old-route redirect.
7. Full `:website:check` and repository-required JavaScript/production checks pass.
8. Run the packaged app on a non-8080 port with a disposable Mongo database containing legacy 1–5 fixtures; verify V013 data and indexes after startup.
9. Exercise complete, zero-vote, malformed-request, anonymous, authenticated up/down/change, Top 10 Liked, redirect, sitemap, desktop, mobile, keyboard, and console cases.
10. Publish a PR, pass Linux/macOS/Windows CI, dependency review, and CodeQL, merge, deploy the merged SHA, and verify public/local health, live assets, migrated aggregates, leaderboard, profiles, services, and database migration state.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--acceptance-criteria"></a>
#### Acceptance Criteria

- No user-facing WFL star scale or “Top 10 Rated” language remains except the intentional redirect compatibility path and historical migration tests/documentation.
- Every valid legacy rating is represented by the required binary vote after V013.
- Numeric rating writes are rejected.
- Public summaries and Top 10 Liked show correct approval percentage and counts.
- Higher-approval restaurants have monotonically higher selection weights; lower-approval restaurants have lower weights; unrated remains neutral.
- All profile SEO/privacy guarantees from PR #1345 remain intact.
- Automated, alternate-port, browser, CI, merge, production, and Builder closeout evidence pass with no unresolved blocker.

<a id="source-docs-specs-2026-08-03-wfl-thumbs-voting-md--open-questions"></a>
#### Open Questions

None. The product, migration, compatibility, UI, ranking, weighting, failure, and validation decisions are approved.

<!-- /migrated-source: docs/specs/2026-08-03-wfl-thumbs-voting.md -->

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md"></a>
## 2026-08-03 | work-closures | WFL Archived Session Recovery Closure

Original source: `docs/work-closures/2026-08-03-wfl-archived-session-recovery-closure.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `0374ebf5b2bbcd94f7ef4697df56bdf93750251fe7dcfdaab9230b368d387a47`.

<!-- migrated-source: docs/work-closures/2026-08-03-wfl-archived-session-recovery-closure.md -->
<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--wfl-archived-session-recovery-closure"></a>
### WFL Archived Session Recovery Closure

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--final-status"></a>
#### Final Status

closed

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--source"></a>
#### Source

Direct user-reported production bug on 2026-08-03: the What's For Lunch page showed "This lunch session is archived and cannot be changed." No separate GitHub issue existed, so no external issue close operation was applicable. PR #1350 had no comments, reviews, or attachments; therefore no untrusted GitHub input influenced scope or closure.

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--completed-scope"></a>
#### Completed Scope

- Rejected archived saved sessions during implicit member-session restoration and returned the browser to normal location/picker initialization.
- Loaded explicit archive URLs by participant read first, joining only when a nonparticipant active link returns 404.
- Kept explicit archives readable with historical picks and disabled session votes.
- Routed refresh, filters, and location actions from archives into a fresh picker instead of an expired-session mutation.
- Preserved active host refreshes, active guest restrictions, server 409 expiry-race enforcement, retention, voting, favorites, and weighted selection.

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--spoke-repository"></a>
#### Spoke Repository

- Repository: `azurras/christopherbell.dev`
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-archived-session-recovery`
- Feature commit: `255df4d101662b56b18f618fd3931e538f881b75`
- Pull request: [#1350 Recover archived WFL sessions locally](https://github.com/azurras/christopherbell.dev/pull/1350)
- Merge commit: `9c587103cb7f7df2ab52ed3e232f1ca67660fd6e`
- Merge state: merged to `main` by squash after all required checks passed

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--automated-validation"></a>
#### Automated Validation

- Focused Node recovery suite: 7 passed, 0 failed.
- Full JavaScript suite: 343 passed, 0 failed.
- `:website:check`: BUILD SUCCESSFUL in 3m 4s; 21 tasks, including Java, JavaScript, static/package checks, and Windows/Pester verification.
- GitHub: Linux, macOS, Windows, CodeQL actions, CodeQL Java/Kotlin, CodeQL JavaScript/TypeScript, and Dependency Review all passed.

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--local-runtime-validation"></a>
#### Local Runtime Validation

The packaged candidate ran on `http://127.0.0.1:8094` against disposable MongoDB fixtures. Browser acceptance proved active shared reset, implicit archive fallback, explicit archive readability, new-session creation from an archive, direct archived `Try 3 more`, archive immutability, and zero browser warnings/errors. The candidate stopped, port 8094 was freed, and the disposable database was dropped. See [WFL Archived Session Recovery Test Report](../test-reports/2026-08-03-wfl-archived-session-recovery-test-report.md).

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--production-deployment-and-acceptance"></a>
#### Production Deployment and Acceptance

- The native SYSTEM automatic deployment started at 21:33:57 and completed listener rotation at 21:39:41 on 2026-08-03 America/Chicago.
- Production listener changed from PID `74080` to PID `63840`.
- The live `/js/whats-for-lunch.js` changed from `HasRecovery=False` to `HasRecovery=True`.
- Signed-in plain `https://www.christopherbell.dev/wfl` rendered `Share your location` instead of restoring the retained archive or displaying a 409 error.
- Explicit archive `09c38747-2cea-4c5c-b6f8-18535d993b19` rendered `Archived lunch session`, the three historical restaurants, disabled session vote controls, and enabled `Try 3 more`.
- After read-only verification, the archive remained revision `143` with the same three restaurant IDs and unchanged lifecycle deadlines.
- The Chrome tab was returned to plain `/wfl`, which again rendered the location prompt; browser warnings/errors were empty.
- Local liveness, local readiness, local WFL, apex WFL, and `www` WFL all returned HTTP 200.
- `MongoDB`, `ChristopherBellDev`, and `cloudflared` remained Running/Automatic.
- Protected production config remained ACL-denied to the non-elevated shell; no ACL was weakened.

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--decisions"></a>
#### Decisions

The server conflict and archive lifecycle were retained because they are correct. Recovery is client-owned: implicit archives are discarded locally, explicit participant archives are read before any join attempt, and fresh selections never mutate known archives.

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

None for this defect. The host-managed worktree is preserved; it can be removed later through the normal workspace lifecycle after no further PR iteration is needed.

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--closure-readiness"></a>
#### Closure Readiness

ready

<a id="source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md--closure-text"></a>
#### Closure Text

Resolved and deployed. PR #1350 merged as `9c587103`. All local and GitHub checks passed. Production rotated to the merged release, plain signed-in `/wfl` now recovers from saved archived state, the retained archive remains explicitly readable and immutable, every checked endpoint is HTTP 200, and all native production services remain Running/Automatic. No separate GitHub issue existed to close and no follow-up gap remains.

<!-- /migrated-source: docs/work-closures/2026-08-03-wfl-archived-session-recovery-closure.md -->

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md"></a>
## 2026-08-03 | work-closures | WFL Thumbs Voting Closure

Original source: `docs/work-closures/2026-08-03-wfl-thumbs-voting.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `8953c1024f345b6916013334da3f85d5426547a00a2d9292208329df52f5c60e`.

<!-- migrated-source: docs/work-closures/2026-08-03-wfl-thumbs-voting.md -->
<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--wfl-thumbs-voting-closure"></a>
### WFL Thumbs Voting Closure

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--final-status"></a>
#### Final Status

closed

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--central-work"></a>
#### Central Work

- [What's For Lunch Thumbs Voting](#source-docs-work-2026-08-03-wfl-thumbs-voting-md)
- [Specification](#source-docs-specs-2026-08-03-wfl-thumbs-voting-md)
- [Implementation plan](../implementation-plans/2026-08-03-wfl-thumbs-voting.md)
- [Local runtime test report](../test-reports/2026-08-03-wfl-thumbs-voting-test-report.md)

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--completed-scope"></a>
#### Completed Scope

- Replaced 1-5 restaurant ratings with strict `UP` and `DOWN` votes.
- Added V013 full-collection preflight and deterministic 3-5 to up, 1-2 to down conversion while retaining the existing collection and unique restaurant/account index.
- Replaced public/private API, aggregation, Top Liked ordering, session/service, and browser contracts with binary votes and approval summaries.
- Weighted daily, nearby, and shared-session selection by smoothed approval so well-liked restaurants appear more often and disliked restaurants less often while no-vote restaurants remain eligible.
- Added thumb controls to WFL picks, restaurant profiles, Favorites, and Top Liked with idempotent/race-safe state updates.
- Applied Void styling to the WFL experience and restaurant profiles, retained indexable canonical profiles, emitted 0-100 approval JSON-LD, and kept zero-vote/missing-profile crawler behavior correct.
- Hardened Windows deployment to validate V013 against a disposable restored clone before a stop-old-writer, forward-only live migration boundary.

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--spoke-repository-and-publication"></a>
#### Spoke Repository and Publication

- Repository: `azurras/christopherbell.dev`
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-thumbs-voting`
- Reviewed branch commit: `fbab5e8816c66fd8c46147a95cf43f0832c3b341`
- Pull request: [#1349 Replace WFL ratings with thumbs voting](https://github.com/azurras/christopherbell.dev/pull/1349)
- Squash merge: `3b9ee44ba29627c3595b8aebc16612cc2065a885`
- Required checks: Ubuntu, macOS, Windows, Dependency Review, CodeQL Actions, CodeQL Java/Kotlin, and CodeQL JavaScript/TypeScript all passed.

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--validation"></a>
#### Validation

- Fresh diff whitespace validation passed.
- Windows production common/operations/deploy Pester passed 92/92.
- `:website:check` completed `BUILD SUCCESSFUL`; supporting totals were 1,656 Java tests with zero failures and 336/336 JavaScript tests.
- Packaged alternate-port validation on 8094 passed invalid-data preflight, successful conversion, strict API rejection, ordering, weighting sample, redirect/sitemap/SEO, desktop/mobile UI, idempotence, persistence, and clean console checks.
- Final whole-branch review passed with no critical, important, or minor findings.

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--production"></a>
#### Production

- Protected release: `C:\ProgramData\christopherbell.dev\releases\3b9ee44ba29627c3595b8aebc16612cc2065a885`
- Listener rotation: port 8080 PID 59036 to PID 74080.
- Services: ChristopherBellDev, MongoDB, and cloudflared running; readiness and liveness HTTP 200.
- V013: `APPLIED` with checksum `c10c2769b37044d866224770f7fb8b0877e02c2457c53d33ee25eeb879ab86f7`.
- Live vote shape: 87 total, 53 up, 34 down, zero legacy rating fields, zero invalid votes, unique `restaurant_account_unique` retained.
- Public verification: Top Liked API/page 200; `/wfl/top-rated` 308 to `/wfl/top-liked`; sitemap current; canonical indexable profile and 0-100 JSON-LD correct; zero-vote profile omits aggregate; missing profile is 404/noindex; `/wfl` and profiles render Void styling without horizontal overflow or browser warnings/errors.

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--decisions"></a>
#### Decisions

- Legacy numeric clients are rejected rather than translated.
- Approval weighting uses `(up + 1.5) / (up + down + 3)` and maps approval to weights from 0.35 through 2.0.
- The live migration is forward-only after the old writer stops. The protected deployment retained the prior release but did not restart it after V013 began.

<a id="source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

No required gaps or follow-ups remain. V013 is immutable; future schema changes must use a new migration ID. The isolated worktree and scratch evidence remain available for audit and can be removed later under normal worktree cleanup.

<!-- /migrated-source: docs/work-closures/2026-08-03-wfl-thumbs-voting.md -->

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md"></a>
## 2026-08-03 | work | WFL Archived Session Recovery

Original source: `docs/work/2026-08-03-wfl-archived-session-recovery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `11867fb4dafc4f7a1a17b7ac76ed579757a6e5a1a0d19871188b72fb937b1584`.

<!-- migrated-source: docs/work/2026-08-03-wfl-archived-session-recovery.md -->
<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--wfl-archived-session-recovery"></a>
### WFL Archived Session Recovery

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--status"></a>
#### Status

closed

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--objective"></a>
#### Objective

Stop the What's For Lunch browser from treating archived shared sessions as mutable current sessions. Automatically discard archived sessions restored from saved browser state, and make a request for new picks from an explicitly opened archived session leave the archive and start a fresh flow without changing archived history.

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--owner-and-context"></a>
#### Owner and Context

- Hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `A:\Projects\christopherbell.dev`
- Reported by: direct user report on 2026-08-03 after the thumbs-voting production release
- Delivery model: root-cause-first diagnosis, approved narrow design, durable spec/plan, isolated worktree from refreshed `origin/main`, test-first JavaScript fix, alternate-port runtime/browser validation, PR/CI/squash merge, protected production deployment, and final Builder closure

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--root-cause-evidence"></a>
#### Root Cause Evidence

- Production retains one archived WFL session and one active WFL session for the reporting account.
- Archived sessions remain readable for 30 days after their 24-hour active window, by design.
- `loadStoredMemberSession()` currently accepts an API detail with `active: false`, keeps it in `activeSession`, and returns success instead of clearing the saved session ID.
- `loadNearbyPicks()` treats any non-null `activeSession` as mutable and calls the shared-session restaurant-reset endpoint.
- The backend correctly classifies that request as `WFL_SESSION_EXPIRED` and returns HTTP 409 with “This lunch session is archived and cannot be changed.”

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--approved-design"></a>
#### Approved Design

- A session restored implicitly from the per-account saved browser key is reusable only when `active !== false`.
- An archived saved session is cleared and normal solo/new-session initialization continues.
- An archived session opened explicitly by URL remains readable and retains its historical picks, votes, link, and archive presentation.
- When the user requests new picks, applies filters, or changes location while viewing an explicit archive, the browser clears the archived client context and starts a new solo flow. It never sends a mutation for the archived session.
- The server archive lifetime, immutable expired-session mutations, HTTP 409 contract, and automatic deletion remain unchanged.

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--related-artifacts"></a>
#### Related Artifacts

- Specification: [WFL Archived Session Recovery](#source-docs-specs-2026-08-03-wfl-archived-session-recovery-md), complete
- Implementation plan: [WFL Archived Session Recovery](../implementation-plans/2026-08-03-wfl-archived-session-recovery.md), complete
- Test report: [WFL Archived Session Recovery Test Report](../test-reports/2026-08-03-wfl-archived-session-recovery-test-report.md), complete
- Closure: [WFL Archived Session Recovery Closure](#source-docs-work-closures-2026-08-03-wfl-archived-session-recovery-closure-md)
- Session memory: [WFL Archived Session Recovery](#source-docs-session-memory-2026-08-03-wfl-archived-session-recovery-md)

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--spoke-repositories"></a>
#### Spoke Repositories

- `azurras/christopherbell.dev` at `A:\Projects\christopherbell.dev`

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--current-state"></a>
#### Current State

PR #1350 merged as `9c587103cb7f7df2ab52ed3e232f1ca67660fd6e` after every required CI, CodeQL, and dependency gate passed. The native SYSTEM deployment rotated production to the merged release. Signed-in production verification proved implicit archive fallback, explicit read-only archive rendering, enabled fresh-pick recovery, unchanged archived MongoDB state, zero browser warnings/errors, HTTP 200 local/apex/www WFL responses, and Running/Automatic native services. No required action remains.

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--validation"></a>
#### Validation

- Live MongoDB session inventory was inspected read-only at 2026-08-04T00:25Z.
- Current client and server session paths were traced from saved browser restoration through the expired mutation response.
- No protected production ACLs or session data were modified.

<a id="source-docs-work-2026-08-03-wfl-archived-session-recovery-md--next-steps"></a>
#### Next Steps

None. This work is closed.

<!-- /migrated-source: docs/work/2026-08-03-wfl-archived-session-recovery.md -->

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md"></a>
## 2026-08-03 | work | What's For Lunch Thumbs Voting

Original source: `docs/work/2026-08-03-wfl-thumbs-voting.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `24cd5fe4142f5c2ab45e795811e93d8f056a6711f869de4765166ec90f4c69f0`.

<!-- migrated-source: docs/work/2026-08-03-wfl-thumbs-voting.md -->
<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--whats-for-lunch-thumbs-voting"></a>
### What's For Lunch Thumbs Voting

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--status"></a>
#### Status

closed

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--objective"></a>
#### Objective

Replace the WFL 1–5 restaurant rating system with thumbs-up/thumbs-down voting, migrate existing data deterministically, rename and re-rank the public leaderboard, preserve indexable restaurant profiles, and align weighted restaurant selection with smoothed binary approval.

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--owner-and-context"></a>
#### Owner and Context

- Hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `A:\Projects\christopherbell.dev`
- Requested by: direct user request on 2026-08-03
- Delivery model: approved design, durable spec and implementation plan, isolated refreshed-origin worktree, regression-first migration and code changes, alternate-port migrated-database/browser validation, PR/CI/merge, protected production deployment, and final Builder closeout

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--approved-decisions"></a>
#### Approved Decisions

- Convert stored `3–5` ratings to `UP` and `1–2` to `DOWN`.
- Use one clean V013 in-place data migration; do not retain dual-schema reads.
- Reject old numeric writes immediately.
- Show approval percentage plus up/down counts.
- Rename Top 10 Rated to Top 10 Liked and permanently redirect the old public page URL.
- Rank by raw approval percentage, then total votes, then stable restaurant ID.
- Use a three-vote neutral prior and preserve the selection-weight range from `0.35×` through `2.0×`.

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--related-artifacts"></a>
#### Related Artifacts

- Specification: [What's For Lunch Thumbs Voting](#source-docs-specs-2026-08-03-wfl-thumbs-voting-md), approved and implemented on the delivery branch
- Implementation plan: [What's For Lunch Thumbs Voting](../implementation-plans/2026-08-03-wfl-thumbs-voting.md), implementation complete and locally verified
- Test report: [WFL Thumbs Voting Test Report](../test-reports/2026-08-03-wfl-thumbs-voting-test-report.md), complete
- Spoke review: final whole-branch review passed with no critical, important, or minor findings
- Closure: [WFL Thumbs Voting Closure](#source-docs-work-closures-2026-08-03-wfl-thumbs-voting-md)
- Session memory: [WFL Thumbs Voting](#source-docs-session-memory-2026-08-03-wfl-thumbs-voting-md)

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--spoke-repositories"></a>
#### Spoke Repositories

- `azurras/christopherbell.dev` at `A:\Projects\christopherbell.dev`

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--current-state"></a>
#### Current State

Implementation completed at reviewed spoke commit `fbab5e8816c66fd8c46147a95cf43f0832c3b341`, passed PR #1349 CI/security, squash-merged as `3b9ee44ba29627c3595b8aebc16612cc2065a885`, and deployed through the protected Windows pipeline. Production now serves the merged release on port 8080 with readiness/liveness healthy. Live V013 is applied; all 87 WFL vote documents are binary with the unique restaurant/account index retained. Public API/UI/SEO and real-browser Void rendering checks passed.

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--validation"></a>
#### Validation

Local runtime validation is recorded in the complete test report. Supporting automated validation passed 92/92 Pester tests, 1,656 Java tests, 336/336 JavaScript tests, and `:website:check`; final pre-publication verification will rerun the authoritative suites.

<a id="source-docs-work-2026-08-03-wfl-thumbs-voting-md--next-steps"></a>
#### Next Steps

No required follow-up remains. Preserve the retained production backup/release according to normal retention; any future vote-contract change must append a new migration rather than modifying V013.

<!-- /migrated-source: docs/work/2026-08-03-wfl-thumbs-voting.md -->

