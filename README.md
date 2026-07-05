# Azurras

Azurras is an AI workflow hub for durable project planning, implementation workflow artifacts, and session continuity. The repository is designed to be opened as the starting point for work so agents can use the checked-in guidance, skills, and documentation conventions consistently.

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

The repository currently includes these workflow skills:

- `save-session-memory`: writes detailed dated session memory under `docs/session-memory/`.
- `save-project-spec`: saves Markdown project specs under `docs/specs/`.
- `save-implementation-plan`: saves Markdown implementation plans under `docs/implementation-plans/`.
- `commit-push-azurras-main`: commits and pushes completed Azurras repo changes to `main`, guarded to this repository and origin.
- `register-spoke-repo`: records external repositories coordinated from the hub.
- `start-hub-work`: creates a central work ledger for cross-repo initiatives.
- `dispatch-spoke-task`: writes task briefs for agents working in spoke repos.
- `ingest-spoke-update`: records returned status and results from spoke agents.
- `sync-spoke-state`: snapshots Git state for registered spoke repositories.
- `save-decision-record`: saves durable architecture or workflow decisions.
- `review-spoke-work`: records reviews of spoke repo changes.
- `close-hub-work`: saves final closure records for hub-and-spoke work.
- `update-hub-indexes`: regenerates Markdown indexes and `docs/active.md`.
- `validate-hub-state`: checks hub artifact conventions, links, statuses, templates, and skills.

Each skill contains a `SKILL.md`, optional helper scripts, and `agents/openai.yaml` UI metadata.
Shared Python helper code for skill scripts lives in `.agents/lib/`.

## Durable Artifacts

Use Markdown for durable workflow artifacts.

- Session memory: `docs/session-memory/YYYY-MM-DD-title.md`
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

For substantive completed requests:

1. Save session memory with `save-session-memory`.
2. Commit and push the repository with `commit-push-azurras-main`.

When saving a project spec or implementation plan, save the artifact first, then follow the same commit and push workflow.

## Hub-And-Spoke Workflow

For work that affects other repositories:

1. Register the external repo with `register-spoke-repo`.
2. Start a central work ledger with `start-hub-work`.
3. Dispatch focused spoke work with `dispatch-spoke-task`.
4. Ingest returned spoke results with `ingest-spoke-update`.
5. Refresh repository state with `sync-spoke-state`.
6. Record durable decisions with `save-decision-record`.
7. Review spoke changes with `review-spoke-work`.
8. Close the initiative with `close-hub-work`.

The hub keeps the state. Spoke repos hold implementation changes.

After changing durable hub artifacts, run `update-hub-indexes` and `validate-hub-state` before committing when practical.

## Git Scope

The commit/push skill is intentionally scoped to:

- Repository: `/Users/cbell/Developer/azurras`
- Branch: `main`
- Origin: `https://github.com/azurras/azurras.git`

Do not use that skill for other repositories.
