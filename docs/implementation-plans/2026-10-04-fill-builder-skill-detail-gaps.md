# Fill Builder Skill Detail Gaps

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
An agent following any of six Builder workflow skills can act without guessing: each skill states the formats, conventions and edge-case steps it relies on. Every rule that several skills share is owned and stated by one skill and referenced the same way by the others. All eight skills declare the same Codex invocation policy.

## Background
On 2026-10-04 the user asked which skills were light on detail. A read-only review of all eight skills, their references, metadata, helper arguments and the test-report validator found gaps in six skills, inconsistent `openai.yaml` metadata, and shared rules worded differently in three or four places. The user then asked to fix gaps 1 to 6, the metadata issue and the wording issue. Specific findings:
- save-session-memory: no entry shape or example, undefined `--time` format and "serialize same-file writes", no slug rule for a new project, no "when to write" or proposed-closure content.
- write-test-report: `references/example.md` is linked from nowhere; the candidate-SHA rule that the spoke preflight enforces is only in other skills; the validator's `complete` rules are undocumented; how to update a report after a rerun is ambiguous; status meanings are undefined.
- publish-spoke-changes: `<agent>` branch prefix shown only as `codex/`; merge method undefined beyond christopherbell.dev; no worktree location; nothing on missing required checks, trusted change requests or post-merge cleanup; its branch and verify steps overlap deliver-change steps 3 to 5 in a different order.
- deliver-change: Resume does not say where to find unfinished work; closure.md lacks authority test, commands and text shape; coordination.md lacks a handoff format.
- publish-builder-changes: index paths unnamed, no commit message convention, divergence resolution unspecified.
- verify-local-app: no hidden-process or log pattern, no concrete isolation check, deployment not pointed at the spoke's instructions.
- `publish-builder-changes`, `save-session-memory` and `verify-local-app` omit `policy: allow_implicit_invocation`; the other five set it to true.

## Goals
- Each of the six skills answers its listed open questions (AC-1 to AC-6).
- All eight skills declare the same invocation policy, enforced by a test (AC-7).
- Each shared rule has one owner and identical references elsewhere (AC-8).
- Delivered on Builder main (AC-9).

## Non-Goals
- No helper script behavior changes. Reason: every gap is documentation of existing behavior; changing helpers would widen review and risk.
- No edits to `write-test-report/references/example.md` or `write-implementation-plan/references/example.md`. Reason: the migration audit verifies them against the historical corpus.
- No changes to write-implementation-plan or write-chris-street-style-code. Reason: the review found them complete; their plan-readiness criteria about runtime proof are review checks, not a competing statement of the rule.
- No new merge-method field in `spokes.json`. Reason: a registry schema change needs helper and validation changes; a documented lookup order is enough for one spoke.
- No AGENTS.md policy change. Reason: policy is already correct; the gaps are procedure.

## Acceptance Criteria
- AC-1: save-session-memory states when to write, the entry shape with an example, the `--time` format, the slug rule for Builder, spokes and new projects, what concurrent writers must do, and what a proposed-closure entry contains.
- AC-2: write-test-report links its example; owns the candidate-identity rule (short SHA of at least 7 hex characters in Branch); lists what the validator requires for `complete`; defines each status; and gives one procedure for updating a report after a rerun on the same or a later date.
- AC-3: publish-spoke-changes defines the branch prefix per agent, the merge-method lookup order, the worktree location, what to do with no required checks and with trusted change requests, post-merge cleanup, and maps its steps onto deliver-change steps without duplicating verification.
- AC-4: deliver-change Resume names where to find unfinished work; spoke branch creation happens before implementation; closure.md gives the authority test, `gh` commands, closing text shape and readback; coordination.md gives a handoff format and how to verify returned evidence.
- AC-5: publish-builder-changes names the three index paths, the commit message convention and the divergence procedure.
- AC-6: verify-local-app gives a PowerShell and POSIX pattern for hidden background processes with logs outside the repository and process-tree stop, a free-port lookup, a concrete isolation check, and points deployment commands at the spoke's own instructions.
- AC-7: All eight `agents/openai.yaml` files contain `policy:` with `allow_implicit_invocation: true`, and a SkillDiscoveryTests test fails if any omits it.
- AC-8: The candidate-SHA rule, the report-update rule and the rerun-after-runtime-edit rule are stated only in their owners (write-test-report and verify-local-app); deliver-change and publish-spoke-changes reference them by skill name without restating different thresholds or wording.
- AC-9: The plan, the change, and dated memory are on Builder origin/main, confirmed by `git ls-remote`.

## Inputs
- User request in chat on 2026-10-04: "Fix 1, 2, 3, 4, 5, 6, fix the metadata issue, fix the same rule different wording issue", after the read-only skill review in the same conversation.
- Inspected on Builder `main` at `e8517e3`, clean tree: all eight SKILL.md files, every reference except the per-language style guides, all `agents/openai.yaml`, helper argument parsers, `.agents/lib/project_memory.py` (`append_entry`, `PROJECT_RE`), `.agents/lib/artifact_quality.py` (`validate_test_report_text`), `preflight_spoke_pr.py` (`COMMIT_ID_RE`, `check_report`), `.agents/tests/test_skill_consolidation.py` (`SkillDiscoveryTests`), `docs/session-memory/2026-10-04-builder.md`, the 2026-10-04 staged-deletions plan, `spokes.json`, Builder commit messages, christopherbell.dev merge settings (`gh repo view`: squash, merge and rebase all allowed) and its merged PR branch names (`codex/<topic>-<YYYYMMDD>`).

## Branch
Builder primary checkout `main` at `e8517e3`; publish the exact task files through publish-builder-changes.

## Assumptions
- The preflight accepts any 7 to 40 lowercase hex string anywhere in the report that prefixes the candidate commit (`COMMIT_ID_RE`), so requiring it in Branch is stricter than, and compatible with, the helper.
- `append_entry` takes `--time` through `datetime.time.fromisoformat` and appends without locking, so concurrent same-file writes are unsafe.
- Codex treats a missing `allow_implicit_invocation` as true, so setting it explicitly does not change behavior.

## Open Questions
None.

## Design
Document existing behavior where each skill's reader needs it, keeping SKILL.md files short and pushing longer procedures into existing references.

Shared-rule owners:
- Candidate identity and report updates: write-test-report.
- Runtime verification before any PR and rerun after runtime-affecting edits: verify-local-app (policy stays in AGENTS.md).
- Builder artifact publication: the phase finalizer (already consistent).
deliver-change and publish-spoke-changes name the owning skill ("as write-test-report requires", "follow verify-local-app's rerun rule") instead of restating thresholds.

Ordering: for spoke work, deliver-change step 3 starts with publish-spoke-changes step 1 (branch or worktree), and its step 4 produces the verified, reported candidate. publish-spoke-changes then starts at preflight and reuses that report; it only reruns verification when HEAD changed. This removes the double verification.

Report updates: on the same date, rewrite the same report with `--overwrite` after reading it and list superseded candidate SHAs and the reason in Bugs / Follow-ups (Git keeps the earlier text). On a later date, save a new dated report and set the old one to `superseded` with a link. Alternative considered: always a new file. Rejected: same-day reruns would produce near-duplicate reports and the save helper dedupes by dated title.

Merge method lookup: the spoke's own instructions, else the only method allowed (`gh repo view --json`), else squash, the method christopherbell.dev history uses. Alternative: a `spokes.json` field; rejected per Non-Goals.

Metadata: add `allow_implicit_invocation: true` to the three files and a test so drift fails CI. Alternative: remove it everywhere and rely on the default; rejected because explicit policy is easier to audit.

## Expected Changes
- `.agents/skills/save-session-memory/SKILL.md`: When to Write, Entry Shape with example, option details, slugs, concurrent writers, proposed closure.
- `.agents/skills/write-test-report/SKILL.md`, `references/report.md`, `references/template.md`: example link, candidate identity, statuses, `complete` requirements, updating a report, title and date options.
- `.agents/skills/publish-spoke-changes/SKILL.md`: branch prefix, worktree location, step mapping, merge method, missing checks, change requests, cleanup.
- `.agents/skills/deliver-change/SKILL.md`, `references/closure.md`, `references/coordination.md`: where to resume, spoke ordering, shared-rule references, closure mechanics, handoff format.
- `.agents/skills/publish-builder-changes/SKILL.md`: index paths, commit message, divergence.
- `.agents/skills/verify-local-app/SKILL.md`: background process pattern, free port, isolation check, deployment pointer.
- `.agents/skills/{publish-builder-changes,save-session-memory,verify-local-app}/agents/openai.yaml`: policy block.
- `.agents/tests/test_skill_consolidation.py`: implicit-invocation assertion.
- This plan, today's Builder session memory and regenerated indexes.

## Task Breakdown

### Task 1 - Fill save-session-memory
Dependencies: Published reviewed plan.
Files: .agents/skills/save-session-memory/SKILL.md.
Symbols: New headings When to Write, Entry Shape, Options, Concurrent Writers; existing helper command.
Inspection: Read SKILL.md, `project_memory.py` and 2026-10-04 Builder memory entries at `e8517e3`.
Behavior: An agent knows when to write, what to write, and how to call the helper.
Invariants: Helper command and arguments unchanged; dated-file and append-only policy unchanged.
Boundary/API: Documentation only.
Effects and failures: None at runtime.
Tests and evidence: Link and script-path checks in SkillDiscoveryTests; reread for each AC-1 item.
Verification: python -B -m unittest discover -s .agents/tests; python .agents/skills/publish-builder-changes/scripts/check_hub.py check --root .

### Task 2 - Make write-test-report own report rules
Dependencies: Task 1 not required; plan published.
Files: .agents/skills/write-test-report/SKILL.md; references/report.md; references/template.md.
Symbols: Headings for Candidate Identity, Statuses, Complete Reports, Updating a Report; example link.
Inspection: Read all three files, `validate_test_report_text`, `save_test_report.py` arguments and `preflight_spoke_pr.py` `check_report` at `e8517e3`.
Behavior: Reports written from this skill alone pass the validator and the spoke preflight.
Invariants: Section names match `REPORT_REQUIRED_SECTIONS`; example.md untouched.
Boundary/API: Documentation only.
Effects and failures: None at runtime.
Tests and evidence: SkillDiscoveryTests link check; test_test_report_workflow unchanged and passing.
Verification: python -B -m unittest discover -s .agents/tests

### Task 3 - Fill publish-spoke-changes
Dependencies: Task 2 (references its rules).
Files: .agents/skills/publish-spoke-changes/SKILL.md.
Symbols: Steps 1 to 7, new When to Use, Failures and Cleanup content.
Inspection: Read SKILL.md, preflight helper, christopherbell.dev merge settings and merged branch names at `e8517e3`.
Behavior: The agent can branch, merge and clean up for any spoke and agent without guessing.
Invariants: Preflight command and gates unchanged; never force push or bypass checks.
Boundary/API: Documentation only.
Effects and failures: None at runtime.
Tests and evidence: SkillDiscoveryTests script-path check.
Verification: python -B -m unittest discover -s .agents/tests

### Task 4 - Fill deliver-change and its references
Dependencies: Tasks 2 and 3.
Files: .agents/skills/deliver-change/SKILL.md; references/closure.md; references/coordination.md.
Symbols: Resume; Steps 3 to 5; closure and coordination bodies.
Inspection: Read all three files and triage_github_comments.py arguments at `e8517e3`.
Behavior: Resume finds unfinished work; spoke ordering is single-path; closure and handoff are executable.
Invariants: Scope table, step Done lines and AGENTS.md ownership unchanged.
Boundary/API: Documentation only.
Effects and failures: None at runtime.
Tests and evidence: SkillDiscoveryTests link check.
Verification: python -B -m unittest discover -s .agents/tests

### Task 5 - Fill publish-builder-changes
Dependencies: Plan published.
Files: .agents/skills/publish-builder-changes/SKILL.md.
Symbols: What You Own items 1 to 3.
Inspection: Read SKILL.md, helper arguments and Builder commit history at `e8517e3`.
Behavior: The agent knows the index paths, message form and divergence steps.
Invariants: Helper commands unchanged; no force push.
Boundary/API: Documentation only.
Effects and failures: None at runtime.
Tests and evidence: SkillDiscoveryTests.
Verification: python -B -m unittest discover -s .agents/tests

### Task 6 - Fill verify-local-app
Dependencies: Plan published.
Files: .agents/skills/verify-local-app/SKILL.md.
Symbols: Preflight items 2 and 5; Verify items 2 and 5; Authorized Deployment item 1.
Inspection: Read SKILL.md at `e8517e3`.
Behavior: Concrete process, port, isolation and deployment guidance.
Invariants: Isolation and endpoint-only data rules unchanged.
Boundary/API: Documentation only.
Effects and failures: None at runtime.
Tests and evidence: SkillDiscoveryTests.
Verification: python -B -m unittest discover -s .agents/tests

### Task 7 - Align invocation metadata
Required skill: write-chris-street-style-code
Dependencies: Plan published.
Files: .agents/skills/publish-builder-changes/agents/openai.yaml; .agents/skills/save-session-memory/agents/openai.yaml; .agents/skills/verify-local-app/agents/openai.yaml; .agents/tests/test_skill_consolidation.py.
Symbols: `policy.allow_implicit_invocation`; `SkillDiscoveryTests.test_every_skill_allows_implicit_invocation` (new).
Inspection: Read all eight openai.yaml files and `SkillDiscoveryTests` at `e8517e3`.
Behavior: Every skill declares `allow_implicit_invocation: true`; the test names any skill that does not.
Invariants: Existing discovery assertions unchanged; YAML stays valid.
Boundary/API: Codex metadata; behavior unchanged because the default is true.
Effects and failures: Test reads files only.
Tests and evidence: Run the new test before the YAML edits to see it fail naming the three skills, then after to see it pass.
Verification: python -B -m unittest .agents/tests/test_skill_consolidation.py; python -B -m unittest discover -s .agents/tests

### Task 8 - Record and publish verified delivery
Dependencies: Tasks 1 to 7 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day Builder memory and the phase finalizer at `e8517e3`.
Behavior: The completed change and its dated evidence are on origin/main.
Invariants: Only selected files are committed; earlier history preserved.
Boundary/API: publish-builder-changes helper.
Effects and failures: Scoped commit and push; a failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Runtime verification does not apply: Builder holds workflow instructions and standalone Python helpers, not a runnable application. Native checks: the full `.agents/tests` suite (link resolution, script paths, discovery), the hub check, `git diff --check`, and a reread of each changed skill against its AC.
- AC-1, AC-2, AC-3, AC-4, AC-5, AC-6: reread each changed file against the AC's listed items; SkillDiscoveryTests confirms every link and helper path resolves; hub check passes. AC-2 also: `test_test_report_workflow` passes unchanged, and a sample report following only write-test-report passes `validate_test_report.py`.
- AC-7: new `test_every_skill_allows_implicit_invocation` fails before the YAML edits and passes after.
- AC-8: `git grep -n "short SHA\|7-character\|at least 7" .agents/skills` shows the threshold only in write-test-report; `git grep -n "update the report" .agents/skills` shows no restated procedure outside write-test-report.
- AC-9: helper output and `git ls-remote origin refs/heads/main` compared with local HEAD.

## Rollback or Recovery
Revert the change commit; skills return to their earlier wording and the test is removed with it. A failed push keeps the commit and recovers with `--push-only`.

## Risks
- New detail could contradict AGENTS.md. Mitigation: only document procedure; reread AGENTS.md sections on publication and runtime proof during review.
- A concurrent session could edit the same skills. Mitigation: check `git status` and fetch before each publication; publish only selected files.
- The `gh pr checks --required` behavior with no required checks may vary by gh version. Mitigation: describe the outcome (no required checks reported) rather than an exact message.

## Implementation Log

### 2026-10-04 - Migration audit already fails and does not cover skill references

- Change: Edited `write-test-report/references/template.md` with a short instruction line; example.md stays untouched as planned.
- Reason: `consolidate_project_memory.py --verify` checks only migrated session-memory sections, not skill templates or examples. It already fails on `docs/skill-migration.md` on `b84cc2f` with this change stashed, so the failure is unrelated to this change and out of scope.
- Impact: Non-Goal reason for example.md is weaker than stated but the file still stays unchanged; the audit failure is a follow-up, not part of AC-1 to AC-9.

## Outcome
Delivered on 2026-10-04 as planned, with one logged discovery (the migration audit's unrelated existing failure).
- AC-1: Met. save-session-memory now has When to Write (including proposed closure and closure result), Entry Shape with an example, Helper option details (`--time` as 24-hour `HH:MM`, slug rule for Builder, spokes and new projects), and Concurrent Writers.
- AC-2: Met. write-test-report links its example, owns Candidate Identity (short SHA of at least 7 hex characters in Branch), defines the four statuses and gives same-date and later-date update procedures; report.md lists what the validator requires for `complete`. A sample report written from the skill alone passes `validate_test_report.py`; `test_test_report_workflow` passes unchanged.
- AC-3: Met. publish-spoke-changes maps its steps onto deliver-change steps 3 to 5 and verifies once, and defines the agent branch prefix, worktree location, merge-method lookup order, no-required-checks handling, trusted change requests (new step 6) and Cleanup.
- AC-4: Met. deliver-change Resume gives a tested `git grep` command for unfinished plans (it listed six, including this one); spoke branching happens before implementation and Builder code is committed in step 5; closure.md has Authority, Gates, `gh` steps, comment shape and readback; coordination.md has a handoff template and return verification.
- AC-5: Met. publish-builder-changes names the three index paths, the message convention and a rebase-based divergence procedure that never stashes others' files.
- AC-6: Met. verify-local-app has PowerShell and POSIX background-start patterns with logs outside the repository, process-tree stop, a free-port lookup, a before-and-after isolation check, deployment pointed at the spoke's instructions, and named Rerun and Before-PR rules.
- AC-7: Met. `test_every_skill_allows_implicit_invocation` failed naming publish-builder-changes, save-session-memory and verify-local-app, and passes after adding their policy blocks.
- AC-8: Met. `git grep` shows the 7-character threshold only in write-test-report; deliver-change and publish-spoke-changes now reference "verify-local-app's rerun rule" and "write-test-report's update rule" instead of restating them.
- AC-9: Met when the delivery commit's `git ls-remote origin refs/heads/main` matches local HEAD; see the [2026-10-04 Builder memory](../session-memory/2026-10-04-builder.md).
Checks: 93 tests pass, the hub check passes and `git diff --check` is clean. Runtime verification does not apply: no runnable application.
Shipped versus planned: as planned. Follow-up: `consolidate_project_memory.py --verify` already fails on `docs/skill-migration.md`, independent of this change.
