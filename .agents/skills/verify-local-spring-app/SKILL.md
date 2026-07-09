---
name: verify-local-spring-app
description: Run, verify, and production-restart a local Spring Boot web app safely on a desktop that may already be serving production traffic. Use when Codex needs to test a Spring Boot site on an alternate port, avoid disrupting an existing production port until validation is complete, identify and stop the process bound to a port, and restart the app with the newly merged code.
---

# Verify Local Spring App

## Overview

Use this workflow for local desktop deployments where the same machine is both the development host and the production host. Keep production traffic running while validation happens on a separate port, then restart the production port only after tests and manual checks pass.

## Workflow

1. Confirm the repository instructions and app defaults before starting:
   - Read `AGENTS.md` and the root `README.md`.
   - Confirm the normal production port and the normal local/test port.
   - Inspect `git status --short --branch`; do not overwrite dirty user work.

2. Run automated verification first:
   - Run the smallest focused tests for the changed behavior.
   - Run the broader build/test command required by the repo before any completion claim.
   - For browser assets, run the repo's JavaScript syntax or browser checks.

3. Start the app on a non-production port:
   - Choose a free alternate port, usually the repo's documented local port.
   - Start the app with explicit profile and port settings instead of relying on inherited environment.
   - Keep the process handle or terminal session id so it can be stopped after checks.

4. Verify the alternate-port app:
   - Poll the base URL until it returns an HTTP response or the startup log shows a fatal error.
   - Exercise the changed endpoints or pages directly with `curl`, `Invoke-WebRequest`, browser automation, or targeted smoke scripts.
   - Capture exact commands, ports, status codes, and any important response snippets.

5. Stop the alternate-port process.

6. Restart production only after validation:
   - Identify the current production process by port before stopping it.
   - Record the command or jar currently used when possible.
   - Stop only the process bound to the intended production port.
   - Start the new code with the production profile and explicit production port.
   - Poll the production URL until it responds.

## Windows Port Commands

Use PowerShell-native commands on Windows:

```powershell
Get-NetTCPConnection -LocalPort 8080 -State Listen |
  Select-Object LocalAddress,LocalPort,OwningProcess

Get-Process -Id <pid> |
  Select-Object Id,ProcessName,Path,StartTime

Stop-Process -Id <pid>
```

Start background helpers hidden unless the user asked for a visible window:

```powershell
Start-Process -WindowStyle Hidden -FilePath ".\gradlew.bat" -ArgumentList ":website:bootRun"
```

Prefer an interactive terminal session when live logs matter, but do not leave temporary verification processes running.

## Safety Rules

- Do not kill the production port before alternate-port validation passes.
- Do not use destructive git commands to update a dirty production checkout.
- If the production checkout has dirty user work, deploy from a clean merged worktree or ask before touching those files.
- Use explicit environment variables for profile and port.
- Report any restart failure immediately with the last relevant log lines and leave the prior process state clear.

## Evidence To Record

- Test/build command names and exit codes.
- Alternate port used and URLs checked.
- Production PID stopped and command used to restart.
- Production URL response after restart.
