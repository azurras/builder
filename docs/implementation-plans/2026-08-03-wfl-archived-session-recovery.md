# WFL Archived Session Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make WFL recover automatically from archived saved sessions and start fresh picks from explicit archived views without attempting an expired-session mutation.

**Architecture:** Add one small dependency-injected browser session-flow controller inside the existing WFL page module. The controller owns only the decision between restoring an active saved session, falling back locally from an archive, refreshing an active shared session, and starting a fresh solo flow; server lifecycle and storage remain unchanged.

**Tech Stack:** Vanilla JavaScript ES modules, Node 25 built-in test runner, Spring Boot static resources, Gradle 9.6.1, Java 25 packaging, PowerShell/native Windows production deployment.

## Global Constraints

- Archived server documents stay readable, immutable, and eligible for normal 30-day TTL retention.
- A saved session detail with `active: false` is never reused as the default current session.
- Explicit `/wfl?session=<id>` archive loading remains unchanged and readable.
- Refresh, filter, or location actions from an archived view start the normal solo/new-session flow and never call the archived restaurant-reset endpoint.
- Active shared-session refresh behavior and visible server conflicts for genuine expiry races remain unchanged.
- No dependencies, server endpoints, MongoDB data, session lifetime settings, thumb votes, or approval weights change.
- Preserve the dirty authoritative spoke checkout; execute only in a clean isolated worktree from refreshed `origin/main`.
- Invoke `write-chris-street-style-code` before editing JavaScript, tests, or executable documentation, and follow strict RED/GREEN TDD.
- Validate a packaged candidate on a non-8080 port before production deployment.

---

## Document Status

complete

## Objective

Implement the approved specification at `docs/specs/2026-08-03-wfl-archived-session-recovery.md` through focused JavaScript orchestration tests, a minimal browser flow correction, aggregate verification, alternate-port authenticated browser acceptance, PR/CI/merge, protected production deployment, and Builder closeout.

## Goals

1. Reject an archived detail as an implicitly reusable saved member session.
2. Keep explicit archives visible until the user requests new picks.
3. Route new-pick requests from archives into `loadSoloSession({ forceNew: true })` without calling `refreshSharedSessionPicks()`.
4. Preserve the active shared-session refresh branch exactly.
5. Prove behavior with real exported orchestration tests and live browser evidence.

## Inputs

- Approved specification: `docs/specs/2026-08-03-wfl-archived-session-recovery.md`.
- Live root cause: one archived retained session is accepted by `loadStoredMemberSession()`, and later `loadNearbyPicks()` branches only on non-null state.
- Existing backend behavior: expired mutations correctly return HTTP 409 `WFL_SESSION_EXPIRED`; no server change is required.
- Current spoke base: `origin/main` at `3b9ee44ba29627c3595b8aebc16612cc2065a885` when inspected.
- Repository instructions: JavaScript is browser-native ESM with no npm workflow; tests run through Node/Gradle.

## Branch

- Create `codex/wfl-archived-session-recovery` from refreshed `origin/main` in `A:\Projects\christopherbell.dev-worktrees\wfl-archived-session-recovery`.
- Use private Gradle home `A:\Projects\christopherbell.dev-gradle-homes\wfl-archived-session-recovery`.

## Non-Goals

- No Java/controller/service/repository/model/configuration edits.
- No session data repair, reactivation, early deletion, or migration.
- No new UI panel, modal, button, or copy redesign.
- No changes to WFL selection, restaurant votes, favorites, or profile/list pages.
- No opportunistic refactor of the large WFL module.

## Assumptions

- `WhatsForLunchSessionDetail.active` is the trusted client lifecycle signal and is explicitly `false` for archived details.
- `loadSoloSession({ forceNew: true })` remains the single existing transition that clears member/anonymous saved state, stops polling, removes a `session` query parameter, and loads new picks.
- Function declarations referenced by the new controller dependencies are available through JavaScript declaration hoisting before any click/load action invokes them.
- The existing backend conflict remains necessary for a session that expires after a client-side active check.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add test-first archived-session recovery orchestration

Sequence / dependencies:
- Runs first and is the only semantic code task.
- Add the full behavior tests and witness RED before changing `whats-for-lunch.js`.
- Update documentation only after the focused tests are GREEN.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: implicit archived saved sessions fall back locally; new-pick requests from explicit archives start fresh; active sessions still refresh in place.
  - Invariants: archived server history is never mutated; active-session reset and expiry-race conflict handling remain unchanged; saved state is cleared only on failed/inactive implicit restore or existing force-new flow.
  - Boundary/API: add exported `createSessionRecoveryController(dependencies)` returning `restoreStoredSession(sessionId)` and `requestNearbyPicks()`; wire only existing private WFL functions through it without changing HTTP endpoints or response shapes.
  - Effects and failures: controller dependencies expose saved-state removal, local active-session mutation, polling stop, session fetch, active reset, and solo load; expected restore failures fall back as before, while downstream solo/reset failures retain their existing callers and rendering.
  - Tests and evidence: RED tests must fail because no controller exists; GREEN tests exercise complete active/archived session fixtures and assert which real orchestration dependency is called, then focused/full JS and aggregate checks prove compatibility.

#### Code Edit 1.1
- File: `website/src/test/js/whats-for-lunch-session-recovery.test.js`
- Lines: 1-120
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```javascript
import assert from 'node:assert/strict';
import test from 'node:test';

globalThis.localStorage = { getItem: () => null, removeItem() {}, setItem() {} };
globalThis.document = { cookie: '', getElementById: () => null };
globalThis.window = { location: { origin: 'https://www.christopherbell.dev', search: '' } };

const picksModule = await import('../../main/resources/static/js/whats-for-lunch.js');

const ACTIVE_SESSION = Object.freeze({
  id: 'active-session',
  createdByUsername: 'Chris',
  canManage: true,
  participantUsernames: ['Chris'],
  restaurants: [],
  votesByRestaurant: {},
  myVoteRestaurantId: null,
  revision: 7,
  active: true,
  canChangeRestaurants: true,
  activeUntil: '2026-08-04T11:48:51.112Z',
  createdOn: '2026-08-03T11:48:51.112Z',
  lastUpdatedOn: '2026-08-03T11:51:53.639Z',
});

const ARCHIVED_SESSION = Object.freeze({
  ...ACTIVE_SESSION,
  id: 'archived-session',
  canManage: false,
  active: false,
  canChangeRestaurants: false,
  activeUntil: '2026-08-03T20:08:40.385Z',
  createdOn: '2026-08-02T20:08:40.385Z',
  lastUpdatedOn: '2026-08-03T02:03:32.948Z',
});

function recoveryPage({ initialSession = null, restoredSession = null } = {}) {
  const state = { session: initialSession };
  const calls = {
    clearStoredSession: 0,
    loadSession: [],
    loadSoloSession: [],
    refreshSharedSession: 0,
    stopPolling: 0,
  };
  const controller = picksModule.createSessionRecoveryController({
    getActiveSession: () => state.session,
    setActiveSession: session => { state.session = session; },
    clearStoredSession: () => { calls.clearStoredSession += 1; },
    stopPolling: () => { calls.stopPolling += 1; },
    loadSession: async (sessionId, options) => {
      calls.loadSession.push({ sessionId, options });
      state.session = restoredSession;
    },
    refreshSharedSession: async () => { calls.refreshSharedSession += 1; },
    loadSoloSession: async options => {
      calls.loadSoloSession.push(options);
      return 'fresh-picks';
    },
  });
  return { calls, controller, state };
}

test('archived saved session is cleared so normal initialization can continue', async () => {
  assert.equal(typeof picksModule.createSessionRecoveryController, 'function');
  const page = recoveryPage({ restoredSession: ARCHIVED_SESSION });

  const restored = await page.controller.restoreStoredSession('archived-session');

  assert.equal(restored, false);
  assert.equal(page.state.session, null);
  assert.equal(page.calls.clearStoredSession, 1);
  assert.equal(page.calls.stopPolling, 1);
  assert.deepEqual(page.calls.loadSession, [{
    sessionId: 'archived-session',
    options: { join: false, storeSession: true },
  }]);
});

test('active saved session remains the current shared session', async () => {
  const page = recoveryPage({ restoredSession: ACTIVE_SESSION });

  const restored = await page.controller.restoreStoredSession('active-session');

  assert.equal(restored, true);
  assert.equal(page.state.session, ACTIVE_SESSION);
  assert.equal(page.calls.clearStoredSession, 0);
  assert.equal(page.calls.stopPolling, 0);
});

test('new picks from an archived session use the solo flow without shared reset', async () => {
  const page = recoveryPage({ initialSession: ARCHIVED_SESSION });

  const result = await page.controller.requestNearbyPicks();

  assert.equal(result, 'fresh-picks');
  assert.equal(page.calls.refreshSharedSession, 0);
  assert.deepEqual(page.calls.loadSoloSession, [{ forceNew: true }]);
});

test('new picks from an active session preserve the shared reset flow', async () => {
  const page = recoveryPage({ initialSession: ACTIVE_SESSION });

  await page.controller.requestNearbyPicks();

  assert.equal(page.calls.refreshSharedSession, 1);
  assert.deepEqual(page.calls.loadSoloSession, []);
});
```

Verification:
- Run `node --test website/src/test/js/whats-for-lunch-session-recovery.test.js` before production edits.
- Expected RED: module export `createSessionRecoveryController` is absent, so the first construction/assertion fails for the missing behavior boundary.

#### Code Edit 1.2
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 534-540
- Action: replace

Current:
```javascript
async function loadNearbyPicks() {
  if (activeSession) {
    await refreshSharedSessionPicks();
    return;
  }
  return loadSoloSession({ forceNew: true });
}
```

Proposed:
```javascript
export function createSessionRecoveryController({
  getActiveSession,
  setActiveSession,
  clearStoredSession,
  stopPolling,
  loadSession,
  refreshSharedSession,
  loadSoloSession,
}) {
  function clearInactiveRestoredSession() {
    clearStoredSession();
    setActiveSession(null);
    stopPolling();
  }

  async function restoreStoredSession(sessionId) {
    if (!sessionId) return false;
    try {
      await loadSession(sessionId, { join: false, storeSession: true });
      const session = getActiveSession();
      if (session && session.active !== false) return true;
    } catch (_) {
      // Stored sessions already fall back to normal initialization on lookup failure.
    }
    clearInactiveRestoredSession();
    return false;
  }

  async function requestNearbyPicks() {
    const session = getActiveSession();
    if (session && session.active !== false) {
      await refreshSharedSession();
      return;
    }
    return loadSoloSession({ forceNew: true });
  }

  return { requestNearbyPicks, restoreStoredSession };
}

const sessionRecoveryController = createSessionRecoveryController({
  getActiveSession: () => activeSession,
  setActiveSession: session => { activeSession = session; },
  clearStoredSession: clearStoredMemberSession,
  stopPolling: stopSessionPolling,
  loadSession,
  refreshSharedSession: refreshSharedSessionPicks,
  loadSoloSession,
});

async function loadNearbyPicks() {
  return sessionRecoveryController.requestNearbyPicks();
}
```

Verification:
- The focused RED test must progress past controller construction after this edit.
- `node --check website/src/main/resources/static/js/whats-for-lunch.js` must exit 0.

#### Code Edit 1.3
- File: `website/src/main/resources/static/js/whats-for-lunch.js`
- Lines: 591-601
- Action: replace

Current:
```javascript
async function loadStoredMemberSession() {
  const storedSessionId = getStoredMemberSessionId();
  if (!storedSessionId) return false;
  try {
    await loadSession(storedSessionId, { join: false, storeSession: true });
    return true;
  } catch (_) {
    clearStoredMemberSession();
    return false;
  }
}
```

Proposed:
```javascript
async function loadStoredMemberSession() {
  return sessionRecoveryController.restoreStoredSession(getStoredMemberSessionId());
}
```

Verification:
- `node --test website/src/test/js/whats-for-lunch-session-recovery.test.js` must pass 4/4.
- Mentally mutate the archived predicate to treat `active: false` as active; the saved-session and archived-new-picks tests must fail.

#### Code Edit 1.4
- File: `website/src/main/resources/static/js/README.md`
- Lines: 60-74
- Action: replace

Current:
```markdown
- `whats-for-lunch.js` lets visitors choose browser geolocation or a ZIP code,
  keeps cuisine and radius filters hidden behind an obvious toggle by default,
  keeps "Try 3 more" as the primary page action, groups filters, location, and
  Lunch with Friends tools into a secondary tabbed control area, loads three restaurants
  from the WFL nearby API, preserves anonymous picks for at most 30 minutes as
  restaurant IDs plus an optional ZIP (never coordinates or full restaurant
  payloads), saves filters for signed-in users, creates
  shareable voting sessions for logged-in users, polls active sessions for
  restaurant/vote changes, links vote usernames to public profiles, lets session-link visitors join after authentication,
  lets signed-in users set `UP` or `DOWN` restaurant votes with accessible thumb
  controls, lets signed-in users favorite restaurants, links cards to restaurant profile pages, replaces
  the card list with a loading wheel while "Try 3 more" fetches new picks, and
  shows archived shared sessions as read-only, permits only the host to request
  new shared picks, and only re-queries when the user clicks "Try 3 more", applies filters, changes
  ZIP/location, or an admin deletes a restaurant.
```

Proposed:
```markdown
- `whats-for-lunch.js` lets visitors choose browser geolocation or a ZIP code,
  keeps cuisine and radius filters hidden behind an obvious toggle by default,
  keeps "Try 3 more" as the primary page action, groups filters, location, and
  Lunch with Friends tools into a secondary tabbed control area, loads three restaurants
  from the WFL nearby API, preserves anonymous picks for at most 30 minutes as
  restaurant IDs plus an optional ZIP (never coordinates or full restaurant
  payloads), saves filters for signed-in users, creates
  shareable voting sessions for logged-in users, polls active sessions for
  restaurant/vote changes, links vote usernames to public profiles, lets session-link visitors join after authentication,
  lets signed-in users set `UP` or `DOWN` restaurant votes with accessible thumb
  controls, lets signed-in users favorite restaurants, links cards to restaurant profile pages, replaces
  the card list with a loading wheel while "Try 3 more" fetches new picks, shows
  explicitly opened archived shared sessions as read-only, discards archived
  sessions restored implicitly from saved browser state, starts fresh picks when
  selection controls are used from an archive, permits only the host to request
  new picks in an active shared session, and only re-queries when the user clicks
  "Try 3 more", applies filters, changes ZIP/location, or an admin deletes a restaurant.
```

Verification:
- Confirm the documentation distinguishes implicit restoration from explicit archive viewing and does not claim server reactivation.

- [ ] Write Code Edit 1.1 only and run the focused Node command to witness the expected RED failure.
- [ ] Apply Code Edits 1.2 and 1.3 with no unrelated refactor.
- [ ] Run the focused Node command to GREEN, then run `node --check website/src/main/resources/static/js/whats-for-lunch.js`.
- [ ] Apply Code Edit 1.4 and run `git diff --check`.
- [ ] Run `./gradlew.bat :website:jsTest --no-daemon --console=plain` with the private Gradle home.
- [ ] Review the task diff against the Before-Edit Brief and commit `Recover archived WFL sessions locally`.

### Task 2 - Validate, publish, deploy, and close the regression fix

Sequence / dependencies:
- Runs only after Task 1 is committed and reviewed clean.
- Contains no product-code edits unless verification finds an in-scope defect; any such defect returns to Task 1 RED/GREEN discipline and review.

Implementation notes:
- Re-read the approved specification and confirm the Task 1 behavior matches it before widening verification.
- Use the existing native Windows deployment pipeline; do not weaken protected ACLs or modify live session records.

- [ ] Run the full `./gradlew.bat :website:check --no-daemon --console=plain` with the private Gradle home.
- [ ] Build the packaged JAR and start it on a free non-8080 port with explicit local profile, disposable MongoDB database, and background import/collector jobs disabled.
- [ ] Seed an authenticated test account plus one active and one archived session in the disposable database without copying production credentials or personal data.
- [ ] Use a real browser to prove implicit archived restoration falls back, explicit archive rendering remains readable, archived “Try 3 more”/filter/location starts fresh, active shared reset still succeeds, and the console remains clean.
- [ ] Capture exact URL/port, UI input, API status/body, database before/after state, and process cleanup in a Builder test report; validate, index, commit, and push the checkpoint.
- [ ] Apply the Jane Street review rubric to the complete diff and resolve every blocker/warning.
- [ ] Push `codex/wfl-archived-session-recovery`, open a ready PR, and wait for Linux/macOS/Windows CI, Dependency Review, and all CodeQL analyzers.
- [ ] Squash merge only when every required check passes; record the merged SHA.
- [ ] Let the authorized SYSTEM deployment path deploy the exact merged SHA and verify listener rotation, liveness/readiness `UP`, exact asset SHA, services, active/archived session invariants, and live browser recovery without the original conflict.
- [ ] Close the Builder work/spec/plan/test-report state, create closure/session memory, update indexes, validate hub state, and commit/push Builder main.

## Code Changes

- `website/src/test/js/whats-for-lunch-session-recovery.test.js`: add real controller behavior tests for implicit archived fallback, active restore, archived fresh-picks routing, and active shared reset.
- `website/src/main/resources/static/js/whats-for-lunch.js:534-540`: add and wire the testable recovery controller; route nearby picks based on active state, not mere session presence.
- `website/src/main/resources/static/js/whats-for-lunch.js:591-601`: delegate stored-member restoration to the recovery controller.
- `website/src/main/resources/static/js/README.md:60-74`: document implicit archive discard and explicit archive recovery behavior.

## Files and Modules

- Browser production: `website/src/main/resources/static/js/whats-for-lunch.js`.
- Browser regression: `website/src/test/js/whats-for-lunch-session-recovery.test.js`.
- Browser ownership documentation: `website/src/main/resources/static/js/README.md`.
- No Java, template, CSS, database, or configuration file changes planned.

## Unit Testing

- RED/GREEN: `node --test website/src/test/js/whats-for-lunch-session-recovery.test.js`.
- Syntax: `node --check website/src/main/resources/static/js/whats-for-lunch.js`.
- Full browser unit/integration suite: `./gradlew.bat :website:jsTest --no-daemon --console=plain`.
- Mutation checks: removing the `active !== false` predicate must fail both archived cases; routing active sessions to solo must fail the active reset case.

## Local Testing

- Use a packaged JAR from the isolated worktree on a free alternate port, never 8080.
- Use a disposable database with test-only account/session/restaurant fixtures.
- Exercise normal `/wfl`, explicit `/wfl?session=<archived-id>`, “Try 3 more”, Apply Filters, location change, and active-session refresh.
- Record HTTP/API results, visible page state, local state effects through UI behavior, Mongo session revision/identity invariants, browser console, and responsive layout.
- Stop the exact alternate-port process and drop only the exact disposable database after evidence capture.

## Validation

- Focused tests witness RED before implementation and 4/4 GREEN after.
- Full JavaScript and aggregate repository checks pass.
- Implicit archive restore produces no archived current session or HTTP 409.
- Explicit archive remains readable until new picks are requested.
- New picks from archive create/use a new session and leave the archived document unchanged.
- Active shared refresh increments only the active document revision.
- Required PR checks pass, merged SHA deploys, production services stay healthy, and the original user flow succeeds.

## Rollback or Recovery

- Before merge: revert the cohesive feature commit or close the PR.
- After merge/deploy: the change is browser-only and schema-compatible; normal protected application rollback is safe.
- No production session restore or database rollback is required because the fix does not write migration/data changes.
- If production verification fails, preserve the exact browser/API evidence and use the protected deployment path for rollback or forward repair according to current operations policy.

## Risks

- Implicit and explicit archive paths may be accidentally conflated. Mitigation: automatic discard lives only in stored restoration; explicit link loading is untouched and separately browser-tested.
- A helper-only test could miss wiring. Mitigation: production uses the exported controller directly, tests assert dependency routing/state, and alternate-port browser acceptance exercises the full page.
- Active session behavior could regress. Mitigation: dedicated active restore and active reset tests plus runtime active-session refresh.
- Location permission could make archived fresh-picks testing nondeterministic. Mitigation: use a fixed ZIP input in browser acceptance.
- Production session data is sensitive. Mitigation: use only counts/invariants for diagnosis and disposable synthetic fixtures for candidate testing.

## Completion Criteria

- Specification and implementation plan are approved, validated, committed, and pushed.
- Isolated worktree starts from refreshed `origin/main` with a clean baseline.
- RED/GREEN evidence and final review are recorded.
- Focused, full JS, and `:website:check` pass.
- Alternate-port authenticated browser report proves every acceptance path with no original conflict.
- PR checks pass, squash merge completes, exact SHA deploys, and production recovery is verified.
- Builder work, closure, session memory, indexes, and validation are committed and pushed with no required follow-up.
