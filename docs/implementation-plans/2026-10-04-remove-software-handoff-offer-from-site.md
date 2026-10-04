# Remove software handoff offer from the site

## Document Status
ready-for-execution

## Plan Format
task-contract-v1

## Objective
Remove the Software Handoff Kit offer, guidance and sample from the live site as requested on2026-10-04.

## Goals
No Tools or sitemap promotion; no packaged offer/checklist/fictional example or worksheet download. Exact former page and preview URLs return empty410 Gone with no-store/noindex; mutations/neighboring routes remain protected. Existing Website Monitor remains usable. Verify and deploy through supported automatic delivery.

## Inputs
User removal request; current main1fbb84a1 and fresh healthy production11:39Z; inspected site AGENTS/README, ContentViewController, view/configuration/JS READMEs, SecurityConfig GET rules, PublicSitemapService and corresponding Java/JS tests. Prior dated delivery records identify original product files; local product archive is outside site scope.

## Branch
Reuse isolated A:/Projects/christopherbell.dev-worktrees/blog-placeholder-cleanup-20261003 on codex/remove-handoff-kit-20261004 from origin/main1fbb84a1; preserve unrelated gradlew.bat. Builder main only exact selected artifacts.

## Non-Goals
No deletion of the separate local software-handoff-kit archive or historical records. No monitor feature changes, databases, deployer changes, payment setup or browser permission retries.

## Assumptions
Removal includes published downloadable preview.410 deliberately retires existing URLs; compatibility route strings remain solely to return no content.

## Open Questions
None blocking; removal and supported deployment are authorized.

## Task Breakdown

### Task 1 - Remove content and discovery
Required skill: chris-street-style
Dependencies: Published reviewed plan.
Files: Inspected website/src/main/java/dev/christopherbell/view/content/ContentViewController.java, view/README.md, configuration/PublicSitemapService.java, configuration/security/SecurityConfig.java (comments/public GET rules), configuration/README.md, resources/static/js/components/nav.js and static/js/README.md; delete resources/templates/resources/software-handoff-kit.html and resources/products/software-handoff-kit-preview.md; affected ViewControllerTest, SecurityConfigTest, PublicSitemapServiceTest and nav-messages-link.test.js.
Symbols: Replace two handoff controller handlers with combined empty410 response; remove product nav and STATIC_URLS entry; adjust owning documentation and discovery/download tests.
Inspection: Current isolated main1fbb84a1 confirms only product page/preview, nav, sitemap and listed owning docs advertise the offer. Other generic technical handoff references are unrelated.
Behavior: Remove page guidance/pricing/fictional sample and worksheet download; no discoverable product link; former exact GET paths return410 with empty body/no attachment/no-store/noindex.
Invariants: Existing public pages/monitor preserved, private/mutation boundaries unchanged, no broad URL allowance, no production fixtures/DB changes; unrelated working changes remain.
Boundary/API: Exact previously public GET page/preview become retired410; no redirect or substitute offer. Former product resources absent from packaged classpath.
Effects and failures: Delete only two tracked site resource files; other edits bounded to route/navigation/sitemap/docs/tests. Unrecognized paths remain existing404/authorization behavior.
Tests and evidence: Regression-first former GET410/body/header/resource absence, removed Tools entry for signed-out/signed-in/admin, removed sitemap canonical, existing monitor rendering and mutation/near-miss protection. Focused native Java/JS, syntax and bootJar then full platform CI.
Verification: :website:test affected classes, :website:jsTest, node --check nav.js, bootJar artifact contents and immutable source review.

### Task 2 - Verify and publish removal
Required skill: chris-street-style
Dependencies: Task1 passing tests and independent review.
Files: This plan, dated runtime report/session record, selected site implementation; inspect supported prod.cmd automatic deployer and owned disposable fixture.
Symbols: Candidate readiness/retired routes/discovery, artifact identity, PR/CI/merge/deployed SHA and closure readback.
Inspection: Existing automatic SYSTEM main observer reports current1fbb84a1 RUNNING/HEALTHY; prior candidate used separate27031/test ledger fixture with jobs/mail disabled and build roots.
Behavior: Native Windows candidate on18092 with explicit test/deploy-smoke and isolated27031/test proves410/no body/attachment, no nav/sitemap offer, monitor200 and readinessUP. Publish evidence, create PR, await all checks, merge exact reviewed head, observe supported deployment and public acceptance.
Invariants: No elevated access/manual service rotation or live DB test records; stop only owned candidate processes; respect refused browser actions.
Boundary/API: Existing GitHub CI/merge and protected automatic deployer; non-destructive public HTTP requests only.
Effects and failures: Failed tests/CI/push/deploy stay incomplete; use supported rollback to1fbb84a1 if required, no ad hoc process changes.
Tests and evidence: Actual status/response headers/body/URLs and classpath absence, process ownership/cleanup, all platform CI and deployed identity/service proof. Browser execution unperformed by existing permission constraint.
Verification: Builder validators/exact publisher; gh PR checks and guarded merge; prod.cmd auto-status and production GET checks.

## Code Changes
Remove offer assets and discovery; replace exact old handlers with empty410 retirement responses. Keep current exact public GET allowlist solely for retirement responses, documented and tested.

## Files and Modules
View/content routing, configuration sitemap metadata, shared Tools navigation, two product resource deletions and owning tests/docs. No persistence module changes.

## Unit Testing
User AGENTS requires native tests. Observe new deletion behavior regressions fail before removal, pass afterward. Full shared-configuration :website:test runs in platform CI before merge; focused local checks and JS suite support candidate.

## Local Testing
Native Java25 Windows candidate18092, owned separate27031/test Mongo fixture, test/deploy-smoke profiles, explicit disabled scheduling/mail, build-scoped storage. Retired URLs GET410 empty/no attachment/no-store/noindex; sitemap/nav absence; monitor/readiness remain healthy. No visual/browser proof claimed.

## Validation
Structural plan and semantic readiness reviewed before implementation. Independent immutable patch review plus full PR CI required; actual candidate runtime report published before source publication.

## Rollback or Recovery
Supported automatic protected rollback to1fbb84a1 if required. No data/schema changes; previous source can restore the removed assets. Preserve historical records and unrelated changes.

## Risks
Cached old content or external search results may persist until refresh; new requests receive410 and removed links. No browser rendering/keyboard/console verification because prior refusals persist.

## Completion Criteria
Offer and preview removed from artifact/navigation/sitemap; exact old URLs410, monitor/readiness remain healthy; reviewed patch and passing native/CI evidence, supported deployed SHA verified, owned helpers stopped, final Builder report/plan/session published.
