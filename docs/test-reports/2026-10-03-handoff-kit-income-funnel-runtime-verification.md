# Handoff kit income funnel runtime verification

## Document Status

complete

## Story/Issue

First website path toward eventual income: planned Software Project Handoff Kit and useful free delivery-inventory sample. Payment processing explicitly deferred. [Implementation plan](../implementation-plans/2026-10-03-christopherbell-dev-handoff-kit-income-funnel.md).

## Branch

codex/handoff-kit-income-funnel-20261003 from main52e1573; reviewed source commit1a90dd66942f5f6949a45c92934fbaacd6664df4. [PR1472](https://github.com/azurras/christopherbell.dev/pull/1472) merged at2026-10-04T00:50:36Z as0f90854b45ee258521be22c23dc500ccedeb44c6 after all eight reported checks passed. Production acceptance passed at19:57CDT on that merge SHA.

## App / Environment

Packaged Java25.0.3 / Boot4.1.1 Windows candidate at http://127.0.0.1:18090. Explicit spring.mongodb.uri=mongodb://127.0.0.1:27029/test; test,deploy-smoke profiles; scheduling and mail disabled. Candidate shared-folder paths under build. Copied prior disposable verified Mongo fixture into runtime-handoff-kit-20261003/mongo-data,244847194 bytes; no live database copy or write. Native Mongo8.3 process18332, Java35508/session20597. Existing production8080/27017 kept running.

## Local Run Details

Candidate artifact website/build/libs/website.jar SHA256 AE84CCA84F61E7DA69CFC02EDFF812613946466C2F301F24265AF43959529004. Process-only JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp. Startup at19:19 CDT confirmed actual Mongo connection only127.0.0.1:27029, then Tomcat18090 and readiness. Anonymous IAB rendered the desktop page and mobile375x812 page. Temporary viewport reset and tab closed. Stopped owned Java session20597 and Mongo18332 after command-line ownership check. Ports18090/27029 closed; production8080/27017 remained listening.

Candidate launch: java -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27029/test --app.scheduling.enabled=false --app.mail.enabled=false --server.address=127.0.0.1 --server.port=18090. The existing SYSTEM auto-deployer observed the trusted main change, built/validated it, and rotated production through its supported mechanism; no manual restart or elevation was used.

The first WSL baseline Gradle run/session23548 was deliberately stopped after a live thread dump proved repeated whole-asset-tree hashing for every application.yml line. Java route baseline tests never ran; do not count them as failed regressions. New JS navigation tests failed before implementation (3 failures), then14/14 focused passed and378/378 full JS passed. Resource-processing fix freezes the fingerprint only on its first read. Broad :website:check/:website:bootJar run/session14683 ended after14m21s with one incorrect new test assumption; XML299 suites:1978 total,137 skipped,1 failure,0 errors. After correcting that assertion, all70 tests across ViewControllerTest, SecurityConfigTest and PublicSitemapServiceTest passed (zero failures/errors/skips), along with native serialization/counting and sensor-resolution gates and bootJar. Focused build/session3096 succeeded in2m41s. Application source was unchanged after the broad run; passing unaffected test evidence is reused and full unfiltered CI is required before merge. No changes to protected permissions, firewall or production configuration.

## Test Cases

| Interaction | Observed result |
| --- | --- |
| Anonymous GET readiness | HTTP200 |
| Anonymous GET /software-handoff-kit | HTTP200; one main h1, planned $15USD, explicit unavailable-for-purchase statement |
| Anonymous GET /software-handoff-kit/preview before browser denial | HTTP200; text/markdown;charset=UTF-8; attachment filename software-project-handoff-preview.md; file bytes exactly match packaged source |
| Anonymous GET /sitemap.xml | HTTP200; canonical kit page present, download absent |
| Desktop Tools button | Public kit link visible; no console errors |
| Mobile375x812 hamburger then Tools | Kit link visible; content width360 <= viewport375; one h1; screenshot showed readable stacked hero/price card and download button |
| Browser download-button click | Browser security policy blocked the requested download because permission was declined. No workaround or second download attempted. This UI download path is unverified; earlier HTTP response proof remains valid. |
| Packaged contents inspection | Only free sample under products; no full kit Markdown, paid ZIP or PDF |
| Independent fingerprint computation | Python sorted relative paths plus null boundary and SHA256 content digests produced5e69429fc58407e68e6e; packaged application.yml matches |
| Production readiness and product page | HTTP200; readiness status UP; planned price and unavailable statement visible |
| Production preview metadata only | HTTP200; text/markdown;charset=UTF-8; attachment filename software-project-handoff-preview.md. ResponseHeadersRead followed by disposal; no preview body read or file saved. |
| Production sitemap | HTTP200; exact canonical page present, preview absent |
| Production desktop/mobile browser | Anonymous Tools link visible at both sizes; readable hero/price card; mobile width360 <=375, one main h1, no forms; console errors empty. Viewport reset and owned tab closed. |

## Data Sent

Anonymous requests GET http://127.0.0.1:18090/software-handoff-kit, GET http://127.0.0.1:18090/software-handoff-kit/preview, GET http://127.0.0.1:18090/sitemap.xml, GET http://127.0.0.1:18090/actuator/health/readiness. Browser input: Tools, mobile hamburger, and sample button. No customer data, payment identifiers, messages or accounts.

Production: GET https://www.christopherbell.dev/actuator/health/readiness, GET https://www.christopherbell.dev/software-handoff-kit, GET https://www.christopherbell.dev/sitemap.xml, and GET https://www.christopherbell.dev/software-handoff-kit/preview with headers-only completion and immediate disposal. Browser visited the public product page, clicked Tools, resized temporarily to375x812 and opened the mobile navigation. No further preview download was attempted after the declined permission.

## Response Received

HTTP status 200 response page heading Software Project Handoff Kit. Visible planned price $15 USD and Not available for purchase yet. Candidate preview HTTP status 200 headers Content-Type text/markdown; charset=UTF-8 and Content-Disposition attachment; filename="software-project-handoff-preview.md". Worksheet response includes delivery inventory, recipient access/evidence fields, no-credentials instruction and permission for completed handoffs. Browser UI is accessible at desktop/mobile; console errors empty. Browser download itself was blocked by tool policy, not proven completed. Production page and sitemap returned HTTP status 200, readiness returned {"status":"UP"}, and preview response headers matched the candidate; the production preview body was not read.

## Pass / Fail

Candidate HTTP/content/navigation/layout/package checks and70 focused native tests pass. Browser button-download verification limited by declined permission. Broad local run had the one corrected test-assumption failure described above; do not call that full command successful. Full unfiltered Java25 builds passed on Ubuntu, macOS and Windows in PR CI, with CodeQL and Dependency Review also passing. Production readiness, page, navigation, responsive layout, sitemap, and preview metadata pass on the merged release. Browser-managed download completion remains unverified and is not claimed. No sales or validated demand.

## Evidence

PR CI Build run37165742705 completed all three platform builds successfully (Ubuntu2m46s, macOS4m1s, Windows7m54s). CodeQL run37165742738 passed all three language checks and the aggregate check; Dependency Review run37165742718 passed. Fresh PR readback before merge confirmed unchanged head1a90dd66 and CLEAN merge state. Merge command used --match-head-commit. Main CI run37166184727 and CodeQL37166184744 subsequently started against the exact mergeSHA; deployment was observed DEPLOYING with the previous release still RUNNING/HEALTHY at19:52CDT.

Supported auto-status at2026-10-04T00:56:37Z reported SUCCEEDED and then at00:57:11Z FRESH/UP_TO_DATE, service RUNNING, site HEALTHY, failureCategory NONE, tool refresh SUCCEEDED, and identical remote/active/attempted/successful SHA0f90854b45ee258521be22c23dc500ccedeb44c6. Windows observer poller ACCESS_DENIED/UNKNOWN remains the known read-only scheduler-query limitation; actual deploy result and application proof passed. Production listener8080 rotated to PID16552 while Mongo27017 remained PID5192. Public HTTP and IAB desktop/mobile checks passed at19:56-19:57CDT. Main CI Build run37166184727 subsequently completed successfully on all three platforms; CodeQL run37166184744 also completed successfully. Fresh status at00:59:10Z still reports the matching release RUNNING/HEALTHY and no failure. The service observer reports ChristopherBellDev Running with wrapper PID21700.

Owned app log runtime-handoff-kit-20261003/app.log confirms port/DB/health. ZIP integrity and byte comparison against original sources passed; current PDF confirmed9 pages through bundled pypdf. Original package SHA25657A21D8FEA377CBDADC17F4B7A883206E0FF7478D38475FEE6420CC4842D35AF. Live stack trace showed Gradle line-filter re-entering staticAssetFingerprint; new packaged fingerprint matches independent calculation. Native test logs retained under website/build.

## Bugs / Follow-ups

Demand and price are unvalidated; no revenue earned or buyer flow enabled. Continue income work after this phase using actual audience/demand evidence. The scoped asset-hashing build blocker fix passed native regression and cross-invocation input trials, all PR CI, and production deployment. No GitHub source issue to close. Browser-managed sample download completion is the explicit verification limitation described above.

The first full Java run exposed an incorrect new test expectation: unknown HTML GET paths are intentionally public so MVC can render404, rather than redirecting to login. Removed that false matcher assumption, retained POST checks and added PUT/DELETE rejection plus actual neighboring-path404 controller coverage. Existing fallback behavior is preserved; the full kit is not an endpoint or packaged public resource. Revised test/gate execution passed.

Independent read-only review of staged patch SHA256 C11B82A17AB4116B8D7C966C6B91EC3990D61A27890B3397D0F4A89C8449F8E6 found no Critical/Important/Minor issues. Reviewer did not run tests/runtime, inspect binary page count independently, access production, or judge demand/revenue; primary execution supplied candidate/native/package evidence and will own CI/deployment proof. Declined browser download remains an explicit limitation.

Controlled asset-input trial passed across fresh Gradle invocations: baseline5e69429fc58407e68e6e, temporary isolated probe changed it to d4c57049bc0ac913abf7, then removing the owned probe restored5e69429fc58407e68e6e. Both processResources builds succeeded (35s and13s); probe is absent. This proves both invalidation and restoration without changing production or leaving a test asset in the publication. The previous live run had remained in repeated hashing for more than10 minutes before being intentionally stopped. The later focused JAR SHA25635F533B833145A22121BD9D51BB6642C22F137FFFF60F281A7401936B6C81616 has the same feature content/fingerprint; only subsequent build metadata differs from the exercised candidate.
