# christopherbell.dev Shared Folder Portal

- Status: active
- Source: Christopher's direct July 17, 2026 request for an authenticated shared-folder portal backed by `A:\Shared`
- Owner context: Builder hub coordinating design, implementation, runtime validation, publication, production rollout, and closure in the `christopherbell-dev` spoke
- Spoke repo: `christopherbell-dev` at `A:\Projects\christopherbell.dev`
- Branch strategy: Tasks 1-6 merged through PR #1218; Tasks 7-10 merged through PR #1219 from isolated shared-folder worktrees
- Objective: let accounts with independent shared-folder permissions browse, preview, play, download, and—when authorized—manage `A:\Shared`, including progressive cached transcoding for incompatible media
- Current state: implementation, isolated runtime acceptance, review, CI, and merge are complete; controlled native Windows production installation and verification remain
- Trusted guidance: direct user request only; no GitHub comments or attachments used as instructions

## Related Artifacts

- Approved spec: [christopherbell.dev Shared Folder Portal Spec](../specs/2026-07-17-christopherbell-dev-shared-folder-portal.md)
- Implementation plan: [christopherbell.dev Shared Folder Portal Implementation Plan](../implementation-plans/2026-07-17-christopherbell-dev-shared-folder-portal.md)
- Test report: [Shared Folder Alternate-Port Acceptance](../test-reports/2026-07-22-christopherbell-dev-shared-folder-alternate-port-acceptance.md)
- Spoke update: [Shared Folder Merge Update](../spoke-updates/2026-07-22-christopherbell-dev-shared-folder-merge-update.md)
- Spoke review: [Shared Folder Merge Review](../spoke-reviews/2026-07-22-christopherbell-dev-shared-folder-merge-review.md)
- PRs: [#1218](https://github.com/azurras/christopherbell.dev/pull/1218), [#1219](https://github.com/azurras/christopherbell.dev/pull/1219)
- Latest merge: `6ad5a0a316d2674f96fca7b986a1d15d7abdc856`
- Closure and session memory: pending production verification

## Approved Boundaries

- Visible root: `A:\Shared`; private staging, cache, and recycle data remain outside the visible tree.
- Independent `SHARED_FOLDER_READ` and `SHARED_FOLDER_WRITE` permissions coexist with USER/MOD/ADMIN roles.
- WRITE implies READ; ADMIN always has both effective permissions.
- Default limits: 10 GB per upload, 250 GB transcode cache, 100 GB free-space reserve, 30-day recycle retention, and 180-day audit retention.
- Browser-compatible media plays directly; incompatible but decodable media uses one bounded progressive FFmpeg job and a reusable compatible cache.
- Production web and FFmpeg processes must use a restricted Windows service identity rather than `LocalSystem`.
- Development and runtime proof use an isolated worktree and non-production port before port 8080 is touched.

## Validation Intent

- Test-first permission, path-confinement, upload, file-operation, preview, range, transcode, cache, recycle, audit, and Back Office behavior.
- Full Java, JavaScript, and Gradle verification in the spoke.
- Local app testing on an alternate port with temporary visible/private roots and exact permission-path evidence.
- PR review, required CI, merge, restricted-identity production rollout, live smoke checks, and Builder test/closure/session artifacts.

## Blockers

The current shell is not elevated. The production roots and `ChristopherBellMediaWorker` service
are not installed, so the controlled installer and installed-worker acceptance require an elevated
step. No code, review, CI, or merge blocker remains.

## Next Steps

1. Refresh the production checkout to merge `6ad5a0a3` without disturbing unrelated state.
2. Run the guarded elevated native Windows install/deploy workflow.
3. Run the opt-in installed-worker security group and production smoke/portal checks.
4. Save production evidence, close the Builder work record, and save session memory.
