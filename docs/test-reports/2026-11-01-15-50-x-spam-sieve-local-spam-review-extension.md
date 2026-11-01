# Local spam review extension: Test Report

## Story/Issue
User requested a standalone local Chrome extension to review and batch-block bot-like spam accounts.

## Branch
`codex/local-spam-review-20261101` at candidate `e4b7d89`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `e4b7d89`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Native rule and serialized worker contracts | ✅ PASS | Expected exit code 0 |
| 2 | Syntax and minimal manifest permissions | ✅ PASS | Expected exit code 0 |
| 3 | Isolated Chrome extension runtime and guarded review block flows | ✅ PASS | Expected exit code 0 |
| 4 | Installable package build | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Native rule and serialized worker contracts**: command `node --test tests/background.test.cjs tests/rules.test.cjs`
2. **Syntax and minimal manifest permissions**: command `node scripts/check.cjs`
3. **Isolated Chrome extension runtime and guarded review block flows**: command `node scripts/verify-browser.cjs`
4. **Installable package build**: command `node scripts/package.cjs`

## App / Environment

| Setting | Value |
|---|---|
| Browser | Chrome 156.0.8078.74 |
| Isolation | Temporary browser profile; X navigation routed to synthetic fixture; no login or live blocks |
| Application entrypoint | extension/manifest.json loaded into actual Chrome through Extensions.loadUnpacked |

## Local Run Details
- **Local command:** `node --test tests/background.test.cjs tests/rules.test.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/check.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/verify-browser.cjs` in `A:\Projects\x-spam-sieve`
- **Local command:** `node scripts/package.cjs` in `A:\Projects\x-spam-sieve`
- **Candidate identity:** `e4b7d89`
- **Cleanup:** Owned browser closed and temporary profile removed; no server listener; no real X account touched.

## Data Sent

### 1. Native rule and serialized worker contracts

```text
node --test tests/background.test.cjs tests/rules.test.cjs
```

### 2. Syntax and minimal manifest permissions

```text
node scripts/check.cjs
```

### 3. Isolated Chrome extension runtime and guarded review block flows

```text
node scripts/verify-browser.cjs
Environment: SIEVE_BROWSER_CHANNEL=chrome
Application: Chrome 156.0.8078.74 loads extension/manifest.json through Extensions.loadUnpacked in an isolated temporary profile.
Navigate: https://x.com/home, intercepted with tests/fixture.html; no request reaches live X.
Fixture authors: walletspam (airdrop), normalhuman (conversation), replyfarm and replyfarmtwo (identical long reply), markuptext (literal HTML-like text).
Actions: open Sieve; manually queue normalhuman and markuptext; save phrases and walletspam allowlist; reload and verify persistence; remove allowlist; select walletspam and replyfarm; confirm batch.
Competing tab: attempt selected walletspam batch while first batch owns lease.
Failure fixtures: wrong heading, author replaced, heading changed during await, title node replaced, duplicate confirmation dialogs, delayed confirmation with Stop, success hidden after block.
Expected: only explicitly selected fixture accounts are blocked; wrong or ambiguous targets never confirmed; uncertain success stops the next account.
```

### 4. Installable package build

```text
node scripts/package.cjs
```

## Response Received

### 1. Native rule and serialized worker contracts

```text
exit code: 0
--- stdout ---
✔ worker serializes competing tabs and validates renewal ownership (4.3102ms)
✔ expired owner cannot confirm or release another lease (0.7895ms)
✔ untrusted senders and malformed storage writes are rejected (1.3259ms)
✔ history retains the latest 200 outcomes without lost concurrent writes (26.3116ms)
✔ concurrent allowlist additions are atomic and stale editors cannot overwrite them (2.1239ms)
✔ ordinary conversation and language do not imply spam (1.4338ms)
✔ explains promotional signals and never selects an account (0.2887ms)
✔ duplicate detection needs long text from distinct authors, not a repeat render (0.165ms)
✔ allowlist overrides automatic rules and configured phrases are literal (0.1188ms)
✔ validates settings and handles at the storage boundary (0.4496ms)
ℹ tests 10
ℹ suites 0
ℹ pass 10
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 94.7821
```

### 2. Syntax and minimal manifest permissions

```text
exit code: 0
--- stdout ---
JavaScript syntax, manifest resources and least-privilege permissions passed.
```

### 3. Isolated Chrome extension runtime and guarded review block flows

```text
exit code: 0
--- stdout ---
EXTENSION: pfgoidmhagcbmmofaahoafacnkjhmfcf loaded through Chrome's extension debugging interface.
PASS: actual unpacked extension loaded in Chromium; three explained suggestions, no selected accounts, no automatic blocks.
PASS: manual review queues the outer post author; markup-like post text remains inert.
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

### 4. Installable package build

```text
exit code: 0
--- stdout ---
Load unpacked: A:\Projects\x-spam-sieve\dist\x-spam-sieve
```

## Evidence
- Case 1 started 2026-11-01T15:49:35-06:00, took 139 ms, candidate `e4b7d89`
- Case 2 started 2026-11-01T15:49:35-06:00, took 375 ms, candidate `e4b7d89`
- Case 3 started 2026-11-01T15:49:41-06:00, took 15421 ms, candidate `e4b7d89`
- Case 4 started 2026-11-01T15:49:57-06:00, took 47 ms, candidate `e4b7d89`

## Bugs / Follow-ups
- Live, signed-in X blocking is unverified; this report establishes actual extension execution and guarded behavior against synthetic X markup only. X interface changes, post removal after blocking and unsupported localization can cause a safe stop or uncertain outcome.
- The downloaded Chrome for Testing 156.0.8078.4 failed to launch with a Windows side-by-side assembly error. Verification used installed Chrome 156.0.8078.74 in an owned isolated profile via the documented channel override. CI uses Playwright Chromium on Linux.
- Review reproduced and fixed an asynchronous confirmation-target race and concurrent allowlist lost updates. Final candidate includes post-await unique target checks, atomic allowlist additions and revision-protected settings saves. No outstanding code-review blockers.

## Document Status
complete

## Project
x-spam-sieve
