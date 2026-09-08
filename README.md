# Builder

Builder is the workflow hub for planning, verification evidence, and project continuity.

## Documents

| Location | Purpose |
| --- | --- |
| [Implementation plans](docs/implementation-plans/index.md) | Requirements, acceptance criteria, design decisions, ordered tasks and verification |
| [Test reports](docs/test-reports/index.md) | Actual runtime inputs, responses, results and evidence |
| [Project session memory](docs/session-memory/index.md) | Dated progress, decisions, reviews, blockers, repository facts, publication and closure |

Session memory uses `YYYY-MM-DD-project.md`: a separate file for every date work occurred on a project. Record that day's work, requests, actions, decisions, discoveries, attempts, reviews, verification, blockers and outcomes. Append more same-day activity to the same file; create another file for a different date. Browse the [dated session records](docs/session-memory/index.md) for Builder, christopherbell.dev, and personal-computer cleanup.

Historical specs, spoke updates/reviews/tasks, work/closure records and per-request memories have been combined into the corresponding project memories with source navigation, dates, provenance and relocated links. Imported status is historical, not a claim about current production. Current AGENTS.md and skills define the workflow. There is no active.md; read the latest relevant project entries for progress.

## Workflow

Reviewed implementation plan -> development -> applicable verification -> publication -> project memory -> verified issue closure. Plans are published before development. Runtime reports remain required when runtime behavior changes; tooling-only work uses appropriate native checks. Append progress and decisions to project memory as work proceeds, then record final publication and closure there.

## Skills and Tools

Repo-scoped skills live in `.agents/skills/`; shared Python helpers are in `.agents/lib/`.

| Skill | Role |
| --- | --- |
| `complete-builder-work` | Delivery and verified closure |
| `plan-builder-work` | Implementation planning and read-only review/validation |
| `save-session-memory` | Record work and events in the appropriate dated project file |
| `record-runtime-verification` | Runtime report writing and validation |
| `coordinate-builder-work` | Actual handoffs and coordination recorded in project memory |
| `review-spoke-work` | Independent review, with authorized findings appended to memory |
| `manage-spoke-repositories` | Read-only Git inspection or explicit memory snapshot |
| `maintain-builder-hub` | Check or refresh the three indexes and validate documents |
| `commit-push-builder-main` | Publish reviewed selected Builder files |
| `verify-local-spring-app` | Isolated verification and authorized deployment |
| `write-jane-street-style-code` | Coding and review standard |

Append Markdown from stdin with `python .agents/skills/save-session-memory/scripts/save_session_memory.py --root . --project builder --title 'Progress update'`. Use the correct existing project slug. Run maintenance with `python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py check --root .`; explicitly use `refresh` after authorized changes.

The migration audit command is `python .agents/skills/save-session-memory/scripts/consolidate_project_memory.py --root . --source-commit 78f0183 --verify`. It compares imported bodies to the original Git corpus. Old helper paths that wrote separate artifacts are retired.

## Git Scope

Builder publication is restricted to `C:\Users\Christopher\Developer\builder` or `/Users/cbell/Developer/builder`, branch `main`, origin `https://github.com/azurras/builder.git`. Preserve unrelated work and review explicit file selections before committing.
