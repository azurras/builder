# Handoff kit guidance and income opportunity assessment

## Document Status

ready-for-execution

Semantic review: bounded additions to an inspected public template, its rendered-view test, and owning documentation. No unresolved implementation decision.

## Plan Format

task-contract-v1

## Objective

Advance the user's request to find legal ways for the website to eventually generate income, with payment processing deferred. Make the existing original digital product easier to evaluate through practical public guidance and record evidence-based income options.

## Goals

Publish an original six-step software handoff checklist and one clearly fictional delivery record on the existing product page. Explain when the free worksheet is enough and when the full kit may be useful. Preserve the planned $15 price and explicit purchase unavailability. Verify rendered content, responsive layout, CI and healthy production delivery. Assess other income models against the user's zero-spending and zero-ongoing-labor constraints without promising demand, sales, or legal certainty.

## Inputs

User's active eventual-income objective; current site main0f90854b; completed [product page plan](2026-10-03-christopherbell-dev-handoff-kit-income-funnel.md) and its candidate/production report; original local HANDOFF-KIT.md and README; current site AGENTS.md and inspected rendered-view contracts. Free handover templates at https://www.smartsheet.com/content/project-handover-templates establish competition only.

## Branch

codex/handoff-guidance-20261003 from fetched origin/main0f90854b in existing isolated blog-placeholder-cleanup-20261003 worktree. Preserve unrelated gradlew.bat line-ending changes.

## Non-Goals

Payment processing, customer collection, accounts, outreach, paid distribution, new routes, database changes, telemetry, paid file exposure, custom services, subscriptions, support commitments, copying competitor content or claiming earnings. An actual sale or validated willingness to pay is not implied by this preparatory delivery.

## Assumptions

Useful public content can give readers a concrete way to evaluate the offer, but is not evidence of traffic or conversion. The existing canonical page and public Tools link provide discovery. Original kit content remains the factual source for the offer.

## Open Questions

Demand and price are unvalidated. No missing answer prevents this bounded delivery; future transactions remain deferred by the user.

## Task Breakdown

### Task 1 - Add practical original guidance to the offer

Required skill: write-jane-street-style-code before code changes.
Dependencies: Prior product delivery passed all CI and current production is healthy at0f90854b.
Files: website/src/main/resources/templates/resources/software-handoff-kit.html; website/src/test/java/dev/christopherbell/view/ViewControllerTest.java; website/src/main/java/dev/christopherbell/view/README.md.
Symbols: Existing contentsHeading/sampleHeading/termsHeading; new checklistHeading/exampleHeading/fitHeading; handoffKitPageExplainsThePlannedProductWithoutOfferingCheckout and a focused rendered-guidance test.
Inspection: Read complete current product template, view README and the relevant WebMvcTest methods on fetched main0f90854b. The route, security, sitemap and nav already exist and need no change. Inspected original kit start, inventory, access and usage sections.
Behavior: Visitors can read six practical handoff steps, a compact fictional record with version, receiving owner, observed access, and an unresolved item, and choose whether a free inventory sheet or a broader kit suits their work. Guidance is visible HTML without login or download. Description metadata reflects the checklist.
Invariants: One main h1; existing price/unavailable statement and sample URL; original factual content; fiction labeled; no credentials or customer details, unsupported outcomes, forms, or paid package exposure.
Boundary/API: Existing GET /software-handoff-kit, canonical URL and static preview contract unchanged. Template output only; no backend or JavaScript behavior change.
Effects and failures: Public HTML changes. Thymeleaf must render valid content; ordinary render errors remain observable failures. No external I/O, database or account mutation.
Tests and evidence: Add rendered guidance regression first, observe failure on absent headings/record, then passing result. Reuse unaffected prior JS/security/sitemap/native evidence; run focused ViewControllerTest, bootJar, CI builds and candidate/prod browser proof for changed HTML.
Verification: :website:test --tests dev.christopherbell.view.ViewControllerTest :website:bootJar using private WSL cache; git diff --check. Candidate18091 with explicit spring.mongodb.uri=mongodb://127.0.0.1:27030/test, test/deploy-smoke profiles, jobs/mail disabled, test storage paths. Confirm actual Mongo connection and no production target. Anonymous HTTP and browser desktop/mobile375x812 must show checklist, labeled fiction, visible unresolved item, suitability advice, unchanged unavailability, one h1 and no overflow. No further browser sample download after the earlier declined permission. Stop only owned candidate processes.

### Task 2 - Deliver and assess the income path

Dependencies: Task1 focused checks, semantic review and candidate proof pass.
Files: This plan; dated handoff-guidance runtime report; docs/session-memory/2026-10-03-christopherbell-dev.md; source PR and CI.
Symbols: Income opportunity assessment, Delivery Outcome, Document Status and runtime evidence.
Inspection: Prior reviewed offer/source/package evidence, live matching release status, current original product files, public primary-source monetization policies where relevant. Production deploy mechanism remains the existing SYSTEM auto-deployer with rollback.
Behavior: Publish reviewed source through PR, all platform CI and supported automatic deployment. Prove live content and report realistic next income steps. Separate actual artifacts from unvalidated market assumptions.
Invariants: Preserve healthy production, zero spending/user labor, no unapproved messages or accounts, no payment work, no invented revenue or forecasts. Existing download permission refusal is respected.
Boundary/API: Existing GitHub publication and prod.cmd auto-status; public read-only HTTP/browser; Builder artifacts only.
Effects and failures: Source publication and deployer-owned service rotation. On failed CI fix the scoped cause; on deployment failure follow supported recovery without repeated manual restarts. Assessment does not enroll in services or enter contracts.
Tests and evidence: Required PR Java25 Ubuntu/macOS/Windows builds, CodeQL and Dependency Review pass; merge readback; fresh matching release SHAs and RUNNING/HEALTHY; live rendered changed content. Assess template sales, disclosed relevant affiliate content, and advertising/sponsorship against primary policies and actual known assets/audience gaps; select work that fits constraints.
Verification: gh pr checks/view; prod.cmd auto-status; GET public product page/readiness and desktop/mobile browser; runtime-report and plan validators, semantic review and exact-file Builder publisher. Complete this phase only with published evidence. Audit the user's actual eventual-income request independently of payment/sale results before deciding goal status.

## Code Changes

Original HTML guidance and accurate description metadata; focused rendered-view test; owning view README. No backend, authorization, route, navigation, sitemap, asset, dependency or database change.

## Files and Modules

Existing content view/template owns the offer. Builder owns the opportunity assessment and evidence; full buyer ZIP and PDF remain local.

## Unit Testing

ViewControllerTest is an MVC slice with mocked preview/profile/consent services and no database connection. Add one focused public-content assertion covering checklist, fictional example, outstanding action and fit guidance; preserve existing contract tests.

## Local Testing

Reuse the stopped owned disposable test fixture from prior handoff runtime. Start isolated Mongo27030/test and native packaged candidate18091, verifying effective test profile and actual connection. Verify response and real desktop/mobile layout. Never operate on production test fixtures. No download retry after denied permission.

## Validation

Plan validation and semantic review before published implementation; red/green view test; native packaging; independent semantic source review; candidate report before source publication; all PR CI; healthy exact deployed release; public acceptance; Builder delivery publication.

## Rollback or Recovery

HTML-only change with no data migration. If candidate fails reject it before merge. If deployed content regresses, revert the scoped PR through trusted main and the supported deployer after observing current health. No protected ACL or service changes.

## Risks

An educational page does not guarantee search visibility, visitors or buyers. Free alternatives exist. Avoid presenting a fictional record as an endorsement or closed acceptance; keep pending work visible. Existing kit package claims must remain accurate. Browser-managed preview download completion remains an inherited verification limitation.

## Completion Criteria

The original guidance is visible in the existing live page with truthful availability and fiction labeling; affected native checks, source review, all PR CI and candidate/production proof pass; required artifacts are published. Income models are assessed honestly with a selected concrete original-product path and unresolved demand described. User-requested payment deferral remains honored. Goal completion is determined from the actual request to work toward eventual income, without adding a requirement to process payments or earn a sale in this task.
