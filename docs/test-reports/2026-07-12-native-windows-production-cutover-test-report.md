# Native Windows Production Cutover Test Report

## Document Status

Complete

## Story/Issue

Complete the `christopherbell.dev` production cutover from the WSL-hosted Spring Boot and MongoDB processes to boot-persistent native Windows services with automatic deployment from `origin/main`.

## Branch

- Production release: `origin/main` at `959621f15b5a13822d9e4bb1e9a0233ac846c9d8`
- Merged repair PRs: `#1189` (`ee4798a31b74eeb892b8cf24672cfbc9a39c1932`) and `#1190` (`959621f15b5a13822d9e4bb1e9a0233ac846c9d8`)

## App / Environment

- App: `christopherbell.dev` Spring Boot website
- Host: native Windows production on the developer workstation
- Profile: `prod`
- Production URL: `http://127.0.0.1:8080/`
- Candidate port: `8081`
- Database: native MongoDB on `mongodb://127.0.0.1:27017`, database `christopherbell`
- Services: `MongoDB` and `ChristopherBellDev`, both configured `Automatic`
- Auto deploy: `ChristopherBellAutoDeploy` startup task running `C:\ProgramData\christopherbell.dev\tools\prod.ps1 auto-deploy`

## Local Run Details

The guarded elevated cutover was executed with:

```powershell
C:\Program Files\PowerShell\7\pwsh.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File A:\Projects\christopherbell.dev-backups\cutover\execute-native-cutover.ps1
```

The script created a fresh WSL `mongodump`, verified its hash and source inventory, built the fetched `origin/main` release, restored to a disposable validation database, compared collection/count/index inventories, exercised a candidate instance, restored the final native database, deployed the native service, installed the startup auto-deploy task, and wrote `A:\Projects\christopherbell.dev-backups\cutover\cutover-result.json`. The native app and MongoDB were left running. The WSL website host was stopped and remains available only as the rollback path.

## Test Cases

1. Create and validate a fresh production archive before cutover.
2. Restore the real archive into a disposable native MongoDB database.
3. Compare source, validation, and final collection/count/index inventories.
4. Start a candidate release against the restored database and exercise home/login endpoints.
5. Start the native production service on port 8080.
6. Verify the known production account is found by sending an intentionally invalid password.
7. Verify native services are running and configured for automatic startup.
8. Verify the automatic deployment startup task is installed and points to the protected production tooling.

## Data Sent

- `GET http://127.0.0.1:8080/`
- `POST http://127.0.0.1:8080/api/accounts/2024-12-15/login`
- Header: `Content-Type: application/json`
- Body: the protected configured smoke-account email with password `deployment-smoke-intentionally-invalid`
- MongoDB archive: `A:\Projects\christopherbell.dev-backups\christopherbell-pre-native-20260712T140506Z.archive.gz`

## Response Received

- Home endpoint status code: `200 OK`
- Login endpoint status code: `401 Unauthorized`
- Login body classification: did not contain `RESOURCE_NOT_FOUND`; `loginAccountFound` recorded as `true`
- Real disposable restore reproduction: `47,968 document(s) restored successfully`, `0 document(s) failed to restore`
- Final release SHA: `959621f15b5a13822d9e4bb1e9a0233ac846c9d8`
- `MongoDB`: `Running`, `Automatic`
- `ChristopherBellDev`: `Running`, `Automatic`
- `ChristopherBellAutoDeploy`: `Ready`, executable `pwsh.exe`, protected `prod.ps1 auto-deploy` arguments

## Pass / Fail

- Fresh backup and inventory: Pass
- Disposable native restore: Pass
- Inventory equality checks: Pass
- Candidate endpoint checks: Pass
- Native production home: Pass
- Known-account login classification: Pass
- Native service state/start type: Pass
- Auto-deploy task installation: Pass
- Overall cutover: Pass

## Evidence

- Cutover result: `A:\Projects\christopherbell.dev-backups\cutover\cutover-result.json`
- Cutover result SHA-256: `F7E3D8BDEBB0CDED639F6BF4A7C7BFAE3EB519ADD346A016CAA0D3F39033ACBB`
- Latest archive: `A:\Projects\christopherbell.dev-backups\christopherbell-pre-native-20260712T140506Z.archive.gz` (`1,876,229` bytes), with `.sha256.json` and `.inventory.json` sidecars
- Local Pester suite after final repair: `33` passed, `0` failed
- PR `#1189`: all seven GitHub checks passed and merged
- PR `#1190`: all seven GitHub checks passed and merged

## Bugs / Follow-ups

Three guarded attempts found issues without data loss. The rollback path restored WSL production each time:

- WSL stop pattern matched its own command line and returned exit code `15`; fixed by PR `#1189` using `[j]ava`.
- Detached `--archive` made Windows `mongorestore` wait on stdin; fixed by PR `#1190` using equals-form URI/archive arguments.
- The outer evidence wrapper used `$home`, which collides case-insensitively with read-only `$HOME`; changed to `$homeResponse`. This wrapper is an operator artifact outside the spoke repository.

A real reboot acceptance test remains intentionally outstanding because rebooting ends the active Codex session. On the next approved maintenance window, reboot Windows and verify both services, port 8080, the known-account login classification, and the auto-deploy startup task without user logon.
