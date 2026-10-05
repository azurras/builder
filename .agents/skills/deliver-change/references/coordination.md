# Coordination

Use this only for an actual authorized handoff to another agent, session or person. Same-agent work does not need dispatch or return artifacts.

## Handoff

Put the handoff in the message to the recipient, using these labels:

```markdown
- Repository: <Builder or spoke slug>; locate with manage_spoke_repositories.py locate
- Branch policy: <branch or worktree to use, base commit, who publishes>
- Objective: <outcome>
- Scope: <in scope>; Non-goals: <out of scope>
- Constraints: <authority limits, data isolation, no deployment, and so on>
- Inspected targets: <files and symbols with the commit they were read at>
- Dependencies: <what must land first>
- Acceptance checks: <AC IDs from the plan and how to prove each>
- Plan: <link to the published plan>; Before-Edit Brief: <task numbers to reuse>
- Return: commits or PR, verification results with report link, blockers, actionable warnings
```

Code-changing work includes the applicable Before-Edit Brief and names write-chris-street-style-code; reuse the plan's brief when current. Record the handoff (recipient, objective, plan link) in dated memory.

## Return

Verify what comes back instead of trusting it: confirm commits exist on the remote (`git ls-remote` or `gh pr view`), read the test report and check it names the returned candidate, and rerun the plan's checks when they are cheap. Record ownership, received evidence, decisions and the next action in the dated project session file.

Blocked or parked work stays incomplete; do not close its issue unless cancellation was requested.
