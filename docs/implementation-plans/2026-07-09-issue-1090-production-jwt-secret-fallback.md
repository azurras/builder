# Issue 1090 Production JWT Secret Fallback Plan

## Objective
Prevent the production profile from silently using the local development JWT signing secret when `APP_JWT_SECRET` or `app.jwt.secret` is blank or weak.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1090
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Base branch: latest `main` after issue #1094 merges
- Planned branch: `agent/1090-prod-jwt-secret-required`

## Assumptions
- Local development should remain easy with an explicit local fallback from default/local configuration.
- Production detection can rely on Spring profile binding rather than static environment probing inside token parsing paths.

## Steps
1. Create a clean branch from updated `origin/main` after prior PR merge.
2. Add failing tests in `website/src/test/java/dev/christopherbell/permission/PermissionServiceTest.java` or a focused configuration test:
   - production profile with blank configured secret throws `IllegalStateException`.
   - production profile with a too-short secret throws `IllegalStateException`.
   - local/default profile with blank configured secret still uses the local development fallback.
   - explicit strong configured secret works.
3. Refactor `PermissionService` so instance property binding captures active profiles and configured secret before calling a small resolver.
4. Keep static token generation/validation working through the configured `Key`, but make fallback profile-aware and production-hostile.
5. Update `website/src/main/java/dev/christopherbell/permission/README.md` and root `README.md` production notes if needed to state production requires a strong JWT secret.
6. Run targeted permission tests.
7. Commit, push, open a PR linked to issue #1090, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Modify: `website/src/main/java/dev/christopherbell/permission/PermissionService.java`
- Modify: `website/src/test/java/dev/christopherbell/permission/PermissionServiceTest.java`
- Modify docs: `website/src/main/java/dev/christopherbell/permission/README.md`, maybe `README.md`

## Validation
- `./gradlew :website:test --tests dev.christopherbell.permission.PermissionServiceTest`
- Confirm production blank and weak secrets fail fast while local fallback remains available.

## Rollback or Recovery
If startup behavior blocks local development, revert the PR and restore the prior local fallback while keeping the production tests as the design target.

## Completion Criteria
- Production cannot start with blank or weak JWT secret.
- Local/default development fallback still works.
- PR merged and issue #1090 closed.
