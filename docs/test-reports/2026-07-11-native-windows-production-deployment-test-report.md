# Native Windows Production Deployment Test Report

## Document Status

complete

## Story/Issue

Native Windows production migration and boot-persistent automatic deployment for `christopherbell.dev`; PR [#1185](https://github.com/azurras/christopherbell.dev/pull/1185).

## Branch

`codex/boot-persistent-deploy`, implementation commit `8c68fe82`, squash-merged as `c4cb9814f636321d073c135294887a46790fc8e7`.

## App / Environment

- App: `christopherbell.dev` Spring Boot monolith.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\boot-persistent-deploy-20260711`.
- Profiles: `prod,deploy-smoke`.
- Candidate port/base URL: `8081`, `http://127.0.0.1:8081`.
- Database context: existing live WSL MongoDB `christopherbell`, reached through localhost; a stored account email was selected internally without printing it.
- Secrets: loaded from the ignored production `.env`; values were not printed or committed.

## Local Run Details

Built `website/build/libs` with Java 25 and started the executable Boot JAR as a hidden Windows process with `--spring.profiles.active=prod,deploy-smoke --server.port=8081`. Candidate PID was `31092`. Standard output and error were captured under `build/candidate-smoke`. After checks, PID `31092` was stopped and port 8081 was confirmed free. Existing production port 8080 was not stopped or modified.

## Test Cases

1. Request the public home page from the native Windows candidate.
2. Submit the email of a real stored account with a deliberately invalid diagnostic password.
3. Inspect candidate logs for scheduler or WFL monthly catch-up startup signals.
4. Stop the candidate and confirm the alternate port is released.
5. Run automated PowerShell, JavaScript, Java, build, and CI checks supporting the runtime evidence.

## Data Sent

- `GET http://127.0.0.1:8081/`.
- `POST http://127.0.0.1:8081/api/accounts/2024-12-15/login` with `Content-Type: application/json` and body shape `{"email":"<stored account>","password":"deployment-smoke-intentionally-invalid"}`.
- No valid password, token, database write, or scheduled mutation was sent.

## Response Received

- Home page status code: `200`; response body was the public application page.
- Login diagnostic status code: `401`; response body contained `INVALID_TOKEN` and did not contain `RESOURCE_NOT_FOUND`.
- Mutation log scan: zero matches for scheduler/monthly catch-up startup patterns.
- Shutdown: `STOPPED_PID=31092`; `PORT_8081_FREE=True`.

## Pass / Fail

- PASS: candidate served the public application on the non-production port.
- PASS: candidate read the correct database account rather than returning the incident's 404 symptom.
- PASS: mutation-free smoke profile showed no scheduling/catch-up startup evidence.
- PASS: candidate cleanup left port 8081 free and production 8080 untouched.
- PASS: 25 Pester tests, 93 JavaScript tests, complete Java tests, three-OS GitHub builds, and all CodeQL checks passed.

## Evidence

- `Invoke-Pester ops/production/windows/tests -Output Normal`: 25 passed, 0 failed.
- `gradlew.bat --no-daemon :website:build`: `BUILD SUCCESSFUL`; JavaScript 93 passed, 0 failed; Java suite passed.
- PR #1185 checks: Windows, macOS, Ubuntu, CodeQL Actions, CodeQL Java/Kotlin, and CodeQL JavaScript all successful.
- WinSW v2.12.0 x64 was independently downloaded; SHA-256 matched `05B82D46AD331CC16BDC00DE5C6332C1EF818DF8CEEFCD49C726553209B3A0DA`.

## Bugs / Follow-ups

- Post-merge host cutover is not executed because the Codex process is not elevated. Native `MongoDB` remains Stopped/Disabled and `C:\ProgramData\christopherbell.dev\config\deploy.json` does not exist.
- Run installation, configuration, migration rehearsal, cutover, automatic-task installation, rollback rehearsal, and reboot acceptance from Administrator PowerShell using `docs/operations/windows-production.md`.
- Preserve the WSL database and verified archives throughout the recommended seven-day soak.
