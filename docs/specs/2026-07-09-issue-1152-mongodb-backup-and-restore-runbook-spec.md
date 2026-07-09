# Issue 1152 MongoDB Backup and Restore Runbook Spec

## Document Status

ready-for-execution

## Purpose

Resolve `azurras/christopherbell.dev` issue #1152 by adding a concise production runbook for backing up, restoring, and verifying MongoDB data used by the Spring Boot site.

## Background

The `christopherbell.dev` app stores application state in MongoDB. The root README currently documents the MongoDB URI, local startup expectations, and production environment variables, but it does not describe production backup or restore operations. Issue #1152 asks for backup, restore, verification, required environment variables, expected storage location, and a restore smoke check.

Source issue: https://github.com/azurras/christopherbell.dev/issues/1152
Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments are present.

## Goals

- Add a production MongoDB backup and restore runbook in the spoke repository.
- Include concrete `mongodump` and `mongorestore` commands that use environment variables instead of hard-coded secrets.
- Document required and optional environment variables.
- Document the expected backup storage location and file naming convention.
- Document verification steps after backup creation.
- Document a restore smoke check that exercises the application after a restore.
- Link the runbook from the root README so it is discoverable from existing production docs.

## Non-Goals

- Do not add automation scripts, cron jobs, or cloud storage integrations.
- Do not change application code, MongoDB schemas, Spring configuration, or runtime behavior.
- Do not add real credentials, hostnames, bucket names, or production data paths specific enough to expose secrets.
- Do not require Docker Compose or local MongoDB setup changes; that is tracked separately by issue #1153.

## Requirements

- The runbook must be Markdown and live in a docs path appropriate for operational documentation.
- Commands must use `MONGODB_URI`, `MONGODB_DATABASE`, and backup-directory variables so operators do not paste secrets into the document.
- The backup procedure must create compressed archive backups with deterministic date-based names.
- The restore procedure must warn about destructive restore behavior and require restore-target confirmation.
- Verification must include archive presence, archive listing, and a local or staging restore validation path.
- The restore smoke check must verify the Spring app can start and serve a public page after pointing at the restored MongoDB database.
- The root README production section must link to the runbook without duplicating the full procedure.

## Proposed Approach

Add `docs/operations/mongodb-backup-restore.md` with sections for prerequisites, environment variables, backup storage, backup command, backup verification, restore command, restore smoke check, and operational notes. Use MongoDB Database Tools commands because they are the standard tooling for archive dumps and restores.

Update `README.md` under the Production area with a short `MongoDB Backups and Restores` subsection that links to the runbook.

## Files or Modules Involved

- `docs/operations/mongodb-backup-restore.md`: new operational runbook.
- `README.md`: add a short discoverability link in the Production section.

## Validation Plan

- Run a targeted documentation diff review for command correctness and absence of secrets.
- Run `:website:test` with worktree-local Gradle user home to ensure unchanged application behavior still passes automated tests.
- Run the Spring app locally with the local profile on a non-production port and request `/` to verify a public page still serves successfully.
- Save a Builder test report with the exact app command, URL, request, response, and pass/fail evidence.
- Open a PR with `Closes #1152`, wait for required GitHub CI gates, merge only after they pass, and verify the issue closes.

## Spec Review

No blockers remain.

- Acceptance criteria are sourced only from issue #1152 authored by `azurras`.
- The expected backup location is explicit: a configurable `BACKUP_DIR` rooted at the host's production backup area, with archive names including database and UTC date.
- The restore smoke check is explicit: restore into a non-production/staging or confirmed target database, start the app against that database, and request a public page.
- Non-goals prevent scope creep into automation, Compose support, or schema changes.

## Open Questions

None.
