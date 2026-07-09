# Issue 1096 Bean Validation Request DTO Plan

## Objective
Add Jakarta Bean Validation annotations to public mutation request DTOs and `@Valid` controller inputs so malformed payloads return a consistent HTTP 400 `Response` envelope before reaching services.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1096
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Planned branch: `agent/1096-bean-validation-request-dtos`
- Dependency: issue #1094 generic/shared exception handler should land first.

## Assumptions
- The project may need `spring-boot-starter-validation` added to `website/build.gradle.kts`.
- Service-level validation should not be removed unless redundant and safely covered by tests.
- Representative invalid-payload controller tests are enough for the first pass, focused on public mutation DTOs named in the issue.

## Steps
1. Create a clean branch from updated `origin/main` after issue #1094 merges.
2. Add failing controller tests for representative invalid payloads:
   - account create blank/invalid email returns 400 envelope and does not call service.
   - post create blank or too-long text returns 400 envelope and does not call service.
   - report create blank post id/reason returns 400 envelope and does not call service.
   - VIN decode invalid VIN shape returns 400 envelope and does not call service.
3. Add `spring-boot-starter-validation` if `jakarta.validation` annotations are unavailable.
4. Add constraints to DTO records/builders:
   - `AccountCreateRequest`: names, email, password, username constraints.
   - `AccountLoginRequest`, password reset request/confirm, and account update where public mutations accept bodies.
   - `PostCreateRequest`: `text` not blank, max 280; optional `parentId` size if applicable.
   - `ReportCreateRequest`: required post id and reason, bounded details.
   - `VehicleVinDecodeRequest` and VIN request DTOs: not blank, VIN length/pattern.
5. Add `@Valid` to controller `@RequestBody` parameters for the constrained DTOs.
6. Add `MethodArgumentNotValidException` handling in `ControllerExceptionHandler` with HTTP 400 and standard `Response` envelope.
7. Update feature READMEs for account, post, report, vehicle model/API validation behavior.
8. Run targeted controller tests, then `./gradlew :website:test` because validation may affect multiple MVC slices.
9. Commit, push, open a PR linked to issue #1096, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Modify: `website/build.gradle.kts`
- Modify: `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`
- Modify DTOs under `account/model`, `account/model/dto`, `post/model`, `report/model`, and `vehicle/model`
- Modify controllers using these DTOs: `AccountController`, `PostController`, `ReportController`, `VehicleController`
- Modify tests: `AccountControllerTest`, `PostControllerTest`, `ReportControllerTest`, `VehicleControllerTest`
- Modify docs: relevant package READMEs

## Validation
- Targeted controller tests for invalid payloads.
- `./gradlew :website:test`
- Confirm validation errors use HTTP 400 and standard envelope, and services are not invoked for invalid bodies.

## Rollback or Recovery
If validation constraints reject existing legitimate payloads, loosen the affected constraint and keep the controller test that documents the intended boundary.

## Completion Criteria
- Public mutation DTOs have useful Jakarta validation constraints.
- Controllers use `@Valid` for constrained bodies.
- Validation failures return HTTP 400 `Response` envelopes.
- PR merged and issue #1096 closed.
