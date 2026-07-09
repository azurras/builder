# Issue 1152 MongoDB Backup and Restore Runbook Implementation Plan

## Document Status

ready-for-execution

## Objective

Add concise, discoverable production MongoDB backup and restore documentation for `christopherbell.dev` issue #1152.

## Goals

- Create an operations runbook with backup, restore, verification, expected storage, environment variables, and restore smoke-check steps.
- Link the runbook from the root README production section.
- Keep the change documentation-only and avoid application behavior changes.
- Verify unchanged app behavior with automated tests and a local app smoke request.

## Inputs

- Spec: `docs/specs/2026-07-09-issue-1152-mongodb-backup-and-restore-runbook-spec.md`.
- Source issue: https://github.com/azurras/christopherbell.dev/issues/1152.
- Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments are present.
- Spoke checkout: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1152-mongodb-backup-runbook`.
- Baseline validation: `:website:test` passed with worktree-local `GRADLE_USER_HOME`.

## Branch

- Repository: `azurras/christopherbell.dev`.
- Base: `origin/main` at `d5ac7aba5abf3a2c8e2ab9bd792273207eb6cda3`.
- Work branch: `agent/1152-mongodb-backup-runbook`.

## Non-Goals

- Do not add scripts, scheduled jobs, Docker Compose files, or cloud provider integrations.
- Do not change Java, Spring, Mongo schemas, application configuration, or runtime behavior.
- Do not include real production secrets or storage account identifiers.
- Do not complete issue #1153 local Docker Compose support.

## Assumptions

- Operators have MongoDB Database Tools available on the host where backup and restore commands run.
- The app can be smoke-tested against a restored database by setting `SPRING_DATA_MONGODB_URI` and a non-production `SERVER_PORT`.
- `BACKUP_DIR` should be configurable because the actual production storage path is environment-specific.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add MongoDB operations runbook

Sequence / dependencies:
- Runs first because the README link should point to the final runbook path.

Implementation notes:
- Create `docs/operations/mongodb-backup-restore.md`.
- Use placeholder environment variables for secrets and host-specific paths.
- Include explicit destructive-restore warning and a non-production smoke path.

#### Code Edit 1.1
- File: `docs/operations/mongodb-backup-restore.md`
- Lines: after 0
- Action: add

Proposed:
````markdown
# MongoDB Backup and Restore Runbook

Use this runbook for production MongoDB backups, restore preparation, and restore smoke checks for `christopherbell.dev`. Run the commands from a host that has network access to MongoDB and the MongoDB Database Tools installed.

### Required Environment

Set these values in the shell that runs the backup or restore commands:

```bash
export MONGODB_URI="mongodb://<host>:<port>"
export MONGODB_DATABASE="christopherbell"
export BACKUP_DIR="/var/backups/christopherbell.dev/mongodb"
export BACKUP_DATE="$(date -u +%Y%m%dT%H%M%SZ)"
export BACKUP_ARCHIVE="$BACKUP_DIR/$MONGODB_DATABASE-$BACKUP_DATE.archive.gz"
```

Use the production MongoDB URI format required by the deployment. If the URI already includes the database name, keep `MONGODB_DATABASE` set to the same database so archive names and restore commands stay explicit.

Optional values for restore validation:

```bash
export RESTORE_DATABASE="christopherbell_restore_check"
export RESTORE_URI="mongodb://<host>:<port>"
export SERVER_PORT=8082
```

### Storage Location

Store production archives under the host's protected backup area, rooted at:

```text
/var/backups/christopherbell.dev/mongodb
```

Archive filenames should use the database and UTC timestamp:

```text
christopherbell-YYYYMMDDTHHMMSSZ.archive.gz
```

Move or replicate completed archives to the production backup storage provider used for the host. Keep local filesystem permissions limited to the service or operator account that performs backups.

### Backup

Create the backup directory and run `mongodump` with a compressed archive:

```bash
mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"

mongodump \
  --uri="$MONGODB_URI" \
  --db="$MONGODB_DATABASE" \
  --archive="$BACKUP_ARCHIVE" \
  --gzip
```

Record the resulting archive path in the deployment or incident log for the change window.

### Verify a Backup

Confirm that the archive exists and is not empty:

```bash
test -s "$BACKUP_ARCHIVE"
ls -lh "$BACKUP_ARCHIVE"
```

List archive contents without restoring them:

```bash
mongorestore \
  --archive="$BACKUP_ARCHIVE" \
  --gzip \
  --dryRun
```

If either check fails, do not delete the previous known-good backup.

### Restore

Restores can overwrite data. Prefer restoring into a staging or temporary validation database first. Only restore into production after confirming the target URI, target database, and maintenance window.

Restore into a validation database:

```bash
mongorestore \
  --uri="$RESTORE_URI" \
  --nsFrom="$MONGODB_DATABASE.*" \
  --nsTo="$RESTORE_DATABASE.*" \
  --archive="$BACKUP_ARCHIVE" \
  --gzip \
  --drop
```

Restore into the original database only when the production target has been confirmed:

```bash
mongorestore \
  --uri="$MONGODB_URI" \
  --db="$MONGODB_DATABASE" \
  --archive="$BACKUP_ARCHIVE" \
  --gzip \
  --drop
```

### Restore Smoke Check

After restoring into a validation database, start the app against that database on a non-production port:

```bash
export SPRING_PROFILES_ACTIVE=local
export SPRING_DATA_MONGODB_URI="$RESTORE_URI/$RESTORE_DATABASE"
export SERVER_PORT=8082

./gradlew :website:bootRun
```

In another shell, request a public page:

```bash
curl -i "http://localhost:$SERVER_PORT/"
```

Expected result:

- HTTP status is `200 OK`.
- The response body contains the public home page title or markup.
- The application logs do not show MongoDB connection or authentication errors.

For production restores, repeat the same smoke pattern against the production process after the restore and deployment restart are complete.

### Operational Notes

- Keep at least one previously verified archive until the new archive has passed verification.
- Do not paste credentials into tickets, pull requests, or shell history shared with other users.
- Test restore procedures periodically against a non-production MongoDB instance.
- Document backup archive path, restore target, operator, timestamp, and smoke-check result in the deployment or incident log.
````

Verification:
- Review `docs/operations/mongodb-backup-restore.md` for required issue content and no secrets.

### Task 2 - Link runbook from README production docs

Sequence / dependencies:
- Runs after Task 1 because the link target must exist.

Implementation notes:
- Add a short discoverability subsection after the production run command.
- Do not duplicate the full runbook in the README.

#### Code Edit 2.1
- File: `README.md`
- Lines: after 372
- Action: add

Proposed:
````markdown

### MongoDB Backups and Restores

Use the MongoDB backup and restore runbook at `docs/operations/mongodb-backup-restore.md` for production backup commands, expected archive storage, restore steps, and restore smoke checks.
````

Verification:
- Review `README.md` production section renders the relative link correctly.

## Code Changes

- `docs/operations/mongodb-backup-restore.md`: add new Markdown runbook.
- `README.md`: add a MongoDB backup and restore link after line 372 in the Production section.

## Files and Modules

- `docs/operations/mongodb-backup-restore.md`
- `README.md`

## Unit Testing

- No unit tests are required for documentation-only edits.
- Run automated regression coverage for unchanged app behavior:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1152'; .\gradlew.bat --no-daemon :website:test`

## Local Testing

- Start the app locally on a non-production port:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1152'; $env:SERVER_PORT='8082'; .\gradlew.bat --no-daemon :website:bootRun`
- Send a public-page smoke request:
  - `curl.exe -i http://localhost:8082/`
- Expected response: `HTTP/1.1 200` and home-page HTML containing the page title.
- Stop the local process after verification.

## Validation

- Documentation diff has no secrets and covers all issue acceptance requirements.
- `:website:test` passes after the documentation change.
- Local app smoke test passes on port `8082` without touching any existing production process.
- Builder test report records data sent, response received, and pass/fail evidence.
- PR includes `Closes #1152`, required CI checks pass, PR merges, and issue closes.

## Rollback or Recovery

- Revert the documentation commit or remove `docs/operations/mongodb-backup-restore.md` and the README link if the runbook is inaccurate.
- Because the implementation is documentation-only, rollback does not require database, application, or configuration changes.

## Risks

- MongoDB command flags may differ across Database Tools versions. Mitigation: use standard `mongodump` and `mongorestore` archive flags and keep commands concise.
- Operators may accidentally target production during restore. Mitigation: document validation restore first and warn about destructive restore behavior.
- The actual production backup storage provider is environment-specific. Mitigation: document `BACKUP_DIR` as configurable and avoid inventing provider-specific paths.

## Completion Criteria

- Reviewed spec and reviewed implementation plan are saved and pushed in Builder.
- Spoke docs are implemented, committed, pushed, and opened as a PR.
- Automated tests and local app smoke verification pass.
- Builder test report is saved, validated, committed, and pushed.
- GitHub PR CI gates pass, PR merges, and issue #1152 closes.
- Builder closure and session memory are saved, indexed, validated, committed, and pushed.
