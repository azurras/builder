# Runtime Report Content

## Report Content

Write test reports as evidence artifacts, not chat transcripts. Every test report should include:

- Document Status: draft, complete, blocked, or superseded.
- Story/Issue: the story, issue, ticket, or work item being verified.
- Branch: the branch, commit, or build under test.
- App / Environment: app name, runtime/configuration, database or fixture context, and relevant environment variables; include port and base URL only when applicable.
- Local Run Details: exact local command, working directory, candidate identity, process details, logs location, and cleanup. For non-HTTP runs, use a label such as `Local command:`, `Local worker launch:` or `Local consumer run:` followed by the actual invocation.
- Test Cases: the user-visible behaviors, endpoints, or flows exercised.
- Data Sent: actual request/UI input, command arguments, stdin, input file contents, queue message or consumer input, as applicable.
- Response Received: actual HTTP/UI response, exit code/status, stdout/stderr, output file/artifact contents, worker result, logs or screenshots, as applicable.
- Pass / Fail: result per test case and a short reason.
- Evidence: commands, timestamps, screenshots, curl output files, browser checks, or log excerpts.
- Bugs / Follow-ups: defects found, retest needs, or gaps intentionally left unverified.

Do not write a report whose only evidence is `npm test`, `pytest`, `./gradlew test`, `mvn test`, or similar automated test output. Do not require references to specs or implementation plans. Include those links only when they are directly useful for traceability.


Use [the report template](template.md); status is draft, complete, blocked, or superseded. Record candidate identity and cleanup, plus deployment proof only when deployment was in scope.
