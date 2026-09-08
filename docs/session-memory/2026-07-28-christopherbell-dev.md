# 2026-07-28 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/session-memory/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery.md](#source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md)
- [docs/session-memory/2026-07-28-christopherbell-dev-unified-music-hub-delivery.md](#source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md)
- [docs/session-memory/2026-07-28-christopherbell-dev-void-public-discovery-release.md](#source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md)
- [docs/session-memory/2026-07-28-music-catalog-pagination-delivery.md](#source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md)
- [docs/session-memory/2026-07-28-void-keep-alive-relaunch.md](#source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md)
- [docs/specs/2026-07-28-christopherbell-dev-music-catalog-pagination.md](#source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md)
- [docs/specs/2026-07-28-christopherbell-dev-unified-music-hub.md](#source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md)
- [docs/specs/2026-07-28-void-public-growth-program.md](#source-docs-specs-2026-07-28-void-public-growth-program-md)
- [docs/spoke-reviews/2026-07-28-christopherbell-dev-unified-music-hub.md](#source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md)
- [docs/work-closures/2026-07-28-christopherbell-dev-activitypub-discovery-foundation.md](#source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md)
- [docs/work-closures/2026-07-28-christopherbell-dev-unified-music-hub.md](#source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md)
- [docs/work/2026-07-28-website-wide-security-audit-and-remediation.md](#source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md)

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md"></a>
## 2026-07-28 | session-memory | 2026-07-28 - ChristopherBell.dev ActivityPub Discovery Foundation Delivery

Original source: `docs/session-memory/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `e584b564d429ab24a5099788ac8dfe93ab5704a5bd01cf5f41d3cb4224e015e4`.

<!-- migrated-source: docs/session-memory/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery.md -->
<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--2026-07-28---christopherbelldev-activitypub-discovery-foundation-delivery"></a>
### 2026-07-28 - ChristopherBell.dev ActivityPub Discovery Foundation Delivery

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--2329---christopherbelldev-activitypub-discovery-foundation-delivery"></a>
#### 23:29 - ChristopherBell.dev ActivityPub Discovery Foundation Delivery

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--request"></a>
##### Request

Continue autonomously from the approved Void public-growth program, commit and push completed tasks, avoid repeated approvals/review churn, and ship working software without security regressions. This turn completed Release 3 gate 1: consent-first ActivityPub discovery.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--project-context"></a>
##### Project Context

- Builder hub: `C:\Users\Christopher\Developer\builder`, branch `main`.
- Spoke: `azurras/christopherbell.dev`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\activitypub-federation`, branch `codex/activitypub-federation`, based on Release 2 SHA `f77c5f5bb644cc75cf98b27e722efdc00cd036f1`.
- The authoritative checkout at `A:\Projects\christopherbell.dev` remained untouched and may contain unrelated user state.
- Production is native Windows on port 8080 with automatic SYSTEM deployment from `origin/main`; all pre-merge runtime checks used port 8081 and a separate database.
- User approval remains durable for continuing approved work without repeated pauses. Ask only for new authority, a material scope change, or a genuine unresolved blocker.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--work-completed"></a>
##### Work Completed

PR `azurras/christopherbell.dev#1316` merged as `6cd9e397e4ec2c3175ae5c31a95f633b7a7c7c95` after three pushed task commits:

- `d7c11fa3`: added explicit nullable-safe account consent, stable per-account RSA-2048 identities, AES-256-GCM encryption with fresh nonce and account/actor/key/version AAD, conditional federation configuration, three fail-closed flags, separate protected secret validation, and migration V006.
- `50cf469a`: added read-only WebFinger, NodeInfo 2.1, Person actors, active-post outbox/ordered pages, followers/following, exact anonymous GET security matchers, uniform no-store/CORS/nosniff headers, and stable cursor limits. No HTTP client, remote persistence, delivery scheduler, or federation mutation was added.
- `45b3618b`: added authoritative federation status API, signup default-on only when enrollment is configured, disabled unavailable state, Profile opt-in/out control with server-confirmed rollback, privacy disclosure, and tests. An already-enrolled user can opt out even if new enrollment becomes unavailable.

The production default remains discovery/inbound/outbound false with no federation secret required. Messages, Music, Shared Folder, reports, and administrative data are never exposed.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--decisions"></a>
##### Decisions

- Reused `app.browser-security.public-base-url` as the sole actor origin to prevent split identities.
- Existing accounts and API clients that omit consent remain opted out. Browser default-on applies only when enrollment is operational.
- Disabling consent immediately removes discoverability but retains encrypted identity, so re-enable preserves the actor and key.
- Kept this as the discovery/metadata gate only. Full outbound/inbound work was not pulled forward.
- Used one PR and limited review effort to working behavior, interoperability, correctness, and security.
- Did not weaken protected production ACLs when `prod.cmd auto-status` was denied. Deployment was proved by listener rotation and version-specific response behavior.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--validation"></a>
##### Validation

- Full `:website:check`: BUILD SUCCESSFUL; 1,353 Java tests, zero failures/errors, three skips; complete JavaScript and sensor/package runtime checks passed.
- PR checks: Ubuntu, macOS, Windows, Dependency Review, CodeQL Java/Kotlin, JavaScript/TypeScript, and Actions all passed.
- Enabled local runtime on port 8081/database `christopherbell_activitypub_discovery_test`: opted-in signup, WebFinger/JRD, NodeInfo, actor, empty outbox/page, followers/following, headers, negative discovery, and blocked inbox POST passed.
- Restart changed PID 44916 to 46752 while actor ID, key ID, public key, WebFinger subject, and self link stayed stable.
- Authenticated toggle: status GET was authoritative; disable returned 200 and actor 404; re-enable returned 200 and restored the exact same public key.
- Disabled runtime PID 39624 started with no encryption key; root returned 200, federation discovery returned 404, and signup rendered a disabled choice.
- Cleanup: stopped only port-8081 candidate processes, dropped only the isolated database, removed test logs/scripts, and confirmed no port-8081 listener.
- Automatic production deploy rotated 8080 from PID 34768 to PID 33352. Public/local home and signup returned 200; new consent markup was present but disabled; NodeInfo/actor returned 404; core services were Running/Automatic.
- Production Mongo remained at 20 accounts, zero enabled federation accounts, zero identities, with `federation_actor_lookup` installed.
- Durable runtime evidence: `docs/test-reports/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-test-report.md` committed at Builder SHA `74f7f83`.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--current-state"></a>
##### Current State

- PR #1316 is merged and automatically deployed.
- Production is healthy and intentionally federation-disabled.
- The spoke worktree is clean. GitHub removed the remote feature branch during merge; the local worktree branch remains only as local history.
- Builder plan status is complete; the program spec records discovery foundation completion and the next gate.
- No local candidate process, isolated test database, or acceptance logs remain.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md--follow-ups"></a>
##### Follow-ups

The next approved federation gate is signed outbound delivery to a controlled peer. It must remain off in production while implementing strict SSRF/redirect defense, bounded remote actor/key fetching, HTTP signatures, retry/idempotency, payload/time limits, kill switches, and controlled-peer evidence. Only after that gate is safe should opted-in outbound production activation be considered. Inbound follows, then signed/idempotent keep-alives/replies, remain later gates.

<!-- /migrated-source: docs/session-memory/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery.md -->

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md"></a>
## 2026-07-28 | session-memory | 2026-07-28 - ChristopherBell.dev Unified Music Hub Delivery

Original source: `docs/session-memory/2026-07-28-christopherbell-dev-unified-music-hub-delivery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4b5f30f3dc0a3a8b13976624343408903f330e25c1cbeec89d83ee8c4c2606fb`.

<!-- migrated-source: docs/session-memory/2026-07-28-christopherbell-dev-unified-music-hub-delivery.md -->
<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--2026-07-28---christopherbelldev-unified-music-hub-delivery"></a>
### 2026-07-28 - ChristopherBell.dev Unified Music Hub Delivery

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--1335---implement-merge-deploy-and-verify-the-unified-music-hub"></a>
#### 13:35 - Implement, merge, deploy, and verify the unified Music hub

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--request"></a>
##### Request

Complete a first-class Music hub for `christopherbell.dev` without process churn: independent Music access, no listener downloads, shared radio/library activity, search, metadata and album-art support, persistent same-tab playback, responsive controls, denied-access logging, seven-day login continuity, automatic deployment, and strong security boundaries. Commit and push completed tasks and preserve the user's dirty production checkout.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--project-context"></a>
##### Project Context

Builder coordinated the spoke from `C:\Users\Christopher\Developer\builder`. Implementation used the isolated worktree `A:\Projects\christopherbell.dev-worktrees\unified-music-hub` on `codex/unified-music-hub`; `A:\Projects\christopherbell.dev` was not modified. Production is the native Windows host running the website, MongoDB, and Cloudflare tunnel.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--work-completed"></a>
##### Work Completed

- Added `MUSIC_READ` and `MUSIC_WRITE`, effective admin access, Back Office grants/removals, and denied-entry audit views.
- Added revocable browser sessions with seven-day idle and 30-day absolute limits while excluding background media traffic from renewal.
- Added the Music catalog, FFprobe metadata, embedded artwork, protected range streaming/transcoding, global radio/queue/history, playlists, favorites, exclusions, and search.
- Added safe writer tag/artwork edits with exact-revision conflicts, private backups, atomic replacement, audit, cleanup, and undo.
- Rebuilt `/music` as a responsive hub and kept one media element alive as the player expands on Music and compacts elsewhere.
- Added production-safe media-tool resolution from a checksum-verified protected manifest and dedicated Music mutation rate limits.
- Fixed the only CodeQL finding (case-insensitive unsafe-HTML assertion) and two cross-platform process-test assumptions before merge.
- Merged PR #1312 as `baf8910dd6707260ec02af94c13d36c1eb2d6979`; automatic deployment published that exact SHA.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--decisions"></a>
##### Decisions

- Music access stays independent of Shared Folder access; `MUSIC_READ` never authorizes downloads.
- Shared state remains global because the radio is primarily personal and the user explicitly rejected silos.
- Music metadata and paths stay behind typed server APIs.
- Review effort was limited to actionable correctness, security, and portability findings.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--validation"></a>
##### Validation

- Full local repository check passed; JavaScript reported 246 passing tests.
- Windows production suite reported 243 passed, 0 failed, and 4 expected machine/elevation skips.
- GitHub Ubuntu, macOS, Windows, dependency review, and both CodeQL language analyses passed.
- Public `/`, `/music`, access status, and versioned Music CSS passed after deployment; protected anonymous catalog/radio/stream requests returned 403.
- CSP, HSTS, and no-store headers were present.
- `ChristopherBellDev`, `MongoDB`, and `cloudflared` were Running/Automatic; one process listened on port 8080.
- An authenticated production browser was unavailable for the final smoke, so the last signed-in desktop/mobile visual pass remains observational rather than automated.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--current-state"></a>
##### Current State

- Spoke `main`: `baf8910dd6707260ec02af94c13d36c1eb2d6979` in production.
- PR #1312: merged with required checks green.
- Feature worktree: clean.
- Production checkout: unrelated dirty state preserved.
- Production services: running automatically.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md--follow-ups"></a>
##### Follow-ups

Use the live Music hub normally with a reader/writer/admin account and report any concrete playback or layout defect. No known implementation or deployment blocker remains.

<!-- /migrated-source: docs/session-memory/2026-07-28-christopherbell-dev-unified-music-hub-delivery.md -->

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md"></a>
## 2026-07-28 | session-memory | 2026-07-28 - ChristopherBell.dev Void Public Discovery Release

Original source: `docs/session-memory/2026-07-28-christopherbell-dev-void-public-discovery-release.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `9c0e57bb6e99476778d45ec82cfe57c3f13ac86f1512fdf8f7187c60548aab24`.

<!-- migrated-source: docs/session-memory/2026-07-28-christopherbell-dev-void-public-discovery-release.md -->
<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--2026-07-28---christopherbelldev-void-public-discovery-release"></a>
### 2026-07-28 - ChristopherBell.dev Void Public Discovery Release

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--2210---christopherbelldev-void-public-discovery-release"></a>
#### 22:10 - ChristopherBell.dev Void Public Discovery Release

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--request"></a>
##### Request

Complete the second of the three approved Void public-growth releases without repeated approval pauses. The release had to make discovery useful without popularity ranking, preserve media playback/navigation behavior, remain safe for anonymous readers, use one PR, commit and push after each task, pass security-focused validation, merge, deploy automatically from `main`, and receive exact-SHA production verification.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--project-context"></a>
##### Project Context

- Builder hub: `C:\Users\Christopher\Developer\builder`, branch `main`.
- Spoke: `azurras/christopherbell.dev`.
- Implementation worktree: `A:\Projects\christopherbell.dev-worktrees\void-public-discovery`, branch `codex/void-public-discovery`.
- The authoritative checkout at `A:\Projects\christopherbell.dev` had unrelated user state and was not modified.
- Production runs natively on Windows. Port 8080 is production; all pre-merge runtime checks used port 8081 and an explicitly separate Mongo database.
- The user has approved autonomous continuation through the three-release program. Ask only for genuinely new authority, a material scope change, or an unresolved external blocker.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--work-completed"></a>
##### Work Completed

Release 2 shipped through PR `azurras/christopherbell.dev#1315` and production SHA `f77c5f5bb644cc75cf98b27e722efdc00cd036f1`.

- Added normalized, deduplicated, bounded post topics and explicit root `lastExtendedOn` timestamps.
- Updated genuine revival behavior so confirmed keep-alives and replies move the timestamp while undo and unrelated actions do not.
- Added bounded, cursor-based, no-store New, Fading, Revived, Topics, topic, and People discovery APIs.
- Added privacy-aware account suggestions: signed-in overlap ranking and anonymous UTC-day rotation, excluding self, existing follows, mute, block in either direction, missing accounts, and suspended accounts.
- Added stricter fixed-window budgets for accounts younger than seven days: 10 roots, 30 replies, 60 added keep-alives, and 30 new follows per hour. Undo/unfollow and duplicate no-op mutations do not consume the add budget.
- Extended login tokens to seven days.
- Added public `/void/explore` and `/void/topic/{topic}` pages, a top-level Explore nav destination, five independently loaded panels, section-local retry/empty/load-more behavior, safe topic/person rendering, and responsive Void styling.
- Added Mongo migrations 004 and 005 with eight named indexes supporting discovery and trust exclusion queries.
- During full runtime verification, found that the two hand-written discovery `@Repository` classes were `final`, which prevented Spring exception-translation proxying. Added `VoidDiscoveryRepositoryProxyCompatibilityTest`, witnessed it fail, made both repositories proxyable, and witnessed it pass before repeating complete runtime and automated checks.
- Saved the local runtime report at `docs/test-reports/2026-07-28-christopherbell-dev-void-public-discovery-test-report.md`.
- Updated the Release 2 implementation plan to complete and advanced the program spec to Release 3.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--decisions"></a>
##### Decisions

- Kept chronological/time-based and topic-overlap ordering. Likes, keep-alives, replies, follower totals, and calculated lifespan never rank discovery.
- Kept responses `Cache-Control: no-store`, active-only, cursor-bounded, and public-safe.
- Reused the existing top-document media/navigation owner so normal Explore and topic links do not replace an active media element.
- Used one coherent release PR. GitHub rejected a merge-commit attempt under the active branch policy; the PR was merged by rebase, preserving the task commits.
- Did not weaken production ACLs when `prod.cmd status` and `auto-status` were denied. Verified automatic deployment through the public release SHA, listener rotation, service state, endpoints, and database migration/index state.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--validation"></a>
##### Validation

- Final local full check: `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-discovery'; .\gradlew.bat :website:check --no-daemon --console=plain` â€” BUILD SUCCESSFUL in 1m 36s.
- Final test evidence: 1,304 Java tests, zero failures/errors, three skipped; 265 JavaScript tests, zero failures/errors; sensor-runtime check passed.
- Isolated runtime: port 8081, PID 46824, database `christopherbell_void_discovery_20260728_01`; all six discovery APIs returned 200 and `no-store`.
- Browser runtime: five populated Explore panels, section isolation, New pagination from 12 to 24 cards, `/void/topic/music` with six cards, and desktop visual screenshot.
- Fixture safety: production documents matching `_id: /^e2e-void-/` were zero before and after; the isolated database was dropped; port 8081 was closed.
- PR checks: Ubuntu, macOS, Windows, Dependency Review, CodeQL Actions, CodeQL Java/Kotlin, and CodeQL JavaScript/TypeScript all passed.
- Automatic production deployment rotated from `7e958e737b34563d6d49a078243437d5fa9e3377` to exact SHA `f77c5f5bb644cc75cf98b27e722efdc00cd036f1` without visible prompts or UAC interaction.
- Production: local port 8080, apex `/void/explore`, and `www` `/void/explore` all returned 200; discovery New/Topics/People returned 200 and `no-store`; the live browser rendered real New/Fading/People results and correct Revived/Topics empty states.
- Production migrations 004/005 and all eight `void_*` indexes were present. `ChristopherBellDev` was Running with Java listener PID 34768 and wrapper PID 33148.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--current-state"></a>
##### Current State

- PR #1315 is merged.
- Remote `main` and production serve `f77c5f5bb644cc75cf98b27e722efdc00cd036f1`.
- The feature worktree remains registered locally; the remote feature branch deletion step could not switch the worktree to `main`, but this did not affect the merge or deployment.
- Builder `main` already contains runtime report commit `5b7a73b`; this memory/spec/plan closeout will be committed separately.
- Production port 8080 is healthy. Temporary port 8081 and the isolated test database are absent.

<a id="source-docs-session-memory-2026-07-28-christopherbell-dev-void-public-discovery-release-md--follow-ups"></a>
##### Follow-ups

Release 3, ActivityPub Federation, is the next approved release in `docs/specs/2026-07-28-void-public-growth-program.md`. It is security-sensitive and must remain staged behind separate inbound/outbound flags. Start with fresh `origin/main`, a new isolated worktree, and a concrete Release 3 implementation plan. The approved rollout gates are discovery/metadata first, outbound delivery to a controlled peer, opted-in outbound production, inbound follows, and only then signed/idempotent inbound keep-alives and replies after SSRF, replay, rate-limit, moderation, and lifespan evidence passes.

<!-- /migrated-source: docs/session-memory/2026-07-28-christopherbell-dev-void-public-discovery-release.md -->

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md"></a>
## 2026-07-28 | session-memory | 2026-07-28 Music Catalog Pagination Delivery

Original source: `docs/session-memory/2026-07-28-music-catalog-pagination-delivery.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `b5983e3e30fb48e8c7f88c381e857d6caddab67b5d56a632bca7b557cf964aeb`.

<!-- migrated-source: docs/session-memory/2026-07-28-music-catalog-pagination-delivery.md -->
<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--2026-07-28-music-catalog-pagination-delivery"></a>
### 2026-07-28 Music Catalog Pagination Delivery

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--1415---complete-music-catalog-paging-and-full-pool-radio-verification"></a>
#### 14:15 - Complete Music catalog paging and full-pool radio verification

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--request"></a>
##### Request

Fix the production Music view that exposed only 98 songs, add practical paging, and guarantee that the global radio selects from every eligible indexed song rather than the current browser page. Keep the implementation functional and secure, use one focused PR, and commit/push completed work.

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--project-context"></a>
##### Project Context

- Builder hub: `C:\Users\Christopher\Developer\builder`.
- Spoke repository: `A:\Projects\christopherbell.dev`.
- The authoritative spoke checkout was dirty and production-hosted, so implementation used the isolated worktree `A:\Projects\christopherbell.dev-worktrees\music-catalog-pagination` from refreshed `origin/main`.
- The filesystem contained 1,549 supported audio files under `A:\Shared\Music`. The existing browser catalog request was capped at 100, yielding 98 READY tracks in the visible result, while the durable radio query already requested up to 10,000 candidates.

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--work-completed"></a>
##### Work Completed

- Replaced the catalog's hidden 100-result ceiling with stable server-side pagination and true `page`, `size`, `totalTracks`, and `totalPages` metadata.
- Added bounded page/view parameters, full-query search and facets, server-side Favorites and playlist filtering, stable sorting ending in unique `id`, and stale-page clamping.
- Corrected an existing Mongo criteria-composition bug exposed by the paging tests so exact favorite and playlist filters are actually applied before count and paging.
- Added accessible numbered Previous/Next controls for desktop and mobile, abort-safe browser requests, server-filtered views, and truthful totals without changing the persistent media player.
- Preserved radio's independent `radioCandidates(10_000)` path. At production verification time, the live database contained 1,068 present READY tracks and all 1,068 were eligible radio candidates; 32 tracks had probe failures. The scheduled reconciler continues adding the remaining supported on-disk files in bounded batches.
- Committed spoke tasks as `663b4a2f` and `1564b4d1`, opened PR #1313, passed all required checks, and squash-merged to `main` as `7d7d042c26d7bbabee2cdf0bc430127a0020e65e`.
- The native SYSTEM poller automatically deployed the merge. The production listener rotated cleanly and public assets report the exact merge SHA.

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--decisions"></a>
##### Decisions

- Use numbered server-backed pages of 50 with a hard server maximum of 100, rather than transferring the full catalog to the browser.
- Apply every search, facet, Favorites, and playlist constraint before count and paging so totals and later pages remain correct.
- Keep radio independent of browser state; visible pages never constrain its candidate query.
- Retain legacy `limit` as a compatibility alias while moving the browser to `page` and `size`.
- Avoid manual/elevated deployment. The protected automatic poller performed the safe alternate-port candidate validation and cutover without Windows approval prompts.

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--validation"></a>
##### Validation

- Backend RED-to-GREEN tests plus `MusicRadioServiceTest`: 14 focused Java tests passed.
- JavaScript RED-to-GREEN suite: 252 tests passed.
- Full `:website:check`: `BUILD SUCCESSFUL in 1m 29s`.
- Candidate on port 8091: root 200, Music 200 with pagination mount, anonymous catalog 403; exact candidate process tree stopped afterward.
- PR CI: Windows, Ubuntu, macOS, Dependency Review, and all CodeQL jobs passed.
- Post-merge CI and CodeQL passed on `7d7d042c`.
- Production: `/music` 200, versioned Music JavaScript 200 with paged-catalog code, anonymous catalog 403, anonymous radio 403, all four services Running/Automatic, port 8080 listening.
- Durable evidence: `docs/test-reports/2026-07-28-music-catalog-pagination.md`.

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--current-state"></a>
##### Current State

- Production serves `7d7d042c26d7bbabee2cdf0bc430127a0020e65e`.
- PR #1313 is merged and its remote feature branch was deleted.
- The isolated spoke worktree remains available for provenance; the authoritative production checkout was not modified.
- Builder specification and implementation plan are saved, and the implementation plan is complete.

<a id="source-docs-session-memory-2026-07-28-music-catalog-pagination-delivery-md--follow-ups"></a>
##### Follow-ups

- The user should refresh the authenticated Music view and confirm that it reports the live indexed total and can navigate later pages.
- Supported files not yet indexed join the catalog and radio pool automatically in batches of up to 100 every five minutes. Probe failures remain excluded until a later successful retry.

<!-- /migrated-source: docs/session-memory/2026-07-28-music-catalog-pagination-delivery.md -->

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md"></a>
## 2026-07-28 | session-memory | 2026-07-28 Void Keep Alive Relaunch

Original source: `docs/session-memory/2026-07-28-void-keep-alive-relaunch.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `a1ceb6d41c573b8a16dedc7f77b6567a1cc2cc1561de1f0701b0652c03db4342`.

<!-- migrated-source: docs/session-memory/2026-07-28-void-keep-alive-relaunch.md -->
<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--2026-07-28-void-keep-alive-relaunch"></a>
### 2026-07-28 Void Keep Alive Relaunch

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--2056---release-1-completed-and-deployed"></a>
#### 20:56 - Release 1 completed and deployed

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--request"></a>
##### Request

Implement Release 1 of the approved three-release Void public-growth program without repeated approval stops. Make the survival proposition obvious, present the existing Like mechanic as Keep alive, remove popularity sorting, improve sharing, add safe post previews, and disclose no content for missing or expired posts. Preserve the existing expiration and authorization domain, prioritize working behavior and security, commit and push completed work, merge it, allow the automatic deployment, and verify production before starting Release 2.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--project-context"></a>
##### Project Context

- Builder hub: `C:\Users\Christopher\Developer\builder`, branch `main`.
- Spoke: `A:\Projects\christopherbell.dev`.
- The authoritative spoke checkout contained user changes and was preserved untouched.
- Implementation used isolated worktree `A:\Projects\christopherbell.dev-worktrees\void-keep-alive-relaunch` on branch `codex/void-keep-alive-relaunch` from main SHA `7d7d042c26d7bbabee2cdf0bc430127a0020e65e`.
- The Like API and post-expiration services remained compatibility and authority boundaries; only the public vocabulary and rendering changed.
- The user has approved continued execution of Releases 2 and 3 without approval checkpoints unless new authority, material scope change, or an unresolved external blocker appears.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--work-completed"></a>
##### Work Completed

- `/void` now leads with `Nothing lasts unless people care` and explains the 24-hour root, keep-alive, and reply rules in the first viewport.
- Visible Like presentation became `Keep alive · +24h` / `Kept alive`, with a quiet count, accessible effect label, and UI updates only after the server response.
- Added native Share with clipboard/prompt fallback while retaining Copy link.
- Removed the engagement-derived Active sort; Newest and Expiring Soon remain.
- Corrected thread/reply lifespan copy so the whole-thread behavior is explicit.
- Added `VoidPostSocialPreview` and its service for normalized, Unicode-bounded active-post metadata.
- Active post metadata is Thymeleaf-escaped and no-store. Missing or expired `/p/{id}` responses return a content-free no-store 404 page and catch only the domain not-found exception.
- Added JavaScript, MVC, and Java tests for keep-alive state, sharing outcomes, ordering, Unicode bounds, escaping, and vanished responses.
- Spoke commits `ba127e8d` and `ba3d2194` were pushed, PR `azurras/christopherbell.dev#1314` passed required checks, and squash merge `7e958e737b34563d6d49a078243437d5fa9e3377` reached production automatically.
- The program spec now marks Release 1 complete and Release 2 as next.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--decisions"></a>
##### Decisions

- Kept backend Like route names unchanged to avoid breaking current clients.
- Made server-returned `liked`, `likesCount`, and `expiresOn` authoritative; there is no optimistic lifespan invention.
- Used time-only ordering and did not expose an engagement-ranked replacement.
- Used the active-domain lookup before generating metadata and mapped only `ResourceNotFoundException` to the vanished page.
- Retained the existing generic 1200x630 preview image for this release.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--validation"></a>
##### Validation

- Task 1 RED: new Keep alive presentation and feed-sort imports failed before implementation. Focused JavaScript tests then passed 26 of 26 and the focused view test passed.
- Task 2 RED: preview types did not compile before implementation. Five focused Java tests passed after implementation.
- Additional RED proved active and missing post pages lacked no-store headers; both passed after controller caching was corrected.
- Final pre-merge command: `$env:GRADLE_USER_HOME='A:\Temp\gradle-void-relaunch'; .\gradlew.bat :website:check --no-daemon` -> `BUILD SUCCESSFUL in 1m 34s`.
- Local desktop/mobile browser checks found no horizontal overflow, showed the rules in the first viewport, and exposed the expected accessible Keep alive controls.
- Corrected isolated runtime on port 8081 proved account creation/login, post creation, exact 24-hour Keep alive extension, active metadata, content-free 404, and no-store headers.
- PR checks passed on Windows, Linux, and macOS, plus dependency review and all CodeQL languages.
- Post-merge CI run `30414906393` and CodeQL run `30414906457` passed.
- Production served the exact merge SHA and new Void copy. `/`, `/void`, `/messages`, `/music`, and `/back-office` returned HTTP 200; missing `/p/{id}` returned generic HTTP 404 with no-store and no identifier leak.
- Production services `ChristopherBellDev`, `ChristopherBellMediaWorker`, `cloudflared`, and `MongoDB` were Running and Automatic after deployment.
- Durable test report: `docs/test-reports/2026-07-28-void-keep-alive-relaunch.md`.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--runtime-isolation-incident-and-cleanup"></a>
##### Runtime Isolation Incident and Cleanup

The first local runtime set only `SPRING_MONGODB_URI`. Because the local profile independently fixes `spring.mongodb.database` to `christopherbell`, it created one test account, one browser session, and one post in the production database. Production verification exposed the fixture immediately.

A read-only cross-collection query found only these exact documents:

- Post `a4f8ef3a-c430-4c1d-b6ce-fc771e2a2cc9`.
- Browser session `3cd85a6c-4747-492a-ace8-7128bb97d0f0`.
- Account `2e7d40df-5a8d-47dd-be34-3c120cb75e3b` (`void_f032bef7`).

All three were deleted with exact identifiers and identifying fields. Follow-up counts were zero, and the public feed no longer contained the post. The runtime was repeated with both `SPRING_MONGODB_URI=mongodb://127.0.0.1:27017` and `SPRING_MONGODB_DATABASE=christopherbell_void_relaunch_test`; corrected fixture IDs existed only in the isolated database and had zero matches in production. Future local verification must set both properties.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--closure-readiness"></a>
##### Closure Readiness

ready

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--closure-text"></a>
##### Closure Text

Release 1 of the user-approved Void public-growth program is complete. PR #1314 merged as `7e958e737b34563d6d49a078243437d5fa9e3377` after Windows, Linux, macOS, dependency-review, and CodeQL checks passed. Full local verification and a corrected isolated runtime proved the Keep alive, sharing, ordering, preview, and vanished-post contracts. The automatic deployment reached the exact merge SHA, production smoke checks passed, and the temporary test-data isolation incident was fully remediated and documented. There was no separate source GitHub issue and no GitHub comments or attachments were used as closure instructions. Continue with Release 2 - Public Discovery under the approved program spec.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--current-state"></a>
##### Current State

- Spoke PR: merged.
- Production: merge `7e958e737b34563d6d49a078243437d5fa9e3377` live.
- Local corrected candidate: stopped; port 8081 closed.
- Production services: healthy.
- Isolated worktree retained for PR provenance; the authoritative dirty spoke checkout remains untouched.
- Builder plan `docs/implementation-plans/2026-07-28-christopherbell-dev-void-keep-alive-relaunch.md`: complete.
- Program spec `docs/specs/2026-07-28-void-public-growth-program.md`: still ready for execution because Releases 2 and 3 remain.

<a id="source-docs-session-memory-2026-07-28-void-keep-alive-relaunch-md--follow-ups"></a>
##### Follow-ups

- Begin Release 2 with a focused implementation plan for Public Discovery.
- Preserve non-popularity ordering and the explicit `lastExtendedOn` semantics from the approved spec.
- Always override both Mongo URI and database for future local candidate runtimes.
- One brief HTTP 502 occurred during the expected production listener rotation; the target release then served HTTP 200. Treat zero-downtime deployment as separate scope if desired.

<!-- /migrated-source: docs/session-memory/2026-07-28-void-keep-alive-relaunch.md -->

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md"></a>
## 2026-07-28 | specs | ChristopherBell.dev Music Catalog Pagination

Original source: `docs/specs/2026-07-28-christopherbell-dev-music-catalog-pagination.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `cc6d8d9421e656295c05fe5b0488418577c56035cca00e61e81fcaff54c413b1`.

<!-- migrated-source: docs/specs/2026-07-28-christopherbell-dev-music-catalog-pagination.md -->
<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--christopherbelldev-music-catalog-pagination"></a>
### ChristopherBell.dev Music Catalog Pagination

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--document-status"></a>
#### Document Status

ready-for-execution

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--purpose"></a>
#### Purpose

Remove the hidden 100-track Music catalog ceiling and let listeners browse every indexed track through explicit, stable server-backed pages without changing the global radio candidate pool.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--background"></a>
#### Background

Production contains 1,549 files with supported audio extensions below `A:\Shared\Music`, while the Music catalog request defaults to 100 results and clamps every request to at most 100. The current browser renders only that response and therefore reports 98 ready tracks rather than the full indexed-library count. Favorites and playlists are also filtered from only the loaded response.

The radio uses a separate `radioCandidates(10_000)` query over all present, ready, non-excluded tracks. Catalog page state must never narrow or replace that radio query.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--goals"></a>
#### Goals

- Return a real total for the full filtered catalog.
- Display 50 tracks per numbered page with Previous, Next, and nearby page controls.
- Apply text search and artist, album, and genre filters before counting and paging.
- Keep ordering stable across page requests by adding a unique final sort key.
- Page Favorites and playlist contents rather than filtering only the current All Music page.
- Preserve radio selection from every eligible indexed track, independent of the visible page.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--non-goals"></a>
#### Non-Goals

- No infinite scrolling or client-side download of the entire catalog.
- No change to playback, download authorization, metadata editing, queue semantics, radio weighting, or the 10,000-track radio safety bound.
- No pagination requirement for the bounded radio-history panel.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--requirements"></a>
#### Requirements

- Catalog requests accept zero-based `page` and bounded `size`; the UI uses size 50.
- Invalid negative pages or out-of-range sizes are normalized or rejected consistently at the typed query boundary.
- Catalog responses include `page`, `size`, `totalTracks`, and `totalPages` alongside tracks and facets.
- The default request returns page zero, not a silent unlabelled subset.
- Search/filter changes reset to page zero.
- Moving pages preserves active text and facet filters and does not restart or replace the persistent media player.
- Facet options describe the full applicable result set rather than only the visible page.
- The current page is clamped to the last available page when mutations reduce the result count.
- Page controls are keyboard accessible, indicate the active page, and remain usable on mobile.
- Protected catalog authorization and no-store response headers remain unchanged.
- Radio continues querying the complete eligible catalog through `radioCandidates(10_000)` and never receives UI page, size, search, facet, favorite, or playlist constraints.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--proposed-approach"></a>
#### Proposed Approach

Use server-backed numbered pagination. Extend the typed Music query/result and catalog API with bounded page metadata, count the complete criteria, then fetch one stable sorted page. Use the same catalog paging boundary for All Music and Favorites. Resolve a selected global playlist to its bounded track-ID set before catalog paging so playlist pages remain complete without exposing paths or downloading the whole catalog.

The browser owns only current query/view/page state. It requests one page at a time, validates all pagination metadata, renders the true result total, and shows a compact window of page buttons. History remains a separate bounded view. Radio remains server-owned and independent.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--options-considered"></a>
#### Options Considered

- Server-backed numbered pages: selected because it provides totals, direct navigation, bounded responses, and predictable mobile behavior.
- Load all tracks and paginate in JavaScript: rejected because response and browser work grow with the entire library.
- Cursor-based infinite loading: rejected because it does not match the requested paging model and makes direct page navigation and total-page display less clear.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--files-or-modules-involved"></a>
#### Files or Modules Involved

- Music catalog query/result/service and read controller/view models.
- Music library playlist lookup boundary where playlist IDs are resolved.
- Music API URL builder, response validator, page state/rendering, template, and responsive styles.
- Java and JavaScript catalog/pagination/radio regression tests.
- Music package and frontend documentation.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--validation-plan"></a>
#### Validation Plan

- RED test proves a 1,549-track match reports the full total while returning only the requested 50-track page.
- Tests cover first, middle, final, empty, excessive, and negative page inputs; stable tie ordering; full-result facets; favorite and playlist paging; and search reset.
- JavaScript tests cover response validation, compact page windows, disabled boundary controls, current-page indication, mobile-safe markup, and preserved filter parameters.
- A radio regression verifies a paged catalog request cannot affect the separate 10,000-candidate query.
- Run focused Java and JavaScript tests, then the full website check and a non-8080 runtime request against the paged endpoint.
- Publish one focused PR, require platform CI, dependency review, and CodeQL, merge, allow automatic deployment, and verify the production total/pages plus radio playback.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--acceptance-criteria"></a>
#### Acceptance Criteria

- All Music reports the full indexed match count rather than 98 or an unlabelled 100-result cap.
- Fifty or fewer tracks render per page, with correct navigation through every page.
- Search, facets, Favorites, and playlists return complete paged results.
- Navigating catalog pages does not interrupt active media.
- Radio remains eligible to select any of the approximately 1,500 present, ready, non-excluded tracks, regardless of the page visible to a listener.
- Authorization, inline-only playback, security headers, CI, and production smoke checks pass.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-music-catalog-pagination-md--open-questions"></a>
#### Open Questions

None. The user approved numbered server paging and explicitly required radio to remain full-library.

<!-- /migrated-source: docs/specs/2026-07-28-christopherbell-dev-music-catalog-pagination.md -->

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md"></a>
## 2026-07-28 | specs | christopherbell.dev Unified Music Hub

Original source: `docs/specs/2026-07-28-christopherbell-dev-unified-music-hub.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `c00bf16c21dcddf200aa63135cc280284b1518cda969483166ba21a65220eacd`.

<!-- migrated-source: docs/specs/2026-07-28-christopherbell-dev-unified-music-hub.md -->
<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--christopherbelldev-unified-music-hub"></a>
### christopherbell.dev Unified Music Hub

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--document-status"></a>
#### Document Status

Ready for review.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--purpose"></a>
#### Purpose

Build one native Music Hub for `christopherbell.dev` that turns audio below
`A:\Shared\Music` into a fast, indexed library with a shared smart radio,
playlists, a shared queue, listening history, direct metadata editing, and
seamless site-wide playback.

The Music Hub must remain part of the existing website rather than introducing
Jellyfin, Navidrome, or another service and authentication silo.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--background"></a>
#### Background

The website already exposes an authenticated Shared Folder, a persistent
site-wide media player, and one shared radio timeline. The current file browser
is useful for raw storage operations but is not an album-, artist-, or
playlist-oriented music library. Radio selection has limited preference data,
and audio metadata is primarily discovered by the browser while playing a file.

The desired result is a dedicated `/music` experience with its own permissions.
It should be the main place for listening and managing music while Shared Folder
remains the raw file-management and download surface.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--goals"></a>
#### Goals

- Provide one cohesive Music Hub for library browsing, playlists, queue, radio,
  history, favorites, exclusions, metadata repair, and playback.
- Keep one server-owned shared radio timeline and one shared administrative
  queue rather than per-user stations.
- Keep active music playing without interruption while navigating anywhere in
  the same browser tab.
- Introduce independent `MUSIC_READ` and `MUSIC_WRITE` capabilities.
- Allow safe, reversible edits to metadata embedded in the original media file.
- Make Music visible in the main navigation while auditing denied access.
- Extend normal browser login usability with a bounded, revocable session model.
- Preserve production safety on the Windows host and avoid background work with
  unbounded CPU, memory, process, storage, or database cost.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--non-goals"></a>
#### Non-Goals

- Do not introduce a separate media server, user database, or embedded third-
  party media interface.
- Do not create personal radio stations, personal playlist silos, or per-user
  copies of the music catalog.
- Do not grant music downloads through `MUSIC_READ` or `MUSIC_WRITE`.
- Do not make metadata editing available for formats that cannot be rewritten
  and validated without re-encoding audio.
- Do not promise uninterrupted audible playback across a browser refresh when
  browser autoplay policy requires a new user gesture.
- Do not change explicit API bearer-token lifetime or renewal behavior as part
  of the browser-session work.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--authorization-model"></a>
#### Authorization Model

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--capabilities"></a>
##### Capabilities

- `MUSIC_READ` grants access to `/music`, catalog browsing and search, audio
  streaming, manual playback, shared-radio listening, playlists, queue state,
  and history. It never grants a download.
- `MUSIC_WRITE` implies `MUSIC_READ`. It permits shared playlist changes, queue
  changes, favorites, radio exclusions, metadata and artwork edits, backup
  restoration, and other Music Hub management actions. It does not grant a
  download.
- `SHARED_FOLDER_READ` and `SHARED_FOLDER_WRITE` remain independent. They do not
  imply either Music capability, and Music capabilities do not imply either
  Shared Folder capability.
- A user who has both `MUSIC_READ` and `SHARED_FOLDER_READ` may still download a
  music file through the Shared Folder because the broader Shared Folder grant
  is additive.
- `ADMIN` has effective `MUSIC_READ` and `MUSIC_WRITE` by default.
- Removing `MUSIC_READ` from an account also removes `MUSIC_WRITE`.
- Back Office allows admins to grant and revoke both Music capabilities.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--enforcement"></a>
##### Enforcement

Every catalog, stream, radio, playlist, queue, preference, history, artwork,
metadata-edit, and restore boundary must enforce the relevant Music capability
server-side. Hiding a button is not authorization. Music streaming must use a
Music-specific content boundary that cannot be converted into an attachment or
download by changing query parameters or headers.

Existing Shared Folder endpoints keep their current authorization contract.
Possessing a Shared Folder capability does not unlock `/music` without an
explicit `MUSIC_READ` grant.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--navigation-and-denied-access"></a>
#### Navigation and Denied Access

- Music is a top-level navigation item visible to anonymous and authenticated
  visitors.
- An anonymous `/music` request renders a polished sign-in/access-required page.
- An authenticated account without `MUSIC_READ` renders a polished access-
  denied page.
- Access-denied rendering must not disclose catalog contents, paths, artwork,
  station state, account data, or authorization internals.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--music-access-audit"></a>
##### Music Access Audit

Back Office includes an admin-only Music Access page with bounded filtering by:

- date range;
- allowed or denied outcome;
- authenticated or anonymous actor;
- account identity; and
- trusted client IP.

Logged-in denied attempts record the durable account identity. Anonymous denied
attempts record the client IP only after the existing trusted-proxy resolution
boundary has rejected spoofable forwarding data. Repeated attempts by the same
actor and route are aggregated within a short bounded window and retain an
attempt count, first occurrence, and latest occurrence rather than creating an
unbounded row per request.

Anonymous IP records expire after 30 days. Expiration is server-enforced and
covered by cleanup tests. Audit persistence failure never grants access; a
request that should be denied remains denied.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--music-catalog"></a>
#### Music Catalog

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--source-and-identity"></a>
##### Source and identity

The catalog indexes ordinary audio files recursively below `A:\Shared\Music`.
Each catalog record is bound to the existing stable file observation identity
and source revision so stale metadata cannot authorize or overwrite a changed
file.

Expected catalog fields include:

- safe relative path and display filename;
- title, artist, album artist, album, track number, disc number, genre, and year;
- duration and audio/container format information;
- embedded artwork identity and bounded thumbnail references;
- file size, modified time, stable observation token, and catalog status; and
- extraction or edit problems safe for administrative display.

Missing metadata uses deterministic filename and folder fallbacks without
inventing embedded values.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--index-maintenance"></a>
##### Index maintenance

- Shared Folder uploads, moves, restores, metadata edits, and deletes notify the
  catalog immediately after the visible filesystem transition succeeds.
- A bounded incremental reconciliation detects files changed directly on the
  drive.
- Unchanged revisions are not reopened, rehashed, or re-probed.
- Probe concurrency, process lifetime, output size, artwork size, and scan work
  per cycle are bounded.
- Removed files leave active results promptly. Missing or failed files do not
  stop the rest of the catalog from serving.

MongoDB is the browsing index, not the media source. Streaming always rechecks
the current filesystem revision at the existing safe read boundary.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--music-hub-interface"></a>
#### Music Hub Interface

`/music` opens on a unified Listen dashboard containing:

- current shared-radio artwork, title, artist, album, elapsed time, and status;
- a prominent Listen Live action;
- the upcoming shared queue;
- recently played tracks; and
- quick access to favorites and playlists.

Primary sections are:

- **Library**: Albums by default, with Artists, Songs, Genres, and Folders as
  alternate views.
- **Playlists**: shared playlists managed by `MUSIC_WRITE` holders.
- **Queue**: the current shared queue with reorder and removal controls for
  `MUSIC_WRITE` holders.
- **History**: searchable shared-radio and playback history.
- **Manage**: writer-only metadata problems, excluded tracks, failed files,
  edits, private backups, and undo controls.

Search remains visible while navigating and matches title, artist, album,
genre, playlist, and safe relative path. Mobile selection opens the chosen
album or track near the top of the viewport rather than below a long result
list. Writer actions use compact overflow menus on small screens.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--persistent-playback-handoff"></a>
#### Persistent Playback Handoff

The existing persistent media session remains the single owner of the live
audio element in a browser tab.

- While the user is on `/music`, the compact bottom player is hidden and the
  Music Hub renders a full player bound to the same live session.
- Navigating away collapses the full player into the bottom bar without
  replacing the audio element, changing the source, seeking, pausing, or losing
  buffer, volume, queue, or radio state.
- Returning to `/music` hides the bottom bar and reconnects the expanded player
  to the same live session without restarting playback.
- The handoff remains same-tab only.
- A true page refresh restores the saved source and position. Audible autoplay
  after refresh remains subject to browser policy and may require a tap.

The expanded and compact players are control surfaces over one playback owner,
not two synchronized media elements.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--shared-smart-radio-and-queue"></a>
#### Shared Smart Radio and Queue

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--station-ownership"></a>
##### Station ownership

The server owns one durable station timeline. It advances independently of
listeners by using durations extracted into the server-side catalog. Joining a
station must return the elapsed point on the current timeline rather than start
a new track for that listener.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--smart-rotation"></a>
##### Smart rotation

Eligible selection must:

- reject every radio-excluded track;
- give favorites a strong but bounded weight;
- enforce separate recent-track and recent-artist cooldowns;
- prefer eligible music that has gone longest without being heard;
- retain an occasional random eligible selection; and
- avoid immediate repetition whenever another eligible track exists.

Selection remains deterministic under injected time and randomness for tests.
One shared history event is recorded per station transition, not per connected
listener.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--queue-behavior"></a>
##### Queue behavior

`MUSIC_WRITE` holders may Play Next, Add to Queue, reorder, or remove queued
tracks. Queue items override smart selection for everyone in their explicit
order. Smart rotation resumes automatically when the queue becomes empty.

Missing, changed, unreadable, unsupported, or failed queued tracks are skipped
and recorded for writer review instead of stopping the station. Queue mutation
uses revision and concurrency controls so simultaneous writers cannot silently
overwrite each other.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--preferences-playlists-and-history"></a>
#### Preferences, Playlists, and History

- A favorite is a shared positive signal that increases but does not guarantee
  radio selection.
- Exclude from Radio is a shared hard rule.
- There are no star ratings or per-user recommendation profiles.
- Playlists are shared and writable only with `MUSIC_WRITE`.
- Readers may browse and play playlists but cannot mutate them.
- Radio history is shared and ordered by server transition time.
- Manual playback history must be bounded and must not create one database write
  per media progress event.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--direct-metadata-editing"></a>
#### Direct Metadata Editing

`MUSIC_WRITE` holders may edit title, artist, album artist, album, track and disc
numbers, genre, year, and embedded artwork for supported formats.

Each edit must:

1. authorize `MUSIC_WRITE` and validate CSRF for browser mutations;
2. recheck the exact visible file revision;
3. create a checksum-bound original backup in private storage with a 30-day
   expiration;
4. copy or open the source through the existing safe filesystem boundary;
5. rewrite metadata in private staging without re-encoding the audio stream;
6. probe the staged output and verify container, audio codec/stream, duration,
   requested tags, and bounded artwork;
7. atomically replace the visible source only if its revision is still current;
8. refresh the catalog after the replacement succeeds; and
9. record success or a safe failure in the administrative audit history.

Unsupported formats remain playable and show read-only metadata controls. A
failed edit leaves the visible source untouched.

Undo is `MUSIC_WRITE`-only and revision-checked. It restores a selected private
backup without overwriting a file changed after the corresponding edit. Restore
must itself use staged validation and an atomic visible transition. Backup
expiration is audited and must not follow links or cross the private backup
root.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--browser-session-lifetime"></a>
#### Browser Session Lifetime

The longer lifetime applies only to normal browser-cookie sessions. Explicit
API bearer-token behavior remains unchanged.

- Browser sessions have a seven-day inactivity timeout.
- Browser sessions have a 30-day absolute lifetime from authentication.
- Eligible interactive browser activity may rotate and extend the cookie up to
  the absolute deadline.
- Media streaming, range requests, radio polling, background API refreshes,
  health checks, static assets, and other non-interactive traffic never refresh
  session activity or lifetime.
- Tokens rotate through a server-tracked session identity. Old rotated tokens
  receive a bounded overlap only when necessary for concurrent browser requests
  and then become invalid.
- Logout, password reset, account suspension, account deletion, and sensitive
  role or permission changes revoke affected browser sessions immediately.
- Cookies remain Secure, HttpOnly, SameSite-protected, path-scoped as
  appropriate, and absent from URLs, response bodies, and logs.
- Session creation, renewal, revocation, expiration, and invalid reuse produce
  safe security audit events without logging token material.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--resource-and-failure-boundaries"></a>
#### Resource and Failure Boundaries

- Catalog scans, media probes, tag-edit jobs, thumbnails, queue/history growth,
  access audit growth, backups, and cleanup work all have explicit bounds.
- Full embedded artwork is not repeatedly loaded for list views; bounded cached
  thumbnails serve browsing surfaces.
- Media tools run only through the existing pinned, restricted worker boundary,
  never from request parameters or an unrestricted website process.
- Failure to read one file cannot make the whole library unavailable.
- Failure to persist a preference or queue mutation is visible to the writer and
  never reported as success.
- Session-store failure requires reauthentication rather than silently
  extending access.
- Access-audit failure never changes an authorization decision.
- Absolute filesystem paths, private backup paths, worker commands, token
  material, and internal exception details never reach browser responses.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--expected-ownership-areas"></a>
#### Expected Ownership Areas

Implementation is expected to touch focused ownership areas in the
`christopherbell.dev` spoke repository, including:

- account permissions, effective authority evaluation, browser session
  issuance/revocation, and Back Office account management;
- shared-folder safe read/mutation boundaries and media worker contracts;
- a new focused music catalog/radio/playlist/queue/history/editing package;
- Music and Back Office controllers, request/response models, and repositories;
- main navigation and `/music` templates;
- the persistent site media player, expanded Music player, Music page modules,
  and responsive CSS;
- production worker/install configuration and bounded cleanup tasks; and
- package documentation, operations guidance, migrations, and tests.

Exact files and literal line ranges belong in the reviewed implementation plan
after inspecting refreshed `origin/main`.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--validation-plan"></a>
#### Validation Plan

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--automated-behavior"></a>
##### Automated behavior

- Test every effective combination of `MUSIC_READ`, `MUSIC_WRITE`,
  `SHARED_FOLDER_READ`, `SHARED_FOLDER_WRITE`, role hierarchy, revocation, and
  admin defaults.
- Prove music-only readers can stream but cannot download through alternate
  routes, headers, ranges, content dispositions, or endpoint substitution.
- Test anonymous and authenticated denied-access rendering and auditing,
  trusted-proxy IP resolution, spoofed forwarding rejection, aggregation,
  Back Office filtering, bounds, authorization, and 30-day expiration.
- Test incremental indexing, file revision changes, stale rows, missing tags,
  unsupported files, probe failures, artwork bounds, and direct-drive changes.
- Test smart selection weights and hard rules with injected clock and randomness,
  listener-free advancement, queue precedence, history uniqueness, concurrent
  mutation, restart recovery, and missing queued tracks.
- Test tag edits against representative supported media fixtures, including
  concurrent source changes, worker failure, invalid output, atomic replacement,
  undo, expiration, and unchanged audio-stream evidence.
- Test seven-day idle expiration, 30-day absolute expiration, rotation overlap,
  non-interactive request exclusion, logout, password reset, suspension,
  deletion, permission-change revocation, and unchanged API bearer behavior.
- Test the compact/expanded player as two views over one media element and prove
  no pause, source reload, seek, or state loss across repeated navigation.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--runtime-acceptance"></a>
##### Runtime acceptance

- Run the complete Java and browser test suites and all shared-folder worker and
  operations checks required by the repository.
- Validate on a non-8080 port on the Windows production host with isolated test
  data and the production-compatible profile.
- Exercise desktop and mobile Music Hub navigation, library search, radio,
  queue, playlists, tag editing, undo, Back Office access logs, permission
  changes, and session renewal/expiration flows.
- Verify continuous playback while navigating between `/music`, public pages,
  Shared Folder, Messages, Tools, and Back Office.
- Publish through a reviewed PR, require platform CI, Dependency Review, and
  CodeQL success, merge to `main`, and let the automatic production pipeline
  deploy.
- Confirm the deployed release SHA, root route, liveness, readiness, authorized
  Music behavior, denied Music behavior, and unchanged Shared Folder behavior.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--acceptance-criteria"></a>
#### Acceptance Criteria

- Music is visible in the main navigation to everyone.
- Only accounts with effective `MUSIC_READ` can enter or stream from the Music
  Hub.
- `MUSIC_READ` and `MUSIC_WRITE` alone cannot download music.
- `MUSIC_WRITE` implies `MUSIC_READ`; admins receive both; Shared Folder
  capabilities remain independent.
- Back Office can grant/revoke Music capabilities and inspect bounded Music
  access logs.
- Anonymous denied attempts retain trusted IP evidence for no more than 30 days.
- `/music` provides the approved Library, Playlists, Queue, History, Manage, and
  expanded-player experience on desktop and mobile.
- Audio continues through same-tab site navigation with an uninterrupted
  compact-to-expanded player handoff.
- One shared smart station advances without listeners, respects favorites,
  exclusions, cooldowns, randomness, queue overrides, and missing-file handling.
- Direct metadata edits preserve audio, create 30-day undo backups, validate
  staged output, replace atomically, and never overwrite a changed source.
- Browser sessions honor seven-day inactivity and 30-day absolute limits without
  renewal from media/background traffic; revocation events take effect
  immediately.
- All required automated, alternate-port, CI, deployment, and production smoke
  evidence passes before completion is claimed.

<a id="source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md--open-questions"></a>
#### Open Questions

None. Product and security decisions required for implementation planning are
resolved in this specification.

<!-- /migrated-source: docs/specs/2026-07-28-christopherbell-dev-unified-music-hub.md -->

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md"></a>
## 2026-07-28 | specs | Void Public Growth Program

Original source: `docs/specs/2026-07-28-void-public-growth-program.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `6e7c2583ac382b4923e986c9088edf7cc973076a26df5f5966b49f13426cffc6`.

<!-- migrated-source: docs/specs/2026-07-28-void-public-growth-program.md -->
<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--void-public-growth-program"></a>
### Void Public Growth Program

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--document-status"></a>
#### Document Status

ready-for-execution

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--purpose"></a>
#### Purpose

Turn Void into the public reason to visit and join `christopherbell.dev`: a chronological, low-pressure social network where every post begins with a limited lifespan and the community decides what survives.

The program will ship as three production releases:

1. Relaunch Void around its existing survival mechanic.
2. Add public discovery without popularity ranking.
3. Connect opted-in accounts to the wider social web through ActivityPub.

Each release must be complete, secure, deployed, and production-verified before implementation begins on the next release.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--background"></a>
#### Background

Void already provides the essential product foundation:

- Anonymous users can read the public feed, profiles, threads, and individual post pages.
- Anyone can create an account and authenticated users can post, reply, follow, and like.
- A root thread begins with a 24-hour lifespan.
- Each keep-alive interaction and each reply adds 24 hours to the entire thread.
- Removing a keep-alive removes its 24-hour extension.
- Replies inherit the root thread expiration.
- The browser already renders a live lifespan countdown and removes expired posts.
- Public post routes are shareable, but their social metadata is generic.
- The feed includes a popularity-derived `Active` sort, which conflicts with the approved no-popularity-ranking identity.

The growth problem is not a lack of unrelated features. Void needs a memorable public proposition, a way for strangers to discover active conversations, and distribution beyond the existing site.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--product-identity"></a>
#### Product Identity

Void's public proposition is:

> Nothing lasts unless people care. Every post begins with 24 hours. Keep it alive or let it disappear.

The experience has four permanent principles:

- The primary feed is chronological, not algorithmically ranked.
- Public popularity scores never determine ordering or recommendation.
- A keep-alive is functional: it adds 24 hours to the thread.
- A reply is participation and therefore also adds 24 hours to the thread.

The public feed may show a quiet keep-alive count because it explains the remaining lifespan. The count must not become a leaderboard or ranking input.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--goals"></a>
#### Goals

- Give a first-time visitor a clear explanation of Void within one screen.
- Make the survival mechanic visible, understandable, and satisfying to use.
- Keep public reading open and account creation immediate.
- Give every active thread an attractive, meaningful share experience.
- Help strangers find new, fading, revived, and topic-relevant conversations.
- Recommend people through shared interests rather than follower or like totals.
- Allow opted-in Void accounts to participate in the ActivityPub network.
- Preserve temporary local content semantics and clearly disclose federation limits.
- Add proportionate abuse, moderation, privacy, and operational controls before increasing reach.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--non-goals"></a>
#### Non-Goals

- No engagement-ranked or personalized infinite-scroll algorithm.
- No advertising, monetization, premium tiers, or creator payouts.
- No public leaderboards for likes, keep-alives, followers, or post survival.
- No guarantee that a federated remote server deletes its cached copy of expired content.
- No federation of private messages, Music, Shared Folder content, administrative data, or private account information.
- No simultaneous implementation of all three releases.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-sequence"></a>
#### Release Sequence

Release status as of July 29, 2026:

- Release 1 - Keep Alive Relaunch: complete and production-verified at merge `7e958e737b34563d6d49a078243437d5fa9e3377` through PR `azurras/christopherbell.dev#1314`.
- Release 2 - Public Discovery: complete and production-verified at merge `f77c5f5bb644cc75cf98b27e722efdc00cd036f1` through PR `azurras/christopherbell.dev#1315`.
- Release 3 - ActivityPub Federation: discovery foundation, controlled-peer outbound delivery, and production read-only discovery activation are complete and production-verified through PRs `azurras/christopherbell.dev#1316`, `#1317`, and `#1318`, latest merge `8405cd77d0f1743fe33d70cc80b47e37048090a0`. Discovery is live; inbound and outbound remain disabled until their separate controlled interoperability gates pass.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-1-keep-alive-relaunch"></a>
##### Release 1: Keep Alive Relaunch

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--public-experience"></a>
###### Public experience

The `/void` hero must state the survival proposition and explain three rules:

1. Every thread starts with 24 hours.
2. Each keep-alive adds 24 hours.
3. Each reply adds 24 hours to the whole thread.

Anonymous visitors continue to read without an account. The composer prompt must offer immediate signup or login and preserve the exact feed, thread, or post destination across authentication.

The existing Like action becomes **Keep alive · +24h**. After the current user acts, its selected state becomes **Kept alive**. The quiet numeric count remains visible. The control must retain an accessible name that explains the 24-hour effect.

Each active root post and reply context must show the server-derived live countdown. A confirmed keep-alive produces a restrained `+24h` visual update; the UI must not extend time optimistically before the server response. Undoing a keep-alive restores the unselected state and server-derived expiration.

Reply composers must explain that a successful reply adds 24 hours to the entire thread. After a confirmed reply, the root and every visible reply must display the updated shared expiration.

Every post retains Copy link and gains a native Share action when `navigator.share` is available. The fallback copies the canonical post URL.

The popularity-derived `Active` sort is removed. Release 1 retains newest-first and expiring-soon ordering. Recently revived ordering belongs to Release 2 and must use extension time rather than totals.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--public-post-previews-and-expiration"></a>
###### Public post previews and expiration

An active `/p/{postId}` response must provide server-rendered, escaped social metadata containing:

- The author's public username.
- A bounded plain-text excerpt.
- The canonical post URL.
- A recognizable 1200x630 Void preview image.
- A concise explanation that the thread is temporary.

The preview must never include raw HTML, secrets, private profile data, or content from an expired thread. An expired or missing public post renders a deliberate `This post vanished into the Void` state with a route back to `/void`; it must not expose deleted content through metadata, APIs, caches, or logs.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--server-and-compatibility"></a>
###### Server and compatibility

The current 24-hour base and extension calculations remain authoritative and unchanged. Existing Like API routes may remain as compatibility boundaries, while new UI and documentation use Keep alive terminology. A future versioned API may rename the action without breaking current clients.

Failure behavior:

- Anonymous interaction redirects to login and preserves the intended return URL.
- A rejected, rate-limited, or failed keep-alive leaves the prior rendered state intact and shows an actionable message.
- A thread that expires during interaction returns the existing not-found domain result and disappears cleanly.
- Malformed or absent expiration data fails closed to server repair behavior; the browser does not invent a lifespan.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-1-acceptance-criteria"></a>
###### Release 1 acceptance criteria

- A first-time anonymous visitor can explain the 24-hour survival mechanic from `/void` without interacting.
- Active threads show a ticking countdown and quiet keep-alive count.
- Keep alive adds exactly 24 hours after server confirmation; undo removes that extension.
- A reply adds exactly 24 hours to the root and all descendants.
- No feed option ranks by keep-alive or reply totals.
- Shared active posts have meaningful escaped metadata; expired posts disclose no original content.
- Public reading, signup, login return paths, reporting, deletion, following, and existing thread navigation continue working.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-2-public-discovery"></a>
##### Release 2: Public Discovery

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--explore-surface"></a>
###### Explore surface

Add a public `/void/explore` page composed of independently loaded, failure-isolated sections:

- **New arrivals:** active root posts ordered by creation time descending.
- **Fading soon:** active root posts ordered by expiration ascending.
- **Recently revived:** active root posts ordered by the most recent confirmed lifespan extension.
- **Topics:** active hashtags ordered by recent active-post or extension time, never total likes.

Each section uses bounded cursor pagination with stable unique tie ordering. A failed section must not prevent other sections from rendering. Empty sections explain their selection rule.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--revival-state"></a>
###### Revival state

Add a dedicated nullable `lastExtendedOn` timestamp to root threads. It changes only when a confirmed keep-alive or reply adds lifespan. Editing, viewing, sharing, following, and notification delivery must not update it.

Undoing a keep-alive recalculates the expiration but does not create a new revival event. The implementation must define and test how `lastExtendedOn` is repaired for historical threads; the approved default is to leave historical values null until the next genuine extension.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--topics"></a>
###### Topics

Topics are hashtags parsed from post text at the trusted post-write boundary.

- Normalize Unicode safely and store a canonical lowercase lookup form plus display text.
- Permit at most five unique topics per post.
- Bound each topic to 40 Unicode code points after normalization.
- Reject or ignore malformed topics without treating the rest of a valid post as HTML.
- Public topic pages use canonical encoded routes such as `/void/topic/music`.
- Topic feeds are chronological and include only active public threads.

Topic pages and API responses must escape all user-controlled display values. Topic lookup must not construct raw regular expressions or unbounded database queries from input.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--account-discovery"></a>
###### Account discovery

Signed-in users receive **People you may want to follow** based on deterministic overlap among topics they have:

- Posted in.
- Replied to.
- Kept alive.

Follower count, keep-alive count, post lifespan, and global popularity are not inputs. Already-followed, blocked, hidden, deleted, and self accounts are excluded. Ties use recent public activity and then a stable unique account identifier.

Anonymous visitors see a daily deterministic rotation of recently active public accounts. This prevents a permanent popularity hierarchy while keeping the section stable within a visit.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--abuse-and-moderation"></a>
###### Abuse and moderation

- New accounts receive stricter bounded posting, reply, follow, and keep-alive limits until the configured account-age threshold passes.
- Existing report, hide-thread, block, and administrative moderation boundaries remain authoritative.
- Explore endpoints return only the fields required for public rendering.
- Discovery caches exclude expired posts and have TTLs shorter than the expiration-cleanup interval.
- Topic and account queries require appropriate indexes and bounded results.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-2-acceptance-criteria"></a>
###### Release 2 acceptance criteria

- All four Explore sections implement their stated non-popularity ordering.
- Recently revived changes only after a confirmed lifespan extension.
- Topic extraction is normalized, bounded, deduplicated, safe, and covered across Unicode and malformed input.
- Suggested accounts never use likes or follower totals and exclude disallowed relationships.
- Anonymous Explore access works without exposing protected account data.
- Partial backend failure produces localized UI errors rather than a blank page.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-3-activitypub-federation"></a>
##### Release 3: ActivityPub Federation

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--consent-and-scope"></a>
###### Consent and scope

Existing accounts are not federated until their owners explicitly enable federation. New signup includes an explicit **Federate my public Void posts** choice that is enabled by default and accompanied by a clear disclosure:

- Federated posts and interactions are delivered to independent servers.
- Void sends Delete activities when content expires.
- Remote servers may retain cached or copied content despite deletion.

Federation applies only to public Void identities, posts, replies, follows, and keep-alive interactions. Disabling federation stops new outbound delivery and inbound interaction for the account; it does not claim to retract remote history automatically.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--protocol-surface"></a>
###### Protocol surface

Implement the bounded ActivityPub surface needed for interoperable public accounts:

- `/.well-known/webfinger` discovery for `@username@christopherbell.dev`.
- NodeInfo discovery and metadata.
- Public ActivityPub actors.
- Per-actor inbox, outbox, followers, and following collections.
- A shared inbox for outbound fan-out efficiency.
- Content negotiation that preserves existing HTML profile and post routes.

The first interoperability target is current Mastodon-compatible behavior. Unsupported activity types return a safe protocol response and do not mutate local state.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--outbound-mapping"></a>
###### Outbound mapping

- A new local root post or reply becomes a public `Create` containing a `Note`.
- A local reply uses the federated root or parent URI through `inReplyTo`.
- A local keep-alive becomes a `Like`; undo becomes `Undo(Like)`.
- Following a remote actor becomes `Follow`; local unfollow becomes `Undo(Follow)`.
- Expiration or owner/moderator deletion emits `Delete` with a tombstone to known recipients.
- Local edits may emit `Update` only while the post remains active.

Outbound delivery uses a durable queue with unique activity identifiers, per-recipient delivery state, bounded exponential backoff, terminal failure classification, and idempotent retry. One remote failure must not block other recipients or local requests.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--inbound-mapping"></a>
###### Inbound mapping

- A verified `Follow` is accepted for an enabled public account.
- A verified `Like` on an active local thread adds 24 hours exactly once per remote actor and target.
- `Undo(Like)` removes that actor's active extension exactly once.
- A verified public `Create(Note)` reply adds 24 hours to the root thread after content and relationship validation.
- `Delete` removes or tombstones locally retained remote content.
- Duplicate or replayed activities do not add time or create duplicate objects.

Remote extensions are abuse-bounded:

- One active keep-alive per remote actor and local target.
- Bounded accepted replies per actor, domain, and time window.
- Per-actor and per-domain request limits.
- A configurable rolling per-domain lifespan-extension ceiling per local root thread.
- Blocked actors and domains contribute no lifespan and receive no delivery.

Local engagement retains the approved existing lifespan rules.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--federation-security"></a>
###### Federation security

- Verify supported HTTP signatures, content digests, request dates, actor ownership, and key identity before mutation.
- Reject stale timestamps, invalid algorithms, mismatched hosts, oversized bodies, duplicate activity IDs, and signature replays.
- Fetch remote actors and keys only through an outbound policy that blocks loopback, private, link-local, multicast, and cloud-metadata destinations after every DNS resolution and redirect.
- Bound redirects, response bytes, connect time, total time, content types, and concurrent remote fetches.
- Store per-account private signing keys encrypted at rest with a protected application secret and support deliberate rotation.
- Never log signing material, authorization data, raw signatures, cookies, or full private payloads.
- Separate inbound and outbound feature flags and kill switches.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--operations-and-moderation"></a>
###### Operations and moderation

The Back Office gains a Federation panel containing:

- Inbound and outbound enabled state.
- Queue depth, retry age, and terminal failures.
- Known and recently active domains.
- Actor and domain block controls.
- Per-domain failure summaries without raw post bodies.
- Separate inbound and outbound emergency kill switches.

Federation rollout is gated inside Release 3:

1. WebFinger, NodeInfo, and local actor discovery.
2. Outbound follows and post delivery to controlled test peers.
3. Outbound production delivery for opted-in accounts.
4. Inbound follows.
5. Inbound keep-alives and replies after signature, replay, SSRF, moderation, and lifespan evidence passes.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--release-3-acceptance-criteria"></a>
###### Release 3 acceptance criteria

- Existing accounts remain unfederated until opt-in; new signup displays the approved explicit consent.
- A Mastodon-compatible test peer can discover, follow, receive, and reply to an opted-in Void actor.
- Valid remote Like/Undo and reply activities produce exactly the approved lifespan changes once.
- Expiration emits bounded Delete delivery and removes the local thread.
- Signature, replay, payload, redirect, DNS/IP, rate-limit, block, and queue tests pass.
- Inbound and outbound kill switches stop their respective effects without taking down local Void.
- Back Office exposes actionable health and moderation state without secrets or post-body logging.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--shared-architecture-and-boundaries"></a>
#### Shared Architecture and Boundaries

Keep the following responsibilities separate:

- **Post lifespan domain:** calculates and persists local thread expiration and extensions.
- **Feed and discovery queries:** return bounded active public projections with explicit ordering.
- **Topic extraction:** validates and normalizes topics at write time.
- **Recommendation service:** computes bounded interest overlap without popularity inputs.
- **Federation protocol boundary:** parses, validates, signs, and serializes ActivityPub messages.
- **Federation delivery queue:** owns outbound effects, retries, and recipient state.
- **Federation inbox service:** owns idempotency, verification, mapping, and mutation dispatch.
- **Remote fetch policy:** owns SSRF-safe actor/key retrieval.
- **Moderation and operations:** owns blocks, feature flags, queue visibility, and kill switches.

The browser must not calculate authoritative expiration, discovery eligibility, federation identity, or moderation decisions.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--expected-areas-of-change"></a>
#### Expected Areas of Change

Exact files belong in per-release implementation plans, but expected modules include:

- Existing post expiration, interaction, creation, feed, thread, and view packages.
- Void feed rendering, controller, templates, CSS, and JavaScript tests.
- Social-preview rendering and public post/profile metadata.
- New discovery/topic packages and indexed Mongo projections.
- Account-follow and public-profile projections.
- New federation protocol, inbox, delivery, remote-fetch, persistence, and operations packages.
- Security configuration, rate-limit configuration, Back Office surfaces, operational documentation, and production configuration examples.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--validation-strategy"></a>
#### Validation Strategy

Every release requires:

- RED-to-GREEN behavioral tests at the narrowest public boundaries.
- Java and JavaScript unit tests for all new invariants and malformed input.
- Security tests for anonymous/public versus authenticated mutation boundaries.
- Full repository checks and CodeQL/dependency review.
- Candidate validation on a non-8080 port on the Windows production host.
- One focused pull request per coherent release or release sub-stage.
- Automatic deployment from `main` followed by exact-SHA public smoke tests.
- Production verification that existing Void, login/signup, Messages, Music persistence, and administrative access remain intact.

ActivityPub additionally requires controlled-peer interoperability tests and negative tests for signatures, replay, SSRF, redirects, payload bounds, blocking, kill switches, idempotency, retry, and deletion.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--rollback-and-recovery"></a>
#### Rollback and Recovery

- Release 1 contains no required lifespan data migration and can roll back through the normal application release mechanism.
- Release 2 schema additions are additive. Old code ignores new topic and extension metadata; rollback must retain documents for later retry.
- Release 3 remains guarded by separate inbound/outbound flags. Disabling both returns Void to local-only operation without deleting queue evidence or signing keys.
- Federation queue replay must be deliberate and idempotent. Operators may retry terminal failures only through bounded Back Office actions.
- Expired local content is never restored merely because remote delivery failed.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--success-measures"></a>
#### Success Measures

The site should track privacy-preserving aggregate product health rather than public popularity:

- Anonymous Void visits that reach an active post or thread.
- Signup completions that originated from Void.
- New accounts that post, reply, follow, or keep something alive within seven days.
- Share actions and successful copied links.
- Active threads with at least two distinct participants.
- Explore-to-thread and topic-to-thread navigation.
- Opted-in federated accounts, successful deliveries, remote follows, and valid remote interactions.

Metrics must be retained only as long as operationally useful, avoid raw post bodies and secrets, and never affect feed ordering.

<a id="source-docs-specs-2026-07-28-void-public-growth-program-md--open-questions"></a>
#### Open Questions

None. Product direction, lifespan rules, public access, discovery rules, consent model, and federation rollout order are approved.

<!-- /migrated-source: docs/specs/2026-07-28-void-public-growth-program.md -->

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md"></a>
## 2026-07-28 | spoke-reviews | ChristopherBell.dev Unified Music Hub Review

Original source: `docs/spoke-reviews/2026-07-28-christopherbell-dev-unified-music-hub.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `31f4f7f16bd94ae7d00a7c7cb0b60385651f0bde801edd4ab768fef4f0d2476a`.

<!-- migrated-source: docs/spoke-reviews/2026-07-28-christopherbell-dev-unified-music-hub.md -->
<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--christopherbelldev-unified-music-hub-review"></a>
### ChristopherBell.dev Unified Music Hub Review

- Related work: [Shared Folder Portal](2026-07-17-christopherbell-dev.md#source-docs-work-2026-07-17-christopherbell-dev-shared-folder-portal-md)
- Specification: [Unified Music Hub](#source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md)
- Implementation plan: [Unified Music Hub](../implementation-plans/2026-07-28-christopherbell-dev-unified-music-hub.md)
- Test report: [Unified Music Hub Production](../test-reports/2026-07-28-christopherbell-dev-unified-music-hub-production.md)
- Repo: `azurras/christopherbell.dev`
- Branch: `codex/unified-music-hub`
- Pull request: [#1312](https://github.com/azurras/christopherbell.dev/pull/1312)
- Reviewed merge: `baf8910dd6707260ec02af94c13d36c1eb2d6979`

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--findings"></a>
#### Findings

No Blockers. No Warnings.

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--scope-reviewed"></a>
#### Scope Reviewed

Reviewed the independent Music permission boundary, seven-day-idle browser sessions, indexed/probed catalog, artwork and range streaming, denied-access audit, durable radio/queue/library state, revision-checked metadata edits and undo, responsive hub, persistent same-tab player, production media-tool resolution, rate limits, and non-interactive deployment path.

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--validation-checked"></a>
#### Validation Checked

Checked the full local repository gate, 246 JavaScript tests, the Windows production suite (243 passed, 0 failed, 4 expected environment skips), all three CI operating-system builds, dependency review, CodeQL, exact-SHA production deployment, anonymous authorization boundaries, security headers, services, and the single live listener.

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--house-style-compliance"></a>
#### House-Style Compliance

The implementation keeps Music authorization separate from Shared Folder download authority, contains filesystem and process effects behind validated boundaries, rejects stale metadata revisions, bounds queries/processes/uploads, fails startup when pinned media tools are invalid, and tests failure behavior across supported platforms. The final CodeQL and dependency review results are green.

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--residual-risks"></a>
#### Residual Risks

The final production smoke was intentionally read-only and anonymous. Authenticated reader/writer/admin interactions and desktop/mobile presentation were not driven through a production browser session during closeout. Focused automated coverage protects those contracts, and normal signed-in use is the remaining observational check.

<a id="source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md--merge-readiness"></a>
#### Merge Readiness

Approved, merged, automatically deployed, and production-smoked. No corrective code change is required from this review.

<!-- /migrated-source: docs/spoke-reviews/2026-07-28-christopherbell-dev-unified-music-hub.md -->

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md"></a>
## 2026-07-28 | work-closures | ChristopherBell.dev ActivityPub Discovery Foundation Closure

Original source: `docs/work-closures/2026-07-28-christopherbell-dev-activitypub-discovery-foundation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `73c79ce16331053534f348905d4765159cd2aacb5d0ab6f7a05d98873238c8c9`.

<!-- migrated-source: docs/work-closures/2026-07-28-christopherbell-dev-activitypub-discovery-foundation.md -->
<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--christopherbelldev-activitypub-discovery-foundation-closure"></a>
### ChristopherBell.dev ActivityPub Discovery Foundation Closure

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--final-status"></a>
#### Final Status

complete

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--related-work"></a>
#### Related Work

- Controlling program: [Void Public Growth Program](#source-docs-specs-2026-07-28-void-public-growth-program-md)
- Implementation plan: [ActivityPub Discovery Foundation](../implementation-plans/2026-07-28-christopherbell-dev-activitypub-discovery-foundation.md)
- Test report: [ActivityPub Discovery Foundation Test Report](../test-reports/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-test-report.md)
- Session memory: [ActivityPub Discovery Foundation Delivery](#source-docs-session-memory-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-delivery-md)

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--completed-scope"></a>
#### Completed Scope

Delivered the first guarded ActivityPub rollout gate. Accounts now have explicit signup/Profile consent, null-safe legacy opt-out behavior, a stable per-account RSA identity, and AES-256-GCM encryption for private PKCS#8 material. The public read-only surface includes WebFinger, NodeInfo 2.1, local Person actors, bounded active-post outboxes, and bounded local followers/following collections.

The release preserves the safety boundary: discovery, inbound, and outbound flags default off; no remote fetch, HTTP request signing, delivery queue, inbox mutation, remote persistence, or lifespan effect exists. Messages, Music, Shared Folder, reports, and administrative data are excluded. Signup shows the choice disabled when enrollment is unavailable, while an existing enrolled account can always opt out.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--pull-request-and-merge"></a>
#### Pull Request and Merge

- Pull request: [#1316](https://github.com/azurras/christopherbell.dev/pull/1316)
- Feature commits: `d7c11fa3`, `50cf469a`, `45b3618b`
- Rebase merge on `main`: `6cd9e397e4ec2c3175ae5c31a95f633b7a7c7c95`
- Automatic production deployment: complete; listener rotated from PID 34768 to PID 33352 and new signup markup appeared locally/publicly.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--validation"></a>
#### Validation

- Full local check: 1,353 Java tests, zero failures/errors, three skips; complete JavaScript and packaged/runtime checks passed.
- Isolated enabled runtime: consented signup, WebFinger, NodeInfo, actor, outbox, followers/following, no-store/CORS/nosniff headers, blocked inbox write, stable restart identity, and opt-out/re-enable behavior passed.
- Isolated disabled runtime: the app started without an encryption key, signup disabled enrollment, and public federation endpoints returned 404.
- GitHub: Ubuntu, macOS, Windows, dependency review, and all CodeQL analyses passed on PR #1316.
- Production: home/signup returned 200 locally/publicly; federation choice was present but disabled; NodeInfo/actor returned 404; all core services were Running/Automatic.
- Production data: 20 accounts, zero federation-enabled accounts, zero identities, and `federation_actor_lookup` present.
- Cleanup: port 8081 closed, isolated database dropped, and temporary scripts/logs removed.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--decisions"></a>
#### Decisions

- Existing and API-omitted accounts remain opted out; new browser signups default on only when the deployment is actually configured to enroll identities.
- Disabling discovery does not remove stored identity material, so re-enable preserves the actor and public key; it immediately removes public discoverability.
- Actor origin is derived only from the existing canonical browser public base URL.
- Outbox content is read-only, active-only, bounded to 20, cursor-stable, and HTML-escaped.
- One coherent PR carried the rollout gate. Reviews were limited to correctness, interoperability, and security boundaries.
- Production remains default-disabled until protected key installation and explicit activation are separately approved as an operational change.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-activitypub-discovery-foundation-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

No defect remains in this gate. This is not full federation.

The next approved gate is signed outbound delivery to a controlled peer, still off in production. It must add bounded remote actor/key discovery, strict SSRF and redirect controls, HTTP signing, retry/idempotency, payload limits, kill switches, and controlled-peer evidence before any outbound production activation. Inbound follows and mutations remain later gates.

Future work should start from merged `main`. Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; the isolated feature worktree is clean.

<!-- /migrated-source: docs/work-closures/2026-07-28-christopherbell-dev-activitypub-discovery-foundation.md -->

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md"></a>
## 2026-07-28 | work-closures | ChristopherBell.dev Unified Music Hub Closure

Original source: `docs/work-closures/2026-07-28-christopherbell-dev-unified-music-hub.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `f73e757674e528153bb3ebb1a736c6cc8fea136047569db81c92c936548a0180`.

<!-- migrated-source: docs/work-closures/2026-07-28-christopherbell-dev-unified-music-hub.md -->
<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--christopherbelldev-unified-music-hub-closure"></a>
### ChristopherBell.dev Unified Music Hub Closure

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--final-status"></a>
#### Final Status

complete

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--related-work"></a>
#### Related Work

- Work record: [Shared Folder Portal](2026-07-17-christopherbell-dev.md#source-docs-work-2026-07-17-christopherbell-dev-shared-folder-portal-md)
- Specification: [Unified Music Hub](#source-docs-specs-2026-07-28-christopherbell-dev-unified-music-hub-md)
- Implementation plan: [Unified Music Hub](../implementation-plans/2026-07-28-christopherbell-dev-unified-music-hub.md)
- Test report: [Unified Music Hub Production](../test-reports/2026-07-28-christopherbell-dev-unified-music-hub-production.md)
- Spoke review: [Unified Music Hub Review](#source-docs-spoke-reviews-2026-07-28-christopherbell-dev-unified-music-hub-md)
- Session memory: [Unified Music Hub Delivery](#source-docs-session-memory-2026-07-28-christopherbell-dev-unified-music-hub-delivery-md)

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--completed-scope"></a>
#### Completed Scope

Delivered the shared Music experience as one permissioned hub rather than per-user silos. The release adds independent `MUSIC_READ` and `MUSIC_WRITE` capabilities, a public data-free Music entry shell, denied-access auditing, durable browser sessions, a catalog rooted under `A:\Shared\Music`, protected streaming/artwork, one global radio/queue/history/library, writer metadata edits with backups and undo, and one persistent same-tab player that expands on `/music` and remains compact elsewhere.

Production integration now resolves FFmpeg and FFprobe only through the protected pinned-tool manifest and fails closed when the tool boundary is invalid. Dedicated mutation rate limits protect Music write paths without throttling range playback. Push-to-main deployment remained automatic and non-interactive.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--pull-request-and-merge"></a>
#### Pull Request and Merge

- Pull request: [#1312](https://github.com/azurras/christopherbell.dev/pull/1312)
- Feature commits: `185fd12b` through `b6b0310b`
- Squash merge on `main`: `baf8910dd6707260ec02af94c13d36c1eb2d6979`
- Automatic production deployment: complete; public versioned assets identify the exact merge SHA.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--validation"></a>
#### Validation

- Full local repository check passed.
- JavaScript: 246 passed.
- Production PowerShell: 243 passed, 0 failed, 4 environment-dependent skips.
- GitHub: Ubuntu, macOS, Windows, dependency review, Java/Kotlin CodeQL, and JavaScript/TypeScript CodeQL all passed.
- Production: `/`, `/music`, and the versioned Music stylesheet returned 200; the anonymous access probe returned a no-access response; anonymous catalog, radio, and stream returned 403.
- CSP, HSTS, and no-store headers were present.
- `ChristopherBellDev`, `MongoDB`, and `cloudflared` were Running/Automatic with one port-8080 listener.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--decisions"></a>
#### Decisions

- Music permissions do not grant Shared Folder downloads.
- Global radio, queue, favorites, playlists, exclusions, and history remain shared rather than user-specific.
- Music media paths remain server-side identifiers; no Music download endpoint was added.
- Same-tab playback state is durable, while browser autoplay restrictions are handled with explicit resume UI.
- Production media processes use a checksum-verified, protected manifest rather than PATH discovery.
- One PR carried the coherent feature, with only findings that affected correctness, portability, or security fixed before merge.

<a id="source-docs-work-closures-2026-07-28-christopherbell-dev-unified-music-hub-md--known-gaps-and-follow-ups"></a>
#### Known Gaps and Follow-ups

No known blocker remains. The closeout smoke did not use an authenticated production browser, so reader/writer/admin interactions and final desktop/mobile appearance were not manually replayed after deployment. Automated permission, mutation, playback-state, and responsive UI tests passed; signed-in use is a useful observational confirmation, not an outstanding implementation task.

Future changes should begin from the merged `main` release. The dirty authoritative checkout at `A:\Projects\christopherbell.dev` remains preserved; the isolated feature worktree is clean.

<!-- /migrated-source: docs/work-closures/2026-07-28-christopherbell-dev-unified-music-hub.md -->

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md"></a>
## 2026-07-28 | work | Website-Wide Security Audit and Remediation

Original source: `docs/work/2026-07-28-website-wide-security-audit-and-remediation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `10db0c66e43cfbc436253b508d80590baf4b6fd26e05d1ff1cd1e0fa1d2693f6`.

<!-- migrated-source: docs/work/2026-07-28-website-wide-security-audit-and-remediation.md -->
<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--website-wide-security-audit-and-remediation"></a>
### Website-Wide Security Audit and Remediation

- Status: closed
- Owner: Codex root agent
- Started: 2026-07-28

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--objective"></a>
#### Objective

Review every file in the current `azurras/christopherbell.dev` repository for security issues, validate realistic attacker paths, fix every validated finding with regression evidence, and complete production-safe delivery.

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--scope"></a>
#### Scope

- Repository-wide standard Codex Security scan of refreshed `origin/main`.
- Threat modeling, deterministic file inventory, candidate discovery, compact validation, and attack-path analysis.
- Minimal test-first fixes for validated findings only.
- Full repository verification, PR/CI/merge, production-safe verification, and Builder closeout.

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--spoke-repositories"></a>
#### Spoke Repositories

- `azurras/christopherbell.dev`
- Authoritative dirty checkout: `A:\Projects\christopherbell.dev` (preserve unchanged)
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\security-audit-20260728`

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--related-artifacts"></a>
#### Related Artifacts

- Repository-wide assessment report: `C:\Users\Christopher\AppData\Local\Temp\codex-security-scans\christopherbell.dev\f77c5f5bb644cc75cf98b27e722efdc00cd036f1_20260728T222511\report.md`
- ActivityPub freshness-delta report: `C:\Users\Christopher\AppData\Local\Temp\codex-security-scans\christopherbell.dev\6c1501070ff518bc040583c4576c2df201dcd3ed_20260729T113714\report.md`
- Pre-final remediation-branch report: `C:\Users\Christopher\AppData\Local\Temp\codex-security-scans\christopherbell.dev\edf3a439e6bdffae22090a33ab8b17d354c6ee34_20260729T113526\report.md`
- Final clean rescan: `C:\Users\Christopher\AppData\Local\Temp\codex-security-scans\christopherbell.dev\5a2186ea5ea2b946faecead2b514f408bab6031e_20260729T170846\report.md`
- [Test report](../test-reports/2026-07-29-website-wide-security-remediation.md)
- [Spoke review](2026-07-29-christopherbell-dev.md#source-docs-spoke-reviews-2026-07-29-website-wide-security-remediation-review-md)
- [Closure record](2026-07-29-christopherbell-dev.md#source-docs-work-closures-2026-07-29-website-wide-security-audit-and-remediation-md)

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--current-state"></a>
#### Current State

PR [#1324](https://github.com/azurras/christopherbell.dev/pull/1324) was squash-merged as `e3f7c676e8bf73a11056b9f009723ba9628025e8`. The final security rescan closed all 26 review rows with zero remaining findings. Production automatically deployed the merge, rotated the port 8080 listener from PID 60136 to PID 48420, and passed internal and external smoke checks. Issues #1281, #1282, #1283, #1288, #1298, #1306, and #1307 are closed by the merge.

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--blockers"></a>
#### Blockers

None. The production ACL correctly denied this non-elevated shell direct access to protected deployment configuration and release metadata; verification used the guarded auto-deployer, listener/service evidence, exact live-asset comparison, database ping, and public behavior without weakening the ACL.

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--validation"></a>
#### Validation

- Repository-wide scan: 15 validated findings (5 high, 7 medium, 3 low); fixes were implemented here or reconciled with newer mainline fixes.
- ActivityPub freshness scan: two low findings; one was fixed and one became not applicable after current main removed the retired approval state. Approved affirmative-consent privacy hardening was also delivered.
- Pre-final branch scan: one Low/P3 dependency-metadata bootstrap finding, fixed in commit `5a2186ea`.
- Final clean rescan: 26 of 26 rows closed; zero candidates or remaining findings.
- Strict clean build: 1,575 Java tests, 0 failures, 0 errors, 4 skipped.
- Browser suite: 279 passed, 0 failed.
- PR CI, Dependency Review, and CodeQL: passed.
- Post-merge main CI and CodeQL: passed on Linux, macOS, and Windows.
- Alternate-port packaged runtime: eight cases passed; live port 8080 remained unchanged.
- Production: merge SHA remained current main; listener rotated; exact live JavaScript matched the merge; MongoDB ping returned `ok: 1`; website, media worker, MongoDB, and cloudflared services were Running/Automatic; internal and external roots returned 200; security-sensitive denial and federation-default checks passed.

<a id="source-docs-work-2026-07-28-website-wide-security-audit-and-remediation-md--next-steps"></a>
#### Next Steps

None. Resume only if a new finding, regression, or dependency update creates new scope.

<!-- /migrated-source: docs/work/2026-07-28-website-wide-security-audit-and-remediation.md -->

