# Toolbar review without Messages obstruction: Test Report

## Story/Issue
User reported Sieve covered the Messages button; replace the floating launcher with a Chrome toolbar action.

## Branch
`codex/toolbar-review-20261101` at candidate `aad2484`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `aad2484`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Toolbar review and unobstructed Messages at three viewport sizes | ✅ PASS | Expected exit code 0 |
| 2 | Native toolbar rules and storage contracts | ✅ PASS | Expected exit code 0 |
| 3 | Syntax and unchanged permissions | ✅ PASS | Expected exit code 0 |
| 4 | Updated toolbar package | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Toolbar review and unobstructed Messages at three viewport sizes**: command `node scripts/verify-browser.cjs`
2. **Native toolbar rules and storage contracts**: command `node --test tests/background.test.cjs tests/rules.test.cjs`
3. **Syntax and unchanged permissions**: command `node scripts/check.cjs`
4. **Updated toolbar package**: command `node scripts/package.cjs`

## App / Environment

| Setting | Value |
|---|---|
| Browser | Installed Chrome 156.0.8078.74; SIEVE_BROWSER_CHANNEL=chrome |
| Application | Actual unpacked extension loaded in isolated profile; X navigation routed to synthetic fixture |

## Local Run Details
- **Local command:** `node scripts/verify-browser.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node --test tests/background.test.cjs tests/rules.test.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/check.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/package.cjs` in `A:\Projects\x-spam-sieve`
- **Candidate identity:** `aad2484`
- **Cleanup:** Browser closed; owned temporary profile removed; no live account accessed or blocked.

## Data Sent

### 1. Toolbar review and unobstructed Messages at three viewport sizes

```text
node scripts/verify-browser.cjs
```

### 2. Native toolbar rules and storage contracts

```text
node --test tests/background.test.cjs tests/rules.test.cjs
```

### 3. Syntax and unchanged permissions

```text
node scripts/check.cjs
```

### 4. Updated toolbar package

```text
node scripts/package.cjs
```

## Response Received

### 1. Toolbar review and unobstructed Messages at three viewport sizes

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
PASS: stop during confirmation wait prevents both the current confirmation and subsequent accounts.
PASS: unverifiable success is recorded as uncertain; the next selected account is untouched.
BROWSER: 156.0.8078.74; extension=A:\Projects\x-spam-sieve\extension; network routed to local fixture; no signed-in account.
SCREENSHOT: C:\Users\CHRIST~1\AppData\Local\Temp\x-spam-sieve-preview.png
CLEANUP: isolated browser closed, owned temporary profile removed; no listener or live X account used.
```

### 2. Native toolbar rules and storage contracts

```text
exit code: 0
--- stdout ---
✔ toolbar action opens only the clicked tab through extension messaging (4.1066ms)
✔ worker serializes competing tabs and validates renewal ownership (1.3497ms)
✔ expired owner cannot confirm or release another lease (1.4206ms)
✔ untrusted senders and malformed storage writes are rejected (0.8484ms)
✔ history retains the latest 200 outcomes without lost concurrent writes (29.9127ms)
✔ concurrent allowlist additions are atomic and stale editors cannot overwrite them (1.434ms)
✔ ordinary conversation and language do not imply spam (1.519ms)
✔ explains promotional signals and never selects an account (0.2842ms)
✔ duplicate detection needs long text from distinct authors, not a repeat render (0.1615ms)
✔ allowlist overrides automatic rules and configured phrases are literal (0.1224ms)
✔ validates settings and handles at the storage boundary (0.4544ms)
ℹ tests 11
ℹ suites 0
ℹ pass 11
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 100.8021
```

### 3. Syntax and unchanged permissions

```text
exit code: 0
--- stdout ---
JavaScript syntax, manifest resources and least-privilege permissions passed.
```

### 4. Updated toolbar package

```text
exit code: 0
--- stdout ---
Load unpacked: A:\Projects\x-spam-sieve\dist\x-spam-sieve
```

## Evidence
- Case 1 started 2026-11-01T16:08:55-06:00, took 14860 ms, candidate `aad2484`
- Case 2 started 2026-11-01T16:09:10-06:00, took 157 ms, candidate `aad2484`
- Case 3 started 2026-11-01T16:09:10-06:00, took 406 ms, candidate `aad2484`
- Case 4 started 2026-11-01T16:09:11-06:00, took 47 ms, candidate `aad2484`

## Bugs / Follow-ups
Live signed-in X remains unverified. The actual Chrome toolbar action was invoked through Extensions.triggerAction against unique fixture tabs. The extension host is hidden before opening; the test opens and closes the review panel and clicks a bottom-right Messages fixture in both states at 1280x1000, 390x740 and 1024x500, verifying six successful clicks. The panel-only manual review, persistence, target validation, cross-tab lock, cancellation and uncertain-outcome regressions also pass. Reload the installed extension and X tab; access Sieve through Chrome's Extensions menu and optionally pin it.

## Document Status
complete

## Project
x-spam-sieve
