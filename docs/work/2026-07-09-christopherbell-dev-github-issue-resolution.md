# christopherbell.dev GitHub Issue Resolution

## Objective
Implement every open GitHub issue in `azurras/christopherbell.dev` as of 2026-07-09, with one implementation plan and one pull request per issue, then merge verified work, restart the production desktop app on port 8080, and close the issues.

## Status
active

## Owner / Agent Context
Codex is coordinating from the Builder hub on Windows at `C:\Users\Christopher\Developer\builder`. The spoke repo is `C:\Users\Christopher\Developer\christopherbell.dev` with remote `https://github.com/azurras/christopherbell.dev.git` and default branch `main`.

## Related Spoke Repos
- `christopherbell.dev`: Spring Boot personal website and application.

## Issue Scope
- #1090 Bug: production JWT can fall back to the local development signing secret.
- #1091 Bug: rate limiting can be bypassed by spoofing X-Forwarded-For.
- #1092 Bug: request size limit does not protect chunked or missing Content-Length bodies.
- #1093 Bug: password reset links are written to logs when email delivery is unavailable or fails.
- #1094 Bug: generic controller exception fallback is not registered.
- #1095 Enhancement: make global rate limits configurable and endpoint-aware.
- #1096 Enhancement: add Bean Validation to request DTOs and controller inputs.

## Constraints
- The desktop machine is also the production host; do not disturb the process on port 8080 until all merged work is verified on another port.
- The local website `main` checkout has uncommitted Canes Box Tracker changes; preserve those changes and implement issue work from clean `origin/main` worktrees/branches.
- Each issue must be merged via a pull request.
- After successful verification and merge, restart the production process on port 8080 with the new code.

## Related Plans
Implementation plans will be saved under `docs/implementation-plans/` with one dated Markdown file per issue.

## Current State
Planning artifacts and a repo-scoped local verification skill are being created before spoke implementation begins.

## Validation Plan
- Run targeted Gradle tests for each issue branch before PR creation.
- Run `./gradlew :website:test` or `./gradlew :website:build` on the fully merged code.
- Start the app on a non-production port and smoke-test representative endpoints/pages.
- Stop the old port 8080 process only after alternate-port verification passes, then restart and smoke-test port 8080.
