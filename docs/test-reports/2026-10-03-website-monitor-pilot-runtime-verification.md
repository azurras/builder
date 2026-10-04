# Website monitor pilot runtime verification

## Document Status

complete

Candidate, healthy public demo, full CI, supported deployment and cleanup verified. Earlier pending observations below remain historical evidence. Browser execution remains unverified.

## Story/Issue

User-approved recurring website monitoring/client-reporting free pilot. [Plan](../implementation-plans/2026-10-03-christopherbell-dev-site-monitor-pilot.md). Billing/email deferred; $29/month demand unvalidated.

## Branch

codex/site-monitor-pilot-20261003, base 8d7e85e2262ac279c35cf5bb8a43e7d8671cb211. Reviewed patch59CFA66BFE0440F78305812FAFE7E3373D859DF80AC98980CC1A5DA86A9F1672. Final patch1A46053C1CF734F2B66C48461D3F813402EE090610D7593727B089796B55937D adds only requested GET/HEAD README correction. JAR SHA256 C175C4A47B4BA34668CF0F549816C98532B2C1EA74E488F768862B47FD2D7690.

## App / Environment

Windows Java25.0.3, test/deploy-smoke profiles, candidate http://127.0.0.1:18092, owned mongodb://127.0.0.1:27031/test. Scheduling/mail disabled; shared/media roots build-owned. Owned Mongo PID26780 uses prior disposable fixture website/build/runtime-handoff-kit-20261003/mongo-data with valid migration ledger. Production8080/27017 not test targets; no production fixture accounts.

## Local Run Details

Worktree A:/Projects/christopherbell.dev-worktrees/blog-placeholder-cleanup-20261003. Start:

```powershell
& 'C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe' '-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp' -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27031/test --app.scheduling.enabled=false --app.mail.enabled=false --app.shared-folder.root=website/build/runtime-site-monitor-20261003/shared --app.shared-folder.system-root=website/build/runtime-site-monitor-20261003/system --app.music.root=website/build/runtime-site-monitor-20261003/shared/Music --app.music.artwork-cache-root=website/build/runtime-site-monitor-20261003/system/artwork --app.music.metadata.private-root=website/build/runtime-site-monitor-20261003/system/metadata --app.music.media-tools.root=website/build/runtime-site-monitor-20261003/system/tools --server.address=127.0.0.1 --server.port=18092 --app.browser-security.public-base-url=http://127.0.0.1:18092
```

PID21668 started23:16CDT and stopped after command-line identity check; restart PID32848 at23:18 retained workspace/export. Candidate/Mongo remain for postdeploy demo. Initial fresh fixture failed existing migration015 ledger precondition; no bypass. Hidden background Java launch was rejected by automatic approval review; tracked foreground launch succeeded without elevation. Refused browser/download permissions not retried.

## Test Cases

| Case | Actual response | Result |
|---|---|---|
| Readiness/public shell |200 UP /200 free pilot, no email |pass|
| Anonymous workspace |403 |pass|
| Two isolated accounts signup/login |201/200 each |pass|
| Owner empty workspace |200 sites=0 |pass|
| Missing CSRF cookie mutation |403 |pass|
| Private destination |400 |pass|
| Fixed demo creation |200 three configured pages |pass|
| Other owner baseline/report |404/404 |pass|
| Check before baseline |409 |pass|
| Predeploy real demo |200 INCOMPLETE; no baseline, old asset HEAD403 |expected negative; healthy proof pending|
| Cooldown |429 Retry-After900 |pass|
| Private report |200 text/plain UTF-8 attachment, no-store |pass|
| Candidate fingerprinted CSS/app/site-monitor JS |GET200/HEAD200 each |pass|
| Private HEAD /asset mutation |403/403 |pass|
| Restart saved workspace/report |200 same report identity and exact UTF-8 export |pass|
| Native real Mongo lifecycle |2 pass,0 skipped |pass|

## Data Sent

GET readiness/shell/private API. Existing account create/login POST with random example.invalid emails/usernames and generated passwords; secrets excluded. Cookie mutations echo X-XSRF-TOKEN except negative case. POST monitor sites {"demo":true,"label":"Demo"}; private target {"label":"Private","origin":"https://127.0.0.1","paths":["/"]}. Owner/unrelated-owner baseline/check/report requests. Fixed outbound public https://www.christopherbell.dev paths /, /zip-coordinates, /vin-decoder. Session cookies kept only in ignored owned fixture for restart proof.

## Response Received

Real packaged demo pages returned HTTP status 200 OK; old production versioned assets returned status 403 Forbidden to HEAD. Baseline remained empty and report INCOMPLETE. Independent production listener /1a08c0e07629ed51549c/js/app.js and css/main.css GET200/HEAD403 reproduced defect. Candidate /a57ce69853a0cdadcb36/ CSS/app/site-monitor assets GET/HEAD200. Private HEAD403 and asset POST403. Restart retained report ID and identical text; helper explicitly reads UTF-8 to avoid Windows default file decoding.

Real-Mongo lifecycle test uses controlled gateway/clock (not real HTTP change/failure): healthy owned baseline, title CHANGES, due daily check/not-due suppression, failed500 capture preserves baseline, nested records reload, generation-safe slot reuse, stale save/delete rejected, owner cleanup isolated and preexisting indexes unchanged. Native driver connected127.0.0.1:27031/test. No actual customer ownership-file deployment or browser interactions claimed.

## Pass / Fail

Candidate HTTP/restart/native Mongo/focused checks pass. Initial healthy demo assertion failed and exposed HEAD defect; evidence retained. New HEAD regression failed before fix then passed. Earlier broad local run:2033 Java tests,3 fixture failures,137 skips; corrected deletion expectations/controller security setup pass focused retests. JS380/380 pass; modified three JS files pass node --check. Final focused security/monitor+bootJar pass1m42s; JwtAuthenticationFilterTest pass28s. Fresh full PR CI required; earlier broad run was not passing.

## Evidence

Local website/build logs: site-monitor-full-build.log, site-monitor-controller-fixed.log, site-monitor-head-red.log, site-monitor-head-fixed.log, site-monitor-jwt.log, site-monitor-native-mongo.log (2 successful). Runtime folder runtime-site-monitor-20261003: initial http-probe.log, http-probe-predeploy.log, predeploy-proof.json, predeploy-report.txt, asset-proof.log, restart-predeploy.log, app-final.log/app-restart.log. Native launcher validates SITE_MONITOR_TEST_MONGO_URI database=test,loopbackhost,port!=27017. Historical manifest digest/frozen architecture baseline unchanged. Final independent review found no Critical/Important findings; requested README correction applied. Fresh prod.cmd auto-status2026-10-04T04:17:11Z: FRESH/UP_TO_DATE/RUNNING/HEALTHY, active/remote8d7e85e2,failureNONE. Protected poller ACCESS_DENIED is a visibility limit.

## Bugs / Follow-ups

Healthy actual demo requires supported HEAD fix deployment. Browser UI/keyboard/console proof unperformed due refused permissions; native HTTP/template/JS evidence available. Billing/email/acquisition unvalidated. Pilot ten accounts,five sites/account,five pages/site,ten reports/site. Bounded metadata/assets do not prove rendered layout, transactions, uptime/security or automatic repair. Stop only owned candidate/Mongo after final proof; preserve production and unrelated work.

### 23:38CDT deployment and CI follow-up

PR1474 all eight checks passed, including Java25 Windows/macOS/Linux; squash merged57b04c5cc997fdf224e42951d6d704e98c777cca at2026-10-04T04:30:15Z. Supported deploy SUCCEEDED04:36:37Z, matching remote/active/attempted/successful SHA, RUNNING/HEALTHY/failureNONE. Listener8080 and public HTTPS native PowerShell probes: /site-monitor200, fingerprint15ad359e610f046d364b CSS/app/site-monitor GET/HEAD200, sitemap200, readiness200UP, anonymous API403. Public Python urllib probe403; native PowerShell and real Java gateway returned200. These are HTTP observations, not browser rendering proof.

Actual candidate on isolated test database captured BASELINE for all three fixed public demo pages, exported private no-store plain text and retained cross-owner/CSRF/cooldown rejections. Evidence: runtime-site-monitor-20261003/http-probe-postdeploy.log, postdeploy-proof.json, postdeploy-report.txt, production-proof.log (includes urllib403), production-public-proof.json. Candidate restart retention of this healthy baseline is pending.

Main CodeQL37177189114 passed; main CI37177189246 macOS failed existing RateLimitFilterTest.sharedFolderUploadRequestsConsumeTheFirstMatchingDedicatedBucket (2036 tests,1 failed,137 skipped). Inspected test exhausts240/minute greedy-refill bucket with241 requests and assumes completion before250ms refill. Published before-edit plan433c99a. Test-only follow-up uses capacity1/two requests while separate assertions retain production240/minute and rule ordering. Focused RateLimitFilterTest/RateLimitPropertiesTest passed46s (site-monitor-rate-limit-fixed.log). Independent immutable test patch E41A8B6132F7ED9E2A61D1BA2FC6219CC153635ED2AE4D3C5D4C8ABA2E830F30 review found no blockers. Runtime does not apply to this test-only change; production code and packaged runtime evidence are unchanged. Follow-up full PR CI required.

### 23:39CDT healthy baseline restart and fixture cleanup

Restart candidate PID34100: owner workspace200 retained all three healthy baseline pages and same report ID; private export200 retained exact UTF-8 body/no-store. DELETE owned demo200. Evidence restart-postdeploy.log and app-healthy-restart.log. Stopped only candidate PID34100 and Mongo26780 after executable/port/database-path identity checks. Candidate18092/Mongo27031 no longer listening; production8080 PID38308 and27017 PID5192 remain. This completes actual healthy demo/restart/remove proof. No production fixture records were created. Follow-up test-only PR1475 commit1cb5e636 opened; full CI pending.

### Final delivery readback - 23:55CDT

PR1475 all eight checks passed (Windows7m34s, macOS3m47s, Linux2m25s); squash merged1fbb84a146bb0f433af81036f13791f53013b2ab at2026-10-04T04:47:01Z. Final main CI Build37177992226 completed success for all three Java25 platforms; main CodeQL37177992194 completed success. These fresh runs include the corrected upload fixture; the prior main macOS failure remains recorded above.

Supported automatic deploy succeeded04:52:21Z; fresh04:55:10Z observer FRESH/UP_TO_DATE, remote/active/attempted/successful1fbb84a1, RUNNING/HEALTHY,failureNONE. Final native HTTPS and listener acceptance at23:53CDT: pilot200 with one h1/free limits/email exclusion/canonical, fingerprint15ad359e610f046d364b CSS/app/site-monitor JS GET/HEAD200, sitemap200 includes pilot, readiness200UP, anonymous monitorAPI403. Saved production-final-proof.json. Application8080 PID22456; Mongo27017 PID5192. Owned candidate18092/Mongo27031 remain stopped. Functional pilot delivery is complete with explicitly unperformed browser rendering/keyboard/console checks, deferred payments/email and unvalidated acquisition/price/demand. No source issue to close and no revenue claim.
