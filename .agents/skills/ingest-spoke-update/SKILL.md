---
name: ingest-spoke-update
description: Record a returned update from an agent working in a spoke repository back into the Builder hub. Use when a spoke task reports progress, commits, pull requests, validation results, blockers, or completion status.
---

# Ingest Spoke Update

## Overview

Preserve spoke repo results in Builder so the hub remains the source of truth for cross-repo work.

## Storage Rules

- Store updates under `docs/spoke-updates/`.
- Name files `YYYY-MM-DD-title.md`.
- Write Markdown only.
- Link the related work record, task brief, spoke repo, commits, PRs, and validation evidence.

## Update Content

Capture source repo, reporting agent/thread, status, changes made, files touched, commit/PR links, tests run, blockers, risks, and next actions.

## Workflow

1. Read the spoke agent's returned update.
2. Normalize it into a durable Markdown update.
3. Save the update, preferring the helper script.
4. Update session memory and use `commit-push-builder-main`.

## Helper Script

```bash
python3 .agents/skills/ingest-spoke-update/scripts/ingest_spoke_update.py \
  --title "Update Title" \
  < spoke-update.md
```
