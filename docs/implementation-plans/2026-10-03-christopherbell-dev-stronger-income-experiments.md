# Stronger website income experiments

## Document Status
draft

## Plan Format
task-contract-v1

## Objective
Replace the generic worksheet as the main income hypothesis with a product that saves a business recurring work. This is an opportunity assessment and bounded experiment design, not a claim of validated demand or a ready application implementation plan.

## Goals
Identify a buyer, a paid outcome, realistic operating obligations, competition, and a demand gate before further substantial development. Preserve the healthy site.

## Inputs
User: "This is not good enough... we need better income streams." Reviewed the existing handoff guidance plan, dated income entries, site AGENTS.md, website overview, Vehicle, Location and What's For Lunch package READMEs, and the completed Cloudflare beacon report. Earlier constraints were $0 spending and no user work; an optional question about retaining them is pending. Payment processing remains deferred.

## Branch
Assessment only in Builder main. Site inspection used existing isolated codex/handoff-guidance-20261003; no site edits. Preserve unrelated gradlew.bat changes. Reinspect origin/main and feature ownership before any implementation.

## Non-Goals
No paid account creation, outreach, advertising enrollment, payment setup, new public offer, production deployment, or promise of passive revenue in this phase.

## Assumptions
Retain earlier spending and user-work constraints until changed. Automation can reduce work but does not remove software maintenance or customer support. Competitor offers establish alternatives and price references, not willingness to buy our product. No verified site traffic, qualified leads or sales are available in the inspected evidence. A functioning analytics beacon is not audience evidence.

## Open Questions
Are the earlier constraints retained? Can an inbound demonstration attract qualified agencies without paid acquisition? Is there a sufficiently valuable gap in their current release reporting? What support and distribution can be sustained? These remain business uncertainties, not grounds to invent projections.

## Opportunity Assessment

| Priority | Buyer and paid outcome | Price experiment, not valuation | Evidence and tradeoff |
| --- | --- | --- | --- |
| 1 | Small web agencies: compare a client site before and after a release, identify broken agreed routes/assets and unexpected metadata changes, export an understandable client report | Test $29/month for a bounded agency plan after useful repeat use; consider a local downloadable license first under zero infrastructure budget | Existing delivery work demonstrates relevant technical experience. [Checkly](https://www.checklyhq.com/pricing/) has a free tier and Starter at $24/month billed annually; [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/pricing/) offers free crawling up to 500 URLs. A generic uptime/link checker is therefore a weak differentiation. Test release comparison and client reporting specifically. No evidence yet that agencies want our version. |
| 2 | Java/Spring teams running on Windows: a narrowly scoped, independently reproducible deployment/recovery package with checks and documentation | Test $99-199 per downloadable version, without lifetime updates or custom deployment promises | [Bootify](https://bootify.io/pricing.html) offers a free generator, Professional $15 for one project/month or $120/year. A generic starter is also weak. Windows deployment/recovery is a narrower possible gap suggested by our own difficulties, not proven customer demand. Our personal application/deployer cannot simply be relabeled and sold; remove personal configuration, inspect licensing, reproduce from a clean environment and define support first. |
| 3, conditional | Restaurants in actual WFL coverage: clearly labeled local sponsor inventory measured by impressions and outbound clicks | No responsible price until local audience and placement performance are measured | Site supports Austin, Bay Area, New Orleans and Dallas restaurant discovery. No verified local audience or advertiser is established. Existing ratings and approval-weighted picks must remain independent of payment. Sponsorship needs sales/contract/moderation work, so it does not currently fit zero owner work. |

Do not treat the existing ZIP/VIN interfaces as defensible paid products just because they exist. ZIP lookup uses bundled Census ZCTA points rather than full address geocoding; VIN decoding uses [NHTSA vPIC](https://vpic.nhtsa.dot.gov/api/). [Geoapify](https://www.geoapify.com/pricing/) offers 3,000 credits/day on a free commercial tier with attribution. Any paid data product would need meaningful workflow improvements, rights review and sustainable service operation beyond a thin wrapper.

## Task Breakdown

### Task 1 - Record and review the opportunity decision
Dependencies: None.
Files: This new plan; docs/session-memory/2026-10-03-christopherbell-dev.md; their existing folder indexes.
Symbols: Opportunity Assessment, Demand Experiment, Constraints and Outcomes.
Inspection: Builder main e0fb31a and the inspected source/readmes and prior evidence listed above; current primary vendor pages on 2026-10-03.
Behavior: Preserve an honest ranked proposal and the missing evidence so later work targets a paid outcome.
Invariants: No sales or validated demand claims; no spending, outreach or runtime changes.
Boundary/API: Documentation only; prices are hypotheses, not public commitments.
Effects and failures: Publish selected Builder documentation; failed push remains incomplete. Preserve all historical records.
Tests and evidence: Structural plan validation, semantic assessment review, exact diff inspection and publication readback. Vendor sources prove only their stated offers.
Verification: Builder plan validator, hub refresh and exact-file publication helper; git status/log readback.

## Demand Experiment
Recommended next experiment: a small release comparison demonstration, first against our own site, producing a report that separates observed changes, failures and untested behavior. Avoid building multi-tenant scheduling, subscriptions or a broad crawler first.

The eventual implementation plan must specify inspected code boundaries and safe URL fetching: owned or authorized targets, bounded requests/body sizes, redirects and DNS destinations checked against private networks, no credentials or state-changing requests, and clear incomplete-run reporting. A local runner reduces hosted fetch risk and infrastructure costs but requires a supported installation experience.

Use a truthful sample and price hypothesis for inbound discovery. Measure qualified use separately from page views. Before a full subscription build, seek independent agency repeat use on their own authorized releases and explicit willingness to pay at the proposed price; a practical decision gate is three independent repeat users, at least two explicitly expressing purchase intent. These are experiment thresholds, not statistical proof or revenue. Do not contact prospects without authorization. If inbound distribution produces no qualified users, investigate distribution rather than manufacture more features or conclude the market has rejected the product.

## Code Changes
None in this assessment. A separate inspected implementation contract is required before developing the demonstration.

## Files and Modules
Builder assessment and dated session record only. Site Vehicle, Location and WFL documentation supplied asset evidence; no site source is changed.

## Unit Testing
Not applicable to documentation-only assessment; no application tests run.

## Local Testing
No application runtime changes or new runtime claims. Reuse the existing production proof only as historical delivery evidence, not buyer validation.

## Validation
Review for unsupported demand, false price precision and hidden owner-work requirements; validate document structure and inspected paths. Do not mark ready-for-execution while the future prototype lacks an inspected code contract.

## Rollback or Recovery
Documentation can be corrected with a follow-up entry/commit. No production rollback is needed because production is unchanged.

## Risks
Acquisition may be the main constraint. A recurring software offer requires support and maintenance. Existing free/paid competitors substantially overlap generic checks. A Windows-only deployment niche may be too small. Restaurant sponsorship cannot be priced responsibly without audience proof. Zero spending and zero owner work make service businesses and managed hosting poor fits.

## Completion Criteria
This assessment is complete when the ranked alternatives, sources, constraints and next demand experiment are published and explained. It does not complete the user's broader income ambition or establish a revenue stream. Future product implementation and sales remain unproven.
