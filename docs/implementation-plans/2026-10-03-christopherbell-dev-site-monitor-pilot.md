# Agency website monitor pilot

## Document Status
in-progress

## Plan Format
task-contract-v1

## Objective
Deliver one usable recurring product: private website baseline checks and client reports for small web agencies. User approved moving forward after the product description. Use existing application accounts and supported deployment; payments remain deferred.

## Goals
Allow a signed-in customer to add a verified public HTTPS site, choose up to five pages, capture an explicit healthy baseline, run bounded repeat checks and review/export results. Run due checks daily, preserve ten reports per site, and provide a usable demonstration against our own site. Start a capped free pilot with proposed future $29/month pricing clearly described as unvalidated and unavailable for purchase.

## Inputs
Approved product description; [opportunity assessment](2026-10-03-christopherbell-dev-stronger-income-experiments.md); site main8d7e85e2; inspected AGENTS.md, README, account/permission, preview destination/transport, kind-scoped persistence/frozen manifest, lease coordinator, native view/frontend and architecture rules. Current Reactor Netty and jsoup API documentation was consulted. Builder planning, coding and delivery skills apply. Existing user autonomy rules supersede routine extra design approval pauses and require one Builder plan rather than separate specs.

## Branch
Reuse isolated A:/Projects/christopherbell.dev-worktrees/blog-placeholder-cleanup-20261003 on codex/site-monitor-pilot-20261003 from origin/main. Preserve unrelated gradlew.bat. Builder artifacts on main.

## Non-Goals
Checkout, billing, new external accounts, paid infrastructure, prospect outreach, email delivery, arbitrary crawling, browser transactions, screenshots, automatic repairs, client account sharing, uptime guarantees, lifetime updates and validated revenue claims.

## Assumptions
Retain zero spending and zero required owner labor. Running a maintained software service still requires future operational capacity. Signed-in beta users accept limitations before using it. Our own public site is an explicitly labeled demonstration, not proof of customer domain ownership. Initial alerts are report/dashboard indicators; email alerts require a subsequent delivery phase.

## Open Questions
Demand, sustainable acquisition, operating costs at scale and willingness to pay remain unverified. None prevents implementing the capped functional pilot. Existing declined local-browser/download permissions are respected; actual UI execution may remain a documented limitation.

## Task Breakdown

### Task 1 - Implement private bounded monitoring
Required skill: chris-street-style
Dependencies: Published reviewed plan.
Files: New website/src/main/java/dev/christopherbell/sitemonitor/{model,fetch,monitor,persistence,api}/ and README.md; inspected configuration/mongo/domain/DomainMongoOperationsFactory.java, DomainAccountDeletionStore.java; new account/api/MonitorAccountAccess.java; architecture/LegacyModuleDependencyRules.java; new sitemonitor tests and runtime-kind tests.
Symbols: Verified origin/page policy, DNS-pinned fetch, site snapshots/comparison, workspace repository, run service and daily scheduler, owner-only API; exact runtime-kind approval and account deletion cleanup.
Inspection: Read existing preview policy/transport, AccountRepository and PermissionService, kind-scoped factory/codec, immutable cutover manifest/ledger, LeaseService/coordinator, and architecture rules at main8d7e85e2. Add new explicit business area without expanding frozen cross-area violation baselines.
Behavior: Cap pilot at ten workspaces, five sites/account and five same-origin pages/site. Ownership uses a random token at a fixed well-known path and is rechecked before every capture/check. HTTPS443 only, no credentials/query/fragment, validated public DNS pinned for each connection, same-origin redirects only, no upstream credentials, bounded bodies/deadlines/assets and explicit incomplete results. A known fixed demonstration site supports proof without customer deployment. Baselines require complete healthy captures and change only explicitly. Reports separate repeated HTTP failures, observations and incomplete checks; retain ten/site. Manual cooldown and one fixed durable lease serialize all mutation/fetch work across instances. Due scheduler processes at most one site per minute, once per day. Deleted/inactive account state is not monitored and is cleaned up.
Invariants: Cross-account reads/writes/export are denied; mutation CSRF remains; no unrelated collection/schema migration/cutover digest changes; no raw HTML or secrets retained; bounded memory/storage/connections; old baseline survives failure; stop effects after lease loss.
Boundary/API: Protected /api/site-monitor/v1 endpoints with standard response envelopes, safe categorized errors, owner-scoped IDs and no-store. Expose only narrow published account/model contracts across modules. New fixed kind in application_runtime through existing namespaced/versioned operations; preserve historical manifest digest.
Effects and failures: GET/HEAD public authorized sites only; bounded pilot records persist through restart. Global lease contention/cooldown gives retry guidance. Storage outages fail explicitly. DNS/body/timeout/redirect failures become incomplete observations, not health claims. Versioned writes preserve concurrent data.
Tests and evidence: Regression-first tests for validation/SSRF/pinning/redirect/deadline/body limits, comparison, incomplete baseline rejection, owner isolation, capacity/cooldown, lease loss, scheduler due behavior and retention. Actual isolated Mongo checks for new-kind identity/version behavior and account cleanup. Architecture freeze must not grow.
Verification: Focused :website:test classes then required broader native/CI checks with inspected test-only Mongo target; actual candidate requests and report content.

### Task 2 - Deliver usable pilot UI and reports
Required skill: chris-street-style
Dependencies: Task 1 API contracts.
Files: Inspected view/tools/ToolsViewController.java, configuration/security/SecurityConfig.java, StaticAssetRequestMatcher.java, PublicMetadataController.java, static/js/lib/api.js, components/nav.js, templates/zip-coordinates.html and shared frontend helpers; new templates/site-monitor.html and static/js/site-monitor.js; owning README files; affected view/security/frontend tests.
Symbols: Public data-free /site-monitor page, account-aware dashboard, accessible setup/verification/baseline/check/delete/report controls, text report export, Tools navigation and canonical metadata.
Inspection: Existing Tools views, ViewControllerTest, exact public routes, shared fetchJson/status helpers, native modules and navigation patterns at main8d7e85e2.
Behavior: Explain recurring buyer value and exact beta limits; demonstrate real checks of our site. Customers can create/verify sites, capture baseline, run/check reports and remove their state. Show timestamps, coverage limits, failures and changes plainly; escape all remote text. Report download is owner-only. No checkout or claim that $29 is validated. Controls show waiting/error states and preserve input on failure.
Invariants: One h1, labeled inputs, keyboard-native controls, safe DOM text insertion, no public customer data, no misleading browser/form/security audit claims.
Boundary/API: Existing auth/CSRF helpers; protected feature APIs; only GET page public. Private report responses no-store and attachment text/plain, never remote HTML.
Effects and failures: UI mutations only after customer action; bounded errors surfaced accessibly. Automatic daily results appear in dashboard. Download/browser permission refusals remain respected.
Tests and evidence: Rendered view and security checks, JS syntax and native JS suite, candidate API lifecycle including demo, anonymous rejection, invalid/private URLs, baseline/check/report/remove, retained state across restart, and real controlled failure/change scenarios in isolated integration fixtures.
Verification: :website:test affected tests, :website:jsTest, bootJar and candidate actual HTTP proof; browser only when allowed. No permission workaround.

### Task 3 - Review, publish and verify delivery
Dependencies: Tasks 1 and 2 passing checks and candidate proof.
Files: This plan, new dated runtime report and session record, selected site changes and owning docs.
Symbols: Review findings, runtime evidence, CI/release identity, delivery outcome and limitations.
Inspection: Supported prod.cmd automatic main deployer and prior current production proof; inspect fresh status before merge. Existing Mongo manifest remains immutable.
Behavior: Obtain independent source review, fix findings, publish candidate report, create PR, wait for all required CI, merge guarded reviewed head, observe supported deployment and prove production readiness/public pilot shell/private API access boundary.
Invariants: Preserve service availability, no production fixtures, no elevated access or manual listener rotation, no sales claims. Do not retry refused browser actions.
Boundary/API: GitHub PR/CI, supported SYSTEM automatic deployer and public health/shell evidence.
Effects and failures: Publication and supported deployment only. Failed CI/push/deploy remains incomplete. Use established protected rollback rather than ad hoc operations.
Tests and evidence: Immutable diff review, targeted native results, runtime report with actual inputs/output/isolation/cleanup, all platform CI and fresh deployed SHA/health.
Verification: Builder validators/exact publisher, gh checks/merge readback, prod.cmd auto-status and actual production GETs.

## Code Changes
Add the isolated site-monitor feature and narrowly necessary shared integration points. No dependency upgrades or old cutover edits. Prefer existing Reactor Netty, jsoup, Mongo kind operations and lease primitives.

## Files and Modules
New sitemonitor business area with published model/API contracts; narrow account published facade; fixed runtime-kind extension in configuration; native tool view/frontend; existing security/navigation metadata and test ownership.

### Bounded persistence refinement
Inspection confirmed application_runtime has only its existing global identity index for this new kind. Use exactly ten fixed pilot workspace identities and direct indexed point reads rather than repeatedly scanning/counting unrelated runtime history. Each workspace stores a separate accountId and unique generation; slot selection and writes remain under the fixed durable lease. Saves and snapshot deletes atomically match accountId, generation and version so a stale worker cannot mutate a reused slot. One additional fixed scheduler identity stores the next permitted automatic attempt across instances. Account deletion publishes its durable marker and removes these identities while sharing the monitor lease; any started deletion blocks monitoring, including failed resumable jobs. This preserves the historical schema and avoids a new index/migration while enforcing the ten-account capacity at the storage identity boundary.

### Runtime-discovered static asset correction

Production listener evidence reproduced GET200 / HEAD403 for fingerprinted JavaScript and CSS. The real demo correctly produced INCOMPLETE and preserved the absence of a baseline. Permit HEAD only for the same public cacheable static resource paths already approved for GET, using the shared static matcher in both authorization and authentication bypass. Keep mutation methods and private namespaces protected. Add a failing matcher regression, a passing focused security check and actual candidate HEAD proof. Verify the real demo against the repaired production assets after the supported deployment, using only the isolated candidate account database.

## Unit Testing
User AGENTS.md requires appropriate native tests. Use smallest meaningful tests first and expand for shared security/persistence changes. Keep all database targets explicitly test; no database-backed execution without proving profile/URI first.

## Local Testing
Java25/Spring4.1 candidate on a free alternate Windows port, disposable Mongo test database on a separate port, scheduling/mail disabled except explicitly controlled scheduler calls in fixtures. Shared/media roots build-owned. Own processes/logs/artifact identity and cleanup. Honor previously refused browser/download permissions.

## Validation
Structural plan validation and semantic review before development. Exact diff review, native checks, runtime report and CI before merge. No unresolved important review findings or falsely broad success claims.

## Rollback or Recovery
Use supported automatic deployment/rollback to previous8d7e85e2 release if necessary. New runtime kind is additive and can remain dormant under older release; existing data/cutover digest untouched. Feature limits isolate resource use. No destructive collection changes. Stop only owned candidate processes.

## Risks
Demand remains unproven. Pilot is deliberately capped and requires customer DNS/hosting access to prove ownership. HTTP metadata checks do not prove rendered layout or business transactions. Ten reports/site is bounded history, not unlimited retention. Email alerts and billing are deferred and must be clearly stated. Additive runtime-kind extension needs regression proof without changing frozen cutover contracts.

## Completion Criteria
Working bounded pilot through verified production delivery, private saved state and report export, honest limits and repeat scheduling, published evidence and clean selected commits. This completes pilot delivery only; acquisition, paid conversion and a profitable revenue stream remain open business outcomes.
