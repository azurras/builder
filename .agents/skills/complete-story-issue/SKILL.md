---
name: complete-story-issue
description: Use when Codex is given a story, issue, ticket, backlog item, GitHub issue, bug, feature request, or task that should be carried from intake through implementation, local app testing, test reporting, closure, and session memory without the user naming every workflow step.
---

# Complete Story Issue

## Overview

Run the default Builder delivery loop for story or issue work. Do not wait for the user to ask for each phase when the request is to complete a story, issue, ticket, bug, or feature.

## Default Loop

Unless the user explicitly asks for only one phase, execute this loop:

1. Story/Issue: capture the source item, acceptance intent, repo, branch strategy, and closing condition.
2. Spec: use `save-project-spec` when requirements or design need a durable spec before implementation.
3. Implementation Plan: use `save-implementation-plan` before coding, including status, branch, goals, ordered task breakdown, code changes, unit testing, local testing, risks, and completion criteria.
4. Develop: implement in the appropriate repo or spoke, respecting repo instructions and dirty worktrees.
5. Local Testing Against the App: run automated tests first, then run the app locally when the change affects runtime behavior. Capture exact commands, ports, URLs, data, and responses.
6. Test Report: use `save-test-report` after local app verification. Record what was tested, the data sent, responses received, pass/fail results, and evidence.
7. Close Story/Issue: close or update the source story only after implementation and testing are complete, merged, intentionally parked, or clearly documented.
8. Session Memory: use `save-session-memory` after substantive completed work, then run `update-hub-indexes`, `validate-hub-state`, and `commit-push-builder-main` for Builder artifacts.

## Operating Rules

- Start the loop from the story or issue the user provides. If the repo or issue details are missing, discover them from local context or available tools before asking.
- Ask only for blocking decisions that cannot be inferred safely.
- Keep existing focused skills focused. This skill orchestrates the sequence and calls the right specialized skill at the right phase.
- Do not close a story or issue before local testing evidence and the test report exist unless the user explicitly scopes the task to planning or investigation only.
- If a phase is not applicable, record why in the next durable artifact instead of silently skipping it.
- For hub-and-spoke work, use the hub skills: `start-hub-work`, `register-spoke-repo`, `dispatch-spoke-task`, `ingest-spoke-update`, `review-spoke-work`, and `close-hub-work` as the work shape requires.

## Completion Checklist

- [ ] Source story or issue captured.
- [ ] Spec saved or explicitly not needed.
- [ ] Implementation plan saved.
- [ ] Code implemented and verified with automated tests.
- [ ] App run locally when runtime behavior changed.
- [ ] Test report saved with data sent and responses received.
- [ ] Story or issue closed or updated with final state.
- [ ] Session memory saved.
- [ ] Builder indexes updated and hub state validated.
- [ ] Builder changes committed and pushed when durable artifacts changed.
