# Generic Local Application Verification

## Document Status
ready-for-execution

## Plan Format
task-contract-v1

## Objective
Generalize verify-local-spring-app into verify-local-app and require actual local execution of the changed application before creating its PR, regardless of language or framework.

## Goals
- Cover web, desktop, CLI, library consumers and background applications using repository-native commands.
- Make local verification precede draft and ready PR creation, with current evidence after relevant candidate changes.
- Preserve production safety, data isolation, cleanup and existing deployment authorization boundaries.
- Align active policy, callers, metadata, discovery and planning guidance.

## Inputs
- User request to generalize the skill for any change and language and explicitly run the application locally before a PR.
- Inspected AGENTS.md, README.md, current skill and metadata, complete-builder-work, record-runtime-verification, plan/review references and SkillDiscoveryTests on clean Builder main at 89efc43403a0726871618efb7867db671613c3c5.
- Current dated Builder memory confirms write-chris-street-style-code is the actual style skill; older external memory identifier is stale.

## Branch
Builder main, origin https://github.com/azurras/builder.git, through the exact-file publication helper. No spoke or application changes.

## Non-Goals
- Application implementation, startup or production deployment for this documentation change.
- Language-specific launch command catalogs or a new runtime runner.
- Rewriting historical completed plans or earlier dated session records.

## Assumptions
- Repositories provide or can establish an appropriate local executable entrypoint.
- Changes without executable runtime use native validation and a recorded reason local application execution does not apply.

## Open Questions
None; routine naming and routing choices are within the authorized scope.

## Task Breakdown

### Task 1 - Generalize verification and align active workflow
Dependencies: None.
Files: .agents/skills/verify-local-spring-app/SKILL.md and agents/openai.yaml move to .agents/skills/verify-local-app; AGENTS.md; README.md; .agents/skills/complete-builder-work/SKILL.md; .agents/skills/record-runtime-verification/SKILL.md; .agents/skills/plan-builder-work/references/plan.md and review.md; .agents/tests/test_skill_consolidation.py.
Symbols: Skill identifier/frontmatter, interface metadata, pre-PR gate, preflight, candidate verification, deployment section, runtime policy, plan readiness and SkillDiscoveryTests expected catalog.
Inspection: Read each listed target and its current caller/test contract on clean main; origin/main has been fetched and no outgoing commits exist.
Required skill: write-chris-street-style-code.
Behavior: Any application change is exercised on the local machine using native tooling before PR creation; framework-independent readiness and changed-behavior evidence replace Spring-only discovery.
Invariants: Preserve production listeners, verified test-data permissions, explicit deployment authority, owned-process cleanup, truthful evidence and three-folder dated-document conventions.
Boundary/API: Rename canonical skill to verify-local-app, update active callers and discovery metadata, and preserve historical prose identifiers as historical evidence.
Effects and failures: Skill/document/test catalog edits and authorized Builder publication only; failed or unavailable local execution blocks application PR creation rather than shifting proof to CI. Documentation-only work records its runtime exemption.
Tests and evidence: Read-only baseline and revised behavioral scenarios across Node, Python, Rust, Spring and docs-only cases; existing discovery, artifact and full native Builder checks; official skill validation and semantic diff review.
Verification: python -B -m unittest discover -s .agents/tests; python C:/Users/Christopher/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/verify-local-app; maintain-builder-hub refresh; git diff --check; inspect active references and publication readback.

## Code Changes
Only the existing discovery catalog fixture changes executable Python. Skill instructions use repository-native run/build/test commands without prescribing a language or universal HTTP readiness signal.

## Files and Modules
Task 1 lists inspected edit targets. This plan, three generated indexes as needed, and docs/session-memory/2026-10-04-builder.md carry planning and verified delivery evidence.

## Unit Testing
Run existing Builder unittest discovery; the catalog test verifies real skill folder/entrypoint/metadata discovery and linked resources. Do not add prose-matching tests.

## Local Testing
No application runtime exists in this change: these are skill/policy documents, metadata and a discovery fixture. Execute actual native Python helpers and tests. Evaluate the skill's decisions with read-only scenarios; do not launch unrelated production applications to validate documentation.

## Validation
Official skill validation, native tests, hub/schema/link checks and semantic review must pass. Verify that neither a passing build nor CI nor a draft PR bypasses required local execution, and that non-HTTP applications have an appropriate readiness/output check.

## Rollback or Recovery
Restore the prior skill paths/content and active callers together through a reviewed follow-up commit. Preserve any successful checkpoint commit if pushing fails and recover using push-only after inspecting outgoing commits.

## Risks
- Broad language support can accidentally dilute isolation rules; keep actual resource/permission checks explicit and qualify Builder-specific test database policy.
- A rename can leave stale callers; scan active policies and metadata and retain historical prose without pretending it is current guidance.
- No executable application exists for docs-only changes; require a concrete exemption and native checks rather than unrelated startup.

## Completion Criteria
- Plan reviewed, structurally validated and published before implementation.
- Generic skill, active callers, metadata and discovery agree; local candidate verification explicitly precedes PR creation.
- Appropriate native and behavioral checks pass; runtime non-applicability and verified results are recorded in dated Builder memory.
- Exact reviewed delivery files are committed and pushed to origin main, with remote readback matching HEAD. No source issue or external closure applies.
