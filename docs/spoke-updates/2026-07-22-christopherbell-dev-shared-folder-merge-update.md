# ChristopherBell.dev Shared Folder Merge Update

- Related work: [Shared Folder Portal](../work/2026-07-17-christopherbell-dev-shared-folder-portal.md)
- Test report: [Alternate-Port Acceptance](../test-reports/2026-07-22-christopherbell-dev-shared-folder-alternate-port-acceptance.md)
- Source repo: `azurras/christopherbell.dev`
- Reporting agent: Codex `/root`
- Status: merged

## Changes Made

Completed the post-portal Windows media worker, fixed-profile FFmpeg/ffprobe boundary, maintenance and capacity authority, pinned verification tooling, and opt-in installed-worker security acceptance. Alternate-port runtime testing exposed and resolved Spring constructor/proxy wiring, Mongo upload-lease version alignment, and full/partial download header and byte-boundary defects.

## Files Touched

The spoke changes cover the shared-folder Java services/controllers/tests, browser portal and worker code, Windows production service/install/operations scripts, pinned media-tool manifest, Gradle verification tasks, and operator documentation.

## Commits and Pull Request

- Runtime commits: `fbe3769cfd894a75f45fed1b124ecbaf7450ccde`, `f91d404c8056bd6b8b316b41909ee0528964331a`
- Pull request: [azurras/christopherbell.dev#1219](https://github.com/azurras/christopherbell.dev/pull/1219)
- Squash merge: `6ad5a0a316d2674f96fca7b986a1d15d7abdc856`

## Validation

- Isolated port-8090 runtime acceptance: 41/41 passed.
- Java: 1,053 tests, 0 failures/errors, 3 expected platform skips.
- JavaScript: 165/165 passed.
- Worker Pester: 56/56; operations Pester: 28/28 under PowerShell 7 and Windows PowerShell 5.1.
- Independent final review: 0 Critical, 0 Important, 0 Minor.
- GitHub: Windows, macOS, Linux, all CodeQL language analyses, and aggregate CodeQL passed.

## Blockers and Risks

No code or merge blocker remains. The installed worker, production roots, ACLs, and installed-worker security group require an elevated controlled production step. The strict maintenance authority is intentionally single-host.

## Next Actions

Install/deploy from the merged revision, run installed-worker acceptance and production smoke/portal checks, then close Builder work and save session memory.
