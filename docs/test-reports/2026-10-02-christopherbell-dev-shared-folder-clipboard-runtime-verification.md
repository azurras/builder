# Shared Folder Clipboard Runtime Verification

## Document Status

blocked

## Story/Issue

Task 56 in the christopherbell.dev site bug-audit plan. Verify the Shared Folder toolbar's clipboard failure feedback and production page/script availability.

## Branch

Branch `codex/shared-folder-preview-copy-feedback-20261002`; PR #1459 passed all required checks and merged as `da393be28b89228d9cb20bd553118442dd61dcad`.

## App / Environment

Production application `https://www.christopherbell.dev` (Java listener on port 8080; MongoDB on port 27017). The Boot 4.1.1 candidate JAR packaged successfully on Java 25. Candidate attempts used port 18081 and only isolated `test` database copies on port 27019. Startup failed closed at migration `015-require-domain-collection-schema` because each fixture contained an incomplete durable migration record. No production database was configured as a candidate target.

## Local Run Details

Packaged with `:website:bootJar` and process-local `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp`. Two isolated fixture copies were tried; the application exited at migration 015 before listening on port 18081. Candidate MongoDB sessions were stopped. After merge, production routes and content-hashed scripts were fetched read-only. `prod.cmd auto-status` was attempted without elevation and denied access to the protected deploy configuration.

## Test Cases

1. Run the focused Shared Folder event-handler regression suite.
2. Request public readiness, the Shared Folder page, and its versioned script after merge.
3. Confirm the served script contains its manual-copy error message.
4. Confirm candidate ports are closed and production listeners remain present.

## Data Sent

- `GET https://www.christopherbell.dev/actuator/health/readiness`
- `GET https://www.christopherbell.dev/shared?path=reports`
- `GET https://www.christopherbell.dev/a4f67dec0c5bf947a767/js/shared-folder.js?verification=da393be2`
- These were read-only requests. No folder mutation or clipboard action was performed.

## Response Received

- Focused Shared Folder regressions passed 35/35; required PR checks passed.
- Readiness, Shared Folder page, and script returned HTTP 200.
- The script returned 35,897 bytes and contained `Unable to copy the link`.
- Candidate startup failed at migration 015 on isolated fixture copies. Production listener ports 8080 and 27017 remained present; candidate ports were closed.
- `prod.cmd auto-status` was denied access to `C:\ProgramData\christopherbell.dev\config\deploy.json` for the standard user. No elevated access was used; exact deployer status and active SHA were unavailable.

## Pass / Fail

Production page and asset availability passed. The focused regression suite passed. Live browser clipboard failure was not simulated, so browser-level feedback remains unverified. Candidate startup against the available isolated fixtures was blocked by the incomplete durable migration record.

## Evidence

Observed 2026-10-02. Production page and content-hashed asset prove the updated handler is served. Focused regression output and PR check results were inspected. Candidate migration failures and listener cleanup were observed directly.

## Bugs / Follow-ups

The browser-level clipboard failure interaction remains unverified. Regression tests verify rejected and unavailable clipboard behavior and success-only confirmation. Standard-user deployer status remains unavailable because the protected configuration ACL denies access.
