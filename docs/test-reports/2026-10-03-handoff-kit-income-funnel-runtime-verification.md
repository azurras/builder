# Handoff kit income funnel runtime verification

## Document Status

draft

## Story/Issue

First website path toward eventual income: planned Software Project Handoff Kit and useful free delivery-inventory sample. Payment processing explicitly deferred. [Implementation plan](../implementation-plans/2026-10-03-christopherbell-dev-handoff-kit-income-funnel.md).

## Branch

codex/handoff-kit-income-funnel-20261003 from main52e1573; reviewed source commit1a90dd66942f5f6949a45c92934fbaacd6664df4. PR, CI, merge and deployment remain pending.

## App / Environment

Packaged Java25.0.3 / Boot4.1.1 Windows candidate at http://127.0.0.1:18090. Explicit spring.mongodb.uri=mongodb://127.0.0.1:27029/test; test,deploy-smoke profiles; scheduling and mail disabled. Candidate shared-folder paths under build. Copied prior disposable verified Mongo fixture into runtime-handoff-kit-20261003/mongo-data,244847194 bytes; no live database copy or write. Native Mongo8.3 process18332, Java35508/session20597. Existing production8080/27017 kept running.

## Local Run Details

Candidate artifact website/build/libs/website.jar SHA256 AE84CCA84F61E7DA69CFC02EDFF812613946466C2F301F24265AF43959529004. Process-only JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp. Startup at19:19 CDT confirmed actual Mongo connection only127.0.0.1:27029, then Tomcat18090 and readiness. Anonymous IAB rendered the desktop page and mobile375x812 page. Temporary viewport reset and tab closed. Stopped owned Java session20597 and Mongo18332 after command-line ownership check. Ports18090/27029 closed; production8080/27017 remained listening.

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

## Data Sent

Anonymous requests GET http://127.0.0.1:18090/software-handoff-kit, GET http://127.0.0.1:18090/software-handoff-kit/preview, GET http://127.0.0.1:18090/sitemap.xml, GET http://127.0.0.1:18090/actuator/health/readiness. Browser input: Tools, mobile hamburger, and sample button. No customer data, payment identifiers, messages or accounts.

## Response Received

HTTP200 response page heading Software Project Handoff Kit. Visible planned price $15USD and Not available for purchase yet. Download HTTP200 headers Content-Type text/markdown; charset=UTF-8 and Content-Disposition attachment; filename="software-project-handoff-preview.md". Worksheet response includes delivery inventory, recipient access/evidence fields, no-credentials instruction and permission for completed handoffs. Browser UI is accessible at desktop/mobile; console errors empty. Browser download itself was blocked by tool policy, not proven completed.

## Pass / Fail

Candidate HTTP/content/navigation/layout/package checks and70 focused native tests pass. Browser button-download verification limited by declined permission. Broad local run had the one corrected test-assumption failure described above; do not call that full command successful. Required full CI and production acceptance remain pending; no delivery claim yet.

## Evidence

Owned app log runtime-handoff-kit-20261003/app.log confirms port/DB/health. ZIP integrity and byte comparison against original sources passed; current PDF confirmed9 pages through bundled pypdf. Original package SHA25657A21D8FEA377CBDADC17F4B7A883206E0FF7478D38475FEE6420CC4842D35AF. Live stack trace showed Gradle line-filter re-entering staticAssetFingerprint; new packaged fingerprint matches independent calculation. Native test logs retained under website/build.

## Bugs / Follow-ups

Demand and price are unvalidated; no revenue earned or buyer flow enabled. Continue income work after this phase using actual audience/demand evidence. The scoped asset-hashing build blocker has a candidate fix; complete checks before publication. No GitHub source issue to close.

The first full Java run exposed an incorrect new test expectation: unknown HTML GET paths are intentionally public so MVC can render404, rather than redirecting to login. Removed that false matcher assumption, retained POST checks and added PUT/DELETE rejection plus actual neighboring-path404 controller coverage. Existing fallback behavior is preserved; the full kit is not an endpoint or packaged public resource. Revised test/gate execution passed.

Independent read-only review of staged patch SHA256 C11B82A17AB4116B8D7C966C6B91EC3990D61A27890B3397D0F4A89C8449F8E6 found no Critical/Important/Minor issues. Reviewer did not run tests/runtime, inspect binary page count independently, access production, or judge demand/revenue; primary execution supplied candidate/native/package evidence and will own CI/deployment proof. Declined browser download remains an explicit limitation.

Controlled asset-input trial passed across fresh Gradle invocations: baseline5e69429fc58407e68e6e, temporary isolated probe changed it to d4c57049bc0ac913abf7, then removing the owned probe restored5e69429fc58407e68e6e. Both processResources builds succeeded (35s and13s); probe is absent. This proves both invalidation and restoration without changing production or leaving a test asset in the publication. The previous live run had remained in repeated hashing for more than10 minutes before being intentionally stopped. The later focused JAR SHA25635F533B833145A22121BD9D51BB6642C22F137FFFF60F281A7401936B6C81616 has the same feature content/fingerprint; only subsequent build metadata differs from the exercised candidate.
