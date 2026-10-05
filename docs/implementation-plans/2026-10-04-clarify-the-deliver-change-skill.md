# Clarify the Deliver-Change Skill

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
An agent that loads deliver-change can tell which steps the request covers, where it is in the flow, what proves each step is done, where each artifact is published, and what to do when blocked.

## Background
On 2026-10-04 the user asked whether deliver-change was too light for an agent to follow. A read of SKILL.md at `17ed180` found seven gaps:
- "Resume at the first incomplete gate" names no gates and gives no evidence that a gate is passed.
- "Publish" never says that plans, reports and memory always go to Builder, so an agent working in a spoke could commit them there.
- Step 1 uses "branch strategy" and "completion boundary" without defining them.
- Step 3 says "review the diff" and "appropriate checks" without naming write-chris-street-style-code review mode or the plan's Test Plan.
- Nothing says what to do on a failed push, a red check or missing evidence.
- Limited scopes (review, closure, inspection) are listed at the bottom, so an agent starts the full flow first; planning-only is not mentioned.
- The flow has no final report; only closure.md has one.
The user said "Let's fix it." The concurrent coverage-gaps change (`17ed180`) had already pointed steps 1 and 5 at the triage helper and publish-spoke-changes; this plan waited for it to land.

## Goals
- An agent chooses its scope before starting and stops where a limited request ends (AC-1).
- Each step ends with a Done line naming observable evidence, so resuming is a lookup (AC-2).
- Publication targets and step-level skill handoffs are explicit (AC-3).
- Blocked handling and the final report are defined (AC-4).
- Checks pass and the change is published (AC-5, AC-6).

## Non-Goals
- No change to AGENTS.md policy. The skill restates where things go but AGENTS.md stays the owner; changing policy was not requested.
- No change to closure.md, coordination.md, repository-inspection.md or the scripts. They were not found unclear.
- No new tests that assert the skill's wording. write-chris-street-style-code says not to add tests that only echo documentation.
- No change to other skills' text. publish-spoke-changes already covers spoke Git steps in detail.

## Acceptance Criteria
- AC-1: SKILL.md opens with a scope table covering full delivery, plan only, review only (code and plan), spoke inspection/registration/snapshot, and close only, each with where it stops.
- AC-2: SKILL.md has seven numbered steps (scope, plan, implement, verify, publish, record, close), each ending with a `Done:` line naming evidence, and a Resume section defining stale evidence.
- AC-3: SKILL.md states that the plan, report and memory are always published to Builder through the phase finalizer, that Builder code uses publish-builder-changes and spoke code uses publish-spoke-changes, defines the default completion boundary, and names write-chris-street-style-code review mode, the plan's Test Plan, and save-session-memory at their steps.
- AC-4: SKILL.md has a When Blocked section (when to ask, which states are incomplete, set the plan blocked, record and report) and a Report section listing what to tell the user.
- AC-5: `python -B -m unittest discover -s .agents/tests` passes, `check_hub.py refresh --root .` passes, and `git diff --check` is clean.
- AC-6: This plan, the change and the dated memory are on origin/main, confirmed by `git ls-remote`.

## Inputs
- User requests in chat on 2026-10-04: "The deliver-change skill looks light. Does it need more detail..." and "Let's fix it".
- Inspected on Builder `main` at `17ed180`, clean tree: deliver-change SKILL.md, agents/openai.yaml and references closure.md, coordination.md, repository-inspection.md; publish-builder-changes SKILL.md and phase-finalization.md; publish-spoke-changes SKILL.md; write-implementation-plan SKILL.md and references plan.md, update.md, review.md; write-chris-street-style-code Review Mode; verify-local-app preflight; AGENTS.md; README skills table; tests referencing deliver-change (test_skill_consolidation.py, test_spoke_registry.py, test_github_trust.py), none of which check SKILL.md wording.

## Branch
Builder primary checkout `main` at `17ed180`; publish the exact task files through publish-builder-changes.

## Assumptions
- No test or validator reads deliver-change SKILL.md text beyond frontmatter and links (confirmed by search; the hub check validates frontmatter and links).

## Open Questions
None.

## Design
Restructure SKILL.md into: scope table, Resume, Where Things Are Published, seven steps each with a Done line, When Blocked, Report. Splitting closure out as step 7 makes its evidence separate from recording. The Done lines replace the unnamed "gates" so the resume rule has something to look up.
Alternative rejected: a separate gate table alongside the steps. Two lists would drift; one Done line per step keeps action and evidence together.
Alternative rejected: move the detail into a new reference file. The skill is the entry point an agent always loads; this detail is needed on every delivery, so it belongs there. The file grows from about 20 to about 60 lines.

## Expected Changes
- `.agents/skills/deliver-change/SKILL.md`: restructured as described; existing content (triage helper, publish-spoke-changes, coordination and inspection links) kept.
- This plan, today's Builder memory and regenerated indexes.

## Task Breakdown

### Task 1 - Restructure deliver-change SKILL.md
Dependencies: Published reviewed plan.
Files: .agents/skills/deliver-change/SKILL.md.
Symbols: headings Choose the Scope, Resume, Where Things Are Published, Steps, When Blocked, Report.
Inspection: Read SKILL.md and the inputs above at `17ed180`.
Behavior: Same flow and policy as before, with scope selection first, Done evidence per step, publication targets, blocked handling and a final report.
Invariants: Frontmatter name and description unchanged; every existing link and helper command kept; no machine paths; consistent with AGENTS.md.
Boundary/API: Skill text only; no script or name change.
Effects and failures: None at runtime.
Tests and evidence: Hub check for frontmatter and links; full suite; read-through that a reader can choose the action for each scope.
Verification: check_hub.py refresh --root .; python -B -m unittest discover -s .agents/tests; git diff --check.

### Task 2 - Record and publish verified delivery
Dependencies: Task 1 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day memory and the phase finalizer at `17ed180`.
Behavior: Completed change and evidence on origin/main.
Invariants: Only selected files committed.
Boundary/API: publish-builder-changes helper.
Effects and failures: Scoped commit and push; a failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run, then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Builder is not a runnable application, so verify-local-app does not apply; the change is skill documentation.
- AC-1, AC-2, AC-3, AC-4: read the final SKILL.md against each criterion and confirm every existing link and command survives (`git diff` review); hub check validates frontmatter and links.
- AC-5: full suite, `check_hub.py refresh --root .`, `git diff --check`.
- AC-6: helper output and `git ls-remote origin refs/heads/main` against local HEAD.

## Rollback or Recovery
Revert the change commit; the skill returns to the `17ed180` text. If a push fails, keep the commit and recover with `--push-only`.

## Risks
- Restated publication rules drift from AGENTS.md. Mitigation: state only targets and owners, link the finalizer, leave policy in AGENTS.md. Likelihood: low.
- A concurrent session edits the same file. Mitigation: confirm a clean tree before editing and before publishing.

## Implementation Log
No entries yet.

## Outcome
- AC-1: met. SKILL.md opens with Choose the Scope covering full delivery, plan only, review only (code and plan), spoke locate/clone/register/inspect/snapshot, and close only, each with its stopping point.
- AC-2: met. Seven steps (scope, plan, implement, verify, publish, record, close) each end with a `Done:` line; Resume defines stale evidence.
- AC-3: met. Where Things Are Published sends the plan, report and memory to Builder through the phase finalizer, Builder code through publish-builder-changes and spoke code through publish-spoke-changes. Step 1 defines the default completion boundary; steps 3 and 6 name the Test Plan, write-chris-street-style-code review mode and save-session-memory.
- AC-4: met. When Blocked and Report sections added.
- AC-5: met. 92 tests pass, `check_hub.py refresh --root .` passes, `git diff --check` is clean.
- AC-6: met by the delivery commit, confirmed with `git ls-remote` (recorded in the 2026-10-04 Builder memory).
- Shipped as planned. The plan was published at `02be182`. Follow-ups: none.
