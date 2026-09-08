# 2026-08-02 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/session-memory/2026-08-02-openstreetmap-import-rename-collision-fix.md](#source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md)
- [docs/session-memory/2026-08-02-restaurant-profile-void-seo.md](#source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md)
- [docs/session-memory/2026-08-02-restore-bootstrap-webjar-assets.md](#source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md)
- [docs/session-memory/2026-08-02-wfl-location-integrity-and-reconciliation.md](#source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md)
- [docs/session-memory/2026-08-02-wfl-rating-weighted-void-upgrade.md](#source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md)
- [docs/specs/2026-08-02-christopherbell-dev-osm-import-rename-collision.md](#source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md)
- [docs/specs/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md](#source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md)
- [docs/specs/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md)
- [docs/specs/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md)
- [docs/specs/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md)
- [docs/specs/2026-08-02-restore-bootstrap-assets-after-webjar-version-bump.md](#source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md)
- [docs/spoke-reviews/2026-08-02-bootstrap-webjar-asset-repair.md](#source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md)
- [docs/spoke-reviews/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review.md](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md)
- [docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-location-integrity-review.md](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md)
- [docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review.md](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md)
- [docs/spoke-reviews/2026-08-02-restaurant-profile-void-seo-review.md](#source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md)
- [docs/spoke-updates/2026-08-02-bootstrap-webjar-asset-repair.md](#source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md)
- [docs/spoke-updates/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion.md](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md)
- [docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-location-integrity-completion.md](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md)
- [docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion.md](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md)
- [docs/spoke-updates/2026-08-02-restaurant-profile-void-seo.md](#source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md)
- [docs/work-closures/2026-08-02-bootstrap-webjar-asset-repair.md](#source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md)
- [docs/work-closures/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure.md](#source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md)
- [docs/work-closures/2026-08-02-christopherbell-dev-wfl-location-integrity-closure.md](#source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md)
- [docs/work-closures/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure.md](#source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md)
- [docs/work-closures/2026-08-02-restaurant-profile-void-seo.md](#source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md)
- [docs/work/2026-08-02-christopherbell-dev-bootstrap-asset-regression.md](#source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md)
- [docs/work/2026-08-02-christopherbell-dev-osm-import-rename-collision.md](#source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md)
- [docs/work/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md](#source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md)
- [docs/work/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md](#source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md)
- [docs/work/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md](#source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md)

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md"></a>
## 2026-08-02 | session-memory | 2026-08-02 - OpenStreetMap import rename collision fix

Original source: `docs/session-memory/2026-08-02-openstreetmap-import-rename-collision-fix.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `fcead11977b92923cf14b1d1b84d263e7e963e23afe3a7d07fba62a84beb4e07`.

<!-- migrated-source: docs/session-memory/2026-08-02-openstreetmap-import-rename-collision-fix.md -->
<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--2026-08-02---openstreetmap-import-rename-collision-fix"></a>
### 2026-08-02 - OpenStreetMap import rename collision fix

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--1314---openstreetmap-import-rename-collision-fix"></a>
#### 13:14 - OpenStreetMap import rename collision fix

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--request"></a>
##### Request

The user asked whether the recurring `RestaurantImportWorkflowService` startup-catch-up error could be fixed, chose the recommended behavior, and approved delivery. The supplied production log was a MongoDB `DuplicateKeyException` on unique `whatsforlunch.normalizedName` value `aama's kitchen`. Required constraints were to preserve the unique-name rule, preserve dirty authoritative checkouts, use isolated worktrees and alternate-port validation, avoid direct production data rewrites, retain causal errors for genuine failures, and complete PR/CI/merge/production delivery.

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--project-context"></a>
##### Project Context

Builder coordinates `azurras/christopherbell.dev`. The authoritative checkout `A:\Projects\christopherbell.dev` was dirty and stale, so work used `A:\Projects\christopherbell.dev-worktrees\restaurant-import-duplicate-name-20260802`. The Windows host is also production; deployment runs through the protected SYSTEM auto-deployer and native services. Non-elevated ACL denial under `C:\ProgramData\christopherbell.dev` is expected and was not weakened.

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--root-cause-and-decision"></a>
##### Root Cause and Decision

Production and upstream inspection established that OpenStreetMap node `8178213204` changed from persisted `China Villa` to `Aama's Kitchen`, while node `13485126044` already owned normalized name `aama's kitchen` at another location. The import's ID-first branch mutated/saved the ID match without checking the incoming normalized-name owner, so MongoDB correctly rejected it and the workflow marked the whole catch-up failed. The approved behavior preserves global name uniqueness, skips only that conflicting rename before mutation, continues later candidates, reports preview unchanged/apply skipped existing, logs the expected branch at DEBUG, and leaves unrelated failures causal and visible.

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--work-completed"></a>
##### Work Completed

- Saved and executed the approved Builder spec and literal-line implementation plan.
- Added `hasConflictingNormalizedNameOwner` to `RestaurantService`, called before preview classification and before apply merge/save.
- Added exact `China Villa` / `Aama's Kitchen` regression with a later continuation candidate.
- Updated the restaurant feature README.
- Spoke implementation commit: `3fdbafc0809a290f09504bb7fb9f8d201fc75e25`.
- Opened ready PR `https://github.com/azurras/christopherbell.dev/pull/1341`; required CI passed.
- Squash-merged as `0dd388fb096c924453bdbab8b66a3215d3e63452`.
- SYSTEM auto-deployer built and cut over the exact merged release; Mission Control reports application commit `0dd388fb`.

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--validation"></a>
##### Validation

- Regression-first RED: preview incorrectly reported one update before the implementation.
- Focused collision test GREEN; all 56 `RestaurantServiceTest` tests passed.
- `:website:test --no-daemon`: exit 0, 2m35s.
- `:website:check --no-daemon`: exit 0, 2m58s.
- Alternate-port runtime on 8096 with isolated MongoDB and loopback Overpass: status `SUCCEEDED`, fetched 2, imported 1, updated 0, skipped existing 1; existing records unchanged, later candidate imported, readiness/nearby HTTP 200, no duplicate-key/workflow error; task processes stopped and isolated database dropped.
- Independent code review: no Critical, Important, or Minor findings.
- GitHub CI: Ubuntu/macOS/Windows builds, Dependency Review, and all CodeQL checks passed.
- Production catch-up: `SUCCEEDED`, `lastCompletedMonth=2026-08`, fetched 20,000, imported 296, updated 442, skipped existing 19,262, skipped invalid 0.
- Production collision records retained their original names, normalized names, addresses, and May 21 `lastUpdatedOn` timestamps.
- Readiness, liveness, local homepage, public homepage, and production nearby endpoint returned HTTP 200; required security headers were present.
- MongoDB, ChristopherBellDev, ChristopherBellMediaWorker, and cloudflared remained Running/Automatic.
- Refreshed Mission Control logs ended with successful import completion; literal current-release searches for `DuplicateKeyException` and `OpenStreetMap import failed` returned no records.

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--durable-artifacts"></a>
##### Durable Artifacts

- Work: `docs/work/2026-08-02-christopherbell-dev-osm-import-rename-collision.md`
- Spec: `docs/specs/2026-08-02-christopherbell-dev-osm-import-rename-collision.md`
- Plan: `docs/implementation-plans/2026-08-02-christopherbell-dev-osm-import-rename-collision.md`
- Test report: `docs/test-reports/2026-08-02-openstreetmap-import-rename-collision-test-report.md`
- Spoke update: `docs/spoke-updates/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion.md`
- Spoke review: `docs/spoke-reviews/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review.md`

<a id="source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md--current-state-and-follow-ups"></a>
##### Current State and Follow-ups

Production is healthy on merged commit `0dd388fb`. No required code, data, operational, or issue follow-up remains. The feature worktree intentionally remains available for PR provenance; its only uncommitted status is the known checkout-only `gradlew.bat` line-ending artifact with an empty `--ignore-space-at-eol` diff. The detached deployment evidence worktree is `A:\Projects\christopherbell.dev-worktrees\osm-import-merge-0dd388fb`. Do not clean unrelated historical worktrees.

<!-- /migrated-source: docs/session-memory/2026-08-02-openstreetmap-import-rename-collision-fix.md -->

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md"></a>
## 2026-08-02 | session-memory | 2026-08-02 Restaurant Profile Void SEO

Original source: `docs/session-memory/2026-08-02-restaurant-profile-void-seo.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `59c6ce2ade8304c521569860d013967a070a17b6aa17c51ef65ba695f3c67672`.

<!-- migrated-source: docs/session-memory/2026-08-02-restaurant-profile-void-seo.md -->
<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--2026-08-02-restaurant-profile-void-seo"></a>
### 2026-08-02 Restaurant Profile Void SEO

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--2247---completed-restaurant-profile-void-and-indexing-delivery"></a>
#### 22:47 - Completed restaurant profile Void and indexing delivery

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--request"></a>
##### Request

Apply the established Void CSS to restaurant profile pages and make valid profiles indexable by search engines. Preserve the approved boundary that all valid profiles are indexable, public content is server-rendered, personal controls are progressive enhancement, and private member/audit fields never enter public HTML or structured data.

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--project-context"></a>
##### Project Context

The Builder hub coordinated `azurras/christopherbell.dev`. Work used the isolated worktree `A:\Projects\christopherbell.dev-worktrees\restaurant-profile-void-seo` from base `9c69623049829394f245515b8d1751c9f7579271`; the dirty authoritative checkout at `A:\Projects\christopherbell.dev` was preserved. Production port `8080` remained untouched until alternate-port acceptance and PR CI passed.

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--work-completed"></a>
##### Work Completed

- Added immutable `RestaurantProfilePage` and `RestaurantProfilePageService` public projection types.
- Replaced the limited social-preview projection and server-rendered complete semantic public restaurant details in `restaurant.html`.
- Added canonical/social metadata and conditional Jackson-serialized schema.org `Restaurant` JSON-LD with safe optional-field handling.
- Reduced `restaurant-profile.js` to authenticated rating/favorite enhancement and kept anonymous/public content independent of API fetch success.
- Moved profile presentation from shared `main.css` into scoped `whats-for-lunch.css` Void ownership.
- Added Java and JavaScript coverage for hostile/sparse data, invalid IDs, privacy, raw SSR output, member controls, stylesheet ownership, accessibility, desktop wrapping, and mobile overflow.
- Updated WFL, JavaScript, and CSS ownership documentation.
- Opened PR #1345; all CI and CodeQL checks passed; squash-merged as `363bb986581c4d20df3434154844807ce88701e4`.
- Deployed through the protected Windows production path and verified the new release through loopback and Cloudflare.

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--decisions"></a>
##### Decisions

- One public-only immutable page model is the only restaurant object exposed to Thymeleaf.
- All valid profiles remain in the public sitemap regardless of rating.
- Missing/malformed profiles remain content-free 404 responses with `noindex,nofollow` and no JSON-LD.
- Unsafe website values and unavailable optional properties are omitted.
- Top Rated and Favorites retain their prior presentation.

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--validation"></a>
##### Validation

- Regression-first focused tests all passed.
- Final `:website:check --rerun-tasks --no-daemon --console=plain`: `BUILD SUCCESSFUL in 3m 14s`, 21 tasks executed.
- JavaScript: 320 passed. Windows production scripts: 74 passed, zero failed.
- Candidate port `8094`: liveness/readiness, robots, sitemap, complete/sparse/missing raw HTML, parsed JSON-LD, privacy sentinels, desktop/mobile layout, keyboard focus, authenticated rating/favorite mutations, and stale-session fallback passed.
- Browser console errors: none.
- GitHub: Ubuntu, macOS, Windows, dependency review, Actions CodeQL, Java/Kotlin CodeQL, and JavaScript/TypeScript CodeQL passed.
- Production: listener rotated from PID `55848` to PID `59036`; local and public liveness/readiness returned 200; sitemap contained 7,340 profile URLs; real profile `Boogaloos` returned canonical indexable Void HTML and Restaurant JSON-LD; versioned assets `/29e5fee580df3dc0a71e/css/whats-for-lunch.css` and `/29e5fee580df3dc0a71e/js/restaurant-profile.js` returned exact new behavior; missing profile returned 404 noindex without JSON-LD; all required services ran.
- Candidate PID and exact isolated database `christopherbell_dev_restaurant_profiles_void_seo` were removed after local testing.

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--current-state"></a>
##### Current State

PR #1345 is merged and production is healthy. The spoke worktree still has only the known line-ending-only `gradlew.bat` modification, which was never staged. The Builder test report is `docs/test-reports/2026-08-02-restaurant-profile-void-seo-test-report.md`.

<a id="source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md--follow-ups"></a>
##### Follow-ups

None required. Preserve the public/private projection invariant in future restaurant profile work.

<!-- /migrated-source: docs/session-memory/2026-08-02-restaurant-profile-void-seo.md -->

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md"></a>
## 2026-08-02 | session-memory | 2026-08-02 - Restore Bootstrap WebJar Assets

Original source: `docs/session-memory/2026-08-02-restore-bootstrap-webjar-assets.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `46fd39bba1586197ebdec4140d1f7fb2d6e3c48bb661790bb46156b3023ab81a`.

<!-- migrated-source: docs/session-memory/2026-08-02-restore-bootstrap-webjar-assets.md -->
<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--2026-08-02---restore-bootstrap-webjar-assets"></a>
### 2026-08-02 - Restore Bootstrap WebJar Assets

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--1204---restore-bootstrap-webjar-assets"></a>
#### 12:04 - Restore Bootstrap WebJar Assets

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--request"></a>
##### Request

Diagnose and fully repair the production site after the user reported that some
CSS loaded while other styling and a Bootstrap URL failed with 404.

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--project-context"></a>
##### Project Context

The authoritative `A:\Projects\christopherbell.dev` checkout was dirty, ahead,
and stale, so it was preserved untouched. Work ran in
`A:\Projects\christopherbell.dev-worktrees\bootstrap-assets-1339` on
`codex/issue-1339-bootstrap-assets` from refreshed origin/main
`2b40bd860d9e4e05aa18b4dd63e13a390d41208e`. Production is native Windows on
port 8080 and was validated first on alternate port 8091.

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--root-cause-and-work-completed"></a>
##### Root Cause and Work Completed

Dependency update commit `20290b2f` moved Bootstrap from 5.3.3 to 5.3.8 but left
runtime templates/CSS imports and both exact security boundaries pinned to
5.3.3. Production requested missing 5.3.3 assets, while valid 5.3.8 assets were
403.

Created issue #1339 and updated 19 spoke files: all runtime WebJar references,
`SecurityConfig`, `StaticAssetRequestMatcher`, security/CSS docs, dependency-
derived JavaScript coverage, public matcher tests, and a direct
`StaticAssetRequestMatcherTest`. Commits `09606ebd87feacc9ad5828c0203fc6dd7ffd4d55`
and `facfa97cdb33dd144fbe4aedae5cbc2e45fc2ea3` were pushed. PR #1340 passed
review and CI, then squash-merged as
`5bd14e994a6130a32166602a6f272581abc53525`; issue #1339 closed automatically.

Builder artifacts include the completed spec, implementation plan, test report,
spoke update/review, work closure, and central work record for this repair.

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--decisions"></a>
##### Decisions

Pinned runtime/security paths to the packaged 5.3.8 version and added a test that
derives the version from `website/build.gradle.kts` so a future dependency-only
bump fails. Kept the exact WebJar allowlist instead of broadening `/webjars/**`.
After independent review exposed a direct matcher-test gap, added boundary tests
for GET/POST, current/obsolete versions, and unrelated namespaces. Preserved the
authoritative dirty checkout and did not weaken protected production ACLs.

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--validation"></a>
##### Validation

- TDD RED reproduced 5.3.3 versus 5.3.8; GREEN contract tests passed.
- Focused `SecurityConfigTest` passed 16/16 and direct matcher coverage passed.
- `:website:jsTest` passed 312/312.
- Final `:website:check` was BUILD SUCCESSFUL in 3m20s with 1,610 Java tests,
  150 Pester tests, zero failures/errors, and 3 skipped Java tests.
- Alternate-port packaged app readiness was UP; pages and current Bootstrap CSS/
  JS returned 200 with exact signatures; obsolete paths returned 403; browser
  computed styles and logs passed.
- Independent re-review reported no actionable findings and Ready to merge: Yes.
- GitHub Linux/macOS/Windows builds, CodeQL, and dependency review passed.
- Production rotated from PID 33024 to PID 2956. A transient readiness 503 became
  200 UP; liveness was UP. Public current assets return 200, obsolete assets 403,
  login/signup reference 5.3.8, browser styles load with no logs, and
  ChristopherBellDev, MongoDB, and cloudflared are Running/Automatic.

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--current-state"></a>
##### Current State

The feature branch is merged and issue #1339 is closed. The isolated worktree
retains only the known CRLF-only `gradlew.bat` checkout artifact, which was never
staged. The authoritative dirty checkout remains untouched. Production is
healthy on the merged release.

<a id="source-docs-session-memory-2026-08-02-restore-bootstrap-webjar-assets-md--follow-ups"></a>
##### Follow-ups

No issue-scoped follow-up remains. The test report records an unrelated local-
profile WFL duplicate-key catch-up log for future WFL work.

<!-- /migrated-source: docs/session-memory/2026-08-02-restore-bootstrap-webjar-assets.md -->

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md"></a>
## 2026-08-02 | session-memory | 2026-08-02 - What's for Lunch location integrity and reconciliation

Original source: `docs/session-memory/2026-08-02-wfl-location-integrity-and-reconciliation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `268af34721980d8ed909326fcb0c3ab00d0cfcfe276ac9c4cc833cce6fac5baa`.

<!-- migrated-source: docs/session-memory/2026-08-02-wfl-location-integrity-and-reconciliation.md -->
<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--2026-08-02---whats-for-lunch-location-integrity-and-reconciliation"></a>
### 2026-08-02 - What's for Lunch location integrity and reconciliation

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--1752---whats-for-lunch-location-integrity-and-reconciliation"></a>
#### 17:52 - What's for Lunch location integrity and reconciliation

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--request"></a>
##### Request

The user reported that What's for Lunch invented `Imported Metro, TX` whenever source data lacked a restaurant location and required either a real location or exclusion. The user approved strict import enforcement, exact placeholder cleanup, and later selected the recommended expanded reconciliation: retain every restaurant whose real locality can be proven and omit only the rest.

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--project-context"></a>
##### Project Context

Builder coordinated `azurras/christopherbell.dev`. The authoritative checkout `A:\Projects\christopherbell.dev` was dirty and preserved; implementation used isolated worktree `A:\Projects\christopherbell.dev-worktrees\wfl-import-location-integrity-20260802`. The Windows development host is also production, so candidate runtime testing used port 8098 and isolated MongoDB before protected deployment to port 8080. Production ACLs were not weakened.

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--work-completed"></a>
##### Work Completed

- PR #1342 removed the fabricated fallback, enforced supported canonical locations, added regression tests, merged as `178d90caca58d2f6284f54ab2ef4514d10df2918`, and deployed.
- A verified backup preceded deletion of 6,825 exact `Imported Metro` OSM rows; a strict reimport did not recreate them.
- Official Census 2025 Gazetteer and TIGERweb analysis expanded the four configured rectangles to 393 unique incorporated places and CDPs.
- PR #1343 added complete configuration coverage, coordinate-aware duplicate city resolution, full state-name aliases, city/rectangle contradiction rejection, independent service validation, tests, and README documentation. It merged and deployed as `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`.
- The live import completed with fetched 10,796, imported 86, updated 136, skipped existing 10,574, skipped invalid 0.
- A new 2,050,494-byte backup was taken and passed `mongorestore --dryRun` before mutation.
- A fresh post-import TIGERweb manifest resolved 199 of 215 remaining violations and found no Census place for 16. Exact-ID drift checks passed; 199 were updated and 16 deleted. No favorites or ratings referenced the deleted IDs, and sessions were preserved.

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--decisions"></a>
##### Decisions

- Never infer or fabricate a city from a metro label, ZIP code, neighborhood, airport name, or nearest-city heuristic.
- Use current official Census place polygons for correction and deletion decisions.
- Keep all place data pinned in the application; Census remains a build/reconciliation source rather than a runtime dependency.
- Disambiguate same-name places using coordinates and optional state evidence.
- Apply production changes only after a verified backup and an immutable checksum-pinned exact-ID manifest.

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--validation"></a>
##### Validation

- Focused final suite: 78 tests passed.
- Full `:website:test`: 1,620 tests, 0 failures, 0 errors, 3 skipped.
- Full `:website:check`: passed, including 76 Pester executions.
- Packaged candidate runtime on port 8098 passed with exact accepted/rejected fixture evidence; test processes stopped and isolated database dropped.
- Both PRs passed required CI and exact merged releases deployed healthy.
- Final production audit: 7,338 OSM rows, all 7,338 valid, 0 violations, 0 synthetic metro placeholders; 7,340 total restaurants.
- Readiness/liveness HTTP 200 `UP`, MongoDB ping `ok: 1`, listener PID `57904`.
- Public nearby requests for Austin, Bay Area, New Orleans, and Dallas returned HTTP 200 and canonical city/state/`US` results.

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--evidence-and-recovery"></a>
##### Evidence and Recovery

- Backup: `A:\Backups\christopherbell.dev\christopherbell-before-wfl-legacy-reconciliation-20260802-224634.archive.gz`, SHA-256 `E8999314FC31EB440D5A142D317F628231B4B6BA25962C30FAA4F000CD92CD23`.
- Manifest: `A:\Backups\christopherbell.dev\wfl-production-reconciliation-manifest-20260802-224741.json`, SHA-256 `A6391EFC45FB88033B25DEA77A06C2C358E551A256EA69FFB59C53F624677918`.
- Receipt: `A:\Backups\christopherbell.dev\wfl-production-reconciliation-receipt-20260802-224800.json`, SHA-256 `F76FBD81E7401BBC85C3DB35EA52334E792D1B95DB541601D1E1197B44BA12E4`.
- Final audit: `A:\Backups\christopherbell.dev\wfl-production-final-invariant-audit-20260802-225100.json`, SHA-256 `E3E31D0B5F5C5A7283DA22DF1CFE5EB4EF234229CEFF9F2588F37B4857ACA055`.
- The backup is the rollback boundary if later data inspection discovers an unexpected issue.

<a id="source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md--current-state-and-follow-ups"></a>
##### Current State and Follow-ups

Production is healthy on merged commit `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`. The Builder work record is closed and no required follow-up remains. Refresh the pinned Census coverage only through a deliberate reviewed change when adopting a newer geography vintage. Preserve unrelated historical worktrees and the dirty authoritative checkout.

<!-- /migrated-source: docs/session-memory/2026-08-02-wfl-location-integrity-and-reconciliation.md -->

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md"></a>
## 2026-08-02 | session-memory | 2026-08-02 - WFL rating-weighted Void upgrade

Original source: `docs/session-memory/2026-08-02-wfl-rating-weighted-void-upgrade.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `e52b387f9948b84bfd0edfd6a870440df602199ee906b187f597334b245a6812`.

<!-- migrated-source: docs/session-memory/2026-08-02-wfl-rating-weighted-void-upgrade.md -->
<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--2026-08-02---wfl-rating-weighted-void-upgrade"></a>
### 2026-08-02 - WFL rating-weighted Void upgrade

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--2017---wfl-rating-weighted-void-upgrade"></a>
#### 20:17 - WFL rating-weighted Void upgrade

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--request"></a>
##### Request

The user asked for the three What's for Lunch restaurants to account for ratings so highly rated restaurants appear more often and low-rated restaurants appear less often, and requested that the page CSS be upgraded to the Void style. The user approved the Decision Console direction and autonomous execution through delivery.

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--project-context"></a>
##### Project Context

Builder coordinated `azurras/christopherbell.dev`. The authoritative checkout `A:\Projects\christopherbell.dev` was dirty and preserved; implementation used isolated worktree `A:\Projects\christopherbell.dev-worktrees\wfl-rating-weighted-void` on `codex/wfl-rating-weighted-void`. The Windows development host is also production, so candidate testing used port 8081 and production port 8080 was not touched until the scheduled deployment pipeline rotated it. Protected ProgramData ACLs were not weakened.

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--work-completed"></a>
##### Work Completed

- Added a rating-weighted selector with a three-rating neutral prior, approved piecewise-linear weights, positive eligibility probability, deterministic injection seam, validation, and sampling without replacement.
- Added one batch MongoDB rating-summary aggregation and wired coordinate/ZIP, daily refresh, and deleted-pick replacement flows through it while preserving persisted order.
- Rebuilt `/wfl` as a dedicated scoped Void Decision Console with three equal desktop cards, a one-column mobile layout, exact rating-influence disclosure, no numeric ranking, accessible focus, and reduced-motion handling.
- Added Java and JavaScript regressions and updated WFL/CSS documentation.
- Independent review found an authenticated rating-color cascade. A failing regression reproduced it; commit `58019300` directly styles both anonymous and authenticated rating paragraphs. Re-review returned ready to merge with no findings.
- PR #1344 passed all required checks, merged as `9c69623049829394f245515b8d1751c9f7579271`, and auto-deployed.

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--decisions"></a>
##### Decisions

- Adjusted rating is `(ratingSum + 9) / (ratingCount + 3)`; unrated is neutral 3-star.
- Weight anchors are 1=0.35, 2=0.60, 3=1.00, 4=1.50, and 5=2.00 with linear interpolation.
- Selection is without replacement and all eligible candidates retain a positive chance.
- Existing daily and shared-session picks remain stable until normal refresh/reset.
- The new visual layer belongs only to `/wfl`; Top Rated, Favorites, and profile pages retain existing ownership.

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--validation"></a>
##### Validation

- Focused final coverage: 8 selector tests, 3 rating query tests, 60 service tests, and 313 JavaScript tests passed.
- Final `:website:check` passed after review correction in 2 minutes 56 seconds, including 150 Pester tests and deployment verification tasks.
- Alternate-port Spring Boot runtime on 8081 passed health, page, today, coordinate, and ZIP HTTP checks plus desktop/mobile Chrome inspection.
- GitHub Windows/macOS/Ubuntu builds, dependency review, and CodeQL for Actions, Java/Kotlin, and JavaScript/TypeScript all passed.
- The merged tree exactly matched the verified feature tree. Production listener rotated from PID 57904 to 55848 and published fingerprinted asset `db0009f03ea001ffc654`.
- Public HTTPS liveness/readiness were `UP`; `/wfl` and three selection paths returned HTTP 200 with real locations and no synthetic metro placeholder.
- Authenticated production browser inspection verified equal cards, zero overflow, corrected 9.06:1 rating contrast, no ranking badges, and no console warnings/errors.

<a id="source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md--current-state-and-follow-ups"></a>
##### Current State and Follow-ups

Production is healthy on the merged release. Builder artifacts are closed, and no required follow-up remains. Preserve the isolated worktree until any post-merge operational window ends; its only dirty file is the known baseline `gradlew.bat` line-ending anomaly, which was never staged or committed.

<!-- /migrated-source: docs/session-memory/2026-08-02-wfl-rating-weighted-void-upgrade.md -->

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md"></a>
## 2026-08-02 | specs | christopherbell.dev OpenStreetMap Import Rename Collision

Original source: `docs/specs/2026-08-02-christopherbell-dev-osm-import-rename-collision.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `becf6afdffb6e36ef86aa45be5e9458a33f6800ab71c63b03e94fcf86a0c2341`.

<!-- migrated-source: docs/specs/2026-08-02-christopherbell-dev-osm-import-rename-collision.md -->
<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--christopherbelldev-openstreetmap-import-rename-collision"></a>
### christopherbell.dev OpenStreetMap Import Rename Collision

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--document-status"></a>
#### Document Status

Complete. The approved behavior was implemented, merged, deployed, and production-verified on 2026-08-02.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--purpose"></a>
#### Purpose

Make the OpenStreetMap restaurant import resilient when an already-persisted OpenStreetMap ID is renamed upstream to a normalized name owned by another restaurant. The candidate must be skipped consistently instead of violating MongoDB's unique-name constraint and aborting the complete scheduled import.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--background"></a>
#### Background

The supplied production log records a startup catch-up import failing in `RestaurantService.applyPreparedImport` with MongoDB error `E11000` for normalized name `aama's kitchen`.

The current data flow is:

1. Normalize the incoming OpenStreetMap restaurant name.
2. Look up a persisted restaurant by the incoming OpenStreetMap ID.
3. If that ID exists, merge all incoming import fields and save immediately.
4. Only when the ID does not exist, look up a restaurant by normalized name and apply the same-name/address duplicate rule.

Read-only production and upstream inspection confirmed the concrete collision:

- `osm:node:8178213204` is persisted as `China Villa` in Livermore, California, but OpenStreetMap now calls it `Aama's Kitchen`.
- `osm:node:13485126044` is a different physical location already persisted as `Aama's Kitchen` and owns normalized name `aama's kitchen`.
- The ID-first update path attempts to replace `China Villa` with the conflicting name and bypasses the duplicate-name rule used by the insert path.

This is a real import control-flow defect. Downgrading or suppressing the exception would hide a failed monthly import and leave its durable completion state incorrect.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--goals"></a>
#### Goals

- Preserve the unique `normalizedName` invariant.
- Apply the same-name/different-address collision rule before an ID-based update mutates or saves a restaurant.
- Skip only the conflicting candidate and continue processing the remaining snapshot.
- Keep import preview counts consistent with apply results.
- Treat the expected collision as a concise non-error diagnostic while retaining `ERROR` and causal stack traces for genuine import failures.
- Prove the behavior with a regression test that models the exact upstream rename pattern.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--non-goals"></a>
#### Non-Goals

- Do not change the unique MongoDB index or allow duplicate normalized names.
- Do not delete, merge, or re-key restaurant documents.
- Do not rewrite the existing `China Villa` or `Aama's Kitchen` production records.
- Do not change ratings, favorites, sessions, public API shapes, import scheduling, lease behavior, or OpenStreetMap query coverage.
- Do not catch and suppress arbitrary `DuplicateKeyException` instances; unexpected persistence failures must remain true errors.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--matching-and-mutation"></a>
##### Matching and mutation

1. After normalizing a valid incoming restaurant, both preview and apply must resolve the current persisted record by ID and the owner of the incoming normalized name.
2. When the ID exists and a different persisted ID owns the incoming normalized name, the importer must classify the candidate as unchanged/skipped and must not mutate or save either persisted record.
3. When the ID exists and no different ID owns the name, the existing merge-and-save behavior must remain unchanged.
4. When the ID does not exist, the existing normalized-name and same-address behavior must remain unchanged.
5. The collision decision must occur before `mergeImportedRestaurant` to prevent an unsaved in-memory mutation from contaminating later logic or tests.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--counts-and-logging"></a>
##### Counts and logging

1. Preview must count an ID/name-owner collision as unchanged, not updated.
2. Apply must count the same collision as `skippedExisting`, not updated or imported.
3. Apply must emit a concise `DEBUG` diagnostic identifying the skipped incoming ID and normalized name without a throwable.
4. The workflow must continue processing subsequent candidates and, when no genuine failure occurs, record the import as completed.
5. Genuine remote, lease, validation, and persistence failures must retain their existing error handling and causal diagnostics.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--compatibility"></a>
##### Compatibility

1. No repository method, public API, MongoDB schema, index, or durable state shape may change.
2. The implementation must stay within the existing restaurant feature ownership boundary.
3. The package README must document ID-based rename collision handling.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--proposed-approach"></a>
#### Proposed Approach

Add a small private predicate in `RestaurantService` that receives the incoming normalized name and the matched restaurant ID, resolves the normalized-name owner through the existing `findRestaurantByNormalizedName` path, and returns true only when another ID owns that name.

Use the predicate in both classification phases:

- `prepareConfiguredMetroImport`: after an ID match, classify a different-name-owner collision as unchanged; otherwise preserve existing create/update/unchanged classification.
- `applyPreparedImport`: after an ID match and before merging, skip a different-name-owner collision, increment `skippedExisting`, log a throwable-free debug message, and continue.

This approach is intentionally narrow. It reuses the existing indexed lookup and duplicate policy, avoids schema or identity changes, and leaves MongoDB's unique constraint as defense in depth rather than normal control flow.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--alternatives-considered"></a>
#### Alternatives Considered

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--recommended-preserve-unique-names-and-skip-the-conflicting-rename"></a>
##### Recommended: preserve unique names and skip the conflicting rename

This matches current product behavior, requires no migration, prevents the recurring error, and lets the remaining import complete. The trade-off is that the older persisted record can retain its prior name until an administrator deliberately reconciles it.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--allow-duplicate-names-by-location"></a>
##### Allow duplicate names by location

Changing uniqueness to a compound name/location identity would represent real-world franchises more naturally, but it would require index migration, revised repository methods, dedupe behavior, API assumptions, and broader production-data validation. The user did not select this scope.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--reconcile-or-delete-one-identity-automatically"></a>
##### Reconcile or delete one identity automatically

Automatically merging or deleting documents could remove stale data, but it risks breaking ratings, favorites, sessions, and stable public restaurant IDs. Import-time destructive reconciliation is outside the approved behavior.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--files-and-modules"></a>
#### Files and Modules

- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--validation-plan"></a>
#### Validation Plan

1. Add a failing service test where an incoming ID matches persisted `China Villa`, the candidate name is `Aama's Kitchen`, and another ID owns normalized name `aama's kitchen` at a different address.
2. Assert preview reports unchanged rather than updated.
3. Assert apply reports one skipped-existing candidate, does not call `save`, and does not mutate either persisted record.
4. Include a following non-conflicting candidate and assert it is still saved, proving the collision does not abort the batch.
5. Run the focused `RestaurantServiceTest` class.
6. Run the full `:website:test` suite and repository checks required by the final diff.
7. Start the application with the production profile on a non-8080 port and an isolated MongoDB database, exercise the import workflow with deterministic collision data, and capture URL, request/input, HTTP status/body, application state, and logs.
8. After merge, deploy the exact merged SHA and verify local/public health, readiness, service state, successful catch-up completion, and absence of the duplicate-key signature during a bounded recurrence window.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--acceptance-criteria"></a>
#### Acceptance Criteria

- The exact ID-based rename collision no longer calls `restaurantRepository.save` for the conflicting record.
- MongoDB emits no duplicate-key exception for the expected collision.
- Preview and apply agree that the candidate is unchanged/skipped.
- Later candidates in the same import are processed.
- The monthly/startup workflow can record successful completion.
- All focused, full, runtime, CI, and production verification gates pass.
- No schema migration or production restaurant mutation is required outside normal non-conflicting import updates.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- Risk: preview and apply drift. Mitigation: use the same private collision predicate and assert both result counts.
- Risk: lookup cost increases for ID matches. Mitigation: use the existing unique indexed `normalizedName` query; the fallback exists only for legacy records missing the indexed field.
- Risk: stale restaurant display data remains. Mitigation: preserve non-destructive import behavior and leave explicit administrative reconciliation for separate scope.
- Risk: an unrelated persistence race still triggers a duplicate key. Mitigation: do not suppress arbitrary persistence failures; retain MongoDB uniqueness and existing error diagnostics.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--open-questions"></a>
#### Open Questions

None. The user selected the recommended unique-name skip behavior on 2026-08-02.

<!-- /migrated-source: docs/specs/2026-08-02-christopherbell-dev-osm-import-rename-collision.md -->

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md"></a>
## 2026-08-02 | specs | christopherbell.dev Restaurant Profiles Void and Search Indexing

Original source: `docs/specs/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `1181b54e8cec0c760959fe2e95883ad7ca21a6dd69b1de3420c41c04a86b47ca`.

<!-- migrated-source: docs/specs/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md -->
<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--christopherbelldev-restaurant-profiles-void-and-search-indexing"></a>
### christopherbell.dev Restaurant Profiles Void and Search Indexing

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--purpose"></a>
#### Purpose

Give every valid public restaurant profile a first-class Void presentation and make its useful restaurant information directly indexable by search engines, while keeping member-specific rating and favorite data private.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--background"></a>
#### Background

The public route `/wfl/restaurants/{restaurantId}` already resolves valid restaurants, emits a canonical URL and social metadata, returns a content-free `404` with `noindex,nofollow` for missing profiles, and is represented in the public sitemap. However, the profile body is currently an empty client-side mount populated by JavaScript. Search crawlers that do not execute the application JavaScript receive only the page shell and limited metadata rather than the address, aggregate rating, contact information, source details, and actions visible to a browser user.

The profile also remains on the light site shell and does not load the scoped What's for Lunch Void stylesheet that now owns the Decision Console. The user approved applying the established Void visual system to restaurant profiles without redesigning the separate Top Rated or Favorites pages.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--user-decisions"></a>
#### User Decisions

1. Every valid public restaurant profile should be indexable, not only selected or highly rated restaurants.
2. Use server-side rendering with progressive enhancement rather than a duplicated crawler-only snapshot or metadata-only optimization.
3. Build one public-only page model from the canonical restaurant detail.
4. Render the complete public profile in Thymeleaf before JavaScript runs.
5. Use JavaScript only to add signed-in personal rating and favorite controls.
6. Extend the approved What's for Lunch Void language to profile pages while preserving their single-restaurant information hierarchy.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--goals"></a>
#### Goals

1. Return meaningful restaurant content in the raw HTML for every valid profile.
2. Provide unique, safe search metadata and structured restaurant data.
3. Preserve canonical URLs, sitemap discovery, and clean `404`/`noindex` behavior.
4. Prevent personal member state and audit data from entering public HTML or structured data.
5. Give restaurant profiles a responsive, accessible Void layout consistent with the WFL Decision Console.
6. Keep the public profile usable if JavaScript is unavailable or the member enhancement request fails.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--non-goals"></a>
#### Non-Goals

- Do not make Favorites public or indexable.
- Do not redesign the Top Rated or Favorites pages.
- Do not expose `myRating`, `myFavorite`, creator identity, modification identity, or audit timestamps in public HTML or JSON-LD.
- Do not create a separate crawler route, hidden keyword content, or duplicated SEO-only profile document.
- Do not change restaurant eligibility, import behavior, rating rules, profile URL shape, database schema, or WFL selection behavior.
- Do not make missing or malformed restaurant IDs indexable.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--public-profile-model"></a>
#### Public Profile Model

Create one immutable public-only page model from the canonical `RestaurantDetail` result. It owns only information appropriate for an anonymous visitor and search crawler:

- restaurant ID;
- name;
- cuisine when present;
- formatted postal address;
- aggregate rating value and count when ratings exist;
- telephone when present;
- safe external website URL when present;
- source/type label when appropriate for public display;
- directions URL;
- canonical URL;
- page title and description; and
- structured-data fields, including coordinates when valid.

The model must not contain member-personalized or audit fields. Keeping those values out of the model is the primary privacy boundary; templates should not receive data they are forbidden to render.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--server-rendering-and-progressive-enhancement"></a>
#### Server Rendering and Progressive Enhancement

The restaurant controller loads the canonical detail once, creates the public page model, and gives Thymeleaf everything required to render the visible profile. The raw response must include the restaurant name, cuisine/location context, address, aggregate rating when available, contact/action details when available, and source information without depending on JavaScript.

JavaScript enhances a dedicated member-controls mount only for an authenticated visitor. It may fetch the existing detail endpoint to add personal rating and favorite controls. Anonymous visitors must not incur an unnecessary profile-detail fetch merely to recreate content already present in HTML.

If member enhancement fails, retain the complete public profile and show a concise inline status in the member-controls area. An API failure must never replace or clear the public content.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--search-indexing-and-structured-data"></a>
#### Search Indexing and Structured Data

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--valid-profiles"></a>
##### Valid Profiles

- Return `200` with meaningful public HTML.
- Emit a unique title and useful description derived from safe restaurant fields.
- Emit one canonical URL using the encoded canonical restaurant ID.
- Do not emit `noindex`.
- Remain discoverable through the public sitemap.
- Be reachable through ordinary profile links from WFL surfaces.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--json-ld"></a>
##### JSON-LD

Emit one valid `application/ld+json` object using `https://schema.org/Restaurant`. Include only fields that exist and pass the application's safety rules:

- `name`;
- `servesCuisine`;
- canonical `url`;
- `PostalAddress` components;
- `GeoCoordinates` when latitude and longitude are valid;
- `telephone` when present;
- the restaurant's safe external website as `sameAs` when present; and
- `AggregateRating` only when the restaurant has one or more ratings and the value/count are valid.

Structured data must be serialized safely rather than assembled through unescaped string concatenation. It must contain the same public facts shown on the page and must never include member state or audit fields.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--missing-or-malformed-profiles"></a>
##### Missing or Malformed Profiles

- Return a content-free `404`.
- Emit `noindex,nofollow`.
- Do not emit restaurant JSON-LD.
- Do not provide a misleading canonical URL for a nonexistent restaurant.

`robots.txt` must continue to permit public restaurant profiles and advertise the sitemap. Favorites remains private and non-indexable; Top Rated and the restaurant sitemap remain public.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--void-profile-design"></a>
#### Void Profile Design

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--ownership-and-scope"></a>
##### Ownership and Scope

Extend `whats-for-lunch.css` so its scoped Void rules own both the chooser and restaurant profiles. The profile page opts into `void-shell-page` and `lunch-void-page` and loads the WFL stylesheet after `main.css`. All new rules remain scoped beneath the WFL Void page class to avoid affecting unrelated pages.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--information-hierarchy"></a>
##### Information Hierarchy

- Use a compact Void hero with a gold `Restaurant signal` label, restaurant name as the single page H1, and cuisine/location context.
- Present the aggregate public rating as a clear signal panel without implying that the profile is selected, sponsored, or objectively ranked.
- Use a structured detail surface for address, contact, source, website, and directions.
- Keep external actions conventional and understandable, with safe-link behavior preserved.
- Reserve a clearly labeled member area for personal rating and favorite controls when signed in.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--visual-language"></a>
##### Visual Language

- Reuse the WFL near-black layered background, subtle grid, teal signal accents, restrained gold highlights, panel borders, and typography hierarchy.
- Use a purpose-built single-restaurant layout rather than copying the chooser's three-card grid.
- Use a balanced two-column detail layout on wider screens and a single stacked column on narrow/mobile screens.
- Preserve sufficient contrast, visible `:focus-visible` states, semantic landmarks/headings, and keyboard operation.
- Do not encode rating or state using color alone.
- Respect `prefers-reduced-motion` for any new transition or animation.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--expected-files-and-modules"></a>
#### Expected Files and Modules

- `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- `website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreviewService.java` or a focused public-profile view-model service beside it
- a focused immutable restaurant public-profile/page model under the WFL view package
- `website/src/main/resources/templates/restaurant.html`
- `website/src/main/resources/static/js/restaurant-profile.js`
- `website/src/main/resources/static/css/whats-for-lunch.css`
- relevant controller, view-model/service, template, JavaScript, stylesheet, sitemap, and robots tests

The implementation plan must confirm exact ownership and literal edit ranges from the refreshed isolated worktree before execution.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--error-and-edge-case-behavior"></a>
#### Error and Edge-Case Behavior

- A valid profile without cuisine, phone, website, source metadata, coordinates, or ratings still renders a useful indexable page; absent optional fields are omitted cleanly.
- An unrated restaurant must not emit a fabricated aggregate rating.
- Invalid external website schemes remain non-clickable and must not enter JSON-LD.
- Missing address components are formatted without placeholder punctuation or invented locations.
- Member endpoint `401` or anonymous state does not create an error banner and does not fetch when authentication status is already known server-side.
- Other member enhancement failures produce a local inline status while preserving public content.
- The public page must remain understandable and navigable with scripts disabled.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--server-search-and-template-tests"></a>
##### Server, Search, and Template Tests

1. Verify a valid profile response contains its public name, address, rating/contact data when present, canonical URL, and no `noindex` before JavaScript executes.
2. Verify unique safe title and description generation for complete and sparse records.
3. Verify JSON-LD parses as JSON, uses `Restaurant`, and conditionally includes address, coordinates, telephone, external website, cuisine, and aggregate rating.
4. Verify hostile or malformed restaurant fields cannot break HTML, metadata, or JSON-LD contexts.
5. Verify member state and audit fields never appear in public HTML or JSON-LD.
6. Verify missing and malformed IDs return content-free `404` responses with `noindex,nofollow` and no restaurant structured data.
7. Verify encoded canonical URLs, restaurant sitemap membership, and public `robots.txt` sitemap/disallow behavior.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--javascript-and-css-tests"></a>
##### JavaScript and CSS Tests

1. Verify anonymous pages keep server-rendered content and perform no redundant detail fetch.
2. Verify authenticated enhancement adds personal rating and favorite behavior without duplicating public fields.
3. Verify enhancement failure retains public content and shows only the inline member-area status.
4. Verify the template opts into the Void shell and the WFL stylesheet.
5. Verify CSS covers hero, rating signal, detail grid, actions, member controls, focus, error, responsive, and reduced-motion states while remaining page-scoped.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--full-and-runtime-verification"></a>
##### Full and Runtime Verification

1. Run focused Java/service/controller/template/JavaScript/static tests, then the full `:website:test` and `:website:check` gates with a task-private Gradle home.
2. Package the candidate and run it on a non-8080 port with an isolated MongoDB database.
3. Inspect raw HTTP for a complete valid profile, sparse/unrated profile, encoded-ID profile, missing profile, `robots.txt`, and sitemap.
4. Validate JSON-LD with a parser and verify no personal/audit fields are present.
5. Exercise anonymous and authenticated profiles in the browser at desktop and mobile widths, including keyboard focus, website/directions, personal rating, favorite, scripts-disabled content, and member API failure fallback.
6. Confirm the production listener on port 8080 remains untouched during candidate validation.
7. Publish a PR, pass required CI, merge, deploy the exact SHA through the protected Windows workflow, and verify production identity, readiness, liveness, MongoDB health, raw indexable HTML, sitemap/robots behavior, and authenticated desktop/mobile profile presentation.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--acceptance-criteria"></a>
#### Acceptance Criteria

- Every valid restaurant profile returns its meaningful public content in raw HTML.
- Valid profiles have unique safe metadata, one canonical URL, valid conditional Restaurant JSON-LD, sitemap discovery, and no `noindex` directive.
- Missing/malformed profiles remain content-free `404` responses with `noindex,nofollow` and no restaurant structured data.
- Public output contains no personal rating/favorite state or audit fields.
- Anonymous visitors do not need a detail API fetch to see the profile.
- Authenticated personal controls enhance the server-rendered profile without replacing it, and failures degrade locally.
- The page matches the approved scoped Void profile direction on desktop and mobile while meeting keyboard, contrast, semantic, and reduced-motion requirements.
- Focused, full, alternate-port runtime, PR CI, deployment, and production checks pass.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- **Private data leakage:** reusing the API detail object in the template could expose member state. Mitigation: use an immutable public-only model that cannot carry those fields.
- **HTML/JSON-LD injection:** dynamic fields cross multiple output contexts. Mitigation: use Thymeleaf escaping and a trusted JSON serializer with hostile-input regression tests.
- **Duplicate data drift:** client and server rendering could disagree. Mitigation: server rendering owns all public fields; JavaScript owns only member-specific controls.
- **Crawler ambiguity:** partial success or missing records could be indexed incorrectly. Mitigation: retain explicit `404` plus `noindex,nofollow` behavior and test raw responses.
- **Broad CSS regressions:** shared styles could affect other pages. Mitigation: scope every addition beneath the WFL Void profile classes and leave Top Rated/Favorites unchanged.
- **Visual regressions for sparse records:** optional fields could create empty panels. Mitigation: conditionally render fields and verify complete, sparse, and unrated fixtures at desktop/mobile widths.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--rollback-and-recovery"></a>
#### Rollback and Recovery

- Code rollback: redeploy the previous known-good merged SHA.
- The feature requires no database migration or data rewrite.
- Existing profile URLs, sitemap entries, restaurant data, ratings, and favorites remain compatible with both versions.
- Reverting the controller/template/model/asset changes restores the previous client-rendered profile without data recovery.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--open-questions"></a>
#### Open Questions

None. The user approved indexing all valid profiles, server rendering with progressive enhancement, the public-only data boundary, structured-data requirements, missing-profile behavior, and the scoped Void profile direction.

<!-- /migrated-source: docs/specs/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md -->

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md"></a>
## 2026-08-02 | specs | christopherbell.dev What's for Lunch Import Location Integrity

Original source: `docs/specs/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `a320a538047f8c0b76c7f5eff311d55506ec50f294932da0a63fce58ea0b4a0c`.

<!-- migrated-source: docs/specs/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md -->
<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--christopherbelldev-whats-for-lunch-import-location-integrity"></a>
### christopherbell.dev What's for Lunch Import Location Integrity

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--document-status"></a>
#### Document Status

ready-for-review

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--purpose"></a>
#### Purpose

Ensure every OpenStreetMap restaurant included in What's for Lunch has a genuine, supported city and state. Remove the fabricated `Imported Metro, TX` fallback, reject unresolved locations, and safely remove the existing placeholder population from production.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--background"></a>
#### Background

Current `origin/main` maps OpenStreetMap elements in `OpenStreetMapRestaurantClient`. When an element lacks `addr:city`, the client stores `Imported Metro`; when it lacks `addr:state`, it stores `TX`; and when it lacks `addr:country`, it stores `US`.

That behavior is factually wrong. The configured import covers Austin, the San Francisco Bay Area, New Orleans, and Dallas. It can therefore label California and Louisiana restaurants as Texas locations, and it exposes a synthetic city that does not exist. The public nearby query selects coordinate-bearing records without requiring a supported city, so placeholder records can appear to users.

The user chose strict correctness over retention: use genuine location evidence when it is available, otherwise do not import the restaurant. The user also approved removal of the already-persisted `Imported Metro` OpenStreetMap records after a production backup and an exact impact report.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--goals"></a>
#### Goals

- Never create or update a restaurant with the synthetic city `Imported Metro`.
- Resolve a genuine locality from supported OpenStreetMap address tags without adding a new external service.
- Include only restaurants whose resolved locality belongs to the configured city/state coverage.
- Require valid coordinates for imported restaurants.
- Reject conflicting country or state evidence instead of silently rewriting it.
- Keep import preview and apply classifications consistent.
- Remove existing placeholder OpenStreetMap records and their direct favorite/rating references from production safely.
- Prove that the cleanup population is not recreated by a subsequent import.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--non-goals"></a>
#### Non-Goals

- Do not introduce per-record reverse geocoding or a dependency on Nominatim or another geocoder.
- Do not guess a city from a metro bounding box, ZIP code, street, or nearest configured city.
- Do not expand the configured metro or city coverage.
- Do not require a street address when the genuine locality, state ownership, country, and coordinates are valid.
- Do not delete valid manually managed restaurants.
- Do not rewrite historical lunch-session documents; unavailable restaurant IDs already degrade to the remaining resolvable restaurants.
- Do not weaken import timeouts, response-size bounds, lease behavior, unique-name constraints, or error reporting.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--genuine-locality-resolution"></a>
##### Genuine locality resolution

1. Resolve locality from the first nonblank OpenStreetMap tag in this order: `addr:city`, `addr:town`, `addr:village`, `addr:municipality`.
2. Normalize the resolved locality only for comparison; preserve the canonical spelling from the matching configured city in stored data.
3. Match the locality against the unique configured `Metro.cities` ownership map.
4. If no supported configured city matches, omit the OpenStreetMap element from the client result.
5. Do not use `addr:place` as a locality because it can represent the address thoroughfare/place component rather than a municipality.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--state-and-country-integrity"></a>
##### State and country integrity

1. Store the state owned by the matched configured city.
2. A blank OpenStreetMap `addr:state` is acceptable because configured city ownership supplies the state deterministically.
3. When `addr:state` is present, accept it only when its normalized value equals the configured state abbreviation; otherwise omit the element.
4. A blank OpenStreetMap `addr:country` is acceptable because every configured metro is United States coverage.
5. When `addr:country` is present, accept case-insensitive `US`, `USA`, or `United States`; otherwise omit the element.
6. Remove the `Imported Metro`, `TX`, and generic default-text address fallbacks from the client.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--coordinate-and-import-classification"></a>
##### Coordinate and import classification

1. Require finite latitude in `[-90, 90]` and longitude in `[-180, 180]` before returning an imported restaurant.
2. Continue allowing a missing street or postal code when locality, state ownership, country, and coordinates are valid.
3. Elements omitted by the client are not fetched import candidates and therefore cannot be previewed, inserted, or used to update existing records.
4. Service-level import validation must independently reject any malformed imported restaurant that bypasses or does not originate from the OpenStreetMap client, including missing/unsupported city-state coverage or invalid coordinates.
5. Preview and apply must use the same service-level validity rule and count rejected candidates as `skippedInvalid` when they are present in a prepared snapshot.
6. Existing valid import matching, unique-name collision handling, counts, and continuation behavior remain unchanged.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--existing-production-cleanup"></a>
##### Existing production cleanup

1. Before mutation, capture a fresh production backup using the protected native-Windows operations workflow.
2. Query and report the exact count and representative samples for records meeting both conditions:
   - `_id` starts with `osm:`.
   - `address.city` equals `Imported Metro` exactly.
3. Record direct reference counts in `whatsforlunch_favorites` and `whatsforlunch_ratings` for the affected restaurant IDs.
4. Delete only the matched restaurant documents and their direct favorite/rating documents. Preserve all other restaurant and member data.
5. Preserve historical `whatsforlunch_sessions`; existing session rendering may omit deleted restaurants while retaining the session record and remaining choices.
6. Run cleanup only after the strict importer is deployed so the placeholder population cannot be recreated.
7. Record pre-cleanup counts, deleted counts, post-cleanup zero-count queries, backup evidence, and rollback instructions in the final test/closure evidence.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--observability-and-documentation"></a>
##### Observability and documentation

1. Tests and import results must make unresolved-location rejection visible through counts, not fabricated output.
2. Genuine remote, parsing, persistence, lease, and workflow failures must retain causal diagnostics.
3. Update the restaurant package README to document supported locality tags, configured city ownership, coordinate requirements, and strict exclusion.
4. No public API response shape or MongoDB restaurant schema changes are required.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--proposed-approach"></a>
#### Proposed Approach

Build a normalized, immutable city-coverage lookup from `WflProperties.Osm.metros` inside `OpenStreetMapRestaurantClient`. Each entry maps one configured locality to its canonical city spelling and configured state. Resolve an element's first genuine locality tag, look it up, validate optional state/country evidence, validate coordinates, and only then build the `Restaurant`.

Add a matching service-level predicate in `RestaurantService` so deterministic tests, future clients, or prepared imports cannot bypass the invariant. Keep client omission and service `skippedInvalid` classification separate: the client avoids manufacturing an invalid candidate, while the service remains the defense-in-depth persistence boundary.

Use a narrowly scoped, reviewable production cleanup operation after deployment. It will select exact OSM placeholder IDs, capture counts and samples, remove only those catalog documents and direct favorite/rating references, and verify zero remaining exact matches. The production backup is the rollback boundary.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--alternatives-considered"></a>
#### Alternatives Considered

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--recommended-strict-source-validation-plus-targeted-cleanup"></a>
##### Recommended: strict source validation plus targeted cleanup

This removes fabricated data, uses only existing OSM and configured coverage evidence, adds no rate-limited dependency, and prevents recurrence. It intentionally drops incomplete or unsupported records.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--reverse-geocode-incomplete-records"></a>
##### Reverse-geocode incomplete records

Coordinate-based geocoding could retain more restaurants, but up to 20,000 monthly candidates would add latency, rate-limit pressure, caching and attribution requirements, a new failure mode, and a second remote trust boundary. This is unnecessary for the approved correctness rule.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--hide-placeholder-records-at-read-time"></a>
##### Hide placeholder records at read time

Filtering nearby results would reduce immediate exposure, but corrupt records would remain in inventory, profiles, favorites, and future code paths. It treats a persistence defect as a presentation concern and does not meet the cleanup requirement.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--files-and-modules-involved"></a>
#### Files and Modules Involved

- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`
- Existing native-Windows production backup/deployment tooling under `ops/production/windows/`
- Builder work, plan, test report, spoke update/review, session memory, and closure artifacts

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--validation-plan"></a>
#### Validation Plan

1. Add a failing client regression proving missing locality no longer becomes `Imported Metro, TX`.
2. Add client tests for each supported locality tag, canonical configured spelling/state, unsupported locality, conflicting state, conflicting country, and invalid/missing coordinates.
3. Add a failing service regression proving an invalid prepared candidate increments `skippedInvalid` and is not saved.
4. Run the focused client and service test classes, full `:website:test`, and `:website:check` with a private Gradle home.
5. Start the packaged application with production-like configuration on a non-8080 port, isolated MongoDB database, and deterministic loopback Overpass response containing valid and invalid examples.
6. Exercise the import status/preview/apply path and a public nearby request; capture URL, port, request data, HTTP status/body, persistence counts, and logs.
7. Obtain independent code review, publish a pull request, wait for every required CI and CodeQL gate, and merge only after success.
8. Deploy the exact merged SHA through protected production operations and verify readiness, liveness, public routes, service state, MongoDB health, and application commit identity.
9. Take the production backup; capture exact placeholder and reference counts; execute the scoped cleanup; verify zero placeholder records and no unexpected count deltas.
10. Run or observe a bounded import after cleanup and prove no `Imported Metro` record is recreated and no placeholder appears in nearby results.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--acceptance-criteria"></a>
#### Acceptance Criteria

- No application code contains an `Imported Metro` or default `TX` import fallback.
- Valid OSM records are stored with a canonical configured city and its actual configured state.
- Missing, unsupported, or contradictory location evidence is excluded rather than guessed.
- Invalid prepared candidates are counted as skipped-invalid and never persisted.
- Existing valid import behavior and API shapes remain compatible.
- Production is backed up before cleanup.
- The exact production OSM placeholder population and direct favorite/rating references are removed with recorded before/after counts.
- Historical sessions and unrelated data remain intact.
- A post-cleanup import does not recreate placeholder records.
- Focused, full, alternate-port runtime, independent review, CI, deployment, and production verification gates pass.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- Risk: strict locality matching reduces catalog size. Mitigation: this is the user-approved correctness trade-off; alternate genuine OSM locality tags retain valid records without guessing.
- Risk: OSM supplies full state names instead of abbreviations. Mitigation: such candidates are conservatively excluded; a future separately designed normalizer may expand accepted verified forms.
- Risk: cleanup removes records referenced by users. Mitigation: count references first, delete direct favorite/rating rows with the same IDs, preserve historical sessions, and retain a pre-mutation backup.
- Risk: client and service validity rules drift. Mitigation: characterize both boundaries with shared acceptance cases and document the invariant in the package README.
- Risk: a partial or failed import is mistaken for successful cleanup validation. Mitigation: require durable successful import status plus database and HTTP evidence before closure.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--rollback"></a>
#### Rollback

- Code rollback: redeploy the previously verified production release if the strict importer causes a runtime regression.
- Data rollback: restore the pre-cleanup MongoDB backup if exact count reconciliation or dependent-data verification fails.
- Do not re-enable synthetic fallback values during rollback; pause imports instead if the previous release would recreate placeholders.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--open-questions"></a>
#### Open Questions

None. The user approved strict genuine-location validation and existing placeholder cleanup on 2026-08-02.

<!-- /migrated-source: docs/specs/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md -->

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md"></a>
## 2026-08-02 | specs | christopherbell.dev What's for Lunch Legacy Location Reconciliation

Original source: `docs/specs/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `5c07f88788d7591b81ca0bb864b9abd043f027599e0ec463d94aec4752f02ade`.

<!-- migrated-source: docs/specs/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md -->
<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--christopherbelldev-whats-for-lunch-legacy-location-reconciliation"></a>
### christopherbell.dev What's for Lunch Legacy Location Reconciliation

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--purpose"></a>
#### Purpose

Finish the What's for Lunch location-integrity repair by retaining restaurants whose real locality can be proven, expanding configured OpenStreetMap coverage to the official places intersecting each configured import rectangle, correcting noncanonical legacy locations, and deleting only records that still have no authoritative place at their coordinates.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--background"></a>
#### Background

PR `#1342` removed the fabricated `Imported Metro, TX` fallback, added strict configured-locality validation, passed CI, merged as `178d90caca58d2f6284f54ab2ef4514d10df2918`, and was deployed. A backup-gated cleanup removed 6,825 exact `Imported Metro` rows, and the first strict production import completed successfully without recreating that exact placeholder.

Post-deployment inspection found a broader legacy population. A fresh read-only audit at 2026-08-02 16:47 America/Chicago classified all 7,268 OSM catalog rows against the current configuration and official U.S. Census Bureau geography:

- 5,493 rows already have a supported canonical city, state, country, and coordinates.
- 1,596 rows name a current 2025 Census incorporated place or Census-designated place inside a configured import rectangle, but are outside the current short city lists or contain a noncanonical state.
- 179 rows use a synthetic, misspelled, postal-community, airport, or otherwise unrecognized locality label.
- Point-in-polygon queries against the Census TIGERweb January 1, 2025 incorporated-place and Census-designated-place layers resolve 163 of those 179 rows to a real place.
- 16 rows have no Census place at their coordinates and remain unresolved.

The user explicitly selected **Expand and reconcile**: verify and add genuine nearby cities, correct reimported locations, and delete only synthetic or unresolved rows.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--authoritative-geography-boundary"></a>
#### Authoritative Geography Boundary

The reconciliation uses only current primary U.S. Census Bureau sources:

- 2025 Gazetteer place files for California, Louisiana, and Texas for canonical place names and identifiers.
- TIGERweb `Places_CouSub_ConCity_SubMCD` incorporated-place layer 4 and Census-designated-place layer 5, January 1, 2025 vintage, for rectangle intersection and point-in-polygon resolution.

The configured rectangles intersect 393 unique official places:

- Austin, TX: 70
- San Francisco Bay Area, CA: 154
- New Orleans, LA: 46
- Dallas, TX: 123

The source query returns two distinct California places named `Mountain View`; configuration stores the canonical name once because both resolve to the same city/state value. `Fairview`, `Rollingwood`, and `Sunnyvale` occur in more than one configured state, so locality resolution must use the restaurant coordinates and any supplied state rather than a global city-name overwrite.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--goals"></a>
#### Goals

1. Treat every official incorporated place or Census-designated place intersecting a configured import rectangle as supported coverage for that metro.
2. Canonicalize city, two-letter state, and `US` country while accepting equivalent full state names from OSM.
3. Disambiguate same-name places using configured rectangle ownership and coordinates.
4. Reject a city tag whose coordinates fall outside the owning metro rectangle, even when the city name is configured.
5. Make the service persistence boundary independently enforce city, state, country, coordinate validity, and metro rectangle ownership.
6. Reimport after deployment so current OSM evidence corrects legacy rows where possible.
7. Use a reviewed, checksum-pinned Census resolution manifest to update remaining legacy OSM locations and delete only rows with no authoritative Census place.
8. Preserve dependent user/session data unless its exact restaurant record is deleted under the approved cleanup contract.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--non-goals"></a>
#### Non-Goals

- Do not infer a city from a metro label, ZIP code, county, neighborhood, airport label, or nearest-place heuristic.
- Do not call Census or another geocoder from the normal application import path.
- Do not admit arbitrary OSM locality text merely because its coordinates are within a metro rectangle.
- Do not change public API response shapes, MongoDB document schemas, import scheduling, or the four configured rectangles.
- Do not delete any row that a fresh authoritative point-in-polygon lookup resolves to a supported place.
- Do not weaken production filesystem ACLs or bypass the protected Windows deployment workflow.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--functional-requirements"></a>
#### Functional Requirements

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--coverage-configuration"></a>
##### Coverage Configuration

1. `application.yml` and `WflProperties` defaults must contain the same 393 unique canonical place names grouped under the existing four metro rectangles.
2. Place names must come from the pinned Census coverage result, not from the observed MongoDB values alone.
3. Duplicate city names across states must remain valid configuration.
4. Duplicate city/state ownership across metros must remain invalid.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--client-resolution"></a>
##### Client Resolution

1. Read locality in the established order: `addr:city`, `addr:town`, `addr:village`, `addr:municipality`.
2. Validate coordinates before locality resolution.
3. Resolve locality candidates by normalized city name, then require coordinate containment in the candidate metro rectangle.
4. If OSM supplies a state, accept either the configured postal abbreviation or its full official name, and reject contradictions.
5. If OSM supplies a country, accept established United States aliases and reject contradictions.
6. Emit exactly one canonical city/state/`US` result; reject no-match or ambiguous-match candidates.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--service-defense-in-depth"></a>
##### Service Defense in Depth

1. A prepared import candidate is valid only when its canonical city and state belong to one configured metro and its coordinates fall inside that metro's rectangle.
2. Missing/invalid coordinates, unsupported city/state, wrong country, or out-of-rectangle coordinates increment `skippedInvalid` and are never persisted.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--production-reconciliation"></a>
##### Production Reconciliation

1. Take a new full production MongoDB backup immediately before reconciliation and prove a dry-run restore can read it.
2. Capture a fresh inventory and generate a deterministic manifest containing each target OSM ID, old location, Census source layer/GEOID when resolved, proposed canonical location, and action (`update` or `delete`).
3. Requery Census for every noncanonical target before mutation; abort if counts, source responses, or manifest checksum differ unexpectedly.
4. Deploy the expanded importer and complete a production preview/apply import before the direct reconciliation.
5. Update only exact manifest IDs with a resolved Census place; set canonical city/state/country and matching search fields without changing restaurant coordinates.
6. Delete only exact manifest IDs with no incorporated-place or Census-designated-place match. Delete their direct favorite and rating rows under the established cleanup contract; preserve historical session references.
7. Verify every remaining OSM row satisfies the deployed invariant and that no synthetic metro label remains.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--proposed-approach"></a>
#### Proposed Approach

Represent supported client locations as a normalized city-to-candidate-list map. Each candidate owns canonical city/state plus its configured bounding box. Resolution filters by valid coordinates, optional state evidence, and rectangle containment. This removes the current last-write-wins behavior for same-name cities in different states.

Generate the four coverage lists once from pinned Census TIGERweb results and check them into both configuration surfaces. The application remains self-contained and does not depend on Census availability at runtime.

After the merged SHA is deployed, run a normal import so expanded current OSM tags update as many legacy documents as possible. Then rebuild the Census reconciliation manifest from the remaining noncanonical rows, take a fresh backup, perform exact-ID updates/deletes, and verify counts and public behavior.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--files-and-modules"></a>
#### Files and Modules

- `website/src/main/resources/application.yml`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/config/WflProperties.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClient.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/OpenStreetMapRestaurantClientTest.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/WflPropertiesTest.java`
- `website/README.md`
- production-only ignored reconciliation evidence under the isolated worktree `build/` directory and `A:\Backups\christopherbell.dev`

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--validation-plan"></a>
#### Validation Plan

1. Add failing client tests for newly covered places, full state names, duplicate city names across states, and out-of-rectangle city tags.
2. Add failing service tests for valid expanded coverage and out-of-rectangle prepared candidates.
3. Verify default and YAML coverage counts and exact city sets agree.
4. Run focused WFL tests, then `:website:test` and `:website:check` with a private Gradle user home.
5. Start the packaged app on a non-8080 port and isolated database with a deterministic Overpass fixture containing cross-state duplicate names, a new official place, a full state name, and invalid examples.
6. Save the local runtime test report, publish a PR, pass all required CI, merge, and deploy the exact SHA.
7. Verify production commit identity, readiness, liveness, public routes, Mongo health, and a bounded production preview/apply import.
8. Back up, generate/checksum/review the exact reconciliation manifest, apply it, and prove zero remaining invariant violations.
9. Exercise public nearby results in all four metros and confirm canonical locations.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--acceptance-criteria"></a>
#### Acceptance Criteria

- The checked-in coverage contains exactly the 393 unique official places intersecting the four existing rectangles.
- Same-name cities in different states resolve correctly from their coordinates and do not overwrite one another.
- Full state names canonicalize to configured abbreviations; contradictory states remain rejected.
- Client and service both reject city/coordinate ownership mismatches.
- Automated, alternate-port runtime, CI, merge, and exact-SHA production evidence pass.
- A fresh full backup and restore dry run precede production reconciliation.
- Every retained OSM row has canonical city/state/`US`, valid coordinates, and coordinates inside the owning metro rectangle.
- Only fresh-manifest rows with no authoritative Census place are deleted.
- No `Imported Metro`, `Austin Metro`, wrong-state fallback, or other unresolved locality appears in the catalog or nearby results.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- **Coverage drift:** Census geography changes annually. Pin the 2025 source evidence and record hashes; refresh deliberately in future work.
- **Same-name collision:** A global city map can silently choose the wrong state. Resolve a candidate list with coordinate ownership and test `Sunnyvale`, `Fairview`, and `Rollingwood`.
- **Rectangle edge behavior:** Official place polygons may cross a rectangle edge. Include places whose polygons intersect the fetch rectangle and require restaurant coordinates themselves to be inside the rectangle.
- **Irreversible cleanup:** Back up immediately before mutation, pin exact IDs and checksums, abort on drift, and retain restore instructions.
- **Reimport changes counts:** Treat the post-import inventory as the only valid input to the final manifest; do not reuse the discovery snapshot for mutation.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--rollback-and-recovery"></a>
#### Rollback and Recovery

- Code rollback: redeploy the prior known-good merged SHA if runtime verification fails.
- Data rollback: restore the new pre-reconciliation MongoDB backup if any exact-ID count or invariant check fails.
- Partial-operation recovery: make manifest operations idempotent and record matched/modified/deleted counts for each collection.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md--open-questions"></a>
#### Open Questions

None. The user approved expanded authoritative coverage and exact reconciliation.

<!-- /migrated-source: docs/specs/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md -->

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md"></a>
## 2026-08-02 | specs | christopherbell.dev What's for Lunch Rating-Weighted Void Upgrade

Original source: `docs/specs/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `1a47e2b8b424a422403b30b13d5d64471cb673aadd7b7b2b319657c526d1af11`.

<!-- migrated-source: docs/specs/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md -->
<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--christopherbelldev-whats-for-lunch-rating-weighted-void-upgrade"></a>
### christopherbell.dev What's for Lunch Rating-Weighted Void Upgrade

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--document-status"></a>
#### Document Status

ready-for-execution

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--purpose"></a>
#### Purpose

Make the three-restaurant What's for Lunch selection rating-aware without turning it into a deterministic leaderboard, and upgrade the WFL page to the approved Void Decision Console visual language while retaining every existing user capability.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--background"></a>
#### Background

Current `azurras/christopherbell.dev` `origin/main` selects restaurants by copying the eligible candidate list, calling `Collections.shuffle`, and taking the first three. The same unweighted order helper serves:

- persisted daily lunch picks;
- on-demand browser-location and ZIP-code picks; and
- a replacement when an administrator deletes a restaurant in today's picks.

The application already stores one whole-number 1–5 rating per account and restaurant, exposes public rating counts and sums, and owns a MongoDB aggregate query repository for rating summaries. Ratings currently appear in the UI but do not affect selection probability.

The WFL page currently uses the light `site-page` shell, a photo-backed hero, Bootstrap-oriented control surfaces, and dedicated lunch styles. The site already has a mature Void shell with near-black layered backgrounds, teal signal accents, restrained gold highlights, accessible focus states, and responsive card layouts. During visual brainstorming, the user selected the **Decision Console** direction rather than a light reskin or a dense terminal layout.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--user-decisions"></a>
#### User Decisions

1. Apply weighting to every three-pick flow.
2. Treat unrated restaurants as neutral so new restaurants remain discoverable.
3. Adjust sparse rating evidence toward neutral; a single vote must not receive full influence.
4. Use moderate rather than mild or strong probability differences.
5. Use confidence-adjusted weighted sampling without replacement.
6. Upgrade the WFL page to the Void Decision Console treatment while preserving its existing functions.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--goals"></a>
#### Goals

1. Make higher-rated eligible restaurants appear more often over repeated draws than neutral or lower-rated restaurants.
2. Make lower-rated eligible restaurants appear less often than neutral restaurants without setting their probability to zero.
3. Return at most three unique restaurants and preserve the current eligibility boundary.
4. Apply one selection policy consistently to daily, nearby/ZIP, and replacement draws.
5. Prevent a single rating from dominating a restaurant's odds.
6. Keep rating aggregation bounded to one query per candidate draw rather than one query per restaurant.
7. Give WFL a first-class Void identity with a compact decision console and three equal result cards.
8. Preserve accessibility, responsiveness, session stability, and all existing restaurant actions.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--non-goals"></a>
#### Non-Goals

- Do not sort picks as a leaderboard or guarantee that the highest-rated restaurant appears.
- Do not permanently exclude low-rated or unrated restaurants.
- Do not use the current viewer's personal rating as a separate selection signal.
- Do not add paid placement, cuisine popularity, distance weighting, favorites weighting, or time-decay behavior.
- Do not change restaurant eligibility, supported metro rectangles, radius handling, cuisine filters, import behavior, rating validation, public API shapes, or database schemas.
- Do not recalculate already-persisted daily picks or active shared-session picks merely because a rating changes or a deployment occurs.
- Do not make the three displayed positions imply a quality ranking.
- Do not convert WFL into a dense administrative terminal or remove conventional labels needed for usability.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--rating-weighted-selection-requirements"></a>
#### Rating-Weighted Selection Requirements

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--candidate-eligibility"></a>
##### Candidate Eligibility

The existing service remains the sole owner of eligibility. Rating weighting runs only after the current rules have selected candidates:

- supported city/state for daily picks;
- valid restaurant ID;
- valid coordinates for nearby/ZIP picks;
- distance within the selected radius;
- matching explicit or saved cuisine filters; and
- exclusion of already-selected IDs during a replacement draw.

Ratings change probability only. They cannot make an otherwise ineligible restaurant eligible.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--confidence-adjusted-rating"></a>
##### Confidence-Adjusted Rating

For each candidate, calculate an adjusted rating from aggregate rating sum and count:

```text
adjustedRating = (ratingSum + 3.0 * 3) / (ratingCount + 3)
```

The prior represents three neutral virtual ratings at 3 stars.

- An unrated restaurant has `adjustedRating = 3.0`.
- One 5-star rating produces `3.5`, not `5.0`.
- One 1-star rating produces `2.5`, not `1.0`.
- Repeated consistent ratings gradually approach their observed average.

Rating count and sum must be non-negative and the calculated score must be clamped to `[1.0, 5.0]` as defense in depth. Normal application writes continue to enforce integer ratings from 1 through 5.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--moderate-weight-curve"></a>
##### Moderate Weight Curve

Map adjusted ratings through these probability-weight anchors, linearly interpolating fractional scores:

| Adjusted rating | Selection weight |
| ---: | ---: |
| 1.0 | 0.35 |
| 2.0 | 0.60 |
| 3.0 | 1.00 |
| 4.0 | 1.50 |
| 5.0 | 2.00 |

Every weight remains positive. With sufficient evidence, a 5-star restaurant approaches twice the selection chance of an unrated/neutral restaurant, while a 1-star restaurant approaches 35% of neutral. Sparse evidence remains materially closer to neutral.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--unique-weighted-draw"></a>
##### Unique Weighted Draw

Select without replacement:

1. Sum the positive weights of the remaining candidates.
2. Draw one random value inside that total.
3. Select the candidate whose cumulative interval owns the value.
4. Remove the selected candidate.
5. Repeat until the requested count is reached or no candidates remain.

The selector must return no duplicate restaurant IDs, preserve the requested maximum, handle fewer candidates than requested, and expose deterministic randomness at a test boundary. Its production entry point uses `ThreadLocalRandom.current().nextDouble()`, while a package-private overload accepts a `DoubleSupplier` for deterministic tests. Tests must not rely on wall-clock or nondeterministic statistical outcomes.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--rating-summary-query"></a>
##### Rating Summary Query

Extend the aggregate rating query repository with a method that accepts the eligible candidate IDs and returns one `RestaurantRatingSummary` per rated restaurant. The query must:

- match only the supplied candidate IDs;
- group by restaurant ID;
- return rating count and sum;
- return no synthetic record for unrated restaurants; and
- perform one aggregate query for the draw.

The service maps absent summaries to the neutral prior. A rating query failure remains a visible service failure rather than silently changing product behavior back to uniform randomness.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--selection-lifecycle"></a>
##### Selection Lifecycle

- **Nearby/browser location:** every request uses current aggregate ratings.
- **ZIP:** every request uses current aggregate ratings after resolving the ZIP origin.
- **Daily:** the next daily generation uses ratings current at generation time; the persisted list stays stable for that date.
- **Deleted-pick replacement:** only the replacement slot is drawn from the remaining eligible candidates using current ratings; surviving picks retain their order and identity.
- **Shared session:** existing session picks remain stable. Host-triggered fresh picks use the normal weighted nearby/ZIP path.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--component-design"></a>
#### Component Design

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--ratingweightedrestaurantselector"></a>
##### `RatingWeightedRestaurantSelector`

A new small, stateless selection-policy component owns:

- neutral-prior adjustment;
- score clamping;
- piecewise-linear weight interpolation;
- weighted sampling without replacement; and
- random-boundary validation.

It receives already-eligible `Restaurant` candidates and rating summaries. It does not query MongoDB, inspect authentication, calculate distance, interpret filters, or persist picks.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--restaurantratingqueryrepository"></a>
##### `RestaurantRatingQueryRepository`

The existing aggregation boundary gains a candidate-summary method. It remains responsible only for MongoDB aggregation and result mapping.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--restaurantservice"></a>
##### `RestaurantService`

The service gains one orchestration helper that:

1. accepts eligible candidates and a requested count;
2. loads rating summaries once;
3. indexes summaries by restaurant ID; and
4. delegates to the selector.

The helper replaces the uniform shuffle in daily generation, nearby/ZIP selection, and deleted-pick replacement. Unrelated rating display, top-rated listing, import, filtering, session, and CRUD behavior stays unchanged.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--void-decision-console-requirements"></a>
#### Void Decision Console Requirements

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--page-shell"></a>
##### Page Shell

- Add the established `void-shell-page` class and a WFL-specific Void page class.
- Replace the photo-backed lunch hero and white content panel with a near-black layered background, subtle grid, teal signal lines, and restrained gold accents drawn from existing Void tokens.
- Keep the global navigation and footer behavior intact.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--information-hierarchy"></a>
##### Information Hierarchy

- Use a compact WFL hero with the existing page title, a Decision Console eyebrow, and a concise lunch-decision description.
- Render secondary WFL navigation and freshness information as quiet Void utility surfaces.
- Style the toolbar plus active Filters, Location, or Lunch with Friends panel as one coherent decision-control deck.
- Make the refresh action visually primary while preserving its current accessible label and disabled semantics.
- Add a short note: ratings influence the draw, but every eligible restaurant remains possible.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--pick-cards"></a>
##### Pick Cards

- Display the three selections as equal-width cards on desktop and a single column on narrower screens.
- Retain `01`, `02`, and `03` as neutral identifiers only.
- Do not add labels such as “best,” “strong signal,” or ranking scores.
- Preserve restaurant name, cuisine, address, public/personal rating display, favorites, voting, directions, website, phone, and administrator deletion.
- Preserve safe external-link behavior and existing profile links.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--states-and-accessibility"></a>
##### States and Accessibility

- Style loading, location prompt, empty, error, active session, archived session, form, success, and disabled states in the same Void language.
- Preserve semantic headings, landmarks, form labels, live regions, button states, and keyboard operation.
- Provide visible `:focus-visible` treatment with sufficient contrast.
- Do not encode rating or state using color alone.
- Retain mobile behavior and make the card/control layouts usable at the current responsive breakpoints.
- Respect `prefers-reduced-motion` for any newly added transitions or animations.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--expected-files-and-modules"></a>
#### Expected Files and Modules

- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/rating/RestaurantRatingQueryRepository.java`
- new focused selector under `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/selection/`
- selector and repository/service tests under the matching `website/src/test/java` packages
- `website/src/main/resources/templates/whatsforlunch.html`
- `website/src/main/resources/static/js/whats-for-lunch.js` for the approved probability disclosure and Decision Console semantic class hooks
- `website/src/main/resources/static/css/main.css`
- relevant WFL and frontend documentation/tests

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--failure-and-edge-case-behavior"></a>
#### Failure and Edge-Case Behavior

- Null/empty candidate input returns an empty selection without a rating query.
- Fewer than three candidates returns every eligible candidate exactly once.
- Duplicate candidate IDs are rejected explicitly before weighting; the final selection cannot duplicate an ID.
- Missing rating summaries are neutral.
- A present rating summary must have a positive count and a sum within `[count, 5 * count]`; corrupt summaries fail explicitly instead of influencing a draw. Valid adjusted scores are still clamped to `[1.0, 5.0]` as defense in depth.
- A random source value outside `[0.0, 1.0)` fails explicitly in the selector test boundary.
- MongoDB aggregation failures propagate through the existing API error handling and UI error state.
- Rating changes do not mutate existing daily/session pick documents.
- The Void redesign must not hide actions when optional restaurant fields are absent.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--automated-behavior-tests"></a>
##### Automated Behavior Tests

1. Prove the old uniform path fails a regression requiring rating-aware selection.
2. Verify exact adjusted-rating calculations for unrated, one 5-star, one 1-star, and established averages.
3. Verify exact weight-anchor and interpolation values.
4. Verify three unique results, fewer-than-three behavior, and no-candidate behavior.
5. Verify deterministic boundary draws select the expected weighted interval and remove the selected candidate.
6. Run a fixed-seed, high-sample deterministic distribution test proving high-rated frequency > neutral frequency > low-rated frequency and moderate ratios remain within reviewed bounds.
7. Verify rating summaries are queried once per draw for only eligible IDs.
8. Verify daily generation, nearby/browser location, ZIP, and replacement all use the weighted selector.
9. Verify persisted daily/session picks remain stable until their established refresh action.
10. Verify rating display and top-rated listing behavior remain unchanged.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--frontend-and-static-tests"></a>
##### Frontend and Static Tests

1. Verify the WFL template opts into the Void shell and approved page structure.
2. Verify all existing interactive selectors and event bindings remain present.
3. Verify the probability disclosure copy is rendered safely.
4. Verify CSS covers the decision console, pick cards, controls, loading, empty, error, focus, disabled, responsive, and reduced-motion states.
5. Run established JavaScript/static asset tests and `git diff --check`.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--full-and-runtime-verification"></a>
##### Full and Runtime Verification

1. Run focused selector, repository, service, controller, and WFL frontend tests.
2. Run full `:website:test` and `:website:check` with a task-private Gradle home.
3. Package the JAR and start it on a non-8080 port with an isolated MongoDB database and deterministic candidate/rating fixtures.
4. Exercise browser-location and ZIP selection, cuisine/radius filters, “Try 3 more,” rating controls, favorite/vote/session behavior, loading/error behavior, and safe links.
5. Capture desktop and narrow/mobile visual evidence for the Decision Console and keyboard-focus states.
6. Prove repeated deterministic runtime draws favor high-rated over neutral over low-rated candidates while returning unique triples.
7. Confirm the production listener on port 8080 remains untouched during candidate testing, then clean up the candidate process and isolated database.
8. Publish a PR, pass required CI, merge, deploy the exact SHA through the protected Windows workflow, and verify production commit identity, readiness, liveness, MongoDB health, and public WFL behavior.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--acceptance-criteria"></a>
#### Acceptance Criteria

- Every new three-pick draw uses the approved confidence-adjusted weighted policy.
- Unrated restaurants have neutral weight exactly `1.0`.
- Well-established high ratings increase draw frequency and well-established low ratings reduce it according to the reviewed anchors.
- No restaurant has zero probability solely because of its rating.
- Every response contains no more than three unique eligible restaurants.
- Rating aggregation performs one candidate-bounded query per draw rather than per restaurant.
- Existing daily and session picks remain stable.
- The WFL page matches the approved Void Decision Console direction on desktop and mobile.
- All existing controls and actions remain usable by pointer and keyboard.
- Automated, alternate-port runtime, PR CI, deployment, and production checks pass.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- **Popularity feedback loop:** higher exposure may create more ratings. Mitigation: cap the maximum at 2× neutral and retain positive probability for every eligible restaurant.
- **Sparse-vote gaming:** one rating could distort odds. Mitigation: use three neutral virtual ratings and the existing one-rating-per-account/restaurant ownership rule.
- **Query growth:** daily selection can contain thousands of candidates. Mitigation: use one aggregate query and review explain/runtime behavior; do not add N+1 access.
- **Statistical test flakiness:** nondeterministic tests can fail spuriously. Mitigation: inject/fix the random sequence and seed every distribution test.
- **Visual regression:** a broad dark-theme override can break nested controls. Mitigation: scope styles to the WFL Void page, exercise every state, and inspect desktop/mobile browser evidence.
- **Implied ranking:** visual emphasis could misrepresent the random picks. Mitigation: use equal cards and neutral numeric identifiers.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--rollback-and-recovery"></a>
#### Rollback and Recovery

- Code rollback: redeploy the previous known-good merged SHA.
- Selection rollback: the change introduces no schema migration; restoring the prior service and CSS returns uniform random behavior.
- Data rollback is not expected because the feature reads existing ratings and does not rewrite rating or restaurant records.
- Existing persisted daily/session pick documents remain compatible with both versions.

<a id="source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--open-questions"></a>
#### Open Questions

None. The user approved the weighting scope, neutral handling, confidence adjustment, moderate strength, weighted-sampling approach, Decision Console direction, component boundaries, lifecycle, and validation requirements.

<!-- /migrated-source: docs/specs/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md -->

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md"></a>
## 2026-08-02 | specs | Restore Bootstrap Assets After WebJar Version Bump

Original source: `docs/specs/2026-08-02-restore-bootstrap-assets-after-webjar-version-bump.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `3f973af32bc85fc109af16893599077a92950bd062d3117c097390619478e6e9`.

<!-- migrated-source: docs/specs/2026-08-02-restore-bootstrap-assets-after-webjar-version-bump.md -->
<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--restore-bootstrap-assets-after-webjar-version-bump"></a>
### Restore Bootstrap Assets After WebJar Version Bump

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--document-status"></a>
#### Document Status

Complete

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--purpose"></a>
#### Purpose

Restore the Bootstrap CSS and JavaScript that production pages lost when the
packaged Bootstrap WebJar changed from 5.3.3 to 5.3.8 without corresponding
changes to application asset references and security matchers.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--background"></a>
#### Background

GitHub issue [#1339](https://github.com/azurras/christopherbell.dev/issues/1339)
tracks a production regression reported on 2026-08-02. The site still serves its
release-versioned custom `main.css` and JavaScript, so some styling and behavior
remain. However, `main.css` imports Bootstrap 5.3.3 and several templates load
the 5.3.3 bundle while the packaged dependency is Bootstrap 5.3.8.

Current production evidence:

- `/webjars/bootstrap/5.3.3/css/bootstrap.min.css` returns HTTP 404.
- `/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js` returns HTTP 404.
- Corresponding `5.3.8` resources return HTTP 403 because both anonymous
  security matchers still permit only the obsolete `5.3.3` namespace.
- Release-versioned custom assets return HTTP 200 and immutable cache headers.

The mismatch began in dependency update commit `20290b2f`, which changed the
Bootstrap dependency to 5.3.8 but did not update direct references or allowlists.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--goals"></a>
#### Goals

- Serve the packaged Bootstrap 5.3.8 CSS and JavaScript successfully to anonymous
  visitors.
- Restore full styling and Bootstrap-powered behavior on every affected page.
- Keep Bootstrap self-hosted through the pinned WebJar.
- Prevent a future WebJar update from silently drifting away from references and
  security matchers.
- Deliver the repair through automated tests, alternate-port runtime testing,
  required CI, merge, and production verification.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--non-goals"></a>
#### Non-Goals

- Redesign site styling or navigation.
- Switch Bootstrap to a CDN.
- Upgrade Bootstrap beyond the already packaged 5.3.8 release.
- Refactor unrelated static-asset versioning or security configuration.
- Modify the dirty authoritative checkout.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--requirements"></a>
#### Requirements

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--functional"></a>
##### Functional

1. `main.css` must import the packaged Bootstrap 5.3.8 stylesheet.
2. Every server-rendered template that loads the Bootstrap bundle must request
   the packaged 5.3.8 bundle.
3. The development feed harness must reference the packaged 5.3.8 stylesheet.
4. Anonymous `GET` requests to the exact Bootstrap 5.3.8 WebJar namespace must
   pass both static-resource classification and Spring Security authorization.
5. Obsolete Bootstrap 5.3.3 references must not remain in production source,
   templates, security matchers, documentation, or tests.
6. Other WebJar namespaces and non-GET access must remain outside the permitted
   static-resource boundary.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--non-functional"></a>
##### Non-Functional

1. The dependency remains pinned to `org.webjars:bootstrap:5.3.8`.
2. Content Security Policy continues to allow self-hosted styles/scripts without
   adding an external Bootstrap host.
3. Static WebJar behavior must remain least-privilege and method-specific.
4. Regression tests must make dependency/reference/allowlist drift visible in CI.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--proposed-approach"></a>
#### Proposed Approach

Use one repository constant only where Java security configuration benefits from
shared construction; do not add runtime indirection to static HTML or CSS.

- Replace all intentional `5.3.3` Bootstrap WebJar paths with `5.3.8`.
- Update the static-asset matcher and anonymous rule registry together.
- Update security tests to exercise the 5.3.8 CSS and bundle paths and retain
  negative tests for near-miss/method boundaries.
- Add a narrow source-consistency test that reads the Gradle dependency version
  and asserts no stale version is referenced by production resources or security
  configuration. Prefer an existing source-contract test pattern if present.
- Update documentation that names the pinned version.
- Do not touch feature code or custom CSS beyond the import URL.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--files-and-modules-involved"></a>
#### Files and Modules Involved

Expected spoke files under `website`:

- `build.gradle.kts` (dependency source of truth; expected test input, no version change)
- `src/main/resources/static/css/main.css`
- `src/main/resources/static/css/README.md`
- `src/main/resources/static/dev/feed-harness.html`
- Bootstrap-loading templates under `src/main/resources/templates/`
- `src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- `src/main/java/dev/christopherbell/configuration/security/StaticAssetRequestMatcher.java`
- `src/main/java/dev/christopherbell/configuration/security/README.md`
- `src/test/java/dev/christopherbell/configuration/SecurityConfigTest.java`
- A narrow consistency test in the configuration/static-asset test area if an
  existing suitable test does not already cover version synchronization.

Implementation occurs in an isolated worktree from refreshed `origin/main`.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--automated"></a>
##### Automated

- Start with a failing test that demonstrates 5.3.8 is not currently permitted
  and/or referenced consistently.
- Run focused static-asset/security tests.
- Run the repository JavaScript test task because templates and browser assets
  are affected.
- Run `:website:check` using a private `GRADLE_USER_HOME`.
- Run source searches proving no stale `5.3.3` reference remains in the scoped
  production/test/documentation files.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--local-runtime"></a>
##### Local Runtime

- Build and start the packaged website on a non-8080 port.
- Request the homepage, login page, and signup page.
- Request both Bootstrap 5.3.8 CSS and bundle paths anonymously and capture
  HTTP status, content type, and response length.
- Confirm the same obsolete 5.3.3 paths return 404 or remain unavailable.
- Use the browser against the alternate-port app to confirm Bootstrap-derived
  computed styling is applied and the affected pages have no failed Bootstrap
  requests.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--delivery-and-production"></a>
##### Delivery and Production

- Commit and push the spoke branch.
- Open a pull request linked to issue #1339.
- Wait for required CI checks and address only in-scope failures.
- Merge after required gates pass.
- Verify automatic production deployment by listener rotation or equivalent
  indirect evidence without weakening protected ACLs.
- Re-request public Bootstrap CSS and JavaScript and confirm HTTP 200.
- Recheck affected public pages in the browser.
- Close issue #1339 only after production verification.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--acceptance-criteria"></a>
#### Acceptance Criteria

- Public Bootstrap 5.3.8 CSS and JavaScript return HTTP 200 with the expected
  content types.
- Homepage and authentication pages render with Bootstrap styles restored.
- No production page references Bootstrap 5.3.3.
- Focused tests, JavaScript tests, and `:website:check` pass.
- Required PR CI passes and the PR is merged.
- Production verification confirms the repair before issue closure.
- Builder test report, work closure, and session memory are persisted.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--risks-and-mitigations"></a>
#### Risks and Mitigations

- Risk: changing the URL without the security matcher still yields 403.
  Mitigation: test both security registries and runtime HTTP responses.
- Risk: updating only known templates leaves another stale reference.
  Mitigation: repository-wide scoped search plus consistency coverage.
- Risk: testing on the production listener interrupts the live site.
  Mitigation: use a packaged app on a non-8080 port first.
- Risk: the authoritative checkout contains extensive unrelated work.
  Mitigation: use a refreshed-origin isolated worktree and never clean or reset
  the authoritative checkout.

<a id="source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md--open-questions"></a>
#### Open Questions

None. The packaged version, affected references, security boundary, validation
surface, and delivery path are all confirmed.

<!-- /migrated-source: docs/specs/2026-08-02-restore-bootstrap-assets-after-webjar-version-bump.md -->

<a id="source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md"></a>
## 2026-08-02 | spoke-reviews | 2026-08-02-bootstrap-webjar-asset-repair

Original source: `docs/spoke-reviews/2026-08-02-bootstrap-webjar-asset-repair.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `eb4720a97d4df92f66dc9338305d63b10608780c431af354c8b4575164ffba95`.

<!-- migrated-source: docs/spoke-reviews/2026-08-02-bootstrap-webjar-asset-repair.md -->
<a id="source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md--review-target"></a>
#### Review Target

- Repository: `azurras/christopherbell.dev`
- Branch head: `facfa97cdb33dd144fbe4aedae5cbc2e45fc2ea3`
- PR: [#1340](https://github.com/azurras/christopherbell.dev/pull/1340)
- Plan: [Implement Bootstrap WebJar Asset Repair](../implementation-plans/2026-08-02-implement-bootstrap-webjar-asset-repair.md)
- Update: [Bootstrap WebJar Asset Repair](#source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md)

<a id="source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md--findings"></a>
#### Findings

No blockers or warnings remain.

The independent review initially identified missing direct behavioral coverage
for `StaticAssetRequestMatcher`. `StaticAssetRequestMatcherTest` now proves that
5.3.8 CSS/JS GETs match, POSTs do not, and obsolete/unrelated WebJar GETs do not.
The same reviewer confirmed the finding fully closed and returned Ready to
merge: Yes.

<a id="source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md--validation-reviewed"></a>
#### Validation Reviewed

Reviewed the full base-to-head diff, focused matcher/security tests, dependency-
derived JavaScript contract, full `:website:check`, alternate-port runtime and
browser evidence, final CI/CodeQL/dependency checks, and production acceptance.
The implementation follows the final Before-Edit Brief and the
`write-jane-street-style-code` boundary/evidence rules.

<a id="source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md--merge-readiness"></a>
#### Merge Readiness

Ready and merged. PR #1340 squash-merged as
`5bd14e994a6130a32166602a6f272581abc53525`.

<!-- /migrated-source: docs/spoke-reviews/2026-08-02-bootstrap-webjar-asset-repair.md -->

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md"></a>
## 2026-08-02 | spoke-reviews | christopherbell.dev OpenStreetMap Import Rename Collision Review

Original source: `docs/spoke-reviews/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `18990e75ed8dd38e3e3395c35617ce4bb8da4fb58a252ab54dbff657f3ec8a48`.

<!-- migrated-source: docs/spoke-reviews/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review.md -->
<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md--christopherbelldev-openstreetmap-import-rename-collision-review"></a>
### christopherbell.dev OpenStreetMap Import Rename Collision Review

- Status: closed
- Repository: `azurras/christopherbell.dev`
- Branch: `codex/restaurant-import-duplicate-name`
- Base: `5bd14e994a6130a32166602a6f272581abc53525`
- Reviewed head: `3fdbafc0809a290f09504bb7fb9f8d201fc75e25`
- Pull request: [#1341](https://github.com/azurras/christopherbell.dev/pull/1341)
- Merged commit: `0dd388fb096c924453bdbab8b66a3215d3e63452`
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md)

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md--findings"></a>
#### Findings

No blockers or warnings.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md--scope-reviewed"></a>
#### Scope Reviewed

- Exact base-to-head diff and surrounding preview/apply/mutation/error paths.
- The approved invariant: globally unique normalized restaurant names.
- The boundary rule: collision resolution before mutation or persistence.
- The effect/failure rule: expected collision is throwable-free DEBUG; unrelated failures preserve their existing causes and severities.
- Regression assertions, feature documentation, runtime evidence, GitHub CI, merge state, and production evidence.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md--house-style-assessment"></a>
#### House-Style Assessment

The change meets the `write-jane-street-style-code` review rubric. It makes the collision invariant explicit in one named predicate, does not widen the public interface, preserves effect ownership inside `RestaurantService`, does not catch broad persistence errors, and includes a mutation-sensitive regression proving no conflicting save and continued processing.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md--validation-reviewed"></a>
#### Validation Reviewed

- Expected RED, then focused GREEN.
- All 56 service tests and full website test/check gates.
- Deterministic `prod,deploy-smoke` alternate-port runtime with isolated MongoDB and loopback Overpass.
- Independent reviewer: no Critical, Important, or Minor findings.
- GitHub Ubuntu, macOS, Windows, Dependency Review, and CodeQL: all successful.
- Production commit `0dd388fb`, successful 20,000-candidate catch-up, preserved collision rows, healthy endpoints/services, and no recurrence in current-release logs.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md--merge-readiness"></a>
#### Merge Readiness

Ready and merged. No residual correctness or maintenance warning remains in the approved scope.

<!-- /migrated-source: docs/spoke-reviews/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review.md -->

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md"></a>
## 2026-08-02 | spoke-reviews | christopherbell.dev What's for Lunch Location Integrity Review

Original source: `docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-location-integrity-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4bcfc98848ea80fa7e2d5555cf59cc746b0579fdda2b1648406d9b30fb51a9b5`.

<!-- migrated-source: docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-location-integrity-review.md -->
<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md--christopherbelldev-whats-for-lunch-location-integrity-review"></a>
### christopherbell.dev What's for Lunch Location Integrity Review

- Status: closed
- Repository: `azurras/christopherbell.dev`
- Reviewed implementation commits: `b85c55c7498e60a298608d18085bb356cae34e33`, `1e7cd1daa066ff3ad386ed56f9391bd94c13bb03`
- Pull requests: [#1342](https://github.com/azurras/christopherbell.dev/pull/1342), [#1343](https://github.com/azurras/christopherbell.dev/pull/1343)
- Merged/deployed head: `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md)

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md--findings"></a>
#### Findings

No blockers or warnings.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md--scope-reviewed"></a>
#### Scope Reviewed

- Removal of fabricated location behavior and strict import rejection.
- Complete Census place coverage in YAML and Java defaults.
- Coordinate-aware duplicate-city resolution, full state aliases, country validation, and rectangle ownership.
- Independent service validation before persistence.
- Regression tests, configuration equality, README source documentation, runtime evidence, PR CI, deployment, and production data reconciliation.
- Exact-ID manifest safeguards, live-value drift checks, verified backup, related-record handling, and final invariant audit.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md--house-style-assessment"></a>
#### House-Style Assessment

The implementation meets the `write-jane-street-style-code` review rubric. It states locality and rectangle ownership as explicit invariants, keeps remote Census lookup out of the runtime application boundary, preserves canonical public data, validates effects before persistence, and tests both same-name ambiguity and contradiction failures. The production mutation was isolated from application code, exact-ID and checksum bounded, preceded by a verified backup, and followed by complete postconditions.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md--validation-reviewed"></a>
#### Validation Reviewed

- Regression-first failures demonstrated the old same-name overwrite, out-of-rectangle acceptance, short coverage, and missing service defense.
- Focused final tests, 1,620-test full suite, full check gate, and alternate-port runtime passed.
- Required GitHub CI passed and exact merge SHA `1d1b322d` deployed healthy.
- Production import succeeded with 0 invalid candidates.
- Backup dry run, 215-record drift preflight, 199 updates, 16 deletes, and final 0-violation audit passed.
- All four public metros returned canonical locations over HTTP 200; readiness, liveness, and MongoDB remained healthy.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md--merge-and-closure-readiness"></a>
#### Merge and Closure Readiness

Ready, merged, deployed, reconciled, and closed. No residual correctness or maintenance warning remains in the approved scope.

<!-- /migrated-source: docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-location-integrity-review.md -->

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md"></a>
## 2026-08-02 | spoke-reviews | christopherbell.dev WFL Rating-Weighted Void Review

Original source: `docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `bcc8e3f4df01a67854244a1c095b8ad61e9267646613299aba1200630a796d6c`.

<!-- migrated-source: docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review.md -->
<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md--christopherbelldev-wfl-rating-weighted-void-review"></a>
### christopherbell.dev WFL Rating-Weighted Void Review

- Status: closed
- Repository: `azurras/christopherbell.dev`
- Reviewed range: `1d1b322dc1667e48bc0230009a3fe79fce0a1b90..58019300a65af830f40a9f7a39e334214e0d9eb7`
- Pull request: [#1344](https://github.com/azurras/christopherbell.dev/pull/1344)
- Merged/deployed commit: `9c69623049829394f245515b8d1751c9f7579271`
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md)

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md--findings"></a>
#### Findings

No open blockers or warnings.

The initial independent review found one important accessibility defect: logged-in rating paragraphs received a dark shared paragraph color because the Void rule styled only the parent container. The required change added direct scoped selectors for `p.lunch-rating-summary` and `.lunch-rating-summary p`, plus a failing-then-passing regression. Re-review confirmed both selectors exceed the shared rule's specificity and returned a ready-to-merge verdict with no remaining critical, important, or minor issues.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md--scope-reviewed"></a>
#### Scope Reviewed

- Confidence-adjusted rating formula and approved anchor interpolation.
- Positive-probability weighted sampling without replacement and input validation.
- One batched Mongo aggregation and service integration across all required pick flows.
- Stored daily/shared-session stability and replacement survivor behavior.
- Dedicated stylesheet ownership, Void presentation, exact disclosure, non-ranked cards, desktop/mobile layout, focus, and reduced motion.
- Regression quality, full repository validation, alternate-port runtime, CI/CodeQL, and production acceptance.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md--house-style-assessment"></a>
#### House-Style Assessment

The implementation meets the `write-jane-street-style-code` review rubric. Rating adjustment and selection are explicit pure boundaries; persistence order is preserved; malformed summaries and random samples fail closed; MongoDB work is bounded to one aggregation; CSS ownership is feature-scoped; and tests cover distribution, deterministic behavior, flow wiring, accessibility cascade, and runtime presentation.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md--validation-reviewed"></a>
#### Validation Reviewed

- Regression-first failures and fixes for selector, aggregation, service integration, page ownership, and authenticated contrast.
- Final focused and repository-wide automated gates.
- Alternate-port HTTP and Chrome desktop/mobile evidence.
- Required GitHub checks, exact merged-tree equality, listener rotation, production assets, live APIs, and authenticated production computed styles.

<a id="source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md--merge-and-closure-readiness"></a>
#### Merge and Closure Readiness

Ready, merged, auto-deployed, production-verified, and closed. No residual correctness or maintenance warning remains in the approved scope.

<!-- /migrated-source: docs/spoke-reviews/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review.md -->

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md"></a>
## 2026-08-02 | spoke-reviews | Restaurant Profile Void SEO Review

Original source: `docs/spoke-reviews/2026-08-02-restaurant-profile-void-seo-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `39f515ed8dade4fa08d04b936abd861536dd43056a1ad0df79b1ea01e5dca433`.

<!-- migrated-source: docs/spoke-reviews/2026-08-02-restaurant-profile-void-seo-review.md -->
<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--restaurant-profile-void-seo-review"></a>
### Restaurant Profile Void SEO Review

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--status"></a>
#### Status

closed

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--related-work"></a>
#### Related Work

- [Central work record](#source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md)
- [Spoke update](#source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md)
- [Test report](../test-reports/2026-08-02-restaurant-profile-void-seo-test-report.md)
- [PR #1345](https://github.com/azurras/christopherbell.dev/pull/1345)

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--reviewed-scope"></a>
#### Reviewed Scope

Reviewed the complete `origin/main...4535eb0e` diff, service and controller boundaries, Thymeleaf rendering and JSON-LD serialization, JavaScript enhancement behavior, scoped CSS ownership, unit/browser evidence, GitHub checks, merge state, and production behavior.

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--findings"></a>
#### Findings

No blockers or warnings.

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--boundary-and-style-review"></a>
#### Boundary and Style Review

- The public projection is immutable, validates optional fields, and intentionally excludes personal and audit data.
- The controller performs one canonical lookup and remains thin.
- JSON-LD is serialized by Jackson with script-element-safe escaping; unsafe persisted website schemes are omitted.
- The template provides meaningful semantic HTML without JavaScript and emits structured data only for a valid profile.
- JavaScript owns only authenticated personal controls and contains local failure handling that cannot erase public content.
- CSS remains scoped beneath the WFL Void page boundary and does not restyle Top Rated or Favorites.
- Focused tests cover success, sparse input, malformed input, privacy, authorization fallback, accessibility, and responsive failure modes.
- The implementation follows the repository's Jane Street-style invariant, boundary, failure, and evidence standards.

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--validation-reviewed"></a>
#### Validation Reviewed

- Exact branch-tip `:website:check --rerun-tasks` success.
- Raw alternate-port HTTP assertions and real browser acceptance at two viewports.
- GitHub CI matrix, dependency review, and CodeQL success.
- Merged production canonical, JSON-LD, sitemap, assets, missing-profile noindex, health, and service evidence.

<a id="source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md--merge-readiness-and-disposition"></a>
#### Merge Readiness and Disposition

Ready and merged. PR #1345 was squash-merged to `main` as `363bb986581c4d20df3434154844807ce88701e4`; production acceptance passed afterward.

<!-- /migrated-source: docs/spoke-reviews/2026-08-02-restaurant-profile-void-seo-review.md -->

<a id="source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md"></a>
## 2026-08-02 | spoke-updates | 2026-08-02-bootstrap-webjar-asset-repair

Original source: `docs/spoke-updates/2026-08-02-bootstrap-webjar-asset-repair.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `dff56566940154b97a31b4e9a41af967cc227523b1a081905a38085e092bc756`.

<!-- migrated-source: docs/spoke-updates/2026-08-02-bootstrap-webjar-asset-repair.md -->
<a id="source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md--source"></a>
#### Source

- Repository: `azurras/christopherbell.dev`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\bootstrap-assets-1339`
- Branch: `codex/issue-1339-bootstrap-assets`
- Base: `2b40bd860d9e4e05aa18b4dd63e13a390d41208e`
- Final branch head: `facfa97cdb33dd144fbe4aedae5cbc2e45fc2ea3`
- PR: [#1340](https://github.com/azurras/christopherbell.dev/pull/1340)
- Merge: `5bd14e994a6130a32166602a6f272581abc53525`
- Related work: [Bootstrap Asset Regression](#source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md)

<a id="source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md--status"></a>
#### Status

Complete and deployed.

<a id="source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md--changes"></a>
#### Changes

Aligned all Bootstrap WebJar references and both exact security boundaries with
packaged version 5.3.8. Added dependency-derived resource scanning, public
allowlist assertions, and direct `StaticAssetRequestMatcher` GET/POST and
version-boundary tests. Updated pinned-version documentation.

<a id="source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md--validation"></a>
#### Validation

- `:website:check`: BUILD SUCCESSFUL; 1,610 Java, 312 JavaScript, and 150 Pester tests.
- Alternate-port packaged app on 8091: readiness UP; current CSS/JS 200; old paths 403; browser rendering passed.
- Independent review: initial matcher-test gap fixed; re-review had no actionable findings and approved merge.
- GitHub: all OS builds, CodeQL lanes, and dependency review passed.
- Production: PID 33024 rotated to 2956; readiness/liveness UP; exact assets and browser rendering passed; required services Running/Automatic.

<a id="source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md--risks-and-follow-ups"></a>
#### Risks and Follow-ups

No issue-scoped gaps remain. The unrelated local-profile WFL duplicate-key
catch-up log remains outside issue #1339.

<!-- /migrated-source: docs/spoke-updates/2026-08-02-bootstrap-webjar-asset-repair.md -->

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md"></a>
## 2026-08-02 | spoke-updates | christopherbell.dev OpenStreetMap Import Rename Collision Completion

Original source: `docs/spoke-updates/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `68c9a563f2d187772fcd242da18d1ec1a1aea66069b524c2a70f3439445b10aa`.

<!-- migrated-source: docs/spoke-updates/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion.md -->
<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md--christopherbelldev-openstreetmap-import-rename-collision-completion"></a>
### christopherbell.dev OpenStreetMap Import Rename Collision Completion

- Status: closed
- Source repository: `azurras/christopherbell.dev`
- Reporting agent: Codex root agent
- Branch: `codex/restaurant-import-duplicate-name`
- Implementation commit: `3fdbafc0809a290f09504bb7fb9f8d201fc75e25`
- Pull request: [#1341](https://github.com/azurras/christopherbell.dev/pull/1341)
- Merged commit: `0dd388fb096c924453bdbab8b66a3215d3e63452`
- Related work: [OpenStreetMap Import Rename Collision](#source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md)

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md--changes-made"></a>
#### Changes Made

- Added one normalized-name-owner collision predicate in `RestaurantService`.
- Applied the predicate before preview classification and before apply mutation/save for existing OpenStreetMap IDs.
- Classified preview collisions as unchanged and apply collisions as skipped existing.
- Kept expected collision diagnostics at DEBUG and left genuine remote, lease, repository, and persistence failures unchanged.
- Added an exact regression proving both existing records remain unchanged and a later candidate still imports.
- Updated the restaurant feature README.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md--files-touched"></a>
#### Files Touched

- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantService.java`
- `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantServiceTest.java`
- `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/README.md`

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md--validation"></a>
#### Validation

- Observed expected regression RED before the implementation.
- Focused test passed; all 56 `RestaurantServiceTest` tests passed.
- `:website:test`: exit 0, 2m35s.
- `:website:check`: exit 0, 2m58s.
- Alternate-port runtime report: [OpenStreetMap Import Rename Collision Test Report](../test-reports/2026-08-02-openstreetmap-import-rename-collision-test-report.md), PASS.
- Independent review found no Critical, Important, or Minor findings.
- Required PR checks passed on Ubuntu, macOS, Windows, Dependency Review, and CodeQL.
- Production Mission Control reports application commit `0dd388fb` and healthy telemetry.
- Production startup catch-up completed `SUCCEEDED`: fetched 20,000, imported 296, updated 442, skipped existing 19,262, skipped invalid 0.
- The two collision documents retained their pre-deployment name, normalized name, address, and `lastUpdatedOn` values.
- Readiness, liveness, local homepage, public homepage, and nearby API returned HTTP 200; all four Windows services remain Running/Automatic.
- Fresh current-release log searches found no `DuplicateKeyException` or `OpenStreetMap import failed` recurrence.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md--blockers-and-risks"></a>
#### Blockers and Risks

None. The full source response reached the configured 20,000 candidate limit, which is existing behavior outside this fix.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md--next-actions"></a>
#### Next Actions

No required spoke action remains.

<!-- /migrated-source: docs/spoke-updates/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion.md -->

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md"></a>
## 2026-08-02 | spoke-updates | christopherbell.dev What's for Lunch Location Integrity Completion

Original source: `docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-location-integrity-completion.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `31397b917802ae5b0ef21559ae9d251b9050407e0887e9fd7bdb368147fd8cba`.

<!-- migrated-source: docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-location-integrity-completion.md -->
<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md--christopherbelldev-whats-for-lunch-location-integrity-completion"></a>
### christopherbell.dev What's for Lunch Location Integrity Completion

- Status: closed
- Source repository: `azurras/christopherbell.dev`
- Reporting agent: Codex root agent
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-import-location-integrity-20260802`
- Implementation commits: `b85c55c7498e60a298608d18085bb356cae34e33`, `1e7cd1daa066ff3ad386ed56f9391bd94c13bb03`
- Pull requests: [#1342](https://github.com/azurras/christopherbell.dev/pull/1342), [#1343](https://github.com/azurras/christopherbell.dev/pull/1343)
- Merged commits: `178d90caca58d2f6284f54ab2ef4514d10df2918`, `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`
- Related work: [What's for Lunch Import Location Integrity](#source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md)

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md--changes-made"></a>
#### Changes Made

- Removed the fabricated `Imported Metro, TX` fallback and required an explicit supported locality before import.
- Added independent service-boundary validation for canonical city/state/country, coordinates, and metro rectangle ownership.
- Expanded the four existing import rectangles to all 393 unique official Census places they intersect: Austin 70, Bay Area 154, New Orleans 46, Dallas 123.
- Made duplicate city names coordinate-aware and accepted canonical state abbreviations or full state names without permitting contradictions.
- Added regression coverage for missing location data, same-name cities across states, expanded places, full state names, and city/coordinate mismatch.
- Documented the fixed Census 2025 configuration source and kept Census/geocoding out of the runtime import path.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md--production-data-work"></a>
#### Production Data Work

- Removed 6,825 exact legacy `Imported Metro` rows after the first verified backup.
- Deployed the expanded importer and completed a fresh production import: 10,796 fetched, 86 imported, 136 updated, 10,574 skipped existing, 0 skipped invalid.
- Took and restore-dry-run-verified a new 2,050,494-byte MongoDB archive immediately before final reconciliation.
- Rebuilt an exact post-import manifest from production and queried current Census TIGERweb place layers for all 215 remaining violations.
- Corrected 199 exact IDs to their Census place and deleted only 16 exact IDs with no incorporated-place or Census-designated-place match.
- Deleted 0 favorites and 0 ratings because none referenced the 16 removals; historical sessions were preserved.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md--validation"></a>
#### Validation

- Focused final suite: 78 tests passed.
- `:website:test`: 1,620 tests, 0 failures, 0 errors, 3 skipped.
- `:website:check`: passed, including 76 Pester executions.
- Alternate-port packaged-JAR runtime: PASS on port 8098 with isolated MongoDB and loopback Overpass.
- Required CI passed for both PRs; both exact merge SHAs deployed healthy.
- Final production audit: 7,338 OSM rows, 7,338 valid, 0 invalid, 0 synthetic metro placeholders.
- Readiness, liveness, and four public nearby metro requests returned HTTP 200; MongoDB ping returned `ok: 1`.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md--blockers-and-risks"></a>
#### Blockers and Risks

None. The checked-in official place list is intentionally pinned to the Census January 1, 2025 vintage and should be refreshed deliberately when the product adopts newer geography.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md--next-actions"></a>
#### Next Actions

No required spoke action remains.

<!-- /migrated-source: docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-location-integrity-completion.md -->

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md"></a>
## 2026-08-02 | spoke-updates | christopherbell.dev WFL Rating-Weighted Void Completion

Original source: `docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4fdab3ff5c053fd3e9d8045787bc48eb57e4e8b9c87e8359057e103fb250c778`.

<!-- migrated-source: docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion.md -->
<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md--christopherbelldev-wfl-rating-weighted-void-completion"></a>
### christopherbell.dev WFL Rating-Weighted Void Completion

- Status: closed
- Source repository: `azurras/christopherbell.dev`
- Reporting agent: Codex root agent
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\wfl-rating-weighted-void`
- Feature head: `58019300a65af830f40a9f7a39e334214e0d9eb7`
- Pull request: [#1344](https://github.com/azurras/christopherbell.dev/pull/1344)
- Merged commit: `9c69623049829394f245515b8d1751c9f7579271`
- Related work: [WFL rating-weighted Void upgrade](#source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md)

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md--changes-made"></a>
#### Changes Made

- Added `RatingWeightedRestaurantSelector` with three neutral virtual ratings, approved piecewise-linear weights, controlled randomness, validation, and sampling without replacement.
- Added one bounded MongoDB aggregation to retrieve count and sum for all candidate restaurant IDs.
- Routed coordinate/ZIP picks, daily refreshes, and deleted-pick replacements through the shared selector while preserving stored daily and shared-session order.
- Added selector distribution/edge tests, Mongo aggregation tests, service flow tests, and frontend ownership/accessibility tests.
- Rebuilt `/wfl` as a scoped Void Decision Console with a three-card desktop grid, single-column mobile layout, exact weighting disclosure, no numeric rank implication, focus visibility, reduced-motion handling, and a dedicated stylesheet.
- Corrected the reviewer-found authenticated rating-color cascade and preserved both anonymous and authenticated rating markup at a 9.06:1 contrast ratio.
- Updated WFL and stylesheet ownership documentation.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md--validation"></a>
#### Validation

- Regression-first RED/GREEN evidence was observed for selector, rating aggregation, service flows, frontend ownership, and authenticated rating contrast.
- Focused tests passed: 8 selector, 3 rating query, 60 service, and 313 JavaScript tests.
- Final `:website:check` passed after review correction in 2 minutes 56 seconds, including 150 Pester tests and deployment build checks.
- Alternate-port runtime on `:8081` returned HTTP 200 for health, `/wfl`, today, coordinate nearby, and ZIP nearby flows.
- Independent review found and closed one important accessibility issue; final verdict was ready to merge with no remaining findings.
- GitHub CI passed on Windows, macOS, and Ubuntu; dependency review and all CodeQL analyses passed.
- Production auto-deployed the merged tree, rotated the listener, and passed public HTTPS plus authenticated desktop/mobile acceptance.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md--blockers-and-risks"></a>
#### Blockers and Risks

None. The weighted distribution intentionally changes frequency over repeated fresh draws without changing eligibility or already-persisted picks.

<a id="source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md--next-actions"></a>
#### Next Actions

No required spoke action remains.

<!-- /migrated-source: docs/spoke-updates/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion.md -->

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md"></a>
## 2026-08-02 | spoke-updates | Restaurant Profile Void SEO

Original source: `docs/spoke-updates/2026-08-02-restaurant-profile-void-seo.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `86eb8b3b1d60fd2d9756477a83e470b1afb264c1b127f316f61df81dcab6b1bc`.

<!-- migrated-source: docs/spoke-updates/2026-08-02-restaurant-profile-void-seo.md -->
<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--restaurant-profile-void-seo"></a>
### Restaurant Profile Void SEO

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--status"></a>
#### Status

closed

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--related-work"></a>
#### Related Work

- [Central work record](#source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md)
- [Implementation plan](../implementation-plans/2026-08-02-restaurant-profiles-void-seo.md)
- [Test report](../test-reports/2026-08-02-restaurant-profile-void-seo-test-report.md)

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--source-repository"></a>
#### Source Repository

- Repository: `azurras/christopherbell.dev`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\restaurant-profile-void-seo`
- Branch: `codex/restaurant-profile-void-seo`
- Pull request: [#1345 Render indexable Void restaurant profiles](https://github.com/azurras/christopherbell.dev/pull/1345)
- Branch tip tested: `4535eb0ecad0711e3a509f4f37ec31230cc50d6a`
- Merged SHA: `363bb986581c4d20df3434154844807ce88701e4`

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--changes-made"></a>
#### Changes Made

- Added one immutable public-only restaurant profile page model and mapping service.
- Server-rendered complete semantic public profile content, one canonical URL, and conditional schema.org `Restaurant` JSON-LD.
- Preserved content-free `404` responses with `noindex,nofollow` and no JSON-LD for missing or malformed profiles.
- Prevented member rating/favorite state, creator/modifier identities, and audit fields from crossing the public view boundary.
- Reduced the browser module to authenticated personal-control progressive enhancement; anonymous visitors perform no redundant detail fetch.
- Moved profile presentation into scoped `whats-for-lunch.css` Void ownership with responsive, overflow-safe, keyboard-visible behavior.
- Updated WFL, JavaScript, and stylesheet ownership documentation.

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--commits"></a>
#### Commits

- `df77ef43` Render public restaurant profile data
- `64ee8195` Server render restaurant profiles
- `568dc3a9` Enhance restaurant member controls
- `dcd35a94` Style restaurant profiles in Void
- `7efb54b5` Document indexable restaurant profiles
- `4535eb0e` Keep profile rating signal intact

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--validation"></a>
#### Validation

- Regression-first focused Java, raw-view, JavaScript, CSS ownership, accessibility, desktop-wrap, and mobile-overflow tests passed.
- `:website:check --rerun-tasks --no-daemon --console=plain` passed in 3m14s with 21 tasks executed.
- JavaScript suite passed 320 tests; Windows production-script suite passed 74 tests with zero failures.
- Isolated port `8094` HTTP and browser verification passed for complete, sparse, missing, anonymous, authenticated, stale-session, desktop, mobile, and keyboard cases.
- GitHub Ubuntu, macOS, Windows, dependency-review, and CodeQL checks passed.
- Production verification passed through loopback and `https://www.christopherbell.dev` after listener rotation from PID `55848` to `59036`.

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--files-touched"></a>
#### Files Touched

The primary files are `RestaurantProfilePage.java`, `RestaurantProfilePageService.java`, `WhatsForLunchViewController.java`, `restaurant.html`, `restaurant-profile.js`, and `whats-for-lunch.css`, with focused Java/JavaScript tests and feature documentation.

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--blockers-and-risks"></a>
#### Blockers and Risks

None. `gradlew.bat` remains a line-ending-only worktree artifact and was never staged. The authoritative checkout at `A:\Projects\christopherbell.dev` was not modified.

<a id="source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md--next-actions"></a>
#### Next Actions

None required.

<!-- /migrated-source: docs/spoke-updates/2026-08-02-restaurant-profile-void-seo.md -->

<a id="source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md"></a>
## 2026-08-02 | work-closures | 2026-08-02-bootstrap-webjar-asset-repair

Original source: `docs/work-closures/2026-08-02-bootstrap-webjar-asset-repair.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `a7bbe45a23a93df3b1f2d4387637b90e9dd48446ee9e3db014cd2096cdbf33c8`.

<!-- migrated-source: docs/work-closures/2026-08-02-bootstrap-webjar-asset-repair.md -->
<a id="source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md--final-status"></a>
#### Final Status

Closed. The Bootstrap WebJar asset regression is fixed, merged, automatically
deployed, and production-verified.

<a id="source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md--related-artifacts"></a>
#### Related Artifacts

- Work: [Bootstrap Asset Regression](#source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md)
- Spec: [Restore Bootstrap Assets After WebJar Version Bump](#source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md)
- Plan: [Implement Bootstrap WebJar Asset Repair](../implementation-plans/2026-08-02-implement-bootstrap-webjar-asset-repair.md)
- Test report: [Bootstrap WebJar Asset Repair Test Report](../test-reports/2026-08-02-bootstrap-webjar-asset-repair-test-report.md)
- Spoke update: [Bootstrap WebJar Asset Repair](#source-docs-spoke-updates-2026-08-02-bootstrap-webjar-asset-repair-md)
- Spoke review: [Bootstrap WebJar Asset Repair](#source-docs-spoke-reviews-2026-08-02-bootstrap-webjar-asset-repair-md)
- Issue: [#1339](https://github.com/azurras/christopherbell.dev/issues/1339)
- PR: [#1340](https://github.com/azurras/christopherbell.dev/pull/1340)

<a id="source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md--completed-scope"></a>
#### Completed Scope

Corrected Bootstrap 5.3.8 references, security allowlists, JWT static-resource
matching, regression coverage, and pinned documentation. Preserved the dirty
authoritative checkout by using an isolated worktree.

<a id="source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md--delivery-and-validation"></a>
#### Delivery and Validation

PR #1340 passed Linux/macOS/Windows Java 25 builds, CodeQL, dependency review,
and independent review, then squash-merged as
`5bd14e994a6130a32166602a6f272581abc53525`. Local full checks and alternate-port
runtime/browser testing passed. Production rotated cleanly, reached UP
liveness/readiness, serves exact current assets, denies obsolete paths, renders
Bootstrap styles in-browser, and retains all required native services Running
and Automatic.

<a id="source-docs-work-closures-2026-08-02-bootstrap-webjar-asset-repair-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

No issue-scoped gaps or required follow-ups remain. An unrelated local-profile
WFL duplicate-key catch-up log is documented in the test report.

<!-- /migrated-source: docs/work-closures/2026-08-02-bootstrap-webjar-asset-repair.md -->

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md"></a>
## 2026-08-02 | work-closures | christopherbell.dev OpenStreetMap Import Rename Collision Closure

Original source: `docs/work-closures/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `e9fc77462810516e844a42a9b78157e74861667cefae4900c42755884d6dd5d7`.

<!-- migrated-source: docs/work-closures/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure.md -->
<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--christopherbelldev-openstreetmap-import-rename-collision-closure"></a>
### christopherbell.dev OpenStreetMap Import Rename Collision Closure

- Status: closed
- Closed: 2026-08-02
- Central work: [OpenStreetMap Import Rename Collision](#source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md)
- Specification: [OpenStreetMap Import Rename Collision](#source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md)
- Implementation plan: [OpenStreetMap Import Rename Collision](../implementation-plans/2026-08-02-christopherbell-dev-osm-import-rename-collision.md)
- Test report: [OpenStreetMap Import Rename Collision Test Report](../test-reports/2026-08-02-openstreetmap-import-rename-collision-test-report.md)
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md)
- Spoke review: [Review](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md)
- Session memory: [OpenStreetMap Import Rename Collision Fix](#source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md)

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--final-status"></a>
#### Final Status

Closed. The recurring startup-catch-up duplicate-key error was reproduced, fixed without weakening the unique index, independently reviewed, merged, deployed, and verified in production.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--completed-scope"></a>
#### Completed Scope

- Diagnosed the exact upstream ID rename/name-owner collision using supplied logs, current source, live OpenStreetMap data, and read-only production MongoDB evidence.
- Added preview and apply guards before mutation/save.
- Preserved global normalized-name uniqueness and genuine failure visibility.
- Added regression coverage and feature documentation.
- Completed isolated alternate-port runtime verification and cleanup.
- Published, passed required CI, merged, deployed, and verified production.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--spoke-delivery"></a>
#### Spoke Delivery

- Repository: `azurras/christopherbell.dev`
- Branch: `codex/restaurant-import-duplicate-name`
- Implementation commit: `3fdbafc0809a290f09504bb7fb9f8d201fc75e25`
- Pull request: [#1341](https://github.com/azurras/christopherbell.dev/pull/1341)
- Merged and deployed commit: `0dd388fb096c924453bdbab8b66a3215d3e63452`

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--validation"></a>
#### Validation

- Expected RED, focused GREEN, 56 service tests passed.
- Full website test and check gates passed.
- Deterministic local runtime PASS on port 8096 with exact data/response/log evidence.
- Independent review: no findings.
- GitHub Ubuntu, macOS, Windows, Dependency Review, and CodeQL: successful.
- Production Mission Control: HEALTHY, application commit `0dd388fb`, production service Running, Mongo connectivity live.
- Production catch-up: `SUCCEEDED`, `lastCompletedMonth=2026-08`, fetched 20,000, imported 296, updated 442, skipped existing 19,262, skipped invalid 0.
- Both collision documents retained their pre-deployment names, normalized names, addresses, and timestamps.
- Local/public health and application requests returned HTTP 200 with required public security headers.
- MongoDB, ChristopherBellDev, ChristopherBellMediaWorker, and cloudflared remained Running/Automatic.
- Current-release Mission Control searches found no `DuplicateKeyException` or `OpenStreetMap import failed` recurrence.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--closure-readiness"></a>
#### Closure Readiness

ready

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--closure-text"></a>
#### Closure Text

Completed the user-reported recurring OpenStreetMap startup catch-up failure. The fix preserves the unique normalized-name invariant, skips only an ID rename owned by another restaurant before mutation, and continues the import. PR #1341 passed all required CI and merged as `0dd388fb096c924453bdbab8b66a3215d3e63452`. Production is live on that commit; the catch-up completed successfully and the original duplicate-key signature did not recur. The source was a direct user request rather than a GitHub issue, so no issue comment trust decision or GitHub issue closure was applicable. The supplied attachment came directly from the user. No known gap or required follow-up remains.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--decisions"></a>
#### Decisions

- Keep one global normalized-name owner rather than creating location-scoped duplicate semantics.
- Skip expected ID rename collisions rather than catch arbitrary duplicate-key exceptions.
- Use DEBUG for the expected branch and retain ERROR for real workflow failure.
- Respect protected production ACLs and rely on the existing SYSTEM deployment path plus Mission Control for exact release evidence.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

None required. The 20,000-candidate source limit was reached during production import; that is existing configured behavior outside this defect.

<!-- /migrated-source: docs/work-closures/2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure.md -->

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md"></a>
## 2026-08-02 | work-closures | christopherbell.dev What's for Lunch Location Integrity Closure

Original source: `docs/work-closures/2026-08-02-christopherbell-dev-wfl-location-integrity-closure.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4978b4b3452fe73ed640745d630145e06a40b311502afc3ede3400299c903d8c`.

<!-- migrated-source: docs/work-closures/2026-08-02-christopherbell-dev-wfl-location-integrity-closure.md -->
<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--christopherbelldev-whats-for-lunch-location-integrity-closure"></a>
### christopherbell.dev What's for Lunch Location Integrity Closure

- Status: closed
- Closed: 2026-08-02
- Central work: [What's for Lunch Import Location Integrity](#source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md)
- Specifications: [Strict import](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md), [legacy reconciliation](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md)
- Implementation plans: [strict import](../implementation-plans/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md), [legacy reconciliation](../implementation-plans/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md)
- Test reports: [strict import](../test-reports/2026-08-02-wfl-import-location-integrity-test-report.md), [legacy reconciliation](../test-reports/2026-08-02-wfl-legacy-location-reconciliation-test-report.md)
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md)
- Spoke review: [Final review](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md)
- Session memory: [Location integrity and reconciliation](#source-docs-session-memory-2026-08-02-wfl-location-integrity-and-reconciliation-md)

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--final-status"></a>
#### Final Status

Closed. What's for Lunch no longer fabricates `Imported Metro, TX`; incomplete or contradictory OSM locations are rejected; all official places intersecting the four configured import rectangles are supported; and the legacy production catalog has been reconciled to zero violations.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--completed-scope"></a>
#### Completed Scope

- Removed fabricated fallback behavior and 6,825 exact placeholder rows.
- Added strict client and service validation.
- Added 393 pinned Census places with coordinate-aware ownership and state alias support.
- Completed regression-first development, full automated testing, alternate-port runtime validation, PR/CI/merge, and exact-SHA production deployment.
- Completed a live import, a second verified backup, a fresh exact Census manifest, 199 canonical updates, 16 no-place deletions, and final production verification.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--spoke-delivery"></a>
#### Spoke Delivery

- Repository: `azurras/christopherbell.dev`
- Strict import PR: [#1342](https://github.com/azurras/christopherbell.dev/pull/1342), merged `178d90caca58d2f6284f54ab2ef4514d10df2918`.
- Reconciliation PR: [#1343](https://github.com/azurras/christopherbell.dev/pull/1343), merged and deployed `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--production-evidence"></a>
#### Production Evidence

- Import `SUCCEEDED`: fetched 10,796, imported 86, updated 136, skipped existing 10,574, skipped invalid 0.
- Backup archive SHA-256: `E8999314FC31EB440D5A142D317F628231B4B6BA25962C30FAA4F000CD92CD23`; restore dry run passed.
- Manifest SHA-256: `A6391EFC45FB88033B25DEA77A06C2C358E551A256EA69FFB59C53F624677918`.
- Receipt SHA-256: `F76FBD81E7401BBC85C3DB35EA52334E792D1B95DB541601D1E1197B44BA12E4`.
- Final audit SHA-256: `E3E31D0B5F5C5A7283DA22DF1CFE5EB4EF234229CEFF9F2588F37B4857ACA055`.
- Final audit: 7,338 OSM rows, 7,338 valid, 0 invalid, 0 synthetic metro placeholders.
- Total catalog: 7,340 restaurants; Back Office refreshed to the same count.
- Readiness and liveness HTTP 200 `UP`; MongoDB ping `ok: 1`; production listener PID `57904`.
- Austin, Bay Area, New Orleans, and Dallas nearby requests each returned HTTP 200 with no state/country mismatch.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--closure-text"></a>
#### Closure Text

Completed the user-reported What's for Lunch location-data repair. PRs #1342 and #1343 passed required CI, merged, and deployed. Production now accepts only canonical supported locations with valid coordinates and rectangle ownership, and the final exact Census reconciliation retained every resolvable record while deleting only 16 records for which Census places could not be established. No GitHub issue closure was applicable because the source was a direct user request.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--decisions"></a>
#### Decisions

- Prefer absence over invented location data.
- Treat current Census incorporated places and CDPs as the authoritative locality set.
- Use coordinates to disambiguate repeated city names and reject city/rectangle contradictions.
- Pin geography in application configuration; do not introduce a runtime geocoder dependency.
- Require verified backup, exact-ID drift checks, checksummed evidence, and complete postconditions for production cleanup.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

None required. Census geography is pinned to January 1, 2025 and should only be refreshed through a reviewed future change.

<!-- /migrated-source: docs/work-closures/2026-08-02-christopherbell-dev-wfl-location-integrity-closure.md -->

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md"></a>
## 2026-08-02 | work-closures | christopherbell.dev WFL Rating-Weighted Void Closure

Original source: `docs/work-closures/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `7a42eaf77e308afa0ed29e9cedbdb432e3ab3171d8c8aa9bf85be435cfba0fea`.

<!-- migrated-source: docs/work-closures/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure.md -->
<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--christopherbelldev-wfl-rating-weighted-void-closure"></a>
### christopherbell.dev WFL Rating-Weighted Void Closure

- Status: closed
- Closed: 2026-08-02
- Central work: [WFL rating-weighted Void upgrade](#source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md)
- Specification: [Approved product specification](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md)
- Implementation plan: [Approved implementation plan](../implementation-plans/2026-08-02-wfl-rating-weighted-void-upgrade.md)
- Test report: [Runtime and production evidence](../test-reports/2026-08-02-wfl-rating-weighted-void-upgrade-test-report.md)
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md)
- Spoke review: [Final review](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md)
- Session memory: [WFL rating-weighted Void upgrade](#source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md)

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--final-status"></a>
#### Final Status

Closed. Fresh WFL draws now favor higher-rated restaurants and reduce lower-rated frequency while leaving every eligible restaurant possible, and `/wfl` now uses the responsive Void Decision Console design.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--completed-scope"></a>
#### Completed Scope

- Implemented the approved neutral-prior rating adjustment and moderate weight curve.
- Applied weighted sampling without replacement to coordinate/ZIP, daily refresh, and deleted-pick replacement paths.
- Preserved previously persisted daily and shared-session picks.
- Batched all candidate rating summaries in one MongoDB aggregation.
- Delivered the dedicated scoped Void stylesheet, exact disclosure, non-ranked cards, and accessible responsive behavior.
- Completed regression-first development, independent review and correction, full testing, alternate-port runtime, PR/CI/CodeQL, merge, automatic deployment, and production verification.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--spoke-delivery"></a>
#### Spoke Delivery

- Repository: `azurras/christopherbell.dev`
- Feature head: `58019300a65af830f40a9f7a39e334214e0d9eb7`.
- PR [#1344](https://github.com/azurras/christopherbell.dev/pull/1344) merged as `9c69623049829394f245515b8d1751c9f7579271`.
- The merged tree `865eb52e7591fadd71551956e77459706671cbe0` exactly matches the fully verified feature tree.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--production-evidence"></a>
#### Production Evidence

- Automatic deployment rotated the production listener from PID `57904` to PID `55848`.
- Fingerprinted production asset: `/db0009f03ea001ffc654/css/whats-for-lunch.css`.
- Liveness and readiness returned HTTP 200 with `{"status":"UP"}` over public HTTPS.
- `/wfl`, today, coordinate nearby, and ZIP nearby requests all returned HTTP 200.
- Sampled live restaurants carried real city/state values and no `Imported Metro, TX` placeholder.
- Authenticated desktop rendered three equal 373 by 474 cards; mobile rendered three aligned 309-pixel cards; both had zero horizontal overflow.
- Authenticated overall and personal rating lines computed to the corrected teal on all cards; no browser console warnings or errors were present.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--closure-text"></a>
#### Closure Text

Completed the direct user request. PR #1344 passed required CI and CodeQL, merged, auto-deployed, and passed production acceptance. No GitHub issue closure was applicable because the source was a direct user request.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--decisions"></a>
#### Decisions

- Treat unrated restaurants as neutral with three virtual three-star ratings.
- Use moderate linear interpolation between 1-star 0.35, 2-star 0.60, 3-star 1.00, 4-star 1.50, and 5-star 2.00 anchors.
- Sample without replacement so each draw remains unique and every eligible restaurant stays possible.
- Preserve existing stored draws until their normal refresh/reset boundary.
- Keep the redesign owned by `/wfl` through a dedicated stylesheet rather than changing neighboring WFL pages.

<a id="source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

None required.

<!-- /migrated-source: docs/work-closures/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure.md -->

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md"></a>
## 2026-08-02 | work-closures | Restaurant Profile Void SEO

Original source: `docs/work-closures/2026-08-02-restaurant-profile-void-seo.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `205ad4955b672e178b2af020c61fe9b032837c904698888c5da6cd10c8cbee2f`.

<!-- migrated-source: docs/work-closures/2026-08-02-restaurant-profile-void-seo.md -->
<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--restaurant-profile-void-seo"></a>
### Restaurant Profile Void SEO

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--final-status"></a>
#### Final Status

closed

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--related-work"></a>
#### Related Work

- [Central work record](#source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md)
- [Specification](#source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md)
- [Implementation plan](../implementation-plans/2026-08-02-restaurant-profiles-void-seo.md)
- [Test report](../test-reports/2026-08-02-restaurant-profile-void-seo-test-report.md)
- [Spoke update](#source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md)
- [Spoke review](#source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md)
- [Session memory](#source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md)

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--completed-scope"></a>
#### Completed Scope

Every valid public restaurant profile now renders meaningful restaurant data in raw HTML, carries one canonical URL, is sitemap-discoverable, and conditionally emits safe schema.org `Restaurant` JSON-LD. Restaurant profiles use the scoped responsive Void presentation. Member rating and favorite state remain authenticated progressive enhancement, while missing profiles remain `404` plus `noindex,nofollow`. Top Rated and Favorites were not redesigned.

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--spoke-delivery"></a>
#### Spoke Delivery

- Repository: `azurras/christopherbell.dev`
- PR: [#1345](https://github.com/azurras/christopherbell.dev/pull/1345)
- Merged SHA: `363bb986581c4d20df3434154844807ce88701e4`
- Production listener: PID `59036` after rotation from PID `55848`

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--validation"></a>
#### Validation

- Full exact-commit Gradle check passed in 3m14s.
- Alternate-port raw HTTP and browser testing passed on isolated port `8094` and isolated MongoDB data.
- Desktop, mobile, keyboard, authenticated mutation, anonymous, stale-session, sparse-data, privacy, canonical, JSON-LD, robots, sitemap, and missing-profile cases passed.
- GitHub Linux, macOS, Windows, dependency review, and CodeQL checks passed.
- Production loopback and public liveness/readiness returned 200.
- Production sitemap exposed 7,340 restaurant profile URLs.
- A real production profile returned 200 with canonical URL, `Restaurant` JSON-LD, public-only content, and versioned Void CSS/JS.
- A nonexistent production profile returned 404 with `noindex,nofollow` and no JSON-LD.
- `ChristopherBellDev`, `MongoDB`, `Cloudflared`, and `ChristopherBellMediaWorker` were all running.

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--decisions-preserved"></a>
#### Decisions Preserved

- Index all valid profiles, not a rating-selected subset.
- Use one immutable public-only page boundary.
- Render public content server-side and reserve JavaScript for personal controls.
- Omit unsafe or unavailable optional fields rather than fabricating placeholders.
- Keep profile CSS scoped to the WFL Void owner.

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

None. The elevated wrapper reported cancellation after the listener switch, but independently observed production evidence proves that the new merged behavior and versioned assets were serving successfully and all guarded health/service checks were green. No rollback occurred.

<a id="source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md--resume-boundary"></a>
#### Resume Boundary

No required work remains. If future profile behavior changes, begin from merged `main` after `363bb986581c4d20df3434154844807ce88701e4` and retain the public/private projection invariant.

<!-- /migrated-source: docs/work-closures/2026-08-02-restaurant-profile-void-seo.md -->

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md"></a>
## 2026-08-02 | work | christopherbell.dev Bootstrap Asset Regression

Original source: `docs/work/2026-08-02-christopherbell-dev-bootstrap-asset-regression.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `9d6d109731bb74eebe694832fc2779b622085315d6d3510c3f5cfcf1d0d79ddc`.

<!-- migrated-source: docs/work/2026-08-02-christopherbell-dev-bootstrap-asset-regression.md -->
<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--christopherbelldev-bootstrap-asset-regression"></a>
### christopherbell.dev Bootstrap Asset Regression

- Status: closed
- Owner/Agent: Codex primary agent
- Started: 2026-08-02

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--objective"></a>
#### Objective

Restore complete Bootstrap styling and behavior on production after the packaged
WebJar moved from 5.3.3 to 5.3.8 without matching asset-path and security updates.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--scope"></a>
#### Scope

- Align application-served Bootstrap CSS and JavaScript references with the
  packaged WebJar version.
- Align anonymous static-resource security matchers with the referenced version.
- Add regression coverage that prevents dependency/reference/allowlist drift.
- Validate locally on a non-production port, deliver through PR/CI, and verify
  production before closing the issue.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`
  and implement from refreshed `origin/main` in an isolated worktree.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--related-specs-and-plans"></a>
#### Related Specs and Plans

- Project spec: [Restore Bootstrap Assets After WebJar Version Bump](#source-docs-specs-2026-08-02-restore-bootstrap-assets-after-webjar-version-bump-md) (`complete`).
- Implementation plan: [Implement Bootstrap WebJar Asset Repair](../implementation-plans/2026-08-02-implement-bootstrap-webjar-asset-repair.md) (`complete`).
- Test report: [Bootstrap WebJar Asset Repair Test Report](../test-reports/2026-08-02-bootstrap-webjar-asset-repair-test-report.md) (`complete`).
- Source issue: [azurras/christopherbell.dev#1339](https://github.com/azurras/christopherbell.dev/issues/1339).

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--spoke-repositories"></a>
#### Spoke Repositories

- `christopherbell-dev`: authoritative checkout `A:\Projects\christopherbell.dev`;
  dirty, ahead 3, and behind current `origin/main`, so it will remain untouched.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\bootstrap-assets-1339`
  from refreshed `origin/main` commit `2b40bd860d9e4e05aa18b4dd63e13a390d41208e`.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--dispatched-tasks"></a>
#### Dispatched Tasks

No sub-agents or external tasks were dispatched.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--current-state"></a>
#### Current State

- PR [#1340](https://github.com/azurras/christopherbell.dev/pull/1340)
  squash-merged as `5bd14e994a6130a32166602a6f272581abc53525` after all CI,
  CodeQL, and dependency-review checks passed.
- Issue [#1339](https://github.com/azurras/christopherbell.dev/issues/1339)
  is closed by the merged PR.
- Production rotated from PID 33024 to PID 2956. Readiness and liveness are UP;
  Bootstrap 5.3.8 CSS and JavaScript return exact HTTP 200 responses; obsolete
  5.3.3 paths remain HTTP 403.
- Public browser checks confirm Bootstrap computed styles, the 5.3.8 bundle,
  and no console errors. ChristopherBellDev, MongoDB, and cloudflared are
  Running and Automatic.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--validation"></a>
#### Validation

- `:website:check` passed with 1,610 Java tests, 312 JavaScript tests, and 150
  Pester tests; focused security tests passed.
- Alternate-port packaged-app HTTP and browser checks passed on port 8091.
- Independent review found one matcher-test gap; the gap was fixed and the
  re-review returned no actionable findings and Ready to merge: Yes.
- Post-merge production HTTP, readiness/liveness, service, and browser checks
  passed against the automatically deployed release.

<a id="source-docs-work-2026-08-02-christopherbell-dev-bootstrap-asset-regression-md--next-steps"></a>
#### Next Steps

None. Resume only if a new Bootstrap dependency or delivery regression is
observed.

<!-- /migrated-source: docs/work/2026-08-02-christopherbell-dev-bootstrap-asset-regression.md -->

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md"></a>
## 2026-08-02 | work | christopherbell.dev OpenStreetMap Import Rename Collision

Original source: `docs/work/2026-08-02-christopherbell-dev-osm-import-rename-collision.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `fabcb4ae6e91949526ff33bed063216ca3099f63f6bd1deed0a7c938491f30c5`.

<!-- migrated-source: docs/work/2026-08-02-christopherbell-dev-osm-import-rename-collision.md -->
<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--christopherbelldev-openstreetmap-import-rename-collision"></a>
### christopherbell.dev OpenStreetMap Import Rename Collision

- Status: closed
- Owner: Codex root agent
- Started: 2026-08-02

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--objective"></a>
#### Objective

Prevent an OpenStreetMap restaurant rename from aborting the monthly or startup catch-up import when another restaurant already owns the incoming normalized name, while preserving the existing unique-name rule and useful diagnostics for genuine failures.

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--scope"></a>
#### Scope

- Diagnose the supplied production `DuplicateKeyException` against current source, upstream OpenStreetMap data, and read-only production restaurant records.
- Apply the existing same-name/different-address skip rule to ID-based rename updates before any mutation or save.
- Keep preview and apply classifications consistent.
- Add focused regression coverage and update the restaurant feature documentation.
- Validate in an isolated worktree, run the app on a non-production port with isolated test data, deliver through pull request and required CI, merge, and verify production behavior.
- Do not relax the unique `normalizedName` index, merge restaurant identities, delete restaurant records, or rewrite production data.

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--spoke-repository"></a>
#### Spoke Repository

- Repository: `azurras/christopherbell.dev`
- Registered checkout: `A:\Projects\christopherbell.dev` (dirty and stale; preserve unchanged)
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\restaurant-import-duplicate-name-20260802`
- Branch: `codex/restaurant-import-duplicate-name`
- Baseline: `origin/main` at `5bd14e994a6130a32166602a6f272581abc53525`

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--related-artifacts"></a>
#### Related Artifacts

- Project specification: [OpenStreetMap Import Rename Collision](#source-docs-specs-2026-08-02-christopherbell-dev-osm-import-rename-collision-md) (`ready-for-execution`, approved 2026-08-02).
- Implementation plan: [OpenStreetMap Import Rename Collision](../implementation-plans/2026-08-02-christopherbell-dev-osm-import-rename-collision.md) (`in-progress`; Tasks 1 and 2 complete).
- Test report: [OpenStreetMap Import Rename Collision Test Report](../test-reports/2026-08-02-openstreetmap-import-rename-collision-test-report.md) (`complete`, PASS).
- Spoke update: [OpenStreetMap Import Rename Collision Completion](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-completion-md) (`closed`).
- Spoke review: [OpenStreetMap Import Rename Collision Review](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-review-md) (no blockers or warnings).
- Session memory: [OpenStreetMap Import Rename Collision Fix](#source-docs-session-memory-2026-08-02-openstreetmap-import-rename-collision-fix-md).
- Closure record: [OpenStreetMap Import Rename Collision Closure](#source-docs-work-closures-2026-08-02-christopherbell-dev-openstreetmap-import-rename-collision-closure-md) (`closed`).

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--current-state"></a>
#### Current State

The root cause is confirmed. OpenStreetMap node `8178213204` changed from the persisted name `China Villa` to `Aama's Kitchen`, while node `13485126044` already owns normalized name `aama's kitchen` at a different location. `RestaurantService.applyPreparedImport` checks an incoming candidate by ID first and merges it without checking whether another ID owns the new normalized name. MongoDB correctly rejects the replacement through the unique `normalizedName` index, and the workflow records the entire startup catch-up run as failed.

The user approved preserving the unique-name invariant and skipping only the conflicting rename so the rest of the import can complete. Implementation commit `3fdbafc0` added preview/apply collision guards, the exact regression, and feature documentation. PR [#1341](https://github.com/azurras/christopherbell.dev/pull/1341) passed all required checks and merged as `0dd388fb096c924453bdbab8b66a3215d3e63452`. The SYSTEM auto-deployer cut over that exact release, the production catch-up succeeded, both collision records remained unchanged, and fresh current-release log searches found no recurrence.

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--validation"></a>
#### Validation

- Current upstream OpenStreetMap data returns two distinct `Aama's Kitchen` nodes in the configured Bay Area bounds: `8178213204` in Livermore and `13485126044` near Hayward.
- Read-only production MongoDB inspection confirmed `osm:node:8178213204` is persisted as `China Villa` and `osm:node:13485126044` owns normalized name `aama's kitchen`.
- Clean isolated-worktree baseline `./gradlew :website:test --no-daemon` completed successfully in 4m12s.
- Regression-first testing observed the expected RED preview mismatch, then the focused test and all 56 `RestaurantServiceTest` tests passed after the fix.
- Post-change `:website:test` passed in 2m35s and `:website:check` passed in 2m58s.
- Port 8096 readiness returned HTTP 200 `UP`; startup catch-up stored `SUCCEEDED` with fetched 2, imported 1, updated 0, and skipped existing 1; the public nearby endpoint returned HTTP 200.
- Cleanup released ports 8096 and 18996, stopped only recorded task processes, and dropped only `christopherbell_osm_collision_test_20260802`.
- GitHub Ubuntu, macOS, Windows, Dependency Review, and CodeQL checks all passed before merge.
- Production Mission Control reports application commit `0dd388fb`; catch-up status is `SUCCEEDED` with fetched 20,000, imported 296, updated 442, skipped existing 19,262, and skipped invalid 0.
- Production readiness, liveness, local/public homepage, and nearby API returned HTTP 200; required security headers were present; all four native services remained Running/Automatic.
- The two collision records retained their pre-deployment names, normalized names, addresses, and timestamps; current-release literal log searches returned no `DuplicateKeyException` or `OpenStreetMap import failed` records.

<a id="source-docs-work-2026-08-02-christopherbell-dev-osm-import-rename-collision-md--next-steps"></a>
#### Next Steps

No required action remains.

<!-- /migrated-source: docs/work/2026-08-02-christopherbell-dev-osm-import-rename-collision.md -->

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md"></a>
## 2026-08-02 | work | christopherbell.dev Restaurant Profiles Void and Search Indexing

Original source: `docs/work/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `7db73e5f478b777df5dc74b52a7041695e19a5558441c898973cf400026cea6f`.

<!-- migrated-source: docs/work/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md -->
<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--christopherbelldev-restaurant-profiles-void-and-search-indexing"></a>
### christopherbell.dev Restaurant Profiles Void and Search Indexing

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--status"></a>
#### Status

closed

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--objective"></a>
#### Objective

Render useful public restaurant profile content server-side so search engines can index every valid profile, add safe Restaurant structured data, and upgrade the profile presentation to the approved scoped Void design without exposing member-specific state.

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--owner-and-context"></a>
#### Owner and Context

- Hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `A:\Projects\christopherbell.dev`
- Requested by: direct user request on 2026-08-02
- Delivery model: approved design, durable spec and implementation-plan checkpoints, isolated spoke worktree from current `origin/main`, regression-first implementation, alternate-port raw HTTP and browser verification, PR/required CI/merge, protected production deployment, and final runtime verification

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--approved-product-decisions"></a>
#### Approved Product Decisions

- Make every valid public restaurant profile indexable.
- Render the complete public profile in Thymeleaf and use JavaScript only for signed-in personal controls.
- Keep member rating/favorite state and audit fields out of the public page model.
- Emit safe conditional `Restaurant` JSON-LD while preserving canonical, sitemap, robots, and `404`/`noindex` behavior.
- Extend the WFL Void system to restaurant profiles with a single-restaurant layout.
- Leave Top Rated and Favorites outside the visual scope.

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--related-artifacts"></a>
#### Related Artifacts

- Project specification: [Restaurant Profiles Void and Search Indexing](#source-docs-specs-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md), complete
- Implementation plan: [Restaurant Profiles Void and Search Indexing](../implementation-plans/2026-08-02-restaurant-profiles-void-seo.md), complete
- Test report: [Restaurant Profile Void SEO Test Report](../test-reports/2026-08-02-restaurant-profile-void-seo-test-report.md)
- Spoke update: [Restaurant Profile Void SEO](#source-docs-spoke-updates-2026-08-02-restaurant-profile-void-seo-md)
- Spoke review: [Restaurant Profile Void SEO Review](#source-docs-spoke-reviews-2026-08-02-restaurant-profile-void-seo-review-md)
- Closure: [Restaurant Profile Void SEO](#source-docs-work-closures-2026-08-02-restaurant-profile-void-seo-md)
- Session memory: [Restaurant Profile Void SEO](#source-docs-session-memory-2026-08-02-restaurant-profile-void-seo-md)

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--spoke-repositories"></a>
#### Spoke Repositories

- `azurras/christopherbell.dev` at `A:\Projects\christopherbell.dev`

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--current-state"></a>
#### Current State

Implementation, alternate-port acceptance, PR review, CI, merge, protected deployment, and production verification are complete. PR [#1345](https://github.com/azurras/christopherbell.dev/pull/1345) merged as `363bb986581c4d20df3434154844807ce88701e4`. Production serves the versioned Void profile assets, public canonical and Restaurant JSON-LD, sitemap discovery, and missing-profile noindex boundary on PID `59036`; required Windows services are running.

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--validation"></a>
#### Validation

Read-only exploration confirmed the current profile route, client-rendered template, progressive-enhancement opportunity, existing canonical/social-preview handling, public restaurant sitemap membership, robots behavior, and missing-profile `404`/`noindex` tests on current `origin/main`. The focused view, sitemap/robots, and JavaScript baseline passed with `BUILD SUCCESSFUL`; the implementation plan passed the Builder quality validator and execution-readiness self-review.

<a id="source-docs-work-2026-08-02-christopherbell-dev-restaurant-profiles-void-seo-md--next-steps"></a>
#### Next Steps

No required next steps. The linked closure and session memory contain the final evidence and resume boundary.

<!-- /migrated-source: docs/work/2026-08-02-christopherbell-dev-restaurant-profiles-void-seo.md -->

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md"></a>
## 2026-08-02 | work | christopherbell.dev What's for Lunch Import Location Integrity

Original source: `docs/work/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `d7b18403ba6aa340b447f523ff9ca47a63ef2474adc579ace196cf0147164735`.

<!-- migrated-source: docs/work/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md -->
<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--christopherbelldev-whats-for-lunch-import-location-integrity"></a>
### christopherbell.dev What's for Lunch Import Location Integrity

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--status"></a>
#### Status

closed

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--objective"></a>
#### Objective

Eliminate fabricated `Imported Metro, TX` restaurant locations from What's for Lunch, prevent incomplete OpenStreetMap records from entering the catalog, and remove the existing placeholder records from production safely.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--owner-and-context"></a>
#### Owner and Context

- Hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `A:\Projects\christopherbell.dev`
- Requested by: user report on 2026-08-02
- Delivery model: isolated spoke worktree refreshed from `origin/main`, alternate-port application validation, pull request and required CI, merge, protected production deployment, and runtime verification

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--related-artifacts"></a>
#### Related Artifacts

- Spec: [What's for Lunch Import Location Integrity](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md)
- Scope amendment: [What's for Lunch Legacy Location Reconciliation](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation-md)
- Implementation plan: [What's for Lunch Import Location Integrity](../implementation-plans/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md)
- Reconciliation plan: [What's for Lunch Legacy Location Reconciliation](../implementation-plans/2026-08-02-christopherbell-dev-wfl-legacy-location-reconciliation.md)
- Test report: [What's for Lunch Import Location Integrity](../test-reports/2026-08-02-wfl-import-location-integrity-test-report.md)
- Reconciliation test report: [What's for Lunch Legacy Location Reconciliation](../test-reports/2026-08-02-wfl-legacy-location-reconciliation-test-report.md)
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-location-integrity-completion-md)
- Spoke review: [Final review](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-location-integrity-review-md)
- Closure: [Work closure](#source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-location-integrity-closure-md)

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--spoke-repositories"></a>
#### Spoke Repositories

- `azurras/christopherbell.dev` at `A:\Projects\christopherbell.dev`

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--current-state"></a>
#### Current State

Closed. PR `#1342` removed the fabricated fallback and merged as `178d90caca58d2f6284f54ab2ef4514d10df2918`; its backup-gated cleanup removed 6,825 exact `Imported Metro` rows. PR `#1343` added all 393 official Census places intersecting the configured rectangles, coordinate-aware resolution, and persistence-boundary enforcement, then merged and deployed as `1d1b322dc1667e48bc0230009a3fe79fce0a1b90`.

The deployed import completed `SUCCEEDED` with 10,796 fetched, 86 imported, 136 updated, 10,574 skipped existing, and 0 skipped invalid. A fresh verified backup then preceded an exact Census manifest: 199 remaining rows were corrected and 16 rows with no incorporated-place or Census-designated-place match were deleted. The final audit contains 7,338 OSM rows, all 7,338 valid, with zero synthetic metro placeholders.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--validation"></a>
#### Validation

Both delivery phases passed regression-first focused tests, full `:website:test`, full `:website:check`, alternate-port runtime verification, required GitHub CI, exact-SHA deployment verification, MongoDB backup/restore dry runs, and production API checks. Final readiness and liveness returned HTTP 200, all four metro nearby requests returned canonical city/state/`US` values, MongoDB ping returned `ok: 1`, and PID `57904` remained the production listener.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-import-location-integrity-md--next-steps"></a>
#### Next Steps

No required follow-up remains. Refresh the pinned Census 2025 place coverage deliberately when adopting a newer Census geography vintage.

<!-- /migrated-source: docs/work/2026-08-02-christopherbell-dev-wfl-import-location-integrity.md -->

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md"></a>
## 2026-08-02 | work | christopherbell.dev What's for Lunch Rating-Weighted Void Upgrade

Original source: `docs/work/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `46c694a4498ffc7d3254ddb3208fb38194af1863ae203cad6ce27db966c28015`.

<!-- migrated-source: docs/work/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md -->
<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--christopherbelldev-whats-for-lunch-rating-weighted-void-upgrade"></a>
### christopherbell.dev What's for Lunch Rating-Weighted Void Upgrade

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--status"></a>
#### Status

closed

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--objective"></a>
#### Objective

Make every three-restaurant What's for Lunch draw rating-aware so highly rated restaurants appear more often and low-rated restaurants appear less often, while preserving randomness and discovery, and upgrade the page to the approved Void Decision Console visual direction.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--owner-and-context"></a>
#### Owner and Context

- Hub: `C:\Users\Christopher\Developer\builder`
- Spoke: `A:\Projects\christopherbell.dev`
- Requested by: direct user request on 2026-08-02
- Delivery model: approved design, durable spec and implementation plan checkpoints, isolated spoke worktree from current `origin/main`, regression-first implementation, alternate-port browser verification, PR/required CI/merge, protected production deployment, and final runtime verification

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--approved-product-decisions"></a>
#### Approved Product Decisions

- Apply rating weighting to daily picks, nearby/ZIP picks, and deleted-pick replacements.
- Treat unrated restaurants as neutral rather than penalizing new places.
- Adjust sparse ratings toward neutral so one vote cannot dominate.
- Use moderate weighting: established 5-star restaurants approach twice neutral odds; established 1-star restaurants approach roughly one-third neutral odds.
- Select three unique restaurants through weighted sampling without replacement.
- Use the approved Void **Decision Console** direction while preserving all existing WFL controls and accessibility behavior.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--related-artifacts"></a>
#### Related Artifacts

- Project specification: [Rating-Weighted Void Upgrade](#source-docs-specs-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md), approved and ready for execution
- Implementation plan: [WFL Rating-Weighted Picks and Void Decision Console](../implementation-plans/2026-08-02-wfl-rating-weighted-void-upgrade.md)
- Test report: [WFL Rating-Weighted Void Upgrade](../test-reports/2026-08-02-wfl-rating-weighted-void-upgrade-test-report.md)
- Spoke update: [Completion update](#source-docs-spoke-updates-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-completion-md)
- Spoke review: [Final review](#source-docs-spoke-reviews-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-review-md)
- Closure: [Final closure](#source-docs-work-closures-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-closure-md)
- Session memory: [WFL rating-weighted Void upgrade](#source-docs-session-memory-2026-08-02-wfl-rating-weighted-void-upgrade-md)

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--spoke-repositories"></a>
#### Spoke Repositories

- `azurras/christopherbell.dev` at `A:\Projects\christopherbell.dev`

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--current-state"></a>
#### Current State

PR [#1344](https://github.com/azurras/christopherbell.dev/pull/1344) passed the complete CI, dependency-review, and CodeQL suite, merged to `main` as `9c69623049829394f245515b8d1751c9f7579271`, auto-deployed, and passed public HTTPS and authenticated desktop/mobile verification. Production now uses the approved rating-weighted selection flows and scoped Void Decision Console.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--blockers"></a>
#### Blockers

None.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--validation"></a>
#### Validation

Regression-first focused tests, all 313 JavaScript tests, the full `:website:check` gate, alternate-port runtime, independent code review, required GitHub checks, production health/API checks, and authenticated desktop/mobile browser checks passed. The reviewer-found authenticated rating-color cascade was corrected before publication and verified at 9.06:1 contrast.

<a id="source-docs-work-2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade-md--next-steps"></a>
#### Next Steps

No required follow-up remains.

<!-- /migrated-source: docs/work/2026-08-02-christopherbell-dev-wfl-rating-weighted-void-upgrade.md -->

