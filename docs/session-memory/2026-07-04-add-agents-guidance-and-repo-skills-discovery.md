# 2026-07-04 - Add agents guidance and repo skills discovery

## 19:13 - Add agents guidance and repo skills discovery

### Request
The user asked to do both recommendations from the previous answer: add a root agent guidance file and make the repo-local skills discoverable by Codex. The intended outcome is for future Codex sessions in the azurras repo to load durable repo guidance and automatically see the checked-in workflow skills.

### Project Context
This repository is `/Users/cbell/Developer/azurras`, the azurras AI workflow hub. Before this request, workflow skills lived under `/Users/cbell/Developer/azurras/skills`, but current Codex documentation says repo-scoped skills are discovered from `.agents/skills` along the path from the current working directory to the repository root. There was no root `/Users/cbell/Developer/azurras/AGENTS.md` file.

### Work Completed
Added `/Users/cbell/Developer/azurras/AGENTS.md` with repo-wide operating guidance. It records the repository purpose, points agents to `.agents/skills`, defines durable artifact locations for session memory, specs, and implementation plans, and states that after saving session memory, specs, or implementation plans, agents should use `commit-push-azurras-main` to commit and push the azurras repo changes to `main`.

Moved the repo-local skills from `/Users/cbell/Developer/azurras/skills` to `/Users/cbell/Developer/azurras/.agents/skills` using `git mv`. This makes the canonical checked-in skills discoverable by Codex as repo-scoped skills while avoiding duplicate skill copies that could drift apart.

The moved skills are: `commit-push-azurras-main`, `save-session-memory`, `save-project-spec`, and `save-implementation-plan`.

### Decisions
Chose to move rather than mirror the skills. Mirroring would satisfy discovery but create two sources of truth, increasing the chance that future edits update one copy and leave the other stale. A single canonical `.agents/skills` tree matches Codex discovery behavior and keeps maintenance simple.

Kept `AGENTS.md` concise and focused on durable repo-wide rules rather than duplicating detailed skill instructions. Detailed workflows remain in each skill's `SKILL.md` and helper scripts.

### Validation
Ran a standard-library frontmatter validation over every `.agents/skills/*/SKILL.md`; all passed. Ran `PYTHONPYCACHEPREFIX=/private/tmp/azurras-agents-pycache python3 -m py_compile` across all helper scripts from their new `.agents/skills` paths; it passed. Ran the moved commit/push helper in `--dry-run` mode; it confirmed repo `/Users/cbell/Developer/azurras`, branch `main`, origin `https://github.com/azurras/azurras.git`, showed the pending renames plus `AGENTS.md`, and made no Git changes.

### Current State
The repo has staged renames from `skills/...` to `.agents/skills/...`, a new `AGENTS.md`, and this new memory file at `/Users/cbell/Developer/azurras/docs/session-memory/2026-07-04-add-agents-guidance-and-repo-skills-discovery.md`. Per the repo workflow, this should be committed and pushed to `origin main` using the guarded `commit-push-azurras-main` helper.

### Follow-ups
Future Codex sessions launched in this repo should load `/Users/cbell/Developer/azurras/AGENTS.md` and discover repo-scoped skills under `/Users/cbell/Developer/azurras/.agents/skills`. If a future session does not show the skills, restart Codex in the repo root so discovery runs again.
