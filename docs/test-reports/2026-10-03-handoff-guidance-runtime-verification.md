# Handoff guidance runtime verification

## Document Status

complete

## Story/Issue

Original public software-handoff guidance for the planned digital kit, toward eventual website income with payment processing deferred. No source issue. [Plan](../implementation-plans/2026-10-03-christopherbell-dev-handoff-guidance.md).

## Branch

codex/handoff-guidance-20261003 from main0f90854b45ee258521be22c23dc500ccedeb44c6. Candidate content identified by immutable three-file patch SHA256443C3771B0E28512184497CC84064FD924AEB8BD5FFF89917FDB4AD46A962E7F, which exactly matches committed source427d750fcad8638043a2ca07e2ba8cb8664b6e22. [PR1473](https://github.com/azurras/christopherbell.dev/pull/1473) merged at2026-10-04T01:21:18Z as8d7e85e2262ac279c35cf5bb8a43e7d8671cb211 after all reported checks passed. Production acceptance passed on that merge SHA at20:28CDT.

## App / Environment

Native Windows Java25.0.3 / Spring Boot4.1.1 candidate at http://127.0.0.1:18091. Mongo8.3 on127.0.0.1:27030/test using the previously owned disposable runtime-handoff-kit-20261003/mongo-data fixture. No production data copy or write. Explicit test/deploy-smoke profiles, scheduling/mail disabled, shared/system paths under current build/runtime-handoff-guidance-20261003. Production8080/27017 kept running.

## Local Run Details

Candidate JAR SHA2561457A2420FAC77368A7F2F08E3A56EF570667ED7EA173BA2C50CDB017A084C3C. Process-only JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp. Command: java -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27030/test --app.scheduling.enabled=false --app.mail.enabled=false --app.shared-folder.root=build/runtime-handoff-guidance-20261003/shared --app.shared-folder.system-root=build/runtime-handoff-guidance-20261003/system --server.address=127.0.0.1 --server.port=18091.

Owned Mongo8376 was launched from installed Mongo8.3 mongod.exe with hidden window, explicit fixture dbpath, bind127.0.0.1, port27030 and candidate mongo.log. Application PID19516/session74028 started20:10:19CDT and actual driver log confirmed connection only27030. Candidate GET readiness/page passed. Application session stopped with Ctrl+C; Mongo stopped after exact PID/command-line/fixture/port ownership check. Both candidate listeners closed; production remained8080 PID16552 and27017 PID5192. No elevated operations or manual production actions.

Native WSL Gradle private cache /tmp/gradle-blog-placeholder-20261003. New rendered-guidance regression failed on baseline at the missing Software project handoff checklist string:1 test,1 failure,1m53s, preserved red-view-result.xml. After HTML additions, full ViewControllerTest plus bootJar succeeded in1m34s:49 tests,0 failures/errors/skips. No backend/security/JS changes; unaffected prior platform/security/JS evidence is reused and all-platform PR CI remains required.

## Test Cases

| Input | Actual result |
| --- | --- |
| GET candidate readiness | HTTP status200; response body status UP |
| GET candidate product page | HTTP status200; checklist, fictional delivery record, outstanding production deployment, fit guidance, price and unavailability rendered |
| Canonical/metadata/source structure | Exact canonical URL retained; checklist description; one main h1; anchor/ARIA targets present; semantic ordered/definition lists; sample links unchanged |
| New MVC regression before edit | Failed for missing checklist as expected |
| Full view-controller suite after edit |49 tests pass,0 failures/errors/skips; bootJar succeeds |
| Candidate browser navigation | Tool denied127.0.0.1:18091 because permission was declined. No retry, alternate surface, host variant or indirect browser access attempted. Owned empty tab closed. |
| Candidate process cleanup | Only owned Java/Mongo stopped; candidate ports closed; production listeners remain |
| Production GET product page | HTTP status200; six checklist steps, labeled fiction, pending deployment, fit guidance, one h1, no forms and unchanged planned price/unavailability/canonical |
| Production readiness and sitemap | HTTP status200; readiness UP; exact canonical present and preview absent from sitemap |
| Production release identity | FRESH/UP_TO_DATE, RUNNING/HEALTHY, all release SHAs8d7e85e2, failure NONE |

## Data Sent

GET http://127.0.0.1:18091/actuator/health/readiness and GET http://127.0.0.1:18091/software-handoff-kit anonymously, before browser permission denial. No customer, payment or credential data. No sample download retried. Browser attempted ordinary candidate page navigation and stopped after denial.

Production acceptance used the materially safer server-response observations: anonymous GET https://www.christopherbell.dev/software-handoff-kit, GET https://www.christopherbell.dev/actuator/health/readiness and GET https://www.christopherbell.dev/sitemap.xml. No browser retry or attempt to reproduce the blocked candidate navigation; no preview body/download fetched.

## Response Received

HTTP status 200 product response body contains Software project handoff checklist, Fictional delivery record, Still open: production deployment and Not available for purchase yet. Canonical remains https://www.christopherbell.dev/software-handoff-kit. Readiness response body is {"status":"UP"}. Driver log excerpt confirms127.0.0.1:27030 and active test/deploy-smoke profiles; startup log confirms Tomcat18091. Browser did not reach a rendered candidate page because permission was declined.

Production HTTP status 200 response has exactly six checklist list-items, one h1 and zero forms, with both guide/example anchor links and matching targets. Fiction labeling, pending work, fit guidance, planned $15 price, purchase unavailability and canonical all passed actual response checks. Readiness response body is {"status":"UP"}; sitemap HTTP status200 contains the canonical and excludes the download. No production visual, keyboard/screen-reader or console result is claimed for this added content.

## Pass / Fail

Native rendering, packaging, candidate HTTP/readiness, isolated database connection and owned-process cleanup pass. Independent source review found no Critical/Important/Minor issues. Visual layout, keyboard/screen-reader and browser console proof for the added content are unverified because candidate browser permission was declined. Existing CSS/JS/layout framework are unchanged; do not infer those checks ran. All PR CI and supported production acceptance now pass; details follow.

PR CI subsequently passed: full Java25 platform builds on Ubuntu/macOS/Windows, CodeQL Java/JavaScript/actions and aggregate, and Dependency Review. Source head427d750f was unchanged and merge state CLEAN before the guarded merge. CI is complete; production acceptance subsequently passed.

## Evidence

Logs under website/build: handoff-guidance-red.log, handoff-guidance-green.log, runtime-handoff-guidance-20261003/app.log and mongo.log. Baseline XML copied to runtime-handoff-guidance-20261003/red-view-result.xml. Current ViewControllerTest XML reports49/0/0/0. Source patch SHA256443C3771B0E28512184497CC84064FD924AEB8BD5FFF89917FDB4AD46A962E7F reviewed independently against main0f90854b. Reviewer confirmed six practical steps, fiction/pending acceptance labeling, accurate availability, heading hierarchy, matching anchors and no new interfaces.

CI Build37167414848 passed Ubuntu3m2s, macOS2m31s and Windows5m29s; CodeQL37167414812 and Dependency Review37167414808 passed. Fresh PR readback showed all eight reported checks SUCCESS. Merge used --match-head-commit427d750fcad8638043a2ca07e2ba8cb8664b6e22; authoritative readback confirms mergeSHA8d7e85e2262ac279c35cf5bb8a43e7d8671cb211.

Existing SYSTEM automatic deployment reported SUCCEEDED at2026-10-04T01:27:23Z, then FRESH/UP_TO_DATE at01:28:11Z with identical remote/active/attempted/successful SHA8d7e85e2262ac279c35cf5bb8a43e7d8671cb211, service RUNNING, site HEALTHY, failureCategory NONE and tool refresh SUCCEEDED. Service ChristopherBellDev is Running (wrapper37768);8080 listener26772, Mongo27017 still5192. Known scheduler observer ACCESS_DENIED/UNKNOWN does not contradict actual successful operation and public application evidence. Production HTTP acceptance passed20:28CDT. Main CI Build37167757293 passed all three platforms; CodeQL37167757213 passed.

Final product audit reconfirmed ZIP57A21D8FEA377CBDADC17F4B7A883206E0FF7478D38475FEE6420CC4842D35AF, all three intended members byte-identical to source, and PDF9 pages. Packaged candidate JAR contains only the free preview under products; no full kit Markdown, PDF or ZIP. Demand and sales remain unvalidated.

## Bugs / Follow-ups

No source defect found. Respect candidate browser permission denial and inherited preview-download denial; no workaround. Carry unverified browser behavior into delivery evidence. No earned revenue, validated demand, affiliate account, advertising program, outreach, buyer collection or payment work. Income opportunity assessment is in the plan. User's eventual-income request does not require a sale or payment-processing implementation in this phase.
