# Azurras

Azurras is an AI workflow hub for durable project planning, implementation workflow artifacts, and session continuity. The repository is designed to be opened as the starting point for work so agents can use the checked-in guidance, skills, and documentation conventions consistently.

## Repository Layout

```text
.
├── AGENTS.md
├── .agents/
│   └── skills/
├── docs/
│   ├── implementation-plans/
│   ├── session-memory/
│   └── specs/
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

Each skill contains a `SKILL.md`, optional helper scripts, and `agents/openai.yaml` UI metadata.

## Durable Artifacts

Use Markdown for durable workflow artifacts.

- Session memory: `docs/session-memory/YYYY-MM-DD-title.md`
- Project specs: `docs/specs/YYYY-MM-DD-title.md`
- Implementation plans: `docs/implementation-plans/YYYY-MM-DD-title.md`

Session memory should explain what happened in enough detail for a future agent to understand the project state without rereading the whole conversation.

## Completion Workflow

For substantive completed requests:

1. Save session memory with `save-session-memory`.
2. Commit and push the repository with `commit-push-azurras-main`.

When saving a project spec or implementation plan, save the artifact first, then follow the same commit and push workflow.

## Git Scope

The commit/push skill is intentionally scoped to:

- Repository: `/Users/cbell/Developer/azurras`
- Branch: `main`
- Origin: `https://github.com/azurras/azurras.git`

Do not use that skill for other repositories.
