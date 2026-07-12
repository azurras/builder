# 2026-07-12 Native Windows Production Cutover

## 09:10 - Native Windows production cutover completed

### Request

Continue the approved `christopherbell.dev` Windows production cutover after the Codex app crashed. Preserve all production data, keep WSL available as rollback, deploy the latest `origin/main`, run the website and MongoDB automatically at computer startup without user input, poll GitHub for automatic deployments, document the setup, and carry fixes through merged pull requests.

### Project Context

- Spoke repo/worktree used for final repairs: `A:\Projects\christopherbell.dev-worktrees\mongorestore-uri-20260711`
- Production host is the developer workstation, so live traffic was protected until candidate and inventory verification passed.
- Native configuration and secrets are under protected `C:\ProgramData\christopherbell.dev` paths.
- Backups are under `A:\Projects\christopherbell.dev-backups` as compressed MongoDB archives with hash and inventory JSON sidecars.
- WSL Debian remains intact as a rollback source; the final production processes are native Windows services.

### Work Completed

- Installed Microsoft-signed PowerShell `7.6.3` machine-wide at `C:\Program Files\PowerShell\7\pwsh.exe` so SYSTEM services/tasks can execute production tooling.
- Verified MongoDB Shell and Database Tools and used native MongoDB at `127.0.0.1:27017`.
- Created guarded cutover/operator scripts under `A:\Projects\christopherbell.dev-backups\cutover`, including automatic WSL rollback and JSON evidence output.
- Preserved multiple fresh production archives. The final cutover archive is `christopherbell-pre-native-20260712T140506Z.archive.gz` (`1,876,229` bytes) with hash and inventory sidecars.
- Diagnosed WSL stop exit code `15` as a self-matching `pkill` expression. Added regression coverage, merged PR `#1189`, and updated the installed protected configuration.
- Diagnosed the stalled native restore as detached `--archive` argument behavior. A visible disposable restore proved the archive by restoring `47,968` documents with zero failures. Added regression coverage and merged PR `#1190`.
- Fixed the outer operator wrapper's PowerShell `$HOME` naming collision and made failed outer verification remove any installed auto-deploy task before restoring WSL.
- Completed the native migration, final restore, candidate checks, deployment, and startup task installation.
- Final active release is `959621f15b5a13822d9e4bb1e9a0233ac846c9d8` from `origin/main`.

### Decisions

- Kept WSL unchanged as a rollback path throughout the cutover instead of deleting or repurposing its database.
- Required a fresh archive and collection/count/index equality before switching traffic.
- Used native Windows services with `Automatic` startup for MongoDB and the Spring Boot app.
- Used a SYSTEM startup task for the one-minute `origin/main` polling loop. Failed releases use the configured backoff and do not replace the active release.
- Did not reboot during the active session; reboot acceptance is a separate maintenance action because it interrupts Codex and the user's desktop.

### Validation

- `33` Windows production Pester tests passed locally after the final repair.
- PR `#1189` merged at `ee4798a31b74eeb892b8cf24672cfbc9a39c1932`; seven GitHub checks passed.
- PR `#1190` merged at `959621f15b5a13822d9e4bb1e9a0233ac846c9d8`; seven GitHub checks passed.
- Final elevated cutover exited `0`.
- `GET http://127.0.0.1:8080/` returned `200`.
- Known-account invalid-password login returned `401` and not `RESOURCE_NOT_FOUND`.
- `MongoDB` and `ChristopherBellDev` are `Running` with `Automatic` startup.
- `ChristopherBellAutoDeploy` is `Ready` and points to `C:\ProgramData\christopherbell.dev\tools\prod.ps1 auto-deploy` via `pwsh.exe`.
- Evidence file: `A:\Projects\christopherbell.dev-backups\cutover\cutover-result.json`, SHA-256 `F7E3D8BDEBB0CDED639F6BF4A7C7BFAE3EB519ADD346A016CAA0D3F39033ACBB`.

### Current State

- Native Windows website and MongoDB are the active production stack.
- WSL website host processes used during rollback are stopped after successful cutover.
- Native release SHA is the merged `origin/main` commit `959621f15b5a13822d9e4bb1e9a0233ac846c9d8`.
- Spoke repair branch `codex/fix-mongorestore-archive-args` may remain locally even though its remote branch was deleted after merge.
- The main checkout was intentionally not reset because it contained pre-existing divergent/dirty state; deployment fetched `origin/main` and built detached releases.

### Follow-ups

- During an approved maintenance window, reboot Windows and verify services/task/port/login before declaring reboot acceptance complete.
- After a suitable soak period and a successful reboot test, decide whether to retire the WSL fallback and remove disposable native validation databases such as `christopherbell_restore_debug` and `christopherbell_restore_check`.
- Use the documented production commands for future upgrades; normal updates should arrive through the one-minute `origin/main` poller.
