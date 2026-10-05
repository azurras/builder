# Builder

Builder is the AI workflow hub. All work starts here; the repositories it coordinates are spokes.

## The Model

Builder keeps one record for every project, so any agent on any computer can pick up any of them: implementation plans, runtime evidence and dated session memory, plus the shared skills and helpers. A spoke keeps only its own code and its own build, run and deployment instructions; its plans, reports and memory live here, never in the spoke. Builder code goes straight to `main`; spoke code goes through a pull request, required CI and a merge.

Every record belongs to one project. The valid project slugs are `builder` (the hub itself), each spoke, and each entry under `projects` in [spokes.json](spokes.json), which lists work with no repository and marks it `active` or `retired`. The save helpers and the hub check refuse any other slug.

## Start on Any Computer

1. Clone Builder anywhere. Nothing depends on its location. On Windows, first turn on Developer Mode and run `git config --global core.symlinks true` so the shared skills link checks out as a real link (macOS and Linux need nothing).
2. List spokes and clone any that are missing (by default they go beside the Builder folder):

   ```bash
   python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py list
   python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py clone --spoke christopherbell-dev
   ```

3. Keep spokes somewhere else by setting `BUILDER_SPOKES_ROOT`, or map individual spokes in an ignored `spokes.local.json` such as `{"christopherbell-dev": "D:/code/site"}`.
4. Open Builder in Claude Code, Codex or ChatGPT. Use `python3` where `python` is unavailable.

| Spoke | Repository |
|---|---|
| christopherbell-dev | [azurras/christopherbell.dev](https://github.com/azurras/christopherbell.dev) |

Register a new spoke in [spokes.json](spokes.json) with `manage_spoke_repositories.py register --spoke <slug> --name <name> --repository <url> --description <text>`.

## Agents

[AGENTS.md](AGENTS.md) is the shared policy: Codex and ChatGPT read it directly, and Claude Code imports it through [CLAUDE.md](CLAUDE.md). Skills live in one folder, `.agents/skills`. `.claude/skills` is a symlink to it, so both agents read the same files; the hub check (`publish-builder-changes/scripts/check_hub.py`) reports a checkout where the link is missing.

## Documents

| Documents | Contents |
|---|---|
| [Implementation plans](docs/implementation-plans/index.md) | Requirements, design, inspected tasks and verification, in YYYY-MM-DD-project-title.md files |
| [Test reports](docs/test-reports/index.md) | Actual runtime inputs, outputs and results, in YYYY-MM-DD-project-title.md files |
| [Session memory](docs/session-memory/index.md) | Work and events in separate YYYY-MM-DD-project.md files |

Plans and reports name their project in a `## Project` section, and each index groups records by project. Older plans and reports without the section are listed last and are left as they are. Append same-day project work; create another file for another date. Preserve decisions, attempts, discoveries, reviews, verification, blockers and outcomes. Plans and reports hold detailed evidence linked from memory.

## Eight Skills

| Skill | Role |
|---|---|
| deliver-change | Delivery, coordination, spoke registration and inspection, GitHub comment triage and closure |
| write-implementation-plan | Living plans: creation, updates and implementation log, readiness review and validation |
| save-session-memory | Dated work records |
| write-test-report | Save or validate runtime evidence |
| verify-local-app | Run any application locally before its PR; authorized deployment |
| write-chris-street-style-code | Implementation standards and read-only code review |
| publish-builder-changes | Hub index refresh and document validation, scoped selected-file publication and push recovery |
| publish-spoke-changes | Spoke branch, PR preflight against the published runtime report, CI, merge and readback |

[AGENTS.md](AGENTS.md) owns shared workflow policy. Skills contain only task-specific guidance, with conditional details in references. Reuse verified plans and progress, load relevant memory sections, and ask for input only when a consequential decision or authority is actually missing.

Helpers retain deterministic filename/date, evidence, link and Git checks. See each skill for commands. The completed historical consolidation has a [read-only audit](.agents/skills/save-session-memory/references/migration-audit.md); archived instructions are not current policy.
