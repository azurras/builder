# Issue 1093 Password Reset Token Logging Plan

## Objective
Remove usable password reset URLs and tokens from logs while preserving safe mail-failure diagnostics.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1093
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Planned branch: `agent/1093-password-reset-log-safety`

## Assumptions
- Development token delivery can be omitted unless there is an existing explicit config need; the acceptance criteria only require full URL logging to be removed or safely gated.
- The reset email body may still contain the full reset URL because that is the intended user delivery channel.

## Steps
1. Create a clean branch from updated `origin/main`.
2. Add log-capture tests in `PasswordResetNotificationServiceTest`:
   - missing `JavaMailSender` logs account id but not the reset URL or token.
   - `MailException` logs account id but not the reset URL or token.
   - successful send still sends an email containing the reset URL.
3. Update `PasswordResetNotificationService` so no warning/error path includes `resetUrl`.
4. If a local-dev diagnostic is retained, make it explicit configuration and never log a usable token by default.
5. Update `website/src/main/java/dev/christopherbell/account/passwordreset/README.md` to document that reset tokens are never logged.
6. Run focused account/password reset tests.
7. Commit, push, open a PR linked to issue #1093, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Modify: `website/src/main/java/dev/christopherbell/account/passwordreset/PasswordResetNotificationService.java`
- Modify: `website/src/test/java/dev/christopherbell/account/PasswordResetNotificationServiceTest.java`
- Modify docs: `website/src/main/java/dev/christopherbell/account/passwordreset/README.md`

## Validation
- `./gradlew :website:test --tests dev.christopherbell.account.PasswordResetNotificationServiceTest`
- Inspect logs captured by tests to prove token and full reset URL are absent.

## Rollback or Recovery
If local password reset workflows require visibility into links, add an explicit local-only sink that displays a non-production reset URL outside production logs.

## Completion Criteria
- No error or missing-mail-sender log contains a usable reset token or URL.
- Reset email sending remains functional.
- PR merged and issue #1093 closed.
