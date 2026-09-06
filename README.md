# Builder

Builder is an AI workflow hub for durable project planning, implementation workflow artifacts, and session continuity. The repository is designed to be opened as the starting point for work so agents can use the checked-in guidance, skills, and documentation conventions consistently.

## Repository Layout

```text
.
├── AGENTS.md
├── .agents/
│   ├── lib/
│   └── skills/
├── docs/
│   ├── decisions/
│   ├── implementation-plans/
│   ├── session-memory/
│   ├── test-reports/
│   ├── specs/
│   ├── spoke-reviews/
│   ├── spoke-tasks/
│   ├── spoke-updates/
│   ├── spokes/
│   ├── templates/
│   ├── work/
│   └── work-closures/
└── README.md
```

## Agent Guidance

`AGENTS.md` contains repo-wide instructions that Codex loads at the start of work in this repository. It defines the durable artifact locations, the completion workflow, and the Git safety rules for this hub.

Repo-scoped Codex skills live in `.agents/skills/` so future Codex sessions can discover them automatically from the repository root.

## Skills

The repository has 11 discoverable skills:

| Skill | Responsibility |
| --- | --- |
| `complete-builder-work` | Full delivery or closure-only work |
| `plan-builder-work` | Spec, plan, read-only review/validation, optional decision |
| `coordinate-builder-work` | Work ledger, actual dispatch, returned update, hub closure |
| `record-runtime-verification` | Save or validate local application evidence |
| `manage-spoke-repositories` | Inspect by default, explicit register or snapshot |
| `maintain-builder-hub` | Read-only check or explicit index refresh and validation |
| `commit-push-builder-main` | Publish selected Builder files with repository guards |
| `verify-local-spring-app` | Isolated Spring verification and authorized deployment |
| `write-jane-street-style-code` | Cross-language coding and review standard |
| `review-spoke-work` | Independent spoke review and merge-readiness evidence |
| `save-session-memory` | Durable continuity and verified closure result |

Each has `SKILL.md` and `agents/openai.yaml`; detailed modes live in focused references. Shared Python helpers live in `.agents/lib/`. Old CLI paths remain supported. See the [migration map](docs/skill-migration.md) for retired skill names.

## Durable Artifacts

Use Markdown for durable workflow artifacts.

- Session memory: `docs/session-memory/YYYY-MM-DD-title.md`
- Runtime test reports: `docs/test-reports/YYYY-MM-DD-title.md`
- Project specs: `docs/specs/YYYY-MM-DD-title.md`
- Implementation plans: `docs/implementation-plans/YYYY-MM-DD-title.md`
- Central work records: `docs/work/YYYY-MM-DD-title.md`
- Spoke task briefs: `docs/spoke-tasks/YYYY-MM-DD-title.md`
- Spoke updates: `docs/spoke-updates/YYYY-MM-DD-title.md`
- Spoke reviews: `docs/spoke-reviews/YYYY-MM-DD-title.md`
- Decisions: `docs/decisions/YYYY-MM-DD-title.md`
- Work closures: `docs/work-closures/YYYY-MM-DD-title.md`
- Spoke registry and state: `docs/spokes/`
- Templates: `docs/templates/`
- Status model: `docs/status-model.md`

Session memory should explain what happened in enough detail for a future agent to understand the project state without rereading the whole conversation.

## Completion Workflow

For complete issue/feature work, use `complete-builder-work`: spec, reviewed plan, implementation, applicable verification, publication, continuity, and verified closure. A request limited to one phase stays within that phase.

Each saved spec, plan, applicable runtime report, and continuity record is a separate publication checkpoint. Use the [phase finalizer](.agents/skills/maintain-builder-hub/references/phase-finalization.md) to refresh indexes, validate, and publish selected files. Maintenance and internal review do not create their own memory/commit cycles.

## Hub-And-Spoke Workflow

Use `manage-spoke-repositories` to establish repository context. `coordinate-builder-work` keeps one ledger and creates dispatch/update records only for actual handoffs or returned results. Review spoke changes with `review-spoke-work`, then close the initiative with evidence links and honest final status. Preserve full evidence in its primary report/review; link it from closure and continuity.

The hub keeps coordination state; spoke repositories hold implementation changes. Inspection and maintenance checks are read-only by default. Explicit snapshot/refresh modes persist intended state.

## Git Scope

The commit/push skill is intentionally scoped to:

- Windows repository: `C:\Users\Christopher\Developer\builder`
- macOS repository: `/Users/cbell/Developer/builder`
- Branch: `main`
- Origin: `https://github.com/azurras/builder.git`

Do not use that skill for other repositories.
