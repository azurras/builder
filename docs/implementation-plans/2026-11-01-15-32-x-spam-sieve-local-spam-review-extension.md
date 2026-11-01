# Review and batch-block spam accounts on X

## Document Status
complete

## Objective
> [!IMPORTANT]
> Deliver a private standalone Chrome extension that helps the user review likely spam and block selected accounts faster, using local rules without API charges.

## Background
The user currently blocks bot-like accounts by hand, requested a custom extension and a new repository, chose review before batch blocking, and then chose local detection instead of an AI API.

## Goals
- Explain likely spam and let the user queue any visible post manually (AC-1).
- Block only selected authors through X's interface, with cancellation and visible failures (AC-2).
- Keep rules, an allowlist and bounded history on the device (AC-3).
- Deliver a tested, installable extension in its own private repository (AC-4).

## Non-Goals
| Not doing | Why |
|---|---|
| AI classification or definitive bot identification | Local text rules identify patterns, not whether an author is human. |
| Chrome Web Store publication | The request authorizes a usable unpacked extension; store accounts and distribution are separate. |
| Blocking real accounts during verification | Verify using an isolated browser and synthetic X interface. |
| Language or nationality targeting | These are not evidence of spam. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Loaded posts receive review controls; repeated cross-account spam and configured phrases produce explained suggestions without automatic selection. |
| AC-2 | An explicit confirmation starts a sequential batch of at most 20 selected accounts; matching author, menu and confirmation are checked; cancellation and failures stop further blocks. |
| AC-3 | Local settings and allowlist survive reload; successful and uncertain block attempts have bounded local history; page text renders as text. |
| AC-4 | The private azurras/x-spam-sieve repository contains install instructions, native tests, browser integration checks, CI and a merged implementation PR; Builder holds the plan and candidate runtime report. |

## Inputs
- **Request:** Current chat and user choices: review then batch-block, separate repo, local rules.
- **Inspected baseline:** New repo README and initial commit 79be973; Builder instructions, spokes.json and delivery helpers at 9a75340.
- **Platform:** Chrome Manifest V3 isolated content scripts and chrome.storage.local documented at https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts and https://developer.chrome.com/docs/extensions/reference/api/storage.

## Branch
`codex/local-spam-review-20261101` from `origin/main` at `79be973`; new clean spoke checkout.

## Assumptions
- X's English interface exposes tweet articles, author links, action menus and block confirmation controls; unsupported markup must fail closed.
- Browser verification uses a synthetic X page, and cannot establish live X compatibility or detection accuracy on unseen posts.

## Open Questions
None. Routine implementation choices are delegated under the user's Builder instructions.

## Design
Use dependency-free Manifest V3 content scripts: pure scoring rules, a DOM adapter for post ownership and blocking, and a shadow-root review panel. Scan loaded posts only, debounce page changes, bound observed posts and review entries, and never choose accounts for the user. Add a manual review button for patterns rules miss. Save configuration and history through extension local storage, never page localStorage. Use a background service worker for a cross-tab batch lease and serialized settings/history mutations. Block through the visible UI, revalidate ownership immediately before every action, enforce minimum pacing, stop on uncertain confirmation, and require observed unblock state before claiming success. Support English X initially. Render untrusted content using textContent. Package only extension sources; use Node's native tests and Playwright Chromium for integration and candidate execution.

| Alternative | Why not |
|---|---|
| AI service | User chose local; adds cost and off-device processing. |
| Automatic blocking | User explicitly chose review first. |
| X private API requests | Unstable endpoints and credential handling add unnecessary risk. |

## Expected Changes
| File or area | Change |
|---|---|
| Builder spokes.json | Register the separate repository. |
| extension/manifest.json, rules.js, x-dom.js, content.js, background.js | Permissions, scoring, guarded blocking, review UI and local persistence. |
| tests/, scripts/, package.json, package-lock.json | Native behavioral tests, browser fixture, repeatable browser exercise and packaging. |
| README.md, AGENTS.md, .gitignore, .github/workflows/check.yml | Installation, development commands, ignored outputs and CI. |

## Task Breakdown
### Task 1 - Detect and review visible posts
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| Dependencies | None. |
| Files | extension/rules.js, extension/x-dom.js, extension/content.js, tests/rules.test.js, tests/fixture.html; initial README inspected at 79be973. |
| Symbols | scorePosts(posts, settings), readPostFrom(article), scanPosts(), renderPanel(). |
| Inspection | The repository is new and contains only its inspected README; Chrome docs establish classic isolated scripts and storage access. |
| Behavior | Explain local spam signals and offer manual queueing; never preselect or block. |
| Invariants | Ignore quoted authors, short duplicate phrases, allowlisted accounts, and language/nationality; bound memory and escape text. |
| Boundary/API | DOM article to validated handle, post identifier and text; pure rule results to UI suggestions. |
| Effects and failures | Own debounced observer and UI; display parsing/settings errors without widening matches. |
| Tests and evidence | Start with failing Node tests for spam versus normal posts and duplicates; exercise visible controls in Chromium. |
| Verification | npm test; npm run check; npm run verify:browser. |

### Task 2 - Guard blocking and persist local preferences
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| Dependencies | Task 1 provides validated candidate authors and review controls. |
| Files | extension/background.js, extension/x-dom.js, extension/content.js, extension/manifest.json, tests/browser.test.js, scripts/verify-browser.cjs. |
| Symbols | blockAccountFrom(candidate, signal), saveSettings(), appendHistory(), acquireBatchLease(). |
| Inspection | New repository baseline and Chrome storage documentation inspected; no prior persistence contracts. |
| Behavior | Confirm selection, take a cross-tab lease, block sequentially with pacing, verify success, record outcomes and allow stopping. |
| Invariants | Match author before menu and confirmation; no blind retries; no overlapping batches; at most 20 accounts; stop on uncertainty. |
| Boundary/API | Chrome runtime messages validate trusted extension senders and payloads; DOM controls must match expected identity; settings revisions reject stale editors and allowlist additions are atomic. |
| Effects and failures | Serialized local storage writes; lease expires after owner loss; cancellation prevents the next irreversible click. |
| Tests and evidence | Exercise allowlist, changed authors, mismatched confirmation, uncertainty, cancellation, persistence and cross-tab exclusion. |
| Verification | Native tests and isolated Chromium exercising the actual unpacked extension; capture candidate SHA, output and cleanup. |

### Task 3 - Package and deliver
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| Dependencies | Tasks 1 and 2 pass native checks and review. |
| Files | README.md, AGENTS.md, package.json, package-lock.json, .gitignore, scripts/package.cjs, .github/workflows/check.yml and Builder plan/report/memory. |
| Symbols | npm test, npm run check, npm run verify:browser, npm run package; installation instructions. |
| Inspection | Builder publication and preflight helpers inspected; new repo has no existing build policy. |
| Behavior | Produce unpacked installation folder, document limitations, run CI and merge the verified candidate. |
| Invariants | No machine paths or credentials in tracked files; runtime report published before PR; no public store upload. |
| Boundary/API | Node 24 and current Playwright Chromium; GitHub PR and Builder records. |
| Effects and failures | Package to ignored dist; push scoped commits; fix failed checks without bypassing safeguards. |
| Tests and evidence | Check package contents and load packaged manifest; review full diff and candidate runtime report. |
| Verification | Package build, candidate browser execution, Builder hub check, spoke preflight, passing CI, merged PR readback. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Node scoring and DOM ownership tests | Load actual unpacked extension in isolated Chromium on routed https://x.com fixture; inspect suggestions and manual review. |
| AC-2 | Guard failure and batch contract tests | Select and confirm fixture accounts, inspect block state; test cancel and wrong-target rejection; test cross-tab lock. |
| AC-3 | Settings validation and bounded history checks | Reload browser page, verify allowlist/settings/history; render markup-like text literally. |
| AC-4 | npm run check, npm test, package contents and CI | verify-local-app candidate run through scripts/verify-browser.cjs, publish write-test-report evidence before PR, then read back merge. |

Rerun affected checks and candidate runtime after every runtime-affecting edit. Use record_run.py for execution evidence. The extension runs in an isolated browser profile without a signed-in X account; requests to X are routed to local fixtures. Live X behavior remains explicitly unverified.

## Rollback or Recovery
Disable or remove the unpacked extension to stop scanning; cancel a batch to stop subsequent accounts. Review history and unblock through X manually. Revert repository commits through a new PR if necessary. Never delete user browser data or reset unrelated work.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| False positives | Medium | Reasons, no automatic selection, allowlist and manual control. |
| X DOM changes or localization | High | English-only adapter fails closed on ambiguous controls; document live compatibility limitation. |
| Rate limits | Medium | Five-second minimum spacing, bounded batches and stop on first failure; no guarantee against X limits. |
| Account changes while queued | Medium | Revalidate current article author and target controls immediately before each click. |

## Implementation Log
### 2026-11-01 - Implement local review and guarded blocking

- **Change:** Implemented all three tasks in the new standalone spoke, using the clean branch checkout rather than a linked worktree because it has no unrelated changes. Selected local rules and review-first flow follow the user's choices.
- **Reason:** The new repository has no existing application or shared checkout work to preserve; product sources remain separate from Builder records.
- **Impact:** Native rule tests first failed for the missing module and then passed; isolated browser execution exercises the actual loaded extension, not only JavaScript helpers.

### 2026-11-01 - Use installed Chrome for isolated runtime proof

- **Change:** Browser verification supports an explicit browser channel and loads the unpacked extension through Chrome's DevTools Extensions.loadUnpacked interface. Local runs use installed Chrome 156.0.8078.74; CI uses Playwright Chromium.
- **Reason:** Downloaded Chrome for Testing 156.0.8078.4 fails before startup with a missing side-by-side assembly. Installed Chrome launches, but its removed load-extension flag does not load extensions; its supported debugging interface does.
- **Impact:** Browser isolation and routed fixtures remain unchanged. No user profile or Chrome installation is altered. Live signed-in X compatibility remains unverified.

### 2026-11-01 - Close review races before publication

- **Change:** A fresh read-only reviewer reproduced confirmation-target replacement during asynchronous checks and identified concurrent allowlist lost updates. Revalidate the unique connected confirmation and current target after the final await, add an atomic allowlist mutation, and reject stale full-settings writes using revisions.
- **Reason:** A wrong-account confirmation must never be clicked, and separate tabs must not silently remove each other's protections.
- **Impact:** Added failing-then-passing concurrent storage regression and browser target-change regression; rerun affected native and candidate browser checks before PR publication. No scope expansion.

### 2026-11-01 - Move intrusive post controls into the panel

- **Change:** User found per-post controls intrusive. Removed all injected review buttons from tweet articles and moved manual queueing to Review loaded accounts inside the existing Sieve panel; updated README and browser regression. This is a three-file fast-track follow-up inside the original review workflow goals.
- **Reason:** Keep the X timeline untouched while preserving manual account review. No changes to detection, storage, permissions or blocking safeguards. Reviewed complete diff with write-chris-street-style-code; the regression failed with five per-post buttons before the fix, then passed with zero.
- **Impact:** Candidate 58d7ed0 passes actual isolated Chrome execution, all 10 native tests, syntax/manifest checks and packaging. Live signed-in X remains unverified. The initial release's per-post manual controls are superseded by panel-only controls; the original completed delivery and its evidence remain historical.

### 2026-11-01 - Read back panel-only review delivery

- **Change:** Panel-only review follow-up merged through PR #2 as 37d2788403f6688dcf497e38cd79ab793ae229be after successful CI on candidate 58d7ed0; merged source matches the locally verified extension.
- **Reason:** Completes the user's request to remove intrusive controls beside posts while preserving manual review inside Sieve.
- **Impact:** [Follow-up runtime report](../test-reports/2026-11-01-16-00-x-spam-sieve-quiet-post-controls.md) covers zero per-post controls and unchanged blocking safeguards. Updated source folder, packaged folder and ZIP are available locally. User must reload the unpacked extension and X tab to apply it; no browser UI was automated for this follow-up.

## Outcome
> [!TIP]
> Delivered the private standalone extension through [PR #1](https://github.com/azurras/x-spam-sieve/pull/1), merged as `8e8c17c2b4842024d08c660bfee603edfd0b99cd` after successful CI on reviewed candidate `e4b7d89`. The extension folder loads directly in Chrome without a build or API key.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met against the supported synthetic interface | [Candidate runtime report](../test-reports/2026-11-01-15-50-x-spam-sieve-local-spam-review-extension.md): explained suggestions, manual queueing, inert post text and no automatic selection. |
| AC-2 | ✅ Met against the supported synthetic interface | Runtime checks exercised explicit selection and confirmation, sequential pacing, cross-tab exclusion, cancellation, changed author and wrong/changed/replaced/duplicate confirmations, plus uncertain-result stop. |
| AC-3 | ✅ Met | Ten native tests include concurrent writes, bounded history, atomic allowlist additions and stale settings rejection; browser reload confirms saved rules, allowlist and history. |
| AC-4 | ✅ Met | [CI run](https://github.com/azurras/x-spam-sieve/actions/runs/41354097230) passed native tests, syntax/manifest checks, Linux Chromium runtime and packaging; PR readback is MERGED; source and package manifest SHA-256 match. |

Shipped local text rules and manual review, not definitive AI/bot classification. No remaining code-review blockers. Live signed-in X behavior remains unverified; unsupported markup or post disappearance can safely stop a batch. No Chrome Web Store publication or installation into the user's browser was performed. Successful browser runs cleaned their owned profiles; automatic approval review rejected cleanup of the initial failed-run temporary profile as blocked by policy, so that profile remains. The local checkout is on merged main; no source issue exists and external closure does not apply.

## Project
x-spam-sieve

## Plan Format
task-contract-v2
