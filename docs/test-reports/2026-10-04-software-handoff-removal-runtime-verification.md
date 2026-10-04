# Software handoff removal runtime verification

## Document Status

complete

Candidate, reviewed PR/full platform CI, merge, supported deployment and public acceptance verified. Final main CI also passes on all three platforms. Earlier pending observations remain historical.

## Story/Issue

User2026-10-04 request: remove software handoff material from the site. [Plan](../implementation-plans/2026-10-04-remove-software-handoff-offer-from-site.md). Separate local product archive/historical records outside removal scope.

## Branch

codex/remove-handoff-kit-20261004 from1fbb84a146bb0f433af81036f13791f53013b2ab. Final independently reviewed staged patch SHA256 E38EB6B6B2A27FC0FD23F53AEBC750914A378E07FE72C46B9B6B8CEF1243F697. Packaged website.jar SHA2561DE50444E88FC0E54784D3852FEC44BD04BD733CB41860926F7BA917638C6083.

## App / Environment

Native Windows Java25.0.3, http://127.0.0.1:18092, profiles test/deploy-smoke. Explicit mongodb://127.0.0.1:27031/test, owned disposable fixture with valid existing ledger; never27017. Scheduling/mail disabled; build-owned storage/media roots. Native test classes use mocked repositories/security matchers, not database connections. Production remains8080PID22456/27017PID5192.

## Local Run Details

Worktree A:/Projects/christopherbell.dev-worktrees/blog-placeholder-cleanup-20261003. Owned Mongo9380 started hidden with C:/Program Files/MongoDB/Server/8.3/bin/mongod.exe --dbpath "A:/Projects/christopherbell.dev-worktrees/blog-placeholder-cleanup-20261003/website/build/runtime-handoff-kit-20261003/mongo-data" --port 27031 --bind_ip 127.0.0.1 --logpath website/build/runtime-remove-handoff-20261004/mongo.log. Existing fixture recovered normally after previous owned process shutdown; no live database use. Candidate5544 started06:49CDT:

```powershell
& 'C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe' '-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp' -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27031/test --app.scheduling.enabled=false --app.mail.enabled=false --app.shared-folder.root=website/build/runtime-remove-handoff-20261004/shared --app.shared-folder.system-root=website/build/runtime-remove-handoff-20261004/system --app.music.root=website/build/runtime-remove-handoff-20261004/shared/Music --app.music.artwork-cache-root=website/build/runtime-remove-handoff-20261004/system/artwork --app.music.metadata.private-root=website/build/runtime-remove-handoff-20261004/system/metadata --app.music.media-tools.root=website/build/runtime-remove-handoff-20261004/system/tools --server.address=127.0.0.1 --server.port=18092 --app.browser-security.public-base-url=http://127.0.0.1:18092
```

Stopped only candidate5544/Mongo9380 after exact executable/port/database-path checks.18092/27031 no longer listen; production8080/27017 unchanged. No production fixture records.

## Test Cases

| Request/check | Actual response | Result |
|---|---|---|
| GET readiness |200 UP |pass|
| GET former offer/preview |410 empty; no attachment; no-store/noindex |pass|
| POST former URLs |403 |pass|
| GET former/full,extra,preview/extra |404 |pass|
| GET sitemap.xml |200; no software-handoff-kit; includes site-monitor |pass|
| GET nav.js |200; no offer URL/label; monitor present |pass|
| GET site-monitor |200 Free pilot/Daily checks |pass|
| JAR resource entries |template/worksheet absent |pass|
| Focused Views/Sitemap/security, JS/syntax, bootJar |pass after fixture correction |pass|

## Data Sent

Anonymous native HTTP requests at http://127.0.0.1:18092: GET /actuator/health/readiness, /software-handoff-kit, /software-handoff-kit/preview, /software-handoff-kit/full, /software-handoff-kit/extra, /software-handoff-kit/preview/extra, /sitemap.xml, /js/components/nav.js, /site-monitor. POST both former exact URLs without credentials/CSRF; no bodies/data mutations. ZIP inspection of compiled JAR names for software-handoff resource entries. No cookies/passwords/customer content.

## Response Received

Both former GET URLs returned status410 Gone, response body empty, Cache-Control:no-store, X-Robots-Tag:noindex, no Content-Disposition. Anonymous POSTs returned status403 Forbidden. Neighboring page URLs returned status404 Not Found under the existing public HTML fallback. Sitemap/nav returned status200 OK without offer URLs/text; monitor returned status200 OK with Free pilot and Daily checks. Readiness response body {"status":"UP"}. JAR contained zero software-handoff resource paths.

## Pass / Fail

Initial Java regressions failed before production edits for two410 endpoints, packaged-resource absence and sitemap removal (remove-handoff-red.log,2m13s); navigation red also caught unwanted entry. First green run passed73/74 Java tests, lone newly added public near-miss denial expectation failed: existing public HTML fallback deliberately sends unknown page GETs to404. Removed that incorrect test expectation; production security behavior unchanged. Existing neighboring404 tests/mutation checks retained. Corrected focused SecurityConfigTest, JS380/380 and bootJar passed51s; nav.js syntax passed. View/Sitemap passing results in firstgreen retained. Fresh full platform CI required before merge.

## Evidence

website/build/remove-handoff-red.log, remove-handoff-nav-red.log, remove-handoff-green.log, remove-handoff-final-green.log; runtime-remove-handoff-20261004/app.log, mongo.log, http-proof.log/http-proof.json, probe.py. Final source review E38EB6B6B2A27FC0FD23F53AEBC750914A378E07FE72C46B9B6B8CEF1243F697 no Critical/Important blockers; reviewer ran no tests. Fresh predeployment prod.cmd auto-status2026-10-04T11:39:11Z FRESH/UP_TO_DATE/RUNNING/HEALTHY, active/remote1fbb84a1,failureNONE. Native candidate proof/cleanup at06:49-06:50CDT.

## Bugs / Follow-ups

CI, supported deployment and public acceptance pending. No browser rendering/keyboard/console proof because prior refused actions remain respected; this deletion has native HTTP/template/JS proof. Existing external caches/search results may persist until refresh; new former-URL GETs return410. Exact legacy route strings remain solely to retire URLs, with no offer/download assets. No database/deployer/monitor behavior changes.

### 07:07CDT live delivery readback

PR1476 all eight checks passed (Windows7m26s, macOS4m16s, Linux3m2s), exact reviewed head995745e539f87957ee5a79f3d12e6e0bc78059c0 squash merged76681a5ca5abd418e8ab5dc4f166a0da8563bb9b at2026-10-04T12:00:45Z. Fresh supported observer12:07:10Z FRESH/UP_TO_DATE, remote/active/attempted/successful76681a5c,RUNNING/HEALTHY,failureNONE. No elevated/manual service operation.

Native HTTPS and listener acceptance: GET former page/preview status410 Gone, empty response body, no attachment,no-store/noindex; sitemap200 without offer and with monitor; monitor200 Free pilot/Daily checks; current fingerprint920968b64c790818ce4f navigation200 without offer label/URL; readiness200UP. Evidence runtime-remove-handoff-20261004/production-proof.log and production-proof.json, production_probe.ps1. Application8080PID38056/Mongo27017PID5192 present; candidate18092/27031 remain stopped. Main CodeQL37200650176 passed; main CI37200650155 Linux/macOS passed, Windows still running at this observation.

Final07:08CDT readback: main CI Build37200650155 completed success for Windows/macOS/Linux; CodeQL37200650176 success. Fresh12:08:10Z production remains UP_TO_DATE/RUNNING/HEALTHY with identical76681a5c release SHAs and failureNONE. Earlier Windows-pending observation is historical. Functional removal delivery and cleanup are complete; no source issue for external closure.
