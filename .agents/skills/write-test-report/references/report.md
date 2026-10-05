# Runtime Report Content

## Report Content

Write test reports as evidence artifacts, not chat transcripts. Start with a `# <Change>: Test Report` title, then use these sections, in this order, with the exact headings from [the template](template.md):

- Story/Issue: the story, issue, ticket, or work item being verified.
- Branch: the branch and the candidate commit's short SHA, as the skill's Candidate Identity section requires.
- Pass / Fail: the verdict, placed right after Branch so it is the first thing a reader sees. Open with a callout giving the count and candidate (`> [!TIP]` when everything passed, `> [!WARNING]` for any failure, `> [!CAUTION]` when blocked), then a table: #, Test case, Result (✅ PASS, ❌ FAIL or ⏸️ BLOCKED), Why.
- Test Cases: a numbered list matching the Pass / Fail rows, each a bold case name and the user-visible behavior, endpoint, or flow exercised.
- App / Environment: a Setting, Value table with the app name, runtime/configuration, database or fixture context, and relevant environment variables; include port and base URL only when applicable.
- Local Run Details: bold-labeled bullets for the exact local command, working directory, candidate identity, process details, logs location, and cleanup. Label the invocation `**Local command:**` (or `**Local worker launch:**`, `**Local consumer run:**` for non-HTTP runs) with the command inline in backticks.
- Data Sent: one `### N. Case name` subsection per test case, each with the actual request/UI input, command arguments, stdin, input file contents, queue message or consumer input in a fenced block (`http`, `json` or `text`).
- Response Received: the same numbered subsections, each with the actual HTTP/UI response, exit code/status, stdout/stderr, output file/artifact contents, worker result, logs or screenshots in a fenced block. Wrap output longer than about 30 lines in `<details>` with a one-line summary.
- Evidence: commands, timestamps, screenshots, curl output files, browser checks, or log excerpts.
- Bugs / Follow-ups: defects found, retest needs, superseded candidates, or gaps intentionally left unverified. Write `None` when there are none.
- Document Status: `draft`, `complete`, `blocked` or `superseded`, defined in the skill's Statuses table. It and Project close the report as metadata; the Pass / Fail callout carries the outcome for readers.
- Project: one slug, the spoke whose candidate ran (or `builder`, or an active project from spokes.json). publish-spoke-changes' preflight refuses a report whose Project is not the spoke.

Do not require references to specs or implementation plans. Include those links only when they are directly useful for traceability. Record deployment proof only when deployment was in scope.

## Presentation

People read reports on GitHub, usually to answer "did it work, and on what?". Present the evidence so that answer comes first:

- **Verdict first.** Story and candidate, then Pass / Fail. Environment and run details follow for the reader who needs them; Document Status and Project close the report.
- **One number per case.** The same `N` and case name appear in Pass / Fail, Test Cases, Data Sent and Response Received, so a reader can follow one case down the page.
- **Raw evidence in fenced blocks.** Requests, commands and output go in fenced blocks with a language tag, never in prose. Sanitize secrets inside them.
- **Tables for settings and results; prose only for judgement.** Explain a failure, blocker or surprising result in a sentence under the table, not inside it.
- **Plain machine values.** Document Status and Project stay bare values on their own line; the save helper and the spoke preflight read them by heading, not position.

## What the Validator Requires

Every report has all eleven sections and a known status; Data Sent, Response Received, Pass / Fail and Evidence must not be empty. A `complete` report must also show:

- **A local application run** in App / Environment, Local Run Details or Evidence: a `Local command:` style label (plain, bold or as a table row) whose command is not a test runner, or a localhost, `127.0.0.1`, port or base URL reference.
- **Runtime input** in Data Sent: a request, UI input, command arguments, fixture input or queue message.
- **Runtime output** in Response Received: an application response, UI result, exit status, output artifact, worker result or log output.

A report whose only evidence is `npm test`, `pytest`, `./gradlew test`, `mvn test` or similar automated test output fails. Mentioning those checks is fine alongside a real local run.
