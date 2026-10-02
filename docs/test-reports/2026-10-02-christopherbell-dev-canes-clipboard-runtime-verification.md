# Cane's Tracker Clipboard Runtime Verification

## Document Status

blocked

## Story/Issue

Task 57 in the christopherbell.dev site bug-audit plan. Verify the Cane's tracker clipboard-unavailable feedback and production page/script availability.

## Branch

Branch `codex/canes-curl-clipboard-availability-20261002`; PR #1460 passed all required checks and merged as `b195b95791de2370587640c25f66aa776cc43d86`.

## App / Environment

Production application `https://www.christopherbell.dev` (Java listener on port 8080; MongoDB on port 27017). A Task 57-specific candidate application was not started. During adjacent Task 56 candidate work, two isolated `test` fixture copies on candidate port 27019 failed the required migration 015 precondition, so no further candidate runtime was attempted against those fixtures. No production database was configured as a candidate target.

## Local Run Details

The production verification used read-only HTTPS requests after merge. Candidate runtime was not started for this task because the adjacent Task 56 candidate setup failed closed on both isolated fixtures. `prod.cmd auto-status` was attempted without elevation and denied access to the protected deploy configuration.

## Test Cases

1. Run the focused Cane's tracker event-handler regression suite.
2. Request public readiness, the Cane's tracker page, and its versioned script after merge.
3. Confirm the served script contains the clipboard failure alert.
4. Confirm only production listeners remain on their expected ports.

## Data Sent

- `GET https://www.christopherbell.dev/actuator/health/readiness`
- `GET https://www.christopherbell.dev/canes-box-tracker`
- `GET https://www.christopherbell.dev/a4f67dec0c5bf947a767/js/canes-box-tracker.js?verification=da393be2`
- These were read-only requests. No API curl was copied or sent to Raising Cane's.

## Response Received

- Focused Cane's tracker regressions passed 18/18; required PR checks passed.
- Readiness, the Cane's tracker page, and its script returned HTTP 200.
- The script returned 18,685 bytes and contained `Could not copy the official API curl request.`.
- Production listeners 8080 and 27017 remained present; candidate ports were closed.
- `prod.cmd auto-status` was denied access to `C:\ProgramData\christopherbell.dev\config\deploy.json` for the standard user. No elevated access was used; exact deployer status and active SHA were unavailable.

## Pass / Fail

Production page and asset availability passed. The focused regression suite passed. Live browser clipboard failure was not simulated, so browser-level feedback remains unverified. Candidate application startup was not attempted after the adjacent Task 56 isolated-fixture failures.

## Evidence

Observed 2026-10-02. The production page and content-hashed asset prove the updated handler is served. Focused regression output and PR checks were inspected. The final port check found only the production listeners on 8080 and 27017.

## Bugs / Follow-ups

The browser-level clipboard-unavailable interaction remains unverified. Focused regressions verify unavailable and rejected clipboard behavior and success confirmation. Standard-user deployer status remains unavailable because the protected configuration ACL denies access.

## Verification correction - adjacent candidate database isolation - 2026-10-02

Task 57 did not start a candidate application. The adjacent Task 56 failed starts used `--spring.data.mongodb.uri` with a Spring Boot 4.1.1 JAR. Boot 4.1.1 configuration metadata marks that key deprecated since 4.0 and replaces it with `spring.mongodb.uri`; the active Mongo properties prefix is `spring.mongodb`. The candidate MongoDB logs show no application connections. Those failed starts therefore were not proven to use the isolated fixture copies, superseding the earlier statement that no production database was configured as a target for those attempts. They may have used the host MongoDB listener's default `test` database.

The read-only migration-ledger query on 2026-10-02 found 15 records; migration 015 had already been `FAILED` since 2026-09-24, and no migration start time was later than that date. This matches the observed startup failure and shows no migration-ledger change from the October 2 attempts, but does not rule out other writes to the `test` database. No evidence indicates the application's production database was accessed or changed. Future Boot 4 candidate runs must use `SPRING_MONGODB_URI` or `--spring.mongodb.uri` and confirm a connection to the isolated port. See [Spring Boot MongoDB configuration](https://docs.spring.io/spring-boot/api/java/org/springframework/boot/mongodb/autoconfigure/MongoProperties.html).
