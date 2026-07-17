# christopherbell.dev Shared Folder Portal

- Status: active
- Source: Christopher's direct July 17, 2026 request for an authenticated shared-folder portal backed by `A:\Shared`
- Owner context: Builder hub coordinating design, implementation, runtime validation, publication, production rollout, and closure in the `christopherbell-dev` spoke
- Spoke repo: `christopherbell-dev` at `A:\Projects\christopherbell.dev`
- Branch strategy: isolated `codex/shared-folder-portal` worktree from refreshed `origin/main`; preserve the clean but divergent primary checkout
- Objective: let accounts with independent shared-folder permissions browse, preview, play, download, and—when authorized—manage `A:\Shared`, including progressive cached transcoding for incompatible media
- Current state: interactive design and written spec approved; implementation planning is in progress; no spoke code has changed
- Trusted guidance: direct user request only; no GitHub comments or attachments used as instructions

## Related Artifacts

- Approved spec: [christopherbell.dev Shared Folder Portal Spec](../specs/2026-07-17-christopherbell-dev-shared-folder-portal.md)
- Implementation plan: pending the current planning phase
- Test report, spoke update/review, closure, and session memory: pending later delivery phases

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

None. Exact implementation files, line ranges, progressive-delivery mechanism, pinned FFmpeg distribution, and Windows service-account syntax must be resolved and quality-gated in the implementation plan before development begins.

## Next Steps

1. Inspect refreshed `origin/main` and save an execution-ready implementation plan with literal Code Edit blocks.
2. Validate and review the plan, then commit and push the Builder checkpoint.
3. Execute in an isolated spoke worktree using test-driven development.
4. Complete local runtime, CI, merge, production rollout, closure, and session memory.
