# Issue 1091 Trusted Client IP Resolution Plan

## Objective
Prevent rate-limit bypass through spoofed `X-Forwarded-For` by centralizing client-IP resolution and trusting forwarded headers only from configured proxy remotes.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1091
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Planned branch: `agent/1091-trusted-client-ip-resolution`

## Assumptions
- Direct desktop access should use `request.getRemoteAddr()` regardless of caller-supplied forwarding headers.
- Trusted proxies can be configured as exact IP/CIDR values through application properties.
- The same resolver should be reused by `RateLimitFilter` and VIN decode client-key selection.

## Steps
1. Create a clean branch from updated `origin/main`.
2. Add failing unit tests for a new resolver in `website/src/test/java/dev/christopherbell/configuration/ClientIpResolverTest.java`:
   - untrusted remote with `X-Forwarded-For` returns remote address.
   - trusted remote with `X-Forwarded-For: client, proxy` returns the first client address.
   - blank or malformed forwarded headers fall back to remote address.
3. Update `RateLimitFilterTest` so spoofed `X-Forwarded-For` from one untrusted remote does not create separate buckets.
4. Update `VehicleControllerTest` so anonymous VIN decode from untrusted remote passes `ip:<remoteAddr>` even when `X-Forwarded-For` is present.
5. Implement typed properties for trusted proxies or reuse the rate-limit properties planned in issue #1095 if that branch has already landed.
6. Inject/use `ClientIpResolver` from `RateLimitFilter` and `VehicleController`; remove duplicated header parsing.
7. Update `configuration` and `vehicle` package docs.
8. Run targeted configuration and vehicle controller tests.
9. Commit, push, open a PR linked to issue #1091, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Create: `website/src/main/java/dev/christopherbell/configuration/ClientIpResolver.java`
- Create/modify: typed configuration properties for trusted proxies.
- Modify: `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitFilter.java`
- Modify: `website/src/main/java/dev/christopherbell/vehicle/VehicleController.java`
- Modify tests: `RateLimitFilterTest`, `VehicleControllerTest`, new resolver tests.
- Modify docs: `website/src/main/java/dev/christopherbell/configuration/README.md`, `website/src/main/java/dev/christopherbell/vehicle/README.md`

## Validation
- `./gradlew :website:test --tests dev.christopherbell.configuration.RateLimitFilterTest --tests dev.christopherbell.configuration.ClientIpResolverTest --tests dev.christopherbell.vehicle.VehicleControllerTest`
- Confirm spoofed headers do not change buckets unless remote is trusted.

## Rollback or Recovery
If proxy detection breaks a real deployment, add the production proxy IP/CIDR to configuration and rerun the resolver tests with that value.

## Completion Criteria
- Client IP resolution is centralized.
- Untrusted `X-Forwarded-For` cannot mint new rate-limit buckets.
- VIN decode anonymous client keys use the same resolver.
- PR merged and issue #1091 closed.
