# Issue 1092 Request Body Size Enforcement Plan

## Objective
Enforce request body limits even when `Content-Length` is missing, chunked, or untrusted, and return HTTP 413 consistently when the read limit is exceeded.

## Inputs
- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1092
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- Planned branch: `agent/1092-request-size-read-limit`

## Assumptions
- The existing `RequestSizeLimitFilter` remains the right ownership point for application-level protection.
- The filter should preserve declared-length rejection and add read-time enforcement for unknown lengths.

## Steps
1. Create a clean branch from updated `origin/main`.
2. Add failing tests in `RequestSizeLimitFilterTest`:
   - declared large `Content-Length` is rejected before the chain.
   - missing content length with a body over the limit returns 413 when downstream reads the body.
   - missing content length with a body under the limit passes through and is readable.
3. Implement a request wrapper and limiting `ServletInputStream`/`BufferedReader` path that throws or signals once more than `maxSizeBytes` is read.
4. Catch the limit exception in the filter and set HTTP 413 without continuing response writes.
5. Keep the default max size unchanged unless configuration already exists in a merged rate-limit/request-limit properties change.
6. Update `website/src/main/java/dev/christopherbell/configuration/filter/README.md` to document declared-length and read-time enforcement.
7. Run focused request-size tests and wider security config tests if filter wiring changes.
8. Commit, push, open a PR linked to issue #1092, verify the PR diff, merge it, and close the issue after merge.

## Files and Modules
- Modify: `website/src/main/java/dev/christopherbell/configuration/filter/RequestSizeLimitFilter.java`
- Modify: `website/src/test/java/dev/christopherbell/configuration/RequestSizeLimitFilterTest.java`
- Modify docs: `website/src/main/java/dev/christopherbell/configuration/filter/README.md`

## Validation
- `./gradlew :website:test --tests dev.christopherbell.configuration.RequestSizeLimitFilterTest`
- Confirm oversized unknown-length reads return 413 and do not reach normal controller handling.

## Rollback or Recovery
If the wrapper breaks multipart or normal JSON parsing, revert the PR and move enforcement to container-level max request settings plus targeted MVC tests.

## Completion Criteria
- Unknown-length oversized bodies are rejected during read.
- Existing declared-length behavior still works.
- PR merged and issue #1092 closed.
