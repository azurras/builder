# Runtime Report Content

## Report Content

Write test reports as evidence artifacts, not chat transcripts. Every test report should include:

- Document Status: draft, complete, blocked, or superseded.
- Story/Issue: the story, issue, ticket, or work item being verified.
- Branch: the branch, commit, or build under test.
- App / Environment: app name, profile, port, base URL, database or fixture context, and relevant environment variables.
- Local Run Details: exact start command, process details, logs location, and whether the app was stopped or left running.
- Test Cases: the user-visible behaviors, endpoints, or flows exercised.
- Data Sent: request method, URL, headers that matter, payload/body/form data, query params, or UI input values.
- Response Received: status code, response headers that matter, body snippets, UI result, redirects, logs, or screenshots.
- Pass / Fail: result per test case and a short reason.
- Evidence: commands, timestamps, screenshots, curl output files, browser checks, or log excerpts.
- Bugs / Follow-ups: defects found, retest needs, or gaps intentionally left unverified.

Do not write a report whose only evidence is `npm test`, `pytest`, `./gradlew test`, `mvn test`, or similar automated test output. Do not require references to specs or implementation plans. Include those links only when they are directly useful for traceability.


Use `docs/templates/test-report.md`; status is draft, complete, blocked, or superseded. Record candidate identity and cleanup, plus deployment proof only when deployment was in scope.
