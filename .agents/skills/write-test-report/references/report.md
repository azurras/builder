# Runtime Report Content

## Report Content

Write test reports as evidence artifacts, not chat transcripts. Use these sections, in this order, with the exact headings from [the template](template.md):

- Document Status: `draft`, `complete`, `blocked` or `superseded`, defined in the skill's Statuses table.
- Project: one slug, the spoke whose candidate ran (or `builder`, or an active project from spokes.json). publish-spoke-changes' preflight refuses a report whose Project is not the spoke.
- Story/Issue: the story, issue, ticket, or work item being verified.
- Branch: the branch and the candidate commit's short SHA, as the skill's Candidate Identity section requires.
- App / Environment: app name, runtime/configuration, database or fixture context, and relevant environment variables; include port and base URL only when applicable.
- Local Run Details: exact local command, working directory, candidate identity, process details, logs location, and cleanup. For non-HTTP runs, use a label such as `Local command:`, `Local worker launch:` or `Local consumer run:` followed by the actual invocation.
- Test Cases: the user-visible behaviors, endpoints, or flows exercised.
- Data Sent: actual request/UI input, command arguments, stdin, input file contents, queue message or consumer input, as applicable.
- Response Received: actual HTTP/UI response, exit code/status, stdout/stderr, output file/artifact contents, worker result, logs or screenshots, as applicable.
- Pass / Fail: result per test case and a short reason.
- Evidence: commands, timestamps, screenshots, curl output files, browser checks, or log excerpts.
- Bugs / Follow-ups: defects found, retest needs, superseded candidates, or gaps intentionally left unverified. Write `None` when there are none.

Do not require references to specs or implementation plans. Include those links only when they are directly useful for traceability. Record deployment proof only when deployment was in scope.

## What the Validator Requires

Every report has all eleven sections and a known status; Data Sent, Response Received, Pass / Fail and Evidence must not be empty. A `complete` report must also show:

- **A local application run** in App / Environment, Local Run Details or Evidence: a `Local command:` style line whose command is not a test runner, or a localhost, `127.0.0.1`, port or base URL reference.
- **Runtime input** in Data Sent: a request, UI input, command arguments, fixture input or queue message.
- **Runtime output** in Response Received: an application response, UI result, exit status, output artifact, worker result or log output.

A report whose only evidence is `npm test`, `pytest`, `./gradlew test`, `mvn test` or similar automated test output fails. Mentioning those checks is fine alongside a real local run.
