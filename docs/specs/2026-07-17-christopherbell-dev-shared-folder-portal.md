# christopherbell.dev Shared Folder Portal Spec

## Document Status

`ready-for-execution`. The interactive design and written spec were approved on July 17, 2026. The service-identity architecture correction was approved the same day after source inspection. Implementation remains gated on an execution-ready implementation plan.

## Purpose

Add a secure shared-folder portal to christopherbell.dev so authorized account holders can browse a dedicated folder on the production Windows host, download files, preview safe documents, play media with minimal format friction, and—when separately authorized—manage the folder through the website.

The feature should feel like a small authenticated shared drive rather than a public file host or a literal FTP server. The filesystem remains the source of truth, so files placed directly into the shared folder from Windows become visible without an import step.

## Source Request and Decisions

The source request is a direct feature request from the site owner rather than an existing GitHub issue.

Approved decisions:

- The shared filesystem root is `A:\Shared`.
- The complete folder tree is available through one authenticated portal rather than through per-file grants.
- Existing `USER`, `MOD`, and `ADMIN` roles remain unchanged.
- Independent `SHARED_FOLDER_READ` and `SHARED_FOLDER_WRITE` account permissions control the portal.
- `SHARED_FOLDER_WRITE` implies `SHARED_FOLDER_READ`; removing READ also removes WRITE.
- Administrators always receive both effective shared-folder permissions.
- Back Office administrators can grant and remove READ and WRITE for non-admin accounts.
- Writers can upload, create folders, rename, move, replace, and delete files and folders.
- Individual uploads are limited to a configurable 10 GB by default.
- Browser-compatible media plays directly. Unsupported media is progressively transcoded and cached.
- Safe inline previews cover raster images, PDFs, plain text, Markdown, logs, and source code. Active or unknown content is download-only.
- The transcode cache is capped at 250 GB by default using least-recently-used eviction.
- Uploads and new transcodes stop before free space on `A:` falls below 100 GB.
- Deleted items enter an isolated 30-day recycle area rather than being immediately destroyed.
- Audit records are retained for 180 days by default.
- The implementation is integrated into the existing Spring Boot application.
- The existing website service identity remains unchanged because Command Center requires its current Windows privileges; FFmpeg and ffprobe instead run through a separate restricted local worker.

## Background

christopherbell.dev is a Java 25, Spring Boot 4.1 application with Thymeleaf templates, vanilla browser JavaScript, MongoDB, JWT authentication, method security, and an existing administrative Back Office. The application already models the hierarchical roles `USER`, `MOD`, and `ADMIN`; `PermissionService.hasAuthority` treats MOD and ADMIN as satisfying USER-level checks.

The authoritative spoke checkout is `A:\Projects\christopherbell.dev`. When inspected for this feature, its primary checkout was clean but divergent from `origin/main`, so implementation must use a clean isolated worktree based on refreshed `origin/main` and must not rewrite or clean the authoritative checkout.

The same Windows desktop hosts development and production. Production traffic must remain on port 8080 while the feature is developed and verified on another port. The host has a 13th Gen Intel Core i5-13600K, an NVIDIA GeForce RTX 4070, and an NTFS `A:` volume of approximately 4 TB with approximately 1.11 TB free at design time. FFmpeg and ffprobe were not available on the active PATH during design inspection.

## Goals

- Provide an authenticated `/shared` page that represents the full `A:\Shared` tree.
- Make directly placed Windows files visible without database import or duplication.
- Separate shared-folder capabilities from the existing role hierarchy.
- Allow administrators to manage shared-folder permissions from Back Office.
- Allow READ users to browse, preview, play, and download originals.
- Allow WRITE users to perform complete shared-drive file management through safe, recoverable operations.
- Support large, resumable uploads without holding complete files in application memory.
- Play compatible media directly with HTTP range requests.
- Detect incompatible media using stream metadata plus browser feedback, then progressively transcode and cache a compatible derivative.
- Keep cached derivatives, upload staging, and recycled files isolated from the visible shared tree.
- Prevent traversal, link/reparse-point escape, active-content execution, disk exhaustion, uncontrolled transcoding load, and silent overwrite races.
- Record permission, content-access, mutation, and transcode activity without recording secrets or file contents.
- Preserve public-site availability when the shared folder, FFmpeg, GPU acceleration, cache, or individual files are unavailable.
- Complete automated tests, alternate-port local app verification, a Builder test report, PR/CI/merge, production deployment verification, closure, and session memory.

## Non-Goals

- No anonymous access, public bearer links, or links that bypass account permissions.
- No per-file or per-folder access-control lists in version one; permission grants apply to the complete shared tree.
- No FTP, SFTP, SMB, WebDAV, desktop sync client, mapped drive, or operating-system network share.
- No exposure of arbitrary host paths or selection of a filesystem root through a request.
- No in-browser editing of documents, source files, images, audio, or video.
- No Office-document conversion or editing in version one; Office files remain downloadable.
- No execution of HTML, SVG, scripts, executables, archives, or unknown formats in the browser.
- No source-media mutation or replacement during transcoding.
- No unbounded concurrent transcoding; version one runs a single low-priority job.
- No permanent deletion by ordinary WRITE users.
- No broad rewrite of the account-role or authentication system.
- No requirement that every possible corrupt or proprietary format become playable when FFmpeg cannot decode it.

## Permission Model

### Stored Permissions

Add a focused account-permission model separate from `Role`, with at least:

- `SHARED_FOLDER_READ`
- `SHARED_FOLDER_WRITE`

MongoDB account documents that predate the feature and have no permission field deserialize to an empty set. Existing non-admin accounts receive no shared-folder access through migration or role inference.

### Effective Permissions

- ADMIN always has effective READ and WRITE, even if the stored set is absent.
- WRITE always produces effective READ.
- Granting WRITE stores or normalizes both WRITE and READ.
- Removing READ also removes WRITE.
- Back Office must not allow an administrator to strand an account in a write-only state.
- An administrator's own effective shared-folder access cannot be accidentally removed through Back Office.
- MOD has no shared-folder access by default; MOD accounts receive capabilities only through explicit grants.

### Enforcement

Every controller method and underlying service operation independently enforces the required capability. Browser button visibility is only presentation and never the authorization boundary.

- READ is required for listings, metadata, copyable links, safe previews, media inspection, native playback, derivative playback, and original downloads.
- WRITE is required for upload sessions, upload chunks, finalization, directory creation, rename, move, explicit replace, and recycle operations.
- ADMIN is required for permission management, audit browsing, recycle restoration, and permanent recycle purge.

## User Experience

### Navigation and Links

- Add a dedicated `/shared` page for authorized users.
- Show a Shared Folder navigation entry only when the current account has effective READ.
- Use breadcrumb navigation and a sortable folder/file listing with name, type, size, modified time, and media/preview state.
- Support responsive desktop and phone layouts without adding a frontend framework or build system.
- Files placed directly into `A:\Shared` appear on the next listing refresh.
- Every file and folder has a copyable christopherbell.dev URL based on its safe relative path.
- A signed-out visitor following a shared URL is sent to login and returned to the original location after successful authentication.
- A copied URL never grants permission by possession alone and returns a non-sensitive access error when the account lacks READ.
- A URL may stop resolving after the underlying item is renamed, moved, or deleted; stable content IDs and rename-following links are not a version-one requirement.

### Read Experience

- Folders open within the portal and preserve breadcrumbs.
- Safe previewable files open in a dedicated preview surface with an explicit Download Original action.
- Media opens in native browser controls with playback, pause, volume, seeking when available, and Download Original.
- When conversion is required, show queued, inspecting, transcoding, buffering, ready, failed, canceled, and insufficient-space states.
- A user can download the untouched original while a derivative is queued or running.
- Unsupported preview types display metadata and a download action without rendering active content.

### Write Experience

- Support drag-and-drop and file-picker uploads, with per-file progress, pause/cancel where supported, network retry, and resume.
- Support uploads up to a configurable 10 GB per file by default.
- Support New Folder, Rename, Move, Replace, and Delete actions.
- Never silently overwrite an existing item.
- A name conflict requires a different name or an explicit replace confirmation.
- Partial uploads never appear in the visible tree.
- Concurrent external or website changes return a refresh-and-retry conflict instead of overwriting unexpected content.
- Delete moves the item into the private recycle area and records its original relative path.
- Only admins restore or permanently purge recycled items in version one.

### Back Office

- Extend the existing user-management view with Shared Folder Read and Shared Folder Write controls.
- Show effective permission state, including the ADMIN default and WRITE-implies-READ rule.
- Confirm permission removals that will revoke active access.
- Provide an admin-only shared-folder activity view with filters for account, action, outcome, relative path, and date.
- Provide an admin-only recycle view with restore and permanent-purge controls.

## Filesystem and Storage Design

### Configured Paths

Production defaults:

- Visible shared root: `A:\Shared`
- Private feature data root: `A:\ChristopherBellDevSharedData`
- Upload staging: `A:\ChristopherBellDevSharedData\staging`
- Transcode cache: `A:\ChristopherBellDevSharedData\cache`
- Recycle storage: `A:\ChristopherBellDevSharedData\recycle`

All paths are typed configuration properties and validated at startup. The visible root and private roots must be distinct and must reside on the intended NTFS volume. The website exposes no endpoint that accepts or changes these absolute paths.

### Path Confinement

- Resolve requests only from normalized relative path segments beneath the configured visible root.
- Reject absolute paths, drive-qualified paths, UNC paths, `.`/`..` traversal, NUL/control characters, alternate-data-stream syntax, Windows device names, and ambiguous trailing dots or spaces.
- Reject symbolic links, junctions, mount points, and other reparse points in every traversed segment and at the final target.
- Recheck confinement immediately before each filesystem mutation to reduce time-of-check/time-of-use risk.
- Do not follow filesystem metadata that would escape the configured root.
- Reserve private feature-directory names and prevent users from creating aliases that collide with them.
- Return safe relative paths to clients and audit storage; never return absolute host paths.

### Uploads and Atomicity

- Stream fixed-size chunks directly to private staging storage rather than buffering complete uploads in JVM memory.
- Persist resumable upload-session metadata with owner, destination, expected size, received ranges, source filename, timestamps, and expiration.
- Bind upload sessions to the creating account and destination; another account cannot append or finalize them.
- Enforce the per-file size limit before and during upload.
- On completion, verify received ranges and expected length before an atomic move into the visible tree where the filesystem permits.
- Expire abandoned staging sessions after a configurable interval, defaulting to 24 hours.
- Use an observed-item token based on safe path, size, and modification time for replace, rename, move, and delete concurrency checks.

### Recycle and Cleanup

- Move deleted items to private recycle storage with metadata that records the original relative path, deleting account, deletion time, and source fingerprint.
- Default retention is 30 days.
- Restore fails with a conflict when the original destination is occupied; it never overwrites implicitly.
- Permanent purge is admin-only and requires explicit confirmation.
- Scheduled cleanup may purge only expired recycle entries, expired staging sessions, and evictable transcode-cache entries.
- Cleanup code must prove its target remains under the corresponding private root before removing content.
- Cache or staging cleanup never deletes `A:\Shared` content.

### Disk Protection

- Default minimum free-space reserve: 100 GB on `A:`.
- Reject new upload chunks, upload finalization that increases visible usage, and new transcodes before the reserve would be breached.
- Existing reads and original downloads continue during low-space conditions.
- Surface current storage availability and the blocking reason without exposing unrelated volume information.

## Preview and Content-Serving Design

### Original Downloads

- Preserve the original filename and bytes.
- Use safe `Content-Disposition` handling with correctly encoded filenames.
- Set `X-Content-Type-Options: nosniff`.
- Treat untrusted and active types as attachments.
- Support bounded streaming and client disconnects without loading whole files into memory.

### Safe Inline Previews

- Raster images: safe browser-supported images may render inline; large images receive bounded thumbnails/previews.
- Unsupported but decodable raster images may receive a cached JPEG or WebP preview while the original remains downloadable.
- PDF: serve through the browser PDF viewer with restrictive response headers and without embedding arbitrary active content in application markup.
- Text, Markdown, logs, and source code: decode with a conservative charset policy, cap preview bytes/lines, escape all content, and render as text rather than HTML.
- Markdown preview in version one is a safe text-oriented view; raw HTML is not executed.
- SVG, HTML, XML with active features, scripts, executables, archives, Office documents, and unknown formats are download-only.

### Native Media

- Inspect container and stream codecs with ffprobe rather than trusting the extension or request MIME type.
- Compare detected streams with a maintained browser-compatible profile.
- Serve compatible originals directly with correct media type, `Accept-Ranges`, `206 Partial Content`, `Content-Range`, and bounded range validation.
- FLAC and compatible Matroska files play directly when their actual codec combination is supported.
- Browser playback errors can request the transcode fallback even when server-side inspection predicted compatibility.
- Log one logical playback/download start rather than every range request.

## Progressive Transcoding

### Job Lifecycle

1. Inspect the source with a pinned ffprobe executable and a strict timeout.
2. Determine whether the original can play directly or requires a derivative.
3. Deduplicate work using a cache key derived from safe relative path, source size, source modification time, output profile, and transcode-profile version.
4. Queue at most one active low-priority transcode job in version one.
5. Prefer NVIDIA hardware encoding on the RTX 4070 when available and verified; use a bounded software fallback when configured.
6. Produce a fragmented browser-compatible H.264/AAC MP4 or compatible audio derivative without modifying the source.
7. Expose progressive bytes after a conservative initial buffer so playback can begin while encoding continues.
8. Publish the completed derivative atomically into private cache storage.
9. Mark failures with a safe category and keep original download available.

The implementation plan must inspect and choose the exact progressive-delivery mechanism. It must support initial playback while output grows, bounded waiting, client disconnects, no duplicate encoder per source, and ordinary range responses after completion. It must not claim arbitrary seek support beyond the portion already produced.

### Resource Bounds

- One active transcode job by default.
- Configurable queue length, per-account queue limit, process timeout, initial-buffer target, and maximum output size.
- Run FFmpeg at low operating-system priority where practical.
- Never build executable paths, codec names, output paths, or command fragments from raw request text.
- Use fixed output profiles and `ProcessBuilder` argument arrays.
- Capture bounded diagnostics; do not return raw command lines or unbounded stderr to clients.
- Cancellation terminates only the owned process tree and removes only its validated partial cache target.
- FFmpeg or GPU failure degrades transcoding only; listings, previews, and original downloads remain available.

### Cache Policy

- Default maximum cache size: 250 GB.
- Evict least-recently-used completed derivatives when the cap or disk reserve requires space.
- Never evict an active derivative or one currently being streamed.
- Source path, size, modification time, or profile changes invalidate the prior derivative.
- Stale derivatives are private disposable data and are not visible in listings.
- Cache loss causes regeneration on demand and never affects originals.

## API Ownership

Use versioned APIs under a focused shared-folder feature package. Exact record names may be finalized in the implementation plan, but the surface must separate these responsibilities:

- List and inspect an item by safe relative path.
- Stream/download original content with range support.
- Request and inspect a safe preview.
- Create, append to, inspect, cancel, and finalize resumable upload sessions.
- Create a directory.
- Rename or move an item with an observed-item token.
- Explicitly replace an existing item.
- Move an item to recycle.
- Request transcode fallback, read job status, cancel an owned queued/running request, and stream progressive/completed output.
- Administer account shared-folder permissions.
- Browse admin audit activity.
- Browse, restore, and permanently purge recycle entries as an administrator.

Controllers remain thin. Filesystem rules, authorization invariants, upload state, media decisions, job orchestration, cache policy, recycle behavior, and audit creation belong in separately testable services with explicit interfaces.

## Audit Model

Store shared-folder audit records in MongoDB with a 180-day default retention policy and a supporting expiration index where appropriate.

Record:

- Permission grants, removals, normalization, and rejected permission changes.
- Upload start/finalize/cancel/expire and explicit replace.
- Folder creation, rename, move, recycle, restore, and purge.
- Download and preview/playback start, deduplicated across range requests.
- Rejected access and invalid-path attempts.
- Transcode queue, start, ready, cancel, timeout, insufficient-space, and failure outcomes.

Each record includes account identifier, action, safe relative path or non-sensitive resource identifier, timestamp, source IP resolved through the existing trusted-proxy boundary, size when applicable, outcome, and safe failure category. Records exclude JWTs, authorization headers, passwords, request bodies, file contents, absolute paths, raw FFmpeg command lines, and unbounded tool output.

## Security and Service Identity

- Permit only the data-free `/shared` page shell through the public-route allowlist because browser navigation cannot send the JWT stored in local storage. Its JavaScript must redirect signed-out visitors through login and reveal no filenames, paths, permissions, storage state, or media data before an authenticated API check succeeds.
- Keep every shared-folder data, content, mutation, permission, audit, recycle, and transcode API out of the public-route allowlist.
- Enforce current-account active/approved state and effective capabilities at the controller and service boundary.
- Apply endpoint-aware rate limits to upload-session creation, chunk writes, mutation requests, permission changes, and transcode requests.
- Set restrictive content headers for every preview and download response.
- Never render filenames, paths, metadata, text contents, or diagnostic messages as unsanitized HTML.
- Preserve the existing trusted-proxy client-IP rules for audit and throttling.
- Do not execute uploaded files.
- Continue relying on host real-time antimalware protection for filesystem writes; explicit antivirus orchestration is not part of version one.

Production must not run uploaded media parsers, ffprobe, or FFmpeg in the privileged website process. Keep the existing website service identity because Command Center directly invokes Windows service, shutdown/reboot, and privileged sensor operations. Run all media inspection and transcoding through a separate restricted local worker identity. Give that worker read-only access to `A:\Shared`, modify access only to its private job, staging, and cache roots, and no access to application secrets, deployment controls, service controls, or shutdown privileges. The Spring application owns authorization, queue admission, validated job creation, status presentation, and output delivery; the worker accepts only constrained job descriptors and fixed transcode profiles. The implementation plan must verify worker ACL isolation, process identity, job validation, failure containment, and website/Command Center behavior before production cutover.

## Error Handling

- `400 Bad Request`: invalid relative path, invalid name, malformed range, invalid operation, or unsafe target.
- `401 Unauthorized`: missing or expired authentication.
- `403 Forbidden`: authenticated account lacks the required capability.
- `404 Not Found`: item no longer exists or is intentionally concealed.
- `409 Conflict`: destination collision, stale observed-item token, occupied restore target, or incompatible concurrent operation.
- `413 Content Too Large`: configured per-file upload limit exceeded.
- `416 Range Not Satisfiable`: invalid or unavailable byte range.
- `429 Too Many Requests`: endpoint, account, or transcode-queue limit exceeded.
- `507 Insufficient Storage`: disk reserve or cache-output bound would be breached.
- `503 Service Unavailable`: shared root, media inspector, or transcode capability temporarily unavailable when no narrower response applies.

Errors shown to users identify the failed action and recovery step without exposing absolute paths, stack traces, tokens, command lines, internal account data, or unrelated filesystem metadata.

## Expected Files and Modules

Source inspection during implementation planning should confirm exact line ranges. Expected ownership includes:

- `website/src/main/java/dev/christopherbell/sharedfolder/**`: domain facade, filesystem, upload, preview, media, transcode, recycle, audit, permission, and model boundaries.
- `website/src/main/java/dev/christopherbell/account/model/**`: independent stored account permissions with backward-compatible Mongo behavior.
- `website/src/main/java/dev/christopherbell/permission/**`: effective-permission helpers only where shared authorization ownership belongs there.
- `website/src/main/java/dev/christopherbell/configuration/**`: typed shared-folder path, size, retention, cache, queue, and FFmpeg properties.
- `website/src/main/java/dev/christopherbell/view/**`: protected `/shared` page route.
- `website/src/main/resources/templates/shared-folder.html`: portal shell.
- `website/src/main/resources/static/js/shared-folder.js`: navigation, operations, upload, preview, playback, and job status.
- `website/src/main/resources/static/js/lib/api.js`: versioned route constants.
- Existing Back Office JavaScript/template/controller/model files: permission, activity, and recycle administration.
- `website/src/main/resources/static/css/main.css` or a focused directly loaded stylesheet plus ownership documentation.
- Profile configuration and Windows production-service/deployment files: paths, limits, FFmpeg, and restricted identity.
- Focused Java and browser tests matching every new service and UI boundary.
- Feature-package and operational documentation updated with behavior, configuration, storage, recovery, and deployment rules.

## Validation Plan

### Automated Validation

- Develop permission, filesystem, upload, media, and mutation behavior test-first.
- Test missing permission fields, ADMIN defaults, WRITE-implies-READ, READ removal, MOD behavior, and Back Office updates.
- Test anonymous, expired-token, no-permission, READ, WRITE, MOD, and ADMIN paths for every relevant API.
- Test traversal, drive-qualified and UNC paths, alternate data streams, reserved names, case behavior, long names, symlinks, junctions, mount points, reparse points, and pre-mutation rechecks.
- Test listing, external filesystem additions/removals, chunk ordering, resume, duplicate chunks, size enforcement, expiration, atomic finalization, collisions, explicit replace, concurrency tokens, move, rename, recycle, restore, and purge.
- Test low-space refusal and prove reads continue.
- Test safe preview allowlists, preview limits, escaping, content-disposition handling, `nosniff`, and active-content rejection.
- Test complete and partial range responses, invalid ranges, disconnects, FLAC, compatible MKV, browser fallback, and logical access-event deduplication.
- Test ffprobe success, timeout, malformed output, missing executable, supported/unsupported codec decisions, hardware encoder availability, software fallback policy, progressive output, initial buffering, queue bounds, deduplication, cancellation, process-tree cleanup, source changes, cache reuse, eviction, and failures.
- Test JavaScript folder navigation, copied links, upload progress/resume/cancel, conflict prompts, playback, fallback, transcode progress, unavailable states, Back Office invariants, audit filters, recycle restore/purge, and safe text rendering.
- Run focused tests first, then `:website:test`, `:website:jsTest`, syntax checks for touched JavaScript, and `:website:build` using an isolated Windows Gradle user home if required.

### Local App Validation

- Use a clean isolated worktree based on refreshed `origin/main`.
- Start the app on a non-production port and leave port 8080 untouched.
- Use temporary visible/private roots separate from production `A:\Shared` and `A:\ChristopherBellDevSharedData`.
- Exercise accounts with no capability, READ, WRITE, MOD, and ADMIN.
- Place files directly through Windows and prove they appear without import.
- Exercise folder navigation, copyable login-return links, original downloads, safe previews, chunked/resumed upload, conflict handling, create, move, rename, recycle, admin restore, and admin purge.
- Verify representative native FLAC and compatible MKV playback with seeking/range evidence.
- Verify at least one controlled unsupported-media transcode begins progressive playback, finishes, and reuses its cache.
- Exercise FFmpeg unavailable, transcode failure, low-space simulation, stale item, invalid path, and permission revocation.
- Inspect phone and desktop layouts.
- Save a detailed Builder test report with exact commands, ports, URLs, accounts/capabilities, inputs, response status/body/header evidence, file hashes or sizes where useful, playback/transcode evidence, and pass/fail state.

### Production Rollout Validation

1. Install pinned FFmpeg and ffprobe binaries from a verified source and record their versions and checksums.
2. Back up the existing service configuration and record current production health.
3. Create visible and private roots with explicit NTFS ACLs.
4. Install the restricted media-worker service and prove its identity can read originals and modify only its private job, staging, and cache roots.
5. Prove the worker cannot read application secrets or invoke website-service, shutdown, reboot, or deployment controls.
6. Run a prod-profile alternate-port verification using controlled test files and no production-port disruption.
7. Apply the production service configuration and restart through the existing safe deployment workflow.
8. Confirm the public home page, login, an authorized shared-folder listing, an unauthorized denial, original download/range behavior, native media playback, one controlled derivative, Back Office permission changes, audit visibility, Command Center controls/sensors, and ordinary production health.
9. Record deployment and runtime evidence in Builder closure/session artifacts.

## Acceptance Criteria

- `A:\Shared` is the only visible filesystem root and manual Windows changes appear through the portal.
- Anonymous users and accounts without effective READ cannot list, inspect, preview, stream, or download shared content.
- READ users can browse, preview allowed types, stream compatible media, and download originals but cannot mutate content.
- WRITE users receive effective READ and can upload, create directories, rename, move, explicitly replace, and recycle content.
- ADMIN always has READ and WRITE and can manage account capabilities, audit activity, restore recycle items, and permanently purge with confirmation.
- Back Office cannot create a write-only permission state.
- Filesystem escape through paths, links, junctions, reparse points, reserved names, or races is rejected.
- A 10 GB configured upload limit is enforced with resumable disk-streamed uploads and no complete-file JVM buffering.
- No upload or transcode breaches the 100 GB free-space reserve.
- Browser-compatible FLAC, MKV, and other media play directly with range support when their actual codecs permit it.
- Unsupported but decodable media begins progressive compatible playback, completes into cache, and reuses the derivative later.
- Cache use remains bounded to 250 GB by default and eviction cannot remove originals.
- Safe document previews cannot execute active file content.
- Deletes are recoverable for 30 days by default and permanent purge is admin-only.
- Audit records cover the approved event set without secrets, contents, absolute paths, or range-request noise.
- FFmpeg failure cannot break listings, safe previews, original downloads, login, or public pages.
- FFmpeg and ffprobe run only in the restricted worker identity; the privileged website process never parses uploaded media or spawns media tools.
- Existing Command Center service, power, and sensor operations still work under the unchanged website service identity.
- Automated tests, local app testing, Builder test reporting, CI, merge, production verification, closure, and session memory complete successfully.

## Risks and Mitigations

- **Uploaded-media parser risk:** Isolate ffprobe and FFmpeg in a restricted worker, accept only validated job descriptors and fixed profiles, enforce timeouts, and never execute uploads.
- **Filesystem escape or destructive race:** Canonicalize relative paths, reject reparse points, recheck before mutation, and use observed-item concurrency tokens.
- **Disk exhaustion:** Enforce per-file, cache, queue, output, staging-expiration, and free-space limits.
- **Production CPU/GPU contention:** Allow one low-priority job, prefer bounded hardware acceleration, surface queue state, and preserve all non-transcode behavior during failure.
- **Progressive-stream complexity:** Require a tested bounded mechanism, explicit seek limitations while growing, and normal range service after completion.
- **Privilege-boundary regression:** Prove worker ACLs and identity restrictions while regression-testing the unchanged privileged website service and Command Center before changing port 8080.
- **Large implementation scope:** Keep feature packages small, controllers thin, APIs explicit, and tasks test-first and independently reviewable.
- **Direct Windows mutations bypass website audit:** Accept the filesystem as source of truth; audit website operations only and document that out-of-band host edits are not attributable through the portal.

## Rollback

- Restore the prior application build and backed-up Windows service configuration.
- Stop and disable the restricted media-worker service when rolling back the feature.
- Disable shared-folder routes and workers through configuration when a narrower rollback is sufficient.
- Do not delete or modify `A:\Shared` during rollback.
- Preserve recycle contents until their retention policy or an explicit admin purge applies.
- Treat staging and cache as disposable only after their resolved paths are verified beneath the private feature root.

## Open Questions

None. Exact API record names, implementation line ranges, FFmpeg output arguments, progressive-delivery mechanism, and Windows service-account syntax require source and host inspection during implementation planning, but they do not change the approved product behavior or security boundaries.
