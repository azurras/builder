# Issue 1094 Generic Controller Exception Fallback Plan

## Objective
Register the shared generic controller exception handler so unexpected controller exceptions return the standard `Response` envelope with HTTP 500.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1094
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Base branch: `origin/main`
- Planned branch: `agent/1094-generic-exception-handler`

## Assumptions
- `ControllerExceptionHandler` in `cbell-lib` is imported by representative `@WebMvcTest` suites.
- Existing specific exception handlers must keep their current status codes and response shapes.

## Steps
1. Create a clean branch from `origin/main` in an isolated worktree.
2. Add a failing controller-level test proving a thrown `RuntimeException` returns status 500 and `$.success == false` with code `INTERNAL_SERVER_ERROR`.
3. Update `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`:
   - Rename `handelGenericException` to `handleGenericException`.
   - Add `@ExceptionHandler(Exception.class)`.
   - Add `@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)`.
4. Run the focused failing test and confirm it passes after implementation.
5. Run `./gradlew :website:test --tests dev.christopherbell.vehicle.VehicleControllerTest` or the exact test class used for the regression.
6. Commit, push, open a PR linked to issue #1094, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Modify: `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`
- Modify test: a representative controller test, preferably `website/src/test/java/dev/christopherbell/vehicle/VehicleControllerTest.java`

## Validation
- Targeted controller test for generic 500 envelope.
- Full affected module test command if the targeted suite exposes wider regressions.
- PR diff review before merge.

## Rollback or Recovery
Revert the PR merge if the generic handler changes specific exception behavior. Specific handlers should remain more specific than `Exception.class` and continue to win.

## Completion Criteria
- Unexpected controller exceptions return HTTP 500 in the standard envelope.
- Existing specific exception tests still pass.
- PR merged and issue #1094 closed.
