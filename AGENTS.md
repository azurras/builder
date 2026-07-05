# AGENTS.md

## Repository Purpose

This repository is the `azurras` AI workflow hub. Treat it as the starting point for project planning, implementation workflow artifacts, and durable session continuity.

## Repo-Scoped Skills

- Repo-scoped Codex skills live under `.agents/skills/`.
- Prefer the checked-in skills and their helper scripts for repeatable workflow tasks.
- Keep skills focused and update their `SKILL.md`, helper scripts, and `agents/openai.yaml` together when behavior changes.
- Shared helper code for skill scripts lives under `.agents/lib/`.

## Durable Artifacts

- Save session memory under `docs/session-memory/`.
- Save project specs under `docs/specs/`.
- Save implementation plans under `docs/implementation-plans/`.
- Save spoke repository registry and state under `docs/spokes/`.
- Save central work records under `docs/work/`.
- Save spoke task briefs under `docs/spoke-tasks/`.
- Save spoke updates under `docs/spoke-updates/`.
- Save spoke reviews under `docs/spoke-reviews/`.
- Save decision records under `docs/decisions/`.
- Save work closure records under `docs/work-closures/`.
- Save reusable artifact templates under `docs/templates/`.
- Use dated Markdown filenames in the form `YYYY-MM-DD-title.md` unless a specific skill defines a more precise convention.
- Do not create non-Markdown planning artifacts unless the user explicitly asks for them.
- Use the canonical statuses from `docs/status-model.md` for hub work and coordination artifacts.

## Completion Workflow

- For substantive completed requests, save session memory with `save-session-memory`.
- After saving session memory, a project spec, or an implementation plan, use `commit-push-azurras-main` to commit and push the azurras repo changes to `main`.
- For hub-and-spoke work, start with `start-hub-work`, register spoke repos with `register-spoke-repo`, dispatch tasks with `dispatch-spoke-task`, ingest spoke results with `ingest-spoke-update`, review with `review-spoke-work`, and close with `close-hub-work`.
- After updating durable artifacts, run `update-hub-indexes` and `validate-hub-state` before committing when practical.
- The commit/push workflow is scoped only to `/Users/cbell/Developer/azurras`, branch `main`, and origin `https://github.com/azurras/azurras.git`.
- Do not use the azurras commit/push skill for any other repository.

## Git Hygiene

- Inspect `git status --short --branch` before committing.
- Keep `.DS_Store` and other local machine metadata out of commits.
- Use concise commit messages that describe the completed workflow update.
