# 2026-07-04 - Create commit push azurras main skill

## 19:07 - Create commit push azurras main skill

### Request
The user asked to create a skill for committing and pushing code to `main` for only the azurras repo. They also specified that anytime session memory, a spec, or an implementation plan is saved, the repo should be committed and pushed to `main` for this repo.

### Project Context
This repository is `/Users/cbell/Developer/azurras`, an AI workflow hub. Repo-local skills are stored under `/Users/cbell/Developer/azurras/skills`. Session memory is stored under `/Users/cbell/Developer/azurras/docs/session-memory`. Project specs are saved under `docs/specs`, and implementation plans are saved under `docs/implementation-plans`. The Git branch is `main`, and `origin` is configured as `https://github.com/azurras/azurras.git`. Before this request, the repo had no commits yet and untracked workflow hub files.

### Work Completed
Created a new repo-local skill at `/Users/cbell/Developer/azurras/skills/commit-push-azurras-main`. The skill includes `SKILL.md`, `agents/openai.yaml`, and `scripts/commit_push_azurras_main.py`.

The skill instructions define a guarded commit/push workflow scoped only to `/Users/cbell/Developer/azurras`, requiring branch `main` and origin `https://github.com/azurras/azurras.git`. It instructs agents to inspect status, stage intended changes, commit with a clear message, push with `git push origin main`, and report the commit hash and push result.

The helper script validates the repo root, current branch, and origin remote before doing anything. It supports `--dry-run` for validation without staging, committing, or pushing. In normal mode it stages changes, excludes `.DS_Store` through the repo's `.gitignore`, commits with the supplied message, and pushes to `origin main`.

Added `/Users/cbell/Developer/azurras/.gitignore` with `.DS_Store` so local macOS metadata is not captured by the first automated commit.

Updated these existing skills so their workflows explicitly call `commit-push-azurras-main` after a successful save: `/Users/cbell/Developer/azurras/skills/save-session-memory/SKILL.md`, `/Users/cbell/Developer/azurras/skills/save-project-spec/SKILL.md`, and `/Users/cbell/Developer/azurras/skills/save-implementation-plan/SKILL.md`.

### Decisions
Named the new skill `commit-push-azurras-main` to make the repo and branch scope obvious. Chose a guarded helper script instead of plain Git instructions because committing and pushing to `main` is high-impact and should verify the exact repo, branch, and remote every time. Added the post-save rule to each save skill rather than embedding Git behavior directly into the save helper scripts, keeping file-writing helpers deterministic and keeping network/Git side effects in one explicit skill.

### Validation
Ran the commit helper in dry-run mode with message `Add azurras commit push workflow`; it confirmed repo `/Users/cbell/Developer/azurras`, branch `main`, remote `https://github.com/azurras/azurras.git`, showed the current untracked status, and exited without staging, committing, or pushing.

Ran `PYTHONPYCACHEPREFIX=/private/tmp/azurras-skill-pycache python3 -m py_compile` across the commit helper and existing save helper scripts; it passed. Ran a standard-library equivalent of the skill frontmatter checks across all repo-local skills; it passed. Ran `git check-ignore` for `.DS_Store` files at the repo root, docs, skills, and each skill folder; all were ignored.

Attempted the official `quick_validate.py` for the new skill, but it still fails in this environment because `PyYAML` is not installed.

### Current State
A new session memory file was created at `/Users/cbell/Developer/azurras/docs/session-memory/2026-07-04-create-commit-push-azurras-main-skill.md`. The repo now contains the new commit/push skill, updates to the three save skills, `.gitignore`, and prior uncommitted docs/skills artifacts. Per the user's new rule, this save should be followed by a guarded commit and push to `main` for the azurras repo.

### Follow-ups
Run `/Users/cbell/Developer/azurras/skills/commit-push-azurras-main/scripts/commit_push_azurras_main.py --message "Add azurras workflow hub skills"` to commit and push the accumulated workflow hub files to `origin main`. Network access and GitHub authentication may be required for the push.
