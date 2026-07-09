# Christopherbell.dev Issue Discovery

- Status: `ready-to-close`
- Owner/agent context: Codex in Builder hub, coordinating issue discovery for the christopherbell.dev spoke repository.
- Objective: Inspect `/mnt/c/Users/Christopher/Developer/christopherbell.dev` for bugs and possible improvements, then create GitHub issues for validated backlog items.
- Related specs/plans: None.
- Spoke repos: `christopherbell.dev` / canonical GitHub repo `azurras/christopherbell.dev`.

## Scope

Reviewed backend security/configuration, request filtering, password reset notification, controller exception handling, and request validation patterns. No source changes were made in the spoke repository.

## GitHub Issues Created

- [#1090 Bug: production JWT can fall back to the local development signing secret](https://github.com/azurras/christopherbell.dev/issues/1090)
- [#1091 Bug: rate limiting can be bypassed by spoofing X-Forwarded-For](https://github.com/azurras/christopherbell.dev/issues/1091)
- [#1092 Bug: request size limit does not protect chunked or missing Content-Length bodies](https://github.com/azurras/christopherbell.dev/issues/1092)
- [#1093 Bug: password reset links are written to logs when email delivery is unavailable or fails](https://github.com/azurras/christopherbell.dev/issues/1093)
- [#1094 Bug: generic controller exception fallback is not registered](https://github.com/azurras/christopherbell.dev/issues/1094)
- [#1095 Enhancement: make global rate limits configurable and endpoint-aware](https://github.com/azurras/christopherbell.dev/issues/1095)
- [#1096 Enhancement: add Bean Validation to request DTOs and controller inputs](https://github.com/azurras/christopherbell.dev/issues/1096)

## Current State

The spoke repo was already heavily dirty before inspection. The investigation did not modify spoke files. The builder repo had existing modified session-memory/index files before this work; they were left in place and later hub updates were added intentionally.

## Validation

- Ran targeted tests in the spoke repo: `./gradlew :website:test --tests dev.christopherbell.configuration.RateLimitFilterTest --tests dev.christopherbell.configuration.RequestSizeLimitFilterTest --tests dev.christopherbell.account.PasswordResetNotificationServiceTest`.
- Result: build successful; selected tests passed.
- Verified canonical GitHub repo by browser redirect from `cbell504/website` to `azurras/christopherbell.dev` before creating issues.

## Blockers

None.

## Next Steps

Prioritize #1090 and #1093 before public deployment changes because they involve token handling. Then address #1091 and #1092 as request-boundary hardening, followed by #1094 and the enhancements.
