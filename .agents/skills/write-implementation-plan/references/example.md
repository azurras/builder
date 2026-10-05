# Example Implementation Plan

## Document Status
ready-for-execution

## Objective
Replace an unsafe fallback secret with required configuration.

## Goals
- Remove the insecure default.
- Fail startup when the secret is absent.
- Cover the behavior with a focused test.

## Inputs
- Story: Example issue 42.
- Repository: `example-app`.

## Branch
`codex/issue-42-require-secret` from `main`

## Non-Goals
- Rotating existing production secrets.

## Assumptions
- Configuration is loaded through `SecurityConfig`.

## Open Questions
None.

## Task Breakdown

### Task 1 - Replace fallback secret handling

Sequence / dependencies:
- First task because runtime behavior depends on the configuration source.

Implementation notes:
- Replace the hard-coded fallback with a required lookup.

#### Code Edit 1.1
- File: `src/main/java/example/SecurityConfig.java`
- Lines: 42-48
- Action: replace

Current:
```java
String jwtSecret() {
    return env.getProperty("JWT_SECRET", "dev-secret");
}
```

Proposed:
```java
String jwtSecret() {
    return Objects.requireNonNull(env.getProperty("JWT_SECRET"), "JWT_SECRET is required");
}
```

Verification:
- `./gradlew test --tests SecurityConfigTest`

## Code Changes
- Code Edit 1.1 replaces fallback secret handling in `SecurityConfig`.

## Files and Modules
- `src/main/java/example/SecurityConfig.java`
- `src/test/java/example/SecurityConfigTest.java`

## Unit Testing
- Add a test that missing `JWT_SECRET` fails startup.

## Local Testing
- Start the app with `JWT_SECRET=local-test-secret`.
- Confirm `/actuator/health` returns 200.

## Validation
- Focused test and local health check pass.

## Rollback or Recovery
- Revert the commit and restore the previous configuration behavior.

## Risks
- Local developers without `JWT_SECRET` will need to set one.

## Completion Criteria
- Test passes, local app starts with explicit secret, and issue is closed.
