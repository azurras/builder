# 2026-07-12 WSL Production Tool Retirement

## 11:06 - Complete native Windows production cutover

### Request

Keep WSL installed but remove every tool used to operate `christopherbell.dev` from it, including cloudflared, nginx, MongoDB, and old website launch artifacts. Make native Windows start production at computer boot, deploy the latest `origin/main` automatically after pushes/merges, keep updates easy through `prod.cmd`/Make targets, and document setup/startup/backup/recovery. Continue through pull-request merge.

### Project Context

- Spoke repository: `A:\Projects\christopherbell.dev` (`azurras/christopherbell.dev`).
- The development machine is also the production host.
- Native production services are `MongoDB`, `ChristopherBellDev`, and `cloudflared`.
- Protected production configuration is under `C:\ProgramData\christopherbell.dev`.
- Backups are stored under `A:\Projects\christopherbell.dev-backups`.
- The canonical public route is `https://www.christopherbell.dev/`; the apex route is not the production smoke target.
- Existing local divergence in the primary checkout belongs to the user and was preserved.

### Work Completed

- Purged WSL cloudflared, nginx, MongoDB server/shell/tools packages, repositories, keys, data/log directories, units, and website production artifacts while preserving Debian and unrelated services.
- Rotated the previously exposed Cloudflare tunnel token and installed signed native cloudflared 2026.7.1 at `C:\Program Files (x86)\cloudflared\cloudflared.exe`.
- Made Windows services automatic and restart-resilient; installed `ChristopherBellAutoDeploy` as a SYSTEM/highest/AtStartup scheduled task.
- Removed the retired WSL migration command/module/tests and all WSL deployment configuration fields.
- Added native-only setup/config merging, exact retired-key cleanup, signed cloudflared executable and service-binding validation, native MongoDB archive/restore-dry-run backup, complete startup contract verification, Make targets, README guidance, and the Windows production runbook.
- Made `prod.cmd` locate the standard PowerShell 7 installation when PATH is stale.
- Stabilized PowerShell module loading so all CLI handlers remain exported.
- Made WinSW setup idempotent instead of replacing a running locked executable.
- Fixed SYSTEM Git `dubious ownership` failures with an exact per-command `safe.directory` override on every production Git operation; no global/wildcard trust was written.
- Made task refreshes deployment-lock-aware: active deployment prevents tool overwrite/task stop; idle refresh stops the old process, waits, registers, releases the lock, then starts the refreshed loop.
- Merged three green PRs:
  - #1191 `Retire WSL production tooling` -> `fffc7b4522167ffa9857ce24559ae273521e3fc6`
  - #1192 `Allow SYSTEM production Git operations` -> `3c1403def215b60943e061b13232e03055c7c106`
  - #1193 `Safely refresh the auto-deploy task` -> `2a21335dd929f8f670b17f5adc8db8637ca05613`
- Deleted all three remote feature branches after merge.

### Decisions

- Windows is the sole production runtime; WSL remains available for unrelated development use.
- Automatic deployment polls every 60 seconds, resolves the fetched remote SHA, builds/tests a candidate, switches atomically, and records success/failure state.
- Cloudflare credentials remain outside Git; token rotation is an explicit protected-file installer input.
- Git repository trust is scoped to each production command and the exact configured repository path.
- Task script updates coordinate through the same deployment lock as release switching to prevent mid-deploy interruption.
- The primary checkout was not reset despite divergence; deployments resolve `origin/main` independently.

### Validation

- Final Pester suite: 48 passed, 0 failed.
- Spring `:website:test`: `BUILD SUCCESSFUL`.
- PR CI/CodeQL: all checks green on Windows, macOS, and Ubuntu for #1191, #1192, and #1193.
- Independent code review after each correction: no remaining Critical or Important findings.
- Native and public root endpoints: HTTP 200.
- Final protected `verify-startup`: exit 0.
- Final services: MongoDB, ChristopherBellDev, cloudflared all Running/Automatic.
- Final release and auto-deploy success state: `2a21335dd929f8f670b17f5adc8db8637ca05613`.
- SYSTEM Git probe resolved final `origin/main` with exit 0.
- WSL production executables and units verified absent.
- Real backup/restore dry-run completed; archive SHA-256 `753A4C80CCA650B0DFD9623C8295C13DA06C651B7EE4FD991497B67D6EA9890B`.
- Detailed evidence: `docs/test-reports/2026-07-12-wsl-production-tool-retirement-test-report.md`.

### Current State

- Production is healthy on final merged SHA `2a21335dd929f8f670b17f5adc8db8637ca05613`.
- Auto-deploy task is installed with final merged scripts and is running.
- The three temporary feature worktrees remain registered for provenance; remote branches are deleted.
- Primary checkout `A:\Projects\christopherbell.dev` remains `main` with pre-existing local divergence and was not modified/reset during cleanup.

### Follow-ups

- Perform one physical Windows reboot during a convenient maintenance window and run `prod.cmd verify-startup` afterward for cold-boot acceptance.
- Do not reintroduce WSL website services or tooling; use the Windows runbook and `prod.cmd`/Make targets.
- Reconcile the primary checkout's local main divergence separately only with explicit user authorization.
