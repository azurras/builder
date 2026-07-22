# ChristopherBell.dev Shared Folder Alternate-Port Acceptance

## Document Status

complete

This report covers the isolated local runtime checkpoint. Production rollout remains separate.

## Story/Issue

Builder work item: `docs/work/2026-07-17-christopherbell-dev-shared-folder-portal.md`.

Verify the authenticated shared-folder portal, independent read/write permissions, resumable
transfers, media preview/fallback, recycle administration, and audit coverage before merge.

## Branch

- Repository: `azurras/christopherbell.dev`
- Branch: `codex/shared-folder-worker`
- Commits: `fbe3769cfd894a75f45fed1b124ecbaf7450ccde` through
  `f91d404c8056bd6b8b316b41909ee0528964331a`
- Pushed remote head: `f91d404c8056bd6b8b316b41909ee0528964331a`

## App / Environment

- App: ChristopherBell.dev Spring Boot website on native Windows.
- Profiles: `prod,deploy-smoke`.
- Base URL: `http://127.0.0.1:8090`.
- JAR: `A:\Projects\christopherbell.dev-worktrees\shared-folder-worker\website\build\libs\website.jar`.
- Mongo database: `christopherbell_shared_folder_acceptance`.
- Visible root: `A:\Temp\cbdev-shared-folder-acceptance-20260722-061901\visible`.
- Private root: `A:\Temp\cbdev-shared-folder-acceptance-20260722-061901\private`.
- Limits: 16 MB upload, 1 MB chunk, 1 MB reserve, 64 MB transcode cache.
- Host actions and sensor libraries were disabled. Secrets and bearer tokens were ephemeral and
  are omitted.

## Local Run Details

The candidate was built and started from the spoke worktree:

```powershell
$env:GRADLE_USER_HOME='A:\Temp\codex-gradle-shared-folder-red'
.\gradlew.bat :website:bootJar --no-daemon
.\.superpowers\sdd\start-task10-candidate.ps1 `
  -BasePath 'A:\Temp\cbdev-shared-folder-acceptance-20260722-061901' `
  -Port 8090
```

The launcher used `-Xrs`, `--enable-native-access=ALL-UNNAMED`, profiles `prod,deploy-smoke`, and
port 8090. PID 21348 returned status code: 200 from `/`; the body was 3,912 UTF-8 bytes and
contained `<title>CB | Home</title>`.

The runtime harness was:

```powershell
.\.superpowers\sdd\run-task10-acceptance.ps1 `
  -BasePath 'A:\Temp\cbdev-shared-folder-acceptance-20260722-061901' `
  -Port 8090
```

Logs were written to the candidate base under `logs/candidate.out.log` and
`logs/candidate.err.log`. After evidence capture, PID 21348 was validated as the isolated
candidate and stopped. Port 8090 was confirmed closed. Production port 8080 was untouched.

## Test Cases

| Case | Behavior | Checks | Result |
| --- | --- | ---: | --- |
| Accounts | Created admin, reader, writer, and no-permission accounts; promoted admin; logged in all actors. | 9 | Pass |
| Authorization | Granted read/write; denied no-permission read and reader mutation. | 4 | Pass |
| Fresh permissions | Same reader token observed immediate revoke and re-grant. | 4 | Pass |
| Read flows | Listed, range-downloaded, text-previewed, and full-downloaded. | 4 | Pass |
| Resumable upload | Created, hash-appended, resumed, and completed an upload. | 4 | Pass |
| Conflict fences | Rejected implicit replacement and racing cancellation with `409`. | 4 | Pass |
| Recycle admin | Recycled, listed, restored, recycled again, and exact-phrase purged. | 5 | Pass |
| Media | FLAC direct preview/probe; MKV fallback queue/status/cancel. | 5 | Pass |
| Audit | Found required permission, list, finalize, restore, purge, and media actions. | 1 | Pass |
| Smoke | `/` returned the expected home page. | 1 | Pass |

Total: 41 passed, 0 failed.

## Data Sent

Protected requests used the appropriate ephemeral bearer token; values are redacted.

- `PATCH /api/accounts/2026-07-17/{id}/shared-folder-permissions` with read-only and read/write
  JSON bodies.
- `GET /api/shared-folder/2026-07-17/entries` as no-permission, reader, revoked-reader, and
  restored-reader actors.
- `POST /api/shared-folder/2026-07-17/folders` with an empty parent and a unique folder name.
- `GET /api/shared-folder/2026-07-17/content?path=hello.txt` with `Range: bytes=0-5`.
- `GET /api/shared-folder/2026-07-17/preview?path=hello.txt`.
- `POST /api/shared-folder/2026-07-17/uploads` with `expectedBytes: 33`, SHA-256, and no
  replacement token; then hash-authenticated chunk, status, and complete requests.
- Recycle requests carried the relative path and observation token; purge carried exact
  confirmation `PURGE {id}`.
- Media requests carried relative FLAC/MKV paths and fixed profile `VIDEO_MP4`.
- `GET /api/shared-folder/2026-07-17/admin/audit?limit=200` as admin.

## Response Received

The running app returned these HTTP responses:

- Smoke status code: 200, 3,912 bytes, title `CB | Home`.
- No-permission read and reader mutation status code: 403.
- Listing and same-token re-grant status code: 200; listing contained `hello.txt`.
- Same-token revocation status code: 403 without another login.
- Range status code: 206; response body exactly `shared`; exactly one `Content-Range` matched
  `bytes 0-5/{total}`.
- Text preview status code: 200; JSON contained `acceptance fixture`.
- Upload create status code: 201; append/status/complete status code: 200; next offset was 33.
- Full download status code: 200; body matched all 33 bytes and had zero `Content-Range` headers.
- Implicit replacement and racing cancellation status code: 409.
- Recycle/purge status code: 204; list/restore status code: 200.
- FLAC status code: 200 with `audio/flac`; direct probe mode was `DIRECT_PROBE`.
- MKV fallback status code: 202 with `QUEUED` and job ID; status/cancel status code: 200.
- Audit status code: 200 with `PERMISSION_CHANGE`, `LIST`, `UPLOAD_FINALIZE`, `RESTORE`,
  `PURGE`, and `MEDIA_QUEUED`.

## Pass / Fail

Pass. All 41 isolated runtime checks succeeded. Independent final review reported 0 Critical,
0 Important, and 0 Minor findings after the range-header and bounded-stream regressions were
fixed test-first.

Supporting verification passed: 1,053 Java tests with 0 failures, 0 errors, and 3 expected skips;
165 JavaScript tests; worker PowerShell 7 Pester 56/56; operations PowerShell 7 Pester 28/28;
and operations Windows PowerShell 5.1 Pester 28/28. The post-review Java/JavaScript gate passed,
and `git diff --check` was clean.

## Evidence

- `A:\Temp\cbdev-shared-folder-acceptance-20260722-061901\candidate.json` recorded PID 21348,
  port 8090, status 200, 3,912 body bytes, title, roots, database, logs, and JAR.
- Harness summary: `Checks: 41`, `Passed: 41`; every named result had `Passed: true`.
- Runtime assertions covered response status, body bytes, range-header count, upload offset, MIME,
  media mode/state, and audit actions.
- `.\gradlew.bat clean test :website:sharedFolderVerification --no-daemon --console=plain`:
  `BUILD SUCCESSFUL` in 1 minute 57 seconds with 19 executed actions.
- `.\gradlew.bat test :website:jsTest --no-daemon --console=plain`: `BUILD SUCCESSFUL` in
  1 minute 23 seconds after final review.

## Bugs / Follow-ups

No alternate-port acceptance defect remains.

The installed-worker security group remains intentionally unrun because
`ChristopherBellMediaWorker`, `A:\Shared`, and `A:\Shared-System` are not installed at this
non-elevated checkpoint. Run it during controlled production installation. PR/CI/merge,
production rollout and verification, Builder closure, and session memory remain.
