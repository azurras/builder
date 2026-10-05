# Portable Hub and Spoke Builder

## Document Status
in-progress

## Plan Format
task-contract-v1

## Objective
Make Builder a portable, agent-neutral hub: every project starts here, spoke repositories are declared once in a tracked registry and located on any computer without hard-coded machine paths, and both Claude Code and Codex/ChatGPT discover the same policy and skills.

## Goals
- Remove machine-specific Builder paths from active policy and publication code; identify the Builder checkout by Git identity instead.
- Add a tracked spoke registry (christopherbell.dev as the only current spoke) with per-machine path resolution and origin verification.
- Let agents list, locate, inspect and clone spokes from the registry using one helper.
- Give Claude Code the same instructions (CLAUDE.md importing AGENTS.md) and the same skills (generated .claude/skills entrypoints that delegate to canonical .agents/skills).
- Keep Codex discovery (.agents/skills, agents/openai.yaml, AGENTS.md) unchanged.

## Inputs
- User request on 2026-10-04: Builder is the AI hub, repos worked on are spokes, christopherbell.dev is the only current spoke, avoid hard-coded paths, usable from any computer, compatible with Claude and ChatGPT.
- Earlier same-session request to remove the C:\Users\Christopher\Developer\builder reference.
- Inspected on Builder main 1514713 (clean after fast-forward): AGENTS.md, README.md, .gitignore, .agents/lib/builder_hub.py, spoke_state.py, project_memory.py, commit_push_builder_main.py and its tests, complete-builder-work SKILL.md and references, manage_spoke_repositories.py, maintain_builder_hub.py, validate_hub_state.py, test_skill_consolidation.py, plan-builder-work references.
- christopherbell.dev checkout on this machine is a sibling of Builder with origin https://github.com/azurras/christopherbell.dev.git on main.

## Branch
Builder main, origin https://github.com/azurras/builder.git, through the exact-file publication helper. No spoke changes.

## Non-Goals
- Changing christopherbell.dev or any other spoke.
- Duplicating spoke build/run commands in Builder; each spoke's own instructions own them.
- Rewriting historical plans, reports or dated memory that mention old paths.
- Generated or copied skill entrypoints (superseded by Task 5 at the user's request).

## Assumptions
- Spokes are usually cloned beside the Builder checkout; other layouts use an environment variable or an ignored local override file.
- Python 3 is available as python or python3.

## Open Questions
None; registry format and path precedence are routine choices recorded under Code Changes.

## Task Breakdown

### Task 1 - Identify the Builder checkout without machine paths
Dependencies: None.
Files: AGENTS.md; .agents/skills/commit-push-builder-main/SKILL.md; .agents/skills/commit-push-builder-main/scripts/commit_push_builder_main.py; .agents/tests/test_commit_push_builder_main.py; .agents/lib/builder_hub.py.
Symbols: EXPECTED_ROOTS, is_expected_root, expected_roots_display, main root checks, HUB_ROOTS, HUB_ROOT, CommitPushBuilderMainTests.
Inspection: Read all listed files on main 1514713; HUB_ROOTS/HUB_ROOT have no callers; root list is enforced at two points in main().
Required skill: write-chris-street-style-code.
Behavior: The helper publishes from any local path when the root is the repository top level, not a linked worktree, on main, with the Builder origin.
Invariants: Exact-file selection, staged-state refusal, dry run and push-only recovery stay unchanged; spokes and linked worktrees remain refused by origin and worktree checks.
Boundary/API: CLI flags unchanged; --root help text changes.
Effects and failures: Subdirectory roots and linked worktrees fail before any Git mutation with explicit messages.
Tests and evidence: New tests refuse a subdirectory root and a linked worktree; existing behavior tests pass without patching a root list.
Verification: python -B -m unittest discover -s .agents/tests -p test_commit_push_builder_main.py.

### Task 2 - Spoke registry and portable resolution
Dependencies: None.
Files: new spokes.json at the Builder root (pattern: root-level hub configuration beside AGENTS.md); new .agents/lib/spoke_registry.py (pattern: .agents/lib/spoke_state.py); .agents/skills/complete-builder-work/scripts/manage_spoke_repositories.py; .gitignore; new .agents/tests/test_spoke_registry.py (pattern: test_skill_consolidation.py temp-repo fixtures).
Symbols: Spoke dataclass, load_spokes, find_spoke, resolve_spoke_path, normalize_remote; manage_spoke_repositories modes list, locate, clone and --spoke option.
Inspection: Read manage_spoke_repositories.py, spoke_state.py and RepositoryInspectionTests; current inspection requires an explicit --path recalled from memory.
Required skill: write-chris-street-style-code.
Behavior: list prints registered spokes; locate prints the resolved local path, whether it exists and whether its origin matches; clone clones a missing spoke to the resolved path; inspect/snapshot accept --spoke instead of --path.
Invariants: Path precedence is spokes.local.json (ignored, per machine), then BUILDER_SPOKES_ROOT, then the Builder checkout's parent directory. Inspect stays read-only. Existing --path behavior and the rejected register mode stay unchanged.
Boundary/API: spokes.json schema {"spokes": [{slug, name, repository, defaultBranch, description, directory?}]}; slug matches the session-memory project slug.
Effects and failures: Invalid registry, unknown slug, origin mismatch and clone into an existing path return explicit nonzero errors. clone is the only network/write operation.
Tests and evidence: Temp-root tests for registry validation, precedence order, origin normalization (https/ssh/.git) and mismatch, list/locate output and existing-path clone refusal.
Verification: python -B -m unittest discover -s .agents/tests -p test_spoke_registry.py; locate christopherbell-dev on this machine.

### Task 3 - Claude Code compatibility
Dependencies: None.
Files: new CLAUDE.md; new .claude/skills/<skill>/SKILL.md for each canonical skill; new .agents/skills/maintain-builder-hub/scripts/sync_claude_skills.py (pattern: update_hub_indexes.py check/refresh); maintain_builder_hub.py; maintain-builder-hub SKILL.md; new test in .agents/tests/test_skill_consolidation.py.
Symbols: CLAUDE.md @AGENTS.md import; render_claude_skill, sync/check entrypoint; maintain_builder_hub command list; SkillDiscoveryTests.
Inspection: Read maintain_builder_hub.py, validate_skill_frontmatter and SkillDiscoveryTests; Claude Code reads CLAUDE.md and .claude/skills, Codex reads AGENTS.md and .agents/skills.
Required skill: write-chris-street-style-code.
Behavior: Claude Code loads AGENTS.md through CLAUDE.md and discovers each Builder skill with identical name/description; each entrypoint delegates to the canonical SKILL.md.
Invariants: .agents/skills stays the single source of truth; refresh regenerates entrypoints, check fails on drift without writing; roots without .agents/skills are skipped.
Boundary/API: maintain_builder_hub check/refresh gain the Claude sync step; no new CLI for agents to remember.
Effects and failures: Refresh writes only .claude/skills/*/SKILL.md and removes generated entrypoints whose canonical skill no longer exists.
Tests and evidence: Test that generated entrypoints exist for exactly the canonical skills and match rendering.
Verification: maintain_builder_hub.py check --root .; full unittest discovery.

### Task 4 - Hub-and-spoke policy and documentation
Dependencies: Tasks 1-3 define the behavior documented here.
Files: AGENTS.md; README.md; .agents/skills/complete-builder-work/SKILL.md; .agents/skills/complete-builder-work/references/repository-inspection.md.
Symbols: AGENTS.md Hub and Spokes section, Documents restriction wording, python3 note; README skill/agent table; repository inspection commands.
Inspection: Read all listed files on main 1514713.
Required skill: write-chris-street-style-code.
Behavior: Agents start in Builder, find spokes through the registry, follow the spoke's own instructions inside it, and record work under the spoke's memory slug.
Invariants: Three docs folders, trusted-author rules and publication checkpoints unchanged.
Boundary/API: Documentation only.
Effects and failures: None beyond text.
Tests and evidence: SkillDiscoveryTests link and command checks; hub validation.
Verification: maintain_builder_hub.py refresh --root .; git diff --check.

### Task 5 - One shared skills folder for Claude and Codex
Dependencies: Task 3 delivered generated entrypoints; the user rejected keeping skills in two places, so this task replaces them.
Files: .claude/skills (becomes a Git symlink to ../.agents/skills); .agents/skills/maintain-builder-hub/scripts/sync_claude_skills.py (removed); maintain_builder_hub.py; validate_hub_state.py; maintain-builder-hub SKILL.md; .agents/tests/test_skill_consolidation.py; AGENTS.md; CLAUDE.md; README.md.
Symbols: maintain_builder_hub command list; validate_claude_skills_link in validate_hub_state; SkillDiscoveryTests Claude tests; AGENTS.md shared-agent paragraph; README Agents and setup sections.
Inspection: Official Claude Code skill docs (code.claude.com/docs/en/skills) list only fixed .claude/skills locations and state there is no custom skill path setting; Codex reads .agents/skills. On this Windows machine a native directory symlink was created successfully and Git reports core.symlinks=true from the system gitconfig.
Required skill: write-chris-street-style-code.
Behavior: Skills exist only in .agents/skills; Claude Code reads the same files through the .claude/skills symlink. Nothing is generated or copied.
Invariants: Codex discovery and skill content unchanged; relative links inside skills still resolve; hub check stays read-only.
Boundary/API: maintain_builder_hub check/refresh lose the sync step; validate_hub_state reports a checkout whose .claude/skills is not a link to .agents/skills, with the fix.
Effects and failures: Windows checkouts without symlink support materialize the link as a text file; validation fails and README gives the one-time Developer Mode and core.symlinks setup.
Tests and evidence: Repository test asserts .claude/skills is a symlink resolving to .agents/skills; validation test covers a non-link .claude/skills in a temp root.
Verification: python -B -m unittest discover -s .agents/tests; maintain_builder_hub.py check --root .; git ls-files -s .claude/skills shows mode 120000.

## Code Changes
Registry is JSON so both agents and stdlib Python parse it without dependencies. Local paths never enter tracked files: precedence is spokes.local.json, BUILDER_SPOKES_ROOT, then sibling of the Builder checkout. Claude skills initially used generated delegating entrypoints; Task 5 replaces them with a single Git symlink .claude/skills -> ../.agents/skills so there is exactly one skills folder. Windows needs symlink support (Developer Mode and core.symlinks=true), checked by hub validation.

## Files and Modules
Tasks 1-4 list inspected targets. This plan, generated indexes and docs/session-memory/2026-10-04-builder.md carry planning and delivery evidence.

## Unit Testing
Builder unittest discovery plus new spoke registry and Claude entrypoint tests using temporary directories and real Git repositories.

## Local Testing
No runnable application exists in this change; Builder is a workflow repository of helper scripts and documents. Exercise the real helpers instead: locate christopherbell-dev on this checkout, run inspect --spoke christopherbell-dev, run maintain check, and dry-run the publication helper from this non-standard path.

## Validation
Full native suite, maintain-builder-hub check, git diff --check, and semantic review that no active file contains a machine-specific Builder or spoke path.

Verified results on 2026-10-04: native suite ran 58 tests with 57 passing, including 11 new spoke registry tests and 2 new Claude entrypoint tests. The single failure is SkillDiscoveryTests detecting seven untracked folders on this machine that hold only __pycache__ from skills removed upstream; they are not tracked content and deleting them was blocked by this session's permission policy. maintain-builder-hub check and git diff --check passed. locate and inspect --spoke christopherbell-dev resolved A:/Projects/christopherbell.dev as the sibling of Builder with matching origin on main. The publication helper ran from this non-standard checkout path. No active file outside dated history contains a machine-specific path.

## Rollback or Recovery
Revert the delivery commit; generated .claude entrypoints and spokes.json are additive. A failed push keeps its commit and is recovered with push-only.

## Risks
- Origin URL variants (ssh vs https) could produce false mismatches; normalize host/owner/repo.
- Generated Claude entrypoints could drift; the hub check fails on drift.
- Stale untracked cache-only skill folders on a machine break SkillDiscoveryTests; they are local leftovers, not tracked content.

## Completion Criteria
- No active policy or code path references a machine-specific Builder path.
- christopherbell-dev is registered and resolves on this machine with matching origin.
- Claude Code and Codex both discover all Builder skills and shared policy.
- Native suite and hub check pass; plan, memory and changes are published to main.
