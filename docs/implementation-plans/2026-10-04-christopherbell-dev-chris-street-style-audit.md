# christopherbell.dev Chris Street Style Audit

## Document Status
in-progress

## Plan Format
task-contract-v1

## Objective
Review and correct all tracked first-party executable code for the website against the Builder Chris Street Style standard, then leave local agent guidance aligned so future website code receives the same review.

## Goals
- Review Java and tests in `website` and `cbell-lib`, browser JavaScript and tests, Thymeleaf/HTML, CSS, executable configuration, Gradle, GitHub Actions, and website-owned PowerShell/command scripts.
- Make only evidence-backed corrections: meaningful names, cohesive responsibilities, valid states and boundaries, explicit effects, causal failure handling, consistent APIs, and risk-appropriate tests.
- Preserve established behavior, public contracts, security boundaries, feature ownership, persistence compatibility, and production operations.
- Add concise, repository-local coding guidance to the website `AGENTS.md` so future work follows this standard.

## Inputs
- Website `origin/main` at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`, freshly checked out in `A:\Projects\christopherbell.dev-worktrees\chris-street-style-codebase-20261004` on 2026-10-04. Draft PR #1477 is explicitly excluded as a source of code or verification.
- `AGENTS.md`, root and module READMEs, Gradle build files, JavaScript/CSS ownership READMEs.
- Builder `.agents/skills/write-chris-street-style-code/SKILL.md` and its Java, JavaScript, API/design, configuration, and testing references.
- Fresh inventory: 1,421 tracked first-party files with code-bearing extensions across website, shared library, operational tooling, and CI/build configuration; see the final audit record for the extension counts and reviewed groups.

## Branch
Use `codex/chris-street-style-codebase-20261004`, created from the fetched website `origin/main` at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`. Keep the dirty authoritative checkout at `A:\Projects\christopherbell.dev` and the separate draft PR worktree untouched.

## Non-Goals
- Add or change product features, routes, API payloads, database schemas, deployment semantics, or external side effects.
- Add frontend frameworks, npm packages, transpilers, or a new build pipeline.
- Reformat files wholesale or make subjective style changes without a concrete standard or readability/contract benefit.
- Modify historical design documents, binary/media files, imported datasets, vendored code, or generated build output unless an executable source contract directly requires it.
- Change production data or manually rotate/restart production services.

## Assumptions
- The requested standard is the Builder Chris Street Style skill, adapted to repository-native Java, JavaScript, templates/configuration, CSS, Gradle, and PowerShell conventions.
- Preserve current externally visible behavior. If an apparent style correction requires a behavior or contract change, do not silently include it; document the evidence and keep the correction out of this scope unless the existing behavior is demonstrably invalid under the named standard.
- Repository CI and the supported deployment flow remain authoritative for publication and runtime activation.

## Open Questions
None. Resolve ordinary naming, cohesion, and test-boundary decisions from the existing feature READMEs and neighboring code.

## Task Breakdown

### Task 1 - Review and correct Java application, library, and tests
- Dependencies: None.
- Required skill: write-chris-street-style-code.
- Files: `website/src/main/java`, `website/src/test/java`, `cbell-lib/src/main/java`, `cbell-lib/src/test`, and `cbell-lib/src/testFixtures`; update owning package READMEs only when ownership or documented behavior changes. Inspected repository guides: `AGENTS.md`, root `README.md`, `website/src/main/java/dev/christopherbell/README.md`, `cbell-lib/README.md`, root/module Gradle build files.
- Symbols: Tracked Java types and methods in the listed source roots; prioritize public boundaries, feature services/controllers, repositories, async/concurrency owners, exception translation, and state constructors.
- Inspection: Clean audit worktree at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`; root instructions, architecture guidance, module guidance and build configuration inspected. Read each owning feature README and its callers/tests before editing that feature.
- Behavior: Preserve observable business, HTTP, database, security, ordering, timeout, and serialization behavior except where a correction is required to uphold an existing documented invariant.
- Invariants: Feature-first package ownership, published Modulith APIs, repository boundaries, constructor injection, Mongo compatibility, explicit transaction/task ownership, interruption propagation, and existing auth checks remain intact.
- Boundary/API: Keep route, DTO, library, module and persisted-document contracts compatible; pass per-operation data explicitly and keep absence, domain rejection, programming defects and infrastructure failure distinct.
- Effects and failures: Retain current I/O and side-effect owners; catch only to recover or translate, preserve causes, redact secrets, and do not turn infrastructure failures into success-shaped values.
- Tests and evidence: Capture clean baseline results before edits. Add or amend focused tests only for changed behavior or invariants; use characterization evidence for behavior-preserving refactors. Every independent correction must first have its own reviewed, published implementation plan, then its own test report naming the exact candidate commit with focused native checks and local application runtime proof. Run full native checks after all code changes.
- Verification: `./gradlew.bat :website:check :cbell-lib:check`; inspect test failures and reports. If any website runtime behavior/configuration changes, also use an isolated packaged candidate and produce the required runtime report.

### Task 2 - Review browser JavaScript and tests
- Dependencies: Task 1 may proceed independently; consolidate final checks in Task 5.
- Required skill: write-chris-street-style-code.
- Files: `website/src/main/resources/static/js`, `website/src/test/js`, and any executable service-worker JavaScript under website resources. Inspected `website/src/main/resources/static/js/README.md`, root `AGENTS.md`, and the Gradle JavaScript test task.
- Symbols: Tracked ES modules, web components, service workers, tests, event handlers, fetch/promise flows, DOM rendering, timers and subscriptions.
- Inspection: `origin/main` baseline `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`; shared/page ownership conventions and native test wiring inspected. Read nearby module/test contracts before each edit.
- Behavior: Preserve page behavior, API paths, event ordering, navigation, focus/accessibility state, and existing browser support.
- Invariants: Validate untrusted runtime data; keep null meanings stable; await/own promises; prevent stale responses; clean up listeners/timers; use context-safe DOM, URL and HTML rendering.
- Boundary/API: Preserve exported module shapes, endpoint contracts, selectors used by templates, and shared/page ownership.
- Effects and failures: Keep network, clipboard, storage and browser APIs explicit; report failures through current UI conventions and do not swallow rejected work.
- Tests and evidence: Establish the existing browser test baseline; extend focused tests only when a rule or behavior changes. Run syntax checks for all tracked JavaScript and `:website:jsTest`. Each independent correction receives its own plan and commit-specific test report.
- Verification: `node --check` for every tracked first-party `.js` file under website, then `./gradlew.bat :website:jsTest`; browser/runtime proof is required if rendered or interaction behavior changes.

### Task 3 - Review templates, styles, and application configuration
- Dependencies: Tasks 1-2 may proceed independently; consolidate final checks in Task 5.
- Required skill: write-chris-street-style-code.
- Files: `website/src/main/resources/templates`, `website/src/main/resources/static/css`, `website/src/main/resources/application*.yml`, and code-bearing static/resource configuration. Inspected `website/src/main/resources/static/css/README.md`, `AGENTS.md`, root README, and `website/build.gradle.kts` resource processing.
- Symbols: Template fragments/pages, Thymeleaf expressions, CSS selectors/media rules, configuration keys, and resource-rendering logic.
- Inspection: Clean baseline at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`; template/config ownership and stylesheet contracts inspected. Trace every edited selector/config key to its consumers and tests.
- Behavior: Preserve page routes, rendered content, responsive behavior, accessibility, security attributes, configuration defaults/precedence, and static asset fingerprints.
- Invariants: Escape for the actual output context, keep shared class contracts stable, fail clearly for missing required security/production configuration, and avoid unscoped CSS/config fallbacks.
- Boundary/API: Template model names, shared fragments, CSS classes consumed by JS/templates, and supported profile/property names remain compatible.
- Effects and failures: Keep rendering/configuration deterministic; do not add implicit external calls or unsafe fallback values.
- Tests and evidence: Use relevant rendered/template/controller tests and configuration validators. Review all changed snapshots/output semantically. Run the full native checks in Task 5. Each independent correction receives its own plan and commit-specific test report.
- Verification: `./gradlew.bat :website:check`; verify rendered/interactive browser behavior and write a runtime report if any browser behavior or application configuration changes.

### Task 4 - Review operational scripts, Gradle, and CI configuration
- Dependencies: Tasks 1-3 may proceed independently; consolidate final checks in Task 5.
- Required skill: write-chris-street-style-code.
- Files: tracked first-party `ops/production/windows/**/*.ps1`, `.psm1`, root and module `*.gradle.kts`, `prod.cmd`, `gradlew.bat`, `.github/workflows/*.yml`, and code-bearing Compose/configuration files. Inspected Gradle build/task wiring and repository worktree/build guidance.
- Symbols: Script entrypoints/functions/modules, command argument parsing, process/file/service/database effects, workflow jobs/steps, and Gradle task/provider/configuration declarations.
- Inspection: Clean audit worktree at `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`; inspect each script's module tests and relevant operational runbook before any edit.
- Behavior: Preserve command syntax, exit codes, output contracts, service ownership, privilege boundaries, dry-run behavior, CI protection gates, and rollback paths.
- Invariants: Validate inputs at boundaries, make mutation and privilege explicit, bound waits/retries, preserve causal errors, avoid secret disclosure and command-string execution.
- Boundary/API: Keep task names, CLI switches, result records, service/API contracts, and workflow trigger/permission contracts compatible.
- Effects and failures: No live production maintenance. Test against disposable or `test` resources; retain tested rollback/recovery for any executable operational change.
- Tests and evidence: Use the repository's Pester/Gradle tests and native PowerShell parsing/analysis where available; run only scope-relevant checks while editing and full gates in Task 5. Each independent correction receives its own plan and commit-specific test report.
- Verification: Run `./gradlew.bat :website:check :cbell-lib:check` and the relevant Pester suites; inspect workflow/script diffs and `git diff --check`. Any production operation/configuration change requires the documented safe runtime proof and report.

### Task 5 - Complete the whole-code audit and deliver verified results
- Dependencies: Tasks 1-4.
- Required skill: write-chris-street-style-code.
- Files: All in-scope tracked source, tests, configuration and executable scripts; website `AGENTS.md` coding guidance; implementation plan, runtime report if required, and dated Builder session memory.
- Symbols: Every in-scope file from the re-counted manifest and all changed public/internal boundaries.
- Inspection: Reconfirm source commit and manifest; semantically review the complete diff against the plan, callers, tests, security boundaries, compatibility and native outputs.
- Behavior: No unintended user-visible, persistence, operational or CI behavior changes.
- Invariants: No in-scope style blocker remains; each accepted warning has a concrete reason and does not violate the standard; all repo-native required gates pass.
- Boundary/API: CI, PR, deployment and reporting follow the current Builder/website instructions; no dirty authoritative checkout is overwritten.
- Effects and failures: Publish reviewed, focused PR(s), wait for required CI, resolve in-scope failures, merge after gates pass, and verify automatic production activation through supported status/evidence. Do not manually restart or rotate production.
- Tests and evidence: Full `:website:check` and `:cbell-lib:check`, JavaScript syntax and tests, relevant PowerShell tests, diff/semantic review; every independent correction has a separately reviewed and published plan and a separately saved test report naming the commit exercised. Candidate startup and a representative application flow are required for every report before PR creation or update.
- Verification: All changed files pass `git diff --check`; each correction has a distinct plan/report pair; full required checks and PR CI are green; merged revision and supported deployment/runtime state are read back; publish the verified dated delivery memory before any external closure. Do not update or merge draft PR #1477 based on its prior contents or checks.

## Code Changes
- Add a concise Chris Street Style section to the website `AGENTS.md`, adapted to repository languages and native conventions.
- Apply only specific code corrections supported by the standard and inspected contracts across the reviewed scope.
- Update feature documentation only when a corrected ownership or behavior contract requires it; record the full inventory/review outcome in the dated Builder session memory, not a new permanent dashboard.

## Files and Modules
- `AGENTS.md`, `website/src/main/java`, `website/src/test/java`, `website/src/main/resources/static/js`, `website/src/test/js`, `website/src/main/resources/templates`, `website/src/main/resources/static/css`, `website/src/main/resources/application*.yml`, `cbell-lib/src`, `ops/production/windows`, root/module Gradle scripts, `.github/workflows`, and code-bearing root configuration.
- Excluded: unchanged binary/media assets, vendored/generated output, imports/data-only files, and historical docs.

## Unit Testing
- Run the pre-edit baseline for `:website:check` and `:cbell-lib:check` before implementation.
- Add no broad rewrite-only tests. Add focused tests where a style correction changes or clarifies a testable contract; prefer existing public behavior boundaries.
- Run native tests for each changed area, then the full module checks at the final gate.

## Local Testing
- Run in the clean audit worktree from the repository root; verify test database configuration is `test` before any Mongo-backed tests.
- Run Node syntax checks and the built-in JS test task; run applicable Pester suites through Gradle/native PowerShell.
- If runtime behavior/configuration changes, build and exercise an isolated packaged candidate using only isolated ports and MongoDB `test`; record actual inputs, outputs and state in a test report. No production DB writes or manual service actions.

## Validation
- Re-count all in-scope tracked code files and account for each reviewed source group.
- Review each source/test/config group against Chris Street Style and local feature contracts; inspect the full diff and causes of findings.
- Run `git diff --check`, required Gradle/JS/Pester gates, PR checks and deployment readback.
- Confirm website `AGENTS.md` describes the adapted standard without conflicting with existing project rules.

## Rollback or Recovery
- Keep changes in the isolated branch and use focused commits/PRs. Before merge, revert or correct the isolated change if checks or candidate proof fail.
- After merge, use a reviewed revert PR and the supported automatic deployment mechanism if a regression is confirmed; preserve production/data state and all audit evidence.
- Keep the dirty canonical checkout and its unrelated files intact throughout.

## Risks
- The scope spans 1,421 tracked files and multiple runtime/operations boundaries; mechanical bulk formatting could obscure behavior, so only evidence-backed narrow edits are allowed.
- A semantic review can find valid design concerns outside style scope; keep unrelated feature changes out and record them separately if needed.
- A style fix that changes browser behavior, configuration, persistence or operations expands verification needs and must meet the corresponding runtime/recovery gate.
- Current production is a native Windows host; candidate proof must use isolated ports, the `test` database and the supported deployment observer.

## Completion Criteria
- All in-scope tracked files have been covered by the source-group inventory/review, and the website agent guide captures the adapted standard for future changes.
- All confirmed in-scope style violations are corrected with focused diffs and appropriate regression evidence; no unsupported blanket refactor remains.
- Full module tests, JavaScript syntax/tests, relevant PowerShell checks, semantic diff review and required CI pass.
- Every code correction has a separately published implementation plan and candidate-specific test report with local runtime evidence; this is an application repository, so startup is required even when an individual change appears behavior-preserving.
- Required PR(s) are merged and supported deployment is read back; dated session memory and Builder publication are complete.

## Implementation Log

### 2026-10-04 - Restart audit from current main

- **Change:** Restarted the audit in a new clean worktree at current `origin/main` commit `76681a5ca5abd418e8ab5dc4f166a0da8563bb9b`; the worktree for draft PR #1477 is not used as a source of code or verification.
- **Reason:** The user instructed not to trust that draft because it predates extensive code-style changes, and the current standard requires sentence-like names and precise argument roles.
- **Impact:** Branch and Inputs now identify the fresh audit baseline. Each confirmed independent code correction must have its own reviewed and published implementation plan and its own test report before PR creation or update; no correction is inferred from the draft PR.

### 2026-10-04 - Correct source inventory count

- **Change:** Corrected the first-party code-bearing inventory from 1,418 to 1,421 tracked files after adding two `.properties` files and one `.toml` file to the extension count.
- **Reason:** The initial recount omitted code-bearing configuration extensions, so its total understated the audit scope.
- **Impact:** Inputs and whole-code coverage criteria use 1,421 files; no code scope or acceptance criterion changed.

### 2026-10-04 - Deliver interruption correction and continue the audit

- **Change:** Completed the first independent correction: bounded process-output readers now propagate interruption; PR #1478 merged as `695a3ed8617f9b4ab07abb7413baf369c58acf6`, all CI passed, and automatic production status confirmed that SHA active and healthy. Its plan and candidate report are separate records. Published the next focused provider-failure plan before editing.
- **Reason:** Continue the audit from the fresh main-based branch while preserving the requested per-correction plan and report evidence; PR #1477 remains excluded.
- **Impact:** The interruption correction is closed; the whole-codebase audit remains in progress, with Java provider future handling as the next reviewed task.
