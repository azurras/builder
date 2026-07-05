# 2026-07-04 - Create repository README

## 19:16 - Create repository README

### Request
The user asked to create a README for the azurras repo.

### Project Context
This repository is `/Users/cbell/Developer/azurras`, the azurras AI workflow hub. Durable repo instructions live in `/Users/cbell/Developer/azurras/AGENTS.md`. Repo-scoped skills live under `/Users/cbell/Developer/azurras/.agents/skills`, and session memory is stored under `/Users/cbell/Developer/azurras/docs/session-memory`. Per repo guidance, substantive completed requests should save session memory and then commit/push to `main` using the guarded `commit-push-azurras-main` skill.

### Work Completed
Created `/Users/cbell/Developer/azurras/README.md`. The README explains the repository purpose, the main directory layout, how `AGENTS.md` and `.agents/skills` fit together, the checked-in workflow skills, durable artifact locations, the completion workflow, and the scoped Git commit/push behavior.

The README documents these artifact conventions: session memory under `docs/session-memory/YYYY-MM-DD-title.md`, project specs under `docs/specs/YYYY-MM-DD-title.md`, and implementation plans under `docs/implementation-plans/YYYY-MM-DD-title.md`. It also records that `commit-push-azurras-main` is scoped to `/Users/cbell/Developer/azurras`, branch `main`, and origin `https://github.com/azurras/azurras.git`.

### Decisions
Kept the README concise and user-facing. It does not duplicate all of `AGENTS.md` or the full skill instructions; instead, it orients humans to where durable rules and reusable workflows live. Used ASCII-only Markdown and a compact tree diagram.

### Validation
Read the generated README after creation and confirmed it matches the current repo layout and workflow. Checked `git status --short --branch`, which showed only the new README before this memory file was saved.

### Current State
This memory entry was saved to `/Users/cbell/Developer/azurras/docs/session-memory/2026-07-04-create-repository-readme.md`. Pending changes now include the new README and this memory file. Per repo workflow, these changes should be committed and pushed to `origin main` with the guarded commit helper.

### Follow-ups
No follow-up is required for the README itself. Future documentation can expand the README if the workflow hub gains install instructions, plugin packaging, or additional repo-scoped skills.
