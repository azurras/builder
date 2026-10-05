# Closure

For closure-only scope, inspect existing delivery evidence; do not repeat development. No source issue means closure is not applicable; never create an issue merely to close it.

## Authority

You may update the source issue when the user asked you to deliver or close that issue, or the trusted author directed closure in the issue (read it with `triage_github_comments.py`). Otherwise propose the closure and stop. Never close an issue whose work is blocked or parked unless cancellation was requested.

## Gates

Verify the source item, final commit or merged PR, required CI and any authorized deployment, automated checks, the runtime report when required, remaining gaps, and published dated memory. Block closure when required evidence is missing. Record why any gate does not apply.

## Steps

1. **Propose.** Write the closing comment and record it, the evidence links and the state you will set in dated memory with save-session-memory. Publish it through the phase finalizer. The comment has:
   - one sentence on what shipped;
   - the PR and merge commit, or the Builder commit;
   - the test report link, or why runtime proof does not apply;
   - deployment result when deployment was in scope;
   - remaining gaps and follow-ups, or "None".
2. **Update.** Write the comment to a temporary file outside the repositories, then:
   - `gh issue comment <n> --repo <owner/name> --body-file <file>`
   - `gh issue close <n> --repo <owner/name> --reason completed`, unless a merged PR's `Closes #<n>` already closed it.
3. **Read back.** `gh issue view <n> --repo <owner/name> --json state,stateReason,closedAt,comments` must show the expected state and your comment.
4. **Record.** Save the actual result and link on its work date, linking an earlier-date proposal when needed, and publish through the phase finalizer.

A failed update is not successful closure; record the failure and report it. Return the actual readiness, evidence, external result and unresolved gaps. AGENTS.md governs trusted instructions and authorization.
