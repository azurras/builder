# Issue 1095 Endpoint Aware Rate Limits Plan

## Objective
Replace the hard-coded global `10000` requests/minute rate limit with typed configuration and endpoint-aware bucket policies for sensitive public mutations, public reads, static assets, and default traffic.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1095
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Planned branch: `agent/1095-configurable-endpoint-rate-limits`
- Related dependency: issue #1091 should land first so trusted client IP resolution is shared.

## Assumptions
- Bucket4j remains the rate-limit implementation.
- Defaults should be conservative for auth mutations but permissive for static assets and normal reads.
- Config should be simple enough to tune from YAML without code changes.

## Steps
1. Create a clean branch from updated `origin/main` after issue #1091 merges.
2. Add failing tests in `RateLimitFilterTest`:
   - auth mutation paths use a stricter bucket than static assets.
   - static assets and default routes use their configured groups.
   - changing group capacity/window in properties changes behavior without code changes.
   - trusted proxy behavior is controlled by the shared resolver/properties.
3. Create typed properties such as `RateLimitProperties` with group policies containing path matchers, HTTP methods when useful, capacity, and window duration.
4. Refactor `RateLimitFilter` to select a policy per request, key buckets by `group + clientIp`, and create Bucket4j buckets from the selected policy.
5. Wire `RateLimitFilter` in `SecurityConfig` with properties and `ClientIpResolver`.
6. Add defaults to `application.yml`, including stricter auth/password-reset/signup/VIN-decode mutation limits.
7. Document defaults and tuning in `website/src/main/java/dev/christopherbell/configuration/README.md` and `configuration/filter/README.md`.
8. Run targeted rate-limit/security tests.
9. Commit, push, open a PR linked to issue #1095, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Create/modify: `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitProperties.java`
- Modify: `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitFilter.java`
- Modify: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Modify: `website/src/main/resources/application.yml`
- Modify tests: `website/src/test/java/dev/christopherbell/configuration/RateLimitFilterTest.java`, maybe `SecurityConfigTest`
- Modify docs: `configuration/README.md`, `configuration/filter/README.md`

## Validation
- `./gradlew :website:test --tests dev.christopherbell.configuration.RateLimitFilterTest --tests dev.christopherbell.configuration.SecurityConfigTest`
- Confirm sensitive public mutations use stricter defaults than static assets/default routes.

## Rollback or Recovery
If endpoint matching causes false positives in production, revert to a single default group through configuration while retaining the typed properties path for future tuning.

## Completion Criteria
- No hard-coded `10000` global default remains as the only policy.
- Rate limits are configurable and endpoint-aware.
- PR merged and issue #1095 closed.
