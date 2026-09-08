# ChristopherBell.dev Tools Menu Access Navigation Implementation Plan

## Document Status

ready-for-execution

## Objective

Make Tools the single alphabetized navigation location for Music, Command Center, and Back Office, with visibility derived from the current account's effective access.

## Goals

- Gate Music on effective Music read access.
- Gate Back Office and Command Center on exact administrator role.
- Preserve Shared Folder access gating and public tools.
- Remove the moved destinations from the top-level and profile menus.
- Prove visibility and ordering with behavioral tests.

## Inputs

The approved [Tools Menu Access Navigation spec](../session-memory/2026-07-29-christopherbell-dev.md#source-docs-specs-2026-07-29-christopherbell-dev-tools-menu-access-navigation-md), refreshed spoke `origin/main` at `e393687d10c40b856f35d669c25bf3ea65c5c083`, and the user's standing authorization to continue without routine approvals.

## Branch

Create `codex/tools-menu-access-navigation` from refreshed `origin/main` in `A:\Projects\christopherbell.dev-worktrees\tools-menu-access-navigation`.

## Non-Goals

No server authorization, API, route, access-log, dropdown styling, page cross-link, or public-tool visibility changes.

## Assumptions

`/api/accounts/me` returns `role` and `permissions`; server-side account rules keep write implying read, but the browser treats either capability as effective read defensively. Direct routes continue enforcing authorization independently of navigation.

## Open Questions

None.

## Task Breakdown

### Task 1 - Centralize access-aware navigation ownership

Sequence / dependencies:
- Single cohesive task; write and run the tests before the production edits, then run focused and full checks.

Implementation notes:
- Required skill: `write-jane-street-style-code` before any code edits.
- Invoke the skill and its JavaScript/testing references before editing.
- Before-Edit Brief:
  - Behavior: Music, Back Office, and Command Center appear only in the alphabetized Tools dropdown for accounts with effective access and disappear from their former navigation locations.
  - Invariants: existing public Tools entries remain public; Shared Folder keeps effective-read gating; ADMIN sees all three protected destinations; direct routes remain authoritative.
  - Boundary/API: pure Music capability helper and pure navigation item builders consume the current-account projection used by the existing nav component.
  - Effects and failures: the existing current-account request is the only I/O; profile-load failure and logout clear capability state and must never leave stale protected links visible.
  - Tests and evidence: focused JavaScript tests fail against the current menu ownership, pass after the edit, and are followed by full Gradle and local runtime checks.

#### Code Edit 1.1
- File: `website/src/test/js/music.test.js`
- Lines: 5-50
- Action: replace

Current:
```javascript
import {
  musicCatalog,
  musicCatalogParameters,
  musicPageNumbers,
  musicPaginationMarkup,
  musicQueueMarkup,
  musicTrackMarkup,
  musicViewFilter,
} from '../../main/resources/static/js/lib/music.js';
```

Proposed:
```javascript
import {
  accountHasMusicRead,
  musicCatalog,
  musicCatalogParameters,
  musicPageNumbers,
  musicPaginationMarkup,
  musicQueueMarkup,
  musicTrackMarkup,
  musicViewFilter,
} from '../../main/resources/static/js/lib/music.js';

test('Music effective read access accepts admin read or write and rejects missing access', () => {
  assert.equal(accountHasMusicRead({ role: 'ADMIN', permissions: [] }), true);
  assert.equal(accountHasMusicRead({ role: 'USER', permissions: ['MUSIC_READ'] }), true);
  assert.equal(accountHasMusicRead({ role: 'USER', permissions: ['MUSIC_WRITE'] }), true);
  assert.equal(accountHasMusicRead({ role: 'USER', permissions: [] }), false);
  assert.equal(accountHasMusicRead(null), false);
});
```

Verification:
- Run the Music JavaScript test and witness RED because `accountHasMusicRead` is not exported.

#### Code Edit 1.2
- File: `website/src/test/js/nav-messages-link.test.js`
- Lines: 34-156
- Action: replace

Current:
```javascript
const {
  hideNavPanel,
  isActiveNavHref,
  messagesNavHref,
  topLevelNavItems,
  toolsMenuItems
} = await import('../../main/resources/static/js/components/nav.js');

const { adminMenuItems, profileMenuItems } = await import('../../main/resources/static/js/components/nav.js');

test('tools menu adds Shared Folder alphabetically only with effective read access', () => {
  assert.equal(toolsMenuItems(false).some((item) => item.href === '/shared'), false);
  assert.deepEqual(
    toolsMenuItems(true).map((item) => item.label),
    ['Raising Canes Box Index', 'Shared Folder', 'VIN Decoder', "What's For Lunch", 'ZIP Coordinates']
  );
});

test('Music is a primary nav destination for signed-in and signed-out visitors', () => {
  assert.deepEqual(
    topLevelNavItems(false).find((item) => item.href === '/music'),
    { href: '/music', label: 'Music' }
  );
  assert.deepEqual(
    topLevelNavItems(true).find((item) => item.href === '/music'),
    { href: '/music', label: 'Music' }
  );
});

test('admin menu alone exposes back office and command center', () => {
  assert.deepEqual(adminMenuItems(false), []);
  assert.deepEqual(adminMenuItems(true), [
    { href: '/back-office', label: 'Back Office' },
    { href: '/command-center', label: 'Command Center' },
  ]);
});

test('profile menu keeps administrative links but no longer contains Shared Folder', () => {
  assert.deepEqual(profileMenuItems(false, true), []);
  assert.deepEqual(profileMenuItems(true, true), [
    { href: '/back-office', label: 'Back Office' },
    { href: '/command-center', label: 'Command Center' },
  ]);
});
```

Proposed:
```javascript
const {
  hideNavPanel,
  isActiveNavHref,
  messagesNavHref,
  profileMenuItems,
  topLevelNavItems,
  toolsMenuItems
} = await import('../../main/resources/static/js/components/nav.js');

test('Tools keeps public entries and Shared Folder effective-read gating', () => {
  assert.equal(toolsMenuItems().some((item) => item.href === '/shared'), false);
  assert.deepEqual(
    toolsMenuItems({ hasSharedFolderRead: true }).map((item) => item.label),
    ['Raising Canes Box Index', 'Shared Folder', 'VIN Decoder', "What's For Lunch", 'ZIP Coordinates']
  );
});

test('Tools gates moved destinations and sorts every visible item alphabetically', () => {
  assert.equal(toolsMenuItems().some((item) => item.href === '/music'), false);
  assert.deepEqual(
    toolsMenuItems({ hasMusicRead: true }).map((item) => item.label),
    ['Music', 'Raising Canes Box Index', 'VIN Decoder', "What's For Lunch", 'ZIP Coordinates']
  );
  assert.deepEqual(
    toolsMenuItems({ isAdmin: true, hasSharedFolderRead: true })
      .map((item) => item.label),
    ['Back Office', 'Command Center', 'Music', 'Raising Canes Box Index', 'Shared Folder',
      'VIN Decoder', "What's For Lunch", 'ZIP Coordinates']
  );
});

test('moved destinations no longer appear in the top-level or profile menus', () => {
  assert.equal(topLevelNavItems(true).some((item) => item.href === '/music'), false);
  assert.deepEqual(profileMenuItems(), [{ href: '/profile', label: 'Profile' }]);
});
```

Verification:
- Run the navigation JavaScript test and witness RED because Tools lacks the new items/signature and the old menus still own them.

#### Code Edit 1.3
- File: `website/src/main/resources/static/js/lib/music.js`
- Lines: before 4
- Action: add

Proposed:
```javascript
/** Return the effective Music read capability reported by the current-account API. */
export function accountHasMusicRead(account) {
  if (account?.role === 'ADMIN') return true;
  const permissions = new Set(Array.isArray(account?.permissions) ? account.permissions : []);
  return permissions.has('MUSIC_READ') || permissions.has('MUSIC_WRITE');
}
```

Verification:
- The focused Music JavaScript test passes.

#### Code Edit 1.4
- File: `website/src/main/resources/static/js/components/nav.js`
- Lines: 8-368
- Action: replace

Current:
```javascript
import { accountHasSharedFolderRead } from '../lib/shared-folder.js';

export function toolsMenuItems(hasSharedFolderRead = false) {
    return [
        { href: '/canes-box-tracker', label: 'Raising Canes Box Index' },
        ...(hasSharedFolderRead ? [{ href: '/shared', label: 'Shared Folder' }] : []),
        { href: '/vin-decoder', label: 'VIN Decoder' },
        { href: '/wfl', label: "What's For Lunch" },
        { href: '/zip-coordinates', label: 'ZIP Coordinates' },
    ];
}

export function topLevelNavItems(isAuthenticated) {
    return [
        { href: '/void', label: 'Feed' },
        { href: '/void/explore', label: 'Explore' },
        { href: '/music', label: 'Music' },
        { href: messagesNavHref(isAuthenticated), label: 'Messages' },
    ];
}

export function adminMenuItems(isAdmin) {
    return isAdmin ? [
        { href: '/back-office', label: 'Back Office' },
        { href: '/command-center', label: 'Command Center' },
    ] : [];
}

export function profileMenuItems(isAdmin) {
    return adminMenuItems(isAdmin);
}
```

Proposed:
```javascript
import { accountHasMusicRead } from '../lib/music.js';
import { accountHasSharedFolderRead } from '../lib/shared-folder.js';

export function toolsMenuItems({
    hasMusicRead = false,
    hasSharedFolderRead = false,
    isAdmin = false,
} = {}) {
    return [
        ...(isAdmin ? [
            { href: '/back-office', label: 'Back Office' },
            { href: '/command-center', label: 'Command Center' },
        ] : []),
        ...(isAdmin || hasMusicRead ? [{ href: '/music', label: 'Music' }] : []),
        { href: '/canes-box-tracker', label: 'Raising Canes Box Index' },
        ...(hasSharedFolderRead ? [{ href: '/shared', label: 'Shared Folder' }] : []),
        { href: '/vin-decoder', label: 'VIN Decoder' },
        { href: '/wfl', label: "What's For Lunch" },
        { href: '/zip-coordinates', label: 'ZIP Coordinates' },
    ].sort((left, right) => left.label.localeCompare(right.label, 'en'));
}

export function topLevelNavItems(isAuthenticated) {
    return [
        { href: '/void', label: 'Feed' },
        { href: '/void/explore', label: 'Explore' },
        { href: messagesNavHref(isAuthenticated), label: 'Messages' },
    ];
}

export function profileMenuItems() {
    return [{ href: '/profile', label: 'Profile' }];
}
```

The component also initializes and clears `musicRead`, derives it with `accountHasMusicRead(account)`, passes `{ hasMusicRead, hasSharedFolderRead, isAdmin }` to `toolsMenuItems`, and renders `profileMenuItems()` instead of administrative profile links.

Verification:
- Both focused JavaScript files pass; logout/profile-load-failure code contains explicit resets for Music and Shared Folder access.

## Code Changes

- `website/src/test/js/music.test.js`: add effective Music read tests.
- `website/src/test/js/nav-messages-link.test.js`: replace old ownership expectations with gated alphabetized Tools expectations.
- `website/src/main/resources/static/js/lib/music.js`: add the pure effective-read helper.
- `website/src/main/resources/static/js/components/nav.js`: make Tools the access-aware single source and remove old menu ownership.

## Files and Modules

Four JavaScript files listed above; no server-side files or dependencies.

## Unit Testing

- Run `node --test website/src/test/js/music.test.js website/src/test/js/nav-messages-link.test.js` for RED and GREEN evidence.
- Run the repository JavaScript test task through Gradle.

## Local Testing

Run the app on a non-8080 port with an isolated database/profile appropriate to the repository. Open the home page in a browser, verify signed-out Tools excludes all three protected destinations and remains alphabetized, then use available test fixtures or the pure access-state tests for listener/admin variants. Confirm Feed, Explore, Messages, Profile, and Logout retain their expected locations.

## Validation

- Focused RED/GREEN tests.
- Full `gradlew.bat :website:check --no-daemon` with isolated Gradle state.
- Local runtime/browser smoke.
- Green PR CI and CodeQL.
- Automatic deployment and public root/navigation-asset smoke.

## Rollback or Recovery

Revert the single spoke commit and let the existing automatic deployment restore prior menu ownership. Server authorization is unchanged, so rollback has no data or permission migration.

## Risks

- Stale account capability state could advertise a protected link; explicit initialization, logout, and fetch-failure resets mitigate it.
- Positional boolean arguments could be misordered; a named options object prevents that invalid state.
- Conditional insertion could break alphabetical order; sorting the final list and testing complete arrays protects the invariant.

## Completion Criteria

One PR is merged and automatically deployed; all three destinations exist only in Tools, access visibility and alphabetical order pass focused/full tests, local runtime behavior is recorded, public production remains healthy, and Builder evidence is closed and pushed.
