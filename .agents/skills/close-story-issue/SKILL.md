---
name: close-story-issue
description: Use when Codex is ready to close or update a story, issue, ticket, GitHub issue, bug, or feature request after implementation, automated verification, local app testing, test reporting, and session memory are complete.
---

# Close Story Issue

## Overview

Close stories and issues only after evidence exists. This skill is the closure gate for the Builder delivery loop.

## Closure Checklist

Before closing or posting a final issue update, verify and include:

- Source story/issue URL or identifier.
- Final branch, commit, and PR or merge state.
- Spec status or reason it was not needed.
- Implementation plan path and status.
- Automated test commands and results.
- Local app test report path, including data sent and response received.
- Known gaps, follow-ups, or risks.
- Session memory path.
- Exact closure or status-update text.

## Rules

- Do not close the story/issue if local app testing was required but no test report exists.
- Do not close the story/issue if implementation is unmerged or intentionally parked unless the update explicitly says so.
- If a closure condition is not applicable, state why in the closure text.

## Output Shape

```markdown
## Closure Readiness
ready | blocked

## Evidence
- ...

## Closure Text
...
```
