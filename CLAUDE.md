# Claude Code Instructions

@AGENTS.md

AGENTS.md is the shared policy for every agent (Claude Code, Codex and ChatGPT). Keep agent-neutral rules there, not here.

Skills: canonical skills live in `.agents/skills/`. Claude Code discovers them through generated entrypoints in `.claude/skills/`, each of which delegates to its canonical SKILL.md. Edit only `.agents/skills/`, then run `python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py refresh --root .` to regenerate the entrypoints.
