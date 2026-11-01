# Toolbar review without Messages obstruction: Test Report

## Story/Issue
User reported Sieve covered Messages; replace the floating launcher with a Chrome toolbar action and repair the timing-dependent confirmation fixture exposed by CI.

## Branch
`codex/toolbar-review-20261101` at candidate `6ebb7a0`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `6ebb7a0`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Toolbar layout and deterministic confirmation guards | ✅ PASS | Expected exit code 0 |
| 2 | Eleven native contracts | ✅ PASS | Expected exit code 0 |
| 3 | Syntax and manifest | ✅ PASS | Expected exit code 0 |
| 4 | Installable toolbar package | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Toolbar layout and deterministic confirmation guards**: command `node scripts/verify-browser.cjs`
2. **Eleven native contracts**: command `node --test tests/background.test.cjs tests/rules.test.cjs`
3. **Syntax and manifest**: command `node scripts/check.cjs`
4. **Installable toolbar package**: command `node scripts/package.cjs`

## App / Environment

| Setting | Value |
|---|---|
| Browser | Installed Chrome 156.0.8078.74; SIEVE_BROWSER_CHANNEL=chrome |
| Application | Actual unpacked extension in isolated profile; https://x.com/home routed to local fixture |

## Local Run Details
- **Local command:** `node scripts/verify-browser.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node --test tests/background.test.cjs tests/rules.test.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/check.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/package.cjs` in `A:\Projects\x-spam-sieve`
- **Candidate identity:** `6ebb7a0`
- **Cleanup:** Browser closed; owned temporary profile removed; no live account accessed or blocked.

## Data Sent

### 1. Toolbar layout and deterministic confirmation guards

```text
node scripts/verify-browser.cjs
```

### 2. Eleven native contracts

```text
node --test tests/background.test.cjs tests/rules.test.cjs
```

### 3. Syntax and manifest

```text
node scripts/check.cjs
```

### 4. Installable toolbar package

```text
node scripts/package.cjs
```

## Response Received

### 1. Toolbar layout and deterministic confirmation guards

```text
exit code: 0
--- stdout ---
EXTENSION: pfgoidmhagcbmmofaahoafacnkjhmfcf loaded through Chrome's extension debugging interface.
PASS: toolbar action toggles the panel; no floating button; Messages remains clickable with panel open and closed at desktop, narrow and short viewports.
PASS: actual unpacked extension loaded in Chromium; three explained suggestions, no selected accounts, no automatic blocks.
PASS: no per-post controls; panel-only manual review queues loaded authors without selecting them; markup-like post text remains inert.
PASS: allowlist and literal phrase settings survive reload and suppress matching accounts.
PASS: explicit selection and confirmation block exactly two fixture accounts, paced sequentially; concurrent tab rejected; local history records verified outcomes.
PASS: block history survives reload.
PASS: wrong-account confirmation and recycled post author both stop before an irreversible click.
PASS: deterministic production DOM-adapter regression rejects a target replaced inside the final asynchronous pre-confirm callback.
PASS: stop during confirmation wait prevents both the current confirmation and subsequent accounts.
PASS: unverifiable success is recorded as uncertain; the next selected account is untouched.
BROWSER: 156.0.8078.74; extension=A:\Projects\x-spam-sieve\extension; network routed to local fixture; no signed-in account.
SCREENSHOT: C:\Users\CHRIST~1\AppData\Local\Temp\x-spam-sieve-preview.png
CLEANUP: isolated browser closed, owned temporary profile removed; no listener or live X account used.
```

### 2. Eleven native contracts

```text
exit code: 0
--- stdout ---
✔ toolbar action opens only the clicked tab through extension messaging (4.3677ms)
✔ worker serializes competing tabs and validates renewal ownership (1.3471ms)
✔ expired owner cannot confirm or release another lease (1.4163ms)
✔ untrusted senders and malformed storage writes are rejected (1.1689ms)
✔ history retains the latest 200 outcomes without lost concurrent writes (29.0275ms)
✔ concurrent allowlist additions are atomic and stale editors cannot overwrite them (1.5321ms)
✔ ordinary conversation and language do not imply spam (1.5647ms)
✔ explains promotional signals and never selects an account (0.4271ms)
✔ duplicate detection needs long text from distinct authors, not a repeat render (0.1737ms)
✔ allowlist overrides automatic rules and configured phrases are literal (0.1209ms)
✔ validates settings and handles at the storage boundary (0.491ms)
ℹ tests 11
ℹ suites 0
ℹ pass 11
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 108.5553
```

### 3. Syntax and manifest

```text
exit code: 0
--- stdout ---
JavaScript syntax, manifest resources and least-privilege permissions passed.
```

### 4. Installable toolbar package

```text
exit code: 0
--- stdout ---
Load unpacked: A:\Projects\x-spam-sieve\dist\x-spam-sieve
```

## Evidence
- Case 1 started 2026-11-01T16:12:13-06:00, took 15452 ms, candidate `6ebb7a0`
- Case 2 started 2026-11-01T16:12:29-06:00, took 156 ms, candidate `6ebb7a0`
- Case 3 started 2026-11-01T16:12:29-06:00, took 453 ms, candidate `6ebb7a0`
- Case 4 started 2026-11-01T16:12:30-06:00, took 47 ms, candidate `6ebb7a0`

## Bugs / Follow-ups
Supersedes candidate aad2484: CI passed toolbar/layout checks but exposed a timer-dependent confirmation fixture. Candidate 6ebb7a0 uses deterministic microtasks for pre-check mutations and a separate production-DOM-adapter callback regression for post-await target replacement; production safeguards are unchanged.

Runtime inputs: invoke the actual toolbar action through Extensions.triggerAction on unique fixture tabs; open and close Sieve at 1280x1000, 390x740 and 1024x500; click bottom-right Messages in both states and observe six clicks. Exercise panel queueing, persistence, wrong/changed/replaced/duplicate confirmations, cross-tab exclusion, cancellation and uncertain-result stop. The new focused regression changes the confirmation target inside the final callback and observes zero confirmation clicks.

Live signed-in X remains unverified. Reload the installed extension and X tab; access Sieve from Chrome's Extensions menu and optionally pin it. No extra permissions were introduced.

## Document Status
complete

## Project
x-spam-sieve
