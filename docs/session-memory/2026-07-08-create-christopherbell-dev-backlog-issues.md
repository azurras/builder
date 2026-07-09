# 2026-07-08 - Create christopherbell.dev backlog issues

## 19:52 - Create christopherbell.dev backlog issues

### Request
The user asked to search for issues and possible improvements in the `developer/christopherbell.dev` repo and create GitHub issues for bugs and enhancements.

### Project Context
The active hub is `/mnt/c/Users/Christopher/Developer/builder`. The target spoke repo is `/mnt/c/Users/Christopher/Developer/christopherbell.dev`, a Java 21 / Spring Boot monolith with MongoDB, Thymeleaf templates, and vanilla JavaScript. The spoke repo was already heavily dirty before inspection; no source edits were made there. Its local origin is `https://github.com/cbell504/website.git`, which redirects publicly to the canonical GitHub repo `azurras/christopherbell.dev`.

### Work Completed
Created Builder work ledger `docs/work/2026-07-08-christopherbell-dev-issue-discovery.md` and registered the spoke in `docs/spokes/repos.md`. Created seven GitHub issues in `azurras/christopherbell.dev`:

- #1090 production JWT can fall back to local development signing secret.
- #1091 rate limiting can be bypassed by spoofing `X-Forwarded-For`.
- #1092 request size limit does not protect chunked or missing `Content-Length` bodies.
- #1093 password reset links are written to logs when email delivery is unavailable or fails.
- #1094 generic controller exception fallback is not registered.
- #1095 enhancement to make global rate limits configurable and endpoint-aware.
- #1096 enhancement to add Bean Validation to request DTOs and controller inputs.

### Decisions
Used the GitHub connector for issue creation because `gh` was not installed in the environment. Initial issue creation against `cbell504/website` returned empty snapshots; browser verification showed GitHub redirects that repo to `azurras/christopherbell.dev`, so issues were created against the canonical repo. Did not apply labels because the repo label set was not verified and unknown labels can fail issue creation.

### Validation
Ran targeted spoke tests: `./gradlew :website:test --tests dev.christopherbell.configuration.RateLimitFilterTest --tests dev.christopherbell.configuration.RequestSizeLimitFilterTest --tests dev.christopherbell.account.PasswordResetNotificationServiceTest`. Result: build successful and selected tests passed. Ran Builder `update_hub_indexes.py` and `validate_hub_state.py`; validation passed before this memory entry.

### Current State
Builder hub artifacts are modified and need final index refresh, validation, and guarded commit/push to `main`. The spoke repo remains dirty with pre-existing user changes plus Gradle build output/test artifacts from validation; no source files were edited by this session.

### Follow-ups
Prioritize issue #1090 and #1093 before deployment hardening because they involve token handling. Then address #1091/#1092 request-boundary hardening, #1094 API consistency, and the two enhancements.
