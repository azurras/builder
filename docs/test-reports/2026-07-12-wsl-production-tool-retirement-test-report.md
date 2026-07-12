# WSL Production Tool Retirement Test Report

## Document Status

Complete

## Story/Issue

Retire the `christopherbell.dev` website production stack from WSL while preserving the Debian distro, make native Windows the only production runtime, and provide documented setup, startup, backup, and automatic `origin/main` deployment workflows.

## Branch

- Cutover PR: `azurras/christopherbell.dev#1191`, squash commit `fffc7b4522167ffa9857ce24559ae273521e3fc6`
- SYSTEM Git follow-up PR: `azurras/christopherbell.dev#1192`, squash commit `3c1403def215b60943e061b13232e03055c7c106`
- Safe task-refresh follow-up PR: `azurras/christopherbell.dev#1193`, squash commit `2a21335dd929f8f670b17f5adc8db8637ca05613`

## App / Environment

- App: `christopherbell.dev` Spring Boot website
- Host: native Windows production machine
- Production profile/port: existing production service on `127.0.0.1:8080`
- Public URL: `https://www.christopherbell.dev/`
- Database: native Windows MongoDB on `127.0.0.1:27017`, database `christopherbell`
- Services: `MongoDB`, `ChristopherBellDev`, and `cloudflared`
- Startup task: `ChristopherBellAutoDeploy`, SYSTEM, highest privileges, enabled AtStartup trigger, one-minute polling
- WSL distro: Debian retained; website production executables and units removed

## Local Run Details

The application was already running as the native Windows `ChristopherBellDev` service and was left running. The production deployment task built candidates from fetched `origin/main`, exercised the deploy-smoke profile, and switched the service release only after candidate validation. Production logs remain under `C:\ProgramData\christopherbell.dev\logs`; deployment state is stored at `C:\ProgramData\christopherbell.dev\state\auto-deploy.json`.

Operational commands exercised from the Windows worktrees included:

```powershell
.\prod.cmd install
.\prod.cmd auto-install
.\prod.cmd deploy -WhatIf
.\prod.cmd backup
.\prod.cmd verify-startup
```

The final live release and successful auto-deploy state both resolved to `2a21335dd929f8f670b17f5adc8db8637ca05613`.

## Test Cases

1. Verify all required Windows services are running and configured for automatic startup.
2. Verify the full SYSTEM scheduled-task contract, including absolute PowerShell 7 action, enabled boot trigger, restart settings, unlimited runtime, and one-minute polling.
3. Send anonymous GET requests to the native and public website roots.
4. Run a real native MongoDB archive backup and `mongorestore --dryRun` validation.
5. Verify protected deployment configuration contains native fields and no retired WSL keys.
6. Verify the SYSTEM account can resolve `origin/main` using scoped per-command repository trust.
7. Verify a merged GitHub push automatically deploys the fetched remote SHA.
8. Verify WSL no longer contains cloudflared, nginx, MongoDB executables, or their systemd units.
9. Verify the task refresh refuses to interrupt an active deployment and succeeds once the deployment lock is free.

## Data Sent

- `GET http://127.0.0.1:8080/` with no authentication or request body.
- `GET https://www.christopherbell.dev/` with no authentication or request body.
- Git remote query as `NT AUTHORITY\SYSTEM`: `git.exe -c safe.directory=A:/Projects/christopherbell.dev -C A:\Projects\christopherbell.dev ls-remote origin refs/heads/main`.
- MongoDB backup arguments used the attached IPv4 forms `--uri=mongodb://127.0.0.1:27017`, `--db=christopherbell`, `--archive=<archive path>`, and `--gzip`; validation used the same archive plus `--dryRun`.
- No tunnel token, application secret, service command line, or protected environment value was printed or recorded.

## Response Received

- Native website root: HTTP `200`.
- Public website root: HTTP `200`.
- Native HTTP response body: 3,912 UTF-8 bytes, contained an HTML document and `<title>CB | Home</title>`.
- Public HTTP response body: 3,912 UTF-8 bytes, contained an HTML document and `<title>CB | Home</title>`.
- `verify-startup`: exit `0`; services `RunningAutomatic`, auto-deploy task running/ready, native endpoint `200`, public endpoint `200`.
- Windows services: `MongoDB`, `ChristopherBellDev`, and `cloudflared` all `Running` / `Automatic`.
- SYSTEM Git probe: returned `2a21335dd929f8f670b17f5adc8db8637ca05613 refs/heads/main` with exit `0` after the final merge.
- Auto-deploy state: `successfulSha=2a21335dd929f8f670b17f5adc8db8637ca05613`, no failed SHA, no error.
- Backup: `A:\Projects\christopherbell.dev-backups\christopherbell-native-20260712T152801Z.archive.gz`, 1,875,552 bytes, SHA-256 `753A4C80CCA650B0DFD9623C8295C13DA06C651B7EE4FD991497B67D6EA9890B`.
- WSL commands absent: `cloudflared`, `nginx`, `mongod`, `mongosh`, `mongodump`, `mongorestore`.
- WSL units absent: `cloudflared.service`, `nginx.service`, `mongod.service`.

## Pass / Fail

All runtime test cases passed. Automatic deployment initially exposed two production-only defects: SYSTEM Git repository ownership rejection and stale `IgnoreNew` task processes during script refresh. Both defects were reproduced, fixed with regression coverage, independently reviewed, merged through green CI, installed, and retested successfully.

Supporting automated checks:

- Pester production suite: 48 passed, 0 failed at final implementation state.
- Spring `:website:test`: `BUILD SUCCESSFUL`.
- GitHub CI and CodeQL: green on PRs #1191, #1192, and #1193 across Windows, macOS, and Ubuntu.
- Independent reviews: no remaining Critical or Important findings.

## Evidence

- PRs: `https://github.com/azurras/christopherbell.dev/pull/1191`, `https://github.com/azurras/christopherbell.dev/pull/1192`, `https://github.com/azurras/christopherbell.dev/pull/1193`
- Final production SHA: `2a21335dd929f8f670b17f5adc8db8637ca05613`
- Final backup path and SHA-256 are recorded above.
- Protected startup verifier exited `0` after the final task refresh.
- Public and native HTTP checks both returned `200` after the final automatic deployment.

## Bugs / Follow-ups

- No open production defect remains from this cutover.
- A real cold reboot was not performed during the Codex session. The full registered startup contract was validated, but a future maintenance window should include one physical reboot acceptance check.
- The primary checkout at `A:\Projects\christopherbell.dev` was intentionally preserved with its existing local divergence (`main` ahead 3 and behind remote) rather than reset or cleaned.
