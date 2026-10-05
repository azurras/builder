# Close Builder Skill Coverage Gaps

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
Every workflow AGENTS.md requires has an owning skill or helper. Spoke branch, PR, CI and merge mechanics belong to a new `publish-spoke-changes` skill. The azurras-only GitHub trust rule is applied by a helper instead of by hand. New spokes are registered by command. The stale bytecode left over from the publish-builder-changes rename is gone.

## Background
On 2026-10-04 the user asked which skills Builder was missing. An audit found no dangling references, but it found four gaps between policy and tooling:
- AGENTS.md says "The publication skill owns exact Git mechanics", but `publish-builder-changes` refuses anything except the Builder checkout on main. Spoke publication has only one sentence in step 5 of `deliver-change`. Recent spoke deliveries (christopherbell.dev PRs 1474 to 1476) therefore rebuilt branch naming, evidence linking, CI waiting and squash merge by hand.
- AGENTS.md says only azurras may direct work through GitHub comments, and `test_github_trust_boundary.py` only checks that the sentence exists. Nothing separates trusted from untrusted comments when an agent reads an issue or PR.
- AGENTS.md says to register a spoke "by adding it to spokes.json". `manage_spoke_repositories.py` can list, locate and clone spokes, but registering one means editing JSON by hand with no validation until later.
- `.agents/tests/__pycache__/test_commit_push_builder_main.cpython-312.pyc` survived the rename. It is ignored by Git, so this is local cleanup only.
The user said "Let's move forward and attack all these issues."

## Goals
- Spoke publication has one owning skill with a read-only preflight that ties the PR candidate to published runtime evidence (AC-1, AC-2).
- GitHub issue and PR comments can be split into trusted direction and untrusted data with one command (AC-3).
- A spoke can be registered with a validated command that keeps the registry free of machine paths and duplicates (AC-4).
- Policy, README and skills name the new owners; the suite and hub check pass; everything is published (AC-5, AC-6, AC-7).

## Non-Goals
- The helpers do not create, push, merge or comment on anything. GitHub mutations stay explicit `gh` commands the agent runs under existing authority, because a wrapper would hide the irreversible steps that AGENTS.md requires confirming.
- No automatic CI polling loop. The skill tells the agent to use `gh pr checks --watch` or the host's PR monitor, which already exist.
- No change to the trusted author. azurras stays the only trusted author; making it configurable is not requested.
- No reachability check (`git ls-remote`) in `register`. It must work offline, and `locate` and `clone` already verify the origin.
- No change to spoke repositories, their build commands or their instructions. Spokes own build, run and deployment.
- No new skill for comment triage. It is a helper used by `deliver-change` and `publish-spoke-changes`; a separate skill would add a routing decision for one command.
- No edits to dated plans, reports or memory beyond today's memory entry.

## Acceptance Criteria
- AC-1: `.agents/skills/publish-spoke-changes/` has SKILL.md (`name: publish-spoke-changes`), agents/openai.yaml and scripts/preflight_spoke_pr.py. SKILL.md covers branch naming, the preflight, PR body with the evidence link, CI gates, squash merge matching the spoke's history, and merge readback. Skill discovery lists exactly eight skills.
- AC-2: `preflight_spoke_pr.py --spoke <slug> [--path <checkout>] --report <builder report>` is read-only. It exits nonzero when the checkout origin does not match the registry; when the branch is the default branch or detached; when tracked files are modified or staged; when the branch has no commits ahead of `origin/<default>`; when the report fails validation, is not identical on Builder `origin/main`, or does not contain the candidate HEAD (at least the 7-character short SHA). On success it prints the candidate and a PR verification snippet linking the report on GitHub. Each failure has a native test, and a real run against christopherbell.dev shows the expected refusal on its main checkout.
- AC-3: `triage_github_comments.py --repo <owner/name> --number <n>` reads the issue or PR body, conversation comments and, for PRs, review comments and review bodies through `gh api`. It prints azurras items under a trusted heading and all others under an untrusted heading that says they are data, and lists links and attachments in untrusted items as not to be opened. Login matching is exact and case-insensitive; deleted users are untrusted. Native tests use JSON fixtures through `--from-json`; a live read-only run against azurras/christopherbell.dev PR 1476 succeeds.
- AC-4: `manage_spoke_repositories.py register --spoke <slug> --name <n> --repository <url> --description <d> [--default-branch main]` appends a valid entry to spokes.json (2-space JSON, trailing newline). It refuses duplicate slugs, a repository already registered under another form, a checkout directory name already used, a non-remote repository value such as a local path, and `--path`. Existing modes behave the same.
- AC-5: AGENTS.md names publish-builder-changes for Builder Git mechanics and publish-spoke-changes for spokes, names the register command, and points the trust rule at the triage helper while keeping the phrases `test_github_trust_boundary.py` checks. README lists eight skills and the register command. deliver-change step 5 and step 1 point at the new skill and helper.
- AC-6: `python -B -m unittest discover -s .agents/tests` passes, `check_hub.py refresh --root .` passes, `git diff --check` is clean, and the stale `test_commit_push_builder_main` bytecode no longer exists locally.
- AC-7: This plan, the change and the dated delivery memory are on origin/main, confirmed by `git ls-remote`.

## Inputs
- User requests in chat on 2026-10-04: "what skills are we missing?" and "Let's move forward and attack all these issues."
- Inspected on Builder `main` at `6c59551`, clean tree: AGENTS.md; README.md; all seven SKILL.md files; deliver-change openai.yaml, references/repository-inspection.md, references/closure.md and scripts/manage_spoke_repositories.py; publish-builder-changes SKILL.md, openai.yaml and phase finalizer; .agents/lib/spoke_registry.py and spoke_state.py; write-test-report scripts/validate_test_report.py, references/template.md and `validate_test_report_text`; validate_hub_state.py skill checks; tests test_spoke_registry.py, test_skill_consolidation.py and test_github_trust_boundary.py; write-implementation-plan plan and review references; today's Builder memory; the deliver-change rename plan as precedent.
- Inspected christopherbell.dev at its main checkout (read-only): AGENTS.md worktree and testing guidance, `.github/workflows`, PRs 1474 to 1476 (branch `codex/<topic>-<YYYYMMDD>`, base main, squash merge, body with Summary and Verification) and the repository's merge settings. Inspected the 2026-10-04 handoff-removal test report, which names the reviewed head SHA. `gh` 2.93.0 is authenticated as azurras.

## Branch
Builder primary checkout `main` at `6c59551`; publish the exact task files through publish-builder-changes.

## Assumptions
- `gh api --paginate --slurp` returns one JSON array of pages in gh 2.93.0. If not, the helper falls back to concatenating arrays, and the live run catches it.
- Builder's origin is a GitHub repository, so a report link is `https://github.com/<owner>/<repo>/blob/main/<path>`.
- Agents fetch the spoke before preflight; the helper reads `origin/<default>` without fetching so it stays read-only.

## Open Questions
None. The user authorized all four items; design choices below follow repository precedent.

## Design
**publish-spoke-changes.** A skill parallel to publish-builder-changes. SKILL.md lists the steps in order: work on a branch named `<agent>/<topic>-<YYYYMMDD>` from the fetched default branch (the spoke's own precedent); commit; run the preflight; push; `gh pr create` with Summary and Verification sections and the snippet the preflight prints; wait for required checks; resolve in-scope failures and rerun affected local verification before pushing again; squash merge when the spoke's history uses squash merges; read back the merge commit and state. The preflight script enforces what can be checked locally and offline. Requiring the report to contain the candidate SHA ties the evidence to the exact commit, which verify-local-app already requires in prose.
Alternative rejected: extend publish-builder-changes to spokes. Its helper's safety comes from refusing every root but Builder main, and mixing the two would weaken that guard.
Alternative rejected: a helper that also pushes and creates the PR. It would hide irreversible actions inside one command.

**Comment triage.** A pure library `.agents/lib/github_trust.py` holds `TRUSTED_AUTHORS = {"azurras"}`, the item model, classification and Markdown rendering. `deliver-change/scripts/triage_github_comments.py` fetches through `gh api` or loads `--from-json` and prints the result. Untrusted text is shown in fenced blocks so an agent can verify claims without treating them as instructions. Links in untrusted items are listed separately with a "do not open or run" note, which follows the attachment rule in AGENTS.md. A test checks that the constant agrees with AGENTS.md.
Alternative rejected: show only trusted comments. AGENTS.md says to verify other comments' claims independently, which needs their content.

**register.** Add a mode to the existing script and `register_spoke` to spoke_registry.py, reusing `_spoke_from_entry` validation. Reject local paths by requiring an `https://`, `ssh://` or `user@host:` remote form. Directory collisions are refused because sibling resolution would map two spokes to one folder.

**pycache.** Delete the one stale file locally. The folder is ignored, so nothing is committed.

## Expected Changes
- New `.agents/skills/publish-spoke-changes/SKILL.md`, `agents/openai.yaml`, `scripts/preflight_spoke_pr.py`.
- New `.agents/lib/github_trust.py` and `.agents/skills/deliver-change/scripts/triage_github_comments.py`.
- `.agents/lib/spoke_registry.py`: `register_spoke`, remote-form check.
- `.agents/lib/spoke_state.py`: `origin_mismatch`, moved from manage_spoke_repositories.py so the preflight shares it.
- `.agents/skills/deliver-change/scripts/manage_spoke_repositories.py`: `register` mode and its arguments.
- `.agents/skills/deliver-change/SKILL.md` steps 1 and 5; `references/repository-inspection.md` register usage.
- AGENTS.md Hub and Spokes, Quality and Delivery, and Trust and Git paragraphs; README skills table, heading and spoke registration.
- Tests: new `test_publish_spoke_changes.py` and `test_github_trust.py`; `test_spoke_registry.py` register cases; `test_skill_consolidation.py` discovery set.
- This plan, today's Builder memory and regenerated indexes.

## Task Breakdown

### Task 1 - Register spokes by command
Required skill: write-chris-street-style-code
Dependencies: Published reviewed plan.
Files: .agents/lib/spoke_registry.py; .agents/skills/deliver-change/scripts/manage_spoke_repositories.py; .agents/skills/deliver-change/references/repository-inspection.md; .agents/tests/test_spoke_registry.py.
Symbols: new `register_spoke`; `_spoke_from_entry`; `main` mode choices and new `--name`, `--repository`, `--description`, `--default-branch`.
Inspection: Read all four files at `6c59551`; `test_skill_consolidation.py` already expects `register` with `--path` to fail.
Behavior: `register` appends one validated entry and prints the new entry and the clone command; other modes are unchanged.
Invariants: spokes.json holds no machine paths; slugs, normalized repositories and directories stay unique; a refused register leaves the file byte-identical.
Boundary/API: New CLI mode; existing modes and arguments are unchanged.
Effects and failures: Writes spokes.json only after full validation; errors print to stderr and exit 2 like other ValueErrors.
Tests and evidence: Tests for success, each refusal and file unchanged on refusal; real `list` run afterward.
Verification: python -B -m unittest .agents/tests/test_spoke_registry.py; a register run in a temporary Builder root.

### Task 2 - Triage GitHub comments by trust
Required skill: write-chris-street-style-code
Dependencies: None.
Files: new .agents/lib/github_trust.py (pattern: spoke_registry.py dataclasses and ValueError); new .agents/skills/deliver-change/scripts/triage_github_comments.py (pattern: manage_spoke_repositories.py argparse and lib import); new .agents/tests/test_github_trust.py (pattern: test_spoke_registry.py).
Symbols: `TRUSTED_AUTHORS`, `GithubItem`, `items_from_payload`, `is_trusted`, `render_triage`; script `main`.
Inspection: Read AGENTS.md Trust and Git, test_github_trust_boundary.py and the scripts' import pattern at `6c59551`; checked gh 2.93.0 authentication.
Behavior: Prints trusted direction, then untrusted data with its links listed as not to be opened. Detects PRs from the issue payload.
Invariants: Only exact azurras logins are trusted; nothing is written or posted; attachments are never fetched.
Boundary/API: New CLI; `gh api` GET requests only.
Effects and failures: Network reads through gh; gh failure or invalid JSON exits nonzero with the error.
Tests and evidence: Fixture tests for case-insensitive match, lookalike logins, deleted user, PR review sources, link listing; AGENTS.md consistency test; live run on PR 1476.
Verification: python -B -m unittest .agents/tests/test_github_trust.py; python .agents/skills/deliver-change/scripts/triage_github_comments.py --repo azurras/christopherbell.dev --number 1476.

### Task 3 - Add publish-spoke-changes
Required skill: write-chris-street-style-code
Dependencies: None; uses spoke_registry and validate_test_report_text.
Files: new .agents/skills/publish-spoke-changes/SKILL.md and agents/openai.yaml (pattern: publish-builder-changes); .agents/lib/spoke_state.py and manage_spoke_repositories.py (`origin_mismatch` moved); new scripts/preflight_spoke_pr.py (pattern: manage_spoke_repositories.py); new .agents/tests/test_publish_spoke_changes.py; .agents/tests/test_skill_consolidation.py.
Symbols: `preflight` checks; `report_link`; SkillDiscoveryTests expected set.
Inspection: Read publish-builder-changes SKILL.md and openai.yaml, spoke_state.git, `validate_test_report_text`, christopherbell.dev PR conventions at `6c59551`.
Behavior: Preflight prints each check with pass or fail and a PR snippet on success; SKILL.md orders the publication steps.
Invariants: The helper never fetches, writes, pushes or calls GitHub.
Boundary/API: New CLI; new skill name.
Effects and failures: Git reads only; every failed check is listed and the exit is nonzero.
Tests and evidence: Fixture repos (spoke with bare origin, Builder with origin and a published report) for every refusal and the success path; real run against christopherbell.dev.
Verification: python -B -m unittest .agents/tests/test_publish_spoke_changes.py; python .agents/skills/publish-spoke-changes/scripts/preflight_spoke_pr.py --spoke christopherbell-dev --report docs/test-reports/2026-10-04-software-handoff-removal-runtime-verification.md (expected refusal: main branch).

### Task 4 - Align policy and docs; remove stale bytecode
Dependencies: Tasks 1 to 3, so docs name real commands.
Files: AGENTS.md; README.md; .agents/skills/deliver-change/SKILL.md; .agents/tests/__pycache__/test_commit_push_builder_main.cpython-312.pyc (local delete).
Symbols: AGENTS.md Hub and Spokes, Quality and Delivery, Trust and Git; README "Seven Skills" table and spoke registration line; deliver-change steps 1 and 5.
Inspection: Read all at `6c59551`.
Behavior: Each workflow names its owner; trust test phrases preserved.
Invariants: AGENTS.md stays agent-neutral and policy-level; no machine paths.
Boundary/API: Documentation only.
Effects and failures: The deleted file is ignored by Git; no commit effect.
Tests and evidence: Full suite, hub check, identifier search.
Verification: python -B -m unittest discover -s .agents/tests; check_hub.py refresh --root .; git diff --check; test -e on the deleted file.

### Task 5 - Record and publish verified delivery
Dependencies: Tasks 1 to 4 checks and review pass.
Files: This plan; docs/session-memory/2026-10-04-builder.md; generated indexes.
Symbols: Outcome; Document Status; appended memory entry.
Inspection: Read same-day memory and the phase finalizer at `6c59551`.
Behavior: Completed change and evidence on origin/main.
Invariants: Only selected files committed.
Boundary/API: publish-builder-changes helper.
Effects and failures: Scoped commit and push; a failed push stays incomplete until push-only recovery.
Tests and evidence: Passing checks, reviewed diff, remote readback.
Verification: Helper dry run, then publication; git ls-remote origin refs/heads/main matches HEAD.

## Test Plan
Builder is not a runnable application, so verify-local-app does not apply. The new helpers are exercised for real against live repositories as their runtime check.
- AC-1: SkillDiscoveryTests with eight skills; hub check validates frontmatter and links.
- AC-2: test_publish_spoke_changes.py covers origin mismatch, default branch, detached HEAD, dirty tracked file, no commits ahead, invalid report, report missing or different on Builder origin/main, report lacking the SHA, and success with the snippet; a read-only run against christopherbell.dev main refuses because the branch is the default branch.
- AC-3: test_github_trust.py fixtures plus the AGENTS.md consistency test; live read-only run on azurras/christopherbell.dev PR 1476 prints both headings.
- AC-4: test_spoke_registry.py register cases, including the byte-identical file on refusal; existing mode tests still pass.
- AC-5: Read the diff; `git grep -n "adding it to spokes.json"` returns nothing; test_github_trust_boundary.py passes.
- AC-6: Full suite, `check_hub.py refresh --root .`, `git diff --check`, file absence check.
- AC-7: Helper output and `git ls-remote origin refs/heads/main` against local HEAD.

## Rollback or Recovery
Revert the task commit; it removes the new skill, helpers and docs together. spokes.json is not changed by this work. If a push fails, keep the commit and recover with `--push-only`.

## Risks
- Report SHA check rejects valid reports that name the candidate differently. Mitigation: accept any prefix of 7 or more characters; the skill tells the writer to include it. Likelihood: low; the latest report already does.
- `gh` pagination output differs. Mitigation: live run and tolerant parsing.
- Concurrent sessions edit AGENTS.md, README or tests. Mitigation: confirm clean tree before editing and before publishing.

## Implementation Log

### 2026-10-04 - Share the origin check through spoke_state

- Change: `origin_mismatch` moved from `manage_spoke_repositories.py` into `.agents/lib/spoke_state.py`; both the spoke helper and `preflight_spoke_pr.py` import it.
- Reason: The preflight needs the same registry-origin check, and scripts are not importable libraries; one shared function keeps the two checks identical.
- Impact: Expected Changes and Task 3 Files now list spoke_state.py. Behavior of locate and inspect is unchanged (existing spoke tests pass). Acceptance criteria unchanged.

## Outcome
Delivered on 2026-10-04 with one logged deviation (the shared origin check).
- AC-1: Met. `.agents/skills/publish-spoke-changes/` has SKILL.md, agents/openai.yaml and scripts/preflight_spoke_pr.py; SKILL.md covers branch naming, preflight, PR body, required CI, squash merge with `--match-head-commit` and readback. The `gh` flags it uses were confirmed in gh 2.93.0. SkillDiscoveryTests passes with eight skills.
- AC-2: Met. test_publish_spoke_changes.py (8 tests) covers success with the report link, origin mismatch, default branch, detached HEAD, modified tracked file (untracked allowed), no commits ahead, report missing from or different on Builder origin/main, report not naming the candidate, draft report and a report path outside docs/test-reports. The real read-only run against the christopherbell.dev main checkout exited 1, refusing on the default branch, a modified `gradlew.bat`, no commits ahead and a report that does not name candidate `e073823`; its checkout and report checks passed and the spoke's status was unchanged.
- AC-3: Met. test_github_trust.py (7 tests) covers exact case-insensitive matching, lookalike and deleted users, every PR source, malformed payloads, rendering and the AGENTS.md consistency check. Live read-only runs: azurras/christopherbell.dev#1476 put the azurras opening post under Trusted direction (1); #1464 put the dependabot[bot] post under Untrusted input (1) with its links listed; a missing number exited 2 with the gh 404.
- AC-4: Met. test_spoke_registry.py adds library and CLI register tests, including byte-identical spokes.json on every refusal; existing mode tests pass. spokes.json itself is unchanged.
- AC-5: Met. AGENTS.md, README (Eight Skills), deliver-change steps 1 and 5 and repository-inspection.md name the new skill, helper and register mode; `git grep "adding it to spokes.json"` outside docs is empty; test_github_trust_boundary.py passes.
- AC-6: Met. `python -B -m unittest discover -s .agents/tests` ran 92 tests, OK. `check_hub.py refresh --root .` passed with only the eight historical warnings. `git diff --check` clean. The stale `test_commit_push_builder_main` bytecode was deleted locally (ignored by Git).
- AC-7: Met when the publication readback in the [2026-10-04 Builder memory](../session-memory/2026-10-04.md) shows origin/main at the delivery commit.
Shipped versus planned: as planned, plus `origin_mismatch` moved into spoke_state.py. Follow-up, not started: the first real spoke PR through publish-spoke-changes will be the skill's first end-to-end use.
