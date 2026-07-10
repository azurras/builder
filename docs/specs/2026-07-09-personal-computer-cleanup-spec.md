# Personal Computer Cleanup Spec

## Document Status

ready-for-review

## Purpose

Create a safe, repeatable cleanup workflow for Christopher's personal Windows development computer. The cleanup should recover disk space, reduce desktop and download clutter, remove stale development artifacts, and improve day-to-day findability without deleting useful work, credentials, project history, or application state.

## Background

The current request is broad: clean up the computer, not a single repository or app. Because the machine is also used for development work, the cleanup must treat source code, package caches, local databases, credentials, shell profiles, browser data, and running services as high-risk areas. The first pass should prioritize inventory, backup, and reviewable cleanup candidates before any destructive action.

## Goals

- Produce a clear inventory of large files, duplicate-looking files, stale downloads, old installers, caches, temporary files, and inactive project folders.
- Separate cleanup candidates into safe-to-remove, review-required, archive, and keep categories.
- Free disk space through low-risk cleanup first: system temp files, recycle bin review, old installers, generated build outputs, stale package caches, and obvious duplicates.
- Organize high-traffic user folders such as Desktop, Downloads, Documents, Pictures, Videos, and project workspaces.
- Preserve source repositories, uncommitted changes, environment files, credentials, license files, personal records, media originals, browser profiles, and app data unless explicitly approved for deletion.
- Leave a durable cleanup report with before-and-after disk usage, files moved or removed, and unresolved review items.

## Non-Goals

- No operating system reinstall, factory reset, disk repartitioning, registry cleaning, or driver cleanup.
- No automated deletion of personal documents, photos, videos, repositories, password stores, browser profiles, cloud-sync folders, local databases, SSH keys, API keys, or dotfiles.
- No attempt to optimize every application setting.
- No permanent deletion before review when the file is user-created, unique, or hard to replace.

## Cleanup Principles

- Inventory before deletion: every destructive action should be preceded by a concrete candidate list.
- Prefer quarantine over deletion for ambiguous files. Move review-required files to a dated holding folder when organization is needed but deletion is not yet approved.
- Keep original paths in the cleanup report so moved files can be traced.
- Treat generated artifacts differently from source. Build outputs and caches can usually be regenerated; repositories and local config often cannot.
- Avoid running scripts from unknown downloads or archives during cleanup.
- Do not extract suspicious archives just to inspect them.

## Scope

### Included Locations

- `C:\Users\Christopher\Desktop`
- `C:\Users\Christopher\Downloads`
- `C:\Users\Christopher\Documents`
- `C:\Users\Christopher\Pictures`
- `C:\Users\Christopher\Videos`
- `C:\Users\Christopher\Developer`
- User-level temp directories
- Recycle Bin contents
- Package-manager caches that can be safely regenerated
- Old local build outputs inside development workspaces

### High-Risk Locations

These locations require explicit review before any deletion or major move:

- `.ssh`, `.gnupg`, `.aws`, `.azure`, `.config`, `.kube`, `.npmrc`, `.pypirc`, `.m2/settings.xml`, shell profiles, and other credential-bearing config.
- Git repositories with uncommitted changes, unpushed branches, tags, releases, or local-only worktrees.
- Local databases, Docker volumes, VM images, WSL distributions, emulator images, and application data folders.
- Cloud-sync folders where deletion may propagate to other devices.
- Browser profiles, password managers, authenticator exports, license keys, tax, legal, medical, financial, and identity documents.

## Requirements

### Inventory

- Capture free and used space for each fixed drive before cleanup.
- Generate a largest-files report for user folders and development workspaces.
- Generate a largest-directories report for high-growth areas such as Downloads, Desktop, Developer, AppData caches, Docker/WSL storage, and package caches.
- Identify files older than 180 days in Downloads and Desktop.
- Identify common installer and archive formats in Downloads: `.exe`, `.msi`, `.zip`, `.7z`, `.rar`, `.iso`, `.dmg`, `.pkg`, `.tar`, `.gz`.
- Identify generated development artifacts such as `node_modules`, `dist`, `build`, `target`, `.gradle`, `.next`, `.turbo`, `.venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, and coverage output.
- Check Git repository status before proposing repository cleanup.

### Backup and Recovery

- Confirm at least one current backup or restore path before destructive cleanup.
- Create a dated cleanup workspace such as `C:\Users\Christopher\Cleanup-Review\YYYY-MM-DD` for reports and quarantine lists.
- For review-required organization, move files to quarantine instead of deleting them.
- Use Recycle Bin for user-file deletion where possible instead of permanent removal.
- Record all deletion and move actions in a cleanup report.

### Cleanup Execution

- Phase cleanup from lowest risk to highest risk.
- Start with OS-supported cleanup tools and clearly regenerated temp/cache data.
- Remove old installers and duplicate downloads only after review.
- Remove development build artifacts only when their owning repository has no uncommitted work that depends on them and the artifact is known to be reproducible.
- For each package ecosystem, prefer official cache-clean commands over manual deletion when available.
- Stop before cleaning Docker, WSL, VM, database, or browser data unless explicitly approved.

### Organization

- Desktop should contain only active shortcuts, current working files, or folders intentionally pinned for current work.
- Downloads should be split into keep, archive, installers, imports, and delete-review groups, or moved into a dated review folder if decisions are pending.
- Development folders should keep active repositories discoverable and mark inactive or archived projects without deleting them.
- Large media should be grouped by source or project when obvious; otherwise leave in place and report candidates.

## Proposed Approach

### Phase 1: Baseline and Safety Check

1. Record disk usage and available space for each fixed drive.
2. Confirm backup coverage or identify that cleanup must remain non-destructive.
3. Create the dated cleanup workspace for reports.
4. Record running development services, Docker state, WSL state, and open sync clients if relevant.

### Phase 2: Inventory Reports

1. Generate large-file and large-directory reports for user folders and development workspaces.
2. Generate age-based reports for Downloads and Desktop.
3. Generate development artifact reports by known directory name.
4. Generate Git status summaries for repositories under `C:\Users\Christopher\Developer`.
5. Review the reports and classify candidates as safe-to-remove, review-required, archive, or keep.

### Phase 3: Low-Risk Cleanup

1. Empty reviewed Recycle Bin contents.
2. Remove temp files using Windows-supported mechanisms and user-level temp cleanup.
3. Remove obvious generated caches that are not credential-bearing and can be regenerated.
4. Remove obsolete installers and duplicate downloads only after the candidate list is approved.

### Phase 4: Development Workspace Cleanup

1. For each repository, skip cleanup when Git status is dirty unless the repo owner approves the exact action.
2. Remove reproducible build outputs from clean repositories when the project tooling clearly owns those outputs.
3. Use package-manager commands for cache cleanup where appropriate.
4. Archive inactive project folders only after confirming they have no unpushed or uncommitted work.

### Phase 5: Organization and Report

1. Move review-required files into the dated cleanup workspace or a clearly named archive folder.
2. Normalize Desktop and Downloads organization.
3. Record before-and-after disk usage.
4. Save final reports: actions taken, items skipped, review queue, and recommended next cleanup pass.

## Suggested Report Artifacts

- `cleanup-baseline.md`: drive usage, backup status, and safety notes.
- `large-files.csv`: large user-visible files with path, size, modified time, and classification.
- `large-directories.csv`: largest directories with path, size, and cleanup recommendation.
- `dev-repo-status.csv`: repository path, branch, dirty state, unpushed branch note, and cleanup eligibility.
- `cleanup-actions.md`: files moved, files deleted, commands run, and skipped high-risk items.
- `review-queue.md`: items needing Christopher's explicit decision.

## Validation Plan

- Compare before-and-after free disk space for each cleaned drive.
- Spot-check that Desktop, Downloads, and Developer folders still contain expected active work.
- Confirm key development tools still launch: shell, Git, package managers, IDE/editor, Docker/WSL only if they were touched.
- Confirm no Git repositories were left in a new dirty state due to cleanup.
- Confirm quarantined files can be restored from the cleanup workspace.
- Confirm cleanup report lists every destructive or organizational action.

## Acceptance Criteria

- A baseline report exists before cleanup actions begin.
- No high-risk location is deleted or moved without explicit approval.
- All cleanup actions are recorded with paths and timestamps.
- Obvious clutter is reduced in Desktop and Downloads.
- Disk space improvement is measured and reported.
- Any remaining uncertain files are listed in a review queue instead of silently deleted.

## Open Questions

- Which drive or symptom matters most: low disk space, clutter, performance, startup noise, or development workspace sprawl?
- Should the cleanup optimize for maximum recovered disk space or minimum risk?
- Are cloud-sync folders in scope?
- Are Docker, WSL, VM images, local databases, and browser profiles explicitly out of scope for the first pass?
- Where should long-term archives live if files are moved out of Desktop or Downloads?
