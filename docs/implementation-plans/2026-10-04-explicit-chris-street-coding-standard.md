# Explicit Chris Street Coding Standard

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Expand write-chris-street-style-code into an explicit house standard, adapting Jane Street engineering and review principles across languages with concrete good and bad examples.

## Goals
- Give implementation and review actionable instructions, decision rules, evidence requirements, and completion checks.
- Require code to read like a sentence: receiver, method name, parameter names, and argument names convey one operation; variables describe their current data and distinct data meanings use distinct variables.
- Cover every language through a general adaptation procedure plus focused language references.
- Link original paired good/bad examples with reasons and executable examples checked in native runtimes.
- Retain the skill identifier, policy scope, read-only review boundary, existing Builder checkpoints, and repository-native tooling.

## Inputs
- User request and supplied Jane Street talk: https://www.janestreet.com/tech-talks/janestreet-code-review/.
- Inspected current SKILL.md, metadata, all six current references, SkillDiscoveryTests, plan validators, and Builder publication helpers at the current clean main checkout.
- Read historical e352536 skill entrypoint and reference structure to recover useful detail without reverting current authority or evidence rules.
- Consulted Jane Street primary articles on uniform interfaces, explicit failures, and expectation tests; concrete rules and examples are an original house adaptation.

## Branch
Builder main using commit-push-builder-main; publish the reviewed plan before implementation and the verified skill afterward under existing user publication authorization.

## Non-Goals
Application changes, deployment, third-party packages, replacing local formatters, or requiring OCaml, Iron, Emacs, or a new workflow system.

## Assumptions
Language-specific syntax is illustrative of universal contracts; supported compiler versions and language conventions come from each target repository. A linked adaptation guide handles unlisted languages.

## Open Questions
None; the requested scope and naming rules are explicit. Resolve routine example and document structure choices from inspected policy.

## Task Breakdown

### Task 1 - Specify the cross-language contract and naming rules
Dependencies: None; source and current skill inspection are complete.
Files: .agents/skills/write-chris-street-style-code/SKILL.md; agents/openai.yaml; new references/naming-and-readability.md; new references/language-adaptation.md; new references/sources-and-adaptation.md within the same skill folder.
Symbols: implementation and review modes; Before-Edit Brief; evidence matrix; mandatory rules; reference routing; naming and language adaptation procedures.
Inspection: Read current entrypoint and metadata, current language references, skill-creator guidance, historical e352536 entrypoint, and the linked Jane Street primary sources.
Required skill: write-chris-street-style-code before code-bearing examples or metadata edits.
Behavior: Future implementers and reviewers can select concrete required actions for naming, data transformation, boundaries, invariants, effects, failures, and review content in any language.
Invariants: Preserve authorization limits and repository conventions; naming rules are explicit house requirements; primary-source claims are attributed accurately; no claim of a complete official all-language Jane Street manual.
Boundary/API: Keep skill name and directory write-chris-street-style-code and implicit invocation enabled; link every new reference from a meaningful routing row.
Effects and failures: Only documentation and skill metadata change; ambiguous or unsafe designs are corrected within authorized scope; missing authority remains a real stopping condition.
Tests and evidence: Baseline read-only scenario assessment; review entrypoint/routing and new references against requirements; native discovery/link checks and skill validator afterward.
Verification: python -B .agents/tests/test_skill_consolidation.py SkillDiscoveryTests; skill-creator quick_validate.py; semantic reference review and stale-link scan.

### Task 2 - Add concrete design and evidence recipes with paired examples
Dependencies: Task 1 defines the rule and reference structure.
Files: references/design-and-api.md; references/testing-and-review.md; references/java.md; references/javascript.md; references/python.md; references/templates-and-configuration.md; new references/good-and-bad-examples.md within the skill folder.
Symbols: validation and state representation; failure taxonomy; mutable/effect ownership; compatibility; test selection; final-content review; paired examples and explanations.
Inspection: Read all current reference contents and their callers in SKILL.md; inspected native Python, Node, and JDK availability for executable example verification.
Required skill: write-chris-street-style-code before writing executable examples.
Behavior: Readers see bad code, its concrete failure, improved code, its preserved contract, and the evidence needed to approve it.
Invariants: Examples are original; runnable code is syntactically valid and handles documented boundaries; illustrative fragments are labeled; absence is distinct from protocol/infrastructure failure; units and resource ownership remain explicit.
Boundary/API: Language guides adapt the shared standard rather than invent conflicting local rules; the general guide supplies equivalents for unlisted languages.
Effects and failures: Example checks run in temporary files using native runtimes with no production state, external requests, or new dependencies.
Tests and evidence: Compile and exercise complete Python, JavaScript, and Java good examples, including invalid/boundary paths; independent scenario and semantic review after updates.
Verification: Run native Python and Node example checks and javac/java on the complete TimeWindow example; verify original paired examples and reviewer traceability.

### Task 3 - Validate and publish the expanded standard
Dependencies: Tasks 1 and 2 complete with verified examples and semantic review.
Files: reviewed skill files; docs/session-memory/2026-10-04-builder.md; generated docs indexes; this implementation plan status.
Symbols: validation outcomes; implementation completion criteria; dated delivery entry and publication evidence.
Inspection: Reinspect final diff, exact publication paths, staged ownership, origin/main and outgoing commits before invoking the checked-in publisher.
Behavior: The reviewed expanded skill, its metadata, references, and delivery record are published on origin main.
Invariants: Preserve unrelated changes; publish only exact task files and intended indexes; never force push; only report verification actually observed.
Boundary/API: Use Builder plan, memory, index, and selected-file commit helpers.
Effects and failures: GitHub commit/push under existing authorization; a failed push retains its commit and requires explicit push-only recovery after inspecting outgoing commits.
Tests and evidence: Discovery/link and skill validation, native example checks, review assessment, diff check, hub refresh, helper dry-run, push result and live remote readback.
Verification: maintain_builder_hub.py refresh --root .; git diff --check; selected-file helper dry-run and actual publication; git ls-remote origin refs/heads/main and clean task-state readback.

## Code Changes
Documentation and invocation metadata only, plus original code-bearing examples in references. No production implementation changes.

## Files and Modules
The single style-skill folder and its references; dated plan and Builder session memory; generated indexes at required checkpoints.

## Unit Testing
Reuse focused SkillDiscoveryTests; native example checks exercise outputs and rejected inputs. Add no phrase-matching tests that merely mirror the document text.

## Local Testing
Application runtime verification does not apply: these are repository instructions and isolated illustrative examples. Compile and run the self-contained examples in temporary directories.

## Validation
Acceptance requires explicit shared rules, sentence-like parameter/argument guidance, good/bad examples with explanations, coverage for unlisted languages, preserved read-only review limits, source attribution, valid reference links, valid metadata, and passing native example checks.

## Rollback or Recovery
Restore prior task files via a reviewed follow-up commit if the expanded guidance causes a demonstrated conflict. Preserve unrelated working state. Retain a successful local commit if push fails, then retry publication through the checked-in helper.

## Risks
Over-prescriptive naming could break public keyword-argument compatibility; require caller inspection and deliberate migrations. Language examples could imply universal syntax; label language-specific choices and use a general adaptation procedure. Mechanical validation cannot establish semantic quality; use independent scenarios and manual review.

## Completion Criteria
- All requirements in Goals are covered by explicit instructions and linked examples.
- Native executable examples and focused discovery checks pass.
- Semantic review has no unresolved actionable defect.
- Hub validation and diff check pass with only established historical schema warnings.
- Exact task files and dated delivery evidence are pushed and the live remote publication is verified.
