# Software Project Handoff Kit website income funnel

## Document Status

ready-for-execution

Semantic self-review found no blocking ambiguity: fixed public content, one free resource, no buyer data or purchase flow. Demand and price remain unvalidated.

## Plan Format

task-contract-v1

## Objective

Find legal ways for christopherbell.dev to eventually earn income, with payment processing deferred by the user. Publish a useful first product discovery path for an existing original kit, then continue evaluating income opportunities from evidence.

## Goals

Make the kit discoverable to independent developers handing off small software projects. Explain six worksheets, fictional worked example, editable Markdown, and nine-page printable noninteractive PDF. Display a planned $15 USD one-time price and prominently say purchases are unavailable. Let visitors download the delivery-inventory sample without an account. Do not claim sales or validated demand.

## Inputs

Active user goal and existing autonomous website delivery authority; site AGENTS.md; current main 52e1573; original product at C:/Users/Christopher/Developer/software-handoff-kit (README.md, HANDOFF-KIT.md, PREVIEW.md). FTC truthful advertising guidance https://www.ftc.gov/business-guidance/advertising-marketing informed the use of factual claims. Original preparation plan is [here](2026-09-13-software-project-handoff-kit-preparation.md).

## Branch

codex/handoff-kit-income-funnel-20261003 from refreshed origin/main in the existing isolated blog-placeholder-cleanup-20261003 worktree. Preserve unrelated gradlew.bat line-ending dirt.

## Non-Goals

Checkout, collecting customer information, paid downloads, subscriptions, custom support, paid advertising, outreach, accounts, spending, homepage redesign, or production database changes. The paid ZIP/PDF/full toolkit stays local.

## Assumptions

The website is the authorized publishing channel. Existing prepared material is available and its contents can be verified. No ongoing user labor is required for this phase. A useful free preview and transparent future product page can establish an offer before checkout.

## Open Questions

None blocking this phase. Demand, conversion, and future payment/fulfillment will need separate evidence; the broad income goal stays active.

## Task Breakdown

### Task 1 - Publish product discovery and free sample

- Required skill: write-jane-street-style-code before code changes.
- Dependencies: None; publish this reviewed plan first.
- Files: website/src/main/java/dev/christopherbell/view/content/ContentViewController.java; website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java; website/src/main/java/dev/christopherbell/configuration/PublicSitemapService.java; website/src/main/resources/static/js/components/nav.js; website/src/test/java/dev/christopherbell/view/ViewControllerTest.java; website/src/test/java/dev/christopherbell/configuration/SecurityConfigTest.java; website/src/test/java/dev/christopherbell/configuration/PublicSitemapServiceTest.java; website/src/test/js/nav-messages-link.test.js; owning View/configuration/JS READMEs; new templates/resources/software-handoff-kit.html and products/software-handoff-kit-preview.md beneath website/src/main/resources. Inspected photo/usage.html as the template pattern and original PREVIEW.md as the sample.
- Symbols: ContentViewController page/download handlers; PUBLIC_URLS; STATIC_URLS; toolsMenuItems; relevant controller, route-matcher, sitemap, and navigation tests.
- Inspection: Read all named existing handlers, public matcher patterns, sitemap count/shard contracts, navigation sorting tests, template layout, and product inventory on current main. Content routing already owns static pages; no new domain subsystem is required.
- Behavior: Anonymous visitors can read /software-handoff-kit and download /software-handoff-kit/preview. Product page includes audience, contents, sample explanation, planned price, purchase availability, usage permission, AI assistance disclosure, and no guarantees. Public Tools navigation and sitemap link to the page.
- Invariants: Fixed classpath sample only; do not expose full package or secrets; no collection, database writes, new dependencies, fabricated endorsements, scarcity, or ongoing support promises. Preserve existing authentication and private routes.
- Boundary/API: Exact GET public page and preview routes; preview response text/markdown;charset=UTF-8 with attachment filename software-project-handoff-preview.md. Neighboring routes and mutation methods remain protected. Existing clients unaffected.
- Effects and failures: Read packaged immutable sample; no dynamic path or network IO. A missing packaged resource is a server failure, never a misleading successful empty download. Existing Spring resource handling owns streaming/errors.
- Tests and evidence: Failing route/download/navigation/sitemap contracts before implementation; passing focused and full native Java/JS checks afterward. Verify package contents against current source, rendered page, anonymous download, real responsive navigation, and effective isolated Mongo test target.
- Verification: node --test website/src/test/js/nav-messages-link.test.js; node --check website/src/main/resources/static/js/components/nav.js; :website:check and :website:bootJar using private WSL Gradle cache when native Windows loopback prevents startup; git diff --check. Candidate on 18090 and isolated Mongo test on 27029, test/deploy-smoke profiles, scheduling/mail disabled; verify actual connection log and anonymous GETs. Check desktop/mobile rendering and preview bytes/header; stop only owned candidate processes.

### Task 2 - Deliver and record production proof

- Dependencies: Task 1 candidate verification and semantic diff review pass.
- Files: This plan; dated christopherbell-dev session memory; new dated runtime report; site PR and required CI.
- Symbols: Document Status, completion evidence, PR merge/deployment state.
- Inspection: README documents SYSTEM auto-deployer every minute and guarded application rollback. Current deployment is healthy at 52e1573, no new migration changes.
- Behavior: Publish candidate report before source PR; require Java25 on Linux/macOS/Windows, CodeQL and Dependency Review; merge and let supported automatic deployment rotate service. Verify new page/download/nav/sitemap on production.
- Invariants: No manual production process kill, elevated operations, ACL changes, database fixture writes, payment collection, or revenue claim.
- Boundary/API: Existing PR/CI and prod.cmd auto-status; public read-only HTTP/browser checks.
- Effects and failures: Source publication and supported deployment only. On CI failure repair the scoped cause; on failed deployment preserve current healthy service and follow documented recovery rather than repeated restarts.
- Tests and evidence: Fresh matching merged/active/attempted/successful SHA, service RUNNING, site HEALTHY, readiness UP, actual public page/download/navigation/sitemap acceptance.
- Verification: gh pr checks/view; prod.cmd auto-status; anonymous public GET /software-handoff-kit, /software-handoff-kit/preview and /sitemap.xml; real browser desktop/mobile. Publish verified delivery memory and completion report; keep income goal active until its full intended outcome is proved.

## Code Changes

Thin content handlers, static honest product page and sample, exact GET permissions, existing sorted Tools menu and canonical sitemap. No checkout or analytics subsystem.

## Files and Modules

View owns HTML/download presentation; configuration owns permission and sitemap boundaries; shared nav owns discovery. Paid artifacts remain outside the site.

## Unit Testing

Controller response and downloadable real-resource contracts, public-route restrictions, sitemap presence/exclusion of download, anonymous Tools discovery and unchanged gating. Full :website:check required because shared security is touched.

## Local Testing

Packaged native Java25 candidate on alternate ports using copied verified disposable Mongo test fixture. Confirm application connection is only 27029, jobs/mail disabled, test shared-folder paths isolated. No production Mongo test execution.

## Validation

Plan structure and semantic self-review, diff review, package inventory inspection, focused then full tests, candidate runtime report, all required CI, and fresh deployed public behavior.

## Rollback or Recovery

No data/schema changes. Reject candidate before merge if any acceptance fails. If deployed page regresses, revert only this PR through trusted main deployment after verifying current service health; no protected files or manual service rotation.

## Risks

Demand is unknown; the page cannot be represented as sales. A planned price and availability statement must agree. Preview should be useful while the paid full kit stays private. Shared navigation/security require regression coverage.

## Completion Criteria

This phase completes only after reviewed source, full checks, candidate proof, required CI, merge, healthy automatic deployment, and public page/download/navigation/sitemap proof plus published Builder artifacts. The larger income goal remains active: no revenue is yet verified and checkout is explicitly deferred.
