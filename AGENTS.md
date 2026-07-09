# AGENTS.md

## Repository Purpose

This repository is the `builder` AI workflow hub. Treat it as the starting point for project planning, implementation workflow artifacts, and durable session continuity.

## Repo-Scoped Skills

- Repo-scoped Codex skills live under `.agents/skills/`.
- Prefer the checked-in skills and their helper scripts for repeatable workflow tasks.
- Keep skills focused and update their `SKILL.md`, helper scripts, and `agents/openai.yaml` together when behavior changes.
- Shared helper code for skill scripts lives under `.agents/lib/`.

## Durable Artifacts

- Save session memory under `docs/session-memory/`.
- Save project specs under `docs/specs/`.
- Save implementation plans under `docs/implementation-plans/`.
- Save local app test reports under `docs/test-reports/`.
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

- When given a story, issue, ticket, bug, or feature request to complete, use the default delivery loop unless the user explicitly scopes the request to one phase: Story/Issue -> Spec -> Implementation Plan -> Develop -> Local Testing against the app -> Test Report -> Close Story/Issue -> Save Session Memory.
- Use `complete-story-issue` to orchestrate that loop and call the focused skills at each phase.
- Any Builder artifact created by a focused save skill that invokes `commit-push-builder-main` is a hard phase checkpoint: commit and push that artifact before moving to the next step in the delivery loop.
- Use `review-implementation-plan` before executing implementation plans and do not proceed from vague plans that lack literal line-range code edit blocks.
- Use `save-test-report` after local app testing to record what was tested, what data was sent, what response was received, pass/fail results, and evidence.
- Use `close-story-issue` before closing or updating the source story/issue to ensure closure text includes commits, validation, test report, known gaps, and session memory.
- For substantive completed requests, save session memory with `save-session-memory`.
- After saving session memory, a project spec, or an implementation plan, use `commit-push-builder-main` to commit and push the builder repo changes to `main`.
- For hub-and-spoke work, start with `start-hub-work`, register spoke repos with `register-spoke-repo`, dispatch tasks with `dispatch-spoke-task`, ingest spoke results with `ingest-spoke-update`, review with `review-spoke-work`, and close with `close-hub-work`.
- After updating durable artifacts, run `update-hub-indexes` and `validate-hub-state` before committing when practical.
- The commit/push workflow is scoped only to `C:\Users\Christopher\Developer\builder` on Windows or `/Users/cbell/Developer/builder` on macOS, branch `main`, and origin `https://github.com/azurras/builder.git`.
- Do not use the builder commit/push skill for any other repository.

## Git Hygiene

- Inspect `git status --short --branch` before committing.
- Keep `.DS_Store` and other local machine metadata out of commits.
- Use concise commit messages that describe the completed workflow update.
