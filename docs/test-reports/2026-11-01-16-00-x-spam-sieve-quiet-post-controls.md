# Quiet post controls: Test Report

## Story/Issue
User reported that the per-post extension buttons were too intrusive; move manual review into the Sieve panel.

## Branch
`codex/quiet-post-controls-20261101` at candidate `58d7ed0`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `58d7ed0`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Panel-only review without post controls and guarded batch regression | ✅ PASS | Expected exit code 0 |
| 2 | Native rules and storage contracts | ✅ PASS | Expected exit code 0 |
| 3 | Syntax and manifest validation | ✅ PASS | Expected exit code 0 |
| 4 | Updated unpacked package | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Panel-only review without post controls and guarded batch regression**: command `node scripts/verify-browser.cjs`
2. **Native rules and storage contracts**: command `node --test tests/background.test.cjs tests/rules.test.cjs`
3. **Syntax and manifest validation**: command `node scripts/check.cjs`
4. **Updated unpacked package**: command `node scripts/package.cjs`

## App / Environment

| Setting | Value |
|---|---|
| Browser | Installed Chrome 156.0.8078.74; SIEVE_BROWSER_CHANNEL=chrome |
| Application | Actual extension/manifest.json loaded in isolated browser; https://x.com/home routed to synthetic fixture |

## Local Run Details
- **Local command:** `node scripts/verify-browser.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node --test tests/background.test.cjs tests/rules.test.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/check.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/package.cjs` in `A:\Projects\x-spam-sieve`
- **Candidate identity:** `58d7ed0`
- **Cleanup:** Owned browser closed and temporary profile removed. No live account accessed or blocked.

## Data Sent

### 1. Panel-only review without post controls and guarded batch regression

```text
node scripts/verify-browser.cjs
```

### 2. Native rules and storage contracts

```text
node --test tests/background.test.cjs tests/rules.test.cjs
```

### 3. Syntax and manifest validation

```text
node scripts/check.cjs
```

### 4. Updated unpacked package

```text
node scripts/package.cjs
```

## Response Received

### 1. Panel-only review without post controls and guarded batch regression

```text
exit code: 0
--- stdout ---
EXTENSION: pfgoidmhagcbmmofaahoafacnkjhmfcf loaded through Chrome's extension debugging interface.
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

### 2. Native rules and storage contracts

```text
exit code: 0
--- stdout ---
✔ worker serializes competing tabs and validates renewal ownership (4.7098ms)
✔ expired owner cannot confirm or release another lease (1.0639ms)
✔ untrusted senders and malformed storage writes are rejected (1.6665ms)
✔ history retains the latest 200 outcomes without lost concurrent writes (27.3303ms)
✔ concurrent allowlist additions are atomic and stale editors cannot overwrite them (1.9307ms)
✔ ordinary conversation and language do not imply spam (1.3152ms)
✔ explains promotional signals and never selects an account (0.2913ms)
✔ duplicate detection needs long text from distinct authors, not a repeat render (0.1585ms)
✔ allowlist overrides automatic rules and configured phrases are literal (0.1199ms)
✔ validates settings and handles at the storage boundary (0.4127ms)
ℹ tests 10
ℹ suites 0
ℹ pass 10
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 97.3625
```

### 3. Syntax and manifest validation

```text
exit code: 0
--- stdout ---
JavaScript syntax, manifest resources and least-privilege permissions passed.
```

### 4. Updated unpacked package

```text
exit code: 0
--- stdout ---
Load unpacked: A:\Projects\x-spam-sieve\dist\x-spam-sieve
```

## Evidence
- Case 1 started 2026-11-01T15:59:24-06:00, took 14625 ms, candidate `58d7ed0`
- Case 2 started 2026-11-01T15:59:42-06:00, took 155 ms, candidate `58d7ed0`
- Case 3 started 2026-11-01T15:59:42-06:00, took 391 ms, candidate `58d7ed0`
- Case 4 started 2026-11-01T15:59:43-06:00, took 46 ms, candidate `58d7ed0`

## Bugs / Follow-ups
Live signed-in X remains unverified. The changed UI and blocking safeguards were exercised with the actual unpacked extension in isolated Chrome, using synthetic X markup. The browser case asserts zero injected tweet buttons, opens Sieve, clicks Review loaded accounts, verifies normalhuman and markuptext appear without automatic selection, and then repeats persistence, confirmation, cross-tab, cancellation and uncertain-outcome checks. Reload the installed extension and X tabs to apply this source update.

## Document Status
complete

## Project
x-spam-sieve
